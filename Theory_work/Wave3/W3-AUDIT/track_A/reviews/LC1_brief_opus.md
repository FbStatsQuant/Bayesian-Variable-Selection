# LC1 brief — blind line check of track-A lemmas T1 (GW) and T2 (BLK) (Claude Opus 5.5, high; fresh agent)

You are an independent line checker. You have never seen this work. You get the files below and nothing else; do not
read any LOG, CHECKPOINT, INDEX, AUDIT or review file. Your job is to **break** these two lemmas.

Workspace (read only; write nothing): `/home/fb31/BVS-wt/W3-AUDIT`.
- `Theory_work/Wave3/W3-AUDIT/track_A/T1_GW/STATEMENT.md`, `.../T1_GW/PROOF.md`
- `Theory_work/Wave3/W3-AUDIT/track_A/T2_BLK/STATEMENT.md`, `.../T2_BLK/PROOF.md`
- The code of record: `Scripts/SMC_BVS/core/` (registry method pin 4676af6; you may confirm with
  `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core`). Read the code yourself; do not trust the proofs' line quotes.
- The sources each STATEMENT cites for the premise (open them to check faithfulness).

For each lemma check:
1. **Correctness:** every step; every code citation says what the proof claims at that line; nothing in the code
   contradicts a claim (e.g. a guard/check site the proof missed, a clock value that does reach a decision, a fired check
   that can still end in output, a stream read by a check; for BLK, an empty or oversize block, a dependence on y or a
   stream, a wrong B).
2. **Strength:** the statement claims no more than the proof shows; every hypothesis used is stated.
3. **Faithfulness:** the statement is what the cited premise (GUARD-W; A:BLOCK-LE-16) needs as used by the cited
   downstream statements.

Reply format (plain markdown):
- Per lemma: a verdict `VERIFIED` / `VERIFIED WITH AMENDMENTS` / `NOT VERIFIED`, then numbered findings, each tagged
  **C** (correctness), **S** (strength), **F** (faithfulness) or **E** (editorial), with file:line and what fails and,
  where you can, the fix.
- A last line `LC1-VERDICT: T1=<verdict>; T2=<verdict>`.
