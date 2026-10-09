"""Reject malformed complete-release inventories before any math subprocess."""
import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent


def need(ok,message):
    if not ok:
        raise ValueError(message)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    raw=(ROOT/'PUBLIC_MANIFEST.json').read_bytes()
    pristine=json.loads(raw);pin=hashlib.sha256(raw).hexdigest()
    # Importing the pinned release validator does not invoke its main.
    spec=importlib.util.spec_from_file_location('release_inventory',ROOT/'verify_release.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    need(mod.integrity(pin)==len(pristine['files']),'pristine complete inventory')
    rejected=[]
    with tempfile.TemporaryDirectory(prefix='complete-covering-release-') as tmp:
        dst=Path(tmp)/'release';dst.mkdir()
        for name in [e['path'] for e in pristine['files']]+['PUBLIC_MANIFEST.json','PUBLIC_SHA256SUMS']:
            out=dst/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,out)
        mp=dst/'PUBLIC_MANIFEST.json'
        def reject(label,newpin):
            for flags in ([],['-O']):
                p=subprocess.run([sys.executable,'-B',*flags,'verify_release.py','--manifest-sha256',newpin],
                    cwd=dst,capture_output=True,text=True,timeout=30)
                need(p.returncode!=0,'accepted malformed complete inventory')
                reason=p.stderr.strip().splitlines()[-1]
                need(reason.startswith('FAIL_CLOSED:'),'explicit complete-inventory rejection')
                rejected.append(dict(fixture=label,optimized=bool(flags),exit_code=p.returncode,reason=reason))
        reject('wrong independently supplied overall pin','0'*64)
        variants=[('wrong schema',lambda d:d.update(schema='other')),
            ('wrong base',lambda d:d.update(base_commit='0'*40)),
            ('empty whitelist',lambda d:d.update(files=[])),
            ('missing member',lambda d:d['files'].pop()),
            ('extra member',lambda d:d['files'].append(dict(path='other',bytes=0,sha256='0'*64))),
            ('equal-count substitution',lambda d:d['files'][0].update(path='other')),
            ('duplicate member',lambda d:d['files'].__setitem__(-1,d['files'][0].copy())),
            ('traversal alias',lambda d:d['files'][0].update(path='../other')),
            ('absolute alias',lambda d:d['files'][0].update(path='/other')),
            ('boolean size',lambda d:d['files'][0].update(bytes=True)),
            ('negative size',lambda d:d['files'][0].update(bytes=-1)),
            ('bad hash',lambda d:d['files'][0].update(sha256='0'*64))]
        for label,change in variants:
            d=json.loads(raw);change(d);need(d!=pristine,'nonvacuous release fixture')
            altered=json.dumps(d).encode();mp.write_bytes(altered)
            reject(label+' with recomputed fixture pin',hashlib.sha256(altered).hexdigest());mp.write_bytes(raw)
        d=json.dumps(pristine).replace('"schema":','"schema":"duplicate", "schema":',1).encode()
        mp.write_bytes(d);reject('duplicate JSON key with recomputed fixture pin',hashlib.sha256(d).hexdigest());mp.write_bytes(raw)
        (dst/'unreviewed.txt').write_bytes(b'unlisted')
        reject('extra actual release file',pin);(dst/'unreviewed.txt').unlink()
        sums=dst/'PUBLIC_SHA256SUMS';saved=sums.read_bytes();sums.write_bytes(b'')
        reject('empty checksum index',pin);sums.write_bytes(saved)
    need(mod.integrity(pin)==len(pristine['files']),'complete release preserved')
    result=dict(status='PASS_COMPLETE_RELEASE_INVENTORY_CONTROLS',physical_process_rejections=len(rejected),
        manifest_variants=len(variants)+1,rejections=rejected,normal_and_optimized_rejected_all=True,
        independently_recomputed_fixture_pins=True,solver_calls=0,network_calls=0,github_writes=0)
    if args.output:
        with args.output.open('x',encoding='utf-8') as stream:
            stream.write(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rejections'},indent=2))


if __name__=='__main__':
    main()
