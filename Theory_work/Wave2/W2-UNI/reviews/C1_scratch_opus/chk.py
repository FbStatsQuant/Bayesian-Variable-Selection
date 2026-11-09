import numpy as np, itertools
rng=np.random.default_rng(7)
p=9
# non-block Psi: AR(1)-like with non-unit diag, then make Sigma correlation: choose lambda, then Psi = Sigma - lam lam^T must be PD
idx=np.arange(p)
R=0.5**np.abs(idx[:,None]-idx[None,:])
lam=rng.uniform(0.2,0.6,p)*rng.choice([-1,1],p)
# Psi with diag 1-lam^2: scale R
d=np.sqrt(1-lam**2)
Psi=(d[:,None]*R*d[None,:])
Sig=np.outer(lam,lam)+Psi
assert np.allclose(np.diag(Sig),1)
print("lam_min Psi",np.linalg.eigvalsh(Psi).min())
def inn(M,T,l,x):
    T=list(T)
    if not T: return x[l]/np.sqrt(M[l,l])
    c=np.linalg.solve(M[np.ix_(T,T)],M[T,l]); v=M[l,l]-M[l,T]@c
    return (x[l]-c@x[T])/np.sqrt(v)
maxerr=0;viol=0;cnt=0
kp=0; cG=np.inf
for r in range(1,p+1):
    for T in itertools.combinations(range(p),r):
        T=list(T); sT=lam[T]@np.linalg.solve(Psi[np.ix_(T,T)],lam[T]); cG=min(cG,sT/len(T))
for T_r in range(0,p):
  for T in itertools.combinations(range(p),T_r):
    T=list(T)
    for l in set(range(p))-set(T):
        if T:
            b=np.linalg.solve(Psi[np.ix_(T,T)],Psi[T,l]); psi=Psi[l,l]-Psi[l,T]@b; lt=lam[l]-b@lam[T]
        else: psi=Psi[l,l]; lt=lam[l]
        kp=max(kp,abs(lt)/np.sqrt(psi))
print("kappa'",kp,"c_G singletons",cG,"kappa",kp/np.sqrt(cG))
for rep in range(200):
    xi0=rng.standard_normal(); zeta=np.linalg.cholesky(Psi)@rng.standard_normal(p); g=lam*xi0+zeta
    for _ in range(30):
        r=rng.integers(0,p); T=list(rng.choice(p,r,replace=False)); l=rng.choice(list(set(range(p))-set(T)))
        Z=inn(Sig,T,l,g)
        if T:
            b=np.linalg.solve(Psi[np.ix_(T,T)],Psi[T,l]); psi=Psi[l,l]-Psi[l,T]@b; lt=lam[l]-b@lam[T]
            Xi=(zeta[l]-b@zeta[T])/np.sqrt(psi); w=np.linalg.solve(Psi[np.ix_(T,T)],lam[T]); s=lam[T]@w
            F=(w@zeta[T])/np.sqrt(s); W=(xi0-np.sqrt(s)*F)/np.sqrt(1+s)
        else:
            psi=Psi[l,l]; lt=lam[l]; Xi=zeta[l]/np.sqrt(psi); s=0; W=xi0; F=0
        Zd=(np.sqrt(psi)*Xi+lt/np.sqrt(1+s)*W)/np.sqrt(psi+lt**2/(1+s))
        maxerr=max(maxerr,abs(Z-Zd)); cnt+=1
        bound=abs(Xi)+kp*abs(xi0)+(kp*abs(F)/np.sqrt(s) if T else 0)
        if abs(Z)>bound+1e-12: viol+=1
print("pairs",cnt,"identity maxerr",maxerr,"(b) violations",viol)
# block CS check c_G = c_min
rb,rw=0.3,0.7; gs=3; G=3; pp=gs*G
H=np.kron(np.eye(G),np.ones((gs,gs))); Ps=(rw-rb)*H+(1-rw)*np.eye(pp); la=np.sqrt(rb)*np.ones(pp)
best=np.inf
grp=np.repeat(np.arange(G),gs)
for r in range(1,pp+1):
  for T in itertools.combinations(range(pp),r):
    T=list(T); s=la[T]@np.linalg.solve(Ps[np.ix_(T,T)],la[T]); h=len(set(grp[T])); best=min(best,s/h)
print("blockCS c_G",best,"c_min",rb/(1-rb))
