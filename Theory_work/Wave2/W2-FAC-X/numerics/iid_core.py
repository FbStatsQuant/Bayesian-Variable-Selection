"""iid_core.py -- W2-FAC-X numerics: EXACT sufficient statistics of iid-Gaussian-row factor designs at any n, and a
fast exact LS0 path (production move rule) with O(k (p-k)) incremental scans.

Design law (raw rows iid):  x^r_j = sum_m Lam_{jm} f_m + sqrt(psi_j) u_j,  psi_j = 1 - |Lam_j|^2,  f, u iid N(0, I),
response y^r = X^r beta + sigma eps.  After centring (C = I - 11'/n) the n-vectors (eps, f_1..f_k, u_1..u_p) are iid
N(0, C); all inner products of d = 1 + k + p such vectors are Wishart_d(n-1, I).  Bartlett: W = A A', A lower
triangular, A_ii = sqrt(chi2_{n-1-i}), A_ij ~ N(0,1) (i > j).  Rows of A are coordinates of the vectors in an
orthonormal frame whose first axis is eps/||eps|| (row 0 = eps) and second axis is the part of f_1 orthogonal to eps.
Hence (exact, the representation of lemmas/X1):  xi_j := A[1+k+j, 0] = u_j' eps/||eps||  iid N(0,1),
eta_m := A[1+m, 0] = f_m' eps/||eps||,  and everything else is independent of (xi, eta, ||eps||).
The method standardises columns (D = sample sds) and scales y by s (s^2 = ||Y||^2/(n-1)); theta* = D beta.

Score (SoP 04_theory.tex:69-74):  F(T) = log w(|T|) - 1/2[logdet((n+1)G_T + I) - logdet(G_T + I)] - nu log(0.02 + Q_T),
Q_T = y'y - n z_T' H_T^{-1} z_T, H_T = (n+1)G_T + I, nu = 0.01 + n/2, w(k) = 1/(2 C(2p-1, k)) on |T| <= K.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import math
import numpy as np
from scipy.special import gammaln


def log_prior_w(p, K):
    k = np.arange(K + 1)
    return -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


def ell_cap(n, p):
    return int(math.ceil(math.log2(n + p + 1)))


class IidData:
    """Exact sufficient statistics (X'X, X'y, y'y) of one iid-row data set; quacks like bvs_core.Problem."""

    def __init__(self, Lam, beta, n, rng, sigma=1.0, mode="iid"):
        Lam = np.asarray(Lam, float)
        if Lam.ndim == 1:
            Lam = Lam[:, None]
        p, k = Lam.shape
        d = 1 + k + p
        assert n - 1 >= d, "need n-1 >= 1+k+p"
        self.n, self.p, self.kf = n, p, k
        self.K = min(p, n // 2)
        psi = 1.0 - (Lam ** 2).sum(1)
        assert (psi > 0).all()
        # Bartlett factor
        A = np.tril(rng.standard_normal((d, d)), -1)
        dof = (n - 1) - np.arange(d)
        A[np.arange(d), np.arange(d)] = np.sqrt(rng.chisquare(dof))
        if mode == "ref":
            # reference design: idiosyncratic Wishart replaced by N*I (u_perp orthogonal, norm sqrt(N)), factor rows
            # orthogonal to everything else with norm sqrt(N); a := 0. Gram = v1v1' + Lam Lam' N + Psi N: the exact
            # one-dimensional (per-loading) structure of lemmas/X1.3 / Target 2 with xi, eta kept random.
            N = n - 1 - (1 + k)
            for m in range(k):
                A[1 + m, 1:] = 0.0
                A[1 + m, 1 + m] = math.sqrt(N)
            A[1 + k:, 1:] = 0.0
            A[1 + k + np.arange(p), 1 + k + np.arange(p)] = math.sqrt(N)
        self.A = A
        E, Fm, U = A[0], A[1:1 + k], A[1 + k:]
        Xc = Lam @ Fm + np.sqrt(psi)[:, None] * U          # p x d coordinates of centred raw columns
        beta = np.asarray(beta, float)
        yc = beta @ Xc + sigma * E
        Graw = Xc @ Xc.T
        sd = np.sqrt(np.diag(Graw) / (n - 1.0))
        self.sd = sd
        self.XtX = Graw / np.outer(sd, sd)
        Y2 = float(yc @ yc)
        s = math.sqrt(Y2 / (n - 1.0))
        self.Xty = (Xc @ yc) / sd / s
        self.yty = n - 1.0
        self.theta = sd * beta
        self.S0 = tuple(int(j) for j in np.flatnonzero(beta))
        self.xi = A[1 + k:, 0].copy()
        self.eta = A[1:1 + k, 0].copy()
        self.Lam, self.psi, self.sigma = Lam, psi, sigma
        self.nu = 0.01 + n / 2.0
        self.logw = log_prior_w(p, self.K)
        self.logm0 = -self.nu * math.log(0.02 + self.yty)
        self.cache = {(): self.logm0}


def _attach_problem_methods():
    import bvs_core as bc
    IidData.logm_idx = bc.Problem.logm_idx
    IidData.logm_many = bc.Problem.logm_many
    IidData.logm = bc.Problem.logm
    IidData.F = bc.Problem.F
    IidData.F_many = bc.Problem.F_many


try:
    _attach_problem_methods()
except Exception:  # bvs_core optional for the path code
    pass


class PathState:
    """Inverse quantities for the current set T and its complement O (all exact linear algebra)."""

    def __init__(self, P, T):
        self.P = P
        self.recompute(np.asarray(sorted(T), dtype=np.int64))

    def recompute(self, T):
        P = self.P
        n, p = P.n, P.p
        c1 = n + 1.0
        self.T = np.asarray(T, dtype=np.int64)
        inT = np.zeros(p, bool)
        inT[self.T] = True
        self.O = np.flatnonzero(~inT)
        k = len(self.T)
        G = P.XtX[np.ix_(self.T, self.T)]
        M1 = c1 * G + np.eye(k)
        M2 = G + np.eye(k)
        L1 = np.linalg.cholesky(M1)
        L2 = np.linalg.cholesky(M2)
        self.ld1 = 2 * np.log(np.diag(L1)).sum()
        self.ld2 = 2 * np.log(np.diag(L2)).sum()
        I = np.eye(k)
        Li1 = np.linalg.solve(L1, I)
        Li2 = np.linalg.solve(L2, I)
        self.W1 = Li1.T @ Li1
        self.W2 = Li2.T @ Li2
        zT = P.Xty[self.T]
        self.u = self.W1 @ zT
        self.quad = float(zT @ self.u)
        if len(self.O):
            GTO = P.XtX[np.ix_(self.T, self.O)]
            self.V1 = self.W1 @ (c1 * GTO)
            self.V2 = self.W2 @ GTO
            dO = np.diag(P.XtX)[self.O]
            self.s1 = (c1 * dO + 1.0) - (c1 * GTO * self.V1).sum(0)
            self.s2 = (dO + 1.0) - (GTO * self.V2).sum(0)
            self.bil = P.Xty[self.O] - (c1 * GTO).T @ self.u
        else:
            self.V1 = np.zeros((k, 0)); self.V2 = np.zeros((k, 0))
            self.s1 = np.zeros(0); self.s2 = np.zeros(0); self.bil = np.zeros(0)
        self.since = 0

    def delete(self, i):
        """delete the element at position i of T (exact rank-one downdate)."""
        T = self.T
        j = int(T[i])
        w1, w2 = self.W1[:, i].copy(), self.W2[:, i].copy()
        w1ii, w2ii = w1[i], w2[i]
        ui = self.u[i]
        keep = np.ones(len(T), bool); keep[i] = False
        # outside updates for old O
        V1i, V2i = self.V1[i].copy(), self.V2[i].copy()
        s1 = self.s1 + V1i ** 2 / w1ii
        s2 = self.s2 + V2i ** 2 / w2ii
        bil = self.bil + V1i * ui / w1ii
        V1 = self.V1[keep] - np.outer(w1[keep], V1i) / w1ii
        V2 = self.V2[keep] - np.outer(w2[keep], V2i) / w2ii
        # new outside column j
        v1j = -w1[keep] / w1ii
        v2j = -w2[keep] / w2ii
        self.ld1 += math.log(w1ii); self.ld2 += math.log(w2ii)
        self.quad -= ui ** 2 / w1ii
        self.u = self.u[keep] - w1[keep] * ui / w1ii
        self.W1 = self.W1[np.ix_(keep, keep)] - np.outer(w1[keep], w1[keep]) / w1ii
        self.W2 = self.W2[np.ix_(keep, keep)] - np.outer(w2[keep], w2[keep]) / w2ii
        self.T = T[keep]
        # insert j into O keeping O sorted
        pos = int(np.searchsorted(self.O, j))
        self.O = np.insert(self.O, pos, j)
        self.V1 = np.insert(V1, pos, v1j, axis=1)
        self.V2 = np.insert(V2, pos, v2j, axis=1)
        self.s1 = np.insert(s1, pos, 1.0 / w1ii)
        self.s2 = np.insert(s2, pos, 1.0 / w2ii)
        self.bil = np.insert(bil, pos, ui / w1ii)
        self.since += 1

    def gains(self, with_swaps=True):
        """exact gains F(nb) - F(T) of all deletions, additions, swaps (stable log1p forms)."""
        P = self.P
        n, K, nu, lw = P.n, P.K, P.nu, P.logw
        k = len(self.T)
        psi = 0.02 + P.yty - n * self.quad
        w1 = np.diag(self.W1).copy(); w2 = np.diag(self.W2).copy()
        dq_del = self.u ** 2 / w1                      # quad drop on deletion
        Gd = (lw[k - 1] - lw[k]) - 0.5 * (np.log(w1) - np.log(w2)) - nu * np.log1p(n * dq_del / psi) if k >= 1 else np.zeros(0)
        if len(self.O) and k < K:
            dq_add = self.bil ** 2 / self.s1
            Ga = (lw[k + 1] - lw[k]) - 0.5 * (np.log(self.s1) - np.log(self.s2)) - nu * np.log1p(-n * dq_add / psi)
        else:
            Ga = np.full(len(self.O), -np.inf)
        if with_swaps and len(self.O) and k >= 1:
            S1 = self.s1[None, :] + self.V1 ** 2 / w1[:, None]
            S2 = self.s2[None, :] + self.V2 ** 2 / w2[:, None]
            B = self.bil[None, :] + self.V1 * (self.u / w1)[:, None]
            dq = B ** 2 / S1 - dq_del[:, None]
            Gs = -0.5 * ((np.log(w1) - np.log(w2))[:, None] + np.log(S1) - np.log(S2)) - nu * np.log1p(-n * dq / psi)
        else:
            Gs = np.zeros((k, 0))
        return Gd, Ga, Gs, psi


def ls0_path(P, start, S0, max_moves=10 ** 6, refresh=200, diag_every=0, diag_fn=None):
    """uncapped production local search from `start`; best strict improvement; exact ties -> lexicographically
    smallest resulting set.  Returns dict(moves=[(type, j_out, l_in, gain)], final, ...)."""
    S0set = set(int(j) for j in S0)
    st = PathState(P, start)
    moves = []
    info = dict(max_add_gain=-np.inf, max_truth_move=-np.inf, max_swap_minus_del=-np.inf, min_del_gain=np.inf, ties=0)
    step = 0
    while True:
        Gd, Ga, Gs, psi = st.gains()
        T, O = st.T, st.O
        isN = np.array([int(t) not in S0set for t in T], bool)
        if len(Ga):
            info["max_add_gain"] = max(info["max_add_gain"], float(Ga.max()))
        tm = -np.inf
        if (~isN).any():
            tm = float(Gd[~isN].max())
            if Gs.size:
                tm = max(tm, float(Gs[~isN].max()))
        info["max_truth_move"] = max(info["max_truth_move"], tm)
        if isN.any() and Gs.size:
            info["max_swap_minus_del"] = max(info["max_swap_minus_del"], float(Gs[isN].max()) - float(Gd[isN].max()))
        if diag_fn is not None and diag_every and step % diag_every == 0:
            diag_fn(P, st, Gd, Ga, Gs, step)
        best = 0.0
        for arr in (Gd, Ga, Gs):
            if arr.size:
                best = max(best, float(arr.max()))
        if not best > 0.0:
            break
        cands = []
        cur = T.tolist()
        for i in np.flatnonzero(Gd == best):
            cands.append((tuple(v for v in cur if v != int(T[i])), ("del", int(i), None)))
        for l in np.flatnonzero(Ga == best):
            cands.append((tuple(sorted(cur + [int(O[l])])), ("add", None, int(l))))
        if Gs.size:
            for i, l in zip(*np.nonzero(Gs == best)):
                cands.append((tuple(sorted([v for v in cur if v != int(T[i])] + [int(O[l])])), ("swap", int(i), int(l))))
        if len(cands) > 1:
            info["ties"] += 1
        cands.sort(key=lambda c: c[0])
        newT, (typ, i, l) = cands[0]
        jo = int(T[i]) if i is not None else None
        li = int(O[l]) if l is not None else None
        tag = typ + ("T" if (jo in S0set or li in S0set) else "N")
        moves.append((tag, jo, li, best))
        if typ == "del":
            info["min_del_gain"] = min(info["min_del_gain"], best)
            st.delete(i)
            if st.since >= refresh and len(st.T):
                st.recompute(st.T)
        else:
            st.recompute(np.array(newT, dtype=np.int64))
        step += 1
        if len(moves) >= max_moves:
            break
    final = tuple(int(j) for j in st.T)
    return dict(moves=moves, final=final, final_is_S0=(set(final) == S0set), info=info)
