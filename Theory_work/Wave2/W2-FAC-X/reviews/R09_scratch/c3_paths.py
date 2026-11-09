# R09: exact delta_j(T) along production LS0 paths at extreme rho (not tested in N1X: rho in {0.3,0.7})
import sys, math, json, numpy as np
sys.path.insert(0, r"../../numerics")
import iid_core as ic
def run(n,p,rho,s0,seed):
    rng=np.random.default_rng(seed)
    lam=math.sqrt(rho); Lam=np.full(p,lam)
    beta=np.zeros(p); S0=list(rng.choice(p,s0,replace=False)); beta[S0]=rng.choice([-1,1],s0)*rng.uniform(0.5,1.5,s0)
    P=ic.IidData(Lam,beta,n,rng)
    res=ic.ls0_path(P,list(range(p)),S0)
    A=P.A; N=n-3; ell=math.sqrt(rho/(1-rho))
    xi=A[2:,0]; a=A[2:,1]; eta=A[1,0]; phi=A[1,1]; Up=A[2:,2:]
    W=Up@Up.T; v1=xi+ell*eta; v2=ell*phi+a
    kap=N/(ell**2*phi**2); vr=N*eta/(ell*phi**2)
    T=list(range(p)); S0s=set(int(s) for s in S0)
    types=set(m[0] for m in res["moves"]); maxdel=0; viol=-1e9; band=0; band_over_d=0
    deleted=[]
    steps=len(res["moves"]); sample=set(np.linspace(0,steps-1,min(steps,25)).astype(int))
    for i,mv in enumerate(res["moves"]):
        if mv[0]!="delN": break
        j=mv[1]
        if i in sample:
            Tn=[t for t in T if t not in S0s]; k=len(T)
            xT=(xi[T].sum()-vr)/(k+kap); gk=1/(k+kap)
            AT=W[np.ix_(T,T)]+np.outer(v2[T],v2[T]); Ai=np.linalg.inv(AT)
            om=(Ai@v1[T])/np.sqrt(np.diag(Ai)); th=math.sqrt(N)*math.sqrt(1-gk)*om
            idx={t:r for r,t in enumerate(T)}
            dl=np.array([th[idx[t]]-(xi[t]-xT) for t in Tn]); md=np.abs(dl).max(); maxdel=max(maxdel,md)
            dT=np.abs(xi[Tn]-xT).min(); viol=max(viol,(abs(xi[j]-xT)-dT)/md)
            below=[xi[t] for t in Tn if xi[t]<xT]; above=[xi[t] for t in Tn if xi[t]>xT]
            aT=max(below) if below else -np.inf; bT=min(above) if above else np.inf
            if deleted:
                dv=np.array([xi[t] for t in deleted])
                out=np.maximum(aT-dv, dv-bT); bo=max(0,out.max()); band=max(band,bo); band_over_d=max(band_over_d,bo/md)
        T.remove(j); deleted.append(j)
    ok=(types=={"delN"}) and set(res["final"])==S0s and len(res["moves"])==p-s0
    Hb=math.sqrt(2*math.log(2*(p-s0)+2)+2*math.log(math.log(n)))
    return dict(n=n,p=p,rho=rho,s0=s0,seed=seed,ok=bool(ok),moves=len(res["moves"]),types=sorted(types),
                maxdelta=round(maxdel,4),ratio=round(maxdel/(Hb*math.sqrt(p*math.log(n)/n)),3),
                Rvarpi_excess_over_maxdelta=round(viol,3),band=round(band,4),band_over_maxdelta=round(band_over_d,3),
                max_add_over_logn=round(res["info"]["max_add_gain"]/math.log(n),3) if "info" in res else None)
cfg=[(10**5,100,0.05,1),(10**5,100,0.95,1),(10**5,300,0.95,2),(10**5,300,0.05,3),(10**6,300,0.95,1),(10**6,300,0.05,1),(10**4,100,0.95,1),(10**4,100,0.02,2)]
for c in cfg:
    for seed in (1,2):
        r=run(*c,seed); print(json.dumps(r)); sys.stdout.flush()
