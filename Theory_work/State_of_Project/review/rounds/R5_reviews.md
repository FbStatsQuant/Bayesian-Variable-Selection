# Council round 5 (final) — replies (2026-11-07) and the lead's actions

## Result: PASSED — both reviewers ≥ 8.0 in the same round, all gates PASS for both, question bank 30/30 for both.

| Round | Sol (gpt-6.1-sol, high) | Opus (claude-opus-5-5, high) | Main changes after the round |
|---|---|---|---|
| 1 | 5.0 (G4 FAIL: TH05 overview "w.p. → 1") | 8.8 | TH05 joint-error wording; PR #1 status queried on GitHub; approval record; singleton qualifier; EMP12 UNCERTAIN; Lean wording; derived frontier ranking; overfull 157 → 75 |
| 2 | 5.0 (G4 FAIL: T03♯ plain reading dropped θ_j*², c > c₀) | 5.0 (G4 FAIL: TH01 row, regime paragraph) | T03♯/TH01/regime fixes; approval citations; PC1 claim 4 wording; independent 63-fix overreach audit; 8 notation rows |
| 3 | 5.0 (G4 FAIL: withdrawn 6-fit cap repeated) | 8.8 | withdrawn inference boxed; M1(e)/(f) "given N1"; LH variants; TH16 fallback; ABL-CONF in full; N9 proof text in FR04 |
| 4 | 5.0 (G4 FAIL: PIP field attribution) | 8.9 | PIP fields; general LH in three-layer box; TH02 step-function row; wave-1 priority row; N1 route text; GR4/GR8 quotes; exhaustive Sol G4 sweep (16 fixes, 4 rejected with objection) |
| 5 | **8.9** (all gates PASS) | **8.9** (all gates PASS) | final polish below |

## Sol R5 (8.9)
GATES all PASS; DIMENSIONS fidelity 9.0 | completeness 9.3 | actionability 9.0 | agent-readiness 8.8 | calibration 9.0 | clarity 8.0; QB 30/30.
Issues: (1) minor: 04_theory.tex:838 cites NBH/03:206 for 558.1 vs 571 (numbers at :204) → fixed (:204-206). (2) minor: 78 overfull boxes → not fixed (cosmetic).
Sol: "the sweep dispositions are sound, including the lead's newline-counting objection to items 1–4."

## Opus R5 (8.9)
GATES all PASS; DIMENSIONS fidelity 9.0 | completeness 9.3 | actionability 9.0 | agent-readiness 8.9 | calibration 9.0 | clarity 8.0; QB 30/30.
Issues (all minor) and dispositions:
1. 03_empirics "Every PIP in this section" also covers exact/benchmark PIPs → fixed: "Every SMC-BVS PIP".
2. 04b cites THEOREM_REVISION_INPUTS.md:13 for TL → fixed (:12).
3. 05_history C15 conflict lacked its own citation → added NBH/05_open_questions_and_next_steps.md:152.
4. TH07 map-row status fragments out of order → fixed to "ConjP: OPEN; […]; (c′): PROOF SKETCH (Seat C, unchecked), W2PC2 TRUE-AS-WRITTEN".
5. T27(i) premises H2/H3 not transcribed → added a verbatim stmt box (Docs/Theory/proofs/T27i_T20C_cancellation_budget/STATEMENT.md:26-49) after the M3 statement box, with the LOCKED_PROOFS status lines.
6. overfull boxes → not fixed (cosmetic).

Final build: 237 pages; check.py 0 errors; 1,685 citations resolve; coverage 100% (273/273); 117 statement boxes; tables regenerate byte-identically.
Remaining known cosmetic issue: 78 overfull hbox warnings (worst ≈ 40 pt).
