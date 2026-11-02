"""CE1, narrow form: the explicit sequence of A-REV1 Sec. 5, evaluated with the method's score.  Seed 20261109.

p_n = ceil(n^(1/3)), S0 = {1}, theta_1 = 1 (fixed), exact Gram with unit diagonal, corr(x1, x2) = r, all other
correlations 0; Gaussian noise sigma = 1.  Boundary state Y = {3} (d = 1): no present truth, so Q_T(Y) = 0 exactly.
Lemma E (W2-VT24G, VERIFIED by A-REV1): one-round exit prob from R_1 >= o*(Y) / (B + m + d + 3) = o*(Y)/(B + 5),
with o*(Y) >= o_2(Y), B = min(floor(sqrt n), floor(sqrt p), 16), L = ceil(log2(n+1)).
We report o_2(Y), the Lemma E floor o_2(Y)/(B+5), and (L+4) times that floor.
"""
import json
import math
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from bvs_core import Target, exact_gram_design  # noqa: E402

rows = []
for r in (0.3, 0.6):
    for n in (200, 1000, 5000, 20000, 100000):
        p = math.ceil(n ** (1 / 3))
        reps = []
        for rep in range(5):
            rng = np.random.default_rng(20261109 + 1000 * rep + n + int(100 * r))
            Sig = np.eye(p)
            Sig[0, 1] = Sig[1, 0] = r
            X = exact_gram_design(n, Sig, rng)
            theta = np.zeros(p)
            theta[0] = 1.0
            # columns have norm^2 n-1, i.e. unit-variance scale; signal mu = theta_1 x_1
            y = X @ theta + rng.standard_normal(n)
            y = y - y.mean()
            y = y / math.sqrt((y @ y) / (n - 1))
            T = Target(X, y)
            o2 = T.gibbs_o((2,), 1)        # coordinate 2 (index 1) at Y = {3} (index 2)
            reps.append(o2)
        B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
        L = math.ceil(math.log2(n + 1))
        omin = min(reps)
        rows.append(dict(r=r, n=n, p=p, B=B, L=L, o2_min=omin, o2_all=reps,
                         lemmaE_floor=omin / (B + 5), L4_times_floor=(L + 4) * omin / (B + 5)))
        print(rows[-1])
with open(__file__.rsplit('/', 2)[0] + '/results/ce1_sequence.json', 'w') as fh:
    json.dump(rows, fh, indent=1)
