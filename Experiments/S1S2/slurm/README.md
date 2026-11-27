# S1 SMC-BVS on NOTS: run book

S1 × 100 reps, SMC-BVS only: 16 settings × 100 reps = 1,600 fits, one Slurm array task per fit. Owner GO is conditional. **Nothing is submitted until the manager relays "SUBMIT BATCH k".**

## Paths
On NOTS, everything lives in exactly two places (POLICIES §8).

| what | where |
|---|---|
| deploy snapshot: `S1S2/` tree, `smcbvs_core@7100bb3b/`, `MANIFEST.sha256`, `DEPLOY_INFO.txt` | `/home/fb31/SMC-BVS/_local/engineering/S1S2/deploy/` |
| compiled engine cache (built once on the login node) | `…/deploy/smcbvs_core@7100bb3b/.cpp_cache/` (not in the manifest) |
| env: modules GCC/14.3.0 + R/4.5.2, single-threaded BLAS/OMP, user R profile and library off | `/home/fb31/SMC-BVS/_local/engineering/envs/S1S2/env.sh` (copy of `nots_env.sh`) |
| submission log, `check_b<k>.tsv` | `/home/fb31/SMC-BVS/_local/engineering/S1S2/logs/` |
| records | `/scratch/fb31/SMC-BVS/runs/S1S2/smcbvs/S1_xx/rep_RRR.{json,rds}` |
| Slurm stdout/stderr (`--chdir` too) | `/scratch/fb31/SMC-BVS/runs/S1S2/logs/` |
| per-task TMPDIR (removed at task exit) | `/scratch/fb31/SMC-BVS/tmp/S1S2/<arrayjob>_<task>/` |
| toy record (environment proof, not part of the grid) | `/scratch/fb31/SMC-BVS/runs/S1S2/_toy/` |

On Owls, the pulled records go to `/home/fb31/Bayesian-Variable-Selection/_local/engineering/runs/S1S2/smcbvs/`, with `_manifests/` and `_superseded/` beside them. Desktop units go to `…/_local/engineering/records/S1S2_smcbvs_b<k>/`.

Scratch is purged after 14 days without access and has no backup. Pull and package each batch as soon as it ends.

## Files

| file | runs on | purpose |
|---|---|---|
| `tasks_S1_smcbvs.tsv` | — | 1,600 rows: `task_id = (cell-1)*100 + rep`, setting_id, rep |
| `s1_smcbvs_array.sbatch` | NOTS (Slurm) | one fit per task. Idempotent: it skips a task whose json has top-level status ok. On a harness wall timeout it writes a "failed" json |
| `submit_batches.sh` | NOTS login | builds the per-class arrays of one batch and prints them. `--test-only` validates; `--go` submits |
| `check_batch.sh` | NOTS login | sacct states, record status and engine E-flags, then the STOP verdict (`--suite 2` for S2) |
| `deploy_to_nots.sh` | Owls | deploys from `--commit HASH` (or a worktree snapshot), builds the manifest, installs env.sh |
| `pull_to_owls.sh` | Owls | builds a NOTS sha256 manifest, rsyncs, then runs `sha256sum -c` on Owls |
| `package_for_desktop.sh` | Owls | builds one flat unit (16 tars, S2: 120, + `slurm_<tag>.tar` partition record + one SHA256SUMS) and moves it into `records/` atomically |
| `free_nots_scratch.sh` | Owls | deletes a batch's NOTS copy only after gates G1–G4 (desktop verified + three sha checks). Dry run by default |
| `tasks_S2_smcbvs.tsv` | — | 12,000 rows for S2 (S2_001..S2_120), same formula; the sbatch reads it when `S1S2_TASKS` points to it |
| `submit_s2_batches.sh` | NOTS login | S2 batches: classes S2N50P1000 / S2N100P1000, commons, `--constraint=cascadelake`, 1G, 08:00:00; initial throttle = 768 − S1 tasks running on commons |
| `sacct_record.sh` | NOTS login | partition record of one batch (JobID, task, Partition, NodeList, Elapsed, State, MaxRSS, node features, CPU model) → `S1S2/logs/sacct_<tag>.tsv` |
| `watch_batch.sh` | Owls (systemd user unit) | per-batch watcher: check, ALERT on STOP (`--cancel-pending-on-stop` cancels the batch's PENDING tasks), at DONE pull + partition record + package. `--suite 2` for S2 |
| `s2_throttle.sh` | NOTS login | re-tunes ONLY the S2 arrays' ArrayTaskThrottle: LOWER when S1 p=5000 pends on our commons QOS cap, else TRACK 768 − S1 commons running |
| `s2_throttle_ctl.sh` | Owls (systemd user timer, 10 min) | one ssh per run to `s2_throttle.sh --apply`; log `_local/engineering/logs/S1S2_throttle.log` |
| `toy_fit.R` | either | environment proof (n=100, p=200) |
| `nots_env.sh` | — | the environment (installed as envs/S1S2/env.sh) |

## Per-class resources (1 CPU per task; the engine is serial)

The harness wall timeout is the Slurm time minus 300 s (p=5000: 86,100 s). Batch 1 ran p=5000 at 12 h; 10 of 200 fits timed out, so HQ raised p=5000 to 24 h (2026-11-26).
p=5000 tasks are pinned to the Sapphire Rapids commons nodes (`--constraint=sapphirerapids`; override `CONSTRAINT_<class>=` to unpin): in batch 1 the Cascade Lake nodes ran 1.2–2.4× slower and hosted 8 of the 10 timeouts.

| class | settings | mem | time |
|---|---|---|---|
| P5000N1000 | S1_13–16 | 8G | 24:00:00 |
| P5000N500 | S1_05–08 | 8G | 24:00:00 |
| P500N1000 | S1_09–12 | 2G | 02:00:00 |
| P500N500 | S1_01–04 | 2G | 02:00:00 |

All classes use partition `commons` (QOS `nots_commons`: 24 h max; per user 1,536 CPUs, 2,304G mem, 5,000 submitted). The per-user caps are shared with every other fb31 job. Override per class with `MEM_<C>`, `TIME_<C>` or `PART_<C>` (for example `PART_P5000N500=long TIME_P5000N500=2-00:00:00`; QOS `nots_long` allows 3 d and 384 CPUs per user).

## Procedure
```bash
# 0 (Owls) deploy from the manager's commit, then check the manifest hash it prints
Experiments/S1S2/slurm/deploy_to_nots.sh --commit <HASH>
# 1 (NOTS) validate batch k; nothing is queued
D=/home/fb31/SMC-BVS/_local/engineering/S1S2/deploy/S1S2/slurm
$D/submit_batches.sh --batch 1 --reps 1-25 --test-only
# 2 (NOTS) ONLY after "SUBMIT BATCH 1"
$D/submit_batches.sh --batch 1 --reps 1-25 --go
# 3 (NOTS) health check while running and after the batch ends; STOP -> report to the manager, submit nothing more
$D/check_batch.sh --batch 1 --reps 1-25
# 4 (Owls) after a PASS: pull + verify, then package
Experiments/S1S2/slurm/pull_to_owls.sh --reps 1-25 --tag b1
Experiments/S1S2/slurm/package_for_desktop.sh --batch 1 --reps 1-25 --manifest <runs/S1S2/_manifests/pull_b1_*.sha256>
# 5 (Owls) once the desktop lists S1S2_smcbvs_b1 in crews/offload/desktop_verified.txt (pulls hourly at :20)
Experiments/S1S2/slurm/free_nots_scratch.sh --batch 1 --manifest <same manifest>          # dry run
Experiments/S1S2/slurm/free_nots_scratch.sh --batch 1 --manifest <same manifest> --go
# later batches (after the manager releases them): --reps 26-50 / 51-75 / 76-100, optionally chained with
#   --dependency afterany:<jobids of the previous batch>   (only after the manager's go)
```
To re-run failed tasks, resubmit the same batch: tasks whose records are ok exit at once.

## STOP rule (check_batch.sh)
STOP and report if any of these holds:
- any task is FAILED, TIMEOUT, OUT_OF_MEMORY, NODE_FAIL or CANCELLED;
- any record is `failed: …` (including `failed: harness wall timeout`);
- any task has no record after its job ended;
- `checks_passed_final == FALSE` (an engine E-flag: E1, E2, E3 or low ESS) in more than 5% of the ok fits, overall or in any class.

Escalation (tier 1) and calibration triggers are reported separately; they do not trigger STOP.

# Benchmark grids (S1 cheap four, S2 five methods): run book

Owner GO via HQ (2026-11-26/27). S2: lasso_cv, scad, susie, bas_mc3, asi = 120 settings × 100 reps each. S1: lasso_cv,
scad, susie, bas_mc3, asi = 16 settings × 100 reps each (S1 asi signed by the owner 2026-11-27).
Same staged protocol as SMC-BVS: batch 1 = reps 1–25 (automatic check), then 2 = 26–60, 3 = 61–100; same watcher,
verdict, pull, partition record, packaging; a STOP cancels the batch's pending tasks. Queue order (owner 2026-11-27):
S1 SMC-BVS tail (never touched) > S1 cheap four (all batches) > S1 asi (staged batches) > S2 cheap four > S2 asi batch 1;
the throttle enforces it (below). **Nothing is submitted until the manager relays the GO for that (suite, method, batch).**

## Files (benchmarks)

| file | runs on | purpose |
|---|---|---|
| `bench_budget.tsv` | — | per (suite, method): `block` (reps per array task), `budget_cpuh` (HARD stop, billed CPU-h of all the method's jobs), `fit_limit_sec` (per-rep wall limit), `mem`, `mem_p5000` (S1 p=5000 classes), `hold`, `ctrl` (adapter ctrl JSON), `fit_limit_p5000` / `ctrl_p5000` (S1 p=5000 settings; `-` = same as p=500). Change values here, then regenerate the task lists and redeploy |
| `make_bench_tasks.sh` | either | writes `tasks_S<suite>_bench_<method>.tsv`: one row per (setting, block of reps), blocks never cross a batch boundary; `task_id = (cell-1)*100 + rep_lo` (the SMC-BVS formula; block 1 = the SMC-BVS ids) |
| `tasks_S<suite>_bench_<method>.tsv` | — | task lists (task_id, setting_id, rep_lo, rep_hi, batch); submit_bench.sh refuses a deploy whose list differs from make_bench_tasks.sh's |
| `bench_array.sbatch` | NOTS (Slurm) | one task = one (suite, method, setting, block): ONE R process (`run_one.R --reps`) loads the adapter once and loops the reps; per-rep watchdog (fit_limit_sec) kills the R process group, writes `failed: harness wall timeout <s>s` for that rep (computational failure) and restarts R for the rest; ok reps are skipped (idempotent). Sources `envs/S1S2/env_bench.sh` |
| `submit_bench.sh` | NOTS login | `--suite 1|2 --method M --batch K --reps LO-HI`: one array per class, `--constraint=cascadelake`, job names `s<suite>bm_<M>_b<K>_<class>`, submissions.tsv batch field `S<suite>bm.<M>.<K>` (column 6: `owner_ok_asi_full` or `-`); prints by default, `--test-only` validates, `--go` submits (refuses: same batch queued; budget reached; asi batch ≥ 2 without `--owner-ok-asi-full`; S1 asi) |
| `check_bench.sh` | NOTS login | benchmark verdict (called as `check_batch.sh --method M`), see the STOP rule below; per-rep table `S1S2/logs/check_s<suite>bm_<M>_b<K>.tsv` |
| `install_md5_ref.sh` | Owls | builds the SMC-BVS data_md5 index (`harness/md5_index.R`) from the Owls copies and installs it as `nots:…/S1S2/ref/smcbvs_data_md5.tsv` (+ .sha256, verified) |
| `harness/md5_index.R` | either | the index: suite, setting_id, rep, data_md5 of every SMC-BVS record with a data_md5 written by R 4.5.2 (NOTS); errors on a path/field mismatch or a conflict between roots |

`check_batch.sh`, `watch_batch.sh`, `pull_to_owls.sh`, `sacct_record.sh`, `package_for_desktop.sh` take `--method M`
(default `smcbvs` = unchanged). Records: `/scratch/fb31/SMC-BVS/runs/S1S2/<M>/S<suite>_xx/rep_RRR.{json,rds}` on NOTS,
`…/_local/engineering/runs/S1S2/<M>/…` on Owls. Pull/record tag `<M>_s<suite>b<K>`; desktop unit `S1S2_<M>_s<suite>b<K>`.

## Per-(suite, method) resources (bench_budget.tsv; 1 CPU per task, billed as 2)

| suite | method | block | tasks b1/b2/b3 | per-rep limit | Slurm time | mem (p=5000) | budget (billed CPU-h) |
|---|---|---|---|---|---|---|---|
| S1 | lasso_cv | 25 | 16 / 32 / 32 | 600 s | 04:20:00 | 2G (4G) | 50 |
| S1 | scad | 10 | 48 / 64 / 64 | 600 s | 01:50:00 | 2G (4G) | 50 |
| S1 | susie | 10 | 48 / 64 / 64 | 600 s | 01:50:00 | 2G (4G) | 50 |
| S1 | bas_mc3 | 5 | 80 / 112 / 128 | 1,800 s | 02:40:00 | 4G (12G) | 50 |
| S1 | asi | 1 | 400 / 560 / 640 | 7,200 s (p=5000: 28,800 s) | 02:10:00 (08:10:00) | 2G (4G) | 7,080 |
| S2 | lasso_cv | 25 | 120 / 240 / 240 | 600 s | 04:20:00 | 2G | 50 |
| S2 | scad | 25 | 120 / 240 / 240 | 600 s | 04:20:00 | 2G | 50 |
| S2 | susie | 25 | 120 / 240 / 240 | 600 s | 04:20:00 | 2G | 50 |
| S2 | bas_mc3 | 5 | 600 / 840 / 960 | 1,800 s | 02:40:00 | 6G | 112.5 |
| S2 | asi | 1 | 3,000 / 4,200 / 4,800 | 10,800 s | 03:10:00 | 2G | 20,332.5 |

Slurm time = block × per-rep limit + 600 s. Memory from Owls `/usr/bin/time -v` MaxRSS (2026-11-27, rep 1-2):
lasso_cv 0.24 / 0.33–0.49 GB (S2 / S1 p=5000), scad 0.14 / 0.25–0.39, susie 0.28 / 0.40–0.50, bas_mc3 0.38–1.9 (S2;
n = 50 is the heavy one) / 0.6–0.9 (S1 p=500) / 2.6–4.7 GB (S1 p=5000), asi 0.16 GB (R + Octave, first 165 s of an S2
fit). Budgets: lasso_cv/scad/susie 50 = approved floor; bas_mc3 S2 112.5 and asi 20,332.5 = mean S2 smoke runtime × 2 ×
12,000 × 1.5 / 3600; S1 cheap four 50 each (floor; the smoke × 1.5 numbers are all below); S1 asi 7,080 (owner). asi
`ctrl` `{"timeout_sec":…}` = the adapter's own Octave limit, 300 s under the per-fit limit (S2 10,500 of 10,800; S1 6,900 of
7,200 at p=500, 28,500 of 28,800 at p=5000; adapter default 8 p s). S1 asi per-fit limits (owner): p=500 2 h, p=5000 8 h
(Owls: 1,300–1,500 s and 8,900–9,550 s); memory 2G / 4G (owner; Owls asi RSS 0.16 GB on S2).
asi on S2 (only) is ON HOLD after batch 1 until the owner OKs the full grid (`hold = owner_ok_after_b1`; `--owner-ok-asi-full`).
MaxSubmitPU 5,000 counts array tasks: asi batches 2 (4,200) and 3 (4,800) must go one class at a time
(`--classes S2N50P1000`, then `S2N100P1000`) unless the queue is nearly empty.

## Concurrency (shared with the S1 SMC-BVS tail)
HARD ceiling 468 running benchmark tasks in total (s1bm_* + s2bm_*, all methods). submit_bench.sh sets the initial
`%K` (sum over the batch's arrays) to min(468, 768 − max(300, S1 SMC tasks on commons) − other fb31 tasks on commons)
minus the benchmark tasks already running; `s2_throttle.sh` (Owls timer `s1s2-s2throttle`, every 10 min, `--reserve
300`) now manages s2smc_* + s1bm_* + s2bm_* as one pool: it LOWERs the pool when any S1 SMC-BVS task (s1smc_*) pends on
commons behind our per-user QOS cap (CPU: 1 slot each; memory: ceil(S1 task mem / smallest pool task mem) each), else
TRACKs 768 − max(300, S1 commons running) − other commons running, and never above `--bench-cap` (468). It also reports
billed CPU-h per (suite, method) and holds an over-budget method's arrays at 1. Benchmarks are pinned to Cascade Lake;
S1 SMC-BVS keeps the Sapphire Rapids nodes.

**Priority inside the benchmark pool** (owner 2026-11-27). Tiers by job name: 1 `s1bm_<cheap four>_*`, 2 `s1bm_asi_*`,
3 `s2bm_<cheap four>_*`, 4 `s2bm_asi_*` (0 = `s2smc_*`, complete). Each array with pending tasks keeps a floor of 1
(Slurm: 0 = unlimited); the rest of the pool total goes tier by tier, highest first, each tier taking at most its
running + pending tasks. So a lower-priority array's throttle is lowered whenever a higher-priority array has pending
tasks: it gets only what the higher tiers' running and pending tasks leave, possibly just 1 (below its running count:
it starts nothing until its tasks end, and the slots go to the higher tier). Within a tier the former split applies
(keep running, share free slots by pending tasks). submit_bench.sh also subtracts the higher tiers' pending tasks from
the initial `%K`. Example (fake squeue, TRACK, total 468): S1 lasso r10/pd30 → 40, S1 asi r100/pd200 → 300,
S2 lasso r150/pd50 → 127, S2 asi r50/pd1000 → 1.

## Procedure (example: S1 lasso_cv batch 1)
```bash
# 0 (Owls) deploy from the manager's commit (installs env.sh and env_bench.sh); then the md5 reference index
Experiments/S1S2/slurm/deploy_to_nots.sh --commit <HASH>
Experiments/S1S2/slurm/install_md5_ref.sh            # re-run after the last S1 SMC-BVS fits are pulled, before freeing scratch
# 1 (NOTS) print / validate; nothing is queued
D=/home/fb31/SMC-BVS/_local/engineering/S1S2/deploy/S1S2/slurm
$D/submit_bench.sh --suite 1 --method lasso_cv --batch 1 --reps 1-25 --test-only
# 2 (NOTS) ONLY after the GO for (S1, lasso_cv, batch 1)
$D/submit_bench.sh --suite 1 --method lasso_cv --batch 1 --reps 1-25 --go
# 3 (Owls) watcher: check every INTERVAL, STOP -> cancels pending; at the end pull + partition record + package (PASS)
LOG=/home/fb31/Bayesian-Variable-Selection/_local/engineering/logs/S1S2_watch_s1bm_lasso_cv_b1.log
systemd-run --user --unit=s1s2-watch-s1bm-lasso_cv-b1-$(date +%Y%m%d-%H%M%S) --collect --quiet \
  -p StandardOutput=append:$LOG -p StandardError=append:$LOG \
  /home/fb31/BVS-wt/P1M/Experiments/S1S2/slurm/watch_batch.sh --suite 1 --method lasso_cv --batch 1 --reps 1-25 --interval 600 --log $LOG
# S1 asi: the same with --method asi (p=500 tasks 02:10:00, p=5000 08:10:00; one rep per task)
# manual equivalents: check_batch.sh --suite 1 --method lasso_cv --batch 1 --reps 1-25 (NOTS);
#   pull_to_owls.sh --suite 1 --method lasso_cv --reps 1-25 --tag lasso_cv_s1b1;
#   sacct_record.sh --suite 1 --method lasso_cv --batch 1 (NOTS);
#   package_for_desktop.sh --suite 1 --method lasso_cv --batch 1 --reps 1-25 --manifest <…/pull_lasso_cv_s1b1_*.sha256> --slurm-tsv <…>
```
To re-run failed reps, resubmit the same batch after it has ended: reps whose json is ok are skipped.
```bash
# 4 (Owls) free the NOTS scratch copy of a benchmark batch: only after the desktop lists S1S2_<M>_s<suite>b<K> in
#   crews/offload/desktop_verified.txt (G1) and the Owls copies / unit tars re-hash (G2, G3); G4 re-hashes on NOTS before rm
Experiments/S1S2/slurm/free_nots_scratch.sh --method lasso_cv --suite 1 --batch 1 --manifest <pull manifest of lasso_cv_s1b1>   # dry run
Experiments/S1S2/slurm/free_nots_scratch.sh --method lasso_cv --suite 1 --batch 1 --manifest <same manifest> --go
# 5 (Owls) tables: per method (incl. benchmarks) and paired vs SMC-BVS (outputs in specs/, gitignored)
Rscript Experiments/S1S2/harness/aggregate.R --method lasso_cv --suite 1          # results_S1_lasso_cv.{tsv,md}
Rscript Experiments/S1S2/harness/aggregate.R --method smcbvs --suite 1 --final    # refuses while a timeout stub's task is queued
Rscript Experiments/S1S2/harness/paired.R --suite 1 [--methods lasso_cv,scad,susie,bas_mc3,asi] [--reps 1-100] [--pairing joint|pairwise]
Rscript Experiments/S1S2/harness/test_aggregate_supersede.R                         # offline test of aggregate.R's record rules
```
aggregate.R appends hamming_mean, TP_mean, FP_mean, FN_mean, F1_mean (failed or missing record = Ŝ = ∅) after the existing
columns; benchmarks have NA E-flag columns. Both scripts read only `<runs>/<M>/<setting>/rep_RRR.json` (never
`_superseded/` or audit folders) and stop on a json whose setting_id / rep / method differs from its path or on a
duplicate record. paired.R pairs on (setting, rep) with equal data_md5 (mismatches counted and listed), McNemar exact p on
the exact-recovery discordant pairs and a sign test on Hamming; joint pairing = the rule of
reports/S1S2/scripts/build_S1_comparison.R (numbers agree exactly on S1 reps 1–25, 2026-11-27).

## Benchmark STOP rule (check_bench.sh; no E-flag rule)
STOP (and the watcher cancels the batch's pending tasks) if any of these holds:
- failed records (`failed: …`, including the watchdog's `harness wall timeout`) plus crashed reps (no record although
  their array task has ended; at batch end every missing rep) exceed 5% of the finished reps, overall or in a class;
  while tasks are still pending/running a group needs ≥ 20 finished reps before the 5% line applies (noise guard);
- any task OUT_OF_MEMORY or NODE_FAIL;
- the method's billed CPU-h (sacct CPUTimeRAW of ALL its `S<suite>bm.<M>.*` jobs, running tasks included) ≥ its budget;
- any data-identity problem: a record's data_md5 differs from the SMC-BVS record of the same (suite, setting, rep)
  (index first, live NOTS json for reps not in the index), an ok record has no data_md5, or no reference exists.
  Both sides are NOTS R 4.5.2 records with digest/jsonlite from the R module, so equality is exact.
PASS at batch end otherwise (no REVIEW band).
