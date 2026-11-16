# PR #26 re-check: WP3 slice 3 fixes (B1–B4, r1, r2), P2 at 10⁶ and L5

Reviewer: Opus 5.5 (high), independent of the author. Date: 2026-11-16.
- Branch: `exp/P1M-wp3-island4` @ `5c8ab8a5`; base `exp/P1M-engine` @ `57a6ba3f` (merged in at `b32a5c50`).
- Re-checked: `32b11a91..5c8ab8a5` (engine diff vs base: `amath.h`, `dep.h`, `island.h`, `kernel.h`, `memory.h`, `store.h`,
  `island_impl.h`, the bench, three NOTS scripts and `nots_guard.sh`).
- First review: `PR26_review.md` (FIX FIRST: B1 MAJOR, B2–B4 MINOR, 3 nits). Carried in: `PR24_recheck.md` r1, r2.
- Contract: INTERFACES v0.1.10. Results that motivate the PR: `results/WP3_LEVERS_SPR.md`.
- Read-only: detached worktrees and builds in `/home/fb31/SMC_Engineering_Department/tmp/20261116-recheck-26` (removed
  after). Nothing was pushed or commented. Owls, `nice -n 19`, `taskset` to 3 cores, one test suite at a time.

## Verdict: **MERGE** (3 MINOR to disposition; none affects outputs or the label-major 10⁶ path)

- **Every L5 change is bit-identical.**
  - Island hashes are equal before (`32b11a91`) and after (`5c8ab8a5`): A and bit, LM and PM, 1 and 3 threads, G = 64
    and 256, at x86-64-v2 and x86-64-v4. That is 20 of 20 configurations.
  - Direct checks: the new π₀ draw equals the old on 202,300 draws (10 setups); the new Fisher–Yates order equals the
    old on 28,248 (m, address) cases; `philox8_word` equals `uniform_at` on 1.6 M lanes.
- **The replacement sort is deterministic.** `psort_noalloc` equals `std::sort` position by position in 1,980 cases
  (1–96 threads, both store orders), given the store's precondition that the hash is a function of the model.
- **The memory plan bounds the label-major peak in every case I measured.**
  - p = 2·10⁴: margins +5.9 to +27.8 %.
  - p = 10⁵: margins +11.7 to +29.7 %, including small-π₀ data where the k = 8 floor sets the plan.
  - **Exception:** the particle-major (serial-store) kernel at 3 threads exceeds the plan by 9–21 % (m1).
- **B1–B4, r1 and r2 are fixed as claimed.** The bench exits 23 on a memory refusal and 13 without k_store at 10⁵. The
  guard refuses every bad TMPDIR or build path I tried.
- **Tests:**
  - **100 of 100 pass** in the default build, plus WP5 (17), the competitor harness, the install script (23) and WP4
    golden (231,999 checks, 0 failures); rc 0.
  - x86-64-v4 build: see test run 2.
  - T3: bit `44a15bfc6fb8d233`, A `d2df149413596a19`.

Counts: CRITICAL 0 · MAJOR 0 · MINOR 3 · nits 4.

## Test runs (Owls, Xeon Gold 6148, gcc 11.5.0, load ≈ 20–23 on 80 CPUs)
1. **`tests/run_tests.sh --build-dir …/bh`** (default x86-64-v2): **100 test cases, 0 failed, 0 check failures**.
   - WP5 Slurm driver: 17 OK. Competitor harness: OK. Install script: 23 OK. WP4 golden: 231,999 checks, 0 failures.
     rc 0.
   - `git_commit` = `5c8ab8a5…`.
   - New tests:
     - `oom_in_parallel_compaction_is_resource_limit`;
     - `k_store_required_at_1e5`;
     - `pi0_fast_draw_equals_draw`: 3,000 / 3,000 draws for each of 2 partitions;
     - `mem_plan_bounds_measured_peak_2e4`: 217/243, 341/459, 230/355 and 410/571 MiB.
2. **Same runner, x86-64-v4 build** (`-DV4_ISLAND_ISA=x86-64-v4`): RESULT_V4.
3. **Island hashes before/after** (`v4_bench_island island 20000 300 1,3 {A,bit} {lm,pm} 64 128 geo:4 1 1`; and
   `… A lm 256 128 geo:6 2 2`). Builds: `32b11a91` (pre-L5) and `5c8ab8a5`. MEASURED.

   | build | config | `32b11a91` (1 thread, 3 threads) | `5c8ab8a5` (1 thread, 3 threads) |
   |---|---|---|---|
   | x86-64-v2 | A lm G64 | `9153c1f05c8ef1e8` ×2 | `9153c1f05c8ef1e8` ×2 |
   | x86-64-v2 | A pm | `9153c1f05c8ef1e8` ×2 | `9153c1f05c8ef1e8` ×2 |
   | x86-64-v2 | bit lm G64 | `f9c6272ed1ffbae5` ×2 | `f9c6272ed1ffbae5` ×2 |
   | x86-64-v2 | bit pm | `f9c6272ed1ffbae5` ×2 | `f9c6272ed1ffbae5` ×2 |
   | x86-64-v2 | A lm G256, 6 stages, L2 Hm2 | `e6c5bd4753f38c83` ×2 | `e6c5bd4753f38c83` ×2 (products block 1, auto) |
   | x86-64-v4 | A lm G256, 6 stages, L2 Hm2 | `a657857325d58f30` ×2 | `a657857325d58f30` ×2 (products block 4, auto) |

   - These runs exercise the new π₀ draw (initial draws and I moves), the new order, the G = 256 row sizing, the
     parallel apply, the walk-offer compaction and the wave bound.
   - The 2·10⁴ hashes equal the first review's.
   - B2's auto block (1 at v2, 4 at v4) is confirmed and output-neutral.
4. **Direct L5 equality** (reviewer driver `chk/l5.cpp`, linked to the PR's headers, random full-range addresses):
   - `philox8_word(word 0 = slot)` vs `uniform_at`: 1,600,000 lanes, 0 mismatches.
   - **Fisher–Yates.** The old loop (`32b11a91` `draw_order`) vs the new 8-lane prefetched loop (copied verbatim):
     - m = 1..70 (every 8-block edge), 127–129, 1,000, 1,016, 4,097, 20,016 and 100,016;
     - **28,248 cases, 0 differ.**
   - **π₀ draw.** `draw_pi0` vs `draw_pi0_fast`, 10 setups:
     - n ∈ {12, …, 200}, p ∈ {40, …, 10⁵};
     - blocks of 1, 4, 7 and 10, plus three irregular partitions with block sizes 1–9;
     - E|S| from 0.4 to 22.9, K up to 100, |S| up to 32.
     - **202,300 draws, 0 differ.**
5. **Parallel sort** (`chk/psort.cpp`):
   - Setup: `psort_noalloc` vs `std::sort` on `StoreRef`s with the store's two comparators (by model; store order, both
     LEX and HPM). Sizes 4,095–304,000, few to many distinct models, tied values, deliberate hash collisions, threads
     {1, 2, 3, 4, 5, 6, 7, 8, 11, 16, 96} (on 3 cores).
   - Result: **1,980 cases, 0 mismatches** (v bits, hash, |S| and S per position).
   - My first harness gave identical model contents *different* hashes. Then thread-dependent orders appeared (760 of
     1,980), which is expected: equivalent elements are no longer identical. The store's Zobrist hash is a function of
     S, so the precondition holds in the engine. See nit n1.
6. **Memory plan vs measured peak** (`chk/memrun.cpp`):
   - Method:
     - one fresh process per configuration;
     - `malloc_trim(0)` and `clear_refs 5` after the data;
     - "increment" = the island's VmHWM increment;
     - "plan" = `plan_island` (the admission's own call) minus the inputs term, as in the PR's test;
     - LM/PM class A, N = 500, grid 0/0.3/0.7/1, L = 1, Hm = 1, `k_store = 8`. MEASURED.

   | p | config | π₀ q90 | plan k | stored mean \|S\| | increment | plan | margin |
   |---|---|---|---|---|---|---|---|
   | 2·10⁴ | LM G64 T3 | 7 | 8 | 7.07 | 229 | 243 | +6.2 % |
   | 2·10⁴ | LM G256 T3 | 7 | 8 | 7.07 | 328 | 355 | +8.1 % |
   | 2·10⁴ | LM G256 T3, no k_store (opt-out) | 7 | 8 | 7.07 | 335 | 355 | +5.9 % |
   | 2·10⁴ | LM G64 **T1** (serial store) | 7 | 8 | 7.07 | 202 | 258 | +27.8 % |
   | 2·10⁴ | LM G64 T3 leaders | 7 | 8 | 7.07 | 389 | 459 | +18.0 % |
   | 2·10⁴ | LM G256 T3, β×2.5 | 7 | 8 | 7.01 | 310 | 355 | +14.5 % |
   | 2·10⁴ | **PM T3** (4 runs) | 7 | 8 | 7.07 | **226–258** | **205** | **−9.4 to −20.6 %** |
   | 2·10⁴ | PM T1 | 7 | 8 | 7.07 | 169 / 172 | 193 | +14.2 / +12.2 % |
   | 2·10⁴ | PM T3, `MALLOC_ARENA_MAX=1` | 7 | 8 | 7.07 | 163 | 205 | +25.6 % |
   | 10⁵ | LM G64 T3 | 15 | 16 | 6.02 | 1,265 | 1,416 | +11.9 % |
   | 10⁵ | LM G256 T3 | 15 | 16 | 6.02 | 1,709 | 1,910 | +11.7 % |
   | 10⁵ | PM T3 | 15 | 16 | 6.02 | 953 | 1,361 | +42.8 % |
   | 10⁵ | LM G256 T3, β×0.3 (small π₀) | 1 | 8 | 1.98 | 1,247 | 1,555 | +24.6 % |
   | 10⁵ | LM G256 T3, β×0.4 | 4 | 8 | 3.14 | 1,278 | 1,555 | +21.7 % |
   | 10⁵ | LM G64 T3, β×0.4 | 4 | 8 | 3.14 | 841 | 1,091 | +29.7 % |

   The label-major bound holds in all 11 LM rows (all MiB). PM at 3 threads fails at k = 8 (m1).
7. **Plan at 10⁶** (`V4_K_STORE=8 v4_bench_island plan 1000000 2500 96 64,256`):
   - G = 64: **37.86 GiB**; G = 256: **44.00 GiB**. k = 62, which is q90 + 1 of the stand-in π₀. The store term is
     28.6 GiB.
   - These match the PR. They are above the SPR-measured 25.4 / 34.3 GB (pre-fix code, stand-in π₀).
   - With a small real π₀, k falls to 8 and the store term to about 6 GiB. That case was not measured at 10⁶; at 10⁵ the
     same setting holds by 22–30 % (table above).
8. **Bench exit codes** (B1):
   - `V4_MEM_BUDGET_GB=0.001 … island 2000 …` prints `status=3` and exits **23**.
   - `V4_K_STORE=0 … island 100000 …` prints `REFUSED: invalid_input … needs k_store` and exits **13**.
   - A normal run exits 0.
9. **`nots_guard.sh`** (sourced in a subshell). Results:

   | TMPDIR / build directory | rc |
   |---|---|
   | no TMPDIR | 2 |
   | `TMPDIR=/tmp` | 2 |
   | build directory `/tmp/b` | 2 |
   | TMPDIR through a symlink inside the department folder that points to `/tmp` | 2 |
   | build directory through that symlink | 2 |
   | `~/SMC_Engineering_Department/../x` | 2 |
   | TMPDIR equal to the root itself | 2 |
   | valid paths | 0, with `LOGDIR=<build>/logs` |

   Relative build directories are resolved before the check.

## Re-check of the findings

| # | Finding | Status | Evidence |
|---|---|---|---|
| B1 | `g256` refused at 10⁶ | **Fixed** | The bench reads `V4_K_STORE` (scripts export 8). Exit 20 + status, or `exit_code` (run 8). The plan at k_store 8 is 44.00 GiB < 60 (run 7). |
| B2 | Block 4 slower on x86-64-v2 | **Fixed** | `products_block_of`: 4 only under `__AVX512F__`. Run 3: block 1 at v2, block 4 at v4, same hashes. |
| B3 | Socket-mode gaps | **Fixed** | Details below. |
| B4 | TMPDIR / paths | **Fixed** | `nots_guard.sh` in all three scripts, logs in `<build>/logs` (run 9). See nit n2. |
| nits | `[round]` label, kernel bench block per run, PR body | Fixed | |
| r1 (#24) | k_store at p ≥ 10⁵ | **Fixed, broader than needed** | `island_impl.h:1053`. See m2. |
| r2 (#24) | OOM in parallel sort | **Fixed** | Details below. |

**B3 (socket mode).**
- It waits for both PIDs and collects each exit code. `if wait; then …; else rcs+=($?)` keeps the right code.
- It prints both logs.
- It fails on: rc ≠ 0, a missing `status=0` (the bench prints `status=%d` on every completed run), or an empty or
  equal hash.

**r2 (OOM in the parallel sort).**
- `psort_noalloc` (`store.h:45`) allocates the boundaries and the scratch before any region. The regions only call
  `std::sort` and `std::merge`, which never allocate.
- `r(s)` in `compact_parallel` is allocated outside the regions.
- The test hook throws at the sort site. The result is resource_limit (test).
- Pairwise merge for odd C: a lone tail chunk is copied by its own `std::merge` with an empty right half. Checked for
  C = 3, 5, 7 and 11.

**L5 by reading (the hashes above confirm each point).**
- **π₀ (`dep.h` `draw_pi0_fast`).**
  - `cat_draw_gt` (upper bound) returns 0 exactly when u < cum[0]. The 8-lane test against `c0r[r][b] =
    cond_cum[b][r][0]` therefore skips exactly the blocks the old loop gives size 0.
  - The full categorical runs on the same uniform (slot `PI0_BLOCKSIZE b`).
  - SUBMODEL draws are made for the same blocks, in increasing order.
  - Lanes past the stop are computed but never consumed. Addressed uniforms have no state, and compat keeps the serial
    path (`if (csrc)`).
  - `philox8_word` with word 0 = slot matches `address_ctr`'s `{slot, position, particle, xph|stage}`. Keys are equal.
- **Fisher–Yates.**
  - Slot d = m − 1 − t and `jj = floor(u · (t + 1))` are unchanged.
  - The targets depend only on the uniforms, so precomputing them for the next block is exact.
  - The clamped slots of the tail lanes are never used.
- **Score rows sized once.** Every (support, label) entry of `lbuf`/`obuf` is written in phase A before it is read:
  - members from the `del_*` arrays;
  - non-members by NaN/0, `eval1`, or the 8-lane path over all `valid` lanes.
  So dropping the re-zeroing cannot expose stale values.
- **Parallel apply.**
  - Particles are independent.
  - The class-A canonical score uses the thread's own scorer.
  - `fail.record` keeps the minimum particle index under a mutex.
  - `fail_fatal()` after the loop only adds the OOM path.
- **Walk-offer compaction and wave bound.** These change only when compactions happen. Store content is a function of
  the set of offers, already shown in #24, and the hashes are equal.

## New findings

### MINOR

**m1. The plan is not an upper bound for the particle-major (serial-store) kernel at more than 1 thread.**
- Where: `memory.h:54` (serial `store_peak_bytes`), `store.h:175` (`reserve_staging`), and the
  `flush()`/`compact_locked()` path that runs on worker threads in PM.
- Evidence (MEASURED, run 6): PM, 3 threads, p = 2·10⁴, k = 8 (floor binding): increment **226–258 MiB vs plan
  205 MiB** (4 runs). Two causes, each measured:
  1. **glibc per-thread arenas.**
     - In PM, the serial compaction runs on whichever worker flushes. The old and new kept runs and the staging growth
       are allocated in different thread arenas, and freed memory stays resident in its arena.
     - With `MALLOC_ARENA_MAX=1`, the same run peaks at 163 MiB (+25.6 %).
  2. **Staging overshoot.**
     - `reserve_staging` reserves exactly `stage_limit` (serial). But one `flush()` appends up to `buf_limit` = 65,536
       entries before the limit check (`store.h:188`), so the reserved vectors reallocate to 2× once per cycle.
     - The serial term in the plan was cut to `s·e` (it was `1.5·pow2(s)·e`) on the assumption of no reallocation.
     - A reviewer-local patch (`n = limit + buf_limit`, not pushed) lowered the PM peak by ≈ 25 MiB (233/226 vs 257/258).
- The label-major kernel holds everywhere (11 rows, +5.9 to +29.7 %), and so does PM at 1 thread and at 10⁵ (where
  k = 16 adds slack).
- Impact:
  - The admission can under-predict theory-mode (PM, bit form) islands at 2·10⁴-like sizes by about 20 %.
  - The V-1M class-A label-major path is not affected.
  - INTERFACES §7 states the plan is an upper bound, without a kernel restriction.
- Fix:
  - reserve `limit + buf_limit` in serial mode;
  - and either cap the arenas at island start (`mallopt(M_ARENA_MAX, 2)` or `MALLOC_ARENA_MAX` in the job env), or add a
    PM slack of (T − 1) × the serial compaction transient;
  - add a PM row at 3 threads to `mem_plan_bounds_measured_peak_2e4`.

**m2. r1 requires k_store at p ≥ 10⁵ for every island, including calibration islands, and without a memory budget.**
- Where: `island_impl.h:1053`.
- The check fires even when `mem_budget == 0`.
- Calibration islands (option `leaders`, WP4 tiers) at p ≥ 10⁵ run before `calib.bin` exists, so they have no measured
  k_store. Their only way through is `k_store_optional`, which is documented as tests and bench only.
- INTERFACES v0.1.10 §7 still reads "uses calibration's measured mean |S| **when it is given**". The tightening is not
  in the contract.
- No production caller exists yet (no CLI or WP4 call of `run_island`), so this is latent.
- Fix (one of):
  - require k_store only when `mem_budget > 0 && !cfg.leaders`;
  - or give calibration a sanctioned value (for example the pilot's measured mean) and ask WP1 for a v0.1.11 §7 line.

**m3. The phase-B wave bound gives about 1.3 tiles per thread per wave at 10⁶, G = 256, 96 threads.** (ESTIMATE)
- Where: `island_impl.h:540`, `wave = min(max(64, 16·NT), (c/10)/(nsup·Bk))`.
- At p = 10⁶: c/10 = 4·10⁶ and nsup·Bk ≤ 256·128.
  - G = 256: wave = **122 tiles**, against 1,536 before, with about 64 waves (barriers) per pass.
  - G = 64: 488 tiles.
- With dynamic scheduling, 122 tasks on 96 threads finish in 2 task-times against a mean of 1.27, so phase B runs at
  ≤ 64 % efficiency.
- Phase B was 1.9 s of the 29.1 s round (WP3_LEVERS_SPR). The likely cost is +0.5–1 s per late round. This is not in
  the PR's "29.1 → ≈ 21.7 s" ESTIMATE.
- The bound is a worst case: every consumed pair offered. Most pairs fall below τ or are filtered as duplicates.
- Fix:
  - check `staged()` every k tiles inside a larger wave, or size the wave from the measured offer rate of the previous
    pass; or keep the bound but at least `4·NT` tiles;
  - in any case, read the `[round]` phase-B seconds in the next SPR batch.

### Nits
- **n1.** `psort_noalloc`'s comment says "equivalent elements are identical in content". For `by_model` this holds only
  because the hash is a function of S (Zobrist). State that, and add a `StoreRef` case to the unit test. The current one
  sorts `uint64_t` only. Run 5 shows the failure mode when the precondition is broken.
- **n2.** `nots_guard.sh` accepts any TMPDIR under the department roots. PROTOCOL §7 asks for
  `scratch/tmp/$SLURM_JOB_ID`, and the guard creates TMPDIR without removing it. Consider requiring
  `…/scratch/tmp/*` (or `$SLURM_JOB_ID` in the path) and an EXIT trap that removes a TMPDIR the script created.
- **n3.** `bench plan` prints "GB" for values in GiB (`/ 2^30`, `bench_island.cpp:250`). With `V4_K_STORE=0` the bench
  prints "k_store absent (pi_0 plan)" and is then refused. The refusal is correct; the message is misleading.
- **n4.** `draw_order` copies the uninitialised `jnext` into `jcur` after the last block (`island_impl.h:291`). It is
  never read, so this is harmless, but `if (d0 + 8 < nd)` around the copy would be cleaner.

## Other checks
- Discipline:
  - all changes are under `engine_v4/`, and `core/` is untouched;
  - there are no large files and no hard-coded user paths;
  - the department roots are `$HOME/…` and `/scratch/fb31/…`, as in the rules.
- Fingerprint and checkpoint:
  - The new fields (`k_store_optional`, `test_admission_k`, `test_oom_merge`, `products_block`) are admission-only, test
    hooks or execution parameters.
  - None enters the law, and the hashes are unchanged.
- The 10⁶ plan numbers in the PR body reproduce exactly (run 7). The L5 per-call timings were not re-measured. They are
  labelled MEASURED (Owls, 1 thread) by the author, and only exactness was in scope here.
