# O-SWAP: finite-n theory of the posterior misses (n = 200, p ∈ {500, 1000}, s₀ = 14)

Run: O-SWAP (Opus 5.5), branch `theory/O-SWAP`, 2026-11-02. Everything here is a **candidate**: not reviewed, not adopted.

## 1. Headline

<!--HEADLINE-->

## 2. Setting and notation

Notation is that of `Docs/Theory/theorems/00_COMMON.md`. We fix the design X (standardised, ‖x_j‖² = n − 1), the truth S₀ (s₀ = |S₀|), and the coefficients θ on the X scale. In the study θ = c·β, where β has the pattern (1.4, −1, 1.8, −1.2, 0.8, −1.6) cycled over the 14 truths, c ∈ {1, 0.5}, and the noise sd is σ = 1. We write ỹ = C y^r = μ + Cε with μ = X_{S₀}θ and ε ~ N(0, σ²I). All probabilities are **conditional on X** and are over ε.

F is invariant under y ↦ a·y except through the constant 2b₀ = 0.02. So we work on the raw contrast scale with b̃ := 2b₀ s_y². In every formula b̃ is replaced by its design-level value 2b₀ s̄_y², where s̄_y² = (‖μ‖² + (n − 1)σ²)/(n − 1). The resulting error in a log-score difference is at most ν·2b₀|s_y² − s̄_y²|/Q, which is below 10⁻³ nats here.

New symbols (all deterministic given X):

- For T ⊂ [p] and k ∉ T: r_{k|T} = (I − P_T)x_k. For a truth j, T_j := S₀ − j and r_j := r_{j|T_j}.
- For a swap pair (j, l): ρ_{jl} := cor(r_{j|T_j}, r_{l|T_j}), the partial correlation of x_j and x_l given the other truths.
- δ_j := θ_j‖r_j‖/σ = θ_j √((n−1)(1 − R²_{j|T_j}))/σ, the signal-to-noise of truth j given the other truths.
- Log determinant ratios use D_S = det H_S / det(G_S + I) exactly:
  - adding l: κ⁺_l := log(w(s₀)/w(s₀+1)) + ½ log(D_{S₀+l}/D_{S₀}) = log((2p−1−s₀)/(s₀+1)) + ½ log(D_{S₀+l}/D_{S₀});
  - dropping j: γ_j := log(w(s₀−1)/w(s₀)) + ½ log(D_{S₀}/D_{S₀−j}) = log((2p−s₀)/s₀) + ½ log(D_{S₀}/D_{S₀−j});
  - swapping j for l: κ_{jl} := ½ log(D_{S₀−j+l}/D_{S₀}). The size prior cancels exactly.
- λ := e^{κ/ν} for each κ, and ν = a₀ + n/2.
- Residual sums: E_A := ‖(I − P_A)ỹ‖², W_A := ‖P_A ỹ‖². The pseudo-observation terms are Ω₀ := E W_{S₀}/(n+1) + b̃ and Ω_j := E W_{T_j}/(n+1) + b̃, with ω = Ω/σ².
- **First-order (one-move) posterior-miss event:** L := {∃ S' ∈ 𝒩(S₀) : F(S') > F(S₀)}, where 𝒩(S₀) holds the p − s₀ adds, the s₀ drops and the s₀(p − s₀) swaps.

At c = 1, Ω₀/σ² ≈ ‖μ‖²/(n+1) ≈ 24; at c = 0.5 it is ≈ 6. The τ = 1 pseudo-observation in H_S = (n+1)G_S + I leaves a fraction 1/(n+1) of the fitted sum of squares in Q_S. This acts as an **SNR-dependent extra size penalty** (Prop. 2).

## 3. Statements and proofs

### Lemma 0 (projection approximation PA). PROVED.

Write G_S = VΛVᵀ and X_S = U Λ^{1/2} Vᵀ, where UᵀU = I and P_S = UUᵀ. Then

  Q_S = Q̃_S + η_S,  with Q̃_S := E_S + W_S/(n+1) and η_S = Σ_i n (u_iᵀỹ)² / ((n+1)((n+1)λ_i + 1)) ∈ [0, n W_S/((n+1)((n+1)λ_min(G_S)+1))].

*Proof.* n X_S H_S⁻¹ X_Sᵀ = U diag(nλ_i/((n+1)λ_i+1)) Uᵀ. Also n/(n+1) − nλ/((n+1)λ+1) = n/((n+1)((n+1)λ+1)), and ỹᵀỹ − (n/(n+1))W_S = E_S + W_S/(n+1). ∎

To first order, η_S ≈ ‖θ̂_S‖²·n/(n+1)², where θ̂_S is the OLS coefficient vector. The error it induces in a one-move log-score difference is ν(η_{S'} − η_{S₀})/Q ≈ (θ̂²_{in} − θ̂²_{out})/(2σ²(n−s₀)), which is O(10⁻³) nats in this study. Every analytic statement below is exact for the score with Q replaced by Q̃ (call it F̃). The conditional Monte Carlo of §4 uses the **exact** F, so the PA is checked empirically.

### Proposition 1 (within-size swap). PROVED under PA.

Fix a truth j and a null l. Set A := r_jᵀỹ/‖r_j‖ and B := r_{l|T_j}ᵀỹ/‖r_{l|T_j}‖. Then (A, B) ~ N(σ(δ_j, ρδ_j), σ²[[1, ρ],[ρ, 1]]) with ρ = ρ_{jl}. Let U = S₀ ∪ {l}, E_U ~ σ²χ²_{n−2−s₀}, and W_{T_j}. These three are mutually independent and independent of (A, B). Then

  {F̃(S₀ − j + l) > F̃(S₀)} = { (n/(n+1))(λ B² − A²) > (λ − 1)(E_U + ‖v‖² + W_{T_j}/(n+1) + b̃) },  where λ = e^{κ_{jl}/ν} and ‖v‖² = (A² − 2ρAB + B²)/(1 − ρ²).

In particular, when κ_{jl} = 0 (to first order κ_{jl} = O(1/n); see the remark),

  **P_swap(j, l) = Φ(−d₋)Φ(d₊) + Φ(d₋)Φ(−d₊),  d∓ := |δ_j| √((1 ∓ ρ)/2)**,

and Φ(−d₋)Φ(d₊) ≤ P_swap ≤ Φ(−d₋) + Φ(−d₊). For ρ > 0 and δ_j → ∞, P_swap ~ Φ(−d₋).

*Proof.*
1. ỹ − P_{T_j}ỹ lies in span(r_j) ⊕ span(r_l)^⊥-part ⊕ (I − P_U)ỹ. Because the components are orthogonal projections of an isotropic Gaussian, A, B, E_U and W_{T_j} have the stated joint law. The means are r_jᵀμ/‖r_j‖ = θ_j‖r_j‖ and r_{l|T}ᵀμ/‖r_{l|T}‖ = θ_j r_{l|T}ᵀr_j/‖r_{l|T}‖ = ρθ_j‖r_j‖, because (I − P_T)μ = θ_j r_j. μ ∈ span X_{S₀} ⊆ span X_U, so E_U is central.
2. Write P_U − P_T = projection onto span(r_j, r_l) =: v. Then Q̃_{T+k} = E_U + ‖v‖² − (n/(n+1))·(coordinate of k)² + W_T/(n+1), where the coordinate is A for k = j and B for k = l. Substituting into F̃(S') − F̃(S₀) = −κ_{jl} − ν log((Q̃_{S'} + b̃)/(Q̃_{S₀} + b̃)) gives the displayed event.
3. When λ = 1 the event is B² > A² ⇔ (B − A)(B + A) > 0. (B − A, B + A) is Gaussian with Cov = Var B − Var A = 0, so its two coordinates are independent. Their standardised means are −δ√((1−ρ)/2) and δ√((1+ρ)/2), which gives the closed form.
4. The bounds follow by dropping a non-negative term, and by the union bound on {B − A > 0} ∪ {B + A < 0}. ∎

The general-λ probability is computed exactly by a Gauss–Hermite integral over the s-coordinate and a closed-form interval in the d-coordinate (`scripts/analytic.py::p_swap`; it agrees with direct MC to 3 decimals in `scripts/test_analytic.py`). There E_U is replaced by its mean. The error this causes is at most |λ − 1|·σ²√(2(n−2−s₀)) ≈ 0.03σ².

*Remark (κ_{jl} is small but not negligible).* In this study |κ_{jl}| ≲ 0.3 nats. That moves P_swap by up to about 15 % relative (e.g. δ = 4, ρ = 0.85: 0.137 at λ = 1 versus 0.116 at λ = 1.002), so the predictions use the exact κ_{jl}.

*Margin link to W1-T37R.* The mean log-score gap is M_{jl} := E[A² − B²]/(2σ²) = δ_j²(1 − ρ²)/2 = (n−1)θ_j²(1 − R²_{j|T_j})(1 − ρ²)/(2σ²). This is T37R's margin, with the partial R² factor added. The miss probability is governed by d₋² = M_{jl}/(1 + ρ), not by M_{jl}: **P_swap ≈ Φ̄(√(M_{jl}/(1+ρ)))**.

### Proposition 2 (superset by one null). PROVED under PA.

For a null l, let u_l = r_{l|S₀}/‖r_{l|S₀}‖ and B_l := u_lᵀỹ. B_l ~ N(0, σ²) exactly, for every design and every θ. Let E := E_{S₀} ~ σ²χ²_{n−1−s₀}. Then

  {F̃(S₀ + l) > F̃(S₀)} = { B_l² / (E + Ω₀) > τ_l },  τ_l := (n+1)(1 − e^{−κ⁺_l/ν})/n.

Hence, with E' := E − B_l² ~ σ²χ²_{n−2−s₀} independent of B_l,

  **P_add(l) = P( χ²₁ (1 − λ_l/(n+1)) > (λ_l − 1)(χ²_{n−2−s₀} + ω₀) )**,  λ_l = e^{κ⁺_l/ν}.

Under the same PA, the union over nulls is exactly {max_l B_l²/τ_l > E + Ω₀}, where (B_l/σ)_l ~ N(0, Γ) with Γ_{ll'} = u_lᵀu_{l'}.

*Proof.* P_{S₀+l} = P_{S₀} + u_lu_lᵀ, so Q̃_{S₀+l} = E − B_l² + (W_{S₀} + B_l²)/(n+1) and Q̃_{S₀} = E + W_{S₀}/(n+1). The event Q̃_{S₀} + b̃ > λ(Q̃_{S₀+l} + b̃) rearranges to λ(n/(n+1))B_l² > (λ − 1)(E + Ω₀), which is the displayed event. Because u_l ⟂ span X_{S₀} ∋ μ, B_l is central. ∎

*Consequences.*
- (i) P_add(l) depends on the design only through κ⁺_l. For every l, κ⁺_l ≈ ½ log(n+1) + log((2p−1−s₀)/(s₀+1)), which is 6.83 at p = 500 and 7.54 at p = 1000. It depends on the signal only through ω₀ ≈ ‖μ‖²/((n+1)σ²).
- (ii) **The superset rate is essentially scenario-free.** For nearly orthogonal u_l, P(superset) ≈ 1 − (1 − q)^{p−s₀}, where q = P_add: 1.5–3.0 × 10⁻⁴ at p = 500 and 0.7–1.5 × 10⁻⁴ at p = 1000 (Cor. 2.1). Correlated nulls (S2–S6) lower the effective count.
- (iii) Lowering the SNR from c = 1 to c = 0.5 lowers ω₀ from ≈ 24 to ≈ 6. That lowers the effective χ²₁ threshold by about 9 % and raises q by about 2× (Cor. 2.1).

### Proposition 3 (subset: a truth dropped). PROVED under PA.

With A := r_jᵀỹ/‖r_j‖ ~ N(σδ_j, σ²), independent of E ~ σ²χ²_{n−1−s₀}, and Λ_j = e^{γ_j/ν},

  **P_drop(j) = E[ Φ(t − |δ_j|) − Φ(−t − |δ_j|) ]**, where t = √((Λ_j − 1)(χ²_{n−1−s₀} + ω_j)/(1 − Λ_j/(n+1))).

*Proof.* Q̃_{S₀−j} = E + A² + W_T/(n+1) and Q̃_{S₀} = E + W_T/(n+1) + A²/(n+1). The event Q̃_{S₀−j} + b̃ < Λ(Q̃_{S₀} + b̃) rearranges to A²(1 − Λ/(n+1)) < (Λ − 1)(E + Ω_j). ∎

The drop gain is γ_j ≈ ½ log(n+1) + log((2p−s₀)/s₀), which is 6.90 at p = 500 and 7.60 at p = 1000. So a truth is at risk when |δ_j| ≲ 3.6 + 2 = 5.6. At c = 0.5 the weakest truths have |θ| = 0.4 and |δ| ≈ 5.4–5.6: they sit right at the edge.

### Theorem 4 (first-order bracket). PROVED (exact F, no PA needed for the inequalities).

For every X and θ:

  max_e p_e ≤ P(L | X) ≤ P(S₀ ≠ S† | X), and P(L | X) ≤ Σ_e p_e,

where e runs over the one-move events and p_e = P(F(S') > F(S₀) | X).

*Proof.* On L, some S' ∈ Ω beats S₀ strictly, so S₀ is not the argmax (ties have probability 0). The other two inequalities are monotonicity and the union bound. ∎

The **predictor T1** is P̂_T1(X) = 1 − Π_e(1 − p_e): independence across events, with p_e from Props. 1–3 and the exact κ's. It is an approximation, not a theorem; its accuracy is reported in §4. The **lower bracket T1-lo** treats each cluster as perfectly dependent and the clusters as independent. The clusters are: the adds of the nulls in one generator group of 5; and, for each truth j, {drop_j} ∪ {swap_{jl} : all l}. The per-cell prediction is the average of P̂(X) over the 100 actual study designs of that cell.

### Proposition 5 (the swap ceiling is information-theoretic). PROVED (standard two-point bound).

Fix (j, l) and let μ' := P_{S₀−j+l} μ be the closest mean supported on S' = S₀ − j + l. Then ‖μ − μ'‖ = σ|δ_j|√(1 − ρ²), and for **any** selector Ŝ (any prior, any method),

  ½[P_μ(Ŝ ≠ S₀) + P_{μ'}(Ŝ ≠ S')] ≥ Φ(−|δ_j|√(1 − ρ²)/2).

The HPM's own swap error is P_swap ≈ Φ(−|δ_j|√((1−ρ)/2)). The squared exponents differ by a factor (1 + ρ)/2, which tends to 1 as ρ → 1.

*Proof.* (I − P_{S'})μ = θ_j(I − P_{S'})x_j and ‖(I − P_{S'})r_j‖² = ‖r_j‖²(1 − ρ²). The rest is Le Cam's two-point bound for N(μ, σ²I) against N(μ', σ²I), whose minimal sum of errors is 2Φ(−‖μ − μ'‖/(2σ)). ∎

*Connection to T07.* Prop. 1 contains no size-prior term: the size prior cancels exactly in a within-size swap. This is T07's Prop. 1 in quantitative form. The swap probability also changes with g only through κ_{jl} = O(1/n). Prop. 5 says more: for look-alikes (ρ ≈ 0.85, as in S4), no method can push the averaged swap error much below the HPM's. The numbers are δ = 5.4, ρ = 0.85: the HPM gives Φ(−1.49) = 0.068 and the two-point bound gives Φ(−1.43) = 0.076.

<!--RESULTS-->
