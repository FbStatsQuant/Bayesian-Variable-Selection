# LC3 brief — blind line check of track-A lemmas T6 (START-X), T7 (KER), T8 (OVL), T9 (TDP)
(Claude Opus 5.5, high; fresh agent)

You are an independent line checker and have never seen this work. Read only the files below; do not open any LOG,
CHECKPOINT, INDEX, CHECK, AUDIT or `reviews/` file. Write no files; change no git state. Your job is to **break** these
lemmas.

Workspace: `/home/fb31/BVS-wt/W3-AUDIT`.
- `Theory_work/Wave3/W3-AUDIT/track_A/T6_START/{STATEMENT,PROOF}.md`, `.../T7_KER/{STATEMENT,PROOF}.md`,
  `.../T8_OVL/{STATEMENT,PROOF}.md`, `.../T9_TDP/{STATEMENT,PROOF}.md`.
- Sibling lemmas they cite as inputs (read to see what is assumed; do not review): `.../T2_BLK/STATEMENT.md`,
  `.../T4_ENC/STATEMENT.md`, `.../T5_CAL/STATEMENT.md`, `.../T1_GW/STATEMENT.md`.
- The code of record `Scripts/SMC_BVS/core/` (registry method pin 4676af6; `git diff --quiet 4676af6 HEAD --
  Scripts/SMC_BVS/core` confirms). Read the code yourself; do not trust the line quotes.
- Every source each STATEMENT cites, including the earlier proofs being re-checked (N9 `PROOF.md`/`REPORT.md`,
  `C-ENG/lemmas/TDP_E.md`, `W1-N3/STATEMENT.md`, T12 `STATEMENT.md`, `W3-SAMP/STATEMENT.md`, `W3-START2-R/STATEMENT.md`).

For each item check:
1. **Correctness:** every step of the mathematics (T6: the telescoping and the index conventions of the backward
   sampler, Z̄₀; T7: each transition law and each detailed-balance identity, the neighbour-graph symmetry, Fisher–Yates;
   T8: the limit argument and the budget bound; T9: the DP, the enumeration, the greedy lex-min invariant, the cost and
   storage bounds), and every code citation against the code.
2. **Strength:** no clause claims more than is proved; every hypothesis used is stated (exact arithmetic, ideal
   uniforms, (A5) where P-START is used).
3. **Faithfulness:** each statement discharges the premise as the cited downstream statements use it, and each
   "comparison with the earlier proof" paragraph reports that proof correctly.

Reply (plain markdown, as your final message): per item a verdict `VERIFIED` / `VERIFIED WITH AMENDMENTS` /
`NOT VERIFIED`, then numbered findings tagged **C**, **S**, **F** or **E** with file:line, what fails, and the fix.
Last line: `LC3-VERDICT: T6=<…>; T7=<…>; T8=<…>; T9=<…>`.
