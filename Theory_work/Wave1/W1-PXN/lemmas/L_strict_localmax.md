# (L) — S₀ is a strict local maximum: corrected addition step (repair of PROOF §8.3, PROOF.md:357-370)

Status: PROVED (by this seat); XF VERIFIED (R17: role in (L); R19: arithmetic) — v1, 2026-11-08, following statement-lock review R00 finding 8.
Only the "additions A = S₀ + l" bullet (PROOF.md:363-367) changes; the deletion/swap bullet is unchanged.

**Issue.** PROOF.md:365 bounds νx_l(1+2x_l) by (Z_l²/2)(1+o(1)) citing (E3), but (E3) only gives RSS_{S₀} ≥ nσ²/2,
which yields νx_l ≤ Z_l²(1+o(1)), i.e. a term ≈ 2 log p instead of log p, and then F(S₀+l) − F(S₀) ≤ log p − ½ log n + ...,
which does not → −∞ when p ≫ √n. The multiplicative "1+o(1)" also must be made additive after multiplication by log p.

**Corrected step.** Work on Ω_n ∩ 𝒵_n (PROOF.md:351, 357), 𝒵_n := {max_{l∉S₀} Z_l² ≤ 2 log p + 2 log log n}, with Lemma E
applied to 𝔉_n = {A : |A| ≤ s₀+2} (J = s₀+2, D = A(s₀+2)). Since μ ∈ span X_{S₀}, Λ_{S₀} = 0 and RSS_{S₀} = ‖Π^⊥_{S₀}ε‖²;
by (E5) (PROOF.md:172, proof at 198-199), |RSS_{S₀} − nσ²| ≤ C₂n^{2/3}, so for n ≥ n₀,
  RSS_{S₀} ≥ nσ²(1 − C₂n^{−1/3}/σ²) =: nσ²(1 − ε_n),  ε_n = O(n^{−1/3}).
With x_l := σ²Z_l²/RSS_{S₀}: x_l ≤ (2 log p + 2 log log n)/(n(1−ε_n)) ≤ 3A log n/n ≤ ¼ for n ≥ n₀ (p ≤ n^A). Using
−log(1−x) ≤ x + x² for x ≤ ½ (in fact ≤ x(1+2x) for x ≤ ¼ suffices) and ν = n/2 + 0.01:
  −ν log(1 − x_l) ≤ ν x_l (1 + x_l) ≤ (n/2 + 0.01) · Z_l²/(n(1−ε_n)) · (1 + 3A log n/n)
                 ≤ (Z_l²/2)(1 + 2ε_n)(1 + 3A log n/n)(1 + 0.02/n)      (ε_n ≤ ½)
                 ≤ (Z_l²/2) + (Z_l²/2)·κ_n,   κ_n := O(n^{−1/3} + (log n)/n).
On 𝒵_n, Z_l²/2 ≤ log p + log log n ≤ A log n + log log n, so the additive remainder is
(Z_l²/2)κ_n ≤ (A log n + log log n)·O(n^{−1/3}) = O(n^{−1/3} log n) = o(1) uniformly in l ∉ S₀ (fixed A).
By (E6) with A = S₀ + l, A′ = S₀ (|R_A − R_{A′}| ≤ 2κ_E):
  F(S₀+l) − F(S₀) ≤ log((s₀+1)/(2p−1−s₀)) − ½ log(n+1) + log p + log log n + 2κ_E + o(1)
                 ≤ log(s₀+1) + log(p/(2p−1−s₀)) − ½ log n + log log n + 2κ_E + o(1)
                 = −½ log n + log log n + O(1) → −∞,
uniformly in l ∉ S₀ (p/(2p−1−s₀) ≤ 1 for p ≥ s₀ + 1). Combined with the unchanged deletion/swap bullet, on Ω_n ∩ 𝒵_n no
feasible flip or swap of S₀ attains a score ≥ F(S₀) for n ≥ n₀: (L).

**Probability of 𝒵_n.** Given X, Z_l = ũ_lᵀε/σ ~ N(0,1) for each l ∉ S₀ (ũ_l the unit vector of Π^⊥_{S₀}x_l; defined a.s.).
With u_n² := 2 log p + 2 log log n (renamed from t_n, R30 #5) and the Mills bound P(|N| > u) ≤ 2φ(u)/u:
P(𝒵_nᶜ | X) ≤ p · 2e^{−log p − log log n}/(√(2π) u_n) = 2/(√(2π) u_n log n) → 0. (No independence across l is needed.)

**Where A enters.** x_l ≤ 3A log n/n; the remainder O(A n^{−1/3} log n); P(𝒵_nᶜ) does not depend on A.
