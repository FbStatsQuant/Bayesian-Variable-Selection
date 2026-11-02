# PROD-H: fix for Sol review 6 (CONF-2b manager, 2026-10-30)

Source: `conformance/review/CONF2B_REVIEW6_sol.md`. R5-1 is RESOLVED. R5-2 was PARTIAL because of the new should-fix (high) R6-1.

| # | Fix | Test (`tests/test_shell2.sh`, block "Sol review 6") |
|---|---|---|
| R6-1: a nonzero sbatch status is not proof of non-acceptance | See below. | Client status 143 and 137 after the scheduler ACCEPTED the job (stub `STUB_SBATCH_ACCEPT_THEN_DIE`): the wrapper exits 13, the lock and IN_FLIGHT (with `client_status`) are kept, and there is no job record; the next scan call exits 12, submits nothing, and exactly ONE acceptance exists. sbatch exit 42: exit 13, with the status and stderr recorded. Parent: exit 2 naming "wrapper exit 13", nothing retired, no P5 array. The old boundary case, which asserted that a rejection releases the lock, is replaced |

**The fix:**
- `runner/p5_scan_run.sh`: on ANY nonzero sbatch status, IN_FLIGHT is no longer removed. The client status and stderr are appended to it, the lock is kept (fail closed) and the wrapper exits **13**, "acceptance UNKNOWN". The message points to the manual resolution.
- `runner/p5_submit.sh` refuses on 13 with that message.
- `JOB.md`, step 0 of the stale-lock procedure: resolve as in step 1. An empty squeue/sacct answer right after the failure is not yet proof; check again after a minute.

Consequence (deliberate): a plain scheduler rejection now also needs a manual unlock, because the status alone cannot distinguish it from an accepted job whose client died.

## Final evidence

Folder: `conformance/work/conf2b_runs/prodh_20261030T0940Z/`, rc 0, finished 2026-10-30T08:10:35Z.

| Suite | Result |
|---|---|
| Python | 51/51 |
| Shell | **225/225** |
| Real CLI parser | 6/6 |
| Syntax | 27/27 |
| Tables | 1/1 |
