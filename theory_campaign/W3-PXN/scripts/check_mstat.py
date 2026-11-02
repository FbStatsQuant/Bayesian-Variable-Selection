"""Theorem P4 check: T_n := Mstat - log pi0(S°) - sum_i log((s+i)p/(2p-s-i)) = sum_i [log r({j_b_i}) + (1/2)log n]
should have the exact law of sum_i -nu log(1 - kappa_n B_i), B_i iid Beta(1/2,(n-2)/2) (Lemma B(iii)), -> chi2_c/2.
KS test per config against a Monte Carlo of the exact law (seed 11)."""
import json, math, numpy as np
from scipy import stats
rng = np.random.default_rng(11)
for name in ("A", "B", "P"):
    R = [json.loads(l) for l in open(f"../results/lh_{name}.jsonl")]
    c = len(R[0]["M"]); s = len(R[0]["Sref"])
    T = []; U = []
    for r in R:
        n, p = r["n"], r["p"]
        pri = sum(math.log((s + i) * p / (2 * p - s - i)) for i in range(1, c + 1))
        t = r["Mstat"] - r["log_pi0_Sref"] - pri
        nu = 0.01 + n / 2; kap = (n - 1) ** 2 / (n * (n - 0.98))
        sim = sum(-nu * np.log1p(-kap * rng.beta(0.5, (n - 2) / 2, 20000)) for _ in range(c))
        U.append(np.mean(sim <= t))  # probability integral transform under the exact law
        T.append(t)
    print("config %s (c=%d, %d reps): median T = %.3f (chi2_%d/2 median %.3f); KS of PIT vs U(0,1): p = %.3f"
          % (name, c, len(R), np.median(T), c, stats.chi2.median(c) / 2, stats.kstest(U, "uniform").pvalue))
