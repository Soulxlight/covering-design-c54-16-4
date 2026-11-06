#!/usr/bin/env python3
"""Replay an immutable bounded-defect move trace; no search required."""
import argparse,hashlib,json,pathlib
p=argparse.ArgumentParser();p.add_argument('input_metadata');p.add_argument('result_metadata');p.add_argument('output_directory');p.add_argument('--input');p.add_argument('--dependency');a=p.parse_args()
m=json.loads(pathlib.Path(a.input_metadata).read_text());r=json.loads(pathlib.Path(a.result_metadata).read_text())
inp=pathlib.Path(a.input or m['input_path']);raw=inp.read_bytes();assert hashlib.sha256(raw).hexdigest()==m['input_sha256']
rows=[list(map(int,line.split())) for line in raw.decode().splitlines() if line.strip()]
trace=json.loads(pathlib.Path(a.dependency or r['moves_path']).read_text())
for move in trace:
 row=rows[move['block']];assert move['remove'] in row and move['insert'] not in row;row[row.index(move['remove'])]=move['insert']
rows=list(dict.fromkeys(tuple(sorted(row)) for row in rows))
data=''.join(' '.join(map(str,row))+'\n' for row in rows).encode();assert hashlib.sha256(data).hexdigest()==r['verification']['sha256']
out=pathlib.Path(a.output_directory);out.mkdir(parents=True,exist_ok=True);(out/'replayed.txt').write_bytes(data)
print(json.dumps({'sha256':hashlib.sha256(data).hexdigest(),'path':str(out/'replayed.txt'),'moves':len(trace)}))
