PURE check of `T8/T8-1_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/t81/`). Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. `git apply --check T8-1_correction.patch` printed CHECK_OK. The patch has one hunk (`@@ -78,7 +78,7`) that replaces one line.
2. I applied it to a copy of STATEMENT.md under `.rc_tmp/t81/` and diffed. `wc -l` gives 262 before and after. `diff` shows only `81c81`. A character-level word diff (`--word-diff-regex=.`) shows only `[-t-]{+false (never fi+}r[-u-]e{+)+}`, which turns "true" into "false (never fire)". The trailing colon and every other character are unchanged.
3. The sentence now reads consistently. The parenthetical on line 81–82 says (i) "would fire once n + p + 1 > 2^{10⁶}", i.e. it describes when the predicate would fire without the lift. Line 83's "with `int` read as unbounded" makes `cap_ll > INT_MAX` impossible to fire. Both fit "never fire".
4. The proof in `lemmas/Q5_dlv0.md` agrees. Line 94 says the rejection predicate `le > 1e6` "can fire, and it is lifted by IDEAL-W⁺ (or false on 𝔇…≤ 10⁶)". Lines 96–97 say the `cap_ll > INT_MAX` predicate "is lifted by IDEAL-W⁺ (or false on 𝔇)". Line 40 has "Without the two lifted predicates". Line 135 says (E5) is the only place IDEAL-W⁺ is used and it isn't needed on 𝔇. In every case the predicates don't fire, so the patched statement matches the proof.
5. I grepped `W3-RM2-R/` (excluding `reviews/`) for `treated as true|treated as false|IDEAL-W⁺`. "treated as true" appears only at STATEMENT.md:81, the patched line, and in ERRATA.md:6 (E2), which records the problem. Nothing contradicts the patched line:
   - H5_SUMMARY.md:24–25 and REPORT.md:8 say "upper bounds … treated as lifted".
   - CHECKPOINT_1.md:34 says "lifts `le > 1e6` … `cap_ll > INT_MAX`".
   - STATEMENT.md:72, 89 and 147, and Q4_core_plus.md:106, refer to IDEAL-W⁺ only by name.
6. One minor point, not a purity issue: E2's suggested text was "the two bounds are treated as satisfied (the rejection predicates … never fire)". The patch uses shorter wording that means the same thing.
7. Nothing else changed. There is no other edit to a claim, constant, status or version line, or hypothesis. All other lines are identical, and no tracked file was modified; the only files I wrote are under `.rc_tmp/t81/`.
