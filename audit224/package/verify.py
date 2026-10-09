"""Offline exact replay of the internally reviewed 224 argument.

This checker verifies integrity, reconstruction, and arithmetic. The included
universal mathematical maps remain internally reviewed ordinary proofs.
"""
import argparse
import ast
import copy
import hashlib
import importlib.util
import itertools
import json
import re
import sys
from collections import Counter
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
EXPECTED = {
 '4': ([4], 1875, 276, '-571108487517/1250000000',
       'b8ec40994ccdd45af8b02e84f87537750ebffcc0e524c090a8733f3b060a1573',
       'a45934ca637409c705e3308bb66780ad4d975b285d60ca2a7e07b9412f559c9a'),
 '31': ([3,1], 2404, 318, '-142277733302693/500000000000',
        'bea28e679c0b4f4c36309ccc4302e78e81830a622c1b0e14bb62848d2953eb2a',
        'b2f8f1cf267d7b3d26c8d9e3098b6b6ac7c57684c0c76ecca2f0df9512748125'),
 '22': ([2,2], 2402, 319, '-132999957096373/1000000000000',
        '8908e73d0b75ee5f7f1acac5c98c0cbff5489f6128a97cfb73fc44e90da1abd8',
        'dd183351d67a8c5443cb9a18f7f1fa1d44640ff69f7f5de48c3c70087100639b'),
 '211': ([2,1,1], 2867, 348, '-30987510834737/250000000000',
         '53bfcddc844c6deeb37c33c892167857610f7e1a3b45fd02df33f8c533eb3a94',
         'b1216be346dd322b2f8320c14bca291c22d1dc8fc96da86868af521381363f6d'),
 '1111': ([1,1,1,1], 2840, 358, '-1665576420999/500000000000',
          '4be1d6e6c1b92e3bb1f2f2d2a03d0ef5527dd9f2acb77634eb3a94f867398812',
          '5492c628058b440dd54bb7252fad26f6da172fef75200ec8ea532b3af92f29cc')}
DAG = {
 'definition': [], 'direct_floor18': ['definition'],
 'tight_geometry': ['definition'], 'occurrence_moments': ['definition'],
 'avoidance18_19': ['definition','tight_geometry'],
 'child66': ['definition','direct_floor18','tight_geometry','occurrence_moments','avoidance18_19'],
 'target_point_floor66': ['definition','child66'],
 'five_partitions': ['target_point_floor66'],
 'all_case_maps': ['definition','direct_floor18','tight_geometry','occurrence_moments','avoidance18_19','five_partitions'],
 'all_case_signed_duals': ['all_case_maps'], 'no223': ['all_case_signed_duals'],
 'padding': ['definition'], 'target224': ['no223','padding']}
PROOFS = [
 'proof/CHILD_BOUND_66.md','proof/PETA_CHILD_SOURCE.md','proof/COMMON_MODEL.md',
 'proof/MULTIPLICITY_PROOF.md','proof/CASE1111_LINKS.md','proof/CASE1111_ENDPOINT.md',
 'proof/CASE4.md','proof/CASE31.md','proof/CASE22.md','proof/CASE211.md','proof/ASSEMBLY.md']

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def read(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)

def integer(value):
    need(type(value) is str and re.fullmatch(r'0|-?[1-9][0-9]*', value) is not None,
         'noncanonical integer string')
    return int(value)

def relative(name):
    need(type(name) is str and '\\' not in name, 'portable relative path')
    p = PurePosixPath(name)
    need(not p.is_absolute() and all(x not in ('', '.', '..') for x in p.parts)
         and str(p)==name and ':' not in name, 'unsafe relative path')
    return p

def check_manifest(doc, base=ROOT):
    need(doc['schema']=='c54-16-4-lower-bound-224-package-v01', 'manifest schema')
    entries=doc['files']; need(type(entries) is list, 'manifest file list')
    names=[e['path'] for e in entries]
    need(len(names)==len(set(names)) and 'MANIFEST.json' not in names, 'unique exact whitelist')
    actual=[]
    for p in base.rglob('*'):
        need(not p.is_symlink(), 'symlink forbidden')
        if p.is_file(): actual.append(p.relative_to(base).as_posix())
    need(set(actual)==set(names)|{'MANIFEST.json'}, 'missing or extra package file')
    for e in entries:
        relative(e['path']); p=base/e['path']
        need(type(e['bytes']) is int and e['bytes']>=0, 'exact file size')
        need(p.is_file() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'], 'file integrity')
    return len(entries)

def partitions(n, cap):
    if n==0:
        yield []
    else:
        for head in range(min(n,cap),0,-1):
            for tail in partitions(n-head,head): yield [head]+tail

def profile(part):
    c=Counter([66]*(54-len(part))+[66+d for d in part])
    return ','.join(f'{r}^{n}' for r,n in sorted(c.items()))

def check_ledger(doc):
    rows=doc['cases']; tags=[r['tag'] for r in rows]
    need(len(tags)==5 and set(tags)==set(EXPECTED), 'exactly five distinct cases')
    need(doc['child_floor']==66 and doc['blocks']==223 and doc['point_excess']==4, 'child and incidence premise')
    for r in rows:
        part,nv,nr,upper,mh,ch=EXPECTED[r['tag']]
        need(r['partition']==part and r['profile']==profile(part), 'case profile')
        need(r['variables']==nv and r['rows']==nr and F(r['upper'])==F(upper)<0, 'dimensions and strict upper')
        need(r['model_sha256']==mh and r['certificate_sha256']==ch, 'frozen case pins')
        need(r['scoped_review']=='PASSWITHLIMITS', 'completed scoped review')
    need(sorted(partitions(4,4))==sorted(v[0] for v in EXPECTED.values()), 'full partition exhaustion')

def check_dependencies(doc):
    dag=doc['dependency_dag']; visiting=set(); done=set()
    def visit(n):
        need(n in dag, 'undeclared dependency')
        need(n not in visiting, 'dependency cycle')
        if n in done: return
        visiting.add(n)
        for dep in dag[n]: visit(dep)
        visiting.remove(n); done.add(n)
    for n in dag: visit(n)
    need(dag==DAG, 'complete reviewed dependency graph')
    need(doc['required_proof_assets']==PROOFS, 'complete proof assets')
    for name in PROOFS: need((ROOT/name).is_file(), 'missing mathematical proof asset')
    need(doc['child_lower_bound']==66 and doc['scope']=='complete indexed uniform covering', 'universal child scope')
    need(doc['formal_kernel_verified'] is False and doc['human_expert_accepted'] is False
         and doc['novelty_certified'] is False, 'accurate review limits')
    return sorted(done)

def reconstruction(tag):
    path=ROOT/f'audits/reconstruct_{tag}.py'
    tree=ast.parse(path.read_text(encoding='utf-8'))
    for n in ast.walk(tree):
        if isinstance(n,(ast.Import,ast.ImportFrom)):
            names=[n.module] if isinstance(n,ast.ImportFrom) else [a.name for a in n.names]
            need(all(x in ('itertools','math','collections','fractions') for x in names), 'offline reconstruction imports')
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):
            need(n.func.id not in ('open','exec','eval','compile','__import__'), 'reconstruction side effects')
    spec=importlib.util.spec_from_file_location('reconstruct_'+tag,path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def check_model(m, mod, tag):
    part,nv,nr,upper,mh,ch=EXPECTED[tag]
    V,R=m['variables'],m['rows']
    need(len(V)==nv and len(R)==nr, 'complete model dimensions')
    need(len({v['name'] for v in V})==nv and len({r['label'] for r in R})==nr, 'unique variables and rows')
    for v in V:
        need(all(type(v[k]) is int for k in ('lower','upper','objective')), 'integer finite variable domain')
        need(v['lower']==0 and v['upper']>=0, 'nonnegative finite domain')
    for r in R:
        need(type(r['lower']) is int and (r['upper'] is None or type(r['upper']) is int), 'integer row endpoints')
        need(r['upper'] is None or r['lower']<=r['upper'], 'ordered row endpoints')
        need(all(type(a) is int for a in r['coefficients'].values()), 'integer coefficients')
    need({v['name']:v['objective'] for v in V if v['objective']}=={n:-1 for n in ('z3p','z3m','z4p','z4m')}, 'actual zero-defect objective')
    need(any(v['name']=='n16' for v in V), 'equal whole-block intersection retained')
    need(m['parameters']==[54,16,4,223] and m['partition']==part, 'complete target parameters')
    mod.validate(m)

def replay(m,c,mod,tag,modelhash):
    check_model(m,mod,tag)
    need(c['model_sha256']==modelhash, 'certificate matrix binding')
    D=integer(c['denominator']); need(D>0, 'positive certificate scale')
    weights=c['row_numerators']; need(type(weights) is list and len(weights)==len(m['rows']), 'all row multipliers')
    col={v['name']:0 for v in m['variables']}; rhs=0
    for raw,r in zip(weights,m['rows']):
        w=integer(raw)
        endpoint=r['upper'] if w>0 else r['lower']
        need(endpoint is not None, 'finite signed endpoint')
        rhs+=w*endpoint
        for name,a in r['coefficients'].items():
            need(name in col, 'known coefficient variable'); col[name]+=w*a
    residual={v['name']:D*v['objective']-col[v['name']] for v in m['variables']}
    positive={n:str(a) for n,a in residual.items() if a>0}
    need(positive==c['positive_column_residuals'], 'all positive residuals')
    correction=sum(max(0,residual[v['name']])*v['upper'] for v in m['variables'])
    need(rhs==integer(c['row_bound_sum_numerator']), 'exact row endpoint sum')
    need(correction==integer(c['finite_bound_correction_numerator']), 'every positive residual corrected')
    upper=F(rhs+correction,D)
    need(upper==F(c['exact_objective_upper_bound'])==F(EXPECTED[tag][3]) and upper<0, 'strict exact case upper')
    return {'upper':str(upper),'denominator':D,'row_sum':rhs,'finite_correction':correction,
            'positive_residual_columns':len(positive),'variables':len(m['variables']),
            'rows':len(m['rows']),'coefficient_positions':len(m['variables'])*len(m['rows'])}

def child_arithmetic():
    # These are calculations within the included analytic proof, not a formal
    # proof of the rank/avoidance maps themselves.
    checks=0
    f=lambda m:F(comb(m,2)-52*int(m==4))
    for m in range(4,19):
        need(f(m)<=11*m-45-45*int(m==4), 'r18 chord'); checks+=1
    for m in range(4,16):
        need(f(m)<=F(19*m-75,2), 'r19 chord'); checks+=1
    for d in range(2,22):
        r=18+d
        for m in range(4,r+1):
            need(f(m)<=F((r+4)*m-5*r,2), 'remaining child chord'); checks+=1
        need(-1404-60*d+d*d<=-1764+289*d, 'complete child envelope'); checks+=1
    for b in (18,19):
        for m in range(16,b+1):
            avoid=b-m; required=255-14*b+m
            maximum=0 if avoid<=1 else 1 if avoid==2 else 3
            need(required>maximum, 'avoidance domain contradiction'); checks+=1
    contradictions={str(b):42*comb(b,2)-1764*53+289*(15*b-954) for b in (64,65)}
    need(contradictions=={'64':-7086,'65':-63}, 'child exact contradiction')
    need(15*17<260<=15*18, 'direct rank floor substitution')
    need(16*222<54*66<=16*223 and 223*16-54*66==4, 'target incidence boundary')
    return {'integer_checks':checks,'contradictions':contradictions,'semantic_proofs_formalized':False}

def padding_toys():
    n,k=5,4; pool=list(itertools.combinations(range(n),k)); checks=0; families=0
    for b in range(1,5):
        for ids in itertools.combinations_with_replacement(range(len(pool)),b):
            blocks=[set(pool[i]) for i in ids]; B0=blocks[0]; families+=1
            old=Counter(len(a&z) for a,z in itertools.combinations(blocks,2))
            for p in range(1,4):
                padded=blocks+[B0]*p
                new=Counter(len(a&z) for a,z in itertools.combinations(padded,2))
                prediction=old.copy()
                for a in blocks: prediction[len(a&B0)]+=p
                prediction[k]+=comb(p,2)
                need(new==prediction, 'repeated occurrence histogram increment')
                for j in range(1,5):
                    ss=list(itertools.combinations(range(n),j))
                    d={t:sum(set(t)<=a for a in blocks) for t in ss}
                    dp={t:sum(set(t)<=a for a in padded) for t in ss}
                    increment=p*sum(d[t] for t in ss if set(t)<=B0)+comb(p,2)*comb(k,j)
                    need(all(dp[t]==d[t]+p*int(set(t)<=B0) for t in ss), 'subset padding increment')
                    need(sum(comb(dp[t],2)-comb(d[t],2) for t in ss)==increment, 'degree padding moment')
                    need(sum((new[s]-old[s])*comb(s,j) for s in range(k+1))==increment, 'intersection padding moment')
                    checks+=1
    return {'families':families,'moment_contexts':checks}

def rejection_controls(ledger,deps,models,manifest):
    rejected=[]
    def bad(name,call):
        try: call()
        except ValueError: rejected.append(name)
        else: raise ValueError('failed corruption control: '+name)
    for tag,(m,c,mod,mh) in models.items():
        def changed(name,change):
            mm,cc=copy.deepcopy(m),copy.deepcopy(c); change(mm,cc)
            bad(tag+': '+name,lambda:replay(mm,cc,mod,tag,mh))
        changed('omitted n16',lambda m,c:m['variables'].__delitem__(16))
        changed('changed coefficient',lambda m,c:m['rows'][0]['coefficients'].update(n0=2))
        changed('wrong profile',lambda m,c:m.update(partition=[5]))
        changed('missing multiplier',lambda m,c:c['row_numerators'].pop())
        changed('omitted residual correction',lambda m,c:c.update(finite_bound_correction_numerator='0'))
        changed('wrong model binding',lambda m,c:c.update(model_sha256='0'*64))
        changed('boolean domain',lambda m,c:m['variables'][0].update(upper=True))
        i=next(i for i,r in enumerate(m['rows']) if r['upper'] is None)
        changed('invalid positive lower-only weight',lambda m,c:c['row_numerators'].__setitem__(i,'1'))
    x=copy.deepcopy(ledger); x['cases'].pop(); bad('omitted case',lambda:check_ledger(x))
    x=copy.deepcopy(ledger); x['cases'][-1]=copy.deepcopy(x['cases'][0]); bad('duplicate case',lambda:check_ledger(x))
    x=copy.deepcopy(ledger); x['child_floor']=65; bad('wrong child premise',lambda:check_ledger(x))
    x=copy.deepcopy(deps); x['dependency_dag']['child66'].append('target224'); bad('child-target cycle',lambda:check_dependencies(x))
    x=copy.deepcopy(deps); x['dependency_dag']['child66'].append('undeclared'); bad('undeclared dependency',lambda:check_dependencies(x))
    x=copy.deepcopy(deps); x['required_proof_assets'].pop(); bad('missing proof obligation',lambda:check_dependencies(x))
    bad('duplicate JSON key',lambda:json.loads('{"x":1,"x":2}',object_pairs_hook=unique))
    bad('path traversal',lambda:relative('../private'))
    bad('absolute path',lambda:relative('/private'))
    x=copy.deepcopy(manifest); x['files'].pop(); bad('missing manifest entry',lambda:check_manifest(x))
    x=copy.deepcopy(manifest); x['files'][0]['sha256']='0'*64; bad('altered file pin',lambda:check_manifest(x))
    return rejected

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest-sha256',required=True)
    a=p.parse_args()
    need(re.fullmatch(r'[0-9a-f]{64}',a.manifest_sha256) is not None, 'external SHA-256 required')
    need(sha(ROOT/'MANIFEST.json')==a.manifest_sha256, 'external manifest pin')
    manifest=read(ROOT/'MANIFEST.json'); count=check_manifest(manifest)
    ledger=read(ROOT/'CASE_LEDGER.json'); check_ledger(ledger)
    deps=read(ROOT/'PROOF_DEPENDENCIES.json'); acyclic=check_dependencies(deps)
    source=read(ROOT/'PROVENANCE.json')
    need(source['scope']=='mathematical source attribution; private metadata omitted', 'provenance scope')
    for entry in source['assets']:
        relative(entry['package_path'])
        need(sha(ROOT/entry['package_path'])==entry['packaged_sha256'], 'attributed asset binding')
    result={}; models={}; assignments=0
    for tag,(part,nv,nr,upper,mh,ch) in EXPECTED.items():
        mp=ROOT/f'cases/{tag}/MODEL.json'; cp=mp.with_name('CERTIFICATE.json')
        need(sha(mp)==mh and sha(cp)==ch, 'unchanged frozen model and certificate')
        m,c=read(mp),read(cp); mod=reconstruction(tag)
        result[tag]=replay(m,c,mod,tag,mh); models[tag]=(m,c,mod,mh)
        number=factorial(54)//factorial(54-len(part))
        for repeat in Counter(part).values(): number//=factorial(repeat)
        result[tag]['labelled_profiles']=number; assignments+=number
        for mode in ('normal','optimized'):
            hist=read(ROOT/f'review/CASE{tag}_{mode.upper()}.json')
            need(hist['status']=='PASSWITHLIMITS', 'reviewed case status')
            old=hist['certificate']; need(F(old.get('upper',old.get('exact_upper')))==F(upper), 'historical review exact upper')
    need(assignments==comb(57,4)==395010, 'complete labelled excess vectors')
    historical=read(ROOT/'review/GLOBAL_NORMAL.json')
    need(historical['status']=='PASSWITHLIMITS' and historical['internally_audited_theorem']=='C(54,16,4)>=224', 'completed global review')
    child=read(ROOT/'review/CHILD_STATUS.json')
    need(child['child_lower_bound_proved']==66 and child['status']=='PASSWITHLIMITS', 'completed child review')
    childcalc=child_arithmetic(); padding=padding_toys()
    controls=rejection_controls(ledger,deps,models,manifest)
    need(check_manifest(manifest)==count, 'package preserved during verification')
    print(json.dumps({'status':'PASS_REPRODUCIBILITY_WITH_SEMANTIC_REVIEW_LIMITS',
          'internally_audited_theorem':'C(54,16,4)>=224','package_files':count,
          'cases':result,'labelled_profiles':assignments,'child_arithmetic':childcalc,
          'padding':padding,'acyclic_dependencies':acyclic,'corruption_rejections':controls,
          'solver_calls':0,'network_calls':0,'package_writes':0,'formal_kernel_verification':False,
          'human_expert_acceptance':False,'novelty_certification':False,'optimized':not __debug__},indent=2,sort_keys=True))

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,TypeError,OSError,json.JSONDecodeError) as e:
        print('FAIL_CLOSED: '+str(e),file=sys.stderr); sys.exit(1)
