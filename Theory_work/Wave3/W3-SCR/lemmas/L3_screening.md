# L3 — proofs of SCR-A, (A∞), SCR-A°, (A°∞), Corollaries A1 and A1°

Uses L1 (L1.1, L1.5, L1.5°, L1.7), L2 (witness t(S), E1, E2⁺, E4), CODE_CHECK (CC2-CC4), Lemma B (L4).
Notation of STATEMENT §1: r_n = r_n(q, x) = (2 log(2N_q) + 2x)^{1/2}, a_x = √(x/(n−1)), τ̄_n(x) = τ_n(1 + 2a_x).

## SCR-A
Let q ∈ {0, …, K−1}, x > 0 with MC(q, x): √Γ_n(q) > τ̄_n(x)√T_n + σ r_n. Put 𝓔_A := E1(q, x) ∩ E2⁺(x);
P(𝓔_Aᶜ) ≤ 3e^{-x} (L2).

**Claim.** On 𝓔_A, every S ⊆ [p] with |S| ≤ q and S ⊉ S₀ satisfies F(S ∪ t(S)) > F(S), and S ∪ t(S) ∈ 𝒩(S).

*Proof.* Fix such an S and write t = t(S) (L2); γ(t|S) = max_{t′∈S₀∖S}γ(t′|S) ≥ Γ_n(q). Since y_c = μ + Cε,
 x_tᵀR_Sy_c = x_tᵀR_Sμ + x_tᵀR_SCε,  |x_tᵀR_Sμ| = (γ(t|S)·a(t|S))^{1/2},
and on E1, |x_tᵀR_SCε| ≤ σ r_n a(t|S)^{1/2}. Dividing by a(t|S)^{1/2} > 0,
 g_{y_c}(t|S)^{1/2} ≥ √Γ_n(q) − σ r_n > τ̄_n(x)√T_n ≥ τ̂√T_n,
the middle inequality by MC (which also makes the left side positive), the last on E2⁺. So
g_y(t|S) = g_{y_c}(t|S)/τ̂² > T_n, and since |S| ≤ q ≤ K−1, L1.5 gives F(S∪t) > F(S). As |S| < K, the addition S∪t
belongs to the coded neighbourhood 𝒩(S). ∎

**Conclusion.** On 𝓔_A no S with |S| ≤ q, S ⊉ S₀ is LO; i.e. every LO model of size ≤ q contains S₀. Every C ∈ 𝒞 is
LO (CC2, CC3), and {`local_certified`} ⊆ 𝒪 ∩ {Ŝ ∈ 𝒞} (CC2). Therefore
 𝒪 ∩ {`local_certified`} ∩ {|Ŝ| ≤ q} ∩ {S₀ ⊄ Ŝ} ⊆ {∃ C ∈ 𝒞: |C| ≤ q, S₀ ⊄ C} ⊆ 𝓔_Aᶜ,
which has probability ≤ 3e^{-x}. On 𝓔_A the intersection of all certified models of size ≤ q contains S₀ (it is [p]
if there is none). EX-A is used only to identify the coded comparisons with comparisons of the exact F. ∎

## (A∞)
Assume ρ := liminf_n √Γ_n(q_n) / [τ_n√(2 log p + log n) + σ√(2 q_n log p)] > 1, q_n ∈ {0, …, K−1}, n → ∞, p ≥ 2.
Take x_n := √(log n) (so x_n → ∞, x_n = o(log n), a_{x_n} → 0). Then:
- T_n = (1 + 1/n)(2 log(2p−1) + log(n+1)) ≤ (1 + 1/n)(2 log p + log n + 2 log 2 + 1/n) = (2 log p + log n)(1 + o(1)),
  because 2 log p + log n → ∞; and τ̄_n(x_n) = τ_n(1 + o(1));
- N_q ≤ (p+1)^q (since C(p,k) ≤ p^k ≤ C(q,k)p^k for k ≤ q), and q log(p+1) ≤ q log p + q/p ≤ q log p + 1, so
  r_n(q_n, x_n) ≤ √(2 q_n log p) + √(2 log 2 + 2 + 2x_n) = √(2 q_n log p) + o(√(log n)).
Since σ ≤ τ_n and log n ≤ 2 log p + log n, the right side of MC(q_n, x_n) is at most
(1 + o(1))·τ_n√(2 log p + log n) + σ√(2 q_n log p) ≤ (1 + o(1))·[τ_n√(2 log p + log n) + σ√(2 q_n log p)], which is
< √Γ_n(q_n) for all large n because ρ > 1. SCR-A then gives probability ≤ 3e^{-x_n} → 0. ∎

## SCR-A°
Let q ∈ {0, …, K−1}, x > 0 with MC°(q, x): √Ψ_n(q) > √(T_n(1 + ϑ°_n)) + r_n, where
ϑ°_n = 2a_x + 2a_x² + r_n/√(n−1) + 1.02(n+1)τ̄_n(x)²/(n(n−1)σ²). Put 𝓔_A° := E1(q,x) ∩ E2⁺(x) ∩ E4(q,x);
P((𝓔_A°)ᶜ) ≤ 4e^{-x}. Recall (L2) that E2⁺ ⊆ {‖Cε‖² ≤ σ²(n−1)(1 + 2a_x + 2a_x²)} ∩ {τ̂ ≤ τ̄_n(x)}.

**Step 1 (the current residual is at the scale σ_S, uniformly).** On E2⁺ ∩ E4, for every S with |S| ≤ q:
 0.02τ̂² + q_S(y_c) ≤ 1.02τ̄_n(x)² + (n/(n+1))·(n−1)σ_S²·(1 + 2a_x + 2a_x² + r_n/√(n−1)).
*Proof.* By L1.1, q_S(y_c) = ‖y_c‖²/(n+1) + (n/(n+1))y_cᵀR_Sy_c, and ‖y_c‖² = (n−1)τ̂², so
0.02τ̂² + ‖y_c‖²/(n+1) ≤ 1.02τ̂² ≤ 1.02τ̄_n(x)² on E2⁺. Next, with y_c = μ + Cε, R_Sμ centred and R_S ⪯ I,
 y_cᵀR_Sy_c = m_S² + 2μᵀR_SCε + (Cε)ᵀR_S(Cε) ≤ m_S² + 2σ m_S r_n + σ²(n−1)(1 + 2a_x + 2a_x²)
on E4 ∩ E2⁺. Since m_S² + σ²(n−1) = (n−1)σ_S², σ² ≤ σ_S², and 2σ m_S = 2σ·(m_S/√(n−1))·√(n−1) ≤ σ_S²√(n−1) (AM–GM),
the right side is ≤ (n−1)σ_S²(1 + 2a_x + 2a_x² + r_n/√(n−1)). ∎

**Step 2.** On 𝓔_A°, fix S with |S| ≤ q, S ⊉ S₀ and t = t(S). As in SCR-A (E1), using σ ≤ σ_S and
γ(t|S)/σ_S² ≥ Ψ_n(q),
 g_{y_c}(t|S)^{1/2} ≥ γ(t|S)^{1/2} − σ r_n ≥ σ_S(√Ψ_n(q) − r_n) > σ_S√(T_n(1 + ϑ°_n)).
By Step 1, ρ̄_n(n−1) ≤ T_n (L1.5°), σ_S ≥ σ and the definition of ϑ°_n,
 ρ̄_n((n+1)/n)(0.02τ̂² + q_S(y_c)) ≤ ρ̄_n(n−1)σ_S²·[1 + 2a_x + 2a_x² + r_n/√(n−1) + 1.02(n+1)τ̄_n(x)²/(n(n−1)σ_S²)]
 ≤ T_nσ_S²(1 + ϑ°_n) < g_{y_c}(t|S).
L1.5° gives F(S∪t) > F(S), and S∪t ∈ 𝒩(S). The conclusion follows as for SCR-A. ∎

## (A°∞)
Assume q_n log p = o(n), ‖μ‖ = o(nσ), ρ° := liminf √Ψ_n(q_n)/[√(2 log p + log n) + √(2 q_n log p)] > 1. With
x_n = √(log n): a_{x_n} → 0; r_n(q_n, x_n)² ≤ 2q_n log p + 2 log 2 + 2 + 2x_n = o(n), so r_n/√(n−1) → 0;
τ̄_n² = (σ² + ‖μ‖²/(n−1))(1 + o(1)) = o(nσ²), so the last term of ϑ°_n → 0. Hence ϑ°_n → 0, and as in (A∞)
√(T_n(1 + ϑ°_n)) + r_n ≤ (1 + o(1))[√(2 log p + log n) + √(2 q_n log p)] < √Ψ_n(q_n) for large n. SCR-A° gives
probability ≤ 4e^{-x_n} → 0. ∎

## Corollary A1 (explicit constant)
Assume φ^d_n(q_n) ≥ κ > 0 (directional floor, L4; implied by φ^a_n(q_n) ≥ κ), θ_min ≥ b > 0, ‖θ*‖₁ ≤ M, with κ, b, M, σ fixed
(not depending on n), q_n ∈ {0, …, K−1}, and
(q_n + 1) log p + log n ≤ c₁n with c₁ := κ²b²/(200(M² + σ²)). Then (A∞) holds with ρ ≥ √2.

*Proof.* ‖θ*‖₂ ≤ ‖θ*‖₁ ≤ M and ‖μ‖ ≤ Σ_t|θ*_t|‖x_t‖ ≤ M√(n−1), so τ_n² ≤ M² + σ² =: τ_*². Let n be so large that
√(κ(n−1))·b ≥ 2M/√(n+1). By Lemma B2 in its directional form B2d (θ_min ≥ b, c_θ ≤ M/√(n+1)) and (n−1)² ≥ n²/4,
 Γ_n(q_n) ≥ (κ(n−1)/n)·(√(κ(n−1))·b/2)² = κ²b²(n−1)²/(4n) ≥ κ²b²n/16.
By (u+v)² ≤ 2u² + 2v² and σ ≤ τ_*,
 [τ_n√(2 log p + log n) + σ√(2 q_n log p)]² ≤ 2τ_*²(2(q_n+1) log p + log n) ≤ 4τ_*²c₁n.
Hence ρ² ≥ κ²b²/(64τ_*²c₁) = 200/64 > 2. ∎
For p ≤ n^A and q_n = o(n/log n) the condition holds for all large n.

## Corollary A1° (beta-min at the rate σ√(𝐋_n/n); no fixed bound on the total signal)
Assume φ^d_n(q_n) ≥ κ > 0, q_n ∈ {0, …, K−1}, 𝐋_n := (q_n+1) log p + log n = o(n), θ_min ≥ 16σκ^{-1}√(𝐋_n/n),
s₀𝐋_n ≤ κn/576, ‖θ*‖₂ ≤ ½√(κ(n²−1))θ_min, ‖μ‖ = o(nσ). Then (A°∞) holds with ρ° ≥ √2.

*Proof.* q_n log p ≤ 𝐋_n = o(n). The condition on ‖θ*‖₂ is √(κ(n−1))θ_min ≥ 2c_θ, so B2° applies with the lower
bound κ ≤ φ^d_n(q_n) (L4, B2° and B2d); hence, using u/(v+w) ≥ ½min(u/v, u/w) and (n−1)² ≥ n²/4,
 Ψ_n(q_n) ≥ ((n−1)²/n)·κ²θ_min²/(4σ² + 9κs₀θ_min²) ≥ (n/8)·min{κ²θ_min²/(4σ²), κ/(9s₀)} ≥ 8𝐋_n,
by the two displayed conditions (κ²θ_min²n/(32σ²) ≥ 8𝐋_n and κn/(72s₀) ≥ 8𝐋_n). On the other hand
[√(2 log p + log n) + √(2 q_n log p)]² ≤ 2(2(q_n+1) log p + log n) ≤ 4𝐋_n. So ρ°² ≥ 2. ∎
