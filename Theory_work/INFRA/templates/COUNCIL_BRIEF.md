# COUNCIL_BRIEF.md — required section of every council blind brief (LIFECYCLE §4.1; Wave 3 rule 15; R03-N2)

HQ copies the block below, with `<k>`, `<seat>` and `<digest>` filled in, into every `reviews/BRIEF_R<k>_<seat>.md`
before launching a council seat. The rest of the brief follows rule 15 (blind first read: the frozen statement,
proofs and the sources the reviewer needs; never earlier reviews, dispositions or scores). `<digest>` is the first
line of `reviews/MANIFEST_R<k>.txt` (`manifest.py freeze`), frozen and committed before launch.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST <digest>` (round R<k>, seat `<seat>`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R<k> manifest=<digest> seat=<seat> score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---

HQ after the round: `python Theory_work/Wave3/tools/manifest.py bind <ticket>/reviews/MANIFEST_R<k>.txt
<sol review> <opus review>` must print `bind: OK`; it also prints the `council` value for the registry. At CP3,
`manifest.py verify <ticket> <ticket>/reviews/MANIFEST_R<k>.txt` must still pass on the final tree, and
`check.py --acceptance <ids> --record` re-checks both.
