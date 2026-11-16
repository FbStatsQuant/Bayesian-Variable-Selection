# STATEMENT — T01 (A0 = T1, contrast reduction and mixed-rate transfer) and T02 (A1 = T2, dimension control and strict supersets)

Status: precise statement for the proof run (wave 3); approved by the statement checker (Opus 5.5 xhigh), review/STATEMENT_CHECK_R2.md. Source files: `theorems/T01_A0_contrast_reduction.md`, `theorems/T02_A1_dimension_supersets.md`, read with `theorems/00_COMMON.md`. Method: SMC-BVS v3.0 (SHA-256 93043758…8019c), §§4–5. The readings that make informal clauses precise are listed in §4 with their reasons; they were submitted to the statement checker (review/STATEMENT_CHECK_*.md).

## 1. Setting

**Valid input.** Raw data X^r ∈ ℝ^{n×p}, y^r ∈ ℝ^n with n ≥ 3, p ≥ 1, no constant column of X^r, y^r not constant. C = I_n − 11ᵀ/n. D_x = diag(sample SDs of the columns of X^r, denominator n−1), X = CX^rD_x⁻¹, s_y² = ‖Cy^r‖²/(n−1) > 0, y = Cy^r/s_y; so ‖x_j‖² = ‖y‖² = n−1. U ∈ ℝ^{n×(n−1)} is a fixed (non-random; it may depend on n only) matrix with UᵀU = I_{n−1}, UUᵀ = C. Contrast data: y_c = Uᵀy^r ∈ ℝ^{n−1}, X_c = UᵀX ∈ ℝ^{(n−1)×p}.

**Target (method §5).** K = min(p, ⌊n/2⌋), Ω = {S ⊆ [p] : |S| ≤ K}. For S ∈ Ω, k = |S|: G_S = X_SᵀX_S = (n−1)R_S, z_S = X_Sᵀy, H_S = (n+1)G_S + I_k, D_S = det H_S / det(G_S + I_k), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S (D_∅ = 1, Q_∅ = yᵀy), a₀ = b₀ = 0.01, ν = a₀ + n/2,
m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{−1/2}(2b₀ + Q_S)^{−ν};
w(k) = ½/C(2p−1, k), W_K = Σ_{k≤K} C(p,k)w(k), ϖ(S) = w(|S|)/W_K; Z = Σ_Ω ϖ(S)m(S); π(S) = Π(S | y) = ϖ(S)m(S)/Z; BF(S) = m(S)/m(∅).
The v3 joint posterior of (S, β_S, σ²) is the posterior of the working model
y | β_S, σ², S ~ N_n(X_Sβ_S, σ²I_n), β_S | σ², S ~ N_k(0, nσ²(G_S+I_k)⁻¹), σ² ~ IG(a₀, b₀), S ~ ϖ on Ω,
evaluated at the standardised y (its S-marginal is π). The **joint transformed posterior** is its image under the bijection (S, β_S, σ²) ↦ (S, θ_S, v) = (S, s_yβ_S, s_y²σ²).

**Contrast model at rate b > 0** (fixed, i.e. not a function of the data, unless stated). For S ∈ Ω:
y_c | θ_S, v, S ~ N_{n−1}(X_{c,S}θ_S, vI_{n−1}), θ_S | v, S ~ N_k(0, nv(G_S+I_k)⁻¹), v ~ IG(0.51, b), S ~ ϖ.
(Note X_{c,S}ᵀX_{c,S} = G_S.) m^c_b(S) := the marginal density of y_c under model S at rate b. z_S^c = X_{c,S}ᵀy_c, Q_S^c = y_cᵀy_c − n (z_S^c)ᵀH_S⁻¹z_S^c. For a measurable parameter event E ⊆ ⋃_{S∈Ω} {S} × ℝ^S × (0,∞) with sections E_S:
I_b(E) := Σ_{S∈Ω} ϖ(S) ∫∫_{E_S} N_{n−1}(y_c; X_{c,S}θ, vI) N_k(θ; 0, nv(G_S+I)⁻¹) IG(v; 0.51, b) dθ dv,
Z^c_b := I_b(everything) = Σ_Ω ϖ(S)m^c_b(S), Π_b(E) := I_b(E)/Z^c_b (the contrast-model posterior at rate b).

**Statistical model (for probabilistic parts).** Fixed design; y^r = α*1 + X^rβ* + ε, ε ~ N_n(0, σ*²I_n), σ*² > 0 fixed, α* ∈ ℝ arbitrary; μ = CX^rβ* = Xθ*, θ* = D_xβ*, S₀ = supp β*, s₀ = |S₀|. P₀, E₀ are over ε. Assumption **G** is this model. Assumption **R**: s₀ fixed; p ≤ n^A with A ≥ 1 fixed; ‖μ‖²/n ≤ M (fixed M ≥ 0); λ_min(R_{S₀}) ≥ φ₀² > 0 (void if s₀ = 0); s₀ ≤ K for all large n. Regime **R1**: n → ∞, s₀ fixed, p ≤ n^A. Assumption **SE**: λ_min(R_T) ≥ φ₀² for every nonempty T with |T| ≤ min(p, m_n + s₀), where m_n = m_n(½ log n).
r_n = √(log n / n); m_n(ω) = ⌈(s₀ log(2p) + (s₀+1)(log n)/2 + ω)/log 2⌉.

**Scale event and envelope rates.** b₋ := b₀σ*²/2, b₊ := b₀(2(σ*²+M)+1), κ := (b₊/b₋)^{0.51} (constants, not depending on n or the data). 𝓑_n := {σ*²/2 ≤ s_y² ≤ 2(σ*²+M)+1} = {b₋ ≤ b₀s_y² ≤ b₊}.

## 2. T01

**(i) [identity; every valid input, deterministic].** The joint transformed posterior of (S, θ_S, v) equals Π_{b₀s_y²}, the posterior of the contrast model at rate b = b₀s_y² (the rate evaluated at the observed s_y), and for every S ∈ Ω
m(S) = c_n(s_y) · m^c_{b₀s_y²}(S),  c_n(s) = s^{n−1}Γ(0.51)/(√(2πb₀)Γ(0.01)).
Hence BF(S) = m^c_{b₀s_y²}(S)/m^c_{b₀s_y²}(∅), π(S) = ϖ(S)m^c_{b₀s_y²}(S)/Z^c_{b₀s_y²}, and Z = c_n(s_y) Z^c_{b₀s_y²}. Moreover z_S^c = s_y z_S, Q_S^c = s_y²Q_S, and under the joint transformed posterior
v | S, y ~ IG(ν, b₀s_y² + Q_S^c/2),  θ_S | v, S, y ~ N_k(nH_S⁻¹z_S^c, nvH_S⁻¹).

**(ii) [envelope; deterministic].** Let 0 < b₁ ≤ b ≤ b₂ be any numbers and κ₁₂ = (b₂/b₁)^{0.51}. For every S ∈ Ω and every y_c ∈ ℝ^{n−1}:
κ₁₂⁻¹m^c_{b₂}(S) ≤ m^c_b(S) ≤ κ₁₂ m^c_{b₁}(S).
For every measurable parameter event E: κ₁₂⁻¹I_{b₂}(E) ≤ I_b(E) ≤ κ₁₂ I_{b₁}(E); consequently Π_b(E) ≤ κ₁₂² I_{b₁}(E)/Z^c_{b₂}. (The original writes b₋, b₊, κ here; the letters are changed only because b₋, b₊, κ denote the specific constants of §1 elsewhere. With b₁ = b₋, b₂ = b₊ one has κ₁₂ = κ.)

**(iii) [scale event].** Under G and R: s_y² − (σ*² + ‖μ‖²/(n−1)) = O_{P₀}(n^{−1/2}) and P₀(𝓑_n) → 1. Also ε_c := Uᵀε ~ N_{n−1}(0, σ*²I_{n−1}) exactly, and y_c = X_cθ* + ε_c.

**(iv) [rate derivative; fixed contrast data].** For S, S′ ∈ Ω and b > 0:
∂_b log[m^c_b(S)/m^c_b(S′)] = 2ν(Q_S^c − Q_{S′}^c)/((2b + Q_S^c)(2b + Q_{S′}^c)).

**(T) [transfer rule].**
(a) *Mixed-endpoint transfer.* With b₋, b₊, κ, 𝓑_n as in §1: on 𝓑_n, for every measurable parameter event E,
Π(E | y) ≤ κ² I_{b₋}(E)/Z^c_{b₊} ≤ κ² I_{b₋}(E)/(ϖ(S₀) m^c_{b₊}(S₀))
(the last step when S₀ ∈ Ω), where Π(· | y) is the joint transformed v3 posterior and the right-hand sides are computed from y_c at the fixed rates b₋ (numerator) and b₊ (denominator). Consequently, under G and R, if I_{b₋}(E_n)/Z^c_{b₊} ≤ ε_n with P₀-probability → 1 (resp. = O_{P₀}(ε_n)), then Π(E_n | y) ≤ κ²ε_n with P₀-probability → 1 (resp. = O_{P₀}(ε_n)).
(b) *Same-rate bounds do not transfer (a worst case over inputs, not a statement about P₀).*
(b1) For any fixed rates 0 < r₁ < r₂ there are valid inputs (n → ∞, p = 1) with Π_{r₁}({S = {1}}) → 1 and Π_{r₂}({S = {1}}) → 0 (so Π_{r₁}({S = ∅}) → 0 and Π_{r₂}({S = ∅}) → 1). Hence, for distinct fixed rates b ≠ b′, there is no function g with g(x) → 0 as x ↓ 0, independent of n and the data, such that Π_{b′}(E) ≤ g(Π_b(E)) for all valid inputs and all events E. (Its inputs have s_y² → 0, so they lie outside 𝓑_n for large n; (b2) is the version on 𝓑_n.)
(b2) Fix any σ*² > 0 and M ≥ 0 (hence b₋, b₊), and any s² with σ*²/2 < s² < 2(σ*²+M)+1. There are valid inputs with p = 2 and s_y² = s² for every n ≥ 4 (so 𝓑_n holds for every n) such that, for E = {S = {1}}, Π_{b₋}(E) → 0 while Π(E | y) → 1 as n → ∞; and there are valid inputs with the same properties such that, for E′ = {S = {1,2}}, Π_{b₊}(E′) → 0 while Π(E′ | y) → 1. Hence, for b ∈ {b₋, b₊}, there is no constant C, independent of n and of the data, such that Π(E | y) ≤ C·Π_b(E) for all valid inputs in 𝓑_n and all events E.
(Proof discipline, not a mathematical claim: the proofs never treat ε or ε_c as N(0, σ*²I) conditionally on s_y or on 𝓑_n.)

## 3. T02

In regime R1, under G and R.

**(i)** For every n and every deterministic integer m (possibly depending on n), define Θ_{n,m} ≥ 0 by
Π(|S| > m | y) = 2^{−m}(2p)^{s₀}(n+1)^{s₀/2}√n · Θ_{n,m}.
Then lim_{L→∞} limsup_{n→∞} sup_{m} P₀(Θ_{n,m} > L) = 0. Consequently, for every deterministic sequence ω_n → ∞ with ω_n = O(log n): Π(|S| > m_n(ω_n) | y) = O_{P₀}(e^{−ω_n}). No eigenvalue condition beyond λ_min(R_{S₀}) ≥ φ₀² is imposed; a tight sup_m Θ_{n,m} (inside the probability) is not claimed.

**(ii)** Under SE in addition: Π({S ∈ Ω : S ⊋ S₀} | y) = O_{P₀}(r_n).

## 4. Readings (precisions of informal clauses) and reasons

1. **(iv)**: the comparison model is written S′ instead of R (R is the assumption bundle). Renaming only.
2. **"Joint transformed posterior"** = image of the v3 working-model posterior of (S, β_S, σ²) under (β_S, σ²) ↦ (s_yβ_S, s_y²σ²); U is any fixed (non-random) orthonormal basis of 1^⊥ (all statements hold for each such U; see reading 7).
3. **"The event of (iii)"** = 𝓑_n with the endpoints of (iii); b₋, b₊ = b₀ × endpoints; κ is then a fixed constant.
4. **Transfer rule** stated as (T)(a)–(b). (a) is the positive content ("holds at cost κ² in the mixed-endpoint form"). (b) is the negative content ("same-rate bounds alone do not establish it"), stated as a worst case over inputs: (b1) no data-free implication between bounds at two different fixed rates; (b2) witnesses inside 𝓑_n showing that a same-rate bound at b₋ or at b₊ does not bound the v3 posterior by any constant factor. A data-free factor growing with n, such as (b₊/b₋)^ν, does bound it (checker's note E6); (b) does not claim otherwise. "Errors are never treated as Gaussian conditional on s_y" is recorded as a discipline on the proofs.
5. **T02(i)**: Θ_{n,m} is defined by the displayed equality, so the content is the tightness, uniform in m (sup_m outside P₀). m ranges over all integers; S₀ ∈ Ω is required only for large n (from R).
6. **T02(ii)**: m_n in SE is m_n(½ log n), as fixed in 00_COMMON §1. Π(S ⊋ S₀ | y) is the π-mass of the strict supersets of S₀ in Ω.
7. **U** is fixed (non-random): with a data-dependent U the exact law of Uᵀε in (iii) can fail (checker's example). The objects in (i), (ii), (iv), (T) do not depend on U.
8. **Contrast quantities**: z^c_S = X_{c,S}ᵀy_c and Q^c_S are defined directly from y_c (so (ii) and (iv) make sense for every y_c ∈ ℝ^{n−1}); the identities z^c_S = s_y z_S, Q^c_S = s_y²Q_S of the original are proved as part of (i).
9. (iii) also states y_c = X_cθ* + ε_c (a true identity, used later). In R, λ_min(R_{S₀}) ≥ φ₀² is void when s₀ = 0. Valid input includes p ≥ 1 (the method's invalid/no_predictors statuses cover p = 0). "No eigenvalue condition near the cap" is written as "no eigenvalue condition beyond λ_min(R_{S₀}) ≥ φ₀²".
10. **(T)(b)** is a worst case over inputs. Under G and R a P₀-version of the negative clause would be false for model events (the checker's P0 sketch, review/STATEMENT_CHECK_R1b.md); (b) does not claim it.
