"""Falsify L1b/c on every residual direction, p<=8, 10 seeds."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import itertools,json
from pathlib import Path
import numpy as np
out=[]
def root(M):
    w,v=np.linalg.eigh(M)
    return (v*np.sqrt(w))@v.T
def direction(M,T,j):
    v=M[:,j].copy()
    if T:
        Q=np.linalg.qr(M[:,T],mode='reduced')[0]
        v-=Q@(Q.T@v)
    return v/np.linalg.norm(v)
for seed in range(10):
    rng=np.random.default_rng(seed)
    for p in (4,8):
        lam=np.linspace(.4,.85,p)
        S=np.diag(1-lam**2)+np.outer(lam,lam)
        A=root(S); c=np.linalg.eigvalsh(S)[0]
        W=rng.normal(size=(p,p)); W=(W+W.T)/2
        E=.24*W/np.linalg.norm(W,2); e=np.linalg.norm(E,2)
        B=root(np.eye(p)+E)@A; z=rng.normal(size=p)
        maxdir=maxnoise=0.; count=0
        for k in range(p):
            for T in itertools.combinations(range(p),k):
                for j in set(range(p))-set(T):
                    qa=direction(A,T,j); qb=direction(B,T,j)
                    maxdir=max(maxdir,np.linalg.norm(qb-qa))
                    maxnoise=max(maxnoise,abs((qb-qa)@z));count+=1
        bound=10*e/np.sqrt(c)
        assert maxdir<=bound and maxnoise<=bound*np.linalg.norm(z)
        out.append(dict(seed=seed,p=p,count=count,e=e,c=c,maxdir=maxdir,
                        direction_bound=bound,maxnoise=maxnoise,noise_bound=bound*np.linalg.norm(z)))
Path(__file__).with_name('N4_geometry_out.json').write_text(json.dumps(out,indent=2))
print(json.dumps(dict(cases=len(out),directions=sum(x['count'] for x in out),
 max_bound_ratio=max(x['maxdir']/x['direction_bound'] for x in out),failures=0)))
