# Thread A build regression and changed-piece tests

Status: metadata T2 additions in `metadata_units.R` are **UNRUN**; root reports the preceding regression04 passed all 32 seeds / 736 checks. That historical result does not validate these additions. AMENDMENT 1 governs: Owls only, R4.6.0/GCC11.5.0, nice19, <=4 A cores; no NOTS/Slurm. Root is the sole SSH/SCP funnel and owns persistent launch, smoke and saved-evidence inspection. This agent makes no remote calls and performs local editing only. No production datasets, truth or holdout are read.

Use R packages Rcpp, digest, jsonlite. Each seed runs both implementations sequentially in separate R processes with identical pinned Makevars flags, single-thread settings and the same synthetic input. A shared content-hashed compile cache builds each implementation once and reuses the binary for every seed. Its key includes all C++/header/Makevars contents, wrappers, R/Rcpp/compiler and compiler environment. Stable frozen TU/header paths and `rebuild=FALSE` prevent per-seed recompilation. Each seed saves its cache identity. Testing-only exports are appended to a copy of each `cpp/v3_core.cpp`; the original headers and engine are unchanged. Source trees/tests are frozen per seed. No source-tree cache is written. Production has no added test controls.

## Root execution handoff

1. Root reads applicable Owls AGENTS.md, freezes production/prototype/tests, creates its persistent-job manifest and deployment RUNS.md entry, records PID/launch command. The task manifests supplement that record.
2. Root launches the sequential runner below, optionally with `1` as the fourth argument for smoke. Inspect compilation, `REPORT.md`, `exit_status.tsv`, worker logs, `comparison.json` and unit RDS evidence. All 32 regression seeds are synthetic development seeds; assessment-study production seed restrictions are separate.
3. `run_all_seeds.sh` checks uptime/free before the batch and between seeds. At load1>40 or available memory<30GiB it waits 15 minutes. It enforces Owls hostname and nice19, uses one R/compiler process at a time, and pins BLAS/compiler parallelism to one. Root coordinates the A memory/disk allowance and global caps. No SSH or scheduler command is issued by these scripts.
4. The runner inspects all saved shards at completion with:

   ```sh
   python3 "$TESTS_DIR/summarize.py" "$TEST_EVIDENCE_DIR"
   ```

   For a smoke only, use `--indices 1`. A smoke pass cannot satisfy the 32-seed gate. Missing outputs, failed worker statuses, changed sources, or changed output hashes prevent an aggregate pass.

Root's persistent Owls launch command (set paths to its frozen snapshot):

```sh
nice -n 19 bash "$TESTS_DIR/run_all_seeds.sh" "$CORE_REFERENCE" "$CORE_PRODUCTION" \
  "$TEST_EVIDENCE_DIR"
```

The destination must be new; existing evidence is never overwritten. Supply a fourth argument `1` for smoke or `2,3,...,32` after a successful smoke; set `V3_TEST_COMPILE_CACHE` when invoking `run_suite.sh` independently to reuse an existing suite cache. A seed can be reproduced independently from its row/frozen sources. Failed builds preserve logs and exit statuses; fix and relaunch to a new directory. `regression.sbatch` was removed under AMENDMENT 1.

## Coverage

| Requirement | Evidence |
|---|---|
| Many fixed small seeds, exact numeric bits | 32 seeds including both legal endpoints; six small n/p patterns, constant-column gaps, duplicate/sign-duplicate and near-collinear columns; `raw_results.rds`, strict recursive double-byte comparator (no tolerances) |
| Scorer, preprocessing, blocks, start, exact | Complete preprocessing/budgets, block tables/start tables/neighbours, selected feasible model scores, local scans, exact PIPs/evidence/HPM/heuristic certificates compared bit for bit |
| RNG order/state and calibration | Streams 0–13; four 64-bit state words, consumed draw count, next uint64; actual pilot and two diagnostics at both tiers, continued streams, V/grids/leaders/inherited final; actual R rebuild/escalation/freeze/check aggregation with a test-environment budget resolver |
| Final/stages/local/flags | Actual tiny final C++ orchestration and R assembly; all increments/ESS/acceptance and boundary counts/distinct counts/RB sums/PIPs/evidence/local paths/HPM provenance/near ties/flags; fresh final and inherited final |
| Local exact tie change | Real duplicate-column singleton tie changes all-scored HPM with zero strict moves; assembled selected-HPM certificate must be false and E3 false. Same-centre and uncertified-centre cases also checked |
| Cut group | Exact equality and next-double-below threshold; negative correlations; uncapped weak bridge between dense groups; no forced partner; large and size<=B split groups; whole groups unflagged; nonconsecutive original indices; NA on exact branch |
| RC-2 | Fully forced schedules at T=2000/4000/16000; forced endpoint retains flag; unforced endpoint in snap window is not snapped; grid validates after snapping and tests interval count after append; all decisions also compared against prototype |
| Guide resampling | Leading/interior/trailing zero masses, underflow/skewed/equal weights; u=0, denorm_min, exact cumulative boundaries and adjacent doubles; same ancestor for each prescribed u; N draw count and seeded RNG state; full downstream island results match |
| Removed secondary/profiling | Secondary present in reference, absent in production; primary and MPM bits unchanged; production signatures and exported functions exclude replay/observer/reference/replication/test switches |
| Memory-only preflight | Every formula term, both tiers, n/p=9/7,200/500,200/1000,256/65; memory equality and one-ULP overage; SMC never calls timer even at tiny hours; exact memory/time/timing-size/defaults; timing recipe spies verify 200 scores on first min(p,max(64,k*)) columns |
| Runtime guard | Strict > boundary; every final/pilot/diagnostic bridge stage, each grid and each local search; timing arithmetic and labels; early stage stop retains partial output/HPM; controlled test-copy expiry at grid completion retains grid and earlier archives |
| Provenance | Source SHA-256 snapshots/inventories, synthetic input RDS, commands/seeds/PIDs/nice priority, environment/compiler/CPU/R, timestamps, raw outputs, logs, exit statuses, source preservation/output SHA-256 inventories and shared compile-cache identity |

## Exact comparison exceptions

Only measured time fields and explicit r2 operational metadata differences are projected out. Reference-only empty offspring/profile traces are removed; stream/seeding documentation is separately asserted. `metadata_units.R` compares the complete final `stage_record` with this invocation's raw islands and each final `streams` entry with its corresponding raw island stream, including identity, positions, hashes, types and attributes. It independently reconstructs the entire final stage table from those raw records and the entire calibration stage table from this invocation's pilot/diagnostic archives (including schedule-limit returns). Every phase/tier/iteration/island/stage identity, row order, partial/grid/rho label, temperature, ESS, evidence increment/cumulative evidence, distinct count and mechanism count/proportion is compared with `exact()`; Gibbs changes divide by max(Gibbs steps,1), and U/N/I acceptances divide by max(the corresponding executions,1). All self-loop/no-score count columns are retained. These checks use the actual full-orchestration archives, not the separate worker calibration with different settings. Saved-record mutations must reject a missing final stream, a changed final stream position, a one-ULP calibration ESS change, a diagnostic mechanism-count change and reordered calibration rows. Old shared stage-table columns also retain their prototype byte comparison. Calibration estimate labels retain the calibration distinction while partial-availability fields are validated. Named record insertion order is canonicalized; field sets, types, attributes and numeric bytes remain strict. Secondary PIP removal and selected-HPM local-certificate correction are asserted before comparing every remaining final field. No arbitrary common-field intersection or numeric tolerance is used.

## Current limitations / interpretation

The tiny test settings exercise the same internal implementations through testing-only wrappers/environments. They do not benchmark production p=500/1000 performance. Root's production-budget smoke and independent B verification remain separate gates. The memory formula is tested as the adopted estimate; this does not prove a peak-memory bound. Guide lookup arithmetic and boundaries are validated, while its O(N) construction is a source-reviewed complexity property, not a timing benchmark. No passed result is claimed until the remote saved outputs are inspected.
