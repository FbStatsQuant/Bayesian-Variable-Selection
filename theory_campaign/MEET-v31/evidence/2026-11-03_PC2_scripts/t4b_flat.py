# Search (fixed seed) for an exactly enumerated posterior with pi(top-c) < alpha, so C1(b)'s "unscored" sentence is
# non-vacuous while (all models scored, Zhat = Z) the unscored mass is 0.
import numpy as np, math, sys
sys.path.insert(0, __file__.rsplit('/',1)[0]); from pc2_common import *
rng=np.random.default_rng(20261107); alpha=0.05
best=None
for s in range(400):
    p=12; n=int(rng.integers(8,30)); Xr=rng.standard_normal((n,p)); a=rng.uniform(0,3)
    Xr=Xr+a*rng.standard_normal((n,1)); w=rng.standard_normal(p)*rng.uniform(0,1.5); yr=Xr@w+rng.standard_normal(n)
    X,y=std(Xr,yr); T=Target(X,y); Fall=T.enum(); lZ=lse(Fall.values())
    o=sorted(Fall.values(),reverse=True); r1=math.exp(o[0]-lZ); r5=math.exp(lse(o[:5])-lZ)
    if best is None or r1<best[0]: best=(r1,r5,n,s,math.exp(lse(o[:49])-lZ),math.exp(lse(o[:481])-lZ))
print("min pi(Shat)=%.4f  pi(top5)=%.4f  (n=%d, draw %d)  pi(top 4p+1)=%.4f  pi(top 40p+1)=%.4f"%best)
r1=best[0]; print("C1(b) with T={Shat}: bound 1-pi(Shat)/alpha = %+.4f vs unscored mass 0"%(1-r1/alpha))
