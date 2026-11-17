# AUDITV — V1 (visibility with a margin uniform in n)

Material for a blind review. Every excerpt is verbatim with its file and line numbers (the theorems and notation at commit 029bb748, the other texts at commit 7df2d81c). Status labels have been replaced by [status omitted].

## 1. V1 statement
`Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/STATEMENT.md` @ 7df2d81c, lines 1–76:
```
    1| # V1 · Lemma VIS (visibility with a margin uniform in n: a sign route and a generic-position route) — STATEMENT v1.4 (draft; [status omitted] [status omitted] WITH CHANGES on v1.1, changes applied)
    2| 
    3| Track V item V1 (manager 11-17, D112; owner + consultant requirement: a margin **uniform in n**, not "nonzero for almost
    4| every β"). Tier B (new lemma; pure linear algebra and topology, no code). **Lean target: yes** (finite-dimensional:
    5| Schur complements, Stieltjes matrices, closed sets of hyperplanes; every statement is for one fixed n plus a uniform
    6| bound).
    7| 
    8| ## Target condition
    9| The population visibility condition — Theorem 5 (A4) (lines 581-582), Theorem 6 (A3) (lines 672-673) and Theorem 10 (A4)
   10| (line 1292, "(A4) of Theorem 5") of `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` on main 029bb748: for a fixed a > 0
   11| and n ≥ n₀ (the theorems state the hypothesis with a fixed a; they are asymptotic, so n ≥ n₀ suffices),
   12|   |Cov(W_j, Wᵀθ* | W_U)| ≥ a  for every j ∈ S₀ and every U ⊆ [p] with j ∉ U, |U| ≤ 15,
   13| with W ~ N_p(0, Σ_n), Σ_n a correlation matrix (positive definite in Theorem 6; Theorems 5 and 10 assume only a
   14| correlation matrix with a small-set floor), Cov(·, · | W_U) the partial covariance
   15| (`Theory_work/Wave3/W3-READER/NOTATION.md` on main, lines 161-164), s₀ = |S₀| ≥ 1 fixed and θ_lo ≤ |θ*_k| ≤ θ_hi on
   16| S₀ (Theorem 6 (A2)). The dossier B8 (`Theory_work/Wave3/W3-AUDIT/TRACK_B.md:209-233`) and track C
   17| (`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md:63-69`) record which designs are inside; this item proves sufficient
   18| conditions with an explicit uniform constant.
   19| 
   20| ## Notation (one n; the index n is dropped)
   21| Σ is a p × p correlation matrix with c₁₆ > 0 (below); it need not be invertible except in (VIS-a).
   22| - For U ⊆ [p] and j, k ∉ U: Γ^U_{jk} := Σ_{jk} − Σ_{jU}Σ_{UU}⁻¹Σ_{Uk} = Cov(W_j, W_k | W_U); for k ∈ U, Cov(W_j, W_k | W_U) := 0.
   23| - S₀ = {k₁ < … < k_{s₀}}; ϑ := (θ*_{k₁}, …, θ*_{k_{s₀}}) ∈ ℝ^{s₀}; i(j) := the rank of j ∈ S₀.
   24| - **Visibility vector** of (U, j): γ(U, j) ∈ ℝ^{s₀}, γ_i := Γ^U_{j k_i} for k_i ∉ U and γ_i := 0 for k_i ∈ U.
   25| - c₁₆ := min_{|V| ≤ 16} λ_min(Σ_V) (the floor on sets of at most 16 columns).
   26| - 𝒩_n := {γ(U, j)/|γ(U, j)| : j ∈ S₀, U ∌ j, |U| ≤ 15} ⊆ S^{s₀−1} (well defined by (VIS-0)); for a design sequence,
   27|   𝒩 := the closure of ∪_{n≥n₀} 𝒩_n, and the **bad set** B := ∪_{ν∈𝒩} ν^⊥ ⊆ ℝ^{s₀} (n₀ as in (VIS-b)).
   28| 
   29| ## Lemma VIS
   30| - **(VIS-0) Reduction.** For j ∈ S₀ and U ∌ j with |U| ≤ 15: Cov(W_j, Wᵀθ* | W_U) = ⟨γ(U, j), ϑ⟩, and
   31|   γ(U, j)_{i(j)} = Var(W_j | W_U) ≥ λ_min(Σ_{U∪{j}}) ≥ c₁₆.
   32| - **(VIS-a) Sign route (explicit constant).** Suppose Σ is positive definite and there is a diagonal matrix D = diag(d₁, …, d_p), d_l ∈ {−1, +1},
   33|   such that DΣ⁻¹D has nonpositive off-diagonal entries, and the truths are **aligned**: d_k·sgn(θ*_k) = d_j·sgn(θ*_j) for
   34|   every j, k ∈ S₀ in the same connected component of the graph of Σ⁻¹ (the graph with an edge {l, l′} iff (Σ⁻¹)_{ll′} ≠ 0).
   35|   Then for every j ∈ S₀ and U ∌ j: |Cov(W_j, Wᵀθ* | W_U)| ≥ |θ*_j|·Var(W_j | W_U), and this is ≥ θ_lo·c₁₆ when |U| ≤ 15.
   36| - **(VIS-b) Generic-position route (explicit constant).** For every n ≥ n₀, every j ∈ S₀ and U ∌ j with |U| ≤ 15,
   37|   |Cov(W_j, Wᵀθ* | W_U)| ≥ c₁₆ · dist(ϑ, B). B is closed, so for a fixed ϑ, ϑ ∉ B ⇔ dist(ϑ, B) > 0, and
   38|   dist(ϑ, B) = min_{ν∈𝒩} |⟨ν, ϑ⟩| (attained: 𝒩 is compact). Hence for a design sequence with
   39|   **c̲ := inf_{n≥n₀} c₁₆(Σ_n) > 0** and **δ := inf_{n≥n₀} dist(ϑ_n, B) > 0** (for instance ϑ_n in a fixed compact
   40|   Θ₀ ⊆ ℝ^{s₀} ∖ B, or ϑ_n = ϑ fixed with ϑ ∉ B), visibility holds for every n ≥ n₀ with the uniform constant **a = c̲·δ**.
   41| - **(VIS-c) The bad set is small when the local patterns are countable.** If 𝒩 is countable, B is a countable union of
   42|   hyperplanes through 0: closed, Lebesgue-null and nowhere dense, so G := ℝ^{s₀} ∖ B is open, dense and of full measure,
   43|   and does not depend on n. If 𝒩 is finite, the minimum in (VIS-b) is over finitely many ν and is computable.
   44| - **(VIS-d) Designs with countably many local patterns.** 𝒩 is countable in each of the following cases (Σ_n correlation
   45|   matrices with c_m := inf_{n≥n₀} min_{|V|≤15+s₀} λ_min(Σ_{n,V}) > 0; 𝒩 formed over n ≥ n₀):
   46|   (i) *finitely many local patterns*: the labelled matrices Σ_{n,V}, V = U ∪ S₀ (labels: which indices are U, which is
   47|   j, and the rank of each truth), take finitely many values over all n, j, U — e.g. block-diagonal Σ_n with blocks from
   48|   a fixed finite list of correlation matrices; block designs with equicorrelated blocks of a fixed ρ_b ∈ [0, 1) and any sizes
   49|   (also growing), the entries depending only on block sharing; equicorrelation with a fixed ρ (ρ ∈ [0, 1) when p → ∞, for
   50|   positive definiteness); factor models Σ_n = Ψ + ΛΛᵀ (unit
   51|   diagonal) whose rows (λ_l, ψ_l) take finitely many values;
   52|   (ii) *stationary designs*: Σ_{n,ll′} = r(|l − l′|) for a fixed function r with r(d) → 0 as d → ∞ (e.g. AR(ρ),
   53|   |ρ| < 1, fixed; banded/MA(q)); also block-diagonal designs whose blocks are of this form, with finitely many r's.
   54| - **(VIS-e) Instances of the sign route** (each with D and the floor): independent columns (D = I; c₁₆ = 1); AR(ρ), |ρ| < 1
   55|   (d_l = s^l with s := sgn ρ, s := +1 if ρ = 0; alignment: s^k·sgn(θ*_k) is the same for every k ∈ S₀ — for ρ > 0 equal
   56|   signs, for ρ < 0 sgn(θ*_k) = σ·(−1)^k for a common σ, i.e. the sign is fixed by the parity of k; c₁₆ ≥ (1 − |ρ|)/(1 + |ρ|)); equicorrelation ρ ∈ [0, 1) (D = I; c₁₆ ≥ 1 − ρ); one-factor
   57|   Σ = Ψ + λλᵀ with Ψ diagonal positive (d_l = sgn(λ_l), sgn 0 := +1; c₁₆ ≥ min_l ψ_l); block-diagonal combinations of
   58|   these (D blockwise; alignment is required only within a block).
   59| 
   60| ## Reading for the theorems
   61| The floors are not new assumptions: Theorem 5 (A3) (|S| ≤ 16 + s₀) gives c₁₆, c_m ≥ c for every n; Theorem 6 (A5) and
   62| Theorem 10 (A3) (|S| ≤ 5(A + 1)(s₀ + 1) log n) give them for n ≥ n₀ with 5(A + 1)(s₀ + 1) log n₀ ≥ 16 + s₀. The new
   63| hypothesis is a condition on (Σ_n, ϑ_n) jointly: alignment (VIS-a; Σ_n positive definite, as in Theorem 6), or a fixed
   64| distance from the bad set (VIS-b). Either gives Theorem 6 (A3) and Theorems 5, 10 (A4) with the stated constant, for every
   65| n ≥ n₀.
   66| 
   67| ## Not claimed
   68| - Anything when ϑ_n approaches B (dist(ϑ_n, B) → 0) or lies on it: there visibility may fail with no margin; this is the
   69|   case of track C's strong factor with mixed-sign truths (D14, D15: population value 0).
   70| - Designs whose local patterns are uncountable without a countable closure of 𝒩 (e.g. irregular or estimated
   71|   correlation matrices such as track C's riboflavin-like D18): B may then have interior; no claim.
   72| - Sample-level visibility (Theorem 7 (A3); W3-START2-R (D3); W3-RM2-R (V♭)) and the other hypotheses of Theorems 5, 6, 10.
   73| - Avoiding, for each n separately, only that n's hyperplanes (ϑ_n ∉ ∪_{ν∈𝒩_n} ν^⊥, "nonzero for almost every β" at each n)
   74|   is not enough and is not used: ϑ may then lie on a limit hyperplane ν^⊥, ν ∈ 𝒩 ∖ ∪_n 𝒩_n, where the margin tends to 0.
   75|   B includes those limit hyperplanes.
   76| 
```

## 2. V1 proof
`Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/PROOF.md` @ 7df2d81c, lines 1–113:
```
    1| # V1 · Lemma VIS — PROOF v1.4
    2| 
    3| Fix n; Σ = Σ_n is a p × p correlation matrix with c₁₆ > 0 (positive definite in (VIS-a)), W ~ N_p(0, Σ). For U ⊆ [p]
    4| write U^c := [p] ∖ U. F1 is applied to positive definite matrices only: to Σ in (VIS-a), and to Σ_V with |V| ≤ 16
    5| (positive definite by c₁₆ > 0) elsewhere.
    6| 
    7| ## Two standard facts ([status omitted] here)
    8| **F1 (Schur complement).** For U ⊆ [p] with U^c ≠ ∅, the matrix Γ^U := (Γ^U_{jk})_{j,k∈U^c} = Σ_{U^cU^c} − Σ_{U^cU}Σ_{UU}⁻¹Σ_{UU^c}
    9| equals ((Σ⁻¹)_{U^cU^c})⁻¹, and it is positive definite. *Proof.* The block-inverse formula for the positive definite Σ
   10| (partitioned as (U^c, U)) gives (Σ⁻¹)_{U^cU^c} = (Σ_{U^cU^c} − Σ_{U^cU}Σ_{UU}⁻¹Σ_{UU^c})⁻¹; (Σ⁻¹)_{U^cU^c} is a principal
   11| submatrix of the positive definite Σ⁻¹, hence positive definite, and so is its inverse. For Gaussian W, Γ^U is the
   12| conditional covariance of W_{U^c} given W_U; in general it is the partial covariance of `NOTATION.md` §6. ∎
   13| **F2 (Stieltjes matrices).** If M is symmetric positive definite with nonpositive off-diagonal entries, then M⁻¹ ≥ 0
   14| entrywise, and every principal submatrix of M has the same two properties. *Proof.* Let s := max_l M_{ll} > 0 and
   15| P := sI − M. P is symmetric with nonnegative entries (diagonal s − M_{ll} ≥ 0, off-diagonal −M_{ll′} ≥ 0). The eigenvalues
   16| of P are s − λ for λ an eigenvalue of M, all < s because λ > 0. For a symmetric nonnegative matrix the spectral radius
   17| is its largest eigenvalue (Perron–Frobenius), so ρ(P) = s − λ_min(M) < s. Hence M = s(I − P/s) with ρ(P/s) < 1, and
   18| M⁻¹ = s⁻¹Σ_{t≥0}(P/s)^t, a convergent series of entrywise nonnegative matrices. A principal submatrix of M is positive
   19| definite (Cauchy interlacing, or xᵀM_Vx = x̃ᵀMx̃ for x̃ the zero-padding) and has nonpositive off-diagonal entries. ∎
   20| 
   21| ## (VIS-0)
   22| For j ∉ U: Cov(W_j, Wᵀθ* | W_U) = Σ_{k∈[p]} θ*_k Cov(W_j, W_k | W_U) by bilinearity of the partial covariance; the terms
   23| with k ∉ S₀ vanish (θ*_k = 0) and those with k ∈ U vanish (the residual of W_k on W_U is 0). So it equals
   24| Σ_{k∈S₀∖U} θ*_k Γ^U_{jk} = ⟨γ(U, j), ϑ⟩. The i(j)-th entry is Γ^U_{jj} = Var(W_j | W_U) (j ∈ S₀ ∖ U). With V := U ∪ {j},
   25| F1 applied to Σ_V (and the subset U of V) gives Var(W_j | W_U) = 1/((Σ_V⁻¹)_{jj}) ≥ 1/λ_max(Σ_V⁻¹) = λ_min(Σ_V) ≥ c₁₆, since
   26| |V| ≤ 16. (Γ^U_{jj} uses only the entries of Σ indexed by V, so computing it from Σ_V or Σ is the same; a general entry
   27| Γ^U_{jk} uses the entries indexed by U ∪ {j, k}.) ∎
   28| 
   29| ## (VIS-a)
   30| Let D be as stated and M := DΣ⁻¹D: symmetric positive definite (D² = I) with nonpositive off-diagonal entries. Fix j ∈ S₀,
   31| U ∌ j, and R := U^c (any |U|). By F1, DΓ^UD restricted to R is (D_{RR})((Σ⁻¹)_{RR})⁻¹(D_{RR}) = ((DΣ⁻¹D)_{RR})⁻¹ = (M_{RR})⁻¹, and by
   32| F2 (M_{RR} is a principal submatrix of M) it is ≥ 0 entrywise: d_j d_k Γ^U_{jk} ≥ 0 for all j, k ∈ R.
   33| *Components.* Permuting [p] so that the connected components of the graph of Σ⁻¹ are consecutive makes Σ⁻¹ block diagonal,
   34| hence Σ block diagonal with the same blocks; then Σ_{jU}Σ_{UU}⁻¹Σ_{Uk} = 0 and Σ_{jk} = 0 for j, k in different components
   35| (Σ_{UU} is block diagonal too), so Γ^U_{jk} = 0 for such j, k. Let C(j) be j's component.
   36| *Bound.* Let σ := d_j sgn(θ*_j). For k ∈ S₀ ∩ C(j), alignment gives d_k sgn(θ*_k) = σ, i.e. θ*_k = σ d_k |θ*_k|. Then
   37| Cov(W_j, Wᵀθ* | W_U) = Σ_{k∈S₀∩C(j)∖U} θ*_k Γ^U_{jk} = σ d_j Σ_{k∈S₀∩C(j)∖U} |θ*_k| (d_j d_k Γ^U_{jk}),
   38| a sign σd_j times a sum of nonnegative terms, one of which (k = j) is |θ*_j| Γ^U_{jj}. So
   39| |Cov(W_j, Wᵀθ* | W_U)| ≥ |θ*_j| Var(W_j | W_U), which is ≥ θ_lo c₁₆ by (VIS-0) when |U| ≤ 15. ∎
   40| 
   41| ## (VIS-b)
   42| *B is closed.* 𝒩 is a closed subset of the unit sphere, hence compact. Let θ_m ∈ B, θ_m → θ; choose ν_m ∈ 𝒩 with
   43| ⟨ν_m, θ_m⟩ = 0; a subsequence ν_m → ν ∈ 𝒩, and ⟨ν, θ⟩ = lim ⟨ν_m, θ_m⟩ = 0, so θ ∈ B.
   44| *Bound.* Fix n ≥ n₀, j, U and let γ := γ(U, j). By (VIS-0) γ ≠ 0; ν := γ/|γ| ∈ 𝒩_n ⊆ 𝒩, so ν^⊥ ⊆ B and
   45| |⟨ν, ϑ⟩| = dist(ϑ, ν^⊥) ≥ dist(ϑ, B). Hence |Cov(W_j, Wᵀθ* | W_U)| = |γ|·|⟨ν, ϑ⟩| ≥ |γ_{i(j)}|·dist(ϑ, B) ≥ c₁₆·dist(ϑ, B).
   46| *Minimum attained.* ν ↦ |⟨ν, ϑ⟩| is continuous on the compact 𝒩, and dist(ϑ, B) = inf_{ν∈𝒩} dist(ϑ, ν^⊥) =
   47| inf_{ν∈𝒩} |⟨ν, ϑ⟩| (B = ∪_{ν∈𝒩} ν^⊥), so the infimum is a minimum; as B is closed, dist(ϑ, B) > 0 iff ϑ ∉ B.
   48| *Uniform constant.* For the sequence (n ≥ n₀): |Cov(W_j, Wᵀθ*_n | W_U)| ≥ c₁₆(Σ_n)·dist(ϑ_n, B) ≥ c̲·δ for every n, j, U. If
   49| ϑ_n ∈ Θ₀ compact with Θ₀ ∩ B = ∅, then δ ≥ dist(Θ₀, B) > 0 (a positive distance between a compact and a disjoint closed
   50| set). ∎
   51| 
   52| ## (VIS-c)
   53| If 𝒩 = {ν₁, ν₂, …} is countable, B = ∪_t ν_t^⊥, a countable union of hyperplanes (each a Lebesgue-null set), so B is
   54| null; B is closed by (VIS-b); a closed null set has empty interior (a nonempty open set has positive measure), so it is
   55| nowhere dense; G = ℝ^{s₀} ∖ B is open, dense and of full measure. B is defined from the whole sequence, so G does not
   56| depend on n. If 𝒩 is finite, dist(ϑ, B) = min_t dist(ϑ, ν_t^⊥) = min_t |⟨ν_t, ϑ⟩|. ∎
   57| 
   58| ## (VIS-d)
   59| *γ is local.* By (VIS-0), γ(U, j) is a function of the labelled local matrix L(U, j) := (Σ_V; the labels of U, of j and the
   60| ranks of the truths), V := U ∪ S₀, |V| ≤ 15 + s₀: each Γ^U_{jk_i} is computed from Σ_{U∪{j,k_i}}. On the set ℳ of labelled
   61| positive definite matrices of size ≤ 15 + s₀ with λ_min ≥ c_m > 0, the map L ↦ γ is continuous (Σ_{UU}⁻¹ is continuous
   62| where λ_min(Σ_{UU}) ≥ c_m), and γ ≠ 0 with |γ| ≥ c_m (the i(j) entry ≥ λ_min of the (|U|+1)-submatrix ≥ c_m), so
   63| L ↦ γ/|γ| is continuous on ℳ, and ℳ is closed (λ_min is continuous). Hence if the set ℒ of all L(U, j) (over n, j, U)
   64| has a countable closure ℒ̄ (always ℒ̄ ⊆ ℳ, since ℒ ⊆ ℳ and ℳ is closed), then 𝒩 ⊆ {γ/|γ| : L ∈ ℒ̄}, which is countable:
   65| ℒ̄ is compact (closed, bounded — correlation entries in [−1, 1] — with finitely many label patterns), so the continuous
   66| image of ℒ̄ is compact and contains the image ∪_n 𝒩_n of ℒ, hence contains its closure 𝒩.
   67| (i) If ℒ is finite, ℒ̄ = ℒ. Block-diagonal Σ_n with blocks from a finite list {R₁, …, R_q} (sizes ≤ b): an entry
   68| Σ_{ll′} is 0 across blocks and (R_t)_{ab} within a block of type t at positions a, b; so L is determined by the types,
   69| the within-block positions and the block-sharing pattern of the ≤ 15 + s₀ indices — finitely many choices. Equicorrelation
   70| ρ: Σ_V = (1 − ρ)I + ρJ, determined by |V| and the labels. Factor models with finitely many row types (λ_l, ψ_l):
   71| Σ_{ll′} = λ_lᵀλ_{l′} (l ≠ l′), 1 on the diagonal — determined by the types of the indices. The floor c_m is λ_min of the
   72| whole Σ_n or better (Cauchy interlacing), e.g. min_t λ_min(R_t) for blocks.
   73| (ii) Stationary: sort V = {v₁ < … < v_m}; L is determined by the labels and the gaps g_t := v_{t+1} − v_t ∈ ℕ_{≥1}
   74| (Σ_{v_av_b} = r(g_a + … + g_{b−1})). On the one-point compactification ℕ̄ = ℕ ∪ {∞} with r(∞) := 0 and sums involving
   75| ∞ equal to ∞, the map (g, labels) ↦ Σ_V is continuous exactly because r(d) → 0; the domain (ℕ̄)^{m−1} × (labels) is
   76| countable and compact, so its image is a countable compact set containing ℒ, hence containing ℒ̄; and ℒ̄ ⊆ ℳ because
   77| ℒ ⊆ ℳ and ℳ is closed. Hence ℒ̄ is countable. For block-diagonal designs with stationary blocks from finitely many r's,
   78| add the (finite) block-sharing pattern and types to the labels. AR(ρ): r(d) = ρ^d; banded/MA(q): r(d) = 0 for d > q. ∎
   79| 
   80| ## (VIS-e)
   81| Independent columns: Σ⁻¹ = I. AR(ρ): Σ⁻¹ is tridiagonal with off-diagonal entries −ρ/(1 − ρ²); with d_l = s^l,
   82| s := sgn ρ (s := 1 if ρ = 0), (DΣ⁻¹D)_{l,l+1} = −ρ s/(1 − ρ²) = −|ρ|/(1 − ρ²) ≤ 0; λ_min(Σ_V) ≥ λ_min(Σ) ≥ min_ω f(ω) =
   83| (1 − |ρ|)/(1 + |ρ|), f(ω) = (1 − ρ²)/(1 − 2ρ cos ω + ρ²) the spectral density (Toeplitz eigenvalues lie in [min f, max f];
   84| interlacing). Equicorrelation ρ ∈ [0, 1): Σ⁻¹ = (1 − ρ)⁻¹(I − ρ(1 + (p − 1)ρ)⁻¹J), off-diagonal ≤ 0; eigenvalues of Σ are
   85| 1 − ρ and 1 + (p − 1)ρ. One factor: Σ⁻¹ = Ψ⁻¹ − Ψ⁻¹λλᵀΨ⁻¹/(1 + λᵀΨ⁻¹λ) (Sherman–Morrison), off-diagonal
   86| −λ_lλ_{l′}/(ψ_lψ_{l′}(1 + λᵀΨ⁻¹λ)); with d_l = sgn λ_l these become −|λ_l||λ_{l′}|/(…) ≤ 0; Σ ⪰ Ψ gives λ_min ≥ min ψ_l.
   87| Block-diagonal: Σ⁻¹ is block diagonal, D blockwise, and the components of the graph of Σ⁻¹ lie inside blocks, so the
   88| alignment of (VIS-a) is required only within a block. ∎
   89| 
   90| ## Remarks
   91| - (VIS-a) and (VIS-b) are separate routes; neither contains the other. (VIS-a) works n by n (D_n and the alignment may
   92|   change with n), while B in (VIS-b) collects the hyperplanes of all n. Example ([status omitted], VSL1): S₀ = {1, 2},
   93|   Σ_n = [[1, r_n], [r_n, 1]] ⊕ I, alternating (r_n, ϑ_n) = (1/2, (1, 2)) and (−1/2, (1, −2)): (VIS-a) applies at every n
   94|   (D = I, resp. D = diag(1, −1, 1, …)) with margin ≥ 3/4, but B ⊇ {θ₁ + θ₂/2 = 0} ∪ {θ₁ − θ₂/2 = 0} contains every ϑ_n,
   95|   so δ = 0. (VIS-a) gives the explicit constant θ_lo c₁₆ directly.
   96| - Track C's designs (`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md:28-50`; spread placement signs + − + −, clustered
   97|   placement four adjacent aligned truths). *(VIS-a) instances:* IND in both placements (components are singletons, so
   98|   alignment is vacuous); the clustered (aligned) placement of AR(ρ), ρ > 0, of the block compound-symmetry designs, of
   99|   the one-factor designs (D10, D12, D14) and of S5 (D16; s5-type M-matrix form, B8); the block compound-symmetry designs
  100|   with the spread placement too, since track C's spread truths lie in different blocks (alignment is required only
  101|   within a block). *(VIS-b) cases:* AR(ρ) with the spread placement (not aligned; there the (VIS-a) inequality itself can
  102|   fail), Toeplitz in both placements (its precision matrix may well be a Stieltjes matrix, which would put the clustered
  103|   placement under (VIS-a), but this is not [status omitted] here), the one-factor designs with the spread (mixed-sign) placement
  104|   (D10, D12; D14's spread truths lie on B), the three-factor designs D11, D13, D15 (not covered by (VIS-e), which treats
  105|   one factor), S5's spread placement, and the FRED-QD-like tiles (D19). B8's s5
  106|   and fac2 (aligned truths) are shown inside by B8's own computations — s5 by the M-matrix form of Σ⁻¹, i.e. a (VIS-a)
  107|   instance; fac2 by an explicit formula for the conditional covariances (`Theory_work/Wave3/W3-AUDIT/TRACK_B.md:222-228`).
  108| - Illustration of B (AR(ρ), two truths at distance g, U = ∅, j = k₁): γ = (1, ρ^g), so B ⊇ {θ₁ + ρ^gθ₂ = 0} for each gap g
  109|   that occurs along the sequence (all g ≥ 1 if the truths' gap ranges over ℕ; a single g if their positions are fixed);
  110|   U ≠ ∅ adds further hyperplanes (e.g. γ = (Var(W_{k₁} | W_U), 0) when U contains a column between the truths, by the
  111|   Markov property). The hyperplanes θ₁ + ρ^gθ₂ = 0 accumulate at {θ₁ = 0}, which |θ*_k| ≥ θ_lo keeps at distance; a
  112|   fixed mixed-sign ϑ is visible with a uniform margin unless it lies on one of the (countably many) hyperplanes of B.
  113| - Mixed-sign pervasive factors (track C D14, D15: population visibility 0) have ϑ on B: consistent with "Not claimed".
```

## 3. Theorem 5 (reader version)
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 029bb748, lines 568–600:
```
  568| ## 5. Theorem 5 — The start law already concentrates
  569| <!-- ROW thm5 BEGIN -->
  570| **Card row** 3.3 · **Section version** 0.3 (2026-11-16)
  571| 
  572| 
  573| ### Reader statement
  574| **Theorem 5.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$, $\Sigma_n$ a correlation matrix, and let
  575| $y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with a deterministic $\theta^*$ (signal fixed on the standardised
  576| scale). Assume
  577| - **(A1) Model.** (S1), (S2), and $p>s_0$.
  578| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  579|   $S_0$.
  580| - **(A3) Small-set floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c$ for every $|S|\le16+s_0$.
  581| - **(A4) Visibility.** For every $j\in S_0$ and every $U\not\ni j$ with $|U|\le15$:
  582|   $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a$, for a fixed $a>0$.
  583| - **(A5) No leakage.** For every $l\notin S_0$ there is a set $H_l\supseteq\{l\}\cup S_0$ with
  584|   **$|H_l|\le e^{\kappa\sqrt{\log n}}$** such that, for every $U\not\ni l$ with $|U|\le15$ and $U_0:=U\cap H_l$:
  585|   $|\operatorname{Cov}(W_l,W_j\mid W_{U_0})|\le Cn^{-1/2}$ for $j\in S_0\setminus U_0$, and
  586|   $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|,|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for $v\in U\setminus H_l$,
  587|   $j\in S_0\setminus U_0$, where $r_n(n\log n)^{1/4}\to0$.
  588| 
  589| Then for every $c<\tfrac12$,
  590| $$
  591| P\big(\pi_0(S_0)\ge1-n^{-c}\big)\to1 .
  592| $$
  593| **If moreover (A6) every null column is uncorrelated with every true column, $\operatorname{Cov}(W_l,W_j)=0$ for
  594| $l\notin S_0$, $j\in S_0$, then**
  595| $$
  596| \mathbf{1-\pi_0(S_0)=O_P\big(\sqrt{\log n/n}\big)} .
  597| $$
  598| The exponent $\tfrac12$ cannot be improved: $1-\pi_0(S_0)\ge\tfrac13(n+1)^{-1/2}$ for every valid data set with
  599| $n\ge4$ and $s_0<K$ (hence for all large $n$) [S1-F4]; **so the rate under (A6) is optimal up to the factor
  600| $\sqrt{\log n}$.**
```

## 4. Theorem 6 (reader version)
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 029bb748, lines 660–700:
```
  660| ## 6. Theorem 6 — The reported model equals the truth (random Gaussian design; main theorem)
  661| <!-- ROW thm6 BEGIN -->
  662| **Card row** 3.1 · **Section version** 0.9 (2026-11-16) · **Pending delta** — (RM2-R rider merged, v0.8)
  663| 
  664| 
  665| ### Reader statement
  666| **Theorem 6.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a positive definite
  667| correlation matrix, and $y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with deterministic $\theta^*$. Fix
  668| $b\in(0,\tfrac12)$ and $\rho>0$ with $15\rho+b<\tfrac12$. Assume
  669| - **(A1) Model.** (S1), (S2) ($p\gg n$ allowed), (S3).
  670| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  671|   $S_0$.
  672| - **(A3) Visibility.** $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a>0$ for every $j\in S_0$ and every
  673|   $U\not\ni j$ with $|U|\le15$.
  674| - **(A4) Polynomial leakage set.** There is a deterministic $Q\supseteq S_0$ with $|Q|\le n^b$ and, for large $n$,
  675|   $|Q|\le K$ and ($Q=[p]$ or $K\ge2|Q|+32s_0+1$), such that:
  676|   (i) *(no leak outside $Q$)* there is a deterministic $\varpi_n$ with $\varpi_n\sqrt{n/\log n}\to0$ such that
  677|   $|\operatorname{Cov}(W_l,W_j\mid W_U)|\le\varpi_n$ for all $l\notin Q$, $j\in S_0\setminus U$, $|U|\le15$;
  678|   (ii) *(locality)* there is a deterministic $r_n\to0$, and every $l\notin Q$ has a deterministic
  679|   $H_l\supseteq\{l\}\cup S_0$, $|H_l|\le n^{\rho}$, such that for all $l\notin Q$, all $U\not\ni l$ with $|U|\le15$
  680|   and $U_0:=U\cap H_l$: $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|\le r_n$ and
  681|   $|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for all $v\in U\setminus H_l$, $j\in S_0\setminus U_0$ [S1-F3].
  682| - **(A5) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c>0$ for every $S$ with
  683|   $|S|\le5(A+1)(s_0+1)\log n$ and for every $S=Q\cup\{l\}$, $l\in[p]$.
  684| - **(A6) Local regressions within $Q$.** There are deterministic sequences $\nu_n=o(\log n)$ and $L_n$, and for every
  685|   $l\in[p]$ a deterministic $N_l\subseteq Q\setminus\{l\}$ with $|N_l|\le\nu_n$ [S1-F3], such that
  686|   $\|\bar\beta_{T,l}-\bar\beta_{T\cap N_l,l}\|_1\le L_n$ for every $T$ with $S_0\subseteq T\subseteq Q$, $l\notin T$,
  687|   where $L_n\to0$ and $L_n^2\log(|Q|+1)=o(\log n)$ (bars: population regression coefficients, zero-padded).
  688| 
  689| Then, under the joint law of design and noise, there are data events $\mathcal G_n$ with $P(\mathcal G_n)\to1$ on
  690| which **every** admissible run that produces output reports $\hat S=S_0$, whatever its seed and the outcome of its
  691| internal calibration; in particular $P(\text{output and }\hat S\neq S_0)\to0$. If moreover the delivery conventions
  692| (S4) hold [S1-F2, RM2R-1],
  693| $$
  694| P(\text{the run produces output})=1\ \ \text{for every admissible }n\ge3,\qquad P(\hat S=S_0)\to1 .
  695| $$
  696| The delivery statement lifts two integer limits of the code (IDEAL-W⁺); in the default configuration neither can be reached on any input R can represent ($n, p_{\mathrm{raw}} \le 2^{31}-1$) [T14-REP], so this matters only for the $n\to\infty$ form. The two limits are a base search cap of $10^6$ (`v3_run.R:96`) and a 32-bit integer bound $2^{31}-1$ on the search cap (`cpp/v3_core.cpp:474`). R stores matrix dimensions as 32-bit integers, so in the default configuration the base cap is $\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le32$ and the search cap is at most $32+\lfloor n/2\rfloor\le2^{30}+31$, and neither limit can fire [T14-REP]. Every such input lies in the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, on which delivery holds under the remaining conventions (S4), without IDEAL-W⁺ [RM2R-5]; IDEAL-W⁺ is used only by the asymptotic form. Representable inputs still carry the other obligations of IDEAL-W (for example `2*p-1` in `int` for $p\ge2^{30}$); the statement is for the default configuration (`v3.ls0_ell` unset).
  697| The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and returns no estimates; anything else it returns is flagged incomplete and is not covered (`v3_fit.R:84-85`; `v3_run.R:110-113, 142-147`) [B2]. [GUARD-W]
  698| 
  699| *Remarks.* (o) [RM2R-3] Under (S4), for every seed and calibration outcome,
  700| $P(\hat S\neq S_0)\le P(S_0\text{ is not the unique maximiser of the score})+P(\text{the local search from the start mode
```

## 5. Theorem 10 (reader version)
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 029bb748, lines 1282–1295:
```
 1282| ## 10. Theorem 10 — The printed outputs are consistent (card row 3.6; row 3.5 as a remark)
 1283| <!-- ROW thm10 BEGIN -->
 1284| **Card row** 3.6 (and 3.5) · **Section version** 1.1 (2026-11-16) · **Pending delta** post-freeze rider SAMP-R1
 1285| 
 1286| ### Reader statement
 1287| **Theorem 10.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a correlation matrix, and
 1288| $y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with a deterministic $\theta^*$. Assume
 1289| - **(A1) Model and method.** (S1), (S2), (S3), (S5); $p>s_0$.
 1290| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on $S_0$.
 1291| - **(A3) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c>0$ for every $|S|\le5(A+1)(s_0+1)\log n$.
 1292| - **(A4) Visibility** and **(A5) no leakage**: (A4) and (A5) of Theorem 5.
 1293| 
 1294| *Which designs.* (A5) holds only for designs with no leakage outside the true model, such as independent predictors.
 1295| AR and block designs, where a null is correlated with a truth at a fixed level, are **not** covered. For those designs
```

## 6. Notation: partial covariance
`Theory_work/Wave3/W3-READER/NOTATION.md` @ 029bb748, lines 155–175:
```
  155|   mean signal when $x_l$ joins $X_U$;
  156| * the **residual variance** left by $U$: $\tau^2_U:=\sigma_*^2+\|(I-P_U)\mu\|^2/(n-1)$ (noise plus unexplained signal
  157|   energy per observation);
  158| * the sample regression coefficient of $x_l$ on $X_U$: $\hat\beta_{U,l}:=(X_U^\top X_U)^{-1}X_U^\top x_l$,
  159|   zero-padded to a vector indexed by a larger set when needed.
  160| 
  161| **Random Gaussian design (population quantities).** With $W\sim N_p(0,\Sigma_n)$:
  162| * the **partial covariance** $\operatorname{Cov}(W_j,W_l\mid W_U)$ of $W_j$ and $W_l$ given $(W_k)_{k\in U}$;
  163| * the population regression coefficient $\beta_{U,l}:=\Sigma_{n,UU}^{-1}\Sigma_{n,Ul}$ of $W_l$ on $W_U$, and the
  164|   conditional variance $\operatorname{Var}(W_l\mid W_U)$.
  165| 
  166| **Leakage set and lattice.** A *leakage set* is a deterministic set $Q$ with $S_0\subseteq Q\subseteq[p]$ that
  167| contains every column able to imitate part of the signal; the *lattice* of $Q$ is
  168| $\mathcal L(Q):=\{T:S_0\subseteq T\subseteq Q\}$. "No leakage" means $Q=S_0$.
  169| 
  170| **Visibility.** A truth $j\in S_0$ is *visible* if its signal cannot be explained away by any $15$ other predictors
  171| ($15=$ largest block size minus one): the gain $\delta^2_{U,j}$ (fixed design) or the partial covariance
  172| $\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)$ (random design) stays large for every $U\not\ni j$ with $|U|\le15$.
  173| 
  174| ## 7. Asymptotic conventions and constants
  175| 
```

## 7. Design dossier B8 (visibility)
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 7df2d81c, lines 209–233:
```
  209| ## B8. Visibility (Thm 6 (A3); Thm 10 (A4)): |Cov(W_j, Wᵀθ* | W_U)| ≥ a for every true j and every |U| ≤ 15
  210| **Comparison: ours implies their Condition 5, in every regime** (p. 958: |cov(x_t, y)| > 0 for every true predictor; it
  211| is our case U = ∅ without the margin). We ask more: a fixed margin, and up to 15 conditioning columns. Same role: the
  212| cheap first stage must see every true predictor.
  213| **Evidence.** U = ∅ in (A3) gives |Cov(W_j, y)| ≥ a [one line]. SL need Condition 5 so that their iterative subset
  214| screening "ensures that all true predictors that are contained in X_s will be selected" (p. 958). Ours conditions on up
  215| to 15 other columns because the method's blocks have at most 16 columns.
  216| **Holds / fails.** Holds when no truth is cancelled by ≤ 15 others: bounded blocks with one truth each, AR, banded
  217| (W2-APP family map, "PTV automatic if ≤ 1 truth/block", `L4_families.md:165`). Fails for masked truths (zero marginal or
  218| partial covariance with y); those designs are treated by a separate theorem (W1-PXN), not by Thm 6. Track C gives two
  219| concrete failures at the population level: a pervasive factor with **mixed-sign** truths (its D14, D15: a set of ≤ 15
  220| columns cancels the truth's covariance with the signal) and a riboflavin-like real-data design (D18).
  221| **Designs** — [status omitted] (AUDITCALC_check_opus.md §5). Inside: S1–S4, S6, IND, AR, BLK (block or Markov structure: the
  222| covariance is θ_j Var(W_j | W_U) plus geometrically small terms, ≥ |θ_j| λ_min/2). cs(ρ) of P6: inside (aligned signs,
  223| positive partial covariances). **fac2 and s5 of P6: inside** (moved from "unclear" in v1.2). P6's truths have aligned
  224| signs (`W3-P6/DESIGN.md:16-17`), so it suffices that every conditional covariance between columns outside U is ≥ 0;
  225| then Cov(W_j, Wᵀθ* | W_U) ≥ θ_j Var(W_j | W_U) ≥ θ_j λ_min(Σ). *s5:* Σ⁻¹ = A⁻¹ − κJ with A = 0.3I + 0.4H, κ > 0, has all
  226| off-diagonal entries negative (an M-matrix), and so has every principal submatrix, hence all conditional covariances
  227| are ≥ 0; margin ≥ 0.3·θ_j. *fac2:* given any U with m₁ even and m₂ odd columns, the conditional covariance of two columns
  228| is 0.10/det (opposite parity) or (0.6 + 0.875·m_opp)/det (same parity), det > 0; margin ≥ 0.40·θ_j. (The reviewer's
  229| argument, API triage T8; I re-derived both computations; they agree with the checker's search values 0.364 and 0.431.)
  230| **Unclear, not upgraded:** S5 of the study (mixed signs; near-cancellation, worst ratio 0.0056) and FAC of 1M (0.16 in
  231| the checker's search, below the aligned-sign bound 0.7, so its signs are mixed). Track C agrees on all counts: visibility inside and rising with n for IND, AR(0.5), fixed
  232| blocks and S6; factor designs inside with aligned truths and outside with mixed-sign truths (its D14, D15); small for
  233| S5 (population 0.06). **Typical user:** the two real-data-like designs of track C are outside (riboflavin-like) or unclear
```

## 8. Track C table (internal proxy computations)
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 7df2d81c, lines 22–51:
```
   22| p = 10n series unless marked. **IN↑** inside, improving; **IN** inside, bounded; **UNCL↑** unclear, moving toward inside;
   23| **UNCL** unclear; **OUT** outside. Searches give upper bounds on minima (they refute, never certify); population floors are
   24| certified by λ_min(Σ); leak sets are subsets of the true ones ("IN" for P5 means "not refuted"). sp = spread truth (study
   25| positions, signs + − + −); cl = clustered (four adjacent columns, aligned signs). Visibility v̂ = δ̂²/log n (sample),
   26| pop = min δ² in the population (n-free).
   27| 
   28| ## Table: design × proxy × n trend (final)
   29| | D | design | P1–P3 floors (sample φ̂²(16); m♯ floor; pop λ_min(Σ)) | P4 visibility sp (sample; pop) | P4 visibility cl | P5 leak \|Q̂\| sp / cl | P6 ℓ¹ tail, P9 width (sp / cl) | P7 rate, margin | P8 Occam | P10 |
   30| |---|---|---|---|---|---|---|---|---|---|
   31| | 01 | IND | IN↑ .15→.54; .006→.22; 1 | IN↑ .37→145; 1 | IN↑ .006→151 | IN 4 / 4 | IN 0; −.55→−.68 / −.54→−.71 | IN↑ | IN | OUT |
   32| | 02 | AR0.5 | IN↑ .12→.29; .005→.14; .33 | IN↑ ≈0→4.6→28→80; .6 | IN↑ 1.1→102 | IN 32→46 / 8→10 | IN↑ 2.5→1.2, +.01→−.17 / IN | IN↑ | IN | OUT |
   33| | 03 | AR0.8 | IN↑ .05→.10; .003→.056; .11 | IN↑ ≈0→.01→5.6→21; .22 | IN↑ .26→40 | IN 109→137 / 19→23 | UNCL↑ 18.6→6.5, +.50→+.005 / IN | IN↑ | IN | OUT |
   34| | 04 | AR0.95 | IN↑ small .013→.023; .001→.014; .026 | UNCL↑ ≈0 to n=800, .45 at 1600; .05 | IN↑ .41→8.8 | IN (slow) 466→585 [n^0.11] / 70→87 | sp UNCL 26→39, +.57→+.42 / cl IN↑ 23→8.5, −.01→−.26 | IN↑ (margin small) | IN | OUT |
   35| | 05 | BLK5-0.7 | IN↑ .08→.21; .004→.11; .3 | IN↑ ≈0→.9→12→40; .37 | IN↑ 7.4→73 | IN 20 / 5 | IN↑ 1.8→.6, −.20→−.45 / IN | IN↑ | IN | OUT |
   36| | 06 | BLK5-0.85 | IN↑ .04→.11; .003→.057; .15 | IN↑ ≈0→≈0→4.8→14; .19 | IN↑ 3.9→37 | IN 20 / 5 | IN↑ 2.5→.84, −.28→−.54 / IN | IN↑ | IN | OUT |
   37| | 07 | BLK√p-0.5 | IN↑ .10→.31; .006→.14; .5 | IN↑ ≈0→.4→14→55; .53 | IN↑ 10→104 | UNCL 180→508 / 45→127 [n^0.5 = √p block, by design] | sp UNCL 12→14, +.57→+.47 / cl IN 4.2→3.9, +.05→−.05 | IN↑ | IN | OUT |
   38| | 08 | TOEP α=1 | IN↑ .12→.32; .005→.15; .39 | IN↑ ≈0→7.5→27→80; .61 | IN↑ 5.4→120 | UNCL 207→508 [n^0.43] / 33→76 [n^0.40] | sp UNCL 10.6→12, +.67→+.57 / cl IN 2.6→2.1, +.04→−.06 | IN↑ | IN | OUT |
   39| | 09 | TOEP α=2 | IN↑ .15→.48; .005→.20; .65 | IN↑ ≈0→11→47→131; .88 | IN↑ 7.4→172 | IN 32→53 [n^0.24] / 8→11 | IN↑ 2.1→1.2, −.01→−.22 / IN | IN↑ | IN | OUT |
   40| | 10 | FAC a=.5 k=1 | IN↑ .15→.54; .006→.22; .97–.99 | IN↑ .003→139; .93→.97 | IN↑ ≈0→12→147 | IN 4 / 4 (= S₀ at every n at p = 10n; at p = n from n = 800) | IN 0; −.63→−.71 / IN | IN↑ | IN | OUT |
   41| | 11 | FAC a=.5 k=3 | IN↑ .15→.54; .006→.22; .97–.99 | IN↑ .08→149; .93→.97 | IN↑ ≈0→13→154 | IN 4 / 4 (as D10) | IN 0; −.61→−.74 / IN | IN↑ | IN | OUT |
   42| | 12 | FAC a=.75 k=1 | IN↑ .14→.52; .006→.21; .87–.92 | IN↑ ≈0→5.8→51→120; .60→.74 | IN↑ .39→169 | OUT [p] / [p] | OUT ≈9–17 flat, +.79→+.81 / OUT | IN↑ | IN | OUT |
   43| | 13 | FAC a=.75 k=3 | IN↑ .15→.52; .006→.21; .87–.92 | IN↑ ≈0→8.5→40→113; .60→.74 | IN↑ ≈0→7.8→57→156 | OUT 600→16000 (= p at 1600) / [p] | OUT / OUT | IN↑ | IN | OUT |
   44| | 14 | FAC a=1 k=1 (cs .5) | IN↑ .08→.27; .003→.11; .5 | **OUT** 5e-7→.012→.019→.10; pop 0 | IN↑ 2.9→100 | OUT [p] / [p] | OUT / OUT | IN↑ | IN | OUT |
   45| | 15 | FAC a=1 k=3 | IN↑ .09→.28; .003→.12; .5 | **OUT** ≈1e-11 at every n; pop 0 | IN↑ ≈0→1.5→13→51 | OUT [p] / [p] | OUT / OUT | IN↑ | IN | OUT |
   46| | 16 | S5 (0.3 global + blocks) | IN↑ .07→.21; .003→.10; .3 | IN↑ (small margin) ≈0→.9→6.9→16; .062 | IN↑ 7.8→72 | OUT [p] / [p] | OUT / OUT | IN↑ | IN | OUT |
   47| | 17 | S6 (blocks ρ .4–.9) | IN↑ .05→.09; .002→.044; .1 | IN↑ ≈0→5.7→5.0→67; .25–.49 | IN↑ 14→136 | IN 20 / 5 | IN↑ 1.5→.5, −.18→−.47 / IN | IN↑ | IN | OUT |
   48| | 18 | riboflavin-like | IN↑ small .04→.09; .002→.039; .1 | **OUT** ≈0 at every n; pop ≈0 | **OUT** ≈0 at every n; pop ≈0 | OUT [p] / [p] → one copy (4088) | OUT 13→25, +.74→+.77 / OUT | IN↑ (margin smaller) | IN | OUT |
   49| | 19 | FRED-QD-like | IN↑ small .05→.09; .002→.048; .1 | UNCL↑ ≈0→.19→5.2→42; pop .24–.30 | IN↑ (small margin) .11→14; pop .076 | IN (bounded by tiles) 628→679 / 170 | sp UNCL 14→19, +.77→+.60 / cl UNCL↑ 18→8.3, +.52→+.04 | IN↑ | IN | OUT |
   50| 
   51| Notes. P3 (floor on Q̂ ∪ {l}, computed where Q̂ fits the lattice cap) rises with n wherever computed (p = 10n slopes +0.07
```

## 9. Track C design definitions
`Theory_work/Wave3/W3-AUDIT/work/C_PLAN.md` @ 7df2d81c, lines 8–22:
```
    8| ## 1. Designs (Gaussian rows N(0, Σ), standardised; s₀ = 4, σ = 1; 19 designs)
    9| Common truth, two placements per X: **spread** = study positions (`gen_dev_data.R:33`, step = ⌊p/s₀⌋), β = (1.4, −1.0, 1.8, −1.2); **clustered** = four consecutive columns inside one correlated group or block, aligned β = (1.4, 1.0, 1.8, 1.2) (the NEG regime of P6, `W3-P6/DESIGN.md` §1).
   10| | ID | Σ (unit diagonal) | parameters |
   11| |---|---|---|
   12| | D01 | IND | I (= S1, `gen_dev_data.R:18`) |
   13| | D02–D04 | AR(ρ) | ρ = 0.5 (= S2), 0.8, 0.95 |
   14| | D05–D06 | block compound symmetry, blocks of 5 | ρ_b = 0.7 (= S3), 0.85 (= S4) |
   15| | D07 | block CS, growing blocks | block size ⌈√p⌉, ρ_b = 0.5 (growing one-factor groups, RM) |
   16| | D08–D09 | Toeplitz, algebraic decay | Σ_jk = (1+\|j−k\|)^(−α), α = 1, 2 (outside the exponential-decay class of W2-APP LOC) |
   17| | D10–D15 | factor, spike λ₁ ≈ 0.5 p^a | x = √h_p Lf + √(1−h_p) e, h_p = 0.5 p^(a−1) split over k_f factors; a ∈ {0.5, 0.75, 1}, k_f ∈ {1, 3}; a = 1, k_f = 1 is P6 cs(0.5); k_f = 3 uses loadings 1, (−1)^j, group-wise ±1 (P6 `fac2`) |
   18| | D16–D17 | study S5, S6 | 0.3·11ᵀ + 0.4H + 0.3I; block ρ = 0.4 + 0.1·((g−1) mod 6) (`gen_dev_data.R:21-22`) |
   19| | D18 | real-data-like: riboflavin | Σ_δ = 0.9 R + 0.1 I, δ = 0.1, R = riboflavin sample correlation (n_data = 71, p = 4088, rank 70; hdi 0.1-10, CRAN Archive). Exact factor form is in `Wave2/W2-SIM/X/data/riboflavin_L.csv` (made by `make_real_lambda.R:1-30`). p < 4088: fixed-seed random column subset. p > 4088: block-diagonal tiling of independent copies |
   20| | D19 | real-data-like: FRED-QD | same recipe, `fred_qd_L.csv` (p = 170, tiled; macro series, one mild factor, top-1 trace share 0.26) |
   21| Seeds: `seed = base + 10000·design + rep`, `RNGkind("Mersenne-Twister","Inversion","Rejection")`, X drawn first (`gen_dev_data.R:52-54`). 10 replicates of X per (design, n, p); both placements are scored on the same X.
   22| 
```

## Task (sent as a separate block)

Break the lemmas; findings only.

Items to judge (8), in this order; return one machine line for each:
V:VIS-0 — (VIS-0): the reduction to <gamma(U, j), theta> and the lower bound Var(W_j | W_U) >= c16
V:VIS-a — (VIS-a): the sign route (Stieltjes after sign flips, aligned truths) and its constant theta_lo*c16
V:VIS-b — (VIS-b): the generic route: B closed, |vis| >= c16*dist(theta, B), the uniform constant a = c*delta
V:VIS-c — (VIS-c): B null and nowhere dense when the set of local directions has countable closure
V:VIS-d — (VIS-d): finitely many local patterns and stationary designs give countable closure
V:VIS-e — (VIS-e): the instances (IND, AR of either sign, equicorrelation, one factor, blocks) with their floors
V:UNIF — the lemma gives a margin uniform in n (B does not depend on n), not merely nonzero for almost every theta at each n
V:SCOPE — the design statements (which designs are inside by which route; D14/D15 on B; D18 not covered) agree with the lemma and the dossier
