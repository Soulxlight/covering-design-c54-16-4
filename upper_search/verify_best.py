#!/usr/bin/env python3
"""Check the pinned best witness with two independent exhaustive algorithms."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check():
    record = json.loads((ROOT / 'upper_search/RESULT.json').read_text())
    path = ROOT / record['witness']
    if not path.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Witness must be inside the project')
    if record['parameters'] != [54, 16, 4]:
        raise ValueError('Incorrect parameters')
    count = record['blocks']
    if type(count) is not int or not 1 <= count < 335:
        raise ValueError('Expected an improved positive block count')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != record['sha256']:
        raise ValueError('Pinned witness hash mismatch')
    flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
    results = []
    for arguments in [
        ['upper334/verify_colex.py', '54', '16', '4', str(path)],
        ['upper334/verify_incidence.py', str(path), '--expected-blocks', str(count)],
    ]:
        process = subprocess.run([sys.executable, *flags, *arguments], cwd=ROOT,
                                 text=True, capture_output=True, timeout=30)
        if process.returncode:
            raise ValueError('Exhaustive verification failed: ' + process.stdout + process.stderr)
        results.append(json.loads(process.stdout))
    colex, incidence = results
    if not (colex['valid'] is True and colex['blocks'] == count
            and colex['total_targets'] == 316251 and colex['uncovered_targets'] == 0
            and colex['sha256'] == digest):
        raise ValueError('Colex result inconsistent with the pinned record')
    if not (incidence['status'] == 'PASS' and incidence['blocks'] == count
            and incidence['distinct_blocks'] == count and incidence['all_blocks_legal'] is True
            and incidence['quadruples_checked'] == 316251
            and incidence['uncovered_quadruples'] == 0
            and incidence['candidate_sha256'] == digest):
        raise ValueError('Incidence result inconsistent with the pinned record')
    return {'status': 'PASS', 'parameters': [54, 16, 4], 'blocks': count,
            'distinct_blocks': count, 'covered_quadruples': 316251,
            'uncovered_quadruples': 0, 'sha256': digest,
            'independent_methods': ['colex subset enumeration', 'point-incidence intersections'],
            'optimality_claimed': False}


if __name__ == '__main__':
    try:
        print(json.dumps(check(), indent=2, sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
