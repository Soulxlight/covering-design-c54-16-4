"""Fresh, solver-free semantic fixtures and exact certificate reconstruction.

Adapted with attribution from the independent task-5 reviewer reconstruction.
No author generator or auditor is imported. Assertions are explicit exceptions,
so this verifier has identical checks under normal Python and python -O.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
from math import comb
from pathlib import Path
import argparse
import copy
import json
import sys
import time
import zipfile

DATA = Path(__file__).resolve().parent / 'data'
PETA = DATA

def need(ok, message):
    if not ok:
        raise ValueError(message)

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def build_model():
    # Derive all parameter constants from the hypothetical covering's counts.
    v, k, b, r, ell = 53, 15, 65, 18, 4
    budget = b*k-v*r
    pair_cap = r+budget//2
    triple_cap = r+budget//3
    variables, rows = [], []
    def var(name, upper, objective=0):
        variables.append(dict(name=name, lower=0, upper=upper, objective=objective))
    def row(label, coefficients, rhs=0, relation='eq'):
        rows.append(dict(label=label, coefficients={n:a for n,a in coefficients.items() if a},
                         rhs=rhs, relation=relation))
    for s in range(k+1): var(f'n{s}', comb(b,2), -comb(s,2))
    for d in range(budget+1): var(f'u{d}', v)
    for e in range(pair_cap-ell+1): var(f'p{e}', comb(v,2), comb(ell+e,2))
    for m in range(1,triple_cap+1): var(f'q{m}', comb(v,3))
    # Support sets are derived via containment and singleton coverage, rather
    # than accepting a producer's list of permitted names.
    ms = [(d,e) for d in range(budget+1) for e in range(pair_cap-ell+1)
          if ell+e <= r+d]
    ns = [(e,m) for e in range(pair_cap-ell+1) for m in range(1,triple_cap+1)
          if m <= ell+e and m-1 <= (k-2)*(ell+e)-(v-2)]
    for d,e in ms: var(f'M{d}_{e}', v*(v-1))
    for e,m in ns: var(f'N{e}_{m}', comb(v,2)*(v-2))
    row('block_pairs', {f'n{s}':1 for s in range(k+1)}, comb(b,2))
    row('point_profile', {f'u{d}':1 for d in range(budget+1)}, v)
    row('point_excess', {f'u{d}':d for d in range(budget+1)}, budget)
    row('pair_profile', {f'p{e}':1 for e in range(pair_cap-ell+1)}, comb(v,2))
    row('pair_excess', {f'p{e}':e for e in range(pair_cap-ell+1)}, b*comb(k,2)-ell*comb(v,2))
    row('triple_profile', {f'q{m}':1 for m in range(1,triple_cap+1)}, comb(v,3))
    row('triple_load', {f'q{m}':m for m in range(1,triple_cap+1)}, b*comb(k,3))
    row('first_intersection', {**{f'n{s}':s for s in range(k+1)},
        **{f'u{d}':-comb(r+d,2) for d in range(budget+1)}})
    row('third_intersection', {**{f'n{s}':comb(s,3) for s in range(k+1)},
        **{f'q{m}':-comb(m,2) for m in range(1,triple_cap+1)}})
    for d in range(budget+1):
        row(f'point_pair_count{d}', {**{f'M{a}_{e}':1 for a,e in ms if a==d}, f'u{d}':-(v-1)})
        row(f'point_pair_load{d}', {**{f'M{a}_{e}':ell+e for a,e in ms if a==d}, f'u{d}':-(k-1)*(r+d)})
    for e in range(pair_cap-ell+1):
        row(f'point_pair_column{e}', {**{f'M{d}_{j}':1 for d,j in ms if j==e}, f'p{e}':-2})
    row('tight_point_neighbors', {'u0':8,'M0_0':-1}, relation='le')
    for e in range(pair_cap-ell+1):
        row(f'pair_triple_count{e}', {**{f'N{j}_{m}':1 for j,m in ns if j==e}, f'p{e}':-(v-2)})
        row(f'pair_triple_load{e}', {**{f'N{j}_{m}':m for j,m in ns if j==e}, f'p{e}':-(k-2)*(ell+e)})
    for m in range(1,triple_cap+1):
        row(f'pair_triple_column{m}', {**{f'N{e}_{j}':1 for e,j in ns if j==m}, f'q{m}':-3})
    row('tight_pair_intersection2', {'p0':5,'n2':-1}, relation='le')
    row('tight_pair_intersection3', {'p0':1,'n3':-3}, relation='le')
    need((len(variables),len(rows),len(ms),len(ns))==(975,156,495,392), 'independent dimensions')
    return variables, rows

def check_model(model, variables, rows):
    need(model['variables']==variables, 'semantic variable/bound/objective mismatch')
    need(model['rows']==rows, 'semantic row mismatch')
    need(model['parameters']==[53,15,3,65] and model['objective_sense']=='maximize','parameters/objective sense')
    expected={'point_degree_floor':18,'pair_degree_floor':4,'point_excess_total':21,
              'pair_excess_total':1313,'pair_excess_cap':24,'triple_degree_cap':25}
    need(all(model.get(k)==v for k,v in expected.items()), 'metadata constants')

def replay_certificate(cert, variables, rows, verify_fields=True):
    scale=int(cert['denominator'])
    need(scale>0, 'positive scale')
    weights=list(map(int,cert['row_numerators']))
    need(len(weights)==len(rows),'full multiplier dimensions')
    columns=dict.fromkeys((v['name'] for v in variables),0)
    rhs=0
    for weight,row in zip(weights,rows):
        need(row['relation']=='eq' or weight>=0,'negative inequality multiplier')
        rhs+=weight*row['rhs']
        for n,a in row['coefficients'].items(): columns[n]+=weight*a
    positive={v['name']:str(scale*v['objective']-columns[v['name']]) for v in variables
              if scale*v['objective']>columns[v['name']]}
    correction=sum(int(positive.get(v['name'],'0'))*v['upper'] for v in variables)
    bound=Fraction(rhs+correction,scale)
    if verify_fields:
        need(cert['row_bound_sum_numerator']==str(rhs),'row RHS receipt')
        need(cert['positive_column_residuals']==positive,'complete residual receipt')
        need(cert['finite_bound_correction_numerator']==str(correction),'finite correction receipt')
        need(cert['exact_objective_upper_bound']==str(bound),'exact rational receipt')
    return dict(row_bound_sum=rhs, correction=correction, numerator=rhs+correction,
                denominator=scale, reduced_upper=str(bound), positive_residuals=positive,
                nonzero_row_multipliers=sum(w!=0 for w in weights),
                inequality_multipliers={row['label']:weights[i] for i,row in enumerate(rows) if row['relation']=='le'})

def mutations(model,cert,variables,rows):
    rejected=[]
    fixtures=[('drop n15',lambda m:m['variables'].pop(15)),
              ('reverse objective',lambda m:m.update(objective_sense='minimize')),
              ('change bound',lambda m:m['variables'][0].update(upper=2079)),
              ('change load',lambda m:m['rows'][10]['coefficients'].update(u0=-251)),
              ('drop row',lambda m:m['rows'].pop()),
              ('reverse cut',lambda m:m['rows'][-1]['coefficients'].update(n3=3))]
    for label,change in fixtures:
        obj=copy.deepcopy(model);change(obj)
        try: check_model(obj,variables,rows)
        except ValueError: rejected.append(label)
        else: raise ValueError('accepted damaged model '+label)
    fixtures=[('negative cut weight',lambda c:c['row_numerators'].__setitem__(-1,'-1')),
              ('zero denominator',lambda c:c.update(denominator='0')),
              ('undercharge residuals',lambda c:c.update(finite_bound_correction_numerator='0')),
              ('drop multiplier',lambda c:c['row_numerators'].pop()),
              ('omit residual',lambda c:c['positive_column_residuals'].pop('M17_24'))]
    for label,change in fixtures:
        obj=copy.deepcopy(cert);change(obj)
        try: replay_certificate(obj,variables,rows)
        except ValueError: rejected.append(label)
        else: raise ValueError('accepted damaged certificate '+label)
    return rejected

def peta_arithmetic():
    chords=[]
    for r in range(18,40):
        maximum=15 if r==19 else r
        for m in range(4,maximum+1):
            f=Fraction(comb(m,2)-52*(m==4))
            cap=(11*m-45-45*(m==4) if r==18 else
                 Fraction(19*m-75,2) if r==19 else Fraction((r+4)*m-5*r,2))
            need(f<=cap,f'chord r={r}, m={m}')
            chords.append([r,m,str(cap-f)])
    need(len(chords)==557,'chord count')
    for s in range(16):
        need((s-6)*(s-7)>=0,'integer polynomial')
        need((s-6)*(s-7)==2*comb(s,2)-12*s+42,'polynomial identity')
    g18=11*252-45*52-45*8-12*comb(18,2)
    g19=Fraction(19*266-75*52,2)-12*comb(19,2)
    need((g18,g19)==(-1764,-1475),'local contributions')
    slacks=[]
    for d in range(2,22):
        slack=-1764+289*d-((18+d)**2-96*(18+d))
        need(slack==(d-2)*(347-d)+334 and slack>0,'envelope')
        slacks.append(slack)
    final={str(b):42*comb(b,2)-1764*53+289*(15*b-954) for b in (64,65)}
    need(final=={'64':-7086,'65':-63},'contradictions')
    # Show why the degree-19 improvement is essential to this analytic envelope.
    return dict(chord_cases=len(chords),minimum_generic_envelope_slack=min(slacks),
                local_g18=g18,local_g19=str(g19),contradictions=final,
                generic_g19_without_avoidance=19**2-96*19,
                generic_degree19_envelope_violation=(19**2-96*19)-(-1764+289))

def support_audit():
    records=[];total=0
    for m in range(16,20):
        inside=(1<<m)-1
        raw=[sum(1<<i for i in s) for s in combinations(range(19),4)]
        supports=sorted(s for s in raw if (s&inside).bit_count() in (1,2))
        document=read(PETA/'support'/f'SUPPORT_GRAPH_m{m}.json')
        need([v['mask'] for v in document['candidate_supports']]==supports,'all binary supports')
        need(len(raw)==3876,'complete raw supports')
        edges=[];degrees=Counter();pairs=0
        # Construct a coloring directly from the at-most-three outside pairs.
        outside_pairs=list(combinations(range(m,19),2))
        colors={}
        for s in supports:
            outside=tuple(i for i in range(m,19) if s>>i&1)
            colors[s]=outside_pairs.index(outside) if len(outside)==2 else 0
        for i,a in enumerate(supports):
            for j in range(i+1,len(supports)):
                pairs+=1;b=supports[j]
                common=(a&b).bit_count()
                compatible=(common==1 or (common==2 and (a&inside).bit_count()==1 and (b&inside).bit_count()==1))
                if compatible:
                    need(colors[a]!=colors[b],'independent proper coloring')
                    edges.append((i,j));degrees[i]+=1;degrees[j]+=1
        csv='left_id,right_id\n'+''.join(f'{i},{j}\n' for i,j in edges)
        need(csv==(PETA/'support'/f'edges_m{m}.csv').read_text(encoding='ascii'),'entire edge list')
        cap=3 if m==16 else 1 if m==17 else 0
        witnesses={16:[196611,327692,393264],17:[393219],18:[],19:[]}[m]
        need(len(witnesses)==cap and all(s in supports for s in witnesses),'explicit clique vertices')
        for a,b in combinations(witnesses,2):
            need((a&b).bit_count()==1,'attaining clique edges')
        forced=5*51-(19*14-m)
        need(forced==m-11 and forced>cap,'avoidance contradiction')
        need((len(edges),pairs)==(document['edge_count'],document['pairs_checked']),'saved graph counts')
        total+=pairs
        records.append(dict(m=m,candidates=len(supports),pairs=pairs,edges=len(edges),
            isolated=len(supports)-len(degrees),proper_color_cap=cap,forced_tight_points=forced))
    need(total==79680,'full pair census')
    return dict(raw_supports=4*3876,total_candidate_pairs=total,cases=records)

def family_counts(v,k,blocks):
    pts=range(v)
    sets=list(map(set,blocks))
    r={x:sum(x in B for B in sets) for x in pts}
    lam={P:sum(set(P)<=B for B in sets) for P in combinations(pts,2)}
    mu={T:sum(set(T)<=B for B in sets) for T in combinations(pts,3)}
    n=Counter(len(A&B) for A,B in combinations(sets,2))
    return sets,r,lam,mu,n

def verify_toy_triple(v,k,blocks):
    sets,r,lam,mu,n=family_counts(v,k,blocks)
    # Identities are verified even for incomplete covers and duplicate occurrences.
    for j,degrees in ((1,r),(2,lam),(3,mu)):
        need(sum(comb(s,j)*c for s,c in n.items())==sum(comb(m,2) for m in degrees.values()),'toy moment')
    for x in range(v):
        need(sum(m for P,m in lam.items() if x in P)==(k-1)*r[x],'toy point transport load')
    for P,m in lam.items():
        need(sum(a for T,a in mu.items() if set(P)<=set(T))==(k-2)*m,'toy pair transport load')
    if not all(mu.values()): return False,False
    ell=(v-2+k-3)//(k-2)
    point_floor=min(r.values())
    budget=len(blocks)*k-v*point_floor
    for P,m in lam.items():
        need(m>=ell and m<=min(r[x] for x in P),'toy pair floor/containment')
        need(m<=point_floor+budget//2,'toy endpoint excess cap')
    for T,a in mu.items():
        need(a<=point_floor+budget//3,'toy triple excess cap')
        for P in combinations(T,2):
            need(a<=lam[P] and a<=1+(k-2)*lam[P]-(v-2),'toy N support bound')
    M=Counter((r[x],m) for P,m in lam.items() for x in P)
    N=Counter((lam[P],a) for T,a in mu.items() for P in combinations(T,2))
    for d,ct in Counter(r.values()).items():
        need(sum(c for (j,_),c in M.items() if j==d)==(v-1)*ct,'toy M row count')
        need(sum(m*c for (j,m),c in M.items() if j==d)==(k-1)*d*ct,'toy M row load')
        minimum=(v-1)-((k-1)*d-ell*(v-1))
        need(M[(d,ell)]>=minimum*ct,'toy tight point neighbors')
    for m,ct in Counter(lam.values()).items():
        need(sum(c for (_,j),c in M.items() if j==m)==2*ct,'toy M column')
        need(sum(c for (j,_),c in N.items() if j==m)==(v-2)*ct,'toy N count')
        need(sum(a*c for (j,a),c in N.items() if j==m)==(k-2)*m*ct,'toy N load')
    for a,ct in Counter(mu.values()).items():
        need(sum(c for (_,j),c in N.items() if j==a)==3*ct,'toy N column')
    tight=[P for P,m in lam.items() if m==ell]
    if ell*(k-2)==v-1:
        for P in tight:
            through=[B for B in sets if set(P)<=B]
            outs=Counter(x for B in through for x in B-set(P))
            need(sorted(outs.values())==[1]*(v-3)+[2],'one-surplus extension distribution')
            intersections=Counter(len(A&B) for A,B in combinations(through,2))
            need(intersections==Counter({2:comb(ell,2)-1,3:1}),'tight pair exact intersections')
        need(n[2]>=(comb(ell,2)-1)*len(tight) and 3*n[3]>=len(tight),'tight pair global assignments')
    # Padding test exercises intersection size k and recomputes incidence counts.
    return True,bool(tight)

def small_fixtures():
    all_families=complete=tight_covers=duplicate_covers=0
    types=list(combinations(range(5),4))
    for b in range(9):
        for indices in combinations_with_replacement(range(len(types)),b):
            blocks=[types[i] for i in indices]
            ok,tight=verify_toy_triple(5,4,blocks)
            all_families+=1;complete+=ok;tight_covers+=tight
            duplicate_covers+=ok and len(set(indices))<len(indices)
    pair_families=pair_complete=tight_points=0
    types=list(combinations(range(4),3))
    for b in range(7):
        for indices in combinations_with_replacement(range(len(types)),b):
            blocks=[set(types[i]) for i in indices]
            pair_families+=1
            if not all(any(set(P)<=B for B in blocks) for P in combinations(range(4),2)):continue
            pair_complete+=1
            for x in range(4):
                through=[B for B in blocks if x in B]
                if len(through)==2:
                    outside=Counter(y for B in through for y in B-{x})
                    need(sorted(outside.values())==[1,1,2],'toy unique repeated partner')
                    tight_points+=1
    # A repeated block pair must be counted at s=k; dropping it violates F2.
    padded=[tuple(x for x in range(5) if x!=j) for j in range(5)]+[(0,1,2,3)]
    sets,r,lam,mu,n=family_counts(5,4,padded)
    need(n[4]==1,'duplicate occurrence retained')
    discrepancy=sum(comb(m,2) for m in lam.values())-sum(comb(s,2)*c for s,c in n.items() if s<4)
    need(discrepancy==comb(4,2),'duplicate mutation detected')
    need(verify_toy_triple(5,4,padded)[0],'padding preserves coverage')
    # Completeness is indispensable: tight incidence counts alone do not imply
    # the one-surplus distribution. This is deliberately incomplete.
    incomplete=[{0,1,2,3},{0,1,2,3}]
    extras=Counter(x for B in incomplete for x in B-{0,1})
    need(sorted(extras.values())==[2,2] and len(extras)<3,'incomplete witness recognized')
    return dict(triple_multisets_checked=all_families,complete_triple_covers=complete,
                complete_covers_with_tight_pairs=tight_covers,complete_covers_with_duplicate_blocks=duplicate_covers,
                pair_multisets_checked=pair_families,complete_pair_covers=pair_complete,
                tight_point_instances=tight_points,duplicate_omission_objective_error=discrepancy,
                complete_padding_fixture=True,incomplete_cover_guard_fixture=True)
