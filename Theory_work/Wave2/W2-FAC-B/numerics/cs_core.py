"""cs_core.py -- exact-Gram compound symmetry (Sigma = (1-rho) I + rho J): closed-form score of every set and an
O(p)-per-scan LS0 path, from the 1-D reduction of lemmas/L1_cs_reduction.md.

For U with |U| = u, A_U = sum_U z_j^2, B_U = sum_U z_j (z = X'y):
  alpha = (n^2-1)(1-rho)+1, beta = (n^2-1) rho, alpha' = (n-1)(1-rho)+1, beta' = (n-1) rho,
  logdet H_U = (u-1) log alpha + log(alpha + u beta);  logdet(G_U+I) = (u-1) log alpha' + log(alpha' + u beta'),
  quad_U = (A_U - gamma_u B_U^2)/alpha,  gamma_u = beta/(alpha + u beta),   Q_U = (n-1) - n quad_U,
  F(U) = log w(u) - 0.5[logdet H_U - logdet(G_U+I)] - nu log(0.02 + Q_U).
Data (exact Gram): g = sqrt(rho) eta 1 + sqrt(1-rho) xi, xi ~ N(0,I_p), eta ~ N(0,1);
  z = [(n-1) Sigma theta + sigma sqrt(n-1) g]/s.
"""
import math
import numpy as np
from scipy.special import gammaln


def log_w(p, K):
    k = np.arange(K + 1)
    return -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


class CS:
    def __init__(self, rho, theta, n, sigma2=1.0, rng=None, xi=None, eta=None, chi=None):
        p = len(theta)
        assert p <= n - 1
        self.rho, self.n, self.p = rho, n, p
        self.K = min(p, n // 2)
        self.theta = np.asarray(theta, float)
        self.S0 = tuple(int(j) for j in np.flatnonzero(self.theta))
        sig = math.sqrt(sigma2)
        if xi is None:
            xi = rng.standard_normal(p)
        if eta is None:
            eta = float(rng.standard_normal())
        if chi is None:
            chi = float(rng.chisquare(n - 1 - p)) if n - 1 - p > 0 else 0.0
        self.xi, self.eta, self.chi = np.asarray(xi, float), eta, chi
        g = math.sqrt(rho) * eta + math.sqrt(1 - rho) * self.xi
        S = self.theta.sum()
        Sth = (1 - rho) * self.theta + rho * S          # Sigma theta
        # g' Sigma^-1 g: Sigma^-1 = [I - rho/(1-rho+p rho) J]/(1-rho)
        gSg = (g @ g - rho / (1 - rho + p * rho) * g.sum() ** 2) / (1 - rho)
        nm1 = n - 1.0
        mu2 = nm1 * float(self.theta @ Sth)
        cross = 2 * sig * math.sqrt(nm1) * float(self.theta @ g)
        e2 = sigma2 * (gSg + chi)
        self.s = math.sqrt((mu2 + cross + e2) / nm1)
        self.z = (nm1 * Sth + sig * math.sqrt(nm1) * g) / self.s
        a = n * n - 1.0
        self.al, self.be = a * (1 - rho) + 1.0, a * rho
        self.al2, self.be2 = nm1 * (1 - rho) + 1.0, nm1 * rho
        self.nu = 0.01 + n / 2.0
        self.lw = log_w(p, self.K)

    def F_stats(self, u, A, B):
        """vectorised F from (u, A, B) (arrays broadcast)."""
        u = np.asarray(u)
        al, be, al2, be2, n = self.al, self.be, self.al2, self.be2, self.n
        um = np.maximum(u, 1)
        ldH = np.where(u > 0, (um - 1) * math.log(al) + np.log(al + um * be), 0.0)
        ldG = np.where(u > 0, (um - 1) * math.log(al2) + np.log(al2 + um * be2), 0.0)
        gam = be / (al + u * be)
        quad = np.where(u > 0, (A - gam * B ** 2) / al, 0.0)
        Q = (n - 1.0) - n * quad
        return self.lw[u] - 0.5 * (ldH - ldG) - self.nu * np.log(0.02 + Q)

    def F(self, T):
        T = list(T)
        zz = self.z[T]
        return float(self.F_stats(len(T), float(zz @ zz), float(zz.sum())))

    def xi_center(self, k, B):
        """centre x_T in xi-units: argmin over z of the deletion criterion is z* = gamma_k B; return (z*-k0)/k1."""
        return None


def ls0_path_cs(P, max_moves=10 ** 7, record_every=0):
    """uncapped production local search from [p] (the start mode on the full-start event), exact F, O(p)/scan.
    Exact float ties -> lexicographically smallest set (only resolved when they occur; reported)."""
    n, p, K = P.n, P.p, P.K
    z = P.z
    S0 = set(P.S0)
    inT = np.ones(p, bool)
    k = p
    A = float(z @ z)
    B = float(z.sum())
    moves = []
    info = dict(max_add_gain=-np.inf, max_swap_minus_del=-np.inf, min_del_gain=np.inf, ties=0, max_truth_move=-np.inf,
                max_add_gain_over_logn=-np.inf)
    rows = []
    while True:
        FT = float(P.F_stats(k, A, B))
        idx_in = np.flatnonzero(inT)
        idx_out = np.flatnonzero(~inT)
        zin, zout = z[idx_in], z[idx_out]
        cands = []  # (F, type, j_out, l_in)
        # deletions
        Fd = P.F_stats(np.full(len(idx_in), k - 1), A - zin ** 2, B - zin) if k >= 1 else np.array([])
        # additions
        Fa = P.F_stats(np.full(len(idx_out), k + 1), A + zout ** 2, B + zout) if (k < K and len(idx_out)) else np.array([])
        # swaps: for each j in T, best l in O is at an extreme of t_l (convex) -> check min and max z_out
        if len(idx_out):
            ext = np.unique([int(np.argmin(zout)), int(np.argmax(zout))])
            zl = zout[ext]
            Fs = P.F_stats(np.full((len(idx_in), len(ext)), k), (A - zin ** 2)[:, None] + zl[None, :] ** 2,
                           (B - zin)[:, None] + zl[None, :])
        else:
            Fs = np.zeros((len(idx_in), 0))
        best = max([FT] + ([float(Fd.max())] if len(Fd) else []) + ([float(Fa.max())] if len(Fa) else []) +
                   ([float(Fs.max())] if Fs.size else []))
        isN_in = np.array([j not in S0 for j in idx_in])
        # diagnostics
        if len(Fa):
            g = float(Fa.max()) - FT
            info["max_add_gain"] = max(info["max_add_gain"], g)
            info["max_add_gain_over_logn"] = max(info["max_add_gain_over_logn"], g / math.log(n))
        if (~isN_in).any():
            tm = float(Fd[~isN_in].max()) - FT
            if Fs.size:
                tm = max(tm, float(Fs[~isN_in].max()) - FT)
            info["max_truth_move"] = max(info["max_truth_move"], tm)
        if isN_in.any() and Fs.size:
            info["max_swap_minus_del"] = max(info["max_swap_minus_del"], float(Fs[isN_in].max()) - float(Fd[isN_in].max()))
        if not best > FT:
            break
        # identify move (ties -> lexicographically smallest resulting set; count ties)
        opts = []
        for i in np.flatnonzero(Fd == best):
            opts.append(("-", int(idx_in[i]), None))
        for i in np.flatnonzero(Fa == best) if len(Fa) else []:
            opts.append(("+", None, int(idx_out[i])))
        if Fs.size:
            for i, e in zip(*np.nonzero(Fs == best)):
                opts.append(("s", int(idx_in[i]), int(idx_out[ext[e]])))
        if len(opts) > 1:
            info["ties"] += 1
        cur = idx_in.tolist()
        def _res(o):
            t, jo_, li_ = o
            st = [v for v in cur if v != jo_] if jo_ is not None else list(cur)
            if li_ is not None: st = sorted(st + [li_])
            return tuple(st)
        opts.sort(key=_res)   # production rule: lexicographically smallest resulting set
        typ, jo, li = opts[0]
        if typ == "-":
            info["min_del_gain"] = min(info["min_del_gain"], best - FT)
        if jo is not None:
            inT[jo] = False; k -= 1; A -= z[jo] ** 2; B -= z[jo]
        if li is not None:
            inT[li] = True; k += 1; A += z[li] ** 2; B += z[li]
        tag = typ + ("T" if (jo in S0 or li in S0) else "N")
        moves.append((tag, jo, li))
        if len(moves) >= max_moves:
            break
    final = tuple(int(j) for j in np.flatnonzero(inT))
    return dict(moves=moves, final=final, final_is_S0=(set(final) == S0), info=info)
