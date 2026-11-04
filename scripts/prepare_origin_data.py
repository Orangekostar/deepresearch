#!/usr/bin/env python3
"""Convert tidy independent-repeat curves into an Origin-ready wide summary CSV."""
import argparse
import csv
import json
import math
from pathlib import Path
import random
import statistics
import sys

REQUIRED=('panel','series','replicate','x','y')
FIELDS=('panel','series','x','mean','lower','upper','err_minus','err_plus','n','interval','independent_unit')


def fnumber(value, label):
    try: v=float(value)
    except (TypeError,ValueError): raise ValueError(f'Invalid numeric {label}: {value!r}')
    if not math.isfinite(v):raise ValueError(f'Nonfinite {label}')
    return v


def summarize(source, interval='none', independent_unit='seed', bootstrap=1000, rng_seed=0):
    with Path(source).open(newline='', encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or any(c not in reader.fieldnames for c in REQUIRED):
            raise ValueError('Input needs panel,series,replicate,x,y')
        rows=list(reader)
    if not rows:raise ValueError('No observations')
    # Preserve all observations, including genuine zero. Explicitly reject missing / duplicate values.
    groups={}; grids={}
    for i,r in enumerate(rows,2):
        p,s,rep=(r[k].strip() for k in ('panel','series','replicate'))
        if not p or not s or not rep:raise ValueError(f'Empty identifiers at line {i}')
        x=fnumber(r['x'],f'line {i} x');y=fnumber(r['y'],f'line {i} y')
        k=(p,s,rep)
        group=groups.setdefault(k,{})
        if x in group:raise ValueError(f'Duplicate x={x} in {k}')
        group[x]=y
        grids.setdefault((p,s),{})[rep]=group
    # Unequal checkpoint grids often create misleading means; reject, never interpolate.
    for key,runmaps in grids.items():
        vals=[set(m) for m in runmaps.values()]
        if any(v!=vals[0] for v in vals[1:]):
            raise ValueError(f'Unequal X grids for {key}; predeclare alignment first')
    panels={}
    for (p,s), runmaps in grids.items():
        panels.setdefault(p,{})[s]=set(next(iter(runmaps.values())))
    for p,series in panels.items():
        values=list(series.values())
        if any(s!=values[0] for s in values[1:]):
            raise ValueError(f'Unequal X grids across series in panel={p}')
    rng=random.Random(rng_seed)
    if interval=='bootstrap95' and bootstrap<100:raise ValueError('Bootstrap draws must be >=100')
    out=[]
    for (p,s),runmaps in sorted(grids.items()):
        ordered=[v for _,v in sorted(runmaps.items())]
        n=len(ordered)
        # Each bootstrap draw selects entire run identities. Share the same
        # selected identities across *all* checkpoints in the curve.
        resamples = ([[rng.randrange(n) for _ in range(n)] for _ in range(bootstrap)]
                     if interval=='bootstrap95' and n>=2 else None)
        for x in sorted(next(iter(runmaps.values()))):
            sample=[v[x] for v in ordered]
            mean=statistics.fmean(sample)
            low=high=None
            if interval in ('sd','sem') and n>=2:
                d=statistics.stdev(sample)
                if interval=='sem':d/=math.sqrt(n)
                low,high=mean-d,mean+d
            elif interval=='bootstrap95' and n>=2:
                # Resample whole independent replicate identities; each x shares the same
                # replicate pool. Pointwise intervals, NOT simultaneous curve intervals.
                boots=[statistics.fmean(sample[i] for i in ids) for ids in resamples]
                boots.sort()
                low=boots[int((bootstrap-1)*.025)]
                high=boots[int((bootstrap-1)*.975)]
            result=dict(panel=p,series=s,x=x,mean=mean,lower='' if low is None else low,
                        upper='' if high is None else high,
                        err_minus='' if low is None or low>mean else mean-low,
                        err_plus='' if high is None or high<mean else high-mean,
                        n=n,interval=interval if low is not None else 'none',independent_unit=independent_unit)
            out.append(result)
    return out,dict(source=str(source),n_raw=len(rows),n_summary=len(out),interval=interval,
                    independent_unit=independent_unit,bootstrap_draws=bootstrap if interval=='bootstrap95' else None,
                    bootstrap_seed=rng_seed if interval=='bootstrap95' else None,
                    note='Pointwise bootstrap over independent replicate identities; no interpolation. Valid zero preserved; invalid runs excluded upstream.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--interval',choices=['none','sd','sem','bootstrap95'],default='none')
    p.add_argument('--independent-unit',required=True)
    p.add_argument('--bootstrap-draws',type=int,default=1000);p.add_argument('--seed',type=int,default=0)
    args=p.parse_args()
    try:
        rows,metadata=summarize(args.input,args.interval,args.independent_unit,args.bootstrap_draws,args.seed)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows(rows)
        args.output.with_suffix(args.output.suffix+'.meta.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(metadata,ensure_ascii=False))
        return 0
    except (OSError,ValueError) as e:print('ERROR:',e,file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
