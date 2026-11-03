# p ≫ n theory evidence from the PROD-H rerun (EVIDENCE_H)

**Data.**
- 2,400 SMC-BVS v2.2.1 fits (run `20261030T0934Z_prodH`): n = 200; p ∈ {500, 1000}; S1–S6; c ∈ {1, 0.5}; 100 replicates.
- All 2,400 records match the 2026-10-23 records on the 11 compared fields; every available estimate reproduces exactly (`repro/`).
- Post-hoc measures come from `code/scoring/run_theory_H.R` on the rerun records. Truth is read only at scoring.

**Scope (D22).** Every quantity is either selection against the truth or a property of the fit and the data. No Ẑ or PIP accuracy is claimed at p ≫ n. Exactness questions are answered by the low-p study (`EVIDENCE_L.md`).

**Files.**
- `case_theory_H.csv`: one row per case. It holds the theory measures, the rerun fields (prefix `rerun_`) and the TD d = 0 columns for the sampled cases.
- `tables/ev_*.csv` and `tables/evidence_numbers.json`, produced by `scripts/evidence_h2.py`.

**Verdict scale.** All the theorems are conditional and/or asymptotic, and the data are a single n = 200 design. So a verdict is about what this design can show.
- **support:** the data agree with the statement, or with an observable consequence or premise of it, at this n. That is consistent with the statement, not a proof of it.
- **contradict:** the data refute the statement as worded. Failure of a finite-n *premise* of a conditional statement is reported as such, and is **not** a contradiction of the implication.
- **silent:** the data cannot speak to it here (asymptotic only, hypotheses not checkable, or quantity unavailable at p ≫ n).

## One-line verdicts

| Theory question | Verdict |
|---|---|
| T22 + T27 (Thm 2), start mass | **Masking: qualitatively consistent with T27.** π₀(S₀) is tiny, and the expected number of iid start hits Q_f·π₀(S₀) is below 1 in 2,393 of 2,394 completed fits. **T27's specific law and T22's hypotheses: silent.** Near-truth mass π₀(𝓡_d) is reported descriptively; it is substantial in most cells and lower in S4 |
| T37 (Thm 3), truth dominance and repair | **The finite-n TD(0, 0) premise fails in all 196 audited cases**, literal and "toward" alike. Truth-for-truth swaps explain the violations in the 4 diagnosed cases. **T37(i) (an implication) is not contradicted; T37(ii)–(iii): silent.** Local search never made an improving move. Clause (c) is a necessary local-optimality diagnostic |
| T38 (Thm 5), HPM consistency with delivery; cost | **Observed first discovery: in the pilot SMC, by Gibbs flips or swaps, in every completed fit.** This motivates a pilot-discovery / T24-type route. **T38(b2)'s formal premises: unverified (silent).** **Cost: descriptively consistent with polynomial scaling** (two values of p) |
| T21 (Thm 4), error decomposition | **Consistent with T21's decomposition; its probability bound is untested (silent).** Operationally: 6 no-output + 565 completed misses, each with a scored competitor above the truth, and 0 detected search misses. The discovery term itself is not identified (between 0 and 565 completed fits) |
| Resource stop vs complete run | **Small observed completion gap.** 2,394/2,400 completed every phase. The 6 runtime-guard stops (all S5, tier 1) could change at most 6 recoveries (0.25 points). P5 was not run (D62), so the retry effect is unknown |
| T03 / T07 (Thm 1, Prop 1), concentration; same-size swaps | **T03: silent** (asymptotic); posterior concentration on S₀ is visibly incomplete at c = 0.5. **T07: support / relevant:** 207 of 565 completed misses (37%) are equal-size wrong supports, which no size-only prior can repair |
| T26(i)–(ii), T12 (Thm 6, Prop 2) | **Silent at p ≫ n** (D22). RB and plain PIPs agree internally: MPM identical in 2,391/2,394 fits, max \|Δ\| 0.0067 |

---

## 1. T22 + T27 (Thm 2): start mass on the truth and near it

**Quantities.**
- π₀(S₀) and π₀(𝓡_d) for d = 0, 1, 2, from the exact block DP.
- The expected number of final-run iid start draws equal to S₀: Q_f·π₀(S₀), with Q_f = 4N_e(T + L + 5) (T21/T27). Here N_e = 2,500 at tier 0 and 10,000 at tier 1, T = the realised final bridge stages, and L = 8.
- Each completed fit is binned as "iid intensity ≥ 1" or "< 1". This is a **descriptive finite-n bin**, not T22(iii)'s hypotheses or T38(a)'s Q_f·π₀(S₀) → ∞.
- Tables: `tables/ev_start_mass.csv` (per p × c × scenario), `tables/ev_recovery_by_pi0R0.csv` and `tables/ev_case_derived.csv`.

**Findings.**
- **π₀(S₀) is tiny.**
  - Median log₁₀ π₀(S₀) by cell is −12.4 to −25.6; the largest over all 2,400 cases is 10^−5.6.
  - The iid intensity Q_f·π₀(S₀) is below 1 in **2,393 of the 2,394** completed fits.
  - The one exception is `p0500_S2_r034_c100`, with intensity ≈ 1.09. There the truth was in fact first scored in the pilot (stage 2), not by final-run iid draws.
  - The cell median of π₀(S₀) falls by about 2–4 orders of magnitude (1.9–4.1) from p = 500 to p = 1000 in every scenario × c cell.
- **Near-truth start mass** (descriptive eligibility inputs; no b_n is specified, so no pass/fail). Pooled medians: π₀(R₀) = 0.20, π₀(R₁) = 0.56, π₀(R₂) = 0.81.

  | Scenario | π₀(R₀) | π₀(R₂) |
  |---|---|---|
  | S1 | ≈ 0.5 | ≈ 0.95 |
  | S4 | ≈ 0.005–0.02 | ≈ 0.25–0.40 (lower mass: a potential difficulty) |
  | S5 | — | median 0.86–0.95; a few fits have π₀(R₂) ≈ 0 |

- **Recovery does not track near-truth start mass at c = 1.** HPM recovery is 93–94% in every π₀(R₀) bin up to 0.75. At c = 0.5 it rises from 53% (π₀(R₀) ≤ 0.25) to 65–68% (0.25–0.75).

**Verdicts.**
- **Masking (T27): qualitatively consistent.** The start puts negligible mass on S₀ itself, and that mass shrinks with p.
- **T27(i)'s joint n/p law: silent.** One n, two values of p, and the completion-chain ratio law is unchecked.
- **T22(iii) and T38(a): silent.** Their hypotheses are not checked. Provenance (§3) identifies the pilot SMC as the source of first truth discovery in the 1,829 hits.
- **T22(i) and T38(b) premise π₀(𝓡_d) ≥ b_n: silent.** b_n is unspecified; the masses above are reported as inputs.

## 2. T37 (Thm 3): truth dominance TD(d, m) and greedy repair

**What was run.**
- **TD audit at d = 0, m = 0** (centres = all 2^14 − 1 proper subsets of S₀, plus S₀), both the literal and the "toward" variant.
  - It covers a fixed sample of 196 cases chosen before any TD result: replicates 1, 25, 50, 75 and 100 in every p × c × scenario cell, plus every c = 1 HPM miss.
  - 18.7 core-h.
  - At d = 0 the centres contain no null variable, so the two variants coincide (checked: identical violation counts in every case).
  - The sample is enriched for misses. Percentages and hit/miss associations below are **unweighted descriptions of the sample**, not population estimates.
- **Move-type diagnosis** (`scripts/td_diagnosis.R`, `tables/ev_td0_diagnosis*.csv`) on 4 cases only: p500 S1 and S4 at c = 1, and S3 and S5 at c = 0.5.
- **The production local search's trace** in every fit: centre, moves and returned model (`tables/ev_local_search.csv`).

**Findings.**
- **The finite-n TD(0, 0) premise holds strictly in 0 of the 196 audited cases** (all 196 audits complete).
  - Clause (a) ("some missing truth's add beats every other move") fails at a median 77% of the 16,383 proper subsets (range 50–98% across cases).
  - Grouping the cases by p × c × scenario, the cell median of the clause-(a) minimum margin runs from −12.1 to −7.8 nats.
- **In the 4 diagnosed cases the competing move is mostly a truth-for-truth swap.**
  - At a subset S ⊂ S₀, dropping a weakly contributing present truth and adding a strongly contributing missing truth gains more than adding the missing truth alone, because the add pays the size penalty.
  - Such a swap leaves |S Δ S₀| unchanged: a lateral move, neither a "toward" move nor a regressive one.
  - This is a failure mode distinct from the d ≥ 1 truth-in swap documented at low p.
  - Share of clause-(a) violators whose best competing move is a truth-for-truth swap:

    | Case | truth-for-truth swap | other best competing moves |
    |---|---|---|
    | p500 S1 c = 1 | 100% | none |
    | p500 S4 c = 1 | 79% | 15% truth-out/null-in swaps, 5% null additions |
    | p500 S3 and S5, c = 0.5 | > 99% | — |

  - Violators concentrate at mid-size centres (5–8 of the 14 truths). Whether the same mechanism dominates the other 192 cases was not diagnosed.
- **Clause (c) (S₀ is a strict local maximum)** holds in 92 of the 92 sampled hits and fails in 97 of the 100 sampled posterior misses.
  - In the other 3 misses, S₀ is a local maximum but the HPM is a better non-neighbour. The remaining 4 sampled cases are stops.
  - So clause (c) is a necessary local-optimality diagnostic for a hit, not a sufficient one.
- **The production local search ran and scanned in every completed fit, but made no improving move** (0 moves in 2,394 fits).
  - In the 1,829 hits, the centre was already S₀.
  - In 541 completed misses the centre lay in 𝓡₂ ∖ {S₀}. Each of these has F(centre) ≥ F(S₀), so no improving path to S₀ exists.

**Verdicts.**
- **TD(0, 0) as a finite-n premise: fails at this design** (0/196).
- **T37(i)** ("if strict TD holds then greedy repair") is an implication whose antecedent fails here: **not contradicted**.
- **T37(ii)–(iii)** (union bound; asymptotics under G/R/SE/BM-∞): **silent**.
- **For the theory phase:** a repair premise that can hold at n = 200 must tolerate lateral (|S Δ S₀|-preserving) moves. These are noted for Fable's statement refinement, not proposed as fixes here. Examples:
  - a potential-function condition on F;
  - dominance stated only along the realised greedy path.
- **Repair by improving moves: not exercised** at p ≫ n.

## 3. T38 (Thm 5): consistency of the reported HPM with delivery; polynomial cost

**Observed first discovery.**
- The reported HPM's provenance (the phase and mechanism that first scored it) is **the pilot (calibration) SMC in all 2,394 completed fits** (`tables/ev_hpm_provenance.csv`).
- For the 1,829 hits, the truth was first scored by Gibbs flips (1,724), neighbour swaps (104) and a uniform swap (1).
- Example: `p0500_S2_r034_c100` first scored the truth at pilot stage 2 (φ ≈ 0.024).
- Neither final-run iid draws (§1) nor local-search moves (§2) were the source.

**Cost when p doubles** (500 → 1000; medians; `tables/ev_cost.csv`): ×2^1.07 fresh scores, ×2^1.5 distinct models (HLL estimate), ×2^1.4 runtime. Escalation to tier 1:

| | p = 500 | p = 1000 |
|---|---|---|
| c = 1 | 9.5% | 18.7% |
| c = 0.5 | 1.0% | 5.5% |

**Verdicts.**
- **Observed first truth discovery in the pilot, by Gibbs flips or swaps.** This motivates a pilot-discovery / T24-type route for T38.
- **The formal premises of T38(b2) are unverified: silent.** That covers T24's conditions, an eligible particle at the terminal rounds, and the asymptotic delivery probability. Pilot provenance does not identify a terminal-round repair trajectory.
- **(a) and (b1): silent.** (b1) was never exercised by an improving move.
- **(c) cost: descriptively consistent with polynomial growth.** Roughly linear to p^1.5 between two values of p. That is not a test of the asymptotic cost corollary.
- **Not tested:** eligibility, the T24 conditions and the asymptotic delivery probability.

## 4. T21 (Thm 4): P(wrong) ≤ P(U) + 2E[mass off the truth] + P(Uᶜ, truth never scored)

**An operational, score-based decomposition** (`tables/ev_miss_class.csv`; F(S₀) from the scorer):
- **no output:** primary `resource_limit`; P5 not run.
- **detected search miss:** F(S₀) > F(HPM). The truth beats the report, so it was never scored.
- **completed miss with a scored competitor above the truth:** F(S₀) ≤ F(HPM), with HPM ≠ S₀. (This was labelled "posterior miss" in the tables.)

| | hit | completed miss, competitor above truth | detected search miss | no output |
|---|---|---|---|---|
| p500, c = 1 | 559 | 40 | **0** | 1 |
| p1000, c = 1 | 560 | 37 | **0** | 3 |
| p500, c = 0.5 | 370 | 230 | **0** | 0 |
| p1000, c = 0.5 | 340 | 258 | **0** | 2 |

- There are no exact ties: the smallest F(HPM) − F(S₀) is 0.0049 nats, 23 of 565 are within 0.1 nats, and 39% are within 1 nat.
- The scorer's `miss_class` agrees in every completed fit.

**What this does and does not show.**
- **Shown:** each of the 565 completed misses has a scored competitor above S₀. Even scoring S₀ could not have made that report a hit; the error would remain.
- **Not identified:** whether S₀ was ever scored in those 565 fits. So T21's discovery term P(Uᶜ, S₀ ∉ 𝒮) is not identified: its count among completed fits lies anywhere between 0 and 565.
- **Why:** the per-model truth trace and the scored mass are unavailable at p > 64, because the registry runs in HLL mode (`truth_scored`, `log_sum_exp_F` and `first_scored` are NA/NULL in all 2,400 records). HPM provenance certifies that S₀ was scored only in the 1,829 hits.
- **Not evaluated:** the posterior-mass expectation 2E₀[1 − π(S₀)].

**Verdict.**
- **Consistent with T21's decomposition:** every wrong report is no output (6) or a completed miss with a scored competitor above S₀ (565); there are 0 detected search misses.
- **T21's probability bound: untested (silent).**

## 5. The gap between resource stops and complete runs

- **Completion:** 2,394/2,400 fits (99.75%) completed every phase.
- **The 6 stops** are runtime-guard stops at the allocation (6,300 s at p500; 24,000 s at p1000) (`tables/ev_stops.csv`):
  - all in S5 and all in tier-1 (escalated) runs;
  - five in the calibration diagnostic phase, one in the final bridge.
- **Audit-only supports at the stop:** at c = 1 the saved support equals S₀ in 3 of 4; at c = 0.5 it does in 0 of 2. These are not counted.
- **P5 (same-seed retry at doubled allocation) was not run** (Felipe, D62).

**Verdict.**
- **Maximum effect of completing the stops:** at most **6** additional recoveries overall (0.25 percentage points of 2,400). By p × c pool:

  | | c = 1 | c = 0.5 |
  |---|---|---|
  | p500 | 1/600 | 0/600 |
  | p1000 | 3/600 | 2/600 |

- **The observed retry effect is unknown.**
- The incomplete fraction is small at this design. That is an observation, not a verification of the theorems' complete-run assumption.

## 6. T03 / T07 (Thm 1, Prop 1): concentration and equal-size wrong supports

The shape of the 565 completed misses (competitor above truth), HPM against S₀ (`tables/ev_posterior_miss_shape.csv`). "Same-size" means an equal-size wrong support, not necessarily a single-variable swap.

| | superset | same-size | subset | mixed size | median gap F(HPM) − F(S₀) |
|---|---|---|---|---|---|
| c = 1 (77) | 70 | 6 | 0 | 1 | 0.6–0.9 nats (supersets) |
| c = 0.5 (488) | 97 | 201 | 133 | 57 | 0.7–2.8 nats by shape |

- **At c = 1** these misses are almost all "truth + one extra variable" (median FP = 1, FN = 0), with small gaps. A spurious addition scores above S₀.
- **At c = 0.5** all shapes occur, and equal-size wrong supports are the largest class. 490 of 1,200 c = 0.5 fits miss; 488 of those are completed misses with a competitor above S₀ (the other 2 are stops).

**Verdicts.**
- **T03: silent.** It is asymptotic and states that no finite-n rate follows. Posterior concentration on S₀ is visibly incomplete at n = 200, c = 0.5.
- **T07(i): support / relevant.** 207 of the 565 completed misses (37%) are equal-size wrong supports, where the likelihood ranks a wrong model of the true size above S₀. No size-only prior can repair these, which bounds what prior tuning could gain.

## 7. T26(i)–(ii), T12 (Thm 6, Prop 2): evidence and PIPs

**At p ≫ n exactness is not assessed (D22).** Only internal agreement between the two PIP estimators is reported (`tables/ev_pip_rb_plain.csv`):
- **MPM agreement:** MPM(RB) = MPM(plain) in **2,391 of 2,394** completed fits. In each of the 3 exceptions, a single variable's two PIPs straddle 0.5, within 0.003 of each other.
- **PIP differences:** the largest |RB PIP − plain PIP| over all variables and fits is 0.0067; per-fit maxima have median about 0.002.
- **Recovery:** plain-MPM recovery equals RB-MPM recovery except in one fit (p1000, c = 0.5, S3).
- **Island spread of log Ẑ (stored only; not an accuracy measure):** the median sd across the four islands is 0.06–0.25.

**Verdicts.** T26(i)–(ii) (accuracy) and T12 (unbiasedness): **silent at p ≫ n.** They are tested against the exact posterior in `EVIDENCE_L.md`.

## 8. Scored-model registry and score ledger

- **Mode:** the registry is in HLL mode in all 2,400 fits, by design (exact mode only for p ≤ 64).
  - **Available:** the HLL estimate of distinct models scored. Medians are 1.1–1.3 × 10⁸ at p500 and 3.2–3.7 × 10⁸ at p1000, of which about 52–58% were already scored after calibration.
  - **Not available:** the scored mass `log_sum_exp_F` and the phase × mechanism matrix of first scores (`first_scored`). The per-model truth trace exists only at p ≤ 32 (low-p study).
- **Stand-in:** the final-run fresh-score ledger (`fit$score_counts$fresh`, pooled over completed fits).

  | By phase | share | By mechanism | share |
  |---|---|---|---|
  | final bridge | 72.6% | Gibbs flips | 97.9% |
  | burn-in | 18.2% | neighbour swaps | 1.7% |
  | measured rounds | 9.1% | uniform swaps | 0.17% |
  | | | independence proposals | 0.11% |
  | | | local scan | 0.003% |

  The ledger covers the final run only.

## Appendix: superseded adaptive-lasso rows (ridge pilot; kept here only, HQ D86)

The original F3 fits (2026-10-19/21) used a ridge pilot for the adaptive weights. BENCH-AUDIT replaced it with the lasso `cv_min` pilot (D42). The rerun's rows are in HEADLINE_H.md. The old pooled exact recoveries /600 were (from `../H_existing_20261030/tables/all_rules_recovery_long.csv`; per-scenario cells in `tables/headline_h2_long_preF3.csv`):

| Rule (ridge pilot) | c = 1: p500 | p1000 | c = 0.5: p500 | p1000 |
|---|---|---|---|---|
| `ebic1_K37` | 247 | 96 | 36 | 12 |
| `cv_min` | 0 | 0 | 0 | 0 |
| `cv_1se` | 9 | 0 | 0 | 0 |

## Method notes and limits

- **TD is sampled (D68):** 196 of 2,400 cases, chosen before any TD result was seen. Full TD would cost about 90 core-h.
- **TD covers d = 0 only.** d = 1 at p = 1000 costs about 1.4 × 10¹¹ scores per fit (THEORY_MEASURES.md); the restricted-pool d = 1 option was not run.
- **The move-type diagnosis covers 4 cases.**
- **The theory rows were computed on both the 10-23 fits and the rerun fits.** They agree, because the fits are identical. The headline numbers use the rerun.
- **Review:** Sol R1 ACCEPT WITH FIXES (`review/SOL_REVIEW_H2_R1.md`). All 8 findings are applied; see `review/REVIEW_RESOLUTION.md`.
