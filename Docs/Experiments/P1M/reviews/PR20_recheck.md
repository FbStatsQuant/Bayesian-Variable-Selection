# PR #20 re-check: WP4 slice 2 (calib/fit writers, island_r.bin reader, `smcbvs4 merge`), fixes for C-1, M-1, M-2, m-1 to m-4

- **Reviewer:** Opus 5.5 (high), independent re-check. Template: `briefs/REVIEW_PR_template.md`; rules: `briefs/BUILD_COMMON.md`.
- **Scope:** new head `4cfcb040` (`exp/P1M-wp4-io`) into `exp/P1M-engine` at `57a6ba3f` (after #24 and #29 to #32; INTERFACES v0.1.10, the same text as the department copy).
  - The fixes are `3da86008`, `e2ff09bb` and `4cfcb040`, on top of the base merge `ddddae0c`. They touch only `engine_v4/`: `merge.h`, `wp4_io.{h,cpp}`, `test_wp4_io.cpp` and the golden harness.
  - The first review is `reviews/PR20_review.md`. The author's fix list is the PR comment.
- **How:**
  - I extracted the PR head and the merged tree with `git archive` into `/home/fb31/SMC_Engineering_Department/tmp/20261116-recheck-20`. That folder was removed at the end.
  - Read only: nothing was pushed, commented or branched.
  - Everything ran under `nice -n 19` with ≤ 3 threads, on Owls only, with no NOTS. Processes were stopped only by PID: one forked probe child of my own, see the test runs.
- **Probe:** a reviewer test binary that `#include`s the PR's `test_wp4_io.cpp`, so it reuses the PR's own fixture (`make_fx`, p = 24) and its hash-consistent `rewrite()`. To that I added:
  - a meta rewriter;
  - the first review's 28 hostile cases, plus 40 new ones;
  - a φ check and a determinism sweep;
  - **real WP3 islands** from `run_island` and `write_island_file`, merged;
  - 22 runs of the real `smcbvs4` binary through the CLI and manifest paths.
  - The probe was built and run against both the PR-head build and the merged build.

## Verdict: **MERGE** (C-1, M-1 and M-2 are fixed; 4 new MINOR, 5 INFO; none blocks)

| grade | count |
|---|---|
| CRITICAL | 0 (C-1 fixed) |
| MAJOR | 0 (M-1 and M-2 fixed) |
| MINOR | 4 new (n-1 to n-4); m-1 to m-4 fixed |
| INFO | 5 |

- **Fixes.** All three blocking findings are fixed and tested through the real binary:
  - **C-1.** R′ comes only from `params.Rp` or `--Rp`. Every refusal the author claims is reproduced, and the finite-estimate check is in place.
  - **M-1.** `--manifest` works with a driver-style manifest. `--mem-budget` is in bytes.
  - **M-2.**
    - The first review's 28 hostile files give **0 crashes**: 27 are refused, and H19 is accepted with the foreign entries ignored, as designed.
    - 40 new cases also give **0 crashes**.
    - Real WP3 islands pass the stricter validation and merge (`law` and `V`).
- **Tests:**

  | build | `v4_tests` | WP4 quick golden |
  |---|---|---|
  | PR head | 97/97 | 254,268 checks, 0 failures |
  | merged onto `57a6ba3f` | 105/105 | 254,268 checks, 0 failures |

  - `git merge-tree` is clean (tree `12a072ca`).
- **What remains is minor:**
  - **n-1.** A wrong `top_hash` duplicates models in the merged store.
  - **n-2.** A few island scalars are still unchecked: `st_ess`, own `island_best`, `hpm_val` log m = ±inf, and the `hpm_ev` tier and sub.
  - **n-3.** Explicit `--Rp`/`--islands` given after `--manifest` override it, so a subset can be pooled.
  - **n-4.** Two parse edges: a huge island index gives `internal_error`, and a negative or huge `--mem-budget` is cast without a check.
  - These can follow in a small PR, or in WP4's next slice.

## Claims, one by one

| claim | result |
|---|---|
| C-1: R′ only from `params.Rp` / `--Rp`; `--islands` is a comma list or a JSON array; missing R′, R′ < 1, a subset, a duplicate or an empty list is refused | **Verified** (MEASURED, probe N44–N49, K1, K1b, M2, M10, M13; the PR test). A comma list + `--Rp 4` → exit 0, completed, R′ = 4. No `--Rp` → 13. `Rp` = 2.5, "4" (string), 2·10⁹ → 13. Trailing comma / empty → 13. A JSON array arrives only through `params.islands` (M12 → exit 0). Through the CLI, a JSON text is split on commas and refused as a missing file (K1c, exit 14): fine, since the CLI documents comma lists. **Gap:** an explicit `--Rp` / `--islands` *after* `--manifest` wins over the manifest (n-3) |
| C-1: no non-finite estimate reported completed | **Verified** by reading (`merge.h:416-425`). `logZ = +inf` in an island is refused at the head as a numerical failure (N9), and NaN `pip_r` → invalid (H18) |
| M-1: `--manifest` object; inputs, R′, mode from it; `--mem-budget` bytes, `-gb` alias | **Verified** (MEASURED). A hand-made driver-style manifest (inputs by path + content hash, `params.Rp`, `mode`) → exit 0 (M1). Wrong island hash → 13 (M11, the CLI's `verify_inputs`). Missing setup input → 13 (M14). R′ 4 with 5 islands → 13 (M9). R′ 5 with 4 → 13 (M10). `island_4` named twice (`island_4.bin` + `island_0004.bin`) → 13 (M7). `--mem-budget 1000` → exit 11 `resource_limit` (M6). The PR's own test runs the real driver chain (dry run → `p1m_manifest.py fill` → merge) and passed in both builds |
| M-2: every model, offset, value, `hpm_ev` field, grid/T, calib/setup shape and `island_best` entry validated before use; 30 hostile files → `invalid_input` | **Verified for the listed classes** (MEASURED; detail below). The PR's 30 cases pass, and my 28 + 40 give 0 crashes. **Not covered:** the store hashes (n-1); `st_ess` values, own `island_best[r]` value, `hpm_val` log m ±inf, `hpm_ev` tier/sub (n-2) |
| m-1: fit.bin `meta.inputs` records the islands' actual content hashes | **Verified** (`wp4_io.cpp:758-759`; the PR test compares `island_1.bin` with `head_island(...).content_hash`) |
| m-2: memory plan = whole task (X + 2.5 × setup.bin); kbar from the store sections; `rb_*` not loaded | **Verified** by reading (`wp4_io.cpp:740-749`, `merge.h:100-109`; `rb_round` is shape-checked only, `wp4_io.cpp:359`). kbar is the max over islands of pool/entries: conservative |
| m-3: "island r: malformed (…)" distinct from "changed between head and load" | **Verified** (MEASURED: H1–H11, H14–H16, H18, H20, N1–N4 report "island 1: malformed (…)") |
| m-4: `--out` required | **Verified** (PR test, exit 13) |
| 97/97 `v4_tests`; full golden 975,925 / 0 | **97/97 verified**, and quick golden 254,268 / 0. The full golden was **not re-run**: the brief asked for the quick set |

## Hostile-file battery (MEASURED; each merge run in a forked child, hash-consistent rewrites through the WP1 Writer)

**The first review's 28 cases: 0 crashes (was 9), 0 completed with wrong content (was 9).**

| case | before (`db58db70`) | now (`4cfcb040`, and identical on the merged tree) |
|---|---|---|
| H1, H2 `top_pool` index p + 10⁸ / −1 | SIGSEGV / SIGABRT (heap) | refused: "top store: index out of range" |
| H3 unsorted store model | completed | refused: "model not strictly increasing" |
| H4 `top_off` = 2⁶⁴ − 1 | completed | refused: "pool offset out of range" |
| H5, H6 `hpm_S` out of range / unsorted | SIGSEGV | refused |
| H7 `hpm_ev` phase 99 / mech 77 | completed | refused |
| H8 `hpm_val` F = NaN | completed | refused |
| H9 `top_v` NaN | refused | refused |
| H10 `st_ess` length 1; H11 empty grid | completed (φ silently 0) | refused: "grid / st_ess length differs from T" |
| H12 meta r = 3 at position 1; H13 meta N = 49 | refused | refused (head) |
| H14, H15 terminal offsets | refused | refused |
| H16 `top_len` past the pool; H17 empty `logZ` | refused | refused |
| H18 `pip_r` NaN | completed with NaN PIPs | refused: "pip_r: not in [0, 1]" |
| H19 island 2's `island_best[1]` = 10³⁰⁰ | completed, E1 masked | completed with the foreign entry **ignored** (as designed; the PR test checks it) |
| H20 `logical` size | refused | refused |
| C1, C2 calib `inh_idx` / `hpm_S` p + 10⁸ | SIGSEGV | refused |
| C3 calib `inh_F` NaN | refused | refused |
| S1 setup `blk` short | refused | refused |
| S2 setup `pos` = 40 | completed (UB shift) | refused: "pos out of range of its block" |
| S3, S4, S5 setup `code_ptr` 10¹² / table pool / `mode_S` | SIGSEGV | refused |

**New cases (40):**

- **Refused** (`invalid_input` unless noted):
  - **Island HPM:** `hpm_ev` BRIDGE stage 0 (N1); `hpm_ev` seg = CALIB (N2); `hpm_S` = the store's second model (N3); `hpm_val` F + 1 ulp (N4).
  - **Island arrays and meta:**
    - `island_best` of length r + 2 (N8);
    - `logZ` = +inf, refused as `numerical_failure` (N9);
    - meta T = 10⁹ (N13), p + 1 (N14), status `numerical_failure` with estimates present (N15, `numerical_failure`), Hm = 3 against calib's 4 (N16);
    - `rb_round` dropped (N17); `pip_r` of length p + 1 (N19); empty store in a completed island (N20); `top_v` order swapped (N21).
  - **Calib:** grid changed, so all 4 islands' `meta.inputs` mismatch (N23); invalid grid (N24); meta L = −1 / N = 0 (N25, N26); `inh_ptr` not covering the pool (N27).
  - **Setup:** empty block (N28); `code_ptr` = −1 (N29); a table model across blocks (N30); `blk_members` permuted (N31); `mode_S` unsorted (N32).
  - **Island lists:**
    - island order 2,1,3,4 (N40);
    - island 1 copied as island 2 (N41);
    - the same file under two spellings, `dir/x` and `dir/./x` (N42);
    - `--mode V` against compat files (N51);
    - no mode (N50);
    - a missing island file, refused as `io_error`, T10 class (N52).
- **Accepted as completed:**
  - N5 `hpm_val` log m = +inf (n-2);
  - N6, N7 own `island_best[1]` = 10³⁰⁰ / −inf (n-2);
  - N10–N12 `st_ess` = NaN / −5 / 10⁹ (n-2);
  - N18 completed island without terminal sections: allowed, since terminal supports are optional (`merge.h:46`);
  - N22, N22b wrong `top_hash` (n-1);
  - N43 island "from another fit" built from the same seed: the files are byte-identical, so the case is void. Islands of a *different* fit fail on `meta.inputs` (N23).
- **R′ and order:**
  - Explicit `Rp = 3` with 3 islands and no manifest → completed, R′ = 3 (N44). That is correct: no manifest claims otherwise.
  - With a manifest it is a gap: n-3.

## Regressions

- **φ reconstruction = v3** (MEASURED): INIT 0 → 0; BRIDGE stages 1/2/3 → 0.3/0.7/1 = `grid[stage]`; BURN, MEASURED → 1. **6/6** equal. Out-of-range stages are now refused, not 0.
- **fit.bin thread invariance** (MEASURED): ℓ {3, 8} × threads {1, 2, 3} × chunk {1, 7, 64, 2048}. **22/22** fit.bin files are identical in every section and in `meta` (apart from `timings` and `mem_estimate`).
- **Real WP3 islands → merge** (MEASURED, new):
  - Setup: 4 islands from `run_island` (label-major, G = 16, 2 threads, N = 50, the calib's frozen grid) and WP3's `write_island_file`, in both `law` (Bit) and `V` (class A).
  - Check: all **3,844 / 3,844** WP3 store hashes equal `D.zob.hash(S)`.
  - Check: each island's `island_best` equals its `hpm.F`.
  - Result: the merge is **completed** in both modes (log Ẑ −48.530643, E1 0).
  - This covers the cross-WP direction the PR's layout test builds by hand.
  - The islands' `binary.git_commit` was set to the fixtures' clean value. My archive build has no git, so theory mode refuses `'unknown'`, as INTERFACES §5.1 requires.
- **Merged onto the current base** (MEASURED): `git merge-tree` is clean against `57a6ba3f`, which includes #24 (WP3 slice 3: `island_file.cpp` writes the compat mode).
  - Build + `v4_tests`: **105/105** (the base adds 8 cases).
  - WP5 driver, competitor harness and install script: OK.
  - Quick golden: 254,268 / 0.
  - My probe on the merged build: output identical to the PR head.

## New findings

### n-1 MINOR (M-2 class): the island store hashes are not verified; a wrong `top_hash` duplicates models in the merged store
`src/merge/wp4_io.cpp:310-317` (island store), `:82-86` (`read_store`, setup table stores); `src/common/store.cpp:59` (duplicates = same v, same hash, same model)
- **Evidence (MEASURED, N22b).** Every `top_hash` of island 1 was XORed with a constant, hash-consistently.
  - The merge completes.
  - The merged top store has 961 entries, but only **860 distinct models**: 101 slots hold duplicates, so 101 legitimate models were evicted from the top 40p + 1.
  - log Z_T happened to be unchanged in this fixture.
  - The store invariant I1 (unique models) is broken in a `completed` fit.bin. WP5's evaluator reads that store.
- **Reachability:** a writer bug, as for M-2. Real WP3 hashes are all correct (3,844 / 3,844).
- **Fix:**
  - Pass the Zobrist table (`D.zob`) in `Expect` and the `read_store` callers.
  - Refuse `hh[i] != zob.hash(S)` in the same loop as `check_model`. The cost is O(pool), already paid by `check_model`.
  - Add a case to `wp4_io_hostile_files_refused`.

### n-2 MINOR (M-2 completeness): a few island scalars are still unchecked
`src/merge/wp4_io.cpp:300` (`st_ess`), `:328` (log m), `:336` (`hpm_ev` tier / sub), `:350` (own `island_best`)
- **`st_ess`** (N10–N12): NaN, −5 and 10⁹ are accepted. A NaN ESS can never trigger `low_empirical_ESS` (`merge.h:414`, `e < 0.5 N` is false), so it would hide a low-ESS island.
  - Fix: require 0 ≤ ESS ≤ N (finite).
- **Own `island_best[r]`** (N6, N7): any value other than NaN / +inf is accepted. 10³⁰⁰ masks that island's E1 contribution (`merge.h:401`). −inf forces it.
  - WP3 writes `island_best == hpm.F` (measured on 4 real islands).
  - Fix: require `ib[r] == hv[0]` when the island has an HPM, or at least ≥.
- **`hpm_val` log m** (N5): only NaN is refused. ±inf is accepted and written to fit.bin `hpm_logm`.
  - Fix: `need_finite`, or check F = logprior[k] + log m bitwise; `Ev` in the fixture computes it that way.
- **`hpm_ev` tier / sub** (by reading): range-checked to [0, 2³²), then cast to `uint8_t`. The tier is not compared with calib's tier.
  - Fix: tier ∈ {0, 1} and equal to `C.tier`; sub < 256.

### n-3 MINOR (C-1 residue, CLI precedence): explicit `--Rp` / `--islands` silently override the manifest, so a subset can be pooled
`src/cli/main.cpp:51-55` (params copied into args in command-line order); `src/merge/wp4_io.cpp:660-694`
- **Evidence (MEASURED, real binary):**
  - **M3.** `merge --manifest m.json --Rp 3 --islands i1,i2,i3` with `params.Rp = 4` and 4 island inputs → **exit 0, completed, R′ = 3**. The manifest's `verify_inputs` passed for all 4 islands; the 4th was then dropped.
  - **M3b.** `--Rp 3 --manifest m.json` → R′ = 4: the manifest wins when it comes second. Precedence depends on argument order.
- **Reachability:** an operator, not the WP5 driver. The driver passes only `--manifest --threads --out`.
- **Why it still matters:** GUARD-W says "no subset is ever pooled". The manifest is the authority for R′.
- **Fix:** when a manifest is given, refuse an explicit `Rp` that differs from `params.Rp`, and an `islands` list that is not exactly the manifest's island inputs (r = 1..R′, same files). Or forbid both with `--manifest`.

### n-4 MINOR (input edges): an island index overflow gives `internal_error`; `--mem-budget` is cast without a check
`src/merge/wp4_io.cpp:683`, `:740`
- **Island index.** `std::stoi` on `island_99999999999.bin` throws `std::out_of_range` → **exit 15, `internal_error`, reason "stoi"** (MEASURED, M8). It should be `invalid_input` (exit 13).
- **Memory budget.** `(uint64_t)nget(args, "mem_budget", 0)`: `--mem-budget -5` and `--mem-budget 1e30` are undefined-behaviour casts. Both ran to **completed** (MEASURED, K1d, K1e), so the budget was effectively off or huge.
  - Fix: require a finite whole number with 0 ≤ b < 2⁶⁴, else `invalid_input`. The same rule should apply to `--mem-budget-gb`.

### INFO
- **I-1.** Two new compiler warnings in the PR code:
  - `wp4_io.cpp:672` `-Wmisleading-indentation`. The comma-split loop is correct; only the layout misleads.
  - `wp4_io.cpp:618` `sget` is now unused.
- **I-2.** INTERFACES does not yet describe the merge's argument forms:
  - `--Rp`;
  - `--islands` as a comma list;
  - inputs found by base name `data.bin` / `setup.bin` / `calib.bin` / `island_<r>.bin`;
  - `island_0004.bin` is accepted as island 4 (M7b).
  - The driver's template matches the convention. One line in §7 would make it binding for WP5.
- **I-3.** R′ exists only in the manifest and the arguments. calib.bin and island_r.bin carry no R′, so no file-level cross-check of R′ is possible. Islands 1..R′ of a run that had more islands cannot be told apart from a complete set: the manifest must stay the authority (see n-3).
- **I-4.** The merge reads every island fully twice: pass-1 verifying reader + pass-2 load. The PR still reads `top_len` / `top_pool` in pass 1 for kbar, but those are mapped and cheap. That is I/O, not resident memory (first review I-2).
- **I-5.** One probe note, not a PR issue. Forking a merge child after the parent process has run OpenMP regions (WP3 islands with 2 threads) deadlocked the child in libgomp. I stopped my own child by PID and ran that merge in process. The PR's `merge_in_child` merges with threads = 1, and its test passed in both builds.

## Test runs (MEASURED; Owls, Xeon Gold 6148, GCC 11.5.0, R 4.6.0, cmake 3.31.8, `nice -n 19`, ≤ 3 threads, 2026-11-16)

TMPDIR `/home/fb31/SMC_Engineering_Department/tmp/20261116-recheck-20`, removed afterwards.

| # | what | result |
|---|---|---|
| 1 | `tests/run_tests.sh --quick --threads 3` at `4cfcb040` | `v4_tests` **97 cases, 0 failed** (incl. `wp4_io_merge_cli_and_driver_manifest`, `wp4_io_hostile_files_refused`). WP5 driver 17 tests OK, competitor harness OK, install script 23 checks OK. **WP4 golden quick: 254,268 checks, 0 failures**. Wall 02:49:20 → 02:56:40. `$TMPDIR/wp4_golden` removed by the runner |
| 2 | merged tree `12a072ca` (= `git merge-tree origin/exp/P1M-engine origin/exp/P1M-wp4-io`, base `57a6ba3f`), same command | **105 cases, 0 failed**; WP5 extras OK; **WP4 golden quick: 254,268 / 0**. Wall 03:09:06 → 03:18:17 |
| 3 | probe `rc_hostile` (PR-head build; 28 original + 40 new cases, forked children) | **0 crashes.** Original 28: 27 refused, H19 completed with foreign entries ignored. New: refused except N5, N6, N7, N10–N12, N18, N22, N22b, N43 (void), N44 (correct); see n-1, n-2 |
| 4 | probe `rc_phi` | 6/6 φ = v3 |
| 5 | probe `rc_det` (threads 3) | 22/22 fit.bin identical |
| 6 | probe `rc_real_wp3` | 4 WP3 islands (`run_island` + `write_island_file`) in `law` and `V` → merge completed; 3,844/3,844 WP3 hashes = `D.zob.hash`. A first attempt in a forked child hung (I-5); PID 1428833, my own child, was stopped by PID |
| 7 | probe `rc_cli`: 22 runs of the real `smcbvs4 merge` | K1 0; K1b 13; K1c 14; K1d 0 (n-4); K1e 0 (n-4); K1f 13; K1g 0; M1 0; M2 13; **M3 0 with R′ = 3 (n-3)**; M3b 0 with R′ = 4; M4 13; M5 13; M6 11; M7 13; M7b 0; **M8 15 (n-4)**; M9 13; M10 13; M11 13; M12 0; M13 13; M14 13 |
| 8 | the probe rebuilt against the merged build (run 2's libraries) | output identical to runs 3–7, line for line (timings aside) |
