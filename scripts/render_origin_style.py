#!/usr/bin/env python3
"""Render reproducible Matplotlib PDF/SVG/PNG previews from prepared Origin data.

Not a native Origin theme/project. Values must be actual prepared measurements.
"""
import argparse
import csv
import json
import math
from pathlib import Path
import sys


def render(table, styles, profile, out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    config=json.loads(Path(styles).read_text(encoding='utf-8'))
    if profile not in config['profiles']:raise ValueError('Unknown style profile')
    style=config['profiles'][profile];mapping=config['methods']
    with Path(table).open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        rows=list(reader)
    if not rows:raise ValueError('Empty summarized table')
    required={'panel','series','x','mean','lower','upper','n','interval'}
    if not required.issubset(reader.fieldnames or []):raise ValueError('Missing summary columns')
    panels=sorted({r['panel'] for r in rows})
    series=sorted({r['series'] for r in rows})
    unknown=set(series)-set(mapping)
    if unknown:raise ValueError(f'Methods lacking stable styles: {sorted(unknown)}')
    seen=set()
    for name in series:
        spec=mapping[name]
        signature=(spec['color'],spec['line'])
        if signature in seen:raise ValueError('Two distinct methods have identical color AND line style')
        seen.add(signature)
    grouped={}
    for r in rows:
        key=r['panel'],r['series']
        x=float(r['x']);m=float(r['mean'])
        if not math.isfinite(x) or not math.isfinite(m):raise ValueError('Nonfinite x or mean')
        lower=float(r['lower']) if r['lower'] else None
        upper=float(r['upper']) if r['upper'] else None
        if (lower is None)!=(upper is None):raise ValueError('Incomplete interval')
        if lower is not None and (not math.isfinite(lower) or not math.isfinite(upper) or lower>upper):
            raise ValueError('Invalid interval')
        grouped.setdefault(key,[]).append((x,m,lower,upper))
    for key,vals in grouped.items():
        vals.sort()
        if len({x for x,*_ in vals})!=len(vals):raise ValueError(f'Duplicate X in {key}')
    # A single checkpoint is a POINT, not a fabricated continuous learning curve.
    width=style['width_mm']/25.4
    ncols=min(3,len(panels));nrows=(len(panels)+ncols-1)//ncols
    fig,axes=plt.subplots(nrows,ncols,figsize=(width,max(2.0,width*0.46*nrows/ncols)),squeeze=False,sharex=False,sharey=False)
    rcParams.update({'font.family':style['font'], 'font.size':style['tick_pt']})
    legend={}
    for i,p in enumerate(panels):
        ax=axes[i//ncols][i%ncols]
        for s in series:
            v=grouped.get((p,s),[])
            if not v:continue
            xs=[x for x,_,_,_ in v]; ms=[m for _,m,_,_ in v]
            lower=[lo for _,_,lo,_ in v]; upper=[hi for _,_,_,hi in v]
            spec=mapping[s]
            lw=style['focus_line_pt'] if spec.get('focus') else style['normal_line_pt']
            if len(v)==1:
                artist=ax.plot(xs,ms,linestyle='None',marker='o',markersize=4,color=spec['color'],label=s)[0]
            else:
                artist=ax.plot(xs,ms,linewidth=lw,color=spec['color'],linestyle=spec['line'],label=s)[0]
            if all(lo is not None and hi is not None for lo,hi in zip(lower,upper)):
                ax.fill_between(xs,lower,upper,color=spec['color'],alpha=style['band_alpha'],linewidth=0)
            legend.setdefault(s,artist)
        ax.set_title(p,fontsize=style['title_pt'])
        ax.set_xlabel('Recorded checkpoint',fontsize=style['label_pt'])
        ax.set_ylabel('Measured outcome',fontsize=style['label_pt'])
        ax.tick_params(labelsize=style['tick_pt'])
        for spine in ax.spines.values():spine.set_linewidth(style['axis_pt'])
    for j in range(len(panels),nrows*ncols):axes[j//ncols][j%ncols].set_visible(False)
    if legend:fig.legend(list(legend.values()),list(legend),loc='upper center',bbox_to_anchor=(0.5,1.03),ncol=min(3,len(legend)),frameon=False,fontsize=style['tick_pt'])
    fig.tight_layout(rect=(0,0,1,0.96))
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    if out.suffix.lower() not in ('.pdf','.png','.svg'):raise ValueError('Output must end .pdf, .png, or .svg')
    fig.savefig(out,dpi=300,bbox_inches='tight')
    plt.close(fig)
    info={'profile':profile,'styles':str(styles),'input':str(table),'panels':panels,'series':series,
          'note':'Matplotlib preview only; labels/uncertainties derived from supplied data, not OGPO paper values'}
    out.with_suffix(out.suffix+'.meta.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return info


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('--styles',type=Path,required=True)
    p.add_argument('--profile',default='origin_publication');p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    try: print(json.dumps(render(a.input,a.styles,a.profile,a.output),ensure_ascii=False));return 0
    except (OSError,ValueError,ImportError) as e:print('ERROR:',e,file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
