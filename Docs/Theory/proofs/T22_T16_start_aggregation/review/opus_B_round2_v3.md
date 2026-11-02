# Opus 5.5 (xhigh) Stage B round-2 ruling on PROOF_v3 — reply saved verbatim by the lead

# Round-2 Stage B review: T22 (T16), parts (i), (ii), (iv), PROOF_v3

**Scope of review.** I read only the files in `round2\`: STATEMENT.md, PROOF_v3.tex, PROOF_v3.pdf, CHANGES_v2_to_v3.md, CLAIMS_OF_FATAL_FLAWS.md and REPORT_FORMAT.md. The only command was a read-only directory listing. I compared v2 and v3 by reading them side by side, not with a mechanical diff, since I ran no tools beyond listing.

- STATEMENT.md is unchanged from round 1: same size (8123 bytes) and same text.
- The v3 PDF has the same content as PROOF_v3.tex.

## (1) Ruling on CLAIMS_OF_FATAL_FLAWS.md

The log records no fatal or gap claims from any review. **I agree with that ruling.**

- My own review of PROOF_v2 found no fatal or gap issues, only five exposition findings, with VERDICT: verified. The log records this correctly.
- My independent check of v3, below, also finds none.
- The log's summaries of Astra #1 (Stage A) and Astra #2 (Stage B) refer to files that are not in my packet. I have not seen those reviews, so I can only confirm that the log's conclusion matches my own findings.

## (2) Status of my five exposition findings from PROOF_v2

**Finding 1 (the (i-a) display overflowed the PDF margin): fixed.**
- v3 splits the display into three aligned lines (tex lines 122–127).
- On PDF page 3 the final factor (1+e)^s/(1−q)^{s+1}·γ₀^unc(S°) is now fully visible.
- The content is unchanged: Σ_Ω ≤ Σ_{[p]} = Σ_T Σ_M; then ≤ Σ_T γ₀^unc(T)·(1+e)^s; then ≤ (1+e)^s(1−q)^{−(s+1)}·γ₀^unc(S°).

**Finding 2 (the step to D_S ≥ 1 was unstated): fixed.**
- v3 now writes D_S = ∏ᵢ(1+ϱλᵢ)/(1+λᵢ), where λᵢ ≥ 0 are the eigenvalues of M_S.
- This is correct: det(I+ϱM_S) = ∏(1+ϱλᵢ) and det(I+M_S) = ∏(1+λᵢ), because M_S is symmetric.
- Each factor is ≥ 1 because ϱ ≥ 1 and λᵢ ≥ 0.

**Finding 3 (notation overload): mostly fixed, with one new clash.**
- c is renamed ϱ, so it no longer clashes with c_n or c_j.
- Sylvester's parameter t is renamed τ, so it no longer clashes with t_S.
- Lemma 2's α, β are renamed ξ, ζ, so they no longer clash with α_S, β_S in Proposition 6.
- None of ϱ, τ, ξ, ζ is used elsewhere. ϱ (varrho) is a different symbol from ϖ (varpi).
- However, renaming g(t) to g(x) creates a new clash; see New finding N1 below.

**Finding 4 (the vacuous case Ω = {S₀}): fixed.**
- v3 replaces the case with a short argument: n ≥ 3 and p ≥ 1 give K = min(p, ⌊n/2⌋) ≥ 1.
- So ∅ and {1} both lie in Ω, Ω∖{S₀} ≠ ∅, and R₀, R₁ > 0.
- This is correct. The proposition still carries "(with 0⁰ = 1)", which matches STATEMENT.md and is harmless.

**Finding 5 (the 0⁰ convention was stated only for e): fixed.**
- The preamble now states x⁰ := 1 for every x ≥ 0.
- This covers every use: e⁰; D_b⁰ when D_b = 0 in Lemma 4's coefficient bound and multinomial step; ε⁰ in Lemma 5; and β_S⁰, R_i⁰ in Proposition 6.

## (3) Correctness of PROOF_v3 and of the v2-to-v3 changes

By my reading, every change from v2 to v3 is one of the five listed in CHANGES_v2_to_v3.md. All other text is the same as v2, apart from the mechanical renaming c → ϱ throughout Lemmas 1 and 2. I checked each change.

**Lemma 1.**
- With ϱ = n+1, the formulas t_S = (n/ϱ)yᵀ(I − (I+ϱM_S)⁻¹)y and D_S = det(I+ϱM_S)/det(I+M_S) are correct.
- The bound t_S ≤ (n/ϱ)yᵀy agrees with the lemma's statement (n/(n+1))yᵀy.
- Sylvester's identity is applied with τ = ϱ and τ = 1.
- The eigenvalue-product argument is correct, as noted under Finding 2.

**Lemma 2.**
- D_{S+l}/D_S = (1+ϱξ)/(1+ζ), with 0 ≤ ξ ≤ ζ.
- 1 + ϱξ ≤ 1 + ϱζ ≤ ϱ(1+ζ) because ϱ ≥ 1.
- Hence m(S+l)/m(S) ≥ ϱ^{−1/2} = (n+1)^{−1/2}, as stated.

**(i-a).**
- The aligned display is the same chain of inequalities as in v2.
- g(x) = 1 − (1+x)^{−s} has g(0) = 0 and g′(x) = s(1+x)^{−s−1} ≤ s for x ≥ 0, so g(e) ≤ s·e.

**Lemma 7.**
- The displayed identity γ₁(S) = γ₀(S)·exp(d(S)) = ϖ(S)·∏_b r_b(S∩C_b)·BF(S)/∏_b r_b(S∩C_b) = ϖ(S)m(S)/m(∅) is correct.

**Proposition 6.**
- R₀ and R₁ are sums of positive terms over the nonempty set Ω∖{S₀}, so both are positive.
- For φ ∈ {0,1}, (iv-a) holds with equality.
- For φ ∈ (0,1), Hölder's inequality with exponents 1/(1−φ) and 1/φ gives the bound.
- The rest of the proof is unchanged from v2.

**Unchanged material.** My round-1 checks of the unchanged parts still apply: the completion bijection, Lemmas 3–6, (i-b), (i-c), (ii-a), (ii-b) and (iv-c). Those checks include the edge cases s = 0 and s = p, the size cap K, the empty maxima and the 0⁰ conventions. Every claim in STATEMENT.md is proved as stated, and every hypothesis used is in STATEMENT.md or is proved.

## Findings

**New finding N1**
- **Location:** Proof of Proposition 1 ((i-a)), second paragraph (tex line 128; PDF page 3).
- **Severity:** exposition.
- **Claim:** The v3 rename g(t) → g(x) reuses the letter x inside the same paragraph. That paragraph has just set x := (1−q)^{s+1} ∈ (0,1]; it then defines g(x) = 1 − (1+x)^{−s} "for x ≥ 0" with x as a free variable, and evaluates g at e. The finding-3 fix therefore removed one clash and added another.
- **Evidence:** The two uses never interact. g is applied only at e, and the fixed x is used only in 1 − x ≤ (s+1)q. So the meaning is unambiguous and correctness is unaffected. A fresh letter for g's argument would remove the clash.

There are no fatal or gap findings.

VERDICT: verified
