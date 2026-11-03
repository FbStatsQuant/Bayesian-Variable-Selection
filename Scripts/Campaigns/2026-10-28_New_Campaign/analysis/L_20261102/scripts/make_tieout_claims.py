"""make_tieout_claims.py TABLES_DIR EVIDENCE_DIR TIEOUT_DIR KEY_PATH

Draws >= 40 random cells (seeded) from the ANALYSIS-L tables, plants 5 canaries (perturbed claimed values) and writes
TIEOUT_DIR/CLAIMS.csv (what the independent worker must recompute from raw records + exact + truth) and the canary key to KEY_PATH,
which must be outside every path the worker is told to read.
Cells are per (p, scale_key, scenario) with scenario in 1..6 or 'all' (pooled over the six scenarios of that p x scale).
"""
import sys, json, random
from pathlib import Path
import pandas as pd

T, E, O, KEY = (Path(a) for a in sys.argv[1:5])
rng = random.Random(20261102)
q1 = pd.read_csv(T / "Q1_logZ.csv", dtype={"scenario": str, "p": str})
q2 = pd.read_csv(T / "Q2_hpm.csv", dtype={"scenario": str, "p": str})
q3 = pd.read_csv(T / "Q3_pip.csv", dtype={"scenario": str, "p": str})
q4 = pd.read_csv(T / "Q4_recovery.csv", dtype={"p": str})
st = pd.read_csv(T / "stability.csv", dtype={"scenario": str, "p": str})
mc = pd.read_csv(E / "miss_class.csv", dtype={"scenario": str, "p": str})
pi = pd.read_csv(E / "pi0.csv", dtype={"scenario": str, "p": str})
claims = []
def cellrows(df):  # per-p cells only (the overall all/all row is excluded: too costly to recompute and implied by the others)
    return df[(df.p != "all")].reset_index(drop=True)
def add(kind, x, quantity, value, method="SMCBVS", rule=""):
    claims.append(dict(cell_type=kind, method_id=method, rule_id=rule, p=int(x["p"]), scale_key=x["scale_key"], scenario=str(x["scenario"]), quantity=quantity, claimed=value))
def draw(df, n): d = cellrows(df); return [d.iloc[i] for i in rng.sample(range(len(d)), n)]

for x in draw(q1, 4): add("Q1", x, "bias = mean of e = log Zhat - log Z_exact over main fits with evidence", round(float(x.bias), 6))
for x in draw(q1, 3): add("Q1", x, "RMSE of e over main fits with evidence", round(float(x.rmse), 6))
for x in draw(q1, 3): add("Q1", x, "90th percentile (R type 7) of |e|", round(float(x.p90_abs_e), 6))
for x in draw(q1, 2): add("Q1", x, "lower-bound coverage = share of main fits with log Zhat + log(0.05) <= log Z_exact", round(float(x.lb_coverage), 4))
for x in draw(q2, 3): add("Q2", x, "% of expected cases with SMC HPM = exact HPM (as sets)", round(float(x.pct_smc_hpm_eq_exact), 2))
for x in draw(q2, 2): add("Q2", x, "% of expected cases with exact HPM = truth", round(float(x.pct_exact_hpm_eq_truth), 2))
for x in draw(q2, 2): add("Q2", x, "% of expected cases with SMC HPM = truth", round(float(x.pct_smc_hpm_eq_truth), 2))
for x in draw(q3, 3): add("Q3", x, "RB PIP: mean over main fits of max_j |PIPhat_j - PIP_exact_j|", float(f"{x.rb_mean_max_err:.6g}"))
for x in draw(q3, 3): add("Q3", x, "plain PIP: mean over main fits of max_j |PIPhat_j - PIP_exact_j|", float(f"{x.plain_mean_max_err:.6g}"))
for x in draw(q3, 2): add("Q3", x, "plain PIP: 90th percentile (type 7) of the per-fit max error", float(f"{x.plain_p90_max_err:.6g}"))
for x in draw(q3, 2): add("Q3", x, "% of expected cases with RB MPM (PIP > 1/2) = exact MPM", round(float(x.pct_mpm_rb_eq_exact), 2))
q4s = q4[q4.method_id.isin(["SMCBVS", "EXACT"])].reset_index(drop=True)
for i in rng.sample(range(len(q4s)), 6):
    x = q4s.iloc[i]; sc = rng.choice(["1", "2", "3", "4", "5", "6", "all"])
    v = int(x.pooled) if sc == "all" else int(x[f"S{sc}"])
    claims.append(dict(cell_type="Q4", method_id=x.method_id, rule_id=x.rule_id, p=int(x.p), scale_key=x.scale_key, scenario=sc,
                       quantity="exact recoveries of the truth (count; missing/failed = not recovered)", claimed=v))
for x in draw(st, 2): add("stability", x, "mean over cases of sd(log Zhat) across the 6 seeds (primary + 5 extra)", float(f"{x.mean_sd_logZ:.6g}"))
for x in draw(st, 2): add("stability", x, "% of cases whose 6 seeds all give the same HPM", round(float(x.pct_cases_all_seeds_same_hpm), 2))
for x in draw(st, 1): add("stability", x, "mean over cases of max_j sd(RB PIP_j) across the 6 seeds", float(f"{x.mean_max_pip_sd_rb:.6g}"))
for x in draw(mc, 2): add("theory", x, "number of cases with miss_class posterior_miss (SMC HPM != truth and F(truth) <= F(SMC HPM))", int(x.n_posterior_miss))
for x in draw(pi, 1): add("theory", x, "median over cases of pi0(S0)", float(f"{x.pi0_S0_median:.6g}"))
assert len(claims) >= 40, len(claims)

# plant 5 canaries
idx = rng.sample(range(len(claims)), 5); key = []
for i in idx:
    c = claims[i]; true = c["claimed"]
    if isinstance(true, int): c["claimed"] = true + (rng.choice([-3, -2, 2, 3]) if true >= 3 else rng.choice([2, 3]))
    else: c["claimed"] = round(true * 1.25 + (0.01 if abs(true) < 0.04 else 0), 6)
    key.append(dict(cell_no=i + 1, true=true, planted=c["claimed"]))
O.mkdir(parents=True, exist_ok=True)
df = pd.DataFrame(claims); df.insert(0, "cell_no", range(1, len(df) + 1)); df.to_csv(O / "CLAIMS.csv", index=False)
KEY.parent.mkdir(parents=True, exist_ok=True); KEY.write_text(json.dumps(key, indent=1))
print(len(df), "claims;", len(key), "canaries; key at", KEY)
