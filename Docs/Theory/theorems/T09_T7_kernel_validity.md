# T09 (T7): Exact start, invariant kernels and whole-round minorisation

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** algorithmic validity and convergence; **core** (proposition).

## Definitions used
Blocks, tables r_b, γ₀, Z̄₀, π₀, backward sampler; d, γ_φ, q_φ, Z̄_φ; round K_φ with m = p + B + 2 labelled steps (Gibbs, uniform swap, B neighbour swaps on the symmetric-union graph N(·), independence proposal from π₀), elementary kernels K_e, realised-order kernel K_σ; ε_φ := inf_S π₀(S)/q_φ(S) (00_COMMON §2).

## Assumptions
EX-A, EX-S (declared idealisations); the actual tables, cap and move rules.

## Precise statement
For every valid component input and every φ ∈ [0, 1]:
(i) Convolving the actual block size profiles with the capped size prior gives Z̄₀ exactly; the backward sampler returns exact iid π₀ draws.
(ii) Each elementary kernel is q_φ-reversible, including the boundaries: addition at |S| = K has Gibbs probability 0; the uniform swap self-loops at |S| ∈ {0, p}; the neighbour-swap reverse ratio reads 0 when the reverse insertion is not a neighbour; the stated Hastings ratio supplies the reverse proposal probability.
(iii) K_φ = (1/m!)Σ_σ K_{σ(1)}⋯K_{σ(m)} is q_φ-invariant and self-adjoint on L²(q_φ). An individual realised order need not be reversible.
(iv) Every realised order satisfies K_σ(x, ·) ≥ ε_φ q_φ(·) with ε_φ = (Z̄_φ/Z̄₀)e^{−φ max_S d(S)} > 0; hence ‖K_φ^h(x,·) − q_φ‖_TV ≤ (1 − ε_φ)^h and the averaged round's absolute L² gap is ≥ ε_φ.
(v) ε_φ ≤ π₀(S)/q_φ(S) for every S. An exponentially small available minorisation constant does not establish exponentially slow mixing of the hybrid kernel; neither a switch nor a large discrepancy range alone supplies such a lower bound.

## Dependencies
Builds on: method §§6.3–6.5; project P1/P6. Used by: T10–T19, T23, T25, T28, T29, T36.

## Numerical evidence (provisional)
provisional evidence (Sol check J2): n = 6, p = 4, K = 3, B = 2: element and round detailed-balance residuals ≤ 2.2·10⁻¹⁶ at φ ∈ {0, ½, 1}; minorisation constants 1, 0.786, 0.619 with nonnegative slack (−1.1·10⁻¹⁶ roundoff at φ = 0); addition ratios ≥ 1.09 × floor. Files: judge/sol2/J2_EXACT_IDENTITIES.md, J2_matrices.npz.

## Proof-route hint (optional)
Sum block profiles; verify detailed balance including boundaries; pair each ordering with its reversal for self-adjointness; the independence kernel minorises q_φ (K_ind(S,S′) ≥ π₀(S′)min{1, w(S′)/w(S)} ≥ q_φ(S′)/sup w, w = q_φ/π₀) and its stochastic prefix and invariant suffix preserve the minorisation. Hardest step: boundary and Hastings bookkeeping. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
