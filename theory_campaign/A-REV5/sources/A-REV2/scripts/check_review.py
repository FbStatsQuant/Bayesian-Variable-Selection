#!/usr/bin/env python3
"""Independent A-REV2 checks. Run only through owls_run -j 2.

Small Gram matrices and exhaustive state spaces (p <= 12); no source-script imports.
Raw sufficient statistics retain the Gaussian contrast law before response scaling.
"""
import itertools as it
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.special import logsumexp

OUT = Path(__file__).resolve().parents[1] / "results" / "checks.json"


def subsets(p, k=None):
    return [s for j in range(1 + (p if k is None else k)) for s in it.combinations(range(p), j)]


class Score:
    def __init__(self, n, R, zraw, yyraw):
        self.n, self.p = n, len(R)
        self.K = min(self.p, n // 2)
        self.G = (n - 1) * np.asarray(R)
        self.zraw, self.yyraw = np.asarray(zraw), float(yyraw)
        self.z = self.zraw * math.sqrt((n - 1) / yyraw)
        self.nu = n / 2 + .01

    @lru_cache(None)
    def parts(self, s):
        if not s:
            return 0., self.n - 1., self.yyraw
        idx = list(s)
        g = self.G[np.ix_(idx, idx)]
        h = (self.n + 1) * g + np.eye(len(s))
        ld = 2 * (np.log(np.diag(np.linalg.cholesky(h))).sum()
                  - np.log(np.diag(np.linalg.cholesky(g + np.eye(len(s))))).sum())
        q = self.n - 1 - self.n * self.z[idx] @ np.linalg.solve(h, self.z[idx])
        # Moore-Penrose is used only for duplicated-column deterministic examples.
        rss = self.yyraw - self.zraw[idx] @ np.linalg.pinv(g, rcond=1e-13) @ self.zraw[idx]
        return float(ld), float(q), float(rss)

    def bf(self, s):
        ld, q, _ = self.parts(tuple(s))
        return -.5 * ld - self.nu * math.log((.02 + q) / (.02 + self.n - 1))

    def logw(self, k):
        return -math.log(2) - sum(math.log((2 * self.p - i) / i) for i in range(1, k + 1))

    @lru_cache(None)
    def f(self, s):
        return self.bf(s) + self.logw(len(s))

    def neighbors(self, s):
        a, out = set(s), set()
        for j in range(self.p):
            b = a ^ {j}
            if len(b) <= self.K:
                out.add(tuple(sorted(b)))
        for j in s:
            for l in set(range(self.p)) - a:
                out.add(tuple(sorted(a - {j} | {l})))
        return sorted(out)

    def move(self, s):
        nb = self.neighbors(s)
        t = min(nb, key=lambda t: (-self.f(t), t)) if nb else None
        return t if t is not None and self.f(t) > self.f(s) + 1e-11 else None

    def path(self, s, ell=None):
        path, scored = [s], {s}
        while True:
            scored.update(self.neighbors(path[-1]))
            t = self.move(path[-1])
            if t is None:
                return path, True, scored
            if ell is not None and len(path) - 1 >= ell:
                return path + [t], False, scored  # final-scan return, not a moved centre
            path.append(t)


def sample(n, R, theta, rng):
    p = len(R)
    A = math.sqrt(n - 1) * np.linalg.cholesky(R).T
    v = A @ theta + rng.normal(size=p)
    return Score(n, R, A.T @ v, v @ v + rng.chisquare(n - 1 - p))


def prior_checks():
    count = 0
    for p in range(2, 33):
        q = [Fraction(math.comb(p, k), 2 * math.comb(2*p-1, k)) for k in range(p+1)]
        for n in (5, 8, 16, 40, 80):
            K = min(p, n // 2)
            for s in range(min(K, 4) + 1):
                w = Fraction(1, 2 * math.comb(2*p-1, s))
                tails = [sum(q[m+1:K+1], Fraction()) / w for m in range(K+1)]
                sharp = next(m for m in range(s, K+1) if tails[m]**2 * n**(s+2) <= 1)
                old = math.ceil((s * math.log(2*p) + (s+2)/2*math.log(n))/math.log(2))
                assert sharp <= min(K, old)
                for m in range(s, K+1):
                    gam = (m*(m-1)-(s-1)*(s-2))/(4*(p-1))
                    ub = math.comb(p, s)*2.**(s-m)*math.exp(-gam)
                    assert float(tails[m]) <= ub*(1+1e-12)
                    if s >= 1 and m < K:
                        lb = math.comb(p,s)*2.**(s-m-1)*math.exp(-(m*(m-1)-(s-1)*(s-2))/(4*(p-m)))
                        assert float(tails[m]) >= lb*(1-1e-12)
                    count += 1
    return {"tail_and_cutoff_cases": count, "failures": 0}


def logtails(n, p, s):
    K = min(p, n//2)
    # Past this upper cutoff there are >150 geometrically decaying terms;
    # all omitted mass is < 2^-150 relative to the threshold neighborhood.
    old = math.ceil((s*math.log(2*p)+(s+2)/2*math.log(n))/math.log(2))
    top = min(K, old + 160)
    lq = sum(math.log((2*p-i)/i) for i in range(1, s+1))
    terms = [lq]
    for k in range(top):
        terms.append(terms[-1] + math.log((p-k)/(2*p-1-k)))
    tail = np.full(top+1, -np.inf)
    for m in range(top-1, -1, -1):
        tail[m] = np.logaddexp(terms[m+1], tail[m+1])
    sharp = next(m for m in range(s, top+1) if tail[m] <= -(s+2)/2*math.log(n))
    return sharp, old


def thresholds():
    rows = []
    for p0 in (500, 1000):
        A = math.log(p0)/math.log(200)
        for n in (200, 130328, 2116048, 2457025, 25571897, 29755302):
            p = round(n**A)
            m, old = logtails(n,p,14)
            ca = 8+3*A
            delta = 3*math.sqrt(math.log(n)/(n-1)) + ca*(m+14)*math.log(n)/(n-1)
            eps = ((1+(0.02*n+1)/(n*n-1))/(1-delta)-1)*ca*math.log(n)/2 if delta < 1 else None
            q = math.sqrt(math.e*ca*math.log(n)/(4*(n+1)))*math.exp(eps) if eps is not None and eps < 700 else None
            rows.append(dict(p_at_200=p0,n=n,m_sharp=m,m_old=old,delta=delta,q_best_case=q,two_epsilon=None if eps is None else 2*eps))
    return rows


def duplicate_checks():
    rng = np.random.default_rng(730)
    rows=[]
    for n in (200,800,3200):
        p=n; K=n//2; N=n-1
        a=math.sqrt(N)+rng.normal(); yy=a*a+rng.chisquare(N-1)
        c2=N*N*a*a/yy
        k=np.arange(1,K+1,dtype=float)
        D=((n+1)*k*N+1)/(k*N+1)
        Q=N-n*k*c2/((n+1)*k*N+1)
        bf=np.r_[0,-.5*np.log(D)-(n/2+.01)*np.log((.02+Q)/(.02+N))]
        lq=[-math.log(2)]
        for i in range(K): lq.append(lq[-1]+math.log((p-i)/(2*p-1-i)))
        mass=np.exp(np.array(lq)+bf-logsumexp(np.array(lq)+bf))
        tails=np.r_[np.cumsum(mass[::-1])[::-1][1:],0.]
        assert bf[1] >= 0
        ratios=[]
        for m in range(min(16,K)):
            lb=2.**(-m-4)*math.exp(-m*(m-1)/(4*(p-m)))
            ratios.append(tails[m]/lb)
            assert tails[m] >= lb
        rows.append(dict(n=n,cutoff=int(np.flatnonzero(tails<=n**-.5)[0]),min_tail_over_bound=min(ratios)))
    return rows


def counterexamples():
    n=100; p=12; R=np.eye(p); R[0,1]=R[1,0]=.95
    theta=np.r_[3.,-2.8,np.zeros(p-2)]
    d=Score(n,R,(n-1)*R@theta,(n-1)*(theta@R@theta+1))
    s0=(0,1)
    r0=[(),(0,),(1,),s0]
    literal=True
    for s in r0:
        if s==s0:
            literal &= all(d.f(t)<d.f(s) for t in d.neighbors(s))
        else:
            missing=set(s0)-set(s)
            winners=[tuple(sorted(set(s)|{j})) for j in missing]
            literal &= any(all(d.f(t)>d.f(u) for u in d.neighbors(s) if u!=t) for t in winners)
    path,cert,_=d.path(())
    allS=subsets(p)
    prob=math.exp(d.f(s0)-logsumexp([d.f(s) for s in allS]))
    assert literal and path==[()] and cert and d.f(s0)>d.f(())
    # Independent reproduction of the first referee's posterior-miss / E_LS example.
    p2=9; r2=np.eye(p2); signal=np.r_[.5,.5,np.zeros(p2-2)]
    noise=np.r_[0.,0.,.45,np.zeros(p2-3)]
    d2=Score(n,r2,(n-1)*(signal+noise),(n-1)*(signal@signal+1))
    path2,cert2,_=d2.path((0,2))
    assert d2.f(s0)>d2.f((0,2)) and d2.f(path2[-1])>d2.f(s0) and cert2
    # Exact duplicate tie: singleton scores equal as algebraic expressions.
    r3=np.ones((2,2)); th3=np.array([.5,0.])
    d3=Score(n,r3,(n-1)*r3@th3,(n-1)*(th3@r3@th3+1))
    assert d3.f((0,))==d3.f((1,)) and d3.move(())==(0,) and d3.move((0,)) is None
    # Suppressor compatible with production tables and the SMC branch.
    # Two groups of four form first (.99 within > .95 between); B=4 separates them.
    p4=20; r4=np.eye(p4)
    for b in (range(4),range(4,8)):
        r4[np.ix_(b,b)]=.99*np.ones((4,4))+.01*np.eye(4)
    r4[:4,4:8]=.95*np.outer(r4[:4,0],r4[4,4:8]);r4[4:8,:4]=r4[:4,4:8].T
    th4=np.zeros(p4);th4[[0,4]]=[3.,-2.8]
    d4=Score(n,r4,(n-1)*r4@th4,(n-1)*(th4@r4@th4+1))
    table_sets=[]
    for b in (tuple(range(4)),tuple(range(4,8)),tuple(range(8,12)),tuple(range(12,16)),tuple(range(16,20))):
        table_sets += [tuple(b[j] for j in s) for s in subsets(4) if s]
    table_gap=max(d4.f(t)-d4.f(()) for t in table_sets)
    assert table_gap<0 and d4.move(()) is None and d4.f((0,4))>d4.f(())
    assert 2**20 > (5*512+4*2500)*20
    # The combination proxy gives TD_inf without TD_P under positive sparse eigenvalues.
    nc=3000; rc=np.eye(8);rc[0,2]=rc[2,0]=rc[1,2]=rc[2,1]=.85/math.sqrt(2)
    thc=np.r_[.3,.3,np.zeros(6)]
    dc=Score(nc,rc,(nc-1)*rc@thc,(nc-1)*(thc@rc@thc+1))
    regc=[s for s in subsets(8) if len(set(s)-{0,1})<=1]; regset=set(regc)
    pathc,_,_=dc.path(())
    infc=all(dc.path(s)[0][-1]==(0,1) and all(t in regset for t in dc.path(s)[0]) for s in regc)
    assert infc and dc.move(())==(2,)
    return dict(suppressor=dict(literal_TD_strict=bool(literal),gain_best_at_empty=d.f((0,))-d.f(()),truth_gain=d.f(s0)-d.f(()),posterior_truth=prob,path=path,certified=cert,
                               refutes_W3_R2_dichotomy=True),
                posterior_miss=dict(initial_gap=d2.f((0,2))-d2.f(s0),final_gap=d2.f(path2[-1])-d2.f(s0),path=path2),
                exact_tie=dict(singleton_gain=d3.f((0,))-d3.f(()),duplicate_add_gain=d3.f((0,1))-d3.f((0,)),TDP=True,D_empty=False),
                table_compatible_suppressor=dict(n=n,p=p4,B=4,max_nonempty_table_gain=table_gap,
                                                truth_gain=d4.f((0,4))-d4.f(()),empty_locally_certified=True,SMC_branch=True),
                combination_proxy=dict(n=nc,p=8,min_eigenvalue=float(np.linalg.eigvalsh(rc).min()),
                                       population_best_truth_gain=.3**2,population_proxy_gain=2*.85**2*.3**2,
                                       states=len(regc),TDinf=bool(infc),TDP=False,path_from_empty=pathc))


def t03_deterministic():
    rng=np.random.default_rng(734); counts=0; max_violation=-math.inf
    for rep in range(6):
        n=24;p=6;N=n-1
        X=rng.normal(size=(n,p));X-=X.mean(axis=0)
        if rep>=3: X[:,5]=X[:,4]+.03*rng.normal(size=n);X[:,5]-=X[:,5].mean()
        X*=math.sqrt(N)/np.linalg.norm(X,axis=0)
        y=rng.normal(size=n)+X[:,0]-.7*X[:,1];y-=y.mean();y*=math.sqrt(N)/np.linalg.norm(y)
        G=X.T@X;d=Score(n,G/N,X.T@y,y@y);truth=(0,1)
        phi2=float(np.linalg.eigvalsh(G[:2,:2]/N).min())
        eta=1/((n+1)*N*phi2);g0=float(np.linalg.eigvalsh(G).min())
        proj={};sm={}
        for s in subsets(p):
            xs=X[:,list(s)]
            proj[s]=xs@np.linalg.pinv(xs) if s else np.zeros((n,n))
            sm[s]=n*xs@np.linalg.solve((n+1)*xs.T@xs+np.eye(len(s)),xs.T) if s else np.zeros((n,n))
        for s in subsets(p):
            union=tuple(sorted(set(s)|set(truth)))
            missing=len(set(truth)-set(s));j=len(set(union)-set(truth))
            upper=n/(n+1)*(proj[union]-proj[truth]+eta*proj[truth])
            violation=float(np.linalg.eigvalsh(sm[union]-sm[truth]-upper).max())
            assert violation<1e-9;max_violation=max(max_violation,violation)
            detdiff=d.parts(union)[0]-d.parts(truth)[0]
            assert detdiff>=j*(math.log(n+1)-math.log1p(1/g0))-1e-9
            if missing:
                assert d.f(s)-d.f(union)<=missing*(math.log(2*p)+.5*math.log(n+1))+1e-9
            counts+=1
    return dict(designs=6,model_comparisons=counts,largest_B3_eigenvalue_violation=max_violation,failures=0)


def greedy_checks():
    rng=np.random.default_rng(731); counts=dict(datasets=0,centres=0,TDP=0,TDinf=0,certified_checks=0)
    for rep in range(16):
        p=8; R=.4**np.abs(np.subtract.outer(np.arange(p),np.arange(p)))
        theta=np.r_[(.35 if rep<8 else 1.5),-(.3 if rep<8 else 1.2),np.zeros(p-2)]
        d=sample(80,R,theta,rng); s0={0,1}; truth=(0,1)
        reg=[s for s in subsets(p) if len(set(s)-s0)<=1]
        regset=set(reg); phi=lambda s:len(set(s)^s0)
        L=d.move(truth) is None
        inf=L and all(d.move(s) is not None and d.move(s) in regset for s in reg if s!=truth)
        prog=L and all(d.move(s) is not None and phi(d.move(s))<phi(s) for s in reg if s!=truth)
        paths={s:d.path(s) for s in reg}
        reaches=all(v[0][-1]==truth and all(t in regset for t in v[0]) for v in paths.values())
        assert inf==reaches
        for s,(path,cert,scored) in paths.items():
            if inf:
                assert len(path)-1<=sum(d.f(t)>d.f(s) for t in reg)
            if prog:
                swaps=sum(phi(a)-phi(b)==2 for a,b in zip(path,path[1:]))
                assert len(path)-1==phi(s)-swaps
                assert all(set(s)&s0 <= set(t)&s0 and set(t)-s0<=set(s)-s0 for t in path)
                capped,certified,seen=d.path(s,3)
                assert capped[-1]==truth and certified and max(d.f(t) for t in seen)<=d.f(truth)+1e-10
                counts['certified_checks']+=1
        counts['datasets']+=1; counts['centres']+=len(reg); counts['TDP']+=int(prog); counts['TDinf']+=int(inf)
    counts['failures']=0
    return counts


def expansion_checks():
    rng=np.random.default_rng(732); rows=[]
    for n in (40,200,800):
        p=8; R=.5**np.abs(np.subtract.outer(np.arange(p),np.arange(p)))
        theta=np.array([1.,0,0,-.8,0,0,.6,0])
        d=sample(n,R,theta,rng)
        phi2=float(np.linalg.eigvalsh(R).min()); M=float(theta@R@theta)
        cstar=1/(8*(M+2))
        kap=(1+1/phi2)/(2*phi2*(n-1))+d.nu*(1.02+1/(n*phi2))/(cstar*n)
        count=0; worst=0.; ratio=0.; identerr=0.
        for t in subsets(p,2):
            ld,q,rss=d.parts(t)
            for l in set(range(p))-set(t):
                v=tuple(sorted(t+(l,))); ld1,q1,rss1=d.parts(v)
                rem=d.bf(v)-d.bf(t)+.5*math.log(n+1)+d.nu*math.log(rss1/rss)
                rssy,rssy1=(n-1)*rss/d.yyraw,(n-1)*rss1/d.yyraw
                eta=ld1-ld-math.log(n+1)
                rhs=-.5*eta-d.nu*(math.log1p((.02+q1-rssy1)/rssy1)-math.log1p((.02+q-rssy)/rssy))
                cert=(1+1/phi2)/(2*phi2*(n-1))+d.nu*(1.02+1/(n*phi2))/min(rssy,rssy1)
                assert abs(rem-rhs)<1e-9 and abs(rem)<=cert+1e-9
                worst=max(worst,abs(rem)); ratio=max(ratio,abs(rem)/cert); identerr=max(identerr,abs(rem-rhs)); count+=1
        rows.append(dict(n=n,pairs=count,max_abs_R=worst,kappa=kap,max_ratio_to_deterministic_certificate=ratio,identity_error=identerr))
    return rows


def masked_chain():
    rng=np.random.default_rng(733); rows=[]
    # Four groups of size 3, B=3. One linked pair (psi=.4 < rho=.7).
    p=12; R=np.eye(p)
    blocks=[tuple(range(j,j+3)) for j in range(0,p,3)]
    for b in blocks: R[np.ix_(b,b)]=.7*np.ones((3,3))+.3*np.eye(3)
    R[:3,3:6]=.4*np.outer(R[:3,0],R[3,3:6]); R[3:6,:3]=R[:3,3:6].T
    theta=np.zeros(p);theta[[0,3,6]]=[1.,-.4,1.]
    assert abs((R@theta)[3])<1e-14
    allS=subsets(p); ref=(0,6);truth=(0,3,6)
    for n in (100,400,1600):
        statistics=[]
        for _ in range(8):
            d=sample(n,R,theta,rng)
            lg={s:d.logw(len(s))+sum(d.bf(tuple(j for j in s if j in b)) for b in blocks) for s in allS}
            lz=logsumexp(list(lg.values()))
            E=d.bf((3,))+.5*math.log(n)
            rem=d.bf((3,))+.5*math.log(n+1)+d.nu*math.log(d.parts((3,))[2]/d.yyraw)
            assert abs((lg[truth]-lg[ref])-(d.logw(3)-d.logw(2)+d.bf((3,))))<1e-10
            phi2=float(np.linalg.eigvalsh(R).min()); M=float(theta@R@theta); cstar=1/(8*(M+2))
            kap=(1+1/phi2)/(2*phi2*(n-1))+d.nu*(1.02+1/(n*phi2))/(cstar*n)
            z=d.zraw[3]/math.sqrt(n-1)
            assert E>=-1-kap and E<=kap+d.nu*z*z/d.parts((3,))[2]
            statistics.append([math.exp(lg[ref]-lz),math.exp(lg[truth]-lz),lg[truth]-lz+math.log(p)+.5*math.log(n),E,rem])
        med=np.median(statistics,axis=0)
        rows.append(dict(n=n,reps=8,median_pi0_reference=med[0],median_pi0_truth=med[1],median_normalized_log_mass=med[2],median_E=med[3],median_chain_R=med[4]))
    return rows


def lemma_u_lower_counterexample():
    # delta=0 does not imply RSS_T is pure noise: omitted orthogonal signal remains.
    # Construct a point strictly inside E1--E4, using contrast sufficient statistics.
    n=1_000_000; N=n-1; L=5.; z2=65.; theta=np.array([1.,0.]); R=np.eye(2)
    zraw=np.array([N, math.sqrt(N*z2)])  # signal direction has zero noise projection
    d=Score(n,R,zraw,2*N)  # total noise energy N; residual energy N-z2
    kappa=1/N+d.nu*(1.02+1/n)/(n/24)
    vartheta=n**(-1/3)+L*math.log(n)/N
    correction=L*math.log(n)*(vartheta+3/n)/(1-vartheta)
    actual=d.bf((1,))+.5*math.log(n+1)
    claimed_lower=z2/2-kappa-correction
    assert z2 < L*math.log(n) and actual < claimed_lower
    assert N-z2 >= N*(1-vartheta) and d.yyraw<=6*n
    return dict(n=n,L=L,Z_squared=z2,delta=0.,kappa=kappa,vartheta_prime=correction,
                actual_log_BF_plus_half_log_n1=actual,claimed_C3_lower=claimed_lower,
                E1_E2_E3_E4_hold=True)


def main():
    result={}
    for name,fn in [('prior',prior_checks),('thresholds',thresholds),('duplicates',duplicate_checks),
                    ('counterexamples',counterexamples),('T03_deterministic',t03_deterministic),('greedy',greedy_checks),
                    ('expansion_and_U',expansion_checks),('chain',masked_chain),
                    ('U_C3_counterexample',lemma_u_lower_counterexample)]:
        result[name]=fn()
        print(name, json.dumps(result[name]), flush=True)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print('All asserted checks passed; results:',OUT,flush=True)


if __name__=='__main__':
    main()
