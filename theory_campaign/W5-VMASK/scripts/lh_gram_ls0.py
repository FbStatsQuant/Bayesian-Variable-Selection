"""Independent reproduction of W4-T38FULL §3.5: LH exact Gram, G = 12 groups of g = 9 (p = 108), rho = 0.7,
psi = 0.5, c in {1,2,3} pairs with beta = (1.4, -1.0, 1.2), one visible hub (theta = 1), sigma = 1,
n in {200, 800, 3200}, 10 replicates. Unlike T38FULL, the v3 partition is actually run (own port, R13 ties matter
here because the exact Gram has exactly equal within-group correlations up to rounding).
Seed 9700 + 100*c + n_index*10 + rep. Output: ../results/lh_gram_ls0.txt and .jsonl
"""
import json, math
import numpy as np
from vm_core import *
from lh_table import lattice_DS

lines = ["c n | blocks=groups | mode=S° | med pi0(S°) | LS0 scores S0 | moves | DS all lattice states>0 | DS Phi>=2 >0 | "
         "min lattice margin (nats) | S0 best among LS0-scored"]
recs = []
for c in (1, 2, 3):
    for ni, n in enumerate((200, 800, 3200)):
        units, theta, S0, Sref, M, groups = lh_spec(12, 9, 0.7, [0.5] * c, [1.4, -1.0, 1.2][:c], [1.0])
        R = []
        for rep in range(10):
            rng = np.random.default_rng(9700 + 100 * c + 10 * ni + rep)
            Xr, yr = gen_lh_gram(n, 12, 9, units, theta, rng)
            X, y = standardise(Xr, yr)
            bl, B = partition(X)
            sc = Scorer(X, y)
            st = StartLaw(sc, bl)
            mode = st.mode()
            ell = int(math.ceil(math.log2(n + 108 + 1)))
            ls = local_search(sc, mode, ell, target=S0, emit_centre=True)
            ds_all, ds_2 = lattice_DS(sc, Sref, M, S0)
            best = ls["best_seen"]
            rec = dict(c=c, n=n, rep=rep, B=B, beq=sorted(bl) == sorted(groups), mode_eq=mode == Sref,
                       pi0_ref=math.exp(st.log_pi0(Sref)), scored=bool(ls["scored"]), moves=ls["moves"],
                       ds_all=ds_all, ds_2=ds_2, S0_best=bool(sc.F(S0) >= best[0] - 1e-9))
            R.append(rec)
            recs.append(rec)
        f = lambda k: [r[k] for r in R]
        ds2 = sum(r["ds_2"] > 0 for r in R) if c >= 2 else "-"
        lines.append(f"{c} {n} | {sum(f('beq'))}/10 | {sum(f('mode_eq'))}/10 | {np.median(f('pi0_ref')):.2f} | "
                     f"{sum(f('scored'))}/10 | {min(f('moves'))}-{max(f('moves'))} | {sum(r['ds_all'] > 0 for r in R)}/10 | "
                     f"{ds2} | {min(f('ds_all')):.1f} | {sum(f('S0_best'))}/10")
        print(lines[-1], flush=True)
open("../results/lh_gram_ls0.txt", "w").write("\n".join(lines) + "\n")
with open("../results/lh_gram_ls0.jsonl", "w") as fh:
    for r in recs:
        fh.write(json.dumps(r) + "\n")
