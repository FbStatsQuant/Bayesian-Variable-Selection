# F-c-r2
stop_reason: end_turn

# Card F, route F-c — non-supersets via references T ⊆ S₀

**Outcome.** Partial. I prove (i) a deterministic bound showing the bias of non-supersets needs no polynomial comparison cost, (ii) an exact tilting identity that gives geometric bounds weighted by π(T) for any small deterministic reference family, and (iii) a reduction of the mean part of the distance clause to one fit tail. I also show by explicit design that the route as literally stated (references T ⊆ S₀ only, control ρ′_T) cannot close: under (E), (C) the adequate reference can lie outside 2^{S₀}. The card's question itself stays open (3 gaps).

Notation: σ := σ*, y := y_c, μ := μ_c, A_S := G_S + I, ρ′ := θ*ᵀA_{S₀}θ*/n ≤ M + M′. For T ⊆ S put W_{T,S} := M_S − M_T. For any S put S′ := S ∪ S₀, W_S := W_{S,S′}, Φ(S) := eᵀM_Se, Φ′(S) := Φ(S′).

## 1. Algebra (deterministic)

**Lemma 1.** Let T ⊆ S ⊆ [p], W = W_{T,S}.
- (a) 0 ⪯ W ⪯ M_S ⪯ P_S and rank W ≤ |S∖T|.
- (b) Q_T − Q_S = yᵀWy, μᵀWμ = L_T − L_S, eᵀWe = Φ(S) − Φ(T).
- (c) I − M_S = Σ_S⁻¹ with Σ_S := I + nX_{c,S}A_S⁻¹X_{c,S}ᵀ ⪰ I and det Σ_S = D_S.
- (d) I − W ≻ 0, (I − W)⁻¹ ⪯ Σ_S, and det(I − W) ≥ D_T/D_S.
- (e) Σ_T^{1/2} W Σ_T^{1/2} = I − Σ_T^{1/2}Σ_S⁻¹Σ_T^{1/2} ⪯ I.

*Proof.*
- (a) By [P1] `lem:spec`(a),(d), M_S = (n/(n+1))(I − R_S) with R_S := ((n+1)X_{c,S}X_{c,S}ᵀ + I)⁻¹, and M_T ⪯ M_S. With Δ := X_{c,S∖T}, Woodbury gives R_T − R_S = (n+1)R_TΔ(I + (n+1)ΔᵀR_TΔ)⁻¹ΔᵀR_T, of rank ≤ |S∖T|. M_S ⪯ P_S is `lem:spec`(b).
- (b) Definitions.
- (c) Woodbury: (I + X(nA⁻¹)Xᵀ)⁻¹ = I − X(A/n + G)⁻¹Xᵀ = I − nXH⁻¹Xᵀ, since A + nG = H. Sylvester: det Σ_S = det(A + nG)/det A = D_S.
- (d) I − W = Σ_S⁻¹ + M_T ⪰ Σ_S⁻¹ ≻ 0. Since Σ_T ⪰ I, W ⪯ W^{1/2}Σ_TW^{1/2}, so I − W ⪰ I − W^{1/2}Σ_TW^{1/2}. The latter has the spectrum of I − Σ_T^{1/2}WΣ_T^{1/2} = Σ_T^{1/2}Σ_S⁻¹Σ_T^{1/2} ≻ 0, whose determinant is D_T/D_S.
- (e) W = Σ_T⁻¹ − Σ_S⁻¹. ∎

**Lemma 2 (tilted gain).** Γ_{T,S} := μᵀ[(I − W)⁻¹ − I]μ = max_w{2wᵀμ − wᵀ(I − M_S)w − wᵀM_Tw} − ‖μ‖². Then:
- (a) Γ_{T,S} ≥ L_T − L_S ≥ 0.
- (b) If μ = X_{c,T}ϑ, then Γ_{T,S} ≤ ϑᵀA_Tϑ/n for every S ⊇ T. In particular Γ_{S₀,S} ≤ ρ′ for all S ⊇ S₀.
- (c) For any ϑ ∈ ℝ^T, g := X_{c,T}ϑ, r := μ − g: Γ_{T,S} ≤ ϑᵀA_Tϑ/n − 2gᵀr + n rᵀX_{c,S}A_S⁻¹X_{c,S}ᵀr.

*Proof.* (a) (I − W)⁻¹ − I ⪰ W. (c) Split 2wᵀμ = 2wᵀg + 2wᵀr. With c = X_{c,T}ᵀw and M_T = X_T(G_T + A_T/n)⁻¹X_Tᵀ, 2cᵀϑ − cᵀ(G_T + A_T/n)⁻¹c ≤ ϑᵀ(G_T + A_T/n)ϑ = ‖g‖² + ϑᵀA_Tϑ/n. Also max_w{2wᵀr − wᵀΣ_S⁻¹w} = rᵀΣ_Sr. Subtract ‖g + r‖². (b) is (c) with r = 0. ∎

**Lemma 3 (oracle-variance Bayes factor).** Let BF°(S:T) := (D_T/D_S)^{1/2}exp{yᵀWy/(2σ²)}, e ~ N(0, σ²I). Then:
- (a) E BF°(S:T) = (D_T/D_S)^{1/2}det(I − W)^{−1/2}e^{Γ_{T,S}/(2σ²)} ≤ e^{Γ_{T,S}/(2σ²)}.
- (b) For every event F, E[BF°·1_F] = E[BF°]·P̃(F), where under P̃, e ~ N((I − W)⁻¹Wμ, σ²(I − W)⁻¹).
- (c) P̃(eᵀW_Se > τ) ≤ 2^{s₀/2}exp{−(τ − 2Γ_{T,S})/(8σ²)}.

*Proof.*
- (a), (b): yᵀWy = eᵀWe + 2(Wμ)ᵀe + μᵀWμ. The Gaussian integral ∫exp{−[eᵀ(I − W)e − 2(Wμ)ᵀe]/(2σ²)} gives det(I − W)^{−1/2}exp{μᵀW(I − W)⁻¹Wμ/(2σ²)}, and W + W(I − W)⁻¹W = (I − W)⁻¹ − I. The inequality is Lemma 1(d).
- (c): under P̃ write e = m̃ + σ(I − W)^{−1/2}z and B := (I − W)^{−1/2}W_S(I − W)^{−1/2}. By Lemma 1(d),(e) applied to (S, S′), ‖B‖ ≤ ‖Σ_S^{1/2}W_SΣ_S^{1/2}‖ ≤ 1, and rank B ≤ s₀.
- Hence eᵀW_Se ≤ 2m̃ᵀW_Sm̃ + 2σ²χ²_{≤s₀}, and m̃ᵀW_Sm̃ ≤ μᵀW(I − W)⁻¹Wμ ≤ Γ_{T,S}. Conclude with [P1] `lem:chi`(a). ∎

## 2. Proposition B: the bias of non-supersets costs no polynomial factor

Let 𝓗₁ := {‖e‖² ≤ Nσ²(1 + log n/√N)}. By [P1] `lem:chi`(b), P(𝓗₁ᶜ) ≤ 2/log²n. Put Λ_n(ω) := 5σ²[s₀ log(2p) + (s₀/2)log(n+1) + ω].

**Proposition B.** Assume (E), (C). There is n₀(M, M′, σ²) such that for n ≥ n₀ and every ω ≥ 0 with Λ_n(ω) ≤ 5σ²n/4, on 𝓗₁:

  π({S ∈ Ω : S ⊉ S₀, S′ ∈ Ω, L_S > ρ′ + 2eᵀW_Se + 2Λ_n(ω)}) ≤ (2^{s₀} − 1)e^{−ω}.

No eigenvalue condition, no union bound over models, no p ≤ n^A.

*Proof.* Fix such S, r := |S₀∖S|.
- Prior and determinant: w(|S|)/w(|S′|) ≤ (2p)^r by [P1] `lem:prior`(b). D_{S′}/D_S ≤ (n+1)^r by Cauchy interlacing (λ_i(G_{S′}) ≤ λ_i(G_S) for i ≤ |S|) and f < n+1 (`lem:spec`(e)).
- Likelihood: Q_S = Q_{S′} + yᵀW_Sy, and yᵀW_Sy ≥ ½μᵀW_Sμ − eᵀW_Se ≥ ½(L_S − ρ′) − eᵀW_Se > Λ_n(ω), using L_{S′} ≤ L_{S₀} ≤ ρ′.
- Denominator: Q_{S′} ≤ Q_{S₀} ≤ ‖y − X_{c,S₀}θ*‖² + ρ′ = ‖e‖² + ρ′. On 𝓗₁ with (E), 2b = 0.02‖y‖²/N ≤ 0.06M + 0.08σ². So B₀ := 2b + Q_{S′} ≤ 1.25Nσ² for n ≥ n₀.
- Combine: ((2b + Q_{S′})/(2b + Q_S))^ν ≤ (1 + Λ/B₀)^{−ν} ≤ exp{−(ν/2)min(Λ/B₀, 1)} ≤ exp{−Λ/(5σ²)}. Hence π(S)/π(S′) ≤ (2p)^{s₀}(n+1)^{s₀/2}e^{−Λ/(5σ²)} = e^{−ω}.
- Each S′ ⊇ S₀ arises from at most 2^{s₀} − 1 sets S, and Σπ(S′) ≤ 1. ∎

*Reading.* A non-superset with ridge bias above ρ′ + O(log n) + 2eᵀW_Se is negligible against its own union. The only random quantity left is the rank-≤ s₀ form eᵀW_Se ≤ Φ′(S) − Φ(S).

## 3. Theorem A: geometric bounds weighted by π(T), any small reference family

Assume p ≤ n^A, C_A := 10 + 4A, m ≤ C_m log n deterministic. Let 𝓗 := 𝓗(m) be the intersection of:
- (H1) |‖e‖² − Nσ²| ≤ σ²√N log n;
- (H2) ‖P⁺_Se‖² ≤ σ²C_A(|S| + 1)log n for all |S| ≤ m, where P⁺_S projects onto col X_{c,S} + ℝμ (rank ≤ |S| + 1).

As in [P1] `lem:good` (rank k + 1, x_k = k(log p + 1) + log n), P(𝓗ᶜ) ≤ 2/log²n + 2/n.

On 𝓗, for |S| ≤ m: Q_S ≥ ‖(I − P_S)y‖² ≥ ‖e‖² − ‖P⁺_Se‖² ≥ Nσ²(1 − δ_n), with δ_n := log n/√N + C_A(m+1)log n/N. The middle step: with a = (I − P_S)μ, ‖(I − P_S)e‖² + 2aᵀe + ‖a‖² ≥ ‖(I − P_S)e‖² − (aᵀe)²/‖a‖², and a ∈ range P⁺_S, a ⊥ col X_{c,S}.

For T ∈ Ω and γ ≥ 0 let 𝒞_T(γ) := {S ∈ Ω : S ⊇ T, |S| ≤ m, Γ_{T,S} ≤ γ}. This class is deterministic.

**Theorem A.** For n ≥ n₀ (δ_n ≤ ½), every T ∈ Ω (t := |T|), γ ≥ 0, j ≥ 0, τ ≥ 0, with 1 + ε_n := (n + 0.02)/(N(1 − δ_n)) and ς_n := ε_n[C_A(m+1)log n + γ/σ²] → 0:

- (a) E[1_𝓗 Σ_{S∈𝒞_T(γ), |S∖T|=j} π(S)/π(T)] ≤ 2·C(t+j, j)·2^{−j}·e^{ς_n + γ/(2σ²)}.
- (b) E[1_𝓗 Σ_{S∈𝒞_T(γ), |S∖T|=j} (π(S)/π(T))·1{eᵀW_Se > τ}] ≤ (a)-bound × 2^{s₀/2}e^{−(τ−2γ)/(8σ²)}.

*Proof.* On 𝓗, with W = W_{T,S}: π(S)/π(T) ≤ [w(t+j)/w(t)](D_T/D_S)^{1/2}exp{ν yᵀWy/(2b + Q_S)} ≤ [w(t+j)/w(t)]·BF°(S:T)·exp{ε_n yᵀWy/(2σ²)}. Also yᵀWy ≤ 2eᵀWe + 2μᵀWμ ≤ 2‖P_Se‖² + 2γ. Drop 1_𝓗, apply Lemma 3(a) (resp. (b), (c)), then [P1] `lem:prior`(e) with s₀ → t (its proof holds for any t with t + j ≤ p). ∎

**Corollary A1.** Let 𝒯 ⊆ Ω be a finite deterministic family (chosen from (X, θ*), not from e) with γ_T ≤ γ. Using Σ_Tπ(T)Y_T ≤ max_T Y_T, Markov with weights 1/(j(j+1)), and Σ_{j≥0}C(t+j, j)2^{−j} = 2^{t+1}:

1. With probability ≥ 1 − 1/x − P(𝓗ᶜ), for all j ≥ 1 simultaneously, π{S : ∃T ∈ 𝒯, S ∈ 𝒞_T(γ), |S∖T| = j} ≤ x|𝒯|·j(j+1)·2 max_t C(t+j, j)·2^{−j}e^{ς_n + γ/(2σ²)}.
2. E[1_𝓗 π{S ∈ ∪_𝒯𝒞_T(γ) : eᵀW_Se > τ}] ≤ Σ_{T∈𝒯}2^{|T|+2}·2^{s₀/2}e^{ς_n + 3γ/(4σ²)}e^{−τ/(8σ²)}.

Three consequences:
- **Supersets.** With 𝒯 = {S₀} and γ = ρ′ (Lemma 2(b)), Σ_{|J|=j, |S|≤m}π(S₀∪J)/π(S₀) ≤ poly(j)·2^{−j}·e^{ρ′/(2σ²)}·O_P(1). This removes Lemma V's η: ratio exactly ½, no e^{C√(ρ′j)}.
- **Trace references.** With 𝒯 = 2^{S₀} and T = S ∩ S₀, the comparison cost (2p)^{s₀}(n+1)^{s₀/2} of [T03R] (C6)(a) is replaced by 3^{s₀}-type constants on the class 𝒞 := ∪_{T⊆S₀}𝒞_T(γ).
- **Bias on the class.** Proposition B plus item 2 give: π{S ∈ 𝒞 : S′ ∈ Ω, L_S > ρ′ + 2τ + 2Λ_n(ω)} ≤ (2^{s₀} − 1)e^{−ω} + O_P(e^{−τ/(8σ²)}). With τ = M_n log n and ω = log n, the bias clause holds on 𝒞 at scale M_n log n under (E), (C) alone.

**Limitation (stated, not hidden).** Γ_{T,S} is a mean-level quantity: it is about d ≈ n times the signal gain in strong new directions. Lemma 2(c) bounds it only when the residual r is nearly orthogonal to col X_S. Enlarging 𝒞 to "L_T − L_S ≤ λ" needs truncated moments, which is F-a's machinery.

## 4. Theorem R: the mean part reduces to one fit tail

**Theorem R.** Assume (E), (C), n ≥ n₀, and that S ∪ S₀ ∈ Ω whenever |S| ≤ m (automatic if K = p, or if m + s₀ ≤ K). On 𝓗₁, for all τ, x ≥ 0 and ω as in Proposition B:

  Π(‖μ̂ − μ‖² > a_n + 9τ | y) ≤ π(Φ′(S) > τ) + π(|S| > m) + (2^{s₀} − 1)e^{−ω} + e^{−x} + e^{−0.09n},

with a_n := 3(5M + 9σ²)(2m log 2 + 4x) + 3ρ′ + 6Λ_n(ω).

*Proof.* Given (S, v, y), X_{c,S}θ − μ = X_{c,S}(θ − θ̂) + M_Se − (I − M_S)μ. So ‖μ̂ − μ‖² ≤ 3‖X_{c,S}(θ − θ̂)‖² + 3Φ(S) + 3L_S.
- The first term is N(0, vM_S), so it is ≤_st vχ²_{|S|} ≤ v(2m log 2 + 4x) outside conditional probability e^{−x} (`lem:chi`(a)).
- v = (b + Q_S/2)/g with g ~ Gamma(ν, 1). Chernoff gives P(g ≤ ν/2) ≤ (e^{1/2}/2)^ν ≤ e^{−0.09n}. On 𝓗₁, b + Q_S/2 ≤ 0.51‖y‖² ≤ 0.51(2nM + 4Nσ²), so v ≤ 5M + 9σ².
- Outside the set of Proposition B (supersets have L_S ≤ ρ′), L_S ≤ ρ′ + 2(Φ′(S) − Φ(S)) + 2Λ_n(ω). Use Φ(S) ≤ Φ′(S). ∎

**Corollary R1 (in R1: s₀ ≥ 1 fixed, p ≤ n^A).** Take m = m♯_n ≤ C_m log n ([T03R] E2(i)) and x = ω = log n, so a_n = O(log n). The term π(|S| > m♯_n) is O_P(n^{−1/2}) by [W3P] Lemma 1a′ with T = S₀. That lemma has status "PROVED (by this seat, unchecked)" and is consumed here as a hypothesis. Then:

  if (FT) π(eᵀM_{S∪S₀}e > M_n log n | y) → 0 in probability for every M_n → ∞, then Π(‖μ̂ − μ‖² > M_n log n | y) → 0 in probability for every M_n → ∞.

So for the mean part, non-supersets need no separate bias argument and no S₀-comparison. Everything is in (FT). Its rank-s₀ piece {eᵀW_Se > τ/2} is settled on 𝒞 by Corollary A1(2).

## 5. Proposition O: why references T ⊆ S₀ cannot suffice

**(i) The S₀-comparison cost is real, and weighting by π(T) cures it.** Take X_{S₀} orthogonal and θ*_j = a/√N for j ∈ S₀, so ‖μ‖² = s₀a². Then D_{S₀} = n^{s₀}, w(0)/w(s₀) = C(2p−1, s₀), and Q_∅ − Q_{S₀} ≤ ‖P_{S₀}y‖² = O_P(1). Hence π(∅)/π(S₀) ≥ ((2p−1)/s₀)^{s₀}n^{s₀/2}e^{−O_P(1)}. No bound on non-supersets normalised by π(S₀) can avoid the factor p^{s₀}n^{s₀/2}. Here T = ∅ is an adequate reference (L_∅ = s₀a²) and Theorem A applies with weight π(∅).

**(ii) Proxy design: the adequate reference is outside 2^{S₀}.** Let u, v be centred orthonormal, κ, c > 0 fixed, ε := κ/(2√N), p ≥ 3.
- Columns: x₁ = √N(√(1−ε²)v + εu), x₂ = √N(√(1−ε²)v − εu), x₃ = √N u; other columns arbitrary.
- Truth: θ* = √n·c(e₁ − e₂), so S₀ = {1, 2} and μ = cκ√n·u.
- Interfaces: (E; c²κ²) and (C; 2c²) hold, ρ′ = c²(κ² + 2).

Computations:
- D_{{3}} = n. G_{S₀} has eigenvalues 2N − κ²/2 and κ²/2, so D_{S₀} ≥ n(n+1)κ²/(κ² + 2). w(1)/w(2) = p − 1.
- Q_{{3}} ≤ ‖y‖² − (uᵀy)²(1 − 1/N), and Q_{S₀} ≥ ‖y‖² − (uᵀy)² − (vᵀe)². So Q_{{3}} − Q_{S₀} ≤ (vᵀe)² + (uᵀy)²/N = O_P(1).
- Hence **π({3})/π(S₀) ≥ (p − 1)√(n+1)·(κ²/(κ²+2))^{1/2}·e^{−O_P(1)} → ∞**.
- On {|uᵀe| ≤ cκ√n/2, ‖e‖² ≤ 2Nσ²} (probability → 1): Q_∅ − Q_{{3}} ≥ nc²κ²/6 and 2b + Q_∅ ≤ 4.04n(c²κ² + σ²). With c₃ := c²κ²/(24.24(c²κ² + σ²)), **π({3})/π(∅) ≥ e^{c₃n/2}/((2p−1)√n)**.

Consequences. S = {3} is a non-superset with trace T = ∅, and it dominates S₀ by a factor ≍ p√n. For its trace, ρ′_∅ = L_∅ = nc²κ² and Γ_{∅,{3}} = (n−1)·nc²κ². So "Σ_J π(T∪J)/π(T) ≤ geometric·O_P(1) with ρ′_T controlled, T ⊆ S₀" is false under (E), (C); the ratio is e^{cn}. The adequate reference is {3} itself (μ = φx₃, cost φ² = O(1)). Theorem A handles it only if {3} ∈ 𝒯.

In general the adequate references are the minimal models with bounded ridge cost. Their number is not bounded by a function of s₀, and a union over them brings back the log p-per-dimension entropy. This is the precise point where F-c stops.

## 6. Gaps

- **GAP 1.** The self-fit tail π(S ⊉ S₀ : eᵀM_Se > τ) at τ = M_n log n. This is the part of (FT) not covered by Corollary A1(2). It needs truncated, direction-wise moments (route F-a) run with reference T instead of S₀.
- **GAP 2.** Non-supersets outside ∪_{T⊆S₀}𝒞_T(γ): the proxy class of Proposition O(ii), and traces with bounded but not tiny signal gain. This needs (a) truncation to replace Γ_{T,S} by L_T − L_S, and (b) a data-independent reference family beyond 2^{S₀} with controlled cardinality. Neither is done.
- **GAP 3.** The variance clause |v/σ² − 1| ≤ C√(t/n) and every exponential-form statement are not treated. Theorem R is in-probability and covers the mean part only.

Consumed unchecked: [W3P] Lemma 1a′, in Corollary R1 only.

ATTEMPT F/F-c RESULT=PARTIAL GAPS=3
