# Provenance of the S1/S2 figures and tables (Sections 2 and 4)

Built 2026-11-28 08:49 UTC by `figures/scripts/build_sim_outputs.R` (R 4.6.0).

Inputs are read-only Engineering outputs under `_local/engineering/` (located through `SMCBVS_ENG_DIR` or a relative path; see `sim_data.R`); nothing from them is stored in the repository. The caches hold fields read from the per-fit JSON records and are rebuilt when absent.

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
| Slurm records | `runs/S1S2/_logs/sacct/` (44 files) | sha256 of the sorted list of their sha256 sums: `4c60cf9a47fb66ef59cb659c5ecc0b523fa720beeb83e8db701f11d1c277c0fc` |
| cache `wall_s1final` | 9600 per-fit JSON records | `4825ba8c5521b7e934ec104a7ae8520d81dfaa0f4d178fe4f81bb1d9af95c315` |
| cache `wall_s2final5` | 60000 per-fit JSON records | `593d01bb37b65afcc96fa7c01222184e40e0ac2889316d2fccc5e2f5c15d31bc` |
| cache `wallmd5_s2asi100` | 12000 per-fit JSON records | `a17284b0889adcaeb9c599ba592ee17b214c09424d0795df1a25dde8015bd9da` |
| cache `smcsum_s1v2` | 1600 per-fit JSON records | `e2ca521dc7fab90fa2924c228b5a3f3ce080325ea9481d93195cd8141432aea2` |
| cache `smcsum_s2v2` | 12000 per-fit JSON records | `0e7cf4612ac7431a4e5ac53ebb215504e04276d1f40a7bf8ee65e39ba0fac77e` |
| cache `runtime_s1` | 9600 per-fit JSON records | `504c491f646ef26637a01af50a098b9a1704df565885c36ef19864a97b49486c` |
| cache `runtime_s2` | 72000 per-fit JSON records | `45b8ea57bc3cccbdbeb52eba1a87766eea75f8a011bcf2774c66896e6712cf25` |

## Checks run by the build (it stops if any fails)
- Recomputed per-setting exact-recovery counts and mean FP, FN, F1 equal Engineering's `*_permethod.tsv` for every setting and method (S1 96 rows, S2 720 rows).
- Every fit of S1 and S2 agrees with Engineering's per-fit tables `final/perfit_precision_recall_S{1,2}.tsv` in |S_hat|, TP, FP, FN and exact; their precision equals TP/|S_hat| wherever |S_hat| > 0.
- S1 median, 90% and max wall times of completed fits equal `final/runtime_S1_smcbvs_asi.tsv`; the ten rerun SMC-BVS fits match the ten COMPLETED tasks of `sacct_b1r.tsv` in elapsed time (within 5 min); the 1,600 ASI tasks of S1 all COMPLETED at the first attempt.
- S2: the five non-ASI methods are identical (|S_hat|, TP, FP, exact, md5) to the earlier 5-method build, fit by fit (60,000 fits); the `data_md5` of every ASI record equals that of the SMC-BVS record for the same data set (12,000).
- S2: the complete-case (six methods finished) exact W/L of SMC-BVS vs ASI equal `S2_comparison_final_paired.tsv` (all of S2 and nu = 2.07, 3.52, 6); the paper's paired table uses all 12,000 data sets, on which both methods finished. Recomputed wall median/q90/max and exact counts equal `final/runtime_S2_smcbvs_asi.tsv`; all 24,000 SMC-BVS and ASI Slurm tasks COMPLETED.
- Escalation counts per fit (JSON `summary.escalated`) sum to Engineering's `final/results_S{1,2}_smcbvs.tsv` totals.
- Precision conventions: (ii) = e + (1 - e)(i) and (iii) = (1 - e)(i) to 1e-12 in every cell.

## Status of the inputs
- S1 and S2: FINAL (reps 1-100, all six methods; 1,600 and 12,000 fits per method).
- Precision is TP/|S_hat| per fit, averaged over the k non-empty fits of a cell (conditional precision; -- when k < 20); the empty count is reported beside it. Recall is TP/s0 per fit, averaged over all fits. A fit that did not finish counts as an empty selection (81 BAS fits in S2); the ten SMC-BVS fits of S1 that hit the 24 h limit were rerun, and the text gives the counts under the empty-selection rule too.

`numbers.tsv` lists every number quoted in the prose of Section 2, keyed by quantity.
