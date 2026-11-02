"""O-BGIBBS bg2: time-to-score on LH exact Gram, pilot stage 1 AND final-run bridge (no floor).

For each replicate (fresh noise):
  * phi1  = pilot stage-1 temperature (engine's particle rule on H iid pi_0 draws, as in bg1);
  * grid  = final-run grid (idealised calibration of bvs_core: exact-law pilot + V + rho_V grid, M §6.7);
  * q(phi) = per-particle probability that ONE round at phi started at S° scores S0 (Monte Carlo, M copies);
            evaluated at phi = 0, phi1, grid[1];
  * logk  = log Gibbs odds of adding each masked hub at S°, at phi1 and grid[1];
  * a final island (N particles, the grid, L + 4 terminal rounds): first stage at which S0 is scored, the basin count
    (S° plus S° u A, A subset of M, plus S° u {masked proxy}) after resampling at that stage, and the minimum basin
    count over the stages before scoring (the "extinction margin").
Prediction checked: S0 is scored by stage t as soon as sum_{s<=t} N_basin(s) q(phi_s) >> 1  (Theorem BG2).
Usage: python bg2_score_rate.py c n reps    (c = 2: p = 16, g = 4;  c = 3: p = 18, g = 3).  Seed fixed per (c, n).
"""
import sys
import numpy as np
from bvs_core import BVS, suff_stats
from bg1_first_stage import pilot_next_phi


def lh_design(c, g, rho=0.7, psi=0.5, beta=1.0):
    ng = 2 * c
    p = ng * g
    S = np.zeros((p, p))
    for h in range(ng):
        for i in range(h * g, (h + 1) * g):
            for j in range(h * g, (h + 1) * g):
                S[i, j] = 1.0 if i == j else rho
    theta = np.zeros(p)
    ha, hb = [], []
    for k in range(c):
        a, b = 2 * k, 2 * k + 1
        ja, jb = a * g, b * g
        for i in range(a * g, (a + 1) * g):
            for j in range(b * g, (b + 1) * g):
                S[i, j] = S[j, i] = psi * S[i, ja] * S[jb, j]
        theta[ja] = beta; theta[jb] = -psi * beta
        ha.append(ja); hb.append(jb)
    return S, theta, ha, hb


def q_round(M, x, phi, rng, Mc=20000):
    """Per-particle one-round scoring probability from x at phi.  Exact per-particle detection: the recorder is
    called with arrays aligned to the particle subset acting at that position; we wrap one_round so that every
    evaluated array is compared with S0 and the hit is attributed through an id array carried alongside."""
    S = np.full(Mc, x, dtype=np.int64)
    hits = np.zeros(Mc, bool)
    p, B = M.p, M.B
    m = p + B + 2
    order = np.argsort(rng.random((Mc, m)), axis=1)
    lg = M.lg0 + phi * M.d
    allmask = (1 << p) - 1
    for pos in range(m):
        lab = order[:, pos]
        gi = np.where(lab < p)[0]
        if len(gi):
            j = lab[gi]; s = S[gi]; bit = (np.int64(1) << j)
            inn = (s & bit) != 0
            s_add = s | bit; s_del = s & ~bit
            other = np.where(inn, s_del, s_add)
            feas = inn | (M.size[s] < M.K)
            hits[gi[feas & (other == M.S0)]] = True
            a = lg[s_add] - lg[s_del]
            o = np.where(feas | inn, 1 / (1 + np.exp(-np.clip(a, -700, 700))), 0.0)
            o = np.where(M.size[s_del] >= M.K, 0.0, o)
            inc = rng.random(len(gi)) < o
            S[gi] = np.where(inc, s_add, s_del)
        ui = np.where(lab == p)[0]
        if len(ui):
            s = S[ui]; k = M.size[s]
            ok = (k > 0) & (k < p); ui, s = ui[ok], s[ok]
            if len(ui):
                j = M._rand_bit(s, rng); l = M._rand_bit(allmask & ~s, rng)
                sp = (s & ~(np.int64(1) << j)) | (np.int64(1) << l)
                hits[ui[sp == M.S0]] = True
                acc = np.log(rng.random(len(ui))) < (lg[sp] - lg[s])
                S[ui] = np.where(acc, sp, s)
        ni = np.where((lab > p) & (lab <= p + B))[0]
        if len(ni):
            s = S[ni]; ok = s > 0; ni, s = ni[ok], s[ok]
            if len(ni):
                j = M._rand_bit(s, rng); cand = M.nbmask[j] & ~s
                ok2 = cand > 0; ni, s, j, cand = ni[ok2], s[ok2], j[ok2], cand[ok2]
                if len(ni):
                    from bvs_core import popcount
                    l = M._rand_bit(cand, rng)
                    sp = (s & ~(np.int64(1) << j)) | (np.int64(1) << l)
                    back = popcount(M.nbmask[l] & ~sp)
                    hits[ni[sp == M.S0]] = True
                    la = lg[sp] - lg[s] + np.log(popcount(cand)) - np.log(back)
                    acc = np.log(rng.random(len(ni))) < la
                    S[ni] = np.where(acc, sp, s)
        ii = np.where(lab == p + B + 1)[0]
        if len(ii):
            s = S[ii]; sp = M.draw_pi0(len(ii), rng)
            hits[ii[sp == M.S0]] = True
            acc = np.log(rng.random(len(ii))) < phi * (M.d[sp] - M.d[s])
            S[ii] = np.where(acc, sp, s)
    return hits.mean()


def main():
    c, n, reps = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    g = 4 if c == 2 else 3
    R, theta, ha, hb = lh_design(c, g)
    p = R.shape[0]
    S0 = [j for j in range(p) if theta[j] != 0]
    Sdeg = sum(1 << j for j in ha)
    hubm = [1 << j for j in hb]
    basin = set([Sdeg])
    for A in range(1 << c):
        if A == (1 << c) - 1: continue
        basin.add(Sdeg | sum(hubm[i] for i in range(c) if (A >> i) & 1))
    for jb in hb:
        for k in range(jb, jb + g):
            basin.add(Sdeg | (1 << k))
    basin = np.array(sorted(basin), dtype=np.int64)
    rng = np.random.default_rng(1000 * c + n)
    N = max(2500, n, p)
    H = int(np.ceil(512 * N / 2500))
    print("c=%d p=%d g=%d n=%d N=%d H=%d reps=%d (LH exact Gram, rho=0.7, psi=0.5, beta=1, sigma=1)" % (c, p, g, n, N, H, reps))
    print("rep | pi(S0) pi0(S°) | phi1  q(0)  q(phi1) H*q(phi1) | T  grid1  q(grid1) N*q(grid1) | first-score stage(mech) phi_at  minbasin_before  sum_{s<t*} Nb*q")
    for r in range(reps):
        z, yy = suff_stats(R, theta, 1.0, n, rng)
        M = BVS(R, z, yy, n, S0, Te=1000)
        X = M.draw_pi0(H, rng)
        phi1, _ = pilot_next_phi(M.d[X], 0.0, H, M.Te)
        grid, pil, forced = M.method_grid()
        q0 = q_round(M, Sdeg, 0.0, rng)
        qp = q_round(M, Sdeg, phi1, rng)
        qg = q_round(M, Sdeg, grid[1], rng)
        isb = np.zeros(M.nstates, bool); isb[basin] = True
        info = M.island(N, grid, rng, sets={"basin": isb})
        fs = info["first_S0"]
        cb = info["counts"]["basin"]
        if fs is None:
            tstar, mech, phis = -1, "none", float("nan")
        else:
            tstar, mech = fs
            phis = grid[min(tstar, len(grid) - 1)]
        # predicted cumulative scoring mass before t*: sum over stages s = 1..t*-1 of N_basin(after stage s-1) q(phi_s)
        upto = (tstar if tstar > 0 else len(grid))
        cum = 0.0
        for s in range(1, min(upto + 1, len(grid), 41)):
            cum += cb[s - 1] * q_round(M, Sdeg, grid[s], rng, Mc=4000)
        minb = int(cb[:max(tstar, 1)].min()) if len(cb) else -1
        print("%2d | %.3f %.3f | %.4f %.1e %.1e %8.1f | %3d %.5f %.1e %8.1f | %3d(%s) %.4f %6d %10.1f"
              % (r, M.post[M.S0], M.pi0[Sdeg], phi1, q0, qp, H * qp, len(grid) - 1, grid[1], qg, N * qg,
                 tstar, mech, phis, minb, cum))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
