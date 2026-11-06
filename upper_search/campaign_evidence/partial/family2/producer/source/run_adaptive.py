#!/usr/bin/env python3
"""Price, enlarge, certify and solve exact protected-point kernels.

Each affected row has at most three free positions. All legal categorical
completions are enumerated before capacity certificates or MIPs are constructed.
All solver processes are isolated to avoid the OR-Tools/HiGHS library collision.
"""
import argparse,datetime as dt,hashlib,importlib.metadata,importlib.util,json,os,pathlib,shutil,subprocess,sys,time,uuid
BASE=pathlib.Path('/workspace/cover_search/exact_long');RECOMB=pathlib.Path('/workspace/cover_search/recombination');HERE=pathlib.Path(__file__).resolve().parent
SELF_BYTES=pathlib.Path(__file__).read_bytes()
sys.path.insert(0,'/workspace/solver_survey')
from verify_cover import verify

def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def atomic(p,v):
 p=pathlib.Path(p);t=pathlib.Path(str(p)+'.tmp');t.write_text(json.dumps(v,indent=2)+'\n');t.replace(p)
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--weak-override',help='Parent-hash-pinned partial row release overrides, bootstrap mode only');ap.add_argument('--fixed-rows',default='',help='Comma-separated zero-based rows to keep unchanged; bootstrap mode only');ap.add_argument('--hole-budget',type=int);ap.add_argument('--bootstrap-threshold',type=int,help='Interpret positional input as a pinned parent, selecting up to three old points per row at this private-loss threshold');ap.add_argument('--rounds',type=int,default=3);ap.add_argument('--batch',type=int,default=4);ap.add_argument('--mip-seconds','--solver-seconds',dest='mip_seconds',type=float,default=20);ap.add_argument('--engine',choices=['mip','sat','maxsat'],default='mip');ap.add_argument('--changed-rows',type=int);ap.add_argument('--prune-dominated',action='store_true');ap.add_argument('--certificate-fixing',action='store_true');ap.add_argument('--certificate-overlap-caps',action='store_true');ap.add_argument('--offset-objective',action='store_true');ap.add_argument('--allow-equal-size',action='store_true',help='Authorized equal-bound cover diversification; does not alter shared improvement-clock rules');ap.add_argument('--skip-baseline-solve',action='store_true',help='Use after the exact initial kernel has already been settled');ap.add_argument('--wall-seconds',type=float,default=120);ap.add_argument('--prefer-existing',action='store_true');ap.add_argument('--prefer-gain',action='store_true',help='Include one maximum certificate-capacity gain release before efficiency-ranked choices');ap.add_argument('--retain-incumbent',action='store_true',help='MIP only: keep the parent deficit feasible while minimizing toward the strict improvement budget');ap.add_argument('--native-solver',choices=['gluecard4','gluecard3','minicard'],default='gluecard4',help='Native SAT/MaxSAT backend');args=ap.parse_args()
 if args.retain_incumbent and args.engine!='mip':ap.error('--retain-incumbent is only supported by the MIP backend')
 fixed_rows={int(x) for x in args.fixed_rows.split(',') if x.strip()}
 if (fixed_rows or args.weak_override) and args.bootstrap_threshold is None:raise ValueError('Fixed rows/weak overrides require bootstrap mode')
 if args.bootstrap_threshold is None:
  initial_cert=json.loads(pathlib.Path(args.certificate).read_text());initial_kernel=json.loads(pathlib.Path(initial_cert['kernel']).read_text())
  assert sha(initial_cert['kernel'])==initial_cert['kernel_sha256'];assert sha(initial_kernel['parent'])==initial_kernel['parent_sha256']
 else:
  initial_kernel={'parent':str(pathlib.Path(args.certificate).resolve()),'parent_sha256':sha(args.certificate)}
 lease=BASE/'AUX_LEASE.json';pause=BASE/'PAUSE';quiesce=BASE/'QUIESCE_REQUEST.json';ident=str(uuid.uuid4())
 with lease.open('x') as f:json.dump({'lease_id':ident,'owner':'exact_trade/adaptive_kernel','pid':os.getpid(),'purpose':'certificate-guided kernel enlargement','created_utc':utc()},f)
 try:
  if quiesce.exists():raise RuntimeError('Quiescence requested; canceled')
  pause.touch();until=time.monotonic()+240
  while json.loads((BASE/'campaign_v5/status.json').read_text()).get('status')!='paused':
   if quiesce.exists():raise RuntimeError('Quiescence requested while waiting')
   if time.monotonic()>until:raise RuntimeError('Pause timeout')
   time.sleep(.2)
  started=time.monotonic();work=HERE/f'run_{time.time_ns()}';work.mkdir()
  tools_source=pathlib.Path(os.environ.get('ADAPTIVE_TOOLS_SOURCE',str(RECOMB)))
  for source in (tools_source/'kernel_hole_lp.py',tools_source/'price_kernel_release.py',BASE/'membership_lns.py',BASE/'defect_walk/replay.py'):
   shutil.copy2(source,work/source.name)
  if args.engine in ('sat','maxsat'):shutil.copy2(pathlib.Path(os.environ.get('ADAPTIVE_SAT_SOURCE',str(RECOMB/'kernel_categorical_sat.py'))),work/'kernel_categorical_sat.py')
  if args.engine=='maxsat':shutil.copy2(RECOMB/'kernel_categorical_maxsat.py',work/'kernel_categorical_maxsat.py')
  (work/'run_adaptive.py').write_bytes(SELF_BYTES);shutil.copy2(initial_kernel['parent'],work/'input.txt')
  if args.bootstrap_threshold is None:
   shutil.copy2(args.certificate,work/'baseline_certificate.json');shutil.copy2(initial_cert['kernel'],work/'baseline_kernel.json')
  else:
   spec=importlib.util.spec_from_file_location('adaptive_bootstrap_state',work/'membership_lns.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M);M.init_universe();state=M.State(M.load(work/'input.txt'))
   weakmap={}
   if any(i<0 or i>=len(state.rows) for i in fixed_rows):raise ValueError('Fixed row index outside parent')
   for i,row in enumerate(state.rows):
    if i in fixed_rows:continue
    points=sorted((int(state.breaks[i,p]),int(p)) for p in row if state.breaks[i,p]<=args.bootstrap_threshold)[:3]
    if points:weakmap[str(i)]=sorted(p+1 for _,p in points)
   if args.weak_override:
    override=json.loads(pathlib.Path(args.weak_override).read_text())
    if override.get('parent_sha256')!=sha(work/'input.txt') or override.get('row_index_base')!=0 or override.get('point_label_base')!=1:raise ValueError('Weak override parent/index mismatch')
    for row,points in override['weak_positions'].items():
     i=int(row);points=sorted(set(map(int,points)))
     if i in fixed_rows or i<0 or i>=len(state.rows) or not 1<=len(points)<=3 or not {p-1 for p in points}<=set(state.rows[i]):raise ValueError('Invalid weak override')
     weakmap[str(i)]=points
    shutil.copy2(args.weak_override,work/'bootstrap_override.json')
   atomic(work/'bootstrap_weak_map.json',{'parent_sha256':sha(work/'input.txt'),'row_index_base':0,'point_label_base':1,'weak_positions':weakmap,'selection':'up to three lowest-private-loss memberships per row','threshold':args.bootstrap_threshold})
   for argv,name in ((['export',work/'input.txt',args.bootstrap_threshold,work/'baseline_kernel.json','--source-dir',work,'--weak-map',work/'bootstrap_weak_map.json'],'bootstrap_export'),(['solve',work/'baseline_kernel.json',work/'baseline_certificate.json','--seconds',2],'bootstrap_lp'),(['verify',work/'baseline_certificate.json'],'bootstrap_verify')):
    with (work/(name+'.log')).open('w') as stream:subprocess.run([sys.executable,str(work/'kernel_hole_lp.py')]+list(map(str,argv)),stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=20)
   initial_kernel=json.loads((work/'baseline_kernel.json').read_text())
   print(json.dumps({'work':str(work),'bootstrap_rows':len(initial_kernel['groups']),'bootstrap_targets':len(initial_kernel['residual_targets']),'bootstrap_certificate':json.loads((work/'baseline_certificate.json').read_text())['hole_lower_bound']}),flush=True)
  source_files={str(p):sha(p) for p in work.iterdir() if p.suffix in ('.py','.json')};deps={p:importlib.metadata.version(p) for p in ('numpy','ortools','highspy','python-sat')}
  metadata={'input_path':str(work/'input.txt'),'input_sha256':sha(work/'input.txt'),'input_verification':verify(work/'input.txt',54,16,4),'source_files':source_files,'dependencies':deps,'initial_certificate':str(work/'baseline_certificate.json'),'initial_kernel':str(work/'baseline_kernel.json'),'settings':vars(args),'environment':{p:os.environ.get(p) for p in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS')},'start_utc':utc()}
  atomic(work/'metadata.json',metadata);old_holes=metadata['input_verification']['uncovered_targets'];blocks=metadata['input_verification']['blocks']
  hole_budget=old_holes-1 if args.hole_budget is None else args.hole_budget
  if not 0<=hole_budget<old_holes:raise ValueError('Requested hole budget must improve the pinned parent')
  current_shared=json.loads(pathlib.Path('/workspace/cover_search/campaign/status.json').read_text())
  current_partial_best=min((p['uncovered_targets'] for p in current_shared.get('partial_archive',{}).values() if p.get('blocks')==blocks),default=old_holes)
  metadata['hole_budget']=hole_budget
  metadata['global_partial_best_holes_at_start']=current_partial_best
  metadata['goal_scope']='strict global partial improvement' if hole_budget<current_partial_best else 'parent-relative family diversification'
  atomic(work/'metadata.json',metadata)
  completed_threshold=blocks-1 if args.allow_equal_size else blocks
  weak={int(g['row']):set(map(int,g.get('old_free_points',[g.get('old_free_point')]))) for g in initial_kernel['groups']};history=[];cert_path=work/'baseline_certificate.json';summaries=[]
  def call(argv,log,timeout):
   with pathlib.Path(log).open('w') as stream:subprocess.run([sys.executable]+list(map(str,argv)),stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=timeout)
  def attempt_solver(stage,kernel_path,round_metadata,record):
   seconds=min(args.mip_seconds,max(.1,args.wall_seconds-(time.monotonic()-started)))
   if args.engine=='sat':
    argv=[work/'kernel_categorical_sat.py',kernel_path,stage/'solver.json','--seconds',seconds,'--allow-holes',hole_budget,'--engine',args.native_solver]
    if args.changed_rows is not None:argv+=['--changed-rows',args.changed_rows]
    if args.prune_dominated:argv+=['--prune-dominated']
    if args.certificate_fixing or args.certificate_overlap_caps:argv+=['--certificate',round_metadata['certificate_path']]
    if args.certificate_overlap_caps:argv+=['--certificate-overlap-caps']
   elif args.engine=='maxsat':
    argv=[work/'kernel_categorical_maxsat.py',kernel_path,stage/'solver.json','--seconds',seconds,'--max-holes',hole_budget,'--engine',args.native_solver]
    if args.changed_rows is not None:argv+=['--changed-rows',args.changed_rows]
    if args.prune_dominated:argv+=['--prune-dominated']
    if args.certificate_fixing or args.offset_objective:argv+=['--certificate',round_metadata['certificate_path']]
    if args.offset_objective:argv+=['--offset-objective']
   else:
    mip_cap=old_holes if args.retain_incumbent else hole_budget
    argv=[work/'kernel_hole_lp.py','mip',kernel_path,stage/'solver.json','--seconds',seconds,'--allow-holes',mip_cap]
    record['solver_hole_cap']=mip_cap;record['strict_improvement_budget']=hole_budget;record['retain_parent_incumbent']=args.retain_incumbent
   call(argv,stage/'solver.log',seconds+10)
   solved=json.loads((stage/'solver.json').read_text());record['solver_engine']=args.engine;record['solver_status']=solved['status'];candidate=solved.get('candidate')
   if candidate and candidate['holes']<old_holes:
    checked=verify(candidate['path'],54,16,4);assert checked['uncovered_targets']==candidate['holes']
    spec=importlib.util.spec_from_file_location('adaptive_independent_incidence',work/'membership_lns.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
    incidence=M.independent_verify(M.load(candidate['path']));assert incidence['uncovered']==checked['uncovered_targets']
    trace=[]
    for change in candidate['changes']:
     removed=change.get('removed_points',[change.get('removed')]);added=change.get('added_points',[change.get('added')]);assert len(removed)==len(added)
     trace.extend({'block':change['row'],'remove':a,'insert':b} for a,b in zip(sorted(removed),sorted(added)))
    atomic(stage/'candidate.moves.json',trace)
    live_shared=json.loads(pathlib.Path('/workspace/cover_search/campaign/status.json').read_text())
    live_partial_best=min((p['uncovered_targets'] for p in live_shared.get('partial_archive',{}).values() if p.get('blocks')==checked['blocks']),default=old_holes)
    relation='strictly_better' if checked['uncovered_targets']<live_partial_best else 'equal' if checked['uncovered_targets']==live_partial_best else 'parent_only'
    result={'path':candidate['path'],'verification':checked,'incidence_verification':incidence,'moves_path':str(stage/'candidate.moves.json'),'solver_result':str(stage/'solver.json'),'status':'VERIFIED_FULL' if checked['valid'] else 'VERIFIED_PARTIAL_IMPROVEMENT','global_partial_best_holes_at_verification':live_partial_best,'global_partial_relation_at_verification':relation};atomic(stage/'candidate_result.json',result)
    ticket={'path':candidate['path'],'provenance':{'kind':'exact-protected-point-cp','input_metadata':str(stage/'input_metadata.json'),'result_metadata':str(stage/'candidate_result.json'),'source_files':round_metadata['source_files'],'dependencies':deps,'dependency_trace':str(stage/'candidate.moves.json'),'log_path':str(stage/'solver.log'),'replay_argv':['python',str(work/'replay.py'),str(stage/'input_metadata.json'),str(stage/'candidate_result.json'),'replay-output']}}
    if not checked['valid']:ticket['kind']='partial'
    atomic(pathlib.Path('/workspace/cover_search/campaign/inbox')/f'adaptive_kernel_{time.time_ns()}.json',ticket);record['candidate']=candidate['path'];record['holes']=checked['uncovered_targets']
  if args.engine=='maxsat':
   positive_kernel=HERE/'positive_1793980928556819592/kernel.json'
   control_argv=[work/'kernel_categorical_maxsat.py',positive_kernel,work/'maxsat_positive_control.json','--seconds',2,'--max-holes',13,'--prune-dominated','--engine',args.native_solver]
   if args.certificate_fixing or args.offset_objective:control_argv+=['--certificate',positive_kernel.parent/'certificate.json']
   if args.offset_objective:control_argv+=['--offset-objective']
   call(control_argv,work/'maxsat_positive_control.log',6)
   control=json.loads((work/'maxsat_positive_control.json').read_text())
   if control['status']!='OPTIMAL' or control.get('candidate',{}).get('holes')!=13:raise RuntimeError('Historical categorical MaxSAT positive control failed')
   if verify(control['candidate']['path'],54,16,4)['uncovered_targets']!=13:raise RuntimeError('MaxSAT control colex mismatch')
   print(json.dumps({'work':str(work),'maxsat_positive_control':'passed','holes':13}),flush=True)
  baseline_cert=json.loads(cert_path.read_text())
  shared=json.loads(pathlib.Path('/workspace/cover_search/campaign/status.json').read_text())
  if not args.skip_baseline_solve and baseline_cert['hole_lower_bound']<=hole_budget and not quiesce.exists() and shared['best']['blocks']>completed_threshold:
   stage=work/'baseline_solve';stage.mkdir();baseline_metadata={**metadata,'round':'baseline','kernel_path':str(work/'baseline_kernel.json'),'certificate_path':str(cert_path),'source_files':{**source_files,**{str(work/n):sha(work/n) for n in ('baseline_kernel.json','baseline_certificate.json')}}}
   atomic(stage/'input_metadata.json',baseline_metadata)
   record={'round':'baseline','certified_hole_lower_bound':baseline_cert['hole_lower_bound'],'lp_bound':baseline_cert['lp_relaxed_hole_objective'],'utc':utc()}
   attempt_solver(stage,work/'baseline_kernel.json',baseline_metadata,record)
   summaries.append(record);atomic(stage/'summary.json',record);print(json.dumps({'work':str(work),**record}),flush=True)
  for step in range(args.rounds):
   shared=json.loads(pathlib.Path('/workspace/cover_search/campaign/status.json').read_text())
   if quiesce.exists() or shared['best']['blocks']<=completed_threshold or time.monotonic()-started>=args.wall_seconds:break
   stage=work/f'round_{step:02d}';stage.mkdir()
   call([work/'price_kernel_release.py',cert_path,stage/'pricing.json'],stage/'pricing.log',20)
   prices=json.loads((stage/'pricing.json').read_text());assert prices['parent_sha256']==metadata['input_sha256']
   candidates={(int(p['row']),int(p['released_point'])):p for p in prices['positive_releases']};chosen=[];touched=set()
   order=prices['efficiency_order']
   if args.prefer_gain:
    high_gain=next(([int(p['row']),int(p['released_point'])] for p in prices['positive_releases'] if len(weak.get(int(p['row']),set()))<3),None)
    if high_gain is not None:order=[high_gain]+[key for key in order if key!=high_gain]
   if args.prefer_existing:
    priority=next((key for key in order if 0<len(weak.get(int(key[0]),set()))<3),None)
    if priority is not None:order=[priority]+[key for key in order if key!=priority]
   for key in order:
    row,point=map(int,key)
    current=weak.get(row,set())
    if row in fixed_rows or row in touched or point in current or len(current)>=3:continue
    item=candidates[(row,point)]
    if set(item['old_weak_points'])!=current or set(item['new_weak_points'])!=current|{point}:raise RuntimeError('Unexpected pricing row scope')
    weak[row]=current|{point};chosen.append(item);touched.add(row)
    if len(chosen)>=args.batch:break
   if not chosen:atomic(stage/'status.json',{'status':'NO_CERTIFICATE_CAPACITY_IMPROVING_RELEASES'});break
   history.extend(chosen)
   config={'parent_sha256':metadata['input_sha256'],'row_index_base':0,'point_label_base':1,'weak_positions':{str(i):sorted(ps) for i,ps in sorted(weak.items())},'new_releases':chosen,'release_history':history,'pricing_receipt':str(stage/'pricing.json'),'pricing_sha256':sha(stage/'pricing.json')}
   atomic(stage/'weak_positions.json',config)
   call([work/'kernel_hole_lp.py','export',work/'input.txt',2,stage/'kernel.json','--source-dir',work,'--weak-map',stage/'weak_positions.json'],stage/'export.log',20)
   call([work/'kernel_hole_lp.py','solve',stage/'kernel.json',stage/'certificate.json','--seconds',2,'--group-size',1],stage/'lp.log',10)
   call([work/'kernel_hole_lp.py','verify',stage/'certificate.json'],stage/'certificate_verification.log',10)
   cert_path=stage/'certificate.json';cert=json.loads(cert_path.read_text());kernel=json.loads((stage/'kernel.json').read_text());assert 0<=cert['hole_lower_bound']<=old_holes
   record={'round':step,'rows':len(weak),'mutable_positions':sum(map(len,weak.values())),'max_free_positions':max(map(len,weak.values())),'residual_targets':len(kernel['residual_targets']),'new_releases':[(p['row'],p['released_point']) for p in chosen],'certified_hole_lower_bound':cert['hole_lower_bound'],'lp_bound':cert['lp_relaxed_hole_objective'],'utc':utc()}
   round_metadata={**metadata,'round':step,'weak_config_path':str(stage/'weak_positions.json'),'certificate_path':str(cert_path),'kernel_path':str(stage/'kernel.json'),'source_files':{**source_files,**{str(stage/n):sha(stage/n) for n in ('weak_positions.json','kernel.json','certificate.json','pricing.json')}},'mip_seconds':args.mip_seconds}
   atomic(stage/'input_metadata.json',round_metadata)
   if cert['hole_lower_bound']<=hole_budget and time.monotonic()-started<args.wall_seconds:
    attempt_solver(stage,stage/'kernel.json',round_metadata,record)
   summaries.append(record);atomic(stage/'summary.json',record);print(json.dumps({'work':str(work),**record}),flush=True)
  atomic(work/'summary.json',summaries)
 finally:
  if lease.exists() and json.loads(lease.read_text()).get('lease_id')==ident:pause.unlink(missing_ok=True);lease.unlink()
if __name__=='__main__':main()
