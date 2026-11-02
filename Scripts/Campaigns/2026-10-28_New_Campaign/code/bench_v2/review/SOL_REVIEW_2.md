# Sol review 2 — BENCH-FIX (last full round)

Independent review by Sol 6.1, 2026-10-30. Local only, no SSH/NOTS, no delegation, no deliverable edits. All scripts, copied sources, generated fixtures, corruptions and logs are under [sol_scripts_r2/](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/). This is the final full review under D53/D48/D54: remaining class **(i)** findings require a fix and a **narrow check**, not another full round; class **(ii)** safe-halting cases below are documented and accepted.

The numerical code and revised test controls are accepted. **The shared bundle validator still accepts a changed primary scientific result and false seed records. Both bundles remain blocked for OPS launch.** These are independently constructed counterexamples; no erroneous fit was found in the inspected original saved records.

## Per-deliverable verdicts

| Deliverable | Verdict | Meaning |
|---|---|---|
| (a) [code/bench_v2](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2) | **ACCEPT** | R1-2 fixed; frozen implementation unchanged and the prior numerical acceptance stands. Downstream consumer/table release gates remain as disclosed. |
| (b) [code/bench_lowp](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_lowp) | **ACCEPT** | r2 acceptance stands; all 34 frozen members reverify. D54's OLS-sensitivity exclusion and F5 exact-check deferral stand. |
| (c) [BENCH_F3_DEV](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_DEV) | **REJECT** | Fix the three remaining class-(i) acceptance-gate findings below, then perform their narrow checks. |
| (d) [BENCH_F3_PROD](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD) | **REJECT** | Same shared-validator findings. Subsequently requires an inspected NOTS DEV pilot and pilot-derived resources before PROD submission. |

## Status of round-1 findings

| Finding | Class / severity from round 1 | Status | Independent ruling |
|---|---|---|---|
| R1-1 | (i), BLOCKING | **PARTLY** | Real positive passes; all ten original corruptions fail; substantial provenance/coefficient/KKT checks now work. Seed binding, null-branch contract and rule-selection semantics remain incomplete: R2-1/2/3. |
| R1-2 | (i), SHOULD-FIX | **RESOLVED** | Actual functions are mutated and restored. The same positive assertions detect rank, RSS, key-order and selected-second-stage-KKT faults. |
| R1-3 | (ii), SHOULD-FIX | **RESOLVED** | Runner manifest is included at prepare time; repeated path-mapped staging preserves upload bytes; exact membership remains enforced; upload receipt authority is explicit and a local transport round trip passes. |
| R1-4 | (i), MINOR | **RESOLVED** | Retry flush/fsync precedes sbatch; accepted-ID append flush/fsync follows it; client-error intent retention is tested. |
| R1-5 | (ii), MINOR | **RESOLVED** | Current-state sections identify freezes, local compatibility, actual test scope and open consumer gates. Historical text is preserved. The old PROGRESS table is superseded by its newest dated log; that residual presentation issue is accepted as class (ii). |

## Remaining class-(i) findings and exact fixes

### R2-1 — (i), SHOULD-FIX: result seeds are not bound to the manifest

**Evidence:** [validate.R:42](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:42) compares *input* metadata/seeds to the manifest. [validate.R:46](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:46) binds result hashes, but no equivalent comparison binds result seeds. [validate.R:55](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:55) only checks that the RDS case and CSV agree with each other. The expected-unit list at [validate.R:161](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:161) excludes seeds.

**Verified counterexample:** for each of `data_seed`, `fold_seed` and `method_seed`, increment its value in all six CSV/RDS rows and the RDS case, leaving the input and manifest unchanged. Write new RDS/CSV hashes. **All three complete saved records are accepted by `validate_prefix`.** See `EXTRA ... ACCEPTED` in [check_validator.log](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_validator.log); the retained examples are in [corruptions](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/corruptions). This can publish a false scientific provenance record even though its consumed-input hash is correct.

**Exact fix:** before either the whole-failure return or successful-fit checks, require each seed to exist and agree in (1) the manifest row, (2) consumed input, (3) every result row and (4) `x$case`. Compare values, not just agreement among result copies. Give each mismatch a seed-specific error. Keep input-file/hash checks intact and leave frozen code untouched.

**Narrow acceptance check:** the unchanged real positive and whole-failure positive pass; each of the three self-consistent rehashed seed corruptions fails specifically on manifest/result seed binding.

### R2-2 — (i), SHOULD-FIX: the null branch accepts records outside AUDIT §3's contract

**Evidence:** [validate.R:103](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:103) checks zero penalized vectors, the null code, held-out zeros and empty weights. It does not check null lambda/index sentinels or the path/candidate contents. [validate.R:118](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:118) skips selected-index checks when `keep` is empty; [validate.R:139](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:139) checks RSS only for EBIC rows. The required null contract is [AUDIT.md:158](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/AUDIT.md:158); the frozen producer implements it at [fit_F3_alasso.R:87](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/F3_AdaptiveLasso/methods/fit_F3_alasso.R:87).

**Verified counterexamples:** starting with the genuine saved null fixture, each separately rehashed record is accepted:
- Replace all rule/coefficient lambda/index NA sentinels by 1, changing both coefficient copies and the rule copies consistently.
- Replace the null path with a seven-row `data.frame(bogus=1:7)`.
- Replace the candidate table with the same meaningless table.
- Change only the primary CV row's RSS to 123456 in all row copies.

See the four `NULL_CONTRACT_CORRUPTION ... ACCEPTED` entries in [check_branches.log](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_branches.log). The original null fixture itself satisfies the complete contract.

**Exact fix:** add a null-specific contract check in the bundle wrapper. Require empty support/k=0, zero p-vectors and predictions, RSS=sum(y²) on **all six rows**, NA rule/coefficient lambda/index, the declared one-row null path with its NA sentinels, and exactly the valid null candidate with independently recomputed RSS/full-p EBIC values. Preserve the existing status/condition, pilot, copy-equality and hash checks.

**Narrow acceptance check:** genuine null/singleton/whole-failure positives still pass; the four saved null corruptions above fail for their specific sentinel/path/candidate/RSS reasons.

### R2-3 — (i), BLOCKING: valid KKT coefficients can be attributed to the wrong selection rule

**Evidence:** [validate.R:119](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:119) verifies that a row references a path entry, then [validate.R:127](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:127) verifies KKT at that entry. It never establishes that the entry is the CV minimum/one-SE choice. The OLS checks at [validate.R:129](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:129) likewise do not recompute EBIC scores or require the EBIC minimizer/first passing occurrence. The frozen selection semantics are [fit_F3_alasso.R:145](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/F3_AdaptiveLasso/methods/fit_F3_alasso.R:145) and [fit_F3_alasso.R:148](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/F3_AdaptiveLasso/methods/fit_F3_alasso.R:148).

**Verified primary-result counterexample:** on the actual saved p500/S1/c100 runner record, the CV minimum is index **200**, k=**64**; one-SE is index **169**, k=**51**. Replace the cv_min row's scientific fields and coefficients with cv_1se's, retaining the cv_min ID/primary role and updating all row/coefficient copies and `fit$beta`. Leave the saved CV path untouched and rehash the files. **The complete file validator accepts the changed 51-variable primary support.** See [check_selection.R](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_selection.R) and [check_selection.log](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_selection.log); the saved counterexample is [corruptions/cv_min_replaced_by_cv_1se](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/corruptions/cv_min_replaced_by_cv_1se).

Separately, setting ebic1's `crit_value=123456` consistently in CSV, RDS rows and fit rules is accepted ([check_validator.log](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_validator.log), `EXTRA EBIC_criterion ACCEPTED`). A correct coefficient vector and OLS RSS do not certify its criterion or rule attribution.

**Exact fix:** retain selected-point KKT and add rule-selection/score consistency:
1. Compute both CV choices using the frozen `cv_choose` on the saved second-stage CV path. Require the corresponding row indices/lambdas and CV mean/SE, and bind `diagnostics$index` to those choices.
2. Recompute the null plus distinct mapped-support candidate table from the consumed X/y, using full p, frozen OLS rank/RSS gates and gamma values. Check the saved candidates, row RSS/`ebic1_value`/`crit_value`, the cap100/K37 eligible sets and deterministic `order(crit,k,key)` minimizers.
3. Require each EBIC coefficient index to be the first/largest-lambda passing occurrence of its chosen support, with the documented failure behavior. Check the declared weighted lambda grid from X/y, pilot weights and frozen grid settings when interpreting its indices.
Do this in the bundle wrapper, without changing frozen fitting/validator sources or refitting the campaign.

**Narrow acceptance check:** original real and three branch positives pass; the rehashed primary-support substitution and criterion alteration fail specifically on rule selection/score checks. Add one wrong-EBIC-pick and one later-occurrence control. No new full numerical suite or campaign run is required.

## Accepted class-(ii) operator edge cases

### R2-4 — (ii), MINOR, ACCEPTED: a zero-duration whole-fit failure is refused

[validate_outputs.R:130](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/F3_AdaptiveLasso/tests/validate_outputs.R:130) requires one positive runtime; [validate.R:150](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:150) retains that gate. The original instantaneous failure record is therefore refused with exactly `runtime_s not one positive value per fit`. I reproduced that refusal.

**Ruling:** acceptable class (ii). The record is retained, validation exits nonzero, and OPS must inspect the failure anyway. Do **not** change the frozen validator, inflate a production runtime, or insert production delays. The 50-ms delay is disclosed test scaffolding only. A whole-fit failure with positive measured runtime is accepted as a recorded failed fit, with failed statuses and NA evidence preserved.

**Exact operator treatment:** retain/quarantine the four files and logs, record the zero-runtime validator refusal, and escalate for inspection under the JOB's failed/missing-unit policy; do not count it as an accepted result or silently omit it. This review documents and accepts that behavior. An optional JOB sentence pointing to this rule is sufficient; no wrapper exception is required.

The stale PROGRESS table is also **(ii), MINOR, ACCEPTED**: [PROGRESS.md:15](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/PROGRESS.md:15) still labels completed phases RUNNING, while the newest dated log records completion and this review. Optional exact documentation repair: label the table an historical snapshot and point to the latest log. It does not override the current manifest or current-state sections and is not a launch blocker.

## Independent verification and scope

**Original ten corruptions.** I copied the exact mutation operations from my round-1 `check_saved.R` final block into [check_validator.R](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_validator.R), supplied the new required context, and tested both object validation and rehashed saved-file validation. All ten fail. The unchanged actual six-rule runner record passes.

| Original corruption | Observed object rejection / saved-file rejection |
|---|---|
| Missing EBIC OLS vector | bad coefficient evidence / same, with copy mismatch |
| Impossible coefficient index | coefficient metadata mismatch / same |
| k=999 | coefficient metadata mismatch / support/k inconsistency |
| Missing pilot diagnostics | pilot/screen diagnostics missing / same |
| Retired kappa_edge | outside vocabulary / same |
| Wrong primary role | roles differ / registry/primary-role mismatch |
| Zeroed input hash | manifest_inputs_sha256 / CSV_RDS_inputs_sha256 |
| Doubled one coefficient copy | coefficient copies differ / same |
| Wrong CSV criterion | CSV_RDS_crit_value / same |
| Infinite failed-rule audit vector | penalized support mismatch / same, plus failed-row violations |

For the all-zero hash, CSV inference gives an earlier type/equality rejection in the saved-file path. I separately changed **all corresponding result copies** to a nonnumeric 64-character hash: input/X/y/fold hashes each fail at their intended `manifest_*sha256` check ([check_binding_types.log](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_binding_types.log)). This isolates actual manifest binding from that CSV inference effect.

Further independent rehashed controls reject altered OLS slopes in both copies (`OLS_beta_ebic1`), altered penalized coefficients in both copies (`selected_KKT_cv_min`), non-NA CV OLS evidence, wrong EBIC RSS, altered pilot keep and altered weights. Scale, scenario and replicate alterations are refused; input bytes are hashed against the manifest and X/y/fold components are independently rehashed. **Seed/result binding remains the explicit exception R2-1.** No claim is made that selected-point KKT alone verifies rule selection.

**Branch authenticity and normalization.** I executed the shipped generator's frozen-runner setup into review-local directories, including the disclosed local glmnet 4.1-10 adapter and separate delayed-failure harness. The regenerated fit objects (excluding measured runtime), coefficient evidence and case metadata are **identical** to the supplied null, singleton and delayed-failure fixtures. These are runner-written records, not fabricated list fixtures. The three original positives and all six supplied object/saved-file corruptions pass their expected tests. Independently checked the complete original null output contract, the singleton soft-threshold full-data coefficients and every fold denominator/CV mean/SE/both choices, and whole-failure NA vectors/statuses.

CSV infers all-NA k as logical. Without normalization the frozen payload check reports six coefficient-metadata mismatches; the bundle's value-preserving logical-NA → integer-NA normalization removes those six and produces no new values. [validate.R:20](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/validate.R:20) is narrowly scoped and acceptable. The zero-runtime record still fails only its runtime gate.

**R1-2 controls and 72/72 claim.** I inspected the full saved 72/72 log/exit and reran **69/69 non-child checks** independently ([run_core.log](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/run_core.log)). Rank removal ([run_all_tests.R:67](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/tests/run_all_tests.R:67)), actual key-order reversal (:78), invalid-RSS finite scoring (:97), and selected-second-stage KKT bypass (:210; at p20/30/120) mutate executable functions, rerun the same positive guard, and restore originals. Their observed failures are the intended assertions. The prior five implementation controls and deployed-ridge canary remain. The three child legacy checks were not independently rerun because their shipped output destinations are outside review; the inspected 72/72 worker log includes them.

**Shared wiring.** [task.sh:21](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/task.sh:21), [retry.py:113](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/retry.py:113) and [reconcile.py:90](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/reconcile.py:90) all invoke the same wrapper with explicit expected unit/input/manifest/frozen-code arguments. The Python real-reconciliation test invokes the actual R validator on the real case; it passes. Expected full campaign membership is not replaced by that test's intentionally one-case mapping.

**Stage, download and durability.** Production Python tests **19/19**, DEV tests **2/2** passed with all temporary directories redirected under review ([check_python.log](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_python.log)). Additional [check_stage.py](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_stage.py) executed prepare on the actual freeze for both kinds, then the stage shell flow twice and upload verification; each unmodified upload retains exactly **34 manifested members plus UPLOAD_SHA256.txt**. Only review-local path guards/destinations/interpreter were mapped; the remote disk guard was stubbed, and all original frozen/hash/membership logic ran. Extra upload and installed-code members are refused. The actual OPS receiver processed a locally supplied manifest/tar transport and wrote a **VERIFIED 35/35** upload receipt; the downloaded upload also passes its original digest. A real-result archival manifest survives copy/verify and refuses an extra file. No actual transfer or NOTS preflight was performed.

Retry source at [retry.py:51](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/retry.py:51) flushes/fsyncs its exclusive claim; :139 calls it before sbatch :146; :157–160 flush/fsync the accepted ID. Scheduler mocks independently passed submission ordering, accepted-ID sync, and retained intent after a failed sbatch client with duplicate refusal. The exact-membership and terminal-state rules were not weakened.

**Integrity.** High-p freeze remains **8905f52e314f706b54f985994d7915052301c9e22912690264b7b27ab58b0373**, **23/23** members; low-p r2 **85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7**, **34/34**. F3 runner source hash is **3e01c77b27ad96ad8ec4761b6b25ea5511d357e8aa08a1db7b2972e71734f42c**. Final bundle ledgers verify **PROD 63/63**, digest **b81e300990ebefb5ed210f7103740b26511c6be8947e20d539658073549766e7**; **DEV 27/27**, digest **c87f25d7fbd05d80e3f41e8e5ae48377b1514ff27941e80a6a0dd1f7b099129f**. Archived pre-freeze ledgers remain historical. After narrow fixes, regenerate current bundle ledgers and actual deployment upload manifests; preserve reviewed/historical snapshots. The final integrity check confirms **82/82 snapshotted reviewed files unchanged**, plus both complete code freezes.

Costs now consistently distinguish 75–90 physical / 150–180 billed PROD core-hours and <2 physical / <4 billed DEV forecasts from DEV's 32.5 physical / 65 billed requested-wall ceiling. Those are forecasts, not NOTS measurements.

## Commands, evidence and limits

All commands used absolute paths, one shell command per call; no directory changes, recursive shell deletions or SSH. R/Python workload concurrency stayed at **at most two** (Python parent plus one child in integration tests). All checks completed in under about 15 minutes individually; the longest independent batch here was the Python suite, about 65 seconds for production tests. R used the specified R 4.4.1 executable and one numerical thread. Session/package details, timestamps, script exit files, source snapshots and retained counterexamples are in the evidence directory.

Reproduce with the absolute [run_r.ps1](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/run_r.ps1) wrapper and `-Name check_validator`, `run_core`, `check_branches`, `check_selection`, or `check_binding_types`; Python uses [run_python.ps1](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/run_python.ps1) and `-Name check_python`, `check_stage`, or `final_integrity`. Fixture/stage generators intentionally refuse existing destinations: use fresh review-local output paths for a rerun. Logs are the inspected results, not proposed commands.

Review-script corrections: an initial low-p manifest-path lookup was corrected; an initial read-helper encoding error was corrected; the first local stage adapter stopped on Git Bash's remote-path conversion, then was corrected with path-conversion disabled and Windows-normalized test destinations. That failed adapter attempt is retained as [check_stage_attempt1.log](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_stage_attempt1.log); the completed [check_stage.log](<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/check_stage.log) exits zero. None of these is a deliverable defect or a claimed successful first attempt. R startup locale warnings were retained.

Not checked this round: actual NOTS stage/task/environment/module gates, ownership/quota/library binaries, scheduler acceptance/accounting or crash durability on NOTS storage, real network transfer/deletion, full 26/2,400-unit reconciliation, remote pilot resource measurements, or 2,400 fitted production units. No complete expensive legacy-suite rerun, new broad low-p campaign, or final scoring/analysis/table tie-out. Prior numerical/source review remains valid because the freezes reverify.

**OPS disposition:** after fixes and narrow checks for R2-1/2/3, proceed **DEV first**. Inspect actual terminal DEV outputs, failures, timing, memory, accounting and all four sizing cells. Only then fill production resources from that accepted NOTS pilot and consider PROD launch. This review neither authorizes submission nor waives the documented downstream release checks.

