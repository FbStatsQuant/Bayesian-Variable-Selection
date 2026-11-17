# BRIEF — council round XR1, seat `sol` (Codex gpt-6.1-sol (high)) — blind first read — W3-AUDIT track A_X: X1, X3, X5, T14

You are one of the two council seats for four Tier B items of W3-AUDIT track A (SMC-BVS project). Work only inside
`/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-AUDIT/track_A_X/reviews/XR1_council_sol.md`. Edit nothing else; start no subagents.

## Frozen content
`Theory_work/Wave3/W3-AUDIT/track_A_X/reviews/MANIFEST_XR1.txt`, first line `MANIFEST 0ebcb2dafa56732bb7b70f920ba3234a7ed62c6a514428162f8e4d973f907d3c`; verify with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A_X Theory_work/Wave3/W3-AUDIT/track_A_X/reviews/MANIFEST_XR1.txt`.

## Files you may read
In `Theory_work/Wave3/W3-AUDIT/track_A_X/`: `X1_T12/`, `X3_L1A/`, `X5_POOLZ/` (incl. `SOURCE_PoolZ.md`, the re-checked
claim copied verbatim), `T14_REP/` — their `STATEMENT.md`, `PROOF.md`, `CITECHECK.txt` — and `citecheck.py`; the external
inputs in `reviews/INPUTS_XR1.txt` (pinned code `Scripts/SMC_BVS/core/` at 4676af6 and the cited sources); the sibling
statements `Theory_work/Wave3/W3-AUDIT/track_A/{T1_GW,T5_CAL,T6_START,T7_KER,T9_TDP}/STATEMENT.md` (inputs, already
council-checked; not under review). **Do not read** `INDEX.md`, any `CHECK.md`, `H5_CARD_DRAFT.md`, `LOG.md`, any other
file in any `reviews/` folder, or anything else in `Theory_work/Wave3/W3-AUDIT/`: blind first read.

## What the council decides
- **X1** — T12's frozen-run identities (i.a)–(i.c), (ii) and the randomness model (R1)–(R3) hold for the final island
  of the code of record (re-check of T12's proof and of W1-N1's code bridge at the pin).
- **X3** — a further line check of `W3-POST:Lemma-1a'` (design-free size tail): verdict VERIFIED.
- **X5** — a line check of `W3-READER:PoolZ` (pooled evidence unbiased): verified for the uninterrupted run, with
  MEAS-J and joint stream independence for the joint-law form (VERIFIED WITH AMENDMENTS).
- **T14 REP** — on every input R can represent (n, p ≤ 2³¹ − 1), the two predicates A:IDEAL-W⁺ lifts are false in the
  shipped default configuration: IDEAL-W⁺ costs nothing on any input the software can receive.
You are briefed to break them. Gates (a gate PASSes only if you hold no C, S or F finding for it): G1 correctness of every
step and code citation; G2 hypotheses used = stated; G3 no hidden assumptions; G4 imports and statuses verbatim;
G5 scope and constants; G6 fidelity to the code as pinned and to the re-checked sources. You **must** give
`gates=FAIL` when you hold a C, S or F finding of your own. Tag findings C / S / F / E (E never blocks).

## Output (your one file)
Verdict summary; gate table G1–G6; per-claim table `| id | decision |` for X1, X3, X5, T14 (ACCEPT / REJECT /
NOT-EXAMINED); numbered findings with file:line and repair; overall score x.y / 10 (C, S, F only); checks performed; not
checked. End with exactly ONE line of its own:
```
COUNCIL-VERDICT round=R1 manifest=0ebcb2dafa56732bb7b70f920ba3234a7ed62c6a514428162f8e4d973f907d3c seat=sol score=<x.y> gates=PASS|FAIL
```
Write no other line containing `COUNCIL-VERDICT`. If you did not review exactly this manifest's content, write `gates=FAIL`.
