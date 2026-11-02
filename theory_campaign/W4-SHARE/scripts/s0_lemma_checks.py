"""W4-SHARE s0: numerical checks of the elementary facts used in PROOF.md.

(a) g(u) = 1/(1-e^{-u}) - 1/u is increasing on (0, inf), g(0+) = 1/2, g(1) = 1/(e-1), g(inf) = 1.
(b) P -> P (1 - exp(-theta/P)) is non-decreasing in P > 0.
(c) The theta-recursion of D4: 1/theta_0 <= 1/Pl_T + (e-1)^{-1} sum_{t<T} 1/Pl_t for non-increasing envelopes,
    and <= sum_t 1/Pl_t in general (random envelopes).
(d) Exactness of the D4 generating-function step against brute force: for a chain n' ~ Bin(N, n r/N) (r <= 1),
    P(n_T = 0) <= (1 - f0 (1 - e^{-theta_0}))^N with n_0 ~ Bin(N, f0)  (exact DP over counts, small N).
(e) Proposition M(a): max_j delta_{T,j}^2 >= (n-1) lam^2 ||th_M||_2^4 / ||th_M||_1^2 on random designs.
Seed 20261102.
"""
import numpy as np
from math import comb

rng = np.random.default_rng(20261102)
out = []

# (a)
u = np.logspace(-6, 3, 20001)
# stable evaluation: series 1/2 + u/12 - u^3/720 for u < 1e-2 (cancellation otherwise)
g = np.where(u < 1e-2, 0.5 + u / 12 - u ** 3 / 720, 1.0 / (-np.expm1(-np.maximum(u, 1e-2))) - 1.0 / np.maximum(u, 1e-2))
out.append(f"(a) g increasing: {bool(np.all(np.diff(g) > -1e-12))}; g(1e-6)={g[0]:.6f}; "
           f"g(1)={1/(-np.expm1(-1.0))-1:.6f} vs 1/(e-1)={1/(np.e-1):.6f}; g(1e3)={g[-1]:.6f}")

# (b)
viol = 0
for _ in range(2000):
    th = 10 ** rng.uniform(-3, 3)
    P = np.sort(10 ** rng.uniform(-4, 4, 50))
    f = P * (-np.expm1(-th / P))
    viol += int(np.any(np.diff(f) < -1e-12 * np.abs(f[1:])))
out.append(f"(b) monotonicity violations: {viol} / 2000")


def theta0(Pl):
    th = np.inf
    for P in Pl[::-1]:
        th = P if np.isinf(th) else P * (-np.expm1(-th / P))
    return th


worst_mono, worst_gen = 0.0, 0.0
for _ in range(5000):
    T = int(rng.integers(1, 200))
    Pl = np.exp(-np.cumsum(rng.exponential(rng.uniform(0, 0.05), T)))  # non-increasing
    th = theta0(Pl)
    bound = 1 / Pl[-1] + (1 / (np.e - 1)) * np.sum(1 / Pl[:-1])
    worst_mono = max(worst_mono, (1 / th) / bound)
    Pr = np.exp(rng.normal(0, 1, T))  # arbitrary positive envelope
    worst_gen = max(worst_gen, (1 / theta0(Pr)) / np.sum(1 / Pr))
out.append(f"(c) max ratio (1/theta0)/bound: monotone form {worst_mono:.6f} (<=1), general form {worst_gen:.6f} (<=1)")

# (d) exact DP: n_{t+1} | n_t ~ Bin(N, n_t r_t / N), r_t <= 1 deterministic; compare exact P(n_T=0) with D4 bound
worst = 0.0
for trial in range(200):
    N = int(rng.integers(5, 40)); T = int(rng.integers(1, 30)); f0 = rng.uniform(0.05, 1.0)
    r = np.exp(-rng.exponential(0.1, T)); r = np.minimum(r, 1.0)
    dist = np.array([comb(N, k) * f0 ** k * (1 - f0) ** (N - k) for k in range(N + 1)])
    for t in range(T):
        new = np.zeros(N + 1)
        for k in range(N + 1):
            if dist[k] == 0: continue
            w = k * r[t] / N
            new += dist[k] * np.array([comb(N, j) * w ** j * (1 - w) ** (N - j) for j in range(N + 1)])
        dist = new
    exact = dist[0]
    Pl = np.cumprod(r)
    th = theta0(Pl)
    bound = (1 - f0 * (-np.expm1(-th))) ** N
    worst = max(worst, exact / bound)
out.append(f"(d) max exact/bound over 200 random chains: {worst:.6f} (<=1 required)")

# (e) Proposition M(a)
worst = np.inf
for _ in range(3000):
    n = int(rng.integers(20, 200)); s0 = int(rng.integers(1, 6)); kT = int(rng.integers(0, 6))
    q = s0 + kT + int(rng.integers(0, 4))
    A = rng.normal(size=(q, q)); C = A @ A.T + rng.uniform(0.01, 1) * np.eye(q)
    L = np.linalg.cholesky(C)
    X = rng.normal(size=(n, q)) @ L.T
    X -= X.mean(0); X /= np.sqrt((X ** 2).sum(0) / (n - 1))
    S0 = list(range(s0)); th = np.zeros(q); th[S0] = rng.normal(size=s0) * rng.uniform(0.1, 3)
    mu = X @ th
    # T: a random proper subset of S0 plus some extras
    keep = [j for j in S0 if rng.random() < 0.5]
    if len(keep) == s0: keep = keep[:-1]
    extras = list(rng.choice(range(s0, q), size=min(kT, q - s0), replace=False)) if q > s0 else []
    T = keep + extras; M = [j for j in S0 if j not in T]
    R = (X.T @ X) / (n - 1)
    idx = T + M
    lam = np.linalg.eigvalsh(R[np.ix_(idx, idx)])[0]
    if T:
        Q, _ = np.linalg.qr(X[:, T]); P = Q @ Q.T
    else:
        P = np.zeros((n, n))
    d2 = []
    for j in M:
        xt = X[:, j] - P @ X[:, j]
        d2.append((xt @ mu) ** 2 / (xt @ xt))
    lhs = max(d2)
    rhs = (n - 1) * lam ** 2 * np.sum(th[M] ** 2) ** 2 / np.sum(np.abs(th[M])) ** 2
    worst = min(worst, lhs / rhs)
out.append(f"(e) Prop M(a): min LHS/RHS over 3000 random cases = {worst:.8f} (>=1 required)")

print("\n".join(out))
