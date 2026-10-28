# T04 (A3 = T4): Contraction without beta-min

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** contraction rate and dimension consistency; **core** (theorem); the double-logarithm fallback clause (i) is **secondary**.

## Definitions used
Joint contrast posterior Π† of (S, θ, v) with θ zero-padded (T01(i)); μ = Xθ*; regime R1; ε_{2,n}² = (s₀+1)log²(p∨n)/n; ε_{1,n}² = (s₀+1)log(p∨n)/n; d_* = s₀ + ⌈s₀(2A+1)⌉.

## Assumptions
G, R (project); SE (project) for the bounded-dimension, single-log and coefficient clauses; DX (new; observable) for raw coefficients. No beta-min.

## Precise statement
In R1 under G, R, there is a fixed C < ∞ such that:
(i) [fallback; secondary] Π†(‖Xθ − μ‖²/n > Cε_{2,n}² | y) → 0 in P₀-probability.
(ii) Under SE: Π(|S| > d_* | y) → 0; prediction contracts at ε_{1,n}²; and Π†(‖θ − θ*‖² > Cε_{1,n}²/φ₀² | y) → 0.
(iii) For the applicable ε_n and every deterministic u_n → ∞: Π†(|v/σ*² − 1| > C[ε_n² + u_n/√n] | y) → 0 (v on the contrast scale).
(iv) Under DX, the raw coefficient error D_x⁻¹(θ − θ*) has the rate of (ii) multiplied by d₋⁻².
Not claimed: beta-min; out-of-sample, intercept-posterior or empirically centred random-design Hellinger results.

## Dependencies
Builds on: T01, T02. Used by: T08; interpretation of computational accuracy (T26).

## Numerical evidence (provisional)
None numerical; provisional evidence (Sol check J1) identifies the transfer obligations (judge/sol1/J1_TARGET_TRANSFER.md).

## Proof-route hint (optional)
First restrict posterior dimension to O(log n) supports by T02(i) (and to d_* under SE); their unions with S₀ are eventually feasible under the cap, so all comparisons stay inside Ω (no out-of-cap augmentation argument). Transfer the project master theorem (proofs/T9_C9/PROOF.md §§5, 9; paper_draft T9/T9a): ridge approximation error of the slab nv(G_S+I)⁻¹, superset completion, dimension-parametrised prediction bound; conditional Gaussian and IG tails for (iii) through T01's joint domination; back-transform for (iv). Hardest step: uniform residual and variance control with the empirical rate and the shared ‖y_c‖² fluctuation. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
