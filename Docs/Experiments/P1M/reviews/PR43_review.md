# PR #43 review — WP3 m3: compaction-sort merge rounds on all threads (merge-path segments), same bits; `[round]` compaction counters

Reviewer: independent (Opus 5.5, high), 2026-11-16.
- **Final head: 8d584649** = e8415a93 (fix) + 5c423dfb (WP3_DESIGN §1.10b) + the merges 0901418d / 8d584649 of
  `exp/P1M-wp3-split` (#42 at 4cb0ebc2, which contains #39 at fcdcd2c0).
- `git diff 4cb0ebc2 8d584649` is exactly the m3 change: `store.h`, `island_run.h` (the `[round]` line),
  `test_island.cpp`, `bench_island.cpp` and WP3_DESIGN.

## Verdict: **MERGE** (ACCEPT)

- **Same bits:** the T3 hashes and the island output hash are unchanged, and the 938-run probe matches `std::sort`
  up to 192 threads.
- **No allocation inside a region:** verified.
- **The measured Owls numbers reproduce within noise.**
- **Counts: 0 CRITICAL, 0 MAJOR, 2 MINOR** (+ 2 INFO). Neither MINOR blocks the merge.

## The change (`include/v4/island/store.h:41-85`)
- `psort_noalloc` keeps its structure: C = threads chunks sorted with `std::sort`, then log2 C merge rounds that
  ping-pong between `a` and the caller's `tmp`.
- In each round, each pair (A = chunks [2wq, 2wq + w), B = the next w chunks) is cut into
  S = ⌈C / npairs⌉ output segments [d0, d1).
- `merge_path_split(A, B, d)` binary-searches the number i of A-elements among the first d outputs of the stable
  merge. Each segment is `std::merge(A[i0, i1), B[d0 − i0, d1 − i1)) → dst[lo + d0 …]`.
- The final copy back is parallel by chunk.
- `compact_parallel` times both sorts (`t_sort`). The verbose `[round]` line adds the compaction count and the sort
  seconds of the round.

## Correctness (by inspection)
- **The split.**
  - The search range is `lo = max(0, d − nb)`, `hi = min(d, na)`.
  - The predicate `!less(B[d−1−mid], A[mid])` means "A[mid] precedes B[d−1−mid] in the stable merge (A first on
    ties)", which is the standard merge-path diagonal search.
  - Every index is in range: mid < na; 0 ≤ d−1−mid ≤ nb−1, because mid ≥ d − nb and mid ≤ d − 1.
  - `std::merge` takes from the first range on ties (it takes B only when `less(*b, *a)`), which is the same rule.
  - Splits are monotone in d (i0 ≤ i1, j0 ≤ j1). So the segments tile the pair's output and each produces exactly
    the global merge's elements d0..d1 in order.
- **Degenerate pairs.**
  - A lone chunk (B empty: nb = 0) gives split = d, a plain copy.
  - Pairs past C are empty (lo = mid = hi = n).
  - nt·sg fits easily in `size_t`.
- **No allocation inside a region.**
  - `b` and `tmp` are sized before any `parallel`.
  - The region bodies call only `std::sort`, `std::merge`, `std::copy` and the search, none of which allocates.
  - Measured below with a counting `operator new`.
- **Determinism.** Both comparators of `compact_parallel` are total on content (by model: hash, |S|, S, then v
  descending; store order), so the sorted sequence is unique. Stability matters only for equivalent elements, which
  are identical in content (equal v, model and hash; possibly distinct pool pointers to equal content, as before).
- **Counters.** `t_sort` is reset in `init`. `merges_prev` / `sort_prev` are per-engine deltas, and the change is
  verbose-only.

## Tests (Owls, Xeon Gold 6148, gcc 11.5, `nice -n 19`, ≤ 3 cores)
All runs used a fresh `git archive` of 8d584649, which is the whole stack (#39 fcdcd2c0 + #42 + #43), under
`TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/20261116-review-39-43/t43`.

1. **`tests/run_tests.sh --threads 3` (quick).**
   - v4_tests: **115 test cases, 0 failed, 0 check failures.** That is the 114 plus #39's
     `calibration_admission_n1_rule`.
     - `oom_in_parallel_compaction_is_resource_limit` passes, including the new psort-vs-`std::sort` matrix
       (n ∈ {4100, 20011}, threads ∈ {1, 2, 3, 4, 5, 7, 8}).
     - T3 hashes are unchanged on all 16 kernel / thread / G / tile rows: bit `44a15bfc6fb8d233`, A
       `d2df149413596a19`.
     - Every island golden vs core passes: final, compat, and calibration compat / law / failure prefix.
   - WP5: driver 17 OK; competitor harness OK; install script 23 checks OK.
   - The suite's WP4 R golden was killed at case 4 of 6 by a T3 server restart (0 failures until then). I re-ran it
     alone on the same tree: **WP4 golden 528,081 checks, 0 failures**. The six `runner = "wp3"` calibrations
     equal `v3_calibrate` (4,855 / 6,134 / 5,996 / 17,524 / 8,660 / 41,314 checks).
2. **Reviewer probe** (`psort_noalloc` from this head's `store.h`; `-O2 -fopenmp -ffp-contract=off`; pinned with
   `taskset` to 3 CPUs, so the high thread counts are oversubscribed on 3 cores).
   - **Sizes:** n ∈ {4095, 4096, 4097, 4100, 5000, 8191, 20011, 65536, 100003, 1000003}.
   - **Keys:** 4 distributions (random 64-bit; 7 distinct keys; 5,000 distinct; all equal). Ties are broken by a
     payload, so the comparator is total; one reverse-sorted input.
   - **Threads:** 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 16, 17, 31, 32, 33, 47, 48, 64, 95, 96, 97, 128, 192.
     At n = 10⁶, threads > 32 are run only at 96.
   - **Checks:**
     - the result equals `std::sort` element by element;
     - a counting global `operator new` sees **0 allocations while `omp_in_parallel()`** and at most 1 per call (the
       chunk-boundary vector, before any region);
     - 5 repetitions at 3 and 96 threads on n = 300,007 give the same sequence.
   - **Result: 938 runs, 0 failures.**
3. **Sort bench** (`v4_bench_island sort <n> <T>`, best of 3, wall; MEASURED, Owls, `taskset` 3 CPUs). Output is
   identical in all variants.

   | n | threads | pairwise (PR26) | merge-path (m3) | `__gnu_parallel` | PR claim (pairwise / m3 / gnu) |
   |---|---|---|---|---|---|
   | 1.5 M | 3 | 0.129 s | 0.088 s | 0.076 s | 0.115 / 0.091 / 0.085 |
   | 6 M | 3 | 0.562 s | 0.397 s | 0.393 s | 0.590 / 0.419 / 0.453 |
   | 1.5 M | 96 (on 3 CPUs) | 0.175 s | 0.116 s | 0.106 s | — |

   The 96-thread row is oversubscribed and shows only that the 96-way segmentation adds no overhead and gives the
   same bits. The SPR batch must measure the real 96-thread gain.
4. **Island bench**, the PR's command (`V4_VERBOSE=1 v4_bench_island island 100000 500 3 A lm 256 128 steps:1 2 1`,
   `taskset` 3 CPUs): MEASURED here, m3 build only.

   | | this run | PR (m3 row) |
   |---|---|---|
   | output hash | **`bab293252e9ebe57`** | the same |
   | store merges | **33** | 33 |
   | compaction | **15.69 s** | 16.38 s |
   | phase B | **19.09 s** | 19.97 s |
   | island wall | **592.6 s** | 625.7 s |
   | sorts | **4.18 s** | 4.3 s |

   - The new `[round]` fields read 21 + 8 + 3 + 1 = 33 compactions, consistent with the run total; sorts per step
     were 2.51 + 1.25 + 0.34 + 0.08 s.
   - I did not re-run the pre-L5 / engine builds. On a shared host (load ≈ 23), the before/after difference at
     3 threads (≈ 2.7 s of compaction) is within run-to-run noise. The sort bench (item 3) is the clean comparison.

## Findings
### MINOR-1 — segments are equal per pair, not per output: rounds with unequal pairs leave threads idle (`store.h:68-77`)
- `S = ⌈C / npairs⌉` segments are given to every pair whatever its size, with `schedule(static, 1)`.
- When the pairs differ in size (C not a power of two: a lone or short last pair), the critical path is longer than
  n / C.
  - **C = 3, round 1:** tasks of n/3, n/3, n/6, n/6 elements on 3 threads. Thread 0 gets n/3 + n/6 = **n/2** (1.5×
    the ideal n/3).
  - **C = 96, the width-32 round:** pair 0 holds 2n/3 elements in 48 segments of n/72; the lone pair 1 copies n/3
    in 48 segments of n/144. The critical path is **n/72**, 1.33× the ideal n/96.
- The other C = 96 rounds are balanced.
- It costs a few percent of the sort and does not change bits.
- **Fix (optional):** cut the round's whole output [0, n) into C global segments, task t covering
  [n·t/C, n·(t+1)/C) and mapped to its pair, or give each pair a segment count proportional to its size.

### MINOR-2 — the unit test does not reach the production thread counts
- `oom_in_parallel_compaction_is_resource_limit` checks threads ≤ 8 with `uint64_t` / `std::less`.
- **Fix:** add threads {16, 33, 64, 96} (oversubscribed, but correctness only, cheap at n = 20,011), n = 4096 (the
  first parallel size) and one all-equal-key input with a tie-breaking payload. My probe (above) shows that these
  pass today; the point is to keep them passing when builder 7 touches `store.h`.

### INFO
- **I-1** `t_sort` times only the two sorts of `compact_parallel`. The serial `compact_locked` path (particle-major
  islands, the leader stores) uses `std::sort` untimed, so `[round] … sorts` reads 0 there. A note in the field's
  comment would help when reading particle-major or calibration logs.
- **I-2** The "≈ 27× shorter critical path at 96 threads" in WP3_DESIGN §1.10b is an ESTIMATE that assumes balanced
  rounds. With MINOR-1 it is ≈ 25×. Only the SPR batch can confirm the 96-thread gain; the 3-core
  oversubscribed run here confirms correctness, not speed.
