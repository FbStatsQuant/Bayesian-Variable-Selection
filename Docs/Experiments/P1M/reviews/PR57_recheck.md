# PR #57 re-check of the fix round (WP3 StartView, gate P5)

Reviewer: Claude (second review, read only). Owls, 2026-11-17. Gate review: `Docs/Experiments/P1M/reviews/PR57_review.md` (head 9344737d, 2 MAJOR, 5 MINOR).
Checked head `ecabdcfc` (fix commit `5d3786c8`; `0399568d` merges engine 7c2c6a75 and was ignored; `ecabdcfc` changes WP3_DESIGN.md only).
Worktree `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-1da14bf6-e16df64bedbcf902`, detached at ecabdcfc. Scratch, builds and `TMPDIR` are under its `.rc_tmp/`; `P1M_TEST_ROOT=$TMPDIR`; `nice -n 19`, `taskset -c 0-2`. Nothing deleted, nothing written outside the worktree (`run_tests.sh --keep`). The p = 1e4 / 3e4 setup files made by the first reviewer were only read, from `t3-3d20ff7b…/.rc_tmp/{s1e4,s3e4,probes}`.

## Verdict: MERGE

All seven findings are closed. I found no CRITICAL or MAJOR issue. Three small residuals are listed at the end; none blocks the merge.

## 1. MAJOR-1: closed

Code (`include/v4/calib_plan.h`, new; used by `calib_run.cpp`, `pilot_only.h`, `tools/plan_tables.cpp`):
- One function, `calib_island_plans`, gives `inputs_bytes = start_inputs_bytes + setup_view_bytes + resident_own`.
- `setup_view_bytes` = 12p + 16(J+1) + 8C + 8(K+1) + 4K + headers.
- `release_table_stores(S)` runs right after `offer_tables` in `calibrate` and in the pilot. The three stores are freed once, after they are in the ledger.
- I grepped the remaining readers of `S` in `calib_run.cpp`. Only `comp()` is used afterwards (blk, pos, code_ptr, logr, blk_ptr, blk_members), plus `S.content_hash`. None of them reads `ttop`, `tlead0` or `tlead1`, so the release is safe.

Reproduction of the reviewer's case. AR, n = 200, p = 3·10⁴ (the first reviewer's `s3e4/data.bin` and `setup.bin`), `calibrate --mode V --threads 3`, portable build of this head (`r3e4/`):

| step | result |
|---|---|
| `--plan-only 1 --mem-budget 1800MiB` (1,887,436,800 B) | exit **11**, `resource_limit`, G = 1, plan 1,894.0 MiB > budget (head 9344737d: `completed`, G = 64, 1,799.4 MiB) |
| the run, same budget | exit **11**, `calibration island not admitted (N-1): resident + island plan 1986049068 B > --mem-budget`; no `calib.bin`; refused with 66 MB RSS, before any array was loaded |
| `--plan-only 1` without a budget | G = 256, total 2,285.8 MiB, **floor 1,894.04 MiB**; `setup_inputs` 193.5 MiB, `setup_copy` 187.8 MiB. The 187.8 MiB agrees with the first reviewer's measured retained SetupView of 343 MiB minus the table stores, which are now released |
| the run at the new floor (`--mem-budget 1986049068`) | **admitted**, loaded, and calibrating |

Measured peak at the new plan:
- Peak RSS of the admitted run: **1,749,764 kB = 1,708.7 MiB**, against a plan of 1,894.0 MiB (peak < plan; 90 %).
- Caveat: at p = 3·10⁴ the run takes more than 50 min on 3 cores, and my `timeout 3000` stopped it (`Exit status 124`, no `calib.bin`). The peak is therefore the maximum of the first 50 min, which cover the load, the hash passes and the tier-0 calibration stages. It is a lower bound for the whole run, not a completed-run peak. The refusal, the admission and a peak under the plan all hold.
- I did not repeat WP3's p = 2·10⁴ IND measurement (1,419 MiB peak vs 1,639 MiB plan). The 3·10⁴ run above is a different size with the same direction: peak below plan. My peak is 191 MiB (10 %) under the plan.

Test added: `start_view_calibrate_admission_counts_setup_copy`. It checks that `floor_old = floor_full − setup_copy` is refused by `--plan-only` (exit 11), that `floor_full − 1` is refused, that `floor_full` is admitted, and that the run with `floor_old` writes no `calib.bin` and the run at `floor_full` does. PASS in the portable and FMA builds.

## 2. MAJOR-2: closed

`map_start_view` (`setup_load.h`) now checks:
- `size_cum` is in [0, 1], non-decreasing, ends at exactly 1.0, and is bit-equal (memcmp) to the rebuild from `logF` and the prior;
- every `cond0[b][r]` is in [0, 1] and bit-equal to the first cumulative of the row rebuilt from `logprof` and `logF` (OpenMP, no allocation, no throw inside the parallel region);
- no NaN or +inf in `size_logmass`, `logF` and `logprof`.

The draws also clamp: k ≤ K, j ≤ len − 1, i ≤ nc − 1 (`start_view.h`).

Reproduced with my own probe (`probes/malformed_new.cpp`, built against this head) on the first reviewer's 101-member file, `probes/s1e4_sizecum_zero.bin` (p = 10⁴, `size_cum` = K + 1 zeros, all hashes valid):
```
old loader refused: ... size_cum differs from the island's rebuild of the start law
mapped loader refused (status invalid_input): ... start law values: size_cum does not end at exactly 1
```
Head 9344737d accepted this file and drew 101 members.

`start_view_malformed_values_refused` passes (portable and FMA, 5.4–5.8 s). It rewrites p = 400 AR setup files through `fmt::Writer`, so every hash is valid, and checks 11 value / structure refusals, 2 identity refusals and 1 draw-bounds check, 14 checks in all:

| group | checks |
|---|---|
| `size_cum` | all zeros; ends at 0.5; not monotone; one ulp off the rebuild |
| `cond0` | entry 2.0; one ulp off the rebuilt row |
| NaN | `logF`; `logprof` |
| partition and offsets | `blk` (see residual 2); `pos` shifted; `code_ptr` step not 2^m |
| identity | `map_start_view` and `load_neighbours` refuse a wrong hash |
| draw bounds | 500 draws from arrays with all-zero `size_cum`, `cond0` and `logprof` stay in [0, p) with k ≤ K |

Cost: the WP3 note gives 0.63 s at p = 10⁵ on 1 thread (about 6 s at 10⁶ on 1 thread; sub-minute at 3+ threads). I did not re-time it. Not a concern.

FMA question I checked: the new rebuild runs inside island TUs compiled with `-march=x86-64-v4`. It uses only long-double `exp`, additions and a division, with `-ffp-contract=off`. The FMA build's `start_view_mapped_wp2_setup` and `start_view_cli_mapped` pass, so bit-equality with WP2's portable-built tables survives in the FMA family.

## 3. MINORs 2-5: closed

- **MINOR-2 (pilot).** `pilot_only.h` now reads `read_data_plan`, `read_setup_dims` (header and table hashes only) and `calib_k_plan(size_logmass)`, then calls the shared `calib_island_plans`, and refuses with `resource_limit` (exit 10 + status) before `load_data`, `read_setup`, the mapping or `offer_tables`. It uses `plan.ledger + plan.export_` as resident state. Same k rule and same function as calibrate. (I read the code only; the pilot tool has no run in the quick suite.)
- **MINOR-3 (identity, MAP_PRIVATE).**
  - `map_start_view(..., expected_hash)` and `load_neighbours(..., expected_hash)` compare `Reader::content_hash()` with `sd.content_hash`. Call sites: `island_cmd.cpp`, `calib_run.cpp`, `pilot_only.h`.
  - The pilot also compares `dhash` and `S.content_hash` with the plan.
  - `fmt::Reader` maps with `MAP_PRIVATE`.
  - Limit: the hash is the header/table hash. A mutation of the file after the second open is not detected; the design records that engine files are written by rename and that an in-place rewrite is outside the contract. Adequate for frozen inputs.
- **MINOR-4 (fixed heap, label).** `kStartFixedHeapBytes` = 1 MiB is added to `start_inputs_bytes`. The island-plan label and WP3_DESIGN now state that hash verification pages the whole file in (reclaimable file pages), and the plan table has a separate "+ reclaimable file pages" column. `start_view_cli_mapped` checks the new constant.
- **MINOR-5 (tests).**
  - Negative loader tests: added (section 2).
  - Admission with the copy: added (section 1).
  - `setup_load.h` self-contained: it includes `island.h`, and `test_start_view.cpp` includes it first.
  - Pinned pre-StartView hashes (law and compat; see section 4): added.

## 4. Bits unchanged

Quick suite, portable build:
- T3: bit `44a15bfc6fb8d233`, A `d2df149413596a19`. Matches the pinned values.
- Pre-StartView island hashes, pinned in `start_view_mapped_wp2_setup` against the merge-base engine and the first reviewer's measured values; the test **PASS**es with them:

| design | law | compat |
|---|---|---|
| AR | `5298f6a5216f12dc` | `c75513efe4d23803` |
| BLK | `eb1d5b4e7f10b76c` | `ee17af9cce39896f` |

  The V (class A) hash depends on the build and is not pinned (pin = 0).
- WP4 R golden: 540,419 checks, 0 failures.

FMA build (`-DV4_ISLAND_ISA=x86-64-v4`, `island_fma true`):
- T3 bit `44a15bfc6fb8d233`, A **`e9cc4ab39f8a72db`**, invariant over PM/LM, threads, G and tile.
- `start_view` 5/5, `island_command` 7/7, `t3_invariance` 2/2: all PASS.

## 5. `results/WP3_PLANS_1e6.md` spot-check: OK

The file is `Docs/Experiments/P1M/results/WP3_PLANS_1e6.md` in the main clone. It is **untracked there (`??`), so it is not part of PR #57** and the manager must commit it. I rebuilt `v4_plan_tables` from this head and ran `--counts` on WP2's `counts/{AR_n200,BLK_n200,IND_n1000}.json` with the default 96 / 96 / 32 threads (`plans_*.log`). Rows compared with the doc:

| row | final | calib alone | calibrate task | file pages | merge | setup inputs | copy | doc |
|---|---|---|---|---|---|---|---|---|
| AR 200 G=1 | 19.5 | 37.1 | 61.7 | 3.7 | 39.3 | 6.78 | 6.54 | equal |
| BLK 200 G=256 | 28.3 | 45.8 | 67.0 | 3.7 | 30.7 | 3.33 | 3.06 | equal |
| IND 1000 G=256 | 46.8 | 64.4 | 91.0 | 6.9 | 59.3 | 9.21 | 8.52 | equal |

(GiB.) Hand check of the AR copy: 12p + 16(J+1) + 8C + 8(K+1) + 4K + 320 with p = 10⁶, J = 74,726, C = 875,529,216, K = 100 = 7.0168·10⁹ B = **6.535 GiB**, matching the table's 6.54. The doc's "calibrate task" column equals the tool's "N-1" column, so the doc merged two identical columns (see residual 3). The doc's reproducibility header says it was built from 0399568d; `ecabdcfc` adds no code after that.

## Test run (MEASURED)

`tests/run_tests.sh --quick --threads 3 --build-dir .rc_tmp/build_portable --keep`, log `.rc_tmp/quick.log`. g++ 11.5.0, flags `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`, Xeon Gold 6148.

| part | result |
|---|---|
| `v4_tests` quick | **180 test cases, 0 failed, 0 check failures** (includes `start_view_*` 5/5 and `island_command_*` 7/7) |
| WP5 Slurm-driver tests | OK (28) |
| WP5 competitor harness | OK |
| WP5 install script | OK (9 checks) |
| WP4 R golden (quick) | 540,419 checks, 0 failures |

FMA build: the three groups in section 4, all pass (`fma_cli.log`).

## Residuals (none blocks the merge)

1. **Peak not from a completed run.** The 3·10⁴ admitted calibration was stopped at my 50 min cap (peak 1,709 MiB so far vs plan 1,894 MiB). WP3's 2·10⁴ completed-run figure (1,419 vs 1,639 MiB) is theirs; I did not repeat it.
2. **`blk` negative case is vacuous in `start_view_malformed_values_refused`.** On the p = 400 AR fixture `blk[0] == blk[1] == 0`, so `b2[1] = b2[0] == b2[1] ? b2[1] : b2[0]` leaves `blk` unchanged and the `if (b2 != blk)` guard skips the check (I confirmed this with `probes/blk_check`). The partition check is still exercised by the `pos` and `code_ptr` cases. Suggested fix: set `b2[1] = b2[1] + 1` (or pick two variables in different blocks).
3. **`WP3_PLANS_1e6.md` is not in the PR, and the tool prints an extra column.** `v4_plan_tables` prints both "calibration island, N-1" and "calibrate task" (equal), while the doc has one. Commit the doc with the merge and drop the duplicate column in the tool, or say in the doc that they are equal.
