"""Run portable normal/-O parity and fail-closed corruption checks.

Outputs contain relative command descriptions and content hashes only.
"""
from hashlib import sha256
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent.parent

def need(ok,message):
    if not ok:raise ValueError(message)

def run(args,cwd=ROOT,success=True):
    proc=subprocess.run([sys.executable,'-B',*args],cwd=cwd,capture_output=True,text=True,timeout=30)
    need((proc.returncode==0)==success,'unexpected process result: '+' '.join(args))
    return proc

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    parser.add_argument('--check-manifest',action='store_true');args=parser.parse_args()
    runs=[];math=[]
    for flags in ([],['-O']):
        command=flags+['audit/verify_audit.py']+(['--check-manifest'] if args.check_manifest else [])
        p=run(command);result=json.loads(p.stdout)
        result.pop('optimized');result.pop('python_version')
        math.append(result)
        runs.append(dict(command=['python','-B',*command],exit_code=p.returncode,
                         stdout_sha256=sha256(p.stdout.encode()).hexdigest(),mathematical_receipt=result))
        p=run(flags+['-m','unittest','discover','-s','tests','-v'])
        lines=p.stderr.strip().splitlines()
        need(lines[-1]=='OK','unittest result')
        runs.append(dict(command=['python','-B',*flags,'-m','unittest','discover','-s','tests','-v'],
                         exit_code=p.returncode,test_output=lines,
                         stderr_sha256=sha256(p.stderr.encode()).hexdigest()))
        p=run(flags+['verify.py'])
        need(json.loads(p.stdout)['exact_F_upper']=='-1330103235427/500000000','unchanged public verifier')
        runs.append(dict(command=['python','-B',*flags,'verify.py'],exit_code=0,stdout_sha256=sha256(p.stdout.encode()).hexdigest()))
    need(math[0]==math[1],'normal/optimized mathematical parity')
    corrupt=[]
    fixtures=[('222 model',Path('data/model.json')),('222 certificate',Path('data/certificate.json')),
              ('223 model',Path('audit/data/scout/POINT_LINK_65_MODEL.json')),
              ('223 certificate',Path('audit/data/scout/POINT_LINK_65_EXACT_UPPER_CERTIFICATE.json'))]
    with tempfile.TemporaryDirectory(prefix='covering-audit-') as temporary:
        target=Path(temporary)/'packet'
        # Copy the fixed release whitelist, never Git state or unrelated output.
        import verify_audit as audit
        for name in (*audit.EXPECTED_MANIFEST_PATHS,'audit/PUBLIC_MANIFEST.json'):
            dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
        for label,relative in fixtures:
            path=target/relative;original=path.read_bytes();path.write_bytes(original+b' ')
            for flags in ([],['-O']):
                p=run(flags+['audit/verify_audit.py'],cwd=target,success=False)
                reason=p.stderr.strip().splitlines()[-1]
                need('immutable source hash:' in reason,'corrupt-file rejection reason')
                corrupt.append(dict(fixture=label,optimized=bool(flags),exit_code=p.returncode,reason=reason))
            path.write_bytes(original)
        support=target/'audit/data/support/edges_m16.csv'
        original=support.read_bytes();support.write_bytes(original.replace(b'0,125\n',b'0,124\n',1))
        need(support.read_bytes()!=original,'edge mutation applied')
        for flags in ([],['-O']):
            p=run(flags+['audit/verify_audit.py'],cwd=target,success=False)
            reason=p.stderr.strip().splitlines()[-1]
            need('entire edge list' in reason,'edge corruption semantic rejection')
            corrupt.append(dict(fixture='support edge',optimized=bool(flags),exit_code=p.returncode,reason=reason))
        support.write_bytes(original)
        manifest=target/'audit/PUBLIC_MANIFEST.json';checksum=target/'SHA256SUMS'
        pristine_manifest=manifest.read_bytes();pristine_checksum=checksum.read_bytes()
        manifest_cases=[('empty manifest and empty checksums',lambda d:d.update(files=[])),
                        ('missing manifest entry',lambda d:d['files'].pop()),
                        ('unexpected manifest entry',lambda d:d['files'].append(dict(path='unexpected.txt',bytes=0,sha256='0'*64))),
                        ('equal-count unexpected substitution',lambda d:d['files'][-1].update(path='unexpected.txt')),
                        ('aliased manifest path',lambda d:d['files'][-1].update(path='./verify.py')),
                        ('case-aliased manifest path',lambda d:d['files'][-1].update(path='VERIFY.py')),
                        ('duplicate manifest entry',lambda d:d['files'].__setitem__(-1,d['files'][0].copy()))]
        for label,mutate in manifest_cases:
            doc=json.loads(pristine_manifest);mutate(doc)
            manifest.write_text(json.dumps(doc),encoding='utf-8')
            if not doc['files']:checksum.write_bytes(b'')
            for flags in ([],['-O']):
                p=run(flags+['audit/verify_audit.py','--check-manifest'],cwd=target,success=False)
                reason=p.stderr.strip().splitlines()[-1]
                need('manifest exact canonical inventory' in reason or 'manifest duplicate names' in reason,'manifest rejection reason')
                corrupt.append(dict(fixture=label,optimized=bool(flags),exit_code=p.returncode,reason=reason))
            manifest.write_bytes(pristine_manifest);checksum.write_bytes(pristine_checksum)
    receipt=dict(status='PASS_ALL_PUBLIC_CHECKS',python_version=sys.version.split()[0],
                 normal_optimized_math_identical=True,solver_calls=0,process_timeout_seconds=30,
                 source_file_mutation_tests=len(corrupt),structural_mutations_per_mode=len(math[0]['corruptions_rejected']),
                 manifest_inventory_cases_per_mode=len(manifest_cases),manifest_inventory_process_rejections=2*len(manifest_cases),
                 runs=runs,corrupt_file_rejections=corrupt)
    if args.output:
        with args.output.open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))

if __name__=='__main__':main()
