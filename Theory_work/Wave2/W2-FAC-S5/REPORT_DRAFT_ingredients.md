# Ingredients used by the W2-FAC-S5 proofs (for W2-UNI; population-level formulation)

Tier 1 (Theorem FAC-BCS-R) uses only the following properties of the design. Everything else is algebra of the method's
score (L1.4) and the inherited Wave-1C machinery (L5).

1. **Exact Gram** XᵀX = (n − 1)Σ with Σ a fixed-structure correlation matrix (model G). Random rows would add the
   perturbation ‖R̂ − Σ‖ ≈ √(p/n), entering through ε of L1.4 — not handled here.
2. **Eigenvalue floor on all principal submatrices**: λ_min(Σ_TT) ≥ d > 0 for every T (used in L1.4 ridge/leakage
   bounds, (L1.4.1) determinant increments, L2 positive pairs, L4.4 truth moves, L5.1 (H0)). For BCS d = 1 − ρ_w.
   This is stronger than W2-UNI's (A1) sparse floor on log-size sets: here sets of size up to p are scored.
3. **One-factor + bounded-block structure** Σ = λλᵀ + Ψ, Ψ block-diagonal with blocks of size ≤ q̄, used for: (a) the
   exact residual decomposition τ_{l|R} = (group part) + (coefficient)·e_R with e_R the scalar error in predicting the
   common factor (L1.3); the group part depends only on (l, R ∩ own block): at most p·2^{q̄} distinct Gaussian
   statistics, controlled by one union bound (E_A, level H_q = √(2 log(2^{q̄}p) + 2 log log n)); (b) a uniform coefficient
   bound c_u/√v ≤ κ₀. **General loadings / general Ψ blocks:** the same decomposition holds for any one-factor model with
   bounded Ψ-blocks (e_R := factor-prediction error; the coefficient becomes λ̃_{l|U}/√v, uniformly bounded by FAC-A's
   κ-type constant), so L1.3/L3/L4 extend verbatim with κ₀ replaced by that constant (not re-checked here).
   **k fixed factors:** e_R becomes a k-vector and the bound |τ| ≤ |A| + ‖coef‖·‖e_R‖; Tier 1 extends with CC stated for
   ‖e_R‖ (not written out).
4. **Positive partial covariances** (inverse-M-matrix property) — used only for the start-mode genericity (FS-BCS) in L2;
   a general version is "c(U, l) ≠ 0 except zero pairs" as an explicit non-cancellation hypothesis (W2-UNI's (A3)).
5. **Beta-min / non-masking**: fixed nonzero ϑ (beta-min at the √n scale, much stronger than needed) and (FS-BCS).
6. **Growth**: p ≤ n/2 for the start mode; p ≤ n^α, α < 1/2 for the path (union-bound level H_q² ≈ 2 log p must stay below
   log n); M_T = ½(1 + o(1)) needs p = o(n).
7. **The centre condition CC_n(δ)** (a path-level event on the latent factor error) — the only non-structural ingredient;
   its probability is the open Tier-2 problem (KL).
