# STYLE_A5_R2: final advisor note on Assignment 5, the additions only (2026-11-17)

Read: Result 1, Result 3 with Corollary 13 and Remark 14, the law-of-rows paragraph, and the places they touch (§1 item
3, §5.3.3, §5.4, §6, Remark A.9). The log is clean.

## (a) Do the additions read cleanly in place?
1. **Result 1, (SGR).** The assumption contains a definition ("$\mathrm{PIP}_j:=0$ for a removed column"), while the
   theorem assumes "(DIM) with $p=p_{\mathrm{raw}}$", under which no column is removed. A reader stops here. Move
   the definition out, and say in words what "$p=p_{\mathrm{raw}}$" asks.
2. **Remark 4 (smaller sets).** Its first sentence has 60 words and names its hypotheses ("energy and beta-min measured
   against the noise variance") without stating them. The last sentence compares three floors at once. Suggest:
   "Against (EF$_\Sigma$) as stated, it asks the floor on smaller sets. The result behind Theorem 3 can let the floor
   on its larger sets vanish slowly; this one cannot."
3. **Corollary 13.** It reads well. Three points:
   - The status says the output fields are still to be added. Say in the lead paragraph that these quantities are
     functions of the returned list, not outputs of the method as described in §3.5.
   - "these errors are $O_P$ on output, and, under (C2$^+$), without 'on output'" → "for runs that produce output;
     under (C2$^+$) every run does".
   - $\varepsilon_n$ is the posterior miss here, the noise is $\varepsilon$, and in §5.3 $\epsilon_n$ is Song and
     Liang's rate.
4. **After Corollary 13,** "is proposed by Theory and not yet claimed" is internal voice. "We do not claim it here."
5. **Remark 14.** Two long sentences. "Within each block", "tile types" and "countably many local correlation patterns"
   are undefined, and "autoregressive correlation" is unqualified, against HQ's wording rule.
6. **The Scope line of Result 3** now sits after Remark 14, a page from Theorem 11. Put it before the corollary.
7. **Law of the rows (§5.3.2).** Clean in structure. Two phrases: "As a factual remark" (drop it), and "In ordinary
   data, (SGR) holds for Gaussian rows", since Gaussian rows are not ordinary data; write "Examples:".
8. **Leftovers:** §5.3.2 still says "$O(\log n)$ predictors (Gaussian rows)" for the floor of Theorem 3. §4.1 calls
   (GR) "used by several results"; it now serves Result 3 only.

## (b) Sentences that now contradict each other (flags, not fixed)
1. **Visibility.** Three places, three accounts:
   - §1 item 3, §5.4 and Remark 14: it fails for strong factors whose mixed-sign coefficients lie on a null set;
   - §5.3.3, "A typical user": it was "found failing for a pervasive factor with effects of mixed signs", unqualified;
   - riboflavin-like data: "under re-examination" (§5.3.3), "is being determined" (Remark 14).
   And by Remark 14(ii) S5 and FAC are in generic position, yet §5.3.3 and Table 3 call them "unclear". Theory should
   say whether their coefficient vectors lie off the null set.
2. **The list premise (Remark A.9).** Its closing sentence says "nothing in this paper proves it" and, in the same
   sentence, that Corollary 13 shows it on the designs of Theorem 11. Split: "In general nothing here proves it. On
   the designs of Theorem 11, Corollary 13 gives it; we do not yet claim its use here."
3. **§6, "the guarantee for the list a run returns [is a remark] in the supplement".** There are now two list
   results, and Corollary 13 is in the main text. Name the remark (the distribution guarantee for the list).
4. **§1 item 3** is not a sentence: "The conditions, that …, the second fails …". Split after "consistent": "It needs
   two conditions: … The second fails for … Visibility fails for …".
5. **Scope of Result 3:** consistent everywhere I looked (heading, Scope line, §5.4, Corollary 13's title).

## (c) The three cheapest trims toward 25 pages (no content lost; about 0.8 page)
1. **Remark 4 and its status (about 14 lines) to the supplement,** next to the omitted-variables theorem, which it
   is a case of. Keep one sentence under Theorem 3.
2. **Merge Remark 14 into the visibility paragraph of §5.3.3 (about 10 lines).** That paragraph's "Evidence" already
   gives the aligned-sign and block cases; Remark 14 is the fuller version of the same argument. State it once.
3. **The "Assumptions." lists (about 15 lines).** Every assumption statement carries its "[§5.3.x]" tag, so each list
   repeats the theorem's "Assume …" sentence.
