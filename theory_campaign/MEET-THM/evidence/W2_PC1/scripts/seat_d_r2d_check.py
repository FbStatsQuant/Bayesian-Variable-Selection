# Seat D, Round 2 local check (<1 min, <=20 seeds). numpy only; exact enumeration of Omega.
# Part 1: PC1's D-epsilon replica (n=40,p=8, pairs, within .6, cross c): WS-eps (i),(ii), corrected (iii) order, C's D_*.
# Part 2: necessity scaling of d_X(S0)=d(S0)-d_sigma(S0) vs the prediction -n*eps*beta*beta'/sigma^2.
import numpy as np, itertools, math
from math import comb
def lse(a): m=a.max(); return m+math.log(np.exp(a-m).sum())
def make_X(n,Sig,rng):
    p=Sig.shape[0]; Z=rng.standard_normal((n,p)); Z-=Z.mean(0); U,_=np.linalg.qr(Z)
    return math.sqrt(n-1)*U@np.linalg.cholesky(Sig).T          # exact Gram X'X=(n-1)Sig, centred
def setup(X,y):
    n,p=X.shape; y=y-y.mean(); y/=y.std(ddof=1); a0=b0=0.01; nu=a0+n/2; Q=2*b0+y@y
    G=X.T@X; z=X.T@y; return n,p,nu,Q,G,z
def logBF(G,z,n,nu,Q,S):
    if not S: return 0.0,0.0
    S=list(S); Gs=G[np.ix_(S,S)]; H=(n+1)*Gs+np.eye(len(S)); zs=z[S]
    t=n*zs@np.linalg.solve(H,zs); D=np.linalg.slogdet(H)[1]-np.linalg.slogdet(Gs+np.eye(len(S)))[1]
    return -0.5*D-nu*math.log(1-t/Q), t/Q
def discrepancies(G,z,n,p,nu,Q,blocks,K):
    Gbd=np.zeros_like(G)
    for b in blocks: Gbd[np.ix_(b,b)]=G[np.ix_(b,b)]
    models=[S for k in range(K+1) for S in itertools.combinations(range(p),k)]
    lw=lambda k: -math.log(2)-math.log(comb(2*p-1,k))
    lg0=[];d=[];dbd=[];ub=[]
    for S in models:
        parts=[[j for j in S if j in b] for b in blocks]
        lr=[logBF(G,z,n,nu,Q,u)[0] for u in parts]
        lb,_=logBF(G,z,n,nu,Q,S); lbd,xbd=logBF(Gbd,z,n,nu,Q,S)
        lg0.append(lw(len(S))+sum(lr)); d.append(lb-sum(lr)); dbd.append(lbd-sum(lr)); ub.append(xbd)
    return models,np.array(lg0),np.array(d),np.array(dbd),max(ub),Gbd
def chi2(lg0,dd,u,v):
    L=lambda t: lse(lg0+t*dd)-lse(lg0)
    return math.exp(L(2*v-u)-2*L(v)+L(u))-1
def greedy(lg0,dd,theta):
    u=0.0;T=0
    while u<1:
        if 1/(1+chi2(lg0,dd,u,1.0))>=theta: return T+1
        lo,hi=u,1.0
        for _ in range(60):
            mid=(lo+hi)/2
            if 1/(1+chi2(lg0,dd,u,mid))>=theta: lo=mid
            else: hi=mid
        u=lo;T+=1
    return T
print("== Part 1: D-epsilon replica (PC1 design), seeds 0..4")
print("cross seed |  sup|d-dbd|   eta_D   D_*   osc_d  a  dA  dH  r | (ii)viol | T_bd(.9e^-4eta) T_true(.9) T_bd(.9e^4eta)")
n,p=40,8; blocks=[[0,1],[2,3],[4,5],[6,7]]; K=8
for c in (1e-5,1e-4,1e-3):
    for seed in range(5):
        rng=np.random.default_rng(seed)
        Sig=np.full((p,p),c)
        for b in blocks:
            for i in b:
                for j in b: Sig[i,j]=.6 if i!=j else 1.0
        X=make_X(n,Sig,rng); beta=np.zeros(p); beta[0]=.25; beta[4]=.2
        y=X@beta+rng.standard_normal(n); n_,p_,nu,Q,G,z=setup(X,y)
        models,lg0,d,dbd,ub,Gbd=discrepancies(G,z,n,p,nu,Q,blocks,K)
        kappa=1-.6; delta=(K-1)*c/kappa
        eta=K*math.log(1/(1-delta))+nu*math.log(1/(1-delta*ub/((1-delta)*(1-ub)))) if delta*ub<(1-delta)*(1-ub) else math.inf
        sup=np.max(np.abs(d-dbd)); osc=d.max()-d.min()
        # C's D_* on the full design (A_D=Gbd+I, H_D=(n+1)Gbd+I, E=G-Gbd)
        E=G-Gbd; AD=Gbd+np.eye(p); HD=(n+1)*Gbd+np.eye(p)
        def relnorm(M,Em):
            L=np.linalg.cholesky(M); Li=np.linalg.inv(L); return np.linalg.norm(Li@Em@Li.T,2)
        dA=relnorm(AD,E); dH=relnorm(HD,(n+1)*E); a=n*z@np.linalg.solve(HD,z)/Q
        r=dH*a/((1-dH)*(1-a)) if dH<1 and a<1 else math.inf
        bX=(K/2)*(-math.log(1-dA)-math.log(1-dH))-nu*math.log(1-r) if r<1 else math.inf
        Dstar=nu*a*a/(2*(1-a))+2*bX
        viol=0
        for (u,v) in [(0,.25),(0,.5),(0,1),(.25,.5),(.5,1),(.3,.8)]:
            lhs=math.log(1+chi2(lg0,d,u,v))-math.log(1+chi2(lg0,dbd,u,v))
            if abs(lhs)>4*v*sup+1e-9: viol+=1
        if eta<math.inf and .9*math.exp(4*eta)<1:
            Ts=(greedy(lg0,dbd,.9*math.exp(-4*eta)),greedy(lg0,d,.9),greedy(lg0,dbd,.9*math.exp(4*eta)))
        else: Ts=("n/a","n/a","n/a")
        print(f"{c:.0e} {seed} | {sup:8.4f} {eta:8.4f} {Dstar:7.2f} {osc:6.2f} {a:.3f} {dA:.1e} {dH:.1e} {r:.1e} | {viol} | {Ts}")
print("\n== Part 2: necessity scaling. Two blocks {0,1},{2,3}, within .5, all cross = eps, S0={0,2}, sigma=1, 3 seeds")
print("regime eps    n | d_X(S0)=d-dbd (mean over seeds) | pred -n*eps*b*b' | ratio | d_sigma(S0) | osc d")
blocks2=[[0,1],[2,3]]
for regime in ("fixedR2","sqrtn"):
    for eps in (.05,.1):
        for n in (100,400,1600,6400):
            vals=[];ds=[];oscs=[]
            for seed in range(3):
                rng=np.random.default_rng(10+seed); p=4
                Sig=np.full((p,p),eps)
                for b in blocks2:
                    for i in b:
                        for j in b: Sig[i,j]=.5 if i!=j else 1.0
                X=make_X(n,Sig,rng); bb=.5 if regime=="fixedR2" else n**-.25
                beta=np.array([bb,0,bb,0.]); y=X@beta+rng.standard_normal(n)
                n_,p_,nu,Q,G,z=setup(X,y)
                models,lg0,d,dbd,ub,Gbd=discrepancies(G,z,n,p,nu,Q,blocks2,p)
                i0=models.index((0,2)); vals.append(d[i0]-dbd[i0]); ds.append(dbd[i0]); oscs.append(d.max()-d.min())
            m=np.mean(vals); pred=-n*eps*bb*bb
            print(f"{regime:7s} {eps:.2f} {n:5d} | {m:9.3f} | {pred:9.3f} | {m/pred:5.2f} | {np.mean(ds):7.3f} | {np.mean(oscs):7.2f}")
