PURE check of `T9/T9-F1_correction.patch` (the exact text of the HQ-approved prep note `Dept/pre_lean_cards/T9_prep.md`, row F1; fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/t9f1_pure_*`). **Verdict NOT-PURE, and the only defect is the line pin `W3-SAMP/STATEMENT.md:107-110` (MR-b is on line 111).** The coordinator did NOT change the manager's text; an ALT with the pin `:107-111` is proposed (`T9/T9-F1_ALT_correction.patch`; the checker states that with that change and nothing else the patch is PURE). Verbatim report (harness indent removed):

PURE-VERDICT: NOT-PURE (the line pin is the only defect)

1. Mechanics are clean. `git apply --check` passes from the repo root. Applying the patch with `patch -p1` to a scratch copy (`.rc_tmp/t9f1_pure_2798190/`) gives exactly one change: a single 245-character insertion on line 26, with no deletions. Both files have 46 lines.
2. The inserted text, minus the trailing space before "On", matches the F1 row of the prep note (line 9 of `T9_prep.md`) character for character. It sits right after "…(its "in particular" clause, :104). " and right before "On $\mathcal A$, $R'=4$, so this holds…".
3. (2a) is true. W1-N1/STATEMENT.md:15-16 sets CODE to the frozen v2.2.1 core. CC_code_check.md:9-10 says "W1-N1 used the frozen v2.2.1 core".
4. (2b) is true. In MR-b (STATEMENT.md:111), h ≡ 1 is allowed: a constant is jointly measurable, has the fixed bound B_h = 1 and does not depend on the final streams. Then (1/N_e)Σ_i h = 1, so E[W_r | 𝓒] = π(1) = 1.
5. W_r is the same quantity in both files: W3-SAMP/STATEMENT.md:52 defines W_r := Ẑ_r/Z with Ẑ_r = exp(log_Z_r[r]), which is PoolZ's W_r := Ẑ_r/Z.
6. (2c) The pin is off by one. Line 107 holds the Lemma MR header with the start of the definition of h, lines 108-109 finish that definition, (MR-a) is on 110, (MR-b) on 111 and (MR-c) on 112. Your measurement is right, and the pin 107-110 does not cover MR-b.
7. Corrected pin: `W3-SAMP/STATEMENT.md:107-111`. `:111` alone would also work, but that drops the definition of h.
8. (2d) The pin is correct. Lines 9-21 are exactly the "Relation to the N1 code of record" paragraph (line 8 is blank and line 23 starts CC1). It ends with N1's code bridge (`L1_bridge.md`) applying "to main's island verbatim, **except** for its sentence identifying `pip_plain`".
9. The inserted text leaves out that `pip_plain` exception. That does not matter here, because PoolZ is about Ẑ only (Remark ii).
10. (3) The registry row in claims.tsv (line 526, W3-READER:PoolZ) gives the span as STATEMENT.md:12-39. Line 26 is inside it, so the recorder must rehash.
11. The Setting and Claim (lines 14-24) are unchanged, as is the conclusion (∎ at line 33). The patch only adds citations (MR-b, CC) and introduces no new hypothesis. The added depends_on entries `W3-SAMP:MR@stmt:MR-b` and `W3-SAMP:CC` match it.
12. (4) The rest of the proof still reads correctly: after the parenthetical, "On $\mathcal A$, $R'=4$, so this holds for r=1,…,4" still refers to the identity E[W_r|𝒞]=1.
13. If the manager changes the patch and prep text to `:107-111`, with nothing else changed, the patch is PURE.
