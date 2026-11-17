# BRIEF — council diff round V-R3, seat `opus` (Claude Opus 5.5 (high)) — W3-AUDIT track V: V1 (Lemma VIS)

Second diff round (after V-R2's E items) (PROTOCOL_v4 §5.5; Dept D91: a diff-only re-check goes to an Opus seat alone). Work only
inside `/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-AUDIT/track_V/reviews/VR3_council_opus.md`. Edit nothing else; start no subagents.

## Frozen content
`Theory_work/Wave3/W3-AUDIT/track_V/reviews/MANIFEST_VR3.txt`, first line `MANIFEST aee579132aa33715622da7d337d485dd4e7db4303442066a02d3e885eb899f17`; verify with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_V Theory_work/Wave3/W3-AUDIT/track_V/reviews/MANIFEST_VR3.txt`.

## Files you may read
Everything the V-R2 brief allowed (`reviews/BRIEF_VR2_opus.md`), plus `reviews/VR2_council_opus.md` (your V-R2 review:
9.4 PASS with E items N-1–N-4), `reviews/VR2_disposition.md` and the diff `reviews/DIFF_VR2_to_VR3.patch`.

## Task
1. For each V-R2 E item (N-1–N-4): RESOLVED / NOT RESOLVED, with the line.
2. Read every hunk of the diff for a new error, a claim stronger than proved, or a design statement that disagrees with
   the lemma, B8 or track C. Unchanged text was accepted in V-R2.
3. Gates G1–G6 on the changed content; `gates=FAIL` if you hold a C, S or F finding.

## Output (your one file)
Finding table; diff-hunk verdicts; gate table; claim table `| V1 | ACCEPT/REJECT |`; score x.y / 10. End with exactly ONE
line of its own:
```
COUNCIL-VERDICT round=R3 manifest=aee579132aa33715622da7d337d485dd4e7db4303442066a02d3e885eb899f17 seat=opus score=<x.y> gates=PASS|FAIL
```
Write no other line containing `COUNCIL-VERDICT`.
