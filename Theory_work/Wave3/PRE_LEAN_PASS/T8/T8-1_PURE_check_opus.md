PURE check (v2, E2 wording, TWO live copies: STATEMENT.md:81 and the carrier; this is the CURRENT T8-1 check: the patch body is byte-identical to the one checked here, verified by diff after the manager withdrew the third copy) of `T8/T8-1_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/pc/`). Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. `git apply --check T8-1_correction.patch` passed. I applied it with `git apply --directory=.rc_tmp/pc/new` to scratch copies, and `diff` shows only `81c81` (STATEMENT.md) and `25c25` (A_IDEALW_PLUS.md). Line counts stay 262 and 29.
2. The character-level diff (`git diff --no-index --word-diff-regex=.`) touches only the quoted phrases. A Python check confirms `old.replace(OLD, NEW) == patched` byte for byte in both files, and each OLD phrase occurs exactly once (count=1).
3. The E2 phrase, backticks included, appears verbatim once in each patched line. It equals the quoted "planned fix" cell of ERRATA.md:6 (substring check True).
4. STATEMENT.md:80-83 now reads "…the lift of **exactly two upper-bound predicates**; the two bounds are treated as satisfied (the rejection predicates … never fire): (i) … (ii) …". It is grammatical.
5. That sentence is consistent with its parentheticals. "It would fire once n + p + 1 > 2^{10⁶}" is a counterfactual, and "with `int` read as unbounded" matches "never fire". It is also consistent with the proof Q5_dlv0.md:92-97 ((E5): "`le > 1e6` can fire, and it is lifted by IDEAL-W⁺ … second predicate is lifted by IDEAL-W⁺ (or false on 𝔇)") and Q5_dlv0.md:135.
6. In the carrier line, the 𝔇 definition, "Both predicates are false there", and the pointer `STATEMENT.md:80-85` are unchanged. The new tail "…never fire), the reading of TR1 §2." agrees with "Both predicates are false there".
7. Registry: the OLD sentence occurs exactly once in assumptions.tsv:116 (count=1 on that line and in the whole file). The row's OLD and NEW strings match CORRECTIONS.md:9 exactly, and that NEW equals the sentence in the patched carrier line (count=1). The registry was only read, not edited.
8. I ran `grep -rIn --exclude-dir=.git --exclude-dir=.rc_tmp 'treated as true'`. Not covered by the patch, and in the expected groups:
   - Recorder: assumptions.tsv:116.
   - History/research copies named in the row: S4_frozen/inputs/A_IDEALW_PLUS.md:25, Dept/research/FUNI_NARROW/A_IDEALW_PLUS.md:25, FUNI_NARROW/DIFF_sol.md:10, FUNI_NARROW/L5_delivery_F-UNI_v2.patch:41, FUNI_transfer/TR1_sol.md:76.
   - W3-RM2-R erratum and reviews: ERRATA.md:6, reviews/R1_council_opus.md:44, reviews/R2_diff.txt:176, reviews/R2_frozen_copies/ERRATA.md:6.
9. One occurrence is in none of those groups: `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:48`. It is a live claim file whose sentence "its 'treated as true' … is read as 'are false' (TR1 §2)" becomes stale once the patch lands. The CORRECTIONS row already names it as "for the manager to rule on". It does not affect the patch's purity, but the manager still has to rule on it.
10. The remaining matches are the T8-1 pass's own files: CORRECTIONS.md:9, the patch's header and `-` lines, and T8-1_PURE_check_opus_v1_superseded.md:9.
11. I did not change any tracked file. Scratch copies are in `.rc_tmp/pc/new/`, which is git-ignored.
