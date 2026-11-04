# T02 (A1 = T2): Dimension control and exclusion of strict supersets

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** posterior consistency with rates; **core** (lemma).

## Definitions used
Target π, cap K, Ω (00_COMMON §1); r_n = √(log n/n); m_n(ω) = ⌈(s₀ log(2p) + (s₀+1)(log n)/2 + ω)/log 2⌉; regime R1 (n → ∞, s₀ fixed, p ≤ n^A).

## Assumptions
G (standard/project), R (project bundle); SE (project; strong) only for the superset clause.

## Precise statement
In R1 under G, R:
(i) For every deterministic ω_n → ∞ with ω_n = O(log n): Π(|S| > m_n(ω_n) | y) = O_{P₀}(e^{−ω_n}). More precisely, for each deterministic integer threshold m,
  Π(|S| > m | y) ≤ 2^{−m}(2p)^{s₀}(n+1)^{s₀/2}√n·Θ_{n,m},  with lim_{L→∞} limsup_n sup_m P₀(Θ_{n,m} > L) = 0.
A tight simultaneous sup_m Θ_{n,m} is not claimed. No eigenvalue condition near the cap is imposed.
(ii) Under SE in addition: Π(S ⊋ S₀ | y) = O_{P₀}(r_n).

## Dependencies
Builds on: T01 (transfer). Used by: T03, T04, T05, T08, T20 (margins), T23 (basin instances).

## Numerical evidence (provisional)
None numerical. provisional evidence (Sol check J1): the line-level transfer ledger (judge/sol1/J1_TARGET_TRANSFER.md) lists every changed bound (noise dimension n−1, eigenvalue normalisation, ridge remainder, determinant lower bound, IG shape/rate, cap augmentation); full statistical transfer remains unresolved.

## Proof-route hint (optional)
Contrast coordinates with T01(ii): numerator sums at the fixed rate b₋, where m^c_{b₋} is a proper density in y_c and the Markov identity E₀[Σ_{S∈𝒜}ϖ(S)m^c_{b₋}(S)/f₀(y_c)] = ϖ(𝒜) is exact; denominator at b₊ through S₀ with the (n−1)-norm Occam penalty n^{−(s₀+1)/2}; the geometric BB size tail (project L6); for (ii), size-by-size summation of truncated Gaussian projection moments over supersets with BB multiplicity cancellation and the (n+1)^{−1/2} determinant penalty, restricted to |S| ≤ m_n by (i). Hardest step: uniform integrated-variance control after the contrast/rate transfer; untruncated critical exponential moments cannot replace it. Transfer sources: paper_draft T6–T7; proofs/T7_T8/PROOF.md §§3–4. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
