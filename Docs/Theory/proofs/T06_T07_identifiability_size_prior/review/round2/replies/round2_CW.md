# Reviewer CW (Claude Work, Opus 5.5 xhigh, read-only; delegate_task T06T07-review-CW-round2), round 2, PROOF_v2. Saved by the lead from the task_status summary.

I read every file in the packet (STATEMENT.md, REPORT_FORMAT.md, CHANGES_v1_to_v2.md, YOUR_ROUND1_REPORT.md, PROOF_v2.tex) and also PROOF_v2.pdf. The PDF has 9 pages, matches the source, and every cross-reference resolves. I wrote nothing and ran nothing.

**Summary.** There are no fatal findings and no gap findings. I re-checked every step from scratch. Round-1 gaps F1 and F2 are closed, and F3–F6 are resolved. Two new exposition remarks follow; neither affects correctness.

## Findings

**N1**
- *Location:* §1, the "Measurability" parenthesis.
- *Severity:* exposition.
- *Claim:* "On the null event {Cy^r = 0} these maps are given the value ∅" works for S† and MPM, which are set-valued. It does not fit π and PIP, which are real-valued. Strictly, the location-invariance claim for π and PIP needs some fixed value for them on that event.
- *Evidence:* any fixed measurable convention on the null event works, and no probability in T06 or T07 changes. This is wording only.

**N2**
- *Location:* §1, "F(S) = log[ϖ(S)m(S)] for S ∈ Ω"; STATEMENT §0 line 15 ("for S ⊆ [p]: … F(S) = …").
- *Severity:* exposition.
- *Claim:* the proof defines F only on Ω, while the statement lists F(S) for every S ⊆ [p].
- *Evidence:* no clause of T06 or T07 evaluates F off Ω, and T07's S*_k for k > K uses m, which is defined for all S. Nothing is lost.

## Status of round-1 findings

- **F1 resolved.**
  - STATEMENT §0 quotes the formulas, and they match proof §1 symbol for symbol.
  - I re-derived them independently:
    - Woodbury gives (I + nX_S(G_S+I)⁻¹X_Sᵀ)⁻¹ = I − nX_SH_S⁻¹X_Sᵀ, so the quadratic form is Q_S.
    - The determinant identity gives D_S.
    - Integrating out σ² ~ IG(a₀, b₀) gives c_n D_S^{−1/2}(2b₀+Q_S)^{−ν}.
    - The BB(1, p) weight is ½/C(2p−1, k).
  - Whether the quotes match 00_COMMON is outside the packet; the statement checker approved that.
- **F2 resolved.**
  - Example 3.2 holds for every n ≥ 4: the norms, orthogonality and zero sums all check, and K ≥ 2.
  - Corollary 3.3 holds at general n.
  - Lemma 3.4(a)(b) for K = 1 is correct.
  - The imprecise "K ≥ 2, i.e. n ≥ 4" is gone.
- **F3 resolved.** D_x is defined as positive diagonal, hence invertible; Corollary 5.3 relies on this.
- **F4 resolved.** Remark 6.1 covers it. The T07 arguments use only totality of the order and the fact that the ≺-least element stays ≺-least in any subset containing it. Nothing uses the size-first property.
- **F5 resolved.** The example now includes a raw response.
- **F6 resolved.** The interpretive sentences are labelled, and (a)–(c) are proved.

## Clause-by-clause verification (fresh)

All checked and correct:
- the preliminaries, eq. (1) and Lemmas 2.1–2.6;
- T06(i)(a), Thm 3.1, both directions, including ∅ and n = 3;
- T06(i)(b), Cor 3.3, Ex 3.2 and Lemma 3.4(a);
- T06(i)(c), Thm 3.5: V-coordinates, P₀(v = 0) = 0, UᵀBU ≠ 0, Lemma 2.6, and the finite union;
- T06(ii)(a), Prop 4.1;
- T06(ii)(b), Prop 4.2: only H-T03 and the definition of O_P are used; NIS is not used; Remark 4.3 is correct;
- T06(iii)(a)(b), Prop 5.1;
- T06(iii)(c), Thm 5.2: randomised selectors via Tonelli, ∫min = 2Φ(−Δ/(2σ*)), Δ = 0, the decomposition, and the α₂ shift;
- T06(iii)(d), Cor 5.3, including the duplicate pair with a common X^r and σ*²;
- T06(iii)(e), Prop 5.4(a)(b): general-n correlations, max|r| = 1/√2, and the K = 1 parenthetical via Lemma 3.4(b);
- T07(i), Thm 6.2, including s₀ > K and m > 0 for all S; Remark 6.3 is correct;
- T07(ii), Lemma 6.4 and Thm 6.5, including boundary ties; Remark 6.6 (N₊ < 2K) is correct;
- T07(iii), Thm 6.7(a)(b)(c);
- the facts stated in STATEMENT §0.

## Edge cases checked

None fails:
- n = 3; n = 4; p = 1;
- the empty model;
- s₀ > K; S₀ ∉ Ω;
- Δ = 0; PIP_j = ½; N₊ = 0;
- ties at the cap boundary; ties in m within a size;
- randomised selectors;
- the degenerate Gaussian Cy^r;
- the null event {Cy^r = 0};
- σ*² > 0;
- different σ*² across Θ_n.

## External inputs

Besides standard mathematics (the preamble list is complete), the proof uses only:
- H-T03, in Proposition 4.2 only;
- the formulas quoted in STATEMENT §0;
- the facts the statement gives.

Remarks 3.6, 4.3, 5.5, 6.3, 6.6 and 6.8 go beyond the statement; I checked them and they are correct.

VERDICT: verified
