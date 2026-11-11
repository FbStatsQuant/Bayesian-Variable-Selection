import numpy as np, math, itertools
rng=np.random.default_rng(7)
def Mmat(Xs,n):
    if Xs.shape[1]==0: return np.zeros((Xs.shape[0],)*2)
    G=Xs.T@Xs; H=(n+1)*G+np.eye(G.shape[0]); return n*Xs@np.linalg.solve(H,Xs.T)
def P(Xs):
    if Xs.shape[1]==0: return np.zeros((Xs.shape[0],)*2)
    return Xs@np.linalg.pinv(Xs)
worst=np.inf; cnt=0
for trial in range(3000):
    N=int(rng.integers(6,40)); n=N+1; p=int(rng.integers(3,7)); s0=int(rng.integers(1,3))
    X=rng.normal(size=(N,p))
    if rng.random()<0.4: X[:,p-1]=X[:,:2]@rng.normal(size=2)   # exact dependence
    if rng.random()<0.3: X[:,p-2]=X[:,0]+1e-3*rng.normal(size=N)
    X*=np.sqrt(N)/np.linalg.norm(X,axis=0)
    S0=list(range(s0)); th=rng.normal(size=s0)*rng.choice([0.05,1,5])
    G0=X[:,S0].T@X[:,S0]; lam=np.linalg.eigvalsh(G0).min()
    if lam<=1e-8: continue
    mu=X[:,S0]@th; e=rng.normal(size=N)*rng.choice([0.3,1,3]); y=mu+e
    gam=(1+1/lam)/(n+1)
    for k in range(0,p+1):
      for S in itertools.combinations(range(p),k):
        S=list(S)
        if set(S0)<=set(S): continue
        Sp=sorted(set(S)|set(S0))
        MS=Mmat(X[:,S],n); MSp=Mmat(X[:,Sp],n); M0=Mmat(X[:,S0],n)
        QS=y@(np.eye(N)-MS)@y; QSp=y@(np.eye(N)-MSp)@y
        LS=mu@(np.eye(N)-MS)@mu
        cross=e@(np.eye(N)-MS)@mu
        chi=e@(P(X[:,Sp])-P(X[:,S0]))@e
        Rn=gam*(y@P(X[:,S0])@y)
        lhs=QS-QSp; rhs=LS+2*cross-chi-Rn
        worst=min(worst,lhs-rhs); cnt+=1
        # D1(b), D1(d)
        PS=P(X[:,S])
        assert np.sum((MS@y-mu)**2) <= 2*e@PS@e+2*LS+1e-8
        assert abs(QS-e@e) <= e@PS@e+2*abs(cross)+LS+1e-8
print('E1 chain: min(lhs-rhs) over',cnt,'cases =',worst)
# A2 check: delta >= O0/(1+O0) on random small problems with coded target
def lchoose(a,k): return math.lgamma(a+1)-math.lgamma(k+1)-math.lgamma(a-k+1)
mins=np.inf
for trial in range(400):
    n=int(rng.integers(8,60)); p=int(rng.integers(2,7)); K=min(p,n//2); s0=int(rng.integers(0,min(K,3)+1))
    Xr=rng.normal(size=(n,p))
    if rng.random()<0.4 and p>=3: Xr[:,2]=Xr[:,0]+Xr[:,1]
    X=Xr-Xr.mean(0); X/=np.sqrt((X**2).sum(0)/(n-1))
    th=rng.normal(size=s0); yr=X[:,:s0]@th+rng.normal(size=n)
    y=yr-yr.mean(); y/=np.sqrt((y**2).sum()/(n-1))
    nu=0.01+n/2; lw=lambda k:-math.log(2)-lchoose(2*p-1,k)
    lF={}; lD={}
    for k in range(K+1):
        for S in itertools.combinations(range(p),k):
            Xs=X[:,list(S)]; G=Xs.T@Xs; H=(n+1)*G+np.eye(k)
            ld=(np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(k))[1]) if k else 0.0
            Q=y@y-(n*(Xs.T@y)@np.linalg.solve(H,Xs.T@y) if k else 0.0)
            lF[S]=lw(k)-0.5*ld-nu*math.log(0.02+Q); lD[S]=ld
    mx=max(lF.values()); Z=sum(math.exp(v-mx) for v in lF.values())
    S0=tuple(range(s0)); delta=1-math.exp(lF[S0]-mx)/Z
    O0=sum(math.exp(lw(len(S))-lw(s0)+0.5*(lD[S0]-lD[S])) for S in lF if len(S)>s0 and set(S0)<=set(S))
    mins=min(mins,delta-O0/(1+O0))
print('A2: min(delta - O0/(1+O0)) =',mins)
# D0 Hellinger inequality
worst=np.inf
for _ in range(200000):
    a,b=rng.normal(size=2)*rng.choice([0.1,1,5]); v,w=np.exp(rng.normal(size=2)*1.5)
    H2=1-math.sqrt(2*math.sqrt(v*w)/(v+w))*math.exp(-(a-b)**2/(4*(v+w)))
    worst=min(worst,(v/w-1)**2+(a-b)**2/(4*w)-H2)
print('D0: min(bound - H2) =',worst)
