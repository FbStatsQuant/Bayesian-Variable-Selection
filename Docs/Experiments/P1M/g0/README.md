# G0 batch: kernel benchmark on one Sapphire Rapids node, plus stage-level island records at 5k and 10k

SMC - Engineering Department, 2026-11-15. Prepared by the Opus 5.5 helper (`briefs/BRIEF_opus_g0_scripts.md`).
Gate G0 is in `ENGINEERING_SPEC.md` §0-v2.6.
- **Not submitted.** The Engineering manager deploys and submits after review and HQ's go. Helpers never run sbatch.
- **HQ approval:** ≈ 65 billed core-h, worst-case admission ≤ 71.5.
- **This batch:** **worst case 57.0 billed core-h** (8.0 kernel + 49.0 stage); expected ≈ 37.

## 1. The two jobs
| job type | script | what it does |
|---|---|---|
| **kernel** (Part K), array of 1 | `kernel/run_kernel.sbatch` | One SPR node (96 CPUs = 48 cores × 2 hyperthreads, 32G, 5 min).<br>Builds `g0_bench` on the node: GCC 14.3.0, `-O3 -march=sapphirerapids -ffp-contract=off -fno-math-errno -fopenmp`, libmvec.<br>Records the node name, `date`, `lscpu`, `numactl -H` and the cpuset.<br>Runs `g0_bench suite 1000000 1,48,96,24 …` (below), then ends. |
| **stage** (Part S), array of 2 | `stage/run_stage.sbatch` | Revision D unmodified. The core at `/scratch/fb31/w3scale/code/v32dev_6866f57` is checked against `stage/revD_SHA256SUMS` before use.<br>Task 1: p = 5k, tier-0 calibration + 16 islands.<br>Task 2: p = 10k, calibration + 8 islands.<br>N = 2,500, frozen grid, same dataset and seed as B3 (`b3_census.tsv`). Every island's stage table is kept, with `gibbs_change`, the top-store F values and the calibration's diagnostic islands. Details in `stage/README.md`. |

### What `g0_bench suite` runs
`kernel/g0_bench.cpp` = the feasibility benchmark's arithmetic (`/home/fb31/p1m_feas_bench/feas_bench.cpp`, copied
verbatim up to `draw_order`). The changes are:
- the drivers are refactored so that one process generates the data and the 256 round orders once;
- the new `offer` mode;
- the pass-fraction counters.

The suite runs:
1. **Store self-test** against a brute-force top-c (duplicates, exact F ties).
2. **For T = 1, 48, 96, 24**, in that order:
   - `batch` class A (variant 2) and bit form (variant 0), each on 256 distinct random supports and on S₀ alone. At
     T = 1, 10% of the tiles are processed (a stride sample); at T ≥ 24, all of them;
   - `direct` (200k steps per thread; 100k at T = 1);
   - `perm` (round order + inverse; every thread its own);
   - `bw` (4 GB read).
   - Bit checks run **at T = 1 only**, on small samples:
     - bit form vs `v3::Scorer` on 2 tiles × 16 supports × 128 labels = 4,096 scores, exact bits;
     - class A on the same 4,096 scores, relative error ≤ 1e-9;
     - direct: 2,000 steps, exact bits.
3. **Pass fractions** (untimed; T = 96): the share of scores with F(S ∪ j) − F(S) ≥ −Δ for Δ ∈ {0, 5, 10, 12, 14, 16, 20, 30}. Supports: 256 distinct, S₀, and S₀ + 1 null.
4. **Store offers** (`offer`): a bounded top-c store of capacity c = 4·10⁷ under the strict HPM order.
   - Structure (a documented choice):
     - flat arrays per slot (F, 64-bit Zobrist hash, size, 8 members);
     - a binary min-heap of slots, whose root is the worst kept model;
     - quick reject = one compare with the root;
     - duplicates found in an open-addressing hash table (linear probing, backward-shift deletion), each hit confirmed on the members.
   - Unit costs per offer: REJECT, DUP-RANDOM (cold probe), DUP-HOT, NEW (replace the root), FILL, plus two mixes.
   - At T = 1 one store of 4·10⁷; at T > 1, one store of 4·10⁷/T per thread, so the total memory stays the same.

The `batch` runs report the realistic ratios: accepted moves per score (8·10⁻⁷ to 7·10⁻⁶ on Owls) and the pass
fractions. The store **threshold** decides the offer cost, because nearly every score is within 16 log units of its
support at p = 10⁶ (Owls: pass fraction 0.10 at Δ = 14, 1.0 at Δ = 16). See §5 for how the cost is combined.

**Time.** The Owls sizing run at p = 10⁶ (T ≤ 4, loaded machine) took 76 s with a peak RSS of 6.5 GB. On SPR the whole
job should take ≈ 2–2.5 min, build included. The suite runs under `timeout 240`, so the log is complete before the
5-minute limit. The most important items run first.

## 2. Deploy and submit (Engineering manager; HQ's go per batch)
1. On Owls, from the repo root (one rsync and one check over the multiplexed `ssh nots`):
   ```
   bash Docs/Experiments/P1M/g0/deploy_g0.sh
   ```
   This copies the files listed in `deploy_g0.sh` to NOTS `~/SMC_Engineering_Department/scripts/g0/` and checks them
   against `SHA256SUMS`.
2. On NOTS, in one login:
   ```
   bash ~/SMC_Engineering_Department/scripts/g0/submit_g0.sh all      # or: kernel | stage
   ```
   This runs exactly:
   ```
   cd ~/SMC_Engineering_Department/scripts/g0
   sbatch --parsable kernel/run_kernel.sbatch                          # array 1,   96 CPUs, 32G, 00:05:00, SPR
   sbatch --parsable stage/run_stage.sbatch                            # array 1-2, 1 (=2 billed) CPU, 5G, 17:30:00, SPR
   scontrol update JobId=<stage job>_1 TimeLimit=07:00:00              # 5k task down to 7 h
   ```
   It appends each submission (job id, worst case, script hash) to `scratch/runs/g0/submissions.jsonl`. If the
   `scontrol update` fails, it says so: the stage worst case is then 70 core-h. Task 1 still stops itself at 6 h 57 min.
3. Monitoring: no loop. At most once every 5 minutes, one call for both jobs:
   ```
   squeue -u fb31 -n p1m_g0_kernel,p1m_g0_stage -o '%.18i %.14j %.8T %.10M %.10l %.6C %R'
   ```
   After the end, one `sacct -j <kernel job>,<stage job> --format=JobID,State,Elapsed,MaxRSS,AllocCPUS,NodeList -P`.

## 3. Billed core-h (NOTS bills per hardware thread)
| job | allocation | time limit | **worst case** (CPUs × limit) | expected |
|---|---|---|---|---|
| kernel (1 task) | 96 CPUs | 00:05:00 | **8.0** | ≈ 3–4 (2–2.5 min) |
| stage task 1, p = 5k, 16 islands | 2 CPUs | 07:00:00 | **14.0** | ≈ 9.4 (1.9 h calibration + 16 × 0.17 h) |
| stage task 2, p = 10k, 8 islands | 2 CPUs | 17:30:00 | **35.0** | ≈ 23.4 (5.9 h + 8 × 0.7 h) |
| **total** | | | **57.0** (≤ 71.5 approved) | **≈ 37** |

- The stage limits are 1.5 × the B3 timings.
- The stage `--mem` (5G) is 2 × the B3 MaxRSS (1.22 / 2.38 GB), rounded up. Memory is not billed.
- The stage runtime guard (`--hours` 6.70 / 17.20) ends a run cleanly before its limit. Finished islands are kept.

## 4. Output paths (NOTS; heavy data under `~/SMC_Engineering_Department/scratch` = `/scratch/fb31/SMC_Engineering_Department`)
| what | path |
|---|---|
| scripts (light, deployed copy) | `~/SMC_Engineering_Department/scripts/g0/{kernel,stage}/` |
| kernel build | `scratch/runs/g0/build/kernel_<array job>/` (`g0_bench`, `build_info.txt`) |
| kernel run | `scratch/runs/g0/kernel_<array job>/kernel.log`, `build_info.txt` |
| stage run | `scratch/runs/g0/stage_<array job>/res/stage_p5000.rds`, `res/stage_p10000.rds`, and `log/` (task logs, `starts.jsonl`, `ends.jsonl`, script hashes) |
| Slurm stdout and stderr | `scratch/slurm_out/p1m_g0_kernel_<A>_1.{out,err}`, `p1m_g0_stage_<A>_{1,2}.{out,err}` |
| TMPDIR | `scratch/tmp/<SLURM_JOB_ID>/`, removed at job end |
| submissions ledger | `scratch/runs/g0/submissions.jsonl` |
| small read-back tables | `~/SMC_Engineering_Department/results/g0/` (§5) |

**INDEX entries the jobs add.** The manager adds these to the NOTS `~/SMC_Engineering_Department/INDEX.md` at
deploy and submit time:
- `scripts/g0/` — G0 scripts (deployed from repo `Docs/Experiments/P1M/g0/`, SHA256SUMS inside);
- `scratch/runs/g0/` — G0 runs: `kernel_<A>/`, `stage_<A>/`, `build/`, `submissions.jsonl`;
- `scratch/slurm_out/p1m_g0_*` — G0 Slurm logs;
- `results/g0/` — G0 read-back tables (§5).

**On Owls (added by this helper):**
- `tmp/20261115-g0-dryrun/` (TMPDIR of the dry runs; removed at the end);
- `bench/20261115-g0-kernel/` (the Owls build and dry-run log of `g0_bench`).

The stage dry run itself lives in `/home/fb31/p1m_g0_dryrun/`. It was started before the folder rule; the manager
moves it.

## 5. Read-back and analysis
### Kernel
```
bash ~/SMC_Engineering_Department/scripts/g0/kernel/kernel_summary.sh scratch/runs/g0/kernel_<A>/kernel.log > results/g0/g0_kernel.tsv
```
1. **Correctness first.**
   - Every `_mism` row must be 0/n: bit form and direct exact, class A ≤ 1e-9.
   - The store self-test line must say "0 of 20 trials failed".
2. **Per (support, label) cost c_s(T).** Use the wall-based column `ns_wallxT` = wall × T / scores, which includes
   load imbalance. Take class A (`batch_*_v2`) for V and the bit form (`_v0`) for T. Bracket the support mix:
   - `distinct256`: |A| ≈ 1,280, conservative;
   - `S0`: shared supports, optimistic.
3. **Offer cost per score:** c_offer = (1 − π)·REJECT + π·[(1 − ν)·DUP + ν·NEW].
   - π = the pass fraction at the store threshold Δ = F(S) − F_min(store). Read π from the `pass_*_D*` rows. Estimate
     Δ from the stage records: F_HPM − min(store$F) at 5k and 10k, with c = 40p + 1, extrapolated to 10⁶.
   - ν = the share of passes that are new models.
   - DUP lies between DUP-HOT and DUP-RANDOM.
   - The two MIX rows check that the sum is linear (branch effects).
4. **Round-order cost per label:** c_perm = `perm_fy` + `perm_inv`.
5. **Cost per elementary step:** c = M·(c_s + c_offer) + c_perm.
   - M = 1 + accepted Gibbs moves per particle-round. Take it from the stage records, `mean_gibbs_change_per_particle`
     at φ near 1 and in the terminal rounds, and from the P6 stage tables. The planning value is M = 3.
6. **Billing.** The plan's thresholds are in thread-ns at 2 billed CPUs per thread. With 96 allocated CPUs, the
   billed-equivalent cost is c × 96 / (2T): c itself at T = 48 (one thread per core), c / 2 at T = 96 (hyperthreads
   counted). Report both. The T = 24 row shows the scaling only.
7. **Gate:**
   - c ≤ 700 ns → precise plan;
   - 700–1,500 → baseline precision, 3 fits at 1M;
   - > 1,500 → stop and report.

### Stage
```
Rscript --vanilla ~/SMC_Engineering_Department/scripts/g0/stage/stage_readback.R ~/SMC_Engineering_Department/results/g0 \
  scratch/runs/g0/stage_<A>/res/stage_p5000.rds scratch/runs/g0/stage_<A>/res/stage_p10000.rds
```
This writes `g0_stage_long.tsv`, `g0_stage_dispersion.tsv`, `g0_islands.tsv`, `g0_runs.tsv` and
`g0_calib_stage_long.tsv` (small; base R, no core needed).
1. **Line-up and status first.** In `g0_runs.tsv`:
   - `b3_grid_identical` and `b3_log_Z_r_identical` should be TRUE (16 islands at 5k, 6 at 10k);
   - `status` is `done`, or a guard stop with the finished islands kept.
2. **Where var(log Ẑ_r) arises.** Compare var(log Ẑ_r) with Σ_t var(log increment_t) (`sum_var_inc`): a gap means
   covariance across stages, i.e. lineage effects. Then:
   - find the stages that carry most of the variance and their φ (`g0_stage_dispersion.tsv`);
   - relate them to `min_ess_share`, the distinct counts and `gibbs_state_changes`;
   - check whether the right-tail island at 5k (B3: −114.0 vs about −115.5) gains its excess in a few early stages or
     spread out (`g0_islands.tsv`: `stage_max_dev`).
3. **M.** `mean_gibbs_change_per_particle` by stage, and the terminal rounds, from `rec$final$terminal_tables`.
4. **Store.**
   - `store$F`: log Σ e^F, its range F_max − F_min, and its sizes. This gives the store threshold Δ for the offer cost.
   - The store is the run's merged store (one ledger per call), not a per-island store.
5. **Calibration replicates.** The diagnostic-island stage tables in `g0_calib_stage_long.tsv` are free replicates on
   rebuilt grids (4 islands per iteration, H = 512 particles).

## 6. Owls dry runs (nice 19, ≤ 4 cores, TMPDIR in the department folder)
### Kernel
`kernel/owls_dryrun.log`: p = 10⁵, T = 1, 3, 2, every mode, offers at c = 4·10⁷.
- Built by `build.sh owls`: gcc 11.5, `-march=native` on Xeon Gold 6148 (Skylake with AVX-512).
- 44 s; peak RSS 3.7 GB.
- Store self-test 0 of 20 failed. Bit form 0 mismatches of 4,096 (×2 supports); class A 0 of 4,096 (×2); direct 0 of 1,999.

Owls was shared and heavily loaded (load average 40–420), so its timings are not SPR numbers. For orientation:

| T | class A, 256 distinct | class A, S₀ | bit form, 256 distinct | bit form, S₀ | direct |
|---|---|---|---|---|---|
| 2–3 | 125–156 ns | 47 ns | 229–235 ns | 163–166 ns | 2,480 ns/step |

The T = 1 S₀ rows at p = 10⁵ use only 40 tiles and are inflated by warm-up; at p = 10⁶ the sizing run gives 48 ns.

| offers, T = 1, c = 4·10⁷ | REJECT | DUP-HOT | DUP-RANDOM | FILL | NEW | MIX (π = 0.01) | MIX (π = 0.10) |
|---|---|---|---|---|---|---|---|
| ns per offer | 6 | 70 | 136 | 174 | 1,670 | 12 | 39 |

`kernel/owls_sizing_p1e6.log`: p = 10⁶, T = 1, 4, the same source. 76 s; peak 6.5 GB. Pass fractions at p = 10⁶:
0.0013 (Δ = 10), 0.011 (Δ = 12), 0.10 (Δ = 14), 1.0 (Δ = 16).

### Stage
STAGE_DRYRUN_RESULTS

## 7. What the dry runs do NOT check
- **NOTS toolchain.** Not run on NOTS:
  - the build with the GCC 14.3.0 module and `-march=sapphirerapids` (Owls used gcc 11.5, `-march=native`). glibc 2.34
    and libmvec are present on the NOTS login node (checked read-only);
  - the `module load` under `--export=NONE`. This is the same pattern as W3-SCALE, which worked.
- **Slurm behaviour.** Array directives, the `--constraint`, the `scontrol update` of task 1, the run-directory and
  TMPDIR creation on scratch, and the output paths (`scratch/slurm_out/` exists).
- **SPR timings and the 5-minute fit.** The T = 24, 48 and 96 runs were never exercised; neither were `OMP_PLACES=cores`
  pinning on the Slurm cpuset and hyperthread sharing at T = 96. The size of the per-T work was chosen from Owls rates.
  If SPR were far slower, `timeout 240` cuts the suite, and the log so far is kept.
- **Kernel memory at 96 threads.** Estimated < 8 GB of 32G; per-thread buffers shrink with T.
- **Stage job on NOTS:**
  - R 4.5.2 loading revision D from its existing `.cpp_cache` (worked for B3);
  - the duration of the 5k and 10k calibrations (taken from B3; a different SPR model can change it);
  - the guard stop near the limit;
  - the B3 line-up (needs the B3 records on NOTS);
  - the record size at 10k (store of 400,001 models; expected tens of MB).
- **Bits of the stage dry run.** The Owls dry run compiled the core with gcc 11.5 and R 4.6.0, so its numbers are not
  bit-comparable with NOTS. It checks the driver's logic and records only.
- **Statistical content.** The dry runs check that the records exist and are consistent, not what they will show.
