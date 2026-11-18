# Campaign timeline and the 20-replicate option after the first 1M fit (Engineering, 2026-11-17)

Basis: 1M fit 6-AR-n200-r01-V-s1 = 437 core-h MEASURED (results/F1M_PILOT_FIT.md); T5 10⁵ fit = 42 MEASURED; MANIFEST_CELLS v0.4.

## 1. Re-costed 1M block (fits at 440 core-h, N 2,500; MEASURED basis)
| cell | plan v0.4 | at 440/fit |
|---|---|---|
| AR-strong × 3 (rep 1 = today's fit) | 3,565 | 1,320 |
| ADJ-OPP × 1 | 1,188 | 440 |
| self-check N = 5,000 on AR rep 1 data (≈ 2× island cost) | 2,221 | ≈ 730 |
| AR-weak (gated) | 1,188 | 440 |
| option D (AR-strong n = 1,000; ×3.43 as in v0.4) | 4,072 | ≈ 1,510 |
Planned excl. D: 18,014 → **≈ 12,800**; × 1.25 contingency ≈ 16.0k; + D (with contingency) ≈ 1.9k → **≈ 17.9k vs 28.3k**. The 10⁴/10⁵
blocks are still at plan values (T5 suggests the 10⁵ fits cost ≈ 40 % of plan); not credited.

## 2. Owner option: 20 replicate datasets of 6-AR-n200 at 1M
- +17 fits beyond the planned 3 (today's = rep 1, see §3): 17 × 440 ≈ **7,480**; ablations (6 %/dataset) ≈ 450; competitors at 1M
  (lasso + 1 variational + SIS, D-21) on 20 datasets ≈ 100–200.
- Total ≈ 12.8k + 8.1k = 20.9k planned; with 25 % contingency on the non-measured blocks only ≈ 24.6k; + D ≈ 26.5k → **fits under
  28.3k** (≈ 1.8k margin). Without option D: ≈ 24.6k. Nothing on top is needed unless option D's n = 1,000 cost exceeds 2×.
- Pacing at 1–2 fits at a time: one fit ≈ 3 h wall (≈ 8 SPR nodes for ≈ 1 h of islands, 1 node for ≈ 1.5 h of calibration). At 2
  concurrent and ≈ 4 fits per day: 19 fits ≈ 5 working days.

## 3. Pilot rule (Sol F7)
The merge memory re-size is a resource request (admission), not the method: V settings (N, R′, budgets, schedule rule, priors), the
data/seed scheme and the arithmetic are unchanged. Code merged after 2cfaa9e5 is same-bits (τ_cal select #59, checkpoint/restart
#60/#62; K2/K5 in review are same-bits). **Today's fit counts as replicate 1**, conditional on the campaign freeze commit
reproducing 2cfaa9e5's T3 hashes + goldens and one 10⁵ island hash (Owls + a ≈ 2 core-h NOTS check at freeze).

## 4. Gaps
- **Merge memory** (plan 43.7 vs 75.1 GiB measured): WP4 (Sonnet) measures the merge's components at 10⁵ (T5 records) and 10⁶ and
  fixes the plan; interim the driver's 10⁶ merge request → 128G.
- **Calibration 85 vs 55 min:** an estimate error, not a slowdown. The V calibration ran 3 iterations (12 diagnostic islands); the
  estimate assumed 2 (from T5). Per-island cost matched P7. O3 (parallel leader-store compaction) trims ≈ 12 % per island.
- `p1m_stage_cost.py` / `smcbvs4 info --meta` stall on 10⁶ island files → builder 7 fixes before campaign reporting.

## 5. Revised timeline (gates and validation order unchanged; the 10⁴ T-vs-V overlap stays first)
| step | needs | dates |
|---|---|---|
| campaign freeze commit | K2/K5 merged, merge plan + 128G, stage-cost tool, T6 restart test on NOTS (≤ 40), freeze hash check | Wed 11-18 – Thu 11-19 |
| 10⁴ overlap rung (T vs V, 20 + 20 fits) | freeze; HQ GO | Thu 11-19 – Sun 11-22 |
| precision study (64 islands) + 10⁴ science (156 fits) | overlap clean | 11-22 – 11-26 |
| 10⁵ rung (12 fits; option D gate) | 10⁴ done | 11-27 – 11-30 (owner priority over Thanksgiving) |
| 1M: AR-strong reps 2–3 (or 2–20), ADJ-OPP, self-check, AR-weak (gated), option D | 10⁵ trend | **from ≈ Tue 12-01**; 20 reps by ≈ 12-08 |
The 1M replicates could start before the 10⁵ rung only by changing the order, which the plan does not do.
