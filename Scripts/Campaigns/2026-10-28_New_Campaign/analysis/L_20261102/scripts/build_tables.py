"""build_tables.py SCORE_DIR TABLES_DIR [INVENTORY_DIR]

Builds the ANALYSIS-L tables from the merged scoring output (case-level CSVs) and checks every p x scenario x c cell
against the pipeline's own H1-H4 (tables.R). Writes only after all checks pass. Denominators follow METRICS.md:
rates over the EXPECTED cases (missing/failed = "not equal"); error statistics over the fits that supply the field (n shown).
Adds an overall pooled row (both p, both c; 2,400 cases) and the benchmark Q4 headline rules (D35/D42) when benchmark rows exist.
"""
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd

S = Path(sys.argv[1]); T = Path(sys.argv[2])
INV = Path(sys.argv[3]) if len(sys.argv) > 3 else None
rd = lambda f: pd.read_csv(S / f, keep_default_na=True, na_values=["NA"], low_memory=False)
roster = rd("roster.csv"); acc = rd("case_smc_accuracy.csv"); ref = rd("case_reference.csv"); sel = rd("case_selection.csv")
stab = rd("case_stability.csv"); H1p = rd("H1_logZ.csv"); H2p = rd("H2_hpm.csv"); H3p = rd("H3_pip.csv"); H4p = rd("H4_recovery.csv")
assert len(roster) == 2400 and roster.case_id.is_unique, "roster must be 2,400 unique cases"

def tf(s):  # logical column -> bool with NA as False
    return s.map(lambda v: str(v).upper() == "TRUE")
def q90(x):
    x = pd.Series(x).dropna()
    return float(np.quantile(x, 0.9)) if len(x) else np.nan  # numpy 'linear' = R type 7
def mean(x):
    x = pd.Series(x).dropna(); return float(x.mean()) if len(x) else np.nan

main = acc[acc["rep"] == 0].copy()
assert main.case_id.is_unique
base = roster.merge(ref[["case_id", "has_exact", "exact_hpm_eq_truth", "exact_mpm_eq_truth"]], on="case_id", how="left")
base = base.merge(main, on="case_id", how="left", suffixes=("", "_acc"))
base["found"] = base["rep"].notna()
base["okb"] = tf(base["ok"])
base["state"] = np.where(~base.found, "missing", np.where(base.okb, "ok", "failed"))
base["has_exactb"] = tf(base["has_exact"])
base["scenario"] = base["scenario"].astype(str)

GROUPS = [("p", "scenario", "scale_key")]
def cells(df):
    out = []
    for (p, c), g in df.groupby(["p", "scale_key"]):
        for sc, gg in g.groupby("scenario"): out.append((p, sc, c, gg))
        out.append((p, "all", c, g))
    out.append(("all", "all", "all", df))
    return out

def avail(g):
    return dict(n_cases=len(g), n_smc_missing=int((g.state == "missing").sum()), n_smc_failed=int((g.state == "failed").sum()),
                n_exact_missing=int((~g.has_exactb).sum()))

def pct(b, n): return 100.0 * int(b.sum()) / n if n else np.nan

q1, q2, q3 = [], [], []
for p, sc, c, g in cells(base):
    ids = dict(p=p, scenario=sc, scale_key=c); a = avail(g); n = len(g)
    e = g["e"].dropna()
    q1.append({**ids, **a, "n_evidence": len(e), "bias": mean(e), "rmse": float(np.sqrt((e ** 2).mean())) if len(e) else np.nan,
               "median_abs_e": float(e.abs().median()) if len(e) else np.nan, "p90_abs_e": q90(e.abs()),
               "lb_coverage": float(tf(g.loc[g["e"].notna(), "lb_cover"]).mean()) if len(e) else np.nan,
               "n_lb_violated": int((tf(g.loc[g["e"].notna(), "lb_cover"]) == False).sum())})
    q2.append({**ids, **a, "pct_smc_hpm_eq_exact": pct(tf(g.hpm_eq_exact), n), "pct_exact_hpm_eq_truth": pct(tf(g.exact_hpm_eq_truth), n),
               "pct_smc_hpm_eq_truth": pct(tf(g.hpm_eq_truth), n), "n_smc_hpm_ne_exact": n - int(tf(g.hpm_eq_exact).sum())})
    q3.append({**ids, **a, "n_rb": int(g.rb_max.notna().sum()), "n_plain": int(g.plain_max.notna().sum()),
               "rb_mean_max_err": mean(g.rb_max), "rb_p90_max_err": q90(g.rb_max), "plain_mean_max_err": mean(g.plain_max), "plain_p90_max_err": q90(g.plain_max),
               "pct_mpm_rb_eq_exact": pct(tf(g.mpm_rb_eq_exact), n), "pct_mpm_plain_eq_exact": pct(tf(g.mpm_plain_eq_exact), n)})
Q1, Q2, Q3 = pd.DataFrame(q1), pd.DataFrame(q2), pd.DataFrame(q3)

# ---- cross-check against the pipeline tables (every p x scenario x c and per-p pooled cell) ----
problems = []
def check(mine, pipe, cols):
    pipe = pipe.copy(); pipe["scenario"] = pipe["scenario"].astype(str); pipe["p"] = pipe["p"].astype(str)
    m = mine[mine.p != "all"].copy(); m["p"] = m["p"].astype(int).astype(str)
    j = m.merge(pipe, on=["p", "scenario", "scale_key"], suffixes=("", "_pipe"), how="outer", indicator=True)
    if (j["_merge"] != "both").any(): problems.append(f"cell sets differ for {cols[0]}")
    for col in cols:
        a, b = j[col].astype(float), j[col + "_pipe"].astype(float)
        bad = ~(np.isclose(a, b, rtol=1e-9, atol=1e-12) | (a.isna() & b.isna()))
        if bad.any(): problems.append(f"{col}: {int(bad.sum())} cells differ from the pipeline")
check(Q1, H1p, ["n_cases", "n_smc_missing", "n_smc_failed", "n_exact_missing", "n_evidence", "bias", "rmse", "median_abs_e", "p90_abs_e", "lb_coverage"])
check(Q2, H2p, ["n_cases", "pct_smc_hpm_eq_exact", "pct_exact_hpm_eq_truth", "pct_smc_hpm_eq_truth"])
check(Q3, H3p, ["n_rb", "n_plain", "rb_mean_max_err", "rb_p90_max_err", "plain_mean_max_err", "plain_p90_max_err", "pct_mpm_rb_eq_exact", "pct_mpm_plain_eq_exact"])

# ---- Q4 recovery: SMC hpm / pip05, EXACT hpm / mpm, benchmark headline + sensitivity rules ----
sel = sel[tf(sel.in_expected)].copy(); sel["scenario"] = sel["scenario"].astype(str)
RULES = [("SMCBVS", "hpm", "SMC-BVS HPM"), ("SMCBVS", "pip05", "SMC-BVS PIP > 0.5 (RB)"), ("EXACT", "hpm", "Exact HPM"), ("EXACT", "mpm", "Exact MPM")]
BENCH = [("F1", "ebic1_K37", "headline"), ("F1", "cv_min", "sensitivity (CV)"), ("F2", "ebic1_K37", "headline"), ("F2", "cv_min", "sensitivity (CV)"),
         ("F3", "ebic1_K37", "headline"), ("F3", "cv_min", "sensitivity (CV)"), ("F4", "ebic1_K37", "headline"), ("F5", "ebic1_K37", "headline"),
         ("A1", "pip05", "headline"), ("A2", "ssl_final", "headline"), ("A3", "ci95", "headline")]
bench_present = bool((sel[sel.method_id.isin([b[0] for b in BENCH])].status != "not_run").any())
q4 = []
for m, r, lab in RULES + [(b[0], b[1], b[2]) for b in BENCH]:
    s = sel[(sel.method_id == m) & (sel.rule_id == r)]
    if len(s) != 2400: problems.append(f"Q4 {m}/{r}: {len(s)} expected-case rows, not 2400")
    for (p, c), g in s.groupby(["p", "scale_key"]):
        row = dict(method_id=m, rule_id=r, label=lab, p=p, scale_key=c)
        for sc in "123456":
            gg = g[g.scenario == sc]; row[f"S{sc}"] = int(tf(gg.exact).sum()); row[f"n_S{sc}"] = len(gg)
            row[f"passing_S{sc}"] = int((tf(gg.exact) & ~tf(gg.diag_flag)).sum())   # passing-only (master IV.1.3), same denominator
        row["pooled"] = int(tf(g.exact).sum()); row["n_pooled"] = len(g)
        row["n_not_run"] = int((g.status == "not_run").sum()); row["n_failed"] = int((g.error_type == "failed").sum())
        row["n_exact_passing"] = int((tf(g.exact) & ~tf(g.diag_flag)).sum())
        q4.append(row)
# SMC MPM from the PLAIN PIPs (not a selection-registry row): from the main-fit accuracy rows (mpm_plain_eq_truth; missing/failed = not recovered).
# Cross-check: the RB MPM there (mpm_rb_eq_truth) must equal the pipeline's SMCBVS/pip05 selection outcome in every case.
pip05 = sel[(sel.method_id == "SMCBVS") & (sel.rule_id == "pip05")].set_index("case_id")
rb_acc = base.set_index("case_id")["mpm_rb_eq_truth"].map(lambda v: str(v).upper() == "TRUE")
if not (rb_acc.reindex(pip05.index) == tf(pip05.exact)).all(): problems.append("RB MPM = truth (accuracy rows) differs from SMCBVS/pip05 selection rows")
smc_flag = sel[(sel.method_id == "SMCBVS") & (sel.rule_id == "hpm")].set_index("case_id").diag_flag
for (p, c), g in base.groupby(["p", "scale_key"]):
    ex = tf(g.mpm_plain_eq_truth); fl = tf(g.case_id.map(smc_flag))
    row = dict(method_id="SMCBVS", rule_id="mpm_plain", label="SMC-BVS PIP > 0.5 (plain)", p=p, scale_key=c)
    for sc in "123456":
        m = (g.scenario == sc).values; row[f"S{sc}"] = int(ex[m].sum()); row[f"n_S{sc}"] = int(m.sum()); row[f"passing_S{sc}"] = int((ex[m] & ~fl[m]).sum())
    row.update(pooled=int(ex.sum()), n_pooled=len(g), n_not_run=0, n_failed=int((g.state != "ok").sum()), n_exact_passing=int((ex & ~fl).sum()))
    q4.append(row)
Q4 = pd.DataFrame(q4)
# check against H4 (in_h4 rows only)
h4 = H4p.copy(); h4["scenario"] = h4["scenario"].astype(str)
for _, x in Q4.iterrows():
    hh = h4[(h4.method_id == x.method_id) & (h4.rule_id == x.rule_id) & (h4.p == x.p) & (h4.scale_key == x.scale_key)]
    if not len(hh): continue
    for sc in "123456":
        v = hh[hh.scenario == sc].n_exact
        if len(v) != 1 or int(v.iloc[0]) != x[f"S{sc}"]: problems.append(f"H4 mismatch {x.method_id}/{x.rule_id} p{x.p} {x.scale_key} S{sc}")
        v = hh[hh.scenario == sc].n_exact_passing
        if len(v) != 1 or int(v.iloc[0]) != x[f"passing_S{sc}"]: problems.append(f"H4 passing mismatch {x.method_id}/{x.rule_id} p{x.p} {x.scale_key} S{sc}")
    v = hh[hh.scenario == "all"].n_exact
    if len(v) != 1 or int(v.iloc[0]) != x.pooled: problems.append(f"H4 pooled mismatch {x.method_id}/{x.rule_id} p{x.p} {x.scale_key}")

# ---- repeat-seed stability (primary + 5 extra seeds = up to 6 fits per case; METRICS.md case_stability) ----
st = roster.merge(stab, on=["case_id"], how="left", suffixes=("", "_s")); st["scenario"] = st["scenario"].astype(str)
sr = []
for p, sc, c, g in cells(st):
    sr.append(dict(p=p, scenario=sc, scale_key=c, n_cases=len(g), n_cases_with_stability=int(g.n_attempted.notna().sum()),
                   fits_attempted=int(g.n_attempted.fillna(0).sum()), fits_completed=int(g.n_completed.fillna(0).sum()),
                   n_sd=int(g.sd_log_Z.notna().sum()), mean_sd_logZ=mean(g.sd_log_Z), median_sd_logZ=float(g.sd_log_Z.median()), p90_sd_logZ=q90(g.sd_log_Z), max_sd_logZ=float(g.sd_log_Z.max()),
                   n_hpm=int(g.hpm_agreement.notna().sum()), pct_cases_all_seeds_same_hpm=pct(g.hpm_agreement == 1, int(g.hpm_agreement.notna().sum())),
                   mean_pairwise_hpm_agreement=mean(g.hpm_agreement), max_n_distinct_hpm=float(g.n_distinct_hpm.max()),
                   mean_max_pip_sd_rb=mean(g.max_pip_sd_rb), p90_max_pip_sd_rb=q90(g.max_pip_sd_rb), max_max_pip_sd_rb=float(g.max_pip_sd_rb.max()),
                   mean_max_pip_sd_plain=mean(g.max_pip_sd_plain), p90_max_pip_sd_plain=q90(g.max_pip_sd_plain), max_max_pip_sd_plain=float(g.max_pip_sd_plain.max())))
STAB = pd.DataFrame(sr)

# ---- repeat fits' own accuracy vs exact (all 12,000 extra-seed fits; context for stability) ----
rp = acc[acc["rep"] > 0].merge(roster[["case_id", "p", "scale_key"]], on="case_id", how="left", suffixes=("_a", ""))
rr = []
for key, g in list(rp.groupby(["p", "scale_key"])) + [(("all", "all"), rp)]:
    n = len(g)
    rr.append(dict(p=key[0], scale_key=key[1], n_fits=n, n_ok=int(tf(g.ok).sum()), n_evidence=int(g.e.notna().sum()), rmse=float(np.sqrt((g.e.dropna() ** 2).mean())),
                   p90_abs_e=q90(g.e.abs()), lb_coverage=float(tf(g.loc[g.e.notna(), "lb_cover"]).mean()), pct_hpm_eq_exact=pct(tf(g.hpm_eq_exact), n),
                   rb_mean_max_err=mean(g.rb_max), plain_mean_max_err=mean(g.plain_max), pct_mpm_rb_eq_exact=pct(tf(g.mpm_rb_eq_exact), n), pct_mpm_plain_eq_exact=pct(tf(g.mpm_plain_eq_exact), n)))
REP = pd.DataFrame(rr)

# ---- reconciliation and availability ----
rec = []
ex_ready = int(tf(ref.drop_duplicates("dataset_id").has_exact).sum()) if "dataset_id" in ref else None
for piece, expected, scored, failed in [
    ("enum (exact, datasets)", 1200, int(tf(ref.drop_duplicates("dataset_id").has_exact).sum()), 0),
    ("smc primary (cases)", 2400, int((base.state == "ok").sum()), int((base.state == "failed").sum())),
    ("smcrep (fits, 5 per case)", 12000, int(tf(acc.loc[acc.rep > 0, "ok"]).sum()), int((~tf(acc.loc[acc.rep > 0, "ok"])).sum()))]:
    rec.append(dict(piece=piece, expected=expected, scored=scored, failed=failed, missing=expected - scored - failed, balances=(expected == scored + failed + (expected - scored - failed))))
REC = pd.DataFrame(rec)
reps_found = acc[acc.rep > 0].groupby("case_id").size()
av = []
for (p, c), g in base.groupby(["p", "scale_key"]):
    av.append(dict(p=p, scale_key=c, n_cases=len(g), smc_ok=int((g.state == "ok").sum()), smc_failed=int((g.state == "failed").sum()), smc_missing=int((g.state == "missing").sum()),
                   exact_ok=int(g.has_exactb.sum()), evidence_ok=int(tf(g.evidence_ok).sum()), hpm_ok=int(tf(g.hpm_ok).sum()), rb_ok=int(tf(g.rb_ok).sum()), plain_ok=int(tf(g.plain_ok).sum()),
                   cases_with_5_repeats=int((g.case_id.map(reps_found).fillna(0) == 5).sum()), repeat_fits_found=int(g.case_id.map(reps_found).fillna(0).sum())))
AV = pd.DataFrame(av)
warnings = [f"reconciliation: {x.piece} has {x.missing} missing/invalid" for _, x in REC.iterrows() if x.missing != 0]

out = dict(problems=problems, warnings=warnings, bench_present=bench_present)
if problems:
    print(json.dumps(out, indent=1)); sys.exit(2)
T.mkdir(parents=True, exist_ok=True)
for df, f in [(Q1, "Q1_logZ.csv"), (Q2, "Q2_hpm.csv"), (Q3, "Q3_pip.csv"), (Q4, "Q4_recovery.csv"), (STAB, "stability.csv"), (REP, "repeat_fit_accuracy.csv"),
              (REC, "reconciliation.csv"), (AV, "availability.csv")]:
    df.to_csv(T / f, index=False, float_format="%.10g")
print(json.dumps(out)); print("BUILD_OK")
