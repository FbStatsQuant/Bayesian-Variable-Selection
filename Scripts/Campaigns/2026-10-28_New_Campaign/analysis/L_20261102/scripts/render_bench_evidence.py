"""render_bench_evidence.py TABLES_DIR ABESS_DIR EVIDENCE_MD : writes (or replaces) the benchmark section of EVIDENCE_L.md between the markers
<!-- BENCH:BEGIN --> and <!-- BENCH:END -->, from tables/Q4_recovery.csv and abess_check/. All numbers come from the CSVs."""
import sys
from pathlib import Path
import pandas as pd
T, A, E = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
q4 = pd.read_csv(T / "Q4_recovery.csv", dtype={"p": str})
MN = {"F1": "Lasso", "F2": "Elastic net", "F3": "Adaptive lasso", "F4": "MCP", "F5": "ABESS", "A1": "SuSiE", "A2": "SSL", "A3": "Horseshoe"}
ROWS = [("SMCBVS", "hpm", "SMC-BVS HPM"), ("SMCBVS", "pip05", "SMC-BVS MPM (RB)"), ("SMCBVS", "mpm_plain", "SMC-BVS MPM (plain)"),
        ("EXACT", "hpm", "Exact-posterior HPM"), ("EXACT", "mpm", "Exact-posterior MPM")] + \
       [(m, r, MN[m]) for m, r in [("F1", "ebic1_K37"), ("F2", "ebic1_K37"), ("F3", "ebic1_K37"), ("F4", "ebic1_K37"), ("F5", "ebic1_K37"), ("A1", "pip05"), ("A2", "ssl_final"), ("A3", "ci95")]] + \
       [(m, "cv_min", f"{MN[m]} (CV sensitivity)") for m in ("F1", "F2", "F3")]
CELLS = [("20", "c100", "p = 20, c = 1"), ("20", "c050", "p = 20, c = 0.5"), ("30", "c100", "p = 30, c = 1"), ("30", "c050", "p = 30, c = 0.5")]
def get(m, r, p, c): x = q4[(q4.method_id == m) & (q4.rule_id == r) & (q4.p == p) & (q4.scale_key == c)]; assert len(x) == 1; return x.iloc[0]
L = ["<!-- BENCH:BEGIN -->", "## Benchmarks at low p (pass C, HQ D92): exact recovery of the truth", "",
     "**Data.** PROD_L_BENCH rev 2, run `20261102T2309Z_lowp_benchres`: 19,200 records (2,400 cases × 8 methods), all accepted by `accept_bench.R`, pulled and verified. "
     "They were scored with the frozen campaign scorer (`code/scoring`, registry derived from `bench_lowp` r2, including the LA-4 low-p overlay). Truth was used in scoring only. "
     "For the 11 benchmark rules below (" + f"{sum(int(get(m, r, p, c).n_pooled) for m, r, _ in ROWS[5:] for p, c, _ in CELLS):,}" + " rule × case results): "
     f"not run {sum(int(get(m, r, p, c).n_not_run) for m, r, _ in ROWS[5:] for p, c, _ in CELLS)}, failed or not run {sum(int(get(m, r, p, c).n_failed) for m, r, _ in ROWS[5:] for p, c, _ in CELLS)}.",
     "",
     "**Rules.** These are the same headline rules as at p ≫ n: F1–F3 (lasso, elastic net, adaptive lasso) `ebic1_K37`, with CV `cv_min` reported as a disclosed sensitivity (D35/D42); F4 MCP and F5 ABESS `ebic1_K37`, their pre-registered primary (D42.4; at p ≤ 30 it equals the cap rows, LA-4 / D17); A1 SuSiE `pip05`, A2 SSL `ssl_final`, A3 horseshoe `ci95`. SMC-BVS MPM (plain) is the plain-PIP > 1/2 set of the primary fit, from `case_smc_accuracy.csv`; its RB counterpart is `pip05`, cross-checked equal to the accuracy-table RB MPM in every case.",
     ""]
for p, c, lab in CELLS:
    L += [f"**{lab}** (count out of 100 per scenario, 600 pooled)", "", "| method | rule | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 |", "|---|---|---|---|---|---|---|---|---|"]
    for m, r, nm in ROWS:
        x = get(m, r, p, c); L.append(f"| {nm} | `{r}` | " + " | ".join(str(int(x[f'S{s}'])) for s in "123456") + f" | **{int(x.pooled)}** |")
    L.append("")
tot = {nm: sum(int(get(m, r, p, c).pooled) for p, c, _ in CELLS) for m, r, nm in ROWS}
ex = tot["Exact-posterior HPM"]
above_exact = [(nm, [lab for p, c, lab in CELLS if int(get(m, r, p, c).pooled) > int(get("EXACT", "hpm", p, c).pooled)]) for m, r, nm in ROWS[5:]]
above_exact = [(nm, cells) for nm, cells in above_exact if cells]
near0 = [nm for m, r, nm in ROWS[5:] if tot[nm] < 0.05 * 2400]
L += ["**Flags (reported, not interpreted; HQ decides on any audit).**"]
for nm, cells in above_exact:
    L.append(f"- {nm} recovers the truth more often than the exact-posterior HPM in: {', '.join(cells)} (pooled {tot[nm]} vs {ex} of 2,400). "
             "The exact posterior is that of the SMC-BVS model, not an oracle, so another prior can recover more often.")
if near0:
    L.append(f"- Near-zero recovery (< 5% of 2,400): {', '.join(f'{nm} ({tot[nm]})' for nm in near0)}. This is the CV behaviour found organic at p ≫ n (BENCH-AUDIT, D42.1); the headline rule is `ebic1_K37`.")
L += ["", "**ABESS exact size-k check (D54.3).** " + (A / "ABESS_LINE.txt").read_text(encoding="utf-8").strip() + " Details: `abess_check/ABESS_CHECK.md`.", "",
      "Per-scenario counts with passing-only columns: `tables/Q4_recovery.csv`. Case-level rows: `score_final_bench/case_selection.csv`.", "<!-- BENCH:END -->"]
txt = E.read_text(encoding="utf-8")
block = "\n".join(L)
if "<!-- BENCH:BEGIN -->" in txt:
    pre, rest = txt.split("<!-- BENCH:BEGIN -->", 1); post = rest.split("<!-- BENCH:END -->", 1)[1]; txt = pre + block + post
else:
    txt = txt.rstrip("\n") + "\n\n" + block + "\n"
E.write_text(txt, encoding="utf-8", newline="\n"); print("benchmark section written;", "flags:", above_exact, near0)
