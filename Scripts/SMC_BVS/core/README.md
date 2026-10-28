# SMC-BVS v3 production core

Authority: master Part I, final SHA-256 `7d77dddb968135d86a6b6431a7a3e04e122eb0c09f5ec9a6a8329e9a20757b6e`, deployment CHANGES and RULINGS_OPEN/2/3, and binding deployment RULINGS_LEAD R-5. Starting source: independently verified `source_snapshots/prototype_core`; all 18 copied R/C++/Makevars hashes were verified before edits. No binary/cache artifacts were copied.

```r
source("/path/to/core/v3.R")
fit <- v3_fit(X, y, seed, allocation = list(mem_gb = 8, hours = 24))
saveRDS(fit, output_path)
```

`v3_fit` accepts only data, seed and allocation. It always performs the mandated exact decision or full fixed-budget calibration and final SMC. Persistence and study mapping belong to the caller. PIPs are `pip_primary` (retained original-column names); supports `hpm` and `mpm` contain original indices. The preprocessing map identifies dropped columns. Invalid seeds return `invalid_input`.

Production changes from the reference:

- Remove observer/watch machinery, scoring-event dumps, replay/trace, resampler traces, experimental replication and profiling overrides. Remove unused R start-mode/log-deficit helpers and the start-mode Rcpp export; retain ordinary scorer/start helpers and unchanged header internals for testing wrappers. Keep operational aggregate score counts, HPM/leaders, acceptance/distinct-count records, stream positions/hashes and local-search archives. Test-only exports are appended by the separate A_build/tests harness to testing copies.
- Remove secondary PIP computation and outputs on both branches; retain equal-island primary PIP arithmetic.
- Report `cut_group`, `cut_group_count` and `cut_group_components` with sizes, block spans, sorted original members and block IDs. Use the uncapped >= threshold graph, with no forced partner; exact branch is NA.
- Certify the SMC selected HPM locally only when it equals the no-improvement fully scanned search centre. Preserve all-scored HPM/tie/near-tie rules and exact-branch heuristic certification, with its explicit required label.
- Memory-only SMC preflight with cap K and prescribed coefficients; exact branch uses the 200-score timing recipe with R-5 corrected distinct k-star model construction. Recheck memory before tier 1. One steady-clock guard checks elapsed plus just-completed operation strictly against allocation after every pilot/diagnostic/final bridge stage, grid construction and local search. `runtime_guard$checkpoints` records all checks. Stops return `resource_limit`, `partial_results=TRUE`, best HPM and archived partial operations/islands, with final estimates unavailable.
- Replace binary-search inverse CDF with the specified O(N) guide build/O(1) expected lookup. Preserve every cumulative arithmetic operation and uniform draw; repeatedly adjust backwards across zero-weight runs.
- Add aggregate numerical-route accounting and explicit phase/tier/island/iteration metadata. These change diagnostic records, not score arithmetic or random draws.
- Save the complete stream 0..13 map, SplitMix64/xoshiro256** seeding algorithm, serial draw-consumption order and boundary conventions in `stream_map`, `seeding_doc` and `variate_order_doc`. Observed calibration stream positions/hashes remain with each pilot/diagnostic iteration; final positions/hashes are in `streams` and each final island's `stream` record. A final stream's tier is filled after calibration selects it.
- Preserve each construction's returned `rho_appended` in `calibration$tiers[[e]]$grids`, and the used grid's `rho_V`/`grid_label` with diagnostic iterations and `frozen`. The final grid retains the latest successful construction, including an identical converged rebuild. No rho is recomputed. Frozen rho is diagnostic metadata outside the existing computational hash.
- Consolidate all attempted tiers' pilot/diagnostic stages and all available final stages into `fit$stage_table`: phase, tier, iter, island, grid label, partial indicator, stage/phi, restricted `rho_V`, empirical ESS, increments/cumulative evidence, both distinct counts, all mechanism counts and acceptance proportions. Pilot rho is `NA` because the adaptive pilot has no frozen restricted grid. `calibration$stage_table` contains calibration rows alone; final-ESS flags are still computed on final rows before consolidation.
- Preserve partial pilot schedules/forced counts/streams, diagnostic stream rows for attempted islands only, produced local-search records, grid archives/costs and calibration-stage rows before returning on resource stops. Calibration estimates are explicitly labelled partial when stopped; they never become final PIP/evidence estimates.

`cpp/v3_calib.h` (including RC-2), `v3_blocks.h`, `v3_start.h`, `v3_util.h`, `Makevars.v3` remain byte-identical to the reference. The unchanged start header retains historical comments about test/profiling uses; production has no corresponding controls.

## v2 repairs required by R-5

v1 was rejected by B; it remains frozen. v2 fixes near-constant centring/scaling and strict numeric input shape validation, cache capacity exactly 500p, timing models of exactly k-star distinct predictors, exact HPM provenance (`phase=exact`, `mechanism=enumeration`), and two rescoring exception paths. No statistical target, kernel, seed rule or production budget is retuned. Stable centring adds a split-centre map only on the numerical fallback path; ordinary prototype arithmetic is preserved where applicable.

Execution follows BRIEF Amendments 1/2 and RULINGS_LEAD R-3/R-4: development validation on Owls R4.6.0/GCC11.5.0, nice19, A at most4cores (2 during C batch), within deployment caps. Root is the sole SSH funnel. NOTS GCC14.3.0/R4.5.2 build and full regression are separately required before any NOTS fit; no NOTS use until the lead opens runs. A's prepared validation scripts do not grant production GO.

Validation evidence belongs to HANDOFF_v2.md and the saved per-job manifests. Source_manifest.json pins source/prototype identity; it is not a numerical-equivalence certificate. B independently re-verifies the frozen v2 before G1 may open.
