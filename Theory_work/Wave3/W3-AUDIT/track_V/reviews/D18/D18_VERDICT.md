# D18 (riboflavin-like) — visibility verdict by the finite computation (lead, 2026-11-17)

**Design.** Track C's D18 (`helpers/W3-AUDIT-C/nots_pkg/scripts/c_designs.py:239-252`, `_real`): Σ₀ = L Lᵀ + 0.1 I, L the
4088 × 70 riboflavin factor matrix (`nots_pkg/data/riboflavin_L.csv`), unit diagonal (max |diag − 1| = 4.8e-14),
λ_min(Σ₀) = 0.1 exactly (L Lᵀ ⪰ 0 has rank 70 < 4088). For p ≤ 4088: a random row subset of Σ₀ (seeded by p); for
p > 4088: block-diagonal tiling, column j ↦ row j mod 4088 of copy ⌊j/4088⌋, zero covariance across copies. Every local
matrix is therefore a labelled principal submatrix of Σ₀ (with cross-copy zeros): **finitely many local patterns**,
case (VIS-d)(i). c₁₆ ≥ 0.1 for every n.
**Placements** (`c_designs.py:38-43, 248-251`): spread = columns 0, p/4, p/2, 3p/4 with θ = (1.4, −1.0, 1.8, −1.2);
clustered = column 0 and its three most correlated partners (rows 0, 214, 660, 295 of copy 0 for every p > 4088) with
θ = (1.4, 1.0, 1.8, 1.2).

**Spread — covered, certified.** For p ≥ 4·4088 = 16352 (n ≥ 1636 on p = 10n) the four truths lie in four different copies;
Σ is block diagonal across copies, so for every j and every U: Cov(W_j, Wᵀθ* | W_U) = θ_j Var(W_j | W_U), hence
|·| ≥ |θ_j| λ_min(Σ_{U∪{j}}) ≥ 1.0 × 0.1 = **0.1**. In the lemma's terms: over n ≥ 1636 every visibility direction is a
coordinate vector, B = the coordinate hyperplanes, **δ = dist(ϑ, B) = min_k |θ_k| = 1.0**, c̲ ≥ 0.1, **a = c̲·δ ≥ 0.1**
(also B8's corollary "one truth per block"). Track C agrees: population min δ² = 0.1445 at p = 20000.
**Clustered — not certifiable; effectively on B.** The four truths are fixed rows of one copy at every p > 4088.
Greedy masking (as track C) finds a 15-column U with Cov(W_{214}, Wᵀθ* | W_U) = −1.908384 × 10⁻⁷ (Var 0.2004), recomputed
in **exact rational arithmetic** from the (binary) entries of Σ₀: nonzero. So dist(ϑ, B) ≤ 1.9e-7/0.2004 ≈ 9.5 × 10⁻⁷ and
the margin is at most 1.9 × 10⁻⁷. The exact minimum over the finitely many patterns (≈ C(4088, 15) ≈ 10⁴³ sets U) cannot
be enumerated, so neither δ > 0 nor δ = 0 can be certified; any certified constant would be < 10⁻⁶: outside in practice.
**Track C's "population ≈ 0", reconciled.** Spread: ≈ 0 only for p ≤ 8000 (truths share a copy or a sub-panel), 1.416e-3 at
p = 16000 (truths 0 and 4000 share copy 0; reproduced here: δ² = 1.416e-3 at a 15-column U), 0.1445 at p = 20000 and for
every p ≥ 16352 (≥ 0.1 by the argument above). Clustered: δ² = 1.817e-13 at every p ≥ 8000 (the same U; reproduced).
Method: `d18.py` (greedy masking over all 4088 columns, 15 steps, numpy; exact `fractions` recomputation of the Schur
complement at the found U); output `d18_output.txt`.
