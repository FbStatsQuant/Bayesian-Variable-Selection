# G0 Part S: stage-level island records at p = 5k and 10k (revision D, unmodified)

SMC - Engineering Department, 2026-11-15. Prepared, **not submitted**. The Engineering manager submits after review and
HQ's go (see `../README.md`).

## Purpose
Find where the dispersion of log Ẑ_r arises. For each final island, record the per-stage log increments, ESS, distinct
supports and move counts, including `gibbs_change` (accepted Gibbs moves per stage). Also record the top-store F
values and the calibration's own diagnostic islands. All of it runs on a frozen tier-0 grid with N = 2,500, R = 16
islands at 5k and 8 at 10k.

## Files
| file | what |
|---|---|
| `stage_measure.R` | the driver. It is `census_measure.R` (W3-SCALE B3, origin/theory/W3-SCALE 299cbc58) with the records B3 dropped put back in. It calls the same internal functions (`v3_cal_tier`, `cpp_cal_export`, `v3_frozen`, `v3_run_settings`, `cpp_final_run`) and edits no core file. |
| `stage_readback.R` | turns `stage_p*.rds` into five TSV tables (stage long table, per-stage dispersion, islands, runs, calibration stages) |
| `run_stage.sbatch` | Slurm array of 2 tasks: 1 = 5k, 2 = 10k |
| `ws_common.R`, `env_scale.sh` | verbatim copies from W3-SCALE (data generator, argument parser, memory probe; GCC 14.3.0 + R 4.5.2 environment) |
| `revD_SHA256SUMS` | sha256 of the 19 source files of revision D. They were read from `/scratch/fb31/w3scale/code/v32dev_6866f57` on NOTS (11-15) and are identical to `git archive 6866f57 Scripts/SMC_BVS/core_v32dev`. The driver checks the core directory against this list before it sources anything, and stops on any difference or extra file. |

## What B3's `census_measure.R` dropped, and what this driver keeps
- **B3 kept, per N:** log Ẑ_r, sd, R_eff, weights, PIPs at the true variables, the minimum ESS share, island seconds, the HPM, and `island_best`.
- **B3 dropped:** the island stage tables (`phi`, `log_increment`, `cum_log_Z`, `ess`, `distinct_resampled`,
  `distinct_moved`, `stage_moves` with `gibbs` and `gibbs_state_changes` = `gibbs_change`, unit and neighbour swap and
  independence-move counts); the terminal tables (burn-in and measured rounds); `rb_acc` and `rb_round`; the stream
  positions; the whole top store and the leader stores; the calibration's pilot and diagnostic-island stage tables;
  and the local-search record.
- **This driver keeps:**
  - every final island's complete core record (`rec$final$islands[[r]]`), plus tidy `stage_tables[[r]]` and
    `terminal_tables[[r]]`;
  - `stage_dispersion`: per stage, the mean and variance over the islands of the log increment, the variance of the
    cumulative log Z, the ESS shares, mean distinct counts, and `gibbs_state_changes / N` (accepted Gibbs moves per
    particle and round);
  - the calibration's pilot stage table and the stage tables of every diagnostic island (4 per iteration);
  - **the top store:** all F values (`store$F`), sizes, the models, log Σ e^F, the capacity (40p + 1) and the full flag;
    also the γ₀ leader values.
- **Not reachable without changing the core:**
  - *Per-island top stores.* `cpp_final_run` keeps one ledger per call. Its store is the top-(40p + 1) of everything
    scored by all R islands, plus the block-table models and the inherited calibration models. It is recorded as the
    run's merged store.
  - *Terminal particle supports.* The population is local to `Engine::run_island_s` (`v3_engine.h`), and
    `island_to_list` (`v3_core.cpp`) does not return it. No exported function exposes it.

## Line-up with B3
- Same generator, same seed, same core, same calibration budget. The grid should therefore be identical to B3's, and
  island r should be the same computation as B3's island r: streams 10..9+R, one final-run call.
- With `--b3-rds` (the job passes the B3 census records, read only), the driver records:
  - `b3_lineup$grid_identical`;
  - whether log Ẑ_r is identical on the islands both runs finished: 16 at 5k; 6 at 10k, where B3 stopped after 6.
- If the line-up fails, the records are still valid as an independent replicate, but the read-back must say so.

## Resources (one task per p, single thread, `--cpus-per-task=1` = 2 billed CPUs)
| task | p | islands | B3 timings | time limit (1.5×) | `--mem` (2 × B3 MaxRSS) | worst case (2 CPUs × limit) | expected |
|---|---|---|---|---|---|---|---|
| 1 | 5,000 | 16 | calibration 1.9 h + 16 × 0.17 h = 4.6 h | 07:00:00 | 2.4 → 5G | **14.0 core-h** | ≈ 9.4 core-h (4.7 h) |
| 2 | 10,000 | 8 | calibration 5.9 h + 8 × 0.7 h = 11.5 h | 17:30:00 | 4.8 → 5G | **35.0 core-h** | ≈ 23.4 core-h (11.7 h) |
| | | | | | | **49.0** | **≈ 33** |

- **Time limits.** An array has one `--time` (17:30:00). `submit_g0.sh` lowers task 1 to 07:00:00 right after
  `sbatch`. Task 1 also runs under `timeout 6h57m`.
- **Runtime guard.** The guard (`--hours` 6.70 / 17.20) stops a run cleanly before the limit. A stopped island is
  marked `partial`, the finished islands are kept, and the record is saved.
- **Memory.** It is not billed. The B3 MaxRSS at 5k (1.22 GB) includes an N = 10,000 run, so 5G is generous for both.

## Owls dry run (p = 1,000, 4 islands, nice 19; local gcc 11.5 / R 4.6.0; core compiled from a copy in /home/fb31/p1m_g0_dryrun)
**Outcome: WORKS.** Run 11-15 20:25–21:04 CT, one core, nice 19, on the shared Owls (load average 25–420). Log
and record: `/home/fb31/p1m_g0_dryrun/stage/stage_p1000.{log,rds}` (1.2 MB).
- **Core check:** 19 of 19 files match `revD_SHA256SUMS`.
- **Calibration:** status ok; T_pilot 27, 7 rebuilds, T_grid 31; 1,349 s.
- **Final run:** completed, 4 of 4 islands, 236 s per island. HPM = truth; sd(log Ẑ_r) 0.21.
- **Store:** 40,001 of 40,001 entries (full); log Σ e^F = −68.33.
- **Totals:** wall 38.5 min; peak RSS 0.46 GB.
- **Records present:**
  - per island: the 31-stage table with all 19 columns, including `gibbs_state_changes`; the 12-round terminal table;
    the complete core record;
  - `stage_dispersion` (Σ_t var(log increment) = 0.0035 against var(log Ẑ_r) = 0.044);
  - the pilot table (27 rows) and 28 diagnostic-island stage tables (7 iterations × 4);
  - the store F values and models.
- **Read-back:** `stage_readback.R` wrote all five tables (124 / 31 / 4 / 1 / 868 rows).
- **Observation at p = 1k only** (not a G0 result): accepted Gibbs moves per particle and round were 2.3–5.4 by
  stage.
- p = 2,000 was not run: the p = 1,000 run alone took 38 min, more than the 10-minute condition.
- Not exercised: the B3 line-up (no B3 records on Owls) and a guard stop.
- Known cosmetic bug: the pilot `ess_share` divides by N₀ instead of H₀ = 512 (see `../README.md` §8).
