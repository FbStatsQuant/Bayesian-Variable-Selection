# Final gate review: PR #64 (WP7 O3, leader stores with deferred parallel compaction)

Reviewer: Claude Opus 5.5, 2026-11-17. This review was independent of the author and used no sub-agents. It followed `REVIEW_PR_template.md`, including its Sandbox section:

- Owls only, `nice -n 19`, at most 3 threads, one suite at a time.
- All builds, logs and `TMPDIR` are under `<worktree>/.rc_tmp/`. Nothing was deleted.
- The worktree was checked out detached at the PR head `9fa534e7`.

Own diff: `96137399..61f1091d`. The merge `9fa534e7` of engine `1331b14b` (#63) adds nothing to the engine diff beyond `61f1091d`: `git diff 1331b14b 9fa534e7` equals the O3 commit's diff, up to the placement of one blank context line.

| PR | Head | Verdict | CRITICAL | MAJOR | MINOR |
|---|---|---|---:|---:|---:|
| #64 WP7 O3 (R2) | `9fa534e7` | **ACCEPT-WITH-FIXES** | 0 | 1 | 4 |

**Summary**

- **The code is correct.** I found no determinism, race or allocation defect in the new logic.
- **I verified the leader-store bits at a size where the new path actually runs.** At p = 2·10⁴ with threads 1 and 3, the deferred leaders, the serial leaders and a checkpoint/resume all give one hash. A planted bug in that path changes the hash.
- **The one MAJOR finding is test-only.** The PR's new test never reaches the code the PR adds, so a regression there would pass the suite. Fix the test before merge (MAJOR-1). The MINOR findings are about cost-column semantics, observability and documentation.

---

## 1. What the PR does (verified by reading)

- **Leader defer flag.** `lead0.defer = lead1.defer = top.defer && cfg.leaders_deferred` (`src/island/island_run.h:228`). It is set in the constructor, before `run_island` calls `reserve_staging` (`island_run.h:984-985`). So each leader staging area is reserved at its deferred hard limit `stage_hard = max(8192, 10p)` (`include/v4/island/store.h:171,203-206`).
- **New trigger function `compact_if_due(mid)`** (`island_run.h:350-354`). It applies the same thresholds as the old top-store code to each store separately:
  - `mid`: staged ≥ (limit + hard)/2;
  - pass boundary: staged ≥ limit.
  
  It releases the matching snapshots and calls `compact_parallel(NT)`. It has three call sites, all serial and outside any OpenMP region:
  - after the walk (`island_lm.h:368`);
  - between phase-B waves (`:450`);
  - at the pass boundary (`:454`).
- **Wave size.** The wave is now bounded by the smallest store capacity (`island_lm.h:378-379`).
- **Step boundary.** `sync_ledgers` compacts the leaders with `compact_parallel` when they are deferred (`island_run.h:334-338`).

## 2. Determinism (focus 1)

- **Content and order are unique.** `TopStore::compact_parallel` (`store.h:278-375`) is unchanged code, already reviewed for the top store. Its output is the top-c of the set of offers, with the largest value kept per model. Leader stores use `Order::LEX` (v desc, lex asc). That is a strict total order on distinct models, so both the content and the order of the result are unique:
  - for every thread count, schedule and flush timing;
  - with ties broken lexicographically;
  - with no reduction whose order varies.
- **Thread-dependent parts are never output.** The hash-index slot layout is built by CAS insertion and can depend on the schedule. It is never serialized or hashed: the checkpoint writes `v/hash/off/len/pool` (`island_run.h:542`), `IslandRun::hash()` reads `v/len/pool`, and load rebuilds the index (`publish_loaded`).
- **No races.** Every `compact_if_due` call runs while all workers are idle. `staged()` takes the store mutex. The workers' stale-snapshot drop (`island_lm.h:391-394`) and the phase-B `lead_pass` filter (`:415`) read `gen` and `tau` with relaxed atomics; `tau` only changes the set of dropped offers, which the τ-monotonicity proof makes content-neutral. No new shared writable data appears in a parallel region, so no false sharing that could change results.
- **Calibration replay is unaffected.** Every `round()` is followed by `sync_ledgers()` (`island_run.h:775,781,791`), so at round start nothing is staged, and `RoundSnap` holds the fully compacted leader kept runs (`:282`). `rebuild_prefix` restores them and discards any staged entries (`:697`, `store.h:378-384`), whenever the in-round compactions happened. The failure exit runs `sync_ledgers` again (`:849-850`). The calibration goldens run label-major at threads 3 against core (`test_island_golden.cpp`, the PR39-m5 loop) and pass.

## 3. Allocation (focus 2)

- **The new code allocates nothing in a parallel region.** `compact_if_due` and the `sync_ledgers` changes are serial. `compact_parallel` performs every allocation before its `omp` pragmas: `r(s)`, sort scratch, `dead/drop`, `alive`, `nk` resizes, `segpool`, `index.assign`.
- **Staging capacity is reserved for the deferred limit** (see §1).
- **Residual.** The deferred store's in-pass serial fallback `flush → compact_locked` (`store.h:216`) allocates under the mutex inside the phase-B region. For leaders it was the *normal* path before O3, so O3 strictly reduces it. At p = 2·10⁴ with threads 3, the probe counts 0 leader fallbacks with deferral against 11 + 25 without (§7). See MINOR-3 for the scale argument and observability.

## 4. Deferred logic, final flush, checkpoint/resume (focus 3)

- **Triggers.** The mid trigger after the walk and between waves, and the pass-boundary trigger, mirror the old top-store code exactly. The probe at p = 2·10⁴, threads 3 shows the new path really runs: 12 mid-trigger and 13 pass-boundary leader compactions.
- **Final flush.** There is no separate end-of-island flush. The last `sync_ledgers` flushes every worker buffer and compacts every leader store unconditionally (`island_run.h:334-338`). The I1 check and the result assembly (`:887-888`) read compacted stores.
- **A checkpoint cannot catch a pending compaction.** `save_ckpt` is reached only through `maybe_ckpt`, which runs after the step's `sync_ledgers`, so the leader staging area is always empty at a checkpoint. The checkpoint writes only kept runs (`island_run.h:542`). Calibration islands have no checkpoints at all (`island_run.h:940`). Leaders with checkpoints exist only on test or bench final islands.
- **Measured resume** (p = 2·10⁴, N = 300, `geo:4 1 1`, class A, LM G 64, `V4_LEADERS=1`). In each case I stopped after step 3 at threads 3 (deferred), then resumed:

  | Resume configuration | Hash |
  |---|---|
  | threads 3, deferred | `def7775abdf88726` |
  | threads 1 | `def7775abdf88726` |
  | threads 3, `V4_LEADERS_SERIAL` | `def7775abdf88726` |

  All three equal the uninterrupted run. Log: `.rc_tmp/logs/ckpt.log`.

## 5. Findings

### MAJOR-1: the new test never reaches the O3 path; a planted bug in it still passes

**Where:** `tests/test_island.cpp:1702-1720` (`leader_stores_deferred_compaction_same_bits`, `Fixture F(100, 300, 64)`).

**Evidence.** I instrumented a copy (`.rc_tmp/negA/`, build `.rc_tmp/build_negA/`) with counters in `compact_if_due` and with an env-switched negative control. The control, `V4_NEG_LEAD`, clears a due leader's staging area instead of merging it. Logs: `.rc_tmp/logs/negA.log`, `.rc_tmp/logs/bench_*.log`.

- **The test's own legs never trigger the new code.** In every leg (threads 1/2/3, G 7/16/96, both forms), the counters read **mid = 0 and pass = 0**. Yet each deferred leg logs 1-2 in-pass *serial* leader compactions (`lead_serial_inpass=2/2`).
  - The cause: at p = 300 the leader cap is 6,000, so `stage_hard = max(8192, 3000) = 8192`. That is below `buf_limit = 65536` (`store.h:169-171`). A worker's buffer flushes into the staging area only when it reaches its 65,536-entry limit, so the first flush passes `stage_hard`, and `flush()` compacts serially before any wave or pass-boundary check can see it.
  - What the test does compare: `compact_parallel` at step boundaries (in `sync_ledgers`) against the PM serial reference. That part is useful.
  - Also, `CHECK(r.ks.t_store_compact_lead > 0)` is satisfied by those step-boundary and serial compactions alone.
- **The negative control passes the test.** Discarding every staged leader offer at `compact_if_due` **still PASSES** `leader_stores_deferred_compaction_same_bits`.
- **The same control is caught at p = 2·10⁴.** There it changes the bench hash from `def7775abdf88726` to `20404ae87a1f24a9` (mid = 121, pass = 45). So the code under test matters for the output, but the test cannot see it.
- **No other suite member fills the gap.** `mem_plan_bounds_measured_peak_2e4` runs label-major leaders at p = 2·10⁴, but it checks memory, not bits.
- **Consequence.** A regression in the code this PR adds would pass the suite. Examples: a wrong store in `compact_if_due`, a missing release, a dropped or duplicated stage. Same for future edits to the wave bound.

**Fix (test-only).**
1. Run the comparison where leader `stage_hard > buf_limit`, i.e. leader cap 20p > 131,072, so p ≳ 6.6·10³. For example, use p = 2·10⁴ with small N, `geo:2`, L = 0, Hm = 1. Alternatively, add a test knob that lowers `buf_limit` / `stage_limit` for the leader stores.
2. Assert that the deferred path ran. For example, export per-store counters of mid and pass compactions (and serial fallbacks) in `KernelStats`, and `CHECK(mid + pass > 0)` on the deferred legs.
3. Keep the drop-the-stage negative control as an in-tree test switch, in the style of `test_bound_shrink`.

### MINOR-2: `t_compact_pass` now includes the leader stores, breaking its documented "of which" meaning

**Where:**
- `src/island/island_lm.h:454-455`: `compact_if_due(false); lap(KS.t_compact_pass);`
- `include/v4/island/island.h:183`: `t_compact, t_compact_pass: top store compaction, all paths / of which at pass boundaries`

**Evidence.**
- The pass-boundary lap now times the leaders' compactions too. So on calibration islands `t_compact_pass` can exceed `t_compact`, which stays top-store only (`island_run.h:409`), and the two seconds are counted in both `t_compact_lead` and `t_compact_pass`.
- The leader compactions after the walk and between waves land in `t_phaseB` (laps at `:452`). That was already true for the top store's mid-wave compactions.
- The new INTERFACES §5.1 sentence ("`t_compact` stays the top store's") does not mention this. It also says `t_compact_lead` is "0 on final islands", but final islands with `leaders = true` (tests, bench `V4_LEADERS`) have a nonzero value.

**Fix:** either take a lap between the top and leader compactions in `compact_if_due(false)`, so `t_compact_pass` stays top-only, or redefine it in `island.h:183` and INTERFACES §5.1 as "all stores at pass boundaries". Also change "0 on final islands" to "0 without leader stores".

### MINOR-3: leader in-pass serial fallbacks are invisible, and the "unreachable" argument does not cover buffered offers

**Where:**
- `src/island/island_lm.h:372-375` (comment: "the in-pass serial compaction … is unreachable in label-major")
- `src/island/island_run.h:891` (`store_serial_merges` = top only)
- `tools/bench_island.cpp:194` (the leader line prints only seconds)

**Evidence.**
- **What the wave bound covers.** The bound limits offers *made during a wave* to ≤ 0.1c. The staging area can also receive up to T × 65,535 entries that sit unflushed in worker buffers from earlier waves.
- **Leader numbers at p = 10⁶, T = 96.** The leader c = 2·10⁷, so `stage_hard` = 10⁷ = 0.5c. The worst case is 0.375c (just under the mid trigger) + 0.1c + 6.3·10⁶ (≈ 0.31c) ≈ 0.79c, which is over 0.5c.
- **Top-store numbers.** The same arithmetic pre-exists for the top store (≈ 0.16c of buffers), so the claim was already loose. Halving the capacity for the leaders doubles the buffered share.
- **Effect.** Content is unaffected. A fallback costs a serial compaction under the mutex with allocation inside the phase-B region.
- **No current output counts it.** `lead*.n_serial_merges` reach no output. My counter was the only evidence that the count is 0 at p = 2·10⁴, T = 3.

**Fix:** export the leader serial-fallback count (`KernelStats`, cost row, bench line). Correct the comment, or include the T × buf_limit term in the bound. Check the count on the first NOTS calibration-shaped run at high T.

### MINOR-4: checkpoint payload layout changed under the same magic; the changelog says "execution only"

**Where:**
- `include/v4/island/island.h:193`: `StepCost` 35 → 36 doubles, raw checkpoint rows
- `src/island/island_run.h:446`: `CostMark` gains `t_lead` in `mark_io`
- `island_run.h:132`: magic still `SMCV4CK2`
- `INTERFACES.md:706-711`

**Evidence.**
- **Old checkpoints are refused safely.** A checkpoint written by the v0.1.24 binary is refused because `fingerprint()` includes the binary block (`island_run.h:509`): "belongs to another configuration or binary". So nothing is misparsed.
- **The changelog does not say so.** It says "Execution only" and does not mention that the checkpoint rows changed.
- **Operational risk.** This matters now that the 1M pilot fit is GO: a final island in a `--stop-after-s` resubmission chain (WP5 driver) cannot switch to this binary mid-chain.

**Fix (documentation):** add one clause to the v0.1.25 line. It should say that the §5.1 checkpoint rows (`StepCost`, 36 fields) and the totals changed, and that a chain must finish on the binary that started it (already enforced by the fingerprint).

### MINOR-5: the memory plan uses the deferred leader term even when `leaders_deferred = false`

**Where:**
- `include/v4/island/memory.h:79`: `store_peak_bytes(cl, z.deferred, k)`
- `include/v4/island/island.h:274`: `z.deferred` ignores `cfg.leaders_deferred`

**Evidence.** With `V4_LEADERS_SERIAL` / `leaders_deferred = false`, the leaders compact serially. The serial term is larger than the deferred one, because it adds a stale generation and pool over-reservation. At p = 10⁶, k = 8 it is about 5.0 GB against 4.2 GB per leader store, so the plan under-counts by about 1.6 GB for the two stores. The impact is limited to bench and tests, because production never sets the option.

**Fix:** `add("leaders", 2.0 * store_peak_bytes(cl, z.deferred && cfg.leaders_deferred, k))`. This requires carrying the flag in `MemSizes`, and `plan_from_sizes_equals_plan_island` will check that both paths agree.

## 6. INTERFACES and cost column (focus 5)

- **Changelog order is now consistent.** At engine `1331b14b` the header said **v0.1.23** although the changelog already had a v0.1.24 line (#63 did not bump the header). This PR sets the header to v0.1.25 (`INTERFACES.md:3`), and the changelog runs v0.1.23 → v0.1.24 (`info --meta`) → v0.1.25 (O3).
- **`t_compact_lead` is wired consistently** through:
  - `StepCost` (`island.h:184`) and its static assert of 36 fields;
  - the JSON row (`:208`);
  - `CostMark` and the checkpoint (`island_run.h:400,409,446`);
  - restore (`:452`), with the sum carried in `lead0` and `lead1` zeroed. That is correct for a sum;
  - `KernelStats::t_store_compact_lead` (`:891`);
  - the rows-sum test (`test_island.cpp:1340`).
- **The schema is additive.** `meta.cost` keeps schema `smcbvs4.cost/1` and gains one column. Readers key on names (`p1m_stage_cost.py` uses `.get`), so old readers keep working. `p1m_stage_cost.py` does not report the new column yet (optional).
- **Remaining gaps.** The semantic issues are MINOR-2 and MINOR-4.

## 7. Measured

| Check | Result |
|---|---|
| Quick suite. Command: `tests/run_tests.sh --quick --threads 3 --keep --build-dir .rc_tmp/build`, with `TMPDIR = P1M_TEST_ROOT = .rc_tmp/tmp`. Log: `.rc_tmp/logs/quick.log` | **Exit 0.** 186 C++ test cases, 0 failed, 0 check failures. WP5 driver: 38 tests OK. Competitor harness OK (8 optional packages absent). Install script 9 checks OK. **WP4 golden: 540,419 checks, 0 failures** |
| T3 (`t3_invariance_*`, portable build) | Bit `44a15bfc6fb8d233`, class A `d2df149413596a19`. **Both equal the pinned values** (PR53_61 review), in the suite and in re-runs at `OMP_NUM_THREADS` 1 and 3 |
| Leader tests at `OMP_NUM_THREADS` 1 and 3 (`v4_tests leader`; log `.rc_tmp/logs/leaders_thr.log`) | `leaders_label_major_equal_particle_major` and `leader_stores_deferred_compaction_same_bits` PASS at both (but see MAJOR-1) |
| Bench, p = 2·10⁴, N 300, class A, LM G 64, tile 128, `geo:4 1 1`, `V4_LEADERS=1`, threads 1 and 3 (instrumented build; log `.rc_tmp/logs/bench_probe_2e4.log`) | Deferred and `V4_LEADERS_SERIAL`, at threads 1 and 3: **all `def7775abdf88726`**. Deferred at threads 3: mid 12, pass 13, 0 leader serial fallbacks. Serial: 11/25 fallbacks. Leader compaction 2.21 → 1.15 s, wall 13.58 → 13.22 s. This matches the direction of the author's p = 5·10⁴ numbers |
| Negative control (`V4_NEG_LEAD`; logs `.rc_tmp/logs/negA.log`, `bench_neg_2e4.log`) | p = 300 test: **PASSES** (blind, MAJOR-1). p = 2·10⁴ bench: hash `20404ae87a1f24a9` ≠ `def7775abdf88726` (caught) |
| Checkpoint/resume, stop after step 3 → resume (log `.rc_tmp/logs/ckpt.log`) | 3/3 resumes give `def7775abdf88726` |

The x86-64-v4 build was not re-run for this PR. The change adds no arithmetic, only store compaction timing.

## 8. Contract, scale, discipline

- **Contract:** no format change to island, calib or setup files. `meta.cost` gains one column. The checkpoint rows changed (MINOR-4). `leaders_deferred` is an execution parameter outside the fingerprint, and resume across it is verified above.
- **Scale:** the leader term in the memory plan now uses the deferred peak. `mem_plan_bounds_measured_peak_2e4` passes, including the label-major calibration row with leaders at threads 3. The wave bound for leaders is still `wave_cap / 10 / per_tile`, which stays ≥ 1 tile at p = 10⁶ (2·10⁶ / 32,768). Index arithmetic is 64-bit, as before.
- **Discipline:** only `Scripts/SMC_BVS/engine_v4/` is touched. `git diff --check` is clean, and there are no large files or hard-coded paths. My instrumented copy lives only in `.rc_tmp/negA/`.
