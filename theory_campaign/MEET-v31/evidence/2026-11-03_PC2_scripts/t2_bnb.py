# C4(a)/(b) branch-and-bound as in O-CERT cert_lib.R::bnb; C4(b) with and without isolating {Shat}; node counts.
import numpy as np, itertools, math, sys
sys.path.insert(0, __file__.rsplit('/',1)[0]); from pc2_common import *
rng=np.random.default_rng(20261104)
def bnb(T,Shat,U,mode,tau=-12.0,isolate=True):
    Fh=T.F(Shat); stack=[((),tuple(U))]; nodes=0; better=[]; rest=[]
    while stack:
        L,Up=stack.pop(); nodes+=1
        if len(L)>T.K: continue
        free=[j for j in Up if j not in L]
        FL=T.F(L)
        if FL>Fh and tuple(sorted(L))!=tuple(sorted(Shat)): better.append(L)
        if not free:
            if tuple(sorted(L))!=tuple(sorted(Shat)): rest.append(FL-Fh)
            continue
        contains_hat=set(L)<=set(Shat)<=set(Up)
        if mode=='opt' and T.Phi(L,Up)<=Fh: continue
        if mode=='mass' and T.M(L,Up)<=Fh+tau and not (isolate and contains_hat):
            rest.append(T.M(L,Up)-Fh); continue
        j=free[0]; stack.append((L,tuple(x for x in Up if x!=j))); stack.append((tuple(sorted(L+(j,))),Up))
    return nodes,better,lse(rest)
def design(n,p,kind):
    if kind=='signal': Xr=rng.standard_normal((n,p)); yr=Xr[:,:3]@np.array([1.,-.8,.6])+rng.standard_normal(n)
    elif kind=='weak': Xr=rng.standard_normal((n,p)); yr=0.35*Xr[:,0]+0.3*Xr[:,1]+rng.standard_normal(n)
    elif kind=='noise_corr': Z=rng.standard_normal((n,1)); Xr=Z+0.3*rng.standard_normal((n,p)); yr=rng.standard_normal(n)
    elif kind=='proxies': Z=rng.standard_normal((n,1)); Xr=Z+0.5*rng.standard_normal((n,p)); yr=Z[:,0]+0.8*rng.standard_normal(n)
    return std(Xr,yr)
print("design n p | exact pi(Shat|2^U) | C4(b) as written (Shat not isolated, tau=-12) | isolated | opt nodes / full tree")
viol=0
for kind in ['signal','weak','noise_corr','proxies']:
  for (n,p) in [(30,10),(60,12),(12,12)]:
    X,y=design(n,p,kind); T=Target(X,y); Fall=T.enum(); Shat=max(Fall,key=lambda S:(Fall[S],-len(S)))
    U=tuple(range(p)); exact=math.exp(Fall[Shat]-lse(Fall.values()))
    nO,bet,_=bnb(T,Shat,U,'opt'); assert not bet
    _,_,r1=bnb(T,Shat,U,'mass',isolate=False); _,_,r2=bnb(T,Shat,U,'mass',isolate=True)
    lb1=1/(1+math.exp(r1)); lb2=1/(1+math.exp(r2))
    viol+= (lb1>exact+1e-12)+(lb2>exact+1e-12)
    print(f"{kind:10s} {n:3d} {p:2d} | {exact:.4f} | {lb1:.4f} | {lb2:.4f} | {nO}/{2**(p+1)-1}")
print("violations of C4(b):",viol)
# cost: worst case over pure-noise, equicorrelated designs, U=[p], Shat = HPM
worst=0
for s in range(30):
    n=int(rng.integers(8,40)); p=12; X,y=design(n,p,['noise_corr','proxies','weak'][s%3]); T=Target(X,y)
    Fall=T.enum(); Shat=max(Fall,key=lambda S:(Fall[S],-len(S))); nO,_,_=bnb(T,Shat,tuple(range(p)),'opt')
    worst=max(worst,nO/(2**(p+1)-1))
print(f"max opt-tree fraction of full binary tree over 30 designs (p=12, U=[p]): {worst:.3f}")
