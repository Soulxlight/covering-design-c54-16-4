"""Separate formula reconstruction of the already public 222 model.

No public author/verifier module is imported. Row names/order match the frozen
model for comparison; constants and sparse coefficients are derived here.
"""
from math import comb
from fractions import Fraction

def need(ok, message):
    if not ok:
        raise ValueError(message)

def build_model():
    v,k,b=54,16,221
    pair_floor=(52*5+14)//15
    point_floor=(53*pair_floor+14)//15
    triple_floor=(51+12)//13
    D=b*k-v*point_floor
    E=b*comb(k,2)-comb(v,2)*pair_floor
    cap=point_floor-pair_floor+D//2
    need((pair_floor,point_floor,triple_floor,D,E,cap)==(18,64,4,80,762,86),'222 domains')
    variables=[]; rows=[]
    def var(name,upper,objective=0):
        variables.append(dict(name=name,lower=0,upper=upper,objective=objective))
    def row(label,terms,bound=0,lower_only=False):
        rows.append(dict(label=label,coefficients={n:a for n,a in terms.items() if a},
                         lower=bound,upper=None if lower_only else bound))
    for s in range(k+1):var(f'n{s}',comb(b,2),-comb(s,3))
    for d in range(D+1):var(f'u{d}',v)
    for e in range(cap+1):var(f'p{e}',comb(v,2))
    for m in range(triple_floor,pair_floor+cap+1):var(f't{m}',comb(v,3),comb(m,2))
    cells=[(e,m) for e in range(cap+1) for m in range(triple_floor,pair_floor+e+1)]
    for e,m in cells:var(f'M{e}_{m}',comb(v,2)*(v-2))
    row('block_pairs',{f'n{s}':1 for s in range(k+1)},comb(b,2))
    row('point_profile',{f'u{d}':1 for d in range(D+1)},v)
    row('point_excess',{f'u{d}':d for d in range(D+1)},D)
    row('point_intersection',{**{f'n{s}':s for s in range(k+1)},**{f'u{d}':-comb(point_floor+d,2) for d in range(D+1)}})
    row('pair_profile',{f'p{e}':1 for e in range(cap+1)},comb(v,2))
    row('pair_excess',{f'p{e}':e for e in range(cap+1)},E)
    row('pair_intersection',{**{f'n{s}':comb(s,2) for s in range(k+1)},**{f'p{e}':-comb(pair_floor+e,2) for e in range(cap+1)}})
    row('triple_profile',{f't{m}':1 for m in range(triple_floor,pair_floor+cap+1)},comb(v,3))
    row('triple_load',{f't{m}':m for m in range(triple_floor,pair_floor+cap+1)},b*comb(k,3))
    for label,terms in [('tight_intersection3',{'n3':1,'t4':-5}),('tight_intersection4',{'n4':4,'t4':-1}),('tight_pair_triples',{'t4':3,'p0':-8}),('tight_pair_transport',{'M0_4':1,'p0':-8})]:
        row(label,terms,lower_only=True)
    for e in range(cap+1):
        for label,factor,rhs in [('count',lambda m:1,v-2),('load',lambda m:m,(k-2)*(pair_floor+e))]:
            terms={f'M{j}_{m}':factor(m) for j,m in cells if j==e}
            terms[f'p{e}']=-rhs
            row(f'transport_{label}{e}',terms)
    for m in range(triple_floor,pair_floor+cap+1):
        row(f'transport_column{m}',{**{f'M{e}_{j}':1 for e,j in cells if j==m},f't{m}':-3})
    need((len(cells),len(variables),len(rows))==(5046,5332,288),'222 full dimensions')
    return variables,rows

def check_model(model,variables,rows):
    need(model['parameters']==[54,16,4,221],'222 parameters')
    need(model['pair_excess_cap']==86 and model['objective_sense']=='maximize','222 cap/sense')
    need(model['variables']==variables,'222 variable/bound/objective mismatch')
    need(model['rows']==rows,'222 semantic row mismatch')

def replay_certificate(cert,variables,rows):
    scale=int(cert['denominator'])
    need(scale==10**9,'222 positive prescribed scale')
    weights=[int(x) for x in cert['row_numerators']]
    need(len(weights)==len(rows),'222 full row multipliers')
    sums=dict.fromkeys((x['name'] for x in variables),0)
    rhs=0
    for weight,row in zip(weights,rows):
        need(row['upper'] is not None or weight<=0,'222 sign on lower-only row')
        bound=row['upper'] if weight>0 else row['lower']
        rhs+=weight*bound
        for name,a in row['coefficients'].items():sums[name]+=weight*a
    residuals={x['name']:str(scale*x['objective']-sums[x['name']]) for x in variables if scale*x['objective']>sums[x['name']]}
    correction=sum(int(residuals.get(x['name'],0))*x['upper'] for x in variables)
    upper=Fraction(rhs+correction,scale)
    need(residuals==cert['positive_column_residuals'],'222 complete residual receipt')
    need(rhs==int(cert['row_bound_sum_numerator']),'222 signed RHS')
    need(correction==int(cert['finite_bound_correction_numerator']),'222 correction receipt')
    need(str(upper)==cert['exact_objective_upper_bound'],'222 exact upper receipt')
    need((rhs,correction,upper)==(-2660294744798,88273944,Fraction(-1330103235427,500000000)),'222 exact pinned values')
    return dict(variables=len(variables),rows=len(rows),coefficient_positions=len(variables)*len(rows),
                denominator=scale,row_bound_sum=rhs,correction=correction,numerator=rhs+correction,
                reduced_upper=str(upper),positive_residuals=residuals)

def check_diagnostic(model,variables,rows):
    witness=model['feasible_integer_diagnostic']
    need(set(witness)<=set(x['name'] for x in variables),'222 diagnostic names')
    for x in variables:
        value=witness.get(x['name'],0)
        need(type(value) is int and 0<=value<=x['upper'],'222 diagnostic bounds')
    for row in rows:
        load=sum(a*witness.get(n,0) for n,a in row['coefficients'].items())
        need(load>=row['lower'] and (row['upper'] is None or load<=row['upper']),'222 diagnostic row '+row['label'])
    objective=sum(x['objective']*witness.get(x['name'],0) for x in variables)
    need(objective==model['feasible_integer_diagnostic_objective']==-19318,'222 diagnostic objective')
    return objective
