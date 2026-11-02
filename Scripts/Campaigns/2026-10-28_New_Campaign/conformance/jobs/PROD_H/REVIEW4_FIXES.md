# PROD-H: fixes for Sol review 4 (CONF-2b manager, 2026-10-30)

Source: `conformance/review/CONF2B_REVIEW4_sol.md`, finding R4-1 (should-fix). R4-2 is a pilot finding, fixed in `code/lowp/pilot/`.

| # | Fix | Test (`tests/test_shell2.sh`, block "Sol review 4: R4-1") |
|---|---|---|
| R4-1 should-fix: overlapping scan calls could retire another call's live job record | See the three changes below. | Held lock: wrapper exit 12, no sbatch, lock left; parent exit 2, nothing retired. **Sol's overlap:** direct scan A and parent B start together with a 45 s sbatch delay → exactly ONE sbatch, A exit 0, B exit 2, A's record kept, in jobs.tsv once, nothing retired or cancelled; a later parent RESUMES A's job. `nc_retire_scan`: a wrong id → 1; no id → 1; a recorded id still LIVE → 1; recorded and proven terminal → 0, set aside |

**The three changes for R4-1:**
1. **One submitter.** `runner/p5_scan_run.sh`: the "no job record" check, the sbatch and the job-record write run under an atomic lock directory per run and phase (`p5_scan_<phase>.submit.lock`, mkdir, owner.txt). The lock is released before the long wait and by an EXIT trap. A concurrent caller exits **12** and submits or retires nothing. The record is re-checked under the lock: a call that recorded its job meanwhile is resumed, never duplicated. Exits 4 and 5 write `p5_scan_<phase>.outcome`, naming the job judged.
2. **Exact-id retirement.** `runner/common.sh` `nc_retire_scan RUN_DIR PHASE TAG EXPECTED_ID` retires nothing unless the current record names exactly EXPECTED_ID AND squeue AND sacct prove that id terminal.
3. **Parent.** `runner/p5_submit.sh` retires on exit 4 only by the outcome id; exit 5 never retires (the aborted job was the caller's own and was never recorded); exit 12 is refused. The refusal and dry-run retirements pass the verified scan id.

`tests/stubs/sbatch` gains `STUB_SBATCH_DELAY` (the scheduler answers late, which opens the overlap window).

**OPS note:** a stale `p5_scan_<phase>.submit.lock` can only come from a killed submitter. Exit 12 says so. Inspect `owner.txt`, check that no call is running, then remove the folder by hand.

## Final suite

Folder: `conformance/work/conf2b_runs/prodh_20261030T0216Z/`, rc 0, finished 2026-10-30T03:07:07Z.

| Suite | Result |
|---|---|
| Python | 51/51 |
| Shell | **206/206** (197 + 9 R4-1) |
| CLI parser | 6/6 |
| Syntax | 27/27 |
| Tables | 1/1 |
| **Overall exit** | **0** |
