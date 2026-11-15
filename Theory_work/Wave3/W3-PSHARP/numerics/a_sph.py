"""W3-PSHARP numerics (a), spherical witness (W-sph): raw design with iid N(0,1) entries, p >> n.

delta_n cannot be enumerated at p >> n. What is computed EXACTLY is the one-step superset odds
    L1 := sum_{j not in S0} pi(S0 + j)/pi(S0)  <=  delta/(1 - delta)        (every omitted model has mass >= 0),
by the closed form of Lemma S:  pi(S0+j)/pi(S0) = [(s0+1)/(2p-1-s0)] (den_j/s_j)^{1/2} (1 - gamma_j)^{-nu},
  g_j = X_S0'x_j, s_j = n^2 - (n+1)^2 g_j'H^{-1}g_j, den_j = n - g_j'(G+I)^{-1}g_j, gamma_j = n (x_j'rho)^2/(s_j (2 b0 + Q_S0)).
Proposition A predicts L1/Lambda_n >= 1 - o_P(1), Lambda_n = (s0+1) [2N/(2p-1-s0)] sqrt(log N/(pi n)), N = p - s0.

V1  closed form vs generic linear algebra (log_score) on small cases.
D1  direct simulation: the full n x p Gaussian design is generated and standardised (chunked).
R1  larger p by an exact-in-law reduction: given (X_S0, y), a null column enters only through the projections of
    C x^r_j on span(X_S0, rho) (iid N(0, I_{s0+1})) and its remaining squared norm (chi^2_{n-2-s0}); R0 compares the
    reduction with the direct simulation at the same (n, p).
Run: py -3.13 -I a_sph.py > a_sph_out.txt
"""
import sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script directory
sys.dont_write_bytecode = True
import numpy as np
from core import B0, standardise, log_score, Lambda


def s0_block(n, s0, beta, rng):
    """Truth block: raw X0 iid N(0,1), y^r = X0 beta + eps; returns standardised X0, y and the S0 quantities."""
    X0r = rng.standard_normal((n, s0))
    yr = X0r @ np.full(s0, beta) + rng.standard_normal(n)
    X0, y = standardise(X0r, yr)
    G = X0.T @ X0
    H = (n + 1) * G + np.eye(s0)
    z0 = X0.T @ y
    Q = float(y @ y - n * z0 @ np.linalg.solve(H, z0))
    rho = y - (n + 1) * X0 @ np.linalg.solve(H, z0)
    return X0, y, G, H, Q, rho


def ratios(n, p, s0, G, H, Q, gmat, sc):
    """pi(S0+j)/pi(S0) for null columns given g_j (rows of gmat) and scores sc_j = x_j'rho."""
    nu = 0.01 + n / 2
    Hi, Ai = np.linalg.inv(H), np.linalg.inv(G + np.eye(s0))
    s = n * n - (n + 1) ** 2 * np.einsum("ij,jk,ik->i", gmat, Hi, gmat)
    den = n - np.einsum("ij,jk,ik->i", gmat, Ai, gmat)
    gam = n * sc ** 2 / (s * (2 * B0 + Q))
    return (s0 + 1) / (2 * p - 1 - s0) * np.sqrt(den / s) * np.exp(-nu * np.log1p(-gam))


def L1_direct(n, p, s0, beta, rng, chunk=20000):
    X0, y, G, H, Q, rho = s0_block(n, s0, beta, rng)
    tot, left = 0.0, p - s0
    while left > 0:
        m = min(chunk, left); left -= m
        Z = rng.standard_normal((n, m))
        Z -= Z.mean(0)
        Z *= math.sqrt(n - 1) / np.sqrt((Z ** 2).sum(0))
        tot += float(ratios(n, p, s0, G, H, Q, (X0.T @ Z).T, rho @ Z).sum())
    return tot


def L1_reduced(n, p, s0, beta, rng, chunk=2000000):
    X0, y, G, H, Q, rho = s0_block(n, s0, beta, rng)
    E, _ = np.linalg.qr(np.column_stack([X0, rho]))          # orthonormal basis of span(X0, rho), inside 1-perp
    XE, rE = X0.T @ E, rho @ E
    tot, left = 0.0, p - s0
    while left > 0:
        m = min(chunk, left); left -= m
        a = rng.standard_normal((m, s0 + 1))
        r = rng.chisquare(n - 2 - s0, m)
        sc_ = math.sqrt(n - 1) / np.sqrt((a ** 2).sum(1) + r)
        tot += float(ratios(n, p, s0, G, H, Q, (a @ XE.T) * sc_[:, None], (a @ rE) * sc_).sum())
    return tot


def summarise(tag, n, p, s0, vals):
    lam = Lambda(n, p, s0, p - s0)
    r = np.array(vals) / lam
    q = np.quantile(r, [0.25, 0.5, 0.75])
    print(f"  {tag} n={n:6d} p={p:9d} (log p/log n={math.log(p)/math.log(n):.2f}) s0={s0} reps={len(r):3d} | Lam={lam:.4f} |"
          f" L1/Lam: median {q[1]:.3f}, quartiles {q[0]:.3f} {q[2]:.3f}, min {r.min():.3f} |"
          f" P(>=0.9) {np.mean(r >= 0.9):.2f}, P(>=0.75) {np.mean(r >= 0.75):.2f}", flush=True)


def V1(rng):
    print("V1: closed form of pi(S0+j)/pi(S0) vs generic linear algebra")
    worst = 0.0
    for (n, p, s0) in ((20, 9, 2), (50, 12, 3), (200, 10, 1)):
        Xr = rng.standard_normal((n, p)); yr = Xr[:, :s0].sum(1) + rng.standard_normal(n)
        X, y = standardise(Xr, yr)
        X0 = X[:, :s0]; G = X0.T @ X0; H = (n + 1) * G + np.eye(s0); z0 = X0.T @ y
        Q = float(y @ y - n * z0 @ np.linalg.solve(H, z0)); rho = y - (n + 1) * X0 @ np.linalg.solve(H, z0)
        cf = ratios(n, p, s0, G, H, Q, (X0.T @ X[:, s0:]).T, rho @ X[:, s0:])
        l0 = log_score(X, y, range(s0))[0]
        br = np.array([math.exp(log_score(X, y, list(range(s0)) + [j])[0] - l0) for j in range(s0, p)])
        worst = max(worst, float(np.abs(cf / br - 1).max()))
    print(f"  max relative difference {worst:.1e}: {'PASS' if worst < 1e-8 else 'FAIL'}")


if __name__ == "__main__":  # (a_boundary imports ratios from this module)
    t0 = time.time()
    rng = np.random.default_rng(20261113)
    V1(rng)
    print("D1: direct simulation (full Gaussian design), beta = 1 on S0, sigma = 1")
    for (n, p) in ((100, 1000), (100, 10000), (400, 8000), (400, 160000)):
        for s0 in (1, 3):
            reps = 100 if n * p <= 4e6 else 40
            summarise("D1", n, p, s0, [L1_direct(n, p, s0, 1.0, rng) for _ in range(reps)])
    print(f"  [D1 done, {time.time()-t0:.0f}s]")
    print("R0: reduction vs direct at the same configuration (two independent samples; compare the rows)")
    for (n, p, s0) in ((100, 10000, 3), (400, 8000, 1)):
        summarise("R0-direct ", n, p, s0, [L1_direct(n, p, s0, 1.0, rng) for _ in range(100)])
        summarise("R0-reduced", n, p, s0, [L1_reduced(n, p, s0, 1.0, rng) for _ in range(100)])
    print("R1: exact-in-law reduction, larger n and p")
    for (n, p) in ((1600, 64000), (1600, 2560000), (6400, 512000), (6400, 40960000), (25600, 4096000)):
        for s0 in (1, 3):
            reps = 100 if p <= 3e6 else 30
            summarise("R1", n, p, s0, [L1_reduced(n, p, s0, 1.0, rng) for _ in range(reps)])
    print(f"  [all done, {time.time()-t0:.0f}s]")
