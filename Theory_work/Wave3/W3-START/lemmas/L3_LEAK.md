# L3 — Lemma J, bridge (B-L) ⇒ [LEAK(Q)], bridge (B1), level vectors and Corollary F4

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Statement proved: `STATEMENT.md` §2 (J0)–(J3); §4 [LEAK(Q)]; §5.2 (B1) (leakage part), (B-L); the arithmetic of
Corollary F4 (§5.3 (T2)). Uses `lemmas/L2_TK.md` (event 𝓔^blk, (TK-a)–(TK-f), constants κ_E, ω_n, ϑ_n, n₁).

## L3.1 Lemma J

For d ∈ ℝ, t ≥ σ > 0, h ≥ 1 and Z ~ N(0, 1): J_h(d, t) := E[exp((d + σZ)²/(2t²))·1{|Z| ≤ h}]. Write a := σ²/t² ∈ (0, 1].
The integrand is exp(d²/(2t²))·exp(dσz/t² + az²/2)·φ(z), φ the standard normal density.

**(J0)** J_h(d, t) ≥ P(|Z| ≤ 1)·exp(d²/(2t²)) ≥ ¼ exp(d²/(2t²)).
*Proof.* exp(az²/2) ≥ 1 and, by symmetry of Z, E[exp(dσZ/t²)1{|Z| ≤ h}] = E[cosh(dσZ/t²)1{|Z| ≤ h}] ≥ P(|Z| ≤ h)
≥ P(|Z| ≤ 1) > 0.68. ∎
**(J1)** If t > σ: J_h(d, t) ≤ E exp((d + σZ)²/(2t²)) = (t/√(t² − σ²))·exp(d²/(2(t² − σ²))).
*Proof.* For W ~ N(m, 1) and λ < ½: E e^{λW²} = (1 − 2λ)^{−1/2}exp(λm²/(1 − 2λ)). Apply with W = d/σ + Z, λ = a/2 < ½:
(1 − a)^{−1/2}exp((d²/(2t²))/(1 − a)), and t²(1 − a) = t² − σ². ∎
**(J2)** J_h(d, t) ≤ √(2/π)·h·exp(d²/(2t²) + |d|σh/t²).
*Proof.* On |z| ≤ h: exp(dσz/t²) ≤ exp(|d|σh/t²) and exp(az²/2)φ(z) ≤ exp(z²/2)φ(z) = (2π)^{−1/2}; ∫_{−h}^{h}dz = 2h. ∎
**(J3)** J_h(0, σ) = ∫_{−h}^{h}e^{z²/2}φ(z)dz = √(2/π)·h. ∎
**(J4) Monotonicity in h.** J_h(d, t) is nondecreasing in h; in particular J_h ≤ J_{z_n} for h ≤ z_n.

## L3.2 Level vectors, the event 𝓩_h, and bridge (B1) for the functionals

Fix a deterministic Q ⊇ S₀ with |Q| ≤ K and a level vector h = (h_l)_{l∉Q}, 1 ≤ h_l ≤ z_n, a function of (X, θ*, σ, Q).
In Setting F all of (X, θ*, Q, h) and the partition are deterministic.
  **𝓩_h := {|Z_{T,l}| ≤ h_l for every l ∉ Q and every T ⊆ C_{b(l)} ∖ {l}}.**
Each Z_{T,l} ~ N(0, 1) ((TK-e); u_{T,l} is a deterministic unit vector), and a column l has at most 2^{15} sets
T ⊆ C_{b(l)} ∖ {l}. With P(|Z| > h) ≤ 2e^{−h²/2}:
  **P(𝓩_hᶜ) ≤ Σ_{l∉Q}2^{15}·2e^{−h_l²/2} = b_n(h).**
*Default levels.* h ≡ z_n: b_n(h) ≤ 2^{16}p·exp(−log(2^{21}p) − log log n) = 1/(32 log n).

**(B1), functionals.** For every partition with blocks of size ≤ 16:
(i) 𝔏^b_n(Q; h) ≤ 𝔏_n(Q; h): for l ∉ Q the sets {T : U*_{b(l)} ⊆ T ⊆ C_{b(l)} ∖ {l}} satisfy T ⊆ [p] ∖ {l}, |T| ≤ 15.
(ii) 𝔏^{b,0}_n(h) ≤ 𝔏^b_n(S₀; h) (T = U*_{b(l)} is one of the sets of (i) with Q = S₀).
(iii) 𝔏^{b,0}_n(h) ≤ 𝔏⁰_n(h). Let l ∉ S₀, b = b(l); |U*_b| ≤ 15 since l ∈ C_b ∖ S₀. If U*_b ⊊ S₀, the term
J_{h_l}(δ_{U*_b,l}, τ_{U*_b}) is among those maximised in 𝔏⁰_n(h). If U*_b = S₀ (all truths in the block of l; when s₀ ≥ 1
there are at most 15 such l), then (I − P_{S₀})μ = 0, so δ_{S₀,l} = 0 and τ_{S₀} = σ, and the term is
J_{h_l}(0, σ) = √(2/π)h_l ≤ √(2/π)z_n by (J3). If s₀ ≥ 1 these at most 15 terms are covered by 15√(2/π)z_n/p; if s₀ = 0
every l is of this kind (U*_b = ∅ = S₀, μ = 0) and 𝔏^{b,0}_n(h) = √(2/π)p⁻¹Σ_l h_l = 𝔏⁰_n(h). ∎

## L3.3 The step bound in the small-gain regime

  z̄_n² := 2 log(2^{21}) + 2A log n + 2 log log n   (z_n ≤ z̄_n whenever p ≤ n^A),
  g⁰_n := (2A + 1) log n + 2 log 4,   g_n := 2g⁰_n + 2z̄_n²,   x̄_n := g_n/((n − 1)(1 − ω̄_n)),
  ς_n := (g_n/2)·[(1 + ϑ̄_n)(1 + x̄_n) − 1],   1 + ϑ̄_n := (n + 0.02)/((n − 1)(1 − ω̄_n))   (ϑ_n ≤ ϑ̄_n for n ≥ n₁).
These are uniform envelopes: all of them depend only on (n, A), not on p or the design. g_n = O(log n), x̄_n → 0 and
ς_n = O(n^{−1/3}log n) → 0 (this is where ω̄_n log n → 0 is used). Let n₂ = n₂(A) ≥ n₁ be such that x̄_n ≤ ½ and ς_n ≤ 1 for
n ≥ n₂.

**Lemma L3.3.** On 𝓔^blk, for n ≥ n₂, for every block b, T ⊆ C_b and l ∈ C_b ∖ T with
  δ²_{T,l} ≤ g⁰_n·τ²_T  and  |Z_{T,l}| ≤ z_n:
  **r_b(T ∪ {l})/r_b(T) ≤ e^{2κ_E+1}·(n + 1)^{−1/2}·exp((δ_{T,l} + σZ_{T,l})²/(2τ²_T)).**
*Proof.* By (TK-d), log[r_b(T ∪ l)/r_b(T)] ≤ −½ log(n + 1) + ν log(RSS_T/RSS_{T∪l}) + 2κ_E. By (TK-e),
RSS_T − RSS_{T∪l} = (δ + σZ)² ≤ 2δ² + 2σ²Z² ≤ τ²_T(2g⁰_n + 2z_n²) ≤ τ²_Tg_n (σ² ≤ τ²_T; z_n ≤ z̄_n). By (TK-a),
x := (RSS_T − RSS_{T∪l})/RSS_T ≤ g_n/((n − 1)(1 − ω_n)) ≤ x̄_n ≤ ½. By (TK-f)(f3),
ν log(RSS_T/RSS_{T∪l}) ≤ (1 + ϑ_n)(1 + x̄_n)(δ + σZ)²/(2τ²_T) ≤ (δ + σZ)²/(2τ²_T) + ς_n, and ς_n ≤ 1. ∎

**Small gains from the averaged condition.** Let l ∉ Q, T ⊆ [p] ∖ {l}, and suppose J_{h_l}(δ_{T,l}, τ_T) ≤ p√n. Then by (J0)
δ²_{T,l}/(2τ²_T) ≤ log(4p√n), i.e. **δ²_{T,l} ≤ τ²_T(2 log(4p) + log n) ≤ g⁰_nτ²_T** (p ≤ n^A). In particular:
(SG-b) if (|Q| + 1)n^{−1/2}𝔏^b_n(Q; h) ≤ 1, then δ²_{T,l} ≤ g⁰_nτ²_T for every l ∉ Q and U*_{b(l)} ⊆ T ⊆ C_{b(l)} ∖ {l}
(each such J is ≤ p𝔏^b_n(Q; h) ≤ p√n);
(SG-0) if n^{−1/2}𝔏^{b,0}_n(h) ≤ 1, then δ²_{T,l} ≤ g⁰_nτ²_T for every l ∉ S₀ and T = U*_{b(l)};
(SG) if ϱ_n(Q; h) ≤ 1, then δ²_{T,l} ≤ g⁰_nτ²_T for every l ∉ Q and every T ⊆ [p] ∖ {l} with |T| ≤ 15 — the consequence
quoted under (AL) in `STATEMENT.md` §3.1, with constant 2A + 1 + o(1).

## L3.4 Bridge (B-L): [LEAK(Q)] in explicit form

**Proposition L3.4.** Setting F, (E), (GF-16); Q, h as in L3.2; n ≥ n₂; c_L := 2^{15}e^{2κ_E+1}. For every λ > 0:
(a) if (|Q| + 1)n^{−1/2}𝔏^b_n(Q; h) ≤ 1:
  **P(U_Q > λ·n^{−1/2}𝔏^b_n(Q; h)) ≤ P((𝓔^blk)ᶜ) + b_n(h) + c_L/λ;**
(b) if Q = S₀, s₀ < K and n^{−1/2}𝔏^{b,0}_n(h) ≤ 1:
  **P(T₁ > λ·(s₀ + 1)·n^{−1/2}𝔏^{b,0}_n(h)) ≤ P((𝓔^blk)ᶜ) + b_n(h) + e^{2κ_E+1}/λ.**
Consequently, along a sequence with b_n(h) → 0: U_Q = O_P(n^{−1/2}𝔏^b_n(Q; h)) under the premise of (a) and
T₁ = O_P(n^{−1/2}𝔏^{b,0}_n(h)) under that of (b): this is [LEAK(Q)]. The bounds are uniform in (X, θ*, Q, h).

*Proof.* (a) If [p] ∖ Q = ∅ then U_Q = 0. Otherwise, for l ∉ Q let 𝒯_l := {T : U*_{b(l)} ⊆ T ⊆ C_{b(l)} ∖ {l}} (|𝒯_l| ≤ 2^{15}) and
  V := p⁻¹Σ_{l∉Q}Σ_{T∈𝒯_l}exp((δ_{T,l} + σZ_{T,l})²/(2τ²_T))·1{|Z_{T,l}| ≤ h_l}.
Since Z_{T,l} ~ N(0, 1): E V = p⁻¹Σ_{l∉Q}Σ_{T∈𝒯_l}J_{h_l}(δ_{T,l}, τ_T) ≤ 2^{15}𝔏^b_n(Q; h). On 𝓔^blk ∩ 𝓩_h, by (SG-b), h_l ≤ z_n and
Lemma L3.3, for every l ∉ Q:
  m_l = max_{T∈𝒯_l}r_b(T ∪ l)/r_b(T) ≤ e^{2κ_E+1}(n + 1)^{−1/2}·Σ_{T∈𝒯_l}exp((δ_{T,l} + σZ_{T,l})²/(2τ²_T))1{|Z_{T,l}| ≤ h_l},
so U_Q = p⁻¹Σ_{l∉Q}m_l ≤ e^{2κ_E+1}(n + 1)^{−1/2}V. Hence, by Markov's inequality (𝔏^b_n(Q; h) > 0),
P(U_Q > λn^{−1/2}𝔏^b_n(Q; h)) ≤ P((𝓔^blk)ᶜ) + P(𝓩_hᶜ) + P(e^{2κ_E+1}V > λ𝔏^b_n(Q; h)) ≤ P((𝓔^blk)ᶜ) + b_n(h) + 2^{15}e^{2κ_E+1}/λ.
(b) T₁ = [(s₀ + 1)/(2p − 1 − s₀)]Σ_{l∉S₀}r_b(U*_b ∪ l)/r_b(U*_b) ≤ ((s₀ + 1)/p)Σ_{l∉S₀}r_b(U*_b ∪ l)/r_b(U*_b) (s₀ ≤ p − 1). On
𝓔^blk ∩ 𝓩_h, by (SG-0) and Lemma L3.3 with T = U*_{b(l)}: T₁ ≤ (s₀ + 1)e^{2κ_E+1}(n + 1)^{−1/2}V₀,
V₀ := p⁻¹Σ_{l∉S₀}exp((δ + σZ)²/(2τ²))1{|Z| ≤ h_l} at T = U*_{b(l)}, E V₀ = 𝔏^{b,0}_n(h). Markov as in (a). ∎

*Remarks.* (1) The union bound behind b_n(h) is over the conditioning sets inside the **actual** blocks (at most 2^{15}
per column); the partition-free maximum over all 15-sets appears only in the deterministic dominating functional
𝔏_n(Q; h). (2) The expectation of the maximum over T is bounded by the sum (factor 2^{15}); no independence between
the Z_{T,l} is used. (3) Levels must not depend on the response: the argument conditions on nothing but the design.

## L3.5 Corollary F4 (arithmetic of the non-default levels)

Let I_n ⊆ [p] ∖ Q, |I_n| ≤ ī, δ²_{U,l} ≤ c·τ²_U log n for l ∈ I_n and all U ⊆ [p] ∖ {l}, |U| ≤ 15; c < 1 + 2A̲ fixed;
h_l := min(z_n, √(4 log log n)) for l ∈ I_n, h_l := z_n otherwise.
* *h is a level vector.* For n ≥ 4: 4 log log n ≥ 4 log log 4 > 1.3 and z_n² > 2 log(2^{21}) > 29, so 1 ≤ h_l ≤ z_n.
* *Budget.* b_n(h) ≤ 1/(32 log n) + 2^{16}ī·max{(log n)^{−2}, 1/(2^{21}p log n)} → 0.
* *Functional.* For l ∈ I_n and |U| ≤ 15, by (J2) with |d|/t ≤ √(c log n), σ/t ≤ 1 and h_l ≤ √(4 log log n):
  J_{h_l}(δ_{U,l}, τ_U) ≤ √(2/π)·√(4 log log n)·exp((c/2) log n + √(4c·log n·log log n)) = n^{c/2+o(1)},
  where o(1) depends only on (n, c). For l ∉ Q ∪ I_n the terms are those of the default functional. Hence
  ϱ_n(Q; h) ≤ ϱ^{−I}_n(Q) + (|Q| + 1)·n^{−1/2}·p⁻¹·ī·n^{c/2+o(1)} = ϱ^{−I}_n(Q) + (|Q| + 1)·n^{−(1+2A̲−c)/2+o(1)},
  using p ≥ n^{A̲−o(1)}. So (AL) holds with this h when ϱ^{−I}_n(Q) → 0 and (|Q| + 1)n^{−κ₁} → 0 for some κ₁ < (1 + 2A̲ − c)/2. ∎
* *Default levels on the same column (remark in F4).* (J2) with h = z_n = √((2A + o(1)) log n) when log p/log n → A gives
  n^{c/2+√(2Ac)+o(1)}, i.e. a charge n^{(c−1)/2+√(2Ac)+o(1)}/p = n^{(c−1)/2+√(2Ac)−A+o(1)} in ϱ_n/(|Q| + 1), hence (|Q| + 1) times
  this in ϱ_n. The exponent of the normalised charge is negative iff √c < √(4A + 1) − √(2A), and
  (√(4A + 1) − √(2A))² < 1 + 2A; for growing |Q| the factor |Q| + 1 must be paid as well, as in F4.
