# BRIEF — council diff round W-R2, seat `opus` (Claude Opus 5.5 (high)) — W3-AUDIT track A_W: W1 (ISL), W2 (FRZ)

Diff round after council W-R1 (PROTOCOL_v4 §5.5; Dept D91: a diff-only re-check goes to an Opus seat alone). Work only
inside `/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-AUDIT/track_A_W/reviews/WR2_council_opus.md`. Edit nothing else; start no subagents.

## Frozen content
`Theory_work/Wave3/W3-AUDIT/track_A_W/reviews/MANIFEST_WR2.txt`, first line `MANIFEST d4f6454099bf4befb7190c555eb2f65a25145ec4e4de2c2884fd8c1c9a580c8e`; verify with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A_W Theory_work/Wave3/W3-AUDIT/track_A_W/reviews/MANIFEST_WR2.txt`.

## Files you may read
Everything the W-R1 brief allowed (`reviews/BRIEF_WR1_opus.md`), plus: the two W-R1 reviews `reviews/WR1_council_sol.md`
(9.4 PASS, 1 E) and `reviews/WR1_council_opus.md` (8.1 FAIL: F1, F2, E1–E7), the lead's disposition
`reviews/WR1_disposition.md`, the diff `reviews/DIFF_WR1_to_WR2.patch` (W1, W2 between the two manifests), the items'
`CHECK.md`, and the added input `Theory_work/Wave3/W3-AUDIT/track_A_X/T14_REP/STATEMENT.md`.

## Task
1. For each W-R1 finding (Opus F1, F2, E1–E7; Sol E1): RESOLVED / NOT RESOLVED, with the line that resolves it.
2. Read every hunk of the diff: does any change introduce a new error, an unstated premise, a claim stronger than proved,
   or a misquote (in particular the new "normal termination" and "no error exit" paragraphs against the code at 4676af6,
   and every corrected locator against the cited file)? Unchanged text was accepted by the W-R1 Sol seat; re-open it only
   if a change makes it wrong.
3. Gates G1–G6 as in W-R1, applied to the changed content. You **must** give `gates=FAIL` if you hold a C, S or F finding.

## Output (your one file)
Finding table; diff-hunk verdicts; gate table; claim table `| W1 | … |`, `| W2 | … |` (ACCEPT/REJECT); score x.y / 10.
End with exactly ONE line of its own:
```
COUNCIL-VERDICT round=R2 manifest=d4f6454099bf4befb7190c555eb2f65a25145ec4e4de2c2884fd8c1c9a580c8e seat=opus score=<x.y> gates=PASS|FAIL
```
Write no other line containing `COUNCIL-VERDICT`.
