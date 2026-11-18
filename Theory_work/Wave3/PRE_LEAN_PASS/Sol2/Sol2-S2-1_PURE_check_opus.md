PURE check of `Sol2/Sol2-S2-1_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/s21_*`). Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. `git apply --check` passes. On scratch copies in `.rc_tmp/s21_2554507/` (applied with `patch -p1`), exactly one line changes per file: CLAIMS_CARD.md:71 and READER_VERSIONS.md:1443. Line counts are unchanged at 181 and 1458. Running `git status` on `W3-READER/` shows the tracked files are untouched.
2. The character-level diff is the same in both files. "(" is deleted before "on". " the part of" is inserted after "on". " where $\pi(S_0\mid y)\ge n^{-cM/2}$ (there the list holds at least that mass" is inserted before the original ")". Putting the old sentence back into the patched line gives the original line byte for byte, so nothing else on the line moved.
3. The new sentence matches the card's "S2-1 replacement (exact)" New text (FABLE_CARD.md:26) character for character, LaTeX included. It occurs exactly once in each patched line.
4. The sentence is true. Cor 6L (READER_VERSIONS.md:1435) says that on Theorem 6's data events 𝒢_n every run with output has S₀ in its list, so π(𝒯) ≥ π(S₀|y). Cor C's premise is π(𝒯) ≥ n^{−cM/2} (W3-DIST/STATEMENT.md:229-231). So the premise holds wherever π(S₀|y) ≥ n^{−cM/2}, and there the list holds at least that mass.
5. This matches COR9C_NOTE N1, which is not on this branch. I read it from commit 0bf478fb at `W3-D5P/reviews/post_cp3/COR9C_NOTE.md:29-33`: "the premise holds on 𝓜_n ∩ 𝒦_n ∩ {π(S₀ | y) ≥ n^{−cM/2}}". Its lines 45-46 explain why the extra condition cannot be dropped, which supports the fix: the old wording overclaimed.
6. The rest of each row or paragraph is untouched. Each of the following appears the same number of times before and after:
   - READER_VERSIONS.md: "Tag vs Theorem 6: **STRONGER**" (1/1) and "Cor 9C's status is unchanged" (1/1).
   - CLAIMS_CARD.md:71: "Cor 9C's status is unchanged" (1/1) and "Pending recording: not presented as a software statement until IMPL-LIST lands." (1/1).
7. Registry spans: neither target line lies inside any claim's statement or premises span.
   - READER_VERSIONS.md:1443: the only `claims.tsv` spans in this file are W3-READER:R1's premises (95-253, 258-320, 325-439, 444-564, 661-811, 1283-1388) and W3-READER:R3's premises (32-60). The highest ends at 1388.
   - CLAIMS_CARD.md: it appears nowhere in `claims.tsv`.
   - No registry row has either file as its `file`. The W3-READER rows point to STATEMENT.md and `lemmas/R*.md`.
8. One scratch directory is left behind: `.rc_tmp/s21_2554507/`. A safety check blocked my `rm` on it.
