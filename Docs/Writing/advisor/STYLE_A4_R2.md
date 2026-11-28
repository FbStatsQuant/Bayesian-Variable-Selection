# STYLE_A4_R2: advisor note on the unified manuscript, full draft (2026-11-17)

Read: all section files, the log and the PDF, against D1 v1, D2 v2.1 and A2 v2.1. No dangling reference; the renames
(ξ, L_bi, T_s, h_b, Δ) are applied throughout, with one exception (c5). It reads as one paper, with the seams below.

## (a) Seams still showing
1. **Both summary tables are at the end of the PDF** (Table 2 on p. 42, Table 3 on p. 43). The log says Table 3 is
   "too large for page by 27pt"; it blocks Table 2 behind it. §4 and §5.1 both open by pointing to a table the reader
   cannot find, and the 22-page count leaves them out (see (e)). Shorten Table 3 until it fits, then pin both.
2. **Result order is 1, 5, 2, 3, 4.** Either renumber in order of appearance, or say in §4's first paragraph that
   Result 5 concerns the rate of Result 1 and is stated right after it.
3. **Section and theorem numbers collide:** Theorem 4.5 is in Section 4.4, Assumption 4.7 and Theorem 4.8 in Section
   4.5. With five results, global counters (Theorem 1, 2, …) would be clearer.
4. **§5 still uses A2's theorem names** ("our selection theorems", "the distribution theorem", "the Gaussian-row
   theorems") after the key that defined them was dropped. Use "Result 1", "Result 2", or define the names once.
5. **Vocabulary:** "prints" survives twice in §4 (Result 3 "why", Result 4 "In words"). "R" appears in (C2$^+$) and
   after Theorem 4.8, but §3 never says what the software is written in. The status is "resource limit" in §3.4 and
   `resource_limit` in §3.5.
6. **Duplicated facts:**
   - "no claim about how likely that event is": Table 2, Result 4 "In words", its "why", Remark 4.12(i), §6;
   - (V), (NL) and the leakage set are restated inside the "Evidence" lines of §5.3.3–5.3.4;
   - §5.4 repeats two sentences of §5.3.3 almost word for word (the factor argument; the numerical check).
7. **Notation left over:**
   - particle index $s$ ("$S_s$", "$\omega^{(t)}_s$") beside $s$ and $s_0$;
   - $M$ is our level and, in §5.3 (law of the rows), Song and Liang's constant ("$M=\log2$");
   - a correlation is $\varrho$ in §4.5 and $\rho$ in §5.3.

## (b) Sentences a referee would read twice
| Where | Problem | Proposed wording |
|---|---|---|
| Abstract, "at the rate $\sqrt{\log n/n}$, which cannot be improved" | Unqualified; Result 5 proves it on two families of designs. | "a rate attained on two families of designs" |
| §1, item 1, "on every design of our simulation studies" | A statement about our designs inside "what we prove", before the designs are introduced. | Move the clause to the paragraph on assumptions. |
| §1, "a planned set of runs …, which are reported separately" | Planned runs cannot be reported. | "The two studies are reported separately; the runs at $p$ up to $10^6$ are planned." |
| §3.3, Example 3.2, "certifies $\{1,3\}$" | Used before Stage 6 defines it. | "and stops there, with no improving neighbour" |
| §3.4, Stages 4–5, "An island of $N$ particles starts … one independence move" | One nine-line sentence. | Three items: reweight, resample, move; then the four moves. |
| §3.4, Stage 1, "(for the sampler, the memory and the worst-case time of the local search from the start mode)" | Unclear what is estimated. | Two plain sentences, or move to Appendix C. |
| §3.5, "anything else it returns is flagged incomplete, and the results do not cover it" | "It" changes referent. | "Whatever a stopped run returns is flagged incomplete; the results do not cover stopped runs." |
| §3.7, (C2$^+$), "an allocation no smaller than the method's own polynomial requirement formulas" | Not a comparison of like things. | "an allocation of at least the memory and time that the method's own formulas require" |
| §4.6, "Why it matters" | A five-line sentence that repeats "In words". | The v2 one: "The numbers a user reads come with guarantees: the evidence estimate is right on average on every design, and without leakage the reported summaries converge." |
| §5.4, first sentence; "needs no leakage at all" | Four lines, two parentheses; the phrase reads as "does not need leakage". | Split after "(S5, the strong-factor study, FAC)". "… needs the condition (NL), which only the independent designs satisfy." |
| §6, "The explicit constants … are conservative. They cover the posterior …" | "They" reads as the constants. | "The results cover …" |
| §6, "three idealising conventions: exact arithmetic, ideal random numbers, and an allocation …" | The conventions are (C1)–(C3), not these three items. | "under Conventions (C1)–(C3), which idealise the arithmetic, the random numbers and the allocation" |

## (c) What the unification broke
1. **Example 3.2, "a small leakage set (here $\{1,3,5\}$)".** §4.5 says a null predictor whose correlation with a true
   one stays fixed must belong to $Q$. By that sentence predictors 2 (0.93 with 1), 4 (0.69 with 3) and 6 belong to it
   too. Say "the predictor that enters the start mode wrongly (here 5)", and let Theory say what $Q$ is in the example.
2. **Table 3, signal-size row:** "If it vary" (a verb is missing).
3. **§5.1, "in the table"** (verbatim headline) now needs "(Table 3)" in the next paragraph.
4. **§5.3, visibility evidence:** "$W$ a standardised row of the design"; §2 defines $W$ as a centred copy of one
   population row.
5. **Appendix C, pilot step floor:** still "$1/T_i$"; the renamed symbol is $T^{\max}_i$.
6. **Nothing lost from D1** that I can find: duplicates, the evidence lower bound, diagnostics and Algorithm 1 are in
   Appendix C and A.4. §4 matches D2 v2.1, including the single delivery clause under (C2$^+$).

## (d) Do §6 and §5.4 say the scope once?
Nearly. §5.4 is the one home of "which designs, and what still holds", and it is clear. Three fixes:
1. Remove from §5.4 the two sentences that §5.3.3 already has (a6), or the reverse; keep the "what still holds" list.
2. §6 names the design limit of Theorem 4.11 but not that of Result 3. Name neither: one sentence, "Which designs are
   inside each result is in Section 5.4."
3. Say "no lower bound on the probability that the calibration succeeds" in Remark 4.12(i) and §6 only.

## (e) Length, and where 1–2 pages could go
The main text is about 24 pp once Tables 2 and 3 are counted, not 22; still under 25.
1. **The "Assumptions." lists (about 0.4 p).** Each assumption statement now carries its own "[§5.3.x]" tag, so the
   seven lists repeat the theorem's "Assume …" sentence. One line each, or none.
2. **§5.3 heads against Table 3 (about 0.6 p).** The conditional sentences appear in both. Keep them in the heads;
   give the table the counterpart's reference and the design symbols. This also makes Table 3 fit on its page.
3. **§5.3 "Evidence" lines that restate §4's definitions (about 0.3 p).**
4. **Result 4's "In words" and "why", and Result 5(c)'s derivation (about 0.25 p).**
5. **§3.4, Stages 1–3 (about 0.2 p):** the memory and time estimate, the neighbour graph and the recursion to
   Appendix C.
6. **A larger option, for HQ:** move the fixed-design Theorem 4.2 and its four assumptions to the supplement (about
   0.8 p). It is part of Result 1, so this needs HQ's agreement; §5.3 and Result 5 would then point to the supplement.
