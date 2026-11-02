# SMC-BVS v2.2 output fields (for the LOWP metrics pipeline and the analysis)

Code: `code/core/v2_2/`. Source: `fit <- v3_fit(X, y, seed, allocation, keep_scored_set = NULL)`. The study record (`SMCBVS.rds`) holds `fit` plus the original-index summaries listed in the last section.

Conventions:
- **Indices.** Every model and support is a sorted integer vector of **original 1-based column indices**. Retained columns are `fit$preprocessing$kept`; dropped constant columns are `fit$preprocessing$dropped`.
- **Named vectors.** Named PIP vectors and the rows of PIP matrices are named by the retained original index.
- **New in v2.2.** Marked **[new]**. Everything else is v2.1, bit-identical (REGRESSION.md).
- **Availability.**
  - Estimates (Ẑ, PIPs, MPM) exist only when `fit$status ∈ {"completed", "exact"}` and `fit$estimates_available` is TRUE.
  - On a runtime-guard `resource_limit`, a calibration or final-run `numerical_failure`, or `schedule_limit`, `fit$hpm` is the best model scored so far, with `hpm_incomplete = TRUE`.
  - A *preflight* `resource_limit` stops before anything is scored: no HPM, no `hpm_incomplete`, no `scored` report.
  - A setup `numerical_failure` returns the best table model, but no registry report.
  - The study CSV marks both rules as failed and keeps the HPM only in `support_audit`.

## Status and run facts

| Field | Meaning |
|---|---|
| `status` | `completed` (SMC finished), `exact` (enumeration branch), `resource_limit`, `schedule_limit`, `numerical_failure`, `y_constant`, `no_predictors`, `invalid_input`. The study adapter adds `adapter_error` |
| `estimates_available`, `partial_results`, `hpm_incomplete` | Availability labels |
| `branch_run` | `"smc"` or `"exact"` (p = 20/30 at n = 200 always run `"smc"`) |
| `n`, `p`, `B`, `budgets` | n, retained p, block size, and the list `K, B, ell, L, N0, H0, T0, R, tiers (e, N, H, T), exact_count, exact_threshold, exact_branch` |
| `seed`, `stream_map` | Method seed; streams 0–9 calibration, 10–13 final |
| `frozen$tier`, `settings$N` | Final tier (0, or 1 if escalated) and particles per island |
| `grid` | Final temperature grid (0 … 1) |
| `timings$total` | Fit wall time (s). Also `timings$setup`, `$calibration`, `$final`. Study record: `runtime_s` |
| `peak_memory_kb` | VmHWM (Linux only; NA on Windows) |

## Evidence Ẑ

| Field | Meaning |
|---|---|
| `log_Z` | Pooled log Ẑ = log mean_r Ẑ_r (full scale) |
| `log_Z_rel_m0` | Pooled log Ẑ − log m(∅) (Bayes-factor scale; **compare this with the exact log Z − log m(∅)**) |
| `log_Z_r`, `log_Z_r_rel_m0` | Per-island log Ẑ_r (length 4), full and relative scale |
| `log_Z_lower95` | log 0.05 + log_Z (95% one-sided lower bound, full scale). Relative bound = `log_Z_rel_m0 + log(0.05)` (not stored) |
| `log_m0`, `log_Zbar0` | log m(∅); log Z̄₀ of the start distribution |
| `log_increment` | List of 4 vectors of per-stage log increments |

## PIPs and selections

| Field | Meaning |
|---|---|
| `pip_primary` | **RB PIP**, pooled: equal-weight mean over the 4 islands; named by retained index |
| `pip_r` | RB PIP per island: p_retained × 4 matrix |
| `mpm` | RB MPM = {j : `pip_primary` > ½} (strict) |
| `pip_plain` **[new]** | **Plain PIP**, pooled: the share of particle-rounds (N particles × 4 measured rounds) that include j, as the equal mean over islands |
| `pip_plain_r` **[new]** | Plain PIP per island: p_retained × 4 |
| `mpm_plain` **[new]** | {j : `pip_plain` > ½} |
| `stage_record[[r]]$plain_acc`, `$plain_round` **[new]** | Inclusion counts (total; per measured round, 4 × p) for island r. RB analogues: `rb_acc`, `rb_round` |
| `hpm`, `hpm_F` | HPM = the best model scored anywhere in the fit (tables, calibration, final, local searches); F = log prior + log marginal likelihood. Exact ties go to the smaller model, then lexicographic |
| `hpm_provenance` | The first-score event of the HPM: phase, mechanism, tier, island, stage, round, particle, position, phi, iter |
| `near_ties`, `near_tie_F`, `near_tie_truncated` | Models with F ≥ hpm_F − 1e-9 |
| `top_store` | Top-(40p+1) distinct scored models by F (`models`, `value`) |
| `local_search`, `local_certified`, `local_limit` | Final local search archive. `local_certified` = no flip or swap improves the HPM |

Exact branch: `log_Z`, `pip_primary`, `mpm`, `hpm`, `global_certified`, `exact$models_scored`. There are no plain PIPs and no instrumentation `scored` fields.

## Flags

| Field | Meaning |
|---|---|
| `flags$E1`, `$E2`, `$E3`, `$low_empirical_ESS`, `$local_limit`, `$near_tie_truncated`, `$checks_passed_final` | Final checks (never trigger reruns) |
| `flags$escalated`, `$checks_passed_calibration`, `$grid_unconverged` (selected tier), `$forced_pilot_steps`, `$calibration_triggers` | Calibration |
| `flags$cut_group`, `cut_group_count`, `cut_group_components` | Informational (fires almost always; see PATCHES P4) |
| Study CSV `diag_flag`, `diag_codes` | R-1 mapping (`study/SCHEMA.md`) |

## Instrumentation **[new]** (`fit$instrumentation`, also `record$instrumentation`)

| Field | Meaning |
|---|---|
| `version` | `"v2.2"` |
| `stages$final` | Planned number of final bridge stages, i.e. the interval count of the frozen grid (= `length(grid) − 1`). NA if there is no final run. On a final-run stop it is *not* the number of stages executed: use `length(partial_final$islands[[r]]$phi)` for that |
| `stages$pilot` | Pilot stages per calibration tier (integer vector, tier 0[, 1]) |
| `stages$diag_grid_intervals` | Per tier: grid intervals used in each rebuild iteration |
| `stages$tier_final` | Selected tier |
| `best_before_local` | (`model`, `F`): global best before the final local search (completed SMC) |
| `best_after_local` | (`model`, `F`, `changed`): the reported HPM after the final local search, and whether it differs |
| `stop` | NULL unless `resource_limit`. Then `where` (`preflight` / `escalation_preflight` / `runtime_guard`) and, from the first exceeded guard checkpoint: `checkpoint` (`bridge_stage` / `grid_construction` / `local_search`), `phase` (`pilot`, `diag`, `final_bridge`, `local`; grid checkpoints are logged as `diag`), `tier`, `iter` (−1 = final run), `island`, `stage`, `elapsed_seconds`, `projected_seconds`, `allocation_seconds`. For `preflight` and `escalation_preflight` there is normally no exceeded checkpoint, so these fields are NA; the details are in `fit$preflight` and `fit$preflight_escalation` (`est_bytes`, `allocation`) |
| `escalation` | `escalated`; `reasons` = names of the tier-0 calibration triggers that fired (`E1`, `E2`, `E3`, `forced_pilot_steps`, `grid_failure`, `grid_unconverged`, `local_limit`); `blocked` |
| `cut_group_large` (integer), `cut_group_large_any` (logical) | Number of cut_group components with size > B; whether there is any |
| `scored` | Present only on the SMC branch once setup succeeded (the registry exists). Absent on the exact branch, early statuses, preflight stops and setup failure |
| `scored$mode` | `"exact"` (p ≤ 64) or `"hll"` (p > 64) |
| `scored$n_distinct` | Number of distinct models scored in the whole fit (tables, calibration, final, local searches). Exact mode only, else NA. This is the union cardinality, not a sum of fresh counters |
| `scored$n_distinct_hll` | HyperLogLog estimate of the same (every p; nominal relative s.e. ≈ 0.8%) |
| `scored$log_sum_exp_F` | log Σ_{distinct scored S} exp F(S). Exact mode only. **Coverage of the posterior by the scored set = exp(`log_sum_exp_F` − exact log Z)** (full scale; Z = Σ_S exp F(S)) |
| `scored$after_calibration` | `n_distinct`, `n_distinct_hll`, `log_sum_exp_F` at the end of calibration |
| `scored$first_scored` | Phase × mechanism matrix: distinct models by their first score (exact mode) |
| `scored$memory_bytes_estimate` | Approximate C++ registry storage. Excludes allocator and rehash overhead, the exported data frame, and the rest of the fit |
| `scored_set` | Produced by default only on the SMC branch, with a registry, at retained p ≤ 32. `keep_scored_set = FALSE` suppresses the export but not the registry. A data.frame sorted by `key`, one row per distinct scored model (see below) |

The registry memory grows with the number of distinct models (O(M) at p ≤ 64; no bound). `peak_memory_kb` and `timings$total` are measured *before* the instrumentation report and scored-set export.

**`scored_set` columns:**
- `key`: bitmask, where bit i (value 2^i, i = 0 … p_retained − 1) means retained column i + 1 is in the model, i.e. original index `preprocessing$kept[i + 1]`. With no dropped columns this is Σ_{j ∈ S} 2^(j−1). Stored as double, exact for p ≤ 32.
- `size`: |S|.
- `first_phase`: one of `table`, `pilot`, `diag`, `final_init`, `final_bridge`, `burn_in`, `measured`, `local`, `inherited`.
- `first_mech`: the route; one of `table`, `init_draw`, `gibbs_flip`, `uswap`, `nswap`, `indep`, `local_scan`.
- `first_tier`.
- `first_iter`: calibration rebuild iteration. 0 = pilot; −1 = tables or final run.
- `first_island`: 1–4. 0 = pilot, tables or local search.
- `first_stage`: phase-dependent.

| Phase | `first_stage` means |
|---|---|
| bridge (pilot, diag, final_bridge) | bridge stage t |
| initial draws (`final_init`, and pilot/diag initial draws) | 0 |
| tables | 1-based block number |
| burn-in and measured rounds | the island's last bridge stage T |
| local search | 1-based scan number |

The compact record omits round, particle, position and φ. "When" means these coordinates, not a global chronological index. Pilot and diagnostic islands label all their events with phase `pilot` or `diag`. There, a `first_stage` below the island's last stage T identifies a bridge stage, but at stage T the last bridge stage, the burn-in and the measured rounds **cannot be told apart** from this record.

Export limit: the export narrows the row count to a 32-bit `int`, so it supports at most 2³¹ − 1 distinct models. In practice the registry exhausts memory long before that (observed: ≤ 1.2 × 10⁵ models at p ≤ 30).

"Was the truth scored, when and by which route": map the truth's original indices to retained positions through `preprocessing$kept`, then look up key = Σ 2^(position − 1) in `scored_set`. This is done by the scoring job only; the fit never sees the truth. The formula Σ 2^(j − 1) over original j is correct only when no column was dropped.

Scope: the registry covers every model of a `v3_fit` call. A stand-alone low-level `cpp_final_run` called with an empty registry and externally supplied inherited models would not register those inherited models (production never does this).

## Number of scores and cost

| Field | Meaning |
|---|---|
| `score_counts$logical`, `score_counts$fresh` | Phase × mechanism matrices of *ledger events* of the **final-run ledger**: logical events (they include held Gibbs states that are not re-evaluated) and fresh events (cache misses; a cache-evicted model counts again).<br>Scope: they include the final run's re-ingestion of the block tables (row `table`) plus the final islands and the final local search. They exclude the re-scoring of inherited calibration models, which updates the stores without ledger events.<br>The calibration ledger is `calibration$ledger$logical` / `$fresh`; its V re-scoring is not a ledger event.<br>Do not add the two ledgers' fresh counts as "models scored": tables appear in both. Use `instrumentation$scored$n_distinct` for distinct models. Scorer-route counters: `numerical_routes` |
| `cache` | Capacity, hits, misses, inserts, clears |
| `timings`, `runtime_guard` | Times. The guard's checkpoints carry elapsed and projected seconds |

## Study record (`SMCBVS.rds`) summaries, original-index length-p vectors

| Field | Meaning |
|---|---|
| `pip` (= `pip_primary_original`) | RB PIP over all p original columns (dropped = 0; NA if unavailable) |
| `pip_plain` **[new]** | Plain PIP, same convention |
| `hpm`, `mpm`, `mpm_plain` **[new]** | Supports (original indices) |
| `native_status`, `estimates_available`, `runtime_s`, `rows` (= CSV rows) | As in v2.1 |
| `instrumentation` **[new]** | = `fit$instrumentation` |
| `adapter_version` | `"2.2-R1"` |

The CSV (`SMCBVS.csv`) columns are unchanged from v2.1.

**Note on study use at low p.** The v2.2 study adapter still accepts only p ∈ {500, 1000}. For low p, call `v3_fit` directly or via a low-p adapter (PATCHES P6).

## v2.2.1 changes (CONF-2b, 2026-10-29)

The core is byte-identical to v2.2, so every `fit$…` field above is unchanged. Only the study envelope changes; the authority is `code/core/v2_2_1/study/SCHEMA.md`, section "v2.2.1".

| Field | Change | Who reads it |
|---|---|---|
| `record$adapter_version` | `"2.2.1-R1"` (was `"2.2-R1"`) | provenance only |
| `record$code$source_sha256` and study file hashes | new values (study layer changed); `v3_source_sha256` unchanged | provenance only |
| CSV (88 columns) | unchanged, same order; `study`/`regime` = `newcampaign_lowp`/`L` at p ∈ {20, 30} | unchanged |
| `record$case` | regime H: v2.2's layout, unchanged. Regime L: v2.2 plus `repeat_m` and `method_seed_base` (the retired LOWP runner's layout) | `scoring/R/extract_smc.R` (regime L) |
| Repeat files | regime L only: `SMCBVS_rep{m}.*` beside `SMCBVS.*`; the method seed is primary + 1,000·m | scoring scan (unchanged pattern) |
| **`record$p5`** (new) | appended last, **only** in a P5 rerun record, never in a primary record: `rule, role = "p5_retry", factor = 2, method_seed, primary = list(prefix, files_sha256, native_status, allocation, allocation_sha256, stop, runtime_s, started_utc, finished_utc), retry_allocation, retry_allocation_sha256` | analysis: the completed-rerun sensitivity (D11) |
| P5 rerun files | `<case>/P5_retry/SMCBVS_p5retry.*` (or `SMCBVS_rep{m}_p5retry.*`; rds, csv, sha256, done). The non-recursive case-folder scan of `scoring/` does not see them (verified in regression c6). Pass these files explicitly to the P5 sensitivity | analysis |
| `tools/p5_scan.R` table | per primary unit: primary/retry status, allocation, stop phase (`where, phase, checkpoint, tier, iter, stage`, elapsed and allocation seconds), `eligible` | OPS (P5 gate), analysis |

Note: `fit$instrumentation$stop$elapsed_seconds` and `projected_seconds` are wall-clock readings. Treat them as timing, like `runtime_s`; they vary between identical reruns.
