#!/usr/bin/env python3
"""Compile and replay the recorded winning WLS run in a separate work directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work-dir',type=Path)
    p.add_argument('--seconds',type=float,help='Override recorded wall-clock budget on a slower machine')
    p.add_argument('--native',action='store_true',help='Retain original -march=native compilation flag')
    p.add_argument('--compile-only',action='store_true')
    args=p.parse_args()
    record=json.loads((ROOT/'reproduction/REPLAY.json').read_text())
    work=args.work_dir.resolve() if args.work_dir else Path(tempfile.mkdtemp(prefix='cover-replay-'))
    if work.is_relative_to(ROOT):
        raise ValueError('Use a work directory outside this immutable packet')
    if work.exists() and any(work.iterdir()):
        raise ValueError('Replay work directory must be empty')
    work.mkdir(parents=True,exist_ok=True)
    binary=work/'cover-search'
    command=[str(binary) if token=='@BINARY@' else token for token in record['compile_argv']]
    if not args.native:
        command=[token for token in command if token!='-march=native']
    subprocess.run(command,cwd=ROOT/'reproduction/source',check=True)
    if args.compile_only:
        print(json.dumps({'status':'COMPILED','binary':str(binary),'compile_argv':command},indent=2))
        return
    env=os.environ.copy()
    for key in record['cleared_environment_variables']:
        env.pop(key,None)
    env.update(record['algorithm_environment'])
    env.update({key:value.replace('@WORK_DIR@',str(work)) for key,value in record.get('checkpoint_environment',{}).items()})
    env['SAVE_PARTIAL']=str(work/'best_partial.txt')
    argv=[str(binary) if token=='@BINARY@' else str(ROOT/'reproduction/input.txt') if token=='@INPUT@' else token for token in record['run_argv']]
    if args.seconds is not None:
        if args.seconds<=0:raise ValueError('Seconds must be positive')
        argv[5]=str(args.seconds)
    with (work/'replay.log').open('w') as stream:
        process=subprocess.run(argv,cwd=work,env=env,stdout=stream,stderr=subprocess.STDOUT)
    if process.returncode:
        raise SystemExit('Search process failed with status '+str(process.returncode)+'; see '+str(work/'replay.log'))
    candidate=work/record['expected_output_filename']
    receipt={'process_returncode':process.returncode,'work_directory':str(work),
             'input_blocks':record['input_blocks'],'input_uncovered':record['input_uncovered'],
             'target_blocks':record['target_blocks'],'targetB':record.get('targetB',record['target_blocks']),
             'reproduced_cover_present':candidate.exists(), 'optimality_claimed':False}
    if candidate.exists():
        receipts=[]
        for command in [[sys.executable,'-B',str(ROOT/'verification/verify_colex.py'),'54','16','4',str(candidate)],
                        [sys.executable,'-B',str(ROOT/'verification/verify_incidence.py'),str(candidate),'--expected-blocks',str(record['target_blocks'])]]:
            check=subprocess.run(command,capture_output=True,text=True)
            if check.returncode:raise ValueError('Replayed output failed exhaustive verification: '+check.stdout+check.stderr)
            receipts.append(json.loads(check.stdout))
        receipt['sha256']=hashlib.sha256(candidate.read_bytes()).hexdigest()
        receipt['same_exact_witness']=receipt['sha256']==record['expected_witness_sha256']
        receipt['verification']=receipts
    (work/'REPLAY_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
    if not candidate.exists():
        raise SystemExit('Target not reached within the wall-clock budget; see replay.log. A longer --seconds budget may be needed.')


if __name__=='__main__':
    main()
