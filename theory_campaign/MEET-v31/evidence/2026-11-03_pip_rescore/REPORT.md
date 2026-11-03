<!-- Chair helper (Opus 5.5, Claude Work, read-only), 2026-11-03. Filed verbatim by the chair. -->
# PIP rescore: equal-weight vs Ẑ-weighted (MEET-v31 helper)

## Main finding
The equal-weight vs Ẑ-weighted MPM comparison cannot be computed for the 2,394 completed fits from this machine: their per-island `log_Z_r` and `pip_r` are not stored here.
- The production bundles are at `C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\claude\prod_p{0500,1000}_20261023T1227Z\p*/<case_id>/SMCBVS.*` on the laptop (sha256-verified).
- The originals are at `/scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_*/results/` on NOTS (not deleted, per `Docs/Records/SMC_BVS_v3_deploy/OUTPUTS.md`).
- Neither is mounted here; `/scratch` does not exist on this host.

What is local:
- (A) 3 study designs re-run with the production code, which do carry per-island data.
- (B) Per-cell counts of MPM_eq == S0 and HPM == S0 for all 2,400 fits, from the scored production tables. There is no Ẑ-weighted counterpart.

## Data sources searched
| path | content | per-island? |
|---|---|---|
| `/home/fb31/ls0_work/full/p{0500,1000}/*.rds` (2,400), `full_lat/` (480) | LS0 records (`row`, `detail`: S0, start, ls0, scan_S0, …) | no |
| `/home/fb31/ls0_work/study{,_mt}/{inputs,truth}` | design inputs; truth (`active` = S0) | n/a |
| `/home/fb31/ls0_work/agg_final/*.csv`, `/home/fb31/ls0_work/sels_ledger_per_fit.csv` | per-fit LS0/paired tables; S-ELS ledger (status, HPM `S_hat`, `S0`, `F_hat`) | no PIPs |
| `Results/SMC_BVS_v3_production/p{0500,1000}/exact_recovery_long.csv` (repo) | per-cell exact counts, SMCBVS rules `pip05` (= MPM of pip_primary) and `hpm` | no |
| `/home/fb31/api_workers/METH-AUDIT/theory_campaign/METH-AUDIT/results/fit_*.rds` (3) | `prod` (R=4 serial), `r4` (R=4 concurrent), `rbig` (R=32, N=312); each with `log_Z_r`, `pip_r`, `hpm` | yes |
| `/home/fb31/abl_work/fits/p0500_S1_r001_c100_{A,B}.rds` | ABL-START arms A (mode 0) and B (mode 1), with `log_Z_r`, `pip_r` | yes |
| `/home/fb31/api_audit_work/out/*.rds` | p = 20 toy designs, not study designs | excluded |

## Method
For each fit with per-island data:
- pip_eq = rowMeans(pip_r).
- W_r = exp(log_Z_r − max) / Σ, and pip_zw = pip_r · W.
- ESS_isl = 1/ΣW_r².
- max_j |pip_zw − pip_eq|.
- MPM = {j : PIP > 1/2}, compared with S0. S0 is taken from the fit object and checked against `ls0_work/study/truth/.../<id>.rds$active`: it matches in 11/11 rows.
- Hamming distance = |MPM Δ S0|.
- HPM == S0 is checked from the fit's saved `hpm`.

Part B counts come from `exact_recovery_long.csv` (`exact_all_sum`). HPM is recounted per fit from the S-ELS ledger, with HPM == S0 iff `native_status == completed` and `S_hat == S0`.

## Part A: per-island subset (n = 3 designs; 11 fit-variants)
pip_eq equals the saved pip_primary/pip_eq exactly (max abs diff 0) in all 11 rows. pip_zw equals METH-AUDIT/ABL's saved pip_zw exactly (0) in all 8 rows where it was saved.

| design | variant | R | range log_Z_r | W_max | ESS_isl | max\|ΔPIP\| | MPM_eq=S0 | MPM_zw=S0 | MPMs differ | Ham eq/zw | HPM=S0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| p0500_S1_r001_c100 | prod R=4 | 4 | 0.146 | 0.264 | 3.987 | 3.94e-06 | T | T | F | 0/0 | T |
| p0500_S1_r001_c100 | r4 concurrent | 4 | 0.146 | 0.264 | 3.987 | 3.94e-06 | T | T | F | 0/0 | T |
| p0500_S1_r001_c100 | rbig R=32 | 32 | 0.612 | 0.042 | 31.22 | 3.03e-05 | T | T | F | 0/0 | T |
| p0500_S4_r001_c050 | prod R=4 | 4 | 0.189 | 0.270 | 3.982 | 1.75e-04 | F | F | F | 1/1 | F |
| p0500_S4_r001_c050 | r4 concurrent | 4 | 0.189 | 0.270 | 3.982 | 1.75e-04 | F | F | F | 1/1 | F |
| p0500_S4_r001_c050 | rbig R=32 | 32 | 0.924 | 0.049 | 30.07 | 8.38e-04 | F | F | F | 1/1 | F |
| p0500_S5_r002_c100 | prod R=4 | 4 | 2.412 | 0.707 | 1.879 | 1.29e-03 | T | T | F | 0/0 | T |
| p0500_S5_r002_c100 | r4 concurrent | 4 | 2.412 | 0.707 | 1.879 | 1.29e-03 | T | T | F | 0/0 | T |
| p0500_S5_r002_c100 | rbig R=32 | 32 | 3.544 | 0.142 | 11.72 | 3.55e-04 | T | T | F | 0/0 | T |
| p0500_S1_r001_c100 | ABL arm A (mode 0) | 4 | 0.146 | 0.264 | 3.987 | 3.94e-06 | T | T | F | 0/0 | T |
| p0500_S1_r001_c100 | ABL arm B (mode 1) | 4 | 0.138 | 0.273 | 3.988 | 8.01e-06 | T | T | F | 0/0 | T |

Notes:
- **S4_r001_c050.** Both MPMs equal the HPM, which is S0 ∪ {81}. Variable 81 has PIP_eq 0.6509 and PIP_zw 0.651, while the smallest PIP_eq on S0 is 0.9429. The Ẑ-weighting moves no PIP across 1/2.
- **S5_r002_c100.** This design has the most uneven island weights (W = 0.063 / 0.080 / 0.707 / 0.150, ESS_isl = 1.88). Even so, max|ΔPIP| = 1.29e-03, the largest PIP off S0 is 0.2185 (eq) and 0.2172 (zw), and every S0 PIP is 1.
- **Match to NOTS production.** For the 3 `prod` re-runs, HPM and hpm_F match the NOTS production ledger (`sels_ledger_per_fit.csv`: `S_hat`, `F_hat` to 10 significant digits). The NOTS pip_r themselves were not compared, because they are not available here.
- **Subset totals (R=4 `prod` only, 3 designs).**
  - MPM_eq right: 2/3. MPM_zw right: 2/3.
  - MPMs differ: 0. zw right & eq wrong: 0. eq right & zw wrong: 0.
  - Median max|ΔPIP| = 1.75e-04 (max 1.29e-03). Median ESS_isl = 3.982.

## Part B: all 2,400 fits, by cell (equal-weight MPM and HPM only)
"Completed" counts exclude the 6 resource_limit stops (p500 c100 S5: 1; p1000 c100 S5: 3; p1000 c050 S5: 2). The HPM count from the per-fit ledger equals the table count in every cell (28/28).

| p | c | scen | completed | MPM_eq=S0 | HPM=S0 |
|---|---|---|---|---|---|
| 500 | 1 | S1 | 100 | 92 | 95 |
| 500 | 1 | S2 | 100 | 97 | 96 |
| 500 | 1 | S3 | 100 | 93 | 94 |
| 500 | 1 | S4 | 100 | 93 | 91 |
| 500 | 1 | S5 | 99 | 90 | 89 |
| 500 | 1 | S6 | 100 | 94 | 94 |
| 500 | 1 | **all** | 599 | 559 | 559 |
| 500 | 0.5 | S1 | 100 | 74 | 79 |
| 500 | 0.5 | S2 | 100 | 83 | 84 |
| 500 | 0.5 | S3 | 100 | 63 | 64 |
| 500 | 0.5 | S4 | 100 | 18 | 25 |
| 500 | 0.5 | S5 | 100 | 53 | 59 |
| 500 | 0.5 | S6 | 100 | 47 | 59 |
| 500 | 0.5 | **all** | 600 | 338 | 370 |
| 1000 | 1 | S1 | 100 | 94 | 95 |
| 1000 | 1 | S2 | 100 | 95 | 95 |
| 1000 | 1 | S3 | 100 | 97 | 97 |
| 1000 | 1 | S4 | 100 | 94 | 93 |
| 1000 | 1 | S5 | 97 | 85 | 84 |
| 1000 | 1 | S6 | 100 | 96 | 96 |
| 1000 | 1 | **all** | 597 | 561 | 560 |
| 1000 | 0.5 | S1 | 100 | 70 | 71 |
| 1000 | 0.5 | S2 | 100 | 76 | 75 |
| 1000 | 0.5 | S3 | 100 | 63 | 67 |
| 1000 | 0.5 | S4 | 100 | 24 | 35 |
| 1000 | 0.5 | S5 | 98 | 32 | 31 |
| 1000 | 0.5 | S6 | 100 | 56 | 61 |
| 1000 | 0.5 | **all** | 598 | 321 | 340 |
| **total** | | | **2,394** | **1,779** | **1,829** |

The columns MPM_zw=S0, "MPMs differ", max|ΔPIP|, ESS_isl and the zw-right/eq-wrong counts are **not computed** for these 2,394 fits, because no per-island data exist locally.

## Caveats
- Part A covers 3 designs (all p = 500; S1 c1, S4 c0.5, S5 c1), chosen by METH-AUDIT rather than at random. It says nothing about the rate of MPM disagreement in the study.
- The METH-AUDIT `prod` objects are local re-runs. Their HPM and F match the production ledger, but bitwise identity of their pip_r to the NOTS bundles was not checked.
- The cells have 6 scenarios (S1–S6), not 5.
- To finish the requested computation, run `pip_rescore.R`'s `score_one()` over `SMCBVS.rds` (fields `log_Z_r`, `pip_r`, `pip_primary`, `hpm`) in the laptop or NOTS result roots. It needs no re-fitting: about 2,394 small reads.

## Files
- Script: `/tmp/claude-71711/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-theory-MEET-v31/14bcdd62-deb0-4c36-99c9-68518a64c746/scratchpad/pip_rescore/pip_rescore.R`
- Outputs: `partA_per_island_subset.csv`, `partB_cell_counts_2400.csv`, `run.log` (same directory)
