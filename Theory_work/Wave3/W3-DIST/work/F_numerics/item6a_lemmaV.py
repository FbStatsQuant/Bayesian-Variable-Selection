"""Item 6a: Lemma V re-check on singular / duplicated / near-singular designs (extends work/prior_probe/probe_checks.py C3).
Checks, for S = S0 u J, eta>0, c=1+eta, D' = M_S^{(1/c)} - M_S0^{(c)}   (M^{(c)} = X (G + c(G+I)/n)^{-1} X'),  rho' = theta*'(G_S0+I)theta*/n:
  (a) Q_S0(y) - Q_S(y) <= e'D'e + (1+2/eta) rho'   for y = X_S0 theta* + e  (sigma*=1)
  (b) 0 <= D' < I (spectrum) and  det(I-D')^{-1/2} (D_S0/D_S)^{1/2} <= (1+eta)^{s0+|J|/2}   [= the expectation in Lemma V(b): E exp(e'D'e/2) = det(I-D')^{-1/2}]
  (c) e'D'e <= e'P_S e = ||P_S0 e||^2 + chi2_{dJ}   (chi2_{dJ}:= e'(P_S-P_S0)e, rank dJ)
  (d) Monte Carlo of E[(D_S0/D_S)^{1/2} exp(e'D'e/2)] against the determinant formula and against the bound.
DRAFT (by this seat, unchecked)"""
import sys, math
from fcommon import *
rng = np.random.default_rng(20261116)

def std_design(Z):
    Z = Z - Z.mean(0)
    return Z * np.sqrt((Z.shape[0] - 1) / (Z ** 2).sum(0))
def ridge_M(X, c, n):
    if X.shape[1] == 0: return np.zeros((X.shape[0], X.shape[0]))
    G = X.T @ X
    return X @ np.linalg.solve(G + c * (G + np.eye(G.shape[0])) / n, X.T)
def logD(X, n):
    if X.shape[1] == 0: return 0.0
    G = X.T @ X; k = G.shape[0]
    return np.linalg.slogdet((n + 1) * G + np.eye(k))[1] - np.linalg.slogdet(G + np.eye(k))[1]
def Qf(X, y, n): return float(y @ y - y @ ridge_M(X, 1.0, n) @ y)
def proj(X):
    if X.shape[1] == 0: return np.zeros((X.shape[0],) * 2)
    U, s, _ = np.linalg.svd(X, full_matrices=False)
    r = int((s > 1e-9 * s[0]).sum()); return U[:, :r] @ U[:, :r].T

KINDS = ["plain", "weakS0", "nearJ", "dupJ", "dupS0", "allJdup", "J_mutual_dup", "near1e-8", "nearJ1e-6", "s0zero", "J_in_span_S0"]
def make(n, s0, j, kind):
    Z = rng.standard_normal((n, s0 + j))
    if kind == "weakS0" and s0 >= 2: Z[:, 1] = Z[:, 0] + 1e-3 * rng.standard_normal(n) / math.sqrt(n)
    if kind == "nearJ":
        for t in range(j): Z[:, s0 + t] = Z[:, t % max(s0, 1)] + 0.05 / math.sqrt(n) * rng.standard_normal(n)
    if kind == "dupJ": Z[:, s0] = Z[:, 0]
    if kind == "dupS0" and s0 >= 2: Z[:, 1] = Z[:, 0]
    if kind == "allJdup":
        for t in range(j): Z[:, s0 + t] = Z[:, t % max(s0, 1)]
    if kind == "J_mutual_dup":
        for t in range(1, j): Z[:, s0 + t] = Z[:, s0]
    if kind == "near1e-8" and s0 >= 2: Z[:, 1] = Z[:, 0] + 1e-8 * rng.standard_normal(n)
    if kind == "nearJ1e-6":
        for t in range(j): Z[:, s0 + t] = Z[:, t % max(s0, 1)] + 1e-6 * rng.standard_normal(n)
    if kind == "J_in_span_S0" and s0 >= 2:
        for t in range(j): Z[:, s0 + t] = Z[:, 0] + Z[:, 1]
    return std_design(Z)

if __name__ == "__main__":
    NTR = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    wa = wb = wc = -np.inf; mine = np.inf; maxeig = -np.inf; worst = {}
    cnt = 0; viol = 0
    for trial in range(NTR):
        n = int(rng.choice([10, 14, 30, 80, 200, 600]))
        s0 = int(rng.choice([0, 1, 2, 3])); j = int(rng.choice([1, 2, 4, 5]))
        if s0 + j > n // 2: j = max(1, n // 2 - s0)
        kind = str(rng.choice(KINDS)); eta = float(rng.choice([0.01, 0.1, 0.5, 1.0, 3.0, 10.0, 100.0]))
        X = make(n, s0, j, kind); X0 = X[:, :s0]
        scale = float(rng.choice([1.0, 5.0, 50.0]))
        th = rng.standard_normal(s0) * scale
        if kind in ("weakS0", "near1e-8", "dupS0") and s0 >= 2: th[0], th[1] = 50.0 * scale, -50.0 * scale
        mu = X0 @ th if s0 else np.zeros(n)
        rho = float(th @ (X0.T @ X0 + np.eye(s0)) @ th / n) if s0 else 0.0
        c = 1 + eta
        Dp = ridge_M(X, 1 / c, n) - ridge_M(X0, c, n)
        ev = np.linalg.eigvalsh((Dp + Dp.T) / 2)
        mine = min(mine, ev[0]); maxeig = max(maxeig, ev[-1])
        PS = proj(X)
        for _ in range(4):
            e = rng.standard_normal(n) * float(rng.choice([0.5, 1.0, 3.0]))   # sigma* != 1 only through scale of e (a stress, not in the lemma)
            sg = 1.0
            e = rng.standard_normal(n)  # sigma*=1 as in the lemma
            y = mu + e
            lhs = Qf(X0, y, n) - Qf(X, y, n)
            rhs = float(e @ Dp @ e) + (1 + 2 / eta) * rho
            m_a = lhs - rhs
            m_c = float(e @ Dp @ e) - float(e @ PS @ e)
            if m_a > wa: wa = m_a; worst['a'] = (kind, n, s0, j, eta)
            wc = max(wc, m_c)
            if m_a > 1e-8 * max(1.0, abs(lhs)): viol += 1
        ld = np.linalg.slogdet(np.eye(n) - Dp)
        lhs_b = -0.5 * ld[1] + 0.5 * (logD(X0, n) - logD(X, n)); rhs_b = (s0 + (X.shape[1] - s0) / 2.0) * math.log(c)
        m_b = lhs_b - rhs_b
        if ld[0] <= 0: print("  det(I-D') <= 0 !", kind, n, s0, j, eta)
        if m_b > wb: wb = m_b; worst['b'] = (kind, n, s0, j, eta)
        cnt += 1
    print(f"Lemma V checks on {cnt} designs (kinds: {', '.join(KINDS)}); eta in 0.01..100; n in 10..600; s0 in 0..3, |J| in 1..5")
    print(f"(a) max over {cnt*4} draws of [Q_S0 - Q_S] - [e'D'e + (1+2/eta) rho'] = {wa:.3e}  (claim <= 0)  worst design {worst.get('a')};  draws with violation > 1e-8 rel: {viol}")
    print(f"(b) spectrum of D': min eig = {mine:.3e} (claim >= 0), max eig = {maxeig:.6f} (claim < 1);  max over designs of log[LHS_b] - log[(1+eta)^(s0+|J|/2)] = {wb:.3e} (claim <= 0)  worst design {worst.get('b')}")
    print(f"(c) max of e'D'e - e'P_S e = {wc:.3e}  (claim <= 0)")
    # (d) Monte Carlo of the expectation in V(b) vs determinant formula
    print("(d) Monte Carlo (2e6 draws) of E[exp(e'D'e/2)] vs det(I-D')^{-1/2}, and of the full left side vs (1+eta)^(s0+|J|/2):")
    for (n, s0, j, kind, eta) in [(30, 2, 2, "plain", 1.0), (30, 2, 2, "dupJ", 0.5), (30, 2, 3, "allJdup", 1.0), (60, 1, 2, "nearJ", 2.0), (30, 3, 2, "near1e-8", 1.0)]:
        X = make(n, s0, j, kind); X0 = X[:, :s0]; c = 1 + eta
        Dp = ridge_M(X, 1 / c, n) - ridge_M(X0, c, n); Dp = (Dp + Dp.T) / 2
        w_, V = np.linalg.eigh(Dp); w_ = np.clip(w_, 0, None)
        tot = 0.0; N = 0
        for _ in range(20):
            g = rng.standard_normal((100000, n)) @ V
            q = (g ** 2) @ w_
            tot += np.exp(q / 2).sum(); N += 100000
        mc = tot / N
        form = math.exp(-0.5 * np.linalg.slogdet(np.eye(n) - Dp)[1])
        fac = math.exp(0.5 * (logD(X0, n) - logD(X, n)))
        print(f"   n={n} s0={s0} |J|={j} {kind:9s} eta={eta} (max eig D'={w_.max():.3f}; Var of exp(q/2) finite iff < 0.5): MC E exp = {mc:.4f}, det formula = {form:.4f}; (D0/DS)^(1/2)*det formula = {fac*form:.4f} <= (1+eta)^(s0+|J|/2) = {c**(s0+j/2):.4f}: {fac*form <= c**(s0+j/2)}")
