"""evidence_h2.py -- ANALYSIS-H2 theory-evidence tables (THEORY_EXTRACTION_STRATEGY rows; D22 scope: truth-based only).

Usage: py -3 evidence_h2.py
Inputs: case_theory_H.csv and tables/smc_h2_per_fit.csv (combine_h2.py). Outputs: tables/ev_*.csv and tables/evidence_numbers.json.
Definitions:
  Q_f = 4 * N_e * (T + L + 5)  (T21/T27: final-run iid start draws; N_e = 2500 at tier 0, 10000 at tier 1; T = final bridge stages; L = 8).
  Descriptive finite-n iid-intensity bins: Q_f*pi0(S0) >= 1 or < 1. Legacy storage labels 'favourable' and 'masked' denote only these bins;
  they do not assert T22/T27/T38 hypotheses or asymptotic regimes (Sol R2).
  miss class (T21): no_output = native_status != completed; hit = HPM = S0; search_miss = F(S0) > F(HPM); posterior_miss = F(S0) <= F(HPM), HPM != S0.
  miss shape (T03/T07): superset (fn = 0), subset (fp = 0), same_size_swap (fp = fn > 0), mixed_size (fp, fn > 0, fp != fn).
  local-search repair (T37): centre = the production local-search centre; centre in R_d <=> centre has <= d null variables.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

H2 = Path(r"C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102")
T = H2 / "tables"
B = lambda s: s.astype(str).str.upper().eq("TRUE")
num = lambda s: pd.to_numeric(s, errors="coerce")
GRP = ["p", "scale_key"]


def main():
    ct = pd.read_csv(H2 / "case_theory_H.csv", dtype=str)
    pf = pd.read_csv(T / "smc_h2_per_fit.csv", dtype=str)
    assert len(ct) == 2400 and len(pf) == 2400
    assert set(ct["case_id"]) == set(pf["case_id"]), "case-id sets differ"
    d = ct.merge(pf, on="case_id", how="left", suffixes=("", "_pf"), validate="one_to_one")
    for c in ["p", "scenario", "log_pi0_S0", "pi0_R0", "pi0_R1", "pi0_R2", "F_truth", "F_smc_hpm", "truth_minus_smc_hpm", "n_stages_final", "tier",
              "hpm_fp", "hpm_fn", "hpm_k", "runtime_s", "reg_n_distinct_hll", "reg_n_distinct_hll_after_cal", "score_fresh_total",
              "pip_rb_plain_maxabs", "pip_rb_plain_n_side", "log_Z_r_sd_stored", "ls_centre_n_null", "ls_centre_dist", "ls_moves", "t_total"]:
        d[c] = num(d[c])
    for c in ["hpm_exact", "mpm_rb_exact", "mpm_plain_exact", "mpm_rb_eq_plain", "escalated", "ls_centre_eq_truth", "ls_returned_eq_truth", "stop_present",
              "before_local_eq_truth", "after_local_eq_truth"]:
        d[c] = B(d[c])
    out = {}
    completed = d["native_status"].eq("completed")
    # ---------- E1 start mass (T22 + T27; T38(a)/(b))
    d["N_e"] = np.where(d["tier"] == 1, 10000, 2500)
    d["log_Qf"] = np.log(4 * d["N_e"] * (d["n_stages_final"] + 8 + 5))
    d["log_Qf_pi0"] = d["log_Qf"] + d["log_pi0_S0"]
    # descriptive iid-intensity bins only (legacy labels; not the theorems' regimes)
    d["iid_regime"] = np.where(~completed, "no_output", np.where(d["log_Qf_pi0"] >= 0, "favourable", "masked"))
    e1 = d.groupby(GRP + ["scenario"]).agg(n=("case_id", "size"), log10_pi0_S0_median=("log_pi0_S0", lambda x: np.median(x) / np.log(10)),
        log10_pi0_S0_max=("log_pi0_S0", lambda x: np.max(x) / np.log(10)), log10_Qf_pi0_max=("log_Qf_pi0", lambda x: np.nanmax(x) / np.log(10)),
        n_favourable=("iid_regime", lambda x: int((x == "favourable").sum())), pi0_R0_median=("pi0_R0", "median"), pi0_R0_min=("pi0_R0", "min"),
        pi0_R1_median=("pi0_R1", "median"), pi0_R2_median=("pi0_R2", "median"), pi0_R2_min=("pi0_R2", "min"), hpm_recovered=("hpm_exact", "sum")).reset_index()
    e1.to_csv(T / "ev_start_mass.csv", index=False)
    bins = pd.cut(d["pi0_R0"], [0, 0.25, 0.5, 0.75, 0.9, 1.0], include_lowest=True)
    e1b = d.groupby(["scale_key", bins], observed=True).agg(n=("case_id", "size"), recovered=("hpm_exact", "sum")).reset_index().rename(columns={"pi0_R0": "pi0_R0_bin"})
    e1b["rate"] = e1b["recovered"] / e1b["n"]; e1b.to_csv(T / "ev_recovery_by_pi0R0.csv", index=False)
    out["start"] = dict(n_favourable=int((d["iid_regime"] == "favourable").sum()), n_masked=int((d["iid_regime"] == "masked").sum()),
        log10_pi0_S0_overall_max=float(d["log_pi0_S0"].max() / np.log(10)), log10_Qf_pi0_overall_max=float(d["log_Qf_pi0"].max() / np.log(10)),
        pi0_R0_median=float(d["pi0_R0"].median()), pi0_R1_median=float(d["pi0_R1"].median()), pi0_R2_median=float(d["pi0_R2"].median()),
        pi0_R2_min=float(d["pi0_R2"].min()), theory_status=d["theory_status"].value_counts().to_dict())
    # ---------- E2 T37: TD d=0 audit (sample) + local-search trace (all fits)
    s = d[B(d["td0_sampled"])].copy()
    for c in ["td0_literal_add_true_n", "td0_literal_add_true_viol", "td0_literal_add_true_tight", "td0_literal_at_S0_viol", "td0_literal_min_margin",
              "td0_literal_at_S0_minmargin", "td0_literal_add_true_minmargin", "td0_toward_violations", "td0_literal_violations", "td0_scores", "td0_secs"]:
        s[c] = num(s[c])
    s["viol_share"] = s["td0_literal_add_true_viol"] / s["td0_literal_add_true_n"]
    s["holds_strict"] = B(s["td0_literal_holds_strict"]); s["complete"] = B(s["td0_complete"])
    s["S0_local_max"] = s["td0_literal_at_S0_viol"] == 0
    s["sample_reason"] = np.where(s["replicate"].astype(int).isin([1, 25, 50, 75, 100]), "fixed", "c100_miss")
    e2 = s.groupby(GRP + ["scenario", "sample_reason"]).agg(n=("case_id", "size"), complete=("complete", "sum"), holds_strict=("holds_strict", "sum"),
        S0_local_max=("S0_local_max", "sum"), viol_share_median=("viol_share", "median"), viol_share_max=("viol_share", "max"),
        add_true_minmargin_median=("td0_literal_add_true_minmargin", "median"), at_S0_margin_median=("td0_literal_at_S0_minmargin", "median"),
        hpm_recovered=("hpm_exact", "sum")).reset_index()
    e2.to_csv(T / "ev_td0.csv", index=False)
    s[["case_id", "p", "scenario", "scale_key", "sample_reason", "complete", "holds_strict", "S0_local_max", "viol_share", "td0_literal_add_true_minmargin",
       "td0_literal_at_S0_minmargin", "td0_toward_violations", "td0_literal_violations", "hpm_exact", "miss_class"]].to_csv(T / "ev_td0_cases.csv", index=False)
    # toward == literal at d = 0 (no nulls in centres)
    out["td0"] = dict(n=int(len(s)), complete=int(s["complete"].sum()), holds_strict=int(s["holds_strict"].sum()),
        S0_local_max=int(s["S0_local_max"].sum()), toward_eq_literal=bool((s["td0_toward_violations"] == s["td0_literal_violations"]).all()),
        viol_share_median=float(s["viol_share"].median()), core_h=float(s["td0_secs"].sum() / 3600),
        holds_by_scale={k: f"{int(v.sum())}/{len(v)}" for k, v in s.groupby("scale_key")["holds_strict"]},
        S0_localmax_by_scale={k: f"{int(v.sum())}/{len(v)}" for k, v in s.groupby("scale_key")["S0_local_max"]},
        S0_local_max_vs_hit=pd.crosstab(s["S0_local_max"], s["miss_class"]).to_dict())
    c = d[completed].copy()
    c["centre_in_R0"] = c["ls_centre_n_null"] == 0; c["centre_in_R1"] = c["ls_centre_n_null"] <= 1; c["centre_in_R2"] = c["ls_centre_n_null"] <= 2
    c["repaired"] = (~c["ls_centre_eq_truth"]) & c["ls_returned_eq_truth"]
    rows = []
    for (p, sc), g in c.groupby(GRP):
        for lab, m in (("centre = S0", g["ls_centre_eq_truth"]), ("centre in R0 \\ S0", g["centre_in_R0"] & ~g["ls_centre_eq_truth"]),
                       ("centre in R1 \\ R0", g["centre_in_R1"] & ~g["centre_in_R0"]), ("centre in R2 \\ R1", g["centre_in_R2"] & ~g["centre_in_R1"]),
                       ("centre outside R2", ~g["centre_in_R2"])):
            rows.append(dict(p=p, scale_key=sc, centre=lab, n=int(m.sum()), returned_S0=int((m & g["ls_returned_eq_truth"]).sum()),
                             hpm_S0=int((m & g["hpm_exact"]).sum()), moves_median=float(g.loc[m, "ls_moves"].median()) if m.any() else np.nan))
    pd.DataFrame(rows).to_csv(T / "ev_local_search.csv", index=False)
    out["local_search"] = dict(n_completed=int(len(c)), repaired=int(c["repaired"].sum()), centre_eq_S0=int(c["ls_centre_eq_truth"].sum()),
        centre_in_R2_not_S0=int((c["centre_in_R2"] & ~c["ls_centre_eq_truth"]).sum()),
        centre_in_R2_not_S0_returned_S0=int((c["centre_in_R2"] & ~c["ls_centre_eq_truth"] & c["ls_returned_eq_truth"]).sum()),
        returned_ne_hpm=int((c["ls_returned"].fillna("") != c["hpm"].fillna("")).sum()))
    prov = pd.crosstab([c["hpm_exact"], c["hpm_prov_phase"]], c["hpm_prov_mech"]); prov.to_csv(T / "ev_hpm_provenance.csv")
    # ---------- E3 T38: recovery by regime + cost vs p
    e3 = d.groupby(GRP).agg(n=("case_id", "size"), recovered=("hpm_exact", "sum"), escalated=("escalated", "sum"),
        runtime_s_median=("runtime_s", "median"), runtime_s_p90=("runtime_s", lambda x: x.quantile(0.9)), fresh_scores_median=("score_fresh_total", "median"),
        distinct_hll_median=("reg_n_distinct_hll", "median"), distinct_hll_after_cal_median=("reg_n_distinct_hll_after_cal", "median")).reset_index()
    e3.to_csv(T / "ev_cost.csv", index=False)
    cost = {}
    for sc in ("c100", "c050"):
        a = e3[(e3.scale_key == sc)].set_index("p")
        cost[sc] = {k: float(np.log(a.loc[1000, k] / a.loc[500, k]) / np.log(2)) for k in ("runtime_s_median", "fresh_scores_median", "distinct_hll_median")}
    out["cost_exponent_p500_to_p1000"] = cost
    # ---------- E4 T21 miss decomposition
    d["miss"] = np.where(~completed, "no_output", np.where(d["hpm_exact"], "hit", np.where(d["truth_minus_smc_hpm"] > 0, "search_miss", "posterior_miss")))
    e4 = d.groupby(GRP + ["scenario", "miss"]).size().unstack(fill_value=0).reset_index(); e4.to_csv(T / "ev_miss_class.csv", index=False)
    out["miss_class"] = {f"p{p}|{sc}": g["miss"].value_counts().to_dict() for (p, sc), g in d.groupby(GRP)}
    chk = d[completed & (d["miss_class"].notna())]
    out["miss_class_agrees_scorer"] = bool((chk["miss"] == chk["miss_class"]).all())
    # ---------- E5 resource stop vs complete run
    stop_cols = [x for x in d.columns if x.startswith("stop_") and x != "stop_present"]
    d[d["stop_present"] | ~completed][["case_id", "native_status", "tier", "runtime_s", "support_audit", "S0"] + stop_cols].to_csv(T / "ev_stops.csv", index=False)
    out["stops"] = dict(completed=int(completed.sum()), not_completed=int((~completed).sum()), stop_records=int(d["stop_present"].sum()),
        status=d["native_status"].value_counts().to_dict(), escalated=int(d["escalated"].sum()))
    # ---------- E6 T03 / T07 miss shape among posterior misses
    pm = d[d["miss"] == "posterior_miss"].copy()
    pm["shape"] = np.select([pm["hpm_fn"] == 0, pm["hpm_fp"] == 0, pm["hpm_fp"] == pm["hpm_fn"]], ["superset", "subset", "same_size_swap"], "mixed_size")
    pm["gap"] = -pm["truth_minus_smc_hpm"]
    e6 = pm.groupby(GRP + ["shape"]).agg(n=("case_id", "size"), gap_median=("gap", "median"), gap_min=("gap", "min"), gap_max=("gap", "max"),
        fp_median=("hpm_fp", "median"), fn_median=("hpm_fn", "median")).reset_index()
    e6.to_csv(T / "ev_posterior_miss_shape.csv", index=False)
    out["posterior_miss_shape"] = {f"p{p}|{sc}": g["shape"].value_counts().to_dict() for (p, sc), g in pm.groupby(GRP)}
    out["posterior_miss_gap_share_lt_1nat"] = float((pm["gap"] < 1).mean()) if len(pm) else None
    # ---------- E7 T26 / T12: RB vs plain PIP agreement; island spread (stored diagnostic, not accuracy)
    e7 = c.groupby(GRP).agg(n=("case_id", "size"), mpm_rb_eq_plain=("mpm_rb_eq_plain", "sum"), rb_exact=("mpm_rb_exact", "sum"),
        plain_exact=("mpm_plain_exact", "sum"), maxabs_median=("pip_rb_plain_maxabs", "median"), maxabs_p99=("pip_rb_plain_maxabs", lambda x: x.quantile(0.99)),
        maxabs_max=("pip_rb_plain_maxabs", "max"), n_side_gt0=("pip_rb_plain_n_side", lambda x: int((x > 0).sum())),
        island_sd_logZ_median=("log_Z_r_sd_stored", "median")).reset_index()
    e7.to_csv(T / "ev_pip_rb_plain.csv", index=False)
    out["pip"] = dict(mpm_rb_eq_plain=int(c["mpm_rb_eq_plain"].sum()), n=int(len(c)), maxabs_max=float(c["pip_rb_plain_maxabs"].max()),
        rb_only=int((c["mpm_rb_exact"] & ~c["mpm_plain_exact"]).sum()), plain_only=int((~c["mpm_rb_exact"] & c["mpm_plain_exact"]).sum()),
        hpm_eq_mpm_rb_exact_both=int((c["hpm_exact"] & c["mpm_rb_exact"]).sum()))
    # ---------- registry
    reg = dict(mode=d["reg_mode"].value_counts(dropna=False).to_dict(), first_scored_present=int(B(d["reg_first_scored_present"]).sum()),
               log_sum_exp_F_nonNA=int(num(d["reg_log_sum_exp_F"]).notna().sum()))
    mech = [x for x in d.columns if x.startswith("fresh_mech_")]; ph = [x for x in d.columns if x.startswith("fresh_ph_")]
    tot = c[mech].apply(num).sum(); reg["fresh_share_by_mech"] = {k[11:]: float(v / tot.sum()) for k, v in tot.items()}
    tot = c[ph].apply(num).sum(); reg["fresh_share_by_phase"] = {k[9:]: float(v / tot.sum()) for k, v in tot.items()}
    out["registry"] = reg
    d[["case_id", "iid_regime", "log_Qf", "log_Qf_pi0", "miss"]].to_csv(T / "ev_case_derived.csv", index=False)
    json.dump(out, open(T / "evidence_numbers.json", "w"), indent=1, default=str)
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
