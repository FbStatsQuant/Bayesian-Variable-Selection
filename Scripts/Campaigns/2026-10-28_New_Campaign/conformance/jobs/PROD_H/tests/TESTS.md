# PROD-H developer tests (CONF-2b, 2026-10-29)

Developer tests only, run locally under Git Bash (`C:/Program Files/Git/bin/bash.exe`), `py -3` and R 4.4.1; **no SSH, no Slurm, no submission**. Sol reviews the bundle independently. Run everything with `bash tests/run_all.sh` (about 12 minutes; the 2,400-unit trees are fabricated several times). Logs in this folder: `summary.log`, `syntax.log`, `tables.log`, `py_tests.log`, `shell_tests.log` (+ `SHELL_TESTS.md`, per-step logs in `logs_shell/`), `cli_parser.log`.

## Result (final, after the Sol review-7 minor fixes and HQ D49: full run finished 2026-10-30T09:29:04Z, `conformance/work/conf2b_runs/prodh_20261030T1430Z/`, exit 0; per-finding cases in `../REVIEW2_FIXES.md` to `../REVIEW7_FIXES.md`)

| Suite | Cases | Result |
|---|---|---|
| `syntax.log`: `bash -n` on every script, Python compile of every `.py`, no CR characters | 27 | 27 PASS |
| `tables.log`: 1,200 datasets / 2,400 unique units, c100 before c050, p1000 = tasks 1-600, p500 = 601-1200, audit seeds | 1 | PASS |
| `test_py.py` (reconcile, C3 poll, accounting; scheduler replaced in process) | 51 | 51 PASS, 0 FAIL |
| `test_shell.sh` + `test_shell2.sh` (real runner scripts, real tables, real frozen v2.2.1 tree and manifest, stub `sbatch/squeue/sacct/scontrol/scancel/srun/Rscript`) | 229 | 229 PASS, 0 WRONG |
| `cli_parser.R`: the real `smcbvs_cli_args()` of `run_case.R` (R 4.4.1) parses the argument vectors RECORDED by `task.sh` and `p5_task.sh` (4 primary, 2 P5) and checks hours = L/3600, `--mem-gb 2`, no seed, no extra option | 6 vectors | PASS |

## What the shell suite covers (the requested list)

- **Exact vectors:** `submit.sh --dry-run` and the real call (precompile, p1000 array `1-600%30` 13:42:00, p500 array `601-1200%30` 03:52:00, every option); the `Rscript` vector of a p1000 task (`--hours 6.666666667`), a p500 task (`--hours 1.75`), both P5 tasks (`--p5-retry`, primary `--mem-gb 2 --hours`), the rerun vector, the P5 sbatch vector (13:36:00, 4G).
- **Refusals:** test hook; guard failure (current and superseded limits); manifest mismatch; unlisted file; staged-hash mismatch; missing manifest; pre-existing cache; existing scratch folder; own throttle > 100; throttle overflow from another queued SMC array, from an unlimited array, from running tasks, and squeue failure (fail closed); a queued job at P5 submit and at rerun; sacct non-terminal; unreconciled unit; scan/reconcile disagreement; existing retry record; second P5 submission; a durable attempt record; a second P5 attempt of the same unit (refused by `p5_task.sh`); manifest refusals (live job, stale lock, existing manifest).
- **Abort mid-chain:** sbatch fails at call 3, call 1, bad job id at call 2: exact-id `scancel` (7001 7002 / none / 7001), `SUBMISSION_ABORTED.txt`.
- **Reconciliation over fabricated trees** (`test_py.py`): completed, resource_limit, other native failure, escalated, infra, infra_repeat, hard timeout, Slurm TIMEOUT task, NODE_FAIL/missing (orphan), running, not_run, rerun-then-ok, stale lock, P5 reported separately.
- **C3 hold logic** (`test_py.py`): resource_limit / timeout in the first 200 finished -> HOLD of the two primary arrays only (no cancel, `HOLD.json`, request for HQ); 4 infra failures -> continue, 5 -> HOLD; failures after the 200th finished unit -> no trigger; fewer than 200 finished fires when certain; STILL_HELD; `HOLD_RELEASED.json`.
- **Rerun selection:** only `infra` / `orphan` / stale-lock units are selected; resource_limit, hard timeout, infra_repeat and done units are not; the rerun task skips ineligible units; a second `rerun.sh` finds nothing.
- **Manifest round trip:** `make_manifests.sh` + `sha256sum -c` on downloaded copies passes; a tampered result, a missing result and a tampered log each FAIL; staging tar round trip (tampered runner file and tampered frozen-tree file FAIL).

## Not covered (needs NOTS or the real stack)

- Real `sbatch`/`squeue`/`sacct` output formats, Slurm `ArrayTaskThrottle` display, `scontrol hold` semantics, the real guard script, Lmod/GCC/R modules, a real fit, `timeout` kill behaviour at L + 300 s (reconcile's reading of it is tested), `/proc` lock-owner check in `task.sh`, Linux `find -printf` on NOTS (GNU, used the same way in Git Bash).
- The real frozen `tools/p5_scan.R` on a real result tree (the shell suite stubs it with a fixture table; its column names are taken from the source).

## Case tables

### test_py.py

```
PASS  reconcile: completed unit -> done / ok
PASS  reconcile: native resource_limit -> done, outcome resource_limit (its own category, not method_failed)
PASS  reconcile: other native failure -> outcome method_failed
PASS  reconcile: escalated flag read from diag_codes
PASS  reconcile: attempt ended without .done -> infra (ever_infra)
PASS  reconcile: two failed attempts -> infra_repeat
PASS  reconcile: unit hard kill (exit 124, timed_out) -> timeout, not infrastructure
PASS  reconcile: attempt without end record, task running -> running
PASS  reconcile: never attempted and task still queued -> not_run
PASS  reconcile: failed attempt then ok in a rerun job -> done, ever_infra true
PASS  reconcile: global indices: p1000 tasks 1-600 and p500 tasks 601-1200 both classified
PASS  reconcile: missing outputs with Slurm State TIMEOUT -> timeout (reported, never an infrastructure rerun)
PASS  reconcile: missing outputs, no native status, NODE_FAIL / not queued -> orphan (infrastructure, rerunnable)
PASS  reconcile: orphan count = every unit not fabricated, not timeout
PASS  reconcile: stale lock kept while its task is live, cleared (and logged) once it is not
PASS  reconcile: P5 retry files (valid / incomplete) are reported under 'p5' and leave the primary classes and outcomes unchanged
PASS  reconcile: p5_reconcile.tsv written; the P5 job id is not part of the primary job list
PASS  poll: 250 clean finished units -> continue, no hold
PASS  poll C3: a resource_limit inside the first 200 finished -> HOLD of both primary arrays only
PASS  poll C3: never cancels; HOLD.json and a request for HQ are written
PASS  poll C3: a timeout inside the first 200 -> HOLD
PASS  poll C3: 4 infrastructure failures in the first 200 -> continue (limit is more than 4)
PASS  poll C3: 5 infrastructure failures in the first 200 -> HOLD
PASS  poll C3: failures AFTER the first 200 finished units are counted but do not trigger
PASS  poll C3: fewer than 200 finished units: fires as soon as it is certain (60 finished, one resource_limit)
PASS  poll C3: after a HOLD the next poll reports STILL_HELD and does not hold again
PASS  poll C3: HOLD_RELEASED.json acknowledges the unit; the poll returns to continue
PASS  poll: report carries finished / escalated / resource_limit / timeout / infrastructure counts per array
PASS  poll: every poll appends one JSON line to polls.jsonl
PASS  accounting: core-hour totals by array (p1000, p500, P5, precompile, reruns); steps excluded; MaxRSS from steps
```

### Shell suite (`SHELL_TESTS.md`; long vectors abbreviated)

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
| refusal: throttle overflow, another queued campaign SMC array %60 + our 100 > 100 -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: throttle overflow is reported as such | 0 | 0 | ok |
| refusal: a queued SMC array with NO throttle (unlimited) counts as over the limit (fail closed) | 2 | 2 | ok |
| refusal: 30 running tasks of another campaign SMC array + 100 > 100 -> exit 2, no sbatch | 2 | 2 | ok |
| refusal: squeue fails -> the throttle cannot be established -> exit 2 (fail closed), no sbatch | 2 | 2 | ok |
| a non-campaign array (name without 'smc') and a plain job do not count: dry run passes -> exit 0 | 0 | 0 | ok |
| **submit.sh: dry run and the exact argument vectors** | | | |
| dry run: exit 0, no sbatch call, nothing created (no launch, config.env, jobs.tsv, scratch folder) | 0 | 0 | ok |
| dry run: precompile vector (1 CPU, 4G, 01:00:00, sapphirerapids, --export=NONE, --no-requeue, account/partition commons) | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| dry run: p1000 array vector (tasks 1-600, %50, 2G, 13:42:00, afterok precompile, logs on scratch) | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| dry run: p500 array vector (tasks 601-1200, %50, 2G, 03:52:00, afterok precompile, logs on scratch) | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | DRY-RUN sbatch --parsable --account=commons --part...x_main/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
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
| abort: sbatch rejected at the 1st call -> exit 5, one attempt, no scancel | 5 | 5 | ok |
| abort: an unparsable sbatch answer (2nd call) -> exit 5, the first id is cancelled by explicit id | 5 | 5 | ok |
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
| fixture: 2,400-unit tree fabricated (ok default; infra, resource_limit, hard timeout, infra_repeat, stale lock, orphan, p500 resource_limit) | 0 | 0 | ok |
| rerun refused while a job of this run is queued/running -> exit 2, no sbatch | 2 | 2 | ok |
| rerun refused at a throttle overflow (another SMC array %95 + 10 > 100) -> exit 2, no sbatch | 2 | 2 | ok |
| rerun refused when the guard refuses -> exit 1, no sbatch | 1 | 1 | ok |
| rerun refuses a test hook in a non-test environment -> exit 2 | 2 | 2 | ok |
| rerun --dry-run selects exactly the infrastructure unit and the orphan (lock-held unit only warned), no sbatch, lock untouched | 0 | 0 | ok |
| rerun: real run exits 0 and clears the stale lock of the lock-held unit (logged), then selects it | 0 | 0 | ok |
| rerun: units.txt = infra + stale-lock + orphan units only (never resource_limit, timeout, infra_repeat, done) | p1000_S1_r001_c100
p1000_S5_r001_c100
p1000_S5_r002_c050 | p1000_S1_r001_c100
p1000_S5_r001_c100
p1000_S5_r002_c050 | ok |
| rerun: exact sbatch vector (one array over the GLOBAL task indices, %10, 4G because a step was OUT_OF_MEMORY, --no-requeue, same constraint) | --parsable --job-name=smcbvs_20261029T1500Z_prodH_...mpaign/runs/20261029T1500Z_prodH/rerun_1/units.txt | --parsable --job-name=smcbvs_20261029T1500Z_prodH_...mpaign/runs/20261029T1500Z_prodH/rerun_1/units.txt | ok |
| rerun: jobs.tsv gains rerun_1 with the new id | 7004 rerun_1 | 7004 rerun_1 | ok |
| rerun: the vector is recorded in rerun_1/sbatch_args.txt and the selection in selected.tsv | 0 | 0 | ok |
| rerun task: runs the listed unit once more (attempt 2, same seed: no seed argument) and leaves its c050 sibling alone | 0 | 0 | ok |
| rerun task: a unit with two failed attempts (infra_repeat) is NOT run again; the skip is logged | 0 | 0 | ok |
| rerun task: a unit that ended by hard timeout is NOT run again | 0 | 0 | ok |
| second rerun.sh after the rerun finished: nothing infra/orphan left (infra_repeat, timeout, resource_limit are not eligible) -> no sbatch | 0 | 0 | ok |
| **P5: one array over the eligible units, one attempt per unit, ever** |
| P5 refused while a job of this run is queued (the rerun array) -> exit 2, no sbatch | 2 | 2 | ok |
| P5 refused while a primary task is not terminal in sacct -> exit 2, no sbatch | 2 | 2 | ok |
| P5 refused while a unit is not reconciled (a fresh infrastructure failure awaiting its rerun) -> exit 2, no sbatch, no scan table | 2 | 2 | ok |
| P5 refused when the guard refuses -> exit 1, no sbatch | 1 | 1 | ok |
| P5 refuses a test hook in a non-test environment -> exit 2 | 2 | 2 | ok |
| P5 refused when the scan and reconcile disagree on the resource_limit units -> exit 2, no sbatch, scan table retired | 2 | 2 | ok |
| P5: the table of a refused attempt is renamed (so the legitimate submission can write a fresh one) | 0 | 0 | ok |
| P5 refused when an eligible unit already has a retry folder/record (an attempt may have happened) -> exit 2, no sbatch | 2 | 2 | ok |
| P5 --dry-run: all gates pass, prints the exact vector, no sbatch, no p5/ record, scan table set aside | DRY-RUN sbatch --parsable --job-name=smcbvs_202610.../fx_rr/home/New_Campaign/runs/20261029T1500Z_prodH | DRY-RUN sbatch --parsable --job-name=smcbvs_202610.../fx_rr/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| P5 submission: exit 0 with exactly one more sbatch call | 0 | 0 | ok |
| P5 selection: only the two resource_limit units, p500 first (sorted), in p5/units.tsv | 1 p0500_S3_r009_c100|2 p1000_S2_r001_c100 | 1 p0500_S3_r009_c100|2 p1000_S2_r001_c100 | ok |
| P5 table: units.tsv carries dataset, scale, p and L per unit | p500 6300 p1000 24000 | p500 6300 p1000 24000 | ok |
| P5: exact sbatch vector (ONE array, one unit per task, 4G, wall 2L + margin = 13:36:00, --no-requeue, same constraint) | --parsable --job-name=smcbvs_20261029T1500Z_prodH_.../fx_rr/home/New_Campaign/runs/20261029T1500Z_prodH | --parsable --job-name=smcbvs_20261029T1500Z_prodH_.../fx_rr/home/New_Campaign/runs/20261029T1500Z_prodH | ok |
| P5: jobs.tsv gains the p5 job; submitted.json and sbatch_args.txt are recorded; scan table kept | 0 | 0 | ok |
| P5 refused when a durable attempt record exists (even without submitted.json): a second attempt of a unit is impossible -> exit 2 | 2 | 2 | ok |
| P5 task 1 (p500): exact vector = primary CLI + --p5-retry with the PRIMARY --mem-gb 2 --hours 1.75 (the adapter doubles them) | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...ore/v2_2_1/core --mem-gb 2 --hours 1.75 --p5-retry | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...ore/v2_2_1/core --mem-gb 2 --hours 1.75 --p5-retry | ok |
| P5 task 2 (p1000): exact vector with --hours 6.666666667 --p5-retry | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...2_1/core --mem-gb 2 --hours 6.666666667 --p5-retry | Rscript --vanilla C:/Users/felip/AppData/Local/Tem...2_1/core --mem-gb 2 --hours 6.666666667 --p5-retry | ok |
| P5 retry files are written to <case>/P5_retry/ (outside the primary files) and the primary record is untouched | 0 | 0 | ok |
| P5 task run a SECOND time for the same unit: refused by the attempt record (exit 0, no Rscript call, refusal logged) | 0 | 0 | ok |
| reconcile after P5: 'p5' section reports both retries valid; the primary classes are those of the rerun-complete state | 0 | 0 | ok |
| p5_scan_run.sh final: every selected unit has a valid retry record or is REPORTED (1 valid, 1 reported) | 0 | 0 | ok |
| p5_scan_run.sh refuses to overwrite an existing scan table: exit 2 | 2 | 2 | ok |
| **final accounting and download manifests** |
| final_accounting refuses while a job is still in the queue: exit 1 | 1 | 1 | ok |
| final_accounting: a task that sacct still shows RUNNING -> NOT TERMINAL, exit 1 | 1 | 1 | ok |
| final_accounting: a recorded job (the P5 array) missing from the snapshot -> exit 2 (never silent) | 2 | 2 | ok |
| final_accounting: terminal snapshot of EVERY job id written (home and logs folder) | 0 | 0 | ok |
| final_accounting: core-hours by array (precompile 0.08, p1000 1.0, p500 0.5, reruns 0.5, P5 3.0 CPU-h) | 0 | 0 | ok |
| make_manifests refuses while a job is queued -> exit 2 | 2 | 2 | ok |
| make_manifests refuses with an unfinished lock directory under a result folder -> exit 2, no manifest written | 2 | 2 | ok |
| make_manifests: one manifest per folder (p0500, p1000, logs/<RUN_ID>), self-checked; nothing deleted | 0 | 0 | ok |
| manifest paths are relative to the folder (no leading ./ or /); P5_retry files are inside the p0500/p1000 manifests; accounting is in the logs manifest | 0 | 0 | ok |
| manifest round trip: the three downloaded copies verify with sha256sum -c (mirrors C:\...\NOTS Data\New_Campaign\results\<RUN_ID>\p0500 etc.) | 0 | 0 | ok |
| manifest round trip: a tampered result file FAILS the check | 1 | 1 | ok |
| manifest round trip: a missing result file FAILS the check | 1 | 1 | ok |
| manifest round trip: a tampered log/attempt file FAILS the check | 1 | 1 | ok |
| make_manifests refuses to overwrite existing manifests -> exit 2 | 2 | 2 | ok |
| **P5 with no resource_limit unit; staging** |
| P5 with no resource_limit unit: exit 0, no array submitted, 'none_eligible' recorded | 0 | 0 | ok |
| stage_local refuses a non-empty output folder: exit 3 | 3 | 3 | ok |
| tar content: no .cpp_cache, no make_tables.py, no truth/inputs folders; runner, tables and the frozen tree are in | 0 | 0 | ok |
| tar round trip: the extracted tar passes sha256sum -c STAGED_SHA256.txt | 0 | 0 | ok |
| tar round trip: a modified runner file FAILS the staged-hash check | 1 | 1 | ok |
| tar round trip: a modified frozen-tree file FAILS the manifest check | 1 | 1 | ok |
