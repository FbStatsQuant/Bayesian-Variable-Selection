"""Diagnose LH-iid config B, n = 1600, rep 4: LS0 ends at S0 + {3514}. Recompute the null-addition gains at S0,
the Z-score of the winning null, and the exact threshold of (L): gain > 0 iff Z^2 (1+o(1)) > 2[log((2p-s0-1)/(s0+1)) + 1/2 log(n+1)].
Also estimate P((L) fails) = P(max over p nulls of the gain > 0) under the null model by Monte Carlo of max chi2_1."""
import math, numpy as np
import lh_iid
from pxn_core import Data, log_F
cfg = lh_iid.CONFIGS["B"]; n, p, rep = 1600, 10120, 4
seed = 20261102 + 1000003 * (ord("B") - 64) + 7919 * n + 31 * p + rep
rng = np.random.default_rng(seed)
X, y, groups, S0, Sref, M = lh_iid.gen_lh(n, p // cfg["g"], cfg["g"], cfg["rho"], cfg["psi"], cfg["pairs"], cfg["visible"], rng)
D = Data(X, y)
XS = D.X[:, S0]
Pr = lambda v: v - XS @ np.linalg.lstsq(XS, v, rcond=None)[0]
r = Pr(D.y)
R = D.X - XS @ np.linalg.lstsq(XS, D.X, rcond=None)[0]
nr = np.sqrt((R ** 2).sum(0)); nr[S0] = np.inf
Z = (R.T @ r) / nr / math.sqrt(r @ r / (n - 1 - len(S0)))
top = np.argsort(-np.abs(Z))[:3]
F0 = log_F(D, [S0])[0]
for l in top:
    print("l=%d group=%d Z^2=%.2f gain F(S0+l)-F(S0)=%.3f" % (l, l // 10, Z[l] ** 2, log_F(D, [sorted(S0 + [int(l)])])[0] - F0))
thr = 2 * (math.log((2 * p - 5 - 1) / 6) + 0.5 * math.log(n + 1))
print("first-order threshold on Z^2: %.2f; p * P(chi2_1 > thr) = %.4f" % (thr, p * math.exp(-thr / 2) / math.sqrt(math.pi * thr / 2)))
for (nn, pp) in [(200, 750), (400, 1790), (800, 4260), (1600, 10120), (10**4, int(1e4**1.25)), (10**6, int(1e6**1.25))]:
    t = 2 * (math.log((2 * pp - 6) / 6) + 0.5 * math.log(nn + 1))
    print("  n=%d p=%d: P((L) fails) ~ p P(chi2_1 > %.1f) = %.4f" % (nn, pp, t, pp * math.exp(-t / 2) / math.sqrt(math.pi * t / 2)))
