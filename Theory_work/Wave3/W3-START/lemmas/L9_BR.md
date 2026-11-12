# L9 — Gaussian-row bridge (B-R) and Theorem START-R (T3)(b)

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Statement proved: `STATEMENT.md` §5.2 (B-R) and §5.3 (T3)(b). Uses `lemmas/L3_LEAK.md` (Lemma J: (J3)),
`lemmas/L6_COROLLARIES.md` (Corollary L6.0′), `lemmas/L8_TRANSFER.md` (Proposition L8.2). No registry claim is consumed;
`Theory_work/Wave3/W3-RM/lemmas/L3_SANDR.md` (status "PROVED (by this seat, unchecked)") was read as a source of the
route (covariance event, localisation, conditioning on the reference columns) and nothing is imported from it.
The whole bridge is a statement about the design: the noise ε does not appear before §L9.7.

## L9.0 Setting, constants

Setting R (`STATEMENT.md` §1): raw rows iid N(m_n, Σ_n), Σ = Σ_n unit-diagonal; W_j ∈ ℝⁿ the j-th raw column; N := n − 1;
t_j := ‖CW_j‖/√N; x_j = CW_j/t_j; R̂ := XᵀX/N (sample correlation matrix); Ŝ := (CW)ᵀ(CW)/N; θ* deterministic,
|θ*_j| ∈ [θ_lo, θ_hi] on S₀, s₀ ≥ 1 fixed, μ = Xθ*; p ≤ n^A. Hypotheses: (FL-R16) λ_min(Σ_S) ≥ c_Σ for |S| ≤ 16 + s₀;
(V-R) with a_V; (L-R) with Q, (H_l)_{l∉Q}, C_L, r_n (r_n(n log n)^{1/4} → 0), κ_Q.
Constants (depending only on the fixed constants): M := s₀²θ_hi²; Δ_hi := s₀²θ_hi²; Δ_lo := (c_Σ/2)θ_lo²;
a̲ := σ²/(σ² + Δ_hi), ā := σ²/(σ² + Δ_lo) < 1; C_S := 1 + 45/c_Σ + 450/c_Σ²; z̄_n² := 2 log(2^{21}) + 2A log n + 2 log log n ≥ z_n².
For an index set U and j, k ∉ U, and a symmetric matrix M: pc(M; j, k | U) := M_jk − M_{jU}M_U⁻¹M_{Uk} (:= M_jk if U = ∅).
Facts: pc(Σ; j, k | U) = Cov(W_j, W_k | W_U) (Gaussian rows); pc(R̂; j, k | U) = N⁻¹x_jᵀ(I − P_U)x_k.
"For n large" below always means n ≥ a threshold depending only on the fixed constants and on the sequence r_n.

## L9.1 The covariance event

x_n⁰ := (2A + 2) log n, h_n := 2√(x_n⁰/N) + 2x_n⁰/N, **E_cov := {|Ŝ_jk − Σ_jk| ≤ h_n for all j, k ∈ [p]}**.
**Lemma L9.1.** P(E_covᶜ) ≤ 4n^{−2}.
*Proof.* Let O be n × N with orthonormal columns spanning 1^⊥ (OOᵀ = C). The rows of OᵀW are N iid N(0, Σ) vectors
(the mean cancels: Oᵀ1 = 0), and Ŝ_jk = N⁻¹Σ_{i≤N}a_ib_i with (a_i, b_i) iid centred Gaussian, unit variances, covariance
ρ := Σ_jk. By polarisation a_ib_i = [(a_i + b_i)² − (a_i − b_i)²]/4, and Σ_i(a_i ± b_i)² ~ (2 ± 2ρ)χ²_N. Laurent–Massart
(P(|χ²_N − N| > 2√(Nx) + 2x) ≤ 2e^{−x}) for both: with probability ≥ 1 − 4e^{−x},
|Ŝ_jk − ρ| ≤ ¼[(2 + 2ρ) + (2 − 2ρ)](2√(x/N) + 2x/N) = 2√(x/N) + 2x/N. Take x = x_n⁰ and a union over ≤ p² ≤ n^{2A} pairs. ∎

**On E_cov, for n large** (h_n ≤ ¼ and (17 + s₀)·3h_n ≤ c_Σ/2):
(c1) t_j² = Ŝ_jj ∈ [1 − h_n, 1 + h_n] ⊆ [½, 2]; |R̂_jk − Σ_jk| ≤ h′_n := 3h_n (|Ŝ_jk − Σ_jk|/(t_jt_k) ≤ h_n/(1 − h_n) and
|Σ_jk|·|1/(t_jt_k) − 1| ≤ h_n/(1 − h_n)); |Σ_jk| ≤ 1 and |R̂_jk| ≤ 1.
(c2) λ_min(R̂_T) ≥ c_Σ/2 for every T with 1 ≤ |T| ≤ 16 + s₀ (‖R̂_T − Σ_T‖_op ≤ |T|h′_n).
(c3) **Schur perturbation.** For U with |U| ≤ 15 and j, k ∉ U (so |U ∪ {j, k}| ≤ 17 ≤ 16 + s₀):
|pc(R̂; j, k | U) − pc(Σ; j, k | U)| ≤ C_Sh′_n.
*Proof of (c3).* M := Σ, M′ := R̂. M_{jU}M_U⁻¹M_{Uk} − M′_{jU}M′_U⁻¹M′_{Uk} = (M_{jU} − M′_{jU})M_U⁻¹M_{Uk} + M′_{jU}(M_U⁻¹ − M′_U⁻¹)M_{Uk}
+ M′_{jU}M′_U⁻¹(M_{Uk} − M′_{Uk}); ‖M_{jU}‖, ‖M′_{jU}‖ ≤ √15, ‖M_{jU} − M′_{jU}‖ ≤ √15h′_n, ‖M_U⁻¹‖ ≤ 1/c_Σ, ‖M′_U⁻¹‖ ≤ 2/c_Σ,
‖M_U⁻¹ − M′_U⁻¹‖ ≤ (1/c_Σ)(15h′_n)(2/c_Σ). Sum: 15h′_n/c_Σ + 450h′_n/c_Σ² + 30h′_n/c_Σ; add |M_jk − M′_jk| ≤ h′_n. ∎
(c4) Schur complements: for T with |T| ≤ 16 + s₀ and T = A ⊔ B, the Schur complement of R̂_A in R̂_T has
λ_min ≥ λ_min(R̂_T) ≥ c_Σ/2; in particular N⁻¹‖(I − P_U)x_j‖² ≥ c_Σ/2 for |U ∪ {j}| ≤ 16 + s₀.

## L9.2 Energy, floors, visibility (first three items of (B-R))

On E_cov, for n large:
**(E).** ‖μ‖ ≤ Σ_{j∈S₀}|θ*_j|‖x_j‖ ≤ s₀θ_hi√N, so ‖μ‖² ≤ Mn (deterministically, on every design). The other parts of (E)
are not consequences of the population conditions: p ≤ n^A and s₀ fixed are part of Setting R, and **p > s₀ for all
large n is a hypothesis** of (B-R) and of (T3)(b) (the population conditions allow p = s₀; that case is not claimed).
**Floors.** By (c2), λ_min(R̂_T) ≥ φ₀² := c_Σ/2 for 1 ≤ |T| ≤ 16; hence (GF-16) with g_* := c_Σ/2 (X_TᵀX_T = N·R̂_T, N ≥ 1).
**(V-c) for every fixed c_V.** Let j ∈ S₀, U ⊆ [p] ∖ {j}, |U| ≤ 15. N⁻¹x_jᵀ(I − P_U)μ = Σ_{k∈S₀∖U}θ*_k·pc(R̂; j, k | U), and
Σ_{k∈S₀∖U}θ*_k·pc(Σ; j, k | U) = Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U) (truths in U contribute zero), of absolute value ≥ a_V by (V-R).
By (c3): |N⁻¹x_jᵀ(I − P_U)μ| ≥ a_V − s₀θ_hiC_Sh′_n ≥ a_V/2 for n large. Since ‖(I − P_U)x_j‖² ≤ N:
δ²_{U,j} = (x_jᵀ(I − P_U)μ)²/‖(I − P_U)x_j‖² ≥ N·a_V²/4, while τ²_U ≤ σ² + ‖μ‖²/N ≤ σ² + Δ_hi. So
δ²_{U,j} ≥ c_V·τ²_U·log n as soon as N·a_V² ≥ 4c_V(σ² + Δ_hi) log n. ∎

## L9.3 The leakage terms as a function of a partial correlation

Work on E_cov, n large. Let l ∉ Q, U ⊆ [p] ∖ {l}, |U| ≤ 15.
*Case S₀ ⊆ U.* (I − P_U)μ = 0: δ_{U,l} = 0, τ_U = σ, and J_n(δ_{U,l}, τ_U) = √(2/π)z_n ((J3)).
*Case S₀ ⊄ U.* Δ_U = N⁻¹‖(I − P_U)X_{S₀∖U}θ*_{S₀∖U}‖² ≥ (c_Σ/2)‖θ*_{S₀∖U}‖² ≥ Δ_lo by (c4) (T = U ∪ S₀, |T| ≤ 15 + s₀), and Δ_U ≤ Δ_hi.
Put a_U := σ²/τ²_U ∈ [a̲, ā],
  ρ̂_{U,l} := ⟨(I − P_U)x_l, (I − P_U)μ⟩/(‖(I − P_U)x_l‖·‖(I − P_U)μ‖),   **g_{U,l} := √N·ρ̂_{U,l}**.
Then δ_{U,l} = ‖(I − P_U)μ‖ρ̂_{U,l} = √Δ_U·g_{U,l}, so (δ_{U,l} + σZ)/τ_U = √(1 − a_U)·g_{U,l} + √a_U·Z, and
  **J_n(δ_{U,l}, τ_U) = F(g_{U,l}, a_U),   F(g, a) := E[exp((√(1 − a)g + √aZ)²/2)·1{|Z| ≤ z_n}],  Z ~ N(0, 1).**
**(F1)** F(g, a) = e^{(1−a)g²/2}·E[cosh(√(a(1 − a))gZ)e^{aZ²/2}; |Z| ≤ z_n] is even and nondecreasing in |g|.
**(F2)** Let |g|, |g′| ≤ G and a, a′ ∈ [a̲, ā]; L_a := 1/(2√(min(a̲, 1 − ā))); η := |g′ − g| + L_a(G + z_n)|a′ − a|. Then
F(g′, a′) ≤ exp(η(G + z_n + η))·F(g, a).
*Proof.* For |Z| ≤ z_n let w := √(1 − a)g + √aZ, w′ the same with (g′, a′). |w| ≤ G + z_n; |w′ − w| ≤ |g′ − g| + (G + z_n)L_a|a′ − a| = η
(|√(1 − a′) − √(1 − a)| ≤ |a′ − a|/(2√(1 − ā)), |√a′ − √a| ≤ |a′ − a|/(2√a̲)). So |w′² − w²|/2 ≤ η(2|w| + η)/2 ≤ η(G + z_n + η). ∎

## L9.4 Localisation: from U to U₀ = U ∩ H_l

ε_n := r_n + C_Sh′_n. Let l ∉ Q, U ∌ l, |U| ≤ 15, S₀ ⊄ U; U₀ := U ∩ H_l, V := U ∖ H_l. Since S₀ ⊆ H_l: S₀ ∩ U = S₀ ∩ U₀, so
S₀ ⊄ U₀. If V = ∅ there is nothing to do. Otherwise put x̃_· := (I − P_{U₀})x_·, μ̃ := (I − P_{U₀})μ, and
  z₀ := ρ̂_{U₀,l},  a_v := ⟨x̃_l, x̃_v⟩/(‖x̃_l‖‖x̃_v‖),  d_v := ⟨μ̃, x̃_v⟩/(‖μ̃‖‖x̃_v‖) (v ∈ V),  R := the correlation matrix of (x̃_v)_{v∈V}.
Projecting out X̃_V after X_{U₀} (I − P_U = (I − P_{U₀}) − P̃_V, P̃_V the projector on span X̃_V) gives the identities
  **ρ̂_{U,l} = (z₀ − aᵀR⁻¹d)/√((1 − aᵀR⁻¹a)(1 − dᵀR⁻¹d)),   Δ_U = Δ_{U₀}·(1 − dᵀR⁻¹d).**
**Lemma L9.4.** On E_cov, for n large, simultaneously for all such (l, U):
  |g_{U,l} − g_{U₀,l}| ≤ ι_n := √N·C₄ε_n²,   |a_U − a_{U₀}| ≤ C₅ε_n²,   and  ι_n√(log n) → 0,
with c_a := 2√15/c_Σ, c_d := √15·s₀θ_hi/√(Δ_lo·c_Σ/2), C₄ := (4/c_Σ)(c_a·c_d + c_a² + c_d²), C₅ := (Δ_hi/σ²)(2/c_Σ)c_d².
*Proof.* By (c4), N⁻¹‖x̃_l‖², N⁻¹‖x̃_v‖² ≥ c_Σ/2 and N⁻¹‖μ̃‖² = Δ_{U₀} ≥ Δ_lo. By (c3) and (L-loc-R):
|N⁻¹⟨x̃_l, x̃_v⟩| = |pc(R̂; l, v | U₀)| ≤ |Cov(W_l, W_v | W_{U₀})| + C_Sh′_n ≤ ε_n, and
|N⁻¹⟨μ̃, x̃_v⟩| = |Σ_{k∈S₀∖U₀}θ*_k pc(R̂; k, v | U₀)| ≤ s₀θ_hiε_n. Hence ‖a‖ ≤ c_aε_n and ‖d‖ ≤ c_dε_n (|V| ≤ 15).
N⁻¹X̃_VᵀX̃_V is the Schur complement of R̂_{U₀} in R̂_U: λ_min ≥ c_Σ/2, diagonal entries ≤ 1; so λ_min(R) ≥ c_Σ/2 and
‖R⁻¹‖ ≤ 2/c_Σ. With q_a := aᵀR⁻¹a, q_d := dᵀR⁻¹d (both ≤ ¼ for n large), P := ((1 − q_a)(1 − q_d))^{−1/2} and (1 − q)^{−1/2} ≤ 1 + q on [0, ½]:
1 ≤ P ≤ (1 + q_a)(1 + q_d) ≤ min{2, 1 + 2(q_a + q_d)}, so with |z₀| ≤ 1:
|ρ̂_{U,l} − z₀| ≤ |z₀|(P − 1) + P|aᵀR⁻¹d| ≤ 2(q_a + q_d) + 2|aᵀR⁻¹d| ≤ C₄ε_n². And |a_U − a_{U₀}| = σ²|Δ_{U₀} − Δ_U|/(τ²_Uτ²_{U₀}) ≤ Δ_hiq_d/σ² ≤ C₅ε_n².
Finally √(N log n)·ε_n² ≤ 2√(n log n)·r_n² + 2C_S²√(n log n)·h′_n² → 0, by r_n(n log n)^{1/4} → 0 and h′_n² = O(log n/n). ∎
These are deterministic consequences of E_cov; they hold for every conditioning set, however it is selected.

## L9.5 Reference pairs: the conditional law of g_{U₀,l}

Reference family: for l ∉ Q, **I_l := {U₀ ⊆ H_l ∖ {l} : |U₀| ≤ 15, S₀ ⊄ U₀}** (deterministic);
|I_l| ≤ N_ref := (1 + (log n)^{κ_Q})^{15}. Fix l ∉ Q and U₀ ∈ I_l; D := U₀ ∪ S₀ (l ∉ D; |D ∪ {l}| ≤ 16 + s₀).
*Population regression.* W_l − m_l1 = (W_{U₀} − 1m_{U₀}ᵀ)γ¹ + (W_{S₀∖U₀} − 1m_{S₀∖U₀}ᵀ)γ² + e, where e ∈ ℝⁿ has iid N(0, τ_e²) entries and
is **independent of W_D**; τ_e² = Var(W_l | W_D) ∈ [c_Σ, 1] (Schur complement in Σ_{D∪l}); and
γ² = Cov(W_{S₀∖U₀} | W_{U₀})⁻¹Cov(W_{S₀∖U₀}, W_l | W_{U₀}), so by (L-gain-R) and λ_min(Cov(W_{S₀∖U₀} | W_{U₀})) ≥ c_Σ:
**‖γ²‖ ≤ √s₀·C_L/(c_Σ√n)**.
*Projection.* Π := (I − P_{U₀})C is the orthogonal projector on 𝒱 := {1, CW_{U₀}}^⊥, of dimension ν₀ := N − |U₀| almost surely.
  (I − P_{U₀})CW_l = m + ẽ,   m := ΠW_{S₀∖U₀}γ²,   ẽ := Πe.
On **CN := {‖CW_j‖² ≤ 2N for all j ∈ S₀}**: ‖m‖ ≤ ‖γ²‖·√s₀·√(2N) ≤ m̄ := √2·s₀C_L/c_Σ. (E_cov ⊆ CN by (c1).)
*Conditioning.* Let 𝒲 := σ(W_D). Given 𝒲: P_{U₀}, Π, μ (a function of W_{S₀}), μ̃ = Πμ, a_{U₀}, m and the event CN are fixed,
and e keeps its law N(0, τ_e²I_n). If μ̃ ≠ 0 put v := μ̃/‖μ̃‖ ∈ 𝒱 and
  ξ := ⟨ẽ, v⟩/τ_e,   d₀ := ⟨m, v⟩/τ_e,   R := ‖(Π − vvᵀ)(m + ẽ)‖²/τ_e².
Given 𝒲: ξ ~ N(0, 1); R is noncentral χ² with ν₀ − 1 degrees of freedom; ξ and R are independent (orthogonal Gaussian
components); |d₀| ≤ d̄ := m̄/√c_Σ on CN. Since x̃_l = (m + ẽ)/t_l, ρ̂_{U₀,l} = ⟨m + ẽ, v⟩/‖m + ẽ‖ and
  **g²_{U₀,l} = N·(ξ + d₀)²/((ξ + d₀)² + R).**                                                            (9.1)
(If μ̃ = 0 then δ_{U₀,l} = 0, a_{U₀} = 1 and the term is F(0, 1) = √(2/π)z_n; put g_{U₀,l} := 0.)
*Events.* x_n¹ := (A + 2) log n; η_n := 16/N + 2√(x_n¹/N); **E_R(l, U₀) := {R ≥ N(1 − η_n)}**, **E_ξ(l, U₀) := {ξ² ≤ 2x_n¹}**.
A noncentral χ² dominates the central one stochastically, ν₀ − 1 ≥ N − 16, and P(χ²_k < k − 2√(kx)) ≤ e^{−x}; so
P(E_R(l, U₀)ᶜ | 𝒲) ≤ n^{−(A+2)} and P(E_ξ(l, U₀)ᶜ | 𝒲) ≤ 2n^{−(A+2)}. On E_R: g² ≤ κ_n²(ξ + d₀)², κ_n := (1 − η_n)^{−1/2}.

**Lemma L9.5.** For n large (η_n ≤ a̲/2), for every l ∉ Q and U₀ ∈ I_l:
  E[F(g_{U₀,l}, a_{U₀})·1_{E_R(l,U₀)}·1_{CN}] ≤ **Φ_n := √(2/a̲)·√(2/π)·z̄_n·exp(η_nz̄_n²/a̲ + 2d̄z̄_n/a̲ + d̄²/a̲)**.
*Proof.* Condition on 𝒲, on CN, μ̃ ≠ 0 (the case μ̃ = 0 is trivial). a := a_{U₀} ≥ a̲ always (Δ_{U₀} ≤ ‖μ‖²/N ≤ Δ_hi). By (F1) and
(9.1), F(g_{U₀,l}, a)1_{E_R} ≤ F(κ_n(ξ + d₀), a), and ξ ~ N(0, 1) given 𝒲. With s′ := κ_n√(1 − a), r := √a:
s′² = (1 − a)/(1 − η_n) < 1 and 1 − s′² = (a − η_n)/(1 − η_n) ≥ a̲/2. For fixed Z, with c := s′d₀ + rZ:
E_ξ exp((s′ξ + c)²/2) = (1 − s′²)^{−1/2}exp(c²/(2(1 − s′²))). Therefore
  E_ξF(κ_n(ξ + d₀), a) = (1 − s′²)^{−1/2}∫_{−z_n}^{z_n}exp((s′d₀ + rZ)²/(2(1 − s′²)) − Z²/2)dZ/√(2π).
The exponent equals ½Z²[r²/(1 − s′²) − 1] + s′rd₀Z/(1 − s′²) + s′²d₀²/(2(1 − s′²)), and r²/(1 − s′²) − 1 = η_n(1 − a)/(a − η_n) ≤ 2η_n/a̲,
s′r/(1 − s′²) ≤ 2/a̲, s′²/(2(1 − s′²)) ≤ 1/a̲. On |Z| ≤ z_n ≤ z̄_n the exponent is ≤ η_nz̄_n²/a̲ + 2d̄z̄_n/a̲ + d̄²/a̲; ∫_{−z_n}^{z_n}dZ/√(2π) = √(2/π)z_n ≤ √(2/π)z̄_n; and
(1 − s′²)^{−1/2} ≤ √(2/a̲). Take expectations over 𝒲. ∎

*What is and is not conditioned on.* Only W_D is conditioned on (it fixes the true columns' scales and μ); the
innovation e is independent of W_D. No law is asserted given E_cov or given a sample covariance.

## L9.6 The bound on 𝔏_n(Q) (last item of (B-R))

**E := E_cov ∩ ⋂{E_R(l, U₀) ∩ E_ξ(l, U₀) : l ∉ Q, U₀ ∈ I_l}.** P(Eᶜ) ≤ 4n^{−2} + p·N_ref·3n^{−(A+2)} ≤ (4 + 3N_ref)n^{−2} → 0.
On E, for n large: for reference pairs, |g_{U₀,l}| ≤ κ_n(|ξ| + d̄) ≤ 2(√(2x_n¹) + d̄) =: G_n − 1; for every (l, U) with S₀ ⊄ U,
|g_{U,l}| ≤ G_n by Lemma L9.4 (ι_n ≤ 1); and a_U, a_{U₀} ∈ [a̲, ā]. By (F2) with G = G_n and
η_n′ := ι_n + L_a(G_n + z̄_n)C₅ε_n²:
  F(g_{U,l}, a_U) ≤ e^{ς′_n}F(g_{U₀,l}, a_{U₀}),   ς′_n := η_n′(G_n + z̄_n + η_n′) → 0
(G_n + z̄_n = O(√log n), ι_n√log n → 0, ε_n² log n → 0). With L9.3, for every l ∉ Q, on E:
  max{J_n(δ_{U,l}, τ_U) : U ∌ l, |U| ≤ 15} ≤ √(2/π)z̄_n + e^{ς′_n}Σ_{U₀∈I_l}F(g_{U₀,l}, a_{U₀})1_{E_R(l,U₀)}1_{CN}
(U ∩ H_l ∈ I_l whenever S₀ ⊄ U). Averaging over l ∉ Q:
  on E:  **𝔏_n(Q) ≤ √(2/π)z̄_n + e^{ς′_n}Ψ_n**,   Ψ_n := p⁻¹Σ_{l∉Q}Σ_{U₀∈I_l}F(g_{U₀,l}, a_{U₀})1_{E_R(l,U₀)}1_{CN},   **E Ψ_n ≤ N_refΦ_n** (L9.5).
By Markov, for every λ > 0 and n large:
  **P(𝔏_n(Q) > √(2/π)z̄_n + e·λ·N_ref·Φ_n) ≤ P(Eᶜ) + 1/λ.**                                              (9.2)
**(a) General C_L.** z̄_n² ≤ (2A + 1) log n for n large, so Φ_n ≤ exp((2d̄√(2A + 1)/a̲)√log n)·O(√log n), and
N_ref = exp(O(log log n)). Taking λ = log n in (9.2): with probability → 1,
  **𝔏_n(Q) ≤ exp(C_B√log n),   C_B := 2d̄√(2A + 1)/a̲ + 1**   (n large).
**(b) C_L = 0.** Then d̄ = 0, Φ_n ≤ 2√(2/a̲)√(2/π)z̄_n for n large, N_ref ≤ 2^{15}(log n)^{15κ_Q}, and (9.2) gives: for every λ ≥ 1,
P(𝔏_n(Q) > C₆λ(log n)^{15κ_Q+1/2}) ≤ P(Eᶜ) + 1/λ, with C₆ := 2^{18}√((2A + 1)/a̲). That is,
  **𝔏_n(Q) = O_P((log n)^{15κ_Q+1/2})** — a tightness statement. (The first-moment estimate and Markov's inequality establish
tightness. No concentration argument across columns is supplied; a fixed-constant bound with probability tending to
one is not established by this proof, and is not claimed.) ∎

This proves (B-R) as stated in `STATEMENT.md` (Setting R with p > s₀ for all large n): with probability → 1 the design
satisfies (E) (energy bound with M = s₀²θ_hi²; the other parts by assumption), the normalised floor with φ₀² = c_Σ/2
(hence (GF-16)), (V-c) for every fixed c_V (L9.2), and 𝔏_n(Q) ≤ exp(C_B√log n) (L9.6(a)); and (b).

## L9.7 Theorem START-R (T3)(b)

Setting R with p > s₀ for all large n, (FL-R16), (V-R), (L-R); default levels (b_n ≤ 1/(32 log n)). (The case p = s₀ is
excluded by hypothesis and nothing is claimed for it.)
*Design set.* Fixed constants for (T1)(d): A, M = s₀²θ_hi², g_* = c_Σ/2, s₀, and (V-c) with c_V := 2A + 4 (so κ_V = 3/2).
𝒳_n := {designs with: (c1)–(c4) of L9.1; (V-c) at level c_V; 𝔏_n(Q) ≤ exp(C_B√log n)}. By L9.1, L9.2, L9.6(a):
P(X^r ∈ 𝒳_n) → 1, every design of 𝒳_n is admissible at n in the sense of `lemmas/L8_TRANSFER.md` L8.0 (S₀ ⊆ Q and |Q| ≤ K by
(L-R); θ*, Q, h deterministic), and on 𝒳_n: ϱ_n(Q) ≤ ϱ̄_n := (|Q| + 1)n^{−1/2}exp(C_B√log n) → 0 (|Q| ≤ (log n)^{κ_Q}).
*Main display.* ϱ̄_n ≤ c_{0,n} for n large. Proposition L8.2 in the form of Corollary L6.0′ with κ = 1:
  P(1 − π₀(𝓛(Q)) > C_nϱ̄_n + n^{−1}) ≤ 4/log n + 1/(32 log n) + P(X^r ∉ 𝒳_n) → 0,
and C_nϱ̄_n + n^{−1} ≤ (|Q| + 1)n^{−1/2}exp(C_R√log n) for n large, **C_R := C_B + 1** (C_n = O(log n)). So
  **P(1 − π₀(𝓛(Q)) ≤ (|Q| + 1)·n^{−1/2}·exp(C_R√log n)) → 1.**
With Q = S₀: (s₀ + 1)n^{−1/2}exp(C_R√log n) ≤ n^{−c} eventually for every c < ½, so **P(π₀(S₀) ≥ 1 − n^{−c}) → 1**; p ≤ n^A is the
only restriction on p.
*Clause C_L = 0.* Let ε ∈ (0, 1), λ := 4/ε, and 𝒳_n^ε := the set 𝒳_n with its last condition replaced by
𝔏_n(Q) ≤ C₆λ(log n)^{15κ_Q+1/2}. By L9.6(b), limsup P(X^r ∉ 𝒳_n^ε) ≤ ε/4. On 𝒳_n^ε,
ϱ_n(Q) ≤ ϱ̄_n^ε := (|Q| + 1)n^{−1/2}C₆λ(log n)^{15κ_Q+1/2} → 0. Proposition L8.2(i) with (ε/4, κ = 1), for n large:
P(1 − π₀(𝓛(Q)) > C(ε/4)ϱ̄_n^ε + n^{−1}) ≤ ε/4 + 1/(32 log n) + P(X^r ∉ 𝒳_n^ε), with limsup ≤ ε/2 < ε. Since
C(ε/4)ϱ̄_n^ε + n^{−1} ≤ C_ε(|Q| + 1)n^{−1/2}(log n)^{15κ_Q+1/2} for a constant C_ε:
  **1 − π₀(𝓛(Q)) = O_P((|Q| + 1)·n^{−1/2}·(log n)^{15κ_Q+1/2}).** ∎

## L9.8 Where each hypothesis is used
(FL-R16): (c2)–(c4) (sets of size ≤ 16 + s₀), τ_e² ≥ c_Σ, ‖γ²‖. (V-R): L9.2 only. (L-gain-R): ‖γ²‖ = O(n^{−1/2}), i.e. a bounded
mean shift d̄ of the Gaussian ξ — this is what produces the factor exp(C√log n); with C_L = 0 the shift vanishes.
(L-loc-R): L9.4 only (the columns outside H_l change g by o(1/√log n)); it reduces the maximum over all 15-sets to
the ≤ N_ref reference sets. |H_l| ≤ (log n)^{κ_Q}: N_ref. Gaussian rows: L9.1 and the exact conditional law in L9.5.
The partition plays no role: 𝔏_n(Q) is partition-free.
