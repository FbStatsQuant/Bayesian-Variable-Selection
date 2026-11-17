# BRIEF — council diff round R2 (after R1), seat `opus` (Claude Opus 5.5 (high)) — W3-AUDIT track A, batch T1–T10

PROTOCOL_v4 §5.5 diff round. You are a fresh thread of the same seat model as in round R1. Work only inside
`/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-AUDIT/track_A/reviews/R2_diff_opus.md`. Do not edit any other file; start no subagents.

## What you get
- Your seat's own R1 review: `Theory_work/Wave3/W3-AUDIT/track_A/reviews/R1_council_opus.md` (R1 manifest
  `MANIFEST_R1.txt`, digest 01c268b0…). Do not open the other seat's review or any disposition.
- The diff since R1: `Theory_work/Wave3/W3-AUDIT/track_A/reviews/DIFF_R1_to_R1d.patch` (git diff of the ticket folder,
  reviews/LOG/CHECKPOINT excluded). Changed: T2 (v6), T8 (v4), T9 (v3), T4 (v3), T6 (STATEMENT v2.1), new
  `STATUS_EXTRACT.md` and `ERRATA.md`, CHECK.md lines (T2, T4, T6, T7, T8, T9) and CITECHECK files.
- The frozen content of this round: `reviews/MANIFEST_R2.txt` (= `MANIFEST_R1d.txt`), first line
  `MANIFEST 93b6cfc7c2451428ff253b282561225273b9e54cf227520a6a80a1433a8110ff`; verify with `python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A
  Theory_work/Wave3/W3-AUDIT/track_A/reviews/MANIFEST_R1d.txt`. External inputs: `reviews/INPUTS_R1d.txt` (same as R1).
- Dependents to re-read where they use a changed object (do not re-read unchanged text otherwise): T2 → T4 (blocks),
  T6 (blocks), T10 §2 (i); T4 → T6, T9 setting, T3 (start mode); T9 → T10 X9; T8 → none inside the package (consumer:
  W3-SAMP Theorem D (D-iv)).

## Answer
1. For each of your R1 findings: RESOLVED / NOT RESOLVED (what is still wrong).
2. Does the diff break anything — in the changed files or in the dependents listed? Tag any new finding C / S / F (no
   new E findings in a diff round).
3. Per-claim table `| id | decision |` for T1 … T10 (ACCEPT / REJECT / NOT-EXAMINED); an unchanged claim you accepted
   in R1 stays ACCEPT unless the diff breaks it.
4. You **must** give `gates=FAIL` if you hold a C, S or F finding of your own.

## Verdict line (mandatory, machine-checked)
End with exactly ONE line of its own:
```
COUNCIL-VERDICT round=R2 manifest=93b6cfc7c2451428ff253b282561225273b9e54cf227520a6a80a1433a8110ff seat=opus score=<x.y> gates=PASS|FAIL
```
Write no other line containing `COUNCIL-VERDICT`. If you did not review exactly this manifest's content, write
`gates=FAIL`.
