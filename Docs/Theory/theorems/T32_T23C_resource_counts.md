# T32 (T23-C): Branch-specific arithmetic and storage counts

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** complexity; **core** (proposition candidate).

## Definitions used
Budgets N_e, H_e, T_e, L, ℓ (00_COMMON §2); m = p + B + 2; k_* = min(K, ⌊p/2⌋); s(K) = O(nK² + 1) per score; Q_all = all start and independence draws; E = Σ_{k≤K}C(p,k); the exact-branch inequality.

## Assumptions
The stated arithmetic/storage model and the fixed budgets. Bit complexity, wall time and numerical validation are separate.

## Precise statement
(i) [score ceiling, SMC branch] C_score ≤ Σ_b2^{|C_b|} + Σ_{e=0}^1(1+4ℓ)H_e[1 + 2m(T_e+L+4)] + 4N₁[1 + 2m(T₁+L+4)] + (8ℓ+3)(ℓ+1)[p + k_*(p−k_*)], with Σ_b2^{|C_b|} ≤ p2^B/B; both Gibbs alternatives and the larger final tier are counted.
(ii) Convolution O(pK); iid-sampler work ≤ O(Q_all p2^B) for a conservative implementation; each grid construction uses O(60T_e) log-sum-exp calls and O(60|V|T_e) scalar-term work, at most 2(ℓ+1) constructions; Gram O(np²); clustering polynomial, with a conservative O(p⁴) for an exhaustive lexicographic implementation (the sharper O(p²log p) needs an implementation audit). Total arithmetic work is polynomial in (n, p).
(iii) [storage] Sequential islands with sparse model keys, scalar score caches and active particle factors: O(np + p² + p2^B + pK + N₁K² + nK) words on the SMC branch; a streaming exact implementation uses O(np + pK + nK + K²) words and E scores, with E = O(N₀p) on that branch. These are implementation contracts, not lower bounds for every implementation. The method's scan bound K(p−K) is corrected to max_{k≤K}k(p−k).

## Dependencies
Builds on: method §§6, 8. Used by: T34.

## Numerical evidence (provisional)
provisional evidence (Sol check J9): baseline upper count at n = 200, p = 500: labelled rounds 5.19·10⁸, score evaluations ≤ 5.35·10¹¹ (two per labelled step), local searches 83, scan evaluations ≤ 3.70·10⁷; branch decisions for n = 3…6 with symbolic p. Files: judge/sol1/J9_RESOURCES_GRID.md.

## Proof-route hint (optional)
Count both tiers, diagnostic rebuilds, labelled rounds and scans; document live arrays and exact-sampler operations. Hardest step: peak storage and the clustering implementation audit. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
