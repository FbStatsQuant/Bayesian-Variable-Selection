"""W3-PSHARP numerics (c): the counterexample design D_n of Proposition C, exact posterior by full enumeration.

Design (STATEMENT section 4): x1, x3..x_{k+2} mutually orthogonal centred, ||.||^2 = n-1; u = sum_{j>=3} x_j;
x2 = c (x1 - eta u), c = (1 + eta^2 k)^{-1/2}, eta = n^{-2}; p = k + 2; T = {1,2}, T' = {3..k+2}.
Counterexample arm: mu = (b/sqrt k) u  (exactly representable by T, only with coefficients ~ b n^2/sqrt k).
Control arm:        mu = (b/2)(x1 + x2) (exactly representable by T with coefficients b/2: Lemma 1a' applies).
Proposition C uses k = ceil(12 log n) (asymptotic choice, n >= 200), far beyond enumeration; here k is 16..22 and the
cutoffs are computed EXACTLY from their definitions, so the check is: is the exact cutoff m^T_n(log n / 2) below k,
and where does the posterior put its mass.
  m'  := m^T_n(omega = log n/2) = min{m >= 2 : R^T_m <= n^{-2}},  R^T_m = sum_{j=m+1}^K q_j / w(2)     [Lemma 1a', t = 2]
  m'' := min{m >= 2 : A^T_m = R^T_m sqrt(D_T) sqrt(n) <= n^{-1/2}}                                 [Lemma 1a'']
  Theta'  := pi(|S| > m')  / (R^T_m' (n+1) sqrt n),   Theta'' := pi(|S| > m'') / A^T_m''
(the lemmas would make Theta', Theta'' tight, i.e. pi(|S| > m') = O_P(n^{-1/2}) R-normalised).
Exact enumeration uses the structure: models (A, B), A subset of {1,2}, B subset of T'; without x2 the columns are
orthogonal; with x2 one Schur complement, written in cancellation-free form (eps_B = eta^2 (k-|B|)/(1+eta^2 k)).
Sufficient statistics (exact in law; noise coordinates in an orthonormal basis): a_1 = u_1'(mu + eps), a_j, and
chi^2_{n-2-k} for the rest.  V1 validates the structured formulas against generic linear algebra (float64 at
eta = 0.05; mpmath 60 digits at eta = n^{-2}).
Run: py -3.13 -I c_counter.py > c_counter_out.txt
"""
import sys, os, math, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script directory
sys.dont_write_bytecode = True
import numpy as np
from core import B0, lchoose, logw


def subset_sums(vals):
    out = np.zeros(1)
    for v in vals:
        out = np.concatenate([out, out + v])
    return out


def group_tables(n, k, eta, z1, zT):
    """For the four groups A in {00, 10, 01, 11}: arrays over all B (bitmask order) of (size, logD, Q)."""
    c = 1 / math.sqrt(1 + eta * eta * k)
    cnt = subset_sums(np.ones(k))
    sz = subset_sums(zT)
    sz2 = subset_sums(zT ** 2)
    ztot = float(zT.sum())
    z2 = c * (z1 - eta * ztot)
    ln = math.log(n)
    yy = n - 1.0
    out = {}
    Q00 = yy - sz2 / n
    out["00"] = (cnt, cnt * ln, Q00)
    Q10 = Q00 - z1 * z1 / n
    out["10"] = (cnt + 1, (cnt + 1) * ln, Q10)
    # add x2 to the orthogonal set O = B
    g2 = c * c * (n - 1) ** 2 * eta * eta * cnt
    s = n * n - (n + 1) ** 2 * g2 / (n * n)
    den = n - g2 / n
    score = z2 + (n + 1) * (n - 1) * c * eta * sz / (n * n)
    out["01"] = (cnt + 1, cnt * ln + np.log(s / den), Q00 - n * score ** 2 / s)
    # add x2 to O = {1} + B (cancellation-free)
    epsB = eta * eta * (k - cnt) / (1 + eta * eta * k)
    s = 2 - n ** -2.0 + (n * n - 2 + n ** -2.0) * epsB
    den = (2 * n - 1) / n + (n - 1) ** 2 * epsB / n
    score = c * z1 / (n * n) - c * eta * ((ztot - sz) + sz / (n * n))
    out["11"] = (cnt + 2, (cnt + 1) * ln + np.log(s / den), Q10 - n * score ** 2 / s)
    return out


def posterior(n, k, eta, z1, zT):
    p = k + 2
    K = min(p, n // 2)
    nu = 0.01 + n / 2
    lw = np.array([logw(p, j) if j <= K else -np.inf for j in range(p + 1)])
    tabs = group_tables(n, k, eta, z1, zT)
    ls, sizes = [], []
    for key in ("00", "10", "01", "11"):
        size, logD, Q = tabs[key]
        assert Q.min() > -1e-9
        ls.append(lw[size.astype(int)] - 0.5 * logD - nu * np.log(2 * B0 + np.maximum(Q, 0)))
        sizes.append(size.astype(int))
    ls, sizes = np.concatenate(ls), np.concatenate(sizes)
    mx = ls.max()
    w = np.exp(ls - mx)
    by_size = np.bincount(sizes, weights=w, minlength=p + 1)
    by_size /= by_size.sum()
    full = (1 << k) - 1
    piTp = w[full] / w.sum()                                  # pi(T'): group 00, B = all
    return by_size, piTp, tabs


def cutoffs(n, k, logD_T):
    p = k + 2
    K = min(p, n // 2)
    q = np.array([math.exp(math.log(0.5) + lchoose(p, j) - lchoose(2 * p - 1, j)) if j <= K else 0.0 for j in range(p + 1)])
    tail = np.concatenate([np.cumsum(q[::-1])[::-1][1:], [0.0]])       # tail[m] = sum_{j > m} q_j
    R = tail / math.exp(logw(p, 2))
    m1 = next(m for m in range(2, p + 1) if R[m] <= n ** -2.0)
    A = R * math.exp(0.5 * logD_T) * math.sqrt(n)
    m2 = next(m for m in range(2, p + 1) if A[m] <= n ** -0.5)
    return m1, m2, R, A


def draw(n, k, eta, b, arm, rng):
    c = 1 / math.sqrt(1 + eta * eta * k)
    g1, gT = rng.standard_normal(), rng.standard_normal(k)
    rest = rng.chisquare(n - 2 - k)
    if arm == "counter":
        a1, aT = g1, math.sqrt(n - 1) * b / math.sqrt(k) + gT
    else:                                                    # control: mu = (b/2)(x1 + x2)
        a1, aT = math.sqrt(n - 1) * (b / 2) * (1 + c) + g1, -math.sqrt(n - 1) * (b / 2) * c * eta + gT
    sy = math.sqrt((a1 * a1 + (aT ** 2).sum() + rest) / (n - 1))
    return math.sqrt(n - 1) * a1 / sy, math.sqrt(n - 1) * aT / sy


def V1(rng):
    print("V1: structured formulas vs generic linear algebra")
    # (i) float64, eta = 0.05, explicit matrices, all 2^(k+2) models
    worst = 0.0
    for (n, k) in ((14, 4), (30, 5)):
        eta = 0.05
        M = rng.standard_normal((n, k + 1)); M -= M.mean(0); Qm, _ = np.linalg.qr(M); Qm -= Qm.mean(0); Qm, _ = np.linalg.qr(Qm)
        Xo = math.sqrt(n - 1) * Qm
        x1, XT = Xo[:, 0], Xo[:, 1:]
        c = 1 / math.sqrt(1 + eta * eta * k)
        x2 = c * (x1 - eta * XT.sum(1))
        X = np.column_stack([x1, x2, XT])
        yr = XT.sum(1) * 0.8 + rng.standard_normal(n); yc = yr - yr.mean(); y = yc / math.sqrt((yc ** 2).sum() / (n - 1))
        tabs = group_tables(n, k, eta, float(x1 @ y), XT.T @ y)
        for key, cols in (("00", []), ("10", [0]), ("01", [1]), ("11", [0, 1])):
            size, logD, Q = tabs[key]
            for mask in range(1 << k):
                S = cols + [2 + i for i in range(k) if mask >> i & 1]
                if S:
                    XS = X[:, S]; G = XS.T @ XS; z = XS.T @ y; H = (n + 1) * G + np.eye(len(S))
                    lD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(len(S)))[1]
                    Qg = float(y @ y - n * z @ np.linalg.solve(H, z))
                else:
                    lD, Qg = 0.0, float(y @ y)
                worst = max(worst, abs(lD - logD[mask]), abs(Qg - Q[mask]) / (n - 1))
                assert int(size[mask]) == len(S)
    print(f"  (i) float64, eta=0.05: max |logD diff| and |Q diff|/(n-1) = {worst:.1e}: {'PASS' if worst < 1e-9 else 'FAIL'}")
    # (ii) mpmath 60 digits, eta = n^-2
    import mpmath as mp
    mp.mp.dps = 60
    worst = mp.mpf(0)
    n, k = 20, 4
    eta = mp.mpf(n) ** -2
    M = rng.standard_normal((n, k + 1)); M -= M.mean(0)
    # Gram-Schmidt in mp
    cols = []
    for j in range(k + 1):
        v = mp.matrix([mp.mpf(float(t)) for t in M[:, j]])
        mean = sum(v) / n
        v = mp.matrix([t - mean for t in v])
        for u in cols:
            v = v - (u.T * v)[0] * u
        cols.append(v / mp.sqrt((v.T * v)[0]))
    sc = mp.sqrt(n - 1)
    x1 = sc * cols[0]; XT = [sc * u for u in cols[1:]]
    c = 1 / mp.sqrt(1 + eta * eta * k)
    usum = XT[0]
    for v in XT[1:]: usum = usum + v
    x2 = c * (x1 - eta * usum)
    allc = [x1, x2] + XT
    yr = mp.matrix([mp.mpf(float(t)) for t in rng.standard_normal(n)]) + mp.mpf("0.9") * usum
    mean = sum(yr) / n; yc = mp.matrix([t - mean for t in yr]); y = yc / mp.sqrt((yc.T * yc)[0] / (n - 1))
    z1 = float((x1.T * y)[0]); zT = np.array([float((v.T * y)[0]) for v in XT])
    tabs = group_tables(n, k, float(eta), z1, zT)
    for key, cc in (("00", []), ("10", [0]), ("01", [1]), ("11", [0, 1])):
        size, logD, Q = tabs[key]
        for mask in range(1 << k):
            S = cc + [2 + i for i in range(k) if mask >> i & 1]
            if S:
                m = len(S)
                G = mp.matrix(m, m)
                for a in range(m):
                    for b_ in range(m):
                        G[a, b_] = (allc[S[a]].T * allc[S[b_]])[0]
                z = mp.matrix([(allc[i].T * y)[0] for i in S])
                H = (n + 1) * G + mp.eye(m)
                lD = mp.log(mp.det(H)) - mp.log(mp.det(G + mp.eye(m)))
                Qg = (y.T * y)[0] - n * (z.T * mp.lu_solve(H, z))[0]
            else:
                lD, Qg = mp.mpf(0), (y.T * y)[0]
            worst = max(worst, abs(lD - mp.mpf(float(logD[mask]))), abs(Qg - mp.mpf(float(Q[mask]))) / (n - 1))
    print(f"  (ii) mpmath 60 digits, eta=n^-2 (n={n}, k={k}): max |logD diff| and |Q diff|/(n-1) = {float(worst):.1e}: {'PASS' if worst < 1e-9 else 'FAIL'}")


def E1(rng, reps=20):
    print("E1: columns: arm n k b | exact cutoffs m' (1a'), m'' (1a'') | median [min, max] of pi(|S| > m') | median Theta', Theta''"
          " | median posterior mean size | median pi(T') | n^(-1/2)")
    for (n, k, b) in ((50, 16, 3.0), (100, 18, 3.0), (200, 20, 3.0), (400, 22, 3.0), (800, 22, 3.0), (1600, 22, 3.0), (400, 22, 1.0), (1600, 22, 0.5)):
        eta = n ** -2.0
        for arm in ("counter", "control"):
            res = []
            for _ in range(reps):
                z1, zT = draw(n, k, eta, b, arm, rng)
                by_size, piTp, tabs = posterior(n, k, eta, z1, zT)
                logD_T = float(tabs["11"][1][0])
                m1, m2, R, A = cutoffs(n, k, logD_T)
                tail1, tail2 = by_size[m1 + 1:].sum(), by_size[m2 + 1:].sum()
                th1 = tail1 / (R[m1] * (n + 1) * math.sqrt(n)) if R[m1] > 0 else 0.0
                th2 = tail2 / A[m2] if A[m2] > 0 else 0.0
                res.append((tail1, th1, th2, float((np.arange(k + 3) * by_size).sum()), piTp))
            res = np.array(res)
            med = np.median(res, 0)
            print(f"  {arm:8s} n={n:5d} k={k} b={b} | m'={m1} m''={m2} (k={k}, p={k+2}) | {med[0]:.3e} [{res[:,0].min():.3e}, {res[:,0].max():.3e}]"
                  f" | {med[1]:.3e} {med[2]:.3e} | {med[3]:.2f} | {med[4]:.3f} | {n**-0.5:.3f}", flush=True)


def E2():
    print("E2: the cutoff bound of Proposition C item 2 at k = ceil(12 log n), p = k+2, m_n = floor(k/2):"
          " exact R^T_{m_n} n^2 (must be <= 1 for n >= 200) and exact m' vs m_n")
    for n in (200, 500, 10 ** 3, 10 ** 4, 10 ** 6):
        k = math.ceil(12 * math.log(n)); p = k + 2; K = min(p, n // 2)
        lq = [math.log(0.5) + lchoose(p, j) - lchoose(2 * p - 1, j) for j in range(p + 1)]
        mn = k // 2
        tail = sum(math.exp(lq[j]) for j in range(mn + 1, K + 1))
        R = tail / math.exp(logw(p, 2))
        m1 = next(m for m in range(2, p + 1) if sum(math.exp(lq[j]) for j in range(m + 1, K + 1)) / math.exp(logw(p, 2)) <= n ** -2.0)
        print(f"  n={n:.0e}: k={k} p={p} K={K} m_n={mn}: R n^2 = {R * n * n:.3e}; exact m' = {m1}")


if __name__ == "__main__":
    t0 = time.time()
    rng = np.random.default_rng(20261114)
    V1(rng); E2(); E1(rng)
    print(f"  [done, {time.time()-t0:.0f}s]")
