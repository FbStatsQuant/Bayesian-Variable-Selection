"""LIT-STAT: exact BB(1,p) size-prior ratios vs the CSvdV (2015) exponential-decrease condition (2.2).
Checks: (a) w(k) = 1/2 / C(2p-1,k) equals B(k+1, 2p-k)/B(1,p) (BB(1,p) per-model weight);
(b) dimension ratio pi_p(s)/pi_p(s-1) = (p-s+1)/(2p-s) (~1/2), hence the implied A4 = -log(ratio)/log p -> 0;
(c) per-model ratio w(k+1)/w(k) = (k+1)/(2p-1-k). Exact rational arithmetic; deterministic (no randomness, seed unused)."""
from fractions import Fraction as F
from math import comb, log, factorial
def B(a, b):  # Beta function for positive integers, exact
    return F(factorial(a-1)*factorial(b-1), factorial(a+b-1))
out = []
for p in (20, 500, 1000):
    ok = all(F(1, 2*comb(2*p-1, k)) == B(k+1, 2*p-k)/B(1, p) for k in range(0, min(p, 60)+1))
    dim = lambda s: comb(p, s)*F(1, 2*comb(2*p-1, s))
    rows = []
    for s in (1, 2, 5, 14, 50, 100):
        if s > p: continue
        r = dim(s)/dim(s-1); assert r == F(p-s+1, 2*p-s)
        A4 = -log(float(r))/log(p)
        wr = F(1, 2*comb(2*p-1, s))/F(1, 2*comb(2*p-1, s-1)); assert wr == F(s, 2*p-s)
        rows.append(f"  s={s:3d}: dim ratio={float(r):.4f}  implied A4={A4:.4f}  per-model w(s)/w(s-1)={float(wr):.3e}")
    out.append(f"p={p}: identity (a) holds for k<=min(p,60): {ok}\n" + "\n".join(rows))
print("\n".join(out))
