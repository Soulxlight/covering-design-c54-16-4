#!/usr/bin/env python3
"""Literal projected controls for the generic selected-row soft SAT backend."""
import itertools
import json
import time

from solve import Encoded, Profile, incidence_holes, require, solve


def literal_missing(rows, v, t):
    covered = {q for row in rows for q in itertools.combinations(sorted(row), t)}
    return set(itertools.combinations(range(v), t)) - covered


def main():
    start = time.monotonic()
    fixtures = [
        (5, 3, 2, [(0, 1, 2), (0, 3, 4), (1, 2, 3), (1, 2, 4)]),
        (5, 3, 2, [(0, 1, 2), (0, 1, 3), (2, 3, 4)]),
        (5, 3, 3, [(0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 2, 3),
                   (0, 2, 4), (0, 3, 4), (1, 2, 3), (1, 2, 4)]),
        (4, 2, 1, [(0, 1), (0, 2), (2, 3)]),
        (3, 2, 2, [(0, 1), (0, 2), (1, 2)]),
    ]
    counters = {'fixtures': 0, 'residual_checks': 0, 'projected_checks': 0,
                'positive_controls': 0, 'changed_fixed_controls': 0, 'free_solves': 0, 'forced_checks': 0,
                'rejected_inputs': 0, 'model_equivalence_checks': 0}
    for v, k, t, rows in fixtures:
        profile = Profile.build(rows, v, k, t)
        require(set(profile.holes) == literal_missing(rows, v, t), 'Parent literal mismatch')
        legal = list(itertools.combinations(range(v), k))
        pairs = (list(itertools.combinations(range(len(rows)), 2)) +
                 list(itertools.combinations(range(len(rows)), 3)))
        # All pair indices for the first two fixtures; bounded representative
        # pair indices for larger fixture, all replacement projections retained.
        pairs = pairs if len(pairs) <= 6 else [pairs[0], pairs[-1], pairs[len(pairs)//2]]
        budgets = sorted({0, 1, len(profile.holes), len(profile.holes) + 1})
        for pair in pairs:
            _, residual = profile.residual(pair)
            fixed = [r for i, r in enumerate(rows) if i not in pair]
            require(set(residual) == literal_missing(fixed, v, t), 'Residual partition mismatch')
            counters['residual_checks'] += 1
            for budget in budgets:
                expected_any = False
                for heavy in (False, True):
                    with Encoded(profile, pair, budget, heavy=heavy) as model:
                        for replacements in itertools.product(legal, repeat=len(pair)):
                            full = fixed + list(replacements)
                            missing = literal_missing(full, v, t)
                            expected = len(missing) <= budget
                            answer = model.solver.solve(assumptions=model.assumptions(replacements))
                            require(answer is expected, 'Projected SAT feasibility mismatch')
                            expected_any |= expected
                            counters['projected_checks'] += 1
                        counters['model_equivalence_checks'] += 1
                    answer = solve(profile, pair, budget, 1.0, heavy=heavy)
                    require(answer['status'] in ('SAT', 'UNSAT'), 'Tiny free solve was inconclusive')
                    require((answer['status'] == 'SAT') is expected_any, 'Free native mismatch')
                    if answer['status'] == 'SAT':
                        require(answer['reused_verified_original_parent'] is False, 'Free SAT skipped independent audit')
                        require(set(map(tuple, answer['missing_targets'])) ==
                                literal_missing(answer['rows'], v, t), 'Decoded literal mismatch')
                    counters['free_solves'] += 1
                if residual:
                    forced = residual[:1]
                    with Encoded(profile, pair, budget, forced_covered=forced) as model:
                        for replacements in itertools.product(legal, repeat=len(pair)):
                            missing = literal_missing(fixed + list(replacements), v, t)
                            expected = len(missing) <= budget and not (set(forced) & missing)
                            answer = model.solver.solve(assumptions=model.assumptions(replacements))
                            require(answer is expected, 'Forced projection mismatch')
                            counters['forced_checks'] += 1
            control = solve(profile, pair, len(profile.holes), 1.0,
                            fixed_rows=[profile.rows[i] for i in pair])
            require(control['status'] == 'SAT' and
                    control['predicted_holes'] == len(profile.holes), 'Original-parent control failed')
            require(control['reused_verified_original_parent'] is True, 'Original control did not reuse checked family')
            counters['positive_controls'] += 1
            changed = [legal[-1]] * len(pair)
            changed_control = solve(profile, pair, len(list(itertools.combinations(range(v), t))),
                                    1.0, fixed_rows=changed)
            require(changed_control['status'] == 'SAT' and
                    changed_control['reused_verified_original_parent'] is False,
                    'Changed fixed control bypassed independent audit')
            require(set(map(tuple, changed_control['missing_targets'])) ==
                    literal_missing(fixed + changed, v, t), 'Changed fixed audit mismatch')
            counters['changed_fixed_controls'] += 1
        counters['fixtures'] += 1
    p = Profile.build(fixtures[0][3], 5, 3, 2)
    rejects = [
        lambda: Profile.build([(0, 0, 1), (1, 2, 3)], 5, 3, 2),
        lambda: Profile.build([(0, 1, 5), (1, 2, 3)], 5, 3, 2),
        lambda: Profile.build([(0, 1, 2), (1, 2, 3)], 5, 3, 0),
        lambda: Profile.build([(0, 1, 2)], 5, 3, 2),
        lambda: p.residual((0, 0)), lambda: p.residual((0, 99)),
        lambda: p.residual((False, 1)), lambda: Encoded(p, (0, 1), -1),
        lambda: Encoded(p, (0, 1), True),
        lambda: Encoded(p, (0, 1), 0, forced_covered=[(99,)]),
        lambda: solve(p, (0, 1), 0, 0),
        lambda: solve(p, (0, 1), 0, float('nan')),
    ]
    for bad in rejects:
        try:
            bad()
        except ValueError:
            counters['rejected_inputs'] += 1
        else:
            raise RuntimeError('Invalid input was accepted')
    print(json.dumps({'status': 'PASS', **counters, 'seconds': time.monotonic()-start}, sort_keys=True))


if __name__ == '__main__':
    main()
