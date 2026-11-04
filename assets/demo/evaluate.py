#!/usr/bin/env python3
"""Real synthetic linear-regression CPU demo, not a scholarly algorithm benchmark."""
import json, math, os, random
from pathlib import Path


def dataset(seed,n):
    r=random.Random(seed)
    return [(x,2.25*x-0.65+r.gauss(0,0.1)) for x in (r.uniform(-2,2) for _ in range(n))]

phase=os.environ['OGPO_PHASE'];seed=int(os.environ['OGPO_SEED'])
if phase not in ('search','confirm'):raise ValueError('Bad phase')
cfg=json.loads(Path('train_config.json').read_text())
lr=float(cfg['learning_rate']);steps=cfg['steps']
if not (math.isfinite(lr) and 0<lr<=1 and isinstance(steps,int) and 1<=steps<=20000):raise ValueError('Bad training settings')
train=dataset(1103,128)
rng=random.Random(seed)
w,b=rng.uniform(-0.5,0.5),rng.uniform(-0.5,0.5)
for _ in range(steps):
    dw=sum(2*(w*x+b-y)*x for x,y in train)/len(train)
    db=sum(2*(w*x+b-y) for x,y in train)/len(train)
    w-=lr*dw;b-=lr*db
    if not (math.isfinite(w) and math.isfinite(b)):raise ValueError('Nonfinite fit')
evaldata=dataset(2301,256) if phase=='search' else dataset(4409,384)
mse=sum((w*x+b-y)**2 for x,y in evaldata)/len(evaldata)
path=Path(os.environ['OGPO_RESULT_PATH'])
with path.open('x',encoding='utf-8') as f:
    json.dump({'metrics':{'mse':mse},'details':{'phase':phase,'seed':seed,'n_train':128,'n_eval':len(evaldata),'independent_unit':'initialization seed; fixed synthetic partitions','status':'demo_not_research'}},f)
print(phase,'seed',seed,'mse',mse)
