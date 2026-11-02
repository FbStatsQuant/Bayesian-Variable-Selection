"""W5-B2ENV r0: numerical spot checks for the referee report on W4-SHARE.  Seed 20261102.

§1  D4 Step 5: g(u) = 1/(1-e^{-u}) - 1/u increasing from 1/2 to 1; 1/theta_0 recursion vs the two closed bounds.
§2  Prop SH(iii): exact one-stage law P(n_1(W)=0) = E[(1 - n0/(n0 + (N-n0)e^kappa))^N], location of the 50% point.
§3  Prop M(a): max_j delta_{T,j}^2 >= (n-1) lam^2 ||theta_M||_2^4/||theta_M||_1^2 on random instances.
"""
import numpy as np
from math import exp, log, lgamma

rng = np.random.default_rng(20261102)
out = []
pr = lambda s: (out.append(s), print(s))

# §1
u = np.logspace(-6, 3, 20001)
x = u / 2  # g(u) = 1/2 + (coth(x) - 1/x)/2 (Langevin form); series for small x avoids cancellation
lang = np.where(x < 1e-2, x / 3 - x ** 3 / 45 + 2 * x ** 5 / 945, 1 / np.tanh(np.maximum(x, 1e-300)) - 1 / np.maximum(x, 1e-300))
g = 0.5 + 0.5 * lang
pr(f"§1 g(u): min {g.min():.6f} max {g.max():.6f}  monotone increasing: {bool(np.all(np.diff(g) >= -1e-12))}  g(1) = {1/(1-exp(-1))-1:.6f} = 1/(e-1) = {1/(np.e-1):.6f}")
worst = 0.0
for rep in range(2000):
    T = rng.integers(1, 60)
    Pl = np.sort(rng.uniform(1e-3, 1, T))[::-1] if rep % 2 == 0 else rng.uniform(1e-3, 1, T)
    th = np.inf
    for t in range(T - 1, -1, -1):
        th = Pl[t] * (1 - exp(-th / Pl[t])) if np.isfinite(th) else Pl[t]
    inv = 1 / th
    b1 = np.sum(1 / Pl)
    worst = max(worst, inv / b1)
    if rep % 2 == 0:
        b2 = 1 / Pl[-1] + np.sum(1 / Pl[:-1]) / (np.e - 1)
        assert inv <= b2 * (1 + 1e-12), (inv, b2)
pr(f"   1/theta_0 <= sum 1/P_t: worst ratio {worst:.4f} (<= 1); monotone-form bound held in 1000/1000 non-increasing cases")

# §2
def p_fail(N, pa, kap):
    n0 = np.arange(N + 1)
    lgf = np.array([lgamma(k + 1) for k in range(N + 1)])
    lp = lgf[N] - lgf - lgf[::-1] + n0 * log(pa) + (N - n0) * log(1 - pa)
    om = n0 / (n0 + (N - n0) * exp(kap))
    return float(np.sum(np.exp(lp) * (1 - om) ** N))

for N, pa in [(1000, 0.5), (10000, 0.5), (10000, 0.99)]:
    ks = np.linspace(0, 3 * log(N), 600)
    pf = np.array([p_fail(N, pa, k) for k in ks])
    k50 = ks[np.argmin(np.abs(pf - 0.5))]
    pr(f"§2 N={N} pi0(a)={pa}: 50% point kappa={k50:.2f};  log(N pi0(a)/pi0(o)) = {log(N*pa/(1-pa)):.2f};  "
       f"log(N pi0(a)) = {log(N*pa):.2f};  2 log N = {2*log(N):.2f}")

# §3
viol = 0; minratio = np.inf
for rep in range(20000):
    k = rng.integers(2, 7); n = 50
    A = rng.standard_normal((n, k)) @ np.linalg.cholesky(np.eye(k) * 0.3 + 0.7 * rng.uniform(0, 1) * np.ones((k, k))).T
    A -= A.mean(0); A /= np.sqrt((A ** 2).sum(0) / (n - 1))
    s0 = rng.integers(1, k + 1)
    S0 = list(range(s0)); th = np.zeros(k); th[S0] = rng.standard_normal(s0) * 2
    mu = A @ th
    Tsz = rng.integers(0, k)
    T = sorted(rng.choice(k, Tsz, replace=False).tolist())
    M = [j for j in S0 if j not in T]
    if not M:
        continue
    R = A.T @ A / (n - 1)
    lam = np.linalg.eigvalsh(R[np.ix_(sorted(set(T) | set(M)), sorted(set(T) | set(M)))]).min()
    if lam <= 1e-8:
        continue
    if T:
        XT = A[:, T]; P = XT @ np.linalg.pinv(XT)
    else:
        P = np.zeros((n, n))
    deltas = []
    for j in M:
        xt = A[:, j] - P @ A[:, j]
        deltas.append((xt @ mu) ** 2 / (xt @ xt))
    lhs = max(deltas)
    rhs = (n - 1) * lam ** 2 * np.sum(th[M] ** 2) ** 2 / np.sum(np.abs(th[M])) ** 2
    minratio = min(minratio, lhs / rhs)
    if lhs < rhs * (1 - 1e-9):
        viol += 1
pr(f"§3 Prop M(a): violations {viol}; min LHS/RHS = {minratio:.4f}")
open(__file__.replace(".py", ".txt"), "w").write("\n".join(out) + "\n")
