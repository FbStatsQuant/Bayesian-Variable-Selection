# Disposition of D2_codex_fidelity.md (Sol, FIDELITY: NOT-FAITHFUL; 2 C, 1 S, 4 F, 1 E). Manager, 2026-11-16.

All 8 findings were confirmed against the cited sources and fixed. Each fix restores the source's wording or meaning; none adds content.

| id | sev | fix |
|---|---|---|
| D2-01 | C | $\bar h_n$ is now defined as in the masters: $\bar h_n^2$ = the mean of the squared one-observation Hellinger distances (a root mean square). Remark 4.9 and Remark 3.20(ii) were reworded (`W3-POST2/STATEMENT.md:104`; `W3-MISR-R/STATEMENT.md:32`). |
| D2-02 | C | §2.6 local search: after the last allowed move the search scans once more. If no neighbour improves it certifies the end point; otherwise it stops at the best improving neighbour, uncertified (`v3_engine.h:385-414`). The same error in D1 §5.6 is fixed. |
| D2-03 | S | The Remark 3.20 status note now says that the reader-form composition (bridge B4.4, NEW) awaits its final check. |
| D2-04 | F | §1: the random-design sentence now states the $O_P$ form, not "the same". |
| D2-05 | F | Thm 5.19 in-words, §1 and Table 1 now speak of errors multiplied by the success indicator and of intersections, with no conditional claim. |
| D2-06 | F | Occam-factor sentence: the determinant ratio *alone* gives about $(n+1)^{-1/2}$ per extra predictor; the fit term can outweigh it. Same fix in D1 §3. |
| D2-07 | F | Example 3.19: the added "no candidate model contains the true regression function" is removed. The reader version's claim is restored: "the full model, with all predictors, is misspecified for the candidate-only fit". |
| D2-08 | E | Ledger: `[L1a′]` does have a registry row, `W3-POST:Lemma-1a'@1.0.0` "PROVED (by this seat, unchecked)" (claims.tsv:343). Corrected. |

**Second Codex read:** none launched. HQ's rule allows one for correctness findings only after HQ is told. The two C findings were local wording errors with mechanical, source-copied fixes. The manager recommends a short Opus spot-check of the 8 fixes instead; HQ to decide.
