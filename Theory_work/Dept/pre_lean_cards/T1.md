# T1 Fable card: Thm 3(a), `W3-PSHARP:B` (Fable 5.2, Claude Personal, high; 2026-11-18)

**Verdict:** no genuine flaw in Corollary B or its proof. Both Codex points are accepted as small, local fixes, and the headline display is untouched.

## 1. Rulings
- **T1-1: AGREE with the fix, reclassified from FLAW to (b) Lean-compile.**
  - **Fix:** add "λ ≥ 0" at `STATEMENT.md:100` and `B_sparsity.md:32`.
  - **Statement change:** yes, one tacit hypothesis made explicit in the B1 reading. Nothing is weakened. I recommend CORRECTION-ONLY.
  - **Why it is an omission, not a wrong step:** the implication is true for −3 < λ < 0 and fails only for λ ≤ −3.
- **T1-2: AGREE with the finite-J truncation; DECLINE the ℝ≥0∞ variant.** The ℝ≥0∞ route adds coercion cost and gains nothing.
  - **Fix:** for each fixed J, eventually π(S₀) ≤ 1/(1 + the first J terms), and these converge. Then let J → ∞.
  - **Statement change:** none. Lean certifies only "limsup π(S₀) ≤ e^{−λ/2}"; the real limsup is safe because π ∈ [0,1].
  - **The paper's liminf line is correct as mathematics:** for s₀ ≥ 1 each factor is ≤ ½, so 𝒪^lb ≤ (1 − 1/(2√n))^{−(s₀+1)} − 1 → e^{λ/2} − 1, and the liminf is a finite limit.
  - **No paper change:** do not add this bound to the proof. The parenthetical "liminf 𝒪^lb ≥ e^{λ/2} − 1" stays as prose.

## 2. Correctness
Nothing beyond Codex. I re-derived and confirmed the following:
- the prior-ratio identity and the count C(p − s₀, j), with all denominators ≥ p > 0;
- Lemma S on intermediate sets of size ≤ K − 1;
- constants (i)–(iv);
- the edge cases n = 3, K = 1, s₀ = 0 and s₀ = p/2;
- the eigenvalue numerator in S(1), and the Schur entries n² and n;
- the term limits (λ/2)^j/j!, and K − s₀ → ∞.

One implicit step needs to be explicit in Lean, with no text change: π(S₀) > 0. It is stated in the proof of S(4) but not in B.

## 3. Lean readiness (ranked)
**Level-2 named axioms: none.** T1 is Level 1. B2, B3 and the "in probability" clause of B1 stay out of Lean scope. No item below changes the statement.

1. **Three-layer split with an abstract core.**
   - (L1) Finite Ω, scores σ > 0, and distinct S_J ≠ S₀ with σ(S_J)/σ(S₀) ≥ ρ_J imply odds ≥ Σρ_J.
   - (L2) Combinatorics.
   - (L3) Linear algebra, entering L1 as the two hypotheses D_{S∪{j}} ≤ n·D_S and 0 ≤ Q_{S∪{j}} ≤ Q_S.

   Thm 3(a) then compiles before any matrix work, and L1 becomes the shared score base for T2.
2. **Critical scale in ε-form with explicit sequences:** for every ε > 0, eventually π(S₀) ≤ e^{−λ/2} + ε, via the finite-J route. This avoids the liminf and limsup side-conditions.
3. **S(1) by one completed square instead of simultaneous diagonalisation.** Use (n+1)A = H + nI, w = A⁻¹g, α = gᵀw and v = w/(n+1). Then gᵀH⁻¹g ≥ 2gᵀv − vᵀHv ≥ α/(n+1), so (n+1)²gᵀH⁻¹g ≥ nα. This needs only `PosDef`, not the spectral theorem. It can be a 3-line PATCH, or kept Lean-only.
4. **Q-monotonicity from Lemma V alone,** by zero-padding: Q_{S⁺} ≤ f_{S⁺}((ϑ̂_S, 0)) = Q_S. This drops block inversion from T1's Lean dependencies, and is Lean-only.
5. **Arithmetic hygiene.**
   - Write n^{−j/2} as (1/√n)^j to avoid `rpow`.
   - Write the products as `Nat.descFactorial` cast to ℝ.
   - Use `Nat.descFactorial_eq_factorial_mul_choose`, `Finset.card_powersetCard`, `Matrix.det_fromBlocks₂₂` and `PosDef.fromBlocks₂₂`. All four exist in the BNP Mathlib checkout.
