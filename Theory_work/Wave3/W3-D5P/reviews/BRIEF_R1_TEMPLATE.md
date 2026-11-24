# BRIEF R1 — council round R1, ticket W3-D5P (Tier B corollary), seat __SEAT__ (__MODEL__); fresh, blind first read

You are one of two council seats for ticket W3-D5P. You have never reviewed this ticket. Work read-only in
`/home/fb31/BVS-wt/W3-D5P` (paths relative to it); **write nothing anywhere** (no scratch files, no TMPDIR); do not change
git state. **Blind first read:** read the frozen content and the sources it cites; do **not** read
`Theory_work/Wave3/W3-D5P/LOG.md`, any `CHECKPOINT_*`, or anything under `Theory_work/Wave3/W3-D5P/reviews/` except this
brief and `reviews/MANIFEST_R1.txt` (earlier reviews, dispositions and scores are not for you).

## What is frozen (`reviews/MANIFEST_R1.txt`, digest __DIGEST__)
The ticket folder `Theory_work/Wave3/W3-D5P/` (STATEMENT.md v1.1 — claims LIST-K, LIST-CODE, LIST-R; TARGET.md;
REPORT.md with its REGISTRY blocks; CARD.md (card text proposal); READER_DELTA.md; DEPS.tsv; PLAN.md; lemmas/L1–L3;
numerics/; sources/SPEC_LIST_PIP_523dda23.md, a byte-identical carrier copy of the definition of the new output fields;
citecheck.py) plus the external inputs listed in the manifest (W3-RM2-R, W3-RM, W3-RM2 statements; C-DLV L2/L4;
W3-SAMP statement and CC code check; W2-APP L1_POST; W3-DIST statement; W3-READER READER_VERSIONS and CLAIMS_CARD; the
pinned core `Scripts/SMC_BVS/core`, identical to commit 4676af6). `python Theory_work/Wave3/tools/manifest.py verify
Theory_work/Wave3/W3-D5P Theory_work/Wave3/W3-D5P/reviews/MANIFEST_R1.txt` must pass on what you read.

## Context in one paragraph (the lead's, not a conclusion)
The method prints a reported model (`hpm`) and returns a list `top_store` of at most 40p + 1 best-scored models. New
output fields (`pip_list`, `mpm_list`, `log_Z_list`) renormalise the posterior to that list (SPEC). The ticket claims that
on Theorem 6's data event (card row 3.1, master W3-RM2-R:RM2-R-plus) every run that produces output has the true model in
its list and that these fields are within 1 − π(S₀ | y) of the truth, with rate √(log n/n). The implementation of the
fields is pending (premise IMPL-LIST).

## Claims to decide (per-claim table `| id | decision |`, ACCEPT / REJECT / NOT-EXAMINED)
W3-D5P:LIST-K, W3-D5P:LIST-CODE, W3-D5P:LIST-R (statements: STATEMENT.md §§1–4; proofs: lemmas/L1–L3; registry
blocks: REPORT.md §5). Consumed registry rows, statuses verbatim: W3-RM2-R:RM2-R-plus@1.0.1, W3-RM2-R:RM0-plus@1.0.1,
W3-RM2-R:DLV-0@1.0.1 "PROVED-CHECKED; council R3, MANIFEST 5d6d3c90… (= R3 b06a8588 re-frozen as R3r), sol=9.5 PASS,
opus=9.4 PASS" (each); W3-SAMP:CC@1.1.2 "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)"; W2-APP:POST@1.0.7
"PROVED-CHECKED"; W3-RM:RM-0@1.0.0 "PROVED-CHECKED". LIST-R is judged as conditional on IMPL-LIST (a named code premise).

## Your job
Break it. A finding blocks only if it is **C** (a step is wrong or unproved), **S** (a text claims more than is proved,
or uses a hypothesis it does not state) or **F** (unfaithful to the code as pinned, to a cited source, to SPEC, or to
STATEMENT in a derived text — REPORT, REGISTRY blocks, CARD.md, READER_DELTA.md). Everything else is **E** (editorial;
never blocks). Tag every finding C, S, F or E with file:line, what fails and a fix. "A stronger theorem is provable" is
not a finding (say it in a separate note). For LIST-CODE, open the cited code lines and look for a missed code path
(another writer of the HPM or of `top`, an `emit = false` evaluation, "completed" without LS0, a cache entry without an
offer, an eviction of the best entry).
**Interpretive sentences (HQ rule).** List every "hence / i.e. / in particular / consequently / so that" sentence inside
the claim spans (C1)–(C3) of STATEMENT and give each a verdict (proved by the cited step / not proved).
**Sweep duties (Tier B; part of your review):** (1) statement copies against the lemmas (each clause of (C1)–(C3) vs the
lemma that proves it); (2) quantifiers and uniformity (every admissible run, either branch, one data event, t ∈ (0, ½),
p ≥ 2 for the rate, the NA qualification); (3) each lemma's scope against its downstream use (L3 uses L1, L2);
(4) REPORT and its REGISTRY blocks against STATEMENT (REPORT restates nothing; ids, line pointers, statuses, conditions);
(5) DEPS.tsv rows spot-checked (sha256 prefixes against the files); (6) CARD.md and READER_DELTA.md against STATEMENT
(hypotheses stated as "those of Theorem 6", nothing added; no clause beyond LIST-R).
**The six gates** — PASS / FAIL with one line each: correct, strength, faithfulness, lit (TARGET parity rows fair),
necessity (no unproved necessity claims), better (no credible strictly better statement within scope without a
disposition in TARGET.md §4).
**Binding rule: you MUST give `gates=FAIL` if you hold any C, S or F finding of your own**, whatever severity you would
give it. Score 0.0–10.0 reflects C, S and F only.

## Reply format
1. Per-claim table. 2. Findings, numbered, tagged. 3. Interpretive-sentence list. 4. Sweep duties (1)–(6), one short
paragraph each. 5. The six gates. 6. The verdict line below, exactly once.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST __DIGEST__` (round R1, seat `__SEAT__`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=__DIGEST__ seat=__SEAT__ score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
