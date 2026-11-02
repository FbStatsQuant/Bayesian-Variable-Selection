# PROD-H: regime-H production job (SMC-BVS v2.2.1, 2,400 fits) — REVIEWED (Sol reviews 2–7; HQ D48/D49) — for HQ, then OPS

Bundle: `conformance/jobs/PROD_H/`. Written by CONF-2b (Sonnet worker) on 2026-10-29 by completing Terra's two partial drafts; **revision 4** adds the Sol review-4 fix R4-1 (one scan submitter; exact-id retirement; `REVIEW4_FIXES.md`); revision 3 fixed Sol's review 3 (`conformance/review/CONF2B_REVIEW3_sol.md`, findings R3-1 scheduler-query failure is not a scan failure, R3-2 disk guard inside the scan wrapper, R3-3 empty result folder; the item-by-item map is `REVIEW3_FIXES.md`) on top of **revision 2**, which fixed Sol's review 2 (`conformance/review/CONF2B_REVIEW2_sol.md`, findings R2-1, R2-4 to R2-10 and the answers to the builder's questions; map `REVIEW2_FIXES.md`). Developer tests only (`tests/TESTS.md`); no SSH was opened, nothing was submitted, and nothing under `code/` was edited. **Do not stage or submit before Sol's re-review and HQ's GO** (and the frozen manifest `code/core/v2_2_1.SHA256SUMS`, which may still be regenerated once: it is read from disk everywhere, never hard-coded).

## 1. What this job is

Rerun of regime H with the frozen v2.2.1 code: 1,200 datasets (p in {500, 1000} x S1-S6 x r001-r100), each at c100 then c050 = **2,400 fits**, one fit per `run_case.R` call, seeds derived by the adapter (never passed; method seed = data seed + 4,000,000). Policy: GO_2400 C1-C5 (allocation, node pin, stop rule, rerun machinery, resource_limit category) as amended by DECISIONS D10, D11 (P5), D19, D20, D21.

| Item | Value |
|---|---|
| Study (read only) | `/projects/ml75/fb31/BVS/bench20261019` (`manifests/inputs_manifest.csv`, `inputs/p0500|p1000/*.rds`) |
| Code | `/home/fb31/projects/BVS/New_Campaign/code/core/v2_2_1/` + `.../code/core/v2_2_1.SHA256SUMS` (verified at staging, before every submit and in every task: `sha256sum -c`, no unlisted file except `core/.cpp_cache`) |
| Environment | `runner/env.sh` (Lmod init, GCC/14.3.0, R/4.5.2, one thread everywhere) = the CONF_NOTS_IDENTITY environment |
| Run ID | `<STAMP>_prodH`, STAMP = YYYYMMDDTHHMMZ (UTC), chosen at staging |
| Arrays | precompile (job 1) -> **p1000 array, global tasks 1-600** and **p500 array, global tasks 601-1200**, both `afterok` the precompile; one task = one dataset = c100 then c050 |
| Allocation (C1) | p500 L = 6,300 s (`--hours 1.75`), p1000 L = 24,000 s (`--hours 6.666666667`); `--mem-gb 2`; Slurm 1 CPU, `--mem=2G` |
| Task wall | p500 **03:52:00**, p1000 **13:42:00** = 2 x (L + 300 s hard-limit margin + 60 s KILL grace) + 600 s once per task for module load, frozen check, hashing. The 300 s margin lets a fit that stops at L (the core's own guard) finish writing; `timeout` kills a fit at L + 300 (then KILL after 60 s). |
| Slurm options (every job) | `--account=commons --partition=commons --qos=nots_commons --export=NONE --no-requeue`; the compiled-core jobs (precompile, primaries, reruns, P5) also `--constraint=sapphirerapids`; `--chdir`/`--output`/`--error` under scratch logs |
| Throttle | **default 30 + 30 (HQ D49)**: 60 one-CPU tasks = **120 billed CPUs** (NOTS bills a 1-CPU task as 2). The campaign's combined ceiling is **192 billed CPUs** (D47): with PROD-L capped at 68 billed CPUs (34 tasks) the total is 188. OPS may raise PROD-H's throttles once PROD-L has finished, with `scontrol update JobId=<array id> ArrayTaskThrottle=<N>` on each PROD-H array, keeping the billed total of ALL campaign arrays <= 192 (at most 96 one-CPU tasks). Every submitting script (`submit.sh`, `rerun.sh`, `p5_submit.sh`) counts **ALL array jobs of fb31, whatever their name** (running tasks, or the `%N` of a pending array; an array with no `%N` counts as unlimited) and refuses unless (queued arrays + the new array) <= 100 TASKS; **this task guard counts PROD-L's array tasks too** (all fb31 arrays). 100 tasks would be 200 billed CPUs, so the 192-billed ceiling is the binding limit and is an OPS check when raising throttles. Any squeue failure or unparsable id refuses (fail closed). Plain (non-array) jobs are not arrays. |
| P5 (D11) | after both primary arrays are terminal and reconciled: a guarded 1-CPU **scan job** (section 3 F), then one array over the `launchable` `resource_limit` units only, same CLI + `--p5-retry`, PRIMARY `--mem-gb 2 --hours L/3600` (the adapter doubles them), Slurm `--mem=4G`, wall 2L + margin (**13:36:00** if any p1000 unit, 03:46:00 if only p500), one unit per task, **at most one attempt per unit, ever** |

Disk and log locations (charter section 2: home = code, manifests and small summaries; ALL logs on scratch):

| Where | What |
|---|---|
| **Scratch** `/scratch/fb31/New_Campaign/logs/<RUN_ID>/` (`LOGROOT`) | Slurm `.out/.err` (`slurm/`), scheduler stderr of every `sbatch` (`submit/`), `polls.jsonl` (one JSON line per poll), the scan job logs (`p5_scan/`), `refusals.log` (before the launch: `logs/_refusals/<RUN_ID>.log`), `locks_cleared.jsonl`, attempt records (`attempts/`, `p5_attempts/`), precompile record, `cleanup/<utc>/` (archived stale locks and temporary files), `accounting/` copy, `MANIFEST.sha256` |
| **Scratch** `/scratch/fb31/New_Campaign/results/<RUN_ID>/p0500|p1000/<case_id>/` | `SMCBVS.{rds,csv,sha256,done}`; P5 files in `P5_retry/SMCBVS_p5retry.*` |
| **Home** `/home/fb31/projects/BVS/New_Campaign/runs/<RUN_ID>/` | staged scripts and tables (about 1 MB), `config.env`, `jobs.tsv`, `launch/`, `manifest.json`, `precompile.ok`, small state and summaries only: `reconcile.tsv`, `poll_latest.json`, `hold_state.json`, `HOLD*.json`, `HQ_REQUEST_*.md`, `URGENT_HOLD_FAILED*.md`, `p5_scan_<phase>.{tsv,receipt,job}`, `p5/`, `p5_final_report.tsv`, `p5_exceptions_for_HQ.tsv`, `rerun_N/`, `accounting/`, `cleanup/` (receipts), `manifests/`, `HOME_MANIFEST.sha256`. No log of any kind is written to home (checked by the tests). |

Home budget: about 1 MB staged + 2-5 MB compile cache + under 25 MB summaries; the guard is asked for 30 MB.

Categories (each unit lands in exactly one): `done` (outcome `ok` / `resource_limit` / `method_failed`), `timeout` (unit hard kill or Slurm task State TIMEOUT: reported and held, **no automatic rerun**), `infra` / `orphan` (node failure, OOM-kill outside the fit, missing outputs with no native status, exit 1: **one** rerun by `rerun.sh`, same seed), `infra_repeat` (second failure: reported to HQ), `running` / `not_run` / `rerun_queued` (not finished). A native `resource_limit` is its own category (C5), never a failure; it is the only input of P5.

## 2. Inputs
- `tables/units.tsv` (2,400 fits), `tables/chunks.tsv` (1,200 datasets; task 1-600 = p1000, 601-1200 = p500).
- `runner/` (frozen into the run folder at staging), the frozen tree + manifest from `code/core/`.
- On NOTS: the read-only study above; OPS guard `/home/fb31/projects/BVS/New_Campaign/code/ops/guard.sh` (campaign <= 0.5 GiB, home <= 9.6 GiB; checked by `guard_check.sh` before every submission).

## 3. Commands for OPS, in exact order

`STAMP` is given by HQ (YYYYMMDDTHHMMZ). `RUN_ID=${STAMP}_prodH`. One ssh connection at a time, batched, through the alias `ssh nots` only (charter section 3).

**A. Laptop (Git Bash): build and verify the upload tar.**
```
cd "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/conformance/jobs/PROD_H"
bash stage_local.sh --stamp $STAMP --out "<empty folder, e.g. C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/runs/${STAMP}_prodH/bundle>"
```
It checks the tables, the frozen tree against `v2_2_1.SHA256SUMS` (no unlisted file), `bash -n`/Python compile, builds `prodH_bundle_$STAMP.tar`, extracts it and re-checks `STAGED_SHA256.txt`. It prints the tar's sha256.

**B. NOTS, connection 1: upload target, extract, verify (nothing is overwritten).**
```
ssh nots 'mkdir -p /scratch/fb31/New_Campaign/upload'
scp prodH_bundle_$STAMP.tar nots:/scratch/fb31/New_Campaign/upload/
ssh nots 'cd /scratch/fb31/New_Campaign/upload && sha256sum prodH_bundle_'$STAMP'.tar'        # compare with the tar's sha256 from step A
ssh nots 'NC=/home/fb31/projects/BVS/New_Campaign; RUN_ID='$STAMP'_prodH; cd $NC && test ! -e runs/$RUN_ID &&
  tar -xf /scratch/fb31/New_Campaign/upload/prodH_bundle_'$STAMP'.tar -C . --skip-old-files &&
  sha256sum --quiet -c runs/$RUN_ID/STAGED_SHA256.txt && (cd code/core/v2_2_1 && sha256sum --quiet -c ../v2_2_1.SHA256SUMS) && echo STAGED_OK'
```
(`--skip-old-files`: if `code/core/v2_2_1` is already on NOTS, the existing files are kept and the two `sha256sum -c` steps decide whether they are the frozen ones.)

**B2. NOTS: confirm the QoS exists BEFORE the dry run (Sol's answer to Q1).** Every job of this bundle (precompile, primaries, reruns, P5 scan job, P5 array) carries `--qos=nots_commons`, as the historical production run did. OPS confirms that the QoS exists for fb31 and records the output in the launch notes:
```
ssh nots 'sacctmgr -nP show assoc where user=fb31 format=Account,Partition,QOS; sacctmgr -nP show qos format=Name,MaxJobsPU,MaxSubmitPU | grep -i nots_commons'
```
If `nots_commons` is not listed for account `commons`, **stop and tell HQ** (do not remove the option or submit without HQ's decision).

**C. NOTS, connection 2: dry run, then submit.** The dry run checks the guard, the frozen tree, the tables, the study and the combined throttle (all fb31 arrays), prints the three exact `sbatch` vectors, and creates nothing.
```
R=/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_prodH
bash $R/runner/submit.sh --dry-run
bash $R/runner/submit.sh            # precompile -> p1000 array -> p500 array; all-or-abort, cancel by explicit id; launch record in $R/launch/
```
Exit 0 = submitted; 1 = guard refused; 2 = another refusal (the reason is printed and appended to the SCRATCH refusal log `/scratch/fb31/New_Campaign/logs/_refusals/<RUN_ID>.log`); 5 = abort: **any** failure after an accepted `sbatch` (rejected call, bad job id, a failed write of `jobs.tsv`, the sbatch vector record or `manifest.json`) cancels every id submitted so far, the accepted one included, BY EXPLICIT ID, records a cancel failure visibly in `launch/SUBMISSION_ABORTED.txt`, and retires the run ID: ask HQ for a new STAMP. Record the three job ids (also in `$R/jobs.tsv`). A pre-existing `core/.cpp_cache` is refused unless HQ instructs `--reuse-cache`.

**D. Stop rule (GO_2400 C3): OPS polls every 5 to 10 minutes for the whole of production, one ssh connection per poll.**
```
ssh nots 'R=/home/fb31/projects/BVS/New_Campaign/runs/'$STAMP'_prodH; python3 $R/runner/poll.py $R'
```
- **Cadence (R2-10).** "At most 10 minutes apart" is a maximum gap of **600 s**. OPS polls every 5 to 10 minutes (never more often than every 5 minutes: the one-connection rule). A gap of **more than 600 s** is LATE: it is flagged in the poll record (`late_poll`, `gap_s`, `late_polls_so_far`) and in the warnings, **at every poll for as long as any unit is running or queued** (not only in the first 200 units), and kept in `/scratch/fb31/New_Campaign/logs/<RUN_ID>/polls.jsonl`. A gap under 300 s is flagged `early_poll`. The monitoring responsibility is OPS's; the bundle has no scheduler. At the end of production run `python3 $R/runner/poll.py --cadence $R` (exit 1 and a list if a late gap occurred while production was active) and send the result to HQ.
- **What it reports:** finished / ok / escalated / resource_limit / timeout / infrastructure failures, per p and in total.
- **What it holds.** If, **inside the first 200 finished units**, there is any `resource_limit` or timeout, or **more than 4** infrastructure failures (the fixed form of "2 %": 4 of 200), the poll requests `scontrol hold` for each primary job (pending tasks only; running tasks go on; nothing is ever cancelled) and then CONFIRMS it from squeue (every pending task of the job shows a Held reason). Failures after the 200th finished unit are reported but never hold.
- **Hold states (R2-1).** Per job, persisted in `$R/hold_state.json` before the first `scontrol` call and again after the confirmation: `hold_requested` (a crash in between leaves this state; the next poll retries), `hold_established` (all pending tasks confirmed held), `hold_failed` (`scontrol` returned non-zero, or the confirmation shows pending tasks that are not held: a partial hold counts as failed), `hold_not_needed` (the job is terminal or has no pending task). While any job is not established every later poll retries the hold, the decision is `HOLD_FAILED`, **the poll exits with status 3**, and `$R/URGENT_HOLD_FAILED.md` is written. **Exit status 3 or that file means: pending tasks may still be launching after the mandatory stop. OPS runs `scontrol hold <jobid>` by hand for each job named in the file, confirms with `squeue -u fb31 -r -o '%i|%T|%r'` that every pending task shows `JobHeldUser`, and tells HQ at once. Never cancel running tasks.** The file is archived as `URGENT_HOLD_FAILED.resolved_<utc>.md` once the hold is established.
- **On `HOLD`/`STILL_HELD`:** send HQ `$R/HQ_REQUEST_<utc>.md` and wait. HQ's release = `scontrol release <jobid>` for each held job plus a `HOLD_RELEASED.json` listing the acknowledged `case_id`s in `$R`.

**E. When both primary arrays have left the queue (squeue shows no job of the run):**
```
R=...; python3 $R/runner/reconcile.py $R --sacct --full-verify          # re-hashes every rds/csv against its .done (about 4 GB; 1-3 min on the login node, as before)
column -t -s$'\t' $R/reconcile.tsv | awk 'NR==1 || $4!="done"' | head -50   # anything that is not done
bash $R/runner/rerun.sh --dry-run ; bash $R/runner/rerun.sh                 # only if infra/orphan units exist; repeat steps E/D after it finishes
```
`rerun.sh` refuses while any job of the run is queued, runs the guard, clears stale locks of dead units (logged to `LOGROOT/locks_cleared.jsonl`), and submits ONE array over the `infra`/`orphan` units (`%10`, `--no-requeue`, `--qos=nots_commons`, same constraint, same seed, 4G only if a step was OUT_OF_MEMORY). A unit is rerun at most once; timeouts, resource limits and second failures are never rerun. If `sbatch` accepts the array but the `jobs.tsv`/`submitted.json` write fails, the job is cancelled by explicit id (`rerun_N/ABORTED.txt`, exit 5).

**F. P5 (D11).** Gate (Q2 of Sol's review 2): P5 does **not** wait on units that are terminal, individually reconciled and reported as `infra_repeat` or `timeout`; it never retries them and never selects them (only primary `resource_limit` units are selected). P5 **still blocks** on any live job of the run and on any unit that is `running`, `not_run`, `rerun_queued`, `infra` or `orphan`. The `timeout`/`infra_repeat` units are listed in `$R/p5_exceptions_for_HQ.tsv` and printed by `p5_submit.sh`; **OPS sends that list to HQ before the real submission** and proceeds once HQ has acknowledged it (the script does not enforce the acknowledgement).
```
bash $R/runner/p5_submit.sh --dry-run        # optional: the scan job (below) + every gate + the exact vector; submits no P5 array (its scan artefacts are set aside)
bash $R/runner/p5_submit.sh                  # the real submission (writes p5_scan_primary.{tsv,receipt,job}, p5/units.tsv, p5/submitted.json)
```
- **The scan is a guarded compute job (R2-4).** The frozen `tools/p5_scan.R` hashes and deserializes every primary RDS (about 2,400 files, about 4 GB; Sol's laptop sample suggests minutes of CPU, not a metadata scan), so it never runs on the login node. `p5_submit.sh` calls `p5_scan_run.sh primary`, which submits `p5_scan.sbatch`: **1 CPU, `--mem=4G`, `--time=01:00:00`** (estimate 10 to 20 min; one record is held at a time, so memory is a few tens of MB; no Sapphire Rapids constraint is needed because no compiled core runs), `--qos=nots_commons --no-requeue --export=NONE`, logs in `LOGROOT/p5_scan/` and `LOGROOT/slurm/`. The job writes `p5_scan_primary.tsv` and then, only after verifying it, an immutable **completion receipt** `p5_scan_primary.receipt` (phase, job id, host, times, table sha256, row count, scanner exit 0, the scanner's summary line). The job id is recorded in `p5_scan_primary.job` and `jobs.tsv` (kind `p5scan_primary`). The wrapper trusts the table only if the job is COMPLETED in sacct **and** the receipt names the same phase and job **and** the sha256, row count, scanner exit and summary line all agree. A second call never resubmits a recorded scan job.
- **Disk guard inside the scan wrapper (R3-2).** The new-job branch of `p5_scan_run.sh` (direct `primary` and `final` calls included, not only the call made by `p5_submit.sh`) runs the charter-limit guard (`guard_check.sh` + the OPS `guard.sh`: home <= 9.6 GiB, campaign <= 0.5 GiB, limits confirmed from `guard.sh` itself) with a **planned allowance of 5 MB** for the home table, receipt and job record, **before** `sbatch`, and keeps the small receipt `p5_scan_<phase>.guard_receipt` (set aside with the other scan artefacts when a scan is retired). A refusing guard = **exit 1 and no `sbatch`**. Re-checking an existing recorded scan job never calls the guard and never resubmits.
- **A scheduler outage is not a scan failure (R3-1).** If `squeue` or `sacct` cannot be read while a scan job is being checked, the state of that job is UNKNOWN. `p5_scan_run.sh` then exits **11** ("SCHEDULER QUERY FAILED") and `p5_submit.sh` exits **2** saying the scan job is RESUMED next time; the recorded `p5_scan_<phase>.job`, table and receipt are **kept in place** and nothing is retired or resubmitted. Run the same command again once the scheduler answers: it resumes **the same job id** (one `sbatch` in total). A recorded scan job is set aside as `*.failed_<utc>` only when `squeue` (job absent) **and** `sacct` (terminal state) prove that it can no longer write, i.e. `p5_scan_run.sh` exit 4 (ended not COMPLETED, or COMPLETED but table/receipt do not verify) or exit 5 (accepted but not recordable; cancelled by explicit id **and** proven terminal). If an accepted scan/rerun/P5 job cannot be recorded and the cancel cannot be proven (scancel failed, or squeue/sacct unreadable or still showing it), the abort is **UNCERTAIN**: `p5_scan_<phase>.uncertain` (scan; wrapper exit 11), `rerun_N/UNCERTAIN` (rerun) or a note in `p5/ABORTED.txt` (P5 array; that file already blocks any relaunch until HQ has looked) is written and recorded visibly, and **no new scan job / rerun is submitted until `squeue` and `sacct` prove the old job terminal** (the marker is then set aside as `.cleared_<utc>`). If a marker keeps blocking: look at the named job with `squeue -u fb31` / `sacct -j <id>`, cancel it by hand with its explicit id if it is still shown, and run the command again.
- **One scan lock: submission and retirement (R4-1, R5-1, R5-2; Sol reviews 4 and 5).** Scan submission and scan retirement both take the atomic lock `RUN_DIR/p5_scan_<phase>.submit.lock` (its `owner.txt` names the holder and role). A call that overlaps exits **12** (`p5_submit.sh`: exit 2, "lock"); it submits nothing and retires nothing. Run it again a minute later. A recorded scan is set aside only by its exact job id, only when `squeue` AND `sacct` prove that id terminal, and only while the lock is held, so a late retirement can never move a newer scan's record. **Stale lock.** A lock without a running holder comes from a killed call. Process death alone does NOT make it safe to remove:
  0. **Exit 13 (R6-1, Sol review 6).** If `sbatch` itself exits nonzero while submitting a scan, the runner cannot tell a rejection from a client that died after the scheduler accepted the job. It therefore KEEPS the lock with `IN_FLIGHT` (which records `client_status` and the client's stderr), and exits 13 (`p5_submit.sh`: exit 2, "wrapper exit 13"). Resolve it exactly as in step 1.
  1. If `IN_FLIGHT` is present inside the lock, an `sbatch` was in flight and a scan job may have been ACCEPTED without its id being recorded (this is also what a TERM/HUP/INT during submission leaves, deliberately). Find it by name: `squeue -u fb31 -n <job_name from IN_FLIGHT> -h -o '%i %T'` and `sacct -u fb31 --name <job_name> -S <since_utc from IN_FLIGHT> -X -P -o JobID,State`. Cancel any such job by its explicit id (`scancel <id>`) and wait until sacct shows it terminal.
  2. **Unlock rule (Sol review 7, R7-2).** Remove the lock ONLY when ALL of these hold:
     (a) the submitting wrapper AND its sbatch client have finished (no such process on the login node);
     (b) every candidate job found by name since the IN_FLIGHT time is absent from squeue AND terminal in sacct (a found job is cancelled by explicit id first);
     (c) the outcome of the submission is positively resolved.
     One minute is only a retry interval: elapsed time, a failed query or a no-match result are NOT authorisation to unlock. A query that keeps failing, or a no-match that cannot be positively confirmed, leaves the lock in place and goes to HQ. Then delete `owner.txt` (and `IN_FLIGHT`), `rmdir` the lock, and rerun the command. Keep the squeue/sacct outputs and the resolution in OPS_LOG.
  3. Without `IN_FLIGHT`, no submission was in flight. Check that no call is running, then remove the lock the same way.
- **If `p5_submit.sh` exits 10** the scan job is still queued or running (the wrapper waits up to 30 minutes): run the same command again later; nothing is resubmitted. **Exit 2 saying the state of the scan job is UNKNOWN** = scheduler query failure or an unproven abort (see R3-1 above): nothing is retired, run it again. **Exit 2 with "the P5 scan job is proven terminal but did not complete or its table/receipt did not verify"** = the scan failed or did not verify (`p5_scan_run.sh` itself exits 4); the scan artefacts are set aside as `*.failed_<utc>` and HQ is told. Nothing is submitted. **Exit 1** = the disk guard refused.
- **Selection.** From the verified table: rows with primary `resource_limit`, base `SMCBVS`, and **`launchable == TRUE`**. The submission is REFUSED if any `resource_limit` unit is `locked`, `incomplete` or `invalid_inspect` (an attempt may have happened: an operator inspects it), if it already has a valid P5 retry, if the scan and reconcile disagree on the `resource_limit` units, or if a durable attempt record exists. A refusal after the scan sets the three scan artefacts aside as `*.refused_<utc>`. With no launchable unit it records `p5/none_eligible.json` and submits nothing.
- **The P5 array** runs `p5_task.sh`; its first action per unit is the noclobber attempt record in `logs/<RUN_ID>/p5_attempts/`, so a second attempt is refused. If `sbatch` accepts the array but the `jobs.tsv`/`submitted.json` write fails, the job is cancelled by explicit id, `p5/ABORTED.txt` records it (including a cancel failure), exit 5, and any further P5 submission is refused until HQ has looked at it.
- **After the P5 array has left the queue:**
```
bash $R/runner/p5_scan_run.sh final          # a second scan job (same resources) -> p5_scan_final.{tsv,receipt,job} + p5_final_report.tsv: every selected unit has a valid retry record or is REPORTED
python3 $R/runner/reconcile.py $R --sacct    # 'p5' section; the primary counts are unchanged
```
A P5 unit whose child was hard-killed appears as `locked`/`incomplete` and is REPORTED; it is never retried a second time. Its lock and temporary files are handled in G.

**G. Terminal accounting, clean-up of killed attempts, manifests (all jobs terminal):**
```
bash $R/runner/final_accounting.sh           # accounting/sacct_final.tsv (JobID,State,ExitCode,Elapsed,NodeList,MaxRSS,AllocCPUS,CPUTimeRAW) + core_hours.tsv/json (incl. the scan jobs); copied into the logs folder
bash $R/runner/cleanup_terminal.sh --dry-run ; bash $R/runner/cleanup_terminal.sh   # only needed if a killed attempt left a lock or temporary file (make_manifests.sh says so)
bash $R/runner/make_manifests.sh             # transactional, see below
```
- `cleanup_terminal.sh` (R2-5) refuses unless **every** job in `jobs.tsv` is out of the queue and terminal in sacct (any scheduler error refuses). It finds `*.lock` directories and `*.tmp.*`/`*.tmp` files under `results/<RUN_ID>`; an artefact is **proven stale** only if its unit has a durable attempt record whose array job is a job of this run (primary: `attempts/<case>/attempt_*.start.json`; P5: `p5_attempts/<case>.start.json` and the unit is in `p5/units.tsv`) and its owner is not a live process on this host. Proven artefacts are **archived** (moved, with `owner.txt`, to `LOGROOT/cleanup/<utc>/<relative path>.archived`, with `CLEANUP_LOG.tsv`; a small receipt goes to `$R/cleanup/`). Anything else is reported UNPROVEN, left untouched, exit 3. The durable attempt records and all result files are never touched (the count is checked before and after) and **no fit is ever relaunched**. `--dry-run` moves nothing.
- `make_manifests.sh` (R2-6) first **preflights all three folders** (existence, no `*.lock`/`*.tmp.*`/`*.tmp`, no live job, final accounting present) and writes nothing if any fails; then builds and self-checks every temporary manifest; an existing manifest is **revalidated** (must pass `sha256sum -c` and list exactly the files now present), never replaced silently; **an existing folder with no file at all (R3-3)** (for example a p1000 folder emptied by `cleanup_terminal.sh`, or a subgroup that failed entirely and exists only in the attempt logs and the terminal-exception lists) is recorded **explicitly as empty**: a `MANIFEST.sha256` of zero lines (a 0-byte file) and `files 0` / `bytes 0` for it in `manifests/summary.tsv` (the script also prints "EMPTY folder recorded explicitly"). Its membership is checked without `sha256sum -c` (which exits nonzero on a manifest without checksum lines): the manifest must be 0 bytes and the folder must hold no file other than `MANIFEST.sha256` (empty sub-folders do not count) - on the first pass, on a re-run and after the commit. An empty folder that later gains a file is INCONSISTENT and refused, and so is a folder whose files all disappeared after a non-empty manifest was written; then commits the new ones, rebuilds `manifests/summary.tsv` in full, and finally writes `HOME_MANIFEST.sha256`. It is safe to rerun after any failure (a later folder failing, an interrupted run): run the same command again.
- **Home run-summary manifest (R2-9).** `$R/HOME_MANIFEST.sha256` covers every file of the home run folder except `runner/` and itself (the downloaded summaries: tables, receipts, reconcile/scan/P5/accounting/cleanup/manifest files). It is a revalidated, never silently replaced, record.

**H. Download and verify (laptop), one folder at a time** (pull with the transfer helper of ops/transfer, or `scp -r`/`rsync` through `ssh nots`):
```
dest="C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign"
# results/<RUN_ID>/p0500, results/<RUN_ID>/p1000, logs/<RUN_ID>, and the home summary folder runs/<RUN_ID> (without runner/ and code)
cd "$dest/results/<RUN_ID>/p0500" && sha256sum --quiet -c MANIFEST.sha256 && echo OK p0500
cd "$dest/results/<RUN_ID>/p1000" && sha256sum --quiet -c MANIFEST.sha256 && echo OK p1000
cd "$dest/logs/<RUN_ID>"          && sha256sum --quiet -c MANIFEST.sha256 && echo OK logs
cd "$dest/runs/<RUN_ID>"          && sha256sum --quiet -c HOME_MANIFEST.sha256 && echo OK home-summaries
# A result folder that `manifests/summary.tsv` records with files = 0 (an EMPTY folder, 0-byte MANIFEST.sha256; R3-3) has NO checksum lines, so `sha256sum -c` exits nonzero on it.
# Its acceptance check is instead (shown for p1000; the same for p0500 / logs):
cd "$dest/results/<RUN_ID>/p1000" && test ! -s MANIFEST.sha256 && test -z "$(find . -type f ! -name MANIFEST.sha256)" && echo OK p1000 EMPTY
```
Also compare each downloaded `MANIFEST.sha256` hash with `$R/manifests/summary.tsv` (the hash of a 0-byte manifest is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). **Neither scratch nor the home run folder is pruned until all four verify locally**, by OPS, one folder at a time (no script of this bundle deletes anything; use the OPS verified-delete helper, or by hand):
```
rm -rf /scratch/fb31/New_Campaign/results/<RUN_ID>/p0500      # after OK p0500; same for p1000 and then logs/<RUN_ID>
rm -rf /scratch/fb31/New_Campaign/upload/prodH_bundle_<STAMP>.tar
```

## 4. Expected outputs and sizes
- 2,400 x {rds, csv, sha256, done}: about **4.0 GB** (the historical run's combined archive was 4,012,247,040 bytes; v2.2.1 adds `instrumentation` to each record, so a little more), plus P5 retry files (about 6 units, a few MB).
- Logs (scratch): 2,400 attempt records + R logs, Slurm outputs, `polls.jsonl` (a few MB), scan logs, precompile record: tens of MB.
- Home: `runs/<RUN_ID>/` staged scripts and tables about 1 MB; summaries (reconcile.tsv about 0.7 MB, verify_cache.json about 1 MB, accounting, manifests about 2 MB) under 25 MB; `core/.cpp_cache` 2-5 MB.
- Expected native statuses from the historical run: 2,394 ok-type, **6 `resource_limit`** (p1000 5, p500 1), 208 escalated; 0 timeout, 0 infrastructure. v2.2 ran 17-21% slower than v2.1 on two units (D20), so slightly more `resource_limit` is possible.

## 5. Memory and time per job
| Job | CPUs | Memory | Wall | Tasks |
|---|---|---|---|---|
| precompile | 1 | 4G | 01:00:00 | 1 |
| primary p1000 | 1 | 2G | 13:42:00 | 600 (%30, D49) |
| primary p500 | 1 | 2G | 03:52:00 | 600 (%30, D49) |
| rerun | 1 | 2G (4G after an OOM step) | 13:42:00 if any p1000 unit, else 03:52:00 | a handful (%10) |
| P5 scan (primary, final; plus one per `--dry-run`) | 1 | 4G | 01:00:00 (estimate 10-20 min) | 1 each |
| P5 | 1 | 4G | 13:36:00 if any p1000 unit, else 03:46:00 | about 6 (%min(N,10)) |

All carry `--qos=nots_commons --no-requeue --export=NONE`; all except the scan jobs also `--constraint=sapphirerapids`.

Wall-clock estimate (not a commitment): p1000 mean about 1,770 s per fit -> about 3,500 s per task -> 12 waves of 50 -> about 12 h plus the long tail (up to 13.7 h); p500 about 4 h; they run side by side. The queue wait on `commons` is unknown.

## 6. Core-hours
- **Native-fit-budget ceiling (primary fits): 10,100 core-hours** = p500 600 x 2 x 6,300 s = 2,100 h plus p1000 600 x 2 x 24,000 s = 8,000 h. This is the sum of the native fit budgets L; it excludes the 300 s + 60 s margins and the 600 s per-task overhead, so it is **not** what Slurm is asked for.
- **Requested-wall ceiling (primary arrays): 10,540 core-hours** = 600 x 03:52:00 = 2,320 h plus 600 x 13:42:00 = 8,220 h; **10,541** with the one-hour precompile request. Before reruns, the P5 scan jobs (at most 1 h each requested, about 0.2-0.4 h expected) and P5 (13.6 h per unit requested; about 70 core-hours expected for 6 units).
- **Expected from the historical runtimes** (`runtime_s` of the 2,400 laptop CSVs of the 2026-10-23 run, read for this estimate): p500 192.7 h, p1000 589.8 h = **782.5 core-hours**; with the +17-21% of D20 about **920**. P5: the historical 6 `resource_limit` units at 2L would cost at most 3.5 h + 5 x 13.3 h = **about 70 core-hours**.
- NOTS bills 2 logical CPUs per core (GATE_REVIEW_GO2400): billed CPU-hours are about twice these. `final_accounting.sh` reports both `alloc_cpu_hours` (Slurm's CPUTimeRAW) and `elapsed_core_hours` per group (primary p500, primary p1000, P5, P5 scan jobs, precompile, reruns), with `native_fit_budget_ceiling_core_hours` and `requested_wall_ceiling_core_hours` beside them.

## 7. Acceptance checks
1. `STAGED_OK`; the QoS check of B2 passed; `submit.sh --dry-run` exit 0; submission exit 0 with three job ids and `$R/launch/` complete (guard receipt, `sbatch_args.txt` with 3 vectors, `v2_2_1.SHA256SUMS` copy, config, effective environment).
2. `precompile.ok` exists and names the compile key; no array task compiled (task logs contain no compiler output).
3. After the primary arrays: `reconcile.py --sacct --full-verify` classes: **done 2,400** is the target; every other unit is listed with its category (timeout, infra_repeat) and reported to HQ. `outcomes` gives ok / resource_limit / method_failed separately; `escalated` is counted.
4. No unit `running`, `not_run`, `orphan`, `infra` or `rerun_queued` before P5 and at the end (terminal `timeout`/`infra_repeat` units may remain, reported to HQ).
5. The poll log `/scratch/fb31/New_Campaign/logs/<RUN_ID>/polls.jsonl` shows polls **5 to 10 minutes apart for as long as production was active** and `poll.py --cadence $R` reports `ok: true` (otherwise each late gap, > 600 s, is explained to HQ); no unacknowledged HOLD; no `URGENT_HOLD_FAILED.md` left unresolved.
6. P5: `p5_scan_primary.receipt` verified; `p5_scan_primary.tsv` lists the `resource_limit` units; `p5_final_report.tsv` shows every selected unit with a valid retry record or explicitly reported; each unit has exactly one entry in `logs/<RUN_ID>/p5_attempts/`; retry files exist only under `P5_retry/`.
7. `final_accounting.sh` exit 0 (every job terminal) and `core_hours.tsv` printed; compare with section 6 (both ceilings).
8. `cleanup_terminal.sh` (if needed) exit 0, or its UNPROVEN list explained to HQ; `make_manifests.sh` exit 0 (three folder manifests + `HOME_MANIFEST.sha256`); the four downloaded folders verify with `sha256sum -c`, **except a folder recorded as empty in `manifests/summary.tsv` (`files` = 0), whose laptop acceptance check is `cd <folder> && test ! -s MANIFEST.sha256 && test -z "$(find . -type f ! -name MANIFEST.sha256)" && echo EMPTY_OK`** (a 0-byte manifest and no other file; `sha256sum -c` is not used there); `ls` of `p0500` and `p1000` shows 600 case folders x 2 each (1,200 per p).
9. Home usage after the run: `guard.sh 0` prints OK and the campaign is below 0.5 GiB. `find $R -name '*.log' -o -name '*.jsonl'` (outside `runner/`) lists nothing: no log in home.

## 8. Clean-up
After H: delete the verified scratch folders and the uploaded tar (commands above). The frozen code tree and `core/.cpp_cache` stay in home (shared with later runs). `runs/<RUN_ID>/` keeps only summaries; after its download is verified against `HOME_MANIFEST.sha256`, HQ decides whether to prune it. Killed-attempt artefacts are archived, not deleted, by `cleanup_terminal.sh` (the archive is inside the logs folder and travels with it). Do not touch `~/.claude/remote`, `.t3-recovery`, or `/projects/ml75/fb31/BVS/bench20261019`.

## 9. Assumptions and open points for HQ / Sol
1. **QoS (Q1).** `--qos=nots_commons` is on every job; B2 makes OPS confirm that it exists for fb31 first. Omitting it is not demonstrated to be invalid, but the pilot's default is not proof of equivalent production scheduling policy.
2. **Cadence (R2-10).** The bundle has no scheduler: OPS owns the 5-to-10-minute polling; lateness (> 600 s) is detected and recorded at the next poll, so a missed poll is visible afterwards, not prevented.
3. **Throttle (R2-8).** Counts all fb31 arrays, whatever their name; an unknown array can therefore block a submission (inspect it, do not rename around it). PROD-L's arrays need no special name.
4. **P5 gate (Q2).** Terminal `timeout`/`infra_repeat` units do not block P5 but must be listed to HQ first (JOB.md F); the acknowledgement is procedural, not enforced by a script.
5. **Login-node load.** `reconcile --full-verify` still re-hashes about 4 GB on the login node (nice 19, a few minutes, run a few times); the P5 scan, which also deserializes every record, is a compute job. If HQ wants `--full-verify` as a job too, that is a separate change.
6. The `--hours` string is `L/3600` printed with 10 significant digits (`1.75`, `6.666666667`); the adapter hashes it into the unit identity, and the P5 call passes the identical string.
7. A Slurm TIMEOUT of a whole array task is classified `timeout` for every unit of that task that has no `.done`, including a second fit that never started.
8. A `--dry-run` of `p5_submit.sh` submits (and waits for) a real scan job; its artefacts are set aside, so the real call runs a second scan. Skip the dry run if HQ does not need to see the vector first.
9. The scan job's requested wall (01:00:00) is a ceiling of about 3x the estimate; if a real scan exceeds it the job TIMEOUTs, nothing is trusted, and HQ decides.
