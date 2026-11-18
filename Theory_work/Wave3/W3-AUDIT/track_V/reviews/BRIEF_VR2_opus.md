# BRIEF — council diff round V-R2, seat `opus` (Claude Opus 5.5 (high)) — W3-AUDIT track V: V1 (Lemma VIS)

Diff round after council V-R1 (PROTOCOL_v4 §5.5; Dept D91: a diff-only re-check goes to an Opus seat alone). Work only
inside `/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-AUDIT/track_V/reviews/VR2_council_opus.md`. Edit nothing else; start no subagents.

## Frozen content
`Theory_work/Wave3/W3-AUDIT/track_V/reviews/MANIFEST_VR2.txt`, first line `MANIFEST 0bc1e0b4474f34c422448fdfa25f704b5269ae8ec76fe70cd5f57e685567b946`; verify with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_V Theory_work/Wave3/W3-AUDIT/track_V/reviews/MANIFEST_VR2.txt`.

## Files you may read
Everything the V-R1 brief allowed (`reviews/BRIEF_VR1_opus.md`), plus: the V-R1 reviews `reviews/VR1_council_sol.md`
(9.5 PASS) and `reviews/VR1_council_opus.md` (8.4 FAIL: F-1, E-1–E-5), the disposition `reviews/VR1_disposition.md`,
the diff `reviews/DIFF_VR1_to_VR2.patch` (V1 between the two manifests), `V1_VIS/CHECK.md`, and the track C design
definitions `Theory_work/Wave3/W3-AUDIT/work/C_PLAN.md:8-22`.

## Task
1. For each V-R1 Opus finding (F-1, E-1–E-5): RESOLVED / NOT RESOLVED, with the line that resolves it.
2. Read every hunk of the diff: does any change introduce a new error, a claim stronger than proved, or a design
   statement that disagrees with the lemma, B8 or track C (in particular the rewritten remark classifying track C's
   designs and placements, and the new (VIS-d)(i) and (VIS-e) sentences)? Unchanged text was accepted by the V-R1 Sol seat;
   re-open it only if a change makes it wrong.
3. Gates G1–G6 as in V-R1, applied to the changed content. You **must** give `gates=FAIL` if you hold a C, S or F finding.

## Output (your one file)
Finding table; diff-hunk verdicts; gate table; claim table `| V1 | ACCEPT/REJECT |`; score x.y / 10. End with exactly ONE
line of its own:
```
COUNCIL-VERDICT round=R2 manifest=0bc1e0b4474f34c422448fdfa25f704b5269ae8ec76fe70cd5f57e685567b946 seat=opus score=<x.y> gates=PASS|FAIL
```
Write no other line containing `COUNCIL-VERDICT`.
