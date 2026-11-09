"""Inequality-level falsification of L4 (Theorem F changed steps and Lemma T), py -3.13.

Fixed design EP: candidates X (n x p, equicorr 0.3, standardised), S0C = {0,1,2}, theta = (1, .8, .6) (standardised scale),
r orthogonal to 1 and every candidate column with ||r||^2/N = Delta; y = mu^C + r + eps, sigma = 1.
Everything is computed on centred n-vectors (isometric to contrast coordinates: ||U'v|| = ||v|| for centred v).
Checks, for random models S (supersets, underfitting, arbitrary), per data set:
 C1 Lemma S: Q^c_S = Qtilde_S + c_n, c_n = ||r||^2 + 2 r'e (relative error)
 C2 ongood(b) core: Q^c_S >= ||r||^2 + 2r'e + ||(I-P_S)e||^2 for S ⊇ S0 ; and (G5) => ||r||^2 + 2r'e >= -2 log n
 C3 ongood(c) core: 2b + Q^c_S <= E^C + V_S for underfitting S
 C4 Lemma T: uniform 2b + Q^c_{S'} >= ||r||^2 + 2r'e + ||e||^2 - ||P_V e||^2 for S' ⊇ S0;
    and log l(S')/l(S0) <= log w-ratio + nu*log(1 + X/B) with X <= n/(n+1)[||(P_S'-P_S0)e||^2 + eta ||y||^2] (the
    (B3) step) -- reported as the max of (lhs - rhs) (should be <= 0).
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
B0 = A0 = 0.01


def logw(p, k):
    return math.log(0.5) - (math.lgamma(2 * p) - math.lgamma(k + 1) - math.lgamma(2 * p - k))


def pn2(XS, v):
    """||P_S v||^2 via reduced QR (no n x n matrices)."""
    if XS.shape[1] == 0:
        return 0.0
    Q, _ = np.linalg.qr(XS)
    return float(np.sum((Q.T @ v) ** 2))


def tq(X, S, v, n):
    """t_S(v) = n v'X_S H^{-1} X_S' v with H = (n+1)G_S + I."""
    if len(S) == 0:
        return 0.0
    XS = X[:, S]
    H = (n + 1) * XS.T @ XS + np.eye(len(S))
    z = XS.T @ v
    return n * float(z @ np.linalg.solve(H, z))


def logD(X, S, n):
    if len(S) == 0:
        return 0.0
    G = X[:, S].T @ X[:, S]
    return np.linalg.slogdet((n + 1) * G + np.eye(len(S)))[1] - np.linalg.slogdet(G + np.eye(len(S)))[1]


def run(n, p, Delta, seed, nmodels=300):
    rg = np.random.default_rng(seed)
    S0 = [0, 1, 2]
    Xr = rg.multivariate_normal(np.zeros(p), 0.7 * np.eye(p) + 0.3, size=n)
    Xc = Xr - Xr.mean(0)
    X = Xc / np.sqrt((Xc ** 2).sum(0) / (n - 1))
    th = np.zeros(p); th[S0] = [1.0, 0.8, 0.6]
    muC = X @ th
    w = rg.standard_normal(n); w -= w.mean()
    Qx, _ = np.linalg.qr(X)
    r = w - Qx @ (Qx.T @ w)
    r *= math.sqrt(Delta * (n - 1) / float(r @ r))
    e = rg.standard_normal(n); e -= e.mean()       # centred noise (contrast noise has the same law in R^N)
    y = muC + r + e
    N = n - 1
    nu = A0 + n / 2
    b = B0 * float(y @ y) / N
    yt = y - r
    cn = float(r @ r) + 2 * float(r @ e)
    logn = math.log(n)
    out = {"n": n, "p": p, "Delta": Delta, "seed": seed, "G5": abs(float(r @ e)) <= math.sqrt(float(r @ r)) * math.sqrt(2 * logn)}
    c1 = c2 = c3 = c4a = c4b = -np.inf
    rest = [j for j in range(p) if j not in S0]
    Q0 = float(y @ y) - tq(X, S0, y, n)
    eta = 1.0 / ((n + 1) * N * 0.5)  # eta_n with phi0^2 = 1/2 (only used in an upper bound; larger phi0 -> smaller eta)
    lam_S0 = np.linalg.eigvalsh(X[:, S0].T @ X[:, S0] / N).min()
    eta = 1.0 / ((n + 1) * N * lam_S0)
    for _ in range(nmodels):
        kind = rg.integers(3)
        j = int(rg.integers(1, min(30, p - 3) + 1))
        J = list(rg.choice(rest, size=j, replace=False))
        if kind == 0:
            S = sorted(S0 + J)                                  # superset
        else:
            keep = [s for s in S0 if rg.random() < 0.5]
            if len(keep) == 3:
                keep = keep[:2]
            S = sorted(keep + J)                                # underfitting
        Qc = float(y @ y) - tq(X, S, y, n)
        Qt = float(yt @ yt) - tq(X, S, yt, n)
        c1 = max(c1, abs(Qc - Qt - cn) / Qc)
        pSe = pn2(X[:, S], e)
        if set(S0) <= set(S):
            lb = float(r @ r) + 2 * float(r @ e) + float(e @ e) - pSe
            c2 = max(c2, lb - Qc)
            lbT = float(r @ r) + 2 * float(r @ e) + float(e @ e) - pn2(X, e)
            c4a = max(c4a, lbT - (2 * b + Qc))
            # (B3)-step bound for Lemma T
            X_ = tq(X, S, y, n) - tq(X, S0, y, n)
            ub = n / (n + 1) * ((pSe - pn2(X[:, S0], e)) + eta * float(y @ y))
            c4b = max(c4b, X_ - ub)
        else:
            Sp = sorted(set(S) | set(S0))
            V = pn2(X[:, Sp], y) - pn2(X[:, S], y)
            E = 2 * b + float((r + e) @ (r + e)) + 2 / (n + 1) * float(y @ y)
            if np.linalg.eigvalsh(X[:, S].T @ X[:, S]).min() >= N * 0.05 and N * 0.05 >= 1:
                c3 = max(c3, (2 * b + Qc) - (E + V))
    out.update({"C1_rel_identity_err": c1, "C2_superset_lb_violation": c2, "C3_underfit_ub_violation": c3,
                "C4a_uniform_lb_violation": c4a, "C4b_B3_violation": c4b,
                "rr_plus_2re_plus_2logn": cn + 2 * logn})
    return out


if __name__ == "__main__":
    rows = []
    for n in (200, 800):
        for Delta in (0.5, 4.0):
            for seed in range(10):
                rows.append(run(n, 40, Delta, 1000 * n + 10 * seed + int(Delta)))
    json.dump(rows, open(os.path.join(HERE, "check_L4_results.json"), "w"), default=float)
    keys = ["C1_rel_identity_err", "C2_superset_lb_violation", "C3_underfit_ub_violation", "C4a_uniform_lb_violation",
            "C4b_B3_violation"]
    lines = ["# check_L4 summary (max over 300 random models x 10 seeds per cell; violations must be <= ~1e-8)", "",
             "| n | Delta | " + " | ".join(keys) + " | min(||r||^2+2r'e+2log n) on G5 | G5 freq |", "|" + "---|" * (len(keys) + 4)]
    for n in (200, 800):
        for Delta in (0.5, 4.0):
            rs = [r for r in rows if r["n"] == n and r["Delta"] == Delta]
            g5 = [r for r in rs if r["G5"]]
            lines.append(f"| {n} | {Delta} | " + " | ".join(f"{max(r[k] for r in rs):.2e}" for k in keys) +
                         f" | {min(r['rr_plus_2re_plus_2logn'] for r in g5) if g5 else float('nan'):.3f} | {len(g5)}/{len(rs)} |")
    open(os.path.join(HERE, "check_L4_summary.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
