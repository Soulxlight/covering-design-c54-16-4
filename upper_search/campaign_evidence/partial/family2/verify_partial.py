#!/usr/bin/env python3
"""Verify the pinned incomplete design; success confirms its stated holes."""
import argparse,hashlib,itertools,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'verification'))
import verify_colex
import verify_incidence

def check(candidate,blocks,expected_hash=None,expected_holes=None):
 candidate=Path(candidate);raw=candidate.read_bytes();digest=hashlib.sha256(raw).hexdigest()
 if expected_hash is not None and digest!=expected_hash:raise ValueError('Candidate hash mismatch')
 colex=verify_colex.verify(candidate,54,16,4);incidence=verify_incidence.verify(candidate,blocks)
 missing=colex['uncovered_targets']
 if colex['blocks']!=blocks or incidence['uncovered_quadruples']!=missing or incidence['distinct_blocks']!=blocks:raise ValueError('Independent verifier disagreement')
 if expected_holes is not None and missing!=expected_holes:raise ValueError('Unexpected hole count')
 rows=[tuple(sorted(map(int,line.split()))) for line in raw.decode('ascii').splitlines() if line.strip()]
 marked=bytearray(math.comb(54,4));columns=[0]*55
 for i,row in enumerate(rows):
  for q in itertools.combinations(row,4):marked[sum(math.comb(p-1,j) for j,p in enumerate(q,1))]=1
  for p in row:columns[p]|=1<<i
 holes_colex=[];holes_incidence=[]
 for q in itertools.combinations(range(1,55),4):
  if not marked[sum(math.comb(p-1,j) for j,p in enumerate(q,1))]:holes_colex.append(list(q))
  if not columns[q[0]]&columns[q[1]]&columns[q[2]]&columns[q[3]]:holes_incidence.append(list(q))
 if holes_colex!=holes_incidence or len(holes_colex)!=missing:raise ValueError('Independent exact hole lists disagree')
 return {'status':'COMPLETE_COVER_VERIFIED' if missing==0 else 'VERIFIED_PARTIAL_NOT_A_COVER',
         'is_complete_cover':missing==0,'blocks':blocks,'uncovered_quadruples':missing,
         'covered_quadruples':316251-missing,'sha256':digest,'exact_holes':holes_colex,
         'independent_methods_agree':True,'colex':colex,'incidence':incidence}

def verify_packet(check_manifest=False):
 record=json.loads((ROOT/'PARTIAL.json').read_text())
 if record['status']!='NOT_A_COVER' or record['is_complete_cover'] is not False or record['uncovered_quadruples']<=0:raise ValueError('Partial must remain explicitly incomplete')
 result=check(ROOT/record['witness'],record['blocks'],record['sha256'],record['uncovered_quadruples'])
 if result['exact_holes']!=json.loads((ROOT/'EXACT_HOLES.json').read_text()):raise ValueError('Pinned hole list mismatch')
 if check_manifest:
  manifest=json.loads((ROOT/'MANIFEST.json').read_text())
  expected=set(manifest['files']);actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}-{'MANIFEST.json','SHA256SUMS'}
  if actual!=expected:raise ValueError('Packet inventory differs from manifest')
  for name,item in manifest['files'].items():
   raw=(ROOT/name).read_bytes()
   if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:raise ValueError('Packet file hash mismatch: '+name)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check-manifest',action='store_true');a=p.parse_args()
 try:result=verify_packet(a.check_manifest)
 except (OSError,ValueError,KeyError) as error:print(json.dumps({'status':'VERIFICATION_ERROR','error':str(error)}));raise SystemExit(2)
 print(json.dumps(result,indent=2))
