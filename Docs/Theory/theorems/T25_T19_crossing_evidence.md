# T25 (T19): Conditional evidence bounds through a crossing

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** reflected particle-system bound (i)–(iii): **secondary**; useful actual-run crossing rates (iv): **optional / open**.

## Definitions used
𝓒-measurable working set W; q_t^W, normalised g_t^W; reflected comparator with iid q₀^W starts and the original initial normaliser, terminal mean Z_W° = r_WZ, r_W = π(W)/π₀(W); Ẑ_{W,r}, pooled Ẑ_W; D_N := ∏_{t=1}^T(1 + (C_t − 1)/N_e) − 1; W_t := Ẑ_t/Z_t; χ_t² at stage t; Φ_t (T14(iii)); inventory codes BW2, BW_W, CPL-E, PW2, RET/OCC, COVER.

## Assumptions
EX-A, EX-S, CAL and completed final runs; BW2 (or BW_W via T19) with CPL-E, or PW2 for the actual run, or T14's set conditions; ONE and COVER(𝔓, ε_C) only for the pair specialisation.

## Precise statement
(i) [BW2 comparator bound] Under BW2 with constants C_t: E_𝓒(Ẑ_{W,r}/(r_WZ) − 1)² ≤ D_N and E_𝓒(Ẑ_W/(r_WZ) − 1)² ≤ D_N/4 (four independent reflected islands).
(ii) [actual-run probability transfer] Under CPL-E with failure h_n^E: P_𝓒(|Ẑ/Z − 1| > |r_W − 1| + x) ≤ h_n^E + r_W²D_N/(4x²). If both endpoint masses of W are ≥ 1 − ε then |r_W − 1| ≤ ε/(1−ε) and r_W ≤ 1/(1−ε); vanishing endpoint deficit, h_n^E → 0 and D_N → 0 give relative evidence consistency. This transfers a probability bound, not the comparator's second moment. Under BW_W, T19's V_Z (with a ≤ C₀) replaces D_N.
(iii) [role of the grid] For a single-flip pair 𝔓 ⊆ V, COVER-pair and T13 control the restricted incremental dispersion and T18 supplies the exact-refresh comparator; a proxy-swap pair has no such refresh; enlarging W needs its own stability and coupling verification. The valid weighted outside-mass identity is q_{t−1}(g_t²1_{Wᶜ}) = (1 + χ_t²)q_{2φ_t−φ_{t−1}}(Wᶜ), a target-law moment, not a squared-evidence-weighted particle history.
(iv) [withdrawn rate; PW2 research target] The v2 RET+OCC variance rate is withdrawn. If the actual particle system satisfies PW2, E_𝓒[W²_{t−1}{(q̂_{t−1}g_t)² − 1}] ≤ (a_t/N_e)E_𝓒W²_{t−1} + ν_t, then Var_𝓒(W_T) ≤ ∏_t(1 + a_t/N_e) − 1 + Σ_sν_s∏_{t>s}(1 + a_t/N_e), divided by four under island pooling. Establishing PW2 with useful constants is the missing task; RET and marginal OCC do not imply it.
(v) [first-moment alternative] The general-set T14 route gives consistency if Σ_{t=0}^T q_t(Wᶜ) + Σ_{t=1}^T Φ_t → 0; the Φ_t need control.
With bounded C_t, T = O(log²n) and N_e ≥ max(n,p) make D_N → 0 but establish none of the other hypotheses. No no-grid ablation rate and no pair-coupling impossibility is adopted.

## Dependencies
Builds on: T09, T12, T13, T14, T17, T18, T19. Used by: T15/T23 (per-island lower tails), T31.

## Numerical evidence (provisional)
provisional evidence (Sol check J10): abstract two-state benchmark with exact COVER, trivial RET and empty OCC slack: lazy within-pair movement gives relative variance 1.75 (N = 1) against the refresh product 0.40 and the advertised RET+OCC ceiling 0.52 (rate contradicted); the BW2 induction B_t ≤ a[1 + (C_t−1)/N]q_t^{W⊗2} is supported exactly; the actual hybrid component (n = 6, p = 3, T = 4) differs from the refresh product (0.00391 vs 0.00389). Files: judge/sol2/J10_CROSSING_RATES.md.

## Proof-route hint (optional)
Under BW2, dominate the squared-weight distinct-child law through the multinomial same-parent/distinct-parent decomposition, propagate by (g_t^WK_t^W)^{⊗2}, integrate, pool islands; T17 for (ii); iterate the displayed recursion for (iv). Hardest step: a useful stability condition and transfer for actual v3. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
