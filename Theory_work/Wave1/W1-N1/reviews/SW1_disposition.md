# SW1 · exhaustive sweep · disposition (lead, 2026-11-08)

Reviewer: Codex gpt-6.1-sol, reasoningEffort high (fresh delegate_task; told not to read LOG/reviews). Reply verbatim:
`SW1_sweep_codex.md`. Count: 0 CRITICAL, 5 MAJOR, 11 MINOR. Overall (reviewer): "N1 and Corollary E are established as
conditional mathematical statements under the locked statement's named idealised premises"; the numerical package needed fixes.

All 16 findings ACCEPTED and fixed; the whole numerical companion was regenerated (v2: harness `cpp/n1_harness_v2.exe`,
outputs archived in `numerics/json/`, report `numerics/RESULTS.md` v2).

| # | Sev. | Fix |
|---|---|---|
| 1 | MINOR | Evidence citations now distinguish `v3_engine.h:300` (initialisation), `:318-320` (increment), `:323` (accumulation) (STATEMENT §1). L1 already cited `:323`. |
| 2 | MINOR | L2: `q_T = q_{φ_T} = q_{φ=1} = π` (stage vs temperature indices). |
| 3 | MAJOR | `n1_exact.py`: row sums for #Ω > 130 now computed exactly as R·1 by the order DP on transposed kernels (valid because the uniform order law is reversal-invariant); assertion row-sum ≤ 1e-12. RESULTS §2 regenerated. |
| 4 | MAJOR | Harness v2: Gibbs inclusion probability by bisection on the production step outcome (RB o_j kept only as a cross-check, max difference reported); every π₀ script validated by calling production `draw_pi0` (returned model + full consumption; failures counted, must be 0); self-proposals of the independence step executed and checked; every swap/independence/Gibbs call checks full script consumption. RESULTS §1 states precisely which quantities come from production tables (π₀ interval widths; RB cross-check) and which from step calls. |
| 5 | MINOR | `threshold()` bisects down to adjacent doubles (error if not reached), records the largest final bracket (RESULTS §1), documents the endpoint conventions. |
| 6 | MINOR | Design kind 4 now two equicorrelated blocks with separate common factors (affects d3, d8; regenerated). |
| 7 | MAJOR | "Production grid" renamed **pilot-derived grid** everywhere (production pilot + production `build_grid` on an enumerated V; not the full calibration path), with the difference stated in RESULTS and the harness. |
| 8 | MAJOR | NC3 now reports the N1-centred paired statistic W·H(h_ω) − π(h_ω) and its z (`n1_mc.py`; RESULTS §5); the weighted-centred statistic is kept in the JSON, labelled as a different target. |
| 9 | MINOR | NC3 reading: non-detection is reported as "this experiment does not detect a discrepancy", with no inference that selection leaves the identity intact. |
| 10 | MINOR | NC2 d7 exception stated in RESULTS §4 and in the case name. |
| 11 | MINOR | π₀ column described as floating-point table/score/normalisation effects (2⁻⁵³ grid not modelled); "does not affect the residuals" replaced by "coexist with the small absolute residuals". |
| 12 | MAJOR | Durable package: small outputs (meta, phis, omega, export log, exact and MC JSON) archived in `numerics/json/dN/`; SHA-256 of every output including non-archived binaries in `json/MANIFEST.sha256`; `numerics/BUILD.md` with build and regeneration commands and seeds; `make_results.py` rebuilds RESULTS.md from `json/` alone. |
| 13 | MINOR | Hash-manifest path corrected to `cpp/production_headers.sha256`. |
| 14 | MINOR | Table bars escaped (`\|`), `#Ω` used in headers. |
| 15 | MINOR | `n1_exact.py` and `make_results.py` assert completeness (10 designs, 20 MC runs), finiteness, N1 tolerance 1e-10, control threshold 1e-6, \|z\| ≤ 4, z_E ≤ 4, π₀ script failures = 0, hook diff = 0; success language is emitted only after the assertions pass. |
| 16 | MINOR | R_remarks: numerical exhibition restricted to NC1–NC3; conditioning items attributed to the cited locked results. |
