# PR #47 re-check — WP7 O1, fix commit 02eea579

**Verdict: MERGE.** Finding 1 (MAJOR) of the first review is closed. 0 CRITICAL, 0 MAJOR, 2 MINOR (both non-blocking).

Scope: `git diff e3ca4716 02eea579`, 3 files, all inside `Scripts/SMC_BVS/engine_v4/` (`island.h` comment, `island_run.h` +8/-3, `tests/test_island.cpp` +48). Read only: nothing pushed, commented or branch-changed. Both commits were extracted with `git archive` into `.rc_tmp/old` (e3ca4716) and `.rc_tmp/new` (02eea579) and built there (CMake Release, `-j3`, `nice -n 19`, `OMP_THREAD_LIMIT=3`, `TMPDIR` under `.rc_tmp/tmp`). Nothing deleted.
Host: the department's Linux box, gcc as in `run_tests.sh` output (`.rc_tmp/suite_new.txt`).

## 1. I1 on every exit — PASS

`island_run.h` (new head): `check_stores()` moved out of the `if (status == 0 || status == 1 || calib)` export guard to a single unconditional call (line ~694) directly after the `try/catch` that sets status 2 (numerical_failure) / 3 (resource_limit, step-budget exit and caught `bad_alloc`) and after the calibration `sync_ledgers()`/`rebuild_prefix()` handling, and before `res.T`, the status-1 assignment and every export / `std::move` of a store.
- Covers ok (0), stopped (1, which also still has the checkpoint guard), numerical_failure (2), resource_limit (3) and the calibration roles, because it precedes every status branch.
- `check_stores()` (unchanged) checks top, `lead0` and `lead1` (`cfg.leaders`), each by generation, so a generation already checked by the last checkpoint is not rescanned. Skips only when `check_store` and `check_store_each_step` are both false; `check_store` defaults to true and the production path never turns it off.
- It sits outside the `try`, so a violation throws `v4::Error(internal_error, "store invariant I1 violated (...)")` out of `run()`. No `IslandRun` is returned, so there is no object to hand to `write_island_file()`: no island file is written for that island. (Failure files that did pass I1 are still written, with the empty top store and no estimates as before; GUARD-W intact.)
- Precedence: INTERFACES `fit_status` order is invalid_input, internal_error, numerical_failure, resource_limit, ...; §7 "invariant violations (I1–I7) → internal_error". A corrupt store now wins over numerical_failure and resource_limit, as specified. An admission refusal before the engine exists has no live store and correctly runs no check.
- Exception safety of the new check on failure paths: `compact_locked()` / `compact_parallel()` build the new kept run `nk` and publish it last (`k = nk; gen.fetch_add`), so a `bad_alloc` mid-compaction leaves the previously published, valid run in place; a failure exit cannot spuriously turn into `internal_error`. The existing `oom_in_parallel_compaction_is_resource_limit` (OOM inside `compact_parallel`) still passes with status 3.

## 2. Reproducer as a test — PASS (fails on e3ca4716, passes on 02eea579)

New test `store_check_on_failure_exits` (`test_island.cpp`, the reviewer's configuration: AR(0.6) n=100 p=300 data seed 43, seed 42, island 3, N=48, L=Hm=2, B=14, label-major, G=16, 3 threads, `test_admission_k=.5`, `mem_budget = plan + 1024`, `test_corrupt_store_step=1`). Cases: (a) step-budget exit, valid store → status 3, `store_checks==1`, failure file written and read back as `resource_limit`; (a') same, corrupted → must throw `internal_error` "I1"; (b) caught OOM in phase A, valid → status 3 with 1 check; (b') same, corrupted → `internal_error`.

Same test source on both builds (test file copied into the scratch `old` tree, rebuilt):

```
== e3ca4716 + new test   (.rc_tmp/repro_old.txt)
FAIL ... :1097 budget exit, valid store: status 3 checks 0
FAIL ... :1091 budget exit, corrupted store: returned status 3 (mem_budget: predicted peak 21 MiB > budget 13 MiB after step 1 ...), checks 0
FAIL ... :1116 oom exit, valid store: status 3 'resource_limit: out of memory inside a parallel region' checks 0 passes 35
FAIL ... :1091 oom exit, corrupted store: returned status 3 (resource_limit: out of memory inside a parallel region), checks 0
[FAIL] store_check_on_failure_exits   1 test cases, 1 failed, 4 check failures

== 02eea579              (.rc_tmp/repro_new.txt)
[PASS] store_check_on_failure_exits   1 test cases, 0 failed, 0 check failures
```

The old run reproduces the first review exactly (status 3, `checks 0`, corrupted store not detected, "predicted peak 21 MiB > budget 13 MiB after step 1").

## 3. Same bits — PASS

`v4_tests t3_invariance` on both builds (all 8 PM/LM, thread, G, tile configurations per arithmetic form pass at both commits); every reference and per-configuration hash line is identical between e3ca4716 and 02eea579 (`diff` of the full hash output: no difference):

| Form | e3ca4716 | 02eea579 | first review (base 8b7f89be) |
| --- | --- | --- | --- |
| T3 bit | `44a15bfc6fb8d233` | `44a15bfc6fb8d233` | `44a15bfc6fb8d233` |
| T3 class A | `d2df149413596a19` | `d2df149413596a19` | `d2df149413596a19` |

The fix only adds a read-only scan in the previously unguarded exits and removes the old guarded call; the successful-path control flow and every output are unchanged. (I did not rerun the independent island seed-43 section digests of the first review; the successful-run path is code-identical to e3ca4716 apart from the call being hoisted, and the hashes above and the 119-case suite cover it.)

## 4. Quick suite — PASS (with one environment note)

`TMPDIR=.rc_tmp/tmp OMP_THREAD_LIMIT=3 nice -n 19 bash tests/run_tests.sh --quick --threads 3 --build-dir .rc_tmp/build_new` on 02eea579 (`.rc_tmp/suite_new.txt`):
- C++: 119 cases (118 at e3ca4716 + the new one); 118 passed, 1 failed in the runner as invoked, with `P1M_TEST_ROOT` pointing to `.rc_tmp/root`. The one failure is `wp4_io_merge_cli_and_driver_manifest`, the same environment-only failure as in the first review: the test's driver subprocess puts its dept dir under `$TMPDIR/v4test_*/dept`, and the driver's department guard (`p1m_driver.py:205`) refuses it unless `P1M_TEST_ROOT` contains it (exit 64). **Environment note for the brief: `.rc_tmp/root` is not enough; use `P1M_TEST_ROOT="$TMPDIR"` (both inside `.rc_tmp/`).**
- Rerun of the whole `v4_tests` binary with `P1M_TEST_ROOT=$TMPDIR` (`.rc_tmp/v4tests_new_rerun.txt`): **119 test cases, 0 failed, 0 check failures.**
- WP4 reference goldens: 528,081 checks, 0 failures. WP5 Slurm driver 17 tests OK; competitor harness OK; install-script guards OK (9 checks).

## Findings

1. **MINOR — numerical_failure / calibration failure exits are covered by structure, not by a corrupting test.** `island_run.h` placement is correct (the check precedes every status branch, outside the `try`), and existing failure goldens pass, but the new test's closing comment (c) claims coverage "by the same call" without a test that corrupts a store and then fails numerically; no injection hook exists for a final-role numerical failure after step 1. Not a defect in the fix; a cheap hook (`test_fail_step`) would let a later package pin it. No action needed for this merge.
2. **MINOR — cost note on failure exits.** A failing island that held a changed store now pays one parallel I1 scan (generation-gated, so at most one per changed store, and none after a checkpoint that just checked it). That is the intended price of the contract; at 4e7 entries it is the same parallel scan already costed in O1. No change requested.

No other deviations found: nothing outside `engine_v4/`, no `core/` change, no new hard-coded paths or large files, no flag or arithmetic change.

## Files
- Review: `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-5676de1e-ec729dd2fe01f5ca/.rc_tmp/PR47_recheck.md`
- Evidence in the same directory: `repro_old.txt`, `repro_new.txt`, `t3_old.txt`, `v4tests_new_rerun.txt`, `suite_new.txt`.
