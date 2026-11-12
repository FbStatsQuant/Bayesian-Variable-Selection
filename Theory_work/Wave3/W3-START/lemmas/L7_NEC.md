# L7 — Necessity: Lemma NEC-b (C2) and Proposition NEC (T4)

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Statement proved: `STATEMENT.md` §5.1 (C2)(i), (ii); §5.3 (T4) (N1)–(N3); (N4) is a scope statement.
Uses `lemmas/L2_TK.md` (𝓔^blk; (TK-a), (TK-d), (TK-e), (TK-f); κ_E, ω̄_n, ϑ̄_n := (n + 0.02)/((n − 1)(1 − ω̄_n)) − 1, n₁),
`lemmas/L1_AGG_FLOOR.md` ((P1), (P2), (T0)), `lemmas/L6_COROLLARIES.md` (F2).

Setting: Setting F, (E), (GF-16) (the quantitative form of [TK]), the actual partition (blocks ≤ 16), s₀ fixed.
Ā := limsup log p/log n, A̲ := liminf log p/log n. π₀(S₀) ≤ γ₀(S₀)/γ₀(S′) for every S′ ∈ Ω, S′ ≠ S₀ (the normaliser
contains both terms).

## L7.1 (C2)(i): one leaking null on the actual partition

**Claim.** Suppose that for all large n there is a null l = l_n with δ²_{U,l} ≥ c·τ²_U·log n at U := U*_{b(l)}, with a fixed
c > 1 + 2Ā. Then P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (c − 1 − 2Ā)/2.

*Proof.* Fix κ′ and put 3ϵ := (c − 1 − 2Ā)/2 − κ′ > 0, ε₁ := min(½, ϵ/c). Let n be large: n ≥ max(n₁, 2s₀ + 2), so s₀ < K
(a null exists, so p > s₀), and S′ := S₀ ∪ {l} ∈ Ω. Let b := b(l). Then
  log[γ₀(S′)/γ₀(S₀)] = log[(s₀ + 1)/(2p − 1 − s₀)] + log[r_b(U ∪ {l})/r_b(U)].
*Event.* 𝒢 := 𝓔^blk ∩ {Z²_{U,l} ≤ 2 log log n}; Z_{U,l} ~ N(0, 1), so P(𝒢ᶜ) ≤ P((𝓔^blk)ᶜ) + 2/log n → 0.
*On 𝒢.* By (TK-d) and (f1): log[r_b(U ∪ l)/r_b(U)] ≥ −½ log(n + 1) + (RSS_U − RSS_{U∪l})/(2τ²_U(1 + ω̄_n)) − 2κ_E. By (TK-e) and
(a + b)² ≥ (1 − ε₁)a² − (1/ε₁ − 1)b²: RSS_U − RSS_{U∪l} = (δ_{U,l} + σZ_{U,l})² ≥ τ²_U[(1 − ε₁)c log n − 2 log log n/ε₁]. No upper
bound on the gain is used. Also (s₀ + 1)/(2p − 1 − s₀) ≥ 1/(2p) and log(2p) ≤ (Ā + ϵ) log n for large n. Hence
  log[γ₀(S′)/γ₀(S₀)] ≥ [(1 − ε₁)c/(2(1 + ω̄_n)) − ½ − Ā − ϵ] log n − log log n/ε₁ − ½ log(5/4) − 2κ_E.
(1 − ε₁)c/2 ≥ c/2 − ϵ/2, and the remaining corrections are o(log n); so the right side is ≥ [(c − 1 − 2Ā)/2 − 2ϵ] log n
≥ κ′ log n for large n. Thus π₀(S₀) ≤ γ₀(S₀)/γ₀(S′) ≤ n^{−κ′} on 𝒢. ∎

## L7.2 (C2)(ii): one weakly visible truth on the actual partition

**Claim.** Suppose that for all large n there is a truth j = j_n with δ²_{U,j} ≤ c·τ²_U·log n at U := U*_{b(j)} ∖ {j}, with a
fixed c < 1 + 2A̲ (c ≥ 0 without loss: for c < 0 the premise cannot hold). Then P(π₀(S₀) ≤ n^{−κ′}) → 1 for every
κ′ < (1 + 2A̲ − c)/2.

*Proof.* Fix κ′, 3ϵ := (1 + 2A̲ − c)/2 − κ′ > 0, ε₁ := min(1, ϵ/max(c, 1)). S′ := S₀ ∖ {j} ∈ Ω. With b := b(j), U ∪ {j} = U*_b:
  log[γ₀(S′)/γ₀(S₀)] = log[(2p − s₀)/s₀] + log[r_b(U)/r_b(U ∪ {j})]   ((P2)),
and by (TK-d): log[r_b(U)/r_b(U ∪ j)] ≥ ½ log(n + 1) − ν log(RSS_U/RSS_{U∪j}) − 2κ_E.
*Event.* 𝒢 := 𝓔^blk ∩ {Z²_{U,j} ≤ 2 log log n}, P(𝒢ᶜ) → 0.
*On 𝒢.* RSS_U − RSS_{U∪j} = (δ_{U,j} + σZ_{U,j})² ≤ (1 + ε₁)δ² + (1 + 1/ε₁)σ²Z² ≤ τ²_U·G_n,
G_n := (1 + ε₁)c log n + 2(1 + 1/ε₁) log log n. By (TK-a), x := (RSS_U − RSS_{U∪j})/RSS_U
≤ G_n/((n − 1)(1 − ω̄_n)) =: x̄_n → 0, so x ≤ ½ for large n and (f3) gives
ν log(RSS_U/RSS_{U∪j}) ≤ (1 + ϑ̄_n)(1 + x̄_n)G_n/2 = (1 + ε₁)(c/2) log n + o(log n)
(ϑ̄_n G_n → 0 because ω̄_n log n → 0). Also (2p − s₀)/s₀ ≥ p/s₀ and log p ≥ (A̲ − ϵ) log n for large n. Hence
  log[γ₀(S′)/γ₀(S₀)] ≥ [A̲ − ϵ + ½ − (1 + ε₁)c/2] log n − o(log n) ≥ [(1 + 2A̲ − c)/2 − 3ϵ/2] log n − o(log n) ≥ κ′ log n
for large n ((1 + ε₁)c/2 ≤ c/2 + ϵ/2). Thus π₀(S₀) ≤ n^{−κ′} on 𝒢. ∎

*Remarks.* (1) Each claim uses one Gaussian variable, at a deterministic witness; no union over columns is needed.
(2) (i) uses the lower bound (f1), valid for gains of any size; (ii) uses (f3), available because the assumed gain is
O(log n). (3) Both hold for every partition with blocks ≤ 16 that is a function of X.

## L7.3 Proposition NEC (T4)

Setting F, (E), (GF-16).
**(N1).** (T0) (`lemmas/L1_AGG_FLOOR.md` L1.5): o₀ ≥ ½(n + 1)^{−1/2} whenever s₀ < K, for every design and data set, so no
hypothesis gives an exponent better than ½ in (T1)–(T3); under F2 with η′ = 0 and κ_V > ½ the order n^{−1/2} is exact
(`lemmas/L6_COROLLARIES.md` L6.2(v)).
**(N2).** Let l = l_n be a null with δ²_{V,l} ≥ c·τ²_V·log n for every V ⊆ S₀ with |V| ≤ 15, c > 1 + 2Ā. For any partition,
U*_{b(l)} = S₀ ∩ C_{b(l)} ⊆ S₀ has at most 15 elements (l ∈ C_{b(l)} ∖ S₀), so it is one of the sets V; apply (C2)(i).
*Scope* (as recorded in `STATEMENT.md`): if s₀ ≤ 15, V = S₀ is admissible and δ_{S₀,l} = 0 because (I − P_{S₀})μ = 0, so the
premise is empty; (N2) has content only for s₀ ≥ 16, and for s₀ ≤ 15 the one-column threshold is the statement (C2)(i).
**(N3).** Let j = j_n be a truth with δ²_{V,j} ≤ c·τ²_V·log n for every V ⊆ S₀ ∖ {j} with |V| ≤ 15, c < 1 + 2A̲. The set
U*_{b(j)} ∖ {j} ⊆ S₀ ∖ {j} has at most 15 elements; apply (C2)(ii). The premise of (N3) is not empty in general (for
instance a truth orthogonal to the other truths with ‖x_j‖²θ*_j² = c′σ² log n, c′ < c). Consequently the constant
1 + 2A in (V-c), and in (V-m) for the instances D = {j}, N = ∅, cannot be lowered when log p/log n → A.
**(N4)** is a statement of scope (masked truths: W1-PXN:Thm-PXN(S)@1.0.0, status "XF VERIFIED", cited as a limit and
not consumed; strong-factor designs at p > K: nothing is claimed). Nothing is proved here. ∎
