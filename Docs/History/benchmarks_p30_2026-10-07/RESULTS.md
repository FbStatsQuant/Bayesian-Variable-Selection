# Results — benchmarks 3 (exact best subset + BIC), 5 (SuSiE), 6 (PARNI), production run of 2026-10-08

Run `runs/b356_production_20261008T012655Z` on NOTS (`~/projects/BVS/Benchmarks`), submitted 01:26:55Z, finalized
01:47:44Z. 600 sealed datasets (S1–S6 × 100), 1,800 fits, 600 exact 2^30 references. All three aggregation gates PASS:
600/600 fits verified per method, 0 integrity problems, 0 nonconverged. Test gate `audit/tests_2047044` PASS.

Files here: `production_20261008T012655Z/report/REPORT.md` (shared report, all rules), `…/exact_comparison/`
(comparison with the exact posterior), `…/aggregation/<Method>/` (gates, per-fit metrics), receipts, metrics and fit
summaries per dataset, `exact_references/` (600 exact posteriors), `audit/` (test gate). Raw `fit.rds` stay on NOTS.

## Exact support recovery, primary rules (count / 100)

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| Exact posterior MPM (Bayes ceiling, control model) | 88 | 79 | 72 | 29 | 65 | 49 |
| Exact posterior HPM | 87 | 81 | 73 | 33 | 63 | 63 |
| PARNI, plain PIP > 0.5 (repeat 1) | 88 | 79 | 72 | 28 | 65 | 50 |
| SuSiE, PIP > 0.5 (IBSS as published) | 90 | 82 | 24 | 0 | 12 | 54 |
| Best subset + BIC | 37 | 34 | 42 | 18 | 34 | 27 |

Sensitivity rules: best subset with EBIC_1 reaches 86 / 80 / 72 / 29 / 61 / 58; SuSiE with `refine = TRUE` 91 / 82 / 29 /
0 / 22 / 54. Full tables (truth included, FP, FN, size) in `REPORT.md`.

## Agreement with the exact posterior decisions (fraction of 100 datasets)

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| PARNI = exact MPM | 1.00 | 1.00 | 1.00 | 0.96 | 1.00 | 0.99 |
| SuSiE = exact MPM | 0.83 | 0.76 | 0.25 | 0.06 | 0.16 | 0.85 |
| Best subset BIC = exact MPM | 0.40 | 0.43 | 0.51 | 0.34 | 0.49 | 0.35 |

## PARNI PIP accuracy against the exact PIPs (median over 100 datasets of the mean absolute error)

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| plain PIP, one run | 6.8e-4 | 7.5e-4 | 1.1e-3 | 2.0e-3 | 1.1e-3 | 1.3e-3 |
| Rao-Blackwell PIP, one run | 2.8e-5 | 6.2e-5 | 3.2e-4 | 1.0e-3 | 2.3e-4 | 5.0e-4 |
| SD of plain PIP across 5 repeats | 8.1e-4 | 9.0e-4 | 1.3e-3 | 2.3e-3 | 1.2e-3 | 1.5e-3 |

SuSiE's PIPs are an approximation under a different model; their median MAE against the control posterior is 0.04
(S1, S2, S6) and 0.12 (S3–S5).

## Cost (mean wall seconds per dataset, one core)

| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| PARNI (5 repeats × 25 chains × 3,000 iterations) | 123 | 121 | 139 | 195 | 127 | 126 |
| Best subset + BIC (incl. verification passes) | 5.9 | 5.8 | 5.9 | 5.9 | 5.9 | 5.9 |
| SuSiE (both variants) | 2.1 | 2.1 | 1.9 | 1.6 | 1.8 | 2.2 |
| Exact enumeration (median) | 218 | 219 | 222 | 211 | 214 | 221 |

Peak memory: PARNI 317 MB, exact 311 MB, SuSiE 262 MB, best subset 103 MB.
