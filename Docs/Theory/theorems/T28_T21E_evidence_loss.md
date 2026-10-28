# T28 (T21-E): Evidence loss under calibration avoidance and evidence coupling

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** conditional negative comparison; **core**.

## Definitions used
Data-measurable hidden set 𝓜 with ∅ ∉ 𝓜; W = 𝓜ᶜ; 𝒮_cal; the reflected comparator of T17 (iid π₀(·|W) starts, same frozen grid, full initial normaliser); r_W = π(W)/π₀(W); coupling failure h_n^E; final E2 (island dispersion of log Ẑ_r), calibration E2 and flags; r_k (T10).

## Assumptions
EX-A, EX-S, CAL; calibration avoidance 𝒮_cal ∩ 𝓜 = ∅ and CPL-E through the last weight evaluation (MISS-E); T03's hypotheses only for the truth/superset consequences.

## Precise statement
Conditional on a frozen 𝓒 with 𝒮_cal ∩ 𝓜 = ∅, under MISS-E with failure ≤ h_n^E:
(i) E_𝓒Ẑ_W = r_WZ and P_𝓒(Ẑ/Z > x) ≤ h_n^E + r_W/x for x > 0. Hence r_W → 0 and h_n^E → 0 give Ẑ/Z → 0 in conditional probability although E_𝓒Ẑ = Z (T12); if the comparator is relatively consistent, Ẑ/Z = r_W(1 + o_P(1)). Joint-probability conclusions need the calibration and parameter events to hold with probability → 1.
(ii) A valid sufficient coupling bound is h_n^E ≤ 4N_eπ₀(Wᶜ) + Σ_eE_𝓒[1{τ > e⁻}K_e(X_{e⁻}, Wᶜ)] over all islands, particles and elementary executions; a large right-hand side does not establish failure.
(iii) [information scope] Only statistics measurable from coupled information transfer: final evidence dispersion (final E2) transfers when the island evidences are coupled; calibration E2 and calibration flags are fixed under the conditioning; final score-based E1, local-search E3 and PIPs need more than this coupling (T29).
(iv) [consequences under T03] r_W → 0 forces S₀ ∈ 𝓜 with probability → 1 (otherwise r_W ≥ π(S₀)); if r_W ≤ e^{−cn}, T10's polynomial addition floors force every feasible S₀ ∪ P, |P| fixed, into 𝓜 on the truth-concentration event. No bridge-temperature threshold is retained. No production family satisfying avoidance and coupling is established (open).

## Dependencies
Builds on: T09, T12, T13, T10, T17. Used by: T30, T31.

## Numerical evidence (provisional)
provisional evidence (Sol check J8): normalisation (comparator mean r_WZ, not Zπ(W)) and the information-transfer corrections; no actual v3 loss family was produced. provisional evidence (Sol check J12): the constructed two-cancellation instance scored S₀ in the pilot, so it is not an instance.

## Proof-route hint (optional)
Preserve restricted targets by elementary reflection; retain the correct initial normalisation; Markov; grid equality from unchanged candidate scores and frozen pilot targets (T13(iv)). Hardest step: exhibiting an actual regression family satisfying avoidance and coupling. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
