# BRIEF — diff check RC2 (seat: Codex gpt-6.1-sol, reasoningEffort high)

You are an independent reviewer for theory ticket W3-RM2 of the SMC-BVS project. This file is your whole brief. Work
only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (all paths below are relative to it). **Change no git state.
Write exactly one file:** `Theory_work/Wave3/W3-RM2/reviews/RC2_diffcheck_sol.md`. Do not edit any other file. Do not
start subagents. Use no effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_RC2.txt`. Its first line is
`MANIFEST 510e9a05ee0463e102d90c0ac2928a4bef8b8408e88bf407c216697308854bd8`. **Quote this digest line verbatim at the
top of your review.** You may run `python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2
Theory_work/Wave3/W3-RM2/reviews/MANIFEST_RC2.txt` (from the worktree root) and report its result.

## Files you may read
* `Theory_work/Wave3/W3-RM2/STATEMENT.md` (now v1.2, in the manifest) and the other files listed in the manifest;
* `Theory_work/Wave3/W3-RM2/reviews/STATEMENT_v1.1_as_reviewed_by_RC1.md` — the exact text the previous
  reconciliation review read (its sha256 is the STATEMENT.md row of `reviews/MANIFEST_RC1.txt`; check it);
* `Theory_work/Wave3/W3-RM2/reviews/RC1_reconciliation_sol.md` and `reviews/RC1_disposition.md`;
* `Theory_work/Wave3/W3-RM2/reviews/SL1_statement_lock_sol.md`, `reviews/SL1_disposition.md` (background only).
Do not read any `LOG.md`, any `CHECKPOINT*.md`, any other review folder, or anything under
`C:/Users/felip/BVS-wt/W3-MEMO-SCR-RM`.

## Task (PROTOCOL rule 15: check of a post-review change)
RC1 returned LOCK WITH CHANGES with two required items: the rest of R4 (MAJOR, record only: registry `depends_on`
edges and a status condition) and N1 (MINOR: a stale exponent equality in §6). The lead says v1.2 = v1.1 + exactly
these record changes, with one stated deviation (the edge to W3-RM:B9 is written `@hyp` instead of `@stmt`).
1. Diff the two files (e.g. `diff` or `git diff --no-index`; this reads files only). List **every** changed hunk.
2. For each hunk say whether it is (a) required by RC1 and applied correctly, (b) an editorial/record change that
   alters no hypothesis, claim, bridge statement, constant or code pin, or (c) a substantive change. Check in
   particular that §§0–4 and §6 outside the N1 phrase are byte-identical apart from the header, and that the registry
   block's edges now cover every bridge each claim uses (PROTOCOL rule 16; RC1's list).
3. Judge the deviation: is `W3-RM:B9@hyp` with "conditional on W3-RM:B9@1.0.0 …" in the status the correct encoding
   for a premise whose registry status is "PROVED (by this seat, unchecked)"
   (`Theory_work/INFRA/templates/ASSUMPTION_MAP.md:49-52`; `Theory_work/Wave3/PROTOCOL.md` rule 11)? Is anything else
   below PROVED-CHECKED now consumed without a condition (look at the new `@proof` edges to W2-LOC2:NA-R and
   W3-RM:D-loc, which the statement describes as proof templates re-run in this ticket)?
4. Give RC1's R4 and N1 a final verdict (RESOLVED / NOT RESOLVED) and one of the attestations
   `ATTESTATION: editorial/record only — v1.2 can be locked` or `ATTESTATION: substantive change — needs a fresh
   review`, with any remaining required change stated exactly.

## Output format (in your one file)
```
MANIFEST <digest>
Hunks: numbered list with classification (a)/(b)/(c).
Verdicts: R4 …, N1 …, deviation ….
ATTESTATION: …
Checks performed / not checked.
```
End your reply with the attestation line and the path of your file.
