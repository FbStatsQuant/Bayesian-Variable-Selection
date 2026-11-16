# PR #43 review — WP3 m3: compaction-sort merge rounds on all threads (merge-path segments), same bits; `[round]` compaction counters

Reviewer: independent (Opus 5.5, high), 2026-11-16.
- **Final head: 8d584649** = e8415a93 (fix) + 5c423dfb (WP3_DESIGN §1.10b) + the merges 0901418d / 8d584649 of
  `exp/P1M-wp3-split` (#42 at 4cb0ebc2, which contains #39 at fcdcd2c0).
- `git diff 4cb0ebc2 8d584649` is exactly the m3 change: `store.h`, `island_run.h` (the `[round]` line),
  `test_island.cpp`, `bench_island.cpp` and WP3_DESIGN.

## Verdict: VERDICT

COUNTS

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

## Tests
TESTS

## Findings
FINDINGS
