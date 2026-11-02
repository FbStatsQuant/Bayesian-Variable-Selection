"""TS counterexample (W2-PREM PROOF.md §6.1): truth stability at incomplete states is NOT implied by G, R, SE, BM-inf.

Design (exact Gram): p = 10; truths 0, 1 with corr r = 0.5; theta_0 = 1, theta_1 = -1/r = -2 (fixed, so BM-inf holds);
the 8 nulls are independent of everything (SE holds with phi0^2 = 1 - r = 0.5).
At W = {0} (truth 1 missing) the projection coefficient of mu on x_0 is theta_0 + r theta_1 = 0, so the Gibbs step of
coordinate 0 deletes the truth with probability -> 1 (a "bad" step of Theorem B at an incomplete state).
Also reported: the gain of adding the missing truth 1 at W = {0} (progress is still available, odds -> infinity),
so repair itself is not blocked -- only Theorem B's potential bookkeeping fails.
Output: results/ts_cancel.txt.  Fixed seeds.
"""
import numpy as np
from bvs_score import Data

p, r = 10, 0.5
Sig = np.eye(p)
Sig[0, 1] = Sig[1, 0] = r
th = np.zeros(p)
th[0], th[1] = 1.0, -1.0 / r
lines = ["n | median P(G_0 deletes truth 0 at W={0}) | median P(G_1 adds truth 1 at W={0}) | 20 reps"]
for n in [200, 1000, 5000, 25000, 125000, 625000]:
    dl, ad = [], []
    for s in range(20):
        D = Data(Sig, th, n, np.random.default_rng(100 * s + n % 1013))
        F0, Fe, F01 = D.F((0,)), D.F(()), D.F((0, 1))
        dl.append(1 / (1 + np.exp(F0 - Fe)))        # 1 - o_0({0})
        ad.append(1 / (1 + np.exp(-(F01 - F0))))   # o_1({0})
    lines.append(f"{n} | {np.median(dl):.6f} | {np.median(ad):.6f}")
    print(lines[-1], flush=True)
with open(__file__.replace("scripts/ts_cancel.py", "results/ts_cancel.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
