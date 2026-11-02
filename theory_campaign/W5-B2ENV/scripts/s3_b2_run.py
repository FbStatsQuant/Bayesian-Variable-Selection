"""W5-B2ENV s3: route (b2) on LH (Theorem B2-LH) -- faithful small-p final runs with exact scores.  Seed 20261102.

Designs: W1-EXP configurations A (STAB-LH holds, m_STAB = 0.305) and A85 (STAB-LH fails, m_swap = -0.005); c = 1, p = 16.
Grid: bvs_core.method_grid() (idealised calibration).  One island = N = max(2500, n) iid pi0 draws, frozen grid, multinomial
resampling, one round per stage (stage-T round at phi = 1), then L + 4 terminal rounds.
Measured per island:
  * confinement: number of (stage-end, particle) pairs outside N = {S ⊇ S°, nu(S) <= 19} for stage ends 0..T-1 (here nu <= 10
    always, so only truth loss can exit), and the stage of the first exit;
  * repair: fraction of particles whose stage-T round (phi = 1) scores S0, and whether some particle does;
  * envelope for the lattice potential h = 1_{S°,S0} (pre-switch) / 1_{S0} (post-switch at the first grid point >= phi*,
    phi* = the crossing temperature of the exact two-state lattice odds): realised kappa_t over visited states,
    Gamma = sum Delta_t kappa_t, and min_t log P_t (realised D4 envelope with eta = 0);
  * Gamma for h = 1_N (should be 0 on the confinement event).
Also: one-round scoring probability at phi = 1 from S° and from the worst-looking states of N (MC, 20000 rounds) vs c0(x).
"""
import sys, time
from math import ceil, log, comb
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from bvs_core import BVS, lse, popcount
from lh_family import lh_sigma, lh_truth, suff_exact_gram

out = []
pr = lambda s: (out.append(s), print(s, flush=True))


def one_round_hits(m, S, phi, rng, target):
    """bvs_core.one_round with per-particle recording of whether `target` was evaluated (SR scoring)."""
    p, B = m.p, m.B
    N = len(S); mm = p + B + 2
    hit = (S == target).copy()
    order = np.argsort(rng.random((N, mm)), axis=1)
    lg = m.lg0 + phi * m.d
    allmask = (1 << p) - 1
    for pos in range(mm):
        lab = order[:, pos]
        gi = np.where(lab < p)[0]
        if len(gi):
            j = lab[gi]; s = S[gi]; bit = (np.int64(1) << j)
            inn = (s & bit) != 0
            s_add = s | bit; s_del = s & ~bit
            other = np.where(inn, s_del, s_add)
            feas = inn | (m.size[s] < m.K)
            hit[gi[feas & (other == target)]] = True
            a = lg[s_add] - lg[s_del]
            o = np.where(feas | inn, 1 / (1 + np.exp(-np.clip(a, -700, 700))), 0.0)
            o = np.where(m.size[s_del] >= m.K, 0.0, o)
            inc = rng.random(len(gi)) < o
            S[gi] = np.where(inc, s_add, s_del)
        ui = np.where(lab == p)[0]
        if len(ui):
            s = S[ui]; k = m.size[s]; ok = (k > 0) & (k < p); ui, s = ui[ok], s[ok]
            if len(ui):
                j = m._rand_bit(s, rng); l = m._rand_bit(allmask & ~s, rng)
                sp = (s & ~(np.int64(1) << j)) | (np.int64(1) << l)
                hit[ui[sp == target]] = True
                acc = np.log(rng.random(len(ui))) < (lg[sp] - lg[s])
                S[ui] = np.where(acc, sp, s)
        ni = np.where((lab > p) & (lab <= p + B))[0]
        if len(ni):
            s = S[ni]; ok = s > 0; ni, s = ni[ok], s[ok]
            if len(ni):
                j = m._rand_bit(s, rng); cand = m.nbmask[j] & ~s; ok2 = cand > 0
                ni, s, j, cand = ni[ok2], s[ok2], j[ok2], cand[ok2]
                if len(ni):
                    l = m._rand_bit(cand, rng)
                    sp = (s & ~(np.int64(1) << j)) | (np.int64(1) << l)
                    back = popcount(m.nbmask[l] & ~sp)
                    hit[ni[sp == target]] = True
                    la = lg[sp] - lg[s] + np.log(popcount(cand)) - np.log(back)
                    acc = np.log(rng.random(len(ni))) < la
                    S[ni] = np.where(acc, sp, s)
        ii = np.where(lab == p + B + 1)[0]
        if len(ii):
            s = S[ii]; sp = m.draw_pi0(len(ii), rng)
            hit[ii[sp == target]] = True
            acc = np.log(rng.random(len(ii))) < phi * (m.d[sp] - m.d[s])
            S[ii] = np.where(acc, sp, s)
        hit |= (S == target)
    return S, hit


def setup(cfg, n, rng):
    rho = {"A": 0.7, "A85": 0.85}[cfg]
    Sig, C = lh_sigma(4, 4, rho, 0, [(0, 1, 0.5)])
    th, S0, M, Sref = lh_truth(4, 4, 0, [(0, 1, 0.5)], {0: 1.4, 2: 1.8})
    R, r = suff_exact_gram(Sig, th, n, 1.0, rng)
    l = ceil(log(n + 17, 2)); Te = max(1000, l * l)
    m = BVS(R, r * (n - 1), n - 1.0, n, S0, Te=Te)
    return m, S0, M, Sref, C


def run(cfg, n, islands, rng):
    m, S0, M, Sref, C = setup(cfg, n, rng)
    grid, pil, forced = m.method_grid(); T = len(grid) - 1
    N = max(2500, n)
    S0m = m.S0; Srefm = sum(1 << j for j in Sref); jb = M[0]
    allm = np.arange(m.nstates)
    neutral = sum(1 << j for j in range(16) if j not in S0 and j // 4 != 1)
    inN = ((allm & Srefm) == Srefm) & (popcount(allm & neutral) <= 19)
    # lattice crossing temperature
    k0 = m.lg0[S0m] - m.lg0[Srefm]; k1 = m.lg1[S0m] - m.lg1[Srefm]
    phi_star = -k0 / (k1 - k0) if k1 > k0 else 1.0
    pr(f"== config {cfg}, n={n}: pi0(S°)={m.pi0[Srefm]:.3f} pi0(S0)={m.pi0[S0m]:.2e} pi(S0)={m.post[S0m]:.3f}; "
       f"pi0(N^c)={m.pi0[~inN].sum():.2e}; grid T={T} (pilot {len(pil)-1}); lattice crossing phi*={phi_star:.4f}; N={N}")
    exits, first_exit, frac_hit, any_hit, Gam_lat, minlogP, Gam_N = [], [], [], [], [], [], []
    t0 = time.time()
    for isl in range(islands):
        S = m.draw_pi0(N, rng)
        ex = int((~inN[S]).sum()); fe = 0 if ex else None
        G_lat = 0.0; logP = 0.0; mlp = 0.0; G_N = 0.0
        for t in range(1, T + 1):
            dphi = grid[t] - grid[t - 1]
            post = grid[t - 1] >= phi_star
            h = (S == S0m) if post else ((S == S0m) | (S == Srefm))
            dv = m.d[S]
            if h.any() and (~h).any():
                kap = max(0.0, dv[~h].max() - dv[h].min())
            else:
                kap = 0.0
            G_lat += dphi * kap
            lw = dphi * dv; Lw = lse(lw)
            if h.any():
                logP += (lse(lw[h]) - log(h.sum())) - (Lw - log(N))
            mlp = min(mlp, logP)
            hN = inN[S]
            if hN.any() and (~hN).any():
                G_N += dphi * max(0.0, dv[~hN].max() - dv[hN].min())
            w = np.exp(lw - Lw)
            anc = np.minimum(np.searchsorted(np.cumsum(w), rng.random(N) * w.sum(), side="left"), N - 1)
            S = S[anc].copy()
            if t == T:
                S, hit = one_round_hits(m, S, grid[t], rng, S0m)
                frac_hit.append(hit.mean()); any_hit.append(bool(hit.any()))
            else:
                S = m.one_round(S, grid[t], rng, lambda a, b: None)
                e = int((~inN[S]).sum()); ex += e
                if e and fe is None: fe = t
        exits.append(ex); first_exit.append(fe); Gam_lat.append(G_lat); minlogP.append(mlp); Gam_N.append(G_N)
    ex = np.array(exits)
    pr(f"   {islands} islands ({time.time()-t0:.0f}s): confinement exits (particle-stage pairs outside N, stage ends 0..T-1): "
       f"islands with any: {np.mean(ex>0):.2f}, mean count {ex.mean():.1f}; first exit stages {[f for f in first_exit if f is not None][:6]}")
    pr(f"   stage-T round at phi=1: fraction of particles scoring S0: median {np.median(frac_hit):.3f} (min {np.min(frac_hit):.3f}); "
       f"islands with a score: {np.mean(any_hit):.2f}")
    pr(f"   lattice potential: Gamma median {np.median(Gam_lat):.2f} (max {np.max(Gam_lat):.2f}); min_t log P_t median "
       f"{np.median(minlogP):.2f} (worst {np.min(minlogP):.2f});  log(N/T_e) = {log(N/m.Te):.2f}, log(N T) = {log(N*T):.2f}")
    pr(f"   h = 1_N: Gamma median {np.median(Gam_N):.3f} (max {np.max(Gam_N):.3f})")
    # one-round repair constants at phi = 1
    rows = []
    for name, x in [("S°", Srefm), ("S°+proxy5", Srefm | (1 << 5)), ("S°+all proxies", Srefm | (7 << 5)),
                    ("S°+3 C_a nonhubs", Srefm | 0b1110), ("S°+proxies+nonhubs+null", Srefm | (7 << 5) | 0b1110 | (1 << 12)),
                    ("S0+null12", S0m | (1 << 12))]:
        Sx = np.full(20000, x, dtype=np.int64)
        _, hit = one_round_hits(m, Sx, 1.0, rng, S0m)
        lam = bin(x & ~S0m).count("1") + (4 if not (x >> jb) & 1 else 0)
        cmiss = 0 if (x >> jb) & 1 else 1
        c0 = 4.0 ** (-cmiss) / comb(lam + m.B + 2, m.B + 2)
        rows.append(f"{name}: {hit.mean():.3f} (c0(x) = {c0:.2e})")
    pr("   P_x(S0 scored in one round at phi=1): " + "; ".join(rows))


if __name__ == "__main__":
    rng = np.random.default_rng(20261102)
    for cfg in ("A", "A85"):
        for n, isl in [(400, 20), (1600, 20), (6400, 10)]:
            run(cfg, n, isl, rng)
    open(__file__.replace(".py", ".txt"), "w").write("\n".join(out) + "\n")
