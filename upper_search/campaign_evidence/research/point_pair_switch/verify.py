#!/usr/bin/env python3
"""Reproduce the fixed-parent exclusion for every two-label switching neighborhood."""
from pathlib import Path
import hashlib,json,itertools,subprocess,tempfile,sys
def require(condition,message):
 if not condition:raise RuntimeError(message)
root=Path(__file__).resolve().parent;manifest=json.loads((root/'manifest.json').read_text())
for name,digest in manifest['files'].items():
 if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Digest mismatch: '+name)
sys.path.insert(0,str(root));from model import read_rows,build,reduce
rows=read_rows(root/'input.txt');allq=set(itertools.combinations(range(54),4));covered=set(q for row in rows for q in itertools.combinations(sorted(row),4));holes=sorted(allq-covered)
require(len(rows)==301 and len(holes)==7,'Parent row/deficit count mismatch')
require(all(len(row)==16 and all(0<=x<54 for x in row) for row in rows),'Illegal parent row')
require(len(set(rows))==301,'Repeated parent row')
with tempfile.TemporaryDirectory(prefix='pair-certificate-') as tmp:
 tmp=Path(tmp);binary=tmp/'screen';out=tmp/'fixed.json'
 subprocess.run(['g++','-O3','-std=c++17',str(root/'screen.cpp'),'-o',str(binary)],check=True)
 subprocess.run([str(binary),'54','16',str(root/'input.txt'),str(out)],check=True)
 screen=json.loads(out.read_text())
 expected=json.loads((root/'fixed_screen.json').read_text());require(screen==expected,'Recomputed fixed screen differs from certificate')
 fixed=parity=0
 for p in screen['pairs']:
  if p['fixed_lower_bound']>=7:fixed+=1;continue
  m=build(rows,54,p['a']-1,p['b']-1,holes);require(m['fixed']==p['fixed_lower_bound'] and m['current_holes']==7,'Python/C++ pair model disagreement')
  r=reduce(m,6);require(r['infeasible'],'Pair not excluded for six holes');parity+=1
require(fixed==821 and parity==610 and fixed+parity==1431,'Incomplete pair accounting')
print(json.dumps({'status':'verified','parent_sha256':manifest['parent_sha256'],'current_holes':7,'strict_target':6,'fixed_bound_rejections':fixed,'conditional_parity_rejections':parity,'scope':'For this exact301-row parent, no coordinated a/b switches among rows containing exactly one ofa,b can reach six holes, for any of1431 point pairs. Not a global covering-design lower bound.'},indent=2))
