"""Run unchanged 224 verifier in both modes and reject physical corruptions."""
import argparse
import ast
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT/'package'
PIN='d5ebe7dba35a94b99675c670616a99c5d669760732b8f3e7cf9a935555a78308'


def need(ok,message):
    if not ok:
        raise ValueError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(base,flags,pin=PIN,success=True):
    p=subprocess.run([sys.executable,'-B',*flags,'verify.py','--manifest-sha256',pin],
                     cwd=base,capture_output=True,text=True,timeout=60)
    need((p.returncode==0)==success,'unexpected verifier exit')
    return p


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    receipts=[]; math=[]; rejected=[]
    for p in [PACKAGE/'verify.py',*sorted((PACKAGE/'audits').glob('*.py')),Path(__file__)]:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text(encoding='utf-8')))),
             'validation assertions forbidden')
    need(sha(PACKAGE/'MANIFEST.json')==PIN,'original scout manifest')
    for flags in ([],['-O']):
        p=run(PACKAGE,flags)
        d=json.loads(p.stdout); d.pop('optimized'); math.append(d)
        receipts.append(dict(command=['python','-B',*flags,'audit224/package/verify.py','--manifest-sha256',PIN],
            exit_code=p.returncode,stdout_sha256=hashlib.sha256(p.stdout.encode()).hexdigest(),mathematics=d))
    need(math[0]==math[1], 'normal/optimized exact parity')
    with tempfile.TemporaryDirectory(prefix='covering224-check-') as tmp:
        target=Path(tmp)/'packet'; shutil.copytree(PACKAGE,target)
        def reject(label,pin=PIN):
            for flags in ([],['-O']):
                p=run(target,flags,pin,False)
                lines=p.stderr.strip().splitlines()
                need(lines and lines[-1].startswith('FAIL_CLOSED:'),'explicit fail-closed diagnostic')
                rejected.append(dict(fixture=label,optimized=bool(flags),exit_code=p.returncode,reason=lines[-1]))
        reject('wrong independently supplied manifest pin','0'*64)
        for tag in ('4','31','22','211','1111'):
            for name in ('MODEL.json','CERTIFICATE.json'):
                p=target/f'cases/{tag}/{name}'; raw=p.read_bytes();p.write_bytes(raw+b' ')
                reject('changed frozen '+tag+'/'+name);p.write_bytes(raw)
        p=target/'PROOF_DEPENDENCIES.json';raw=p.read_bytes();p.unlink()
        reject('missing proof dependency file');p.write_bytes(raw)
        p=target/'unlisted.txt';p.write_bytes(b'unreviewed');reject('extra unlisted file');p.unlink()
        mp=target/'MANIFEST.json'; raw=mp.read_bytes()
        pristine=json.loads(raw)
        variants=[
          ('wrong schema',lambda d:d.update(schema='other')),
          ('empty inventory',lambda d:d.update(files=[])),
          ('omitted member',lambda d:d['files'].pop()),
          ('unexpected member',lambda d:d['files'].append(dict(path='other',bytes=0,sha256='0'*64))),
          ('equal-count substitution',lambda d:d['files'][-1].update(path='other')),
          ('duplicate member',lambda d:d['files'].__setitem__(-1,d['files'][0].copy())),
          ('self inclusion',lambda d:d['files'].append(dict(path='MANIFEST.json',bytes=0,sha256='0'*64))),
          ('dot alias',lambda d:d['files'][0].update(path='./'+d['files'][0]['path'])),
          ('case alias',lambda d:d['files'][0].update(path=d['files'][0]['path'].upper())),
          ('traversal name',lambda d:d['files'][0].update(path='../other')),
          ('absolute name',lambda d:d['files'][0].update(path='/other')),
          ('Windows separator alias',lambda d:d['files'][0].update(path=d['files'][0]['path'].replace('/','\\'))),
          ('boolean byte size',lambda d:d['files'][0].update(bytes=True)),
          ('negative byte size',lambda d:d['files'][0].update(bytes=-1)),
          ('altered member pin',lambda d:d['files'][0].update(sha256='0'*64))]
        for label,change in variants:
            d=json.loads(raw);change(d)
            need(d!=pristine,'nonvacuous manifest mutation '+label)
            mp.write_text(json.dumps(d),encoding='utf-8')
            reject(label+' with recomputed external fixture pin',sha(mp));mp.write_bytes(raw)
        d=json.loads(raw)
        text=json.dumps(d);text=text.replace('"schema":','"schema":"duplicate", "schema":',1)
        mp.write_text(text,encoding='utf-8')
        reject('duplicate JSON manifest key with recomputed external fixture pin',sha(mp));mp.write_bytes(raw)
        need(sha(mp)==PIN,'temp manifest restored')
    result=dict(status='PASS_NORMAL_OPTIMIZED_AND_PHYSICAL_CORRUPTION_CONTROLS',
        python_version=sys.version.split()[0],normal_optimized_math_identical=True,
        mathematical_in_memory_rejections_per_mode=len(math[0]['corruption_rejections']),
        physical_process_rejections=len(rejected),inventory_variants=len(variants)+1,
        symlink_creation_test='not exercised; Windows privilege changes not requested',
        runs=receipts,rejections=rejected,solver_calls=0,network_calls=0,github_writes=0,
        formal_kernel_verification=False,human_expert_acceptance=False,priority_certification=False)
    if args.output:
        with args.output.open('x',encoding='utf-8') as stream:
            stream.write(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('runs','rejections')},indent=2))


if __name__=='__main__':
    main()
