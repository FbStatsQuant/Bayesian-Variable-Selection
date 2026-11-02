# LOWP final confirmation 2 — independent Sol 6.1 review

**OPS handoff: NO-GO for the current pilot bundle.** The original FC1–FC6 and FC8 reproductions are repaired. FC7 is only partly repaired: the summary still gives OVERALL PASS to missing or zero unit wall measurements and to scaling evidence from the wrong dataset or with a wrong total model count. These are release blockers for a bundle whose purpose is trustworthy production sizing. FC9 retains minor contradictory wording. All requested shipped suites passed; passing them does not cover the additional counterexamples below.

Reviewer: Sol 6.1, independently, no subagents. Review execution: 2026-10-29 04:26–04:36 UTC (2026-10-28, Chicago). ROOT/CAMP have the meanings in the brief. Evidence root, abbreviated **E** below:

`<PC_TEMP_PATH>`

## Scope and execution

Read the named context, previous FINAL_CONFIRM report/probes, changed implementations, tests and documentation. Felipe additionally authorized the scoring suite's core dependency and external benchmark smoke outputs. Current core sources were copied to `E/snapshot/code/core/v2_2/core`; compilation and every test/report write occurred in scratch. No reviewed implementation was edited. Before/after SHA-256 comparison found **all 122 snapshotted reviewed/dependency files unchanged** (`source_before.csv`, `source_after.csv`, `source_integrity.txt`). This includes the authorized core; no build was run inside `CAMP/code/core`.

R was `C:/Program Files/R/R-4.4.1/bin/Rscript.exe`. The temporary LOWP library was prepended, retaining the default user library and R's own library; `fc_probes.log` records `.libPaths()` and `sessionInfo()`. BLAS/MKL/OpenMP defaults were one thread, with enumerator probes explicitly using two. Independent numerical probes used seed 20261029; the shipped fabricated pilot uses seed 7; suite seeds remain in their source snapshots. No SSH/NOTS, full p = 30 enumeration, real benchmark fitting, real staging/submission or deployment-library modification occurred.

The scratch copy of enum t10/t11/t12 and helpers only relocates their hard-coded CAMP path to the snapshot. Test assertions and production implementation bytes were unchanged. Scoring ran from its scratch copy, including the authorized external real-smoke registry comparison; it had no skipped assertions. Locale startup warnings and the local data.table build-version warning were retained. t10's global `tasklist` wait was slow on this shared Windows machine but eventually returned; no check was bypassed.

Commands, arguments, UTC start/end times, launcher PIDs, exit codes and logs are in `run_suite.ps1`, `*.status.json`, `execution_summary.csv` and `*.log`. Source/configuration snapshots and hashes, probe scripts, mutated/re-signed records, summaries and projections are retained. `evidence_sha256.csv` indexes saved evidence, excluding disposable compile caches and R temporary directories.

## Shipped suites rerun

All exited 0. Assertions/checks were inspected, rather than treating exit 0 alone as proof (enum scripts do not themselves fail their process on every failed assertion).

| Suite | Result | Evidence relative to E |
|---|---|---|
| Enum t10_cli_completion.R | **36/36 PASS** | `t10.log`; concurrent child logs in `enum_suite/` |
| Enum t11_partial_and_validation.R | **32/32 PASS** | `t11.log` |
| Enum t12_exact_contract.R | **61/61 PASS** | `t12.log` |
| Benchmark test_derived_conditions.R | **3/3 PASS** | `bench.log`: no condition, warning-only, message-only |
| Scoring test_scoring.R, including review/recheck regressions | **187/187 PASS, 0 skipped** | `scoring.log`, `snapshot/code/scoring/tests/TEST_REPORT.md` |
| Pilot test_shell.sh | **34/34 PASS** | `shell.log`, `shell/SHELL_TESTS.md` |
| Pilot run_negative_tests.R | **45/45 expected outcomes** | `negative.log`, `neg/NEGATIVE_TESTS.md` |

Total: **398 successful checks/assertions/cases**. Pilot fixture costs, memory, scheduler states and reports are fabricated logic-test data, not campaign measurements.

## FC1–FC9 dispositions

“FIXED” here closes the previously demonstrated defect; additional issues discovered during this review are listed separately below.

| ID | Disposition | Independent evidence and qualification |
|---|---|---|
| **FC1** | **FIXED** | Replayed the unsealed-to-sealed sequence: existing unsealed output is recomputed with sealed provenance, not skipped. Re-signed wrong dimensions, false top completeness, stale source, missing fields, partial scale and joint-valued size masses all recompute. t12 also checks changed manifest identity and retained-map/input binding. `fc_probes.log`, `fc_observations.rds`, `probe_enum_*.log`, `t12.log`. CLI calls the shared validator with X, dataset/input/manifest hashes, requested mode and exact scale set at `run_enum_dataset.R:94` and `:149`. |
| **FC2** | **FIXED** | On a p20 input with one constant column, API and CLI score exactly 524288 = 2^19 models, original p remains 20, K/retained map are 19, and the CLI publishes consistent marker/sidecar/RDS. A rerun verifies and skips. `fc_probes.log`, `probe_enum_11_drop.log`, `probe_enum_12_drop.log` (also t12). Coverage at CLI `:133` now uses retained `run$p`. |
| **FC3** | **FIXED** | Reused the prior saved three-point fixture with all original rules failed, zero warning count, and only captured message text. The successful restricted row is now `warning`, retains the message, has `k_valid_max=1` and `ebic_at_largest`. `message_only_probe.csv`, `fc_probes.log`; shipped three-case suite passes. `common.R:68–69` detects message/warning text independently of original failure status. |
| **FC4** | **FIXED** | Re-signed genuine producer record: missing both counts, equal zero counts, absent c050, false top completeness and partial scale all return `ok=FALSE`; clean record passes. `probe_scoring/`, `fc_probes.log`. Scoring now invokes the shared contract; G30 and the full suite pass. New cross-field consistency gaps are RC3, not a recurrence of these count/scale cases. |
| **FC5** | **FIXED (original cases)** | Replayed contradictory SMC `.done` status, top complete FALSE, missing scale status/scope and unnormalized size masses: all exit 2 / FAIL, 258/259 valid. Benchmark status consistency is covered by the shipped negatives. Current enum empty support is accepted. Baseline fixtures now carry the required metadata and normalized masses. `pilot_additional.csv`, `pilot_more.log`, `neg/NEGATIVE_TESTS.md`. Additional shared-contract consistency and SMC empty-support issues remain at RC3/RC4. |
| **FC6** | **FIXED** | The original ancestor-junction dry-run reproduction now refuses with exit **4**, before deletion; outside `precious.txt` remains. `junction_probe.sh`, `junction_probe.log`, `junction_case/`. Shipped shell suite additionally checks dry-run/real cleanup with linked runs directory and linked target, plus existing ownership/scheduler/shared-tree cases. Canonical campaign roots now bound exact resolved targets (`cleanup_pilot.sh:25–46`). |
| **FC7** | **PARTIAL** | All 16 benchmark method × p in-process medians are now finite, read from `rows$runtime_s`; CSV/RDS discrepancies reject. Missing scaling file and missing all enum30 wall times now give INCOMPLETE/3, and the silent in-process-time projection fallback is removed. However individual missing measurements, zero wall times and wrong scaling identity/coverage still give PASS; RC1/RC2 are blocking. `pilot_additional.csv`, `pilot_extra.log`, `pilot_new.csv` and saved per-case outputs. |
| **FC8** | **FIXED** | Sibling `R452_UNAPPROVED` path and version/sessionInfo defect probes now fail. Shipped negatives also reject effective R4.4.1, provenance version disagreement, R4.4.x build and absent version. Exact normalized library-parent equality, effective R4.5.2 and version/build evidence are checked for dev records. `pilot_more.log`, `negative.log`. The old `wrong_R_version` mutation still passes because it overwrites `environment$identity` with an unrelated list while leaving the current authoritative `sessionInfo` at R4.5.2; it is not evidence that a wrong effective session is accepted. Actual pinned deployment remains an OPS gate. |
| **FC9** | **PARTIAL (minor)** | I1 now includes truth `dataset_id`; JOB §1 correctly says RUN_DESIGN already states the subsets; JOB's detailed cache row identifies the small home core cache. But JOB line 11 still says “no logs, results or caches in home”, contradicting line 13. LOCAL_TEST's earlier active-looking table still says RUN_DESIGN “needs HQ to change”, despite revision 4 saying this stale instruction was removed. Align/supersede those statements explicitly. |

## Remaining findings and required corrections

### RC1 — blocking: incomplete or zero unit wall measurements still accepted (FC7 residual)

`pilot/summarize_pilot.R:237–250, 270–277, 406–409, 421` checks timing row count and exit status but never requires a finite positive wall time for each unit. V12 checks only the arm/p median; `med`, `mn` and `q90` silently discard nonfinite measurements. Zero is finite and accepted.

Independent saved cases:

- `pilot_one_enum30_wall_cpu_missing`: one of six p30 measurements has wall/user/sys NA; **exit 0, OVERALL PASS, 259/259 valid**.
- `pilot_enum30_zero_walls`: all six p30 wall measurements are zero; **exit 0, OVERALL PASS, 259/259 valid**. Its `sum/pilot_projection.csv` reports enum30 mean/p90 wall **0**, expected task time **00:00**, **0 core-hours**, and a 15-minute request.
- `pilot_all_enum30_CPU_missing`: all CPU measurements absent also gives PASS. CPU availability needs an explicit policy; allocated-CPU wall projections alone do not recover observed CPU usage.

Require finite positive process wall measurements **per required unit**, before marking it valid and using it in sizing; missing evidence must make the overall result INCOMPLETE, zero/negative values invalid. Apply an explicit CPU-availability policy, and prevent summaries/projections from being labelled accepted when required evidence is absent. Add these cases to the shipped suite. No real runtime is claimed to have been zero: this demonstrates a fail-open acceptance boundary.

### RC2 — blocking: scaling rows not bound to the expected problem/coverage (FC7 residual)

`summarize_pilot.R:284–295` uses the first row's `models_total/models_scored` to extrapolate full-run time. V13 at `:411` checks four thread/repetition pairs, positive wall/task/model counts and equal `models_scored`, but ignores dataset identity, expected total, fraction, n_tasks and consistent tasks_run.

Changing only the saved scaling CSV to (a) the wrong p20 dataset, (b) `models_total=1`, or (c) `tasks_run[1]=1` while others remain 31 gives **exit 0 / OVERALL PASS /259 valid** in every case. The wrong-total case produces full-run speedups around 10^-8 while still passing (`pilot_scaling_wrong_total/sum/pilot_scaling.csv`). See `pilot_new.csv` and the three saved case trees.

Validate the expected `dev_p0030_S4_r001` problem, full retained coverage, declared fraction/task split, consistent task/model counts and the fixed common subset across the four rows before extrapolating. Check every row's identity/coverage fields, not just the first row's total. Missing/wrong evidence must not yield PASS or an accepted sizing table.

### RC3 — should-fix: shared EXACT validator accepts contradictory scientific fields

`enum/exact_contract.R:118–128` validates the two size-vector log-sum-exp totals independently and the first top **score**, but not the corresponding per-size identity or HPM **support**. With a genuine fresh p20 CLI record, re-signing each separate mutation yields shared-validator `ok=TRUE` and scoring `ok=TRUE`:

1. Reverse only `size_logjoint`: `max(abs(size_logjoint - log_Z - size_logmass)) = 46.4146788905`.
2. Set HPM to `{1}` while the first top model remains `{3}`: scoring extracts `{1}` as the exact HPM.
3. Set `log_Z = hpm_F - 10`, updating size_logjoint and relative logZ consistently: impossible evidence below one contained model's mass is accepted.

`exact_consistency.csv`, `exact_consistency/` and `consistency_probes.R` retain the genuine control and mutations. The pilot also accepts the first two mutations with 259/259 valid (`pilot_exact_mass_joint_permutation`, `pilot_exact_HPM_top_disagreement`). Its fabricated baseline itself has logZ around -100 but best model score -90 and repeated top-model masks, so it tests structure rather than a coherent exact posterior.

Add tolerance-aware per-k size-mass identities, HPM/top support-mask-size agreement, basic evidence lower bounds and relative-logZ consistency. Keep a genuinely coherent empty-model control instead of changing HPM alone while leaving a different top model. This is additional validation work; no actual arithmetic error in the fresh enum output was demonstrated.

### RC4 — should-fix: valid empty SMC HPM is still rejected

`summarize_pilot.R:171` uses `!length(f$hpm)` to reject a native SMC result. `pilot_smc_empty_valid_HPM` changes a completed, estimates-available record to `hpm=integer(0)` with finite logZ; the summary exits 2 / FAIL solely for “bad: log_Z or hpm”. I1–I4's general support convention allows the empty model. Distinguish present empty support from absent/malformed support, validate original-index bounds, and retain the valid null-model fit for timing. The original enum-empty FC5 probe is fixed; this remaining SMC boundary is separate.

### RC5 — minor documentation (FC9 residual)

Remove JOB line 11's absolute no-home-cache claim and the stale RUN_DESIGN instruction in LOCAL_TEST, or label the latter explicitly as historical revision-3 text superseded by revision 4. No numerical change is needed.

## Final component verdicts

| Component | Verdict | Basis / remaining condition |
|---|---|---|
| **(a) Enumerator** | **ACCEPT WITH FIXES** | FC1/FC2 closed; t10–t12 and independent producer probes pass. No fresh producer/arithmetic regression demonstrated. RC3 remains in the shared validator before it can support the stronger internal-consistency claim. |
| **(c) Benchmark adapters** | **ACCEPT** | FC3 closed by shipped suite and independent saved-fixture replay; restricted diagnostics retained. This round does not claim another full real-fit benchmark smoke. |
| **(d) Scoring** | **ACCEPT WITH FIXES** | FC4 closed; 187/187 assertions, no skips. RC3 still allows contradictory exact references through readiness and into the headline inputs. |
| **(e) Pilot bundle** | **REJECT** | Original FC5 acceptance cases and FC6/FC8 repairs confirmed, but RC1/RC2 still admit unusable sizing evidence as PASS. Repair those release blockers; also address RC3/RC4 and FC9 wording before fresh confirmation. |

**Explicit OPS decision: NO-GO for handing off this version as an approved pilot bundle to stage/submit.** The review may be circulated through HQ to coordinate corrections. After those corrections are independently confirmed, OPS still fills MODULES/MODULES_BENCH, verifies actual D7 limits/footprint and guard receipts, uses the configured NOTS alias, and executes the real Linux mode-000, regeneration, scorer/enum identity, pinned-library, Slurm dependency/cancellation and final-accounting gates. Those platform gates do not replace the local acceptance-logic repairs identified here.

**Compact summary:** all 398 shipped checks passed; FC1–FC6/FC8 FIXED, FC7 PARTIAL, FC9 PARTIAL/minor. Independent probes expose remaining false-PASS timing/scaling evidence plus shared EXACT consistency and SMC-empty-support gaps. Enumerator/scoring ACCEPT WITH FIXES; benchmarks ACCEPT; pilot REJECT; OPS NO-GO. All 122 snapshotted source/dependency files stayed unchanged.
