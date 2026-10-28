# T06 (A5 = T-ID): Identifiability and exact ties

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** identifiability and limits; **core** (proposition).

## Definitions used
Score function F(S) as a function of the standardised response y (X fixed); feasible models (|S| ≤ K ≤ ⌊n/2⌋); contrast space of dimension n−1; smoother M_S = nX_SH_S⁻¹X_Sᵀ = f(X_SX_Sᵀ) with f(λ) = nλ/((n+1)λ+1). The method's near-duplicate report: components of {|r| ≥ 1 − 10⁻¹⁰}.

## Assumptions
Valid input for (i); G and NIS (new; decidable from X) for the null-tie clause; the hypotheses of T03 for the strict-mode clause; G and DUP (new) for (iii), with SE deliberately absent.

## Precise statement
(i) [exact ties] For fixed valid (X, n, p), the score functions of two feasible models S ≠ S′ coincide for every standardised y iff X_SX_Sᵀ = X_{S′}X_{S′}ᵀ; equality of outer products forces |S| = |S′| (traces, ‖x_j‖² = n−1). Equal column spans with unequal outer products need not tie. Under G and NIS, accidental exact ties among feasible models have probability zero.
(ii) [fallback without NIS] Under T03's hypotheses, S₀ is the strict global maximiser on {π(S₀) > ½}, an event of probability → 1; the tie rule is not invoked at S₀.
(iii) [duplicates; DUP] Signed duplicate columns x_i = ±x_j preserve every score under relabelling; any support containing exactly one of them has an equally probable counterpart, so neither atom exceeds ½. For two Gaussian truths with common noise variance, every selector has maximal error ≥ Φ(−‖μ₁−μ₂‖/(2σ*)); uniform recovery is impossible when ‖μ₁−μ₂‖/σ* → 0. The near-duplicate reporting threshold is a warning, not an exact-identifiability statement.

## Dependencies
Builds on: T03 (strict-mode clause only). Used by: T11 (tie order in the ledger), T31, T33.

## Numerical evidence (provisional)
provisional evidence (Sol check J11): duplicates and different bases with equal outer products tie (score difference 0); equal spans with unequal outer products do not (score difference 0.0126). Files: judge/sol1/J11_ties.json.

## Proof-route hint (optional)
Identical scores give proportional residual quadratic forms y_cᵀ[κI − M_S]y_c = c·y_cᵀ[κI − M_{S′}]y_c on the contrast sphere (κ = 1 + 2b₀/(n−1)); each feasible smoother has a nontrivial kernel since K ≤ n−2 < n−1, which with positivity forces c = 1; injectivity of f gives equal outer products; traces give equal sizes; under NIS, F(S) − F(S′) is a non-identically-zero real-analytic function on the sphere, whose zero set is null under the Gaussian angular density. (iii): posterior symmetry; the two-point testing bound. Hardest step: stating the sphere argument correctly. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
