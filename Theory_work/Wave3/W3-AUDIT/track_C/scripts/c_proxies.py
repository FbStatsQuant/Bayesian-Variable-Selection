"""W3-AUDIT track C -- proxies P1-P10 (C_PLAN.md v3 §2).  All quantities are computed from a Gram ORACLE
rows(idx) -> G[idx, :] with unit diagonal: the sample correlation R_hat = Z'Z (Z centred, unit-norm columns) or the
population Sigma.  Searches give UPPER bounds on minima (they can refute a floor, never certify it); the refined
Gershgorin bound and lambda_min(Sigma) are LOWER bounds.  Qualitative readings only (HQ rule 11-16: explicit proof
constants are not tested).
"""
import math
import numpy as np
from scipy.special import gammaln
from scipy.sparse.linalg import LinearOperator, eigsh


# ---------------------------------------------------------------------------------------------------------------------
# oracles
class SampleOracle:
    def __init__(self, Z):
        self.Z = Z; self.n, self.p = Z.shape

    def rows(self, idx):
        idx = np.atleast_1d(np.asarray(idx, int))
        return self.Z[:, idx].T @ self.Z


class PopOracle:
    def __init__(self, design):
        self.d = design; self.p = design.p

    def rows(self, idx):
        return self.d.sigma_rows(np.atleast_1d(np.asarray(idx, int)))


# ---------------------------------------------------------------------------------------------------------------------
# sparse minimum eigenvalues
def bordered_lmin(GSS, GSc, exclude=None, iters=60):
    """lambda_min(G_{S u {c}}) for every candidate column c of GSc (= G[S, cands]), unit diagonal, by the secular
    equation 1 - lam - sum_i w_ic^2/(d_i - lam) = 0 on (-inf, d_1); bisection with pruning.  Pruned candidates (which
    cannot be the argmin) get +inf: only the min / argmin is exact.  Returns (vals, lambda_min(G_SS))."""
    d, Q = np.linalg.eigh(GSS)
    m = GSc.shape[1]
    act = np.ones(m, bool)
    if exclude is not None:
        act[exclude] = False
    idx = np.flatnonzero(act)
    W = (Q.T @ GSc[:, idx]) ** 2
    lo = np.full(idx.size, min(0.0, d[0]) - 1e-9); hi = np.full(idx.size, d[0])
    for it in range(iters):
        mid = 0.5 * (lo + hi)
        with np.errstate(divide="ignore", invalid="ignore"):
            f = 1.0 - mid - (W / (d[:, None] - mid[None, :])).sum(0)
        up = f > 0
        lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
        if it % 4 == 3 and idx.size > 1:
            keep = lo <= hi.min() + 1e-15
            if not keep.all():
                idx, W, lo, hi = idx[keep], W[:, keep], lo[keep], hi[keep]
    vals = np.full(m, np.inf); vals[idx] = 0.5 * (lo + hi)
    return vals, float(d[0])


def greedy_chain(oracle, start, kmax):
    """Greedy chain: from S = start add the column that most lowers lambda_min(G_S).  lam[k] = exact lambda_min of the
    first k elements (k >= len(start)), an UPPER bound on the k-sparse (anchored) minimum."""
    S = list(map(int, start)); GR = oracle.rows(S); lam = {}
    while len(S) < kmax:
        vals, d0 = bordered_lmin(GR[:, S], GR, exclude=S)
        lam[len(S)] = d0
        c = int(np.argmin(vals)); S.append(c)
        GR = np.vstack([GR, oracle.rows([c])])
    lam[len(S)] = float(np.linalg.eigvalsh(GR[:, S])[0])
    return S, lam


def chunk_pass(Z, K, taus, chunk=512):
    """One pass over R_hat = Z'Z in row chunks (never stored).  Returns: top pair (i, j, |r|); refined Gershgorin
    lower bound LB(k) = 1 - max_j (sum of the k-1 largest |r_jl|, l != j) for k = 2..K+1; per-row degrees
    #{l : |r_jl| > tau} for each tau."""
    n, p = Z.shape
    K = min(K, p - 1)
    csmax = np.zeros(K)
    deg = np.zeros((len(taus), p), int)
    best = (-1.0, 0, 1)
    for a in range(0, p, chunk):
        ii = np.arange(a, min(p, a + chunk))
        C = np.abs(Z[:, ii].T @ Z)
        C[np.arange(ii.size), ii] = 0.0
        for t, tau in enumerate(taus):
            deg[t, ii] = (C > tau).sum(1)
        r = np.argmax(C.max(1)); c = int(np.argmax(C[r]))
        if C[r, c] > best[0]:
            best = (float(C[r, c]), int(ii[r]), c)
        part = -np.partition(-C, K - 1, axis=1)[:, :K]
        part = -np.sort(-part, axis=1)
        csmax = np.maximum(csmax, np.cumsum(part, axis=1).max(0))
    lb = {k: 1.0 - csmax[k - 2] for k in range(2, K + 2)}
    return {"top": best, "gersh": lb, "deg": deg}


def lse(v):
    v = np.asarray(v, float)
    if v.size == 0:
        return -np.inf
    m = v.max()
    return m + math.log(np.exp(v - m).sum()) if np.isfinite(m) else m


def lchoose(a, b):
    return gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1)


def msharp(n, p, s0):
    """m#_n = m#_n(1/2 log n) of W3-POST STATEMENT §0 (port of diag_lib.R::msharp)."""
    K = min(p, n // 2); k = np.arange(K + 1)
    lw = lambda kk: -math.log(2) - lchoose(2 * p - 1, kk)
    term = lchoose(p, k) + lw(k) - lw(s0)
    thr = -(s0 + 2) / 2 * math.log(n)
    for m in range(s0, max(K, s0) + 1):
        lR = -np.inf if m + 1 > K else lse(term[m + 1:])
        if lR <= thr:
            return m
    return K


# ---------------------------------------------------------------------------------------------------------------------
# conditional (partial) covariances along a growing conditioning set U
class Cond:
    """Keeps B = L^{-1} G[U, :] (rows orthonormalised), so Cov(a, b | U) = G_ab - B[:, a]'B[:, b].  Optional signal
    mu = sum theta_k W_k: gmu = G theta (p-vector), vmu = theta'G_{S0 S0}theta."""

    def __init__(self, oracle, p, gmu=None, vmu=None):
        self.o = oracle; self.p = p; self.U = []
        self.B = np.zeros((0, p)); self.var = np.ones(p)
        self.gmu = gmu; self.vmu = vmu; self.bmu = np.zeros(0)

    def add(self, u, Grow=None):
        Gu = self.o.rows([u])[0] if Grow is None else Grow
        bu = self.B[:, u]
        s2 = Gu[u] - bu @ bu
        if s2 <= 1e-12:
            return False
        s = math.sqrt(s2)
        newrow = (Gu - bu @ self.B) / s
        if self.gmu is not None:
            self.bmu = np.r_[self.bmu, (self.gmu[u] - bu @ self.bmu) / s]
        self.B = np.vstack([self.B, newrow]); self.var = self.var - newrow ** 2
        self.U.append(int(u))
        return True

    def cov_with(self, Grow_j, j):
        return Grow_j - self.B[:, j] @ self.B

    def cov_mu(self):
        return self.gmu - self.bmu @ self.B

    def var_mu(self):
        return self.vmu - self.bmu @ self.bmu


def visibility_path(oracle, p, S0, theta, j, Gj, gmu, vmu, umax=15):
    """Greedy masking for truth column j: U grows by the column that most lowers
    delta2_{U,j} = Cov(j, mu | U)^2 / Var(j | U).  Returns the list of (U-prefix size, delta2) and the U path."""
    cd = Cond(oracle, p, gmu, vmu)
    out = []
    for step in range(umax + 1):
        cj = cd.cov_with(Gj, j); vj = max(cj[j], 1e-15)
        cm = cd.cov_mu(); mj = cm[j]
        out.append(mj * mj / vj)
        if step == umax:
            break
        vc = cd.var.copy()
        ok = vc > 1e-10; ok[j] = False; ok[cd.U] = False
        a = cj; m = cm
        with np.errstate(divide="ignore", invalid="ignore"):
            num = (mj - a * m / vc) ** 2
            den = np.maximum(vj - a * a / vc, 1e-15)
            new = np.where(ok, num / den, np.inf)
        c = int(np.argmin(new))
        if not np.isfinite(new[c]) or not cd.add(c):
            break
    return np.array(out), list(cd.U)


def margin_path(oracle, p, S0, theta, j, gmu, vmu, j0):
    """(ID) margin proxy for truth column j: start at U = S0 \\ {j}, greedily add (excluding j) the column with the
    largest reduction of Var(mu | U); returns Var(mu | U) after j0 additions (an UPPER bound on
    min_{|J| <= j0} Delta_{(S0 \\ j) u J})."""
    cd = Cond(oracle, p, gmu, vmu)
    for u in S0:
        if u != j:
            cd.add(u)
    path = [cd.var_mu()]
    for _ in range(j0):
        cm = cd.cov_mu(); vc = cd.var.copy()
        ok = vc > 1e-10; ok[j] = False; ok[cd.U] = False
        red = np.where(ok, cm * cm / np.maximum(vc, 1e-15), -np.inf)
        c = int(np.argmax(red))
        if not np.isfinite(red[c]) or not cd.add(c):
            break
        path.append(cd.var_mu())
    return float(min(path))


def leakage_scores(oracle, p, S0, theta, gmu, vmu, umax=15):
    """Population leakage g_l = max over U in a family, j in S0 \\ U of |Cov(W_l, W_j | W_U)|; family = {empty set,
    S0 \\ {j}, every prefix of the greedy masking path of each j}.  A max over a SUBFAMILY: g_l is a lower bound of the
    true sup, so the leak set built from it is a SUBSET of the true one."""
    GS = oracle.rows(S0)
    g = np.abs(GS).max(0)                                            # U = empty
    fams = []
    for jj, j in enumerate(S0):
        fams.append([u for u in S0 if u != j])
        _, Upath = visibility_path(oracle, p, S0, theta, j, GS[jj], gmu, vmu, umax)
        fams.extend(Upath[:k] for k in range(1, len(Upath) + 1))
    for U in fams:
        cd = Cond(oracle, p)
        for u in U:
            cd.add(u)
        for jj, j in enumerate(S0):
            if j in cd.U:
                continue
            g = np.maximum(g, np.abs(cd.cov_with(GS[jj], j)))
    g[list(S0)] = np.inf
    return g


# ---------------------------------------------------------------------------------------------------------------------
# P8 Occam sum, first two terms (sample)
def occam_terms(Z, S0, top=200):
    n, p = Z.shape
    s0 = len(S0); S0 = list(S0)
    G_S = (n - 1) * (Z[:, S0].T @ Z)                                 # s0 x p,  G = X'X with ||x||^2 = n - 1
    GSS = G_S[:, S0]
    H = (n + 1) * GSS + np.eye(s0); A = GSS + np.eye(s0)
    Hi_g = np.linalg.solve(H, G_S); Ai_g = np.linalg.solve(A, G_S)
    h = (n + 1) * (n - 1) + 1 - (n + 1) ** 2 * (G_S * Hi_g).sum(0)
    a = (n - 1) + 1 - (G_S * Ai_g).sum(0)
    mask = np.ones(p, bool); mask[S0] = False
    ratio = np.where(mask, a / h, 0.0)                               # D_{S0}/D_{S0 u l}
    t1 = (s0 + 1) / (2 * p - 1 - s0) * np.sqrt(np.maximum(ratio, 0)).sum()
    # j = 2 over the top-`top` columns by ratio
    T = np.argsort(-ratio)[:min(top, mask.sum())]
    GTT = (n - 1) * (Z[:, T].T @ Z[:, T])
    hTT = (n + 1) * GTT - (n + 1) ** 2 * (G_S[:, T].T @ Hi_g[:, T])
    aTT = GTT - G_S[:, T].T @ Ai_g[:, T]
    hd = np.diag(hTT).copy(); ad = np.diag(aTT).copy()
    hd = (n + 1) * (n - 1) + 1 - (n + 1) ** 2 * (G_S[:, T] * Hi_g[:, T]).sum(0)
    ad = n - (G_S[:, T] * Ai_g[:, T]).sum(0)
    iu = np.triu_indices(T.size, 1)
    num = ad[iu[0]] * ad[iu[1]] - aTT[iu] ** 2
    den = hd[iu[0]] * hd[iu[1]] - hTT[iu] ** 2
    w2 = (s0 + 1) * (s0 + 2) / ((2 * p - 1 - s0) * (2 * p - 2 - s0))
    t2 = w2 * np.sqrt(np.maximum(num / den, 0)).sum()
    return float(t1), float(t2)


# ---------------------------------------------------------------------------------------------------------------------
# lattice sample, local regressions (P6) and lattice width (P9)
def lattice_sets(Q, S0, cap, rng, draws=5):
    extra = np.array([q for q in Q if q not in set(S0)], int)
    m = extra.size
    sizes = sorted(set([0, m // 4, m // 2, m]))
    sets = []
    for sz in sizes:
        sz = min(sz, max(cap - len(S0), 0))
        for _ in range(1 if sz in (0, m) and m <= cap - len(S0) else draws):
            pick = rng.choice(extra, sz, replace=False) if sz > 0 else np.zeros(0, int)
            sets.append(np.r_[np.asarray(S0, int), np.sort(pick)])
    return sets


def local_and_width(Z, Rrows_fn, sets, ndraw, rng, Lvals=(0.1, 0.05), nus=(0, 4, 8)):
    """For each lattice set T and every l not in T: coefficients bbar_{T,l} of x_l on X_T; nu_hat(L) = smallest nu
    with l1 tail beyond the nu largest |coef| <= L (max over l and T).  Width: w0 = mean over draws g of
    max_{T,l} (|u_{T,l}'g| - a0(|T|)), a0(k) = sqrt(log(n+1) + 2 log(p/(k+1)))."""
    n, p = Z.shape
    Gg = rng.standard_normal((n, ndraw))
    ZtG = Z.T @ Gg                                                   # p x ndraw
    nu = {L: 0 for L in Lvals}; nu_q99 = {L: 0.0 for L in Lvals}; l1max = 0.0
    tmax = {v: 0.0 for v in nus}; tq99 = {v: 0.0 for v in nus}
    wmax = np.full(ndraw, -np.inf)
    for T in sets:
        RT = Rrows_fn(T)                                             # |T| x p
        RTT = RT[:, T]
        cf = np.linalg.solve(RTT, RT)                                # |T| x p
        res2 = 1.0 - (RT * cf).sum(0)
        out = np.ones(p, bool); out[T] = False
        ok = out & (res2 > 1e-10)
        A = np.abs(cf[:, ok])
        As = -np.sort(-A, axis=0)
        tail = As.sum(0)[None, :] - np.cumsum(np.vstack([np.zeros((1, A.shape[1])), As]), axis=0)  # tail[nu]
        l1max = max(l1max, float(As.sum(0).max()))
        for v in nus:
            tv = tail[min(v, tail.shape[0] - 1)]
            tmax[v] = max(tmax[v], float(tv.max())); tq99[v] = max(tq99[v], float(np.quantile(tv, 0.99)))
        for L in Lvals:
            nuh = (tail > L).sum(0)                                  # smallest nu with tail <= L
            nu[L] = max(nu[L], int(nuh.max())); nu_q99[L] = max(nu_q99[L], float(np.quantile(nuh, 0.99)))
        # width
        proj = (ZtG[ok] - cf[:, ok].T @ ZtG[T]) / np.sqrt(res2[ok])[:, None]
        a0 = math.sqrt(math.log(n + 1) + 2 * math.log(p / (len(T) + 1)))
        wmax = np.maximum(wmax, np.abs(proj).max(0) - a0)
    return nu, nu_q99, l1max, float(wmax.mean()), tmax, tq99


# ---------------------------------------------------------------------------------------------------------------------
# P10 operator norm
def op_norm_diff(Z, sigma_matvec):
    n, p = Z.shape
    op = LinearOperator((p, p), matvec=lambda v: Z.T @ (Z @ v) - sigma_matvec(np.ravel(v)), dtype=float)
    return float(abs(eigsh(op, k=1, which="LM", tol=1e-3, maxiter=3000, return_eigenvectors=False)[0]))
