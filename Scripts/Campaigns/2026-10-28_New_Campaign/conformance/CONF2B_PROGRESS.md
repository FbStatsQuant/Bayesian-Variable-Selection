# CONF-2b progress (crash-recovery log; updated after each step)

Last update: 2026-10-29 23:25Z (CONF-2b manager).

## Done

1. **D20 cmp2 amendment.** ACCEPT on job 2455971; dry runs and controls behave (`jobs/CONF_NOTS_IDENTITY/ACCEPTANCE_2455971_D20.md`). Sol: ACCEPT (review 1).
2. **Regression a/b/c and lane G.** 0 FAIL in every section (`work/v2_2_1_regression/RESULTS.md`); Terra verification; F1 mutation check.
3. **Fork retired.** `code/lowp/smc/` is a README pointer only; ledgered.
4. **Pilot bundle.** Revision 7b: shell 54/54, negative 89/89, frozen check OK (`code/lowp/pilot/LOCAL_TEST.md`).
5. **Sol review 1.** Fixed F1–F7 (`review/CONF2B_REVIEW1_disposition.md`).
6. **Sol review 2.** v2.2.1 items fixed: R2-3 (scanner, no fallback) and R2-2 (a2 classifier) (`review/CONF2B_REVIEW2_disposition.md`).
7. **Current v2.2.1 manifest.** `code/core/v2_2_1.SHA256SUMS`, sha256 df4e7cf0e20981ef9fe4632fe2280355cbdb9e15d2dd724f1615b2c232054c41 (27 files). Diff: 519 lines, sha256 26303af84092f23179d8e02fd0d361693b2a337e8e6fcdaf111c7fe220ec5860.

## Running / in recovery

- **PROD-H fixes for Sol review 2** (R2-1 blocking; R2-4..R2-10; Q1 qos; Q2; accounting label). The first worker died (API error, about 16:59Z) after partly editing `runner/` and `tests/`. It wrote no `REVIEW2_FIXES.md`; the last suite run (14:40Z) predates its edits.
  - Recovery: audit the partial edits against Sol's pre-fix copy, then finish with a new worker. The worker runs the suite as a detached background job with an on-disk log.
  - 20:15Z: baseline and partial-edit diffs saved in `work/prodh_review2/`. A new Sonnet worker was launched to audit and finish. Its own progress is in `jobs/PROD_H_DRAFT/REVIEW2_FIXES.md` ("Progress" section).

- 22:05Z: the second PROD-H worker also died (the Claude worker OAuth expired at about 20:36Z). Its state: runner fixes and test_shell2 rewritten; JOB.md rewritten (revision 2); py suite 51/51; shell suite 164 pass / 7 fail (tests/shell_run_20261029T203602.out). The 7 failures: R2-6/R2-9 make_manifests (4) and R2-5 cleanup_terminal (3). The manager is diagnosing them directly.

- 22:25Z: the 7 shell failures are diagnosed and fixed by the manager. (1) make_manifests.sh parsed only the `hash  path` line form; Git Bash writes `hash *path` (binary marker), so every rerun saw an INCONSISTENT manifest (4 failures). The fix normalises on writing and accepts both on reading. (2) cleanup_terminal.sh crashed with exit 1 under pipefail when p5_attempts/ does not exist, i.e. a run without P5, which would also happen on NOTS (3 failures). Full suite rerun launched detached: tests/run_all_<stamp>.out/.rc.

- 23:20Z: PROD-H suite CLEAN: py 51/51, shell 171/171, CLI 6/6, syntax 27/27, tables 1/1, exit 0 (`tests/run_all_20261029T225330.out`). The last failure was a test over-count (the home line also matched "manifest reused"). `REVIEW2_FIXES.md` items table filled; `TESTS.md` updated. Next: Sol review 3.

- 23:30Z: Sol review 3 launched (new delegate_task): v2.2.1 R2-2/R2-3 + freeze verdict; PROD-H review-2 fixes. Output: `review/CONF2B_REVIEW3_sol.md`.

- 23:55Z: **Sol review 3:** v2.2.1 YES, FREEZE; PROD-H NOT READY (0 blocking; should-fix R3-1 scan retirement on a scheduler-query failure, R3-2 no disk guard on direct scan submission; minor R3-3 empty-folder manifest).
- 00:00Z: **v2.2.1 FROZEN.** FROZEN section in CHANGES_v2_2_1.md; final manifest sha256 d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1 (27 files; only CHANGES differs from the one Sol verified, df4e7cf0…); diff 527 lines, fabce9fa…; CODE_LEDGER entry. Pilot and PROD-H frozen checks pass.
- 00:05Z: R3-1..R3-3 delegated to a Sonnet worker (state in `jobs/PROD_H_DRAFT/REVIEW3_FIXES.md`). Then a narrow Sol confirmation (review 4), then rename PROD_H_DRAFT to PROD_H.

- 00:25Z: session restart at 00:20:54Z. State: the R3 worker made all runner and test edits plus JOB.md rev 3; its suite run `run_all_20261030T000326` is STILL LIVE (started 00:03Z; the worker thought it dead); its relaunch (002250) never started. The worker task was cancelled so the manager is the single writer. Pilot GNU-time fix (HQ add-on) not started: `slurm/common.sh` unchanged. PROD-H has no external `time` call (grep: no `/usr/bin/time`, no `%e/%U/%M` format).

- 00:45Z: **Pilot GNU-time fix done by the manager** (revision 7c). `slurm/common.sh` resolves /usr/bin/time, then /opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time; GNU verified by --version and an -f/-o probe; per-task record LOG/env/time_bin_*.txt; sizing arms exit 68 without it; infra arms continue. New `tests/test_gnu_time.sh` 30/30. JOB.md and CHANGES updated. Pilot suites rerunning detached (tests/logs_v2_2_1/*.rc). PROD-H suite `run_all_20261030T000326` still running.

- 01:15Z: **Pilot suites clean** (rev 7c): shell 54/54, GNU time 30/30, negative 89/89 (rc files in tests/logs_v2_2_1/). **PROD-H suite clean** (rev 3): py 51/51, shell 197/197, CLI 6/6, syntax 27/27, tables 1/1, rc 0 (run_all_20261030T000326). REVIEW3_FIXES.md table and TESTS.md filled. Next: Sol review 4.

- 01:20Z: **Sol review 4:** pilot READY for HQ → OPS (GNU time fix accepted; minor R4-2 numeric pattern); PROD-H NOT READY (should-fix R4-1: overlapping scan calls can retire another call's live job record); frozen tree 27/27 verified.
- 01:25Z: manager fixes, not yet suite-tested.
  - R4-2: pilot `slurm/common.sh` probe line requires valid decimals and an integer RSS; `tests/test_gnu_time.sh` 37/37 (7 new controls).
  - R4-1: PROD-H `p5_scan_run.sh` takes an atomic submission lock per run/phase (exit 12 for a concurrent caller) and writes `p5_scan_<phase>.outcome`. `common.sh nc_retire_scan` needs the EXPECTED id: it retires only if the record names that id and squeue AND sacct prove it terminal. `p5_submit.sh` retires on exit 4 only by the outcome id, never on 5, refuses on 12, and passes the verified id elsewhere. `tests/test_shell2.sh` has a new R4-1 block (held lock; real overlap with a 45 s sbatch delay → one sbatch; exact-id retirement); `tests/stubs/sbatch` has STUB_SBATCH_DELAY.
- 02:15Z: the 01:27Z launch never ran (a permission prompt; HQ interrupted it). Relaunched SEPARATELY via scripts in `work/conf2b_runs/`: pilot suites → `work/conf2b_runs/pilot_20261030T0215Z/`; PROD-H suite → `work/conf2b_runs/prodh_20261030T0216Z/` (each with *.rc and DONE).

- 02:45Z: **pilot READY for OPS.**
  - Sol review 4: READY (GNU time fix accepted). Its minor R4-2 is fixed, and the suites pass on the final files: shell 54/54, GNU time 37/37, negative 89/89, all rc 0 (`work/conf2b_runs/pilot_20261030T0215Z/`).
  - Bundle: `code/lowp/pilot/`, revision 7c + R4-2. It reads the frozen v2.2.1 manifest (sha256 d880afdb…) at run time.
  - OPS pre-check: `/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time --version` prints `time (GNU Time) 1.9`.

- 03:15Z: **PROD-H suite CLEAN with the R4-1 fix:** py 51/51, shell 206/206 (+9 R4-1), CLI 6/6, syntax 27/27, tables 1/1, rc 0 (`work/conf2b_runs/prodh_20261030T0216Z/`). `REVIEW4_FIXES.md` written; JOB.md rev 4 (exit-12 / stale-lock note). Sol review 5 (narrow R4-1 re-check) launched → `review/CONF2B_REVIEW5_sol.md`.

- 03:40Z: **Sol review 5:** R4-1 PARTIAL; PROD-H NOT READY. Two should-fix findings:
  - R5-1: retirement check-to-move race;
  - R5-2: TERM/HUP/INT during an in-flight sbatch released the lock.

  Frozen tree 27/27.
- 04:05Z: manager fixes.
  - `common.sh`: shared `nc_scan_lock`/`nc_scan_unlock` (refuses to release while `IN_FLIGHT` exists). `nc_retire_scan` takes the lock for check, prove and move.
  - `p5_scan_run.sh`: uses the shared lock and writes `IN_FLIGHT` (job name, user, since) before sbatch. It clears the marker only on a journaled id, a sbatch rejection, a proven-terminal abort, or when the UNCERTAIN marker takes over.
  - Stubs: sacct gains `STUB_SACCT_DELAY`.
  - `test_shell2.sh`: R5 block (slow retirement vs. a second retirement / scan call / late retirement; TERM/HUP/INT in flight keep the lock and the next call exits 12; sbatch rejection releases).
  - JOB.md: stale-lock recovery with IN_FLIGHT (find the job by name, cancel by id, then remove).
  - Full suite launched → `work/conf2b_runs/prodh_20261030T0405Z/`.

- 04:50Z: suite `prodh_20261030T0405Z`: py 51/51, shell 219/220. All 14 new R5 cases pass. The 1 failure is an R4-1 case grepping the OLD lock message ("another call is submitting"); the exit code was right (12). Grep updated to the new wording. Rerun → `work/conf2b_runs/prodh_20261030T0450Z/`.

- 05:55Z: **pilot rev 7d (HQ D44, after the OPS-4 STOP at P0a):**
  - B1: P0a is a cross-platform generator check (`code/lowp/R/lowp_verify_nots.R`): exact on what the fits consume; tolerance 1e-12 × max(1, |sealed|) on the regenerated floats; maxima reported.
  - B2: unlock reports LOCK_NEVER_RAN and verifies against `STAGED_SHA256.txt` (`truth_wave.sh`).
  - B3: the clean-up re-executes itself from memory (`cleanup_pilot.sh`).
  - New tests: p0a_tolerance 8/8, unlock 7/7, cleanup_inplace 3/3. Existing: shell 54/54, GNU time 37/37, negative 89/89, all rc 0 (`work/conf2b_runs/pilot7d_20261030T0520Z/`).
  - Docs updated (JOB, CHANGES, LOCAL_TEST rev 7d).
  - Sol narrow check launched → `review/PILOT7D_SOL.md`.

- 07:40Z: **pilot READY for OPS (rev 7d).**
  - Sol PILOT7D: READY WITH MINOR FIXES (all Low). R7D-1 (names/dimnames exact), R7D-2 (staging list must cover each truth file exactly once), R7D-3 (relative paths resolved before `cd /`; the dry run stays put) and R7D-4 (test noise sign) are fixed, each with a test.
  - Final suites on the final files: P0a 9/9, unlock 10/10, clean-up 5/5, GNU time 37/37, shell 54/54, negative 89/89, all rc 0 (`work/conf2b_runs/pilot7d_20261030T0710Z/`).
  - Frozen tree unchanged (Sol: 27/27).
  - OPS restages from `code/lowp/pilot/` (`lowp_verify_nots.R` is in `code/lowp/R/`, staged with the bundle).
- 07:40Z: PROD-H suite `prodh_20261030T0450Z`: shell **220/220**, CLI 6/6, syntax 27/27, tables 1/1. Python 50/51: the one failure is a test-timing flake (the "540 s on-time" gap measured > 600 s on the heavily loaded machine). The test now uses 420 s and 30 s seeds with slack; Python suite rerunning (`py_tests_rerun_0720.log`).

- 08:15Z: **PROD-H suite clean on the R5 fixes:** shell 220/220, Python 51/51 (rerun after the cadence-test timing fix), CLI 6/6, syntax 27/27, tables 1/1. `REVIEW5_FIXES.md` written. Sol review 6 (narrow R5-1/R5-2) launched → `review/CONF2B_REVIEW6_sol.md`.

- 09:20Z: **Sol review 6:** R5-1 RESOLVED; R5-2 PARTIAL, with new should-fix **R6-1**: a nonzero sbatch status was treated as "not accepted", clearing IN_FLIGHT and the lock. A client killed after acceptance let a duplicate scan through (TERM and KILL reproduced). Frozen tree 27/27.
- 09:40Z: manager fix.
  - `p5_scan_run.sh`: on ANY nonzero sbatch status, IN_FLIGHT (with `client_status` and stderr) and the lock are KEPT and the exit is **13** (acceptance UNKNOWN).
  - `p5_submit.sh`: refuses on 13 with the manual-resolution message.
  - JOB.md: step 0 for exit 13.
  - Tests: stub sbatch `STUB_SBATCH_ACCEPT_THEN_DIE`; test_shell2 "Sol review 6" block (client status 143/137 → exit 13, lock kept, the next call exits 12, exactly one acceptance; exit 42 → 13 with stderr recorded; parent → exit 2 "wrapper exit 13"). The old boundary case, which asserted lock release on a rejection, is replaced.
  - Full suite launched → `work/conf2b_runs/prodh_20261030T0940Z/`.

- 11:20Z: **PROD-H suite clean with R6-1:** Python 51/51, shell 225/225 (6 R6-1 cases), CLI 6/6, syntax 27/27, tables 1/1, rc 0 (`work/conf2b_runs/prodh_20261030T0940Z/`). `REVIEW6_FIXES.md` written. Sol review 7 (narrow R6-1) launched → `review/CONF2B_REVIEW7_sol.md`.

- 13:10Z: **Sol review 7:** R6-1 RESOLVED; **PROD-H READY WITH MINOR FIXES** (D48 path). Frozen tree 27/27.
  - R7-1 (low): the diagnostic append to IN_FLIGHT is now best effort, so exit 13 is always reached. Regression test (stub `STUB_BREAK_INFLIGHT`).
  - R7-2 (low): JOB.md unlock rule; time or empty queries never authorise an unlock.
  - Final full suite launched → `work/conf2b_runs/prodh_20261030T1310Z/`. Then rename to PROD_H and send the final report.

- 14:30Z: **HQ D49 folded in:** PROD-H default throttles 30 + 30 (60 tasks = 120 billed CPUs; 188 with PROD-L at 68, within 192).
  - Changes: `submit.sh` default. JOB.md documents the billing (1 CPU = 2 billed), the 192 ceiling, the `scontrol update ArrayTaskThrottle` raise after PROD-L, and that the ≤ 100 task guard counts PROD-L.
  - Tests adjusted: the vectors (%30); the fixtures whose overflow depended on the old 100 (30 → 41 running tasks, %1 → %41). New D49 cases: PROD-L at %34 + 60 passes; PROD-L %50 + 60 is refused.
  - The run started at 13:10Z was stopped (it tested superseded files). Final full suite launched → `work/conf2b_runs/prodh_20261030T1430Z/`.

## Next

0. (done) pilot READY for OPS (rev 7d), reported to HQ.
0c. Sol review 6 → if READY: rename PROD_H_DRAFT to PROD_H, banner "Reviewed (Sol review 6), for HQ, then OPS", ledger path, final report.
0b. Sol review 5 → if READY: rename PROD_H_DRAFT to PROD_H, banner "Reviewed (Sol review 5), for HQ, then OPS", ledger path; final report.
1. Sol review 4 (a NEW delegate_task): R3-1..R3-3 (PROD-H) + the GNU time fix (pilot rev 7c; PROD-H has no external time). Output: `review/CONF2B_REVIEW4_sol.md`.
2. If READY: rename `jobs/PROD_H_DRAFT` to `jobs/PROD_H`; JOB.md banners "Reviewed (Sol review 4)"; CODE_LEDGER path.
3. Final report to HQ (OPS-4 can resume).

## FINAL (2026-10-30 ~14:45 local)

- **PROD-H:**
  - final suite clean: Python 51/51, shell 229/229, CLI 6/6, syntax 27/27, tables 1/1 (`work/conf2b_runs/prodh_20261030T1430Z/`);
  - renamed `jobs/PROD_H_DRAFT` → `jobs/PROD_H`; JOB.md "REVIEWED (Sol reviews 2–7; HQ D48/D49) — for HQ, then OPS";
  - `BUNDLE_SHA256SUMS` (53 files, 2a2a8b1f…);
  - D48 class (ii) items: none.
- **Pilot:** rev 7d READY for OPS (reported earlier).
- **Ledger:** CODE_LEDGER entry "2026-10-30 — job bundles released".
- **Frozen v2.2.1:** unchanged (d880afdb…, 27/27).
- **CONF-2b is DONE.** Final report sent to HQ.
