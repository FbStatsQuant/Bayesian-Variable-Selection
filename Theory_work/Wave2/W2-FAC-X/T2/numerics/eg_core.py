"""eg_core.py -- W2-FAC-X Target 2: EXACT-GRAM one-factor designs, closed-form LS0 path (lemmas: T2/L4r_path.md, L4r.0).

Design: X'X = (n-1) Sigma, Sigma = lam lam' + diag(psi), psi = 1 - lam^2 (Upsilon = I).  Data (FACB L1.1, general):
  g = lam*eta + sqrt(psi)*xi,  eta ~ N(0,1), xi ~ N(0,I_p), r ~ chi2_{n-1-p};  ||e||^2 = sigma^2 (g' Sigma^-1 g + r);
  (n-1) s^2 = (n-1) th' Sigma th + 2 sigma sqrt(n-1) th' g + ||e||^2;  z = [(n-1) Sigma th + sigma sqrt(n-1) g]/s.
Score: F(U) = log w(|U|) - 1/2 [logdet((n+1)G_U + I) - logdet(G_U + I)] - nu log(0.02 + Q_U),
  Q_U = (n-1) - n z_U' H_U^-1 z_U, H_U = (n+1) G_U + I, nu = n/2 + 0.01.

Closed form (L4r.0): with a = n^2 - 1, d_i^2 = a psi_i + 1, eps_i^2 = a psi_i/(a psi_i + 1), l'_i = eps_i l_i
(l_i = lam_i/sqrt(psi_i)), zc_i = eps_i (xi_i + sqrt(n-1) sqrt(psi_i) th_i / sigma), rho0 = eta + sqrt(n-1) lam'th/sigma:
  X_U = (sum_U l'_i zc_i - rho0)/(1 + |l'_U|^2)      (any U; exact drift identity)
  quad_U - quad_{U\\j} = (1 + g'_j(U)) k1^2 (zc_j - l'_j X_U)^2,  g'_j(U) = l'_j^2/(1 + |l'_U|^2 - l'_j^2),  k1^2 = sigma^2/(s^2 (n+1))
  L_U = sum_U log(d_i^2/d''_i^2) + log((1+|l'_U|^2)/(1+|l''_U|^2)),  d''^2 = (n-1)psi+1, l''^2 = (n-1)lam^2/d''^2.
The path code works with these formulas only (no matrices); eg_selftest.py checks them against direct linear algebra
and against the general production-path code iid_core.ls0_path.
"""
import math
import numpy as np
from scipy.special import gammaln


def log_prior_w(p, K):
    k = np.arange(K + 1)
    return -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


class EGData:
    def __init__(self, lam, theta, n, rng, sigma=1.0):
        lam = np.asarray(lam, float); theta = np.asarray(theta, float)
        p = len(lam)
        self.n, self.p, self.sigma = n, p, sigma
        self.K = min(p, n // 2)
        self.lam, self.theta = lam, theta
        self.psi = 1.0 - lam ** 2
        self.ell = lam / np.sqrt(self.psi)
        self.S0 = np.flatnonzero(theta)
        self.isT = theta != 0
        self.eta = float(rng.standard_normal())
        self.xi = rng.standard_normal(p)
        self.r = float(rng.chisquare(n - 1 - p))
        g = lam * self.eta + np.sqrt(self.psi) * self.xi
        gt = g / np.sqrt(self.psi)
        gSg = float(gt @ gt - (self.ell @ gt) ** 2 / (1 + self.ell @ self.ell))
        self.e2 = sigma ** 2 * (gSg + self.r)
        Sth = lam * (lam @ theta) + self.psi * theta
        thSth = float(theta @ Sth)
        s2 = (thSth * (n - 1) + 2 * sigma * math.sqrt(n - 1) * float(theta @ g) + self.e2) / (n - 1)
        self.s = math.sqrt(s2)
        self.z = ((n - 1) * Sth + sigma * math.sqrt(n - 1) * g) / self.s
        self.g = g
        self.nu = n / 2.0 + 0.01
        self.logw = log_prior_w(p, self.K)
        a = float(n) ** 2 - 1.0
        self.a = a
        self.d2 = a * self.psi + 1.0
        self.eps2 = a * self.psi / self.d2
        self.lp = np.sqrt(self.eps2) * self.ell            # l'
        self.zc = np.sqrt(self.eps2) * (self.xi + math.sqrt(n - 1) * np.sqrt(self.psi) * theta / sigma)
        self.rho0 = self.eta + math.sqrt(n - 1) * float(lam @ theta) / sigma
        self.k1sq = sigma ** 2 / (s2 * (n + 1.0))
        self.dd2 = (n - 1.0) * self.psi + 1.0
        self.lpp2 = (n - 1.0) * lam ** 2 / self.dd2         # l''^2
        self.logdr = np.log(self.d2) - np.log(self.dd2)      # log(d^2/d''^2)
        # T-independent reduced offset for T >= S0 (L4r.0(a)):  X_T = (sum_{K} l' zeta - varrho)/D'_T
        S0 = self.S0
        self.varrho = (self.eta - float((self.eps2[S0] * self.ell[S0] * self.xi[S0]).sum())
                       + math.sqrt(n - 1) / sigma * float(((1 - self.eps2[S0]) * lam[S0] * theta[S0]).sum()))

    # ---------------- direct (matrix) score, for self-tests only ----------------
    def F_direct(self, U):
        U = np.asarray(sorted(U), int); n = self.n
        if len(U) == 0:
            return self.logw[0] - self.nu * math.log(0.02 + (n - 1))
        Sig = np.outer(self.lam[U], self.lam[U]) + np.diag(self.psi[U])
        G = (n - 1) * Sig
        H = (n + 1) * G + np.eye(len(U))
        zU = self.z[U]
        quad = float(zU @ np.linalg.solve(H, zU))
        Q = (n - 1) - n * quad
        L = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(len(U)))[1]
        return self.logw[len(U)] - 0.5 * L - self.nu * math.log(0.02 + Q)

    def quad_closed(self, U):
        U = np.asarray(sorted(U), int)
        zt = self.z[U] / np.sqrt(self.d2[U]); lp = self.lp[U]
        return float(zt @ zt - (lp @ zt) ** 2 / (1 + lp @ lp))

    def L_closed(self, U):
        U = np.asarray(sorted(U), int)
        return float(self.logdr[U].sum() + math.log1p(self.lp[U] @ self.lp[U]) - math.log1p(self.lpp2[U].sum()))

    def F_closed(self, U):
        n = self.n
        Q = (n - 1) - n * self.quad_closed(U)
        return self.logw[len(U)] - 0.5 * self.L_closed(U) - self.nu * math.log(0.02 + Q)


def classes_of(lam):
    vals, cls = np.unique(lam, return_inverse=True)
    return vals, cls


def eg_path(P, start, max_moves=10 ** 7, record=True, Hbar=None):
    """Uncapped production local search (best strict improvement; exact-tie -> lexicographically smallest set) from
    `start`, using only the closed forms.  Requires finitely many loading values (swap maximisation per class).
    Returns dict(moves, final_is_S0, info, steps) where steps holds per-step diagnostics."""
    n, p, nu = P.n, P.p, P.nu
    lw = P.logw; K = P.K
    vals, cls = classes_of(P.lam)
    r = len(vals)
    inT = np.zeros(p, bool); inT[list(start)] = True
    S0set = set(int(j) for j in P.S0)
    # Q_T at start: direct closed form
    T = np.flatnonzero(inT)
    Q = (n - 1) - n * P.quad_closed(T)
    moves = []; steps = []
    info = dict(max_add=-np.inf, max_truth=-np.inf, max_swap_minus_del=-np.inf, min_best_del=np.inf, ties=0,
                crossings=0, interval_viol=0, max_centre_ratio=0.0, max_centre_ratio_end=0.0)
    if Hbar is None:
        Hbar = float(np.abs(P.xi[~P.isT]).max())
    ell_c = vals / np.sqrt(1 - vals ** 2)
    while True:
        T = np.flatnonzero(inT); O = np.flatnonzero(~inT)
        k = len(T)
        psiT = 0.02 + Q
        lpT = P.lp[T]
        Dp = 1.0 + float(lpT @ lpT)
        Dpp = 1.0 + float(P.lpp2[T].sum())
        X = (float(lpT @ P.zc[T]) - P.rho0) / Dp
        # ---- deletions
        tau = P.zc[T] - P.lp[T] * X
        gp = P.lp[T] ** 2 / (Dp - P.lp[T] ** 2)
        dQd = n * (1 + gp) * P.k1sq * tau ** 2
        dL = P.logdr[T] + np.log(Dp) - np.log(Dp - P.lp[T] ** 2) - np.log(Dpp) + np.log(Dpp - P.lpp2[T])  # L_T - L_{T\j}
        Gd = (lw[k - 1] - lw[k]) + 0.5 * dL - nu * np.log1p(dQd / psiT) if k >= 1 else np.zeros(0)
        # ---- additions
        if len(O) and k < K:
            tl = P.zc[O] - P.lp[O] * X
            dQa = n * (1 - P.lp[O] ** 2 / (Dp + P.lp[O] ** 2)) * P.k1sq * tl ** 2
            dLa = P.logdr[O] + np.log(Dp + P.lp[O] ** 2) - np.log(Dp) - np.log(Dpp + P.lpp2[O]) + np.log(Dpp)  # L_{T+l}-L_T
            Ga = (lw[k + 1] - lw[k]) - 0.5 * dLa - nu * np.log1p(-dQa / psiT)
        else:
            Ga = np.full(len(O), -np.inf)
        # ---- swaps: for each j in T, best l per class = outside extreme of zc within class
        Gs_best = np.full(k, -np.inf); Gs_arg = np.full(k, -1)
        if len(O) and k >= 1:
            Xj = X - P.lp[T] * tau / (Dp - P.lp[T] ** 2)           # X_{T\j}
            Dpj = Dp - P.lp[T] ** 2; Dppj = Dpp - P.lpp2[T]
            Qj = Q + dQd                                            # Q_{T\j}
            for c in range(r):
                Oc = O[cls[O] == c]
                if len(Oc) == 0:
                    continue
                cand = [Oc[np.argmin(P.zc[Oc])], Oc[np.argmax(P.zc[Oc])]]
                # truths outside (cannot happen when T >= S0, but keep exact)
                for l in set(int(x) for x in cand):
                    tl = P.zc[l] - P.lp[l] * Xj
                    dq = n * (1 - P.lp[l] ** 2 / (Dpj + P.lp[l] ** 2)) * P.k1sq * tl ** 2
                    Qn = Qj - dq
                    Lsw = (P.logdr[l] + np.log(Dpj + P.lp[l] ** 2) - np.log(Dpj) - np.log(Dppj + P.lpp2[l])
                           + np.log(Dppj)) - dL                    # L_{T'} - L_T
                    g = -0.5 * Lsw - nu * np.log((0.02 + Qn) / psiT)
                    better = g > Gs_best
                    Gs_best = np.where(better, g, Gs_best); Gs_arg = np.where(better, l, Gs_arg)
        isN = ~P.isT[T]
        if len(Ga):
            info["max_add"] = max(info["max_add"], float(Ga.max()))
        if (~isN).any():
            info["max_truth"] = max(info["max_truth"], float(Gd[~isN].max()), float(Gs_best[~isN].max()))
        if isN.any():
            bd = float(Gd[isN].max())
            info["max_swap_minus_del"] = max(info["max_swap_minus_del"], float(Gs_best[isN].max()) - bd)
            info["min_best_del"] = min(info["min_best_del"], bd)
        # ---- diagnostics: per-class interval holes, centres
        m = int(isN.sum())
        cr = float(np.max(np.abs(ell_c * X))) / Hbar
        info["max_centre_ratio"] = max(info["max_centre_ratio"], cr)
        if record:
            nulls_all = np.flatnonzero(~P.isT)
            viol = 0
            dmax = 0.0; onesided = 0
            for c in range(r):
                Nc = nulls_all[cls[nulls_all] == c]
                kept = inT[Nc]
                if kept.all() or (~kept).all():
                    continue
                order = np.argsort(P.xi[Nc]); kd = kept[order]
                dele = np.flatnonzero(~kd)
                contiguous = (dele[-1] - dele[0] + 1) == len(dele)
                cen = ell_c[c] * X
                xs = P.xi[Nc][order]
                lo = xs[dele[0] - 1] if dele[0] > 0 else -np.inf
                hi = xs[dele[-1] + 1] if dele[-1] + 1 < len(xs) else np.inf
                if not (contiguous and lo < cen < hi):
                    viol += 1
                if np.isfinite(lo) and np.isfinite(hi):
                    dmax = max(dmax, abs((hi - cen) - (cen - lo)) / (2 * ell_c[c]) / Hbar)
                else:
                    onesided += 1
            if m >= 30:
                info["bulk_delta_over_l"] = max(info.get("bulk_delta_over_l", 0.0), dmax)
                info["bulk_absX"] = max(info.get("bulk_absX", 0.0), abs(X) / Hbar)
                info["bulk_onesided_steps"] = info.get("bulk_onesided_steps", 0) + (onesided > 0)
            if viol:
                info["interval_viol"] += 1
            Kn = T[isN]
            J = float((P.ell[Kn] * P.xi[Kn]).sum()) / Hbar
            steps.append((k, m, X, cr, viol, J, Dp))
        # ---- choose best move
        best = 0.0
        for arr in (Gd, Ga, Gs_best):
            if arr.size:
                best = max(best, float(arr.max()))
        if not best > 0.0:
            break
        cands = []
        cur = T.tolist()
        for i in np.flatnonzero(Gd == best):
            cands.append((tuple(v for v in cur if v != int(T[i])), ("del", int(T[i]), None)))
        for i in np.flatnonzero(Ga == best):
            cands.append((tuple(sorted(cur + [int(O[i])])), ("add", None, int(O[i]))))
        for i in np.flatnonzero(Gs_best == best):
            cands.append((tuple(sorted([v for v in cur if v != int(T[i])] + [int(Gs_arg[i])])), ("swap", int(T[i]), int(Gs_arg[i]))))
        if len(cands) > 1:
            info["ties"] += 1
        cands.sort(key=lambda c: c[0])
        _, (typ, jo, li) = cands[0]
        tag = typ + ("T" if (jo in S0set or li in S0set) else "N")
        if typ == "del":
            i = int(np.flatnonzero(T == jo)[0]); Q = Q + float(dQd[i]); inT[jo] = False
        elif typ == "add":
            i = int(np.flatnonzero(O == li)[0]); Q = Q - float(dQa[i]); inT[li] = True
        else:
            inT[jo] = False; inT[li] = True
            T2 = np.flatnonzero(inT); Q = (n - 1) - n * P.quad_closed(T2)
        cl = int(cls[jo]) if jo is not None else int(cls[li])
        moves.append((tag, jo, li, best, cl))
        if len(moves) >= max_moves:
            break
    final = set(int(j) for j in np.flatnonzero(inT))
    return dict(moves=moves, final_is_S0=(final == S0set), info=info, steps=steps, Hbar=Hbar)
