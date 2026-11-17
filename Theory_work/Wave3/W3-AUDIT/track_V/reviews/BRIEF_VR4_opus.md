# BRIEF — diff check V-R4, seat `opus` (Claude Opus 5.5 (high)) — W3-AUDIT track V: V1 (Lemma VIS), scope-text correction

After the bound round V-R3, HQ's blind API audit found the lemma's clauses clean but refuted its scope text: the "Not
claimed" bullet excluded track C's riboflavin-like design D18 for "uncountable local patterns", which is false (D18 is
built from one fixed matrix), and treated D19 (same recipe) the other way. This is a minimal correction (v1.5). Dept D91:
diff-only re-check, Opus seat alone. Work only inside `/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly
one file:** `Theory_work/Wave3/W3-AUDIT/track_V/reviews/VR4_council_opus.md`. Start no subagents.

## Frozen content
`Theory_work/Wave3/W3-AUDIT/track_V/reviews/MANIFEST_VR4.txt`, first line `MANIFEST 8a691d2a54c5f13ca164dd0617b68e7bbca893cc3058cfe8d41c0c76d7fe26f0`; verify with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_V Theory_work/Wave3/W3-AUDIT/track_V/reviews/MANIFEST_VR4.txt`.

## Files you may read
`V1_VIS/{STATEMENT,PROOF,CHECK}.md`; the diff `reviews/DIFF_VR3_to_VR4.patch`; `reviews/VR3_post_disposition.md`; the D18
computation `reviews/D18/D18_VERDICT.md`, `reviews/D18/D18C_reply_opus.md` (independent check), `reviews/D18/d18.py`,
`reviews/D18/d18_output.txt`; the design code `/home/fb31/SMC_Theory_Department/helpers/W3-AUDIT-C/nots_pkg/scripts/c_designs.py`
(`_real`, `LowRank`); `Theory_work/Wave3/W3-AUDIT/TRACK_B.md:209-233`, `Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md`.

## Task
1. Is the new "Not claimed" bullet correct (every design sequence has countably many local patterns; only an uncountable
   closure 𝒩 escapes (VIS-c); (VIS-b) still applies when δ > 0; D18, D19 fall under (VIS-d)(i))? Does it remove the
   refuted claim and the D18/D19 inconsistency?
2. Is the new proof remark on D18 faithful to the D18 computation (spread: four truths in four tiles for p ≥ 16352,
   a ≥ 0.1 up to 5e-14; clustered: effectively on B, |Cov| ≤ 6.9e-9 at a 15-column U, exact recomputation)? Any claim
   stronger than the computation supports?
3. Any other hunk introducing an error. Gates G1–G6 on the changed content; `gates=FAIL` if you hold a C, S or F finding.

## Output (your one file)
Finding table; diff-hunk verdicts; gate table; claim table `| V1 | ACCEPT/REJECT |`; score x.y / 10. End with exactly ONE
line of its own:
```
COUNCIL-VERDICT round=R4 manifest=8a691d2a54c5f13ca164dd0617b68e7bbca893cc3058cfe8d41c0c76d7fe26f0 seat=opus score=<x.y> gates=PASS|FAIL
```
Write no other line containing `COUNCIL-VERDICT`.
