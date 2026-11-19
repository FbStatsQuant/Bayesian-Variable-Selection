# 10⁴ overlap: budget re-projection at the W0 checkpoint (Opus child, 2026-11-18; read-only analysis)

## Decision summary (8 lines)
1. **Expected rung total = 1,816 core-h (P10–P90 1,613–2,021)** counting all W0 spend (254.74 incl. the 91.5 evidence batches); 1,725 (1,522–1,929) with only the counted W0 batches (163.24). **Both are > 1.6k → HOLD W1 and go to HQ (H-18).** No stop rule has fired yet: actual 254.7; the monitor's projection is 1,724 (< 2.5k).
2. **What counts:** recommend all 254.74 (it was billed for the rung, the monitor's stop_rules already counts it, and the ledger bills it). HQ to confirm. Leaving out the evidence batches does not get under 1.6k either (P(> 1.6k) = 0.78).
3. **P(breach 1.6k) = 0.91** (0.78 with counted batches only); **P(breach 2.5k) < 0.01**. If every T fit escalates and none has a tail, the total is 2,279.
4. **Escalation:** 10.0 of the 18 T fits are expected to escalate (P10–P90 7–13); AR-strong 0.85, AR-weak 0.5, IND 0.35, ADJ-OPP 0.3, NULL 0.25. Tier 1 ≈ 110 / fit vs tier 0 48.3. **Tier 2 (N 160,000) cannot happen:** the coded rule allows at most one escalation.
5. **When 1.6k would bind:** W1 + W2 end at about 1,181 (P90 1,356; P(> 1.6k) < 0.002). The rule would trip during **W3** (6 AR fits, ≈ 635), so W3 is the real decision.
6. **Options, best first:** (A) raise the cumulative stop to 2.1k (≤ 2.5k): no change to the science, P(breach) 0.04. (C) W3 AR on T with s1 only: −0.3k, P 0.24, but weakens E1 on AR. (B) drop T s2 on IND and NULL: −0.13k, P 0.70, does not suffice alone. (D) drop AR r04: −0.2k, P 0.50. Stopping escalation is NOT allowed without Theory.
7. **Recommendation:** A. Under every option except B, W1 is unchanged and cannot breach 1.6k, so HQ can release W1 now and decide on W3 at the W2 read-back, which will have 12 escalation outcomes and the first AR seed pair.
8. **E1 is at moderate risk** on AR (judgement ≈ 1 in 4 for a miss on ≥ 1 AR dataset). A miss makes the outcome MARGINAL, not "not clean". Also, the PREREG addendum 1 (accept the N of `tier_final`) must land before W1 is read: about 10 escalated T fits would otherwise count as "not delivered" and fail D.

## 1. What drives escalation (coded rule, D-26; engine `include/v4/calib.h:262-286`, = core/v3_calib.R:144-193)
- The T calibration runs tier 0 (H 2,048, T_e 1,000, N_final 10⁴; up to ℓ = 14 rebuilds until the grid is bitwise identical). It escalates once to tier 1 (4× H, T_e and N → 40,000) if **any of 7 triggers** fires: E1, E2, E3, forced_pilot_steps, grid_failure, **grid_unconverged**, local_limit. The loop is `if (!fired || e == 1) break;`, so tier 1 is final. `calib.bin.json` lists only tiers 0 and 1.
- **W0 evidence:** the AR-T tier 0 ran all 14 rebuilds (cost files k1–k14, i.e. the cap ℓ was reached), so grid_unconverged almost certainly fired. Tier 1 then converged at k1. ADJ-OPP converged at k12 with no trigger, both in T2 and in the evidence run. The B3 run at p = 10k (REQUESTS R6) had converged = FALSE with both E2 and grid_unconverged; at 5k only E2 fired. E2 is noisy: with 4 islands it fires with probability 0.39 at σ = 1 and 0.68 at σ = 1.4 (REVIEW_fable). Triggers are not in the collected records (`calib.bin` was not collected), so "which trigger fired" is inferred.
- **Per design (ESTIMATE, judgement; a Beta prior per design + a per-dataset latent so that seeds of one dataset are correlated):**

| design | remaining T fits | P(esc) (range) | basis | E cost / T fit |
|---|---|---|---|---|
| AR-strong | 7 (r01 s2: 0.9) | 0.85 (0.6–0.95) | W0 escalated at the ℓ cap; B3 10k unconverged; "certain at p ≥ 5k" (F16) | 100.7 (r01 s2: 103.8) |
| AR-weak | 4 | 0.5 (0.25–0.75) | same correlated X, flatter posterior; E2 more likely, grid convergence unknown | 79.1 |
| ADJ-OPP | 3 (r01 s2: 0.2) | 0.3 (0.15–0.5) | W0 converged at 12/14 with no trigger | 66.8 (r01 s2: 60.6) |
| IND | 2 | 0.35 (0.15–0.6) | no measurement; easy posterior, but V still churns at p = 10⁴ | 69.9 |
| NULL | 2 | 0.25 (0.1–0.5) | no measurement; short likelihood range, small E2 dispersion | 63.7 |

## 2. Cost per T fit
- **Tier 0:** 48.3 (ADJ-OPP: calibration 35.8 + islands 12.3), modelled as N(48.3, 4).
- **Tier 1 after #86:** 110.0 (no refused islands now): tier-0 calibration at full ℓ ≈ 47 + tier 1 13.6 + islands at 40,000 49.2 (4 × 24 CPU, ≈ 35 min) + 0.15 for setup, merge and eval; modelled as N(110, 8).
- **Tail:** with probability 0.05 per escalated fit, the tier-1 calibration does not converge at k1. Each extra rebuild costs ≈ 12.5, up to the 3:00 × 48-CPU calibrate limit (144), which would end in a TIMEOUT, a failed stage and a stop rule. P(any T fit > 172.5) is 0.28 under this tail, 0 with no tail and 0.63 if the tail probability is 0.15. This is the main **per-fit** stop risk, and it rests on a single tier-1 observation. Worst case under the #86 limits: 344.7 per T fit.
- **Tier 2: impossible** (above). Even if Theory added one, it would cost ≈ 300–400 per fit, more than the 172.5 per-fit stop, and the islands (≈ 2 h at 4 × 24 CPU) would hit the 2:00 cap.
- **V:** 2.42 per fit, 18 left = 44.

## 3. Projection (Monte Carlo, 2·10⁵ draws; script `…/scratchpad/proj.py` in the session scratch, not kept)
| basis | E | P10 | P50 | P90 | P > 1.6k | P > 2.0k | P > 2.1k | P > 2.5k |
|---|---|---|---|---|---|---|---|---|
| W0 + evidence (254.74), **recommended** | **1,816** | 1,613 | 1,815 | 2,021 | **0.91** | 0.12 | 0.04 | < 0.01 |
| W0 counted only (163.24) | 1,725 | 1,522 | 1,724 | 1,929 | 0.78 | 0.04 | ≈ 0.01 | 0 |
| sensitivity, all P(esc) × 0.7 / × 1.15 (W0 + ev.) | 1,643 / 1,903 | | | | 0.59 / 0.99 | 0.02 / 0.25 | | 0 |

By wave (expected / P90): W1 447 / 569; W2 479 / 596; W3 635 / 733. Cumulative: 702 after W1, **1,181 after W2 (P90 1,356)**, 1,816 after W3.

## 4. Options (ranked; costs are expected remaining-rung savings, with P(> 1.6k) on the W0 + evidence basis)
| # | option | saves | new E (P > 1.6k) | scientific effect |
|---|---|---|---|---|
| **A** | Raise the cumulative stop 1.6k → **2.1k** (≤ the 2.5k ceiling); per-fit, wave and 2.5k projection rules unchanged | 0 | 1,816 (P > 2.1k 0.04) | None: 40/40, prereg intact. The cost is ≈ 0.2–0.5k more than the 1.6k line. CAMPAIGN_RUN_PLAN stage 1 (basis 2,806) and the H-14 margin (4.2–6.1k) absorb it |
| C | W3 AR r02–r04: T on **s1 only** (V keeps both seeds) | ≈ 310 | 1,499 (0.24) | D 37/40 (a logged deviation + script sha). s_T pooled over 7 datasets (7 df instead of 10). S1 rests on one T seed on 3 AR sets. **It weakens E1 exactly on AR**, the near-edge design |
| B | T s2 dropped on IND and NULL (W1) | ≈ 140 | 1,676 (0.70) | D 38/40; s_T over 8 datasets; S4 on one T seed. Not enough alone; B + C gives 1,359 (0.03) at 35/40. It also changes W1 |
| D | AR r04 dropped (T and V, both seeds) | ≈ 210 | 1,604 (0.50) | 9 datasets: the HPM "≥ 9/10" rule needs restating, AR has 3 reps. Worse value than C |
| ✗ | Stop T escalating (tier 0 only) | ≈ 620 | ≈ 1.2k | **NOT ALLOWED without Theory.** T would stop being the coded rule (D-26: theory mode keeps tier 1 = 4× N), the overlap would no longer link V to the theory, and W0's AR-T would not pair with the rest |

- Accounting alone (leave out the 91.5) does not fix it. Cheapest path to a decision: release W1 now (A, C and D leave it unchanged), and choose A or C at the W2 read-back on measured rates. W2 ends at ≈ 1.18k, well under 1.6k.
- Suggestion (cost-neutral): move AR r01 s2 (T + V) from W2 to W1. That brings forward the first AR seed pair (E1 yardstick) and the repeatability of escalation on one dataset.

## 5. W1 release data (if HQ releases)
- **Caps (worst cases from #86, T fit 344.7):** OV_W1_T = 6 × 344.7 = **2,068**; OV_W1_V = 6 × 46.7 = **280**; the wave reserves 2,348 against the envelope (Σ actual ≈ 1.23k + this ≪ 28.3k).
- **Monitor QUOTE for W1 = 450 core-h** (T 435 + V 15; P90 569), so the wave stop rule fires at **> 900**. Per-fit stops stay at T > 172.5 and V > 15. Cumulative stop: 1,600 unless HQ adopts A (2,100). The projection stop is > 2,500. Later quotes: W2 480 (stop > 960), W3 640 (stop > 1,280; the A + C variant: 320).

## 6. E1 at risk?
- E1 passes per dataset iff |Δ_d| ≤ 3·se_comb,d, with se_comb taken from the seed-pooled s_A and the island s.e. as a floor; all 10 datasets must pass (PREREG §3.4).
- If the floor binds at AR r01 (2-seed mean: √(0.0062²/2 + 0.0010²/2) = 0.0044) and s2 repeats Δ ≈ −0.015, the ratio is 3.4 and **E1 fails**. If the s1 gap is noise (a 2.4-σ draw), the expected 2-seed ratio is ≈ 1.7, a pass.
- The island s.e. leaves out the calibration-to-calibration variation (all R′ islands share one grid), so s_T and s_V are probably above the floor, which is lenient. **A systematic sign (V < T) on all AR sets would be a real N/tier effect** (V at N 2,500 vs escalated T at 40,000). E1 exists to catch that. It would give MARGINAL, and the precision study (N 2,500 vs 10⁴) would be the diagnosis.
- Escalation also mixes N inside s_T (one seed tier 0, the other tier 1). The analysis worker should report s_T by tier.
- Option C removes 3 of the 4 AR seed pairs that pin this down. That is a reason to prefer A.
