# CONFIRMATION RESULTS — sealed set C, S1–S6 × 200 (fresh seeds 508001–513200), 2026-10-14
Frozen rule: confirm/CONFIRMATION_FREEZE.md (sha256 87ef87a3…, written before C existed). Tables: Owls E/confirm/out/analysis/TABLES.md
(local C:\Users\felip\BVS_campaign_data\vs_20261013\confirm\analysis\). Provisional (unreviewed AI code).

## Identification (SMC decisions, /200)
| rule | S1 | S2 | S3 | S4 | S5 | S6 | total /1,200 |
|---|---|---|---|---|---|---|---|
| BB(1,30)-HPM (candidate) | 173 | 178 | 160 | 71 | 143 | 121 | **846** |
| Bern(0.2)-HPM | 160 | 165 | 149 | 84 | 137 | 115 | 810 |
| Bern(0.2) median (current) | 159 | 165 | 143 | 75 | 131 | 102 | 775 |
| Bern(0.2) BFDR 5 % (current) | 173 | 171 | 126 | 25 | 118 | 67 | 680 |
| BB median | 172 | 175 | 150 | 70 | 141 | 105 | 813 |

## Frozen endpoints
- W1 BB-HPM vs median@Bern: +71; discordant 102 vs 31; exact McNemar p = 4.9e-10 (Holm 9.8e-10) → HOLDS (predicted +40 to +60).
- W2 BB-HPM vs HPM@Bern: +36; discordant 63 vs 27; p = 1.9e-4 (Holm 1.9e-4) → HOLDS (predicted +30 to +50).
- G1 per scenario (≤ 10/200 below either comparator): **FAILS in S4**: BB-HPM 71 vs Bern-HPM 84 (−13; discordant 3 vs 16, p = .004); vs median −4 (passes).
  All other scenarios BB-HPM ≥ both comparators (S1 +13/+14, S2 +13/+13, S3 +11/+17, S5 +6/+12, S6 +6/+19 vs Bern-HPM/median).
- G2 swap stratum S3+S4+S6 (n = 600): BB-HPM 352 vs Bern-HPM 348, median 320, BFDR 218 → passes.
- G3 engine gates (BB vs exact BB): all PASS in all six scenarios (median |log Ẑ_hyb err| 2.3e-4–4.0e-4; p95 ≤ 1.05e-3; exact HPM ∈ V 1,200/1,200;
  SMC HPM = exact HPM 1,200/1,200; median agreement ≥ 199/200).
- G4 (report): truth-included BB-HPM vs Bern-HPM: S1 187/193, S2 191/192, S3 170/171, S4 76/97, S5 152/161, S6 133/133. S4 mean FN 1.08 vs 0.78.
  Hybrid Ẑ RMSE (%): BB 0.037–0.056, Bern 0.052–0.091. Product Ẑ RMSE: BB 1.01–4.41 (S4 max 20.4 %), Bern 0.90–2.05.
- Prediction check per scenario (/200): S1 173 (predicted 180–192, below: fresh S1 data are harder for every rule, median 159 vs dev 176/200 equivalent),
  S2 178 ✓, S3 160 ✓, S4 71 ✓ (range 56–76), S5 143 ✓, S6 121 ✓.

## Verdict under the frozen rule
W1 and W2 hold with large margins and the engine gates pass, but guardrail G1 fails in S4, so the frozen label "CONFIRMED" is NOT granted.
Precise statement: "BB(1,p)+HPM beats the current rule and Bern(0.2)+HPM out of sample when pooled over S1–S6 (+71 and +36 per 1,200), and in 5 of 6
scenarios; in the strongest-correlation design S4 (ρ = .85) it is worse than Bern(0.2)+HPM by 13/200 because it omits weak true signals (truth
included 76 vs 97)." Consistent with the W1–W6 limitation: the multiplicity penalty costs weak or highly-confounded signals.
Per Felipe's instruction the candidate remains BB(1,p)+HPM (no evidence against it pooled); the S4 loss is carried as a documented limitation and a
design target for the next stage (correlated designs at p >> n).
