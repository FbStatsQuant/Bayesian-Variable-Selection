# STYLE_R1: advisor report on D2 (§2 and §3.1), round 1 (2026-11-16)

Read: the standards, `what_we_prove.tex` and its PDF, `smcbvs.sty`, the reader versions of Theorems 1–10, the claims
card, the source notation file, the status ledger. Findings only. Nothing here changes a statement or a status;
possible content issues are flags (C3).

## A. Style sheet (D2 and D1)

**Voice.**
- "We" + present tense for what the paper does. "The method" + present tense for what the software does. Theorem
  statements are impersonal.
- One claim per sentence, about 30 words at most. One idea per paragraph. No sentence starts with a symbol.
- British spelling. "With probability tending to one" in words.
- One word per concept: *predictor* ("column" only for a matrix); *model* = a set of predictors; *true model*, *true
  predictor*, *null predictor* (not "the truth", "nulls"); *over-fitted model* = strict superset of $S_0$; *run*;
  *reported* (not "printed").
- Not in running text: shipped, printed, branch, ladder, covered configuration. "As coded" stays in the D1 title and in
  the one sentence that defines "the method".
- Section summaries are the first paragraph, in roman type. Italic marks a term at its definition, nothing else.

**Theorem block, in this order.**
1. *Lead-in:* one or two sentences on the question the result answers.
2. *In words:* at most four sentences; only $n$, $p$ and the rate as symbols; conditions named in the order of the
   formal list. It comes **before** the assumptions, so the reader knows what they are for.
3. *New assumptions only:* label, name, one-sentence statement, then "Rules out:" in normal size. Nothing else.
4. *Theorem [name]:* setting; "Assume …" in the order model, signal, design, search, conventions; "Then" and numbered
   displays. No commentary.
5. *Status note:* outside, `\status`, the three fixed phrases only; one line per display if parts differ.
6. *Remarks:* fixed titles in fixed order: Further consequences; On the assumptions; What is not claimed; At moderate
   $n$; Comparison with Song and Liang (2015). At most three items each, with italic run-in heads.

**Displays and constants.**
- Number a display if it is cited, and every theorem conclusion. A sentence in words sits next to each display.
- One statement per line; nothing wider than the text (display (10) is 58pt overfull: use two aligned lines).
- Write the rate out, $\sqrt{\log n/n}$. `:=` for definitions; $\max_{j\in[p]}$ for index ranges.
- "Fixed" means "does not depend on $n$". A constant introduced in an assumption has its own letter or subscript,
  never bare $c$ or $C$. Generic $C$, $c$ only in prose. A constant shared by two displays is numbered ($C_1$).
- Name the size class before the bound: "sets of bounded size", "sets of logarithmic size".

## B. Assumption labels: decision

**Neither 35 global mnemonics nor grouped numbering. Use two tiers.**

- *Against 35 mnemonics:* 22 of them serve one theorem only. No reader holds (FF), (VF), (BL), (LQ), (EK), (FC), (SB),
  (GM), and a two-letter code does not say where it is defined.
- *Against (P1)–(P5), (S1)–…:* numbers carry no meaning, so remarks that compare conditions become unreadable.
- *Rule:* a condition used by **two or more theorems** gets a global mnemonic name, stated once at first use. A
  condition used by **one theorem** is an item of that theorem's own numbered Assumption (same counter as theorems),
  cited as "Assumption 5.3(b)". Twins share a label; a subscript names the scale or the population.
- *Conventions are not assumptions:* the computational ones become "Convention (C1)–(C3)", so the reader sees which
  hypotheses are statistical. (MC) must go in any case: here it reads as "Monte Carlo".
- *One table:* "Assumptions at a glance" in Appendix A (label, in words, where stated, used by).

| Family | Global label (13 + 3) | Replaces | Used by (reader numbering) |
|---|---|---|---|
| Model | (GL) Gaussian linear model | (GL) | 1, 1′, 2, 3(b), 5–8, 10 |
| | (DIM) Dimension | (DIM), minus "$n\to\infty$" | 1, 1′, 2, 5–7, 10 |
| | (GR) Gaussian rows | (GR) | 2, 5, 6, 10 |
| Signal | (SP) Sparsity | (SP) | 1, 1′, 2, 5–7, 10 |
| | (BC) Bounded coefficients | (BC) | 1, 1′, 7 |
| | (BM) Beta-min, forms (a), (b) | (BM) | 1, 7 |
| | (FS$_\beta$) Fixed signals, raw scale | (FS) | 2 |
| | (FS$_\theta$) Fixed signals, standardised scale | (FT) | 5, 6, 10 |
| Design | (EF) Eigenvalue floor, sets of bounded size | (SE), which reads "standard error" | 1, 7 |
| | (NC) No near-exact collinearity | (NC) | 1, 1′, 7 |
| | (EF$_\Sigma$) Population eigenvalue floor | (PE) | 2, 6, 10 |
| Search | (V) Visibility; (NL) No leakage | (V); (NL) | 5, 6, 10; 5, 10 |
| Conventions | (C1) Method; (C2), (C2$^+$) Delivery; (C3) Sampler | (MC); (DC), (DC$^+$); (SC) | 5–8, 10; 6, 7; 10 |

Local Assumptions, one per theorem, items lettered:
- Thm 1′: (a) floor on the true model; (b) identifiability margin. Replaces (ID).
- Thm 4: (a) candidate model; (b) floor; (c) signal relative to residual variance. Replaces (CM), (CF), (CS).
- Thm 9: (a) i.i.d. rows and Gaussian linear model; (b) sparsity and dimension; (c) sub-Gaussian predictors; (d) no
  near-exact collinearity; (e) bounded signal. Thm 9B: detectable signal. Replaces (IID), (SD), (SG), (NE), (BS), (DS).
- Thm 5: small-set floor; "uncorrelated nulls" is stated inline in the theorem. Replaces (SF), (UN).
- Thm 6: (a) polynomial leakage set; (b) local regressions; (c) floor on $Q\cup\{l\}$. Replaces (PL), (LR).
- Thm 7: (a) floors; (b) visibility; (c) bounded leakage; (d) size of the leakage set. Replaces (FF), (VF), (BL), (LQ).
- Thm 8: (a) eigenvalue floor; (b) fixed signal bounds; (c) size budget. Thm 8′: gain margin inline. Replaces (EK),
  (FC), (SB), (GM).

Notes. Local labels suit Theorem 9 well: its model differs from (GL) and (DIM) ($p_{\mathrm{raw}}\le n^A$; $\sigma_*$ may
vary with $n$), and a shared label would hide that. I considered one parametrised floor EF$(k,\varphi)$ for all
eigenvalue conditions and do not recommend it now: the scales differ ($\varphi_0^2$, $\kappa$, $c_\psi/n$), and each
instance would need a new check against its source.

## C. Line-level findings, §2 and §3.1

### C1. Wording and order

| # | Where (quoted) | Problem | Proposed wording |
|---|---|---|---|
| 1 | §2 Notation: "$I_n$ is the …" | Sentences start with symbols. The asymptotic symbols sit in §2.7; the assignment wants one Notation paragraph. | Start with words. Add: "A star marks a true parameter value; the true model and its size are $S_0$, $s_0$. $I$ is an identity matrix whose size is clear from the context." |
| 2 | §2.1: "$y^{\mathrm r}$"; bullet 2, "a generic population row" | Superscript r unexplained. "Model", "null predictor" and the subscript in $\Sigma_n$ never defined. Four ideas in one bullet. | "(the superscript r marks raw data)". "A *model* is a set $S\subseteq[p]$ of predictors; predictors outside $S_0$ are *null predictors*." "We write $W\sim\mathrm N_p(0,\Sigma_n)$ for a centred copy of one row. The subscript $n$ recalls that this law may change with $n$." |
| 3 | §2.1: "A law for the rows is … not a choice of a particular family of designs." | Answers a debate the reader has not seen. | "No theorem assumes a particular correlation structure, such as equicorrelation. Such structures appear only as examples." |
| 4 | §2.2: "On this scale the true coefficients and the mean signal are" | $y$ is rescaled, $\theta^*$ is not; "this scale" is unclear. | "In terms of the standardised predictors, the centred response is $P^\perp_{\mathbf 1}y^{\mathrm r}=X\theta^*+P^\perp_{\mathbf 1}\varepsilon$, with $\theta^*:=D\beta^*$. So $\theta^*$ is in the units of the raw response." Add "(divisor $n-1$)" to "sample standard deviations". |
| 5 | §2.3: "each predictor enters the model independently with the same probability $q$" | Independent only given $q$. | "A probability $q$ is drawn from $\mathrm{Beta}(1,p)$. Given $q$, each predictor enters independently with probability $q$." |
| 6 | Example 2.1: "The probabilities add up to one, so here the cap does not bind." | Logic backwards. | "Here $K=p$, so no model is excluded, and the weights already add up to one." (The example belongs to D1; D2 keeps a pointer.) |
| 7 | §2.3: "Given a model $S$ and the noise variance $\sigma^2$ …" | Priors precede the likelihood that introduces $\sigma^2$. $\beta_S$ lives on the standardised scale, where the truth is called $\theta^*$. IG: shape or rate? | Likelihood first: "The method fits the working model $y\mid S,\theta_S,\sigma^2\sim\mathrm N_n(X_S\theta_S,\sigma^2I_n)$ to the standardised data. Here $\theta_S$ and $\sigma^2$ are working parameters, not the true values." Then the priors; "shape $a_0$, scale $b_0$". |
| 8 | §2.4: "charges about $(n+1)^{1/2}$ for each predictor" | Direction ambiguous. | "a penalty for model size (an Occam factor): in a well-conditioned model each extra predictor multiplies $m(S)$ by about $(n+1)^{-1/2}$". |
| 9 | §2.4: "Two elementary facts link them."; "within $\delta_n$ of the truth" | Every theorem uses these facts; they have no number. | Make them Lemma 2.x: "… within $1-\pi(S_0\mid y)$ of its ideal value, 1 for a true predictor and 0 for a null one." Name $Z$ at (7). |
| 10 | §2.5 summary: "a deterministic start, an internal calibration" | Contradicts a start law that is sampled. Run, seed, calibration, admissible, enumeration are used in §2.6 and never defined. | Open §2.5 with a paragraph "A run": one sentence each on run, seed, calibration, the enumeration case and "produces output". |
| 11 | §2.5 Local search: the 30-word parenthesis | Definition buried; "or after at most". | "Two models are neighbours if one comes from the other by deleting one predictor, adding one (while the size is below $K$), or swapping one member for one non-member. From the start mode, the method scans all neighbours of the current model and moves to the best one if its log score is strictly higher. It stops at the first scan with no improvement, or after $\ell_n+\lvert\tilde S_0\rvert$ moves, whichever comes first." |
| 12 | §2.5: "The method *certifies* $\hat S$ … when either the model space was small enough …" | 60 words, two cases, past tense. | "The method certifies $\hat S$ in two cases. (a) It enumerated $\Omega$; then $\hat S$ maximises $F$ over $\Omega$. (b) $\hat S$ ends a local search whose last scan found no improvement; then no neighbour of $\hat S$ has a higher log score." |
| 13 | (DIM): "$n\to\infty$ and … are allowed and are the main case"; §2.7: "Constants written with Greek or Latin letters …", "$s_0$ is fixed unless …", "$r_n:=$" | $n\to\infty$ is not a condition "at that $n$". $\gg$ and "fixed" are used before §2.7. In §2.7 the first phrase is vacuous, the second duplicates (SP), and $r_n$ is never used. | "(DIM) $2\le p\le n^A$ for a fixed $A\ge1$. *Rules out:* $p$ growing faster than every power of $n$, such as $p=e^{n^{a}}$. The case $p\gg n$ is allowed." §2.7 moves before §2.6 and says: "A quantity is *fixed* if it does not depend on $n$. Every constant introduced in an assumption is fixed." |
| 14 | (DC): "An idealised machine, the covered configuration, ideal random numbers, and a declared memory and time allocation at least the method's polynomial envelopes" | A fragment with four undefined terms. Same in (SC): "realise their stated kernels". | "Convention (C2) (Delivery). The computer does exact arithmetic and never overflows or fails. The method runs in its default configuration, with ideal random numbers. The user grants at least the memory and time that the method's own requirement formulas, polynomial in $(n,p_{\mathrm{raw}})$, ask for. Appendix B gives the full list." |
| 15 | (BC): "could drift off scale" | Needs a second read. | "*Rules out:* true coefficients that grow with $n$. The signal energy $\lVert X\theta^*\rVert^2$ then stays of order $n$, like the noise energy." |
| 16 | (NC): "$O(\log n)$" in the title; "$X_S^\top X_S$"; "so it vanishes as $n$ grows" | $G_S$ exists for this. The last sentence is not a "rules out". "The vanishing floor" is later used as a name, never introduced. | $\lambda_{\min}(G_S)\ge g_0$. "*Rules out:* exact, or nearly exact, linear dependence among $O(\log n)$ predictors; duplicated predictors, for instance." Then, outside: "For correlation matrices (NC) reads $\lambda_{\min}(\hat R_S)\ge g_0/(n-1)$, a floor that vanishes as $n$ grows. We call (NC) the *vanishing floor*." |
| 17 | In words, Thm 3.1: "uniformly over all such designs"; "within $O_P(\cdot)$ of 0 or 1" | Second read; "0 or 1" loses the side. | "Then, on average over the noise, the posterior mass outside the true model is at most a constant times $\sqrt{\log n/n}$. The constant is the same for every design that meets the conditions. … Every inclusion probability is within order $\sqrt{\log n/n}$ of 1 for a true predictor and of 0 for a null one." |
| 18 | "drops the eigenvalue floor away from the true model" | Second read. | "The next result asks for an eigenvalue floor on the true model only, and for no beta-min condition. In exchange it asks for an identifiability margin: every small model that misses a true predictor must leave part of the signal unexplained. The vanishing floor (NC) is kept." |
| 19 | (ID): one 55-word sentence; "Floor on the truth"; In words, Thm 3.2: "of order $\log n$" | Two conditions and three restrictions on $S$ at once. $\mu$ exists for this. "Of order" hides a lower bound. | "(a) *Floor on the true model.* …  (b) *Margin.* Every model $S\in\Omega$ that misses a true predictor and has at most $j_0$ predictors outside $S_0$ leaves unexplained signal $\lVert(I-P_S)\mu\rVert^2\ge c_{\mathrm{id}}\,\sigma_*^2\log n$." In words: "at least a constant times $\sigma_*^2\log n$", in three sentences. |
| 20 | Remark 3.3, items (i)–(vii) | Seven items, three subjects; (i), (ii), (v) are consequences. The determinant condition is unreadable inline. | Split into "Further consequences" (i, ii, v) and "On the assumptions" (iii, iv, vi, vii). Display the condition. (i): "inclusion probabilities of true predictors are close to one, those of null predictors close to zero, uniformly in $j$". (iii): replace "the two theorems coexist" by which theorem applies in that range. |
| 21 | Remark 3.4: "times a $\chi^2_1$ factor"; "a mixture over" | Form of the factor unclear. | "… of order $n^{-1/2}/p$, times a random factor [exact form from Theory]"; "the posterior is spread over $S_0$ and many models with one extra null predictor". |

### C2. Symbols (fix once in `smcbvs.sty`, before more text is written)

- *Collisions inside §2–§3.1.* $c$: generic (§2.7), the margin constant in (ID), a third use in Remark 3.3(ii). $C$:
  "changes from line to line", yet (10) reuses the $C$ of (9). $J$: number of blocks in (8), a set in Remark 3.3(vi).
  $m$: integer in $[m]$, mean $m_n$, marginal likelihood $m(S)$. $R$: number of islands, and $\hat R_S$.
- *Defined, not used in §3.1:* $r_n$, $\delta_n$, $\mu$. Delete $r_n$. Keep the term "posterior miss", write
  $1-\pi(S_0\mid y)$, drop $\delta_n$. Use $\mu$ in (ID).
- *Collisions ahead (Theorems 2–10).* $\varpi$ (prior) and $\varpi_n$ (leak bound); the prior needs no symbol, since
  only $w$ is used after (4). $b_0$: inverse-gamma scale and signal floor (certified screening). $Q_S$ and the leakage
  set $Q$. $\nu$ and $\nu_n$. $H_S$, the sets $H_l$, Hellinger $H$. $D$ and $D_n$. $z_S$ and $z_j$. $M$ (four meanings).
  Optional: $\tilde S_0$ differs from $S_0$ by a tilde only.

### C3. Flags for the manager (possible content or status issues; not rewritten)

1. **Dimension of $X^{\mathrm r}$:** $n\times p_{\mathrm{raw}}$ in §2.1, but its rows are $\mathrm N_p$, $D$ is $p\times p$,
   $S_0\subseteq[p]$. What happens to a removed predictor in model (1)? The source notation has the same gap.
2. **"We may and do take $\Sigma_n$ to be a correlation matrix."** The reader versions state it as a hypothesis. As a
   reduction it rescales $\beta^*$, which matters for a condition on raw coefficients.
3. **Signals fixed on the standardised scale.** Theorems 5, 6, 10 take $\theta^*$ deterministic, so $\beta^*$ in (1)
   depends on the design. (GL) as worded does not clearly cover this; the end of §2.2 ¶2 hides it.
4. **§2.6, "Two assumptions are used by every theorem."** Not so: sharpness part (a) uses neither, certified screening
   does not need (DIM), and the omitted-variables and distribution theorems have their own model.
5. **(DC) contains a conclusion** ("Under (DC), a run produces output on …"). It belongs to the delivery theorems.
6. **§3 opening summary.** "Cannot be improved in general" reads as "on every design"; the source claims sharpness on
   the witness designs only. "The same holds when the fitted predictors omit some": the omitted-variables target is
   the support of the best candidate predictor, not the true model.
7. **Status note of Theorem 3.1.** Display (10) contains $1-4C\sqrt{\log n/n}$ with the $C$ of the conditional bound
   (9). "(10): proved and independently checked" may hold only for "$\to1$" and the $O_P$ part.
8. **Remark 3.3 (ii), (v), (vi)** assert bounds with no stated hypotheses or status. (v) drops the source's "uses a
   coefficient bound instead". "(numerical counterexample)" has no pointer. Is "specificity", not "sensitivity",
   meant in (ii)? $c_D$ is undefined.
9. **(ID), "it does not restrict correlations among the other predictors"** is stronger than the source wording ("no
   eigenvalue condition off $S_0$ beyond the vanishing floor").
10. **$c_0$, $c_1$** are called explicit but not given. The source asks for "a sufficiently large constant" in the
    statement and the formulas in an appendix; none is planned.
11. **$m(S)$ is defined up to a constant,** so $Z$, and later "unbiased for $Z$", need the normalisation fixed.
12. **"Produces output" and "completes"** (Theorem 10, Corollary 9C): one event or two? Also "local searches"
    (plural) in §2.5, where one search is described.
13. **Theorem 3.2, "the conclusions of Theorem 3.1 hold":** cite (9) and (10), and say whether "for every $n\ge n_0$
    and every design" carries over.
14. **$4C$.** Lemma 2.x plus Markov's inequality gives $2C$. The statement is correct, but a reader will ask.
15. **(SP) also excludes $s_0=0$.** Say so, or say where the empty true model is covered.
16. **Verbatim Song–Liang text** is in card shorthand. Ask HQ whether the same claims may be put in full sentences.

## D. Structure

- **Section order: keep it.** It follows the abstract's four questions. Three changes inside it:
  1. §4 has its own setting (i.i.d. pairs, $p_{\mathrm{raw}}$, level, window): open it with "Setting for this section".
  2. §5 keeps the build-up order, but its first paragraph states the main theorem in words, since it arrives late.
  3. Pooled-evidence unbiasedness is planned in §5.4 and in §6. State it once (§5.4) and cite it. §6 has no theorem:
     half a page, titled "The parallel method: what is and is not proved".
- **§2:** asymptotic conventions before the assumptions; add "A run"; mark the recalled parts, so that §2 shrinks once
  D1 precedes it.
- **Appendices:** A Notation and the assumptions table; B Conventions in full; a new one for the explicit constants
  (flag 10); C Status ledger.
- **Overview contents** (no symbols beyond $n$, $p$, the rate):
  1. three sentences of setting;
  2. the four questions, each with its answer in words and theorem numbers; the main theorem singled out;
  3. Table 1, results at a glance: result, one sentence, design, rate, where stated, status (under the toggle);
  4. a small diagram of which result rests on which, and a theorem-by-assumption grid;
  5. "How to read a result": the block layout, where the assumptions table is, what "the method" means, where the
     proofs are;
  6. what "asymptotic" means, and the posterior at moderate $n$;
  7. a correspondence table with Song and Liang (2015): our theorem, their theorem, the remark that compares them. It
     points only and adds no comparative claim.
- **Song–Liang comparisons: per theorem, as planned, not one section.** The question arises at each theorem, and the
  checked sentences stay next to what they compare. Length rule: up to about 120 words, a remark; longer (the
  distribution theorem), a titled subsection at the end of its section, with its stronger / weaker / different /
  overall structure.

## E. Where an example or a figure helps most

1. **Figure for Remark 3.4, the posterior at moderate $n$** (Overview or §3.1). Stacked bars of posterior mass for one
   design at four sample sizes and fixed $p$: the true model, the models with one extra null predictor, the rest. One
   exact computation on an orthogonal design is enough. It shows what the rate looks like and removes the apparent
   conflict between "consistent" and "not a point mass at moderate $n$", which a referee will ask about first. The
   numbers must come from Theory or Engineering.
2. **Example and schematic before the main theorem (§5.2): visibility and leakage,** the hardest conditions in the
   paper. (a) Two true predictors with correlation $\rho$ and $\theta^*=(1,-1)$: $\operatorname{Cov}(W_1,W^\top\theta^*)=1-\rho$,
   so a true predictor becomes invisible as $\rho\to1$; add one null predictor correlated with a true one to show a
   leak. (b) A schematic of $S_0\subseteq\tilde S_0\subseteq Q$, with the local search deleting one spurious member per
   move down to $S_0$. Theory should check the arithmetic.

## Summary: top five recommendations

(1) Replace the 35 global labels by two tiers: 13 named assumptions and three Conventions for conditions shared by
several theorems, numbered local Assumptions with lettered items for the rest, and one table in Appendix A.
(2) Order every theorem block as lead-in, in words, new assumptions, theorem, status, remarks with fixed titles, and
split the seven-item Remark 3.3. (3) Settle the symbols now in `smcbvs.sty`: remove the collisions of C2 (first $c$/$C$,
$J$, $\varpi$, $b_0$, $Q$), delete the unused $r_n$ and $\delta_n$, and name every assumption constant. (4) Rewrite
§2.5–§2.7 for a reader who has not seen the software: an "A run" paragraph, the conventions in plain sentences, the
conclusion taken out of (DC), the asymptotic conventions before the assumptions. (5) Before the full draft, clear the
flags of C3 with Theory and HQ, starting with 1–7 (the dimension of $X^{\mathrm r}$, the scale on which signals are
fixed, the §3 summary, the scope of the Theorem 3.1 status note), and commission the moderate-$n$ figure.
