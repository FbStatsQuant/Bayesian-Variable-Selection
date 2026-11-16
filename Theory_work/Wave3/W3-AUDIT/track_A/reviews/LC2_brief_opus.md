# LC2 brief — blind line check of track-A lemmas T3 (OPC), T4 (ENC), T5 (CAL-C), T10 (P1/S.3 re-audit)
(Claude Opus 5.5, high; fresh agent)

You are an independent line checker and have never seen this work. Read only the files below; do not open any LOG,
CHECKPOINT, INDEX, CHECK, AUDIT or `reviews/` file. Write no files; change no git state. Your job is to **break** these
lemmas.

Workspace: `/home/fb31/BVS-wt/W3-AUDIT`.
- `Theory_work/Wave3/W3-AUDIT/track_A/T3_OPC/{STATEMENT,PROOF}.md`, `.../T4_ENC/{STATEMENT,PROOF}.md`,
  `.../T5_CAL/{STATEMENT,PROOF}.md`, `.../T10_P1S3/{STATEMENT,PROOF}.md`.
- They cite two sibling lemmas as inputs; you may read them to see what is assumed, but do not review them:
  `.../T1_GW/STATEMENT.md` and `.../T2_BLK/STATEMENT.md` (and `.../T9_TDP/STATEMENT.md` for T10's X9).
- The code of record `Scripts/SMC_BVS/core/` (registry method pin 4676af6; `git diff --quiet 4676af6 HEAD --
  Scripts/SMC_BVS/core` confirms). Read the code yourself; do not trust the line quotes.
- Every source each STATEMENT cites (open them to check faithfulness).

For each item check:
1. **Correctness:** every step; every code citation says what the proof claims; nothing in the code contradicts a
   claim (T3: a way a completed run skips LS0, interrupts it, uses other options, or leaves an LS0-scored model out of
   the ledger; LS0's rules differing from the abstract search; T4: a field not set as stated, or the start object
   changed after setup; T5: a stream outside 0–9 read before calibration returns, a final-run setting not determined
   by the calibration record, a measurability gap; T10: an exit of `v3_fit` missing from the map, a mis-located line,
   a wrong "unreachable", and the D1 claim).
2. **Strength:** no clause claims more than is proved; every hypothesis used is stated.
3. **Faithfulness:** each statement discharges the premise as the cited downstream statements use it.

Reply (plain markdown, as your final message): per item a verdict `VERIFIED` / `VERIFIED WITH AMENDMENTS` /
`NOT VERIFIED`, then numbered findings tagged **C**, **S**, **F** or **E** with file:line, what fails, and the fix.
Last line: `LC2-VERDICT: T3=<…>; T4=<…>; T5=<…>; T10=<…>`.
