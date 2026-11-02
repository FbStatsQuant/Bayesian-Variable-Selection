# Changes in bench_v2

## Current state (2026-10-30, frozen)

The high-p manifest SHA-256 is `8905f52e314f706b54f985994d7915052301c9e22912690264b7b27ab58b0373`, the F3 source tree hash is `3e01c77b27ad96ad8ec4761b6b25ea5511d357e8aa08a1db7b2972e71734f42c`, and the low-p r2 manifest SHA-256 is `85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7`. D54 applies to the r2 low-p freeze; see the [Sol review](review/SOL_REVIEW_1.md).

All 24 controlled high-p cases passed paired F1/F2 identity, F3 pilot identity, six-rule coefficient support and K37 comparisons. The revised single runner passed 72/72, and the earlier F2 legacy suite passed 24/24; F1 legacy evidence is a union of runs, as detailed in [the test report](tests/TEST_REPORT.md). Local R 4.4.1/glmnet 4.1-10 checks use scoped compatibility and Windows path wrappers; production version checks remain unchanged. Sol accepted the low-p r2 code, accepted high-p numerical work with fixes, and rejected both job bundles pending R1-1; R1-3 and R1-4 also remain review findings. R1-2 is addressed in tests outside the freeze and R1-5 by these current-state notes; both fixes await review.

Schema-v2 consumers must use the wrapper's six rows and coefficient evidence; do not re-derive K37 for v2. High-p scoring/analysis integration, low-p F2 alpha disclosure and independent table tie-out remain downstream release checks; see [consumer policy](CONSUMERS.md).

The local runner shims are `tests/run_local_runner.R`, `tests/run_local_f1_runner.R` and `tests/run_local_f2_suite.R`; `tests/run_all_tests.R` provides the scoped local glmnet compatibility adapter.

## Historical implementation notes

**Status: work in progress; not validated or frozen.**

- AUDIT §3 items 1–3: replace the F3 ridge pilot with F1's CV-min lasso, screen its nonzero coefficients, normalize inverse weights stably, and use screened fitting. Null and singleton pilot sizes have explicit paths.
- AUDIT §3 items 4–5: calculate EBIC using original p, add K37 rules, retire ridge-only metadata and add pilot metadata and codes. The F3 pilot vector is available in both `diagnostics$pilot$beta` and `diagnostics$pilot_beta`.
- AUDIT §5 and §3 item 5: save penalized and separately labelled OLS coefficient evidence per registered rule; assert agreement with each successful rule's support. Runner RDS schema is version 2 and stores `coefficients`.
- Manager clarification: for a failed rule in an otherwise completed fit, preserve the selected penalized coefficients and compare their support with `support_audit`; a whole-fit failure still yields NA vectors.
- SPEC §3: F1/F2 gain two K37 rule rows. Their original rule logic and diagnostics are intended to remain unchanged; detached case reproduction is required before claiming invariance.
- AUDIT §3 / Sol R2-1: unrepresentable weights or normalized factors fail the fit rather than being floored.
- AUDIT §3 test migration and manager decisions: CV exactness on the F3 orthogonal canary is disclosed as a diagnostic; after a bit-identical deployed/v2 canary comparison, the same applies to F1/F2 CV exactness. Truth inclusion and EBIC exactness remain blocking, as does F1/F2 deployed-row identity. The evidence and G3 exception citation are in tests/TEST_REPORT.md.

Runner changes are the schema version, coefficient saving, and generation of NA coefficient evidence when the runner catches a failure. All changes are provisional pending the tests and independent review.
