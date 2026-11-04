# T06 and T07: identifiability and exact ties; size-only ranking ceiling and Bayes decisions

Sources: `theorems/T06_A5_identifiability_ties.md`, `theorems/T07_A6_size_prior_ceiling.md`, `theorems/00_COMMON.md`; method SMC-BVS v3.0 (METHODOLOGY_v3.md, authoritative). Statement checker: approved with required edits (review/STATEMENT_CHECK.md); all edits applied.

## 0. Setting and notation

- Valid input (method §4): finite raw data, n ≥ 3, p ≥ 1 after dropping exactly constant columns, non-constant raw response. C = I − 11ᵀ/n and V = range(C) = {v ∈ ℝⁿ : 1ᵀv = 0}, of dimension n − 1.
- The standardised design X has columns x_j ∈ V with ‖x_j‖² = n − 1. Every such matrix arises from valid raw data (take X^r = X). Correlations: r_ij = x_iᵀx_j/(n − 1).
- The set of standardised responses is the contrast sphere 𝕊 = {y ∈ V : ‖y‖² = n − 1}. It is exactly the set of values of y = Cy^r/s_y over non-constant raw responses y^r.
- K = min(p, ⌊n/2⌋) and Ω = {S ⊆ [p] : |S| ≤ K} (the feasible models).
- Score formulas, quoted verbatim from `theorems/00_COMMON.md` §1 (the target uses β_S ~ N(0, nσ²(G_S+I)⁻¹), σ² ~ IG(0.01, 0.01), BB(1, p) capped at K):
  - "G_S = X_SᵀX_S = (n−1)R_S; z_S = X_Sᵀy; H_S = (n+1)G_S + I; D_S = det H_S/det(G_S+I); Q_S = yᵀy − n z_SᵀH_S⁻¹z_S; ν = 0.01 + n/2; a₀ = b₀ = 0.01."
  - "m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{−1/2}(2b₀ + Q_S)^{−ν}; w(k) = ½/C(2p−1, k); W_K = Σ_{k≤K} C(p,k)w(k); ϖ(S) = w(|S|)/W_K."
  - "F(S) = log[ϖ(S)m(S)]; Z = Σ_Ω ϖ(S)m(S); π(S) = e^{F(S)}/Z"
- Hence for S ⊆ [p]: G_S, z_S, H_S, D_S, Q_S, ν = a₀ + n/2, a₀ = b₀ = 0.01, m(S), w(k), W_K, ϖ(S) = w(|S|)/W_K, F(S) = log[ϖ(S)m(S)], Z, π(S) = e^{F(S)}/Z on Ω and π(a) := 0 for a ⊆ [p] with a ∉ Ω, PIP_j = π({S : j ∈ S}) and MPM = {j : PIP_j > ½}. All are as in 00_COMMON §1. X_∅X_∅ᵀ := 0, D_∅ = 1 and Q_∅ = yᵀy.
- The score function of S is F_S : 𝕊 → ℝ, y ↦ F(S) computed at the response y (X fixed).
- Tie order (method §6.10): ≺ orders models by smaller size, then by the lexicographically smaller sorted index list. S† is the ≺-least element of argmax_Ω F.
- 𝒮 ⊆ Ω is the nonempty set of all scored models. Ŝ is the ≺-least element of argmax_𝒮 F.
- Statistical model G: X^r is the fixed retained n × p raw design (its retained columns, after dropping exactly constant ones, index [p]; D_x is the positive diagonal matrix of their raw sample SDs, so X = CX^rD_x⁻¹) and y^r = α1 + X^rβ + ε, with ε ~ N_n(0, σ*²I) and σ*² > 0. μ = CX^rβ ∈ V, m_θ = α1 + X^rβ (the mean of y^r), S₀ = supp β, s₀ = |S₀|. P₀ is the law of y^r. The event Cy^r = 0 has P₀-probability 0, and y = Cy^r/s_y is defined off it.
- NIS: there are no S ≠ S′ in Ω with X_SX_Sᵀ = X_{S′}X_{S′}ᵀ.
- DUP(a): there are i ≠ j with x_i = ±x_j (equivalently |r_ij| = 1).
- A *selector* is a measurable map δ = δ(y^r, U) into the subsets of [p]. U is an auxiliary randomisation, independent of y^r, with a law not depending on the truth. δ is *location-invariant* if it depends on y^r only through Cy^r (δ = h(Cy^r, U)). Every measurable function of the standardised data (X, y) and of U is location-invariant (y = Cy^r/s_y is a function of Cy^r); in particular S†, π, PIP and MPM are. Its error at a truth θ is P_θ(δ ≠ S₀(θ)).
  - *Remark (not part of the theorem):* the method's reported outputs are computed from the standardised data and its own random streams (method §4), so they are location-invariant up to the method's numerical preprocessing. This is not proved here and nothing below depends on it.
- Φ is the standard normal cdf.

## 1. T06: identifiability and exact ties

**(i) Exact ties.**

(a) For S, S′ ∈ Ω: F_S = F_{S′} on 𝕊 if and only if X_SX_Sᵀ = X_{S′}X_{S′}ᵀ. If X_SX_Sᵀ = X_{S′}X_{S′}ᵀ then |S| = |S′|, and moreover F(S) = F(S′) for every response vector put into the formulas.

(b) Hence if span(X_S) = span(X_{S′}) but X_SX_Sᵀ ≠ X_{S′}X_{S′}ᵀ, the score functions differ somewhere on 𝕊. Such feasible pairs exist for some valid input at every n ≥ 4 (with p = 4); they never exist when K = 1 (in particular when n = 3).

(c) Under G, P₀-almost surely, every exact tie F(S) = F(S′) at the observed y between models S ≠ S′ in Ω has X_SX_Sᵀ = X_{S′}X_{S′}ᵀ. Consequently, under G and NIS,

  P₀(∃ S ≠ S′ in Ω with F(S) = F(S′)) = 0.

**(ii) Fallback without NIS.**

(a) Deterministic: for every valid input, every S₀ ⊆ [p] and every response, on the event {π(S₀) > ½} one has S₀ ∈ Ω and F(S₀) > F(S) for every S ∈ Ω ∖ {S₀}. So argmax_Ω F = {S₀}, and S† = S₀ for every tie rule (the tie rule is not invoked).

(b) Hypothesis H-T03 (T03 is unproved; this clause is **conditional on T03**). `theorems/T03_A2_selection_consistency.md` states, verbatim: "In R1 under G, R, SE and BM-C (or BM-∞): (i) 1 − π(S₀) = O_{P₀}(r_n)." with r_n := √(log n/n) (00_COMMON §1). H-T03 is the assumption that this conclusion holds along the sequence considered; the only consequence used is π(S₀) → 1 in P₀-probability. Under H-T03, P₀(π(S₀) > ½) → 1, so the conclusions of (a) hold with probability → 1. NIS is not assumed.

**(iii) Duplicates and weak separation.**

(a) Under DUP(a), let τ be the transposition of i and j acting on subsets of [p]. For every S ∈ Ω: τS ∈ Ω, |τS| = |S| and F(τS) = F(S) for every y.

(b) Under DUP(a), if S ∈ Ω contains exactly one of i and j, then τS ≠ S, π(τS) = π(S) and π(S) < ½. Also PIP_i = PIP_j.

(c) Two-point bound. Let θ_k = (α_k, β_k), k = 1, 2, be two truths under G with the same X^r and the same σ*² > 0, and with supports S₁ ≠ S₂. Put μ_k = CX^rβ_k and m_k = α_k1 + X^rβ_k. For every selector δ,

  max_k P_{θ_k}(δ ≠ S_k) ≥ ½ Σ_k P_{θ_k}(δ ≠ S_k) ≥ Φ(−‖m₁ − m₂‖/(2σ*)).

Here ‖m₁ − m₂‖² = ‖μ₁ − μ₂‖² + (1ᵀ(m₁ − m₂))²/n, so ‖m₁ − m₂‖ = ‖μ₁ − μ₂‖ if and only if 1ᵀm₁ = 1ᵀm₂, i.e. α₁ + x̄^{r⊤}β₁ = α₂ + x̄^{r⊤}β₂ (equal mean of y^r; this is *not* α₁ = α₂). Call such a pair *mean-matched*. For every location-invariant selector, and any intercepts,

  max_k P_{θ_k}(δ ≠ S_k) ≥ Φ(−‖μ₁ − μ₂‖/(2σ*)).

(d) No uniform recovery. For each n, let Θ_n be a class of truths under G (σ*² may depend on the pair) containing a pair θ_{1,n}, θ_{2,n} with a common design X^r_n, distinct supports and common noise variance σ_n², such that ‖μ_{1,n} − μ_{2,n}‖/σ_n → 0. Then every sequence of location-invariant selectors satisfies liminf_n sup_{θ∈Θ_n} P_θ(δ_n ≠ S₀(θ)) ≥ ½. The same holds for every sequence of selectors if the pairs are mean-matched (1ᵀm_{1,n} = 1ᵀm_{2,n}). In particular, uniform recovery over Θ_n is impossible. Under DUP(a) with x_i = s·x_j (s = ±1), the truths θ* = b e_i and θ* = s·b e_j (b ≠ 0, θ* = D_xβ) have μ₁ = μ₂. With a common X^r and a common σ*², every location-invariant selector then has maximal error ≥ ½ over this pair (intercepts arbitrary).

(e) The near-duplicate report is a warning, not an exact-identifiability statement. The method reports the components of {|r_ij| ≥ 1 − 10⁻¹⁰}.
  - For i ≠ j, A ⊆ [p] ∖ {i, j} and |A| + 1 ≤ K: F_{A∪{i}} = F_{A∪{j}} on 𝕊 if and only if |r_ij| = 1. So a reported pair with |r_ij| < 1 gives no such identity.
  - For every n ≥ 4 there are valid inputs (with p = 4) with feasible S ≠ S′ and X_SX_Sᵀ = X_{S′}X_{S′}ᵀ (identical score functions) in which no pair is reported: max_{i≠j} |r_ij| ≤ 1/√2. (When K = 1, every pair of distinct feasible models with equal outer products is {i}, {j} with |r_ij| = 1, hence reported.)

## 2. T07: size-only ranking ceiling and Bayes decisions

Setting. m is the marginal likelihood (only m > 0 is used). ≺ is the tie order above; any fixed total order on subsets of [p] works. For a positive size-only prior on Ω, w̃(k) > 0 for 0 ≤ k ≤ K and ϖ_w̃(S) = w̃(|S|)/Σ_{k≤K} C(p,k) w̃(k). S†_w̃ is the ≺-least element of argmax_{S∈Ω} ϖ_w̃(S)m(S). For 0 ≤ k ≤ p, S*_k is the ≺-least element of argmax_{|S|=k} m(S).

**(i) Ceiling.** For every response and every positive size-only prior w̃, {S†_w̃ = S₀} ⊆ {S*_{s₀} = S₀}. Here s₀ ≤ K on the left event, which is empty when s₀ > K. Equivalently: on {S*_{s₀} ≠ S₀} (a within-size ranking error, S₀ beaten or ≺-preceded within its size by m), S†_w̃ ≠ S₀ for every positive size-only prior. No size-only prior repairs it.

**(ii) Bayes decisions.** π is the target posterior on Ω. J₊ = {j : PIP_j > ½} and N₊ = |J₊|. The posterior risk of an action a under a loss L is ρ_L(a) = Σ_S π(S) L(a, S).

(a) For the 0–1 loss on supports, L(a, S) = 1{a ≠ S} with a ⊆ [p]: ρ(a) = 1 − π(a) (with π(a) = 0 for a ∉ Ω). The minimisers over all a ⊆ [p] are exactly argmax_Ω F, and S† is one of them.

(b) For the Hamming loss, L(a, S) = |a △ S| with a ⊆ [p]: MPM = J₊ minimises ρ_H over all subsets of [p]. It is the unique minimiser if and only if no PIP_j equals ½.

(c) Capped. Put ℓ = min(K, N₊). Let a* ⊆ J₊ be the ℓ elements of J₊ with the largest PIPs, with ties at the boundary broken by a fixed deterministic rule. Then a* minimises ρ_H over Ω = {a : |a| ≤ K}.

**(iii) Target versus reported decisions.** (i)–(ii) concern S†, π and PIP. (Interpretation, not a separate claim: for the reported objects they hold only through scoring and estimation events.)

(a) Ŝ = S† if and only if S† ∈ 𝒮. Ŝ minimises the posterior 0–1 loss if and only if 𝒮 ∩ argmax_Ω F ≠ ∅.

(b) {Ŝ = S₀} ∩ {S*_{s₀} ≠ S₀} ⊆ {S*_{s₀} ∉ 𝒮}. (Interpretation, not a separate claim: the ceiling of (i) is a statement about S†; for Ŝ the corresponding event depends on 𝒮.)

(c) Let p̂ ∈ [0,1]^p be any PIP estimate and 𝒜 the action class: all subsets for the MPM rule, Ω for the capped rule. Let â minimise Σ_{j∈a}(1 − 2p̂_j) over 𝒜 (MPM̂ = {j : p̂_j > ½}, or the capped rule of (ii)(c) applied to p̂). For any minimiser a_opt of ρ_H over 𝒜,

  0 ≤ ρ_H(â) − ρ_H(a_opt) ≤ 2 Σ_{j ∈ â △ a_opt} |p̂_j − PIP_j| ≤ 2‖p̂ − PIP‖₁.

MPM̂ = MPM if and only if, for every j, p̂_j > ½ ⇔ PIP_j > ½.

Interpretation (not a separate claim): the scoring events and estimation errors in (a)–(c) are not controlled by (i)–(ii). Their control is the subject of computational results (T21, T23, T26), which this document neither uses nor proves.

## 3. Readings and precisions (change report for the statement checker)

See `review/CHANGE_REPORT.md` (items 1–11) and the checker's reply `review/STATEMENT_CHECK.md`.

- Statement check (2026-10-22): APPROVED WITH REQUIRED EDITS, all applied: mean-matched wording; H-T03 quoted verbatim and (ii)(b) marked conditional on T03; π := 0 off Ω; the claim about the method's reported outputs moved to a labelled remark; quantifiers in (ii)(a) and (iii)(d); n ≥ 4 for the existence examples; the generic selector renamed δ.
- After review round 1 (2026-10-22): the 00_COMMON score formulas are quoted verbatim in §0; D_x is defined; the n ≥ 4 / K = 1 parentheticals in (i)(b) and (iii)(e) are made precise (checker consulted: review/STATEMENT_CHECK_2.md); the common X^r and σ*² of the duplicate pair are explicit; the interpretive sentences of T07(iii) are labelled as such. Claims in (i)(b) and (iii)(e) made precise (strengthened; approved, review/STATEMENT_CHECK_2.md); no other claim changed.
