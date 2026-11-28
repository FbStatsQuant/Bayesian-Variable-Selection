# Provenance of the S1/S2 figures and tables (Sections 2 and 4)

Built 2026-11-28 07:40 UTC on Owls by `figures/scripts/build_sim_outputs.R` (R 4.6.0).

Inputs are read-only Engineering outputs under `_local/engineering/` on Owls; nothing from them is stored in the repository.

| input | path (under `_local/engineering/`) | sha256 |
|---|---|---|
| `s1_records` | `reports/S1S2/S1_comparison_final_records.tsv` | `c15a6138191a36ccf59e672f18bd0f0e321710e278c79c0c9e839e8437d42ea7` |
| `s1_permethod` | `reports/S1S2/S1_comparison_final_permethod.tsv` | `c167660dfb8e1f5208f250635fd784eaf10b5caa8f4a4ccb42abecee68e36a97` |
| `s1_paired` | `reports/S1S2/S1_comparison_final_paired.tsv` | `58ce95c917fa0b170a211b0b531aed224388686dfa55e7a646ba3b53c783f866` |
| `s1_runtime` | `reports/S1S2/final/runtime_S1_smcbvs_asi.tsv` | `e76745da19ed74460018cdf48a1e20c3e3ea0f10bbf1149ce46eeab0aca7761e` |
| `s2_records` | `reports/S1S2/S2_comparison_final_records.tsv` | `f71a9fa4a8321ddc0451501c706fa342c8a8d3f1df00df9e8f7a80657f3a4dd7` |
| `s2_permethod` | `reports/S1S2/S2_comparison_final_permethod.tsv` | `328f2b70eca7ccdf5c68cd40691355315701ea16af2521251592d28303118153` |
| `s2_paired` | `reports/S1S2/S2_comparison_final_paired.tsv` | `20e23a1156bc0ab8e55922fe9170d6ebdbb9711a3005b1ef2164827410d98992` |
| `s2_runtime` | `reports/S1S2/final/runtime_S2_smcbvs_asi.tsv` | `97b43f9aeca05baec0e9ccceff3f72b86f8b6a61463970372b747cf04435e8ae` |
| `s2_records5` | `reports/S1S2/S2_comparison_records.tsv` | `6db30814a3935da359f48ea8e0a6af3f0eb65a297e8ddaa4a6626242a386a858` |
| `s2_smc_final` | `reports/S1S2/final/results_S2_smcbvs.tsv` | `f70874e92bf05d11a19a50e8ea5c616589b6728056c7d886c3c4711961885518` |
| `s1_smc_final` | `reports/S1S2/final/results_S1_smcbvs.tsv` | `0f227f9af817a3532996450471e7f574c46dd45d834e0f1e399bd919b094665e` |
| `bt2_diag` | `reports/S1S2/diagnostics/bt2_diagnostic_per_rep.tsv` | `cf562ddd897351a51eb05dae1c12b1e703e4468999e417bf8101440333805cf5` |
| `s1_perfit` | `reports/S1S2/final/perfit_precision_recall_S1.tsv` | `d74ae54a402b6a4dd2c4a71b175ecfcd851d7ec956783f63a99ce2f9f4f8acd6` |
| `s2_perfit` | `reports/S1S2/final/perfit_precision_recall_S2.tsv` | `c8335dc36258eda74633d315eecbc330e358a742bf98f17ff994fe9216d5552c` |
| wall cache `wall_s1final` | 9600 per-fit JSON records (`wall_sec_harness`) | `4825ba8c5521b7e934ec104a7ae8520d81dfaa0f4d178fe4f81bb1d9af95c315` |
| wall cache `wall_s2final5` | 60000 per-fit JSON records (`wall_sec_harness`) | `593d01bb37b65afcc96fa7c01222184e40e0ac2889316d2fccc5e2f5c15d31bc` |
| wall cache `wallmd5_s2asi100` | 12000 per-fit JSON records (`wall_sec_harness`) | `a17284b0889adcaeb9c599ba592ee17b214c09424d0795df1a25dde8015bd9da` |

## Checks run by the build (it stops if any fails)
- Recomputed per-setting exact-recovery counts and mean FP, FN, F1 equal Engineering's `*_permethod.tsv` for every setting and method (S1 96 rows, S2 600 + 720 rows; max abs difference < 1e-15).
- S1 median, 90% and max wall times recomputed from the JSON records equal `final/runtime_S1_smcbvs_asi.tsv`.
- S2: the five non-ASI methods in the final 6-method records are identical (|S_hat|, TP, FP, exact, md5) to the earlier 5-method build, fit by fit (60,000 fits).
- S2: recomputed exact W/L of SMC-BVS vs ASI on the shared data sets equal `S2_comparison_final_paired.tsv` (all of S2 and nu = 2.07, 3.52, 6); recomputed wall median/q90/max and exact counts equal `final/runtime_S2_smcbvs_asi.tsv`.
- Every fit of S1 and S2 agrees with Engineering's per-fit tables `final/perfit_precision_recall_S{1,2}.tsv` in |S_hat|, TP, FP, FN and exact; their precision equals TP/|S_hat| wherever |S_hat| > 0 (NA for an empty selection).
- S2 ASI: the `data_md5` of every ASI JSON record (12,000) equals the md5 of the SMC-BVS record for the same data set.

## Status of the inputs
- S1: FINAL (reps 1-100, all six methods, 1,600 fits each).
- S2: FINAL, reps 1-100, all six methods (12,000 fits each), from `S2_comparison_final_records.tsv`.
- Precision is TP/|S_hat| per fit, averaged over the k non-empty fits of a cell (conditional precision; shown as -- when k < 20 in the full grids); the empty-selection share is reported beside it. `supp_s2_prec_conventions.tex` gives the empty -> 1, empty -> 0 and pooled (sum TP / sum |S_hat|) versions; the build checks (ii) = e + (1 - e)(i) and (iii) = (1 - e)(i). Recall is TP/s0 per fit, averaged over all fits.

`numbers.tsv` lists every number quoted in the prose of Section 2, keyed by quantity.
