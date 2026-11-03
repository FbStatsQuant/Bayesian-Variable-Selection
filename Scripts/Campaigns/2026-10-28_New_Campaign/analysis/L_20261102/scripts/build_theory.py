#!/usr/bin/env python
"""build_theory.py SCORE_DIR OUT_DIR  --  theory evidence tables (ANALYSIS-L, regime L).

Reads roster.csv, case_theory.csv, case_smc_accuracy.csv, case_selection.csv,
case_reference.csv from SCORE_DIR and writes ten CSV tables to OUT_DIR
(pi0, coverage, truth_first, miss_class, td, t21, recovery_by_pi0, cost,
td_vs_outcome, zhat_unbiased).  pandas + numpy only.  No interpretation.

Conventions
- NA is the string "NA" on input and output; logicals TRUE/FALSE.
- Cells: p x scale_key x scenario (1..6), pooled row (scenario = "all") per
  p x scale_key, overall row (p = scale_key = scenario = "all").  Tables 3, 7, 9, 10
  have only the p x scale_key rows and the overall row (scenario = "all").
- n_cases = roster rows in the cell (the expected cases).  Statistic-specific n
  columns say what each statistic is computed over.  pct_* columns are 0-100.
- Main fit = case_smc_accuracy rep 0.
"""
import sys
import os
import itertools
import numpy as np
import pandas as pd


# ----------------------------------------------------------------- helpers
def read(path):
    return pd.read_csv(path, keep_default_na=False, na_values=["NA"])


def B(s):
    """-> pandas nullable boolean from TRUE/FALSE strings or bool."""
    m = {True: True, False: False, "TRUE": True, "FALSE": False,
         "True": True, "False": False}
    return s.map(m).astype("boolean")


def num(s):
    return pd.to_numeric(s, errors="coerce")


def nT(s):
    return int(s.fillna(False).astype(bool).sum())


def nF(s):
    return int((~s.fillna(True).astype(bool)).sum())


def nNA(s):
    return int(s.isna().sum())


def fin(s):
    x = num(s).dropna()
    return x[np.isfinite(x)]


def med(x):
    return float(np.median(x)) if len(x) else np.nan


def q(x, p):
    return float(np.quantile(x, p)) if len(x) else np.nan


def mn(x):
    return float(np.min(x)) if len(x) else np.nan


def mx(x):
    return float(np.max(x)) if len(x) else np.nan


def pct(k, n):
    return 100.0 * k / n if n else np.nan


def tier_label(v):
    if pd.isna(v):
        return "NA"
    try:
        f = float(v)
        if f.is_integer():
            return str(int(f))
        return str(v)
    except (TypeError, ValueError):
        return str(v)


def cells(df, scen=True):
    out = []
    for p in sorted(df["p"].unique()):
        for sk in sorted(df["scale_key"].unique()):
            sub = df[(df["p"] == p) & (df["scale_key"] == sk)]
            if scen:
                for sc in sorted(sub["scenario"].unique()):
                    out.append((p, sk, sc, sub[sub["scenario"] == sc]))
            out.append((p, sk, "all", sub))
    out.append(("all", "all", "all", df))
    return out


def build(df, scen, fn):
    rows = []
    for p, sk, sc, sub in cells(df, scen):
        res = fn(sub)
        if isinstance(res, dict):
            res = [res]
        for r in res:
            d = {"p": p, "scale_key": sk, "scenario": sc, "n_cases": len(sub)}
            d.update(r)
            rows.append(d)
    return pd.DataFrame(rows)


def write(df, out_dir, name):
    for c in df.columns:
        if df[c].dtype == bool:
            df[c] = df[c].map({True: "TRUE", False: "FALSE"})
    df.to_csv(os.path.join(out_dir, name), index=False, na_rep="NA")
    print("%-24s rows=%d cols=%d" % (name, len(df), df.shape[1]))


# -------------------------------------------------------------------- main
def main(score_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    roster = read(os.path.join(score_dir, "roster.csv"))
    theory = read(os.path.join(score_dir, "case_theory.csv"))
    smc = read(os.path.join(score_dir, "case_smc_accuracy.csv"))
    sel = read(os.path.join(score_dir, "case_selection.csv"))
    ref = read(os.path.join(score_dir, "case_reference.csv"))

    assert roster["case_id"].is_unique, "duplicate case_id in roster"
    assert theory["case_id"].is_unique, "duplicate case_id in case_theory"
    assert ref["case_id"].is_unique, "duplicate case_id in case_reference"

    # ---- type conversions
    for c in ["truth_scored"] + [c for c in theory.columns
                                 if c.endswith("_complete") or c.endswith("_holds_strict")]:
        if c in theory.columns:
            theory[c] = B(theory[c])
    for c in ["has_exact", "exact_hpm_eq_truth", "exact_mpm_eq_truth"]:
        ref[c] = B(ref[c])
    for c in ["ok", "hpm_eq_truth", "escalated"]:
        smc[c] = B(smc[c])
    smc["rep"] = num(smc["rep"]).fillna(0).astype(int)

    # ---- master: one row per roster case
    main_fit = smc[smc["rep"] == 0]
    assert main_fit["case_id"].is_unique, "duplicate main fit rows"
    mf = main_fit[["case_id", "ok", "e", "hpm_eq_truth", "runtime_s",
                   "n_distinct_scored", "escalated", "tier"]].copy()
    mf.columns = ["case_id"] + ["m_" + c for c in mf.columns[1:]]
    sm = sel[(sel["method_id"] == "SMCBVS") & (sel["rule_id"] == "hpm")]
    assert sm["case_id"].is_unique, "duplicate SMCBVS/hpm selection rows"
    sm = sm[["case_id", "fp", "fn"]].copy()
    sm.columns = ["case_id", "sel_fp", "sel_fn"]
    th_cols = [c for c in theory.columns
               if c not in ("dataset_id", "p", "scenario", "replicate", "scale_key")]
    df = roster.merge(theory[th_cols], on="case_id", how="left")
    df = df.merge(mf, on="case_id", how="left")
    df = df.merge(sm, on="case_id", how="left")
    df = df.merge(ref[["case_id", "has_exact", "exact_hpm_eq_truth", "log_truth_mass"]]
                  .rename(columns={"log_truth_mass": "ref_log_truth_mass"}),
                  on="case_id", how="left")
    assert len(df) == len(roster)
    for c in ["has_exact", "exact_hpm_eq_truth", "m_ok", "m_hpm_eq_truth", "m_escalated"]:
        df[c] = df[c].astype("boolean")
    df["truth_scored"] = df["truth_scored"].astype("boolean")
    for c in ["pi0_S0", "pi0_R0", "pi0_R1", "pi0_R2", "scored_coverage", "m_e",
              "m_runtime_s", "m_n_distinct_scored", "sel_fp", "sel_fn",
              "ref_log_truth_mass"]:
        df[c] = num(df[c])
    df["p"] = num(df["p"]).astype(int)
    df["scenario"] = num(df["scenario"]).astype(int)

    # ================================================================ 1 pi0
    def f_pi0(sub):
        r = {}
        for qn in ["pi0_S0", "pi0_R0", "pi0_R1", "pi0_R2"]:
            x = fin(sub[qn])
            r["%s_n" % qn] = len(x)
            r["%s_median" % qn] = med(x)
            r["%s_p10" % qn] = q(x, 0.10)
            r["%s_min" % qn] = mn(x)
        s0 = sub["pi0_S0"]
        r["pct_of_cases_pi0_S0_ge_0.5"] = pct(int((s0 >= 0.5).sum()), len(sub))
        r["pct_of_cases_pi0_S0_lt_0.01"] = pct(int((s0 < 0.01).sum()), len(sub))
        return r
    write(build(df, True, f_pi0), out_dir, "pi0.csv")

    # ========================================================== 2 coverage
    def f_cov(sub):
        x = fin(sub["scored_coverage"])
        ts = sub["truth_scored"]
        return {
            "n": len(x), "median": med(x), "p10": q(x, 0.10), "min": mn(x),
            "pct_of_n_ge_0.99": pct(int((x >= 0.99).sum()), len(x)),
            "pct_of_n_ge_0.999": pct(int((x >= 0.999).sum()), len(x)),
            "pct_of_cases_ge_0.99": pct(int((x >= 0.99).sum()), len(sub)),
            "pct_of_cases_ge_0.999": pct(int((x >= 0.999).sum()), len(sub)),
            "truth_scored_n_TRUE": nT(ts), "truth_scored_n_FALSE": nF(ts),
            "truth_scored_n_NA": nNA(ts)}
    write(build(df, True, f_cov), out_dir, "coverage.csv")

    # ======================================================== 3 truth_first
    d3 = df.copy()
    ts = d3["truth_scored"]
    ph = d3["truth_first_phase"].astype(object).where(d3["truth_first_phase"].notna(), "NA")
    me = d3["truth_first_mech"].astype(object).where(d3["truth_first_mech"].notna(), "NA")
    never = ts.eq(False).fillna(False).astype(bool)
    d3["phase_cat"] = np.where(never, "never_scored", ph)
    d3["mech_cat"] = np.where(never, "never_scored", me)

    def f_tf(sub):
        g = sub.groupby(["phase_cat", "mech_cat"]).size().reset_index(name="n")
        g = g.sort_values(["phase_cat", "mech_cat"])
        return [{"truth_first_phase": r.phase_cat, "truth_first_mech": r.mech_cat,
                 "n": int(r.n), "pct_of_cases": pct(int(r.n), len(sub))}
                for r in g.itertuples()]
    write(build(d3, False, f_tf), out_dir, "truth_first.csv")

    # ========================================================= 4 miss_class
    def comp(sub, pre):
        fp, fn = sub["sel_fp"], sub["sel_fn"]
        sup = (fn == 0) & (fp > 0)
        subs = (fp == 0) & (fn > 0)
        swap = (fp == fn) & (fp > 0)
        mixed = (fp != fn) & (fp > 0) & (fn > 0)
        n = len(sub)
        used = int(sup.sum() + subs.sum() + swap.sum() + mixed.sum())
        return {pre + "n": n, pre + "superset": int(sup.sum()),
                pre + "subset": int(subs.sum()),
                pre + "same_size_swap": int(swap.sum()),
                pre + "mixed": int(mixed.sum()),
                pre + "other_or_NA": n - used}

    def f_miss(sub):
        mc = sub["miss_class"]
        r = {"n_hit": int((mc == "hit").sum()),
             "n_search_miss": int((mc == "search_miss").sum()),
             "n_posterior_miss": int((mc == "posterior_miss").sum()),
             "n_NA": int(mc.isna().sum())}
        r.update(comp(sub[mc == "posterior_miss"], "pm_"))
        r.update(comp(sub[mc == "search_miss"], "sm_"))
        return r
    write(build(df, True, f_miss), out_dir, "miss_class.csv")

    # ================================================================== 5 td
    def f_td(sub):
        rows = []
        for d, v in itertools.product([1, 2], ["literal", "toward"]):
            pre = "td%d_%s_" % (d, v)
            comp_ok = sub["td%d_complete" % d].fillna(False).astype(bool)
            sc = sub[comp_ok]
            nc = len(sc)
            viol = num(sc[pre + "violations"])
            mm = fin(sc[pre + "min_margin"])
            r = {"d": d, "variant": v, "n_complete": nc,
                 "pct_holds_strict_of_complete": pct(nT(sc[pre + "holds_strict"]), nc),
                 "total_violations": float(viol.sum()) if nc else np.nan,
                 "cases_with_violation": int((viol >= 1).sum()) if nc else np.nan,
                 "median_min_margin": med(mm), "min_min_margin": mn(mm),
                 "n_min_margin": len(mm)}
            for cl in ["add_true", "remove_extra", "at_S0"]:
                r["viol_" + cl] = float(num(sc[pre + cl + "_viol"]).sum()) if nc else np.nan
            if v == "literal":
                ab = float(num(sc["td%d_literal_viol_ab" % d]).sum()) if nc else np.nan
                sw = float(num(sc["td%d_literal_viol_truthin_swap" % d]).sum()) if nc else np.nan
                r["sum_viol_ab"] = ab
                r["sum_viol_truthin_swap"] = sw
                r["ratio_truthin_swap_to_viol_ab"] = (sw / ab) if (nc and ab > 0) else np.nan
            else:
                r["sum_viol_ab"] = np.nan
                r["sum_viol_truthin_swap"] = np.nan
                r["ratio_truthin_swap_to_viol_ab"] = np.nan
            rows.append(r)
        return rows
    write(build(df, True, f_td), out_dir, "td.csv")

    # ================================================================= 6 t21
    def f_t21(sub):
        n = len(sub)
        p_wrong = pct(n - nT(sub["m_hpm_eq_truth"]), n) / 100.0
        p_no = pct(n - nT(sub["m_ok"]), n) / 100.0
        he = sub["has_exact"].fillna(False).astype(bool)
        lm = sub.loc[he, "ref_log_truth_mass"]
        lm = lm[np.isfinite(lm)]
        e_off = float(np.mean(1.0 - np.exp(lm))) if len(lm) else np.nan
        p_ns = pct(nF(sub["truth_scored"]), n) / 100.0
        bound = p_no + 2.0 * e_off + p_ns if np.isfinite(e_off) else np.nan
        holds = (p_wrong <= bound) if np.isfinite(bound) else np.nan
        return {"p_wrong": p_wrong, "p_no_output": p_no, "n_mass": len(lm),
                "e_mass_off": e_off, "p_never_scored": p_ns,
                "n_truth_scored_na": nNA(sub["truth_scored"]),
                "bound": bound,
                "holds": ("TRUE" if holds else "FALSE") if np.isfinite(bound) else np.nan,
                "slack": bound - p_wrong if np.isfinite(bound) else np.nan}
    write(build(df, True, f_t21), out_dir, "t21.csv")

    # ======================================================= 7 recovery_by_pi0
    # label "missing" (not "NA") so the class is not read back as a missing value
    classes = ["<0.01", "0.01-0.1", "0.1-0.5", ">=0.5", "missing"]
    pc = pd.Series("missing", index=df.index, dtype=object)
    x = df["pi0_S0"]
    pc[x < 0.01] = "<0.01"
    pc[(x >= 0.01) & (x < 0.1)] = "0.01-0.1"
    pc[(x >= 0.1) & (x < 0.5)] = "0.1-0.5"
    pc[x >= 0.5] = ">=0.5"
    d7 = df.copy()
    d7["pi0_class"] = pc

    def f_rec(sub):
        rows = []
        for c in classes:
            s = sub[sub["pi0_class"] == c]
            n = len(s)
            rows.append({"pi0_S0_class": c, "n": n,
                         "n_has_exact": nT(s["has_exact"]),
                         "pct_smc_hpm_eq_truth": pct(nT(s["m_hpm_eq_truth"]), n),
                         "pct_exact_hpm_eq_truth": pct(nT(s["exact_hpm_eq_truth"]), n)})
        return rows
    write(build(d7, False, f_rec), out_dir, "recovery_by_pi0.csv")

    # ================================================================ 8 cost
    tiers = sorted({tier_label(v) for v in df["m_tier"][df["m_ok"].fillna(False).astype(bool)]})
    d8 = df.copy()
    d8["tier_lab"] = d8["m_tier"].map(tier_label)

    def f_cost(sub):
        ok = sub["m_ok"].fillna(False).astype(bool)
        s = sub[ok]
        rt = fin(s["m_runtime_s"])
        nd = fin(s["m_n_distinct_scored"])
        esc = s["m_escalated"]
        r = {"n_ok": len(s), "n_runtime": len(rt),
             "median_runtime_s": med(rt), "p90_runtime_s": q(rt, 0.90),
             "n_n_distinct_scored": len(nd),
             "median_n_distinct_scored": med(nd), "max_n_distinct_scored": mx(nd),
             "pct_escalated_of_ok": pct(nT(esc), int(esc.notna().sum())),
             "n_escalated_NA": nNA(esc)}
        for t in tiers:
            r["n_tier_" + t] = int((s["tier_lab"] == t).sum())
        return r
    write(build(d8, True, f_cost), out_dir, "cost.csv")

    # ======================================================= 9 td_vs_outcome
    def f_tdo(sub):
        rows = []
        for d in [1, 2]:
            h = sub["td%d_toward_holds_strict" % d]
            for lab, mask in [("TRUE", h.eq(True).fillna(False).astype(bool)),
                              ("FALSE", h.eq(False).fillna(False).astype(bool)),
                              ("missing", h.isna())]:
                s = sub[mask]
                mc = s["miss_class"]
                rows.append({"d": d, "td_toward_holds_strict": lab, "n": len(s),
                             "n_hit": int((mc == "hit").sum()),
                             "n_search_miss": int((mc == "search_miss").sum()),
                             "n_posterior_miss": int((mc == "posterior_miss").sum()),
                             "n_miss_class_NA": int(mc.isna().sum())})
        return rows
    write(build(df, False, f_tdo), out_dir, "td_vs_outcome.csv")

    # ======================================================== 10 zhat_unbiased
    has_extra = bool((smc["rep"] > 0).any())
    smc_e = smc[["case_id", "rep", "e"]].copy()
    smc_e["e"] = num(smc_e["e"])

    def msd(e):
        n = len(e)
        if n == 0:
            return n, np.nan, np.nan, np.nan, np.nan
        rel = np.exp(e) - 1.0
        se_rel = float(np.std(rel, ddof=1) / np.sqrt(n)) if n >= 2 else np.nan
        se_e = float(np.std(e, ddof=1) / np.sqrt(n)) if n >= 2 else np.nan
        return n, float(np.mean(e)), se_e, float(np.mean(rel)), se_rel

    def f_z(sub):
        em = fin(sub["m_e"]).to_numpy()
        n, me_, se_e, mr, se_r = msd(em)
        r = {"n_main": n, "mean_e": me_, "se_e": se_e,
             "mean_rel_err": mr, "se_rel_err": se_r}
        if has_extra:
            a = smc_e[smc_e["case_id"].isin(sub["case_id"])]
            ea = fin(a["e"]).to_numpy()
            n2, me2, se_e2, mr2, se_r2 = msd(ea)
            n_extra = int((a["rep"] > 0).sum())
        else:
            n2, me2, se_e2, mr2, se_r2 = 0, np.nan, np.nan, np.nan, np.nan
            n_extra = 0
        r.update({"n_extra_seed_fits": n_extra, "n_all_fits": n2,
                  "all_mean_e": me2, "all_se_e": se_e2,
                  "all_mean_rel_err": mr2, "all_se_rel_err": se_r2})
        return r
    write(build(df, False, f_z), out_dir, "zhat_unbiased.csv")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: py -3 build_theory.py SCORE_DIR OUT_DIR")
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
