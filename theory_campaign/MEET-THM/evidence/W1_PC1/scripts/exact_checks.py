"""PC1: deterministic exhaustive small designs, exact sums, fixed seeds. No simulation of asymptotic proofs."""
import itertools, math, json
from pathlib import Path
import numpy as np
from scipy.special import logsumexp, gammaln
from scipy.cluster.hierarchy import linkage
OUT={}
def models(p,K): return [tuple(s) for k in range(K+1) for s in itertools.combinations(range(p),k)]
def lw(p,k): return -math.log(2)-gammaln(2*p)+gammaln(k+1)+gammaln(2*p-k)
def score(G,z,Y,n,S):
    if not S:return 0.,0.
    ix=np.ix_(S,S);gs=G[ix];zs=z[list(S)];h=(n+1)*gs+np.eye(len(S))
    x=n*zs@np.linalg.solve(h,zs)/(2*.01+Y)
    return -.5*(np.linalg.slogdet(h)[1]-np.linalg.slogdet(gs+np.eye(len(S)))[1])-(.01+n/2)*np.log1p(-x),x

def setup(n,p,blocks,rho,eps,seed=17,beta=None,null_y=False):
    rng=np.random.default_rng(seed);Sig=np.full((p,p),eps)
    for b in blocks:Sig[np.ix_(b,b)]=rho
    np.fill_diagonal(Sig,1.)
    Z=rng.normal(size=(n,p+1));Z-=Z.mean(0);U=np.linalg.qr(Z)[0]
    X=np.sqrt(n-1)*U[:,:p]@np.linalg.cholesky(Sig).T
    beta=np.zeros(p) if beta is None else np.asarray(beta)
    y=U[:,p]*np.sqrt(n-1) if null_y else X@beta+U[:,p]*np.sqrt(n-1)
    y-=y.mean(); y/=y.std(ddof=1)
    G=X.T@X; z=X.T@y;Y=y@y;K=min(p,n//2);ss=models(p,K)
    l0=[];d=[];ds=[];etas=[];xbars=[]
    for s in ss:
        f,x=score(G,z,Y,n,s);parts=[tuple(j for j in s if j in b) for b in blocks]
        sc=[score(G,z,Y,n,t) for t in parts];xb=sum(t[1] for t in sc)
        l0.append(lw(p,len(s))+sum(t[0] for t in sc));d.append(f-sum(t[0] for t in sc));xbars.append(xb)
        ds.append((.01+n/2)*(sum(np.log1p(-t[1]) for t in sc)-np.log1p(-xb)) if xb<1 else np.nan)
        if not s:etas.append(0);continue
        R=Sig[np.ix_(s,s)];A=np.zeros_like(R)
        for b in blocks:
            for i,j in enumerate(s):
                for k,l in enumerate(s):
                    if j in b and l in b:A[i,k]=R[i,k]
        Ah=np.linalg.inv(np.linalg.cholesky(A));E=Ah@(R-A)@Ah.T;e=np.linalg.norm(E,2);F=np.sum(E*E)
        etas.append((.01+n/2)*e*xb/(1-e-xb)+F/(4*(1-e)) if e<1-xb else np.inf)
    return dict(n=n,p=p,blocks=blocks,Sig=Sig,X=X,y=y,G=G,z=z,Y=Y,ss=ss,l0=np.array(l0),d=np.array(d),ds=np.array(ds),eta=max(etas),xb=max(xbars))
def L(l0,d,t):return logsumexp(l0+t*d)
def lc(l0,d,u,v):return L(l0,d,2*v-u)+L(l0,d,u)-2*L(l0,d,v)
def grid(l0,d,thr=.9,targets=(1.,),cap=1000):
    out=[0.];rs=[]
    while out[-1]<1:
        u=out[-1];b=next((t for t in targets if t>u),None)
        if b is None:return out,rs,'no_target'
        if lc(l0,d,u,b)<=-math.log(thr):v=b
        else:
            lo,hi=u,b
            for _ in range(60):
                mid=(lo+hi)/2
                if lc(l0,d,u,mid)<=-math.log(thr):lo=mid
                else:hi=mid
            v=lo
        if v>=1-1e-12:v=1.
        rv=math.exp(-lc(l0,d,u,v))
        if v<=u or rv<thr-2e-13:return out,rs,'validation'
        out.append(v);rs.append(rv)
        if len(rs)>cap:return out,rs,'too_many'
    return out,rs,'ok'

# Real method budgets: p=8 -> B=2, K=8, hence 256 states (not K=4 / 163 states).
own=[]
for eps in (1e-5,1e-4,.001):
    b=np.zeros(8);b[0]=.25;b[4]=.2
    a=setup(40,8,[[0,1],[2,3],[4,5],[6,7]],.6,eps,beta=b)
    l0,d,ds=a['l0'],a['d'],a['ds']; eta=a['eta'];etaD=(7*eps/.4)
    explicit=8*math.log(1/(1-etaD))+(20.01)*math.log(1/(1-etaD*a['xb']/((1-etaD)*(1-a['xb']))))
    # actual complete-linkage cut at B=2
    dd=1-np.abs(a['Sig']);cond=dd[np.triu_indices(8,1)];tree=linkage(cond,method='complete')
    def cut(i):
        if i<8:return [[i]]
        row=tree[i-8];
        if row[3]<=2:
            def leaves(j):return [j] if j<8 else leaves(int(tree[j-8,0]))+leaves(int(tree[j-8,1]))
            return [leaves(i)]
        return cut(int(row[0]))+cut(int(row[1]))
    recovered=cut(14)
    pilot=(.15,.3,.55,.8,1.)
    g,rs,status=grid(l0,d,targets=pilot)
    q=lambda t:np.exp(l0+t*d-L(l0,d,t))
    idx=a['ss'].index((0,4));m=min(q(0)[idx],q(2)[idx]);errs=[]
    V=np.array([len(s)<=2 for s in a['ss']]);av=lambda t:q(t)[V].sum()
    for u,v in zip(g[:-1],g[1:]):
        c=lc(l0,d,u,v);cv=lc(l0[V],d[V],u,v)
        errs.append(abs(math.exp(-c)-math.exp(-cv)*av(u)*av(2*v-u)/av(v)**2))
        assert c<=-2*math.log(m)+1e-10
        assert abs(c-lc(l0,ds,u,v))<=4*v*eta+1e-10
    assert np.max(abs(d-ds))<=eta+1e-10
    assert np.max(abs(d-ds))<=explicit+1e-10
    own.append(dict(eps=eps,states=len(d),B=2,K=8,groups=recovered,eta_A=eta,eta_D=explicit,discrepancy=float(max(abs(d-ds))),ubar=a['xb'],grid=g,min_ESS=min(rs),grid_status=status,coverage_error=max(errs),m=m))
OUT['own_correlated']=own
# A.C9(c): BO variance zero, actual variance strictly positive, all hypotheses hold.
a=setup(8,2,[[0],[1]],0,.2,null_y=True)
c=lc(a['l0'],a['d'],0,1);OUT['A_variance_cex']=dict(n=8,p=2,eps=.2,eta=a['eta'],d=a['d'].tolist(),ds=a['ds'].tolist(),chi2=float(np.expm1(c)),BO_chi2=float(np.expm1(lc(a['l0'],a['ds'],0,1))))
assert np.expm1(c)>1e-8
# D.M10(iii): compare identical true/BO bridges satisfying the looser |e|<=eta hypothesis.
l0=np.log([.999,.001]);d=np.array([0.,10.]);eta=.01
counts=[len(grid(l0,d,thr=t)[1]) for t in (.9*math.exp(4*eta),.9,.9*math.exp(-4*eta))]
OUT['D_sandwich_abstract']=dict(eta=eta,thresholds=[.9*math.exp(4*eta),.9,.9*math.exp(-4*eta)],counts=counts)
# Production pilot endpoints: flat discrepancy needs only 1 free interval but grid retains 4.
g,rs,st=grid(np.log([.5,.5]),np.zeros(2),targets=(.25,.5,.75,1.))
OUT['coded_not_global_shortest']=dict(grid=g,stages=len(rs),unconstrained_min=1,sd=0.)
# Duplicate model-space law: group inclusion ->1 need not mean one inclusion.
# n->infinity, p=2, identical strong signal columns: D(single)=n; D(pair)=(2n^2-1)/(2n-1) ~ n.
# With fixed nonzero noise and sample R^2->1/2, BF(pair)/BF(single)->1; the pair keeps mass 1/3.
dups=[]
for n in (40,400,4000,40000):
    G=(n-1)*np.ones((2,2));z=np.sqrt(.5)*(n-1)*np.ones(2);ss=models(2,2)
    logp=np.array([lw(2,len(s))+score(G,z,n-1,n,s)[0] for s in ss]);p=np.exp(logp-logsumexp(logp))
    dups.append(dict(n=n,pi=p.tolist(),PIP=float(p[1]+p[3]),group=1-float(p[0])))
OUT['duplicates']=dups
# Strict local maximum fails with ties: y orthogonal duplicate x, tune so singletons tie above null, while pair below.
# Easier cap K=1 at n=3 gives singleton tie, choose y=x; local best may instead empty, so n=3 high enough? search.
for n in (3,4,5,6,8,12,20):
    G=(n-1)*np.ones((2,2));z=(n-1)*np.ones(2);ss=models(2,min(2,n//2));f={s:lw(2,len(s))+score(G,z,n-1,n,s)[0] for s in ss}
    if f[(0,)]>f[()] and (len(ss)==3 or f[(0,)]>=f[(0,1)]):
        OUT['strict_local_cex']=dict(n=n,K=min(2,n//2),scores={str(k):v for k,v in f.items()});break
# TV/KL restricted law, finite-R bounds, singleton identity, KL lower bound exhaustive finite cases.
maxerr=0
for p in (2,4,8):
    a=setup(20,p,[[i] for i in range(p)],0,.001,null_y=True)
    l0=a['l0'];d=a['d'];pi0=np.exp(l0-logsumexp(l0));pi=np.exp(l0+d-logsumexp(l0+d));q2=np.exp(l0+2*d-logsumexp(l0+2*d));idx=1
    chi=np.sum(pi*pi/pi0)
    assert np.max(abs(chi-pi*pi/(pi0*q2)))<1e-9
    kl=np.sum(pi*np.log(pi/pi0));lb=pi[idx]*math.log(1/pi0[idx])-math.log(2);assert kl>=lb-1e-10
    mask=np.arange(len(pi))%2==0;pt=pi[mask].sum();r=np.where(mask,pi/pt,0)
    assert abs(.5*np.sum(abs(r-pi))-(1-pt))<1e-12
    assert abs(np.sum(r[mask]*np.log(r[mask]/pi[mask]))+math.log(pt))<1e-12
OUT['finite_algebra_checks']='PASS, p=2,4,8; singleton chi2, Lemma KL, restricted TV/KL'
# Bin packing table bound claimed <= p*2^B/B fails at p=B+1, leftover singleton.
OUT['table_bound_cex']=dict(p=5,B=4,blocks=[4,1],table_scores=2**4+2,claimed=5*2**4/4)
# More effective actual B=3 at p=10; blocks [3,3,3,1]: 26 <=26.66; B=4,p=17 [4,4,4,4,1]:66<=68. Bound holds for B>=3 except tiny blocks. enumerate arbitrary allowed sizes.
for B in range(1,17):
    if B/(2**B)<.5:continue
    # x=1 gives 2 > 2^B/B only B=3? 8/3>2, B=2 equality, B=1 equality.
OUT.pop('table_bound_cex') # 2^k/k <=2^B/B for all integer 1<=k<=B, so sum bound is valid.
print(json.dumps(OUT,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(OUT,indent=2)+'\n')
# Additional literal-statement counterexamples, same fixed seed.
# Weak-signal duplicate columns make tied singleton modes exceed null and pair.
for n in (20,40,100):
    for r2 in np.linspace(.05,.95,91):
        G=(n-1)*np.ones((2,2));z=np.sqrt(r2)*(n-1)*np.ones(2);ss=models(2,2)
        f={s:lw(2,len(s))+score(G,z,n-1,n,s)[0] for s in ss}
        if f[(0,)]>f[()] and f[(0,)]>f[(0,1)]:
            OUT['tied_local_and_permutation_cex']=dict(n=n,r2=float(r2),scores={str(k):v for k,v in f.items()},point='singleton is certified but tied with swap; index tie rule breaks equivariance in law');break
    if 'tied_local_and_permutation_cex' in OUT:break
# Actual finite BVS example for reversed D sandwich, with every D matrix hypothesis.
for eps in (1e-6,1e-5,1e-4):
    for amp in np.linspace(.25,2.,36):
        beta=np.zeros(8);beta[0]=amp;beta[4]=amp
        a=setup(40,8,[[0,1],[2,3],[4,5],[6,7]],.6,eps,beta=beta)
        delta=7*eps/.4;ub=a['xb'];r=delta*ub/((1-delta)*(1-ub))
        if ub>=1 or r>=1:continue
        eta=8*np.log(1/(1-delta))+20.01*np.log(1/(1-r))
        if .9*np.exp(4*eta)>=1:continue
        counts=[len(grid(a['l0'],a['ds'],thr=.9*np.exp(4*eta))[1]),len(grid(a['l0'],a['d'])[1]),len(grid(a['l0'],a['ds'],thr=.9*np.exp(-4*eta))[1])]
        if counts[0]>counts[1] or counts[1]>counts[2]:
            OUT['D_sandwich_BVS_cex']=dict(n=40,p=8,B=2,K=8,eps=eps,amp=float(amp),ubar=ub,delta=delta,eta=float(eta),counts=counts);break
    if 'D_sandwich_BVS_cex' in OUT:break
# Logical support/norm/tilt counterexamples, exact finite laws.
OUT['KL_reverse_exception']='T=Omega implies KL(pi||pi_T)=0, not infinity.'
OUT['bounded_h_norm_cex']=dict(pi=[.9,.1],T=[0],h=[0,100],delta=.1,error=10.,claimed_2delta=.2)
OUT['Lambda_not_length']=dict(pi0=[.5,.5],d=[10,10],Lambda=10,J=0,length=0)
# B.N: local alternative in BO has alpha=Lambda_b=0, theta_n=n^(-1/2), no cancellation, start not concentrated.
# At n increasing, one-signal singleton logBF= -0.5 log n + O(1), prior odds bounded, so pi0(S0)->0.
OUT['B_necessity_cex']='BO, fixed p=2, beta=(n^(-1/2),0), sigma=1, G/R/SE; no leakage/cancellation; logBF(signal)=-.5log n+O_P(1).'
Path(__file__).with_suffix('.json').write_text(json.dumps(OUT,indent=2)+'\n')
print('ADDITIONS',json.dumps({k:OUT[k] for k in OUT if k.endswith('_cex') or k=='Lambda_not_length'},indent=2))

# Explicit trivial-bridge counterexample emitted as evidence, not just an available helper.
a=setup(8,2,[[0],[1]],0,0,null_y=True)
OUT['A_never_trivial_cex']=dict(n=8,p=2,eps=0,z=a['z'].tolist(),d=a['d'].tolist(),max_abs_d=float(max(abs(a['d']))))
assert max(abs(a['d']))<1e-12
Path(__file__).with_suffix('.json').write_text(json.dumps(OUT,indent=2)+'\n')
