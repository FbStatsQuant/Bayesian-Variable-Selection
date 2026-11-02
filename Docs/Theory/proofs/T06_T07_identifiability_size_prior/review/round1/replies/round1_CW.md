# Reviewer CW (Claude Work, Opus 5.5 xhigh, read-only, via delegate_task T06T07-review-CW-round1), round 1, PROOF_v1 — saved by the lead from task_status summary

# Independent review of PROOF_v1 (T06 and T07)

I read STATEMENT.md, REPORT_FORMAT.md, PROOF_v1.tex and PROOF_v1.pdf (9 pages; the PDF matches the source and every cross-reference resolves). I wrote nothing and ran nothing.

**Summary.** No fatal findings. All the mathematics checks out step by step, given the formulas the proof writes down in its §1. Two gaps stop me from giving an unconditional "verified". F1: I cannot check the §1 formulas against 00_COMMON §1, which is not in the packet. F2: the "n ≥ 4" qualifier in T06(i)(b) and T06(iii)(e) is asserted but not proved. Both are cheap to close. F3–F6 are exposition.

## Findings

**F1**
- **Location:** proof §1, lines 38–42 (H_S, D_S, Q_S, m(S), c_n, w(k)); STATEMENT §0 ("All are as in 00_COMMON §1").
- **Severity:** gap (a fidelity question that cannot be checked inside the packet).
- **Claim:** The proof fixes explicit formulas that STATEMENT.md does not contain; it refers to 00_COMMON §1 instead:
  - H_S = (n+1)G_S + I_k;
  - D_S = det H_S/det(G_S + I_k);
  - Q_S = yᵀy − n z_SᵀH_S⁻¹z_S;
  - m(S) = c_n D_S^{−1/2}(2b₀ + Q_S)^{−ν};
  - c_n = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀));
  - w(k) = ½/C(2p−1, k).
- **Evidence:** I checked the formulas against a standard conjugate model, and they are exactly right for it:
  - with β_S | σ² ~ N(0, nσ²(G_S+I)⁻¹) and σ² ~ IG(a₀, b₀), yᵀ(I + X_SΣ₀X_Sᵀ)⁻¹y = Q_S and det(I + X_SΣ₀X_Sᵀ) = det(nΣ₀′)·det(H_S/n) = D_S;
  - integrating out σ² gives exactly c_n D_S^{−1/2}(2b₀ + Q_S)^{−ν};
  - w(k) is the BB(1, p) weight, p·k!(2p−1−k)!/(2p)! = ½/C(2p−1, k).

  If 00_COMMON differs, the following must be re-checked: Lemmas 2.1 and 2.4, the "only if" of Theorem 3.1, and the results that depend on them (Theorem 3.4, Proposition 5.4(a)). These steps need M_S = f(X_SX_Sᵀ) with f strictly increasing, f(0) = 0 and sup f < κ, and D_S a function of X_SX_Sᵀ. T06(ii), T06(iii)(c)(d) and all of T07 use only m > 0 and a positive size-only prior, so they are unaffected. The lead should confirm §1 against 00_COMMON §1.

**F2**
- **Location:** Example 3.2 heading ("such examples need K ≥ 2, i.e. n ≥ 4"), Corollary 3.3 and Proposition 5.4(b); in STATEMENT.md, T06(i)(b) and the second bullet of T06(iii)(e), both "(n ≥ 4; an explicit example with n = 5)".
- **Severity:** gap (minor).
- **Claim:** The proof gives only the n = 5 example. Under neither reading of the parenthetical is it proved:
  - "such inputs need n ≥ 4" is asserted in a heading without argument;
  - "such inputs exist for every n ≥ 4" is shown only for n = 5.

  Also, "K ≥ 2, i.e. n ≥ 4" is imprecise: K ≥ 2 holds exactly when n ≥ 4 and p ≥ 2.
- **Evidence:** Both readings are true and easy to prove.
  - *Necessity in (i)(b), K = 1.* Feasible models have at most one element, and every x_j ≠ 0. So equal spans with S ≠ S′ force S = {i}, S′ = {j} and x_i = λx_j. Equal norms give λ = ±1, so the outer products are equal. No qualifying pair exists.
  - *Necessity in (e)(b), K = 1.* Equal outer products force equal sizes (Lemma 2.3). Then x_ix_iᵀ = x_jx_jᵀ forces |r_ij| = 1, as in the proof of Prop 5.4(a), so the pair is reported.
  - *Existence for every n ≥ 4.* Take x₁ = c(1,1,−1,−1,0,…,0)ᵀ and x₂ = c(1,−1,1,−1,0,…,0)ᵀ with c = √(n−1)/2, and x₃, x₄ as in Example 3.2. Every identity used there still holds.

**F3**
- **Location:** §1, line 46 (X = CX^rD_x⁻¹, θ = D_xβ); proof of Corollary 5.3 ("D_x is diagonal and positive").
- **Severity:** exposition.
- **Claim:** The proof silently assumes that X^r has no exactly constant columns, so that D_x is invertible and β is indexed by [p]. STATEMENT §0 uses the same convention implicitly (S₀ = supp β ⊆ [p], θ* = D_xβ). State it once.
- **Evidence:** μ = Xθ* = CX^rD_x⁻¹D_xβ in Cor 5.3 requires D_x invertible.

**F4**
- **Location:** §6 preamble; the T07 setting in STATEMENT.md ("any fixed total order on subsets of [p] works").
- **Severity:** exposition.
- **Claim:** The proof never addresses this sentence.
- **Evidence:** Thms 6.1, 6.4(a) and 6.6(a)(b) use only that ≺ is a total order and that the ≺-least element of a set is ≺-least in any subset containing it. Thm 6.6(b) also needs S*_k and Ŝ to use the same order. So the claim holds for any fixed order used throughout, but this should be said.

**F5**
- **Location:** Example 3.2.
- **Severity:** exposition.
- **Claim:** A valid input requires a non-constant raw response, and none is given.
- **Evidence:** All the claims concern X only, so any non-constant y^r completes the input. One clause fixes this.

**F6**
- **Location:** STATEMENT T07(iii) framing sentences ("hold only through scoring and estimation events"; "not controlled by (i)–(ii)"); proof Remark 6.7.
- **Severity:** exposition.
- **Claim:** These are informal framing, not theorems; Remark 6.7 restates them. The formal content of T07(iii) is (a)–(c), which are proved. Nothing is missing.

## Clause-by-clause verification

**T06(i)(a), Thm 3.1.** ✓
- SVD: M_S = Σ ns_i²/((n+1)s_i²+1) u_iu_iᵀ = f(X_SX_Sᵀ), with f < n/(n+1) < 1 < κ, and D_S = Π g(s_i²).
- On 𝕊, 2b₀ + Q_S = yᵀ(κI − M_S)y.
- Only if: CBC = 0 gives (1−c)κC = M_S − cM_S′. Since rank M_S ≤ K < n−1 = dim V (n = 3: 1 < 2), M_S has a kernel vector in V, so c ≥ 1; symmetrically c ≤ 1. So M_S = M_S′, and injectivity of f finishes.
- If: the trace lemma. ∅ is handled by the conventions.

**T06(i)(b), Cor 3.3 / Ex 3.2.** ✓ apart from F2.
- Recomputed x₃ = (√2,0,0,−√2,0) and x₄ = (0,√2,−√2,0,0).
- All column sums are 0 and all squared norms are 4.
- r₁₂ = r₃₄ = 0, r₁₃ = r₁₄ = r₂₃ = 1/√2, r₂₄ = −1/√2.
- X_SX_Sᵀx₂ = 4x₂ ≠ 2(x₁+x₂) = X_S′X_S′ᵀx₂.

**T06(i)(c), Thm 3.4.** ✓
- t = Uᵀv ~ N_{n−1}(Uᵀμ, σ²I); by homogeneity, a tie holds iff tᵀ(UᵀBU)t = 0.
- UᵀBU ≠ 0 by Lemma 2.5 and Thm 3.1.
- The zero set is null: each section has at most 2 points, then Fubini. Finite union over pairs.

**T06(ii)(a), Prop 4.1.** ✓ π(S) ≤ 1 − π(S₀) < ½ < π(S₀), and F is strictly monotone in π. If S₀ ∉ Ω, the event is empty.

**T06(ii)(b), Prop 4.2.** ✓ Uses H-T03 only. r_n → 0 and r_n > 0 for n ≥ 3. {1−π ≥ ½} ⊆ {1−π > Mr_n} once Mr_n < ½. NIS is not used.

**T06(iii)(a)(b), Prop 5.1.** ✓ x_{τk}x_{τk}ᵀ = x_kx_kᵀ; τ is an involution of Ω that swaps {S∋i} and {S∋j}; 2π(S) ≤ 1 − π(∅) < 1.

**T06(iii)(c), Thm 5.2.** ✓
- ‖y−m₁‖² − ‖y−m₂‖² = 2ΔT(y), and T ~ N(∓Δ/2, σ²), so ∫min(p₁,p₂) = 2Φ(−Δ/(2σ)); for Δ = 0 it is 1 = 2Φ(0).
- Randomisation is handled through φ (Tonelli) and convexity.
- (I−C)(m₁−m₂) = 11ᵀ(m₁−m₂)/n.
- The intercept shift keeps μ₂, the support, and the law of (Cy^r, U).

**T06(iii)(d), Cor 5.3.** ✓ (see F3). Continuity of Φ; for the duplicate pair, μ₂ = s b x_j = s² b x_i = μ₁.

**T06(iii)(e), Prop 5.4.** ✓ apart from F2.
- Applying the outer products to x_i gives x_i = r_ij x_j, so |r_ij| = 1; the converse is Cauchy–Schwarz.
- x₃x₃ᵀ + x₄x₄ᵀ = x₁x₁ᵀ + x₂x₂ᵀ, and max|r| = 1/√2.

**T07(i), Thm 6.1.** ✓ The prior is constant (γ > 0) on {|S| = s₀} ⊆ Ω, so argmax_𝒦 m ⊆ argmax_Ω ϖm, and being ≺-least passes to the subset. If s₀ > K, the event is empty.

**T07(ii)(a)–(c), Thm 6.4 / Lemma 6.3.** ✓
- ρ_H = Σ PIP_j + Σ_{j∈a}(1−2PIP_j).
- The minimisers are J₊ ∪ E with E ⊆ {q_j = ½}.
- Capped case: restrict to a∩J₊; the ℓ smallest c_j are all negative.

**T07(iii)(a)–(c), Thm 6.6.** ✓
- (a) max_𝒮 F = max_Ω F when the intersection is nonempty.
- (b) Equal prior weight at size s₀. If m(S*) > m(S₀), S₀ is not the 𝒮-argmax. If equal, S* ≺ S₀. Either way Ŝ ≠ S₀, a contradiction.
- (c) Three-bracket split with c_j − ĉ_j = 2(p̂_j − PIP_j); the middle bracket is ≤ 0.

## Edge cases checked

None of these fails:
- n = 3 (K = 1): eq. (1) holds; only F2 is affected;
- the empty model;
- s₀ > K;
- the null event Cy^r = 0;
- Δ = 0;
- PIP_j = ½;
- ties at the cap boundary;
- randomised selectors;
- σ*² > 0 (needed for the density arguments, and assumed).

## External inputs

Besides standard mathematics, the proof uses only H-T03 (Prop 4.2) and the §1 formulas (F1). Statement-given facts are used as given: 𝕊 is the image set, X^r = X is a valid input, and the report threshold is 1 − 10⁻¹⁰. Remarks 3.5, 4.3, 5.5, 6.2 and 6.5 go beyond the statement; I checked them, and they are correct.

## To reach "verified"

Add the K = 1 necessity argument and the general-n ≥ 4 example (F2), and have the lead confirm the §1 formulas against 00_COMMON §1 (F1).

VERDICT: not verified
