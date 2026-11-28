# LC2 brief — blind line check of X1 (T12 identities at the pin), X3 (re-check of W3-POST:Lemma-1a'), X5 (re-check of
# W3-READER:PoolZ) (Claude Opus 5.5, high; fresh agent)

You are an independent line checker and have never seen this work. Read only the files below; do not open any LOG,
INDEX, CHECKPOINT, CHECK or `reviews/` file (other than this brief). Write exactly one file:
`Theory_work/Wave3/W3-AUDIT/track_A_X/reviews/LC2_reply_opus.md` (your full review). Change no git state; start no
subagents. Your job is to **break** these items.

Workspace: `/home/fb31/BVS-wt/W3-AUDIT`.
- `Theory_work/Wave3/W3-AUDIT/track_A_X/{X1_T12,X3_L1A,X5_POOLZ}/{STATEMENT,PROOF}.md`.
- Inputs they cite (read them): T12 `Docs/Theory/proofs/T12_T8_frozen_run_identities/{STATEMENT.md,PROOF_v6.tex}`;
  `Theory_work/Wave1/W1-N1/{STATEMENT.md,lemmas/L1_bridge.md}`; `Theory_work/Wave3/W3-SAMP/STATEMENT.md` and
  `lemmas/CC_code_check.md`; `Theory_work/Wave3/W3-POST/{STATEMENT.md,lemmas/L1a_size_tail.md}`;
  `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`;
  `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md`; the sibling lemma statements
  `Theory_work/Wave3/W3-AUDIT/track_A/{T1_GW,T5_CAL,T6_START,T7_KER}/STATEMENT.md` (to see what is assumed; do not review);
  for X5, the claim lives in the worktree `/home/fb31/BVS-wt/W3-READER` (branch `theory/W3-READER`), file
  `Theory_work/Wave3/W3-READER/STATEMENT.md` lines 12–37 (read it there).
- The code of record `Scripts/SMC_BVS/core/` (pin 4676af6 = HEAD for the core).

For each item: (1) correctness of every step (X1: each re-derived T12 lemma and the code identification (R1)–(R3) at the
pin; X3: each step of L1a′ against [P1]/[T03R]; X5: the four steps and the 𝒜° precision); (2) strength (nothing claimed
beyond what is shown; every hypothesis stated); (3) faithfulness (the item's own verdict on the re-checked proof is
right; quotes and statuses verbatim).

Reply format: per item a verdict `VERIFIED` / `VERIFIED WITH AMENDMENTS` / `NOT VERIFIED`, numbered findings tagged
C / S / F / E with file:line and the fix; last line `LC2-VERDICT: X1=<…>; X3=<…>; X5=<…>`.
