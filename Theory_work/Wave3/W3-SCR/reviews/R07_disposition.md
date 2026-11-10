# R07 (exhaustive sweep, gpt-6-astra high) — disposition

Counts: **0 blocker, 3 major, 9 minor** (12 findings). All three majors and four of the minors concern ASSUMPTION_MAP.md
(overstated "necessary" labels and wording), not a theorem or a proof. The sweep's verification ledger records as
completely checked and correct: L1.1-L1.7 (incl. L1.5°); all events of L2; SCR-A, (A∞), SCR-A°, (A°∞); B1, B2, B2°,
B2d, B3; A1, A1°; SCR-M and M1-M6; M2, M5 and SCR-G as coded; L5 facts, (EC′)/(EC), L5.2, SCR-C; SCR-R; SCR-N and both
consequences; CC1-CC6 (substantive implications). Report verbatim: `R07_sweep_astra.md`. All 12 fixed:

| # | Sev. | Finding | Fix |
|---|---|---|---|
| 1 | MAJOR | Map: "Γ_n(q) is 0 once q columns span the missing mean" is false (ridge gain stays positive) | Map row rewritten: span containment gives Δ_n(q) = 0 and voids the bridges; ridge visibility need not vanish. |
| 2 | MAJOR | Map: ID / AF / DF labelled "necessary" — not necessary for the (possibly vacuous) screening conclusion | Relabelled "sufficient bridge properties"; non-identifiability only obstructs *uniform* support identification. Outcome item 2 rewritten. |
| 3 | MAJOR | Map: "nΔ must dominate log p" unsupported, not scale invariant | Deleted; an information-theoretic necessity statement is listed as not attempted. |
| 4 | MINOR | Map sketch: positive part and event qualifier missing | Fixed. |
| 5 | MINOR | "truths already in S do not raise the bar" ignores ridge shrinkage (A²/n² contribution) | Reworded in STATEMENT and the map. |
| 6 | MINOR | "only at S = ∅ is Q_S = n−1" | Reworded ("identically at S = ∅"). |
| 7 | MINOR | G_S used both for the Gram matrix and for a scalar | Scalar renamed g⁻_S in STATEMENT (SCR-M) and L7. |
| 8 | MINOR | SV(q) had a finite-sample and an asymptotic meaning | Map now has SV(q,x) = MC(q,x), SV∞, SV°(q,x) as separate rows. |
| 9 | MINOR | "some near-orthogonality" listed as necessary | Outcome item 2: only SCR-N's threshold is listed as proved sharp; NF is "one sufficient condition". |
| 10 | MINOR | CODE_CHECK tie sentence overstated when the top-level flag is FALSE | Reworded (a displaced centre's certificate does not transfer; the flag needs a certified archive returning the HPM). |
| 11 | MINOR | STATEMENT §0 "same setting except…" omitted that σ may vary | Added. |
| 12 | MINOR | Unescaped pipes in the map table | Table rewritten without in-cell pipes. |

STATEMENT is now v3.3 = v3.2 (LOCKED) + wording/notation fixes only (findings 5, 7, 11 and R06's 2, 5): no hypothesis,
constant or conclusion changed. Next: council C1 (gpt-6-astra high + Claude Opus 5.5 high on claudeAgent).
