# T27 (T20-C): Sequential cancellation and the iid-discovery budget

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** computational limit; **secondary** (corollary).

## Definitions used
Tables r_b; π₀; Q_f with 4N_e(L+6) ≤ Q_f ≤ 4N_e(T_e+L+5); r_k (T10); p ≍ n^a; a completion chain S^{(0)} ⊂ S^{(1)} ⊂ ⋯ ⊂ S^{(c)} = S₀ of feasible successive additions with fixed c and fixed starting size, b_i the block of the i-th added coordinate.

## Assumptions
EX-A, EX-S, CAL, successful final execution; the sequential ratio law: r_{b_i}(S^{(i+1)}∩C_{b_i})/r_{b_i}(S^{(i)}∩C_{b_i}) = n^{−1/2}e^{O_{P₀}(1)} jointly over i; π₀(S^{(0)}) ≥ c₀ > 0 with probability → 1. G and R alone do not establish these.

## Precise statement
(i) [mass law] π₀(S₀) = p^{−c}n^{−c/2}e^{O_{P₀}(1)}.
(ii) [budget exponent] The polynomial exponent of Q_fπ₀(S₀) is β = max(1, a) − c(a + ½). If β > 0, iid discovery tends to certainty; if β < 0 its probability tends to zero; if β = 0 the guaranteed logarithmic factor and the tight reciprocal mass multiplier give discovery under the stated ≍ and tightness assumptions. One cancellation is iid-cheap at p ≍ √n.
(iii) [scales] π₀(S₀) ≫ [max(n,p) log n]⁻¹ suffices uniformly over successful schedules; π₀(S₀) ≪ [max(n,p) log²n]⁻¹ precludes discovery by the final iid draws; intermediate scales depend on the realised schedule.
(iv) Without the two-sided law, T10 gives only π₀(S₀) ≥ π₀(S^{(0)})∏_{i<c}r_{|S^{(i)}|}, which cannot establish expense. The former V_δ window needs an explicit normalised mass bound or a verified T22 comparison; its unqualified form is withdrawn. Small iid discovery probability says nothing about Gibbs, swaps or scans.

## Dependencies
Builds on: T10, T11, T22 (deterministic clauses). Used by: T21 (interpretation), T31.

## Numerical evidence (provisional)
provisional evidence (Sol check J7): exponent grid at n = 10⁸: a = 0.25 → +0.25 (Q_min·r₄ ≈ 3.4·10⁴); a = 0.5 → 0 (≈ 330); a = 0.75 → −0.25 (≈ 3.3); a ≥ 1 → −0.5 (≈ 0.033); a suppressor illustration with weak singletons and strong joint fit lies outside regular SE (min eigenvalue 0.0078). Files: judge/sol1/J7_DISCOVERY_BUDGETS.md.

## Proof-route hint (optional)
Telescope the exact table and prior ratios along the chain; apply T11(iii)'s iid miss formula with the budget bounds. Hardest step: the two-sided sequential law and control of the composite normaliser (initial-base cancellation does not justify multiplying initial ratios). *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
