# F3 deployed ridge-test migration

The deployed F3 test body is retained at F3_AdaptiveLasso/tests/test_F3_alasso.R, with a v2 adapter. The migrated canaries have run locally; these mappings distinguish their coverage from remaining dev-data validation.

| Deployed check or section | v2 treatment |
|---|---|
| ridge_vs_solve | Retired: no ridge in v2. |
| ridge_vs_glmnet_alpha0_map | Retired: no ridge in v2. |
| ridge_normal_equations_full_grid | Retired: no ridge in v2; selected pilot KKT is checked instead. |
| ridge_cv_vs_naive | Retired: no ridge in v2; pilot identity and CV checks replace the pilot comparison. |
| ridge_cv_tie_larger | Retired: no ridge in v2; cv_choose and K37 tie checks apply to the new grid. |
| pf_sum_is_p | Replaced by screened-factor sum = m check. |
| pf_7v_equals_v | Replaced by F3 penalty factor rescaling invariance. |
| orth_ridge_closed_form | Retired: no ridge in v2. |
| orth_weighted_soft_threshold | Replaced by singleton independent full/fold scalar checks and a multi-column orthogonal path check; passed. |
| grid_first_point_null_orth | Retained in the migrated orthogonal canary; passed. |
| orth_primary_recovers_5 | Manager reclassified exact CV-min recovery as a disclosed diagnostic; truth inclusion remains hard and passed. |
| orth_primary_contains_5, orth_some_rule_exact | Replaced by hard truth-inclusion and exact ebic1/ebic1_K37 checks; passed. |
| noint_ridge_full_path, noint_ridge_fitted | Retired: no ridge in v2. |
| noint_weighted_path, noint_path_solves_centred_problem, noint_weighted_path_k_le_100 | Adapted to lasso-pilot weights and passed on the orthogonal fixture. |
| noint_rss_identity | Adapted to lasso-pilot supports and passed. |
| determinism_cvm_bitwise (ridge CV component) | Replaced by identical pilot CV, rules and beta check in run_all_tests.R. |
| fail_ridge_check | Replaced by injected pilot KKT failure and mutated implementation negative control. |
| ridge/kappa/floor diagnostic print and dimension checks | Replaced by schema-v2 pilot/screen fields and retired-field checks in validate_outputs.R. |

The existing dev-scale common EBIC, wrapper, input, version, failure, no-oracle, and engine checks also need full dev-data validation; several have analogous checks in run_all_tests.R and the canaries.
