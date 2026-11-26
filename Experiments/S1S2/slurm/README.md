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
| `check_batch.sh` | NOTS login | sacct states, record status and engine E-flags, then the STOP verdict |
| `deploy_to_nots.sh` | Owls | deploys from `--commit HASH` (or a worktree snapshot), builds the manifest, installs env.sh |
| `pull_to_owls.sh` | Owls | builds a NOTS sha256 manifest, rsyncs, then runs `sha256sum -c` on Owls |
| `package_for_desktop.sh` | Owls | builds one flat unit (16 tars + one SHA256SUMS) and moves it into `records/` atomically |
| `free_nots_scratch.sh` | Owls | deletes a batch's NOTS copy only after gates G1–G4 (desktop verified + three sha checks). Dry run by default |
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
