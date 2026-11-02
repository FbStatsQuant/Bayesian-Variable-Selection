"""CE1 asymptotic check (W2-VT24G): one-round exit probability from R_1 at the worst boundary state as n grows
(p = 20 fixed, so B = 4 fixed; designs S3, S4, S2; c = 0.5; data seeds 1-3). The PROOF SKETCH predicts the exit
probability stays >= (1 - o(1)) / (B + d + 4) = 1/9 and does not tend to 0. Exact first-change lower bound + MC."""
import sys, json, math, itertools
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ref_engine import make_data, Model, mask_to_list
from ce1_recheck import region, pstar_exit
rng = np.random.default_rng(31)
recs = []
for scen in [2, 3, 4]:
    for n in [200, 800, 3200]:
        for seed in [1, 2, 3]:
            X, y, S0 = make_data(scen, 0.5, n=n, seed=seed)
            M = Model(X, y, S0)
            inR = region(M, 1)
            tru = mask_to_list(S0); nul = [j for j in range(M.p) if j not in tru]
            cands = []
            for r in range(len(tru)):
                for U in itertools.combinations(tru, r):
                    for l0 in nul:
                        Y = sum(1 << j for j in U) | (1 << l0)
                        mx = max(1 / (1 + math.exp(min(700, M.F[Y] - M.F[Y | (1 << l)]))) for l in nul if l != l0)
                        cands.append((mx, Y))
            cands.sort(reverse=True)
            best = max((pstar_exit(M, Y, inR), Y) for _, Y in cands[:15])
            _, _, ex = M.round(np.full(10000, best[1], dtype=np.int64), rng, region=inR)
            rec = dict(scen=scen, n=n, seed=seed, B=M.B, L=M.L, Y=mask_to_list(best[1]), pstar_exit=best[0],
                       exit_mc=float(ex.mean()), Lplus4_times_exit=(M.L + 4) * float(ex.mean()))
            recs.append(rec); print(json.dumps(rec), flush=True)
json.dump(recs, open(sys.argv[1], 'w'), indent=1)
