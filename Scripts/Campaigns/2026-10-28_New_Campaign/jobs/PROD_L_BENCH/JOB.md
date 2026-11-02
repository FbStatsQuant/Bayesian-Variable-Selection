# JOB: PROD-L benchmark wave (PROD_L_BENCH) on NOTS

**Status: NOT YET REVIEWED: needs Sol READY (HQ D53 limit) before OPS stages.** For OPS via HQ; charter §6. HQ D56. `STAMP=YYYYMMDDTHHMMZ` UTC (a FRESH stamp, not PROD-L's); `RID=<STAMP>_lowp_bench`; `HOME_ROOT=/home/fb31/projects/BVS/New_Campaign`; `SCR_ROOT=/scratch/fb31/New_Campaign`; `RUN_HOME=HOME_ROOT/runs/<RID>`; `LOG_RUN=SCR_ROOT/logs/<RID>`; results `SCR_ROOT/results/<STAMP>_lowp_benchres`. All bundle scripts on NOTS are under `RUN_HOME/code/prod_l_bench/` (`B` below); the laptop bundle is `CAMP/jobs/PROD_L_BENCH`. Use the configured `ssh nots` alias, one connection at a time, batched; bundle scripts never open SSH.

## 0. Charter limits
Campaign home ≤ 0.5 GiB; total home < 9.6 GiB (OPS guard). One stage of ≈ 64 MiB in home (code + 1,200 inputs + the inputs manifest); all results, logs, caches and temporary files on scratch. **No truth file and no truth manifest is staged for this run**; staging and submission refuse any `truth`/`holdout` path, and the frozen CLI refuses such path components too. Nothing shared is overwritten.

## 1. Purpose
The 8 primary benchmark methods (F1 lasso, F2 elastic net, F3 adaptive lasso with the D42 lasso pilot, F4 MCP, F5 ABESS, A1 SuSiE, A2 SSL, A3 horseshoe) with their committed low-p rules (`code/bench_lowp/ADAPTATIONS.md`, LA-1–LA-4) on the 1,200 sealed low-p datasets × c ∈ {c100, c050} = **2,400 cases** (one unit = one case running all 8 methods; 19,200 method records). Frozen code: `code/bench_lowp` r2 (manifest `BENCH_LOWP_MANIFEST_SHA256_r2.txt`, sha256 `85a182488450…a6b7`, 34 files; BENCH-FIX Sol ACCEPT, D55). R 4.5.2 with the pinned read-only library `/projects/ml75/fb31/BVS/bench20261019/lib/R452`. Coefficient vectors are saved at every rule's selected point (D42.5; F1–F5 per-rule penalized and OLS coefficients, A1–A3 beta/pip) by the frozen CLI and checked by `accept_bench.R`. **D54.3: the ABESS exact size check is deferred and disclosed** (not run, not a gate).

## 2. Staging
Before staging run the OPS guard with the stage reservation: `/home/fb31/projects/BVS/New_Campaign/code/ops/guard.sh 75` (`PLANNED_HOME_MB_STAGE`) and keep its line. **HQ D57: the stage is reserved ONCE, here.** After extraction it is part of home usage, so `submit_bench.sh` asks the guard only for the remaining growth (`PLANNED_HOME_MB_MAIN` = 5 MB) and records `stage_on_disk_kb` in the launch guard receipt; it never adds the stage a second time. On the laptop:
```bash
"C:/Program Files/Git/bin/bash.exe" "CAMP/jobs/PROD_L_BENCH/stage_local.sh" --sealed "C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/inputs/lowp_study" --stamp <STAMP> --out "<durable-run-folder>"
```
It copies the frozen `code/bench_lowp`, writes `code/bench_lowp.SHA256SUMS` (the r2 manifest with `./`-prefixed paths, proven identical pair by pair to r2) and `code/bench_lowp.r2_manifest_original.txt` (r2 as frozen; its sha256 must be `85a18248…a6b7`), runs the frozen check, refuses any truth/holdout/dev path, and writes `prodLB_bundle_<STAMP>.tar` + `.sha256`. Upload the tar; verify its hash on NOTS; from `HOME_ROOT`: `test ! -e runs/<RID>` then extract, then `sha256sum --quiet -c runs/<RID>/STAGED_SHA256.txt`.

## 3. OPS confirms `B/bench.env`
`MODULES_BENCH="GCC/14.3.0 R/4.5.2"` (the pilot's benchmark modules), the pinned library path, roots, guard, ceilings (132 / 68 / 192), the per-piece table (bench 1 h / 600 s per case; benchretry 1 h / 1,200 s), throttles `%32` / `%16`.

## 4. Test hooks
Never set `PILOT_DRYRUN`, `PILOT_SKIP_MODULES`, `PILOT_TIME_BIN`, `PRODL_UNIT_CMD`, `PRODL_TEST_WALL_S`, `PRODL_TEST_BUDGET_S`, `PRODL_TEST_NOW_OFFSET_S` or `PRODL_BENCH_EXTRA` for a real run; the driver and every job refuse them outside `--local-test`.

## 5. OPS sequence
1. **When:** after PROD-L's fitting lane (no `lowpL_s1`–`s4_` job queued or running; the driver refuses otherwise) and when the 192-billed-CPU ceiling allows (the driver's ceiling check counts PROD-H, PROD-L, BENCH_F3 and every other fb31 job). Guard, stage, upload and verify as §2; confirm §3. Set `B=/home/fb31/projects/BVS/New_Campaign/runs/<RID>/code/prod_l_bench` and `export STAMP=<STAMP>`.
2. `bash "$B/submit_bench.sh" --wave main --profile alone --dry-run` (`withH` while PROD-H runs); inspect guard, ceiling and the three vectors (`lowpB_s0_verify`; `lowpB_s1_bench` `0-95%32` or `%16`, afterok verify; `lowpB_s9_collect` afterany); then the same without `--dry-run`. All-or-abort; cancel only by explicit id.
3. On the laptop: `bash "CAMP/jobs/PROD_L_BENCH/waiter.sh" <LOGFILE> <JOBIDS> [MAX_CHECKS]` (ids from `LOG_RUN/jobids.tsv`). Exit 3 = triage only, then restart with `--until-terminal`; exit 0 (all COMPLETED) or 4 (all terminal, some failed) = complete terminal accounting; exit 2 = restart.
4. `python3 "$B/reconcile_bench.py" "$STAMP"` → `RUN_HOME/inventory_final/INVENTORY.md` (STATUS line, outcomes, rule statuses per method, exceptions). `bash "$B/clear_stale.sh" "$STAMP"` lists stale artefacts (method locks, the CLI's hidden `.<M>.<ext>…` temporary files, incomplete method units); after inspection `--yes` moves them to `LOG_RUN/cleanup/<utc>/`.
5. **Resubmission round rN (r1, then r2, …):** `bash "$B/make_resubmit.sh" "$STAMP" r1` writes `RUN_HOME/resubmit/bench_r1.tsv` (never started; or one start that ended unit_failed / killed_external), `benchretry_r1.tsv` (one start killed by the hard timeout: **one retry at doubled time**, 1,200 s per case), and `bench_r1_exceptions.tsv` (two starts, or a retry already made: report to HQ, never relisted); or prints `NOTHING_TO_RESUBMIT`. Then ONE submission with the pieces that got a list, e.g. `bash "$B/submit_bench.sh" --wave r1 --profile alone --pieces bench,benchretry`. Wait (step 3); the next round is r2.
5b. **PROD-H interplay (D49/D50):** if PROD-H is to be submitted while this wave's arrays are queued or running, first the dry run `bash "$B/retune_throttle.sh" "$STAMP" --profile withH` (admission receipt), then `bash "$B/retune_throttle.sh" "$STAMP" --profile withH --yes` (applies `scontrol update ArrayTaskThrottle` to this run's arrays only and confirms by re-query), then repeat `bash "$B/retune_throttle.sh" "$STAMP" --check-drained` until it exits 0 (running billed ≤ 68) before PROD-H is submitted. Once PROD-H has finished, `--profile alone --yes` may raise the throttles again (refused while any PROD-H job is queued or running; ceiling-checked).
6. **Close, pull, verify, delete (HQ D49):** when every case is done (or HQ acknowledges the exceptions): `bash "$B/make_manifests.sh" "$STAMP" --piece bench` (refuses with exit 6 otherwise; `--allow-incomplete` only after HQ's acknowledgement), then on the laptop `MSYS_NO_PATHCONV=1 py -3 ops/transfer/nots_pull.py "/scratch/fb31/New_Campaign/results/${STAMP}_lowp_benchres" --delete`; verify `MANIFEST.sha256` locally. Then `bash "$B/final_accounting.sh" "$STAMP"`, `bash "$B/make_manifests.sh" "$STAMP" --piece logs`, and `MSYS_NO_PATHCONV=1 py -3 ops/transfer/nots_pull.py "/scratch/fb31/New_Campaign/logs/${STAMP}_lowp_bench" --delete`. Pull the home summaries without deletion: `MSYS_NO_PATHCONV=1 py -3 ops/transfer/nots_pull.py "/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_bench/manifests"`, the same for `inventory_final` and `resubmit` (if present).
7. **Laptop acceptance:** `"C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "CAMP/jobs/PROD_L_BENCH/accept_bench.R" --results "<downloaded>/results/<STAMP>_lowp_benchres" --lists "CAMP/jobs/PROD_L_BENCH/lists/units.tsv" --code "CAMP/code/bench_lowp" --r2-manifest "CAMP/code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt" --inputs-manifest "C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/inputs/lowp_study/manifests/inputs_manifest_lowp.csv" --out "<downloaded>/accept"` → `ACCEPT_BENCH.md` must say ACCEPTED (exit 0); FAIL (2) and INCOMPLETE (3) go to HQ. Every check is against an authoritative source (Sol R1 I1–I4): the exact rule/role structure from the frozen registry + `lowp_derive`; the SPEC coefficient contract (D42.5) and A1's PIPs; identity, seeds and input hashes from the sealed INPUTS manifest (no truth); the code fingerprint recomputed and anchored to the r2 tree; R 4.5.2, pinned library, pinned versions and package locations.
8. `bash "$B/cleanup_bench.sh" "$STAMP"` (dry run), then `--yes --receipt <path outside the run folder>`; require `CLEANUP VERIFIED`.

## 6. Requests
All: account/partition `commons`, `--constraint=sapphirerapids`, `--no-requeue`; one requested CPU bills two.

| Step | Array alone / withH | CPUs | Memory | Wall | Dependency |
|---|---|---:|---:|---:|---|
| s0_verify (frozen check, P0b inputs, env probe) | — | 1 | 2G | 0:30 | — |
| s1_bench (25 cases per task) | 0-95%32 / 0-95%16 | 1 | 1G | 1:00 | afterok verify (main wave) |
| s2_benchretry (rN only) | 0-(k−1)%32 / %16 | 1 | 1G | 1:00 | — |
| s9_collect | — | 1 | 1G | 0:15 | afterany of the wave |

Billed peak: 64 alone, 32 withH (`ceiling_check.py`: ≤ 132 / ≤ 68, combined with every other fb31 job ≤ 192). PROD-H's ≤ 100-array-task guard counts `%32` / `%16`.

## 7. Batch deadline and retry
As PROD-L: before every case the runner needs the full hard budget (600 s; 1,200 s in benchretry) + 60 s kill grace + 120 s commit margin before the deadline (scheduler end time − 60 s, and task start + wall − 120 s); otherwise it defers that case and the rest of the task. A case runs under GNU `timeout`; a killed case (124/137) is `killed_timeout`, and gets exactly one doubled-time retry. CLI exit 2 (a committed failed rule) is a scientific outcome: the case is done and never resubmitted.

## 8. Truth
No truth on NOTS for this run (no lock needed). The CLI reads only `study/inputs` and `study/manifests/inputs_manifest_lowp.csv`; scoring against the truth happens on the laptop later (ANALYSIS-L).

## 9. Disk
Home ≈ 64 MiB (reserved once before staging with 75 MB; the submission then asks only 5 MB, D57). If the guard refuses, wait for PROD-L's clean-up or use the D31 route. D40's 9.70 GiB is the last resort and needs a recorded HQ decision applied in BOTH places: OPS's `guard.sh` (`HOME_LIMIT_KB`) and this bundle's `bench.env` (`REQUIRED_HOME_LIMIT_KB=10171187`); `guard_check.sh` then probes against the guard's own limit (it refuses any guard limit above `REQUIRED_HOME_LIMIT_KB`). Scratch ≈ 1.5 GiB results (≈ 645 KiB per case) + logs.

## 10. Core-hours
Expected **38.3** billed core-h, conservative **40.6**, F3 lasso-pilot sensitivity **≈ 45.4**; requested-wall ceiling 192. See `CORE_HOURS.md`.

## 11. Outputs
`SCR_ROOT/results/<STAMP>_lowp_benchres/p0020|p0030/<dataset>_<scale>/<M>.{rds,csv,sha256,done}` for M ∈ F1–F5, A1–A3 (2,400 case folders, 19,200 method units). `LOG_RUN`: launch receipts, job ids, Slurm outputs, ledger, timing (GNU time per case), unit logs, env, p0_verify, accounting, reconcile diagnostics, cleanup evidence.

## 12. Acceptance checks
1. Launch receipts (guard, ceiling, env hash, vectors, job ids) for every wave.
2. s0_verify PASS: frozen r2 tree, P0b 1,200 inputs, environment probe (R 4.5.2, pinned versions).
3. `reconcile_bench.py` STATUS `CLEAN` (exit 0): 2,400 / 2,400 cases done, no exception; or `COMPLETE WITH n HQ-ACKNOWLEDGED EXCEPTIONS` (exit 4) after HQ's acknowledgement. No silent drops.
4. No case has more than one doubled-time retry; exceptions reported.
5. `final_accounting.sh` all terminal; `core_hours.tsv` vs §10.
6. Manifests verify after download; transfer receipts kept.
7. `accept_bench.R` ACCEPTED (incl. D42.5 coefficient evidence, provenance R 4.5.2 / pinned library / `test_library` FALSE; D54.3 disclosed).
8. `CLEANUP VERIFIED` with its receipt outside the removed tree.

## 13. HQ items
- No truth lock: no truth staged (stronger than locking); HQ asked to reuse the lock, this replaces it.
- Serialized after PROD-L's fitting lane; `--allow-concurrent-prodl` exists for HQ only (the ceiling check still applies).

## 14. Operating notes
- **No truth on NOTS (by design; replaces PROD-L's truth lock):** this run stages no truth file and no truth manifest; `stage_local.sh` and `submit_bench.sh` refuse any path containing `truth` or `holdout` under the run folder, so there is nothing to lock or recover. If a submission is refused for that reason, do NOT delete anything by hand: report to HQ (the stage is wrong and must be rebuilt with a fresh STAMP).
- **D54.3 disclosure:** the ABESS exact size check is deferred; neither this bundle nor `accept_bench.R` performs it. Report it as disclosed in any result.
- **Stale artefacts:** after terminal accounting, `clear_stale.sh` (dry run) then `--yes`; it moves (never deletes) `*.lock` directories, the CLI's hidden temporary files and incomplete method units (`<M>.rds/.csv/.sha256` without `<M>.done`, which the CLI refuses as "manual repair") to `LOG_RUN/cleanup/<utc>/`. Then build the round's lists.
- **Corrupted COMPLETED method unit (Sol R1 II1; safe halt).** A method with `<M>.done` present but a missing or corrupt companion (`.rds`, `.csv`, `.sha256`) is invalid to `reconcile_bench.py`/`bench_verify.py`, yet `clear_stale.sh` does not touch it (it has `.done`) and the frozen CLI refuses to resume it, so a blind retry only consumes an attempt. Resolution, after complete terminal accounting and BEFORE building another round: (1) preserve the method's four exact paths (`M.rds`, `M.csv`, `M.sha256`, `M.done`, whichever exist), their SHA-256 values and the reconcile diagnostic in a fresh `LOG_RUN/cleanup/<UTC>/<case>/` archive (copy first); (2) obtain HQ's determination: storage/transfer damage (refit) or a scientific exception; (3) for an HQ-approved refit, MOVE only the existing files of that one invalid method into that archive, leaving every other method of the case and every ledger/start record untouched; (4) only if the case's ledger still permits an attempt (`make_resubmit.sh` routes it to `bench_rN` or `benchretry_rN`, not to exceptions), build a fresh round with `make_resubmit.sh`, inspect the routing, and submit once: the CLI resumes the intact methods and refits only the moved one; (5) if a doubled-time attempt already happened or there are two starts, keep it as an HQ exception: never reset the ledger or bypass the cap; (6) reconcile again before closing. Never use this procedure on PROD-L's already-running stage.
- **Existing start record or unexpected restart:** the runner refuses a reused job tag (`LOG_RUN/refusals/`) and a restarted task (exit 71); preserve the ledger and logs, investigate with HQ, and use a fresh round only for cases still eligible.
- **Missing scheduler end time:** every case of the task is deferred (`reason=no_scheduler_end_time`, task exit 1); once Slurm reports end times, resubmit the deferred cases in the next round.
- **Guard refusal at submission:** nothing is created; wait for PROD-L's clean-up to free home, or use the D31 archive route; D40 is the last resort.
- **Closure refused (exit 6):** resubmit, or obtain HQ's acknowledgement of the listed cases/exceptions and close with `--allow-incomplete`; acknowledged exceptions stay in every later inventory (reconcile exit 4, never 0).
