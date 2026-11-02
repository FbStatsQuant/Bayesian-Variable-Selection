import numpy as np, itertools, sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Bayesian-Variable-Selection/eb0b38ac-c837-5510-b7b2-7052431f35fc/scratchpad/ref')
from lhlat import build, Delta
rng=np.random.default_rng(7); maxerr=0
for rep in range(40):
    G=7;g=3; rh=list(rng.uniform(.05,.99,G)); pr=[]
    for k in range(3):
        a,b=2*k,2*k+1; ps=rng.uniform(.9,.9999)*min(rh[a],rh[b])*rng.choice([-1,1]) if rep%2 else rng.uniform(.01,1)*min(rh[a],rh[b])*rng.choice([-1,1])
        pr.append((a,b,ps,rng.choice([-1,1])*rng.uniform(.2,3)))
    vis=[(6,rng.uniform(-2,2))]
    S,th=build(G,g,rh,pr,vis); p=G*g
    M=[gb*g for (_,gb,_,_) in pr]; S0=set(np.nonzero(th)[0]); Sc=S0-set(M)
    for r in range(4):
      for sub in itertools.combinations(range(3),r):
        St=Sc|{M[i] for i in sub}; dS=Delta(S,th,St)
        for l in range(p):
            if l in St: continue
            pred=0.0
            for i,(ga,gb,ps,b) in enumerate(pr):
                Ri=b*b*ps*ps*(1-ps*ps)
                if l==gb*g and i not in sub: pred=Ri
                elif gb*g<l<(gb+1)*g and i not in sub: pred=Ri*rh[gb]**2*(1-ps**2)/(1-ps**2*rh[gb]**2)
            maxerr=max(maxerr,abs((dS-Delta(S,th,St|{l}))-pred))
        for t in St:
            pred=None
            for i,(ga,gb,ps,b) in enumerate(pr):
                if t==ga*g: pred=b*b*(1-ps*ps) if i in sub else b*b*(1-ps*ps)**2
                if t==gb*g: pred=b*b*ps*ps*(1-ps*ps)
            if pred is None: pred=vis[0][1]**2
            maxerr=max(maxerr,abs((Delta(S,th,St-{t})-dS)-pred))
print("max abs error of red(l)/deletion formulas:",maxerr)
