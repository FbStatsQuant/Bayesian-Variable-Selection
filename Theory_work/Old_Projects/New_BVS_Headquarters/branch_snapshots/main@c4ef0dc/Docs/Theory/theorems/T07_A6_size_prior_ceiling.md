# T07 (A6 = T5-C): Size-only ranking ceiling and Bayes decisions

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** decision validity and limits; **core** (proposition; near-verbatim transfer of project P3/P5).

## Definitions used
Global HPM S†, PIP_j, MPM (00_COMMON §1). For a size-only prior on Ω and a fixed tie order, S*_k := the tie-preferred maximiser of m(S) over |S| = k. Posterior 0–1 loss on supports; Hamming loss.

## Assumptions
A positive size-only prior on Ω and the specified decision/action space. No statistical assumption.

## Precise statement
(i) For any positive size-only prior with a fixed tie order: {S† = S₀} ⊆ {S*_{s₀} = S₀}. No size-only prior can repair a within-size likelihood ranking error.
(ii) The global HPM minimises posterior 0–1 loss on supports; the unconstrained MPM minimises posterior Hamming loss; the cap-constrained Hamming minimiser keeps the largest min(K, #{j : PIP_j > ½}) PIPs (boundary ties resolved deterministically).
(iii) These conclusions concern the target decisions; they do not automatically apply to the best scored model Ŝ or to estimated PIPs, which need their computational guarantees (T21, T23, T26).

## Dependencies
Builds on: target definitions. Used by: T05 (interpretation), T31.

## Numerical evidence (provisional)
None.

## Proof-route hint (optional)
Cancel the common within-size prior factor; minimise the posterior risks directly (project P3, P5 verbatim). No substantial hardest step. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
