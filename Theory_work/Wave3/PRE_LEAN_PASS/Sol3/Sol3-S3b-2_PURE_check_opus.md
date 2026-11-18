PURE check of `Sol3/Sol3-S3b-2_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/s3b2/`). Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. `git apply --check` passes, and the patch touches only `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` (1 insertion, 1 deletion). I applied it to a scratch copy in `.rc_tmp/s3b2/`. Only line 301 changes and the file stays at 1458 lines. At character level the edit removes "2, " and inserts ", as did the previous Gaussian proof of Theorem 2 (the presented Theorem 2 uses B2.2′ instead)". Nothing else changes.
2. The old and new strings match `FABLE_CARD.md` row S3b-2 column (c) exactly: the old string is in the original line, the new string is in the patched line, and `orig.replace(old,new) == patched` returns True.
3. The new text agrees with the next row (line 302, B2.3/B2.2′). That row says B3w "replaces B2.2 for the presented statement; B2.2 stays for the Gaussian case".
4. It also agrees with `W3-D3/STATEMENT.md` and `lemmas/B3w.md`. STATEMENT.md:94-97 says Thm2SG coexists with `W2-APP:POST` and covers Gaussian rows as L=1. B3w.md builds the events from `W3-DIST:B1`, `B2core` and `B2` part (a), with Theorem 1 item 6 applied in ASSEMBLY. It does not cite `W2-APP:POST` part (a).
5. Nothing else in lines 258-320 now contradicts the patched row. Lines 292-294 still cite `W2-APP:POST@1.0.7` as an input to Theorem 2, but only at `L1_POST.md:27-33`, the diagonal step used through Theorem 1 item 6. That is not the Gaussian-row events of part (a), which matches the card's note. Line 313 (v0.3 changelog) mentions B2.2 only as history. Lines 308 and 319 say Theorem 2 is presented with sub-Gaussian rows, which fits the new wording.
6. No claim or statement span in the registry's statement files is touched. The change is reader bridge-table prose only. Nothing tracked was modified; the scratch copies are in `.rc_tmp/s3b2/`.
