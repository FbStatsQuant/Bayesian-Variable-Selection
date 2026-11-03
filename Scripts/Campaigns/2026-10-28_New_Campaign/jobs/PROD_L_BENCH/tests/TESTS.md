# PROD_L_BENCH acceptance tests (black box, from jobs/PROD_L_BENCH/DESIGN.md; adapted from the PROD_L suites)

Run all: `bash <B2>/tests/run_all.sh <PC_TEMP_PATH>` (sequential; per-suite `.log` / `.rc` and `SUMMARY.txt`). One suite: `bash test_X.sh WORKDIR` / `py -3 -I test_X.py WORKDIR`.
Work dirs only under `<PC_TEMP_PATH>`. Each suite ends with `<suite>: N passed, M failed`. Only `test_accept.sh` starts R (one process at a time; cap 8).
`PRODL_B_SRC=<folder>` points the staging helpers at another bundle folder. PROD_L's own tests are untouched.

Assumptions where DESIGN.md is silent (change them here and in the suite if the manager rules otherwise):
- Staged layout: scripts run from `HOME_ROOT/runs/<STAMP>_lowp_bench/code/prod_l_bench/` (bundle without tests/, review/, BUILD_NOTES.md, PROGRESS.md); fixture OWNER `lowp_bench <STAMP> staged ...`; study = manifest + 1,200 dummy inputs, NO truth; frozen tree `code/bench_lowp` + `code/bench_lowp.SHA256SUMS`.
- Same stubs, `ceiling_check.py --plan` header `step cpus max_concurrent_tasks phase`, comma-separated `--own-ids`, ledger records single-space `key=value`, waiter sacct rows `JobID|State`, `batch_runner.sh` sourced after `pilot_init`.
- Main wave = 3 vectors (`lowpB_s0_verify` 1 CPU 2G 0:30; `lowpB_s1_bench` array `0-95%32` alone / `%16` withH, 1 CPU 1G 1:00:00, afterok verify; `lowpB_s9_collect` afterany). Later waves: `lowpB_s1_bench` / `lowpB_s2_benchretry` arrays (no verify, no dependency) + collect afterany the arrays.
- `make_resubmit.sh STAMP rN` (one call per round) writes `bench_rN.tsv`, `benchretry_rN.tsv`, `bench_rN_exceptions.tsv`; stale artefact refusal exit 5 (resubmit) / 2 (manifests); reconcile_bench.py `--home-root --scr-root --lists --out`, tables `<out>/inventory/bench.tsv` (`piece unit outcome detail`), `<out>/exceptions.tsv`, STATUS line in INVENTORY.md.
- A case's `cli_status` is `ok` for CLI rc 0 and `failed_rules` for rc 2 (rc 2 -> outcome `ok`, task exit 0); rc 1 -> `unit_failed`.

| id | what it checks | expected | DESIGN section |
|---|---|---|---|
| **test_lists.py** | | | |
| L01-L08 | LF, header, only piece `bench`, 2,400 unique units `<dataset>_<scale>`, repeat 0, 24 cells x 100 replicates, 96 tasks x 25 (one cell and one aligned block each), numbering identical to PROD-L's smc piece, generator present | exact | 2 |
| **test_ceiling.py** | | | |
| B01-B12, B20 | bench plan peaks 64 alone / 32 withH (receipt), plan caps 132 / 68, max over phases, `_prodH` refuses alone only, combined 192 (others <= 128 alone / 160 withH), PROD-L / BENCH_F3 jobs count as others, own ids ignored, array throttle with running tasks, unparsable row, stdin, receipt, billed(c) boundaries c=1..16 | as stated | 4 |
| **test_waiter.sh** | | | |
| WT00-WT49, UT01-UT20 | PROD-L waiter semantics with the prefix `lowpB_`: failure-like states exit 3 at once, all terminal 0, partial / unparsable accounting waits, ssh back-off, `--until-terminal` (0 / 4, never 3); WT11b-c: a PROD-L job is not ours, a queued lowpB_ job keeps waiting | as stated | 4 |
| **test_deadline.sh** | | | |
| DL00-DL06 | bench units, window open: exit 0, `.start`/`.end` fields, D = T0 + 3600... (hook), inventory, timing rows, start recorded before the unit runs | as stated | 3 |
| DL10-DL35 | window closed / boundary / deadline mid-task: deferral with reason=deadline | as stated | 3 |
| DL40-DL46 | budget kill: `killed_timeout` (rc 124/137), task exit 1, next unit still runs | as stated | 3 |
| DL50-DL54 | rc 3 -> `unit_failed`, exit 1 | as stated | 3 |
| DL60-DL68 | bench rc mapping: rc 2 -> outcome ok with `cli_status=failed_rules` (task exit 0, also in benchretry); rc 1 -> unit_failed; rc 0 -> ok | as stated | 3 |
| DL70-DL74d | SLURM_JOB_END_TIME bound; junk = absent (local test runs, production defers with reason no_scheduler_end_time, exit 1) | as stated | 3 |
| DL80-DL85 | benchretry (WALL 3600, BUDGET 1200, need 1380) starts at elapsed 2000 and defers at 2150; bench (budget 600, need 780) starts at 2650 and defers at 2750 | as stated | 3 |
| DL90-DL91, RQ00-RQ16 | second job tag adds files; same job/task id twice refuses (ledger + inventory byte-identical, evidence in LOG_RUN/refusals/<JOB_TAG>.txt); SLURM_RESTART_COUNT=1/2 -> exit 71 before any write | as stated | 3 |
| ES01-ES18 | end-time source (env / squeue %e / script time in local tests only), end_source/end_epoch recorded, production without a source defers | as stated | 3 |
| DL95 (x4) | PRODL_* hooks outside a local test refused (exit 70) | as stated | 3 |
| **test_driver.sh** | | | |
| D00-D04 (alone, withH) | main wave: exit 0; 3 submissions; vectors (names lowpB_s0_verify / s1_bench / s9_collect, account / partition / constraint, cpus, mem, time, `0-95%32` / `%16`, afterok verify, collect afterany, kill-on-invalid-dep, outputs %j / %A_%a, --no-requeue); no lock / unlock step; launch record (bench.env + sha256, STAGED list, OWNER, frozen manifest, lists, guard 75 MB / ceiling receipts, effective_env without SECRET_TOKEN_TEST, sbatch_args); jobids files | as stated | 4 |
| D10-D16 | dry run prints 3 vectors and creates nothing; `--local-test` with hooks accepted and recorded | as stated | 4 |
| D20-D29 | waves r1 / r2 / r3: bench list (2 tasks), bench + benchretry lists (3 submissions), benchretry only; JOBIDS appended; guard 5 MB; missing list refused | as stated | 4 |
| N01-N04 | 7 hooks without `--local-test`, env without flag, flag without env, no fake root: exit 2 | exit 2 | 4 |
| N10-N13 | any path component named truth / holdout (case-insensitive, dir or file, nested) under the run folder: exit 2, nothing created | exit 2 | 1, 4 |
| N20-N24 | a queued / running `lowpL_s1..s4_*` job refuses (exit 2); non-fitting PROD-L jobs do not; `--allow-concurrent-prodl` allows and is recorded; also for later waves | as stated | 4 |
| N30-N31 | guard refusal: exit 1 | exit 1 | 4 |
| N40-N45 | frozen bench_lowp file altered / unlisted file / manifest missing / staged file altered / staged list altered / launch/main exists | exit 2 | 4 |
| N50-N53 | later wave while a run job is active; squeue failing (main and later); CLOSED bench | refused, nothing submitted | 4 |
| N60-N65 | ceiling: `_prodH` alone; 200 + 60 + 32 > 192; 124 + 32 admitted; others 130 + 64 refused, 128 + 64 admitted; unparsable row | exit 2 / 0 | 4 |
| N70-N71 | sbatch fails at call 1 / 2 / 3, unparsable id | exit 5, earlier ids cancelled by explicit id, SUBMISSION_ABORTED.txt | 4 |
| **test_resubmit.sh** | | | |
| RS00-RS06 | gates: job RUNNING / PENDING array / squeue error / sacct RUNNING / missing id / sacct error | exit 3 / 3 / 4 / 3 / refused / 4 | 5 |
| RS10-RS22 | routing: never started -> bench; one start unit_failed or killed_external -> bench; one start killed_timeout -> benchretry; >= 2 starts or a benchretry attempt -> exceptions; case done only with 8 valid methods (7 of 8, bad sidecar, malformed CSV are not done; a committed failed rule stays done); chunks of 25 renumbered | exact lists | 5 |
| RS30-RS46 | SAME_LIST, changed state exit 2, new wave, NOTHING_TO_RESUBMIT, retry-only round, CLOSED piece exit 2 | as stated | 5 |
| ST01-ST18 | stale kinds (F1.lock dir; hidden temps `.F1.rds3a9c`, `.F3.csv5b21`, `.A2.done77aa`; incomplete method units F2.rds+F2.csv without .done, F5 without .done) refuse make_resubmit.sh (exit 5, names clear_stale.sh), also in a done case; clear_stale dry run lists, `--yes` moves (never deletes) all kinds, gates 3 / 4 | as stated | 5 |
| **test_manifests.sh** | | | |
| MM00-MM44 | gates 3 / 4; stale kinds exit 2 then clear_stale; one method missing / bad sidecar / empty rds / bad CSV / bad .done -> exit 6; `--allow-incomplete` closes; committed failed rules close; MANIFEST verifies and lists exactly the files; CLOSED / inventory / exceptions snapshot / summary, hash fields; second close 2; existing manifest revalidated (valid) or exit 2 (tampered); logs piece needs accounting + bench CLOSED | as stated | 6 |
| RC01-RC26 | reconcile_bench.py: CLEAN exit 0, exceptions.tsv header, inventory rows once, failed rule counted in the per-method rule-status table, unexpected output -> exit 1 / unexpected_output, malformed record -> malformed_record, partial case not done, ledger classes over bench + benchretry (deferred / unit_failed / killed_external / not_run) | as stated | 6 |
| X01-X09, N01-N07 (manifests) | closure refused while exceptions exist (6); `--allow-incomplete` -> exceptions snapshot -> move away -> reconcile exit 4 with acknowledged=yes and STATUS COMPLETE WITH 1 HQ-ACKNOWLEDGED EXCEPTIONS; tampered snapshot / inventory exit 2; rule-status table invariant across close and pull | as stated | 6 |
| **test_reconcile.py** | | | |
| SV01-SV05 | strict validation of one method per case: missing RDS with a sidecar for another file, one-line / duplicate / escaping / three-line sidecar, malformed .done, CSV without method_id / case_id, status outside the set, method_id or case_id mismatch, zero rows, empty RDS, tampered RDS, 3 of 8 methods -> not done; committed failed rule and a fully valid case -> done; exit 1, STATUS INCOMPLETE OR UNRESOLVED, malformed_record exception | as stated | 5 |
| EX01-EX06 | CLEAN; unexpected folder alone exits 1; not_run cases; failed / warning counted in the rule table; benchretry ledger counts; inventory header | as stated | 6 |
| **test_cleanup.sh** | | | |
| CU00-CU62 | cleanup_bench.sh (B3): dry run; `--yes` from inside the run folder, re-exec from memory, receipt outside; refusals (results/<STAMP>_lowp_benchres or logs/<RID> on scratch, job active, scheduler errors, OWNER, ids, linked `runs/`); guard failure -> UNVERIFIED | as PROD-L | 4 |
| **test_collect.sh** | | | |
| CO00-CO31 | s9_collect.sbatch: every predecessor terminal -> accounting snapshot + guard (no unlock logic, no truthlock folder); the nine terminal states; CANCELLED suffixes; non-terminal / unknown / missing id / no ids -> exit 1, guard not called; guard refusal exit nonzero | as stated | 4 |
| **test_retune.sh** | | | |
| RT00-RT56 | raise to alone admitted at 64 + 128 and refused at 130; dry run vs `--yes` (`scontrol update JobId=7001 ArrayTaskThrottle=32`), record launch/retune_<utc>.txt, squeue confirmation, unconfirmed -> nonzero; live plain verify job counted but not updated; `_prodH`, squeue failure, bad profile refused; lowering to %16; `--check-drained` | as stated | 4 |
| **test_jobmd.sh** | | | |
| JM00-JM48 | JOB.md: absolute `/scratch/fb31/New_Campaign/...` nots_pull paths (one result folder `_lowp_benchres`), home summaries without `--delete`, main wave and rN commands, one make_resubmit round then ONE submit, bench / benchretry routing, `--allow-concurrent-prodl` HQ-only, serialisation after PROD-L, retune + drain, waiter semantics, reconcile / close / cleanup / accept commands, NO lock / unlock / P5 instructions, section 14 with the ABESS D54.3 disclosure, the no-truth note and the stale-artefact recovery | as stated | 4-6 |
| **test_accept.sh** | | | |
| AC00-AC71 | accept_bench.R (new CLI: `--results --lists --code --r2-manifest --inputs-manifest --out [--local-test]`): positive controls = the manager's 3 real live cases (24 records) with `--local-test` (ACCEPTED, 24 PASS, report says environment checks skipped; WITHOUT `--local-test` they FAIL) and real records produced by the frozen CLI (local mode ACCEPTED; pinned provenance, non-local, ACCEPTED, ABESS D54.3 disclosure, results folder untouched); one-defect negative controls on the pinned fixture (missing coefficients entry, beta_pen / beta_ols / A1 beta of length p-1, support != row support, EBIC/K37 k mismatch, test_library TRUE, wrong sealed_library, wrong R) exit 2; missing case or method exit 3; missing `--r2-manifest` / `--inputs-manifest` refused | as stated | 6 |
| ACI1a-ACI1e | I1 (Sol R1): single mutation on copies of the real live records (csv + sha256 re-sealed): F4 `ebic1_lam005` removed from rows AND both coefficient lists in EVERY F4 record (3 FAIL) and in the first record only (1 FAIL); extra rule in F2; A1 roles all S0; F5 `sic_smax` missing; each exit 2 with the reason `rule ids/roles differ` | as stated | 6 |
| ACI2a-ACI2f | I2: F1 `ebic1` beta_ols all NA; F1 `cv_min` beta_ols finite (SPEC: NA for CV rules); beta_pen with an Inf; A1 `fit$pip` deleted; A1 pip 1.2; A2 beta NA on a successful fit; each exit 2, one failing record, the matching reason | as stated | 6 |
| ACI3a-ACI3h | I3: data_seed 1 / method_seed 4000001; fold_seed changed; scale_key c050 in a c100 folder; scale 0.5; run_id different from the results folder name; y_sha256 zeros; `record$input$hashes` changed; dataset absent from the sealed inputs manifest (copy of the manifest without it: its 8 records FAIL, the others PASS) | as stated | 6 |
| ACN1a-ACN1h | N1 (Sol R2) selections, single mutation on copies of the live records: F1 cv_min k 999; F1 ebic1 support unsorted `16;3;7;14`; duplicate index; index p+1; A2 ssl_final support `20` k 1 with beta unchanged; support and k columns removed from the A1/A2/A3 rows (3 FAIL); F4 coefficient-entry k != its row; A1 row support != fit$rules; each exit 2 with the matching reason | as stated | 6 |
| ACN2a-ACN2c | N2: F4 bic_K37 crit_value 99999; F5 bic_K37 support != bic; F4 bic_K37 k != bic; exit 2, reason `bic / bic_K37 pair differs` | as stated | 6 |
| ACN3a-ACN3b | positives that must stay ACCEPTED (24 PASS): a legitimate null selection made consistently (F1 ebic1 + K37: support "", k 0, beta_pen/beta_ols zeros) and a legitimate failed rule made consistently (F1 ebic05 + K37: status failed, support NA, k NA, coefficient entry failed with NA vectors) | as stated | 6 |
| ACI4a-ACI4k | I4: `code$source_sha256` NULL; one common wrong 64-hex in every record (24 FAIL; also in the non-local pinned fixture); `record$code$files` with one hash changed (fingerprint not / recomputed: the latter caught only by the r2 comparison); non-local: `package_provenance` removed, a pinned package (glmnet) at the wrong version, a non-base package (glmnet) located in R's own library; the supplied `--code` tree with one byte changed / one extra file FAIL (named file / extra files), the genuine tree ACCEPTED | as stated | 6 |

| **test_stage_guard.sh** (HQ D57) | | | |
| SG01-SG39 | capacity-modelling guard stub (home used + add > limit -> exit 1 `home+add>limit`, ops/guard.sh line format) seeded at 9.46 GiB: the pre-staging reservation of the stage (75 MB) is admitted; after "extraction" (usage += stage) the main wave is ADMITTED and the guard is called with PLANNED_HOME_MB_MAIN (5), never the stage size again; the old behaviour (stage size again) is refused; D57 line in launch/main/guard_receipt.txt; a home without room for the growth refuses (exit 1); guard_check.sh probes the guard's OWN limit: 9.70 GiB guard + REQUIRED 10171187 -> OK with probe ~327 MB, 9.70 guard + REQUIRED 9.6 -> refused, 9.6/9.6 unchanged (probe ~224 MB), guard below the floor or without the campaign limit refused | as stated | D57 |
| D5701-D5709 (test_manifests.sh) | after clear_stale.sh --yes archived a lock dir and a hidden temp into LOG_RUN/cleanup/<utc>/ and with a hidden ledger temp `.7002_0.1234.tmp`: `--piece logs` SUCCEEDS and its MANIFEST.sha256 lists the archived files and the ledger temp; the result piece still refuses (exit 2) with a stale artefact in its own folder | as stated | D57 |

Not encoded: the live local run of real cases through `batch_runner.sh` with the real CLI (DESIGN section 8, manager's live run), `stage_local.sh`, `final_accounting.sh`, `frozen_check` symlink variants (covered in PROD-L), the P0b R checks of `s0_verify` (needs R on the cluster build). (`bench_env_probe.R` was listed here until HQ D82; it is now encoded in `test_probe_real.sh`.)

## HQ D82 (rev 2): `test_probe_real.sh` (26 checks) -- the env probe run for real

Rev 1 failed on NOTS at `s0_verify` (job 2510090): `R/bench_env_probe.R` called `lowp_load_method(mid, code, p=20, test_library=FALSE)`; the frozen signature is
`lowp_load_method(id, code_dir, p, test_versions = FALSE)` (`code/bench_lowp/R/common.R:2`), so R stopped with "unused argument (test_library = FALSE)".
Why the suite missed it: (1) every unit suite replaces `Rscript` by a stub (`lib.sh`), so no bundle R script except `accept_bench.R` ever ran; (2) the probe was
listed above as "not encoded"; (3) the live run's probe step expected a FAIL (laptop glmnet 4.1-10 != pin 5.1) and did not check the reason, and run 1 stopped
before reaching it. A wrong keyword and a wrong package version both gave exit 1.

| IDs | What | Expected |
|---|---|---|
| PR00-PR02 | prerequisites; `code/bench_lowp` = r2 file by file (34/0, the REAL frozen tree); the frozen signature line | as stated |
| PR03-PR05 | the real probe on the real frozen code with a library of metadata-only packages at the r2 pins (`tests/mk_pinlib.R`; pins typed by hand) | exit 0, `PASS benchmark environment`, no "unused argument" |
| PR06 | same without `--local-test` on R 4.4.1 | exit 1 `R 4.5.2 required` |
| PR07 (x8) | each pinned package at 0.0.1 | exit 1 on the pin check, never a wiring error |
| PR08, PR08b | doParallel / digest absent from the pinned library while the laptop's own copies are on the path | exit 1 `Package outside sealed library` (new probe check = frozen CLI rule) |
| PR09 | strict pin check kept (`test_versions = FALSE`) | as stated |
| PR10-PR11 | rev-1 line reproduced on the same code and library | exit 1 `unused argument (test_library = FALSE)` |
| PR12-PR14 | `tests/check_frozen_calls.R`: match.call of every bundle call into a frozen definition (`accept_bench.R`, `R/*.R`) | 2 calls, 0 bad; the rev-1 line flagged BAD |
| PR15 | the bundle has exactly 3 R scripts outside tests/review (all checked) | 3 |
| PR16-PR17 | `s0_verify` passes `--code $BENCH_DIR --library $R_LIBS_BENCH`; `BENCH_DIR` = staged `code/bench_lowp` | as stated |

The live run (rev 2, `tests/live/live_bench_rev2.out`) also runs the staged `slurm/s0_verify.sbatch` itself, end to end, on the extracted stage (positive and a
wrong-pin negative).


Known limits (Sol D82 narrow check, minor, documented): `mk_pinlib.R` packages carry no dependency metadata, so the transitive-dependency and
base/recommended branches of the probe's location rule are verified by inspection against the frozen CLI, not by a test; `check_frozen_calls.R` is a
name/formals compatibility check for this bundle's calls (it accepts any matching definition of a repeated name, skips file-local names, does not prove
required arguments are supplied, and does not cover shell → CLI flags, which the live run exercises).
