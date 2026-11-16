# S-b-1
stop_reason: end_turn

# Card S, route S-b — direct proof with closed-form marginals and Stirling

**Result.** The route closes with no gaps and gives a slightly stronger statement than the card: n₀ = 3, every real t > 0 (no upper limit n^{1−κ₀}), no t/√n term, and constants independent of κ₀. The card's statement follows as a corollary.

**Notation.** τ := |T| (the card's t is kept for the tail level). N = n − 1, E′ := ‖e‖²/σ*², b₀ = 0.01, b = b₀s_y². R^T_m := Σ_{k=max(m+1,0)}^{K} q_k/w(τ), as in [W3P] §0. If the card's sum is read as running to p instead of K, R is larger, the hypothesis is stronger, and the result still applies. T and ϑ are deterministic, i.e. functions of the fixed design only and not of e.

## Theorem S♭

Assume ‖μ‖² ≤ nM with μ ∈ 1^⊥, T ∈ Ω, ϑ ∈ ℝ^T and B_T(ϑ) ≤ B. Put

- b₋ := b₀σ*²/2 and b₊ := b₀(3M + 4σ*²);
- c₁ := Γ(0.51)·200^{0.51}·(2π)^{−1/2}·exp{0.04 + 0.03M/σ*² + B/(2σ*²)}, so log c₁ ≈ 2.376 + 0.03M/σ*² + B/(2σ*²) > 0;
- C_S := max{log c₁, √(2B)/σ*}.

Then for every n ≥ 3, every real t > 0 and every integer m with

  log R^T_m + ½ log D_T + ½ log n + C_S(1 + √t) ≤ −2t,   (H)

we have

  P_e[ π(|S| > m) > e^{−t} ] ≤ 2e^{−t} + 3e^{−n/64}.

**Corollary (the card's statement).** Take C := max{C_S, 3}, c := 1/64, n₀ := 3. Since C[1 + √t + t/√n] ≥ C_S(1 + √t), the card's hypothesis implies (H), and 2e^{−t} + 3e^{−n/64} ≤ Ce^{−t} + Ce^{−cn}. One n₀ serves all t, and C, c depend on (σ*², M, B) only.

## Proof

If R^T_m = 0 then {S ∈ Ω : |S| > m} is empty and π(|S| > m) = 0. Assume R^T_m > 0.

**Step 0 (scale bracket, exponential probability).** Let 𝓑 := {σ*²/2 ≤ s_y² ≤ 3M + 4σ*²} = {b₋ ≤ b ≤ b₊}.

- *Upper side.* Ns_y² = ‖μ_c + e‖² ≤ 2‖μ‖² + 2‖e‖² ≤ 2nM + 2‖e‖², and n/N ≤ 3/2. So {E′ ≤ 2N} ⊆ {s_y² ≤ 3M + 4σ*²}. Chernoff with E e^{χ²_N/4} = 2^{N/2} gives P(E′ > 2N) ≤ (2/e)^{N/2} ≤ e^{−N/8}.
- *Lower side (n ≥ 4).* Let Π₁ be the orthogonal projection onto a line containing μ_c. Then ‖μ_c + e‖² ≥ ‖(I − Π₁)e‖² = σ*²χ²_d with d = N − 1 ≥ 2. So {s_y² < σ*²/2} ⊆ {χ²_d < (d+1)/2} ⊆ {χ²_d ≤ 3d/4}. Chernoff with E e^{−χ²_d/6} = (3/4)^{d/2} gives P(χ²_d ≤ 3d/4) ≤ exp{−d(½ log(4/3) − 1/8)} ≤ e^{−d/64}.

Hence for n ≥ 4, P(𝓑ᶜ) ≤ e^{−(n−1)/8} + e^{−(n−2)/64} ≤ 3e^{−n/64}. For n = 3 the bound 3e^{−3/64} > 1 is trivial. On 𝓑, s_y > 0 and π is well defined.

**Step 1 (reference bound on Q^c_T).** Put r_c := Uᵀ(μ − X_Tϑ). Both μ and X_Tϑ lie in 1^⊥, so ‖r_c‖² = ‖μ − X_Tϑ‖². Take φ = ϑ in the variational form of Q^c_T ([P1] `lem:slab`), using y_c − X_{c,T}ϑ = e + r_c and ϑᵀ(G_T + I)ϑ = ‖X_Tϑ‖² + ‖ϑ‖²:

  Q^c_T ≤ ‖e‖² + 2eᵀr_c + B_T(ϑ) ≤ σ*²E′ + B + 2eᵀr_c.   (1)

For T = ∅ this is an equality with r_c = μ_c. Let Z := eᵀr_c/σ*² ~ N(0, ‖r_c‖²/σ*²); its variance is at most B/σ*².

**Step 2 (numerator: a fixed-rate proper mixture).** For S ∈ Ω let

  g_S(x) := (2π)^{−N/2} b₋^{0.51} Γ(ν)/Γ(0.51) · D_S^{−1/2}(b₋ + xᵀ(I − M_S)x/2)^{−ν},  x ∈ ℝ^N.

This is m^c_{b₋}(S) of [P1] eq. (`eq:mc`), with ν = 0.51 + N/2. It is the marginal density of the data under a proper prior at the data-free rate b₋, so ∫g_S = 1 ([P1] `lem:num`). Let f₀ be the N_N(μ_c, σ*²I) density of y_c; it is positive everywhere. Define

  Θ := Σ_{S∈Ω, |S|>m} w(|S|) g_S(y_c) / (w(τ) R^T_m f₀(y_c)) ≥ 0.

Since Σ_{S∈Ω, |S|>m} w(|S|) = w(τ)R^T_m and E[g_S(y_c)/f₀(y_c)] = 1, we get EΘ = 1.

**Step 3 (deterministic inequality on 𝓑).** Since T ∈ Ω, 0 < π(T) ≤ 1, so π(|S| > m) ≤ Σ_{S∈Ω, |S|>m} π(S)/π(T). On 𝓑, b ∈ [b₋, b₊] and Q^c ≥ 0, so

  π(S)/π(T) = [w(|S|)/w(τ)] (D_T/D_S)^{1/2} [(b + Q^c_T/2)/(b + Q^c_S/2)]^ν
       ≤ [w(|S|)/w(τ)] D_T^{1/2} (b₊ + Q^c_T/2)^ν · D_S^{−1/2}(b₋ + Q^c_S/2)^{−ν}.

Substitute D_S^{−1/2}(b₋ + Q^c_S/2)^{−ν} = g_S(y_c)(2π)^{N/2}Γ(0.51)/(b₋^{0.51}Γ(ν)), sum over S, and use (2π)^{N/2}f₀(y_c) = σ*^{−N}e^{−E′/2}:

  π(|S| > m) ≤ R^T_m D_T^{1/2} Θ · Γ(0.51) b₋^{−0.51} · σ*^{−N} e^{−E′/2} (b₊ + Q^c_T/2)^ν / Γ(ν).   (2)

**Step 4 (Stirling; the route's step).** Put u := (b₊ + Q^c_T/2)/(νσ*²) > 0. With 2ν − N = 1.02,

  σ*^{−N} e^{−E′/2}(b₊ + Q^c_T/2)^ν/Γ(ν) = σ*^{1.02} · [(νu)^ν e^{−νu}/Γ(ν)] · e^{νu − E′/2}.

- Since ue^{1−u} ≤ 1, (νu)^ν e^{−νu} ≤ ν^ν e^{−ν}.
- Stirling's lower bound Γ(x) > √(2π) x^{x−1/2}e^{−x} for x > 0 (NIST DLMF 5.6.1; Whittaker–Watson §12.33) gives ν^νe^{−ν}/Γ(ν) ≤ √(ν/(2π)) ≤ √(n/(2π)), using ν = n/2 + 0.01 ≤ n.
- By (1), νu − E′/2 = b₊/σ*² + (Q^c_T − σ*²E′)/(2σ*²) ≤ b₊/σ*² + B/(2σ*²) + Z.
- b₋^{−0.51}σ*^{1.02} = 200^{0.51} and b₊/σ*² = 0.04 + 0.03M/σ*².

Inserting these in (2), on 𝓑:

  π(|S| > m) ≤ c₁ · R^T_m √(D_T) √n · Θ e^{Z}.   (3)

**Step 5 (tails).**
- Markov: P(Θ > e^t) ≤ e^{−t}.
- Gaussian tail: P(Z > √(2Bt)/σ*) ≤ e^{−t}; if r_c = 0 then Z = 0.
- Step 0: P(𝓑ᶜ) ≤ 3e^{−n/64}.

On the intersection of the three good events, (3) and (H) give

  log π(|S| > m) ≤ log R^T_m + ½ log D_T + ½ log n + log c₁ + (√(2B)/σ*)√t + t ≤ −2t + t = −t.

Hence P[π(|S| > m) > e^{−t}] ≤ 2e^{−t} + 3e^{−n/64}. ∎

## Remarks

1. **Difference from route S-a.** The closed form replaces the v-window of [P1] `lem:den`, so the term |E′ − N|/(2√n) + E′/(2n) of Λ″_n never appears. That term is the only source of the card's t/√n term and of the restriction t ≤ n^{1−κ₀}. Here the √t term comes only from the cross term eᵀr_c.
2. **Exact reference.** If μ = X_Tϑ then r_c = 0 and Z ≡ 0. Condition (H) can be replaced by log R^T_m + ½ log D_T + ½ log n + log c₁ ≤ −2t, and the probability bound becomes e^{−t} + 3e^{−n/64}.
3. **Uniformity.** The bound depends on (X, μ, T, ϑ, p) only through (M, B, σ*²). No p ≤ n^A, no eigenvalue condition and no restriction on model sizes up to K are used, because every g_S is a proper density even for singular G_S. For a random design with e independent of X and (T, ϑ) X-measurable, apply the theorem conditionally on X.
4. **Cutoff m_n(t) with T = S₀, ϑ = θ*, B = M + M′.** If m_n(t) = K the tail is 0. Otherwise R_m ≤ 2(2p)^{s₀}2^{−m} ([P1] `lem:prior`(c),(d)) and D_{S₀} ≤ (n+1)^{s₀} give log R + ½ log D + ½ log n ≤ log 2 − ½ log n − 3t. So (H) holds once C_S(1 + √t) + log 2 ≤ t + ½ log n, for instance for all t ≥ 1 when log n ≥ C_S² + 2C_S + 2 (using C_S√t ≤ t + C_S²/4). No lower restriction t ≥ log n is needed for n beyond that threshold.
5. **Stirling constant.** Only Γ(ν) ≥ c·ν^{ν−1/2}e^{−ν} with some absolute c > 0 is needed; a different c only changes c₁.

ATTEMPT S/S-b RESULT=PROVED GAPS=0
