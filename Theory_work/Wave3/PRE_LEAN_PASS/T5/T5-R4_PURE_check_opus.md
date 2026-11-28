PURE check of `T5/T5-R4_correction.patch` (statement copy; the reader copy is the staged `T5/T5-R4-reader_correction.patch`, applied together in this check; fresh Opus subagent, claudeAgent_personal, high; scratch under `.rc_tmp/`, removed). Verbatim report (harness indent removed):

PURE-VERDICT: PURE
1. `git apply --check` passes for both T5-R4 and T5-R4-reader. On scratch copies made with `patch`, STATEMENT.md stays at 499 lines and only line 152 changes (1 line out, 1 line in). The character diff runs from just after "are counted in them" to the end of that line and touches nothing else.
2. The new text matches the card's R4 column (c) character for character, and the old clause is exactly the one the card names.
3. Notation: in the reader statement block, line 142 says "Let r be the number of predictors that remain (r ≤ p)", so p is the raw count and r the retained count, and "r < p" is correct here. Lines 28-30 use different notation (p := p_ret), but they sit in the master preamble, outside this block.
4. The displays (i)/(ii) at :189-191 have the form P*[Π(·) > n^{−cM}] ≤ n^{−cM}. Reading Π as 1 on undefined data puts that data inside the event (1 > n^{−cM}), so it is counted in the exceptional probability. This is consistent with "counted in them" and with "the same set" at :198.
5. B1.md:11-15 defines 𝓔₁ and shows no column is constant on it, so p_ret = p. ASSEMBLY.md:78/111/122 put P(𝓔₁ᶜ) in the common remainder. So {r < p} ⊆ 𝓔₁ᶜ is in the common exceptional set, as claimed.
6. "Fewer than two remain" (with p ≥ 2 by (A2)) implies r < p, so it is covered. A constant response has probability 0 under (A1) with σ*² > 0. The sentence is true.
7. Reader copy (READER_VERSIONS.md:1066-1067, 1458 lines unchanged): its text is the same convention sentence, word for word, with "$p<p_{\mathrm{raw}}$" in place of "r < p". This fits the reader's notation at :1060, where p ≤ p_raw is the non-constant count. Both copies are consistent with the text around them.
8. Span to rehash: line 152 is in the shared premises span `STATEMENT.md:136-183`. It is not in the Thm-A claim span `:185-207`, which is unchanged.
9. Eight claims.tsv rows cite that premises span and need rehashing: Thm-A, Thm-B, Cor-C, B0, B1, B2core, B2 and B3.
10. Nits that don't affect purity: the patch header says ":151-152" but only line 152 changes, and the new line 152 is longer than the file's usual wrap width. The new reader text splits over 2 lines (1066-1067), where the old one took 2 lines (1066-1067), so the reader's line count is unchanged.
11. Scratch directory `.rc_tmp/pure_t5r4_*` was removed. No tracked file was modified and nothing was committed.
