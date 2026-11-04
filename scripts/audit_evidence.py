#!/usr/bin/env python3
"""Structural audit only. Does not verify scientific truth or statistical validity."""
import argparse
import json
import math
from pathlib import Path
import sys


def audit(data, home):
    errors=[]; warnings=[]
    if data.get('schema_version')!=1:errors.append('schema_version must be 1')
    cs=data.get('claims',[]); es=data.get('experiments',[])
    if not isinstance(cs,list) or not isinstance(es,list):return ['claims/experiments must be lists'], []
    claims={c.get('id'):c for c in cs if isinstance(c,dict)}
    exps={e.get('id'):e for e in es if isinstance(e,dict)}
    if len(claims)!=len(cs):errors.append('Duplicate/missing claim IDs')
    if len(exps)!=len(es):errors.append('Duplicate/missing experiment IDs')
    for ident,c in claims.items():
        status=c.get('status')
        if status not in ('hypothesis','supported','mixed','refuted'):errors.append(f'{ident}: bad claim status')
        linked=c.get('evidence_ids',[])
        if not isinstance(linked,list):errors.append(f'{ident}: evidence_ids not list');continue
        for e in linked:
            if e not in exps:errors.append(f'{ident}: unknown evidence {e}')
        if status=='supported':
            supports=[e for e in linked if exps.get(e,{}).get('status')=='completed' and exps[e].get('interpretations',{}).get(ident)=='supports']
            refutes=[e for e in linked if exps.get(e,{}).get('status')=='completed' and exps[e].get('interpretations',{}).get(ident)=='refutes']
            if not supports or refutes:errors.append(f'{ident}: supported not justified by recorded interpretations')
        elif status=='hypothesis':warnings.append(f'{ident}: remains a hypothesis')
    for ident,e in exps.items():
        status=e.get('status')
        if status not in ('planned','running','completed','failed'):errors.append(f'{ident}: bad experiment status');continue
        for c in e.get('claim_ids',[]):
            if c not in claims:errors.append(f'{ident}: unknown claim {c}')
        if status=='completed':
            result=e.get('result')
            if not isinstance(result,dict):errors.append(f'{ident}: completed missing result');continue
            n=result.get('n_independent')
            if isinstance(n,bool) or not isinstance(n,int) or n<1:errors.append(f'{ident}: missing independent-unit count')
            if not result.get('independent_unit'):errors.append(f'{ident}: no independent unit')
            for m in result.get('measurements',[]):
                v=m.get('value')
                if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):
                    errors.append(f'{ident}: nonfinite metric')
            artifacts=e.get('artifacts',[])
            if not artifacts:errors.append(f'{ident}: missing artifact')
            for item in artifacts:
                if item.startswith(('https://','http://')):continue
                p=Path(item);p=p if p.is_absolute() else home/p
                if not p.is_file():errors.append(f'{ident}: artifact missing {item}')
            for c in e.get('claim_ids',[]):
                if c not in e.get('interpretations',{}):errors.append(f'{ident}: missing interpretation {c}')
        elif e.get('result') is not None:errors.append(f'{ident}: result supplied for noncompleted experiment')
    for c in data.get('manuscript_claim_ids',[]):
        if c not in claims or claims[c].get('status')!='supported':
            errors.append(f'Manuscript claim {c} lacks supported evidence status')
    return errors,warnings


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('ledger',type=Path)
    args=p.parse_args()
    try:
        path=args.ledger.resolve();data=json.loads(path.read_text(encoding='utf-8'))
        errors,warnings=audit(data,path.parent)
    except (ValueError,OSError,TypeError) as e:
        print('INPUT ERROR:',e);return 2
    for a in warnings:print('WARNING:',a)
    for a in errors:print('ERROR:',a)
    print(f'{"FAIL" if errors else "PASS"}: {len(errors)} errors, {len(warnings)} warnings. Structural only.')
    return int(bool(errors))

if __name__=='__main__':sys.exit(main())
