"""Per cell: SMC-BVS HPM / MPM vs the best of the 8 benchmark primaries (from headline_recovery_long.csv)."""
import sys
from pathlib import Path
import pandas as pd
T = Path(sys.argv[1])
h = pd.read_csv(T / "headline_recovery_long.csv", dtype={"scenario": str})
rows = []
for (sc, p, s), g in h.groupby(["scale", "p", "scenario"]):
    b = g[g.method_id != "SMCBVS"].sort_values("exact", ascending=False)
    best = b.iloc[0]; ties = ",".join(b[b.exact == best.exact].method)
    hpm = int(g[(g.method_id == "SMCBVS") & (g.rule_id == "hpm")].exact.iloc[0])
    mpm = int(g[(g.method_id == "SMCBVS") & (g.rule_id == "pip05")].exact.iloc[0])
    rows.append(dict(scale=sc, p=p, scenario=s, smc_hpm=hpm, smc_mpm=mpm, best_benchmark=ties, best_value=int(best.exact),
                     hpm_minus_best=hpm - int(best.exact), hpm_rank_among_9=int((b.exact > hpm).sum()) + 1))
out = pd.DataFrame(rows).sort_values(["scale", "p", "scenario"], ascending=[False, True, True])
out.to_csv(T / "smc_vs_best_benchmark.csv", index=False)
print(out.to_string(index=False))
