# R05 scratch: diagnostic only. Same simulator as r05_check.py with cap ell+2K (cap_extra=K); counts swaps vs n.
import importlib.util, json, sys, math
sys.argv=['x']; src=open('r05_check.py').read().split('out=[]')[0]; exec(src)
res=[]
for n in [400,1000,2000,4000]:
    for seed in range(3):
        r=ls0(n,.75,2,100+seed,cap_extra=n//2); r['sqrt_n_over_sqrtlog']=math.sqrt(n/math.log(n)); res.append(r); print(json.dumps(r)); sys.stdout.flush()
json.dump(res,open('r05_cap2_out.json','w'),indent=1)
