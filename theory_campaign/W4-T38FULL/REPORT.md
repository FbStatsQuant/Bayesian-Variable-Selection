# W4-T38FULL: REPORT. The main theorem T38, assembled and paper-ready

Run of 2026-11-02, branch `theory/W4-T38FULL`, from `theory/campaign` at 894a529.

**Deliverables:**
- `T38_STATEMENT.md`: the paper statement, the dependency map, the method-change list, and what holds without LS0;
- `T38_PROOF.md`: the full proof;
- `scripts/lh_ls0_check.py` and its output `.txt`, with a fixed seed.

Everything here is a **candidate**: not reviewed and not adopted. "VERIFIED" means that one adversarial verifier of the same model family checked the result. That is not cross-family review.

## 1. Headline

1. **T38 composition: PROVED, in a stronger form than the liminf.** For every n, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + P(𝒪̄, S₀ ∉ 𝒮̄⁺), on the potential uninterrupted run R̄ and never conditioning on completion. So once a discovery route works, P(output and Ŝ⁺ = S₀) = P(output) − o(1). This implies liminf P(𝒪, Ŝ⁺ = S₀) ≥ 1 − limsup P(U).
2. **(a) Favourable regime: PROVED-UNDER (F).** EXP′ is now a theorem, so the remaining inputs are the locked T22(iii) design conditions, or the checkable BO or zero-leakage versions, together with T11(iii). It holds with no open statistical input on the orthogonal family ORTH (p < n).
3. **(b1) Masked regime with LS0: PROVED-UNDER three deterministic design conditions.** These are ELIG(S°), POP-LAT(S°) and λ_min(R_{S°∪S₀}) > 0.
   - It is **PROVED with no open statistical input on an explicit masked family**: the linked-hub family LH, exact Gram, p < n, any fixed c. That family is masked: π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}, and the final run's iid draws miss S₀ with probability → 1.
   - The new ingredients are Lemma LS-score, Lemma M and Proposition LH-LAT. They are PROVED here but unreviewed.
   - The p ≫ n analogue (LH-iid) was claimed as PROVED by W3-PXN *during* this run. That claim is unverified.
4. **(b1′) D2 (no method change): PROVED as a conditional theorem**, with W3-VT38E's repair (r* = (11+2√10)/9 and the weaker event NB′). Its statistical instance on a masked family is a **PROOF SKETCH** (LH with c = 1; the NB step is unfinished).
5. **(b2) Gibbs path (no method change): PROVED-UNDER DELIV and REP.** DELIV (SHARE or LT) stays **OPEN**, and COUNTEREXAMPLE C1 shows that it is a genuine particle-level property. (c) Cost is PROVED-UNDER T32(i), which is a CONJECTURE.
6. **Without LS0, the paper has no masked-regime consistency theorem whose premises are all proved on an explicit family.** LS0 is the method-change dependency. It must emit its centre as a score event.

## 2. Statements

The full text is in `T38_STATEMENT.md` Part I. In brief:

**Theorem 5 (T38).**
- **Standing assumptions:** EX-A, EX-S, CAL (idealisations); SR and GUARD (implementation facts); (P), meaning δ₁ → 0 by locked T03 or T03♯; regime R1 with the v3 budgets.
- **(0)** P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n, where D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}). If D_n → 0, then P(𝒪, Ŝ⁺ ≠ S₀) → 0, and liminf P(𝒪, Ŝ⁺ = S₀) ≥ 1 − limsup P(U).
- **(a)** D_n → 0 under (F): 1 − π₀(S₀) → 0. Sufficient conditions:
  - (F1): G, R, SE-blk, VIS, NL_η, NL_avg(κ);
  - (F2): G, R, SE-blk, BO, BM-blk;
  - (F3): ZL(S₀), SPREAD, VIS-lin(S₀).
- **(b1)** D_n → 0 under four conditions:
  - (M1) P₀(π₀(S°) > ½) → 1 for a deterministic S° with Φ(S°) bounded;
  - (M2) POP-LAT(S°, m_n): along Lat(S°) ∩ {Φ ≥ 2}, some progress neighbour beats every non-progress neighbour, and the state itself, by at least m_n ≫ √(log n/n) in Δ;
  - (M3) λ_min(R_{S°∪S₀}) ≥ φ₀² and ‖μ‖²/n ≤ M;
  - OP-LS0.
- **(b1-LH)** On LH in exact Gram (p ≤ n − 1, 0 < |ψ_i| < ρ, g ≤ B < 2g, fixed coefficients):
  - (P), (M1), (M2) with a fixed margin m₀ > 0, and (M3) all hold;
  - Q_f π₀(S₀) → 0 when c ≥ 2 and p → ∞, or when c = 1 and p/(√n log²n) → ∞.
- **(b1′)** D_n → 0 under D2's hypotheses: π₀(S₀ ⊕ j) ≥ b > 1/10; Dep ≤ 1 − c₁ off a bounded set; P(NB′ᶜ) → 0.
- **(b2)** D_n → 0 under DELIV (an eligible particle at terminal start) and REP (sup over 𝔛_n of β_{L+5} → 0), with H′ = L + 5.
- **(c)** The number of scores is ≤ T32(i)'s ceiling + (ℓ+1)max_k[p + k(p−k)], which is O((n+p)(p+B)log²n + p²log²n).

**New results proved here** (`T38_PROOF.md` §3):
- **Lemma LS-score.** Suppose D_S holds on Lat(C₀) ∩ {Φ ≥ 2}, ℓ ≥ Φ(C₀) − 1, and C₀ ≠ S₀ or the centre is emitted. Then the production search from C₀ scores S₀.
- **Lemma M.** On an event of probability → 1, F(A) > F(B) for every pair with |A|, |B| ≤ k, λ_min(R_A) ≥ φ₀² and Δ(B) − Δ(A) ≥ m_n ≥ M_n√(log n/n).
- **Theorem b1:** (M1)–(M3) + OP-LS0 ⇒ D_n → 0.
- **Proposition LH-LAT.** POP-LAT holds on LH with m₀ = min{(1−κ_max)R_min, R_min, min β_i²(1−ψ_i²)², min θ_h²}, where R_i = β_i²ψ_i²(1−ψ_i²) and κ_i = ρ_{b_i}²(1−ψ_i²)/(1−ψ_i²ρ_{b_i}²).

## 3. Proofs

All proofs are in `T38_PROOF.md`. Source proofs are cited by label; the repairs are tabulated in its §8. The structure:
- **§1, composition.** Lemma RO, strict maximality of S₀ when π(S₀) > ½, then Markov and bounded convergence.
- **§2, part (a).** Locked T11(iii) on R̄ gives D_n ≤ P(s₀ > K) + E₀[1 − π₀(S₀)]. (F1)–(F3) come from W1-EXP Thm 1, Thm 2 and Thm 6 with locked T22(iii). ORTH is a new composition, checked line by line here.
- **§3, part (b1).**
  - Lemma LS-score uses lattice closure of progress moves (W1-T37R Lemma 2(a)) and the scan-before-limit rule of the engine.
  - Lemma M combines deterministic prior, determinant and Q-versus-RSS bounds (W1-T38E E1) with a uniform χ²/Gaussian event over all sets of size ≤ k + s₀, and an RSS floor through span(A ∪ S₀).
  - Proposition LH-LAT uses unit additivity of Δ (LH's Σ is block-diagonal over pair, visible and null units), closed-form unit residuals, and an exhaustive case list of neighbours.
  - **This is the crux of the run.** It replaces the open TD′ black box of W1-T38E by a checkable population condition, and verifies that condition on an explicit masked family.
- **§4, part (b1′).** W1-T38E D2, with step 2 replaced by W3-VT38E §3.1. The LH c = 1 instance is a sketch.
- **§5, part (b2).** IND-T plus Theorem B′ give a product bound conditional on 𝔉_T. Lemma F′, B1′/B2′ and H′ = L + 5 are incorporated.
- **§6, part (c).** T32(i) plus the LS0 term.

## 4. Evidence

**`scripts/lh_ls0_check.py`** (seed 20261102). LH in exact Gram: G = 12, g = 9 (p = 108), ρ = 0.7, ψ = 0.5, c ∈ {1, 2, 3}, n ∈ {200, 800, 3200}, 10 replicates per cell. It computes the exact π₀ mode, π₀(S°) by convolution, the production local search, D_S at every lattice state, and the margins.
- S̃₀ = S° in **90/90** runs.
- LS0 scores S₀ in **90/90**, in exactly c moves for n ≥ 800.
- The minimal lattice margin grows roughly linearly in n: 11 → 58 → 266 nats (c = 1) and 30 → 135 nats (c = 3). This is the Θ(n) margin of Lemma M.
- At n = 200, D_S failed at one state in one replicate of each of c = 2 and c = 3. LS0 still scored S₀ there.
- The full table is in `T38_PROOF.md` §3.5.

**Reproduced or cited evidence from the sources:**
- C1 extinction: 0.56 at N = 10⁵ and 1.00 at N = 10⁶, with a reversible kernel (W3-VT38E).
- D2's full bound in CF(1): 2.2·10⁻⁷ / 1.6·10⁻⁵. Those instances are not masked.
- W3-VT37R's 720-design exhaustive check of Theorem A.
- EXP′ reproduced (W3-VEXP).
- W3-PXN's interim LS0-on-study data: S₀ scored in 48/49 fits, S1/S3, n = 200. Unverified.

**Study relevance (n = 200).**
- The start is dilution-masked (W3-VEXP Prop. D; W3-PXN Prop. W).
- The misses are posterior misses (THEORY_PRIORITIES §5).
- The T03 proof thresholds start near n ≈ 2×10⁶ (W2-VT03R R1).
- So T38 explains the mechanism, not the n = 200 numbers.

## 5. What fails, and why

- **Using TD′ as a black box at the single centre S̃₀** (W1-T38E (b1)). It is correct, but nearly a restatement (W3-VT38E §5.1). It is replaced here by POP-LAT plus Lemma M, which turns the input into a population margin and makes it checkable.
- **W1-T37R Thm A(A3) as the repair input.** It asks for the local maximum (L), D_S at Φ = 1 states, and ℓ ≥ τ, because it targets certification. T38 needs scoring only, so those requirements are dropped (Lemma LS-score). Theorem C (PGD + LD*) remains a PROOF SKETCH, and PGD is false in general (C3). It is kept only as the alternative for data-dependent centres.
- **Literal TD(d,0)** is false for d ≥ 1 on {π(S₀) > ½} (W1-T37R Prop 1; W3-VT38E V1). It is not used anywhere.
- **Eligibility of the best-scored model without LS0.** E1: the natural sufficient condition fails with probability → 1 under omission masking. Lemma 0 / R2: the final search can deliver S₀ only on E_LS. This stays OPEN, and is the reason LS0 is needed.
- **(b2) from start mass + bridge mass + exit control.** False by C1. SHARE is nearly its own conclusion. LT fails exactly in the masked case.
- **The H24-based route (e).** Its asymptotic input fails (CE1, Lemma E). It is retired, and T38 uses Theorem B′ only inside (b2).
- **The brief's limit form and cost formula** were both malformed; corrected (W1-T38E).
- **Joint-family requirement (Astra).** The CF family of W1-T38E is verified only at n ∈ {400, 1600}. LH exact Gram is now a fully proved joint family for (b1). For (b1′) and (b2), no joint family has every premise proved.

## 6. Needs escalation

1. **An independent (cross-family) check of the three new results:** Lemma M, Lemma LS-score and Proposition LH-LAT. These carry the only fully proved masked-regime instance. They are short: about two pages, deterministic plus one uniform χ² event. A same-family background check was run during this session; its verdict is in §6a.
2. **HQ / Felipe: adopt LS0 or not.** It is the single method-change dependency of the main masked-regime result. Requirements:
   - call `local_search(…, emit_centre = true)`;
   - break ties in argmax π₀ by the HPM rule;
   - label LS0-augmented fits;
   - it falls under the investment rule (pilot evidence that performance is kept).
3. **Verify W3-PXN.** It claims the p ≫ n LH-iid family and D2 for c = 1. If it is verified, (b1) holds on a p ≫ n family, which is the paper-relevant case.
4. **GUARD code check** (W2-BOOK); **SR confirmation** (Felipe).
5. **T32(i)**: write a proof, or downgrade (c) to a remark.

## 6a. Same-family check of the new results (this run)

*Filled in below after the background referee returned.*

## 7. Outside scope

- At study size, LS0 cannot fix posterior misses, and S4/S6 start modes are often 12–14 moves away, beyond ℓ = 10–11 (W3-PXN interim). The paper should not suggest that LS0 changes the n = 200 results.
- **Proposition LH-LAT gives an exact formula for the masked-regime margin:** (1−κ)R = β²ψ²(1−ψ²)(1−ρ_b²)/(1−ψ²ρ_b²). It quantifies T37's "Why" (truth versus look-alike capture share) on a concrete family. It could replace T37's informal (n−1)θ²(1−r²)/(2σ²) in the paper text.
- W2-PREM found a COUNTEREXAMPLE to W1-T24G's repair family on LH (Theorem B♯ replaces it). Anything citing Theorem B on LH should cite B♯.

## 8. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| T38(0) composition | P(𝒪, Ŝ⁺≠S₀) ≤ 2E₀δ₁ + D_n; o(1) form ⇒ liminf form | 0.98 | done | GUARD as a fact; δ₁ → 0 (locked T03) | no |
| T38(a) | D_n → 0 under (F1)/(F2)/(F3); ORTH joint family | 0.95 | done (composition); relevance needs n ≳ 10³ | VIS/NL in non-orthogonal designs; in-sample partition decoupling | no |
| T38(b1) general | (M1)–(M3) + LS0 ⇒ D_n → 0 | 0.93 | done (new, unreviewed) | Lemma M's uniform event; scan-before-limit engine fact | **yes, LS0** |
| T38(b1-LH), p < n | all premises proved on LH exact Gram | 0.9 | done (new, unreviewed) | the case list in Prop. LH-LAT; Thm 5(a) | **yes, LS0** |
| T38(b1) on p ≫ n (LH-iid) | as W3-PXN claims | 0.8 | 0.7 (needs verification) | in-sample margins, exact Beta laws | **yes, LS0** |
| T38(b1′) D2 | conditional theorem (VERIFIED); LH c = 1 instance | 0.9 / 0.75 | done / 0.6 | NB′ (uniform d over non-S° pilot draws) | no |
| T38(b2) | DELIV + REP ⇒ D_n → 0 | 0.95 as an implication; 0.5 that DELIV holds in BVS designs | 0.15 (DELIV) | selection vs within-region moves (C1) | no |
| T38(c) cost | T32(i) + LS0 term, polynomial | 0.95 | 0.7 (T32(i) is bookkeeping) | an engine audit of score counts | no |
| "T38 explains n = 200" | — | 0.1 | — | dilution masking, posterior misses, T03 thresholds 10⁶ | — |

## 9. What remains open, ranked by importance for the paper

1. **Cross-family review of the new (b1) pieces** (Lemma M, LS-score, LH-LAT) and of W3-PXN. Without it, the main masked-regime theorem rests on unreviewed proofs. This is cheap.
2. **The LS0 decision and validation** (method change, investment rule). Every fully proved masked-regime statement depends on it.
3. **A p ≫ n masked joint family** (W3-PXN's claim, unverified). The study design is p ≫ n, so a p < n-only theorem is weaker for the paper.
4. **A no-method-change masked theorem:** finish NB for D2 on LH with c = 1 (two independent sketches share the same crux). Beyond Gibbs distance 1 this is OPEN, and it is the delivery problem.
5. **DELIV (SHARE/LT) for (b2)** (OPEN; C1). This is the only remaining route for c ≥ 2 without LS0. W4-SHARE had only a plan when this run ended.
6. **Eligibility of the best-scored model without LS0** (OPEN; E1 is negative).
7. **REP premises outside LH**: phase-1 conditions under cancellation; NL0 under dense correlation, where a COUNTEREXAMPLE exists.
8. **T32(i)** (the cost corollary) and the **GUARD** code check.
9. **In-sample favourable regime for iid S1/S3/S4/S6** (a partition–noise decoupling GAP). This affects only the relevance of (a).
10. **Finite-n relevance at n = 200.** This is not provable with this technique, and must be disclosed (dilution masking; posterior misses; thresholds near 10⁶).
