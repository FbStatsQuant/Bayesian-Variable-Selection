# Council C1 — result and disposition

Package scored: STATEMENT v3.3, CODE_CHECK, lemmas L1-L7, ASSUMPTION_MAP (brief: `C1_brief.md`). Seats scored
independently; reports verbatim in `C1_council_astra.md` and `C1_council_opus.md`.

| Seat | G1 | G2 | G3 | G4 | G5 | G6 | Score |
|---|---|---|---|---|---|---|---|
| gpt-6-astra (high, codex) | PASS | PASS | PASS | PASS | PASS | PASS | **9.3** |
| Claude Opus 5.5 (high, claudeAgent) | PASS | PASS | PASS | PASS | PASS | PASS | **8.9** |

**Council PASSED in round 1** (both ≥ 8.0, all six gates PASS in the same round). No blocker, no major.

Findings (all minor or notes) and post-pass edits (v3.4; not re-scored, none changes a conclusion or a constant):
| Seat | Sev. | Finding | Edit |
|---|---|---|---|
| Astra 1 | MINOR | STATEMENT M6 prose said b_𝓗 "does not depend on the number of models"; only its geometric upper bound does not | Reworded. |
| Opus 1 | MINOR | A1 / SCR-G said only "σ fixed"; the "for large n" steps of M4 (and of A1's proof) need κ, b, M fixed too | "κ, b, M, σ fixed (not depending on n)" added to A1 (STATEMENT, L3), SCR-G and M4 (L7). |
| Opus 2 | NOTE | The map's claim that κ² is attained for two missing truths had no construction | Two-line construction added to ASSUMPTION_MAP. |
| Opus 3 | NOTE | CC5 did not mention the scorer's Q-recomputation branch and fallback routes | Sentence added to CC5 (same Q and determinants under EX-A). |
| Opus 4 | NOTE | c₂ and M each used with two meanings | L5's proof constant renamed c₄; the model count of SCR-M renamed M_𝓗. |
| Opus 5 | NOTE | CODE_CHECK named commit 2252d57; HEAD is now 2ac3896 | Note added: core unchanged since 72785fe; hashes re-verified at HEAD. |
