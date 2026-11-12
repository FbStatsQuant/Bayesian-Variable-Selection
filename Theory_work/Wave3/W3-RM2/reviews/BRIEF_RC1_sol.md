# BRIEF — reconciliation review RC1 (seat: Codex gpt-6.1-sol, reasoningEffort high)

You are an independent reconciliation reviewer for theory ticket W3-RM2 of the SMC-BVS project. This file is your
whole brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (all paths below are relative to it).
**Change no git state. Write exactly one file:** `Theory_work/Wave3/W3-RM2/reviews/RC1_reconciliation_sol.md`. Do not
edit any other file. Do not start subagents. Use no effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_RC1.txt`. Its first line is
`MANIFEST 94c0349e10ddd9354fe9317803559f78d8d05f1682bf8e5d2d10e3f1a863c735`. **Quote this digest line verbatim at the
top of your review.** You may run `python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2
Theory_work/Wave3/W3-RM2/reviews/MANIFEST_RC1.txt` (from the worktree root) and report its result.

## Files you may read
* the files listed in the manifest: `Theory_work/Wave3/W3-RM2/STATEMENT.md` (now v1.1 — the object under review),
  `PLAN.md`, `BRIEF.md` in the same folder, and the 31 external inputs listed in
  `Theory_work/Wave3/W3-RM2/reviews/INPUTS.txt`;
* the earlier statement-lock review `Theory_work/Wave3/W3-RM2/reviews/SL1_statement_lock_sol.md` (on the previous
  manifest) and the lead's disposition `Theory_work/Wave3/W3-RM2/reviews/SL1_disposition.md`.
Do not read any `LOG.md`, any `CHECKPOINT*.md`, any other review folder, or anything under
`C:/Users/felip/BVS-wt/W3-MEMO-SCR-RM`.

## Task
The statement-lock review SL1 returned LOCK WITH CHANGES with six required changes (2 MAJOR, 4 MINOR) and four
optional suggestions. The lead says all ten were applied in v1.1 (markers [SL1-#] in STATEMENT.md). Nothing in the
statement is proved yet; this is still a target.
1. For **each** of the six required changes and each of the four optional suggestions, check the new text against
   what SL1 asked and give a verdict: RESOLVED / PARTIALLY RESOLVED / NOT RESOLVED, with file:line evidence and, if
   not fully resolved, the exact text change you require.
2. Check that the changes introduced **no new defect**: an inconsistent constant or quantifier (in particular δ₀, δ,
   δ₁, b, h, ρ across §3, (C3)(c), (C4), (P9) and the registry block), a broken cross-reference, a hypothesis that
   silently became stronger or weaker than SL1 reviewed, or a registry row that misstates a claim. In particular:
   * (W-unif) with parameter δ ∈ (0, (1 − 2b)/2): does it imply (W) with δ₀ = δ for large n, and is the chain
     (W-ref) ⇒ (W-unif) with δ = (1 − 2b − 2h)/4 ⇒ (W) correct with these constants?
   * "(D-R^b) is sufficient for (W-R) for every fixed δ₀ ∈ (0, 1 − 2b)": consistent with (C2), (C4) and (P9)?
   * the registry block §7: do the headline rows now list exactly the hypotheses of (C1) and (C2); are the
     sufficient forms registered as alternatives; do the `depends_on` edges cover every bridge the claim uses
     (PROTOCOL rule 16); are the sharpness/binding entries no stronger than what the statement claims?
3. State whether, in your judgement, v1.1 can be **locked as it stands**, or list the remaining required changes
   (classified CRITICAL / MAJOR / MINOR). Do not propose a different theorem.

## Output format (in your one file)
```
MANIFEST <digest>
Per-finding verdicts: R1 … R6, O1 … O4 — each RESOLVED / PARTIALLY RESOLVED / NOT RESOLVED, with evidence.
New defects: numbered, classified, with location and the exact change required (or "none found").
Lock verdict: LOCK | LOCK WITH CHANGES | DO NOT LOCK
Checks performed / not checked.
```
End your reply with the lock verdict line and the path of your file.
