# S — one-step supersets with the fit factor kept (W3-PSHARP, Lemma S and Lemma V)

Status: **PROVED (by this seat, unchecked)**. Check record: see `../REPORT.md` §2.
Notation: `../STATEMENT.md` §0 (the coded target π of [W3P] §0). Self-contained: nothing is cited beyond the
definition of π.

## Lemma V (variational form of Q; scaling)
For every S ⊆ [p] (any size, S = ∅ included) and every standardised y:
  Q_S = min_{ϑ∈ℝ^S} { ‖y − X_Sϑ‖² + ϑᵀ(G_S + I)ϑ/n } ≥ 0,
and, with Cy^r = s_y y,
  s_y² Q_S = min_{ϑ∈ℝ^S} { ‖Cy^r − X_Sϑ‖² + ϑᵀ(G_S + I)ϑ/n }.
*Proof.* ‖y − X_Sϑ‖² + ϑᵀ(G_S + I)ϑ/n = yᵀy − 2z_Sᵀϑ + ϑᵀ[G_S + (G_S + I)/n]ϑ = yᵀy − 2z_Sᵀϑ + ϑᵀH_Sϑ/n, because
G_S + (G_S + I)/n = ((n + 1)G_S + I)/n = H_S/n. H_S is positive definite, so the minimum is at ϑ = nH_S⁻¹z_S, with
value yᵀy − n z_SᵀH_S⁻¹z_S = Q_S. The objective is a sum of two nonnegative terms, so Q_S ≥ 0. The second display is
the first multiplied by s_y², with ϑ replaced by ϑ/s_y. (S = ∅: Q_∅ = yᵀy.) ∎

## Lemma S
Let n ≥ 3, X a standardised design with p ≥ 2, y a standardised response, S ⊆ [p] with |S| + 1 ≤ K, j ∉ S. Write
G := G_S, H := H_S, A := G + I, g := g_{S,j} = X_Sᵀx_j, s := s_{S,j} = n² − (n + 1)²gᵀH⁻¹g, S⁺ := S ∪ {j}.
(If S = ∅: g is void, s = n², and every quadratic form in g is 0.)

**1. Determinant.** D_{S⁺}/D_S = s/(n − gᵀA⁻¹g); 0 < s ≤ n²; D_{S⁺}/D_S ≤ n, with equality iff x_j ⟂ col X_S; and
D_{S∪J}/D_S ≤ n^{|J|} for every J disjoint from S.

*Proof.* Order the columns as (X_S, x_j). Since ‖x_j‖² = n − 1,
  H_{S⁺} = [[H, (n+1)g], [(n+1)gᵀ, (n+1)(n−1) + 1]] = [[H, (n+1)g], [(n+1)gᵀ, n²]],  G_{S⁺} + I = [[A, g], [gᵀ, n]].
Both matrices are positive definite (G_{S⁺} ⪰ 0), and so are H and A. By the Schur complement formula,
det H_{S⁺} = det H · (n² − (n+1)²gᵀH⁻¹g) = det H · s and det(G_{S⁺} + I) = det A · (n − gᵀA⁻¹g), and both Schur
complements are positive. Hence D_{S⁺}/D_S = s/(n − gᵀA⁻¹g), and 0 < s ≤ n² (H⁻¹ ⪰ 0).
The inequality s ≤ n(n − gᵀA⁻¹g) is equivalent to gᵀ[(n+1)²H⁻¹ − nA⁻¹]g ≥ 0. H and A are functions of G, hence
simultaneously diagonalisable; on an eigenvector of G with eigenvalue λ ≥ 0 the matrix (n+1)²H⁻¹ − nA⁻¹ has eigenvalue
  (n+1)²/((n+1)λ + 1) − n/(λ + 1) = [(n+1)λ + n² + n + 1] / [((n+1)λ + 1)(λ + 1)] > 0
(numerator: (n+1)²(λ+1) − n((n+1)λ + 1) = (n+1)λ + (n+1)² − n). So it is positive definite: the inequality holds,
with equality iff g = 0, i.e. x_j ⟂ col X_S. The last claim follows by adding the columns of J one at a time: the
matrices H_·, G_· + I and the identity above are defined for every subset of [p], whatever its size. ∎

**2. Fit.** With ρ̃_S := y − (n+1)X_SH⁻¹X_Sᵀy:  Q_S − Q_{S⁺} = n (x_jᵀρ̃_S)²/s ≥ (x_jᵀρ̃_S)²/n ≥ 0, and 0 ≤ Q_{S⁺} ≤ Q_S.

*Proof.* For a positive definite block matrix M = [[H, h], [hᵀ, d]] and v = (v₁, v₂),
vᵀM⁻¹v = v₁ᵀH⁻¹v₁ + (v₂ − hᵀH⁻¹v₁)²/(d − hᵀH⁻¹h) (block inversion). With M = H_{S⁺}, h = (n+1)g, d = n², v = (z_S, z_j),
z_j = x_jᵀy: v₂ − hᵀH⁻¹v₁ = x_jᵀy − (n+1)x_jᵀX_SH⁻¹X_Sᵀy = x_jᵀρ̃_S and d − hᵀH⁻¹h = s. Therefore
z_{S⁺}ᵀH_{S⁺}⁻¹z_{S⁺} − z_SᵀH⁻¹z_S = (x_jᵀρ̃_S)²/s, and Q_S − Q_{S⁺} = n(x_jᵀρ̃_S)²/s. The lower bound uses s ≤ n². Q_{S⁺} ≥ 0
by Lemma V. ∎

**3. One model.** Let S = S₀ (so s₀ + 1 ≤ K) and γ_j := (Q_{S₀} − Q_{S₀∪{j}})/(2b₀ + Q_{S₀}). Then γ_j ∈ [0, 1) and
  π(S₀∪{j})/π(S₀) ≥ [(s₀+1)/(2p−1−s₀)] n^{−1/2} (1 − γ_j)^{−ν} ≥ [(s₀+1)/(2p−1−s₀)] n^{−1/2} e^{νγ_j}.

*Proof.* Both models are in Ω, and the normalising constant of π cancels:
  π(S₀∪{j})/π(S₀) = [w(s₀+1)/w(s₀)] · (D_{S₀}/D_{S₀∪{j}})^{1/2} · ((2b₀ + Q_{S₀})/(2b₀ + Q_{S₀∪{j}}))^{ν}.
Prior: w(s₀+1)/w(s₀) = C(2p−1, s₀)/C(2p−1, s₀+1) = (s₀+1)/(2p−1−s₀). Determinant: ≥ n^{−1/2} by item 1.
Fit: (2b₀ + Q_{S₀∪{j}})/(2b₀ + Q_{S₀}) = 1 − γ_j, and 0 ≤ Q_{S₀∪{j}} ≤ Q_{S₀} with b₀ > 0 give 0 ≤ γ_j < 1. Finally
−log(1 − γ) ≥ γ on [0, 1). ∎

**4. Sum.** For every 𝒩 ⊆ [p]∖S₀:  δ_n/(1 − δ_n) ≥ [(s₀+1)/(2p−1−s₀)] n^{−1/2} Σ_{j∈𝒩} e^{νγ_j}.

*Proof.* π(S₀) > 0 (every score is positive and finite), and δ_n/(1 − δ_n) = Σ_{S∈Ω, S≠S₀} π(S)/π(S₀). The models
S₀∪{j}, j ∈ 𝒩, are distinct elements of Ω∖{S₀}; all other terms are ≥ 0. Apply item 3. ∎

## Remarks
1. Item 1 improves the bound D_{S⁺}/D_S ≤ n + 1 used in [LB] line 25 to n, which is attained (orthogonal column).
2. Falsification: `../numerics/b_check.py` F1 → `b_check_out.txt` (8,064 pairs (S, j) on iid, correlated,
   rank-deficient, near-duplicate, orthogonal and binary designs: both identities to 1e-12; max (D_{S⁺}/D_S)/n =
   1.000000000000).
