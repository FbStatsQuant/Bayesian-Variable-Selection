# V-b-1
stop_reason: end_turn

# Card V, route V-b — Lemma V via the marginal-likelihood (Gaussian integral) identity

**Result.** Lemma V (a), (b), (c) is proved as stated, with no eigenvalue or rank condition; singular G_S, duplicated columns, s₀ = 0, J = ∅, |S| > N and S ∉ Ω are all covered. Part (b) comes out slightly stronger, with exponent (rank G_{S₀} + rank G_S)/2 ≤ s₀ + |J|/2. Parts (b) and the order facts are derived independently of REPORT A2 (no determinant-monotonicity step); part (a) is necessarily the same Young-inequality shift as A2, so for (a) this is a re-derivation that confirms the constants rather than an independent argument.

**Notation.** σ := σ*. Z_T := X_{c,T} ∈ ℝ^{N×|T|}, so G_T = Z_TᵀZ_T (because X = UX_c), and A_T := G_T + I ≻ 0. Write 0 for S₀. θ* also denotes its restriction to S₀, and θ̃ ∈ ℝ^S its zero-padding. Then μ_c = Z₀θ* = Z_Sθ̃ and y_c = μ_c + e. For κ > 0:

- M^{(κ)}_T := Z_T(G_T + κA_T/n)⁻¹Z_Tᵀ, with M^{(1)}_T = nZ_TH_T⁻¹Z_Tᵀ = M_T since G + A/n = H/n;
- Σ^{(κ)}_T := I_N + (n/κ)Z_TA_T⁻¹Z_Tᵀ;
- D^{(κ)}_T := det Σ^{(κ)}_T;
- Q^{(κ)}_T(Y) := min_φ{‖Y − Z_Tφ‖² + κφᵀA_Tφ/n}, with Q^{(1)}_T(y_c) = Q^c_T.

For T = ∅: M = 0, Σ = I, D = 1, Q(Y) = ‖Y‖².

**Interpretation (not used as a proof step).** σ²Σ^{(κ)}_T is the covariance of Y = Z_Tφ + ε with ε ~ N(0, σ²I) and φ ~ N(0, (nσ²/κ)A_T⁻¹). So g_T^{(κ)} := N_N(·; 0, σ²Σ^{(κ)}_T) is the fixed-variance marginal likelihood of model T with the slab precision scaled by κ ([P1] `lem:slab` is κ = 1). P2–P3 below are the two ways of writing this density.

## 1. Preliminaries (each holds for every T ⊆ [p] and κ > 0)

**P1 (minimum).** Q^{(κ)}_T(Y) = Yᵀ(I − M^{(κ)}_T)Y.
*Proof.* The objective is ‖Y‖² − 2φᵀZᵀY + φᵀ(G + κA/n)φ with G + κA/n ≻ 0. Completing the square gives the minimiser (G + κA/n)⁻¹ZᵀY and the value ‖Y‖² − YᵀM^{(κ)}Y. ∎

**P2 (spectral form).** M^{(κ)}_T = h_κ(Z_TZ_Tᵀ) with h_κ(λ) = nλ/((n+κ)λ + κ). Hence 0 ⪯ M^{(κ)}_T ⪯ (n/(n+κ))P_T. Moreover P_T − M^{(κ)}_T has eigenvalues κ(g+1)/((n+κ)g + κ) ∈ (0, 1] on col Z_T (g running over the nonzero eigenvalues of G_T) and vanishes on (col Z_T)^⊥.
*Proof.* For α ≥ 0, β > 0, (αZZᵀ + βI)Z = Z(αZᵀZ + βI), so Z(αG + βI)⁻¹ = (αZZᵀ + βI)⁻¹Z. With α = 1 + κ/n and β = κ/n this gives M^{(κ)} = (αZZᵀ + βI)⁻¹ZZᵀ = h_κ(ZZᵀ). h_κ is increasing, h_κ(0) = 0 and h_κ < n/(n+κ). The eigenvectors of ZZᵀ with nonzero eigenvalue span col Z, and those eigenvalues are the nonzero eigenvalues of G. ∎

**P3 (Woodbury and determinant).** (Σ^{(κ)}_T)⁻¹ = I − M^{(κ)}_T, Σ^{(κ)}_T ⪰ I, and D^{(κ)}_T = ∏_{i≤|T|}(1 + x_i/κ) with x_i := nλ_i/(λ_i + 1) ≥ 0, λ_i the eigenvalues of G_T. In particular D^{(1)}_T = ∏(1 + x_i) = D_T. With r_T := rank G_T and c ≥ 1:

  D^{(1/c)}_T ≤ c^{r_T}D_T  and  D_T ≤ c^{r_T}D^{(c)}_T.

*Proof.* Let B = (n/κ)A⁻¹ ≻ 0. Then
(I + ZBZᵀ)(I − Z(B⁻¹ + G)⁻¹Zᵀ) = I + Z[B − (I + BG)(B⁻¹ + G)⁻¹]Zᵀ = I,
because I + BG = B(B⁻¹ + G); and B⁻¹ + G = G + κA/n. Σ ⪰ I since ZBZᵀ ⪰ 0. By Sylvester's identity det(I_N + ZBZᵀ) = det(I_{|T|} + BG) = ∏(1 + (n/κ)λ_i/(λ_i+1)). For x ≥ 0 and c ≥ 1: 1 + cx ≤ c(1 + x) and 1 + x ≤ c(1 + x/c); factors with x_i = 0 equal 1 on both sides, so only the r_T nonzero eigenvalues cost a factor c. ∎

**P4 (order).** For S = S₀ ∪ J and c = 1 + η > 1: Σ₁ := Σ^{(1/c)}_S ⪰ Σ₀ := Σ^{(c)}_{S₀} ⪰ I.
*Proof.* By P3's Woodbury identity with B = I, Z_TA_T⁻¹Z_Tᵀ = I − (I + Z_TZ_Tᵀ)⁻¹. Since Z_SZ_Sᵀ = Z₀Z₀ᵀ + Z_JZ_Jᵀ ⪰ Z₀Z₀ᵀ, inversion reverses the Loewner order ([P1] preamble), so Z_SA_S⁻¹Z_Sᵀ ⪰ Z₀A₀⁻¹Z₀ᵀ ⪰ 0. Then
Σ₁ − Σ₀ = n(c − 1/c)Z_SA_S⁻¹Z_Sᵀ + (n/c)(Z_SA_S⁻¹Z_Sᵀ − Z₀A₀⁻¹Z₀ᵀ) ⪰ 0. ∎

By P3, D′ = M^{(1/c)}_S − M^{(c)}_{S₀} = Σ₀⁻¹ − Σ₁⁻¹.  (★)

## 2. Proof of (a)

*D′ ⪰ 0.* By (★) and P4, Σ₁ ⪰ Σ₀ ≻ 0 gives Σ₀⁻¹ ⪰ Σ₁⁻¹.

*‖D′‖ < 1.* 0 ⪯ D′ ⪯ M^{(1/c)}_S ⪯ (cn/(cn+1))P_S by P2, so ‖D′‖ = λ_max(D′) ≤ cn/(cn+1) < 1.

*Inequality (for every e ∈ ℝ^N).* For a positive semidefinite form ⟨·,·⟩_A and η > 0, expanding and using 2|⟨a,b⟩_A| ≤ η‖a‖²_A + ‖b‖²_A/η gives

 (Y1) ‖a + b‖²_A ≤ (1+η)‖a‖²_A + (1 + 1/η)‖b‖²_A;
 (Y2) ‖a + b‖²_A ≥ ‖a‖²_A/(1+η) − ‖b‖²_A/η.

(Y2 is Y1 applied to a = (a + b) + (−b), divided by 1 + η.)

Upper bound for Q^c_{S₀}: substitute φ = θ* + ψ in P1's minimum (κ = 1), use y_c − Z₀φ = e − Z₀ψ and (Y1) with a = ψ, b = θ*, A = A₀:

 Q^c_{S₀} = min_ψ{‖e − Z₀ψ‖² + ‖θ* + ψ‖²_{A₀}/n} ≤ min_ψ{‖e − Z₀ψ‖² + cψᵀA₀ψ/n} + (1 + 1/η)θ*ᵀA₀θ*/n = Q^{(c)}_{S₀}(e) + (1 + 1/η)ρ′.

Lower bound for Q^c_S: substitute φ = θ̃ + ψ, use y_c − Z_Sφ = e − Z_Sψ and (Y2) with a = ψ, b = θ̃, A = A_S:

 Q^c_S = min_ψ{‖e − Z_Sψ‖² + ‖θ̃ + ψ‖²_{A_S}/n} ≥ min_ψ{‖e − Z_Sψ‖² + ψᵀA_Sψ/(cn)} − θ̃ᵀA_Sθ̃/(ηn) = Q^{(1/c)}_S(e) − ρ′/η.

Here θ̃ᵀA_Sθ̃ = θ*ᵀA₀θ* = nρ′, because θ̃ is supported on S₀ and the S₀×S₀ block of A_S is A₀. Subtracting and applying P1:

 Q^c_{S₀} − Q^c_S ≤ eᵀ(M^{(1/c)}_S − M^{(c)}_{S₀})e + (1 + 2/η)ρ′ = eᵀD′e + (1 + 2/η)ρ′.

*Definition of ρ′.* ρ′ = θ*ᵀ(G_{S₀} + I)θ*/n = (‖Z₀θ*‖² + ‖θ*‖²)/n = (‖μ‖² + ‖θ*‖²)/n, since ‖μ_c‖ = ‖Uᵀμ‖ = ‖μ‖ (μ ∈ range C). So ρ′ ≤ M + M′ under (E), (C). For s₀ = 0, ρ′ = 0. ∎

## 3. Proof of (c)

Put R₀ := P_{S₀} − M^{(c)}_{S₀}. By P2, 0 ⪯ R₀ ⪯ P_{S₀}, with eigenvalues c(g+1)/((n+c)g + c) on col Z₀. By P2 again M^{(1/c)}_S ⪯ P_S, so

 D′ ⪯ P_S − M^{(c)}_{S₀} = (P_S − P_{S₀}) + R₀. ∎

(Since col Z₀ ⊆ col Z_S, P_S − P_{S₀} is a projection of rank d_J = rank Z_S − rank Z₀. Hence eᵀD′e ≤ ‖(P_S − P_{S₀})e‖² + ‖P_{S₀}e‖² with ‖(P_S − P_{S₀})e‖²/σ² ~ χ²_{d_J}, as REPORT §3 uses.)

## 4. Proof of (b) — expected marginal-likelihood ratio

Let g_Σ := N_N(·; 0, σ²Σ) for Σ ≻ 0. By (★), for every x:

 exp(xᵀD′x/(2σ²)) = exp(−xᵀΣ₁⁻¹x/(2σ²))/exp(−xᵀΣ₀⁻¹x/(2σ²)) = (det Σ₁/det Σ₀)^{1/2}·g_{Σ₁}(x)/g_{Σ₀}(x).

Since e ~ g_I,

 E exp(eᵀD′e/(2σ²)) = (D^{(1/c)}_S/D^{(c)}_{S₀})^{1/2}·𝓘,  𝓘 := ∫ g_I(x)g_{Σ₁}(x)/g_{Σ₀}(x) dx.  (4.1)

𝓘 is the expectation under pure noise of the ratio of the superset marginal likelihood (slab inflated by c) to the reference marginal likelihood (slab deflated by c).

**Claim: 𝓘 ≤ 1 whenever Σ₁ ⪰ Σ₀ ⪰ I** (true here by P4).

*Proof.* Let W := Σ₁ − Σ₀ ⪰ 0 and ξ ~ N(0, σ²W) (possibly degenerate), independent of ζ ~ N(0, σ²Σ₀). Then ζ + ξ ~ N(0, σ²Σ₁), and its density is x ↦ E_ξ g_{Σ₀}(x − ξ). Both this and g_{Σ₁} are continuous, so g_{Σ₁}(x) = E_ξ g_{Σ₀}(x − ξ) for every x. By Tonelli,

 𝓘 = E_ξ ∫ g_I(x)·g_{Σ₀}(x − ξ)/g_{Σ₀}(x) dx = E_ξ ∫ g_I(x) exp{(2ξᵀΣ₀⁻¹x − ξᵀΣ₀⁻¹ξ)/(2σ²)} dx.

By the Gaussian moment generating function, ∫ g_I(x)exp(aᵀx/σ²)dx = exp(‖a‖²/(2σ²)); take a = Σ₀⁻¹ξ:

 𝓘 = E_ξ exp{−ξᵀ(Σ₀⁻¹ − Σ₀⁻²)ξ/(2σ²)} ≤ 1,

because the eigenvalues of Σ₀ are ≥ 1, so Σ₀⁻² ⪯ Σ₀⁻¹. ∎

*Conclusion.* By (4.1), the claim and P3 (c = 1 + η ≥ 1):

 E[(D_{S₀}/D_S)^{1/2}exp(eᵀD′e/(2σ²))] ≤ (D_{S₀}/D^{(c)}_{S₀})^{1/2}(D^{(1/c)}_S/D_S)^{1/2} ≤ c^{(r_{S₀} + r_S)/2} ≤ (1+η)^{(s₀ + |S|)/2} = (1+η)^{s₀ + |J|/2}. ∎

## 5. Remarks

1. **Cross-check with A2.** Since 0 ⪯ D′ ≺ I, the left side of (4.1) equals det(I − D′)^{−1/2}, so §4 gives det(I − D′) ≥ D^{(c)}_{S₀}/D^{(1/c)}_S. This is A2's inequality, obtained here without the step det(I − D′) ≥ det(I − D′^{1/2}Σ₀D′^{1/2}). The slack is exactly 𝓘 = E_ξ exp{−ξᵀΣ₀⁻¹M^{(c)}_{S₀}ξ/(2σ²)}; for s₀ = 0 it is an equality, E exp(eᵀD′e/2σ²) = (D^{(1/c)}_S)^{1/2}.
2. **Rank form.** (b) holds with (1+η)^{(rank G_{S₀} + rank G_S)/2}, so exact duplicates in J cost no factor.
3. **Choice of representation.** (a) uses θ* only through μ_c = Z₀θ*. It holds for any ϑ ∈ ℝ^{S₀} with X_{S₀}ϑ = μ and ρ′(ϑ) = (‖μ‖² + ‖ϑ‖²)/n, which matters only when G_{S₀} is singular.
4. **Caveat for consumers (outside the card).** (b) is at exponent exactly 1/(2σ*²). Since ‖D′‖ can be as large as cn/(cn+1), E exp((1+ε)eᵀD′e/(2σ*²)) may be infinite for fixed ε > 0. The variance surcharge of Lemma X4 therefore has to be handled on the truncation event, as ROUTES §2 plans, and not by re-using (b) at an inflated exponent.

External facts used: push-through and Woodbury identities (verified inline), Sylvester's determinant identity det(I + AB) = det(I + BA), Loewner-order reversal under inversion ([P1] preamble), the Gaussian moment generating function, the sum of independent Gaussians, and Tonelli's theorem.

ATTEMPT V/V-b RESULT=PROVED GAPS=0
