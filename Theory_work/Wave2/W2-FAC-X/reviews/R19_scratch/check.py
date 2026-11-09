import json
from pathlib import Path
import numpy as np

out = dict(algebra_cases=0, max_schur_error=0., max_projection_error=0., max_swap_error=0., paths=0, steps=0, crossings=0, band_checks=0, violations=0)
for seed in range(20):
    rng = np.random.default_rng(seed + 19000)
    for rep in range(10):
        k = int(rng.integers(2, 12)); N = 40
        U = rng.normal(size=(N,k)); v = rng.normal(size=k); b = rng.normal(size=k)
        A = U.T@U + np.outer(b,b); inv = np.linalg.inv(A)
        q = v@inv@v
        projection = v@np.linalg.solve(A+np.outer(v,v),v)
        out['max_projection_error'] = max(out['max_projection_error'], abs(projection-q/(1+q)))
        for j in range(k):
            ix = np.arange(k)!=j
            diff = q-v[ix]@np.linalg.solve(A[np.ix_(ix,ix)],v[ix])
            out['max_schur_error'] = max(out['max_schur_error'], abs(diff-(inv@v)[j]**2/inv[j,j]))
        kap = 10**rng.uniform(-3,3); tj,tl = rng.normal(size=2)
        g=1/(k+kap); gm=1/(k-1+kap)
        lhs=(1+gm)*((1-g)**2*(tl+gm*tj)**2-tj**2)
        rhs=tl**2-tj**2-g*(tl-tj)**2
        out['max_swap_error']=max(out['max_swap_error'],abs(lhs-rhs))
        out['algebra_cases']+=1
    for rep in range(20):
        size=int(rng.integers(3,160)); vals=rng.normal(size=size)
        kap=1+10**rng.uniform(-2,2); B=rng.normal()*5
        tol=10**rng.uniform(-5,0); kept=set(range(size)); deleted=set()
        Q=max(int(np.sum((vals>=v)&(vals<=v+9*tol))) for v in vals)
        dense_ok=4*Q/(size-Q-1+kap)<=.1
        while kept:
            x=(sum(vals[j] for j in kept)+B)/(len(kept)+kap)
            a=max([vals[j] for j in kept if vals[j]<x],default=-np.inf)
            b=min([vals[j] for j in kept if vals[j]>x],default=np.inf)
            if dense_ok and len(kept)>=2:
                out['band_checks']+=1
                assert all(a-4.3*tol<vals[j]<b+4.3*tol for j in deleted)
            d=min(abs(vals[j]-x) for j in kept)
            candidates=[j for j in kept if abs(vals[j]-x)<=d+2*tol]
            j=int(rng.choice(candidates))
            xn=x-(vals[j]-x)/(len(kept)-1+kap)
            crossing=any(min(x,xn)<vals[l]<max(x,xn) for l in kept if l!=j)
            if crossing:
                out['crossings']+=1
                assert d<2*tol/(len(kept)-2+kap)
                assert b-a<=2*d+2*tol+1e-12
                if len(kept)>=3: assert b-a<4*tol
            kept.remove(j); deleted.add(j); out['steps']+=1
        out['paths']+=1
assert max(out['max_projection_error'],out['max_schur_error'],out['max_swap_error'])<1e-11
text=json.dumps(out,indent=2)
Path(__file__).with_name('check_output.json').write_text(text+'\n',encoding='utf-8')
print(text)
