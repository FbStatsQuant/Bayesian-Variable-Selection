"""Independent R11 matrix checks; evidence only, not an asymptotic proof."""
import itertools
import json
import math
import numpy as np
from scipy.special import gammaln


def subsets(xs):
    return [list(t) for k in range(len(xs)+1) for t in itertools.combinations(xs,k)]


def score(G,z,n,p,T):
    k=len(T)
    prior=-math.log(2)-gammaln(2*p)+gammaln(k+1)+gammaln(2*p-k)
    if not T:
        return prior-(n/2+.01)*math.log(n-1+.02)
    g=G[np.ix_(T,T)]; zz=z[T]; h=(n+1)*g+np.eye(k)
    q=n-1-n*(zz@np.linalg.solve(h,zz))
    ld=np.linalg.slogdet(h)[1]-np.linalg.slogdet(g+np.eye(k))[1]
    return prior-.5*ld-(n/2+.01)*math.log(q+.02)


def exact_algebra():
    rng=np.random.default_rng(111)
    n=173; p=8; lam=np.linspace(.1,.98,p); psi=1-lam**2; ell=lam/np.sqrt(psi)
    th=np.array([1.2,-.8,0,0,0,0,0,0]); eta=rng.normal(); xi=rng.normal(size=p)
    sig=np.outer(lam,lam)+np.diag(psi); g=lam*eta+np.sqrt(psi)*xi
    e2=g@np.linalg.solve(sig,g)+rng.chisquare(n-1-p)
    s2=((n-1)*(th@sig@th)+2*np.sqrt(n-1)*(th@g)+e2)/(n-1)
    z=((n-1)*(sig@th)+np.sqrt(n-1)*g)/np.sqrt(s2)
    aa=n*n-1; d2=aa*psi+1; eps=np.sqrt(aa*psi/d2); lp=eps*ell
    zeta=eps*(xi+np.sqrt(n-1)*np.sqrt(psi)*th); rho0=eta+np.sqrt(n-1)*(lam@th)
    lpp2=(n-1)*lam**2/((n-1)*psi+1)
    rho=eta-np.sum(eps[:2]**2*ell[:2]*xi[:2])+np.sqrt(n-1)*np.sum((1-eps[:2]**2)*lam[:2]*th[:2])
    allsets=subsets(range(p)); records={}
    for T in allsets:
        idx=tuple(T); D=1+np.sum(lp[T]**2); X=(lp[T]@zeta[T]-rho0)/D
        H=aa*sig[np.ix_(T,T)]+np.eye(len(T))
        quad=z[T]@np.linalg.solve(H,z[T]) if T else 0.
        L=np.linalg.slogdet(H)[1]-np.linalg.slogdet((n-1)*sig[np.ix_(T,T)]+np.eye(len(T)))[1]
        records[idx]=(D,X,quad,L)
    worst=dict(deletion=0.,addition=0.,drift=0.,determinant=0.,reduced_centre=0.)
    for T in allsets:
        D,X,quad,L=records[tuple(T)]
        if 0 in T and 1 in T:
            null=[i for i in T if i>=2]
            worst['reduced_centre']=max(worst['reduced_centre'],abs(X-(lp[null]@(eps[null]*xi[null])-rho)/D))
            Hbar=max(abs(xi[2:])); taus=zeta[null]-lp[null]*X
            if null:
                assert min(abs(taus))<=Hbar+abs(rho)/min(lp)+1e-12
                top=np.sort(xi[2:]**2)[::-1][:len(null)]
                assert abs(X)<=np.sqrt(np.mean(top))/min(lp)+abs(rho)+1e-12
        for j in T:
            V=[i for i in T if i!=j]; Dv,Xv,qv,Lv=records[tuple(V)]; tau=zeta[j]-lp[j]*X
            pred=(D/(D-lp[j]**2))*tau**2/(s2*(n+1))
            worst['deletion']=max(worst['deletion'],abs(quad-qv-pred))
            worst['drift']=max(worst['drift'],abs(Xv-X+lp[j]*tau/(D-lp[j]**2)))
            Dpp=1+np.sum(lpp2[T]); Dppv=1+np.sum(lpp2[V])
            ej=-math.log1p(n/d2[j])+math.log(D/Dv)-math.log(Dpp/Dppv)
            worst['determinant']=max(worst['determinant'],abs(L-Lv-math.log(n+1)-ej))
            assert abs(ej)<=3/((n-1)*min(psi))
        for j in set(range(p))-set(T):
            V=sorted(T+[j]); _,Xv,qv,_=records[tuple(V)]; tau=zeta[j]-lp[j]*X
            pred=D/(D+lp[j]**2)*tau**2/(s2*(n+1))
            worst['addition']=max(worst['addition'],abs(qv-quad-pred))
            worst['drift']=max(worst['drift'],abs(Xv-X-lp[j]*tau/(D+lp[j]**2)))
    return dict(sets=len(allsets),max_absolute_errors=worst)


def uniform_scan(mode,seed):
    rng=np.random.default_rng(seed); n=10**8; p=10; N=n-3
    lam=np.linspace(.59,.61,p); psi=1-lam**2; ell=lam/np.sqrt(psi)
    eta=rng.normal(); xi=rng.normal(size=p); th=np.zeros(p); th[0]=1.2
    if mode=='exact':
        sig=np.outer(lam,lam)+np.diag(psi); g=lam*eta+np.sqrt(psi)*xi
        e2=g@np.linalg.solve(sig,g)+rng.chisquare(n-1-p)
        rawG=(n-1)*sig; noise=np.sqrt(n-1)*g
        phi2=None
    else:
        phi2=rng.chisquare(n-2); a=rng.normal(size=p)
        B=np.tril(rng.normal(size=(p,p)),-1)
        B[np.diag_indices(p)]=np.sqrt(rng.chisquare(N-np.arange(p)))
        W=B@B.T; v1=xi+ell*eta; v2=ell*np.sqrt(phi2)+a
        rawG=np.sqrt(psi)[:,None]*(np.outer(v1,v1)+np.outer(v2,v2)+W)*np.sqrt(psi)[None,:]
        e2=rng.chisquare(n-1); noise=np.sqrt(e2)*np.sqrt(psi)*v1
    sd=np.sqrt(np.diag(rawG)/(n-1)); G=rawG/np.outer(sd,sd)
    s2=(th@rawG@th+2*th@noise+e2)/(n-1)
    z=(rawG@th+noise)/sd/np.sqrt(s2)
    Ts=[[0]+K for K in subsets(range(1,p))]
    # Include truth-out neighbours in this independent D0 score cache.
    scores={tuple(T):score(G,z,n,p,T) for T in subsets(range(p))}
    mindel=float('inf'); maxadd=-float('inf'); maxtruth=-float('inf'); maxswapgap=-float('inf')
    maxdelta=0.; maxreferr=0.; swaps=0
    for T in Ts:
        f=scores[tuple(T)]; kept=T[1:]; outside=sorted(set(range(p))-set(T))
        dels=[scores[tuple(i for i in T if i!=j)]-f for j in kept]
        if dels: mindel=min(mindel,max(dels)/math.log(n))
        for l in outside:
            maxadd=max(maxadd,(scores[tuple(sorted(T+[l]))]-f)/math.log(n))
        maxtruth=max(maxtruth,scores[tuple(kept)]-f)
        for l in outside:
            maxtruth=max(maxtruth,scores[tuple(sorted(kept+[l]))]-f)
            for j in kept:
                gain=scores[tuple(sorted([i for i in T if i!=j]+[l]))]-f
                maxswapgap=max(maxswapgap,gain-max(dels)); swaps+=1
        if mode=='iid':
            A=W[np.ix_(T,T)]+np.outer(v2[T],v2[T]); inv=np.linalg.inv(A)
            omega=(inv@v1[T])/np.sqrt(np.diag(inv))
            kappa=N/phi2; D=kappa+ell[T]@ell[T]; X=(ell[T]@xi[T]-kappa*eta)/D
            c0=xi[T]-ell[T]*X; diag0=1-ell[T]**2/D
            inv0=np.linalg.inv(N*np.eye(len(T))+phi2*np.outer(ell[T],ell[T]))
            maxreferr=max(maxreferr,float(np.max(abs(N*inv0@v1[T]-c0))))
            if kept: maxdelta=max(maxdelta,float(np.max(abs(np.sqrt(N)*omega[1:]-c0[1:]/np.sqrt(diag0[1:])))))
    R=max(ell)/min(ell); AS=1/(2*(R*R+2*R))
    assert math.log(p)/math.log(n)<AS
    assert mindel>0 and maxadd<0 and maxtruth<0 and maxswapgap<0
    return dict(mode=mode,seed=seed,n=n,p=p,logp_logn=math.log(p)/math.log(n),A_S=AS,
                supersets=len(Ts),null_swaps=swaps,min_best_del_over_logn=mindel,
                max_add_over_logn=maxadd,max_truth_gain=maxtruth,max_null_swap_minus_best_del=maxswapgap,
                max_iid_null_delta=maxdelta,max_reference_identity_error=maxreferr)


if __name__=='__main__':
    print(json.dumps({'exact_algebra':exact_algebra()},indent=2),flush=True)
    for mode in ('exact','iid'):
        for seed in (112,113,114):
            print(json.dumps(uniform_scan(mode,seed)),flush=True)
