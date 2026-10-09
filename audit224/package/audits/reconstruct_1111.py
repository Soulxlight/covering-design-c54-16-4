"""Portable extraction of independently reviewed case 1111 reconstruction.
See PROVENANCE.json for source hashes and exact extraction rule.
"""
import itertools
from collections import Counter
from fractions import Fraction as Q
from math import comb as C

def need(ok, msg):
    if not ok:
        raise ValueError(msg)

def reconstruct():
    pop = {0: 50, 1: 4}
    slots = [(a, b, C(pop[a], 2) if a == b else pop[a] * pop[b], min(36 + 15 * a, 36 + 15 * b, 48 + min(a, b))) for a, b in itertools.combinations_with_replacement(pop, 2)]
    variables, rows = ([], [])

    def var(n, u, c=0):
        variables.append(dict(name=n, lower=0, upper=u, objective=c))

    def row(n, a, l=0, u=0):
        rows.append(dict(label=n, coefficients={k: v for k, v in a.items() if v}, lower=l, upper=u))

    def mc(e):
        return min(43, 15 if e <= 1 else 18 + e)

    def qc(m):
        return 2 if m == 4 else min(m, 35)
    for s in range(17):
        var(f'n{s}', C(223, 2))
    for e in range(50):
        var(f'p{e}', C(54, 2))
    for m in range(4, 44):
        var(f't{m}', C(54, 3))
    for h in range(1, 36):
        var(f'q{h}', C(54, 4))
    for a, b, size, cap in slots:
        for e in range(cap + 1):
            var(f'J{a}_{b}_{e}', size)
    for e in range(50):
        for m in range(4, mc(e) + 1):
            var(f'M{e}_{m}', 52 * C(54, 2))
    for m in range(4, 44):
        for h in range(1, qc(m) + 1):
            var(f'N{m}_{h}', 51 * C(54, 3))
    for n, u in [('z3p', C(54, 3) * C(43, 2)), ('z3m', C(223, 2) * C(16, 3)), ('z4p', C(54, 4) * C(35, 2)), ('z4m', C(223, 2) * C(16, 4))]:
        var(n, u, -1)
    row('block_pairs', {f'n{s}': 1 for s in range(17)}, C(223, 2), C(223, 2))
    point_moment = sum((pop[d] * C(66 + d, 2) for d in pop))
    row('point_moment', {f'n{s}': s for s in range(17)}, point_moment, point_moment)
    row('pair_count', {f'p{e}': 1 for e in range(50)}, C(54, 2), C(54, 2))
    excess = 223 * C(16, 2) - 18 * C(54, 2)
    row('pair_excess', {f'p{e}': e for e in range(50)}, excess, excess)
    row('pair_moment', {**{f'n{s}': C(s, 2) for s in range(17)}, **{f'p{e}': -C(18 + e, 2) for e in range(50)}})
    row('triple_count', {f't{m}': 1 for m in range(4, 44)}, C(54, 3), C(54, 3))
    row('triple_load', {f't{m}': m for m in range(4, 44)}, 223 * C(16, 3), 223 * C(16, 3))
    row('quad_count', {f'q{h}': 1 for h in range(1, 36)}, C(54, 4), C(54, 4))
    row('quad_load', {f'q{h}': h for h in range(1, 36)}, 223 * C(16, 4), 223 * C(16, 4))
    row('tight_intersection3', {'n3': 1, 't4': -5}, 0, None)
    row('tight_intersection4', {'n4': 4, 't4': -1}, 0, None)
    row('tight_pair_transport', {'M0_4': 1, 'p0': -8}, 0, None)
    row('one_high_triple', {f't{m}': -1 for m in range(37, 44)}, -1, None)
    row('one_high_quad', {f'q{h}': -1 for h in range(31, 36)}, -1, None)
    for a, b, size, cap in slots:
        row(f'joint_count{a}_{b}', {f'J{a}_{b}_{e}': 1 for e in range(cap + 1)}, size, size)
    for e in range(50):
        row(f'joint_column{e}', {**{f'J{a}_{b}_{e}': 1 for a, b, size, cap in slots if e <= cap}, f'p{e}': -1})
    for d in pop:
        row(f'joint_vertex_load{d}', {f'J{a}_{b}_{e}': e * (int(a == d) + int(b == d)) for a, b, size, cap in slots for e in range(cap + 1) if d in (a, b)}, pop[d] * (36 + 15 * d), pop[d] * (36 + 15 * d))
    for e in range(50):
        row(f'transport_count{e}', {**{f'M{e}_{m}': 1 for m in range(4, mc(e) + 1)}, f'p{e}': -52})
        row(f'transport_load{e}', {**{f'M{e}_{m}': m for m in range(4, mc(e) + 1)}, f'p{e}': -14 * (18 + e)})
    for m in range(4, 44):
        row(f'transport_column{m}', {**{f'M{e}_{m}': 1 for e in range(50) if m <= mc(e)}, f't{m}': -3})
        row(f'quad_transport_count{m}', {**{f'N{m}_{h}': 1 for h in range(1, qc(m) + 1)}, f't{m}': -51})
        row(f'quad_transport_load{m}', {**{f'N{m}_{h}': h for h in range(1, qc(m) + 1)}, f't{m}': -13 * m})
    for h in range(1, 36):
        row(f'quad_transport_column{h}', {**{f'N{m}_{h}': 1 for m in range(4, 44) if h <= qc(m)}, f'q{h}': -4})
    for j in (3, 4):
        row(f'moment{j}_defect', {**{f"{('t' if j == 3 else 'q')}{h}": C(h, 2) for h in range(4 if j == 3 else 1, 44 if j == 3 else 36)}, **{f'n{s}': -C(s, j) for s in range(17)}, f'z{j}p': -1, f'z{j}m': 1})
    for h in range(37, 44):
        row(f'exceptional_link_{h}', {**{f'J1_1_{e}': 1 for e in range(h - 18, 50)}, **{f't{m}': -3 for m in range(h, 44)}}, 0, None)
    for h in range(19, 44):
        coefs = {f't{m}': -3 for m in range(h, 44)}
        for a, b, size, cap in slots:
            for e in range(h - 18, cap + 1):
                capacity = min(52, (36 + 15 * a - e) // (h - 18), (36 + 15 * b - e) // (h - 18))
                need(capacity >= 0, 'nonnegative reconstructed capacity')
                coefs[f'J{a}_{b}_{e}'] = capacity
        row(f'endpoint_residual_link_{h}', coefs, 0, None)
    return (variables, rows)
V, R = reconstruct()

def validate(model):
    need(model['variables'] == V, 'all reconstructed variables/bounds/objectives')
    need(model['rows'] == R, 'all reconstructed rows, coefficients and bounds')
    expected = {'case': '1111', 'partition': [1, 1, 1, 1], 'populations': {'0': 50, '1': 4}, 'parameters': [54, 16, 4, 223], 'floors': {'point': 66, 'pair': 18, 'triple': 4, 'quad': 1}, 'point_excess_total': 4, 'pair_excess_total': 1002, 'point_intersection_moment': 116094, 'pair_excess_cap': 49, 'triple_cap': 43, 'quad_cap': 35}
    for k, v in expected.items():
        need(model[k] == v, 'parameter ' + k)
