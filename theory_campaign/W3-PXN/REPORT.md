# W3-PXN — REPORT: a p ≫ n family that carries all of T38(b)'s premises jointly

Run of 2026-11-02, branch `theory/W3-PXN`. Proofs: `PROOF.md`. Scripts: `scripts/` (fixed seeds in each file). Raw
results: `results/*.jsonl`. Tables: `results/summary.txt`, `results/check_*.txt`. Every result is a **candidate pending
cross-family review**. Status words never upgraded.

## 1. Headline

1. **PROVED (candidate), one p ≫ n family that carries every premise jointly.** The family is LH-iid. Its rows are iid
   Gaussian with W1-EXP's linked-hub correlation: equicorrelated groups of size g, with 9 ≤ g ≤ 16 so that g ≤ B < 2g. c
   linked pairs carry a suppressor coefficient, some groups are visible and the rest are null. The dimension satisfies
   n^a ≤ p ≤ n^A, so p ≫ n is allowed. On the actual X-dependent partition, with probability → 1, the family satisfies:
   - blocks = groups;
   - G, R, the locked SE, SE-blk and W1-T03R's anchored SE;
   - BM-∞;
   - near-truth start mass 1 − π₀(S°) = O_P(√(log n/n));
   - T27 masking with an exact limit law, log π₀(S₀) + c log p + (c/2)log n →_d Σ log((s+i)/2) + ½χ²_c;
   - S̃₀ = S°;
   - the TD′ lattice condition of W1-T37R Thm A at S̃₀, so LS0 scores and certifies S₀ in c moves;
   - π(S₀) → 1.

   T38(b) (W1-T38E composition) therefore holds on this family through route (b1), the LS0 tweak, for every fixed c.
2. **The no-tweak route works for one masked variable.** For c = 1 the original method scores S₀ in the first pilot round
   (route D2). The hypotheses D2-a, D2-b and D2-c, including Dep = O_P(√(log n/n)), are PROVED; D2-d (NB) is a PROOF
   SKETCH. For c ≥ 2 the no-tweak route stays OPEN, because it needs delivery (b2).
3. **The partition limits masking (PROOF SKETCH).** When a linked unit fits in half a block (2g ≤ B, e.g. the study's
   groups of 5), complete linkage puts the cancelling variables in one block and the masking disappears. Cancellation
   masking therefore survives the method's own partition only for units larger than B/2.
4. **The study's n = 200 masking is not the masking of T27/LH.** It is *dilution masking*: the start's block view treats
   the other 13 truths' signal as noise (v_T ≈ 7–26σ²). The masked truths have L² = δ²/σ² ≈ 50–200, not O(1). The
   CL(L) rate overshoots log₁₀π₀(S₀) by 20–30, and the effect is scale-free and gone by n ≈ 1600. W1-EXP's "weak-signal
   masking" is right only in the block-SNR sense, and its "bounded L" version is rejected (numerics, §5). Under the frozen
   setting (s₀ fixed, BM-∞) dilution vanishes, so **no fixed-s₀ BM-∞ theorem describes the n = 200 numbers**
   (Proposition W, PROOF SKETCH).

## 2. Statements (full proofs in PROOF.md; section numbers refer there)

**Family LH-iid (PROOF §0).** The fixed parameters are:
- g, c ≥ 1, v ≥ 0, and ρ ∈ (0,1);
- 0 < |ψ_i| < ρ, and nonzero β_i, β^vis_h;
- σ² > 0, and 1 ≤ a ≤ A.

The design has p = Gg with n^a ≤ p ≤ n^A, and g ≤ B_n < 2g eventually, i.e. 9 ≤ g ≤ 16. Rows are iid N(0, Σ_LH) and
ε ~ N(0, σ²I) is independent of the rows. The truth is θ_{j_a} = β, θ_{j_b} = −ψβ and θ_{j_h} = β^vis_h. Write
S° = S₀∖M with M the masked hubs, s = |S°| = c + v, and s₀ = s + c. Regime R1, with s₀ fixed.

| # | Statement | Hypotheses beyond LH-iid | Status |
|---|---|---|---|
| P1 | The v3 partition equals the groups w.p. → 1 | Gaussian correlation concentration (cited, Lemma C1) | PROVED |
| P2 | G; R; locked SE at size m_n + s₀; SE-blk; SE_λ(j₀), SE_w(m♯; g₀); BM-∞, all w.p. → 1 | C1 | PROVED |
| B | Exact Beta laws: X_{h,V} ~ Beta(\|V\|/2, (n−1−\|U°\|−\|V\|)/2); neutral x_{A,l} ~ Beta(½, ·); masked hubs independent of y | — | PROVED |
| P3 | q = O_P(√(log n/n)), e = O_P(p√n e^{−c₆n}), so **1 − π₀(S°) = O_P(√(log n/n))** and b_n := π₀(𝓡_d) ≥ π₀(S°) → 1 | W1-EXP Thm 1 (EXP′), locked T22(i) | PROVED |
| P4 | **Mstat_n →_d Σ_{i≤c}log((s+i)/2) + ½χ²_c**; hence π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}, and T27's H1–H3 hold with CL(L), L = O_P(1) | locked T22(ii-a), P3 | PROVED |
| P5 | S̃₀ = S° w.p. → 1 (eligibility for LS0) | P3 | PROVED |
| P6 | TD′ lattice condition at S°: (L) and D_S for all S ∈ Lat(S°)∖S₀ w.p. → 1, so LS0 returns S₀ certified in c ≤ ℓ_n moves | W1-EXP Lemmas 1.1, 1.2, 1.4 (general-set form), W1-T37R Thm A(A3) | PROVED |
| P7 | D2 with x° = S°, 𝒟 = C_b∖j_b, b = ½ (c = 1): D2-a, b, c PROVED (Dep = O_P(√(log n/n))); D2-d (NB) PROOF SKETCH; so P(S₀ ∉ 𝒮_cal) → 0 | EX-A, EX-S, SR, W1-T38E D2 | PROVED / PROOF SKETCH |
| P8 | 1 − π(S₀) = O_P(√(log n/n)) | locked T03, plus a design de-randomisation lemma (PROVED) | PROVED |
| Cor | liminf P(Uᶜ, Ŝ⁺ = S₀) ≥ 1 − limsup P(U): via LS0 for all c; via the original method for c = 1 | the above, plus W1-T38E T38(b)-R | PROVED (b1); PROVED modulo NB sketch (b1′) |
| Q | If 2g ≤ B, linked pairs are co-blocked and LH masking disappears | — | PROOF SKETCH |
| W | Dilution: LO₀(j) = −log((2p−s₀)/s₀) − ½log(n+1) + (n/2)θ_j²Var(x_j\|X_T)/v_T(1+o_P(1)); under s₀ fixed + BM-∞ every block-orthogonal family is favourable | block-orthogonal population | PROOF SKETCH |
| W′ | A fixed-s₀ dilution family (local alternatives in the window (1+2A) < κ < (1+2A)v_T/σ²) has π₀(S₀) → 0 with LO₁ → ∞ | — | CONJECTURE (π(S₀) → 1 needs a sharp-constant T03) |

**The key new argument (P3).** In LH-iid every quantity the start law needs at the reference S° has an *exact* Beta law
that is independent of the response. This holds for null, neutral and masked-group subsets alike (Lemma B), because of
the population identities Cov(X_V, μ | X_{U°}) = 0. EXP′ turns each block ratio into
(n+1)^{−j/2}e^{O(1)}(1 − X)^{−ν}. The truncated moment E[(1−X)^{−ν}1{X ≤ τ}] ≤ 2^{e₁}(mτ/2)^{j/2}/Γ(j/2+1)
(Lemma Tr) then bounds every a_bj. Truncation is essential, since E(1−X)^{−ν} = ∞. Jensen applied to (j!a_bj)^{1/j}
gives E[q1_𝒢] = O(√(log n/n)), and locked T22(i) concludes. No NL_η, VIS-lin or exact-zero-leakage hypothesis is
needed. This closes W1-EXP's §4.3 PROOF SKETCH, and it does so at p ≫ n with a better rate.

## 3. Proofs or sketches

All are in `PROOF.md` §§0–14. The cruxes:
- P3: Lemma B (independence through F1–F3) and Lemma Tr.
- P6: the component decomposition of the population residual λ (Lemma Λ) and the margin table in §9.3. Every
  non-progress neighbour of a lattice state exceeds the best progress move by a fixed amount c₂ > 0. The (L) part at S₀
  uses max_l Z_l² ≤ 2log p + 2log log n against −½log n − log 2p.
- P7 (NB): three bad sets of initial draws, each with H₀·π₀ → 0, and d varying by only O(log n) on the good set,
  against a threshold of order log²n.

## 4. Evidence: LH-iid (exact start law by convolution; `scripts/lh_iid.py`)

The configurations are as follows.
- **A:** c = 1. One linked pair (β = 1, ψ = 0.5) and one visible group (β = 1); ρ = 0.7 (S3-like), g = 10.
- **B:** c = 2. Pairs with β = ±1, plus one visible group.
- **P:** config A at n = 200 with p ∈ {500, 1000, 2000, 4000}.

p ≈ n^{1.25} in A and B. Everything is computed exactly:
- the full v3 partition (scipy complete linkage + R13 left-child rule + top-down cut + next-fit; when p > 4300 the
  sufficient margin condition of Lemma P1 is checked instead);
- all block tables, π₀ by convolution, π₀(𝓡_d) by bivariate convolution, and the start mode by max-plus convolution;
- iid π₀ draws by the backward sampler, and the production local search from S̃₀;
- D2's Dep, and NB over the H₀ draws.

The library is checked against brute-force enumeration in `results/sanity.txt` (agreement to 1e-15).

TABLE_LH

Checks (`results/check_lemmas.txt`, `results/check_mstat.txt`):
- **Lemma B:** KS tests of six exact Beta laws (a-group neutral, visible neutral and null additions given S°;
  |V| = 2 block statistics in a null group and in the masked group; the masked hub). All p-values are in [0.17, 0.62]
  (400 reps each).
- **Theorem P4:** T_n = Mstat − log π₀(S°) − prior term matches its exact finite-n law in every configuration (PIT KS
  p = 0.93 for A, 0.34 for B, 0.93 for P). The slow approach of Mstat to its limit comes *only* from log π₀(S°).
- **Theorem P6 margins:** an exhaustive population check over 81 parameter settings (c ∈ {1,2,3}, ρ ∈ {.4,.7,.85},
  ψ up to ρ − .05, β ∈ {.5,1,2}). The smallest D_S margin is 0.0027 > 0 and the smallest (L) margin is 0.0027 > 0.

## 5. Evidence: the study design at n = 200 (`scripts/study_n200.py`, `study_ls0.py`)

The generator is `gen_dev_data.R` re-implemented in numpy, so the data are distributionally equal but not bitwise equal:
- n = 200; s₀ = 14, one truth per group of 5;
- β pattern (1.4, −1.0, 1.8, −1.2, 0.8, −1.6) × scale ∈ {1, 0.5};
- scenarios S1, S3, S4, S6; p ∈ {500, 1000}; 10 replicates per cell;
- actual v3 partition (B = 14), exact π₀.

For each truth j the script computes:
- the exact start keep-odds LO₀(j) = log π₀(S₀) − log π₀(S₀ − j) and posterior keep-odds LO₁(j) = F(S₀) − F(S₀ − j);
- the block statistic V₀ = −ν log(1 − x^blk);
- its population (dilution) prediction V₀pop = δ²_pop/(2v_T) + ½.

TABLE_STUDY

**Answer to the task's question.** The study's masking (median π₀(S₀) ≈ 10⁻¹²–10⁻¹⁸) is weak-signal masking only in the
block-SNR sense, which here is dilution. It is not consistent with W1-EXP's specific mechanism ("CL(L) with bounded L,
T27's law with c = number of weak truths"). The evidence:
- **Signal leaks strongly into the blocks.** The masked truths have L² = δ²_pop/σ² ≈ 50 (scale 0.5) to 199 (scale 1),
  not O(1). The CL(0) prediction −#missing·log₁₀(p√n) ≈ −29 to −46 overshoots the observed
  log₁₀π₀(S₀) − log₁₀π₀(S̃₀) ≈ −11 to −17 by 20–30 orders of magnitude.
- **The dilution prediction fits.** Masked truths have V₀ ≈ 3.2–4.4 against a threshold τ = log((2p−s₀)/s₀) + ½log(n+1)
  ≈ 7.0–7.6. The posterior sees V₁ ≈ 23–78, and 96–100% of the start-masked truths have LO₁ > 0. corr(V₀, V₀pop) is 0.69
  at n = 200 and 0.95 in the n-sweep. The predicted number of masked truths (7.0–10.0 per fit) matches the observed
  6.3–9.0, with 71–82% per-truth agreement at n = 200.
- **It is scale-free.** V₀ of the masked truths is the same at scale 0.5 and 1 (v_T = 7.2 vs 25.6 cancels the 4× signal),
  as Proposition W predicts. Stronger signals do not remove it at n = 200.
- **It is a finite-n effect.** In the n-sweep at p = 1000, scale 0.5, the mean number of start-masked truths falls
  8.4 → 4.2 → 1.4 → 0.1 (S1) and 8.2 → 4.4 → 1.8 → 0.0 (S3) for n = 200, 400, 800, 1600; median log₁₀π₀(S₀) goes
  −17.4 → −7.6 → −1.9 → −0.3. This is the favourable regime asymptotically, as Proposition W says for fixed s₀ + BM-∞.
- **Partition co-blocking is the other half.** The study's groups of 5 fit in a block (B = 14), so by Proposition Q
  LH-type cancellation could not survive the partition even if it were planted. S1/S3/S4/S6 have none at population
  level anyway (W1-EXP).

**LS0 on the study data** (`study_ls0.py`; HQ-relevant input for the LS0 tweak, outside the strict scope):

TABLE_LS0

Reading: LS0 scores S₀ from the start mode whenever |S̃₀ Δ S₀| ≤ ℓ + 1 and the greedy path is monotone, which is the
typical case in S1/S3. In S4 (ρ = 0.85) and S6 at scale 0.5 the start mode is often 12–14 moves away, beyond ℓ = 10–11.
There LS0 fails or ends at a better-scoring wrong model, which would be a posterior miss and not a search miss. Dilution
masking with c ≈ s₀/2–3s₀/4 masked truths is exactly the case where the fixed-c theory says nothing about ℓ.

## 6. What fails and why

- **D2 for c ≥ 2.** D2 needs Gibbs distance 1 from a start-heavy state. At distance ≥ 2 the intermediate addition has
  start odds ≈ n^{−1/2}/p, so a crossing temperature must be reached first. That is the (b2) delivery problem (SHARE,
  W1-T38E C1). The original method's masked-regime theorem on LH-iid is therefore OPEN for c ≥ 2. With LS0 it is PROVED.
- **The study's group size is outside the family.** g = 5 ≤ B/2 is outside LH-iid (Proposition Q); the family needs
  9 ≤ g ≤ 16. A study-like p ≫ n *masked* family with g = 5 would have to use cancellation between units larger than a
  block, or non-clustering weak links. Neither is constructed.
- **LH-iid at n = 200 is near the edge.** In config A at n = 200, F(S₀) − F(S°) < 0 in 3/20 replicates (the masked
  coefficient −ψβ = −0.5 is weak), and Mstat has a heavy lower tail because π₀(S°) is only 0.70 in median. The theorems
  are asymptotic. Their margins are positive but small at the study size.
- **The dilution regime has no fixed-s₀ BM-∞ theorem.** It vanishes asymptotically (Proposition W). A theory for it
  needs either s₀ ≍ n/log n (outside the frozen setting) or local alternatives with a sharp-constant selection theorem
  (T03♯'s c₀ = L* is far too large). It is recorded as CONJECTURE W′, not pursued.
- **W1-EXP's random-design remark "NL_η fails, truncation essential".** Confirmed. Lemma Tr's truncation at
  τ_n = 4(A+3)log n/n is the device, and E(1−X)^{−ν} = ∞ for every Beta statistic here.
- **The rate.** √(n/log n)·(1 − π₀(S°)) stays in 1.5–2.6 across n ∈ [200, 1600]. The √log n factor of P3 looks
  genuine: it comes from the max of p chi-squares. W1-EXP's exact-Gram realisation has n^{−1/2} because it has no null
  sample correlations.

## 7. Needs escalation

1. **Independent check of Lemma B and Theorem P3.** These are the new load-bearing arguments: conditional-independence
   identities F1–F3; the Grassmannian/Beta step after standardisation; the truncated moment; Jensen on (j!a)^{1/j}. A
   cross-family reviewer should redo them.
2. **W1-EXP Lemmas 1.1, 1.2, 1.4 at full generality.** PROOF §9.1 uses them for arbitrary sets of size ≤ s₀ + 2 rather
   than within-block sets. I checked that the proofs never use block membership; the reviewer should confirm.
3. **P7 (D2-d, NB) bookkeeping.** The π₀(S ⊉ S°) peeling bound and the uniform d-range bound are sketched. They are low
   risk, but they are the only non-PROVED step of route (b1′).
4. **HQ decision.** T38(b) can now be stated on an explicit p ≫ n family (LH-iid). The paper must **not** present it as
   the explanation of the n = 200 masking, which is dilution (a different, finite-n mechanism). Suggested wording: "the
   masked regime of Thm 5 is realised by cross-block cancellation; at the study size the start is masked by dilution,
   which disappears asymptotically and which LS0 repairs when |S̃₀ Δ S₀| ≤ ℓ + 1".
5. **Felipe / method.** The LS0 numbers at n = 200 suggest that ℓ (10–11) binds in S4/S6. If LS0 is adopted, consider
   letting the LS0 search run to certification. This is a cost change of a few scans, and it would need its own
   validation under the investment rule.

## 8. Outside scope (recorded, not pursued)

- **Correction to W1-EXP.** Its claim that under weak-signal masking "π(S₀) is also small, unlike LH" is not supported
  locally: 96–100% of start-masked truths have LO₁ > 0. Whether the study's posterior misses (565/2394) come from
  elsewhere (supersets at c = 1, swaps at c = 0.5) is the statistical-half question.
- **Start mass on 𝓡₂ at n = 200.** π₀(𝓡₂) is 0.7–0.96 in S1/S3/S6 but only 0.1–0.3 in S4 (ρ = 0.85). The study's
  "median π₀(𝓡₂) ≈ 0.8" hides a scenario split.
- **Sharpened T22(iii).** Theorem P3's method (exact Beta laws plus truncation) should give T22(iii) in the
  *favourable* regime for iid S1/S3/S4/S6 designs with the actual partition, rate √(log n/n) (W1-EXP card "T22(iii) iid
  designs", 0.8/0.6). The only changes are U_h° = S₀ ∩ C_h and the visible-group computation. Not written.

## 9. Confidence cards

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| Joint p ≫ n family (task goal) | LH-iid carries G, R, SE (all variants), BM-∞, P3, P4, P5, P6, P8 jointly on the actual partition | 0.93 | done (PROVED, candidate) | Lemma B + Lemma Tr (P3); margin table (P6) | No (LS0 for the eligibility route) |
| Near-truth start mass b_n (T22(i) on LH-iid) | 1 − π₀(S°) = O_P(√(log n/n)) | 0.95 | done | exact Beta laws + truncation | No |
| T27 masking at the CL(L) rate | Mstat →_d Σlog((s+i)/2) + ½χ²_c | 0.97 | done | — | No |
| Eligibility (LS0) | S̃₀ = S° w.p. → 1 | 0.97 | done | — | Yes, minor (LS0) |
| Repair input TD′ (W1-T37R Thm A) | lattice condition at S° | 0.93 | done | population margins c₂ > 0 | No |
| D2 (no tweak), c = 1 | S₀ ∈ 𝒮_cal w.p. → 1 | 0.88 | 0.85 (NB bookkeeping left) | NB: H₀π₀(bad) → 0 | No (needs SR) |
| No-tweak route, c ≥ 2 | Ŝ = S₀ w.p. → 1 − P(U) without LS0 | 0.6 | 0.15 | delivery/SHARE (W1-T38E C1) | No, but unproved |
| π(S₀) → 1 on LH-iid | 1 − π(S₀) = O_P(√(log n/n)) | 0.97 | done (via locked T03) | de-randomisation lemma | No |
| Co-blocking (Prop. Q) | 2g ≤ B ⇒ linked pair co-blocked, no masking | 0.9 | 0.85 | merge-order argument | No |
| Dilution explains n = 200 masking (Prop. W) | start-masked ⇔ nθ²Var/(2v_T) < τ; vanishes for fixed s₀ + BM-∞ | 0.9 (mechanism); 0.85 (asymptotic statement) | 0.7 | uniform x_{T,j} → population with v_T | No |
| Fixed-s₀ dilution family with π(S₀) → 1 (W′) | local alternatives in the window | 0.7 | 0.3 | sharp-constant T03 | No |
