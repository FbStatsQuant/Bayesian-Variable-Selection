# T29 (T21-H): HPM loss requires scoring avoidance; PIP loss requires reward control

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** conditional negative comparison; **secondary**.

## Definitions used
Hidden set 𝓜 as in T28; S†; first score time τ of 𝓜 over chronological opportunities with hazards p_e; stopped count O; μ_j^W = π(·|W)(o_j(·,1)) (T17(iv)); falling factorial (p+B+2)_h; h = |T Δ S₀|.

## Assumptions
EX-A, EX-S, CAL, SR; MISS-H (calibration avoidance plus avoidance of every subsequent scoring opportunity, failure h_n^H); a reward-preserving coupling for PIP/diagnostic transfer; clause (iv) adds G, R (and T24's hypotheses for its last sentence).

## Precise statement
(i) If calibration avoids 𝓜, S† ∈ 𝓜, and MISS-H gives an event of probability ≥ 1 − h_n^H on which every subsequent scoring route avoids 𝓜, then P_𝓒(Ŝ = S†) ≤ h_n^H. State coupling alone does not establish this event.
(ii) [first score] P_𝓒(τ ≤ H) = Σ_eE_𝓒[1{τ > e⁻}p_e]; iid opportunities contribute ≤ Q_fπ₀(𝓜); a feasible hidden Gibbs alternative is scored with certainty at its execution; swap proposals score before acceptance; a random local-search centre contributes an expected indicator; for predictable opportunities with hazard ≥ b, P(no hit, O ≥ D) ≤ (1−b)^D. These quantified conditions replace distance or "protection" classifications.
(iii) [PIPs] A coupling through measured trajectories must preserve the original RB rewards or supply a discrepancy allowance; the reflected target mean μ_j^W generally differs from π(j ∈ S|W); neither finite-budget accuracy for μ_j^W nor PIP failure follows from reflection alone; a PIP-loss conclusion needs comparator accuracy plus separation from the full-target PIP, or a direct comparator error bound.
(iv) [bounded-state accessibility sub-conjecture] Under G and R, for fixed d, uniformly over |T| ≤ d with |T ∪ S₀| ≤ K, an additions-first, deletions-second Gibbs path to S₀ at φ = 1 has probability ≥ n^{−C′}: additions use T10's floors; deletions after completing truth are proposed to have log-score loss ≤ C log n uniformly over bounded supersets (obligation); prescribing the h coordinate labels first, in order, costs 1/(p+B+2)_h. This is polynomial accessibility, not discovery at the actual budget. Under T24's hypotheses and eligible occupancy, T24 instead gives high-probability discovery and excludes the corresponding MISS-H instance.

## Dependencies
Builds on: T10, T11, T17, T24. Used by: T31.

## Numerical evidence (provisional)
provisional evidence (Sol check J8): scoring and reward distinctions (rejected proposals scored outside W with probability 0.294; original RB mean 0.26 vs restricted PIP 0); hand counts at n = 200, p = 500: full-execution-occupancy entry floor ≈ 18.4 (k = 1), 55.3 (k = 5); unconditional ordering floor 0.036. provisional evidence (Sol check J12): discovery during an incomplete pilot prefix only.

## Proof-route hint (optional)
All-scored decision rule plus the first-hit ledger (T11); transfer only statistics represented in the coupling (T17); for (iv) control Gaussian projection gains after truth completion and prescribe the finite path. Hardest step: constructing a genuine loss family. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
