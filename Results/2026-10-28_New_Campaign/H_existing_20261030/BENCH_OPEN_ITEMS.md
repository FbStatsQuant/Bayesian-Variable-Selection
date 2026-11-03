# Benchmark open items: state on 2026-10-30 (reported, not fixed)

BS = `ROOT/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019`.

## 1. G9 independent recount, c = 0.5

**State:** the recount matches every number, but its strict verdict, FAIL on one publication defect, has not been formally re-checked since the fix.

**What matched exactly** (`BS/verify/recount/c050/REPORT.md`, `FINAL_G9_VERDICT.csv`):
- all 120,000 case/rule outcomes;
- all 700 paired rows;
- TP/FP/FN, supports and statuses.

**The defect:**
- **What:** for the CV rules of F1–F3, the counts of "selected k > 37" were published as NA. 168 keys, across c = 0.5 and c = 1.
- **The fix:** the scoring thread re-aggregated the tables as v7. Its ledger (`BS/scoring/LEDGER_ENTRY.md`) says "fixed in v7, 168/168 values equal to the recount".
- **Not on file:** a formal re-check by the recounter (planned in `BS/RUNS.md`, "R re-check after S"). The verdict file still says FAIL.

**Effect on these tables:** none. The defect is a flag-count column, not a recovery count. Our pipeline reproduces `combined_c050_v7/rules_long.csv` and `combined_v3_v7/rules_long.csv` cell-for-cell, with types (`published_reproduction.csv`, `cell_and_type_equal = TRUE`).

**To close:** one narrow re-check of the 168 v7 cells against `FLAG_PUBLICATION_DEFECTS.csv`. It is cheap and can be done locally.

## 2. G5 reproduction / disclosure

**State:** NOT CERTIFIED for the frequentist methods. Bayesian methods PASS.

| Methods | Verdict | Evidence |
|---|---|---|
| A1 SuSiE (+L100), A2 SSL (+SSL-RS), A3 horseshoe, SuSiE-refine | PASS; 1,466 reproduction checks, 0 failures | `BS/verify/G5_bayes/REPORT.md`; `BS/RUNS.md` |
| F1–F4 and SCAD | PARTIAL at both scales | `BS/verify/G5_freq/REPORT.md`, `BS/verify/G5_freq/c050/REPORT.md` |
| F5 ABESS | FAIL (search limitation) at both scales | same |

- **F1–F4 and SCAD:** everything that could be measured passed, but G5 is PARTIAL:
  - the original non-primary coefficient vectors were not saved;
  - all-case rule, weight and CV checks pass, and so do sampled primary coefficient checks;
  - for F1–F3, sampled non-primary supports also reproduce (144 comparisons per method at c = 0.5).
- **MCP/SCAD:** the saved-vector checks cover raw `ebic1`, not K37. So the c = 0.5 MCP headline primary (`ebic1_K37`) lacks coefficient-level certification.
- **F5 ABESS:** an independent same-size search finds a lower-RSS subset than ABESS's own:
  - at c = 1, for 7 of 48 sampled primary EBIC1 selections;
  - at c = 0.5, for 109 of 168 sampled selected-rule rows (24 datasets), including 9 of 24 for the `ebic1_K37` primary.

  The EBIC choice over ABESS's saved candidates is computed correctly; the candidates themselves are not globally best.
- **Disclosure needed with any benchmark table:**
  - "the benchmark code is AI-written; frequentist reproduction (G5) is partial, and ABESS fails the search check";
  - `BS/scoring/SUMMARY.md` still carries the "provisional (G5)" banner.

## 3. Full `cv_1se` and K37 rows

**State:** complete. Every registered and derived rule is present at both scales, for all 1,200 datasets. See `tables/all_rules_recovery_long.csv` and `tables/sensitivity_rules_wide.csv`.

- **`cv_1se`, F1–F3:** 0/600 in every p × c cell, except adaptive lasso at p500, c = 1 (9/600).
- **K37 rules:**
  - at c = 1 they are post hoc, labelled as such;
  - at c = 0.5 they are pre-registered (PREREG_c050 R1), and `ebic1_K37` is the F4/F5 primary there.

  F1–F3 capped and uncapped EBIC rules have the same exact-recovery counts in these tables. That does not mean identical selections or error breakdowns: F3 `ebic05` at p1000, c = 1 includes a k = 40 choice, which changes under K37.

## 4. Note on the earlier ad hoc table

`NOTS_BVS/smcbvs_v3_deploy_20261022/F_analysis/HEADLINE_TABLES.md` (2026-10-28, unreviewed) used MCP/ABESS `ebic1` at c = 0.5, where the pre-registered primary is `ebic1_K37`. `HEADLINE_H.md` uses `ebic1_K37`:

| Method, c = 0.5 | p | `ebic1` | `ebic1_K37` |
|---|---|---|---|
| MCP | 500 | 203 | 240 |
| MCP | 1000 | 102 | 192 |
| ABESS | 500 | 254 | 256 |
| ABESS | 1000 | 186 | 214 |

All other cells agree.
