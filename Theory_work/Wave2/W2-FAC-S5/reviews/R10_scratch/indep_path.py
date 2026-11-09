# R10 independent check: exact-Gram BCS scorer written from D0 (not bcs_core), complete-neighbour steepest ascent from [p],
# checks: path = pure null deletions to S0, strict endpoint, CC(delta) along the path, |tau|<=|A|+k0|e| bound.
import numpy as np, itertools, sys
from math import lgamma, log
def run(seed, n, q=5, J=6, rb=.3, rw=.7, truths=(0,5,10), th=(1.0,-0.7,0.5), sigma=1.0, delta=0.05):
    rng=np.random.default_rng(seed); p=q*J; b=rw-rb; d=1-rw
    grp=np.repeat(np.arange(J),q)
    Sig=rb*np.ones((p,p))+np.where(grp[:,None]==grp[None,:],b,0)+d*np.eye(p)
    h=np.sqrt(rb)*rng.standard_normal(); zeta=rng.standard_normal(J); xi=rng.standard_normal(p)
    y=np.sqrt(b)*zeta[grp]+np.sqrt(d)*xi; g=h+y
    r=rng.chisquare(n-1-p)
    theta=np.zeros(p); theta[list(truths)]=th
    quadg=g@np.linalg.solve(Sig,g)
    s2=(theta@Sig@theta*(n-1)+2*sigma*np.sqrt(n-1)*theta@g+sigma**2*(quadg+r))/(n-1)
    s=np.sqrt(s2); z=((n-1)*Sig@theta+sigma*np.sqrt(n-1)*g)/s
    a=n*n-1.; ap=n-1.; nu=.01+n/2
    def logw(k): return -log(2)-(lgamma(2*p)-lgamma(k+1)-lgamma(2*p-k))
    cache={}
    def F(S):
        S=tuple(sorted(S))
        if S in cache: return cache[S]
        if len(S)==0: val=logw(0)-nu*log(.02+(n-1))
        else:
            idx=list(S); SS=Sig[np.ix_(idx,idx)]
            ev=np.linalg.eigvalsh(SS)
            L=np.sum(np.log((a*ev+1)/(ap*ev+1)))
            Ht=SS+np.eye(len(idx))/a      # H = a*Ht
            quad=z[idx]@np.linalg.solve(Ht,z[idx])/a
            Q=(n-1)-n*quad
            val=logw(len(idx))-0.5*L-nu*log(.02+Q)
        cache[S]=val; return val
    S0=set(truths); T=set(range(p)); path=[]; ok=True
    def e_of(R):
        R=sorted(R)
        if not R: return h
        c=rb*np.ones(len(R)); return h-c@np.linalg.solve(Sig[np.ix_(R,R)],g[R])
    H=np.sqrt(2*log(2**q*p)+2*log(log(n))); k0=(1-rb)**-.5
    ccmin=np.inf; ccratio_e=0
    while True:
        k=len(T); Lam=log(n)+2*log((2*p-k)/(k+1))
        for Tp in [T]+[T-{j} for j in T-S0]:
            lhs=(H+k0*abs(e_of(Tp)))**2; ccmin=min(ccmin,(1-delta)*Lam-lhs)
            ccratio_e=max(ccratio_e,k0*abs(e_of(Tp))/H)
        f0=F(T); best=None
        nb=[]
        for j in T: nb.append(('del',j,None,T-{j}))
        for l in set(range(p))-T: nb.append(('add',None,l,T|{l}))
        for j in T:
            for l in set(range(p))-T: nb.append(('swap',j,l,(T-{j})|{l}))
        gains=[(F(S)-f0,tuple(sorted(S)),kind,j,l) for kind,j,l,S in nb]
        gains.sort(key=lambda t:(-t[0],t[1]))
        gbest=gains[0]
        if gbest[0]<=0: break
        if not(gbest[2]=='del' and gbest[3] not in S0): ok=False
        # margin of best non-null-deletion
        other=max(g_[0] for g_ in gains if not(g_[2]=='del' and g_[3] not in S0))
        path.append((len(T),gbest[2],gbest[0]/log(n),(gbest[0]-other)/log(n)))
        T=set(gbest[1])
    return ok and T==S0, T==S0, path, ccmin/log(n), ccratio_e
for n in [1e8,1e12]:
    for seed in range(4):
        ok,end,path,cc,cr=run(seed,n)
        mg=min(t[2] for t in path); mm=min(t[3] for t in path)
        print(f"n={n:.0e} seed={seed} pure_null_del_to_S0={ok} end_S0={end} steps={len(path)} min_gain/logn={mg:.3f} min_margin/logn={mm:.3f} CCmargin_min/logn={cc:.3f} max k0|e|/H={cr:.3f}")
