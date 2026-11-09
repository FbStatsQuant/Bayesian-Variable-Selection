# v1.1 fidelity review R1 — disposition (lead, 2026-11-09)

Reviewer: one fresh Codex gpt-6.1-sol (reasoning effort high), brief `BRIEF.md`, review `R1_fidelity_sol.md`.
Verdict: **FAITHFUL-WITH-FIXES** — BLOCKING 0, MAJOR 1, MINOR 6, NIT 0. No statement-box or council-score discrepancy found
(86 stmt boxes compared with their spans; all section-7 status spans, update paragraphs, brief, changelog, registry rows audited).

All seven findings were checked against the cited sources and **accepted and applied** (no objection):

| # | sev | disposition | change |
|---|---|---|---|
| 1 | MAJOR | applied | §07 overview plain reading: the "everything asymptotic / joint with output" sentence replaced by the reviewer's scoped text (selection consistency asymptotic; reported HPM joint with output except fallback delivery; N1/Cor. E fixed-data potential-run scope; SL0, M5(0), CAP deterministic finite-n; fallback delivery every n ≥ 3; no finite-n selection guarantee at n = 200), cited W1/W1-N1/STATEMENT.md:20-23 and W1C/FINAL/sections/s8_scope.tex:6. Agent brief: "any finite-n guarantee" → "a quantitative finite-n selection-consistency guarantee, in particular for the study at n = 200". |
| 2 | MINOR | applied | N1 plain reading rewritten with the a.s. localisation on successful calibration with island r present, the named premises, deterministic bound, declared h; cited STATEMENT.md:62-65, 94-105. |
| 3 | MINOR | applied | C-GROW citations corrected: REPORT.md:96-99 → 93-96; 19-21 → 16-18; 22-23 → 19-20 (lead's line-offset error). |
| 4 | MINOR | applied | A1 stmt span 9-15 → 9-19 (abridgement marker kept). |
| 5 | MINOR | applied | OB03 update: N3 REPORT.md:13 → 12-13; C-DLV card: `\src{W1C/C-DLV/REPORT.md:24-28}` after `\status{PARTIAL}`. |
| 6 | MINOR | applied | Direct `\src` citations added to every ticket clause in the agent-brief v1.1 paragraph (and s8_scope.tex:6-15 for the frontier), to every status in the v1.1 changelog item, and to the overview rows for the HQ audits (A1:3, A2:1-5, A3:5, A4:1) and the final chapter (C3_disposition:3-6; round-1/2 score lines). |
| 7 | MINOR | applied | Frontier item F9 (floating point) replaced by the reviewer's text: N3-code(e) and UM-FP are the binary64 start-mode results (W1/W1-N3/STATEMENT.md:101, 128-132; W1C/C-PACK/STATEMENT.md:23-29); the chapter's "only binary64 statement" is noted as a chapter summary. |

After the fixes: `scripts/check.py` 0 errors; full build re-run (see final message). No second review round was run
(the brief asked for one fresh reviewer; all findings were editorial/citation-level and applied verbatim from the reviewer's
proposed fixes).
