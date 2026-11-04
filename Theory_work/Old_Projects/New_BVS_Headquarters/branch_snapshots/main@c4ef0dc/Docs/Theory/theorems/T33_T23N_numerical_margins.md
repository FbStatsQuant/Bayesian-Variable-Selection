# T33 (T23-N): Numerical margins on a common scored set

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** numerical robustness; **secondary** (lemma candidate).

## Definitions used
H_S = (n+1)G_S + I; NUM (simultaneous error bound η on all compared log scores at fixed n); the common actual scored set; the tie rule and the near-tie list; T03's global margin.

## Assumptions
EX-A for the matrix statement; NUM on the common scored set; T03's hypotheses for the statistical margin.

## Precise statement
(i) I ≼ H_S ≼ [1 + (n+1)(n−1)|S|]I; the exact matrix is positive definite, including with duplicate columns, so exact Cholesky never fails.
(ii) Under NUM, if every evaluated log score on a common actual scored set differs from its exact value by at most η and the set's exact best model has gap > 2η, its ranking is preserved. If S₀ is scored, T03 supplies the candidate global margin ½ log n − ½ log log n − O_{P₀}(1), so η = o(log n) suffices on the corresponding high-probability event.
(iii) Not shown: that perturbed and exact runs score the same models, preserve proposal probabilities, or estimate evidence similarly. Exact ties require validated comparisons and the specified tie order; the near-tie list never changes the decision. No probability-zero statement for numerical_failure under NUM; no numerical growth estimate is adopted.

## Dependencies
Builds on: T03, T06, T20. Used by: T34.

## Numerical evidence (provisional)
None.

## Proof-route hint (optional)
Gram eigenvalues bounded by the trace (‖x_j‖² = n−1); perturb score differences. Hardest step: establishing NUM through preprocessing, solves and residual evaluation (backward-error precedents UNVERIFIED). *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
