# CLAIMS OF FATAL FLAWS: T06 + T07

Every fatal or gap finding, copied verbatim (full replies in review/round1/replies/), with the lead's answer. Exposition findings are listed at the end with their dispositions.

## Round 1 (PROOF_v1)

No fatal findings from either reviewer. Two gap findings, raised independently by both reviewers.

### CP-F1 and CW-F1 (gap): the score formulas cannot be checked against 00_COMMON §1

**CP-F1, verbatim:** "Location: Proof §1 (definitions of H_S, D_S, Q_S, m(S), c_n, w(k)), used by Lemma 2.1, 2.4, Thm 3.1, 3.4 and everything downstream. Severity: gap (unverifiable from the packet; load-bearing). Claim: STATEMENT.md only names these objects ("All are as in 00_COMMON §1"), which is not in the packet. The proof supplies explicit formulas (…); I cannot confirm they match the source; this is also material beyond STATEMENT.md. Evidence: internally coherent (…). The exact form matters: under a Zellner g-prior (H_S ∝ G_S), M_S = (g/(1+g))P_S and D_S = (1+g)^{|S|}, so F_S would depend only on (span X_S, |S|), and in Example 3.2 S = {1,2}, S′ = {1,3} would tie with different outer products — T06(i)(a) "only if" and (i)(b) would be false. So correctness depends on the proof's formulas being those of 00_COMMON §1."

**CW-F1, verbatim:** "Location: proof §1, lines 38–42 (H_S, D_S, Q_S, m(S), c_n, w(k)); STATEMENT §0 ("All are as in 00_COMMON §1"). Severity: gap (a fidelity question that cannot be checked inside the packet). Claim: The proof fixes explicit formulas that STATEMENT.md does not contain (…). Evidence: (…) exactly right for β_S | σ² ~ N(0, nσ²(G_S+I)⁻¹), σ² ~ IG(a₀, b₀) (…). If 00_COMMON differs, the following must be re-checked: Lemmas 2.1 and 2.4, the "only if" of Theorem 3.1, and Theorem 3.4 and Proposition 5.4(a), which depend on them (…). The lead should confirm §1 against 00_COMMON §1."

**Lead's answer: accepted and fixed.**
- I compared the proof's §1 formulas with `theorems/00_COMMON.md` §1, lines 10–11. They agree exactly:
  - H_S = (n+1)G_S + I;
  - D_S = det H_S/det(G_S+I);
  - Q_S = yᵀy − n z_SᵀH_S⁻¹z_S;
  - ν = 0.01 + n/2 and a₀ = b₀ = 0.01;
  - m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{−1/2}(2b₀ + Q_S)^{−ν};
  - w(k) = ½/C(2p−1, k).
- The prior β_S ~ N(0, nσ²(G_S+I)⁻¹) is on line 5 of the same file.
- Fix: STATEMENT.md §0 now quotes these lines verbatim, so the statement is self-contained. The proof's §1 says they are the statement's formulas. The mathematics is unchanged.

### CP-F2 and CW-F2 (gap): the "(n ≥ 4)" parenthetical is not proved

**CP-F2, verbatim:** "Location: STATEMENT T06(i)(b) and T06(iii)(e) second bullet, parenthetical "(n ≥ 4; an explicit example with n = 5)"; proof Example 3.2 title, Cor 3.3, Prop 5.4(b). Severity: gap (minor). Claim: the proof only asserts "such examples need K ≥ 2, i.e. n ≥ 4" in the title, with no argument, and gives only the n = 5 example; so the parenthetical is not proved either as a necessary condition or as "exist for every n ≥ 4". (…) Also "K ≥ 2, i.e. n ≥ 4" is imprecise: K ≥ 2 iff n ≥ 4 and p ≥ 2."

**CW-F2, verbatim:** "Location: Example 3.2 heading (…), Corollary 3.3, Proposition 5.4(b); in STATEMENT.md, T06(i)(b) and the second bullet of T06(iii)(e) (…). Severity: gap (minor). Claim: The proof gives only the n = 5 example. Under neither reading of the parenthetical is it proved (…). Evidence: Both readings are true and easy to prove: (…) necessity for K = 1 (…); existence for every n ≥ 4: x₁ = c(1,1,−1,−1,0,…,0)ᵀ, x₂ = c(1,−1,1,−1,0,…,0)ᵀ, c = √(n−1)/2, x₃, x₄ as in Example 3.2."

**Lead's answer: accepted and fixed.**
- The parenthetical now states both readings, and the proof proves both:
  - Example 3.2 is generalised to every n ≥ 4 (p = 4, so K ≥ 2).
  - New Lemma 3.3 shows that when K = 1 (in particular n = 3, or p = 1) no feasible pair has equal spans with unequal outer products, and every pair with equal outer products is a reported pair with |r_ij| = 1.
- The imprecise phrase "K ≥ 2, i.e. n ≥ 4" is removed.
- This is a precision of a parenthetical, not a change to any claim. The statement checker is consulted on the wording (review/STATEMENT_CHECK_2.md).

## Exposition findings, round 1 (dispositions)

- **CP-E1 / CW-F5** (Example 3.2 lacks a raw response): fixed. Any non-constant y^r completes the input.
- **CP-E2 / CW-F3** (D_x undefined; no constant columns assumed): fixed. §1 defines D_x as the positive diagonal matrix of retained raw column SDs (dropped constant columns excluded), as in 00_COMMON §1.
- **CP-E3** (the duplicate pair needs common X^r and σ*²): fixed. Stated explicitly in Corollary 5.3 and STATEMENT (iii)(d).
- **CP-E4 / CW-F4** ("any fixed total order works" is not addressed): fixed. A remark at the start of §6 says the arguments use only that ≺ is one total order shared by S†_w̃, S*_k, S† and Ŝ.
- **CP-E5** (measurability, and the convention on {Cy^r = 0}): fixed. §1 adds a measurability sentence and the convention (output ∅ on that null event).
- **CP-E6 / CW-F6** (T07(iii) framing is informal): fixed. Remark 6.7 now gives the one-line example 𝒮 = {S₀}, and STATEMENT marks the framing sentences as interpretation.
- **CP-E7** (the standard-facts list is incomplete): fixed. The list is completed.

## Round 2 (PROOF_v2)

Neither reviewer raised a fatal or gap finding, and both verdicts are **verified**. Each reviewer confirmed that every one of its round-1 findings is resolved. The new findings are exposition only:
- CP-N1 / CW-N1: the null-event convention "value ∅" fits only the set-valued maps; π and PIP need any fixed convention.
- CP-N2: the symbol c is reused.
- CP-N3: Remark 6.8 needs the one-line step S† = S†_w.
- CW-N2: F is defined on Ω in the proof but listed for every S ⊆ [p] in STATEMENT §0.

All the reviewers agree these affect no result. They are not applied, so that the verified text stays exactly as reviewed; they are recorded in FINAL_REPORT.md for a later editorial pass.
