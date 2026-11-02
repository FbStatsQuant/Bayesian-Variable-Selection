# CONF-2b review 4 — independent Sol confirmation

Reviewer: Sol 6.1. Completed 2026-10-30 UTC. Binding context: CHARTER §§2 (including disk), 3 and 6; DECISIONS, including D11/D19/D23/D26/D27/D32. This is the requested narrow runner/GNU-time review; the frozen numerical tree was **hash-checked only**, not re-reviewed.

**PROD-H: NOT READY for HQ → OPS.** R3-1 is PARTIAL: the original sequential scheduler-outage reproduction is fixed, but an overlapping scan submission can still retire a live scan's handle and permit a replacement. R4-1 below is should-fix. R3-2 and R3-3 are RESOLVED. No blocking-severity finding.

**Pilot: READY for HQ → OPS (OPS-4 resume), for this bundle change. GNU time verdict: ACCEPT, with non-gating minor R4-2.** This clears the timing-code issue, not OPS's separate current disk-usage/preflight requirements.

Evidence root **E**: `<PC_TEMP_PATH>`. File locations below are relative to campaign **C**, unless prefixed E. Only this review and files under E were written. No SSH, NOTS access, real scheduler submission, compilation, sampler fit or numerical experiment was performed. Scheduler/fit execution in local tests was fabricated/stubbed.

## Frozen-tree check

`code/core/v2_2_1.SHA256SUMS` SHA-256 is exactly:

`d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1`

**27/27 listed file hashes verify**, with exact non-cache file membership (no missing or unlisted file). The manifest hash was checked again at completion. All **273 snapshotted reviewed/evidence files** remain unchanged. Evidence: E/hash_audit.json, E/source_snapshot.json, E/final_audit.json. No historical freeze snapshot was altered.

## Part 1 — PROD-H review-3 dispositions

| Finding | Verdict | Independent confirmation |
|---|---|---|
| R3-1: unknown scheduler state / scan resume | **PARTIAL** | Original full-parent reproduction now keeps scan 8001 after the query outage; the second call resumes 8001, returns 10 while it is live, and total sbatch count stays one. The focused cases also pass for unreadable squeue/sacct, same-ID recovery, aborted-scan UNCERTAIN markers and rerun UNCERTAIN markers. However, the terminal proof after a recording collision belongs to the losing job, not necessarily the job in the shared record: R4-1. |
| R3-2: missing direct-scan disk guard | **RESOLVED** | `runner/p5_scan_run.sh:64–65` checks uncertainty and the real charter-limit guard with a planned 5 MB before sbatch. Both direct primary and final calls refuse under a denying guard, with refusal receipts and zero submissions; obsolete limits refuse too. Allowing calls retain GUARD_CHECK_OK. A recorded-job recheck neither calls the guard nor resubmits. |
| R3-3: empty-folder manifests | **RESOLVED** | Original killed-P5 cleanup reproduction now commits a zero-byte p1000 manifest, records files=0/bytes=0, verifies HOME_MANIFEST and safely reuses all manifests. The focused cases cover added files, disappearance of all formerly listed files, restoration, and downloaded empty-folder acceptance/refusal. JOB.md H and acceptance check 8 describe the empty branch and comparison with the summary's manifest hash. |

The UNCERTAIN mechanism correctly distinguishes unreadable/unknown state from terminal state in the tested serial paths. `nc_job_state` requires absence from squeue followed by a terminal sacct state. Successful cancellation alone is not treated as sufficient. The defect below is **which job that proof applies to**.

P5-specific checks: overlapping P5 parents using an already verified scan produce **one P5 array**, because `mkdir "$RUN_DIR/p5"` is atomic; the other parent refuses, and a sequential repeat also refuses. Running its selected one-unit task twice produces **one native stub invocation and one durable start record**, a successful end record, then an explicit second-attempt refusal. No skipped eligible attempt was observed. Killed/incomplete attempts remain reportable rather than silently reattempted. These checks do not cure the separate scan-handle defect.

## Part 2 — pilot GNU time and PROD-H applicability

- **GNU identification:** `slurm/common.sh:30–49` accepts GNU 1.9's actual `time (GNU Time) 1.9` spelling, case-insensitively, and requires the executable to run an `-f`/`-o` probe. Missing paths, directories, non-GNU time and a purported GNU binary ignoring `-f` are rejected. The numeric pattern has the minor gap in R4-2.
- **Arm split:** the expected sizing units in `summarize_pilot.R:64–72,245–265` use enum20/enum30/scale/smc/bench. Enumeration, including full scaling, requires finite user+sys CPU; SMC/benchmark CPU is informational, but all sizing units need wall and usable memory evidence. Requiring GNU time for all five sizing arms is a reasonable stricter preflight and changes no acceptance threshold. `bitid` is a correctness/step-exit gate (`:387–393,406–410`), not a sizing unit: its CPU/RSS values do not enter a gate. Its wall-only fallback is appropriate. Build/lock/truthlock/verify/unlock/collect can likewise proceed, and missing GNU time cannot prevent truth restoration.
- **Absolute module path:** the fallback is explicitly pinned to `/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time`; no module load/purge is added to time resolution. Given the supplied libc-only linkage, GCCcore need not be loaded merely to execute it. A missing dependency or unusable executable makes the launch/format probe fail, so sizing arms refuse before any unit. No remote-library claim was independently tested in this no-SSH review; OPS still performs its documented precheck.
- **Task provenance and hooks:** the per-task arm/job/host/UTC, chosen path, version and SHA-256 record at `slurm/common.sh:51–59,75–79` is adequate for identifying the timer used under normal writable-log conditions. It is emitted before a missing-timer refusal too. PILOT_TIME_BIN is refused by both submission and task initialization outside local tests. Local PILOT_DRYRUN correctly allows absent time while running no units. The record writer is best-effort, consistent with the surrounding environment receipts; OPS should inspect these saved records with the downloaded logs.
- **PROD-H needs no GNU-time patch.** Inspected the complete runner directory. There is no external `time` invocation. Fit runtime is the adapter's saved runtime_s; task elapsed checks use `date`; `runner/final_accounting.sh:22` and `accounting_summary.py:57` use sacct's Elapsed/AllocCPUS/CPUTimeRAW. `--time` scheduler resource flags and `timeout` are unrelated to GNU time.

## Numbered findings

### R4-1 — should-fix — an overlapping scan-record collision retires another, live job

**Locations:** `conformance/jobs/PROD_H_DRAFT/runner/p5_scan_run.sh:55,70,75–79`; `runner/p5_submit.sh:82`; `runner/common.sh:124–126`.

There is no atomic exclusion around “no job file → sbatch → write job file”. With overlapping direct-wrapper and parent calls, both can pass the absence check and receive accepted IDs. The loser of the noclobber write cancels **its own** accepted job and returns 5 when that ID is proven terminal. The parent interprets exit 5 as permission to retire **whatever job is currently in the shared .job file**. That file belongs to the winner, which can still be live. `nc_retire_scan` does not check its ID or state.

**Reproduced on unchanged runner copies:** E/scan_concurrency_confirm.sh uses the actual wrapper and actual parent on one checksum-valid fabricated resource_limit unit. Scheduler stubs coordinate the overlap and successful explicit-ID cancellation; no scanner or fit is run. Direct scan 8101 remains live; parent scan 8102 loses the job-record race, is cancelled and proven CANCELLED; the parent nevertheless renames the record naming **8101** as `.failed_*`. Both calls finish (10,2), the current job record is absent, and squeue still shows 8101. A later actual parent call accepts 8103 (exit 10): **8101 and 8103 are live together**, sharing the phase's output/receipt paths. See E/scan_concurrency_confirm.log and E/scan_concurrency_confirm/{parent_A.log,parent_B.log,parent_C.log,stub/accepted,stub/cancelled,home/runs/scan_concurrency_confirm/p5_scan_primary.job.failed_*}. This is not evidence of duplicate native fits; it is duplicate live scan submission and loss of the promised resume handle.

**Concrete fix:** serialize each run/phase's job-file absence check, submission and accepted-ID journaling with an atomic lock, releasing it before the long wait. Make retirement take an expected ID and refuse unless the current record still names that exact ID and that ID is proven terminal. On a noclobber collision, cancel only the losing accepted job, preserve the winner's record, and resume/refuse safely. Add the overlapping direct-wrapper + parent reproduction as a regression: at most one active scan, the winner's record retained, and no subsequent replacement while it is live. Merely changing exit 5's message is insufficient.

### R4-2 — minor — GNU-time probe's “numeric” pattern accepts malformed decimals

**Location:** `code/lowp/pilot/slurm/common.sh:38`.

The first three fields use `[0-9.]+`, which accepts `.` and `1..2`. E/additional.sh supplies a fake GNU-version candidate writing `.\t1..2\t0.0\t1024`; `pilot_is_gnu_time` returns 0. This does not undermine the intended trusted GNU 1.9 binary or let such missing enumeration CPU evidence pass the downstream summarizer, so it is non-gating.

**Concrete fix:** require each elapsed/user/sys field to match a valid nonnegative decimal, e.g. `[0-9]+([.][0-9]+)?`, with exactly four tab-separated fields and integer RSS. Add malformed-decimal rejection controls. No numerical-core change is needed.

## Checks and evidence

Fresh targeted execution, all detached with saved logs and exit codes:

1. **E/original_scan_full.log / .rc:** original review-3 full-parent outage reproduction against fixed runner; retained 8001, second exit 10, one sbatch total.
2. **E/original_cleanup_manifest.log / .rc:** original review-3 cleanup/empty-folder reproduction; preflight refusal commits nothing; cleanup 0; first manifest commit 0; reuse 0; added-file refusal 2 with prior manifest preserved.
3. **E/focused.log / .rc:** supplied “Sol review 3” block preserved verbatim, with independent one-unit fixture setup to avoid the full suite: **25/25**, exit 0. Covers unknown state, same-ID resume, scan/rerun UNCERTAIN, guards/receipts, empty manifests and laptop acceptance.
4. **E/gnu_time.log / .rc:** fresh copied pilot test_gnu_time.sh **30/30**, exit 0, including all arm policies, GNU 1.9 spelling, provenance, dry-run and hook refusal.
5. **E/additional.log / .rc:** independent direct denying-guard probes: primary=1/final=1, zero sbatch; malformed-format acceptance control for R4-2; **16 shell source syntax checks, zero failures**.
6. **E/p5_concurrency.log / .rc:** overlapping P5 submission parents: one array; repeat refused. **E/p5_task_check.log / .rc:** one selected attempt executes once; second invocation refuses; one start and successful end record.
7. **E/scan_concurrency_confirm.log / .rc:** clean final R4-1 reproduction described above. Driver exit 0 means the reproduction completed, not that the production behavior passed. Earlier scratch attempts are retained: one needed the squeue stub's requested-field projection corrected; another concurrent-parent setup stopped in reconciliation before both reached submission. Neither diagnostic is the final evidence.

Inspected, **not rerun in full**: PROD-H `tests/run_all_20261030T000326.out/.rc`, `summary.log`, `shell_tests.log`: Python 51/51, shell 197/197, CLI 6/6, syntax 27/27, tables 1/1, overall 0; final summary 2026-10-30T01:05:59Z. Pilot `tests/logs_v2_2_1`: shell 54/54, GNU time 30/30, negative 89/89, all three persistent rc files 0. These saved passing suites do not cover R4-1's ownership collision.

Tool environment: Rscript 4.4.1, Python (`py -3`) 3.13.1, Git Bash 5.2.37 on Windows. Launchers, process IDs, commands, source/config snapshots, fabricated fixtures, logs and exit files remain under E; E/EVIDENCE_SHA256.json hashes the evidence files. No reviewed file was repaired in this review.
