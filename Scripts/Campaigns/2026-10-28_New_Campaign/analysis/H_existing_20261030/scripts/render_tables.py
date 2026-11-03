"""Render the HEADLINE_H recovery tables (markdown) from tables/all_rules_recovery_long.csv.

Primary rules decide comparisons and ranks; companion rows required by PREREG_c050 R2 (F1-F3 cv_min, cv_1se,
ebic1_K37 side by side) and R4 (SuSiE-refine beside A1) are shown in the same table, plus the other
MCP/ABESS EBIC variant, each with its registry label.
"""
import sys
from pathlib import Path
import pandas as pd

T = Path(sys.argv[1])
a = pd.read_csv(T / "all_rules_recovery_long.csv", dtype={"scenario": str})
SC = ["1", "2", "3", "4", "5", "6", "pooled"]

def rows(scale):
    k37 = "post hoc" if scale == "c100" else "pre-registered primary"
    e1 = "pre-declared primary" if scale == "c100" else "pre-declared, non-primary at c = 0.5"
    refine = ("companion (R4); arm added after the c = 1 results were seen; fit selection by ELBO" if scale == "c100"
              else "companion (R4), pre-registered; fit selection by ELBO")
    mcp_p, mcp_o = (("ebic1", e1), ("ebic1_K37", k37)) if scale == "c100" else (("ebic1_K37", k37), ("ebic1", e1))
    return [("SMCBVS", "hpm", "**SMC-BVS HPM**", "primary"), ("SMCBVS", "pip05", "**SMC-BVS MPM (RB PIP > 0.5)**", "secondary"),
            ("A1", "pip05", "SuSiE", "primary"), ("SuSiE-refine", "pip05", "SuSiE-refine", refine),
            ("A2", "ssl_final", "Spike-and-slab lasso", "primary"), ("A3", "ci95", "Horseshoe (95% CI)", "primary"),
            ("F4", mcp_p[0], f"MCP `{mcp_p[0]}`", mcp_p[1]), ("F4", mcp_o[0], f"MCP `{mcp_o[0]}`", mcp_o[1]),
            ("F5", mcp_p[0], f"ABESS (splicing heuristic) `{mcp_p[0]}`", mcp_p[1]), ("F5", mcp_o[0], f"ABESS (splicing heuristic) `{mcp_o[0]}`", mcp_o[1])] + \
           [(m, r, f"{lab} `{r}`", "primary" if r == "cv_min" else ("companion (R2)" if r == "cv_1se" else f"companion (R2), {k37.replace(' primary', '')}"))
            for m, lab in (("F1", "Lasso"), ("F2", "Elastic net"), ("F3", "Adaptive lasso")) for r in ("cv_min", "cv_1se", "ebic1_K37")]

out = []
for scale, title in (("c100", "c = 1 (strong signal)"), ("c050", "c = 0.5 (weak signal)")):
    out.append(f"### Exact recovery, {title}\n")
    out.append("| Method / rule | role | p500 S1 | S2 | S3 | S4 | S5 | S6 | **/600** | p1000 S1 | S2 | S3 | S4 | S5 | S6 | **/600** |")
    out.append("|---|---|" + "---|" * 14)
    for m, r, lab, role in rows(scale):
        cells = []
        for p in (500, 1000):
            for s in SC:
                x = a[(a.method_id == m) & (a.rule_id == r) & (a.scale_key == scale) & (a.p == p) & (a.scenario == s)]
                assert len(x) == 1, (m, r, scale, p, s)
                v = int(x.exact_all_sum.iloc[0]); cells.append(f"**{v}**" if s == "pooled" else str(v))
        out.append(f"| {lab} | {role} | " + " | ".join(cells) + " |")
    out.append("")
(T / "headline_tables.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
