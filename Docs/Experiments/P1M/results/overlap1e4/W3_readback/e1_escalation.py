#!/usr/bin/env python3
"""e1_escalation.py -- HQ H-24 (3): is the per-fit V - T log Zhat gap tied to T escalation?  Descriptive + simple tests, n = 3 escalated vs 17 not.
Reads final/v2/per_fit.csv (the v2 verdict run, all 40 fits) and the escalation CSVs (rebuild counts).  Writes e1_escalation_pairs.csv.
Run with envs/ci-py313 python -I (numpy, scipy)."""
import csv, json, itertools, os
import numpy as np
from scipy import stats
here = os.path.dirname(os.path.abspath(__file__)); base = os.path.dirname(here)
pf = {r["run_id"]: r for r in csv.DictReader(open(os.path.join(here, "final/v2/per_fit.csv")))}
K0 = {}
import glob, re as _re
REC = os.path.expanduser("~/SMC_Engineering_Department/records/overlap1e4")
for u in glob.glob(REC + "/W*/4-*-T-s*"):
    rid = os.path.basename(u).split(".")[0]
    if u.endswith("-s1") or u.endswith("-s2"):
        if os.path.exists(u + ".T2"): continue          # W0: the counted unit is .T2
    ks = [int(m.group(1)) for p in glob.glob(u + "/cost/cost_diag_t0_k*_r1.jsonl") for m in [_re.search(r"_k(\d+)_", p)] if m]
    K0[rid] = (max(ks or [0]), None)
rows = []
for rid, r in sorted(pf.items()):
    if r["arm"] != "T": continue
    v = pf[rid.replace("-T-", "-V-")]
    ds = rid.rsplit("-T-", 1)[0]; s = int(r["seed"])
    gap = float(v["logZ"]) - float(r["logZ"]); se = (float(v["se_logZ_islands"]) ** 2 + float(r["se_logZ_islands"]) ** 2) ** .5
    k0 = K0.get(rid, (None, None))
    rows.append(dict(fit=rid, dataset=ds, seed=s, tier_final_T=int(r["tier_final"]), N_final_T=int(r["N_final"]), logZ_V=float(v["logZ"]), logZ_T=float(r["logZ"]),
                     gap_V_minus_T=gap, se_isl_comb=se, gap_in_isl_se=gap / se, T_rebuilds_t0=k0[0], T_core_h=float(r["core_h"])))
with open(os.path.join(here, "e1_escalation_pairs.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
g = np.array([r["gap_V_minus_T"] for r in rows]); esc = np.array([r["tier_final_T"] >= 1 for r in rows]); z = np.array([r["gap_in_isl_se"] for r in rows])
print("n pairs", len(g), "escalated", esc.sum())
print("ESCALATED:"); [print("  %-24s gap %+.5f (%.2f isl se)  K0 %s core-h %.1f" % (r["fit"], r["gap_V_minus_T"], r["gap_in_isl_se"], r["T_rebuilds_t0"], r["T_core_h"])) for r in rows if r["tier_final_T"] >= 1]
print("NOT ESCALATED:"); [print("  %-24s gap %+.5f (%.2f isl se)  K0 %s core-h %.1f" % (r["fit"], r["gap_V_minus_T"], r["gap_in_isl_se"], r["T_rebuilds_t0"], r["T_core_h"])) for r in rows if r["tier_final_T"] < 1]
a, b = g[esc], g[~esc]
print("\nmeans: escalated %.5f (sd %.5f, n %d); not escalated %.5f (sd %.5f, n %d); all %.5f; difference (esc - non) %.5f" % (a.mean(), a.std(ddof=1), len(a), b.mean(), b.std(ddof=1), len(b), g.mean(), a.mean() - b.mean()))
print("negative gaps: escalated %d/%d, not escalated %d/%d" % ((a < 0).sum(), len(a), (b < 0).sum(), len(b)))
# Welch
tw = stats.ttest_ind(a, b, equal_var=False); print("Welch t = %.2f, df ~ %.1f, p = %.3f" % (tw.statistic, tw.df, tw.pvalue))
# CI of the difference (Welch)
va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b); dfw = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1)); d = a.mean() - b.mean(); se = (va + vb) ** .5
print("Welch 95%% CI of difference: [%.5f, %.5f]" % (d - stats.t.ppf(.975, dfw) * se, d + stats.t.ppf(.975, dfw) * se))
# pooled-variance t (n=3 vs 17)
tp = stats.ttest_ind(a, b, equal_var=True); sp = (((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)) ** .5; sep = sp * (1 / len(a) + 1 / len(b)) ** .5
print("pooled t = %.2f (df %d), p = %.3f, 95%% CI [%.5f, %.5f]" % (tp.statistic, len(a) + len(b) - 2, tp.pvalue, d - stats.t.ppf(.975, 18) * sep, d + stats.t.ppf(.975, 18) * sep))
# exact permutation test on the mean difference, all C(20,3) labelings, one- and two-sided
idx = range(len(g)); obs = d; perm = []
for c in itertools.combinations(idx, int(esc.sum())):
    m = np.zeros(len(g), bool); m[list(c)] = True; perm.append(g[m].mean() - g[~m].mean())
perm = np.array(perm); print("exact permutation (%d labelings): two-sided p = %.4f, one-sided (esc more negative) p = %.4f" % (len(perm), (np.abs(perm) >= abs(obs) - 1e-15).mean(), (perm <= obs + 1e-15).mean()))
mw = stats.mannwhitneyu(a, b, alternative="two-sided"); print("Mann-Whitney U = %.1f, exact two-sided p = %.4f" % (mw.statistic, mw.pvalue))
# in isl-se units
tz = stats.ttest_ind(z[esc], z[~esc], equal_var=False); print("gap in island-se units: mean esc %.2f, non %.2f, Welch p = %.3f" % (z[esc].mean(), z[~esc].mean(), tz.pvalue))
# not escalated alone: is the gap itself nonzero? (V - T bias independent of escalation)
t1 = stats.ttest_1samp(b, 0); print("non-escalated alone: mean %.5f, sd %.5f, one-sample t = %.2f (df 16), p = %.3f, 95%% CI [%.5f, %.5f]" % (b.mean(), b.std(ddof=1), t1.statistic, t1.pvalue, *(b.mean() + np.array([-1, 1]) * stats.t.ppf(.975, 16) * b.std(ddof=1) / len(b) ** .5)))
t2 = stats.ttest_1samp(g, 0); print("all 20: mean %.5f, t = %.2f (df 19), p = %.3f (pairs are not independent: 2 seeds per dataset)" % (g.mean(), t2.statistic, t2.pvalue))
# within-dataset contrast: the 3 datasets with one escalated and one non-escalated seed
print("\nwithin-dataset contrast (datasets with one escalated seed):")
byds = {}
for r in rows: byds.setdefault(r["dataset"], {})[r["seed"]] = r
con = []
for ds, sd in sorted(byds.items()):
    e = [x for x in sd.values() if x["tier_final_T"] >= 1]; n = [x for x in sd.values() if x["tier_final_T"] < 1]
    if len(e) == 1 and len(n) == 1:
        c = e[0]["gap_V_minus_T"] - n[0]["gap_V_minus_T"]; con.append(c); print("  %-20s escalated s%d gap %+.5f, other seed gap %+.5f, contrast %+.5f" % (ds, e[0]["seed"], e[0]["gap_V_minus_T"], n[0]["gap_V_minus_T"], c))
con = np.array(con); tc = stats.ttest_1samp(con, 0)
print("  mean contrast %.5f (sd %.5f), paired t = %.2f (df 2), p = %.3f, 95%% CI [%.5f, %.5f]; all 3 negative: %s" % (con.mean(), con.std(ddof=1), tc.statistic, tc.pvalue, *(con.mean() + np.array([-1, 1]) * stats.t.ppf(.975, 2) * con.std(ddof=1) / 3 ** .5), (con < 0).all()))
print("  (the non-escalated seeds of AR r01, ARweak r01, IND r01 have mean gap %.5f)" % np.mean([ [x for x in sd.values() if x['tier_final_T']<1][0]['gap_V_minus_T'] for ds, sd in byds.items() if any(x['tier_final_T']>=1 for x in sd.values())]))
# non-escalated AR-strong
ar = [r for r in rows if r["dataset"].startswith("4-AR-n200") and r["tier_final_T"] < 1]; print("\nAR-strong T tier-0 fits (%d): mean gap %.5f; AR r04 s1/s2 (both tier 0): %+.5f / %+.5f" % (len(ar), np.mean([r["gap_V_minus_T"] for r in ar]), byds["4-AR-n200-r04"][1]["gap_V_minus_T"], byds["4-AR-n200-r04"][2]["gap_V_minus_T"]))
# covariates: rebuilds at tier 0 and cost (exploratory)
k = np.array([r["T_rebuilds_t0"] for r in rows], float); c = np.array([r["T_core_h"] for r in rows])
print("exploratory Spearman: gap vs K0 (tier-0 rebuilds) rho = %.2f (p = %.3f); gap vs T core-h rho = %.2f (p = %.3f)" % (*stats.spearmanr(g, k), *stats.spearmanr(g, c)))
sl = stats.linregress(k, g); print("   OLS gap ~ K0: slope %.5f per rebuild (p = %.3f)" % (sl.slope, sl.pvalue))
slow = k >= 7
print("   slow-regime tier-0 non-escalated fits (K0 >= 7): n %d, mean gap %.5f ; fast-regime (K0 < 7): n %d, mean gap %.5f" % ((slow & ~esc).sum(), g[slow & ~esc].mean(), (~slow & ~esc).sum(), g[~slow & ~esc].mean()))
# by dataset pooled seed means
print("\nSeed-pooled gap by dataset vs registered E1 ratio is in per_dataset.csv.")
