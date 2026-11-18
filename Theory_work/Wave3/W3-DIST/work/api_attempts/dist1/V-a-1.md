# V-a-1
stop_reason: end_turn

# Card V, route V-a — line-by-line verification of REPORT A2

**Verdict.** Lemma V is correct as stated on the card. A2's derivation is sound; the three places where it is terse are filled in below (flagged at the end). No eigenvalue condition is used anywhere, G_S may be singular, s₀ = 0 and J = ∅ are covered, and S need not lie in Ω.

## Notation and the exact ρ′

Write Z_T := X_{c,T} (so Z_TᵀZ_T = G_T), A_T := G_T + I ≻ 0, Z₀ := Z_{S₀}, A₀ := A_{S₀}, P₀ := P_{S₀}, j := |J|, |S| = s₀ + j. For γ > 0 and Y ∈ ℝ^N put

 Q^{(γ)}_T(Y) := min_{φ∈ℝ^T} { ‖Y − Z_Tφ‖² + (γ/n) φᵀA_Tφ },  M^{(γ)}_T := Z_T(G_T + (γ/n)A_T)⁻¹Z_Tᵀ.

For T = ∅: Q^{(γ)}_∅(Y) = ‖Y‖², M^{(γ)}_∅ = 0, D_∅ = 1.

**Definition of ρ′ (fixed).** ρ′ := θ*_{S₀}ᵀ(G_{S₀} + I)θ*_{S₀}/n. Since X_{S₀}θ*_{S₀} = Xθ* = μ, this gives ρ′ = (‖μ‖² + ‖θ*‖²)/n exactly, hence ρ′ ≤ M + M′ under (E), (C); ρ′ = 0 if s₀ = 0. Also μ_c = UᵀXθ* = Z₀θ*_{S₀} = Z_Sθ̃, where θ̃ ∈ ℝ^S is θ*_{S₀} zero-padded, and θ̃ᵀA_Sθ̃ = θ*_{S₀}ᵀA₀θ*_{S₀} = nρ′ because the S₀-block of A_S is A₀.

## Preliminary facts (all deterministic, any T ⊆ [p], γ > 0)

**(F1) Quadratic form.** Q^{(γ)}_T(Y) = Yᵀ(I − M^{(γ)}_T)Y.
The objective is YᵀY − 2φᵀZ_TᵀY + φᵀ(G_T + (γ/n)A_T)φ with positive definite Hessian; its minimiser is (G_T + (γ/n)A_T)⁻¹Z_TᵀY and the minimum is YᵀY − YᵀM^{(γ)}_TY. For γ = 1, G_T + A_T/n = H_T/n, so M^{(1)}_T = M_T and Q^{(1)}_T = Q^c_T (this is [P1] `lem:slab`).

**(F2) Spectrum.** M^{(γ)}_T = h_γ(Z_TZ_Tᵀ) with h_γ(λ) := nλ/((n+γ)λ + γ).
With α = 1 + γ/n, β = γ/n: Z_T(αG_T + βI) = (αZ_TZ_Tᵀ + βI)Z_T, so Z_T(αG_T + βI)⁻¹Z_Tᵀ = (αZ_TZ_Tᵀ + βI)⁻¹Z_TZ_Tᵀ (same argument as [P1] `lem:spec`(a)). h_γ is increasing, h_γ(0) = 0, and h_γ < n/(n+γ). The eigenvectors of Z_TZ_Tᵀ with positive eigenvalue span col Z_T. Hence

 0 ⪯ M^{(γ)}_T ⪯ (n/(n+γ))P_T ⪯ P_T.

**(F3) Monotone in γ.** For γ₁ ≤ γ₂ the objective at γ₁ is pointwise ≤ that at γ₂, so Q^{(γ₁)}_T ≤ Q^{(γ₂)}_T for every Y. By (F1), M^{(γ₁)}_T ⪰ M^{(γ₂)}_T.

**(F4) Monotone in T.** For T ⊆ T′, restrict the minimum defining Q^{(γ)}_{T′} to φ supported on T. Then Z_{T′}φ = Z_Tφ_T and φᵀA_{T′}φ = φ_TᵀA_Tφ_T, so Q^{(γ)}_{T′} ≤ Q^{(γ)}_T, i.e. M^{(γ)}_{T′} ⪰ M^{(γ)}_T.

**(F5) Woodbury and determinant.** Put Σ^{(γ)}_T := I_N + (n/γ)Z_TA_T⁻¹Z_Tᵀ ⪰ I. Then I − M^{(γ)}_T = (Σ^{(γ)}_T)⁻¹ and

 det Σ^{(γ)}_T = det((1 + n/γ)G_T + I)/det(G_T + I) =: D^{(γ)}_T,  D^{(1)}_T = D_T.

Proof: with B = (γ/n)A_T ≻ 0,
(I + Z_TB⁻¹Z_Tᵀ)(I − Z_T(B + G_T)⁻¹Z_Tᵀ) = I + Z_T[B⁻¹(B + G_T) − I − B⁻¹G_T](B + G_T)⁻¹Z_Tᵀ = I.
By Sylvester's identity det(I_N + (n/γ)Z_TA_T⁻¹Z_Tᵀ) = det(I + (n/γ)A_T⁻¹G_T) = det(A_T + (n/γ)G_T)/det A_T.

## (a) D′ ⪰ 0, ‖D′‖ < 1, and the split

*D′ ⪰ 0.* Since 1/c < c, (F3) then (F4) give M^{(1/c)}_S ⪰ M^{(c)}_S ⪰ M^{(c)}_{S₀}.

*‖D′‖ < 1.* 0 ⪯ D′ ⪯ M^{(1/c)}_S because M^{(c)}_{S₀} ⪰ 0. By (F2), ‖D′‖ ≤ ‖M^{(1/c)}_S‖ ≤ n/(n + 1/c) = cn/(cn + 1) < 1.

*Split.* For a PSD matrix A, vectors a, b and η > 0, from 2|aᵀAb| ≤ η aᵀAa + η⁻¹bᵀAb:

 (i) (a+b)ᵀA(a+b) ≤ (1+η)aᵀAa + (1+1/η)bᵀAb.

Applying (i) to a = (a+b) + (−b) and dividing by 1+η:

 (ii) (a+b)ᵀA(a+b) ≥ aᵀAa/(1+η) − bᵀAb/η.

Upper bound for S₀. Substitute φ = θ*_{S₀} + φ′. Since y_c − Z₀φ = e − Z₀φ′, (i) with A = A₀, a = φ′, b = θ*_{S₀} gives
 Q^c_{S₀} = min_{φ′}{‖e − Z₀φ′‖² + (θ*_{S₀}+φ′)ᵀA₀(θ*_{S₀}+φ′)/n}
  ≤ min_{φ′}{‖e − Z₀φ′‖² + (c/n)φ′ᵀA₀φ′} + (1+1/η)ρ′ = Q^{(c)}_{S₀}(e) + (1+1/η)ρ′.

Lower bound for S. Substitute φ = θ̃ + φ′. Since y_c − Z_Sφ = e − Z_Sφ′, (ii) with A = A_S, a = φ′, b = θ̃ gives
 Q^c_S ≥ min_{φ′}{‖e − Z_Sφ′‖² + (1/(cn))φ′ᵀA_Sφ′} − ρ′/η = Q^{(1/c)}_S(e) − ρ′/η.

Subtracting and using (F1): for every e ∈ ℝ^N,

 Q^c_{S₀} − Q^c_S ≤ eᵀ(M^{(1/c)}_S − M^{(c)}_{S₀})e + (1 + 2/η)ρ′ = eᵀD′e + (1 + 2/η)ρ′. ∎

For s₀ = 0 this reads ‖e‖² − Q^c_S ≤ eᵀM^{(1/c)}_Se, true by (F3).

## (b) Moment bound

Write Σ₀ := Σ^{(c)}_{S₀} ⪰ I and Σ_S := Σ^{(1/c)}_S. By (F5), D′ = Σ₀⁻¹ − Σ_S⁻¹.

*Step 1 (Gaussian MGF).* D′ is symmetric with eigenvalues d_i ∈ [0, 1). e/σ* ~ N(0, I_N) is rotation invariant and E e^{dz²/2} = (1−d)^{−1/2} for z ~ N(0,1), d < 1. Hence
 E exp(eᵀD′e/(2σ*²)) = ∏_i(1 − d_i)^{−1/2} = det(I − D′)^{−1/2}.

*Step 2 (determinant comparison).* Let B := D′^{1/2}Σ₀^{1/2}.
- BᵀB = Σ₀^{1/2}D′Σ₀^{1/2} = I − Σ₀^{1/2}Σ_S⁻¹Σ₀^{1/2}, so I − BᵀB = Σ₀^{1/2}Σ_S⁻¹Σ₀^{1/2} ≻ 0. All eigenvalues of BᵀB are therefore < 1.
- BBᵀ = D′^{1/2}Σ₀D′^{1/2} has the same eigenvalues as BᵀB (B is square), so I − BBᵀ ≻ 0.
- Σ₀ ⪰ I gives BBᵀ ⪰ D′, so 0 ≺ I − BBᵀ ⪯ I − D′.
- Monotonicity of eigenvalues (Courant–Fischer) and Sylvester give
 det(I − D′) ≥ det(I − BBᵀ) = det(I − BᵀB) = det Σ₀/det Σ_S = D^{(c)}_{S₀}/D^{(1/c)}_S.

So det(I − D′)^{−1/2} ≤ (D^{(1/c)}_S/D^{(c)}_{S₀})^{1/2}.

*Step 3 (eigenvalue-wise comparison with D_S, D_{S₀}).* For an eigenvalue g ≥ 0 of the Gram matrix:
- c[1 + (n+1)g] − [1 + (1 + cn)g] = (c − 1)(1 + g) ≥ 0, so D^{(1/c)}_S = ∏_i [1 + (1+cn)g_i]/(1+g_i) ≤ c^{|S|}D_S.
- c[1 + (1 + n/c)g] − [1 + (n+1)g] = (c − 1)(1 + g) ≥ 0, so D_{S₀} ≤ c^{s₀}D^{(c)}_{S₀}.

*Conclusion.* (D_{S₀}/D_S)^{1/2} det(I − D′)^{−1/2} ≤ (D_{S₀}/D^{(c)}_{S₀})^{1/2}(D^{(1/c)}_S/D_S)^{1/2} ≤ c^{(s₀+|S|)/2} = (1+η)^{s₀+j/2}. ∎

For s₀ = 0: D′ = M^{(1/c)}_S, det(I − D′) = 1/D^{(1/c)}_S, bound c^{j/2}.

## (c) Projection bound

Put R₀ := P₀ − M^{(c)}_{S₀}. By (F2), 0 ⪯ M^{(c)}_{S₀} ⪯ P₀, so 0 ⪯ R₀ ⪯ P₀. On col Z₀ its eigenvalues are 1 − h_c(g) = c(g+1)/(ng + c(g+1)) ∈ (0,1) for the positive eigenvalues g of G_{S₀}; R₀ = 0 off col Z₀. By (F2) again M^{(1/c)}_S ⪯ P_S, hence

 D′ ⪯ P_S − M^{(c)}_{S₀} = (P_S − P₀) + R₀. ∎

Consequence: col Z₀ ⊆ col Z_S, so P_S − P₀ is the orthogonal projection onto a subspace of dimension d_J = rank X_S − rank X_{S₀} (rank Z_T = rank G_T = rank X_T). Therefore eᵀD′e ≤ σ*²χ²_J + ‖P₀e‖² with χ²_J := ‖(P_S − P₀)e‖²/σ*² ~ χ²_{d_J} exactly.

## Audit of A2 against the above

- **(a):** correct. The lower inequality (ii) is derived above from (i). The identity θ*ᵀA_Sθ* = θ*ᵀA₀θ* = nρ′ holds because of zero-padding.
- **D′ ⪰ 0, eigenvalue formula g/(g + (g+1)/(cn)):** correct; it equals h_{1/c}(g).
- **(b):** correct. A2 omits that I − D′^{1/2}Σ₀D′^{1/2} ≻ 0, which the determinant monotonicity step needs; this is supplied in Step 2. A2's shorthand "1 + cx ≤ c(1+x), 1 + x ≤ c(1 + x/c)" is replaced by the two exact identities in Step 3, both with slack (c−1)(1+g).
- **(c):** correct. A2 writes the R₀ eigenvalues as "∈ (0,1]"; they are in (0,1), which is immaterial.
- **Remark (not needed for the card).** The proof of (a) uses θ* only through Z₀θ*_{S₀} = μ_c. So (a) holds with ρ′ replaced by (‖μ‖² + ‖ϑ‖²)/n for any ϑ ∈ ℝ^{S₀} with X_{S₀}ϑ = μ, e.g. the minimum-norm one when G_{S₀} is singular.

ATTEMPT V/V-a RESULT=PROVED GAPS=0
