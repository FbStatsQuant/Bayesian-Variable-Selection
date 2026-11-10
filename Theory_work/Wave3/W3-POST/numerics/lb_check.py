"""Falsification check of Proposition LB (lemmas/LB_rate_lower_bound.md): for every data set and every S0 with
1 <= s0 < p, s0+1 <= K: 1 - pi(S0) >= 1/(1+sqrt(n+1)). Exact coded posterior (post_exact.Post), p <= 10.
Designs: iid, duplicated columns, near-collinear, (nearly) all-identical; responses: signal, pure noise, and y fitted
almost exactly by one column (adversarial). Reports min over all cases and all candidate S0 of size 1..3 of
(1 - pi(S0)) * (1 + sqrt(n+1)), which must be >= 1. Run: py -3.13 -I lb_check.py"""
import itertools, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from post_exact import Post, standardise

rng = np.random.default_rng(20261109)
worst, count, arg = math.inf, 0, None
for n in [6, 12, 40, 200, 1000]:
    for p in [3, 6, 10]:
        for kind in ["iid", "dup", "near", "same"]:
            for rep in range(3):
                Xr = rng.standard_normal((n, p))
                if kind == "dup":
                    Xr[:, 1] = Xr[:, 0]
                if kind == "near":
                    Xr[:, 1] = Xr[:, 0] + 1e-4 * rng.standard_normal(n)
                if kind == "same":
                    Xr = np.tile(Xr[:, :1], (1, p)) + 1e-6 * rng.standard_normal((n, p))
                X, _ = standardise(Xr, rng.standard_normal(n))
                for yk in ["sig", "noise", "exact"]:
                    if yk == "sig":
                        yr = X[:, :2] @ np.array([3.0, -2.0]) + rng.standard_normal(n)
                    elif yk == "noise":
                        yr = rng.standard_normal(n)
                    else:
                        yr = 5.0 * X[:, 0] + 1e-6 * rng.standard_normal(n)
                    X2, y = standardise(X, yr)
                    P = Post(X2, y)
                    for s0 in range(1, min(3, p - 1) + 1):
                        if s0 + 1 > P.K:
                            continue
                        for S0 in itertools.combinations(range(p), s0):
                            v = (1 - P.mass(S0)) * (1 + math.sqrt(n + 1))
                            count += 1
                            if v < worst:
                                worst, arg = v, (n, p, kind, yk, S0)
print(f"LB check: {count} (data set, S0) pairs; min (1-pi(S0))*(1+sqrt(n+1)) = {worst:.6f} (must be >= 1) at {arg}")
