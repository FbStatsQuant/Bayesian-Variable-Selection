# R07 disposition (exhaustive sweep, Codex gpt-6.1-sol xhigh; 0 FATAL / 0 MAJOR / 10 MINOR / 6 NIT; reply verbatim R07_sweep_sol.md)
| # | Sev | Item | Disposition |
|---|---|---|---|
| 1 | MINOR | Mis-description of inherited NA routes (REPORT, L2 Remark 1) | APPLIED: L2 Remark 1 now states GROW L2.3(a)/L6.6/APP L3.6 thresholds precisely; NA-R presented as a different sufficient construction, no claim the earlier routes necessarily fail; REPORT rewritten accordingly. |
| 2 | MINOR | REPORT drops the additive error ϵ_n | APPLIED in REPORT §1. |
| 3 | MINOR | matching (log n)^d extras asserted without proof | APPLIED: L4 Remark (3) and REPORT state the upper bound O((log n)^d); growth observations labelled. |
| 4 | MINOR | polynomial upper envelopes stated as orders | APPLIED in REPORT (O(n^{15ρ}), O(n^{1/(2α)})). |
| 5 | MINOR | EBM regime / route-obstruction inference | APPLIED: D1_SUMMARY header and reading 1 corrected (s₀(g−1) ≈ 9 log n, not in VN (V2) regime; observations only). |
| 6 | MINOR | "≤ 6 h-units" false | APPLIED: recomputed max per-run gap 9.19 (G2A n = 800 seed 3), labelled as a lower-estimate gap. |
| 7 | MINOR | numerics attribute an unproved O(√log|Q|) remainder | APPLIED: replaced by the proved max Z² ≤ 2 log p + o(log n). |
| 8 | MINOR | numerical metric names in L2 header | APPLIED: "collinearity check, cosine deficit ≤ 5.6e-16"; "magnitude difference | |Z| − |Z^pop| |". |
| 9 | MINOR | "polynomial groups break the counting" too strong | APPLIED: L4 Part B Remark (2) states the sandwich exponent inequality and that NA/assembly would need a polynomial analysis. |
| 10 | MINOR | REPORT says R06a/b pending | APPLIED: REPORT rewritten and synchronized. |
| 11 | NIT | stale D3 independence qualification | APPLIED (STATEMENT (D3)). |
| 12 | NIT | ℓ_n reused in L2 | APPLIED: L2 uses ℓ_𝔓 for log|𝔓|; L6 citations into L2 re-synchronized (line shift +1). |
| 13 | NIT | atom identity mixes functionals and vectors | APPLIED (STATEMENT (B): 𝒲a). |
| 14 | NIT | CT_d unused upper spectral bound | APPLIED: CT_d assumes λ_min(A) ≥ α only. |
| 15 | NIT | undefined "DLV" abbreviation | APPLIED: full path in L7. |
| 16 | NIT | distance metric in numerics | APPLIED: D1_SUMMARY column header and L4 header. |
All 16 items fixed; no objection recorded.
