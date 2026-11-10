"""C1 (Opus seat): exact coded posterior for R03 §5A p=3 construction (specificity without beta-min).
x1, x2, u centred, mutually orthogonal, ||.||^2 = n-1; x3 = r(x1+x2)/sqrt2 + sqrt(1-r^2) u; r^2 = 0.9.
S0 = {1,2}, theta1 = theta2 = b sqrt(log n / n), b^2 = 0.75 (L = 1/2), sigma = 1. Score as coded (v3_score.h)."""
import itertools, math, sys
import numpy as np
def post(X, y):
    n, p = X.shape; K = min(p, n // 2); nu = 0.01 + n / 2
    G = X.T @ X; z = X.T @ y; yty = y @ y; out = {}
    for k in range(K + 1):
        lw = -math.log(2) - (math.lgamma(2*p) - math.lgamma(k+1) - math.lgamma(2*p-k))
        for S in itertools.combinations(range(p), k):
            if k == 0: out[S] = lw - nu*math.log(0.02 + yty); continue
            idx = list(S); Gs = G[np.ix_(idx, idx)]; H = (n+1)*Gs + np.eye(k); A = Gs + np.eye(k)
            Q = yty - n * z[idx] @ np.linalg.solve(H, z[idx])
            out[S] = lw - 0.5*(np.linalg.slogdet(H)[1] - np.linalg.slogdet(A)[1]) - nu*math.log(0.02 + max(Q, 0))
    m = max(out.values()); w = {S: math.exp(v - m) for S, v in out.items()}; Z = sum(w.values())
    return {S: v / Z for S, v in w.items()}
r2, b2 = 0.9, float(sys.argv[1]) if len(sys.argv) > 1 else 0.75
print(f"b2 = {b2}, r2 = {r2}"); print("n      med pi(S0)  med pi({3})  med PIP_3  P(HPM={3})   (20 seeds)")
for n in [100, 1000, 10000, 100000, 1000000]:
    res = []
    for sd in range(20):
        rng = np.random.default_rng(11 * n + sd)
        M = rng.standard_normal((n, 3)); M -= M.mean(0)
        Qm, _ = np.linalg.qr(M); Qm *= math.sqrt(n - 1)        # centred orthogonal, norm^2 = n-1
        x1, x2, u = Qm.T
        x3 = math.sqrt(r2) * (x1 + x2) / math.sqrt(2) + math.sqrt(1 - r2) * u
        X = np.column_stack([x1, x2, x3 / math.sqrt((x3 @ x3) / (n - 1))])
        th = math.sqrt(b2 * math.log(n) / n)
        yr = th * (x1 + x2) + rng.standard_normal(n)
        y = yr - yr.mean(); y = y / math.sqrt(y @ y / (n - 1))
        P = post(X, y)
        res.append((P[(0, 1)], P[(2,)], sum(v for S, v in P.items() if 2 in S), max(P, key=P.get) == (2,)))
    a = np.array(res, dtype=float)
    print(f"{n:7d}  {np.median(a[:,0]):.3e}  {np.median(a[:,1]):.3e}  {np.median(a[:,2]):.3e}  {a[:,3].mean():.2f}")
    sys.stdout.flush()
print("lambda_min of population Gram (normalised):", 1 - math.sqrt(r2))
