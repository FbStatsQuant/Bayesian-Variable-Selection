# P3 — Proposition NEC (T4⁺): the partition-free leaking-null limit (N2⁺)

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Citations: BASE `path:lines` is a file of the base ticket; a short citation `:a-b` continues the file cited last before it.
Statement proved: `STATEMENT.md` §3.2 (T4⁺): clause (N2⁺), its scope paragraph (including the statement that its premise
can hold together with (E) and (GF-16)), and the clauses (N1), (N3), (N4). BASE := `Theory_work/Wave3/W3-START/`.
Uses: (C2)(i) (BASE `STATEMENT.md:221-224`; proved in BASE `lemmas/L7_NEC.md:14-26`), BASE `lemmas/L7_NEC.md:53-65`
((N1), (N3), (N4)), and `lemmas/P1_LEADING.md` P1.6 (F2⁺, for (N1)).

Setting: Setting F, (E), (GF-16); a partition {C_b} of [p] with blocks of size ≤ 16 that is a function of X (BASE
`STATEMENT.md:62-63`); in Setting F it is deterministic. Ā := limsup log p/log n.

## P3.1 A counting fact

**Lemma P3.1.** Let 1 ≤ s₀ ≤ 15 and let I ⊆ [p] ∖ S₀ have 17 − s₀ elements. Then some l ∈ I has U*_{b(l)} ⊊ S₀.
*Proof.* Suppose U*_{b(l)} = S₀ for every l ∈ I, that is, S₀ ⊆ C_{b(l)}. Fix j ∈ S₀ (s₀ ≥ 1) and let C be the block that
contains j; the blocks are disjoint, so C_{b(l)} = C for every l ∈ I. Then S₀ ∪ I ⊆ C. This union is disjoint and has
s₀ + (17 − s₀) = 17 elements, but |C| ≤ 16: a contradiction. ∎

## P3.2 Clause (N2⁺)

**Hypothesis.** s₀ ≥ 1, r(s₀) := max(1, 17 − s₀). For all large n there is a deterministic set I_n ⊆ [p] ∖ S₀ of r(s₀)
distinct nulls with δ²_{V,l} ≥ c·τ²_V·log n for every l ∈ I_n and every V ⊊ S₀ with |V| ≤ 15; c > 1 + 2Ā fixed.
**Claim.** P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (c − 1 − 2Ā)/2.

*Proof.* Let n be large enough for the hypothesis. Choose a witness l_n ∈ I_n as follows.
* If s₀ ≥ 16: I_n = {l_n}. The set U*_{b(l_n)} = S₀ ∩ C_{b(l_n)} lies in C_{b(l_n)} ∖ {l_n}, so it has at most 15 < s₀ elements:
  it is a proper subset of S₀.
* If 1 ≤ s₀ ≤ 15: |I_n| = 17 − s₀, and by Lemma P3.1 the set {l ∈ I_n : U*_{b(l)} ⊊ S₀} is not empty; let l_n be its
  smallest element. Here |U*_{b(l_n)}| ≤ s₀ − 1 ≤ 14.

In both cases l_n is a null column determined by X and I_n (no use of the response), and V := U*_{b(l_n)} is a proper
subset of S₀ with |V| ≤ 15. By hypothesis, δ²_{V,l_n} ≥ c·τ²_V·log n at V = U*_{b(l_n)}. This is the premise of (C2)(i) on the
actual partition with the null l_n and the same constant c > 1 + 2Ā; (C2)(i) gives the claim. ((C2) is stated under
[TK]; under (E) and (GF-16), [TK] holds by (B-TK), BASE `STATEMENT.md:233`; the proof in BASE `lemmas/L7_NEC.md:14-26`
uses 𝓔^blk and one Gaussian variable at the deterministic witness.) ∎

**(N2⁺) and (N2).** For s₀ ≥ 16, r(s₀) = 1 and every V ⊆ S₀ with |V| ≤ 15 is proper, so the hypothesis and the
conclusion of (N2⁺) are those of (N2) (BASE `STATEMENT.md:318-319`). For 1 ≤ s₀ ≤ 15 the premise of (N2) cannot hold
(BASE `STATEMENT.md:320-321`), so (N2) asserts nothing there. Hence (T4⁺) implies (T4).

## P3.3 The premise of (N2⁺) can hold (1 ≤ s₀ ≤ 15)

**Example P3.3** (an example, not a hypothesis of any claim). Fix s := s₀ ∈ {1, …, 15}, r := 17 − s, θ ≠ 0, σ² > 0 and
c > 1. Let p := 17, S₀ := {1, …, s}, I := {s + 1, …, 17}, and for n ≥ 18
  ρ_n² := c·(σ² + sθ²)·log n/((n − 1)θ²)  (ρ_n > 0),   G_n := [[I_s, ρ_n·1_s1_rᵀ], [ρ_n·1_r1_sᵀ, I_r]] ∈ ℝ^{17×17}.
* *G_n is positive definite for large n.* G_n = I + ρ_nB with B := [[0, 1_s1_rᵀ], [1_r1_sᵀ, 0]]; B has rank 2 and its non-zero
  eigenvalues are ±√(sr) (B² = diag(r·1_s1_sᵀ, s·1_r1_rᵀ), with largest eigenvalue sr). So the eigenvalues of G_n are
  1 − ρ_n√(sr), 1, 1 + ρ_n√(sr). Since sr ≤ 72 and ρ_n → 0: λ_min(G_n) ≥ ½ for large n.
* *The design.* Let O be n × 17 with orthonormal columns orthogonal to 1_n (n ≥ 18), and X := √(n − 1)·O·G_n^{1/2}. The
  columns of X are centred and XᵀX = (n − 1)G_n, so each column has sample variance 1: X is a standardised design
  (raw design X^r := X, D_x = I), with x_jᵀx_k = (n − 1)(G_n)_{jk}. Coefficients: θ*_j := θ for j ∈ S₀, 0 otherwise;
  μ = θ·Σ_{j∈S₀}x_j.
* *(E).* ‖μ‖² = θ²·(n − 1)·s ≤ Mn with M := sθ²; p = 17 ≤ n^A for large n (any A > 0); p > s₀. Here Ā = 0.
* *(GF-16).* For 1 ≤ |T| ≤ 16: λ_min(X_TᵀX_T) ≥ (n − 1)λ_min(G_n) ≥ (n − 1)/2 ≥ 1 =: g_* for large n.
* *The premise.* Let l ∈ I and V ⊊ S₀, v := |V| ≤ s − 1 ≤ 14. The truth columns are mutually orthogonal, so
  (I − P_V)μ = θ·Σ_{j∈S₀∖V}x_j, Λ_V = (n − 1)(s − v)θ², Δ_V = (s − v)θ², τ²_V = σ² + (s − v)θ².
  (I − P_V)x_l = x_l − ρ_n·Σ_{k∈V}x_k (the columns of V are orthonormal up to the factor n − 1, and x_kᵀx_l = (n − 1)ρ_n), so
  ‖(I − P_V)x_l‖² = (n − 1)(1 − vρ_n²) > 0 and x_lᵀ(I − P_V)μ = μᵀ(I − P_V)x_l = θ·Σ_{j∈S₀∖V}x_jᵀx_l = (n − 1)θ(s − v)ρ_n
  (x_jᵀx_k = 0 for j ∈ S₀ ∖ V, k ∈ V). Hence
    δ²_{V,l} = (n − 1)θ²(s − v)²ρ_n²/(1 − vρ_n²) ≥ (n − 1)θ²(s − v)²ρ_n² = c·(σ² + sθ²)·(s − v)²·log n ≥ c·τ²_V·log n,
  because s − v ≥ 1 and σ² + sθ² ≥ σ² + (s − v)θ² = τ²_V.
So for all large n the set I_n := I of 17 − s₀ nulls satisfies the premise of (N2⁺) with this c > 1 = 1 + 2Ā, together
with (E) and (GF-16); (N2⁺) gives P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (c − 1)/2. ∎

*Remarks.* (1) The premise of (N2⁺) involves only the columns of S₀ ∪ I_n. (2) In the example δ_{S₀,l} = 0 for every null
l (as always), which is why V = S₀ had to be removed from the premise. (3) With fewer than 17 − s₀ leaking nulls the
counting argument fails: a block may hold S₀ and up to 16 − s₀ nulls, and for a null l in that block (C2)(i) is a
statement about δ_{S₀,l} = 0. No partition-free limit is claimed in that case (`STATEMENT.md` §4).

## P3.4 Clauses (N1), (N3), (N4)

**(N1)** is BASE `lemmas/L7_NEC.md:53-55` with (T1⁺)–(T3⁺) and F2⁺ in place of (T1)–(T3) and F2: (T0) gives
o₀ ≥ ½(n + 1)^{−1/2} whenever s₀ < K, and under F2⁺ with η′ = 0 and κ_V > ½ the order n^{−1/2} is exact
(`lemmas/P1_LEADING.md` P1.6(v)). **(N3)** and **(N4)**: BASE `lemmas/L7_NEC.md:60-65`, unchanged. ∎
