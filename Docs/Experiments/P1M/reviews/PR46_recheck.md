# PR #46 re-check of the fix round

Reviewer: Claude Sonnet 5.5 (review sub-agent), Owls, 2026-11-17. Read only: nothing pushed or commented, no sub-agents,
nothing deleted; scratch, build and `TMPDIR` under `<worktree>/.rc_tmp/`, `P1M_TEST_ROOT="$TMPDIR"`.

## Verdict: MERGE

0 CRITICAL, 0 MAJOR, 0 MINOR open. All five requested checks pass; the first review's MAJOR-1, MAJOR-2 and MINOR-4 are
closed, MAJOR-3 is not reintroduced. Two non-blocking notes at the end.

Tree: `exp/P1M-wp4-calib2` at `f44ff58d` (detached; `origin/exp/P1M-wp4-calib2` = `f44ff58d`), which merges
`exp/P1M-engine` `af2d3f60` (merge commit `d5ecf360`). Fix commits examined: `a16c4f19` (MAJOR-1/2, MINOR-4),
`64634927` (read_setup contract), `5b2a440c` (J + 1 in the island-cmd fixture), `f44ff58d` (WP2 fixture regenerated
post-D-31) and the merge's conflict resolution. I read the net PR diff against `af2d3f60` (15 files, all inside
`Scripts/SMC_BVS/engine_v4/`), not what the engine merges brought in.

## Requested checks

1. **MAJOR-1 (calibrate command fixture): fixed.** `calibrate_command_end_to_end` (via `make_cal_inputs`,
   `tests/test_island.cpp:1091`) writes `size_logmass` into setup.bin next to `size_cum`; `test_island_cmd.cpp:131`
   does the same (`45fcd32d`). The command's required-section check stays: `read_setup_dims` refuses a setup.bin without
   `size_logmass` (`island/setup_load.h:98-99`), `check_size_logmass` validates it (`calib_run.cpp:168`) and
   `wp4_io_calib_plan_from_setup` covers the missing / short / non-normalised / NaN / Inf size-law refusals.
   `calibrate_command_end_to_end` PASS (16.1 s).

2. **MAJOR-2 (admission before the full loads): fixed; probe re-run.** `calib::run` now takes n, p, K from
   `read_data_plan` (header, section table, `meta`, each hash-checked; no column read) and the setup's dimensions from
   WP3's `read_setup_dims(..., verify=false)` (section table, `blk_ptr`, neighbour lengths, size law). Plan,
   `resident_ok` / `island_ok` and the refusals (`calib_run.cpp:176-199`; load at `:206-208`) all precede `prep::load_data` and
   `read_setup`, which now run only after admission; each load's content hash is compared with the plan
   read's, so a file changed in between is refused. Allocation probe (`calibrate_admission_before_allocation`, p ≈ 20,000
   after prep, `mem_budget = 1`, every `operator new` counted inside `calib::run`; MEASURED, PASS):

   ```text
   plan_only 0: 1467 allocations, 391719 B, largest 40008 B before the refusal
   plan_only 1: 1519 allocations, 400305 B, largest 40008 B before the refusal
   ```

   Largest request 40,008 B = (J + 1) × 8 for `blk_ptr` at blocks of 4 (≈ 40 KB, as expected). The first review's probe on
   the old order recorded blocks of 160,000 B and p-sized copies. The test asserts < 64 KiB largest and < 1 MiB total.
   The probe counts C++ `operator new` only, not mapped pages (as before). `wp4_io_plan_readers` (plan reader equals
   the full reader; an altered `meta` byte is refused by the plan read itself) PASS.

3. **MINOR-4 (30 + 4k): fixed.** `calib_run.h:80` `entry = 30.0 + 4.0 * kbar` and `merge.h:102` the same, with the
   comments saying why (26 + 4k data + 4 index). `island/memory.h` (WP3) keeps `26 + 4k` with a separate index term
   (`idx = 4 × pow2_at_least(2c + 2)`), so nothing is counted twice; `account.cpp`'s `26 + 4B` is WP2's setup-stage
   model, outside this PR. `wp4_io_calib_plan_from_setup` asserts resident = ledger + export and
   total = resident + inputs + island ledger.

4. **read_setup follows the contract (INTERFACES v0.1.19): yes.**
   - No `meta.stores` required: `read_setup` calls `read_store_sections` with caps/orders from §4.1 (top 40p + 1 HPM,
     lead0/lead1 20p LEX); a stray `meta.stores` is ignored (tested with cap 3).
   - `code_ptr` J + 1 checked (`wp4_io.cpp`, `read_setup`): size equals `blk_ptr`'s, `code_ptr[0] = 0`,
     `code_ptr[J] = |logr|`, and each block's table length `= 2^m`. The old J-entry shape, a wrong end marker, a wrong
     mid entry and a non-zero start are each refused with their own message (`wp4_io_setup_contract_v0119`).
   - `write_setup_min` refuses the old shape (`internal_error`) and writes no `meta.stores`; every fixture builder
     appends the J + 1 end entry (`test_wp4_io.cpp`, `test_island.cpp:1076`, `test_island_cmd.cpp:122`,
     `test_island.cpp` admission fixture).
   - WP2 real fixture: `tests/fixtures/wp2_setup/p14_{data,setup}.bin` (8,512 and 13,312 bytes, regenerated in
     `f44ff58d`). `smcbvs4 info --meta 1` shows no `stores` in meta, `code_ptr`, `size_logmass`, **`cond0`** and
     `nb_ptr` sections present. `wp4_io_reads_wp2_setup_bin` PASS: `read_setup`, WP3's `read_setup_dims` and `load_start`
     read the same file (equal hashes and size law), J = 5, stores with the §4.1 caps, and `calibrate --plan-only`
     returns `completed`.
   - INTERFACES consistency: v0.1.19 (§2 Tables, §5.1 `setup.bin`) says `code_ptr` J + 1 and no `meta.stores`;
     v0.1.20 (D-31) replaces `cond_ptr`/`cond_cum` by `cond0` without touching `code_ptr` or stores; v0.1.18 concerns
     `island_isa` / `island_fma` and the §5.3 binary block. The three entries are in order (18, 19, 20), their
     numbering notes agree with each other, and the §5.1 `setup.bin` line lists `code_ptr (J + 1 entries ...)`,
     `cond0` and the no-`meta.stores` rule together. WP2's writer (`setup_run.cpp:106`, `tables.cpp:170-175`) and
     WP3's `load_start` (J or J + 1, `setup_load.h:22-29`) agree with it.

5. **`test_island.cpp` conflict resolution: correct.** `g_new_track` / `g_new_calls` / `g_new_bytes` / `g_new_max`
   (this PR's probe) and `g_count_allocs` / `g_allocs` (PR #50, used by `test_setup.cpp:40-41`, `extern`) are both
   declared once and both incremented in the single `operator new`, before the injection countdown; the non-`static`
   linkage of `g_count_allocs` / `g_allocs` is retained. Both users pass (probe above; "D-31 allocation-free: 0
   allocations" for AR, BLK and TIE).

## MAJOR-3 not reintroduced (calibrate exit 0 / "completed")

The calibrate record's `status` is now `status_name(task_status(co.status))`, with the calibration's own name in
`cal_status` (`calib_run.cpp:240`, from #52). Real CLI on the WP2 fixture, built from `f44ff58d`:

```bash
smcbvs4 calibrate --mode compat --data tests/fixtures/wp2_setup/p14_data.bin --setup .../p14_setup.bin --seed 77 --threads 1 --out .rc_tmp/cli/calib_compat.bin   # exit 0
smcbvs4 calibrate --mode V      ... --out .rc_tmp/cli/calib_V.bin                                                                                          # exit 0
```

Both exit **0**; the sidecars `calib_compat.bin.json` and `calib_V.bin.json` say `status: completed`, with
`mem_plan.kbar_source = "max(8, q90(pi_0 size) + 1) from setup.bin"`; the 114,944 and 113,664 byte calib.bin files
exist. This is the real binary through `main`, not the in-process command. The in-process
`calibrate_command_end_to_end` also expects `completed`.

## Test record (MEASURED)

Owls `owls.stat.rice.edu`, Xeon Gold 6148, g++ 11.5.0, CMake 3.31.8, glibc 2.34; `nice -n 19`, `taskset -c 0-2`,
OMP 3, OpenBLAS/MKL 1.

```bash
env TMPDIR="$PWD/.rc_tmp/tmp" P1M_TEST_ROOT="$PWD/.rc_tmp/tmp" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=3 \
  OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 19 taskset -c 0-2 \
  bash Scripts/SMC_BVS/engine_v4/tests/run_tests.sh --quick --threads 3 --keep --build-dir "$PWD/.rc_tmp/build"
```

(`--keep` so the script does not `rm -rf` the golden work dir; the driver-manifest test ran with `P1M_TEST_ROOT`.)
Exit **0**; log `.rc_tmp/quick.log`:

- Unit/golden binary: **166 test cases, 0 failed, 0 check failures** (includes `wp4_io_calib_refusals`,
  `wp4_io_plan_readers`, `wp4_io_setup_contract_v0119`, `wp4_io_reads_wp2_setup_bin`, `wp4_io_calib_plan_from_setup`,
  `wp4_io_merge_cli_and_driver_manifest` 37 s, `calibrate_command_end_to_end`, `calibrate_admission_before_allocation`,
  `pilot_only_equals_calibrate_pilot`, `calibration_admission_n1_rule`, `wp4_calib_backend_toy`).
- WP5 Slurm driver **28 tests OK**; competitor harness **OK** (missing optional packages reported, mocks tested);
  install script **9 guard checks OK**.
- WP4 golden against core (quick level): **540,419 checks, 0 failures**.
- NOT RUN: the `--full` level (T7 closed-forms Monte Carlo, the p = 100,000 RSS case, full-level golden fixtures);
  this re-check was asked for the quick suite. The first review's FULL-level golden run (7/7 fixtures, 0 failures)
  predates the fix commits; the fix round changes no scorer, transition or table arithmetic (the diff touches only
  readers, plan arithmetic, the calibrate command order, tests and docs), so I do not claim FULL coverage for `f44ff58d`.

Discipline: all changed files are under `engine_v4/`; largest changed file `tests/test_island.cpp` 108,762 bytes; the
two fixtures 8.5 and 13 KB; no new hard-coded paths (the fixture directory comes from `V4_FIXTURE_DIR`).

## Notes (not blocking, no grade)

- INTERFACES.md's header line still reads v0.1.13 while the changelog runs to v0.1.20. The v0.1.19/20 entries say the
  header moves with PR #45 (WP1's change); nothing for this PR to do, but WP1 should bring the header up to date when
  #45 lands.
- The allocation probe (and so the "before any allocation" evidence) counts C++ `operator new`, not `malloc` or mapped
  pages. The bounded readers use `mmap` and O(J) / O(sections) vectors; at p = 10⁶ the largest is `blk_ptr`'s J + 1
  entries, at most 8 MB (blocks of 1). No 1M RSS claim is made here.
