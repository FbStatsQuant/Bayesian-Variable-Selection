# CONF-2b review 5 — narrow independent R4-1 re-check

Reviewer: Sol 6.1, for Felipe. Completed 2026-10-30 UTC.

**R4-1: PARTIAL. PROD-H: NOT READY for HQ → OPS.** The original direct-wrapper/parent overlap is fixed, but concurrent retirement can still remove another call's live scan record and permit a second live scan. The new EXIT cleanup also permits replacement after an interrupted, accepted-but-not-yet-journaled submission. Both are should-fix findings within the requested lock/retirement re-check; no blocking-severity finding is assigned.

Campaign **C** is `<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign`. Evidence **E** is `<PC_TEMP_PATH>`. Locations below are relative to `C/conformance/jobs/PROD_H_DRAFT/` unless specified otherwise.

Only this review and new scratch files under E were written. All execution used copied, unchanged runners with fabricated scheduler commands and a checksum-valid, one-unit fixture. No SSH, NOTS access, real submission, compilation, sampler fit, or numerical experiment was performed. This review does not reopen pilot/GNU-time or other historical findings.

## What passes

- **Original overlap, equivalent reproduction:** pause the scheduler stub after accepting scan 8101 but before returning its ID. An overlapping actual `p5_submit.sh` refuses with 2, and a second direct wrapper exits 12. There is exactly one accepted job; the contenders leave the owner's lock intact. Release the scheduler reply: the winner returns 10, records 8101 once, and releases its lock. A later actual parent returns 10, resumes 8101, and submits nothing. The live queue contains only 8101; nothing is cancelled or retired. Evidence: `E/overlap/`, `E/probes.log`.
- **Absence-check/submission TOCTOU:** suspend caller A immediately before its lock mkdir, let B submit and record live 8101, then let A acquire the lock. A's under-lock re-check resumes 8101. Both return 10; one acceptance; record preserved; no leaked lock. Evidence: `E/recheck/`.
- **Exact-ID controls:** a wrong ID, missing ID, and the correct-but-live ID each make `nc_retire_scan` return 1 without moving the record. The terminal retirement control succeeds. These controls do not make the check-and-move atomic.
- **Exit handling:** exercised owned-lock cleanup for ordinary `nc_fail` refusals, rejected sbatch, invalid sbatch response, guard failure, unresolved uncertainty, recording failure with successful cancellation (5), recording failure with cancellation failure (11), verified completion (0), terminal failure (4), scheduler query failure (11), and live wait (10). Additional controls cover a bad frozen manifest, absent results, malformed existing record, and a jobs.tsv append failure after acceptance. Exit 12 leaves the other caller's lock in place. The parent handles 12 explicitly, before `SCAN_MADE=1`, and neither retires nor resubmits. Exit 5 likewise does not call retirement.

## Findings

### R5-1 — should-fix — retirement still has an unprotected check-to-move race

**Locations:** `runner/common.sh:126` (especially lines 129–134); reachable through `runner/p5_submit.sh:84`, with the same helper also called at lines 37, 112 and 135.

`nc_retire_scan` reads the expected ID, queries the scheduler, then moves the shared paths without holding the submission lock or re-establishing ownership atomically. Another caller can retire that same terminal record and a new wrapper can submit and record a live replacement while the first retirement's scheduler query is outstanding. The delayed retirement then moves the replacement's record using terminal proof for the old ID.

**Reproduced with actual parents, no runner edits:**

1. Parents A and B both inspect recorded failed job 8000. A reaches `nc_retire_scan`, passes its ID check, and pauses in its terminal-accounting query.
2. B's actual parent retires 8000 and exits 2. Direct wrapper C submits live 8101, records it, and exits 10.
3. Resume A's query, which correctly reports **8000 FAILED**. A returns 2 after moving the shared record now naming **8101** into `.failed_*`. There is no current job record, but 8101 remains live.
4. Actual parent D accepts 8102 and returns 10. The stub queue now contains **8101 and 8102**, both live.

Evidence: `E/followups.log`, `E/parent_retire_race/{parent_A.log,parent_B.log,scan_C.log,parent_D.log,live_before_replacement.txt,live_after_replacement.txt}`, its `stub/accepted`, `jobs.tsv`, and archived job records. A separate direct-helper reproduction reaches the same result in `E/retire_race/`. The old scheduler proof is valid; its association with the shared record is stale.

**Concrete fix:** make retirement acquire the **same per-run/per-phase lock** as submission, then read/re-check the expected ID, prove that ID terminal, and move all associated artifacts before releasing the lock. All retirement callers must use that protocol and refuse safely on contention. A re-read alone still leaves a race between that read and `mv`. Add the two-parent, delayed-accounting-query interleaving above as a regression, asserting that the new live record survives and no replacement is accepted.

### R5-2 — should-fix — catchable signals release exclusion during an uncertain submission

**Locations:** `runner/p5_scan_run.sh:44`–46 and `:83`–90; recovery guidance at `JOB.md:101` and `p5_scan_run.sh:64`.

The EXIT trap always removes an owned submission lock. If the scheduler has accepted a job but `JOB=$(sbatch ...)` has not returned its ID, TERM, HUP, or INT exits the wrapper before the job record or uncertainty marker is written. The EXIT trap then removes the only exclusion protecting that unresolved acceptance.

**Reproduced independently for each signal:** the stub durably accepts live 8101 and withholds its reply. Signal the wrapper PID from `owner.txt`, then release the reply. TERM/HUP/INT produce exits **143/129/130**, respectively; each leaves **no lock, no job record, and no uncertain marker**. The next actual scan wrapper accepts 8102 and exits 10; both 8101 and 8102 are live. With SIGKILL, exit 137 leaves the lock; the next wrapper exits 12 and only 8101 is accepted. Thus the stale-lock behavior is fail-closed for KILL, but catchable-signal cleanup is not.

Evidence: `E/followups.log`, `E/signal_{TERM,HUP,INT,KILL}/`, including individual wrapper logs, accepted IDs, and saved live queues. Signals were sent only to local fabricated-test wrapper PIDs.

**Concrete fix:** persist a submission-in-progress state before invoking sbatch. Distinguish safe cleanup (no acceptance possible, or an accepted ID safely journaled/proven terminal) from unresolved acceptance. Signal/EXIT handling during the latter interval must retain a durable fail-closed lock/marker until the accepted job is identified and journaled or cancelled and proven terminal. Preserve the signal exit status. Update stale-lock instructions to require resolving potentially accepted live scan jobs as well as checking that the submitting process is gone; process death alone is insufficient. Add the accepted-before-ID signal controls above.

## Checks and saved results

All substantial checks ran detached, with saved launcher commands, PIDs, UTC launch times, logs and exit files:

- `E/probes.sh` / `probes.log` / `probes.rc`: **19 passing assertions, 2 failing safety assertions**, exit 1. The two failures independently reproduce R5-1; they are production-safety failures, not a failed harness setup.
- `E/followups.sh` / `followups.log` / `followups.rc`: **1 passing assertion, 4 failing safety assertions**, exit 1. Full-parent R5-1 plus TERM/HUP/INT R5-2 fail; KILL fails closed.
- `E/boundaries.log`: four additional refusal/abort controls pass. Its first pre-submission signal fixture was rejected by the guard's static-format check before reaching its barrier; driver exit 91. This diagnostic is retained and is not counted as evidence about signal behavior.
- `E/signal_boundaries.sh` / `signal_boundaries.log` / `signal_boundaries.rc`: corrected boundary fixtures, **2/2 pass**, exit 0. TERM before sbatch releases the lock with zero accepted jobs; TERM after journaling preserves live 8101's record with the submission lock already released. These controls isolate R5-2 to the unresolved-acceptance interval.
- `E/syntax.json`: **15/15 runner shell/sbatch source syntax checks pass**.
- Inspected, **not rerun in full**: `C/conformance/work/conf2b_runs/prodh_20261030T0216Z/run_all.rc` = 0 and `summary.log`: Python 51/51, shell 206/206, CLI 6/6, syntax 27/27, tables 1/1, finished 2026-10-30T03:07:07Z. Inspected the R4-1 test block and saved rows 199–208. Those cases cover submission overlap and serial ID checks, not the delayed-retirement interleaving or acceptance-window signals.
- `E/runner_since_review4.diff`: all runner differences from the preserved review-4 snapshot inspected. Only `common.sh`, `p5_scan_run.sh`, and `p5_submit.sh` differ.

Tool versions: Git Bash 5.2.37, Python 3.13.1 through `py -3`, Rscript 4.4.1 (version inspection only). Fixtures have no random seed or numerical results. Source/configuration snapshots, exact launchers, fabricated scheduler state, process/exit evidence, and evidence SHA-256 hashes are retained under E.

## Frozen tree and write audit

`C/code/core/v2_2_1.SHA256SUMS` SHA-256 is exactly:

`d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1`

**27/27 listed files verify**, with no missing or unlisted non-cache files. **245 snapshotted reviewed/evidence files remain unchanged.** Evidence: `E/hash_audit.json`, `E/source_snapshot.json`, `E/final_audit.json`, `E/EVIDENCE_SHA256.json`. The frozen numerical code was hash-checked only, not re-reviewed or executed.
