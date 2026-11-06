#!/usr/bin/env python3
"""Exhaustively verify a C(54,16,4) witness using point-incidence bitsets.

This verifier uses no combinatorial ranking and no search-engine state.
Defaults to ../data/cover-334.txt, requiring exactly 334 distinct blocks.
Only Python's standard library is needed.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path


def verify(candidate, expected_blocks=334):
    raw = candidate.read_bytes()
    rows = [tuple(map(int, line.split()))
            for line in raw.decode('ascii').splitlines() if line.strip()]
    if len(rows) != expected_blocks:
        raise ValueError(f'Expected {expected_blocks} rows, found {len(rows)}')
    for line, row in enumerate(rows, 1):
        if len(row) != 16 or len(set(row)) != 16 or min(row) < 1 or max(row) > 54:
            raise ValueError(f'Illegal block at nonempty line {line}: {row}')
    normalized = [tuple(sorted(row)) for row in rows]
    if len(set(normalized)) != len(rows):
        raise ValueError('Duplicate blocks')
    columns = [0] * 55
    for index, row in enumerate(rows):
        for point in row:
            columns[point] |= 1 << index
    multiplicities = collections.Counter()
    first_holes = []
    checked = 0
    for a, b, c, d in itertools.combinations(range(1, 55), 4):
        hit = columns[a] & columns[b] & columns[c] & columns[d]
        multiplicities[hit.bit_count()] += 1
        checked += 1
        if not hit and len(first_holes) < 20:
            first_holes.append([a, b, c, d])
    missing = multiplicities[0]
    return {
        'method': 'Point-incidence integer bitset intersections over every increasing quadruple',
        'candidate_sha256': hashlib.sha256(raw).hexdigest(),
        'candidate_bytes': len(raw),
        'parameters': {'v': 54, 'k': 16, 't': 4},
        'blocks': len(rows),
        'distinct_blocks': len(set(normalized)),
        'all_blocks_legal': True,
        'quadruples_checked': checked,
        'covered_quadruples': checked - missing,
        'uncovered_quadruples': missing,
        'first_uncovered_quadruples': first_holes,
        'coverage_multiplicity_histogram': dict(sorted(multiplicities.items())),
        'total_coverage_incidence': sum(k * v for k, v in multiplicities.items()),
        'status': 'PASS' if checked == 316251 and not missing else 'FAIL',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?', type=Path,
                        default=Path(__file__).resolve().parent.parent / 'data/cover-334.txt')
    parser.add_argument('--expected-blocks', type=int, default=334)
    args = parser.parse_args()
    try:
        receipt = verify(args.path, args.expected_blocks)
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}))
        return 2
    print(json.dumps(receipt, indent=2))
    return 0 if receipt['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
