# T14 (L-FM): First-moment evidence consistency

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** algorithmic convergence (consistency of the evidence); **core** (lemma).

## Definitions used
Stage laws q_t, G_t = e^{Δ_td}, empirical population q̂_{t−1} reweighted at stage t, island evidence Ẑ_r (00_COMMON §2). For a model S° fixed given 𝓒: η_t = 1 − q_t(S°), ε_* = max_{0≤t≤T}η_t; R_t(S) = G_t(S)/G_t(S°); A_t = ∏_{v=1}^t q̂_{v−1}(R_v); b_t = q₀(S°)/q_t(S°). For a set 𝔄: ε_t = 1 − q_t(𝔄); c_t = q_{t−1}(G_t1_𝔄)/q_{t−1}(𝔄); R_t = G_t/c_t; A_t, b_t = q₀(𝔄)/q_t(𝔄) analogously; Φ_t = E[A_{t−1}|q̂_{t−1}((R_t − 1)1_𝔄)|]/b_{t−1}.

## Assumptions
EX-A, EX-S, CAL; exact start; prescribed multinomial resampling and q_φ-invariant rounds, one round per stage.

## Precise statement
Conditional on a successful 𝓒:
(i) [singleton] Ẑ_r/Z = A_T/b_T, and for every N ≥ 1 (ε_* < 1):
  E|Ẑ_r/Z − 1| ≤ [Σ_{t=1}^T(b_{t−1}η_{t−1} + b_tη_t) + |1 − b_T|]/b_T ≤ (2/(1−ε_*))Σ_{t=0}^T η_t.
The endpoint term |1 − b_T| is essential. Convexity gives the same bound for the pooled Ẑ.
(ii) [consequence] Along launched families, Σ_{t=0}^T η_t → 0 in data/calibration probability implies Ẑ/Z → 1 in joint probability. No over-tempered condition and no N^{−1/2} rate is asserted.
(iii) [general set] Ẑ_r/Z = A_T/b_T with the set definitions, and E|Ẑ_r/Z − 1| ≤ [2Σ_{t=0}^T ε_t + Σ_{t=1}^T Φ_t]/(1 − max_tε_t). The signed expression inside Φ_t's absolute value has weighted mean zero; Φ_t ≥ 0 need not vanish (it vanishes for a singleton); Φ_t ≤ q_{t−1}(|R_t − 1|1_𝔄), which need not be summably small. Set mass alone does not control within-set weight dispersion; reflection is one possible further route, not an automatic transfer.

## Dependencies
Builds on: T12. Used by: T15, T25 (first-moment alternative), T26.

## Numerical evidence (provisional)
provisional evidence (Sol check J6): exact finite-state laws (N ≤ 2, T = 3): a rare state with singleton deficits (10⁻¹², 3·10⁻⁸, 10⁻³) has exact L¹ error 0.0020 ≤ telescoping-with-endpoint 0.00200 ≤ bound 0.00200, while E(Ẑ/Z)² ≈ 10⁶; a two-state set with full set mass has L¹ error 1.996 = Φ. Files: judge/sol2/J6_FIRST_MOMENTS.md.

## Proof-route hint (optional)
Use E[A_{t−1}q̂_{t−1}(f)] = b_{t−1}q_{t−1}(f) (T12), the exact identity q_{t−1}(R_t1_{S°ᶜ}) = (b_t/b_{t−1})q_t(S°ᶜ) and R_t(S°) = 1 to get E|A_t − A_{t−1}| ≤ b_{t−1}η_{t−1} + b_tη_t; telescope A_t; retain |1 − b_T|; note b_t/b_T = q_T(S°)/q_t(S°) and |1 − b_T|/b_T = |q_T(S°) − q₀(S°)|/q₀(S°). For sets, choose c_t so that R_t has q_{t−1}(·|𝔄)-mean 1 and separate inside/outside contributions. Hardest step: Φ_t for larger sets. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
