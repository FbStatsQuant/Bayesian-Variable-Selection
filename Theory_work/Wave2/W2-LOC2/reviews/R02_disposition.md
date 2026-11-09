# R02 disposition (Codex gpt-6.1-sol high; L1_toolkit VERIFIED-WITH-AMENDMENTS, L3_CTd VERIFIED-WITH-AMENDMENTS; reply verbatim in R02_L1L3_check_sol.md)
| # | Sev | Item | Disposition |
|---|---|---|---|
| 1 | MAJOR | CD_d: Cov(W_V|W_U) = (Θ_VV)⁻¹ false for V ⊊ [p]∖U (AR(1) counterexample) | APPLIED: proof via H := [p]∖U, Cov(W_H|W_U) = (Θ_HH)⁻¹, CT_d on Θ_HH, arbitrary V ⊆ H by principal submatrix + interlacing; statement (b) restricted to V ⊆ [p]∖U. Constants unchanged. Downstream uses checked: TAIL uses V = T∖T′ ⊆ [p]∖T′ (fine); RB applies CT_d to Σ_{A∪l} directly (unaffected). |
| 2 | MINOR | Envelope conversion: L0′ assumes coefficient-one bounds | APPLIED: invoke L0′ with κ_tool = κ + 1; t_n, h_n defined from actual cardinalities. |
| 3 | MINOR | ω_n → 0 insufficient; need ω_n log n → 0 | APPLIED: explicit rate in L1_toolkit L2.2 bullet. |
| 4 | MINOR | numerical L0 truncated; numerics not a certificate | APPLIED: L3 header qualified. |
| 5 | NIT | K in majorant; rename vector c → b in TAIL | APPLIED. |
