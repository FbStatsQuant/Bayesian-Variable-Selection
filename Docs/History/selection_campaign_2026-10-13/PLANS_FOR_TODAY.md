# Five plans, in the order to try them (VS campaign, round 1, 2026-10-13)

Ranking by Fable (fable/03_final_selection_reply.md) after an Opus red team (redteam/RT1_round1.md); the lead adopted it unchanged.
All numbers are on the development set D (600 datasets already used for selection). They are provisional: the code behind them is
AI-written and unreviewed (CODE_LEDGER.md).

## Where things stand (evidence)
| rule @ prior | S1 | S2 | S3 | S4 | S5 | S6 (/100) | S1–S5 /500 |
|---|---|---|---|---|---|---|---|
| CURRENT median @ Bern(0.2) | 88 | 79 | 72 | 29 | 65 | 49 | 333 |
| CURRENT BFDR 5 % @ Bern(0.2) | 93 | 87 | 57 | 12 | 56 | – | 305 |
| HPM @ Bern(0.2) | 87 | 81 | 73 | 33 | 63 | 63 | 337 |
| **HPM @ BB(1,p)** | **93** | **90** | **76** | **33** | **73** | **66** | **365** |
| count-level BFDR q=.05 @ Bern(0.2) | 93 | 88 | 74 | 29 | 70 | 37/50 | 354 |
| ceiling: any size prior + HPM | 100 | 98 | 83 | 43 | 85 | – | 409 |
S6 is exact (stratified enumeration, all 100). S1–S5 are visited-set reweighting, validated (exact = V in 300/300 on S6), pending the exact pass.
Costs of BB(1,p)-HPM: truth-included S1 95 vs 99 (median); vs Bern-HPM −4/−3/−4/−8 in S1–S4; S4 errors per dataset (FP+FN) 1.72 → 1.93;
S4 datasets keeping the cancelling pair (2,3) 86 → 72. Swaps are a data ceiling: the truth is not the best model of its size in
0/2/17/57/15 of S1–S5 datasets, and S6 swaps (26–29/100) do not move under any size prior.

---

## Plan 1 — BB(1,p) + HPM inside the SMC, with a corrected exact start (confirmatory)
**What.** Use a beta-binomial model prior BB(1,p) (Scott & Berger 2010; Wilson et al. 2010 default) with the highest-posterior model,
keeping the median as the secondary rule. The SMC change keeps everything exact:
- c_k = Σ_{|S|=k} m̃(S) by convolving the per-block size profiles of the 2^5 block tables;
- Z_0 = Σ_k c_k B(1+k, 2p−k)/B(1,p) is exact;
- start: draw k ∝ c_k B(1+k, 2p−k), then the block sizes given k by dynamic programming, then S_b given its size (exact for any size-only prior);
- the φ-bridge is unchanged (its weights depend on S only);
- collapsed Gibbs log-odds log((|S_−j|+1)/(p−|S_−j|−1+p)) + φ Δℓ + (1−φ) Δℓ̃;
- P(h | y) by Rao–Blackwellisation.

Do not use "draw h ~ Beta, then S | h". The red team showed that start samples the wrong distribution.

**Runs today (Owls).**
- (a) Stratified exact enumerator on the 500 S1–S5 development datasets, in 5 jobs of 100 or fewer (~13 s per dataset on 60 cores; S6 is done).
- (b) Build the corrected start and collapsed Gibbs. Unit gates on 5 datasets:
  - the start's distribution of |S| equals the exact π_0(k) (χ², p > .01);
  - a run with m = m̃ returns Z_0 to 1e-10.
- (c) Accuracy bench: 20 datasets × 3 SMC seeds × S1–S6 under BB, plus 120 runs under Bern(0.2) for the seed-SD comparison, all against the exact references from (a).
- (d) Cross-check: the prior-continuation path (validated Bern(0.2) run to φ = 1, then an ESS-adaptive path to BB) on 10 datasets.
- (e) Generate and seal the confirmation set C: S1–S10 × 200, seeds 508000 + 1000(k−1) + r, generator SHA-256s.

C enumeration (~300–450 CPU-h) runs on NOTS **only on your go**.

**Decision.** The engine passes only if all of these hold:
- median |log Ẑ error| ≤ 1e-3, 95th percentile ≤ 1e-2;
- PIP MAE on variables with exact PIP in [.05, .95] ≤ 2× the current engine's;
- exact HPM inside V in ≥ 99 %;
- SMC decision = exact decision in ≥ 97 %;
- across-seed SD of log Ẑ ≤ 2× that under Bern(0.2).

Development bars: BB-HPM ≥ median + 20 and ≥ Bern-HPM + 15 pooled on S1–S5 (exact), and S6 ≥ Bern-HPM − 2 (met: 66 vs 63).

On C, the win requires the multiplicity stratum (S1, S2, S5) pooled to beat both the median and Bern-HPM (McNemar p < .05, Holm). Guardrails:
- the swap stratum is no worse than any comparator by more than 2/100;
- truth-included is below the median by no more than 5/100 and below Bern-HPM by no more than 10/100;
- pooled Hamming error is no worse than either comparator's;
- S7–S10 are within 5/100 of the median.

The predicted omission costs above are written down before unsealing.

**p = 200 version.** Same construction (40 blocks; the convolution costs O(p²)). Compare against Bern(1/(p+1)) or EB-h, not Bern(0.2). It needs Plan 3's HPM check.

## Plan 2 — Weak-signal stress test (S10-dev) before committing the confirmatory slot
**Why.** BB(1,p) is harshest when the truth is small and weak: the prior odds of the first inclusion are 1/59. The development data have no |β| below .5.

**Runs today (Owls).** S10-dev: |S*| ∈ {2,3,4}, |β| ~ U(.25,.45), S5-type correlation, 100 datasets, seed band 117000 + r (C keeps 517000 + r). The exact pass takes ~25 min. Score all size priors, the median, BFDR 5 % and Plan 4.

**Decision.** If BB-HPM is more than 5/100 below the median, or its mean FN exceeds the median's by more than 0.3, the confirmatory candidate becomes **Bern(0.2) + HPM**: no prior change and no engine change, +4 on S1–S5 and +14/100 on S6 vs the median, with no truth-included loss. BB is then reported as a prior for strong-signal regimes only.

## Plan 3 — p = 60 exact scaling test with a certified HPM (does the rule generalise in p?)
**What.** A p = 60 generator (12 blocks, S5-type correlation, |S*| ∈ {2,5,10}, strong- and weak-β arms) with size-truncated exact enumeration |S| ≤ 8 (~3.4e9 models, same C++ path). The SMC checks the tail beyond size 8.

Annealing past φ = 1 (π_κ ∝ [p(S)m(S)]^κ after Z and PIPs are frozen) is tested as the large-p HPM search against the certified HPM.

**Today.** Build the generator and the truncation, time 2–4 datasets, and confirm the tail mass beyond size 8 is below 1e-3 under BB(1,60) and Bern(1/61). The full run (6 arms × 50) is tomorrow.

**Decision.**
- If BB(1,p)-HPM loses to Bern(1/(p+1))-HPM or a fixed-h Bern by more than 5/100 in any arm, BB is not p-generic and the large-p recommendation switches.
- If the annealed HPM matches the certified HPM in fewer than 95 % of datasets, the large-p HPM claim is withdrawn.

## Plan 4 — Count-level hierarchical BFDR (exploratory; replaces the per-variable BFDR family)
**What.** Compute lfdr on nested cluster-count events K_b ≥ k over X-only clusters, then take the conditional mode. An occupied cluster has lfdr ≈ 0 even when its mass is split, so the rule no longer collapses in S3–S5:
- old BFDR 5 %: 57/12/56;
- this rule: 74/29/70, while keeping 93/88 on S1/S2.

The target is unchanged (Bern(0.2)), so Z and PIPs are untouched. It is labelled an "FDR-type rule": control is on count events, not on identities.

**Today.** Score it on S6 r51–100 (needs the S6 visited sets r51–100 on Owls, ~2 min).

**Decision.** It is judged against per-variable BFDR 5 % only. On C it must beat it pooled on S1–S5 (McNemar p < .05) with no scenario worse by more than 3. Its result against BB-HPM is reported, but no claim is made.

## Plan 5 — Honest output where the data cannot decide (companion, different metric)
**What.** Report the HPM with P(HPM | y), the u65-optimal top-k model set (whole joint models, which keeps signs and the cancelling pair), and BLiP regions at q = .05.

**Today.** From the exact development pass:
- how often the certificate P(HPM) ≥ .5 fires (expected rare);
- the u65 set size and coverage;
- nominal vs empirical coverage of 90 % model sets.

**Decision.** On C, 90 % model sets must reach ≥ 85 % empirical coverage in every scenario and mean set size ≤ 4 in S4. It is killed if coverage falls below 60 %. It never counts toward the exact-recovery win.

---

## Freeze before C is unsealed
- Rule definitions: HPM tie-break, V window, BB a = 1, b = p; comparators {median, BFDR 5 %, Bern-HPM}; strata, Holm, the guardrails above with the written predictions; the Plan 2 decision.
- Engine build hash and settings: N, blocks, polish sweeps, seed offsets. The primary in-engine arm is the size-convolution start; the prior-continuation path is a cross-check only.
- C: generator SHA-256s, seeds, S9 β floor .25, S10 spec, and a manifest of 2,000 datasets.
- A one-pass analysis script with failure anatomy, FN/FP/Hamming, and the Plan 4 and Plan 5 definitions.

## Killed this round (numbers in CANDIDATES.md)
- Occupancy/identity rules: OMI 358, OF-HPM 361, count-first HPM 358.
- Γ-robust rules: maximin 351; persistence = BB-HPM.
- κ-MPM 362.
- Two-level cluster BB 334.
- Size-first rules ≤ 360.
- Evidence-chosen prior (always Bern(0.2)).
- Moment-tilted non-local slab 351/360.
- Dilution prior 364 (neutral).
- g-path / hyper-g (theory).
- BayesBag (deferred).
