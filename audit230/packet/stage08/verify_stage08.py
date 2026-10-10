"""Independent basis-Gram inversion and integer row-knapsack reconstruction."""
import collections,hashlib,itertools,json,math,sys,time
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)
def enc(x):
    x=F(x);return [x.numerator,x.denominator]
def sha(file):return hashlib.sha256(file.read_bytes()).hexdigest()

def inverse_basis(a,j):
    size=a+1;B=[[F(4 if p==q else 1) for q in range(a)]+[F(4)] for p in range(a)]
    for p in range(0,2*j,2):B[p][p+1]=B[p+1][p]=F(2)
    B.append([F(4)]*a+[F(18)])
    aug=[row+[F(int(p==q)) for q in range(size)] for p,row in enumerate(B)]
    for column in range(size):
        pivot=aug[column][column];need(pivot>0,'basis Gram not positive definite')
        aug[column]=[value/pivot for value in aug[column]]
        for row in range(size):
            if row==column:continue
            scale=aug[row][column]
            if scale:aug[row]=[v-scale*w for v,w in zip(aug[row],aug[column])]
    inv=[row[size:] for row in aug]
    for p in range(size):
        for q in range(size):need(sum(B[p][k]*inv[k][q] for k in range(size))==int(p==q),'inverse basis identity failed')
    return inv

def projected(inv,a,j,r,h,s,k,diagonal=False):
    left=[F(1)]*a+[F(r)];right=[F(1)]*a+[F(s)]
    for p in range(2*j,2*j+h):left[p]+=1
    start=2*j if diagonal else 2*j+h
    need(start+k<=a,'disjoint partner supports exceeded')
    for p in range(start,start+k):right[p]+=1
    return sum(left[p]*sum(inv[p][q]*right[q] for q in range(a+1)) for p in range(a+1))

def profiles(D,H,N):
    # Generic vector-partition enumeration instead of the producer's specialized high-degree cases.
    types=[(d,h) for d in range(D+1) for h in range(H+1) if d or h]
    chosen=[]
    def walk(index,leftD,leftH):
        if index==len(types):
            if leftD or leftH:return
            count=sum(n for d,h,n in chosen);need(count<=N,'profile point count exceeded')
            record=[[5+d,h,n] for d,h,n in chosen]
            if count<N:record.append([5,0,N-count])
            yield sorted(record);return
        d,h=types[index];limits=[N-sum(n for d,h,n in chosen)]
        if d:limits.append(leftD//d)
        if h:limits.append(leftH//h)
        for n in range(min(limits)+1):
            if n:chosen.append((d,h,n))
            yield from walk(index+1,leftD-d*n,leftH-h*n)
            if n:chosen.pop()
    yield from walk(0,D,H)

def integer_max(neighbors,load):
    denom=1
    for cap,c in neighbors:denom=math.lcm(denom,c.denominator)
    dp=[0]+[None]*load
    for cap,c in neighbors:
        linear=int(c*denom);new=[None]*(load+1)
        for used,value in enumerate(dp):
            if value is None:continue
            for extra in range(min(cap,load-used)+1):
                candidate=value+denom*extra*extra+2*linear*extra;target=used+extra
                if new[target] is None or candidate>new[target]:new[target]=candidate
        dp=new
    need(dp[load] is not None,'row integer universe empty');return F(dp[load],denom)

def main():
    started=time.monotonic();deadline=started+20;file=HERE/sys.argv[1];data=json.loads(file.read_text())
    need(data['pair_cover_hypothesis']==[52,14,2,18] and data['previous227_assumed'] is False,'changed hypothesis or circular theorem assumption')
    need(all(data[key] is False for key in ['public_bound_changed','complete_cover_found','human_expert_accepted','formal_kernel_verified','priority_certified']),'unsupported publication, cover or acceptance claim')
    source=json.loads((HERE/'STAGE08_PRODUCER_SOURCE_RECEIPT.json').read_text());need(source['producer_sha256']==sha(HERE/'stage08_projection.py') and source['producer_runs']==1 and source['covering_solver_or_DP_calls']==0,'producer source/scope differs')
    macros={(rec['a'],rec['j']):rec for rec in data['macro_cases']}
    domain={(a,j) for a in range(8,18) for j in range(a//2+1)}
    need(set(macros)==domain and len(data['macro_cases'])==data['macro_case_count']==70,'incomplete macro universe')
    supplied={}
    for rec in data['full_joint_type_cases']:
        key=(rec['a'],rec['j'],tuple(tuple(row) for row in rec['normal_types']));need(key not in supplied,'duplicate full joint profile');supplied[key]=rec
    expected_keys=set();computed=[];basis_cache={};projection_cache={};row_count=0
    def projection(a,j,r,h,s,k,diagonal=False):
        key=(a,j,r,h,s,k,diagonal)
        if key not in projection_cache:projection_cache[key]=projected(basis_cache[(a,j)],a,j,r,h,s,k,diagonal)
        return projection_cache[key]
    for a,j in sorted(domain):
        need(time.monotonic()<deadline,'UNKNOWN: checker deadline');basis_cache[(a,j)]=inverse_basis(a,j)
        L=60-3*a+2*j;R=17-a;q=projection(a,j,5,0,5,0)
        need(L>=5 and 1<q<F(3,2),'plain principal-matrix bound premise failed')
        tr=L*(5-q);upper=L*((5-q)**2+(L-1)*(1-q)**2+52+28*(1-q));slack=tr*tr-R*upper
        expected={'a':a,'j':j,'non_tight_points':52-a,'degree_excess':a-8,'external_tight_partners':a-2*j,'guaranteed_plain_columns':L,'rank_cap':R,'plain_projection':enc(q),'trace':enc(tr),'frobenius_upper':enc(upper),'rank_slack':enc(slack),'excluded':slack>0}
        need(macros[(a,j)]==expected,'independent macro coefficients differ')
        if slack>0:continue
        need(a<=10,'UNKNOWN: undeclared high-extra full-profile universe')
        for types in profiles(a-8,a-2*j,52-a):
            key=(a,j,tuple(tuple(row) for row in types));need(key in supplied,'omitted full joint profile');expected_keys.add(key);record=supplied[key]
            need(sum(n for r,h,n in types)==52-a and sum((r-5)*n for r,h,n in types)==a-8 and sum(h*n for r,h,n in types)==a-2*j,'joint parameter arithmetic differs')
            trace=F(0);frob=F(0);negative=[];rows=[]
            for r,h,n in types:
                need(time.monotonic()<deadline,'UNKNOWN: full-profile checker deadline')
                diagonal=F(r)-projection(a,j,r,h,r,h,True);trace+=n*diagonal
                if diagonal<0:negative.append([r,h,n,enc(diagonal)])
                neighbors=[];constant=diagonal*diagonal
                for s,k,count in types:
                    available=count-int((r,h)==(s,k))
                    if available==0:continue
                    c=1-projection(a,j,r,h,s,k);constant+=available*c*c;neighbors.extend([(min(r,s)-1,c)]*available)
                load=13*r-51-h;need(0<=load<=sum(cap for cap,c in neighbors),'joint row capacity failed')
                maximum=integer_max(neighbors,load);rowupper=constant+maximum;frob+=n*rowupper;row_count+=1
                rows.append({'r':r,'h':h,'count':n,'residual_diagonal':enc(diagonal),'row_excess':load,'row_objective_maximum':enc(maximum),'row_frobenius_upper':enc(rowupper)})
            full_slack=trace*trace-R*frob
            full_expected={'a':a,'j':j,'normal_types':types,'rank_cap':R,'trace':enc(trace),'frobenius_upper':enc(frob),'rank_slack':enc(full_slack),'negative_residual_diagonals':negative,'row_receipts':rows,'excluded':bool(negative) or full_slack>0}
            need(record==full_expected,'independent full-profile coefficients or row maxima differ');computed.append(full_expected)
    need(set(supplied)==expected_keys and len(computed)==data['full_joint_type_case_count']==len(data['full_joint_type_cases']),'missing/unexpected full profile')
    survivors=[rec for rec in computed if not rec['excluded']]
    need(sorted(data['surviving_joint_type_cases'],key=lambda rec:(rec['a'],rec['j'],rec['normal_types']))==sorted(survivors,key=lambda rec:(rec['a'],rec['j'],rec['normal_types'])),'false survivor set')
    closed=not survivors;need(data['all_declared_cases_excluded']==closed,'false closure')
    need(data['status']==('PROPOSED_PAIR_FLOOR19_CHILD68_PARENT230_FOR_FRESH_SEMANTIC_REVIEW' if closed else 'INCONCLUSIVE_COMPLETE_TIGHT_GRAM_PROJECTION_RELAXATION'),'unjustified theorem status')
    need([data['candidate_pair_floor'],data['candidate_child_floor'],data['candidate_parent_floor']]==([19,68,230] if closed else [None,None,None]) and data['fresh_independent_semantic_review_required']==closed,'false candidate adoption')
    need(data['lift_arithmetic']=={'child_required':1007,'67_child_incidence':1005,'child_floor':68,'parent_required':3672,'229_parent_incidence':3664,'parent_floor':230},'conditional lift arithmetic differs')
    # Complete small integer allocation toys, uniform4 and one cap5, coefficients -1/2,0,1/2.
    vectors=loads=0
    for length in range(1,5):
        for onefive in [False,True]:
            caps=[5 if onefive and index==0 else 4 for index in range(length)]
            for coeffs in itertools.product([F(-1,2),F(0),F(1,2)],repeat=length):
                brute={}
                for values in itertools.product(*(range(cap+1) for cap in caps)):
                    vectors+=1;load=sum(values);score=sum(F(e*e)+2*c*e for e,c in zip(values,coeffs));brute[load]=max(brute.get(load,score),score)
                neighbors=list(zip(caps,coeffs))
                for load,score in brute.items():need(integer_max(neighbors,load)==score,'complete row allocation toy differs');loads+=1
    need((vectors,loads)==(119328,3768),'toy allocation universe incomplete')
    need(time.monotonic()<deadline,'UNKNOWN: checker deadline')
    result={'status':'PASS_INDEPENDENT_COMPLETE_TIGHT_GRAM_PROJECTION_STAGE','result_sha256':sha(file),'macro_cases':70,'full_joint_type_cases':len(computed),'independently_reconstructed_row_maxima':row_count,'surviving_joint_type_cases':len(survivors),'minimum_full_rank_slack':enc(min(F(*rec['rank_slack']) for rec in computed)),'complete_toy_allocations':vectors,'toy_load_maxima':loads,'all18_pair_covers_excluded':closed,'candidate_parent_floor':230 if closed else None,'public_bound_changed':False,'previous227_assumed':False}
    out=HERE/sys.argv[2];need(not out.exists(),'receipt exists');out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result))

if __name__=='__main__':
    try:main()
    except Exception as exc:print('REJECTED: '+str(exc),file=sys.stderr);sys.exit(2)
