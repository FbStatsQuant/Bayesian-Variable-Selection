# PROD-L sizing from the LOWP pilot 20261030T0712Z (OPS-4, 2026-10-30; revised after Sol review)

Source: accepted pilot (`code/lowp/pilot/summary_20261030T0712Z_lowp_pilot/PILOT_SUMMARY.md`: OVERALL PASS, 259/259 units, 16/16 verdicts; clean-up evidence in `ops/evidence/ops4_pilot_20261030T0712Z_cleanup.txt`) and the terminal Slurm snapshot (`NOTS Data\New_Campaign\logs\20261030T0712Z_lowp_pilot\accounting\sacct_final.tsv`). Sapphire Rapids (Xeon 8468), R 4.5.2 / GCC 14.3.0, single-threaded BLAS. Production counts and layout from `code/lowp/RUN_DESIGN.md` §1 and §3. **The benchmark arm is sized separately: it is gated on BENCH-AUDIT (D36/D42), and F3 may change.** Review: `ops/review/SOL_REVIEW_PILOT_20261030T0712Z.md` (sizing ACCEPT WITH FIXES; this revision applies findings 2–8).

**Scope of every figure:** charged CPU-hours = AllocCPUS × elapsed, for the fitting pieces only. Production build/gate/lock/collector jobs (≈ 0.1 CPU-h each in the pilot), retries and local scoring are excluded.

**Do not copy the summarizer's generic `accepted` projection** (`pilot_projection.csv`) as production requests. It costs SMC and benchmark tasks at 1 CPU (the charge is 2), uses the stall-inflated p = 20 SMC mean, and suggests 512 MiB / 30 min for SMC, which is incompatible with the 2 GiB / 4 h core allocation. This document supersedes it for resource sizing.

## 0. Two observations that change the costing
1. **Every 1-CPU task received AllocCPUS = 2.** Tasks requesting 4/16/32 CPUs received 4/16/32. This fits the node topology (192 logical CPUs, 2 threads per core: Slurm allocates a whole core). It is observed allocation, not an audit of Rice's billing/TRES weights. Single-thread costs below are wall × 2.
2. **One SMC task had a large non-compute delay.** Task 2469176_8 on bb3u18c1: 526 s elapsed; 319.5 s outside the timed R process; the process itself 206.5 s wall for 12.2 s CPU (user 4.8, sys 7.4), and the fit reported 3.3 s runtime with no escalation. This is consistent with filesystem/start-up I/O wait, not compute. Its incidence (per task, per R process, or bursts) cannot be identified from 28 one-fit tasks, so the stall terms below are **scenarios, not measured rates**.

## 1. Pilot cost: measured against the estimate
**Measured 2.796 charged CPU-hours** (10,066 allocated CPU-seconds over the 67 parent jobs/tasks; Sol reproduced it). JOB.md estimated **about 10 (range 7–14)**. JOB.md's **311 CPU-h requested ceiling** (requested CPUs × wall limits) corresponds to **472.7 allocated CPU-h** under the observed doubling of 1-CPU tasks. The measurement is below the range, largely because the NOTS timings were faster than the laptop-based estimates (enumeration p = 30: 25.4 s in-process vs 85–100 s assumed; scaling job 97 s vs about 8 min; SMC p = 30: 2.9 s in-process vs 18–24 s). Platform, concurrency and cache conditions also differ, so not all of the gap is processor speed.

| Step | Tasks | CPUs (alloc) | Charged CPU-h | Max task elapsed | Peak RSS (batch step, MiB) |
|---|---|---|---|---|---|
| s0_build | 1 | 2 | 0.015 | 27 s | 575 |
| s0_verify (P0a) | 1 | 2 | 0.005 | 9 s | 102 |
| s0_truthlock | 1 | 2 | 0.033 | 59 s | 81 |
| s0_lock | 1 | 2 | 0.003 | 5 s | 74 |
| s1_enum20 | 1 | 4 | 0.074 | 67 s | 78 |
| s1_enum30 | 6 | 16 | 0.853 | 33 s | 87 |
| s1_scale | 1 | 32 | 0.862 | 97 s | 91 |
| s1_bitid | 1 | 16 | 0.036 | 8 s | 261 |
| s2_smc | 28 | 2 | 0.464 | 526 s (delay; others ≤ 17 s) | 189 |
| s3_bench | 24 | 2 | 0.448 | 35 s | 256 |
| s8_unlock / s9_collect | 2 | 2 | 0.003 | 4 s | 66 |
| **Total** | **67** | | **2.796** | | |

## 2. Per-unit measurements used (valid units; process wall from GNU time, including R start-up)
| Unit | Mean wall | 90th pct / max wall | Peak RSS | Output per unit |
|---|---|---|---|---|
| Enumeration p = 20 (4 threads, both scales) | 1.95 s | 2.44 / 6.8 s | 83 MiB | 95 KiB |
| Enumeration p = 30 (16 threads) | 27.4 s (in-process 25.4 s: overhead ≈ 2 s) | 28.6 / 28.7 s | 84 MiB | 99 KiB |
| SMC fit p = 20 / p = 30 (1 CPU; delayed unit excluded) | 6.8 s / 7.7 s | — / 8.3 s, 13.5 s | 174 / 196 MiB | 178 / 588 KiB |
| SMC repeat fit p = 20 / p = 30 (2 fits each) | 5.4 s / 7.3 s | 7.1 / 10.2 s | 172 / 193 MiB | 167 / 711 KiB |
| Benchmark case, all 8 methods (1 CPU) p = 20 / p = 30 | 28.7 s / 28.4 s | 29.7 / 30.8 s (90th) | 256 MiB (A1) | ≈ 645 KiB per case |
| Per method (p pooled): F1 5.3, F2 3.2, F3 2.2, F4 1.0, F5 2.8, A1 3.8, A2 1.0, **A3 9.3** s | | | F1–F3, F5, A1 ≈ 220–256 MiB; A3 ≈ 182; F4, A2 ≈ 80–90 | |

Enumerator thread scaling (one dataset, dev_p0030_S4_r001; process/in-process wall): **8 threads 35.05 / 32.48 s; 16 threads 19.65 / 17.69 s; 32 threads 15.31 / 14.09 s**; outputs identical at 8/16/16/32 threads. The same dataset took 28.69 / 27.07 s in its enum30 task at 16 threads, a sizeable between-job variation.

## 3. PROD-L sizing (charged CPU-h; formulas below the table)
| Piece | Units | Layout | Per task (expected) | CPUs charged | CPU-h expected | CPU-h conservative | Delay sensitivity | Memory request | Time request |
|---|---|---|---|---|---|---|---|---|---|
| enum20 | 600 datasets | 1 task, `--threads 4` | ≈ 20 min | 4 | **1.30** | 1.62 | — | **1 GiB** (peak 83 MiB) | 1 h |
| enum30, 16 threads (**supported design**) | 600 | 24 tasks × 25, `--threads 16` | 11.4 min | 16 | **73.1** | 76.3 | — | **1 GiB** (peak 87 MiB) | 45 min |
| *enum30, 8 threads (provisional scenario)* | 600 | 24 × 25, `--threads 8` | ≈ 15–18 min | 8 | *46.7 (single-dataset baseline 35.05 s)* | *56.7 (35.05 s + 7.45 s allowance = 42.5 s)* | — | 1 GiB | 1 h |
| SMC primary | 2,400 fits | 96 tasks × 25 fits, 1 CPU | ≈ 3.1 min | 2 | **10.9** (scenario: one 500 s delay per 28 tasks) | 15.9 (11 s/fit) | **21.6** (observed per-fit tail + task-level delay) | **2 GiB** (= core guard `--mem-gb 2`; peak 196 MiB) | 4 h + deadline rule (§4) |
| SMC repeats (5 extra seeds × r 1..20 × 24 cells) | 2,400 fits | 120 tasks × 20 fits, 1 CPU | ≈ 2.2 min | 2 | **10.0** | 16.2 (11 s/fit) | **19.1** (one excess delay per 28 fits) | 2 GiB | 4 h + deadline rule (§4) |
| **Subtotal without benchmarks** | | | | | **95.3** (enum30 16 thr) | **110.0** | ≈ 115 (with both delay-sensitivity cases) | | |
| **Benchmarks (separate; gated by BENCH-AUDIT D36/D42)** | 2,400 cases × 8 = 19,200 fits | 96 tasks × 25 cases, 1 CPU | ≈ 12 min | 2 | **38.3** (A3 12.4, F1 7.1, A1 5.0, F2 4.2, F5 3.8, F3 3.0, F4 1.4, A2 1.3) | 40.6 (90th-pct case wall 30.25 s) | — | **1 GiB** (peak 256 MiB; the pilot asked for 6 GiB, RUN_DESIGN 4 GiB) | 1 h |
| **Total with benchmarks** | | | | | **133.6** | **150.6** | ≈ 153 | | |

Formulas (all × charged CPUs, / 3,600; per-task overhead 5 s from the SMC/bench tasks; delay scenario 500 s per 28 tasks):
- enum20: 600 × 1.95 s × 4 (expected); 600 × 2.44 s × 4 (conservative, 90th pct).
- enum30 16 threads: 600 × 27.4 s × 16; conservative 600 × 28.6 s × 16 (90th pct).
- enum30 8 threads: 600 × 35.05 s × 8 = 46.7 is a single-dataset baseline. 600 × 42.5 s × 8 = 56.7 adds a 7.45 s allowance for between-job variation (the S4 dataset was 9.04 s slower in its own enum30 task than in the scaling job at 16 threads). The matched comparison on the scaling dataset is 46.7 vs 52.4 CPU-h at 8 vs 16 threads, a saving of about 11 %. The larger gap to 73.1 compares different conditions. **The 8-thread option is not established; keep 16 threads unless HQ accepts it as provisional.**
- SMC primary: (2,400 × 7.24 s + 96 × 5 s + 96/28 × 500 s) × 2 = 10.9; conservative 11 s/fit in place of 7.24 s = 15.9; sensitivity (Sol) keeps the observed per-fit wall tail and the task-level outside-process delay = 21.6.
- SMC repeats: (2,400 × 6.35 s + 120 × 5 s + 120/28 × 500 s) × 2 = 10.0; conservative 11 s/fit = 16.2; sensitivity (one excess delay per 28 fits) = 19.1. Repeat timing rests on 2 fits per p.
- Benchmarks: (2,400 × 28.54 s + 96 × 5 s) × 2 = 38.3; conservative with the 90th-percentile case wall 30.25 s = 40.6.
- Repeat design: RUN_DESIGN's proposal (20 replicates × 5 extra seeds per (p, S, c); primary seeds not counted again). HQ decision 1 there (all 100 replicates) would make it 12,000 fits ≈ 50 CPU-h expected.

## 4. Recommended PROD-L layout, throttle and deadlines
**Order:** enum20 + enum30 ∥ smc → smcrep, now; **benchmarks only after BENCH-AUDIT clears**, re-sized for the revised F3. **Benchmarks are serialized after the SMC/repeat lane** (not concurrent with it).

**Shared truth lock.** If several pieces run in one wave, complete every guard check and stage once, before a single shared truth lock. The unlock depends (`afterany`) on every consumer of the locked tree, not on one piece. No `du`/guard on campaign home during a locked wave.

**Combined CPU ceiling (charged CPUs):** PROD-L alone ≤ 132; while PROD-H runs, PROD-L ≤ 68 and the combined PROD-H + PROD-L stays within a ceiling HQ agrees (OPS proposes ≤ 192 charged CPUs, one Sapphire Rapids node's worth). Throttles are lowered at submission to respect it; a per-array `%N` alone does not enforce a campaign cap.

| Piece | Array | Throttle (alone / with PROD-H) | Concurrent charged CPUs | Waves × per-task wall | Wall (excl. queue), alone |
|---|---|---|---|---|---|
| enum20 | 1 | — | 4 | 1 × 20 min | 20 min |
| enum30 (16 threads) | 0-23 | `%4` / `%2` | 64 / 32 | 6 × 11.4 min | ≈ 70 min |
| smc | 0-95 | `%32` / `%16` | 64 / 32 | 3 × 3.1 min | ≈ 10 min |
| smcrep (after smc) | 0-119 | `%32` / `%16` | 64 / 32 | 4 × 2.2 min | ≈ 10 min |
| bench (cleared; after smcrep) | 0-95 | `%32` / `%16` | 64 / 32 | 3 × 12 min | ≈ 36 min |

Peak alone: enum20 + enum30 + smc = 132 charged CPUs; with PROD-H: 68. Every piece uses `--constraint=sapphirerapids` and account/partition commons, with single-threaded BLAS except in the enumerator.

**Batch deadline rule (SMC primary and repeats).** The core's `--hours 4` is a per-fit guard, but a task runs 20–25 fits under one Slurm limit. The production runner must not start a fit without adequate remaining scheduler time (at least the per-fit guard plus margin), must commit each finished unit, and must write a completion inventory. Remaining or killed units are resubmitted explicitly in a fresh task, never counted as successes. Alternatively the batch gets a separately justified larger limit. Four hours is ample for ordinary batches (≈ 3 min measured) but does not bound an escalation tail, which the pilot did not sample (0 escalations in 28 fits). This is a bundle requirement for the PROD-L job (LOWP/CONF), not an OPS setting.

## 5. Disk
- **Home** (guard planned add, one shared stage for all pieces): staged code ≈ 15 MiB + sealed study (1,200 inputs + truth + manifests) 72 MiB + compile caches 2–5 MiB ≈ **100 MiB** → 9.42 + 0.10 ≈ 9.52 GiB, under 9.6 GiB with ≈ 80–90 MiB to spare. This holds only if inputs/code are not copied afresh per piece and the live guard is rerun at submission (Codex state grew ≈ 0.9 GiB in a day on 2026-10-29). If the guard refuses, OPS applies the D31 archive-verify-review-erase route.
- **Scratch** (transient, pulled and deleted per run folder), from measured output means: enumeration 0.111 GiB; SMC primary 0.876 GiB; SMC repeats **1.005 GiB** (repeat records at p = 30 are 711 KiB vs 588 KiB primary); benchmarks 1.492 GiB; total **3.49 GiB (3.74 decimal GB)** before logs (≈ 10 MiB), caches (≈ 1 MiB per piece) and escalation growth. **Plan for 4 GiB plus a reserve**, and pull each folder as soon as its piece completes.

## 6. Caveats
- Coverage: p = 30 enumeration and all SMC/benchmark timings come from replicate 1 of each scenario (12 datasets × 2 scales); SMC repeats from 2 fits per p. The 28 SMC fits had **0 escalations**, and P5 found 0 `resource_limit`; escalation tails are unsampled.
- The delay term rests on a single event; production should log per-fit and per-task wall and CPU, and the budget should be revised from the first production piece's evidence.
- The benchmark figures are for the current bench_lowp code; BENCH-AUDIT's F3 change will alter F3's ≈ 3 CPU-h. Validate F3's cost and memory after the fix.
