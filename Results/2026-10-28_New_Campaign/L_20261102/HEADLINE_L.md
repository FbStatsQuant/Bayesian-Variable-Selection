# Regime L (p = 20, 30; n = 200): headline answers

PROD-L run `20261030T1811Z_lowp_prodL`: 1,200 datasets (p ∈ {20, 30}, S1–S6, 100 replicates) × c ∈ {1, 0.5} = 2,400 cases. The exact posterior comes from full enumeration of all 2^p models. Truth was used only in scoring. Reconciliation: enumeration 1200/1,200, SMC primary 2400/2,400, SMC repeats 12000/12,000. Failed: 0. Missing: 0.

## Short answers

1. **Is Ẑ accurate? Yes.** Over the 2,400 primary fits, the error e = log Ẑ − log Z has bias -0.0002, RMSE 0.012, median |e| 0.007, and 90th-percentile |e| 0.020. That is, pooled over all fits, Ẑ is within about 2.1% of Z in 90% of them (the per-cell 90th percentile reaches 0.029, about 3%). The 0.05·Ẑ lower bound covered Z in 100% of fits (0 violations), so the bound is very conservative.
2. **Is the HPM accurate? Yes.** The SMC HPM equals the exact HPM in 100% of cases. The exact HPM equals the truth in 92.3%, and so does the SMC HPM (92.3%). Every SMC miss of the truth is a miss of the exact posterior itself, not of the search.
3. **Are the PIPs accurate? Yes, both kinds.** The per-fit maximum |PIP − exact PIP| has mean 0.0005 for the RB PIP (90th percentile 0.0014), and mean 0.0020 for the plain PIP (90th percentile 0.0033). The MPM equals the exact MPM in 99.9% of cases (RB) and 99.8% (plain). The RB PIPs are about 4× closer.
4. **Recovery (exact recovery of the truth, out of 600 per p × c).** p = 20, c100: SMC-BVS HPM 576; p = 20, c050: SMC-BVS HPM 562; p = 30, c100: SMC-BVS HPM 571; p = 30, c050: SMC-BVS HPM 507. The exact HPM gives identical counts, and the hardest cell is S4 at p = 30, c = 0.5. Pooled over all 2,400 cases, SMC-BVS HPM recovers 2216; the best benchmark under its headline rule is SSL with 2251, then SuSiE (2183) and Adaptive lasso (2066). Benchmarks above SMC-BVS: SSL. Full table in Q4.

## Q1. Ẑ error, e = log Ẑ − log Z (exact)

RMSE of e, per p × c × scenario:

| p, c | S1 | S2 | S3 | S4 | S5 | S6 | pooled |
|---|---|---|---|---|---|---|---|
| 20, c100 | 0.005 | 0.010 | 0.016 | 0.017 | 0.014 | 0.015 | 0.014 |
| 20, c050 | 0.005 | 0.010 | 0.014 | 0.015 | 0.014 | 0.013 | 0.012 |
| 30, c100 | 0.006 | 0.010 | 0.009 | 0.011 | 0.015 | 0.010 | 0.010 |
| 30, c050 | 0.008 | 0.010 | 0.010 | 0.012 | 0.014 | 0.011 | 0.011 |
| **all 2,400** |  |  |  |  |  |  | **0.012** |

90th percentile of |e|:

| p, c | S1 | S2 | S3 | S4 | S5 | S6 | pooled |
|---|---|---|---|---|---|---|---|
| 20, c100 | 0.007 | 0.016 | 0.027 | 0.029 | 0.024 | 0.026 | 0.024 |
| 20, c050 | 0.008 | 0.016 | 0.025 | 0.025 | 0.021 | 0.020 | 0.022 |
| 30, c100 | 0.012 | 0.016 | 0.015 | 0.019 | 0.024 | 0.015 | 0.017 |
| 30, c050 | 0.014 | 0.017 | 0.016 | 0.020 | 0.023 | 0.017 | 0.018 |
| **all 2,400** |  |  |  |  |  |  | **0.020** |

The bias lies between -0.0021 and +0.0030 in every cell, and the median |e| between 0.0030 and 0.0125. The 0.05·Ẑ lower bound had 100% coverage in every cell. Full table: `tables/Q1_logZ.csv`.

## Q2. HPM

% of cases with SMC HPM = exact HPM: **100 in every cell** (2,400/2,400).

% of cases with exact HPM = truth (identical to % SMC HPM = truth in every cell):

| p, c | S1 | S2 | S3 | S4 | S5 | S6 | pooled |
|---|---|---|---|---|---|---|---|
| 20, c100 | 96 | 98 | 97 | 95 | 95 | 95 | 96 |
| 20, c050 | 96 | 97 | 96 | 87 | 92 | 94 | 93.7 |
| 30, c100 | 95 | 95 | 97 | 89 | 97 | 98 | 95.2 |
| 30, c050 | 94 | 91 | 94 | 61 | 86 | 81 | 84.5 |
| **all 2,400** |  |  |  |  |  |  | **92.3** |

Full table: `tables/Q2_hpm.csv`.

## Q3. PIPs against the exact PIPs

Mean per-fit max |PIP − exact PIP|, RB:

| p, c | S1 | S2 | S3 | S4 | S5 | S6 | pooled |
|---|---|---|---|---|---|---|---|
| 20, c100 | 0.0001 | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0001 | 0.0002 |
| 20, c050 | 0.0001 | 0.0002 | 0.0004 | 0.0017 | 0.0005 | 0.0003 | 0.0005 |
| 30, c100 | 0.0001 | 0.0002 | 0.0002 | 0.0004 | 0.0002 | 0.0002 | 0.0002 |
| 30, c050 | 0.0001 | 0.0004 | 0.0011 | 0.0030 | 0.0010 | 0.0018 | 0.0012 |
| **all 2,400** |  |  |  |  |  |  | **0.0005** |

Mean per-fit max |PIP − exact PIP|, plain:

| p, c | S1 | S2 | S3 | S4 | S5 | S6 | pooled |
|---|---|---|---|---|---|---|---|
| 20, c100 | 0.0017 | 0.0017 | 0.0017 | 0.0018 | 0.0017 | 0.0018 | 0.0017 |
| 20, c050 | 0.0019 | 0.0018 | 0.0019 | 0.0025 | 0.0018 | 0.0017 | 0.0019 |
| 30, c100 | 0.0018 | 0.0018 | 0.0017 | 0.0019 | 0.0017 | 0.0017 | 0.0018 |
| 30, c050 | 0.0020 | 0.0020 | 0.0022 | 0.0036 | 0.0022 | 0.0026 | 0.0024 |
| **all 2,400** |  |  |  |  |  |  | **0.0020** |

% of cases with MPM = exact MPM, RB:

| p, c | S1 | S2 | S3 | S4 | S5 | S6 | pooled |
|---|---|---|---|---|---|---|---|
| 20, c100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| 20, c050 | 100 | 100 | 100 | 99 | 100 | 100 | 99.8 |
| 30, c100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| 30, c050 | 100 | 100 | 100 | 99 | 99 | 100 | 99.7 |
| **all 2,400** |  |  |  |  |  |  | **99.9** |

% of cases with MPM = exact MPM, plain:

| p, c | S1 | S2 | S3 | S4 | S5 | S6 | pooled |
|---|---|---|---|---|---|---|---|
| 20, c100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| 20, c050 | 100 | 100 | 99 | 99 | 99 | 100 | 99.5 |
| 30, c100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| 30, c050 | 100 | 100 | 100 | 99 | 100 | 100 | 99.8 |
| **all 2,400** |  |  |  |  |  |  | **99.8** |

The 90th percentiles are in `tables/Q3_pip.csv`.

## Q4. Exact recovery of the truth (count out of 100 per scenario, 600 pooled)

| method | rule | p, c | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 |
|---|---|---|---|---|---|---|---|---|---|
| SMC-BVS | HPM | 20, c100 | 96 | 98 | 97 | 95 | 95 | 95 | **576** |
| SMC-BVS | HPM | 20, c050 | 96 | 97 | 96 | 87 | 92 | 94 | **562** |
| SMC-BVS | HPM | 30, c100 | 95 | 95 | 97 | 89 | 97 | 98 | **571** |
| SMC-BVS | HPM | 30, c050 | 94 | 91 | 94 | 61 | 86 | 81 | **507** |
| SMC-BVS | PIP > 0.5 (RB) | 20, c100 | 96 | 98 | 97 | 95 | 94 | 96 | **576** |
| SMC-BVS | PIP > 0.5 (RB) | 20, c050 | 96 | 98 | 94 | 78 | 92 | 94 | **552** |
| SMC-BVS | PIP > 0.5 (RB) | 30, c100 | 94 | 95 | 97 | 90 | 97 | 98 | **571** |
| SMC-BVS | PIP > 0.5 (RB) | 30, c050 | 93 | 91 | 90 | 53 | 85 | 79 | **491** |
| SMC-BVS | PIP > 0.5 (plain) | 20, c100 | 96 | 98 | 97 | 95 | 94 | 96 | **576** |
| SMC-BVS | PIP > 0.5 (plain) | 20, c050 | 96 | 98 | 94 | 78 | 91 | 94 | **551** |
| SMC-BVS | PIP > 0.5 (plain) | 30, c100 | 94 | 95 | 97 | 90 | 97 | 98 | **571** |
| SMC-BVS | PIP > 0.5 (plain) | 30, c050 | 93 | 91 | 90 | 53 | 84 | 79 | **490** |
| Exact enumeration | HPM | 20, c100 | 96 | 98 | 97 | 95 | 95 | 95 | **576** |
| Exact enumeration | HPM | 20, c050 | 96 | 97 | 96 | 87 | 92 | 94 | **562** |
| Exact enumeration | HPM | 30, c100 | 95 | 95 | 97 | 89 | 97 | 98 | **571** |
| Exact enumeration | HPM | 30, c050 | 94 | 91 | 94 | 61 | 86 | 81 | **507** |
| Exact enumeration | MPM | 20, c100 | 96 | 98 | 97 | 95 | 94 | 96 | **576** |
| Exact enumeration | MPM | 20, c050 | 96 | 98 | 94 | 79 | 92 | 94 | **553** |
| Exact enumeration | MPM | 30, c100 | 94 | 95 | 97 | 90 | 97 | 98 | **571** |
| Exact enumeration | MPM | 30, c050 | 93 | 91 | 90 | 53 | 84 | 79 | **490** |

**All methods, pooled exact recovery /600 per p × c** (benchmarks under their headline rule: lasso family F1–F3 `ebic1_K37`, with CV `cv_min` as a disclosed sensitivity per D35/D42; MCP and ABESS `ebic1_K37`; SuSiE `pip05`, SSL `ssl_final`, horseshoe `ci95`). Per-scenario counts are in `EVIDENCE_L.md` and `tables/Q4_recovery.csv`.

| method | rule | p = 20, c = 1 | p = 20, c = 0.5 | p = 30, c = 1 | p = 30, c = 0.5 | all /2,400 |
|---|---|---|---|---|---|---|
| SMC-BVS HPM | `hpm` | 576 | 562 | 571 | 507 | **2216** |
| SMC-BVS MPM (RB) | `pip05` | 576 | 552 | 571 | 491 | **2190** |
| SMC-BVS MPM (plain) | `mpm_plain` | 576 | 551 | 571 | 490 | **2188** |
| Exact-posterior HPM | `hpm` | 576 | 562 | 571 | 507 | **2216** |
| Exact-posterior MPM | `mpm` | 576 | 553 | 571 | 490 | **2190** |
| Lasso | `ebic1_K37` | 541 | 482 | 478 | 351 | **1852** |
| Elastic net | `ebic1_K37` | 502 | 449 | 416 | 325 | **1692** |
| Adaptive lasso | `ebic1_K37` | 534 | 521 | 531 | 480 | **2066** |
| MCP | `ebic1_K37` | 534 | 517 | 532 | 478 | **2061** |
| ABESS | `ebic1_K37` | 534 | 516 | 529 | 472 | **2051** |
| SuSiE | `pip05` | 575 | 550 | 570 | 488 | **2183** |
| SSL | `ssl_final` | 590 | 574 | 586 | 501 | **2251** |
| Horseshoe | `ci95` | 573 | 520 | 568 | 367 | **2028** |
| Lasso (CV sensitivity) | `cv_min` | 5 | 5 | 1 | 1 | **12** |
| Elastic net (CV sensitivity) | `cv_min` | 2 | 4 | 1 | 1 | **8** |
| Adaptive lasso (CV sensitivity) | `cv_min` | 156 | 120 | 127 | 77 | **480** |

Benchmark results not run: 0; failed: 0 (either would count as a non-recovery). ABESS exact size-k check (D54.3): the ebic1_K37 (headline) ABESS support is the exact best subset of its size (by RSS, ties allowed) in 2,375/2,400 fits; in the other 25 (max relative RSS gap 0.027) the exact best subset would have recovered the truth in 9 and ABESS recovered it while the best subset would not in 2, so replacing each suboptimal support by the exact best subset of the same size (holding the selected sizes fixed; EBIC selection over an exact path was not recomputed) would change ABESS's /2,400 count by +7. Over the whole stored path (sizes 1–p), 15,712 of 60,000 size-k supports are not RSS-optimal, 98.8% of them at sizes above the true size.

Two SMC fits carry a diagnostic flag (a final check failed, with low ESS): p = 20, c = 1, S4, and p = 30, c = 1, S3. Both recovered the truth. Under the passing-only count (master IV.1.3) each loses that one recovery, for both SMC rules (HPM and PIP > 0.5), with the denominators unchanged (100 per scenario, 600 pooled). So p = 20, c = 1 has 575/600 and S4 94/100; p = 30, c = 1 has 570/600 and S3 96/100. Per-scenario all-saved and passing-only counts: `tables/Q4_recovery.csv` (columns `S1`–`S6`, `passing_S1`–`passing_S6`).

## Repeat-seed stability (primary + 5 extra seeds = 6 fits per case, 14,400 fits)

These spreads use all 6 fits of each case: the primary plus the 5 extra seeds. That is a slight widening of the brief's "across the 5 extra seeds" definition, from the scoring pipeline (METRICS.md, `case_stability.csv`). The 5 extra seeds' own accuracy is reported separately, in the last bullet.

- **HPM:** all 6 seeds gave the same HPM in **100%** of cases (2,400/2,400).
- **log Ẑ:** the spread is the sd of log Ẑ across the 6 seeds. It has mean 0.011 and 90th percentile 0.018, with a maximum of 0.030. That is similar to the RMSE against the exact value (0.012), consistent with seed variability dominating the error; the pooled bias is small (Q1).
- **PIPs:** the spread is the max over variables of the sd of the PIP across seeds. For RB it has mean 0.0005 (90th percentile 0.0016); for plain, mean 0.0017 (90th percentile 0.0029).
- The 12,000 extra-seed fits are as accurate as the primaries. RMSE of e 0.012, lower-bound coverage 100%, HPM = exact HPM 100%, MPM = exact MPM 99.9% (RB) and 99.8% (plain).

Tables: `tables/stability.csv`, `tables/repeat_fit_accuracy.csv`.

## Files
- `tables/`: Q1–Q4, stability, repeat-fit accuracy, reconciliation (expected = scored + failed + missing), availability. Each table is rebuilt from the case-level CSVs and checked cell by cell against the pipeline's own H1–H4 (`scripts/build_tables.py`).
- `score_final/`: the scoring pipeline output (case-level CSVs, H1–H4, flag × error 2×2 table, SE calibration).
- `EVIDENCE_L.md`, `case_theory.csv`, `evidence/`: theory measures.
- `tieout/`, `review/`: the independent tie-out and the Sol review.
