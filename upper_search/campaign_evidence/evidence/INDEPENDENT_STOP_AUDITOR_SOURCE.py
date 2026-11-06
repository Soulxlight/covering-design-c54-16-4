#!/usr/bin/env python3
"""Independent exhaustive witness audit and per-block-count partial statistics."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import tempfile
import time

ROOT = Path('/workspace/cover_search/independent_long')
CAMPAIGN = Path('/workspace/cover_search/campaign')
PROJECT = Path('/workspace/covering-design-c54-16-4')
BASELINE_UTC = '2026-11-06T13:16:33+00:00'
EXPECTED_BASELINE_HASH = '1a6fc9eda36010fade6996b371ffb8b30f0bff1b9054d1ea6f6c74544211f364'


def utc():
    return datetime.now(timezone.utc).isoformat()


def parse_utc(value):
    value = value.replace('Z', '+00:00').replace(' UTC', '+00:00')
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError('Timezone missing from UTC time')
    return result.astimezone(timezone.utc)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def atomic_write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def write_json(path, obj):
    atomic_write(path, (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode())


def append_json(path, obj):
    with path.open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(obj, sort_keys=True) + '\n')
        stream.flush()
        os.fsync(stream.fileno())


def stable_read(path):
    # Even legacy direct writes must produce identical bytes and stat signatures
    # twice before the captured bytes are accepted; all captured bytes are then
    # validated and copied atomically before a consumer may use them.
    previous = path.stat()
    raw = path.read_bytes()
    middle = path.stat()
    again = path.read_bytes()
    final = path.stat()
    stamp = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
    if not (stamp(previous) == stamp(middle) == stamp(final) and raw == again
            and len(raw) == final.st_size and raw.endswith(b'\n')):
        raise ValueError('Unstable or unfinished file: ' + str(path))
    return raw


def verify(raw):
    rows = [tuple(map(int, line.split())) for line in raw.decode('ascii').splitlines()]
    if not rows or len(rows) > 335:
        raise ValueError('Unexpected row count')
    normalized = []
    columns = [0] * 55
    for index, row in enumerate(rows):
        if len(row) != 16 or len(set(row)) != 16 or min(row) < 1 or max(row) > 54:
            raise ValueError('Illegal row ' + str(index + 1))
        normalized.append(tuple(sorted(row)))
        for point in row:
            columns[point] |= 1 << index
    histogram = Counter()
    holes = []
    for a, b, c, d in itertools.combinations(range(1, 55), 4):
        multiplicity = (columns[a] & columns[b] & columns[c] & columns[d]).bit_count()
        histogram[multiplicity] += 1
        if multiplicity == 0:
            holes.append([a, b, c, d])
    distinct = len(set(normalized))
    return {
        'method': 'Independent point-incidence integer bitset intersections',
        'parameters': [54, 16, 4], 'blocks': len(rows), 'distinct_blocks': distinct,
        'all_blocks_legal': True, 'quadruples_checked': sum(histogram.values()),
        'covered_quadruples': sum(histogram.values()) - len(holes),
        'uncovered_quadruples': len(holes), 'holes': holes,
        'coverage_multiplicity_histogram': dict(sorted(histogram.items())),
        'total_coverage_incidence': sum(m * n for m, n in histogram.items()),
        'sha256': sha(raw), 'bytes': len(raw),
        'complete_cover': not holes and distinct == len(rows),
    }


def load_state():
    path = ROOT / 'state.json'
    if path.exists():
        return json.loads(path.read_text())
    return {'best_blocks': 335, 'last_improvement_utc': BASELINE_UTC,
            'partial_records': {}, 'best_seen_hashes': [], 'stop_audited_signature': None}


def audit_best(state, path, expected_blocks, expected_hash, event_utc, baseline=False):
    raw = stable_read(path)
    if sha(raw) != expected_hash:
        raise ValueError('Declared best witness SHA256 mismatch: ' + str(path))
    if expected_hash in state['best_seen_hashes']:
        if expected_blocks == state['best_blocks'] and parse_utc(event_utc) <= parse_utc(state['last_improvement_utc']) and expected_hash != state.get('best_sha256'):
            append_json(ROOT / 'clock_reconciliations.jsonl', {'audit_utc': utc(), 'event':'earliest_verified_witness_pin_reconciled', 'blocks':expected_blocks, 'previous_sha256':state.get('best_sha256'), 'sha256':expected_hash, 'verified_utc':event_utc})
            state['best_sha256']=expected_hash
            state['best_path']=str(ROOT/'full'/f'cover-{expected_blocks}-{expected_hash}.txt')
        if expected_blocks == state['best_blocks'] and parse_utc(event_utc) < parse_utc(state['last_improvement_utc']):
            append_json(ROOT / 'clock_reconciliations.jsonl', {'audit_utc': utc(), 'blocks': expected_blocks, 'previous_utc': state['last_improvement_utc'], 'earlier_verified_utc': event_utc, 'sha256': expected_hash})
            state['last_improvement_utc'] = event_utc
        return
    report = verify(raw)
    if not (report['complete_cover'] and report['blocks'] == expected_blocks
            and report['quadruples_checked'] == 316251):
        raise ValueError('Declared best is not the claimed complete cover: ' + str(path))
    stamp = utc()
    event_time = parse_utc(event_utc)
    if event_time > parse_utc(stamp):
        raise ValueError('Improvement timestamp lies in the future')
    snapshot = ROOT / 'full' / f'cover-{expected_blocks}-{expected_hash}.txt'
    atomic_write(snapshot, raw)
    report.update({'source_path': str(path), 'snapshot': str(snapshot),
                   'audit_utc': stamp, 'improvement_utc': event_utc,
                   'event': 'baseline' if baseline else 'verified_cover'})
    write_json(snapshot.with_suffix('.json'), report)
    state['best_seen_hashes'].append(expected_hash)
    if expected_blocks < state['best_blocks']:
        report['previous_best_blocks'] = state['best_blocks']
        state['best_blocks'] = expected_blocks
        state['best_path'] = str(snapshot)
        state['best_sha256'] = expected_hash
        state['last_improvement_utc'] = BASELINE_UTC if baseline else event_utc
        append_json(ROOT / 'improvements.jsonl', report)
        print(json.dumps({'event': report['event'], 'blocks': expected_blocks,
                          'sha256': expected_hash, 'audit_utc': stamp,
                          'improvement_utc': state['last_improvement_utc']}), flush=True)
    elif expected_blocks == state['best_blocks'] and event_time < parse_utc(state['last_improvement_utc']):
        append_json(ROOT / 'clock_reconciliations.jsonl', {'audit_utc': stamp, 'blocks': expected_blocks, 'previous_utc': state['last_improvement_utc'], 'earlier_verified_utc': event_utc, 'sha256': expected_hash})
        state['last_improvement_utc'] = event_utc


def audit_partial(state, worker):
    directory = Path(worker['directory'])
    path = directory / 'best_partial.txt'
    archived = worker.get('partial_path')
    archive_hash = worker.get('partial_sha256')
    seen_archives = state.setdefault('partial_archive_hashes', [])
    if archived and archive_hash and archive_hash not in seen_archives:
        archive_path = Path(archived)
        archived_raw = stable_read(archive_path)
        if sha(archived_raw) != archive_hash:
            raise ValueError('Hash-pinned archived partial changed: ' + str(archive_path))
        archived_report = verify(archived_raw)
        if (archived_report['blocks'] != worker['partial_blocks']
                or archived_report['uncovered_quadruples'] != worker['partial_uncovered']):
            raise ValueError('Hash-pinned archived partial declared counts incorrect: ' + str(archive_path))
        archived_report.update({'audit_utc': utc(), 'source_path': str(archive_path)})
        write_json(ROOT / 'archive_checks' / (archive_hash + '.json'), archived_report)
        seen_archives.append(archive_hash)
    if not path.exists():
        return None
    # Read the earlier log first. For a fixed target a saved current partial
    # cannot have more holes than a best already reported before capture.
    log_path = directory / 'run.log'
    log = log_path.read_text(errors='replace') if log_path.exists() else ''
    events = list(re.finditer(r'(?:BEST b=(\d+) uncovered=(\d+)|PROGRESS b=(\d+) best=(\d+))', log))
    last_log = None
    if events:
        values = events[-1].groups()
        last_log = [int(values[0] or values[2]), int(values[1] or values[3])]
    raw = stable_read(path)
    source_hash = sha(raw)
    key = str(path)
    old = state['partial_records'].get(key)
    if old and old['sha256'] == source_hash:
        return old
    report = verify(raw)
    count, holes = report['blocks'], report['uncovered_quadruples']
    warnings = []
    if old and old['blocks'] == count and holes > old['uncovered_quadruples']:
        warnings.append('Same-target saved partial regressed in actual hole count')
    if last_log and last_log[0] == count and holes > last_log[1]:
        warnings.append('Partial has more holes than the earlier same-target log best')
    declared_blocks = worker.get('partial_blocks')
    declared_holes = worker.get('partial_uncovered')
    declared_hash = worker.get('partial_sha256')
    exact_status_match = declared_hash == source_hash
    if exact_status_match and (declared_blocks != count or declared_holes != holes):
        warnings.append('Hash-pinned status partial counts are incorrect')
    snapshot = ROOT / 'partial' / f'{directory.name}-b{count}-h{holes}-{source_hash}.txt'
    atomic_write(snapshot, raw)
    report.update({'audit_utc': utc(), 'source_path': str(path), 'snapshot': str(snapshot),
                   'worker': directory.name, 'earlier_log_best': last_log,
                   'declared_blocks': declared_blocks, 'declared_holes': declared_holes,
                   'declared_hash_matches': exact_status_match, 'warnings': warnings})
    write_json(snapshot.with_suffix('.json'), report)
    compact = {k: report[k] for k in ['blocks', 'uncovered_quadruples', 'sha256', 'snapshot', 'audit_utc', 'warnings']}
    state['partial_records'][key] = compact
    append_json(ROOT / 'partial_ledger.jsonl', dict(compact, source_path=key, worker=directory.name))
    if warnings:
        print(json.dumps({'event': 'PARTIAL_WARNING', 'path': key, 'warnings': warnings}), flush=True)
    return compact


def audit_archived_partials(state, status):
    seen = state.setdefault('partial_archive_hashes', [])
    records = []
    for domain in ('partial_archive','secondary_final_archive'):
        archived = status.get(domain,{})
        archived = archived.values() if isinstance(archived,dict) else archived
        records.extend((domain,record) for record in archived)
    for domain,record in records:
        expected_hash = record['sha256']
        if expected_hash in seen:
            continue
        source = Path(record['path'])
        raw = stable_read(source)
        if sha(raw) != expected_hash:
            raise ValueError('Archived partial hash mismatch: ' + str(source))
        report = verify(raw)
        if (report['blocks'] != record['blocks']
                or report['uncovered_quadruples'] != record['uncovered_targets']):
            raise ValueError('Archived partial count mismatch: ' + str(source))
        snapshot = ROOT / 'partial' / f'archive-b{report["blocks"]}-h{report["uncovered_quadruples"]}-{expected_hash}.txt'
        atomic_write(snapshot, raw)
        report.update({'audit_utc': utc(), 'source_path': str(source),
                       'snapshot': str(snapshot), 'provenance': record.get('provenance'),
                       'archive_domain': domain, 'warnings': []})
        write_json(ROOT / 'archive_checks' / (expected_hash + '.json'), report)
        write_json(snapshot.with_suffix('.json'), report)
        compact = {k:report[k] for k in ['blocks', 'uncovered_quadruples', 'sha256', 'snapshot', 'audit_utc', 'warnings']}
        append_json(ROOT / 'partial_ledger.jsonl', dict(compact, source_path=str(source), worker=domain))
        seen.append(expected_hash)


def audit_partial_pool(state, status):
    """Track intersection holes in independently checked equal-best partials."""
    archive=status.get('partial_archive',{}) if status else {}
    records=archive.values() if isinstance(archive,dict) else archive
    target=state['best_blocks']-1
    records=[record for record in records if record['blocks']==target]
    if not records:
        return None
    minimum=min(record['uncovered_targets'] for record in records)
    chosen=[record for record in records if record['uncovered_targets']==minimum]
    holes=[];hashes=[];pending=[]
    for record in chosen:
        path=ROOT/'archive_checks'/(record['sha256']+'.json')
        if not path.exists():
            pending.append(record['sha256']);continue
        report=json.loads(path.read_text())
        if report['sha256']!=record['sha256'] or report['uncovered_quadruples']!=minimum:
            raise ValueError('Independent pool receipt mismatch')
        holes.append({tuple(hole) for hole in report['holes']});hashes.append(record['sha256'])
    common=sorted(set.intersection(*holes)) if holes else None
    result={'target_blocks':target,'minimum_uncovered':minimum,'independently_checked_snapshots':len(hashes),
            'snapshot_sha256s':sorted(hashes),'pending_hashes':pending,
            'common_uncovered_quadruples':common,
            'scope':'Intersection of holes in the selected immutable parent witnesses; not a fixed-size cover.'}
    signature=json.dumps([target,minimum,common])
    if signature!=state.get('partial_pool_signature'):
        event={'event':'PARTIAL_POOL_CHANGE','utc':utc(),**result}
        append_json(ROOT/'pool_changes.jsonl',event)
        print(json.dumps({k:v for k,v in event.items() if k not in ['snapshot_sha256s','scope']}),flush=True)
        state['partial_pool_signature']=signature
    write_json(ROOT/'partial_pool_status.json',result)
    return result


def audit_shutdown_barrier(state, status):
    """Observe final producer quiescence independently of the elapsed clock."""
    live=[]
    for worker in status.get('workers',[]):
        pid=worker.get('pid')
        try:
            command=(Path('/proc')/str(pid)/'cmdline').read_bytes().split(b'\0')
        except FileNotFoundError:
            continue
        expected=(worker.get('argv') or [''])[0]
        if command and command[0] and command[0].decode()==expected:
            live.append({'run_id':worker.get('run_id'),'pid':pid,'executable':expected})
    control=CAMPAIGN.parent/'exact_long'
    request=status.get('quiescence_request') or {}
    ack=status.get('quiescence_acknowledgment') or {}
    try:
        disk_request=json.loads(stable_read(control/'QUIESCE_REQUEST.json'))
        disk_ack=json.loads(stable_read(control/'QUIESCED.json'))
        exact_status=json.loads(stable_read(control/'campaign_v5/status.json'))
    except (OSError,ValueError):
        disk_request={};disk_ack={};exact_status={}
    request_id=request.get('request_id')
    matching=bool(request_id) and all(record.get('request_id')==request_id
                                    for record in [ack,disk_request,disk_ack])
    # A graceful exact controller first acknowledges quiescence, then writes a
    # stronger terminal record which deliberately omits the request identifier.
    # Bind that terminal record to both durable acknowledgments and actual dead
    # processes; never fabricate or rewrite an intermediate quiesced state.
    processes={}
    for proc in Path('/proc').iterdir():
        if not proc.name.isdigit():continue
        try:
            fields=(proc/'stat').read_text().rsplit(')',1)[1].split()
            argv=[x.decode(errors='replace') for x in (proc/'cmdline').read_bytes().split(b'\0') if x]
            processes[int(proc.name)]={'pid':int(proc.name),'state':fields[0],'ppid':int(fields[1]),'argv':argv}
        except (OSError,IndexError,ValueError):continue
    exact_pid=exact_status.get('pid');seen={exact_pid} if type(exact_pid)is int else set()
    while True:
        added={pid for pid,record in processes.items() if record['ppid'] in seen}-seen
        if not added:break
        seen.update(added)
    active_descendants=[record for pid,record in processes.items() if pid in seen and record['state'] not in ('Z','X')]
    active_exact_namespace=[record for record in processes.values() if record['state'] not in ('Z','X') and any(arg.startswith(str(control)+'/') for arg in record['argv'])]
    pid_matches=type(exact_pid)is int and all(record.get('pid')==exact_pid for record in [ack,disk_ack])
    completed_matches=type(exact_status.get('completed'))is int and all(record.get('completed_jobs')==exact_status['completed'] for record in [ack,disk_ack])
    try: terminal_time_matches=all(parse_utc(exact_status['utc'])>=parse_utc(record['utc']) for record in [ack,disk_ack])
    except (KeyError,TypeError,ValueError):terminal_time_matches=False
    terminal_pass=(exact_status.get('status')=='stopped' and matching and pid_matches and completed_matches and terminal_time_matches and not active_descendants and not active_exact_namespace)
    quiesced_pass=exact_status.get('status')=='quiesced' and exact_status.get('request_id')==request_id
    flags=all(record.get(key) is True for record in [ack,disk_ack]
              for key in ['no_active_solver','all_candidate_tickets_committed','no_auxiliary_lease'])
    processed=set(status.get('processed_inbox',[]))
    pending=sorted(str(path) for path in (CAMPAIGN/'inbox').glob('*.json') if str(path) not in processed)
    full_archive=status.get('full_archive',{})
    full_records=full_archive.values() if isinstance(full_archive,dict) else full_archive
    unaudited=[record['sha256'] for record in full_records if record['sha256'] not in state['best_seen_hashes']]
    observed={'campaign_status_is_stopped':status.get('status')=='stopped',
              'live_wls_processes':live,'unprocessed_inbox_tickets':pending,
              'unaudited_archived_full_hashes':unaudited,
              'exact_request_id':request_id,'exact_request_ack_ids_match':matching,
              'exact_quiescence_flags_all_true':flags,
              'exact_status_is_quiesced':quiesced_pass,
              'exact_terminal_stopped_binding_pass':terminal_pass,
              'exact_terminal_pid':exact_pid,'exact_terminal_process_state':processes.get(exact_pid,{}).get('state','absent'),
              'exact_active_supervisor_or_descendants':active_descendants,
              'exact_active_namespace_processes':active_exact_namespace,
              'exact_completed_jobs_match_both_acks':completed_matches,
              'exact_terminal_timestamp_after_both_acks':terminal_time_matches,
              'exact_controller_shutdown_pass':quiesced_pass or terminal_pass,
              'exact_auxiliary_lease_absent':not (control/'AUX_LEASE.json').exists()}
    observed['producer_shutdown_barrier_pass']=all([observed['campaign_status_is_stopped'],
        not live,not pending,not unaudited,matching,flags,observed['exact_controller_shutdown_pass'],
        observed['exact_auxiliary_lease_absent']])
    return observed


def tick():
    state = load_state()
    if state['best_blocks'] > 318:
        audit_best(state, PROJECT / 'data/cover-318.txt', 318, EXPECTED_BASELINE_HASH,
                   BASELINE_UTC, baseline=True)
    # Discover completed witnesses independently even before supervisor status
    # appears; files are saved atomically by the campaign binary.
    candidates = []
    for path in (CAMPAIGN / 'runs').glob('*/shrink_cover_54_16_4_*.txt'):
        match = re.fullmatch(r'shrink_cover_54_16_4_(\d+)_\d+\.txt', path.name)
        if match and int(match.group(1)) < state['best_blocks']:
            candidates.append((path.stat().st_mtime_ns, int(match.group(1)), path))
    for _, count, path in sorted(candidates):
        if count < state['best_blocks']:
            raw = stable_read(path)
            audit_best(state, path, count, sha(raw), utc())
    status_path = CAMPAIGN / 'status.json'
    status = json.loads(stable_read(status_path)) if status_path.exists() else None
    if status:
        audit_archived_partials(state, status)
        # Preserve intermediate verified bounds even when multiple improvements
        # occur between polls or arrive through the exact-repair inbox.
        archive = status.get('full_archive', {})
        records = archive.values() if isinstance(archive, dict) else archive
        for record in sorted(records, key=lambda item: item.get('verified_utc', '')):
            if record['sha256'] not in state['best_seen_hashes']:
                audit_best(state, Path(record['path']), record['blocks'], record['sha256'], record['verified_utc'])
        best = status.get('best') or {}
        if best:
            audit_best(state, Path(best['path']), best['blocks'], best['sha256'],
                       best.get('verified_utc') or status['last_improvement_utc'])
        workers = status.get('workers', [])
        if isinstance(workers, dict):
            workers = list(workers.values())
    else:
        bootstrap = CAMPAIGN / 'bootstrap.json'
        workers = json.loads(bootstrap.read_text()) if bootstrap.exists() else []
    partials = []
    for worker in workers:
        if not isinstance(worker, dict) or 'directory' not in worker:
            continue
        try:
            partial = audit_partial(state, worker)
            if partial:
                partials.append(dict(partial, worker=Path(worker['directory']).name))
        except (OSError, ValueError) as error:
            append_json(ROOT / 'read_events.jsonl', {'utc': utc(), 'path': worker.get('directory'), 'error': str(error)})
    pool_summary = audit_partial_pool(state,status)
    stamp = utc()
    elapsed = (parse_utc(stamp) - parse_utc(state['last_improvement_utc'])).total_seconds()
    stopping_reason = status.get('stopping_reason') if status else None
    stop_audit = None
    if stopping_reason:
        # User cancellation is distinct from the mathematical stall criterion.
        stop_time = status.get('stopped_utc') or status.get('updated_utc') or stamp
        stop_elapsed = (parse_utc(stop_time) - parse_utc(state['last_improvement_utc'])).total_seconds()
        stop_audit = {'stopping_reason': stopping_reason, 'stop_utc': stop_time,
                      'last_verified_improvement_utc': state['last_improvement_utc'],
                      'elapsed_seconds': stop_elapsed,
                      'strictly_exceeds_10800_seconds': stop_elapsed > 10800,
                      'supervisor_reported_gap_seconds': status.get('seconds_since_verified_improvement'),
                      'supervisor_gap_strictly_exceeds_10800_seconds': (status.get('seconds_since_verified_improvement', -1) > 10800)}
        stop_audit.update(audit_shutdown_barrier(state,status))
        signature = json.dumps(stop_audit, sort_keys=True)
        if state.get('stop_audited_signature') != signature:
            write_json(ROOT / 'stop_audit.json', stop_audit)
            append_json(ROOT / 'stop_ledger.jsonl', stop_audit)
            state['stop_audited_signature'] = signature
            print(json.dumps({'event': 'STOP_AUDIT', **stop_audit}), flush=True)
    write_json(ROOT / 'state.json', state)
    write_json(ROOT / 'status.json', {
        'audit_utc': stamp, 'status_source_present': status is not None,
        'best_blocks': state['best_blocks'], 'best_sha256': state['best_sha256'],
        'best_snapshot': state['best_path'], 'baseline_restart_utc': BASELINE_UTC,
        'last_verified_improvement_utc': state['last_improvement_utc'],
        'elapsed_since_verified_improvement_seconds': elapsed,
        'stall_threshold_seconds': 10800, 'stall_threshold_strictly_exceeded': elapsed > 10800,
        'partials': partials, 'partial_pool': pool_summary, 'stop_audit': stop_audit,
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--watch', action='store_true')
    parser.add_argument('--interval', type=float, default=20)
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            tick()
        except Exception as error:
            event = {'event': 'AUDIT_ERROR', 'utc': utc(), 'error': repr(error)}
            append_json(ROOT / 'errors.jsonl', event)
            print(json.dumps(event), flush=True)
            if not args.watch:
                raise
        if not args.watch:
            break
        time.sleep(args.interval)


if __name__ == '__main__':
    main()
