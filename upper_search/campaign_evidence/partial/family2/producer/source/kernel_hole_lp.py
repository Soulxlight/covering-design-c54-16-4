#!/usr/bin/env python3
"""Rational lower certificates for holes in a protected-point choice kernel.

Run export and solve as separate processes: the state exporter imports OR-Tools,
while the LP solver imports highspy, whose bundled libraries must be isolated.
"""
import argparse
import hashlib
import importlib.util
import itertools as it
import json
import math
from pathlib import Path
import sys


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path,data):Path(path).write_text(json.dumps(data,indent=2)+'\n')


def old_free_points(group):
    return group['old_free_points'] if 'old_free_points' in group else [group['old_free_point']]


def added_points(option):
    return option['added_points'] if 'added_points' in option else [option['added_point']]


def completion_patterns(keep,old_free,target_masks):
    """All completion patterns, using the at-most-three missing points per target.

    Old completion is first, retaining it as the representative of its pattern.
    Points and bit positions here are zero based.
    """
    km=sum(1<<p for p in keep);free=len(old_free);required={}
    for h,target in enumerate(target_masks):
        missing=target&~km
        if missing.bit_count()<=free:
            key=tuple(bits(missing));required[key]=required.get(key,0)|(1<<h)
    outside=sorted(set(range(54))-set(keep));patterns={}
    for extra in it.chain([tuple(old_free)],it.combinations(outside,free)):
        pattern=required.get((),0)
        for size in range(1,free+1):
            for subset in it.combinations(extra,size):pattern|=required.get(subset,0)
        patterns.setdefault(pattern,extra)
    return patterns


def export(args):
    import numpy as np
    sys.path.insert(0,str(Path(args.source_dir).resolve()))
    import membership_lns as M
    M.init_universe();state=M.State(M.load(args.parent));selected=[];protected=[];weak=[];explicit=None
    if args.weak_map:
        mapping=json.loads(Path(args.weak_map).read_text())
        if mapping.get('parent_sha256')!=digest(args.parent) or mapping.get('row_index_base')!=0 or mapping.get('point_label_base')!=1:raise ValueError('Explicit weak-map identity/indexing mismatch')
        explicit={int(i):sorted(set(int(p)-1 for p in values)) for i,values in mapping['weak_positions'].items()}
        if any(i<0 or i>=len(state.rows) or not set(values).issubset(state.rows[i]) for i,values in explicit.items()):raise ValueError('Explicit weak point is not in its original row')
    for i,row in enumerate(state.rows):
        removed=explicit.get(i,[]) if explicit is not None else [p for p in row if state.breaks[i,p]<=args.threshold]
        if removed:
            if not 1<=len(removed)<=args.max_free:raise ValueError(f'Row{i} has{len(removed)} free positions; maximum is {args.max_free}')
            selected.append(i);weak.append(removed);protected.append([p for p in row if p not in removed])
    fixed=state.cov.copy()
    if selected:np.subtract.at(fixed,state.ids[selected].ravel(),1)
    for keep in protected:
        np.add.at(fixed,M.rank(np.array(list(it.combinations(keep,4)),dtype=np.int16)),1)
    residual=[int(h) for h in np.flatnonzero(fixed==0)];targets=[list(map(int,M.TARGET_POINTS[h])) for h in residual]
    target_masks=[sum(1<<p for p in q) for q in targets];groups=[]
    for i,keep,old_free in zip(selected,protected,weak):
        patterns=completion_patterns(keep,old_free,target_masks)
        group={'row':i,'protected_points':[p+1 for p in keep],'old_free_points':[p+1 for p in old_free],
               'options':[{'added_points':[p+1 for p in extra],'covered_targets':list(bits(pattern))} for pattern,extra in patterns.items()]}
        if len(old_free)==1:
            group['old_free_point']=old_free[0]+1
            for option in group['options']:option['added_point']=option['added_points'][0]
        groups.append(group)
    result={'parameters':[54,16,4],'parent':str(Path(args.parent).resolve()),'parent_sha256':digest(args.parent),
            'source_state_module':str(Path(M.__file__).resolve()),'source_state_sha256':digest(M.__file__),
            'threshold':args.threshold,'input_holes':len(state.holes),'residual_target_ranks':residual,
            'residual_targets':[[p+1 for p in q] for q in targets],'groups':groups,
            'max_free_positions':args.max_free,
            'scope':'Only this pinned protected-point kernel; all legal completions of every retained subblock are represented'}
    if explicit is not None:
        result['restriction']={'kind':'explicit_weak_map','source_path':str(Path(args.weak_map).resolve()),'source_sha256':digest(args.weak_map),
                               'mapping':{'parent_sha256':digest(args.parent),'row_index_base':0,'point_label_base':1,
                                          'weak_positions':{str(i):[p+1 for p in values] for i,values in sorted(explicit.items()) if values}}}
    else:result['restriction']={'kind':'private_loss_threshold','threshold':args.threshold}
    dump(args.output,result);print(json.dumps({'kernel':args.output,'rows':len(groups),'targets':len(targets),'distinct_options':sum(len(g['options']) for g in groups),'input_holes':len(state.holes)}))


def build_groupings(kernel,size):
    row_masks=[sum(1<<h for h in set(it.chain.from_iterable(o['covered_targets'] for o in g['options']))) for g in kernel['groups']]
    remaining=set(range(len(row_masks)));grouping=[]
    while remaining:
        first=max(remaining,key=lambda i:(sum((row_masks[i]&row_masks[j]).bit_count() for j in remaining if i!=j),-i))
        group=[first];remaining.remove(first);union=row_masks[first]
        while remaining and len(group)<size:
            nextrow=max(remaining,key=lambda i:((union&row_masks[i]).bit_count(),-i));group.append(nextrow);remaining.remove(nextrow);union|=row_masks[nextrow]
        grouping.append(group)
    return grouping


def union_patterns(kernel,group):
    patterns={0}
    for i in group:
        options=[sum(1<<h for h in o['covered_targets']) for o in kernel['groups'][i]['options']]
        patterns={a|b for a in patterns for b in options}
    return sorted(patterns)


def bits(mask):
    while mask:
        low=mask&-mask;yield low.bit_length()-1;mask-=low


def solve(args):
    import highspy
    import numpy as np
    kernel=json.loads(Path(args.kernel).read_text());nh=len(kernel['residual_targets']);grouping=build_groupings(kernel,args.group_size)
    patterns=[union_patterns(kernel,g) for g in grouping];nr=len(patterns);starts=[0];columns=[];values=[]
    for i,choices in enumerate(patterns):
        for mask in choices:
            columns.extend(bits(mask));values.extend([1.0]*mask.bit_count());columns.append(nh+i);values.append(-1.0);starts.append(len(columns))
    high=highspy.Highs();high.setOptionValue('output_flag',False);high.setOptionValue('threads',1);high.setOptionValue('time_limit',args.seconds)
    high.addCols(nh+nr,np.array([-1.0]*nh+[1.0]*nr),np.zeros(nh+nr),np.array([1.0]*nh+[highspy.kHighsInf]*nr),0,np.array([0],dtype=np.int32),np.array([],dtype=np.int32),np.array([],dtype=np.float64))
    high.addRows(len(starts)-1,np.full(len(starts)-1,-highspy.kHighsInf),np.zeros(len(starts)-1),len(columns),np.array(starts,dtype=np.int32),np.array(columns,dtype=np.int32),np.array(values,dtype=np.float64))
    high.run();solution=high.getSolution();scale=args.denominator
    raw=solution.col_value[:nh] if solution.value_valid else [0.0]*nh
    weights=[math.floor(max(0.0,min(1.0,float(w)))*scale) if math.isfinite(float(w)) else 0 for w in raw]
    maxima=[max((sum(weights[h] for h in bits(mask)) for mask in choices),default=0) for choices in patterns]
    numerator=sum(weights)-sum(maxima);bound=max(0,-(-numerator//scale))
    cert={'kernel':str(Path(args.kernel).resolve()),'kernel_sha256':digest(args.kernel),'denominator':scale,
          'weights':weights,'grouping':grouping,'group_maxima':maxima,'numerator':numerator,'hole_lower_bound':bound,
          'lp_status':high.modelStatusToString(high.getModelStatus()),'lp_relaxed_hole_objective':-float(high.getObjectiveValue()),
          'group_option_counts':list(map(len,patterns)),
          'scope':'Exact rational lower bound on holes in this pinned protected-point kernel only; no global covering bound'}
    dump(args.output,cert);print(json.dumps({k:v for k,v in cert.items() if k not in ('weights','grouping','group_maxima')}))


def validated_choice_hint(kernel, supplied=None, kernel_sha256=None):
    """Return exact completion indices and directly recomputed residual holes.

    Explicit hints are pinned to the complete serialized kernel. Computing
    actual target containment here avoids trusting claimed hint objectives or
    coverage metadata when giving the solver an incumbent.
    """
    groups=kernel['groups'];targets=[frozenset(q) for q in kernel['residual_targets']]
    if supplied is not None:
        if supplied.get('kernel_sha256')!=kernel_sha256:raise ValueError('Completion hint/kernel digest mismatch')
        indices=supplied.get('option_indices')
        if not isinstance(indices,list) or len(indices)!=len(groups):raise ValueError('Completion hint needs one option index per group')
    else:
        indices=[next(j for j,option in enumerate(group['options']) if added_points(option)==old_free_points(group)) for group in groups]
    covered=set()
    for group,j in zip(groups,indices):
        if type(j) is not int or not 0<=j<len(group['options']):raise ValueError('Invalid completion hint option index')
        option=group['options'][j];keep=set(group['protected_points']);extra=added_points(option);old=old_free_points(group)
        if len(extra)!=len(old) or len(set(extra))!=len(extra) or keep&set(extra):raise ValueError('Completion hint selects an illegal row completion')
        block=keep|set(extra)
        actual={h for h,target in enumerate(targets) if target<=block}
        advertised=option['covered_targets']
        if any(type(h) is not int or not 0<=h<len(targets) for h in advertised) or len(set(advertised))!=len(advertised) or set(advertised)!=actual:
            raise ValueError('Completion hint option coverage differs from literal target containment')
        covered.update(actual)
    return list(indices),covered,len(targets)-len(covered)


def mip(args):
    import highspy
    import numpy as np
    kernel=json.loads(Path(args.kernel).read_text());groups=kernel['groups'];nh=len(kernel['residual_targets'])
    choices=[];row_columns=[];target_columns=[[] for _ in range(nh)]
    for i,group in enumerate(groups):
        indices=[]
        for option in group['options']:
            c=len(choices);choices.append((i,option));indices.append(c)
            for h in option['covered_targets']:target_columns[h].append(c)
        row_columns.append(indices)
    nc=len(choices);starts=[0];columns=[];values=[];lower=[];upper=[]
    def constraint(ids,lo,hi):
        columns.extend(ids);values.extend([1.0]*len(ids));starts.append(len(columns));lower.append(lo);upper.append(hi)
    for ids in row_columns:constraint(ids,1.0,1.0)
    for h,ids in enumerate(target_columns):constraint(ids+[nc+h],1.0,highspy.kHighsInf)
    if args.allow_holes is not None:constraint(list(range(nc,nc+nh)),-highspy.kHighsInf,float(args.allow_holes))
    high=highspy.Highs();high.setOptionValue('output_flag',False);high.setOptionValue('threads',1);high.setOptionValue('time_limit',args.seconds);high.setOptionValue('mip_rel_gap',0.0)
    high.addCols(nc+nh,np.array([0.0]*nc+[1.0]*nh),np.zeros(nc+nh),np.ones(nc+nh),0,np.array([0],dtype=np.int32),np.array([],dtype=np.int32),np.array([],dtype=np.float64))
    for c in range(nc):high.changeColIntegrality(c,highspy.HighsVarType.kInteger)
    high.addRows(len(lower),np.array(lower),np.array(upper),len(columns),np.array(starts,dtype=np.int32),np.array(columns,dtype=np.int32),np.array(values,dtype=np.float64))
    # Default remains the original completion. An explicit pinned endpoint can
    # provide a better incumbent without changing this kernel's feasible set.
    hint_path=getattr(args,'hint',None)
    supplied=json.loads(Path(hint_path).read_text()) if hint_path else None
    hint_indices,hint_covered,hint_holes=validated_choice_hint(kernel,supplied,digest(args.kernel))
    hint=np.zeros(nc+nh)
    for i,j in enumerate(hint_indices):hint[row_columns[i][j]]=1
    for h in range(nh):hint[nc+h]=int(h not in hint_covered)
    hint_submitted=args.allow_holes is None or hint_holes<=args.allow_holes
    if hint_submitted:
        solution=highspy.HighsSolution();solution.col_value=hint;solution.value_valid=True;high.setSolution(solution)
    high.run();solution=high.getSolution();info=high.getInfo()
    result={'kernel':str(Path(args.kernel).resolve()),'kernel_sha256':digest(args.kernel),'status':high.modelStatusToString(high.getModelStatus()),
            'point_choice_variables':nc,'continuous_hole_variables':nh,'mip_nodes':int(info.mip_node_count),
            'mip_dual_bound':float(info.mip_dual_bound) if math.isfinite(info.mip_dual_bound) else None,
            'mip_gap':float(info.mip_gap) if math.isfinite(info.mip_gap) else None,'allow_holes':args.allow_holes,
            'hint':{'kind':'explicit_completion' if hint_path else 'original_completion','holes':hint_holes,'submitted':hint_submitted,
                    'source_path':str(Path(hint_path).resolve()) if hint_path else None,'source_sha256':digest(hint_path) if hint_path else None},
            'scope':'Only this protected-point completion kernel; candidate coverage requires independent verification'}
    if solution.value_valid:
        x=solution.col_value[:nc]
        if all(abs(v-round(v))<1e-6 for v in x):
            selected=[c for c,v in enumerate(x) if v>0.5]
            if all(sum(c in selected for c in ids)==1 for ids in row_columns):
                parent=[tuple(sorted(map(int,line.split()))) for line in Path(kernel['parent']).read_text().splitlines() if line.strip()]
                covered=set();changed=[]
                for c in selected:
                    i,option=choices[c];group=groups[i];extra=added_points(option);old=old_free_points(group);row=tuple(sorted(group['protected_points']+extra))
                    parent[group['row']]=row;covered.update(option['covered_targets'])
                    if extra!=old:changed.append({'row':group['row'],'removed_points':sorted(set(old)-set(extra)),'added_points':sorted(set(extra)-set(old))})
                missing=nh-len(covered)
                if args.allow_holes is not None and missing>args.allow_holes:raise RuntimeError('Integer MIP assignment violates the requested hole budget')
                parent=list(dict.fromkeys(parent));path=Path(args.output).with_suffix('.cover.txt' if missing==0 else '.partial.txt')
                path.write_text(''.join(' '.join(map(str,row))+'\n' for row in parent))
                spec=importlib.util.spec_from_file_location('strict_cover_verifier','/workspace/solver_survey/verify_cover.py');checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
                checked=checker.verify(path,54,16,4)
                if checked['uncovered_targets']!=missing:raise RuntimeError('Independent MIP coverage verification mismatch')
                result['candidate']={'path':str(path),'changes':changed,'holes':missing,'verification':checked}
                result['objective']=missing
    dump(args.output,result);print(json.dumps(result))


def verify(args):
    cert=json.loads(Path(args.certificate).read_text());kernel=json.loads(Path(cert['kernel']).read_text())
    if digest(cert['kernel'])!=cert['kernel_sha256'] or digest(kernel['parent'])!=kernel['parent_sha256']:raise ValueError('Pinned source hash mismatch')
    rows=[tuple(sorted(map(int,line.split()))) for line in Path(kernel['parent']).read_text().splitlines() if line.strip()]
    if any(len(row)!=16 or len(set(row))!=16 or min(row)<1 or max(row)>54 for row in rows):raise ValueError('Illegal parent row')
    if len(set(rows))!=len(rows) or kernel['parameters']!=[54,16,4]:raise ValueError('Duplicate parent rows or wrong parameters')
    incidence=[0]*55
    for i,row in enumerate(rows):
        for p in row:incidence[p]|=1<<i
    expected={};restriction=kernel.get('restriction',{'kind':'private_loss_threshold'})
    if restriction['kind']=='explicit_weak_map':
        mapping=restriction['mapping']
        if mapping.get('parent_sha256')!=kernel['parent_sha256'] or mapping.get('row_index_base')!=0 or mapping.get('point_label_base')!=1:raise ValueError('Explicit map identity/indexing mismatch')
        for row_index,values in mapping['weak_positions'].items():
            i=int(row_index);weak=set(values)
            if i<0 or i>=len(rows) or not weak.issubset(rows[i]) or len(weak)>kernel.get('max_free_positions',1):raise ValueError('Invalid explicit protected-point restriction')
            if weak:expected[i]=(set(rows[i])-weak,sorted(weak))
    elif restriction['kind']=='private_loss_threshold':
        # Recompute every original private loss independently by incidence.
        threshold=kernel['threshold']
        for i,row in enumerate(rows):
            losses={p:0 for p in row}
            for q in it.combinations(row,4):
                owner=incidence[q[0]]&incidence[q[1]]&incidence[q[2]]&incidence[q[3]]
                if owner==1<<i:
                    for p in q:losses[p]+=1
            weak=[p for p in row if losses[p]<=threshold]
            if weak:
                if len(weak)>kernel.get('max_free_positions',1):raise ValueError('Kernel exceeds its free-point limit')
                expected[i]=(set(row)-set(weak),sorted(weak))
    else:raise ValueError('Unknown protected-kernel restriction')
    if len(expected)!=len(kernel['groups']) or set(expected)!=set(g['row'] for g in kernel['groups']):raise ValueError('Affected-row selection mismatch')
    frozen=list(rows)
    for group in kernel['groups']:
        if (set(group['protected_points']),old_free_points(group))!=expected[group['row']]:raise ValueError('Protected-point mismatch')
        frozen[group['row']]=tuple(group['protected_points'])
    fixed_incidence=[0]*55
    for i,row in enumerate(frozen):
        for p in row:fixed_incidence[p]|=1<<i
    residual=[q for q in it.combinations(range(1,55),4) if not fixed_incidence[q[0]]&fixed_incidence[q[1]]&fixed_incidence[q[2]]&fixed_incidence[q[3]]]
    if len(residual)!=len(kernel['residual_targets']) or set(residual)!=set(map(tuple,kernel['residual_targets'])):raise ValueError('Residual target family mismatch')
    targets=list(map(set,kernel['residual_targets']))
    for group in kernel['groups']:
        keep=set(group['protected_points']);free=len(old_free_points(group));outside=set(range(1,55))-keep
        # Independently transpose the target-to-completion relation: extend
        # each target's missing point set to every legal full completion.
        completion_cover={extra:0 for extra in it.combinations(sorted(outside),free)}
        for h,target in enumerate(targets):
            required=target-keep
            if len(required)>free:continue
            for filler in it.combinations(sorted(outside-required),free-len(required)):
                extra=tuple(sorted(required|set(filler)));completion_cover[extra]|=1<<h
        expected_patterns={tuple(bits(pattern)) for pattern in completion_cover.values()}
        recorded={tuple(o['covered_targets']) for o in group['options']}
        if recorded!=expected_patterns:raise ValueError('Omitted or incorrect legal addition coverage pattern')
        for option in group['options']:
            extra=added_points(option)
            if len(extra)!=free or len(set(extra))!=free or not set(extra).issubset(outside):raise ValueError('Illegal representative completion')
            if tuple(option['covered_targets'])!=tuple(h for h,target in enumerate(targets) if target.issubset(keep|set(extra))):raise ValueError('Representative completion has incorrect coverage')
    denominator=cert['denominator'];weights=cert['weights']
    if not isinstance(denominator,int) or denominator<=0 or len(weights)!=len(targets) or any(not isinstance(w,int) or not 0<=w<=denominator for w in weights):raise ValueError('Invalid rational target weights')
    partition=list(it.chain.from_iterable(cert['grouping']))
    if sorted(partition)!=list(range(len(kernel['groups']))):raise ValueError('Row groups are not a partition')
    maxima=[max(sum(weights[h] for h in bits(mask)) for mask in union_patterns(kernel,g)) for g in cert['grouping']]
    numerator=sum(weights)-sum(maxima);bound=max(0,-(-numerator//denominator))
    if maxima!=cert['group_maxima'] or numerator!=cert['numerator'] or bound!=cert['hole_lower_bound']:raise ValueError('Exact certificate arithmetic mismatch')
    print(json.dumps({'valid':True,'hole_lower_bound':bound,'numerator':numerator,'denominator':denominator,'rows':len(expected),'residual_targets':len(targets),'scope':cert['scope']}))


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    e=sub.add_parser('export');e.add_argument('parent');e.add_argument('threshold',type=int);e.add_argument('output');e.add_argument('--source-dir',required=True);e.add_argument('--weak-map',help='Complete explicit weak-position map; overrides the threshold selection');e.add_argument('--max-free',type=int,choices=[1,2,3],default=3)
    s=sub.add_parser('solve');s.add_argument('kernel');s.add_argument('output');s.add_argument('--seconds',type=float,default=2);s.add_argument('--denominator',type=int,default=1000000);s.add_argument('--group-size',type=int,choices=[1,2,3],default=1)
    m=sub.add_parser('mip');m.add_argument('kernel');m.add_argument('output');m.add_argument('--seconds',type=float,default=15);m.add_argument('--allow-holes',type=int);m.add_argument('--hint',help='JSON with kernel_sha256 and one option_indices entry per group; ignored as an incumbent if it exceeds --allow-holes')
    v=sub.add_parser('verify');v.add_argument('certificate');args=p.parse_args()
    if args.command=='export':export(args)
    elif args.command=='solve':solve(args)
    elif args.command=='mip':mip(args)
    else:verify(args)


if __name__=='__main__':main()
