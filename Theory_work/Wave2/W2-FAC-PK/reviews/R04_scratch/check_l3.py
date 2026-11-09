"""Read-only proof falsification; all outputs stay beside this script."""
import sys
from pathlib import Path
import math
import json
import itertools
import numpy as np
from scipy.special import gammaln, ndtr

HERE = Path(__file__).resolve().parent
NUM = HERE.parents[1] / "numerics"
sys.path.insert(0, str(NUM))
import pk_core as pk
from l3_static import gains


def pair_search(P):
    """Exhaust every retained pair, maximizing d, without an extreme-tail assumption."""
    rho, n = P.rho, P.n
    kap = P.al / P.be
    varrho = (math.sqrt(n-1)*rho*P.theta.sum()/math.sqrt(1-rho)
              + math.sqrt(rho/(1-rho))*P.al*P.eta)/P.be
    b = P.xi[list(P.S0)].sum() - varrho
    nulls = np.setdiff1d(np.arange(P.p), P.S0)
    best = (-1., None)
    pairs = 0
    for i in range(len(nulls)-1):
        js = nulls[i+1:]
        u, vs = P.xi[nulls[i]], P.xi[js]
        x = (u+vs+b)/(2+len(P.S0)+kap)
        d = np.minimum(np.abs(u-x), np.abs(vs-x))
        j = int(d.argmax())
        if d[j] > best[0]:
            best = (float(d[j]), [int(nulls[i]), int(js[j])])
        pairs += len(js)
    one_x = (P.xi[nulls]+b)/(1+len(P.S0)+kap)
    one_d = np.abs(P.xi[nulls]-one_x)
    one = int(nulls[one_d.argmax()])
    ans = dict(n=n, p=P.p, rho=rho, b=float(b), pair_count=pairs,
               m1_max_d=float(one_d.max()), m1_null=one,
               m1_gain_ratio=gains(P, set(P.S0)|{one})[0]/math.log(n),
               m2_max_d=best[0], m2_nulls=best[1],
               m2_gain_ratio=gains(P, set(P.S0)|set(best[1]))[0]/math.log(n),
               cD=.5-1/(len(P.S0)+1+(1-rho)/rho))
    return ans


def exhaustive_small():
    """Check exact score budgets and phase-A swap existence for every size-K set."""
    results=[]
    for rho, co in [(.2, [1.4,-1.0]), (.8,[1.]), (.95,[1.,-.9])]:
        n=14; p=13
        th=np.zeros(p); th[:len(co)]=co
        P=pk.make_cs(rho,th,n,7)
        s0=set(P.S0); K=P.K
        min_phase=math.inf; max_del=-math.inf; max_budget_excess=-math.inf
        nmissing=0; nabove=0
        ln=math.log(n)
        for tup in itertools.combinations(range(p),K):
            T=set(tup)
            ins=np.array(tup); outs=np.array(sorted(set(range(p))-T))
            B=P.z[ins].sum(); A=np.square(P.z[ins]).sum()
            gam=P.be/(P.al+K*P.be)
            psi=.02+n-1-n*(A-gam*B*B)/P.al
            tin=P.z[ins]-gam*B; tout=P.z[outs]-gam*B
            delta=P.lw[K-1]-P.lw[K]+.5*(pk._ldet(P,K)-pk._ldet(P,K-1))
            dels=delta-P.nu*np.log1p(n*(1+P.be/(P.al+(K-1)*P.be))*tin**2/(P.al*psi))
            max_del=max(max_del,float(dels.max()-delta))
            if not s0<=T:
                v=tout[None,:]**2-tin[:,None]**2-gam*(tout[None,:]-tin[:,None])**2
                swaps=-P.nu*np.log1p(-n*v/(P.al*psi))
                min_phase=min(min_phase,float(swaps.max()/n)); nmissing+=1
            else:
                ds=sum(float(P.lw[k-1]-P.lw[k]+.5*(pk._ldet(P,k)-pk._ldet(P,k-1))) for k in range(len(s0)+1,K+1))
                max_budget_excess=max(max_budget_excess,P.F(s0)-P.F(T)-ds); nabove+=1
        results.append(dict(n=n,p=p,rho=rho,truth=co,sizeK_sets=math.comb(p,K),
                            missing_sets=nmissing,above_sets=nabove,
                            min_best_swap_over_n=min_phase,
                            max_deletion_minus_delta=max_del,
                            max_budget_excess=max_budget_excess))
    return results


def main():
    rows=[]
    for rho, co, seed in [(.8,[1.],3),(.95,[1.],4),(.5,[1.4,-1.,1.8,-1.2],6)]:
        n=8000; th=np.zeros(n-1); th[:len(co)]=co
        P=pk.make_cs(rho,th,n,seed)
        r=pair_search(P); rows.append(r); print(json.dumps(r),flush=True)
    small=exhaustive_small()
    for r in small: print(json.dumps(r),flush=True)
    # Algebraic m=1 factor and the two-sided bound, including rho close to one.
    factor_max=0.
    for s in [1,2,4,16]:
        for rho in [.001,.2,.5,.8,.95,.999999]:
            t=s+(1-rho)/rho
            for m in range(1,1001):
                factor=t*t/((m+t-1)*(m+t))
                factor_max=max(factor_max,factor-t/(t+1))
                assert factor<=t/(t+1)+1e-14
    out=dict(pair_searches=rows,exhaustive_small=small,
             max_one_sided_factor_excess=factor_max)
    (HERE/'check_l3_results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
