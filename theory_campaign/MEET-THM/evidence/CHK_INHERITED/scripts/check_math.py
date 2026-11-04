"""PC1 independent algebra checks; 10 fixed seeds, small finite enumerations.
Run from any directory; writes only beside this script.
"""
from pathlib import Path
from itertools import combinations
import json, math
import numpy as np
from scipy.special import logsumexp, gammaln

OUT=Path(__file__).resolve().parent
blocks=[np.array([0,1]),np.array([2,3]),np.array([4,5])]
models=[np.array(s,dtype=int) for k in range(7) for s in combinations(range(6),k)]

def fit(R,z,n,S):
    if len(S)==0:return 0.,0.
    G=(n-1)*R[np.ix_(S,S)]
    H=(n+1)*G+np.eye(len(S))
    ld=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(S)))[1]
    t=n*z[S]@np.linalg.solve(H,z[S])
    return ld,t

def invsqrt(M):
    v,U=np.linalg.eigh(M)
    return (U/np.sqrt(v))@U.T

def probs(a):return np.exp(a-logsumexp(a))

def logsecond(a,b):return logsumexp(2*a-b) # normalised log probabilities

res={'seeds':list(range(10)), 'bo_max_error':0.,'ws4_max_positive_violation':0.,
     'identity_max_error':0.,'ws7_max_positive_violation':0.,'orth':[]}
for seed in range(10):
    rng=np.random.default_rng(seed)
    n=80;p=6;nu=n/2+.01;Q=n-1+.02
    A=np.eye(p)
    for b in blocks:
        r=rng.uniform(-.6,.6);A[b[0],b[1]]=A[b[1],b[0]]=r
    E=rng.normal(size=(p,p));E=(E+E.T)/2
    for b in blocks:E[np.ix_(b,b)]=0
    C=invsqrt(A)@E@invsqrt(A)
    E*=.1/np.linalg.norm(C,2)
    z=rng.normal(size=p)*7
    # BO finite identities, Gamma MGF, positivity and pairwise upper bound.
    for S in models:
        ld,t=fit(A,z,n,S)
        ld_b=[];t_b=[]
        for b in blocks:
            l,v=fit(A,z,n,np.intersect1d(S,b));ld_b.append(l);t_b.append(v)
        xb=np.array(t_b)/Q; xs=t/Q
        assert xb.sum()<1
        d=nu*(np.log1p(-xb).sum()-np.log1p(-xs))
        pair=sum(xb[i]*xb[j] for i in range(3) for j in range(i+1,3))
        upper=nu*pair/(1-xb.sum())
        # Gamma shape nu, rate Q/2 gives exact log-MGF below.
        gamma_log=-sum(ld_b)/2-nu*np.log1p(-sum(t_b)/Q)
        bf_log=-ld/2-nu*np.log1p(-xs)
        err=max(abs(ld-sum(ld_b)),abs(t-sum(t_b)),abs(gamma_log-bf_log),max(-d,0),max(d-upper,0))
        res['bo_max_error']=max(res['bo_max_error'],float(err))
    # WS4 per-model estimates and bridges, with genuinely correlated epsilon=.1.
    all_d=[];all_ds=[];all_eta=[];g0=[]
    for S in models:
        ld,t=fit(A+E,z,n,S)
        ld_b=[];t_b=[]
        for b in blocks:
            l,v=fit(A,z,n,np.intersect1d(S,b));ld_b.append(l);t_b.append(v)
        xbar=sum(t_b)/Q;xs=t/Q
        if len(S):
            As=A[np.ix_(S,S)];Es=E[np.ix_(S,S)]
            Cs=invsqrt(As)@Es@invsqrt(As)
            eps=np.linalg.norm(Cs,2);F=np.linalg.norm(Cs,'fro')**2
            spectral=np.linalg.eigvalsh((A+E)[np.ix_(S,S)]).min()
            low=(1-eps)*np.linalg.eigvalsh(As).min()
        else:eps=F=0.;spectral=low=0.
        assert xbar<1-eps
        ds=nu*(sum(np.log1p(-np.array(t_b)/Q))-np.log1p(-xbar))
        dd=-(ld-sum(ld_b))/2
        df=-nu*np.log((1-xs)/(1-xbar))
        eta=nu*eps*xbar/(1-eps-xbar)+F/(4*(1-eps))
        d=-ld/2-nu*np.log1p(-xs)-sum(-l/2-nu*np.log1p(-v/Q) for l,v in zip(ld_b,t_b))
        v=max(0.,low-spectral,abs(t-sum(t_b))-eps/(1-eps)*sum(t_b),
              abs(dd)-F/(4*(1-eps)),abs(df)-nu*eps*xbar/(1-eps-xbar),
              abs(d-ds)-eta,abs(d-dd-df-ds)-1e-10)
        res['ws4_max_positive_violation']=max(res['ws4_max_positive_violation'],float(v))
        k=len(S)
        logw=-math.log(2)-gammaln(2*p)+gammaln(k+1)+gammaln(2*p-k)
        g0.append(logw+sum(-l/2-nu*np.log1p(-v/Q) for l,v in zip(ld_b,t_b)))
        all_d.append(d);all_ds.append(ds);all_eta.append(eta)
    d=np.array(all_d);ds=np.array(all_ds);g0=np.array(g0);eta=np.array(all_eta)
    for ix in [np.arange(len(models)),np.arange(0,len(models),2)]:
        l0=g0[ix]-logsumexp(g0[ix]);err=eta[ix].max()
        for v in [-1.,.5,1.,2.]:
            lv=g0[ix]+v*d[ix];lv-=logsumexp(lv)
            ls=g0[ix]+v*ds[ix];ls-=logsumexp(ls)
            gap=abs(logsecond(lv,l0)-logsecond(ls,l0))-4*abs(v)*err
            tv=.5*np.abs(np.exp(lv)-np.exp(ls)).sum()
            violation=max(0.,gap,tv-(1-np.exp(-2*abs(v)*err)))
            res['ws4_max_positive_violation']=max(res['ws4_max_positive_violation'],float(violation))
    # WS1, WS2, WS6(a-c), WS7(a,d) on arbitrary finite positive families.
    m=9;a=rng.normal(size=m);d=rng.normal(size=m)*2
    def lp(v):return a+v*d-logsumexp(a+v*d)
    l0,l1,l2=lp(0),lp(1),lp(2);p0,p1,p2=map(np.exp,[l0,l1,l2])
    L=logsecond(l1,l0)
    res['identity_max_error']=max(res['identity_max_error'],float(np.max(np.abs(2*l1-l0-l2-L))))
    ess=np.exp(-L);kl=np.sum(p1*(l1-l0));tv=.5*abs(p1-p0).sum()
    for s in range(m):
        vl=max(0.,ess-p0[s]/p1[s]**2,p1[s]*(-l0[s])-math.log(2)-kl,p1[s]-p0[s]-tv)
        res['ws7_max_positive_violation']=max(res['ws7_max_positive_violation'],float(vl))
        for theta in [.2,1.]:
            up=l1[s]-l0[s]+p1[s]/theta*np.expm1(-lp(1+theta)[s])
            res['ws7_max_positive_violation']=max(res['ws7_max_positive_violation'],float(max(0.,kl-up)))
    u=.2;v=.3;w=2*v-u;Lstep=logsecond(lp(v),lp(u));s=2
    # rho=actual ESS, so the necessary halving inequality must hold exactly.
    vl=(-lp(u)[s]-Lstep)/2-(-lp(v)[s])
    res['ws7_max_positive_violation']=max(res['ws7_max_positive_violation'],float(max(0.,vl)))
    # Exact ORTH calculation in n-1 contrast coordinates, no n x p matrix.
    n=65536;p=n-1;s0=2;nu=n/2+.01;Q=n-1+.02
    Y=rng.normal(size=n-1);Y[[0,16]]+=np.sqrt(n-1)*np.sqrt(2)
    sy2=Y@Y/(n-1);tj=(n-1)*Y**2/(n*sy2);t0=tj[[0,16]].sum()
    truthfree=np.ones(p,dtype=bool);truthfree[:32]=False
    b=tj[truthfree]/Q;a1=tj[truthfree]/(Q-t0);Z2=Y[truthfree]**2;r=.8;alpha=2
    prior=np.log((s0+1)/(2*p-s0-1))-.5*np.log(n)
    lc=prior-alpha*nu*np.log1p(-a1)+(alpha-1)*nu*np.log1p(-b)
    simple=prior+alpha*nu*a1-(alpha-1)*nu*b/(1-b)
    assert np.min(lc-simple)>-1e-10
    approx=prior+(1+(alpha-1)*r)*Z2/2
    M=Z2.max();N=len(Z2)
    res['orth'].append({'seed':seed,'max_logc':float(lc.max()),
        'max_expansion_error':float(abs(lc-approx).max()),
        'maximum_centered':float(M-2*np.log(N)+np.log(np.log(N))),
        'logc_bound_slack':float((lc-simple).min())})
# Counterexample to reading WS7(c)'s equality as terminal presence: N=2,
# pi0(S0)=1/2, resample twice with equal weights. Presence: 1/4+1/2*(3/4)=5/8.
res['ws7c_initial_presence']=.75
res['ws7c_after_one_multinomial_resampling']=.625
assert res['bo_max_error']<1e-9
assert res['ws4_max_positive_violation']<1e-9
assert res['identity_max_error']<1e-10
assert res['ws7_max_positive_violation']<1e-10
(OUT/'math_results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
