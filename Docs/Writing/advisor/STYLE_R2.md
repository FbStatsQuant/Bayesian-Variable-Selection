# STYLE_R2: advisor report on the full D2 draft (2026-11-16)

Read: all section files, the appendices, `smcbvs.sty`, the compile log (clean: no overfull box, no undefined
reference) and the PDF, against READER_VERSIONS. The draft follows the style sheet well; §3 is the model for the rest.
Findings only. Numbers are those of the PDF. Note: the visibility example is **Example 5.5** (5.6 is the Assumption).

## 1. Possible drift from READER_VERSIONS (flags; nothing rewritten)

1. **Fixed noise variance dropped in §5.** Theorems 5.2, 5.7 and 5.18 no longer assume (GL), and (FS$_\theta$) states
   the model without "fixed $\sigma_*^2$". The source assumes a fixed variance for all three.
2. **"Completes" widens Theorem 5.18.** §2.6 says a run that produces output "completes", which includes enumeration.
   The source's "the run completes" and "completed run" (Theorem 5.18, Corollary 4.7) mean the sampler status only;
   enumeration is out of scope there. Suggest: delete the synonym; define "*completed run*: a sampler run that ends
   with status completed".
3. **Theorem 4.2 lost two parts.** In the source the level-$M$ form with the size bound (18), and display (19), belong
   to the theorem. They are now Remark 4.3. As a result Corollary 4.7 takes its hypotheses from a remark, and $C_2$ is
   declared in the theorem but used only in the remark. Suggest a Proposition right after Theorem 4.2.
4. **Theorem 3.4 adds a uniformity clause** ("for every $n\ge n_0$ and every design and $\theta^*$ … at that $n$").
   The source says only "the conclusions of Theorem 1 hold". Probably intended; please confirm with Theory. It also
   reuses the name $C_1$ for a different constant.
5. **Theorem 3.12(a) is overstated in prose.** In words: "any one small model"; after the theorem: "no model, the true
   one included". The bound holds only for $|S|\le\min(K-1,p/2)$, which is not "small", and Remark 3.13(i) says it
   fails without that restriction.
6. **Remark 3.5(i), "Theorem 3.4 does not follow from it"** reverses the source ("the two coexist"). Suggest: "in that
   range Theorem 3.1 applies, and Theorem 3.4 is not shown to apply."
7. **Specifications the source does not state:** "for a fixed $c_D>0$" and "every set $T$ of *null* predictors"
   (Remark 3.5(iii)); "the columns *of $X$*" in Assumption 3.11(b); "for every $n\ge3$" in Theorem 5.7, where the source
   has "every admissible $n\ge3$".
8. **(GR), "the unit diagonal only fixes the scale of each predictor."** This brings back the "without loss of
   generality" reading that WD7(2) removed; under (FS$_\beta$) the scale matters. Delete, or say that (FS$_\beta$) is
   read per unit standard deviation.
9. **The superset Occam-sum condition is never stated,** yet Remark 4.9(b) is conditional on it and §7 item 1 is about
   it. Either state it, or (Theory's call) condition Remark 4.9(b) on (NC), which the source says implies it.
10. **Claims in remarks without a status** (my R1 flag 8, still open): Remark 3.2(ii)–(iii); the "alternative
    argument … under a global-overlap condition" in Remark 5.20; "(a numerical counterexample shows this)" has no
    pointer.

## 2. Sentences read twice; terms used before their definition

| Where | Problem | Proposed wording |
|---|---|---|
| §2.2, "No theorem assumes a particular correlation structure" (my R1 wording) | Theorem 3.12(b) is proved on two explicit designs. | "Apart from the lower bounds of Theorem 3.12(b), which are proved on two explicit designs, no theorem assumes …" |
| (NL), one 70-word sentence | Two conditions and three index sets at once; $\mathcal H_l$ and $U_0$ have no words. | Two items, "(i) *no leak*", "(ii) *locality*", as in Assumption 5.6(a). Then: "In words: a null predictor is almost uncorrelated with every true predictor, given any block-sized set; only predictors in its neighbourhood $\mathcal H_l$ matter for this." |
| §4.1, "If fewer than two predictors remain … and $p=p_{\mathrm{raw}}$ outside them." | Four clauses. | "The posterior is not defined if fewer than two predictors remain or the response is constant in the sample. Under the assumptions below such data sets are rare, and they are counted in the exceptional sets of the theorems. Outside those sets, $p=p_{\mathrm{raw}}$." |
| §4.1, "$s\ge0$ is an integer" | The reader takes $s$ for $s_0$. | "$s\ge0$ is an upper bound on the number of nonzero coefficients (not the exact count $s_0$)." |
| Theorem 5.7, "the domain $\mathfrak D$ defined below" | A theorem refers forward, past its status note. Appendix A points to §2.8, where $\mathfrak D$ no longer is. | Move the paragraph that defines $\mathfrak D$ before the In-words of Theorem 5.7. |
| Remark 5.4(i), "The level is sharp in the fixed-design analogue (threshold $\log n+2\log p$ for every $p$)." | Which level, and a threshold of what? | Ask Theory for one full sentence, or drop the parenthesis. |
| Remark 5.9(i), "stops dominating the best of $p$ noise gains … beyond it" | "It" has no referent. | "For larger $b$ the key events of the argument are expected to fail." |
| §5.5, "computed from the four islands' uninterrupted records" | Unexplained. | "… the values the four islands would produce if the run were not interrupted. On completed runs they are exactly the reported values." |
| In words, Theorem 5.18: "close to $0$ or $1$ … are the true model" | Loses the side, and the probability. | "… close to 1 for true predictors and to 0 for null ones, and the reported models are wrong with vanishing probability." |
| Theorem 5.16, "the method's ridge-regularised residual quadratic form" | Undefined; it looks like $\mathrm{SS}_S$ of (7). | If so: "the decrease of $\mathrm{SS}_S$ when $t$ joins $S$ and $y$ is replaced by $\mu$". Also note $\tau_n^2=\tau^2_\emptyset$ of §5.1. |
| §5.4 numerics: "the 2,400-fit study", "the strong-factor experiment", "At these constants" | Study names with no pointer; which constants? | Cite where each study is described; name the constants ($\kappa$, $\underline\theta$, $M_1$, $\sigma_*$) or give their values. |
| Remark 4.9: "on the centred scale; conclusions are in probability"; $C'_H$ | Fragments; undefined constant. | "All limits are in probability." "… for a constant $C'_H$." Define $\bar h_n$ by a formula, or cite where it is defined. |
| Remark 3.19(ii), "with its mean centred over the sample (the fitted mean carries no intercept)" | Three qualifiers in one sentence. | Split: the two rates first; then one sentence on the centring. |
| Remark 3.7, "posterior odds against $S_0$" | Direction ambiguous. | "posterior odds relative to $S_0$". |
| Remark 3.20(iii), "is open; until then" | "Then" has no referent. | "For now the two theorems rest on …" |
| §1, "on one data event of probability tending to one" (also §5 opening) | "One data event" is unclear. | "there is an event, determined by the data alone and of probability tending to one, on which every run …" |
| §6, "one island held 79% of the evidence weight" | Undefined. | "one island would have received 79% of the weight if islands were weighted by their evidence estimates". |
| §7 items 2, 3, 9, 10 | "a bounded ridge cost" and "in the plain form of" are undefined; item 3 is not a question; "printed outputs". | 2: say what would replace the floor, in one clause. 3: "Optimise the constant …". 9: drop "in the plain form of". 10: "reported estimates". |
| Lemma 2.1; (C3); Appendix B (C3) | The lemma has no name. (C3) is a verbless list; in Appendix B it is one 110-word sentence. | "Lemma 2.1 (The posterior miss controls the summaries)". Itemise (C3) as (C2) is. |
| "Every symbol is listed in Appendix A" (§1, §2) | Not so: about 40 are missing ($L$, $c_\psi$, $\bar b$, $C_2$, $M_0$, $a$, $\kappa_H$, $r_n$, $\varpi_n$, $b$, $d_n$, $L_n$, $N_l$, $\omega_n$, $\eta$, $\gamma$, $\Gamma_n$, $\tau_n$, $\mathcal G_n$, …). | Complete the table, or say "the main symbols; constants of a single assumption are defined there". |

## 3. Consistency with the style sheet

- **Remark titles outside the fixed set:** 3.14 "Growing true models", 4.9 "Fixed designs", 5.10 "Comparison with the
  literature", 5.21. Suggest "Further consequences (growing true models)", "Further consequences (fixed designs)",
  "Comparison with Song and Liang (2015)"; 5.21 may keep its title, since it states a result.
- **Items under the wrong title:** 3.10(iii) is a comparison; 4.3(iii) and 5.8(iii) are examples ("Examples, never
  hypotheses" → "Designs that satisfy the assumptions include …"); 5.13(iii) "Not available" belongs to "What is not
  claimed"; 5.20 "At moderate $n$" is mostly about the mechanism and an alternative argument.
- **Block order:** Theorem 5.16 has no lead-in or In-words before it (its In-words comes after the status). Text sits
  between Theorem 3.12 and its status. The lead-in and the In-words of Theorem 3.4 say the same thing twice; keep one
  question sentence as lead-in. Example 5.5 precedes the lead-in of its theorem (fine, but then say "the next example
  prepares the conditions").
- **References to local items:** in §4 the word "Assumption" is missing eight times ("4.1(c) is required", "under
  4.1(e)", "satisfy 4.1(c)"); Remark 3.14 has "type (b)". Always "Assumption 4.1(c)".
- **"Rules out" lines that hold other content:** Assumption 3.3 ("it asks for no eigenvalue condition away from the
  true model": move out, and write "on sets other than the true model"), (EF$_\Sigma$) ("No upper bound … is needed",
  already in Remark 3.10), Assumption 5.1 ("it keeps block regressions well posed").
- **Twins not parallel:** (FS$_\theta$) contains the model and "$s_0\ge1$ fixed"; (FS$_\beta$) does not, and Theorem
  3.9 lists (GL) and (SP) separately. Make them parallel (this also settles flag 1).
- **Smaller points:** the order of labels differs between Theorems 5.7 and 5.18; conclusions are unnumbered in
  Theorems 3.9, 3.17, 4.6 and Corollary 4.7; "shipped" and "the truth" survive in Remark 3.8, §7 item 2 and Appendix
  B; Assumption 5.11(a) uses $Q$ before item (c) introduces it; a stray " ," follows "display (19)" in §4.5.

## 4. The Overview

It does its job: the text is under two pages, and three with the tables. Seven fixes.

1. **The tables float into §2** (Table 1 on p. 3 inside §2.2, Table 2 on p. 4, two pages after the paragraph that
   announces it). Pin them, so that §2 starts after both.
2. **Question 1 answers "Yes." with no conditions,** while question 3 names its conditions. Add: "Yes, under sparsity,
   eigenvalue and signal-strength conditions."
3. **"Every reported estimate is consistent"** needs "when the calibration succeeds" (text and Table 1).
4. **Table 1.** "Design: random" covers both Gaussian rows and i.i.d. pairs; write "Gaussian rows" and "i.i.d.". The
   Rate column uses $M_n$, $\rho_n$ and $n^{-c}$ before they are defined; use words ("parametric", "almost
   $n^{-1/2}$").
5. **Status.** The Status column, its six footnotes and the "Status notes" paragraph are not under the `\showstatus`
   toggle. Three plain labels would do, with the detail left to each note.
6. **Missing:** where the proofs are, and one sentence on which result rests on which (the random-design theorem on
   the fixed-design one; the main theorem and the reported estimates on the random-design theorem; the parametric
   rate on Theorem 3.1).
7. **Abstract:** "Every result is asymptotic" is not true of Theorem 3.12(a) or of the lower bound in Theorem 5.2.

## 5. Remaining notation collisions

- **$y$, $x$, $x_j$.** In §2, $y$ is the standardised response and $x_j$ a column of $X$; in §4, $y$ is the raw scalar
  response, $x_j$ a coordinate and $x_i$ an observation, against the "superscript r" rule. Say so at the top of §4.1.
- **$\beta$.** Working coefficients on the standardised scale (§2.4), posterior draws in original units (§4), regression
  coefficients $\hat\beta_{U,l}$, $\bar\beta_{U,l}$, the case label ($\beta$) in Assumption 5.11(d), and $\beta$,
  $\beta_0$ in Appendix B. Use $\theta_S$ in §2.4, (d1)/(d2) for the cases, and other letters in Appendix B (also for
  $\tau$, $\tau_0$).
- **$q_n$:** window (§4) and size budget (§5.4). The text admits it; rename the budget, for example $k_n$.
- **$M_0$:** energy ratio in Assumption 3.16(c) and smallest level in Theorem 4.2.
- **$\rho$:** a correlation (Example 5.5, Remark 4.3(iii), the numerics), the exponent of $|\mathcal H_l|\le n^\rho$,
  and the rate $\rho_n$. Rename the exponent, for example $b_H$.
- **$W_K$** (prior normaliser) against $W_S$, $W_U$ (sub-vectors of a row).
- **Bare $c$ in displays,** against §2.7: $n^{-cM}$ (Theorem 4.2), "for every $c<\tfrac12$" (Theorem 5.2), Remark
  3.2(ii).
- **Minor:** $C_b$ (block) next to $C_\beta$; $\delta^2_{U,l}$ and the fixed $\delta$ of Assumption 5.11(d); $\kappa$
  (screening floor) and $(\log n)^\kappa$ in Remark 5.8(ii); $\pi(\mathcal T)$ lacks "$\mid y$"; Song–Liang's $r_n$ in
  §4.5 against our $r_n$.

## 6. Example 5.5

The arithmetic is right: with unit variances, $\operatorname{Cov}(W_1,W_1-W_2)=1-\rho$. The inference on $Q$ is right:
a fixed nonzero $\operatorname{Cov}(W_3,W_1)$ violates Assumption 5.6(a)(i) at $U=\emptyset$ for large $n$, so
$3\in Q$. Three wording points. "(V) requires $1-\rho\ge a$" is the case $U=\emptyset$ only: write "(V) requires, among
other things". Say "consider three of the $p$ predictors", and that $\operatorname{Corr}(W_3,W_2)$ may take any
admissible value. Add that this design violates (NL), so Theorem 5.2 does not apply to it, while Theorem 5.7 does.

## Top five

(1) Clear flags 1–3 of §1 first: the fixed noise variance in §5, the word "completes", and the parts of Theorem 4.2
now sitting in a remark. (2) State or remove the three undefined conditions and quantities that results depend on: the
superset Occam-sum condition, the global-overlap condition, and the quadratic form in Theorem 5.16. (3) In the
Overview, pin the tables, put conditions on the first "Yes", and put the status material under the toggle. (4) Finish
the mechanical consistency pass: remark titles, "Assumption" before every local item, "rules out" lines, block order
at Theorems 3.12, 5.7 and 5.16. (5) Remove the last collisions that a reader will trip on: $y$/$x$ in §4, $\beta$,
$q_n$, $M_0$, $\rho$, $W_K$; and make Appendix A complete or say what it omits.
