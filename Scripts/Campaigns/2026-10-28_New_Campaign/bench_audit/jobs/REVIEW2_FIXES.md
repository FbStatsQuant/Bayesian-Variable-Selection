# BENCH-FIX Sol review 2 — narrow implementation response

Only the bundle's `BENCH_F3_PROD/runner/validate.R` was changed among executable production files; frozen fitting/validator sources remain untouched. No fitting or SSH was performed. `tests/test_review2.R` reads Sol's rehashed counterexamples and writes its additional temporary corrupted records only inside the bundle test folder.

| Finding | Change | Check and result |
|---|---|---|
| R2-1 | Require each data/fold/method seed to exist and agree exactly across input, manifest, every result row and RDS case before either success or whole-fit-failure paths. | Three Sol saved records rejected specifically by `seed_binding_data_seed`, `seed_binding_fold_seed`, `seed_binding_method_seed`; the same three errors occur on rehashed whole-failure seed controls. Real and whole-failure positives pass. |
| R2-2 | Enforce zero-pilot support, coefficient/prediction vectors, all-row RSS, NA index/lambda, exact null path and frozen-function-recomputed null candidate and scores. | Sol's four rehashed records rejected as `null_sentinels`, `null_path`, `null_candidates`, `null_rss`; genuine null passes. |
| R2-3 | Source frozen `cv_choose`, `lambda_fraction`, `ebic_candidates`, `ebic_pick`, `occurrence_ok`; verify weighted grid, both CV choices/diagnostics and scores/statuses, full-p candidate table, capped minimizers and first passing occurrence/associated lambda. | CV substitution: `CV_choice_cv_min`; false EBIC criterion: `EBIC_score_ebic1`; wrong EBIC pick: `EBIC_pick_ebic1`; later occurrence: `EBIC_occurrence_ebic1`. Additional controls reject `weighted_lambda_grid`, `candidate_table`, `CV_diagnostic_choices`. Real and singleton positives pass. |
| R2-4 accepted | Both JOB.md files state the quarantine, record, escalate and never-accept treatment for zero-runtime whole-fit failures. | Existing zero-runtime saved record remains rejected as `runtime_s not one positive value per fit`; no frozen source changed. |

Results: **14/14** distinct saved-record R2 corruption controls, **3/3** whole-failure seed controls, **4/4** real/null/singleton/whole-failure positives, existing six branch corruption controls, and existing 17 earlier controls passed. Python suites: PROD **19/19**, DEV **2/2**. All local R/Python work was run with at most two processes, with no new fits.

These are implementation checks, not Sol's requested narrow independent check. The bundles remain blocked until that check and the ordinary OPS/dev-pilot gates.
