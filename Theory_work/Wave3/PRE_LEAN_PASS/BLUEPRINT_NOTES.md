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
