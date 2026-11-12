# W3-PSHARP — council R2 disposition (lead, Opus 5.5 high on Claude Personal; 2026-11-12 07:30 CST)

Round R2 on MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14.
- `R2_council_sol.md`: 9.2, G1–G6 PASS, 0 FATAL / 0 MAJOR / 0 MINOR / 2 NIT.
- `R2_council_opus.md`: 9.3, G1–G6 PASS, 0 / 0 / 0 / 6 NIT.
- `R2_reconciliation_sol.md`: RECONCILIATION: ALL-RESOLVED (11/11 R1 entries; 0 regressions).
- `manifest.py bind` OK on both seats; `manifest.py verify` OK on the current tree (07:27 CST).

All eight findings are NITs, editorial only: no statement item, proof step, premise or code pin is affected.
**Disposition: ACCEPT ALL, DEFERRED, not applied.** Editing covered files now would break `verify` on MANIFEST_R2.
Under rule 15 they go in as one editorial batch after HQ's go, with an independent Sol diff check attesting
"editorial only".

| # | Source | File:line | Accepted change |
|---|---|---|---|
| E1 | sol N1 | REPORT.md:39 | `Σ_{j≥1}` → `Σ_{j=1}^{K−s₀}` |
| E2 | sol N2 | PLAN.md:28–29 | replace with Sol's wording (restricted odds/Λ_n; transformed lower bound on δ_n√n) |
| E3 | opus N1 | STATEMENT.md:73 | append "(under (W-orth) this needs p ≤ n−1−r₀, e.g. p = min(n−1−s₀, ⌊n^a⌋); under (W-sph) any a > 0)"; the claim is vacuous there, not false; wording only |
| E4 | opus N2 | REPORT.md:9 | "Lemma S and Corollary B are deterministic …; Propositions A and C are asymptotic; all concern the exact coded target π" |
| E5 | opus N3 | REPORT.md:46–47 | mark the p = s₀+1 remark "(heuristic, not proved here)" |
| E6 | opus N4 | REPORT.md:111 | Opus's two-part wording (lower bound proved on the witness classes; exactness only on the Remark A3 sequences, conditional on W3-POST:Thm-1 / Cor-1R) |
| E7 | opus N5 | ASSUMPTION_MAP.md:16 | "route threshold; behaviour of the constant beyond it not determined (outside R1 anyway)" |
| E8 | opus N6 | REPORT.md:88–89 | `3·10⁻¹³` → `≤ 3.5·10⁻¹³` |
| E9 | lead | REPORT.md:8, 74, 174–175 | "CHECKPOINT_2.md" → "CHECKPOINT_3.md" (the council record is filed under CP3, per PROTOCOL rule 10) |
