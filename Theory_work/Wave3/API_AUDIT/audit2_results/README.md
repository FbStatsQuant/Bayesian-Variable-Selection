# AUDIT2 results (HQ, 2026-11-16): blind Fable re-check of the W3-AUDIT v1.3 label flips
- 2 samples, max_tokens raised to 128k by HQ (the audit1 lesson); both end_turn; $2.81. Total API spend today: $10.66.
- REFUTED (count of 2 samples):
  - B5.S (2), B6.S (2), SAMP.LABEL (2);
  - HEAD.CONC (2), HEAD.S (2), HEAD.H (1);
  - S.LOWER (2), S.UPPER (1), S.CONC (1), B4.PROOFS (1).
- UNCLEAR: B4.STATED (1).
- Note: audit2_build.py verdicts failed (it calls git show on a dept commit absent here); VERDICTS_ALL.txt was taken from the results.
