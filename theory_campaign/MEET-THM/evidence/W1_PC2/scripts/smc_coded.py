"""PC2: forced-dispatch replica of the v3.1 final run on a genuinely correlated small design (p = 9), used to test
R1_C D14 (pathwise W in [e^-osc, e^osc], M_2 <= e^{D_*}), D1 (E[W H(h)] = pi(h), RB PIP identity, ratio bound),
D15-TV (empirical cell-TV bound), D15-KL (support obstruction).

Faithful to M §6.3–6.12 except: (1) the exact branch would fire at p = 9 (Sum C(p,k) <= (5H0+4N0)p), so SMC is
forced; (2) budgets are scaled down (N, H, R below); (3) the start is sampled from the enumerated pi0 table (same
law as the exact backward sampler).  Kept: coded partition, product start with exact normaliser, the coded pilot
rule (ESS 0.9, 60 halvings, floor 1/T_e) and the coded candidate-grid construction (v3_calib.h replica, incl.
snap and validation), the full random-order move round (p Gibbs, uniform swap, B neighbour swaps, independence),
multinomial resampling every stage, L burn-in + 4 measured rounds, Z-hat product formula, RB PIP records.
Seeds fixed; ~3-4 minutes.
"""
import math
import sys
import numpy as np
from bvs_common import (suff_from_data, method_sizes, coded_partition, d_table, card_Dstar, log_prior_w, all_models)

N_FINAL, H_PILOT, R_ISL, TE = 300, 300, 400, 1000


def lse(x):
    m = np.max(x)
    return m + math.log(np.exp(x - m).sum()) if np.isfinite(m) else m


# ---- v3_calib.h replicas ----
def pop_ess_frac(dv, delta):
    x = delta * dv
    return math.exp(2 * lse(x) - lse(2 * x)) / len(dv)


def pilot_next_phi(dv, phi, Te):
    if pop_ess_frac(dv, 1.0 - phi) >= 0.90:
        return 1.0, False
    lo, hi = phi, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if pop_ess_frac(dv, mid - phi) >= 0.90:
            lo = mid
        else:
            hi = mid
    if lo - phi < 1.0 / Te:
        f = min(1.0, phi + 1.0 / Te)
        if f >= 1.0 - 1e-12:
            f = 1.0
        return f, True
    return lo, False


def FV(lg0V, dV, t):
    return lse(lg0V + t * dV)


def rhoV(lg0V, dV, u, v):
    return math.exp(2 * FV(lg0V, dV, v) - FV(lg0V, dV, u) - FV(lg0V, dV, 2 * v - u))


def build_grid(lg0V, dV, targets, Te):
    targets = sorted(targets)
    grid = [0.0]
    u = 0.0
    while u < 1.0:
        b = next((t for t in targets if t > u), None)
        if b is None:
            return None, 'no_target'
        if rhoV(lg0V, dV, u, b) >= 0.90:
            v = b
        else:
            lo, hi, anyp = u, b, False
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if rhoV(lg0V, dV, u, mid) >= 0.90:
                    lo, anyp = mid, True
                else:
                    hi = mid
            if not anyp:
                return None, 'non_progress'
            v = lo
        if v >= 1.0 - 1e-12:
            v = 1.0
        if not v > u:
            return None, 'non_progress'
        if not rhoV(lg0V, dV, u, v) >= 0.90:
            return None, 'validation_failed'
        grid.append(v)
        if len(grid) - 1 > Te:
            return None, 'too_many'
        u = v
    return grid, 'ok'


class Sampler:
    def __init__(self, G, z, Y, n, seed_design=0):
        p = G.shape[0]
        self.p, self.n = p, n
        self.K, self.B = method_sizes(n, p)
        self.blocks = coded_partition(G, self.B)
        models, d, lbf = d_table(G, z, Y, n, self.blocks, self.K)
        lp = np.array([log_prior_w(p, len(S)) for S in models])
        self.models = models
        # bitmask tables over all 2^p subsets; infeasible = -inf
        P2 = 1 << p
        self.lg0 = np.full(P2, -np.inf)
        self.d = np.zeros(P2)
        self.size = np.array([bin(i).count('1') for i in range(P2)])
        self.idx_of = {}
        for S, dd, lb, l in zip(models, d, lbf, lp):
            i = sum(1 << j for j in S)
            self.lg0[i] = l + lb - dd
            self.d[i] = dd
            self.idx_of[S] = i
        feas = np.isfinite(self.lg0)
        self.feas = feas
        self.lpi0 = self.lg0 - lse(self.lg0[feas])
        self.lpi = self.lpi0 + np.where(feas, self.d, 0) - lse((self.lpi0 + self.d)[feas])
        self.pi0 = np.where(feas, np.exp(self.lpi0), 0.0)
        self.pi = np.where(feas, np.exp(self.lpi), 0.0)
        self.osc = float(d.max() - d.min())
        self.cs = card_Dstar(G, z, Y, n, self.blocks, self.K)
        # log Z relative: Z/(m(empty) Zbar0) = E_pi0 e^d
        self.logEd = lse((self.lpi0 + self.d)[feas])
        # neighbour graph (M §6.4)
        dg = np.sqrt(np.diag(G))
        Rm = G / np.outer(dg, dg)
        rn = math.sqrt(2 * math.log(p) / n)
        Nb = np.zeros((p, p), bool)
        for j in range(p):
            a = np.abs(Rm[j]).copy()
            a[j] = -1
            order = sorted([l for l in range(p) if l != j], key=lambda l: (-a[l], l))
            part = [l for l in order if a[l] > rn][:self.B]
            if order[0] not in part:
                part = [order[0]] + part[:self.B - 1]
            for l in part:
                Nb[j, l] = Nb[l, j] = True
        self.Nb = Nb
        self.m = p + self.B + 2
        self.pow2 = (1 << np.arange(p)).astype(np.int64)
        self.feas_idx = np.where(feas)[0]

    def draw_pi0(self, rng, N):
        i = rng.choice(self.feas_idx, size=N, p=self.pi0[self.feas_idx] / self.pi0[self.feas_idx].sum())
        return ((i[:, None] >> np.arange(self.p)) & 1).astype(bool)

    def idx(self, X):
        return X.astype(np.int64) @ self.pow2

    def lgam(self, I, phi):
        return self.lg0[I] + phi * self.d[I]

    def round(self, X, phi, rng, record=None):
        N, p, B = X.shape[0], self.p, self.B
        perms = np.argsort(rng.random((N, self.m)), axis=1)
        for s in range(self.m):
            st = perms[:, s]
            # Gibbs
            gmask = st < p
            if gmask.any():
                rows = np.where(gmask)[0]
                js = st[rows]
                Xon = X[rows].copy()
                Xon[np.arange(len(rows)), js] = True
                Xoff = X[rows].copy()
                Xoff[np.arange(len(rows)), js] = False
                lon = self.lgam(self.idx(Xon), phi)
                loff = self.lgam(self.idx(Xoff), phi)
                o = np.where(np.isfinite(lon), 1.0 / (1.0 + np.exp(np.clip(loff - lon, -700, 700))), 0.0)
                if record is not None:
                    np.add.at(record, js, o)
                newv = rng.random(len(rows)) < o
                X[rows, js] = newv
            # uniform swap
            rows = np.where(st == p)[0]
            if len(rows):
                Xr = X[rows]
                sz = Xr.sum(1)
                ok = (sz > 0) & (sz < p)
                rows, Xr = rows[ok], Xr[ok]
                if len(rows):
                    j = np.argmax(rng.random(Xr.shape) * Xr, axis=1)
                    l = np.argmax(rng.random(Xr.shape) * (~Xr), axis=1)
                    Xn = Xr.copy()
                    Xn[np.arange(len(rows)), j] = False
                    Xn[np.arange(len(rows)), l] = True
                    la = self.lgam(self.idx(Xn), phi) - self.lgam(self.idx(Xr), phi)
                    acc = np.log(rng.random(len(rows))) < la
                    X[rows[acc]] = Xn[acc]
            # neighbour swaps
            rows = np.where((st > p) & (st <= p + B))[0]
            if len(rows):
                Xr = X[rows]
                ok = Xr.sum(1) > 0
                rows, Xr = rows[ok], Xr[ok]
                if len(rows):
                    j = np.argmax(rng.random(Xr.shape) * Xr, axis=1)
                    cand = self.Nb[j] & ~Xr
                    nc = cand.sum(1)
                    ok2 = nc > 0
                    rows, Xr, j, cand, nc = rows[ok2], Xr[ok2], j[ok2], cand[ok2], nc[ok2]
                    if len(rows):
                        l = np.argmax(rng.random(Xr.shape) * cand, axis=1)
                        Xn = Xr.copy()
                        Xn[np.arange(len(rows)), j] = False
                        Xn[np.arange(len(rows)), l] = True
                        nrev = (self.Nb[l] & ~Xn).sum(1)
                        la = self.lgam(self.idx(Xn), phi) - self.lgam(self.idx(Xr), phi) + np.log(nc) - np.log(nrev)
                        acc = np.log(rng.random(len(rows))) < la
                        X[rows[acc]] = Xn[acc]
            # independence
            rows = np.where(st == p + B + 1)[0]
            if len(rows):
                Xp = self.draw_pi0(rng, len(rows))
                la = phi * (self.d[self.idx(Xp)] - self.d[self.idx(X[rows])])
                acc = np.log(rng.random(len(rows))) < la
                X[rows[acc]] = Xp[acc]
        return X

    def pilot_grid(self, rng, Vmode='top'):
        X = self.draw_pi0(rng, H_PILOT)
        phi, temps = 0.0, []
        while phi < 1.0:
            dv = self.d[self.idx(X)]
            nphi, forced = pilot_next_phi(dv, phi, TE)
            w = np.exp((nphi - phi) * (dv - dv.max()))
            X = X[rng.choice(len(w), size=len(w), p=w / w.sum())]
            X = self.round(X, nphi, rng)
            phi = nphi
            temps.append(phi)
        f = self.feas_idx
        if Vmode == 'top':
            k = 20 * self.p
            V = set(f[np.argsort(-self.lg0[f])[:k]]) | set(f[np.argsort(-(self.lg0 + self.d)[f])[:k]]) | {0}
        else:  # deliberately poor V: start-side top only
            V = set(f[np.argsort(-self.lg0[f])[:5]]) | {0}
        V = np.array(sorted(V))
        grid, why = build_grid(self.lg0[V], self.d[V], temps, TE)
        return grid, why, temps

    def final_island(self, grid, rng, n_burn):
        N = N_FINAL
        X = self.draw_pi0(rng, N)
        logW = 0.0
        for t in range(1, len(grid)):
            dl = grid[t] - grid[t - 1]
            dv = self.d[self.idx(X)]
            lw = dl * dv
            logW += lse(lw) - math.log(N)
            w = np.exp(lw - lw.max())
            X = X[rng.choice(N, size=N, p=w / w.sum())]
            X = self.round(X, grid[t], rng)
        for _ in range(n_burn):
            X = self.round(X, 1.0, rng)
        rec = np.zeros(self.p)
        counts = np.zeros(len(self.lpi))
        for _ in range(4):
            X = self.round(X, 1.0, rng, record=rec)
            np.add.at(counts, self.idx(X), 1)
        return logW - self.logEd, rec / (4 * N), counts / (4 * N)


def design(seed):
    rng = np.random.default_rng(seed)
    p, n = 9, 400
    S = np.eye(p)
    gid = np.arange(p) // 3
    for i in range(p):
        for j in range(i + 1, p):
            S[i, j] = S[j, i] = 0.5 if gid[i] == gid[j] else rng.choice([-1, 1]) * rng.uniform(0.03, 0.08)
    L = np.linalg.cholesky(S)
    X = rng.standard_normal((n, p)) @ L.T
    theta = np.zeros(p)
    theta[[0, 3, 6]] = [0.25, -0.2, 0.15]
    y = X @ theta + rng.standard_normal(n)
    return suff_from_data(X, y)


def design_mask(seed, s=0.35):
    """Masked linked-hub-like design: groups of 3 (within 0.6), hub link corr 0.4 between vars 0 and 3,
    theta_0 = s, theta_3 = -0.4 s (zero marginal covariance of x_3), other cross-block corr +-[0.02,0.05]."""
    rng = np.random.default_rng(seed)
    p, n = 9, 400
    S = np.eye(p)
    gid = np.arange(p) // 3
    for i in range(p):
        for j in range(i + 1, p):
            S[i, j] = S[j, i] = 0.6 if gid[i] == gid[j] else rng.choice([-1, 1]) * rng.uniform(0.02, 0.05)
    S[0, 3] = S[3, 0] = 0.4
    L = np.linalg.cholesky(S)
    X = rng.standard_normal((n, p)) @ L.T
    theta = np.zeros(p)
    theta[[0, 3]] = [s, -0.4 * s]
    y = X @ theta + rng.standard_normal(n)
    return suff_from_data(X, y)


def main():
    G, z, Y, n = design(7) if (len(sys.argv) < 2 or sys.argv[1] != 'mask') else design_mask(5)
    sm = Sampler(G, z, Y, n)
    p = sm.p
    dg = np.sqrt(np.diag(G))
    Rm = G / np.outer(dg, dg)
    cross = [abs(Rm[i, j]) for i in range(p) for j in range(i + 1, p) if i // 3 != j // 3]
    print(f"design p={p} n={n} K={sm.K} B={sm.B} blocks={sm.blocks}; |cross-block corr| in [{min(cross):.3f},{max(cross):.3f}]")
    print(f"osc d = {sm.osc:.4f}; card D_* = {sm.cs['Dstar']:.4f} (a={sm.cs['a']:.3g}, dA={sm.cs['dA']:.3g}, dH={sm.cs['dH']:.3g})")
    L = max(4, math.ceil(math.log2(n + 1)))
    PIP = np.array([sum(sm.pi[i] for i in range(len(sm.pi)) if (i >> j) & 1) for j in range(p)])
    sizes = sm.size
    for Vmode in ('top', 'poor'):
        rng = np.random.default_rng(11 if Vmode == 'top' else 12)
        grid, why, temps = sm.pilot_grid(rng, Vmode)
        print(f"\n[V={Vmode}] pilot stages {len(temps)}, grid status {why}, grid stages {len(grid) - 1 if grid else None}")
        if grid is None:
            continue
        lw, rbs, ems = [], [], []
        for r in range(R_ISL):
            l, rb, em = sm.final_island(grid, rng, L)
            lw.append(l)
            rbs.append(rb)
            ems.append(em)
        lw = np.array(lw)
        W = np.exp(lw)
        rbs = np.array(rbs)
        ems = np.array(ems)
        print(f"  W range [{W.min():.4f}, {W.max():.4f}] vs [e^-osc, e^osc] = [{math.exp(-sm.osc):.4f}, {math.exp(sm.osc):.4f}];"
              f" pathwise violations: {int(((lw > sm.osc + 1e-9) | (lw < -sm.osc - 1e-9)).sum())}")
        print(f"  mean W = {W.mean():.4f} (se {W.std() / math.sqrt(len(W)):.4f}); mean W^2 = {(W ** 2).mean():.4f}"
              f" <= e^osc = {math.exp(sm.osc):.4f}, e^D* = {math.exp(sm.cs['Dstar']):.4g}")
        # D1 identities: E[W * H(h)] = pi(h)
        h_size2 = (sizes == 2).astype(float)
        pair = np.array([1.0 if (i & 1) and (i >> 3) & 1 else 0.0 for i in range(len(sm.pi))])
        for name, h in (('size=2', h_size2), ('pair{0,3}', pair)):
            Hr = ems @ h
            est = (W * Hr).mean()
            se = (W * Hr).std() / math.sqrt(len(W))
            print(f"  D1 E[W H({name})] = {est:.4f} (se {se:.4f}) vs pi(h) = {float(sm.pi @ h):.4f}")
        estrb = (W[:, None] * rbs).mean(0)
        se_rb = (W[:, None] * rbs).std(0) / math.sqrt(len(W))
        zs = (estrb - PIP) / np.maximum(se_rb, 1e-12)
        print(f"  D1 RB PIP: max |E[W PIP_rb] - PIP|/se = {np.abs(zs).max():.2f} over {p} coords")
        # D1 ratio bound and D15-TV cell bound at R = 4 (groups of 4 islands)
        M2 = (W ** 2).mean()
        Rg = 4
        grpW = W[: (len(W) // Rg) * Rg].reshape(-1, Rg)
        grpE = ems[: (len(W) // Rg) * Rg].reshape(-1, Rg, ems.shape[1])
        grpRB = rbs[: (len(W) // Rg) * Rg].reshape(-1, Rg, p)
        for eps in (0.05, 0.1, 0.2):
            muhat = (grpW[:, :, None] * grpRB).sum(1) / grpW.sum(1)[:, None]
            fr = (np.abs(muhat[:, 0] - PIP[0]) > eps).mean()
            bnd = min(1, 4 * (M2 - 1) / Rg + 4 * M2 / (Rg * eps ** 2))
            pihat = (grpW[:, :, None] * grpE).sum(1) / grpW.sum(1)[:, None]
            # size cells, d0 = K+1
            cells = np.array([[pihat[g][sizes == k].sum() for k in range(sm.K + 1)] for g in range(len(pihat))])
            pic = np.array([sm.pi[sizes == k].sum() for k in range(sm.K + 1)])
            tv = 0.5 * np.abs(cells - pic).sum(1)
            ftv = (tv > eps).mean()
            btv = min(1, 4 * (M2 - 1) / Rg + 4 * (sm.K + 1) * M2 / (Rg * eps ** 2))
            print(f"  eps={eps}: P(|PIPhat_0 - PIP_0|>eps) = {fr:.3f} <= D1 bound {bnd:.3f};"
                  f" P(size-cell TV>eps) = {ftv:.3f} <= D15 bound {btv:.3f}")
        # D15-KL support obstruction: |Omega| vs 4NR atoms and missing support
        Omega = int(sm.feas.sum())
        miss = int(((ems.sum(0) == 0) & sm.feas).sum())
        print(f"  |Omega|={Omega}, 4*N*R={4 * N_FINAL * R_ISL}; states never in any endpoint record: {miss}")


if __name__ == '__main__':
    main()
