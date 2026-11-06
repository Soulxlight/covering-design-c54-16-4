#!/usr/bin/env python3
"""Run malformed-input and uncovered-target controls against both verifiers."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    package = Path(__file__).resolve().parent
    lines = (package.parent / 'data/cover-334.txt').read_text().splitlines()
    first = lines[0].split()
    rest = '\n'.join(lines[1:]) + '\n'
    variants = {
        'duplicate_point': ' '.join([first[0]] + first[:-1]) + '\n' + rest,
        'point_out_of_range': ' '.join(['55'] + first[1:]) + '\n' + rest,
        'short_block': ' '.join(first[:-1]) + '\n' + rest,
        'duplicate_block': '\n'.join([lines[1]] + lines[1:]) + '\n',
        'noninteger': ' '.join(['bad'] + first[1:]) + '\n' + rest,
        'removed_first_block': rest,
    }
    commands = {
        'colex': [sys.executable, '-B', str(package / 'verify_colex.py'), '54', '16', '4'],
        'incidence': [sys.executable, '-B', str(package / 'verify_incidence.py')],
    }
    receipts = []
    with tempfile.TemporaryDirectory(prefix='c54-controls-') as tmp:
        for name, text in variants.items():
            path = Path(tmp) / (name + '.txt')
            path.write_text(text)
            for verifier, command in commands.items():
                # For the shortened cover, test actual missing coverage rather
                # than only the count check in the incidence verifier.
                opts = ['--expected-blocks', '333'] if verifier == 'incidence' and name == 'removed_first_block' else []
                run = subprocess.run(command + [str(path)] + opts,
                                     capture_output=True, text=True)
                if run.returncode == 0:
                    raise RuntimeError(f'{verifier} incorrectly accepted {name}')
                result = json.loads(run.stdout)
                if name == 'removed_first_block':
                    key = 'uncovered_targets' if verifier == 'colex' else 'uncovered_quadruples'
                    if result.get(key, 0) <= 0:
                        raise RuntimeError(f'{verifier} did not detect actual coverage loss')
                receipts.append({'control': name, 'verifier': verifier,
                                 'exit_code': run.returncode,
                                 'correctly_rejected': True, 'result': result})
    print(json.dumps(receipts, indent=2))


if __name__ == '__main__':
    main()
