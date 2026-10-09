"""Fail-closed integrity and arithmetic replay of the complete release whitelist."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parent
BASE='946f7ee8931ca9a3b64ef3f1c0f4b0a9fe803c35'
SCOUT_PIN='d5ebe7dba35a94b99675c670616a99c5d669760732b8f3e7cf9a935555a78308'
EXPECTED_PATHS=('.gitattributes', 'CITATIONS.md', 'LICENSE', 'README.md', 'REPRODUCE.md', 'SHA256SUMS', 'audit/ATTRIBUTION.md', 'audit/CHANGELOG.md', 'audit/DEPENDENCIES.md', 'audit/ENUMERATIONS.md', 'audit/PROOFS.md', 'audit/PUBLIC_MANIFEST.json', 'audit/README.md', 'audit/REVIEW_LIMITS.md', 'audit/SEMANTIC_CERTIFICATE_223.md', 'audit/SOURCE_PROVENANCE.json', 'audit/data/scout/POINT_LINK_65_EXACT_UPPER_CERTIFICATE.json', 'audit/data/scout/POINT_LINK_65_MODEL.json', 'audit/data/support/SUPPORT_GRAPH_m16.json', 'audit/data/support/SUPPORT_GRAPH_m17.json', 'audit/data/support/SUPPORT_GRAPH_m18.json', 'audit/data/support/SUPPORT_GRAPH_m19.json', 'audit/data/support/edges_m16.csv', 'audit/data/support/edges_m17.csv', 'audit/data/support/edges_m18.csv', 'audit/data/support/edges_m19.csv', 'audit/independent222.py', 'audit/independent223.py', 'audit/receipts/TEST_RECEIPT.json', 'audit/run_checks.py', 'audit/verify_audit.py', 'audit224/ARITHMETIC_INDEX.json', 'audit224/ASSUMPTION_CODE_MAP.md', 'audit224/CHANGELOG.md', 'audit224/ENUMERATIONS.md', 'audit224/REVIEWER_START.md', 'audit224/SOURCE_PRESERVATION.json', 'audit224/STEP_BY_STEP_224.md', 'audit224/check_release_inventory.py', 'audit224/derive_arithmetic_index.py', 'audit224/package/CASE_LEDGER.json', 'audit224/package/MANIFEST.json', 'audit224/package/PROOF_DEPENDENCIES.json', 'audit224/package/PROVENANCE.json', 'audit224/package/README.md', 'audit224/package/REFERENCES.md', 'audit224/package/REPORT.md', 'audit224/package/audits/reconstruct_1111.py', 'audit224/package/audits/reconstruct_211.py', 'audit224/package/audits/reconstruct_22.py', 'audit224/package/audits/reconstruct_31.py', 'audit224/package/audits/reconstruct_4.py', 'audit224/package/cases/1111/CERTIFICATE.json', 'audit224/package/cases/1111/MODEL.json', 'audit224/package/cases/211/CERTIFICATE.json', 'audit224/package/cases/211/MODEL.json', 'audit224/package/cases/22/CERTIFICATE.json', 'audit224/package/cases/22/MODEL.json', 'audit224/package/cases/31/CERTIFICATE.json', 'audit224/package/cases/31/MODEL.json', 'audit224/package/cases/4/CERTIFICATE.json', 'audit224/package/cases/4/MODEL.json', 'audit224/package/proof/ASSEMBLY.md', 'audit224/package/proof/CASE1111_ENDPOINT.md', 'audit224/package/proof/CASE1111_LINKS.md', 'audit224/package/proof/CASE211.md', 'audit224/package/proof/CASE22.md', 'audit224/package/proof/CASE31.md', 'audit224/package/proof/CASE4.md', 'audit224/package/proof/CHILD_BOUND_66.md', 'audit224/package/proof/COMMON_MODEL.md', 'audit224/package/proof/MULTIPLICITY_PROOF.md', 'audit224/package/proof/PETA_CHILD_SOURCE.md', 'audit224/package/review/CASE1111_NORMAL.json', 'audit224/package/review/CASE1111_OPTIMIZED.json', 'audit224/package/review/CASE211_NORMAL.json', 'audit224/package/review/CASE211_OPTIMIZED.json', 'audit224/package/review/CASE22_NORMAL.json', 'audit224/package/review/CASE22_OPTIMIZED.json', 'audit224/package/review/CASE31_NORMAL.json', 'audit224/package/review/CASE31_OPTIMIZED.json', 'audit224/package/review/CASE4_NORMAL.json', 'audit224/package/review/CASE4_OPTIMIZED.json', 'audit224/package/review/CHILD_STATUS.json', 'audit224/package/review/GLOBAL_NORMAL.json', 'audit224/package/review/GLOBAL_OPTIMIZED.json', 'audit224/package/review/REVIEW_STATUS.md', 'audit224/package/verify.py', 'audit224/prior_art/PUBLISHED_BOUND_EVALUATIONS.json', 'audit224/prior_art/QUERY_LEDGER.json', 'audit224/prior_art/SEARCH_REPORT.md', 'audit224/prior_art/evaluate_published_bounds.py', 'audit224/receipts/COMPLETE_INVENTORY_CONTROLS.json', 'audit224/receipts/LEGACY_COMBINED_REPLAY.json', 'audit224/receipts/ROOT_NORMAL_OPTIMIZED.json', 'audit224/receipts/TEST_RECEIPT.json', 'audit224/run_checks224.py', 'data/certificate.json', 'data/model.json', 'proofs/LOWER_BOUND_221.md', 'proofs/LOWER_BOUND_222.md', 'requirements.txt', 'tests/test_audit.py', 'tests/test_verify.py', 'verify.py', 'verify_release.py')


def need(ok,message):
    if not ok:
        raise ValueError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d


def integrity(pin):
    need(re.fullmatch('[0-9a-f]{64}',pin) is not None,'external SHA256 required')
    need(sha(ROOT/'PUBLIC_MANIFEST.json')==pin,'external public manifest pin')
    doc=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text(encoding='utf-8'),object_pairs_hook=unique)
    need(doc['schema']=='c54-16-4-combined-public-audit-224-v01' and doc['base_commit']==BASE,'release schema/base')
    files=doc['files'];need(type(files) is list,'inventory list')
    need(all(type(e) is dict and set(e)=={'path','bytes','sha256'} for e in files),'exact entry fields')
    names=[e['path'] for e in files]
    need(names==list(EXPECTED_PATHS) and len(names)==len(set(names)),'fixed exact release whitelist')
    actual=[]
    for p in ROOT.rglob('*'):
        relative=p.relative_to(ROOT)
        if relative.parts[0]=='.git':
            continue
        need(not p.is_symlink(),'symlinks forbidden')
        if hasattr(p,'is_junction'):
            need(not p.is_junction(),'junctions forbidden')
        if p.is_file():
            actual.append(relative.as_posix())
    need(set(actual)==set(names)|{'PUBLIC_MANIFEST.json','PUBLIC_SHA256SUMS'},'missing or extra release file')
    for e in files:
        name=e['path'];need(type(name) is str and '\\' not in name and ':' not in name,'portable path')
        pp=PurePosixPath(name)
        need(not pp.is_absolute() and str(pp)==name and all(x not in ('','.','..') for x in pp.parts),'canonical safe path')
        need(type(e['bytes']) is int and e['bytes']>=0,'integer size')
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None,'hash format')
        p=ROOT/name;need(p.is_file() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'release member hash')
    expected=[e['sha256']+'  '+e['path'] for e in files]+[pin+'  PUBLIC_MANIFEST.json']
    need((ROOT/'PUBLIC_SHA256SUMS').read_text(encoding='utf-8').splitlines()==expected,'complete checksum index')
    return len(files)


def child(script,*args):
    flags=['-O'] if sys.flags.optimize else []
    p=subprocess.run([sys.executable,'-B',*flags,script,*args],cwd=ROOT,capture_output=True,text=True,timeout=60)
    need(p.returncode==0,'arithmetic subvalidator failure: '+script)
    return json.loads(p.stdout)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256',required=True)
    args=parser.parse_args();count=integrity(args.manifest_sha256)
    old=child('audit/verify_audit.py','--check-manifest')
    new=child('audit224/package/verify.py','--manifest-sha256',SCOUT_PIN)
    index=child('audit224/derive_arithmetic_index.py')
    prior=child('audit224/prior_art/evaluate_published_bounds.py')
    need(old['status']=='PASS_INTERNAL_AUDIT_WITH_LIMITS' and
         new['status']=='PASS_REPRODUCIBILITY_WITH_SEMANTIC_REVIEW_LIMITS','accepted replay statuses')
    need(old['public222']['reduced_upper']=='-1330103235427/500000000','old222 upper')
    need(new['internally_audited_theorem']=='C(54,16,4)>=224','complete proposed statement')
    print(json.dumps(dict(status='PASS_COMBINED_WHITELIST_AND_EXACT_ARITHMETIC',
        declared_files=count,total_release_files=count+2,optimized=bool(sys.flags.optimize),
        public_base_commit=BASE,public222=old['public222'],proposed223=old['proposed223'],
        proposed224=new,arithmetic_index_status=index['status'],prior_art_formula_status=prior['status'],
        source_integrity_rechecked=integrity(args.manifest_sha256)==count,
        solver_calls=0,network_calls=0,github_writes=0,
        formal_kernel_verified=False,human_expert_accepted=False,priority_certified=False),indent=2,sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except (ValueError,KeyError,TypeError,OSError,json.JSONDecodeError) as error:
        print('FAIL_CLOSED: '+str(error),file=sys.stderr);sys.exit(1)
