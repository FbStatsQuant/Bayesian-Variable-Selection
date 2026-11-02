"""Replicate scaling of the phase-2 constants (a = 1, 2) of Theorem B with n (p = 20 fixed, B = 4).
Design seeds 1..10; prints per (scen, c, n) the median/mean of eta2, epsdel, c2 and 1 - pi(S0)."""
import sys, json, math
import numpy as np
from bvs_engine import *
from progress_bounds import phase2_B
out = []
for scen in [1, 4, 5]:
    for n in [200, 800, 3200, 12800]:
        rows = []
        for seed in range(1, 11):
            X, y, S0, b = gen_design(scen, p=20, n=n, c=0.5, seed=seed)
            M = Model(X, y, S0)
            r1 = phase2_B(M, 1); r2 = phase2_B(M, 2)
            rows.append([r1['eta2'], r1['epsdel'], r1['c2'], r2['eta2'], r2['epsdel'], r2['c2'], 1 - math.exp(M.logpi[S0])])
        R = np.array(rows)
        rec = dict(scen=scen, c=0.5, n=n, L=max(4, math.ceil(math.log2(n + 1))),
                   median=dict(zip(['eta2_1', 'epsdel_1', 'c2_1', 'eta2_2', 'epsdel_2', 'c2_2', 'delta1'], np.median(R, 0).tolist())),
                   mean=dict(zip(['eta2_1', 'epsdel_1', 'c2_1', 'eta2_2', 'epsdel_2', 'c2_2', 'delta1'], R.mean(0).tolist())))
        out.append(rec); print(json.dumps(rec), flush=True)
        json.dump(out, open(sys.argv[1], 'w'), indent=1)
