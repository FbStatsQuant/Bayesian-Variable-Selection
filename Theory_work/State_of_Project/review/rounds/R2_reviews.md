# Council round 2 — replies as received (2026-11-07)

## Sol (gpt-6.1-sol, high): SCORE 5.0 (G4 FAIL cap)
GATES: G1 PASS (seed 2 sample: 02_method.tex:440,513,541; 04_theory.tex:534; 04b_supplement.tex:100,191,280,582,715,828,1027,1089,1125,1156,1169) | G2 PASS (seed 2 sample: CL11, CL04, CE144, CJ213, CJ178, TH116, LIM06, RF198, OB05, CJ26, TH06.a, CL07, TH290, TH183, TH02.a2, RF270, EMP19, TH06, TH07.c, RF169) | G3 PASS (regenerated tables identical; −0.0002, 0.012, 0.007, 0.020, 0.0005, 0.0020, 99.9%, 99.8%, 2,251, 2,216 checked) | G4 FAIL (sample 02:104,167,252,283,587,716; 03:266; 04:807; 04b:223,459; 05:185,334; 06:134,146; C:3; overview audit found unsupported signal-threshold claim at 04_theory.tex:788) | G5 PASS
DIMENSIONS: fidelity 8.4 | completeness 9.4 | actionability 9.2 | agent-readiness 9.0 | calibration 8.8 | clarity 8.0
QUESTION_BANK: 30/30
ISSUES:
1. [major][G4] 04_theory.tex:788 plain reading of T03♯ drops the square (θ_j*²) and c > c₀. -> state squared condition with c > c₀.
2. [minor][calibration] 05_history.tex:62 "later fate is not recorded" not propagated from the dated PR #1 observation. -> qualify as archive cutoff and cross-reference.
STRENGTHS: traceability, coverage, reproducible tables, actionable charters; round-1 fixes present.

## Opus (claude-opus-5-5, high): SCORE 5.0 (G4 FAIL cap; 8.5 weighted before cap)
GATES: G1 PASS | G2 PASS | G3 PASS | G4 FAIL (two summary lines claim more than cards) | G5 PASS (v3_run.R:88,129,147; v3_preprocess.R:106; v3_fit.R:16,28; B_MAX line drift)
DIMENSIONS: fidelity 8.5 | completeness 9.0 | actionability 8.5 | agent-readiness 8.0 | calibration 8.5 | clarity 8.0
QUESTION_BANK: 29/30 (Q27 partial: PC1 claim 4 replacement wording missing)
NEXT_STEP_TEST fetched facts: L-DIL undefined; TD′∞, Lat(S°), S° definitions; N9 §3 prefix-identity proof text; STAB-LH condition; Thm5-LH proof text.
ISSUES:
1. [major][G4] 04_theory.tex:27 TH01 overview "with declared stacking → h(S₀)" for any data; that is M1(i), asymptotic under T03♯ hyps + osc d = O_P(1) + R′_n. -> qualify.
2. [major][G4] 04_theory.tex:838 regime plain box "reported model equals S₀ with probability tending to one … jointly with output" — round-1 overclaim again. -> joint-error wording; grep all summaries.
3. [minor][agent-readiness] TD′∞, Lat(S°), S°, Φ(C) centre, STAB-LH, L-DIL missing from Appendices A/D. -> add rows quoting sources.
4. [minor][contradiction] DEC01 (06:16), DEC03 box (06:37), history timeline (05:31) cite AUTHORING.md for approval, not sources/approval_2026-11-07.md (which also says DEC03 not covered). -> repoint.
5. [minor][contradiction] singleton qualifier missing at 05_history.tex:182 and registry EMP25 regime. -> add.
6. [minor][completeness] Q27: transcribe PC1 claim 4 corrected wording (METHOD_v3.1_FINAL.md:173) next to RF233.
7. [minor][clarity] 75 overfull boxes (worst ~40 pt), optional.
STRENGTHS: exact transcription and statuses; disclosed abridgements; byte-identical tables; code-verified divergences; UNCERTAIN boxes; frontier and regime map make it close to a start-proving document.

## Lead's actions after round 2
- Sol 1: T03♯ plain reading now states θ_j*² ≥ cσ² log n/(nφ₀²) for fixed c > c₀, the J_n(c) mass bound, and vacuity for empty J_n(c).
- Sol 2: §5 divergence box distinguishes the archive cutoff from the 2026-11-07 observation (OPEN, unmerged) and points to DEC09.
- Opus 1: TH01 overview row now separates fixed-data μ̂(h) → π(h) (R′ → ∞, cited) from the asymptotic M1(i) limit under its hypotheses.
- Opus 2: regime plain box now uses the joint-error wording; delivery not claimed.
- Opus 3: delegated to the overreach auditor (notation rows with sources).
- Opus 4: all approval citations point to sources/approval_2026-11-07.md; DEC03 box cites line 6 (placement not covered).
- Opus 5: singleton qualifier added at 05_history CE213 line and registry EMP25 regime.
- Opus 6: PC1 claim 4 wording transcribed after RF233 (METHOD_v3.1_FINAL.md:173).
- Opus 7: deferred (cosmetic).
- Systemic: an independent Opus auditor is checking every summary-type line (plain/agentnote/notproved boxes, overview and map tables, brief, frontier summaries, glossary, notation, registry short/regime columns) against its card before round 3.
- During round 2 the lead also added to FR04 the N1 route text (THEOREM_LIST_FINAL.md:119) and the N9 report's state-independence statement (N9-KERNEL/REPORT.md:47-49), labelled as the lead's reading where it compares them.
