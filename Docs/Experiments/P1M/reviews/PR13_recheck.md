# PR #13 re-check (WP2 setup) — head c303164e, base exp/P1M-engine

Reviewer: independent re-check, read only, own worktree (detached checkout), scratch/TMPDIR/P1M_TEST_ROOT under `.rc_tmp/`, nothing deleted, nothing pushed.
First review: `reviews/PR13_review.md` (ACCEPT-WITH-FIXES, 0 CRITICAL / 2 MAJOR / 9 MINOR). Dispositions: `reviews/PR13_disposition.md`.

## Verdict: **MERGE** (0 CRITICAL, 0 MAJOR, 0 open MINOR of the first review; 5 new NITs, none blocking)

## Test runs (MEASURED, Owls, Xeon Gold 6148, GCC 11.5.0, nice 19, ≤ 3 cores)
| run | result |
|---|---|
| `tests/run_tests.sh --quick --threads 3 --keep` at c303164e (clean build, no warnings) | **143 test cases, 0 failed, 0 check failures**; WP5 Slurm driver 17 tests OK; competitor harness OK; install-script guards 9 checks OK; WP4 R golden 528,081 checks, 0 failures; runner exit 0 (`.rc_tmp/quick13.log`) |
| `v4_tests --full T11_truncated_equals_exact_below_cut_full` | PASS (573 s): AR/BLK/IND/TIE p = 20,000, AR strict, AR n = 400 p = 10,000 |
| `--full golden_G1_neighbour_graph_full` | PASS (39 s) |
| `--full golden_G2_exact_partition_full` | PASS (15 s) |
| `--full golden_G3to7_tables_stores_start_draws_mode_full` | PASS (80 s) |
| merge into current base | `git merge-tree` with `origin/exp/P1M-engine` (82e985eb): clean; GitHub `mergeable: MERGEABLE`. (I did not build the merged tree.) |
| discipline | diff vs merge-base 544e38f9 touches only `Scripts/SMC_BVS/engine_v4/`; no file added over 50 MB |

## A1. Each finding of the first review

| # | finding | status | evidence |
|---|---|---|---|
| M1 | does not merge / `/tmp` fallback | **FIXED** | branch merges clean and GitHub says MERGEABLE; `run_tests.sh` uses `"$TMPDIR/v4_fixwork_wp2"`, no `/tmp` fallback, `args=("${allow[@]}")` kept |
| M2 | meta lacks binary block | **FIXED** | `setup_run.cpp` `m["binary"] = binary_block()`; `cli_setup_pipeline` asserts `meta.binary` and the record's `binary` |
| m1 | thin T11 tie coverage | **FIXED** | `golden_T11_exact_tie_design_vs_v3` (Walsh design, p = 320, 6 duplicates, τ ∈ {0.3, 0.5, 1−⅔}, ≤ and <, vs `v3::complete_linkage`); at τ = 1−⅔ 23 merges lie exactly at the cut and ≤/< give 284 vs 261 merges, both match v3 (quick log). See N1 |
| m2 | table-stage peak at 10⁶ | **DISPOSITIONED / delivered as accounting** | D-18 sections not stored, two-pass stores (no staging blow-up), exact accounting + admission; the ≤ 12 GB target is an estimate, not measured at 10⁶ here (PR50 recheck reproduces the accounting) |
| m3 | content hash changes per run; test hid it | **FIXED** (as dispositioned) | `invariance_threads_and_tiles` compares the hashes of every section except `meta` at threads 1/2/3, no clearing of timings |
| m4 | own libm guard + bypass | **FIXED** | `allow_non_fma_libm` and the setup-side guard are gone (grep: only `pmath` itself and its report mention `fma_variant_expected`) |
| m5 | D-4 wording | **FIXED** | DECISIONS D-4a records the height predicate fl(1−|r|) ≤ fl(1−τ_n), ≥/> as `strict` |
| m6 | packing untested | **FIXED** | `unit_truncated_partition_shape` recomputes retained clusters from the forest, sorts by minimum index, next-fits, and compares `bptr`/`members` |
| m7 | exact mode memory guard | **FIXED** | `run_setup` refuses `partition=exact` with `resource_limit` when 8p² > limit (default 32 GB, or `--mem-budget`); reason string states both numbers |
| m8 | exceptions inside OpenMP | **FIXED** (one residual, N4) | tables: `Error` / `bad_alloc` / `...` caught inside the region, rethrown after; correlation tiles: caught in `tile_pass` (`tiles.h:104-113`), rethrown |
| m9 | small items | **FIXED** | global top-B lists independent of thread count; R script requires a work dir or `TMPDIR`; `cli_setup_pipeline` covers gen → prep → setup → info; `partition` and `file_mode` are recorded in the record; compat defaults to the exact partition, and compat + truncated is refused |

## A2. The late fix: `setup --manifest` (commits 9d8f9c25, c303164e)
Read `setup_run.cpp:175-250` and the new `cli_setup_pipeline` block; ran the test (PASS).
- **data.bin from the manifest's inputs:** the input whose base name is `data.bin`; main has already verified its content hash (`verify_inputs`). ✔ (same convention as calibrate/island/merge)
- **Refuses conflicts:** an explicit `--data` that differs from the manifest's path → exit 13 (tested); two `data.bin` inputs → `invalid_input`; manifest `params.n`/`p` ≠ data.bin → exit 13 (tested, p = 401); no data at all → exit 13 (tested). ✔
- **Mode from the manifest:** `--file_mode`, else the manifest's `mode` (must be a string); `compat` ⇒ exact partition and a compat file (tested: `partition = exact`, `file_mode = compat`); `law` default tested. ✔
- **Data sections identical to the `--data` form:** the test runs both forms on the same data (AR n = 80, p = 400, seed 5), erases `meta`, and compares the sha256 of every other section; also checks `meta.inputs.data.bin` and `meta.mode`. ✔
- **Format decision (manager 11-16):** `code_ptr` is built with **J + 1** entries (`tables.cpp:170`, `assign(P.J + 1, 0)`), and setup.bin carries **no `meta.stores`** (the test asserts `!meta.contains("stores")`). Both confirmed. ✔

## New findings (all NIT / MINOR, none blocking)
- **N1 (MINOR, test strength).** `golden_T11_exact_tie_design_vs_v3` prints the number of merges at the cut but never asserts `at_cut > 0` for τ = 1−⅔ (or that ≤ and < differ). Today it does (23; 284 vs 261), so the case is real, but a changed seed or shuffle could silently lose the property. Fix: `SCHECK(tau != 1-2/3 || at_cut > 0)`.
- **N2 (MINOR, consistency).** With a manifest, an explicit `--file_mode` that disagrees with the manifest's `mode` is silently preferred; `merge` refuses disagreement ("both given must agree") and `--data` is refused here. Also `mode_from_name` accepts `none` for setup, whereas `calibrate` allows only compat | law | V. Fix: refuse a mode conflict and any mode outside {compat, law, V}.
- **N3 (NIT).** `--data` is compared to the manifest path as a string, so the same file under two spellings is refused (conservative, fine for the driver).
- **N4 (NIT).** The `chosen` selection region in `correlation_pass` (`corr.cpp:125-139`) still has an unguarded per-thread `std::vector` that can in principle throw `bad_alloc` inside OpenMP; practically unreachable (≤ B entries).
- **N5 (NIT).** Stale comment in `cli_setup_pipeline` ("driver form … p = 2000"; the data are p = 400).

Contract: setup.bin sections, binary block, hex64 and statuses as in INTERFACES (v0.1.13 base). Nothing outside `engine_v4/`.
