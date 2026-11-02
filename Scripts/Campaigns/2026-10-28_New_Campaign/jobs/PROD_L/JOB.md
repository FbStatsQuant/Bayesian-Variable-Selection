# JOB: PROD-L on NOTS

**Status: PROD_L READY for OPS (2026-10-30).** Sol R1 REJECT → fixed; Sol R2 REJECT on class-(i) I1–I3 only → fixed; Sol narrow check `review/SOL_CHECK_PRODL_I1_I3.md`: I1–I3 RESOLVED. Class-(ii) items accepted under HQ D53 (§14): II1 failed initial P5 scan (removed by code: `--from-scan` any phase), II2 receipt after `recover_truth.sh` (Sol's procedure). Local evidence `tests/SUMMARY_r3_final.txt` (14 suites, 1,438 passed, 0 failed) and `tests/live/live_r1fix.out`. Stage with a fresh STAMP (the builder's test tar is not for deployment). For OPS via HQ; charter §6. `STAMP=YYYYMMDDTHHMMZ` UTC; `RID=<STAMP>_lowp_prodL`; `HOME_ROOT=/home/fb31/projects/BVS/New_Campaign`; `SCR_ROOT=/scratch/fb31/New_Campaign`; `RUN_HOME=HOME_ROOT/runs/<RID>`; `LOG_RUN=SCR_ROOT/logs/<RID>`. All bundle scripts on NOTS are under `RUN_HOME/code/prod_l/` (abbreviated `B` below); laptop bundle is `CAMP/jobs/PROD_L`. Use the configured `ssh nots` alias, one connection at a time, with batched commands; bundle scripts do not open SSH.

## 0. Charter limits

Campaign home footprint ≤ 0.5 GiB; total home usage < 9.6 GiB. OPS owns the guard, which must enforce both. All bulky results, logs, cache and temporary files are on scratch; the single owned stage and its small core compile cache are in home. Nothing shared is overwritten. The sealed study remains on the laptop. Follow charter §2–§3 and D31/D40.

## 1. Purpose and pieces

Produce 600 enum20, 600 enum30, 2,400 primary SMC, and 12,000 SMC repeat units on Sapphire Rapids, with P0a/P0b and truth-lock gates. Repeats use the frozen adapter's seeds; the primary and all five repeats are distinct. No benchmarks are included: `B/bench_hook/README.md` specifies the gated later wave. SMC uses frozen `RUN_HOME/code/core/v2_2_1` and its manifest; staging, submission, and each SMC task verify it.

## 2. Staging

Before staging run the OPS-owned `/home/fb31/projects/BVS/New_Campaign/code/ops/guard.sh 110` (`PLANNED_HOME_MB_STAGE`) and retain its receipt. **HQ D57: this is the only reservation of the stage**; after extraction `submit_prodl.sh --wave main` asks the guard only for the remaining growth (`PLANNED_HOME_MB_MAIN` = 10 MB: compile caches + bookkeeping). (The first deployment, run `20261030T1811Z_lowp_prodL`, still counted the stage twice; fixed after it.) On the laptop, use the sealed study and a durable output folder:

```bash
"C:/Program Files/Git/bin/bash.exe" "CAMP/jobs/PROD_L/stage_local.sh" --sealed "<PC_NOTS_DATA>/New_Campaign/inputs/lowp_study" --stamp <STAMP> --out "<durable-run-folder>"
```

Replace `CAMP` with `<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign`. Upload the tar and its SHA-256 file through the approved transfer workflow; verify the tar hash on NOTS before extraction. From `HOME_ROOT`, extract only after `test ! -e runs/<RID>` succeeds, then run `sha256sum --quiet -c runs/<RID>/STAGED_SHA256.txt` from `HOME_ROOT`. Preserve the local tar and hash. The tar contains one `runs/<RID>` tree, whole sealed study including production and dev truth, frozen code, and the bundle; the stage checks truth separation and frozen hashes.

## 3. OPS confirms `B/prodl.env`

Confirm `MODULES="GCC/14.3.0 R/4.5.2"` matches CONF's v2.2.1 build and the LOWP library paths supply Rcpp and digest. Confirm roots, OPS guard, ceilings, wall/budget and throttle constants. The benchmark library settings are unused. The driver records the effective environment, final env and hash, staged list, frozen manifest, owner, lists, JOB, guard and ceiling receipts, and exact sbatch vectors in `LOG_RUN/launch/<wave>/`.

## 4. Test hooks

Never set `PILOT_DRYRUN`, `PILOT_SKIP_MODULES`, `PILOT_TIME_BIN`, `PRODL_UNIT_CMD`, `PRODL_TEST_WALL_S`, `PRODL_TEST_BUDGET_S`, or `PRODL_TEST_NOW_OFFSET_S` for a real run. The driver requires `--local-test`, `PILOT_LOCAL_TEST=1` and a fake `NC_HOME_ROOT` for hooks; jobs refuse hooks outside local test.

## 5. OPS sequence

1. Guard before staging, stage, upload and verify as §2; confirm §3. In the commands below set `B=/home/fb31/projects/BVS/New_Campaign/runs/<RID>/code/prod_l` and export `STAMP=<STAMP>`.
2. `bash "$B/submit_prodl.sh" --wave main --profile alone --dry-run` (choose `withH` instead when appropriate), inspect guard, ceiling and sbatch vectors; then `bash "$B/submit_prodl.sh" --wave main --profile alone` using the same selected profile. Submission is all-or-abort with explicit cancellation on failure. Save launch receipts and job IDs.
3. On the laptop run `bash "CAMP/jobs/PROD_L/waiter.sh" <LOGFILE> <JOBIDS> [MAX_CHECKS]` with the wave's job ids (comma-separated, from `LOG_RUN/jobids.tsv`). **Exit 3 (EARLY_FAILURE) is triage only**: inspect the failed rows (Slurm outputs, ledger, unit logs); the rest of the wave keeps running, so restart the waiter as `bash "CAMP/jobs/PROD_L/waiter.sh" <LOGFILE> <JOBIDS> [MAX_CHECKS] --until-terminal`, which never exits early. **Exit 0 (ALL_TERMINAL)** or **exit 4 (ALL_TERMINAL_WITH_FAILURES)** means every requested job has complete terminal accounting; exit 2 means MAX_CHECKS was reached (restart it). Before reconciliation, stale cleanup or any later wave require waiter exit 0 or 4 AND `WAVE_UNLOCK_VERIFIED` in `LOG_RUN/truthlock/<wave>/WAVE_UNLOCK.txt`; failed units are then handled by reconciliation and the resubmission round (step 5). Do not run guard or `du` while locked; recover as §8.
4. After main is terminal and unlocked, inspect P0, lock/unlock, scheduler, and ledger evidence. Run `python3 "$B/reconcile_prodl.py" "$STAMP"`; inspect `RUN_HOME/inventory_final/INVENTORY.md` and the piece tables. `bash "$B/clear_stale.sh" "$STAMP"` lists stale files; after inspection, `bash "$B/clear_stale.sh" "$STAMP" --yes` moves them to logged cleanup evidence. Both gate on terminal jobs.
5. **Resubmission round rN (r1, then r2, …): build every list first, then submit once.** For a piece that is already CLOSED skip its line (the script refuses it). Run, one per line:
   `bash "$B/make_resubmit.sh" "$STAMP" enum20 r1`
   `bash "$B/make_resubmit.sh" "$STAMP" enum30 r1`
   `bash "$B/make_resubmit.sh" "$STAMP" smc r1`
   `bash "$B/make_resubmit.sh" "$STAMP" smcrep r1`
   Each prints `NOTHING_TO_RESUBMIT` or writes `RUN_HOME/resubmit/<piece>_r1.tsv` (and `<piece>_r1_exceptions.tsv`: units with two started attempts, never resubmitted; report them to HQ). Then submit ALL pieces that got a list in ONE command, e.g. `bash "$B/submit_prodl.sh" --wave r1 --profile alone --pieces enum20,smc` (`withH` while PROD-H runs). Wait (step 3) and verify the unlock; the next round uses a fresh wave name (r2), never r1 again.
6. Run `bash "$B/submit_prodl.sh" --p5-scan --phase initial`, wait for terminal, then `bash "$B/make_p5_list.sh" "$STAMP" --from-scan initial` and `bash "$B/make_p5_list.sh" "$STAMP" --wave p5`. Submit a nonempty list with `--wave p5`. For never-started units use `--wave p5r1` in both list and submit commands; attempted failures are HQ exceptions. After ANY fitting wave that follows the initial scan, run a new scan phase and `make_p5_list.sh --from-scan <phase>` again, then P5 waves for new units, then the final scan. Submit `--p5-scan --phase final` (or the next unused final phase) after all fitting waves and wait for completion.
7. Before PROD-H submission run `bash "$B/retune_throttle.sh" "$STAMP" --profile withH --yes`, then repeat `bash "$B/retune_throttle.sh" "$STAMP" --check-drained` until exit 0. PROD-H's separate task guard also applies. Once PROD-H has finished, the alone profile may be admitted.
8. **Close, pull, verify and delete each piece as soon as it is final (HQ D49; scratch is transient).** A piece is final when the run is idle (no job of the run queued or running) and `reconcile_prodl.py` shows every unit of that piece `done`: enum20 and enum30 normally right after the main wave; **smc and smcrep only after P5** (step 6: the scan reported and, if any unit was eligible, the P5 wave terminal), because P5 writes into their folders. For each final piece:
   - `bash "$B/make_manifests.sh" "$STAMP" --piece <enum20|enum30|smc|smcrep>`: refuses unless the run is idle and terminal, the folder holds no `*.lock`/`*.tmp*` (else `clear_stale.sh`), and every unit of the piece is `done` (exit 6 otherwise: resubmit first, or HQ acknowledges the exceptions and OPS adds `--allow-incomplete`). It writes `MANIFEST.sha256` in the piece's results folder, `RUN_HOME/manifests/<piece>.CLOSED`, `<piece>.inventory.tsv` (the authoritative inventory once the folder has left scratch) and updates `manifests/summary.tsv`. After closing, `make_resubmit.sh` and `submit_prodl.sh` refuse that piece (a deleted folder would otherwise look like 100 % missing).
   - On the laptop: `MSYS_NO_PATHCONV=1 py -3 ops/transfer/nots_pull.py "/scratch/fb31/New_Campaign/results/${STAMP}_lowp_${piece}" --delete`. Verify its manifest and retain the transfer receipt.
   - Run `bash "$B/final_accounting.sh" "$STAMP"`, close logs, then pull `"/scratch/fb31/New_Campaign/logs/${STAMP}_lowp_prodL"` with the same command and `--delete`. Pull each existing home folder without deletion using these explicit commands:
     `MSYS_NO_PATHCONV=1 py -3 ops/transfer/nots_pull.py "/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL/manifests"`,
     `MSYS_NO_PATHCONV=1 py -3 ops/transfer/nots_pull.py "/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL/inventory_final"`,
     `MSYS_NO_PATHCONV=1 py -3 ops/transfer/nots_pull.py "/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL/p5"`,
     `MSYS_NO_PATHCONV=1 py -3 ops/transfer/nots_pull.py "/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL/resubmit"`. The manifests folder contains JOBIDS.tsv.
9. After all results and logs have been pulled, run `bash "$B/cleanup_prodl.sh" "$STAMP"` for inspection, then `bash "$B/cleanup_prodl.sh" "$STAMP" --yes --receipt <local-evidence-path>` with a receipt path outside the removed tree, accessible to the command. Preserve the closure receipt locally and require `CLEANUP VERIFIED`.

## 6. Requests and dependencies

All use account/partition `commons`, constraint `sapphirerapids`; dependent jobs use `--kill-on-invalid-dep=yes`. Time is Slurm wall limit. One requested CPU bills as two.

| Step | Array alone / withH | CPUs | Memory | Wall | Dependency |
|---|---|---:|---:|---:|---|
| s0_build | — | 2 | 4G | 0:40 | — |
| s0_verify P0a + P0b | — | 1 | 2G | 0:30 | — |
| s0_truthlock | — | 1 | 2G | 0:30 | afterok verify |
| s0_lock | — | 1 | 1G | 0:10 | afterok truthlock |
| s1_enum20 | 1 / 1 | 4 | 1G | 1:00 | afterok build, verify, truthlock, lock |
| s1_enum30 | 0-23%4 / 0-23%2 | 16 | 1G | 0:45 | same |
| s2_smc | 0-95%32 / 0-95%16 | 1 | 2G | 5:00 | same |
| s3_smcrep | 0-479%32 / 0-479%16 | 1 | 2G | 5:00 | same; afterany smc |
| s8_unlock | — | 1 | 1G | 0:15 | afterany lock and fits |
| s9_collect | — | 1 | 1G | 0:15 | afterany build, verify, truthlock, unlock |
| s4_p5 | one per eligible unit, %min(N,8) / %min(N,4) | 1 | 4G | 9:00 | later wave lock chain |
| s5_p5scan | — | 1 | 2G | scales with the records scanned (HQ D63): max(2:00, 600 s + 2.0 s × (smc+smcrep units + rows of `p5/expected.tsv`)) = **8:10** for 14,400 primaries and no retry; each listed retry adds 2 s | after terminal reconciliation; no truth lock |

Later waves repeat truthlock → lock → arrays → unlock → collect. Billed peak is 132 alone, 68 withH; other work plus PROD-L must stay ≤ 192. `B/ceiling_check.py` refuses unsafe plans. Requested-wall ceilings: enum20 4, enum30 288, smc 960, smcrep 4,800, infrastructure approximately 6; total approximately 6,058 billed core-hours. P5: 16 is the nominal doubled core allocation (8 h × 2 billed); the wrapper bound is 29,160 s ≈ 16.2 core-hours; the requested-wall ceiling is 18 per unit.

## 7. Batch deadline

Before every unit, including the first, the runner requires time for the full hard unit budget, 60 seconds kill grace and 120 seconds commit margin before the deadline, itself 120 seconds before wall end (and at least 60 seconds before Slurm's end). Otherwise it records this and all remaining units as deferred. A started unit is wrapped in GNU `timeout` and GNU time. Deferred is not a task failure; timeout and unit failure wake the waiter.

## 8. Truth lock and recovery

Each wave tests both staged truth trees, saves pre-lock hashes in `LOG_RUN/truthlock/<wave>/evidence`, locks and verifies both mode 000 before fits, and unlocks only after all recorded fitting jobs across waves are inactive. The finalizer verifies hashes; if the lock never ran it verifies open trees against `STAGED_SHA256.txt`. If unlock fails or trees remain locked, inspect scheduler state; cancel only explicit run job IDs if needed, then `bash "$B/recover_truth.sh" "$STAMP"`. Recovery refuses active jobs or scheduler errors, restores and verifies both trees, and records the incident for HQ. Never run guard/du until restored.

## 9. Disk

Home stage and cache are approximately 100 MiB; the stage is reserved once before staging (110 MB), the main-wave submission then asks 10 MB, later waves 5 MB (D57). If guard refuses, use D31 archive-then-erase. D40's 9.70 GiB is a last resort and needs a recorded HQ decision applied in both OPS's `guard.sh` and `prodl.env` (`REQUIRED_HOME_LIMIT_KB=10171187`); `guard_check.sh` probes against the guard's own limit and still refuses any guard limit above `REQUIRED_HOME_LIMIT_KB`. Scratch results are approximately 6 GiB plus logs: smcrep alone is approximately 5.0 GiB. Pull each final piece promptly.

## 10. Core-hours

Expected billed usage is approximately 134 core-h, conservative 173, delay sensitivity 191; enum20 1.30, enum30 73.1, smc 10.9, smcrep 48.4 and infrastructure 0.2 expected. Estimates exclude P5 and benchmarks. Repeat estimates rest on two pilot fits per p; update from actual accounting. See `B/CORE_HOURS.md` for assumptions and wall ceilings.

## 11. Outputs

Under `SCR_ROOT/results/<STAMP>_lowp_<piece>/p0020|p0030/`: enum20 and enum30 each have 600 `<dataset>/EXACT.{rds,sha256,done}` units; smc has 2,400 `<dataset>_<scale>/SMCBVS.{rds,csv,sha256,done}` units; smcrep has 12,000 `<dataset>_<scale>/SMCBVS_rep<m>.{rds,csv,sha256,done}` units, m=1..5. P5 artifacts are separate in `P5_retry/`; primary records remain unchanged. `LOG_RUN` contains launch receipts, job IDs, scheduler logs, ledger, timing, environment, P0, wave truth evidence, P5 scan, accounting and manifests. A valid `.done` plus verified sidecar establishes operational completion; inspect SMC `v3_status` and `status` for scientific outcomes.

## 12. Acceptance checks

1. Launch receipts, env hashes, guard and ceiling checks, sbatch vectors and job IDs are saved for every wave.
2. P0a and P0b both PASS; frozen checks pass.
3. Truth-lock test, wave lock and verified unlock are evidenced for every wave.
4. Reconciliation has exactly 600 / 600 / 2,400 / 12,000 done, no silent drops; exceptions are reported and resolved with HQ.
5. P5 scan is reported; no unit has more than one P5 attempt.
6. Final accounting shows all jobs terminal; compare `core_hours.tsv` with the estimate.
7. All manifests verify after download and transfer receipts are retained.
8. Cleanup reports `CLEANUP VERIFIED` and its closure receipt is retained outside the removed tree.

## 13. Assumptions and HQ items

- **Throttles with PROD-H (HQ D49).** PROD-H's defaults are `%30` + `%30` one-CPU tasks = 120 billed CPUs; PROD-L stays ≤ 68 billed while PROD-H runs and ≤ 132 alone, combined ≤ 192 (120 + 68 = 188). `ceiling_check.py` refuses any submission that would exceed these.
- **PROD-L counts toward PROD-H's guard.** PROD-H's submit guard counts the throttles of ALL fb31 array jobs and refuses unless the total is ≤ 100 tasks. PROD-L's arrays count `%2 + %16 + %16 = 34` tasks at the withH profile (60 + 34 = 94, admitted) but `%4 + %32 + %32 = 68` at the alone profile (60 + 68 = 128, refused). So **before PROD-H is submitted, OPS lowers PROD-L to withH** (`retune_throttle.sh STAMP --profile withH --yes`), and **once PROD-H has finished OPS may raise PROD-L back** (`retune_throttle.sh STAMP --profile alone --yes`, which runs `scontrol update JobId=<id> ArrayTaskThrottle=<n>` for PROD-L's own live arrays only).
- **Scratch (HQ D49).** About 6 GiB is fine (home, not scratch, is the constraint). The rule stands: each piece's results folder is pulled, sha256-verified against its own manifest and deleted from scratch as soon as that piece is final (§5 step 8).
- Benchmarks await BENCH-FIX (b), Sol ACCEPT and revised sizing. No staging until Sol accepts this bundle.

## 14. Operating notes

- Failed initial P5 scan: submit a fresh scan phase (`--p5-scan --phase r1`, next unused rN), then `make_p5_list.sh STAMP --from-scan r1`; never edit or copy scan files by hand; never overwrite `expected.tsv` (it is append-only).
- If the scheduled unlock never produced `WAVE_UNLOCK_VERIFIED`, first wait for complete terminal accounting, run `bash "$B/recover_truth.sh" "$STAMP"` and retain its stdout/stderr. Require exit 0. Set `WAVE` to that failed wave and use the confirmed LOWP R module/library environment. Ensure `LOG_RUN/truthlock/$WAVE` exists. Run `env RSCRIPT=Rscript bash "$B/truth_wave.sh" unlock "$RUN_HOME/study" "$RUN_HOME/code/lowp/R" "$LOG_RUN/truthlock/$WAVE/WAVE_UNLOCK.txt" "$LOG_RUN/truthlock/$WAVE/evidence"` and retain its output/exit status. This verifies 755/444, counts and the wave's pre-lock hashes; when both pre-lock lists are absent it uses the B2 staged-truth verification. Require exit 0 and the newly appended `WAVE_UNLOCK_VERIFIED` with equal/staged-equal hashes before guard, reconciliation, cleanup of stale files, or another wave. A missing single pre-lock list or hash mismatch remains STOP for HQ. Never create the verified marker by hand. Preserve the failed scheduled-unlock evidence and report the recovery to HQ.
- Scheduler evidence missing, invalid or nonterminal: keep truth locked, inspect the recorded job IDs and scheduler/accounting, and retry only when every ID is present and terminal. If unlock failed, run `bash "$B/recover_truth.sh" "$STAMP"` after all jobs are terminal; verify the staged truth hashes against `STAGED_SHA256.txt` from HOME_ROOT before using guard or submitting another wave.
- P5 scan failed or has unsafe retry state: inspect the scan and retry artifacts, preserve evidence, report to HQ, and repeat a failed scan under a fresh phase name after the cause is resolved. Do not remove an attempt record or rerun an attempted unit.
- A P5 attempt failed or was interrupted: preserve its ledger and artifacts, report the exception to HQ, and do not relaunch it. A never-started unit can go into the next `p5rN` list.
- Stale lock or temporary file: after terminal accounting and verified unlock, inspect `bash "$B/clear_stale.sh" "$STAMP"`, then use `--yes` to move the listed files to cleanup evidence.
- Existing start record or unexpected restart: preserve the existing ledger and task logs, investigate the job with HQ, and use a fresh wave only for units eligible under the attempt limits.
- Missing scheduler end time: inspect Slurm metadata and accounting; once scheduler time is available and the wave is terminal and unlocked, create a fresh resubmission list for deferred units.
- Closure or checksum mismatch: preserve the inventory, marker and result folder; investigate and resolve the mismatch with HQ before transfer or an acknowledged `--allow-incomplete` closure.
- **Logs close refused with "stale artifacts" (post-READY finding, 2026-10-30, safe halt).** The staged `make_manifests.sh` scans the logs folder for `*.lock`/`*.tmp*`; after `clear_stale.sh --yes` the archived artefacts live in `LOG_RUN/cleanup/`, and an interrupted ledger write may leave a hidden `.<tag>.<pid>.tmp`, so `--piece logs` refuses. The laptop bundle's `make_manifests.sh` is fixed (logs are not scanned). Resolution on NOTS, only if every listed path is under `LOG_RUN/cleanup/` or is a ledger/inventory temporary file: after all four pieces are CLOSED and final accounting is written, create the manifest by hand from `LOG_RUN` (`find . -type f ! -name MANIFEST.sha256 -print0 | LC_ALL=C sort -z | xargs -0 sha256sum` into a file outside the folder, then move it to `LOG_RUN/MANIFEST.sha256`), record its sha256 in the OPS log, and pull `logs/<RID>` as in §5 step 8 (the logs CLOSED marker is not required by `cleanup_prodl.sh`). Report to HQ.
- Throttle admission or confirmation fails: inspect the saved receipt and live queue, resolve conflicting work or scheduler errors, and retry. Before submitting PROD-H, repeat `--check-drained` until exit 0.
