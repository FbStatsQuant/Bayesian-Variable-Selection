# WP3 architect confirmation on SPR (MEASURED, job 2749483, commit 39be5a08 = exp/P1M-wp3-arch, 2026-11-16 06:10–06:26 CST)

Exclusive node bb5u19c1. Socket 0: `tools/nots_bench_arch.sh` + early stages; socket 1: calibration-shaped island
(`V4_LEADERS=1`). Billed **51.7 core-h** (16.2 min × 192; quote ≈ 96, worst 160). Logs: `arch_2749483/`.

**Bit identity: PASS.** ref, check, bounded and gram all print `7ef6cfdb5cb8e748` (= jobs 2748756 and 2749328); early
stages ref = gram (`1839ac6500595b9c`). fma differs by design (D-28: not adopted).

## Late 10⁶ round (G = 256, one socket, 96 threads; round 5, the clean round after the resume; ns·CPU per pair = wall × 96 / pairs)
| variant | levers | wall s | **ns·CPU / pair** | × plan (200) | phase A s | products thread-ns/pair |
|---|---|---|---|---|---|---|
| ref | PR #26 + I1 check every step | 23.90 | 236 | 1.18 | 11.6 | 46.6 |
| check | − per-step check (lever 1) | 18.18 | 180 | 0.90 | 11.5 | 46.2 |
| bounded | + bounded scoring (lever 2) | 13.92 | 137 | 0.69 | 8.2 | 47.0 |
| **gram** | **+ Gram rows (lever 3)** | **11.77** | **116** | **0.58** | 6.1 | 23.7 |
| fma | + FMA (D-28: NO) | 11.39 | 113 | 0.56 | 5.8 | 18.7 |
Bounded scoring: flips per step 3.89 → 1.38. Gram rows: products computed for 54 of 151 active columns per pass.
Peak RSS 18.0 GB (ref) → 23.0 GB (gram: + 5 GB of Gram slots). Stand-in tables.

## Early bridge stages at 10⁶ (stand-in π₀, mean |S| ≈ 55; N = G = 64, 96 threads; φ = 0.01, 0.02, 0.03)
| stage | M (pairs/step) | ref: wall s / µs·CPU per step | gram: wall s / µs·CPU per step | gram split (s): phase A / build / phase B / compaction |
|---|---|---|---|---|
| 1 | 21.5 | 26.5 / 39.7 | 30.5 / 45.7 | 1.7 / 5.1 / 3.9 / 14.8 |
| 2 | 20.8 | 20.6 / 30.9 | 15.5 / 23.2 | 1.4 / 0.7 / 1.4 / 8.5 |
| 3 | 19.5 | 16.3 / 24.5 | 10.2 / 15.3 | 1.4 / 0.7 / 0.8 / 4.1 |
- Bounded scoring cuts flips per step 20 → 1.5 and the products to 1/7 (phase A 9.2 → 1.4 s), as on Owls.
- **But store compaction dominates the early stages** (π₀-sized new models are offered at almost every flip): 4–15 s of a
  10–30 s stage, in both variants. This is R3; the offer floor (D-29) targets it.
- N = 64 makes the per-step figures pessimistic (fixed per-pass costs over few particles). They are an upper bracket.
- Plan per step: 0.6 µs·CPU at M = 3. Early stages: ≈ 15–46 µs·CPU per step today (25–75× the plan per step). Without
  compaction (ESTIMATE, offer floor): ≈ 4–5 µs·CPU per step ≈ 230 ns·CPU per pair at M ≈ 20. **Per pair near the plan;
  the excess is M.**

## Calibration-shaped island (leaders on; socket 1; default build = bounded scoring on, check on; G = 256)
Wall 611 s; **phase B 266 s** (top-store-only islands: ≈ 55 s) → the serial leader-store compaction (R2) costs ≈ 210 s per
island, mostly in rounds 1–2 (round 2: 112 s). Late rounds 24–29 s (≈ unaffected). **Peak RSS 48.6 GB.** Hash
`86d5c36c3760aaf1` (leaders change the ledger, not the particle path).

## What this means
1. Late rounds: **116 ns·CPU per pair MEASURED (0.58× plan)** with levers 1–3, same bits. Builders 6–7 productionise them.
2. The 1M fit's cost is governed by the **mean M over the calibrated schedule** and by **early-stage compaction**, not by
   the per-pair kernel cost. Re-size per stage once WP2 gives the production π₀ size at 10⁶ and the schedule's M profile
   is known (10⁵ bridge: mean M 6.6 against the plan's 3).
3. Calibration islands need ≈ 50 GB and lose ≈ 210 s each to serial leader compaction until O3 (builder 7).
