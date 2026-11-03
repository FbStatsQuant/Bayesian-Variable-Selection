"""Draw the tie-out cells (random, seeded) from the built tables and plant canaries (wrong claimed values).

Writes tieout/CLAIMS.csv (what the worker must check) and the canary key to a path given as argv[2]
(kept away from the worker until it reports).
"""
import sys, json, random
from pathlib import Path
import pandas as pd

T = Path(sys.argv[1]); KEY = Path(sys.argv[2]); OUT = T.parent / "tieout"
rng = random.Random(20261030)
head = pd.read_csv(T / "headline_recovery_long.csv", dtype={"scenario": str})
sens = pd.read_csv(T / "all_rules_recovery_long.csv", dtype={"scenario": str})
fpfn = pd.read_csv(T / "error_types_fp_fn.csv", dtype={"scenario": str})
flags = pd.read_csv(T / "smc_diag_flag_rates.csv", dtype={"scenario": str})
pair = pd.read_csv(T / "paired_wins_losses.csv", dtype={"scenario": str})
claims = []

def add(kind, d, quantity, value):
    claims.append(dict(cell_type=kind, quantity=quantity, claimed=value, **d))

# 30 headline exact-recovery cells (per scenario and pooled), stratified so SMC rows are well represented.
smc = head[head.method_id == "SMCBVS"]; oth = head[head.method_id != "SMCBVS"]
for df, n in ((smc, 14), (oth, 16)):
    for i in rng.sample(range(len(df)), n):
        x = df.iloc[i]
        add("exact_count", dict(method_id=x.method_id, rule_id=x.rule_id, scale=x.scale, p=int(x.p), scenario=x.scenario), "exact recoveries (failed/missing = miss)", int(x.exact))
# 4 further rule cells: F1 cv_1se, F4 ebic1_K37 (post hoc at c100, registered primary at c050; the draw gave c050), SSL-RS, SuSiE-refine.
for m, r in (("F1", "cv_1se"), ("F4", "ebic1_K37"), ("SSL-RS", "ssl_final"), ("SuSiE-refine", "pip05")):
    df = sens[(sens.method_id == m) & (sens.rule_id == r)]
    x = df.iloc[rng.randrange(len(df))]
    add("exact_count", dict(method_id=m, rule_id=r, scale=x.scale_key, p=int(x.p), scenario=x.scenario), "exact recoveries (failed/missing = miss)", int(x.exact_all_sum))
# 4 FP/FN / error-type cells.
for q in ("fp_mean", "fn_mean", "err_extra_only", "err_missed_only"):
    x = fpfn.iloc[rng.randrange(len(fpfn))]
    v = round(float(x[q]), 4) if q.endswith("mean") else int(x[q])
    add("error_breakdown", dict(method_id=x.method_id, rule_id=x.rule_id, scale=x.scale_key, p=int(x.p), scenario=x.scenario),
        {"fp_mean": "mean FP over successful fits", "fn_mean": "mean FN over successful fits", "err_extra_only": "fits with all truth + >=1 extra", "err_missed_only": "fits with a strict subset of truth"}[q], v)
# 2 diag_flag cells.
for i in rng.sample(range(len(flags)), 2):
    x = flags.iloc[i]
    add("diag_flag", dict(method_id="SMCBVS", rule_id="hpm", scale=x.scale_key, p=int(x.p), scenario=x.scenario), "fits with diag_flag TRUE", int(x.n_flagged))
# 2 paired cells.
for i in rng.sample(range(len(pair)), 2):
    x = pair.iloc[i]
    add("paired", dict(method_id=f"SMCBVS:{x.smc_rule} vs {x.method_id}:{x.rule_id}", rule_id="", scale=x.scale, p=int(x.p), scenario=x.scenario), "cases where SMC exact and comparator not", int(x.smc_only))
# 2 reconciliation cells.
add("reconciliation", dict(method_id="SMCBVS", rule_id="", scale="all", p=0, scenario="all"), "fits with v3_status resource_limit", 6)
add("reconciliation", dict(method_id="SMCBVS", rule_id="", scale="all", p=0, scenario="all"), "SMC fit bundles (case_ids) present", 2400)

# Plant 5 canaries: perturb claimed values of 5 random cells (exact counts and one FP mean).
idx = rng.sample([i for i, c in enumerate(claims) if c["cell_type"] == "exact_count"], 4)
idx.append(next(i for i, c in enumerate(claims) if c["quantity"] == "mean FP over successful fits"))
key = []
for i in idx:
    c = claims[i]; true = c["claimed"]
    if isinstance(true, float): c["claimed"] = round(true + 0.37, 4)
    else: c["claimed"] = true + rng.choice([-3, -2, -1, 1, 2, 3]) if true >= 3 else true + rng.choice([1, 2, 3])
    key.append(dict(row=i + 1, true=true, planted=c["claimed"]))
df = pd.DataFrame(claims); df.insert(0, "cell_no", range(1, len(df) + 1))
OUT.mkdir(exist_ok=True); df.to_csv(OUT / "CLAIMS.csv", index=False)
KEY.write_text(json.dumps(key, indent=2))
print(len(df), "cells;", len(key), "canaries")
