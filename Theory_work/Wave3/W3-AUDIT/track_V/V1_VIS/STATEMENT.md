# V1 · Lemma VIS (visibility with a margin uniform in n: a sign route and a generic-position route) — STATEMENT v1 (draft, not locked)

Track V item V1 (manager 11-17, D112; owner + consultant requirement: a margin **uniform in n**, not "nonzero for almost
every β"). Tier B (new lemma; pure linear algebra and topology, no code). **Lean target: yes** (finite-dimensional:
Schur complements, Stieltjes matrices, closed sets of hyperplanes; every statement is for one fixed n plus a uniform
bound).

## Target condition
The population visibility condition of Theorem 6 (A3), Theorem 5 (A4) and Theorem 10 (A4) (`Theory_work/Wave3/W3-READER/READER_VERSIONS.md`
on main 029bb748, lines 581-582, 672-673, 1292): for a fixed a > 0 and all large n,
  |Cov(W_j, Wᵀθ* | W_U)| ≥ a  for every j ∈ S₀ and every U ⊆ [p] with j ∉ U, |U| ≤ 15,
with W ~ N_p(0, Σ_n), Σ_n a positive definite correlation matrix, Cov(·, · | W_U) the partial covariance
(`Theory_work/Wave3/W3-READER/NOTATION.md` on main, lines 161-164), s₀ = |S₀| ≥ 1 fixed and θ_lo ≤ |θ*_k| ≤ θ_hi on
S₀ (Theorem 6 (A2)). The dossier B8 (`Theory_work/Wave3/W3-AUDIT/TRACK_B.md:209-233`) and track C
(`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md:63-69`) record which designs are inside; this item proves sufficient
conditions with an explicit uniform constant.

## Notation (one n; the index n is dropped)
- For U ⊆ [p] and j, k ∉ U: Γ^U_{jk} := Σ_{jk} − Σ_{jU}Σ_{UU}⁻¹Σ_{Uk} = Cov(W_j, W_k | W_U); for k ∈ U, Cov(W_j, W_k | W_U) := 0.
- S₀ = {k₁ < … < k_{s₀}}; ϑ := (θ*_{k₁}, …, θ*_{k_{s₀}}) ∈ ℝ^{s₀}; i(j) := the rank of j ∈ S₀.
- **Visibility vector** of (U, j): γ(U, j) ∈ ℝ^{s₀}, γ_i := Γ^U_{j k_i} for k_i ∉ U and γ_i := 0 for k_i ∈ U.
- c₁₆ := min_{|V| ≤ 16} λ_min(Σ_V) (the floor on sets of at most 16 columns).
- 𝒩_n := {γ(U, j)/|γ(U, j)| : j ∈ S₀, U ∌ j, |U| ≤ 15} ⊆ S^{s₀−1} (well defined by (VIS-0)); for a design sequence,
  𝒩 := the closure of ∪_n 𝒩_n, and the **bad set** B := ∪_{ν∈𝒩} ν^⊥ ⊆ ℝ^{s₀}.

## Lemma VIS
- **(VIS-0) Reduction.** Cov(W_j, Wᵀθ* | W_U) = ⟨γ(U, j), ϑ⟩, and γ(U, j)_{i(j)} = Var(W_j | W_U) ≥ λ_min(Σ_{U∪{j}}) ≥ c₁₆.
- **(VIS-a) Sign route (explicit constant).** Suppose there is a diagonal matrix D = diag(d₁, …, d_p), d_l ∈ {−1, +1},
  such that DΣ⁻¹D has nonpositive off-diagonal entries, and the truths are **aligned**: d_k·sgn(θ*_k) = d_j·sgn(θ*_j) for
  every j, k ∈ S₀ in the same connected component of the graph of Σ⁻¹ (the graph with an edge {l, l′} iff (Σ⁻¹)_{ll′} ≠ 0).
  Then for every j ∈ S₀ and U ∌ j: |Cov(W_j, Wᵀθ* | W_U)| ≥ |θ*_j|·Var(W_j | W_U) ≥ θ_lo·c₁₆.
- **(VIS-b) Generic-position route (explicit constant).** For every j ∈ S₀ and U ∌ j with |U| ≤ 15,
  |Cov(W_j, Wᵀθ* | W_U)| ≥ c₁₆ · dist(ϑ, B). B is closed. Hence for a design sequence with **c̲ := inf_n c₁₆(Σ_n) > 0** and
  **δ := inf_n dist(ϑ_n, B) > 0** (for instance ϑ_n in a fixed compact Θ₀ ⊆ ℝ^{s₀} ∖ B), visibility holds for every n
  with the uniform constant **a = c̲·δ**.
- **(VIS-c) The bad set is small when the local patterns are countable.** If 𝒩 is countable, B is a countable union of
  hyperplanes through 0: closed, Lebesgue-null and nowhere dense, so G := ℝ^{s₀} ∖ B is open, dense and of full measure,
  and does not depend on n. If 𝒩 is finite, dist(ϑ, B) = min_{ν∈𝒩} |⟨ν, ϑ⟩|.
- **(VIS-d) Designs with countably many local patterns.** 𝒩 is countable in each of the following cases (Σ_n positive
  definite correlation matrices with c_m := inf_n min_{|V|≤15+s₀} λ_min(Σ_{n,V}) > 0):
  (i) *finitely many local patterns*: the labelled matrices Σ_{n,V}, V = U ∪ S₀ (labels: which indices are U, which is
  j, and the rank of each truth), take finitely many values over all n, j, U — e.g. block-diagonal Σ_n with blocks from
  a fixed finite list of correlation matrices; equicorrelation with a fixed ρ; factor models Σ_n = Ψ + ΛΛᵀ (unit
  diagonal) whose rows (λ_l, ψ_l) take finitely many values;
  (ii) *stationary designs*: Σ_{n,ll′} = r(|l − l′|) for a fixed function r with r(d) → 0 as d → ∞ (e.g. AR(ρ),
  |ρ| < 1, fixed; banded/MA(q)); also block-diagonal designs whose blocks are of this form, with finitely many r's.
- **(VIS-e) Instances of the sign route** (each with D and the floor): independent columns (D = I; c₁₆ = 1); AR(ρ), |ρ| < 1
  (d_l = sgn(ρ)^l; c₁₆ ≥ (1 − |ρ|)/(1 + |ρ|)); equicorrelation ρ ∈ [0, 1) (D = I; c₁₆ ≥ 1 − ρ); one-factor
  Σ = Ψ + λλᵀ with Ψ diagonal positive (d_l = sgn(λ_l), sgn 0 := +1; c₁₆ ≥ min_l ψ_l); block-diagonal combinations of
  these (D blockwise; alignment is required only within a block).

## Reading for the theorems
Under Theorem 6 (A5) (or Theorem 5 (A3)), c₁₆ and c_m are bounded below by the theorem's floor c for large n, so the floor
is not a new assumption there. The new hypothesis is a condition on (Σ_n, ϑ_n) jointly: alignment (VIS-a), or a fixed
distance from the bad set (VIS-b). Either gives (A3) with the stated constant, for every n.

## Not claimed
- Anything when ϑ_n approaches B (dist(ϑ_n, B) → 0) or lies on it: there visibility may fail with no margin; this is the
  case of track C's strong factor with mixed-sign truths (D14, D15: population value 0).
- Designs whose local patterns are uncountable without a countable closure of 𝒩 (e.g. irregular or estimated
  correlation matrices such as track C's riboflavin-like D18): B may then have interior; no claim.
- Sample-level visibility (Theorem 7 (A3); W3-START2-R (D3); W3-RM2-R (V♭)) and the other hypotheses of Theorems 5, 6, 10.
- "Nonzero for almost every β" alone (ϑ ∉ B without a uniform distance) does not give a uniform margin and is not used.

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM | track V V1 | manager 11-17, D112 | `CHECK.md` |
