"""combine_h2.py -- merge ANALYSIS-H2 per-case outputs.

Usage: py -3 combine_h2.py THEORY_NOTD_DIR
  THEORY_NOTD_DIR = theory/rows_notd_new (headline; theory rows on the rerun fits) or theory/rows_notd_old (preview).
Writes (H2 = this analysis folder):
  tables/smc_h2_per_fit.csv           one row per PROD-H fit (extract/fit/*.csv)
  repro/repro_detail.tsv, repro/repro_summary.csv, repro/repro_mismatches.tsv   (extract/repro/*.tsv)
  case_theory_H.csv                   theory rows + TD d=0 columns (sample) + rerun per-fit fields, one row per case
Refuses (exit 1) on duplicate cases, *.err files, or a non-2,400 fit table (unless --partial).
"""
import sys, glob
from pathlib import Path
import pandas as pd

H2 = Path(r"C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102")


def cat(pattern, sep=","):
    fs = sorted(glob.glob(str(pattern)))
    return pd.concat([pd.read_csv(f, sep=sep, dtype=str, keep_default_na=False, na_values=["NA"]) for f in fs], ignore_index=True) if fs else pd.DataFrame()


def main(notd_dir, partial=False):
    errs = []
    for d in (H2 / "extract", Path(notd_dir), H2 / "theory/rows_td0_old"):
        e = glob.glob(str(d / "*.err"))
        if e:
            errs.append(f"{len(e)} .err files in {d}")
    fit = cat(H2 / "extract/fit/*.csv")
    rp = cat(H2 / "extract/repro/*.tsv", sep="\t")
    th = cat(Path(notd_dir) / "*.csv")
    td = cat(H2 / "theory/rows_td0_old/*.csv")
    for nm, df in (("fit", fit), ("theory", th)):
        if df["case_id"].duplicated().any():
            errs.append(f"duplicate case_id in {nm}")
        if not partial and len(df) != 2400:
            errs.append(f"{nm}: {len(df)} rows (want 2400)")
    # hardening (Sol R1 #7): identical case-id sets, 11 unique repro fields per case, TD rows = unique members of the fixed sample
    FIELDS = {"native_status", "fit$log_Z", "fit$log_Z_r", "fit$hpm", "fit$hpm_F", "fit$pip_primary", "fit$pip_r", "fit$mpm", "record$pip", "record$hpm", "record$mpm"}
    if set(fit["case_id"]) != set(th["case_id"]) or set(fit["case_id"]) != set(rp["case_id"]):
        errs.append("case-id sets differ between fit, theory and repro")
    if rp.duplicated(["case_id", "field"]).any() or any(set(g) != FIELDS for _, g in rp.groupby("case_id")["field"]):
        errs.append("repro: not exactly the 11 expected unique fields per case")
    samp = pd.read_csv(H2 / "theory/td0_sample.tsv", sep="\t", dtype=str)
    if len(td) and (td["case_id"].duplicated().any() or not set(td["case_id"]) <= set(samp["case_id"])):
        errs.append("TD rows duplicated or outside the fixed sample")
    if not partial and len(td) != len(samp):
        errs.append(f"TD rows {len(td)} != sample {len(samp)}")
    if errs:
        print("COMBINE FAILED:\n  " + "\n  ".join(errs)); sys.exit(1)
    (H2 / "tables").mkdir(exist_ok=True); (H2 / "repro").mkdir(exist_ok=True)
    fit.sort_values("case_id").to_csv(H2 / "tables/smc_h2_per_fit.csv", index=False)
    rp.to_csv(H2 / "repro/repro_detail.tsv", sep="\t", index=False)
    rp["identical"] = rp["identical"].str.upper().eq("TRUE")
    rp["max_abs_diff"] = pd.to_numeric(rp["max_abs_diff"], errors="coerce")
    s = rp.groupby("field").agg(n_cases=("case_id", "nunique"), n_identical=("identical", "sum"), max_abs_diff=("max_abs_diff", "max")).reset_index()
    s.to_csv(H2 / "repro/repro_summary.csv", index=False)
    rp[~rp["identical"]].to_csv(H2 / "repro/repro_mismatches.tsv", sep="\t", index=False)
    # case_theory_H: theory row (+ TD d=0 columns where sampled) + rerun fields
    tdc = ["case_id"] + [c for c in td.columns if c.startswith("td0_")] + (["theory_secs"] if "theory_secs" in td.columns else [])
    tdx = td[tdc].rename(columns={"theory_secs": "td0_secs"}) if len(td) else pd.DataFrame(columns=["case_id"])
    th = th.drop(columns=[c for c in th.columns if c.startswith("td")] + (["theory_secs"] if "theory_secs" in th.columns else []), errors="ignore")
    keep = ["case_id", "native_status", "hpm", "hpm_k", "hpm_fp", "hpm_fn", "hpm_exact", "mpm_rb_exact", "mpm_plain_exact", "mpm_rb_eq_plain",
            "pip_rb_plain_maxabs", "pip_rb_plain_n_side", "escalated", "tier", "runtime_s", "reg_mode", "reg_n_distinct_hll",
            "reg_n_distinct_hll_after_cal", "score_fresh_total", "hpm_prov_phase", "hpm_prov_mech", "ls_centre_eq_truth", "ls_returned_eq_truth",
            "ls_moves", "local_changed", "stop_present"] + [c for c in fit.columns if c.startswith("stop_") and c != "stop_present"]
    ct = th.merge(fit[[c for c in keep if c in fit.columns]].rename(columns=lambda c: c if c == "case_id" else "rerun_" + c), on="case_id", how="left", validate="one_to_one")
    ct = ct.merge(tdx, on="case_id", how="left", validate="one_to_one")
    ct["td0_sampled"] = ct["case_id"].isin(tdx["case_id"])
    ct.sort_values("case_id").to_csv(H2 / "case_theory_H.csv", index=False)
    print(f"fit {len(fit)}  repro rows {len(rp)} ({rp['case_id'].nunique()} cases, {int((~rp['identical']).sum())} mismatching fields)  theory {len(th)}  td0 {len(tdx)}")
    print(s.to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1], partial="--partial" in sys.argv)
