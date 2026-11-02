# FIELD_MAP: native SMC-BVS fields read by `scoring/R/extract_smc.R`

`extract_smc(record)` is the only place that knows native field names. The table at the top of that file (`FIELD_MAP`) is the single source; this file is generated from it.
A record is the study-adapter envelope (`code/core/v2_2/study/SCHEMA.md`, `adapter_version 2.2-R1`). Paths are relative to the record; alternatives are tried left to right and the first non-NULL wins. `$` separates list levels.

Status: **code** = verified by reading the v2.2 core (`v3_fit.R`, `v3_run.R`, `core/cpp/v3_core.cpp`) and the adapter (`study/adapter.R`), and exercised on one real p = 20 fit (`tests/INTEGRATION_REPORT.md`); **provisional** = name not yet defined by `conformance/OUTPUT_FIELDS.md` (which did not exist when this was written).

| Name | Paths (tried in order) | Status | Meaning |
|---|---|---|---|
| `native_status` | `native_status` ; `fit$status` | code | adapter native_status (completed/exact/failure statuses) |
| `estimates_available` | `estimates_available` ; `fit$estimates_available` | code | logical |
| `runtime_s` | `runtime_s` | code | wall seconds around the core call |
| `method_seed` | `case$method_seed` ; `fit$seed` | code | data seed + 4e6 (+1000 m for repeat m) |
| `log_Z` | `fit$log_Z` | code | pooled log Z-hat, full working scale |
| `log_Z_r` | `fit$log_Z_r` | code | 4 island log Z-hat_r |
| `log_Z_lower95` | `fit$log_Z_lower95` | code | native log(0.05)+log_Z |
| `log_Z_rel_m0` | `fit$log_Z_rel_m0` | code | relative to m(empty) |
| `log_m0` | `fit$log_m0` | code | log m(empty) |
| `pip_primary_full` | `pip` ; `pip_primary_original` | code | record$pip: length-p vector, zeros for dropped columns |
| `pip_primary_retained` | `fit$pip_primary` | code | retained-column named vector (names = original index) |
| `pip_r` | `fit$pip_r` | code | retained-p x R matrix, rownames = original index |
| `mpm` | `fit$mpm` ; `mpm` | code | strict PIP > 1/2 on the RB PIP |
| `hpm` | `fit$hpm` ; `hpm` | code | sorted original-index support |
| `hpm_F` | `fit$hpm_F` | code | F of the HPM |
| `pip_plain_full` | `pip_plain` | code | plain (non-Rao-Blackwellised) PIP, length-p; NA for exact fits |
| `pip_plain_retained` | `fit$pip_plain` | code | retained vector |
| `pip_plain_r` | `fit$pip_plain_r` | code | retained-p x R matrix |
| `mpm_plain` | `mpm_plain` ; `fit$mpm_plain` | code | plain-PIP MPM |
| `kept` | `fit$preprocessing$kept` | code | retained original indices |
| `flag_escalated` | `fit$flags$escalated` | code | tier 1 used |
| `flag_checks_passed_final` | `fit$flags$checks_passed_final` | code | FALSE = a final check failed |
| `flag_E1` | `fit$flags$E1` | code | final E1 |
| `flag_E2` | `fit$flags$E2` | code | final E2 |
| `flag_E3` | `fit$flags$E3` | code | final E3 |
| `flag_low_ess` | `fit$flags$low_empirical_ESS` | code | any final-stage ESS < 0.5 N_e |
| `flag_local_limit` | `fit$flags$local_limit` ; `fit$local_limit` | code | local search hit its move cap |
| `flag_grid_unconverged` | `fit$flags$grid_unconverged` | code | calibration grid not converged |
| `flag_near_tie_truncated` | `fit$flags$near_tie_truncated` | code | near-tie store truncated |
| `flag_cut_group` | `fit$flags$cut_group` ; `fit$cut_group` | code | a correlated group spans >= 2 blocks |
| `flag_local_certified` | `fit$local_certified` | code | returned HPM is a scanned centre with no improving neighbour |
| `stage_table` | `fit$stage_table` | code | phase,tier,iter,island,...,ess,... (final rows phase == 'final_bridge') |
| `score_fresh` | `fit$score_counts$fresh` | code | mechanism matrix of fresh scores (final ledger) |
| `score_logical` | `fit$score_counts$logical` | code | mechanism matrix of logical scores (final ledger) |
| `tier` | `fit$settings$tier` | code | final tier |
| `n_stages_final` | `instrumentation$stages$final` ; `fit$instrumentation$stages$final` | code | number of final bridge stages |
| `blocks` | `fit$blocks` | code | packed blocks (original indices) |
| `log_mass_scored` | `instrumentation$scored$log_sum_exp_F` ; `fit$instrumentation$scored$log_sum_exp_F` ; `fit$log_mass_scored` | code (v2.2 registry; name of the derived scalar log_mass_scored is provisional) | log sum over DISTINCT scored S of exp F(S) (v2.2 registry, exact mode p <= 64); = log_mass_scored |
| `n_distinct_scored` | `instrumentation$scored$n_distinct` ; `fit$instrumentation$scored$n_distinct` | code (v2.2 registry) | distinct scored models |
| `scored_set` | `instrumentation$scored_set` ; `fit$instrumentation$scored_set` | code (v2.2 registry) | data.frame key (bitmask over retained positions), size, first_phase, first_mech, first_tier, first_iter, first_island, first_stage (p <= 32) |
| `truth_trace` | `instrumentation$truth_trace` ; `fit$instrumentation$truth_trace` ; `fit$truth_trace` | provisional | PROVISIONAL: in-fit trace of the truth model if the sibling thread adds one: list(scored, first_phase, first_mech, ...). Truth never enters fits, so by default scoring derives it from scored_set. |

## Notes

- v2.2 additions confirmed in the code: `fit$pip_plain`, `fit$pip_plain_r`, `fit$mpm_plain` (completed SMC fits only; absent on the exact branch), `record$pip_plain`, `record$mpm_plain`, `record$instrumentation` (= `fit$instrumentation`: `stages`, `best_before_local`, `best_after_local`, `stop`, `escalation`, `cut_group_large`, `version`, and for SMC fits `scored` = registry report and, for p <= 32, `scored_set`).
- `log_mass_scored` is **derived**: `fit$instrumentation$scored$log_sum_exp_F` (log sum over distinct scored models of exp F, exact mode, p <= 64). It lives on the same scale as `log_Z` because F = log varpi + log m and Z = sum exp F. If the sibling thread adds a flat top-level field, add its path to the `log_mass_scored` row.
- `truth_trace` is provisional and expected to stay NA: truth never enters a fit, so by default scoring derives the truth trace after the fact from `scored_set` (`truth_trace_from_scored()` in `R/theory_measures.R`).
- Island PIP components: `pip_r` (RB) and `pip_plain_r` are retained-p x 4 matrices with rownames = original index; `extract_smc` expands them to length p (zeros for dropped columns).
- Flags are read from `fit$flags` (E1, E2, E3, low_empirical_ESS, local_limit, near_tie_truncated, checks_passed_final, escalated, grid_unconverged, cut_group); `cut_group` also at top level of the fit.
- **Validation (review findings 8, N2, N3)**: a full-length PIP vector (adapter `record$pip`) is accepted only as a valid probability vector with names a permutation of 1..p (reordered to the canonical order; duplicates / unknown names rejected) whose confirmed dropped columns are 0; retained vectors and island matrices are accepted only if their names cover exactly `preprocessing$kept`, values are in [0, 1] and matrices have four island columns; otherwise the field is unavailable (`rb_ok` / `plain_ok` FALSE), never padded with zeros. Evidence (`evidence_ok`) needs a finite `log_Z` and, for a completed SMC fit, four finite `log_Z_r`; the native `exact` branch (no islands) keeps its pooled evidence, and `islands_ok` (four finite islands) gates the island errors and SE. The final stage rows are those with `phase == 'final_bridge'` (the real label, checked on a real p = 20 fit; calibration rows are `pilot` / `diag`); there is no fallback to other phases. Absent or all-NA counts stay NA. Scored-set fields are read only for a completed fit.
- The CSV rows of the record (`record$rows`) give the `hpm` / `pip05` supports for the selection tables (`smc_rule_rows()`); everything else is read from the RDS.
