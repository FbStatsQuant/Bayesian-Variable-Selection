# W3-DIST — disposition of pre-check P6 (`reviews/P6_opus_precheck_C.md`; Claude Opus 5.5, Claude Third; filter, not a review layer)
Object: `work/C_size/S.md`, `V.md`, `X12.md`. Verdict: VERIFIED-WITH-AMENDMENTS; no mathematical error; 2 MINOR, 5 NIT.
Lemma S VERIFIED-WITH-AMENDMENTS; Lemma V, X1, X2, facts F1–F7 VERIFIED.
| id | sev. | disposition |
|---|---|---|
| C-1 | MINOR | ADOPT (S.md amendment A-1): corollary stated for t ≥ max{log n, (2C_S + 1)²}, n ≥ max{3, 2s₀^r, ⌈4C_S²⌉} |
| C-7 | MINOR | ADOPT (queued STATEMENT edit): "(C) is used only through (L₀)" is false for Lemma V(a) and step X4, which use ρ′ = (‖μ‖² + ‖θ*‖²)/n; restrict the sentence to Lemma S and DIST-3 |
| C-2, C-3, C-4 | NIT | ADOPT (S.md amendments A-2, A-3, A-4) |
| C-6 | NIT | ADOPT (queued STATEMENT edit): write Q^c in Lemma V |
| C-8 | NIT | X12.md is not on the path (lemmas/X.md is self-contained); no change |
Comparison: API S-a, S-b, S-c and V-a, V-b, V-c agree with S.md and V.md on statements and shared steps; S-b's
closed-form route has no t/√n term (a possible later simplification, not needed).
