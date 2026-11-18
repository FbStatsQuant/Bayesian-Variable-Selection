PURE check of `Sol3/Sol3-S3b-1_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/s3b1/`). Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. `git apply --check` passes. On scratch copies, READER_VERSIONS.md stays at 1459 lines and REPORT.md at 93 (split on "\n"; `wc -l` gives 1458 and 92). The only changed lines are :295 and :42.
2. Character diff for READER_VERSIONS:295: `/B3@1.0.2` becomes `@1.0.2` (and `W3-DIST:B3@1.0.2` as the proof template of B3w only; its last sentence, conditional on `W3-POST:Thm-1`, is not used). Nothing else on the line changes.
3. Character diff for REPORT:42: `/B3` is deleted, and "`; `W3-DIST:B3` is the proof template of B3w only`" is inserted after "all PROVED-CHECKED". The final "." and the rest of the line are unchanged.
4. The READER_VERSIONS text is the same, character for character, as FABLE_CARD.md row S3b-1 column (c).
5. The REPORT.md wording carries out the card's instruction: B3 leaves the "all PROVED-CHECKED" group, and the card's exact phrase is added.
6. W3-D3/STATEMENT.md:154-157 calls B3 "the template of Lemma B3w" and says "(Its last sentence, δ_n → 0, is not used; …)". This matches the patch.
7. The registry row W3-DIST:B3 (claims.tsv) is v1.0.2 with status "PROVED-CHECKED, conditional on W3-POST:Thm-1 (for its last sentence); council R2, …". This supports taking B3 out of the unqualified "all PROVED-CHECKED" group.
8. REPORT.md:42 is in free text. The only ``` fences in REPORT.md are at lines 67 and 92, so the REGISTRY block is below line 42.
9. `ingest.py convert` exits 0 on both the original and the patched scratch copy. The two outputs match once the embedded scratch path is normalised; the raw bytes differ only because the path is part of the output.
10. No claims.tsv row has READER_VERSIONS.md or W3-D3/REPORT.md as its statement file (0 matches), so the patch touches no registry claim span.
11. Scratch files are only under `.rc_tmp/s3b1/`. No tracked file was modified and nothing was committed.
