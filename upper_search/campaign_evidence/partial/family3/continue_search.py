#!/usr/bin/env python3
"""Start a new search from the verified partial in a fresh external work directory."""
import argparse,json,math,os,subprocess,sys,tempfile
from pathlib import Path
from verify_partial import check,verify_packet
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work-dir',type=Path);p.add_argument('--seconds',type=float,default=3600);p.add_argument('--seed',type=int);p.add_argument('--native',action='store_true');p.add_argument('--compile-only',action='store_true');a=p.parse_args()
if not math.isfinite(a.seconds) or a.seconds<=0:raise ValueError('Seconds must be positive and finite')
pinned=verify_packet(True);record=json.loads((ROOT/'CONTINUATION.json').read_text());work=a.work_dir.resolve() if a.work_dir else Path(tempfile.mkdtemp(prefix='c54-partial-continuation-'))
if work.is_relative_to(ROOT):raise ValueError('Work directory must be outside this immutable packet')
if work.exists() and any(work.iterdir()):raise ValueError('Work directory must be empty')
work.mkdir(parents=True,exist_ok=True);binary=work/'cover-search';command=[str(binary) if x=='@BINARY@' else x for x in record['compile_argv']]
if not a.native:command=[x for x in command if x!='-march=native']
subprocess.run(command,cwd=ROOT/record.get('source_directory','producer/source'),check=True)
if a.compile_only:print(json.dumps({'status':'COMPILED_ONLY','partial_is_a_cover':False,'work_directory':str(work),'compile_argv':command},indent=2));raise SystemExit(0)
env=os.environ.copy()
for key in record['cleared_environment_variables']:env.pop(key,None)
env.update(record['algorithm_environment']);env.update({k:v.replace('@WORK_DIR@',str(work)) for k,v in record['checkpoint_environment'].items()});env['SAVE_PARTIAL']=str(work/'best_partial.txt')
seed=record['seed'] if a.seed is None else a.seed;argv=[str(binary),'54','16','4',str(record['input_blocks']),str(a.seconds),str(seed),str(ROOT/'partial.txt'),str(record['tenure']),str(record['noise']),str(record['targetB'])]
with (work/'search.log').open('w') as stream:process=subprocess.run(argv,cwd=work,env=env,stdout=stream,stderr=subprocess.STDOUT)
if process.returncode:raise SystemExit('Search failed with status '+str(process.returncode)+'; see '+str(work/'search.log'))
full=[]
for path in sorted(work.glob('shrink_cover_54_16_4_*_'+str(seed)+'.txt')):
 count=int(path.name.split('_')[-2]);receipt=check(path,count)
 if not receipt['is_complete_cover'] or count>record['targetB']:raise ValueError('Search emitted an invalid complete-cover claim')
 full.append({'path':str(path),'verification':receipt})
if full:
 full.sort(key=lambda item:item['verification']['blocks']);result={'status':'NEW_COMPLETE_COVER_VERIFIED','is_complete_cover':True,'covers':full,'work_directory':str(work)};exit_code=0
else:
 path=work/'best_partial.txt'
 if not path.is_file():raise ValueError('Search produced neither a cover nor an initialized partial')
 count=sum(bool(line.strip()) for line in path.read_text().splitlines());receipt=check(path,count)
 if count>record['targetB'] or count<=0:raise ValueError('Invalid output block count')
 result={'status':'NEW_COMPLETE_COVER_VERIFIED' if receipt['is_complete_cover'] else 'PARTIAL_NOT_A_COVER','is_complete_cover':receipt['is_complete_cover'],'best_partial_path':str(path),'verification':receipt,'work_directory':str(work)};exit_code=0 if receipt['is_complete_cover'] else 1
(work/'CONTINUATION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(exit_code)
