# Statement checker, second consultation (same agent, resumed), 2026-10-22

Question: approve two precisions made after review round 1 (the n ≥ 4 / K = 1 parentheticals; verbatim formulas, D_x, common X^r and σ*², interpretation labels).

Reply (saved by the lead from the agent's returned report):

**Precision 1: APPROVED.** The new wording is true in both directions and strictly stronger than round 1's "(n ≥ 4; an explicit example with n = 5)".
- *Construction for every n ≥ 4.* With c = √(n−1)/2, x₁ = c(1,1,−1,−1,0,…) and x₂ = c(1,−1,1,−1,0,…) lie in V, have ‖x‖² = 4c² = n−1, and x₁ᵀx₂ = 0. Then x₃ = (x₁+x₂)/√2 and x₄ = (x₁−x₂)/√2 are in V with norm² n−1. With p = 4, K = min(4, ⌊n/2⌋) ≥ 2, and X^r = X is valid.
  - (i)(b): S = {1,2}, S′ = {1,3} have the same span (x₃ ∈ span(x₁,x₂), x₃ ∦ x₁) and different outer products (x₃ ≠ ±x₂).
  - (iii)(e): S = {1,2}, S′ = {3,4} satisfy x₃x₃ᵀ + x₄x₄ᵀ = x₁x₁ᵀ + x₂x₂ᵀ. The correlations are r₁₂ = 0, r₁₃ = r₁₄ = r₂₃ = 1/√2, r₂₄ = −1/√2 and r₃₄ = 0, so max|r| = 1/√2 < 1 − 10⁻¹⁰ and no pair is reported.
- *K = 1 claims.* Ω = {∅} ∪ singletons.
  - ∅ versus {i}: the spans and outer products both differ.
  - {i} versus {j}: equal span means x_j = λx_i, and equal norms force λ = ±1, so the outer products are equal, |r_ij| = 1, and the pair is reported.
  - Hence no (i)(b)-pair exists, and the (iii)(e) parenthetical is correct (vacuous if p = 1). n = 3 forces K = 1.
- *Faithfulness.* Both are strengthenings beyond the original T06 ("need not tie"; "a warning, not an exact-identifiability statement"); nothing is weakened.

**Precision 2: APPROVED.** I diffed STATEMENT.md against review/STATEMENT_round1.md; the only other changes are the ones described.
- *Formulas.* All three quoted strings match 00_COMMON §1, lines 10–12, character for character. The F/Z/π quote stops before "; BF(S) = m(S)/m(∅)", which is unused. The prior parenthetical matches line 5, and ν = a₀ + n/2 agrees with ν = 0.01 + n/2.
- *D_x.* The definition matches 00_COMMON §1; it is positive because the retained columns are non-constant.
- *(iii)(d).* Making the common X^r and σ*² explicit, with "intercepts arbitrary", is correct: μ₁ = b·x_i and μ₂ = s·b·x_j = b·x_i, so Cy^r has the same law whatever α_k. This only makes an implicit quantifier explicit.
- *T07(iii).* The labels are right: those sentences were never proved claims. (iii)(a), (iii)(b) inclusion and (iii)(c) still carry the formal content; nothing is dropped.

**Non-blocking notes:**
1. §3's "No claim changed" is inaccurate for Precision 1. Suggested: "claims in (i)(b) and (iii)(e) made precise (strengthened); no other claim changed."
2. The T07(iii) header sentence "For the reported objects they hold only through scoring and estimation events" is still unlabelled informal text and could get the same "Interpretation" label.
3. In G, "X^r" should be stated to mean the retained n × p raw matrix, so that supp β ⊆ [p]. This was already present in round 1 and is not new.

**OVERALL: APPROVED** (Precisions 1 and 2 both approved; the three notes are optional wording fixes).
