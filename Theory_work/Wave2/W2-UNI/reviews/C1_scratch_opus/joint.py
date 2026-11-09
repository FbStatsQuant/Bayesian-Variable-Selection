import numpy as np, itertools
def run(seed,p=9,kind="ar"):
    rng=np.random.default_rng(seed); idx=np.arange(p)
    R=0.5**np.abs(idx[:,None]-idx[None,:])
    lam=rng.uniform(0.2,0.6,p)*rng.choice([-1,1],p)
    d=np.sqrt(1-lam**2); Psi=d[:,None]*R*d[None,:]
    kp=0;cG=np.inf;kj=0
    for r in range(0,p):
        for T in itertools.combinations(range(p),r):
            T=list(T)
            if T:
                PT=Psi[np.ix_(T,T)]; s=lam[T]@np.linalg.solve(PT,lam[T]); cG=min(cG,s/len(T))
            for l in set(range(p))-set(T):
                if T:
                    b=np.linalg.solve(PT,Psi[T,l]); psi=Psi[l,l]-Psi[l,T]@b; lt=lam[l]-b@lam[T]
                else: psi=Psi[l,l]; lt=lam[l]
                k=abs(lt)/np.sqrt(psi); kp=max(kp,k)
                if T: kj=max(kj,k*np.sqrt(len(T)/s))
    return kp/np.sqrt(cG), kj
for s in range(4): print(run(s))
