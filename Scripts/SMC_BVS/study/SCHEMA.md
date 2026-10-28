# Study adapter schema: binding R-1

Authority: deployment `RULINGS_LEAD.md`, R-1 (2026-10-22 19:25Z), and `BRIEF.md` with amendments. This describes live adapter `schema_version=2L`, `adapter_version="2-R1"`. Historical v1 snapshots and outputs retain their original unresolved mapping and are not rewritten. No production-core field or statistical setting is changed by this adapter.

## Unit and file contract

One dataset/scale produces exactly two rows, in order `hpm`, `pip05`, at `results/RUN_ID/pPPPP/CASE_ID/SMCBVS.{rds,csv,sha256,done}`. `CASE_ID` includes `c100` or `c050`. `.rds` is R serialization version 3, xz compressed. `.csv` is `utils::write.csv(rows, row.names=FALSE, na="NA")`; strings are quoted, embedded quotes doubled, and embedded newlines preserved. R logicals serialize as `TRUE`/`FALSE`/`NA`. Missing support is NA, while a valid empty support is the quoted empty string `""`; readers must preserve that distinction. Use the RDS for exact condition boundaries, empty supports and native types.

`.sha256` has two lines, each `SHA256  BASENAME`, for the RDS then CSV. `.done` is written last, with `status STATUS_HPM,STATUS_PIP05` and `finished_utc UTC_TIMESTAMP`. A directory lock `SMCBVS.lock/owner.txt` contains PID, host and UTC during writing; stale locks require inspection. Each file is staged and renamed atomically. A done unit is reusable only after checksum, run/method/case/seed/source/policy/allocation/manifest/input identity checks. A valid historical unit with different identity requires a new run ID. Input container/manifest hashes cover validated fold provenance even though row fold fields are NA.

## Exact CSV column order

The same ordered columns are in `record$rows`. There are no CSV list columns. `sel_a01` through `sel_a14` and `pip_a01` through `pip_a14` below are literal columns, not wildcard names.

```text
study,run_id,source_sha256,regime,p,scenario,replicate,scale_key,scale,dataset_id,case_id,data_seed,fold_seed,method_seed,inputs_sha256,x_sha256,y_sha256,fold_sha256,method_id,method_label,package,package_version,rule_id,role,status,converged,diag_flag,diag_codes,n_warnings,warnings,messages,error,k,support,support_audit,tp,fp,fn,exact,error_type,sel_a01,sel_a02,sel_a03,sel_a04,sel_a05,sel_a06,sel_a07,sel_a08,sel_a09,sel_a10,sel_a11,sel_a12,sel_a13,sel_a14,pip_a01,pip_a02,pip_a03,pip_a04,pip_a05,pip_a06,pip_a07,pip_a08,pip_a09,pip_a10,pip_a11,pip_a12,pip_a13,pip_a14,max_pip_null,runtime_s,host,slurm_job_id,slurm_array_task_id,started_utc,finished_utc,v3_version,v3_source_sha256,v3_status,v3_estimates_available,v3_partial_results,v3_p_retained,v3_target_scale,v3_flags_json,allocation_sha256,input_manifest_sha256,adapter_mapping_status,adapter_policy_id,adapter_policy_sha256
```

Types below describe RDS row values before scoring; CSV itself is text. Fields that are not available are NA. Unfilled scoring columns are logical NA placeholders until the scoring step assigns their target types.

| Column(s) | Type / exact meaning |
|---|---|
| `study`, `regime` | Character constants `bench20261019`, `H`. |
| `run_id` | Character immutable run label; starts alphanumeric, then alphanumeric/underscore/dot/hyphen. |
| `source_sha256` | Character SHA-256 of ordered `code$files` labels and hashes, including core and study files. |
| `p`, `scenario`, `replicate` | Integer input design, p=500/1000, scenario=1..6, replicate=1..100; assessment selection of r=1..10 is the runner's responsibility. |
| `scale_key`, `scale` | Character `c100`/`c050`; numeric 1/0.5. |
| `dataset_id`, `case_id` | Character validated IDs; dataset excludes scale, case includes it; development uses `dev_` prefix. |
| `data_seed`, `method_seed` | Integer ID-derived seed, and data seed + 4000000; identical across paired scales. |
| `fold_seed`, `fold_sha256` | Always integer NA / character NA, respectively. Sampler does not use folds. Validated input values survive in RDS. |
| `inputs_sha256` | Character SHA-256 of the on-disk input RDS, checked before deserialization. |
| `x_sha256`, `y_sha256` | Character SHA-256 of stored X / selected Y column before standardization. Column-major doubles, little endian, no R serialization. |
| `method_id`, `method_label`, `package`, `package_version` | Character constants `SMCBVS`, `SMC-BVS v3`, `SMCBVS-v3`, `3`. |
| `rule_id`, `role` | Character `hpm` / `primary`, then `pip05` / `S0`. |
| `status` | Character `ok`, `warning`, `failed`; mapping below. Reconciliation alone may later create `timeout` or `not_run`. |
| `converged` | Logical NA on every row: no solver convergence criterion. |
| `diag_flag` | Nonmissing logical, identical on both rows, independent of status/support. |
| `diag_codes` | Character semicolon-separated ordered codes below; empty string when none. |
| `n_warnings` | Integer count of captured warnings plus captured messages, including repeats. |
| `warnings`, `messages` | Character condition text joined separately with literal ` | `; NA when no corresponding conditions. Every constituent text is verbatim, including newlines. The join is not an unambiguous encoding; RDS vectors preserve boundaries. |
| `error` | Character captured error text, or synthetic failure explanation `v3_status=STATUS; rule estimate unavailable` / `v3_status=STATUS; incomplete fit; support is audit only`; NA otherwise. Native `fit$message` remains separately in the raw fit. |
| `k` | Integer support size on nonfailed rule; NA on failed rule. |
| `support` | Character sorted original 1-based indices separated by semicolons; `""` is a valid empty selection; NA on failed rule. |
| `support_audit` | Same encoding of returned/derived HPM or PIP support on failed rule, if supplied; valid empty audit support is `""`; NA when unavailable or rule nonfailed. |
| `tp`, `fp`, `fn`, `exact`, `error_type` | NA until benchmark scoring assigns counts, exact-recovery indicator and error classification. |
| `sel_a01` ... `sel_a14` | NA until scoring assigns active-variable selections. |
| `pip_a01` ... `pip_a14`, `max_pip_null` | NA until scoring assigns values from full primary RB PIP; adapter does not read truth. |
| `runtime_s` | Numeric whole-fit wall elapsed seconds around the core call plus adapter output validation, shared by both rules. Compilation/loading and file serialization are outside this timer. |
| `host` | Character node name. |
| `slurm_job_id`, `slurm_array_task_id` | Character environment values, otherwise NA; unused on Owls. |
| `started_utc`, `finished_utc` | Character UTC timestamps `YYYY-MM-DDTHH:MM:SSZ` around timed fit. |
| `v3_version` | Character `3`. |
| `v3_source_sha256` | Character aggregate SHA-256 of core files only. |
| `v3_status` | Character native status, or adapter extension `adapter_error`; the unmodified raw native return, including its original status, is always `record$fit`. |
| `v3_estimates_available` | Logical: status exact/completed and native availability not explicitly FALSE. Retained failed PIPs remain audit-only even if supplied. |
| `v3_partial_results` | Logical: native `partial_results=TRUE` or native status schedule/numerical/resource limit. |
| `v3_p_retained` | Numeric/integer native `fit$p`, else preprocessing p, else NA. Distinct from input row `p`. |
| `v3_target_scale` | Character `standardised working model; not raw-data marginal likelihood`. |
| `v3_flags_json` | JSON string with `flags`, `cut_group`, `cut_group_count`, `cut_group_components`, `local_limit`, `local_certified`, `global_certified`, `near_tie_truncated`; absent/NA are JSON null, scalars auto-unboxed. Full nested flags/searches remain in RDS. |
| `allocation_sha256` | Character SHA-256 of version-3 serialized normalized allocation list. |
| `input_manifest_sha256` | Character SHA-256 of verified input-manifest file. |
| `adapter_mapping_status`, `adapter_policy_id` | Character constants `adopted`, `R-1-20261022`. |
| `adapter_policy_sha256` | Character SHA-256 of version-3 serialized fixed R-1 policy. Computed mapping fields/provenance override any stale values passed in a historical design. |

## Binding status and diagnostics

| Native status | Study status |
|---|---|
| `exact`, `completed` | `ok`; `warning` iff any R warning or message was captured. A missing required rule estimate fails that rule. Successful malformed output becomes `adapter_error`. |
| `schedule_limit`, `numerical_failure`, `resource_limit`, `invalid_input` | `failed`, regardless of conditions or diagnostics. |
| `y_constant`, `no_predictors` | `failed` on both study rules, preserving native status and any empty HPM in audit. |
| `adapter_error` | `failed`, preserving raw core return and independently valid audit outputs. |

v2.1 (A-CODE F3): an uncaught R-level memory-allocation error (`cannot allocate`, `std::bad_alloc`, `bad allocation`) is recorded like any other R error from the fit: native `adapter_error` with `fit = NULL`, both rules `failed`, error text verbatim, `.done` written. A process killed by the scheduler writes no `.done` and is classified by the runner. `timeout` and `not_run` are never inferred or emitted by this adapter. Diagnostic codes and native explanatory text do not change study status or selections. No captured conditions means diagnostics alone cannot create `warning`.

`diag_flag=TRUE` iff `checks_passed_final` is explicitly FALSE, or `low_empirical_ESS`, `grid_unconverged`, or a native `local_limit` is explicitly TRUE. Missing/NA checks did not fail and do not produce NA in the flag. These rules apply equally to exact, completed and failed rows. Flags are looked up in `fit$flags`, then a same-named top-level fit field, then `fit$calibration$flags` when absent. Calibration E1/E2/E3 triggers are not final-island checks.

Local-limit is a failed-anywhere check: OR explicit `local_limit=TRUE` in fit flags/top level, final `local_search` (including archived `partial_final$local_search`), calibration flags and `triggers_by_tier`, and each calibration tier's `triggers`, pilot search, iteration searches and failed `partial_operation$local_search`. A later FALSE never erases an earlier TRUE. This includes a failed post-search time guard before top-level final flags were assembled. Native structures are inspected without modification.

Codes are emitted once in this order when applicable:

1. `final_check_E1`, `final_check_E2`, `final_check_E3`: corresponding final E flag TRUE and `checks_passed_final=FALSE`.
2. `low_empirical_ESS`, `grid_unconverged`, `local_limit`: corresponding named quality check fired.
3. Informational only: `escalated`, `cut_group`, `near_tie_truncated`, `forced_pilot_steps`, `exact_branch`, `local_certified_false`, `global_certified`.

Informational booleans require TRUE, except `local_certified_false` requires explicitly FALSE and `forced_pilot_steps` accepts the native nonnegative scalar numeric/integer count and emits the code only when count > 0 (logical fixture values remain accepted). Zero/NA counts do not emit it. `exact_branch` follows native status exact, actual `branch_run="exact"`, or an explicit exact-branch flag; the branch decision alone is not enough to assert execution. An exact fit without SMC flags has `diag_flag=FALSE`. Informational codes never set the flag. A failed final summary without individually supplied E flags sets the flag without inventing a code.

## Exact RDS envelope

All following top-level keys are present. Native keys beneath `fit` are branch-dependent and are retained in full, without a whitelist, including any future extra keys.

| Key | Type / contents |
|---|---|
| `schema_version`, `adapter_version` | Integer `2L`, character `2-R1`. |
| `rows` | Two-row data.frame with exact ordered CSV schema above. |
| `fit` | Entire native core return unchanged; NULL if call threw before returning; even malformed raw returns survive. Native `message` is not a captured R message. |
| `pip`, `pip_primary_original` | Identical numeric vectors of input p, names `"1"`..`"p"`. Valid supplied retained primary PIPs are expanded with zero for dropped predictors, including on failed fits. If unavailable, all NA. Raw retained primary vector also survives unchanged in `fit$pip_primary`. |
| `hpm`, `mpm` | Sorted integer original-index supports, possibly integer(0), else NULL. On failure these are audit-only. If failed fit supplies MPM it is retained; if only valid primary PIPs are supplied, strict >0.5 yields its audit MPM. Successful MPM must equal that threshold. |
| `native_status` | Character mapped native status or `adapter_error`. Original returned status remains in `fit$status`. |
| `estimates_available` | Logical same as row `v3_estimates_available`. |
| `warnings`, `messages` | Separate ordered character vectors of verbatim `conditionMessage()` strings, length zero if none. Repetition, internal/trailing newlines and literal separators retained. |
| `error` | Captured error character scalar, else NULL; synthetic row failure explanations are not substituted here. |
| `runtime_s` | Numeric elapsed seconds, same as rows. |
| `case` | Named list: `dataset_id`, `case_id` (character); `p`, `scenario`, `replicate` (integer); `scale_key` (character), `scale` (numeric), `development` (logical); `data_seed`, validated input `fold_seed`, `method_seed` (integer). Row fold_seed is NA even though case retains benchmark provenance. |
| `input` | Named list: character `input_path`, `manifest_path`, `manifest_sha256`; one-row all-character data.frame `manifest_row` as read; character `inputs_sha256`, `x_sha256`, `y_sha256`, validated input `fold_sha256`. The manifest row includes original benchmark fields unchanged. No X/Y/fold vector/truth is added to this envelope. |
| `code` | Named list: character `core_dir`, `study_dir`; named character SHA vector `files` labelled `core/...` or `study/BASENAME`; character `source_sha256`, `v3_source_sha256`. Files sorted by full path; aggregate hash is SHA-256 of `paste(names(h), h, collapse="\n")`, no serialization. Includes core R files, cpp/h/v3 files in cpp/, all study R/md files. |
| `adapter_policy` | Exact fixed list described below; contrary policy arguments/files rejected in development and production. |
| `adapter_policy_sha256` | SHA-256 of `serialize(adapter_policy, NULL, version=3)`, `serialize=FALSE` in digest. |
| `allocation` | Named list `mem_gb`, `hours`, each positive finite double, forwarded unchanged after normalization. |
| `allocation_sha256` | Same serialization/hash convention as policy. |
| `target_scale` | Character same as `v3_target_scale`. |
| `environment` | Named list detailed below. |
| `started_utc`, `finished_utc` | Character UTC timestamps same as rows. |

`adapter_policy` has these keys, in order: character `id="R-1-20261022"`; logical `adopted=TRUE`; character `authority="RULINGS_LEAD.md R-1 (2026-10-22 19:25Z)"`; character `mapping_status="adopted"`; named character `roles=c(hpm="primary", pip05="S0")`; named character `status_map` in native-status order (`exact`, `completed`, `schedule_limit`, `numerical_failure`, `resource_limit`, `y_constant`, `no_predictors`, `invalid_input`, `adapter_error`), first two `ok`, remainder `failed`; identically named logical all-NA `converged_map`; character `diag_true_flags=c("low_empirical_ESS","grid_unconverged","local_limit")`; character `diag_false_flags="checks_passed_final"`; character `flagged_status="ok"`. These final fields document the policy; full code/informational/archived-search mapping is in the adapter helpers, never caller-configurable. Condition-driven warning handling does not alter status_map.

`environment` keys, in order: character `R` (`R.version.string`); character vector `session_info`; character vector `lib_paths`; character `host`; integer `pid`; character vector `RNGkind`; character vector `command` (`commandArgs(FALSE)`); named character-scalar list `threads` for `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS`, `NUMEXPR_NUM_THREADS`; named character-scalar list `slurm` for `SLURM_JOB_ID`, `SLURM_ARRAY_JOB_ID`, `SLURM_ARRAY_TASK_ID`, `SLURM_CPUS_PER_TASK`, `SLURM_MEM_PER_NODE`, `SLURM_MEM_PER_CPU`, `SLURM_TIMELIMIT`; named character vector `compiler` for `CC`, `CXX`, `CXX17`, `LOADEDMODULES`. Unset environment values are NA. Sampler RNG implementation/streams are separately retained in `fit`.

## Native fit structure retained in full

This is an inventory of the current production return, not a requirement that every branch supplies every key. Absent native fields stay absent; no final evidence is manufactured from calibration estimates. All additional native keys, list attributes, matrices and data.frame columns survive in `record$fit`.

| Native path(s) | Contents / nested fields |
|---|---|
| `status`, `message`, `seed`, `allocation`, `n`, `p`, `B`, `partial_results`, `estimates_available`, `hpm_incomplete` | Native status/text, method seed/allocation, retained dimensions and availability/partial markers. Initial failures may supply only a subset. |
| `preprocessing` | `status`, `reason` when invalid; on usable input `n`, `p_raw`, `p`, `kept`, `dropped`, `col_max`, `col_mean`, `col_sd`, `y_max`, `y_mean`, `y_sd_scaled`, `s_y`, `dup_components`; R-5 stable fallback additionally retains `stable_centering` split-centre maps (columns/response). Special early branches may retain native empty `hpm`. Standardized X/y excluded by native fit assembly. Maps refer to original predictor indices. |
| `budgets` | `n`, `p`, `K`, `B`, `ell`, `L`, `N0`, `H0`, `T0`, `R`; `tiers` table `e,N,H,T`; `exact_count`, `exact_count_saturated`, `exact_threshold`, `exact_branch`. |
| `branch_decision`, `branch_run` | Native `exact` or `smc`; operational branch provenance. |
| `preflight`, `preflight_escalation` | `branch`, `tier`, `est_bytes`, named `memory_components`, `est_seconds`, `seconds_per_score`, `score_count`, `score_components`, `timing_procedure`, `label`, `allocation`, `exceeds`. SMC timing estimates are NA; exact timing procedure includes label/scores/size/columns/environment (R/platform/compiler/modules). |
| `blocks`, `neighbours`, `log_Zbar0` | Packed original-index blocks (including native dendrogram attributes where supplied), neighbor supports and start normalization. |
| `cut_group`, `cut_group_count`, `cut_group_components`, `cut_group_graph` | Native logical/count/component inventory (size, block_span, members, blocks); graph threshold/graph. |
| `hpm`, `hpm_F`, `hpm_provenance`, `mpm`, `pip_primary` | Native selected support/score/provenance; strict primary-PIP MPM; retained original-index named primary vector. No secondary PIP is allowed. Provenance may include phase, tier, island, stage, round, particle, position, phi, iter, mechanism; exact has phase exact and mechanism enumeration in v2. |
| `log_Z`, `log_Z_r`, `log_Z_rel_m0`, `log_Z_r_rel_m0`, `log_Z_lower95`, `log_m0`, `log_increment` | Pooled and per-island log evidence, values relative to empty model, native lower bound, per-island/stage increments. The target is the standardized working model. Bound field/label are preserved, not retargeted. |
| `pip_r`, `rb` | Retained-p by island PIP matrix; per-island lists with `rb_acc`, `rb_round` accumulators. `pip_primary` is the native equal-island mean. |
| `stage_table` | Full native concatenated per-stage calibration/final table, columns specified below. Partial stage records retained where native supplied them. |
| `stage_record`, `streams` | Final island records and stream metadata. Island records: `phase`, `tier`, `iter`, `island`, `log_Z`, `phi`, `log_increment`, `ess`, `cum_log_Z`, `distinct_resampled`, `distinct_moved`, `stage_moves`, `terminal_moves`, `terminal_distinct`, `pip`, `rb_acc`, `rb_round`, `partial`, `init_draws_hash`, named seconds (`init`,`bridge`,`burn_in`,`measured`), `stream` (`stream`,`position_start`,`position_end`,`init_draws_hash`). Partial native island lists may contain NULLs. |
| `terminal_table` | `island`, `phase` (burn_in/measured), `round`, `distinct`, and native move-count columns below. |
| `local_search` | `centre`, `centre_F`, `path`, `path_F`, `scanned_centres`, `scanned_F`, `scan_complete`, `scan_size`, `termination`, `local_limit`, `local_certified`, `returned`, `returned_F`, `moves`, `n_evaluated`; R annotations `phase`, `tier`, `iter`, `island`. Present before certain failed early returns, even without top-level local_limit. |
| `local_limit`, `local_certified`, `global_certified` | Native flags/certificates; false local certification and true global certification are informational only. |
| `near_ties`, `near_tie_F`, `near_tie_truncated`, `island_best`, `hpm_before_local` | Native near-tie support/score list, truncation flag, final island best scores, pre-search `model`/`F`. |
| `flags` | Native final flags: `E1`, `E2`, `E3`, `low_empirical_ESS`, `local_limit`, `near_tie_truncated`, `checks_passed_final`, `escalated`, `grid_unconverged`, numeric `forced_pilot_steps`, `checks_passed_calibration`, `calibration_triggers`, `cut_group` where supplied. Early calibration failures instead supply calibration flags. No rewrite to suit study diag_codes. |
| `settings`, `frozen_sha256`, `grid` | Final settings `N,L,measured_rounds,islands,tier,ell,cache_capacity`, frozen calibration hash and grid actually used. |
| `frozen` | Class `v3_frozen`; `grid`, `tier`, `N`, `L`, `inherited`, `source`, `sha256`; calibration adds `rho_V`, `grid_label`. Inherited includes models and native HPM/provenance. |
| `calibration` | Full structure detailed below; retains diagnostic estimates even if fitting fails, clearly distinct from final reported primary PIP/evidence. |
| `exact` | Enumeration `status`, `message`, `log_Z`, retained named `pip`, `hpm`, `hpm_F`, `models_scored`, `top`, `second_F`, `margin`, `hpm_error_bound`, `hpm_error_bound_kind`, `certificate_bound`, `global_certified`; R adds `near_ties`, `near_tie_F`, `near_tie_truncated`, `mpm`, `log_Z_rel_m0`, `local_certified`, `R9`. `R9` contains margin/error bound/kind/certificate bound/rule. Error-bound kind is exactly `heuristic (not a validated interval bound)` and is retained with the certificate. |
| `leaders_gamma0`, `leaders_gamma1`, `top_store` | Native stores with `models`, `value`, `capacity`, `full`. |
| `score_counts`, `cache` | Logical/fresh mechanism counter matrices; named cache metrics (`capacity`,`hits`,`misses`,`inserts`,`clears`,`entries_at_end`) as supplied. |
| `ledger`, `partial_final` | Failure archives. Ledger includes `hpm` (model/F/log_m/provenance), `top`, `leaders_gamma0`, `leaders_gamma1`, `island_best`, `logical`, `fresh`. Partial final retains raw status/message/islands/local_search/hpm_before_local/ledger/cache/seconds_local/seconds_total/log_m0/log_Zbar0. |
| `timings`, `peak_memory_kb`, `runtime_guard`, `numerical_routes` | Native total/exact/setup/setup_total/calibration/final/final_detail timings as applicable, including islands/local/final_total; Linux peak resident high-water KiB; full runtime-guard and numerical-route records without filtering. |
| `stream_map`, `seeding_doc`, `variate_order_doc` | Full stream allocation table (`stream`,`phase`,`tier`,`island`) and native prose describing generator, seed arithmetic, draw order and stream counters. |

`stage_table` columns are `phase,tier,iter,island,grid_label,partial,stage,phi,rho_V,ess,log_increment,cum_log_Z,distinct_resampled,distinct_moved,acc_gibbs_change,acc_uswap,acc_nswap,acc_indep`, followed by move-count columns `gibbs,gibbs_state_changes,uswap_exec,uswap_acc,uswap_self,nswap_exec,nswap_acc,nswap_reject_noscore,nswap_self,indep_exec,indep_acc`. Move-count columns also occur in island stage/terminal move tables and terminal_table. Pilot rho is NA; final/diagnostic rho and labels are copied from the actual native grid, not reconstructed by the adapter.

`calibration` keys: `status`, `calibration_seed`, `tier_final`, `escalated`, `escalation_blocked`, `tiers`, `hpm`, `ledger`, `cache`, `stage_table`, `flags`, optional `frozen`, `seconds`. Its `flags` include `escalated`, `escalation_blocked`, `checks_passed_calibration`, numeric count `forced_pilot_steps`, `grid_unconverged`, `triggers_fired`, `triggers_by_tier`. Each trigger record may have `E1`, `E2`, `E3`, `forced_pilot_steps` (logical within trigger record), `grid_failure`, `grid_unconverged`, `local_limit`.

Each `calibration$tiers[[i]]` retains `tier`, native calibration `settings`, `status`, optional `message`, `pilot`, `grid`, `rho_V`, `grid_label`, `grid_source`, `converged`, `rebuilds`, `triggers`, `iterations`, `snapshots`, `grids`, `grid_construction`, `seconds`; on failure also `partial_results`, `partial_operation`, `seconds_total` where native supplied them. Pilot fields: `schedule`, numeric `forced_pilot_steps`, `stream`, `stage_record`, `local_search`, `best_before_local`, `best_after_local`, `seconds`, `partial`, `calibration_estimate`. Pilot estimate has explicit calibration-only label, partial marker, log_Z, named pip, ess and log_increment. Each iteration retains `iteration`, `grid`, `rho_V`, `grid_label`, `streams`, `log_Z_r`, `island_best`, `stage_record`, `local_search`, `seconds`, `partial`, `calibration_estimate`, optional `overall_best`, E1/E2/E3. Diagnostic calibration estimate retains its explicit calibration-only label, partial marker, log_Z_r, pip_r and ess. Snapshots and grids preserve their entire native finite-set/grid-construction inventories, labels, errors, intervals, F_V evaluations and seconds. These calibration estimates are never substituted for final primary PIPs or evidence.

Calibration settings are `tier,H,T_e,L,Hm,ell`. Each snapshot has `label,size,truncated,models,log_gamma0,d`; each archived grid has `label,grid,rho_appended,ok,reason,intervals,F_V_evaluations,seconds`. `grid_construction` contains `seconds,F_V_evaluations`. `runtime_guard` has `label,exceeded,allocation_seconds,elapsed_seconds,checkpoints`; each checkpoint has `checkpoint,phase,tier,iter,island,stage,elapsed_seconds,operation_seconds,projected_seconds,allocation_seconds,exceeded`. `numerical_routes` has numeric counts `chol,chol_refactor,qr,Q_recomputed,numerical_failures`. All remain native values.

## Validation handoff

The editable smoke contract is `A_build/smoke/test_adapter_contract.R`; it reuses `smoke/fixtures/core/v3.R` and mutates only copied fixtures in its evidence directory. It covers all native statuses and adapter errors, exact informational handling, individual numerical/informational diagnostics, zero/positive numeric forced counts, nested failed searches/calibration triggers, verbatim warning/message CSV/RDS persistence, failed full primary PIP/support audit, mapping provenance and immutable resume. Root runs it on Owls under the resource policy and inspects saved `adapter_test_evidence.{rds,txt}`. No numerical execution or SSH was performed while implementing this mapping. Root owns external HANDOFF/ledger/run updates and verification evidence.
