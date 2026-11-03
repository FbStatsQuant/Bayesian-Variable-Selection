"""make_claims_h2.py -- tie-out claims for ANALYSIS-H2 (Terra recomputes from raw records; >= 40 genuine cells + 5 canaries).

Usage: py -3 make_claims_h2.py KEY_PATH
Writes tieout/CLAIMS.csv (cells with claimed values, canaries indistinguishable) and the canary key to KEY_PATH (kept outside the
worker's paths until the tie-out reports). Every genuine claimed value is read from this analysis's own tables.
"""
import sys, json, random
from pathlib import Path
import pandas as pd

H2 = Path(r"C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102")


def main(key_path):
    L = pd.read_csv(H2 / "tables/headline_h2_long.csv")
    f = pd.read_csv(H2 / "tables/smc_h2_per_fit.csv")
    ct = pd.read_csv(H2 / "case_theory_H.csv")
    rp = pd.read_csv(H2 / "repro/repro_summary.csv")
    cells = []
    add = lambda typ, q, v, **k: cells.append(dict(cell_type=typ, quantity=q, claimed=v, **k))
    H = L[L.table == "headline"]
    g = lambda lab, sc, p, s=None: int(H[(H.label == lab) & (H.scale_key == sc) & (H.p == p) & ((H.scenario == s) if s else True)].recovered.sum())
    # A. SMC recovery counts (rerun records; failed fits = miss)
    for lab, rule in (("SMC-BVS HPM", "hpm"), ("SMC-BVS MPM (RB PIP > 0.5)", "mpm_rb"), ("SMC-BVS MPM (plain PIP > 0.5)", "mpm_plain")):
        for sc, p, s in (("c100", 500, None), ("c050", 1000, None), ("c050", 500, 4), ("c100", 1000, 5), ("c050", 1000, 3)):
            add("smc_recovery", f"exact recoveries, rule {rule} (failed = miss)", g(lab, sc, p, s), method="SMCBVS", rule=rule, scale=sc, p=p, scenario=s or "pooled")
    # B. lasso-family ebic1_K37 headline cells (raw benchmark outputs)
    for lab, m in (("Lasso `ebic1_K37`", "F1"), ("Elastic net `ebic1_K37`", "F2")):
        for sc, p, s in (("c100", 500, 1), ("c100", 1000, None), ("c050", 500, None)):
            add("bench_recovery", "exact recoveries, rule ebic1_K37", g(lab, sc, p, s), method=m, rule="ebic1_K37", scale=sc, p=p, scenario=s or "pooled")
    # C. reproduction (all 2,400 rerun records vs the 2026-10-23 records)
    for fld in ("fit$log_Z", "fit$hpm", "fit$pip_primary", "record$pip", "native_status"):
        add("reproduction", f"cases (of 2400) with identical() {fld}, old vs new", int(rp.loc[rp.field == fld, "n_identical"].iloc[0]), field=fld)
    # D. status / accounting / instrumentation
    add("accounting", "fits with native_status resource_limit", int((f.native_status == "resource_limit").sum()))
    add("accounting", "resource_limit fits whose instrumentation$stop$phase == 'diag'", int(((f.native_status == "resource_limit") & (f.stop_phase == "diag")).sum()))
    for sc, p in (("c100", 1000), ("c050", 500)):
        add("accounting", "fits with fit$flags$escalated TRUE", int(f[(f.scale_key == sc) & (f.p == p)].escalated.astype(str).str.upper().eq("TRUE").sum()), scale=sc, p=p)
    add("registry", "records whose instrumentation$scored$mode == 'hll'", int((f.reg_mode == "hll").sum()))
    add("registry", "records whose instrumentation$scored$first_scored is NULL", int((~f.reg_first_scored_present.astype(str).str.upper().eq("TRUE")).sum()))
    comp = f[f.native_status == "completed"]
    add("local_search", "completed fits with fit$local_search$moves > 0", int((comp.ls_moves > 0).sum()))
    add("local_search", "completed fits whose fit$hpm_provenance$phase == 'pilot'", int((comp.hpm_prov_phase == "pilot").sum()))
    add("local_search", "completed fits whose fit$local_search$centre equals the truth", int(comp.ls_centre_eq_truth.astype(str).str.upper().eq("TRUE").sum()))
    # E. PIP agreement
    add("pip", "completed fits where MPM(RB PIP>0.5) == MPM(plain PIP>0.5) as sets", int(comp.mpm_rb_eq_plain.astype(str).str.upper().eq("TRUE").sum()))
    add("pip", "max over completed fits and variables of |record$pip - record$pip_plain| (4 dp)", round(float(comp.pip_rb_plain_maxabs.max()), 4))
    # F. miss shapes (HPM vs truth, completed non-hits)
    nh = comp[~comp.hpm_exact.astype(str).str.upper().eq("TRUE")]
    shape = lambda x: "superset" if x.hpm_fn == 0 else ("subset" if x.hpm_fp == 0 else ("same_size_swap" if x.hpm_fp == x.hpm_fn else "mixed_size"))
    nh = nh.assign(mshape=nh.apply(shape, axis=1))   # not 'shape': nh.shape is the DataFrame attribute
    for sc, p, sh in (("c100", 500, "superset"), ("c050", 500, "same_size_swap"), ("c050", 1000, "subset"), ("c050", 1000, "mixed_size")):
        add("miss_shape", f"completed non-recovered fits with HPM shape {sh} vs truth", int(((nh.scale_key == sc) & (nh.p == p) & (nh["mshape"] == sh)).sum()), scale=sc, p=p)
    # G. F-based: search misses (F(S0) > F(HPM)) -- needs the scorer
    for sc, p in (("c050", 500), ("c100", 1000)):
        x = ct[(ct.scale_key == sc) & (ct.p == p) & (ct.miss_class.isin(["posterior_miss", "search_miss"]))]
        add("miss_class", "completed non-recovered fits with F(S0) > F(HPM) (search misses)", int((x.miss_class == "search_miss").sum()), scale=sc, p=p)
    # H. S0 strict local maximum under all single flips and swaps (independent check of TD clause c) for named cases
    td = ct[ct.td0_sampled.astype(str).str.upper().eq("TRUE") & ct.td0_complete.notna()]
    pick = list(td[td.miss_class == "hit"].case_id.head(3)) + list(td[td.miss_class == "posterior_miss"].case_id.head(3))
    for cid in pick:
        r = td[td.case_id == cid].iloc[0]
        add("td_clause_c", "is S0 a strict local maximum of F over all single adds, removes and swaps? (TRUE/FALSE)", bool(int(r.td0_literal_at_S0_viol) == 0), case=cid)
    # I. pi0 (rerun the scoring code on named cases; execution check)
    for cid in ("p0500_S1_r001_c100", "p1000_S4_r050_c050"):
        r = ct[ct.case_id == cid].iloc[0]
        add("pi0", "pi0(R1) (4 significant digits)", float(f"{r.pi0_R1:.4g}"), case=cid)
    C = pd.DataFrame(cells)
    C.insert(0, "cell_no", range(1, len(C) + 1))
    # canaries: perturb 5 genuine numeric cells (indistinguishable in CLAIMS.csv)
    rnd = random.Random(20261102)
    numeric = [i for i, v in enumerate(C.claimed) if isinstance(v, (int, float)) and not isinstance(v, bool)]
    can = sorted(rnd.sample(numeric, 5)); key = {}
    for i in can:
        true = C.at[i, "claimed"]; fake = round(true * 1.5, 4) if isinstance(true, float) else int(true) + rnd.choice([-3, -2, 2, 3])
        if fake == true or fake < 0:
            fake = true + 2
        key[int(C.at[i, "cell_no"])] = dict(true=true, planted=fake); C.at[i, "claimed"] = fake
    (H2 / "tieout").mkdir(exist_ok=True)
    C.to_csv(H2 / "tieout/CLAIMS.csv", index=False)
    Path(key_path).write_text(json.dumps(key, indent=1, default=str))
    print(f"{len(C)} cells ({len(C) - 5} genuine + 5 canaries); key -> {key_path}")


if __name__ == "__main__":
    main(sys.argv[1])
