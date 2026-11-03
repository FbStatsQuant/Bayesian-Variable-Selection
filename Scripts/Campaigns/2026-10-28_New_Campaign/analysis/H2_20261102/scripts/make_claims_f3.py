"""make_claims_f3.py -- numbers-only tie-out claims for the new adaptive-lasso (F3, BENCH_F3_PROD) rows (HQ D86).
Usage: py -3 make_claims_f3.py KEY_PATH  ->  tieout/F3_CLAIMS.csv (+ 3 canaries; key written to KEY_PATH, outside the worker's paths).
"""
import sys, json, random
from pathlib import Path
import pandas as pd

H2 = Path(r"C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102")
A = pd.read_csv(H2 / "tables/f3/f3_new_recovery_long.csv")
chk = (H2 / "tables/f3/f3_new_checks.txt").read_text()
cells = []
for sc in ("c100", "c050"):
    for p in (500, 1000):
        for s in range(1, 7):
            cells.append(dict(quantity="exact recoveries /100", rule="ebic1_K37", scale=sc, p=p, scenario=s,
                              claimed=int(A[(A.rule_id == "ebic1_K37") & (A.scale_key == sc) & (A.p == p) & (A.scenario == s)].exact.iloc[0])))
for r in ("ebic1_K37", "cv_min", "cv_1se", "ebic1"):
    for sc in ("c100", "c050"):
        for p in (500, 1000):
            cells.append(dict(quantity="exact recoveries /600 (pooled S1-S6)", rule=r, scale=sc, p=p, scenario="pooled",
                              claimed=int(A[(A.rule_id == r) & (A.scale_key == sc) & (A.p == p)].exact.sum())))
ll = {("p0500", "c100"): 260, ("p0500", "c050"): 58, ("p1000", "c100"): 391, ("p1000", "c050"): 95}   # from f3_new_checks.txt (asserted below)
assert "804 / 2400" in chk
for (pp, sc), v in ll.items():
    cells.append(dict(quantity="cv_min rows whose diag_codes contain 'lambda_last' (of 600)", rule="cv_min", scale=sc, p=int(pp[1:]), scenario="pooled", claimed=v))
C = pd.DataFrame(cells); C.insert(0, "cell_no", range(1, len(C) + 1))
rnd = random.Random(86); can = sorted(rnd.sample(range(len(C)), 3)); key = {}
for i in can:
    t = int(C.at[i, "claimed"]); f = t + rnd.choice([-3, -2, 2, 3]); f = f if f >= 0 else t + 2
    key[int(C.at[i, "cell_no"])] = dict(true=t, planted=f); C.at[i, "claimed"] = f
C.to_csv(H2 / "tieout/F3_CLAIMS.csv", index=False)
Path(sys.argv[1]).write_text(json.dumps(key, indent=1))
print(f"{len(C)} cells ({len(C) - 3} genuine + 3 canaries)")
