"""Regenerate all17 reviewed negative fixtures and reject them under both modes."""
import argparse,copy,hashlib,json,shutil,subprocess,sys,tempfile,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work-dir',type=Path);args=parser.parse_args()
    if args.work_dir:need(args.work_dir.is_dir(),'existing writable scratch parent required')
    start=time.monotonic();protected={p.relative_to(HERE).as_posix():sha(p) for p in (HERE/'packet').rglob('*') if p.is_file()};cases=[]
    with tempfile.TemporaryDirectory(prefix='c54-public230-corruptions-',dir=args.work_dir) as name:
        temp=Path(name);need(temp.resolve().is_relative_to((args.work_dir if args.work_dir else Path(tempfile.gettempdir())).resolve()),'scratch directory outside selected root');shutil.copytree(HERE/'packet',temp/'packet')
        for stage in ['08','09']:
            d=temp/'packet'/('stage'+stage);base=json.loads((d/('STAGE'+stage+'_RESULT.json')).read_text());fixtures={}
            def change(label,fn):
                data=copy.deepcopy(base);fn(data);fixtures[label]=data
            if stage=='08':
                change('missing_macro_case',lambda x:x['macro_cases'].pop())
                change('missing_joint_profile',lambda x:x['full_joint_type_cases'].pop())
                change('false_projection_coefficient',lambda x:x['macro_cases'][0]['plain_projection'].__setitem__(0,x['macro_cases'][0]['plain_projection'][0]+1))
                change('false_row_maximum',lambda x:x['full_joint_type_cases'][0]['row_receipts'][0]['row_objective_maximum'].__setitem__(0,x['full_joint_type_cases'][0]['row_receipts'][0]['row_objective_maximum'][0]+1))
                change('omitted_survivor',lambda x:x['surviving_joint_type_cases'].pop())
                change('false_global_closure',lambda x:x.update(all_declared_cases_excluded=True))
                change('circular_prior_theorem',lambda x:x.update(previous227_assumed=True))
            else:
                change('missing_survivor_case',lambda x:x['cases'].pop())
                change('false_binary_neighbor_cap',lambda x:x['cases'][0]['row_receipts'][0].update(cap3_neighbors=x['cases'][0]['row_receipts'][0]['cap3_neighbors']+1))
                change('false_projection',lambda x:x['cases'][0]['row_receipts'][0]['residual_diagonal'].__setitem__(0,x['cases'][0]['row_receipts'][0]['residual_diagonal'][0]+1))
                change('false_integer_row_maximum',lambda x:x['cases'][0]['row_receipts'][0]['row_objective_maximum'].__setitem__(0,x['cases'][0]['row_receipts'][0]['row_objective_maximum'][0]+1))
                change('false_rank_gap',lambda x:x['cases'][0]['rank_slack'].__setitem__(0,x['cases'][0]['rank_slack'][0]+1))
                change('false_survivor_status',lambda x:x.update(survivors=[x['cases'][0]]))
                change('false_lift',lambda x:x.update(candidate_parent_floor=231))
                change('circular227_assumption',lambda x:x.update(previous227_assumed=True))
                change('false_human_acceptance',lambda x:x.update(human_expert_accepted=True))
                change('false_public_adoption',lambda x:x.update(public_bound_changed=True))
            for label,data in sorted(fixtures.items()):
                p=d/(label+'.json');p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
                for optimized in [False,True]:
                    need(time.monotonic()-start<25,'UNKNOWN: corruption controller deadline')
                    out=label+('_optimized' if optimized else '_normal')+'_FALSE_PASS.json'
                    proc=subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+['verify_stage'+stage+'.py',p.name,out],cwd=d,capture_output=True,text=True,timeout=21)
                    need(proc.returncode==2 and proc.stderr.startswith('REJECTED: ') and not(d/out).exists(),'corruption accepted or wrong failure '+stage+'/'+label)
                    cases.append({'stage':stage,'fixture':label,'optimized':optimized,'returncode':2,'false_pass_written':False})
    need(protected=={p.relative_to(HERE).as_posix():sha(p) for p in (HERE/'packet').rglob('*') if p.is_file()},'frozen public source changed')
    need(len(cases)==34,'complete34 reviewed negative processes')
    print(json.dumps({'status':'PASS_PUBLIC230_ALL34_CORRUPTION_PROCESSES','rejected_processes':34,'cases':cases,'originals_unchanged':True,'assertions_used':False,'producer_runs':0,'cover_searches':0},indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as exc:print('FAIL_CLOSED: '+str(exc),file=sys.stderr);sys.exit(2)
