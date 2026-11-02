"""Lemma E numerics (API-PXNGAP §4) on LH-iid at (n, p) = (200, 500) and (400, 1000), g = 10, rho = .7, psi = .5, c = 1, v = 1.
Checks (E1) eta_A range, (E2) a_A range, (E3) RSS floor and ||Y||^2 bound, (E4) remainder range over the family,
(E5) |RSS_A - n sigma^2 - Lambda_A| / n^{2/3}, for all within-group subsets of 6 groups and 3000 random sets of size <= s0+2.
Seeds fixed per replicate."""
import math, sys
import numpy as np
from pxn_core import *
sys.path.insert(0, '.')
from lh_gen import gen_lh

def exact_parts(D, A, _unused, mu, Yc):
    """returns log D_A, Q_A, RSS^y_A, RSS_A (raw-centred), Lambda_A, lam_min(R_A)."""
    n = D.n
    if len(A) == 0:
        return 0.0, n - 1.0, n - 1.0, float(Yc @ Yc), float(mu @ mu), 1.0
    Xs = D.X[:, A]; G = Xs.T @ Xs; k = len(A)
    H = (n + 1) * G + np.eye(k)
    ldD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(k))[1]
    z = D.z[A]
    Q = (n - 1) - n * z @ np.linalg.solve(H, z)
    RSSy = (n - 1) - z @ np.linalg.solve(G, z)
    Qm, _ = np.linalg.qr(Xs)
    resY = Yc - Qm @ (Qm.T @ Yc); RSS = float(resY @ resY)
    resmu = mu - Qm @ (Qm.T @ mu); Lam = float(resmu @ resmu)
    lmin = float(np.linalg.eigvalsh(G / (n - 1)).min())
    return float(ldD), float(Q), float(RSSy), RSS, Lam, lmin

for (n, p) in ((200, 500), (400, 1000)):
    g, G = 10, p // 10
    rng = np.random.default_rng(1000 + n)
    X, y, groups, S0, Sref, M, theta = gen_lh(n, G, g, 0.7, 0.5, [(0, 1, 1.0)], [(2, 1.0)], rng, return_theta=True)
    D = Data(X, y)
    s0 = len(S0); Yc = y - y.mean(); mu = (X - X.mean(0)) @ theta
    sigma2, Mb = 1.0, 2 * float(theta @ theta) + 1  # population M := 2 theta' Sigma theta + 1, Sigma approx by sample below
    # families
    fam = []
    for h in range(6):
        C = groups[h]
        for mask in range(1, 1 << g):
            fam.append([C[t] for t in range(g) if (mask >> t) & 1])
    for _ in range(3000):
        k = int(rng.integers(1, s0 + 3)); fam.append(sorted(rng.choice(p, k, replace=False).tolist()))
    fam.append([])
    phi0sq = None
    rows = []
    for A in fam:
        ldD, Q, RSSy, RSS, Lam, lmin = exact_parts(D, A, None, mu, Yc)
        k = len(A)
        eta = ldD - k * math.log(n + 1)
        a = 2 * B0 + Q - RSSy
        rem = -0.5 * eta - D.nu * math.log1p(a / RSSy)
        rows.append((k, eta, a, RSSy, RSS, Lam, lmin, rem))
    rows = np.array(rows)
    k, eta, a, RSSy, RSS, Lam, lmin, rem = rows.T
    phi0sq = lmin[k > 0].min()
    Mn = (mu @ mu) / n
    cE = sigma2 / (12 * (Mn + sigma2)); kapE = 0.52 / cE + 1
    print(f"\n=== n={n} p={p} s0={s0} |family|={len(fam)} ||mu||^2/n={Mn:.3f} min lam_min(R_A)={phi0sq:.4f} ===")
    print(f"(E1) eta_A in [{eta.min():.4f}, {eta.max():.4f}]; bound [-2k/((n-1)phi0^2), 0] worst={-2*(s0+2)/((n-1)*phi0sq):.4f}  "
          f"{'OK' if (eta.max() <= 1e-12 and (eta >= -2*k/((n-1)*phi0sq) - 1e-12).all()) else 'VIOLATION'}")
    print(f"(E2) a_A in [{a.min():.4f}, {a.max():.4f}]; bound [0.02, {0.02 + 1 + 1/((n-1)*phi0sq):.4f}]  "
          f"{'OK' if (a.min() >= 0.02 - 1e-9 and a.max() <= 0.02 + 1 + 1/((n-1)*phi0sq) + 1e-9) else 'VIOLATION'}")
    print(f"(E3) min RSS_A/(n sigma^2)={RSS.min()/(n*sigma2):.3f} (>= 1/2?) ; ||Y||^2/(3(M+sigma^2)n)={float(Yc@Yc)/(3*(Mn+sigma2)*n):.3f} (<= 1?) ; "
          f"min RSS^y_A/(c_E n)={RSSy.min()/(cE*n):.2f} (>= 1?)")
    print(f"(E4) remainder R_A range over family = [{rem.min():.4f}, {rem.max():.4f}] (spread {rem.max()-rem.min():.4f}); kappa_E={kapE:.2f}; "
          f"2 kappa_E={2*kapE:.2f}  {'OK' if rem.max()-rem.min() <= 2*kapE else 'VIOLATION'}")
    e5 = np.abs(RSS - n * sigma2 - Lam) / n ** (2 / 3)
    print(f"(E5) max |RSS_A - n sigma^2 - Lambda_A| / n^(2/3) = {e5.max():.3f}; cross-term scale sqrt(M n log n)/n^(2/3)={math.sqrt(Mn*n*math.log(n))/n**(2/3):.3f}")
    # the within-group single-addition expansion (4.1): log r(U+l)-log r(U) + 1/2 log(n+1) + nu log(1-x) = R_{U+l}-R_U
    T = Tables(D, groups[:6])
    diffs = []
    for h in range(6):
        C = groups[h]
        for mask in range(1, 1 << g):
            for t in range(g):
                if (mask >> t) & 1: continue
                U = [C[i] for i in range(g) if (mask >> i) & 1]; l = C[t]
                lrU, lrUl = T.lr[h][mask], T.lr[h][mask | (1 << t)]
                _, _, _, RU, _, _ = exact_parts(D, U, None, mu, Yc); _, _, _, RUl, _, _ = exact_parts(D, sorted(U + [l]), None, mu, Yc)
                x = 1 - RUl / RU
                diffs.append(lrUl - lrU + 0.5 * math.log(n + 1) + D.nu * math.log1p(-x))
            if mask > 300: break  # cap work
    diffs = np.array(diffs)
    print(f"(4.1) within-group remainder differences: range [{diffs.min():.4f}, {diffs.max():.4f}] over {len(diffs)} additions; bound 2 kappa_E = {2*kapE:.2f}  "
          f"{'OK' if np.abs(diffs).max() <= 2*kapE else 'VIOLATION'}")
