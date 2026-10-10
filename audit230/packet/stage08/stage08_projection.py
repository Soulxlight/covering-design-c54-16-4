"""Exact tight-column projection rank bounds; one complete declared finite stage."""
import collections,hashlib,json,sys,time
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)
def enc(x):
    x=F(x);return [x.numerator,x.denominator]

def project(a,j,r,h,s,k,diagonal=False):
    t=F(2*a-j,6);one=1+t;u=t+h*F(1,3);v=t+k*F(1,3)
    tight=t+F(h+k,3)+(F(h,3) if diagonal else 0)-u*v/one
    return tight+(r-4*u/one)*(s-4*v/one)/(18-16*t/one)

def partitions(total,least=1):
    if total==0:yield [];return
    for part in range(least,total+1):
        for rest in partitions(total-part,part):yield [part]+rest

def joint_types(D,H,N):
    if D==0:high_sets=[[]]
    elif D==1:high_sets=[[(1,h)] for h in range(H+1)]
    elif D==2:
        high_sets=[[(2,h)] for h in range(H+1)]+[[(1,u),(1,v)] for u in range(H+1) for v in range(u,H-u+1)]
    else:raise ValueError('UNKNOWN: unclosed high-extra macro')
    for high in high_sets:
        remaining=H-sum(h for d,h in high)
        if remaining<0:continue
        for low in partitions(remaining):
            counts=collections.Counter((5+d,h) for d,h in high)
            counts.update((5,h) for h in low)
            plain=N-sum(counts.values());need(plain>=0,'normal-point count exceeded')
            if plain:counts[(5,0)]+=plain
            yield [[r,h,count] for (r,h),count in sorted(counts.items())]

def uniform_max(coeffs,load):
    need(0<=load<=4*len(coeffs),'row load outside uniform capacity')
    coeffs=sorted(coeffs,reverse=True);full,rem=divmod(load,4)
    value=sum((16+8*c for c in coeffs[:full]),F(0))
    if rem:value+=rem*rem+2*coeffs[full]*rem
    return value

def row_max(neighbors,load):
    special=[(cap,c) for cap,c in neighbors if cap!=4];regular=[c for cap,c in neighbors if cap==4]
    need(len(special)<=1 and all(cap==5 for cap,c in special),'unexpected nonuniform cap universe')
    if not special:return uniform_max(regular,load)
    cap,c=special[0];values=[]
    for e in range(min(cap,load)+1):
        if load-e<=4*len(regular):values.append(F(e*e)+2*c*e+uniform_max(regular,load-e))
    need(values,'nonuniform row infeasible');return max(values)

def full_record(a,j,types):
    R=17-a;trace=F(0);upper=F(0);negative=[];row_receipts=[]
    for r,h,count in types:
        diagonal=F(r)-project(a,j,r,h,r,h,True);trace+=count*diagonal
        if diagonal<0:negative.append([r,h,count,enc(diagonal)])
        neighbors=[];constant=diagonal*diagonal
        for s,k,n in types:
            available=n-int((r,h)==(s,k));c=1-project(a,j,r,h,s,k)
            constant+=available*c*c;neighbors.extend([(min(r,s)-1,c)]*available)
        load=13*r-51-h
        capacity=sum(cap for cap,c in neighbors)
        need(0<=load<=capacity,'unexpected infeasible full-profile row')
        maximum=row_max(neighbors,load);rowupper=constant+maximum;upper+=count*rowupper
        row_receipts.append({'r':r,'h':h,'count':count,'residual_diagonal':enc(diagonal),'row_excess':load,'row_objective_maximum':enc(maximum),'row_frobenius_upper':enc(rowupper)})
    slack=trace*trace-R*upper
    return {'a':a,'j':j,'normal_types':types,'rank_cap':R,'trace':enc(trace),'frobenius_upper':enc(upper),'rank_slack':enc(slack),'negative_residual_diagonals':negative,'row_receipts':row_receipts,'excluded':bool(negative) or slack>0}

def main():
    started=time.monotonic();deadline=started+10;macros=[];full=[]
    for a in range(8,18):
        for j in range(a//2+1):
            need(time.monotonic()<deadline,'UNKNOWN: producer deadline')
            L=60-3*a+2*j;R=17-a;q=project(a,j,5,0,5,0)
            need(L>=5 and 1<q<F(3,2),'plain-column rank premise fails')
            diagonal=5-q;c=1-q;trace=L*diagonal
            upper=L*(diagonal*diagonal+(L-1)*c*c+52+28*c);slack=trace*trace-R*upper
            macro={'a':a,'j':j,'non_tight_points':52-a,'degree_excess':a-8,'external_tight_partners':a-2*j,'guaranteed_plain_columns':L,'rank_cap':R,'plain_projection':enc(q),'trace':enc(trace),'frobenius_upper':enc(upper),'rank_slack':enc(slack),'excluded':slack>0};macros.append(macro)
            if slack<=0:
                need(a<=10,'UNKNOWN: plain gate did not close a>10; no expanded profile retry')
                for types in joint_types(a-8,a-2*j,52-a):
                    need(time.monotonic()<deadline,'UNKNOWN: producer deadline');full.append(full_record(a,j,types))
    need(len(macros)==70,'macro universe incomplete')
    survivors=[rec for rec in full if not rec['excluded']];all_excluded=not survivors
    result={'status':'PROPOSED_PAIR_FLOOR19_CHILD68_PARENT230_FOR_FRESH_SEMANTIC_REVIEW' if all_excluded else 'INCONCLUSIVE_COMPLETE_TIGHT_GRAM_PROJECTION_RELAXATION','pair_cover_hypothesis':[52,14,2,18],'macro_cases':macros,'full_joint_type_cases':full,'macro_case_count':len(macros),'full_joint_type_case_count':len(full),'surviving_joint_type_cases':survivors,'all_declared_cases_excluded':all_excluded,'candidate_pair_floor':19 if all_excluded else None,'candidate_child_floor':68 if all_excluded else None,'candidate_parent_floor':230 if all_excluded else None,'lift_arithmetic':{'child_required':53*19,'67_child_incidence':67*15,'child_floor':(53*19+14)//15,'parent_required':54*68,'229_parent_incidence':229*16,'parent_floor':(54*68+15)//16},'previous227_assumed':False,'public_bound_changed':False,'complete_cover_found':False,'human_expert_accepted':False,'formal_kernel_verified':False,'priority_certified':False,'fresh_independent_semantic_review_required':all_excluded,'search_seconds':time.monotonic()-started}
    need(time.monotonic()<deadline,'UNKNOWN: producer deadline')
    with (HERE/'STAGE08_RESULT.json').open('x') as out:out.write(json.dumps(result,indent=2)+'\n')
    source={'status':'COMPLETE_ONE_STAGE08_EXACT_PROJECTION_PRODUCER','producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'result_sha256':hashlib.sha256((HERE/'STAGE08_RESULT.json').read_bytes()).hexdigest(),'producer_runs':1,'covering_solver_or_DP_calls':0}
    with (HERE/'STAGE08_PRODUCER_SOURCE_RECEIPT.json').open('x') as out:out.write(json.dumps(source,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'macro_cases':70,'full_joint_type_cases':len(full),'survivors':len(survivors),'minimum_full_rank_slack':enc(min(F(*rec['rank_slack']) for rec in full)),'seconds':result['search_seconds']}))

if __name__=='__main__':
    try:main()
    except Exception as exc:print('REJECTED: '+str(exc),file=sys.stderr);sys.exit(2)
