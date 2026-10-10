"""Independent LDL basis reconstruction, full integer rows and complete toys."""
import collections,hashlib,itertools,json,math,sys,time
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
PIN='224486fbd98b5dc11e8a0eccbca8d69cb151c2021c1157084cf9771ad37ce287'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):
    x=F(x);return [x.numerator,x.denominator]
def inverse():
    B=[[F(4 if p==q else 1) for q in range(8)]+[F(4)] for p in range(8)]+[[F(4)]*8+[F(18)]]
    L=[[F(int(p==q)) for q in range(9)] for p in range(9)];D=[]
    for p in range(9):
        D.append(B[p][p]-sum(L[p][k]*L[p][k]*D[k] for k in range(p)));need(D[p]>0,'basis not positive definite')
        for q in range(p+1,9):L[q][p]=(B[q][p]-sum(L[q][k]*L[p][k]*D[k] for k in range(p)))/D[p]
    inv=[[F(0)]*9 for p in range(9)]
    for column in range(9):
        y=[]
        for p in range(9):y.append(F(int(p==column))-sum(L[p][k]*y[k] for k in range(p)))
        z=[y[p]/D[p] for p in range(9)];x=[F(0)]*9
        for p in range(8,-1,-1):x[p]=z[p]-sum(L[k][p]*x[k] for k in range(p+1,9))
        for p in range(9):inv[p][column]=x[p]
    for p in range(9):
        for q in range(9):need(sum(B[p][k]*inv[k][q] for k in range(9))==int(p==q),'inverse identity differs')
    return inv
def projected(inv,h,k,diagonal=False):
    left=[F(2 if p<h else 1) for p in range(8)]+[F(5)]
    right=[F(1)]*8+[F(5)];start=0 if diagonal else h
    need(start+k<=8,'tight partner supports overlap or exceed eight')
    for p in range(start,start+k):right[p]+=1
    return sum(left[p]*inv[p][q]*right[q] for p in range(9) for q in range(9))
def all_maxima(neighbors,maxload):
    scale=1
    for cap,c in neighbors:scale=math.lcm(scale,c.denominator)
    values=[0]+[None]*maxload
    for cap,c in neighbors:
        linear=int(c*scale);following=[None]*(maxload+1)
        for load,val in enumerate(values):
            if val is None:continue
            for e in range(min(cap,maxload-load)+1):
                score=val+scale*e*e+2*linear*e;index=load+e
                if following[index] is None or score>following[index]:following[index]=score
        values=following
    return [None if val is None else F(val,scale) for val in values]
def partitions_eight():
    # Multiplicity vectors for part sizes1..8, unlike the producer's prior survivor iteration.
    def walk(size,left,parts):
        if size==9:
            if left==0:yield parts
            return
        for n in range(left//size+1):yield from walk(size+1,left-size*n,parts+[size]*n)
    yield from walk(1,8,[])
def main():
    started=time.monotonic();deadline=started+20;file=HERE/sys.argv[1];data=json.loads(file.read_text())
    need(data['pair_cover_hypothesis']==[52,14,2,18] and data['previous227_assumed'] is False,'changed hypothesis or circular assumption')
    need(all(data[key] is False for key in ['public_bound_changed','complete_cover_found','human_expert_accepted','formal_kernel_verified','priority_certified']),'unsupported public, cover or acceptance claim')
    need(data['stage08_result_sha256']==PIN,'prior projection binding differs')
    oldfile=HERE/'dependencies/STAGE08_RESULT.json';need(sha(oldfile)==PIN,'frozen projection changed');old=json.loads(oldfile.read_text())
    need((HERE/'dependencies/STAGE08_NORMAL.json').read_bytes()==(HERE/'dependencies/STAGE08_OPTIMIZED.json').read_bytes(),'prior parity differs')
    priorcheck=json.loads((HERE/'dependencies/STAGE08_NORMAL.json').read_text());need(priorcheck['result_sha256']==PIN and priorcheck['macro_cases']==70 and priorcheck['full_joint_type_cases']==574 and priorcheck['surviving_joint_type_cases']==15,'prior complete verification binding differs')
    source=json.loads((HERE/'STAGE09_PRODUCER_SOURCE_RECEIPT.json').read_text());need(source['producer_sha256']==sha(HERE/'stage09_binary_cap.py') and source['producer_runs']==1 and source['covering_solver_calls']==0,'producer source/scope differs')
    prior={tuple(tuple(row) for row in rec['normal_types']):rec for rec in old['full_joint_type_cases'] if (rec['a'],rec['j'])==(8,0)}
    complete=[];domain=[]
    for parts in partitions_eight():
        counts=collections.Counter(parts);types=[[5,0,44-len(parts)]]+[[5,h,n] for h,n in sorted(counts.items())];key=tuple(tuple(row) for row in types);complete.append(key)
        need(key in prior,'prior all-partition universe missing')
        if not prior[key]['excluded']:domain.append(key)
    need(len(complete)==22 and set(complete)==set(prior) and len(domain)==15,'prior survivor reduction incomplete')
    records={tuple(tuple(row) for row in rec['normal_types']):rec for rec in data['cases']}
    need(set(records)==set(domain) and len(data['cases'])==data['case_count']==15,'omitted or duplicated binary-cap case')
    inv=inverse();projection={};computed=[];rowcount=0
    def q(h,k,diagonal=False):
        key=(h,k,diagonal)
        if key not in projection:projection[key]=projected(inv,h,k,diagonal)
        return projection[key]
    for key in sorted(domain):
        types=[list(row) for row in key];need(sum(n for r,h,n in types)==44 and sum(h*n for r,h,n in types)==8 and all(r==5 for r,h,n in types),'joint survivor parameters differ')
        trace=F(0);upper=F(0);rows=[]
        for r,h,n in types:
            need(time.monotonic()<deadline,'UNKNOWN: checker deadline');diagonal=5-q(h,h,True);need(diagonal>=0,'survivor diagonal negative');trace+=n*diagonal;constant=diagonal**2;neighbors=[];caps=collections.Counter()
            for s,k,count in types:
                available=count-int(h==k)
                if not available:continue
                # The lemma permits plain twins but forbids a twin involving an external partner.
                cap=4-int(bool(h or k));c=1-q(h,k);caps[cap]+=available;constant+=available*c*c;neighbors.extend([(cap,c)]*available)
            load=14-h;need(0<=load<=sum(cap for cap,c in neighbors),'row outside complete integer capacity');maximum=all_maxima(neighbors,load)[load];need(maximum is not None,'row universe empty');rowupper=constant+maximum;upper+=n*rowupper;rowcount+=1
            rows.append({'h':h,'count':n,'residual_diagonal':enc(diagonal),'row_excess':load,'cap3_neighbors':caps[3],'cap4_neighbors':caps[4],'row_objective_maximum':enc(maximum),'row_frobenius_upper':enc(rowupper)})
        gap=trace*trace-9*upper;expected={'a':8,'j':0,'normal_types':types,'rank_cap':9,'trace':enc(trace),'frobenius_upper':enc(upper),'rank_slack':enc(gap),'row_receipts':rows,'excluded':gap>0}
        need(records[key]==expected,'independent coefficients, binary caps, row maxima or rank gap differ');computed.append(expected)
    survivors=[rec for rec in computed if not rec['excluded']];closed=not survivors
    need(sorted(data['survivors'],key=lambda rec:rec['normal_types'])==sorted(survivors,key=lambda rec:rec['normal_types']),'false survivor list')
    need(data['all18_pair_covers_excluded']==closed and data['fresh_independent_semantic_review_required']==closed,'false closure/review status')
    need(data['status']==('PROPOSED_PAIR19_CHILD68_PARENT230_PENDING_FRESH_REVIEW' if closed else 'INCONCLUSIVE_COMPLETE_BINARY_CAP_REFINEMENT'),'unjustified theorem status')
    need([data['candidate_pair_floor'],data['candidate_child_floor'],data['candidate_parent_floor']]==([19,68,230] if closed else [None,None,None]),'false candidate adoption')
    minimum=min(F(*rec['rank_slack']) for rec in computed);need(data['minimum_rank_slack']==enc(minimum),'minimum gap differs')
    vectors=loads=patterns=0
    for length in range(1,6):
        coeffs=[F(2*i-length,6) for i in range(length)]
        for caps in itertools.product([3,4],repeat=length):
            patterns+=1;brute={}
            for es in itertools.product(*(range(cap+1) for cap in caps)):
                vectors+=1;load=sum(es);score=sum((e*e+2*c*e for e,c in zip(es,coeffs)),F(0));brute[load]=max(brute.get(load,score),score)
            dynamic=all_maxima(list(zip(caps,coeffs)),sum(caps))
            for load,score in brute.items():need(dynamic[load]==score,'mixed-cap exhaustive toy differs');loads+=1
    need((patterns,vectors,loads)==(62,66429,965),'mixed toy universe incomplete')
    weights3=[sum(1<<i for i in points) for points in itertools.combinations(range(8),3)];weights4=[sum(1<<i for i in points) for points in itertools.combinations(range(8),4)];binary_checks=0
    for p in weights3:
        for qv in weights3:
            intersection=(p&qv).bit_count();need((intersection==3)==(p==qv),'binary equal-weight containment failed')
            for tight in weights4:
                binary_checks+=1
                if (p&tight).bit_count()!=(qv&tight).bit_count():need(intersection<=2,'distinct tight cross coordinates failed to distinguish columns')
    need(binary_checks==219520,'binary toy universe incomplete');need(time.monotonic()<deadline,'UNKNOWN: checker deadline')
    result={'status':'PASS_INDEPENDENT_BINARY_CAP_RECONSTRUCTION','result_sha256':sha(file),'case_count':15,'reconstructed_row_maxima':rowcount,'survivors':len(survivors),'minimum_rank_slack':enc(minimum),'all18_pair_covers_excluded':closed,'candidate_parent_floor':230 if closed else None,'complete_mixed_cap_patterns':patterns,'complete_toy_vectors':vectors,'toy_load_maxima':loads,'binary_containment_checks':binary_checks,'public_bound_changed':False,'previous227_assumed':False}
    with (HERE/sys.argv[2]).open('x') as out:out.write(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result))
if __name__=='__main__':
    try:main()
    except Exception as exc:print('REJECTED: '+str(exc),file=sys.stderr);sys.exit(2)
