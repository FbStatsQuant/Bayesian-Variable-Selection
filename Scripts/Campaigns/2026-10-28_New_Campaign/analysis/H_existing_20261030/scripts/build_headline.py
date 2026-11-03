"""ANALYSIS-H: headline p >> n BVS-vs-truth tables from the 2026-10-28 pipeline outputs (no rescoring).

Reads the two F_analysis pipeline passes (one per p; each pass scored one SMC root and all benchmark rows),
takes SMC rows from the pass that scored that p, checks that benchmark rows agree across passes, and writes CSVs.
Scope (D22): only BVS against the truth. No Z or PIP-accuracy quantities are produced.

Usage: py -3 build_headline.py <F_analysis dir> <out tables dir>
"""
import sys, json
from pathlib import Path
import pandas as pd

FA, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
PASSES = {500: FA / "score_p0500_20261028T1404Z", 1000: FA / "score_p1000_20261028T1404Z"}
SCALES = {"c100": "c = 1", "c050": "c = 0.5"}

# Headline rules: SMC-BVS hpm + pip05 (MPM from RB PIP), the 8 benchmarks' primary rules.
# F4/F5: pre-declared primary ebic1 at c = 1; PREREG_c050 R1 primary ebic1_K37 at c = 0.5.
def headline_rules(scale):
    f45 = "ebic1" if scale == "c100" else "ebic1_K37"
    return [("SMCBVS", "hpm", "SMC-BVS HPM"), ("SMCBVS", "pip05", "SMC-BVS MPM (RB PIP>0.5)"),
            ("A1", "pip05", "SuSiE"), ("A2", "ssl_final", "Spike-and-slab lasso"),
            ("A3", "ci95", "Horseshoe"), ("F1", "cv_min", "Lasso (CV-min)"),
            ("F2", "cv_min", "Elastic net (CV-min)"), ("F3", "cv_min", "Adaptive lasso (CV-min)"),
            ("F4", f45, f"MCP ({f45})"), ("F5", f45, f"ABESS ({f45})")]

def load(name):
    out = {}
    for p, d in PASSES.items():
        out[p] = pd.read_csv(d / "results" / name, dtype={"scenario": str})
    return out

er = load("exact_recovery_long.csv")
keys = ["method_id", "rule_id", "scale_key", "p", "scenario"]
# Explicit expected key set: every registered/derived rule of every method, both scales, both p, S1..S6 + pooled.
RULES = {"SMCBVS": ["hpm", "pip05"], "A1": ["bfdr10", "cslead", "pip05"], "A2": ["ssl_final"], "A3": ["ci95", "km2"],
         **{m: ["cv_1se", "cv_min", "ebic05", "ebic05_K37", "ebic1", "ebic1_K37"] for m in ("F1", "F2", "F3")},
         **{m: ["bic", "bic_K37", "ebic05", "ebic05_K37", "ebic1", "ebic1_K37", "ebic1_lam005"] for m in ("F4", "F4_SCAD")},
         "F5": ["bic", "bic_K37", "ebic05", "ebic05_K37", "ebic1", "ebic1_K37", "sic_smax"],
         "SSL-RS": ["ssl_final"], "SuSiE-L100": ["pip05"], "SuSiE-refine": ["bfdr10", "cslead", "pip05"]}
SCN = ["1", "2", "3", "4", "5", "6", "pooled"]
EXPECTED = {(m, r, sc, p, s) for m, rs in RULES.items() for r in rs for sc in SCALES for p in PASSES for s in SCN}
checks = {}
STAGED = {}  # every output is staged here and written only after all checks pass
# All checks run before any file is written.
for p in PASSES:
    assert list(er[p].columns) == list(er[500].columns), "schemas differ between passes"
    assert not er[p].duplicated(keys).any(), f"duplicate keys in pass p{p}"
    got = set(map(tuple, er[p][keys].astype({"p": int}).values.tolist()))
    assert got == EXPECTED, f"pass p{p} key set: missing {sorted(EXPECTED - got)[:5]}, extra {sorted(got - EXPECTED)[:5]}"
    other = er[p][(er[p].method_id == "SMCBVS") & (er[p].p != p)]
    assert set(map(tuple, other[keys].values.tolist())) == {k for k in EXPECTED if k[0] == "SMCBVS" and k[3] != p}, "wrong-pass key set"
    checks[f"pass_p{p}_other_p_smc_all_missing"] = bool((other.n_missing == other.n_expected).all())
    assert checks[f"pass_p{p}_other_p_smc_all_missing"], f"pass p{p} saw SMC rows for the other p"
    mine = er[p][(er[p].method_id == "SMCBVS") & (er[p].p == p)]
    checks[f"pass_p{p}_own_smc_missing"] = int(mine[mine.scenario != "pooled"].n_missing.sum())
# SMC rows from the pass that scored that p; benchmark rows must agree between passes in every saved column.
smc = pd.concat([er[p][(er[p].method_id == "SMCBVS") & (er[p].p == p)] for p in PASSES])
bench = {p: er[p][er[p].method_id != "SMCBVS"].sort_values(keys).reset_index(drop=True) for p in PASSES}
same = bench[500].equals(bench[1000])
checks.update({"benchmark_rows_equal_across_passes_all_columns": bool(same), "benchmark_rows": int(len(bench[500]))})
assert same, "benchmark rows differ between passes"
allrows = pd.concat([smc, bench[500]], ignore_index=True)
assert set(map(tuple, allrows[keys].values.tolist())) == EXPECTED and len(allrows) == len(EXPECTED), "combined key set"
assert (allrows[allrows.scenario != "pooled"].n_expected == 100).all() and (allrows[allrows.scenario == "pooled"].n_expected == 600).all(), "denominators"
checks["combined_rows"] = int(len(allrows))
STAGED["all_rules_recovery_long.csv"] = allrows
# 1. Headline recovery table (long + wide).
rows = []
for sc in SCALES:
    for order, (m, r, lab) in enumerate(headline_rules(sc)):
        sub = allrows[(allrows.method_id == m) & (allrows.rule_id == r) & (allrows.scale_key == sc)]
        assert len(sub) == 14, (m, r, sc, len(sub))
        for _, x in sub.iterrows():
            rows.append(dict(order=order, method=lab, method_id=m, rule_id=r, role=x.role, label=x.label, scale=sc,
                             p=int(x.p), scenario=x.scenario, exact=int(x.exact_all_sum), n=int(x.n_expected),
                             n_success=int(x.n_success), n_failed=int(x.n_fail_total), n_missing=int(x.n_missing)))
head = pd.DataFrame(rows)
STAGED["headline_recovery_long.csv"] = head
wide = head.pivot_table(index=["scale", "order", "method", "method_id", "rule_id"], columns=["p", "scenario"], values="exact").reset_index()
wide.columns = ["_".join(str(c) for c in col if c != "").strip("_") if isinstance(col, tuple) else col for col in wide.columns]
wide = wide.sort_values(["scale", "order"], ascending=[False, True]).drop(columns="order")
STAGED["headline_recovery_wide.csv"] = wide
# 2. Sensitivity rows (all other rules incl. cv_1se, *_K37, SCAD, SSL-RS, SuSiE-L100, SuSiE-refine).
hk = {(m, r, sc) for sc in SCALES for m, r, _ in headline_rules(sc)}
sens = allrows[[(a, b, c) not in hk for a, b, c in zip(allrows.method_id, allrows.rule_id, allrows.scale_key)]]
sens_w = sens.pivot_table(index=["scale_key", "method_id", "rule_id", "role", "label"], columns=["p", "scenario"], values="exact_all_sum").reset_index()
sens_w.columns = ["_".join(str(c) for c in col if c != "").strip("_") if isinstance(col, tuple) else col for col in sens_w.columns]
STAGED["sensitivity_rules_wide.csv"] = sens_w
# 3. Error types and FP/FN (successful fits), headline rules.
cols = ["method_id", "rule_id", "scale_key", "p", "scenario", "n_expected", "n_success", "err_exact", "err_extra_only",
        "err_missed_only", "err_mixed", "err_failed", "n_missing", "tp_mean", "fp_mean", "fn_mean", "fp_mcse", "fn_mcse"]
fpfn = pd.concat([allrows[(allrows.method_id == m) & (allrows.rule_id == r) & (allrows.scale_key == sc)][cols]
                  for sc in SCALES for m, r, _ in headline_rules(sc)])
STAGED["error_types_fp_fn.csv"] = fpfn
# 4. SMC diag_flag rates (informational, D13) + code counts, from the pass that scored that p.
fl = load("smc_flag_rates.csv")
flags = pd.concat([fl[p][fl[p].p == p] for p in PASSES])
STAGED["smc_diag_flag_rates.csv"] = flags
rg = load("smc_recovery_given_flag.csv")
STAGED["smc_recovery_given_flag.csv"] = pd.concat([rg[p][rg[p].p == p] for p in PASSES])
# 5. Per-fit SMC rows + paired wins/losses vs each headline comparator (same case_id), from joined rows.
use = ["method_id", "rule_id", "scale_key", "p", "scenario", "replicate", "case_id", "dataset_id", "status", "v3_status",
       "diag_flag", "k", "tp", "fp", "fn", "exact", "error_type", "support", "support_audit"]
jr = []
for p, d in PASSES.items():
    j = pd.read_csv(d / "analysis" / "joined_scored_rows.csv", usecols=use, dtype={"support": str, "support_audit": str}, low_memory=False)
    jr.append(j[(j.method_id == "SMCBVS") & (j.p == p)])
    if p == 500:
        benchj = j[j.method_id != "SMCBVS"]
jr = pd.concat(jr)
STAGED["smc_per_fit.csv"] = jr
checks["smc_fit_rows"] = int(len(jr))
checks["smc_cases"] = int(jr.case_id.nunique())

pair = []
for sc in SCALES:
    for m, r, lab in headline_rules(sc)[2:]:
        for smcr in ("hpm", "pip05"):
            a = jr[(jr.rule_id == smcr) & (jr.scale_key == sc)][["case_id", "p", "scenario", "exact"]]
            b = benchj[(benchj.method_id == m) & (benchj.rule_id == r) & (benchj.scale_key == sc)][["case_id", "exact"]]
            ab = a.merge(b, on="case_id", how="outer", suffixes=("_smc", "_cmp"), indicator=True, validate="one_to_one")
            assert (ab._merge == "both").all() and len(ab) == 1200, (m, r, sc, len(ab))
            ab["e_s"] = ab.exact_smc.fillna(False).astype(str).str.upper().eq("TRUE")
            ab["e_c"] = ab.exact_cmp.fillna(False).astype(str).str.upper().eq("TRUE")
            for (p, s), g in list(ab.groupby(["p", "scenario"])) + [((pp, "pooled"), gg) for pp, gg in ab.groupby("p")]:
                pair.append(dict(scale=sc, smc_rule=smcr, comparator=lab, method_id=m, rule_id=r, p=int(p), scenario=str(s),
                                 n=len(g), both=int((g.e_s & g.e_c).sum()), smc_only=int((g.e_s & ~g.e_c).sum()),
                                 cmp_only=int((~g.e_s & g.e_c).sum()), neither=int((~g.e_s & ~g.e_c).sum())))
STAGED["paired_wins_losses.csv"] = pd.DataFrame(pair)
# 6. Reconciliation: 2,400 fits = completed + resource_limit + other failed + missing.
hp = jr[jr.rule_id == "hpm"]
rec = hp.groupby(["p", "scale_key"]).agg(fits=("case_id", "nunique"),
                                         completed=("v3_status", lambda s: int((s == "completed").sum())),
                                         resource_limit=("v3_status", lambda s: int((s == "resource_limit").sum())),
                                         status_ok=("status", lambda s: int(s.isin(["ok", "warning"]).sum())),
                                         status_failed=("status", lambda s: int((~s.isin(["ok", "warning"])).sum()))).reset_index()
rec["expected"] = 600
rec["missing"] = rec.expected - rec.fits
STAGED["reconciliation.csv"] = rec
stops = hp[hp.v3_status != "completed"][["case_id", "p", "scale_key", "scenario", "replicate", "status", "v3_status", "k", "support", "support_audit"]]
STAGED["resource_limit_fits.csv"] = stops
checks["reconciliation"] = rec.to_dict(orient="records")
# Publication block: reached only if every assertion above passed.
for name, df in STAGED.items():
    df.to_csv(OUT / name, index=False)
(OUT / "build_checks.json").write_text(json.dumps(checks, indent=2, default=str))
print(json.dumps(checks, indent=2, default=str))
