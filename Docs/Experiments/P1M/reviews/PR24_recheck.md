# PR #24 re-check: WP3 slice 2 review fixes (P1 leaders in label-major, P2 memory plan as an upper bound, minors)

Reviewer: Opus 5.5 (high), independent of the author. Date: 2026-11-16.
- Branch: `exp/P1M-wp3-island3` @ `9466489d`; base `exp/P1M-wp3-island2` (#21, merged into `exp/P1M-engine`).
- Re-checked diff: `2f6b629f..9466489d`, 7 files, +293/−86. First review: `PR24_review.md` (2 MAJOR, 6 MINOR, 4 nits).
- Read-only: detached worktrees in `/home/fb31/SMC_Engineering_Department/tmp/20261116-review-24-26` (removed after).
  Nothing was pushed or commented.

## Verdict: **MERGE**

- **P1 is fixed.** Label-major leaders equal particle-major leaders. This holds in the PR's test and in a harder reviewer
  check, where a top-store cap of 30 forces the cut-off path that the old code got wrong.
- **P2 is fixed for the cases that can be measured.** The plan is above the measured peak in every case at 10⁵.
  - The tightest case is G = 64, no leaders: **plan 1,336 MiB, measured increment 1,197 MiB** (reviewer; the PR reports
    1,238). The plan is the larger number, so there is no MAJOR.
  - The margin is about 10 %, and it is measured at 3 threads only.
- **All minors are addressed.**
- **Tests: 69 of 69 pass** (gcc 11.5, Owls). The T3 hashes are unchanged.
- **New findings:** 3 MINOR and 3 nits. None blocks the merge.

Counts: CRITICAL 0 · MAJOR 0 · MINOR 3 · nits 3.

## Test runs (Owls, Xeon Gold 6148, load 21–30, gcc 11.5.0, `nice -n 19`, ≤ 3 threads)
1. **`tests/run_tests.sh --build-dir …/b3`** (quick): **69 test cases, 0 failed, 0 check failures**, exit 0.
   `git_commit` = `9466489d…`.
   - T3: bit `44a15bfc6fb8d233`, A `d2df149413596a19` (unchanged), over PM/LM, threads 1–3, G and tile.
   - `leaders_label_major_equal_particle_major`: lead0/lead1 6,000/6,000 (full at 20p), LM = PM in both forms.
   - `golden_compat_island_vs_core_serial_stream` variant 2: 357 Gibbs steps at the cap (m6).
   - `store_snapshots_released`: max 2 kept runs (m4).
   - `mem_plan_bounds_measured_peak_2e4`: 201/314, 357/534, 338/422, 467/643 MiB.
2. **Leaders, harder case** (reviewer driver `chk/leadchk.cpp`, linked to the PR's libs):
   - Setup: p ∈ {60, 300}, `store_cap` ∈ {default, **30**}, both arithmetic forms. PM runs with 1 thread; LM runs with
     3 threads and G = 16.
   - With cap 30, the top store's τ binds from the first stage. The leaders (cap 20p) fill completely (1,200 and 6,000
     entries).
   - Result: **8 of 8 configurations match exactly**: lead0/lead1 values (bits) and pools, and the output hash.
3. **Memory plan vs measured peak at p = 10⁵** (reviewer driver `chk/memrun.cpp`):
   - Method: **one fresh process per configuration**, so no heap is retained from an earlier island. Fixture n = 200,
     seed 36. `malloc_trim(0)` and `clear_refs 5` after the data are built. LM, 3 threads, N = 500, grid 0/0.3/0.7/1,
     L = 0, Hm = 1, class A.
   - "Increment" is the island's VmHWM increment. The plan is `island_memory` at the true stored mean |S|, without the
     inputs term (the same convention as the PR's test). MaxRSS is the whole process, from `/usr/bin/time -v`.

   | G | leaders | k (true) | measured increment | **plan** | margin | process MaxRSS |
   |---|---|---|---|---|---|---|
   | 64 | no | 6.03 | **1,197 MiB** (1,204 without trim) | **1,336 MiB** | +11.6 % | 1,579 MiB |
   | 64 | yes | 14.04 | 1,887 | 3,218 | +71 % | 2,269 |
   | 256 | no | 6.03 | 1,614 | 1,793 | +11.1 % | 1,996 |
   | 256 | yes | 14.04 | 2,279 | 3,704 | +63 % | 2,661 |

   - Store full in every run: 4,000,001 entries, 25–28 merges, 0 serial fallbacks, status 0.
   - MEASURED. **The bound holds in all four.**
   - The PR's own figures (1,238/1,336; 1,505/1,793) agree to within 3–7 %.
   - The leader cases are loose because one k (the maximum over the three stores, which is lead0's 14.0) prices all
     three stores.

## Re-check of the first review's findings

| # | Finding | Status | Evidence |
|---|---|---|---|
| P1 | Leaders wrong under LM | **Fixed** | `island_impl.h:559-563` (details below). Test plus reviewer check 2. |
| P2 | Plan not an upper bound | **Fixed (≤ 10⁵, 3 threads)** | `memory.h` (details below). Reviewer check 3. |
| m1 | Step refusal untested, store content | **Fixed** | `mem_budget_admission` (4) forces it with `k_store = 0.5` (details below). |
| m2 | Admission depends on threads | **Documented** | WP3_DESIGN §1.8; `memory.h` header. |
| m3 | PM defers to c/2 | **Fixed** | `defer` only for LM (`:177`); PM drops a stale snapshot per particle (`:270`). |
| m4 | `kept_live` counts empty Kept | **Fixed** | `Kept::count_live()` only once the run holds entries; test asserts ≤ 3 (measured 2). |
| m5 | Compaction test bypasses `offer()` | **Fixed** | `store_offer_path_fallbacks_and_parallel` (details below). |
| m6 | Compat golden: no cap or fallback | **Fixed / argued** | Variant n = 12 (K = 6) reaches the cap 357 times. The fallback routes are unreachable for finite data (WP3_DESIGN §1.8). I accept the argument. |
| n1 (#21) | OOM in a parallel region aborts | **Mostly fixed** | `oom_guard` (details below). One hole remains: r2. |
| nits | | Fixed | Leaders moved, not copied. `rb_d` only in compat. |

**P1 (`island_impl.h:559-563`).**
- lg0 = `prior_{del,add} + comp_{del,add}(st, c, j)`.
- `comp_add`/`comp_del` (`kernel.h:63-79`) start from `bpre[m]`, a running prefix built from 0.0 in increasing block
  order (`kernel.h:122,127`). They then add the changed block's `lr` and the remaining `bterm`s, again in increasing
  block order. This is the same sequence of additions as `Start::comp` (`dep.h:81-93`: s = 0, then += `logr[b][code]`
  over sorted blocks), and an emptied block is skipped in both. So the result has the same bits as PM's
  `logprior[|T|] + st.comp(T)` (`:294`).
- Phase-B offers go to the leaders when `lg0 ≥ lead0.τ || F ≥ lead1.τ`, independently of the top store's shortcut.
  Each store's `offer()` applies its own τ. NaN is refused.

**P2 (`memory.h`).**
- New terms: sort temporaries (64 B per staged entry), staging at pow2 × 1.5, pool over-reservation, a second index,
  one stale generation, leaders, worker buffers per store, `rb_round`/compat, support caches, and inputs.
- Admission uses `k_store` when it is given. The step re-check uses the exact pool once the store is full.

**m1 (step refusal).**
- `mem_budget_admission` (4) forces the refusal with `k_store = 0.5`.
- It checks status 3, a reason containing "after step", no store and no RB, and a file with `resource_limit`, 0 entries,
  no `logZ` and no `terminal_S`.
- `res.status == 0 || 1` gates the store (`:939`).

**m5 (offer path).**
- `store_offer_path_fallbacks_and_parallel` goes through `offer()`, with the filter active and stale snapshots.
- Serial fallbacks (3 and 13) are interleaved with parallel compactions, and the content equals WP1's `v4::Store`.

**n1 (OOM).**
- `oom_guard` wraps every LM region body. PM, walk and initial draws catch `bad_alloc`, ranked `UINT32_MAX` so that a
  numerical failure in the same round wins.
- `fail_fatal()` returns after each region. `run()` maps a `resource_limit` Error or `bad_alloc` to status 3.
- Test `oom_in_region_is_resource_limit` covers PM and LM at 1 and 3 threads.

**Regression check of the fixes:**
- Leader snapshot release at tile start (`:526-530`) and in `sync_ledgers` (`:656`), and the leaders' NaN check (`:657`).
- `rb_d` only when `csrc`.
- The defer change does not touch the LM path.
- The T3 and golden hashes are unchanged.
- The fingerprint and checkpoint are unchanged (new config fields: `k_store` and `inputs_bytes` are admission-only;
  `test_oom_pass` is a test hook).

No regression found.

## New findings

### MINOR

**r1. Without `k_store`, the admission at 10⁶ refuses every realistic budget (the π₀ estimate scales with p).**
- Where: `island_impl.h` `run_island`, `k_est = max(8, 2·E_π₀|S| + 2)` when `k_store == 0`. The step re-check before
  the store is full uses `max(kk, k_est)`, which has the same effect.
- Evidence: for the stand-in π₀ (AR(0.6), blocks of 4), E|S| grows with p. MEASURED, `chk/ek.cpp` (data seed 2026,
  except the 10⁶ row):

  | p | E\|S\| | k_est |
  |---|---|---|
  | 10⁵ | 16.9 | 35.8 |
  | 2·10⁵ | 36.1 | 74.3 |
  | 10⁶ (data seed 7) | 38.6 | 79.2 |

- The bench's 10⁶ island prints `k = 114.29` and a plan of **99,491 MiB** (MEASURED; see PR26_review B1).
- At k ≈ 7 (the stored size measured in job 2748105), the plan is 17.1 GiB for G = 64 and 21.7 GiB for G = 256.
- `G = 0` (auto) would walk G down to 1 and still refuse, because the store term alone is ≈ 88 GiB at k = 114.
- Impact: none on outputs. But `--mem-budget` is unusable at 10⁶ unless the caller passes `k_store`, and today only
  calibration can measure it.
- Fix: make `k_store` mandatory whenever `mem_budget` is set and p > 10⁵ (`invalid_input` otherwise), or cap the π₀
  fallback, for example `min(k_est, K)` priced as a mean with an explicit ESTIMATE label. Record this in the requested
  INTERFACES §7 note (v0.1.10) together with `inputs_bytes`.

**r2. Out of memory inside `__gnu_parallel::sort` still terminates the process.**
- Where: `store.h` `compact_parallel`, two `__gnu_parallel::sort` calls (`:232` and `:245`).
- libstdc++'s multiway mergesort allocates its temporary copy (s × 32 B, the largest single transient of a compaction)
  **inside its own OpenMP region**. A `bad_alloc` there cannot reach `run()`'s handler, so the result is
  `std::terminate`, not `resource_limit`.
- The other compaction regions only write into vectors sized outside the regions. They are fine.
- Fix:
  - preallocate the sort buffer outside the region and use a sort that takes it (or a two-pass sort of runs plus the
    existing merge-path merge); or
  - document that a compaction OOM aborts, and rely on the admission. The admission is now an upper bound (≤ 10⁵), so
    this is a rare path.

**r3. The bound is validated only at 3 threads and ≤ 10⁵, with a 10–12 % margin. The setup tables sit outside the plan unless `inputs_bytes` is set.**
- At 96 threads, the per-thread terms (worker buffers, product tiles, scratch) and glibc's per-thread arenas (up to
  8 × cores, with fragmentation that is not modelled) are untested.
- With `inputs_bytes = 0`, as in the bench and the PR's test, the whole process exceeds `plan.total`.
  - G = 64: MaxRSS 1,579 MiB vs plan total 1,490 MiB.
  - The difference is the ≈ 228 MiB of Start/neighbour tables, which belong to `inputs_bytes`.
  - The test checks only the increment, so it cannot catch a caller that forgets `inputs_bytes`.
- Fix:
  - Have the CLI (WP2/WP4) set `inputs_bytes` from the mapped sections, and add one test that compares the **whole
    process's** VmHWM with `plan.total` when `inputs_bytes` is set.
  - Compare the 10⁶ plan (17.1 GiB at k = 7, G = 64, 96 threads) with the NOTS lever batch's MaxRSS before the island
    memory request is fixed.

### Nits
- `memory.h` prices every store (top, lead0, lead1) at one k: the test passes the maximum over the three stores. The
  leader cases are therefore 63–71 % conservative. Per-store k (top k_store, leaders measured) would tighten them.
- The plan's 10⁶ example ("≈ 17.5 GiB", WP3_DESIGN §1.8) uses Hm = 4. With the bench's Hm = 2 it is 17.1 GiB. State Hm.
- `plan_bounds_peak` runs four islands in one process. Later baselines include heap retained from earlier islands, so
  their increments can understate. My one-process-per-configuration numbers agree here (within 3–7 %), but a fork per
  configuration, or `malloc_trim(0)` before `clear_refs`, would make the test robust.

## Discipline
- All changes are under `engine_v4/`, and `core/` is untouched.
- No hard-coded paths, no large files.
- MEASURED and ESTIMATE labels are present in the PR body and in WP3_DESIGN §1.8.
- Reviewer temporary files were kept only under the department tmp folder and removed after.
