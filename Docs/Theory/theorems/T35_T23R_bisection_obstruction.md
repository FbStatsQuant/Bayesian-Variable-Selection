# T35 (T23-R): Mass-qualified fixed-bisection obstruction and the discrepancy range

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** finite-rule limitation; **optional** (corrected remark with provable content).

## Definitions used
The candidate-grid search (bisection toward b from u with 60 halvings, acceptance ρ_V ≥ 0.9); a two-state restricted law with higher-discrepancy mass a at u and discrepancy gap D; x = D(v−u); ρ(a, x) := [a + (1−a)e^{−x}]²/[a + (1−a)e^{−2x}]; J = number of blocks, J_max = min(K, J), ν = 0.01 + n/2; range(d) = max_S d(S) − min_S d(S).

## Assumptions
EX-A; the two-state restricted law for (i)–(ii); standardised valid inputs for (iii).

## Precise statement
(i) For the two-state law the restricted ESS fraction at step v is exactly ρ(a, x); it decreases from 1 toward a as x grows; a ≥ 0.9 always passes; for fixed x a sufficiently small a also passes.
(ii) [obstruction] If ρ(a, D(b−u)2^{−60}) < 0.9 (STIFF), every positive tested endpoint fails and the construction cannot accept any step toward b. A gap condition alone is insufficient. Multi-state versions need their own mass and moment conditions.
(iii) [range bound] range(d) ≤ [(J_max + 1)ν + K] log(n+1). The former bound (n+K) log(n+1) fails (selecting one signal-aligned duplicate per actual block accumulates the same fit gain repeatedly in the table product); the former "unreachable below n ≈ 10¹⁷" cutoff is withdrawn. Actual production failure additionally needs a candidate set attaining the obstruction and passing preflight; the proxy-deletion production construction remains UNVERIFIED.

## Dependencies
Builds on: T13, method §6.7. Used by: T34 (operational discussion).

## Numerical evidence (provisional)
provisional evidence (Sol check J9): at x = 10, ESS < 0.9 iff a ∈ (2.29·10⁻¹⁰, 0.89999); e.g. a = 10⁻⁸ fails (ρ = 0.171), a = 10⁻¹² passes (0.9995), a = 0.95 passes; duplicate actual-partition instance n = 65, p = 64, B = 8: |d| = 930 > old bound 406 ≤ new bound 1360; symbolic duplicates reach |d|2^{−60} ≥ 10 at n ≈ 2·10⁹. Files: judge/sol1/J9_dyadic_ESS.json, J9_duplicates.json.

## Proof-route hint (optional)
Evaluate the two finite moments for (i)–(ii) and use monotonicity in x; determinant and residual bounds per table for (iii), with J_max blocks each able to repeat the full signal gain. Hardest step: realising the required candidate masses in an executable regression family. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
