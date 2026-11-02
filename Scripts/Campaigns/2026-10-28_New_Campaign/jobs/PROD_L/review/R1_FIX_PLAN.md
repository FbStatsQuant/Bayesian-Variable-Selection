# R1 fix plan (manager, binding for fixer and tester; answers `SOL_REVIEW_PRODL_R1.md`)

HQ D53: at most two full Sol rounds. R1 findings are fixed here; each fix has a regression test. Numbers = Sol's findings.

## F1 (blocking) Unlock and recovery fail CLOSED on scheduler evidence
`slurm/s8_unlock.sbatch` and `recover_truth.sh`:
1. `squeue -h -u fb31 -o '%i|%j|%T'` must exit 0 (else STOP, trees stay locked, exit 1). Any row whose array root id (part before `_`) is a recorded fitting id of ANY wave (steps `s1_*`–`s4_*`; for recover_truth: ANY recorded id) → STOP.
2. `sacct -X -n -P -j <all those ids> -o JobID,State` must exit 0, and EVERY recorded id must appear with at least one row, and every row must be terminal (`COMPLETED|FAILED|CANCELLED*|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE`). Missing id, unparsable row or non-terminal → STOP.
3. No inference from an error message ("invalid job id" handling is REMOVED). B2 never-locked hash verification is kept unchanged (truth_wave.sh).
Tests: mixed old/new ids with an active earlier-wave task; missing accounting; squeue error; sacct error; all terminal → unlock runs.

## F2 (blocking) P5 is a reconciled, closable phase
Files: `submit_prodl.sh`, `slurm/s5_p5scan.sbatch`, `make_p5_list.sh`, `reconcile_prodl.py`, `make_manifests.sh`, `batch_runner.sh` (P5 attempt record unchanged).
1. **Scan phases.** `submit_prodl.sh --p5-scan --phase <name>` with `name` matching `^(initial|final[0-9]*|r[0-9]+)$`; launch dir `launch/p5scan_<name>`; job env `PHASE=<name>`; outputs `LOG_RUN/p5/scan_<name>_{smc,smcrep}.tsv` + `scan_<name>.ok` (written only if both scans exit 0). A failed scan phase can be repeated under a new name.
2. **Expected P5 inventory.** `make_p5_list.sh STAMP --from-scan initial` (run gate as now): reads `scan_initial_*.tsv`; refuses (exit 2) if any `primary resource_limit` row is `locked`, `incomplete` or `invalid_inspect`; writes `RUN_HOME/p5/expected.tsv` (all `eligible` rows: piece column `p5`, base_piece smc|smcrep, unit, dataset, scale, repeat) ONCE (idempotent same-content; different → exit 2), and `RUN_HOME/p5/scan_initial.receipt` (sha256 of the two scan tables). Zero eligible → `expected.tsv` with header only + `none_eligible.txt`.
3. **P5 waves.** Wave names `p5` and `p5r1`, `p5r2`, … `make_p5_list.sh STAMP --wave <p5|p5rN>` writes `RUN_HOME/p5/units_<wave>.tsv` (one unit per task, tasks 0..k−1): the expected units that have NO `LOG_RUN/p5_attempts/<unit>` record and no valid retry (never started: deferred, not reached, or never submitted). A unit WITH an attempt record and no valid retry is never relaunched: it goes to `RUN_HOME/p5/exceptions_<wave>.tsv` (report to HQ). Idempotent like make_resubmit (SAME_LIST / exit 2 / NOTHING_TO_SUBMIT). `submit_prodl.sh --wave p5|p5rN` reads `units_<wave>.tsv`.
4. **Reconcile.** When `RUN_HOME/p5/expected.tsv` exists, every expected P5 unit gets its own row in `inventory/p5.tsv` (`piece unit outcome detail`): `done` (valid `P5_retry/<prefix>_p5retry.*` with the exact-file validation of F6), `attempt_failed` (attempt record, no valid retry), `deferred`, `killed_external`, `not_run`. INVENTORY.md gets a P5 section. If `expected.tsv` does NOT exist, smc/smcrep rows carry detail `p5_scan_pending` and the P5 status line says PENDING. Exit 0 requires every expected P5 unit `done` in addition to the existing condition.
5. **Closing smc/smcrep** (`make_manifests.sh`) requires: `p5/expected.tsv` exists; a FINAL scan phase (`scan_final*.ok`) whose job finished after every P5 wave job (compare against JOBIDS order: the final scan's job id is greater than every p5 wave job id); every expected P5 unit `done` in the frozen scanner's final table (`retry_state == done` for that unit) AND in reconcile; else exit 6 unless `--allow-incomplete` (HQ-acknowledged; listed in CLOSED). With zero expected units, the final scan may be the initial one (`scan_initial.ok` suffices).
Tests: interrupted P5 (start, no end, NODE_FAIL) → not done, exit nonzero, close refused; never-started P5 unit → listed in `units_p5r1.tsv`; attempted unit → exception, never relisted; zero-eligible path closes; scan phase reuse refused, new phase allowed.

## F3 (blocking) No silent requeue
1. Every `sbatch` vector gets `--no-requeue` (driver; also s5 scan).
2. `batch_runner.sh` (and `slurm/common.sh`'s `pilot_init` for every arm) refuses, before ANY ledger or attempt write, when `SLURM_RESTART_COUNT` is set and not `0` (exit 71, message names the job).
3. `.start` records are created with noclobber semantics: if `<JOB_TAG>.start` already exists for a unit, the unit is NOT run (outcome `unit_failed`, reason `start_record_exists`), the existing record is untouched.
Tests: same job/task id run twice → second run refuses, first records byte-identical; `SLURM_RESTART_COUNT=1` → exit 71 with no ledger change; vectors contain `--no-requeue`.

## F4 (should) Collector never runs the guard on a locked or unverified tree
`slurm/s9_collect.sbatch`: always write the accounting snapshot; then run the guard ONLY if `LOG_RUN/truthlock/<wave>/WAVE_UNLOCK.txt` contains `WAVE_UNLOCK_VERIFIED` AND both truth top directories are mode 755 (`stat -c %a`). Otherwise write `accounting/<wave>/GUARD_SKIPPED.txt` with the recovery instruction (`recover_truth.sh`, then verify hashes) and exit 1. Non-terminal check uses the terminal whitelist, not a partial blacklist. Tests: FAILED/CANCELLED unlock → guard not called, exit 1; verified unlock → guard called.

## F5 (should) Stale artefacts = the real CLI temp names
`clear_stale.sh`, `make_resubmit.sh`, `make_manifests.sh` share ONE definition: directories named `*.lock` (including `.lock`), and files whose name contains `.tmp` (`EXACT.rds.tmp<PID>`, `EXACT.sha256.tmp<PID>`, `.done.tmp<PID>`, adapter `*.tmp.<PID>`). Put the `find` expression in one sourced helper (`stale_lib.sh`). Tests with all four names + `.lock` dirs.

## F6 (should) Exact completion validation, shared
New `prodl_verify.py` (stdlib), imported by `reconcile_prodl.py` and called by `make_resubmit.sh` (replaces bare `sha256sum -c`):
- enum `EXACT`: `EXACT.sha256` exactly one line `<64 hex>  EXACT.rds`; `EXACT.rds` exists, non-empty, hash matches; `EXACT.done` first line = the same hash.
- SMC `<prefix>` (`SMCBVS`, `SMCBVS_rep<m>`, `P5_retry/<prefix>_p5retry`): sidecar exactly two lines naming `<base>.rds` and `<base>.csv` (no duplicates, basenames only), both non-empty and matching; `.done` first line starts with `status `; CSV parses with columns `status` and `v3_status` and exactly 2 rows.
- Anything else → not done, with the reason. A committed scientific failure (valid record, status failed) stays `done` with its native status reported.
- Reconcile exit is nonzero also when any unexpected result folder exists or any CSV is malformed.
Tests: missing RDS with a sidecar for another file; one-line SMC sidecar; duplicate name; malformed `.done`; malformed CSV; unexpected folder.

## F7 (should) Reconcile remembers CLOSED pieces
`make_manifests.sh` writes `inventory_sha256=<sha of <piece>.inventory.tsv>` into `<piece>.CLOSED`. `reconcile_prodl.py`: for a piece with `RUN_HOME/manifests/<piece>.CLOSED`, load `<piece>.inventory.tsv` after verifying its sha256 against CLOSED (mismatch → exit 2) instead of scanning scratch; mark the piece `closed` in INVENTORY.md. With `--home-root` pointing to a downloaded home summary the same works on the laptop. Final inventory covers all 15,600 units (+ P5). Test: close → move the folder away → reconcile still `done` and exit 0.

## F8 (should) JOB.md executable as written
- nots_pull with ABSOLUTE NOTS paths: `/scratch/fb31/New_Campaign/results/${STAMP}_lowp_${piece}`, `/scratch/fb31/New_Campaign/logs/${STAMP}_lowp_prodL`; the home summaries pulled WITHOUT `--delete` by explicit commands per folder that exists (`manifests`, `inventory_final`, `p5`, `resubmit`) plus `JOBIDS.tsv` (check `ops/transfer/nots_pull.py` for what it accepts; if it pulls only folders, pull `runs/<RID>/manifests` etc. and copy JOBIDS.tsv into `manifests/` first via `final_accounting.sh`).
- Waiter: exit 3 = triage only (inspect, and if the wave continues, restart the waiter); exit 0 = all terminal. Before reconcile/clear_stale/any later wave: `waiter` exit 0 AND `WAVE_UNLOCK_VERIFIED` in this wave's unlock record.
- Resubmission round: run `make_resubmit.sh STAMP <piece> rN` for EVERY piece first, then ONE `submit_prodl.sh --wave rN --pieces <pieces with a list>`; next round rN+1.
- Operating notes section (§14) for safe-halt recoveries (see D53 class ii).

## F9 (should) Retune with admission and drain check
`retune_throttle.sh STAMP --profile alone|withH [--yes]` and `retune_throttle.sh STAMP --check-drained`:
- builds a plan from this run's LIVE arrays (cpus × new throttle, phase fit, smc/smcrep serial rule) and runs `ceiling_check.py` against a fresh squeue (fail closed); `alone` additionally refused while `_prodH` jobs exist (kept);
- `--yes` applies `scontrol update` and then re-queries squeue to confirm each pending array shows the new `%N` (record in `LOG_RUN/launch/retune_<utc>.txt`);
- `--check-drained` prints PROD-L's RUNNING billed CPUs and exits 0 only if ≤ CEIL_WITHH (68).
JOB.md: before PROD-H submission: `--profile withH --yes`, then repeat `--check-drained` until 0.
Tests: raise with 70 billed of other work → refused; lowering prints/applies; check-drained over/under.

## F10 (should) Waiter needs complete accounting
`waiter.sh`: sacct `-n -X -P -j IDS -o JobID,State`; every requested id must have ≥ 1 row (by array root); all terminal → ALL_TERMINAL; any missing/unparsable → keep waiting (UNKNOWN); any failure-like row → EARLY_FAILURE at once. Fix WT40 to expect "not terminal".

## F11 (should) No diagnostics in home
`make_manifests.sh` writes the reconcile stdout/stderr to `LOG_RUN/reconcile/<utc>_<piece>.out` (scratch). Home keeps only inventories, CLOSED, summary.

## F12 (minor) P5 wording
CORE_HOURS.md and JOB.md: "16 = nominal doubled core allocation (8 h × 2 billed); wrapper bound 29,160 s ≈ 16.2; requested-wall ceiling 18 per unit".

## F13 (should) Deadline from scheduler time
`batch_runner.sh`: end time source, in order: numeric `SLURM_JOB_END_TIME`; else `squeue -h -j "$SLURM_JOB_ID" -o %e` parsed with `date -d` (must give a number); else, in production, refuse before any unit (all units recorded `deferred` with `reason=no_scheduler_end_time`, task exit 1); only under `PILOT_LOCAL_TEST=1` may it fall back to script time. Deadline = min(T0 + WALL − START_SLACK_S, END − 60). Record `end_source=` and `end_epoch=` in every `.start`/`.deferred` record. DESIGN.md §3 updated; DL74 changed to expect refusal outside local test.
