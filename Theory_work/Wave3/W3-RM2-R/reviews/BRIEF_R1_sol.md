# BRIEF R1 — council round R1, ticket W3-RM2-R (Tier B rider), seat sol (OpenAI seat: codex gpt-6.1-sol, reasoningEffort high); fresh, blind first read

You are one of two council seats for ticket W3-RM2-R. You have never reviewed this ticket. Work read-only in
`/home/fb31/BVS-wt/W3-RM2-R` (paths relative to it); write nothing; do not change git state. **Blind first read:** read
the frozen content and the sources it cites; do **not** read `Theory_work/Wave3/W3-RM2-R/LOG.md`, any `CHECKPOINT_*`, or
anything under `Theory_work/Wave3/W3-RM2-R/reviews/` except this brief and `reviews/MANIFEST_R1.txt` (earlier reviews,
dispositions and scores are not for you).

## What is frozen (`reviews/MANIFEST_R1.txt`, digest 4c2183ce4a87dfa35cdf95977a06a85915d0c96b65b43f327de69102558cd402)
The ticket folder `Theory_work/Wave3/W3-RM2-R/` (STATEMENT.md v1.0 — a delta over W3-RM2 v1.4 and W3-RM RM-0; TARGET.md;
REPORT.md with its REGISTRY block; READER_DELTA.md; DEPS.tsv; PLAN.md; ERRATA.md; H5_SUMMARY.md; lemmas/Q1, Q2, Q4, Q5,
Q6, Q7; numerics/; citecheck.py) plus the external inputs listed in the manifest (parent statements and lemmas, C-DLV,
FINAL s6, W2-UNI/FAC-A delivery lemmas, W3-POST statement, the TH09 card, the R-AUD1 audit, the pinned core
`Scripts/SMC_BVS/core`). `python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2-R Theory_work/Wave3/W3-RM2-R/reviews/MANIFEST_R1.txt`
must pass on what you read.

## Claims to decide (per-claim table `| id | decision |`, decision ACCEPT / REJECT / NOT-EXAMINED)
W3-RM2-R:RM0-plus, W3-RM2-R:DLV-0, W3-RM2-R:RM2-F-plus, W3-RM2-R:RM2-R-plus, W3-RM2-R:SAND-F-c, W3-RM2-R:TL-F-c,
W3-RM2-R:Ex-Proxy-d, W3-RM2-R:Cont-plus (statements: STATEMENT.md §§2–6; proofs: lemmas/; registry block: REPORT.md §5).
Statuses consumed below PROVED-CHECKED are explicit conditions (SOP:TH09@1.0.0 for Form F, W2-APP:POST@1.0.1 for Form R);
DLV-0 is relative to the inherited C-DLV code-reading audits (P1, S.3). Judge the claims as conditional on those.

## Your job
Break it. A finding blocks only if it is **C** (a step is wrong or unproved), **S** (a text claims more than is proved,
or uses a hypothesis it does not state) or **F** (unfaithful to the code as pinned, to a cited source, or to STATEMENT
in a derived text — REPORT, REGISTRY block, READER_DELTA bridges). Everything else is **E** (editorial; never blocks;
it goes to ERRATA). Tag every finding C, S, F or E with file:line, what fails and a fix. "A stronger theorem is
provable" is not a finding (say it in a separate note if you like).
**Sweep duties (Tier B: they are part of your review):** (1) statement copies against lemma statements (every bridge
row and claim in STATEMENT vs the lemma that proves it); (2) quantifiers and uniformity (every seed / every admissible
run / one data event; n₀ dependence; "for every valid input"); (3) each lemma's scope against every downstream use
(Q4 (c⁺) and Q6 use Q5; Q6 uses Q1, Q2, Q4, Q7); (4) REPORT and its REGISTRY block against STATEMENT (REPORT restates
nothing; ids, line pointers, statuses, conditions, `implies` vs `depends_on`); (5) DEPS.tsv rows spot-checked
(sha256 prefixes of the files against the recorded `sha`; state OK means checked at that sha); (6) READER_DELTA's
bridges R7.1–R7.4 against STATEMENT.
**The six gates** — answer each PASS / FAIL with one line: correct (every claim's proof is right), strength (no text
claims more than is proved), faithfulness (code, sources, derived texts), lit (TARGET.md parity rows are fair),
necessity (TARGET/numerics do not claim necessity they do not prove), better (no credible strictly better provable
statement within this rider's scope is left without a disposition in TARGET.md §4).
**Binding rule: you MUST give `gates=FAIL` if you hold any C, S or F finding of your own**, whatever severity you would
give it. Score 0.0–10.0 reflects C, S and F only.

## Reply format
1. Per-claim table `| id | decision |`. 2. Findings, numbered, tagged. 3. Sweep duties (1)–(6), one short paragraph each.
4. The six gates. 5. The verdict line below, exactly once.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 4c2183ce4a87dfa35cdf95977a06a85915d0c96b65b43f327de69102558cd402` (round R1, seat `sol`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=4c2183ce4a87dfa35cdf95977a06a85915d0c96b65b43f327de69102558cd402 seat=sol score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
