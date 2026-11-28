# COUNCIL RECORD — TH-SONG-ASSUMPTIONS

Council: Opus 5.5 (claude-opus-5-5, effort high), Neon (gemini-4-neon, thought_level high) and Sol (gpt-6.2-sol, reasoningEffort high).
Bar: every assumption scores ≥ 8.5 on D and R, with no open blockers, in at most 3 rounds. Nitpicks are declined with a one-line reason, and any score penalty driven only by nitpicks is disregarded.

## Pre-council advisor rounds (context)
- **DESIGN_MEMO_R0** → Astra R1 and Fable R1, run independently. Both converged on:
  - the selection margin with a width allowance;
  - dropping the eigenvalue floors;
  - the BB(1, p^u) correction.
- **Astra R2** reviewed the integrated draft and made five substantive corrections, all applied in v1.1 (commit 5b62aaa9):
  - TD′ becomes a high-risk conjecture;
  - A-MARGIN-U is restated in the R2 form;
  - the converse needs A-NEC on T and gives liminf ≥ Φ(−c);
  - the finite-n companion is withdrawn and becomes a diagnostic;
  - SUBG does not imply SL Condition 3, so A-MARGIN-H supplies R;
  - TM-a0 now has one fixed law and uses E[Z_j²u²];
  - A-BS′ is recorded but not adopted.

## Round 1 (package v1.1, commit 5b62aaa9; dispatched 2026-11-27)
_Pending seat reports: council/R1_OPUS.md, council/R1_NEON.md, council/R1_SOL.md._
