# PROD-L acceptance tests (black box, from DESIGN.md only)

Run all: `bash <B>/tests/run_all.sh <PC_TEMP_PATH>` (writes `<run>/<suite>.log`, `.rc`, `SUMMARY.txt`). One suite: `bash test_X.sh WORKDIR` or `py -3 test_X.py WORKDIR`.
Work dirs must be under `<PC_TEMP_PATH>` (refused otherwise). Every suite ends with a line `<suite>: N passed, M failed`; exit status = failures > 0.
`PRODL_B_SRC=<folder>` points the staging helpers at another bundle folder (used only to smoke-test the tests themselves against mock scripts).

Assumptions the tests make where DESIGN.md is silent (change them here and in the suite if the manager rules otherwise):
- Staged layout as section 9: the driver and all scripts are run from `HOME/runs/<STAMP>_lowp_prodL/code/prod_l/` (a copy of B without tests/, review/, PROGRESS.md); common.sh is found with `find code/prod_l -maxdepth 2 -name common.sh`.
- Stubs: `sbatch squeue sacct scancel scontrol python3 python stat Rscript` on PATH, and the env names `GUARD SQUEUE SACCT SCANCEL SCONTROL PYTHON` (pilot convention) point at the same stubs. squeue stub rows are `id|name|state|cpus`.
- `ceiling_check.py --plan` file has the header row `step cpus max_concurrent_tasks phase` (tab separated); `--own-ids` is comma separated.
- batch_runner.sh is SOURCED after pilot_init/pilot_modules/pilot_blas_single (it may `exit`); ledger fields are whitespace-separated in the order of section 3.
- On the laptop `chmod 000` on a directory has no effect (NTFS): the "locked truth" controls use a `stat` shim that reports mode 0 for the two truth trees (real chmod on Linux).
- truth_lib.sh is replaced by a marker-file stub in the staged copy for test_unlock.sh (permission helpers are Linux-only and covered by test_truth_lock_linux.sh).
- inventory tables of reconcile_prodl.py are parsed by header (a `unit` column and one of status/state/outcome/class/result).

| id | what it checks | expected | DESIGN section |
|---|---|---|---|
| **test_driver.sh** | | | |
| D00 | submit_prodl.sh exists in the bundle | present | 5 |
| D01-D03 (alone, withH) | `--wave main`: exit, number of submissions, recorded sbatch vectors (see V-checks below) | exit 0; 10 submissions | 5 |
| V-names | job names `lowpL_<step>`, each once, exactly the 10 steps | set equal | 5 |
| V-acp | `--account=commons --partition=commons --constraint=sapphirerapids` on every job | all present | 5 |
| V-cpus | cpus per task 2,1,1,1,4,16,1,1,1,1 | per table | 5 |
| V-mem | 4G build; 2G verify/truthlock/smc/smcrep; 1G lock/enum/unlock/collect | per table | 5 |
| V-time | 0:40,0:30,0:30,0:10,1:00:00,0:45:00,5:00:00,5:00:00,0:15,0:15 | per table | 5, 3 |
| V-array | enum30 `0-23%4`/`%2`; smc `0-95%32`/`%16`; smcrep `0-479%32`/`%16`; no array on the others | exact strings | 5 |
| V-deps | afterok chains; smcrep afterok gate AND afterany smc; unlock afterany lock+5..8; collect afterany 1,2,3,unlock | exact sets | 5 |
| V-kill | `--kill-on-invalid-dep=yes` on every dependent | present | 5 |
| V-outputs | `--output/--error` under LOG_RUN | prefix | 5 |
| launch record | launch/main: prodl.env + .sha256 (verifies), STAGED_SHA256.txt, OWNER, frozen manifest, lists/units.tsv, guard receipt (GUARD_CHECK_OK), ceiling receipt, effective_env.txt, sbatch_args.tsv with 10 lines | present | 5.6 |
| jobids | LOG_RUN/jobids.tsv and RUN_HOME/JOBIDS.tsv: header `wave step jobid array dependency`, 10 rows wave=main, ids digits, files agree | as stated | 5.6 |
| guard MB | guard asked for 110 MB (main), 5 MB (other waves, p5 scan) | recorded | 5.3 |
| D04-D08 | `--dry-run`: exit 0, sbatch never called, no launch record/JOBIDS, prints 10 vectors with the throttled arrays | as stated | 5 |
| D09-D17 | `--pieces enum20,enum30` (8 jobs), `smc,smcrep` withH (8), `smcrep` (7); vectors via V-checks | exit 0; counts; V-checks | 5 |
| D18-D20 | `--local-test` + PILOT_LOCAL_TEST=1 + fake NC_HOME_ROOT + hook accepted; hook recorded in effective_env | exit 0; 10 jobs | 5.0 |
| D21-D28 | wave r1 (smc, 30 units = 2 tasks): 5 jobs (truth test, lock, array `0-1`, unlock, collect), launch/r1 added, JOBIDS appended (main rows kept), guard 5 MB | exit 0 | 4, 5 |
| D29-D31 | wave r2 withH smc+smcrep: 6 jobs, smcrep afterany smc | exit 0 | 4, 5 |
| D32-D33 | wave r1 without its resubmit list | refused, nothing submitted | 4 |
| D34-D35 | wave p5 with 3 / 20 units: `s4_p5`, 1 CPU, 4G, 9:00:00, array `0-(N-1)%min(N,8)` alone, `%min(N,4)` withH | exact | 5, 6 |
| D36-D39 | `--p5-scan`: one job `lowpL_s5_p5scan` (1 CPU, 2G, time limit 08:10:00 = 29,400 s for the real list and no expected inventory, HQ D63; was 0:30), guard 5 MB | exit 0 | 6 |
| D40-D53 (HQ D63 + Sol narrow-check residual) | scan time limit = max(7,200 s, 600 s + ceil(records x 2.0 s)), records = smc + smcrep rows of the staged `lists/units.tsv` (primaries) + data rows of `RUN_HOME/p5/expected.tsv` when present (possible P5 retries; list swapped for fake ones and restored): real list, initial (no expected) -> `--time=08:10:00`, never 00:30:00, driver prints `P5 scan: 14400 records (14400 primaries + 0 possible retries) -> time limit 08:10:00`; final with header-only expected -> 08:10:00; 100 expected retries -> 08:13:20; heavily retried final (one retry per primary, 28,800 records) -> 16:10:00; Sol residual reproduced (primaries-only 08:10:00 < 2 x 0.75 s x 28,800); 10,000 rows -> 05:43:20; 100 rows and 1 row -> the 02:00:00 floor; 3,300 -> 02:00:00 and 3,301 -> 02:00:02; 3,300 primaries + 1 retry -> 02:00:02; enum rows are not counted; every limit >= 2 x the observed 0.75 s per record x records read; the old 1,800 s is below 0.75 s x 14,400 | as stated | D63 |
| N01 (x7) | each hook PILOT_DRYRUN PILOT_SKIP_MODULES PILOT_TIME_BIN PRODL_UNIT_CMD PRODL_TEST_WALL_S PRODL_TEST_BUDGET_S PRODL_TEST_NOW_OFFSET_S set without `--local-test` | exit 2, nothing submitted/created | 5.0, 3 |
| N02-N04 | PILOT_LOCAL_TEST=1 without the flag; flag without PILOT_LOCAL_TEST; flag without a fake NC_HOME_ROOT | exit 2 | 5.0 |
| N05-N07 | `--wave bench`, `--pieces bench`, `--pieces smc,bench` | exit 2; message names BENCH-FIX gate | 5.0, 10 |
| N08-N11 | truth trees locked (mode 000) at submission, main and a later wave | exit 2; guard NOT called; message "locked" | 5.1 |
| N12-N13 | guard refuses (home full / campaign over) | exit 1, nothing created | 5.3 |
| N14-N15 | frozen v2.2.1 file altered; unlisted file in the frozen tree (staged list regenerated) | exit 2 | 5.4, 0.3 |
| N16-N17 | STAGED_SHA256.txt mismatch (a staged R file / list file altered) | exit 2 | 5.4 |
| N18 | launch/main already exists | exit 2 | 5.4 |
| N19-N22 | later wave (r1, p5) while a run job is RUNNING / PENDING / a pending array in squeue | exit 2, nothing submitted | 5.2 |
| N23-N24 | squeue failing (main and later wave) | refused (not 5), nothing submitted/created | 5.2, 7 |
| N25-N28 | ceiling: alone + `_prodH`; PROD-H 2x(50x2)=200 withH; control PROD-H 124 + 68 = 192 admitted; unparsable squeue row | exit 2 / 0 / 2 | 7 |
| N29 (k=1,2,6,10) | sbatch rejected at call k | exit 5; k attempts; earlier ids cancelled by explicit id (no selectors); SUBMISSION_ABORTED.txt; jobids.tsv ids digits | 5.7 |
| N30 | sbatch prints an unparsable id at call 3 | exit 5; ids 7001,7002 cancelled | 5.7 |
| **test_deadline.sh** | | | |
| DL00 | bundle has common.sh, batch_runner.sh, prodl.env | present | 3 |
| DL01-DL06 | 3 quick units, window open: exit 0, 3 runs, per unit exactly `.start`+`.end` with the documented fields (unit piece task job_tag host start_utc deadline need_s; unit rc outcome wall cli_status cli_skipped end_utc), D = T0+WALL-120 (hook), inventory rows, timing rows, `.start` exists before the unit runs | as stated | 3 |
| DL10-DL17 | offset 640 (now+NEED > D): nothing starts, all deferred (`unit reason=deadline now deadline need`), exit 0, inventory deferred, no `.start` | as stated | 3 |
| DL20-DL21 | offset 560: first unit and the next start | 2 runs | 3 |
| DL30-DL35 | deadline reached mid-task (window 12 s, first unit 20 s): first unit runs, later units deferred, exit 0 | as stated | 3 |
| DL40-DL46 | unit over budget (3 s): `killed_timeout`, rc 124/137, wall about the budget, task exit 1, next unit still runs | as stated | 3 |
| DL50-DL54 | failing unit rc 3: `unit_failed`, exit 1, next unit runs | as stated | 3 |
| DL60-DL65 | skipped units (smc `skipped=TRUE`; enum "nothing to do"): outcome `skipped`, cli_skipped TRUE, enum cli_status NA | as stated | 3 |
| DL70-DL74 | SLURM_JOB_END_TIME-60 caps D; far/non-numeric value ignored | as stated | 3 |
| DL80-DL83 | p5 task with production constants: starts; at elapsed 3500 s deferred (need 29,280) | as stated | 3 |
| DL90-DL91 | second job tag on the same unit adds files, first tag's records byte-identical | 4 files | 3 |
| DL95 (x4) | PRODL_UNIT_CMD / PRODL_TEST_WALL_S / PRODL_TEST_BUDGET_S / PRODL_TEST_NOW_OFFSET_S without PILOT_LOCAL_TEST | pilot_init exit 70, no unit | 3 |
| clean checks (DL04, 16, 35, 46, 54) | ledger holds only `.start/.end/.deferred`; inventory only `<JOB_TAG>.tsv`; no tmp leftovers | none other | 3 |
| **test_resubmit.sh** | | | |
| RS00 | make_resubmit.sh and clear_stale.sh exist | present | 4 |
| RS01-RS06 | RUNNING / PENDING array in squeue, squeue error, sacct RUNNING, sacct PENDING, sacct error | exit 3,3,4,3,3,4; nothing written | 4.1 |
| RS10-RS26 | list = units without verified .done/.sha256: corrupted sidecar listed, deferred-only listed, 1 failed start listed, .done without sidecar listed; 2 starts + no done -> exceptions file only; 2 starts + done -> neither; chunks 25+14 renumbered 0..1, order kept, units.tsv format | exact | 4.2-4.4 |
| RS30-RS36 | second run SAME_LIST exit 0 (file unchanged); changed state same wave -> exit 2 (file unchanged); new wave r2 -> 38 units | as stated | 4.4 |
| RS37-RS39 | `--dry-run` | exit 0, no file, reports units | 4 |
| RS40-RS42 | everything done (only an exception left) | NOTHING_TO_RESUBMIT, exit 0, no file | 4.4 |
| RS50-RS54 | stale `.lock` / `*.tmp.*` for a listed unit; lock on a done (unlisted) unit | exit 5 naming clear_stale.sh; exit 0 | 4.5 |
| RS60-RS64 | prefixes: enum20 `EXACT` (an SMCBVS.done does not count), smcrep `SMCBVS_rep<m>` (a primary SMCBVS.done does not count) | exact lists | 4.2 |
| CS01-CS03 | clear_stale.sh dry run | exit 0, nothing changed, lists lock and tmp files | 4 |
| CS04-CS06 | `--yes` with an active job / squeue failing | exit 3 / 4, nothing moved | 4 |
| CS07-CS14 | `--yes`: moved (not deleted) to LOG_RUN/cleanup/<utc>/ with owner.txt and a listing; verified results untouched; make_resubmit then proceeds | as stated | 4 |
| **test_manifests.sh** | | | |
| MM00 | make_manifests.sh and make_resubmit.sh exist | present | 8 |
| MM01-MM04 | run job RUNNING in squeue; squeue fails; sacct fails; sacct RUNNING with empty squeue | exit 3 / 4 / 4 / 3, no manifest | 8 |
| MM05-MM07 | `*.lock` dir / `*.tmp.*` / `*.tmp` artefact in the piece folder | exit 2, no manifest | 8 |
| MM10-MM14 | piece with a non-done / not_run unit | exit 6, nothing written; with `--allow-incomplete` closes (manifest + CLOSED) | 8 |
| MM20-MM26 | complete piece: exit 0; MANIFEST.sha256 verifies (`sha256sum -c`) and lists exactly the files present; `manifests/<piece>.CLOSED`, `<piece>.inventory.tsv`; summary.tsv row (folder, manifest sha256, file count) | as stated | 8 |
| MM27-MM28 | second close of a CLOSED piece | exit 2, manifest intact | 8 |
| MM30-MM33 | the other three pieces close independently (smcrep prefix listed) | exit 0 each; 4 summary rows | 8 |
| MM40-MM44 | existing valid manifest is revalidated, not replaced (exit 0); existing manifest that no longer verifies | exit 2, manifest untouched, not CLOSED | 8 |
| MM50-MM56 | `--piece logs` before final accounting files; with none / 3 of 4 pieces CLOSED; then with all four | refused (no manifest); exit 0, logs manifest + logs.CLOSED + summary row | 8 |
| MM60-MM64 | make_resubmit.sh on a CLOSED piece | exit 2 naming CLOSED, no list; open piece still works | 8 |
| N31-N37 (test_driver.sh) | `--wave r1 --pieces <closed>` (also mixed), `--p5-scan` and `--wave p5` with smc or smcrep CLOSED; control: only smcrep closed, `--pieces smc` runs | refused, nothing submitted; control exit 0 | 8, 6 |
| D01b (test_driver.sh) | `SECRET_TOKEN_TEST=xyz` in the environment | absent from launch/<wave>/effective_env.txt | 5.6 |
| V-outpat (test_driver.sh) | `--output/--error` of plain jobs use `%j`, array jobs `%A_%a` | exact | 5 |
| **Round 2: regression tests for Sol's R1 review (R1_FIX_PLAN.md F1-F13)** | | | |
| UN60-UN67 (test_unlock.sh, F1) | recover_truth.sh: all recorded ids terminal proceeds; active earlier/other-wave task, ANY recorded id active, sacct error, missing accounting for an id, non-terminal row, unparsable row, squeue active-row-plus-"Invalid job id" error | refused, trees untouched (control exit 0) | F1 |
| S8-00..S8-14 (test_unlock.sh, F1) | the REAL slurm/s8_unlock.sbatch: control (all terminal) unlocks; active task of an earlier wave / another wave's pending array / this wave's array; squeue error; Sol's mixed active-row + Invalid-job-id repro; sacct error; id missing from accounting; RUNNING row; unparsable row; controls (array task rows only, FAILED/CANCELLED+/TIMEOUT/NODE_FAIL, foreign job, own finalizer, non-fitting id in squeue) | STOP, exit nonzero, trees stay locked; controls unlock | F1 |
| RQ00-RQ16 (test_deadline.sh, F3) | same job/task id run twice: second refuses, no unit started, first ledger and inventory byte-identical; SLURM_RESTART_COUNT=1 -> exit 71 before any ledger/inventory write (also p5 arm, production mode); restart count 2 after a finished run; count 0 is a normal start | as stated | F3 |
| ES01-ES18 (test_deadline.sh, F13) | end-time source: numeric SLURM_JOB_END_TIME (end_epoch, end_source); absent -> `squeue -h -j $SLURM_JOB_ID -o %e` parsed with date -d; env wins over squeue; near squeue end defers all; local test falls back to script time and records it; production with neither source: all units deferred reason=no_scheduler_end_time, exit 1; near numeric end in production defers; every .start/.deferred carries end_source and end_epoch | as stated | F13 |
| DL74, DL74b-d | junk SLURM_JOB_END_TIME is treated as absent: local test still runs, production defers all (reason=no_scheduler_end_time, exit 1) | as stated | F13 |
| V-norequeue (test_driver.sh) | every sbatch vector carries `--no-requeue` (main, r, p5, p5scan) | present | F3 |
| D34b/D35b (test_driver.sh) | wave p5r1 reads units_p5r1.tsv: 4 units, `s4_p5`, `%min(N,4)` withH | exact | F2 |
| D36-D39, N34-N37 (test_driver.sh) | `--p5-scan --phase initial` (the old unphased form is gone); P5 lists are units_<wave>.tsv + expected.tsv | as before | F2 |
| PH01-PH13 (test_p5.sh) | `--p5-scan --phase initial|final|final2|r1`: one job, launch/p5scan_<phase>, PHASE=<phase> in the job environment, reuse of a phase name refused, invalid names (bogus, Initial, final_x, r, r1a, empty) refused, active run job refused | as stated | F2.1 |
| SC01-SC09 (test_p5.sh) | the real s5_p5scan.sbatch: scan_<phase>_{smc,smcrep}.tsv + scan_<phase>.ok only if both scans succeed; failed phase repeated under a new name; no unphased scan_smc.tsv | as stated | F2.1 |
| EX01-EX42 (test_p5.sh) | make_p5_list.sh --from-scan initial: expected.tsv (eligible resource_limit rows of both tables, piece p5, base_piece, repeat) once, scan_initial.receipt with both sha256, idempotent, different scan -> exit 2, locked/incomplete/invalid_inspect -> exit 2, zero eligible -> header-only expected.tsv + none_eligible.txt, gate 3/4, missing tables refused | as stated | F2.2 |
| WV01-WV32 (test_p5.sh) | make_p5_list.sh --wave p5|p5rN: units_<wave>.tsv = never-started units (one per task), exceptions_<wave>.tsv = attempted without valid retry (never relisted), SAME_LIST / exit 2 / NOTHING_TO_SUBMIT, gate, invalid wave name, missing expected.tsv | as stated | F2.3 |
| RP01-RP23 (test_p5.sh) | reconcile p5 inventory: done / attempt_failed / deferred / killed_external / not_run, header `piece unit outcome detail`, INVENTORY.md P5 section, exit nonzero until every P5 unit is done, invalid retry not done, without expected.tsv detail `p5_scan_pending` + PENDING | as stated | F2.4 |
| P501-P511 (test_manifests.sh) | closing smc/smcrep: no expected.tsv, no final scan, final scan older than the P5 wave job, no scan_final.ok, unfinished P5 unit, scan/reconcile disagreement -> exit 6; `--allow-incomplete` closes and lists the unit in CLOSED; zero-eligible path (scan_initial.ok) and the complete path close | as stated | F2.5 |
| CO00-CO30 (test_collect.sh, F4) | the real s9_collect.sbatch: verified unlock + 755 trees -> guard called, exit 0; FAILED record / no record / FAILED or CANCELLED finalizer (Sol repro) / locked trees / lock-only record -> guard NOT called, GUARD_SKIPPED.txt names recover_truth.sh, accounting kept, exit nonzero; terminal whitelist (PENDING RUNNING REQUEUED SUSPENDED FOO non-terminal; the nine terminal states pass) | as stated | F4 |
| ST01-ST14 (test_resubmit.sh, F5) | EXACT.rds.tmp4242, EXACT.sha256.tmp4242, .done.tmp4242, `.lock` (enumerator) and SMCBVS.rds.tmp.123, SMCBVS.lock (adapter): make_resubmit.sh refuses (5), clear_stale.sh lists and `--yes` moves all six, then make_resubmit.sh proceeds | as stated | F5 |
| MM80-MM83 (test_manifests.sh, F5) | the real enumerator temp names block `make_manifests.sh` (exit 2) until `clear_stale.sh --yes`; then the piece closes | as stated | F5 |
| VE00-VE13 (test_resubmit.sh, F6) | strict completion: missing RDS with a sidecar for another file, two-line EXACT sidecar, .done of another hash, empty RDS, sidecar naming another file; one-line SMC sidecar, duplicate name, malformed .done, malformed CSV, 3-row CSV, escaping name -> listed; committed scientific failure and valid units not listed | as stated | F6 |
| MM90-MM91 (test_manifests.sh, F6) | empty EXACT.rds / malformed SMC CSV inside the close gate | exit 6 | F6 |
| ST20, MM70-MM74 (F11, F7) | no `.reconcile_*` or diagnostics under RUN_HOME; reconcile output in LOG_RUN/reconcile/<utc>_<piece>.out; RUN_HOME/manifests holds only CLOSED, inventory, summary; CLOSED has `inventory_sha256=<sha of the inventory>` | as stated | F7, F11 |
| SV01-SV07 (test_reconcile.py, F6) | strict controls at reconcile level; committed failure stays done with its native status; an unexpected folder alone, or a malformed CSV alone, makes the exit nonzero | as stated | F6 |
| CL01-CL06 (test_reconcile.py, F7) | home-layout tree: CLOSED piece moved away from scratch stays `done`, exit 0; not closed -> not_run; tampered inventory -> exit 2; INVENTORY.md marks it closed; live pieces still checked against scratch; one final inventory covers every unit | as stated | F7 |
| RT00-RT47 (test_retune.sh, F9) | raise to alone with 70 billed of other work refused (60 admitted, dry run does not call scontrol); `--yes` calls `scontrol update JobId=7001 ArrayTaskThrottle=4`, `JobId=7002 ... =32` only for this run's arrays, writes launch/retune_<utc>.txt, squeue confirms; scontrol no-op -> unconfirmed, nonzero; `_prodH`, squeue failure, bad profile refused; lowering to withH; `--check-drained` exit 0 at 68, 1 at 70, only PROD-L's running allocation counts, squeue failure nonzero | as stated | F9 |
| WT40-WT49 (test_waiter.sh, F10) | WT40 now NOT terminal (one row for three ids); missing id, unparsable row, empty state -> keep waiting (exit 2); array root covered by task rows; real failure with a missing id -> EARLY_FAILURE; sacct query is `-P`, delimited | as stated | F10 |
| UT01-UT20 (test_waiter.sh, manager ruling F8/F10) | `--until-terminal` (flag before or after MAX_CHECKS): never exits early (a failure with another id still RUNNING keeps waiting), exit 0 when every id is terminal and COMPLETED, exit 4 ALL_TERMINAL_WITH_FAILURES when every id is terminal and some failed (task rows, CANCELLED+, OUT_OF_MEMORY), missing / unparsable / empty-state accounting and a lowpL_ job in squeue keep waiting, ssh failure backs off; default mode unchanged (exit 3 at the first failure-like row) | as stated | F8, F10 |
| JM00-JM52 (test_jobmd.sh, F8, F12) | static checks of JOB.md: absolute /scratch/fb31/New_Campaign/ nots_pull paths, home summaries pulled without --delete, waiter exit 3 = triage, WAVE_UNLOCK_VERIFIED precondition, all make_resubmit lists before ONE `--wave rN --pieces` submit, section 14 Operating notes, P5 phase commands, retune `--profile withH --yes` + `--check-drained`, 16 = nominal / 29,160 s / 18 wording | as stated | F8, F12 |
| **Round 3: regression tests for Sol's R2 review (R2_FIX_PLAN.md I1-I3, II1-II2, M1-M2)** | | | |
| L101-L107 (test_p5.sh, I1) | Sol's repro: EMPTY initial inventory -> a late r1 wave commits a resource_limit primary -> the final scan lists it eligible: reconcile nonzero, exceptions.tsv kind p5_unlisted_eligible (header piece kind item detail), INVENTORY.md names the scan phase, closure of smc exit 6 | as stated | I1.2, I1.3 |
| L110-L113 | the same with a NONEMPTY initial list plus one later eligible unit: only the new unit is reported; closure exit 6 | as stated | I1 |
| L120-L130 | `make_p5_list.sh --from-scan r1` appends exactly the new unit (existing rows byte-identical), writes expected_history.tsv (phase, both table sha256, rows_before 1, rows_after 2), same phase twice adds nothing; `--wave p5` lists it; after its retry is done and a NEWER final scan (job above every fitting job) reconcile exits 0 and closure succeeds | as stated | I1.1, I1.2 |
| L140-L141 | zero-eligible control: scan_initial.ok alone no longer suffices (exit 6); a complete newer final scan closes (exit 0) | as stated | I1.2 |
| L150-L158 | coverage violations: control closes; a done unit missing from the final table; a row for a unit that is not done; a fitting wave (r2) / a P5 wave / ANY s1_ job newer than the final scan job; resource_limit rows in state locked / incomplete / invalid_inspect; no scan_final.ok -> exit 6; `--allow-incomplete` acknowledges | as stated | I1.2 |
| L160-L172 | `--from-scan r1` creates expected.tsv when the initial scan failed (history 0 -> 1); initial still accepted; a phase without .ok refused; locked / incomplete / invalid_inspect refused for rN with expected.tsv unchanged; a finalN phase can extend the inventory | as stated | I1.1, II1 |
| X01-X32 (test_manifests.sh, I2) | reconcile CLEAN (exit 0, exceptions.tsv header only); unexpected output with every unit done -> exit 1, row unexpected_output, STATUS INCOMPLETE OR UNRESOLVED; closure refused (exit 6), `--allow-incomplete` closes and saves `<piece>.exceptions.tsv` with `exceptions_sha256=` and `acknowledged_exceptions=1` in CLOSED; close -> move away -> reconcile exit 4 (never 0), row kept with acknowledged=yes, STATUS COMPLETE WITH 1 HQ-ACKNOWLEDGED EXCEPTIONS; tampered or emptied exceptions file -> exit 2; clean close saves a header-only file, moved clean piece stays CLEAN; an unrelated unfinished piece or another piece's exception does not block a clean piece, the owning piece is refused | as stated | I2 |
| EX01-EX06 (test_reconcile.py, I2/I1.3) | live reconcile: CLEAN, malformed_record, unexpected_output, p5_unlisted_eligible naming the scan phase, p5_unsafe_state, newest scan phase chosen by job id | as stated | I1.3, I2 |
| N301-N309 (test_manifests.sh, I3) | native-status counts (one per unit; resource_limit committed failures x2 + complete, nonempty P5 inventory with done retries) are identical before / after closing and pulling smc, smcrep, then all four pieces; every reconcile exit 0 | as stated | I3 |
| RT50-RT55 (test_retune.sh, M1) | the plan holds the live plain enum20 job (4 CPUs): with 60 billed of other work admitted (192), 62 and 64 refused, the record shows the enum20 row, the plain job is not updated, a finished enum20 changes the boundary | as stated | M1 |
| JM60-JM70 (test_jobmd.sh, M2/II1/II2) | no 'invalid job id' tolerance claim in REUSE/DESIGN/JOB; JOB.md section 14 has the II2 command (`truth_wave.sh" unlock`), the WAVE_UNLOCK.txt target, the never-by-hand rule, the II1 note (`--phase r1`, `--from-scan`, append-only); DESIGN/REUSE mention prodl_verify.py, stale_lib.sh, append-only inventory, per-piece exceptions / exit 4, --no-requeue, CLOSED, restart guard | as stated | M2, II1, II2 |
| (all) | existing zero-eligible closure fixtures now carry a complete FINAL scan (rows for every done unit, job 7400 above every fitting job) because scan_initial.ok alone no longer suffices | - | I1.2 |
| **test_stage_guard.sh** (HQ D57) | | | |
| SG01-SG39 | capacity-modelling guard stub (home used + add > limit -> exit 1 `home+add>limit`, ops/guard.sh line format) seeded at 9.42 GiB: the pre-staging reservation of the stage (110 MB) is admitted; after "extraction" (usage += stage) the main wave is ADMITTED and the guard is called with PLANNED_HOME_MB_MAIN (10), never the stage size again; the old behaviour (stage size again) is refused; D57 line in launch/main/guard_receipt.txt; a home without room for the growth refuses (exit 1); guard_check.sh probes the guard's OWN limit: 9.70 GiB guard + REQUIRED 10171187 -> OK with probe ~327 MB, 9.70 guard + REQUIRED 9.6 -> refused, 9.6/9.6 unchanged (probe ~224 MB), guard below the floor or without the campaign limit refused | as stated | D57 |
| D5701-D5709 (test_manifests.sh) | after clear_stale.sh --yes archived a `.lock` dir and `EXACT.rds.tmp4242` into LOG_RUN/cleanup/<utc>/ and with a hidden ledger temp `.7002_0.1234.tmp`: the four result pieces close, `--piece logs` SUCCEEDS and its MANIFEST.sha256 lists the archived files and the ledger temp; a result piece still refuses (exit 2) with a stale artefact in its own folder | as stated | D57 |
| **test_ceiling.py** | | | |
| C01-C02 | empty squeue alone / withH | admitted; receipt carries 132 / 68 | 7 |
| C03-C07 | PROD-L peak over 132 / 68 refused; at the limit admitted; summed pre phase counts | exit 2 / 0 | 7 |
| C10-C11 | `_prodH` present with profile alone (running, pending, array, name anywhere) | exit 2, receipt names PROD-H | 7 |
| C12-C14 | PROD-H `[1-600%50]`+`[601-1200%50]` = 200 refused (receipt 200); `%31`+`%31` = 124 admitted (124+68=192); `%32`+`%31` refused | exit 2 / 0 / 2 | 7 |
| C15 | running rows billed 2 per 1-CPU: 62 ok, 63 refused | exit 0 / 2 | 7 |
| C16-C17 | array without `%N` counts all pending; `%N` caps | boundary 62/63 | 7 |
| C18-C19 | running tasks of an array reduce its pending allowance; range lists `[1,3,5-9%4]` | admitted at 124 | 7 |
| C20 | plain pending job billed(%C) | boundary | 7 |
| C21-C22 | own-run ids ignored (full and partial list) | refused without, admitted with | 7 |
| C23 | unparsable rows (garbage, non-numeric cpus, bad range, 3 fields) | exit 2 | 7 |
| C24-C25 | squeue from stdin `-`; receipt written for a refusal | as stated | 7 |
| C26 | alone: others at most 60 | 30 rows ok, 31 refused | 7 |
| C30-C31 | billed(c)=2*ceil(c/2) for c=1,2,3,4,5,16 at the 124 boundary | admitted at 124, refused at 126 | 7 |
| **test_waiter.sh** | | | |
| WT00 | waiter.sh exists | present | 8 |
| WT01 (x10) | FAILED TIMEOUT OUT_OF_MEMORY NODE_FAIL CANCELLED "CANCELLED by 123" CANCELLED+ PREEMPTED BOOT_FAIL DEADLINE among COMPLETED/PENDING rows | exit 3 at the first check, no sleep, EARLY_FAILURE logged | 8 |
| WT02-WT03 | FAILED with an empty squeue / alone | exit 3 | 8 |
| WT10-WT11 | all COMPLETED, empty squeue (and only foreign jobs in squeue) | exit 0, ALL_TERMINAL | 8 |
| WT20-WT25 | empty squeue + PENDING sacct row; RUNNING; lowpL_ job still in squeue; no sacct rows; REQUEUED | exit 2 (not terminal) | 8 |
| WT26 | two checks of a RUNNING job | exit 2; 2 ssh; sleep >= 600; no 900 | 8 |
| WT30-WT31 | ssh failure (255), its stderr containing FAILED | back-off 900, ssh_rc logged, no EARLY_FAILURE, exit 2 | 8 |
| WT40-WT42 | ids, squeue+sacct and host `nots` on the single ssh command line | present | 8 |
| **test_lists.py** | | | |
| L01-L07 | LF, trailing newline, header, 6 columns, pieces and counts 600/600/2400/12000, no bench, unique units, task counts and sizes | exact | 1 |
| L10-L12 | unit id formats for enum / smc / smcrep, scale and repeat columns | exact | 1 |
| L20-L23 | exact datasets; replicates 1..100 once per cell (/m); every smc unit has exactly 5 repeats m=1..5 | exact | 1 |
| L30-L34 | enum30 `task = 4(s-1)+block`; each task one cell and one aligned block of 25; replicates ascending | exact | 1 |
| L40 | tools/make_lists.py exists | present | 1 |
| **test_reconcile.py** | | | |
| RC01-RC03 | not all done -> exit != 0; inventory/<piece>.tsv and INVENTORY.md written; every expected unit exactly once | as stated | 8 |
| RC10-RC12 | enum classes done / deferred / unit_failed / killed_timeout / killed_external / not_run; done beats an earlier failure; done without ledger | exact | 8 |
| RC20-RC22 | smc classes; a done with a bad sidecar is not done; native v3_status of a done unit reported | exact | 8 |
| RC30 | smcrep classes | exact | 8 |
| RC40-RC41 | unexpected result folder listed, no expected unit hidden | listed | 8 |
| RC50-RC51 | everything done -> exit 0; one deferred unit -> non-zero; no results at all -> non-zero | as stated | 8 |
| **test_cleanup.sh** | | | |
| CU00-CU04 | dry run from inside the tree | exit 0, nothing changed, targets listed, no re-exec | 8 |
| CU10-CU18 | `--yes` from inside runs/<RID> with `--receipt` outside: CLEANUP VERIFIED, re-exec from memory, targets gone, shared code kept, receipt with verdict/guard/residue | exit 0 | 8 (B3, Sol F1) |
| CU20-CU22 | results/<STAMP>_lowp_* or logs/<RID> still on scratch (also in the dry run) | exit 3, nothing removed | 8 |
| CU30-CU34 | run job active (id in JOBIDS column 3), lowpL_* job not in JOBIDS, sacct RUNNING, squeue fails, sacct fails | exit 3,3,3,4,4 | 8 |
| CU40-CU43 | OWNER of another campaign / another STAMP / missing; JOBIDS.tsv missing | exit 3 | 8 |
| CU50-CU52 | final guard refuses | CLEANUP UNVERIFIED, exit 1, receipt written | 8 |
| CU60-CU62 | `runs/` is a junction/symlink outside the root (removal and dry run) | exit 4, nothing deleted | 8 |
| **test_unlock.sh** | | | |
| UN00 | truth_wave.sh and recover_truth.sh exist | present | 5 |
| UN01-UN11 | never-locked path (B2): intact -> LOCK_NEVER_RAN + staged_equal(1260); changed / missing / list missing / duplicate line / swapped file | exit 0 / 1 | 5 |
| UN20-UN28 | normal lock -> unlock on 1,200 + 60 files: WAVE_LOCK_VERIFIED, locked state, WAVE_UNLOCK_VERIFIED sha=equal, no LOCK_NEVER_RAN; a lock that did not lock fails | exit 0 / 1 | 5 |
| UN30-UN33 | file changed while locked -> DIFFERENT; one list only -> DIFFERENT, not never-locked | exit 1 | 5 |
| UN40-UN42 | per-wave evidence dirs: r1 evidence verifies, main's older evidence fails on the same state | exit 0 / 1 / 0 | 5 |
| UN50-UN56 | recover_truth.sh: run job active, lowpL_* job not in JOBIDS, scheduler error, JOBIDS missing refuse (3); lowp_p* pilot job ignored; idle -> reopens (0) | as stated | 5 |

Not encoded by these suites (updated after R2): `final_accounting.sh` and `stage_local.sh` (exercised only by the builders' smoke checks and OPS evidence); the `P0b` R check (`prodl_inputs_check.R`: checked by builder A on the real sealed study, PASS, and on a one-byte change, MISMATCH); the real SMC/enum unit command lines (covered by the live integration `tests/live/`, not by the stub suites); the REUSE.md hash audit (checked by Sol R1/R2). Now encoded and no longer in this list: the all-wave unlock refusal (`test_unlock.sh`), `retune_throttle.sh` (`test_retune.sh`), `make_manifests.sh` (`test_manifests.sh`), `make_p5_list.sh`, the `--p5-retry` path and the P5 attempt record (`test_p5.sh`, `test_deadline.sh`).
