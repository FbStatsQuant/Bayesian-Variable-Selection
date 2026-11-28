# AUDIT1 results (HQ, 2026-11-16)
- First pass: batch msgbatch_01GP6n4xTuDEFaq4HaKm14MV, $3.75. 5 of 6 stopped at max_tokens (32k); only core2-s1 is complete (18/18 NO-FINDING).
- Re-run of the 5 with max_tokens 128000 (audit1b): $4.10, all end_turn. Total spend $7.85.
- Tally of REFUTED/UNCLEAR across both core1/core3 samples, plus core2-s2:
  - core1: B5.SL (1 of 2), B6.SL (2 of 2), B7.SL (2 of 2);
  - core3: A2.SL (2 of 2), B7.SL (2 of 2), B8.IO (2 of 2; this one is in our favour: P6 fac2 and s5 are inside), B10-FL.SL (1 of 2); UNCLEAR B2.SL and B5.SL;
  - core2: 0 findings in both samples.
- All .IO design verdicts for cores 1 and 2: NO-FINDING.
- Theory triages with the audit Fable.
