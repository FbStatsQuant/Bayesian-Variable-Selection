# PR #37 review: WP4 calibration pipeline without the island runner (IslandRunner, LedgerBackend, calibrate_with, calib.bin stages)

- **Reviewer:** Opus 5.5 (high), independent of the author. Template: `briefs/REVIEW_PR_template.md`; rules: `briefs/BUILD_COMMON.md`.
- **Scope:** PR #37, head `453b227c` (`exp/P1M-wp4-calib-run`) into `exp/P1M-engine`. The PR is based on `b1434b59` (INTERFACES v0.1.11). The base has since moved to `4c238a32` (PR #26 island4 and PR #36 INTERFACES v0.1.12).
- **Contract and decisions:** `engine_v4/INTERFACES.md` v0.1.12 (on `exp/P1M-engine`), ENGINEERING_SPEC §1 row 3 and §4.1, DECISIONS D-1, D-7 and D-26, WP3_DESIGN §1.11 (v0.6, commit `5c894da7` on `exp/P1M-wp3-calib`; this section is not yet on `exp/P1M-engine`), and the earlier WP4 reviews (PR16 review and re-check, PR20 re-check).
- **How:** own worktree, detached checkouts, read only. Nothing was pushed, commented or branched. Temp files only in `/home/fb31/SMC_Engineering_Department/tmp/20261116-review-37`, removed at the end. All runs used `nice -n 19` and ≤ 3 threads on Owls, one suite at a time, no NOTS. I stopped only my own processes, by PID.

## Verdict: **ACCEPT-WITH-FIXES** (0 CRITICAL, 6 MAJOR, 6 MINOR, 4 INFO)

The structure is right, and the core claim reproduces: the v4 calibration ledger, local searches, V and inherited export equal `v3_calibrate` when core's own islands are plugged in (MEASURED, below). Merging this PR changes no running path, because `smcbvs4 calibrate` still refuses. The PR still should not merge as is. The runner interface and the V-mode wiring are what WP3 and the 1M pipeline will build on, and the MAJOR findings are defects in exactly those parts:

- **M-1:** V-mode settings come from v3's budgets. At p = 10⁶ that gives H = 204,800 and a final N of 10⁶, against D-1 and D-26 (N = 2,500, H = 512).
- **M-2:** an island refused at admission (`resource_limit`, nothing partial) and any `internal_error` from the runner are reported as `numerical_failure`.
- **M-3:** island ledgers built without leader stores are silently accepted. V then comes from local-search events only.
- **M-4:** calib.bin does not carry the calibration mean |S| that INTERFACES v0.1.12 §7 requires for final islands at p ≥ 10⁵.
- **M-5:** the calibration process's own memory is not accounted anywhere. The command has no `--mem-budget`, and `IslandSpec` has no way to tell the island what is already resident.
- **M-6:** the golden does not compare the stage records, the stream positions, the inherited values or any stop path. The claim "every field bit for bit, calib.bin included" is too broad.

## Test runs (MEASURED, Owls `owls.stat.rice.edu`, Xeon Gold 6148, g++ 11.5.0, 3 threads, `nice -n 19`)

| tree | command | result |
|---|---|---|
| PR head `453b227c` | `TMPDIR=… tests/run_tests.sh --quick --threads 3` | `v4_tests` **107 test cases, 0 failed, 0 check failures**; WP5 driver 17/17 OK; WP5 competitor harness and install script OK; **WP4 golden (quick): 428,237 checks, 0 failures** |
| PR merged onto current `exp/P1M-engine` `4c238a32` (local detached merge `eed6a859`, tree `01c583be`; `git merge-tree` clean, no file overlaps) | same | `v4_tests` **110 test cases, 0 failed** (3 more from PR #26 / v0.1.12); WP5 all OK; **WP4 golden (quick): 428,237 checks, 0 failures** |

- **Check count:** the PR's 1,986,300 is presumably the `--full` golden. I ran the quick level, as asked. The ledger path (`ledger_calib`) runs at every level: every case at 1 and 3 threads, plus P1, P2, P4 and P5.
- **Reviewer probe:** `probe.cpp`, linked against the PR's `libv4_bit.a`, 1 thread. It ran five cases, labelled A–E:
  - A: admission `resource_limit` → `numerical_failure`;
  - B: `internal_error` → `numerical_failure`;
  - C: leaders-off island ledgers → status ok;
  - D: V settings at (200, 10⁶) → H 204,800 and N0 10⁶;
  - E: the I_max clamp.

  Cases A–D are cited in M-1, M-2 and M-3; E is cited in m-5.

## Focus questions

### (1) Does the golden run unmodified core, and which v3_calibrate fields does it compare?

**Core is unmodified. Verified by reading `wp4_golden.R:30-48`:**
- `core/` is copied into the work directory and never written.
- The copy's `v3_core.cpp` and `wp4_harness.cpp` are concatenated into one translation unit and compiled with core's `Makevars.v3`.
- The harness has no `#define` or `#undef` and does not redefine any core symbol.
- `CoreRunner` (`wp4_harness.cpp:545-584`) calls core's `Engine::run_island_s` directly. It uses core's stream ids (0 / 5 + r), seeded as `CalState::stream` does, and continues the streams across rebuilds.

One structural difference from core: core's `CalState` shares one score cache across the whole calibration, while `CoreRunner` uses a fresh cache per island. Cache statistics are on the exclusion list, and every compared field matched, so this is fine.

**Compared by `compare_calib` on the ledger path (`ledger_calib`, `wp4_golden.R:91-108`, 111-144):**
- status, tier_final, escalated;
- per tier: status, triggers, pilot schedule, every grid (label, grid, rho_appended, ok, reason, intervals, F_V_evaluations);
- per iteration: iteration, grid, rho_V, label, log_Z_r, island_best, overall_best, E1, E2, E3;
- per tier: converged, rebuilds, grid, rho_V, label, source;
- all flags except `triggers_by_tier` (covered by the per-tier triggers);
- frozen grid, tier, rho_V, label;
- calibration HPM and provenance, top store, both leader stores, logical counters, island_best.

On the calib.bin round trip it also compares grid, tier, N, the inherited models (order and content), the HPM and provenance, and the **number** of stage records.

**Not compared:**

| v3_calibrate field | on the compat exclusion list (spec §4.1)? |
|---|---|
| `ledger$fresh` | yes (OD-3) |
| `cache` | yes (OD-3) |
| `seconds`, `pilot$seconds`, `grid_construction$seconds` | yes (timings) |
| `stage_table` (phi, log increment, ESS, cum, moves, distinct counts of the pilot and every diagnostic island) | **no**: class B. Only the record count is checked (M-6) |
| `pilot$stream`, `iterations[[k]]$streams` (stream id, position start and end, `init_draws_hash`) | **no**: stream positions are class B in §4.1. `IslandOut.position_*` is filled and then dropped, and `init_hash` is not in `IslandOut` at all (M-6, m-1) |
| `pilot$calibration_estimate` (log_Z, pip, ess, log_increment), `iterations$calibration_estimate` (pip_r, ess) | **no** (M-6) |
| `pilot$local_search`, `iterations$local_search` archives (path, scanned centres, termination, moves) | **no**: only their effects (HPM, ledger, E3, local_limit) are checked |
| `snapshots` (V snapshot: size, models, lg0, d) | **no**: indirectly covered by the grids |
| `frozen$inherited` values (F, lg0, log m are a v4 addition) | **no**: models only, and only via calib.bin. T9 runs from v3's frozen object, so the v4 ledger path's inherited values are never compared |
| `frozen$L`, `frozen` hash | **no** |
| `message` and partial archives on stop paths | **no**: no stop path goes through the v4 backend in the golden (M-6) |

### (2) Is the runner interface sufficient and unambiguous for WP3?

It is close, but not yet. See M-2, M-3 and m-1.
- **Partial output on `resource_limit`.** The interface asks for status `resource_limit` together with `partial = true`. It does not cover the admission refusal (status `resource_limit`, nothing run, so `partial = false`). That case becomes `numerical_failure` (M-2).
- **Partial output on `numerical_failure`.** The header and WP3 §1.11 disagree on what to return (m-1).
- **Ledger configuration.** The required configuration (islands 4, leaders on, caps 40p + 1 / 20p / 20p, empty start with no tables or inherited models) is stated in WP3 §1.11. Nothing enforces it (M-3).
- **Stream ownership.** It is implicit: `IslandSpec` carries no seed, mode, stream handle, N, thread count or memory budget. The runner must therefore be a stateful object that keeps the streams across rebuilds (R6). `CoreRunner` does this, but `calib_backend.h` does not say so (m-1).

### (3) V-1M bounded rule (D-26)

The **Driver** is correct. I read `calib.h:172-299`, and the PR16 tests cover it:
- it never escalates (`fired` is coded-only);
- it refuses `tier0 ≠ 0` and `I_max ∉ [0, ℓ]` with `invalid_input`;
- on a construction failure it installs the last successfully built grid (`g` is replaced only by a successful build), else the pilot schedule, and sets the flag `grid_fallback`;
- otherwise `grid_unconverged`.

The PR's **wiring** of the rule is wrong:
- M-1: wrong H and N for V.
- m-5: `settings_from` silently clamps I_max to ℓ instead of refusing. It is also inconsistent with the command, which overwrites the clamp.
- m-4: the command throws `internal_error` before the Driver is built, so `I_max > ℓ` is not refused yet.

### (4) calib.bin validation before use, and GUARD-W

**What `read_calib` checks (`wp4_io.cpp:206-231`):**
- kind;
- N, L, Hm and tier ranges;
- that the grid is valid when status is ok;
- the HPM and inherited models are in range;
- inherited values are finite.

**What the merge adds:**
- it refuses a calib.bin whose status is not ok, or whose mode differs;
- it checks the calib.bin content hash against the manifest.

**Not checked:**
- the calib.bin `meta.inputs` (data and setup hashes) against the data and setup in use;
- in V mode, that the rule is bounded, the tier is 0 and N = 2,500;
- `I_used ≤ I_max ≤ ℓ`.

The writer writes stores, the HPM and inherited models on any status. GUARD-W holds today only because the merge refuses a calib.bin whose status is not ok (m-3).

### (5) Memory at p = 10⁶

Not accounted (M-5). ESTIMATE, assuming a mean |S| of about 10 and about 66 B per store entry:

| item | entries / size |
|---|---|
| calibration ledger: top (40p + 1), lead0 (20p), lead1 (20p) | 8·10⁷ entries ≈ 5.3 GB |
| an island ledger of the same caps, held in `IslandOut` while merging | another ≈ 5.3 GB |
| staging growth during `Store::merge` | up to ≈ 1.5× the incoming entries |
| V as `std::set<Model>` plus its vector copy (≤ 4·10⁷ + 1 models) | ≈ 8 GB |
| inherited export: `std::set<Model>` U, its copy, and `InheritedModel` (≤ 8·10⁷ models) | ≈ 20–25 GB |
| write_calib flat copies | further GB |

These are on top of the island's own peak (X, the H particles, setup tables). None of this is counted:
- the command has no `--mem-budget`;
- `IslandSpec` cannot pass the resident calibration state to WP3's admission, so the island cannot apply the v0.1.10 "whole task" rule.

Diagnostic islands run one at a time, and each island ledger is freed after its merge. That part is fine.

### (6) CLI input validation

Partial (m-4):
- `--mode none` is accepted and runs the coded rule;
- I_max, refine_m and threads are cast from double without integer or range checks (2.7 becomes 2; 1e12 is undefined behaviour);
- in theory mode, `--I_max` and `--refine_m` are silently ignored;
- the setup.bin's own data hash is not checked against data.bin;
- the refusal message says "inputs validated", but the Driver's checks (`I_max ≤ ℓ`, `refine_m ≥ 1`) have not run.

The required arguments and the seed range are checked.

## Findings

### M-1 MAJOR: V-mode calibration uses v3's budgets: H = 204,800 and N = 10⁶ at p = 10⁶ (D-1, D-26)

- **Where:** `include/v4/calib_run.h:36-40` (`settings_from`); `src/calib/calib_run.cpp:26-32`; `tests/test_wp4.cpp:585-586`.
- **Evidence:**
  - `settings_from(budgets(n, p), Rule::bounded)` takes `tiers[0].H = H0 = ceil(512·max(2500, n, p)/2500)`.
  - Probe (MEASURED): n = 200, p = 10⁶ gives tier-0 H = **204,800**, T_e = 1000, L = 8, ℓ = 20, and N0 = **1,000,000**.
  - D-26: "in V-1M there is **no tier escalation**: N = 2,500 and H = 512 always (D-1)". `calib.h:8` says so too.
  - The final N that will go into calib.bin (`CalibWrite.N`) has no V rule either. The merge takes `ms.N = C.N` unchecked.
  - The unit test pins the v3 values for (200, 10⁶). That is right for the coded rule, but there is no test of the V settings.
- **Impact:** once WP3's runner is plugged in, a V calibration at 10⁶ runs 400× too many particles per calibration island, and the frozen N would be 10⁶.
- **Fix:**
  - `settings_from(b, Rule::bounded)` sets H = 512 for tier 0 (and blanks tier 1), and the frozen N = 2,500 (constants named after D-1 / D-26).
  - Write N into calib.bin from the rule, not from the v3 budgets.
  - `read_calib` (or the merge) refuses a V calib.bin with tier ≠ 0, rule ≠ bounded or N ≠ 2,500.
  - Add a unit test of the V settings at (200, 10⁶).

### M-2 MAJOR: a runner's `resource_limit` without `partial`, or any other status, becomes `numerical_failure`

- **Where:** `include/v4/calib_backend.h:75` and `:96`.
- **Evidence:**
  - `if (io.status != Status::completed && !io.partial) → CalStatus::numerical_failure`.
  - INTERFACES §7: island admission "refuses deterministically with `resource_limit`, before any allocation". Such an island has nothing partial.
  - Probe (MEASURED):
    - A runner returning `resource_limit`, `partial = false` gives calibration status `numerical_failure` and task status `numerical_failure` (exit 13 instead of 11).
    - A runner returning `internal_error` gives `numerical_failure` with the message "pilot: admission".
  - The status is wrong exactly where it matters at 10⁶: a memory refusal is reported as a numerical failure.
- **Fix:**
  - Map `Status::resource_limit` to `CalStatus::resource_limit` whatever `partial` is.
  - Throw `Error(io.status, …)` for `invalid_input`, `internal_error` and `io_error`, so `main` records the true status.
  - State in `IslandOut` that `partial` ⇔ (status == resource_limit and the island had started).
  - Add a toy test for each status.

### M-3 MAJOR: island ledgers without leader stores (or with other caps) are merged silently, and V is then wrong

- **Where:** `include/v4/calib_backend.h:77, 98, 131-134`; `src/common/ledger.cpp:32-33, 76-79`.
- **Evidence:**
  - `merge_tally` checks only `p` and `islands`.
  - `Store::merge` offers into whatever cap the calibration store has, and skips stores whose cap is 0.
  - WP3_DESIGN §1.11 says "`Ledger::merge` refuses a mismatch". It does not.
  - Probe (MEASURED): a runner whose island ledgers have `leaders = false` completes with status **ok**. The calibration lead0 and lead1 then hold only local-search events (40 each at p = 20), so V and the grid are silently wrong.
  - An island ledger that ingested tables or inherited models is also not detected. It would double-count the TABLE logical counters.
- **Fix:**
  - Check in `LedgerBackend` (or in `Ledger::merge`) that the island ledger has `leaders == true`, the same caps and orders for top, lead0 and lead1, and `logical[PH_TABLE] == 0` and `logical[PH_INHERITED] == 0`.
  - Else raise `internal_error`.
  - Add a toy test.

### M-4 MAJOR: no calibration mean |S| in calib.bin (INTERFACES v0.1.12 §7, merged after this PR's base)

- **Where:** `include/v4/calib_backend.h` (`IslandOut`); `include/v4/wp4_io.h` (`CalibWrite` / `CalibIn`); `wp4_io.cpp:142-231`.
- **Evidence:**
  - v0.1.12 §7: admission plans the store with k = max(q90(π₀ size) + 1, **calibration's measured mean |S| when calib.bin exists**).
  - At p ≥ 10⁵ "a final island without a calib.bin k is refused with `invalid_input`".
  - `IslandOut` has no |S| statistic, the backend aggregates none, and calib.bin has no such field.
- **Impact:** once v0.1.12 admission is in, every 1M final island would refuse.
- **Fix:**
  - Add a measured size statistic to `IslandOut` (for example the sum of |S| and a count over the measured rounds, so the mean is exact and order-free).
  - Aggregate it in `LedgerBackend` and write it to calib.bin meta with a declared name.
  - Expose it in `CalibIn` and check it is finite and positive.
  - Agree the definition with WP3 / WP1: which rounds, particles or events.

### M-5 MAJOR: the calibration process's memory is not accounted (`--mem-budget`, v0.1.10 "whole task")

- **Where:** `src/calib/calib_run.cpp` (no `mem_budget`); `IslandSpec` (no budget or resident-bytes field); `calib_run.h:61-69` and `calib_backend.h:105-113` (`std::set<Model>` for the inherited export and V).
- **Evidence:** the ESTIMATE in focus (5): ≈ 5 GB for the calibration ledger, ≈ 5 GB for each island ledger in flight, and up to ≈ 25 GB for the inherited export through `std::set` / vector-of-vector at 8·10⁷ models.
  - The island admission cannot see the calibration ledger, which is resident in the same process.
  - Nothing refuses before allocation.
- **Fix:**
  - Accept `--mem-budget` in `calibrate` (same parsing as the merge, PR20 n-4).
  - Plan the calibration-side peak: three stores, one island ledger plus merge staging, V and the export.
  - Pass the resident bytes (or the remaining budget) to the runner through `IslandSpec` so WP3's admission counts the whole task.
  - Build V and the export with a k-way merge of the sorted stores into a flat pool (m-6). This removes most of the `std::set` overhead.

### M-6 MAJOR: golden coverage is narrower than claimed (stage records, stream positions, inherited values, stop paths)

- **Where:** `tests/golden/wp4_golden.R:91-108, 111-144`; `wp4_harness.cpp:545-584, 660-674`.
- **Evidence:** see the table in focus (1).
  - The calibration `stage_table` and the stream positions are class B in spec §4.1 and are not on the exclusion list. The stage records written to calib.bin are only counted.
  - The inherited F, lg0 and log m are never compared.
  - The ledger path runs only status-ok cases plus P1, P2, P4 and P5. No `resource_limit`, `numerical_failure`, forced `local_limit` or preflight-blocked path goes through `LedgerBackend` against core. Those paths are toy-tested only.
- **Fix:**
  - Export `oc.stages` and the per-island stream positions and init hash from the harness, and compare them with `r$stage_table` and `r$tiers[[i]]$pilot$stream` / `iterations[[k]]$streams`.
  - Compare the inherited F, lg0 and log m with core scores (`cpp_cal_V`-style scorer).
  - Run `coded_path`'s `force_ll_pilot` and the numerical-failure fixture through `ledger_calib`.
  - State the remaining exclusions in the PR.

### m-1 MINOR: runner contract ambiguities (WP3 §1.11 vs `calib_backend.h`)

- **(a) `numerical_failure`:**
  - The header says the ledger so far is merged if the runner returns one.
  - WP3 §1.11 says "status and message only".
  - Core's shared ledger keeps those events, and `v3_calibrate` exports the ledger even on failure.
  - Pick one rule and write it in both places.
- **(b) Streams and settings:** the seed, mode, stream ownership across rebuilds (R6), N, threads and budget are not in `IslandSpec`. Document that the runner is a stateful object created per calibration, holding seed, mode and streams.
- **(c) Missing outputs:** `IslandOut` lacks `init_hash`, which §1.11 lists and core reports. Stream positions are `double`; they are exact to 2⁵³, which is fine, but say so.
- **(d) `role`:** `IslandSpec.role` uses values 1 and 2, while WP3's `IslandConfig::role` has `Final` / `Pilot` / `Diag`. Name the mapping.

### m-2 MINOR: calib.bin content vs spec §1 row 3 and INTERFACES §5

- **Missing:**
  - per-iteration triggers and diagnostics (E1, E2, E3, log Z_r, island_best);
  - the stream addresses used;
  - `d` for the calibration stores ("stored F, log γ₀, d").
- **`CalibWrite.extra`** is copied into meta after status, tier and N (`wp4_io.cpp:201`), so it can silently overwrite them. Refuse reserved keys.

### m-3 MINOR: calib.bin validation and GUARD-W

- `read_calib` does not check `meta.inputs` against the data and setup actually loaded. In the explicit merge form nothing ties calib.bin to them.
- It does not check rule, tier or N against the mode (see M-1), or `I_used ≤ I_max ≤ ℓ`.
- `write_calib` writes stores, the HPM and inherited models for any status. Write them only when status is ok (or mark them clearly as partial), and have `read_calib` refuse to expose them otherwise.

### m-4 MINOR: CLI validation (`src/calib/calib_run.cpp:17-34`)

- `--mode none` is accepted and becomes the coded rule. Accept only compat, law and V.
- A non-string manifest `mode` reaches `.str()`.
- I_max, refine_m and threads are cast from double unchecked. Require whole numbers in range.
- `--I_max` and `--refine_m` are silently ignored in theory mode. Refuse them.
- setup.bin's own data hash is not compared with data.bin.
- Construct the Driver (or call a `validate(Settings)`) before the WP3 refusal, so `I_max > ℓ` returns `invalid_input` now and the "inputs validated" message is true.

### m-5 MINOR: `settings_from` silently clamps I_max to ℓ (`calib_run.h:39`)

D-26 makes I_max ≤ ℓ a requirement, and the Driver refuses a violation. The clamp hides a violation for library callers (probe: at ℓ = 2, I_max 3 becomes 2), and the command overwrites the clamp anyway. Remove it and let the Driver refuse.

### m-6 MINOR: V and the inherited export via `std::set<Model>` at 10⁶ (`calib_backend.h:105-113`, `calib_run.h:61-69`)

- The cost is about 8·10⁷ heap-allocated vectors plus set nodes, then a full copy, then `InheritedModel` copies (≈ 20–25 GB, ESTIMATE).
- lead0 and lead1 are already in lexicographic order; top is not.
- Fix:
  - sort a flat index of top;
  - k-way merge the three stores with deduplication into one pool and offset array;
  - score in place.
- This also bounds the time; the sorted order itself is the same.

### INFO

- **I-1. Unmodified core in the golden:** verified (focus 1). The golden compares the v4 calibration ledger itself (stores, leaders, logical counters, HPM and provenance, island_best). This is the strongest part of the PR.
- **I-2. D-26 in the Driver:** verified by reading. One edge: in the bounded rule, if the pilot schedule failed `check_grid`, the status would be `grid_failure_no_escalation` (no output). A completed pilot always ends at 1 and increases strictly, so this cannot happen. It predates this PR (PR16).
- **I-3. No runtime guard or preflight in `LedgerBackend`:** it inherits `Backend::grid_stop` and `preflight_exceeds` as false. In production the coded rule's escalation is therefore never blocked by a preflight. The tier-1 islands' admission must refuse instead, which depends on M-2.
- **I-4. Discipline:** nothing is written outside `engine_v4/`. There are no hard-coded paths and no large files. The `stubs.cpp` removal of `calib` is consistent with `calib::run` now living in `src/calib/calib_run.cpp`. The `tail.h` change (CALIB keys, `iter` as int8) is safe: iter ≤ ℓ ≤ 31 for p < 2³¹.
