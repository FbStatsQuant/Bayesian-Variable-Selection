# R05 midpoint scratch: relative (whitened) deviation of centered, sample-sd-standardized
# sample correlation R from CS Sigma, versus sqrt(p/n) and p/sqrt(n). Also unequal loadings.
import numpy as np, json, sys
out=[]
for design in ["CS","FAC"]:
  for seed in range(3):
    rng=np.random.default_rng(seed)
    for n in [2000,8000]:
      for p in [25,100,400]:
        if design=="CS":
          rho=.5; lam=np.full(p,np.sqrt(rho))
        else:
          lam=rng.uniform(.3,.9,p)
        Sig=np.outer(lam,lam); np.fill_diagonal(Sig,1.0)
        w,V=np.linalg.eigh(Sig); Sih=V@np.diag(w**-.5)@V.T
        f=rng.standard_normal(n); U=rng.standard_normal((n,p))
        X=f[:,None]*lam[None,:]+U*np.sqrt(1-lam**2)[None,:]
        X=X-X.mean(0); X=X/np.sqrt((X**2).sum(0)/(n-1))
        R=X.T@X/(n-1)
        e=np.linalg.norm(Sih@(R-Sig)@Sih,2)
        ea=np.linalg.norm(R-Sig,2)
        out.append(dict(design=design,seed=seed,n=n,p=p,e_rel=e,e_abs=ea,
          ratio_rel_sqrtpn=e/np.sqrt(p/n),ratio_rel_psqrtn=e/(p/np.sqrt(n)),ratio_abs_psqrtn=ea/(p/np.sqrt(n))))
json.dump(out,open("R05_relnorm_out.json","w"),indent=1)
for o in out:
  if o["seed"]==0: print(o["design"],o["n"],o["p"],"rel/sqrt(p/n)=%.2f rel/(p/sqrt n)=%.3f abs/(p/sqrt n)=%.3f"%(o["ratio_rel_sqrtpn"],o["ratio_rel_psqrtn"],o["ratio_abs_psqrtn"]))
print("max rel/sqrt(p/n) over all:",max(o["ratio_rel_sqrtpn"] for o in out))
