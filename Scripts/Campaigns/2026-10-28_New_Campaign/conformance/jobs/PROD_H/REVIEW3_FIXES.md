# REVIEW3_FIXES — PROD-H bundle, response to Sol review 3

Source: `conformance/review/CONF2B_REVIEW3_sol.md` (findings R3-1, R3-2, R3-3).

## Progress

- [done] Step 0: read review, bundle, tests (design: common.sh gets nc_job_state / nc_abort_accepted / nc_clear_uncertain; wrapper exit 11 = scheduler state unknown, kept + resumed; guard inside wrapper new-job branch; make_manifests nc_verify_manifest)
- [done, untested] runner edits for R3-1, R3-2, R3-3 (common.sh, p5_scan_run.sh, p5_submit.sh, rerun.sh, make_manifests.sh)
- [done] regression tests written (test_shell2.sh Sol-review-3 block + rerun assert; stubs squeue one-shot outage, sbatch arm)
- [done] JOB.md rev 3 edited; full suite run 1 (20261030T000326) was killed at 57 shell cases by a server restart (no failures seen)
- [done] full suite run 1 was NOT killed: it finished 01:05:59Z, rc 0 (run 2 never started). The worker was cancelled by the manager after the restart.
- [done by manager] TESTS.md update
- [done] full suite detached (run 1)
- [done by manager] final table

## Findings table

The Sonnet worker made the runner and test edits and JOB.md revision 3. A session restart at 00:20:54Z interrupted it; the manager cancelled it (single writer), let its live suite run finish, and filled in this table.

| # | Fix (file:line) | Tests (`tests/test_shell2.sh`, block "Sol review 3"; plus line 92) |
|---|---|---|
| R3-1 should-fix: unknown scheduler state is not failure | `runner/common.sh:123-170`: job state probe where "unknown" is never "failed"; `nc_abort_accepted` cancels by explicit id and leaves an UNCERTAIN marker until squeue AND sacct prove the job terminal. `runner/p5_scan_run.sh:16` and its re-check path: a squeue/sacct failure is exit 11, and the job record, table and receipt are KEPT; the next call RESUMES the same id. `runner/p5_submit.sh:14-15,75,151`: a scan is retired or relaunched only when proven terminal. `runner/rerun.sh:29,72`: the same rule for an aborted rerun. | Full parent: accepted scan, transient squeue failure, repeat invocation → exactly ONE sbatch, records kept, the same job resumed. Wrapper: unreadable sacct or squeue → exit 11, kept, resumed. Uncertain post-acceptance abort → no new scan until proven terminal, then one. rerun.sh: UNCERTAIN blocks until proven (lines 92, 431-471) |
| R3-2 should-fix: guard inside the scan wrapper | `runner/p5_scan_run.sh:13` and its new-job branch: `nc_run_guard` (home ≤ 9.6 GiB, campaign ≤ 0.5 GiB, behavioural probes) with a planned 5 MB, before sbatch, for direct primary and final calls. A small guard receipt is kept. A re-check of an existing job never calls the guard or resubmits. | A denying guard on direct final and primary calls → exit 1, no sbatch, refusal receipt. A guard with the superseded limits → refused. An allowing guard → one sbatch and GUARD_CHECK_OK. A re-check never resubmits (lines 473-488) |
| R3-3 minor: empty result folder | `runner/make_manifests.sh:19,42` (`nc_verify_manifest`): a zero-file folder gets a 0-byte MANIFEST.sha256 and `files=0` in the summary; empty membership is validated without `sha256sum -c`, on the first pass, on rerun and after the commit. JOB.md documents the laptop check for an empty folder. | First pass with an empty p1000 folder → 0-byte manifest, files=0. Reuse after commit. A file added later → refused. Why `sha256sum -c` is never used on an empty manifest. Laptop check passes, and a stray file fails it (lines 491-506) |

**GNU time (HQ add-on, Sol review 4 scope).** PROD-H calls no external `time` binary: no `/usr/bin/time` and no `-f '%e…'` format anywhere in `runner/`. Its runtime and accounting come from the adapter's `runtime_s` and from `sacct` (`final_accounting.sh`). No change is needed; the pilot fix is in `code/lowp/pilot/` (revision 7c).

## Final suite (`tests/run_all_20261030T000326.out`, rc 0; finished 2026-10-30T01:05:59Z)

Python 51/51 · shell **197/197** (171 before, +26 review-3 cases) · real CLI parser 6/6 · syntax 27/27 · tables 1/1 · **overall exit 0**. The run started at 00:03:26Z; no runner, stub or test file changed after that. Only JOB.md (docs) and this file changed.
