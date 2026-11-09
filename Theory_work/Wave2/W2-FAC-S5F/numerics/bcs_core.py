"""bcs_core.py -- W2-FAC-S5F numerics: exact-Gram BLOCK compound symmetry (study S5 type) at large n.

Design: Sigma = a*11' + b*H + c*I,  H = indicator of groups of size q (grp(j) = j // q), a + b + c = 1.
        S5: a = 0.3, b = 0.4, c = 0.3, q = 5.   Plain CS: b = 0 (or q = 1).  Pure block design: a = 0.
Exact Gram (fixed design, centred X, X'X = (n-1) Sigma, p <= n-1), model G: X'e = sigma sqrt(n-1) g, g ~ N(0, Sigma),
        g = sqrt(a) eta 1 + sqrt(b) zeta_{grp} + sqrt(c) xi   (eta ~ N(0,1), zeta ~ N(0,I_J), xi ~ N(0,I_p)),
        ||e||^2 = sigma^2 (g' Sigma^-1 g + chi2_{n-1-p}),  y = (mu + e)/s,  s^2 = ||mu+e||^2/(n-1),  z = X'y,  y'y = n-1.
Score (SoP 04_theory.tex:69-74): log m(T) = -1/2[logdet H_T - logdet(G_T+I)] - nu log(0.02 + Q_T),
        H_T = (n^2-1) Sigma_TT + I = (n^2-1) M(c1),  G_T + I = (n-1) M(c2),  c1 = c + 1/(n^2-1),  c2 = c + 1/(n-1),
        M(c') := a J + b H + c' I restricted to T;  Q_T = (n-1) - n z_T' H_T^-1 z_T;  nu = 0.01 + n/2;
        F(T) = log w(|T|) + log m(T),  w(k) = 1/(2 C(2p-1,k)) (K = min(p, n//2)).
Closed form for M = aJ + bH + c'I on T with group counts u_G, sums S_G = sum z, P_G = sum z^2:
        w_G = 1/(c' + b u_G),  W = sum_G u_G w_G,  B = sum_G w_G S_G,
        M^-1 = D - a w~ w~'/(1 + aW),  D = c'^-1 (I - sum_G b w_G J_G),  w~ = D 1 (= w_G on group G),
        z' M^-1 z = [sum_G P_G - sum_G b w_G S_G^2]/c' - a B^2/(1 + aW),
        logdet M = sum_{G: u_G>=1} [(u_G - 1) log c' + log(c' + b u_G)] + log(1 + aW).
Every neighbour gain is computed DIFFERENTIALLY (Schur complements: residual^2 / conditional variance, log1p), so no
cancellation of O(nu log Q) ~ n log n quantities occurs; valid for any n representable in float64 (n up to 1e12 used).
LS0 move rule = production rule (best strictly improving flip/swap neighbour; exact ties -> lexicographically smallest
set; measure-zero here).  Verified against FAC-B's general exact-Gram scorer (fac_core.scan) in bcs_selftest.py.
"""
import math
import numpy as np
from scipy.special import gammaln


def log_prior_w(p, K):
    """log w(k) = -log 2 - log C(2p-1, k), k = 0..K (SoP 02_method: capped BB(1,p))."""
    k = np.arange(K + 1)
    return -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


class BCS:
    def __init__(self, p, q, a, b, c, theta, n, rng, sigma2=1.0):
        assert abs(a + b + c - 1) < 1e-12 and p <= n - 1
        self.p, self.q, self.a, self.b, self.c, self.n = p, q, a, b, c, n
        self.grp = np.arange(p) // q
        self.J = int(self.grp.max()) + 1
        self.K = min(p, n // 2)
        self.nu = 0.01 + n / 2.0
        self.c1 = c + 1.0 / (n * n - 1.0)
        self.c2 = c + 1.0 / (n - 1.0)
        self.theta = np.asarray(theta, float)
        self.S0 = tuple(int(i) for i in np.flatnonzero(self.theta))
        sig = math.sqrt(sigma2)
        # noise representation
        self.eta = float(rng.standard_normal())
        self.zeta = rng.standard_normal(self.J)
        self.xi = rng.standard_normal(p)
        g = math.sqrt(a) * self.eta + math.sqrt(b) * self.zeta[self.grp] + math.sqrt(c) * self.xi
        self.g = g
        # g' Sigma^-1 g via the closed form (full set, c' = c)
        gSg = self._quad_full(g, c)
        chi = rng.chisquare(n - 1 - p) if n - 1 - p > 0 else 0.0
        self.chi = chi
        nm1 = n - 1.0
        Sth = self.Sigma_times(self.theta)
        mu2 = nm1 * float(self.theta @ Sth)
        cross = 2.0 * sig * math.sqrt(nm1) * float(self.theta @ g)
        e2 = sigma2 * (gSg + chi)
        self.s = math.sqrt((mu2 + cross + e2) / nm1)
        self.z = (nm1 * Sth + sig * math.sqrt(nm1) * g) / self.s
        self.logw = log_prior_w(p, self.K)
        self.yty = nm1

    # ------------------------------------------------------------------------------------------ design algebra
    def Sigma_times(self, v):
        gs = np.bincount(self.grp, weights=v, minlength=self.J)
        return self.a * v.sum() + self.b * gs[self.grp] + self.c * v

    def _quad_full(self, v, cp):
        u = np.bincount(self.grp, minlength=self.J).astype(float)
        S = np.bincount(self.grp, weights=v, minlength=self.J)
        P = float(v @ v)
        w = 1.0 / (cp + self.b * u)
        W = float(u @ w)
        B = float(S @ w)
        return (P - self.b * float(w @ S ** 2)) / cp - self.a * B * B / (1.0 + self.a * W)

    # ------------------------------------------------------------------------------------------ aggregates
    def aggregates(self, T):
        T = np.asarray(T, dtype=np.int64)
        u = np.bincount(self.grp[T], minlength=self.J).astype(float)
        S = np.bincount(self.grp[T], weights=self.z[T], minlength=self.J)
        P = np.bincount(self.grp[T], weights=self.z[T] ** 2, minlength=self.J)
        return u, S, P

    def _parts(self, u, S, P, cp):
        w = 1.0 / (cp + self.b * u)
        W = float(u @ w)
        B = float(S @ w)
        quad = (P.sum() - self.b * float(w @ S ** 2)) / cp - self.a * B * B / (1.0 + self.a * W)
        hit = u >= 1
        ld = float(((u[hit] - 1.0) * math.log(cp) + np.log(cp + self.b * u[hit])).sum()) + math.log(1.0 + self.a * W)
        return w, W, B, quad, ld

    def F(self, T):
        T = tuple(sorted(int(t) for t in T))
        k = len(T)
        if k == 0:
            return self.logw[0] - self.nu * math.log(0.02 + self.yty)
        u, S, P = self.aggregates(T)
        _, _, _, q1, ld1 = self._parts(u, S, P, self.c1)
        _, _, _, _, ld2 = self._parts(u, S, P, self.c2)
        n = self.n
        Q = self.yty - n * q1 / (n * n - 1.0)
        return self.logw[k] - 0.5 * (k * math.log(n + 1.0) + ld1 - ld2) - self.nu * math.log(0.02 + Q)

    # ------------------------------------------------------------------------------------------ scan (gains)
    def scan(self, T, want_swaps=True):
        """Gains F(neighbour) - F(T) for all deletions (array over T), additions (array over O), swaps (|T| x |O|).
        Also returns the standardized statistics Z^2 (residual^2 / cond. variance in M(c1) units, times (n-1)/s^2-free
        scaling: Zsq_del[j] = v_j^2 / m_jj etc.), and the per-step threshold pieces."""
        n, p, K, a, b = self.n, self.p, self.K, self.a, self.b
        T = np.asarray(sorted(T), dtype=np.int64)
        k = len(T)
        inT = np.zeros(p, bool)
        inT[T] = True
        O = np.flatnonzero(~inT)
        z = self.z
        u, S, P = self.aggregates(T)
        c1, c2 = self.c1, self.c2
        w1, W1, B1, q1, ld1 = self._parts(u, S, P, c1)
        w2, W2, B2, q2, ld2 = self._parts(u, S, P, c2)
        Q = self.yty - n * q1 / (n * n - 1.0)
        psi = 0.02 + Q
        out = dict(T=tuple(int(t) for t in T), O=O, k=k, Q=Q, u=u.copy())
        lw = self.logw
        gT = self.grp[T]
        gO = self.grp[O]
        f1 = 1.0 + a * W1
        f2 = 1.0 + a * W2

        def lik_gain(dquad1):
            # F change from the likelihood term, given quad(T') - quad(T) in M(c1) units
            dQ = -n * dquad1 / (n * n - 1.0)
            return -self.nu * np.log1p(dQ / psi)

        # ---- deletions ----
        if k >= 1:
            wj1 = w1[gT]
            uj = u[gT]
            v1 = (z[T] - b * S[gT] * wj1) / c1 - a * wj1 * B1 / f1
            m1 = (c1 + b * (uj - 1.0)) / (c1 * (c1 + b * uj)) - a * wj1 ** 2 / f1  # (M^-1)_jj = D_jj - a w_G^2/(1+aW)
            dquad_del = -v1 ** 2 / m1
            Zsq_del = v1 ** 2 / m1  # in M(c1) units (quad units)
            # log det changes (group term + global term), for c1 and c2

            def dld_del(cp, w, W):
                grp_term = -(math.log(cp) + np.log((cp + b * uj) / (cp + b * (uj - 1.0))))
                Wp = W - uj * w[gT] + (uj - 1.0) / (cp + b * (uj - 1.0))
                glob = np.log1p(a * Wp) - math.log1p(a * W)
                return grp_term + glob

            d1 = dld_del(c1, w1, W1)
            d2 = dld_del(c2, w2, W2)
            size_term = lw[k - 1] - lw[k] + 0.5 * math.log(n + 1.0)
            out["del"] = size_term - 0.5 * (d1 - d2) + lik_gain(dquad_del)
            out["del_size"] = size_term - 0.5 * (d1 - d2)
            out["Zsq_del"] = Zsq_del
            out["del_lik"] = lik_gain(dquad_del)
        else:
            out["del"] = np.array([])
            out["Zsq_del"] = np.array([])

        # ---- additions ----
        if len(O) and k < K:
            wl1 = w1[gO]
            pred1 = b * wl1 * S[gO] + a * B1 * c1 * wl1 / f1
            var1 = c1 * (1.0 + b * wl1) + a * c1 ** 2 * wl1 ** 2 / f1
            r1 = z[O] - pred1
            dquad_add = r1 ** 2 / var1
            ul = u[gO]

            def dld_add(cp, w, W):
                grp_term = math.log(cp) + np.log((cp + b * (ul + 1.0)) / (cp + b * ul))
                Wp = W - ul * w[gO] + (ul + 1.0) / (cp + b * (ul + 1.0))
                glob = np.log1p(a * Wp) - math.log1p(a * W)
                return grp_term + glob

            d1 = dld_add(c1, w1, W1)
            d2 = dld_add(c2, w2, W2)
            size_term = lw[k + 1] - lw[k] - 0.5 * math.log(n + 1.0)
            out["add"] = size_term - 0.5 * (d1 - d2) + lik_gain(dquad_add)
            out["add_size"] = size_term - 0.5 * (d1 - d2)
            out["Zsq_add"] = dquad_add
        else:
            out["add"] = np.array([]) if len(O) == 0 else np.full(len(O), -np.inf)
            out["Zsq_add"] = np.array([])

        # ---- swaps: j out (rows), l in (cols) ----
        if want_swaps and k >= 1 and len(O):
            uj = u[gT]
            # aggregates of T \ j (only group of j changes); scalars per j
            wj1_new = 1.0 / (c1 + b * (uj - 1.0))
            Sj_new = S[gT] - z[T]
            W1j = W1 - uj * w1[gT] + (uj - 1.0) * wj1_new
            B1j = B1 - w1[gT] * S[gT] + wj1_new * Sj_new
            f1j = 1.0 + a * W1j
            # for each (j,l): group of l aggregates in T\j
            same = (gT[:, None] == gO[None, :])
            ul_j = u[gO][None, :] - same  # u of l's group after removing j
            Sl_j = S[gO][None, :] - same * z[T][:, None]
            wl_j = 1.0 / (c1 + b * ul_j)
            pred = b * wl_j * Sl_j + a * B1j[:, None] * c1 * wl_j / f1j[:, None]
            var = c1 * (1.0 + b * wl_j) + a * c1 ** 2 * wl_j ** 2 / f1j[:, None]
            r = z[O][None, :] - pred
            dquad_sw = out["del"].size and (-(out["Zsq_del"])[:, None] + r ** 2 / var)
            # log det: deletion part (per j) + addition part w.r.t. T\j (per j,l) for c1 and c2

            def dld_sw(cp, w, W):
                wjn = 1.0 / (cp + b * (uj - 1.0))
                Wj = W - uj * w[gT] + (uj - 1.0) * wjn
                grp_del = -(math.log(cp) + np.log((cp + b * uj) / (cp + b * (uj - 1.0))))
                grp_add = math.log(cp) + np.log((cp + b * (ul_j + 1.0)) / (cp + b * ul_j))
                Wjl = Wj[:, None] - ul_j / (cp + b * ul_j) + (ul_j + 1.0) / (cp + b * (ul_j + 1.0))
                glob = np.log1p(a * Wjl) - math.log1p(a * W)
                return grp_del[:, None] + grp_add + glob

            d1 = dld_sw(c1, w1, W1)
            d2 = dld_sw(c2, w2, W2)
            out["swap"] = -0.5 * (d1 - d2) + lik_gain(dquad_sw)
        else:
            out["swap"] = np.zeros((k, len(O)))
        return out


def best_move(sc, S0set):
    """Production rule on the scanned neighbours. Returns (newT or None, info)."""
    T = list(sc["T"])
    O = sc["O"]
    add, dl, sw = sc["add"], sc["del"], sc["swap"]
    best = -np.inf
    for arr in (add, dl, sw):
        if arr is not None and np.size(arr):
            best = max(best, float(np.max(arr)))
    Tarr = np.array(T, dtype=np.int64)
    isN = np.array([t not in S0set for t in T], bool) if len(T) else np.zeros(0, bool)
    info = dict(best=best, best_add=float(np.max(add)) if np.size(add) else -np.inf,
                best_del_N=float(dl[isN].max()) if len(dl) and isN.any() else -np.inf,
                best_del_T=float(dl[~isN].max()) if len(dl) and (~isN).any() else -np.inf,
                best_swap=float(sw.max()) if sw.size else -np.inf)
    if sw.size and isN.any():
        info["best_swap_N"] = float(sw[isN].max())
    if not best > 0.0:
        return None, info
    cands = []
    if np.size(add):
        for i in np.flatnonzero(add == best):
            cands.append((tuple(sorted(T + [int(O[i])])), "+" + ("T" if int(O[i]) in S0set else "N")))
    for i in np.flatnonzero(dl == best):
        cands.append((tuple(t for t in T if t != T[i]), "-" + ("T" if T[i] in S0set else "N"), int(T[i])))
    if sw.size:
        for i, j in zip(*np.nonzero(sw == best)):
            j_out, l_in = T[i], int(O[j])
            ns = tuple(sorted([t for t in T if t != j_out] + [l_in]))
            cands.append((ns, "sw" + ("T" if j_out in S0set else "N") + ">" + ("T" if l_in in S0set else "N"), j_out, l_in))
    cands.sort(key=lambda c: c[0])
    info["n_ties"] = len(cands)
    info["move"] = cands[0][1]
    if len(cands[0]) >= 3:
        info["j"] = cands[0][2]
    if len(cands[0]) >= 4:
        info["l"] = cands[0][3]
    return cands[0][0], info


def ls0_path(P, centre, max_moves=10 ** 7, record=None, want_swaps=True):
    """Uncapped production local search from `centre`. record(P, T, sc, info) is called at every visited set."""
    S0set = set(P.S0)
    T = tuple(sorted(int(t) for t in centre))
    steps = []
    while True:
        sc = P.scan(T, want_swaps=want_swaps)
        nxt, info = best_move(sc, S0set)
        info["k"] = len(T)
        info["extras"] = len(set(T) - S0set)
        info["missing"] = len(S0set - set(T))
        if record is not None:
            record(P, T, sc, info)
        steps.append(info)
        if nxt is None or len(steps) > max_moves:
            break
        T = nxt
    return dict(final=T, steps=steps, moves=len(steps) - 1, final_is_S0=(T == tuple(sorted(P.S0))))


def study_layout(p, c=1.0, s0=4, step=5):
    """C-GROW diagnostic layout (as FAC-B fac_core.study_layout): truths 2,26,53,75 for s0=4; coefficients
    c*(1.4,-1,1.8,-1.2,...)."""
    POS = (3, 2, 4, 1, 5, 3)
    PATTERN = (1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
    k = np.arange(s0)
    block = 1 + step * k
    pos = np.array([POS[i % 6] for i in k])
    act = 5 * (block - 1) + pos - 1
    th = np.zeros(p)
    th[act] = c * np.array([PATTERN[i % 6] for i in k])
    return th
