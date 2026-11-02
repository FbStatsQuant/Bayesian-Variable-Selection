#!/usr/bin/env python3
"""API-N200: assemble the n = 200 table (predicted vs observed, per cell).

Inputs (all read-only, committed copies / repo files):
  data/oswap/local_p{p}_S{s}.csv : O-SWAP per-design quantities (100 designs x 2 scales):
      MC_one  = exact-score MC estimate of P(L | X)  (L = some one-move neighbour of S0 beats S0), R = 40 draws
      MC_miss = same, for "L or a double drop beats S0"
      real_one/real_miss = the same events realised on the study's own y
      A_sum   = sum_e p_e (union bound on P(L|X); PA closed forms, exact kappa's)
      A_max_swap, A_max_drop = max_e p_e over swaps / drops (lower bracket; PA)
      A_ind   = T1 independence predictor, A_lo = cluster-max predictor
  data/oswap/t2_p{p}_S{s}.csv : T2 predictor and Le Cam floor per design
  Results/SMC_BVS_v3_production/p{0500,1000}/exact_recovery_long.csv : observed SMC-BVS v3 HPM outcomes
      n_success (output available), n_fail_total (no output = U), err_exact, err_extra_only, err_missed_only, err_mixed
  S-ELS (theory/S-ELS REPORT, tables/numbers.json): 0 search misses in 2,394 completed fits, S0 scored in all of them.

Output: results/n200_table.csv, results/n200_table.md
"""
import csv, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(HERE, "..", "data", "oswap")
OUT = os.path.join(HERE, "..", "results")
os.makedirs(OUT, exist_ok=True)

def read_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))

# --- observed ---------------------------------------------------------------
obs = {}
for p in (500, 1000):
    path = os.path.join(ROOT, "Results", "SMC_BVS_v3_production", f"p{p:04d}", "exact_recovery_long.csv")
    for r in read_csv(path):
        if r["method_id"] != "SMCBVS" or r["rule_id"] != "hpm" or r["role"] != "primary":
            continue
        if int(r["p"]) != p or r["scenario"] == "pooled":
            continue
        key = (p, int(r["scenario"]), r["scale_key"])
        obs[key] = dict(N=int(r["n_expected"]), n_out=int(r["n_success"]), n_U=int(r["n_fail_total"]),
                        exact=int(r["err_exact"]), extra=int(r["err_extra_only"]),
                        missed=int(r["err_missed_only"]), mixed=int(r["err_mixed"]))
        o = obs[key]
        o["miss"] = o["n_out"] - o["exact"]          # posterior misses (S-ELS: 0 search misses)
        o["wrong"] = o["n_U"] + o["miss"]            # LHS of Thm N200: U or S-hat != S0
        assert o["miss"] == o["extra"] + o["missed"] + o["mixed"], key

# --- predicted (O-SWAP per-design) -------------------------------------------
rows = []
for p in (500, 1000):
    for s in range(1, 7):
        loc = read_csv(os.path.join(DATA, f"local_p{p}_S{s}.csv"))
        t2 = read_csv(os.path.join(DATA, f"t2_p{p}_S{s}.csv"))
        for scale in ("c100", "c050"):
            L = [r for r in loc if r["scale"] == scale]
            T = [r for r in t2 if r["scale"] == scale]
            assert len(L) == 100 and len(T) == 100, (p, s, scale, len(L), len(T))
            f = lambda k, rs=L: np.array([float(r[k]) for r in rs])
            mc_one, mc_miss = f("MC_one"), f("MC_miss")
            R = int(L[0]["MC_R"])
            real_one, real_miss = f("real_one"), f("real_miss")
            a_sum = np.minimum(1.0, f("A_sum"))
            a_max = np.maximum(f("A_max_swap"), f("A_max_drop"))
            t2v = np.array([float(r["T2"]) for r in T])
            lecam = np.array([float(r["lecam_floor"]) for r in T])
            o = obs[(p, s, scale)]
            # predicted count of posterior misses among the n_out fits with output: sum of P(L|X_i) (MC) over designs
            # (we have 100 designs; scale to n_out to compare with the observed miss count among completed fits)
            pred_L = mc_one.mean() * o["n_out"]
            pred_Lmiss = mc_miss.mean() * o["n_out"]
            # z: binomial variance over designs plus MC error of each p-hat
            var = (mc_one * (1 - mc_one)).sum() * o["n_out"] / 100 + (mc_one * (1 - mc_one) / R).sum() * (o["n_out"] / 100) ** 2
            z = (o["miss"] - pred_L) / math.sqrt(max(var, 1e-12))
            rows.append(dict(p=p, S=s, c=0.5 if scale == "c050" else 1.0, N=o["N"], n_out=o["n_out"],
                             obs_U=o["n_U"], obs_miss=o["miss"], obs_wrong=o["wrong"],
                             obs_extra=o["extra"], obs_missed=o["missed"], obs_mixed=o["mixed"],
                             MC_PL=100 * mc_one.mean(), MC_Pmiss=100 * mc_miss.mean(),
                             MC_excess=100 * (mc_miss - mc_one).mean(),
                             real_one=int(real_one.sum()), real_miss=int(real_miss.sum()),
                             lower_maxe=100 * a_max.mean(), union_sum=100 * a_sum.mean(),
                             T2=100 * t2v.mean(), lecam=100 * lecam.mean(),
                             pred_wrong=o["n_U"] + pred_L, pred_wrong_dd=o["n_U"] + pred_Lmiss, z=z))

# --- write ------------------------------------------------------------------
keys = list(rows[0].keys())
with open(os.path.join(OUT, "n200_table.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)

def fmt(x, d=1):
    return f"{x:.{d}f}" if isinstance(x, float) else str(x)

lines = []
lines.append("# n = 200 table: Theorem N200 terms, predicted vs observed, per cell (100 fits each)\n")
lines.append("Columns: obs U = fits with no output (resource_limit); obs miss = posterior misses among fits with output "
             "(S-ELS: every completed wrong HPM has F(S0) < F(S-hat); 0 search misses); obs wrong = U + miss = the event of Thm N200. "
             "P(L|X) = exact-score MC (R = 40 draws per design, 100 designs) of the one-move posterior-miss event, a rigorous LOWER bound on the posterior-miss term P(S-dagger != S0 | X); "
             "P(L or dd) adds the 91 double drops; excess = their difference (the measured multi-move contribution, not a bound); "
             "realised = the same events on the study's own y (count of 100); "
             "max_e p_e = rigorous lower bracket (PA closed forms); sum_e p_e = union bound on P(L|X) (PA), capped at 1 per design; T2 = O-SWAP's approximate predictor; Le Cam = pairwise two-point floor for ANY selector. "
             "pred wrong = obs U + n_out * mean P(L|X); z = (obs miss - n_out * mean P(L|X)) / SD (design binomial + MC error).\n")
for c in (1.0, 0.5):
    lines.append(f"\n## c = {c}\n")
    lines.append("| p | S | obs U | obs miss (extra/missed/mixed) | **obs wrong** | P(L\\|X) % | P(L or dd) % | excess pts | realised one/miss | max_e p_e % | sum_e p_e % | T2 % | Le Cam % | **pred wrong** | z |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    tot = dict(U=0, miss=0, wrong=0, pL=0.0, pLdd=0.0, pred=0.0, real=0, T2=0.0, var=0.0)
    for p in (500, 1000):
        for r in [r for r in rows if r["c"] == c and r["p"] == p]:
            lines.append(f"| {r['p']} | S{r['S']} | {r['obs_U']} | {r['obs_miss']} ({r['obs_extra']}/{r['obs_missed']}/{r['obs_mixed']}) | **{r['obs_wrong']}** | "
                         f"{fmt(r['MC_PL'])} | {fmt(r['MC_Pmiss'])} | {fmt(r['MC_excess'])} | {r['real_one']}/{r['real_miss']} | {fmt(r['lower_maxe'],2)} | {fmt(r['union_sum'])} | {fmt(r['T2'])} | {fmt(r['lecam'])} | **{fmt(r['pred_wrong'])}** | {fmt(r['z'])} |")
            tot["U"] += r["obs_U"]; tot["miss"] += r["obs_miss"]; tot["wrong"] += r["obs_wrong"]
            tot["pL"] += r["MC_PL"] * r["n_out"] / 100; tot["pLdd"] += r["MC_Pmiss"] * r["n_out"] / 100
            tot["pred"] += r["pred_wrong"]; tot["real"] += r["real_one"]; tot["T2"] += r["T2"] * r["n_out"] / 100
        sub = [r for r in rows if r["c"] == c and r["p"] == p]
        lines.append(f"| {p} | **sum** | {sum(r['obs_U'] for r in sub)} | {sum(r['obs_miss'] for r in sub)} | **{sum(r['obs_wrong'] for r in sub)}** | "
                     f"{fmt(sum(r['MC_PL']*r['n_out']/100 for r in sub))} | {fmt(sum(r['MC_Pmiss']*r['n_out']/100 for r in sub))} | | {sum(r['real_one'] for r in sub)}/{sum(r['real_miss'] for r in sub)} | | | {fmt(sum(r['T2']*r['n_out']/100 for r in sub))} | | **{fmt(sum(r['pred_wrong'] for r in sub))}** | |")
    lines.append(f"\nc = {c} totals over 1,200 fits: observed wrong = {tot['wrong']} (U = {tot['U']}, posterior misses = {tot['miss']}); "
                 f"predicted wrong = U + sum P(L|X) = {tot['pred']:.1f}; with double drops = {tot['U'] + tot['pLdd']:.1f}; realised one-move on study y = {tot['real']}; T2 = {tot['T2']:.1f}.")
allU = sum(r["obs_U"] for r in rows); allmiss = sum(r["obs_miss"] for r in rows)
allpred = sum(r["pred_wrong"] for r in rows)
lines.append(f"\n**Grand total (2,400 fits):** observed wrong = {allU + allmiss} (U = {allU}, posterior misses = {allmiss}, search misses = 0); "
             f"predicted = {allpred:.1f} (U observed + sum of MC P(L|X)); RMS z over 24 cells = {math.sqrt(np.mean([r['z']**2 for r in rows])):.2f}; "
             f"max |z| = {max(abs(r['z']) for r in rows):.2f}.")
# discovery term: rule of three
n_done = sum(r["n_out"] for r in rows)
lines.append(f"\n**Discovery / search-miss term:** observed 0 of {n_done} completed fits (S-ELS); exact 95% Clopper-Pearson upper bound "
             f"{100 * (1 - 0.05 ** (1 / n_done)):.3f}% per fit; pooled over the 24 cells.")
with open(os.path.join(OUT, "n200_table.md"), "w") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))
