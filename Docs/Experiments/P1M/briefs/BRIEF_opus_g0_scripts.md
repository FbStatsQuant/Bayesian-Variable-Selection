# BRIEF — G0 batch scripts (Opus 5.5 helper, high). SMC - Engineering Department, 2026-11-15

Goal: prepare, **but not submit**, the NOTS batch for gate G0 of `ENGINEERING_SPEC.md` §0-v2.6, and dry-run it locally on
Owls. The Engineering manager and HQ review it; HQ gives the go per batch. You have read-only NOTS access via `ssh nots`
(squeue, sacct, sinfo, ls/reading under /scratch/fb31 and /home/fb31/projects/BVS/theory_w3). **Never run sbatch or srun.
Never touch `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/` or `/projects/ml75`.**

Owner memo (POLICIES.md 34ce461a): solve technical problems inside the department; no Fable without approval; report big
problems at once. You start no sub-agents.

## Write only under `Docs/Experiments/P1M/g0/` in `/home/fb31/Bayesian-Variable-Selection`
No other repo file. No git state change. Local scratch: `/home/fb31/p1m_g0_dryrun/` (create it).

## Part K — kernel benchmark on one Sapphire Rapids node
- Program: `/home/fb31/p1m_feas_bench/feas_bench.cpp` (+ `core_copy/`). Read its header and `run1.sh` / `run2.sh` /
  the logs. Copy what you need into `g0/kernel/`; do not edit the original folder.
- Deliver:
  - `g0/kernel/build.sh`: builds on a NOTS compute node with the NOTS toolchain (GCC 14.3.0, as in the W3-SCALE env
    `git show origin/theory/W3-SCALE:Theory_work/Wave3/W3-SCALE/nots/env_scale.sh`); `-march=sapphirerapids`, keeping
    `-ffp-contract=off`.
  - `g0/kernel/run_kernel.sbatch`: commons, `--constraint=sapphirerapids`, `--cpus-per-task=96`, `--mem=32G`,
    `--time=00:30:00`.
    - Threads T ∈ {1, 24, 48, 96}: `bw`, `perm`, `direct` at p = 10⁶, and `batch` variants 0 and 2 at p = 10⁶ (S₀-alone,
      S₀ + 1 null, 256 distinct supports), plus the bit checks at T = 1.
    - Record `lscpu`, the node name and `date` in the log.
    - Target wall time ≤ 20 min, i.e. ≤ 32 billed core-h.
  - **Store-offer cost** (missing from the expert's benchmark): add a mode `offer` that times inserting scored models into
    a bounded top-c store of capacity 4·10⁷ under a strict order (flat arrays or a heap; your choice, documented), with
    the realistic acceptance ratio implied by the `batch` runs. Report ns per offer.
- Dry run on Owls: build with the local gcc (`-march=native`) and run every mode at p = 10⁵ with T ≤ 4 and
  `nice -n 19`, ≤ 10 min total. Save the log in `g0/kernel/owls_dryrun.log`.

## Part S — stage-level island records at p = 5k and 10k with the existing code (revision D, unmodified)
- Purpose: where the dispersion of log Ẑ_r arises. The per-stage log increments and ESS of every final island are needed
  for 16 islands of N = 2,500 on a frozen tier-0 grid, plus `gibbs_change` (accepted Gibbs moves) per stage.
- Start from the W3-SCALE driver `git show origin/theory/W3-SCALE:Theory_work/Wave3/W3-SCALE/scripts/census_measure.R`
  (+ `ws_common.R`, `nots/run_task.sh`, `nots/submit.sh`, `nots/env_scale.sh`). Find out which records it drops, and
  write `g0/stage/stage_measure.R`, which keeps, per island:
  - the full stage table (φ, log increment, cumulative log Z, ESS, distinct_resampled, distinct_moved, the move counts
    incl. gibbs_change);
  - the top-store F values (for log Σ e^F);
  - the terminal particle supports if they are reachable without changing the core; if not, say so.
- The code under test is **revision D unmodified**. On NOTS it is at `/scratch/fb31/w3scale/code/v32dev_6866f57`; check by
  `ls` and hash. The driver may call internal functions, but must not edit core files.
- Datasets: the S3-type datasets of the B3 census (same generator and seed as W3-SCALE used, so the results line up with
  `b3_census.tsv`): p = 5k and 10k, n = 200.
- Deliver:
  - `g0/stage/stage_measure.R`;
  - `g0/stage/run_stage.sbatch`: one task per p, 2 CPUs (single thread), `--mem` from the B3 MaxRSS × 2, time limit from
    the B3 timings × 1.5 (B3: tier-0 calibration 1.9 h at 5k and 5.9 h at 10k; one island 0.17 h at 5k and 0.7 h at 10k);
  - `g0/stage/README.md` with the expected core-h.
- Dry run on Owls at p = 1,000 (and 2,000 if under 10 min), 4 islands, nice 19. It must produce the records. Compile the
  core in `/home/fb31/p1m_g0_dryrun/` from a copy, never inside the repo.

## Also deliver
`g0/README.md`:
- what each job does;
- the exact sbatch commands HQ would run;
- the expected billed core-h per job (allocated CPUs × wall limit = the worst case; plus the expected value);
- the output paths (under `/scratch/fb31/p1m/g0/`);
- the read-back and analysis steps;
- what is NOT checked by the dry run.

Final message: at most 12 lines: what was built, the dry-run results, the total worst-case core-h, and anything blocking.
