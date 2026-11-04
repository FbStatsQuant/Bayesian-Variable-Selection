# T12 (T8): Frozen-run evidence and recorded-RB identities

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** algorithmic validity; **core** (theorem).

## Definitions used
Stage notation q_t, Z_t, q̂_{r,t}, Ẑ_{r,t}; the final run (4 islands × N_e, multinomial resampling after every reweighting, one round per stage, L burn-in + 4 measured rounds); PIP̂_{rj} = pre-draw Gibbs conditionals averaged over particles and the 4 measured rounds; pooled Ẑ = ¼Σ_rẐ_r; primary/secondary PIPs (00_COMMON §2).

## Assumptions
EX-A, EX-S, CAL; prescribed multinomial resampling and independent particle mutations.

## Precise statement
Conditional on a successful 𝓒, for every island r, N ≥ 1, stage t and bounded fixed f:
(i) E[Ẑ_{r,t}q̂_{r,t}(f)] = Z_tq_t(f); in particular EẐ_r = Z. Appending terminal invariant rounds with unit potentials preserves the identity; it holds at fixed elementary prefixes and immediately before a specified Gibbs label in a state-independent random permutation; not at arbitrary state-dependent stopping times.
(ii) For the actual pre-draw RB recordings: E[Ẑ_r PIP̂_{rj}] = Z·PIP_j.
(iii) For the pooled evidence: EẐ = Z; E log Ẑ ≤ log Z; P(Z ≥ αẐ) ≥ 1 − α for 0 < α < 1 (Jensen also islandwise).
(iv) Primary and secondary normalised PIPs and log Ẑ are not unbiased in general. Conditional island independence holds given 𝓒, not necessarily after averaging over shared calibration. Averaging over a 𝓒-measurable launch event preserves evidence unbiasedness; conditioning on favourable final diagnostics does not guarantee any of (i)–(iii). NUM alone supplies no unbiasedness or Markov guarantee for implemented floating-point evidence.

## Dependencies
Builds on: T09; project P7/P11. Used by: T14, T15, T16, T17, T19, T25, T28, T31.

## Numerical evidence (provisional)
provisional evidence (Sol check J2): exact weighted-law propagation (N = 1, T = 1, 2, 3, through terminal resampling, burn-in and measured rounds with pre-draw rewards): max relative residual of EẐ = Z and E[Ẑ PIP̂_j] = Z·PIP_j is 1.3·10⁻¹⁵. Files: judge/sol2/J2_EXACT_IDENTITIES.md.

## Proof-route hint (optional)
Induct on the unnormalised empirical measure through weighting, resampling and mutation (Feynman–Kac unbiasedness); append unit-potential invariant kernels; treat the pre-coordinate reward as a marked transition and replace the indicator by o_j (project P11); tower property. Hardest step: the recording position within a round; terminal indicators cannot replace recorded conditionals. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
