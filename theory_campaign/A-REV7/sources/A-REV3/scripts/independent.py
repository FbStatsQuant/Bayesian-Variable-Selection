import json, math
from pathlib import Path
import numpy as np
from pxn_core import Data, log_bf_sets
rng=np.random.default_rng(2026110203)
rows=[]
for rep in range(3):
    a=np.load(f'results/data_{rep}.npz'); D=Data(a['X'],a['y'])
    for k in range(1,7):
        S=sorted(rng.choice(D.p,k,replace=False).tolist())
        U,s,_=np.linalg.svd(D.X[:,S],full_matrices=False)
        eig=s*s
        logD=np.log(((D.n+1)*eig+1)/(eig+1)).sum()
        Q=D.y@D.y-np.sum(D.n*eig/((D.n+1)*eig+1)*(U.T@D.y)**2)
        bf=-logD/2-D.nu*np.log((.02+Q)/(.02+D.y@D.y))
        orig=log_bf_sets(D,[S])[0]
        rows.append(dict(rep=rep,S=S,spectral=float(bf),author=float(orig),abs_error=float(abs(bf-orig))))
Path('results/independent_scores.json').write_text(json.dumps(rows,indent=2))
print('independent SVD score maximum absolute discrepancy',max(r['abs_error'] for r in rows))
rows=[]
for n in [100,1000,10000]:
    x=np.where(np.arange(n)%2,1.,-1.); x*=math.sqrt((n-1)/n)
    y=x+rng.normal(size=n); y-=y.mean(); y*=math.sqrt((n-1)/(y@y))
    r2=float((x@y/(n-1))**2)
    exact=-(.01+n/2)*math.log1p(-((n-1)**2/(n*(n-.98)))*r2)
    rows.append(dict(n=n,r2=r2,exact_gain_per_n=exact/n,quadratic_gain_per_n=r2/2))
Path('results/independent_expansion.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows))
