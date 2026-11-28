# WP3 L5 (per-pass overhead) on SPR at p = 10⁶ (MEASURED, job 2749328, commit be24e9d, 2026-11-16 05:04–05:17 CST)

Node bb5u23c1, exclusive (192 CPUs). Two near-stationary 10⁶ islands at once, one per socket (96 threads, bound close +
membind), both the H-9 production configuration: G = 256, products block 4, k_store 8, mem budget 60 GB. Island 1 on
socket 0, island 2 on socket 1. Same data/schedule as job 2748756. Billed **42.7 core-h** (13.3 min; quote 42; worst 96).
Logs: `l5_2749328/`.

**Bit identity on SPR: PASS.** Island 1's output hash is `7ef6cfdb5cb8e748`, equal to job 2748756 (pre-L5 code, same stream).
Island 2 (independent) hashes differently (`50192aea327c6ae8`), as required.

## Late rounds, before (2748756, G = 256) → after (this job), ns·CPU per pair (= wall × 96 / pairs)
| round | before | after, island 1 | after, island 2 | wall before → after (island 1) |
|---|---|---|---|---|
| 4 (measured) | 289 | **254** | **254** | 31.3 → 27.4 s |
| 5 (measured) | 287 | **240** | **240** | 29.1 → 24.3 s |
| mean of rounds 4–5 | 288 | **247** (both islands) | | |

**= 1.23× the plan (200)**, down from 1.44× (−14%). WP3 projected ≈ 215 (ESTIMATE); measured 247.

## Where the time went (whole island, wall s, island 1; before → after)
walk 38.1 → 5.9 · build 26.2 → 9.7 · orders 14.7 → 8.6 · apply 8.9 → 0.3 (the L5 levers all landed) · phase A 503 → 523 ·
**phase B 38.5 → 57.1 and compaction 65 → 88 s** (worse). Late rounds: phase B + compaction 2.7 → 4.4 s per round.
**m3 confirmed:** the new phase-B wave cap / staging changes cost ≈ 1.7 s per late round and more in rounds 1–2 (round 2:
77 → 85 s). Recovering it would bring the late round to ≈ 22.6 s ≈ 223 ns·CPU/pair (ESTIMATE).

## Memory
Peak RSS 34.8 / 34.4 GB (islands 1 / 2); job MaxRSS 70.4 GB for both. The admission plan printed 45.1 GB (k = 62 from π₀ q90),
≥ the peak (1.3× margin). Stand-in partition: real setup tables add to both (D-27).

## Re-size (H-9 basis 1.44 → measured 1.23; ratio 0.857 on all 10⁶ costs)
| | H-9 / manifest v0.3 | at 1.23 |
|---|---|---|
| 1M block (5 fits) | 8,139 | 6,975 |
| option D | 4,752 | 4,072 |
| A + D with contingency | 28,398 | **≈ 26,090** |
| + buy back AR-weak at 1M (963 × 1.234 × 1.25 = 1,485) | | **≈ 27,580** (≤ the H-9 envelope ≈ 28.3k) |
The M risk (3.9–4.1 pairs per step vs 3) is still unpriced until T5.
