# LOWP pilot summary: OVERALL PASS

Generated 2026-10-30 07:53 UTC by `pilot/summarize_pilot.R`. All required evidence is present and valid.

Dev datasets only (excluded from all counts); every arm ran on the real dev ids through the production CLIs with `--development`.

## Verdicts

| item | verdict | detail |
|---|---|---|
| Launch receipt (final pilot.env, hashes, guard receipt, sbatch vectors, effective environment) | PASS | pilot.env hash, 12 sbatch vectors, guard receipt with the D7 limits, no test hook |
| P0 regeneration on NOTS (lowp_verify_nots.R: exit 0 PASS / 1 MISMATCH / 3 INCOMPLETE) | PASS | PASS (exit status 0). Regenerated 1200 production and 60 dev datasets; 1200 + 60 truth files and 6 of 6 pilot copies compared; 0 failed checks. |
| P0 truth-lock test (ordinary user, production + dev truth; evidence final_status.txt) | PASS | FINAL_EXIT_STATUS 0, 37 checks, 0 failed; trees after the test 755/444 |
| Wave lock: both truth trees mode 000 and verified before any fit | PASS | LOCK_STATE truth_mode=0 devtruth_mode=0 ls_denied=2 files_visible=0 | WAVE_LOCK_VERIFIED LOCK_STATE truth_mode=0 devtruth_mode=0 ls_denied=2 files_visible=0 |
| Wave unlock: trees restored to 755/444 after the last fitting job, hashes unchanged | PASS | OPEN_STATE n_truth=1200 n_devtruth=60 dirs_not_755=0 files_not_444=0 | SHA256_AGAINST_PRELOCK equal | WAVE_UNLOCK_VERIFIED OPEN_STATE n_truth=1200 n_devtruth=60 dirs_not_755=0 files_not_444=0 sha=equal |
| Enumerator vs scorer: bytes for scores, tolerance for aggregates, exact decisions, thread invariance | PASS | 26 rows, 26 pass; checks present: T1,T2,T3,T4,T5; byte mismatches in T2/T3: 0 |
| Exact unit sets valid (30 enum20, 6 enum30, 3 scaling, 24 SMC, 4 repeats, 192 benchmark units) | PASS | enum20 30/30; enum30 6/6; scaling 3/3; smc_primary 24/24; smc_repeat 4/4; benchmarks 192/192 |
| Step commands executed with exit status 0 (build, verify, truth test, wave lock/unlock, bit identity, scaling subsets) | PASS | 10 of 10 timing rows with rc 0 |
| Thread invariance: dev_p0030_S4_r001 outputs identical at 8, 16, 16, 32 threads | PASS | identical, identical, identical, identical |
| SMC repeat fits: valid, seed = primary + 1,000, Monte Carlo spread vs the primary fit | PASS | 4 pairs; |dlogZ| median 0.013 max 0.030; same HPM 4 of 4 |
| Fit statuses: no failed, timeout or unknown rule row (a captured R warning is accepted and counted) | PASS | 0 valid units carry status 'warning' |
| Slurm: every job and array task COMPLETED with exit 0:0 (terminal snapshot) | PASS | all 12 steps and 67 jobs/array tasks |
| Memory evidence for every arm and p used in sizing (GNU time, else sacct job-level bound, else core VmHWM) | PASS | sources: gnu_time |
| Wall-time evidence for every arm and p used in sizing (unit timing rows; no fallback to in-process time) | PASS | all arms and p have process wall times |
| Thread-scaling subset measurements: expected problem, full coverage, declared split, one common subset (every row checked) | PASS | 4 rows: dev_p0030_S4_r001, 2^30 models, 31 of 1,024 tasks, one common subset (64-hex digest) |
| P5 scan of the SMC results (DECISIONS D11; informative, no gate) | PASS | 28 SMC units scanned: primary_resource_limit = 0, eligible = 0. |

## Unit sets

| set | valid | present | expected |
|---|---|---|---|
| enum20 | 30 | 30 | 30 |
| enum30 | 6 | 6 | 6 |
| scaling | 3 | 3 | 3 |
| smc_primary | 24 | 24 | 24 |
| smc_repeat | 4 | 4 | 4 |
| benchmarks | 192 | 192 | 192 |

## Cost per unit, by arm and p (valid units only)

Policy: every required unit needs a finite positive process wall time (missing: INCOMPLETE, zero or negative: invalid); enumeration units also need observed CPU time user+sys (absence: INCOMPLETE), single-thread units are costed as wall x 1 CPU. In-process = `runtime_s` of the runner; wall = whole process (start-up, cache load, fit) from GNU time; peak RSS from GNU time, else the batch-step MaxRSS of the job (**a job-level conservative bound**, for jobs that run several units it covers all of them), else the core's VmHWM.

| Arm | p | Threads | Valid | Expected | In-process median s | 90th s | Max s | Wall median s (incl. start-up) | Wall max s | Peak RSS MB (max) | Memory source | Output KB / unit | Escalations | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Exact enumeration (both scales, one pass) | 20 | 4 | 30 | 30 | 0.293 | 0.327 | 0.351 | 1.63 | 6.83 | 82.7 | gnu_time | 94.5 | NA | 0 |
| Exact enumeration (both scales, one pass) | 30 | 16 | 6 | 6 | 25.4 | 26.9 | 27.1 | 27.6 | 28.7 | 83.9 | gnu_time | 99.4 | NA | 0 |
| SMC-BVS v2.2.1, primary seed | 20 | 1 | 12 | 12 | 3.07 | 4.91 | 5.68 | 7.17 | 207 | 174 | gnu_time | 178 | 0 | 0 |
| SMC-BVS v2.2.1, primary seed | 30 | 1 | 12 | 12 | 2.94 | 5.1 | 6.28 | 7.26 | 13.5 | 196 | gnu_time | 588 | 0 | 0 |
| SMC-BVS v2.2.1, repeat seed | 20 | 1 | 2 | 2 | 2.56 | 3.44 | 3.66 | 5.42 | 7.14 | 171 | gnu_time | 167 | 0 | 0 |
| SMC-BVS v2.2.1, repeat seed | 30 | 1 | 2 | 2 | 2.67 | 3.45 | 3.64 | 7.28 | 10.2 | 193 | gnu_time | 711 | 0 | 0 |
| F1 Lasso | 20 | 1 | 12 | 12 | 1.04 | 1.08 | 1.1 | 5.33 | 5.71 | 220 | gnu_time | 50.2 | NA | 0 |
| F1 Lasso | 30 | 1 | 12 | 12 | 1.17 | 1.3 | 1.47 | 5.42 | 5.62 | 225 | gnu_time | 50.7 | NA | 0 |
| F2 Elastic net | 20 | 1 | 12 | 12 | 1.41 | 1.64 | 1.7 | 2.99 | 3.21 | 249 | gnu_time | 198 | NA | 0 |
| F2 Elastic net | 30 | 1 | 12 | 12 | 1.92 | 2.45 | 2.52 | 3.46 | 3.95 | 247 | gnu_time | 198 | NA | 0 |
| F3 Adaptive lasso | 20 | 1 | 12 | 12 | 1.06 | 1.1 | 1.1 | 2.22 | 2.29 | 227 | gnu_time | 56.4 | NA | 0 |
| F3 Adaptive lasso | 30 | 1 | 12 | 12 | 1.1 | 1.27 | 1.43 | 2.21 | 2.49 | 231 | gnu_time | 57.2 | NA | 0 |
| F4 MCP | 20 | 1 | 12 | 12 | 0.0495 | 0.0529 | 0.053 | 0.975 | 1.08 | 88.3 | gnu_time | 33.8 | NA | 0 |
| F4 MCP | 30 | 1 | 12 | 12 | 0.0545 | 0.059 | 0.061 | 1.03 | 1.22 | 89 | gnu_time | 43.2 | NA | 0 |
| F5 ABESS | 20 | 1 | 12 | 12 | 0.813 | 0.815 | 0.819 | 2.96 | 3.38 | 217 | gnu_time | 28.2 | NA | 0 |
| F5 ABESS | 30 | 1 | 12 | 12 | 0.815 | 1.01 | 1.04 | 2.58 | 3.25 | 217 | gnu_time | 31.4 | NA | 0 |
| A1 SuSiE | 20 | 1 | 12 | 12 | 1.3 | 1.39 | 1.46 | 3.88 | 4.01 | 253 | gnu_time | 27.8 | NA | 0 |
| A1 SuSiE | 30 | 1 | 12 | 12 | 1.41 | 1.43 | 1.44 | 3.78 | 3.92 | 256 | gnu_time | 28 | NA | 0 |
| A2 SSL | 20 | 1 | 12 | 12 | 0.012 | 0.0139 | 0.015 | 1.04 | 1.07 | 77.9 | gnu_time | 11.4 | NA | 0 |
| A2 SSL | 30 | 1 | 12 | 12 | 0.013 | 0.0149 | 0.015 | 0.965 | 1.06 | 77.8 | gnu_time | 11.7 | NA | 0 |
| A3 Horseshoe | 20 | 1 | 12 | 12 | 7.72 | 7.74 | 7.76 | 9.3 | 9.39 | 182 | gnu_time | 239 | NA | 0 |
| A3 Horseshoe | 30 | 1 | 12 | 12 | 7.71 | 8.29 | 8.32 | 9.24 | 9.72 | 180 | gnu_time | 240 | NA | 0 |

## Thread scaling of the enumerator (dev_p0030_S4_r001)

Single-thread full-run time extrapolated from the 3% subset: 241 s.

| source | threads | wall_s | reps | speedup_vs_1 | efficiency |
|---|---|---|---|---|---|
| 3% task subset | 1 | 7.3 | 2 | 1 | 1 |
| 3% task subset | 8 | 1.06 | 2 | 6.89 | 0.861 |
| full enumeration | 8 | 32.5 | 1 | 7.42 | 0.928 |
| full (enum30 task) | 16 | 27.1 | 1 | 8.91 | 0.557 |
| full enumeration | 16 | 17.7 | 1 | 13.6 | 0.852 |
| full enumeration | 32 | 14.1 | 1 | 17.1 | 0.535 |

## Projected production cost (RUN_DESIGN section 3 layout): accepted

Per-task wall = units per task x mean unit wall (expected) or x 90th-percentile unit wall (conservative); time request = 1.5 x conservative + 15 min rounded to 15 min; memory request = 1.5 x the largest pilot peak RSS, rounded up to 512 MB; core-hours = allocated CPUs x expected wall; scratch = units x mean pilot output size. Failed or missing pilot units are excluded.

| piece | tasks | units_per_task | cpus_per_task | unit_wall_mean_s | unit_wall_p90_s | task_wall_expected | task_wall_conservative | suggested_time_request | suggested_mem_request_mb | core_hours | scratch_gb | pilot_escalations | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| enum30 | 24 | 25 | 16 | 27.4 | 28.6 | 00:11 | 00:11 | 00:45 | 512 | 73.1 | 0.0569 | 0 | accepted |
| enum20 | 1 | 600 | 4 | 1.95 | 2.44 | 00:19 | 00:24 | 01:00 | 512 | 1.3 | 0.0541 | 0 | accepted |
| smc p=20 | 48 | 25 | 1 | 23.4 | 9.09 | 00:09 | 00:03 | 00:30 | 512 | 7.81 | 0.203 | 0 | accepted |
| smc p=30 | 48 | 25 | 1 | 7.71 | 11.7 | 00:03 | 00:04 | 00:30 | 512 | 2.57 | 0.673 | 0 | accepted |
| smcrep p=20 | 60 | 20 | 1 | 23.4 | 9.09 | 00:07 | 00:03 | 00:30 | 512 | 7.81 | 0.203 | 0 | accepted |
| smcrep p=30 | 60 | 20 | 1 | 7.71 | 11.7 | 00:02 | 00:03 | 00:30 | 512 | 2.57 | 0.673 | 0 | accepted |
| bench p=20 | 48 | 25 | 1 | 28.7 | 29.7 | 00:11 | 00:12 | 00:45 | 512 | 9.56 | 0.737 | 0 | accepted |
| bench p=30 | 48 | 25 | 1 | 28.4 | 30.8 | 00:11 | 00:12 | 00:45 | 512 | 9.46 | 0.755 | 0 | accepted |
| TOTAL | 337 | NA | NA | NA | NA | NA | NA | NA | NA | 114 | 3.36 | NA | accepted |

## Sample coverage and its limits

| arm | datasets | what |
|---|---|---|
| Exact enumeration p = 20 | 30 | S1..S6 x r1..r5 at p = 20 (both scales in one pass) |
| Exact enumeration p = 30 | 6 | S1..S6, r1 only, at p = 30 |
| SMC-BVS primary | 12 | p in {20,30} x S1..S6, r1 only, c100 and c050 (24 fits) |
| SMC-BVS repeat | 4 | 4 of those cases, repeat 1 (seed + 1,000) |
| Benchmarks (8 methods) | 12 | the same 24 cases, one fit per method |
| Regeneration check (not timing) | 60 | all 60 dev manifest rows regenerated and hashed; gives no fit-time measurement |

Timing and memory come from these subsets only: p = 30 enumeration and all SMC/benchmark timings use replicate 1 of six scenarios; production extrapolation assumes that replicates within a cell cost alike and that rare SMC escalations are absent from 28 fits. Keep a margin. The 60-row regeneration check proves the generator, not fit cost.

### Slurm accounting

Snapshot: sacct_final.tsv (terminal, incl. the collector).

| JobName | State | rows |
|---|---|---|
| lowp_p0_build | COMPLETED | 1 |
| lowp_p0_lock | COMPLETED | 1 |
| lowp_p0_truthlock | COMPLETED | 1 |
| lowp_p0_verify | COMPLETED | 1 |
| lowp_p1_bitid | COMPLETED | 1 |
| lowp_p1_enum20 | COMPLETED | 1 |
| lowp_p1_enum30 | COMPLETED | 6 |
| lowp_p1_scale | COMPLETED | 1 |
| lowp_p2_smc | COMPLETED | 28 |
| lowp_p3_bench | COMPLETED | 24 |
| lowp_p8_unlock | COMPLETED | 1 |
| lowp_p9_collect | COMPLETED | 1 |

## Disk after the pilot

```
# disk footprint of the pilot at 2026-10-30T07:26:07Z, KB
15900	/scratch/fb31/New_Campaign/results/20261030T0712Z_lowp_pilot_bench
2869	/scratch/fb31/New_Campaign/results/20261030T0712Z_lowp_pilot_enum20
603	/scratch/fb31/New_Campaign/results/20261030T0712Z_lowp_pilot_enum30
100	/scratch/fb31/New_Campaign/results/20261030T0712Z_lowp_pilot_scale_t08
100	/scratch/fb31/New_Campaign/results/20261030T0712Z_lowp_pilot_scale_t16
100	/scratch/fb31/New_Campaign/results/20261030T0712Z_lowp_pilot_scale_t32
10983	/scratch/fb31/New_Campaign/results/20261030T0712Z_lowp_pilot_smc
1625	/scratch/fb31/New_Campaign/logs/20261030T0712Z_lowp_pilot
848	/scratch/fb31/New_Campaign/runs/20261030T0712Z_lowp_pilot_cache
0	/scratch/fb31/New_Campaign/runs/20261030T0712Z_lowp_pilot_tmp
1600	/home/fb31/projects/BVS/New_Campaign/runs/20261030T0712Z_lowp_pilot/code/core/v2_2_1/core/.cpp_cache
12972	/home/fb31/projects/BVS/New_Campaign/runs/20261030T0712Z_lowp_pilot
3200	/home/fb31/projects/BVS/New_Campaign/runs/20261030T0712Z_lowp_pilot/inputs/lowp_dev
6572	/home/fb31/projects/BVS/New_Campaign/runs/20261030T0712Z_lowp_pilot/study
```

## P5 scan of the SMC results (DECISIONS D11)

Informative: not an acceptance gate. Produced by `core/v2_2_1/tools/p5_scan.R` over the SMC result folder.

`p5_scan units=28 primary_resource_limit=0 eligible=0 retried=0 retry_outcomes=none incomplete=0 launchable=0 locked=0 invalid_inspect=0`

`primary_resource_limit` = **0**, `eligible` = **0** (SMC units scanned: 28). Full table: `pilot_p5_scan.tsv`.

No SMC unit ended `resource_limit`: nothing for HQ to decide under P5.

## SMC escalations

None among the valid pilot fits.

Files: `pilot_table.csv`, `pilot_units.csv`, `pilot_scaling.csv`, `pilot_projection.csv`, `pilot_verdicts.csv`, `pilot_repeat_vs_primary.csv`, `pilot_p5_scan.tsv`.
