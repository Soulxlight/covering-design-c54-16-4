#!/usr/bin/env python3
"""Verify this portable evidence bundle without running any search."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def read(p):return json.loads(p.read_text())
def hashfile(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(argv):
 p=subprocess.run([sys.executable,'-B',*(['-O'] if sys.flags.optimize else []),*argv],capture_output=True,text=True)
 need(p.returncode in (0,1),'Verifier failed: '+p.stdout+p.stderr);return json.loads(p.stdout)
def full_or_partial(path,blocks,holes,digest):
 common=ROOT/'full/primary/verification';a=run([str(common/'verify_colex.py'),'54','16','4',str(path)]);b=run([str(common/'verify_incidence.py'),str(path),'--expected-blocks',str(blocks)]);need(a['blocks']==blocks and a['sha256']==digest and a['uncovered_targets']==holes,'Colex witness mismatch');need(b['candidate_sha256']==digest and b['blocks']==b['distinct_blocks']==blocks and b['uncovered_quadruples']==holes,'Incidence witness mismatch');return {'blocks':blocks,'holes':holes,'sha256':digest,'is_complete_cover':holes==0}
manifest=read(ROOT/'MANIFEST.json');expected=set(manifest['files']);actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}-{'MANIFEST.json','SHA256SUMS'};need(expected==actual,'Bundle inventory mismatch')
for name,entry in manifest['files'].items():
 p=ROOT/name;need(p.resolve().is_relative_to(ROOT) and p.is_file() and not p.is_symlink(),'Unsafe inventory entry');need(p.stat().st_size==entry['bytes'] and hashfile(p)==entry['sha256'],'Bundle hash mismatch: '+name)
stop=read(ROOT/'evidence/FINAL_STOP_AUDIT.json');need(stop['strictly_exceeds_10800_seconds'] and stop['supervisor_gap_strictly_exceeds_10800_seconds'] and stop['producer_shutdown_barrier_pass'],'Final stop evidence failed')
packet=read(ROOT/'PACKET.json');need(packet['status']=='FINAL_STOPPED_VERIFIED','Unexpected final classification');fulls=[];partials=[]
for r in packet['full_packets']:
 need(hashfile(ROOT/r['packet_directory']/'MANIFEST.json')==r['manifest_sha256'],'Full packet pin mismatch');fulls.append(full_or_partial(ROOT/r['witness'],r['blocks'],0,r['sha256']))
spectra=[]
for r in packet['full_packets']:
 counts=[0]*55
 for line in (ROOT/r['witness']).read_text().splitlines():
  for point in map(int,line.split()):counts[point]+=1
 spectra.append(tuple(sorted(counts[1:])))
need(len(set(spectra))==len(spectra),'Retained full covers do not have distinct point-degree spectra')
for r in packet['incomplete_packets']:
 need(r['holes']>0 and r['is_complete_cover'] is False,'Partial mislabeled as full');folder=ROOT/r['packet_directory'];need(hashfile(folder/'MANIFEST.json')==r['manifest_sha256'],'Partial packet pin mismatch');v=run([str(folder/'verify_partial.py'),'--check-manifest']);need(v['sha256']==r['sha256'] and v['blocks']==r['blocks'] and v['uncovered_quadruples']==r['holes'] and not v['is_complete_cover'],'Partial receipt mismatch');partials.append({'blocks':r['blocks'],'holes':r['holes'],'sha256':r['sha256'],'is_complete_cover':False})
neutral=[];folder=ROOT/'optional_neutral_7'
if folder.exists():
 recipe=read(folder/'RECIPES.json');need(hashfile(folder/'parent.txt')==recipe['parent_sha256'],'Neutral parent pin mismatch');original=[set(map(int,l.split())) for l in (folder/'parent.txt').read_text().splitlines()]
 for r in recipe['checkpoints']:
  rows=[set(x) for x in original]
  for move in r['moves']:
   row=rows[move['row']];need(move['remove'] in row and move['add'] not in row,'Invalid neutral trace');row.remove(move['remove']);row.add(move['add'])
  raw=('\n'.join(' '.join(map(str,sorted(row))) for row in rows)+'\n').encode();path=folder/r['path'];need(raw==path.read_bytes(),'Neutral trace reconstruction mismatch');neutral.append(full_or_partial(path,recipe['blocks'],r['holes'],r['sha256']))
packing=run([str(ROOT/'research/finite_pool_packing/verify.py')]);need(packing['status']=='PASS_EXACT_FINITE_POOL_PACKING' and packing['necessary_alternative_rows']==280 and not packing['proves_infeasibility'],'Finite-pool packing proof failed')
third=run([str(ROOT/'research/third_family_repair_trace/verify.py')]);need(third['status']=='PASS_RECORDED_THIRD_FAMILY_REPAIRS' and not third['is_complete_cover'],'Recorded family repair failed')
print(json.dumps({'pairwise_nonisomorphism_certified_by_distinct_point_degree_spectra':True,'third_family_recorded_repair':third,'finite_pool_packing':packing,'status':'PASS_FINAL_EVIDENCE_BUNDLE','complete_cover_families':fulls,'incomplete_resume_checkpoints':partials,'optional_neutral_checkpoints':neutral,'search_executed':False,'lower_proofs_verified_by_this_bundle':False},indent=2))
