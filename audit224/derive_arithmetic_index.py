"""Recount all finite domains and row families from the displayed formulas."""
import json
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = {
 '4': ([4], {0:53,4:1},36,36,30),
 '31': ([3,1], {0:52,1:1,3:1},49,36,30),
 '22': ([2,2], {0:52,2:2},50,36,30),
 '211': ([2,1,1], {0:51,1:2,2:1},49,43,30),
 '1111': ([1,1,1,1], {0:50,1:4},49,43,35)}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def derive():
    out = {}
    for tag,(part,pop,E,T,Q) in CASES.items():
        mc = lambda e: min(T,15 if e<=1 else 18+e)
        qc = lambda m: 2 if m==4 else min(m,Q)
        classes=[]
        for a in sorted(pop):
            for b in sorted(pop):
                if a>b:
                    continue
                count=comb(pop[a],2) if a==b else pop[a]*pop[b]
                if count:
                    classes.append(dict(a=a,b=b,population=count,
                        excess_cap=min(36+15*a,36+15*b,48+min(a,b))))
        vf=dict(n=17,p=E+1,t=T-3,q=Q,J=sum(c['excess_cap']+1 for c in classes),
                M=sum(mc(e)-3 for e in range(E+1)),
                N=sum(qc(m) for m in range(4,T+1)),defects=4)
        rf=dict(histograms=9,tight=3,high_tail=int(T==43)+int(Q==35),
                joint_counts=len(classes),joint_columns=E+1,vertex_budgets=len(pop),
                pair_transport_counts=E+1,pair_transport_loads=E+1,
                triple_transport_columns=T-3,quad_transport_counts=T-3,
                quad_transport_loads=T-3,quad_transport_columns=Q,
                defect_equations=2,exceptional_links=7 if tag=='1111' else 0,
                endpoint_links=T-18)
        m=json.loads((ROOT/f'package/cases/{tag}/MODEL.json').read_text())
        c=json.loads((ROOT/f'package/cases/{tag}/CERTIFICATE.json').read_text())
        actual=Counter('defects' if v['name'].startswith('z') else v['name'][0] for v in m['variables'])
        need(dict(actual)==vf and sum(vf.values())==len(m['variables']), 'every variable family')
        need(sum(rf.values())==len(m['rows']), 'complete row family count')
        row_sum=int(c['row_bound_sum_numerator']); correction=int(c['finite_bound_correction_numerator'])
        denominator=int(c['denominator'])
        need(str(Fraction(row_sum+correction,denominator))==c['exact_objective_upper_bound'], 'reduced exact bound')
        out[tag]=dict(partition=part,classes=classes,
            vertex_budgets={str(a):pop[a]*(36+15*a) for a in pop},
            variable_families=vf,row_families=rf,variables=sum(vf.values()),rows=sum(rf.values()),
            implicit_and_explicit_coefficient_positions=len(m['variables'])*len(m['rows']),
            explicit_nonzero_coefficients=sum(len(r['coefficients']) for r in m['rows']),
            point_moment=sum(pop[a]*comb(66+a,2) for a in pop),
            n_cell_upper=comb(223,2),p_cell_upper=comb(54,2),t_cell_upper=comb(54,3),
            q_cell_upper=comb(54,4),M_cell_upper=52*comb(54,2),N_cell_upper=51*comb(54,3),
            defect_uppers=dict(z3p=comb(54,3)*comb(T,2),z3m=comb(223,2)*comb(16,3),
                z4p=comb(54,4)*comb(Q,2),z4m=comb(223,2)*comb(16,4)),
            endpoint_thresholds=list(range(19,T+1)),
            all_endpoint_capacity_cells=(T-18)*vf['J'],
            certificate=dict(denominator=denominator,row_sum=row_sum,correction=correction,
                combined_numerator=row_sum+correction,upper=c['exact_objective_upper_bound'],
                positive_residual_columns=len(c['positive_column_residuals'])))
    return dict(status='PASS_COMPLETE_FINITE_ARITHMETIC_INDEX',cases=out,solver_calls=0,
                mathematical_semantics_formalized=False)


if __name__=='__main__':
    result=derive()
    p=ROOT/'ARITHMETIC_INDEX.json'
    if p.exists():
        need(json.loads(p.read_text())==result, 'arithmetic index preservation')
    else:
        with p.open('x',encoding='utf-8') as stream:
            stream.write(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
