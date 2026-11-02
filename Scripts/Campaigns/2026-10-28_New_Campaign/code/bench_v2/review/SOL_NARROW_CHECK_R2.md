# Sol narrow check of review-2 fixes

Independent Sol 6.1 check, 2026-10-30, under HQ D48/D53/D54. **R2-1, R2-2 and R2-3 are RESOLVED; R2-4's requested operator sentence is present in both JOB files.** No remaining acceptance-gate defect was found in this narrow scope.

| Deliverable | Final verdict | OPS disposition |
|---|---|---|
| (c) BENCH_F3_DEV | **READY FOR OPS** | DEV first, subject to the documented OPS environment, staging and submission gates. |
| (d) BENCH_F3_PROD | **READY FOR OPS** | PROD submission remains conditional on an inspected NOTS DEV pilot and resources filled from that pilot. Placeholder resources and local test timings do not satisfy this gate. |

These verdicts clear the review-2 bundle defects for OPS handoff. They do not certify a completed NOTS pilot or authorize bypassing JOB requirements. This was a narrow check, not a new full review or numerical campaign.

## Observed finding results

All checks below invoked the fixed `BENCH_F3_PROD/runner/validate.R` through `validate_prefix`, including its frozen saved-file validator, hashes, input and manifest context. The nine retained round-2 counterexamples were read directly from `sol_scripts_r2/corruptions/`; they were not regenerated or edited. New counterexamples were serialized and rehashed under `sol_scripts_r3/corruptions/` before validation. The script asserts each complete reason string exactly.

| Finding | Status | Independently observed result |
|---|---|---|
| R2-1: seed binding | **RESOLVED** | Retained `extra_data_seed`, `extra_fold_seed`, `extra_method_seed` rejected respectively as `seed_binding_data_seed`, `seed_binding_fold_seed`, `seed_binding_method_seed`. The same three independently rehashed mutations on the genuine positive-runtime whole-fit-failure record produced the same respective reasons. Both original records passed. |
| R2-2: null contract | **RESOLVED** | Retained `null_index_lambda` rejected as `null_sentinels`; `null_path` as `null_path`; `null_candidates` as `null_candidates`; primary-CV `null_CV_RSS` as `null_rss`. The genuine null fixture passed. |
| R2-3: rule selection and scores | **RESOLVED** | Retained `cv_min_replaced_by_cv_1se` rejected as `CV_choice_cv_min`; retained ebic1 `crit_value=123456` (`extra_EBIC_criterion`) rejected as `EBIC_score_ebic1`. The new wrong-K37 substitution and later-occurrence control below were also rejected at their intended selection checks. |
| R2-4: accepted zero-runtime behavior | **RESOLVED (documentation; accepted behavior retained)** | The exact requested sentence is present in DEV `JOB.md:60` and PROD `JOB.md:69`: retain/quarantine four files and logs, record the `runtime_s not one positive value per fit` refusal, escalate under failed-unit policy, never count as accepted or silently omit. No runtime exception or frozen-source change was introduced. The zero-runtime record was not rerun in this narrow check; round-2's accepted refusal stands. |

The seed loop precedes the whole-failure return and requires every seed in the manifest, consumed input, RDS case and every result row, with exact value comparison and no missing values. Existing input-file and component-hash checks remain. The null branch now checks support/zero vectors and predictions, NA lambda/index sentinels, declared one-row path, recomputed null candidate and full-p scores, and RSS on all six rows.

## R2-3 selection-code inspection and new control

I read the revised wrapper and the frozen `common.R`, `methods/glmnet_helpers.R` and `methods/fit_F3_alasso.R` that define the relevant semantics. The wrapper sources the actual frozen helpers rather than implementing alternate selection rules:

- `cv_choose` supplies both choices, including first/largest-lambda exact minimum and first eligible one-SE index. The wrapper binds diagnostics, row indices/lambdas, CV mean/SE, support and failed-status logic to those choices.
- `ebic_candidates` is called with the full consumed X, so the combinatorial penalty uses full **p=500**, not screened p. It reconstructs the null plus distinct mapped supports, frozen OLS rank/positive-finite-RSS gates and both gamma scores. Frozen `kmax_ebic` is **100**. K37 rules further filter to `k <= floor(n/log(n))`, which is **37** for this n=200 record.
- `ebic_pick` retains `order(crit, k, key, method="radix")`, including its deterministic byte-order tie break. The wrapper compares the saved candidate table, selected support, RSS, `ebic1_value`, rule criterion, eligible valid maximum and path maximum.
- EBIC indices must select the **first full-data-KKT-passing occurrence** of the chosen support on the decreasing lambda grid, hence the largest passing lambda. The no-passing-occurrence fallback, failed status and null-support exception follow the frozen `occurrence_ok`/producer semantics. Fold KKT is used for CV's status rules; it is not incorrectly added to frozen EBIC occurrence eligibility.
- The second-stage grid is recomputed as `max_mult * max(abs(X_keep' y)/n/v) * lambda_fraction(GRID)`, using the checked pilot weights and frozen grid settings. Existing selected-coefficient KKT and OLS evidence checks remain after selection validation.

**One new substitution of my own design:** the saved p500 record's unrestricted and K37 EBIC1 picks coincide (k=15, index=88), so merely copying one to the other would not be a corruption. Instead, I attributed the actual CV-one-SE **k=51, index=169** support to `ebic1_K37`. This candidate is valid in the cap100 table but ineligible for K37. I copied its actual penalized coefficients, recomputed its zero-intercept OLS coefficients and used its true full-p RSS/EBIC1 score; I updated CSV/RDS rows, fit rules and both coefficient copies consistently, retaining the target rule ID. The rehashed saved record was rejected exactly as **`EBIC_pick_ebic1_K37`**. Retained evidence: `sol_scripts_r3/corruptions/K37_from_actual_k51_cv1se/`.

I also repeated the original finding's later-occurrence acceptance control: move ebic1 from index **88 to 89**, a later full-data-KKT-passing occurrence of the same support, with matching lambda and both coefficient metadata copies. It was rejected exactly as **`EBIC_occurrence_ebic1`**, before coefficient KKT testing. Evidence: `sol_scripts_r3/corruptions/later_ebic1_occurrence/`.

The shipped `tests/test_review2.R` was inspected. I used an independent review-local saved-record harness instead of executing its bundle-local temporary-file writes. Its additional grid/candidate/diagnostic controls were not claimed as independently rerun here.

## Positives, regression checks and integrity

The actual p500/S1/r001/c100 six-rule record and genuine null, singleton and positive-runtime whole-failure fixtures all passed (**4/4**). Original p500 CV-min remains k=64/index=200 and CV-one-SE k=51/index=169. Overall: **18/18 targeted saved-record checks** passed, comprising four positives, nine retained corruptions, three whole-failure seed corruptions, the new K37 substitution and the later-occurrence control.

The actual Python suites were independently rerun sequentially: **PROD 19/19**, including real-record reconciliation through the actual R wrapper, and **DEV 2/2**. Tests' explicit temporary directories were redirected under `sol_scripts_r3/tmp/`; bytecode writes were disabled. No tests or deliverables were edited.

| Integrity target | Observed SHA-256 | Verification |
|---|---|---|
| `code/bench_v2/MANIFEST_SHA256.txt` | `8905f52e314f706b54f985994d7915052301c9e22912690264b7b27ab58b0373` | **23/23 members unchanged** |
| Low-p r2 manifest | `85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7` | **34/34 members unchanged** |
| DEV `BUNDLE_SHA256SUMS_FINAL` | `d5da3b0d57b5d6f3c885c7014e2eafaa7667c8e02999b113186ebb1760a4c4d4` | **28/28**, unique entries, every digest matches |
| PROD `BUNDLE_SHA256SUMS_FINAL` | `9129e5df92d5055376f42cdb1ccf1e53f2c8353fdddc4337ad70e7f26cc44827` | **65/65**, unique entries, every digest matches |

The actual `BENCH_F3_PROD/runner/frozen.py check` returned **`FROZEN_OK`**, exit **0**, against the real F3 tree, high-p manifest and `runner/freeze.json`. Frozen F3 source digest remains `3e01c77b27ad96ad8ec4761b6b25ea5511d357e8aa08a1db7b2972e71734f42c`. Before/after verification around the Python suite confirms **155/155 snapshotted deliverable files unchanged**, and **144/144 retained round-2 corruption files unchanged**.

## Evidence and limits

Evidence is under [sol_scripts_r3/](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r3/). The inspected execution logs are `check_narrow.log` and `check_python_integrity.log`; both corresponding `.exit` files are **0**. Source/configuration snapshots, SHA-256 lists, new four-file corruptions, timestamps, environment details and final audit are retained there. R ran 2026-10-30 **16:29:52–16:29:55 UTC**; Python checks ran **16:30:45–16:30:54 UTC**. R 4.4.1 startup locale warnings are retained in stderr and did not affect the checks.

Reproduction uses absolute scripts: `powershell -NoProfile -ExecutionPolicy Bypass -File <absolute sol_scripts_r3/run_r.ps1>` and then the corresponding `run_python.ps1`; their exact executable/script paths and redirections are in the retained wrappers. The first direct PowerShell wrapper invocation was refused by the local script execution policy before R started; the process-scoped invocation above completed successfully. This changed no persistent policy. A repeat final audit is `python -B <absolute sol_scripts_r3/seal_evidence.py>`.

Local only as explicitly requested: **no SSH/NOTS, no new fits, no delegation, no broad full-round suite**. R/Python workloads were sequential, with at most a Python parent plus one child process, and one numerical thread. All new files are confined to `sol_scripts_r3/` and this output file. Prior numerical acceptance is preserved by the verified freezes. Actual NOTS environment, scheduler, accounting, pilot measurements and PROD resource filling remain OPS work; final downstream consumer/table release gates from round 2 still stand.
