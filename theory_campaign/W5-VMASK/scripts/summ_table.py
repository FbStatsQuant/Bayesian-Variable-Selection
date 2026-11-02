"""Summarise ../results/lh_<CFG>.jsonl into the PXN-style table. Output appended to ../results/table_<CFG>.txt"""
import json, sys, math
import numpy as np
from scipy.stats import chi2
cfg = sys.argv[1]
recs = [json.loads(l) for l in open(f"../results/lh_{cfg}.jsonl")]
c = {"A": 1, "B": 2}.get(cfg, 1)
s = {"A": 2, "B": 3}.get(cfg, 2)
lim0 = sum(math.log((s + i) / 2) for i in range(1, c + 1))
q = [lim0 + 0.5 * chi2.ppf(x, c) for x in (0.05, 0.5, 0.95)]
out = [f"config {cfg}; Mstat limit law quantiles q05/med/q95 = {q[0]:.2f}/{q[1]:.2f}/{q[2]:.2f}",
       "n | p | reps | b=g | P1-margin(minin>maxout) | SE-blk med | med log10 pi0(S0) | Mstat q05/med/q95 | sqrt(n/logn)(1-pi0(S°)) med | med pi0(S°) | mode=S° | med q | T22 ok | LS0 scored | LS0 cert@S0 | med F(S0)-F(S°) | #F(S0)<F(S°) | (L) holds | med (L) margin | DS_all>0 | DS_phi2>0 | med Dep"]
for n in sorted(set(r["n"] for r in recs)):
    R = [r for r in recs if r["n"] == n]
    p = R[0]["p"]
    f = lambda k: np.array([r[k] for r in R], float)
    ms = np.quantile(f("mstat"), [0.05, 0.5, 0.95])
    dep = f"{np.median(f('Dep')):.3f}" if "Dep" in R[0] else "-"
    ds2 = sum(r["DS_phi2"] > 0 for r in R) if c >= 2 else "-"
    out.append(f"{n} | {p} | {len(R)} | {sum(r['blocks_eq_groups'] for r in R)} | {sum(r['minin'] > r['maxout'] for r in R)} | "
               f"{np.median(f('seblk')):.3f} | {np.median(f('log10_pi0_S0')):.2f} | {ms[0]:.2f}/{ms[1]:.2f}/{ms[2]:.2f} | "
               f"{np.median(f('scaled_def')):.2f} | {np.median(f('pi0_ref')):.3f} | {sum(r['mode_eq_ref'] for r in R)} | "
               f"{np.median(f('q')):.3f} | {sum(r['t22_ok'] for r in R)} | {sum(r['ls_scored'] for r in R)} | "
               f"{sum(r['ls_cert_S0'] for r in R)} | {np.median(f('dF')):.1f} | {sum(r['dF'] < 0 for r in R)} | "
               f"{sum(r['L_margin'] > 0 for r in R)} | {np.median(f('L_margin')):.2f} | {sum(r['DS_all'] > 0 for r in R)} | {ds2} | {dep}")
txt = "\n".join(out)
print(txt)
open(f"../results/table_{cfg}.txt", "w").write(txt + "\n")
