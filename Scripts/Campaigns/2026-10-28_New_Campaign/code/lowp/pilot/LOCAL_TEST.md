# LOCAL_TEST (revision 3, 2026-10-29): fixes of the independent review, with evidence

Windows 11, R 4.4.1, Git Bash. Work areas: `C:\Users\felip\AppData\Local\Temp\lowp_work\pilot_test\` (shell, neg, live, fabricated trees). Nothing written outside `code/lowp/pilot/` and that folder; no SSH, no NOTS. Review: `code/review/REVIEW_pilot_bundle_sol.md`. The bundle must get a **fresh independent review** before OPS submits.

## Reproduce

```
bash   tests/test_shell.sh        <work>/shell      # 31 cases, ~2 min    -> SHELL_TESTS.md
Rscript tests/run_negative_tests.R <work>/neg       # 26 cases, ~4 min    -> NEGATIVE_TESTS.md   (self-contained: builds its own fabricated trees)
```
Both are shipped in `tests/`. Fixture times, memory and sacct values are FABRICATED; they exercise logic only.

## Findings, fixes, evidence

| # | Finding | Fix | Evidence |
|---|---|---|---|
| 1 | blocking: failed `sbatch` not stopping the driver | `submit()` no longer runs in `$(...)`; checks the exit status, validates the id (digits), records ids as they come, and on any failure cancels the submitted ids by explicit id (`scancel`), writes `launch/SUBMISSION_ABORTED.txt`, exit 5 | shell tests: reject at 1st call -> exit 5, 1 attempt; reject at 6th call -> exit 5, 6 attempts, scancel of exactly 7001..7005; unparsable answer -> exit 5; no malformed id in jobids.tsv; complete chain -> 12 submissions |
| 2 | blocking: truth readable during the wave | new gate `s0_truthlock` (afterok verify) -> `s0_lock` (afterok test): `truth_wave.sh lock` sets both staged truth trees to mode 000 and VERIFIES (modes, ls denied, no file visible); all fits `afterok` build+verify+test+lock; finalizer `s8_unlock` `afterany` lock + all fits (refuses while a fit is active, then verifies 755/444, 1,200 + 60 files, hashes = pre-lock); collect after it. OPS recovery: `recover_truth.sh` + JOB.md section 6 | shell tests: dependency graph asserted for steps 3, 4, 5-10, 11, 12; recover_truth refuses (exit 3) while a pilot job is active or the scheduler fails, reopens and verifies 1,200 + 60 files when idle; negative tests: wave lock not verified -> FAIL, wave unlock missing -> INCOMPLETE. **The real chmod 000 behaviour cannot be tested on Windows** |
| 3 | blocking: cleanup fails open | scheduler output and status captured first (`squeue` failure -> exit 4, nothing deleted); recorded job ids from `RUN_HOME/JOBIDS.tsv` checked against the queue and `sacct` states; ownership marker, canonical paths, results/logs gone; residue search and guard errors propagate; final line `CLEANUP VERIFIED` (0) or `CLEANUP UNVERIFIED: <reasons>` (1) | shell tests: squeue exit 17 -> exit 4 and OWNER still there; active id -> 3; no OWNER -> 3; results on scratch -> 3; ids file missing -> 3; guard refuses at the end -> UNVERIFIED (1); clean run -> VERIFIED (0) |
| 4 | blocking: summary PASS without completion | exact expected sets from the lists (30 / 6 / 3 / 24 / 4 / 192), per unit: files, sha256 sidecar/marker vs RDS, timing row with rc 0, semantic checks; Slurm states/exit codes of 12 steps and 67 jobs/array tasks; repeat seed = primary + 1,000; verdicts PASS / WARN / FAIL / INCOMPLETE; exit 0 / 2 / 3; failed units excluded from sizing | review cases (a) rc 2 -> exit 2; (b) 192 markers removed -> exit 3; (c) repeats failed -> exit 2; (d) benchmark arm omitted -> exit 3; plus 22 more (table below); baseline accepted (exit 0, 259/259 valid) |
| 5 | blocking: guard enforces superseded limits | guard is OPS-owned and untouched. `guard_check.sh` REFUSES unless the guard's own LIMIT lines give campaign <= 524288 KB and home <= 10066329 KB, a 513 MB add is refused for the campaign limit, an add past 9.6 GiB is refused for the home limit, the real call is OK without TEST_LIMITS, and no `GUARD_ALLOW_TEST`/`GUARD_TEST_*` is set; receipt `launch/guard_receipt_submit.txt` | shell tests: D7 guard accepted; 7 GiB/9 GiB guard refused; GUARD_ALLOW_TEST refused; planned add refused; home too full refused; driver refuses with no sbatch in each case; **the real `ops/guard.sh` (now 0.5 / 9.6 GiB) was not run here (needs NOTS)** |
| 6 | missing enumeration evidence defaulted to success | required schema, two named scales, p/K/n, `models_scored = 2^p` (derived from p, K), complete exact run, sealed manifest, positive re-check coverage, zero mismatches/fallbacks, finite outputs; missing evidence is a reason, never a default. Fixtures are p-specific (p20 vs p30 lengths, K, counts) | negative cases: p30 record with p20 K/model count -> FAIL; `models_scored = 1` + numerics removed -> FAIL; recheck_count 0 -> FAIL; RDS altered after sidecar -> FAIL |
| 7 | sacct memory fallback not used | batch-step MaxRSS joined by job/task id into the unit table (label `sacct_job_bound`, "job-level conservative bound"); no memory evidence -> verdict INCOMPLETE | negative cases: GNU RSS NA but sacct present -> accepted, all `suggested_mem_request_mb` finite; GNU NA and no sacct -> exit 3 |
| 8 | collector cannot prove its own COMPLETED | collector snapshots predecessors only, fails on sacct/guard errors; OPS runs `final_accounting.sh` (all ids incl. the collector, exit 1 if any row non-terminal); summary requires `sacct_final.tsv` | negative cases: FAILED task -> exit 2; final snapshot missing -> exit 3 |
| 9 | bit vs numerical equality mixed | scores (F, eta, HPM F, top-list F) compared as serialised float64 bytes, non-finite fails; log Z, PIPs, certificate with declared tolerances; decisions exact; T5 thread invariance; every row records byte mismatches and max abs diff | live run on the new enumerator: 26 of 26 rows PASS (T1 scores/decisions/aggregates x 6, T2 x 2, T3 x 2, T4 x 2, T5 x 2 ... ) |
| 10 | cleanup ownership boundary | the pilot now stages into its own folder `HOME/runs/<PID>` (code, dev inputs, study copy); extraction requires `test ! -e runs/<PID>`; cleanup removes only that folder and two scratch folders and never touches `code/`, `inputs/`, `manifests/` | shell test: shared `code/core/shared` and `code/lowp_shared` untouched after a verified cleanup |
| 11 | test hooks inherited by real jobs | driver refuses the six hooks unless `--local-test` + `PILOT_LOCAL_TEST=1` + a fake root; every job refuses them (exit 70); effective environment recorded; benchmark records checked (test_library FALSE, pinned sealed library, every non-base package from it, also for dev ids) | shell test: `PILOT_LIMIT` set -> exit 2, no sbatch; negative cases: test_library TRUE -> FAIL, package outside the pinned library -> FAIL, hook in the recorded environment -> FAIL; **live run: the 8 benchmark units run with `--test-library` were all rejected by the summarizer, as designed** |
| 12 | fixture test not self-contained | `tests/make_fabricated_pilot.R` builds every record from the documented interfaces (no external templates, p-specific); `tests/run_negative_tests.R` and `tests/test_shell.sh` ship in the bundle | both suites run from the bundle alone |
| 13 | final OPS configuration not preserved | at submission: final `pilot.env` + sha256, `STAGED_SHA256.txt`, `OWNER`, JOB.md, lists, exact sbatch vectors, guard receipt, effective environment -> `LOG/launch/`; the stage tar and its hash are kept locally by using the durable run folder as `--out`; the summary requires the receipt | shell test: launch record present (12 vectors, receipt, env); negative case: receipt missing -> exit 3 |
| 14 | stale login node | JOB.md: only through the configured `ssh nots` alias (loginx2), one connection at a time | text |
| 15 | sample coverage overstated | JOB.md section 1 and the summary's "Sample coverage and its limits" table state per-arm subsets and extrapolation limits; the 60-row regeneration check is labelled as not a timing measurement. RUN_DESIGN section 4 wording needs HQ to change (**historical revision-3 text, SUPERSEDED: RUN_DESIGN section 4 already states these subsets; no edit is requested**) | text |

Addendum (truth-lock evidence): `s0_truthlock` calls `RSCRIPT=Rscript bash code/lowp/tests/test_truth_lock_linux.sh "$STUDY" "$CODE/lowp/R" --evidence-dir "$LOG/truthlock/evidence"` (scratch, D7); the summary reads `evidence/final_status.txt` (`final_exit_status`, `failed`, `checks`), the download list includes `SCR/logs/<PID>` with that evidence. The script version used here is the one of 21:59 on 2026-10-28 (re-read at the end; unchanged).

## Negative tests of the summarizer (26 cases, all as expected)

baseline accepted (0); review (a) timing rc 2 (2); (b) markers and sidecars removed (3); (c) repeat fits failed (2); (d) benchmark arm omitted (3); enum `models_scored = 1` + numerics removed (2); p30 record with p20 dimensions (2); recheck coverage 0 (2); RDS altered after sidecar (2); thread-invariance defect (2); repeat seed offset wrong (2); benchmark `test_library` TRUE (2); package outside the pinned library (2); unexpected extra unit folder (3); Slurm task FAILED (2); terminal snapshot missing (3); GNU RSS NA with sacct (0, memory from sacct); GNU RSS NA without sacct (3); truth-lock test failed (2); wave unlock record missing (3); wave lock not verified (2); launch receipt missing (3); P0 MISMATCH (2); P0 INCOMPLETE (3); score/aggregate FAIL (2); test hook at submission (2). Result file: `neg/NEGATIVE_TESTS.md` ("All cases behaved as expected").

## Shell tests (31 cases, all as expected)

`guard_check` x 5; submit x 14 (hook, guard refusal, superseded limits, abort at the first and in the middle with explicit cancels, unparsable id, complete chain, dependency graph for steps 3 to 12, launch record, scratch-only output); cleanup x 10; recover_truth x 3. Result file: `shell/SHELL_TESTS.md` ("passed 31 failed 0"). These cover the review's own shell reproductions (guard refusal, rejected sbatch, squeue outage, retained results) against the new layout; the review's harness scripts assume the old layout and were not re-run as such.

## Live run through a fake `sbatch` (real scripts and CLIs, Windows R, sequential)

Staged from the local sealed test study with `stage_local.sh` (10.6 MB tar, 1,432 files, 11.5 MB on disk), unpacked into a fake `runs/<PID>` (sha256 check passed), driven by `submit_pilot.sh --local-test`: guard receipt `GUARD_CHECK_OK` with probes; 12 submissions with the new dependency chain; build; P0a **PASS** (1,200 + 60, 6 of 6 copies); score/aggregate checks **26 of 26 PASS**; enum20 (2), enum30 task 5 (full 2^30), SMC tasks 0 and 24, benchmarks task 0 (8 methods), collect/unlock stubs. Expected local failures: `s0_truthlock`, `s0_lock` (Windows has no mode 000 and `lowp_truth_lock` refuses it), reported as FAIL by the summarizer; the unlock finalizer, via the plain-chmod fallback, verified 1,200 + 60 files, 755/444 and unchanged hashes. The summarizer on this partial tree: OVERALL FAIL (unit sets INCOMPLETE 5/259 valid, hook recorded, truth lock FAIL, benchmarks invalid because they used `--test-library`), exit 2.

## Not testable locally

Real Slurm (dependencies, cancellation semantics, `sacct`), `module`, GNU time, the Linux mode-000 behaviour and the test script's real pass, the real `ops/guard.sh`, NOTS compilers and pinned R 4.5.2 library, timings. The three full p = 30 scaling runs were not executed (command lines dry-run in earlier rounds).

---

# Revision 4 (final-confirmation findings FC5 to FC9): fixes and evidence

Source: `code/review/FINAL_CONFIRM_sol.md` (section 4 and FC5 to FC9; evidence under `lowp_work/final_confirm/`). Tests: `tests/test_shell.sh` (**34 of 34**, was 31) and `tests/run_negative_tests.R` (**45 cases**, was 26), both re-run on the final scripts; fabricated baseline rebuilt first.

| ID | Fix | Test evidence |
|---|---|---|
| FC5 enum acceptance | `summarize_pilot.R` sources `code/lowp/enum/exact_contract.R` (staged in the bundle; `--enum-dir` overrides) and validates every enumeration unit with `lowp_validate_exact(record, c("c100","c050"), list(dataset_id = id), "sealed", exact_scale_set = TRUE)`; pilot extras on top: threads, positive re-check coverage, no fallbacks, p/n. `.done` statuses are compared with the CSV statuses and with the RDS `rows$status` (SMC and benchmarks); an empty HPM is accepted. **The fabricated baseline was rebuilt first to satisfy the full current I2 contract** (top-level `complete`/`models_expected`, sealed-input binding, retained-column map, normalised size masses with `size_logjoint = masses + log Z`, 1,000-row top list, named PIPs, `mpm = {pip > 1/2}`, `scope = "full"`, one unit with `integer(0)` HPM) | baseline accepted (259/259 valid, exit 0, including the empty-HPM unit); new rejections: `.done` "failed,failed" vs CSV ok,ok (smc) and "ok,failed" (benchmark); re-signed records with `complete = FALSE`, without top-level coverage fields, with a scale lacking status/scope, non-normalised size masses, `size_logjoint` inconsistent with log Z, a short top list |
| FC6 cleanup path boundary | cleanup canonicalises both campaign roots (`readlink -f`, must be `New_Campaign` folders), spells every target from the canonical root (`canon(home)/runs/<PID>`, `canon(scratch)/runs/<PID>_{cache,tmp}`), refuses when `runs/` or the target is a link or resolves anywhere else (exit 4), in the dry run too, before any removal | shell tests with real Windows junctions: `runs/` junction to a folder outside the root -> exit 4, outside `precious.txt` intact; same in the dry run -> exit 4; `runs/<PID>` junction to an outside folder -> exit 4, outside folder intact; the earlier 10 cleanup cases still pass |
| FC7 runtime, scaling, wall | benchmark per-fit runtime is read from `rows$runtime_s` and cross-checked with the CSV (SMC: RDS vs CSV); the saved `scaling/scaling_subset.csv` with its four rows (1 and 8 threads x 2 reps, equal task subset, finite wall) is a verdict; **no timing fallback**: the in-process-time fallback in the projection was removed and a missing wall time is a verdict (INCOMPLETE) | baseline: the in-process medians of all 16 benchmark arm x p rows are now finite (A3 p20 35.6 s); rejections: rows runtime != CSV, rows runtime absent, scaling file missing (exit 3), scaling file with two rows, enum30 wall times missing (exit 3) |
| FC8 library and provenance | the package directory must be exactly inside the pinned library (`dirname(path) == library`, no prefix/sibling); each non-base package needs a version and a build under R 4.5.x; the saved `sessionInfo` must show **R 4.5.2**; the method's own package version must equal the CSV `package_version`; all also for dev ids | sibling `R452_UNAPPROVED/glmnet` -> FAIL; effective R 4.4.1 -> FAIL; version "0.0" vs CSV 5.1 -> FAIL; built under 4.4.3 -> FAIL; version absent -> FAIL |
| FC9 wording | the stale request to edit RUN_DESIGN removed (it states the subsets already); JOB now says the only cache in home is the small core `.cpp_cache` inside the pilot-owned `runs/<PID>` (the enumerator cache is on scratch) | text |

Notes. A record that exists but is defective is FAIL (exit 2); evidence that is absent (folders, files, timing rows, accounting) is INCOMPLETE (exit 3). The live fake-`sbatch` run of revision 3 was not repeated: this round changed the summarizer, cleanup, fixtures and tests, not the job scripts; `stage_local.sh` and `submit_pilot.sh` only gained the `exact_contract.R` requirement. FC1 to FC4 (enumerator resume/dropped columns, benchmark message-only status, scoring readiness) belong to other components and are not part of the pilot bundle.

---

# Revision 5 (second final confirmation: RC1, RC2, RC4, RC5)

Source: `code/review/FINAL_CONFIRM2_sol.md`. Tests re-run on the final scripts: `tests/run_negative_tests.R` **70 of 70** (was 45; 25 new RC cases) and `tests/test_shell.sh` **34 of 34**. The shared validator `code/lowp/enum/exact_contract.R` was re-read at the end: last modified 2026-10-28 23:43:59 (it already contains the RC3 cross-field checks: per-size `size_logjoint = size_logmass + log_Z`, HPM = top[1] support/size/mask, `second_F = top$F[2]`, `log_Z >= hpm_F` and `>= lse(top F)`, `log_Z_rel_m0`, distinct masks, section I.6 order); the rebuilt baseline passes it unchanged.

**Baseline rebuilt as a coherent exact posterior** (RC3 alignment): 1,000 distinct listed models with strictly decreasing scores, the best one is the HPM (the empty model in the empty-support control), `log_Z` >= the log-sum-exp of the listed scores, per-size joint masses contain the listed masses of that size, `size_logjoint[k] = size_logmass[k] + log_Z` exactly, PIPs >= the listed posterior shares, `mpm = {pip > 1/2}`, `second_F`/`margin` from the list. Result: 259/259 valid, exit 0.

| ID | Fix | Test evidence (all in `run_negative_tests.R`) |
|---|---|---|
| RC1 per-unit wall and CPU | before a unit is valid or used in sizing: finite positive process wall time (missing: INCOMPLETE, exit 3; zero or negative: invalid, exit 2). **CPU policy**: enumeration units (CPU-bound, multi-thread) need observed user+sys, absent: INCOMPLETE, negative: invalid; single-thread SMC/benchmark units are costed as wall x 1 CPU, their CPU time is informational. `pilot_projection.csv` and `pilot_table.csv` carry `status`/`accepted`; when the pilot is not accepted every projection row says `NOT ACCEPTED` and the summary heading says "do not use for sizing" | one enum30 unit with wall/user/sys NA -> exit 3 and projections NOT ACCEPTED in the CSV and the markdown; all six enum30 walls zero -> 2; one negative enum20 wall -> 2; all enum30 CPU missing -> 3; negative CPU -> 2; one SMC wall NA -> 3; one benchmark wall zero -> 2; SMC/benchmark CPU missing -> still accepted (0); baseline projections `accepted` |
| RC2 scaling identity and coverage | every row is checked: dataset `dev_p0030_S4_r001`; `models_total` = 2^30 (full retained coverage); `n_tasks` 1024; fraction 0.03; `tasks_run` = ceiling(0.03 x 1024) = 31; `models_scored` = tasks_run x models_total / n_tasks; one common task subset (`tasks_sha256`, a column the scaling script now writes); finite positive walls. Nothing is extrapolated from rows that fail | wrong p20 dataset -> 2; `models_total` = 1 in every row -> 2; wrong in one row only -> 2; `tasks_run[1]` = 1 -> 2; models_scored inconsistent -> 2; fraction differs in one row -> 2; different task-subset hash -> 2; hash column absent -> 3; zero scaling wall -> 2 |
| RC4 empty SMC HPM | `fit$hpm` present and empty (`integer(0)`, the null model) is valid and keeps its timing; absent, non-integer/NA, an index outside 1..p, zero/negative, unsorted or duplicated is invalid | baseline contains an SMC primary unit with an empty HPM (valid); absent -> 2; `c(3, 7.5)` -> 2; index 99 -> 2; index 0 -> 2; `c(7, 3)` -> 2; a repeat fit with an empty HPM (primary non-empty) -> accepted |
| RC5 wording | JOB line 11 no longer says "no caches in home": the only cache in home is the small core `.cpp_cache` built inside the pilot-owned `runs/<PID>`; the stale RUN_DESIGN instruction in the revision-3 table above is marked historical and superseded | text |

Sol's saved case trees (`final_confirm2/pilot_*`) were built on the older fabricated baseline (no task-subset hash, enum records that fail the shared validator's cross-field checks), so re-running the summarizer on them gives exit 2 for unrelated reasons; they were used as the specification of the cases, which are re-created on the coherent baseline above. On `pilot_smc_empty_valid_HPM` all 28 SMC units are now valid (no `hpm` reason). Not tested here, as before: real Slurm, the real mode-000 truth lock, the real `ops/guard.sh`, NOTS timings.

---

# Revision 6 (third final confirmation: N1, N2, N3, receipt temp folder)

Source: `code/review/FINAL_CONFIRM3_sol.md`. Re-run on the final scripts: `tests/run_negative_tests.R` **82 of 82** (was 70; 12 new) and `tests/test_shell.sh` **35 of 35** (was 34; 1 new). Shared validator `code/lowp/enum/exact_contract.R` re-read at the end (last modified 2026-10-29 00:30:41; it now carries the PIP-feasibility and size/PIP moment checks): all 39 fabricated EXACT records pass it, and Sol's impossible-PIP mutation (PIPs 1, mpm = all variables) fails it.

| ID | Fix | Test evidence |
|---|---|---|
| **N1** zero memory accepted | a memory source is usable only if finite **and positive**; order GNU time, batch-step MaxRSS (job-level bound), core VmHWM (SMC); a fallback carries an explicit label (`sacct_job_bound (GNU RSS unusable)`, `core_vmhwm (GNU/sacct RSS unusable)`); with no usable source the unit is absent evidence (INCOMPLETE) and the arm/p memory verdict fails; the suggested memory request is computed only from a positive maximum and a projection row is `accepted` only if its request is > 0 | every GNU RSS = 0, positive fallbacks exist -> accepted, labelled, all requests > 0 (exit 0); every GNU RSS negative -> same; GNU 0 and batch 0 for enumerations and benchmarks -> exit 3, all projection rows NOT ACCEPTED and no accepted request <= 0; SMC GNU 0 without sacct -> SMC uses the labelled core figure; one benchmark unit with GNU 0 and batch 0 -> INCOMPLETE (exit 3) |
| **N2** coherent fixture | the fabricated enum records are built from ONE realizable support distribution: 1,000 listed models (strictly decreasing scores, best = HPM, empty model in the control) plus an unlisted remainder with explicit support (the empty model if unlisted, up to five leftover small models, one model of each size 4..K, all scoring below the listed minimum); `log_Z`, size masses, PIPs and `mpm` are derived from it, so sum(PIP) = E|S| (2.351652 both, to the printed digits) and every PIP lies between its listed share and the share plus the unlisted mass | all 39 EXACT records valid under the updated shared validator; re-signed impossible PIPs (all 1, mpm = all) -> FAIL (exit 2); PIPs inconsistent with the size distribution -> FAIL |
| **N3** scaling hash and malformed values | `tasks_sha256` must be a lower-case 64-hex digest in every row (and identical); types and missingness are validated before any comparison and the whole check is wrapped so malformed evidence yields a FAIL/INCOMPLETE verdict with the full report | placeholder string in every row -> exit 2; dataset NA -> exit 2 with PILOT_SUMMARY.md and projections written (was a crash, exit 1, no report); text in a numeric column -> exit 2; NA wall -> exit 2; upper-case digest -> exit 2 |
| receipt temp folder | `submit_pilot.sh` sets `TMPDIR=SCR/runs/<PID>_tmp` (created) before its first `mktemp`; the folder is removed on exit if empty | shell test: with a poisoned caller `TMPDIR`, the receipt path handed to `guard_check.sh` is under `SCR/runs/` and the caller's directory stays empty |

Note: the shell suite must be run **without** `MSYS_NO_PATHCONV` (its junction tests call `cmd //c mklink /J`); with it set they are reported SKIPPED and counted as failures. The negative suite is run with it set. As before: real Slurm, the real mode-000 truth lock, the real `ops/guard.sh` and NOTS timings are not covered locally.

---

# Revision 7 (2026-10-29, single frozen code tree v2.2.1): rewire, new consistency check, evidence

What changed is listed in `CHANGES_v2_2_1.md` (SMC step on `code/core/v2_2_1/study/run_case.R`; `frozen_check.sh` against `v2_2_1.SHA256SUMS` in the stager, the driver, `s0_build` and every SMC task; P5 scan reported by the summarizer, never run automatically; retired `code/lowp/smc/` and `core/v2_2`). Gates, thresholds, steps, dependencies and resources are unchanged (12 steps, 67 jobs/array tasks). The bundle must still get a **fresh independent review** before OPS submits. Nothing was submitted, no SSH. Comparison base: the Sol-reviewed revision-6 bundle (hash-verified copy in `conformance/work/pilot_rewire_audit/baseline/pilot/`); `summarize_pilot.R` differs from it only by additions (P5 block, the new check below, the `--v221-dir`/`--rscript` options, labels "v2.2.1"). The manifest hash and file count are not hard-coded anywhere (the scripts read the manifest at run time; the file count printed is `grep -c .` of the manifest).

## Gate hole found and closed during the rewire audit

A unit whose CSV `v3_status` disagreed with the RDS native status (`fit$status`) used to be accepted (the old test expected a WARN for a CSV-only `resource_limit`). `check_smc` now requires, when the CSV has a `v3_status` column, `v3_status == fit$status` in every row; a mismatch is a bad unit (exit 2). A CSV without the column is not checked (nothing to compare; the shipped adapter always writes it). The negative test for that case now expects exit 2 and a new case with every CSV consistent expects PASS (exit 0, P5 row PASS).

## Commands

```
# negative tests (run WITH MSYS_NO_PATHCONV=1), work dir conformance/work/pilot_rewire_audit/neg_run7
MSYS_NO_PATHCONV=1 Rscript tests/run_negative_tests.R <work>/neg > tests/logs_v2_2_1/run_negative_tests.log     # ~7 min
# shell tests (run WITHOUT MSYS_NO_PATHCONV), work dir .../shell_run7
bash tests/test_shell.sh <work>/shell > tests/logs_v2_2_1/test_shell.log                                         # ~2 min
# stage test on a real sealed study (done once by the previous worker; the sealed study was deleted afterwards)
bash stage_local.sh --sealed <SEALED> --stamp <STAMP> --out <OUT>      # log: conformance/work/pilot_rewire_audit/stage_test/STAGE_TEST_LOG.txt
```

## Results

| Script | Cases | Passed | Failed | Log |
|---|---|---|---|---|
| `tests/test_shell.sh` | 46 (was 35 in revision 6; 11 new: frozen-tree and manifest refusals, `.cpp_cache` tolerated, manifest in launch record, SMC dry run primary and `--repeat 1`, tampered tree and unlisted adapter exit 67, no retired reference) | 46 | 0 | `tests/logs_v2_2_1/test_shell.log` (re-run after the `summarize_pilot.R` change) |
| `tests/run_negative_tests.R` | 88 (was 82; 5 P5 cases + the all-consistent case; one case changed to expect exit 2) | 88 | 0 | `tests/logs_v2_2_1/run_negative_tests.log` ("All cases behaved as expected") |

New or changed negative cases: baseline P5 row PASS with 0/0 and the TSV/summary section written (exit 0); one SMC CSV with `v3_status = resource_limit` over a fine RDS (re-signed) -> exit 2, P5 row WARN with eligible = 1 and the "FINDING FOR HQ" text; every CSV `v3_status` equal to the RDS status -> exit 0, P5 PASS; a real `resource_limit` unit -> exit 2 (existing gate) and P5 eligible = 1; `p5_scan.R` not found -> accepted, P5 row WARN "scan NOT run"; no `_smc` folder -> exit 3 (unit sets) with the P5 row "scan NOT run". Every revision-6 case still passes unchanged.

Stage test (`stage_local.sh` on a real sealed study): rc 0; "frozen v2.2.1 tree verified in the stage: 27 files match v2_2_1.SHA256SUMS" (the manifest as it was at the time); tar 1,485 entries, 0 `lowp/smc`, 0 `.cpp_cache`; `code/core` holds only `v2_2_1` and `v2_2_1.SHA256SUMS`; an independent `pilot_check_frozen` on the extracted stage PASS; staged manifest byte-identical to the source; `STAGED_SHA256.txt` check from the HOME root PASS; 0 retired references in the staged pilot scripts; no truth folder outside the study copy. PASS.

## Reviewed points (read and diffed against the revision-6 baseline)

(a) no existing gate or threshold is weakened (summarizer diff = additions only); (b) the new check cannot reject a legitimate unit: a CSV without `v3_status` is skipped, a consistent `completed`/`exact` unit passes, and a consistent `resource_limit` unit was already invalid under the existing native-status check; (c) `p5_scan.R --run-dir <results>/<PID>_smc` reads `p00xx/<case>/SMCBVS[_rep{m}].done`, the layout `run_case.R` writes (`outroot/results/run_id/pNNNN/case_id/`); (d) `s2_smc.sbatch` passes only `--case --scale --study --outroot --run-id --core-dir --mem-gb --hours --development [--repeat m]`, all accepted by `run_case.R`; `--repeat` is added for array tasks 24 to 27 (list column `repeat` = 1); (e) `--p5-retry` is never passed; the scan is informative (PASS/WARN row, no gate); (f) no manifest hash or file count is hard-coded.

As before, not covered locally: real Slurm, the mode-000 truth lock, the real `ops/guard.sh`, the NOTS R 4.5.2 library and any NOTS timing.

# Revision 7a (2026-10-29, Sol F6 + v2.2.1 review fixes F1 to F4, F7)

`frozen_check.sh` (changed by the manager) now refuses a symlinked tree root and any entry that is not a regular file or directory outside `core/.cpp_cache/` (symlinks to files or directories, special files). The frozen tree `code/core/v2_2_1/` (`study/adapter.R`, `tools/p5_scan.R`, `CHANGES_v2_2_1.md`) and `v2_2_1.SHA256SUMS` changed for the review fixes; the scripts read the manifest at run time. Both suites were re-run in full on the final tree (`p5_scan.R` 09:31:53, manifest 09:32:01); one clean run each, logs overwritten in `tests/logs_v2_2_1/`. Real symlinks only (`MSYS=winsymlinks:nativestrict`, checked with `[ -L ]`); a case whose link cannot be created is counted as a failure ("SKIPPED"), none was.

| Script | Cases | Passed | Failed | Change against revision 7 |
|---|---|---|---|---|
| `tests/test_shell.sh` | 54 | 54 | 0 | 46 -> 54: 8 new symlink cases (below); the 46 old cases unchanged and passing |
| `tests/run_negative_tests.R` | 88 | 88 | 0 | same 88 cases; one P5 expectation updated and the fabricated tree adjusted (below) |

New shell cases (all through `submit_pilot.sh`: exit 2, no sbatch call, and the refusal message is the symlink rule of `frozen_check.sh`; SMC task: exit 67, no DRYRUN command): unlisted FILE symlink (`study/unlisted_adapter.R -> adapter.R`); unlisted DIRECTORY symlink (`study/linkdir -> ../core`); symlink REPLACING the listed `study/run_case.R` with an identical copy elsewhere (the case also asserts that `sha256sum -c` alone passes, so only the link rule can refuse it); `core/.cpp_cache` as a symlink to a folder outside the tree; the tree root itself as a symlink; a REAL `core/.cpp_cache` directory still tolerated (chain complete, 12 submissions); SMC task with an unlisted file symlink (67); SMC task with a symlink replacing `study/run_case.R` (67).

Negative suite, adjustments for the new `p5_scan.R` (tests only; `summarize_pilot.R` unchanged): (1) `make_fabricated_pilot.R` now writes `v3_status = "completed"` in the SMC CSVs, as the shipped adapter does; the new scan (F3) compares every unit's CSV `v3_status` with the RDS native status and refuses a unit whose column is absent, which made the fabricated baseline's P5 row WARN instead of PASS. (2) The case "CSV says resource_limit over a fine RDS" still exits 2 (summarizer gate) but its P5 row is now WARN "scan NOT run ... differs from the RDS native status" (the scan refuses an inconsistent unit) instead of "eligible = 1"; the check was changed accordingly. The case "a real resource_limit unit" still gives eligible = 1.

Summary-line check: `summarize_pilot.R` finds the line with `^p5_scan units=` and reads `units`, `primary_resource_limit`, `eligible` by name; the three appended fields (`launchable`, `locked`, `invalid_inspect`) and the new TSV columns (`retry_problem`, `retry_artefacts`, `launchable`) do not affect it, and its P5 table uses only `case_id`, `base`, `primary_v3_status`, `primary_stop_*`, `retry_state`, `eligible`, all still present. Real check: `source frozen_check.sh; pilot_check_frozen code/core/v2_2_1 code/core/v2_2_1.SHA256SUMS` returns 0 (27 listed files, no link or special entry in the real tree).


# Revision 7b (Sol review 2, R2-3)

The frozen scanner `code/core/v2_2_1/tools/p5_scan.R` no longer falls back to `fit$status`: every SMC record must carry a top-level `record$native_status` equal to its CSV `v3_status`, otherwise the scan refuses (exit 1) and the summarizer's P5 row reads "scan NOT run". The real adapter always writes `native_status`; the fabricated records did not. `v2_2_1.SHA256SUMS` was regenerated by the manager. Tests only (`summarize_pilot.R` and the frozen tree untouched).

- `tests/make_fabricated_pilot.R`: every fabricated SMC record now has `native_status = "completed"` (= its `fit$status` and CSV `v3_status`), as the adapter writes it.
- `tests/run_negative_tests.R`: the "real resource_limit unit" case sets `z$native_status` together with `fit$status` and the CSV (a consistent unit, still exit 2 and eligible = 1); the all-consistent case needs no change (`set_v3` copies `fit$status`, which now equals `native_status`); the CSV/RDS mismatch case (CSV `resource_limit` over a `completed` record) still produces a mismatch (exit 2, P5 row WARN "scan NOT run"). **One new case** (89 total, was 88): a record without top-level `native_status` (re-signed, `fit$status` and CSV fine) -> exit 0 from the summarizer, P5 row WARN "scan NOT run" naming "absent" (the scan must not fall back to `fit$status`). No test weakened.
- Results, one clean run each on the final files (logs overwritten in `tests/logs_v2_2_1/`): `tests/test_shell.sh` **54 of 54**; `tests/run_negative_tests.R` **89 of 89** ("All cases behaved as expected"; baseline P5 row PASS again). Shell suite run without `MSYS_NO_PATHCONV` and with `MSYS=winsymlinks:nativestrict` (no case skipped), negative suite with `MSYS_NO_PATHCONV=1`; work dir `%TEMP%\lowp_work\conf2b_run`.
- Real frozen check: `source frozen_check.sh; pilot_check_frozen code/core/v2_2_1 code/core/v2_2_1.SHA256SUMS` returned **0** against the regenerated manifest.

## Revision 7c (2026-10-30, CONF-2b; GNU time on NOTS, HQ add-on after OPS-4)

Change: `slurm/common.sh` resolves a VERIFIED GNU time, trying `/usr/bin/time` and then the NOTS module binary `/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time`. The sizing arms fail closed with exit 68; infrastructure arms continue wall-only. Each task records the binary in `LOG/env/time_bin_*.txt`. Details are in `CHANGES_v2_2_1.md`, "Revision 7c", and in JOB.md section 5.

| Suite | Cases | Passed | Failed | Log |
|---|---|---|---|---|
| `tests/test_gnu_time.sh <work>` (new) | 30 | 30 | 0 | `tests/logs_v2_2_1/test_gnu_time.log` |
| `MSYS=winsymlinks:nativestrict bash tests/test_shell.sh <work>/shell` | 54 | 54 | 0 | `tests/logs_v2_2_1/test_shell.log` |
| `MSYS_NO_PATHCONV=1 Rscript tests/run_negative_tests.R <work>/neg` | 89 | 89 | 0 | `tests/logs_v2_2_1/run_negative_tests.log` |

All three were run once each, detached, on the final files (exit codes in `tests/logs_v2_2_1/*.rc`, all 0). The real NOTS module binary is not testable on this PC; OPS runs the pre-check in JOB.md section 5.

## Sol review 4 (2026-10-30): pilot READY; minor R4-2 fixed

R4-2: the GNU time probe line must hold three valid nonnegative decimals and an integer RSS (`slurm/common.sh`, `pilot_is_gnu_time`). `tests/test_gnu_time.sh` has 7 new controls, including Sol's `.`/`1..2` case.

Final run, one each, on the final files (`conformance/work/conf2b_runs/pilot_20261030T0215Z/`, all rc 0):

| Suite | Result |
|---|---|
| shell | 54/54 |
| GNU time | 37/37 |
| negative | 89/89 |

## Revision 7d (2026-10-30, CONF-2b; HQ D44 after the OPS-4 STOP at P0a)

The fixes are B1 (P0a becomes a cross-platform generator check), B2 (unlock when the lock never ran) and B3 (the clean-up re-executes itself from memory). Details are in `CHANGES_v2_2_1.md`, "Revision 7d".

Run: `conformance/work/conf2b_runs/run_pilot_suites_7d.sh`, one run on the final files, logs in `conformance/work/conf2b_runs/pilot7d_20261030T0520Z/`, all rc 0.

| Suite | Result |
|---|---|
| `tests/test_p0a_tolerance.R` (new, B1) | 8/8. Unmodified and 1-3 ulp noise PASS (observed max scaled delta 7.6e-16 against the bound 1e-12). A 1e-9 change of one eps value or one pilot X value, a foldid swap, and an altered sealed truth file all give MISMATCH. A missing truth file gives INCOMPLETE. |
| `tests/test_unlock_never_locked.sh` (new, B2) | 7/7 |
| `tests/test_cleanup_inplace.sh` (new, B3) | 3/3. The old script, run from inside the tree, is UNVERIFIED locally. |
| `tests/test_gnu_time.sh` | 37/37 |
| `tests/test_shell.sh` | 54/54 |
| `tests/run_negative_tests.R` | 89/89 |

## Revision 7d (follow-up): Sol PILOT7D minor fixes R7D-1 to R7D-4

Sol's narrow check (`conformance/review/PILOT7D_SOL.md`): READY WITH MINOR FIXES, all findings Low. Disposition: `conformance/review/PILOT7D_disposition.md`.

Final run on the final files: `conformance/work/conf2b_runs/pilot7d_20261030T0710Z/`, all rc 0.

| Suite | Result |
|---|---|
| P0a tolerance (+ names-only case N) | 9/9 |
| unlock (+ 3 R7D-2 cases) | 10/10 |
| clean-up in place (+ 2 R7D-3 cases) | 5/5 |
| GNU time | 37/37 |
| shell | 54/54 |
| negative | 89/89 |
