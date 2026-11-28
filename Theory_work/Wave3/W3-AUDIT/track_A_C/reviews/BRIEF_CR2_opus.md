# BRIEF — council diff round C-R2, seat `opus` (Claude Opus 5.5 (high)) — W3-AUDIT track A_C: C1

Diff round after council C-R1 (PROTOCOL_v4 §5.5; Dept D91: a diff-only re-check goes to an Opus seat alone). Work only
inside `/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-AUDIT/track_A_C/reviews/CR2_council_opus.md`. Edit nothing else; start no subagents.

## Frozen content
`Theory_work/Wave3/W3-AUDIT/track_A_C/reviews/MANIFEST_CR2.txt`, first line `MANIFEST c27fb00ef1630f39b5ca8a38972c2c97df3fabc95d2d2741daedb4df3a3c492e`; verify with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A_C/C1_AUDITS Theory_work/Wave3/W3-AUDIT/track_A_C/reviews/MANIFEST_CR2.txt`.

## Files you may read
Everything the C-R1 brief allowed (`reviews/BRIEF_CR1_opus.md`), plus: the two C-R1 reviews
`reviews/CR1_council_sol.md` (9.3 PASS, no findings) and `reviews/CR1_council_opus.md` (8.5 FAIL: F1, E1–E6), the lead's
disposition `reviews/CR1_disposition.md`, the diff `reviews/DIFF_CR1_to_CR2.patch` (C1_AUDITS between the C-R1 manifest
and this one), and `C1_AUDITS/CHECK.md`.

## Task
1. For each C-R1 finding (F1, E1–E6): RESOLVED / NOT RESOLVED, with the line that resolves it.
2. Read every hunk of the diff: does any change introduce a new error, a claim stronger than proved, or a misquote
   (in particular the FIN A4 quotation, `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:37-44`, and DLV-0's words,
   `git show e78a1055:Theory_work/Wave3/W3-RM2-R/lemmas/Q5_dlv0.md` lines 59-65)? Unchanged text was accepted by both
   C-R1 seats; re-open it only if a change makes it wrong.
3. Gates G1–G6 as in C-R1, applied to the changed content. You **must** give `gates=FAIL` if you hold a C, S or F finding.

## Output (your one file)
Finding table; diff-hunk verdicts; gate table; claim table `| C1 | ACCEPT/REJECT |`; score x.y / 10. End with exactly ONE
line of its own:
```
COUNCIL-VERDICT round=R2 manifest=c27fb00ef1630f39b5ca8a38972c2c97df3fabc95d2d2741daedb4df3a3c492e seat=opus score=<x.y> gates=PASS|FAIL
```
Write no other line containing `COUNCIL-VERDICT`.
