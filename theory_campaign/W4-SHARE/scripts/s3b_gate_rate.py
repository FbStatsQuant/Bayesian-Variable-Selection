"""W4-SHARE s3b: gate rate in PB(n=16000, J=80): S0 evaluations per particle-round at phi = 1 from {12} and from pi0 draws (3 rounds x 400000 particles), and pair-state start masses / d-increments. Seed 3."""
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0] if '/' in __file__ else '.')
import numpy as np
exec(open(__file__.rsplit("/",1)[0]+"/s3_bvs_barrier.py" if "/" in __file__ else "s3_bvs_barrier.py").read().split("out = []")[0])
R, alpha = build_R()
n=16000; J=80; s=np.sqrt(2*J/(n-1)); om=0.01
th=np.zeros(p); th[8]=s/np.sqrt(om); th[0]=th[4]=-alpha*s/np.sqrt(om); th[12]=0.3
z,yy=suff_stats(R,th,1.0,n,np.random.default_rng(11))
m=BVS(R,z,yy,n,[0,4,8,12])
rng=np.random.default_rng(3)
Sd=1<<12
from collections import Counter
for start in ['{12}','pi0']:
    S = np.full(400000, Sd, dtype=np.int64) if start=='{12}' else m.draw_pi0(400000, rng)
    hits=Counter()
    def rec(states, mech):
        k=int(np.sum(states==m.S0))
        if k: hits[mech]+=k
    for r in range(3):
        S=m.one_round(S,1.0,rng,rec)
    print(start, 'S0 evals in 3 rounds x 400000:', dict(hits), 'occupying S0 at end:', int(np.sum(S==m.S0)))
# rate of pair states under pi0 and q_1
pair=[Sd|1<<0|1<<8, Sd|1<<4|1<<8, Sd|1<<0|1<<4]
print('pi0 pairs', [m.pi0[x] for x in pair], 'pi(pairs)', [m.post[x] for x in pair])
print('d diffs', [m.d[x]-m.d[Sd] for x in pair], 'd(S0)-d', m.d[m.S0]-m.d[Sd])
