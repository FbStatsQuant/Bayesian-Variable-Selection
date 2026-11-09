# Q2 (part): FAC-XA visibility constant c₀ for the family-X one-factor designs

Script `X/scripts/x_visibility.py` (local, deterministic; output `Q2_visibility_c0.json`). Population computation, no
simulation. FAC-XA STATEMENT v1 (locked research target): c(U, j) = Cov(x_j, μ | x_U), μ = Σ_{i∈S₀} θ_i x_i,
c₀ = inf_n min |c(U, j)| over |U| ≤ 15, j ∉ U, (j ∈ S₀ or U ⊉ S₀).

Closed form for one factor (Woodbury; checked against direct linear algebra on 900 random (U, j), max abs error 5.2e-16):
with ℓ_i² = λ_i²/(1 − λ_i²), Q_U = Σ_{U} ℓ_i², V = U ∩ S₀, a_V = Σ_V λ_iθ_i, m = Σ_{S₀} λ_iθ_i:
* null j: c(U, j) = λ_j (m − a_V)/(1 + Q_U);
* truth j ∉ U: c(U, j) = ψ_jθ_j + λ_j (m − a_V)/(1 + Q_U).
c depends on U only through (V, Q_U). Finite loading classes: all attainable Q_U enumerated exactly. Continuous loadings:
attainable Q_U treated as the interval [Q_V, Q_V + (sum of the 15 − |V| largest null ℓ²)] (dense as p → ∞); c₀ = 0
reported when c changes sign on it (then attainable values approach 0 as p grows).

Truths at linspace(2, p − 3, 4), θ = (1.4, −1.0, 1.8, −1.2) ("std") or (−1.0, 1.4, −1.2, 1.8) ("rev").

| design | θ | c₀ (p = 500 / 2000 / 5000) | minimiser |
|---|---|---|---|
| CS ρ = 0.3 | std, rev | 0.0081 (all p) | null j, V = two truths, Q = 15ℓ² |
| CS ρ = 0.5 | std, rev | **0 (2.2e-16)** | truth θ = −1.0, U = ∅: ψθ_j + λ²Σθ = −0.5 + 0.5·1.0 = 0 |
| CS ρ = 0.7 | std, rev | 0.0039 (all p) | null j, V = two truths |
| two-class 0.3/0.9 | std / rev | 2.8e-4 / 1.5e-3 | null j (λ = 0.3), large Q |
| two-class 0.5/0.95 | std / rev | 1.9e-4 / 8.2e-4 | null j (λ = 0.5), large Q |
| U[0.2, 0.9] | std | **0** (sign change, all p) | truth j, Q in the attainable interval |
| U[0.2, 0.9] | rev | 0 / 7.2e-4 / 0 | truth (p 500, 5000) / null (p 2000) |

Reading (evidence about the hypothesis, not about the method): (i) XA's visibility V holds with small but n-free c₀ for
CS ρ ∈ {0.3, 0.7} and the two-class designs; (ii) it fails exactly for CS ρ = 0.5 with these coefficients — the same
cancellation makes FAC-X's (FS)(b) fail (V = S₀, l = the −1.0 truth, u = 0: −1 + ρ·1.0/(1 − ρ) = 0 at ρ = 0.5), so
ρ = 0.5 with mixed signs is a degenerate (FS-failing) design and is not used in items A/C of family X; (iii) for
continuous loadings c(U, j) for a truth j changes sign over the attainable conditioning sets, so V fails generically
(c₀ → 0 as p grows) — V is a restrictive hypothesis for C2 with continuous loadings, while the item-B simulations test
the method on exactly such designs.
