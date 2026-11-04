# T15 (L-OCC): Occupancy from an evidence lower tail

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** algorithmic convergence (source of BASIN's δ); **core** (lemma).

## Definitions used
Island evidence Ẑ_r; f_r(𝔄ᶜ) = the fraction of island r's particles outside a set 𝔄 (fixed given 𝓒) at stage T or at a fixed terminal recording prefix (as in T12(i)); W := Ẑ_r/Z.

## Assumptions
EX-A, EX-S, CAL; prefixes as specified in T12.

## Precise statement
Conditional on a successful 𝓒, for every c, u ∈ (0, 1):
  E f_r(𝔄ᶜ) ≤ min{1, π(𝔄ᶜ)/c + P(Ẑ_r/Z < c)},  P(f_r(𝔄ᶜ) > u) ≤ π(𝔄ᶜ)/(cu) + P(Ẑ_r/Z < c).
If E|Ẑ_r/Z − 1| ≤ B then the lower-tail term is ≤ B/(1−c). These are calibration-conditional bounds; conditional on an already realised population its actual outside fraction must be used. The lower tail must be islandwise; a pooled-evidence lower tail does not substitute.

## Dependencies
Builds on: T12 (and optionally T14 or T25 for the lower tail). Used by: T23, T24, T26.

## Numerical evidence (provisional)
provisional evidence (Sol check J6): exact finite-particle check of E[Wf] = π(𝔄ᶜ) (weighted fraction 0.01980 = target outside 0.01980) and of the linear bound. Files: judge/sol2/J6_FIRST_MOMENTS.md.

## Proof-route hint (optional)
T12(i) with f = 1_{𝔄ᶜ} gives E[Wf_r] = π(𝔄ᶜ); split at W = c using 0 ≤ f_r ≤ 1; Markov for the probability bound. No substantive hardest step; the content is the lower-tail input. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
