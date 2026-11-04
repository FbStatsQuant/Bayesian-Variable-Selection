# MEET-THM · STATUS (chair)

Updated 2026-11-04 (check wave 2 running).

| Step | State |
|---|---|
| 0. Dossier frozen; Round 0 (R0_D, R0_E) | done |
| 1. R0 diff | done: `R0_DIFF.md` (K01–K108) |
| 2. Round 1 (Seats A–D) | done: `R1_A.md`–`R1_D.md` (verbatim); clerk side-by-side `evidence/R1_SIDE_BY_SIDE.md` |
| 3. Check wave 1 | done: `evidence/W1_PC1/VERDICTS.md` (A, B, D: 11 COUNTEREXAMPLE, 25 NEEDS-HYPOTHESIS), `evidence/W1_PC2/VERDICTS.md` (C: 0 COUNTEREXAMPLE) |
| 4. Synthesis 1 | **final v2.2** `SYNTH_R1.md`: audit FAIL → v2 re-audit FAIL → v2.1 verification PASS WITH CORRECTIONS (applied). Files: `SYNTH_R1_AUDIT.md`, `SYNTH_R1_REAUDIT.md`, `SYNTH_R1_VERIFY.md` |
| — Inherited-proof check | **done**: `evidence/CHK_INHERITED/REPORT.md`. WS3, WS4 VERIFIED; WS6(d), WS7, N9 VERIFIED WITH AMENDMENT; one-shot refutation survives (Q1(c) met) |
| 5. Round 2 (Seats A–D) | **done**: `R2_A.md`–`R2_D.md` (verbatim) |
| 6. Check wave 2 | **running**: `CHECK_W2_BRIEF.md`; PC1 (gpt-6.1-sol) on A, B, D; PC2 (Opus 5.5) on C → `evidence/W2_PC1/`, `evidence/W2_PC2/`. Clerk building `evidence/R2_SIDE_BY_SIDE.md` |
| 7. Synthesis 2 | written: `SYNTH_R2.md` (reconciled list proposal, §5.3 package, run-card, growth rates; R3-1..R3-6). **Auditor running** |
| 8. Round 3; close | not started |

HQ: Q1–Q4 answered (`evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`), applied in `HQ_QUESTIONS.md`. FUTURE_WORK opened (FW1, FW2).

## Running tasks (delegate task ids, suffix only)
| Role | Target | Task |
|---|---|---|
| Auditor, SYNTH_R1 v1 | codex · gpt-6.1-sol high | done → FAIL |
| Auditor, SYNTH_R1 v2 re-audit | codex · gpt-6.1-sol high | done → FAIL (6) |
| Auditor, v2.1 narrow verification | codex · gpt-6.1-sol high | done → PASS WITH CORRECTIONS (applied) |
| Seat A, R2 | claudeAgent_personal · Fable 5.1 high | done → `R2_A.md` |
| Seat B, R2 | claudeAgent · Fable 5.1 high | done → `R2_B.md` |
| Seat C, R2 | codex · gpt-6-astra high | done → `R2_C.md` |
| PC1, wave 2 | codex · gpt-6.1-sol high | done → `evidence/W2_PC1/VERDICTS.md` |
| PC2, wave 2 | claudeAgent · Opus 5.5 high | done → `evidence/W2_PC2/VERDICTS.md` (29 TRUE-AS-WRITTEN, 0 COUNTEREXAMPLE) |
| Clerk, R2 side-by-side | claudeAgent · Haiku 5.5 | done |
| Seat D, R2 | claudeAgent_personal · Fable 5.1 high | done → `R2_D.md` |
| PC1, inherited proofs | codex · gpt-6.1-sol high | done |
