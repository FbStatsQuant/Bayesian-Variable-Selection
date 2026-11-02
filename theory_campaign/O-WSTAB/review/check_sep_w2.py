"""Independent reviewer check (does NOT import wstab_core): scores built directly from 00_COMMON §1-2.
Checks (1) the ORTH log-gamma_w formula of REPORT §3.5, (2) Lemma SEP bound, (3) Lemma W2 sandwich under BO with
correlated blocks, (4) Prop L(ii) identity.  Seed 20261102, p <= 10, single core."""
import itertools, math
import numpy as np
from scipy.special import gammaln, logsumexp

rng = np.random.default_rng(20261102)
b0 = 0.01

def standardise(Xr, yr):
    n = Xr.shape[0]
    X = Xr - Xr.mean(0); X = X / X.std(0, ddof=1)
    y = yr - yr.mean(); y = y / y.std(ddof=1)
    return X, y

def logBF(X, y, S):
    n = X.shape[0]; nu = 0.01 + n / 2; Qbar = 2 * b0 + y @ y
    if len(S) == 0: return 0.0
    XS = X[:, list(S)]; G = XS.T @ XS; H = (n + 1) * G + np.eye(len(S)); z = XS.T @ y
    D = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(len(S)))[1]
    Q = y @ y - n * z @ np.linalg.solve(H, z)
    return -0.5 * D - nu * (math.log(2 * b0 + Q) - math.log(Qbar))

def logw(k, p):  # log w(k) = log(1/2) - log C(2p-1,k)
    return math.log(0.5) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))

def tables(X, y, blocks):
    p = X.shape[1]; subs = list(itertools.chain.from_iterable(itertools.combinations(range(p), k) for k in range(p + 1)))
    lbf = {S: logBF(X, y, S) for S in subs}
    bl = {j: b for b, C in enumerate(blocks) for j in C}
    lr = {S: sum(lbf[tuple(sorted(j for j in S if bl[j] == b))] for b in range(len(blocks))) for S in subs}
    return subs, lbf, lr

def loggam(w, subs, lbf, lr, p):
    return np.array([logw(len(S), p) + w * lbf[S] + (1 - w) * lr[S] for S in subs])

def ell(w, S0, subs, lbf, lr, p):
    lg = loggam(w, subs, lbf, lr, p); return logsumexp(lg) - lg[subs.index(S0)]

def orth_design(n, p, theta, sig):
    A = rng.standard_normal((n, p)); A -= A.mean(0)
    Qm, _ = np.linalg.qr(A); X = Qm * math.sqrt(n - 1)
    yr = X @ theta + sig * rng.standard_normal(n)
    return standardise(X, yr) if False else (X, (yr - yr.mean()) / (yr - yr.mean()).std(ddof=1))

out = []
# ---- (1),(2) ORTH: formula and SEP
worst_formula = 0.0; sep_rows = []
for (n, p, s0, amp, blocks_kind) in [(40, 8, 2, 0.6, 'pairs'), (200, 9, 2, 0.4, 'triples'), (1000, 10, 3, 0.3, 'random'),
                                      (5000, 10, 1, 0.5, 'single'), (400, 10, 2, 1.5, 'pairs'), (20000, 9, 2, 0.25, 'triples')]:
    theta = np.zeros(p); S0 = tuple(range(s0)); theta[:s0] = amp
    X, y = orth_design(n, p, theta, 1.0)
    assert np.allclose(X.T @ X, (n - 1) * np.eye(p))
    perm = list(rng.permutation(p))
    if blocks_kind == 'pairs': blocks = [perm[i:i + 2] for i in range(0, p, 2)]
    elif blocks_kind == 'triples': blocks = [perm[i:i + 3] for i in range(0, p, 3)]
    elif blocks_kind == 'single': blocks = [[j] for j in range(p)]
    else:
        cuts = sorted(rng.choice(range(1, p), 3, replace=False)); blocks = [list(a) for a in np.split(np.array(perm), cuts)]
    subs, lbf, lr = tables(X, y, blocks)
    nu = 0.01 + n / 2; Qbar = 2 * b0 + y @ y
    xj = (X.T @ y) ** 2 / n / Qbar
    g = lambda z: -math.log1p(-z)
    bl = {j: b for b, C in enumerate(blocks) for j in C}
    for w in [0.0, 0.5, 1.0, 1.5, 2.0]:
        lg = loggam(w, subs, lbf, lr, p)
        for i, S in enumerate(subs):
            XS = sum(xj[list(S)]) if S else 0.0
            f = logw(len(S), p) - len(S) / 2 * math.log(n) + w * nu * g(XS) + (1 - w) * nu * sum(
                g(sum(xj[[j for j in S if bl[j] == b]])) for b in range(len(blocks)))
            worst_formula = max(worst_formula, abs(f - lg[i]))
        s = xj[list(S0)].sum(); Nn = [j for j in range(p) if j not in S0]; ubar = xj[Nn].sum() / (1 - s)
        beta = 1 / ((1 - s) * (1 - ubar)) if w <= 1 else w / ((1 - s) * (1 - ubar)) - (w - 1)
        q = sum(n ** -0.5 * math.exp(beta * nu * xj[j]) for j in Nn) / p
        l = ell(w, S0, subs, lbf, lr, p)
        if q < 1 and ubar < 1:
            bound = sum(math.log1p(2 * p * math.sqrt(n) * math.exp(-nu * xj[j])) for j in S0) - (s0 + 1) * math.log1p(-q)
            sep_rows.append((n, p, s0, blocks_kind, w, l, bound, l <= bound + 1e-9))
        else:
            sep_rows.append((n, p, s0, blocks_kind, w, l, float('inf'), True))
out.append(f"(1) ORTH log gamma_w formula (REPORT 3.5): max |formula - direct| over 6 designs x 5 w x all S = {worst_formula:.2e}")
out.append("(2) Lemma SEP: n p s0 blocks w | ell(w) | SEP bound | ok")
for r in sep_rows: out.append("    %6d %2d %d %-7s %.1f | %.5g | %.5g | %s" % r)
out.append(f"    SEP violations: {sum(not r[-1] for r in sep_rows)} of {len(sep_rows)}; finite-bound cases: {sum(math.isfinite(r[6]) for r in sep_rows)}")

# ---- (3) W2 sandwich under BO with correlated blocks
viol = 0; cnt = 0; maxrel = 0.0
for trial in range(6):
    n = int(rng.choice([60, 300, 2000])); p = 8; blocks = [[0, 1, 2], [3, 4], [5, 6, 7]]
    # block-orthogonal, within-block correlated: orthonormal basis, then mix inside blocks
    A = rng.standard_normal((n, p)); A -= A.mean(0); Qm, _ = np.linalg.qr(A)
    X = np.zeros((n, p))
    for C in blocks:
        M = rng.standard_normal((len(C), len(C))) + 2 * np.eye(len(C)); X[:, C] = Qm[:, C] @ M
    X = X / X.std(0, ddof=1)
    for C1, C2 in itertools.combinations(blocks, 2): assert np.abs(X[:, C1].T @ X[:, C2]).max() < 1e-8
    theta = np.zeros(p); theta[[0, 3]] = rng.uniform(0.2, 1.0, 2)
    yr = X @ theta + rng.standard_normal(n); y = (yr - yr.mean()) / (yr - yr.mean()).std(ddof=1)
    subs, lbf, lr = tables(X, y, blocks)
    nu = 0.01 + n / 2; Qbar = 2 * b0 + y @ y
    def t(S):
        if not S: return 0.0
        XS = X[:, list(S)]; H = (n + 1) * XS.T @ XS + np.eye(len(S)); z = XS.T @ y; return n * z @ np.linalg.solve(H, z)
    bl = {j: b for b, C in enumerate(blocks) for j in C}
    for So in [(0,), (0, 3), (0, 3, 5), (1, 4, 6)]:
        for l in range(p):
            if l in So: continue
            T = tuple(j for j in So if bl[j] == bl[l]); Tl = tuple(sorted(T + (l,))); Sl = tuple(sorted(So + (l,)))
            d = lambda S: lbf[S] - lr[S]
            LR = d(Sl) - d(So)
            xbar = t(So) / Qbar; xT = t(T) / Qbar; yy = (t(Tl) - t(T)) / (Qbar - t(So)); kap = (xbar - xT) / (1 - xT)
            G = lbf[Sl] - lbf[So] + 0.5 * (np.linalg.slogdet((n + 1) * X[:, list(Tl)].T @ X[:, list(Tl)] + np.eye(len(Tl)))[1]
                                           - np.linalg.slogdet(X[:, list(Tl)].T @ X[:, list(Tl)] + np.eye(len(Tl)))[1]
                                           - (np.linalg.slogdet((n + 1) * X[:, list(T)].T @ X[:, list(T)] + np.eye(len(T)))[1]
                                              - np.linalg.slogdet(X[:, list(T)].T @ X[:, list(T)] + np.eye(len(T)))[1] if T else 0.0))
            maxrel = max(maxrel, abs(G - nu * -math.log1p(-yy)) / max(1e-12, abs(G)),
                         abs(LR - nu * (-math.log1p(-yy) + math.log1p(-(1 - kap) * yy))) / max(1e-12, abs(LR)))
            cnt += 1
            if not (kap * G <= LR * (1 + 1e-9) + 1e-12 and LR <= kap * G / (1 - yy) * (1 + 1e-9) + 1e-12): viol += 1
out.append(f"(3) Lemma W2: {cnt} (S0, l) pairs in 6 BO correlated-block designs; sandwich violations = {viol}; "
           f"max rel. error of G = nu g(y) and LR = nu[g(y)-g((1-kappa)y)] = {maxrel:.2e}")

# ---- (4) Prop L(ii) on the last ORTH-like design (BO) : log(1+chi2(q_v||q_u)) = l(u)+l(w)-2l(v)
worst = 0.0
for _ in range(40):
    u, v = rng.uniform(-0.5, 1.5, 2); w = 2 * v - u
    lu, lv, lw = (loggam(a, subs, lbf, lr, p) for a in (u, v, w))
    lhs = logsumexp(2 * (lv - logsumexp(lv)) - (lu - logsumexp(lu)))  # log sum q_v^2/q_u, in log space
    S0 = (0, 3); rhs = ell(u, S0, subs, lbf, lr, p) + ell(w, S0, subs, lbf, lr, p) - 2 * ell(v, S0, subs, lbf, lr, p)
    worst = max(worst, abs(lhs - rhs))
out.append(f"(4) Prop L(ii): max |log(1+chi2) - [l(u)+l(w)-2l(v)]| over 40 random (u,v) = {worst:.2e}")
print("\n".join(out))
