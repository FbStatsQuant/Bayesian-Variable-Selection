# Brief — statement-change check NA_DROP (Claude Opus 5.5, effort high, Claude Personal; fresh)

Work read-only in `/home/fb31/BVS-wt/W3-D5P`; **write nothing anywhere**; do not change git state. Read: the prepared
change `Theory_work/Wave3/W3-D5P/reviews/post_cp3/NA_DROP/NA_DROP.patch` (with `CHANGE.md` beside it and the drafts
`STATEMENT_v1.2_draft.md`, `L3_listR_v1.2_draft.md`), the current `Theory_work/Wave3/W3-D5P/STATEMENT.md`,
`lemmas/L2_listCODE.md`, `lemmas/L3_listR.md`, the SPEC carrier `Theory_work/Wave3/W3-D5P/sources/SPEC_LIST_PIP_523dda23.md`
(§4), RM2R `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:144-163` (Lemma S.2 inventory) and the code it cites
(`Scripts/SMC_BVS/core/`). Do not read LOG.md, CHECKPOINT_* or other reviews.

Context: HQ allows dropping the qualifier "when `log_Z_list` is not NA" from LIST-R only if the field is provably never
NA on the delivery event. HQ has confirmed to Engineering two readings of SPEC §4: (1) on the exact branch `pip_list` =
the enumeration PIPs and `log_Z_list`, `list_size`, `list_full` come from `fit$exact$top`; (2) if all scores are −Inf, the
fields are NA with `pip_list_flag = "nonfinite_score"`.

**Task: break the change.** (1) Is new clause (C3)(o) true and proved by L3's new Step 0′ (every SPEC §4 NA row excluded on
every output run under EX-A + IMPL-LIST with reading (1); nonempty lists; finite scores; yᵀy > 0)? (2) Are all removals of
the qualifier in (C3)(i)–(iii), B₃ and L3 Steps 1–3 now justified by (o)? (3) Is the IMPL-LIST edit a faithful statement
of SPEC §4 in HQ's reading (1), and does reading (2) conflict with any LIST-CODE clause (i)–(v)? (4) Tags: is v1.2
STRONGER for the conclusions and EQUAL for the premise edit? (5) Are the derived-text hunks (REPORT, CARD, READER_DELTA)
faithful to v1.2? (6) Any interpretive sentence inside a claim span that is not proved?

**Answer.** Findings (file:line, C/S/F/E, fix); per-question verdicts; last line
`NA-CHECK: <ACCEPT | ACCEPT-WITH-CHANGES | REJECT>`.
