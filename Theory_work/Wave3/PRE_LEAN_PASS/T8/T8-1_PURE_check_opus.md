PURE check (v4: fresh re-run on the CURRENT two-copy patch, at the manager's request after the L5_delivery reversal) of `T8/T8-1_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/t81pure_*`, removed). The previous two-copy run is kept as `T8-1_PURE_check_opus_v2_two_copies_prior_run.md`; the withdrawn three-copy run as `..._v3_three_copies_withdrawn.md`. Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. The patch has 2 `diff --git` sections, for the carrier and STATEMENT.md. No hunk touches L5_delivery.md: its only appearance is the header line 5 (the REVERSAL note). `git apply --check` passes, and `git apply --numstat` lists two files, each with 1 change. With `patch -p1` on scratch copies, only STATEMENT.md:81 and A_IDEALW_PLUS.md:25 change, and line counts stay 262→262 and 29→29.
2. The character-level diff shows only the quoted phrases change. On :81, ", which are treated as true:" becomes "; <E2>:", and "**exactly two upper-bound predicates**" is kept. On :25, `the predicates are "treated as true", which TR1 §2 reads as "are false".` becomes `the two bounds are treated as satisfied (…never fire), the reading of TR1 §2.`
3. The E2 text, backticks included, appears verbatim once in each patched line and exactly matches the quoted planned-fix cell of ERRATA.md:6.
4. The patched STATEMENT.md:80-83 is grammatical. The semicolon clause, then the colon, introduces (i)/(ii), which name the same two predicates, so the parenthetical is redundant but consistent. It matches Q5_dlv0.md (E5) :92-97, where each predicate is "lifted by IDEAL-W⁺ (or false on 𝔇)", and :135, where IDEAL-W⁺ is used only in (E5). The carrier sentence agrees with the earlier part of :25, "Both predicates are false there".
5. The OLD registry sentence in the CORRECTIONS.md T8-1 row occurs exactly once in assumptions.tsv, on line 116. The NEW sentence matches the patched carrier line exactly, and occurs once in CORRECTIONS.md.
6. L5_delivery.md is untouched: no diff against HEAD, and its last commit is a14ce83b. Line 48 still reads `its "treated as true" for the lifted predicates is read as "are false" (TR1 §2)`.
7. STATEMENT.md:81 lies in the premises column of every W3-RM2-R claim:
   - `:52-115`: RM2-F-plus, RM2-R-plus, SAND-F-c, TL-F-c, Ex-Proxy-d, Cont-plus.
   - `:52-93`: RM0-plus.
   - `:71-93`: DLV-0.
   - Line 81 is in no claim's `lines` span, since those all start at 118 or later, and no other claim cites a W3-RM2-R/STATEMENT.md span.
   - The carrier file is in no registry span; the only A_IDEALW_PLUS hit is assumptions.tsv's source field, which points to the FUNI_NARROW copy.
8. No tracked file was modified, and the scratch directory `.rc_tmp/t81pure_*` has been removed.
