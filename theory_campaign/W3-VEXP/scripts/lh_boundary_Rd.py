"""Beyond Lemma 4.2's hypothesis (psi >= rho): where does the start mass go?  pi0(R_d), d = 0,1,2, and the start mode.
Config A with psi in {0.69, 0.71, 0.8}; explicit exact-Gram design; seed 20261102 + n + 1000 psi; 30 replicates."""
import itertools, math, sys, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import vcore as V
from lh_more import lh_sigma, one
p = 16; S0 = (0, 4, 8)
masks = np.arange(1 << p)
inS0 = sum(1 << j for j in S0)
extra = V.popcount(masks & ~inS0)
for psi in [0.69, 0.71, 0.8]:
    Sigma, groups = lh_sigma(p, 4, 0.7, [(0, 1, psi)])
    th = np.zeros(p); th[0] = 1.4; th[4] = -psi * 1.4; th[8] = 1.8
    for n in [1600, 25600]:
        rng = np.random.default_rng(20261102 + n + int(1000 * psi))
        Rd = {0: [], 1: [], 2: []}; modes = {}; Xf = None
        for r in range(30):
            pi0, _, blocks, Xf = one(n, Sigma, th, rng, Xf)
            for d in Rd: Rd[d].append(pi0[extra <= d].sum())
            m = int(np.argmax(pi0)); key = tuple(j for j in range(p) if m >> j & 1)
            modes[key] = modes.get(key, 0) + 1
        print(json.dumps(dict(psi=psi, n=n, pi0_Rd_med={d: round(float(np.median(v)), 4) for d, v in Rd.items()},
                              start_modes={str(k): v for k, v in modes.items()})), flush=True)
