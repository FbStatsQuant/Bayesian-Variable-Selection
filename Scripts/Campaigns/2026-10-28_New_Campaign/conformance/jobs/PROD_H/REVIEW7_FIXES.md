# PROD-H: minor fixes for Sol review 7 (CONF-2b manager, 2026-10-30; HQ D48)

Source: `conformance/review/CONF2B_REVIEW7_sol.md`. R6-1 is RESOLVED. Verdict: **READY WITH MINOR FIXES**. Under D48 the minors are fixed with tests, then the bundle is renamed `PROD_H`; there is no further review round.

| # | Fix | Test |
|---|---|---|
| R7-1 (low): a failed diagnostic append bypassed exit 13 | `runner/p5_scan_run.sh`: the `client_status`/`client_stderr` append to IN_FLIGHT is best effort (`2>/dev/null \|\| warning`). The marker and the lock stay, and the wrapper always reaches the exit-13 branch. | `tests/test_shell2.sh`, block "Sol review 7": the scheduler accepts the job, the client exits 42 AND the append fails (stub `STUB_BREAK_INFLIGHT` turns the marker path into a directory). The parent exits 2 naming "wrapper exit 13" (not a guard refusal), the warning is printed, the lock is kept; the next p5_submit is refused, exactly ONE acceptance, no P5 array |
| R7-2 (low): recovery wording | `JOB.md`, stale-lock procedure, step 2 "Unlock rule". Unlock only when (a) the wrapper and its sbatch client have finished, (b) every candidate found by name since the IN_FLIGHT time is absent from squeue and terminal in sacct (cancelled by explicit id first) and (c) the outcome is positively resolved. One minute is only a retry interval; elapsed time, failed queries or an unconfirmed no-match never authorise an unlock; escalate to HQ; keep the evidence in OPS_LOG. | documentation (the runner never unlocks on time or empty queries) |

## D48 class (ii) items

None: the review-7 verdict was READY WITH MINOR FIXES, and both minors are fixed above. The operator procedures that remain are documented in JOB.md and were reviewed in reviews 5 to 7: a lock kept after a signal or an unknown sbatch outcome (exit 12 or 13), and the stale-lock recovery.

## HQ D49 (folded into this round; no further Sol review)

The default throttles are 30 + 30 (`runner/submit.sh`): 60 one-CPU tasks = 120 billed CPUs (NOTS bills 1 CPU as 2). With PROD-L capped at 68 billed CPUs the total is 188, within the campaign ceiling of 192 (D47).

JOB.md documents:
- the billing;
- the 192 ceiling;
- `scontrol update JobId=<array id> ArrayTaskThrottle=<N>` to raise PROD-H's throttles after PROD-L, keeping the total at most 192 billed;
- that the ≤ 100-TASK submit guard counts PROD-L's tasks too.

Tests:
- the vectors expect `%30`;
- two refusal fixtures whose overflow depended on the old default were raised (30 → 41 running tasks, `%1` → `%41`);
- new: PROD-L at `%34` + 60 passes; PROD-L at `%50` + 60 is refused.

Note for HQ: the task guard admits up to 100 tasks (200 billed). The 192-billed ceiling is enforced by the defaults and by the documented OPS check, not by code.

## Final suite

Folder: `conformance/work/conf2b_runs/prodh_20261030T1430Z/`, rc 0, finished 2026-10-30T09:29:04Z.

| Suite | Result |
|---|---|
| Python | 51/51 |
| Shell | **229/229** |
| Real CLI parser | 6/6 |
| Syntax | 27/27 |
| Tables | 1/1 |

(A run started at 13:10Z, before D49, was stopped and discarded.)
