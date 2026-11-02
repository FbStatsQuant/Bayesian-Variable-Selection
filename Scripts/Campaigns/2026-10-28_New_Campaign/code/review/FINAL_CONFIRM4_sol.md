# LOWP final confirmation 4 — independent Sol 6.1 review

**OPS handoff: GO.** Independent review performed by Sol 6.1, without subagents. Local Windows execution was expressly authorized; no SSH/NOTS connection or remote job was used. Review date: 2026-10-29 UTC.

Evidence root **E**: `<PC_TEMP_PATH>`.

## Preservation and execution

Reviewed the named context, the preceding FINAL_CONFIRM3 and FINAL_CONFIRM2 evidence, current enum/scoring/pilot sources and tests, the named benchmark condition test, and the authorized core dependency. Source/context/dependency snapshots and original SHA-256 values are in `source_before.csv` and `snapshot/`. Before/after SHA-256 comparison: **119/119 unchanged**, recorded in `source_integrity.txt`. Reviewed files were not edited; only this requested new review is delivered to CAMP.

The comparison with FINAL_CONFIRM3 (`changed_since_confirm3.csv`) isolates the substantive changes to the shared validator, pilot summarizer/fixture/submission receipt, their tests and documentation. The enumerator producer, scoring loader, cleanup and truth-wave implementations are unchanged from that reviewed baseline.

All compilation and test writes occurred under E. Only the scratch copies of enum t10/t11/t12/helpers replace their hard-coded CAMP prefix with the scratch snapshot prefix; production implementation bytes are unchanged. Scoring uses the copied core and the explicitly authorized `bench_smoke_reviewfix_v6/results/smoke` records. Its regenerated report is `snapshot/code/scoring/tests/TEST_REPORT.md`.

R: `C:/Program Files/R/R-4.4.1/bin/Rscript.exe`. The temporary `lowp_Rlib` was prepended while retaining the ordinary user library and R's default library; actual `.libPaths()` and `sessionInfo()` are saved in `rc_probes.log`. OpenMP/BLAS/MKL defaults were one thread; shipped enum tests explicitly request two. Independent probe seed: 20261029; shipped fabricated fixture seed: 7 (per-record seeds are also in its source). No full p30 enumeration, real SMC fit or new benchmark fitting smoke was run.

The benchmark condition test uses its **current named test file** with `common.R` and `config_lowp.R` copied from the expressly permitted FINAL_CONFIRM3 evidence. This respects the read restriction on current benchmark adapter sources. Its result does not constitute a fresh audit of those current adapters.

`setup.ps1`, `run_suite.ps1`, `all_suites.ps1`, saved probe scripts, `*.status.json`, `*.log` and `execution_summary.csv` preserve invocations, executable/argument vectors, launcher PIDs, timestamps, exit statuses and inspected outputs. The shell suite ran in Git Bash with `MSYS_NO_PATHCONV` **unset**. Locale and data.table build-version warnings are retained. Two failed starts of the independent receipt launcher, caused by a reviewer path-string error, are retained as `receipt_launcher_attempt*.status.json`; neither invoked the test. The corrected receipt probe exited 0. No assertion or acceptance gate was bypassed.

`evidence_sha256.csv` indexes saved evidence, excluding disposable compile caches, Rtmp directories, junction traversal and self-referential identity files. `report_identity.json` binds that index to the delivered report.

## Shipped suites

All seven suites exited 0. Printed assertion totals and generated reports were inspected; exit status alone was not used as evidence.

| Suite | Result | Evidence relative to E |
|---|---|---|
| Enum t10_cli_completion.R | **36/36 PASS** | `t10.log`, `enum_suite/` child logs |
| Enum t11_partial_and_validation.R | **32/32 PASS** | `t11.log` |
| Enum t12_exact_contract.R | **79/79 PASS** | `t12.log` |
| Scoring test_scoring.R, including G33 | **195/195 PASS; 0 skipped** | `scoring.log`, regenerated `snapshot/code/scoring/tests/TEST_REPORT.md` |
| Pilot run_negative_tests.R | **82/82 expected outcomes** | `negative.log`, `neg/NEGATIVE_TESTS.md` |
| Pilot test_shell.sh | **35/35 PASS; junction tests ran** | `shell.log`, `shell/SHELL_TESTS.md` |
| Bench test_derived_conditions.R | **3/3 PASS**, with the helper-source qualification above | `bench.log` |

Total: **462 successful shipped checks/assertions/cases**. Independent probes are additional. All 11 required suite/probe processes exited 0; `execution_summary.csv` also retains the two unsuccessful receipt-launcher attempts.

All pilot cost values in these fixtures are fabricated logic-test data. They establish acceptance behavior, not actual campaign performance.

## Final-confirmation findings

| Item | Disposition | Independently reproduced result on the current baseline |
|---|---|---|
| **N1 — nonpositive memory** | **FIXED** | GNU RSS zero or negative with positive accounting fallbacks: exit 0 / PASS, 259 valid; every production memory request is positive, minimum 512 MB, with explicit `sacct_job_bound (GNU RSS unusable)` labels. With GNU, batch and SMC core measurements all unusable: exit 3 / INCOMPLETE, 0 valid, no accepted projections, no accepted nonpositive request. SMC GNU RSS zero and batch zero with positive core VmHWM: exit 0 / PASS, 259 valid; SMC rows use `core_vmhwm (GNU/sacct RSS unusable)`. |
| **N2 — PIP consistency and fabricated posterior** | **FIXED for the identified defects** | Fresh genuine p20 control passes validator/scoring. Re-signed all-one PIPs with consistent MPM reject through both. A second mutation preserves the PIP sum but moves probability between variables beyond listed-mass feasibility; both reject it too. On the fresh fabricated pilot, both mutations give exit 2 / FAIL, 258 valid, with NOT ACCEPTED projections. All 39 fabricated EXACT records / 78 scales pass the current validator; maximum independent size/PIP moment error is 1.7764e-14, with zero listed-mass feasibility excess, retaining the empty-HPM control. |
| **N3 — placeholder digest and NA dataset** | **FIXED** | Identical `not-a-sha256` in every scaling row and a single NA dataset value each give exit 2 / FAIL with the complete Markdown/verdict/projection outputs and all projections NOT ACCEPTED. Neither produces an unhandled crash or false PASS. |
| **Temporary guard receipt path** | **FIXED** | An independent wrapper around actual `mktemp` observes `SCR/runs/<PID>_tmp/guard_receipt.XXXXXX`, despite a poisoned caller TMPDIR. All 12 mocked submissions succeed; the temporary receipt is removed, the caller directory remains empty, and the durable scratch launch receipt retains `GUARD_CHECK_OK`. |

**N1 evidence:** `rc_probes.csv`, `memory_and_reports.csv`, `pilot_all_memory_zero/`, `pilot_memory_negative_positive_fallback/`, `pilot_memory_zero_no_positive_fallback/`, `pilot_memory_negative_no_positive_fallback/`, `pilot_smc_core_fallback/`. Each case retains `sum/pilot_units.csv`, verdicts, projections and Markdown. Memory now requires finite positive evidence **per unit**, before validation/sizing; precedence is GNU time, batch-step conservative bound, then SMC core VmHWM. The request calculation also requires a positive maximum. Missing one enum30 GNU measurement with a positive fallback remains accepted, as intended.

**N2 evidence:** `exact_consistency.csv`, `consistency_probes.log`, re-signed records under `exact_consistency/`, `fixture_coherence.csv`, `pilot_exact_impossible_PIP/`, `pilot_exact_moment_preserving_impossible_PIP/`, plus the regenerated G33 scoring report. On the genuine record, all-one PIPs imply expected size 20 while the stored size distribution has expectation 4.3447773; both moment and feasibility failures are reported. The unchanged-sum mutation is rejected specifically by the lower/upper listed-share constraints. G33 additionally verifies exclusion end to end: no ready exact reference, no evidence error for that dataset, EXACT selection rows `not_run`, and reduced evidence denominator.

The fixture construction was inspected: distinct listed supports, disjoint explicit remainder supports scoring below the listed minimum, and common weights used to derive log Z, size masses, PIPs and MPM. For its first c100 record, sum(PIP) = 2.35165166727683 versus expected size 2.35165166727684. This repairs the earlier independent-random-PIP construction. These are probability-fixture consistency checks; passing them does not certify the accuracy of a scientific posterior.

**N3 evidence:** `pilot_scaling_placeholder_hash/`, `pilot_scaling_dataset_NA/`, their logs, `rc_probes.csv`, `memory_and_reports.csv`. The shared scaling check validates finite numeric values/missingness, exact problem and coverage, four thread/repetition rows, common lowercase 64-hex digest and positive walls; malformed comparisons are handled as a reportable failure. Shipped negatives additionally cover text in numeric fields, NA wall and uppercase digest.

**Receipt evidence:** `receipt_probe.sh`, `receipt.log`, `receipt/stub/mktemp_trace.txt`, `receipt/SHELL_TESTS.md`, `receipt/submit_independent.log` and its durable launch receipt. Local Git Bash represents the Windows temporary workspace with its `/tmp` mount; the observed file is beneath the exact **mock campaign SCR root**, not the caller/system temporary directory selected by inherited TMPDIR. Production configuration derives the same location from `/scratch/fb31/New_Campaign`.

## Earlier RC/FC items: no observed regression

| Items | Current evidence |
|---|---|
| **RC1 / FC7 wall and CPU evidence** | Missing one enum30 wall/user/sys: 3 / INCOMPLETE, 258 valid; all enum30 CPU absent: 3, 253 valid; all enum30 walls zero: 2 / FAIL, 253 valid. All projections NOT ACCEPTED. Baseline: 0 / PASS, 259 valid and accepted projections. `rc_probes.csv`. |
| **RC2 / FC7 scaling identity** | Wrong dataset, total models = 1, inconsistent first-row tasks: each 2 / FAIL; missing scaling CSV: 3 / INCOMPLETE. No accepted projections. `rc_probes.csv`. No new scaling-producer performance run was needed: its implementation hash is unchanged, and the actual small producer check is preserved in FINAL_CONFIRM3 evidence. |
| **RC3 cross-field identities** | Reversed joint size masses, HPM/top support disagreement, log Z below HPM with related fields updated: all reject in validator and scoring on a fresh genuine record and in the current pilot (2 / FAIL, 258 valid). `exact_consistency.csv`, `rc_probes.csv`. Together with N2 this closes the previously identified RC3 residuals. |
| **RC4 null SMC HPM** | Present `integer(0)` remains valid (0 / PASS, 259 valid); absent field rejects (2 / FAIL, 258 valid). `rc_probes.csv`; shipped tests also cover malformed/out-of-range/unsorted values and null repeats. |
| **RC5 / FC9 documentation** | JOB revision 6 identifies the small pilot-owned home core cache and scratch enumerator cache. LOCAL_TEST marks the stale RUN_DESIGN edit request historical and superseded. The requested fixes and OPS responsibilities are explicit. |
| **FC1 / FC2 producer resume and retained coverage** | Current t10/t12 re-exercise stale/old-contract/partial records, changed manifest and sealed mode, false completeness, requested scale changes, and constant-column input: CLI/API score 2^19, retain original p20 with K19, publish consistent sidecars/marker, then verify and skip. |
| **FC4 / FC5 completeness and statuses** | Independent genuine-record loader rejects absent/equal-zero counts, absent scale, false completeness and partial scale. Current pilot rejects false completeness and unnormalized masses (2 / FAIL); separate re-created SMC done-status contradiction also rejects (2 / FAIL, 258 valid). `exact_consistency.csv`, `rc_probes.csv`, `fc_regression.csv`. |
| **FC6 cleanup boundary / scheduler handling** | Current shipped shell tests exercise ancestor/target junctions, missing ownership/IDs, scheduler failure/active jobs, residual results/logs, exact targets, shared-tree preservation and verified cleanup. No junction case was skipped. Cleanup implementation bytes are unchanged from FINAL_CONFIRM3. |
| **FC7 / FC8 benchmark runtime and environment** | Independent re-signed runtime disagreement, sibling `R452_UNAPPROVED` package path and wrong authoritative R session each give 2 / FAIL, 258 valid. `fc_regression.csv`. Shipped tests cover additional version/build/provenance and CSV/status defects. |
| **FC3 derived benchmark conditions** | Current named three-case suite checks no condition, warning-only and message-only statuses, restricted support and diagnostics, using the explicitly qualified prior-review helpers above. |

Independent production arithmetic still ties out: enum30 allocated core-hours = `600 * mean(wall) * 16 / 3600`; benchmark p20 wall per case is the sum of all eight method means; enum30 memory request = `512 * ceiling(1.5 * max(RSS_MB) / 512)` = 512 MB. `sizing_tieout.csv`: all three pass.

## Component verdicts and OPS handoff

| Component | Verdict | Basis |
|---|---|---|
| **(a) Enumerator** | **ACCEPT** | t10–t12 pass; current genuine outputs remain valid; the identified RC3/N2 consistency defects now reject, including a same-moment PIP counterexample. |
| **(d) Scoring** | **ACCEPT** | 195/195, no skips; independent loader rejection and G33 end-to-end exclusion confirmed. |
| **(e) Pilot bundle** | **ACCEPT for OPS handoff** | N1/N2/N3 and receipt path fixed; 82/82 negative cases and 35/35 shell cases; prior RC/FC controls show no observed regression. |

**Explicit decision: GO for handing this pilot bundle through HQ to OPS.** No unresolved local blocker was found in this scope. OPS completes the environment configuration and real-platform gates below before relying on a real pilot for production sizing.

The reviewed dependency graph gates all six fitting steps on successful build, regeneration, Linux truth-lock test and verified wave lock; unlock waits for the lock and fitting steps and checks scheduler state. Submission failures cancel only recorded explicit IDs. Cleanup canonicalizes campaign roots and the three exact pilot-owned targets, refuses linked intermediates/targets and uninspectable/active jobs, and requires residue/guard checks before claiming verified removal. These static and mocked checks support the local bundle review.

OPS still fills `MODULES` / `MODULES_BENCH`, verifies the actual D7 limits and planned footprint/guard receipt (0.5 GiB campaign home, total home under 9.6 GiB), and executes the real Linux mode-000, regeneration, compiler/scorer identity, pinned-library, Slurm dependency/cancellation/recovery and terminal-accounting gates. Those untested platform gates are mandatory at execution and are not, by themselves, a local handoff blocker. This review does not claim that any of them ran on NOTS.

**Compact summary:** N1 FIXED; N2 FIXED for the identified validator/fixture defects; N3 FIXED; receipt path FIXED. Enumerator ACCEPT; scoring ACCEPT; pilot ACCEPT for OPS handoff. **OPS GO**, with real-platform execution gates retained. All 462 shipped checks pass; all 119 reviewed files unchanged.
