"""analyse_ledger.py -- S-ELS: classification and tables from the per-fit ledger.

Usage: py -3 analyse_ledger.py LEDGER_RAW_PREFIX CASE_THEORY_H_CSV OUT_DIR
  LEDGER_RAW_PREFIX : path prefix of the extract_ledger.R parts (…/ledger_raw.csv -> ledger_raw.csv.part1..3), or a single csv
  CASE_THEORY_H_CSV : H2 case_theory_H.csv (F_truth = F(S0) scored with the fit's frozen scorer, per case)
Writes (small tables only) into OUT_DIR: ledger_per_fit.csv, class_counts.csv, c541_cases.csv, c541_summary.csv,
  c541_reason.csv, strict_same_size_misses.csv, checks.txt, numbers.json.
"""
import glob, json, os, sys
import numpy as np
import pandas as pd

raw_prefix, ctH, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
parts = sorted(glob.glob(raw_prefix + ".part*")) or [raw_prefix]
L = pd.concat([pd.read_csv(p) for p in parts], ignore_index=True).sort_values("case_id").reset_index(drop=True)
assert len(L) == 2400 and L.case_id.is_unique, len(L)
T = pd.read_csv(ctH, usecols=["case_id", "F_truth", "F_smc_hpm", "miss_class", "S0"]).rename(columns={"S0": "S0_h2"})
L = L.merge(T, on="case_id", how="left", validate="1:1")
chk = []
def check(name, ok, detail=""):
    chk.append(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")

TOL = 1e-6   # F ties: scores are doubles from the same C++ scorer; differences below 1e-6 are treated as ties
def sset(s):
    return frozenset() if (not isinstance(s, str) or s == "") else frozenset(int(x) for x in s.split(";"))
for c in ["S0", "S_hat", "S_c", "S_ret", "S_before_local"]:
    L["_" + c] = L[c].map(sset)
check("S0 equals H2 S0", bool((L.S0 == L.S0_h2).all()))
check("H2 F_smc_hpm equals ledger F_hat (non-stopped)", bool(np.nanmax(np.abs(L.F_hat - L.F_smc_hpm)) < 1e-9), f"max diff {np.nanmax(np.abs(L.F_hat - L.F_smc_hpm))}")

ok = L.native_status.eq("completed") & L.F_hat.notna() & L.F_c.notna()
L["fit_ok"] = ok
print("fits not completed / without final ledger:", int((~ok).sum()), L.loc[~ok, ["case_id", "native_status"]].values.tolist())

# --- ledger identities ---
o = L[ok]
check("S_c == hpm_before_local model, F_c == F_before_local (all completed fits)",
      bool((o._S_c == o._S_before_local).all() and np.nanmax(np.abs(o.F_c - o.F_before_local)) < 1e-12))
check("F_hat >= F_c (search never lowers the best)", bool((o.F_hat >= o.F_c - 1e-12).all()))
check("S_hat == S_ret unless equal-F HPM tie change", bool(((o._S_hat == o._S_ret) | (np.abs(o.F_hat - o.F_ret) < 1e-9)).all()),
      f"S_hat!=S_ret in {int((o._S_hat != o._S_ret).sum())}")
check("E3 == (F_hat > F_before_local)", bool((o.E3 == (o.F_hat > o.F_before_local)).all()), f"E3 true in {int(o.E3.sum())}")
check("moves > 0  <=>  E3 (best-improvement path starts at the global best)", bool(((o.ls_moves > 0) == o.E3).all()),
      f"moves>0 in {int((o.ls_moves > 0).sum())}, E3 in {int(o.E3.sum())}")
# F_truth cross-check against the top store
st = o[o.S0_in_store]
check("F_truth == top-store F(S0) where S0 is in the store", bool(np.nanmax(np.abs(st.F_truth - st.S0_store_F)) < 1e-4),
      f"n={len(st)}, max diff {np.nanmax(np.abs(st.F_truth - st.S0_store_F)):.2e}")
hit = o[o._S_hat == o._S0]
check("F_truth == F_hat on exact recoveries", bool(np.nanmax(np.abs(hit.F_truth - hit.F_hat)) < 1e-6),
      f"n={len(hit)}, max diff {np.nanmax(np.abs(hit.F_truth - hit.F_hat)):.2e}")

# --- geometry of S_c relative to S0 ---
L["m_c"] = [len(s0 - c) for s0, c in zip(L._S0, L._S_c)]          # missing truths
L["e_c"] = [len(c - s0) for s0, c in zip(L._S0, L._S_c)]          # extras
L["dist_c"] = L.m_c + L.e_c                                       # |S_c Delta S0|
L["min_moves_c"] = np.maximum(L.m_c, L.e_c)                       # fewest flips/swaps from S_c to S0
L["S0_in_nbhd"] = L.dist_c.between(1, 2) & (L.min_moves_c == 1)   # S0 in N(S_c): add / delete / swap
L["m_hat"] = [len(s0 - c) for s0, c in zip(L._S0, L._S_hat)]
L["e_hat"] = [len(c - s0) for s0, c in zip(L._S0, L._S_hat)]
L["dist_hat"] = L.m_hat + L.e_hat
L["exact"] = L._S_hat == L._S0
L["c_eq_S0"] = L._S_c == L._S0

# --- S0 scored by the fit?  (top store holds the 20,001 best-F models scored) ---
def scored_state(r):
    if not r.fit_ok:
        return "n/a (no final ledger)"
    if r.S0_in_store:
        return "scored (in top store)"
    if r.F_truth > r.store_min_F + 1e-9 and r.store_full:
        return "not scored (F(S0) above store floor, absent)"
    return "undetermined (F(S0) below store floor)"
L["S0_scored_by_fit"] = L.apply(scored_state, axis=1)

# --- task-2 classification ---
def klass(r):
    if not r.fit_ok:
        return "no final ledger (fit stopped at resource_limit)"
    if np.isnan(r.F_truth):
        return "S0 unscored (no F_truth)"
    if r.exact:
        return "exact recovery"
    return "posterior miss" if r.F_truth <= r.F_hat + TOL else "search miss"
L["klass"] = L.apply(klass, axis=1)
L["strict_post_miss"] = (L.klass == "posterior miss") & (L.F_truth < L.F_hat - TOL)
L["tie_post_miss"] = (L.klass == "posterior miss") & ~L.strict_post_miss
L["dF_S0_minus_Sc"] = L.F_truth - L.F_c
L["dF_S0_minus_Shat"] = L.F_truth - L.F_hat

cols = ["case_id", "p", "scale_key", "scenario", "replicate", "s0", "native_status", "klass", "S0_scored_by_fit",
        "k_hat", "F_hat", "F_c", "F_ret", "F_truth", "dF_S0_minus_Sc", "dF_S0_minus_Shat",
        "m_c", "e_c", "dist_c", "min_moves_c", "S0_in_nbhd", "m_hat", "e_hat", "dist_hat",
        "ls_moves", "ls_termination", "local_certified", "local_limit", "ls_n_evaluated", "E1", "E2", "E3",
        "store_min_F", "S0_in_store", "S0_store_F", "S_hat", "S_c", "S_ret", "S0"]
L[cols].to_csv(os.path.join(out, "ledger_per_fit.csv"), index=False, float_format="%.10g")

# ---------------- tables ----------------
def cell(df):
    return df.groupby(["p", "scale_key"]).size()
cc = L.groupby(["p", "scale_key", "klass"]).size().unstack(fill_value=0)
cc.loc[("all", "all"), :] = cc.sum()
cc.to_csv(os.path.join(out, "class_counts.csv"))
by_scen = L[L.scale_key == "c050"].groupby(["p", "scenario", "klass"]).size().unstack(fill_value=0)
by_scen.to_csv(os.path.join(out, "class_counts_c050_by_scenario.csv"))

# --- 541-type: S_c in R2 \ {S0}  (R_d = {U u P : U subset S0, |P| <= d}, i.e. e_c <= d) ---
C = L[L.fit_ok & (L.e_c <= 2) & ~L.c_eq_S0].copy()
def reason(r):
    if r.exact:
        return "E: search returned S0"
    if r.dF_S0_minus_Sc <= TOL:
        return "A: F(S0) <= F(S_c)  (Lemma 0: S0 cannot be on the path; no search could deliver it)"
    # F(S0) > F(S_c): S0 was not the best scored model before the search
    if r.F_truth <= r.F_hat + TOL:
        return "B: F(S_c) < F(S0) <= F(S_hat)  (search climbed to a model at or above S0; posterior miss with E_LS true)"
    # search miss: F(S0) > F(S_hat)
    if r.local_limit:
        return "C1: F(S0) > F(S_hat), search stopped at the move cap l"
    if r.ls_moves == 0:
        return "C2: F(S0) > F(S_c), 0 moves, S_c a certified local max of the 1-flip/swap scan" + ("" if not r.S0_in_nbhd else " (S0 in N(S_c)!?)")
    return "C3: F(S0) > F(S_hat), search moved and ended at a certified local max"
C["reason"] = C.apply(reason, axis=1)
c541_cols = ["case_id", "p", "scale_key", "scenario", "replicate", "m_c", "e_c", "dist_c", "min_moves_c", "S0_in_nbhd",
             "F_c", "F_hat", "F_truth", "dF_S0_minus_Sc", "dF_S0_minus_Shat", "ls_moves", "ls_termination", "local_certified",
             "local_limit", "E3", "S0_scored_by_fit", "klass", "reason"]
C[c541_cols].to_csv(os.path.join(out, "c541_cases.csv"), index=False, float_format="%.10g")

def q(x, qs):
    return {f"q{int(v*100):02d}": float(np.quantile(x, v)) for v in qs}
summ = []
for key, g in list(C.groupby(["p", "scale_key"])) + [(("all", "all"), C)]:
    dF = g.dF_S0_minus_Sc
    summ.append(dict(p=key[0], scale=key[1], n=len(g), n_d1_or_less=int((g.e_c <= 1).sum()),
                     n_E3=int(g.E3.sum()), n_moves_gt0=int((g.ls_moves > 0).sum()),
                     n_exact=int(g.exact.sum()), n_dF_le_0=int((dF <= TOL).sum()), n_dF_gt_0=int((dF > TOL).sum()),
                     dF_min=float(dF.min()), dF_median=float(dF.median()), dF_max=float(dF.max()),
                     dist_median=float(g.dist_c.median()), dist_max=int(g.dist_c.max()),
                     n_S0_in_nbhd=int(g.S0_in_nbhd.sum()), n_within_cap=int((g.min_moves_c <= 10).sum()),
                     n_cert=int(g.local_certified.sum()), n_limit=int(g.local_limit.sum())))
pd.DataFrame(summ).to_csv(os.path.join(out, "c541_summary.csv"), index=False)
rs = C.groupby(["p", "scale_key", "reason"]).size().unstack(fill_value=0)
rs.loc[("all", "all"), :] = rs.sum()
rs.to_csv(os.path.join(out, "c541_reason.csv"))
dist_tab = C.groupby(["dist_c"]).agg(n=("case_id", "size"), dF_med=("dF_S0_minus_Sc", "median"),
                                     n_dF_gt0=("dF_S0_minus_Sc", lambda x: int((x > TOL).sum()))).reset_index()
dist_tab.to_csv(os.path.join(out, "c541_by_distance.csv"), index=False)

# --- referee check: posterior miss with F(S0) > F(S_c) ---
pm = L[L.klass == "posterior miss"]
ref = pm[pm.dF_S0_minus_Sc > TOL]
ref_tab = pd.DataFrame({"posterior_misses": [len(pm)], "with_F_S0_gt_F_Sc": [len(ref)],
                        "of_those_E3": [int(ref.E3.sum())], "of_those_E3_false": [int((~ref.E3).sum())],
                        "of_those_S_c_in_R2": [int(((ref.e_c <= 2)).sum())]})
ref_tab.to_csv(os.path.join(out, "referee_check.csv"), index=False)
ref_by = pm.assign(gt=pm.dF_S0_minus_Sc > TOL).groupby(["p", "scale_key", "gt"]).size().unstack(fill_value=0)
ref_by.to_csv(os.path.join(out, "referee_check_by_cell.csv"))

# --- task 4: strict same-size posterior misses ---
sm = L[L.strict_post_miss & (L.k_hat == L.s0)].copy()
sm["n_swaps"] = sm.e_hat
t4 = sm.groupby(["scale_key", "p", "scenario"]).size().rename("strict_same_size_posterior_misses").reset_index()
allmiss = L[L.klass == "posterior miss"].groupby(["scale_key", "p", "scenario"]).size().rename("posterior_misses").reset_index()
t4 = allmiss.merge(t4, how="left", on=["scale_key", "p", "scenario"]).fillna(0)
t4["strict_same_size_posterior_misses"] = t4.strict_same_size_posterior_misses.astype(int)
sw = sm.groupby(["scale_key", "p", "scenario", "n_swaps"]).size().unstack(fill_value=0)
sw.columns = [f"swaps_{c}" for c in sw.columns]
t4 = t4.merge(sw.reset_index(), how="left", on=["scale_key", "p", "scenario"]).fillna(0)
t4["same_size_not_strict_ties"] = 0
tie_ss = L[L.tie_post_miss & (L.k_hat == L.s0)].groupby(["scale_key", "p", "scenario"]).size()
for i, r in t4.iterrows():
    t4.loc[i, "same_size_not_strict_ties"] = int(tie_ss.get((r.scale_key, r.p, r.scenario), 0))
for c in t4.columns:
    if t4[c].dtype != object and c not in ("p", "scenario"):
        t4[c] = t4[c].astype(int) if c != "scale_key" else t4[c]
t4.to_csv(os.path.join(out, "strict_same_size_misses.csv"), index=False)
sizes = L[L.klass == "posterior miss"].assign(dk=lambda d: d.k_hat - d.s0).groupby(["scale_key", "dk"]).size().unstack(fill_value=0)
sizes.to_csv(os.path.join(out, "post_miss_size_offset.csv"))

# --- misc counters ---
nums = dict(
    n_fits=len(L), n_stopped=int((~L.fit_ok).sum()),
    klass=L.klass.value_counts().to_dict(),
    n_c541=len(C), n_E3_all=int(o.E3.sum()), n_moves_gt0_all=int((o.ls_moves > 0).sum()),
    n_local_limit_all=int(o.local_limit.sum()), n_E1=int(o.E1.sum()), n_E2=int(o.E2.sum()),
    n_c_eq_S0=int(o.assign(z=o._S_c == o._S0).z.sum()),
    n_c541_exact=int(C.exact.sum()),
    n_search_miss=int((L.klass == "search miss").sum()),
    max_F_truth_minus_F_hat_over_misses=float(L.loc[L.klass.isin(["posterior miss", "search miss"]), "dF_S0_minus_Shat"].max()),
    scored_state=L[L.fit_ok & ~L.exact].S0_scored_by_fit.value_counts().to_dict(),
    c541_scored_state=C.S0_scored_by_fit.value_counts().to_dict(),
)
json.dump(nums, open(os.path.join(out, "numbers.json"), "w"), indent=1, default=str)
open(os.path.join(out, "checks.txt"), "w").write("\n".join(chk) + "\n")
print("\n".join(chk)); print(json.dumps(nums, indent=1, default=str))
