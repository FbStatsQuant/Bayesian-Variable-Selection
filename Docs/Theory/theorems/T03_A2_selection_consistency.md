# T03 (A2 = T3): Selection, screening, PIPs and the global HPM

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** consistency; **core** (theorem).

## Definitions used
Target π, PIP_j, MPM, global HPM S† with the tie rule (00_COMMON §1); r_n; regime R1. Constants: j_* = ⌈(2A+1)s₀⌉ + 1; C_* = 2s₀ + 3[Aj_* + s₀ + log(j_*+1) + 1]; L_* = max{4C_*, 32[s₀(A+1)+2]}; M_* = 2L_* + 1.

## Assumptions
G, R, SE (project); BM-C (new candidate fixed constant M_*; provisional, from the J1 audit of proofs/T7_T8 §5; the proving run may replace M_* by any constant it can justify) or BM-∞ (project; M_n → ∞), either suffices. No beta-min for the screening clause.

## Precise statement
In R1 under G, R, SE and BM-C (or BM-∞):
(i) 1 − π(S₀) = O_{P₀}(r_n).
(ii) max_j |PIP_j − 1{j ∈ S₀}| ≤ 1 − π(S₀) (deterministic given (i)); P₀(MPM = S₀) → 1.
(iii) P₀(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)] → 0; on {π(S₀) > ½}, S₀ is the strict global maximiser of F (the tie rule is not invoked).
(iv) [screening; G, R, SE only] With J_n = {j ∈ S₀ : θ*_j² ≥ M_*σ*² log n/(nφ₀²)}: Π(S ⊉ J_n | y) = O_{P₀}(r_n); the PIPs of J_n tend uniformly to one. (Screening has its own underfitting comparison; it is not a consequence of full-support selection.)
(v) Null-truth beta-min is vacuous. Replacing (θ*, σ*²) by (θ*/s_y, σ*²/s_y²) leaves BM unchanged.
No frequentist O(r_n) selection-error rate follows from the posterior O_{P₀}(r_n) rate. M_* is conservative, not sharp; the sharp general-design constant is open.

## Dependencies
Builds on: T01, T02. Used by: T05, T06 (strict-mode clause), T08, T20, T21, T22 (endpoint propagation), T23, T24, T26, T28 (truth/superset consequences), T30, T31, T33.

## Numerical evidence (provisional)
provisional evidence (Sol check J1): the inspected selection proof uses diverging BM only to exceed fixed thresholds; the conservative fixed coefficient M_* = 2L_*+1 supplies missing signal ≥ (1−1/n)M_*σ*² log n, eventually exceeding L_* times the noise scale; illustrative s₀ = 2, A = 1: C_* ≈ 40.24, L_* = 192, M_* = 385. This is a sufficient-constant derivation for review, not an accepted proof.

## Proof-route hint (optional)
Compare each underfitted S with S ∪ S₀ in contrast coordinates via T01(ii); the unfitted signal enters as a gain ≥ (n−1)φ₀²‖θ*_{S₀∖S}‖²/σ*² against addition cost ½ log n + log(2p); separate bounded and large extra-variable classes using T02(ii) before taking Gaussian maxima over the finite-size comparison classes (no p^{m_n} union bound); the fixed constants exceed the noise and multiplicity thresholds of proofs/T7_T8/PROOF.md §§5.2–5.5; (iii) is elementary from π(S₀) > ½; screening repeats the comparison for omitted strong coordinates. Hardest step: completing every v3 transfer and truncated-sum bound while preserving the beta-min scale. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
