# Pre-Lean BLIND API batch: results (HQ, 2026-11-18)

- **Batch:** msgbatch_01W9r1RmBSAG84ErfrkwviUN. 12 requests, built from theory/prelean-blind b6950652 (= main 97f9c8c3 text, after the pre-Lean correction batch). Model claude-fable-5-2, effort high, max_tokens 128k. Two independent blind samples (s1, s2) per target. No repo context, no reviews.
- **Cost:** 851,608 input + 511,472 output tokens, about **$13.64** at batch rates (USAGE.txt). All 12 requests ended with end_turn.
- **Verdicts (VERDICTS.tsv):** FINDINGS=0 on every audited claim in T1 (Thm 3(a)), T3 (Hellinger reduction / DIST-C / Cor-C), T4 (Thm 1 via POST2:C/E, Thm2SG, B3w, ExSG), T5 (Thm 9, 9B, Cor 9C), T9 (Thm 10 / R4), and on RM2-F-plus and RM0-plus (T8), in BOTH samples.
- **One exception:** PB-T8-s1 reports **W3-RM2-R:DLV-0 FINDINGS=2** (both GAP, delivery clause); PB-T8-s2 reports 0 on the same claim.
  - (1) The resource-exit exclusion is not covered by the consumed Lemma R / Corollary R (Q5_dlv0.md:59-67).
  - (2) Lemma E4 is used outside DLV-0's stated hypotheses (Q5_dlv0.md:100-103).
  - Routed to Theory's triage (Fable card + acceptance filter); DLV-0 is in the A re-pin batch.
