"""R03 scratch: s0=2 singleton variant, theta=(1,1); counts initial swaps vs ell+4. Nonproduction partition."""
import sys, json
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'numerics'))
from n3_singletons import *
for n in (800,2000):
    for ratio in (.6,.85):
        p=int(ratio*n)
        for seed in range(2):
            theta=np.zeros(p);theta[0]=1;theta[1]=1
            P=cs.CS(.5,theta,n,rng=np.random.default_rng(100+seed))
            S=singleton_start(P); r=run_path(P,S); mv=r['moves']
            init=next((i for i,m in enumerate(mv) if m[0]!='sN'),len(mv))
            ell=bc.ell_cap(n,p)
            print(json.dumps(dict(n=n,p=p,seed=seed,start=len(S),truth_in=all(j in S for j in (0,1)),
              init_swaps=init,ell=ell,need=ell+4,miss_pred=init>=ell+4,moves=len(mv),final_S0=r['final_is_S0'])),flush=True)
