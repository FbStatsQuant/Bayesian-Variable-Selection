# STYLE_A2_R2: advisor note on the draft "Are the assumptions reasonable?" (2026-11-16)

Read: `assumptions.tex` and its PDF, against `TRACK_B.md`, `AUDIT.md` §6 and §9, `CHECKPOINT_3.md`. The D2 numbers
cited in the draft are right. The draft is now 5 text pages, a table page and a page holding one reference.

## 1. Where to cut (about 35 lines; no evidence lost)

- **§5 (14 lines) repeats §1 ¶2–3.** Keep its two new sentences, moved: "real data … may be outside" into the
  visibility paragraph, and the sentence on the proof route into the no-leakage paragraph. Delete the section.
- **§6, second bullet (6 lines).** Name three of the ten items as examples, not all ten. In the first bullet write
  "the posterior-summary lemma (Lemma 2.1)" for its three-line description.
- **Said twice (5 lines).** "Inside" is defined in §1 and again in the caption. The uninspected supplement is in §1
  and under signal size. The case $U=\emptyset$ is in the visibility head and its first evidence sentence.
- **Evidence that can be shorter (8 lines):**
  - law of the rows: give the constants and "a two-line computation, independently checked" for the inline derivation;
  - bounded leakage set: keep the second quotation only;
  - dimension: drop the sentence on union bounds;
  - visibility: drop "the theory's map of design families records \ldots as automatic", and keep the covariance bound.
- **Layout (8 lines and the last page).** "3 Summary" is an empty heading, because the table floats to p. 3: pin the
  table and drop the heading. A compact title block brings the reference back onto the last text page.

## 2. Sentences read twice

| Where | Problem | Proposed wording |
|---|---|---|
| §1 ¶3, "needs *no leakage*" | Reads as "does not need leakage". | "needs one more condition, *no leakage*:" |
| §1 ¶1, "hold on every design we simulate"; "a fixed number of fixed nonzero coefficients" | "Inside" is defined three paragraphs later, and the $10^6$ plan is not simulated. Double "fixed". | "every design of our studies and of the $10^6$ plan satisfies their assumptions (in the sense defined below)"; "a fixed number of nonzero coefficients that do not change with $n$". |
| Eigenvalue floor, head: "stronger in level and on smaller sets" | Parses as "stronger on smaller sets". | "a higher level, on smaller sets, for a stronger conclusion". |
| Signal size, "Above, … Below, …"; head "((BC), …" | Openers unclear; doubled parentheses in four heads. | "For the upper bound, … For the lower bound, …". |
| Bounded leakage set, "exceeds the level $o(\sqrt{\log n/n})$" | Not well formed. | "exceeds a level $\varpi_n=o(\sqrt{\log n/n})$". |
| No leakage, §5: "the start law"; "the cheap first stage" | Never defined in this section. | Add "(the distribution the sampler starts from)". |
| §5, "falls below every power of $n$" | Which powers? | "below $n^{-k}$ for every $k$", if that is the meaning. |
| §6, "Pending as claims, not premises"; "one correction to how the record links …" | Opaque. | "Two supporting lemmas behind … are not yet independently checked." |
| Law of the rows, "$z_{j_i}$" | D2 writes $\zeta_j$; $z$ is undefined here. | Use $\zeta$. |
| Table | "truth(s)", "nulls"; "Cor. 1, p. 954; p. 950"; "Dimension: stronger". | "true predictor", "null predictor"; say what p. 950 is; footnote "weaker on the lower range". |

Fixed model size has no "Rules out" line; the other ten have one.

## 3. Against TRACK_B and AUDIT (flags, not fixed)

1. **§5 ¶1, "For all of them the posterior theorems hold."** "All of them" includes real data. The source says only
   that a real-data user *may* be inside those theorems.
2. **§5 ¶2, "The present proof route cannot be extended to these designs."** The source says this of AR and BLK
   only. For S3, S4 and S6 it names a candidate repair (not proved) that would bring them inside.
3. **Unbiasedness is stated three times with no status,** and §6 omits its two pending inputs (AUDIT X1, the frozen-run
   identities, and X5, the pooled form).
4. **§6, "Posterior theorems: no open premise"** as a heading, while D2 marks the expectation bound of Theorem 3.1
   conditional on two unchecked lemmas. The text below it is accurate; the heading claims more.
5. **Eigenvalue floor, "on smaller sets".** The draft compares $O(\log n)$ with $\bar r_n+1$, which does not show
   "smaller". TRACK_B's support is the parenthesis the draft dropped: the floor is needed only on sets of
   $(2A+2)s_0+2$ predictors.
6. **Visibility, "a near-cancellation for S5, none for the others."** TRACK_B lists the strong-factor study's own
   version of S5 separately, with no cancellation found. The draft merges the two.
7. **Footnote $a$** (my earlier flag, still open): a one-factor design is "inside" in the strong-factor study and
   "unclear" as FAC. §2 now shows both as "one factor at 0.3", so a reader will ask.
8. **Smaller:**
   - §1 ¶1, "needs only this" omits the Gaussian linear model.
   - Signal size drops "under (4) alone their main text states no bound".
   - "Rules out" for the row law names heavy tails only, though Gaussian rows exclude every non-Gaussian law.
   - §2 drops that FAC is contingent and run at $p=10^4$ only.
   - "Rules out" for signal size says "shrink faster than", but beta-min also excludes signals of that order with a
     small constant.
