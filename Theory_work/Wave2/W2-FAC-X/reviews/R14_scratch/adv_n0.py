# R14: adversarial excluded sets 𝔫 (|𝔫|=15) for claim (C2) "simultaneously for every 𝔫"; exact delta along the path.
import sys, math, json, numpy as np
sys.path.insert(0, r"../../numerics")
import iid_core as ic
def run(n,p,rho,s0,seed,mode):
    rng=np.random.default_rng(seed)
    Lam=np.full(p,math.sqrt(rho))
    beta=np.zeros(p); S0=sorted(int(s) for s in rng.choice(p,s0,replace=False))
    beta[S0]=rng.choice([-1,1],s0)*rng.uniform(0.5,1.5,s0)
    P=ic.IidData(Lam,beta,n,rng)
    A=P.A; N=n-3; ell=math.sqrt(rho/(1-rho))
    xi=A[2:,0]; a=A[2:,1]; eta=A[1,0]; phi=A[1,1]; Up=A[2:,2:]
    kap=N/(ell**2*phi**2); vr=N*eta/(ell*phi**2)
    nulls=[j for j in range(p) if j not in S0]
    x0=(xi[[j for j in range(p)]].sum()-vr)/(p+kap)
    if mode=="near": nn=sorted(nulls,key=lambda j:abs(xi[j]-x0))[:15]
    elif mode=="top": nn=sorted(nulls,key=lambda j:-abs(xi[j]))[:15]
    elif mode=="toppos": nn=sorted(nulls,key=lambda j:-xi[j])[:15]
    elif mode=="none": nn=[]
    start=[j for j in range(p) if j not in nn]
    W=Up@Up.T; v1=xi+ell*eta; v2=ell*phi+a
    res=ic.ls0_path(P,start,S0)
    T=list(start); S0s=set(S0); deleted=[]; maxd=0; exc=0; band=0
    steps=len(res["moves"]); sample=set(np.linspace(0,max(steps-1,0),min(steps,20)).astype(int))
    for i,mv in enumerate(res["moves"]):
        if mv[0]!="delN": break
        j=mv[1]; Tn=[t for t in T if t not in S0s]; k=len(T)
        xT=(xi[T].sum()-vr)/(k+kap)
        dT=np.abs(xi[Tn]-xT).min(); exc=max(exc,abs(xi[j]-xT)-dT)
        below=[xi[t] for t in Tn if xi[t]<xT]; above=[xi[t] for t in Tn if xi[t]>xT]
        aT=max(below) if below else -np.inf; bT=min(above) if above else np.inf
        if deleted:
            dv=xi[deleted]; band=max(band,max(0,np.maximum(aT-dv,dv-bT).max()))
            assert not any(aT<xi[t]<bT for t in Tn)
        if i in sample:
            gk=1/(k+kap); AT=W[np.ix_(T,T)]+np.outer(v2[T],v2[T]); Ai=np.linalg.inv(AT)
            th=math.sqrt(N)*math.sqrt(1-gk)*(Ai@v1[T])/np.sqrt(np.diag(Ai)); idx={t:r for r,t in enumerate(T)}
            maxd=max(maxd,max(abs(th[idx[t]]-(xi[t]-xT)) for t in Tn))
        T.remove(j); deleted.append(j)
    ok=all(m[0]=="delN" for m in res["moves"]) and set(res["final"])==S0s and steps==len(start)-s0
    inf=res["info"]
    return dict(n=n,p=p,rho=rho,s0=s0,seed=seed,mode=mode,ok=bool(ok),moves=steps,
        maxdelta_sampled=round(maxd,4),excess=round(exc,4),band=round(band,4),
        exc_over_maxd=round(exc/maxd,2) if maxd else None, band_over_maxd=round(band/maxd,2) if maxd else None,
        max_add_over_logn=round(inf["max_add_gain"]/math.log(n),3), max_truth=round(inf["max_truth_move"],2),
        swap_minus_del=round(inf["max_swap_minus_del"],3))
if __name__=="__main__":
  cfg=[(10**5,180,0.5,1),(10**5,180,0.1,2),(10**6,400,0.9,1),(10**6,400,0.3,3)]
  for c in cfg:
    for mode in ("near","top","toppos"):
        for seed in (11,12):
            print(json.dumps(run(*c,seed,mode))); sys.stdout.flush()
