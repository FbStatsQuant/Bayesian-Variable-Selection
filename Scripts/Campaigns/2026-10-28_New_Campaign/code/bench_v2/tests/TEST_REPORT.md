# Benchmark test report

## Current state (2026-10-30, frozen)

High-p manifest SHA-256: `8905f52e314f706b54f985994d7915052301c9e22912690264b7b27ab58b0373`; F3 source tree: `3e01c77b27ad96ad8ec4761b6b25ea5511d357e8aa08a1db7b2972e71734f42c`; low-p r2 manifest: `85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7`. D54 and r2 are reflected in the [Sol review](../review/SOL_REVIEW_1.md). The 24 controlled cases passed paired F1/F2 identity, F3 pilot identity, six-rule coefficient support and K37 comparisons. The revised runner passed 72/72, the earlier F2 legacy suite passed 24/24, F3 migrated canaries passed 14/14, the real runner/validator passed, and nine real-output corruption controls were rejected. Local execution used scoped R 4.4.1/glmnet 4.1-10 compatibility and Windows path wrappers, with production checks unchanged.

F1 legacy evidence is a **union**, not a single clean full-suite pass: the capped run passed complete 10b (skip, corruption refusal and refit) but failed stale four-row 9f; the six-rule run passed corrected 9f but failed 10b during its nested process. The manager's 11/11 10b recheck covered initial outputs and idempotent skip, a narrower scope than complete 10b. Sol accepted the combined evidence with that limit disclosed.

The local runner wrappers are `run_local_runner.R`, `run_local_f1_runner.R` and `run_local_f2_suite.R`; the scoped glmnet compatibility adapter is in `run_all_tests.R`.

Sol's verdict is high-p ACCEPT WITH FIXES and low-p r2 ACCEPT; both job bundles were REJECT pending the R1-1 validator fix, with R1-3 and R1-4 also outstanding in that review. R1-2 implementation-mutation controls and R1-5 current-state notes are fixed pending review. Schema-v2 consumers must use wrapper K37 rows and coefficient evidence; high-p scoring/analysis integration, low-p F2 alpha disclosure and independent table tie-out remain open release checks.

### R1-2 mutation rerun

The detached `run_review1_suite.R` run wrote `review1_suite.script_exit` = 0; `review1_suite.log` reports **72/72 pass, 0 fail**. It runs the entire top-level single runner under the existing local glmnet compatibility override, without setting `BENCH_V2_LOCAL_TEST` globally; hence the expensive optional F2 legacy subprocess was not repeated in this run (its earlier 24/24 is separate evidence). The F1 common, paired orthogonal and F3 migrated canary subprocesses were included. `review1_suite.stderr.log` records four locale startup warnings.

| Mutated real function | Positive guard on original | Same guard on mutant |
|---|---|---|
| EBIC candidate rank gate removed | PASS | assertion failed, as required |
| EBIC invalid RSS given finite scores: zero | PASS | assertion failed, as required |
| EBIC invalid RSS given finite scores: nonfinite | PASS | assertion failed, as required |
| EBIC picker reversed key tie order | PASS | assertion failed, as required |
| F3 selected second-stage KKT condition bypassed with fault retained, p=20/30/120 | PASS at each p | assertion failed at each p, as required |

The existing five implementation mutations (weights, full-p EBIC, fold Gram, index mapping and pilot KKT) each triggered their expected guard failure, and the deployed ridge weakness canary failed while v2 passed. Mutant functions were sourced into isolated test environments and the originals restored. The 23 frozen manifest entries were rehashed 23/23 successfully after this change; no benchmark-tree member was edited.

## Historical test notes

Command: `Rscript.exe --vanilla <bench_v2>/tests/run_all_tests.R`; local R 4.4.1 and glmnet 4.1-10 with the audit's local compatibility override. The latest run finished exit 0 with 71/71 top-level checks passing, including the adapted deployed F1 common suite's 11 checks, paired deployed/v2 F1 and F2 canaries, and the migrated F3 canary suite's 14 checks. Startup reported four Windows locale warnings; full output is in TEST_RUN.log.

After that run, the implementation-mutation helper was changed to source each mutated function copy into a test environment, as requested by the manager. A focused capped rerun exited 0 and passed 5/5 controls: unstable weights, screened-p EBIC, fold Gram, index mapping and pilot KKT propagation each caused the real guard to fail as intended (mutation_only.log and mutation_only.exit in repro/controlled_2a8362b2f348).

The revised full runner subsequently reported 71/71 passing in mutation_suite_capped.log and exited 0 after the F2 local-path-shim suite passed 24/24 (F2_capped.log).

- Stable overflow normalization and the 1e-12 weight example passed. The intentionally naive overflow normalization failed its assertion as intended. Unrepresentable reciprocal and underflowed normalized factor were rejected.
- Rank deficiency, EBIC key tie order, and zero RSS rejection passed. Forced rank validity, reverse key order, and forced finite invalid RSS each failed their assertion as intended.
- Mocked-pilot null and singleton fixtures at p=20, 30 and 120 passed basic output checks. Injected pilot KKT failures propagated; a changed successful-status negative control failed its assertion at each p.
- A real glmnet screened fit on a small synthetic dataset passed and each saved penalized vector matched its rule support.
- Added F3 determinism, normalized screened penalty factors, factor-rescaling invariance and a no-truth-input source check.
- On that small real fixture the F3 pilot matched the F1 v2 CV-min beta bit-for-bit, and F1/F2 penalized coefficient evidence matched the rule supports.
- Independently computed singleton fold CV means, standard errors and both choices passed for all three p values. Substituting the full-data Gram denominator in fold fits failed the check in each case.
- Permuted singleton fixtures at p=20, 30 and 120 mapped back correctly; an intentionally wrong map failed at each p. Injected selected-point KKT violations failed their CV rules and preserved penalized coefficients matching support_audit; masking those violations failed the guard. A hand-calculated full-p EBIC fixture picked a different model when p was replaced by screened m. Injected nonfinite RSS was rejected.
- Actual function-expression mutations for unstable normalization, screened-p EBIC, fold Gram denominator, index mapping and pilot KKT propagation each caused the corresponding guard to fail. An injected failed CV rule retained a finite penalized vector matching support_audit.
- Forced KKT failures in F1 and F2 also retained finite penalized vectors matching each failed rule's support_audit.

| SPEC test | Current evidence and remaining work |
|---|---|
| 1 ridge weakness / pilot identity | Correlated truth fixture passes v2 and fails deployed; all 24 controlled dev pilot identities pass against both snapshot F1 and original F1. |
| 2 pilot failure | Injected KKT and mutated implementation controls pass; includes p=20, 30, 120. |
| 3 m=0 / m=1 | Mock-pilot wrappers and independent full/fold scalar CV/choices pass for p=20, 30, 120; mutated Gram control fails as intended. |
| 4 weight extremes | 1e-12, overflowing sum and underflowed/unrepresentable weights checked; mutated normalization fails guard. |
| 5 mapping | Permuted singleton support checks at p=20, 30, 120 pass; mutated implementation fails guard. |
| 6 full-p EBIC | Hand calculation and screened-p changed-pick fixture pass; mutated implementation fails guard. |
| 7 rank deficiency | Invalid rank and infinite score checked, with forced-valid negative control. |
| 8 tie order | Criterion/k/key ordering checked, with reversed-key control. |
| 9 screened KKT | Selected-point KKT injection checked and failed rule coefficient audited at all three p values; masking control fails guard. |
| 10 coefficient consistency | Real small fits and all six rules for each method in all 24 controlled dev cases pass saved coefficient-support checks. |
| 11 RSS validity | Zero RSS and injected nonfinite RSS rejected; forced finite invalid-score control fails guard. |
| 12 K37 | Frozen derive_rules comparison passes on real n=200 fixture and all 24 controlled dev cases for all three methods. |
| 13 low p | Pilot failure, edges, scalar CV and permutation exercised for p=20 and p=30; weight normalization tested independently of p. |
| 14 deployed tests | F1 common 11/11 and F3 migrated canaries 14/14 passed; F2 local-path-shim rerun passed 24/24, and full adapted F1 is running. F2 diagnostic-only scripts are separately disclosed below. |
- The updated validator accepted a synthetic schema-v2 payload and rejected individual corruptions of schema version, rule id, role, extra column, coefficients, coefficient metadata, support, retired field and vocabulary. It also passed on the real end-to-end output and rejected each of those nine independent corruptions of that output; see VALIDATOR_RUN.log and VALIDATOR_CONTROLS.log.

## Real runner and validator

The real F3 runner's `main()` was executed through `tests/run_local_runner.R` with the dev manifest and the local-only audit compatibility override. It exited 0 and wrote F3.rds, F3.csv, F3.sha256 and F3.done for dev_p0500_S1_r001_c100. The done file records 244.22 s and completion at 2026-10-30T05:04:36Z. The runner's F3 source tree hash was `3e01c77b27ad96ad8ec4761b6b25ea5511d357e8aa08a1db7b2972e71734f42c`, and the input file hash was `ee045bfb113fee6cb3dd9451a77bf3067e0cada77b056317baf1b94035955f6f`. All six rows were ok, pilot k=78, index=73, and k values 64/51/15/15/15/15. The actual `validate_outputs.R --expect 1` run exited 0 with VALIDATION PASS. Nine one-field corruption controls each caused the validator to reject the affected payload. Production 5.1 gates were not altered.
- On an n=200, p=20 fixture, both K37 rows from each method matched the frozen derive_rules implementation's selected support, criterion and eligible maximum; changing the derivation cap to zero changed the F3 pick.
- The correlated n=40, p=160 fixture with four strong true variables passed the v2 ridge-weakness guard and failed on deployed F3. V2 maximum true weight 0.2097029 was below minimum noise weight 8.597449; deployed maximum true weight 1.326602 exceeded minimum noise weight 1.130285. Truth appeared on both paths. Excluded v2 noise variables count as infinite weight.
- The deployed F1 common suite initially passed 10/11 and failed its four-rule registry assumption. After adapting the fixture to six rows, it passed 11/11; the single runner now invokes it.

The adapted full F1 and F2 suites remain incomplete, so SPEC §4 is not yet complete. All 24 final-snapshot dev cases have passed pilot identity, support and K37 checks. The p=120 singleton fixture is a mock-pilot edge check. The five specifically requested stronger controls mutate implementation expressions; other controls also exercise intentionally corrupted outputs or assertions as described above.

The deployed F3 entry point was adapted to route v2 testing to the migrated canary suite; the original ridge-based body is retained below that adapter for historical reference. Its retired checks and replacements are listed individually in F3_RETIRED_TESTS.md. The local 4.1-10 override is gated by BENCH_V2_LOCAL_TEST; the production branch keeps the 5.1 version check. The migrated suite and run_all_tests cover parts of the former suite; full dev-data validation passed on 24 cases, F2's adapted suite passed, and F1's adapted suite remains running.

The copied F2 `diag_accuracy.R` and `diag_maxit.R` identify themselves as diagnostics rather than G3 tests; they remain byte-identical to deployed and have not been rerun. Launcher PID 36104 finished its F2 run exit 1, with 22/24 checks passing and the two Windows-path runner fixtures failing as documented below. The full local-shim rerun passed 24/24 and its parent exited 0.

The first F1 run exited 1; its stderr records an intermediate runner parse error (`unexpected symbol`), encountered while the adapted test was being edited. The current test and its paired fixture parse cleanly; a clean F1 rerun is queued. F2 has started. The original F1 run is not claimed as a passing suite.

Static inspection during the clean F1 run found three remaining four-rule expected vectors in its isolated KKT fixture 9f. The earlier adapted run subsequently reached that fixture and failed its four-element status expectation; its p=500 and p=1000 engine comparisons, all-grid KKT, rule recomputation and determinism checks passed. A second F1 run is active through an in-memory local test wrapper that extends the two fold-failure expectations to six rows and computes the expected K37 outcomes for full-path failure. This is a test harness change only; benchmark sources and the snapshot remain unchanged. Both runs' outcomes will be retained.

The first F2 legacy run reported failures in `runner_outer_failure` and `no_oracle_run_without_truth`: deployed's runner calls Windows `normalizePath` with its default backslash output and then checks for `/inputs/`. The test invokes that unchanged runner locally. A local-only F2 test wrapper sources the adapted test with a forward-slash normalization shim in its runner environment; the full rerun passed 24/24. The original failures remain recorded and no production runner check was changed.

The first F1 suite run reported its old hard orthogonal every-rule exact-recovery assertion as failed: cv_min selected `3;5;7;14;16;20;24;25;26`, cv_1se `3;7;14;16;24;25`, and all four EBIC rows selected the truth `3;7;14;16;25`. The running process loaded that earlier assertion; a rerun with the manager-approved split is queued after the F2 suite.

The same first F1 run also reported a failure of the deployed suite's hard p=500 no-intercept full-path tolerance: the shifted-y path differed by 0.00267174062318287 against the 1e-8 threshold; the centered comparison differed by 1.72911684970245e-12. The F1 glmnet helper is byte-identical to deployed. The paired deployed/v2 path check has now passed, as detailed under Disclosed reclassifications.

The manager authorized disclosure of this full-path tolerance conditional on exact deployed/v2 path identity, with KKT and zero intercept remaining blocking. The separate paired check exited 0; the full corrected F1 suite remains queued.

F2's adapted suite applies the manager's standing policy conditionally to the historically recorded generic-backend and shifted-response path tolerances: it first confirms byte-identical helper source, exact deployed/v2 coefficient paths and KKT diagnostics, KKT within tolerance, and zero intercept. The original support and RSS checks remain hard. Both results are disclosed below; the local-shim full-suite rerun passed 24/24. The historical failed thresholds and numerical-conditioning evidence are in deployed F2 `FAILED_ATTEMPTS.md`, item 2026-10-19 job 2275403.

The separate migrated F3 canary file `F3_AdaptiveLasso/tests/test_F3_v2_canaries.R` initially had a source-environment setup error, which was fixed. Its original-seed, 200-point canary initially failed the old hard CV-min exact-recovery assertion. Following the manager's decision below, the split canary passes all 14 blocking checks, including outer input and version failures; the side-by-side v2 and deployed ridge outcomes are saved in TEST_RUN.log.

## Disclosed reclassifications

F1's shifted-response p=500 full-path tolerance is disclosed as historical numerical conditioning after the paired check exited 0: deployed/v2 beta paths and KKT were identical for y, y+3 and centered y, every observed intercept was zero, and maxima of KKT were respectively 2.85264350e-8, 3.54200845e-8 and 2.85264369e-8 within the configured tolerance. The per-lambda maximum coefficient-difference median, p90, p99 and maximum were 2.08172020e-7, 4.06067481e-5, 1.57574142e-3 and 2.67174062e-3. The deployment record reports 2.1e-7, 4.1e-5, 1.6e-3 and 2.7e-3, with KKT at most 3.5e-8 ([F1 TEST_RESULTS.md](../../../../F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/methods_dev/F1_Lasso/TEST_RESULTS.md), §1 row 3a and §2). Exact paired paths, KKT and zero intercept remain blocking in the full rerun.

The first F2 legacy suite's shifted-response full-path tolerance yielded maximum relative difference 6.330179e-5 (per alpha 3.96e-6, 6.66e-6, 1.36e-5, 2.22e-5 and 6.33e-5) against 1e-8. It passed exact paired deployed/v2 path and KKT identity, KKT threshold, observed zero intercepts, original support and RSS checks. The helper is byte-identical to deployed, and the same 6.3e-5 failure and numerical-conditioning diagnosis are recorded in [F2 FAILED_ATTEMPTS.md](../../../../F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/methods_dev/F2_ElasticNet/FAILED_ATTEMPTS.md), line 5. The full local-shim rerun passed.

The F2 generic-backend full-path coefficient tolerance failed in the paired suite: alpha 0.1 maximum difference 1.315724e-5 versus tolerance 1.043544e-6, and alpha 0.9 maximum 0.0007028518 versus 1.769379e-6. The deployed and v2 helper files are byte-identical, paired deployed/v2 paths and KKT are identical, and the KKT and support checks passed. The deployment-era record reports the same failing assertion at alpha 0.1 (1.3e-5 versus 1.04e-6), attributes it to numerical conditioning, and records KKT evidence ([F2 FAILED_ATTEMPTS.md](../../../../F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/methods_dev/F2_ElasticNet/FAILED_ATTEMPTS.md), line 5). That old assertion stopped at alpha 0.1; the alpha 0.9 result above is additionally reported here. The full local-shim rerun passed.

The manager explicitly reclassified **CV-min exact recovery on the orthogonal canary** as a reported diagnostic for v2. Prediction-CV overselection is method behaviour in the audit; the original campaign accepted CV-min's orthogonal canary as a G3 exception ([REPORT_W3.md](../../../bench_audit/work_chain/REPORT_W3.md), Link 3; deployed F3 `FAILED_ATTEMPTS.md`, item 1 records the earlier rejected unilateral softening and the requirement for a lead decision). Truth inclusion in CV-min and exact recovery by ebic1 and ebic1_K37 remain hard checks. The deployed canary did not require exact ebic05 or ebic05_K37, so these are reported rather than added as blockers.

The manager conditionally extended the disclosure to F1 and F2 CV exact recovery after paired tests on their original fixtures. Under the same local environment, deployed and v2 **all four original rule rows were bit-identical for both methods** (PAIRED_ORTHOGONAL.log and paired_orthogonal_canaries.rds). F1 truth was `3;7;14;16;25`: deployed and v2 cv_min were `3;5;7;14;16;20;24;25;26`, and both cv_1se were `3;7;14;16;24;25`. F2 truth was `3;8;14;21;27`: deployed and v2 cv_min were `3;5;8;10;14;19;20;21;24;25;26;27`, and both cv_1se were exactly truth. For each method all four v2 EBIC/K37 rows selected truth. The adapted F1/F2 tests retain blocking checks for truth inclusion in both CV supports, exact recovery by all four EBIC/K37 rules and bit-identical deployed original rows. The same G3-exception citation applies.

Truth was `3;7;14;16;25`. V2 CV-min selected `3;7;10;14;16;21;25;30`; deployed ridge CV-min selected `3;7;14;16;21;25;30`. Both included truth. V2 and ridge CV-1se, ebic1 and ebic05 selected the exact truth; both K37 variants also selected the exact truth (ridge K37 re-derived from its candidate table).
