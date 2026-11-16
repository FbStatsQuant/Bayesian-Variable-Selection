# STYLE_A2_R1: advisor note on the outline "Are the assumptions reasonable?" (2026-11-16)

Read: `assumptions/OUTLINE.md` against `TRACK_B.md`, `AUDIT.md` §6 and §9, `BRIEF.md`, `CHECKPOINT_3.md`. Findings only.

## (a) Structure and order

The outline answers first, which is right. Five changes make it answer faster.

1. **One ordering, not three.** The opening is by theorem, the table by kind of assumption, §3 by dossier number. Use
   the theorem families everywhere: *all theorems* (B1–B3); *posterior theorems* (B4–B7); *reported model, in
   addition* (B8–B10); *reported estimates, in addition* (B11).
2. **Say what "inside" means, in §1** (two lines): the design, continued as a sequence in $n$ with its structure and
   $s_0$ fixed, satisfies the assumption; the judgement is on the qualitative condition. Without this the table and
   the sentence "hold on all our designs" can be misread as simulation results.
3. **Give the primitive form once, in the opening.** TRACK_B's B5 corollary (i.i.d. Gaussian rows, smallest eigenvalue
   of the correlation matrix bounded below, fixed nonzero coefficients, $p\le n^A$) is the fastest way for the advisor
   to judge the posterior theorems. TRACK_B says it needs no new proof. The B9 corollary is a candidate, not proved; if
   used, it must say so.
4. **Spend the space where the verdict is not "same".** B1 and B3 need two lines each. B5, B8, B9 and B11 carry the
   argument.
5. **Put §5 before §4.** §5 completes the answer (who is outside, what still holds). §4 answers a different question
   (is everything about the method itself proved?). Title §5 by its content: "What is outside, and what still holds
   there". Drop from §5 what the opening already says.

## (b) The three style questions

1. **One table, portrait, not two and not landscape.** The message is the contrast between the upper block (all
   inside) and the lower block (a pattern); two tables hide it. See (c) for how it fits.
2. **Run-in labels, no mini-tables.** Eleven mini-tables would fragment the pages and repeat the summary table. Put
   the verdict in the heading line: "**Eigenvalue floor on small sets** (EF), (EF$_\Sigma$). *Comparable to
   Song–Liang's Condition 3.*" Then *Evidence.* and *Rules out.* as run-in italics, as in D2. Give the "Our designs"
   line only where it is not "all inside" (B8–B11), and say once, for B1–B7, that every design is inside.
3. **Labels: yes, but second.** Plain name first, the D2 label in parentheses at the paragraph head and in the table,
   never a label alone in running text, none in the opening. The labels are the advisor's link to the theorems. For
   the same reason write "the reported-model theorem (Theorem 5.7)", not "core 3" or "row 3.6".

## (c) Table design

- **Three design columns, not nine.** In TRACK_B's table the designs fall into three classes with identical rows:
  *independent* (S1, IND); *locally correlated* (S2, S3, S4, S6, AR, BLK); *pervasive factor* (S5, the strong-factor
  study, FAC). The only cell that differs inside a class is visibility for the one-factor designs of the strong-factor
  study ("in"), which takes a footnote. The legend names the members of each class.
- **Columns** (portrait, `\small`): assumption with label (14%) · in words, at most 8 words (24%) · verdict, one word
  (12%) · place in Song–Liang, equation and page (22%) · three design columns (8% each).
- **Verdict as one word** from a fixed set: same, comparable, stronger, none. Qualifiers ("stronger above, weaker
  below" for the dimension) go to the paragraph.
- **Symbols, not words, in the design cells:** ● inside, ○ outside, ? unclear, – not applicable; explained in the
  caption, which also carries the definition of "inside".
- **Rows grouped by theorem family** with a rule and a bold group line, so no per-row list of theorems is needed.
  Eleven rows; the witness designs stay a footnote.

## (d) Where the outline overstates or misstates TRACK_B (flags, not fixed)

1. **§0.2, "can fail for pervasive factors with mixed-sign effects and for riboflavin-like data."** TRACK_B puts
   *every* pervasive-factor design with $p\gg\sqrt n$ outside the reported-model theorem, through the leakage set,
   aligned signs included, and names ours: S5, all of the strong-factor study, FAC. Mixed signs and the
   riboflavin-like design concern visibility only.
2. **§0.3 and §5, "elsewhere the reported-model theorem … still hold."** Only on S2–S4, S6, AR, BLK. On the factor
   designs only the unbiasedness and the posterior theorems hold. The outline also drops what has no theorem there:
   that the reported inclusion probabilities, median model and evidence estimate are close to the exact ones.
3. **§0.1, "each mildly."** Not TRACK_B's words. It calls only the collinearity floor "very weak in absolute terms".
   For the row law it says bounded or genotype data are outside Theorems 3.9, 5.7 and 5.19 as stated; for the
   dimension, that Song–Liang's exponential range is given up.
4. **§0.2, "two … conditions, with Song–Liang counterparts."** TRACK_B: visibility is *stronger than* their Condition
   5; their remark (a) is "an informal remark, not a condition", with no formal counterpart to compare levels; and
   there is a third added condition (B10) with no counterpart.
5. **§0.2, "hold for independent, block and AR designs (AR up to correlation 0.8)."** TRACK_B's verdict is on *our*
   designs, and its general form needs at most one true predictor per block. "Up to 0.8" comes from track C, which the
   brief marks "internal only; not for the paper", which is partly pending, and which reads "unclear but improving"
   for local regressions at AR(0.8). The same holds for "riboflavin-like". Decide whether track C is cited at all;
   if so, with its status and its caution, not only its favourable lines.
6. **§4, "No open item for the posterior theorems."** The outline's own "five further claims" include two unchecked
   lemmas behind the expectation bound of Theorem 3.1 (AUDIT X2, X3) and one registry correction for Corollary 4.7
   (X4).
7. **§4, "13 code-level items … being checked."** One of the 13 needs a new key lemma and is an open premise of a
   remark, not a check (T11); two block no core theorem (T12, T13); several are mathematical, not code-level (T6–T9).
   AUDIT lists them as a queue, not as work in progress.
8. **§3, unchecked lines.** TRACK_B excludes lines marked "[audit calc]" *and* "[audit reading]" (the last sentence of
   B5); the outline names only the first.
9. **Omissions that change the reading.**
   - The Song–Liang supplement was not inspected, and the beta-min comparison (B4) stops at that point.
   - The brief asks whether a typical user is inside; TRACK_B answers in B6, B7 and B8, and the layout has no slot
     for it.
   - CHECKPOINT_3 item 6 recommends one sentence for the report: nothing recorded says the start mass is poor at the
     sizes of the $10^6$ plan.
10. **Row map.** The eigenvalue-floor row lists 3.3(a) but not the margin 3.3(b) or the floor of Assumption 4.5(a),
    both of which B5 covers.
11. **Inside TRACK_B itself** (for Theory): one-factor designs are "inside" on visibility in the strong-factor study,
    but FAC, also a one-factor design, is "unclear". The table cell needs their explanation.
