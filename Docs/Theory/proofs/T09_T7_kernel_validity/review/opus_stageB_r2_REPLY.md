(Stage B reviewer: Opus 5.5, effort xhigh, native Agent tool on Claude Personal, Plan type; round 2 rulings on PROOF_v3, continued by SendMessage. Reply saved verbatim by the lead.)

# Stage B round 2 (rulings) for T09 (T7): my F1–F7, the claims log, and PROOF_v3

**Verdict on PROOF_v3: verified.** I agree with every author answer, all seven fixes work, and the v2→v3 edits broke no step. My only new findings are three small notation clashes (N1–N3 below), all exposition. I read only the packet: STATEMENT.md is unchanged from round 1, and I re-checked it against PROOF_v3.tex. I ran nothing.

## (a) Rulings on my findings and on the claims log

**F1 (any fixed exponential rate).** Agree. The fix (new Remark "Any prescribed exponential rate", cited in the closing paragraph) works:
- The arguments in Lemmas 10–12 and Propositions 13–14 only need τ, ρ ∈ (0,1) fixed, which gives κ₁ > κ₂ > 0. Their thresholds n₀ depend on (τ, ρ).
- The constants 1/40 and 55 do not depend on (τ, ρ).
- κ₂ = ½log(1/(1−τ²ρ²)) grows without bound as τρ ↑ 1. For any K₀ > 0, taking τ = ρ = (1−e^{−4K₀})^{1/4} gives κ₂ = 2K₀. Proposition 14 with κ = κ₂/2 ≥ K₀ then gives ε₁ ≤ e^{−K₀n} and discrepancy range ≥ K₀n.

**F2 (two-sided limit of d({1,2})/n).** Agree, and the fix works:
- The identity R_{12|1} = R_{12|2}·γ₁({2})/γ₁({1}) holds, since the ratio γ₁({1,2})/γ₁({1}) factors through γ₁({2}).
- So (1/n)log R_{12|1} → (κ₁−κ₂) − (κ₁−κ₂) = 0, and (1/n)d({1,2}) → −κ₂ follows.
- The one-sided bound −d({1,2}) ≥ log(3R₂) − log(2e^{1.01}n^{−1/2}) follows from R_{12|1} ≤ 2e^{1.01}n^{−1/2}. Proposition 14 uses exactly this bound.

**F3 (facts about the method I could not verify).** Agree, and the fix works:
- Validity of the data now rests on STATEMENT §1 alone.
- |C_b| ≤ B = 1 on a partition of {1,2} forces the blocks {1}, {2}.
- The claim "no property of N beyond N(j) ⊆ {1,2}∖{j} is used" is true. Proposition 13 uses K_ns({1,2},{1,2}) = K_ns(∅,∅) = 1. Proposition 14 uses only stochasticity. Part (ii) gives reversibility for any neighbour family.

**F4 (overloaded symbols).** Agree. The renaming is consistent: no c, κ_a, κ_b, e_± or "b"-as-state is left in Section 6, and the Doeblin constant is now written "constant 1/40". The renaming does introduce new minor clashes (N1–N3 below).

**F5 (index ranges in the convolution).** Agree; the fix works. The added sentence is correct: only 0 ≤ j ≤ |C_b| with t − j ≥ 0 contribute.

**F6 (lumped factors).** Agree; the fix works. I re-derived each range:
- D₂/D₁₂ ∈ [n/(n+1)², 4/n] by (B3), so its square root lies in [√n/(n+1), 2/√n].
- √n/(n+1) ≥ 1/(3(n+1)).
- 2n^{−1/2} ≤ n^{1/2} for n ≥ 2.
- ⅓n^{−1/2} lies in [1/(3(n+1)), n^{1/2}].

**F7 (asymptotic parameter).** Agree; the fix works. The new opening sentence of Section 6 states that the parameter is n with p = 2 fixed.

**Claims log, Stage A, Astra #1, finding 1 (graded fatal, about STATEMENT's old reading of (v)).** I agree with the finding and with the fix.
- Check: K ≥ 1, so Ω contains ∅ and {1}, so min q_φ ≤ ½. Then sup_x‖δ_x − q_φ‖_TV = 1 − min q_φ ≥ ½ > ¼, so t_mix ≥ 1 always. A mixing-time lower bound tending to 0 was therefore trivially available, and the old parenthetical was wrong.
- The current reading ("lower bound tending to infinity", plus t_mix ≤ 55) is faithful to the original wording ("exponentially slow mixing", "such a lower bound").
- The bound t_mix ≤ 55 is proved: log(40/39) > 1/39 − 1/(2·39²) ≈ 0.025312 > 0.0253, and 55 × 0.0253 = 1.3915 > log 4 ≈ 1.3863.
- The change touched only the reading. The original wording, the hypotheses and the existence claim are unchanged, as the log says.

**Claims log, Astra #1, finding 2 (exposition, 0/0 in the reverse proposal probability).** Agree that it is fixed. The two case formulas for Q(S,S′) and Q(S′,S) in Part (ii) have nonzero denominators exactly where they are used. I verified this in round 1, and the text is unchanged in v3.

**Claims log, Stage B entries.** The quotation of my F1 is accurate. Astra #2's "no findings" is consistent with my own review: I found no fatal error and no gap.

## (b) Review of PROOF_v3 against STATEMENT.md

**What changed.** Sections 1, 3, 4 and 5 and both Remarks outside Section 6 are identical to v2, which I verified in round 1. Section 2 differs only by the F5 sentence.

**Section 6, re-derived under the new names:**
- Norms are all n−1. Inner products: x₁ᵀx₂ = (n−1)τ, z₁ = (n−1)ρ, z₂ = (n−1)τρ.
- Singletons: H = n², D = n, Q₁ and Q₂ as stated.
- The pair: α± = (n²−1)(1±τ) + 1 = (n+1)β± − n, so D₁₂ = f(1+τ)f(1−τ).
- t₁₂ = n(n−1)ρ²(1−δ/2)/(n+1) with 0 < δ < 2/(n²−1).
- (B1)–(B3) carry over unchanged with (n−1)(1−τ) ≥ 1.
- R₁ = BF({1})/3, and R_{12|1}, R_{12|2} as stated (using w(2)/w(1) = 1).
- The new fifth limit of Lemma 11 and the new Lemma 12(c) bound are correct (see F2).
- In Proposition 14's proof, "≥ log(3R₂) − log(2e^{1.01}n^{−1/2}) = κ₂n + o(n)" is right as an asymptotic equality: the left side is log R₂ + ½log n + O(1).
- Propositions 13 and 14 are correct under the renaming.
- The Remark is verified (see F1).

**New findings:**

**N1.**
- **Location:** Section 6, Remark "Any prescribed exponential rate", and the claims log.
- **Severity:** exposition.
- **Claim:** The prescribed rate is written K₀. K already denotes the maximum model size, and K_σ, K_φ denote kernels, so K₀ reads naturally as the kernel at φ = 0.
- **Evidence:** STATEMENT §1 defines K = min(p, ⌊n/2⌋) and K_φ. The meaning is clear from context, and correctness is unaffected.

**N2.**
- **Location:** Section 6, "The family" versus Proposition 14.
- **Severity:** exposition.
- **Claim:** The renaming to h₁, h₂, h₃ for the orthonormal vectors clashes with h, the number of steps in "K₁^h" and "for all h ≥ 0", within the same section.
- **Evidence:** "fix orthonormal h₁,h₂,h₃" sits a few paragraphs before "‖K₁^h(x,·) − q₁‖ ≤ (39/40)^h". The two are never confused in any computation.

**N3.**
- **Location:** Section 6, notation paragraph.
- **Severity:** exposition.
- **Claims:**
  - Subscript 1 now means the state {1} on Q, D, A, R and κ, but φ = 1 on q₁, γ₁, ε₁ and K₁. K₁ also collides with STATEMENT's "K_1, …, K_m", the step kernels.
  - Unsubscripted R is the correlation matrix, while R₁, R₂ and R_{12|·} are ratios.
  - x denotes both the data columns x₁, x₂ and states x, x′ ∈ Ω. That clash was already in v2.
  - "w(1) = w(1)" in Lemma 11 is a vacuous way of saying both singletons carry the same prior weight. Also carried over from v2.
- **Evidence:** The notation paragraph lists which symbols carry state subscripts, so every formula can still be parsed unambiguously. No step is affected.

Nothing the v2→v3 changes touched is broken. The rename is consistent across every lemma and proposition, the Remark's claims are correct, and the new limit (1/n)log R_{12|1} → 0 is correctly derived. All of STATEMENT.md's claims (i)–(v) are established, including the readings of (iii) and (v), which are faithful to the quoted original wording.

**Verdict on PROOF_v3: verified.**
