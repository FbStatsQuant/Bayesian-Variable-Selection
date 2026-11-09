"""bcs_core.py -- W2-FAC-S5 numerics: exact-Gram block compound symmetry (BCS), closed-form score and LS0 path.

Design (exact Gram, after column sign correction):  X'X = (n-1) Sigma,
    Sigma = rb 11' + (+)_g ( b J_{q_g} + d I_{q_g} ),   b = rw - rb > 0, d = 1 - rw > 0, groups G_g of bounded size.
    Study S5: rb = 0.3, rw = 0.7 (b = 0.4, d = 0.3), q = 5.
Noise: g := X'eps/(sigma sqrt(n-1)) ~ N(0, Sigma) represented as g_j = sqrt(rb) eta + sqrt(b) zeta_{g(j)} + sqrt(d) xi_j;
       ||e||^2 = sigma^2 (g' Sigma^-1 g + r), r ~ chi2_{n-1-p} independent.
Score (SoP 04_theory.tex:69-74; identical to W2-FAC-B fac_core.scan):
    F(T) = log w(|T|) - 1/2[logdet H_T - logdet(G_T + I)] - nu log(0.02 + Q_T),
    H_T = (n^2-1) Sigma_TT + I, G_T + I = (n-1) Sigma_TT + I, Q_T = (n-1) - n z_T' H_T^-1 z_T, nu = 0.01 + n/2.
Closed form: with a = n^2-1, alpha = a d + 1, bw = a b, bb = a rb, per group (u_g, B_g = sum z), phi_g = 1/(alpha + u_g bw),
    H_T = (+)(alpha I + bw J) + bb 11';  S = sum_g B_g phi_g,  W = sum_g u_g phi_g,
    v_j = (H_T^-1 z)_j = (z_j - bw phi_g B_g)/alpha - bb S phi_g/(1 + bb W),
    h_jj = (H_T^-1)_jj = (1 - bw phi_g)/alpha - bb phi_g^2/(1 + bb W),
    quad_T - quad_{T\\j} = v_j^2 / h_jj   (deletion; addition = deletion formula at T u l; swap = del then add).
logdet H_T = sum_{u_g>=1} [(u_g - 1) log alpha + log(alpha + u_g bw)] + log(1 + bb W)  (same with a' = n-1).
All gains are computed as exact increments (no differences of large F values).
"""
import math
import numpy as np
from scipy.special import gammaln


def log_prior_w(p, K):
    """capped BB(1,p): w(k) = 1/(2 C(2p-1, k)) on 0..K (normalisation irrelevant for differences)."""
    k = np.arange(K + 1)
    return -(gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k)) - math.log(2.0)


class BCS:
    def __init__(self, n, groups, rb, rw, theta, rng, sigma2=1.0, eta=None):
        """groups: int array of group labels (0..G-1) per variable; theta: standardised-scale coefficients."""
        self.n = n
        self.grp = np.asarray(groups, np.int64)
        p = len(self.grp)
        self.p = p
        self.G = int(self.grp.max()) + 1
        self.qg = np.bincount(self.grp, minlength=self.G)
        self.K = min(p, n // 2)
        self.rb, self.rw = rb, rw
        self.b, self.d = rw - rb, 1.0 - rw
        b, d = self.b, self.d
        sig = math.sqrt(sigma2)
        self.sigma2 = sigma2
        self.theta = np.asarray(theta, float)
        self.S0 = np.flatnonzero(self.theta != 0)
        # noise
        self.eta = rng.standard_normal() if eta is None else eta
        self.zeta = rng.standard_normal(self.G)
        self.xi = rng.standard_normal(p)
        h = math.sqrt(rb) * self.eta
        self.h = h
        self.gnoise = h + math.sqrt(b) * self.zeta[self.grp] + math.sqrt(d) * self.xi
        nm1 = n - 1.0
        self.r = rng.chisquare(n - 1 - p) if n - 1 - p > 0 else 0.0
        gSg = self.quad_sigma_inv(self.gnoise)
        Sth = self.sigma_mult(self.theta)
        mu2 = nm1 * float(self.theta @ Sth)
        cross = 2.0 * sig * math.sqrt(nm1) * float(self.theta @ self.gnoise)
        e2 = sigma2 * (gSg + self.r)
        self.s = math.sqrt((mu2 + cross + e2) / nm1)
        self.z = (nm1 * Sth + sig * math.sqrt(nm1) * self.gnoise) / self.s
        self.nu = 0.01 + n / 2.0
        self.logw = log_prior_w(p, self.K)
        a = n * n - 1.0
        a1 = nm1
        self.alpha, self.bw, self.bb = a * d + 1.0, a * b, a * rb
        self.alpha1, self.bw1, self.bb1 = a1 * d + 1.0, a1 * b, a1 * rb

    # Sigma algebra (full index set)
    def sigma_mult(self, x):
        gs = np.bincount(self.grp, weights=x, minlength=self.G)
        return self.rb * x.sum() + self.b * gs[self.grp] + self.d * x

    def quad_sigma_inv(self, x):
        """x' Sigma^-1 x via Sherman-Morrison on the block structure."""
        b, d, rb = self.b, self.d, self.rb
        q = self.qg
        Bx = np.bincount(self.grp, weights=x, minlength=self.G)
        Ax = np.bincount(self.grp, weights=x * x, minlength=self.G)
        ph = 1.0 / (d + q * b)
        quadM = ((Ax - b * ph * Bx * Bx) / d).sum()
        S = (Bx * ph).sum()
        W = (q * ph).sum()
        return float(quadM - rb * S * S / (1.0 + rb * W))

    # ------------------------------------------------------------------ state
    def state(self, inT):
        z = self.z
        u = np.bincount(self.grp[inT], minlength=self.G).astype(float)
        B = np.bincount(self.grp[inT], weights=z[inT], minlength=self.G)
        A = np.bincount(self.grp[inT], weights=z[inT] ** 2, minlength=self.G)
        return u, B, A

    def quad_logdet(self, u, B, A):
        al, bw, bb = self.alpha, self.bw, self.bb
        ph = 1.0 / (al + u * bw)
        S = (B * ph).sum()
        W = (u * ph).sum()
        quad = ((A - bw * ph * B * B) / al).sum() - bb * S * S / (1.0 + bb * W)
        m = u >= 1
        ld1 = ((u[m] - 1) * math.log(al) + np.log(al + u[m] * bw)).sum() + math.log1p(bb * W)
        al1, bw1, bb1 = self.alpha1, self.bw1, self.bb1
        ph1 = 1.0 / (al1 + u * bw1)
        W1 = (u * ph1).sum()
        ld2 = ((u[m] - 1) * math.log(al1) + np.log(al1 + u[m] * bw1)).sum() + math.log1p(bb1 * W1)
        return quad, ld1, ld2, S, W, W1

    def F(self, inT):
        u, B, A = self.state(inT)
        quad, ld1, ld2, *_ = self.quad_logdet(u, B, A)
        Q = (self.n - 1.0) - self.n * quad
        return self.logw[int(inT.sum())] - 0.5 * (ld1 - ld2) - self.nu * math.log(0.02 + Q)


class Path:
    """Closed-form scorer for the uncapped local search (flip + swap neighbourhood); the move selection (incl. the
    lexicographic tie rule) is implemented in the drivers s1_path.py / s3_cc.py.
    Swaps: exact values on a candidate set (all pairs if exhaustive=True; else top-J deletions x all outside,
    all outside x top-J... plus all same-group pairs)."""

    def __init__(self, P, start_mask):
        self.P = P
        self.inT = start_mask.copy()
        self.u, self.B, self.A = P.state(self.inT)
        self._refresh()

    def _refresh(self):
        P = self.P
        self.quad, self.ld1, self.ld2, self.S, self.W, self.W1 = P.quad_logdet(self.u, self.B, self.A)
        self.Q = (P.n - 1.0) - P.n * self.quad
        self.k = int(self.inT.sum())

    # generic: deletion increment of variables idx (in set described by u,B,S,W)
    def _del_inc(self, idx, u, B, S, W):
        P = self.P
        al, bw, bb = P.alpha, P.bw, P.bb
        g = P.grp[idx]
        ph = 1.0 / (al + u[g] * bw)
        v = (P.z[idx] - bw * ph * B[g]) / al - bb * S * ph / (1.0 + bb * W)
        hjj = (1.0 - bw * ph) / al - bb * ph * ph / (1.0 + bb * W)
        return v * v / hjj

    def _ld_change_del(self, gidx, u, W, W1):
        """change of (ld1 - ld2) when one variable of group g (current count u_g) is removed (vectorised over gidx)."""
        P = self.P
        ug = u[gidx]
        al, bw, bb = P.alpha, P.bw, P.bb
        al1, bw1, bb1 = P.alpha1, P.bw1, P.bb1
        def part(al, bw, bb, Wc):
            ph_old = ug / (al + ug * bw)
            ph_new = np.where(ug - 1 > 0, (ug - 1) / (al + (ug - 1) * bw), 0.0)
            Wn = Wc - ph_old + ph_new
            new_g = np.where(ug - 1 >= 1, (ug - 2) * math.log(al) + np.log(al + np.maximum(ug - 1, 0) * bw), 0.0)
            old_g = (ug - 1) * math.log(al) + np.log(al + ug * bw)
            return (new_g - old_g) + np.log1p(bb * Wn) - math.log1p(bb * Wc), Wn
        d1, Wn = part(al, bw, bb, W)
        d2, Wn1 = part(al1, bw1, bb1, W1)
        return d1 - d2, Wn

    def gains(self, swaps=True, J=12, exhaustive=False):
        P = self.P
        n, nu = P.n, P.nu
        inT = self.inT
        k = self.k
        Tidx = np.flatnonzero(inT)
        Oidx = np.flatnonzero(~inT)
        psi = 0.02 + self.Q
        res = {}
        # deletions
        if k >= 1:
            dq = self._del_inc(Tidx, self.u, self.B, self.S, self.W)
            dld, _ = self._ld_change_del(P.grp[Tidx], self.u, self.W, self.W1)
            gdel = (P.logw[k - 1] - P.logw[k]) - 0.5 * dld - nu * np.log1p(n * dq / psi)
        else:
            dq = np.array([]); gdel = np.array([])
        res["Tidx"], res["gdel"], res["dqdel"] = Tidx, gdel, dq
        # additions: deletion formula at T u l
        if len(Oidx) and k < P.K:
            gadd = self._add_gains(Oidx, self.u, self.B, self.S, self.W, self.W1, self.Q, k)
        else:
            gadd = np.full(len(Oidx), -np.inf)
        res["Oidx"], res["gadd"] = Oidx, gadd
        if swaps and k >= 1 and len(Oidx):
            res["swap"] = self._swaps(Tidx, Oidx, gdel, dq, gadd, J, exhaustive)
        else:
            res["swap"] = (-np.inf, None, None)
        return res

    def _add_gains(self, Oidx, u, B, S, W, W1, Q, k):
        P = self.P
        n, nu = P.n, P.nu
        al, bw, bb = P.alpha, P.bw, P.bb
        g = P.grp[Oidx]
        ug = u[g]
        ph_old = 1.0 / (al + ug * bw)
        ph_new = 1.0 / (al + (ug + 1) * bw)
        Sn = S - B[g] * ph_old + (B[g] + P.z[Oidx]) * ph_new
        Wn = W - ug * ph_old + (ug + 1) * ph_new
        Bn = B[g] + P.z[Oidx]
        v = (P.z[Oidx] - bw * ph_new * Bn) / al - bb * Sn * ph_new / (1.0 + bb * Wn)
        hll = (1.0 - bw * ph_new) / al - bb * ph_new * ph_new / (1.0 + bb * Wn)
        dq = v * v / hll
        # logdet change of adding = -(change of deleting from T u l)
        al1, bw1, bb1 = P.alpha1, P.bw1, P.bb1
        def part(al, bw, bb, Wc):
            Wn_ = Wc - ug / (al + ug * bw) + (ug + 1) / (al + (ug + 1) * bw)
            old_g = np.where(ug >= 1, (ug - 1) * math.log(al) + np.log(al + ug * bw), 0.0)
            new_g = ug * math.log(al) + np.log(al + (ug + 1) * bw)
            return (new_g - old_g) + np.log1p(bb * Wn_) - math.log1p(bb * Wc)
        dld = part(al, bw, bb, W) - part(al1, bw1, bb1, W1)
        psi = 0.02 + Q
        x = n * dq / psi
        with np.errstate(invalid="ignore", divide="ignore"):
            ga = (P.logw[k + 1] - P.logw[k]) - 0.5 * dld - nu * np.log1p(-x)
        ga = np.where(x < 1, ga, np.inf)
        return ga

    def swap_pairs(self, jarr, larr):
        """exact swap gains F(T minus j plus l) - F(T) for arrays of pairs (j in T, l not in T), vectorised."""
        P = self.P
        n, nu, k = P.n, P.nu, self.k
        al, bw, bb = P.alpha, P.bw, P.bb
        al1, bw1, bb1 = P.alpha1, P.bw1, P.bb1
        gj, gl = P.grp[jarr], P.grp[larr]
        zj, zl = P.z[jarr], P.z[larr]
        u0, B0 = self.u, self.B
        # deletion of j (exact increments as in gains())
        uj = u0[gj]
        ph_o = 1.0 / (al + uj * bw); ph_n = 1.0 / (al + (uj - 1) * bw)
        S1 = self.S - B0[gj] * ph_o + (B0[gj] - zj) * ph_n
        W1 = self.W - uj * ph_o + (uj - 1) * ph_n
        p1o = 1.0 / (al1 + uj * bw1); p1n = 1.0 / (al1 + (uj - 1) * bw1)
        W11 = self.W1 - uj * p1o + (uj - 1) * p1n
        v = (zj - bw * ph_o * B0[gj]) / al - bb * self.S * ph_o / (1.0 + bb * self.W)
        hjj = (1.0 - bw * ph_o) / al - bb * ph_o * ph_o / (1.0 + bb * self.W)
        dq_del = v * v / hjj
        psi = 0.02 + self.Q
        def ldg(al_, bw_, uu):
            return np.where(uu >= 1, (uu - 1) * math.log(al_) + np.log(al_ + np.maximum(uu, 0) * bw_), 0.0)
        dld_del = (ldg(al, bw, uj - 1) - ldg(al, bw, uj) + np.log1p(bb * W1) - math.log1p(bb * self.W))                 - (ldg(al1, bw1, uj - 1) - ldg(al1, bw1, uj) + np.log1p(bb1 * W11) - math.log1p(bb1 * self.W1))
        gdel = (P.logw[k - 1] - P.logw[k]) - 0.5 * dld_del - nu * np.log1p(n * dq_del / psi)
        Q1 = self.Q + n * dq_del
        # addition of l to T \ j
        same = gj == gl
        ul = np.where(same, uj - 1, u0[gl])
        Bl = np.where(same, B0[gj] - zj, B0[gl])
        po = 1.0 / (al + ul * bw); pn = 1.0 / (al + (ul + 1) * bw)
        Sn = S1 - Bl * po + (Bl + zl) * pn
        Wn = W1 - ul * po + (ul + 1) * pn
        Bn = Bl + zl
        v2 = (zl - bw * pn * Bn) / al - bb * Sn * pn / (1.0 + bb * Wn)
        h2 = (1.0 - bw * pn) / al - bb * pn * pn / (1.0 + bb * Wn)
        dq_add = v2 * v2 / h2
        p1o2 = 1.0 / (al1 + ul * bw1); p1n2 = 1.0 / (al1 + (ul + 1) * bw1)
        Wn1 = W11 - ul * p1o2 + (ul + 1) * p1n2
        dld_add = (ldg(al, bw, ul + 1) - ldg(al, bw, ul) + np.log1p(bb * Wn) - np.log1p(bb * W1))                 - (ldg(al1, bw1, ul + 1) - ldg(al1, bw1, ul) + np.log1p(bb1 * Wn1) - np.log1p(bb1 * W11))
        x = n * dq_add / (0.02 + Q1)
        with np.errstate(invalid="ignore", divide="ignore"):
            gadd = (P.logw[k] - P.logw[k - 1]) - 0.5 * dld_add - nu * np.log1p(-x)
        gadd = np.where(x < 1, gadd, np.inf)
        return gdel + gadd

    def _swaps(self, Tidx, Oidx, gdel, dqdel, gadd, J, exhaustive):
        """best swap value on a candidate set: (top-J deletions x all outside) u (all retained x top-J additions)
        u (all same-group pairs); exhaustive=True: all pairs."""
        P = self.P
        if exhaustive:
            jj, ll = np.meshgrid(Tidx, Oidx, indexing="ij")
            jarr, larr = jj.ravel(), ll.ravel()
        else:
            tj = Tidx[np.argsort(-gdel)[:J]]
            tl = Oidx[np.argsort(-gadd)[:J]]
            a1 = np.repeat(tj, len(Oidx)); b1 = np.tile(Oidx, len(tj))
            a2 = np.repeat(Tidx, len(tl)); b2 = np.tile(tl, len(Tidx))
            # same-group pairs
            order = np.argsort(P.grp[Oidx], kind="stable")
            Og = Oidx[order]; gO = P.grp[Og]
            starts = np.searchsorted(gO, P.grp[Tidx], "left"); ends = np.searchsorted(gO, P.grp[Tidx], "right")
            cnt = ends - starts
            a3 = np.repeat(Tidx, cnt)
            b3 = Og[np.concatenate([np.arange(s, e) for s, e in zip(starts, ends)])] if cnt.sum() else np.array([], np.int64)
            jarr = np.concatenate([a1, a2, a3]).astype(np.int64); larr = np.concatenate([b1, b2, b3]).astype(np.int64)
        if len(jarr) == 0:
            return (-np.inf, None, None)
        val = self.swap_pairs(jarr, larr)
        i = int(np.argmax(val))
        return (float(val[i]), int(jarr[i]), int(larr[i]))

    def apply(self, kind, j=None, l=None):
        P = self.P
        if kind in ("del", "swap"):
            g = P.grp[j]
            self.inT[j] = False
            self.u[g] -= 1; self.B[g] -= P.z[j]; self.A[g] -= P.z[j] ** 2
        if kind in ("add", "swap"):
            g = P.grp[l]
            self.inT[l] = True
            self.u[g] += 1; self.B[g] += P.z[l]; self.A[g] += P.z[l] ** 2
        self._refresh()

    # ---------------------------------------------------------- noise-space diagnostics (a = infinity)
    def noise_tau(self):
        """tau_l(T) for every variable: standardised residual of g_l given g_{T \\ l} under N(0, Sigma).
        Decomposition r_l = a_l(U) + c_u e_R (R = T \\ l, U = R n G_{g(l)}), returned with its parts."""
        P = self.P
        b, d, rb = P.b, P.d, P.rb
        g = P.gnoise
        inT = self.inT
        u = np.bincount(P.grp[inT], minlength=P.G).astype(float)
        sg = np.bincount(P.grp[inT], weights=g[inT], minlength=P.G)
        om = u / (u * b + d)
        gbar = np.where(u > 0, sg / np.maximum(u, 1), 0.0)
        num_all = (om * (gbar - P.h)).sum()
        den_all = 1.0 / rb + om.sum()
        p = P.p
        out = {}
        gl = P.grp
        # conditioning set for l: R = T \ l
        uR = u[gl] - inT.astype(float)
        sgR = sg[gl] - np.where(inT, g, 0.0)
        gbarR = np.where(uR > 0, sgR / np.maximum(uR, 1), 0.0)
        omR = uR / (uR * b + d)
        # remove group's contribution and add the R-version
        num = num_all - om[gl] * (gbar[gl] - P.h) + omR * (gbarR - P.h)
        den = den_all - om[gl] + omR
        eR = (P.h / rb - num) / den
        VR = 1.0 / den
        c = d / (uR * b + d)
        a_l = g - c * P.h - (1 - c) * gbarR
        s2 = d * (d + (uR + 1) * b) / (d + uR * b)
        tot = s2 + c * c * VR
        tau = (a_l + c * eR) / np.sqrt(tot)
        out.update(tau=tau, A=a_l / np.sqrt(s2), ce=c * eR / np.sqrt(tot), eR=eR, uR=uR)
        e_T = (P.h / rb - num_all) / den_all
        out["e_T"] = e_T
        return out


def s5_groups(p, q=5):
    return np.arange(p) // q


def layout(p, q, s0=4, c=1.0, spread=True):
    """truths in distinct groups spread over the index range (one per group), coefficients c*(1.4,-1,1.8,-1.2,...)."""
    PATTERN = (1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
    G = p // q
    th = np.zeros(p)
    gs = np.linspace(0, G - 1, s0 + 2)[1:-1].astype(int) if spread else np.arange(s0)
    for i, gg in enumerate(gs):
        th[gg * q + (i % q)] = c * PATTERN[i % 6]
    return th
