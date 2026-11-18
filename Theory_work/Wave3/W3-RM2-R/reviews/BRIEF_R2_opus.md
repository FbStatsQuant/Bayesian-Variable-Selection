# BRIEF R2 — council diff round, ticket W3-RM2-R, seat opus (Claude seat: Opus 5.5, effort high, Claude Third); fresh thread

PROTOCOL_v4 §5.5 diff round. You are the same seat model as in round R1, in a new thread. Work read-only in
`/home/fb31/BVS-wt/W3-RM2-R` (paths relative to it); do not change git state. Write no file at all.
Read only: this brief; your own R1 review `Theory_work/Wave3/W3-RM2-R/reviews/R1_council_opus.md`; the diff
`Theory_work/Wave3/W3-RM2-R/reviews/R2_diff.txt` (R1 manifest 4c2183ce…cd402 → R2 manifest e71637e0a175535f82cf9a86996974e83b968caa5df9981d97bc59b69a88190b; exactly six files
changed: TARGET.md, REPORT.md, READER_DELTA.md, H5_SUMMARY.md, ERRATA.md, numerics/RESULTS.md — STATEMENT.md and every
lemma are byte-identical to R1, which `manifest.py verify` on both manifests shows); and the DEPS dependents of the
changed objects, which are text-level only: REPORT.md's REGISTRY block against `STATEMENT.md` (lines 188-190, 197-205, 225-240),
READER_DELTA.md's bridges against `STATEMENT.md:107-112`, TARGET.md against `numerics/RESULTS.md`. You may open
`Theory_work/Wave3/W3-RM2-R/reviews/MANIFEST_R2.txt` and run
`python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2-R Theory_work/Wave3/W3-RM2-R/reviews/MANIFEST_R2.txt`.
Do not read LOG.md, CHECKPOINT files, the other seat's review, or any disposition file. Do not re-read unchanged text
and do not add E findings.

Answer: (1) for each of **your** R1 findings (C/S/F and the E ones the diff addresses): RESOLVED / NOT RESOLVED, one line
why; (2) does the diff break anything (any new C/S/F finding in the changed lines, tagged, with file:line and fix);
(3) the per-claim table `| id | decision |` (ACCEPT / REJECT / NOT-EXAMINED) for W3-RM2-R:RM0-plus, DLV-0, RM2-F-plus,
RM2-R-plus, SAND-F-c, TL-F-c, Ex-Proxy-d, Cont-plus; (4) the six gates (correct, strength, faithfulness, lit,
necessity, better) PASS / FAIL on manifest R2. **You MUST give `gates=FAIL` if you hold any C, S or F finding of your
own.** Score 0.0–10.0 on C/S/F only.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST e71637e0a175535f82cf9a86996974e83b968caa5df9981d97bc59b69a88190b` (round R2, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R2 manifest=e71637e0a175535f82cf9a86996974e83b968caa5df9981d97bc59b69a88190b seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
