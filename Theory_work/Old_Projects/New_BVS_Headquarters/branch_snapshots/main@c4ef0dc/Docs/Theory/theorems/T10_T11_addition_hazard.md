# T10 (T11): Feasible-addition hazards and ordered paths

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** algorithmic convergence and accessibility; **core** (lemma).

## Definitions used
γ_φ, q_φ, π₀, Gibbs conditional o_j(S, φ), the random-order round with m = p + B + 2 labels, execution-time state X_{e⁻} (state immediately before elementary step e) (00_COMMON §2). r_k := (k+1)/((2p−k−1)√(n+1)); h_k := r_k/(1+r_k).

## Assumptions
EX-A, EX-S. SR only when a Gibbs evaluation is translated into a scoring event (via T11).

## Precise statement
For S ∈ Ω with k = |S| < K, j ∉ S, and every φ ∈ [0, 1]:
(i) γ_φ(S+j)/γ_φ(S) ≥ r_k; o_j(S, φ) ≥ h_k; π₀(S+j) ≥ r_kπ₀(S).
(ii) [ordered path] If a round starts at S, J ∩ S = ∅, |J| = a, k + a ≤ K: P(visit S ∪ J during the round | S) ≥ C(m,a)⁻¹∏_{i=0}^{a−1}h_{k+i} (the event that the first a labels are those of J). The unconditional one-addition bound carries the ordering factor 1/m; the v2 clause "no ordering constant for a = 1" is false.
(iii) [execution time] At an actual execution of coordinate j with current state S, conditional on the whole past, the addition probability is o_j(S, φ) ≥ h_k; the expected number of such entries is Σ_e P(X_{e⁻} = S)o_j(S, φ_e) ≥ h_kΣ_e P(X_{e⁻} = S).
(iv) These are visit/entry statements, not terminal-occupancy statements. A fixed-length addition path is inverse-polynomially accessible in polynomial-dimensional regimes; this does not establish discovery within the declared budget. No feasible addition is counted beyond the cap.

## Dependencies
Builds on: score formulas, T09. Used by: T11, T17, T21, T22 (deterministic clause), T24, T27, T28, T29, T30.

## Numerical evidence (provisional)
provisional evidence (Sol check J8): complete hybrid round at n = 200, p = 4, start {i} with o_i ≈ 0 and orthogonal j: full-hybrid visit probability 0.0147 < one-step execution conditional 0.0660 ≥ floor 0.0659 (ordering factor confirmed; endpoint occupancy 6.9·10⁻⁷). provisional evidence (Sol check J2): addition ratios ≥ 1.09 × r_k on the test data.

## Proof-route hint (optional)
Q_{S+j} ≤ Q_S by push-through monotonicity of t_S; 1 ≤ D_{S+j}/D_S ≤ n+1 by a Schur complement; the same bound for the affected block table; interpolate the two likelihood ratios with exponents 1−φ, φ; multiply by the exact prior ratio w(k+1)/w(k) = (k+1)/(2p−k−1). (ii): probability of the order of the first a labels; (iii): condition on the realised prefix. Hardest step: the execution-time occupancy interpretation, not the algebra. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
