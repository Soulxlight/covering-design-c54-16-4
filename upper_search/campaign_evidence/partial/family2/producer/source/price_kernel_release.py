#!/usr/bin/env python3
"""Exact one-extra-point release pricing against a grouped-single-row certificate.

The returned completions are legal blocks and potential kernel enlargements,
not coverings. Gross private loss is distinct from final uncovered targets:
other changed rows may rescue a target whose original private owner is lost.
Completions with up to three free points are supported; releasing a fourth
point is skipped explicitly rather than silently truncating its domain.
"""
import argparse
import collections
import hashlib
import itertools as it
import json
from pathlib import Path
import time


def points(mask):
    while mask:
        bit=mask&-mask;yield bit.bit_length()-1;mask-=bit


def completion_scores(keep,targets):
    km=sum(1<<p for p in keep);free=16-len(keep);outside=sorted(set(range(54))-keep)
    if not 1<=free<=3:raise ValueError('Completion pricing requires one to three free points')
    w0=0;w1=[0]*54;w2=collections.defaultdict(int);w3=collections.defaultdict(int)
    for q,w in targets:
        missing=q&~km;n=missing.bit_count()
        if n==0:w0+=w
        elif n==1:w1[missing.bit_length()-1]+=w
        elif n==2 and free>=2:w2[tuple(points(missing))]+=w
        elif n==3 and free>=3:w3[tuple(points(missing))]+=w
    for extra in it.combinations(outside,free):
        score=w0+sum(w1[p] for p in extra)
        if free>=2:score+=sum(w2.get(pair,0) for pair in it.combinations(extra,2))
        if free==3:score+=w3.get(extra,0)
        yield score,km|sum(1<<p for p in extra),extra


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate');p.add_argument('output')
    p.add_argument('--max-free',type=int,choices=[1,2,3],default=3)
    a=p.parse_args();started=time.monotonic();cert=json.loads(Path(a.certificate).read_text());kernel_path=Path(cert['kernel']);kernel=json.loads(kernel_path.read_text())
    if hashlib.sha256(kernel_path.read_bytes()).hexdigest()!=cert['kernel_sha256']:raise ValueError('Kernel hash mismatch')
    parent=Path(kernel['parent']);data=parent.read_bytes()
    if hashlib.sha256(data).hexdigest()!=kernel['parent_sha256']:raise ValueError('Parent hash mismatch')
    if any(len(g)!=1 for g in cert['grouping']):raise ValueError('Pricing requires a certificate with separate capacities for each row')
    rows=[tuple(sorted(int(x)-1 for x in line.split())) for line in data.decode().splitlines() if line.strip()]
    row_masks=[sum(1<<p for p in row) for row in rows];weights=cert['weights'];denominator=cert['denominator']
    targets=[(sum(1<<(p-1) for p in q),w) for q,w in zip(kernel['residual_targets'],weights) if w]
    old_capacity=[0]*len(rows);kept=[set(row) for row in rows]
    for grouping,claimed in zip(cert['grouping'],cert['group_maxima']):
        group=kernel['groups'][grouping[0]];i=group['row'];keep={p-1 for p in group['protected_points']}
        if not 13<=len(keep)<=15:raise ValueError('Existing mutable slots must have one to three free points')
        exact=max(score for score,_,_ in completion_scores(keep,targets))
        if exact!=claimed:raise ValueError('Old row capacity does not match certificate')
        old_capacity[i]=exact;kept[i]=keep
    for i,keep in enumerate(kept):
        if len(keep)==16 and any(row_masks[i]&q==q for q,_ in targets):raise ValueError('Certificate target is already covered by a frozen row')
    incidence=[0]*54
    for i,row in enumerate(rows):
        for p in row:incidence[p]|=1<<i
    private=[[] for _ in rows];losses=[[0]*54 for _ in rows]
    for i,row in enumerate(rows):
        for q in it.combinations(row,4):
            owners=incidence[q[0]]&incidence[q[1]]&incidence[q[2]]&incidence[q[3]]
            if owners==1<<i:
                mask=sum(1<<p for p in q);private[i].append(mask)
                for p in q:losses[i][p]+=1
    positive=[];cases=0;completions=0;skipped=0
    for i,keep in enumerate(kept):
        old_weak=set(rows[i])-keep
        if len(old_weak)+1>a.max_free:
            skipped+=len(keep);continue
        for released in sorted(keep):
            cases+=1;new_keep=keep-{released};km=sum(1<<p for p in new_keep);free=16-len(new_keep)
            best=None
            for score,mask,extra in completion_scores(new_keep,targets):
                completions+=1
                changed=16-(mask&row_masks[i]).bit_count()
                key=(score,-changed,-mask)
                if best is None or key>best[0]:best=(key,mask,extra)
            score=best[0][0]
            if score<=old_capacity[i]:continue
            mask=best[1];extra=best[2];direct=sum(w for q,w in targets if mask&q==q)
            if direct!=score or mask.bit_count()!=16 or mask&km!=km or mask>>released&1:raise RuntimeError('Priced completion failed exact checking')
            removed=row_masks[i]&~mask;gross=sum(bool(q&removed) for q in private[i])
            positive.append({'row':i,'released_point':released+1,'old_weak_points':sorted(p+1 for p in old_weak),
                             'new_weak_points':sorted(p+1 for p in old_weak|{released}),
                             'old_capacity':old_capacity[i],'new_capacity':score,'capacity_gain':score-old_capacity[i],
                             'released_point_private_loss':losses[i][released],'witness_gross_private_loss':gross,
                             'witness_completion':[p+1 for p in points(mask)],'witness_added_points':[p+1 for p in extra],
                             'witness_removed_points':[p+1 for p in points(removed)],
                             'previously_frozen_row':len(keep)==16})
    positive.sort(key=lambda x:(-x['capacity_gain'],x['released_point_private_loss'],x['witness_gross_private_loss'],x['row'],x['released_point']))
    efficient=sorted(positive,key=lambda x:(-x['capacity_gain']/(1+x['released_point_private_loss']),x['witness_gross_private_loss'],x['row'],x['released_point']))[:50]
    result={'parent':str(parent),'parent_sha256':kernel['parent_sha256'],'certificate':str(Path(a.certificate).resolve()),
            'certificate_sha256':hashlib.sha256(Path(a.certificate).read_bytes()).hexdigest(),'kernel':str(kernel_path),
            'denominator':denominator,'weighted_targets':len(targets),'tested_releases':cases,'tested_completions':completions,
            'max_resulting_free_positions':a.max_free,'skipped_releases_above_free_limit':skipped,
            'positive_releases':positive,'positive_count':len(positive),'previously_frozen_positive_count':sum(x['previously_frozen_row'] for x in positive),
            'efficiency_order':[[x['row'],x['released_point']] for x in efficient],
            'indexing':{'row':'zero-based','point':'one-based','capacities':'integer numerator over the common denominator'},
            'elapsed_seconds':time.monotonic()-started,
            'scope':'Certificate-violating kernel releases and legal single-block completions only; no whole-design improvement claim',
            'private_loss_caveat':'Gross loss counts targets lost by their original private owner. Other changed rows can rescue them; this is not a lower bound on final holes.'}
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('positive_releases','efficiency_order')},indent=2))


if __name__=='__main__':main()
