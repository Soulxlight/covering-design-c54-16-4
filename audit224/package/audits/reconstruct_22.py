"""Portable extraction of independently reviewed case 22 reconstruction.
See PROVENANCE.json for source hashes and exact extraction rule.
"""
import itertools as it
from collections import Counter
from fractions import Fraction as F
from math import comb

def need(x, message):
    if not x:
        raise ValueError(message)

def reconstruct():
    V, R = ([], [])
    classes = [(0, 0, comb(52, 2), 36), (0, 2, 104, 36), (2, 2, 1, 50)]

    def v(n, U, c=0):
        V.append({'name': n, 'lower': 0, 'upper': U, 'objective': c})

    def r(n, a, L=0, U=0):
        R.append({'label': n, 'coefficients': {k: x for k, x in a.items() if x}, 'lower': L, 'upper': U})

    def cells(prefix, lo, hi, value):
        return {prefix + str(i): value(i) for i in range(lo, hi + 1)}

    def mc(e):
        return min(36, 15 if e in (0, 1) else 18 + e)

    def qc(m):
        return 2 if m == 4 else min(m, 30)
    for s in range(17):
        v(f'n{s}', comb(223, 2))
    for e in range(51):
        v(f'p{e}', comb(54, 2))
    for m in range(4, 37):
        v(f't{m}', comb(54, 3))
    for h in range(1, 31):
        v(f'q{h}', comb(54, 4))
    for a, b, count, cap in classes:
        for e in range(cap + 1):
            v(f'J{a}_{b}_{e}', count)
    for e in range(51):
        for m in range(4, mc(e) + 1):
            v(f'M{e}_{m}', 52 * comb(54, 2))
    for m in range(4, 37):
        for h in range(1, qc(m) + 1):
            v(f'N{m}_{h}', 51 * comb(54, 3))
    for n, U in [('z3p', comb(54, 3) * comb(36, 2)), ('z3m', comb(223, 2) * comb(16, 3)), ('z4p', comb(54, 4) * comb(30, 2)), ('z4m', comb(223, 2) * comb(16, 4))]:
        v(n, U, -1)
    r('block_pairs', cells('n', 0, 16, lambda s: 1), comb(223, 2), comb(223, 2))
    I = 52 * comb(66, 2) + 2 * comb(68, 2)
    r('point_moment', cells('n', 0, 16, lambda s: s), I, I)
    r('pair_count', cells('p', 0, 50, lambda e: 1), comb(54, 2), comb(54, 2))
    E = 223 * comb(16, 2) - 18 * comb(54, 2)
    r('pair_excess', cells('p', 0, 50, lambda e: e), E, E)
    r('pair_moment', {**cells('n', 0, 16, lambda s: comb(s, 2)), **cells('p', 0, 50, lambda e: -comb(18 + e, 2))})
    for prefix, lo, hi, s, label in [('t', 4, 36, 3, 'triple'), ('q', 1, 30, 4, 'quad')]:
        r(label + '_count', cells(prefix, lo, hi, lambda i: 1), comb(54, s), comb(54, s))
        r(label + '_load', cells(prefix, lo, hi, lambda i: i), 223 * comb(16, s), 223 * comb(16, s))
    r('tight_intersection3', {'n3': 1, 't4': -5}, 0, None)
    r('tight_intersection4', {'n4': 4, 't4': -1}, 0, None)
    r('tight_pair_transport', {'M0_4': 1, 'p0': -8}, 0, None)
    for a, b, count, cap in classes:
        r(f'joint_count{a}_{b}', cells(f'J{a}_{b}_', 0, cap, lambda e: 1), count, count)
    for e in range(51):
        r(f'joint_column{e}', {**{f'J{a}_{b}_{e}': 1 for a, b, count, cap in classes if e <= cap}, f'p{e}': -1})
    for c, pop in [(0, 52), (2, 2)]:
        co = {f'J{a}_{b}_{e}': e * (int(a == c) + int(b == c)) for a, b, count, cap in classes for e in range(cap + 1)}
        r(f'joint_vertex_load{c}', co, pop * (36 + 15 * c), pop * (36 + 15 * c))
    for e in range(51):
        r(f'transport_count{e}', {**cells(f'M{e}_', 4, mc(e), lambda m: 1), f'p{e}': -52})
        r(f'transport_load{e}', {**cells(f'M{e}_', 4, mc(e), lambda m: m), f'p{e}': -14 * (18 + e)})
    for m in range(4, 37):
        r(f'transport_column{m}', {**{f'M{e}_{m}': 1 for e in range(51) if m <= mc(e)}, f't{m}': -3})
        r(f'quad_transport_count{m}', {**cells(f'N{m}_', 1, qc(m), lambda h: 1), f't{m}': -51})
        r(f'quad_transport_load{m}', {**cells(f'N{m}_', 1, qc(m), lambda h: h), f't{m}': -13 * m})
    for h in range(1, 31):
        r(f'quad_transport_column{h}', {**{f'N{m}_{h}': 1 for m in range(4, 37) if h <= qc(m)}, f'q{h}': -4})
    for s in (3, 4):
        r(f'moment{s}_defect', {**cells('t' if s == 3 else 'q', 4 if s == 3 else 1, 36 if s == 3 else 30, lambda i: comb(i, 2)), **cells('n', 0, 16, lambda i: -comb(i, s)), f'z{s}p': -1, f'z{s}m': 1})
    need(len(R) == 301, 'reconstructed base size')
    capchecks = 0
    for h in range(19, 37):
        co = cells('t', h, 36, lambda m: -3)
        for a, b, count, jcap in classes:
            for e in range(jcap + 1):
                least = 36 if a == 0 else 66
                cap = 0 if e < h - 18 else min(52, (least - e) // (h - 18))
                both = 0 if e < h - 18 else min(52, (36 + 15 * a - e) // (h - 18), (36 + 15 * b - e) // (h - 18))
                need(cap == both and cap >= 0, 'case-specific ordinary/exceptional endpoint cap')
                if cap:
                    co[f'J{a}_{b}_{e}'] = cap
                capchecks += 1
        r(f'endpoint_residual_link_{h}', co, 0, None)
    need(len(V) == 2402 and len(R) == 319, 'fresh dimensions')
    return (V, R, capchecks)
V, R, CAPCHECKS = reconstruct()
META = {'case': '22', 'partition': [2, 2], 'populations': {'0': 52, '2': 2}, 'parameters': [54, 16, 4, 223], 'floors': {'point': 66, 'pair': 18, 'triple': 4, 'quad': 1}, 'point_excess_total': 4, 'pair_excess_total': 1002, 'point_intersection_moment': 116096, 'pair_excess_cap': 50, 'triple_cap': 36, 'quad_cap': 30}

def validate(m):
    for v in m['variables']:
        for key in ('lower', 'upper', 'objective'):
            need(type(v[key]) is int, 'integral variable ' + key)
    for r in m['rows']:
        need(type(r['lower']) is int and (r['upper'] is None or type(r['upper']) is int), 'integral row endpoints')
        need(all((type(a) is int for a in r['coefficients'].values())), 'integral coefficients')
    need(m['variables'] == V, 'complete independent variables and finite bounds')
    need(m['rows'] == R, 'complete independent row order, bounds, coefficients')
    for k, x in META.items():
        need(m[k] == x, 'metadata ' + k)
    need(m['endpoint_extension']['thresholds'] == list(range(19, 37)), 'complete endpoint thresholds')
    need(m['endpoint_extension']['added_rows'] == 18 and m['endpoint_extension']['new_variables'] == 0, 'extension dimensions')
    need(m['endpoint_extension']['raw_exceptional_degree36_cap_not_tightened'] is True, 'raw exceptional capacity flag')
    need(all((R[-1]['coefficients'][f'J2_2_{e}'] == 2 for e in range(18, 31))), 'all raw capacity2 cells retained')
