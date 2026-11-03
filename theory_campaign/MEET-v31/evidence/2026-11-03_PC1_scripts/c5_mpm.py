import sys; sys.path.insert(0, sys.argv[1]); from common import *
rng=np.random.default_rng(20261105)
worst=0; found=None; nviol=0; trials=0
for rep in range(60):
    n=int(rng.integers(15,40)); p=8; K=min(p,n//2)
    Xr=rng.standard_normal((n,p)); 
    if rep%2: Xr[:,1]=Xr[:,0]+rng.uniform(0.2,1.5)*rng.standard_normal(n)
    beta=np.zeros(p); s0=int(rng.integers(1,4)); beta[:s0]=rng.uniform(0.3,1.2,s0)*rng.choice([-1,1],s0)
    X,y=standardise(Xr,Xr@beta+rng.standard_normal(n))
    F=enum_F(X,y,K); keys=list(F); f=np.array([F[S] for S in keys]); lZ=lse(f); post=np.exp(f-lZ)
    S0=tuple(range(s0)); d1=1-post[keys.index(S0)]
    for t in range(40):
        trials+=1
        m=int(rng.integers(1,len(keys)))
        idx=set(rng.choice(len(keys),m,replace=False).tolist())|{keys.index(S0)}
        if t==0: idx=set(np.argsort(-f)[:4*p+1].tolist())|{keys.index(S0)}  # top store 40p+1 analog
        idx=sorted(idx); ZT=post[idx].sum()
        pipT=np.zeros(p)
        for i in idx:
            for j in keys[i]: pipT[j]+=post[i]
        pipT/=ZT
        out=[j for j in range(p) if j not in S0]; inn=list(S0)
        mx=max(pipT[out]) if out else 0
        worst=max(worst, mx-d1)
        if mx>d1+1e-12 or (inn and min(pipT[inn])<1-d1-1e-12): nviol+=1
        mpm=tuple(j for j in range(p) if pipT[j]>0.5)
        if 1/3<=d1<0.5 and mpm==S0 and found is None: found=(n,s0,d1,mx,rep)
print("trials",trials,"violations of PIP^T_j<=delta1 (j notin S0) or >=1-delta1 (j in S0):",nviol," max(PIP^T_out - delta1)=",worst)
print("instance with 1/3<=delta1<1/2 and MPM^T=S0 (n,s0,delta1,max out PIP^T,rep):",found)
# delta1 = 1/2 boundary: S0={0}, pi(S0)=1/2, pi(S0 minus 0 = empty)=1/2, T=Omega
print("boundary: pi({0})=pi({})=1/2 -> PIP_0 = 0.5, not >1/2, MPM = {} != S0; HPM tie -> smallest size -> {} != S0")
