# P1 — the sharp leading functional: Lemma LEAK-0, (T1⁺), F2⁺, (T3⁺)(a), IF-START⁺

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Citations: BASE `path:lines` is a file of the base ticket; a short citation `:a-b` continues the file cited last before it.
Statement proved: `STATEMENT.md` §2 (D1) (the facts stated there); §3.1 Lemma LEAK-0; §3.2 (T1⁺), F2⁺, (T3⁺)(a),
IF-START⁺. BASE := `Theory_work/Wave3/W3-START/`. Only the steps that change are proved here; every other step is a
step of a BASE proof file and is cited by line. Notation of BASE `STATEMENT.md` §1–§2 and of the cited files:
𝓔^blk, κ_E, (TK-a)–(TK-f) (BASE `lemmas/L2_TK.md:32-95`); 𝓩_h, z̄_n, g⁰_n, n₂, c_L := 2^{15}e^{2κ_E+1} (BASE
`lemmas/L3_LEAK.md:27-30`, `:44-48`, `:71`); 𝓧, κ′, λ, c₀, C, n₀ (BASE `lemmas/L5_ASM_STARTF.md:39-50`).
**Abbreviation:** e_κ := e^{2κ_E+1}.

## P1.1 Elementary facts about 𝔏^♯_n(h) (statement (D1))

Let s₀ ≥ 1, p > s₀, and h a level vector for S₀. For l ∉ S₀ put 𝒰 := {U ⊊ S₀ : |U| ≤ 15}; ∅ ∈ 𝒰 because s₀ ≥ 1, so the
maximum in (D1) is over a non-empty finite family.
* **(a) 𝔏^♯_n(h) ≥ (p − s₀)/(4p) ≥ 1/(4p).** Each J_{h_l}(δ_{U,l}, τ_U) is ≥ ¼·exp(δ²_{U,l}/(2τ²_U)) ≥ ¼ by (J0) (BASE
  BASE `lemmas/L3_LEAK.md:12-14`; h_l ≥ 1, τ_U ≥ σ), and there are p − s₀ ≥ 1 null columns. Hence **1/p ≤ 4𝔏^♯_n(h)**.
* **(b) 𝔏^♯_n(h) ≤ 𝔏_n(S₀; h).** For l ∉ S₀ every U ∈ 𝒰 satisfies U ⊆ [p] ∖ {l} and |U| ≤ 15, so it is one of the sets
  maximised over in 𝔏_n(S₀; h) (BASE `STATEMENT.md:110`).
* **(c) 𝔏^♯_n(h) = 𝔏⁰_n(h) − 15√(2/π)z_n/p** (compare (D1) with BASE `STATEMENT.md:112-114`); in particular
  𝔏^♯_n(h) ≤ 𝔏⁰_n(h).
For s₀ = 0, 𝔏^♯_n(h) = 𝔏⁰_n(h) by definition. ∎

## P1.2 The two kinds of null column

Let s₀ ≥ 1 and let {C_b} be a partition of [p] with blocks of size ≤ 16 that is a function of X (the coded
partition is one; BASE `STATEMENT.md:62-63`). Put
  **𝒩_exc := {l ∉ S₀ : U*_{b(l)} = S₀}** (the block of l contains every truth),  **𝒩_prop := {l ∉ S₀ : U*_{b(l)} ⊊ S₀}**.
These sets partition the nulls, and in Setting F they are deterministic.
* **(a) |𝒩_exc| ≤ max(0, 16 − s₀) ≤ 15; in particular 𝒩_exc = ∅ if s₀ ≥ 16.** Fix j ∈ S₀ (s₀ ≥ 1) and let C be the block
  containing j; it is unique because the blocks are disjoint. If l ∈ 𝒩_exc then j ∈ S₀ ⊆ C_{b(l)}, so C_{b(l)} = C. Hence, if
  𝒩_exc ≠ ∅, then S₀ ∪ 𝒩_exc ⊆ C: a disjoint union inside a set of at most 16 elements, so s₀ + |𝒩_exc| ≤ 16.
* **(b)** For l ∈ 𝒩_prop: U*_{b(l)} ⊊ S₀ and |U*_{b(l)}| ≤ 15 (U*_{b(l)} ⊆ C_{b(l)} ∖ {l}); so U*_{b(l)} ∈ 𝒰.
* **(c)** For l ∈ 𝒩_exc: (I − P_{S₀})μ = 0 because μ = X_{S₀}θ*_{S₀}; so δ_{S₀,l} = 0, Λ_{S₀} = 0 and τ_{S₀} = σ. ∎

## P1.3 Lemma LEAK-0

**Hypotheses.** Setting F, (E), (GF-16), s₀ ≥ 1, s₀ < K, h a level vector for S₀, n ≥ n₂, n^{−1/2}𝔏^♯_n(h) ≤ 1, and
15e_κ ≤ λ ≤ 15e_κ·2^{21}·p·log n. **Claim.** P(T₁ > 5λ(s₀ + 1)n^{−1/2}𝔏^♯_n(h)) ≤ P((𝓔^blk)ᶜ) + b_n(h) + 451e_κ/λ.

*Proof.* Write, for l ∉ S₀: b := b(l), U_l := U*_{b(l)}, δ_l := δ_{U_l,l}, τ_l := τ_{U_l}, Z_l := Z_{U_l,l},
ρ_l := r_b(U_l ∪ {l})/r_b(U_l).
*Step 0 (the sum).* Since s₀ < K, T₁ = [(s₀ + 1)/(2p − 1 − s₀)]·Σ_{l∉S₀}ρ_l ≤ ((s₀ + 1)/p)·Σ_{l∉S₀}ρ_l, because s₀ ≤ p − 1
(BASE `STATEMENT.md:89`; BASE `lemmas/L3_LEAK.md:86`).
*Step 1 (cut-off for the exceptional columns).* Put **H := √(2 log(λ/(15e_κ)))**; H ≥ 0 is real because λ ≥ 15e_κ, and
e^{H²/2} = λ/(15e_κ). Since z_n² = 2 log(2^{21}p) + 2 log log n, e^{z_n²/2} = 2^{21}·p·log n, so the upper bound on λ is
exactly **H ≤ z_n**. Let **𝓗 := {|Z_l| ≤ H for every l ∈ 𝒩_exc}**. Each Z_l is N(0, 1): u_{U_l,l} is a deterministic
unit vector, (I − P_{U_l})x_l ≠ 0 by (GF-16) (BASE `lemmas/L3_LEAK.md:28`). By P1.2(a) and P(|Z| > H) ≤ 2e^{−H²/2}:
  P(𝓗ᶜ) ≤ 15·2·e^{−H²/2} = 30·15e_κ/λ = **450e_κ/λ**.
*Step 2 (small gains).* For l ∈ 𝒩_prop, by P1.2(b), J_{h_l}(δ_l, τ_l) ≤ max{J_{h_l}(δ_{U,l}, τ_U) : U ∈ 𝒰} ≤ p·𝔏^♯_n(h) ≤ p√n
(each of the other summands of p𝔏^♯_n(h) is non-negative). By "small gains from the averaged condition" (BASE
`lemmas/L3_LEAK.md:61-62`): δ_l² ≤ g⁰_n·τ_l². For l ∈ 𝒩_exc, δ_l = 0 ≤ g⁰_nτ_l² (P1.2(c)).
*Step 3 (step bound).* On 𝓔^blk ∩ 𝓩_h ∩ 𝓗: for l ∈ 𝒩_prop, |Z_l| ≤ h_l ≤ z_n (definition of 𝓩_h with T = U_l ⊆ C_b ∖ {l});
for l ∈ 𝒩_exc, |Z_l| ≤ H ≤ z_n. So Lemma L3.3 (BASE `lemmas/L3_LEAK.md:51-53`; n ≥ n₂, T = U_l) applies to every null:
  ρ_l ≤ e_κ·(n + 1)^{−1/2}·exp((δ_l + σZ_l)²/(2τ_l²)).
For l ∈ 𝒩_exc the exponent is Z_l²/2 ≤ H²/2 (P1.2(c)), so ρ_l ≤ e_κ(n + 1)^{−1/2}e^{H²/2} = (λ/15)(n + 1)^{−1/2}. For
l ∈ 𝒩_prop, 1{|Z_l| ≤ h_l} = 1 on 𝓩_h. With
  **V := p⁻¹·Σ_{l∈𝒩_prop} exp((δ_l + σZ_l)²/(2τ_l²))·1{|Z_l| ≤ h_l}**   (V := 0 if 𝒩_prop = ∅),
Step 0 and |𝒩_exc| ≤ 15 give, on 𝓔^blk ∩ 𝓩_h ∩ 𝓗:
  T₁ ≤ (s₀ + 1)(n + 1)^{−1/2}·[e_κV + |𝒩_exc|·(λ/15)/p] ≤ (s₀ + 1)·n^{−1/2}·[e_κV + λ/p].                              (1.1)
*Step 4 (Markov).* E V = p⁻¹Σ_{l∈𝒩_prop}J_{h_l}(δ_l, τ_l) ≤ 𝔏^♯_n(h) (the definition of J_h, BASE `STATEMENT.md:106`;
P1.2(b); Z_l ~ N(0, 1)), and 𝔏^♯_n(h) > 0 (P1.1(a)). So P(e_κV > λ𝔏^♯_n(h)) ≤ e_κ/λ.
*Step 5.* On 𝓔^blk ∩ 𝓩_h ∩ 𝓗 ∩ {e_κV ≤ λ𝔏^♯_n(h)}, (1.1) and 1/p ≤ 4𝔏^♯_n(h) (P1.1(a)) give
T₁ ≤ (s₀ + 1)n^{−1/2}λ[𝔏^♯_n(h) + 1/p] ≤ 5λ(s₀ + 1)n^{−1/2}𝔏^♯_n(h). The complement of this event has probability at most
P((𝓔^blk)ᶜ) + b_n(h) + 450e_κ/λ + e_κ/λ (P(𝓩_hᶜ) ≤ b_n(h): BASE `lemmas/L3_LEAK.md:30`). ∎

**For later use (event form).** Under the hypotheses of the lemma,
  **P({T₁ > 5λ(s₀ + 1)n^{−1/2}𝔏^♯_n(h)} ∩ 𝓔^blk ∩ 𝓩_h) ≤ 451e_κ/λ.**                                                     (1.2)
**Consequence.** Along a sequence with b_n(h) → 0 and n^{−1/2}𝔏^♯_n(h) ≤ 1 for all large n: given ε ∈ (0, 1) take
λ := 2·451e_κ/ε; for n large, n ≥ n₂, λ ≤ 15e_κ2^{21}p log n (log n → ∞, p ≥ 1), P((𝓔^blk)ᶜ) ≤ 2e^{−n^{1/3}} + 2/n → 0 (BASE
`lemmas/L2_TK.md:32`) and b_n(h) → 0; so limsup P(T₁ > 5λ(s₀ + 1)n^{−1/2}𝔏^♯_n(h)) ≤ ε/2: **T₁ = O_P(n^{−1/2}𝔏^♯_n(h))**. Nothing
depends on (X, θ*, h) beyond the hypotheses.

*Remarks.* (1) No independence between the Z_l is used. (2) exp(Z²/2) has no first moment, which is why version
1.3.4 truncated at z_n and paid √(2/π)z_n per column. For at most 15 columns a union bound at a fixed level H
replaces the truncated mean; the price is that the constant 5λ grows like 1/ε. (3) The split is a function of X
only, so no selection by the response occurs. (4) If s₀ = 0 every null is exceptional (U_l = ∅ = S₀) and there are p
of them; the argument does not apply, and (D1) keeps 𝔏⁰_n(h).

## P1.4 Theorem START-F, uniform form: (T1⁺)(d)

**Proposition P1.4.** Fix the constants, ε ∈ (0, 1), κ ∈ (0, κ_V), and κ′, λ := 4c_L/ε, c₀ := 1/(64s₀′λ), C := 43s₀′λ and n₀
exactly as in BASE Proposition L5.2 (BASE `lemmas/L5_ASM_STARTF.md:39-50`; s₀′ := max(s₀, 1)). Put
  **C^♯ := 5λ(s₀ + 1) + ½(s₀ + 1)(s₀ + 2)(4/3)^{s₀+3}λ²**.
Then for every n ≥ n₀ and every admissible (X, θ*, Q, h) of L5.2 (in particular ϱ_n(Q; h) ≤ c₀):
  (i) P(1 − π₀(𝓛(Q)) > C·ϱ_n(Q; h) + n^{−κ}) ≤ ε + b_n(h);
  (ii) if Q = S₀: **P(o₀ > C^♯·[n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)²] + n^{−κ}) ≤ ε + b_n(h).**

*Proof.* (i) is BASE L5.2(i), unchanged. (ii) with s₀ = 0 is BASE L5.2(ii) (𝔏^♯_n(h) = 𝔏⁰_n(h), and C^♯ ≥ C′). Let s₀ ≥ 1,
Q = S₀, n ≥ n₀ and (X, θ*, S₀, h) admissible.
*Hypotheses of Lemma LEAK-0.* s₀ < K (n ≥ 2s₀ + 2 and p > s₀); n ≥ n₂; by P1.1(b),
n^{−1/2}𝔏^♯_n(h) ≤ n^{−1/2}𝔏_n(S₀; h) = ϱ_n(S₀; h)/(s₀ + 1) ≤ c₀ ≤ 1; λ = 2^{17}e_κ/ε ≥ 15e_κ; and λ ≤ 15e_κ2^{21}p log n because n₀
was chosen with 2e^{−n^{1/3}} + 2/n + 1/log n ≤ ε/2 (BASE `lemmas/L5_ASM_STARTF.md:50`), so log n ≥ 2/ε and
2^{17}/ε ≤ 2^{16} log n ≤ 15·2^{21}·p·log n.
*Events.* 𝓔^blk, 𝓧, 𝓩_h and 𝓜 := {U ≤ λn^{−1/2}𝔏^b_n(S₀; h)} as in the BASE proof (`:53-56`), and, in place of 𝓜₀,
  **𝓜^♯ := {T₁ ≤ 5λ(s₀ + 1)n^{−1/2}𝔏^♯_n(h)}**.
The BASE bounds are unchanged: P((𝓔^blk)ᶜ) + P(𝓧ᶜ) ≤ ε/2, P(𝓩_hᶜ) ≤ b_n(h), P(𝓜ᶜ ∩ 𝓔^blk ∩ 𝓩_h) ≤ ε/4 (`:55-56`). By (1.2):
P((𝓜^♯)ᶜ ∩ 𝓔^blk ∩ 𝓩_h) ≤ 451e_κ/λ = 451ε/2^{17} ≤ ε/4. So 𝒢^♯ := 𝓔^blk ∩ 𝓧 ∩ 𝓩_h ∩ 𝓜 ∩ 𝓜^♯ has **P((𝒢^♯)ᶜ) ≤ ε + b_n(h)**.
*On 𝒢^♯.* As in the BASE proof (`:60-61`, which uses 𝓔^blk, 𝓧, 𝓩_h and 𝓜 only): U ≤ ¼ and Ξ ≤ n^{−κ′}. The deterministic
inequality of `:63-64` — (AGG-b), (e3) with c = s₀ + 1, and e^x − 1 ≤ 2x — gives
  o₀ ≤ T₁ + ½(s₀ + 1)(s₀ + 2)(4/3)^{s₀+3}U² + 2s₀n^{−κ′}(4/3)^{16s₀+1}.
Now T₁ ≤ 5λ(s₀ + 1)n^{−1/2}𝔏^♯_n(h) (𝓜^♯); U ≤ λn^{−1/2}𝔏^b_n(S₀; h) ≤ λn^{−1/2}𝔏_n(S₀; h) (𝓜 and (B1)(i), BASE
`lemmas/L3_LEAK.md:34`); and 2s₀n^{−κ′}(4/3)^{16s₀+1} ≤ n^{−κ} (choice of n₀). Hence
o₀ ≤ C^♯[n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)²] + n^{−κ} on 𝒢^♯. ∎

**Dependence of n₀ on ε, and the high-probability form.** The requirements on n₀ are those of BASE L5.2 (the range of
λ follows from one of them), so BASE Lemma L6.0 (BASE `lemmas/L6_COROLLARIES.md:11-17`) holds for Proposition P1.4 as it
stands. BASE Corollary L6.0′ (`:19-26`) therefore holds with C′_n replaced by
C^♯_n := 5λ_n(s₀ + 1) + ½(s₀ + 1)(s₀ + 2)(4/3)^{s₀+3}λ_n² and 𝔏⁰_n(h) replaced by 𝔏^♯_n(h) in its second display: there
ε_n = 4/log n and λ_n = c_L log n, and 15e_κ ≤ 2^{15}e_κ log n ≤ 15e_κ2^{21}p log n for every n ≥ 3. Its first display is
unchanged.

## P1.5 Theorem START-F (T1⁺)(a)–(d)

Setting F, (E), (GF-16), visibility with exponent κ_V, (AL) for Q with level vector h; κ ∈ (0, κ_V).
**(a)** is BASE L5.3(a) (BASE `lemmas/L5_ASM_STARTF.md:76-79`), unchanged.
**(b)** Q = S₀. The argument of BASE L5.3(a)–(b) (`:76-80`) with Proposition P1.4(ii) in place of L5.2(ii): with
κ″ := (κ + κ_V)/2 and X_n := o₀, for every ε ∈ (0, 1) and all n ≥ n₀(ε, κ″) with ϱ_n(S₀; h) ≤ c₀(ε),
P(o₀ > C^♯(ε)[n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)²] + n^{−κ″}) ≤ ε + b_n(h). With B_n := n^{−κ″} and A_n := (o₀ − B_n)₊:
A_n = O_P(n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)²), n^κB_n → 0 and o₀ ≤ A_n + B_n. So
  **o₀ = O_P(n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)²) + o_P(n^{−κ}).**
The rate tends to zero: if s₀ ≥ 1, n^{−1/2}𝔏^♯_n(h) ≤ n^{−1/2}𝔏_n(S₀; h) ≤ ϱ_n(S₀; h) → 0 (P1.1(b)); if s₀ = 0 as in BASE
(`:81-83`); and n^{−1}𝔏_n(S₀; h)² ≤ ϱ_n(S₀; h)² → 0. Hence o₀ → 0 and π₀(S₀) = 1/(1 + o₀) → 1 in probability.
**(c)** is BASE L5.3(c) (`:84-88`), unchanged: it uses the event 𝒢 of BASE L5.2 only through the bounds on U and Ξ
and the deterministic lower bound T₁ ≥ ½(n + 1)^{−1/2}.
**(d)** is Proposition P1.4, with the constant max(C, C^♯) in both displays. ∎

## P1.6 Corollary F2⁺

Hypotheses: Setting F, (E), (GF-16), visibility with exponent κ_V, default levels; s₀ ≥ 1; θ*_min ≥ θ_lo > 0;
λ_min(R̂_{S₀}) ≥ φ₀²; n^{−1/2}𝔏_n(S₀)² → 0; δ²_{U,l} ≤ η′Δ_U log n for l ∉ S₀, U ⊊ S₀, |U| ≤ 15; η′ ∈ [0, 1) fixed.
(i) Δ_U ≥ φ₀²θ_lo² for every U ⊊ S₀: BASE `lemmas/L6_COROLLARIES.md:50-51`, unchanged.
(ii) For l ∉ S₀ and U ⊊ S₀ with |U| ≤ 15: J_n(δ_{U,l}, τ_U) ≤ C_Fn^{η′/2}, C_F := √(1 + σ²/(φ₀²θ_lo²)), by (J1) (BASE
`:52-53`). Every term of 𝔏^♯_n is of this kind and there are p − s₀ ≤ p of them, so **𝔏^♯_n ≤ C_Fn^{η′/2}** and
n^{−1/2}𝔏^♯_n ≤ C_Fn^{−(1−η′)/2}. (The BASE proof needed p/√log n → ∞ at exactly one place, to make the term 15√(2/π)z̄_n/p
of 𝔏⁰_n negligible (`:54-55`); 𝔏^♯_n has no such term.)
(iii) (AL) at Q = S₀ with default levels: BASE `:56`, unchanged.
(iv) By (T1⁺)(b): o₀ = O_P(n^{−1/2}𝔏^♯_n + n^{−1}𝔏_n(S₀)²) + o_P(n^{−κ}) for every κ ∈ (0, κ_V); n^{−1}𝔏_n(S₀)² = n^{−1/2}·o(1) is
O(n^{−(1−η′)/2}). With (ii): **o₀ = O_P(n^{−(1−η′)/2}) + o_P(n^{−κ})**.
(v) If η′ = 0 and κ_V > ½: take κ ∈ (½, κ_V): o₀ = O_P(n^{−1/2}); and o₀ ≥ ½(n + 1)^{−1/2} on every data set by (T0), since
s₀ < K for large n (p > s₀ by (E)). So o₀ is of exact order n^{−1/2}. ∎
*Bounded p.* No step of (T1⁺) or of this proof uses p → ∞: Proposition P1.4 holds for every design with
1 ≤ s₀ < p ≤ n^A, and (E) asks only p > s₀ for all large n.

## P1.7 Transfer (T3⁺)(a)

BASE Proposition L8.2 (BASE `lemmas/L8_TRANSFER.md:37-50`) holds with (ii) in the form: *if Q = S₀ on 𝒳 and
n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)² ≤ r̄ for every x ∈ 𝒳, then P(o₀ > C^♯·r̄ + n^{−κ}) ≤ ε + b̄ + P(X^r ∉ 𝒳)*. The proof is the BASE
proof (`:45-50`) with Proposition P1.4(ii) applied to each fixed design x ∈ 𝒳 in place of L5.2(ii); the constants of
P1.4 depend only on (ε, κ) and the fixed constants, as the BASE argument requires (`:52-53`). (On designs with
s₀ = 0, 𝔏^♯_n(h) = 𝔏⁰_n(h).) Theorem (T3⁺)(a) then follows as in BASE L8.3 (`:57-66`), word for word. ∎

## P1.8 IF-START⁺

(a) *Fixed design.* Under (T1⁺) with (AL) at Q = S₀ and level vector h, 0 < κ < κ_V,
r_n := n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)² + n^{−κ} → 0 (P1.5(b)). By (T1⁺)(b) with an exponent κ₁ ∈ (κ, κ_V):
o₀ = O_P(n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)²) + o_P(n^{−κ₁}) = O_P(r_n); and 0 ≤ 1_𝒜o₀ ≤ o₀ for any event 𝒜. This is the argument
of BASE `lemmas/L10_INTERFACES.md:11-15` with (T1⁺)(b).
(b) *Gaussian rows.* BASE `:16-18` with (T3⁺)(b) at Q = S₀ (`lemmas/P4_BR.md`; at Q = S₀ its display is that of
version 1.3.4).
(c) What the consumer gets: BASE `lemmas/L10_INTERFACES.md:19-24`, unchanged. ∎
