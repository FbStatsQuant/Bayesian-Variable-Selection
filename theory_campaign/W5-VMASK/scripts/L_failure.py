"""(L)-failure rate at S0 on LH-iid config A (c = 1, s0 = 3): event {exists null/neutral/proxy l: F(S0 + l) > F(S0)}.
Exact scores (own scorer), many replicates; compared with PXN's first-order formulas
   P1 := (s0+1)/sqrt(2 pi (n+1) t_n),   P2 := p * P(chi2_1 > t_n),   t_n := 2 log((2p-s0-1)/(s0+1)) + log(n+1).
Deletion/swap parts of (L) have Theta(n) margins and are not simulated here. Seed 9500 + n.
Output: ../results/L_failure.txt
"""
import math, sys
import numpy as np
from scipy import stats
from vm_core import lh_spec, gen_lh_iid, standardise, Scorer

grid = [(200, 750, 3000), (400, 1790, 1500), (800, 4260, 500), (1600, 10120, 150)]
if len(sys.argv) > 1:
    grid = grid[:int(sys.argv[1])]
lines = ["n p reps | fails (rate, 95% CI) | P1 formula | P2 formula | median max gain | fails by a proxy l"]
for n, p, reps in grid:
    G = p // 10
    units, theta, S0, Sref, M, groups = lh_spec(G, 10, 0.7, [0.5], [1.0], [1.0])
    rng = np.random.default_rng(9500 + n)
    s0 = len(S0)
    fails, gains, proxy_fail = 0, [], 0
    for r in range(reps):
        Xr, yr = gen_lh_iid(n, G, 10, units, theta, rng)
        X, y = standardise(Xr, yr)
        sc = Scorer(X, y)
        a = sc.add_scan(S0) + sc.logw[s0 + 1] - sc.F(S0)
        a[S0] = -np.inf
        l = int(np.argmax(a))
        gains.append(a[l])
        if a[l] > 0:
            fails += 1
            if l in range(10, 20):
                proxy_fail += 1
    t = 2 * math.log((2 * p - s0 - 1) / (s0 + 1)) + math.log(n + 1)
    P1 = (s0 + 1) / math.sqrt(2 * math.pi * (n + 1) * t)
    P2 = p * stats.chi2.sf(t, 1)
    ci = stats.binomtest(fails, reps).proportion_ci()
    lines.append(f"{n} {p} {reps} | {fails} ({fails/reps:.4f}, [{ci.low:.4f}, {ci.high:.4f}]) | {P1:.4f} | {P2:.4f} | "
                 f"{np.median(gains):.2f} | {proxy_fail}")
    print(lines[-1], flush=True)
open("../results/L_failure.txt", "w").write("\n".join(lines) + "\n")
