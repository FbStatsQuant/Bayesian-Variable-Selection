"""Proposition LB needs a feasible one-variable extension of S0 (1 <= s0 < p, s0+1 <= K). Outside that domain it can
fail: p = s0 = 2, exactly orthogonal centred columns, standardised y = (x1 + x2)/sqrt(2) (noise-free). Exact coded
posterior (post_exact.Post). Reproduces the C2 seat-A counterexample (reviews/C2_council_astra.md, F1).
Run: py -3.13 -I lb_domain.py"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from post_exact import Post, standardise

for n in [6, 20, 100]:
    rng = np.random.default_rng(1)
    Z = rng.standard_normal((n, 2))
    Z = Z - Z.mean(0)
    Q, _ = np.linalg.qr(Z)                     # orthonormal, centred columns
    X, _ = standardise(Q, rng.standard_normal(n))
    yr = (X[:, 0] + X[:, 1]) / math.sqrt(2)
    X2, y = standardise(X, yr)
    P = Post(X2, y)
    d = 1 - P.mass((0, 1))
    print(f"n={n:4d} p=s0=2: 1-pi(S0) = {d:.4e}   LB value 1/(1+sqrt(n+1)) = {1 / (1 + math.sqrt(n + 1)):.4e}   "
          f"max |x1'x2|/(n-1) = {abs(X2[:, 0] @ X2[:, 1]) / (n - 1):.1e}")
