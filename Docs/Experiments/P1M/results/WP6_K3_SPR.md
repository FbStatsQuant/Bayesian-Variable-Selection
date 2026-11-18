# WP6 K3 on SPR: late 10⁶ round 5, dense vs K1 vs K3 (job 2756524, 2026-11-16)

**Job:** NOTS 2756524, node bb6u19g1 (Xeon Platinum 8468), one socket (96 CPUs, 72G), COMPLETED in 13 min 14 s,
**21.2 core-h** (quote ≈ 50, worst 96). Code: PR #51 head 89366d4a (K3; K1 merged), built with `-DV4_ISLAND_ISA=sapphirerapids`.
Bench: `tools/nots_bench_k1.sh`, p = 10⁶, N = 2,500, G = 256, class A, label-major, tile 128, **stand-in data/start law**
(not the production setup), rounds 4–5 resumed from one checkpoint per variant, I1 check off in all variants.
**Same output hash in all six variants: `7ef6cfdb5cb8e748`** (logZ −703.308561, HPM |S| = 5). M = 3.89 pairs per particle-round.

| variant | round-5 wall (s) | ns·CPU per pair | products (thread-s) | phase A (s) | phase B (s) | flips per step | peak RSS (GB) |
|---|---|---|---|---|---|---|---|
| dense | 18.87 | 186.3 | 472.5 | 11.77 | 3.56 | 3.889 | 18.01 |
| dense2 | 19.29 | 190.4 | 483.1 | 11.83 | 3.91 | 3.889 | 18.02 |
| k1 | 14.98 | 147.9 | 439.8 | 8.24 | 3.17 | 1.377 | 18.07 |
| k1b | 15.65 | 154.5 | 496.8 | 8.93 | 3.18 | 1.377 | 18.01 |
| k3 | 14.31 | 141.3 | 314.3 | 7.53 | 3.19 | 1.377 | 20.71 |
| k3b | 13.99 | 138.1 | 309.3 | 7.33 | 3.07 | 1.377 | 20.71 |

Gram rows (K3): computed 7,108, reused 12,645 column×passes (64% reuse), no-slot 0.

**Reading (MEASURED, stand-in data):**
- K1 vs dense: round wall −20% (19.1 → 15.3 s mean), ns·CPU/pair 188 → 151; flips per step 3.89 → 1.38.
- K3 vs K1: round wall −7% (15.3 → 14.15 s), products −34% (468 → 312 thread-s), ns·CPU/pair 151 → 140; RSS +2.7 GB.
- K1 + K3 vs dense: **−26% wall, 188 → 140 ns·CPU/pair**. The architect's plan expected ≈ 18.5 → 14.3 → 12 s; measured
  19.1 → 15.3 → 14.15 s, so K3's measured gain is about half the ESTIMATE.
- Lever 1 (O1, the I1 check) is off in every variant, so its saving is not in this table; it is measured in the P7 pilot.
- These are stand-in data; the P7 calibration pilot with the production setup is the gate measurement (H-11).
