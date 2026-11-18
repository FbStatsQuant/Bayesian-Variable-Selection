# BRIEF R3 — targeted re-check (candidate; launched only on HQ's order, PROTOCOL_v4 §5.8), ticket W3-D5P, seat opus (Claude Opus 5.5, effort high, Claude Personal); fresh thread

Opus-only (department manager). Work read-only in `/home/fb31/BVS-wt/W3-D5P`; **write nothing anywhere**; do not change
git state. Do not read `LOG.md`, `CHECKPOINT_*`, or files under `reviews/` other than those named here.

## Inputs
- The R2 review: `Theory_work/Wave3/W3-D5P/reviews/R2_council_opus.md` (MANIFEST 7431d66d…): one F finding (F-1, CARD.md)
  and five E findings.
- The diff since R2's manifest: `Theory_work/Wave3/W3-D5P/reviews/R3_diff.txt` (CARD.md, lemmas/L3_listR.md (0.5),
  DEPS.tsv). Frozen content of this round: `reviews/MANIFEST_R3.txt`, digest 35a027bee24df09f64dc3f3f5b5cb47de7d74b71f77817b87d782f26b5723c8a;
  `python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-D5P Theory_work/Wave3/W3-D5P/reviews/MANIFEST_R3.txt`
  must pass on what you read. DEPS dependents: CARD.md (derived text of LIST-R) and the LIST-R row (L3).

## Answer
1. R2 findings F-1 and E-1..E-5: RESOLVED / PARTLY / NOT, one line each.
2. Does the diff break anything (new C, S or F)? In particular: is L3 (0.5) still a correct derivation from IMPL-LIST as
   STATEMENT §1 states it, with the guard sentence; are CARD Options A/B now faithful to STATEMENT (C3) (data event,
   branches, NA qualification, which evidence error)?
3. Per-claim table `| id | decision |` for W3-D5P:LIST-K, LIST-CODE, LIST-R.
4. The six gates, one line each. No E findings on unchanged text.
**Binding rule: you MUST give `gates=FAIL` if you hold any C, S or F finding of your own.** Score reflects C, S, F only.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 35a027bee24df09f64dc3f3f5b5cb47de7d74b71f77817b87d782f26b5723c8a` (round R3, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R3 manifest=35a027bee24df09f64dc3f3f5b5cb47de7d74b71f77817b87d782f26b5723c8a seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
