# T01 (A0 = T1): Contrast reduction and mixed-rate transfer

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** algorithmic validity and robustness (foundation); **core** (lemma).

## Definitions used
Standardised data, contrast coordinates (U, y_c, X_c), m(S), Q_S, D_S, H_S, ν, ϖ, F, Z, π (00_COMMON §1). Contrast-scale parameters θ = s_yβ, v = s_y²σ²; z_S^c = s_y z_S; Q_S^c = s_y²Q_S. m^c_b(S) := the contrast marginal likelihood of model S when the IG rate is b (shape 0.51): the marginal of y_c under y_c | θ_S, v, S ~ N_{n−1}(X_{c,S}θ_S, vI), θ_S | v ~ N(0, nv(G_S+I)⁻¹), v ~ IG(0.51, b).

## Assumptions
- Identities: valid input (n ≥ 3, no constant column, non-constant y^r). None else.
- Scale event: G (standard/project), R (project bundle).

## Precise statement
(i) [identity] For every valid input, the joint transformed posterior of (S, θ, v) under v3 equals the posterior of the contrast model
  y_c | θ_S, v, S ~ N_{n−1}(X_{c,S}θ_S, vI), θ_S | v, S ~ N(0, nv(G_S+I)⁻¹), v ~ IG(0.51, b₀s_y²), prior ϖ,
and m(S) = c_n(s_y)·m^c_{b₀s_y²}(S) with the model-independent factor c_n(s) = s^{n−1}Γ(0.51)/(√(2πb₀)Γ(0.01)). Bayes factors and posterior model probabilities coincide; evidences differ by c_n(s_y). The conditionals are v | S, y ~ IG(ν, b₀s_y² + Q_S^c/2) and θ_S | v, S, y ~ N(nH_S⁻¹z_S^c, nvH_S⁻¹).
(ii) [envelope] For fixed 0 < b₋ ≤ b ≤ b₊ and κ = (b₊/b₋)^{0.51}: κ⁻¹m^c_{b₊}(S) ≤ m^c_b(S) ≤ κm^c_{b₋}(S) for every S and every y_c. The same domination holds for nonnegative joint numerator integrals I_b(E) over parameter events E, giving Π_b(E) ≤ κ²I_{b₋}(E)/Z^c_{b₊}.
(iii) [scale event] Under G and R: s_y² − (σ*² + ‖μ‖²/(n−1)) = O_{P₀}(n^{−1/2}), and P₀(s_y² ∈ [σ*²/2, 2(σ*²+M)+1]) → 1. Uᵀε ~ N_{n−1}(0, σ*²I) exactly.
(iv) [rate derivative, fixed contrast data] ∂_b log[m^c_b(S)/m^c_b(R)] = 2ν(Q_S^c − Q_R^c)/((2b+Q_S^c)(2b+Q_R^c)).
Transfer rule: a target bound holds for v3 on the event of (iii) at multiplicative cost κ² only in the mixed-endpoint form (numerator sums at b₋, S₀-denominator at b₊); same-rate bounds alone do not establish it. Errors are never treated as Gaussian conditional on s_y.

## Dependencies
Builds on: method §5 definitions. Used by: T02, T03, T04, T05, T08, T22 (block-score expansions).

## Numerical evidence (provisional)
provisional evidence (Sol check J1): on one centred dataset (n = 24, p = 6, all 64 models), max absolute residuals of the score, Q, posterior-mean, covariance, joint log-density and posterior-probability identities ≤ 2.2·10⁻¹⁴; envelope violations 0. provisional evidence (Sol check J2): independent implementation (n = 6, p = 4) agrees to 2.7·10⁻¹⁵. Sol files: judge/sol1/J1_TARGET_TRANSFER.md, judge/sol2/J2_EXACT_IDENTITIES.md.

## Proof-route hint (optional)
Change variables θ = s_yβ, v = s_y²σ² keeping the Jacobian s_y^{−k−2}; integrate β_S and σ² with all constants; IG density ratio (b/b₋)^{0.51}e^{−(b−b₋)/v} ≤ κ; χ²_{n−1} concentration for ‖Cε‖², cross term 2μᵀε/(n−1) = O_P(√Mσ*/√n). Hardest step: none in the algebra; the downstream mixed-rate numerator/denominator argument. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
