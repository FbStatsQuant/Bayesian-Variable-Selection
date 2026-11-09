"""mc_core.py -- W2-FAC-K2 numerics: exact-Gram MULTI-CLASS exchangeable designs, closed-form k-dimensional scans.

Design: classes c = 0..k-1 (array cls[j]), Sigma = Psi + E R E', Psi = diag(psi_{cls[j]}), psi_c = 1 - R_cc (unit
diagonal), E the p x k class indicator.  Requires Sigma PD (checked).
Score (SoP 04_theory.tex:69-74): log m(U) = -1/2[logdet H_U - logdet(G_U+I)] - nu log(0.02 + Q_U),
  G_U = (n-1) Sigma_UU, H_U = (n+1) G_U + I, Q_U = (n-1) - n z_U' H_U^-1 z_U, nu = 0.01 + n/2; F = log w(|S|) + log m.
Closed forms (push-through / matrix determinant lemma), for H_U = Psi'_U + E_U R' E_U' with psi'_c = (n^2-1)psi_c + 1,
R' = (n^2-1) R, and G_U + I = Psi''_U + E_U R'' E_U' with psi''_c = (n-1) psi_c + 1, R'' = (n-1) R:
  logdet H_U = sum_j log psi'_{c(j)} + logdet(I + R' N'_U),   N'_U = diag(u_c / psi'_c)
  z' H_U^-1 z = sum_j z_j^2/psi'_{c(j)} - w' R'(I + N' R')^-1 w,   w_c = sum_{j in U, class c} z_j / psi'_c.
So F(U) depends on U only through the class counts u_c, A = sum z_j^2/psi'_c and the k-vector w (k-dim reduction).
Scans: every deletion / addition exactly, vectorised per class; swaps exactly for the best pair per (class-out,
class-in) using convexity in z_l (max at an extreme z_l of the outside class), plus full swap matrix optionally.
Validated against fac_core.scan (general exact-Gram scorer) in mc_selftest.py.
Data (exact-Gram, model G, FAC-B L1.1): X'e = sigma sqrt(n-1) g, g ~ N(0, Sigma), g = E A eta + zeta, R = A A'
(eigen-decomposition; works for singular R), zeta_j ~ N(0, psi_c); ||e||^2 = sigma^2 (g' Sigma^-1 g + chi2_{n-1-p}).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import math
import numpy as np


def log_prior_w(p, K):
    """capped BB(1,p): w(k) = 1/(2 C(2p-1,k)) for k <= K (bvs_core.log_prior_w)."""
    from scipy.special import gammaln
    k = np.arange(K + 1)
    return -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


class MCDesign:
    def __init__(self, cls, R):
        self.cls = np.asarray(cls, dtype=np.int64)
        self.p = len(self.cls)
        self.R = np.asarray(R, float)
        self.k = self.R.shape[0]
        self.psi = 1.0 - np.diag(self.R)
        assert np.all(self.psi > 0), "need R_cc < 1"
        self.sizes = np.bincount(self.cls, minlength=self.k)
        # PD check of Sigma: eigenvalues of Psi^{-1/2} Sigma Psi^{-1/2} = I + D^{1/2}... use block form
        # Sigma PD  <=>  I_k + R N  has positive eigenvalues where N = diag(p_c/psi_c)  (and psi > 0)
        N = np.diag(self.sizes / self.psi)
        ev = np.linalg.eigvals(np.eye(self.k) + self.R @ N)
        assert np.all(ev.real > 1e-12), "Sigma not PD"
        w, V = np.linalg.eigh(self.R)
        w = np.clip(w, 0, None)
        self.A = V * np.sqrt(w)[None, :]          # R = A A'
        self.kappa_marg = self.psi / np.clip(np.diag(self.R), 1e-300, None)   # psi_c / rho_cc

    def Sigma(self):
        E = np.eye(self.k)[self.cls]
        return np.diag(self.psi[self.cls]) + E @ self.R @ E.T

    def kappa_eff(self, counts_other):
        """effective shrinkage constant kappa_c = psi_c * [Schur complement of (R^-1 + N_{-c}) at c], for every c,
        given the retained counts of the OTHER classes (vector of length k; own entry ignored)."""
        Rinv = np.linalg.inv(self.R)
        out = np.zeros(self.k)
        for c in range(self.k):
            Q = Rinv.copy()
            for d in range(self.k):
                if d != c:
                    Q[d, d] += counts_other[d] / self.psi[d]
            idx = [d for d in range(self.k) if d != c]
            if idx:
                S = Q[c, c] - Q[c, idx] @ np.linalg.solve(Q[np.ix_(idx, idx)], Q[idx, c])
            else:
                S = Q[c, c]
            out[c] = self.psi[c] * S
        return out


class MCData:
    """one exact-Gram data set on an MCDesign; sufficient statistics z = X'y, yty = n-1 (FAC-B L1.1 convention)."""

    def __init__(self, D, theta, n, rng, sigma2=1.0):
        self.D, self.n, self.p = D, n, D.p
        p, k = D.p, D.k
        assert p <= n - 1
        self.K = min(p, n // 2)
        self.theta = np.asarray(theta, float)
        sig = math.sqrt(sigma2)
        cls, psi = D.cls, D.psi
        self.eta = rng.standard_normal(k)
        self.xi = rng.standard_normal(p)                 # standardised idiosyncratic coordinates
        zeta = np.sqrt(psi[cls]) * self.xi
        common = (D.A @ self.eta)[cls]
        g = common + zeta
        self.g = g
        # g' Sigma^-1 g via push-through with Psi, R
        v = g / psi[cls]
        wv = np.bincount(cls, weights=v, minlength=k)
        Nn = np.diag(D.sizes / psi)
        M = D.R @ np.linalg.inv(np.eye(k) + Nn @ D.R)
        gSg = float(g @ v - wv @ M @ wv)
        chi = rng.chisquare(n - 1 - p) if n - 1 - p > 0 else 0.0
        self.chi = chi
        nm1 = n - 1.0
        # Sigma theta: psi_c theta_j + sum_d R_{c d} vartheta_d
        vth = np.bincount(cls, weights=self.theta, minlength=k)          # class truth sums
        Sth = psi[cls] * self.theta + (D.R @ vth)[cls]
        mu2 = nm1 * float(self.theta @ Sth)
        cross = 2.0 * sig * math.sqrt(nm1) * float(self.theta @ g)
        e2 = sigma2 * (gSg + chi)
        s = math.sqrt((mu2 + cross + e2) / nm1)
        self.s = s
        self.z = (nm1 * Sth + sig * math.sqrt(nm1) * g) / s
        self.yty = nm1
        self.nu = 0.01 + n / 2.0
        self.logw = log_prior_w(p, self.K)
        a = n * n - 1.0
        self.psi1 = a * psi + 1.0           # psi'
        self.R1 = a * D.R                  # R'
        self.psi2 = nm1 * psi + 1.0        # psi''
        self.R2 = nm1 * D.R                # R''
        self.lpsi1 = np.log(self.psi1)
        self.lpsi2 = np.log(self.psi2)
        self.zz1 = self.z ** 2 / self.psi1[cls]     # per-variable contribution to A
        self.zw1 = self.z / self.psi1[cls]          # per-variable contribution to w
        self.Ik = np.eye(k)

    # ------------------------------------------------------------------ core closed forms
    def _logdet_terms(self, counts):
        """returns (logdet H - logdet(G+I)) size-only part for class counts vector."""
        N1 = counts / self.psi1
        N2 = counts / self.psi2
        ld1 = float(counts @ self.lpsi1) + float(np.linalg.slogdet(self.Ik + self.R1 * N1[None, :])[1])
        ld2 = float(counts @ self.lpsi2) + float(np.linalg.slogdet(self.Ik + self.R2 * N2[None, :])[1])
        return ld1 - ld2

    def _M(self, counts):
        """M = R'(I + N' R')^-1 (k x k, symmetric) for class counts."""
        N1 = counts / self.psi1
        return self.R1 @ np.linalg.inv(self.Ik + N1[:, None] * self.R1)

    def F(self, U):
        U = np.asarray(sorted(U), dtype=np.int64)
        u = len(U)
        if u > self.K:
            return -np.inf
        counts = np.bincount(self.D.cls[U], minlength=self.D.k).astype(float)
        A = float(self.zz1[U].sum())
        w = np.bincount(self.D.cls[U], weights=self.zw1[U], minlength=self.D.k)
        quad = A - float(w @ self._M(counts) @ w)
        Q = self.yty - self.n * quad
        return float(self.logw[u] - 0.5 * self._logdet_terms(counts) - self.nu * math.log(0.02 + Q))

    # ------------------------------------------------------------------ centre and residuals (for diagnostics)
    def centre(self, T):
        """class-wise centre C_c(T) = (M w)_c in z-units and X_c in xi-units: for a null j in class c,
        z_j - C_c = kappa1 sqrt(psi_c) (xi_j - X_c(T))."""
        T = np.asarray(T, dtype=np.int64)
        cls = self.D.cls
        counts = np.bincount(cls[T], minlength=self.D.k).astype(float)
        w = np.bincount(cls[T], weights=self.zw1[T], minlength=self.D.k)
        C = self._M(counts) @ w
        nm1 = self.n - 1.0
        kappa1 = math.sqrt(nm1) / self.s
        vth = np.bincount(cls, weights=self.theta, minlength=self.D.k)
        common = nm1 * (self.D.R @ vth) / self.s + kappa1 * (self.D.A @ self.eta)   # class-common part of z (nulls)
        X = (C - common) / (kappa1 * np.sqrt(self.D.psi))
        return C, X

    # ------------------------------------------------------------------ scan
    def scan(self, T, full_swaps=False):
        """all flip neighbours exactly; swaps: best per (class out, class in) via convexity (exact for the maximum
        over l in each outside class), or the full matrix if full_swaps. Returns dict."""
        n, p, K, k = self.n, self.p, self.K, self.D.k
        cls = self.D.cls
        T = np.asarray(T, dtype=np.int64)
        kT = len(T)
        inT = np.zeros(p, bool)
        inT[T] = True
        O = np.flatnonzero(~inT)
        counts = np.bincount(cls[T], minlength=k).astype(float)
        A = float(self.zz1[T].sum()) if kT else 0.0
        w = np.bincount(cls[T], weights=self.zw1[T], minlength=k) if kT else np.zeros(k)
        nu, yty, lw = self.nu, self.yty, self.logw

        def Fof(ld, quad, size):
            return lw[size] - 0.5 * ld - nu * np.log(0.02 + yty - n * quad)

        ldT = self._logdet_terms(counts)
        MT = self._M(counts)
        quadT = A - float(w @ MT @ w)
        FT = float(Fof(ldT, quadT, kT))
        out = dict(T=tuple(int(t) for t in T), O=O, FT=FT, counts=counts)
        # deletions, per class
        Fdel = np.full(kT, -np.inf)
        if kT:
            for c in range(k):
                idx = np.flatnonzero(cls[T] == c)
                if len(idx) == 0:
                    continue
                cnt = counts.copy()
                cnt[c] -= 1
                ld = self._logdet_terms(cnt)
                M = self._M(cnt)
                zj = self.z[T[idx]]
                # w' = w - zj e_c / psi1_c ; quad' = A - zj^2/psi1_c - w'^T M w'
                a0 = float(w @ M @ w)
                Mw_c = float((M @ w)[c])
                Mcc = M[c, c]
                dj = zj / self.psi1[c]
                quad = A - self.zz1[T[idx]] - (a0 - 2 * dj * Mw_c + dj ** 2 * Mcc)
                Fdel[idx] = Fof(ld, quad, kT - 1)
        out["del"] = Fdel
        # additions, per class
        Fadd = np.full(len(O), -np.inf)
        if kT < K and len(O):
            for c in range(k):
                idx = np.flatnonzero(cls[O] == c)
                if len(idx) == 0:
                    continue
                cnt = counts.copy()
                cnt[c] += 1
                ld = self._logdet_terms(cnt)
                M = self._M(cnt)
                zl = self.z[O[idx]]
                a0 = float(w @ M @ w)
                Mw_c = float((M @ w)[c])
                Mcc = M[c, c]
                dl = zl / self.psi1[c]
                quad = A + self.zz1[O[idx]] - (a0 + 2 * dl * Mw_c + dl ** 2 * Mcc)
                Fadd[idx] = Fof(ld, quad, kT + 1)
        out["add"] = Fadd
        # swaps
        best_sw = -np.inf
        best_pair = None
        if kT and len(O):
            if full_swaps:
                SW = np.full((kT, len(O)), -np.inf)
            for c in range(k):
                idj = np.flatnonzero(cls[T] == c)
                if len(idj) == 0:
                    continue
                for d in range(k):
                    idl = np.flatnonzero(cls[O] == d)
                    if len(idl) == 0:
                        continue
                    cnt = counts.copy()
                    cnt[c] -= 1
                    cnt[d] += 1
                    ld = self._logdet_terms(cnt)
                    M = self._M(cnt)
                    zj = self.z[T[idj]]
                    zl = self.z[O[idl]]
                    dj = zj / self.psi1[c]
                    dl = zl / self.psi1[d]
                    a0 = float(w @ M @ w)
                    Mw = M @ w
                    # w' = w - dj e_c + dl e_d
                    # w'Mw' = a0 - 2 dj Mw_c + 2 dl Mw_d + dj^2 Mcc + dl^2 Mdd - 2 dj dl Mcd
                    if full_swaps:
                        q = (A - self.zz1[T[idj]][:, None] + self.zz1[O[idl]][None, :]
                             - (a0 - 2 * dj[:, None] * Mw[c] + 2 * dl[None, :] * Mw[d]
                                + dj[:, None] ** 2 * M[c, c] + dl[None, :] ** 2 * M[d, d]
                                - 2 * dj[:, None] * dl[None, :] * M[c, d]))
                        Fsw = Fof(ld, q, kT)
                        SW[np.ix_(idj, idl)] = Fsw
                        i, jj = np.unravel_index(np.argmax(Fsw), Fsw.shape)
                        if Fsw[i, jj] > best_sw:
                            best_sw = float(Fsw[i, jj]); best_pair = (int(T[idj[i]]), int(O[idl[jj]]))
                    else:
                        # convex in zl (coefficient 1/psi1_d - Mdd/psi1_d^2 > 0): candidates = extreme zl's
                        cand = [int(np.argmin(zl)), int(np.argmax(zl))]
                        for ii in cand:
                            q = (A - self.zz1[T[idj]] + self.zz1[O[idl[ii]]]
                                 - (a0 - 2 * dj * Mw[c] + 2 * dl[ii] * Mw[d]
                                    + dj ** 2 * M[c, c] + dl[ii] ** 2 * M[d, d] - 2 * dj * dl[ii] * M[c, d]))
                            Fsw = Fof(ld, q, kT)
                            i = int(np.argmax(Fsw))
                            if Fsw[i] > best_sw:
                                best_sw = float(Fsw[i]); best_pair = (int(T[idj[i]]), int(O[idl[ii]]))
            if full_swaps:
                out["swap"] = SW
        out["best_swap"] = best_sw
        out["best_swap_pair"] = best_pair
        return out


def best_move(sc, S0set):
    """production rule: best scanned neighbour, strict improvement; exact ties -> lexicographically smallest set."""
    T = list(sc["T"]); O = sc["O"]; FT = sc["FT"]
    add, dl = sc["add"], sc["del"]
    bsw = sc["best_swap"]
    best = max([-np.inf] + ([float(add.max())] if len(add) else []) + ([float(dl.max())] if len(dl) else []) + [bsw])
    isN = np.array([t not in S0set for t in T], bool)
    info = dict(FT=FT, best=best,
                best_add=(float(add.max()) - FT) if len(add) else -np.inf,
                best_del_N=(float(dl[isN].max()) - FT) if isN.any() else -np.inf,
                best_del_T=(float(dl[~isN].max()) - FT) if (~isN).any() else -np.inf,
                best_swap=bsw - FT if np.isfinite(bsw) else -np.inf)
    if not best > FT:
        return None, info
    cands = []
    if len(add):
        for i in np.flatnonzero(add == best):
            cands.append((tuple(sorted(T + [int(O[i])])), "+" + ("T" if int(O[i]) in S0set else "N")))
    for i in np.flatnonzero(dl == best):
        cands.append((tuple(t for t in T if t != T[i]), "-" + ("T" if T[i] in S0set else "N")))
    if bsw == best and sc["best_swap_pair"] is not None:
        j_out, l_in = sc["best_swap_pair"]
        cands.append((tuple(sorted([t for t in T if t != j_out] + [l_in])),
                      "sw" + ("T" if j_out in S0set else "N") + ">" + ("T" if l_in in S0set else "N")))
    cands.sort()
    info["n_ties"] = len(cands)
    return cands[0][0], dict(info, move=cands[0][1])


def ls0_path(P, centre, S0, max_moves=10 ** 7, record=None):
    """uncapped production local search from `centre`; records per step. S0 scored if it is a neighbour."""
    S0set = set(int(s) for s in S0)
    T = tuple(sorted(int(t) for t in centre))
    steps = []
    scored_S0 = (T == tuple(sorted(S0set)))
    while True:
        sc = P.scan(T)
        if not scored_S0:
            sd = set(T) ^ S0set
            if len(sd) == 1 or (len(sd) == 2 and len(set(T) - S0set) == 1 and len(S0set - set(T)) == 1):
                scored_S0 = True
        nxt, info = best_move(sc, S0set)
        info["size"] = len(T); info["extras"] = len(set(T) - S0set); info["missing"] = len(S0set - set(T))
        info["counts"] = sc["counts"].astype(int).tolist()
        if record is not None:
            record(P, T, sc, info)
        steps.append(info)
        if nxt is None or len(steps) > max_moves:
            break
        T = nxt
        if T == tuple(sorted(S0set)):
            scored_S0 = True
    return dict(final=T, steps=steps, moves=len(steps) - 1, scored_S0=scored_S0)
