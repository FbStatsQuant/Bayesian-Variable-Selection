# L5 — Lemma ASM (C1) and Theorem START-F (T1)(a)–(d)

Status: **PROVED (by this seat, unchecked)**.
Statement proved: `STATEMENT.md` §5.1 (C1) and §5.3 (T1). Uses: `lemmas/L1_AGG_FLOOR.md` ((AGG-a), (AGG-b), (T0));
`lemmas/L2_TK.md` (𝓔^blk); `lemmas/L3_LEAK.md` (Proposition L3.4, (B1), n₂, c_L); `lemmas/L4_VIS.md` (𝓧, Propositions
L4.1, L4.2, n₃, n₄). Notation: s₀′ := max(s₀, 1). "X_n = O_P(a_n) + o_P(n^{−κ})" means X_n ≤ A_n + B_n with A_n = O_P(a_n),
n^κB_n → 0 in probability.

## L5.0 Two elementary inequalities

**(e1)** c_Q + 1 = |Q| + 15s₀ + 1 ≤ 16s₀′(|Q| + 1), and c_Q ≤ 16s₀′(|Q| + 1).
**(e2)** Let 0 ≤ U_Q ≤ ¼, (c_Q + 1)U_Q ≤ ¼ and s₀Ξ(Q) ≤ ½. Then
  ∏_{b∈𝔹*}(1 + Ξ_b(Q))·(1 − U_Q)^{−(c_Q+1)} − 1 ≤ 2s₀Ξ(Q) + (8/3)(c_Q + 1)U_Q.
*Proof.* log(1 + ξ) ≤ ξ and −log(1 − u) ≤ u/(1 − u) ≤ (4/3)u give ∏(1 + Ξ_b)(1 − U_Q)^{−(c_Q+1)} ≤ exp(x) with
x := s₀Ξ(Q) + (4/3)(c_Q + 1)U_Q ≤ ½ + ⅓ < 1 (|𝔹*| ≤ s₀, Ξ_b ≤ Ξ), and e^x − 1 ≤ (e − 1)x ≤ 2x on [0, 1]. ∎
**(e3)** For c > 0 and 0 ≤ u ≤ ¼: (1 − u)^{−c} − 1 − cu ≤ ½c(c + 1)(4/3)^{c+2}u² (Taylor with Lagrange remainder). ∎

## L5.1 Lemma ASM (C1)

Setting F, deterministic Q ⊇ S₀ with |Q| ≤ K, s₀ fixed, p > s₀ eventually, a level vector h with b_n(h) → 0. Assume [TK],
[LEAK(Q)] with a_n := (|Q| + 1)n^{−1/2}𝔏^b_n(Q; h) → 0, and [VIS(κ; Q)] for some κ > 0.

(a) By [LEAK(Q)], U_Q = O_P(n^{−1/2}𝔏^b_n(Q; h)), so by (e1) (c_Q + 1)U_Q = O_P(a_n) → 0 in probability; by [VIS(κ; Q)],
P(Ξ(Q) > n^{−κ}) → 0. On 𝒢 := {(c_Q + 1)U_Q ≤ ¼, U_Q ≤ ¼, Ξ(Q) ≤ n^{−κ}} (P(𝒢) → 1) and for n so large that s₀n^{−κ} ≤ ½,
(AGG-a) and (e2) give
  1 − π₀(𝓛(Q)) ≤ 2s₀n^{−κ} + (8/3)(c_Q + 1)U_Q.
The first term is O(n^{−κ}); the second is O_P(a_n). Hence 1 − π₀(𝓛(Q)) = O_P(a_n) + O_P(n^{−κ}), and O_P(n^{−κ}) is o_P(n^{−κ′})
for every κ′ < κ.
(b) Q = S₀; s₀ < K for all large n (p > s₀, n ≥ 2s₀ + 2). On 𝒢, (AGG-b), (e3) with c = s₀ + 1, and e^x − 1 ≤ 2x:
  o₀ ≤ T₁ + ½(s₀ + 1)(s₀ + 2)(4/3)^{s₀+3}U² + 2s₀n^{−κ}(4/3)^{16s₀+1}.
By [LEAK(S₀)]: T₁ = O_P(n^{−1/2}𝔏^{b,0}_n(h)) (its premise n^{−1/2}𝔏^{b,0}_n(h) → 0 holds because 𝔏^{b,0}_n(h) ≤ 𝔏^b_n(S₀; h),
(B1)(ii)), and U² = O_P(n^{−1}𝔏^b_n(S₀; h)²). So o₀ = O_P(n^{−1/2}𝔏^{b,0}_n(h) + n^{−1}𝔏^b_n(S₀; h)²) + O_P(n^{−κ}).
(c) Q = S₀, κ > ½, n^{−1/2}𝔏^b_n(S₀; h)² → 0. By (AGG-b) and (T0) (s₀ < K): T₁ ≥ ½(n + 1)^{−1/2} > 0 and, on 𝒢,
  0 ≤ o₀/T₁ − 1 ≤ 2√(n + 1)·[½(s₀ + 1)(s₀ + 2)(4/3)^{s₀+3}U² + 2s₀n^{−κ}(4/3)^{16s₀+1}].
√n·U² = O_P(n^{−1/2}𝔏^b_n(S₀; h)²) → 0 in probability and √n·n^{−κ} → 0. Hence o₀/T₁ → 1 in probability. ∎

## L5.2 Theorem START-F, explicit uniform form: (T1)(d)

**Proposition L5.2.** Fix (A, M, σ², g_*, s₀) and either c_V > 1 + 2A (κ_V := (c_V − 1 − 2A)/2) or (c_m, ε₀) (κ_V := c_m/2). Let
ε ∈ (0, 1) and κ ∈ (0, κ_V). Put κ′ := (κ + κ_V)/2,
  λ := 4c_L/ε  (c_L = 2^{15}e^{2κ_E+1}),   c₀ := 1/(64s₀′λ),   C := 43s₀′λ,
  C′ := λ(s₀ + 1) + ½(s₀ + 1)(s₀ + 2)(4/3)^{s₀+3}λ².
There is n₀, depending only on (ε, κ) and the fixed constants, such that for every n ≥ n₀ and every (X, θ*, Q, h) — a
fixed design with p ≤ n^A retained columns, |supp θ*| = s₀ < p, S₀ ⊆ Q, |Q| ≤ K, h a level vector for Q — satisfying at n
‖μ‖² ≤ Mn, (GF-16), the visibility condition ((V-c) with c_V, or (V-m) with (c_m, ε₀)) and **ϱ_n(Q; h) ≤ c₀**:
  (i) P(1 − π₀(𝓛(Q)) > C·ϱ_n(Q; h) + n^{−κ}) ≤ ε + b_n(h);
  (ii) if Q = S₀: P(o₀ > C′·[n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)²] + n^{−κ}) ≤ ε + b_n(h).

*Proof.* Let n₀ ≥ max(n₂, n₃ or n₄ (for the exponent κ′), 2s₀ + 2) be such that for n ≥ n₀:
2e^{−n^{1/3}} + 2/n + 1/log n ≤ ε/2, 2s₀n^{−κ′}(4/3)^{16s₀+1} ≤ n^{−κ}, and s₀n^{−κ′} ≤ ½. Fix n ≥ n₀ and an admissible
(X, θ*, Q, h). By (B1), (GF-16) holds on the block family, the visibility condition holds for the block instances, and
  a^b := (|Q| + 1)n^{−1/2}𝔏^b_n(Q; h) ≤ ϱ_n(Q; h) ≤ c₀ ≤ 1.
*Events.* 𝓔^blk (L2), 𝓧 (L4; if s₀ = 0 put 𝓧 := the sure event), and
  𝓜 := {U_Q ≤ λn^{−1/2}𝔏^b_n(Q; h)};  for Q = S₀ also 𝓜₀ := {T₁ ≤ λ(s₀ + 1)n^{−1/2}𝔏^{b,0}_n(h)}.
Probabilities: P((𝓔^blk)ᶜ) ≤ 2e^{−n^{1/3}} + 2/n (Lemma L2.1); P(𝓧ᶜ) ≤ 1/log n (L4.0); P(𝓩_hᶜ) ≤ b_n(h) (L3.2); and the Markov step
in the proof of Proposition L3.4 gives P(𝓜ᶜ ∩ 𝓔^blk ∩ 𝓩_h) ≤ c_L/λ = ε/4 (premise a^b ≤ 1) and
P(𝓜₀ᶜ ∩ 𝓔^blk ∩ 𝓩_h) ≤ e^{2κ_E+1}/λ ≤ ε/4 (premise n^{−1/2}𝔏^{b,0}_n(h) ≤ 1: true since 𝔏^{b,0}_n(h) ≤ 𝔏^b_n(S₀; h) ≤ √n; and s₀ < K for
n ≥ 2s₀ + 2). So the event
  𝒢 := 𝓔^blk ∩ 𝓧 ∩ 𝓩_h ∩ 𝓜 (∩ 𝓜₀ if Q = S₀)   has   **P(𝒢ᶜ) ≤ ε + b_n(h).**
*On 𝒢.* By (e1): (c_Q + 1)U_Q ≤ 16s₀′(|Q| + 1)λn^{−1/2}𝔏^b_n(Q; h) = 16s₀′λa^b ≤ 16s₀′λc₀ = ¼; so U_Q ≤ ¼ and c_QU_Q ≤ 1.
By Proposition L4.1 (under (V-m)) or L4.2 (under (V-c); c_QU_Q ≤ 1), with exponent κ′: Ξ(Q) ≤ n^{−κ′} (Ξ(Q) = 0 if s₀ = 0).
(i) By (AGG-a) and (e2): 1 − π₀(𝓛(Q)) ≤ 2s₀n^{−κ′} + (8/3)·16s₀′λa^b ≤ n^{−κ} + Cϱ_n(Q; h).
(ii) Q = S₀, s₀ < K. By (AGG-b), (e3) (c = s₀ + 1, U ≤ ¼) and e^x − 1 ≤ 2x (x = s₀Ξ ≤ ½):
  o₀ ≤ T₁ + ½(s₀ + 1)(s₀ + 2)(4/3)^{s₀+3}U² + 2s₀n^{−κ′}(4/3)^{16s₀+1}
    ≤ λ(s₀ + 1)n^{−1/2}𝔏^{b,0}_n(h) + ½(s₀ + 1)(s₀ + 2)(4/3)^{s₀+3}λ²n^{−1}𝔏^b_n(S₀; h)² + n^{−κ}
    ≤ C′[n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)²] + n^{−κ}
by (B1): 𝔏^{b,0}_n(h) ≤ 𝔏⁰_n(h), 𝔏^b_n(S₀; h) ≤ 𝔏_n(S₀; h). ∎

*Remarks.* (1) The constants C, C′, c₀ depend on ε only through λ = 4c_L/ε, and on (g_*, M, σ²) through κ_E. (2) No
relation between b_n(h) and ε is assumed at a fixed n; if b_n(h) is not small the bound is vacuous, as it should be.

## L5.3 Theorem START-F (T1)(a)–(c)

Setting F, (E), (GF-16), visibility with exponent κ_V, (AL) for a deterministic Q ⊇ S₀, |Q| ≤ K, with level vector h:
b_n(h) → 0 and ϱ_n(Q; h) → 0. Fix κ ∈ (0, κ_V) and put κ″ := (κ + κ_V)/2.
**(a)** Let X_n := 1 − π₀(𝓛(Q)) and ε ∈ (0, 1). Apply L5.2(i) with (ε, κ″): for all n large enough that n ≥ n₀(ε, κ″) and
ϱ_n(Q; h) ≤ c₀(ε): P(X_n > C(ε)ϱ_n(Q; h) + n^{−κ″}) ≤ ε + b_n(h). Put B_n := n^{−κ″} (n^κB_n → 0) and A_n := (X_n − B_n)₊; then
limsup_n P(A_n > C(ε)ϱ_n(Q; h)) ≤ ε for every ε, i.e. A_n = O_P(ϱ_n(Q; h)), and X_n ≤ A_n + B_n:
**1 − π₀(𝓛(Q)) = O_P(ϱ_n(Q; h)) + o_P(n^{−κ}).**
**(b)** Q = S₀: the same argument with L5.2(ii) gives **o₀ = O_P(n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)²) + o_P(n^{−κ})**. The rate tends
to zero: n^{−1}𝔏_n(S₀; h)² ≤ ϱ_n(S₀; h)² → 0; if s₀ ≥ 1, 𝔏⁰_n(h) ≤ 𝔏_n(S₀; h) + 15√(2/π)z_n/p (the sets U ⊊ S₀, |U| ≤ 15, are
among those of 𝔏_n(S₀; h)) and n^{−1/2}z_n/p → 0; if s₀ = 0, 𝔏⁰_n(h) = √(2/π)p⁻¹Σ_l h_l ≤ 𝔏_n(∅; h) (the term U = ∅ of each
maximum is J_{h_l}(0, σ) = √(2/π)h_l). Hence o₀ → 0 and π₀(S₀) = 1/(1 + o₀) → 1 in probability.
**(c)** Q = S₀, κ_V > ½, n^{−1/2}𝔏_n(S₀; h)² → 0. Fix κ′ ∈ (½, κ_V), ε ∈ (0, 1), and the event 𝒢 of L5.2 built with (ε, κ′)
(n large, ϱ_n(S₀; h) ≤ c₀(ε)); P(𝒢ᶜ) ≤ ε + b_n(h). By (T0), T₁ ≥ ½(n + 1)^{−1/2} > 0 (s₀ < K); by (AGG-b) and the bounds on 𝒢,
  0 ≤ o₀/T₁ − 1 ≤ 2√(n + 1)·[½(s₀ + 1)(s₀ + 2)(4/3)^{s₀+3}λ²n^{−1}𝔏_n(S₀; h)² + 2s₀n^{−κ′}(4/3)^{16s₀+1}] =: D_n(ε),
and D_n(ε) → 0 as n → ∞ for fixed ε (n^{−1/2}𝔏_n(S₀; h)² → 0; κ′ > ½). So for every η > 0:
limsup_n P(|o₀/T₁ − 1| > η) ≤ ε; ε is arbitrary. **o₀/T₁ → 1 in probability.**
**(d)** is Proposition L5.2 (with the constant max(C, C′) in both displays). ∎

## L5.4 What is used, in one place

| input | where proved | used for |
|---|---|---|
| (AGG-a), (AGG-b), (AGG-d), (T0) | L1 (deterministic) | odds ≤ table functionals; T₁ ≥ ½(n + 1)^{−1/2} |
| 𝓔^blk, (TK-a)–(TK-f) | L2, from (E), (GF-16) | every table ratio |
| Lemma J, 𝓩_h, L3.3, L3.4, (B1) | L3 | U_Q, T₁ = O_P(n^{−1/2}·leakage functional); small gains from (AL) |
| 𝓧, L4.1 / L4.2 | L4, from (V-m) / (V-c) | Ξ(Q) ≤ n^{−κ′} |

No registry claim is consumed. Probability bounds add up to ε + b_n(h): Gaussian events (2e^{−n^{1/3}} + 2/n + 1/log n),
the level event (b_n(h)), two Markov bounds (ε/4 each).
