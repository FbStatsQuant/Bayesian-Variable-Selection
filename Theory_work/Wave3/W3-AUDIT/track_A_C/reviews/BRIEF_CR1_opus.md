# BRIEF — council round C-R1, seat `opus` (Claude Opus 5.5 (high)) — blind first read — W3-AUDIT track A_C: C1

You are one of the two council seats for one Tier B item of W3-AUDIT track A_C (SMC-BVS project). Work only inside
`/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-AUDIT/track_A_C/reviews/CR1_council_opus.md`. Edit nothing else; start no subagents.

## Frozen content
`Theory_work/Wave3/W3-AUDIT/track_A_C/reviews/MANIFEST_CR1.txt`, first line `MANIFEST 221ca4e1597f3c3a7cf25a76dc579986b5abdf3f4a52397d5546972677ec3cef`; verify with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A_C/C1_AUDITS Theory_work/Wave3/W3-AUDIT/track_A_C/reviews/MANIFEST_CR1.txt`.

## Files you may read
`Theory_work/Wave3/W3-AUDIT/track_A_C/C1_AUDITS/{STATEMENT,PROOF,CITECHECK}` (`.md`/`.txt`) and
`Theory_work/Wave3/W3-AUDIT/track_A_C/citecheck.py`; the external inputs in `reviews/INPUTS_CR1.txt` (pinned code
`Scripts/SMC_BVS/core/` at 4676af6; the registered audits under check `Theory_work/Wave1C/C-DLV/{STATEMENT,INVENTORY}.md`,
`lemmas/L2_degenerate.md`; FIN `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex`; the cited sibling statements, already
council-checked, not under review); the consumer Lemma DLV-0, not on this branch:
`git show e78a1055:Theory_work/Wave3/W3-RM2-R/STATEMENT.md` (lines ~140-165, 225-235) and
`git show e78a1055:Theory_work/Wave3/W3-RM2-R/lemmas/Q5_dlv0.md`. **Do not read** `INDEX.md`, `LOG.md`, any `CHECK.md`,
`P1_CONSUMERS.md`, `H5_T14_CARD.md`, any other file in any `reviews/` folder, or anything else in
`Theory_work/Wave3/W3-AUDIT/`: blind first read.

## What the council decides
**C1** — the two registered "AUDITED (code reading)" claims `C-DLV:P1-Inventory` ("every exit of `v3_fit` without
estimates is one of the listed sites") and `C-DLV:L2-S3` (D2 and the internal-invariant sites X2 unreachable), written
before LS0 shipped, hold at pin 4676af6 in the shipped default configuration after amendments A-1–A-7; A-7 (row B1′:
the SMC preflight's LS0 worst-case seconds / `ls0_archive` bytes) is the one coverage defect; and the amended audits
give DLV-0 (row 3.1, the main theorem's delivery clause) what it takes from them, with the B1′ exit excluded by DLV-0's
own (E2) through 𝒜_n's FIN A4 term P̄_LS0.
You are briefed to break it: find a reachable no-estimates exit (or error) of the shipped `v3_fit` that no row covers, a
wrong "unreachable", a wrong re-location, a trigger missing from A-7, or a gap in the DLV-0 (E2) exclusion.
Gates (a gate PASSes only if you hold no C, S or F finding for it): G1 correctness of every step and code citation;
G2 hypotheses used = stated; G3 no hidden assumptions; G4 imports and statuses verbatim; G5 scope (configuration,
options, branches, tiers); G6 fidelity to the code as pinned and to the registered texts. You **must** give
`gates=FAIL` when you hold a C, S or F finding of your own. Tag findings C / S / F / E (E never blocks).

## Output (your one file)
Verdict summary; gate table G1–G6; claim table `| id | decision |` for C1 (ACCEPT / REJECT); numbered findings with
file:line and repair; overall score x.y / 10 (C, S, F only); checks performed; not checked. End with exactly ONE line of
its own:
```
COUNCIL-VERDICT round=R1 manifest=221ca4e1597f3c3a7cf25a76dc579986b5abdf3f4a52397d5546972677ec3cef seat=opus score=<x.y> gates=PASS|FAIL
```
Write no other line containing `COUNCIL-VERDICT`. If you did not review exactly this manifest's content, write `gates=FAIL`.
