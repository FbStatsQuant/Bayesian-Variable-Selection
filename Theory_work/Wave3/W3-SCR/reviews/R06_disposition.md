# R06 (independent mid-point, gpt-6-astra high; statement + proofs + code only) — disposition

Verdict: **CONTINUE**. "SCR-A and SCR-M are proved"; the capped-search argument, the exact-recovery threshold and the
constants checked out; no blocker, no redesign. Report verbatim: `R06_midpoint_astra.md` (it reviewed v3.1).

| # | Sev. | Finding | Disposition |
|---|---|---|---|
| 1 | MAJOR | STATEMENT M3 lacked the maximising-witness qualifier (L7 has it) | Already fixed in v3.2 (same finding as R05b N1). |
| 2 | MINOR | "strong coefficients do not raise the bar for weak ones" too categorical (missing strong truths raise σ_S) | Fixed: wording now distinguishes truths already in S from strong truths still missing. |
| 3 | MINOR | EC′ "informative only when…" gloss | Already fixed in v3.2 (R05b N2). |
| 4 | NOTE | Within the file excerpts allowed to this reviewer, cache ownership, enumeration and parts of the scorer could not be audited | These were audited with full code access by R01 (finding 7) and R05 (finding 11: new cache and ledger per final run, inherited models rescored, cache hit checks the full model, enumeration scores every feasible set). No change. |
| 5 | MINOR | M6 illustration: make "fixed" explicit | Fixed (STATEMENT, L7). |
