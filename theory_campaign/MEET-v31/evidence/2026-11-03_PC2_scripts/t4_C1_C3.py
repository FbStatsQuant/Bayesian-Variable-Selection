# C1(a) ratio with S = Shat; C1(b) "unscored" sentence; C3(c) on top-c stores of random scored sets. Exact enumeration.
import numpy as np, math, sys
sys.path.insert(0, __file__.rsplit('/',1)[0]); from pc2_common import *
rng=np.random.default_rng(20261106)
alpha=0.05
# flat-ish posterior: proxies of one latent, weak signal -> pi(Shat) small
n,p=40,12; Z=rng.standard_normal((n,1)); Xr=Z+0.7*rng.standard_normal((n,p)); yr=0.6*Z[:,0]+rng.standard_normal(n)
X,y=std(Xr,yr); T=Target(X,y); Fall=T.enum(); lZ=lse(Fall.values())
order=sorted(Fall,key=lambda S:(-Fall[S],len(S),S)); Shat=order[0]
piS=math.exp(Fall[Shat]-lZ); g=Fall[Shat]-Fall[order[1]]
print(f"[C1(a)] S=Shat in T: ratio pi(S)/pi(Shat)=1, e^-g={math.exp(-g):.4f} -> inequality '<= e^-g' fails for S=Shat whenever g>0 (g={g:.4f})")
# Scenario: every model of Omega scored (scored set = Omega), Zhat = Z (so Z >= alpha*Zhat holds surely), reported T = top-c.
for c in [1,5,20,4*p+1,40*p+1]:
    Tset=order[:c]; ZT=math.exp(lse([Fall[S] for S in Tset])-lZ)
    lb=1-ZT/alpha          # C1(b) 'unscored and unreported mass >= 1 - Z_T/(alpha Zhat)', Zhat=Z
    out=1-ZT              # exact mass outside T
    print(f"[C1(b)] |T|={c:4d}: Z_T/Z={ZT:.4f}; bound 1-Z_T/(aZhat)={lb:+.4f}; exact pi(Omega\\T)={out:.4f}; exact unscored mass=0 -> "
          + ("'unscored' sentence FALSE" if lb>0 else "vacuous"))
print(f"  |Omega|={len(Fall)}, pi(Shat)={piS:.4f}")
# C3(c): random scored sets, store = top-(40p+1) under HPM order; check pi(S)<=e^-g pi(Shat) for all scored S != Shat
viol=0; trials=0
for t in range(300):
    m=int(rng.integers(2,len(order))); idx=rng.choice(len(order),m,replace=False); scored=[order[i] for i in sorted(idx)]
    cap=int(rng.choice([2,5,4*p+1,40*p+1]))
    store=scored[:cap]; Sh=store[0]; gg=Fall[Sh]-Fall[store[1]]
    for S in scored[1:]:
        trials+=1; viol+= Fall[S]-Fall[Sh] > -gg+1e-12
print(f"[C3(c)] {trials} (scored S, store) pairs, caps in {{2,5,4p+1,40p+1}}: violations {viol}")
