"""Exhaustively verify the pinned335-block witness with point-incidence integers."""
import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WITNESS = ROOT / 'data' / 'cover-335.txt'
EXPECTED_SHA256 = 'f00db8b4253b98fecf412031948e7de4e5c5f78a9cc021ef483bb01ea9d84bc8'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def parse_blocks(raw):
    lines = raw.decode('ascii').splitlines()
    need(len(lines) == 335, 'expected335 block lines')
    rows, seen = [], set()
    for number, line in enumerate(lines, 1):
        cells = line.split()
        need(len(cells) == 16 and all(len(x) == 2 and x.isdigit() for x in cells),
             'expected16 two-digit labels on line ' + str(number))
        row = tuple(sorted(int(x) for x in cells))
        need(len(set(row)) == 16 and all(1 <= x <= 54 for x in row),
             'repeated or out-of-range point on line ' + str(number))
        need(row not in seen, 'repeated whole block on line ' + str(number))
        seen.add(row); rows.append(row)
    return rows


def build_columns(rows, points=54):
    columns = [0] * (points + 1)
    for index, row in enumerate(rows):
        for point in row:
            need(1 <= point <= points, 'point outside incidence frame')
            columns[point] |= 1 << index
    return columns


def covered(columns, quadruple):
    a, b, c, d = quadruple
    return bool(columns[a] & columns[b] & columns[c] & columns[d])


def self_test():
    rows = ((1, 2, 3, 4), (4, 5, 6, 7))
    columns = build_columns(rows, 8)
    count = 0
    for quadruple in itertools.combinations(range(1, 9), 4):
        value = covered(columns, quadruple)
        need(value == (quadruple in rows), '8-label boundary control')
        count += value
    need(count == 2, 'boundary-control count')


def verify(path=WITNESS):
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    need(len(raw) == 16415 and digest == EXPECTED_SHA256, 'pinned witness byte identity')
    rows = parse_blocks(raw); columns = build_columns(rows)
    self_test()
    checked = covered_count = 0
    holes = []
    for quadruple in itertools.combinations(range(1, 55), 4):
        checked += 1
        if covered(columns, quadruple):
            covered_count += 1
        elif len(holes) < 100:
            holes.append(list(quadruple))
    missing = checked - covered_count
    need(checked == 316251, 'full four-subset universe')
    need(missing == 0, 'witness has uncovered quadruples: ' + str(missing))
    return dict(status='PASS_COMPLETE_COVER_335', method='Python integer point-incidence intersection',
                witness='data/cover-335.txt', source_sha256=digest, bytes=len(raw),
                points=54, block_size=16, legal_blocks=len(rows), distinct_blocks=len(rows),
                quadruples_checked=checked, covered=covered_count, uncovered=missing,
                holes=holes, control_quadruples=70, upper_bound=335, optimality_claimed=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cover', type=Path, default=WITNESS,
                        help='An exact copy of the pinned witness')
    args = parser.parse_args()
    print(json.dumps(verify(args.cover), indent=2, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, UnicodeError) as error:
        print('FAIL_CLOSED: ' + str(error), file=sys.stderr)
        sys.exit(1)
