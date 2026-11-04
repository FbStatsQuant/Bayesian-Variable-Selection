# CLAIMS OF FATAL FLAWS — T04 (A3)

This file logs every fatal or gap finding, copied verbatim, together with the lead's answer.

## Round 1 (reviewing PROOF_v1)

Neither reviewer reported a fatal finding. There was one gap finding, from CW. CP raised the same point, graded as exposition.

### CW-F1 (gap)

> **F1. Lemma 1.2 / §0 "Prior and target": the formula for π is imported from outside the packet.**
> - **Severity:** gap (packet scope; load-bearing but likely easily repaired).
> - **Claim.** The proof uses π(S) ∝ ϖ(S) D_S^{-1/2} (2b₀ + Q^{v3}_S)^{-ν}, with Q^{v3}_S = yᵀy − n z_Sᵀ H_S⁻¹ z_S, y = Cy^r/s_y and z_S = X_Sᵀ y, all "from 00_COMMON §1". Neither STATEMENT.md nor the proof defines this formula: §0 writes π(S) ∝ ϖ(S) m(S) and never defines m(S). So I cannot confirm from the packet that this is the v3 posterior.
> - **Why it matters.** The identity "S-marginal of Π† = π" carries weight in two places:
>   - H-T02 is a statement about π, and the proof uses it to discard {|S| > m_n} under Π†.
>   - The first claim of (ii) is about π, and Theorem 7.4 proves it through (2), which comes from Lemma 1.1(a) via Lemma 1.2.
> - **Evidence.** Given the quoted formula, the algebra in Lemma 1.2 is correct: Cy^r = U y_c, so y = U y_c / s_y and z_S = Z_Sᵀ y_c / s_y, hence Q^{v3}_S = Q_S / s_y² and 2b₀ + Q^{v3}_S = (2b + Q_S)/s_y². The factor s_y^{2ν} does not depend on S. The formula is also consistent with:
>   - the quantities listed in STATEMENT §1 (D_S, ν = 0.01 + n/2, b₀);
>   - the T01(i) remark: θ = s_y β and v = s_y² σ² map IG(0.51, b₀) to IG(0.51, b₀ s_y²), and N(0, nσ²(G_S + I)⁻¹) to N(0, nv(G_S + I)⁻¹).
> - **Suggested repair.** Quote the 00_COMMON §1 definition verbatim (in §0 or in the packet). A one-line comparison then closes the gap.

(CP Finding 1, graded exposition, makes the same point and recommends "reproducing the formula in STATEMENT.md".)

**Lead's answer: accepted and fixed.**
- **Check against the source.** The formula is the v3 definition. 00_COMMON §1 reads, verbatim:

  > m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{−1/2}(2b₀ + Q_S)^{−ν}

  with Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, z_S = X_Sᵀy, y = Cy^r/s_y, a₀ = b₀ = 0.01, ν = 0.01 + n/2, F(S) = log[ϖ(S)m(S)], Z = Σ_Ω ϖ(S)m(S) and π(S) = e^{F(S)}/Z.
- **Changes made.**
  - STATEMENT.md §1 ("Model quantities") now writes out this definition of m(S) and π in full. This adds a definition already in 00_COMMON §1. It is not a change to the statement.
  - PROOF_v2 §0 ("Prior and target") states the same formula.
  - Lemma 1.2 now cites §0 rather than 00_COMMON.
- **Why it suffices.** The comparison in Lemma 1.2 was already verified by both reviewers. Once the formula is in the packet, the gap closes.

## Round 2 (reviewing PROOF_v2)

- **Fatal or gap findings:** none, from either reviewer.
- **CW-F1:** both reviewers confirm it is closed (review/ROUND2_CP.md, review/ROUND2_CW.md).
- **Verdicts:** CP verified; CW verified.
- **Exposition findings left open:** these are notation notes only (CP F1–F3, CW R2-E1/E2). They are recorded in FINAL_REPORT.md and are not applied, so that the final proof is exactly the text both reviewers verified.
