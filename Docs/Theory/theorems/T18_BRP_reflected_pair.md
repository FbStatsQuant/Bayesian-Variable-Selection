# T18 (B-RP): Reflected single-flip pair benchmark

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** conditional algorithmic convergence (reflected process only); **secondary** (lemma).

## Definitions used
Single-flip pair 𝔓 = {S̃₀, S₀} with S̃₀ = S₀ Δ {j*}; reflected run at 𝔓 (T17(i)) with iid q₀^𝔓 starts and the original initial normaliser; q_t^𝔓 = q_t(·|𝔓); χ_t² = χ²(q_t^𝔓‖q_{t−1}^𝔓); r_𝔓 = q₁(𝔓)/q₀(𝔓); c_ε = 10/(9(1−ε_C)²) − 1; candidate set V; COVER(𝔓, ε_C).

## Assumptions
EX-A, EX-S, CAL; ONE in single-flip form; 𝔓 ⊆ V, every grid interval passing its restricted ESS test (ρ_V ≥ 0.9) and COVER(𝔓, ε_C) for the grid corollary.

## Precise statement
(i) In the reflected run every round is an exact refresh: K^𝔓_{φ_t}(x, ·) = q_t^𝔓(·) for x ∈ 𝔓 (the switching coordinate j*'s Gibbs step draws exactly from q_t^𝔓; all other reflected steps are invariant).
(ii) One island: Var(Ẑ_r^𝔓)/(Zr_𝔓)² = ∏_{t=1}^T(1 + χ_t²/N) − 1; four independent islands divide this by 4.
(iii) Under the grid corollary's hypotheses, for every x > 0: P(|Ẑ^𝔓/Z − 1| > ε_C/(1−ε_C) + x) ≤ [(1 + c_ε/N)^T − 1]/(4(1−ε_C)²x²).
(iv) This is a reflected-process statement. A proxy-swap pair lacks the switching refresh. Actual-run transfer needs its own coupling or particle argument; RET/OCC does not supply one. Original non-switching RB rewards retain T17(iv)'s distinct target mean.

## Dependencies
Builds on: T09, T13, T17. Used by: T23 (pair instance), T25 (benchmark).

## Numerical evidence (provisional)
provisional evidence (Sol check J6): exact pair laws: relative variance equals the product ∏(1 + χ_t²/N) − 1 to residual 0 (N = 1: 0.03953; N = 2: 0.01964); original-normaliser relative mean 1.0002; four-island factor verified. provisional evidence (Sol check J10): the product fails for lazy proxy-like and no-refresh kernels (relative variance 1.75 vs product 0.40).

## Proof-route hint (optional)
Exact refresh ⇒ stage populations are fresh iid samples ⇒ product formula for the relative second moment; T13 bounds χ_t² by c_ε; |r_𝔓 − 1| ≤ ε_C/(1−ε_C); Chebyshev. Hardest step: none beyond T13; transfer to the actual run is outside this lemma. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
