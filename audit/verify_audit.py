"""Portable, fail-closed verification for the 222/223 publication audit.

Run from any directory with Python 3.10+. Standard library only. The meaning
of a complete covering and the semantic proofs remain human review boundaries.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import ast
import copy
import json
import sys

import independent222 as old
import independent223 as new

ROOT=Path(__file__).resolve().parent.parent
# Trusted release inventory is fixed independently of the supplied manifest.
# The manifest excludes itself; SHA256SUMS is one of these 38 hashed files.
EXPECTED_MANIFEST_PATHS=(
    '.gitattributes', 'CITATIONS.md', 'LICENSE', 'README.md', 'REPRODUCE.md', 'SHA256SUMS',
    'audit/ATTRIBUTION.md', 'audit/CHANGELOG.md', 'audit/DEPENDENCIES.md',
    'audit/ENUMERATIONS.md', 'audit/PROOFS.md', 'audit/README.md', 'audit/REVIEW_LIMITS.md',
    'audit/SEMANTIC_CERTIFICATE_223.md', 'audit/SOURCE_PROVENANCE.json',
    'audit/data/scout/POINT_LINK_65_EXACT_UPPER_CERTIFICATE.json',
    'audit/data/scout/POINT_LINK_65_MODEL.json',
    'audit/data/support/SUPPORT_GRAPH_m16.json', 'audit/data/support/SUPPORT_GRAPH_m17.json',
    'audit/data/support/SUPPORT_GRAPH_m18.json', 'audit/data/support/SUPPORT_GRAPH_m19.json',
    'audit/data/support/edges_m16.csv', 'audit/data/support/edges_m17.csv',
    'audit/data/support/edges_m18.csv', 'audit/data/support/edges_m19.csv',
    'audit/independent222.py', 'audit/independent223.py', 'audit/receipts/TEST_RECEIPT.json',
    'audit/run_checks.py', 'audit/verify_audit.py', 'data/certificate.json', 'data/model.json',
    'proofs/LOWER_BOUND_221.md', 'proofs/LOWER_BOUND_222.md', 'requirements.txt',
    'tests/test_audit.py', 'tests/test_verify.py', 'verify.py',
)
PINS={
    'data/model.json':'3f65a5e44b96d0ee5844176331b4b5172ba267f29479e995f3d744d4acca1c24',
    'data/certificate.json':'9483912feec907e2f4b2118d1ebd2d83bcf881602d41ecbdf8d5674e03c0d973',
    'audit/data/scout/POINT_LINK_65_MODEL.json':'3f0a02d0fc5ac86b2c08fec8f17f10d895dfceb9f861480f3e0b3fe110f1707a',
    'audit/data/scout/POINT_LINK_65_EXACT_UPPER_CERTIFICATE.json':'51fc7bee0712da2bb6551be0957262a0e840cc494358edb73eafe8c2ba8fface',
}

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(p):return sha256(p.read_bytes()).hexdigest()

def read(p):
    def unique(pairs):
        result={}
        for k,v in pairs:
            need(k not in result,'duplicate JSON key')
            result[k]=v
        return result
    def reject_constant(value):raise ValueError('nonfinite JSON number')
    return json.loads(p.read_text(encoding='utf-8-sig'),object_pairs_hook=unique,parse_constant=reject_constant)

def check_integer_structure(variables,rows):
    for v in variables:
        need(all(type(v[k]) is int for k in ('lower','upper','objective')),'integer variable coefficients')
    for row in rows:
        need(all(type(x) is int for x in row['coefficients'].values()),'integer row coefficients')
        for k in ('rhs','lower','upper'):
            if k in row:need(row[k] is None or type(row[k]) is int,'integer row bounds')

def direct_floor():
    checked=0
    for a in range(53):
        for e in range(a//2+1):
            edges=[(2*i,2*i+1) for i in range(e)]
            left=Counter({(i,i):3 for i in range(a)})
            right=Counter({(i,i):2 for i in range(a)})
            for i,j in edges:
                left[i,j]+=2
                right[i,i]+=1;right[j,j]+=1;right[i,j]+=2
            for i in range(2*e,a):right[i,i]+=1
            for i in range(a):
                for j in range(i,a):
                    left[i,j]+=1 if i==j else 2
                    right[i,j]+=1 if i==j else 2
            need(left==right,'matching positive-definite polynomial')
            checked+=1
    need(checked==729,'all matching isomorphism types')
    need(all(260-14*b>b for b in range(18)),'all integer sizes below 18')
    need((260+14)//15==18,'rank bound ceiling')
    return dict(matching_isomorphism_types=checked,excluded_integer_sizes=list(range(18)),
                incidence_constant=260,rank_bound='15b>=260',floor=18)

def extended_support_checks():
    receipts=[]
    for m in range(16,20):
        p=ROOT/'audit/data/support'/f'SUPPORT_GRAPH_m{m}.json'
        doc=read(p);vertices=doc['candidate_supports'];cap={16:3,17:1,18:0,19:0}[m]
        need(doc['m']==m and doc['block_positions']==19 and doc['distinguished_point_mask']==(1<<m)-1,'support parameters')
        need(doc['candidate_count']==len(vertices),'support candidate count')
        degrees=Counter();edge_count=0
        for i,a in enumerate(vertices):
            positions=[j for j in range(19) if a['mask']>>j&1]
            need(a['id']==i and a['support_positions']==positions and len(positions)==4,'support positions/id')
            inside=sum(j<m for j in positions)
            need(a['inside_count']==inside and inside in (1,2),'support inside count')
            need(type(a['color']) is int and 0<=a['color']<cap,'supplied color domain')
            for j in range(i+1,len(vertices)):
                b=vertices[j];common=(a['mask']&b['mask']).bit_count()
                if common==1 or (common==2 and inside==1 and b['inside_count']==1):
                    need(a['color']!=b['color'],'supplied proper coloring')
                    edge_count+=1;degrees[i]+=1;degrees[j]+=1
        ids=doc['clique_witness_ids']
        need(len(set(ids))==len(ids)==cap and all(0<=i<len(vertices) for i in ids),'clique ids')
        masks=[vertices[i]['mask'] for i in ids]
        need(masks==doc['clique_witness_masks'],'clique mask receipt')
        for i in range(len(ids)):
            for j in range(i+1,len(ids)):
                need((masks[i]&masks[j]).bit_count()==1,'clique edge')
        need(doc['isolated_ids']==[i for i in range(len(vertices)) if not degrees[i]],'complete isolation list')
        need(doc['maximum_clique_size']==doc['proper_color_count']==cap,'graph bound receipt')
        need(doc['minimum_tight_points_from_incidence']==m-11>cap,'support incidence contradiction')
        need(doc['edge_count']==edge_count,'support edge count')
        need(doc['edge_file']==f'edges_m{m}.csv','edge basename')
        need(digest(p.parent/doc['edge_file'])==doc['edges_sha256'],'edge bytes hash')
        receipts.append(dict(m=m,saved_coloring_checked=True,saved_clique_checked=True,isolated=len(vertices)-len(degrees)))
    return receipts

def corruptions222(model,cert,variables,rows):
    rejected=[]
    def expect(label,operation):
        try:operation()
        except (ValueError,KeyError,IndexError,TypeError):rejected.append(label)
        else:raise ValueError('accepted corruption: '+label)
    fixtures=[('222 omit n16',lambda x:x['variables'].pop(16)),
              ('222 reverse objective',lambda x:x.update(objective_sense='minimize')),
              ('222 change bound',lambda x:x['variables'][0].update(upper=24309)),
              ('222 reverse tight cut',lambda x:x['rows'][9]['coefficients'].update(t4=5)),
              ('222 omit transport row',lambda x:x['rows'].pop())]
    for label,mutate in fixtures:
        x=copy.deepcopy(model);mutate(x);expect(label,lambda:old.check_model(x,variables,rows))
    fixtures=[('222 positive lower-only multiplier',lambda x:x['row_numerators'].__setitem__(9,'1')),
              ('222 zero denominator',lambda x:x.update(denominator='0')),
              ('222 drop multiplier',lambda x:x['row_numerators'].pop()),
              ('222 omit residual',lambda x:x['positive_column_residuals'].pop(next(iter(x['positive_column_residuals'])))),
              ('222 undercharge correction',lambda x:x.update(finite_bound_correction_numerator='0')),
              ('222 alter stated fraction',lambda x:x.update(exact_objective_upper_bound='0'))]
    for label,mutate in fixtures:
        x=copy.deepcopy(cert);mutate(x);expect(label,lambda:old.replay_certificate(x,variables,rows))
    return rejected

def verify_manifest(root=ROOT):
    doc=read(root/'audit/PUBLIC_MANIFEST.json')
    need(type(doc) is dict and type(doc.get('schema')) is int and doc['schema']==1,'manifest schema')
    need(doc['base_commit']=='946f7ee8931ca9a3b64ef3f1c0f4b0a9fe803c35','manifest base')
    need(doc.get('self_excluded')=='audit/PUBLIC_MANIFEST.json','manifest self exclusion')
    need(doc.get('sha256sums_exclusions')==['SHA256SUMS','audit/PUBLIC_MANIFEST.json'],'manifest checksum exclusions')
    files=doc['files'];need(type(files) is list,'manifest entries must be a list')
    need(all(type(x) is dict and set(x)=={'path','bytes','sha256'} for x in files),'manifest entry fields')
    names=[x['path'] for x in files]
    need(all(type(name) is str for name in names),'manifest path type')
    need(len(set(names))==len(names),'manifest duplicate names')
    need(names==list(EXPECTED_MANIFEST_PATHS),'manifest exact canonical inventory')
    for entry in files:
        path=Path(entry['path'])
        need(not path.is_absolute() and '..' not in path.parts and '\\' not in entry['path'],'safe relative manifest path')
        need(type(entry['bytes']) is int and entry['bytes']>=0,'manifest byte size')
        need(type(entry['sha256']) is str and len(entry['sha256'])==64 and all(c in '0123456789abcdef' for c in entry['sha256']),'manifest hash encoding')
        p=root/path
        need(p.is_file() and not p.is_symlink(),'manifest regular file')
        need(p.stat().st_size==entry['bytes'] and digest(p)==entry['sha256'],'manifest file hash: '+entry['path'])
    sums=(root/'SHA256SUMS').read_text(encoding='utf-8').splitlines()
    expected=[e['sha256']+'  '+e['path'] for e in files if e['path']!='SHA256SUMS']
    need(sums==expected,'complete SHA256SUMS list')
    return dict(files_hashed=len(files),exact_expected_inventory=True,manifest_self_excluded=True,
                scope='the 38 canonical declared release paths; generated local output is outside the publication whitelist')

def verify_all():
    for relative,expected in PINS.items():need(digest(ROOT/relative)==expected,'immutable source hash: '+relative)
    m222=read(ROOT/'data/model.json');c222=read(ROOT/'data/certificate.json')
    v222,r222=old.build_model();check_integer_structure(m222['variables'],m222['rows']);old.check_model(m222,v222,r222)
    need(c222['model_sha256']==PINS['data/model.json'],'222 certificate model binding')
    prior=old.replay_certificate(c222,v222,r222);prior['diagnostic_objective']=old.check_diagnostic(m222,v222,r222)
    base=ROOT/'audit/data/scout'
    model=read(base/'POINT_LINK_65_MODEL.json');cert=read(base/'POINT_LINK_65_EXACT_UPPER_CERTIFICATE.json')
    variables,rows=new.build_model();check_integer_structure(model['variables'],model['rows']);new.check_model(model,variables,rows)
    need(cert['model_sha256']==PINS['audit/data/scout/POINT_LINK_65_MODEL.json'],'223 certificate model binding')
    proposed=new.replay_certificate(cert,variables,rows)
    need((proposed['denominator'],proposed['row_bound_sum'],proposed['correction'],proposed['reduced_upper'])==(10**9,-1210499996608,867398,'-121049912921/100000000'),'223 exact pinned arithmetic')
    proposed.update(variables=len(variables),rows=len(rows),coefficient_positions=len(variables)*len(rows))
    scripts=[ROOT/'audit'/p for p in ('independent222.py','independent223.py','verify_audit.py','run_checks.py')]
    for p in scripts:need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(p.read_text(encoding='utf-8')))),'public validation assert forbidden')
    return dict(status='PASS_INTERNAL_AUDIT_WITH_LIMITS',solver_calls=0,
                public222=prior,proposed223=proposed,direct_floor=direct_floor(),
                peta=new.peta_arithmetic(),support=new.support_audit(),saved_graph_checks=extended_support_checks(),
                semantic_fixtures=new.small_fixtures(),
                corruptions_rejected=corruptions222(m222,c222,v222,r222)+new.mutations(model,cert,variables,rows),
                lifting=dict(incidences=54*66,lower_boundary=16*222,upper_boundary=16*223,ceiling=(54*66+15)//16),
                formal_assistant_verification=False,human_expert_acceptance=False,priority_established=False)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check-manifest',action='store_true')
    args=parser.parse_args();result=verify_all()
    if args.check_manifest:result['manifest']=verify_manifest()
    receipt=dict(result,python_version=sys.version.split()[0],optimized=bool(sys.flags.optimize))
    if args.output:
        with args.output.open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))

if __name__=='__main__':main()
