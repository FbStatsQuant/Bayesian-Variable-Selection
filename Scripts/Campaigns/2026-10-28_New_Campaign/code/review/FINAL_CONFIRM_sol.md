# LOWP final confirmation - Sol 6.1

**Pilot verdict: REJECT. The revised pilot bundle may NOT go to OPS for submission yet.** The shipped suites pass (31 shell cases, 26 R negative cases), and most earlier defects are repaired. Independent additional probes still find acceptance/contract gaps and a cleanup path-boundary defect. Component verdicts are at the end.

Reviewer: independent Sol 6.1; performed directly, no subagents. Reviewed 2026-10-28 America/Chicago / executed 2026-10-29 UTC. Reviewed files were not edited. This report is the only campaign file written.

## Evidence and execution limits

`E = <PC_TEMP_PATH>`.

- `source_before.csv`, `source_after.csv`, `source_integrity.txt`, `snapshot/`: **125 tracked reviewed files, zero changed entries**; snapshots match the pre-review hashes. Includes the named pilot, enum, generator/tests, scoring, benchmark common/runner/README, contracts and OPS facts/guard.
- `shell/SHELL_TESTS.md`, `shell.log`, `shell.status.json`: **31/31**, exit 0. Actual interval 03:39:19-03:41:42 UTC. Stub Slurm, disposable roots only.
- `neg/NEGATIVE_TESTS.md`, `negative_default.log`, `negative_default.status.json`: **26/26**, exit 0, 03:42:36-03:45:34 UTC. Fabricated records, not scientific runs.
- `ab_probes.R/.log/.status.json`, `ab_observations.rds`, `enum_*.log`, `enum_study/`, `enum_out/`: current CLI resume/contract probes, fresh small input and saved results. Exit 0. Full p20 only; no full p30 enumeration.
- `cd_probes.R/.log/.status.json`, `cd_observations.rds`, `registry.csv`, `edge_probes.rds`, `derived_condition_probe.csv`, `restricted_candidate_probe.csv`, `scoring_exact/`, `dup1/`, `dup2/`: replayed benchmark edge fixture and independent G26-G31-equivalent boundary checks. Exit 0.
- `extra_abc.R/.log/.status.json`, `additional_ab_c.rds`, `enum_drop_cli.log`, `message_only_probe.csv`: direct C++ negative-margin rejection, constant-column CLI regression, message-only derived-rule condition. Driver exit 0; the deliberately failing CLI exits 1.
- `pilot_extra.R/.log/.status.json`, `pilot_additional.csv`, `pilot_additional_observations.rds`, `pilot_more.R/.log/.status.json`, `pilot_more_observations.rds`, `pilot_*/sum/`: additional complete-tree acceptance probes. Both drivers exit 0; individual summarizer exits are preserved. `byte_probe.R/.log`, `byte_comparison.rds` execute the actual byte comparator on signed zero/nonfinite values.
- `junction_probe.sh/.log`, `junction_case/`: cleanup dry run with a Windows directory junction whose target is outside the configured fake campaign root but still inside E. **No deletion was requested or performed.**
- `review_environment.json`, per-driver status JSONs, scripts, raw RDS/CSV, logs, source snapshots and `evidence_sha256.csv` retain commands, seeds, timestamps, PIDs, exits, environment and hashes.

R 4.4.1 and Git Bash 5.2.37 on local Windows, expressly authorized; BLAS/MKL one thread, enum two threads. The enumerator used the permitted earlier review's saved preprocessing/scorer-header snapshot in `E/core_snapshot/`, checked against current vendored headers; no unlisted current core source was opened. Thus this is current enum/CLI validation against that preserved core contract, not certification of the current deployed core build. Synthetic seed 20261029; shipped fabricated fixture seed 7.

The initial launcher replaced `R_LIBS_USER`, hiding the default user library. Those failed setup attempts are retained. After Felipe's clarification, the successful runs **preserved default libraries and prepended lowp_Rlib**; `digest 0.6.39` resolved normally (`library_check.log`). No package was installed. This was a reviewer setup issue, not a shipped-suite finding. `cd_probes_attempt1.log` retains a reviewer fixture error (an unintended duplicate seed); the corrected final driver completed. Startup locale warnings and the data.table build-version warning remain in logs.

No SSH/NOTS/Owls connection, full p30 enumeration, real benchmark fitting, current SMC adapter execution, or real staging was performed. Real Linux mode-000 behavior, Slurm cancellation/dependencies/accounting, modules, R 4.5.2 pinned deployment and Sapphire Rapids costs remain pilot gates for OPS. The current SMC path expressly named in this brief is its README; current writer internals outside that allowlist were not opened. Cross-checks use that README, the prior permitted schema/evidence and producer-shaped envelopes. The full scoring suite was not run unchanged: it loads unlisted current core dependencies, reads an unlisted smoke tree, and writes reports beside reviewed files. Its G26-G31 source was inspected, and the relevant boundaries were independently rerun in E instead.

## 1. RECHECK_ab residuals

| Item | Disposition | Evidence / qualification |
|---|---|---|
| Enumerator N1: resume validates the full contract | **PARTIAL** | Current-source fingerprint, exact requested scale set, required field names, scale exact/full labels, heuristic labels and normalized size masses are checked. Earlier one-scale-to-two-scale probe now recomputes; stale source, missing label, partial scale and old joint-valued size masses each recompute successfully. However a test-mode record is silently reused after a sealed manifest is added, retaining `input_mode=unsealed_test`; re-signed, internally self-consistent wrong dimensions/counts also skip. See FC1 and `ab_probes.log` / `enum_02_seal.log`, `enum_09_contract.log`. |
| Enumerator N2: top-level models_expected / complete | **FIXED** | Fresh writer gives `models_expected=1048576`, `complete=TRUE` at top level, retaining extra copies; matches I2. `ab_observations.rds`; CLI lines 154-161. |
| a4: margin >= 0 | **FIXED** | Negative margin rejects in public R and direct compiled `cpp_td`; messages explicitly require finite >=0. `ab_probes.log`, `extra_abc.log`; guards in both current R/C++. |
| Generator b3: n / kind / scales required | **FIXED** | Clean generated p20 control has no problems. Deleting each separately produces schema and metadata problems. `LOWP_INPUT_REQUIRED` and unconditional comparisons enforce all three. `ab_probes.log`, `ab_observations.rds`. |
| N3: retain Linux truth-lock evidence | **FIXED** | `test_truth_lock_linux.sh` retains complete R logs, pre/post file hashes, modes, run.log, script SHA and final_status.txt. Cleanup of tmp is optional; pilot explicitly sends evidence to scratch and downloads it. Static confirmation only; real Linux execution remains for the pilot. |

Additional enum regression: the API correctly completes a 19-retained-column problem from a p20 input containing one constant column, scoring 524288 models; the CLI then refuses its own freshly committed record because it derives coverage from original p=20 instead of retained p=19 (FC2).

## 2. RECHECK_c manager fixes

| Item | Disposition | Evidence / qualification |
|---|---|---|
| N1: successful derived row with captured conditions | **PARTIAL** | Original warning reproducer now yields `warning`, retaining count 1 and warning text. But replaying the same fixture with only a captured message, all original rules failed and `n_warnings=0`, yields successful `ebic1_lam005` with `status=ok`, `messages='captured message'`. The runner itself treats messages as warning-status conditions. FC3; `cd_probes.log`, `message_only_probe.csv`. |
| N2: restricted k_valid_max / ebic_at_largest | **FIXED** | Replayed three-point fixture selects size 1, reports `k_valid_max=1` and `ebic_at_largest`, retaining full-path metadata. `restricted_candidate_probe.csv`; `common.R:75-77`. |
| N3: LA-4 provenance | **FIXED** | Current runner assigns F1-F4 `LA-1;LA-4`, F5 `LA-1;LA-2;LA-4` after derivation for every output row, including failure rows. `run_bench_case.R:167-174`. Confirmed by source inspection; no new real benchmark smoke is claimed. |

## 3. RECHECK_d residuals

| Item | Disposition | Evidence / qualification |
|---|---|---|
| N1: registry derived from bench_lowp | **FIXED** | `R/registry.R` sources benchmark config and calls actual `lowp_derive`; default pipeline uses `build_registry`, and `make_registry.R` exposes the audit CSV. Independent check gives 42 required rows / 12 H4 rows; F4/F5 primary `ebic1_K37`, caps secondary. Deliberately different primary/cap supports give F4 1/1 and F5 0/1 using K37. Conflicting observed roles reject. `registry.csv`, `cd_probes.log`; G26 source inspected. |
| N2: genuine exact-branch evidence | **FIXED** | Producer-shaped native exact record with finite logZ and no islands retains `ok/evidence_ok=TRUE`, logZ=-90; `islands_ok=FALSE`, plain unavailable. Current extraction explicitly distinguishes exact from completed SMC. `cd_observations.rds`; G27 inspected. |
| N3: full-vector indexing and exact probabilities | **FIXED** | Reversed full-vector names reorder to identical canonical PIPs; duplicate/unknown names and nonzero confirmed dropped entries reject. Exact PIPs 1.8, NaN, Inf, -0.2 reject. `cd_probes.log`; G28 inspected. |
| Finding 6: duplicate identity / unique main key | **FIXED** | Actual scanner merges identical benchmark copies and rejects copies differing only in diag_flag; diag_codes is also in the compared RULE_COLS. Direct main-table duplicate rejects. `cd_observations.rds`, `dup1/`, `dup2/`; G29 inspected. |
| Finding 10: EXACT readiness | **PARTIAL** | Missing top/extra completeness, partial scale and unequal supplied counts now reject; clean control passes. But missing both counts, equal zero counts, and an absent c050 scale still return `ok=TRUE`. Counts are optional and not checked against design coverage. FC4; `scoring_exact/`, `cd_probes.log`; G30 misses these cases. |
| Finding 11: known distinct repeat seeds | **FIXED** | Two unknown seeds give `n_unknown_seed=2`, `n_completed=n_evidence=0`, SD/agreement NA. Duplicate known seed rejects. `cd_probes.log`; G31 inspected. |

## 4. All 15 REVIEW_pilot_bundle findings

| # | Earlier finding | Disposition | Evidence / remaining work |
|---|---|---|---|
| 1 | Swallowed sbatch failure | **FIXED** | First/middle rejection and bad parsable id abort with exit 5; no subsequent submissions; exact previously submitted IDs cancelled and abort receipt saved. Shell suite. |
| 2 | Truth readable during fitting wave | **FIXED** | Test after verify, wave lock after test, all six fit steps afterok build+verify+test+lock; unlock afterany lock+all fits, collection afterward. Recovery refuses active jobs/scheduler failure. Graph and recovery tests pass; real Linux/Slurm behavior remains untested here. |
| 3 | Cleanup fails open on scheduler errors | **FIXED** | squeue failure ->4, active id ->3, missing ID record ->3, retained results ->3; final guard refusal ->UNVERIFIED exit1. Canonical-path boundary is a separate remaining part of #10 (FC6). |
| 4 | Summary misses failed/incomplete units | **PARTIAL** | All original adversarial cases now reject with 2/3: timing rc2, missing sidecars/markers, failed repeats, absent benchmark arm. Expected 259-unit set and 67 jobs/tasks checked. However a marker stating `status failed,failed` is accepted; missing scaling evidence is accepted; other semantic gaps remain. FC5/FC7. |
| 5 | Outdated guard ceilings | **FIXED** | Named OPS guard now sets 524288 KB campaign and 10066329 KB home. `guard_check.sh` refuses old limits, test overrides and insufficient room; receipts saved. Logs/results/evidence go to scratch. Real quota probe not run locally. |
| 6 | Missing enum evidence defaults to success | **PARTIAL** | Models=1, wrong p30 K/count, zero rechecks, hash tampering all reject. But top-level complete/count fields and source fields are not required, per-scale status/scope remain optional, and size masses need only length/finiteness, not normalization. Re-signed `complete=FALSE, models_expected=1` and nonnormalized masses each retain OVERALL PASS /259 valid. Shipped baseline itself lacks I2 top completeness/counts and uses `scope=all_models`. FC5. |
| 7 | sacct memory fallback not used | **FIXED** | Missing GNU RSS + batch MaxRSS -> accepted with finite requests and `sacct_job_bound`; neither source ->INCOMPLETE. Independent rerun of shipped negative cases. |
| 8 | Collector cannot prove own terminal state | **FIXED** | Collector snapshots predecessors, OPS final_accounting captures all; summary requires final snapshot and expected IDs/tasks with COMPLETED/0:0. Missing final snapshot ->3; failed task ->2. Final script's success alone is not acceptance; the summary checks coverage. |
| 9 | Byte vs numerical equality mixed | **FIXED** | Actual byte comparator distinguishes +0/-0 (1 byte-value mismatch, numerical difference 0) and flags nonfinite values. T1 scores/eta and T2/T3 use bytes; aggregates use declared tolerances; decisions/thread invariance exact. `byte_probe.log`, current `pilot_bitid.R`. Full bitid workload not rerun. |
| 10 | Cleanup/staging ownership | **PARTIAL** | Fresh versioned `runs/<PID>` replaces shared-tree deletion; shared trees survive shell test. But canonical target is compared only with its canonical immediate parent, which does not bound a linked ancestor to the campaign root. Scratch junction dry run accepts an outside-root target (FC6). |
| 11 | Test hooks / unpinned dev library | **PARTIAL** | Normal driver/jobs refuse hooks, launch records save them; test_library TRUE/outside obvious library path reject. Yet version/R provenance is not checked, and startsWith accepts sibling `R452_UNAPPROVED/glmnet`. Both independent probes give PASS/259. Frozen library is only read by bundle code; no chmod/move/write into it found. FC8. |
| 12 | Fixture suite not self-contained | **FIXED** | Both shipped suites run from the named bundle alone once normal default R libraries are preserved. No external record templates. Its enum semantics still need FC5 fixes; passing fabricated logic tests is not scientific validation. |
| 13 | Final OPS configuration not retained | **FIXED** | Final pilot.env+SHA, staged file list, owner, JOB, lists, exact sbatch vectors, effective environment and guard receipt copied to scratch launch receipt. JOB specifies durable local archive+SHA. Shell suite checks receipt; missing launch receipt ->3. Real staging was not run outside the allowed source scope. |
| 14 | Stale login node | **FIXED** | JOB uses only configured `ssh nots` alias, pinned loginx2, one connection at a time; agrees with current charter/OPS facts. Scripts open no SSH. |
| 15 | Sample coverage overstated | **FIXED** | RUN_DESIGN section4 now says 30 p20 +6 p30 enum,24 SMC + 4 repeats,24 x 8 benchmarks; regeneration all 1200+60 is distinct. Lists and summary agree. JOB/LOCAL_TEST still say RUN_DESIGN needs this edit although it is already done (minor FC9). |

Amended charter check: campaign home cap 0.5 GiB, total home <9.6 GiB are reflected in code; default slurm/unit/report/truth-test/accounting logs are on scratch. Small core compile cache remains in the owned home code tree with a stated allowance; enum cache/TMPDIR are scratch. The staged study COPY's truth trees remain locked throughout the fitting dependency wave, with restoration/recovery explicit. The frozen benchmark library is passed read-only and no direct mutations to either frozen tree were found. Actual footprints and effective read-only deployment remain OPS checks, not laptop measurements established here.

## 5. Cross-component consistency

| Contract / consumer | Disposition | Result |
|---|---|---|
| I1 generator / input validation | **PARTIAL (minor documentation)** | n/kind/scales and five Y columns agree, primary fits use c100/c050. Truth actually also includes required dataset_id; I1's displayed truth list omits it. Dev layout/IDs and truth-free fit study in pilot agree. |
| I2 enum producer / resume / scoring / pilot | **PARTIAL** | Writer now has documented top completeness fields, statuses, posterior/joint size masses and source fingerprint. Resume, scoring readiness and pilot summary enforce different subsets; FC1/FC2/FC4/FC5 show concrete consequences. Empty support is valid in enum/scoring but pilot rejects empty HPM. |
| I3 SMC envelopes / pilot invocation / scoring extraction | **PARTIAL (verification limit)** | Named CLI README, pilot --case/scale/development/repeat/allocation flags, output filenames and +4e6/+1000 seeds agree. Current extractor maps producer-shaped exact/RB/plain records correctly in targeted tests. Current writer internals were not within the expressly named paths; no new end-to-end SMC writer certification is claimed. |
| I4 benchmark producer / registry / pilot | **PARTIAL** | Paths/rules/LA-4/roles and scoring registry agree. Benchmark runtime is in record$rows$runtime_s/CSV, whereas pilot reads top-level record$runtime_s: all16 method-by-p in-process medians are NA even on accepted baseline. FC7. |
| I5 scoring artifacts | **FIXED / consistent** | Current pipeline emits the named case/headline tables, plus registry_used.csv and diagnostic/stability outputs; primary K37 rows enter H4 and cap rows remain stored outside H4. |
| RUN_DESIGN / pilot bundle | **FIXED, with minor text drift** | Counts, per-arm subsets, fitting allocation, Sapphire Rapids, separate thread-scaling runs, scratch logs/results, wave-wide truth lock and post-pilot sizing order agree. Pilot benchmark request6G/2h is deliberately measured before production4G/4h is sized; no requirement that these requests coincide. JOB's stale instruction to amend RUN_DESIGN and its “no caches in home” statement conflict with already amended text / documented small home core cache (FC9). |

## Findings still requiring action

| ID | Severity | Location and demonstrated issue | Required correction |
|---|---|---|---|
| FC1 | **Should-fix** | `enum/run_enum_dataset.R:89-110`: resume contract gaps. After unsealed-test output, adding valid manifest yields exit0/skip with old unsealed provenance. Re-signed p=K=1/counts2 record on unchanged p20 input also skips. | Bind resume to requested input_mode/manifest verification and manifest identity; validate n/p/retained map/K/dimensions against input/design, and both completeness copies. Preserve current source/scale checks. |
| FC2 | **Should-fix (new regression)** | Same CLI:101 vs writer:151. Constant p20 input drops to19; API complete524288; CLI post-commit check derives1048575 from rawp20,K19 and exits1 without done. | Derive coverage from retained dimension, consistently with the API; validate original-p metadata separately. Add dropped-column CLI test. |
| FC3 | **Should-fix** | `bench_lowp/R/common.R:67-68`: message-only provenance still hidden when original rows failed; successful restricted rule says ok while retaining message. | Detect captured messages as well as warnings/counts, independently of original failure status; retain failure precedence and test both condition types. |
| FC4 | **Should-fix** | `scoring/R/extract_exact.R:33-38`: complete flags true but missing counts, counts0/0 or missing requested scale are ready. | Require finite valid coverage fields, derive expected count from retained p/K, reject0 coverage, require each requested scale/status/full contract. Extend G30. |
| FC5 | **Blocking for pilot acceptance** | `pilot/summarize_pilot.R:110-160`: false PASS for contradictory .done status, topcompleteFALSE, absent scale status/scope, nonnormalized size mass. Shipped fixture also omits required current I2 fields. Empty legitimate HPM instead gets FAIL. | Share a strict current EXACT contract validator with producers/consumers; require all documented readiness metadata and normalized masses, allow integer(0) support, and compare .done statuses with CSV/RDS. Repair baseline fixtures before adding these negative cases. |
| FC6 | **Should-fix, high cleanup risk** | `pilot/cleanup_pilot.sh:26-32`: comparing canon(target) with canon(parent)/basename permits linked ancestor escape. `junction_probe.log` shows outside fake campaign target accepted by dry run, exit0. | Canonicalize allowed campaign/runs roots and prove each resolved target is the intended descendant; reject linked intermediate directories or compare against canon(campaign_root)/runs/exactPID. Apply before recursive removal; add ancestor-link refusal test. No deletion was executed here. |
| FC7 | **Should-fix** | `pilot/summarize_pilot.R:245,279-290,350-356`: all benchmark in-process times NA because writer has rows$runtime_s; missing scaling_subset.csv still PASS; missing enum30 wall/CPU measurements silently accepted with fallback runtime. | Read and cross-check per-fit row runtime; require/validate expected four subset measurement rows and saved scaling file. State and gate any allowed timing fallback; do not label missing required measurements complete. |
| FC8 | **Should-fix** | `pilot/summarize_pilot.R:201-211`: prefix check accepts pinned-root sibling R452_UNAPPROVED; supplied version/sessionInfo evidence (R4.4.1/glmnet0.0) is ignored, giving PASS. Dev runner intentionally relaxes library-location checks. | Require exact normalized package-library parent equality (or prefix plus separator), validate required package/version/build provenance and effective R4.5.2 from the saved environment, including dev pilot. Main package pins are already checked by the runner; post-run provenance must support the broader sealed-deployment claim. |
| FC9 | **Minor** | I1 omits truth dataset_id; JOB/LOCAL_TEST still ask for already-completed RUN_DESIGN edit; JOB says no home caches while build intentionally uses small home .cpp_cache. | Align displayed contracts and wording with actual approved layout. No numerical change required. |

These are controlled boundary/metadata probes, not evidence of corruption in any real campaign output. FC2 is an actual fresh-producer failure on a supported preprocessing case. FC3 is a reproducible condition-status boundary. FC6 demonstrates the path-check logic with a disposable Windows junction; real Linux execution was not attempted, but the comparison has the same ancestor-link flaw. No scientific accuracy or timing conclusion is inferred from fabricated pilot records.

## Final component verdicts

| Component | Verdict | Release condition |
|---|---|---|
| (a) Enumerator | **ACCEPT WITH FIXES** | FC1/FC2; N2 and nonnegative-margin repairs confirmed. No new scorer arithmetic defect demonstrated. |
| (b) Spec + generator | **ACCEPT** | Requested residuals fixed; minor I1 wording in FC9. Existing platform/regeneration gates remain mandatory. |
| (c) Benchmark adapters | **ACCEPT WITH FIXES** | FC3 message-only status; restricted diagnostics and LA-4 provenance repaired. |
| (d) Scoring | **ACCEPT WITH FIXES** | FC4 exact-readiness coverage; registry, exact-branch evidence, PIP mapping/probabilities, duplicate handling and unknown-seed repairs confirmed. |
| (e) Pilot bundle | **REJECT** | FC5 blocks acceptance; also repair FC6-FC8 and align with fixed producer contracts before a fresh independent confirmation. |

**OPS handoff: NO for submission.** HQ may circulate this review and the revised bundle to coordinate fixes; this is not approval to stage/submit the pilot. Once code is corrected and independently confirmed, OPS still supplies modules, checks the actual archive/cache budget and guard receipt, and executes the real platform gates.

**Compact summary:** 31 shell and 26 R negative tests passed; 125 tracked reviewed files stayed unchanged. Most earlier repairs are confirmed, but enum resume/drop-column handling, message-only benchmark status, exact-readiness validation and pilot acceptance/cleanup/provenance still need fixes. Generator ACCEPT; enum/bench/scoring ACCEPT WITH FIXES; pilot REJECT; no OPS submission approval.

