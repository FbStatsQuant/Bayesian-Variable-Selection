import numpy as np
rng=np.random.default_rng(7)
# 1. alpha_0 arithmetic: feasible rho iff 1/(4a) < (1/2-1/(2a))/15
for a in [8.4,8.5,8.5001,9,20]:
    print("alpha",a,"feasible",1/(4*a) < (0.5-1/(2*a))/15)
# 2. one-factor: e = r - sum lam xi ; ||lam||_1<=1/b_lo ; Var(r)<=Var(e)
blo,bbar=0.3,0.95; worst=0
for _ in range(20000):
    g=rng.integers(2,60); b=np.where(rng.random(g)<0.2,0,rng.uniform(blo,bbar,g))
    l=0; A=np.arange(1,g)[rng.random(g-1)<rng.random()]
    if len(A)==0: continue
    S=np.outer(b,b)+np.diag(1-b**2)
    beta=np.linalg.solve(S[np.ix_(A,A)],S[A,l])
    lam=beta*np.sqrt(1-b[A]**2)
    worst=max(worst,np.abs(lam).sum()*blo)
    tau2=S[l,l]-S[A,l]@beta
    rho2=(b[l]-beta@b[A])**2+(1-b[l]**2)
    assert abs(tau2-(rho2+lam@lam))<1e-9
print("one-factor max ||lam||_1 * b_lo =",worst,"(<=1 required)")
# 3. CT_d on irregular separated 2-D sites (Sigma branch), check |A^-1_ij| <= (2/alpha) e^{-t* d}
def tstar(alpha,K,a,d,M=4000):
    m=np.arange(1,M)
    S=lambda t: K*np.sum((2*m+3.0)**d*np.exp(-(a-t)*m)*(1-np.exp(-t*(m+1))))
    lo,hi=0,a*(1-1e-9)
    for _ in range(100):
        mid=(lo+hi)/2
        if S(mid)<=alpha/2: lo=mid
        else: hi=mid
    return lo
pts=[]
while len(pts)<300:
    x=rng.uniform(0,25,2)
    if all(np.linalg.norm(x-y)>=1 for y in pts): pts.append(x)
P=np.array(pts); D=np.linalg.norm(P[:,None]-P[None],axis=2)
a=1/1.5; Sig=np.exp(-a*D); lam=np.linalg.eigvalsh(Sig).min()
ts=tstar(lam,1.0,a,2); Ai=np.linalg.inv(Sig)
ratio=np.max(np.abs(Ai)/((2/lam)*np.exp(-ts*D)))
print("irregular 2D: lam_min",round(lam,3),"t*",ts,"max ratio",ratio)
# 4. Lemma BC: polynomial Toeplitz alpha=3, conditional cov * (1+d)^alpha for random U (|U|<=15)
p=400; al=3.0; d=np.abs(np.subtract.outer(np.arange(p),np.arange(p)))
Sig=(1+d)**(-al)*0.5; np.fill_diagonal(Sig,1); print("Toeplitz lam_min",np.linalg.eigvalsh(Sig).min())
mx=0
for _ in range(3000):
    U=rng.choice(p,rng.integers(0,16),replace=False); rest=np.setdiff1d(np.arange(p),U)
    j,k=rng.choice(rest,2,replace=False)
    if len(U):
        C=Sig[np.ix_([j,k],[j,k])]-Sig[np.ix_([j,k],U)]@np.linalg.solve(Sig[np.ix_(U,U)],Sig[np.ix_(U,[j,k])])
    else: C=Sig[np.ix_([j,k],[j,k])]
    mx=max(mx,abs(C[0,1])*(1+abs(j-k))**al)
print("BC: max |condcov|*(1+d)^alpha =",mx)
