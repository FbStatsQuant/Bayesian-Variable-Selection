# STYLE_R1: advisor report on D2 (§2 and §3.1), round 1 (2026-11-16)

Read: `ASSIGNMENT_1.md`, `what_we_prove.tex` and its PDF, `smcbvs.sty`, the reader versions of Theorems 1–10, the claims
card, the source notation file and the status ledger. Findings and recommendations only. Nothing here changes a
statement or a status; possible content issues are listed as flags in C3.

## A. Style sheet (for all of D2 and D1)

**Voice and tense.**
- "We" + present tense for what the paper does (we assume, we show). "The method" + present tense for what the software
  does. Theorem statements are impersonal and in the present tense.
- One claim per sentence, about 30 words at most. One idea per paragraph. No sentence starts with a symbol.
- British spelling, as in the draft. "With probability tending to one" is written in words.
- One word per concept: *predictor* (not variable, covariate; "column" only for a column of a matrix); *model* = a set
  of predictors; *true model*, *true predictor*, *null predictor* (not "the truth", "truths", "nulls"); *over-fitted
  model* = a model that strictly contains $S_0$; *run*; *reported* (not "printed").
- Not in running text: shipped, printed, branch, ladder, covered configuration, and "as coded" (keep it in the D1 title
  and in the one sentence that defines "the method").
- Section summaries (2–3 sentences) are the first paragraph, in roman type. Italic is for a term at its definition.

**Theorem block, in this order.**
1. *Lead-in:* one or two sentences on the question the result answers.
2. *In words:* at most four sentences; only $n$, $p$ and the rate as symbols. It names the conditions informally, in the
   order of the formal list. It comes **before** the assumptions, so the reader knows what they are for.
3. *New assumptions only:* label, name, one-sentence statement, then a "Rules out:" line in normal size. Nothing else.
4. *Theorem [name]:* sentence 1 is the setting. Sentence 2 is "Assume …", in the fixed order model, signal, design,
   search, conventions. Then "Then" and the conclusions in numbered displays. No commentary inside.
5. *Status note:* outside, with `\status`, using only the three fixed phrases. If parts differ, one line per display.
6. *Remarks:* fixed titles, fixed order: Further consequences; On the assumptions; What is not claimed; At moderate $n$;
   Comparison with Song and Liang (2015). At most three items each, with italic run-in heads. A remark that asserts a
   bound belongs under "Further consequences" and is covered by a status.

**Displays and constants.**
- Number a display if it is cited, and number every theorem conclusion. Each display has a sentence in words next to it.
- One statement per display line. No line wider than the text (display (10) is 58pt overfull: use two aligned lines).
- Write the rate out, $\sqrt{\log n/n}$. Use `:=` for definitions and $\max_{j\in[p]}$ for index ranges.
- "Fixed" means "does not depend on $n$". Each constant introduced in an assumption has its own letter or subscript,
  never a bare $c$ or $C$. Generic $C$, $c$ appear only in prose. A constant that recurs across displays of a theorem is
  numbered ($C_1$).
- Name the size class in words before the bound: "sets of bounded size", "sets of logarithmic size".

## B. Assumption labels: decision

**Not the 35 global mnemonic labels, and not grouped numbering. Use two tiers.**

- *Why not 35 mnemonics.* Twenty-two of them are used by one theorem only. A reader cannot hold (FF), (VF), (BL), (LQ),
  (EK), (FC), (SB), (GM), and a two-letter code does not say where it is defined.
- *Why not (P1)–(P5), (S1)–…* Numbers carry no meaning. Remarks that compare conditions ("under (SE) and (BM)(a) the
  margin holds") become unreadable.
- *Rule.* A condition used by **two or more theorems** gets a global mnemonic name, stated once at first use. A
  condition used by **one theorem** is an item of that theorem's own numbered Assumption (shared counter with theorems),
  cited as "Assumption 5.3(b)". Twins share a label and differ by a subscript that names the scale or the population.
- *Conventions are not assumptions.* The three computational ones get their own environment, "Convention (C1)–(C3)", so
  a statistician sees at once which hypotheses are statistical. (MC) must go in any case: it reads as "Monte Carlo".
- *One table.* Appendix A gets "Assumptions at a glance" (label, in words, where stated, used by), and the Overview gets
  a theorem-by-assumption grid.

| Family | Global label (13 + 3) | Replaces | Used by (reader numbering) |
|---|---|---|---|
| Model | (GL) Gaussian linear model | (GL) | 1, 1′, 2, 3(b), 5–8, 10 |
| | (DIM) Dimension | (DIM), without "$n\to\infty$" | 1, 1′, 2, 5–7, 10 |
| | (GR) Gaussian rows | (GR) | 2, 5, 6, 10 |
| Signal | (SP) Sparsity | (SP) | 1, 1′, 2, 5–7, 10 |
| | (BC) Bounded coefficients | (BC) | 1, 1′, 7 |
| | (BM) Beta-min, forms (a), (b) | (BM) | 1, 7 |
| | (FS$_\beta$) Fixed signals, raw scale | (FS) | 2 |
| | (FS$_\theta$) Fixed signals, standardised scale | (FT) | 5, 6, 10 |
| Design | (EF) Eigenvalue floor on sets of bounded size | (SE), which reads as "standard error" | 1, 7 |
| | (NC) No near-exact collinearity, "the vanishing floor" | (NC) | 1, 1′, 7 |
| | (EF$_\Sigma$) Population eigenvalue floor | (PE) | 2, 6, 10 |
| Search | (V) Visibility | (V) | 5, 6, 10 |
| | (NL) No leakage | (NL) | 5, 10 |
| Conventions | (C1) Method; (C2), (C2$^+$) Delivery; (C3) Sampler | (MC); (DC), (DC$^+$); (SC) | 5–8, 10; 6, 7; 10 |

| Local Assumption (numbered in its section) | Items | Replaces |
|---|---|---|
| Identifiability margin (Thm 1′) | (a) floor on the true model; (b) margin | (ID) |
| Omitted variables (Thm 4) | (a) candidate model; (b) floor; (c) signal relative to residual variance | (CM), (CF), (CS) |
| Distribution (Thm 9) | (a) i.i.d. rows, Gaussian linear model; (b) sparsity and dimension; (c) sub-Gaussian predictors; (d) no near-exact collinearity; (e) bounded signal | (IID), (SD), (SG), (NE), (BS) |
| Detectable signal (Thm 9B) | one item | (DS) |
| Start law (Thm 5) | small-set floor; the uncorrelated-nulls hypothesis is stated inline in the theorem | (SF), (UN) |
| Main theorem (Thm 6) | (a) polynomial leakage set; (b) local regressions; (c) floor on $Q\cup\{l\}$ | (PL), (LR) |
| Reported model, fixed design (Thm 7) | (a) floors; (b) visibility; (c) bounded leakage; (d) size of the leakage set | (FF), (VF), (BL), (LQ) |
| Certified screening (Thm 8) | (a) eigenvalue floor; (b) fixed signal bounds; (c) size budget; the gain margin of Thm 8′ is inline | (EK), (FC), (SB), (GM) |

Notes. (i) Local labels suit Theorem 9 in particular: its model differs from (GL) and (DIM) ($p_{\mathrm{raw}}\le n^A$,
$\sigma_*$ may vary with $n$), and a shared label would hide that. (ii) I considered one parametrised floor EF$(k,\varphi)$
for all eigenvalue conditions. I do not recommend it now: the scales differ ($\varphi_0^2$, $\kappa$, $c_\psi/n$, sample or
population), and each instance would need a new check against its source. (iii) `\as` needs a label key separate from
the printed form, for subscripted labels.

## C. Line-level findings, §2 and §3.1

### C1. Wording and order (proposed text in the right column)

| # | Where, quoted | Problem | Proposal |
|---|---|---|---|
| 1 | §2 Notation: "$I_n$ is the …", "$\log$ is the …" | Sentences start with symbols. $O$, $o$, $O_P$, $\asymp$, $\lesssim$ sit in §2.7, but the assignment asks for one Notation paragraph. | Start each with words. Add: "A star marks a true parameter value; the true model and its size are $S_0$ and $s_0$. $I$ is an identity matrix whose size is clear from the context." Move the asymptotic symbols here. |
| 2 | §2.1 ¶1: "a response vector $y^{\mathrm r}$" | The superscript r is not explained. "Model" and "null predictor" are never defined. | Add "(the superscript r marks raw data)". Add: "A *model* is a set $S\subseteq[p]$ of predictors. Predictors outside $S_0$ are *null predictors*." |
| 3 | §2.1 bullet 2 | Four ideas in one bullet. "Generic population row" needs a second read. The subscript $n$ on $m_n$, $\Sigma_n$ is unexplained. | Split. "We write $W\sim\mathrm N_p(0,\Sigma_n)$ for a centred copy of one row. The subscript $n$ recalls that this law may change with $n$." |
| 4 | §2.1: "A law for the rows is an assumption … not a choice of a particular family of designs." | Reads as a reply to a debate the reader has not seen. | "No theorem assumes a particular correlation structure, such as equicorrelation or autoregressive decay. Such structures appear only as examples." |
| 5 | §2.2: "On this scale the true coefficients and the mean signal are" | $y$ is also rescaled, $\theta^*$ is not; "this scale" is unclear. | "In terms of the standardised predictors, the centred response is $P^\perp_{\mathbf 1}y^{\mathrm r}=X\theta^*+P^\perp_{\mathbf 1}\varepsilon$, where $\theta^*:=D\beta^*$. So $\theta^*$ is in the units of the raw response." Also "(divisor $n-1$)" after "sample standard deviations". |
| 6 | §2.3 Model prior: "each predictor enters the model independently with the same probability $q$, and $q$ itself is drawn" | Independence holds only given $q$. | "A probability $q$ is drawn from $\mathrm{Beta}(1,p)$. Given $q$, each predictor enters the model independently with probability $q$." |
| 7 | Example 2.1: "The probabilities add up to one, so here the cap does not bind." | The logic runs backwards. | "Here $K=p$, so no model is excluded, and the weights already add up to one." The example belongs to D1; D2 keeps a pointer. |
| 8 | §2.3 Coefficients: "Given a model $S$ and the noise variance $\sigma^2$ …" | Priors come before the likelihood that introduces $\sigma^2$. $\beta_S$ is on the standardised scale, where the true value is called $\theta^*$. "IG$(a_0,b_0)$" does not say shape and scale. | Likelihood first: "The method fits the working model $y\mid S,\theta_S,\sigma^2\sim\mathrm N_n(X_S\theta_S,\sigma^2I_n)$ to the standardised data. Here $\theta_S$ and $\sigma^2$ are working parameters, not the true values." Then the two priors; "shape $a_0$ and scale $b_0$". |
| 9 | §2.4: "an Occam factor that charges about $(n+1)^{1/2}$ for each predictor" | Direction of the factor is ambiguous. | "a penalty for model size (an Occam factor): in a well-conditioned model, each extra predictor multiplies $m(S)$ by about $(n+1)^{-1/2}$". |
| 10 | §2.4: "within $\delta_n$ of the truth"; "Two elementary facts link them." | Every theorem uses these facts, but they have no number. | Make them Lemma 2.x. "… within $1-\pi(S_0\mid y)$ of its ideal value: 1 for a true predictor, 0 for a null one." Name $Z$ at (7), where it first appears. |
| 11 | §2.5 summary: "a deterministic start, an internal calibration, and a local search" | "Deterministic start" contradicts a start law that is sampled. Run, seed, calibration, enumeration, admissible are used later and never defined. | Open §2.5 with a paragraph "A run": one sentence each for run, seed, calibration, the enumeration case, and "produces output" (now at the end of §2.5). |
| 12 | §2.5 Local search: the 30-word parenthesis | Definition buried in a parenthesis; "or after at most". | "Two models are neighbours if one comes from the other by deleting one predictor, adding one (only while the size is below $K$), or swapping one member for one non-member. Starting at the start mode, the method scans all neighbours of the current model and moves to the best one if its log score is strictly higher. The search stops at the first scan with no improvement, or after $\ell_n+\lvert\tilde S_0\rvert$ moves, whichever comes first." |
| 13 | §2.5: "The method *certifies* $\hat S$ … when either the model space was small enough …" | 60-word sentence, two cases, past tense. | "The method certifies $\hat S$ in two cases. (a) It enumerated $\Omega$; then $\hat S$ maximises $F$ over $\Omega$. (b) $\hat S$ is the end point of a local search whose last scan found no improvement; then no neighbour of $\hat S$ has a higher log score." |
| 14 | §2.6 (DIM): "$n\to\infty$ and … ($p\gg n$) are allowed and are the main case." | $n\to\infty$ is the framework, not a condition "at that $n$". Commentary inside the statement. $\gg$ and "fixed" are used before §2.7 defines them. | "(DIM) $2\le p\le n^A$ for a fixed $A\ge1$. *Rules out:* $p$ growing faster than every power of $n$, for example $p=e^{n^{a}}$. The case $p\gg n$ is allowed." Put §2.7 before §2.6. |
| 15 | §2.6 (DC): "An idealised machine, the covered configuration, ideal random numbers, and a declared memory and time allocation at least the method's polynomial envelopes" | A fragment with four undefined terms. (SC) has the same problem ("realise their stated kernels"). | "Convention (C2) (Delivery). The computer does exact arithmetic and never overflows or fails. The method runs in its default configuration, with ideal random numbers. The user grants at least the memory and time that the method's own requirement formulas, polynomial in $(n,p_{\mathrm{raw}})$, ask for. Appendix B gives the full list." |
| 16 | §2.7: "Constants written with Greek or Latin letters in an assumption … are fixed"; "$s_0$ is fixed unless …"; "$r_n:=$" | The first is vacuous. The second duplicates (SP). $r_n$ is never used. | "A quantity is *fixed* if it does not depend on $n$. Every constant introduced in an assumption is fixed." Delete the other two. |
| 17 | §3.1 ¶1: "We first state the assumptions … Each comes with one line on what it rules out." | Meta-comment; the reader meets five formal conditions before knowing the goal. | Replace by the lead-in and the In-words paragraph (style sheet, step 2). |
| 18 | (BC): "under which the posterior of the noise variance could drift off scale" | "Drift off scale" needs a second read. | "*Rules out:* true coefficients that grow with $n$. The signal energy $\lVert X\theta^*\rVert^2$ then stays of order $n$, like the noise energy." |
| 19 | (NC): title with $O(\log n)$; "$X_S^\top X_S$"; "On the correlation scale the floor is $g_0/(n-1)$, so it vanishes" | $G_S$ was defined for this. The second sentence is not a "rules out". "The vanishing floor" is used later as a name and never introduced. | Title "No near-exact collinearity in sets of logarithmic size"; $\lambda_{\min}(G_S)\ge g_0$. "*Rules out:* exact, or nearly exact, linear dependence among $O(\log n)$ predictors; duplicated predictors, for instance." Then, outside: "This is far weaker than (EF). For correlation matrices it reads $\lambda_{\min}(\hat R_S)\ge g_0/(n-1)$, a floor that vanishes as $n$ grows. We call (NC) the *vanishing floor*." |
| 20 | In words, Thm 3.1: "on average over the noise, uniformly over all such designs"; "within $O_P(\cdot)$ of 0 or 1" | "Uniformly over" needs a second read. "Of 0 or 1" loses which side. | "Then, on average over the noise, the posterior mass outside the true model is at most a constant times $\sqrt{\log n/n}$. The constant is the same for every design that meets the conditions. As a consequence, with probability tending to one, the highest posterior model and the median probability model are both the true model. Every inclusion probability is within order $\sqrt{\log n/n}$ of 1 for a true predictor and of 0 for a null one." |
| 21 | After Thm 3.1: "drops the eigenvalue floor away from the true model" | "Away from" needs a second read. | "The next result asks for an eigenvalue floor on the true model only, and for no beta-min condition. In exchange it asks for an identifiability margin: every small model that misses a true predictor must leave part of the signal unexplained. The vanishing floor (NC) is kept." |
| 22 | (ID): one 55-word sentence; "Floor on the truth"; "leaves residual signal" | Two conditions and three restrictions on $S$ in one sentence. $\mu$ was defined for this. | Two items: "(a) *Floor on the true model.* …" and "(b) *Margin.* Every model $S\in\Omega$ that misses a true predictor and has at most $j_0$ predictors outside $S_0$ leaves unexplained signal $\lVert(I-P_S)\mu\rVert^2\ge c_{\mathrm{id}}\,\sigma_*^2\log n$." |
| 23 | In words, Thm 3.2 | One 50-word sentence. "Of order $\log n$" hides that it is a lower bound. | Three sentences; "at least a constant times $\sigma_*^2\log n$". |
| 24 | Remark 3.3 "On the assumptions", items (i)–(vii) | Seven items on three subjects. (i), (ii), (v) are consequences, not comments on assumptions. The determinant condition in (vi) is unreadable inline. | Split: "Further consequences" (i, ii, v) and "On the assumptions" (iii, iv, vi, vii). Display the determinant condition. (i): "inclusion probabilities of true predictors are close to one and those of null predictors close to zero, uniformly in $j$". (iii): replace "the two theorems coexist" by a sentence that says which theorem applies in that range. |
| 25 | Remark 3.4: "times a $\chi^2_1$ factor"; "a mixture over" | The form of the factor is unclear. | "its posterior odds relative to $S_0$ are of order $n^{-1/2}/p$, times a random factor [exact form from Theory]"; "the posterior is spread over $S_0$ and many models with one extra null predictor". |

### C2. Symbols: collisions and unused definitions (fix once in `smcbvs.sty`, before more text is written)

- *Within §2–§3.1.* $c$: generic (§2.7), the margin constant in (ID), and a third meaning in Remark 3.3(ii). $C$:
  "changes from line to line", yet (10) reuses the $C$ of (9) as $4C$. $J$: number of blocks in (8), a set in Remark
  3.3(vi). $m$: the integer in $[m]$, the mean $m_n$, the marginal likelihood $m(S)$. $R$: number of islands, and
  $\hat R_S$.
- *Defined, then not used in §3.1.* $r_n$, $\delta_n$, $\mu$. Delete $r_n$. Keep the term "posterior miss" but write
  $1-\pi(S_0\mid y)$ and drop $\delta_n$. Use $\mu$ in (ID).
- *Ahead, in Theorems 2–10.* $\varpi$ (model prior) against $\varpi_n$ (leak bound, main theorem); the prior needs no
  symbol, since only $w$ is used after (4). $b_0$ (inverse-gamma scale) against $b_0$ (signal floor, certified
  screening). $Q_S$ against the leakage set $Q$. $\nu$ against $\nu_n$. $H_S$ against the sets $H_l$ and Hellinger $H$.
  $D$ against the data set $D_n$. $z_S$ against $z_j$. $M$ (four meanings). $\delta$ in $\delta^2_{U,j}$. Optional:
  $\tilde S_0$ differs from $S_0$ by a tilde only.

### C3. Flags for the manager (possible content or status issues; not rewritten)

1. **Dimension of $X^{\mathrm r}$.** §2.1 defines it as $n\times p_{\mathrm{raw}}$, but its rows are $\mathrm N_p$, $D$ is
   $p\times p$ and $S_0\subseteq[p]$. One sentence is missing on what happens to a removed predictor in model (1). The
   source notation has the same gap.
2. **"We may and do take $\Sigma_n$ to be a correlation matrix."** The reader versions state this as a hypothesis. As a
   reduction it rescales $\beta^*$, which matters for a condition on raw coefficients. Theory should choose the form.
3. **Signals fixed on the standardised scale.** Theorems 5, 6 and 10 write $y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$
   with deterministic $\theta^*$, so $\beta^*$ in (1) depends on the design. (GL) as worded does not clearly cover this.
   The last sentence of §2.2 ¶2 hides it.
4. **§2.6: "Two assumptions are used by every theorem."** Not so in the reader versions: sharpness part (a) uses
   neither, certified screening does not need (DIM), and the omitted-variables and distribution theorems have their own
   model.
5. **(DC) contains a conclusion:** "Under (DC), a run produces output on the bounded domain …". That clause belongs to
   the delivery theorems. The convention should only define $\mathfrak D$ and (DC$^+$).
6. **§3 opening summary.** "Cannot be improved in general" can be read as "on every design"; the source claims
   sharpness on the witness designs only. "The same holds when the fitted predictors omit some" is not the same
   statement: the omitted-variables target is the support of the best candidate predictor.
7. **Status note of Theorem 3.1.** Display (10) contains $1-4C\sqrt{\log n/n}$ with the $C$ of the expectation bound
   (9), which is conditional. "(10): proved and independently checked" may hold only for "$\to1$" and the $O_P$ part.
8. **Remark 3.3 (ii), (v), (vi).** They assert bounds with no stated hypotheses and no status. (v) drops the source's
   "uses a coefficient bound instead". "(numerical counterexample)" has no pointer. Please confirm that "specificity",
   not "sensitivity", is meant in (ii). $c_D$ in (vi) is undefined.
9. **(ID), "it does not restrict correlations among the other predictors."** Stronger than the source wording ("no
   eigenvalue condition off $S_0$ beyond the vanishing floor").
10. **$c_0(s_0,A)$, $c_1(s_0,A)$** are called explicit but are not given. The source asks for "a sufficiently large
    constant" in the statement and the formulas in an appendix. No such appendix is planned.
11. **$m(S)$ is defined up to a constant,** so $Z$, and "unbiased for $Z$" later, need the normalisation fixed.
12. **"Produces output" against "completes"** (Theorem 10, Corollary 9C). If they are the same event, use one term; if
    not, define both in §2.5. Also "local searches" (plural) in §2.5, where only one search is described.
13. **Theorem 3.2, "the conclusions of Theorem 3.1 hold."** Cite (9) and (10), and say whether the clause "for every
    $n\ge n_0$ and every design" carries over.
14. **A reader's check.** The lemma of C1 #10 plus Markov's inequality gives $1-2C\sqrt{\log n/n}$; the theorem states
    $4C$. It is correct as stated, but a reader will ask. Theory may want to say which is intended.
15. **(SP) also excludes $s_0=0$.** Say so, or say where the empty true model is covered.
16. **Verbatim Song–Liang text.** The card sentences are in shorthand ("Narrower in dimension ($n^A$ vs …)"). Ask HQ
    whether "verbatim" allows the same claims in full sentences.

## D. Structure

- **Section order: keep it.** It follows the four questions of the abstract and the owner's grouping. Three changes
  inside it:
  1. §4 (distribution) has its own setting (i.i.d. pairs, $p_{\mathrm{raw}}$, level $M$, window $q_n$). Open it with a short
     "Setting for this section" and keep its assumptions local (B).
  2. §5 keeps the build-up order (start law, reported model, certified screening, reported estimates), but its first
     paragraph states the main theorem in words, since it arrives late.
  3. Pooled-evidence unbiasedness is planned twice (§5.4 remark and §6). State it once in §5.4 and cite it from §6. §6
     has no theorem: keep it to half a page titled "The parallel method: what is and is not proved".
- **§2:** move the asymptotic conventions before the common assumptions; add the "A run" paragraph; mark the recalled
  parts so that §2 shrinks to one page once D1 precedes it in the paper.
- **Appendices:** A Notation, plus the assumptions table. B Conventions in full. A new short appendix for the explicit
  constants (flag 10). C Status ledger (internal).
- **The Overview should contain** (no symbols beyond $n$, $p$ and the rate):
  1. three sentences of setting;
  2. the four questions, each with its answer in words and its theorem numbers, the main theorem singled out;
  3. Table 1, "Results at a glance": result, one sentence, design (fixed, Gaussian rows, i.i.d.), rate, where stated,
     status (the status column under the `\showstatus` toggle);
  4. a small diagram of which result rests on which (3.1 → random design → main theorem and reported estimates; start
     law → reported estimates; distribution separate), and the theorem-by-assumption grid;
  5. "How to read a result": the block layout, where the assumption table is, what "the method" means, and where the
     proofs are (a reader will ask);
  6. the paragraph on what "asymptotic" means and the shape of the posterior at moderate $n$;
  7. a correspondence table with Song and Liang (2015): our theorem, their theorem, the remark that compares them. The
     table points only; it adds no comparative claim.
- **Song–Liang comparisons: per-theorem, as planned, not one section.** The question arises at each theorem, and the
  checked sentences stay next to what they compare. One length rule: up to about 120 words it is a remark; longer (the
  comparison for the distribution theorem) it is a titled subsection at the end of its section, keeping its
  stronger / weaker / different / overall structure.

## E. Where an example or a figure helps most

1. **Figure for Remark 3.4 (the posterior at moderate $n$), placed in the Overview or §3.1.** Stacked bars of posterior
   mass for one design at four sample sizes (for instance $n=100,400,1600,6400$, fixed $p$): the true model, the models
   with one extra null predictor, everything else. One exact computation on an orthogonal design is enough. It shows what
   the rate $\sqrt{\log n/n}$ looks like and removes the apparent conflict between "consistent" and "not a point mass
   at moderate $n$", which is the first thing a referee will ask. The numbers must come from Theory or Engineering.
2. **Worked example and schematic before the main theorem (§5.2): visibility and leakage.** These are the hardest
   conditions in the paper. (a) A two-predictor example with unit variances and correlation $\rho$: for
   $\theta^*=(1,-1)$, $\operatorname{Cov}(W_1,W^\top\theta^*)=1-\rho$, so the first true predictor becomes invisible as
   $\rho\to1$ (masking); add one null predictor correlated with a true one to show a leak. (b) A schematic of the nested
   sets $S_0\subseteq\tilde S_0\subseteq Q$, with the local search deleting one spurious member per move until it
   reaches $S_0$. It explains the mechanism of the main theorem in one picture. Theory should check the arithmetic.

## Summary: top five recommendations

(1) Replace the 35 global labels by a two-tier scheme: 13 named assumptions and three "Conventions" for conditions used
by several theorems, numbered local Assumptions with lettered items for the rest, and one table in Appendix A.
(2) Reorder every theorem block as lead-in, in words, new assumptions, theorem, status, remarks, with fixed remark
titles; split the seven-item Remark 3.3 into "Further consequences" and "On the assumptions". (3) Settle the symbol
system now in `smcbvs.sty`: remove the collisions of C2 (above all $c$/$C$, $J$, $\varpi$, $b_0$, $Q$), delete the
unused $r_n$ and $\delta_n$, and give every assumption constant its own name. (4) Rewrite §2.5–§2.7 for a reader who
has not seen the software: add an "A run" paragraph, state the three conventions in plain sentences, take the
conclusion out of (DC), and put the asymptotic conventions before the assumptions. (5) Before the full draft, clear the
content flags of C3 with Theory and HQ, first of all flags 1–7 (the dimension of $X^{\mathrm r}$, the scale on which
signals are fixed, the §3 summary sentence, and the scope of the Theorem 3.1 status note), and commission the
moderate-$n$ figure of E.
