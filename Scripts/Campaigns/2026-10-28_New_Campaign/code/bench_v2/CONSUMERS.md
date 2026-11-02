# Consumer changes for bench_v2

## Current state (2026-10-30, frozen)

High-p manifest SHA-256: `8905f52e314f706b54f985994d7915052301c9e22912690264b7b27ab58b0373`; F3 source tree: `3e01c77b27ad96ad8ec4761b6b25ea5511d357e8aa08a1db7b2972e71734f42c`; low-p r2 manifest: `85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7`. D54 applies to the r2 freeze. Controlled high-p reproduction passed 24/24 cases; the revised runner passed 72/72 and the earlier F2 legacy run passed 24/24. Local tests use scoped R 4.4.1/glmnet 4.1-10 compatibility and Windows path wrappers only; production remains pinned. Sol accepted low-p r2 and high-p numerical results with fixes; bundle R1-1 blocks deployment, and R1-3/R1-4 remain review findings. R1-2 controls and R1-5 current-state documentation are fixed pending review. See [Sol's review](review/SOL_REVIEW_1.md) and [test report](tests/TEST_REPORT.md).

For schema-v2 records, consume all six wrapper rows and the RDS coefficient evidence; never re-derive or duplicate the wrapper's K37 rows. Historical v1 runs retain their historical derivation.

The local-only shims are `tests/run_local_runner.R`, `tests/run_local_f1_runner.R` and `tests/run_local_f2_suite.R`; the test suite's scoped glmnet adapter is in `tests/run_all_tests.R`.

**OPEN downstream release checks:** high-p schema-v2 scoring and analysis integration; F2 alpha disclosure in low-p reporting; and the independent table tie-out. Passing the K37 comparison to the frozen derivation does not establish consumer integration.

## Historical consumer notes

**Status: implementation pending validation; consumers have not been edited.**

- Read `schema_version = 2` and the named RDS `coefficients` element. Each rule has `beta_pen` and `beta_ols`; CV OLS vectors and whole-fit-failure vectors are NA. For a rule-level failure in a completed fit, `beta_pen` is retained and matches `support_audit`. EBIC OLS slopes are distinct from the penalized vector.
- F1, F2, and F3 wrappers now emit `ebic1_K37` and `ebic05_K37`. Scoring and analysis must use these rows for bench_v2 runs and must not append duplicate rows from the frozen `derive_rules.R`. Older schema v1 runs still require the historic derivation.
- Validators must accept the six rule IDs, roles, added F3 columns `pilot_k`, `pilot_index`, `pilot_lambda`, and codes `pilot_null` and `pilot_single`; singleton glmnet-only diagnostic fields have jerr zero and npasses NA.
- F3 diagnostics contain `pilot` with lambda grid, selected index, beta, CV and KKT evidence, plus `pilot_beta`, `keep`, `w`, `v`, mapped path and full-p candidate table.
- Retire F3 `kappa`, `ridge`, `ridge_resid_max`, `ridge_fold_mse`, `kappa_min`, `kappa_index`, `kappa_boundary`, `eps_floor`, `n_floored`, and codes `kappa_edge` and `floored_selected`. Preserve historic ridge runs as separately labelled sensitivity results.
- The low-p port and its runner, frozen scoring code, and deployed validators remain separate work for the manager.
