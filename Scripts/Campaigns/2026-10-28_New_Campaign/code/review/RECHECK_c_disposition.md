# Disposition of RECHECK_c_sol.md (LOWP manager, 2026-10-29)

Fixed by the manager (small, local changes):

| Finding | Fix | Evidence |
|---|---|---|
| N1 derived row `ok` despite captured conditions | `bench_lowp/R/common.R::lowp_derive`: a successful derived row is `warning` iff the fit captured any condition (`n_warnings > 0` on any original row, or any original `warning` status), independent of the original rows' failure status | Sol's `edge_probes.R` replayed on the fixed code: derived status `warning` (expected `warning`), n_warnings = 1 |
| N2 restricted-rule `k_valid_max` / `ebic_at_largest` | computed from the rule's own eligible candidates; `k_path_max` unchanged | same probe: k_valid_max 1 (expected 1), diag_codes `ebic_at_largest` (expected) |
| N3 LA-4 missing from `adaptation_ids` | `run_bench_case.R`: F1–F4 `LA-1;LA-4`, F5 `LA-1;LA-2;LA-4` | smoke rerun: every F-method row carries LA-4 |

Regression: full smoke rerun (`smoke/smoke3.R`, outroot `…/lowp_work/bench_smoke_reviewfix_v6`): 60/60 checks (48 fits, resume, dev, tamper exit 1, forced failure exit 2, identity mismatch exit 1); `smoke/derived_checks.R`: 122/122. The probe replay ran from a copy in `…/lowp_work/mgr_probe/` but writes to Sol's scratch path, so `…/recheck_c/edge_probes.rds` and `adaptation_provenance.csv` now hold the post-fix replay (Sol's pre-fix values are quoted in RECHECK_c_sol.md).

Status: no further Sol re-check commissioned for these three items (manager-verified with Sol's own probes); they are included in the final LOWP review scope if HQ wants one.

## FINAL_CONFIRM FC3 (2026-10-29, manager)

`lowp_derive` now also treats captured warning or message text on the original rows as a condition (failure precedence unchanged). Regression `bench_lowp/smoke/test_derived_conditions.R`: no-condition → ok (k_valid_max 1, ebic_at_largest), warning-only → warning, message-only → warning; all pass.
