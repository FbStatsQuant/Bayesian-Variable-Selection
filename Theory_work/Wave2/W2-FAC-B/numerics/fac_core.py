"""fac_core.py -- W2-FAC-B numerics: exact-Gram factor designs at large n, start mode and the LS0 path.

Exact-Gram reduction (fixed design, X centred, X'X = (n-1) Sigma, p <= n-1, noise e = C eps, eps ~ N(0, s2 I)):
  X'e = sigma sqrt(n-1) g,  g ~ N(0, Sigma);   ||e||^2 = s2 (g' Sigma^-1 g + chi2_{n-1-p}).
  With g = Lam eta + zeta (eta ~ N(0,I_k), zeta ~ N(0,Psi)) the factor pieces are recorded too.
  y = (mu + e)/s, s^2 = ||mu+e||^2/(n-1);  z = X'y;  y'y = n-1.
Score (SoP 04_theory.tex:69-74, as bvs_core.Problem.logm_idx):
  log m(U) = -1/2[logdet((n+1)G_U + I) - logdet(G_U + I)] - nu log(0.02 + Q_U),  G_U = (n-1) Sigma_UU,
  Q_U = (n-1) - n z_U' H_U^-1 z_U,  nu = 0.01 + n/2;   F(S) = log w(|S|) + log m(S).
Start mode, tables and partition: bvs_core (copied unchanged from Wave1C/C-GROW/numerics).
LS0 path: production local search (flip + swap neighbourhood, best strict improvement, exact float ties ->
lexicographically smallest set), uncapped, every scan computed in closed form (Schur complements); verified
against direct scoring in fac_selftest.py.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import math
import numpy as np
from scipy.special import gammaln
import bvs_core as bc


# ----------------------------------------------------------------------------------------------- designs
def s5_sigma(p):
    """study S5: 0.3*11' + 0.4*H + 0.3*I, H = groups of 5. Factor form: Lam = sqrt(.3)*1 (k=1), Psi = .4H+.3I."""
    grp = np.arange(p) // 5
    H = (grp[:, None] == grp[None, :]).astype(float)
    Lam = math.sqrt(0.3) * np.ones((p, 1))
    Psi = 0.4 * H + 0.3 * np.eye(p)
    return Lam @ Lam.T + Psi, Lam, Psi


def factor_sigma(p, loadings, psi_diag):
    """Sigma = Lam Lam' + diag(psi), standardised to unit diagonal (loadings rows rescaled)."""
    Lam = np.asarray(loadings, float).reshape(p, -1)
    psi = np.asarray(psi_diag, float)
    d = np.sqrt((Lam ** 2).sum(1) + psi)
    Lam = Lam / d[:, None]
    psi = psi / d ** 2
    Psi = np.diag(psi)
    return Lam @ Lam.T + Psi, Lam, Psi


def study_layout(p, c=1.0, s0=4, step=5):
    """diagnostic layout of C-GROW (truths 0-based 2,26,53,75 for s0=4; coefficients c*(1.4,-1,1.8,-1.2))."""
    POS = (3, 2, 4, 1, 5, 3)
    PATTERN = (1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
    k = np.arange(s0)
    block = 1 + step * k
    pos = np.array([POS[i % 6] for i in k])
    act = 5 * (block - 1) + pos - 1
    th = np.zeros(p)
    th[act] = c * np.array([PATTERN[i % 6] for i in k])
    return th, tuple(int(a) for a in sorted(act))


# ----------------------------------------------------------------------------------------------- data
class ExactGram:
    """Sufficient statistics of one exact-Gram data set; quacks like bvs_core.Problem for tables/start mode."""

    def __init__(self, Sigma, theta, n, rng, sigma2=1.0, Lam=None, Psi=None):
        p = Sigma.shape[0]
        assert p <= n - 1
        self.n, self.p = n, p
        self.K = min(p, n // 2)
        self.Sigma = Sigma
        sig = math.sqrt(sigma2)
        if Lam is not None:
            k = Lam.shape[1]
            self.eta = rng.standard_normal(k)
            self.zeta = np.linalg.cholesky(Psi) @ rng.standard_normal(p)
            g = Lam @ self.eta + self.zeta
        else:
            g = np.linalg.cholesky(Sigma) @ rng.standard_normal(p)
        self.g = g
        chi = rng.chisquare(n - 1 - p) if n - 1 - p > 0 else 0.0
        gSg = float(g @ np.linalg.solve(Sigma, g))
        nm1 = n - 1.0
        mu2 = nm1 * float(theta @ Sigma @ theta)
        cross = 2.0 * sig * math.sqrt(nm1) * float(theta @ g)
        e2 = sigma2 * (gSg + chi)
        s = math.sqrt((mu2 + cross + e2) / nm1)
        self.Xty = (nm1 * (Sigma @ theta) + sig * math.sqrt(nm1) * g) / s
        self.XtX = nm1 * Sigma
        self.yty = nm1
        self.nu = 0.01 + n / 2.0
        self.logw = bc.log_prior_w(p, self.K)
        self.logm0 = -self.nu * math.log(0.02 + self.yty)
        self.cache = {(): self.logm0}
        self.scale_s = s

    logm_idx = bc.Problem.logm_idx
    logm_many = bc.Problem.logm_many
    logm = bc.Problem.logm
    F = bc.Problem.F
    F_many = bc.Problem.F_many


# ----------------------------------------------------------------------------------------------- scan
def scan(P, T):
    """All flip/swap neighbours of T (sorted tuple) in closed form.
    Returns dict with F(T) and arrays: add (l, F), del (j, F), swap (j, l, F matrix)."""
    n, p, K = P.n, P.p, P.K
    T = np.asarray(T, dtype=np.int64)
    k = len(T)
    inT = np.zeros(p, bool)
    inT[T] = True
    O = np.flatnonzero(~inT)
    c1 = n + 1.0
    XtX, z = P.XtX, P.Xty
    nu = P.nu
    yty = P.yty
    lw = P.logw

    def Fval(ld1, ld2, quad, size):
        Q = yty - n * quad
        return lw[size] - 0.5 * (ld1 - ld2) - nu * np.log(0.02 + Q)

    out = dict(T=tuple(int(t) for t in T), O=O)
    if k == 0:
        out["FT"] = P.logm0 + lw[0]
        d1 = c1 * np.diag(XtX)[O] + 1.0
        d2 = np.diag(XtX)[O] + 1.0
        quad = z[O] ** 2 / d1
        out["add"] = Fval(np.log(d1), np.log(d2), quad, 1) if K >= 1 else None
        out["del"] = np.array([])
        out["swap"] = np.zeros((0, len(O)))
        return out
    G = XtX[np.ix_(T, T)]
    M1 = c1 * G + np.eye(k)
    M2 = G + np.eye(k)
    L1 = np.linalg.cholesky(M1)
    L2 = np.linalg.cholesky(M2)
    ld1 = 2 * np.log(np.diag(L1)).sum()
    ld2 = 2 * np.log(np.diag(L2)).sum()
    W1 = np.linalg.inv(M1)
    W1 = 0.5 * (W1 + W1.T)
    W2 = np.linalg.inv(M2)
    W2 = 0.5 * (W2 + W2.T)
    zT = z[T]
    u = W1 @ zT
    quadT = float(zT @ u)
    out["FT"] = float(Fval(ld1, ld2, quadT, k))
    w1 = np.diag(W1).copy()
    w2 = np.diag(W2).copy()
    # deletions
    qd = quadT - u ** 2 / w1
    out["del"] = Fval(ld1 + np.log(w1), ld2 + np.log(w2), qd, k - 1)
    if len(O) == 0:
        out["add"] = np.array([])
        out["swap"] = np.zeros((k, 0))
        return out
    A2 = XtX[np.ix_(T, O)]
    A1 = c1 * A2
    V1 = W1 @ A1
    V2 = W2 @ A2
    dO = np.diag(XtX)[O]
    s1 = (c1 * dO + 1.0) - (A1 * V1).sum(0)
    s2 = (dO + 1.0) - (A2 * V2).sum(0)
    bil = z[O] - A1.T @ u
    if k < K:
        out["add"] = Fval(ld1 + np.log(s1), ld2 + np.log(s2), quadT + bil ** 2 / s1, k + 1)
    else:
        out["add"] = np.full(len(O), -np.inf)
    # swaps j out (row), l in (col)
    S1 = s1[None, :] + V1 ** 2 / w1[:, None]
    S2 = s2[None, :] + V2 ** 2 / w2[:, None]
    B = bil[None, :] + V1 * (u / w1)[:, None]
    qs = qd[:, None] + B ** 2 / S1
    out["swap"] = Fval((ld1 + np.log(w1))[:, None] + np.log(S1), (ld2 + np.log(w2))[:, None] + np.log(S2), qs, k)
    return out


def best_move(sc, S0set):
    """production rule: best scanned neighbour; strict improvement; exact ties -> lexicographically smallest set.
    Returns (newT or None, info)."""
    T = list(sc["T"])
    O = sc["O"]
    FT = sc["FT"]
    cands = []  # (F, newset, type)
    add, dl, sw = sc["add"], sc["del"], sc["swap"]
    best = -np.inf
    if add is not None and len(add):
        best = max(best, float(np.max(add)))
    if len(dl):
        best = max(best, float(np.max(dl)))
    if sw.size:
        best = max(best, float(np.max(sw)))
    info = dict(FT=FT, best=best,
                best_add=float(np.max(add)) - FT if add is not None and len(add) else -np.inf,
                best_del_N=-np.inf, best_del_T=-np.inf, best_swap=-np.inf, best_swap_T=-np.inf)
    Tarr = np.array(T)
    isN = np.array([t not in S0set for t in T])
    if len(dl):
        if isN.any():
            info["best_del_N"] = float(dl[isN].max()) - FT
        if (~isN).any():
            info["best_del_T"] = float(dl[~isN].max()) - FT
    if sw.size:
        if isN.any():
            info["best_swap"] = float(sw[isN].max()) - FT
        if (~isN).any():
            info["best_swap_T"] = float(sw[~isN].max()) - FT
    if not best > FT:
        return None, info
    if add is not None and len(add):
        for i in np.flatnonzero(add == best):
            cands.append((tuple(sorted(T + [int(O[i])])), "+" + ("T" if int(O[i]) in S0set else "N")))
    for i in np.flatnonzero(dl == best):
        cands.append((tuple(t for t in T if t != T[i]), "-" + ("T" if T[i] in S0set else "N")))
    if sw.size:
        for i, j in zip(*np.nonzero(sw == best)):
            j_out, l_in = T[i], int(O[j])
            ns = tuple(sorted([t for t in T if t != j_out] + [l_in]))
            cands.append((ns, "sw" + ("T" if j_out in S0set else "N") + ">" + ("T" if l_in in S0set else "N")))
    cands.sort()
    info["n_ties"] = len(cands)
    return cands[0][0], dict(info, move=cands[0][1])


def ls0_path(P, centre, S0, max_moves=100000, record=None):
    S0set = set(S0)
    T = tuple(sorted(centre))
    steps = []
    scored_S0 = (T == tuple(sorted(S0)))
    while True:
        sc = scan(P, T)
        if not scored_S0:
            # S0 scored if it is a neighbour of T
            sd = set(T) ^ S0set
            if len(sd) == 1 or (len(sd) == 2 and len(set(T) - S0set) == 1 and len(S0set - set(T)) == 1):
                scored_S0 = True
        nxt, info = best_move(sc, S0set)
        info["size"] = len(T)
        info["extras"] = len(set(T) - S0set)
        info["missing"] = len(S0set - set(T))
        if record is not None:
            record(P, T, sc, info)
        steps.append(info)
        if nxt is None or len(steps) > max_moves:
            break
        T = nxt
        if T == tuple(sorted(S0)):
            scored_S0 = True
    return dict(final=T, steps=steps, moves=len(steps) - 1, scored_S0=scored_S0)
