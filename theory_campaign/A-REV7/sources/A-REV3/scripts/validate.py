import json, math, platform, sys, hashlib
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import binom
from lh_iid import run_rep, CONFIGS, gen_lh

out = Path('results'); out.mkdir(exist_ok=True)
print(json.dumps(dict(python=sys.version, platform=platform.platform(), numpy=np.__version__, scipy=scipy.__version__)), flush=True)
# Reproduce three saved-source LH cases on the actual complete-linkage partition.
with (out/'lh.jsonl').open('w') as f:
    for rep in range(3):
        rec = run_rep(CONFIGS['A'], 200, 750, rep, 'A')
        f.write(json.dumps(rec)+'\n'); f.flush()
        cfg=CONFIGS['A']
        X,y,*_ = gen_lh(200,75,10,cfg['rho'],cfg['psi'],cfg['pairs'],cfg['visible'],np.random.default_rng(rec['seed']))
        np.savez_compressed(out/f'data_{rep}.npz', X=X,y=y)
        print(json.dumps(rec), flush=True)
# Exact rare-outsider counterexample to an unqualified sharp-transition assertion.
for N in [100,1000,10000]:
    q=1/N; kappa=3*math.log(N); k=np.arange(N+1)
    # k is number of outsiders. Conditional extinction of target a.
    omega=k*np.exp(kappa)/(N-k+k*np.exp(kappa))
    exact=float(np.dot(binom.pmf(k,N,q),omega**N))
    print(json.dumps(dict(test='SH_rare_outsider',N=N,kappa=kappa,extinction=exact,ceiling=1-(1-q)**N)),flush=True)
# Fixed-signal counterexample to M(b)'s quadratic equality with a small remainder.
# Orthogonal single truth, theta=sigma=1: x -> 1/2, exact gain/n -> log(2)/2.
print(json.dumps(dict(test='M_expansion',exact_limit=math.log(2)/2,quadratic_limit=0.25,difference=math.log(2)/2-0.25)),flush=True)
# Exact log retention vs the replacement sum eta used in W4's final assembly.
print(json.dumps(dict(test='eta_replacement',eta=.5,exact_loss_per_stage=-math.log(.5),claimed_loss_per_stage=.5)),flush=True)
