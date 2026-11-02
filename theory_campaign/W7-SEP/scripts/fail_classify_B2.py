"""W7-SEP: classify the centres C ⊆ R from which the production search fails to score S0 (small n), into
  move-limited (the path is still improving after ell moves) vs trapped (path ends at a local max of F that is not
  within one move of S0), and record whether trapped ends beat S0 (posterior miss) or not (genuine search trap).
Same configs as sep_exact.py; seed fixed. Output: ../results/fail_classify_B2.txt"""
import math, numpy as np
from sep_core import *
rng = np.random.default_rng(20261106)
lines = ["cfg n rep | #fail C⊆R | move-limited | trapped: end beats S0 (posterior miss) | trapped: end below S0 (search trap) | trapped ends unlimited-ell: still fail"]
for cfg, ns in (("B2", (400,)),):
    for n in ns:
        for rep in range(10):
            d = build(make_config(cfg), n, rng); p = d["p"]
            sc = scores(d); F, pc, K = sc["F"], sc["pc"], sc["K"]
            S0m = mask_of(d["S0"]); ell = math.ceil(math.log2(n + p + 1))
            succ = successor(F, p, K, pc); near = near_mask(p, K, pc, S0m)
            hit, end, moves = ls_scores_S0(succ, near, ell)
            hitU, endU, _ = ls_scores_S0(succ, near, 200)   # uncapped (path length < 2^p anyway; 200 suffices here)
            allm = np.arange(1 << p); inR = (allm & ~mask_of(d["R"])) == 0; feas = pc <= K
            fail = inR & feas & ~hit
            lim = fail & (succ[end] != end)
            trap = fail & (succ[end] == end)
            tpm = trap & (F[end] > F[S0m]); tst = trap & (F[end] < F[S0m])
            lines.append(f"{cfg} {n} {rep} | {fail.sum()} | {lim.sum()} | {tpm.sum()} | {tst.sum()} | {(fail & ~hitU).sum()}")
            print(lines[-1], flush=True)
open("../results/fail_classify_B2.txt", "w").write("\n".join(lines) + "\n")
