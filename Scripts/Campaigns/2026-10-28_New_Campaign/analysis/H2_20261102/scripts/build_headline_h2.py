"""build_headline_h2.py -- ANALYSIS-H2 headline recovery tables (D22 scope).

Usage: py -3 build_headline_h2.py SMC_PER_FIT_CSV OUT_DIR

SMC-BVS rows come from the PROD-H rerun per-fit table (HPM, RB-PIP > 0.5, plain-PIP > 0.5; failed / resource_limit fits count as misses).
Benchmark rows come unchanged from analysis/H_existing_20261030/tables/all_rules_recovery_long.csv (same datasets), with the lasso
family (F1 lasso, F2 elastic net) headlined by ebic1_K37 and CV kept as disclosed sensitivity (D35/D42 item 6). Adaptive lasso (F3)
rows come from the BENCH_F3_PROD rerun (lasso cv_min pilot; run 20261102T1252Z_bench_f3v2_prod), scored by scripts/score_f3.R into
tables/f3/f3_new_recovery_long.csv (method id 'F3v2' here); ebic1_K37 headline, CV sensitivity (HQ D86). The superseded ridge-pilot F3 rows
are no longer in the headline (old numbers kept in EVIDENCE_H.md only).
Checks (any failure -> exit 1, nothing written): 2,400 SMC fits, 100 per cell; every benchmark cell has n_expected 100;
rerun HPM and RB-MPM counts equal the 2026-10-23 counts (SMCBVS hpm / pip05 rows of the old table) in every cell.
"""
import sys, json
from pathlib import Path
import pandas as pd

OLD = Path(r"C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H_existing_20261030/tables/all_rules_recovery_long.csv")
ALPHA = Path(r"C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/mgr_checks/f2_alpha_table.csv")
F3NEW = Path(r"C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tables/f3/f3_new_recovery_long.csv")
CELLS = [(p, s) for p in (500, 1000) for s in range(1, 7)]
PEND = "pending F3 rerun (BENCH_F3_PROD)"

# (row label, role, method_id, rule_id per scale {c100, c050}); rule None = pending
ROWS = [
    ("SMC-BVS HPM", "primary", "SMC", {"c100": "hpm", "c050": "hpm"}),
    ("SMC-BVS MPM (RB PIP > 0.5)", "secondary", "SMC", {"c100": "mpm_rb", "c050": "mpm_rb"}),
    ("SMC-BVS MPM (plain PIP > 0.5)", "secondary (new in rerun)", "SMC", {"c100": "mpm_plain", "c050": "mpm_plain"}),
    ("SuSiE", "primary", "A1", {"c100": "pip05", "c050": "pip05"}),
    ("SuSiE-refine", "companion (R4)", "SuSiE-refine", {"c100": "pip05", "c050": "pip05"}),
    ("Spike-and-slab lasso", "primary", "A2", {"c100": "ssl_final", "c050": "ssl_final"}),
    ("Horseshoe (95% CI)", "primary", "A3", {"c100": "ci95", "c050": "ci95"}),
    ("MCP `ebic1`", {"c100": "pre-declared primary", "c050": "pre-declared, non-primary at c = 0.5"}, "F4", {"c100": "ebic1", "c050": "ebic1"}),
    ("MCP `ebic1_K37`", {"c100": "post hoc", "c050": "pre-registered primary"}, "F4", {"c100": "ebic1_K37", "c050": "ebic1_K37"}),
    ("ABESS (splicing heuristic) `ebic1`", {"c100": "pre-declared primary", "c050": "pre-declared, non-primary at c = 0.5"}, "F5", {"c100": "ebic1", "c050": "ebic1"}),
    ("ABESS (splicing heuristic) `ebic1_K37`", {"c100": "post hoc", "c050": "pre-registered primary"}, "F5", {"c100": "ebic1_K37", "c050": "ebic1_K37"}),
    ("Lasso `ebic1_K37`", "headline (D35/D42)", "F1", {"c100": "ebic1_K37", "c050": "ebic1_K37"}),
    ("Elastic net `ebic1_K37`", "headline (D35/D42); α disclosure below", "F2", {"c100": "ebic1_K37", "c050": "ebic1_K37"}),
    ("Adaptive lasso `ebic1_K37`", "headline (D42/D86); lasso cv_min pilot (BENCH_F3_PROD)", "F3v2", {"c100": "ebic1_K37", "c050": "ebic1_K37"}),
]
SENS = [
    ("Lasso `cv_min`", "sensitivity (registered primary before D42)", "F1", "cv_min"),
    ("Lasso `cv_1se`", "sensitivity (R2)", "F1", "cv_1se"),
    ("Elastic net `cv_min`", "sensitivity (registered primary before D42)", "F2", "cv_min"),
    ("Elastic net `cv_1se`", "sensitivity (R2)", "F2", "cv_1se"),
    ("Adaptive lasso `cv_min`", "sensitivity (registered primary before D42)", "F3v2", "cv_min"),
    ("Adaptive lasso `cv_1se`", "sensitivity (R2)", "F3v2", "cv_1se"),
]


def main(smc_csv, out_dir):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    errs = []
    f = pd.read_csv(smc_csv)
    if len(f) != 2400 or f["case_id"].duplicated().any():
        errs.append(f"SMC per-fit rows {len(f)} (want 2400 unique)")
    cnt = f.groupby(["scale_key", "p", "scenario"]).size()
    if not (cnt == 100).all():
        errs.append("SMC cells without 100 fits")
    for c in ("hpm_exact", "mpm_rb_exact", "mpm_plain_exact"):
        f[c] = f[c].astype(str).str.upper().eq("TRUE")
    smc = {r: f.groupby(["scale_key", "p", "scenario"])[c].sum() for r, c in
           (("hpm", "hpm_exact"), ("mpm_rb", "mpm_rb_exact"), ("mpm_plain", "mpm_plain_exact"))}
    old = pd.read_csv(OLD, dtype={"scenario": str})
    old = old[old["scenario"].str.isdigit()].copy()          # drop the 'pooled' rows; pooled totals are recomputed from the cells
    old["scenario"] = old["scenario"].astype(int); old["p"] = old["p"].astype(int)
    ob = old.set_index(["method_id", "rule_id", "scale_key", "p", "scenario"])
    # reproduction of the headline counts
    for r_new, r_old in (("hpm", "hpm"), ("mpm_rb", "pip05")):
        for sc in ("c100", "c050"):
            for p, s in CELLS:
                a = int(smc[r_new].get((sc, p, s), -1)); b = int(ob.loc[("SMCBVS", r_old, sc, p, s), "exact_all_sum"])
                if a != b:
                    errs.append(f"SMC {r_new} {sc} p{p} S{s}: rerun {a} vs 10-23 {b}")
    long = []

    f3 = pd.read_csv(F3NEW).set_index(["rule_id", "scale_key", "p", "scenario"])
    if len(f3) != 6 * 2 * 12 or not (f3["n"] == 100).all():
        errs.append("F3v2 table not 6 rules x 24 cells x 100")

    def cell(method, rule, sc, p, s):
        if method == "SMC":
            return int(smc[rule].get((sc, p, s)))
        if method == "F3v2":
            return int(f3.loc[(rule, sc, p, s), "exact"])
        row = ob.loc[(method, rule, sc, p, s)]
        if int(row["n_expected"]) != 100:
            errs.append(f"{method} {rule} {sc} p{p} S{s}: n_expected {row['n_expected']}")
        return int(row["exact_all_sum"])

    for label, role, m, rules in ROWS:
        for sc in ("c100", "c050"):
            rl = role[sc] if isinstance(role, dict) else role
            for p, s in CELLS:
                rule = rules[sc]
                v = cell(m, rule, sc, p, s) if rule else None
                long.append(dict(table="headline", label=label, role=rl, method_id=m, rule_id=rule or "pending", scale_key=sc, p=p, scenario=s,
                                 recovered=v, n=100))
    for label, role, m, rule in SENS:
        for sc in ("c100", "c050"):
            for p, s in CELLS:
                long.append(dict(table="sensitivity", label=label, role=role, method_id=m, rule_id=rule, scale_key=sc, p=p, scenario=s,
                                 recovered=cell(m, rule, sc, p, s), n=100))
    L = pd.DataFrame(long)
    al = pd.read_csv(ALPHA)
    if len(al) != 24 or not (al["n"] == 100).all():
        errs.append("alpha table not 24 cells x 100")
    if errs:
        print("BUILD FAILED:\n  " + "\n  ".join(errs)); sys.exit(1)
    L.to_csv(out / "headline_h2_long.csv", index=False)
    al.to_csv(out / "f2_alpha_disclosure.csv", index=False)
    # render
    md = []
    for title, tab in (("headline", "Exact recovery"), ("sensitivity", "Sensitivity rows")):
        for sc, nm in (("c100", "c = 1 (strong signal)"), ("c050", "c = 0.5 (weak signal)")):
            sub = L[(L.table == title) & (L.scale_key == sc)]
            md.append(f"#### {tab}, {nm}\n")
            md.append("| Method / rule | role | p500 S1 | S2 | S3 | S4 | S5 | S6 | **/600** | p1000 S1 | S2 | S3 | S4 | S5 | S6 | **/600** |")
            md.append("|---|---|" + "---|" * 14)
            for label in dict.fromkeys(sub.label):
                r = sub[sub.label == label]
                cells = []
                for p in (500, 1000):
                    rr = r[r.p == p].sort_values("scenario")
                    if rr["recovered"].isna().any():
                        cells += ["pending"] * 6 + ["**pending**"]
                    else:
                        v = rr["recovered"].astype(int).tolist(); cells += [str(x) for x in v] + [f"**{sum(v)}**"]
                bold = label.startswith("SMC-BVS")
                lab = f"**{label}**" if bold else label
                role = r["role"].iloc[0] + (f"; {PEND}" if r["recovered"].isna().any() else "")
                md.append(f"| {lab} | {role} | " + " | ".join(cells) + " |")
            md.append("")
    (out / "headline_h2_tables.md").write_text("\n".join(md), encoding="utf-8")
    smc_tot = {(r, sc, p): int(smc[r].xs((sc, p), level=(0, 1)).sum()) for r in smc for sc in ("c100", "c050") for p in (500, 1000)}
    json.dump({"checks": "pass", "smc_pooled": {f"{r}|{sc}|p{p}": v for (r, sc, p), v in smc_tot.items()}}, open(out / "build_checks_h2.json", "w"), indent=1)
    print("BUILD OK"); print(json.dumps({f"{r}|{sc}|p{p}": v for (r, sc, p), v in smc_tot.items()}, indent=0))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
