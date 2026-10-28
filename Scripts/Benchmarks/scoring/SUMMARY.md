# SUMMARY: n = 200 benchmark production runs, c = 1 (thread S)

All numbers are provisional: the method code and the scoring code are AI-written and unreviewed (G5); the independent recount (G9) is separate.
Denominators: 100 per (p, scenario), 600 pooled per p. Failures = failed + timeout + not_run + missing; they count as non-recovery.
Flagged = fits with `diag_flag = TRUE` (passing-only count in brackets).

## A2: primary rule `ssl_final`

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 99 | 99 | 97 | 84 | 93 | 97 | 569 | 0 | 0 |
| 1000 | 100 | 96 | 98 | 92 | 97 | 99 | 582 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|
| SSL-RS | ssl_final | S1 | 593 | 592 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261019T2140Z_bench20261019_prod_A2_SSL/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/20261019T2140Z_bench20261019_prod_A2_SSL/`.

## F3: primary rule `cv_min`

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|
| F3 | cv_1se | S0 |   9 |  0 |
| F3 | ebic1 | S0 (T1 companion) | 247 | 96 |
| F3 | ebic05 | S0 | 212 | 91 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261019T2157Z_bench20261019_prod_F3_AdaptiveLasso/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/20261019T2157Z_bench20261019_prod_F3_AdaptiveLasso/`.

## F5: primary rule `ebic1`

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 66 | 77 | 71 | 26 | 76 | 49 | 365 | 0 | 0 |
| 1000 | 40 | 63 | 76 | 24 | 66 | 54 | 323 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|
| F5 | ebic05 | S0 | 47 | 7 |
| F5 | bic | S0 |  0 | 0 |

**Post hoc (chosen after seeing the production cap-hit diagnostics; not a pre-declared rule; not in T1):**

| method_id | rule_id | p | exact_all | n_expected | n_fail_total |
|---|---|---|---|---|---|
| F5 | ebic1_K37 |  500 | 367 | 600 | 0 |
| F5 | ebic1_K37 | 1000 | 356 | 600 | 0 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261019T2157Z_bench20261019_prod_F5_ABESS/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/20261019T2157Z_bench20261019_prod_F5_ABESS/`; post hoc `/projects/ml75/fb31/BVS/bench20261019/scoring/out/20261019T2157Z_bench20261019_prod_F5_ABESS/posthoc_ebic1_K37/`.

## A3: primary rule `ci95`

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
|  500 | 92 | 98 | 100 | 87 | 98 | 99 | 574 | 0 |  0 |
| 1000 | 91 [71] | 95 [91] | 100 | 91 | 98 | 100 [99] | 575 [550] | 0 | 32 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|
| A3 | km2 | S0 | 511 | 522 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261019T2209Z_bench20261019_prod_A3_Horseshoe/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/20261019T2209Z_bench20261019_prod_A3_Horseshoe/`.

## A1: primary rule `pip05`

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
|  500 | 99 [94] | 98 [97] | 97 [93] | 95 [93] | 98 | 98 [97] | 585 [572] | 0 | 13 |
| 1000 | 100 [98] | 96 [93] | 98 [95] | 95 [92] | 94 | 99 [94] | 582 [566] | 0 | 16 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|
| A1 | cslead | S0 | 591 | 592 |
| A1 | bfdr10 | S0 |   0 |   0 |
| SuSiE-L100 | pip05 | S1 | 585 | 582 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261019T2219Z_bench20261019_prod_A1_SuSiE/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/20261019T2219Z_bench20261019_prod_A1_SuSiE/`.

## F4: primary rule `ebic1`

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 39 | 69 | 77 | 44 | 78 | 70 | 377 | 0 | 0 |
| 1000 | 18 | 28 | 60 | 32 | 49 | 48 | 235 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|
| F4 | ebic05 | S0 |  28 |   6 |
| F4 | bic | S0 |   0 |   0 |
| F4_SCAD | ebic1 | S1 | 454 | 417 |
| F4_SCAD | ebic05 | S1 |  66 |  22 |
| F4_SCAD | bic | S1 |   0 |   0 |

**Post hoc (chosen after seeing the production cap-hit diagnostics; not a pre-declared rule; not in T1):**

| method_id | rule_id | p | exact_all | n_expected | n_fail_total |
|---|---|---|---|---|---|
| F4 | ebic1_K37 |  500 | 417 | 600 | 0 |
| F4 | ebic1_K37 | 1000 | 386 | 600 | 0 |
| F4_SCAD | ebic1_K37 |  500 | 455 | 600 | 0 |
| F4_SCAD | ebic1_K37 | 1000 | 448 | 600 | 0 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261019T2219Z_bench20261019_prod_F4_MCP_SCAD/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/20261019T2219Z_bench20261019_prod_F4_MCP_SCAD/`; post hoc `/projects/ml75/fb31/BVS/bench20261019/scoring/out/20261019T2219Z_bench20261019_prod_F4_MCP_SCAD/posthoc_ebic1_K37/`.

## F2: primary rule `cv_min`

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|
| F2 | cv_1se | S0 |  0 |  0 |
| F2 | ebic1 | S0 (T1 companion) | 61 | 50 |
| F2 | ebic05 | S0 | 53 | 48 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261019T2232Z_bench20261019_prod_F2_ElasticNet/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/20261019T2232Z_bench20261019_prod_F2_ElasticNet/`.

## F1: primary rule `cv_min`

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|
| F1 | cv_1se | S0 |   0 |  0 |
| F1 | ebic1 | S0 (T1 companion) | 111 | 89 |
| F1 | ebic05 | S0 |  92 | 82 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261019T2308Z_bench20261019_prod_F1_Lasso/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/20261019T2308Z_bench20261019_prod_F1_Lasso/`.

Combined tables: `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined/` (rules_long, T1–T6, S_tables, caps, codes_by_rule; real values at 17 significant digits).
