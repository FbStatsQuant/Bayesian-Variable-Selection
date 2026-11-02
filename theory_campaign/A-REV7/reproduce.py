"""Astra-authored small-scale audit; execute on Owls only. Seed 20261102.
Population count-type enumeration reuses frozen candidate implementation;
the explicit swap witness and sample score calculations are independent.
"""
import sys, json, math, platform, datetime
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'sources/W5-B2ENV/scripts'))
from s1_stab import margins_types
from lh_family import lh_sigma, lh_truth, suff_exact_gram
rng = np.random.default_rng(20261102)
out = {'seed':20261102,'utc':str(datetime.datetime.now(datetime.timezone.utc)),
       'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),'margins':[],'witnesses':[]}
for g,rho,psi,vis in [(4,.7,.5,{0:1.4,2:1.8}), (4,.85,.5,{0:1.4,2:1.8}),
                       (9,.4,.2,{0:1.}), (9,.85,.5,{0:1.4})]:
    md,ms,mg,arg = margins_types(g,rho,[(0,1,psi)],vis)
    out['margins'].append(dict(g=g,rho=rho,psi=psi,visible=vis,delete=md,swap=ms,gain=mg,arg=arg))
    print(out['margins'][-1],flush=True)

def delta(R,t,S):
    ix=sorted(S);v=R@t
    return float(t@R@t-v[ix]@np.linalg.solve(R[np.ix_(ix,ix)],v[ix]))

def score(R,r,n,S):
    ix=sorted(S);k=len(ix);p=len(R)
    G=(n-1)*R[np.ix_(ix,ix)];z=(n-1)*r[ix];H=(n+1)*G+np.eye(k)
    Q=n-1-n*z@np.linalg.solve(H,z)
    ld=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(k))[1]
    prior=math.lgamma(k+1)+math.lgamma(2*p-k)-math.lgamma(2*p)
    return prior-.5*ld-(.01+n/2)*math.log(.02+Q)

for name,g,rho,psi,vis,S,j,l in [
    ('same_pair_swap',4,.85,.5,{0:1.4},set(range(4)),0,4),
    ('c1_visible_DOM_not_void',4,.4,.2,{0:1.,2:.01},{0,8},8,4)]:
    G=2 if len(vis)==1 else 3
    R,_=lh_sigma(G,g,rho,0,[(0,1,psi)])
    t,*_=lh_truth(G,g,0,[(0,1,psi)],vis)
    dest=S-{j}|{l}
    w=dict(name=name,S=sorted(S),remove=j,add=l,delta_before=delta(R,t,S),delta_after=delta(R,t,dest),samples=[])
    for n in [400,1600,6400]:
        for rep in range(4):
            _,r=suff_exact_gram(R,t,n,1.,rng)
            w['samples'].append(dict(n=n,rep=rep,swap_log_odds=score(R,r,n,dest)-score(R,r,n,S)))
    out['witnesses'].append(w);print(w,flush=True)
(ROOT/'results.json').write_text(json.dumps(out,indent=2))
