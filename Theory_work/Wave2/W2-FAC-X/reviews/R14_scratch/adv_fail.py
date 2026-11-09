import sys, math, json, numpy as np
sys.path.insert(0, r"../../numerics")
import iid_core as ic
from adv_n0 import run
def first_move(n,p,rho,s0,seed):
    rng=np.random.default_rng(seed)
    Lam=np.full(p,math.sqrt(rho)); beta=np.zeros(p); S0=sorted(int(s) for s in rng.choice(p,s0,replace=False))
    beta[S0]=rng.choice([-1,1],s0)*rng.uniform(0.5,1.5,s0)
    P=ic.IidData(Lam,beta,n,rng); A=P.A; N=n-3; ell=math.sqrt(rho/(1-rho))
    xi=A[2:,0]; eta=A[1,0]; phi=A[1,1]; kap=N/(ell**2*phi**2); vr=N*eta/(ell*phi**2)
    nulls=[j for j in range(p) if j not in S0]; nn=sorted(nulls,key=lambda j:-xi[j])[:15]
    start=[j for j in range(p) if j not in nn]
    res=ic.ls0_path(P,start,S0,max_moves=3)
    k=len(start); xT=(xi[start].sum()-vr)/(k+kap); g=1/(k+1+kap)
    l=max(nn,key=lambda j:xi[j])
    Delta=math.log((2*p-k-1)/(k+1))+0.5*math.log(n+1)
    approx=-Delta+0.5*(1-g)*(xi[l]-xT)**2
    return dict(n=n,seed=seed,moves=[(m[0],m[1],m[2],round(m[3],3)) for m in res["moves"]],xi_max=round(xi[l],3),xT=round(xT,3),
                Delta=round(Delta,3),approx_Gadd=round(approx,3),log2p2_plus_Ln=round(math.log(2*p+2)+math.log(math.log(n)),3),half_logn=round(0.5*math.log(n),3))
print(json.dumps(first_move(10**5,180,0.1,2,11)))
import adv_n0
for n in (10**7,10**9):
    for seed in (11,12,13,14):
        r=run(n,180,0.1,2,seed,"toppos"); print(json.dumps({k:r[k] for k in ("n","seed","ok","max_add_over_logn","swap_minus_del","exc_over_maxd","band_over_maxd")})); sys.stdout.flush()
