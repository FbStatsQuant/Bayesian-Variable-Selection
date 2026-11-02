# Reviewer CP (Claude Personal, Opus 5.5 xhigh, read-only; same agent resumed), round 2, PROOF_v2. Saved by the lead from the agent's returned report.

Read only the six round-2 packet files; the PDF matches the .tex. Numbering has shifted (new Lemma 3.4, Theorem 3.5 is T06(i)(c), Remark 3.6, new Remark 6.1, Theorem 6.2 through Remark 6.8); all cross-references resolve. Numbering below follows the PDF.

## Summary
Every clause was re-checked from scratch.
- Material unchanged since v1 is word-for-word the same: Lemmas 2.1–2.6, Thm 3.1, Thm 3.5, Props 4.1–4.2, Prop 5.1, Thm 5.2, Prop 5.4(a), Thms 6.2, 6.5, 6.7, Lemma 6.4. Re-verified; no errors.
- New and changed material checked line by line.

All round-1 findings are resolved. Only three new minor wording findings (N1–N3).

## Status of round-1 findings

**F1 (score formulas): resolved.**
- STATEMENT §0 now quotes H_S, D_S, Q_S, ν, m(S) with c_n, w(k), W_K, ϖ, F, Z = Σ_Ω ϖm and π. They match proof §1 symbol for symbol; Z = Σ_Ω e^{F(S)} is the same as Σ_Ω ϖm.
- The proof now relies only on STATEMENT.md, standard mathematics and H-T03.
- 00_COMMON.md is not visible to me, so I cannot confirm the quote is verbatim; that is a property of the statement, not of the proof. Two independent checks support it:
  - c_n is exactly the marginal likelihood under β_S ~ N(0, nσ²(G_S+I)⁻¹) and σ² ~ IG(a₀, b₀).
  - w(k) = ½/C(2p−1,k) equals B(k+1, 2p−k)/B(1,p), the per-model BB(1,p) prior.

**F2 (n ≥ 4 parenthetical): resolved.**
- *Ex 3.2 for general n:*
  - x₁ᵀx₂ = 0, ‖x₁‖² = ‖x₂‖² = 4c² = n−1, ‖x₃‖² = ‖x₄‖² = n−1;
  - entries sum to 0 and no column is constant;
  - K ≥ 2 for every n ≥ 4; at n = 4 there are no trailing zeros and c = √3/2.
- *Cor 3.3:* X_SX_Sᵀx₂ = (n−1)x₂, while X_S′X_S′ᵀx₂ = ((n−1)/2)(x₁+x₂). These differ because x₁ ≠ x₂.
- *Prop 5.4(b):* correlations recomputed (r₁₂ = 0, r₁₃ = r₁₄ = r₂₃ = 1/√2, r₂₄ = −1/√2, r₃₄ = 0), and x₃x₃ᵀ + x₄x₄ᵀ = x₁x₁ᵀ + x₂x₂ᵀ.
- *Lemma 3.4 (K = 1):* Ω = {∅} ∪ singletons and every x_j ≠ 0.
  - (a) Equal spans force x_i = λx_j with λ = ±1, so the outer products are equal.
  - (b) Equal outer products force equal sizes, so the pair is two singletons, and |r_ij| = 1, so it is reported.
  - This proves "never when K = 1, in particular n = 3" and the bracketed claim in (iii)(e).

**E1–E7: resolved.**
- E1: Example 3.2 now includes a response.
- E2: D_x is defined.
- E3: the duplicate pair now explicitly shares X^r and σ*².
- E4: Remark 6.1 covers the tie order; all T07 arguments use only one common total order and "least in a set ⇒ least in any subset containing it" (Thm 6.7(b) also uses totality).
- E5: measurability is correct, since {S† = S} and {MPM = a} are finite intersections of strict and non-strict comparisons that are continuous off {Cy^r = 0}. A small wording point remains (N1).
- E6: the interpretive sentences are labelled and Remark 6.8 gives examples.
- E7: the list of standard facts is complete.

## New findings

- **N1.** Location: §1, selector paragraph, last sentence. Severity: exposition.
  - Claim: "these maps are given the value ∅" seems to include π and PIP, which are a distribution and a vector, so the sentence only makes sense for S† and MPM.
  - Evidence: any fixed convention works and changes no probability, since P₀(Cy^r = 0) = 0. No result is affected.
- **N2.** Location: Example 3.2. Severity: exposition.
  - Claim: "c = √(n−1)/2" reuses the symbol c, which also denotes c_{S,S′} (Thm 3.1) and c_j (Lemma 6.4).
  - Evidence: each use is local, so nothing is ambiguous.
- **N3.** Location: Remark 6.8. Severity: exposition.
  - Claim: "S† ≠ S₀ by Theorem 6.2" needs the unstated step S† = S†_w̃ with w̃ = w.
  - Evidence: the step holds because w > 0 is a positive size-only prior and argmax_Ω F = argmax_Ω ϖm. It is one line, and the remark is not a statement clause.

## Clause-by-clause check (fresh)
- T06(i)(a), Thm 3.1 with Lemmas 2.1–2.5: correct.
- T06(i)(b), Cor 3.3, Ex 3.2, Lemma 3.4(a): correct for every n ≥ 4, and the K = 1 exclusion is proved.
- T06(i)(c), Thm 3.5 with Lemma 2.6: correct.
- T06(ii)(a), Prop 4.1: correct.
- T06(ii)(b), Prop 4.2: correct, conditional on H-T03 only.
- T06(iii)(a)(b), Prop 5.1: correct.
- T06(iii)(c), Thm 5.2: correct.
- T06(iii)(d), Cor 5.3: correct; the conditions are now explicit.
- T06(iii)(e) bullet 1, Prop 5.4(a): correct.
- T06(iii)(e) bullet 2 and bracket, Prop 5.4(b), Ex 3.2, Lemma 3.4(b): correct.
- T07 setting "any total order", Remark 6.1: correct.
- T07(i), Thm 6.2: correct.
- T07(ii)(a)–(c), Thm 6.5 and Lemma 6.4: correct.
- T07(iii)(a)–(c), Thm 6.7: correct; the interpretive sentences are labelled and illustrated in Remark 6.8.

Every clause of STATEMENT.md is proved. Nothing is used beyond STATEMENT.md, standard mathematics, and H-T03 (only in T06(ii)(b)).

## Bottom line
All round-1 findings are resolved. No fatal or gap findings remain; N1–N3 are wording only.

VERDICT: verified
