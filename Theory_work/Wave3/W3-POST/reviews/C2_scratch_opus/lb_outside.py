"""C2 seat B: LB outside its domain (p = s0 = 2, no feasible extension): delta can be far below 1/(1+sqrt(n+1))."""
import sys, math
import numpy as np
sys.path.insert(0, r"C:\Users\felip\Bayesian-Variable-Selection\Theory_work\Wave3\W3-POST\numerics")
from post_exact import Post, standardise
rng = np.random.default_rng(3)
n = 20
Z = rng.standard_normal((n, 2)); Z -= Z.mean(0)
Qm, _ = np.linalg.qr(np.column_stack([np.ones(n), Z])); X = Qm[:, 1:3] * math.sqrt(n - 1)
for th in [0.5, 1.0, 2.0]:
    y = X @ np.array([th, th]) + rng.standard_normal(n)
    X2, y2 = standardise(X, y); P = Post(X2, y2)
    print(f"n={n} p=s0=2 theta={th}: delta={1-P.mass((0,1)):.3e}  LB value={1/(1+math.sqrt(n+1)):.3e}")
