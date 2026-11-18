# WP3 fixed-rounds island on NOTS SPR at p = 10⁵ and 10⁶ (MEASURED, jobs 2748104 / 2748105, commit cd1a7e02, 2026-11-15/16)

Class A, label-major, N = 2,500, tile 128, AR(0.6), n = 200, stand-in partition (blocks of 4), B = 14. 96 CPUs per job,
OMP spread over threads. Raw logs: `wp3_rounds_2748104_p1e5.log`, `wp3_rounds_2748105_p1e6.log`.
Billed: 2748104 10.3 core-h (6.5 min); 2748105 67.1 core-h (42 min). **Sweep total 77.4 core-h** (HQ's ≈ 40 + the
standing exploratory authority; worst case was 112).
"Step" = one (particle, label) per round, as in the bench. "Pair" = one (support, label) score. The plan's per-step cost is
c = M·c_s + c_f = 3·90 + 30 = 300 ns thread-time = **600 ns·CPU billed per step, i.e. ≈ 200 ns·CPU per pair** (M = pairs per
step = 3). With 96 threads on 96 CPUs, thread-time = billed ns·CPU; with 48 threads on 96 CPUs, billed = 2 × thread-time.

## Whole runs (include the first rounds' serial store work and the transient from π₀)
| p | island | threads | wall s | billed ns·CPU / step (96 CPUs) | M (pairs/step) | billed ns·CPU / pair | phase A ns/pair (thread) | products ns/pair (thread) | peak RSS | hash equal |
|---|---|---|---|---|---|---|---|---|---|---|
| 10⁵ | transient (3 stages + 1 round) | 24 / 48 / 96 | 66.5 / 55.3 / 51.5 | 6,384 / 5,311 / 4,940 | 5.63 | — / 943 / 877 | — | — | 3.1 / 4.3 / 6.4 GB | yes |
| 10⁵ | near-stationary (φ=1, 3 burn-in + 1) | 24 / 48 / 96 | 71.0 / 52.7 / 46.2 | 5,452 / 4,049 / 3,546 | 7.04 | — / 575 / 504 | 78 / 89 / 120 | 18.5 / 22.0 / 44.1 | 3.3 / 4.3 / 5.7 GB | yes |
| **10⁶** | transient (3 stages + 1 round), G = 64 | **48 / 96** | **1,314 / 1,142** | 12,614 / 10,962 | 17.59 | 717 / **623** | 174 / 283 | 49.5 / 98.8 | 29.2 / 30.9 GB (sacct MaxRSS 32.6 GB) | yes |

## Late rounds (read from the per-round [island] lines; ESTIMATE of per-pair cost, using pass counts as the pair share)
| p | round | threads | wall of the round | billed ns·CPU / step | est. pairs/step in the round | **est. billed ns·CPU / pair** | vs plan (200) |
|---|---|---|---|---|---|---|---|
| 10⁵ | near-stationary rounds 4–5 | 96 | 2.75 s | 1,056 | ≈ 5.3 | **≈ 200** | ≈ 1.0× |
| 10⁵ | same | 48 | 3.45 s | 1,325 | ≈ 5.3 | ≈ 250 | 1.25× |
| 10⁶ | measured round at φ = 1 (step 4) | 96 | 69.8 s | 2,680 | ≈ 8 | **≈ 330** | **≈ 1.65×** |
| 10⁶ | same | 48 | 81.6 s | 3,133 | ≈ 8 | ≈ 390 | 1.95× |

## Findings
1. **T3 on SPR holds at 10⁵ and 10⁶**: identical output hash at every thread count.
2. **Thread scaling at 10⁶ is weak**: 48 → 96 threads (hyperthreads on the same 48 cores) gives 1.15× wall. On a 96-CPU
   allocation, 96 threads is still the cheaper per billed CPU.
3. **The cost per pair grows with p**: products 18 → 44 → 99 ns per pair (10⁴ → 10⁵ → 10⁶, 96 threads). Each pass carries
   fewer distinct supports at 10⁶ (41.9 with G = 64, vs 106 at 10⁵ with G = 256), so each X column load is reused less, and
   X (1.6 GB) sits on one socket's memory while the threads span both. **Memory-bandwidth / NUMA bound** (diagnosis,
   not yet measured directly).
4. **Early rounds are expensive**: at 10⁶ the first two rounds take 430–580 s each; the serial store compaction is a large
   part (phase B 310–330 s by round 2). Parallel compaction is in PR #24 (not in this commit).
5. **M** (pairs per step) is 5.6–7.0 at 10⁵ and 17.6 at 10⁶ on these crude 1- and 3-stage grids. It is not a budget number.
   The calibrated schedule (T5) sets M. The plan assumes 3; 10⁴ measured 3.63 on an adaptive grid.
6. **Memory**: 31 GB peak per 10⁶ island (G = 64, 96 threads), including the M2 snapshot leak found in the PR #21 review.
   This is the top of the planned 24–32 GB island task.

## Consequence for H-1 (budget)
At 10⁶ the late-round cost per pair is ≈ 1.65× the plan (96 threads; ESTIMATE). Pro-rated over the 1M block of the
manifest (8,415 core-h), that is ≈ +5.5k, so A + D with contingency moves from 26.9k to ≈ 33.7k (+37% vs the 24.6k
envelope). **This exceeds 15% and is reported to HQ with levers** (OD below). No 10⁶ stage is released before it is resolved.
Levers, cheapest first (to measure in one ≤ 80 core-h batch after the PR #21 fixes and PR #24 land):
- (L1) socket-local islands: two 48-CPU islands per node, each bound to one socket with X first-touched locally. Cost 0.
- (L2) G = 256 at 10⁶ (more supports per pass, so more X reuse). Memory +≈ 1 GB.
- (L3) parallel compaction (PR #24): removes most of the early-round serial phase B.
- (L4) quantity cuts, in order: the N = 10⁴ self-check (3,600 planned) → N = 5,000 or dropped; AR-weak at 1M; one AR-strong rep.
