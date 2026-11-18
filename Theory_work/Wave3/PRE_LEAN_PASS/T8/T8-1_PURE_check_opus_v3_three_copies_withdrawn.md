PURE check (v3: E2 wording, three live copies) of `T8/T8-1_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/t81/`). Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. `git apply --check` passes. I applied the patch with `patch -p1` to scratch copies in .rc_tmp/t81. Inside a repo subdirectory, `git apply` skipped the paths without saying so. Each file changes on exactly one line: STATEMENT.md 81, A_IDEALW_PLUS.md 25, L5_delivery.md 48. Line counts stay at 262, 29 and 49. A word-level diff shows only the quoted phrases change; every other character is identical.
2. The E2 text appears verbatim, backticks included, once in each patched line (`grep -F` = 1 per file). It is byte-identical to the planned-fix cell of ERRATA.md:6 (`cmp` OK).
3. STATEMENT.md:80-83 reads correctly: "…lift of **exactly two upper-bound predicates**; the two bounds are treated as satisfied (… never fire): (i) `le > 1e6` …; (ii) `cap_ll > numeric_limits<int>::max()` …". It agrees with Q5_dlv0 (E5) at :94 and :97 ("lifted by IDEAL-W⁺ (or false on 𝔇)") and with :135. The parenthetical's `INT_MAX` versus (ii)'s `numeric_limits<int>::max()` is fixed by the E2 wording, and the carrier's wording note defines INT_MAX as that value.
4. The carrier sentence ("that file says … never fire), the reading of TR1 §2.") is grammatical and matches the sentence before it ("Both predicates are false there").
5. In L5_delivery.md:48, "it" refers to W3-RM2-R Lemma DLV-0 / STATEMENT.md. "The lifted predicates never fire" restates the paragraph's own ":46 under A:IDEAL-W⁺ both predicates are false" and claims nothing new.
6. Spans: claims.tsv:271 is the only row naming the file. It is W2-UNI:F-UNI, statement span L5_delivery.md 15-21, premises :8-13. Line 48 is outside both. W2-UNI's CHECKPOINT.md and REPORT.md do not pin :48, and its CITECHECK.txt / CITECHECK_AUDIT.md cite only lines :4, :5, :12, :29, :30, :33, :39.
7. Report only: L5_delivery.md is hashed as an EXT file in W3-RM2-R's manifests. MANIFEST_R3r.txt:76 and MANIFEST_R3r2.txt:76 give 51cf7255…, which matches the current file. The patched file hashes to 3713fef8…. Those EXT entries (and the R3r_record_opus.md:3 note, which names :48) will need a recorder re-point when the patch lands.
8. Registry: the OLD sentence occurs exactly once in assumptions.tsv:116 and nowhere else in that file. The NEW sentence in the CORRECTIONS.md T8-1 row matches the patched carrier line exactly (grep = 1).
9. Residual 'treated as true' outside the patched lines falls only in the allowed groups:
   - the registry row, assumptions.tsv:116;
   - Dept/research files: FUNI_NARROW/A_IDEALW_PLUS.md:25, DIFF_sol.md:10, L5_delivery_F-UNI_v2.patch:41, and FUNI_transfer/TR1_sol.md:76;
   - S4_frozen/inputs/A_IDEALW_PLUS.md:25;
   - W3-RM2-R ERRATA.md:6 and its reviews (R1_council_opus.md:44, R2_diff.txt:176, R2_frozen_copies/ERRATA.md:6);
   - this pass's own files (CORRECTIONS.md:9, T8-1_PURE_check_opus*.md, the patch).
10. Two CORRECTIONS.md rows are out of date (this does not affect the patch's purity):
    - The T8-1 row (:9) still says "two live copies patched" and lists L5_delivery.md:48 under "NOT touched, for the manager to rule on".
    - The PATCH-STACK row (:30) lists 16 files and omits L5_delivery (49 lines).

    Both should be updated to match the three-file patch. (Done by the coordinator after this check: see CORRECTIONS.md.)
