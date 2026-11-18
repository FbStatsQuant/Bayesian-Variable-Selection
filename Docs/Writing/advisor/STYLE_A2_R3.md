# STYLE_A2_R3: advisor note on the Assignment 2 draft after TRACK_B v1.4 (2026-11-16)

Read: `assumptions.tex`, its PDF (6 pp.), `TRACK_B_v1.4.md`, `WRITING_DELTA_v1.4.md`. Findings only.
The headline is verbatim. No "our conclusions are stronger"; none of the dropped v1.3 sentences survives. Every
one-word comparison sits on a case the delta marks uniform (model, sparsity, visibility, the three "no counterpart").

## 1. Against v1.4 and the delta (flags, not fixed)

1. **Table, signal size and near-exact collinearity:** "Depends on whether their $\beta^*$ may vary with $n$" and "the
   direction depends on $\bar r_n$" name the regime but give no direction. The rule asks for the conditional sentence.
2. **Eigenvalue floor, head:** it says ours implies "their Condition 3 and their (22)–(23)" in both set-size cases.
   v1.4 pairs them: (22)–(23) against Theorem 3.1 with standardised columns; Condition 3 against Theorem 3.9 with
   Gaussian predictors. The two qualifiers are dropped.
3. **Law of the rows, table:** "otherwise neither implies the other" reads as "on uncentred predictors". v1.4 has two
   cases: raw predictors, and their $|x_i|\le1$ whatever the centring. The paragraph head has it right.
4. **Near-exact collinearity, evidence, "at the price of a slower rate":** an unqualified rate comparison. v1.4 says
   their rate then carries the diverging factor $\bar r_n$ (their (10)).
5. **Conclusions, "their theorems reach larger radii and exponential $p$":** the delta says only that ours does not
   reach them.
6. **Leakage set, quotation:** the draft has "the true predictor $X_t$"; v1.4 quotes "the true predictors $X_t$".
7. **Visibility, evidence:** "at most one true predictor per correlation block" is applied to AR designs too; v1.4
   attaches it to blocks only. And $W$ is a population row, not "the standardised predictors".
8. **Near-exact collinearity, head:** "so that neither implies the other" attaches to both cases; in v1.4 it belongs
   to the case $\bar r_n\prec\log n$ only.
9. **Smaller:** unbiasedness (§2) drops "given the calibration"; the table's "nonzero, not changing with $n$" does not
   fit Theorems 3.1 and 4.2, whose coefficients may vary.

## 2. Can each conditional sentence be read in one pass?

Three heads cannot: signal size, eigenvalue floor, collinearity. They run four or five italic lines with inequalities
in parentheses. Two general fixes: set only the regime marker in italics, and move set-size inequalities to "Evidence".

- **Dimension.** "*Upper range:* ours allows fewer values of $p$: far fewer than their Corollary 1 (p. 954), slightly
  fewer than their Theorem S (supp. p. 13). *Lower range:* ours allows bounded $p$; theirs needs $P_n\succ n^\theta$
  (p. 950)."
- **Signal size.** "They state no lower bound. *If their $\beta^*$ is one fixed sequence* (the natural reading of
  p. 950): Theorems 3.9, 5.7 and 5.19 ask the same; Theorems 3.1 and 4.2 admit more. *If it may vary with $n$:* their
  proof steps need rates (supp. pp. 6, 15), and our fixed signals ask more than those steps use."
- **Eigenvalue floor.** "*Where their sets are no larger than ours:* our fixed floor implies their (22)–(23)
  (supp. p. 13; standardised columns) and their Condition 3 (p. 955; Gaussian predictors), and asks more. *Where their
  sets are larger* ($\bar r_n\succ\log n$): the two constrain different sets; neither implies the other."
- **Near-exact collinearity.** "*Against their Theorems 1–2:* a condition they do not have. *Against Condition 3 and
  (22), if their sets are at least as large as ours:* theirs gives ours on the sets they cover. *If their sets are
  smaller* ($\bar r_n\prec\log n$): ours constrains sets theirs does not; neither implies the other."
- **Floor and local regressions.** "*Floor on $Q\cup\{l\}$:* of the kind of their Condition 3 and (22), on other sets;
  it compares as the eigenvalue floor does. *Local regressions:* no counterpart."
- **Table cells.** Sentence first, references after; one key reference is enough, since the head has them all.
  - Signal size: "If their $\beta^*$ is fixed: the same as our fixed signals. If it may vary: ours asks more than their
    proof steps use."
  - Collinearity: "None in their Theorems 1–2. Against Cond. 3 and (22): theirs gives ours where their sets are at
    least as large; neither implies the other where they are smaller."
  - Law of the rows: as the paragraph head.
  - Dimension: "admits fewer dimensions" → "allows fewer values of $p$".

## 3. Does the structure still answer first?

Yes. §1 is the headline and one paragraph, and that paragraph gives the reach of the two coded-method theorems.

- **Order inside §2.** Put the designs and "inside" before "How the conclusions compare". §1 ¶2 already uses the three
  design classes, so the reader needs them first.
- **"The theorems" is one 12-line paragraph with four jobs:** the key, the primitive form, the caveats of the
  printed-estimates theorem, and unbiasedness. Give the primitive form its own two lines; it is the fastest evidence
  in the section.
- **The headline points to "the table", which is two pages later.** The headline is verbatim, so add "(Table 1)" at
  the end of §1 ¶2.

## 4. Cuts (the text is exactly at the limit: p. 6 is full)

1. **Table placement.** It floats alone on p. 3 and leaves 45% of that page blank. Placing it at the top of the page
   with text below gives about 20 lines of room and removes nothing.
2. **§2, theorem key (4 lines):** the sentence on the event of the printed-estimates theorem and the unbiasedness
   sentence. The first is detail of the companion section; the second is in §1 and §4.
3. **Heads (about 5 lines):** the shorter forms of §2 above.
4. **Collinearity evidence (2 lines):** "the assumption costs one log factor" repeats "an extra factor"; the gloss of
   $p_{\mathrm{raw}}$ can go.
5. **Leakage-set evidence (2 lines):** "no formal counterpart to compare levels with" repeats the head's "No ordering
   is claimed".
6. **Dimension (1 line):** the head and the evidence both cite the condition of Theorem S; keep the formula in the
   evidence only.
