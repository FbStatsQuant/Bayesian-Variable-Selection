# V-c-1
stop_reason: end_turn

# Card V, route V-c (adversarial): no counterexample — Lemma V holds as written, for every design

I attacked the statement in the regimes the route names (singular G_S, duplicated columns, s₀ = 0, |S| near or beyond K, near-singular G_{S₀}). Every attack fails for the same structural reason: nothing in the argument uses the rank of G_S or G_{S₀}, |S| ≤ K, or uniqueness of θ*. Section 1 gives the rank-free proof, which is the precise reason the attacks fail. Section 2 gives the explicit attacks with closed-form computations (hand-computed, no code run). Section 3 records what is false or sharp just outside the statement.

## 1. Why every attack fails: a rank-free proof

**Notation.** For T ⊆ [p] and κ > 0 put A_T := G_T + I ≻ 0 and q^{(κ)}_T(z) := min_{φ∈ℝ^T}{‖z − X_{c,T}φ‖² + κφᵀA_Tφ/n}. Since G_T + κA_T/n ≻ 0 for every T (singular G_T included), completing the square gives q^{(κ)}_T(z) = zᵀ(I − M^{(κ)}_T)z. Also M^{(1)}_T = M_T, Q^c_T = q^{(1)}_T(y_c), and M^{(κ)}_∅ = 0.

- **F1 (monotone in κ).** κ₁ ≤ κ₂ ⇒ q^{(κ₁)}_T ≤ q^{(κ₂)}_T pointwise ⇒ M^{(κ₁)}_T ⪰ M^{(κ₂)}_T.
- **F2 (nesting).** T ⊆ T′ ⇒ M^{(κ)}_T ⪯ M^{(κ)}_{T′}. Restrict the minimum over ℝ^{T′} to φ supported on T; A_T is a principal block of A_{T′}, so the penalty is unchanged.
- **F3 (spectrum).** By push-through, X f(XᵀX)Xᵀ = f(XXᵀ)XXᵀ, so M^{(κ)}_T = h_κ(X_{c,T}X_{c,T}ᵀ) with h_κ(λ) = nλ/(nλ + κ(λ+1)) ∈ [0, 1) and h_κ(0) = 0. With ξ := nλ/(λ+1) ∈ [0, n), h_κ = ξ/(ξ+κ). Hence 0 ⪯ M^{(κ)}_T ⪯ P_T and ‖M^{(κ)}_T‖ < 1.
- **F4 (determinants).** Σ^{(κ)}_T := (I − M^{(κ)}_T)⁻¹ exists, Σ^{(κ)}_T ⪰ I, with eigenvalues 1 + ξ_i/κ on the range of X_{c,T} and 1 elsewhere. The nonzero eigenvalues of X_{c,T}X_{c,T}ᵀ are those of G_T, so det Σ^{(κ)}_T = ∏_{i=1}^{|T|}(1 + ξ_i/κ) =: D^{(κ)}_T, with ξ_i = nλ_i(G_T)/(λ_i(G_T)+1). Zero eigenvalues contribute 1, and D^{(1)}_T = D_T ([P1] `lem:spec`(e)).

**(a).** D′ = M^{(1/c)}_S − M^{(c)}_{S₀} ⪰ M^{(c)}_S − M^{(c)}_{S₀} ⪰ 0 by F1 (1/c < c) and F2. Also D′ ⪯ M^{(1/c)}_S, so ‖D′‖ ≤ ‖M^{(1/c)}_S‖ < 1; quantitatively 1 − ‖D′‖ > 1/(cn+1).

Fix any e ∈ ℝ^N. For Q^c_{S₀}, substitute φ = θ* + φ′ and use X_{c,S₀}θ* = μ_c with Young's inequality (u+w)ᵀA(u+w) ≤ (1+η)uᵀAu + (1+1/η)wᵀAw:

Q^c_{S₀} ≤ min_{φ′}{‖e − X_{c,S₀}φ′‖² + cφ′ᵀA_{S₀}φ′/n} + (1+1/η)ρ′ = eᵀ(I − M^{(c)}_{S₀})e + (1+1/η)ρ′.

For Q^c_S, write φ = θ* + φ′ with θ* zero-padded, and use (u+w)ᵀA(u+w) ≥ uᵀAu/(1+η) − wᵀAw/η (the previous inequality applied to u = (u+w) − w). Since θ*ᵀA_Sθ* = θ*ᵀA_{S₀}θ* = ‖μ‖² + ‖θ*‖² = nρ′:

Q^c_S ≥ eᵀ(I − M^{(1/c)}_S)e − ρ′/η.

Subtracting gives (a), deterministically for every e.

**(b).** ‖D′‖ < 1 gives E exp(eᵀD′e/(2σ*²)) = det(I − D′)^{−1/2}. By F4, D′ = (Σ^{(c)}_{S₀})⁻¹ − (Σ^{(1/c)}_S)⁻¹. Write Σ₀ := Σ^{(c)}_{S₀}, Σ_S := Σ^{(1/c)}_S and B := D′^{1/2}Σ₀D′^{1/2}.

- B ⪰ D′ because Σ₀ ⪰ I.
- B has the spectrum of Σ₀^{1/2}D′Σ₀^{1/2} = I − Σ₀^{1/2}Σ_S⁻¹Σ₀^{1/2} ≺ I.
- So 0 ≺ I − B ⪯ I − D′, and det(I − D′) ≥ det(I − B) = det Σ₀/det Σ_S = D^{(c)}_{S₀}/D^{(1/c)}_S.
- Eigenvalue-wise, 1 + cξ ≤ c(1+ξ) and 1 + ξ ≤ c(1 + ξ/c), with equality at ξ = 0 only if the factor c is dropped. So D^{(1/c)}_S ≤ c^{rank X_S}D_S and D_{S₀} ≤ c^{rank X_{S₀}}D^{(c)}_{S₀}.

Therefore (D_{S₀}/D_S)^{1/2}det(I − D′)^{−1/2} ≤ c^{(rank X_S + rank X_{S₀})/2} ≤ (1+η)^{s₀+|J|/2}.

**(c).** By F3, M^{(1/c)}_S ⪯ P_S. Put R₀ := P_{S₀} − M^{(c)}_{S₀}; F3 gives 0 ⪯ R₀ ⪯ P_{S₀}. Then D′ ⪯ P_S − M^{(c)}_{S₀} = (P_S − P_{S₀}) + R₀. ∎

No step is a GAP. The only external facts are Young's inequality for a PSD form, det monotonicity on 0 ≺ A ⪯ B, and the Gaussian MGF of a quadratic form.

## 2. Explicit attacks, and where each dies

Write ξ(g) := ng/(g+1). Every design below is centred with ‖x_j‖² = N, built from orthonormal u, u₁, u₂ ∈ ℝ^N.

**Attack 1 — s₀ = 0, arbitrary J (singular G_J, duplicates, |J| > K or > N).** Here ρ′ = 0 and D′ = M^{(1/c)}_J, so everything is exact.

- (a): Q^c_∅ − Q^c_J − eᵀD′e = −Σ_i (c−1)ξ_i/((cξ_i+1)(ξ_i+1))·(u_iᵀe)² ≤ 0.
- (b): LHS = ∏_{i≤rank X_J}((1+cξ_i)/(1+ξ_i))^{1/2}, and each factor lies in (1, √c).
- j orthogonal columns: LHS = c^{j/2}(1 − η/(cn))^{j/2}, just below the bound.
- k exact copies of one column: LHS = ((1+cξ)/(1+ξ))^{1/2} < c^{1/2}, with ξ = nkN/(kN+1), against an allowed c^{k/2}.
- |J| > N: LHS < c^{N/2} < c^{|J|/2}.

No violation; duplicates only add slack.

**Attack 2 — J duplicates an S₀ column (rank gain 0).** S₀ = {1}, x₂ = x₁ = √N u, θ* = θ, ρ′ = θ². Then ξ₀ = N, ξ_S = 2nN/(2n−1), and D′ = d·uuᵀ with 1 − d = 1/(cξ_S+1) + N/(N+c).

- (a): Q^c_{S₀} − Q^c_S = δ(θ√N + uᵀe)² with δ = N/(n(2n²−1)). So sup_e[LHS − eᵀD′e] = θ²N/(1/δ − 1/d).
- (b): LHS² = (D_{S₀}/D_S)/(1−d).
- At n = 3, c = 2: δ = 2/51, d = 0.3276, sup = 0.089θ² against (1+2/η)ρ′ = 3θ²; LHS(b) = 1.146 against 2^{3/2} = 2.83.
- At c = 1: LHS(b)² = 1 − N²/(2n³−2n+1) < 1.

No violation.

**Attack 3 — near-singular G_{S₀}, weak direction boosted by J.** This is the most dangerous configuration (REPORT F3).

- Design: S₀ = {1,2}, x₁ = √N u₁, x₂ = √N(cos α·u₁ + sin α·u₂), J = {3}, x₃ = √N w₋ with w₋ = −sin(α/2)u₁ + cos(α/2)u₂.
- Spectrum: X₀X₀ᵀ has eigenvalues N(1+cos α) on w₊ and γ := N(1−cos α) on w₋. Adding x₃ changes only the w₋ eigenvalue, to γ + N, so everything commutes.
- Signal: μ_c = τw₋, θ* = (τ/(2√N sin(α/2)))(−1, 1), so s₀ = 2 and ρ′ = τ²/ξ₀ with ξ₀ = ξ(γ). Put ξ_S = ξ(γ+N).
- (a): with δ = ξ_S/(ξ_S+1) − ξ₀/(ξ₀+1) and d₋ = cξ_S/(cξ_S+1) − ξ₀/(ξ₀+c), sup_e[Q^c_{S₀} − Q^c_S − eᵀD′e] = τ²/(1/δ − 1/d₋). So (a) is equivalent here to 1/δ − 1/d₋ ≥ ξ₀η/(η+2).
- Numbers at n = 100, γ = 0.01, η = 10: ξ₀ = 0.9901, ξ_S = 99.0001, 1/δ = 2.0305, 1/d₋ = 1.0911, difference 0.9394 ≥ 0.8251. Equivalently sup = 1.0645τ² ≤ 1.212τ² = (1+2/η)ρ′.
- Limit ξ_S → ∞: the difference tends to ξ₀η/(1+η), so (a) holds with slack factor (2+η)/(1+η) ∈ (1, 2). This is the closest approach I found.
- (b) at the same numbers: LHS² = 1.1094 × 0.2384 = 0.264, LHS = 0.51, against 11^{2.5} ≈ 401.

No violation.

**Attack 4 — non-identifiable θ*.** S₀ = {1,2}, x₁ = x₂, θ* = (L, −L), so μ = 0, s₀ = 2, ρ′ = 2L²/n is arbitrary. The left side of (a) does not depend on L, and eᵀ(M_S − M_{S₀})e ≤ eᵀD′e already holds by F1. The statement is true but arbitrarily lossy. The proof of (a) works verbatim for any ϑ ∈ ℝ^{S₀} with X_{S₀}ϑ = μ, so ρ′ may be replaced by min_ϑ ϑᵀ(G_{S₀}+I)ϑ/n. This is not a defect of the statement.

**Attack 5 — |S| near K, S ∉ Ω, rank saturation.** The lemma never uses S ∈ Ω. If rank X_{c,S} = N then P_S = I and (c) reads D′ ⪯ (I − P_{S₀}) + R₀. Still ‖D′‖ ≤ max h_{1/c} < 1, since 1 − h_{1/c}(λ) = (λ+1)/(cnλ+λ+1) > 1/(cn+1). The MGF in (b) is finite, and the bound is only lossier because rank X_S ≤ N < |S|.

## 3. Boundary of validity (not counterexamples to the card)

1. **Sharper true form of (b).** The proof gives E[…] ≤ (1+η)^{rank X_{S₀} + d_J/2}, with d_J = rank X_S − rank X_{S₀}. The exponent |J|/2 cannot be lowered in general: Attack 1 with orthogonal J attains c^{j/2}(1 − η/(cn))^{j/2}. In the commuting designs of Attacks 2–3 the S₀-exponent actually needed is at most s₀/2; whether s₀ can be replaced by s₀/2 in general is not established here.

2. **The constant in (a).** Attack 3 with ξ_S → ∞ shows 1 + 2/η cannot be replaced by anything below 1 + 1/η. It is optimal within a factor (2+η)/(1+η) ≤ 2.

3. **False variant: ρ′ replaced by L_{S₀}.** In Attack 3 let α → 0. Then L_{S₀} = τ²/(1+ξ₀) → τ², but sup_e[Q^c_{S₀} − Q^c_S − eᵀD′e] → (1+1/η)Nτ². At n = 100, γ = 10⁻⁶, η = 1 the sup is ≈ 196τ² against L_{S₀} ≈ τ². So Lemma V(a) genuinely needs the coefficient cost (C) (or a reference ϑ with small ϑᵀ(G+I)ϑ/n). The remark in W3-DIST STATEMENT §0 that (C) is "used only through (L₀)" cannot be applied to Lemma V or to step X4 of Lemma X.

4. **False variant: (b) with a variance surcharge.** E exp((1+ε)eᵀD′e/(2σ*²)) = ∞ as soon as (1+ε)‖D′‖ ≥ 1. With s₀ = 0 and one column, ‖D′‖ = cN/(cN+1), so this happens for every ε ≥ 1/(cN). The surcharge ε_{n,t} ≫ 1/n of ROUTES X4 can therefore never be put inside the moment; it must be handled by truncation on the noise event, as ROUTES plans.

5. **(b) and (c) cannot be chained inside an expectation.** After (c), with R₀ ⪯ P_{S₀}, the factor exp(‖P_{S₀}e‖²/(2σ*²)) has infinite mean when rank X_{S₀} ≥ 1. Even the exact E exp(eᵀR₀e/(2σ*²)) = ∏(1 + c/ξ_i(G_{S₀}))^{1/2} is unbounded as ξ_i → 0.

ATTEMPT V/V-c RESULT=PROVED GAPS=0
