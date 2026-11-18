# BRIEF — council round R2 (diff round, PROTOCOL_v4 §5.5), seat `opus` (Claude Opus 5.5, effort high, Claude Third)

You were (as a model) the `opus` seat of round R1 for ticket W3-START2-R. This is a **diff round** in a fresh thread.
Work only inside `/home/fb31/BVS-wt/W3-START2-R`. **Change no git state and write no file in the repository.** Set no
TMPDIR; scratch only under `/home/fb31/BVS-wt/W3-START2-R/.rc_tmp/` (git-ignored), deleted at the end. Do not start
subagents. Return your review as your final message (saved verbatim to `Theory_work/Wave3/W3-START2-R/reviews/R2_council_opus.md`).

## Read exactly these
1. Your own R1 review: `Theory_work/Wave3/W3-START2-R/reviews/R1_council_opus.md` (round R1, MANIFEST 1834d1c0941f297eef629337b02361097a0d2f02ae1596afeaa4bf322ebbab19).
2. The diff since R1's manifest: `Theory_work/Wave3/W3-START2-R/reviews/R2_diff.diff` — the only content change is in `Theory_work/Wave3/W3-START2-R/READER_DELTA.md`; the
   new file `Theory_work/Wave3/W3-START2-R/ERRATA.md` records editorial findings of R1 (not applied in the frozen content, PROTOCOL_v4 §5.3).
   Confirm with `python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START2-R Theory_work/Wave3/W3-START2-R/reviews/MANIFEST_R1.txt` (it should list
   exactly CHANGED READER_DELTA.md and ADDED ERRATA.md) and
   `python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START2-R Theory_work/Wave3/W3-START2-R/reviews/MANIFEST_R2.txt` (OK).
3. The dependents of the changed object: `Theory_work/Wave3/W3-START2-R/READER_DELTA.md` (whole file; it is the reader version of the headline
   statements) and the master statements it cites, `Theory_work/Wave3/W3-START2-R/STATEMENT.md` §3.2 and the proof `Theory_work/Wave3/W3-START2-R/lemmas/R3_RATE.md` R3.3, R3.6.
   No DEPS row was edited (`Theory_work/Wave3/W3-START2-R/DEPS.tsv` has no row for READER_DELTA).
Do not re-read unchanged text beyond what you need to answer, and add no new E findings.

## Questions
1. Is each of **your** R1 C/S/F findings resolved? (If you had none, say so.)
2. Does the diff break anything (in particular: does the new READER_DELTA wording claim more than R3.3/R3.6 prove)?
3. Per-claim table `| id | decision |` (ACCEPT / REJECT / NOT-EXAMINED) for the ids of `Theory_work/Wave3/W3-START2-R/REPORT.md` §3.
4. Overall score (reflects C, S, F findings only; 8.0 or more means acceptable as checked mathematics).

**You must give `gates=FAIL` if you hold any C, S or F finding of your own.**

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 90886d0690e10474a213853b690f3b1ae62ad70a3c8cdf184fe99c497d713319` (round R2, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R2 manifest=90886d0690e10474a213853b690f3b1ae62ad70a3c8cdf184fe99c497d713319 seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---
