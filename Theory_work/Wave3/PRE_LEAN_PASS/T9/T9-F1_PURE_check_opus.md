PURE check (v2, ALT pin `:107-111`, given its own run at the manager's request) of `T9/T9-F1_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/pure_f1_*`). The v1 check of the prep-note text (pin `:107-110`, NOT-PURE only for that pin) is kept as `T9-F1_PURE_check_opus_v1_pin107-110_NOT-PURE.md`. Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. Mechanics: `git apply --check` passes from the repo root. I applied the patch with `patch -p1` to a scratch copy in `.rc_tmp/pure_f1_2822796/`. Only physical line 26 changes, and the file is still 46 lines (`wc -l`).
2. Character-level diff: there is exactly one opcode, an `insert` at column 116 of line 26. Nothing is deleted or replaced. The inserted text is the parenthetical plus one trailing space. It sits right after "(its "in particular" clause, :104)." and right before "On $\mathcal A$, $R'=4$".
3. Text check: I extracted the F1 quote from `origin/dept/theory:…/T9_prep.md` (row 9) by script. The pin `:107-110` appears once there. After replacing it with `:107-111`, the result equals the inserted text exactly (`MATCH True`).
4. W3-SAMP/STATEMENT.md line by line: 107 is the Lemma MR header and the start of h's definition; 108–109 finish h's definition (bound B_h, evaluated at c = 𝓒, W1-N1's class) and give "Under the N1 premises, given 𝓒 on 𝒜:"; 110 is (MR-a); 111 is (MR-b), all of it on that line; 112 is (MR-c). So `:107-111` covers h's definition and all of (MR-b), and stops before (MR-c).
5. (MR-b) with h ≡ 1 is true. The constant 1 is measurable, bounded with B_h = 1, and does not depend on the final streams, so it is admissible. Then (1/N_e)Σ_i 1 = 1, which gives E[W_r | 𝓒] = π(1) = 1 on 𝒜. That is the same identity N1 gives, under the same N1 premises.
6. N1 uses the frozen v2.2.1 core: `W1-N1/STATEMENT.md:15` sets CODE to `.../core/v2_2_1/core/`. `CC_code_check.md:9` says the same ("W1-N1 used the frozen v2.2.1 core").
7. `CC_code_check.md:9-21` is exactly the "Relation to the N1 code of record" paragraph; line 22 is blank. It concludes at lines 19–20 that N1's code bridge "applies to main's island verbatim", except for the `pip_plain` sentence, which has nothing to do with Ẑ.
8. Registry: `claims.tsv` line 526 is W3-READER:PoolZ, with span `STATEMENT.md` 12-39. Line 12 is the "## Claim PoolZ" heading and line 39 is blank, just before "## Bridge lemmas". Line 26 is inside the span.
9. The Claim text (lines 20–23) does not change, and neither do its conclusion or the "No condition on the design or the data" sentence. The insertion only adds citations to existing results, so it introduces no new hypothesis.
10. The rest of the proof still holds: the R′ = 4 step, linearity, Z > 0 fixed, H-U/SI and the Remarks all rely on the same per-r identity, which now has a second source. Nothing downstream refers to the inserted text.
11. Note for the recorder: PoolZ's current `depends_on` field in `claims.tsv` is `W1-N1/STATEMENT.md:68-90`. Adding `W3-SAMP:MR@stmt:MR-b` and `W3-SAMP:CC` and rehashing the 12-39 span is still to be done, as the patch header says.

No tracked files were modified. The scratch files are in `.rc_tmp/pure_f1_*`.
