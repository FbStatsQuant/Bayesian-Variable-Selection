# LOWP final confirmation 3 — independent Sol 6.1 review

**OPS handoff: NO-GO for this pilot bundle.** RC1, RC2, RC4 and RC5 are repaired. The three original RC3 mutations are now rejected, but the broader internal-consistency claim and the claimed coherent fabricated posterior remain only partly repaired. A new blocking sizing defect accepts zero RSS as valid evidence and publishes accepted production memory requests of **0 MB**.

Reviewer: Sol 6.1, independently, no subagents. Review date: 2026-10-29 UTC. Local Windows execution expressly authorized for this review; no SSH/NOTS. Evidence root **E**:

`<PC_TEMP_PATH>`

## Scope, preservation and execution

Read the named context, FINAL_CONFIRM2 findings, allowed earlier evidence, current enum/pilot/scoring sources and tests, and the authorized core dependency. Snapshotted 120 source/context/dependency files; the original reviewed files were not edited. Before/after SHA-256 comparison: **120/120 unchanged**, as recorded in `source_integrity.txt` and `report_identity.json`. Only this requested new review is delivered to CAMP.

All compilation, fixtures, mutations, reports and test writes ran in E. The scratch copies of enum t10/t11/t12/helpers replace only their hard-coded CAMP prefix with the scratch snapshot; assertions and production implementation bytes are unchanged. Scoring used the copied core and the expressly authorized external `bench_smoke_reviewfix_v6/results/smoke` records. Its generated report is in `E/snapshot/code/scoring/tests/TEST_REPORT.md`.

R: `C:/Program Files/R/R-4.4.1/bin/Rscript.exe`; the temporary `lowp_Rlib` was prepended, retaining the default user library and R's default library. `.libPaths()` and `sessionInfo()` are saved in `rc_probes.log`. BLAS/MKL/OpenMP default to one thread; enum CLI tests explicitly use two. Independent probe seed 20261029; shipped fixture seed 7; shipped suite seeds remain in their source snapshots. No full p30 enumeration or real SMC/benchmark fit was launched. The additional scaling-producer check used only a 3% p20 subset at one and two threads.

The benchmark condition test is the current named `test_derived_conditions.R`, run with `common.R` and `config_lowp.R` from the expressly allowed **prior review snapshot**, copied into E. This preserves the read-only path restriction: current benchmark adapter sources beyond the named test were not read. Its result does not constitute a new audit of those current adapters.

Commands, executable/argument vectors, launcher PIDs, UTC timestamps, exit codes and logs are in `setup.ps1`, `run_suite.ps1`, `all_suites.ps1`, `retry_suites.ps1`, `*.status.json` and `*.log`; `execution_summary.csv` indexes the runs. An initial launcher sequencing error ran t10/t11 before snapshot preparation completed; both exited with Windows startup status -1073741819 and no test output. Those attempts are retained as `t10_setup_attempt.*` / `t11_setup_attempt.*`; both were subsequently rerun successfully. Locale and data.table build-version warnings are retained. No assertion or gate was bypassed.

`evidence_sha256.csv` hashes saved evidence, excluding disposable compile caches, R temporary directories, junction traversal and self-referential identity files. `report_identity.json` binds the delivered review and evidence index.

## Shipped suites

All seven suites exited 0. Assertion totals and saved reports were inspected; enum exit codes alone were not treated as proof.

| Suite | Result | Evidence relative to E |
|---|---|---|
| Enum t10_cli_completion.R | **36/36 PASS** | `t10.log`, concurrent child logs under `enum_suite/` |
| Enum t11_partial_and_validation.R | **32/32 PASS** | `t11.log` |
| Enum t12_exact_contract.R | **74/74 PASS** | `t12.log` |
| Scoring test_scoring.R, including G32 | **193/193 PASS; 0 skipped** | `scoring.log`, regenerated `snapshot/code/scoring/tests/TEST_REPORT.md` |
| Pilot run_negative_tests.R | **70/70 expected outcomes** | `negative.log`, `neg/NEGATIVE_TESTS.md` |
| Pilot test_shell.sh | **34/34 PASS** | `shell.log`, `shell/SHELL_TESTS.md` |
| Bench test_derived_conditions.R | **3/3 PASS**, with the helper-source qualification above | `bench.log`: no condition, warning-only, message-only |

Total: **442 successful checks/assertions/cases**. Additional syntax inspection: **22 pilot shell/sbatch files, zero syntax failures** (`shell_syntax.log`). Independent probes are additional to these totals.

All pilot performance values in these fixtures are fabricated logic-test data, not campaign measurements. Passing the suites does not cover the additional counterexamples below.

## RC dispositions

| Item | Disposition | Independent evidence |
|---|---|---|
| **RC1 — per-unit wall/CPU evidence** | **FIXED** | Re-created on the new baseline: one enum30 unit with missing wall/user/sys gives exit 3 / INCOMPLETE, 258/259 valid; all enum30 CPU absent gives 3 / INCOMPLETE, 253 valid; all six enum30 walls zero gives 2 / FAIL, 253 valid. Every resulting projection is NOT ACCEPTED. Baseline gives 0 / PASS, 259 valid and accepted projections. `rc_probes.csv`, `pilot_one_enum30_wall_cpu_missing/`, `pilot_all_enum30_CPU_missing/`, `pilot_enum30_zero_walls/`. The explicit enum-observed-CPU versus single-thread-allocated-wall policy is implemented and documented. |
| **RC2 — scaling identity/coverage** | **FIXED (original defect)** | Re-created wrong p20 dataset, total model count 1, and inconsistent first-row task count: each gives 2 / FAIL; all projection rows become NOT ACCEPTED. Source checks every row against dev_p0030_S4_r001, 2^30 total models, fraction .03, 1024 tasks, 31 run and consistent scored count, and requires a shared subset hash. The actual producer on a modest p20 input emits 1024/31/31744 with 2^20 total and the same real 64-hex digest at one and two threads. `rc_probes.csv`, per-case summaries, `scaling_producer.csv`, `scaling_producer_probe.log`. Additional malformed-evidence hardening is N3. |
| **RC3 — internally contradictory EXACT fields** | **PARTIAL** | **All three original mutations are fixed:** on a fresh genuine p20 t12 CLI record, reversed joint size masses, HPM/top disagreement, and logZ below HPM mass with both related logZ fields updated are rejected by both shared validator and scoring loader. Control passes both. The pilot rejects the same three re-signed mutations on its new baseline, each exit 2 / FAIL, 258 valid. Shipped G32 also excludes each mutated reference from scoring tables. However impossible PIPs still pass validator/scoring readiness, and the rebuilt pilot fixture is not a coherent posterior; see N2. `exact_consistency.csv`, `consistency_probes.log`, `rc_probes.csv`, G32 report, `coherence.csv`, `impossible_PIP.csv`. |
| **RC4 — empty SMC HPM** | **FIXED** | A completed, estimates-available primary SMC fit changed to `integer(0)` remains valid: exit 0 / PASS, 259 valid, timing retained. Removing the field instead gives 2 / FAIL, 258 valid. The baseline's existing null-model control also passes. Shipped negatives cover malformed/non-integer, out-of-range, zero and unsorted support, and a null-model repeat. `pilot_smc_empty_valid_HPM/`, `pilot_smc_absent_HPM/`, `rc_probes.csv`. |
| **RC5 — documentation** | **FIXED** | JOB revision 5 explicitly permits only the small pilot-owned core cache in home; its absolute no-home-cache claim is gone. LOCAL_TEST labels the stale RUN_DESIGN edit request historical and superseded. Current RUN_DESIGN already states the subsets. |

## Remaining findings

### N1 — BLOCKING: zero memory evidence produces accepted 0 MB requests

`pilot/summarize_pilot.R:254–258` selects GNU RSS whenever it is finite, so **zero** overrides even a positive accounting fallback. V11 at lines 434–436 requires only a finite arm/p maximum. Projection lines 460–466 and 473 round this to 0 and label it accepted.

Independent reproduction: copy the fresh baseline and set only `maxrss_kb = 0` in its timing TSV. Results in `E/pilot_all_memory_zero/sum/`:

- exit **0**, **OVERALL PASS**, **259/259 valid**;
- memory verdict PASS, source `gnu_time`;
- all eight production pieces have `suggested_mem_request_mb = 0` and `status = accepted`;
- positive batch accounting and SMC core memory figures are available but ignored.

An R fitting process has a nonzero memory footprint. This is unusable sizing evidence accepted as complete, directly analogous to the repaired zero-wall boundary. The ordinary baseline's enum30 request is 512 MB; the zero-only mutation changes it to 0 without any rejection. No real campaign RSS is claimed to have been zero.

Require finite **positive** memory evidence before using a source; use an explicitly labelled positive fallback when appropriate. If no usable source remains, reject as missing/invalid evidence and mark projections NOT ACCEPTED. Never publish an accepted nonpositive memory request. Add zero/negative RSS and unusable-fallback cases to the shipped tests. This defect alone prevents approved OPS handoff.

### N2 — should-fix: PIP consistency and the coherent-fixture claim

Every posterior satisfies `sum(PIP_j) = sum(k * P(|S|=k))`. Also a variable's PIP cannot exceed its posterior share among the listed models plus **all** unlisted posterior mass.

For the first fabricated enum20 baseline record, c100: summed PIPs **6.4654642590**, expected size **2.3516838624**, discrepancy **4.1137803967**. The unlisted probability is only **0.0000687913**, yet one PIP exceeds its listed share plus that entire tail by **0.3756498798**. c050 also fails (summed PIPs 6.9643962331 versus expected size 2.2142546970). Therefore no joint distribution over supports can have these stored fields. The cause is the independent `share + runif(p)*0.4` construction in `tests/make_fabricated_pilot.R:56`. Distinct top masks, coherent HPM/top support, logZ bounds and per-size log identities repair earlier structural defects but do not make the full posterior coherent.

This is not only a fixture wording issue: re-sign a genuine current p20 producer record after setting c100 PIPs to one and MPM to all 20 variables. Both `lowp_validate_exact` and `load_exact_checked` return TRUE, although expected model size remains **4.3447773215**. Saved under `exact_consistency/impossible_PIP/`; `additional_checks.log`, `impossible_PIP.csv`. The untouched genuine control agrees in the size/PIP identity to about 5e-14 (`coherence.csv`). No fresh producer arithmetic error was found.

Build the synthetic posterior's size masses and PIPs from one realizable support distribution (including its unlisted remainder), retaining the empty-model control. Add tolerance-aware size/PIP moment and listed-mass feasibility checks to the shared validator, with scoring regressions. At minimum remove the unsupported assertion that the current fixture is a coherent exact posterior. `coherence.csv` also records null-model likelihood/joint fields for inspection; those two quantities differ by a model-prior term and are **not** asserted equal here.

### N3 — minor: malformed scaling evidence handling

All four `tasks_sha256` values set to the identical string `not-a-sha256` still give exit 0 / PASS, 259 valid and accepted projections (`pilot_scaling_placeholder_hash/`). Require a 64-hex digest in addition to equality. A dataset value of NA instead crashes `scaling_check` at line 305 with exit 1, leaving no verdict/projection/Markdown report (`pilot_scaling_dataset_NA.log`). This fails closed but misses the promised FAIL/INCOMPLETE summary. Validate types/missingness before comparisons and handle malformed values explicitly. The shipped producer emits a proper digest; neither case reproduces the repaired wrong-dataset/count false PASS.

## Safety and sizing inspection

The reviewed default paths place staged code/inputs/study copies and the small core cache under the pilot-owned New_Campaign home `runs/<PID>`, results/logs/enum caches under New_Campaign scratch, and per-job temporary files under its scratch TMPDIR. No bundle script opens SSH. The benchmark library is read only; cleanup targets exclude shared trees and the frozen benchmark locations.

Submission checks D7 with the OPS-owned guard before creating launch output or calling sbatch: parses the 0.5/9.6 GiB ceilings, refuses test overrides, checks the real planned addition and refusal probes, and preserves a receipt. Every sbatch result is checked; failure cancels only explicitly recorded IDs. The current allowed guard source carries the D7 constants. It was not executed against NOTS here.

Truth separation is enforced across the whole fitting wave in the submitted dependency graph: regeneration → truth permission test → verified wave lock; every fitting step additionally requires the successful build and all these gates; unlock is afterany of lock plus all six fitting steps and rechecks fitting-job activity before restoration. Recovery refuses scheduler failure/active jobs. The build precedes the lock but is compilation, not fitting. Windows cannot establish actual Linux mode-000 isolation; real Slurm cancellation/dependency and Linux permission tests remain mandatory OPS gates.

Cleanup canonicalizes both New_Campaign roots and exact three removal targets; refuses linked `runs`/targets, missing ownership/IDs, remaining scratch results/logs, scheduler errors and active pilot jobs before deletion. Its verified result additionally requires residue search and guard success. The shipped shell tests exercise the junction, ownership, shared-tree and refusal boundaries. No real campaign deletion or truth chmod was performed in this review.

One narrow path qualification: `submit_pilot.sh:38` creates the temporary guard receipt with bare `mktemp` **before** setting a private scratch TMPDIR; without an OPS-supplied TMPDIR this can be in system `/tmp`. It is removed and its durable copy is on campaign scratch. Thus the absolute claim that every transient write is under New_Campaign is not self-enforced at submission. Set a campaign-owned scratch temporary location for this receipt; all job-side `mktemp` calls inherit `pilot_init`'s scratch TMPDIR. This is a small transient-file boundary issue, not a shared-tree deletion finding.

The ordinary baseline's production arithmetic ties out independently: enum30 allocated core-hours = `600 * mean(process wall) * 16 / 3600`; benchmark p20 mean case wall is the sum of the eight method means; enum30 memory rounding gives 512 MB (`sizing_tieout.csv`). Counts, sampled subsets, shared-machine/rare-escalation caveats and NOT ACCEPTED labelling are clear. The new N1 acceptance boundary remains a blocker even though the ordinary arithmetic is correct. These checks do not establish real NOTS performance.

## Final component verdicts

| Component | Verdict | Basis |
|---|---|---|
| **(a) Enumerator** | **ACCEPT WITH FIXES** | t10–t12 pass; the three original RC3 mutations are closed; no fresh producer arithmetic regression. N2 remains in the shared validator's stronger internal-consistency claim and fixtures. |
| **(d) Scoring** | **ACCEPT WITH FIXES** | 193/193, no skips; G32 excludes the original RC3 defects end to end; independent genuine-record replay agrees. N2 still admits an impossible PIP reference through readiness. |
| **(e) Pilot bundle** | **REJECT** | RC1/RC2/RC4/RC5 repaired, but N1 publishes accepted zero-memory sizing. RC3/fixture consistency is partial, with minor N3 and temporary-receipt qualifications. |

**Explicit OPS decision: NO-GO for handing this version to OPS as an approved stage/submit pilot bundle.** Correct N1 and re-confirm it; address N2's claimed scientific consistency and record the remaining minor handling fixes. This review may be circulated through HQ to coordinate those changes. Even after local approval, OPS must fill MODULES/MODULES_BENCH, verify actual guard limits/footprint under D7, and run the real Linux mode-000, regeneration, compiler/scorer identity, pinned-library, Slurm dependency/cancellation/recovery and terminal-accounting gates. No permission to stage or submit is implied by this local review.

**Compact summary:** RC1/RC2/RC4/RC5 FIXED; RC3 PARTIAL (all three original probes now reject). Enumerator/scoring ACCEPT WITH FIXES; pilot REJECT; OPS NO-GO because zero RSS still yields accepted 0 MB production requests. Execution evidence and unchanged-source hashes are saved in E.
