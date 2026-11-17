# BRIEF — council diff round XR2 (after XR1), seat `opus` (Claude Opus 5.5 (high)) — X1, X3, X5, T14

PROTOCOL_v4 §5.5 diff round; you are a fresh thread of the same seat model as in XR1. Work only inside
`/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-AUDIT/track_A_X/reviews/XR2_diff_opus.md`. Edit nothing else; start no subagents.

You get: your seat's own XR1 review `Theory_work/Wave3/W3-AUDIT/track_A_X/reviews/XR1_council_opus.md` (do not open the
other seat's review or any disposition); the diff `reviews/DIFF_XR1_to_XR2.patch` (only T14 changed: STATEMENT v1, PROOF
v1, CHECK, CITECHECK); the frozen content `reviews/MANIFEST_XR2.txt`, first line `MANIFEST 5db04d3a8e3c408d826a0d28af1825dc4cad0abe345df28d55f2b8928d5c64d6` (verify with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A_X Theory_work/Wave3/W3-AUDIT/track_A_X/reviews/MANIFEST_XR2.txt`);
inputs `reviews/INPUTS_XR1.txt` (unchanged), in particular `Scripts/SMC_BVS/core/cpp/v3_start.h` for T14's new Step 3.
Do not re-read unchanged text. No other item depends on T14 inside the package.

Answer: (1) for each of your XR1 findings, RESOLVED / NOT RESOLVED; (2) does the diff break anything (new findings tagged
C / S / F only); (3) per-claim table `| id | decision |` for X1, X3, X5, T14; (4) you **must** give `gates=FAIL` if you hold
a C, S or F finding. End with exactly ONE line of its own:
```
COUNCIL-VERDICT round=R2 manifest=5db04d3a8e3c408d826a0d28af1825dc4cad0abe345df28d55f2b8928d5c64d6 seat=opus score=<x.y> gates=PASS|FAIL
```
