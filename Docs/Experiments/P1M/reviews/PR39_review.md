# PR #39 review — WP3 calibration roles (PILOT / DIAG), CalibIslandRunner, `smcbvs4 calibrate` plugged in, re-check m1 / m2

Reviewer: independent (Opus 5.5, high), 2026-11-16. Base: `exp/P1M-engine` 571f11bc.
- **Heads:** I reviewed **e8bef8b0** in full. **fcdcd2c0** was pushed during the review (the N-1 admission, see
  MAJOR-1); I reviewed that diff and tested it inside the whole stack (#43 head 8d584649, full `run_tests.sh`).
- **Contract:** INTERFACES v0.1.13 on the branch, plus the calibration memory rule of v0.1.14 §7 (shared docs; WP4
  N-1, LOG 07:37).
- **Design:** WP3_DESIGN §1.11, §1.12. **WP4 interface:** `include/v4/calib_backend.h`.

## Verdict: **ACCEPT-WITH-FIXES** (mergeable now; the fixes are follow-ups)

- The calibration roles, the runner and the ledger so far are correct. There is no bit divergence; the goldens compare
  against core, and WP4's whole-calibration golden with WP3's islands equals `v3_calibrate`.
- The calibration memory rule was missing at e8bef8b0 (MAJOR-1). It is now implemented on the WP3 side at fcdcd2c0.
- **What remains:**
  - a scale problem: at 10⁶ the V calibration does not fit the driver's 64 G task until StartView lands, and
    `--plan-only` cannot show it (MAJOR-2, for the manager / driver);
  - WP4's half of N-1: the up-front refusal (MINOR-6);
  - test gaps.

Counts at fcdcd2c0: **0 CRITICAL, 1 MAJOR (+ 1 MAJOR resolved), 6 MINOR** (+ 4 INFO).

## Test runs
**fcdcd2c0, inside the stack** (#43 head 8d584649 = fcdcd2c0 + #42 + #43; see PR43_review.md):
- v4_tests **115 / 115**, including `calibration_admission_n1_rule`. T3 hashes are unchanged.
- WP4 R golden **528,081 checks, 0 failures**, the six `runner = "wp3"` runs included.
- WP5 extras OK.

### e8bef8b0 (Owls, Xeon Gold 6148, gcc 11.5, `nice -n 19`, 3 threads, fresh build from `git archive`)
`TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/20261116-review-39-43/t39 tests/run_tests.sh --threads 3` (quick):
- v4_tests: **114 test cases, 0 failed, 0 check failures**.
  - Island goldens vs core: `golden_island_vs_core_engine`, `golden_compat_island_vs_core_serial_stream`,
    `golden_calibration_islands_compat_vs_core` (3.7 s), `golden_calibration_islands_law_vs_core` (5.7 s) and
    `golden_calibration_failure_ledger_so_far` all pass.
  - T3 hashes: bit `44a15bfc6fb8d233` and A `d2df149413596a19` (default build) on every kernel / thread / G / tile row.
    These equal the PR's values.
  - `mem_plan_bounds_measured_peak_2e4` holds the plan ≥ 1.10 × measured bound in every row. MEASURED here (peak
    increment / plan, MiB):

    | row | measured | plan |
    |---|---|---|
    | LM G 64 | 202 | 272 |
    | LM G 64, leaders | 325 | 532 |
    | LM G 256 | 266 | 397 |
    | LM G 256, leaders | 352 | 657 |
    | PM 3 threads | 29 | 238 |
    | PM 3 threads, leaders, N 250 | 229 | 498 |
    | LM calibration island | 331 | 649 |

    The smallest margin is +30%. The measured values vary between runs (the PR has 81 and 186 MiB for the PM rows).
  - `calibrate_command_end_to_end`: compat 8.5 s, law 2.9 s, V 6.4 s / 5.0 s (1 / 3 threads); V is the same at 1 and
    3 threads.
- WP5 driver 17 OK; competitor harness OK; install script OK (23 checks).
- WP4 R golden: **528,081 checks, 0 failures**, the same as the claim. The six `runner = "wp3"` whole-calibration runs
  equal `v3_calibrate` bit for bit:

  | case | checks |
  |---|---|
  | AR0.9 p30 | 4,855 |
  | AR0.6 p40 | 6,134 |
  | AR0.6 p40, tier-1 start | 5,996 |
  | AR0.9 p120 | 17,524 |
  | IND p60 | 8,660 |
  | AR0.5 p300 | 41,314 |

  The per-case counts are higher than the PR table because PR #37's re-check added stage / stream checks.

## Findings

### MAJOR-1 — the calibration memory rule (INTERFACES v0.1.14 §7, WP4 N-1) was not implemented — **RESOLVED at fcdcd2c0 (WP3 side)**

**Resolution, checked at fcdcd2c0:**
- `calib_runner.h:44` adds `spec.resident_bytes` to the island plan's caller-supplied inputs term and keeps
  `mem_budget` = the spec's budget.
- `calib_run.cpp:140` passes `resident = ledger + export` (no inputs) and the whole `--mem-budget`.
- So an island is admitted iff resident + plan ≤ budget. The resident bytes sit in the `inputs` term, so they get no
  12% headroom. The admission, the G-reduction loop and the step-boundary `over_budget` all see the same total
  (`msz.inputs_bytes`).
- The double count of X / setup is gone.
- New test `calibration_admission_n1_rule`: refused at plan − 1 with `partial = false`, admitted at plan, and admitted
  at plan − resident without resident. It passes in the stack run.
- Items 1–3 below are fixed. Item 4 (the up-front refusal) is WP4's code and remains: MINOR-6.

As found at e8bef8b0:
The rule: islands get `mem_budget` = the whole task's budget; `resident_bytes` = calibration ledger + inherited
export, **excluding** data and setup inputs; an island is admitted iff `resident_bytes + plan ≤ mem_budget`;
`calibrate` refuses up front, before any allocation, iff `resident + inputs + one island ledger > --mem-budget`.

What the PR does instead:
1. **`calib_run.cpp:139`** passes `island_budget = budget − plan.resident` as `IslandSpec::mem_budget`. **`calib_run.h:79`**
   has `resident = ledger + export + inputs`, where `inputs` = the data.bin + setup.bin file bytes.
2. **`calib_runner.h:41`** ignores `IslandSpec::resident_bytes` and admits on `plan ≤ spec.mem_budget`. So once WP4
   lands N-1 (`mem_budget` = the whole budget), this runner would admit every island **without** the 17.4 GiB
   (10⁶) resident state. It would over-admit and risk an OOM kill instead of a deterministic `resource_limit`. The two
   sides must change together.
3. **The inputs are counted twice.**
   - X is in `resident` (data.bin bytes) and again in the island plan's `inputs` term (n·p·8 + 16p).
   - The setup is in `resident` (setup.bin bytes) and again as `rc.inputs_bytes = start_bytes(st, nb)`
     (`calib_run.cpp:129`).
4. **The up-front refusal is only `resident ≥ budget`** (`calib_run.cpp:115`, WP4's code). `load_start` then expands
   dep::Start, which is 13–38 GB at 10⁶ (WP2, D-31), at `calib_run.cpp:126` before any check counts it. An
   undersized budget is then exceeded by an allocation, not refused.

- **Impact at 10⁶** (ESTIMATE, from `island_memory()` of this head: n 200, p 10⁶, 96 threads, label-major,
  deferred, leaders, calibration snapshot, k = 8; `inputs_bytes` = 0):
  - the calibration island's plan is **30.1 GiB at G = 1, 31.9 at G = 64 and 37.2 at G = 256**;
  - the driver's calibrate task is 64 G with `--mem-budget` = 90% (57.6 GB = 53.6 GiB);
  - with this PR the island budget is 53.6 − (17.4 + ≈ 8 GiB of files) ≈ 28 GiB, below the G = 1 floor, so the
    **V pilot is refused (`resource_limit`) whatever the Start size**.
  - Under the N-1 rule it is 17.4 + 31.9 + start_bytes. That fits only if start_bytes < ≈ 4 GiB, which today's
    dep::Start does not meet (see MAJOR-2).
- **Fix (small).**
  - Runner: admit iff `resident_bytes + plan ≤ mem_budget`. For example, pass `c.mem_budget = sp.mem_budget`, add
    `IslandConfig::resident_bytes`, and use `resident + mp.total` in the admission, in the G-reduction loop and in
    `over_budget` at step boundaries.
  - `calibrate`: pass the whole budget and `resident = ledger + export`. Refuse up front on `resident + inputs + one
    island ledger`, with inputs = data + **start_bytes**. Ideally compute start_bytes before `load_start` expands
    the Start, from the setup section sizes.
  - Add a `calibrate --mem-budget` test (see MINOR-1). Agree the change with WP4 so that only one side subtracts.

### MAJOR-2 — 10⁶ V calibration does not fit the driver's 64 G task; `--plan-only` cannot show it (scale; ESTIMATE)
- `calibrate --plan-only` reports WP4's plan: 17.4 GiB resident + 10.8 GiB island ledger + inputs ≈ 36 GiB.
  - It does **not** contain the calibration island's own plan: 30.1 / 31.9 / 37.2 GiB at G = 1 / 64 / 256, before
    the Start (MAJOR-1).
  - Its `island_budget` field (`calib_run.cpp:69`, budget − resident with the inputs) no longer describes what
    islands receive after fcdcd2c0.
- The true peak of the calibration task is about `resident + island plan + start_bytes`.
  - At fcdcd2c0, with the N-1 rule, the island is admitted iff 17.4 + 30.1 (G = 1) + start_bytes ≤ 53.6 GiB, so
    only when **start_bytes ≤ ≈ 6 GiB**.
  - Today's dep::Start (13–38 GB, WP2) is refused at the V pilot. The task then ends with `resource_limit` and
    produces no calib.bin. This is deterministic and safe, but it blocks the 10⁶ calibration pilot that H-11 makes
    the next measurement.
  - With StartView (4.4–14.1 GB of setup sections) it fits only at the low end and with a reduced G.
  - Unconstrained, the peak at G = 64 is ≈ 17.4 + 31.9 + start ≈ 61–85 GiB today and ≈ 53–63 GiB with StartView
    (ESTIMATE).
- **Fix.**
  - Have `--plan-only` print the island plan as well (`plan_island` with a calibration `IslandConfig`, the
    V-mode N / threads / k from setup) and the total.
  - The manager re-sizes the 10⁶ calibrate task from it, likely ≥ 96 G until StartView lands. This sits with the
    driver re-size already noted in LOG 07:09.

### MINOR-1 — the runner's resource paths are not tested through the runner or the command (partly addressed at fcdcd2c0)
- `calibrate_command_end_to_end` never passes `--mem-budget`, so `island_budget`, the up-front refusal and an
  island admission refusal through `calib::run` (exit 11) are not exercised.
- `partial = true` (a step-boundary stop with the ledger so far) is only tested with WP4's toy runner
  (`test_wp4.cpp:504-583`). At fcdcd2c0, `partial = false` (admission) is tested through `CalibIslandRunner`
  (`calibration_admission_n1_rule`).
- The R golden's resource stop uses core's runner only (`wp4_harness.cpp`: "runtime guard applies to core's runner
  only").
- **Fix:**
  - a `CalibIslandRunner` test with `mem_budget` = plan − 1 (`resource_limit`, `partial == false`, empty ledger);
  - a step-boundary refusal via `test_admission_k` (`partial == true`, the schedule / stages / ledger so far merged
    by `LedgerBackend`);
  - a `calibrate --mem-budget` run that refuses.

### MINOR-2 — `load_start` partition checks have two holes (`setup_load.h:21-33`)
- `blk_ptr[0] == 0` is not checked.
  - With `blk_ptr[0] = 1`, the blocks cover `members[1..p-1]`. One variable keeps `blk = -1` and nothing reports it.
  - With `blk_ptr[0] < 0`, `members[blk_ptr[b] + i]` reads before the array.
- `blk_ptr[b+1] ≥ blk_ptr[b]` is enforced only through `m ≥ 1`, which is fine.
- **Fix:** require `blk_ptr[0] == 0`, and after the loop that every `blk[j] ≥ 0`. setup.bin is hash-checked WP2
  output, so this is defensive, but the function claims `invalid_input` on a bad partition.

### MINOR-3 — the round-start snapshot is taken in compat, where it is never used (`island_impl.h:662`, `:952`)
- Compat stops at the first failure and never calls `rebuild_prefix` (`if (calib && !csrc && snap.valid)`).
- Yet every compat calibration round copies the population (`snap.P = P`). It also pins the round-start kept runs,
  so compaction cannot free them during the round.
- The cost is small at compat sizes (p ≤ 5k), but it is dead work, and the plan's `calib_snapshot` term is charged
  to compat islands too.
- **Fix:** `if (calib && !csrc)`.

### MINOR-4 — the static-library cycle works but is fragile (`island.cmake:12`)
- `v4_bit PUBLIC v4_a` + `v4_a PUBLIC v4_bit` relies on CMake repeating strongly connected static libraries
  (LINK_INTERFACE_MULTIPLICITY, default 2). It links today (all targets built).
- But every v4_bit-only tool (`v4_pmath_check`, `v4_bench_store`, `v4_bench_score`, `v4_bench_wp4_fv`) now also
  links v4_a.
- A third object that needs a symbol two levels deep around the cycle would need the multiplicity raised.
- **Fix:** move `calib_run.cpp` (and later `island_cmd`) into a small `v4_cmd` library that links `v4_a v4_bit`,
  so the libraries form a DAG again. This is accepted as interim until m9; recorded here so it is not forgotten.

### MINOR-5 — golden coverage relative to the claims
- The completed-island law golden runs particle-major at 1 thread and label-major at 3 threads.
- Label-major at 1 thread and particle-major at 3 threads are compared to core only on the failure-prefix fixture.
- Tier-1 diagnostic streams 6–9 are not in the C++ sequence (tier-0 pilot, tier-0 diagnostics, tier-1 pilot). They
  are covered by the R golden's "P2 tier-1 start" run with `runner = "wp3"`.
- **Fix (cheap):** add `{LM, 1}` and `{PM, 3}` to the law loop, and a tier-1 diagnostic rebuild to `cal_sequence`.

### MINOR-6 — WP4's half of N-1: the up-front refusal (`calib_run.cpp:115`, unchanged at fcdcd2c0)
- The rule: refuse up front iff `resident + inputs + one island ledger > --mem-budget`. The code refuses only on
  `resident ≥ budget`.
- `load_start` then expands dep::Start (13–38 GB at 10⁶) at `calib_run.cpp:126`, before any check counts it.
- Under an undersized budget this allocates before the island admission refuses. That admission now does refuse
  deterministically, but only after the Start and the calibration ledger with its tables are built.
- The calibration plan's k is still `max(8, |mode| + 1)` instead of `max(8, q90(π₀) + 1)` (WP4 N-2).
- **Fix (WP4):**
  - implement the rule's up-front check with inputs = data + the Start bytes. The Start bytes can be computed from
    setup.bin section sizes before expansion, or from the island plan once StartView lands;
  - use the setup's q90 for k, the same helper as `plan_island`;
  - drop or redefine `island_budget` in `plan_json`.

### INFO
- **I-1 ISA propagation is sound for bits.**
  - With `V4_ISLAND_ISA`, `calib_run.cpp` (WP4 calibration templates: FV, grid rules, local search) compiles with the
    island `-march` and keeps `-ffp-contract=off`. GCC does not vectorise FP reductions without reassociation, so
    the values are unchanged.
  - COMDAT copies of shared inline functions may be taken from that TU. The binary then needs the island ISA
    everywhere, which an `x86-64-v4` / `sapphirerapids` build needs anyway.
  - `-DV4_WIDE_ISA=ON` without `V4_ISLAND_ISA` puts `island_a.cpp` in `isa_fma` and its callers in `isa_base`. That
    configuration is unused by the scripts and probably did not link before this PR either (not built here); m9
    resolves it.
- **I-2** `fix_mmap_threshold()` is process-wide and permanent. In `calibrate` law mode (particle-major, threads > 1)
  it also changes how WP4's later large allocations (stores, V) are served. This affects performance only.
- **I-4** The N-1 rule counts the setup once, as the expanded dep::Start. `calibrate` also keeps setup.bin
  mapped: the table stores and `logr` are read through `SetupView`. Its touched pages are page cache that Slurm's
  cgroup charges to the task. Until StartView replaces the expanded copy, the real footprint can exceed the plan by
  the touched part of setup.bin (up to ≈ 7 GB at 10⁶, ESTIMATE). Worth a VmRSS + cgroup reading on the 10⁶ pilot.
- **I-3** `compat_stream` throws `std::out_of_range` (not `v4::Error`) for tier > 1, and `IslandRun` status 1 maps
  to `resource_limit` in the runner. Neither is reachable from WP4's calibration today.

## Checked and correct
- **Addresses and keys.**
  - Role PILOT / DIAG, tier e, iter k, island r in `addr()`.
  - `base_key()`: SG_CALIB, tier, iter, unit r.
  - MEASURED event round L + h (`RoundCtx` `ev_round`).
  - Phases PH_PILOT / PH_DIAG via `phase_of`.
  - Validation: pilot island 0 / iter 0; diagnostic 1..4 / k ≥ 1; tier < 4, iter < 64; no checkpoints.
- **Compat streams** `5·tier + island` equal core's `CalState` streams 0 / 1–4 / 5 / 6–9 (`v3_core.cpp:593-596`,
  `rng.h:104`). The runner continues them across rebuilds and tiers, and it records `stream_start` / `stream_count`.
- **Ledger so far.**
  - Kept runs are immutable once published (`make_shared<Kept>` per compaction), so the round-start `shared_ptr`
    snapshot is safe.
  - `sync_ledgers` compacts at every step boundary, so `restore()` clearing the staging loses no earlier event.
  - `reset_counters` clears HPM / island_best / logical / moves.
  - Label-major fails group by group with the smallest particle index, so `last_fail_particle` is the global
    smallest failing particle.
  - The replay is serial particle-major at the same addresses.
  - `NumericalFailure` is thrown only from `throw_if_failed()` in the island, so `last_fail_particle` is always set.
- **`to_record`.**
  - Calibration ledger config: islands 4, leaders on, caps 40p + 1 / 20p / 20p.
  - HPM φ from the event key.
  - The pilot has no island_best; leaders are offered.
  - WP4's `check_island_ledger` passes in the R golden.
- **Schedule on a stop:** φ only for completed stages (`min(stages, grid − 1)`).
- **m1:**
  - serial staging reserved at limit + buf_limit;
  - leaders' staging reserved;
  - plan terms `calib_snapshot` and 12% headroom (inputs excluded) match `memory.h`.
- **m2:** `k_store` is required only for a final island with a budget at p ≥ 10⁵; calibration islands plan with
  max(8, q90(π₀) + 1, k_store).
- **Compat with the adaptive schedule:** the pilot rule is `pilot_next_phi` (core `v3_calib.h:30-46`) and `forced`
  is counted. Golden equal.
- **`load_start`:** `size_cum` equality with WP2 in bits; the neighbour-list checks are complete.
- **Discipline:** everything is under `engine_v4/`, with no hard-coded paths and no large files.
