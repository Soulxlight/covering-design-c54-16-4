#!/usr/bin/env python3
"""Reconstruct the recorded row changes; this does not rerun the original solver."""
import argparse,hashlib,json,tempfile
from pathlib import Path
from verify_partial import check,verify_packet
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work-dir',type=Path);a=p.parse_args()
verify_packet(True);recipe=json.loads((ROOT/'producer/row_changes.json').read_text())
raw=(ROOT/'producer/direct_input.txt').read_bytes()
if hashlib.sha256(raw).hexdigest()!=recipe['input_sha256']:raise ValueError('Input hash mismatch')
rows=[list(map(int,line.split())) for line in raw.decode('ascii').splitlines() if line.strip()]
if recipe['deleted_block'] is not None:del rows[recipe['deleted_block']]
for change in recipe['changes']:
 i=change['row'];old=set(rows[i])
 if sorted(old)!=change['before']:raise ValueError('Recorded original row mismatch')
 old.difference_update(change['removed']);old.update(change['added'])
 if sorted(old)!=change['after']:raise ValueError('Recorded row change mismatch')
 rows[i]=sorted(old)
out=('\n'.join(' '.join(map(str,sorted(rows[i]))) for i in recipe['output_order'])+'\n').encode()
if hashlib.sha256(out).hexdigest()!=recipe['output_sha256']:raise ValueError('Reconstruction does not match pinned output bytes')
work=a.work_dir.resolve() if a.work_dir else Path(tempfile.mkdtemp(prefix='partial-recorded-reconstruction-'))
if work.is_relative_to(ROOT) or (work.exists() and any(work.iterdir())):raise ValueError('Use a fresh external directory')
work.mkdir(parents=True,exist_ok=True);target=work/'reconstructed_partial.txt';target.write_bytes(out)
receipt=check(target,recipe['output_blocks'],recipe['output_sha256'],recipe['output_holes'])
(work/'RECONSTRUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
