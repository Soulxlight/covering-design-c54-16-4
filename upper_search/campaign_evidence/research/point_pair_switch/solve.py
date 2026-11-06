"""Bounded weighted SAT/MaxSAT for a threshold-reduced paired-point kernel."""
import time,threading
from model import reduce,score

def solve(model,target,seconds=2,mode='sat'):
 from pysat.formula import CNF,WCNF
 from pysat.card import CardEnc,EncType
 from pysat.solvers import Solver
 began=time.monotonic();reduced=reduce(model,target)
 if reduced['infeasible']:
  return {'status':'UNSAT_PARITY','target':target,'fixed_after_threshold_assumptions':reduced['fixed'],'parity_merges':reduced['merges'],'scope':'Threshold-conditional proof only; not a global lower bound of this numeric fixed cost.'}
 groups=reduced['groups'];budget=reduced['budget'];n=len(model['variable_rows']);nv=n;hard=[];soft=[];cost_vars=[]
 roots=sorted({abs(lit) for vs in groups for lit in vs})
 if roots:hard.append([-roots[0]]) # Global a/b exchange preserves every NAE cost.
 for vs,w in groups.items():
  pos=list(vs);neg=[-x for x in vs]
  if w>budget:hard.extend((pos,neg));continue
  if mode=='maxsat':soft.extend(((pos,w),(neg,w)));continue
  nv+=1;r=nv;hard.extend(([r,*pos],[r,*neg]));cost_vars.append(r)
  for _ in range(w-1):
   nv+=1;z=nv;hard.extend(([-r,z],[r,-z]));cost_vars.append(z)
 if mode=='sat' and cost_vars:
  enc=CardEnc.atmost(lits=cost_vars,bound=budget,top_id=nv,encoding=EncType.seqcounter);hard.extend(enc.clauses);nv=enc.nv
 phases=[x if model['original_assignment'].get(x,0) else -x for x in roots]
 timer=None;solver=None;interrupted=threading.Event();assignment=None;status='UNKNOWN';optimum=None
 try:
  if mode=='sat':
   solver=Solver(name='g4',bootstrap_with=hard);solver.set_phases(phases)
   def stop():interrupted.set();solver.interrupt()
   timer=threading.Timer(max(.001,seconds-(time.monotonic()-began)),stop);timer.daemon=True;timer.start()
   answer=solver.solve_limited(expect_interrupt=True)
   if answer is True:assignment=solver.get_model();status='SAT'
   elif answer is False:status='UNSAT'
  elif mode=='maxsat':
   from pysat.examples.rc2 import RC2
   formula=WCNF()
   for c in hard:formula.append(c)
   for c,w in soft:formula.append(c,weight=w)
   solver=RC2(formula,solver='g4',adapt=False,exhaust=False,minz=False,trim=0,verbose=0);solver.oracle.set_phases(phases)
   def stop():interrupted.set();solver.interrupt()
   timer=threading.Timer(max(.001,seconds-(time.monotonic()-began)),stop);timer.daemon=True;timer.start()
   assignment=solver.compute(expect_interrupt=True)
   if assignment is not None:status='OPTIMAL';optimum=reduced['fixed']+solver.cost
   elif not interrupted.is_set():status='UNSAT'
  else:raise ValueError('unknown mode')
 finally:
  if timer is not None:timer.cancel();timer.join()
  if solver is not None:solver.delete()
 result={'status':status,'mode':mode,'target':target,'fixed_after_threshold_assumptions':reduced['fixed'],'remaining_budget':budget,'parity_merges':reduced['merges'],'reduced_supports':len(groups),'active_root_variables':len(roots),'hard_clauses':len(hard),'soft_clauses':len(soft),'encoding_variables':nv,'interrupted':interrupted.is_set(),'seconds':time.monotonic()-began}
 if assignment is not None:
  positive={x for x in assignment if x>0};root_values={r:int(r in positive) for r in roots}
  # Unconstrained parity components choose the orientation with fewer row flips.
  choices={}
  for var,old in model['original_assignment'].items():
   r,p=reduced['parity'].find(var);choices.setdefault(r,[]).append(old^p)
  for r,values in choices.items():root_values.setdefault(r,int(sum(values)*2>len(values)))
  decoded={var:root_values[reduced['parity'].find(var)[0]]^reduced['parity'].find(var)[1] for var in model['original_assignment']}
  # Also consider global color complementation for a smaller equivalent edit.
  change=sum(decoded[v]!=old for v,old in model['original_assignment'].items())
  if change>len(decoded)-change:decoded={v:1-x for v,x in decoded.items()};change=len(decoded)-change
  predicted=score(model,decoded)
  if mode=='sat':assert predicted<=target
  else:assert predicted==optimum
  result.update(assignment=decoded,predicted_holes=predicted,changed_rows=change)
 return result
