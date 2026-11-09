# MP1 disposition (independent mid-point, gpt-6-astra high) — 2026-11-09

Verdict: **CONTINUE** (no fatal step in LT♯, C or D; three local corrections).

| # | Sev. | Issue | Disposition |
|---|---|---|---|
| 1 | MEDIUM | P-OVL∞ written as 1_𝒜L/M → ∞ silently forces P(𝒜) → 1 | ACCEPTED. P-OVL∞ := P(𝒜 ∩ {L/M ≤ c}) → 0 ∀c (Q = ∞ off 𝒜); TR-d proof uses 1_𝒜e_L ≤ e^{−Q}; production form P(𝒜 ∩ {M > ε log n}) → 0. STATEMENT, TR. |
| 2 | LOW | "property of (π, π₀) only" overstates (L can vary) | ACCEPTED. Relabelled "relative to the executed burn-in L; on (π, π₀) alone once L is the production budget". |
| 3 | LOW | LT-e′ MPM at u = ½ vs strict tail | ACCEPTED. Use u = ¼ and {MPM ≠ S₀} ⊆ {pooled ≥ ½} ⊆ ∪_r{E_r > ¼}. |

Reviewer's closing caution adopted for REPORT: P-CONC and P-START enter only through their external interfaces; neither
calibration success nor computational overlap is established here from primitive conditions.
