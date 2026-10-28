# T05 (A4 = T5-S): Orthogonal threshold and benchmark gap

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** sharp consistency boundary and limit result; **secondary** (theorem).

## Definitions used
Global HPM S†; D_S, Q_S, z_j (00_COMMON §1). λ_n = (n−1)b_n²/σ*²; τ_n = log n + 2 log((2p_n − s₀)/s₀). Φ = standard normal cdf. "Known-size, known-noise selector": the top-s₀ absolute-statistic selector that knows s₀ and σ*.

## Assumptions
G, R (project); ORTH (project benchmark: G = (n−1)I_p, so p ≤ n−1; fixed 1 ≤ s₀ < p; equal magnitudes b_n on S₀; b_n²/σ*² bounded). No beta-min. Not a p > n result.

## Precise statement
Under G, R, ORTH:
(i) [exact identities] D_S = n^{|S|} and Q_S = yᵀy − n⁻¹Σ_{j∈S}z_j². The exact addition log-odds are log[(k+1)/(2p−k−1)] − ½ log n + ν log[(0.02+Q_S)/(0.02+Q_S−z_j²/n)].
(ii) [threshold] If √λ_n − √τ_n → c ∈ [−∞, ∞], then P₀(S† = S₀) → Φ(c)^{s₀}.
(iii) [gap] If p_n − s₀ → ∞, every signal sequence with √λ_n − √(2 log(p_n−s₀)) → ∞ and √τ_n − √λ_n → ∞ is recovered by the known-size, known-noise selector with probability → 1 while v3's global HPM fails with probability → 1. Such sequences exist, since τ_n − 2 log(p_n−s₀) = log n + 2 log(2/s₀) + o(1); e.g. λ_n = (1−ε)τ_n with 0 < ε < 1/(1+2A); at p ≍ n^a the gap is [√(1+2a) − √(2a)]√(log n) to leading order. No minimax theorem is adopted.

## Dependencies
Builds on: T01, T02. Used by: T21 (interpretation), T31.

## Numerical evidence (provisional)
provisional evidence (Sol check J11): orthogonal n = 40, p = 6: max errors of log D, Q and neighbour log-odds ≤ 1.4·10⁻¹⁴; all top-k rankings match enumeration; deterministic gap evaluations (e.g. log n = 1000, p = n^{0.75}: √-gap 11.27). The single seed does not estimate Φ(c)^{s₀}. Files: judge/sol1/J11_TARGET_BOUNDARIES.md.

## Proof-route hint (optional)
Preserve exact top-k rankings; control the selected size and supersets by T02 in orthogonal form; transfer the project order-statistic argument (Pb1) through T01; at the transition the integrated-variance error in the squared statistic must be o_P(√τ_n), not merely relative o_P(1); candidate local remainder O_P(log n/√n + log²n/n); oracle half via Gaussian maxima; the v3 half is (ii) with c = −∞. Hardest step: the selected-size/order-statistic sandwich with a remainder negligible on the square-root scale. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
