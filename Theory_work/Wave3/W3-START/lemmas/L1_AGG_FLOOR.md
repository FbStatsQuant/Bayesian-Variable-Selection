# L1 — Lemma AGG (table identities) and FLOOR — claims (C0), (T0)

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`). Deterministic: no probability is used anywhere in this file.
Statement proved: `STATEMENT.md` §5.1 (C0) (AGG-a)–(AGG-d), (FLOOR), and §5.3 (T0). Notation of `STATEMENT.md` §1–§2.

## L1.0 Setting, conventions, elementary facts

Valid inputs, n ≥ 4, EX-A. {C_b} is any partition of [p] with |C_b| ≤ min(16, K). S₀ ∈ Ω is **any** reference model,
s₀ := |S₀|, U*_b := S₀ ∩ C_b, 𝔹* := {b : U*_b ≠ ∅}; Q ⊇ S₀ with |Q| ≤ K; c_Q := |Q| + 15s₀.
Tables: r_b(U) := m(U)/m(∅) for U ⊆ C_b; r_b(U) ∈ (0, ∞) by (L1.5)(i) below. γ₀(S) := w(|S|)∏_b r_b(S ∩ C_b) for
S ∈ Ω = {|S| ≤ K}; π₀ = γ₀/Σ_Ω γ₀. w(k) := ½/C(2p − 1, k) is used as a formula for every integer 0 ≤ k ≤ 2p − 1.
Parts L1.1–L1.4 use **only**: r_b > 0, the formula for w, K ≤ p, and the block-size bound. Rising factorial:
(x)_a := x(x + 1)⋯(x + a − 1), (x)_0 := 1.

**(P1)** w(k + 1)/w(k) = (k + 1)/(2p − 1 − k) for 0 ≤ k ≤ 2p − 2; it is ≤ (k + 1)/p when k ≤ p − 1.
**(P2)** w(k − 1)/w(k) = (2p − k)/k for 1 ≤ k ≤ 2p − 1; it is ≤ 2p, and it is ≥ p/k when k ≤ p.
*Proof.* C(2p − 1, k + 1)/C(2p − 1, k) = (2p − 1 − k)/(k + 1). ∎

**(P3) Path bound.** For integers 0 ≤ D ≤ k ≤ p and a ≥ 0 with k − D + a ≤ p:
  w(k − D + a)/w(k) ≤ (2p)^D · p^{−a} · (k − D + 1)_a.
*Proof.* w(k − D)/w(k) = ∏_{i=0}^{D−1} w(k − i − 1)/w(k − i) ≤ (2p)^D by (P2) (k − i ≥ 1). And
w(k − D + a)/w(k − D) = ∏_{i=0}^{a−1}(k − D + i + 1)/(2p − 1 − (k − D + i)) ≤ ∏_{i=0}^{a−1}(k − D + i + 1)/p by (P1), because
k − D + i ≤ k − D + a − 1 ≤ p − 1. ∎

**(P4)** For 0 ≤ u < 1 and real c > 0: Σ_{a≥0}(c)_a u^a/a! = (1 − u)^{−c} (binomial series).
**(P5)** For a finite set L and m_l ≥ 0: Σ_{N⊆L, |N|=a}∏_{l∈N}m_l ≤ (Σ_{l∈L}m_l)^a/a!.
*Proof.* (Σ_l m_l)^a is the sum of ∏ m_{l_i} over ordered a-tuples; each a-subset contributes a! tuples. ∎

**(CH) Chain bound.** Recall m_l := max{r_b(T ∪ {l})/r_b(T) : U*_b ⊆ T ⊆ C_b ∖ {l}}, b = b(l), for l ∉ S₀. Let T ⊆ C_b with
U*_b ⊆ T and N ⊆ C_b ∖ T with N ∩ S₀ = ∅. Then r_b(T ∪ N)/r_b(T) ≤ ∏_{l∈N}m_l.
*Proof.* Enumerate N = {l₁, …, l_a} and put T_i := T ∪ {l₁, …, l_i}. Then r_b(T ∪ N)/r_b(T) = ∏_{i=1}^a r_b(T_{i−1} ∪ {l_i})/r_b(T_{i−1}),
and U*_b ⊆ T_{i−1} ⊆ C_b ∖ {l_i}, so each factor is ≤ m_{l_i}. ∎

## L1.1 Decomposition of a model relative to the lattice

For S ∈ Ω put U_b := S ∩ C_b and **T(S) := (S ∩ Q) ∪ S₀**. Then S₀ ⊆ T(S) ⊆ Q, so T(S) ∈ 𝓛(Q) ⊆ Ω (|T(S)| ≤ |Q| ≤ K), and
S ∈ 𝓛(Q) ⟺ S = T(S). Write T_b := T(S) ∩ C_b = (U_b ∩ Q) ∪ U*_b.
* Block b is **bad for S** if U*_b ⊄ U_b (then b ∈ 𝔹*); put d_b := |U*_b ∖ U_b| ≥ 1 and a_b := |U_b ∖ Q|. Then
  T_b = T_b(U_b) in the notation of `STATEMENT.md` §2, |U_b| = |T_b| − d_b + a_b, and a_b ≤ 15 (U_b ∖ Q ⊆ C_b ∖ U*_b and
  U*_b ≠ ∅).
* Otherwise b is **good for S**: U_b = T_b ⊔ N_b with T_b = U_b ∩ Q ⊇ U*_b and N_b := U_b ∖ Q.
S is determined by T(S), its set of bad blocks, the sets U_b of the bad blocks, and N := ⊔_{b good}N_b ⊆ [p] ∖ Q.

**Lemma L1.1 (fibre bound).** For every T ∈ 𝓛(Q), every sub-family 𝔹′ ⊆ 𝔹* and every a′ ≥ 0, let 𝒮(T, 𝔹′, a′) be the set
of S ∈ Ω with T(S) = T, set of bad blocks 𝔹′, and |N| = a′. Then
  Σ_{S∈𝒮(T,𝔹′,a′)} γ₀(S) ≤ γ₀(T)·∏_{b∈𝔹′}Ξ_b(Q)·(κ₀ + 1)_{a′}·U_Q^{a′}/a′!,   κ₀ := c_Q if 𝔹′ ≠ ∅, κ₀ := |T| if 𝔹′ = ∅.

*Proof.* Fix S ∈ 𝒮(T, 𝔹′, a′). Put D := Σ_{b∈𝔹′}(d_b − a_b)₊ and E := Σ_{b∈𝔹′}(a_b − d_b)₊. Then |S| = |T| − D + E + a′,
D ≤ Σ_{b∈𝔹′}d_b ≤ s₀ ≤ |T|, and |S| ≤ K ≤ p. By (P3) with k := |T| and a := E + a′,
  w(|S|)/w(|T|) ≤ (2p)^D p^{−E−a′}(x)_{E+a′},   x := |T| − D + 1,   (x)_{E+a′} = (x)_E·(x + E)_{a′}.
If 𝔹′ = ∅ then D = E = 0 and (x)_{a′} = (|T| + 1)_{a′}. If 𝔹′ ≠ ∅: E ≤ Σ_{b∈𝔹′}a_b ≤ 15s₀ and |T| ≤ |Q|, so
x + E − 1 ≤ |T| + E ≤ c_Q; hence (x)_E ≤ (x + E − 1)^E ≤ c_Q^E (also when E = 0) and (x + E)_{a′} ≤ (c_Q + 1)_{a′}. In both cases
  w(|S|)/w(|T|) ≤ ∏_{b∈𝔹′}(2p)^{(d_b−a_b)₊}(c_Q/p)^{(a_b−d_b)₊} · (κ₀ + 1)_{a′}p^{−a′} = ∏_{b∈𝔹′}ω^Q(U_b) · (κ₀ + 1)_{a′}p^{−a′}.
(For b ∈ 𝔹′, U_b ∖ (Q ∪ S₀) = U_b ∖ Q, so the exponents are those of ω^Q(U_b).) For a good block, (CH) gives
r_b(U_b)/r_b(T_b) ≤ ∏_{l∈N_b}m_l. Therefore
  γ₀(S)/γ₀(T) ≤ ∏_{b∈𝔹′}[ω^Q(U_b)·r_b(U_b)/r_b(T_b)] · (κ₀ + 1)_{a′}p^{−a′}∏_{l∈N}m_l.
The map S ↦ ((U_b)_{b∈𝔹′}, N) is injective on 𝒮(T, 𝔹′, a′); U_b ranges in {U ⊆ C_b : U*_b ⊄ U, T_b(U) = T ∩ C_b} and N in
the a′-subsets of [p] ∖ Q. Summing the bound over all such tuples (a superset of the image),
  Σ_S γ₀(S)/γ₀(T) ≤ ∏_{b∈𝔹′}[Σ{ω^Q(U)r_b(U)/r_b(T ∩ C_b) : U ⊆ C_b, U*_b ⊄ U, T_b(U) = T ∩ C_b}] · (κ₀ + 1)_{a′}p^{−a′}·(pU_Q)^{a′}/a′!
by (P5) (Σ_{l∉Q}m_l = pU_Q). Since U*_b ⊆ T ∩ C_b ⊆ C_b ∩ Q, each bracket is ≤ Ξ_b(Q) by the definition of Ξ_b(Q). ∎

## L1.2 (AGG-a), lattice form

Let U_Q < 1. Summing Lemma L1.1 over a′ ≥ 0 with (P4), and using (|T| + 1)_{a′} ≤ (c_Q + 1)_{a′}, then over 𝔹′ ⊆ 𝔹*
(Σ_{𝔹′}∏_{b∈𝔹′}Ξ_b(Q) = ∏_{b∈𝔹*}(1 + Ξ_b(Q))), then over T ∈ 𝓛(Q):
  Σ_{S∈Ω}γ₀(S) ≤ F·Σ_{T∈𝓛(Q)}γ₀(T),   F := ∏_{b∈𝔹*}(1 + Ξ_b(Q))·(1 − U_Q)^{−(c_Q+1)} ≥ 1.
Hence π₀(𝓛(Q)) ≥ 1/F and **1 − π₀(𝓛(Q)) ≤ 1 − 1/F ≤ F − 1**, which is (AGG-a). ∎

## L1.3 (AGG-b), two-sided form at Q = S₀

Let Q = S₀ (so 𝓛(Q) = {S₀}, T(S) = S₀ for all S, c_Q = 16s₀), s₀ < K, U < 1. o₀ = Σ_{S∈Ω, S≠S₀}γ₀(S)/γ₀(S₀).
*Lower bound T₁.* For l ∉ S₀, S₀ ∪ {l} ∈ Ω (s₀ + 1 ≤ K) and γ₀(S₀ ∪ {l})/γ₀(S₀) = [w(s₀ + 1)/w(s₀)]·r_b(U*_b ∪ {l})/r_b(U*_b),
b = b(l). These models are distinct and differ from S₀, so o₀ ≥ T₁, and T₁ has the displayed form by (P1). Since
s₀ ≤ K − 1 ≤ p − 1, (P1) gives w(s₀ + 1)/w(s₀) ≤ (s₀ + 1)/p, and r_b(U*_b ∪ {l})/r_b(U*_b) ≤ m_l; hence **T₁ ≤ (s₀ + 1)U**.
*Upper bound.* Split {S ≠ S₀} by Lemma L1.1 with T = S₀.
(i) 𝔹′ = ∅, a′ = 1: these S are exactly the S₀ ∪ {l}, l ∉ S₀, and their total is T₁ (exact, no bound used).
(ii) 𝔹′ = ∅, a′ ≥ 2: total ≤ Σ_{a′≥2}(s₀ + 1)_{a′}U^{a′}/a′! = (1 − U)^{−(s₀+1)} − 1 − (s₀ + 1)U = R₂ by (P4).
(iii) 𝔹′ ≠ ∅: total ≤ [∏_{b∈𝔹*}(1 + Ξ_b) − 1]·(1 − U)^{−(16s₀+1)}.
(𝔹′ = ∅, a′ = 0 is S = S₀.) Adding: **o₀ ≤ T₁ + R₂ + [∏_{b∈𝔹*}(1 + Ξ_b) − 1](1 − U)^{−(16s₀+1)}**.
*Lower bound c_sΞ.* Let s₀ + 16 ≤ K and b ∈ 𝔹* (so s₀ ≥ 1). For U ⊆ C_b with U*_b ⊄ U put S_U := (S₀ ∖ U*_b) ∪ U, d := |U*_b ∖ U|,
a := |U ∖ S₀|. Then |S_U| = s₀ − d + a ≤ s₀ + 15 ≤ K, so S_U ∈ Ω; S_U ≠ S₀; U ↦ S_U is injective; and
γ₀(S_U)/γ₀(S₀) = [w(s₀ − d + a)/w(s₀)]·r_b(U)/r_b(U*_b). Claim: w(s₀ − d + a)/w(s₀) ≥ c_s·ω(U), ω(U) = (2p)^{(d−a)₊}(16s₀/p)^{(a−d)₊}.
* d ≥ a, e := d − a ≤ min(s₀, 16): by (P2), w(s₀ − e)/w(s₀) = ∏_{i=0}^{e−1}(2p − s₀ + i)/(s₀ − i) ≥ (p/s₀)^e = (2p)^e(2s₀)^{−e}
  ≥ (2p)^e(2s₀)^{−16} (2p − s₀ ≥ p as s₀ ≤ p).
* a > d, e := a − d ≤ 15: by (P1), w(s₀ + e)/w(s₀) = ∏_{i=0}^{e−1}(s₀ + i + 1)/(2p − 1 − s₀ − i) ≥ ((s₀ + 1)/(2p))^e
  = (16s₀/p)^e·((s₀ + 1)/(32s₀))^e ≥ (16s₀/p)^e·32^{−15}.
Both are ≥ c_s·ω(U) with c_s = (64s₀)^{−16}. Summing over U: **o₀ ≥ c_sΞ_b** for every b ∈ 𝔹*, i.e. o₀ ≥ c_sΞ (trivial if s₀ = 0). ∎

## L1.4 (AGG-c) and (AGG-d)

**(AGG-c).** Here m_l is also defined, by the same formula, for l ∈ Q ∖ S₀ ((CH) holds for every N disjoint from S₀).
1/π₀(S₀) = Σ_{S∈Ω}γ₀(S)/γ₀(S₀). Fix S; d_b := |U*_b ∖ U_b|, d := Σ_b d_b = |S₀ ∖ S|, N_Q := S ∩ Q ∖ S₀, N_o := S ∖ Q,
a_Q := |N_Q|, a_o := |N_o|. For each block,
  r_b(U_b)/r_b(U*_b) = [r_b(U_b)/r_b(U_b ∪ U*_b)]·[r_b(U_b ∪ U*_b)/r_b(U*_b)] ≤ (e_n/(2p))^{d_b}·∏_{l∈U_b∖S₀}m_l:
the first factor is 1 if d_b = 0 and is ≤ (e_n/(2p))^{d_b} by the definition of e_n if d_b ≥ 1; the second is (CH) with
T = U*_b, N = U_b ∖ S₀ (|U_b ∪ U*_b| ≤ |C_b| ≤ K, so the table entry exists). By (P3) with k = s₀, D = d, a = a_Q + a_o
(k − D + a = |S| ≤ p): w(|S|)/w(s₀) ≤ (2p)^d p^{−a}(s₀ − d + 1)_a ≤ (2p)^d p^{−a}(s₀ + 1)_{a_Q}(s₀ + a_Q + 1)_{a_o}
≤ (2p)^d p^{−a}|Q|^{a_Q}(|Q| + 1)_{a_o} (s₀ + a_Q ≤ |Q|). So
  γ₀(S)/γ₀(S₀) ≤ e_n^d·∏_{l∈N_Q}(|Q|m_l/p)·(|Q| + 1)_{a_o}p^{−a_o}∏_{l∈N_o}m_l.
S is determined by (S₀ ∖ S, N_Q, N_o); summing over all subsets of S₀, of Q ∖ S₀ and (by (P5), (P4), U_Q < 1) of [p] ∖ Q:
**1/π₀(S₀) ≤ (1 + e_n)^{s₀}·∏_{l∈Q∖S₀}(1 + |Q|m_l/p)·(1 − U_Q)^{−(|Q|+1)}**. ∎

**(AGG-d).** Let c_QU_Q ≤ 1, b ∈ 𝔹* (so s₀ ≥ 1, c_Q ≥ 1, U_Q ≤ 1). Fix T′ with U*_b ⊆ T′ ⊆ C_b ∩ Q and U ⊆ C_b with U*_b ⊄ U,
T_b(U) = T′; d := |U*_b ∖ U| ∈ [1, 16], N := U ∖ Q, a := |N|. Then U ∪ U*_b = T′ ⊔ N and
  r_b(U)/r_b(T′) = [r_b(U)/r_b(U ∪ U*_b)]·[r_b(T′ ⊔ N)/r_b(T′)] ≤ (e_n/(2p))^d·∏_{l∈N}m_l ≤ (e_n/(2p))^d(pU_Q)^a
(definition of e_n; (CH); m_l ≤ Σ_{l′∉Q}m_{l′} = pU_Q for l ∉ Q). Multiply by ω^Q(U):
* d ≥ a: (2p)^{d−a}(e_n/(2p))^d(pU_Q)^a = e_n^d(U_Q/2)^a ≤ e_n^d;
* a > d: (c_Q/p)^{a−d}(e_n/(2p))^d(pU_Q)^a = e_n^d(c_QU_Q)^{a−d}(U_Q/2)^d ≤ e_n^d.
There are at most 2^{16} sets U ⊆ C_b, and e_n^d ≤ max(e_n, e_n^{16}); hence **Ξ_b(Q) ≤ 2^{16}max(e_n, e_n^{16})**. ∎

## L1.5 (FLOOR) and Theorem (T0)

Scorer (`STATEMENT.md` §1): m(S) = c_n·D_S^{−1/2}·(2b₀ + Q_S)^{−ν}, D_S := det H_S/det(G_S + I), H_S = (n + 1)G_S + I,
Q_S = yᵀy − n z_SᵀH_S⁻¹z_S; D_∅ = 1, Q_∅ = yᵀy. No rank condition on X_S is used below (H_S ≻ 0 and G_S + I ≻ 0 always).

**(i) Q is a ridge criterion, non-negative and monotone.** With λ := 1/(n + 1): nH_S⁻¹ = (n/(n + 1))(G_S + λI)⁻¹, and
ρ_S := min_{β∈ℝ^S}{‖y − X_Sβ‖² + λ‖β‖²} = yᵀy − z_Sᵀ(G_S + λI)⁻¹z_S. Hence
  Q_S = yᵀy/(n + 1) + (n/(n + 1))·ρ_S.
So Q_S ≥ 0 (thus 2b₀ + Q_S > 0 and m(S) ∈ (0, ∞)), and for S ⊆ S′: ρ_{S′} ≤ ρ_S (minimum over a larger space), hence
Q_{S′} ≤ Q_S.
**(ii) One-step determinant ratio.** Let l ∉ S, g := X_Sᵀx_l. For λ > 0 put s(λ) := x_lᵀx_l + λ − gᵀ(G_S + λI)⁻¹g. Schur
complements give det(G_{S∪l} + λI) = det(G_S + λI)·s(λ), and H_S = (n + 1)(G_S + I/(n + 1)), so
  D_{S∪l}/D_S = (n + 1)·s(1/(n + 1))/s(1).
s is positive (a Schur complement of a positive definite matrix) and nondecreasing: s′(λ) = 1 + gᵀ(G_S + λI)^{−2}g > 0.
Hence **D_{S∪l}/D_S ≤ n + 1**.
**(iii)** By (i), (ii) and ν > 0: for every S and l ∉ S with |S| + 1 ≤ K,
  **m(S ∪ {l})/m(S) = (D_{S∪l}/D_S)^{−1/2}·((2b₀ + Q_S)/(2b₀ + Q_{S∪l}))^ν ≥ (n + 1)^{−1/2}.**
**(iv) Floor for π₀.** Let S ∈ Ω, k := |S| < K. For l ∉ S, with b = b(l): S ∪ {l} ∈ Ω and
γ₀(S ∪ {l})/γ₀(S) = [w(k + 1)/w(k)]·m((S ∩ C_b) ∪ {l})/m(S ∩ C_b) ≥ [(k + 1)/(2p − 1 − k)]·(n + 1)^{−1/2} by (P1) and (iii)
applied inside the block (|(S ∩ C_b) ∪ {l}| ≤ |C_b| ≤ K). Summing over the p − k indices l ∉ S:
  (1 − π₀(S))/π₀(S) ≥ Σ_{l∉S}γ₀(S ∪ {l})/γ₀(S) ≥ f_n(k) = (k + 1)(p − k)/((2p − 1 − k)√(n + 1)),
so **1 − π₀(S) ≥ f_n(k)/(1 + f_n(k))**. For k < p: 2(k + 1)(p − k) − (2p − 1 − k) = k(2(p − k) − 1) + 1 > 0, so
f_n(k) ≥ ½(n + 1)^{−1/2} =: f. As x ↦ x/(1 + x) is increasing and f ≤ ½·5^{−1/2} < ½ (n ≥ 4):
f_n(k)/(1 + f_n(k)) ≥ f/(1 + f) ≥ (2/3)f = ⅓(n + 1)^{−1/2}. (K ≤ p, so k < K implies k < p.) This is (FLOOR) and the first
display of (T0).
**(v)** If s₀ < K, the same sum with S = S₀ is T₁ (L1.3), so **o₀ ≥ T₁ ≥ f_n(s₀) ≥ ½(n + 1)^{−1/2}**: the second display of
(T0). ∎

## L1.6 Remarks
1. Lemma L1.1 gives slightly more than (AGG-a): 1 − π₀(𝓛(Q)) ≤ 1 − 1/F.
2. Where the constants come from: 15 = the largest number of nulls in a block that contains a truth (a_b ≤ 15); c_Q bounds
   every intermediate size on the path of (P3) after the bad blocks have been handled; c_s loses (2s₀)^{−16} and 32^{−15}.
3. (FLOOR) holds for rank-deficient X_S as well, and for the posterior ratio in the same way (not claimed in the
   statement).
