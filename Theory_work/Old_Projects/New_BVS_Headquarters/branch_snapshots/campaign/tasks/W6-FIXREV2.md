# W6-FIXREV2: Apply the cross-family (Astra) review A-REV2 to T03♯, the refined T37, EXP′ and Lemma U

Read `theory_campaign/A-REV2/REVIEW.md` on branch `theory/A-REV2` (GPT-6 Astra, a cross-family review).
- **Core results VERIFIED:** T03♯ and its supporting lemmas; Theorem A (refined T37) with the POS repair; EXP′ and the deterministic-chain theorems (with qualifications).
- **ERRORS and GAPS found:**
  - the T03 proof-onset claim near 1.2e5 (already corrected by W2-VT03R; confirm);
  - Lemma 0(b)'s posterior-miss inference;
  - V37 R2's failure dichotomy, which omits inferior local maxima and capped searches ending below the truth;
  - A5 without POS (confirmed false);
  - the TD′_P "iff" definition, where strict separation is sufficient but not necessary with exact ties;
  - the "weakest condition" prose;
  - the constant 0.52/c_* (should be 0.51/c_*);
  - Lemma U's extra quantifier (a GAP; the cardinality budget must include the extra sets);
  - Lemma U C3's matching lower bound, which needs μ ∈ span(X_T) (an ERROR with a counterexample);
  - random-design / actual-packing extensions of EXP′ (keep as SKETCH).

Sources: theory/W1-T03R, W2-VT03R, W1-T37R, W3-VT37R, W1-EXP, W3-VEXP and W2-PREM (folders theory_campaign/<ID>/).

**Goal:** a consolidated corrected package.
1. For each A-REV2 finding: the fix, applied in full (corrected statements and proofs), plus downstream effects. Check in particular W4-T38FULL, W3-PXN, W3-PGD, W2-T26 and F-REFINE's CARDS.md (branch theory/F-REFINE) for uses of the corrected items.
2. Write corrected, paper-ready statements of T03♯, Theorem A (T37 refined, exact-ties-aware definition of TD′), EXP′ and Lemma U, each with its precise hypotheses, in `STATEMENTS.md`.
3. Where you disagree with A-REV2, give a precise counter-argument.

**Deliverable:** `theory_campaign/W6-FIXREV2/REPORT.md` (change log: item | A-REV2 verdict | fix | downstream), plus `STATEMENTS.md` and a confidence card.
