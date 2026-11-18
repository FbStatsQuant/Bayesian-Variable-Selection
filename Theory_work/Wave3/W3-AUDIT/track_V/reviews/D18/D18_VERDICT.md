# D18 (riboflavin-like) — visibility verdict by the finite computation (lead, 2026-11-17)

**Design.** Track C's D18 (`helpers/W3-AUDIT-C/nots_pkg/scripts/c_designs.py:239-252`, `_real`): Σ₀ = L Lᵀ + 0.1 I, L the
4088 × 70 riboflavin factor matrix (`nots_pkg/data/riboflavin_L.csv`), unit diagonal up to 4.8e-14 (the code's
`sigma_rows` sets the diagonal to exactly 1), λ_min(L Lᵀ + 0.1 I) = 0.1 exactly (rank 70 < 4088), so the code's matrix has
λ_min ≥ 0.1 − 5 × 10⁻¹⁴ (D18C E-1). For p ≤ 4088: a random row subset of Σ₀ (seeded by p); for
p > 4088: block-diagonal tiling, column j ↦ row j mod 4088 of copy ⌊j/4088⌋, zero covariance across copies. Every local
matrix is therefore a labelled principal submatrix of Σ₀ (with cross-copy zeros): **finitely many local patterns**,
case (VIS-d)(i). c₁₆ ≥ 0.1 for every n.
**Placements** (`c_designs.py:38-43, 248-251`): spread = columns 0, p/4, p/2, 3p/4 with θ = (1.4, −1.0, 1.8, −1.2);
clustered = column 0 and its three most correlated partners (rows 0, 214, 660, 295 of copy 0 for every p > 4088) with
θ = (1.4, 1.0, 1.8, 1.2).

**Spread — covered, certified.** For p ≥ 4·4088 = 16352 (n ≥ 1636 on p = 10n) the four truths lie in four different copies;
Σ is block diagonal across copies, so for every j and every U: Cov(W_j, Wᵀθ* | W_U) = θ_j Var(W_j | W_U), hence
|·| ≥ |θ_j| λ_min(Σ_{U∪{j}}) ≥ 1.0 × (0.1 − 5 × 10⁻¹⁴) ≈ **0.1**. In the lemma's terms: over n ≥ 1636 every visibility direction is a
coordinate vector, B = the coordinate hyperplanes, **δ = dist(ϑ, B) = min_k |θ_k| = 1.0**, c̲ ≥ 0.1, **a = c̲·δ ≥ 0.1**
(also B8's corollary "one truth per block"). Track C agrees: population min δ² = 0.1445 at p = 20000.
**Clustered — not certifiable; effectively on B.** The four truths are fixed rows of one copy at every p > 4088.
Greedy masking (as track C) finds a 15-column U with Cov(W_{214}, Wᵀθ* | W_U) = −1.908384 × 10⁻⁷ (Var 0.2004), recomputed
in **exact rational arithmetic** from the (binary) entries of Σ₀: nonzero. The independent check (D18C, randomized greedy
+ swap search, exact recomputation two ways) finds smaller values: Cov(W_0, Wᵀθ* | W_U) = −6.896 × 10⁻⁹ (Var 0.529).
So **the margin is at most 6.9 × 10⁻⁹** and dist(ϑ, B) ≤ 1.3 × 10⁻⁸. The exact minimum over the finitely many patterns (≈ C(4088, 15) ≈ 10⁴³ sets U) cannot
be enumerated, so neither δ > 0 nor δ = 0 can be certified; any certified constant would be < 10⁻⁸: outside in practice.
**Track C's "population ≈ 0", reconciled.** Spread: ≈ 0 for every p < 16352, where two truths share a copy or a
sub-panel (at p = 16000, truths 0 and 4000 share copy 0: track C's greedy gives δ² = 1.416e-3, reproduced here, but the
D18C swap search finds a 15-column U with δ² ≤ 2.1 × 10⁻¹¹, |Cov| ≤ 2.4 × 10⁻⁶); ≥ 0.1 for every p ≥ 16352 by the argument
above (track C's 0.1445 at p = 20000, a search upper bound, is consistent) (D18C S-1). Clustered: δ² = 1.817e-13 at every p ≥ 8000 (the same U; reproduced).
Method: `d18.py` (greedy masking over all 4088 columns, 15 steps, numpy; exact `fractions` recomputation of the Schur
complement at the found U; it uses L Lᵀ + 0.1 I, which differs from the code's unit diagonal by ≤ 4.8e-14 — D18C's exact
diagonal-1 recomputation agrees to about 9 digits); output `d18_output.txt`. **Independent check:** Opus D18C (own code,
R/Python), `D18C_reply_opus.md`: spread CONFIRMED, clustered CONFIRMED (tighter bound), reconciliation CONFIRMED with S-1
applied.
