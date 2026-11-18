# X-a-1
stop_reason: end_turn

# Card X, route X-a — proof of Lemma X as stated (c = ½)

The statement is proved as written, with no gaps I can find; the proof is my own and unchecked. Two deviations from the route sketch, both simplifications:

- **Lemma V is not consumed.** On the noise event, for S ⊇ S₀, the bounds Q_S ≥ ‖e‖² − ‖P_S e‖² and Q_{S₀} ≤ ‖e‖² + σ²(t + C_B) give the same split directly, with no floor on S₀.
- **Lemma S is not consumed.** The one instance needed (reference S₀, cutoff m_n(t)) is proved inline in Step 5.

Notation: σ² := σ*², ℓ := log n (≥ 1 for n ≥ 3), N = n − 1, Q_S := Q^c_S, B := M + M′, s := s₀^r, m := m_n(t), b₀ = 0.01. For S ⊆ [p] put ℓ(S) := w(|S|) D_S^{−1/2}(2b + Q_S)^{−ν}, so π(S)/π(S′) = ℓ(S)/ℓ(S′) on Ω.

## 0. External results used

- **[P1] (locked file, proofs there).**
  - `lem:slab`: min-representation of Q.
  - `lem:spec`: (a) Q = Yᵀ(I − M)Y; (b) 0 ⪯ M_S ⪯ P_S, so I − M_S ⪰ I − P_S; (d) Q decreases when columns are added; (e) D = Π f(λ_i(G)), f(λ) = ((n+1)λ+1)/(λ+1) ∈ [1, n+1), so 1 ≤ D_S ≤ (n+1)^{|S|}.
  - `lem:prior`: (a) Σ_{k≤p} q_k = 1; (c, proof line) Σ_{k>m} q_k ≤ 2^{−m} for m ≥ 0; (e) C(p−s₀, j) w(s₀+j)/w(s₀) ≤ 2(j+1)^{s₀}2^{−j} for s₀ + j ≤ p.
  - `lem:chi`: (a) r ≤ d, x ≥ 0 ⇒ P(χ²_r ≥ 2d log 2 + 4x) ≤ e^{−x}; (c) E[e^{χ²_d/2}1{χ²_d ≤ τ}] ≤ (eτ/d)^{d/2} for d ≥ 1.
  - `prop:closed` eq. (mc): m^c_b(S) = c_n b^{0.51} D_S^{−1/2}(b + Q_S/2)^{−ν}, so π(S) = ϖ(S) m^c_b(S)/Z^c_b at b = b₀s_y² (`thm:T01i`).
  - `thm:T01ii`: for b₁ ≤ b ≤ b₂, Π_b(E) ≤ (b₂/b₁)^{1.02} I_{b₁}(E)/Z^c_{b₂}, pointwise in y_c.
  - `lem:num`: for data-free b and 𝒜 ⊆ Ω, E[Σ_{S∈𝒜} ϖ(S) m^c_b(S)/f₀(y_c)] = ϖ(𝒜), with f₀ = N_N(μ_c, σ²I).
  - Integral representation in the proof of `lem:den`: m^c_b(S)/f₀(y_c) = D_S^{−1/2} ∫ exp{−(N/2) log(v/σ²) + E′/2 − Q_S/(2v)} IG(v; 0.51, b) dv, E′ := ‖e‖²/σ².
- **(LM)** Laurent–Massart, Ann. Statist. 28 (2000), Lemma 1: P(χ²_D − D ≥ 2√(Dx) + 2x) ≤ e^{−x}, P(D − χ²_D ≥ 2√(Dx)) ≤ e^{−x}.
- **(GT)** For Γ ~ Gamma(ν, 1): P(Γ − ν ≥ √(2νx) + x) ≤ e^{−x} and P(Γ − ν ≤ −√(2νx)) ≤ e^{−x}. (Boucheron–Lugosi–Massart 2013, §2.4: log E e^{λ(Γ−ν)} = ν(−log(1−λ) − λ) ≤ νλ²/(2(1−λ)) on (0,1), and ≤ νλ²/2 for λ < 0.)
- **(GAU)** P(|N(0,1)| > √(2x)) ≤ 2e^{−x}.
- **(IL)** Cauchy interlacing. If S ⊆ S′ with |S′∖S| = a, then λ_i(G_{S′}) ≤ λ_i(G_S) for i ≤ |S| (increasing order), so by `lem:spec`(e) D_{S′} ≤ D_S (n+1)^a.
- **(W)** w(k)/w(k+a) = Π_{i=k}^{k+a−1}(2p−1−i)/(i+1) ≤ (2p)^a; and 1/w(s₀) = 2C(2p−1, s₀) ≤ 2(2p)^{s₀}.
- **(L₀)** L_{S₀} ≤ B: `lem:slab` with Y = μ_c at φ = θ*_{S₀} gives L_{S₀} ≤ (‖μ‖² + ‖θ*‖²)/n.

## 1. Constants (chosen in this order; all depend only on s, A, σ², M, M′)

- C_A := 4A + 6; τ_k := C_A k ℓ + 4t.
- b₋ := b₀σ²/2, b₊ := b₀(3M + 4σ²), κ := (b₊/b₋)^{0.51}, c_IG := min_{v∈[σ²,2σ²]} IG(v; 0.51, b₊) > 0, c♯ := κ²/(c_IG σ²).
- C_B := (2s(A+1) + 3)B/σ²; c_ρ := 2√(2(s(A+1)+1)B)/σ; C_S := 1 + B/(2σ²) + (1 + c_ρ/2)²/2.
- **C′ := 4(8 + C_B)**; C₀ := C′ + s + 1; C₁ := C_A C₀ + 4; C₃ := (A+1)C₀ + 1.
- C″ := max{32C₃, 4(C₁ + 1 + C_B), 47}; Λ := C″σ²t; c₄ := (log 2)/16 (so c₄C″ ≥ 2).
- C₂ := C₁ + 2√(2C₃C″) + C″; C_v := 2(10 + C₂ + 2b₊/σ²); C_μ := 8C₀ + 16 + 4C₁ + 4C″; **C := max(C_v, C_μ)**.
- C_m := 2s + 1 + (s(A+2) + 5)/log 2; K_s := Σ_{j≥1}(j+1)^s 2^{−j}.
- **M₀ := max{4, s(5A+9), 1 + s(A+2), 2 log(4 + K_s)}**; **c := ½**.

Since M₀ ≥ 1, t ≥ ℓ ≥ 1 on the range. Hence, with d_t = s₀ + ⌈C′t/ℓ⌉ and j₁ := d_t − s₀:

 (1.1) d_t ℓ ≤ (s₀+1)ℓ + C′t ≤ C₀t, d_t ≤ C₀t, τ_k ≤ C₁t for k ≤ d_t, j₁ℓ ≥ C′t;
 (1.2) m + s₀ ≤ C_m t (from log(2p) ≤ (1+A)ℓ, log(n+1) ≤ 2ℓ), so τ_{m+s₀} ≤ (C_A C_m ℓ + 4)t.

**Choice of n₀** (depends in addition on c_D, κ₀). Put t̄ := n^{1−κ₀}. n₀ is such that for n ≥ n₀:

- (R1) t̄ ≤ N and 2√(Nt̄) + 2t̄ ≤ N/2;
- (R2) 2b₊ + σ²(1 + C_B)t̄ + σ²(2√(Nt̄) + 2t̄) ≤ Nσ²;
- (R3) 5√(t̄/n) ≤ ½ and C_v√(t̄/n) ≤ 1;
- (R4) c₄C″t̄ ≤ (n/2) log 2;
- (R5) ε̄_n := [2√(Nt̄) + (C_A C_m ℓ + 4)t̄]/N ≤ ¼, and ε̄′_n := 2ε̄_n + 3/N satisfies ε̄′_n ≤ ½ and C_A ℓ ε̄′_n ≤ log 2;
- (R6) e(C_A + 4)ℓ/(2c_D(n+1)) ≤ 1/(4√n);
- (R7) n ≥ 16 and 2c♯e^{C_S} ≤ √n.

Each left side tends to 0 relative to its right side because t̄/n = n^{−κ₀}. Each is monotone in t, so it holds for every t ≤ t̄. This gives one n₀ for the whole range.

Fix n ≥ n₀ and t ∈ [M₀ℓ, t̄].

## 2. Noise event 𝓔_t

𝓔_t is the intersection of:

- (N1) |‖e‖² − Nσ²| ≤ σ²(2√(Nt) + 2t);
- (N2) ‖P_T e‖² ≤ σ²τ_{|T|} for every nonempty T ⊆ [p];
- (N3) |eᵀ(I − M_S)μ_c| ≤ σ√(2x_S L_S) for every S ⊆ [p] (∅ included), x_S := |S|(log p + 1) + t ≤ |S|(A+1)ℓ + t;
- (N5) χ²_J := σ^{−2}‖(P_{S₀∪J} − P_{S₀})e‖² ≤ τ_{|J|} for every nonempty J ⊆ [p]∖S₀.

**Claim: P(𝓔_tᶜ) ≤ 6.4e^{−t}.**

- (N1): (LM) with D = N, x = t; failure ≤ 2e^{−t}.
- (N2): for |T| = k, ‖P_T e‖²/σ² ~ χ²_r with r ≤ k. `lem:chi`(a) with d = k, x = k(log p + 1) + t has threshold 2k log 2 + 4k(log p + 1) + 4t ≤ τ_k (as 2 log 2 + 4 ≤ 6ℓ, log p ≤ Aℓ). The union over ≤ p^k sets and k ≥ 1 costs e^{−t}Σ_{k≥1}e^{−k} ≤ 0.6e^{−t}.
- (N5): the same. P_{S₀∪J} − P_{S₀} is a projection of rank d_J ≤ |J|, so χ²_J ~ χ²_{d_J}; failure ≤ 0.6e^{−t}.
- (N3): eᵀ(I − M_S)μ_c ~ N(0, σ²‖(I − M_S)μ_c‖²) and ‖(I − M_S)μ_c‖² ≤ L_S (0 ⪯ I − M_S ⪯ I). (GAU) and a union give 2e^{−t}Σ_{k≥0}e^{−k} ≤ 3.2e^{−t}.

**Consequences on 𝓔_t (deterministic).**

- (2.1) Nσ²/2 ≤ ‖e‖² ≤ 3Nσ²/2, by (R1).
- (2.2) σ²/2 ≤ s_y² ≤ 3M + 4σ², i.e. b₋ ≤ b ≤ b₊.
 - Upper: ‖y_c‖² ≤ 2nM + 2‖e‖² and n/N ≤ 3/2.
 - Lower: (N3) at S = ∅ gives |eᵀμ_c| ≤ σ√(2t)‖μ_c‖, so ‖y_c‖² ≥ ‖e‖² + min_x(x² − 2σ√(2t)x) = ‖e‖² − 2σ²t ≥ Nσ²/2 by (R1).
- (2.3) For every S ⊆ [p], with y_c = μ_c + e and `lem:spec`(a),(b):
 Q_S = ‖e‖² − eᵀM_S e + 2eᵀ(I − M_S)μ_c + L_S, 0 ≤ eᵀM_S e ≤ ‖P_S e‖².
- (2.4) Q_{S₀} ≤ ‖e‖² + σ²(c_ρ√t + B/σ²) ≤ ‖e‖² + σ²(t + C_B).
 By (2.3), (N3), (L₀) and x_{S₀} ≤ (s(A+1)+1)t: 2|eᵀ(I − M_{S₀})μ_c| ≤ σ²c_ρ√t ≤ σ²(t + 2(s(A+1)+1)B/σ²).
- (2.5) 2b + Q_{S₀} ≤ 2Nσ², by (2.4), (N1), (R2).

## 3. Good models: 𝒮_good := {S ∈ Ω : |S| ≤ d_t, L_S ≤ Λ}

**Claim.** On 𝓔_t, for every S ∈ 𝒮_good: Π(‖μ̂ − μ‖² > Cσ²t or |v/σ² − 1| > C√(t/n) | S, y) ≤ 3e^{−t}.

*Fit centre.* M_S y_c − μ_c = M_S e − (I − M_S)μ_c. Since ‖M_S e‖ ≤ ‖P_S e‖ (M_S² ⪯ P_S) and ‖(I − M_S)μ_c‖² ≤ L_S, (N2) and (1.1) give

 ‖M_S y_c − μ_c‖² ≤ 2σ²C₁t + 2C″σ²t.

*Q_S.* By (2.3), (N2), (N3), with x_S ≤ d_t(A+1)ℓ + t ≤ C₃t:

 |Q_S − ‖e‖²| ≤ σ²C₁t + 2σ√(2C₃t·C″σ²t) + C″σ²t = σ²C₂t.

With (N1) and t ≤ √(Nt): |Q_S − Nσ²| ≤ σ²(4 + C₂)√(Nt). Hence, using 0 < 2b ≤ 2b₊,

 |(2b + Q_S)/σ² − n| ≤ (5 + C₂ + 2b₊/σ²)√(nt).

*Variance.* v | S, y ~ IG(ν, β_S) with β_S = b + Q_S/2, i.e. v = β_S/Γ with Γ ~ Gamma(ν, 1). By (GT), with conditional probability ≥ 1 − 2e^{−t}: |Γ − ν| ≤ √(2νt) + t, hence |2Γ − n| ≤ 5√(nt) and 2Γ ≥ n/2 by (R3). On that event

 |v/σ² − 1| = |(2b + Q_S)/σ² − 2Γ|/(2Γ) ≤ C_v√(t/n), and v ≤ 2σ² by (R3).

*Mean.* Given (v, S, y), X_{c,S}(θ − θ̂_S) ~ N(0, vM_S). The eigenvalues of M_S lie in [0, 1) and at most |S| are nonzero, so ‖X_{c,S}(θ − θ̂_S)‖² ≤ vχ²_{|S|} under a coupling. By `lem:chi`(a), with conditional probability ≥ 1 − e^{−t} it is ≤ v(2|S| log 2 + 4t) ≤ v(2C₀ + 4)t. On both events, since ‖μ̂ − μ‖ = ‖X_{c,S}θ − μ_c‖ and X_{c,S}θ̂_S = M_S y_c:

 ‖μ̂ − μ‖² ≤ 2·2σ²(2C₀ + 4)t + 2(2σ²C₁t + 2C″σ²t) = C_μσ²t. ∎

## 4. Small far models: 𝒮_far := {S ∈ Ω : |S| ≤ d_t, L_S > Λ}

**Claim.** On 𝓔_t, π(𝒮_far) ≤ e^{−t}.

Let S ∈ 𝒮_far and write L_S = λσ²t with λ > C″. By (2.3), (N2), (N3) with x_S ≤ C₃t:

 Q_S − ‖e‖² ≥ σ²t(λ − 2√(2C₃λ) − C₁) ≥ σ²t(λ/2 − C₁) (λ ≥ 32C₃).

With (2.4): D := Q_S − Q_{S₀} ≥ σ²t(λ/2 − C₁ − 1 − C_B) ≥ σ²tλ/4 > 0 (λ ≥ 4(C₁ + 1 + C_B)).

Then ((2b + Q_{S₀})/(2b + Q_S))^ν = (1 + D/(2b + Q_{S₀}))^{−ν}. Use log(1+u) ≥ (log 2)min(u, 1), ν ≥ n/2 and (2.5):

- if D ≥ 2b + Q_{S₀}, the factor is ≤ 2^{−n/2} ≤ e^{−c₄C″t} by (R4);
- otherwise ν log(1 + u) ≥ (n/2)(log 2)D/(2Nσ²) ≥ (log 2/4)(λt/4) ≥ c₄C″t.

Summing ℓ(S)/ℓ(S₀) with D_S ≥ 1, D_{S₀} ≤ (n+1)^{s₀}, Σ_{k≤K} q_k ≤ 1 and (W):

 π(𝒮_far) ≤ 2(2p)^{s₀}(n+1)^{s₀/2}e^{−c₄C″t} ≤ e^{(1 + s(A+2))ℓ − 2t} ≤ e^{−t},

since ℓ ≤ t/M₀ and M₀ ≥ 1 + s(A+2). ∎

## 5. Sizes above m = m_n(t)

**Claim.** There is an event 𝓜_t with P(𝓜_tᶜ) ≤ e^{−t} such that on 𝓔_t ∩ 𝓜_t, π(|S| > m) ≤ e^{−t}.

If m = K the mass is 0. Let m < K, so m equals the ceiling expression, and put E_m := {S ∈ Ω : |S| > m}.

*Numerator.* N_m := Σ_{S∈E_m} ϖ(S) m^c_{b₋}(S)/f₀(y_c). Since b₋ is data-free, `lem:num` gives E N_m = ϖ(E_m). Let 𝓜_t := {N_m ≤ e^t ϖ(E_m)}; Markov gives P(𝓜_tᶜ) ≤ e^{−t}.

*Denominator.* In the integral representation at (S₀, b₊), put v = σ²u with 1 ≤ u ≤ 1 + n^{−1/2}, and use Q_{S₀} ≤ σ²(E′ + ρ), ρ := c_ρ√t + B/σ² from (2.4). With log u ≤ u − 1 and 1/u ≥ 2 − u (the computation of [P1] `lem:den`), the exponent is

 ≥ ((u−1)/2)(E′/u − N) − ρ/(2u) ≥ −|E′ − N|/(2√n) − E′/(2n) − ρ/2 =: −Λ_n.

On 𝓔_t: |E′ − N|/(2√n) ≤ √t + t/√n and E′/(2n) ≤ 1, so by AM–GM and (R7)

 Λ_n ≤ (1 + c_ρ/2)√t + t/√n + 1 + B/(2σ²) ≤ t + C_S.

Restricting the integral to that interval (length σ²n^{−1/2}, IG ≥ c_IG):

 m^c_{b₊}(S₀)/f₀ ≥ D_{S₀}^{−1/2} c_IG σ² n^{−1/2} e^{−t − C_S}.

*Transfer.* By (2.2) and `thm:T01ii` (with Z^c_{b₊} ≥ ϖ(S₀)m^c_{b₊}(S₀), S₀ ∈ Ω), on 𝓔_t ∩ 𝓜_t:

 π(E_m) ≤ κ² f₀N_m/(ϖ(S₀)m^c_{b₊}(S₀)) ≤ c♯ · [ϖ(E_m)/ϖ(S₀)] · √(D_{S₀}) √n · e^{2t + C_S}.

*Prior ratio.* ϖ(E_m)/ϖ(S₀) = Σ_{k>m} q_k/w(s₀) ≤ 2(2p)^{s₀}2^{−m}, and by the definition of m, 2^{−m} ≤ 2^{−s₀}(2p)^{−s₀}(n+1)^{−(s₀+2)/2}e^{−3t}. With D_{S₀} ≤ (n+1)^{s₀}:

 π(E_m) ≤ 2c♯e^{C_S} n^{−1/2} e^{−t} ≤ e^{−t} by (R7). ∎

## 6. Intermediate sizes: d_t < |S| ≤ m

**Claim.** There is an event 𝓥_t with P(𝓥_tᶜ) ≤ 2K_s e^{−t} such that on 𝓔_t ∩ 𝓥_t, π(d_t < |S| ≤ m) ≤ e^{−t}.

If d_t ≥ m the set is empty. Write S_J := S₀ ∪ J for J ⊆ [p]∖S₀, and j* := min(m, p − s₀).

**(6a) Reduction to supersets, valid for every data set.** Let S ∈ Ω with d_t < |S| ≤ m.

- If S ⊇ S₀, then S = S_J with j₁ < |J| ≤ m − s₀ ≤ j*.
- Otherwise put J′ := S∖S₀ and S′ := S ∪ S₀ = S_{J′} (possibly ∉ Ω; ℓ is defined on all subsets). Then j₁ + 2 ≤ |J′| ≤ j*, and with a := |S₀∖S| ≤ s₀:
 ℓ(S)/ℓ(S′) = [w(|S|)/w(|S′|)]·(D_{S′}/D_S)^{1/2}·((2b + Q_{S′})/(2b + Q_S))^ν ≤ (2p)^a (n+1)^{a/2},
 by (W), (IL) and Q_{S′} ≤ Q_S.
- Each S_{J′} arises from at most 2^{s₀} − 1 such S.

Hence

 π(d_t < |S| ≤ m) ≤ 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2} Σ_{j=j₁+1}^{j*} Σ_{|J|=j} ℓ(S_J)/ℓ(S₀). (6.1)

**(6b) One superset on 𝓔_t.** Let 1 ≤ |J| = j ≤ j* and S = S_J.

- Since μ_c ∈ col X_{c,S}: Q_S ≥ ‖(I − P_S)e‖² = ‖e‖² − ‖P_{S₀}e‖² − σ²χ²_J.
- By (N1), (N2), (1.2): Q_S ≥ Nσ²(1 − ε), with ε ≤ ε̄_n ≤ ¼.
- With (2.4) and (N2) at T = S₀: 0 ≤ Δ := Q_{S₀} − Q_S ≤ σ²[χ²_J + C_A s₀ℓ + 5t + C_B].
- As Q_{S₀} ≥ Q_S > 0 and b > 0: ((2b + Q_{S₀})/(2b + Q_S))^ν ≤ (1 + Δ/Q_S)^ν ≤ e^{νΔ/Q_S}.
- ν/Q_S ≤ (n + 0.02)/(2Nσ²(1 − ε)) ≤ (1 + ε′)/(2σ²), with ε′ ≤ 2ε + 3/N ≤ ε̄′_n ≤ ½.
- By (N5), χ²_J ≤ τ_j, so (1 + ε′)χ²_J/2 ≤ χ²_J/2 + ε̄′_nτ_j/2.

Therefore on 𝓔_t

 ℓ(S_J)/ℓ(S₀) ≤ F_t · [w(s₀+j)/w(s₀)] (D_{S₀}/D_{S_J})^{1/2} e^{ε̄′_nτ_j/2} e^{χ²_J/2} 1{χ²_J ≤ τ_j}, (6.2)

 F_t := exp{(3/4)(C_A s₀ℓ + 5t + C_B)} ≤ exp{C_A sℓ + 4t + C_B}.

**(6c) Expectation.** Let V be the sum over j₁ < j ≤ j*, |J| = j, of the right side of (6.2) without F_t. It has a deterministic index set and weights, and χ²_J ~ χ²_{d_J} with 0 ≤ d_J ≤ j.

- *Uniform envelope before averaging.* For d = 0 the truncated moment is 1. For 1 ≤ d ≤ j it is ≤ (eτ_j/d)^{d/2}, and d ↦ (d/2) log(eτ_j/d) has derivative ½ log(τ_j/d) ≥ 0 since d ≤ j ≤ τ_j. So for every J the moment is ≤ (eτ_j/j)^{j/2}.
- For j > j₁ ≥ C′t/ℓ and C′ ≥ 1: τ_j/j ≤ (C_A + 4)ℓ.
- By (R5): e^{ε̄′_nτ_j/2} = e^{ε̄′_nC_A jℓ/2} e^{2ε̄′_n t} ≤ 2^{j/2}e^t.
- (ND; c_D, m) applies for j ≤ j*, and `lem:prior`(e) applies since s₀ + j ≤ p.

Together:

 E V ≤ Σ_{j>j₁} 2(j+1)^{s₀} 2^{−j} [c_D(n+1)]^{−j/2} 2^{j/2} e^t (e(C_A+4)ℓ)^{j/2} = 2e^t Σ_{j>j₁} (j+1)^{s₀} g^j,

with g² = e(C_A+4)ℓ/(2c_D(n+1)) ≤ 1/(4√n) by (R6). So g^j ≤ 2^{−j}n^{−j/4} and

 E V ≤ 2K_s e^t n^{−(j₁+1)/4} ≤ 2K_s e^{t − C′t/4} (j₁ℓ ≥ C′t).

**(6d) Markov and budget.** Let 𝓥_t := {V ≤ e^{−(6 + C_B)t}}. Then P(𝓥_tᶜ) ≤ 2K_s e^{(7 + C_B − C′/4)t} = 2K_s e^{−t} by the choice of C′.

On 𝓔_t ∩ 𝓥_t, by (6.1), (6.2):

 π(d_t < |S| ≤ m) ≤ exp{s(A+3)ℓ + C_A sℓ + 4t + C_B} · V ≤ e^{(5 + C_B)t} e^{−(6 + C_B)t} = e^{−t},

using s(A + 3 + C_A)ℓ = s(5A+9)ℓ ≤ t (M₀ ≥ s(5A+9)) and C_B ≤ C_B t. ∎

The three factors of S1-06 are paid here explicitly:

1. e^{‖P_{S₀}e‖²/(2σ²)} ≤ e^{(C_A s₀ℓ + 4t)/2}, inside F_t;
2. the union multiplicity 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2}, in (6.1);
3. the variance surcharge e^{ε̄′_n τ_j/2} ≤ 2^{j/2}e^t, with ε̄′_n ℓ → 0 uniformly in t because t ≤ n^{1−κ₀}.

All are absorbed by C′ and M₀.

## 7. Assembly

Let Bad := {‖μ̂ − μ‖² > Cσ²t} ∪ {|v/σ² − 1| > C√(t/n)} ∪ {|S| > d_t}. Since {|S| > d_t} ⊆ {|S| > m} ∪ {d_t < |S| ≤ m} and Ω ∩ {|S| ≤ d_t} = 𝒮_good ∪ 𝒮_far:

 Π(Bad | y) ≤ π(|S| > m) + π(d_t < |S| ≤ m) + π(𝒮_far) + max_{S∈𝒮_good} Π(Bad | S, y).

On 𝓔_t ∩ 𝓜_t ∩ 𝓥_t, §§3–6 give Π(Bad | y) ≤ e^{−t} + e^{−t} + e^{−t} + 3e^{−t} = 6e^{−t}. The failure probability is ≤ (6.4 + 1 + 2K_s)e^{−t}.

Since t ≥ M₀ℓ ≥ M₀ ≥ max{4, 2 log(4 + K_s)}: 6e^{−t} ≤ e^{−t/2} and (7.4 + 2K_s)e^{−t} ≤ 2e^{−t/2}. Hence, for all n ≥ n₀ and all t ∈ [M₀ log n, n^{1−κ₀}]:

 P_e[ Π(‖μ̂ − μ‖² > Cσ*²t or |v/σ*² − 1| > C√(t/n) or |S| > d_t | y) > e^{−t/2} ] ≤ 2e^{−t/2}.

This is Lemma X with c = ½, C, C′, M₀ as in §1 and n₀ from (R1)–(R7). ∎

## 8. Remarks

- **Where each hypothesis enters.**
 - (E): only (2.2).
 - (C): only through L_{S₀} ≤ B, i.e. (L₀; B) suffices.
 - (ND): only (6c), on j₁ < j ≤ min(m_n(t), p − s₀).
 - p ≤ n^A: the union bounds and the prefactors.
 - t ≤ n^{1−κ₀}: (R1)–(R5), in particular ε̄′_n log n → 0.
 - t ≥ M₀ log n: absorbing n^{O(s)} prefactors, and d_t log n ≲ t.
 - No eigenvalue condition on any set; s₀ = 0 is covered (S₀ = ∅, no underfits, K₀ = 1).
- **Constants.** C′ = 4(8 + C_B) does not depend on c_D; c_D enters only n₀ through (R6). M₀ is of order s(A+1). Any c < 1 is reachable by enlarging M₀.
- **Without (ND).** Dropping §6 and taking d_t := m_n(t) in §§3–4 gives the X′ variant: (1.1) becomes d_t ℓ ≤ C_m tℓ, so the mean radius becomes Cσ²tℓ and Λ becomes C″σ²tℓ. §§3–5 never use (ND). This is noted only, not written out here.

ATTEMPT X/X-a RESULT=PROVED GAPS=0
