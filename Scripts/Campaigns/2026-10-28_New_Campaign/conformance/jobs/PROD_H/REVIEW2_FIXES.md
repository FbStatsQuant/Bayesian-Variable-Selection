# PROD-H review-2 fixes (resumed worker)

NOT YET REVIEWED — for Sol review, then HQ.

## Progress
- [done] Step 0a: audited runner edits: poll.py, common.sh, submit.sh, rerun.sh, p5_*.sh/sbatch, cleanup_terminal.sh, make_manifests.sh, accounting_summary.py look complete. Small gaps found: submit.sh sbatch_args write unguarded between accepted jobs; cleanup_terminal.sh does not skip paths inside an already archived lock dir.
- [done] Step 0b: audited tests: test_py.py (R2-1, R2-10, accounting, locks log) and test_shell.sh part 1 (R2-7 submit, R2-8, qos, scratch refusal log) and stubs (sbatch BREAK_JOURNAL/STUB_RUN_SCAN, Rscript killlock/summary) are updated. test_shell2.sh was NOT touched: still the old expectations (no qos, locks_cleared in home, scan on login node, no cleanup/manifest recovery tests).
- [in progress] Step 1: py suite run on current state (background; log /tmp/py_run.out, rc /tmp/py_run.rc; slow because output is buffered until the end).
- [done] small runner fixes: submit.sh guards the sbatch_args write (abort_submission), cleanup_terminal.sh skips paths inside an already archived lock dir and renames .tmp files inside archived lock dirs.
- [done] Step 2a: test_shell2.sh rewritten (rerun qos + R2-7, P5 scan job R2-4, Q2, SIGKILLed P5 unit c40 -> final scan -> cleanup -> manifests, R2-6, R2-9, primary-kill cleanup, accounting). Python suite on the dead worker's state: 51 passed, 0 failed.
- [in progress] Step 2b: run the shell suite detached (tests/shell_run_<stamp>.out/.rc) and fix failures.
- [done] JOB.md rewritten (revision 2: QoS check B2, cadence, hold states, scan job, cleanup, manifests, ceilings, scratch/home paths).
- [next] Step 3: rewrite test_shell2.sh (rerun qos+R2-7, P5 scan job R2-4, Q2, R2-5 cleanup, R2-6 manifests, R2-9 paths); small runner fixes (submit.sh sbatch_args guard, cleanup nested-path skip).
- [next] Fix/finish runner files; add tests; update JOB.md and tests/TESTS.md; run suite detached.

## Items (fix file:line, covering test)

Workers: the first PROD-H fix worker made most of the runner edits; it died at about 16:59Z. The second audited them, added small fixes, rewrote `test_shell2.sh` and `JOB.md`, and died at about 20:36Z (OAuth expired). The CONF-2b manager diagnosed and fixed the last 7 shell failures.

| Item | Fix | Test (suite) |
|---|---|---|
| R2-1 (blocking) C3 hold | `runner/poll.py:17-47,87-130`: per-job `hold_requested` / `hold_established` / `hold_failed` / `hold_not_needed`, confirmed with squeue (pending tasks held). Failed holds are retried on every later poll; the decision is HOLD_FAILED, the exit is 3, an URGENT_HOLD_FAILED.md is written; nothing is ever cancelled. | `tests/test_py.py`: "poll hold: ..." cases (failed, partial, retry on the next poll, established, the CLI exit 3) |
| R2-4 P5 scan as a compute job | `runner/p5_scan.sbatch` (1 CPU, 4G, 1 h, scratch logs); `runner/p5_scan_run.sh` (submits, records the id, verifies table + receipt); `runner/p5_submit.sh:14,78-81` (selection on `launchable`; refuses locked / incomplete / invalid_inspect) | `tests/test_shell2.sh` R2-4 cases (16): failed scan, no receipt, refusal, accepted scan |
| R2-5 terminal cleanup | `runner/cleanup_terminal.sh` (all recorded jobs dead in squeue + sacct; archive proven-stale locks and temp files, UNPROVEN left with exit 3; attempt records counted before and after). **Manager fix:** the attempt-record count crashed under pipefail when `p5_attempts/` is absent, i.e. a run without P5 (`:79,104`). | `tests/test_shell2.sh` R2-5 cases (15): SIGKILLed P5 child → final scan → cleanup → manifests; primary kill; unproven; live owner; temp inside a lock; sacct/squeue failure refuses |
| R2-6 manifests transactional | `runner/make_manifests.sh:38-75`: every folder preflighted, all temporary manifests built and checked, then committed; a rerun revalidates ("reused") and never replaces an inconsistent manifest. **Manager fix:** one line format `<hash>  <path>` (normalised on writing; `hash *path` from Git Bash/Cygwin accepted on reading, `:34-36,52,82`). Before, every rerun on Windows saw INCONSISTENT. | `tests/test_shell2.sh` R2-6 cases (7): later-folder failure then recovery, rerun on an unchanged tree, a file added → refused. **Manager test fix:** the rerun case counted the home line as a 4th "manifest reused" |
| R2-7 writes after an accepted sbatch | `runner/submit.sh:155-172` (`abort_submission`: cancel by explicit id, cancel failure recorded, exit 5); the same in `rerun.sh:66`, `p5_submit.sh:135`, `p5_scan_run.sh:71` | `tests/test_shell.sh` / `test_shell2.sh` R2-7 cases (10): a journal failure after accepted sbatch, a cancel failure |
| R2-8 throttle fail-closed | `runner/common.sh:64-89` `nc_campaign_throttle`: every queued fb31 array counts, whatever its name; a pending record without `%N` is unlimited; squeue failure refuses | `tests/test_shell.sh` R2-8 cases (5): a non-"smc" array, an unlimited array, squeue failure |
| R2-9 logs on scratch, home manifest | `polls.jsonl`, scan logs, refusal and lock logs, scheduler stderr → `LOGROOT` (`poll.py:30,55`; submit/p5 scripts). Home keeps receipts, state and summaries plus `HOME_MANIFEST.sha256` (`make_manifests.sh:77-91`, everything except `runner/`) | `tests/test_shell2.sh` R2-9 cases (8): no `*.log/*.jsonl/*.err/*.out` in home; home manifest coverage, round trip, tamper, refusal |
| R2-10 cadence | `runner/poll.py:5,45,129,245-258`: OPS polls every 5–10 min; a gap > 600 s is LATE and recorded, checked throughout active production | `tests/test_py.py` cadence cases (a 601 s gap) |
| Q1 QoS | `--qos=nots_commons` on every sbatch (precompile, primaries, reruns, P5, scan). JOB.md: OPS confirms the QoS first | shell cases check the vectors (`vectors_final.txt`) |
| Q2 P5 vs terminal exceptions | `runner/p5_submit.sh:11,62`: terminal, reconciled, reported `timeout`/`infra_repeat` do not block P5 and are never retried; live, not_run, rerun_queued, infra and orphan still block | `tests/test_shell2.sh` Q2 cases (4) |
| Accounting ceilings | `runner/accounting_summary.py:8-21,63-74`: native-fit-budget ceiling 10,100 core-h; requested-wall ceiling 10,540 (10,541 with the precompile) | `tests/test_shell2.sh` accounting case |

## Final suite (manager run, 2026-10-29T23:15Z; `tests/run_all_20261029T225330.out`, rc 0)

Python 51/51 · shell 171/171 · real CLI parser 6/6 vectors · syntax 27/27 · tables 1/1 · **overall exit 0**. Logs: `tests/summary.log`, `py_tests.log`, `shell_tests.log`, `cli_parser.log`, `syntax.log`, `tables.log`.
