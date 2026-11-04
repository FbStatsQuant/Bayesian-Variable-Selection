# STATEMENT — T04 (A3 = T4): Contraction without beta-min

Source: `Theory_architecture_v3\theorems\T04_A3_contraction.md` (SMC-BVS v3.0, 2026-10-19), read with `theorems\00_COMMON.md`. Wave 3, lead Claude Opus 5.5.

Statement status: **the original statement, unchanged.** The items below make its definitions, quantifiers and dependencies explicit. They are readings, not changes. T01 and T02 are unproved v3 results, so the one input taken from them enters as an explicit hypothesis (H-T02).

## 1. Setting and definitions

- **Data.** Raw data (X^r, y^r) with n ≥ 4, p ≥ 1, a fixed (deterministic) design X^r with no constant column. C = I − 11ᵀ/n. D_x = diag(raw column sample SDs). Standardised design X = C X^r D_x⁻¹, so ‖x_j‖² = n − 1. U ∈ ℝ^{n×(n−1)} is a fixed matrix with UᵀU = I and UUᵀ = C. Contrast data y_c = Uᵀy^r, contrast design X_c = UᵀX (so X = U X_c), and s_y² = ‖Cy^r‖²/(n−1) = ‖y_c‖²/(n−1).
- **Truth.** y^r = α*1 + X^rβ* + ε, with ε ~ N_n(0, σ*²I) and σ*² > 0 fixed. μ = CX^rβ* = Xθ*, θ* = D_xβ*, S₀ = supp β*, s₀ = |S₀|. P₀ is the law of ε.
- **Model quantities.** For S ⊆ [p] with k = |S|: G_S = X_SᵀX_S = (X_c)_Sᵀ(X_c)_S = (n−1)R_S, H_S = (n+1)G_S + I_k, D_S = det H_S / det(G_S + I_k). Ω = {S : |S| ≤ K} with K = min(p, ⌊n/2⌋). ν = 0.01 + n/2, b₀ = 0.01. The prior on S is ϖ(S) = w(|S|)/W_K on Ω, with w(k) = ½ / C(2p−1, k) (the BB(1, p) prior capped at K). π is the v3 posterior on Ω, as defined in 00_COMMON §1 (quoted here in full):
  - y = Cy^r/s_y;
  - z_S = X_Sᵀy;
  - Q_S = yᵀy − n z_SᵀH_S⁻¹z_S;
  - a₀ = b₀ = 0.01;
  - m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{−1/2}(2b₀ + Q_S)^{−ν};
  - F(S) = log[ϖ(S)m(S)], Z = Σ_Ω ϖ(S)m(S) and π(S) = e^{F(S)}/Z.

  Π(· | y) denotes π. (This definition was added after round-1 review finding CW-F1. It only copies 00_COMMON and does not change the statement.)
- **Π† (the joint contrast posterior).** Π†(· | y) is the posterior of (S, θ, v) in the contrast model
  - S ~ ϖ on Ω;
  - v ~ IG(0.51, b), with b := b₀ s_y² plugged in;
  - θ_S | v, S ~ N_{|S|}(0, n v (G_S + I)⁻¹), and θ_j = 0 for j ∉ S (zero-padded θ ∈ ℝ^p);
  - y_c | θ, v, S ~ N_{n−1}((X_c)_S θ_S, v I_{n−1}).

  By T01(i) this is the image of the v3 joint posterior of (S, β, σ²) under θ = s_yβ, v = s_y²σ². The proof uses Π† only through this definition. It shows directly that the S-marginal of Π† equals π.
- **Rates.** ℓ_n := log(p ∨ n); ε_{2,n}² = (s₀+1)ℓ_n²/n; ε_{1,n}² = (s₀+1)ℓ_n/n; d_* = s₀ + ⌈s₀(2A+1)⌉; m_n := m_n(½ log n) = ⌈(s₀ log(2p) + (s₀+1)(log n)/2 + ½ log n)/log 2⌉ (00_COMMON §1).

## 2. Assumptions

- **R1:** n → ∞, s₀ fixed, p = p_n ≤ n^A with a fixed A ≥ 1.
- **G:** the fixed design and Gaussian errors above.
- **R:** s₀ fixed; p ≤ n^A with A ≥ 1; ‖μ‖²/n ≤ M; λ_min(R_{S₀}) ≥ φ₀² > 0 (vacuous if s₀ = 0); eventually s₀ ≤ K.
- **SE** (only where stated): λ_min(R_T) ≥ φ₀² for every nonempty T ⊆ [p] with |T| ≤ min(p, m_n + s₀).
- **DX** (only for (iv)): every diagonal entry of D_x is ≥ d₋ > 0.
- **H-T02** (= T02(i), an explicit hypothesis because it is unproved): in R1 under G and R, Π(|S| > m_n(ω_n) | y) = O_{P₀}(e^{−ω_n}) for every deterministic ω_n → ∞ with ω_n = O(log n). It is used only with ω_n = ½ log n, in the form Π(|S| > m_n | y) → 0 in P₀-probability.
- No beta-min condition is assumed.

## 3. Conclusion

"→ 0" means convergence to 0 in P₀-probability as n → ∞. There is a constant C < ∞, depending only on (σ*², M, φ₀, A) (b₀ = 0.01 is fixed), such that, in R1 under G, R and H-T02:

- **(i) [fallback; secondary]** Π†(‖Xθ − μ‖²/n > C ε_{2,n}² | y) → 0.
- **(ii) Under SE in addition:**
  - Π(|S| > d_* | y) → 0;
  - Π†(‖Xθ − μ‖²/n > C ε_{1,n}² | y) → 0;
  - Π†(‖θ − θ*‖² > C ε_{1,n}²/φ₀² | y) → 0.
- **(iii)** For every deterministic sequence u_n → ∞: Π†(|v/σ*² − 1| > C[ε_n² + u_n/√n] | y) → 0. Here ε_n = ε_{2,n} under G, R, and ε_n = ε_{1,n} under SE in addition (the "applicable ε_n"). v is on the contrast scale.
- **(iv) Under SE and DX:** Π†(‖D_x⁻¹(θ − θ*)‖² > C ε_{1,n}²/(φ₀² d₋²) | y) → 0. This is the rate of (ii) multiplied by d₋⁻².

**Not claimed:** beta-min; out-of-sample, intercept-posterior or empirically centred random-design Hellinger results.
