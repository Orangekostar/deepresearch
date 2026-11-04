#!/usr/bin/env python3
"""Bounded experiment runner. Real evaluator, no internal LLM or daemon.

Requires Python >=3.10 and POSIX for fcntl / process groups. NOT a sandbox.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, obj):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.part')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(path)


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def hashes(project, names):
    out = {}
    for name in names:
        p = project / name
        if p.is_symlink() or not p.is_file():
            raise ValueError(f'Missing or symlinked declared file: {name}')
        out[name] = digest(p.read_bytes())
    return out


def validate(raw, source):
    if raw.get('schema_version') != 1 or not isinstance(raw.get('name'), str) or not raw['name']:
        raise ValueError('schema_version=1 and nonempty name required')
    project = (source.parent / raw.get('project_dir', '.')).resolve()
    if not project.is_dir():
        raise ValueError(f'Missing project: {project}')
    for role in ('search', 'confirm'):
        arr = raw.get('commands', {}).get(role)
        if not isinstance(arr, list) or not arr or any(not isinstance(a, str) or not a for a in arr):
            raise ValueError('Commands must be argv lists for search and confirm')
    metric = raw.get('metric', {})
    if not metric.get('name') or metric.get('direction') not in ('min', 'max'):
        raise ValueError('Need metric name and direction min/max')
    delta = metric.get('min_delta', 0)
    if isinstance(delta, bool) or not isinstance(delta, (int,float)) or not math.isfinite(delta) or delta < 0:
        raise ValueError('Invalid min_delta')
    for field in ('editable_files', 'protected_files'):
        names = raw.get(field)
        if not isinstance(names, list) or not names or len(set(names)) != len(names):
            raise ValueError(f'{field}: need distinct file list')
        for name in names:
            if not isinstance(name, str) or Path(name).is_absolute() or '..' in Path(name).parts:
                raise ValueError(f'Unsafe relative path: {name}')
            if not (project/name).resolve().is_relative_to(project):
                raise ValueError(f'Path escapes project: {name}')
    if set(raw['editable_files']) & set(raw['protected_files']):
        raise ValueError('Protected and editable files overlap')
    hashes(project, raw['editable_files']+raw['protected_files'])
    budget = raw.get('budgets', {})
    for k in ('max_trials', 'per_trial_seconds', 'max_total_seconds', 'max_consecutive_failures'):
        v=budget.get(k)
        if isinstance(v, bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<=0:
            raise ValueError(f'Invalid positive finite budget {k}')
    for k in ('max_trials','max_consecutive_failures'):
        if not isinstance(budget[k],int):
            raise ValueError(f'{k} must be integer')
    normalized = dict(raw)
    normalized['project_dir'] = str(project)
    return normalized


def records(state):
    return [read(p) for p in sorted((state/'trials').glob('*/record.json'))]


def report(session, rows):
    budget=session['config']['budgets']
    elapsed=sum(r.get('elapsed_seconds',0) for r in rows)
    completed=[r for r in rows if r['status']=='completed']
    eligible=[r for r in completed if r['decision'] in ('baseline','candidate_keep')]
    failures=0
    for r in rows[::-1]:
        if r['status']=='completed':
            break
        failures += 1
    reasons=[]
    if session.get('finished'): reasons.append('finished')
    if any(r['status']=='running' for r in rows): reasons.append('unfinished_trial')
    if len(rows)>=budget['max_trials']: reasons.append('max_trials')
    if elapsed>=budget['max_total_seconds']: reasons.append('max_total_seconds')
    if failures>=budget['max_consecutive_failures']: reasons.append('max_consecutive_failures')
    return dict(trials=len(rows), elapsed_seconds=round(elapsed,6),
                baseline=next((r['trial_id'] for r in completed if r['role']=='baseline'),None),
                incumbent=None if not eligible else {'trial_id':eligible[-1]['trial_id'], 'metric':eligible[-1]['metric']},
                confirmation_trials=sum(r['role']=='confirmation' for r in completed),
                stop_reasons=reasons, scientific_claim_status='not_determined_by_runner')


@contextmanager
def lock(state):
    if not (state/'session.json').is_file():
        raise ValueError('Uninitialized state directory')
    with (state/'session.lock').open('a+') as f:
        fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try: yield
        finally: fcntl.flock(f,fcntl.LOCK_UN)


def load_session(state):
    sess=read(state/'session.json')
    raw=read(sess['source_config'])
    if digest(json.dumps(raw,sort_keys=True).encode())!=sess['config_digest']:
        raise ValueError('Source config changed after init; use new session')
    project=Path(sess['config']['project_dir'])
    current=hashes(project,sess['config']['protected_files'])
    if current!=sess['protected_hashes']:
        raise ValueError('Protected file hash drift detected')
    return sess


def init(args):
    source=args.config.resolve()
    raw=read(source)
    config=validate(raw,source)
    project=Path(config['project_dir'])
    state=args.state.resolve()
    if state.exists(): raise ValueError('State exists; use a fresh directory')
    if state == project or state.is_relative_to(project):
        raise ValueError('Keep state directory outside project')
    state.mkdir(parents=True)
    (state/'trials').mkdir()
    write(state/'session.json',dict(config=config, source_config=str(source),
        config_digest=digest(json.dumps(raw,sort_keys=True).encode()),
        protected_hashes=hashes(project,config['protected_files']),
        initial_editable_hashes=hashes(project,config['editable_files']),
        created=timestamp(),finished=False))
    print(json.dumps({'initialized':str(state),'project':str(project)}))


def terminate(proc):
    if proc is None: return
    try: os.killpg(proc.pid,signal.SIGTERM)
    except ProcessLookupError: pass
    try: proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        try: os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError: pass
        proc.wait()


def run(args):
    state=args.state.resolve()
    with lock(state):
        sess=load_session(state)
        rows=records(state)
        summary=report(sess, rows)
        if summary['stop_reasons']: raise ValueError('Session stopped: '+','.join(summary['stop_reasons']))
        if args.role!='baseline' and summary['baseline'] is None:
            raise ValueError('A successful baseline is required first')
        if args.role=='baseline' and summary['baseline'] is not None:
            raise ValueError('Baseline already exists; use confirmation to rerun')
        config=sess['config']; project=Path(config['project_dir'])
        source_before=hashes(project,config['editable_files']+config['protected_files'])
        used_ids=[int(p.name) for p in (state/'trials').iterdir() if p.is_dir() and p.name.isdigit()]
        trial_id=f'{max(used_ids,default=0)+1:06d}'
        folder=state/'trials'/trial_id
        folder.mkdir()
        (folder/'source').mkdir()
        for name in config['editable_files']:
            dest=folder/'source'/name; dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(project/name,dest)
        phase='confirm' if args.role=='confirmation' else 'search'
        remaining=config['budgets']['max_total_seconds']-summary['elapsed_seconds']
        timeout=min(config['budgets']['per_trial_seconds'],remaining)
        row=dict(trial_id=trial_id, role=args.role, label=args.label or args.role,
                 hypothesis=args.hypothesis, seed=args.seed, phase=phase,
                 status='running', decision=None, metric=None,
                 source_sha256=source_before, started_at=timestamp(),
                 command=config['commands'][phase], timeout_seconds=timeout)
        write(folder/'record.json',row)
        env=os.environ.copy()
        env.update(OGPO_PHASE=phase,OGPO_SEED=str(args.seed),OGPO_TRIAL_ID=trial_id,
                   OGPO_RESULT_PATH=str(folder/'metrics.json'))
        proc=None; start=time.monotonic()
        try:
            with (folder/'run.log').open('w',encoding='utf-8') as log:
                proc=subprocess.Popen(config['commands'][phase],cwd=project,env=env,
                    stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
                row['pid']=proc.pid; write(folder/'record.json',row)
                code=proc.wait(timeout=timeout)
                terminate(proc); proc=None
            if code!=0: raise RuntimeError(f'Evaluation exit code {code}')
            if source_before!=hashes(project,config['editable_files']+config['protected_files']):
                raise RuntimeError('Declared source changed during run')
            if sess['protected_hashes']!=hashes(project,config['protected_files']):
                raise RuntimeError('Protected file changed during run')
            metrics_path=folder/'metrics.json'
            if metrics_path.is_symlink() or not metrics_path.is_file():
                raise RuntimeError('Missing fresh metrics file')
            result=read(metrics_path)
            value=result.get('metrics',{}).get(config['metric']['name'])
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
                raise RuntimeError('Primary metric is missing or nonfinite')
            row.update(status='completed',metric=value,metric_sha256=digest(metrics_path.read_bytes()))
            if args.role=='baseline': row['decision']='baseline'
            elif args.role=='confirmation': row['decision']='confirmation_recorded'
            else:
                previous=summary['incumbent']['metric']
                gain=(previous-value if config['metric']['direction']=='min' else value-previous)
                row['gain']=gain
                row['decision']='candidate_keep' if gain>0 and gain>=config['metric'].get('min_delta',0) else 'candidate_discard'
        except subprocess.TimeoutExpired:
            row.update(status='timeout',decision='invalid',error='Per-trial/remaining session timeout')
        except (OSError,RuntimeError,ValueError,KeyError,json.JSONDecodeError) as e:
            row.update(status='failed',decision='invalid',error=str(e))
        finally:
            terminate(proc)
            row.update(elapsed_seconds=round(time.monotonic()-start,6),finished_at=timestamp())
            if row['status']!='completed': row['metric']=None
            write(folder/'record.json',row)
            with (state/'history.jsonl').open('a',encoding='utf-8') as history:
                history.write(json.dumps(row,ensure_ascii=False,allow_nan=False)+'\n')
        print(json.dumps(row,ensure_ascii=False,indent=2))
        return 0 if row['status']=='completed' else 1


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='action',required=True)
    a=sub.add_parser('init');a.add_argument('--config',type=Path,required=True);a.add_argument('--state',type=Path,required=True)
    a=sub.add_parser('run');a.add_argument('--state',type=Path,required=True)
    a.add_argument('--role',choices=['baseline','candidate','confirmation'],required=True)
    a.add_argument('--hypothesis',required=True);a.add_argument('--seed',type=int,required=True);a.add_argument('--label')
    for name in ('status','finish','recover'):
        a=sub.add_parser(name);a.add_argument('--state',type=Path,required=True)
        if name in ('finish','recover'):a.add_argument('--reason',required=True)
    args=p.parse_args()
    try:
        if args.action=='init':return init(args) or 0
        if args.action=='run':return run(args)
        state=args.state.resolve()
        with lock(state):
            sess=load_session(state)
            rows=records(state)
            if args.action=='recover':
                for r in rows:
                    if r['status']!='running':continue
                    pid=r.get('pid')
                    if pid:
                        try:
                            os.killpg(pid,0)
                        except ProcessLookupError:
                            pass
                        except PermissionError as e:
                            raise ValueError(f'Cannot verify process group {pid}: {e}')
                        else:
                            raise ValueError(f'Process group {pid} may still be active; inspect it before recovery')
                    folder=state/'trials'/r['trial_id']
                    r.update(status='interrupted',decision='invalid',metric=None,
                             error=args.reason, finished_at=timestamp(),
                             elapsed_seconds=r['timeout_seconds'],
                             recovery_note='Conservative full timeout charged; no metric inferred')
                    write(folder/'record.json',r)
                    with (state/'history.jsonl').open('a',encoding='utf-8') as h:
                        h.write(json.dumps(r,ensure_ascii=False,allow_nan=False)+'\n')
                rows=records(state)
            if args.action=='finish':
                if any(r['status']=='running' for r in rows):raise ValueError('Unfinished trial; preserve and inspect evidence')
                sess.update(finished=True,finished_at=timestamp(),finish_reason=args.reason)
                write(state/'session.json',sess)
            print(json.dumps(report(sess,rows),ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,KeyError,BlockingIOError,TypeError) as e:
        print(f'ERROR: {e}',file=sys.stderr)
        return 2

if __name__=='__main__':
    sys.exit(main())
