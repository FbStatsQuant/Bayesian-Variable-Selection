| Case | Expected | Got | Result |
|---|---|---|---|
| stage_local: builds and verifies the tar (extraction + STAGED_SHA256 + frozen tree) | 0 | 0 | ok |
| **submit.sh: refusals (nothing may reach sbatch)** | | | |
| refusal: test hook (NC_STUB_BIN / roots) in a non-test environment -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: guard refuses (home would pass 9.6 GiB) -> exit 1, no sbatch, no launch record, no scratch folder | 1 | 1 | ok |
| refusal: guard with the superseded limits (7 GiB / 9 GiB) -> exit 1, no sbatch | 1 | 1 | ok |
| refusal: manifest mismatch (run_case.R modified, staged list regenerated) -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: manifest mismatch is reported as a frozen-tree failure | 0 | 0 | ok |
| refusal: an unlisted file in the v2.2.1 tree -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: unlisted file is named by the frozen check | 0 | 0 | ok |
| refusal: a staged runner file differs from STAGED_SHA256.txt -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: manifest file missing -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: pre-existing core/.cpp_cache (fresh build required) -> exit 2, no sbatch | 2 | 2 | ok |
| pre-existing cache tolerated by the frozen check and allowed with --reuse-cache (dry run) -> exit 0, no sbatch | 0 | 0 | ok |
| refusal: the scratch log folder of this run already exists -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: own throttles 60 + 50 > 100 -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: throttle overflow, another queued campaign SMC array %60 + our 60 > 100 -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: throttle overflow is reported as such, in the scratch refusal log (nothing in home) | 0 | 0 | ok |
| refusal: a queued SMC array with NO throttle (unlimited) counts as over the limit (fail closed) | 2 | 2 | ok |
| refusal: 41 running tasks of another campaign SMC array + our 60 > 100 -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: squeue fails -> the throttle cannot be established -> exit 2 (fail closed), no sbatch | 2 | 2 | ok |
| R2-8 fail closed: an fb31 array whose name does NOT contain 'smc' (my_other_job, %90) still counts: 90 + 60 > 100 -> exit 2, no sbatch | 2 | 2 | ok |
| R2-8: a small array with a truncated name (%3) plus an unlimited array named x (9006_[1-2], no %N) -> both counted, refused -> exit 2 | 2 | 2 | ok |
| R2-8: 41 + 60 > 100 -> exit 2 even for an array named any_name_at_all (a plain job never counts) | 2 | 2 | ok |
| R2-8: only plain (non-array) jobs queued -> the default 30 + 30 (D49) passes: dry run exit 0 | 0 | 0 | ok |
| D49: PROD-L queued at its cap (%34 = 68 billed CPUs) + PROD-H default 30 + 30 = 94 tasks <= 100 (188 billed <= 192): dry run passes (exit 0) | 0 | 0 | ok |
| D49: a PROD-L array throttled %50 + PROD-H 60 = 110 > 100: refused (exit 2) -- the task guard counts PROD-L too | 2 | 2 | ok |
| **submit.sh: dry run and the exact argument vectors** | | | |
| dry run: exit 0, no sbatch call, nothing created (no launch, config.env, jobs.tsv, scratch folder) | 0 | 0 | ok |
| dry run: precompile vector (1 CPU, 4G, 01:00:00, sapphirerapids, --export=NONE, --no-requeue, account/partition commons) | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| dry run: p1000 array vector (tasks 1-600, %30 (D49), 2G, 13:42:00, afterok precompile, logs on scratch) | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| dry run: p500 array vector (tasks 601-1200, %30 (D49), 2G, 03:52:00, afterok precompile, logs on scratch) | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| **submit.sh: real submission (stub sbatch)** | | | |
| submission: exit 0 with exactly 3 sbatch calls (precompile, p1000, p500) | 0 | 0 | ok |
| submission: precompile argument vector is exactly the specified one | --parsable --account=commons --partition=commons -...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | --parsable --account=commons --partition=commons -...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| submission: p1000 array vector is exactly the specified one, dependency on the REAL precompile id 7001 | --parsable --account=commons --partition=commons -...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | --parsable --account=commons --partition=commons -...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| submission: p500 array vector is exactly the specified one, dependency on 7001 | --parsable --account=commons --partition=commons -...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | --parsable --account=commons --partition=commons -...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| launch record: guard receipt says GUARD_CHECK_OK; copies of config.env, STAGED list and manifest; 3 recorded vectors | 0 | 0 | ok |
| launch record: jobs.tsv holds precompile, primary_p1000, primary_p500 with the three ids | 7001 precompile|7002 primary_p1000|7003 primary_p500 | 7001 precompile|7002 primary_p1000|7003 primary_p500 | ok |
| launch record: manifest.json has submitted_utc, the code-manifest hash (read from disk), the study-manifest hash and the runner hashes | 0 | 0 | ok |
| config.env: OUTROOT/LOGROOT on scratch, L500 = 6300, L1000 = 24000 | 0 | 0 | ok |
| submission: every --output/--error and --chdir is under scratch logs/<RUN_ID> | 0 | 0 | ok |
| refusal: a second submission of the same run -> exit 2, still 3 sbatch calls | 2 | 2 | ok |
| **submit.sh: abort mid-chain cancels by explicit id** | | | |
| abort: sbatch rejected at the 3rd call (p500) -> exit 5, 3 attempts | 5 | 5 | ok |
| abort: the ids already submitted were cancelled BY EXPLICIT ID (7001, 7002), nothing else | 7001 7002 | 7001 7002 | ok |
| abort: SUBMISSION_ABORTED.txt records the reason and the ids; the failed id is not in jobs.tsv | 0 | 0 | ok |
| abort: the scheduler's stderr of the failed call is on SCRATCH (LOGROOT/submit/), not in the home launch folder | 0 | 0 | ok |
| abort: sbatch rejected at the 1st call -> exit 5, one attempt, no scancel | 5 | 5 | ok |
| abort: an unparsable sbatch answer (2nd call) -> exit 5, the first id is cancelled by explicit id | 5 | 5 | ok |
| R2-7: sbatch ACCEPTS the 2nd call (7002) but the jobs.tsv append fails -> abort path, exit 5, no 3rd sbatch call | 5 | 5 | ok |
| R2-7: the accepted job AND the earlier one are cancelled BY EXPLICIT ID (7001 7002); the reason and 'scancel 7002 ok' are in SUBMISSION_ABORTED.txt | 7001 7002 | 7001 7002 | ok |
| R2-7: a CANCEL FAILURE after a journal failure is recorded visibly (stderr and SUBMISSION_ABORTED.txt) and the exit is still 5 | 5 | 5 | ok |
| **precompile and array tasks (stub Rscript)** |
| task before precompile: refuses (exit 66), no fit, no attempt record | 66 | 66 | ok |
| precompile.sbatch: exit 0, precompile.ok holds the compiled_key, cache READY, env record and compile log on scratch | 0 | 0 | ok |
| after the precompile the frozen check still passes (only core/.cpp_cache was added) | 0 | 0 | ok |
| precompile.sbatch refuses a second run (precompile.ok exists): exit 65 | 65 | 65 | ok |
| task 1 (p1000, dataset S1 r001): exit 0, both fits ran, c100 before c050 | 0 | 0 | ok |
| exact Rscript vector, p1000_S1_r001_c100 (L = 24000 s -> --hours 6.666666667, --mem-gb 2, no seed, no extra flag) | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...de/core/v2_2_1/core --mem-gb 2 --hours 6.666666667 | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...de/core/v2_2_1/core --mem-gb 2 --hours 6.666666667 | ok |
| attempt record for p1000_S1_r001_c100: end record done:true, exit 0; result files in results/<RUN_ID>/p1000/<case_id>/ | 0 | 0 | ok |
| exact Rscript vector, p1000_S1_r001_c050 (L = 24000 s -> --hours 6.666666667, --mem-gb 2, no seed, no extra flag) | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...de/core/v2_2_1/core --mem-gb 2 --hours 6.666666667 | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...de/core/v2_2_1/core --mem-gb 2 --hours 6.666666667 | ok |
| attempt record for p1000_S1_r001_c050: end record done:true, exit 0; result files in results/<RUN_ID>/p1000/<case_id>/ | 0 | 0 | ok |
| task 601 (p500): exact Rscript vector (L = 6300 s -> --hours 1.75), result under results/<RUN_ID>/p0500/ | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...aign/code/core/v2_2_1/core --mem-gb 2 --hours 1.75 | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...aign/code/core/v2_2_1/core --mem-gb 2 --hours 1.75 | ok |
| no vector of the primary tasks carries a seed argument | 0 | 0 | ok |
| task 2: a saved resource_limit (run_case exit 2) and an infrastructure exit 1 are recorded per unit; the task itself exits 0 | 0 | 0 | ok |
| task refuses a tampered frozen tree (exit 67), no fit | 67 | 67 | ok |
| task with an index outside the tables (1201) refuses: exit 65 | 65 | 65 | ok |
| task refuses a non-1-CPU allocation: exit 65 | 65 | 65 | ok |
| **rerun.sh: infrastructure failures only, once** |
| fixture: 2,400-unit tree fabricated (ok default; infra, 3 resource_limit, hard timeout, infra_repeat, stale lock, orphan) | 0 | 0 | ok |
| rerun refused while a job of this run is queued/running -> exit 2, no sbatch | 2 | 2 | ok |
| rerun refused at a throttle overflow (another array %95 + 10 > 100) -> exit 2, no sbatch | 2 | 2 | ok |
| R2-8: rerun throttle counts ANY fb31 array whatever its name (nothing_to_do_with_smc %95 + 10 > 100) -> exit 2, no sbatch | 2 | 2 | ok |
| rerun refused when the guard refuses -> exit 1, no sbatch | 1 | 1 | ok |
| rerun refuses a test hook in a non-test environment -> exit 2 | 2 | 2 | ok |
| rerun --dry-run selects exactly the infrastructure unit and the orphan (lock-held unit only warned), no sbatch, lock untouched | 0 | 0 | ok |
| R2-7: rerun.sh: sbatch ACCEPTS (7004) but the jobs.tsv append fails -> exit 5, the job is cancelled BY EXPLICIT ID (7004 only), ABORTED.txt says so, no submitted.json | 5 | 5 | ok |
| R2-7: rerun.sh: a CANCEL FAILURE after the journal failure is recorded visibly (stderr and ABORTED.txt), exit still 5 | 5 | 5 | ok |
| R3-1 (rerun): the failed cancel leaves rerun_1/UNCERTAIN naming job 7004 (the accepted job is not proven terminal), recorded visibly in ABORTED.txt | 0 | 0 | ok |
| rerun: real run exits 0; the stale lock of the lock-held unit was cleared and logged ON SCRATCH (LOGROOT/locks_cleared.jsonl, nothing in home), then the unit is selected | 0 | 0 | ok |
| rerun: units.txt = infra + stale-lock + orphan units only (never resource_limit, timeout, infra_repeat, done) | p1000_S1_r001_c100
p1000_S5_r001_c100
p1000_S5_r002_c050 | p1000_S1_r001_c100
p1000_S5_r001_c100
p1000_S5_r002_c050 | ok |
| rerun: exact sbatch vector (one array over the GLOBAL task indices, %10, --qos=nots_commons, 4G because a step was OUT_OF_MEMORY, --no-requeue, same constraint) | --parsable --job-name=smcbvs_20261029T1500Z_prodH_...mpaign/runs/20261029T1500Z_prodH/rerun_1/units.txt | --parsable --job-name=smcbvs_20261029T1500Z_prodH_...mpaign/runs/20261029T1500Z_prodH/rerun_1/units.txt | ok |
| rerun: jobs.tsv gains rerun_1 with the new id | 7004 rerun_1 | 7004 rerun_1 | ok |
| rerun: the vector is recorded in rerun_1/sbatch_args.txt and the selection in selected.tsv; the scheduler's stderr path is on scratch | 0 | 0 | ok |
| rerun task: runs the listed unit once more (attempt 2, same seed: no seed argument) and leaves its c050 sibling alone | 0 | 0 | ok |
| rerun task: a unit with two failed attempts (infra_repeat) is NOT run again; the skip is logged | 0 | 0 | ok |
| rerun task: a unit that ended by hard timeout is NOT run again | 0 | 0 | ok |
| second rerun.sh after the rerun finished: nothing infra/orphan left (infra_repeat, timeout, resource_limit are not eligible) -> no sbatch | 0 | 0 | ok |
| **P5: the scan as a compute job, one array over the launchable units, one attempt per unit, ever** |
| P5 refused while a job of this run is queued (the rerun array) -> exit 2, no sbatch (no scan job either) | 2 | 2 | ok |
| P5 refused while a primary task is not terminal in sacct -> exit 2, no sbatch | 2 | 2 | ok |
| Q2: P5 still blocks on an INFRA unit (a fresh infrastructure failure awaiting its rerun) -> exit 2, no sbatch, no scan table | 2 | 2 | ok |
| Q2: P5 still blocks on an ORPHAN unit (no attempt, no output, nothing queued) -> exit 2, no sbatch, no scan table | 2 | 2 | ok |
| Q2: P5 blocks on a LIVE job (running / not_run / rerun_queued units exist only while a job of the run is queued) -> exit 2, no sbatch | 2 | 2 | ok |
| P5 refused when the guard refuses -> exit 1, no sbatch | 1 | 1 | ok |
| P5 refuses a test hook in a non-test environment -> exit 2 | 2 | 2 | ok |
| R2-4: p5_scan_run primary: exit 0, ONE sbatch call, exact vector (1 CPU, 4G, 01:00:00, --qos=nots_commons, --no-requeue, --export=NONE, no Sapphire Rapids constraint, logs on scratch) | --parsable --job-name=smcbvs_20261029T1500Z_prodH_...ome/New_Campaign/runs/20261029T1500Z_prodH primary | --parsable --job-name=smcbvs_20261029T1500Z_prodH_...ome/New_Campaign/runs/20261029T1500Z_prodH primary | ok |
| R2-4: the completion receipt names phase primary, the scan job id, scanner_exit 0, the table sha256 and row count (4), and the scanner's summary line (launchable=3 locked=0 invalid_inspect=0) | 0 | 0 | ok |
| R2-4/R2-9: the scan job's log is on SCRATCH (LOGROOT/p5_scan/); home holds only the table, the receipt and the job record (no .log); jobs.tsv gains p5scan_primary | 0 | 0 | ok |
| R2-4: a second call with a recorded scan job does NOT submit again: it re-verifies (exit 0, still one sbatch call) | 0 | 0 | ok |
| R2-4: a table changed after the scan (sha256/row count differ from the receipt) is NOT trusted: exit 4 | 4 | 4 | ok |
| R2-4: a receipt that names another job is NOT trusted: exit 4 | 4 | 4 | ok |
| R2-4: a scan table with no recorded scan job is never trusted or overwritten: exit 2, no sbatch | 2 | 2 | ok |
| R2-4: a scan job that FAILS (scanner exit 3) leaves no receipt: the run reports SCAN FAILED, exit 4 | 4 | 4 | ok |
| R2-4: --no-wait with the scan job still running: exit 10, job recorded, nothing else | 10 | 10 | ok |
| R2-4: p5_submit while the recorded scan job is still running waits, then exits 10 (the job is reused, nothing resubmitted, no P5 array) | 10 | 10 | ok |
| R2-4: the scan job COMPLETED in sacct but wrote no table/receipt: not verified, exit 4 | 4 | 4 | ok |
| R2-4: p5_submit with that unverified scan job: refused (exit 2), the scan record is set aside as failed, no P5 array | 2 | 2 | ok |
| P5 refused when the scan and reconcile disagree on the resource_limit units -> exit 2, no P5 array, scan record retired | 2 | 2 | ok |
| P5: the table, receipt and job record of a refused attempt are all set aside (so the legitimate submission writes a fresh set) | 0 | 0 | ok |
| R2-4: P5 REFUSES while a resource_limit unit is locked (an attempt may have happened: an operator must inspect it) -> exit 2, no P5 array | 2 | 2 | ok |
| R2-4: P5 REFUSES while a resource_limit unit is incomplete (an attempt may have happened: an operator must inspect it) -> exit 2, no P5 array | 2 | 2 | ok |
| R2-4: P5 REFUSES while a resource_limit unit is invalid_inspect (an attempt may have happened: an operator must inspect it) -> exit 2, no P5 array | 2 | 2 | ok |
| R2-4: a scan row with retry_state none but launchable FALSE is inconsistent -> refused, exit 2 | 2 | 2 | ok |
| P5 refused when a resource_limit unit already has a valid P5 retry (at most one attempt per unit, ever) -> exit 2 | 2 | 2 | ok |
| P5 --dry-run: all gates pass (the scan job ran and its receipt verified), prints the exact vector, no P5 array, no p5/ record, scan artefacts set aside | DRY-RUN sbatch --parsable --job-name=smcbvs_202610.../fx_rr/home/New_Campaign/runs/20261029T1500Z_prodH | DRY-RUN sbatch --parsable --job-name=smcbvs_202610.../fx_rr/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| R2-7: P5 array ACCEPTED (7016) but the jobs.tsv append fails -> exit 5, cancelled BY EXPLICIT ID (only 7016), p5/ABORTED.txt says 'scancel 7016 ok', no submitted.json | 5 | 5 | ok |
| R2-7: after the abort every further P5 submission is refused until HQ has looked at p5/ABORTED.txt -> exit 2, no new sbatch call | 2 | 2 | ok |
| R2-7: the scan job accepted but jobs.tsv fails -> the scan job is cancelled by explicit id (a cancel failure is recorded visibly), no P5 array | 2 | 2 | ok |
| P5 submission: exit 0 with exactly two more sbatch calls (the scan job, then ONE P5 array) | 0 | 0 | ok |
| P5 selection: only the three launchable resource_limit units, sorted, in p5/units.tsv (select on launchable == TRUE) | 1 p0500_S3_r009_c100|2 p1000_S2_r001_c100|3 p1000_S3_r004_c100 | 1 p0500_S3_r009_c100|2 p1000_S2_r001_c100|3 p1000_S3_r004_c100 | ok |
| P5 table: units.tsv carries dataset, scale, p and L per unit | p500 6300 p1000 24000 p1000 24000 | p500 6300 p1000 24000 p1000 24000 | ok |
| P5: exact sbatch vector (ONE array, one unit per task, 4G, wall 2L + margin = 13:36:00, --qos=nots_commons, --no-requeue, same constraint) | --parsable --job-name=smcbvs_20261029T1500Z_prodH_.../fx_rr/home/New_Campaign/runs/20261029T1500Z_prodH | --parsable --job-name=smcbvs_20261029T1500Z_prodH_.../fx_rr/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| P5: jobs.tsv gains the scan job and the p5 job; submitted.json and sbatch_args.txt recorded; the scan table, receipt and job record are kept | 0 | 0 | ok |
| Q2: timeout and infra_repeat units did NOT block P5; they are listed for HQ in p5_exceptions_for_HQ.tsv, are never selected, and are named in the submission output | 0 | 0 | ok |
| Q1: EVERY sbatch call of this fixture (rerun, scan jobs, P5 array) carries --qos=nots_commons | 0 | 0 | ok |
| second P5 submission refused: one P5 array per run, ever -> exit 2 | 2 | 2 | ok |
| P5 refused when a durable attempt record exists (even without submitted.json): a second attempt of a unit is impossible -> exit 2 (reason in the SCRATCH refusal log) | 2 | 2 | ok |
| P5 task 1 (p500): exact vector = primary CLI + --p5-retry with the PRIMARY --mem-gb 2 --hours 1.75 (the adapter doubles them) | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...ore/v2_2_1/core --mem-gb 2 --hours 1.75 --p5-retry | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...ore/v2_2_1/core --mem-gb 2 --hours 1.75 --p5-retry | ok |
| P5 task 2 (p1000): exact vector with --hours 6.666666667 --p5-retry | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...2_1/core --mem-gb 2 --hours 6.666666667 --p5-retry | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...2_1/core --mem-gb 2 --hours 6.666666667 --p5-retry | ok |
| P5 task 3: the child is SIGKILLed (exit 137): the task itself exits 0, writes the end record (exit 137, done false, lock_left true) and leaves the lock + temporary file in P5_retry/ | 0 | 0 | ok |
| P5 retry files are written to <case>/P5_retry/ (outside the primary files) and the primary record is untouched | 0 | 0 | ok |
| P5 task run a SECOND time for the same unit: refused by the attempt record (exit 0, no Rscript call, refusal logged) | 0 | 0 | ok |
| the SIGKILLed P5 unit is never relaunched (a second task for it: refused, no Rscript call) | 0 | 0 | ok |
| reconcile after P5: the 'p5' section reports two valid retries and the killed one as incomplete; the primary classes are those of the rerun-complete state | 0 | 0 | ok |
| p5_scan_run final (a scan job again): every selected unit has a valid retry record or is REPORTED (2 valid, 1 reported: the SIGKILLed unit); the NOTE names cleanup_terminal.sh | 0 | 0 | ok |
| p5_scan_run final again: the recorded job is re-verified, not resubmitted (exit 0) | 0 | 0 | ok |
| p5_scan_run final: an existing scan table without its job record is never overwritten: exit 2 | 2 | 2 | ok |
| **final accounting** |
| final_accounting refuses while a job is still in the queue: exit 1 | 1 | 1 | ok |
| final_accounting: a task that sacct still shows RUNNING -> NOT TERMINAL, exit 1 | 1 | 1 | ok |
| final_accounting: a recorded job (the P5 array) missing from the snapshot -> exit 2 (never silent) | 2 | 2 | ok |
| final_accounting: terminal snapshot of EVERY job id written (home and logs folder) | 0 | 0 | ok |
| final_accounting: core-hours by array (precompile 0.08, p1000 1.0, p500 0.5, reruns 0.5, P5 3.5 CPU-h, scan jobs 12 x 300 s) and the two ceilings (native-fit-budget 10,100; requested-wall 10,540 / 10,541) | 0 | 0 | ok |
| **cleanup_terminal.sh: SIGKILLed P5 attempt -> final scan -> cleanup -> manifests (R2-5, R2-6)** |
| R2-5: cleanup REFUSES while a recorded job is still queued/running -> exit 2, the lock and the temporary file are untouched | 2 | 2 | ok |
| R2-5: cleanup REFUSES when sacct shows a task that is not terminal -> exit 2, nothing touched | 2 | 2 | ok |
| R2-5: cleanup REFUSES when a recorded job is missing from sacct (state unknown, fail closed) -> exit 2 | 2 | 2 | ok |
| R2-5: cleanup REFUSES when squeue fails (fail closed) -> exit 2 | 2 | 2 | ok |
| R2-6: make_manifests with the killed attempt's lock/temporary file in the LATER folder (p1000): refused (exit 2), names cleanup_terminal.sh, and NOTHING was written: no manifest in p0500, p1000 or logs, no summary, no home manifest | 2 | 2 | ok |
| R2-5: cleanup --dry-run lists both artefacts as WOULD ARCHIVE (proven stale: P5 attempt record of this run's array), moves nothing | 0 | 0 | ok |
| R2-5: cleanup archives the lock (with owner.txt) and the temporary file under LOGROOT/cleanup/<utc>/, CLEANUP_LOG.tsv, a small receipt in home; they are gone from the results tree | 0 | 0 | ok |
| R2-5: the durable attempt records are kept (same file count, the killed unit's start/end records included), the other P5 retries and all result files are untouched, and NO fit was relaunched | 0 | 0 | ok |
| R2-5: a second cleanup finds nothing left (exit 0, idempotent) | 0 | 0 | ok |
| R2-5: an artefact that is NOT proven stale (a P5 lock of a unit p5_submit never selected, no attempt record) is reported, left untouched, exit 3 | 3 | 3 | ok |
| R2-6: make_manifests still refuses while an unproven artefact remains, and writes nothing | 2 | 2 | ok |
| **make_manifests.sh: transactional, safe to rerun (R2-6), home manifest (R2-9)** |
| make_manifests refuses while a job is queued -> exit 2 | 2 | 2 | ok |
| make_manifests refuses with an unfinished lock directory under a result folder -> exit 2, no manifest written | 2 | 2 | ok |
| make_manifests: one manifest per folder (p0500, p1000, logs/<RUN_ID>), self-checked, then the full summary.tsv; nothing deleted | 0 | 0 | ok |
| manifest paths are relative to the folder (no leading ./ or /); P5_retry files (also the archived evidence under logs/cleanup) are inside the manifests; accounting is in the logs manifest | 0 | 0 | ok |
| manifest round trip: the three downloaded copies verify with sha256sum -c (mirrors C:\...\NOTS Data\New_Campaign\results\<RUN_ID>\p0500 etc.) | 0 | 0 | ok |
| manifest round trip: a tampered result file FAILS the check | 1 | 1 | ok |
| manifest round trip: a missing result file FAILS the check | 1 | 1 | ok |
| manifest round trip: a tampered log/attempt file FAILS the check | 1 | 1 | ok |
| R2-9: HOME_MANIFEST.sha256 covers the small home summaries (tables, receipts, reconcile/scan/P5/accounting/cleanup/manifest files) but not runner/ and not itself | 0 | 0 | ok |
| R2-9: the downloaded home summary folder (without runner/) verifies with sha256sum -c HOME_MANIFEST.sha256 | 0 | 0 | ok |
| R2-9: a tampered home summary file FAILS the home manifest check | 1 | 1 | ok |
| R2-9: after the whole run the home folder holds NO execution log (no *.log, *.jsonl, *.err, *.out outside runner/); the scan, refusal, locks and scheduler logs are all on scratch | 0 | 0 | ok |
| R2-6: rerunning make_manifests on an unchanged tree is safe: exit 0, every manifest 'reused' (revalidated, not replaced), the summary and the home manifest are identical | 0 | 0 | ok |
| R2-6: recovery after a partial pass (logs manifest and the summary missing): exit 0, p0500 and p1000 reused, logs rebuilt, the summary rebuilt IN FULL (4 lines) | 0 | 0 | ok |
| R2-6: an existing manifest that no longer matches its folder (a file added) is never replaced silently: exit 2, every manifest unchanged | 2 | 2 | ok |
| R2-9: a home summary changed after HOME_MANIFEST.sha256 was written: refused (exit 2), the home manifest is not replaced | 2 | 2 | ok |
| **cleanup_terminal.sh: SIGKILLed PRIMARY attempts (task.sh), unproven and live-owner artefacts (R2-5)** |
| primary task with SIGKILLed children (exit 137): the task exits 0; both units leave SMCBVS.lock (foreign host: task.sh does not remove it) and a temporary file | 0 | 0 | ok |
| R2-5: primary cleanup archives the proven-stale locks and temporary files (attempt records of this run's array), reports the lock of a unit with NO attempt record as UNPROVEN and leaves it: exit 3 | 3 | 3 | ok |
| R2-5: the primary attempt records are kept (same count), no fit was relaunched, no sbatch call was made | 0 | 0 | ok |
| R2-5: a lock whose owner process is ALIVE on this host is reported UNPROVEN and left untouched: exit 3 | 3 | 3 | ok |
| R2-5: a temporary file inside a lock directory moves with it and is renamed; no *.tmp.* / *.lock name is left anywhere under results/ or logs/ | 0 | 0 | ok |
| **P5 with no resource_limit unit; staging** |
| P5 with no resource_limit unit: exit 0, the scan job runs, NO P5 array is submitted, 'none_eligible' recorded | 0 | 0 | ok |
| **Sol review 3: R3-1 unknown scheduler state is not failure, R3-2 guard inside the scan wrapper, R3-3 empty result folder** |
| R3-1: scan job ACCEPTED, then a transient squeue failure: p5_submit exits 2 (state UNKNOWN, 'RESUMED' announced), ONE sbatch, no scancel, no P5 array | 2 | 2 | ok |
| R3-1: after the outage the scan job record (id 7005), the table and the receipt are all KEPT in place and nothing was set aside (failed/refused/dryrun) | 0 | 0 | ok |
| R3-1: the repeat invocation RESUMES the same scan job 7005 (not resubmitted), verifies it and passes all gates (dry run, exit 0): still exactly ONE sbatch in total | 0 | 0 | ok |
| R3-1 setup: a direct scan primary submits ONE scan job and verifies it (exit 0) | 0 | 0 | ok |
| R3-1: sacct unreadable on a re-check: exit 11 (state unknown), the job record, table and receipt are kept, nothing resubmitted | 11 | 11 | ok |
| R3-1: squeue unreadable on a re-check: exit 11 as well, records kept | 11 | 11 | ok |
| R3-1: the next call (scheduler readable again) resumes the SAME job: exit 0, still one sbatch | 0 | 0 | ok |
| R3-1: scan job 7007 accepted, jobs.tsv append fails, cancel issued but squeue/sacct cannot prove it terminal: exit 11, cancelled BY EXPLICIT ID, p5_scan_primary.uncertain names the job, ABORTED says UNCERTAIN | 11 | 11 | ok |
| R3-1: while the earlier accepted job is not proven terminal (sacct unreadable) a new scan job is NOT submitted: exit 11, no new sbatch, marker kept | 11 | 11 | ok |
| R3-1: once squeue AND sacct prove the old job terminal the marker is set aside (.cleared_*) and ONE new scan job is submitted: exit 0 | 0 | 0 | ok |
| **Sol review 4: R4-1 overlapping scan calls (submission lock, exact-id retirement)** |
| R4-1: the submission lock is held by another call: the direct scan wrapper exits 12, NO sbatch, no job record, the lock is left to its owner | 12 | 12 | ok |
| R4-1: p5_submit while the lock is held: refused (exit 2), NO sbatch, nothing retired | 2 | 2 | ok |
| R4-1: overlapping direct scan + parent: exactly ONE sbatch in total; the first call (A) finishes its scan (exit 0); the parent (B) runs into the lock and refuses (exit 2) | 0 2 1 | 0 2 1 | ok |
| R4-1: after the overlap the job record names A's job 7009, it is in jobs.tsv once, and NOTHING was retired or cancelled | 0 | 0 | ok |
| R4-1: a later parent call RESUMES A's job 7009 (no new sbatch; dry run passes, exit 0); the dry run then retires exactly that proven-terminal job | 0 | 0 | ok |
| R4-1: nc_retire_scan with an id the record does not name (9999 vs 7009): returns 1, nothing retired | 1 | 1 | ok |
| R4-1: nc_retire_scan without an expected id: returns 1, nothing retired | 1 | 1 | ok |
| R4-1: nc_retire_scan of the recorded id while squeue still shows it LIVE: returns 1, nothing retired | 1 | 1 | ok |
| R4-1: nc_retire_scan of the recorded id once squeue AND sacct prove it terminal: returns 0 and the record is set aside (.failed_*) | 0 | 0 | ok |
| **Sol review 5: R5-1 retirement serialised with submission, R5-2 catchable signals during an in-flight sbatch** |
| R5-1: while retirement A holds the scan lock, a second retirement B of the same id is refused (1); a scan call C resumes and judges the recorded job 8000 (exit 4) and submits nothing | 1 4 9 | 1 4 9 | ok |
| R5-1: A completes (0): the record of the terminal job 8000 is set aside and the lock is released | 0 | 0 | ok |
| R5-1: a new scan C2 submits ONE job (7010) once the lock is free (exit 0) | 0 | 0 | ok |
| R5-1: a LATE retirement of the old id 8000 refuses (1): the record now names 7010, which survives untouched | 1 | 1 | ok |
| R5-2 (TERM): the wrapper is signalled while its sbatch is in flight: it ends non-zero and the lock with IN_FLIGHT (job name recorded) is KEPT, no job record | 0 | 0 | ok |
| R5-2 (TERM): the next scan call exits 12 (lock kept, IN_FLIGHT named in the message) and submits NOTHING: still one sbatch | 12 | 12 | ok |
| R5-2 (TERM): a retirement while the in-flight lock is held is refused (1), nothing moved | 1 | 1 | ok |
| R5-2 (HUP): the wrapper is signalled while its sbatch is in flight: it ends non-zero and the lock with IN_FLIGHT (job name recorded) is KEPT, no job record | 0 | 0 | ok |
| R5-2 (HUP): the next scan call exits 12 (lock kept, IN_FLIGHT named in the message) and submits NOTHING: still one sbatch | 12 | 12 | ok |
| R5-2 (HUP): a retirement while the in-flight lock is held is refused (1), nothing moved | 1 | 1 | ok |
| R5-2 (INT): the wrapper is signalled while its sbatch is in flight: it ends non-zero and the lock with IN_FLIGHT (job name recorded) is KEPT, no job record | 0 | 0 | ok |
| R5-2 (INT): the next scan call exits 12 (lock kept, IN_FLIGHT named in the message) and submits NOTHING: still one sbatch | 12 | 12 | ok |
| R5-2 (INT): a retirement while the in-flight lock is held is refused (1), nothing moved | 1 | 1 | ok |
| **Sol review 6: R6-1 nonzero sbatch status = acceptance UNKNOWN (fail closed)** |
| R6-1 (client status 143): the scheduler ACCEPTED a job but the sbatch client died before returning its id: wrapper exits 13 (UNKNOWN), lock + IN_FLIGHT KEPT with client_status 143, no job record | 13 | 13 | ok |
| R6-1 (client status 143): the next scan call exits 12 and submits NOTHING: exactly ONE acceptance in total, no replacement | 12 | 12 | ok |
| R6-1 (client status 137): the scheduler ACCEPTED a job but the sbatch client died before returning its id: wrapper exits 13 (UNKNOWN), lock + IN_FLIGHT KEPT with client_status 137, no job record | 13 | 13 | ok |
| R6-1 (client status 137): the next scan call exits 12 and submits NOTHING: exactly ONE acceptance in total, no replacement | 12 | 12 | ok |
| R6-1: sbatch exits 42 (a rejection, or a failed client): wrapper exits 13, lock + IN_FLIGHT kept with client_status 42 and its stderr; nothing submitted again | 13 | 13 | ok |
| R6-1: p5_submit when the scan's sbatch fails: refused (exit 2) naming 'wrapper exit 13' and the kept lock; nothing retired, no P5 array | 2 | 2 | ok |
| **Sol review 7: R7-1 a failed diagnostic append still ends in exit 13** |
| R7-1: accepted job, client exits 42 AND the append to IN_FLIGHT fails: the parent refuses (exit 2) naming 'wrapper exit 13' (not a guard refusal), the warning is printed, the lock and the IN_FLIGHT entry are kept | 2 | 2 | ok |
| R7-1: the next p5_submit is refused by the kept lock (exit 2), nothing submitted: exactly ONE acceptance, no P5 array | 2 | 2 | ok |
| R3-1 (rerun): an UNCERTAIN marker whose job is not proven terminal blocks every new rerun: exit 2, no sbatch | 2 | 2 | ok |
| R3-1 (rerun): once squeue AND sacct prove job 7999 terminal the marker is set aside and rerun.sh proceeds (nothing to rerun here: exit 0, no sbatch) | 0 | 0 | ok |
| R3-2: a direct FINAL scan with a DENYING guard (home would pass 9.6 GiB): exit 1, NO sbatch, no scan job record, the guard call is recorded in the guard receipt | 1 | 1 | ok |
| R3-2: a direct final scan with the guard that does not enforce the charter limits (7 GiB / 9 GiB): exit 1, NO sbatch | 1 | 1 | ok |
| R3-2: a direct PRIMARY scan with a denying guard: exit 1, NO sbatch, a guard receipt names the refusal | 1 | 1 | ok |
| R3-2: a direct final scan with an ALLOWING guard: exit 0, exactly ONE sbatch, guard receipt GUARD_CHECK_OK for the planned 5 MB, job record and jobs.tsv entry created | 0 | 0 | ok |
| R3-2: re-checking an existing scan job never resubmits and never calls the guard (denying guard, exit 0, same sbatch count, guard receipt unchanged) | 0 | 0 | ok |
| R3-3: first pass with an EMPTY p1000 folder (only an empty sub-folder): exit 0, MANIFEST.sha256 is a 0-byte file, summary records files=0 bytes=0, the log says so | 0 | 0 | ok |
| R3-3: REUSE after the commit: rerun on the unchanged tree with the empty folder: exit 0, p1000 manifest 'reused', summary and home manifest identical | 0 | 0 | ok |
| R3-3: why the bundle never runs 'sha256sum -c' on an empty manifest: it exits nonzero (no checksum lines) | 1 | 1 | ok |
| R3-3: the laptop acceptance check for an empty folder (0-byte MANIFEST.sha256 and no other file) passes on the downloaded copy | 0 | 0 | ok |
| R3-3: the laptop acceptance check FAILS when the downloaded empty folder gained a file | 1 | 1 | ok |
| R3-3: an empty folder that later gains a file is INCONSISTENT: exit 2, the 0-byte manifest and the summary are not replaced | 2 | 2 | ok |
| R3-3: a folder whose files were all removed after a NON-empty manifest was written is INCONSISTENT too (never silently treated as empty): exit 2 | 2 | 2 | ok |
| R3-3: with the file restored everything is 'reused' again (exit 0) | 0 | 0 | ok |
| stage_local refuses a non-empty output folder: exit 3 | 3 | 3 | ok |
| tar content: no .cpp_cache, no make_tables.py, no truth/inputs folders; runner (incl. p5_scan.sbatch, cleanup_terminal.sh), tables and the frozen tree are in | 0 | 0 | ok |
| tar round trip: the extracted tar passes sha256sum -c STAGED_SHA256.txt | 0 | 0 | ok |
| tar round trip: a modified runner file FAILS the staged-hash check | 1 | 1 | ok |
| tar round trip: a modified frozen-tree file FAILS the manifest check | 1 | 1 | ok |
