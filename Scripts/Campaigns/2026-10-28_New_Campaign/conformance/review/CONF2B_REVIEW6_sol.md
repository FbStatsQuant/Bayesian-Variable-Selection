# CONF-2b review 6 — narrow R5-1 / R5-2 re-check

Reviewer: Sol 6.1, independent reviewer for Felipe. 2026-10-30 UTC.

**R5-1: RESOLVED. R5-2: PARTIAL. PROD-H: NOT READY for HQ → OPS.**

The retirement race is closed by the shared lock. All four original accepted-before-ID **wrapper-signal** reproductions now fail closed and preserve their signal exits. However, another exit in that same acceptance interval still removes exclusion without proving rejection: a signalled **sbatch client**, with the wrapper left running. Two independent targeted cases produce two live scans. This is a should-fix finding within this narrow re-check.

Campaign **C** is `<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign`. Evidence **E** is `<PC_TEMP_PATH>`. Source locations below are relative to `C/conformance/jobs/PROD_H_DRAFT/`.

Only this review and new scratch files under E were written. Execution used copies of unchanged production runners, fabricated scheduler commands and checksum-valid one-unit fixtures. No SSH, NOTS access, real scheduler submission, compilation, sampler fit, simulation or numerical experiment was performed. R 4.4.1 was inspected for its version only. No historical findings beyond the requested lock/retirement/acceptance scope were reopened.

## Finding R6-1 — should-fix (high): nonzero sbatch status is not proof of nonacceptance

**Location:** `runner/p5_scan_run.sh:89–91`, especially the unconditional removal of `IN_FLIGHT` at line 90; the resulting EXIT unlock is at `:48` and `runner/common.sh:156–164`.

The new branch treats **every nonzero sbatch exit** as “nothing was accepted.” A client process can die after the scheduler has accepted its request but before it delivers the ID to the wrapper. In that case its nonzero exit proves that the client failed, not that the scheduler rejected the job. This branch deletes the only durable exclusion even though no ID, terminal proof or uncertainty marker has replaced it.

**Independent reproduction, actual copied runner, no runner edits:**

1. The fake scheduler durably accepts live job **8101** and pauses before returning its ID. `IN_FLIGHT` exists; there is no job record. Save the marker and the sbatch client's PID.
2. Signal only that client, leaving the actual scan wrapper alive. TERM yields sbatch status **143**; KILL yields **137**.
3. In both cases the wrapper exits **2**, reports “the scan job was not accepted by sbatch,” and leaves **no submission lock, no job record and no uncertainty marker**. The accepted 8101 remains live.
4. The next actual scan wrapper exits **10**, accepts **8102**, and journals it. The saved queue contains **8101 and 8102**, both live.

Evidence: `E/sbatch_child_signal.sh`, `.log`, `.rc` (= 1; two failed safety assertions); `E/sbatch_signal_{TERM,KILL}/{A.log,B.log,inflight_before.txt,live_after.txt}`; each fixture's `stub/{accepted,sbatch.pid,sbatch_calls.txt}`. The fabricated acceptance happens before the signal barrier, rather than being inferred from timing. `A.log` explicitly records the child's 143/137 status. The replacement runs without the gate.

**Concrete fix:** keep `IN_FLIGHT` and the owned lock for a nonzero sbatch exit unless there is independent, positive evidence that no acceptance occurred. The simplest safe implementation is to fail closed on every nonzero client status, report the outcome as UNKNOWN with the client status, and direct OPS to the existing job-name/since-time recovery. Do not call this “not accepted” based only on `$rc`. If an ID can be recovered, journal it or cancel it by explicit ID and prove it terminal before clearing exclusion. Add the accepted-before-reply TERM/KILL **client** cases, as well as the existing wrapper cases, and assert one acceptance, retained exclusion and no replacement. Revise the rejection regression if it currently requires clearing the lock based only on a fabricated exit 42.

## R5-1 assessment — RESOLVED

- `common.sh:129–142` takes the same lock used by submission **before** reading the current record, and holds it across the exact-ID check, terminal proof and moves. A contending retirement returns 1 before entering the critical section; it does not unlock the owner. A delayed old-ID retirement cannot move a newer record written through this protocol.
- Reran the review-5 **direct-helper** accounting barrier: A holds the retirement lock on terminal 8000; B returns 1; direct C returns 4 after judging the old record and submits nothing. A then retires 8000 and releases the lock. A later wrapper accepts only 8101; late retirement of 8000 returns 1 and preserves 8101.
- Reran the review-5 **actual-parent** accounting barrier: A's second accounting query is inside retirement. B returns 2 and C returns 4, without acceptance. A returns 2 after retiring 8000. Later actual parent D returns 10, journals 8101 and leaves only that job live. Evidence: `E/parent_retire_race/`, `E/targeted.log`.
- Inspected **all four callers** in unchanged `p5_submit.sh`: lines **37, 84, 112, 135**. Each checks the helper result or explicitly keeps the record on failure; none submits a replacement in response to lock contention. Exit 12 is handled at line 87 before `SCAN_MADE=1` at line 90, so that refusal does not attempt retirement. Dry-run contention may still return 0 while saying the record was kept; it submits no P5 array.
- There is no nested-lock deadlock in these call paths: the child wrapper releases its owned submission lock before returning a verified scan to the parent, and the parent then acquires its own retirement lock. Actual dry runs with one eligible unit and with zero eligible units, plus a post-verification malformed-table refusal, exercise lines 135, 112 and 37 respectively. Each retires the scan and leaves no lock. The failed-scan parent barrier exercises line 84.
- Original submission overlap, absence-check/recheck, wrong/missing-ID and live-ID retirement controls also pass. Contenders leave the owner's lock in place. No lock-ownership confusion was observed in the reviewed call graph.

## R5-2 assessment — PARTIAL

The original wrapper-signal defect is repaired. At the same accepted-before-ID barrier used in review 5:

| Signal sent to wrapper | Wrapper exit | IN_FLIGHT lock | Subsequent wrapper / retirement / parent | Accepted live jobs |
|---|---:|---|---|---:|
| TERM | 143 | kept | 12 / 1 / 2 | 1 |
| HUP | 129 | kept | 12 / 1 / 2 | 1 |
| INT | 130 | kept | 12 / 1 / 2 | 1 |
| KILL | 137 | kept | 12 / 1 / 2 | 1 |

Each fixture has no job record after the interrupted call. The next wrapper explains IN_FLIGHT, possible acceptance and manual resolution. Evidence: `E/signal_{TERM,HUP,INT,KILL}/`, `E/targeted.log`. Pre-sbatch TERM still exits 143, releases its lock and accepts nothing; post-journaling TERM exits 143 and preserves the recorded live ID with the lock already released (`E/signal_boundaries.*`).

**Exit-path audit from writing IN_FLIGHT to clearing it:**

| Path | Assessment |
|---|---|
| Failure writing the initial marker (`:87`) | Occurs before sbatch; no acceptance is possible through that invocation. |
| Wrapper signal/exit while awaiting sbatch (`:88`) | Marker remains; unlock refuses; exact signal exits independently verified. |
| Nonzero client status (`:89–91`) | **Unsafe: R6-1 above.** |
| Zero status but unusable ID (`:94`) | Refuses and retains marker/lock; independently exercised. |
| Failure appending the known ID to IN_FLIGHT (`:95`) | Under `set -e`, EXIT retains the existing marker. Code inspection. |
| Record/journal failure, cancellation proven terminal (`:97–101`) | Clears marker safely; exit 5. Job-record and jobs.tsv failure controls exercised. |
| Record/journal failure, abort unresolved (`:103–104`) | A nonempty uncertainty marker takes over before removal; exit 11. Independently exercised with cancellation failure. |
| Failure to create that uncertainty marker | With no nonempty replacement marker, `:103` leaves IN_FLIGHT. Code inspection; no successful fault-injection evidence claimed. |
| Both journals written (`:106–107`) | ID is durable before clearing; safe. Live, verified, terminal-failed and scheduler-query-error exits exercised. |
| Failure removing IN_FLIGHT | Cannot open the lock: EXIT sees the marker and refuses unlock. Code inspection. |

`JOB.md:101–104` now correctly warns that process death is insufficient, identifies the possible job by its saved name and since-time, requires explicit-ID cancellation and terminal accounting, and says to log recovery. For a positively identified job this is an appropriate manual recovery route. “Only then” must be applied literally: an empty or failed scheduler query is not terminal proof, and an outstanding sbatch client must finish before acceptance can be considered resolved. No stale IN_FLIGHT in the tested original signal cases silently opens submission; the next-wrapper diagnostic is clear. The procedure cannot compensate for R6-1, where the runner deletes the marker and lock itself.

## Checks and saved results

Substantial shell checks were launched detached, with commands, UTC launch times, PIDs, logs and exit files in E. No full 1–2 hour suite rerun was needed.

- `targeted.sh` / `targeted.log` / `targeted.rc`: **34/34 pass**, exit **0**. Adapted review-5 overlap/recheck/exit controls, both retirement races and all four original wrapper-signal cases. Expectations were updated for the intended new fail-closed invalid-ID/retirement behavior. An early diagnostic `count()` prints “accepted: No such file” before any acceptance in the full-parent race; the asserted final acceptance and saved queue are valid and pass.
- `signal_boundaries.sh` / `.log` / `.rc`: **2/2 pass**, exit **0**; unchanged review-5 boundary logic against current copied runners.
- `sbatch_child_signal.sh` / `.log` / `.rc`: **0 pass, 2 failing safety assertions**, exit **1**; independently reproduces R6-1 for TERM and KILL.
- `additional_clean.sh` / `.log` / `.rc`: **7/7 pass**, exit **0**; the three parent retirement branches above and two jobs.tsv-write-failure abort/handoff controls, including no replacement. Initial `additional.*` also contains a failed marker-write fixture that was refused **before sbatch** (it created a directory at the uncertainty path too early), so its two assertions are harness diagnostics, not production findings. `additional_confirm.*` failed setup on already-existing fixture directories; the clean rerun uses fresh directories. Both diagnostics are retained and excluded from the passing totals.
- `syntax.json`: **15/15** production runner shell/sbatch files pass `bash -n`. `audit.log` / `audit.rc` = **0**. `frozen_runner_check.json`: the production frozen-tree verifier passes on the actual tree, exit **0**, including membership/special-entry checks. `unchanged_parent.json`: `p5_submit.sh` is byte-for-byte unchanged from review 5.
- Inspected the supplied suite, **not rerun**: `C/conformance/work/conf2b_runs/prodh_20261030T0450Z/shell_tests.log` reports **220/220**, including all 14 R5 cases; `py_tests_rerun_0720.log` reports **51/51**; the saved summary records CLI **6/6**, syntax **27/27**, tables **1/1**. The original `summary.log`/`run_all.rc` remain **overall exit 1** because the first Python run was 50/51; the separate Python rerun is the evidence for the timing-test correction. Existing R5 tests signal the wrapper and cover an explicit stub rejection; they do not cover an accepted client dying before replying.
- Inspected all runner differences from the preserved review-5 snapshot (`runner_since_review5.diff`): only `common.sh` and `p5_scan_run.sh` changed. Inspected `REVIEW5_FIXES.md`, JOB recovery, the R5 test block and the cadence timing change.

Tool versions: Git Bash **5.2.37**, `py -3` Python **3.13.1**, Rscript **4.4.1** (version only). Fixtures have no random seed or numerical results. E preserves copied sources, fixture configuration, fabricated scheduler states, launch metadata, process/exit evidence and SHA-256 evidence hashes.

## Frozen tree and write audit

`C/code/core/v2_2_1.SHA256SUMS` SHA-256 is exactly:

`d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1`

**27/27 listed files verify.** The actual frozen-tree membership check passes. **All 269 snapshotted reviewed/source/evidence files are unchanged**, with no added files in the reviewed bundle, frozen tree or supplied suite. Evidence: `E/source_snapshot.json`, `E/hash_audit.json`, `E/frozen_runner_check.json`, `E/final_audit.json`, `E/EVIDENCE_SHA256.json`. The only campaign write is this requested review. The frozen numerical code was hash-checked, not re-reviewed or executed.
