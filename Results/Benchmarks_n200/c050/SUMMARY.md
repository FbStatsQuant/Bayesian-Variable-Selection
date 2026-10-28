# SUMMARY: n = 200 benchmark production runs, c = 1 (thread S)

All numbers are provisional: the method code and the scoring code are AI-written and unreviewed (G5); the independent recount (G9) is separate.
Denominators: 100 per (p, scenario), 600 pooled per p. Failures = failed + timeout + not_run + missing; they count as non-recovery.
Flagged = fits with `diag_flag = TRUE` (passing-only count in brackets).

## A1: primary rule `pip05` (pre-declared)

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
|  500 | 65 [61] | 70 [70] | 34 [33] | 9 [9] | 3 | 39 [38] | 220 [214] | 0 | 14 |
| 1000 | 49 [48] | 57 [56] | 47 [46] | 21 [20] | 0 | 31 [31] | 205 [201] | 0 |  8 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | label | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|---|
| A1 | cslead | S0 | pre-declared | 195 | 187 |
| A1 | bfdr10 | S0 | pre-declared |  46 |  40 |
| SuSiE-L100 | pip05 | S1 | pre-declared | 221 | 205 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261021T1540Z_bench20261019_prodc050_A1_SuSiE/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined_c050/runs/20261021T1540Z_bench20261019_prodc050_A1_SuSiE/`.

## F2: primary rule `cv_min` (pre-declared)

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | label | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|---|
| F2 | cv_1se | S0 | pre-declared |  0 |  0 |
| F2 | ebic1 | S0 (T1 companion) | pre-declared | 14 | 10 |
| F2 | ebic05 | S0 | pre-declared |  9 | 10 |
| F2 | ebic1_K37 | S0 | pre-registered (PREREG_c050 R1) | 14 | 10 |
| F2 | ebic05_K37 | S0 | pre-registered (PREREG_c050 R1) |  9 | 10 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261021T1540Z_bench20261019_prodc050_F2_ElasticNet/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined_c050/runs/20261021T1540Z_bench20261019_prodc050_F2_ElasticNet/`.

## F3: primary rule `cv_min` (pre-declared)

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | label | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|---|
| F3 | cv_1se | S0 | pre-declared |  0 |  0 |
| F3 | ebic1 | S0 (T1 companion) | pre-declared | 36 | 12 |
| F3 | ebic05 | S0 | pre-declared | 26 | 12 |
| F3 | ebic1_K37 | S0 | pre-registered (PREREG_c050 R1) | 36 | 12 |
| F3 | ebic05_K37 | S0 | pre-registered (PREREG_c050 R1) | 26 | 12 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261021T1540Z_bench20261019_prodc050_F3_AdaptiveLasso/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined_c050/runs/20261021T1540Z_bench20261019_prodc050_F3_AdaptiveLasso/`.

## A2: primary rule `ssl_final` (pre-declared)

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
|  500 | 80 | 84 [84] | 53 |  9 | 42 | 35 | 303 [303] | 0 | 1 |
| 1000 | 67 | 64 | 43 | 15 | 28 | 38 | 255 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | label | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|---|
| SSL-RS | ssl_final | S1 | pre-declared | 32 | 32 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261021T1552Z_bench20261019_prodc050_A2_SSL/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined_c050/runs/20261021T1552Z_bench20261019_prodc050_A2_SSL/`.

## F4: primary rule `ebic1` (pre-declared)

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged | k > 37 |
|---|---|---|---|---|---|---|---|---|---|---|
| 500 | 38 | 58 | 42 | 1 | 45 | 19 | 203 | 0 | 0 | 60 |
| 1000 | 13 | 26 | 34 | 1 | 18 | 10 | 102 | 0 | 0 | 214 |

## F4: primary rule `ebic1_K37` (pre-registered (PREREG_c050 R1))

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged | k > 37 |
|---|---|---|---|---|---|---|---|---|---|---|
| 500 | 62 | 71 | 42 | 1 | 45 | 19 | 240 | 0 | 0 | 0 |
| 1000 | 49 | 59 | 45 | 1 | 20 | 18 | 192 | 0 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | label | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|---|
| F4 | ebic05 | S0 | pre-declared |  13 |   0 |
| F4 | bic | S0 | pre-declared |   0 |   0 |
| F4 | ebic05_K37 | S0 | pre-registered (PREREG_c050 R1) |  89 |  34 |
| F4 | bic_K37 | S0 | pre-registered (PREREG_c050 R1) |   0 |   0 |
| F4 | ebic1_lam005 | S0 | pre-registered (PREREG_c050 R1) | 240 | 192 |
| F4_SCAD | ebic1 | S1 | pre-declared |  95 |  55 |
| F4_SCAD | ebic05 | S1 | pre-declared |  14 |   3 |
| F4_SCAD | bic | S1 | pre-declared |   0 |   0 |
| F4_SCAD | ebic1_K37 | S1 | pre-registered (PREREG_c050 R1) |  96 |  59 |
| F4_SCAD | ebic05_K37 | S1 | pre-registered (PREREG_c050 R1) |  62 |  34 |
| F4_SCAD | bic_K37 | S1 | pre-registered (PREREG_c050 R1) |   0 |   0 |
| F4_SCAD | ebic1_lam005 | S1 | pre-registered (PREREG_c050 R1) |  96 |  59 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261021T1604Z_bench20261019_prodc050_F4_MCP_SCAD/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined_c050/runs/20261021T1604Z_bench20261019_prodc050_F4_MCP_SCAD/`.

## F5: primary rule `ebic1` (pre-declared)

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged | k > 37 |
|---|---|---|---|---|---|---|---|---|---|---|
| 500 | 65 | 72 | 34 | 4 | 48 | 31 | 254 | 0 | 0 | 4 |
| 1000 | 36 | 55 | 42 | 3 | 22 | 28 | 186 | 0 | 0 | 66 |

## F5: primary rule `ebic1_K37` (pre-registered (PREREG_c050 R1))

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged | k > 37 |
|---|---|---|---|---|---|---|---|---|---|---|
| 500 | 67 | 72 | 34 | 4 | 48 | 31 | 256 | 0 | 0 | 0 |
| 1000 | 54 | 64 | 42 | 3 | 23 | 28 | 214 | 0 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | label | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|---|
| F5 | ebic05 | S0 | pre-declared |  29 |   2 |
| F5 | bic | S0 | pre-declared |   0 |   0 |
| F5 | ebic05_K37 | S0 | pre-registered (PREREG_c050 R1) |  57 |  14 |
| F5 | bic_K37 | S0 | pre-registered (PREREG_c050 R1) |   0 |   0 |
| F5 | sic_smax | S0 | pre-registered (PREREG_c050 R1) | 167 | 127 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261021T1604Z_bench20261019_prodc050_F5_ABESS/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined_c050/runs/20261021T1604Z_bench20261019_prodc050_F5_ABESS/`.

## F1: primary rule `cv_min` (pre-declared)

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | label | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|---|
| F1 | cv_1se | S0 | pre-declared |  0 |  0 |
| F1 | ebic1 | S0 (T1 companion) | pre-declared | 24 | 15 |
| F1 | ebic05 | S0 | pre-declared | 19 | 14 |
| F1 | ebic1_K37 | S0 | pre-registered (PREREG_c050 R1) | 24 | 15 |
| F1 | ebic05_K37 | S0 | pre-registered (PREREG_c050 R1) | 19 | 14 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261021T1615Z_bench20261019_prodc050_F1_Lasso/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined_c050/runs/20261021T1615Z_bench20261019_prodc050_F1_Lasso/`.

## A3: primary rule `ci95` (pre-declared)

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
|  500 | 74 | 69 | 18 | 0 | 10 | 14 | 185 | 0 |  0 |
| 1000 | 60 [45] | 50 [49] | 11 [11] | 0 | 11 | 4 [4] | 136 [120] | 0 | 38 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | label | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|---|
| A3 | km2 | S0 | pre-declared | 139 | 128 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261021T1818Z_bench20261019_prodc050_A3_Horseshoe/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined_c050/runs/20261021T1818Z_bench20261019_prodc050_A3_Horseshoe/`.

## SuSiE-refine: S1 rule `pip05` (pre-registered arm (PREREG_c050 R4); fit selection by ELBO)

| p | S1 | S2 | S3 | S4 | S5 | S6 | pooled /600 | failures | flagged |
|---|---|---|---|---|---|---|---|---|---|
|  500 | 66 [62] | 71 [71] | 43 [42] | 17 [17] | 6 | 46 [45] | 249 [243] | 0 | 13 |
| 1000 | 49 [48] | 57 [56] | 49 [48] | 22 [21] | 3 | 32 [32] | 212 [208] | 0 |  8 |

Pre-declared companion and sensitivity rules (pooled):

| method_id | rule_id | role | label | p = 500 /600 | p = 1000 /600 |
|---|---|---|---|---|---|
| SuSiE-refine | cslead | S0 | pre-registered arm (PREREG_c050 R4); fit selection by ELBO | 222 | 194 |
| SuSiE-refine | bfdr10 | S0 | pre-registered arm (PREREG_c050 R4); fit selection by ELBO |  49 |  38 |

Paths: results `/projects/ml75/fb31/BVS/bench20261019/results/20261021T1818Z_bench20261019_prodc050_SuSiErefine/`; tables `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined_c050/runs/20261021T1818Z_bench20261019_prodc050_SuSiErefine/`.

Combined tables: `/projects/ml75/fb31/BVS/bench20261019/scoring/out/combined_c050/` (rules_long, T1–T6, S_tables, caps, codes_by_rule; real values at 17 significant digits).
