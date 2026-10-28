# T17 (L-RC): Reflection with output-specific coupling

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** algorithmic validity and comparison device; **core** (lemma).

## Definitions used
Reflected elementary kernels K_e^W(x, A) = K_e(x, A∩W) + K_e(x, Wᶜ)1_A(x); reflected round; the reflected comparator run (iid q₀(·|W) starts, full initial normaliser m(∅)Z̄₀, same frozen grid and weights G_t); r_W = q₁(W)/q₀(W); first mismatch time τ; original Gibbs rewards o_j(·,1); μ_j^W := π(·|W)(o_j(·,1)) (00_COMMON §2; inventory CPL-E, CPL-H/RB).

## Assumptions
EX-A, EX-S, CAL; CPL-E, CPL-H or the RB condition when transferring the corresponding output.

## Precise statement
Fix nonempty W ⊆ Ω given 𝓒.
(i) Each K_e^W is q_φ(·|W)-reversible; the random-order reflected round is invariant and self-adjoint. The comparator's evidence has EẐ_r^W = Z·r_W (not Zq₁(W)).
(ii) [coupling] Couple each full initial draw with its conditional-W counterpart (agreeing when the full draw lies in W); while populations agree, share resampling and transition randomness. Up to the horizon relevant to the output, the failure probability satisfies h ≤ 4Nq₀(Wᶜ) + Σ_{r,i,e}E[1{τ > e⁻}K_e(X_{ri,e⁻}, Wᶜ)] (accepted exits at first occurrence; resampling causes no mismatch while populations and weights agree).
(iii) [transfer] For any statistic U measurable from coupled variables: |P(U ∈ A) − P(U^W ∈ A)| ≤ h. Under CPL-E: P(Ẑ/Z > x) ≤ h_E + r_W/x for x > 0. Evidence needs coupling only through its last weight evaluation; PIPs need the measured paths and the same reward function (or a reward-discrepancy allowance); HPM needs every scored proposal and scan. Rejecting an outside transition does not suppress its score.
(iv) [rewards] If original Gibbs rewards are retained in the reflected run, E[Ẑ_r^W PIP̂_{rj}^{W,orig}] = Z r_W μ_j^W, where in general μ_j^W ≠ π(j ∈ S | W), but |μ_j^W − PIP_j| ≤ π(Wᶜ).
(v) [hazard floor] For a boundary addition with hazard ≥ h_k, the stopped first-exit opportunities obey T11(iv), including P(failure) ≥ h_kEO. No blanket impossibility of coupling follows from a large union-bound upper bound or from a small stationary outside mass alone.

## Dependencies
Builds on: T09, T10, T11, T12. Used by: T18, T19, T25, T28, T29, T31.

## Numerical evidence (provisional)
provisional evidence (Sol check J8): reflected component on W = pair: original RB mean of a non-switching coordinate 0.2596 vs restricted PIP 0; rejected independence proposals scored outside W with probability 0.294 without an accepted exit (0.248). Files: judge/sol2/J8_EXPOSURE_COUPLING.md.

## Proof-route hint (optional)
Elementary detailed balance for the reflected kernels; T12 on restricted targets for the comparator mean; valid conditional-start coupling and first-failure decomposition; (iv): μ_j^W − PIP_j = π(o_j1_W)(1/π(W) − 1) − π(o_j1_{Wᶜ}), both terms bounded by π(Wᶜ). Hardest step: bounding the actual particle-system exit sum and preserving the output's rewards. External restricted-kernel precedents UNVERIFIED. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
