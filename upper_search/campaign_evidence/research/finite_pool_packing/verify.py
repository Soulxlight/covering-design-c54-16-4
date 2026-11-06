#!/usr/bin/env python3
"""Verify a finite-pool packing certificate with exact integer arithmetic only."""
import hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parent

def need(ok,message):
 if not ok:raise ValueError(message)

def main():
 c=json.loads((R/'certificate.json').read_text());raw=(R/'pool.txt').read_bytes();need(hashlib.sha256(raw).hexdigest()==c['pool_sha256'],'pool hash');rows=[tuple(map(int,l.split())) for l in raw.decode().splitlines()];need(len(rows)==len(set(rows))==663,'distinct pool rows')
 for row in rows:need(row==tuple(sorted(row)) and len(row)==len(set(row))==16 and set(row)<=set(range(1,55)),'canonical legal16-set')
 need(c['parameters']==[54,16,4],'parameter metadata');cap=c['hole_cap'];fixed=c['fixed_rows'];need(cap==6 and fixed==19 and c['row_budget']==301,'certificate scope');inc=[0]*55
 for i,row in enumerate(rows):
  for p in row:inc[p]|=1<<i
 def support(t):
  need(t==sorted(t) and len(t)==len(set(t))==4 and set(t)<=set(range(1,55)),'canonical legal target');return inc[t[0]]&inc[t[1]]&inc[t[2]]&inc[t[3]]
 need(len(c['forced_singleton_targets'])==fixed,'forcing count')
 for i,targets in enumerate(c['forced_singleton_targets']):
  need(len(targets)>cap and len(set(map(tuple,targets)))==len(targets),'forcing multiplicity')
  for t in targets:need(support(t)==1<<i,'singleton owner')
 scores=[0]*(len(rows)-fixed);total=0;seen=set();weight_by_group={}
 for g in c['weighted_mandatory_supports']:
  w=g['weight'];cols=g['support_columns'];targets=g['mandatory_witness_targets'];need(type(w)is int and w>0,'positive integer weight');need(cols==sorted(set(cols)) and cols and all(type(j)is int and 0<=j<len(scores) for j in cols),'support columns');need(len(targets)>cap and len(set(map(tuple,targets)))==len(targets),'mandatory multiplicity');mask=sum(1<<(j+fixed) for j in cols)
  for t in targets:
   tt=tuple(t);need(tt not in seen,'distinct group witness');seen.add(tt);need(support(t)==mask,'exact target support')
  need(g['original_signature_index'] not in weight_by_group,'unique signature label');total+=w;weight_by_group[g['original_signature_index']]=w
  for j in cols:scores[j]+=w
 M=max(scores);K=c['row_budget']-fixed;need(M==c['max_alternative_score'] and total==c['integer_weight_sum'],'integer capacities');bound=(total+M-1)//M;need(K==c['alternative_budget'] and bound==c['alternative_column_lower_bound'],'capacity conclusion');slack=K*M-total
 for item in c['overlap_caps']:
  w=weight_by_group[item['signature_index']];need(w==item['integer_weight'] and item['at_most_selected_owners']>=1+slack//w,'weighted overlap cap')
 result={'status':'PASS_EXACT_FINITE_POOL_PACKING','finite_pool_rows':len(rows),'hole_cap':cap,'forced_rows':fixed,'necessary_alternative_rows':bound,'available_alternative_slots':K,'integer_weight_sum':total,'maximum_column_score':M,'overlap_caps_checked':len(c['overlap_caps']),'proves_infeasibility':False,'proves_global_lower_bound':False};print(json.dumps(result,indent=2));return result
if __name__=='__main__':main()
