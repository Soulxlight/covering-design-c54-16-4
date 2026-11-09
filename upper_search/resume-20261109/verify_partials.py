#!/usr/bin/env python3
"""Verify incomplete restart seeds by literal subsets and point intersections."""
from pathlib import Path
import hashlib,itertools,json
ROOT=Path(__file__).resolve().parent
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    manifest=json.loads((ROOT/'PARTIALS.json').read_text());need(manifest['parameters']==[54,16,4],'parameters')
    results=[];universe=set(itertools.combinations(range(1,55),4))
    for record in manifest['partials']:
        path=ROOT/record['path'];raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==record['sha256'],'hash')
        rows=[tuple(map(int,line.split()))for line in raw.decode('ascii').splitlines()if line.strip()]
        need(len(rows)==len(set(rows))==296,'distinct block count')
        need(all(len(r)==16 and r==tuple(sorted(set(r)))and 1<=min(r)<=max(r)<=54 for r in rows),'row legality')
        covered={q for row in rows for q in itertools.combinations(row,4)};literal=sorted(universe-covered)
        incidence=[0]*55
        for i,row in enumerate(rows):
            for point in row:incidence[point]|=1<<i
        intersections=[q for q in sorted(universe)if not(incidence[q[0]]&incidence[q[1]]&incidence[q[2]]&incidence[q[3]])]
        need(literal==intersections==[tuple(q)for q in record['holes']]and len(literal)==2,'exact holes')
        need(record['valid_cover']is False and record['status']=='NOT_A_COVER','partial classification')
        results.append({'path':record['path'],'sha256':record['sha256'],'blocks':296,'covered_targets':316249,'holes':literal,'valid_cover':False})
    print(json.dumps({'status':'PASS_DUAL_VERIFIED_PARTIALS_NOT_COVERS','partials':results},indent=2))
if __name__=='__main__':main()
