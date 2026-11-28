# R1 re-size of the 1M fit with the production start law (2026-11-16)

**Input (MEASURED, WP2, p = 10⁶, n = 200, production partition and start law):** E_π₀|S| = 3.61 (AR), 3.86 (IND); quantiles
q50/q90/q99 = 3/5/7 (AR), 4/5/7 (IND); expected blocks touched = 3.61 / 3.86 (exact; 2,000 π₀ draws: 3.58 / 3.83).
The stand-in start law of every bench so far had E|S| ≈ 56. **The production start law is ≈ 15× smaller.**

**Model:** the architect's `tools/arch_resize_model.py` (WP3_ARCH_REVIEW.md §8; branch exp/P1M-wp3-arch a01f4627), run
at E0 = 3.6 / 3.9 (full output: `R1_resize_model_output.txt`). Per-step anchors are MEASURED on SPR (jobs 2749328,
2749483), the stage profiles MEASURED (G0 5k / 10k, the 10⁵ bridge). The fit totals are ESTIMATES.

## Core-h per 1M fit (16 islands + calibration ≈ 3 island-equivalents) vs H-10's 1,188
| code state | late M = 3.9: central [low, high] | × H-10 | late M = 5.5 (G0): central [low, high] | × H-10 |
|---|---|---|---|---|
| today (be24e9d) | 2,273–2,284 [1,704, 4,256] | 1.9 | 2,705–2,718 [2,128, 4,699] | 2.3 |
| levers 1–3 | 1,415–1,422 [886, 3,274] | 1.2 | 1,504–1,511 [975, 3,363] | 1.3 |
| **levers 1–3 + m3 sort fix** | **995–1,002** [741, 1,890] | **0.8** | **1,084–1,091** [830, 1,978] | **0.9** |
| + offer floor (D-29) | 766–771 [696, 997] | 0.6 | 855–860 [785, 1,086] | 0.7 |
The bracket is driven by the offers per step in a bridge stage (0.01–0.10); the offer floor removes most of it.

## Budget consequence (total ≈ 27,608 + 15,293 × (f − 1), f = fit / 1,188)
- levers 1–3 + m3: f ≈ 0.8–0.9 → **≈ 24.6k–26.1k** (central); high bracket f ≈ 1.6–1.7 → ≈ 37k.
- + offer floor: f ≈ 0.65–0.72 → **≈ 22.3k–23.4k** (central); high ≈ 26.8k.
- today's code: f ≈ 1.9–2.3 → ≈ 41k–47k. **The 1M fits must not run on today's code.**

## Gate (proposed)
No 1M stage is released before levers 1–3 + m3 (builders 6–7, WP3 #43) are merged **and** measured on SPR with the
production setup (the calibration pilot at 10⁶ of WP3_ARCH_REVIEW.md §8 (c), ≈ 27–50 core-h). The offer floor (D-29)
narrows the bracket and is worth doing before the 1M fits. n = 400 / 1,000 (option D) E0 values follow from WP2.
