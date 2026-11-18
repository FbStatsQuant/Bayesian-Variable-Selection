# STYLE_A3_R2: advisor note on the draft of "What we prove", v2 (2026-11-16)

Read: all v2 section files, `CUT_LIST.md`, `OUTLINE_DECISIONS.md`, against v1, the ledger and the Theory notes.

## (a) Format and "why it matters"
- Results 1–4 follow the format. Result 5 does not: as Remark 3.3 it has no "why". Add one line at its head, for
  example "It shows that the rate of Result 1 is the right one, and why the posterior is not a point mass at $n=200$."
- Result 3's "why" is the best. Results 1 and 4 convince.
- Result 2's "why" joins two claims; "prediction is reliable" is more than a Hellinger statement, and the Song–Liang
  clause is not a reason. Suggest: "The posterior describes the response correctly even when some true predictors are
  too weak to be selected, so prediction does not depend on perfect selection."

## (b) Read twice; is §2 enough without v1?
Not quite. Six terms are used and never defined in v2, and three objects have no definition a reader can use.
1. **Undefined terms:**
   - "certifies / certified" (Remark 5.4(ii), Theorem A.12);
   - "completed run", "the run completes" (Theorem 6.2, Corollary A.8, Remark 4.3);
   - "the calibration succeeds" (§6);
   - "valid data set" (Theorem A.9);
   - the design names S1, IND, AR, block, factor (§6 scope, Remark 5.4(iv)): point to Assumptions §2;
   - blocks $C_b$, $J$ (Appendix C).
2. **The working model is missing.** §2 puts priors on "the coefficients" and "the noise variance" of a model it
   never states. One clause: "of a working Gaussian linear model for the standardised data".
3. **$F$ has no name**, yet "log score" is used in §2.2 and before Corollary A.8.
4. **The start law has no formula**, yet Theorem A.9 is a statement about $\pi_0(S_0)$. Restore v1's two-line display.
5. **Notation paragraph:** $o$, $O$, $o_P$, $\gg$, $\gtrsim$ and $\vee$ are used and not defined.
6. **§1:** "The constants … are explicit where they are displayed and conservative; they are not part of any
   assumption we judge." Suggest: "The explicit constants are conservative. The assumptions section judges the
   qualitative conditions, not the constants."
7. **§4, In words:** $c_{\mathrm H}$ and $M$ appear before "level" is introduced; "a set of data sets" → "an event".
8. **§6, In words:** "the conditions of Result 3 hold with no leakage at all" is not what Theorem 6.2 assumes (it
   does not use Assumption 5.2). Say "visibility, and no null predictor more than weakly correlated with a true one".
9. **(C2):** "an allocation at least the method's own polynomial requirement formulas" is not a sentence.
10. **§2.3:** "an assumption used by one result only is stated with it"; but (V) and (FS$_\theta$), used by Results 3
    and 4, are stated in §5.
11. **Remark 4.3** cites "(c)" and "(d)" bare; write "Assumption 4.1(c)".

## (c) Against v1, the ledger and the Theory notes (flags, not fixed)
The condensed §2 (run, prior), Remark 3.3(a)–(b), Theorem A.9 and the §6 scope paragraph state nothing wrong; their
gaps are in (b). The IDEAL-W⁺ sentence in the Result 3 status matches the note. The flags:
1. **After Theorem A.3, "neither contains the other".** v1: Theorem 3.4 contains Theorem 3.1 when
   $C_\beta^2\varphi_0^2>c_1$; the two coexist only for $c_0<C_\beta^2\varphi_0^2\le c_1$.
2. **Theorem A.12, the numerics** keep the favourable counts only. Dropped from v1:
   - the certified model contained every true predictor in 61 of 122 strong-factor fits at $n=50$ (18 of 20, 30 of 30
     at larger $n$);
   - "At these constants the size budget requires $n\gtrsim1{,}450$", which the reader versions record as kept by HQ;
   - "a run is not claimed to certify a small model with probability tending to one".
   Next to "every completed run certified", the last omission misleads. None of the three is on the cut list.
3. **Theorem A.12, "(SP) is not assumed"** is new text. v1 says "no bound on $s_0$" only of the margin form (v1 Thm
   5.17). Here $s_0\le M_1/\underline\theta$ follows from the hypotheses.
4. **Theorem A.11 and (AG).** `OUTLINE_DECISIONS.md` says (AG) is presented there; the draft does not mention it.
   Theory should say whether the fixed-design delivery clause needs it in the statement.
5. **Remark 4.3, "it carries over to the list … a completed run returns"** drops the condition of Corollary A.8 (the
   list must hold posterior mass at least $n^{-c_{\mathrm H}M/2}$, which the run does not certify).
6. **§4 setting** drops v1's convention that the posterior is undefined on some data sets, which are counted in the
   exceptional event. Display (8) needs it.
7. **Proposition 6.1** drops "on the event that the sampler is used and the calibration succeeds" (v1: "on
   $\mathcal A$").
8. **Table 1:**
   - Result 1: "Proved and checked" is not the H1 label ("proved and independently verified").
   - Result 4: "Consistency: as Result 3" is wrong; Theorem 6.2 does not assume the leakage-set conditions.
9. **Remark 5.4:**
   - (i) "in practice $\mathfrak D$ contains every feasible $(n,p_{\mathrm{raw}})$" repeats the unrecorded result of
     the status note, with no status and vaguer words;
   - (iii) drops v1's "(heuristic; whether the conclusion fails is open)" and reads as fact.
10. **Remark 3.3(c), "the same quantity as in (b)".** (b) bounds the posterior miss; (c) is a ratio to the weight of
    $S_0$. Same expression, different object.
11. **§6 scope, "no theorem yet covers the printed … evidence estimate".** Proposition 6.1 covers its unbiasedness;
    write "the consistency of".
12. **Smaller:**
    - "padded with zeros" is dropped for $\bar\beta_{T,l}$ (§5), so Assumption 5.2(c) subtracts vectors of unequal
      length;
    - the primitive-terms sentence after Theorem 3.1 omits the Gaussian linear model;
    - $m_{\mathcal C}$ in Assumption A.4 is $m$ in Theorem A.5.

## (d) The cut list
- **Bring back:**
  - one sentence of v1 Remark 5.3 under Theorem A.9: with a leakage set, the start law concentrates on the models
    between the true model and $Q$. Result 3's "In words" and the assumptions section both lean on it;
  - the three items of (c)2.
- **Record on the list** (dropped but not listed): the §4 convention of (c)6; the model-size evidence of the screening
  numerics.
- **Still in the document, could go:**
  - Remark 5.4(i), which the status note and Appendix C already say;
  - the "Rules out" line of Assumption A.10, the only one left in v2;
  - three lines of derivation in Remark 3.3(c): keep the formula, the heavy-tail clause and the numbers.
- The other cuts are sound.

## (e) The budget
The main text ends on p. 12, so it is about 11.3 pp with statuses on: within the limit, with 0.7 page spare.
- **Spend it on (b)1–5 and (c)5–7,** about 15 lines in all.
- **Tighter without loss:**
  - each "Assumptions, and where they are judged" list repeats the theorem's "Assume …" sentence; keep the gloss and
    the pointer, drop the repeated labels where the theorem has just listed them (about 8 lines over seven lists);
  - Remark 5.4(i) (2 lines);
  - Remark 3.3(c) (3 lines);
  - the abstract repeats §1's first paragraph (5 lines).
