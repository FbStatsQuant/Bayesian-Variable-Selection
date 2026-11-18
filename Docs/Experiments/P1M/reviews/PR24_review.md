# PR #24 review: WP3 slice 2 (parallel compaction, `--mem-budget` admission, compat island)

Reviewer: Opus 5.5 (high), independent of the author. Date: 2026-11-16.
- Branch: `exp/P1M-wp3-island3` @ `2f6b629f`, stacked on #21 (`afa7a0d7`). Reviewed diff: `afa7a0d7..2f6b629f`, 9 files,
  +500/−33.
- Commit structure: `f973fdcd` (slice 2, built on `cd1a7e02`), `9907c4a4` (leaders option, v0.1.7), then a merge of
  `afa7a0d7`.
- Contract: INTERFACES v0.1.7. Design: WP3_DESIGN v0.2 §1.6, §1.7, §6, §7. Spec: ENGINEERING_SPEC §0-v3. Decisions:
  D-7, D-21, D-24.
- Read-only: detached worktree under the tmp folder. Nothing was pushed or commented.

## Verdict: **FIX FIRST**

**What holds:**
- Parallel compaction is deterministic. It equals serial compaction for every thread count and flush order, by argument
  and by test.
- The merge of the #21 fixes is intact: M1 handlers, M2 releases, NaN check.
- The T3 hashes are unchanged. Serial compaction (1 thread) and parallel compaction (2–3 threads) give the same hash.
- The compat golden test compares against unmodified core on core's own stream.
- **Tests: 65 of 65 pass.**

**Two MAJOR findings must be fixed before merge:**
- **P1.** `leaders = true` with the label-major kernel gives silently wrong leader stores. The option is advertised for
  calibration islands, whose leader stores feed V (the D-7 condition).
- **P2.** The admission plan undercounts the island's real peak. Given the true support size it is **−36 % at p = 10⁵**
  (MEASURED). It looks conservative only because k_est = 2·E_π₀|S| + 2 overestimates k (51 vs 6 here). It does **not**
  explain the 31 GB 10⁶ peak.

Counts: CRITICAL 0 · MAJOR 2 · MINOR 6 · nits 4.

---

## Test runs (Owls, Xeon Gold 6148, load ≈ 600 on 80 CPUs, gcc 11.5.0, `nice -n 19`, ≤ 3 threads)
TMPDIR: `/home/fb31/SMC_Engineering_Department/tmp/20261116-review-21-24`, removed after.

1. **`tests/run_tests.sh --build-dir …/b3`**: **65 test cases, 0 failed, 0 check failures**, exit 0. `git_commit` =
   `2f6b629f…`. The PR body says "60 of 60" (stale; nit).
   - T3: bit `44a15bfc6fb8d233`, A `d2df149413596a19`. These are the same as #21, across PM/LM, threads 1–3 (serial
     vs parallel compaction), G and tile.
   - `golden_compat_island_vs_core_serial_stream`, two variants:
     - variant 0: 135,211 draws, store 8,801, leaders 4,400/4,400;
     - variant 1: 155,680 draws, store 6,001, leaders 3,000/3,000.
   - `store_snapshots_released`: max 4 (see m4).
2. **Reviewer check: memory plan vs measured island RSS.** An out-of-tree driver, `chk/memrun.cpp`, linked against the
   PR's libs:
   - it builds the data, then resets VmHWM through `/proc/self/clear_refs`;
   - it runs one class-A label-major island (3 threads, G = 128, grid 0.3/0.7/1, L = 0, Hm = 1, deferred parallel
     compaction);
   - it reports the island-phase increment of VmHWM and evaluates `island_memory` at the store's measured mean |S|.

   MEASURED on Owls:

   | p, N | true mean \|S\| | plan at true k | measured island increment | plan used by admission (k_est) |
   |---|---|---|---|---|
   | 2·10⁴, 500 | 7.03 | 241 MiB | 247 MiB (−2 %) | 283 MiB (k_est 11.6) |
   | **10⁵, 500** | **6.00** | **1,086 MiB** | **1,703 MiB (plan −36 %)** | 2,864 MiB (k_est 51.1) |

   Both runs: `kept_live_max` 4, 0 serial fallbacks, status completed. The 10⁵ run: 30 merges.

## Answers to the focus items

**1. Determinism of parallel compaction: deterministic.**
`compact_parallel` (`store.h:208-295`) produces the unique top-c of {(S, max offered value)}:
- **(a)** `__gnu_parallel::sort` under (hash, |S|, S, v desc). This order is total on content. Equal elements are bitwise
  equal in (v, S), so the sorted sequence is unique up to indistinguishable entries.
- **(b)** The sequential first-per-model scan keeps the maximum value.
- **(c)** Parallel matching against the kept index. Distinct staged models map to distinct kept slots, so the `dead[at]`
  byte writes never collide.
- **(d)** Survivors are sorted under `ord_less`, which is a strict total order on distinct models. The union of alive kept
  entries and survivors has distinct models: a survivor's kept copy is either dropped or marked dead.
- **(e)** The merge path: I checked `split()`.
  - It is the standard lower-bound on the diagonal.
  - The `d − i − 1` index stays in range for i ∈ [max(0, d − nb), min(d, na)).
  - There are no ties, so the A-first and B-first conventions coincide.
  - The output is truncated at `keep = min(cap, na + nb)`, as in serial.
- **(f)** The pool offsets come from a prefix sum over the segments.
- **(g)** The CAS index: the layout depends on timing, but lookups do not. Only `find` reads the index. Checkpoints and the
  output hash use the arrays, not the index.

Other points:
- Workers are idle during the call: it runs on the master thread between waves, at pass boundaries and in `sync_ledgers`,
  under `mu`. Snapshots are released first.
- *When* compaction triggers depends on the schedule (staged counts at wave ends). By the set-function argument of
  §1.3 this cannot change content.
- `store_parallel_compaction_any_flush_order`: 2 × 2 caps × threads 1–4 × 3 permutations, entry by entry equal to the
  serial store and to WP1's `v4::Store`; the index finds every entry. Two limits of this test are in m5.

**2. Memory accounting at p = 10⁶ (does it explain the 31 GB?): no.** See P2.
- I evaluated `island_memory` for the NOTS job 2748105 configuration: p = 10⁶, n = 200, N = 2,500, B = 14, G = 64, tile
  128, serial compaction (pre-#24), k = 6–8.
  - Plan: **9.0 GiB at 48 threads, 9.2–9.9 GiB at 96 threads**.
  - Plus X itself (1.5 GiB, deliberately not counted): **≈ 10.5–11.4 GiB**.
  - Measured (job 2748105): **29.2 GB (48 threads) / 30.9 GB (96 threads)** VmHWM; sacct 32.6 GB.
- About 18–20 GB is outside the plan. The leaks fixed in #21 can plausibly supply it, but this is not shown:
  - stale snapshot generations, ≈ 2.7 GB each at k = 7 (M2);
  - end-of-run copies of the store, +≈ 4.4 GB (m8b);
  - the I1 sort, 0.64 GB (m8a).
- My 10⁵ measurement shows that even after those fixes, the itemised plan misses **≈ 0.6 GiB at c = 4·10⁶**. The gap was
  ≈ 0 at c = 8·10⁵, so it grows with c. Extrapolated linearly to c = 4·10⁷, that is **≈ 6 GiB** (ESTIMATE).
- No post-fix 10⁶ peak has been measured. The 24–32 GB island request is therefore not yet supported by the accounting.

**3. The compat golden test really compares against unmodified core: yes.**
- Core is genuine:
  - `test_island_golden.cpp` includes `core/cpp/v3_engine.h` from `../core/cpp`, compiled unchanged with the v3 flags;
    `core/` is untouched in the diff, and the pinned-reference test passes.
  - It runs `v3::Engine::run_island` with core's own `v3::RngSource` seeded `seed_stream(seed, 9 + r)`. This is exactly
    how `v3_core.cpp:441` seeds final island r.
- Differences from core's production call, none of which changes outputs:
  - `E.cache = nullptr`. With a cache, hits are not offered to the stores (`v3_ledger.h:112`). A hit returns identical bits,
    the stores keep the maximum per model, and the HPM keeps the first score. Only the `fresh` counters change, and those
    are on the OD-3 exclusion list.
  - A fresh `Ledger` per island, without `ingest_tables`. This matches v4's per-island store; inherited and table models
    belong to WP4.
  - Tier 0.
- The test compares every output in bits (RB, `rb_round`, PIP included), HPM and provenance, counters, store, both leader
  stores, and the stream position.
- Compat resume after steps 0/3/6 matches the uninterrupted compat run, with the stream count restored. Non-serial
  configurations are refused.
- A gap: neither variant reaches the Gibbs cap or a scorer fallback route (m6).

---

## Findings

### MAJOR

**P1. `leaders = true` with the label-major kernel silently builds wrong leader stores.**
- Where: `island_impl.h:539` (the phase-B `L.scored(...)` call has no `lg0` argument), `store.h:128`, `store.h` `scored()`
  (`if (lead0) {…}`), `island_impl.h:164`, `run_island` checks.
- Evidence:
  - In phase B, each Gibbs flip is offered with the default `lg0 = NaN`. `lead0->offer` drops it and sets `nan_offered`,
    a flag that is never checked for the leader stores. So lead0 receives **no** flip events from the label-major kernel.
  - Phase-B offers are also gated by the top store's shortcut `F >= top.tau || F > island_best || F >= hpm.F`. lead1 (cap
    20p, LEX order, its own cut-off) therefore misses every flip below the top store's τ that it would have kept.
  - Only the PM path (`:283`) passes `lg0`.
  - `run_island` refuses `leaders` only indirectly, through compat (PM, 1 thread). `leaders` + LM, the class-A
    production kernel, runs without complaint.
- Impact:
  - `island.h:46` names "calibration islands" as the intended user.
  - D-7 is SAFE-TO-DROP only "on the condition that calibration keeps feeding its leader stores into V". A calibration
    island run label-major with this option would feed V from incomplete leader stores, with no error.
  - The leader stores are also absent from the memory plan: at 10⁶, 2 × 2·10⁷ entries ≈ 2.2 GB plus their serial
    compaction peaks.
- Fix, either of:
  - (a) Refuse `leaders` unless the kernel is particle-major (`invalid_input`), and record that calibration leader stores
    need the PM path.
  - (b) Implement them in phase B: compute lg0 for flips when `leaders` is set, offer to lead0/lead1 outside the top-store
    shortcut (or extend the shortcut with the leader cut-offs), and check the leaders' `nan_offered`.

  In both cases, add the leader stores to `island_memory` and add a test with leaders under LM = leaders under PM.

**P2. The `--mem-budget` plan is not an upper bound of the island's memory. Its apparent conservatism comes from k_est only.**
- Where: `include/v4/island/memory.h:31-52`; `run_island` (k_est = max(8, 2·E_π₀|S| + 2)); `over_budget`.
- Evidence (MEASURED, test run 2):
  - At p = 10⁵, the plan evaluated at the true mean stored size (6.00) is 1,086 MiB, but the island used 1,703 MiB above
    the data baseline.
  - The plan the admission actually used (2,864 MiB) covers that only because the stand-in π₀ has a mean size of 24.5,
    giving k_est = 51.
  - With a production π₀ concentrated on small models, k_est → 8 and the plan would understate the peak.
- Components the formula misses or underestimates, all visible in the code:
  - (i) The `__gnu_parallel::sort` multiway mergesort allocates a temporary copy of the sequence: +32 B per staged
    reference, for both sorts. The formula counts refs + flags = 33 B per staged entry, not 65.
  - (ii) Staging `StoreBuffer` vectors grow by `push_back` doubling. They keep their capacity after `clear()`, and they hold
    old and new buffers during a reallocation. Capacity is up to 2× the s·e term, transiently 3×. The deferred limit is
    c/2, so this term doubled with this PR.
  - (iii) The serial path (`compact_locked`, also the in-pass fallback) reserves `K.pool + stage.pool` for the new pool
    and keeps workers' snapshots alive (no `release_snapshots()` before a flush-triggered fallback). Its peak can exceed
    "2 kept runs" (m3).
  - (iv) Leader stores (P1).
  - (v) X, z, diag(G), neighbours and setup tables are excluded by design (`memory.h:19`). If the CLI passes the task's
    memory request as `--mem-budget`, the 1.6 GB of X at 10⁶ alone is unbudgeted. Nothing in the code or in INTERFACES
    says who subtracts it.
  - (vi) There are smaller unbounded items: `res.rb_round` is Hm × p × 8, and the result copies of the leader stores.
- Impact:
  - The admission is the planned defence against OOM at 10⁶, where the per-item error scales with c (≈ 0 at c = 8·10⁵,
    0.6 GiB at 4·10⁶, ≈ 6 GiB extrapolated at 4·10⁷).
  - An OOM kill is not a deterministic `resource_limit`: n1 of the #21 re-check, `bad_alloc` in a region → abort.
  - Focus answer: the plan (≈ 11 GiB with X) does not explain the measured 29–31 GB.
- Fix:
  - (1) Add the missing terms: the sort temporaries (64 B per staged entry), staging at the next power of two × 1.5 for
    reallocation, the serial-fallback peak including one snapshot generation per worker (or call `release_snapshots()`
    before a flush-triggered fallback; workers are then mid-pass, so this is only a hint), the leader stores, and an
    explicit `inputs` term (X + tables) or a documented "budget minus inputs" rule in INTERFACES §7 / the CLI.
  - (2) Base the plan on an upper bound of the stored mean |S| that does not rely on the π₀ stand-in, for example K-capped
    or calibration-measured, and keep the step-boundary re-check.
  - (3) Add a validation test: `island_memory(true k) ≥` measured VmHWM increment for a 10⁴–10⁵ island (Owls), as in
    `chk/memrun.cpp`.
  - (4) Before the 24–32 GB request is fixed, measure one post-#21/#24 10⁶ island on SPR (G = 64 and 256, 96 threads) and
    record plan vs MaxRSS.

### MINOR

**m1. The step-boundary refusal is untested, and its file content is undefined.**
- `over_budget` (`island_impl.h:636-645`, called at `:884`) is never reached in a test. The test budget is always at or
  above the admission plan with k ≥ k_est.
- When it fires, `res.status = 3`. The store is then moved into the result (`status != 2`) and written to island_r.bin
  (`top_*` unconditional), while `numerical_failure` writes none.
- Fix: decide per INTERFACES whether a `resource_limit` island carries its store; WP4 must not merge it. Add a test that
  forces it, for example by injecting a k_est below the true k.

**m2. The admission depends on the thread count.**
- `worker_bufs`, `products` and the deferred staging size (c/2 for threads > 1, c/4 for 1 thread) all depend on threads.
  A resume with a different thread count (allowed by checkpoints) can therefore turn into a refusal, and G = 0 picks a
  thread-dependent G.
- The output does not change (G is an execution parameter), so this is acceptable. State it in WP3_DESIGN §1.6, and say
  that a refusal is reproducible only for the same thread count.

**m3. The particle-major kernel with more than one thread now defers compaction to c/2 with no boundary compactions in the round.**
- `defer = parallel && NT > 1` (`island_impl.h:169`) also applies to PM. PM has no waves or passes, so every in-round
  compaction is the serial fallback at c/2.
- That fallback runs while other workers hold snapshots, so the "≤ 2 kept runs" claim of `memory.h:15` and WP3_DESIGN §1.7
  does not hold for it.
- PM is ≤ 10⁴ (D-21), so the impact is small. Fix: `defer` only for the label-major kernel, or call `release_snapshots()` in
  the PM round at particle boundaries.

**m4. `kept_live` counts empty `Kept` objects, so the M2 test no longer measures what it says.**
- Every `TopStore` default-constructs a `Kept`, including the unused `lead0`/`lead1` members, and `init()` makes a
  transient fourth. The counter therefore reaches 4 at construction (test: max 4; my runs: 4).
- `store_snapshots_released` asserts ≤ 4, so its headroom is consumed by artifacts. It would still fail on one stale
  generation, but the printed "kept runs alive" is misleading.
- Fix: count only kept runs with entries, or count per store. Assert ≤ 2 for the top store.

**m5. Parallel-compaction test limits.**
- The test pushes offers straight into `StoreBuffer`s, bypassing `offer()`. Its `dup_filter` on/off variation is
  therefore vacuous.
- `stage_hard = 2³⁰` excludes the serial fallback interleaved with parallel compactions.
- The island T3 covers both indirectly. Add one case with `offer()` (filter active, stale snapshots) and a small
  `stage_hard`.

**m6. The compat golden test covers no cap and no fallback route.**
- Both variants have K = n/2 ≥ 40 and small supports, and no scorer fallback (pivot / QR route) is exercised under compat.
- Fix: add a third variant with small n (as in `gibbs_cap_island`, K ≈ 6) and one with near-collinear columns.

### Nits
- PR description:
  - "60 of 60" should read 65 of 65.
  - "island_r.bin mode compat with `lead0_*`/`lead1_*`" contradicts `9907c4a4`. The code writes no leader stores, as it
    should.
- The merge commit `2f6b629f` says "Merge branch 'exp/P1M-wp3-island'" but merges `afa7a0d7`, the island2 head.
- The leaders result is copied (`res.lead0_v = lead0.k->v`, `:907-909`), while the top store is moved (#21 m8b).
- `rb_d.assign(p, 0.0)` is allocated in non-compat runs (8 MB at 10⁶).

## Merge of the #21 fixes (regression check)
Slice 2 was written on `cd1a7e02` and merged with `afa7a0d7`. In `2f6b629f` I checked each of the following:
- all M1 handlers (`island_impl.h:276, 294, 489, 491, 565, 819`) and `throw_if_failed` after LM groups, PM rounds and the
  initial draws;
- the M2 tile-start release (`:509`), the flush release (`store.h:146`), and `release_snapshots()` in `sync_ledgers` and
  before every boundary compaction;
- the NaN check in `sync_ledgers`;
- m3 statuses (status 3 maps to `resource_limit` in `to_record` and in the file);
- m8b moves.

The fingerprint adds `compat` and `leaders`. The checkpoint adds the xoshiro state, the count and the double RB. The T3 and
golden hashes are unchanged.

## Discipline
- All changes are under `Scripts/SMC_BVS/engine_v4/`, and `core/` is untouched.
- No hard-coded paths, no large files.
- Measured numbers in the PR are labelled. The "conservative" claim for the 10⁵ plan should say that it rests on k_est.
