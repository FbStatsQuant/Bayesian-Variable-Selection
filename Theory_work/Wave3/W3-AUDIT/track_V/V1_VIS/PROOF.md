# V1 · Lemma VIS — PROOF v1

Fix n; Σ = Σ_n is a positive definite p × p correlation matrix, W ~ N_p(0, Σ). For U ⊆ [p] write U^c := [p] ∖ U.

## Two standard facts (proved here)
**F1 (Schur complement).** For U ⊆ [p] with U^c ≠ ∅, the matrix Γ^U := (Γ^U_{jk})_{j,k∈U^c} = Σ_{U^cU^c} − Σ_{U^cU}Σ_{UU}⁻¹Σ_{UU^c}
equals ((Σ⁻¹)_{U^cU^c})⁻¹, and it is positive definite. *Proof.* The block-inverse formula for the positive definite Σ
(partitioned as (U^c, U)) gives (Σ⁻¹)_{U^cU^c} = (Σ_{U^cU^c} − Σ_{U^cU}Σ_{UU}⁻¹Σ_{UU^c})⁻¹; (Σ⁻¹)_{U^cU^c} is a principal
submatrix of the positive definite Σ⁻¹, hence positive definite, and so is its inverse. For Gaussian W, Γ^U is the
conditional covariance of W_{U^c} given W_U; in general it is the partial covariance of `NOTATION.md` §6. ∎
**F2 (Stieltjes matrices).** If M is symmetric positive definite with nonpositive off-diagonal entries, then M⁻¹ ≥ 0
entrywise, and every principal submatrix of M has the same two properties. *Proof.* Let s := max_l M_{ll} > 0 and
P := sI − M. P is symmetric with nonnegative entries (diagonal s − M_{ll} ≥ 0, off-diagonal −M_{ll′} ≥ 0). The eigenvalues
of P are s − λ for λ an eigenvalue of M, all < s because λ > 0. For a symmetric nonnegative matrix the spectral radius
is its largest eigenvalue (Perron–Frobenius), so ρ(P) = s − λ_min(M) < s. Hence M = s(I − P/s) with ρ(P/s) < 1, and
M⁻¹ = s⁻¹Σ_{t≥0}(P/s)^t, a convergent series of entrywise nonnegative matrices. A principal submatrix of M is positive
definite (Cauchy interlacing, or xᵀM_Vx = x̃ᵀMx̃ for x̃ the zero-padding) and has nonpositive off-diagonal entries. ∎

## (VIS-0)
For j ∉ U: Cov(W_j, Wᵀθ* | W_U) = Σ_{k∈[p]} θ*_k Cov(W_j, W_k | W_U) by bilinearity of the partial covariance; the terms
with k ∉ S₀ vanish (θ*_k = 0) and those with k ∈ U vanish (the residual of W_k on W_U is 0). So it equals
Σ_{k∈S₀∖U} θ*_k Γ^U_{jk} = ⟨γ(U, j), ϑ⟩. The i(j)-th entry is Γ^U_{jj} = Var(W_j | W_U) (j ∈ S₀ ∖ U). With V := U ∪ {j},
F1 applied to Σ_V (and the subset U of V) gives Var(W_j | W_U) = 1/((Σ_V⁻¹)_{jj}) ≥ 1/λ_max(Σ_V⁻¹) = λ_min(Σ_V) ≥ c₁₆, since
|V| ≤ 16. (Γ^U_{jk} uses only the entries of Σ indexed by U ∪ {j, k}, so computing it from Σ_V or Σ is the same.) ∎

## (VIS-a)
Let D be as stated and M := DΣ⁻¹D: symmetric positive definite (D² = I) with nonpositive off-diagonal entries. Fix j ∈ S₀,
U ∌ j, and W := U^c. By F1, DΓ^UD restricted to W is (D_{WW})((Σ⁻¹)_{WW})⁻¹(D_{WW}) = ((DΣ⁻¹D)_{WW})⁻¹ = (M_{WW})⁻¹, and by
F2 (M_{WW} is a principal submatrix of M) it is ≥ 0 entrywise: d_j d_k Γ^U_{jk} ≥ 0 for all j, k ∈ W.
*Components.* Permuting [p] so that the connected components of the graph of Σ⁻¹ are consecutive makes Σ⁻¹ block diagonal,
hence Σ block diagonal with the same blocks; then Σ_{jU}Σ_{UU}⁻¹Σ_{Uk} = 0 and Σ_{jk} = 0 for j, k in different components
(Σ_{UU} is block diagonal too), so Γ^U_{jk} = 0 for such j, k. Let C(j) be j's component.
*Bound.* Let σ := d_j sgn(θ*_j). For k ∈ S₀ ∩ C(j), alignment gives d_k sgn(θ*_k) = σ, i.e. θ*_k = σ d_k |θ*_k|. Then
Cov(W_j, Wᵀθ* | W_U) = Σ_{k∈S₀∩C(j)∖U} θ*_k Γ^U_{jk} = σ d_j Σ_{k∈S₀∩C(j)∖U} |θ*_k| (d_j d_k Γ^U_{jk}),
a sign σd_j times a sum of nonnegative terms, one of which (k = j) is |θ*_j| Γ^U_{jj}. So
|Cov(W_j, Wᵀθ* | W_U)| ≥ |θ*_j| Var(W_j | W_U) ≥ θ_lo c₁₆ by (VIS-0). ∎

## (VIS-b)
*B is closed.* 𝒩 is a closed subset of the unit sphere, hence compact. Let θ_m ∈ B, θ_m → θ; choose ν_m ∈ 𝒩 with
⟨ν_m, θ_m⟩ = 0; a subsequence ν_m → ν ∈ 𝒩, and ⟨ν, θ⟩ = lim ⟨ν_m, θ_m⟩ = 0, so θ ∈ B.
*Bound.* Fix n, j, U and let γ := γ(U, j). By (VIS-0) γ ≠ 0; ν := γ/|γ| ∈ 𝒩_n ⊆ 𝒩, so ν^⊥ ⊆ B and
|⟨ν, ϑ⟩| = dist(ϑ, ν^⊥) ≥ dist(ϑ, B). Hence |Cov(W_j, Wᵀθ* | W_U)| = |γ|·|⟨ν, ϑ⟩| ≥ |γ_{i(j)}|·dist(ϑ, B) ≥ c₁₆·dist(ϑ, B).
*Uniform constant.* For the sequence: |Cov(W_j, Wᵀθ*_n | W_U)| ≥ c₁₆(Σ_n)·dist(ϑ_n, B) ≥ c̲·δ for every n, j, U. If
ϑ_n ∈ Θ₀ compact with Θ₀ ∩ B = ∅, then δ ≥ dist(Θ₀, B) > 0 (a positive distance between a compact and a disjoint closed
set). ∎

## (VIS-c)
If 𝒩 = {ν₁, ν₂, …} is countable, B = ∪_t ν_t^⊥, a countable union of hyperplanes (each a Lebesgue-null set), so B is
null; B is closed by (VIS-b); a closed null set has empty interior (a nonempty open set has positive measure), so it is
nowhere dense; G = ℝ^{s₀} ∖ B is open, dense and of full measure. B is defined from the whole sequence, so G does not
depend on n. If 𝒩 is finite, dist(ϑ, B) = min_t dist(ϑ, ν_t^⊥) = min_t |⟨ν_t, ϑ⟩|. ∎

## (VIS-d)
*γ is local.* By (VIS-0), γ(U, j) is a function of the labelled local matrix L(U, j) := (Σ_V; the labels of U, of j and the
ranks of the truths), V := U ∪ S₀, |V| ≤ 15 + s₀: each Γ^U_{jk_i} is computed from Σ_{U∪{j,k_i}}. On the set ℳ of labelled
positive definite matrices of size ≤ 15 + s₀ with λ_min ≥ c_m > 0, the map L ↦ γ is continuous (Σ_{UU}⁻¹ is continuous
where λ_min(Σ_{UU}) ≥ c_m), and γ ≠ 0 with |γ| ≥ c_m (the i(j) entry ≥ λ_min of the (|U|+1)-submatrix ≥ c_m), so
L ↦ γ/|γ| is continuous on ℳ, and ℳ is closed (λ_min is continuous). Hence if the set ℒ of all L(U, j) (over n, j, U)
has a countable closure ℒ̄ (always ℒ̄ ⊆ ℳ, since ℒ ⊆ ℳ and ℳ is closed), then 𝒩 ⊆ {γ/|γ| : L ∈ ℒ̄}, which is countable:
ℒ̄ is compact (closed, bounded — correlation entries in [−1, 1] — with finitely many label patterns), so the continuous
image of ℒ̄ is compact and contains the image ∪_n 𝒩_n of ℒ, hence contains its closure 𝒩.
(i) If ℒ is finite, ℒ̄ = ℒ. Block-diagonal Σ_n with blocks from a finite list {R₁, …, R_q} (sizes ≤ b): an entry
Σ_{ll′} is 0 across blocks and (R_t)_{ab} within a block of type t at positions a, b; so L is determined by the types,
the within-block positions and the block-sharing pattern of the ≤ 15 + s₀ indices — finitely many choices. Equicorrelation
ρ: Σ_V = (1 − ρ)I + ρJ, determined by |V| and the labels. Factor models with finitely many row types (λ_l, ψ_l):
Σ_{ll′} = λ_lᵀλ_{l′} (l ≠ l′), 1 on the diagonal — determined by the types of the indices. The floor c_m is λ_min of the
whole Σ_n or better (Cauchy interlacing), e.g. min_t λ_min(R_t) for blocks.
(ii) Stationary: sort V = {v₁ < … < v_m}; L is determined by the labels and the gaps g_t := v_{t+1} − v_t ∈ ℕ_{≥1}
(Σ_{v_av_b} = r(g_a + … + g_{b−1})). On the one-point compactification ℕ̄ = ℕ ∪ {∞} with r(∞) := 0 and sums involving
∞ equal to ∞, the map (g, labels) ↦ Σ_V is continuous exactly because r(d) → 0; the domain (ℕ̄)^{m−1} × (labels) is
countable and compact, so its image is a countable compact set containing ℒ, hence containing ℒ̄; and ℒ̄ ⊆ ℳ because
ℒ ⊆ ℳ and ℳ is closed. Hence ℒ̄ is countable. For block-diagonal designs with stationary blocks from finitely many r's,
add the (finite) block-sharing pattern and types to the labels. AR(ρ): r(d) = ρ^d; banded/MA(q): r(d) = 0 for d > q. ∎

## (VIS-e)
Independent columns: Σ⁻¹ = I. AR(ρ): Σ⁻¹ is tridiagonal with off-diagonal entries −ρ/(1 − ρ²); with d_l = s^l,
s := sgn ρ (s := 1 if ρ = 0), (DΣ⁻¹D)_{l,l+1} = −ρ s/(1 − ρ²) = −|ρ|/(1 − ρ²) ≤ 0; λ_min(Σ_V) ≥ λ_min(Σ) ≥ min_ω f(ω) =
(1 − |ρ|)/(1 + |ρ|), f(ω) = (1 − ρ²)/(1 − 2ρ cos ω + ρ²) the spectral density (Toeplitz eigenvalues lie in [min f, max f];
interlacing). Equicorrelation ρ ∈ [0, 1): Σ⁻¹ = (1 − ρ)⁻¹(I − ρ(1 + (p − 1)ρ)⁻¹J), off-diagonal ≤ 0; eigenvalues of Σ are
1 − ρ and 1 + (p − 1)ρ. One factor: Σ⁻¹ = Ψ⁻¹ − Ψ⁻¹λλᵀΨ⁻¹/(1 + λᵀΨ⁻¹λ) (Sherman–Morrison), off-diagonal
−λ_lλ_{l′}/(ψ_lψ_{l′}(1 + λᵀΨ⁻¹λ)); with d_l = sgn λ_l these become −|λ_l||λ_{l′}|/(…) ≤ 0; Σ ⪰ Ψ gives λ_min ≥ min ψ_l.
Block-diagonal: Σ⁻¹ is block diagonal, D blockwise, and the components of the graph of Σ⁻¹ lie inside blocks, so the
alignment of (VIS-a) is required only within a block. ∎

## Remarks
- (VIS-a) is the case of (VIS-b) in which the aligned orthant misses B; it gives the larger, simpler constant θ_lo c₁₆.
  Track C's aligned designs (IND, AR(0.5), blocks, cs, aligned factors; `Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md:63-68`)
  and B8's cs/fac-aligned/s5 cases are instances or (s5, fac2) have their own M-matrix/explicit computations in B8
  (`Theory_work/Wave3/W3-AUDIT/TRACK_B.md:222-228`).
- Illustration of B (AR(ρ), two truths at distance g, U = ∅, j = k₁): γ = (1, ρ^g), so B ⊇ {θ₁ + ρ^gθ₂ = 0}, g ≥ 1; these
  hyperplanes accumulate at {θ₁ = 0}, which |θ*_k| ≥ θ_lo keeps at distance; a fixed mixed-sign ϑ is visible with a
  uniform margin unless it lies on one of the (countably many) hyperplanes of B.
- Mixed-sign pervasive factors (track C D14, D15: population visibility 0) have ϑ on B: consistent with "Not claimed".
