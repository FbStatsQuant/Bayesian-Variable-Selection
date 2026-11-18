# WP3 10⁶ lever batch on one exclusive SPR node (MEASURED, job 2748756, commit efc0dfd0, 2026-11-16 01:27–01:42 CST)

Node bb4u14c1 (2 × Xeon 8468; NUMA node 0 = CPUs 0–47,96–143; node 1 = 48–95,144–191). Two near-stationary 10⁶ islands
**at the same time**, one per socket, each 96 threads bound close + `numactl --membind` to its own node:
socket 0 G = 64, socket 1 G = 256; both products block 4, parallel compaction. N = 2,500, class A, label-major, AR(0.6),
n = 200, stand-in partition (blocks of 4), B = 14; φ = 1 after one stage, 2 burn-in + 2 measured rounds.
Build is pre-#24-fix (run manifest: leader path unused, memory only recorded). Logs: `levers_2748756/`.
Billed **48.3 core-h** (15.1 min × 192 CPUs; approved ≤ 112, realistic quote 64).

**G invariance: PASS.** Both islands ran island 1 on the same stream; output hash `7ef6cfdb5cb8e748` at G = 64 and G = 256.

## Per round (per-round counters; ns per pair = wall × 96 threads / pairs = billed ns·CPU, 96 CPUs per island)
| round | M (pairs/step) | G = 64: wall s | **ns·CPU/pair** | products ns/pair (thread) | G = 256: wall s | **ns·CPU/pair** | products ns/pair (thread) |
|---|---|---|---|---|---|---|---|
| 1 (π₀ → φ = 1 in one stage) | 55 | 591.0 | 412 | 96.5 | 539.8 | 379 | 71.8 |
| 2 (burn-in) | 9.9 | 96.9 | 376 | 120.1 | 77.2 | 300 | 92.4 |
| 3 (burn-in) | 5.1 | 50.3 | 380 | 82.3 | 38.8 | 293 | 54.0 |
| 4 (measured) | 4.15 | 40.8 | **378** | 75.5 | 31.3 | **289** | 46.2 |
| 5 (measured) | 3.89 | 38.4 | **379** | 74.9 | 29.1 | **287** | 44.4 |

Late rounds (4–5) per step: G = 64 ≈ 1,470–1,570 ns·CPU; **G = 256 ≈ 1,116–1,200 ns·CPU** (plan: 600 at M = 3).
Late-round time split at G = 256 (round 5, 29.1 s): phase A ≈ 11.1 s (products ≈ 4.5 s), phase B 1.9 s, compaction 0.7 s,
**the rest ≈ 15 s = per-pass overheads (walk, build, orders, apply)**. Whole run: walk 38 s, build 26 s, orders 15 s.

## Findings
1. **Best configuration: G = 256, socket-local:** **≈ 288 ns·CPU per pair = 1.44× the plan (200)**. G = 64 is 1.89×. G = 256 cuts
   passes 3.5× (131 vs 457 per late round) and with them the per-pass overheads; the products also fall (44 vs 75 ns/pair).
2. **Products are no longer the bottleneck** (44 ns/pair at G = 256 vs 99 in 2748105). The remaining excess is the per-pass
   overhead (≈ half of a late round). Next engineering lever (L5): cut walk / build / orders per pass.
3. **M in the late rounds at φ = 1 is 3.9–4.1** (plan 3; 10⁴ calibrated 3.63). The calibrated schedule (T5) fixes it; a residual
   risk of ×1.2–1.35 on per-step cost, not included in the re-size below.
4. **Memory: peak RSS 25.4 GB (G = 64) and 34.3 GB (G = 256)** per island, with the M2 fix in. The pre-fix plan printed 54.5 /
   61.0 GB (it assumed k = 114). WP3's post-fix plan quotes ≈ 17.5 GiB at 10⁶, below the measured 23.7 GiB at G = 64, so
   **the post-fix plan is not an upper bound at 10⁶** → back to WP3 (P2). Island task request at G = 256: **40 GB** (plan 24–32).
5. Parallel compaction works: 0 serial fallbacks; compaction 0.7–1.5 s in late rounds, 21–48 s in round 1.

## Re-size (H-1), at the best measured configuration (G = 256, socket-local; per-pair ratio 1.44)
| | planned (v0.2 manifest) | re-sized |
|---|---|---|
| 1M block (6 fits) | 8,415 | 12,118 |
| planned excl. option D | 18,199 | 21,902 |
| with 25% contingency | 22,749 | 27,378 |
| option D (with contingency) | 4,125 | 5,940 |
| **A + D with contingency** | **26,874 (+9.2%)** | **33,318 (+35%)** |
| L4 step 1: drop the N = 10⁴ self-check (3,600 × 1.44 × 1.25 = 6,480) | | **26,838 (+9.1%)** |
| L4 alt: self-check at N = 5,000 (saves 3,240) | | 30,078 (+22%) |
| + drop AR-weak at 1M (saves 1,733) | | 28,345 (+15.2%) |
