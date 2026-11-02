# CONF-2b review 7 — narrow R6-1 re-check of PROD-H

Reviewer: Sol 6.1, independent reviewer for Felipe. 2026-10-30 UTC.

**R6-1: RESOLVED. PROD-H: READY WITH MINOR FIXES.**

The original duplicate-acceptance defect is closed. Actual TERM and KILL signals to an accepted-before-reply sbatch client now retain exclusion, and subsequent calls submit no replacement. Two low-severity items remain: a diagnostic-write error can bypass exit 13 and produce a misleading parent message, and the manual recovery wording needs an explicit rule for unresolved empty queries. Correct these before OPS uses the recovery procedure. No high- or medium-severity finding arose in this narrow re-check.

Campaign **C** is `<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign`. Evidence **E** is `<PC_TEMP_PATH>`. Source locations below are relative to `C/conformance/jobs/PROD_H_DRAFT/`.

Only this review and new files under E were written by this reviewer. Checks used copied production runners, fabricated scheduler commands and checksum-valid fixtures. No SSH, NOTS access, real submission, compilation, sampler execution, simulation or numerical experiment occurred. This review does not reopen the wider production audit.

## Findings

### R7-1 — low: diagnostic append failure bypasses the new exit-13 handling

**Locations:** `runner/p5_scan_run.sh:93–94`; resulting parent classification at `runner/p5_submit.sh:81`.

The append of `client_status` and `client_stderr` is subject to `set -e`. If it fails, the wrapper exits 1 before reaching `NC_RC=13 nc_fail`. Exclusion remains closed, but the parent then says **“the OPS guard refused the scan job ... nothing was submitted”**, even when the scheduler accepted a job.

**Targeted reproduction:** after accepting 8101, the scratch sbatch stub saves the initial marker, replaces its path with a directory to induce an append I/O failure, and exits 42. The actual parent exits **1**, prints the incorrect guard/no-submission message, and keeps the lock. Its next invocation exits **2**; acceptance count remains **1**, with no P5 array. Evidence: `E/extra.sh`, `E/extra.log`, `E/diagnostic_append_failure/{A.log,B.log,stub/inflight.saved,stub/accepted}`. This is an injected storage-error check, not a claim that the normal TERM/KILL cases fail.

**Concrete fix:** make this diagnostic append best effort, preserving the existing marker and continuing to the explicit UNKNOWN/exit-13 branch even if the append fails. For example, guard the append with `|| true` and give a best-effort warning. Add an append-failure regression asserting wrapper 13, parent 2 naming UNKNOWN, retained exclusion and no replacement.

### R7-2 — low: clarify the recovery rule when no matching job is found

**Location:** `JOB.md:102–104`, especially “check again after a minute before removing the lock.”

The identified-job route is adequate: locate by saved name/time, cancel by explicit ID, obtain terminal accounting, then remove the lock and log recovery. The added minute is a useful retry interval, but the text can be read as allowing removal after a second empty query. The bundle provides no guarantee that visibility is complete after 60 seconds. It also does not explicitly require resolution of any surviving submitting client before removal.

**Concrete fix:** say that one minute is only a retry interval. Require the submitting wrapper/client to have finished; require every identified candidate to be absent from squeue and terminal in sacct. Failed queries or unresolved no-match results must leave the lock in place and be escalated for positive resolution of the submission outcome; elapsed time alone is not authorization to unlock. Preserve the query outputs and resolution in OPS_LOG.

This is a manual-procedure clarification. The runner itself does not unlock after a timeout or empty query.

## R6-1 reproduction and caller assessment

Reran the review-6 `sbatch_child_signal.sh` reproduction against current, unchanged runner copies, retaining its durable acceptance barrier and actual OS signals:

| Client signal | First wrapper | Next wrapper | Exclusion after both calls | Accepted live jobs |
|---|---:|---:|---|---:|
| TERM | 13 | 12 | lock + IN_FLIGHT retained; client_status 143 | 1 |
| KILL | 13 | 12 | lock + IN_FLIGHT retained; client_status 137 | 1 |

Neither case has a scan job record. There is no replacement. Subsequent actual parents return 2 and retirement helpers return 1 without removing exclusion. Evidence: `E/sbatch_child_signal_rerun.{sh,log,rc}` and `E/sbatch_signal_rerun_{TERM,KILL}/`.

A fresh plain-exit-42 fixture returns wrapper **13**, next wrapper **12**, actual parent **2**, retirement **1**. Status and stderr are retained. It makes exactly **one sbatch attempt**, with **zero acceptances**, and makes no replacement attempt. Evidence: `E/plain_confirm.{sh,log,rc}`, `E/plain_nonzero42_confirm/`.

Additional accepted-before-reply TERM/KILL cases launched through the actual **non-dry-run parent** both return 2 naming “wrapper exit 13”; later parents remain blocked, exactly one acceptance exists, and no P5 directory/array or retirement is created. Direct **final --no-wait** cases return 13, then 12, with exactly one acceptance. Evidence: `E/actual_parent_client_{TERM,KILL}/`, `E/final_client_{TERM,KILL}/`, `E/extra.log`.

The only production program that executes this wrapper is `p5_submit.sh:74`. Its case at `:88` refuses before `SCAN_MADE=1` at `:91`, so `refuse()` at `:37` cannot retire anything on exit 13. The default nonzero branch also refuses. The primary/final commands in JOB.md are direct operator calls; `submit.sh:62` and `stage_local.sh:26` copy the file, and `p5_submit.sh:160` prints the final command. Test callers capture statuses. No other production caller was found that treats 13 as success or triggers replacement. The normal handling is safe and clear; R7-1 covers the exceptional diagnostic-write path.

## Exit-path audit: IN_FLIGHT creation through removal

| Path / location | Result |
|---|---|
| Initial marker write fails, `p5_scan_run.sh:88` | sbatch has not run; this invocation cannot have accepted a job. |
| Wrapper exit/signal while sbatch is outstanding, `:89` | Marker remains; EXIT cannot unlock. TERM/HUP/INT/KILL controls retain exclusion. |
| Nonzero sbatch, `:90–95` | No removal; normal outcome 13. Diagnostic append failure also retains exclusion, with the reporting defect R7-1. |
| Zero status, unusable ID, `:96–97` | Exit 2; marker and lock retained. |
| Append of known ID fails, `:98` | Existing marker remains; error exit cannot unlock. Code inspection. |
| Record/journal failure; abort proven terminal, `:100–104` | Explicit-ID cancellation plus terminal proof precede removal; exit 5. Record- and journal-failure controls pass. |
| Abort unresolved, `:105–107` | Removal is conditional on a nonempty uncertainty marker naming the accepted job. That marker gates future submissions. If no nonempty replacement marker was created, IN_FLIGHT remains. Failed uncertainty-marker creation assessed by inspection. |
| Both journals succeed, `:109–110` | ID is recorded before removal/release; subsequent checking resumes that ID. |
| Marker removal fails, `:104,106,109` | An existing marker prevents EXIT unlock. Code inspection. |
| Interruption after marker removal | The recorded ID, proven-terminal abort, or uncertainty marker already resolves/gates the acceptance; a stale lock adds exclusion. |
| EXIT release, `:49–50`, `common.sh:156–164` | Presence of IN_FLIGHT makes unlock refuse. No nonzero-sbatch path removes it. |

After release, exits 0/10/11/4 operate on the recorded ID. Terminal retirement still takes the shared lock and checks the expected current ID and terminal proof. An outcome-file write failure cannot authorize retirement without a valid expected ID.

## R4-1 / R5-1 / R5-2 regression assessment

**No regression found; R5-2's R6-1 remainder is now resolved within this scope.**

The review-6 comparison shows only the new nonzero branch/exit documentation in `p5_scan_run.sh` and the parent case in `p5_submit.sh`; `common.sh` is byte-for-byte unchanged. Independent controls pass for submission overlap, under-lock record recheck, wrong/missing/live retirement IDs, the direct-helper retirement barrier, and the full-parent retirement barrier. Both barriers preserve the later 8101 record and allow only one subsequent acceptance.

All four original accepted-before-ID **wrapper** signals preserve their exact exits: TERM 143, HUP 129, INT 130, KILL 137. Each keeps IN_FLIGHT; later wrapper/retirement/parent return 12/1/2 with one live acceptance. Pre-sbatch TERM releases the lock with zero acceptances; post-journaling TERM preserves the recorded live ID. Dry-run retirement with one and zero eligible units, post-verification refusal, and journal-failure terminal/uncertain handoffs also pass.

## Checks, limitations and saved evidence

All substantial shell checks ran detached with launch commands, Windows process IDs, UTC start/end files, logs and exit files in E. Launch records: `launch.json` (46196), `extra_launch.json` (19332), `targeted_launch.json` (37276), `plain_launch.json` (27588).

- `sbatch_child_signal_rerun`: **2/2 pass**, rc **0**.
- `targeted_rerun`: **34/34 pass**, rc **0**; prior controls adapted only for exit-13 rejection/retained-lock expectations and fresh fixture names.
- `signal_boundaries`: **2/2 pass**, rc **0**.
- `additional_clean`: **7/7 pass**, rc **0**.
- `extra`: **10 pass, 1 harness assertion fail**, rc **1**. The failed plain-42 assertion required no trailing space in normalized stderr; production preserves a trailing space from newline flattening. Fresh `plain_confirm`: **1/1 pass**, rc **0**, with whitespace-tolerant stderr checking and explicit 13/12/2/1 statuses. The other ten assertions include parent/final signal cases and the R7-1 reproduction.
- Initial `sbatch_child_signal` and `targeted` attempts timed out at the barrier, rc **91**, after an omitted fabricated cache READY fixture caused pre-sbatch refusal. They accepted nothing. The prior fabricated READY file was restored only under E; the successful fresh reruns above supersede these setup failures. Original logs/exit files and the resulting initial group rc 1 are retained.
- The retirement-barrier log's early missing-`accepted` diagnostic occurs before any acceptance; the final asserted count/queue are saved and pass.
- `syntax.log`: **19/19** currently present runner/staging/test shell and sbatch files pass `bash -n`; no suite files were generated in the reviewed tree.
- Inspected, **not rerun**, the supplied `C/conformance/work/conf2b_runs/prodh_20261030T0940Z/`: `run_all.rc` **0**, summary Python **51/51**, shell **225/225**, CLI **6/6**, syntax **27/27**, tables **1/1**. Shell log rows 223–229 include the R6-1 block. These supplied status simulations are supplemented here by actual TERM/KILL client signals.

Tool versions and environment are saved in `tool_versions.txt` and `environment.json`. Fixtures use deterministic IDs/states; numerical seeds are not applicable. E preserves source/configuration copies, fabricated queue/accounting state, logs, statuses, reproduction scripts and SHA-256 evidence.

## Frozen tree and write audit

The actual `C/code/core/v2_2_1.SHA256SUMS` has SHA-256:

`d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1`

**27/27 listed files verify**, and the actual production frozen-tree verifier passes its membership/special-entry checks. Evidence: `E/frozen.{log,rc}`, `E/source_audit.json`.

All **293** snapshotted files in the reviewed scope (bundle, frozen tree/manifest, supplied suite and prior reviews) are unchanged. The sole addition there is this requested review. Evidence: `E/source_snapshot.json`, `E/scoped_audit.json`, `E/runner_copy_audit.json`, `E/EVIDENCE_SHA256.json`. The broader snapshot also records changes in unrelated active `code/bench_v2/repro/` outputs; no campaign-wide quiescence is claimed. The frozen numerical code was hash-checked and was not executed or re-reviewed.
