"""CE1 re-check (W2-VT24G): one-round exit probability from R_d at boundary states, p = 20, n = 200.

H24 requires sup_{x in R_d} P_x(some elementary state of one round lies outside R_d) <= eta_n with (L+4) eta_n -> 0.
For each design: enumerate all boundary states Y = U u P (U subset S0 with >= 1 missing truth, |P| = d), compute
(i) the EXACT first-change lower bound  P*_exit(Y) = sum_e s_e int prod_{j != e}(1 - t q_j) dt  (Lemma O(iii)),
    a rigorous lower bound on P_Y(exit in one round)  (s_e = P_Y(label e moves outside R_d), q_e = P_Y(e moves));
(ii) the closed-form look-alike bound  max_l o_l(Y) * (product-free) 1/(B+d+4)-type bound is NOT used; we use (i);
(iii) Monte Carlo of the actual round (vectorised engine) at the top states: 20000 reps.
Designs: seed 1 (W1's datasets) and seeds 2..4 (fresh replicates). RNG seed 2026.
"""
import sys, json, math, itertools
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ref_engine import make_data, Model, mask_to_list
from exact_laws import label_laws, indep_accept, first_change_prob


def region(M, d):
    ar = np.arange(1 << M.p, dtype=np.int64)
    extra = M.sizes[ar & ~np.int64(M.S0)]
    return extra <= d


def pstar_exit(M, x, inR):
    s, q = [], []
    for name, law in label_laws(M, x):
        s.append(sum(pr for yy, pr in law.items() if yy != x and not inR[yy]))
        q.append(sum(pr for yy, pr in law.items() if yy != x))
    a = indep_accept(M, x); a[x] = 0
    s.append(float(a[~inR].sum())); q.append(float(a.sum()))
    return first_change_prob(s, q)


def main(out):
    rng = np.random.default_rng(2026)
    recs = []
    for seed in [1, 2, 3, 4]:
        for scen in [1, 2, 3, 4, 5, 6]:
            for c in [1.0, 0.5]:
                if seed > 1 and c == 0.5:
                    continue
                X, y, S0 = make_data(scen, c, seed=seed)
                M = Model(X, y, S0)
                tru = mask_to_list(S0); nul = [j for j in range(M.p) if j not in tru]
                for d in [1, 2]:
                    inR = region(M, d)
                    cands = []
                    for r in range(0, len(tru)):          # |U| = r < s0 (>= 1 missing)
                        for U in itertools.combinations(tru, r):
                            for P in itertools.combinations(nul, d):
                                Y = sum(1 << j for j in U + P)
                                # screen: max over absent nulls of the Gibbs inclusion probability at Y
                                mx = max(1.0 / (1.0 + math.exp(M.F[Y] - M.F[Y | (1 << l)]))
                                         for l in nul if not Y >> l & 1)
                                cands.append((mx, Y))
                    cands.sort(reverse=True)
                    best = (-1, None)
                    for _, Y in cands[:30]:
                        v = pstar_exit(M, Y, inR)
                        if v > best[0]:
                            best = (v, Y)
                    Y = best[1]
                    _, _, ex = M.round(np.full(20000, Y, dtype=np.int64), rng, region=inR)
                    pe = float(ex.mean())
                    rec = dict(seed=seed, scen=scen, c=c, d=d, Y=mask_to_list(Y), S0=tru,
                               missing=[j for j in tru if not Y >> j & 1], pstar_exit_exact=best[0],
                               exit_mc=pe, mc_se=math.sqrt(pe * (1 - pe) / 20000), Lplus4_times_exit=(M.L + 4) * pe,
                               pi_S0=float(M.post[S0]), floor_1_over_B_d_4=1.0 / (M.B + d + 4))
                    recs.append(rec)
                    print(json.dumps(rec), flush=True)
    json.dump(recs, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
