#!/usr/bin/env python3
"""Strict, exhaustive verifier for ordinary C(v,k,t) covers.

Usage: python verify_cover.py v k t blocks.txt
One block per nonempty line, containing exactly k distinct integers in 1..v.
This implementation uses a colex-ranked byte array and no search-engine state.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


def verify(path, v, k, t):
    if not 0 <= t <= k <= v:
        raise ValueError("Require 0 <= t <= k <= v")
    data = Path(path).read_bytes()
    blocks = []
    seen = set()
    for line_no, line in enumerate(data.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = tuple(sorted(map(int, line.split())))
        if len(row) != k or len(set(row)) != k:
            raise ValueError(f"Line {line_no}: expected exactly {k} distinct points")
        if any(p < 1 or p > v for p in row):
            raise ValueError(f"Line {line_no}: point outside 1..{v}")
        if row in seen:
            raise ValueError(f"Line {line_no}: duplicate block")
        seen.add(row)
        blocks.append(tuple(p - 1 for p in row))
    total = math.comb(v, t)
    covered = bytearray(total)
    choose = [[math.comb(p, j) if p >= j else 0 for j in range(t + 1)]
              for p in range(v)]
    for block in blocks:
        for target in itertools.combinations(block, t):
            rank = sum(choose[p][j] for j, p in enumerate(target, 1))
            covered[rank] = 1
    missing = covered.count(0)
    return {"parameters": [v, k, t], "blocks": len(blocks),
            "total_targets": total, "covered_targets": total - missing,
            "uncovered_targets": missing, "valid": missing == 0,
            "sha256": hashlib.sha256(data).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("v", "k", "t"):
        parser.add_argument(name, type=int)
    parser.add_argument("path")
    args = parser.parse_args()
    try:
        result = verify(args.path, args.v, args.k, args.t)
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}))
        raise SystemExit(2)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["valid"] else 1)
