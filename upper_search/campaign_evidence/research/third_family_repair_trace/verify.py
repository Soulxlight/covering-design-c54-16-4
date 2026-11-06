#!/usr/bin/env python3
"""Replay recorded point changes; independently count every remaining quadruple."""
import hashlib,itertools,json,pathlib
R=pathlib.Path(__file__).resolve().parent

def need(ok,msg):
 if not ok:raise ValueError(msg)
def check(raw,expected_hash,expected_holes):
 need(hashlib.sha256(raw).hexdigest()==expected_hash,'witness hash');rows=[tuple(map(int,l.split())) for l in raw.decode().splitlines()];need(len(rows)==len(set(rows))==301,'distinct301 rows')
 for row in rows:need(row==tuple(sorted(row)) and len(row)==len(set(row))==16 and set(row)<=set(range(1,55)),'legal canonical row')
 inc=[0]*55
 for i,row in enumerate(rows):
  for x in row:inc[x]|=1<<i
 holes_a={q for q in itertools.combinations(range(1,55),4) if not(inc[q[0]]&inc[q[1]]&inc[q[2]]&inc[q[3]])}
 covered={q for row in rows for q in itertools.combinations(row,4)};holes_b=set(itertools.combinations(range(1,55),4))-covered
 need(holes_a==holes_b and len(holes_a)==expected_holes,'two coverage methods disagree');need(expected_holes>0,'these are partials only');return [set(row) for row in rows]
c=json.loads((R/'TRACE.json').read_text());raw=(R/'parent_26.txt').read_bytes();rows=check(raw,c['parent_sha256'],c['parent_holes']);checks=[]
for step in c['steps']:
 for i,old,new in step['moves']:
  need(old in rows[i] and new not in rows[i],'invalid recorded point change');rows[i].remove(old);rows[i].add(new)
 raw=('\n'.join(' '.join(map(str,sorted(row))) for row in rows)+'\n').encode();check(raw,step['sha256'],step['holes']);checks.append({'sha256':step['sha256'],'holes':step['holes']})
need(raw==(R/'descendant_22.txt').read_bytes(),'recorded endpoint mismatch')
print(json.dumps({'status':'PASS_RECORDED_THIRD_FAMILY_REPAIRS','blocks':301,'initial_holes':26,'final_holes':22,'point_changes':sum(len(s['moves'])for s in c['steps']),'is_complete_cover':False,'global_bound_improvement_claimed':False,'two_independent_methods_agree':True,'checkpoints':checks},indent=2))
