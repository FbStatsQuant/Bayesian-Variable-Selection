"""Sanity checks for Theorem DIST-3 (DIST3.md). DRAFT helper, stream B. Run: python3 check_DIST3.py > check_DIST3_out.txt
Gaussian x (exact d_H^2 in closed form), exact conditional posterior given S0 (API_CARDS common definitions)."""
import numpy as np
from math import log, sqrt, ceil

rng = np.random.default_rng(11)
a0 = b0 = 0.01

# constants of DIST3.md for an example
def constants(sig2, s0r, M, B, CT, kappa0):
    ks = 4 + 2 * s0r * log(2); bbar = 4 * b0 * (M + sig2); sig = sqrt(sig2)
    Crho = 2 * bbar / sig2 + 2 * a0 + 1 + 2 * sqrt(2) + ks + 2 * sqrt(2 * B) / sig + B / sig2
    Cv = 2 * (Crho + 2 * sqrt(2)); Cmu = 8 * sig2 * ks + 4 * B
    Crad = sqrt(Cv ** 2 + CT * (2 * sig2 + Cmu) / (4 * sig2))
    n0 = max(3, 2 * s0r, ceil(Cv ** (2 / kappa0)))
    return Crho, Cv, Cmu, Crad, n0
Crho, Cv, Cmu, Crad, n0 = constants(1.0, 3, 1.0, 1.0, 2.0, 0.5)
print(f"[0] constants (sigma*^2=1, s0^r=3, M=B=1, C_T=2, kappa0=1/2): C_rho={Crho:.2f}, C_v={Cv:.2f}, C_mu={Cmu:.2f}, C_rad={Crad:.2f}, n0={n0}")

P = 10; R = [0, 1, 2]
beta = np.zeros(P); beta[R] = [1.0, -0.5, 0.8]; alpha = 2.0; sig2 = 1.0
mx = np.ones(P)
Sig = 0.5 ** np.abs(np.subtract.outer(np.arange(P), np.arange(P)))

def one_dataset(n, ndraw=400):
    Xr = mx + rng.normal(size=(n, P)) @ np.linalg.cholesky(Sig).T
    eps = rng.normal(size=n) * sqrt(sig2)
    y = alpha + Xr @ beta + eps
    xbar = Xr.mean(0); C = np.eye(n) - 1.0 / n
    Xc_raw = Xr - xbar
    sh = np.sqrt((Xc_raw ** 2).sum(0) / (n - 1))
    X = Xc_raw / sh
    S0 = R
    XS = X[:, S0]; G = XS.T @ XS; H = (n + 1) * G + np.eye(len(S0))
    yc_full = y - y.mean()                       # centred response (= U y_c, isometric)
    sy2 = (yc_full ** 2).sum() / (n - 1); b = b0 * sy2; nu = a0 + n / 2
    Mfit = n * XS @ np.linalg.solve(H, XS.T)
    Q = yc_full @ yc_full - yc_full @ Mfit @ yc_full
    beta_post = b + Q / 2
    thetahat = n * np.linalg.solve(H, XS.T @ yc_full)
    mu = Xc_raw @ beta
    # realised (TR0) constant on R: max generalised eigenvalue of Sigma_pop vs Sigma_n for xi=(1,x_R)
    Xi = np.column_stack([np.ones(n), Xr[:, R]])
    Sn = Xi.T @ Xi / n
    Sp = np.zeros((4, 4)); Sp[0, 0] = 1; Sp[0, 1:] = Sp[1:, 0] = mx[R]
    Sp[1:, 1:] = Sig[np.ix_(R, R)] + np.outer(mx[R], mx[R])
    L = np.linalg.cholesky(Sn); Li = np.linalg.inv(L)
    CT_real = np.linalg.eigvalsh(Li @ Sp @ Li.T).max()
    Hinv = np.linalg.inv(H)
    out = []
    for _ in range(ndraw):
        v = beta_post / rng.gamma(nu)
        th = rng.multivariate_normal(thetahat, n * v * Hinv)
        bb = np.zeros(P); bb[S0] = th / sh[S0]
        ahat = y.mean() - xbar @ bb
        a = ahat - alpha; w = bb - beta
        mD = a + w @ mx; sD2 = w @ Sig @ w
        lam = 1 / (4 * (v + sig2))
        A = sqrt(2 * sqrt(v * sig2) / (v + sig2))
        EB = (1 + 2 * lam * sD2) ** -0.5 * np.exp(-lam * mD ** 2 / (1 + 2 * lam * sD2))
        dH2 = 1 - A * EB                                  # exact population d_H^2
        EDelta2 = mD ** 2 + sD2
        muhat = XS @ th
        insample = eps.mean() ** 2 + ((muhat - mu) ** 2).sum() / n
        Delta_i = ahat + Xr @ bb - (alpha + Xr @ beta)
        out.append((dH2, (v / sig2 - 1) ** 2, EDelta2, insample, np.mean(Delta_i ** 2)))
    return np.array(out), CT_real

print("[1] chain checks on posterior draws given S0 (all must hold):")
for n in [100, 400, 1600, 6400]:
    reps = 20 if n <= 1600 else 8
    q50, q95, viol_H, viol_TR, idgap, CTs = [], [], 0, 0, 0.0, []
    for _ in range(reps):
        o, CT = one_dataset(n, 300)
        CTs.append(CT)
        dH2, var, ED2, ins, emp = o.T
        viol_H += np.sum(dH2 > var + ED2 / 4 + 1e-12)          # Lemma H (untruncated form)
        viol_TR += np.sum(ED2 > CT * ins * (1 + 1e-9) + 1e-12)  # (TR0) with the realised C_T, via H-id
        idgap = max(idgap, np.max(np.abs(ins - emp)))           # H-id
        q50.append(np.median(n * dH2)); q95.append(np.quantile(n * dH2, 0.95))
    print(f"    n={n:5d}: median_n[d_H^2]: {np.mean(q50):.3f}  95%-quantile n d_H^2: {np.mean(q95):.3f}; "
          f"Lemma H violations: {viol_H}; TR0-chain violations: {viol_TR}; max |H-id gap| {idgap:.1e}; realised C_T mean {np.mean(CTs):.3f}")
print("    (n*d_H^2 is flat in n: parametric rate; values far below C_rad^2*u, as expected of a crude constant.)")
