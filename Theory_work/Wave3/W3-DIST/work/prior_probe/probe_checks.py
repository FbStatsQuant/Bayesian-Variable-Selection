#!/usr/bin/env python3
"""W3-DIST prior probe: small falsification checks (no cluster, a few seconds).

C1  exact BB(1,p) size law q_k = C(p,k)/(2 C(2p-1,k)) vs 2^{-k-1}; tail bracket; successive ratio.
C2  Song-Liang B(r), B~ for the coded slab V_S = n (G_S + I)^{-1} (duplicate column => B~ = n).
C3  algebra used in REPORT Q3 (Lemma V), on adversarial designs (weak directions inside S0,
    near-collinear J, exact duplicates):
      (a) Delta := Q_S0(y) - Q_S(y) <= e'D'e + (1 + 2/eta) rho',  D' := M_S^{(1/(1+eta))} - M_S0^{(1+eta)},
          rho' := theta*'(G_S0 + I)theta*/n,  y = mu + e,  mu = X_S0 theta*;
      (b) D' >= 0  and  det(I - D')^{-1/2} (D_S0/D_S)^{1/2} <= (1+eta)^{(s0+|S|)/2}.
C4  exact posterior size law (full enumeration) for s0 = 1 and q null columns that are
    near-duplicates of x1 with orthogonal residuals, residual (Schur) eigenvalue gamma = kappa/(n+1);
    compared with independent null columns (full Occam factor).
"""
import itertools, math
import numpy as np

rng = np.random.default_rng(20261115)

def logC(a, b):
    return math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)

# ---------------- C1 ----------------
print("C1  BB(1,p) size law")
for p in [10, 100, 10**4, 10**6]:
    q = [0.5 * math.exp(logC(p, k) - logC(2 * p - 1, k)) if k <= p else 0.0 for k in range(0, 41)]
    ks = [0, 1, 2, 5, 10, 20, 40]
    ratio = [q[k] / 2 ** (-k - 1) for k in ks if k <= min(p, 40)]
    tail = lambda m: sum(q[m + 1:])  # truncated at 40, fine for display
    br = [(m, 2.0 ** (-m - 3), tail(m), 2.0 ** (-m) * p / (2 * p - 1)) for m in [0, 2, 5, 10] if m + 1 <= p]
    print(f"  p={p:>8}: q_k/2^(-k-1) at k={ks}: " + ", ".join(f"{r:.4f}" for r in ratio))
    print("            tail bracket (m, 2^-(m+3), P(|S|>m) [k<=40], 2^-m p/(2p-1)): " +
          "; ".join(f"({m}, {a:.2e}, {b:.2e}, {c:.2e})" for m, a, b, c in br))
    rr = [q[k] / q[k - 1] for k in [1, 2, 3, 10] if k <= p]
    print("            q_k/q_(k-1) at k=1,2,3,10: " + ", ".join(f"{r:.4f}" for r in rr))

# ---------------- helpers ----------------
def std_design(Z):
    Z = Z - Z.mean(0)
    return Z * np.sqrt((Z.shape[0] - 1) / (Z ** 2).sum(0))

def ridge_M(X, c, n):
    """M^{(c)} = X (G + c (G+I)/n)^{-1} X'  (c = 1 is the coded M_S = n X H^{-1} X')."""
    if X.shape[1] == 0:
        return np.zeros((X.shape[0], X.shape[0]))
    G = X.T @ X
    A = G + c * (G + np.eye(G.shape[0])) / n
    return X @ np.linalg.solve(A, X.T)

def logD(X, n):
    if X.shape[1] == 0:
        return 0.0
    G = X.T @ X
    k = G.shape[0]
    return np.linalg.slogdet((n + 1) * G + np.eye(k))[1] - np.linalg.slogdet(G + np.eye(k))[1]

def Q(X, y, n):
    return float(y @ y - y @ ridge_M(X, 1.0, n) @ y)

# ---------------- C2 ----------------
print("\nC2  Song-Liang B(r), B~ for V_S = n (G_S+I)^{-1}")
n = 200
Z = rng.standard_normal((n, 30)); Z[:, 1] = Z[:, 0]  # an exact duplicate
X = std_design(Z)
for S in [[0], [0, 2], [0, 1], list(range(2, 12))]:
    G = X[:, S].T @ X[:, S]
    ev = np.linalg.eigvalsh(G)
    print(f"  S={S if len(S) < 5 else str(len(S))+' indep cols'}: ch1(V^-1)=(lmax+1)/n={(ev[-1]+1)/n:.3f} (<= |S|+1),"
          f" ch1(V)=n/(lmin+1)={n/(ev[0]+1):.3f} (<= n={n})")

# ---------------- C3 ----------------
print("\nC3  Lemma V algebra on adversarial designs")
def make_design(n, s0, j, kind):
    Z = rng.standard_normal((n, s0 + j))
    if kind == "weakS0" and s0 >= 2:      # near-collinear pair inside S0 (tiny Schur eigenvalue)
        Z[:, 1] = Z[:, 0] + 1e-3 * rng.standard_normal(n) / np.sqrt(n)
    if kind == "nearJ":                   # J near-duplicates of S0 columns
        for t in range(j):
            Z[:, s0 + t] = Z[:, t % s0] + 0.05 / np.sqrt(n) * rng.standard_normal(n)
    if kind == "dupJ":                    # exact duplicate in J
        Z[:, s0] = Z[:, 0]
    return std_design(Z)

worst_a, worst_b, min_eig = -np.inf, -np.inf, np.inf
for trial in range(400):
    n = int(rng.choice([30, 80, 200]))
    s0 = int(rng.choice([1, 2, 3])); j = int(rng.choice([1, 2, 4]))
    kind = rng.choice(["plain", "weakS0", "nearJ", "dupJ"])
    eta = float(rng.choice([0.1, 0.5, 1.0, 3.0]))
    X = make_design(n, s0, j, kind)
    X0, XS = X[:, :s0], X
    if kind == "weakS0" and s0 >= 2:
        th = np.zeros(s0); th[0], th[1] = 50.0, -50.0   # large coefficients on the weak direction
        th[2:] = rng.standard_normal(s0 - 2)
    else:
        th = rng.standard_normal(s0) * 2
    mu = X0 @ th
    rho = float(th @ (X0.T @ X0 + np.eye(s0)) @ th / n)
    c = 1 + eta
    Dp = ridge_M(XS, 1 / c, n) - ridge_M(X0, c, n)
    min_eig = min(min_eig, np.linalg.eigvalsh((Dp + Dp.T) / 2)[0])
    for _ in range(5):
        e = rng.standard_normal(n) * float(rng.choice([0.5, 1, 3]))
        y = mu + e
        lhs = Q(X0, y, n) - Q(XS, y, n)
        rhs = float(e @ Dp @ e) + (1 + 2 / eta) * rho
        worst_a = max(worst_a, lhs - rhs)
    # (b): note the e-free statement; D' has eigenvalues < 1
    ld = np.linalg.slogdet(np.eye(n) - Dp)
    assert ld[0] > 0
    lhs_b = -0.5 * ld[1] + 0.5 * (logD(X0, n) - logD(XS, n))
    rhs_b = 0.5 * (s0 + XS.shape[1]) * math.log(c)
    worst_b = max(worst_b, lhs_b - rhs_b)
print(f"  (a) max over 2000 draws of Delta - [e'D'e + (1+2/eta)rho'] = {worst_a:.3e}  (claim: <= 0)")
print(f"  (b) min eigenvalue of D' = {min_eig:.3e} (claim >= 0, up to rounding);"
      f" max log[det(I-D')^-1/2 (D0/DS)^1/2] - log[(1+eta)^((s0+|S|)/2)] = {worst_b:.3e} (claim <= 0)")

# ---------------- C4 ----------------
print("\nC4  exact posterior size law, s0=1, q near-duplicate nulls (orthogonal residuals) vs independent nulls")
def post_size(X, y, n, K):
    """Exact pi(|S|=k) by enumeration, using G = X'X and z = X'y only."""
    p = X.shape[1]
    nu = 0.01 + n / 2
    Gf, zf, yy = X.T @ X, X.T @ y, float(y @ y)
    logw = lambda k: -math.log(2) - logC(2 * p - 1, k)
    mass = np.full(K + 1, -np.inf)
    for k in range(0, K + 1):
        vals = []
        for S in itertools.combinations(range(p), k):
            S = list(S)
            if k == 0:
                ld, QS = 0.0, yy
            else:
                G = Gf[np.ix_(S, S)]; z = zf[S]; I = np.eye(k)
                H = (n + 1) * G + I
                ld = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + I)[1]
                QS = yy - n * float(z @ np.linalg.solve(H, z))
            vals.append(logw(k) - 0.5 * ld - nu * math.log(0.02 + QS))
        vals = np.array(vals)
        mass[k] = vals.max() + math.log(np.exp(vals - vals.max()).sum())
    mass -= mass.max()
    pr = np.exp(mass); return pr / pr.sum()

n, q = 1500, 11
p = q + 1
K = p  # cap inactive at this p (K = min(p, n/2))
# orthonormal basis of 1-perp
B = np.linalg.qr(np.column_stack([np.ones(n), rng.standard_normal((n, q + 1))]))[0][:, 1:]
u0, U = B[:, 0], B[:, 1:]
for label, kappa in [("kappa=0.5", 0.5), ("kappa=2", 2.0), ("kappa=log n", math.log(n)), ("indep", None)]:
    if kappa is None:
        X = np.column_stack([np.sqrt(n - 1) * u0] + [np.sqrt(n - 1) * U[:, t] for t in range(q)])
    else:
        gam = kappa / (n + 1); eta_ = gam / (n - 1)
        X = np.column_stack([np.sqrt(n - 1) * u0] +
                            [np.sqrt(n - 1) * (np.sqrt(1 - eta_) * u0 + np.sqrt(eta_) * U[:, t]) for t in range(q)])
    sizes = []
    for seed in range(4):
        r2 = np.random.default_rng(100 + seed)
        yr = 0.3 * X[:, 0] + r2.standard_normal(n)
        y = (yr - yr.mean()); y = y / np.sqrt((y ** 2).sum() / (n - 1))
        sizes.append(post_size(X, y, n, min(K, 7)))
    S = np.mean(sizes, 0)
    print(f"  {label:>12}: mean over 4 seeds of pi(|S|=k), k=0..7: " + " ".join(f"{v:.2e}" for v in S))
print("  reference: geometric (k)(q/2p)^(k-1)-type decay vs Occam n^{-(k-1)/2} ~ " + f"{n**-0.5:.1e} per extra variable")
