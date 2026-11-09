"""N7 (falsification for L2.5 Corollary M): exact-Gram CS with a masked truth j ((1-rho) theta_j + rho*Theta = 0):
start mode (coded partition) == S*, and the LS0 path from S* (closed form) is pure deletion ending at S0.
Output N7_out.txt"""
import math, json, itertools, numpy as np
import bvs_core as bc, fac_core as fc, cs_core as cc, cs_gain as cg
rows = []
for rho in [0.5, 0.3]:
    for (p, n) in [(100, 10**7), (200, 10**8), (400, 10**8)]:
        for seed in range(3):
            # truths at 2 and 40 (different blocks); theta_2 masked: (1-rho) t1 + rho (t1 + t2) = 0 -> t2 = -t1/rho
            t1 = 1.0; t2 = -t1 / rho
            th = np.zeros(p); th[2] = t1; th[40] = t2
            masked = abs((1 - rho) * th[2] + rho * th.sum()) < 1e-12
            Sigma, Lam, Psi = fc.factor_sigma(p, math.sqrt(rho) * np.ones(p), (1 - rho) * np.ones(p))
            P = fc.ExactGram(Sigma, th, n, np.random.default_rng(seed + 9), Lam=Lam, Psi=Psi)
            blocks = bc.partition_from_corr(Sigma, bc.block_size(n, p))
            info = bc.start_mode(P, blocks)
            Pc = cc.CS(rho, th, n, rng=np.random.default_rng(seed + 9))
            out = cg.ls0_path_gain(Pc)
            r = dict(rho=rho, p=p, n=n, seed=seed, masked_truth_index=2, masked=bool(masked), start_full=(len(info.mode) == p),
                     start_has_S0=({2, 40} <= set(info.mode)), path_pure=all(m[0] == "-N" for m in out["moves"]),
                     path_final_S0=out["final_is_S0"], max_add_gain_over_logn=out["info"]["max_add_gain_over_logn"])
            rows.append(r); print(json.dumps(r), flush=True)
print("start full:", sum(r["start_full"] for r in rows), "/", len(rows), " path pure & S0:", sum(r["path_pure"] and r["path_final_S0"] for r in rows))
