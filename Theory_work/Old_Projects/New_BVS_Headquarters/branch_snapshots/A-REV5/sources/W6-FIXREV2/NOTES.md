# W6-FIXREV2 — working notes

Run of 2026-11-02, branch `theory/W6-FIXREV2` (from `theory/campaign` @ af634b2).
Task: apply A-REV2 (`theory/A-REV2`, REVIEW.md) to T03♯, refined T37 (Theorem A), EXP′ and Lemma U.

## Sources read (branch heads fetched 2026-11-02)
- A-REV2 REVIEW.md (the review being applied).
- W1-T03R PROOF.md / REPORT.md; W2-VT03R REPORT.md (R1, R2, Lemma A1, Prop. W, Prop. D′).
- W1-T37R PROOF.md; W3-VT37R REPORT.md / REPAIRS.md (R1–R6).
- W1-EXP PROOF.md; W3-VEXP REPAIRS.md (R1–R4, Prop. D).
- W2-PREM PROOF.md §§0–3, 6.3–6.4 (Lemma U and its users).
- Downstream: W4-T38FULL (T38_STATEMENT, T38_PROOF, REPORT), W3-PXN PROOF §9, W3-PGD PROOF §§0–6,
  W2-T26 PROOF/REPORT, F-REFINE CARDS.md.
- Engine: `Scripts/SMC_BVS/core/cpp/v3_engine.h::local_search` (tie rule = `lex_less` on sorted index vectors,
  "proper prefix first"; strict `best.F > C.F` for a move; one extra scan at the cap returns `best` with local_limit).

## Plan
1. Independent scripts (fixed seeds) reproducing every A-REV2 counterexample I rely on, plus checks of the repaired
   statements (tie-aware TD′ equivalence; three-way failure partition; C3 lower bound under μ ∈ span X_T;
   κ limit 0.51/c_*; T03 thresholds).
2. CHANGELOG (item | A-REV2 verdict | fix | downstream) → REPORT.md.
3. STATEMENTS.md: paper-ready T03♯, Theorem A (tie-aware), EXP′ (+ Theorems 3/4 scope), Lemma U (budgeted).

## Log
- Scripts written and run: core.py, t37_checks.py, t37_extra.py, lemmaU_checks.py, t03_thresholds.py (all outputs in results/).
- All A-REV2 counterexample numbers reproduced to 10 digits; T03 thresholds match V03 R1 to the integer.
- New: Lemma NT (ties null under full-rank unions), Prop. F (three-way failure partition), budgeted Lemma U, C3-low′.
- Downstream finding outside A-REV2's list: W3-PXN §9.1 (U1) "≤ 1" is false (constant only).
- Engine check: final local search is the last scoring call; `hpm_before` records F_pre (v3_core.cpp).
- Pushed to theory/W6-FIXREV2 as instructed by HQ (the harness-designated claude/ branch was not used).
