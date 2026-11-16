#!/usr/bin/env python3
"""Stream C numerical sanity checks (W3-DIST): Lemma V, Lemma S (deterministic core), X1/X2 facts.
Falsification checks only, not proofs. Run: python3 c_checks.py > c_checks_out.txt  (local, < 2 min).
Notation as in API_CARDS.md "Common definitions" and the files V.md, S.md, X12.md of this folder."""
import itertools, math
import numpy as np
from scipy.special import gammaln

rng = np.random.default_rng(20261115)
B0 = 0.01

def contrast_basis(n):
    # U in R^{n x (n-1)}, U^T U = I, U U^T = I - 11^T/n
    Cm = np.eye(n) - np.ones((n, n)) / n
    w, V = np.linalg.eigh(Cm)
    return V[:, w > 0.5]

def standardise(Xr):
    n = Xr.shape[0]
    Xc = Xr - Xr.mean(0)
    s = np.sqrt((Xc ** 2).sum(0) / (n - 1))
    return Xc / s

def quantities(Xc, S, n):
    """Xc: contrast design (N x p). Returns G, A, D, M (smoother), P (projection) for model S."""
    N = Xc.shape[0]
    if len(S) == 0:
        return None, None, 1.0, np.zeros((N, N)), np.zeros((N, N))
    XS = Xc[:, S]
    G = XS.T @ XS
    A = G + np.eye(len(S))
    H = (n + 1) * G + np.eye(len(S))
    D = np.linalg.det(H) / np.linalg.det(A)
    M = n * XS @ np.linalg.solve(H, XS.T)
    P = proj(XS)
    return G, A, D, M, P

def proj(XS):
    U_, s, _ = np.linalg.svd(XS, full_matrices=False)
    r = (s > 1e-9 * max(1.0, s.max())).sum()
    Ur = U_[:, :r]
    return Ur @ Ur.T

def Mc(Xc, S, n, c):
    N = Xc.shape[0]
    if len(S) == 0:
        return np.zeros((N, N))
    XS = Xc[:, S]
    G = XS.T @ XS
    A = G + np.eye(len(S))
    return XS @ np.linalg.solve(G + c * A / n, XS.T)

def Dc(Xc, S, n, c):
    if len(S) == 0:
        return 1.0
    G = Xc[:, S].T @ Xc[:, S]
    lam = np.clip(np.linalg.eigvalsh(G), 0, None)
    return float(np.prod((1 + lam * (1 + n / c)) / (1 + lam)))

# ---------------------------------------------------------------- Lemma V
def design_family(fam, n, p):
    Z = rng.standard_normal((n, p))
    if fam == "dup":            # duplicated columns (0,1) in S0 and (2,3) with 3 in J
        Z[:, 1] = Z[:, 0]; Z[:, 3] = Z[:, 2]
    elif fam == "collinear":    # 1e-3-collinear pair in S0
        Z[:, 1] = Z[:, 0] + 1e-3 * rng.standard_normal(n)
    elif fam == "nearspan":     # J column nearly in span of S0
        Z[:, 4] = Z[:, 0] - Z[:, 1] + 1e-4 * rng.standard_normal(n)
    return standardise(Z)

def check_V(n_rep=300):
    out = []
    worst = dict(a=-np.inf, b=-np.inf, c=np.inf, psd=np.inf, norm=-np.inf, R0lo=np.inf, R0hi=np.inf, D1=0.0)
    for rep in range(n_rep):
        fam = ["iid", "dup", "collinear", "nearspan", "s0zero", "bigS"][rep % 6]
        if fam == "bigS":
            n, p = 24, 14
        else:
            n, p = int(rng.integers(12, 40)), 10
        X = design_family(fam if fam in ("dup", "collinear", "nearspan") else "iid", n, p)
        U = contrast_basis(n)
        Xc = U.T @ X
        N = n - 1
        s0 = 0 if fam == "s0zero" else int(rng.integers(1, 4))
        S0 = list(range(s0))
        if fam == "bigS":
            J = list(range(s0, n // 2))             # |S| = K = n/2
        else:
            jsz = int(rng.integers(0, p - s0 + 1))
            J = sorted(rng.choice(np.arange(s0, p), size=jsz, replace=False).tolist())
        S = S0 + J
        if len(S) == 0:
            J = [s0]; S = S0 + J                    # skip the trivial S = empty set (equality case)
        th = rng.standard_normal(s0) * (50 if fam == "collinear" else 2)
        if fam == "collinear" and s0 >= 2:
            th[1] = -th[0]
        mu_c = Xc[:, S0] @ th if s0 else np.zeros(N)
        rho = (mu_c @ mu_c + th @ th) / n if s0 else 0.0
        eta = float(rng.choice([0.05, 0.3, 1.0, 3.0]))
        c = 1 + eta
        Dp = Mc(Xc, S, n, 1 / c) - Mc(Xc, S0, n, c)
        ev = np.linalg.eigvalsh((Dp + Dp.T) / 2)
        worst["psd"] = min(worst["psd"], ev.min())
        worst["norm"] = max(worst["norm"], ev.max() - c * n / (c * n + 1))
        # (a) on several noise draws, sigma = 1.7
        sig = 1.7
        _, _, D0, M0, P0 = quantities(Xc, S0, n)
        _, _, DS, MS, PS = quantities(Xc, S, n)
        for _ in range(20):
            e = sig * rng.standard_normal(N)
            y = mu_c + e
            Q0 = y @ (np.eye(N) - M0) @ y
            QS = y @ (np.eye(N) - MS) @ y
            worst["a"] = max(worst["a"], (Q0 - QS) - (e @ Dp @ e + (1 + 2 / eta) * rho))
        # (b) exact: (D0/DS)^{1/2} det(I - D')^{-1/2} <= c^{s0+|J|/2}
        sign, logdet = np.linalg.slogdet(np.eye(N) - Dp)
        lhs = 0.5 * (math.log(D0) - math.log(DS)) - 0.5 * logdet
        rhs = (s0 + len(J) / 2) * math.log(c)
        worst["b"] = max(worst["b"], lhs - rhs)
        # D^{(1)} = D (consistency of the Woodbury/determinant formula)
        worst["D1"] = max(worst["D1"], abs(math.log(Dc(Xc, S, n, 1.0)) - math.log(DS)))
        # (c) (P_S - P_S0) + R0 - D' >= 0, 0 <= R0 <= P_S0
        R0 = P0 - Mc(Xc, S0, n, c)
        worst["c"] = min(worst["c"], np.linalg.eigvalsh(PS - P0 + R0 - Dp).min())
        worst["R0lo"] = min(worst["R0lo"], np.linalg.eigvalsh(R0).min())
        worst["R0hi"] = min(worst["R0hi"], np.linalg.eigvalsh(P0 - R0).min())
    out.append("V: max over draws of (a) LHS-RHS = %.3e (must be <= 0)" % worst["a"])
    out.append("V: max over designs of (b) log LHS - log RHS = %.3e (must be <= 0)" % worst["b"])
    out.append("V: min eig D' = %.3e (>= 0 up to rounding); max (lam_max D' - cn/(cn+1)) = %.3e (<= 0)" % (worst["psd"], worst["norm"]))
    out.append("V: min eig of (P_S-P_S0+R0-D') = %.3e; min eig R0 = %.3e; min eig (P_S0-R0) = %.3e (all >= 0 up to rounding)" % (worst["c"], worst["R0lo"], worst["R0hi"]))
    out.append("V: max |log D^(1) - log D| = %.3e" % worst["D1"])
    return out

def check_V_mc():
    """Monte Carlo check of the Gaussian identity E exp(e'D'e/2s^2) = det(I-D')^{-1/2} in a case with ||D'|| < 1/2."""
    n, p = 30, 4
    X = standardise(rng.standard_normal((n, p)))
    X[:, 3] = standardise((X[:, 0] + 0.02 * rng.standard_normal(n))[:, None])[:, 0]  # weak new direction
    U = contrast_basis(n); Xc = U.T @ X; N = n - 1
    S0, S = [0], [0, 3]
    c = 1.3
    Dp = Mc(Xc, S, n, 1 / c) - Mc(Xc, S0, n, c)
    lmax = np.linalg.eigvalsh(Dp).max()
    sig = 1.0
    E = sig * rng.standard_normal((400000, N))
    vals = np.exp(np.einsum("ij,jk,ik->i", E, Dp, E) / (2 * sig ** 2))
    mc = vals.mean(); se = vals.std() / math.sqrt(len(vals))
    exact = np.linalg.det(np.eye(N) - Dp) ** -0.5
    return ["V-MC: lambda_max(D') = %.3f; MC mean %.5f +- %.5f vs det formula %.5f" % (lmax, mc, se, exact)]

# ---------------------------------------------------------------- Lemma S (deterministic core)
def log_mc_ratio(Q, D, E1, N, n, b, sig2):
    """log m^c_b(T)/f0(y_c) by quadrature; f0 = (2 pi sig2)^{-N/2} e^{-E1/2}."""
    v = np.exp(np.linspace(math.log(sig2) - 4, math.log(sig2) + 4, 40001))
    a = 0.51
    logIG = a * math.log(b) - gammaln(a) - (a + 1) * np.log(v) - b / v
    integrand = -(N / 2) * np.log(v / sig2) + E1 / 2 - Q / (2 * v) + logIG + np.log(v)  # d(log v)
    mx = integrand.max()
    dlv = np.log(v[1]) - np.log(v[0])
    return -0.5 * math.log(D) + mx + math.log(np.exp(integrand - mx).sum() * dlv)

def check_S(n_rep=60):
    out = []
    worst_den = -np.inf; worst_asm = -np.inf; nB = 0
    for rep in range(n_rep):
        n = int(rng.choice([20, 40, 80])); p = 8
        sig2 = float(rng.choice([0.5, 1.0, 2.0])); M = 3.0
        X = standardise(rng.standard_normal((n, p)))
        if rep % 3 == 1:
            X[:, 5] = X[:, 4]
        U = contrast_basis(n); Xc = U.T @ X; N = n - 1
        # truth G': mu not in col X (add an orthogonal component), ||mu||^2 <= nM
        s0 = 2
        th = np.array([1.0, -0.7])
        mu = X[:, :s0] @ th
        g = U @ rng.standard_normal(N); g -= X @ np.linalg.lstsq(X, g, rcond=None)[0]
        mu = mu + 0.8 * g / np.linalg.norm(g)
        mu *= min(1.0, math.sqrt(n * M) / np.linalg.norm(mu))
        T = [0, 1]; vt = th
        r = mu - X[:, T] @ vt
        Bv = r @ r + ((X[:, T] @ vt) @ (X[:, T] @ vt) + vt @ vt) / n
        eps = math.sqrt(sig2) * rng.standard_normal(n)
        yr = 0.3 + mu + eps
        yc = U.T @ yr; ec = U.T @ eps
        E1 = ec @ ec / sig2
        bm = B0 * sig2 / 2; bp = B0 * (2 * (sig2 + M) + 1)
        _, _, DT, MT, _ = quantities(Xc, T, n)
        QT = yc @ (np.eye(N) - MT) @ yc
        rho2 = Bv + 2 * abs(eps @ r)
        Lam = abs(E1 - N) / (2 * math.sqrt(n)) + E1 / (2 * n) + rho2 / (2 * sig2)
        vv = np.linspace(sig2, 2 * sig2, 2001)
        cIG = np.exp(0.51 * math.log(bp) - gammaln(0.51) - 1.51 * np.log(vv) - bp / vv).min()
        lhs = log_mc_ratio(QT, DT, E1, N, n, bp, sig2)
        rhs = -0.5 * math.log(DT) + math.log(cIG * sig2) - 0.5 * math.log(n) - Lam
        worst_den = max(worst_den, rhs - lhs)
        # assembly on B_n: pi(E_m) <= R_m sqrt(D_T) sqrt(n) c# e^Lam Theta1, by exact enumeration
        sy2 = yc @ yc / N
        if not (bm <= B0 * sy2 <= bp):
            continue
        nB += 1
        K = min(p, n // 2)
        w = lambda k: 0.5 / math.comb(2 * p - 1, k)
        models = [list(S) for k in range(K + 1) for S in itertools.combinations(range(p), k)]
        b = B0 * sy2; nu = 0.01 + n / 2
        logpost = []; logIb = []
        for S in models:
            _, _, DS, MS, _ = quantities(Xc, S, n)
            QS = yc @ (np.eye(N) - MS) @ yc
            logpost.append(math.log(w(len(S))) - 0.5 * math.log(DS) - nu * math.log(2 * b + QS))
            # log of varpi(S) m^c_{b-}(S)/f0 up to the common W_K (cancels in Theta1 because v_m uses varpi too)
            logm = (-(N / 2) * math.log(2 * math.pi) + 0.51 * math.log(bm) + gammaln(nu) - gammaln(0.51)
                    - 0.5 * math.log(DS) - nu * math.log(bm + QS / 2))
            logf0 = -(N / 2) * math.log(2 * math.pi * sig2) - E1 / 2
            logIb.append(math.log(w(len(S))) + logm - logf0)
        logpost = np.array(logpost); lp = np.exp(logpost - logpost.max()); lp /= lp.sum()
        logIb = np.array(logIb)
        sizes = np.array([len(S) for S in models])
        csharp = ((bp / bm) ** 0.51) ** 2 / (cIG * sig2)
        for m in range(len(T), K):
            sel = sizes > m
            piE = lp[sel].sum()
            Rm = sum(math.comb(p, k) * w(k) for k in range(m + 1, K + 1)) / w(len(T))
            vm_over = sum(math.comb(p, k) * w(k) for k in range(m + 1, K + 1))  # varpi(E_m) * W_K
            Theta1 = np.exp(logIb[sel]).sum() / vm_over
            bound = Rm * math.sqrt(DT) * math.sqrt(n) * csharp * math.exp(Lam) * Theta1
            worst_asm = max(worst_asm, math.log(piE) - math.log(bound))
    out.append("S: max over draws of log[lower bound] - log[m^c_{b+}(T)/f0] = %.3e (must be <= 0)" % worst_den)
    out.append("S: draws on B_n: %d; max over (draw, m) of log pi(|S|>m) - log[R sqrt(D_T n) c# e^Lam Theta1] = %.3e (<= 0)" % (nB, worst_asm))
    return out

def check_Bn_tail():
    """Exponential bound for P(B_n^c) vs Monte Carlo (sigma^2 = 1, M = 1, worst-case direction of mu)."""
    out = []
    for n in [20, 40, 80]:
        N = n - 1; sig2 = 1.0; M = 1.0
        reps = 200000
        E1 = rng.chisquare(N, reps)
        Zmu = rng.standard_normal(reps) * math.sqrt(sig2 * n * M)  # mu'eps with ||mu||^2 = nM
        sy2 = (n * M + 2 * Zmu + sig2 * E1) / N
        bad = ((sy2 < sig2 / 2) | (sy2 > 2 * (sig2 + M) + 1)).mean()
        bound = 2 * math.exp(-N / 100) + 2 * math.exp(-N * sig2 / (192 * M))
        out.append("B_n: n=%d MC P(B_n^c)=%.2e <= bound %.3f" % (n, bad, bound))
    return out

# ---------------------------------------------------------------- X1 / X2
def check_X(n_rep=40):
    out = []
    n, p = 120, 8
    sig2 = 1.0; sig = 1.0
    lp = math.log(math.e ** 2 * p)
    fails = 0; tot = 0; worst = dict(F2lo=-np.inf, F2hi=-np.inf, F3=-np.inf, F4=-np.inf, sy=-np.inf)
    subsets = [list(S) for k in range(p + 1) for S in itertools.combinations(range(p), k)]
    X = standardise(rng.standard_normal((n, p))); X[:, 7] = X[:, 6]
    U = contrast_basis(n); Xc = U.T @ X; N = n - 1
    S0 = [0, 1]; th = np.array([0.6, -0.4])
    mu_c = Xc[:, S0] @ th; M = (mu_c @ mu_c) / n
    pre = {}
    for S in subsets:
        _, _, DS, MS, PS = quantities(Xc, S, n)
        aS = (np.eye(N) - MS) @ mu_c
        pre[tuple(S)] = (MS, PS, aS, mu_c @ aS)
    t = 2.0
    for rep in range(4000):
        e = sig * rng.standard_normal(N)
        ok = (-2 * math.sqrt(2 * N * t) <= e @ e / sig2 - N <= 2 * math.sqrt(2 * N * t) + 4 * t)
        for S in subsets:
            MS, PS, aS, LS = pre[tuple(S)]
            k = len(S)
            if e @ PS @ e > sig2 * (3 * k * lp + 6 * t): ok = False; break
            if abs(e @ aS) > sig * math.sqrt(aS @ aS) * math.sqrt(2 * k * lp + 6 * t): ok = False; break
            J = [j for j in S if j not in S0]
            if set(S0) <= set(S):
                P0 = pre[tuple(S0)][1]
                if e @ (PS - P0) @ e > sig2 * (3 * len(J) * lp + 6 * t): ok = False; break
        tot += 1
        if not ok:
            fails += 1
            continue
        y = mu_c + e
        sy2 = y @ y / N
        worst["sy"] = max(worst["sy"], sy2 - 3 * (M + sig2))
        b = B0 * sy2; nu = 0.01 + n / 2
        Q0 = y @ (np.eye(N) - pre[tuple(S0)][0]) @ y; L0 = pre[tuple(S0)][3]
        for S in subsets:
            MS, PS, aS, LS = pre[tuple(S)]
            k = len(S); wS = 2 * k * lp + 6 * t
            QS = y @ (np.eye(N) - MS) @ y
            d = QS - e @ e
            worst["F2lo"] = max(worst["F2lo"], (LS / 2 - sig2 * (7 * k * lp + 18 * t)) - d)
            worst["F2hi"] = max(worst["F2hi"], d - (2 * LS + sig2 * (2 * k * lp + 6 * t)))
            worst["F3"] = max(worst["F3"], (LS / 2 - 2 * L0 - sig2 * (7 * k * lp + 2 * len(S0) * lp + 24 * t)) - (QS - Q0))
            DS_ = N - 2 * math.sqrt(2 * N * t) - 5 * k * lp - 12 * t
            if DS_ > 0:
                worst["F4"] = max(worst["F4"], nu / (2 * b + QS) - (n + 0.02) / (2 * sig2 * DS_))
    out.append("X1: n=%d p=%d t=%.1f: empirical P(E_t^c) = %d/%d = %.4f <= e^-t = %.4f" % (n, p, t, fails, tot, fails / tot, math.exp(-t)))
    out.append("X1(iv): max (s_y^2 - 3(M+s^2)) on E_t = %.3e (<= 0)" % worst["sy"])
    out.append("X facts on E_t: F2 lower viol %.3e, F2 upper viol %.3e, F3 viol %.3e, F4 viol %.3e (all <= 0)" % (worst["F2lo"], worst["F2hi"], worst["F3"], worst["F4"]))
    return out

def check_X2():
    """Conditional posterior: Monte Carlo of Pi(bad | S, y) for a good model, vs e^{-t}."""
    out = []
    n, p = 400, 6; N = n - 1; sig2 = 1.0
    X = standardise(rng.standard_normal((n, p))); U = contrast_basis(n); Xc = U.T @ X
    S0 = [0, 1]; th = np.array([0.5, 0.5]); mu_c = Xc[:, S0] @ th
    S = [0, 1, 2]; t = 3.0
    C2, C3p = 1.0, 1.0           # C'' and C''' (d log p <= C''' t with d = 3: log 6*3 = 5.4 > 3 -> use C''' = 2)
    C3p = 2.0; C3 = 4 * C3p
    M = (mu_c @ mu_c) / n
    KQ = 3 * C3 + 6 + 2 * math.sqrt(C2 * (2 * C3 + 6)) + C2
    Kb = 2 * math.sqrt(2) + 5.08 + 0.06 * M / sig2 + KQ
    Cv = 9 * Kb / 4 + 8; Cmu = 16 * C3 + 48 + 4 * C2
    worst = 0.0
    _, _, DS, MS, PS = quantities(Xc, S, n)
    H = (n + 1) * (Xc[:, S].T @ Xc[:, S]) + np.eye(len(S))
    for rep in range(200):
        e = rng.standard_normal(N); y = mu_c + e
        sy2 = y @ y / N; b = B0 * sy2; nu = 0.01 + n / 2
        QS = y @ (np.eye(N) - MS) @ y; beta = b + QS / 2
        v = beta / rng.gamma(nu, 1.0, 20000)
        thhat = n * np.linalg.solve(H, Xc[:, S].T @ y)
        L = np.linalg.cholesky(np.linalg.inv(H) * n)
        Zs = rng.standard_normal((20000, len(S))) @ L.T * np.sqrt(v)[:, None]
        fit = (Zs + thhat) @ Xc[:, S].T - mu_c
        err = (fit ** 2).sum(1)
        bad = (err > Cmu * sig2 * t) | (np.abs(v / sig2 - 1) > Cv * math.sqrt(t / n))
        bad2 = (err > 2 * sig2 * t) | (np.abs(v / sig2 - 1) > 2 * math.sqrt(t / n))   # much tighter constants
        worst = max(worst, bad.mean())
    out.append("X2: n=%d, t=%.0f, C_mu=%.0f, C_v=%.0f: max over 200 data sets of MC Pi(bad|S,y) = %.2e <= e^-t = %.3f" % (n, t, Cmu, Cv, worst, math.exp(-t)))
    out.append("X2: (the explicit constants are loose; with C=2 the MC frequency of the last data set is %.3f)" % bad2.mean())
    return out

if __name__ == "__main__":
    for f in (check_V, check_V_mc, check_S, check_Bn_tail, check_X, check_X2):
        for line in f():
            print(line, flush=True)
