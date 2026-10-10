"""Independent exact bordering inverse, h-first joint types and grouped row DP.

No author module is imported. All universes and values are reconstructed from
the hypothesized binary 18-by-52 incidence matrix and then compared to records.
"""
import collections,hashlib,itertools,json,math,sys,time
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
PACKET=HERE/'packet'
def need(x,m):
    if not x:raise ValueError(m)
def enc(x):
    x=F(x);return [x.numerator,x.denominator]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def basis(a,j):
    B=[[4 if p==q else 1 for q in range(a)]+[4] for p in range(a)]+[[4]*a+[18]]
    for p in range(0,2*j,2):B[p][p+1]=B[p+1][p]=2
    # Grow the exact inverse by bordering the actual integer Gram. This is
    # distinct from the packet's Gauss-Jordan and LDL implementations.
    inv=[];pivots=[]
    for n in range(a+1):
        vec=[sum(inv[p][q]*B[q][n] for q in range(n)) for p in range(n)]
        schur=F(B[n][n])-sum(F(B[n][p])*vec[p] for p in range(n))
        need(schur>0,'basis not positive definite')
        inv=[[inv[p][q]+vec[p]*vec[q]/schur for q in range(n)]+[-vec[p]/schur] for p in range(n)]+[[-v/schur for v in vec]+[1/schur]]
        pivots.append(schur)
    for p in range(a+1):
        for q in range(a+1):need(sum(B[p][k]*inv[k][q] for k in range(a+1))==int(p==q),'bordering inverse identity')
    return B,inv,pivots

def q_actual(inv,a,j,r,h,s,k,diag=False):
    x=[1]*a+[r];y=[1]*a+[s]
    need(h<=a-2*j and k<=a-2*j,'external cross support domain')
    start=2*j if diag else 2*j+h
    need(start+k<=a and (not diag or (r,h)==(s,k)),'support disjointness/diagonal')
    for p in range(2*j,2*j+h):x[p]=2
    for p in range(start,start+k):y[p]=2
    return sum(x[p]*sum(inv[p][t]*y[t] for t in range(a+1)) for p in range(a+1))

def partitions(total,maximum=None):
    # Descending part lists, opposite traversal from the author producer.
    if total==0:yield ();return
    maximum=total if maximum is None else min(maximum,total)
    for head in range(maximum,0,-1):
        for tail in partitions(total-head,head):yield (head,)+tail

def all_types(D,H,N):
    """Enumerate partner partitions first, then allocate D degree units.

    D<=2. Assign one degree unit, two to one point, or one to each of two.
    Allocation among equal h classes is quotiented by their multiplicities.
    """
    need(D in (0,1,2),'undeclared degree-excess domain')
    records=set()
    for hs in partitions(H):
        base=collections.Counter({(5,h):hs.count(h) for h in set(hs)})
        base[(5,0)]=N-len(hs);need(base[(5,0)]>=0,'partner profile point count')
        hvalues=sorted(h for (r,h),count in base.items() if count)
        changes=[()] if D==0 else [((h,D),) for h in hvalues]
        if D==2:
            changes.extend(((h,1),(k,1)) for i,h in enumerate(hvalues) for k in hvalues[i:]
                           if h!=k or base[(5,h)]>=2)
        for allocation in changes:
            counts=base.copy()
            for h,d in allocation:
                counts[(5,h)]-=1;counts[(5+d,h)]+=1
            need(all(n>=0 for n in counts.values()),'invalid allocation')
            record=tuple((r,h,n) for (r,h),n in sorted(counts.items()) if n)
            need(sum(n for r,h,n in record)==N and sum((r-5)*n for r,h,n in record)==D and sum(h*n for r,h,n in record)==H,'joint conservation')
            records.add(record)
    return sorted(records)

def grouped_max(neighbors,load):
    """Exact max-plus convolution over groups with equal cap/coefficient.

    Within a group, exchange towards endpoints shows max sum e^2 at fixed
    load t is floor(t/c)c^2+(t mod c)^2; linear terms are fixed by that load.
    Convolving every group load exhausts all complete integer row assignments.
    """
    scale=math.lcm(*(z.denominator for cap,z in neighbors)) if neighbors else 1
    groups=collections.Counter(neighbors)
    dp=[0]+[None]*load
    for (cap,z),number in sorted(groups.items()):
        linear=int(z*scale)
        scores=[]
        for t in range(min(number*cap,load)+1):
            full,rem=divmod(t,cap);scores.append(scale*(full*cap*cap+rem*rem)+2*linear*t)
        new=[None]*(load+1)
        for used,value in enumerate(dp):
            if value is None:continue
            for t in range(min(len(scores)-1,load-used)+1):
                target=used+t;candidate=value+scores[t]
                if new[target] is None or candidate>new[target]:new[target]=candidate
        dp=new
    need(dp[load] is not None,'empty integer row domain')
    return F(dp[load],scale)

def main():
    started=time.monotonic();old=json.loads((PACKET/'stage08/STAGE08_RESULT.json').read_text(encoding='utf-8'))
    new=json.loads((PACKET/'stage09/STAGE09_RESULT.json').read_text(encoding='utf-8'))
    supplied_macro={(rec['a'],rec['j']):rec for rec in old['macro_cases']}
    supplied_full={(rec['a'],rec['j'],tuple(map(tuple,rec['normal_types']))):rec for rec in old['full_joint_type_cases']}
    supplied_refined={tuple(map(tuple,rec['normal_types'])):rec for rec in new['cases']}
    need(len(supplied_macro)==len(old['macro_cases'])==70,'macro count/duplicates')
    need(len(supplied_full)==len(old['full_joint_type_cases'])==574,'full count/duplicates')
    macros=[];full=[];refined=[];bases={};projection_cache={};row_count=refined_row_count=0;macro_survivors=[];type_counts=[]
    def q(a,j,r,h,s,k,diag=False):
        key=(a,j,r,h,s,k,diag)
        if key not in projection_cache:projection_cache[key]=q_actual(bases[(a,j)][1],a,j,r,h,s,k,diag)
        return projection_cache[key]
    def full_case(a,j,types,refine=False):
        nonlocal row_count,refined_row_count
        R=17-a;trace=F(0);U=F(0);rows=[];negative=[]
        for r,h,n in types:
            diagonal=r-q(a,j,r,h,r,h,True);trace+=n*diagonal
            if diagonal<0:negative.append([r,h,n,enc(diagonal)])
            constant=diagonal*diagonal;neighbors=[];caps=collections.Counter()
            for s,k,count in types:
                available=count-int((r,h)==(s,k))
                if not available:continue
                cap=(3 if h or k else 4) if refine else min(r,s)-1
                z=1-q(a,j,r,h,s,k);constant+=available*z*z
                neighbors.extend([(cap,z)]*available);caps[cap]+=available
            load=13*r-51-h
            need(0<=load<=sum(cap for cap,z in neighbors),'row capacity domain')
            optimum=grouped_max(neighbors,load);upper=constant+optimum;U+=n*upper
            if refine:
                need(r==5,'binary cap applied beyond weight five')
                refined_row_count+=1
                rows.append({'h':h,'count':n,'residual_diagonal':enc(diagonal),'row_excess':load,
                             'cap3_neighbors':caps[3],'cap4_neighbors':caps[4],
                             'row_objective_maximum':enc(optimum),'row_frobenius_upper':enc(upper)})
            else:
                row_count+=1
                rows.append({'r':r,'h':h,'count':n,'residual_diagonal':enc(diagonal),'row_excess':load,
                             'row_objective_maximum':enc(optimum),'row_frobenius_upper':enc(upper)})
        gap=trace*trace-R*U
        record={'a':a,'j':j,'normal_types':[list(t) for t in types],'rank_cap':R,'trace':enc(trace),
                'frobenius_upper':enc(U),'rank_slack':enc(gap),'row_receipts':rows,'excluded':bool(negative) or gap>0}
        if not refine:record['negative_residual_diagonals']=negative
        return record
    for a in range(8,18):
        for j in range(a//2+1):
            bases[(a,j)]=basis(a,j)
            L=52-a-(a-8)-(a-2*j);R=17-a;plain=q(a,j,5,0,5,0)
            need(L>=5 and 1<plain<F(3,2),'principal-row premises')
            # Independently maximize each possible within-principal load 0..14,
            # rather than assuming exact14 and the pre-derived square constant52.
            z=1-plain
            extra=max(grouped_max([(4,z)]*(L-1),load) for load in range(15))
            need(extra==52+28*z,'principal load14 maximum')
            trace=L*(5-plain);U=L*((5-plain)**2+(L-1)*z*z+extra);gap=trace*trace-R*U
            record={'a':a,'j':j,'non_tight_points':52-a,'degree_excess':a-8,'external_tight_partners':a-2*j,
                    'guaranteed_plain_columns':L,'rank_cap':R,'plain_projection':enc(plain),'trace':enc(trace),
                    'frobenius_upper':enc(U),'rank_slack':enc(gap),'excluded':gap>0}
            need(supplied_macro.get((a,j))==record,'macro reconstruction mismatch');macros.append(record)
            if gap>0:continue
            need(a<=10,'unhandled extra-degree macro');macro_survivors.append((a,j))
            profiles=all_types(a-8,a-2*j,52-a);type_counts.append([a,j,len(profiles)])
            for types in profiles:
                key=(a,j,types);computed=full_case(a,j,types)
                need(supplied_full.get(key)==computed,'full joint/projection/row mismatch');full.append(computed)
                if not computed['excluded']:
                    need((a,j)==(8,0),'unexpected survivor macro')
                    tightened=full_case(a,j,types,True)
                    need(supplied_refined.get(types)==tightened,'refined coefficients/caps/maximum mismatch');refined.append(tightened)
            print(json.dumps({'macro':[a,j],'joint_types':len(profiles),'elapsed_seconds':round(time.monotonic()-started,3)}),flush=True)
            need(time.monotonic()-started<60,'UNKNOWN: bounded reconstruction deadline')
    need(set(supplied_macro)=={(a,j) for a in range(8,18) for j in range(a//2+1)},'complete macro key set')
    need(len(full)==574 and len(refined)==len(supplied_refined)==15 and row_count==2363 and refined_row_count==48,'all joint/row universes')
    need({(r['a'],r['j'],tuple(map(tuple,r['normal_types']))) for r in full}==set(supplied_full),'complete full case key set')
    survivors=[r for r in full if not r['excluded']]
    need(sorted(survivors,key=lambda r:r['normal_types'])==sorted(old['surviving_joint_type_cases'],key=lambda r:r['normal_types']),'exact old survivor set')
    need(all(r['excluded'] for r in refined),'nonpositive refined gap')
    minimum=min(F(*r['rank_slack']) for r in refined);need(minimum==F(686878,1225),'weakest refined gap')
    # Independent mixed-group tiny optimization census, including genuinely
    # equal coefficients and multiple caps, checked against all allocations.
    toy_vectors=toy_models=toy_loads=0
    for length in range(1,5):
        coefficient_sets=[[F(0)]*length,[F((i%2)*2-1,2) for i in range(length)],[F(i-length,3) for i in range(length)]]
        for caps in itertools.product(range(2,6),repeat=length):
            for zs in coefficient_sets:
                groups=list(zip(caps,zs));brute={};toy_models+=1
                for es in itertools.product(*(range(c+1) for c in caps)):
                    toy_vectors+=1;t=sum(es);value=sum((e*e+2*z*e for e,z in zip(es,zs)),F(0))
                    brute[t]=max(value,brute.get(t,value))
                for t,value in brute.items():need(grouped_max(groups,t)==value,'grouped row recurrence brute mismatch');toy_loads+=1
    # Exactly check all binary supports on an 8-set at weights0..4. Equal
    # weight and full intersection iff equal, with every test coordinate.
    binary_pairs=binary_distinguish=0
    for weight in range(5):
        supports=[sum(1<<i for i in T) for T in itertools.combinations(range(8),weight)]
        for p in supports:
            for other in supports:
                overlap=(p&other).bit_count();need((overlap==weight)==(p==other),'equal-weight containment');binary_pairs+=1
                for i in range(8):
                    if ((p>>i)&1)!=((other>>i)&1):
                        need(overlap<=weight-1,'a binary coordinate distinguishes twins');binary_distinguish+=1
    need((53*19+14)//15==68 and (54*68+15)//16==230,'independent link lifts')
    need(15*67==1005<1007==53*19 and 16*229==3664<3672==54*68,'strict deficient incidences')
    result={'status':'PASS_INDEPENDENT_BORDERING_TYPE_ENUMERATION_GROUPED_ROW_RECONSTRUCTION',
            'author_code_imported':False,'matrix_algorithm':'Positive-Schur exact bordering inverse of actual integer basis',
            'type_algorithm':'Partner-count partitions first, then all allocations of zero/one/two degree units',
            'row_algorithm':'Exact max-plus convolution over equal-cap/equal-coefficient groups',
            'macro_cases':macros,'macro_survivors':macro_survivors,'joint_type_counts':type_counts,
            'full_joint_cases':full,'refined_cases':refined,'full_row_maxima':row_count,'refined_row_maxima':refined_row_count,
            'old_survivors':len(survivors),'all_refined_excluded':True,'minimum_refined_gap':enc(minimum),
            'complete_toy_vectors':toy_vectors,'complete_toy_models':toy_models,'complete_toy_load_maxima':toy_loads,
            'binary_support_pairs':binary_pairs,'binary_distinguishing_coordinates':binary_distinguish,
            'pair_floor':19,'child_floor':68,'parent_floor':230,'previous227_assumed':False,
            'elapsed_seconds':time.monotonic()-started,'script_sha256':sha(Path(__file__)),'public_actions':0}
    out=HERE/('INDEPENDENT_OPTIMIZED.json' if sys.flags.optimize else 'INDEPENDENT_NORMAL.json')
    need(not out.exists(),'output exists');out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('macro_cases','full_joint_cases','refined_cases')},indent=2))

if __name__=='__main__':main()
