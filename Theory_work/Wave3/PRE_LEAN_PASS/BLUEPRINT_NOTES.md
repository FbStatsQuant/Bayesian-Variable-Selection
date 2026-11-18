# PRE-LEAN PASS: Lean-readiness notes (copied from the Fable cards; input to the Lean Department's blueprint)

## T1: Thm 3(a), `W3-PSHARP:B` (card `T1/FABLE_CARD.md`)
Level-2 named axioms: none (Level 1). B2, B3 and the "in probability" clause of B1 stay out of Lean scope. No item changes the statement.
1. **Three-layer split with an abstract core.** (L1) Finite Ω, scores σ > 0, distinct S_J ≠ S₀ with σ(S_J)/σ(S₀) ≥ ρ_J imply odds ≥ Σρ_J. (L2) Combinatorics. (L3) Linear algebra, entering L1 as the two hypotheses D_{S∪{j}} ≤ n·D_S and 0 ≤ Q_{S∪{j}} ≤ Q_S. Thm 3(a) then compiles before any matrix work; L1 is the shared score base for T2.
2. **Critical scale in ε-form with explicit sequences:** for every ε > 0, eventually π(S₀) ≤ e^{−λ/2} + ε, via the finite-J route (T1-2). Avoids liminf/limsup side-conditions; the ℝ≥0∞ variant is declined.
3. **S(1) by one completed square instead of simultaneous diagonalisation:** (n+1)A = H + nI, w = A⁻¹g, α = gᵀw, v = w/(n+1); then gᵀH⁻¹g ≥ 2gᵀv − vᵀHv ≥ α/(n+1), so (n+1)²gᵀH⁻¹g ≥ nα. Needs only `PosDef`. A 3-line PATCH or Lean-only.
4. **Q-monotonicity from Lemma V alone,** by zero-padding: Q_{S⁺} ≤ f_{S⁺}((ϑ̂_S, 0)) = Q_S. Drops block inversion from T1's Lean dependencies. Lean-only.
5. **Arithmetic hygiene:** write n^{−j/2} as (1/√n)^j (no `rpow`); products as `Nat.descFactorial` cast to ℝ; use `Nat.descFactorial_eq_factorial_mul_choose`, `Finset.card_powersetCard`, `Matrix.det_fromBlocks₂₂`, `PosDef.fromBlocks₂₂` (all in the BNP Mathlib checkout).
6. Implicit step to make explicit in Lean (no text change): π(S₀) > 0 (stated in the proof of S(4), not in B).

## T2: SL0 + LT-d pooling, `C-PACK:SL0`, `W3-SAMP:LT#` clause LT-d (card `T2/FABLE_CARD.md`)
Level-2 named axioms: none for items 1–4 (Level 1). No item changes a paper statement.
1. **One master lemma for SL0.** For a probability π on a finite type and a point a: ∀B, |π(B) − 1_B(a)| ≤ 1 − π(a). Take π on all subsets of [p]; then "π(S₀) := 0 when s₀ > K" is just the value of π, with no case split and no subtype for Ω. Gain: (i), (ii) first part and (v) become one-line instances. Cost: a thin corollary restating them in the paper's Ω form, so the fidelity check reads MATCH.
2. **(ii) h-part without a TV library.** Prove "≤ δ·osc(h)" from the displayed sum, and state the supremum as two facts: ≤ δ for every [0,1]-valued h, and = δ at h = 1{S ≠ S₀}. Gain: no dependency on a total-variation definition. Cost: "TV(π, point mass)" stays a prose label.
3. **LT-d pooling as a pure vector lemma.** For v₁..v₄ and t in ℝ^p: ‖¼Σv_r − t‖_∞ ≤ max_r‖v_r − t‖_∞, and {j : v_j > ½} ≠ S₀ ⇒ some |v_j − 1{j∈S₀}| ≥ ½. `pip_primary := ¼Σ p̂_r` is a Lean definition; CC3 is a code fact and stays outside Lean. Gain: no sampler objects. Cost: none.
4. **HPM clause without formalising the tie rule.** Hypotheses: Ŝ ∈ 𝓜; no S ∈ 𝓜 is better than Ŝ; F(S) > F(T) ⇒ S better than T; S₀ ∈ 𝓜; F(S₀) > F(S) for S ≠ S₀. Conclusion: Ŝ = S₀. Gain: skips the size-then-lex order and its totality proof. Lemma PC and CC2 enter as hypotheses, not axioms. Cost: none.
5. **MPM probability bound: keep out of Lean this round.** If wanted later at Level 2, it is a three-line implication with LT-b, κ₀ ≤ o₁ (ST-b) and λ₀ ≤ 19·o₁ as the named hypotheses.

## T3: domination transfer, Hellinger reduction, Lemma D0 (card `T3/FABLE_CARD.md`)
**Level-2 named axioms: none** (all Level 1). No item changes a statement.

1. **Domination transfer as finite sums of weights.** Finite type Ω; π, Q : Ω → ℝ≥0; k : Ω → [0, 1] standing for S ↦ Π(B | S, D_n).
   - (a) Q ≤ L·π ⇒ ΣQk ≤ L·Σπk. (b) π{k > a} ≤ Σπk/a.
   - Store form: Q = π restricted to 𝒯 and renormalised, with hypothesis π(𝒯) ≥ a > 0, giving ΣQk ≤ ϱ/a.
   - Gain: no kernels, no measurability, no Positivity lemma. Cost: none.
2. **HPM clauses (C-ii)(α), (C-iii):** reuse the order lemma of T2 item 4. Cost: none.
3. **Lemma H and D0 in three layers.**
   - Scalar inequality (pure real analysis): for r > 0 and z ≥ 0, 1 − A(r)·e^{−z} ≤ (r − 1)² + min{1, z·(1 + r)}, which is (H.1) after z = Δ²/(4(v + σ*²)).
   - Gaussian affinity closed form, from Mathlib's Gaussian integral; it can be time-boxed as a separate lemma because D0 already takes H² = 1 − A·B as given.
   - Integration against ν_x (Tonelli, Claim 2).
   - Gain: D0 and the pointwise half of H are certified without any integration.
4. **P6(c) by Hölder on `lintegral`** (see T3-2), with `lintegral_lintegral_swap` for the two Tonelli steps. Stay in ℝ≥0∞ until the last line.
5. **Define d_H² once.** Mathlib has no Hellinger distance (I searched the pinned checkout). Put d_H²(f, g) := 1 − ∫√(fg) for densities in a shared file; T3 and T5 both use it.

## T4: Thm 1, Thm 1′, presented Thm 2 (card `T4/FABLE_CARD.md`; consistency tier)
Lean readiness (ranked; no item changes a presented statement):

1. **Thm 2 from the presented Thm 1, not from item 6.** Thm2SG ⇐ B3w + `W3-POST2:C` case (i): expectation bound on 𝒜′_n, Markov, add P(𝒜′_nᶜ).
   - Gain: removes the proof by contradiction over sequences of designs and the O_P black box.
   - Cost: Lean-only. Named axioms: B1 (variance concentration for sub-Gaussian coordinates) and B2-core (sparse quadratic-form lower bound), unless proved.
2. **Make the expectation form the Lean headline, at a single n.** Parameters (s₀, A, σ*², M, φ₀, g₀, and c or the envelope M_n); the thresholds of walk §5.4 as hypotheses. The O_P, HPM/MPM and PIP clauses then follow from Markov and SL0 (T2).
   - Gain: no "eventually", no tightness definitions. Cost: none.
3. **Flatten the chain into five lemmas, each with its own hypotheses:** size tail → good event → supersets → underfits → assembly (R3, N3).
   - Gain: no locked-proof diffing inside Lean. Cost: blueprint work only.
4. **Level-2 named axioms for the chain** (one file per source):
   - Laurent–Massart χ² tails;
   - Gaussian tail with a union bound;
   - a Gaussian projected on a rank-d subspace is σ²χ²_d;
   - the truncated χ² moment bound of (C5);
   - the marginal-likelihood identity E₀[m_b(S)/f₀] = 1 (or the closed form, December target 4);
   - Cauchy interlacing, if Mathlib lacks it (I did not check).
5. **Conventions fixed once:** 2 ≤ p (raw count), S₀ on retained columns, m♯ as a function of (n, p, s₀), h on 2^{[p]} (R1, R4, R5, N4, N5).

## T5: Thm 9 (Thm A/B, Cor 9C chain) (card `T5/FABLE_CARD.md`; consistency tier)
Lean readiness (ranked; no item changes a presented statement):

1. **State Theorem 9 with an explicit success event.** There is a measurable set G_n of data sets with P*(G_n) ≥ 1 − n^{−cM} such that on G_n the data are admissible, r = p, Π(d_H > √(M log n/n)) ≤ n^{−cM} and Π(|S| > s + C₁M) ≤ n^{−cM}.
   - Gain: no posterior on inadmissible data; displays (i), (ii) and "the same exceptional set" follow at once; it is exactly the G_n that Cor 9C consumes.
   - Cost: the fidelity check must accept this as the paper's "In words" reading.
2. **Three layers for Theorem A.** Deterministic: Lemma H (T3). Fixed-design: Lemma X as "on a noise event, the posterior mass of the bad set is ≤ e^{−t/2}". Design: bridges B1, B2-core, B2.
   - Level-2 named axioms: the Lemma T transfer inequality (growth-function bound, a VC-type fact); Laurent–Massart χ² tails; Gamma tails; sub-Gaussian concentration for B1 and the net bound for B2-core; the marginal-likelihood identity of `lem:num`.
3. **Cor 9C at Level 1** from item 1 and the finite-sum transfer of T3 item 1; exact arithmetic and the store invariant enter as hypotheses.
4. **Thm 9B from the expectation form** (N3), with the completed pair of B3w (c) (R3). Gain: no diagonal argument. Named axioms: as T4 item 1.
5. **Lemma S cutoff in product form** (R5).

## Sol-2, Sol-3, Sol-4 cards
No Lean items (final-text confirmations of reader text, D2/D3 and the track V dossier).

## T7: Thm 4, omitted variables (card `T7/FABLE_CARD.md`)
Lean readiness (ranked; no item changes a statement):

1. **Theorem 4 as a corollary of the T4 Lean headline at unit noise.** MIS(i) is `W3-POST2:C` applied to (x, β/√v, σ*² = 1) after two deterministic reductions: posterior invariance under y ↦ a·1 + c·y (Lemma R′), and the rescaling of the class conditions by v.
   - Gain: no new probabilistic work; uniformity in v is free. Cost: R′ is Level-1 algebra on the closed-form score.
   - Named axioms: only those of T4.
2. **Make the fixed-design MIS(i) the Lean statement; derive the reader theorem** through bridges B4.0–B4.2, importing B4.1 from `W3-READER:R1` (explicit for n ≥ 3).
   - Gain: one event layer instead of two.
3. **Random-design layer (CorGb-plus) as "bound on a design event, plus its complement".** E δ_n ≤ C·r_n + P(𝒜_nᶜ).
   - Named axioms: the two conditional inputs C-MIS:GDb and C-MIS:Prop-P (they are the registry conditions), and Gaussian sample-variance concentration.
4. **Example (E1) in two parts:** the Schur-complement algebra (Level 1), and "jointly Gaussian and uncorrelated implies independent" as a named axiom unless Mathlib has it (not checked). Carry σ² + τ² > 0 as a hypothesis (T7-1).
5. **Cor H clauses:** the (KL) identity for two normals is deterministic (Level 1) and the Hellinger part reuses Lemma D0 from T3.
