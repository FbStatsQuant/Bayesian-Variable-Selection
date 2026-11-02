"""W7-SEP: summarise ../results/sep_*.jsonl into ../results/summary.txt (medians / counts per cell)."""
import json, glob, math, numpy as np
out = []
for f in sorted(glob.glob("../results/sep_*.jsonl")):
    R = [json.loads(l) for l in open(f)]
    if not R: continue
    cfg, des = R[0]["cfg"], R[0]["design"]
    out.append(f"## {cfg} ({des}), p = {R[0]['p']}, c = {R[0]['c']}")
    out.append("n | reps | med log10 pi0(S0) | Mstat q05/med/q95 | med pi(S0) | med pi0(S°) | mode=S° | "
               "med P(hit|Q_f) | med P(hit|Q=n) | med P(hit|Q=n^2) | med log10(1+chi2) | med KL | med log10 relvar/draw | "
               "LS0 scores S0 | med pi0(basin) | min pi0(basin) | all C⊆R scored (reps) | min frac C⊆R | med frac all centres | max moves C⊆R | ell | reps with other local maxima")
    for n in sorted(set(r["n"] for r in R)):
        S = [r for r in R if r["n"] == n]
        med = lambda k: float(np.median([r[k] for r in S]))
        Ms = np.array([r["Mstat"] for r in S])
        out.append(f"{n} | {len(S)} | {med('logpi0_S0')/math.log(10):.2f} | "
                   f"{np.quantile(Ms,.05):.2f}/{np.median(Ms):.2f}/{np.quantile(Ms,.95):.2f} | {med('pi_S0'):.3f} | "
                   f"{med('pi0_Sstar'):.3f} | {sum(r['mode_is_Sstar'] for r in S)}/{len(S)} | "
                   f"{np.median([r['hit']['Qf'] for r in S]):.3g} | {np.median([r['hit']['n'] for r in S]):.3g} | "
                   f"{np.median([r['hit']['n2'] for r in S]):.3g} | {med('log_chi2p1')/math.log(10):.2f} | {med('KL'):.2f} | "
                   f"{math.log10(med('relvar_per_draw')):.2f} | {sum(r['ls0_scores_S0'] for r in S)}/{len(S)} | "
                   f"{med('pi0_basin'):.6f} | {min(r['pi0_basin'] for r in S):.6f} | "
                   f"{sum(r['n_R_fail']==0 for r in S)}/{len(S)} | {min(r['frac_R_centres'] for r in S):.4f} | "
                   f"{med('frac_all_centres'):.4f} | {max(r['max_moves_R'] for r in S)} | {S[0]['ell']} | "
                   f"{sum(r['n_local_max_other']>0 for r in S)}/{len(S)}")
    out.append("")
open("../results/summary.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
