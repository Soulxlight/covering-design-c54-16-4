"""One exact binary-containment refinement of the preserved projection stage."""
import hashlib,itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
PIN='224486fbd98b5dc11e8a0eccbca8d69cb151c2021c1157084cf9771ad37ce287'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):
    x=F(x);return [x.numerator,x.denominator]
def project(h,k,diagonal=False):
    t=F(8,3);u=t+F(h,3);v=t+F(k,3);one=1+t
    return t+F(h+k,3)+(F(h,3) if diagonal else 0)-u*v/one+(5-4*u/one)*(5-4*v/one)/(18-16*t/one)
def uniform(coeffs,load,cap):
    need(0<=load<=cap*len(coeffs),'uniform load infeasible')
    coeffs=sorted(coeffs,reverse=True);full,rem=divmod(load,cap)
    value=sum((cap*cap+2*cap*c for c in coeffs[:full]),F(0))
    if rem:value+=rem*rem+2*rem*coeffs[full]
    return value
def row_max(h,neighbors,load):
    if h:need(all(cap==3 for cap,c in neighbors),'positive partner row cap differs');return uniform([c for cap,c in neighbors],load,3)
    special=[c for cap,c in neighbors if cap==3];plain=[c for cap,c in neighbors if cap==4]
    need(len(special)<=5,'undeclared partner-neighbor enumeration')
    scores=[]
    for es in itertools.product(range(4),repeat=len(special)):
        left=load-sum(es)
        if 0<=left<=4*len(plain):scores.append(sum((e*e+2*c*e for e,c in zip(es,special)),F(0))+uniform(plain,left,4))
    need(scores,'mixed row infeasible');return max(scores)
def case(types):
    trace=F(0);frob=F(0);rows=[]
    for r,h,n in types:
        need(r==5,'survivor degree changed');diagonal=5-project(h,h,True);trace+=n*diagonal;constant=diagonal*diagonal;neighbors=[];cap_counts={3:0,4:0}
        for s,k,count in types:
            available=count-int(h==k)
            if not available:continue
            cap=3 if h or k else 4;c=1-project(h,k);constant+=available*c*c;neighbors.extend([(cap,c)]*available);cap_counts[cap]+=available
        maximum=row_max(h,neighbors,14-h);upper=constant+maximum;frob+=n*upper
        rows.append({'h':h,'count':n,'residual_diagonal':enc(diagonal),'row_excess':14-h,'cap3_neighbors':cap_counts[3],'cap4_neighbors':cap_counts[4],'row_objective_maximum':enc(maximum),'row_frobenius_upper':enc(upper)})
    gap=trace*trace-9*frob
    return {'a':8,'j':0,'normal_types':types,'rank_cap':9,'trace':enc(trace),'frobenius_upper':enc(frob),'rank_slack':enc(gap),'row_receipts':rows,'excluded':gap>0}
def main():
    start=time.monotonic();deadline=start+10;p=HERE/'dependencies/STAGE08_RESULT.json';need(sha(p)==PIN,'frozen projection input differs');old=json.loads(p.read_text());need(len(old['surviving_joint_type_cases'])==15 and not old['all_declared_cases_excluded'],'prior stage status differs')
    cases=[]
    for rec in old['surviving_joint_type_cases']:
        need(time.monotonic()<deadline,'UNKNOWN: producer deadline');need((rec['a'],rec['j'])==(8,0),'undeclared survivor macro');cases.append(case(rec['normal_types']))
    survivors=[rec for rec in cases if not rec['excluded']];closed=not survivors
    result={'status':'PROPOSED_PAIR19_CHILD68_PARENT230_PENDING_FRESH_REVIEW' if closed else 'INCONCLUSIVE_COMPLETE_BINARY_CAP_REFINEMENT','pair_cover_hypothesis':[52,14,2,18],'stage08_result_sha256':PIN,'case_count':15,'cases':cases,'survivors':survivors,'all18_pair_covers_excluded':closed,'candidate_pair_floor':19 if closed else None,'candidate_child_floor':68 if closed else None,'candidate_parent_floor':230 if closed else None,'minimum_rank_slack':enc(min(F(*rec['rank_slack']) for rec in cases)),'previous227_assumed':False,'public_bound_changed':False,'complete_cover_found':False,'human_expert_accepted':False,'formal_kernel_verified':False,'priority_certified':False,'fresh_independent_semantic_review_required':closed,'search_seconds':time.monotonic()-start}
    need(time.monotonic()<deadline,'UNKNOWN: producer deadline')
    with (HERE/'STAGE09_RESULT.json').open('x') as out:out.write(json.dumps(result,indent=2)+'\n')
    source={'status':'ONE_STAGE09_PRODUCER_COMPLETE','producer_sha256':sha(Path(__file__)),'result_sha256':sha(HERE/'STAGE09_RESULT.json'),'producer_runs':1,'covering_solver_calls':0}
    with (HERE/'STAGE09_PRODUCER_SOURCE_RECEIPT.json').open('x') as out:out.write(json.dumps(source,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'case_count':15,'survivors':len(survivors),'minimum_rank_slack':result['minimum_rank_slack'],'seconds':result['search_seconds']}))
if __name__=='__main__':
    try:main()
    except Exception as exc:print('REJECTED: '+str(exc),file=sys.stderr);sys.exit(2)
