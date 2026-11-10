"""C2 seat B: adversarial near-tight cases for Proposition LB. p = s0+1, extra column orthogonal to X_S0 and y."""
import sys, math, itertools
import numpy as np
sys.path.insert(0, r"C:\Users\felip\Bayesian-Variable-Selection\Theory_work\Wave3\W3-POST\numerics")
from post_exact import Post, standardise
rng = np.random.default_rng(7)
worst = math.inf
for n in [6, 8, 10, 20, 100, 1000, 10000]:
    for s0 in [1, 2, 3]:
        p = s0 + 1
        if s0 + 1 > min(p, n // 2):
            continue
        for amp in [3.0, 30.0, 300.0]:
            Z = rng.standard_normal((n, p + 1)); Z -= Z.mean(0)
            Qm, _ = np.linalg.qr(np.column_stack([np.ones(n), Z]))
            B = Qm[:, 1:p + 2] * math.sqrt(n - 1)   # orthonormal centred columns, norm^2 = n-1
            X = B[:, :p]
            y = X[:, :s0] @ (amp * np.ones(s0)) + 1e-3 * B[:, p]  # y in span of S0 (plus a tiny orthogonal bit)
            X2, y2 = standardise(X, y)
            P = Post(X2, y2)
            v = (1 - P.mass(tuple(range(s0)))) * (1 + math.sqrt(n + 1))
            worst = min(worst, v)
            print(f"n={n:6d} s0={s0} amp={amp:6.1f}  (1-pi(S0))(1+sqrt(n+1)) = {v:.6f}")
print("min", worst)
