# Provenance of the S1/S2 figures and tables (Sections 2 and 4)

Built 2026-11-28 04:55 UTC on Owls by `figures/scripts/build_sim_outputs.R` (R 4.6.0).

Inputs are read-only Engineering outputs under `_local/engineering/` on Owls; nothing from them is stored in the repository.

| input | path (under `_local/engineering/`) | sha256 |
|---|---|---|
| `s1_records` | `reports/S1S2/S1_comparison_final_records.tsv` | `c15a6138191a36ccf59e672f18bd0f0e321710e278c79c0c9e839e8437d42ea7` |
| `s1_permethod` | `reports/S1S2/S1_comparison_final_permethod.tsv` | `c167660dfb8e1f5208f250635fd784eaf10b5caa8f4a4ccb42abecee68e36a97` |
| `s1_paired` | `reports/S1S2/S1_comparison_final_paired.tsv` | `58ce95c917fa0b170a211b0b531aed224388686dfa55e7a646ba3b53c783f866` |
| `s1_runtime` | `reports/S1S2/final/runtime_S1_smcbvs_asi.tsv` | `e76745da19ed74460018cdf48a1e20c3e3ea0f10bbf1149ce46eeab0aca7761e` |
| `s2_records` | `reports/S1S2/S2_comparison_records.tsv` | `6db30814a3935da359f48ea8e0a6af3f0eb65a297e8ddaa4a6626242a386a858` |
| `s2_permethod` | `reports/S1S2/S2_comparison_permethod.tsv` | `ceae8f79cd5ef87d5a904c67547c377d6213c92c2167e10c265d8b36b978fb2f` |
| `s2_asi_records` | `reports/S1S2/hq_s2asi_b1/S2_comparison_asi_b1_records.tsv` | `b25b110a4bcea1c7f804a45e2cd23fa8924788a3326c0db4a5a39315fe185acd` |
| `s2_asi_permethod` | `reports/S1S2/hq_s2asi_b1/S2_comparison_asi_b1_permethod.tsv` | `27eae7b3fa82115c0e57931854f63ea195d1f12556887ebc0814b7a85c8d77b2` |
| `s2_asi_paired` | `reports/S1S2/hq_s2asi_b1/S2_comparison_asi_b1_paired.tsv` | `74cba7b6ce35552e62dd7c976dc514197e2f478ad039a006f771a96186290ed2` |
| `s2_smc_final` | `reports/S1S2/final/results_S2_smcbvs.tsv` | `f70874e92bf05d11a19a50e8ea5c616589b6728056c7d886c3c4711961885518` |
| `s1_smc_final` | `reports/S1S2/final/results_S1_smcbvs.tsv` | `0f227f9af817a3532996450471e7f574c46dd45d834e0f1e399bd919b094665e` |
| `bt2_diag` | `reports/S1S2/diagnostics/bt2_diagnostic_per_rep.tsv` | `cf562ddd897351a51eb05dae1c12b1e703e4468999e417bf8101440333805cf5` |
| wall cache `s1final` | 9600 per-fit JSON records (`wall_sec_harness`) | `4825ba8c5521b7e934ec104a7ae8520d81dfaa0f4d178fe4f81bb1d9af95c315` |
| wall cache `s2final5` | 60000 per-fit JSON records (`wall_sec_harness`) | `593d01bb37b65afcc96fa7c01222184e40e0ac2889316d2fccc5e2f5c15d31bc` |
| wall cache `s2asi25` | 18000 per-fit JSON records (`wall_sec_harness`) | `f9967d9625d133628794ab52311cc3155c9a99192d75b19118761179b40ae531` |

## Checks run by the build (it stops if any fails)
- Recomputed per-setting exact-recovery counts and mean FP, FN, F1 equal Engineering's `*_permethod.tsv` for every setting and method (S1 96 rows, S2 600 + 720 rows; max abs difference < 1e-15).
- S1 median, 90% and max wall times recomputed from the JSON records equal `final/runtime_S1_smcbvs_asi.tsv`.
- S2 interim (reps 1-25) records of the five non-ASI methods are identical (|S_hat|, TP, exact) to the final 100-rep records on reps 1-25.

## Status of the inputs
- S1: FINAL (reps 1-100, all six methods, 1,600 fits each).
- S2: FINAL for SMC-BVS, lasso, SCAD, BAS, SuSiE (reps 1-100, 12,000 fits each). ASI is INTERIM: reps 1-25 (3,000 fits), from the HQ build `hq_s2asi_b1/`. Replace by the Engineering S2 final (`S2_comparison_final_*`) when it exists.
- Precision and recall are per fit and then averaged (precision = 1 - FP/max(|S_hat|,1)); Engineering's `precision`/`recall` columns are pooled ratios (sum TP / sum |S_hat|), which this build does not use.

`numbers.tsv` lists every number quoted in the prose of Section 2, keyed by quantity.
