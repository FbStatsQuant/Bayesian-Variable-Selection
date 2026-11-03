# C4 cost remark: search small designs for large B&B opt trees (U=[p], Shat = exact HPM). Fixed seed.
import numpy as np, math, sys
sys.path.insert(0, __file__.rsplit('/',1)[0]); from pc2_common import *
from t2_bnb import bnb
rng=np.random.default_rng(20261105)
best=(0,None)
for s in range(120):
    p=12; n=int(rng.integers(6,26)); mode=s%4
    Xr=rng.standard_normal((n,p))
    if mode==1: Xr=Xr+2*rng.standard_normal((n,1))
    if mode==2: Xr[:,6:]=Xr[:,:6]+0.05*rng.standard_normal((n,6))   # 6 near-duplicate pairs
    yr=rng.standard_normal(n) if mode!=3 else Xr[:,:6].sum(1)*0.25+rng.standard_normal(n)
    if mode==2: yr=Xr[:,:6].sum(1)*0.3+rng.standard_normal(n)
    X,y=std(Xr,yr); T=Target(X,y); Fall=T.enum(); Shat=max(Fall,key=lambda S:(Fall[S],-len(S)))
    nO,bet,_=bnb(T,Shat,tuple(range(p)),'opt'); assert not bet
    if nO>best[0]: best=(nO,(n,mode,len(Shat),T.K))
print("largest opt tree:",best[0],"of",2**13-1,"nodes; (n, design mode, |Shat|, K) =",best[1])
