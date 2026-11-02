"""O-BGIBBS bg3: locked start set U = {y : y contains S°} and terminal-round discovery (Theorem BG3) on LH exact Gram.

For each replicate (fresh noise): one faithful final island (N iid pi_0 draws, the method grid, L + 4 terminal rounds
at phi = 1, no resampling in the terminal rounds).  Records
  * N_U(t)/N, the fraction of particles containing S° after every stage, and its minimum over the whole run
    (confinement: Theorem BG3 (L1) predicts 1 up to N*pi0(U^c) + exponentially small exits);
  * pi0(U^c);
  * q1 := per-particle probability that ONE round at phi = 1 scores S0, from S° and from each distinct state of the
    end-of-bridge population inside U (minimum reported; Monte Carlo, 4000 copies each, at most 30 states);
  * the implied bound on P(S0 unscored in the terminal rounds | population in U) <= (1 - min q1)^(N (L+4)).
Usage: python bg3_locked.py c n reps.  Seed fixed per (c, n).
"""
import sys
import numpy as np
from bvs_core import BVS, suff_stats, popcount
from bg2_score_rate import lh_design, q_round


def main():
    c, n, reps = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    g = 4 if c == 2 else 3
    R, theta, ha, hb = lh_design(c, g)
    p = R.shape[0]
    S0 = [j for j in range(p) if theta[j] != 0]
    Sdeg = sum(1 << j for j in ha)
    rng = np.random.default_rng(7000 + 100 * c + n)
    N = max(2500, n, p)
    print("c=%d p=%d g=%d n=%d N=%d reps=%d (LH exact Gram)" % (c, p, g, n, N, reps))
    print("rep | pi0(U^c)  min_t N_U/N  N_U/N(end bridge)  N_U/N(final) | first score (stage, mech) | q1(S°)  min q1 over end-of-bridge U states (#states)  log10 bound")
    for r in range(reps):
        z, yy = suff_stats(R, theta, 1.0, n, rng)
        M = BVS(R, z, yy, n, S0, Te=1000)
        allm = np.arange(M.nstates, dtype=np.int64)
        isU = (allm & Sdeg) == Sdeg
        grid, _, _ = M.method_grid()
        info = M.island(N, grid, rng, sets={"U": isU})
        cu = info["counts"]["U"] / N
        fin = info["final_counts"]["U"] / N
        # end-of-bridge population is not returned; use the final states as the population sample inside U
        st = np.unique(info["final_states"][isU[info["final_states"]]])
        st = list(st[st != M.S0][:20])
        prox = [k for jb in hb for k in range(jb + 1, jb + g)]
        nulls = [ha[0] + 1, ha[-1] + 1]   # non-hub members of C_a (zero partial covariance given a, P1d)
        st += [Sdeg | (1 << k) for k in prox[:4]] + [Sdeg | (1 << nulls[0]), Sdeg | (1 << nulls[0]) | (1 << nulls[1])]
        st += [Sdeg | sum(1 << k for k in prox)]                       # every masked proxy present
        st += [Sdeg | (1 << hb[0]) | sum(1 << k for k in prox if k > hb[-1])]   # one hub + proxies of the last group
        q1s = q_round(M, Sdeg, 1.0, rng, Mc=4000)
        qs = [q_round(M, int(x), 1.0, rng, Mc=4000) for x in st]
        qmin = min(qs) if qs else float("nan")
        L4 = M.L + 4
        qq = min(q1s, qmin) if qs else q1s
        lb = N * L4 * np.log10(max(1e-300, 1 - qq)) if qq < 1 else -np.inf
        print("%2d | %.1e  %.4f  %.4f  %.4f | %s | %.3f  %.3f (%d)  %.0f"
              % (r, M.pi0[~isU].sum(), cu.min(), cu[-1], fin, str(info["first_S0"]), q1s, qmin, len(st), lb))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
