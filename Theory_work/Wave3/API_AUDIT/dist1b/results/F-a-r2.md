# F-a-r2
stop_reason: end_turn

# Card F, route F-a — attempt

## 0. Outcome

- **Proved (Theorem 1).** Under G, (E), (C), p ≤ n^A and nothing else on the design, the posterior mass of *supersets* S ⊇ S₀ with ‖μ̂ − μ‖² > M σ*² log n is at most O_P(1)·M^{s₀}·c^M + o_P(1), with c = (3/4)^{1/(16C_A)} < 1. Hence Π(S ⊇ S₀, ‖μ̂ − μ‖² > M_n σ*² log n | y) → 0 in probability for every M_n → ∞.
- **Complete answer for s₀ = 0.** Every model is a superset of ∅, so the in-probability form of the card holds for every standardised design.
- **Conditional answer for s₀ ≥ 1.** The in-probability form holds whenever Π(S ⊉ S₀ | y) → 0 in probability. Non-supersets are not treated (GAP 1; this is route F-c).
- **Proved (Theorem 2, the F-a joint bound).** An exact tilting identity for E[weight; fit > g]. It gives an exponential fit tail at the parametric scale on any family of supersets whose tilted spectrum is bounded by κ̄; exact duplicates have κ̄ ≤ 2/(n(n−1)).
- **Not proved, and I believe not provable by this route:** the exponential clause at the sharp rate without (ND) (GAP 2). The identity shows a direction with κ ≍ log n carries expected weight of order 1 with fit ≍ log n, so first moments give only e^{−c·fit/log n}.
- The v-clause is not written out (GAP 3).

Mechanism of Theorem 1: no per-direction joint bound is needed at the M_n log n rate. On the noise event the fit of a model is at most C(s₀ + j) log n, and the design-free superset size tail (Lemma V, re-proved below) has ratio < 3/4.

## 1. Conventions

- Common definitions; ρ′ := θ*ᵀ(G_{S₀} + I)θ*/n = (‖μ‖² + ‖θ*‖²)/n ≤ B := M + M′ (ρ′ = 0 if s₀ = 0). Assume s₀ ≤ K, p ≤ n^A, C_A := 10 + 4A.
- For c > 0 and T ⊆ [p], with X = X_{c,T}, A_T = G_T + I: Q_T^{(c)}(u) := min_ψ{‖u − Xψ‖² + cψᵀA_Tψ/n} = uᵀ(I − M_T^{(c)})u, M_T^{(c)} := X(G_T + cA_T/n)⁻¹Xᵀ = h_c(XXᵀ), h_c(λ) = λ/((1 + c/n)λ + c/n). So M_T^{(1)} = M_T.
- Facts about h_c: it is operator monotone in λ (same argument as [P1] `lem:spec`(d)), decreasing in c, and 0 ≤ h_c < 1. Hence
  - (F1) T ⊆ T′ ⟹ M_T^{(c)} ⪯ M_{T′}^{(c)};
  - (F2) c ≤ c′ ⟹ M_T^{(c′)} ⪯ M_T^{(c)};
  - (F3) 0 ⪯ M_T^{(c)} ⪯ P_T.
- Woodbury: I − M_T^{(c)} = (Σ_T^{(c)})⁻¹ with Σ_T^{(c)} := I + (n/c)XA_T⁻¹Xᵀ ⪰ I, and det Σ_T^{(c)} = ∏_i(1 + (n/c)g_i/(1 + g_i)) =: D_T^{(c)} (g_i the eigenvalues of G_T). D_T^{(1)} = D_T, and for a ≤ 1: D_T ≤ D_T^{(a)} ≤ a^{−|T|}D_T (F4).
- Cutoff: m̄ := min{K, s₀ + 2 + ⌈(s₀ log(2p) + ((s₀+2)/2) log(n+1))/log 2⌉} ≤ C_m log n, C_m := s₀ + 3 + (s₀(A+1) + s₀ + 2)/log 2.
- Noise event 𝒢 := (G1) ∩ (G2*):
  - (G1) |‖e‖² − Nσ*²| ≤ σ*²√N log n;
  - (G2*) ‖P_Te‖² ≤ σ*²C_A|T| log n for every T ≠ ∅.
  - P(𝒢ᶜ) ≤ 2/log²n + 1/n ([P1] `lem:chi`(b), and the proof of `lem:good`, which establishes the per-size bound).
- δ_n := log n/√N + C_AC_m log²n/N; 1 + ε_n := (n + 0.02)/(N(1 − δ_n)); ζ_n := ε_nC_A log n/2. Let n₀ = n₀(s₀, A) be such that for n ≥ n₀: log n ≤ √N, δ_n ≤ ½, ε_n ≤ 1, e^{ζ_n} ≤ 1.06. This is possible because ε_n ≤ 2(δ_n + 1.02/N) and δ_n log n → 0.
- χ₀ := ‖P_{S₀}e‖²/σ*² ≤_st χ²_{s₀}.

## 2. Lemmas

**Lemma 1 (variational split; = Lemma V(a), proved).** Let S ⊇ S₀, η > 0, c = 1 + η, a = 1/c, Δ_S := M_S^{(a)} − M_{S₀}^{(a)} ⪰ 0, G_S := eᵀΔ_Se/σ*². Then

 Q^c_{S₀} − Q^c_S ≤ σ*²G_S + ‖P_{S₀}e‖² + (1 + 2/η)ρ′,  M_S − M_{S₀} ⪯ Δ_S + P_{S₀},  Δ_S ⪯ P_S.

*Proof.*
- Upper bound for S₀: in the variational formula put φ = θ* + ψ. Then ‖y_c − X_{c,S₀}φ‖² = ‖e − X_{c,S₀}ψ‖² and φᵀAφ ≤ (1+η)ψᵀAψ + (1 + 1/η)θ*ᵀAθ*. So Q^c_{S₀} ≤ Q^{(c)}_{S₀}(e) + (1 + 1/η)ρ′.
- Lower bound for S: for φ ∈ ℝ^S write φ = θ* + ψ (θ* zero-padded). Then ‖y_c − X_{c,S}φ‖² = ‖e − X_{c,S}ψ‖² and φᵀA_Sφ ≥ ψᵀA_Sψ/(1+η) − θ*ᵀA_Sθ*/η (from 2uᵀAw ≥ −δuᵀAu − wᵀAw/δ with δ = η/(1+η)). Also θ*ᵀA_Sθ* = nρ′. So Q^c_S ≥ Q_S^{(a)}(e) − ρ′/η.
- Subtract: Q^c_{S₀} − Q^c_S ≤ eᵀ(M_S^{(a)} − M_{S₀}^{(c)})e + (1 + 2/η)ρ′, and M_S^{(a)} − M_{S₀}^{(c)} = Δ_S + (M_{S₀}^{(a)} − M_{S₀}^{(c)}) ⪯ Δ_S + P_{S₀} by (F3).
- Δ_S ⪰ 0 by (F1). M_S − M_{S₀} ⪯ M_S^{(a)} − M_{S₀} = Δ_S + M_{S₀}^{(a)} − M_{S₀} ⪯ Δ_S + P_{S₀} by (F2), (F3). Δ_S ⪯ M_S^{(a)} ⪯ P_S. ∎

**Lemma 2 (tilting identity and moment bound).** Let S = S₀ ∪ J, |J| = j, with η, a as above. Let δ_i ∈ [0, 1) be the eigenvalues of Δ_S and κ_i := δ_i/(1 − δ_i); at most s₀ + j of them are nonzero. For ξ ~ N(0, I_N) and every measurable g ≥ 0:

 E[e^{G_S/2}g(e)] = ∏_i(1 + κ_i)^{1/2} · E[g(σ*(I − Δ_S)^{−1/2}ξ)],  and under the tilted law G_S = Σ_iκ_iξ_i²;

 (D_{S₀}/D_S)^{1/2}∏_i(1 + κ_i)^{1/2} ≤ (1+η)^{(s₀+j)/2}.

*Proof.*
- Write Σ₀ = Σ_{S₀}^{(a)}, Σ₁ = Σ_S^{(a)}. Then Δ_S = Σ₀⁻¹ − Σ₁⁻¹ and I − Δ_S ⪰ Σ₁⁻¹ ≻ 0 (as Σ₀ ⪰ I). The identity is the Gaussian integral ∫(2π)^{−N/2}e^{−zᵀ(I−Δ)z/2}g(σ*z)dz, and (I−Δ)^{−1/2}Δ(I−Δ)^{−1/2} has eigenvalues κ_i.
- E := Δ^{1/2}Σ₀Δ^{1/2} ⪰ Δ, and E has the nonzero eigenvalues of Σ₀^{1/2}ΔΣ₀^{1/2} = I − Σ₀^{1/2}Σ₁⁻¹Σ₀^{1/2} ≺ I. By Weyl monotonicity (A ⪯ B ⟹ λ_i(A) ≤ λ_i(B); Courant–Fischer), det(I − Δ) ≥ det(I − E) = det Σ₀/det Σ₁.
- Hence ∏(1 + κ_i) = det(I − Δ)⁻¹ ≤ D_S^{(a)}/D_{S₀}^{(a)} ≤ (1+η)^{s₀+j}D_S/D_{S₀} by (F4). ∎

No rank or eigenvalue condition is used in Lemmas 1–2.

**Lemma 3 (one superset, on 𝒢).** Let n ≥ n₀, S = S₀ ∪ J ∈ Ω, 1 ≤ j, |S| ≤ m̄, T_j := C_A(s₀ + j) log n. On 𝒢:

 π(S)/π(S₀) ≤ F_n · e^{(s₀+j)ζ_n} · [w(s₀+j)/w(s₀)](D_{S₀}/D_S)^{1/2}e^{G_S/2},  F_n := exp{(1+ε_n)[χ₀/2 + (1 + 2/η)ρ′/(2σ*²)]},

and G_S ≤ T_j.

*Proof.*
- μ_c ∈ col X_{c,S}, so by [P1] `lem:spec`(b), (G1), (G2*): Q^c_S ≥ ‖e‖² − ‖P_Se‖² ≥ Nσ*²(1 − δ_n) > 0.
- Q^c_{S₀} ≥ Q^c_S by (F1). As in [P1] `lem:one`, ((2b + Q_{S₀})/(2b + Q_S))^ν ≤ exp{ν(Q_{S₀} − Q_S)/Q_S} ≤ exp{(1+ε_n)(Q_{S₀} − Q_S)/(2σ*²)}.
- Insert Lemma 1. G_S ≤ ‖P_Se‖²/σ*² ≤ T_j by Δ_S ⪯ P_S and (G2*), so (1+ε_n)G_S/2 ≤ G_S/2 + (s₀+j)ζ_n. ∎

**Lemma 4 (design-free size tail; = [W3P] Lemma 1a′, re-derived).** For L′ > c♯² (c♯ of [T03R] §2):

 P(π(|S| > m̄) > L′(n+1)^{−1/2}) ≤ (8 + 24M/σ*²)/(n−1) + L′^{−1/2} + C′_Λ/log(√L′/c♯),  C′_Λ := 1/√2 + ½ + B/(2σ*²).

*Proof.*
- In the proof of [P1] `lem:den` replace the bound on Q^c_{S₀} by Q^c_{S₀} ≤ ‖y_c − X_{c,S₀}θ*‖² + ρ′ = σ*²E′ + ρ′ (φ = θ* in the variational formula). The rest of that proof is unchanged with R_n := ρ′ and gives m^c_{b₊}(S₀)/f₀ ≥ D_{S₀}^{−1/2}c_IGσ*²n^{−1/2}e^{−Λ′}, EΛ′ ≤ C′_Λ.
- The proof of [T03R] T02(i♯) ([P1] `lem:num`, `thm:Ta`, `thm:T01iii`, Markov) then gives the display with threshold L′·R_{m̄}√(D_{S₀})√n.
- By [P1] `lem:prior`(c),(d), R_m ≤ 4(2p)^{s₀}2^{−m}. If m̄ < K, the choice of m̄ gives R_{m̄}(n+1)^{s₀/2}√n ≤ (n+1)^{−1/2}; if m̄ = K the mass is 0. ∎

**Lemma 5 (within a superset, on 𝒢, n ≥ n₀).** Let S ⊇ S₀, |S| = s₀ + j ≤ m̄, V̄ := 4σ*² + 2B. Then

- (i) ‖M_Sy_c − μ_c‖² ≤ 2σ*²C_A(s₀+j) log n + 2B;
- (ii) for u > 0: Π(‖μ̂ − μ‖² > 4σ*²C_A(s₀+j) log n + 4B + 2V̄(2(s₀+j) log 2 + 4u) | S, y) ≤ e^{−u} + 0.83^{n/2}.

*Proof.*
- (i) M_Sy_c − μ_c = M_Se − (I − M_S)μ_c. ‖M_Se‖² ≤ ‖P_Se‖², and ‖(I − M_S)μ_c‖² ≤ L_S ≤ L_{S₀} ≤ ρ′ ≤ B by (F1), (F3).
- (ii) ‖μ̂ − μ‖ = ‖X_{c,S}θ − μ_c‖ because μ̂ − μ ∈ range C. Given (S, v, y), X_{c,S}θ − M_Sy_c ~ N(0, vM_S), so its squared norm is ≤_st vχ²_{|S|}.
- v = (b + Q^c_S/2)/Γ with Γ ~ Gamma(ν, 1). On 𝒢: Q^c_S ≤ Q^c_{S₀} ≤ ‖e‖² + ρ′ ≤ 2Nσ*² + B and b ≤ 0.02(nM/N + 2σ*²), so b + Q^c_S/2 ≤ nσ*² + B.
- Chernoff: P(Γ ≤ ν/2) ≤ (√e/2)^ν ≤ 0.83^{n/2}. Otherwise v ≤ V̄. Then use [P1] `lem:chi`(a) and ‖a + b‖² ≤ 2‖a‖² + 2‖b‖². ∎

## 3. Theorem 1 (superset fit tail; no (ND), no floor)

Put τ(j₁, u) := (s₀ + j₁)(4σ*²C_A log n + 4V̄ log 2) + 4B + 8V̄u, K_{s₀} := Σ_{i≥1}i^{s₀}(3/4)^i, K₁ := 1.06^{s₀}2^{1+s₀/2}K_{s₀}.

**Theorem 1.** Assume G, (E; M), (C; M′), p ≤ n^A, s₀ ≤ K, n ≥ n₀(s₀, A). For all integers j₁ ≥ 0 and reals u, x₀, L > 0, L′ > c♯², with probability at least

 1 − [2/log²n + 1/n + P(χ²_{s₀} > x₀) + K₁e^{x₀+3B/σ*²}/L + (8 + 24M/σ*²)/(n−1) + L′^{−1/2} + C′_Λ/log(√L′/c♯)]:

 Π(S ⊇ S₀, ‖μ̂ − μ‖² > τ(j₁, u) | y) ≤ e^{−u} + 0.83^{n/2} + L(j₁+2)^{s₀}(3/4)^{j₁} + L′(n+1)^{−1/2}.

The bound is uniform over designs and θ* with these (M, M′, σ*², s₀, A).

*Proof.* Take η = 1. Split the supersets by size.
1. **|S| ≤ min(s₀ + j₁, m̄).** By Lemma 5(ii) (monotone in j) the conditional bad mass is ≤ e^{−u} + 0.83^{n/2} on 𝒢.
2. **|S| > m̄.** Lemma 4.
3. **s₀ + j₁ < |S| ≤ m̄.** The mass is at most Σ π(S)/π(S₀). On 𝒢 ∩ {χ₀ ≤ x₀}, Lemma 3 with ε_n ≤ 1 gives F_n ≤ e^{x₀+3B/σ*²}, so the sum is ≤ e^{x₀+3B/σ*²}1.06^{s₀}Ṽ, where Ṽ := Σ_{j>j₁}e^{jζ_n}V_j and V_j := Σ_{|J|=j}[w(s₀+j)/w(s₀)](D_{S₀}/D_{S₀∪J})^{1/2}e^{G_{S₀∪J}/2}.
   - By Lemma 2 (g ≡ 1) and [P1] `lem:prior`(e): EV_j ≤ 2(j+1)^{s₀}2^{−j}2^{(s₀+j)/2}.
   - So EṼ ≤ 2^{1+s₀/2}Σ_{j>j₁}(j+1)^{s₀}(1.06/√2)^j ≤ 2^{1+s₀/2}K_{s₀}(j₁+2)^{s₀}(3/4)^{j₁}, using 1.06/√2 < 3/4 and j₁ + i + 1 ≤ (j₁+2)i for i ≥ 1.
   - Markov on Ṽ gives the term K₁e^{x₀+3B/σ*²}/L. ∎

**Corollary 1.** Under the hypotheses of Theorem 1:
- (a) For every M_n → ∞: Π(S ⊇ S₀, ‖μ̂ − μ‖² > M_nσ*² log n | y) → 0 in probability. Take j₁ = ⌊M_n/(16C_A)⌋ − s₀ and u = M_nσ*² log n/(32V̄); then τ(j₁, u) ≤ M_nσ*² log n for large n. Then choose x₀, L, L′ large.
- (b) For fixed M ≥ 16C_A s₀: the same mass is ≤ L(M+2)^{s₀}(3/4)^{M/(16C_A)−s₀−1} + n^{−Mσ*²/(32V̄)} + L′(n+1)^{−1/2} + 0.83^{n/2} with probability → 1 as L, L′ → ∞ (the "c^M" form).
- (c) **s₀ = 0** (μ = 0; (E), (C) void): Π(‖μ̂‖² > M_nσ*² log n | y) → 0 in probability for every standardised design with p ≤ n^A. This is the card's in-probability form in full.
- (d) **s₀ ≥ 1:** the card's in-probability form holds for every array with Π(S ⊉ S₀ | y) → 0 in probability, with no (ND), (F_w) or (OS).

## 4. Theorem 2 (the joint weight/fit bound of F-a)

**Proposition (exact identity).** For S = S₀ ∪ J and 0 ≤ g < T ≤ ∞:

 E[(D_{S₀}/D_S)^{1/2}e^{G_S/2}1{g < G_S ≤ T}] = (D_{S₀}/D_S)^{1/2}∏(1+κ_i)^{1/2} · P(g < Σ_iκ_iξ_i² ≤ T) ≤ (1+η)^{(s₀+j)/2}P(g < Σ_iκ_iξ_i² ≤ T).

This is Lemma 2 with g(e) = 1{g < G_S ≤ T}. In the card's commuting one-direction picture, κ_i = d_i − 1, the weight is d_i^{−1/2}e^{(1−1/d_i)z_i²/2}, and the tilted gain is (d_i − 1)ξ_i².

**Theorem 2.** Assume the hypotheses of Theorem 1 with η = 0.1. Let 𝒮 be a deterministic family of supersets S = S₀ ∪ J ∈ Ω, J ≠ ∅, |S| ≤ m̄, with κ_max(S) := max_iκ_i ≤ κ̄. For g, x₀, L > 0, with probability ≥ 1 − P(𝒢ᶜ) − P(χ²_{s₀} > x₀) − K₂e^{x₀+21B/σ*²}/L:

 Π(S ∈ 𝒮, ‖M_Sy_c − μ_c‖² > 4σ*²g + 8σ*²x₀ + 2B | y) ≤ L e^{−g/(8κ̄)},

 K₂ := 1.06^{s₀}·1.2111^{s₀}·Σ_{j≥1}2(j+1)^{s₀}(0.642)^j.

*Proof.*
- On 𝒢 ∩ {χ₀ ≤ x₀}, by Lemma 1: ‖M_Se‖² ≤ 2eᵀ(M_S − M_{S₀})e + 2‖P_{S₀}e‖² ≤ 2σ*²G_S + 4σ*²χ₀. With Lemma 5(i)'s decomposition, ‖M_Sy_c − μ_c‖² ≤ 4σ*²G_S + 8σ*²x₀ + 2B. So the bad models have G_S > g.
- Chernoff with λ = 1/(8κ̄): P(Σκ_iξ_i² > g) ≤ e^{−g/(8κ̄)}∏(1 − κ_i/(4κ̄))^{−1/2} ≤ e^{−g/(8κ̄)}(4/3)^{(s₀+j)/2}.
- With the Proposition and Lemma 3, the expected relative mass is ≤ e^{−g/(8κ̄)}Σ_j2(j+1)^{s₀}2^{−j}1.06^j(1.1·4/3)^{(s₀+j)/2}, and √(1.1·4/3)·1.06/2 < 0.642. Markov. ∎

*Remark (duplicates).* In Proposition D's design (all columns equal), Δ_S = (h_a(kN) − h_a(N))uuᵀ ⪯ uuᵀ/(nN), so κ̄ ≤ 2/(nN). The posterior-mean fit of all supersets up to size m̄ is then O_P(1) (parametric scale), although the size tail is geometric. More generally, directions with κ = O(1) are harmless at the scale t. Directions with κ ≫ log n are suppressed by the small-ball factor P(Σκ_iξ_i² ≤ T) in the Proposition, but only at polynomial order per direction.

## 5. Where F-a stops

- **GAP 1 (non-supersets, s₀ ≥ 1).** Models S ⊉ S₀ are not treated. Comparison with S ∪ S₀ costs (2p)^{s₀}(n+1)^{s₀/2}, which only gives the DIST-2 rate. A c^M bound needs references T ⊊ S₀ with control of ρ′_T (route F-c).
- **GAP 2 (exponential clause at the sharp rate without (ND)).** Not proved. By the Proposition, one direction with κ = T (T ≈ C_A log n, the smallest truncation level a union bound over p^j models permits) has E[weight; T/2 < gain ≤ T] = P(½ < ξ² ≤ 1)·(prefactor ≈ 1) ≈ 0.16, independent of n. So j such directions carry expected relative mass ≈ (0.08)^j with fit ≈ jT/2. First-moment arguments therefore give at best Π(fit > Cσ*²t) ≲ e^{−ct/log n}, which is what Theorem 1 yields with j₁ ≍ t/log n. This is an obstruction to the proof, not a lower bound on the posterior; it agrees with the F-b heuristic, and I expect the exponential clause to be false at γ ≍ log n/n.
- **GAP 3 (v-clause).** Π(|v/σ*² − 1| > M_nn^{−1/2}, S ⊇ S₀ | y) → 0 is not written out. On 𝒢, ‖e‖² − σ*²C_Am̄ log n ≤ Q^c_S ≤ ‖e‖² + B for supersets with |S| ≤ m̄, so it should follow from Gamma concentration and Lemma 4; not checked line by line.
- **Limits of what is proved.** Theorem 1 is in-probability only: P(𝒢ᶜ) ≤ 2/log²n + 1/n, and Lemma 4 has a 1/log L′ tail. Upgrading these (Lemma S, χ² tails for (G1)) would not change GAP 2.

ATTEMPT F/F-a RESULT=PROVED-VARIANT GAPS=3
