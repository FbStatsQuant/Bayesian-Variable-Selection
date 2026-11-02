# PROD-H: fixes for Sol review 5 (CONF-2b manager, 2026-10-30)

Source: `conformance/review/CONF2B_REVIEW5_sol.md`. R4-1 was PARTIAL; two should-fix findings remained.

| # | Fix | Test (`tests/test_shell2.sh`, block "Sol review 5") |
|---|---|---|
| R5-1 retirement check-to-move race | See "R5-1" below. | A slow retirement A (sacct delayed 12 s) of failed job 8000 holds the lock: a second retirement B of the same id is refused (1); a scan call C resumes and judges the recorded job (exit 4) and submits nothing. A completes (0) and releases the lock. A new scan C2 submits ONE job. A LATE retirement of 8000 then refuses (1), and the newer record survives untouched |
| R5-2 catchable signals released exclusion during an in-flight sbatch | See "R5-2" below. | For each of TERM, HUP and INT sent while sbatch is in flight (stub delay 8 s): the wrapper ends non-zero and the lock with IN_FLIGHT (job name) is KEPT, with no job record; the next scan call exits 12 and submits nothing (still one sbatch); a retirement while the in-flight lock is held is refused. Boundary: an sbatch REJECTION leaves no IN_FLIGHT and no lock |

**R5-1 fix.** `runner/common.sh`: the shared lock `nc_scan_lock`/`nc_scan_unlock` (`RUN_DIR/p5_scan_<phase>.submit.lock`, owner.txt with role) is used by submission AND retirement. `nc_retire_scan` takes it, then re-reads the record, proves the expected id terminal (squeue AND sacct) and moves the artefacts before releasing it. On contention nothing is retired.

**R5-2 fix.**
- `runner/p5_scan_run.sh` writes `IN_FLIGHT` (job name, user, since, pid) inside the lock before sbatch.
- It removes it only when the outcome is safe:
  - the id is journaled;
  - sbatch definitely rejected the job;
  - an aborted job is proven terminal;
  - or the UNCERTAIN marker naming the job takes over.
- An invalid id answer keeps it. `nc_scan_unlock` refuses to release while IN_FLIGHT exists, so no exit or catchable signal opens the way to a duplicate scan.
- JOB.md has the recovery procedure: find the job by name in squeue/sacct, cancel it by explicit id, then remove the lock.

Stubs: `tests/stubs/sacct` gains `STUB_SACCT_DELAY`; `tests/stubs/sbatch` gained `STUB_SBATCH_DELAY` in review 4.

Test fixes, none of them changes runner code:
- The R4-1 case grepped the old lock message. It now expects "another call holds the primary scan lock".
- `tests/test_py.py` cadence: the on-time and early seeds are 420 s and 30 s. A 540 s seed once measured more than 600 s on a heavily loaded machine, because `poll.main` reconciles before it measures the gap. This is a test-timing artefact, not a code fault.

## Final evidence

Folder: `conformance/work/conf2b_runs/prodh_20261030T0450Z/`.

| Suite | Result | Log |
|---|---|---|
| Shell | **220/220** (206 + 14 R5) | `shell_tests.log` |
| Python | **51/51** | `py_tests_rerun_0720.log`; the rerun covers only the test-timing fix |
| Real CLI parser | 6/6 | |
| Syntax | 27/27 | |
| Tables | 1/1 | |

No runner, stub or shell test file changed after that shell run.
