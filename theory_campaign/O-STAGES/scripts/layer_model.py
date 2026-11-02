"""W' at large p under the single-null layer law of Theorem W (F-DRAFT step 2, Lemma W2):
q_t(S0+l)/q_t(S0) = a_l * exp((t-1) * kappa * Z_l^2/2),  a_l = (s0+1)/(2p) (n+1)^(-1/2) exp(Z_l^2/2),  Z_l iid N(0,1).
F(t) = t*d0 + log(1 + eps(t)) (the affine part cancels in Phi). Exact greedy grid on this F; seed fixed.
This checks the deterministic reduction (Theorem F) + the layer law, not the layer law itself."""
import numpy as np
from math import log, log2, sqrt, ceil
from scipy.special import logsumexp
from grid_core import greedy_grid, N_halving

rng = np.random.default_rng(20261102)
s0 = 2
print(f"{'p':>8} {'n':>8} {'R2':>4} {'T*':>4} {'W_prime':>7} {'g':>7} {'N(wbar)':>7}  (wbar: eps(w)=1/9)")
for R2 in [0.5, 0.9]:
    for p in [100, 1000, 10**4, 10**5]:
        Z2 = rng.standard_normal(p) ** 2
        for n in [200, 1000, 10**4, 10**5, 10**6]:
            la = log((s0 + 1) / (2 * p)) - 0.5 * log(n + 1) + Z2 / 2
            leps = lambda t: float(logsumexp(la + (t - 1) * R2 * Z2 / 2))
            F = lambda t: float(np.logaddexp(0.0, leps(t)))
            g = greedy_grid(F); T = len(g) - 1
            gg = log(sqrt(n) / 9) / (R2 * log(p))
            Wp = 1 if gg >= 1 else (ceil(log2(1 + 1 / gg)) if gg > 0 else -1)
            # eps is increasing in t, so wbar = sup{w in [1,2]: eps(w) <= 1/9} by bisection
            if leps(2.0) <= log(1 / 9): wbar = 2.0
            elif leps(1.0) > log(1 / 9): wbar = 1.0
            else:
                lo, hi = 1.0, 2.0
                for _ in range(50):
                    mid = (lo + hi) / 2
                    if leps(mid) <= log(1 / 9): lo = mid
                    else: hi = mid
                wbar = lo
            Nw = N_halving(wbar) if wbar > 1 else -1
            print(f"{p:8d} {n:8d} {R2:4.1f} {T:4d} {Wp:7d} {gg:7.3f} {Nw:7d}")
