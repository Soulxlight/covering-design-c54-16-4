#!/usr/bin/env python3
"""Exact two-row replacement SAT backend; real runs require the leased owner.

All point and row indices in this API are zero-based. Residual targets are
derived from the full parent, never supplied by a caller. No complete pair
sweep or global lower-bound claim follows from a bounded invocation.
"""
import collections
import itertools
import math
import threading
import time
from dataclasses import dataclass

from pysat.solvers import Minicard


def require(condition, message):
    if not condition:
        raise ValueError(message)


def legal_rows(rows, v, k):
    result = []
    for row in rows:
        require(len(row) == k and len(set(row)) == k, 'Wrong row cardinality')
        require(all(type(p) is int and 0 <= p < v for p in row), 'Invalid point')
        result.append(tuple(sorted(row)))
    return tuple(result)


def incidence_holes(rows, v, t):
    incidence = [0] * v
    for i, row in enumerate(rows):
        for p in row:
            incidence[p] |= 1 << i
    missing = []
    for q in itertools.combinations(range(v), t):
        owners = incidence[q[0]]
        for p in q[1:]:
            owners &= incidence[p]
        if not owners:
            missing.append(q)
    return tuple(missing)


@dataclass(frozen=True)
class Profile:
    v: int
    k: int
    t: int
    rows: tuple
    holes: tuple
    private: tuple
    doubles: dict

    @classmethod
    def build(cls, rows, v, k, t):
        require(all(type(x) is int for x in (v, k, t)), 'Noninteger parameters')
        require(1 <= t <= k <= v, 'Invalid parameters')
        rows = legal_rows(rows, v, k)
        require(len(rows) >= 2, 'Need two parent rows')
        owners = {}
        for i, row in enumerate(rows):
            bit = 1 << i
            for q in itertools.combinations(row, t):
                owners[q] = owners.get(q, 0) | bit
        private = [[] for _ in rows]
        doubles = collections.defaultdict(list)
        holes = []
        for q in itertools.combinations(range(v), t):
            mask = owners.get(q, 0)
            count = mask.bit_count()
            if count == 0:
                holes.append(q)
            elif count == 1:
                private[mask.bit_length() - 1].append(q)
            elif count == 2:
                low = mask & -mask
                pair = (low.bit_length() - 1, (mask ^ low).bit_length() - 1)
                doubles[pair].append(q)
        # Independent point-incidence construction verifies the deficit.
        require(tuple(holes) == incidence_holes(rows, v, t), 'Parent audit mismatch')
        return cls(v, k, t, rows, tuple(holes),
                   tuple(tuple(qs) for qs in private),
                   {pair: tuple(qs) for pair, qs in doubles.items()})

    def residual(self, pair):
        require(len(pair) == 2 and all(type(i) is int for i in pair), 'Invalid pair')
        i, j = sorted(pair)
        require(0 <= i < j < len(self.rows), 'Pair out of range or repeated')
        result = (self.holes + self.private[i] + self.private[j]
                  + self.doubles.get((i, j), ()))
        require(len(set(result)) == len(result), 'Residual ownership partition overlaps')
        return (i, j), tuple(sorted(result))


class Encoded:
    """Owns a MiniCard instance; use as a context manager."""

    def __init__(self, profile, pair, budget, heavy=True, forced_covered=()):
        require(isinstance(profile, Profile), 'Expected freshly built Profile')
        require(type(budget) is int and budget >= 0, 'Invalid defect budget')
        require(type(heavy) is bool, 'Invalid heavy-constraint flag')
        self.profile = profile
        self.pair, self.residual = profile.residual(pair)
        self.budget = budget
        self.heavy = heavy
        required = set(tuple(q) for q in forced_covered)
        require(required <= set(self.residual), 'Forced target outside residual')
        self.required = required
        self.solver = Minicard(use_timer=True)
        self.next_variable = 0
        self.membership = []
        self.cache = [{}, {}]
        self.defects = []
        self.heavy_vertices = 0
        self.heavy_edges = 0
        try:
            phases = []
            for row in self.pair:
                xs = [self.variable() for _ in range(profile.v)]
                self.membership.append(xs)
                self.solver.add_atmost(xs, profile.k)
                self.solver.add_atmost([-x for x in xs], profile.v - profile.k)
                parent = set(profile.rows[row])
                phases.extend(x if p in parent else -x for p, x in enumerate(xs))
            if heavy:
                vertices = collections.Counter(p for q in self.residual for p in q)
                edges = collections.Counter(e for q in self.residual
                                            for e in itertools.combinations(q, 2))
                for p, count in vertices.items():
                    if count > budget:
                        self.solver.add_clause([self.membership[0][p], self.membership[1][p]])
                        self.heavy_vertices += 1
                for e, count in edges.items():
                    if count > budget:
                        self.solver.add_clause([self.conjunction(0, e), self.conjunction(1, e)])
                        self.heavy_edges += 1
            old_holes = set(profile.holes)
            for q in self.residual:
                owners = [self.conjunction(r, q) for r in (0, 1)]
                if budget > 0 and q not in required:
                    hole = self.variable()
                    self.defects.append(hole)
                    self.solver.add_clause(owners + [hole])
                    for owner in owners:
                        self.solver.add_clause([-owner, -hole])
                    phases.append(hole if q in old_holes else -hole)
                else:
                    self.solver.add_clause(owners)
            if self.defects:
                self.solver.add_atmost(self.defects, min(budget, len(self.defects)))
            self.solver.set_phases(phases)
        except BaseException:
            self.solver.delete()
            raise

    def variable(self):
        self.next_variable += 1
        return self.next_variable

    def conjunction(self, row, points):
        points = tuple(points)
        if len(points) == 1:
            return self.membership[row][points[0]]
        if points not in self.cache[row]:
            z = self.variable()
            xs = [self.membership[row][p] for p in points]
            for x in xs:
                self.solver.add_clause([-z, x])
            self.solver.add_clause([z] + [-x for x in xs])
            self.cache[row][points] = z
        return self.cache[row][points]

    def assumptions(self, replacement_rows):
        rows = legal_rows(replacement_rows, self.profile.v, self.profile.k)
        require(len(rows) == 2, 'Expected exactly two replacement rows')
        return [x if p in row else -x
                for xs, row in zip(self.membership, map(set, rows))
                for p, x in enumerate(xs)]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.solver.delete()


def solve(profile, pair, budget, seconds, heavy=True, forced_covered=(),
          fixed_rows=None, progress=None):
    require(type(seconds) in (int, float) and math.isfinite(seconds) and seconds > 0,
            'Invalid native duration')
    setup_start = time.monotonic()
    with Encoded(profile, pair, budget, heavy, forced_covered) as model:
        assumptions = model.assumptions(fixed_rows) if fixed_rows is not None else []
        started = time.monotonic()
        if progress is not None:
            progress({'stage': 'search_started', 'pair': model.pair,
                      'native_start_monotonic': started,
                      'native_deadline_monotonic': started + seconds})
        timer = threading.Timer(seconds, model.solver.interrupt)
        timer.start()
        try:
            outcome = model.solver.solve_limited(assumptions=assumptions, expect_interrupt=True)
        finally:
            timer.cancel()
            timer.join()
        finished = time.monotonic()
        status = 'SAT' if outcome is True else 'UNSAT' if outcome is False else 'UNKNOWN'
        if progress is not None:
            progress({'stage': 'search_finished', 'pair': model.pair,
                      'native_status': status, 'native_finish_monotonic': finished})
        result = {'status': status, 'parameters': [profile.v, profile.k, profile.t],
                  'point_label_base': 0, 'row_index_base': 0, 'pair': model.pair,
                  'budget': budget, 'parent_deficit': len(profile.holes),
                  'residual_targets': len(model.residual), 'heavy_constraints': heavy,
                  'heavy_vertices': model.heavy_vertices, 'heavy_edges': model.heavy_edges,
                  'variables': model.next_variable, 'setup_seconds': started - setup_start,
                  'native_seconds': finished - started, 'seconds_requested': seconds,
                  'statistics': model.solver.accum_stats(),
                  'scope': 'Only arbitrary replacements of this pinned pair of rows.'}
        if outcome is True:
            positive = {x for x in model.solver.get_model() if x > 0}
            replacements = tuple(tuple(p for p, x in enumerate(xs) if x in positive)
                                 for xs in model.membership)
            replacements = legal_rows(replacements, profile.v, profile.k)
            full_rows = list(profile.rows)
            for index, row in zip(model.pair, replacements):
                full_rows[index] = row
            # A fixed original-parent control reconstructs the identical family.
            # Profile.build independently audited precisely this normalized family.
            # All free SAT solutions and changed fixed controls still rebuild
            # the complete point-incidence coverage independently.
            reused_parent = fixed_rows is not None and tuple(full_rows) == profile.rows
            holes = (profile.holes if reused_parent else
                     incidence_holes(full_rows, profile.v, profile.t))
            result['reused_verified_original_parent'] = reused_parent
            require(len(holes) <= budget, 'SAT decoding fails independent full coverage audit')
            require(not (set(holes) & model.required), 'Forced target remains uncovered')
            require(set(holes) <= set(model.residual), 'Hole outside exact residual')
            result.update(replacement_rows=replacements, missing_targets=holes,
                          predicted_holes=len(holes), rows=full_rows)
        return result
