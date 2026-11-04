"""W2_PC2: R2_C §R3 'Necessity: what is within reach'. Fixed 0 < eps < 1/4 replaces W's cross correlation; two
coefficients n^{-1/4} (j1 in group 1, j2 in group 2), sigma^2 = 1, actual blocks = groups (strict separation
0.75 < 1 - eps, B in [9,16] for n >= 9^6).  Claim: d(S0) = -eps(1+eps) sqrt(n) + o_P(sqrt n), d(empty) = 0.
d(S0) = log BF(S0) - log r_1({j1}) - log r_2({j2}) needs only (G_{S0}, z_{S0}, Y); its exact law is simulated with
the 2-column exact-Gram realisation (same law of these statistics as in the full design).  10 seeds per n.
Also reports the full-model D_* lower bound osc d >= -d(S0)."""
import math
import numpy as np
from bvs_common import exact_gram_suff, log_m

for eps in (0.01, 0.05, 0.2):
    print(f"=== eps = {eps}")
    for n in (531441, 10 ** 7, 10 ** 9, 10 ** 11, 10 ** 13):
        Sig = np.array([[1, eps], [eps, 1.0]])
        th = np.array([n ** -0.25, n ** -0.25])
        vals = []
        for s in range(10):
            rng = np.random.default_rng(500 + s)
            G, z, Y, _ = exact_gram_suff(Sig, th, n, 1.0, rng)
            l0 = log_m(G, z, Y, n, [])
            dS = (log_m(G, z, Y, n, [0, 1]) - l0) - (log_m(G, z, Y, n, [0]) - l0) - (log_m(G, z, Y, n, [1]) - l0)
            vals.append(dS)
        vals = np.array(vals)
        pred = -eps * (1 + eps) * math.sqrt(n)
        print(f"n={n:.3g}: d(S0) median {np.median(vals):.4g} [min {vals.min():.4g}, max {vals.max():.4g}]  "
              f"pred {pred:.4g}  ratio {np.median(vals)/pred:.4f}  (d-pred)/n^0.25 max {np.abs(vals-pred).max()/n**0.25:.3f}")
