# T08 (A7 = T6): Oracle joint Bernstein–von Mises limit

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** asymptotic normality / Bernstein–von Mises; **optional** (theorem).

## Definitions used
Joint contrast posterior Π† (T01(i)); θ̂₀ = contrast least squares on S₀; v̂₀ = ‖(I − P_{X_{c,S₀}})y_c‖²/(n−1); Γ₀ from GL; conditionals v | S, y ~ IG(ν, b₀s_y² + Q_S^c/2), θ_S | v, S, y ~ N(nH_S⁻¹z_S^c, nvH_S⁻¹).

## Assumptions
G, R, SE (project); BM-C or BM-∞ (through T03); GL (project limit form; generic BvM precedent UNVERIFIED).

## Precise statement
Conditional on S = S₀, the posterior law of (√n(θ_{S₀} − θ̂₀), √n(v − v̂₀)) converges in total variation, in P₀-probability, to N_{s₀+1}(0, diag(σ*²Γ₀⁻¹, 2σ*⁴)). Embed by zero-padding outside S₀ in the common space ℝ^{p_n+1} of the transformed full posterior; removing the support conditioning costs at most 1 − π(S₀) in total variation (T03). The scaled coefficient covariance conditional on (v, S₀) is exactly n²vH_{S₀}⁻¹ → vΓ₀⁻¹. No coefficient-interval output is added to v3.

## Dependencies
Builds on: T01, T03, T04. Used by: nothing (terminal, optional).

## Numerical evidence (provisional)
provisional evidence (Sol check J11): conjugate scaling at n = 64, 256, 1024: max|nCov(θ) − R⁻¹| = 1.6·10⁻⁴, 1.0·10⁻⁵, 6.3·10⁻⁷; nVar(v) → 2.0; this verifies scaling and the variance factor, not joint total variation.

## Proof-route hint (optional)
Direct conjugate expansion from the exact conditionals (not an imported generic BvM): ridge centring bias O(1/n) = o(n^{−1/2}); IG centring shift O(1/n) under bounded support conditions; IG-normal approximation; uniform control of the empirical rate via T01; then joint total variation and asymptotic independence. Hardest step: joint total variation. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
