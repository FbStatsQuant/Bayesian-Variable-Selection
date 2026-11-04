# T19 (T12): Conservative working-set bounds with explicit reward targets

**Status:** conjectured, not proven (a new judge conjecture, not numerically validated). Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** finite-budget algorithmic convergence; **optional** (theorem).

## Definitions used
Reflected comparator on W (T17) with Z_W° = Zr_W; normalised semigroup 𝒬^W_{s,t} = ∏(g_j^WK_j^W) with g_t^W normalised by the restricted normaliser ratio; PIP̂^{W,orig}_{rj} (original Gibbs rewards averaged over the measured rounds); μ_j^W (T17(iv)); b_W = max_j|μ_j^W − PIP_j| ≤ π(Wᶜ); V_Z = (1 + a²/N)^T − 1; V_R = (1 + a²/N)^{T+1} − 1.

## Assumptions
EX-A, EX-S, CAL; the normalised future-weight component of WS: sup_{0≤s<t≤T}sup_{x∈W}𝒬^W_{s,t}1(x)/q_s^W(𝒬^W_{s,t}1) ≤ a ≥ 1 (BW_W sufficient with a = C₀); CPL-E (failure h_E) and a measured-path coupling preserving original rewards (failure h_P) for actual outputs; warmness and gap only for the terminal-chain clause.

## Precise statement
(i) E(Ẑ_r^W/Z_W° − 1)² ≤ V_Z; E[(Ẑ_r^W/Z_W°)²(PIP̂^{W,orig}_{rj} − μ_j^W)²] ≤ V_R; hence E(PIP̂^{W,orig}_{rj} − μ_j^W)² ≤ 4(V_Z + V_R), also for primary pooling (no variance division by four for possibly biased normalised estimates).
(ii) [actual outputs] P(|Ẑ/Z − 1| > |r_W − 1| + x) ≤ h_E + r_W²V_Z/(4x²); P(max_j|PIP̂_j − PIP_j| > b_W + x) ≤ h_P + 4p(V_Z + V_R)/x² (clipped at one; a logarithmic dependence on p would need a further concentration argument).
(iii) [terminal chain] If λ ≤ wπ(·|W) and K₁^W has absolute gap g: ‖λ(K₁^W)^L − π(·|W)‖_TV ≤ ½√(w−1)(1−g)^L; over H terminal rounds a sufficient single-chain exit bound is Hmwπ(Wᶜ)/π(W). This does not establish a coupling for the tempering/resampling particle system.
(iv) Full-space WS is not universally impossible (constant discrepancy is a benign case); conversely none of these bounds establishes useful constants for a specified crossing family. The v2 logarithmic-uniform concentration rate is withdrawn.

## Dependencies
Builds on: T09, T12, T17. Used by: T25 (alternative comparator bound), T26 (optional alternative).

## Numerical evidence (provisional)
provisional evidence (Sol check J8, J10): the normalisation, reward and particle-control gaps of the v2 formulation (d ≡ 0 satisfies full-space future-weight stability). The displayed bounds themselves were not checked.

## Proof-route hint (optional)
Unnormalised particle martingale decomposition; local sampling variance ≤ a²EW_s²/N giving the geometric second-moment bound; attach each particle's terminal trajectory and bounded RB average as a marked final mutation and apply the same decomposition to the centred reward; denominator split at ½; convexity; T17 for the transfer. Hardest step: checking the marked-particle decomposition and its constants uniformly over the semigroup family. External nonasymptotic SMC precedents UNVERIFIED. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
