# BRIEF R3 — council seat `sol` (diff-only confirmation round) — W3-READER

You are one of two council seats (gpt-6.1-sol, reasoning effort high). Round R2 PASSED (sol 9.3, opus 9.3, MANIFEST_R2 3af23c35…, reviews
`reviews/R2_council_sol.md`, `reviews/R2_council_opus.md`). R3 confirms only the post-R2 editorial changes so that the
bound text is the corrected one.

## Content under review (frozen as `MANIFEST 7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263`, file `Theory_work/Wave3/W3-READER/reviews/MANIFEST_R3.txt`)
**Review only the R2 → R3 diff**: `Theory_work/Wave3/W3-READER/reviews/R3_diff_R2_to_R3.diff` (= `git diff ae8acc8e 68443dcc`
on the ticket folder, reviews/ and LOG.md excluded). The 14 items, each tagged in the text:
| tag | file | change |
|---|---|---|
| R2-O1 / R2-E2(sol) | CLAIMS_CARD row 3.5 | single conditioning: "On calibration success, given the frozen calibration and the data, …" |
| R2-O2 | READER_VERSIONS thm1 remark (vi) | domain pointer "$s_0\le K-1$ suffices, by Corollary B with $c(p,s_0)\ge1$ or by Prop. LB" |
| R2-O3 | METHOD_INTUITION §3 | "mass at least $1-n^{-c}$" (two places) |
| R2-O4 | READER_VERSIONS thm7 (A5)(b) | $C_Q$ example "any fixed $C_Q>\max\{32,64A+c\}$ with $c$ as in Remark (a)" |
| R2-O5 | STATEMENT bridge table | R1 used by Thms 1, 2, 3, 4, 6, 10 |
| R2-O6 | READER_VERSIONS thm6 remark (iii) | `W3-RM2:Ex-PolyR@1.0.3` status verbatim |
| R2-O7 | lemmas/R4 "Not claimed" | completion via `W3-RM2-R:DLV-0` (F-UNI Step 2 as history) |
| R2-O8 | METHOD_INTUITION §4 | unbiasedness scoped: "the uninterrupted final run's estimate, given the calibration" |
| R2-O9 | REPORT PoolZ conclusion | "potential record, data fixed; equals the printed field on completed runs" |
| R2-O10 | CLAIMS_CARD v1.8 changelog | original history text restored (its correction stays in v1.11) |
| R2-E1(sol) | CLAIMS_CARD row 3.1 bridge column; READER_VERSIONS B7.2, B7.3 | "NEW bridge R2; delivery identity B6.6′; R3 historical"; old BM commentary labelled historical, truth removal via B7.2′/B7.3′ |
| R2-E2(sol) | READER_VERSIONS thm10 honest limits | exact ratio $e^{C\sqrt{\log n}}/\sqrt{\log n}$ to the posterior rate |
| R2-L1 (lead) | READER_VERSIONS thm10 honest limits | "row 3.5 applies there, and row 3.1 for particular AR or block designs that satisfy Theorem 6's conditions" (same scope as card row 3.6 after R1-F5) |
| GUARD-W (HQ/manager) | READER_VERSIONS thm7 after the delivery display; CLAIMS_CARD row 3.2 | "The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and no output." (as already in rows 3.1, 3.5, 3.6, reviewed in R2) |
Also: update-log lines, card v1.12 header, DEPS.tsv regenerated (bookkeeping).
Read the current files and the cited masters as needed to judge each item in context. You may read the two R2 reviews and
`reviews/R3_diff_R2_to_R3.diff`; nothing else under `reviews/`, nor `LOG.md`, nor `CHECKPOINT_*.md`. Scratch: `/home/fb31/BVS-wt/W3-READER/.rc_tmp/R3_scratch_sol/`.
Change no other file; do not commit; start no subagents.

## Gates (as in R2; judged on the diff, each PASS or FAIL)
G1 correctness; G2 hypotheses used = stated; G3 faithfulness to masters (no change claims more than its master; each item
does what its tag says and nothing else); D71 interpretive sentences in changed text; G4 statuses verbatim against
`Theory_work/INFRA/registry/claims.tsv`; G5 no hidden finite-n or scope claims; G6 code fidelity of changed code facts.
A change outside the 14 items (other than bookkeeping) is an F finding.

## Output
Write `Theory_work/Wave3/W3-READER/reviews/R3_council_sol.md`: per-item table `| tag | decision (ACCEPT/REJECT) | note |`;
findings tagged C/S/F/E with file:line and exact correction; the gates; a score (0.0–10.0, one decimal) on C, S, F only.
You must give `gates=FAIL` if you hold a C, S or F finding.

## Fidelity line (this seat only)
Give exactly one line `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL` on the final reader statements as frozen in R3.

## Verdict line (mandatory, machine-checked)
End the review with exactly ONE line of its own:
COUNCIL-VERDICT round=R3 manifest=7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263 seat=sol score=<x.y> gates=PASS|FAIL
Write no other line containing that verdict keyword. If you did not review exactly this manifest, write `gates=FAIL`.
