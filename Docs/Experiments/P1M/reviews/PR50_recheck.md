# PR #50 re-check (WP2 D-31, stacked on #13) — head 5f2b4777 (`git diff c303164e 5f2b4777`, 10 files)

Reviewer: independent re-check, read only, own worktree, scratch/TMPDIR/P1M_TEST_ROOT under `.rc_tmp/`, nothing deleted or pushed.
First review: `reviews/PR50_review.md` (REJECT: 2 MAJOR, 1 MINOR).

## Verdict: **MERGE** (after #13; retarget to `exp/P1M-engine`). 0 CRITICAL, 0 MAJOR, 0 open MINOR from the first review. One merge precondition (process, not code): WP1 must adopt the INTERFACES change (see F1).

## Test runs (MEASURED, Owls, GCC 11.5.0, nice 19, taskset 3 cores)
| run | result |
|---|---|
| clean build of 5f2b4777 (`smcbvs4 v4_tests v4_setup_bench v4_pmath_check`) | no warnings |
| `v4_tests` (all C++ cases, quick) | **146 test cases, 0 failed, 0 check failures** (`.rc_tmp/quick50.log`). The R / WP4 golden / WP5 stages of `run_tests.sh` are untouched by this diff and I did not re-run them |
| row-equality test `d31_cond_row_scan_table` | PASS: AR, IND, BLK, TIE × n ∈ {100, 400}, p = 1,200; 6,171–23,316 rows per case, ≈ 4.4 M u values, 4,000 Philox draws each |
| `--full golden_G3to7_tables_stores_start_draws_mode_full` (20,000 draws × 42 fixtures vs core) | **PASS, 0 failed, 0 check failures**, 122.8 s (`.rc_tmp/golden50.log`) |
| `d31_pi0_draw_allocation_free`, `d31_accounting_includes_cond0` | PASS |
| my own probe (`.rc_tmp/probe50.cpp`, global `operator new`/`new[]` counter; AR n = 200, p = 3,000 setup.bin from the CLI; J = 228, K = 100) | see MAJOR-1 |
| my own accounting reconstruction (`v4_setup_bench acct` on synthetic and 10⁶ records) | see MAJOR-2 and MINOR |

## MAJOR-1 (heap allocation in the π₀ draw): **FIXED**
Code (`start.cpp`, `tables.cpp`, `setup.h`):
- `cond_row` / `pi0_block_size` use `CondScratch` (fixed 17 entries: `lj`, long-double `e`, `row`): no heap. `cumulative_from_logs(lp, n, c, e)` keeps the arithmetic of the old function (same max / `expl` / long-double sums / division / last-positive-mass order); `cond_row` builds `pr[j] + Fb[r−j]` in ascending j as core/v3_start.h:145-147 (single add; `-ffp-contract=off`). Length is checked ≤ 17.
- The sub-model path moved to `DrawScratch` (`lv`, `sc`, `e` of 12,870 = C(16,8), plus the block list); `DrawScratch(K)` is built before the region and warms the static code tables.
- The 3-argument `Start::draw_pi0` keeps a `thread_local DrawScratch` (one-time allocation per thread). It is called only from tests and bench tools: the production island code uses `island::dep::draw_pi0` on `dep::Start` (`island_run.h`, `island_pm.h`), so no production parallel region hits it. It is documented in the header.
Measured by my probe, 3 OpenMP threads, scratch built and team created before arming, counter armed from the first draw:
- scratch-form draws: **60,000 draws, 0 allocations, 0 bytes**;
- `pi0_block_size`: **137,712 calls (u = 0, cond0 ± 1 ulp, cond0, 1−ε, random) over every (b, r), 0 allocations**, 0 mismatches against the stored-row form;
- draws equal the stored-row form: **0 mismatches in 60,000**;
- 3-argument form: first use in a region = 8 allocations / 825,296 bytes in total, one-time (3 threads); second pass: 0 allocations.
The first review's repro (30,000 calls → 30,000 allocations) is gone. The in-tree test counts every `operator new` on all threads from the first call (AR, BLK, TIE; 9,000 draws and 40–48 k block-size calls each) and has a self-check of the counter.

## MAJOR-2 (cond0 missing from the stage peaks): **FIXED**
- `account.cpp`: `start_law` = all `data` + all `persistent` items; `start_mode` = those + the `mode` transient. Selected by stage, not by display name. I compared with the old name list: it was the same set plus the renamed item, so only `cond0` re-enters.
- Reproduced the first review's counterexamples with `v4_setup_bench acct`: singleton blocks, n = p = J = 1,000, K = 500: overall estimated peak **21,915,472** (the review's corrected figure; it was 17,907,472), cond0 item 4,008,000 B. n = 200, J = 100 blocks of 14: `start_law` stage = sum of data + persistent items exactly (25,325,222 B), cond0 = 80,800 B included.
- `d31_accounting_includes_cond0` checks stage = live set, peak ≥ live set, and the admission boundary on the accounted peak (budget 1e-6 below → `resource_limit` "admission:", 1e-6 above → completed, peak deterministic). The array-size assertion is no longer the only check.
- The admission in `run_setup` uses `acc.peak`, so the fixed totals reach the budget check; `count_only` uses the same `account()`.

## MINOR (PR text vs accounting): **FIXED**
The PR text now says the table stage becomes the limiting stage and the overall peak falls by less than the retained size. I recomputed three rows at p = 10⁶ from the histograms in `WP2_COUNTS_1e6.md` (edges as recorded, `nb_nnz` unknown so the bound is used; the difference is ≈ 0.1 GB):
| row | PR text | my recomputation |
|---|---|---|
| AR n = 200 | peak 14.1 (tables), bound 20.3, setup.bin 10.3, start_law 12.0 | 14.11 (tables), 20.27, 10.31, 11.95 |
| AR n = 1,000 | peak 19.1 (tables), bound 25.2, setup.bin 9.4, start_law 17.4 | 19.08 (tables), 25.24, 9.38, 17.43 |
| IND n = 1,000 | peak 22.7, bound 29.5, setup.bin 12.9, start_law 21.0 | 22.66, 29.45, 12.91, 20.96 |
The "setup.bin falls by up to 4.2 GB at n = 1,000" and "peak falls 2.9–3.0 GB at n = 1,000, unchanged at n ≤ 400" statements are consistent with these. The PR flags BLK n = 1,000 as pending and labels the µs/draw table as measured before the scratch change.

## Other checks
- Bits: `cond0` entry = entry 0 of the core row; shortcut is strict `u < cond0`, so equality falls to `upper_bound`; the stored-row (tests-only) path is preserved. Row bits, draws and uniform consumption equal core in G5/G6 (quick and 20,000-draw full) and in my probe.
- `setup.bin`: `cond0` J × (K+1) written, size checked on read; an old file without `cond0` is refused. Round-trip and loader tests updated (the `island::dep::Start` loader rebuilds full rows with `cond_row`, same bits).
- Scope: 10 files, all under `engine_v4/`; no large files. No production consumer of the removed sections remains in `src/`/`tools/` (remaining mentions are `dep::Start`'s own rows and WP3_DESIGN text).

## Findings (new)
- **F1 (MINOR, merge-order, process).** `INTERFACES.md` §2 (line 87) and §5.1 (line 312 in the tree; line 336 in the authoritative copy) still name `cond_ptr/cond_cum` as setup.bin sections. This PR writes `cond0` instead. The PR correctly leaves the contract to the WP1 owner and gives the wording; the change (with a changelog line, in both the authoritative document and the engine copy) must land with or before the merge. WP3_DESIGN §1.12 (lines 352-363) also still plans to read `cond_ptr/cond_cum`.
- **F2 (MINOR, expectation).** As the first reviewer noted and the PR accepts: the island and calibration loaders still rebuild full rows (`dep::Start`, `setup_load.h`, `calib_run.cpp`). D-31's "no island touches the full table" is not delivered until WP3's StartView lands; no island memory or speed gain should be attributed to this PR.
- **F3 (NIT).** The 3-argument `draw_pi0`'s `thread_local` scratch sizes its block list with the first `K` it sees; a later `Start` with a larger K only costs a reallocation (correct, not allocation-free). Production callers use the scratch form, so no action beyond the header comment.
- **F4 (NIT).** The p = 10⁵ µs/draw table in the PR text predates the scratch change; at p = 10⁴ the first reviewer measured 43.9 vs 65.2 µs/draw (scan + recompute vs stored rows). Re-measure when the PR text is next updated.
