"""make_bench_claims.py TABLES_DIR ABESS_DIR OUT_DIR KEY_PATH : pass-C (benchmark) tie-out claims. Draws random benchmark recovery cells
(headline rules + CV sensitivity), SMC plain-MPM cells and ABESS size-check cells (seeded), plants 4 canaries, writes OUT_DIR/CLAIMS_BENCH.csv and
the canary key to KEY_PATH (outside every path the worker reads)."""
import sys, json, random
from pathlib import Path
import pandas as pd
T, A, O, KEY = (Path(x) for x in sys.argv[1:5])
rng = random.Random(20261103)
q4 = pd.read_csv(T / "Q4_recovery.csv", dtype={"p": str}); ab = pd.read_csv(A / "abess_size_summary.csv", dtype={"p": str})
RULES = [("F1", "ebic1_K37"), ("F2", "ebic1_K37"), ("F3", "ebic1_K37"), ("F4", "ebic1_K37"), ("F5", "ebic1_K37"), ("A1", "pip05"), ("A2", "ssl_final"), ("A3", "ci95"),
         ("F1", "cv_min"), ("F2", "cv_min"), ("F3", "cv_min")]
claims = []
def rec(m, r, sc=None):
    x = q4[(q4.method_id == m) & (q4.rule_id == r)].reset_index(drop=True).iloc[rng.randrange(4)]
    sc = sc or rng.choice(["1", "2", "3", "4", "5", "6", "all"])
    v = int(x.pooled) if sc == "all" else int(x[f"S{sc}"])
    claims.append(dict(cell_type="recovery", method_id=m, rule_id=r, p=int(x.p), scale_key=x.scale_key, scenario=sc,
                       quantity="exact recoveries of the truth (count over the 100 or 600 expected cases; failed/not-run = not recovered)", claimed=v))
for m, r in RULES: rec(m, r)                                  # one cell per headline/CV rule (11)
for m, r in rng.sample(RULES[:8], 6): rec(m, r, "all")       # 6 pooled cells
for m, r in rng.sample(RULES[:8], 4): rec(m, r, rng.choice(["1", "2"]))   # 4 S1/S2 cells (reported to HQ)
for _ in range(2): rec("SMCBVS", "mpm_plain")
for i in rng.sample(range(4), 2):
    x = ab.iloc[i]
    claims.append(dict(cell_type="abess_size", method_id="F5", rule_id="ebic1_K37", p=int(x.p), scale_key=x.scale_key, scenario="all",
                       quantity="fits whose ebic1_K37 support has centred RSS above the exact best-subset RSS of the same size (rel. tol 1e-8)", claimed=int(x.headline_suboptimal)))
idx = rng.sample(range(len(claims)), 4); key = []
for i in idx:
    c = claims[i]; true = c["claimed"]; c["claimed"] = true + (rng.choice([-3, -2, 2, 3]) if true >= 3 else rng.choice([2, 3]))
    key.append(dict(cell_no=i + 1, true=true, planted=c["claimed"]))
O.mkdir(parents=True, exist_ok=True)
df = pd.DataFrame(claims); df.insert(0, "cell_no", range(1, len(df) + 1)); df.to_csv(O / "CLAIMS_BENCH.csv", index=False)
KEY.parent.mkdir(parents=True, exist_ok=True); KEY.write_text(json.dumps(key, indent=1))
print(len(df), "claims;", len(key), "canaries")
