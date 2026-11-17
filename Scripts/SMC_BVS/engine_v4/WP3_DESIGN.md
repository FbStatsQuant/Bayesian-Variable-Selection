# WP3_DESIGN — the island: stores, addressed sampling, label-major round, restart

**v0.7, 2026-11-16, WP3 builder (Opus 5.5). Status: PROVISIONAL.** v0.7 records the built calibration roles (§1.11); v0.6 added §1.11 (calibration islands, agreed with WP4); v0.5 added §1.10 (review PR26); v0.2 added §1.7 (parallel compaction, waves, snapshot filter), implements §1.6 (admission) and §6 (compat), and records the manager's §5 decisions. Branch `exp/P1M-wp3-island`
(stacked on WP1's PR #11). Inputs: ENGINEERING_SPEC §0-v2, §3, §6; INTERFACES v0.1.3 (v0.1.5 announced: RNG domain and
event key); Sol EXP-CP1 review §F2, §F4, §F5 (T3, T6); manager directives of 11-15 (D-21 scope cut, G ≤ 256, mem budget).
Code references: `include/v4/island/*.h`, `src/island/island_impl.h`, `tests/test_island*.cpp`. Every number below
is labelled MEASURED (Owls, command given) or ESTIMATE.

**What exists and passes today** (Owls, gcc 11.5, 3 threads, `v4_tests`: 41 cases, 0 failures, in the default build
and in an `x86-64-v4` build):
- particle-major island, bit form, **bit-identical to `core/` `v3::Engine::run_island`** (core compiled unchanged, fed the
  same addressed uniforms through an adapter): log Ẑ, stage table, moves, distinct counts, init hash, HPM + provenance,
  island_best, every logical counter, the top store; RB/PIP to 1e-12 (declared fixed-point reduction, §3.6);
- label-major island in bit form and class A, identical output hash to the particle-major island of the same arithmetic
  for threads 1–3, G ∈ {1, 7, 16, 48}, tiles 64–256 (T3); restart from checkpoints after 6 different steps with changed
  threads/G/kernel (T6); flip kernels 0 mismatches of 16,000 (bit) / ≤ 7.8e-16 relative (class A vs bit).

Under D-21 the bit-form label-major kernel is **not part of the deliverable**: T runs particle-major. The code exists
and is tested; §5 Q1 asks whether to keep it as a test-only path or delete it.

---

## 1. Deterministic stores under threads

### 1.1 Data structures (`include/v4/island/store.h`)
| object | owner | content | bound |
|---|---|---|---|
| `TopStore` (island) | one per island process | kept run: sorted arrays `v, hash, off, len` + `pool` (HPM order, value F); hash index (open addressing, u32 slot = entry+1); staging run (`StoreBuffer`); atomic `tau` | kept ≤ c = 40p + 1; staging ≤ max(c/4, 4096); index 2c…4c slots |
| `StoreBuffer` (offer buffer) | one per worker thread | appended (v, hash, len, off) + pool | ≤ `buf_limit` = 65,536 entries (INTERFACES v0.1.2) |
| `ThreadLedger` (tally) | one per worker thread | logical[N_PHASE][N_MECH], island_best, HPM candidate (S, F, log m, EventKey, phase, mech), MoveStats, its `StoreBuffer` | O(K + buf_limit) |
| island `master` tally | one per island | the absorbed tallies | O(K) |

### 1.2 Algorithm
- **offer(v, S, h)** (worker, hot path): `if v < tau: drop` (relaxed atomic load; ties kept); else append to the worker's
  buffer; if the buffer holds `buf_limit` entries → **flush**.
- **flush(buffer)**: take the island mutex; append the buffer to the staging run; clear the buffer; if staging ≥
  `stage_limit` → **compact** (still under the mutex).
- **compact()**: (1) sort staging by (hash, |S|, S, v desc) and keep the first entry of each model (its largest value);
  (2) look each one up in the kept run through the hash index: if the kept copy has a value ≥ the staged one, drop the
  staged one, else mark the kept copy dead (class A only: one model can carry two path values, §3.7); (3) sort the
  survivors under the store order; (4) linear merge of kept (skipping dead) and survivors, stop at c; (5) rebuild pool
  and index; (6) `tau ← v[c−1]` if c entries are kept, else −∞ (release store). Cost O(c + s log s).
- **absorb protocol** (INTERFACES §4.2 / §7(4)): at every step boundary (after init, after every bridge stage, every
  burn-in and measured round) and before any read or checkpoint, the island flushes each thread's buffer and merges its
  tally **in thread-index order**, then calls compact(). The kernels run only between step boundaries, so the absorb
  is single-threaded.

### 1.3 Why the content is deterministic (independent of threads, schedule, flush timing, merge order, G, tiles)
Define Ω = the multiset of (model, value) offers of the step so far. Claim: after compact(), kept = top-c (under the
strict store order) of {(S, max value of S in Ω)}. Proof sketch:
1. Without drops, compact() computes exactly that set: dedupe-by-max then truncation commute with union
   (top_c(top_c(A) ∪ B) = top_c(A ∪ B) for a strict total order on distinct models, and max is associative).
2. **Drops never change it.** A drop at time t has v < tau_t, where tau_t = the value of the c-th of c distinct kept
   models at t. Values per model only grow, and kept models only get replaced by better ones, so the final c-th value
   is ≥ tau_t > v. If S ends in the final top-c its final value ≥ tau_t > v, so v was not its maximum; if S does not,
   the offer is irrelevant. Equal values (v = tau_t) are never dropped because the tie order (|S|, lex) may admit them.
3. `tau` is read stale by other threads: a stale tau is ≤ the current one, so a stale read only drops less.
Tally merge: counters by sum, island_best by max, HPM by (F desc, |S| asc, lex asc, EventKey asc) — a strict total
order on events, so the max is order-free; for one model the smallest EventKey wins (= core's "first score" rule).

### 1.4 The one-worker-supplies-all-winners case (Sol F2)
Nothing in the design partitions capacity by worker: buffers are bounded only in **entries in flight**, and a full
buffer is flushed into the single island store. If worker 0 offers all c winners and the others only losers, worker 0
flushes ⌈c/65,536⌉ times; content = top-c. Test (to add, `store_one_worker_all_winners`): 3 threads, c = 10⁵; thread 0
offers the c best of 3c models, threads 1–2 offer the rest interleaved; compare with WP1's `v4::Store` reference and
with a serial run (both orders). Existing tests: `store_order_free_multithread` (caps 1…10⁵, buffer limits 1/37/10⁵,
1 and 3 threads, permuted order, value ties, two-value models) and `store_equals_wp1_reference_store`.

### 1.5 Peak-live memory of the store path (ESTIMATE; formula exact in entries)
Entry = 8 v + 8 hash + 8 off + 2 len + 4k pool bytes = 26 + 4k B. Let c = 40p + 1, s = stage_limit = c/4, T = threads.
- kept run c entries; during compaction a new kept run (≤ c) + staged refs (s × 32 B) + dead flags (c B) + index
  (≤ 4c × 4 B): **peak ≈ 2c entries + 1.25c × 32 B + 16c B** plus staging s entries.
- per worker: buf_limit entries (65,536 × (26 + 4k) B ≈ 3.5 MB at k = 7, 28 MB at k = K = 100).
At p = 10⁶, k = 7 (c = 4·10⁷): kept 2.2 GB, peak ≈ 2.2 + 2.2 + 0.55 (staging) + 1.6 (refs) + 0.64 (index) ≈ **7.2 GB**,
workers 48 × 3.5 MB = 0.17 GB. At the admission bound k = K = 100 the per-entry size is 426 B: c × 426 B = 17 GB kept —
**the store cannot be admitted at K-sized supports at 1M**; the admission check (§1.6) uses the pool's actual size, so
it refuses on growth with a named reason rather than OOM. (Q4 asks for the policy.)
MEASURED (Owls, `v4_bench_island store 4000001 3 2e7`): fill 2.1 µs per accepted new model, mixed traffic (90 % below
tau, 10 % duplicates of kept models) 213 ns per offer — the duplicates dominate: each costs a compaction share. At
p = 10⁴ islands, 5 % of consumed flip events pass tau (MEASURED, 53.7 M of 1.05·10⁹). Lever (Q5): a worker-side
duplicate filter against an immutable snapshot of the index.

**v0.1.1 (review PR21 M2).** Snapshot lifetime: a worker drops its snapshot when it flushes, at the start of every
phase-B tile if a newer kept run was published, and every worker drops it at every step boundary. A worker therefore
holds at most one stale generation, and only while it works through one tile. Kept runs alive at once ≤ 2 (current, and
the new one during a compaction) + the stale generations held mid-tile; a compaction is triggered by c/4 staged offers,
far more than all workers emit during one tile at production sizes (T · tile · G ≪ c/4 at 10⁶), so in practice ≤ 3.
MEASURED: the counter `kept_live_max` (every `Kept` construction/destruction) reads 3 in the test island with 12
compactions (cap 2,000) and 2 in the p = 10⁵ islands below; all kept runs are released after the island.
MEASURED (Owls, 3 threads, `v4_bench_island island 100000 2500 3 A lm G 128 steps:0.3,0.7,1 0 1`, class A, n = 200,
c = 4·10⁶, mean stored |S| = 6.0): kept run 200 MB + index 34 MB; **peak RSS 2.20 GB at G = 256, 1.82 GB at G = 64**
(includes X 160 MB, tiled X 160 MB, rows 2Gp·8, orders 2Gm·4, tables, store compaction peak); same output hash.
Corrected peak (reviewer): ≈ 6.7–7.1 GB at 10⁶, k = 7 for the compaction itself (old kept 2.7 + new kept 2.2 +
over-reserved pool 0.3 + new index 0.5 + staging 0.7–1.1 + refs 0.3) + one stale generation (2.7) ≈ 9.4–9.8 GB.

### 1.6 `--mem-budget` admission (implemented v0.2: `include/v4/island/memory.h`, `IslandConfig::mem_budget`, G = 0 = auto)
`island_memory(cfg, p, n, K)` sums, before any allocation: X tiles (n·p·8, a second tiled copy), store peak (§1.5 with
k = the running mean support size, re-checked at every compaction with the real pool size), staging, index, worker
buffers (T × buf_limit × (26 + 4k)), RB accumulators (16 B × p × 2: current round and total; particle-major: + T × 16 p),
group buffers (G × m × 4 B × 2 for orders + inverses; nsup × p × 16 B for the per-support score and odds rows;
|A| × n × 8 gathered columns; T × |A| × tile × 8 products), particles (N × (k × 4 + 48) × 2), checkpoint serialisation
(the byte image ≈ store + particles + 16 p, written from a buffer: Q6). Refusal: status `resource_limit`, reason
`"mem_budget: <component> <bytes> > budget"`, deterministic (a function of the configuration and of the run's own
state at a step boundary). Config checks: **G ≤ 256** (manager item 2), tile multiple of 64, N ≥ 1, grid strictly
increasing from 0 to 1, B ≥ 0.

### 1.7 v0.2: duplicate filter, parallel compaction, waves (implemented)
- **Exact snapshot filter.** The kept run is immutable once published (`Kept`: arrays + hash index); compaction builds
  a new one and publishes it under a generation counter. A worker drops an offer whose model is in its snapshot with
  a value ≥ the offer's: exact even with a stale snapshot (the snapshot holds only offered values; values per model only
  grow). MEASURED (Owls, 3 threads, p = 10⁴): buffered offers ÷ 3.6, compactions 87 → 27, identical output hash.
- **Deferred parallel compaction.** Workers only append to the staging area during a pass. Compaction runs where all
  threads are free: after a wave of phase-B tiles (staging ≥ 0.375c), at the pass boundary (≥ c/4) and at every step
  boundary; a chunked parallel sort with its scratch allocated before the region (`psort_noalloc`, §1.10), parallel kept-index matching, merge-path parallel merge truncated at c, prefix-sum
  pool offsets, CAS-built index. The result is unique (strict total order, distinct models), so it equals the serial
  compaction for every thread count and flush order (test `store_parallel_compaction_any_flush_order`; T3 compares the
  serial path, 1 thread, with the parallel path, 2–3 threads). A serial in-pass compaction remains only as a fallback at
  the hard limit c/2. Workers release their snapshots before every boundary compaction, so at most two kept runs live:
  peak ≈ 2c + c/2 entries (§1.6 formula).
- MEASURED (Owls, 3 threads, p = 10⁵, N = 500, transient 3 stages + 1 measured round): compaction 33.8 s serial →
  21.9 s parallel at pass ends (9 serial fallbacks) → 21.8 s with waves (0 fallbacks); island 108.7 → 93.5–100 s
  (machine load 59–224 during the runs). The gain grows with the thread count.

### 1.8 v0.3 (review PR24): the plan is an upper bound; leaders in label-major
- **Plan** (`memory.h`, terms listed there): inputs (X, z, diag(G); the caller adds the setup/calib sections through
  `inputs_bytes`: **--mem-budget is the task's memory**, X is inside the plan; INTERFACES §7 note requested from WP1),
  tiled X, the store (old + new kept run, pool over-reservation, staging at pow2 × 1.5, sort refs + the parallel
  sort's scratch copy, flags, alive list, two indexes, one stale snapshot generation), the leader stores,
  worker buffers for every store, RB incl. `rb_round` and compat, group buffers, support caches (k_q = min(K, 3k)),
  particles and terminal supports, checkpoint buffers. Admission uses the calibration-measured mean stored |S|
  (`k_store`) when given, else the π₀ estimate; the step-boundary re-check uses the store's actual pool (exact) and
  refuses deterministically (resource_limit, no store reported, GUARD-W). The plan depends on the thread count, so a
  refusal is reproducible for the same thread count (G and threads never change outputs).
- MEASURED (Owls, 3 threads, N = 500, 3 stages + 1 round, VmHWM increment after clear_refs vs the plan without inputs,
  at the true stored mean |S|): p = 2·10⁴: 231 / 314 MiB (G 64), 219 / 422 (G 256), with leaders 346 / 534 and
  317 / 643 — the bound holds in all four; p = 10⁵: see the PR. Plan at 10⁶, k = 7, G = 64, 96 threads: ≈ 17.5 GiB
  (store 12.3, inputs 1.5, x tiles 1.5, rows 1.0, orders 0.5, worker buffers 0.5) — to be checked against the post-fix
  10⁶ peak of the NOTS lever batch.
- **Leaders under label-major** (P1, option (b)): phase B computes log γ₀ of each consumed flip (the same block sum)
  and offers to the leader stores under their own cut-offs (not the top store's shortcut); leader snapshots are released
  like the top store's; NaN offers are refused. Test: leaders label-major = particle-major in both forms (the compat
  golden ties particle-major to core). Cost: one composite sum per consumed (support, label) pair, only when `leaders`.
- **Fallback routes under compat** (m6): with H = (n+1)G_S + I and A = G_S + I both positive definite and
  Q ≥ y'y/(n+1) > 1e-8 y'y, the refactor, QR and non-negative-Q routes cannot be reached in exact arithmetic for
  finite data; near-collinear columns do not trigger them. The compat golden adds a cap variant (n = 12, K = 6) instead.

### 1.9 v0.4 (lever batch 2748756): the 10⁶ peak, and L5
- **Missing plan term at 10⁶ (P2 again)**: round 1 stores π₀-sized models before the particles shrink (stand-in π₀ at
  10⁶: mean size 56), so the store's peak is reached with k ≈ 56–62, not the final 6. The plan's k is now
  max(8, q90(π₀ size) + 1, k_store) — exact from the setup's size masses — and three transients are removed from the
  code instead of being budgeted: score rows sized once at G·p (growing re-zero-filled and reallocated them), the
  staging area reserved once at its hard limit, and phase-B waves bounded to 0.1 c offers so the in-pass serial
  compaction (stale snapshots, pool over-reservation) cannot occur in label-major. MEASURED plan vs the lever batch
  (setup inputs measured in-process, 2.24 GB beyond X): **G = 64: plan 37.7 GiB ≥ measured 23.7 GiB; G = 256: 43.8 ≥ 32.0
  GiB** (measured at efc0dfd0, before these fixes). At 2·10⁴ / 10⁵ the bound holds in all eight configurations.
- **L5, per-pass overheads.** Per-call costs (MEASURED, Owls, 1 thread, `v4_bench_island overheads p`), old → new, all
  exact (same uniforms, same results; T3 hashes and both golden tests unchanged):
  π₀ draw (every I step and initial draw) 59.2 → 4.0 ms at 10⁶ (8.99 → 0.42 ms at 10⁵): the draw checks 8 blocks at once
  against an r-major table of P(k_b = 0 | r) with 8-lane Philox over the block slots; round order (Fisher–Yates) 41.8 →
  21.0 ns per label at 10⁶ (8-lane Philox + prefetched swap targets); inverse 4.9 → 3.4 ns; score rows no longer
  re-zero-filled (1.8 s per group at 10⁶, G = 256); apply in parallel.
  ESTIMATE for the late 10⁶ round of job 2748756 (G = 256, 29.1 s): walk −3.3 s, build −2.2 s, orders −1.4 s,
  apply −0.5 s → ≈ 21.7 s, i.e. **≈ 215 ns·CPU per pair (≈ 1.07× the plan), from 287**. To be measured on SPR.
  Not built yet: dropping the stored round order (only the inverse is needed if phase A records the label of the
  first change) halves the order arrays and allows G = 512 within 2 GB of orders (+4 GB of score rows).
  Production note: the r-major table is (K + 1)·J·8 bytes (≈ 200 MB at 10⁶) built from WP2's tables; with WP2's
  setup it belongs in the plan (or in setup.bin).

### 1.10 v0.5 (review PR26 and PR24 r1/r2)
- **k_store is required at p ≥ 10⁵** (`run_island`: invalid_input without `k_store`; the island CLI passes calib.bin's
  measured mean stored |S|). Only tests and the bench may set `k_store_optional`. The plan's k stays
  max(8, q90(π₀ size) + 1, k_store): round 1 stores π₀-sized models, so k_store alone (≈ 8 at 10⁶) cannot bound round 1
  when π₀ is large (stand-in π₀ at 10⁶: q90 + 1 = 62). MEASURED (`V4_K_STORE=8 v4_bench_island plan 1000000 2500 96
  64,256`, Owls, setup inputs 2.43 GB measured in-process): **G = 64: 37.86 GiB (40.7 GB) ≥ 25.4 GB measured; G = 256:
  44.00 GiB (47.2 GB) ≥ 34.3 GB measured** (lever batch 2748756), so G = 256 is admitted under a 60 GiB budget. With a
  real setup whose π₀ is small, the plan falls toward the k_store value.
- **OOM in the parallel compaction** (r2): `__gnu_parallel::sort` allocated inside its own OpenMP region, where a
  `std::bad_alloc` cannot be caught. `psort_noalloc` sorts T chunks with `std::sort` and merges pairwise with
  `std::merge` into a scratch vector allocated before any region; both orders are total on content, so the result is
  the same for every thread count (tested against `std::sort` at 1, 2, 3, 5, 8 threads). An allocation failure now
  reaches `run()` and gives resource_limit (test `oom_in_parallel_compaction_is_resource_limit`).
- **Products block by ISA** (B2): `products_block = 0` (auto) is 4 when the island translation unit has AVX-512 and 1
  otherwise. MEASURED by the reviewer (Owls, `island 20000 300 … geo:4 1 1`): block 4 = −27 % at x86-64-v4 (44 → 32 ns
  per pair), +17 % at x86-64-v2 (190 → 223 ns per pair); same bits in both.
- **Bench and NOTS scripts**: `V4_K_STORE`; the bench exits non-zero when any run is refused or does not complete; the
  scripts refuse without TMPDIR or outside the department folders (`tools/nots_guard.sh`), keep logs in
  `<build>/logs`; socket mode waits for both islands, prints both logs, and requires exit 0, `status=0` and two
  distinct non-empty hashes.

### 1.10b m3 (L5 SPR batch 2749328): the phase-B / compaction regression
- **Cause.** The r2 fix (PR #26) replaced `__gnu_parallel::sort` in the parallel compaction with `psort_noalloc`, which
  merged the sorted chunks pairwise with one task per pair. Round r of the merge therefore ran on threads / 2^(r+1)
  tasks, and the last round on one: the merge's critical path was about 2n element moves. On SPR (96 threads) that made
  the compaction's two sorts nearly serial.
  - Compaction runs at pass and step boundaries and between phase-B waves, so it showed up in both phase B and compaction
    time: 38.5 → 57.1 s and 65 → 88 s per island.
  - The compaction count is unchanged (33 in every build below), so neither the wave cap nor the reserved staging is
    the cause.
- **Fix.**
  - Each merge round cuts every pair's output into equal segments at merge-path splits. Each segment is one stable
    `std::merge` of the two sub-ranges that produce it, so the result is the same sequence as before, with all threads
    busy in every round and no allocation inside a region.
  - The merge's critical path becomes about (n / threads) · log2(threads): roughly 27× shorter at 96 threads (ESTIMATE).
  - The `[round]` lines now report the number of compactions and the sort seconds.
- **MEASURED, Owls, 3 threads.**
  - The sort alone (`v4_bench_island sort`, best of 3; all three variants give the same sequence):

    | staged refs | pairwise | merge-path | `__gnu_parallel` |
    |---|---|---|---|
    | 1.5 M | 0.115 s | 0.091 s | 0.085 s |
    | 6 M | 0.590 s | 0.419 s | 0.453 s |

  - The island (p = 10⁵, N = 500, G = 256, `steps:1`, L = 2, Hm = 1): the same output hash `bab293252e9ebe57` in all
    three builds.

    | build | compaction (33 in each) | phase B |
    |---|---|---|
    | pre-L5 (`32b11a91`) | 15.56 s | 19.00 s |
    | engine (`4c238a32`) | 19.05 s | 22.17 s |
    | m3 | 16.38 s | 19.97 s |

    In the m3 build the sorts are 4.3 s of the 16.4 s of compaction.
  - 3 threads show only the first rounds of the problem; the SPR batch measures the 96-thread gain.

### 1.11 v0.6 (agreed with WP4, 2026-11-16): calibration islands (pilot, diagnostic)
This is the API that WP4's `calib::IslandRunner` calls. It is built after the PR #26 re-check. Core reference:
`core/cpp/v3_core.cpp:620-692` (`cpp_cal_pilot`, `cpp_cal_diag`) and `cpp/v3_engine.h:269-372` (`run_island_s` with
`phase_override`).
- **Config.**
  - `IslandConfig::role` is `Final`, `Pilot` or `Diag`. `tier` = e, the new `iter` = k (0 for the pilot, k for rebuild
    k), and `island` = 0 for the pilot, 1…4 for the diagnostic islands.
  - Addresses use role R_PILOT / R_DIAG with tier e, iter k and island r (INTERFACES §3). Islands of different rebuilds
    get fresh addresses.
  - The pilot uses the adaptive schedule (core's pilot rule, `adaptive_H` = H, `adaptive_Te`). The diagnostic islands
    use WP4's fixed grid.
  - `leaders` is on for calibration roles (they feed V). Final islands never carry leaders (D-7).
- **Events.**
  - Every event is labelled PH_PILOT or PH_DIAG (core's `phase_override`).
  - EventKey = (CALIB, e, k, r, xph, stage, round, particle, position, sub). MEASURED rounds are numbered L + h
    (INTERFACES v0.1.5 §4.2).
- **Output.**
  - IslandRun → `to_record()` → `v4::IslandResult` with its own Ledger: top store, lead0 / lead1, HPM + key,
    island_best and logical counts.
  - Ledger configuration: islands = 4, leaders = true, caps 40p + 1 / 20p / 20p (`Ledger::merge` refuses a mismatch).
    The pilot (unit 0) has no island_best of its own.
  - The island ledger starts empty: no tables and no inherited models.
  - WP4 owns the calibration ledger and merges island ledgers with `Ledger::merge`, which is order-free.
  - WP4 also resets island_best before each rebuild's four diagnostic islands (`v3_core.cpp:662`) and runs every local
    search (CALIB, e, k, UNIT_LOCAL). There is no local search inside the island.
  - Also returned: `forced` (forced pilot steps), the schedule used, stages, logZ, pip, init_hash, and the stream
    positions (start, end) in compat.
- **Admission (WP4's N-1 rule, `IslandSpec`).**
  - `mem_budget` is the whole calibration task's budget, passed unchanged to every island.
  - `resident_bytes` is the calibration process's own state: the calibration ledger at its staging peak and the
    inherited export. It excludes X / z / diag(G) and the setup inputs, which the island's plan counts itself.
  - The runner adds `resident_bytes` to the plan's caller-supplied inputs term, so an island is admitted iff
    resident_bytes + plan ≤ mem_budget. No byte is counted twice.
  - `calib_run` passes resident = ledger + export (WP4's plan without its inputs term) and budget = the task's budget.
  - Test `calibration_admission_n1_rule`: refused at plan − 1, admitted at plan.
- **Stops.**
  - resource_limit returns core's partial output: the schedule so far, `forced`, the stages so far, logZ so far and
    `partial = true`.
  - The ledger so far is also returned, because core's shared ledger keeps a partial island's events. WP4 decides
    whether to merge it.
  - numerical_failure returns status and message, plus the ledger so far (WP4, 11-16).
    - Core's shared ledger keeps the events up to the failure, and `v3_calibrate`'s exported HPM-so-far includes them.
      WP4 merges the ledger so far in both stop cases.
    - Meaning: the serial prefix. That is every event of the earlier rounds; in the failing round (or the initial
      draw), the events of particles 1…i−1; and the events of the failing particle i at positions before the failing
      score.
    - Label-major processes a round's particles together, so the prefix is rebuilt exactly as follows.
      - At each round start in a calibration role, after the step-boundary compaction, the island keeps:
        - the published kept runs, which are immutable `shared_ptr`s, so keeping them is O(1);
        - copies of the tallies;
        - the particles' states.
      - On a failure, it restores that state and replays the round's prefix particle-major, serially, at the same
        addresses, so the events and offers are identical.
      - The replay stops at the failing score.
    - The cost is one partial particle-major round, and only on failure. The compat island is already serial
      particle-major, so its ledger is the prefix directly.
    - Tests: in compat, ledger so far = CoreRunner's ledger after the failure, bit for bit. In law mode, label-major =
      particle-major (threads 1 and 3). The failure is forced at the initial draw and at a Gibbs flip in a bridge
      round (the existing failure fixtures).
  - There are no island checkpoints in calibration.
- **Compat.**
  - Streams are caller-owned: `IslandConfig::compat_src` is a `v4::CompatSource*` that is required for calibration
    roles. The streams are 0 (pilot, e = 0) or 5 (e = 1), and 1–4 or 6–9 for the diagnostic islands.
  - The island draws from the stream in core's serial order and leaves it advanced. WP4 keeps each stream across
    rebuilds (R6). A final compat island keeps its own stream 9 + r unless one is passed.
  - `fresh` and the cache statistics are on the compat exclusion list (spec §4.1, OD-3): no seen-set, never compared.
- **Golden tests.**
  - Per island, against WP4's `CoreRunner`, which runs core `Engine::run_island_s` with a fresh v3 ledger and
    caller-owned streams. Fixtures are `fixture()` / `make_setup()` from `tests/golden/wp4_harness.cpp`.
  - Compat (bit-identical) and law mode (particle-major = label-major; the island = core's law through the adapter, as
    for final islands).
  - WP4 compares the whole calibration with `v3_calibrate`, so swapping in this runner changes no calib.bin bits in
    compat.

- **Built (v0.7).**
  - The runner is `include/v4/island/calib_runner.h`: `CalibIslandRunner<A>`, header-only. It owns the compat streams
    and converts the island's output to WP4's `IslandOut`.
  - The island side is in `island_impl.h`.
    - Address role, tier and iteration come from `IslandConfig::role / tier / iter`.
    - `base_key()` gives (CALIB, e, k, r).
    - `phase_of()` gives PH_PILOT / PH_DIAG.
    - Measured rounds are numbered L + h in the key; the address keeps h.
    - `forced` counts the forced pilot steps.
  - Ledger so far after a numerical failure: the round start keeps the published kept runs (O(1)) and a copy of the
    particles. `rebuild_prefix()` discards the round's buffers and tallies, restores the stores (`TopStore::restore`)
    and replays particles 1…i serially, particle-major.
  - Compat stops at the first failure: no further draws, as core.
  - The plan gains a `calib_snapshot` term (one kept run per store and a copy of the population).
- **The calibrate command.**
  - `src/calib/calib_run.cpp` runs `CalibIslandRunner` with the start law and neighbours read from setup.bin
    (`island/setup_load.h`).
    - Partition and block tables are read.
    - The sampler is rebuilt by core's arithmetic.
    - WP2's `size_cum`, when present, must equal the rebuild bit for bit.
  - The kernel and arithmetic depend on the mode: compat and law use the bit form, particle-major (compat on 1 thread);
    V uses class A, label-major.
  - Build changes:
    - a cycle between `v4_bit` (calib_run) and `v4_a` (the class-A island), declared in `island.cmake`;
    - every translation unit that calls the island is compiled with the island's ISA (inline ISA namespaces; m9 will
      remove the need).
- **Memory plan (re-check m1, manager 11-16).**
  - The serial staging is reserved at limit + one buffer. Particle-major islands with threads > 1 fix glibc's mmap
    threshold.
  - New terms:
    - `calib_snapshot`: one kept run per store plus a copy of the population;
    - **`headroom` = 12% of every term except the inputs**: allocator slack and the run-to-run variation of the peak. The
      VmHWM of one label-major row varied from 220 to 237 MiB against a 243 MiB plan.
  - The plan-bound test requires plan ≥ 1.10 × measured in every row: label-major G 64 / 256 with leaders off / on,
    particle-major on 3 threads, and a calibration island.
  - The calibrate command passes the Start model (`island::start_bytes_model`, §1.13) as the inputs term until the
    island reads WP2's flat arrays as a view.
- **Tests.** MEASURED, Owls, 3 threads, `nice -n 19`.
  - `golden_calibration_islands_compat_vs_core`: 10 islands (pilot e = 0; 2 rebuilds × 4 diagnostic islands; pilot
    e = 1) on streams 0–5, continued. Everything equals core in bits, ledgers and stream positions included.
  - `golden_calibration_islands_law_vs_core`: the same sequence on addressed uniforms, against core through the address
    adapter, which tracks phases under `phase_override`. Particle-major on 1 thread and label-major on 3 threads.
  - `golden_calibration_failure_ledger_so_far`: initial-draw and Gibbs-flip failures. The ledger so far equals core's
    ledger after its throw: compat, PM 1/3 threads, LM 3 threads.
  - `calibrate_command_end_to_end`: `smcbvs4 calibrate` in compat, law and V. V gives the same calibration at 1 and 3
    threads.
  - WP4's R golden with `runner = "wp3"`: the whole calibration through WP3's islands equals `v3_calibrate`, the
    calib.bin round trip included.

### 1.12 Planned (manager-approved 11-16): StartView over WP2's flat setup arrays
- **What changes.**
  - The island reads WP2's `setup.h` arrays as a view over the mapped setup.bin instead of expanding them into
    `dep::Start`.
  - Arrays read: the partition, `code_ptr` / `logr`, `size_logmass` / `size_cum`, `cond_ptr` / `cond_cum`, `logZbar0`.
  - `codes_by_size` and `sub_cum` are rebuilt per draw, only for the blocks the draw selects (D-18).
  - `c0r` is dropped. The 8-lane size-0 test gathers `cond_cum[cond_ptr[b*(K+1) + r]]`: the same comparison, the same
    bits.
  - One view type serves both owned storage (tests, bench) and mapped storage.
  - The memory plan's inputs term becomes the mapped section lengths.
- **WP2's layout answers (11-16).**
  - The row index is b·(K+1) + r, b-major. Row (b, r) holds min(m_b, r) + 1 cumulative masses, equal to core's bits,
    and ends at 1.0.
  - An all-−∞ row has the same length and holds zeros, so the gather of entry 0 is always in bounds. A valid draw never
    reaches such a row; debug builds assert this.
  - Pending HQ: WP2 may move `cond_cum` on demand (`cond_row(b, r)`, same bits). The gather then calls it.
- **Why.** WP2's ESTIMATE of the sections an island reads at 10⁶ is 4.4–14.1 GB, against 13–38 GB for `dep::Start`.
- **When.** After WP2's PR #13 merges, built on its `setup.h` types.

### 1.13 v0.7 (manager 11-16, 1M fast-track P4): the `island` command (`src/island/island_cmd.cpp`)
- **What it runs.** One **final** island r of a fit. Pilot and diagnostic islands run inside `calibrate`, which owns
  their streams and ledgers (§1.11); `--role` other than `final` is `invalid_input`.
- **Argument forms** (the same rules as WP4's `merge`, INTERFACES §1; proposed for WP1 to copy into §1):
  - **Driver form:** `island --manifest island_r.json --out island_r.bin [--threads k] [--mem-budget BYTES]`.
    - The manifest is authoritative. Inputs are found by base name (`data.bin`, `setup.bin`, `calib.bin`) among its
      `inputs`, and the mode is its `mode`.
    - r = `params.id` (the driver's `--set params.id=$R`) or `params.island` (INTERFACES §5.3); seed = `params.seed`;
      R′ = `params.Rp` (r ≤ R′ is checked).
    - An explicit `--data/--setup/--calib/--mode/--seed/--island/--id/--Rp` that disagrees is refused (exit 13), in
      either argument order; agreeing ones are accepted. A manifest whose `command` is not `island` is refused.
  - **Explicit form:** `island --data D --setup S --calib C --island r --seed s --mode compat|law|V --out island_r.bin
    [--Rp R] [--threads k] [--mem-budget BYTES | --mem-budget-gb G] [--G g] [--tile t] [--ckpt 0|1] [--ckpt-every-s s]`.
  - **Plan only:** either form with `--plan-only 1` (no `--out`), which prints the admission plan and does not run.
    Without files, `--plan-only 1 --mode M --n n --p p [--N --threads --G --k --inputs-bytes]` gives the same plan
    from sizes (ESTIMATE).
- **Settings come from calib.bin and the data, never from the arguments:** grid, N, L, Hm, tier, k_store from calib.bin;
  **B = min(isqrt n, isqrt p, 16) from `calib::budgets(n, p)`**, the budget the calibration ran with (review PR52 MAJOR-3).
  B is part of the law (the N-swap labels per round: shuffled order, addresses, compat stream use), and a hard-coded 14 is
  right only for n ≥ 196, p ≥ 196. A conflicting `--B` is `invalid_input`. Plans use the same B.
  - The calibration's status must be `ok`; its mode must equal the command's mode.
  - A given N or seed that differs from calib.bin's is refused.
  - **The manifest freezes the scientific parameters** (seed, id / island, Rp; for `calibrate` also seed, I_max,
    refine_m). An explicit different value is refused **on either side of `--manifest`** (review PR52 MAJOR-4): `main`
    copies a manifest's `params` over an earlier explicit value, so it also records the explicit values separately
    (`args["cli_explicit"]`), and the commands compare those (`include/v4/cmd_args.h`). `merge` (WP4) has the same
    copy-over hazard for `--Rp` / `--mode`; it can use `cmd::explicit_args()`.
  - calib.bin's `meta.inputs` must equal the data.bin and setup.bin in use, and setup.bin's must equal data.bin.
  - Only calib.bin's `meta` and `grid` are read; its stores (GBs at 10⁶) are not loaded. Every section hash is
    still verified on open.
- **Kernels (D-21).**
  - compat: bit form, particle-major, 1 thread (forced), v3 stream 9 + r.
  - law: bit form, particle-major.
  - V: class A, label-major.
- **Memory (INTERFACES §7).** `--mem-budget` is the whole task's memory.
  - **Admission comes before anything that grows with the setup is allocated** (review PR52 MAJOR-2). The command reads
    calib.bin's settings, data.bin's n / p / K from its mapped metadata and `read_setup_dims` (setup.bin mapped: the
    block-size histogram, the section lengths and size_logmass; nothing expanded), plans, and refuses or admits. Only
    then are the arrays read: `load_data` (X), `load_start`, `load_neighbours`, with every file verified in full.
  - The plan is `plan_island`'s own rule, from `plan_sizes` + `plan_with_budget` (island.h; `plan_island` calls them,
    so there is one implementation). Its caller-supplied term is `start_bytes_model(dims)`: an upper-bound model of the
    expanded `dep::Start` + neighbour lists from the section sizes (payloads, vector headers, ×2 for push_back growth). The
    same number is used before the load and in the run, so the pre-load refusal and the island's own admission are one
    decision. Test `start_bytes_model_bounds_start_bytes` pins `start_bytes ≤ model ≤ 3 × start_bytes` (measured 1.05–1.17).
    StartView (§1.12) replaces the model by the mapped section lengths.
  - k = max(8, q90(π₀ size) + 1, k_store), with q90 from setup.bin's persisted `size_logmass` (required).
  - With `--G 0` (the default) and a budget, the island takes the largest G ≤ 256 that fits. It is then admitted iff
    the G = 1 plan fits.
  - Over budget, the result is `resource_limit` before the run. island_r.bin is still written with that status, the
    request's mode and schedule (header mode, `meta.mode`, `grid`, T; review PR52 m6) and no estimate section (GUARD-W);
    the exit code is 11. `--plan-only` makes the same decision from the same numbers and loads nothing.
  - **What remains for StartView:** the memory the island process holds after admission is still the expanded Start (the
    model bounds it); the setup is read twice (mapped for the dimensions, then expanded). `calibrate` (WP4) still reads data.bin
    and `read_setup` (copies of blk / pos / logr and the table stores) before its own plan; that reader split is WP4's
    (PR46 MAJOR-2), and `read_setup_dims` is the cheap half of it.
- **Output.**
  - island_r.bin (island_file.h) with `meta.inputs` = the three content hashes, which is what the merge checks.
  - island_r.bin is written in every status except `interrupted`.
  - The record holds status, reason, r, N, T, L, Hm, tier, `mem_plan`, `G_used`, `output_hash` (FNV over the law
    outputs, = `IslandRun::hash()`), `init_hash`, `logZ` (completed only), `resumed_from_step`, and the seconds
    (load / island / ckpt / store check / total).
- **Checkpoints.**
  - Written to `<out without .bin>.ckpt.{a,b}` (INTERFACES §5.1), every `--ckpt-every-s` seconds (default 600).
  - **Identity (review PR52 MAJOR-1).** The checkpoint fingerprint includes the data / setup / calib **content hashes**
    (`IslandConfig::input_id`, `input_identity()`), checked before any state is read: a restart on other inputs is
    `invalid_input` (exit 13), the checkpoint stays on disk, no island file is written. Test `island_command_resume` changes only
    the neighbour graph (valid, normal checks all pass; calib.bin's inputs updated), so only the identity tells the runs apart.
  - **Container (review PR52 m7).** The files are not kind-8 containers: they are a streamed payload (magic `SMCV4CKP`,
    two generations, FNV checksum, atomic rename) because the store held by an island at 10⁶ is GBs and `fmt::Writer`
    would hold a second copy of it (its `add_copy` owns its bytes). `smcbvs4 info` therefore cannot read them. A contract
    amendment to INTERFACES §5.1 (kind 8 = this streamed layout, or a Writer that streams) is requested from WP1 through the
    manager; no behaviour changes meanwhile.
  - A rerun of the same command resumes from the newest valid generation. The fingerprint includes the binary, so a
    resume needs the same executable.
  - Both generations are removed once island_r.bin is written as completed. They are kept on any other status.
- **`calibrate --plan-only` (review PR39 MAJOR-2).**
  - It adds `island_plan`: the largest calibration island (max H and Hm over the tiers the rule can use, leaders, the
    round-start snapshot), planned as `CalibIslandRunner` admits it under WP4's N-1 rule.
  - The caller-supplied term is `start_bytes_model` (from `read_setup_dims`: nothing is expanded, also in the run, where
    the island's admission precedes `load_start`) + the calibration's resident state without the inputs (ledger + export).
  - `total` is the plan at the G the budget allows; `floor` is the G = 1 plan. The calibration is admitted iff
    `floor ≤ --mem-budget`, and the driver sizes from it. Over budget, the result is `resource_limit` (exit 11), and the
    plan is printed all the same (review PR52 m5), so the requester sees the minimum budget when resizing.
  - Without setup.bin it plans from sizes (k = kbar, setup inputs **not** counted).
  - `mem_plan.island_budget` (budget − resident with inputs; obsolete since N-1) is removed (review PR39 m6).
- **Fixed on the way.** `calibrate`'s record held `status: "ok"`, which `main` cannot map: a successful
  `smcbvs4 calibrate` exited 13 with its record overwritten, and the driver's fill would have refused calib.bin.
  `status` is now the task status; `cal_status` is the v3 name (ok, schedule_limit, …).
- **Link graph (review PR39 m4).** `calibrate` and `island` (both forms of the island) live in `v4_cmd`, which links
  `v4_a` and `v4_bit`. There is no v4_bit ↔ v4_a cycle. WP4's R golden still links `libv4_bit.a` alone.
- **Tests** (`tests/test_island_cmd.cpp`):
  - `island_command_end_to_end`: calibrate → island → merge through the binary, per mode. The file equals
    `run_island` (output hash). In V, 1 thread / G 7 / tile 64 gives the same sections as 3 threads. Theory-mode
    merges need a clean commit (MergeTheory) and are expected refused on `-dirty` builds.
  - `island_command_driver_manifest`: driver dry run → `p1m_manifest.py fill --set params.id=3` → the driver's
    command line. Equal to the explicit form; manifest authority.
  - `island_command_refusals_and_budget`: the invalid_input cases, admission to the byte, and plans (files, sizes,
    calibrate N-1 floor).
  - `island_command_resume`: resume from a checkpoint left by an interrupted island, with the same output; the
    checkpoints are removed after completion.
  - `plan_from_sizes_equals_plan_island`.

---

## 2. Addressed sampling

### 2.1 Address map (INTERFACES §3; Philox4x32-10, key = {seed, role<<28 | tier<<26 | iter<<20 | island},
counter = {slot, position, particle, xph<<24 | stage}); `particle` is always the **destination** index 1…N
| consumer | xph | stage | particle | position | slot | code |
|---|---|---|---|---|---|---|
| initial π₀ draw of particle i | INIT | 0 | i | 0 | 0…u−1 in the documented order: size, block sizes J…1, submodels 1…J | `run()` init |
| resampling uniform i at stage t | RESAMPLE | t | i (the i-th draw of `resample`) | 0 | 0 | `resample()` |
| round order, Fisher–Yates step t = m−1…1 | BRIDGE / BURN / MEASURED | t / l / h | i | 0 | m−1−t | `draw_order()` |
| Gibbs label at position q | as round | as round | i | q | 0 | phase A (label-major), `pm_round` |
| U swap at q | as round | as round | i | q | 0 j, 1 l, 2 accept | `step_nongibbs` |
| N_b swap at q | as round | as round | i | q | 0 j, 1 l, 2 accept | `step_nongibbs` |
| I at q | as round | as round | i | q | 0…u−1 the π₀ draw, `SLOT_ACCEPT` = 0xFFFFFFFF accept | `step_nongibbs` |
**Destination rule.** After resampling, particle i is a copy of ancestor a_i, but every later uniform uses address
particle = i (its destination), stage/round = the current one: no stream state is inherited (production stores no
generator state at all). **Injectivity.** (xph, stage) identifies the phase and the stage/round; position 0 within a
round phase is the order draw only, positions 1…m are the steps; within a step the slot is the ordinal of the uniform
in that step's documented order (variable-length π₀ draws included, u ≤ 1 + 2J < 2³²−1, so they never reach
SLOT_ACCEPT); INIT and RESAMPLE have their own xph. The key separates role/tier/iter/island. Hence distinct consumers
get distinct counters. Widths: island < 2²⁰, iter < 64, tier < 4, stage/round < 2²⁴, particle < 2³², position ≤ m =
p + B + 2 < 2³², slot < 2³²; WP1's `address_key/ctr` throw on overflow. Final islands: role FINAL, tier = iter = 0.
I5 is checked by WP1's `CheckedSource` in tests (to wire; the island currently calls `uniform_at` directly).
**v0.1.5** will add Sol's slot taxonomy (order / resampling / categorical sizes / submodels / acceptances); the island
code computes every address in four functions (`addr`, `draw_order`, `step_nongibbs`, init), so adopting a new map is
local. Any map change changes the trajectories (law-equivalent, class L) and the golden adapter changes with it.

### 2.2 Event key (provenance) and logical counts
EventKey = (seg = FINAL, tier, iter, unit = r, xph, stage, round, particle, position, sub). Today `sub` = 0 for every
event; v0.1.5 (Sol F4) adds the within-step ordinal: proposed **sub = 0 held, 1 flip (Gibbs); 0 the proposal (U/N/I);
0 init**. Held events are never offered, so the HPM key of a Gibbs flip is (…, q, 1). The serial traversal across
units (tables → inherited → islands → final LS → LS0) is the merge's (WP4) concern; inside an island the key order
equals core's serial order (particle-major) — golden-tested on provenance.
Logical counts, by mechanism (fixes spec I4, Sol F4): per particle-round, `gibbs_held` = p (every Gibbs step);
`gibbs_flip` = p − #(additions refused at |S| = K); `uswap` = 1 − self-loops; `nswap` = B − self-loops − empty N(j)\S;
`indep` = 1; `init` = N once. Test `logical_counts_and_invariants` checks held = N·p·rounds and the U/N/I identities;
the flip identity check is to add.

---

## 3. The label-major round (class A for V; spec §3 rules 1–4)

### 3.1 Notation
m = p + B + 2 labels; particle i has round order ord_i and inverse inv_i (1-based positions); its state at the start of
pass r is (S, log m, lg0, d) and its consumed prefix is positions 1…q_i.

### 3.2 Group formation and buffers
Particles [g0, g0 + G) in index order, **G ≤ 256** (memory: orders + inverses 2 G m × 4 B = 2 GB at 10⁶, G = 256; the
per-support rows nsup × p × 16 B ≤ G × 16 MB = 4 GB at 10⁶: **G = 64 at 10⁶**, Q3). Groups are processed one after the
other; inside a group, threads work over tiles (phase A, B), supports (cache build) or particles (orders, walk).

### 3.3 One pass
1. **Distinct supports** of the active particles, key (hash, bits of log m, S); particle lists sorted by index.
2. **Cache** per support: Cholesky factors of H and A, forward solve, prefix sums, composite blocks, k deletion scores
   (WP1 Bit scorer), odds of members.
3. **Active columns** A = ∪ members of supports that can add; gathered contiguous (|A| × n).
4. **Phase A** (threads over tiles of 128 labels, X pre-tiled row-major, 64-B aligned): products x_aᵀx_j (sequential in
   i), flip scores and odds for every (support, label) into row buffers; for each particle on the support, the first
   position > q_i whose addressed uniform changes its state (8-lane Philox, `fmin` = integer atomic min).
5. **Walk** (threads over particles): U/N/I labels with q_i < position < fmin_i executed in position order on the
   unchanged state; the first that changes the state ends the segment: e_i = that position; else e_i = fmin_i (Gibbs
   change) or m (no change).
6. **Phase B** (threads over tiles): Gibbs labels at positions (q_i, e_i] are consumed: RB, held/flip counters,
   island_best, HPM candidate with the key of the smallest consuming particle, one store offer per (support, label).
7. **Apply**: new state (Gibbs: S △ j with the row-buffer log m; U/N/I: the walk's state), q_i ← e_i; done iff e_i = m.

### 3.4 Sweeps per particle (M) and re-entry
A particle takes one pass per state change plus one: M = 1 + (Gibbs changes + accepted U/N/I) per round. A moved
particle re-enters the next pass with its new support and its consumed prefix q_i; positions ≤ q_i are never re-read.
MEASURED (Owls, `v4_bench_island island 10000 2500 3 A lm 256 128 30 8 4`, AR(0.6), n = 200, geometric 30-stage grid
— **not a calibrated grid**): M = 4.19; (support, label) pairs per particle-round = 2.96 p (sharing); 1.4 Gibbs
changes per particle-round at φ = 1, 2.4 at φ ≈ 0; 57.8 distinct supports per pass (G = 256).

### 3.5 Equality with the particle-major algorithm (same arithmetic)
For each particle the label-major round performs **the same sequence of state transitions** as `pm_round`:
- position by position, the state used at position t is the state after the last change before t (a segment never
  crosses a change: fmin and the walk stop at the first change);
- every value used at a position is the same function of (state, label, address): flip score and odds come from the
  same 8-lane primitives (`eval8_add`/`eval1`, lane-wise identical ops whatever the other lanes), the uniform from the
  same address, the U/N/I steps from the same function;
- labels after the change are recomputed in the next pass from the new state (their first computation is discarded,
  rule 2), so a value is never used with a stale state.
The ledger receives the same events (same model, F, key, phase, mech) — stores and tallies are order-free (§1.3) —
and RB the same per-(particle, label) odds (exact sum, §3.6). Particles are independent within a round (no shared
state but the order-free ledger), so group boundaries and thread schedules do not matter. Hence identical outputs; T3
tests the hash in both arithmetic forms.

### 3.6 Reduction order (RB) — declared choice
`o_j` enters as the integer ⌊o_j · 2⁶³⌋ into unsigned 128-bit accumulators (current measured round and total). The
sum is exact, so it does not depend on particle, pass, group or thread order (stronger than spec §3 rule 3's "particle
order in chunks of 64"); against core's double sum it is class A, |error| ≤ 2⁻⁶³ per term (golden: ≤ 1e-12 relative).
Writes are race-free: phase B threads own disjoint label tiles (particle-major: per-thread arrays summed exactly).
Memory 32 B × p (+ 16 B × p × T particle-major). Q2 asks to confirm this instead of chunked double sums.

### 3.7 Class-A path values
A class-A flip score (bordered update from S) can differ in the last bits from the value of the same model reached
otherwise (full Bit score after U/N/I, or a flip from another support). Consequences, all deterministic: the particle
keeps the value it was given; supports are keyed by (S, log m bits); the store keeps the largest value per model;
the HPM order adds the key after (F, |S|, lex). Bit form: no effect. (Alternative, Q2b: canonicalise every accepted
state by a full Bit score — +1 score per change, removes path dependence.)

---

## 4. Restart (spec §6; T6; D-21: stage boundaries only)
**When.** After a step (init, each bridge stage, each burn-in and measured round), after the absorb, at most every
`ckpt_every_s` (600 s) and always at `stop_after_step` (tests).
**Content.** Configuration fingerprint (seed, island, N, grid, L, Hm, B, cap, n, p, y'y, log Z̄₀, J, arithmetic — not
threads, G, tile or kernel: a resume may change them); step index; log Ẑ so far; init hash; particles (S, h, log m,
lg0, d, F); stage table, terminal moves and distinct counts; `rb_round` so far; the 128-bit RB totals; the master tally
(counters, island_best, HPM + key); the compacted store (v, hash, off, len, pool). No generator state (addresses are
recomputed). Compat mode (not built by WP3) would add the xoshiro state.
**Atomicity.** Two generations `<path>.a/.b` written alternately: payload → `<file>.tmp.<pid>`, `fsync`, `rename`.
Header: magic, generation, length, FNV-1a checksum (provisional; WP1's kind-8 file with SHA-256 sections replaces it).
A load reads both, keeps those with valid magic, length, checksum and fingerprint, takes the larger generation.
**Equivalence.** Every output of the remaining steps is a function of exactly the checkpointed state and the
addresses (store: top_c(top_c(A) ∪ B) = top_c(A ∪ B); tallies: sums/max/strict-order max; RB: exact integers), so a
resumed run produces identical bytes. **Tests**: `t6_restart_bit_identical` — interrupt after steps 0, 2, 5, 6, last
and resume with other threads/G/kernel; corrupt newest generation → resume from the older one. **To add** (Sol F5,
manager item 7): kill during write = truncated `.tmp` and truncated generation file (simulated), crash between
fsync and rename, repeated resubmission (resume twice), resume with a different binary/config → refusal.

---

## 5. Open questions and decisions needed from the manager
1. **Bit-form label-major kernel** (exists, tested, T3-equal): keep as a test-only path (config check refuses it in
   production; zero maintenance cost so far) or delete? Recommendation: keep test-only.
2. **RB reduction**: approve the exact 128-bit fixed-point sum (§3.6) in place of spec §3 rule 3's chunked double
   sum. (2b) Class-A path values (§3.7): accept, or canonicalise accepted states by a full Bit score?
3. **G at 10⁶**: G = 64 (row buffers 1 GB) vs 256 (4 GB); smaller G costs more passes per particle. Recommend G = 64
   at 10⁶, 256 at ≤ 10⁵, set by the admission check from `--mem-budget`.
4. **Store at large supports**: the top store's pool grows with k; at 1M and k ≈ 20 the kept run alone is ≈ 4.2 GB.
   Policy on refusal vs a capped pool (e.g. refuse when the admission check fails at a compaction)?
5. **Store offer cost** (MEASURED 213 ns per offer in a duplicate-heavy mix at c = 4·10⁶): approve a worker-side
   duplicate filter against an immutable index snapshot (double-buffered index: + 4c × 4 B), or accept the cost?
6. **Checkpoint size at 10⁶** (≈ store 2.2–4.5 GB + 16 p): write streamed from the arrays (no byte image) — needed to
   keep the peak inside the budget; OK to implement now (it is in the uncontested restart part)?
7. **v0.1.5 event key**: confirm `sub` = 0 held / 1 flip / 0 proposals / 0 init (§2.2).
8. **The `island` CLI command and `island_r.bin`** wait for WP2 (`setup.bin`) and WP4 (`calib.bin` grid) readers;
   until then `run_island()` takes in-memory Data/Start/Neighbours. Who owns the `island_r.bin` section writer — WP3
   (my assumption, per INTERFACES §5.1)?
9. **Measured cost vs plan** (Owls, loaded, 3 threads; to be re-measured on SPR at G0-style thread counts): class-A
   island at 10⁴ c = **545 ns** per elementary step (plan 300) with M = 4.19 (plan 3) on an uncalibrated grid;
   bit-form label-major 994 ns. Kernel per (support, label) at 10⁵: class A 147 ns (256 distinct supports, |A| = 1,273;
   products 90 + flip/odds 57) and 66 ns (64 copies of S₀); bit form 282 / 187 ns. Within the G0 bound (700 ns) but
   above the precise-plan value; levers: phase B (96 ns per step), M, products sharing, offers.

---

## 6. Compat island (v0.2; manager Q2: the ≤ 5k bit anchor against unmodified core)
`IslandConfig::compat`: Arith::Bit, particle-major, 1 thread, fixed grid. Every uniform is the next draw of WP1's
`CompatSource` on the island's v3 stream (seed, 9 + r) — the particle-major code requests uniforms in exactly core's
serial order (proved address by address by the golden adapter). RB is core's double sum in serial order, `rb_round`
the difference of cumulative sums (`core/cpp/v3_engine.h:350-364`); the two leader stores (lead0: log γ₀, lead1: F,
LEX order, 20p) are NOT kept in final runs (INTERFACES v0.1.7: not outputs in any mode; option `leaders`, default off,
for calibration islands and the golden test only); checkpoints add the xoshiro state + count and the double accumulator;
island_r.bin is mode `compat` and never carries leader stores. Test `golden_compat_island_vs_core_serial_stream`: core's
`Engine::run_island` with its own `RngSource` on stream 9 + r against the compat island — **every output in bits**
(RB, rb_round, PIP included), HPM + provenance, counters, store, stream position (and, with the test-only `leaders`
option, both leader stores).

## 7. Manager decisions on §5 (2026-11-15)
Q1 bit-form LM test-only (production refuses; `allow_test_kernels`). Q2 exact fixed-point RB in law mode, core's double
sum in compat. Q2b accepted states canonicalised by a full Bit score. Q3 G chosen by the budget (largest ≤ 256).
Q4 no capped pool; a step-boundary check of the content-determined kept pool ends the island with resource_limit.
Q5 duplicate filter deferred then implemented after the SPR profile showed store compaction as the phase-B bottleneck.
Q6 streamed checkpoints. Q7 sub = held 0 / flip 1. Q8 WP3 owns island_r.bin (terminal supports: N after the last
measured round).
