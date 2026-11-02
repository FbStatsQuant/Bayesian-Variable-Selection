# CONF-2b review 2 — independent Sol review

Reviewer: Sol 6.1, 2026-10-29. Scope: review-1 fixes and PROD-H, against CHARTER sections 2/3/6, D10/D11/D19/D20/D21 and GO_2400 C1–C5. No SSH, NOTS contact, submission, compilation, new sampler fits or subagents. All executions were local review checks explicitly authorized by this brief, using R 4.4.1, Git Bash and Python via py -3. Reviewed files were not changed.

Scratch evidence **E**: `<PC_TEMP_PATH>`. Paths below are relative to **C**, the New Campaign directory.

## Verdicts

**Part A — v2.2.1: ACCEPT WITH FIXES; not ready to freeze.** The concurrency repair works, the numerical core remains byte-identical to v2.2, and the normal scanner/resume behavior is supported. F5 still admits invalid types under the different-checkpoint exception. The new scanner fallback also labels a record launchable which the retry adapter refuses.

| Review-1 finding | Verdict | Re-check |
|---|---|---|
| F1: commit between check and lock | RESOLVED | Rechecks are under the acquired lock. Lane G 23/23 and my original valid-competing-commit reproduction pass: skipped TRUE, no second fit/write. Identity mismatch and changed/invalid primary paths refuse. |
| F2: named NULL H extras | RESOLVED | H checks are unconditional; L remains optional. Lane G 24/24 and the original H NULL controls pass. |
| F3: wrong-primary retry / CSV–RDS consistency | PARTIAL | Wrong seed, primary binding, allocation and status controls pass in both directions (26/26 combined F3/F7 checks). The new missing-native fallback disagrees with adapter eligibility; finding R2-3. |
| F4: resumed stop phase | RESOLVED | Lane G 22/22; the original saved-unit resume now returns its stop. Primary/retry, preflight/runtime-guard and repeat resumes are covered. |
| F5: forced-stop classifier | PARTIAL | Same-checkpoint timing type/shape/finiteness checks and native outcome checks are improved; all 15 supplied controls pass. Different-checkpoint pairs still accept corrupt timing/dimension types; R2-2. |
| F6: unlisted symlinks | RESOLVED | Both real-tree checks accept; both refuse my original native unlisted-file symlink. Pilot shell suite 54/54 includes file/directory/replacement/root/cache-link controls. |
| F7: partial retry artifacts / launchability | RESOLVED | CSV-only is incomplete, lock-only is locked, neither launchable; foreign retry is invalid_inspect. Original reproduction and lane G agree. |

**Part B — PROD-H: NOT READY for HQ → OPS.** R2-1 is blocking. Resolve the should-fix items below and re-review the changed paths before staging/submission. Passing stub suites do not cover these failure cases.

## Findings

### R2-1 — blocking — a failed C3 hold is recorded as an established hold and never retried

**Location:** `conformance/jobs/PROD_H_DRAFT/runner/poll.py:104–107`, `:127–130`, `:96–101`.

Every nonzero scontrol result is merely appended to the receipt. HOLD.json is still written, and the next invocation takes STILL_HELD without trying again. The request even says pending tasks “were held.” A transient controller error can therefore leave pending tasks launching after the mandatory stop trigger.

**Evidence:** E/python_probes.log: first decision HOLD, both hold return codes 1; second decision STILL_HELD, zero new hold calls.

**Fix:** track hold success per job, confirm the pending tasks' held state, and persist a distinct hold-requested/hold-failed state until established. Retry failed holds on subsequent polls; return nonzero and explicitly request urgent OPS/HQ action on failure. Treat terminal/no-pending jobs separately. Do not cancel running tasks. Add failed/partially successful hold tests.

### R2-2 — should-fix — F5's whole top-level layout rule is insufficient to validate output structure

**Location:** `conformance/work/v2_2_1_regression/scripts/a2_compare.R:44–64`, especially `:57–59`.

Allowing each top-level name vector to match an actual v2.2 layout is reasonable for progress-dependent partial fields and ordering. It does not validate nested structure, field types, or invariant metadata. The different-checkpoint branch never applies timing_valid. In each of the 0.0002/0.0003/0.0006 pairs, changing the v2.2.1 stop elapsed_seconds to a string still yields PASS. Replacing its existing p with “not-a-dimension” also yields PASS. cmp2 detects the type difference; the classifier discards it.

**Evidence:** E/a2_probes.log. The four unmodified saved pairs reproduce their classifications; all 15 existing controls also pass independently in E/a2_results/. These controls miss the remaining hole.

**Fix:** validate each fit's schema independently before applying D10: finite scalar stop timings, required field types/shapes and invariant case/allocation metadata, with explicit accommodation for variable partial-result lengths. Apply these checks to the different-checkpoint branch too. Add both corruptions above as negative controls. Keep the differing-progress cases explicitly timing-excluded/non-identity evidence; do not imply numerical identity.

### R2-3 — should-fix — the new native-status fallback can consume a P5 attempt on an ineligible record

**Location:** `code/core/v2_2_1/tools/p5_scan.R:34–39`, `:97–98`; `study/adapter.R:380–381`.

The scanner falls back from missing record$native_status to fit$status. The adapter requires record$native_status itself to equal resource_limit. On a scratch copy of a valid primary with only native_status removed and its sidecar regenerated, the scanner reports eligible=TRUE and launchable=TRUE; smcbvs_p5_primary refuses it. PROD-H would record its one durable attempt before discovering this disagreement.

**Evidence:** E/adapter_extra.log and E/fallback.tsv.

**Fix:** for these study records, fail closed with an inspect/refusal state when native_status is absent, or deliberately share one canonical status helper between scanner and retry validation if legacy compatibility is required. Continue treating a present native_status as authoritative: adapter_error can intentionally differ from raw fit$status. Test the missing-native case and the legitimate adapter-error case.

### R2-4 — should-fix — full xz deserialization is now an unbudgeted login-node workload

**Location:** `code/core/v2_2_1/tools/p5_scan.R:31–36`; `conformance/jobs/PROD_H_DRAFT/runner/p5_scan_run.sh:2–5,22`; `JOB.md:145`.

The scanner now hashes AND decompresses/deserializes every primary RDS, including the roughly 2,394 ordinary completions. Nice 19 changes priority; it does not make this a cheap metadata scan. The stated “few minutes” rationale considers hashing, not this new work. My read-only sample of the saved 994,176-byte H record took about 0.98 s for five reads, an illustrative 470 s for 2,400 such reads before hashing or CLI startup. This is a laptop sample, not a NOTS timing estimate; production files and NOTS could differ substantially. Memory is bounded by current records, not all 2,400 records retained together.

**Fix:** retain both-direction consistency validation, but run the full scan as a persistent, guarded single-CPU compute job with explicit memory/time, scratch logs, job ID and completion receipt; wait for its verified table before P5 selection. Alternatively build a separately reviewed, immutable compact status receipt while writing each record. Do not restore the one-sided check to save time.

### R2-5 — should-fix — a killed P5 attempt leaves locks/temp files with no terminal cleanup path

**Location:** `conformance/jobs/PROD_H_DRAFT/runner/p5_task.sh:40–51`; `runner/reconcile.py:262–270`; `runner/make_manifests.sh:23–24`.

Unlike task.sh, p5_task.sh has no post-child lock cleanup. Reconcile's stale-lock code handles only the primary SMCBVS.lock, not P5_retry locks or atomic-write remnants. A hard-killed P5 unit can be correctly REPORTED by the final scan yet permanently refuse the documented manifest/transfer workflow.

**Evidence:** E/failure_paths_corrected.log: a stub step creates a P5 lock then exits 137; the actual p5_task.sh returns 0 with the lock still present, and the manifest command refuses it.

**Fix:** add terminal P5 cleanup after checking all recorded P5 jobs are dead. Archive owner/temp evidence, remove only proven-stale artifacts for selected units, preserve durable attempt records, and never relaunch the fit. Test SIGKILL/incomplete-write cleanup through final scan and manifest creation. A single cleanup path can also cover primary atomic-write remnants.

### R2-6 — should-fix — manifest creation cannot recover from a partial pass

**Location:** `conformance/jobs/PROD_H_DRAFT/runner/make_manifests.sh:19–30`.

The script writes p0500's manifest before preflighting p1000/logs. If a later folder has a stale artifact, it exits after committing the earlier manifest. After resolving the artifact, rerunning immediately refuses the already-created p0500 manifest; summary.tsv has also been truncated at startup.

**Evidence:** E/failure_paths_corrected.log: first call commits p0500 then refuses p1000's P5 lock; after scratch lock removal, second call refuses p0500/MANIFEST.sha256.

**Fix:** preflight all three folders first and build/verify all temporary manifests before committing, and/or support safe resumption by revalidating existing manifests and rebuilding the full summary. Never silently replace an inconsistent manifest. Add a later-folder failure/recovery test.

### R2-7 — should-fix — post-submission journal failures bypass the promised abort handler

**Location:** `conformance/jobs/PROD_H_DRAFT/runner/submit.sh:171–172`; `runner/rerun.sh:59–65`.

After successful sbatch, a failed jobs.tsv append under set -e exits submit.sh directly, without abort_submission and without cancelling the accepted job. The rerun driver similarly leaves an accepted job untracked if its ledger write fails. Subsequent live-job checks and accounting rely on that ledger.

**Evidence:** E/submission_record_probe.sh executes the actual submit() definition with stub sbatch returning 9001 and an unwritable journal target. Exit is 1; the abort stub is never called. No scheduler was contacted.

**Fix:** explicitly guard every journal/config/receipt write after a job is accepted. On failure, invoke the abort/cancel path by the known explicit ID and record cancellation failure visibly. Apply this transaction handling to rerun.sh too. Test a journal failure after successful sbatch, not only scheduler rejection.

### R2-8 — should-fix — the throttle gate is conditional on an unenforced job-name convention

**Location:** `conformance/jobs/PROD_H_DRAFT/runner/common.sh:64–89`, especially `:74`; `JOB.md:143`.

The current two arrays sum to 100 and all names in this bundle match. However, an fb31 campaign array without “smc” is explicitly ignored; a current test asserts that ignoring behavior. Thus this is not an unconditional combined campaign cap.

**Fix:** fail closed by counting all fb31 arrays, or identify campaign arrays by a durable registry/path and query their actual throttle/running counts. A naming convention alone is sufficient only if every campaign submission enforces it and unknown arrays are inspected/refused. Test a relevant array with a nonmatching/truncated name. Preserve the two-array 50+50 default.

### R2-9 — should-fix — several execution logs are still written to home

**Location:** `conformance/jobs/PROD_H_DRAFT/runner/poll.py:125–126`; `runner/p5_scan_run.sh:22`; `runner/submit.sh:41,167`; `runner/p5_submit.sh:27,104`.

polls.jsonl, scan logs, refusal logs and scheduler stderr go under the home run directory. CHARTER section 2 rule 2 explicitly sends everything else, including logs, to scratch. Being small does not satisfy that location rule. The three folder manifests cover results/logs on scratch, but not newly produced home run summaries before any eventual home pruning.

**Fix:** place append-only execution logs under LOGROOT, keeping only small immutable receipts, state and summaries in home. Update documented paths and tests. Add a manifest for the downloaded run-summary folder, or explicitly require a separately generated/locally verified manifest before pruning it.

### R2-10 — should-fix — C3 cadence is weakened to “about” ten minutes and only warns after eleven

**Location:** `conformance/jobs/PROD_H_DRAFT/runner/poll.py:32,117`; `JOB.md:61,131,142`.

“At most 10 minutes apart” is a maximum 600-second gap, not permission to wait at least ten minutes. The current threshold silently accepts gaps between 600 and 660 seconds, and acceptance checks only “about” ten minutes during the first 200 units.

**Fix:** specify an OPS cadence within 5–10 minutes, set lateness at >600 s, and record/check actual gaps throughout active production. A scheduler is not needed in this bundle, but the handoff must name the monitoring responsibility and retain receipts. Test a 601-second gap. Preserve the one-connection rule.

## PROD-H contract checks and recommendations

The allocation/vectors are correct as written: p500 L=6,300 s, hours=1.75; p1000 L=24,000 s, hours=6.666666667; native memory 2 GB, Slurm 2G; walls 03:52:00 and 13:42:00. There are 1,200 datasets/2,400 units, one task per dataset, c100 then c050, two arrays. Primary, infrastructure rerun and P5 commands use Sapphire Rapids and no-requeue. Reruns select infra/orphan, preserve native allocation and derived seed, and leave timeout/resource_limit/infra_repeat alone. Native resource limits and scheduler timeouts remain separate categories.

P5 correctly waits for reconciliation, compares scanner resource-limit selection with reconciliation, rejects non-none retry states (equivalent to current launchable=TRUE for eligible resource-limit rows), uses the PRIMARY allocation, Slurm 4G, and one unit per task. Walls are 13:36:00 if any p1000 unit or 03:46:00 for p500 alone. Durable noclobber attempt records prevent repeated P5 task execution. The fallback inconsistency and dead-artifact cleanup above remain.

Accounting separates arrays/reruns/P5/precompile, excludes step double-counting, preserves scheduler rows and distinguishes allocated CPU time from elapsed core time. **Minor clarification:** 10,100 core-hours is the sum of native fit budgets, not the requested primary Slurm wall ceiling. The two primary arrays request 2,320 + 8,220 = **10,540 core-hours**, or **10,541** including the one-hour precompile request, before reruns/P5. JOB.md discloses excluded margins, but accounting_summary.py:16,56 calls 10,100 an allocated ceiling; rename it native-fit-budget ceiling and also show the requested-wall ceiling. Expected usage and billed logical CPU time are different quantities.

Answers to the builder's four questions:

1. **QoS:** recommend restoring explicit --qos=nots_commons consistently to precompile, primaries, infrastructure reruns and P5, matching the successful historical production setup. Omission is not demonstrated to be invalid by these local checks; the pilot's default is not proof of equivalent production scheduling policy. OPS can instead record a current default-QoS equivalence check before launch. No remote check was made in this review.
2. **Terminal infra_repeat/timeout before P5:** do not automatically block unrelated eligible resource-limit units once those exceptions are terminal, individually reconciled and explicitly reported/acknowledged by HQ. D11 is per unit. Keep blocking live, not_run, rerun_queued, infra and orphan units. P5 must not retry timeout or infra_repeat.
3. **Name-filtered throttle:** insufficient as a guarantee without enforced naming/unknown-array handling; R2-8.
4. **Poll reading:** maximum ten minutes between polls; use 5–10 minutes and >600-second lateness, R2-10.

## Checks run and evidence

- Read review 1, disposition, specified code/evidence, historical GO_2400/runner/OUTPUTS, charter/decisions, and all PROD-H runner/staging scripts, tables and tests.
- Independently verified all **27 manifest hashes**, manifest SHA-256 fda7c3f3a8e02f28bde82c3aa67aa243ec1eb1fb33a3e9e49e4ee44d1013789c, and diff SHA-256 807d16509b70fd99e5ad1e370dbdd2992ec9808eed3fa3ba52f8e6e2dea19e06. All **21 core files** match v2.2 byte for byte. The six-file diff applies in a scratch dry run. E/hash_audit.json, python_probes.log, diff_dryrun.log.
- Re-ran copied lane G scripts against copies of current source and saved fixtures: F1 **23/23**, F2 **24/24**, F3/F7 **26/26**, F4 **22/22**. All are stubs/resumes, not numerical fits. E/laneG/results/, g_f*.log; F4's corrected run is g_f4_corrected.log.
- Re-ran my original scan/valid-commit/resume reproduction against the fixed tree: E/review1_scan_corrected.log. Original edge controls confirm H NULL refusals; its earlier synthetic race uses mocked validity and is not used as evidence against the fixed production lock. The real saved-record interleaving and lane G are decisive.
- Additional owner.txt write failure: error propagates, no core call, caller-owned lock removed. Existing foreign locks remain untouched. E/adapter_extra.log.
- Re-ran the amended a2 classifier on the four saved pairs and all **15 supplied controls**, redirecting all output writes to E/a2_results. Added independent differing-checkpoint type-corruption probes. E/a2_probes.log, a2_saved_controls.log.
- Re-ran pilot shell suite on a scratch copy: **54 passed, 0 failed**, including native symlink tests. E/pilot_shell.log, pilot_shell/SHELL_TESTS.md. Both actual frozen checks and the original unlisted-symlink reproduction were independently exercised: E/frozen_probes.log. Read the saved 88-case negative-suite evidence; did not rerun numerical pilot work.
- PROD-H full suite independently rerun on a scratch copy: **overall exit 0**, Python **30/30**, shell **111/111**, real CLI parser **6/6**, syntax **25/25**, table audit **1/1**. Fresh summary timestamp 2026-10-29T15:36:09Z; E/run_all.log and E/campaign/conformance/jobs/PROD_H_DRAFT/tests/{summary,py_tests,shell_tests,cli_parser,syntax,tables}.log. No real scheduler or fit was used.
- Final source snapshot: **51/51** reviewed source/table files still match their initial scratch copies. E/reviewed_source_snapshot.json. The original builder summary log was not overwritten.
- Additional C3 failed-hold, missing-native fallback, P5 killed-child/manifest recovery, and successful-sbatch/failed-journal probes: E/python_probes.log, adapter_extra.log, failure_paths_corrected.log, submission_record_probe.log. Stub scheduler calls only.

Setup corrections are retained in scratch: the initial scan reproduction lacked its input_fixture (created before the corrected rerun); Windows child R required en_US.UTF-8 to match saved serialization hashes; the first kill-path shell probe used a mixed Windows path in PATH and was corrected to a POSIX path. These setup failures are not production failures. No claim here relies on those initial attempts.
