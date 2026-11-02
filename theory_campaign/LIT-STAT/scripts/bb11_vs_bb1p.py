"""LIT-STAT: per-model weights of BB(1,1) (Rossell 2022 / Scott-Berger) vs BB(1,p) (ours). Exact rationals, deterministic.
w11(k) = 1/((p+1) C(p,k));  w1p(k) = 1/(2 C(2p-1,k)).
Checks: per-model ratios w(k+1)/w(k): (k+1)/(p-k) vs (k+1)/(2p-1-k)  (same order 1/p per variable);
and w1p(k)/w11(k) = (p+1) C(p,k) / (2 C(2p-1,k)), compared with (p+1)/2 * 2^{-k}  (BB(1,p) = BB(1,1) x geometric size tilt)."""
from fractions import Fraction as F
from math import comb
for p in (500, 1000):
    print(f"p={p}")
    for k in (0, 1, 5, 14, 30, 100):
        w11 = F(1, (p+1)*comb(p, k)); w1p = F(1, 2*comb(2*p-1, k))
        r11 = F(1, (p+1)*comb(p, k+1))/w11; r1p = F(1, 2*comb(2*p-1, k+1))/w1p
        assert r11 == F(k+1, p-k) and r1p == F(k+1, 2*p-1-k)
        tilt = (w1p/w11) / (F(p+1, 2) * F(1, 2**k))
        print(f"  k={k:3d}: ratio BB11={float(r11):.3e} BB1p={float(r1p):.3e}  [w1p/w11]/[(p+1)/2*2^-k]={float(tilt):.4f}")
