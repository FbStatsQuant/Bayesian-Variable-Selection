# BRIEF — council round R1, seat `opus` (Claude Opus 5.5 (high)) — blind first read — W3-AUDIT track A, batch T1–T10

You are one of the two council seats for the Tier B lemma batch T1–T10 of W3-AUDIT track A (SMC-BVS project). This file
is your whole brief. Work only inside the worktree `/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly
one file:** `Theory_work/Wave3/W3-AUDIT/track_A/reviews/R1_council_opus.md`. Do not edit any other file. Do not start
subagents. If you run code, keep scripts outside the repository.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-AUDIT/track_A/reviews/MANIFEST_R1.txt`, first line `MANIFEST 01c268b030c3f12619fe885edc02483d0516038ee4e53e66b8840b14b383bc2b`. You may run
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A Theory_work/Wave3/W3-AUDIT/track_A/reviews/MANIFEST_R1.txt`.

## Files you may read
In the ticket folder `Theory_work/Wave3/W3-AUDIT/track_A/`: the twenty files `T*/STATEMENT.md` and `T*/PROOF.md`
(T1_GW, T2_BLK, T3_OPC, T4_ENC, T5_CAL, T6_START, T7_KER, T8_OVL, T9_TDP, T10_P1S3), `T*/CITECHECK.txt` and `citecheck.py`;
and the external inputs listed in `reviews/INPUTS_R1.txt` (the pinned code `Scripts/SMC_BVS/core/` at method pin
4676af6 and the sources the proofs cite). **Do not read** `INDEX.md`, any `T*/CHECK.md`, any file in `reviews/` other than
the manifest and `INPUTS_R1.txt`, `LOG.md`, any `CHECKPOINT*.md`, or anything in `Theory_work/Wave3/W3-AUDIT/` outside
`track_A/` (AUDIT.md, TRACK_B.md, …): this is a blind first read, and you must form your verdict without any earlier
review, disposition or score. The STATEMENT changelog rows name review files as triggers; do not open them.

## What the council decides
Ten Tier B lemmas close the unchecked or missing "track A" premises of the project's core theorems (the coded
algorithm reports the true model; the run's estimates are consistent and unbiased): T1 GUARD-W (stop-only run-time
guard), T2 the coded partition (blocks ≤ 16, a function of X), T3 OP-LS0 (LS0 runs as specified), T4 the start-table
encoding, T5 CAL (calibration record on streams 0–9), T6 START (exact start sampler and normaliser), T7 KERNEL (coded
moves = stated reversible kernels; uniform order), T8 P-OVL (from P-START and the budget; incl. clause OVL-d, the
uninterrupted run), T9 the tie-aware start-mode DP, T10 a second-seat re-audit of the no-output inventory P1 and of S.3.
Most are code readings under exact arithmetic (EX-A) and ideal uniforms (H-U); T6–T9 also re-check earlier proofs.
Each STATEMENT names the premise it discharges and where it is consumed. You decide, claim by claim, whether each can
be accepted as checked. You are briefed to break them: assume there is an error and look for it.

Gates (a gate PASSes only if you found no C, S or F finding of your own for it):
* **G1 correctness** — every step, every code citation against the code at the pin (read the code yourself).
* **G2 hypotheses used = stated.**
* **G3 no hidden assumptions** (e.g. a premise of T1/T5 used in T3/T8 without being stated; measurability; an
  unstated range of n, p; floating-point facts used under EX-A).
* **G4 imports and statuses** — every consumed result is cited with its recorded status, verbatim; consumers' premises
  quoted correctly (W1-N1, W3-SAMP, W3-RM, W3-RM2, W2-UNI, C-DLV, W3-START2-R).
* **G5 scope and constants** — bounds, cost and storage claims, index conventions, "for every input" quantifiers.
* **G6 fidelity to the method as coded** — each lemma is about `Scripts/SMC_BVS/core/` as pinned, in the shipped
  configuration.

You **must** give `gates=FAIL` when you hold a C, S or F finding of your own, whatever severity you would give it.
Tag every finding **C** (a step is wrong or unproved), **S** (claims more than proved, or uses an unstated hypothesis),
**F** (unfaithful to the code, a cited source, or a STATEMENT) or **E** (editorial; never blocks, never lowers the score).

## Output format (in your one file)
```
Verdict summary: one paragraph.
Gate table: G1 … G6, each PASS or FAIL with a justification naming what you re-derived or re-read.
Per-claim table: | id | decision | for T1 … T10 (ACCEPT / REJECT / NOT-EXAMINED).
Findings: numbered; each tagged C/S/F/E, with file:line, the problem and the repair you propose.
Overall score: x.y / 10 (reflects C, S, F only; 8.0 or more = acceptable as checked as it stands).
Checks performed. Not checked.
```
---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 01c268b030c3f12619fe885edc02483d0516038ee4e53e66b8840b14b383bc2b` (round R1, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=01c268b030c3f12619fe885edc02483d0516038ee4e53e66b8840b14b383bc2b seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict.
