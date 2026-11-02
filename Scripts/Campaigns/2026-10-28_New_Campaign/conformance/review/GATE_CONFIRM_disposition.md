# Disposition of GATE_CONFIRM_sol.md (CONF manager, 2026-10-29)

Verdict received: ACCEPT WITH FIXES. There was one blocking follow-up, plus one documentation correction. Both are applied:

1. **Stage reports.** `compare_identity.R` now derives the expected `stages$pilot` and `stages$diag_grid_intervals` from the retained `calibration$tiers`, using the emitter's logic: the schedule length minus 1, and the grid length minus 1 per iteration. It requires them to be identical and non-empty with positive values, and checks the number of tiers against the expected escalation.
   - Verified on a real local v2.2 fit (`work/regression2/out_r3/p20_seed1001.rds`): it passes.
   - The `list(NULL)` diagnostic report and `pilot = 999` placeholders are rejected.
2. **JOB.md transfer order.** The ACCEPTANCE log is now produced on the downloaded copy *before* scratch is deleted.

Also confirmed: the C++ registry report emits `after_calibration` in the order `n_distinct`, `n_distinct_hll`, `log_sum_exp_F` (`code/core/v2_2/core/cpp/v3_core.cpp`, `cpp_registry_report`), so the script's order check matches the producer. This was the reviewer's uninspected point.

The dry-run negative controls were refreshed (`jobs/CONF_NOTS_IDENTITY/DRYRUN_negative_controls.log`): the historical v2.1 outputs posing as new, with an emptied manifest and a conflicting job record, fail and exit 1.

**Bundle status: ready to submit via HQ → OPS.**
