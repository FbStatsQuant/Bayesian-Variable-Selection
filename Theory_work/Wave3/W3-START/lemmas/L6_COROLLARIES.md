# L6 — Corollaries F1–F4 (T2), and the high-probability form of (T1)(d)

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Statement proved: `STATEMENT.md` §5.3 (T2) F1, F2, F3, F4. Uses `lemmas/L3_LEAK.md` (Lemma J; L3.5),
`lemmas/L5_ASM_STARTF.md` (Proposition L5.2, Theorem (T1)(a)–(c)), `lemmas/L1_AGG_FLOOR.md` ((T0)).
Setting throughout: Setting F, (E), (GF-16), visibility with exponent κ_V, default levels h ≡ z_n unless stated;
z̄_n² := 2 log(2^{21}) + 2A log n + 2 log log n ≥ z_n² (p ≤ n^A); s₀′ := max(s₀, 1).

## L6.0 How n₀ in Proposition L5.2 depends on ε; high-probability form

**Lemma L6.0.** In Proposition L5.2 the threshold n₀(ε, κ) can be taken as max(n*(κ), n_ε), where
* n*(κ) depends only on κ and the fixed constants: it is the least m such that for all n ≥ m:
  n ≥ max(n₂, 2s₀ + 2), n ≥ n₃ or n₄ (the threshold of Proposition L4.1 or L4.2 for the exponent κ′ = (κ + κ_V)/2),
  2s₀n^{−κ′}(4/3)^{16s₀+1} ≤ n^{−κ}, and s₀n^{−κ′} ≤ ½;
* n_ε is the least m such that 2e^{−n^{1/3}} + 2/n + 1/log n ≤ ε/2 for all n ≥ m.
*Proof.* These are exactly the requirements placed on n₀ in the proof of L5.2 (`lemmas/L5_ASM_STARTF.md`, first
paragraph of the proof); ε enters only through the last one. ∎

**Corollary L6.0′ (high-probability form).** Put ε_n := 4/log n, λ_n := 4c_L/ε_n = c_L log n, c_{0,n} := 1/(64s₀′λ_n),
C_n := 43s₀′λ_n, C′_n := λ_n(s₀ + 1) + ½(s₀ + 1)(s₀ + 2)(4/3)^{s₀+3}λ_n². Let κ ∈ (0, κ_V). There is n**(κ), depending only on κ
and the fixed constants, such that for n ≥ n**(κ) and every admissible (X, θ*, Q, h) of L5.2 with ϱ_n(Q; h) ≤ c_{0,n}:
  P(1 − π₀(𝓛(Q)) > C_nϱ_n(Q; h) + n^{−κ}) ≤ 4/log n + b_n(h),
and for Q = S₀: P(o₀ > C′_n[n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)²] + n^{−κ}) ≤ 4/log n + b_n(h).
*Proof.* Apply L5.2 at each n with ε = ε_n: by L6.0 this is allowed once n ≥ n*(κ) and 2e^{−n^{1/3}} + 2/n ≤ 1/log n (then
2e^{−n^{1/3}} + 2/n + 1/log n ≤ 2/log n = ε_n/2), and ε_n < 1 once log n > 4. ∎
So C_n, C′_n = O((log n)²) and 1/c_{0,n} = O(log n): every polynomial or exp(C√log n) slack absorbs them.

## L6.1 Corollary F1 (uniform leakage)

Hypothesis: δ²_{U,l} ≤ η·τ²_U·log n for every l ∉ Q and U ⊆ [p] ∖ {l}, |U| ≤ 15, with a fixed η ∈ [0, η_A),
η_A = (√(2A + 1) − √(2A))²; κ_L(η, A) = ½ − η/2 − √(2Aη) > 0.
**(i) 𝔏_n(Q) ≤ n^{η/2+√(2Aη)+o(1)}.** By (J2) with |d|/t ≤ √(η log n) and σ/t ≤ 1:
J_n(δ_{U,l}, τ_U) ≤ √(2/π)z̄_n·exp((η/2) log n + √(η log n)·z̄_n), and √(η log n)·z̄_n = (√(2Aη) + o(1)) log n, with o(1)
depending only on (n, A, η). Average over l ∉ Q.
**(ii) (AL).** If (|Q| + 1)n^{−κ₁} → 0 for some κ₁ < κ_L(η, A): ϱ_n(Q) ≤ (|Q| + 1)n^{−κ_L(η,A)+o(1)}
= (|Q| + 1)n^{−κ₁}·n^{−(κ_L−κ₁)+o(1)} → 0, and b_n ≤ 1/(32 log n) → 0. So (AL) holds with the default levels.
**(iii) Conclusion.** Let κ < min{κ_L(η, A), κ_V} and κ₃ ∈ (κ, κ_V). By (ii), ϱ_n(Q) ≤ [(|Q| + 1)n^{−κ₁}]·n^{−(κ_L−κ₁)+o(1)}, which
tends to zero polynomially fast and is therefore ≤ c_{0,n} for large n. By L6.0′ with exponent κ₃, with probability
≥ 1 − 4/log n − 1/(32 log n) → 1:
  1 − π₀(𝓛(Q)) ≤ C_n·(|Q| + 1)n^{−κ_L+o(1)} + n^{−κ₃} ≤ (|Q| + 1)n^{−κ} + n^{−κ}   for large n
(C_n = O(log n), κ < κ_L, κ < κ₃). This is the display of F1.
**(iv) η = 0.** Then δ_{U,l} = 0 and J_n(0, τ_U) = E[exp(σ²Z²/(2τ²_U)); |Z| ≤ z_n] ≤ E[e^{Z²/2}; |Z| ≤ z_n] = √(2/π)z_n, so
𝔏_n(Q) ≤ √(2/π)z̄_n = O(√log n) and ϱ_n(Q) = O((|Q| + 1)√(log n/n)), which tends to 0 under the premise of (ii)
(κ₁ < ½). By (T1)(a): 1 − π₀(𝓛(Q)) = O_P((|Q| + 1)√(log n/n)) + o_P(n^{−κ}) for every κ < κ_V. ∎

## L6.2 Corollary F2 (strong signals, Q = S₀)

Hypotheses: s₀ ≥ 1; θ*_min ≥ θ_lo > 0; λ_min(R̂_{S₀}) ≥ φ₀² (fixed φ₀ ∈ (0, 1]); p/√log n → ∞; n^{−1/2}𝔏_n(S₀)² → 0;
δ²_{U,l} ≤ η′·Δ_U·log n for every l ∉ S₀ and U ⊊ S₀ with |U| ≤ 15, η′ ∈ [0, 1) fixed.
**(i) Δ_U ≥ φ₀²θ_lo² for every U ⊊ S₀.** (n − 1)Δ_U = ‖(I − P_U)X_{S₀∖U}θ*_{S₀∖U}‖² = (n − 1)·θ*ᵀ_{S₀∖U}·𝒮·θ*_{S₀∖U}, where 𝒮 is the
Schur complement of R̂_U in R̂_{S₀}; λ_min(𝒮) ≥ λ_min(R̂_{S₀}) ≥ φ₀², and ‖θ*_{S₀∖U}‖² ≥ θ_lo² (S₀ ∖ U ≠ ∅).
**(ii) Leading functional.** For U ⊊ S₀: τ_U > σ, τ²_U − σ² = Δ_U, and by (J1)
J_n(δ_{U,l}, τ_U) ≤ (τ_U/√Δ_U)·exp(δ²_{U,l}/(2Δ_U)) ≤ √(1 + σ²/(φ₀²θ_lo²))·n^{η′/2}. Hence
𝔏⁰_n ≤ C_F n^{η′/2} + 15√(2/π)z̄_n/p, C_F := √(1 + σ²/(φ₀²θ_lo²)), and
  n^{−1/2}𝔏⁰_n ≤ C_F n^{−(1−η′)/2} + o(n^{−1/2})   (p/√log n → ∞, z̄_n = O(√log n)).
**(iii) (AL) at Q = S₀.** ϱ_n(S₀) = (s₀ + 1)n^{−1/4}·(n^{−1/2}𝔏_n(S₀)²)^{1/2} → 0; default levels, b_n → 0.
**(iv) Conclusion.** By (T1)(b): o₀ = O_P(n^{−1/2}𝔏⁰_n + n^{−1}𝔏_n(S₀)²) + o_P(n^{−κ}) for every κ < κ_V, and
n^{−1}𝔏_n(S₀)² = n^{−1/2}·o(1). With (ii): **o₀ = O_P(n^{−(1−η′)/2}) + o_P(n^{−κ})**.
**(v) Exact order.** If η′ = 0 and κ_V > ½, take κ ∈ (½, κ_V): o₀ = O_P(n^{−1/2}). By (T0) (s₀ < K for large n, as p > s₀):
o₀ ≥ ½(n + 1)^{−1/2} on every data set. So o₀ is of exact order n^{−1/2}. ∎

## L6.3 Corollary F3 (bounded gains)

Hypotheses: δ²_{U,l} ≤ C₀τ²_U for every l ∉ Q, |U| ≤ 15; (|Q| + 1)n^{−1/2}e^{C₁√log n} → 0 for every fixed C₁.
By (J2): J_n(δ_{U,l}, τ_U) ≤ √(2/π)z̄_n·exp(C₀/2 + √C₀·z̄_n). For large n (depending on A only) z̄_n² ≤ (2A + 1) log n, so
𝔏_n(Q) ≤ exp(C₃√log n) with C₃ := √(C₀(2A + 1)) + 1 (the factor √(2/π)z̄_n e^{C₀/2} is ≤ e^{√log n} for large n). Hence
ϱ_n(Q) ≤ (|Q| + 1)n^{−1/2}e^{C₃√log n} → 0: (AL) holds, and ϱ_n(Q) ≤ c_{0,n} for large n (apply the hypothesis with
C₁ = C₃ + 1: (|Q| + 1)n^{−1/2}e^{(C₃+1)√log n} → 0 and e^{−√log n} log n → 0). By L6.0′, for κ < κ_V, with probability
≥ 1 − 4/log n − 1/(32 log n) → 1:
  1 − π₀(𝓛(Q)) ≤ C_n(|Q| + 1)n^{−1/2}e^{C₃√log n} + n^{−κ} ≤ (|Q| + 1)n^{−1/2}e^{C₂√log n} + n^{−κ},   C₂ := C₃ + 1 = √(C₀(2A + 1)) + 2,
for large n (C_n = 43s₀′c_L log n ≤ e^{√log n} eventually). C₂ depends only on (C₀, A). ∎

## L6.4 Corollary F4 (isolated leaking columns)

The arithmetic is in `lemmas/L3_LEAK.md` L3.5: with h_l = min(z_n, √(4 log log n)) on I_n and h_l = z_n elsewhere, h is a
level vector, b_n(h) → 0, and ϱ_n(Q; h) ≤ ϱ^{−I}_n(Q) + (|Q| + 1)n^{−(1+2A̲−c)/2+o(1)}. If ϱ^{−I}_n(Q) → 0 and (|Q| + 1)n^{−κ₁} → 0 for
some κ₁ < (1 + 2A̲ − c)/2, then ϱ_n(Q; h) → 0: (AL) holds with this h, and (T1)(a)–(d) apply with it. ∎
(The sentence in F4 comparing with the failure threshold refers to the component diagnostic (C2)(i),
`lemmas/L7_NEC.md`.)
