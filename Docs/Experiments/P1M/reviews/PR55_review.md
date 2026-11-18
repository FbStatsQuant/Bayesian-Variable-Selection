# PR #55 review (builder 7, O5: T5 harness at 10^5, 10^6 calibration-pilot command, D-32 ISA rules, cost records)

Reviewer: independent review sub-agent (Sonnet 5.5; Owls; read only). Reviewed `git diff 82e985eb c1a8016e` (head c1a8016e, 21 files,
+1227/-20, all under `Scripts/SMC_BVS/engine_v4/`; no file over 50 MB; no new hard-coded absolute path except the documented
`$HOME/SMC_Engineering_Department` in the runbook).

## Verdict: ACCEPT-WITH-FIXES

Cost safety holds for both example plans. D-32 is implemented as the decision says. The pilot island is the first island of
`calibrate --mode V` (the test compares them row by row). The cost-record plumbing is sidecar or timing only. One MAJOR fix is needed
before the manager submits P7: the P7 batch directory also contains a full-fit `submit.sh`, and the driver prints and ledgers 3352 core-h
for it, not the 144 that will be submitted (finding 1). The remaining findings are MINOR.

Counts: CRITICAL 0, MAJOR 1, MINOR 6, INFO 3.

## Test run (Owls, `nice -n 19`, 3 threads, scratch and TMPDIR under `<worktree>/.rc_tmp/tmp`, detached at c1a8016e)
- `tests/run_tests.sh --quick --threads 3`: **EXIT 0, 128 `[PASS]`, 0 `[FAIL]`**. Includes `calibrate_command_end_to_end`,
  `cost_record_per_step` (now also `info --meta 1` and `binary.island_isa`), `pilot_only_equals_calibrate_pilot` (1 and 3 threads;
  pilot T = 10, 22 rows each; calibrate wrote 9 cost records, 8 diagnostic), `merge_refuses_mixed_fma_families`,
  `wp4_io_merge_command_e2e` (timings keys and `island_isa` in fit.json), the golden island/calibration tests against core, and the
  WP4 R golden suite (528,081 checks, 0 failures). WP5 competitor and install-script checks OK.
- `python3 tools/slurm/test_p1m_driver.py` (also inside run_tests): **Ran 27 tests, OK**.
- `cmake -DV4_ISLAND_ISA=sapphirerapids -DV4_TESTS=OFF` configure plus `make -n`: `provenance.cpp` gets
  `-DV4_ISLAND_ISA_STR="sapphirerapids"`; `island_a.cpp` and `calib_run.cpp` get a trailing `-march=sapphirerapids` (it wins over the
  target's `-march=x86-64-v2`). Not compiled: only the configure and the command lines were checked.
- Driver dry runs (`P1M_TEST_ROOT=$TMPDIR`, `--dept` and `--out` under `.rc_tmp/tmp`):
  - `plan_T5_1e5.json`: 23 files, 21 tasks, **worst case 366.0**. Hand sum: setup 32x0.5 = 16, calibrate 64x1 = 64, islands 16x48x(1/3) = 256,
    merge 16x0.5 = 8, eval 8x0.75 = 6, isa_check 48x(1/3) = 16. Equals the per-file "Worst case" headers (8+16+64+16+256+6) and is <= `core_h_cap` 400.
  - `plan_P7_pilot_1e6.json`: 24 files, 20 tasks, **printed worst case 3352.0** (see finding 1). `submit_pilot.sh` header: 144.0
    (setup 48x1 + pilot 96x1; exactly the 144 cap, no slack).

## Checks requested

**(1) Cost safety.**
- T5: printed 366 = sum of CPUs x limits, <= 400, enforced by `core_h_cap` in the plan.
- `submit_pilot.sh` submits only `stage_setup.sbatch` and `stage_pilot.sbatch` (2 sbatch lines; the unit test counts exactly 2 calls). It refuses
  without `CONFIRM=yes` (exit 64, tested), without `SHA256SUMS` match, and without `bin/v4_pilot_island` (exit 66, tested).
  `submit.sh` also requires `CONFIRM=yes` (line 527 of the driver template).
- The generated pilot job: 96 CPUs x 1:00:00, `--no-requeue`, `--kill-on-invalid-dep=yes`, so the 96 core-h pilot cannot run longer or retry.
- Gaps: finding 1 (P7 cap not machine-enforced, full-fit script present, wrong printed number) and finding 5 (isa_check time limit).

**(2) D-32.**
- A V plan (plan-level `mode` or any fit `mode`) refuses an `island_isa` outside the FMA allowlist {x86-64-v3, x86-64-v4, sapphirerapids,
  icelake-server, cascadelake, skylake-avx512}; I confirmed `haswell`, `""`, `portable`, `x86-64-v2` all raise PlanError. `island_isa` is
  regex-limited to `[A-Za-z0-9_.-]+` (no shell injection). `p1m_cells.py` adds `island_isa` to every V plan (tested over all generated plans).
- `--constraint=sapphirerapids` is on all 6 T5 sbatch files (setup, calibrate, islands, isa_check, merge, eval) and on `stage_pilot.sbatch`
  (line 252 of the driver is unconditional, so it covers every task).
- One `smcbvs4` (built with `-DV4_ISLAND_ISA=<plan ISA>`) runs setup, calibrate, island, merge and eval; only the isa_check comparison binaries are
  other builds. The merge's scoring is the bit form (`BitFactory`, wp4_io.cpp:696/868), which is ISA-independent, so merge/tail/LS0
  carry no FMA-family dependence; the runbook says so.
- Merge refusal: `binary_compatible(MergeV)` rejects islands whose `island_isa` families differ (`portable`, `x86-64`, `x86-64-v2` = non-FMA).
  Tested on synthetic blocks and not on the merge CLI (findings 3, 7).
- T5 check: `against` defaults to `x86-64-v3` and must be an FMA ISA. `stage_isa_check.sbatch` re-runs island 1 with `smcbvs4_isa_check` (own manifest
  and output names, so no checkpoint clash) and `p1m_stage_cost.py isa` requires equal `meta.output_hash` plus equal name, dtype, dims and sha256 of every
  non-meta section. It also runs `v4_bench_island island 20000 64 $OMP_NUM_THREADS bit pm 1 128 geo:4 1 1` from three builds (sapphirerapids, x86-64-v3,
  x86-64-v2) and requires one output hash. I checked the argument list against `bench_island.cpp:306-308`.
- ISA recorded: `binary_block().island_isa` (so every record and every file's meta, `island_r.bin` included) and the top-level `fit.json` field.
- Not enforced at run time: island vs `calib.bin` family (finding 3).

**(3) `v4_pilot_island`.**
- It runs the same sequence as `calib_run.cpp`: `calib::budgets` (B from it), `settings_from(b, bounded)`, `read_setup`, the data-hash check,
  `kbar = max(8, |mode_S|+1)`, `calib_memory_plan`, `load_start` and `load_neighbours`, the same `CalibRunnerConfig`
  (label-major, `inputs_bytes = start_bytes`), `LedgerConfig{islands 4, leaders, fresh_counters false}`, `offer_tables` (when `--with-ledger 1`, the
  default), and an `IslandSpec` equal to `LedgerBackend::pilot` (role Pilot, tier, iter 0, island 0, H, adaptive, Te, L, Hm,
  `resident_bytes = plan.ledger + plan.export_`, `mem_budget`). It takes the same seed.
- The seed in `stage_pilot.sbatch` is `run_manifests/<run>.json params.seed` (602020001 in the P7 plan). That is the same value the calibrate manifest carries.
- Memory: default `128G`. `mem_from_plan` is sized as `(island_plan.total [+ setup inputs]) x 1.15 / 0.9`, rounded up to 8 G, refused above 240G
  (tested). The task's `--mem-budget` is 90% of the allocation, as in calibrate.
- The pilot writes `pilot_plan.json` first (`calibrate --plan-only 1`, `|| true`), and the island's own admission refuses before allocating.
- Test `pilot_only_equals_calibrate_pilot` compares `phi`, `particle_rounds`, `sweeps`, `pairs`, `store_size`, `mean_S`, `act_cols`, `passes`, `step`, `kind`,
  at 1 and 3 threads, and also 1 vs 3 threads. Flips and offers are excluded (finding 8).
- Differences from calibrate, all benign: no `Driver::validate` (not applicable to the pilot), and no up-front `plan.resident >= budget` refusal (the
  island's own admission covers it).

**(4) Cost-record plumbing does not change science.**
- `cost_dir` only sets `IslandConfig::cost_path`, the non-authoritative sidecar (island_run.h:441-470, best effort, never fails the island);
  `verbose` only prints. `meta.cost` already existed (O2).
- `merge.h`: `t_islands`, `t_local` and `t_ls0` are `steady_clock` readings stored in `FitOut` and written to `meta.timings` and `fit.json`. They are
  not in any section. `wp4_io_merge_command_e2e` still requires thread invariance of every non-meta section.
- `info --meta 1` is read only. `p1m_stage_cost.py` is a reader (stdlib only).
- Residual: no test proves that `calibrate --cost-dir` / `--verbose` leaves `calib.bin` identical (finding 7a).

**(5) Hard-coded science constants.** None added. `rc.B = b.B` (from `calib::budgets`); `H, Te, L, Hm` from `settings_from` tier 0. The pilot
repeats `lc.islands = 4` and `kbar >= 8` (duplicated from `calib_run.cpp`; the test guards drift). `c.B = 14` remains only in the pre-existing
`tools/bench_island.cpp` (a benchmark, used here only for the bit-form hash comparison; the PR only moved a comment on that line).

## Findings

### MAJOR
1. **The P7 batch ships a full-fit `submit.sh`; the printed worst case and the ledger row are for it, not for the 144 core-h pilot; the 144 cap cannot be
   enforced.** Driver: `p1m_driver.py` main() print (line ~639), `ledger_row.md` (generate), `resolve()` pilot block (~l.120-165). Evidence (dry run of
   `plan_P7_pilot_1e6.json`): the printed line is `... 20 tasks, worst case 3352.0 billed core-h` and `ledger_row.md` records 3352.0. The directory contains
   `submit.sh` (setup -> calibrate 96x2h -> 16 islands 96x2h -> merge -> eval, 3352 core-h, over the 1,188 per-fit manifest limit), and its header
   says "submit.sh (the fit) needs HQ GO". Setting `"core_h_cap": 144` in the plan fails (`worst case 3352.0 ... exceeds ... 144.0`). So the 144 limit
   lives only in `submit_pilot.sh`'s header and `plan.resolved.json`. `submit_pilot.sh` itself is safe, but one wrong command
   (`CONFIRM=yes bash submit.sh` from the P7 directory) is a 3352 core-h job. The LEDGER admission figure would also be wrong, in the conservative direction.
   Fix (small): a plan key `"pilot_only": true` (or implied by `pilot` without `fits[].resources`) that (a) does not generate `submit.sh` or the
   calibrate/islands/merge/eval sbatch files, (b) prints `worst_case_pilot_core_h` and writes it to `ledger_row.md`, (c) applies `core_h_cap` to it
   (put `"core_h_cap": 144` in `plan_P7_pilot_1e6.json`). Also fix the `stage_pilot.sbatch` header (`# Submitted only by submit.sh`, copied from HEADER).
   Add a test for the printed figure.

### MINOR
2. **Pilot cap has zero margin.** 48x1 + 96x1 = 144 = the HQ cap, so any change to the setup limit trips it. Fine for now; the cap stays inside the HQ envelope (P7 <= 144).
   No change needed except noting it next to finding 1's `core_h_cap`.
3. **D-32 rule (2) is enforced by the driver (one binary) and by the island-vs-island merge check only.** `check_binaries` (wp4_io.cpp:458-468) compares
   each island to the first loadable island; it never compares an island with `calib.bin`'s binary block or with the merge binary. A V island run
   against a `calib.bin` from the other family loads without complaint. Suggested: the island command refuses a `calib.bin` whose `meta.binary.island_isa`
   family differs from its own (class A calibration output feeds N and the grid). Low urgency (one binary per fit).
4. **The `island_isa` family label can be wrong.**
   - `provenance.cpp:67-71` treats everything except `portable`, `x86-64`, `x86-64-v2` as FMA (`nehalem`, `sandybridge`, ... would be mislabelled).
   - More important: a build with `-DV4_WIDE_ISA=ON` and no `V4_ISLAND_ISA` compiles class A with `-march=x86-64-v3` (cmake/flags.cmake:5) but records
     `island_isa = "portable"` (non-FMA label). The merge would then accept it mixed with a true v2 `portable` build (same label, different class-A bits) and
     refuse it against `x86-64-v3`. The driver never uses `V4_WIDE_ISA`, so this is only a hand-built risk. Fix: record `x86-64-v3` when WIDE_ISA is ON
     without an override (or put both in the block).
5. **`stage_isa_check` has only the islands' 20-minute limit** (T5 plan: islands 48 CPUs, 0:20) for one island re-run (runbook: 4-14 min), two
   `smcbvs4 info --meta 1` verifications of the island files, and three bit-form bench runs at 48 threads. A slow island leaves the check unfinished
   after the run it validates. Give it its own limit (e.g. `isa_check.time` 40 min: 32 core-h, T5 total 382 <= 400). In addition,
   `isa_check.against == island_isa` is accepted (e.g. `sapphirerapids`) and makes the class-A comparison vacuous; reject it.
6. **INTERFACES.md was only partly updated** (the diff touches the cost lines in §5.1). Not documented: `island_isa` in the binary block (the §5.3 example
   and the "Binary consistency" bullet, which still says merge (V) needs "equal flags and libm binding" with no ISA-family rule), the fit.json `island_isa`
   field and `timings` keys (`merge_islands_seconds`, `tail_local_seconds`, `ls0_seconds`), `info --meta 1`, `calibrate --verbose`, and the
   `v4_pilot_island` tool. D-32 (4) points at those fields; add them to the contract (WP1 line).
7. **Test gaps (no failures found; nothing here fails today).**
   - (a) No check that `calibrate --cost-dir` / `--verbose` leaves `calib.bin` (non-meta section hashes) unchanged: both runs in the new test use `cost_dir`.
     Add a run without it and compare the section hashes.
   - (b) The mixed-family refusal is tested only through `binary_compatible()` on synthetic blocks; add a merge (FileIslandSource) run with two island files
     whose `meta.binary.island_isa` differ, expecting `binary_mismatch`.
   - (c) T5's isa_check and bit-form hashing run only on NOTS; the driver test uses fake benches. The first real check is the T5 run itself
     (the runbook states it).

### INFO
8. The test excludes `flips` (`flip_evals`) and `offers` from the pilot-vs-calibrate comparison, calling them "schedule-dependent". Please confirm
   that this is run-to-run execution-count variation in one binary (e.g. compare two `v4_pilot_island` runs), not a configuration difference between the two paths. Law-determined
   fields agree exactly, so the sampled state is not in question. The P7 report's `flips_per_step` is therefore not reproducible bit for bit.
9. `--plan-only` does not yet print the island plan (P5); until then `mem_from_plan` is refused by design (no `island_plan` key) and the default 128G applies.
   Matches the runbook.
10. Machine note: Owls load was ~22 with other reviewers' suites running; I did not touch their processes. Timings in the test log are not benchmarks.

## What was not checked
- Real NOTS behaviour (sbatch, queueing, the island/`setup` CLI that is still a stub on the base: runbook preconditions).
- Compilation with `-DV4_ISLAND_ISA=sapphirerapids` (the CPU here is Skylake-SP; configure and `make -n` only) and the AVX-512 / v3 / v2 class-A equality itself
  (D-32's measured claim; T5 will check it).
- Scale at 10^6 beyond code reading (no 32-bit overflow introduced: `mem_budget` is `uint64_t`, sizes are `uint64_t`/`double`).
