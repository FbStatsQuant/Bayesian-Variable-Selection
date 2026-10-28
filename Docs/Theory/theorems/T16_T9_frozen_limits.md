# T16 (T9): Frozen-particle and independent-island limits

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** algorithmic convergence and asymptotic normality (idealised families); **secondary** (theorem).

## Definitions used
Regime R3 (data and 𝓒 fixed; N or the island count varies); Ẑ_r, PIP̂_{rj}, primary and secondary pooling, island SD of log Ẑ_r (00_COMMON §2).

## Assumptions
EX-A, EX-S, CAL; finite state space, fixed schedule, independent particle/round randomness.

## Precise statement
(i) [particle family] Fix data and 𝓒 except the final particle count; retain T, L, V, tier and four islands. As N → ∞: Ẑ_r/Z → 1 and PIP̂_{rj} → PIP_j in probability; the joint vector of relative evidence, primary-PIP and secondary-PIP errors has a centred (possibly singular) √N-Gaussian limit with fixed-calibration mean-square errors O_𝓒(N⁻¹). Averaging over an N-independent calibration law gives a conditional-Gaussian mixture; no triangular-array production rate follows without uniform control of the constants.
(ii) [island family] Fix N, 𝓒 and construct independent islands. As R_isl → ∞: Σ_rẐ_rPIP̂_{rj}/Σ_rẐ_r → PIP_j a.s., with √R_isl-limit variance Var{Ẑ_r(PIP̂_{rj} − PIP_j) | 𝓒}/Z²; primary pooling converges to E[PIP̂_{1j} | 𝓒] ≠ PIP_j in general; the island sample SD of log Ẑ_r converges to its conditional population SD.
Both families are idealisations; production uses four islands and the two-tier budgets.

## Dependencies
Builds on: T09, T12. Used by: T31 (interpretation). Does not supply T26.

## Numerical evidence (provisional)
None.

## Proof-route hint (optional)
Finite-state multinomial LLN/CLT induction with the state augmented by the realised order (so the round is a Markov kernel) and bounded marked terminal rewards; delta method; T12 and iid island laws for (ii). Precedents (Del Moral–Doucet–Jasra 2006; Chopin 2004) UNVERIFIED; a direct finite-state proof is required. Hardest step: the joint covariance with genealogy and recording positions. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
