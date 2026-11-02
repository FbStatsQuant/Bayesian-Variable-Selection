# Independent review: LOWP NOTS pilot bundle

**Verdict: REJECT — do not submit this revision.**

Reviewer: Sol 6.1, independent review performed directly, without subagents. Reviewed 2026-10-28 CDT / 2026-10-29 UTC. Scope: the named `code/lowp/pilot/` bundle and the exact context, CLI and OPS paths in the brief. Paths below are relative to the campaign root; `pilot/` abbreviates `code/lowp/pilot/`.

The bundle covers the intended pilot arms and its ordinary command lines largely match the current runners. However, submission errors are swallowed, truth is not locked throughout fitting, cleanup fails open when scheduler inspection fails, and the summary can present an incomplete or failed pilot with every verdict PASS. The supplied disk guard also implements superseded charter limits. These prevent approval.

## Findings

1. **[blocking] Failed `sbatch` calls do not stop the driver.**

   **Location:** `pilot/submit_pilot.sh:71–74`, called through command substitutions at lines 76–87.

   **Evidence:** `submit()` runs inside `$(...)`, where ordinary Bash disables inherited `errexit`. A rejected `sbatch` is followed by a successful `printf` and `echo`, so the function succeeds with an empty ID. With a scratch-only stub that rejects every submission with exit 42, the real driver attempted all ten submissions, wrote ten empty IDs, generated dependencies such as `afterok::` and `afterany:::::::::`, and exited **0**. See `review_pilot/sbatch_failure.log`, `shell_test_transcript.txt`, and `sbatch_calls.txt` in the evidence directory below.

   **Fix:** explicitly test the `sbatch` assignment and return nonzero on failure; validate and normalize the returned parsable job ID before recording or using it. Abort subsequent submissions on the first failure, preserving the successfully submitted IDs and a clear partial-submission record. Add a regression test with failure in the middle of the chain as well as at the first call.

2. **[blocking] Truth is readable for most of the fitting wave.**

   **Location:** `pilot/submit_pilot.sh:78–85`; `pilot/slurm/s0_truthlock.sbatch:30–34`; `pilot/JOB.md:83,92,174`; `code/lowp/tests/test_truth_lock_linux.sh:11,55–80`.

   **Evidence:** all fitting jobs depend only on build and regeneration. The separate truth-lock test also starts after regeneration, locks/unlocks repeatedly, and leaves both trees readable at 755/444. There is no wave-wide lock operation or dependency on a successful lock. Fits can run concurrently with the test and continue after its final unlock. Passing a truth-free `DEV_STUDY` prevents an intended input-path leak, but does not satisfy charter/LOWP_SPEC/RUN_DESIGN's requirement that existing truth trees be mode 000 during fitting.

   **Fix:** finish regeneration and the permission test, then lock both staged truth trees and verify the lock before releasing fitting jobs. Restore through an `afterany` finalizer only after every fitting job is terminal, with an explicit OPS recovery procedure for cancellation/finalizer failure. Run collection/guard measurements after restoration. Keep verification/scoring outside the locked fitting phase.

3. **[blocking] Cleanup proceeds when it cannot determine whether jobs are active.**

   **Location:** `pilot/cleanup_pilot.sh:25–27,51,55–60`.

   **Evidence:** the `squeue | grep` pipeline is an `if` condition. With `pipefail`, an `squeue` error makes that condition false and cleanup continues. In the scratch-only test, `squeue` exited 17; `cleanup_pilot.sh --yes --keep-staged` removed the run sentinel and printed **CLEAN**, exit **0**. Scheduler stderr is suppressed. The residue search suppresses its own errors and the final guard is explicitly ignored, so CLEAN is also possible without successful final verification.

   **Fix:** capture scheduler output/status first and refuse deletion if inspection fails. Check the recorded explicit job IDs and all relevant active states. Propagate residue-search and guard errors; distinguish verified cleanup from an unverified outcome. Preserve the existing refusal for retained results/logs, which did work in the local test (exit 3).

4. **[blocking] Summary verdicts do not establish completion or successful execution.**

   **Location:** `pilot/summarize_pilot.R:58–105,155–202,233–243`; `pilot/JOB.md:123–129`.

   **Evidence:** discovery reads available RDS/CSV files, skips missing/unreadable files, and never checks the required unit lists, `.done` markers or sidecar agreement. `timing$rc` is never checked. Slurm states are displayed but do not affect verdicts. Independent fixture tests all exited 0 and retained **eight PASS verdicts** after (a) a benchmark timing row was changed to rc 2; (b) all 192 benchmark completion markers and sidecars were removed; (c) all four repeat CSV statuses were changed to failed; and (d) the entire benchmark result arm was omitted, leaving only 67 unit rows. The repeat verdict still said the fits were valid because it checks only unequal seeds. Missing arms need not even receive a NOT RUN verdict. Failed-unit CPU/time can also contaminate the sizing table.

   **Fix:** validate the expected exact set of 30 enum20, 6 enum30, 3 scaling, 24 primary SMC, 4 repeat SMC, and 192 benchmark units, plus required timing/report/accounting records. Validate completion protocols and hashes before accepting a unit. Add explicit execution, count, fit-status and scheduler verdicts; fail or mark INCOMPLETE for absent evidence. Check repeat seed offsets/identity and fit validity, not just inequality. Emit a nonzero acceptance exit status when required checks fail. Keep descriptive partial summaries available, clearly labeled incomplete.

5. **[blocking] The supplied OPS guard does not enforce the current charter.**

   **Location:** `ops/guard.sh:15–16,38–39`; `CHARTER.md:§2.2`; `pilot/submit_pilot.sh:17,23–27`; `pilot/JOB.md:54`.

   **Evidence:** the charter currently requires campaign home ≤ **0.5 GiB** and total home ≤ **9.6 GiB**. The named guard instead permits campaign home up to **7 GiB** and refuses total home above **9 GiB**. It can therefore admit a campaign footprint above the binding campaign ceiling, and refuse otherwise compliant total usage. The brief, scaffold and RUN_DESIGN retain older figures. The driver does correctly invoke the guard with 30 MB and stop on refusal (independently reproduced: exit 1, zero sbatch calls). Thirty MB is conservative relative to the bundle's stated staged footprint plus core cache, but its actual sufficiency awaits the final staged archive/build.

   **Fix:** OPS must reconcile the guard and supporting documentation with the current charter before staging/submission, verify the final staged size and cache allowance, and preserve a successful pre-stage/pre-submit guard receipt. Do not bypass this mismatch through test-limit overrides.

6. **[should-fix] Missing enumeration evidence defaults to success.**

   **Location:** `pilot/summarize_pilot.R:69–80,175–182`.

   **Evidence:** absent status/complete fields default to exact/TRUE, absent recheck statistics become zero, and a missing expected model count bypasses the count comparison. In a disposable fixture, one record was changed to `models_scored = 1` and its required completion/count/numerics fields removed; all verdicts remained PASS. The provided fixture generator also copies one p20 template into p30 envelopes without updating K/model counts or scale dimensions (`pilot/tests/make_fabricated_pilot.R:16–27`), so its baseline is not an independent semantic check of full p30 enumeration.

   **Fix:** enforce the current schema and required fields, two named scales, p/K/dimensions, full scope, expected model count derived from the design, positive recheck coverage, and finite valid numerical outputs. Missing evidence must be INCOMPLETE. Construct p-specific fixture envelopes and add deliberate malformed-record cases.

7. **[should-fix] The documented `sacct` memory fallback does not feed sizing.**

   **Location:** `pilot/summarize_pilot.R:75,89–92,101–103,218–225,240–243`; `pilot/JOB.md:172`.

   **Evidence:** only SMC has a record-based fallback. `sacct` MaxRSS is parsed later into Markdown and never joined into unit/table/projection memory. With GNU-time RSS set to NA and fabricated valid batch MaxRSS still present, enum20, enum30 and both benchmark projections had `suggested_mem_request_mb = NA`, while every verdict remained PASS. This contradicts the documented fallback and leaves the pilot unable to size those arms in that supported case.

   **Fix:** join batch-step accounting by job/task ID before aggregation. Where one job runs multiple units, label its peak as a job-level conservative bound rather than a measured per-method peak. Require usable memory evidence for sizing, or stop acceptance with an explicit missing-measurement verdict.

8. **[should-fix] Collection cannot prove its own terminal COMPLETED state.**

   **Location:** `pilot/slurm/s9_collect.sbatch:20–23`; `pilot/submit_pilot.sh:87`; `pilot/JOB.md:123`.

   **Evidence:** the collector queries the job-ID file while it is running. If its own row is present, its accounting state is RUNNING rather than COMPLETED; there is also a startup race with appending that row. Thus the stated acceptance check that every recorded job is COMPLETED cannot be met from this snapshot alone. `sacct` failure is tolerated with no acceptance failure.

   **Fix:** capture terminal accounting for predecessor jobs in the collector, then have OPS append a final terminal snapshot including the collector after it exits. Validate expected IDs/array tasks, states and exit codes, and treat unavailable accounting as incomplete evidence.

9. **[should-fix] Bit-identity checks mix numerical equality and bit equality, and overrequire aggregate identity.**

   **Location:** `pilot/R/pilot_bitid.R:25–27,40,57,70`; `code/lowp/enum/README.md:49–50`.

   **Evidence:** T2/T3 count differences with numeric `!=`, which does not distinguish signed zero or all IEEE representations. Conversely, T1 requires bit-identical log Z even though the current enumerator contract explicitly permits rounding differences in aggregate log Z/PIPs versus the core due to accumulation order. This can certify weaker-than-described score comparisons or reject a conforming NOTS build for an aggregate rounding difference.

   **Fix:** compare serialized float64 bytes for the claimed F/eta bit checks, with explicit handling of nonfinite values. Apply a declared numerical tolerance to aggregate log Z/PIPs consistent with the enumerator contract; retain exact model/tie decisions and same-split thread invariance checks. Record both byte mismatches and numerical differences.

10. **[should-fix] Cleanup has no ownership boundary for shared deployed code.**

    **Location:** `pilot/cleanup_pilot.sh:30–36,51–52`; `pilot/JOB.md:49–52,164–165`.

    **Evidence:** default cleanup removes entire `code/core/v2_2`, `code/lowp` and `code/bench_lowp` trees, regardless of whether they existed before staging or were later updated. The queue filter only covers `lowp_p*`; other campaign jobs can use those shared trees. The documented extraction also overwrites those shared destinations without a freshness/ownership precondition. The lexical prefix checks bound deletion to the configured roots but do not establish pilot ownership.

    **Fix:** deploy into a pilot-owned versioned location, or require and record fresh destinations and delete only an immutable inventory owned by this pilot. Refuse cleanup when any dependent campaign job is active or ownership has changed. Explicitly validate canonical root/parent paths before recursive deletion. `--keep-staged` is a useful option, but does not make the default safe for an existing deployment.

11. **[should-fix] Local test hooks are inherited by real jobs without a production refusal.**

    **Location:** `pilot/submit_pilot.sh:59`; `pilot/slurm/common.sh:34,69`; `pilot/slurm/s1_enum20.sbatch:27`; `pilot/slurm/s3_bench.sbatch:27,30`.

    **Evidence:** `--export=ALL` passes through `PILOT_DRYRUN`, `PILOT_SKIP_MODULES`, `PILOT_LIMIT`, `PILOT_BENCH_METHODS` and `PILOT_BENCH_EXTRA`. They can respectively suppress execution/module loading, truncate enumeration, omit methods, or add `--test-library` despite a real submission. Comments say local-only, but no driver check enforces that. In addition, the benchmark CLI's sealed-library-location check is conditional on `!dev` (`code/bench_lowp/run_bench_case.R:106`), whereas every pilot case is dev.

    **Fix:** refuse test hooks for NOTS submissions or explicitly clear them with a controlled export allowlist. Verify that benchmark records use the intended R 4.5.2 pinned library/dependency provenance and `test_library = FALSE`, including for dev pilot IDs. Record the final effective environment.

12. **[should-fix] The supplied fixture test is not self-contained within the bundle.**

    **Location:** `pilot/tests/make_fabricated_pilot.R:6–9,33,47`; `pilot/LOCAL_TEST.md:47`.

    **Evidence:** SMC/benchmark templates are hardcoded to earlier temporary smoke directories outside the review's allowed paths; only the exact template has an override. No fabricated tree or template records are shipped under `tests/`. Consequently the stated complete-tree test cannot be reproduced from this bundle alone. This review used a scratch copy of the generator with its template root redirected and small schema-shaped stand-ins constructed from the named interfaces; no out-of-scope smoke artifacts were read.

    **Fix:** ship minimal versioned p20/p30 templates or construct them in the test, parameterize all template paths, and assert expected summaries, completion failures and nonzero acceptance status. Keep fixture times explicitly fabricated. See finding 6 for the p30 template semantics.

13. **[should-fix] Preserve the final OPS configuration with downloaded run evidence.**

    **Location:** `pilot/stage_local.sh:49–50`; `pilot/submit_pilot.sh:55–59,71–72`; `pilot/JOB.md:117,132–165`.

    **Evidence:** `pilot.env` is deliberately excluded from staged hashes so OPS can fill it, but the driver does not save/hash the final edited file or a complete effective launch configuration in the downloaded log folder. The staged hash list stays in home `runs/<PID>` and is deleted by cleanup. Module/R environment reports and unit/source hashes are useful, but do not replace an immutable configuration and launch receipt.

    **Fix:** before submission, copy/hash the final `pilot.env`, staged hash list, JOB, unit lists and exact sbatch argument vectors into the run logs. Preserve the corresponding staged source archive locally under a durable run ID. Include guard receipts, timestamps and final accounting before verified deletion.

14. **[minor] JOB's login-node instruction is stale.**

    **Location:** `pilot/JOB.md:70`; compare `CHARTER.md:§3` and `ops/NOTS_ENV.md:6`.

    **Evidence:** JOB says loginx3; the current charter/OPS notes require the configured `ssh nots` alias pinned to loginx2. No bundle script actually invokes SSH, which is correct.

    **Fix:** say “OPS, through the configured `ssh nots` alias, one connection at a time”; avoid a stale physical login-node instruction.

15. **[minor] State the fitting sample coverage consistently with RUN_DESIGN.**

    **Location:** `code/lowp/RUN_DESIGN.md:50`; `pilot/JOB.md:15–17`; `pilot/lists/enum30.txt:1–6`.

    **Evidence:** RUN_DESIGN describes measurements “on the 60 dev datasets,” but the fitting lists cover 30 p20 datasets and six p30 datasets, with SMC/benchmarks restricted to 12 datasets at two scales. Regeneration checks all 60 dev manifest rows; it does not provide missing fit-time measurements. The selected subsets can still size a pilot, but the sample claim is overstated.

    **Fix:** document the per-arm subset and its extrapolation limits in RUN_DESIGN and the summary, or extend the lists if all 60 fitted datasets are actually required. Do not silently treat manifest/regeneration coverage as timing coverage.

## Checks and evidence

Evidence directory: `<PC_TEMP_PATH>`.

| Check | Observed result |
|---|---|
| Git Bash `bash -n` | PASS: all 15 bundle shell/env/sbatch files, plus the named truth-lock test and OPS guard (17 files total); `bash_syntax.txt` |
| R 4.4.1 parsing | PASS: all five bundle R files; `summary_test_transcript.txt` |
| Fabricated complete baseline | 259 units, 22 arm/p table rows, eight PASS verdicts; independent assertions verified wall medians, peak-memory maxima, mean record bytes and enum30 allocated core-hours |
| Supplied bad fixture variant | Correctly shows generator STOP and truth-lock/bit-identity/recheck/thread-invariance failures; summarizer still exits 0 |
| Adversarial summary cases | Reproduced false PASS for nonzero timing rc, missing benchmark markers/sidecars, failed repeats, missing benchmark arm and missing required exact-record fields |
| Missing GNU-time RSS | Reproduced NA enum/benchmark memory requests despite available accounting; `extra_test_transcript.txt` |
| Guard/cleanup positive refusals | Guard nonzero stops driver with exit 1 and zero submissions; retained results stop cleanup with exit 3 |
| Submission/scheduler failures | Reproduced submission exit 0 after ten sbatch rejections; cleanup exit 0/deletion after squeue failure; `shell_test_transcript.txt` |
| Bundle preservation | All 26 files have identical before/after SHA-256 entries in `reviewed_sha256_before.txt` / `reviewed_sha256_after.txt`; no reviewed file edited |

Reproduction harnesses are `review_summary_tests.R`, `review_extra_tests.R` and `review_shell_tests.sh`. They use only disposable roots under the evidence directory. The R harness evaluates a scratch copy of the supplied fixture generator with scratch-only templates, then invokes the unchanged summarizer. These are structural/logic tests, not simulation, benchmark or timing evidence. The complete baseline's arithmetic is correct for the fabricated input values; its all-PASS result does not validate the scientific contents of those fabricated records.

Static checks that passed: all ten sbatch files explicitly request account/partition `commons`, `constraint=sapphirerapids`, one node/task, memory, time and CPUs within the supplied NOTS facts. Driver arrays 0–5, 0–27 and 0–23 match the checked-in dev-ID lists; indices and `--development`, `--study`, `--outroot`, repeat and library flags match the current named CLIs. Fitting covers 36 distinct dev datasets; regeneration checks all 60 dev manifest rows (see finding 15). Regeneration passes the required production/dev manifests and six-copy study to the strict 0/1/3 CLI; nonzero rc is recorded and the verify job fails, so `afterok` prevents fits after a genuine verification failure once submission handling is fixed. `timed()` records unit rc and `pilot_finish()` fails a task containing failed commands.

Explicit shell output, log and temporary paths default to the two permitted campaign roots. There is no script SSH command, shell home expansion, whole-disk scan, or explicit write/chmod/move into either frozen benchmark tree. The benchmark library is passed for reading. BLAS/thread environment limits are set before fitting; enumeration alone raises its OpenMP count. Enumeration cache and per-task temp directories are under campaign scratch; the core cache is under the staged campaign-home core. Actual compile-key reuse, permissions and owner writability still require OPS inspection. The benchmark runner inventories installed-package metadata and its dependency package files for provenance; this review did not inspect any R library.

JOB supplies the charter §6 essentials: commands, inputs, expected outputs, per-job resources and acceptance checks; module/compiler/library fill-ins are clearly marked. Its readiness claim is premature because the findings above affect execution and acceptance. Final archive size, real Slurm dependency/cancellation semantics, Linux mode-000 behavior, actual NOTS toolchains/pinned packages, scorer identity, memory and Sapphire Rapids timings remain unverified here. No SSH/NOTS/Owls connection, model fit, enumeration, data generation or benchmark was run. Real staging was not executed because its source dependencies and sealed data extend beyond the paths authorized for this review. No README-type file exists in the named `ops/transfer/` directory; its implementation files were not read.

## Compact hand-off

**REJECT.** Five blocking findings: swallowed submission errors, no fitting-wave truth lock, cleanup that fails open, acceptance summaries that miss failed/incomplete runs, and an outdated disk guard. Syntax and fabricated arithmetic checks passed; negative tests reproduced the failures above. Save this review and its scratch evidence, fix the blockers and supporting acceptance/provenance gaps, then obtain a fresh independent bundle review before OPS submission. No reviewed files were changed.
