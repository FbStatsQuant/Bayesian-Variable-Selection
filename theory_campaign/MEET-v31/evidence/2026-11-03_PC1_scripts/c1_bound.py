import sys; sys.path.insert(0, sys.argv[1]); from common import *
rng=np.random.default_rng(20261103)
cases=[(20,10,'indep'),(30,12,'corr'),(8,12,'p>n'),(15,10,'strong')]
for n,p,kind in cases:
    K=min(p,n//2)
    if kind=='corr':
        Z0=rng.standard_normal((n,1)); Xr=0.9*Z0+0.3*rng.standard_normal((n,p))
    else: Xr=rng.standard_normal((n,p))
    beta=np.zeros(p); beta[:3]=[2,-1.5,1] if kind!='strong' else [20,-15,10]
    yr=3+Xr@beta+rng.standard_normal(n)*(0.05 if kind=='strong' else 1)
    X,y=standardise(Xr,yr)
    F=enum_F(X,y,K); logZ=lse(F.values())
    minD=min(score_parts(X,y,S)[0] for S in F); minQ=min(score_parts(X,y,S)[1] for S in F)
    yy=float(y@y); nu=a0+n/2
    logB=logCn(n)-nu*math.log(2*b0+yy/(n+1))
    print(f"{kind:7s} n={n} p={p} K={K} #models={len(F)} yTy={yy:.4f}(n-1={n-1}) min logD={minD:.3e} minQ={minQ:.5f} yTy/(n+1)={yy/(n+1):.5f} logZ={logZ:.4f} logBound={logB:.4f} ok={logZ<=logB and minD>=-1e-12 and minQ>=yy/(n+1)-1e-12}")
# uncentred y, raw (bound should hold for any y)
n,p=12,8; X=rng.standard_normal((n,p)); y=rng.standard_normal(n)+5
F=enum_F(X,y,min(p,n//2)); logZ=lse(F.values()); yy=y@y
print("uncentred y: minQ-yTy/(n+1)=",min(score_parts(X,y,S)[1] for S in F)-yy/(n+1)," logZ<=logB:",logZ<=logCn(n)-(a0+n/2)*math.log(2*b0+yy/(n+1)))
