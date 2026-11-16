# PR #37 re-check: WP4 calibration pipeline, review fixes (M-1..M-6, m-1..m-6)

- **Reviewer:** Opus 5.5 (high), independent of the author. Date: 2026-11-16. Template: `briefs/REVIEW_PR_template.md`; rules: `briefs/BUILD_COMMON.md`.
- **Scope:** PR #37, branch `exp/P1M-wp4-calib-run`, head `7a950fde`. This is the fix commit on top of `a69a2b5e`, which merges `exp/P1M-engine` @ `4c238a32` (INTERFACES v0.1.12).
  - Diff re-checked: `a69a2b5e..7a950fde`, 10 files, +457 / −96.
  - Files: `calib.h`, `calib_backend.h`, `calib_run.h`, `wp4_io.h`, `calib_run.cpp`, `wp4_io.cpp`, the golden R script and harness, `test_wp4.cpp` and `test_wp4_io.cpp`.
- **First review:** `PR37_review.md` (ACCEPT-WITH-FIXES: 6 MAJOR, 6 MINOR). Fix list: the PR comment of 2026-11-16.
- **Contract:** INTERFACES v0.1.12 (§5, §7); DECISIONS D-1, D-26 and D-29; WP3_DESIGN §1.11 (v0.6, on `exp/P1M-wp3-calib`).
- **How:**
  - Detached worktrees, read only, in `/home/fb31/SMC_Engineering_Department/tmp/20261116-recheck-37`, removed at the end.
  - Nothing was pushed, commented or branched. The local merge commit existed only in a detached temp worktree.
  - Owls, `nice -n 19`, `taskset -c 0-2`, `--threads 3`, one suite at a time, no NOTS. I stopped only my own PIDs.

## Verdict: **MERGE**

All 6 MAJOR and 6 MINOR findings are fixed as claimed. I found 4 new MINOR findings and 3 INFO items; none blocks the merge, and each should be dispositioned.

- **Tests (MEASURED):**
  - PR head: `v4_tests` 110/110, WP5 OK, quick golden **443,598 checks, 0 failures**. The first review's quick run had 428,237, so the new M-6 checks add about 15k.
  - Merged with the current base `322e4a60` (PR #38 moved the base after the PR's last base merge): the merge is clean and the suites pass. One run showed a flaky WP5 unit failure that comes from the base, not from this PR (INFO-3).
- **WP3 stacking:** the `IslandRunner` interface changed only additively, and `exp/P1M-wp3-calib` merges cleanly onto `7a950fde`. Three notes for WP3's runner are under "WP3 interface" below.

Counts: CRITICAL 0 · MAJOR 0 open · MINOR 4 new · INFO 3.

## Test runs (MEASURED; Owls `owls.stat.rice.edu`, Xeon Gold 6148, g++ 11.5.0, R 4.6.0, 3 threads, load ≈ 23 on 80 CPUs)

| tree | command | result |
|---|---|---|
| PR head `7a950fde` | `TMPDIR=… tests/run_tests.sh --quick --threads 3 --build-dir …` | `v4_tests` **110 cases, 0 failed**; WP5 driver 17 OK; competitor harness OK; install script 23 OK; **WP4 golden (quick) 443,598 checks, 0 failures**; rc 0 |
| local merge `7a950fde` + `322e4a60` (tree `e7f6960a`, the same tree `git merge-tree` gives, no conflicts; the base change is only `tools/slurm/p1m_cells.py` and `test_p1m_driver.py`) | same | first run: 110 cases, **1 failed** (`wp5_selection_pip_evidence`, INFO-3); WP5 driver 17 OK; harness and install OK; **WP4 golden 443,598 / 0** |
| same merged build | `v4_tests` again (full), then the failing case alone 3× | **110 / 110**; the single case passes 3/3 in both builds |

- The full golden (`--full`, 2,005,641 claimed) was not re-run. As asked, I ran the quick level.
- The ledger path, including every new M-6 comparison, runs at the quick level.

Reviewer probes (MEASURED):
- **`probe.cpp`, linked against the PR's `libv4_bit.a`:** write_calib / read_calib with each new refusal. Results are in M-1, M-4 and m-3 below.
- **`smcbvs4 calibrate --plan-only 1 …`:** eleven argument sets. Results are in M-1, M-5 and m-4.

## Claims, one by one

### M-1 V settings (D-1, D-26): **FIXED**
- **Settings.** `settings_from(b, bounded)` sets tier-0 H = `V_H` = 512 and blanks tier 1. `frozen_N(b, bounded, ·)` = `V_N` = 2,500 (`calib_run.h:35-50`). The I_max clamp is gone.
- **Through the binary** at n = 200, p = 10⁶:
  - `--mode V` gives exactly one tier with H 512, T_e 1000, N_final 2500 and ℓ 20.
  - `--mode compat` gives 204,800 / 10⁶ for tier 0 and 819,200 / 4·10⁶ for tier 1 (v3 budgets, unchanged for theory mode).
- **`read_calib` (probe).** Each of these is refused with `invalid_input`:
  - a V calib.bin with N = 50, tier 1, the coded rule, I_max 5 > ℓ 3, I_used 2 > I_max 1, or no settings block;
  - a compat calib.bin with the bounded rule.

  A valid V calib.bin and a valid compat calib.bin read back.
- **Remaining gap.** calib.bin's `N` still comes from the caller (`CalibWrite.N`); only the reader enforces 2,500. When WP3's runner lands, the command must write `frozen_N(...)`. That is fine as long as the reader check stays.

### M-2 runner statuses: **FIXED**
- **Mapping in `LedgerBackend::take`** (`calib_backend.h:175-191`):
  - completed → ok;
  - resource_limit → resource_limit, whether partial or not;
  - numerical_failure → numerical_failure;
  - invalid_input, internal_error and io_error → thrown as `Error` with that status, so `main` records it.
- **Admission refusal (nothing ran):** no ledger is merged and no stage record is written. The message defaults to "resource_limit (admission)".
- **Toy tests:** an admission refusal at a diagnostic island (iter 1, island 3) gives resource_limit with task status resource_limit. internal_error, invalid_input and io_error are each thrown with their own status.
- **Nit:** there is no toy test of an admission refusal at the pilot. The code path is the same `take`.

### M-3 island ledger configuration: **FIXED**
- **`check_island_ledger`** raises `internal_error` unless the island ledger has:
  - the same p, islands = 4 and leaders on;
  - the same caps and orders for top, lead0 and lead1;
  - no PH_TABLE, PH_INHERITED, PH_LOCAL or PH_LS0 logical counts.
- **A ran island without a ledger** is refused unless its status is numerical_failure.
- **Toy tests:** leaders off, and table events. Both are refused.
- **Doc nit:** WP3 §1.11 still says "`Ledger::merge` refuses a mismatch". The check lives in the backend, which has the same effect. Update the wording when §1.11 is next touched.

### M-4 calib.bin `meta.k_store`: **FIXED**
- `k_store` = pool size ÷ entries of the calibration top store, which is the mean stored |S|. It is the right quantity for the store plan in INTERFACES §7.
- It is written only when the status is ok.
- `read_calib` requires it finite and > 0. Probe: 0 is refused; NaN (written as JSON null) is refused with `invalid_input`.
- It is exposed as `CalibIn::k_store`.
- The INTERFACES §5 calib.bin list does not name `meta.k_store` yet (INFO-1).

### M-5 `--mem-budget`, `--plan-only`, resident / budget to islands: **FIXED, with caveats (N-1, N-2)**
- **Plan reproduced.** `calib_memory_plan` at p = 10⁶, kbar 8 gives:

  | item | GiB |
  |---|---|
  | ledger | 10.80 |
  | island ledger | 10.80 |
  | export | 6.56 |
  | resident | 17.36 |
  | total | 28.16 |

  These match the claim (resident 17.4 GiB, total 28.2 GiB).
  - The per-entry size 26 + 4k B and the 2.5× staging peak agree with `Store` (`store.cpp:36-80`: v, off, hash and len plus the int32 pool; reserve room = kept + trigger).
  - The export term (4k + 8 + 32 + 16 B per model) matches `InheritedFlat` plus the `ModelView` index.
  - With X (≈ 1.6 GB) and setup (≈ 7 GB), the total is ≈ 38.8 GB (≈ 36 GiB), ESTIMATE. The PR's "≈ 37 GB" mixes GB and GiB but is in range.
  - This figure excludes the calibration island's own working set (particles, orders, products at G ≤ 256). WP3's admission counts that.
- **Refusal.** The command refuses when `resident ≥ --mem-budget`:
  - status `resource_limit`, exit 11 (probe: `--mem-budget 18e9` → 11);
  - before the calibration ledger is built;
  - data.bin and setup.bin are opened through `mmap` (`format.cpp:109`), so no calibration state has been allocated at that point.
- **Islands.** Every `IslandSpec` carries `resident_bytes` and `mem_budget` = budget − resident.
- **Input checks.** `--mem-budget` must be a whole number in [0, 2⁵⁰]. `--plan-only` works with `--n/--p` (no inputs) or with `--data/--setup`.

### M-6 golden coverage: **FIXED for the listed items; one exclusion not justified as stated (N-3)**
- **New comparisons on every `ledger_calib` run:**
  - per calibration island, the stage record: identity; phi, log increment, ESS and cumulative log Z; both distinct counts; the 11 move counts; the partial flag;
  - the stream id, position start / end and init-draws hash, against core's pilot stream and the diagnostic `streams` tables;
  - inherited F, log m, log γ₀ and d on 60 sampled models, against core's R-level scorer;
  - new stop paths through the v4 backend:
    - a forced pilot local_limit (the same R wrapper on core's side, the backend test hook on v4's);
    - a pilot resource stop (core's runtime guard with a 0-hour allocation on both sides).
- **The exclusions listed in `wp4_golden.R:92-98`, judged:**

  | exclusion | justified? |
  |---|---|
  | `fresh`, cache statistics | yes: OD-3, spec §4.1 |
  | timings | yes |
  | calibration local-search archives (path, scanned centres) | yes. The compared ledger (every stored event with its provenance key), the PH_LOCAL logical counts, the HPM, E3 and local_limit pin the scan. |
  | V snapshots | yes. V = {∅} ∪ lead0 ∪ lead1, and both leader stores, every grid, `F_V_evaluations` and the inherited lg0 / d are compared. |
  | calibration pip / ESS estimates | yes. They are not in calib.bin and nothing downstream reads them. log Z and the increments are compared via the stage records. |
  | numerical failure (stated only in the PR comment, "cannot be forced in unmodified core") | **no, as stated** (N-3) |

- **Exclusions that are real but missing from the file:**
  - **A diagnostic-island resource stop.** Core's guard is wall-clock, so only a 0-hour allocation is deterministic, and that stops the pilot. Justified.
  - **The grid-runtime stop and the P3 preflight.** `LedgerBackend` has neither, so they are not applicable.
  - **The bounded rule (D-26) through `ledger_calib`.** It runs only through the core backend (`wp4_calibrate`), so the production V path never runs through `LedgerBackend` in the golden. It cannot be compared with core (D-26 is v4-only). A self-consistency check is possible: ledger backend vs core backend, bounded, same seed.

  All three should be written into the exclusion comment (N-3).

### Minors m-1..m-6: **all FIXED**
- **m-1:** the `calib_backend.h` contract text now covers:
  - the stateful runner, which owns the streams (R6);
  - every status, including the ledger so far on numerical_failure (now equal to WP3 §1.11);
  - the Pilot / Diag role mapping;
  - `init_hash`;
  - u64 stream positions.
- **m-2:**
  - per-iteration diagnostics in meta (`iterations`: logZ_r, island_best, overall_best, E1-E3);
  - the `stage_stream` section (init hash, start, end);
  - `inh_d`;
  - extra keys that collide with meta are refused. Probe: the extra keys `N` and `k_store` give `internal_error`; `seed` is accepted.
- **m-3:**
  - stores, the HPM and inherited models are written only when the status is ok; otherwise `hpm_incomplete` and the HPM so far go in meta;
  - a non-ok calib.bin exposes no inherited models;
  - the merge passes the data and setup hashes to `read_calib`, which compares them with `meta.inputs`. Probe: a data or setup mismatch is refused.
- **m-4** (probes through the binary). Each of these exits 13:
  - `--mode none`;
  - `--I_max` or `--refine_m` in compat or law;
  - `--threads 2.5`;
  - `--refine_m 0`;
  - `--n 2`;
  - `--I_max 25` at p = 10⁶ (ℓ = 20), caught by `Driver::validate` before the WP3 refusal.

  A non-string manifest mode is refused. The setup.bin's data hash is checked against data.bin.
- **m-5:** no clamp; `Driver::validate` refuses instead. Unit test, plus the probe above.
- **m-6:**
  - V and the export use `sorted_unique_models`: flat `ModelView`s, `lex_less` (`std::lexicographical_compare`, the same order as `std::set<std::vector<int>>`), and `same_model` for de-duplication;
  - `InheritedFlat` replaces the per-model vectors;
  - `candidate_set`'s inlined scoring is line-for-line `rescore_V`, with the same chunk of 256 and the same NumericalFailure handling;
  - the golden equality of every grid and of the inherited order confirms both.

## Regressions

None found.
- **Stricter `read_calib`.** It now requires `rule` and, when the status is ok, `k_store`. No calib.bin is committed as a fixture. Every writer in the tree (harness, `test_wp4_io` fixture, toy test) was updated, and all suites pass.
- **`smcbvs4 calibrate` still refuses** (`internal_error`) after validating, so no running path changes.
- **WP5's driver passes only `--threads`** to calibrate, which is still accepted.
- **`test_force_local_limit_pilot` is a public test hook** on the production `LedgerBackend` (nit). Consider guarding it, or naming it in the contract as test-only, which the comment does.

## WP3 interface (stacking `exp/P1M-wp3-calib`; WP3_DESIGN §1.11 v0.6)

- **Compatible:**
  - `IslandRunner::run(const IslandSpec&) → IslandOut` is unchanged.
  - `IslandSpec` gains only `resident_bytes` and `mem_budget`.
  - `IslandOut` gains `init_hash`, and the positions change from `double` to `uint64_t`.
  - `exp/P1M-wp3-calib` has no `IslandRunner` implementation yet (grep). Its only use of `calibrate_with` / `CalibOutcome` is the copy of `calib_run.h` it merged from `453b227c`.
  - `git merge-tree origin/exp/P1M-wp3-calib 7a950fde` is clean.
  - The new header text matches §1.11:
    - stateful runner with caller-owned compat streams 0/5 and 1-4/6-9;
    - partial output on resource_limit;
    - the ledger so far on numerical_failure;
    - leaders on, islands = 4, caps 40p + 1 / 20p / 20p, no tables or inherited models or local search.
- **Notes for WP3's runner:**
  1. **k_store at p ≥ 10⁵.** `run_island` refuses p ≥ 10⁵ without `k_store` (`island_impl.h:1053`). INTERFACES §7 says calibration islands use the setup-derived k. The calibration-role runner therefore needs a role-based exemption, not `k_store_optional`, which is the bench override.
  2. **Memory semantics.** See N-1.
  3. **Admission refusal.** WP3's `status 3` (resource_limit) at admission must come back as `resource_limit` with `partial = false`. At a step boundary it must come back with `partial = true` and the ledger so far.

## New findings

### N-1 MINOR: the `resident_bytes` / `mem_budget` contract is ambiguous and double-counts the inputs
- **Where:** `calib_backend.h:44-46`; `calib_run.cpp` (`island_budget = budget − resident`); `calib_run.h` (`resident` includes `inputs` = data.bin + setup.bin bytes).
- **Evidence:**
  - The header says the island gets "the bytes this calibration process already holds … and the budget left for the island … The island's admission counts both."
  - If WP3 reads "counts both" as `resident + own_peak ≤ mem_budget`, the resident bytes are subtracted twice. At 10⁶ that is ≈ 17 GiB plus inputs.
  - WP3's island plan (INTERFACES §7) already counts X, z, diag(G) and "the setup inputs, whose size the caller supplies". Those are also in `resident` (as file bytes). So the inputs (≈ 8.6 GB at 10⁶) are counted twice in any reading.
- **Impact:** a spurious `resource_limit` at the first calibration island under a budget that would fit. It is deterministic, but it rejects valid runs.
- **Fix:** state one rule. Suggested:
  - `mem_budget` = the whole task's budget (as `IslandConfig::mem_budget` already means);
  - `resident_bytes` = the calibration state excluding X and setup (ledger + export);
  - the island admits iff `resident_bytes + island_plan(including X / setup) ≤ mem_budget`.

  Alternatively keep the remainder and exclude the inputs from `resident`. Either way, write it in `calib_backend.h` and WP3 §1.11.

### N-2 MINOR: the calibration plan's k and its up-front check differ from INTERFACES §7
- **Where:** `calib_run.cpp` (`kbar = max(8, |mode_S| + 1)`; refusal only when `resident ≥ budget`).
- **The k.** INTERFACES §7 plans with k = max(q90(π₀ size) + 1 from setup, …). The island uses `max(8, q90(π₀) + 1, k_store)` (`island_impl.h:1024`). The calibration plan uses the start mode's size instead. With a π₀ larger than the mode, the calibration ledger is under-planned.
- **The up-front check.** When resident < budget < resident + (any island), the command builds the calibration ledger and offers the tables before the first island's admission refuses. Probe: `--mem-budget 20e9` at 10⁶ is admitted with an island budget of 1.27 GiB, and the island ledger alone is 10.8 GiB. The outcome is still `resource_limit`, but after allocation.
- **Fix:**
  - Use the setup's q90(π₀) + 1 (the same helper as WP3's plan).
  - Refuse up front when `total` (resident + one island ledger) > budget. A real island cannot run without its own ledger.

### N-3 MINOR: the numerical-failure golden exclusion is not justified as stated, and three exclusions are not written down
- **Where:** `wp4_golden.R:92-98` and the PR comment.
- **"Cannot be forced in unmodified core" is too strong.** Two ways exist without touching core:
  - **(a) Data-level.** Columns scaled by 1e200 make core's scorer throw `NumericalFailure`. Optionally set the π₀ table entries to −inf so that the failure lands at a Gibbs flip. This is exactly how `test_island.cpp:639-700` forces it, and WP3 §1.11 plans the same fixtures with `CoreRunner` ("ledger so far = CoreRunner's ledger after the failure, bit for bit"). It needs only harness-side data, applied on both sides.
  - **(b) Wrapper-level.** The golden already injects `fail_diag_at` / `fail_V_at` through `with_faults` (`wp4_golden.R:252-253`) for the core backend. A matching runner / backend test hook, as was done for `force_ll_pilot`, would compare the backend's ledger-so-far merge and the HPM so far with `v3_calibrate` on a failure path. That merge is exactly the m-1(a) semantics.
- **Not written down:** the diagnostic-island resource stop (justified), the grid-runtime stop and P3 preflight (not applicable to `LedgerBackend`), and the bounded rule never going through `ledger_calib`.
- **Fix:**
  - Add (b) now, or (a) with WP3's runner tests.
  - Write all of the above into the exclusion comment.
  - Optionally add a bounded-rule self-consistency run: ledger backend vs core backend, same seed.

### N-4 MINOR: the new `read_calib` and `write_calib` refusals have no negative unit tests
- **Where:** `tests/test_wp4_io.cpp`, `tests/test_wp4.cpp`.
- **Evidence:** none of these refusals is exercised in `v4_tests`:
  - V rule, tier or N;
  - I_used ≤ I_max ≤ ℓ;
  - missing or invalid `k_store`;
  - `meta.inputs` mismatch inside `read_calib`. Test `:204` covers the manifest hash, not `meta.inputs`;
  - reserved extra keys.

  My probe shows that all of them behave as specified, but nothing pins them.
- **Fix:** add the probe's cases (V N = 50, tier 1, coded rule, I_max > ℓ, I_used > I_max, k_store 0 / NaN, data or setup mismatch, extra `N`) to `test_wp4_io.cpp`.

### INFO
- **INFO-1:** INTERFACES §5 (calib.bin, line 306) should name `meta.k_store` (double, the mean stored |S| of the calibration top store), plus the new `iterations`, `stage_stream` and `inh_d` sections. This is for WP1, as the author noted.
- **INFO-2 (act before the 10⁶ calibrate):** WP5's `p1m_driver.py:57` gives the 10⁶ calibrate stage **32G**, and the driver passes no `--mem-budget`.
  - This PR's own ESTIMATE is ≈ 30 GB of calibration state plus ≈ 8.6 GB of inputs, ≈ 39 GB.
  - That is before the calibration island's working set. H-9 measured a 10⁶ final island at 34.3 GB peak RSS, which includes X, setup and its store.
  - As configured, a 10⁶ calibration would be OOM-killed by Slurm rather than refused by admission.
  - The manager should have WP5 re-cost this cell from the plan, and pass `--mem-budget` = the Slurm memory minus a margin.
- **INFO-3 (base, not this PR):** `tests/wp5/test_eval.cpp:205` is flaky.
  - `test_data(60, 12, …)` uses the default S0 {3, 9, 15} with p = 12. Line 24 then reads column 15 of a 12-column X, a heap out-of-bounds read.
  - Depending on the heap contents, y becomes non-finite and `data_from_raw` throws. That happened once in the merged run; the case passed in 3/3 isolated runs and in a full rerun.
  - It is unchanged since `f596f27b` (WP5, 2026-11-15) and identical on the base.
  - Fix in WP5: pass an S0 within p, for example `{3, 9, 11}`.
