"""Study-scale check of W1-EXP headline 6 (n = 200, p in {500, 1000}, scenarios S1..S6).

Covariances and truth ported from Scripts/Data_generators/gen_dev_data.R (scenario_covariance, truth).
Designs: rows iid N(0, Sigma) via numpy (distributionally equal to the R generator, not bitwise).
Partition: port of the engine's v3_blocks.h (vcore.make_blocks). For each cell and design replicate:
  * min_b lambda_min(R_{C_b}) (SE-blk constant phi0^2 on the actual blocks);
  * whether every block is a union of whole groups of 5 (S3-S6);
  * population leakage lambda_b(S0)/(n-1) = c_b' Sigma_bb^{-1} c_b - c_U' Sigma_UU^{-1} c_U, c = Sigma theta,
    U = S0 n C_b, on the ACTUAL sample partition (number of blocks with leakage > 1e-10);
  * population visibility of each true variable in its block: min over U subset of the block's truths... (only
    the U = empty, single-truth case is reported: c_j^2 > 0).
Seed 20261102 + 100*scenario + p. REPS designs per cell (default 3).
"""
import math, sys, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import vcore as V

N = 200
REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 3


from scen import scenario_cov, truth


out = []
for p in (500, 1000):
    act, beta = truth(p)
    th = np.zeros(p); th[act] = beta
    for sc in range(1, 7):
        Sig = scenario_cov(sc, p)
        L = np.linalg.cholesky(Sig)
        cvec = Sig @ th
        rng = np.random.default_rng(20261102 + 100 * sc + p)
        for r in range(REPS):
            Z = rng.standard_normal((N, p)) @ L.T
            X = Z - Z.mean(0); X /= X.std(0, ddof=1)
            R = (X.T @ X) / (N - 1)
            B = V.B_rule(N, p)
            blocks = V.make_blocks(R, B)
            phi2 = min(np.linalg.eigvalsh(R[np.ix_(C, C)]).min() for C in blocks)
            whole = all(len(set(j // 5 for j in C)) * 5 == len(C) for C in blocks)
            nleak = 0; maxleak = 0.0
            for C in blocks:
                U = [j for j in C if th[j] != 0]
                lb = cvec[C] @ np.linalg.solve(Sig[np.ix_(C, C)], cvec[C])
                lu = cvec[U] @ np.linalg.solve(Sig[np.ix_(U, U)], cvec[U]) if U else 0.0
                lam = lb - lu
                if lam > 1e-10: nleak += 1
                maxleak = max(maxleak, lam)
            row = dict(p=p, S=sc, rep=r, B=B, J=len(blocks), phi0sq=round(float(phi2), 4), whole_groups=whole,
                       leaky_blocks=f"{nleak}/{len(blocks)}", max_pop_leak_per_n=round(float(maxleak), 4),
                       sizes=sorted(set(len(C) for C in blocks)))
            print(json.dumps(row), flush=True)
            out.append(row)
json.dump(out, open(__file__.rsplit('/', 2)[0] + '/results/study_check.json', 'w'), indent=0)
