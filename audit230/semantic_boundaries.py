"""Small complete covers, repeated rows, binary containment and rank boundaries."""
import itertools,json
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(x,m):
    if not x:raise ValueError(m)

def inverse(B):
    inv=[]
    for n in range(len(B)):
        v=[sum(inv[p][q]*B[q][n] for q in range(n)) for p in range(n)]
        d=F(B[n][n])-sum(F(B[n][p])*v[p] for p in range(n))
        need(d>0,'toy basis positive pivot')
        inv=[[inv[p][q]+v[p]*v[q]/d for q in range(n)]+[-v[p]/d] for p in range(n)]+[[-x/d for x in v]+[1/d]]
    return inv
def dot(x,y):return sum(p*q for p,q in zip(x,y))
def quad(x,inv,y):return sum(x[p]*sum(inv[p][q]*y[q] for q in range(len(y))) for p in range(len(x)))

# All 177100 indexed multisets of six triples on six points. Every complete
# cover has point degree3, exactly one repeated partner and a tight matching.
blocks=list(itertools.combinations(range(6),3));pairs=list(itertools.combinations(range(6),2))
masks=[sum(1<<pairs.index(pair) for pair in itertools.combinations(B,2)) for B in blocks]
families=complete=repeated=0;example=None
for indices in itertools.combinations_with_replacement(range(20),6):
    families+=1;covered=0
    for index in indices:covered|=masks[index]
    if covered!=(1<<15)-1:continue
    complete+=1;family=[blocks[i] for i in indices];repeated+=len(set(indices))<6
    columns=[[int(p in B) for B in family] for p in range(6)]
    need(all(sum(x)==3 for x in columns),'toy tight incidence floor')
    for p in range(6):
        codes=[dot(columns[p],columns[q]) for q in range(6) if q!=p]
        need(sorted(codes)==[1,1,1,1,2],'toy unique repeated partner')
    if example is None:example=family
need(families==177100 and example is not None,'complete toy family census')

# Here u is dependent: the target-specific strict16<18 condition cannot be
# replaced by a general assertion that ones is always an independent direction.
cols=[[int(p in B) for B in example] for p in range(6)]
T=[[dot(x,y) for y in cols] for x in cols];Tinverse=inverse(T)
u_projection=quad([3]*6,Tinverse,[3]*6)
need(u_projection==6,'toy all-ones dependence boundary')

# Repeat each row of this full covering. Check the actual residual Gram and
# external-partner support disjointness in all six indexed repeated-row covers.
residual_tests=[]
for repeated_row in range(6):
    family=example+[example[repeated_row]]
    cols=[[int(p in B) for B in family] for p in range(6)];degrees=list(map(sum,cols))
    tight=[p for p,r in enumerate(degrees) if r==3];normal=[p for p,r in enumerate(degrees) if r>3]
    basiscols=[cols[p] for p in tight]+[[1]*7]
    B=[[dot(x,y) for y in basiscols] for x in basiscols];inv=inverse(B)
    supports={p:{i for i,q in enumerate(tight) if dot(cols[p],cols[q])==2} for p in normal}
    need(all(not supports[p]&supports[q] for p,q in itertools.combinations(normal,2)),'external tight partners not disjoint')
    cross={p:[dot(cols[p],x) for x in basiscols] for p in normal}
    S=[[F(dot(cols[p],cols[q]))-quad(cross[p],inv,cross[q]) for q in normal] for p in normal]
    R=7-len(basiscols);trace=sum(S[i][i] for i in range(len(normal)));frob=sum(x*x for row in S for x in row)
    need(all(S[i][i]>=0 for i in range(len(normal))) and trace*trace<=R*frob,'toy residual trace/rank inequality')
    for p in normal:
        need(sum(dot(cols[p],cols[q])-1 for q in normal if q!=p)==2*degrees[p]-5-len(supports[p]),'toy complete residual-row load')
    residual_tests.append({'repeated_row':repeated_row,'tight':len(tight),'normal':len(normal),'residual_rank_cap':R,
                           'trace':[trace.numerator,trace.denominator],'frobenius':[frob.numerator,frob.denominator]})

# Target-weight binary tests. Plain twins are deliberately included; cross
# values differ only when actual vectors differ. Repeat-coordinate filtering
# checks that duplicate block positions leave the binary implication intact.
supports5=[sum(1<<i for i in X) for X in itertools.combinations(range(8),5)]
supports4=[sum(1<<i for i in X) for X in itertools.combinations(range(8),4)]
binary_checks=distinguished=plain_twins=0
for p in supports5:
    for q in supports5:
        m=(p&q).bit_count();need((m==5)==(p==q),'weight5 full overlap iff twins')
        plain_twins+=p==q
        for tight in supports4:
            binary_checks+=1
            if (p&tight).bit_count()!=(q&tight).bit_count():
                need(m<=4,'cross-coordinate distinguishes non-twins');distinguished+=1
duplicate_columns=[p for p in supports5 if (p&1)==((p>>1)&1)]
duplicate_tights=[t for t in supports4 if (t&1)==((t>>1)&1)]
repeated_binary_checks=0
for p in duplicate_columns:
    for q in duplicate_columns:
        for t in duplicate_tights:
            repeated_binary_checks+=1
            if (p&t).bit_count()!=(q&t).bit_count():need((p&q).bit_count()<=4,'repeated-row containment failure')
need(binary_checks==219520 and plain_twins==56,'complete weight5 toy universe')
result={'status':'PASS_COMPLETE_PAIR_COVER_REPETITION_PROJECTION_AND_BINARY_BOUNDARIES',
        'toy_pair_cover_families':families,'complete_toy_pair_covers':complete,'repeated_complete_minimum_covers':repeated,
        'all_ones_dependent_toy_projection_norm':[u_projection.numerator,u_projection.denominator],
        'target_ones_independence_uses_strict_16_below_18':True,'repeated_row_residual_tests':residual_tests,
        'weight5_binary_tight_cross_tests':binary_checks,'distinguished_pairs_cross_tests':distinguished,
        'plain_twin_cases_kept':plain_twins,'duplicate_coordinate_binary_tests':repeated_binary_checks,
        'no_target_cover_search':True,'public_actions':0}
(HERE/'SEMANTIC_BOUNDARY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
