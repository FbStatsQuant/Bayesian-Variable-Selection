# T34 (T23-S): Statuses and allocation-dependent guarantees

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** operational limits; **core** (proposition candidate).

## Definitions used
Statuses (exact, completed, schedule_limit, numerical_failure, resource_limit, y_constant, no_predictors, invalid_input); the preflight; the exact-branch inequality Σ_{k≤K}C(p,k) ≤ (5H₀+4N₀)p; OP-a, OP-s, NUM, EX-A.

## Assumptions
Valid input; branch-specific storage/time model (T32); EX-A or validated numerics; OP-a and OP-s where outputs require them.

## Precise statement
(i) On the dense-Gram SMC branch the Gram alone needs 8p² bytes plus retained data and other storage: a necessary SMC constraint, not a universal capacity formula. The exact branch precedes Gram and block construction; for valid inputs with 3 ≤ n ≤ 5 its inequality holds for every p (E ≤ 1 + p + p(p−1)/2 ≤ 4p² ≤ threshold), subject to preflight; a streaming implementation's retained-data restriction scales with np, so no universal p_max = Θ(√M₀) follows.
(ii) schedule_limit returns the best scored model but no evidence or PIPs; HPM routes completed earlier need no OP-s; final-run routes retain the nonlaunch-and-no-earlier-hit term; evidence/PIP consistency needs availability conditions (OP-s).
(iii) Under EX-A numerical scoring failure is excluded; NUM alone does not exclude it. Under nondegenerate Gaussian noise y_constant has probability zero. Other invalid-input cases are outside the statistical regime.
(iv) Population stage-count results do not transfer automatically to the empirical pilot with its floor, 60 halvings and retained pilot temperatures (T36).

## Dependencies
Builds on: T32, T33, T36, method §§2, 6.1–6.2, 8. Used by: T21, T26.

## Numerical evidence (provisional)
provisional evidence (Sol check J9): n = 3, 4, 5 with p = 10⁸ take the exact branch (E ≤ 5·10¹⁵ < threshold 5.02·10¹⁶); n = 6 takes SMC; the universal √M₀ ceiling is contradicted. Files: judge/sol1/J9_branches.json.

## Proof-route hint (optional)
Follow the execution order and the preflight separately for each branch; method §2 states what each status returns. Hardest step: useful completion probabilities (unresolved). *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
