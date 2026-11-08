# L8 — A canonical, checkable certificate for (H2): block projection coefficients

Status: **PROVED (by this seat, unchecked)**. Added after the mid-point review R05 (item 4: "give one worked
non-LH/non-W certificate"; item 2 of the statement lock R01: the exact Λ-minimiser is not a valid certificate in
general). This is a sufficient condition for (H2b)–(H2c); it changes no hypothesis of STATEMENT.md.

Setting: fixed design, notation of STATEMENT §1, (H2a) on the actual blocks, and bounded energy ‖μ‖² ≤ Mn with the
same fixed M used in the thresholds below (sweep R10 item 1). Minima over empty supports are +∞ (conditions on blocks
with empty support are vacuous). The certificate supplies (H2b)–(H2c) only; using it in Theorem GEN still requires
S* ⊆ 𝒱, s* ≤ v̄, feasibility and the relevance-set hypothesis (H1) (or S* = S₀). For each block b, since X_{C_b} has full
column rank, the block projection of μ has unique coefficients

  P_{C_b}μ = X_{C_b}γ_b,   γ_b ∈ ℝ^{C_b}   (γ_b = G_{C_b}⁻¹X_{C_b}ᵀμ: the regression of μ on the block alone).

## L8.1 Exact certificate

**Lemma L8.1.** Let U*_b := supp(γ_b) and S*_can := ∪_b U*_b. Then:
(a) the minimisers of U ↦ Λ_U over U ⊆ C_b are exactly the sets U ⊇ U*_b (so U*_b is the unique ⊆-minimal one);
(b) every leakage residual vanishes: δ_{T,l} = 0 for all (b, T, l) ∈ 𝓛(S*_can) (NL_η with η = 0);
(c) for U ⊆ C_b with U*_b ⊄ U and M := U*_b ∖ U: g_{b,U} ≥ (n − 1)φ₀²‖γ_{b,M}‖² ≥ (n − 1)φ₀² min_{j∈U*_b} γ²_{b,j}.
Hence (H2b) holds for S*_can as soon as the **block beta-min** condition holds:

  (n − 1)φ₀² min_{b} min_{j∈supp γ_b} γ²_{b,j} ≥ M_n (σ² + 2M) log n,  M_n → ∞   (empty minima = +∞).      (BBM)

*Proof.* For U ⊆ C_b, Λ_U = ‖μ‖² − ‖P_Uμ‖² and ‖P_Uμ‖² = ‖P_U P_{C_b}μ‖² ≤ ‖P_{C_b}μ‖², with equality iff
P_{C_b}μ ∈ span X_U. As X_{C_b} has independent columns, X_{C_b}γ_b ∈ span X_U iff supp(γ_b) ⊆ U. This is (a).
(b) If U*_b ⊆ T ⊆ C_b ∖ {l}, then P_{C_b}μ = X_{U*_b}γ_{b,U*_b} ∈ span X_T, and u_{T,l} ∈ span X_{T∪{l}} ⊆ span X_{C_b}
with u_{T,l} ⊥ span X_T; so δ_{T,l} = u_{T,l}ᵀμ = u_{T,l}ᵀP_{C_b}μ = 0. (c) U ∪ U*_b ⊆ C_b contains supp γ_b, so
P_{U∪U*_b}μ = P_{C_b}μ and (P_{U∪U*_b} − P_U)μ = (I − P_U)P_{C_b}μ = (I − P_U)X_Mγ_{b,M} (the columns in U*_b ∩ U are
annihilated). Its squared norm is γ_{b,M}ᵀ[X_Mᵀ(I − P_U)X_M]γ_{b,M}, and the bracket is the Schur complement of G_U in
G_{U∪M}, with λ_min ≥ (n − 1)φ₀² by (H2a). Finally v_U ≤ σ² + ‖μ‖²/(n − 1) ≤ σ² + Mn/(n − 1) ≤ σ² + 2M for n ≥ 2, so g_{b,U} ≥ M_n v_U log n. ∎

## L8.2 Thresholded certificate (near-zero coefficients)

**Lemma L8.2.** Suppose each γ_b splits as γ_b = γ^L_b + γ^S_b with disjoint supports, and for fixed
0 ≤ η < (√(2A + 1) − √(2A))² and some M_n → ∞:
  (i) ‖X_{C_b}γ^S_b‖² ≤ ησ² log n for every b;
  (ii) √((n − 1)φ₀²) min_{j∈supp γ^L_b}|γ^L_{b,j}| ≥ √(ησ² log n) + √(M_n(σ² + 2M) log n) for every b with
       supp γ^L_b ≠ ∅.
Then S* := ∪_b supp(γ^L_b) satisfies (H2b) and NL_η(S*), hence (H2c).

*Proof.* Put U*_b := supp γ^L_b and write P_{C_b}μ = X_{U*_b}γ^L_{b,U*_b} + s_b, s_b := X_{C_b}γ^S_b. For U ⊆ C_b,
projections of μ onto subspaces of span X_{C_b} equal those of P_{C_b}μ. VIS: (P_{U∪U*_b} − P_U)X_{U*_b}γ^L =
(I − P_U)X_Mγ^L_M with norm ≥ √((n − 1)φ₀²)‖γ^L_M‖ (L8.1(c)), and ‖(P_{U∪U*_b} − P_U)s_b‖ ≤ ‖s_b‖ ≤ √(ησ² log n);
so √g_{b,U} ≥ √((n − 1)φ₀²)‖γ^L_M‖ − √(ησ² log n) ≥ √(M_n(σ² + 2M) log n) ≥ √(M_n v_U log n) (n ≥ 2). Leakage: for
U*_b ⊆ T ⊆ C_b ∖ {l}, u_{T,l} ⊥ X_{U*_b}, so δ_{T,l} = u_{T,l}ᵀs_b and δ²_{T,l} ≤ ‖s_b‖² ≤ ησ² log n. ∎

## L8.3 Reading and examples

* **Interpretation.** (BBM) is a beta-min condition on the **block-level regression coefficients** of the mean on each
  block's own columns (with the response's full signal, as the tables see it). A true variable is *masked* exactly
  when its block coefficient vanishes (or is negligible, L8.2); a null enters S* exactly when it carries a non-
  negligible block coefficient (a block-level proxy). This is the block analogue of the marginal-correlation condition
  that Song–Liang's Condition 5 imposes globally: here it is imposed per block, and violations (masking) are allowed
  and repaired by the descent (L3) instead of being excluded.
* **Checkability.** Given (X, β, σ², actual partition): one least-squares solve per block (B ≤ 16 columns), then
  (BBM)/(L8.2) are explicit inequalities. For iid designs the population version uses Σ_{C_bC_b}⁻¹Σ_{C_b,·}θ.
* **LH (exact Gram).** γ for an a-group = β_i(1 − ψ_i²)e_{a_i} (only the hub; L6(a)), b-groups γ = 0 (masked), visible
  groups γ = θ_he_h, null groups γ = 0: S*_can = S₀ ∖ M, (BBM) with fixed coefficients. Recovers L6(a)'s (H2).
* **W.** In a signal group C ∋ j₁, P_Cμ = θx_{j₁} + θP_Cx_{j₂}; take γ^L := γ_{j₁}e_{j₁} (the actual coefficient on the
  active coordinate, θ(1 + O(ε_n))) and γ^S := the coefficients on the other coordinates. The off-active part of P_Cμ is
  part of θP_Cx_{j₂}: writing P_Cx_{j₂} = c x_{j₁} + X_{C∖j₁}γ′, X_Cγ^S = θX_{C∖j₁}γ′ = θ(P_Cx_{j₂} − c x_{j₁}), so
  ‖X_Cγ^S‖ ≤ θ(‖P_Cx_{j₂}‖ + |c|√(n − 1)) with ‖P_Cx_{j₂}‖² ≤ (n − 1)·9ε_n²·(4/3) and |c| ≤ (4/3)·3ε_n (λ_min(Σ_C) = ¾,
  ‖Σ_{C,j₂}‖ = 3ε_n); hence ‖X_Cγ^S‖² = O(nθ²ε_n²) → 0;
  null groups: γ^L = 0, ‖X_Cγ^S‖² = ‖P_Cμ‖² = O(nθ²ε_n²). So L8.2(i) holds for any η > 0 eventually. Recovers L6(c).
* **A worked non-LH, non-W instance ("finite-core designs").** Exact Gram; a core 𝒦 of fixed size k̄ ≥ s₀ containing
  S₀ with an arbitrary fixed correlation matrix Σ_𝒦 (λ_min(Σ_𝒦) ≥ φ₀²) and fixed θ; all remaining columns orthogonal to
  𝒦 (arbitrary correlations among themselves, subject to (H0)'s anchored sparse-eigenvalue conditions and (H2a)).
  Then: (H1) holds with 𝒱 := 𝒦, ζ_n = 0 (outside columns are orthogonal to μ and to 𝒦); for any actual partition,
  a block's γ_b is the regression of μ on (C_b ∩ 𝒦) (outside columns in the block get coefficient 0), a fixed
  function of Σ_𝒦, θ and the core's block pattern; if every nonzero entry of every such γ_b is nonzero in the limit
  (generic in (Σ_𝒦, θ)), (BBM) holds with M_n ≍ n/log n and L8.1 gives (H2) with S* = S*_can ⊆ 𝒦. So (C3) holds, with
  masking whenever some truth has zero coefficient in its core block. Example: 𝒦 = {1, 2, 3}, Σ_𝒦 with r₁₂ = r, r₁₃ =
  r₂₃ = 0 (0 < |r| < 1), θ = (1, −r, 0), so μ = x₁ − rx₂ and S₀ = {1, 2}. If 1 and 2 lie in different blocks, the
  block of 2 has γ = 0 on x₂ (Cov(x₂, μ) = r − r = 0, and its other members are orthogonal to μ): x₂ is masked, while
  the block of 1 has γ = (1 − r²)e₁; S*_can = {1}, and the descent adds x₂ (one move). If 1 and 2 share a block,
  γ = (1, −r) on them: no masking, S*_can = S₀. Both cases are covered.
