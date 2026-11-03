# p ≫ n headline: does each method recover the true model? (existing fits)

n = 200; p = 500 and 1000; scenarios S1–S6; 100 datasets per cell. The truth has 14 variables. A method "recovers" when its selected set equals the true set exactly. Failed fits count as misses.

**Sources.** These tables use the existing 2,400 SMC-BVS v3 fits and the existing benchmark fits, on the same datasets.
- D23 approves a rerun to collect additional outputs. Whether its completed results agree with these tables remains to be checked.
- Original outcomes remain primary. Doubled-allocation retries will be reported separately (D11).

**Scope (D22).** At p ≫ n there is no exact posterior to compare against, so only selection against the truth is reported here.

**Columns.**
- **HPM:** SMC-BVS's highest-probability model.
- **MPM:** variables whose Rao–Blackwellised PIP exceeds 0.5. Plain PIPs are not in these fits; the rerun adds them.
- **Benchmarks:** each of the 8 methods with its registered primary rule. For MCP and ABESS (splicing heuristic) that is EBIC(γ = 1) at c = 1, and EBIC(γ = 1) with the size bound K = 37 at c = 0.5 (pre-registered).

## 1–2. Exact recovery against the truth (count out of 100 per scenario; pooled out of 600)

Comparisons and ranks below use each method's **primary** rule. Companion rows are shown beside them with their registry labels: F1–F3 `cv_1se` and `ebic1_K37` (PREREG_c050 R2), SuSiE-refine (R4), and the other MCP/ABESS EBIC variant.

**Caveat.** The benchmark code is AI-written. Its frequentist reproduction check (G5) is partial, and ABESS fails the independent same-size search check. These caveats qualify the comparisons (§6).

#### Exact recovery, c = 1 (strong signal)

| Method / rule | role | p500 S1 | S2 | S3 | S4 | S5 | S6 | **/600** | p1000 S1 | S2 | S3 | S4 | S5 | S6 | **/600** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **SMC-BVS HPM** | primary | 95 | 96 | 94 | 91 | 89 | 94 | **559** | 95 | 95 | 97 | 93 | 84 | 96 | **560** |
| **SMC-BVS MPM (RB PIP > 0.5)** | secondary | 92 | 97 | 93 | 93 | 90 | 94 | **559** | 94 | 95 | 97 | 94 | 85 | 96 | **561** |
| SuSiE | primary | 99 | 98 | 97 | 95 | 98 | 98 | **585** | 100 | 96 | 98 | 95 | 94 | 99 | **582** |
| SuSiE-refine | companion (R4); arm added after the c = 1 results were seen; fit selection by ELBO | 99 | 98 | 97 | 95 | 98 | 98 | **585** | 100 | 96 | 98 | 95 | 93 | 99 | **581** |
| Spike-and-slab lasso | primary | 99 | 99 | 97 | 84 | 93 | 97 | **569** | 100 | 96 | 98 | 92 | 97 | 99 | **582** |
| Horseshoe (95% CI) | primary | 92 | 98 | 100 | 87 | 98 | 99 | **574** | 91 | 95 | 100 | 91 | 98 | 100 | **575** |
| MCP `ebic1` | pre-declared primary | 39 | 69 | 77 | 44 | 78 | 70 | **377** | 18 | 28 | 60 | 32 | 49 | 48 | **235** |
| MCP `ebic1_K37` | post hoc | 69 | 79 | 77 | 44 | 78 | 70 | **417** | 66 | 74 | 80 | 32 | 69 | 65 | **386** |
| ABESS (splicing heuristic) `ebic1` | pre-declared primary | 66 | 77 | 71 | 26 | 76 | 49 | **365** | 40 | 63 | 76 | 24 | 66 | 54 | **323** |
| ABESS (splicing heuristic) `ebic1_K37` | post hoc | 68 | 77 | 71 | 26 | 76 | 49 | **367** | 63 | 72 | 76 | 24 | 67 | 54 | **356** |
| Lasso `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Lasso `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Lasso `ebic1_K37` | companion (R2), post hoc | 67 | 29 | 2 | 0 | 9 | 4 | **111** | 48 | 28 | 4 | 0 | 5 | 4 | **89** |
| Elastic net `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Elastic net `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Elastic net `ebic1_K37` | companion (R2), post hoc | 48 | 11 | 0 | 0 | 2 | 0 | **61** | 38 | 12 | 0 | 0 | 0 | 0 | **50** |
| Adaptive lasso `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Adaptive lasso `cv_1se` | companion (R2) | 3 | 4 | 0 | 0 | 1 | 1 | **9** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Adaptive lasso `ebic1_K37` | companion (R2), post hoc | 74 | 60 | 26 | 14 | 47 | 26 | **247** | 36 | 27 | 9 | 4 | 11 | 9 | **96** |

#### Exact recovery, c = 0.5 (weak signal)

| Method / rule | role | p500 S1 | S2 | S3 | S4 | S5 | S6 | **/600** | p1000 S1 | S2 | S3 | S4 | S5 | S6 | **/600** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **SMC-BVS HPM** | primary | 79 | 84 | 64 | 25 | 59 | 59 | **370** | 71 | 75 | 67 | 35 | 31 | 61 | **340** |
| **SMC-BVS MPM (RB PIP > 0.5)** | secondary | 74 | 83 | 63 | 18 | 53 | 47 | **338** | 70 | 76 | 63 | 24 | 32 | 56 | **321** |
| SuSiE | primary | 65 | 70 | 34 | 9 | 3 | 39 | **220** | 49 | 57 | 47 | 21 | 0 | 31 | **205** |
| SuSiE-refine | companion (R4), pre-registered; fit selection by ELBO | 66 | 71 | 43 | 17 | 6 | 46 | **249** | 49 | 57 | 49 | 22 | 3 | 32 | **212** |
| Spike-and-slab lasso | primary | 80 | 84 | 53 | 9 | 42 | 35 | **303** | 67 | 64 | 43 | 15 | 28 | 38 | **255** |
| Horseshoe (95% CI) | primary | 74 | 69 | 18 | 0 | 10 | 14 | **185** | 60 | 50 | 11 | 0 | 11 | 4 | **136** |
| MCP `ebic1_K37` | pre-registered primary | 62 | 71 | 42 | 1 | 45 | 19 | **240** | 49 | 59 | 45 | 1 | 20 | 18 | **192** |
| MCP `ebic1` | pre-declared, non-primary at c = 0.5 | 38 | 58 | 42 | 1 | 45 | 19 | **203** | 13 | 26 | 34 | 1 | 18 | 10 | **102** |
| ABESS (splicing heuristic) `ebic1_K37` | pre-registered primary | 67 | 72 | 34 | 4 | 48 | 31 | **256** | 54 | 64 | 42 | 3 | 23 | 28 | **214** |
| ABESS (splicing heuristic) `ebic1` | pre-declared, non-primary at c = 0.5 | 65 | 72 | 34 | 4 | 48 | 31 | **254** | 36 | 55 | 42 | 3 | 22 | 28 | **186** |
| Lasso `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Lasso `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Lasso `ebic1_K37` | companion (R2), pre-registered | 17 | 5 | 0 | 0 | 1 | 1 | **24** | 11 | 3 | 1 | 0 | 0 | 0 | **15** |
| Elastic net `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Elastic net `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Elastic net `ebic1_K37` | companion (R2), pre-registered | 11 | 3 | 0 | 0 | 0 | 0 | **14** | 8 | 2 | 0 | 0 | 0 | 0 | **10** |
| Adaptive lasso `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Adaptive lasso `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Adaptive lasso `ebic1_K37` | companion (R2), pre-registered | 10 | 17 | 1 | 0 | 2 | 6 | **36** | 10 | 2 | 0 | 0 | 0 | 0 | **12** |

Rule effects stated by pre-registration (R7):
- The horseshoe's 95%-CI rule under-selects at weak signals by construction.
- ABESS supports are not polished.

## 3. SMC-BVS: share of datasets where the selected model equals the truth

| | HPM = truth | MPM = truth |
|---|---|---|
| p = 500, c = 1 | 93.2% (559/600) | 93.2% (559/600) |
| p = 1000, c = 1 | 93.3% (560/600) | 93.5% (561/600) |
| p = 500, c = 0.5 | 61.7% (370/600) | 56.3% (338/600) |
| p = 1000, c = 0.5 | 56.7% (340/600) | 53.5% (321/600) |

The Monte Carlo standard error of each pooled share is about 1–2 percentage points.

## 4. Where SMC-BVS wins and where it loses

**c = 0.5 (weak signal): SMC-BVS wins.**
- The HPM is first or tied-first in 11 of 12 scenario cells. The exception is p500 S1, where it is second, one dataset behind the spike-and-slab lasso (79 vs 80).
- Pooled, it leads the best benchmark (spike-and-slab lasso) by 67 datasets at p500 (370 vs 303) and by 85 at p1000 (340 vs 255).
- Paired on the same datasets, against the spike-and-slab lasso:

  | p | only SMC-BVS recovers | only SSL recovers |
  |---|---|---|
  | 500 | 106 | 39 |
  | 1000 | 117 | 32 |

- Against SuSiE, the margin is 178 vs 28 at p500 and 159 vs 24 at p1000.
- Relative to the best benchmark in each cell, the HPM gains in S3, S4 and S6 range from 11 to 23 datasets.

**c = 1 (strong signal): SMC-BVS loses narrowly to the three Bayesian benchmarks.**
- Pooled, it ranks 4th of the 9 methods, behind SuSiE, the spike-and-slab lasso and the horseshoe, at about 93% against 95–97%.
- Paired against SuSiE:

  | p | only SuSiE recovers | only SMC-BVS recovers |
  |---|---|---|
  | 500 | 27 | 1 |
  | 1000 | 25 | 3 |

- Almost every SMC miss adds variables (the truth plus at least one extra); it rarely drops one:

  | p | truth + extras | mixed | misses only | stopped |
  |---|---|---|---|---|
  | 500 | 36 | 4 | 0 | 1 |
  | 1000 | 34 | 3 | 0 | 3 |

  "Mixed" means it both missed and added variables; "stopped" means a `resource_limit` stop.
- The largest gap is p1000 S5: 84 against the horseshoe's 98.

**Against the frequentist primary rules, SMC-BVS wins everywhere.**
- The HPM beats the MCP and ABESS primaries in all 24 scenario cells.
- The CV-min lasso, elastic net and adaptive lasso recover the truth in no dataset. Every CV-min selection adds false positives (30–80 on average), and some also omit true variables.
- Their EBIC-K37 companion rows recover 10–247 of 600; see the tables above.

See `BENCH_FLAGS.md`.

## 5. Accounting and diagnostics

- **2,400 fits = 2,394 completed + 6 stopped + 0 missing.**
  - The 6 stopped fits are `resource_limit` stops, all in S5: p500 c = 1 (1), p1000 c = 1 (3), p1000 c = 0.5 (2).
  - They count as misses in every table above. P5 reruns them with double the allocation (D11).
  - In 3 of the 4 c = 1 stops, the audit-only support saved at the stop equals the truth. It is not counted.
- **All 2,400 fit bundles pass their sha256 check** against the stored hashes (2026-10-30).
- **diag_flag rate (informational only, D13):**

  | p | c = 1 | c = 0.5 |
  |---|---|---|
  | 500 | 5.7% | 1.0% |
  | 1000 | 9.3% | 2.3% |

  Recovery with and without the flag:

  | | flagged fits recovered | unflagged recovery rate |
  |---|---|---|
  | p500, c = 1 | 34/34 | 93% |
  | p1000, c = 1 | 48/56 | 94% |
  | p500, c = 0.5 | 4/6 | 62% |
  | p1000, c = 0.5 | 6/14 | 57% |

## 6. Benchmark caveats

- The benchmark code is AI-written, and the scoring summary is still marked provisional.
- The frequentist benchmark code is not fully certified by its reproduction check (G5):
  - **ABESS fails the independent search check:** a lower-RSS subset of the same size exists for many of its selected models. That alone does not show truth recovery would improve.
  - **MCP, SCAD, lasso, elastic net and adaptive lasso are PARTIAL:** the original non-primary coefficient vectors were not saved. All-case rule, weight and CV checks pass, and so do sampled coefficient checks at the primary point.
  - **MCP at c = 0.5:** the saved-vector checks cover raw `ebic1`, not K37. So its c = 0.5 headline primary (`ebic1_K37`) lacks coefficient-level certification.
- The Bayesian benchmarks (SuSiE, the spike-and-slab lasso, the horseshoe) pass G5.
- The independent recount (G9) matches every recovery outcome.

Details are in `BENCH_OPEN_ITEMS.md`.

## Files

Everything is in `tables/`:
- `headline_tables.md`: the expanded tables above, rendered from `all_rules_recovery_long.csv` by `scripts/render_tables.py`.
- `headline_recovery_long.csv` and `headline_recovery_wide.csv`: the primary and secondary-rule tables used for the headline comparison.
- `all_rules_recovery_long.csv` and `sensitivity_rules_wide.csv`: every rule, including cv_1se, the K = 37 variants, SCAD, SSL-RS, SuSiE-L100 and SuSiE-refine.
- `error_types_fp_fn.csv`: error types and mean FP/FN.
- `paired_wins_losses.csv`: paired wins and losses.
- `smc_vs_best_benchmark.csv`: SMC-BVS against the best benchmark in each cell.
- `smc_diag_flag_rates.csv` and `smc_recovery_given_flag.csv`: diag_flag rates, and recovery with and without the flag.
- `reconciliation.csv` and `resource_limit_fits.csv`: the fit accounting and the 6 stopped fits.
- `smc_per_fit.csv`: one row per SMC-BVS fit.

The tie-out is in `tieout/`; the review is in `review/`.
