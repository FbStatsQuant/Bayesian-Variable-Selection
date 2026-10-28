# T23 (T18): Basin-to-output guarantee with recording-prefix control

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** conditional algorithmic convergence; abstract theorem (i)–(iv): **core**; conditional instances (v): **secondary**.

## Definitions used
Final-run terminal rounds (L burn-in + 4 measured) at φ = 1; f_H(S₀ᶜ) = fraction of an island's particles outside S₀ after H terminal rounds; B_{i,h} = indicator that particle i is outside S₀ at some point during measured round h (including its start); B̄_r = (4N_e)⁻¹Σ_{h=1}^4Σ_iB_{i,h}; PIP̂_{rj}, primary average; u_π = δ₁/π(S₀); ρ_* = min{1,(B+3)u_π}; BASIN(𝓡, r₀, a, η, ρ, δ) (inventory); 𝔓 = {S̃₀, S₀}.

## Assumptions
EX-A, EX-S, CAL, BASIN; T03's hypotheses supply statistical truth stability; the instances in (v) need their own exit, gain and initial-population hypotheses.

## Precise statement
(i) For one island, after H terminal rounds: E_𝓒 f_H(S₀ᶜ) ≤ δ + (1−a)^{⌊H/r₀⌋} + H(η + ρ). Conditioning on the realised initial population replaces δ by its actual outside-basin fraction.
(ii) [pathwise RB bound] max_j|PIP̂_{rj} − 1{j ∈ S₀}| ≤ B̄_r + max_j|o_j(S₀,1) − 1{j ∈ S₀}| ≤ B̄_r + u_π. Hence for the primary average, E_𝓒 max_j|PIP̂_j^{primary} − 1{j∈S₀}| ≤ δ + (1−a)^{⌊L/r₀⌋} + (L+4)(η+ρ) + u_π =: 𝓑_n; no particle independence and no union over p coordinates is needed; the conditional MPM error probability is ≤ 2𝓑_n.
(iii) [truth stability] For the actual hybrid round, ρ ≤ ρ_*: the Gibbs first-departure probabilities sum over distinct one-flip neighbours, and each of the B+2 other labels contributes ≤ u_π by reversibility.
(iv) [initial occupancy] T15 supplies δ ≤ π(𝓡ᶜ)/c + P_𝓒(Ẑ_r/Z < c), 0 < c < 1, with a per-island lower tail.
(v) [conditional instances] For either single-flip form of ONE, if the actual one-round first-exit probability from 𝔓 is uniformly ≤ η_𝔓, reflection and T18 give the candidate entrance bound a ≥ π(S₀|𝔓) − η_𝔓; the pair is useful when (L+4)η_𝔓 → 0 and the initial-population condition holds. For a proxy swap, the natural basin {proxy state, S₀, S₀ ∪ proxy} needs verified entrance and exit bounds, or T24's 𝓡₁. ONE and TL_avg alone establish neither basin claim.

## Dependencies
Builds on: T03, T09, T12, T15, T18. Used by: T24, T26, T31. T25 may supply the per-island lower tail.

## Numerical evidence (provisional)
provisional evidence (Sol check J4): labelled-round enumeration (n = 8, p = 4) confirms the first-exit partition (residual 2.2·10⁻¹⁶) and that end-of-round fractions alone do not give the pathwise RB bound (max visit-minus-endpoint 0.578). provisional evidence (Sol check J6): occupancy identity. Files: judge/sol2/J4_REPAIR_BASIN.md.

## Proof-route hint (optional)
Blockwise entrance trials over ⌊H/r₀⌋ blocks; separate basin exits from truth departures; bound measured rewards by whole-round bad-path indicators (a pre-coordinate fraction is bounded in expectation by its round-start fraction plus truth's prefix-departure probability); T12 and T15 for the initial occupancy. Hardest step: deriving a useful basin for the actual mixed-label kernel. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
