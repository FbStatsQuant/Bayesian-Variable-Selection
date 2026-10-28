# T36 (R-T13): The pilot limit as a finite-comparison rule

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** convergence of an idealised pilot (remark-level statement with provable content); **secondary**.

## Definitions used
The pilot: empirical-ESS bisection with threshold 0.9, 60 halvings, floor 1/T_e, stage ceiling T_e, forced steps; population ESS fraction ρ(u, v) = Z̄_v²/(Z̄_uZ̄_{2v−u}); candidate set V; the candidate-grid construction (retains every pilot temperature) (00_COMMON §2; THEORY_BRIEF §2).

## Assumptions
EX-A, EX-S; NDR (new nondegeneracy); the frozen-ceiling idealisation (H → ∞ with T_e, floor, bisection depth and all other pilot rules fixed).

## Precise statement
Let H → ∞ with everything else fixed. Under NDR, the empirical pilot schedule, its stage count and its forced-step indicators equal, with probability → 1, those of the deterministic rule that applies the same floor and bisection to the population ESS fraction ρ(u, v) at its comparisons. For any frozen V, a successful candidate-grid construction retains every pilot temperature; under EX-A, equality of rebuilt grids means equality of the exact outputs of the finite-comparison rule. This does not establish stabilisation of the data-dependent candidate set, a bounded stage count, or completion of the whole calibration loop.

## Dependencies
Builds on: T09; finite-state LLN. Used by: T34 (schedule discussion).

## Numerical evidence (provisional)
None.

## Proof-route hint (optional)
Induct over the finite comparison tree: once previous comparisons agree, the next tested temperatures coincide; the finite-space particle LLN and NDR give the next agreement with probability → 1; maintain the induction through resampling and the exploratory floor. The external adaptive-tempering precedent (Beskos et al. 2016) is UNVERIFIED and not needed. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
