#!/usr/bin/env python3
"""Exact local regeneration of blocks for ordinary C(54,16,4) covers.

Given a full or partial cover, freeze every block outside a neighborhood and
replace its q blocks by q arbitrary 16-subsets. Point-membership variables,
rather than a finite enumerated candidate list, represent replacement blocks.
An optional Johnson-distance bound limits each replacement's changes from its
original block. ALL holes of the frozen remainder are constrained explicitly.
Only a fully independently verified cover is reported as a verified result.
"""
import argparse
import collections
import hashlib
import itertools as it
import json
import math
import os
import random
import sys
import time
from pathlib import Path

import numpy as np
from ortools.sat.python import cp_model


V, K, T = 54, 16, 4
NT = math.comb(V, T)
CHOOSE = np.array([[math.comb(p,j) if p >= j else 0 for p in range(V)]
                   for j in range(1,T+1)], dtype=np.int64)
POSITIONS = np.array(list(it.combinations(range(K), T)), dtype=np.int16)
TARGET_POINTS = None
TARGET_MASKS = None


def rank(tuples):
    result = np.zeros(tuples.shape[:-1], dtype=np.int64)
    for j in range(T):
        result += CHOOSE[j,tuples[...,j]]
    return result


def init_universe():
    global TARGET_POINTS, TARGET_MASKS
    if TARGET_POINTS is not None:
        return
    pts = np.array(list(it.combinations(range(V), T)), dtype=np.int16)
    ranks = rank(pts)
    TARGET_POINTS = np.empty_like(pts)
    TARGET_POINTS[ranks] = pts
    TARGET_MASKS = np.bitwise_or.reduce(np.left_shift(np.uint64(1),TARGET_POINTS.astype(np.uint64)),axis=1)


def load(path):
    rows = [tuple(sorted(int(x)-1 for x in line.split()))
            for line in Path(path).read_text().splitlines() if line.strip()]
    if not rows or any(len(b)!=K or len(set(b))!=K or min(b)<0 or max(b)>=V for b in rows):
        raise ValueError('Malformed input blocks')
    if len(set(rows)) != len(rows):
        raise ValueError('Duplicate input blocks')
    return rows


def write_rows(path, rows):
    text = ''.join(' '.join(str(x+1) for x in b)+'\n' for b in rows)
    tmp = Path(str(path)+'.tmp')
    tmp.write_text(text)
    tmp.replace(path)


def mask(row):
    return sum(1 << int(p) for p in row)


class State:
    def __init__(self, rows):
        self.rows = rows
        self.ids = rank(np.array(rows,dtype=np.int16)[:,POSITIONS])
        self.cov = np.bincount(self.ids.ravel(),minlength=NT)
        self.masks = np.array([mask(row) for row in rows],dtype=np.uint64)
        self.holes = np.flatnonzero(self.cov==0)
        self.private = np.sum(self.cov[self.ids]==1,axis=1)
        self.breaks = np.zeros((len(rows),V),dtype=np.int32)
        for i,ids in enumerate(self.ids):
            pts = TARGET_POINTS[ids[self.cov[ids]==1]]
            self.breaks[i] = np.bincount(pts.ravel(),minlength=V)

    def remove_block(self, i):
        return State([b for j,b in enumerate(self.rows) if j!=i])

    def residual(self, selected):
        cov = self.cov.copy()
        np.subtract.at(cov,self.ids[selected].ravel(),1)
        return np.flatnonzero(cov==0)

    def select(self, size, radius, rng, trial, focus=None):
        n = len(self.rows)
        selected = []
        # Evaluate direct ways to absorb current holes, preferring cheap point
        # removals. The CP model later permits simultaneous multi-point changes.
        scores = np.zeros(n,dtype=float)
        holes = list(self.holes if focus is None else focus)
        rng.shuffle(holes)
        for h in holes[:100]:
            hm = TARGET_MASKS[h]
            overlap = np.bitwise_count(self.masks & hm)
            choices = []
            hp = set(map(int,TARGET_POINTS[h]))
            for i in np.flatnonzero(overlap >= max(1,T-radius)):
                missing = T-int(overlap[i])
                removal = sorted(int(self.breaks[i,p]) for p in self.rows[i] if p not in hp)
                price = sum(removal[:missing])
                value = 1/(1+price)
                scores[i] += value
                choices.append((price*rng.uniform(0.85,1.15),int(i)))
            choices.sort()
            for _,i in choices[:min(2,max(1,size//max(1,len(holes))))]:
                if i not in selected and len(selected)<size:
                    selected.append(i)
        if not selected:
            selected=[int(np.argsort(self.private)[trial%min(30,n)])]
        while len(selected)<size:
            # Add blocks which can absorb targets currently exclusive to the
            # selected region. This creates a repair dependency neighborhood.
            if trial%4==0:
                seed = rng.choice(selected)
                ids=self.ids[seed][self.cov[self.ids[seed]]==1]
                if len(ids):
                    sample=rng.sample(list(ids),min(32,len(ids)))
                    closeness=np.bitwise_count(self.masks[:,None]&TARGET_MASKS[sample][None,:])
                    gain=np.sum(closeness>=3,axis=1)
                else:gain=np.zeros(n)
            else:
                closeness=np.bitwise_count(self.masks[:,None]&self.masks[selected][None,:])
                gain=np.sum(closeness.astype(float)**3,axis=1)/(1+self.private/200)
            gain=np.asarray(gain,dtype=float)
            gain*=np.array([rng.uniform(0.65,1.35) for _ in range(n)])
            gain[selected]=-1
            selected.append(int(np.argmax(gain)))
        return sorted(selected)


def independent_verify(rows):
    if len(set(rows)) != len(rows):
        return {'valid':False,'error':'duplicate blocks'}
    columns=[0]*V
    for i,row in enumerate(rows):
        if len(row)!=K or len(set(row))!=K or min(row)<0 or max(row)>=V:
            return {'valid':False,'error':'illegal block'}
        for p in row:columns[p]|=1<<i
    holes=[]
    counts=collections.Counter()
    for a,b,c,d in it.combinations(range(V),T):
        hit=columns[a]&columns[b]&columns[c]&columns[d]
        counts[hit.bit_count()]+=1
        if not hit and len(holes)<20:holes.append([a+1,b+1,c+1,d+1])
    return {'valid':counts[0]==0,'blocks':len(rows),'targets':NT,
            'uncovered':counts[0],'first_holes':holes,
            'multiplicity_histogram':dict(sorted(counts.items()))}


def solve_neighborhood(state, selected, radius, seconds, seed, outprefix):
    started=time.monotonic()
    residual=state.residual(selected)
    hpts=TARGET_POINTS[residual]
    hmasks=TARGET_MASKS[residual]
    bm=state.masks[selected]
    possible=np.bitwise_count(hmasks[:,None]&bm[None,:])>=T-radius
    q=len(selected)
    required=np.zeros(q,dtype=np.uint64)
    forced_rounds=0
    # Logical closure: a target with one possible owner forces all its points
    # into that block. Capacity and distance bounds can then rule out owners.
    while True:
        counts=possible.sum(axis=1)
        if np.any(counts==0):
            return {'status':'PREINFEASIBLE','reason':'target has no feasible owner',
                    'residual':len(residual),'forced_rounds':forced_rounds,
                    'model_seconds':time.monotonic()-started}
        forced=np.flatnonzero(counts==1)
        new=required.copy()
        for h in forced:
            i=int(np.flatnonzero(possible[h])[0])
            new[i]|=hmasks[h]
        if np.array_equal(new,required):break
        required=new;forced_rounds+=1
        if np.any(np.bitwise_count(required)>K) or np.any(np.bitwise_count(required&~bm)>radius):
            return {'status':'PREINFEASIBLE','reason':'forced points exceed capacity',
                    'residual':len(residual),'forced_rounds':forced_rounds,
                    'model_seconds':time.monotonic()-started}
        unions=hmasks[:,None]|required[None,:]
        possible&=(np.bitwise_count(unions)<=K)&(np.bitwise_count(unions&~bm[None,:])<=radius)
    model=cp_model.CpModel()
    x=[[model.new_bool_var(f'x{i}_{p}') for p in range(V)] for i in range(q)]
    for i,oldindex in enumerate(selected):
        old=set(state.rows[oldindex])
        model.add(sum(x[i])==K)
        model.add(sum(x[i][p] for p in range(V) if p not in old)<=radius)
        for p in range(V):
            model.add_hint(x[i][p],int(p in old))
            if int(required[i])>>p&1:model.add(x[i][p]==1)
    covervars=0
    for h,pts in enumerate(hpts):
        options=[]
        for i in np.flatnonzero(possible[h]):
            if all(int(required[i])>>int(p)&1 for p in pts):
                options=None
                break
            c=model.new_bool_var(f'h{h}_{i}')
            covervars+=1
            model.add_bool_and([x[i][int(p)] for p in pts]).only_enforce_if(c)
            options.append(c)
        if options is not None:model.add_bool_or(options)
    model_elapsed=time.monotonic()-started
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=seconds
    solver.parameters.random_seed=seed
    solver.parameters.cp_model_presolve=True
    status=solver.solve(model)
    receipt={'status':solver.status_name(status),'residual':len(residual),
             'neighborhood_size':q,'radius':radius,'cover_variables':covervars,
             'forced_points':list(map(int,np.bitwise_count(required))),
             'forced_rounds':forced_rounds,'model_seconds':model_elapsed,
             'solve_seconds':solver.wall_time,'branches':solver.num_branches,
             'conflicts':solver.num_conflicts,'selected':selected,'seed':seed}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        replacement=[tuple(p for p in range(V) if solver.value(x[i][p])) for i in range(q)]
        updated=[b for j,b in enumerate(state.rows) if j not in selected]+replacement
        receipt['verification']=independent_verify(updated)
        if not receipt['verification']['valid']:
            write_rows(str(outprefix)+'_INVALID.txt',updated)
            raise RuntimeError('Exact solver result failed independent verification')
        path=Path(str(outprefix)+f'_cover{len(updated)}.txt')
        write_rows(path,updated)
        receipt['output']=str(path)
        receipt['output_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input');p.add_argument('outdir')
    p.add_argument('--seconds',type=float,default=15)
    p.add_argument('--trials',type=int,default=10000)
    p.add_argument('--seed',type=int,default=54001)
    p.add_argument('--sizes',default='4,8,12,16,24,32')
    p.add_argument('--radii',default='2,3,4')
    p.add_argument('--delete',type=int,default=-1,help='delete this block index; -1 picks min-private if full')
    args=p.parse_args()
    init_universe()
    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    state=State(load(args.input))
    inputsha=hashlib.sha256(Path(args.input).read_bytes()).hexdigest()
    dropped=None
    if not len(state.holes):
        dropped=args.delete if args.delete>=0 else int(np.argmin(state.private))
        state=state.remove_block(dropped)
    write_rows(outdir/'input_partial.txt',state.rows)
    header={'input':args.input,'sha256':inputsha,'blocks':len(state.rows),
            'starting_holes':len(state.holes),'deleted_block':dropped}
    print(json.dumps(header),flush=True)
    (outdir/'input_metadata.json').write_text(json.dumps(header,indent=2)+'\n')
    sizes=list(map(int,args.sizes.split(',')));radii=list(map(int,args.radii.split(',')))
    rng=random.Random(args.seed)
    for trial in range(args.trials):
        if (outdir/'STOP').exists():break
        size=sizes[trial%len(sizes)]
        radius=radii[(trial//len(sizes))%len(radii)]
        selected=state.select(size,radius,rng,trial)
        prefix=outdir/f'trial_{trial:06d}'
        result=solve_neighborhood(state,selected,radius,args.seconds,args.seed+trial,prefix)
        result['trial']=trial
        Path(str(prefix)+'.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),flush=True)
        if result.get('output'):
            (outdir/'SUCCESS.json').write_text(json.dumps(result,indent=2)+'\n')
            return


if __name__=='__main__':main()
