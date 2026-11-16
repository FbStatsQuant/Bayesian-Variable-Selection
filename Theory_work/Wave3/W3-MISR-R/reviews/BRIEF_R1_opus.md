# BRIEF R1 — council seat `opus`, W3-MISR-R (saved before launch)

Claude seat: Opus 5.5 (claudeAgent_claude_third, effort high), fresh agent, blind first read. Manifest: `reviews/MANIFEST_R1.txt` = MANIFEST fadb67e8cceacbceaf7b226925155c5817aa5915b4f333542e3aef7bfba8a994.

---

You are a council seat (round R1, blind first read) for the rider ticket W3-MISR-R (Tier B, NORMAL mode) in the checkout
`/home/fb31/BVS-wt/W3-MISR-R` (read-only for you, except the one reply file named at the end). You have never reviewed this
ticket. Read only the frozen content listed in `Theory_work/Wave3/W3-MISR-R/reviews/MANIFEST_R1.txt` (every file of the
ticket folder except `reviews/`, `LOG.md` and `CHECKPOINT_*.md`, plus the external inputs listed there) and, where a
citation needs it, the files those cite. Do **not** read `LOG.md`, `CHECKPOINT_*.md` or any other file in
`Theory_work/Wave3/W3-MISR-R/reviews/` (earlier reviews, dispositions and scores are withheld from you), except
`reviews/MANIFEST_R1.txt` and `reviews/CITECHECK.txt`. Your task is to break the results.

**What to review.** `STATEMENT.md` (v1.2; a delta over the parent `Theory_work/Wave3/W3-MISR/STATEMENT.md` v1.3) states four
claims; their proofs are `lemmas/G1_min.md`, `lemmas/G2_corr.md`, `lemmas/H1_plus.md`, `lemmas/H2_uniform.md`:
- W3-MISR-R:CorG-min (STATEMENT §2), W3-MISR-R:CorGb-plus (§3), W3-MISR-R:CorH-plus (§4), W3-MISR-R:CorH-U (§5).
Also in scope: `REPORT.md` (and its REGISTRY blocks), `DEPS.tsv` (with `deps_hand.py`), `TARGET.md`, `READER_DELTA.md` (a
proposed reader version of a headline theorem, to be faithful to the masters plus bridges), `ERRATA.md`, `citecheck.py` and
`reviews/CITECHECK.txt`, `numerics/`.

**Principles (PROTOCOL_v4 §0, §5).** A finding blocks only if it is **C** (correctness: a step is wrong or unproved),
**S** (strength: the text claims more than is proved, or uses a hypothesis it does not state) or **F** (faithfulness: to
the code as pinned, to cited sources, or to STATEMENT in any derived text — REPORT, registry blocks, READER_DELTA). Tag
everything else **E** (editorial: wording, notation, record, citation form, presentation of numerics); E never blocks and
never lowers the score. "A stronger theorem is provable" is not a finding: list it separately as a better-theorem proposal.
Name the clause or `file:line` and say what fails for every C/S/F finding.

**Sweep duties (Tier B: the sweep's duties are part of this review).** Check and report on each:
1. statement copies against lemma statements (every clause of STATEMENT §§2–5 is proved, as stated, in its lemma);
2. quantifiers and uniformity (order of "for every / there is", which constants depend on what, sequence-dependent
   thresholds, measurability and null events);
3. each lemma's scope against every downstream use (G1 → G2, H1, H2; H1 → H2; G2 → H2 clause (G));
4. REPORT and the REGISTRY blocks against STATEMENT (statuses verbatim from the lemma files; statement/premise line
   ranges; conditional-on lists complete; `implies` rows true; the W3-DIST paragraph labelled HEURISTIC/OPEN and asserting
   no mathematics beyond STATEMENT);
5. DEPS rows spot-checked: recompute two or three sha values (`python3 deps_hand.py` prints them; the checked_by files
   are withheld from you, so check only that sha = checked_sha and the `uses` columns are right);
6. READER_DELTA: the proposed reader statement claims nothing beyond the masters (CorGb-plus, CorG-min examples,
   CorH-plus, CorH-U (G)) plus the bridges it lists; each bridge is correct.

**Gates.** Give PASS / FAIL with one line each for the six gates: `correct` (every claim's proof is correct), `strength`
(nothing claims more than is proved; every used hypothesis stated), `faithful` (derived texts and citations faithful),
`statuses` (statuses and conditionality carried verbatim and complete), `sweep` (the six duties above done, nothing
blocking found), `reader` (READER_DELTA = masters + correct bridges).
**You must give `gates=FAIL` if you hold any C, S or F finding of your own, whatever severity you would give it.**

**Reply format.** Write your full review to `Theory_work/Wave3/W3-MISR-R/reviews/R1_council_opus.md` (create it; write nothing else
anywhere), and return the same content as your final message:
1. Per-claim table `| id | decision |` with ACCEPT / REJECT / NOT-EXAMINED for W3-MISR-R:CorG-min, W3-MISR-R:CorGb-plus,
   W3-MISR-R:CorH-plus, W3-MISR-R:CorH-U.
2. Findings, numbered, each tagged C / S / F / E, with `file:line`, what fails and a concrete fix.
3. Sweep duties 1–6: one short paragraph each.
4. Better-theorem proposals (if any), separately.
5. The six gates.
6. A score 0.0–10.0 (reflecting C, S and F only) and the mandatory verdict line below.

## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST fadb67e8cceacbceaf7b226925155c5817aa5915b4f333542e3aef7bfba8a994` (round R1, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=fadb67e8cceacbceaf7b226925155c5817aa5915b4f333542e3aef7bfba8a994 seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
