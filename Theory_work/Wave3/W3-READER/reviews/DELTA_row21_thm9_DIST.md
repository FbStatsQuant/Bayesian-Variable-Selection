# DELTA — card row 2.1 / READER_VERSIONS row thm9 (W3-DIST) — v-next (v0.4), PROPOSAL, not applied (H5 card 13 AGREED)

Written 2026-11-16 by the W3-READER lead for the manager / HQ. Nothing here is applied to `READER_VERSIONS.md` or
`CLAIMS_CARD.md`. Two applicable patches, one per status variant (both pass `git apply --check` on theory/W3-READER HEAD):
- `reviews/DELTA_row21_thm9_DIST_A.diff`: task T discharges SOP:TH09 (T01 part);
- `reviews/DELTA_row21_thm9_DIST_B.diff`: it does not; statuses read "PROVED-CHECKED, conditional on SOP:TH09 (T01 part)".
The earlier single `DELTA_row21_thm9_DIST.diff` (v0.3) is superseded and removed.

**Source (read only):** `/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/` at main —
`STATEMENT.md` v1.4.10 (§0 :17-70, §1 :72-112, §1R :126-269, bridges :384-417), `CHECKPOINT_3.md` (§2, §5), `TARGET.md` §2,
§6, `REPORT.md` :11-17, `reviews/UNHARVESTED_STRENGTH.md` item 9. Council R2 PASSED, MANIFEST
c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc (astra 9.3, opus 9.2). Song & Liang (2015):
`Papers/Core_bibliography/32_2015_Song_Liang_….pdf`, checked sentence by sentence in `reviews/SL_PDF_CHECK.md` (helper Opus
5.5, high, Claude Third; journal pages).

## 0. HQ's binding edits (H5 card 13) and how each is met
1. **The analogue is display (i) only.** Comparison opens with "The analogue is display (i)"; display (iii) is listed
   separately as "Not the analogue", carrying the $\sqrt{\log(p_{\mathrm{raw}}ee n)}$ factor and the as-proved cubic
   sparsity bound (RT1; UNHARVESTED item 9). For (i): radius constant free of $s$ and level at most linear in $s$, stated
   in DIST-1's interface form (STATEMENT :84-87, TC3; UNHARVESTED item 9), **with one precision**: in the reader form the
   (A5)-implied energy and coefficient-cost bounds grow with $s$ (bridge B1 :391-395: $2s^2ar b^2$, $2sar b^2$). The text
   says so, so the claim is not read as holding for the reader constants.
2. **Weaker list, "s fixed".** Added, but **the PDF contradicts the brief's "where Song–Liang's s may grow"** (SL_PDF_CHECK
   S9, MISMATCH). Their Theorem 2 (strict sparsity, their (4), p. 950) also has a true model of bounded size. Only their
   Theorem 1 (approximate sparsity (3), predictors bounded by 1) lets the number of nonzero coefficients grow. The text
   states exactly that.
3. **Every Song–Liang sentence checked against the paper.** `reviews/SL_PDF_CHECK.md` gives verbatim quotes with page and
   equation numbers. Corrections taken into the text:
   - (15) is Theorem 1's display; Theorem 2 has the same form, unnumbered (S2).
   - The prior family is described as in the paper (S3).
   - Theorem 2's rate condition at polynomial $p$ is $ar r_n\log n=o(narepsilon_n^2)$, plus their (14) (S4).
   - Corollary 1 is quoted as printed: $arepsilon_n=O\{n^{-(1-lpha)/2}\log^{k/2}n\}$, p. 954, no equation number (S5).
   - The eigenvalue conditions in their (11) and (14) are on the prior covariance, not the design (S10).
   - Their lower growth bound on $p$, $P_n\succ n^	heta$, is cited (S6).
4. **What is estimated.** A new paragraph "What is estimated" (the conditional law of $y$; sample-mean intercept; law of $x$
   not estimated; the averaged-conditional form of $d_H^2$, STATEMENT :42-52). "Recovers the joint distribution" is
   replaced in the section title, the card row and the in-words sentence.
5. **Order and placement.** The fixed-level display (i) comes first, then the level-M form with (ii); then (iii), 9B and 9C.
   New block "Placements": abstract = display (i) only (clause drafted); the rest in the body.
6. **Row 2.2** stays a body remark (§3, F9 text unchanged).
**Status:** two variants, A and B (§1 and §2 master block); requote from `claims.tsv` at application.

**Flags outside this row (SL_PDF_CHECK; not changed here):**
- S12, **card row 1.4** (applied at v1.1 from the W3-MISR-R delta): "in their omitted-Gaussian-predictor setting, where the
  candidate-only conditional model is correctly specified" does not match the paper. Their Theorem 4 / Corollary 2 setting
  assumes only second moments of the candidates, never Gaussian omitted predictors, and calls the model misspecified
  ("f* ∉ P_s", p. 956-957). The proposed fix needs HQ / MISR-R.
- S13, **card row 1.1**: the $e^{Cn^lpha}$ dimension range comes from their (10) and Corollary 1, not their Theorem 3
  (sure screening only). A wording point for row 1.1's "Narrower in dimension".

## 1. Card row 2.1 (two status variants) and the abstract-list line
**Variant A** (task T discharges SOP:TH09, T01 part):

| 2.1 (Thm 9) | **The posterior recovers the conditional law of $y$ given $x$, in Hellinger distance averaged over $x$ (Song–Liang's joint distance)** [H5-13]. The law of $x$ is not estimated; the fitted conditional law uses the sample-mean intercept. Rows i.i.d.; Gaussian linear model, any noise level; at most $s$ nonzero coefficients, at most $n^A$ predictors; bounded signal per predictor; sub-Gaussian predictors on sparse directions and no near-exact collinearity (smallest correlation eigenvalue $\ge c_\psi/n$), both on sets of at most $q_n(M)=\min\{p_{\mathrm{raw}},\lceil C_qM\log n\rceil\}$ predictors. **Abstract (display (i); fixed level $M\ge M_0$, all large $n$):** except on data sets of probability $\le n^{-cM}$, the posterior puts mass $\le n^{-cM}$ on conditional laws farther than $\sqrt{M\log n/n}$ from the true one. No beta-min and no fixed lower bound on eigenvalues. *Body:* the same for every level $M_0\le M\le\sqrt n/\log n$, with posterior model size $\le s+C_1M$; without the collinearity condition (sub-Gaussianity for single predictors only), radius larger by $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$ and size bound $s+C_1M\log n$; rate $M_n/\sqrt n$ under a fixed eigenvalue floor and detectable signals (Thm 9B); every completed sampler run whose returned list carries posterior mass $\ge n^{-cM/2}$: the posterior restricted to the list puts mass $\le n^{-cM/2}$ outside the same radius (Cor 9C; exact arithmetic). | `W3-DIST:Thm-A`: "PROVED-CHECKED"; `W3-DIST:Thm-B`: "PROVED-CHECKED, conditional on W3-POST:Thm-1"; `W3-DIST:Cor-C`: "PROVED-CHECKED" (exact arithmetic a stated premise); DIST-C delivery statements (not used by Cor 9C): "PROVED-CHECKED, conditional on W3-SAMP:D, W3-SAMP:PC, W3-SAMP:LT#, W3-SAMP:C, W3-SAMP:TR". W3-DIST council R2 (MANIFEST c5cd9cdd…); H5 card 13. Requote from `claims.tsv` at application. | Song–Liang (2015) Theorems 1–2 analogue (display (i)): same distance and the exponential form of their (15); radius a constant times $\sqrt{\log n/n}$ with the prior as coded and no tuning; plus a parametric rate and the sampler's output, which they do not treat. Narrower: at most $n^A$ predictors, exact sparsity with $s$ fixed, and a design condition (no near-exact collinearity) their Theorems 1–2 do not need. Overall incomparable (checked against the paper: `reviews/SL_PDF_CHECK.md`). | **clean**; bridges identity / EXISTS + B9.5 (VERIFIED) |

**Variant B** (it does not):

| 2.1 (Thm 9) | **The posterior recovers the conditional law of $y$ given $x$, in Hellinger distance averaged over $x$ (Song–Liang's joint distance)** [H5-13]. The law of $x$ is not estimated; the fitted conditional law uses the sample-mean intercept. Rows i.i.d.; Gaussian linear model, any noise level; at most $s$ nonzero coefficients, at most $n^A$ predictors; bounded signal per predictor; sub-Gaussian predictors on sparse directions and no near-exact collinearity (smallest correlation eigenvalue $\ge c_\psi/n$), both on sets of at most $q_n(M)=\min\{p_{\mathrm{raw}},\lceil C_qM\log n\rceil\}$ predictors. **Abstract (display (i); fixed level $M\ge M_0$, all large $n$):** except on data sets of probability $\le n^{-cM}$, the posterior puts mass $\le n^{-cM}$ on conditional laws farther than $\sqrt{M\log n/n}$ from the true one. No beta-min and no fixed lower bound on eigenvalues. *Body:* the same for every level $M_0\le M\le\sqrt n/\log n$, with posterior model size $\le s+C_1M$; without the collinearity condition (sub-Gaussianity for single predictors only), radius larger by $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$ and size bound $s+C_1M\log n$; rate $M_n/\sqrt n$ under a fixed eigenvalue floor and detectable signals (Thm 9B); every completed sampler run whose returned list carries posterior mass $\ge n^{-cM/2}$: the posterior restricted to the list puts mass $\le n^{-cM/2}$ outside the same radius (Cor 9C; exact arithmetic). | `W3-DIST:Thm-A`: "PROVED-CHECKED, conditional on SOP:TH09 (T01 part)"; `W3-DIST:Thm-B`: "PROVED-CHECKED, conditional on W3-POST:Thm-1, SOP:TH09 (T01 part)"; `W3-DIST:Cor-C`: "PROVED-CHECKED, conditional on SOP:TH09 (T01 part)" (exact arithmetic a stated premise); DIST-C delivery statements (not used by Cor 9C): "PROVED-CHECKED, conditional on SOP:TH09 (T01 part), W3-SAMP:D, W3-SAMP:PC, W3-SAMP:LT#, W3-SAMP:C, W3-SAMP:TR". W3-DIST council R2 (MANIFEST c5cd9cdd…); H5 card 13. Requote from `claims.tsv` at application. | Song–Liang (2015) Theorems 1–2 analogue (display (i)): same distance and the exponential form of their (15); radius a constant times $\sqrt{\log n/n}$ with the prior as coded and no tuning; plus a parametric rate and the sampler's output, which they do not treat. Narrower: at most $n^A$ predictors, exact sparsity with $s$ fixed, and a design condition (no near-exact collinearity) their Theorems 1–2 do not need. Overall incomparable (checked against the paper: `reviews/SL_PDF_CHECK.md`). | **clean**; bridges identity / EXISTS + B9.5 (VERIFIED) |

- **2.1** abstract: display (i) only, at a fixed level (row thm9 "Placements"); level-M form, 9B, 9C in the body; **2.2** body remark [H5-13].

## 2. Row thm9 — proposed reader text (v0.4; shown with variant B; variant A replaces the master-status bullets by the block below)
Interpretive sentences (D71), each a claim with a source:
- "the posterior contracts at the rate $\sqrt{\log n/n}$" — display (i), fixed $M$.
- "What is estimated" — STATEMENT :42-52.
- "(ii) … does not say that they are the true ones" — STATEMENT :196.
- Song–Liang items — SL_PDF_CHECK (pages, equations); the sparsity sentences — B9.8.
- Why-lines — TARGET §6, shortened.

````markdown
## 9. Theorem 9 — The posterior recovers the conditional law of the response, in Song–Liang's distance
<!-- ROW thm9 BEGIN -->
**Card row** 2.1 · **Section version** 0.4 (proposal, 2026-11-16) · **Pending delta** —


### Setting and notation
The data are $n$ independent copies $(x_i,y_i)$, $i=1,\dots,n$, of a pair $(x,y)$: $x\in\mathbb R^{p_{\mathrm{raw}}}$ is the
vector of all observed predictors (a row of $X^{\mathrm r}$, §1 of the notation) and $y\in\mathbb R$ the response (an entry of
$y^{\mathrm r}$). $D_n$ denotes the data set. $p_{\mathrm{raw}}$ may grow with $n$ and may be much larger than $n$; the law of
$(x,y)$ may change with $n$. As in every theorem, $p\le p_{\mathrm{raw}}$ is the number of predictors not constant in the
sample, and the method runs on these (standardisation §2, prior $\mathrm{BB}(1,p)$ capped at $\min(p,\lfloor n/2\rfloor)$, slab
and inverse-gamma prior §3; no tuning). $\Pi(\cdot\mid D_n)$ is the resulting exact posterior of $(S,\beta,\sigma^2)$, mapped
back to the original units: $S$ is the set of included predictors, $\beta\in\mathbb R^{p_{\mathrm{raw}}}$ the coefficient vector
(zero outside $S$ and on removed predictors), $\sigma^2$ the noise variance. If fewer than two predictors remain, or the
response is constant in the sample, the posterior is not defined; under the assumptions below such data sets have
probability smaller than the exceptional probabilities in the theorems and are counted in them (and $p=p_{\mathrm{raw}}$
outside them).

*What is estimated.* A draw $(S,\beta,\sigma^2)$ defines a conditional law of $y$ given $x$,
$N\big(\bar y+(x-\bar x)^\top\beta,\ \sigma^2\big)$, with the sample-mean intercept ($\bar y$, $\bar x$ are the sample means). The
law of $x$ is **not** estimated: $f$ denotes the joint density of $(x,y)$ in which $x$ has its true law and $y$ given $x$
has the law above, and $f^*$ is the true joint density. Because $f$ and $f^*$ share the law of $x$,
$$
d_H^2(f,f^*)=E_x\Big[H^2\Big(N\big(\bar y+(x-\bar x)^\top\beta,\sigma^2\big),\ N\big(\alpha^*+x^\top\beta^*,\sigma_*^2\big)\Big)\Big],
$$
the squared Hellinger distance between the fitted and the true conditional laws of $y$ given $x$, averaged over $x$ (with
$x$ independent of the data). This is the joint-density distance of Song and Liang (2015), Theorems 1–2 (they use
$\int(\sqrt f-\sqrt{f^*})^2=2d_H^2$).

*Further notation.* $H^2(P,Q):=1-\int\sqrt{dP\,dQ}$ and $d_H(f,g):=\big(1-\int\sqrt{fg}\big)^{1/2}$. $P^*$ is the distribution
of the data. $\mathrm{sd}$, $\mathrm{Var}$, $\mathrm{Corr}$ are population standard deviations, variances and correlation
matrices; $z_j:=(x_j-Ex_j)/\mathrm{sd}(x_j)$ and $z:=(z_1,\dots,z_{p_{\mathrm{raw}}})$; $x_T$ is the sub-vector of $x$ indexed by a
set $T$; $|S|$ is the number of predictors in $S$; $a\vee b:=\max(a,b)$; $\log$ is the natural logarithm.

*Constants, level and window.* $s\ge0$ is an integer and $A\ge1$, $L\ge1$, $c_\psi>0$, $\bar b>0$ are constants; none depends
on $n$. The reader fixes a **level** $M\ge1$ (a larger $M$ gives a larger ball and a smaller exceptional probability). The
**window** is
$$
q_n:=\min\big\{p_{\mathrm{raw}},\ \lceil C_qM\log n\rceil\big\},\qquad C_q:=2\big(s(A+2)+4\big)/\log 2 ,
$$
the largest number of predictors that (A3) and (A4) constrain jointly (of order $\log n$ for a fixed level).

### Assumptions
- **(A1) Gaussian linear model.** $y=\alpha^*+x^\top\beta^*+\varepsilon$ with $\varepsilon\sim N(0,\sigma_*^2)$, $\sigma_*^2>0$,
  independent of $x$ ($\alpha^*$, $\beta^*$, $\sigma_*$ and the law of $x$ may depend on $n$).
- **(A2) Sparsity and dimension.** At most $s$ coordinates of $\beta^*$ are nonzero, and $2\le p_{\mathrm{raw}}\le n^A$.
- **(A3) Sub-Gaussian predictors on sparse directions.** Every predictor has positive variance, and for every
  $u\in\mathbb R^{p_{\mathrm{raw}}}$ with at most $q_n$ nonzero entries and every $\lambda\in\mathbb R$:
  $E\exp(\lambda u^\top z)\le\exp\big(L^2\lambda^2\,\mathrm{Var}(u^\top z)/2\big)$.
- **(A4) No near-exact collinearity.** $\lambda_{\min}(\mathrm{Corr}(x_T))\ge c_\psi/n$ for every set $T$ of at most $q_n$
  predictors.
- **(A5) Bounded signal.** $|\beta^*_j|\,\mathrm{sd}(x_j)\le\bar b\,\sigma_*$ for every $j$.

No lower bound on the nonzero coefficients (no beta-min condition) and no fixed lower bound on eigenvalues is assumed:
under (A4) predictors may be correlated up to $1-c_\psi/n$.

### Reader statement
**Theorem 9 (distribution-level consistency).** There are constants $c>0$, $C_1$, $M_0$ and $n_0$, depending only on
$(s,A,L,c_\psi,\bar b)$, such that the following holds. Fix a level $M\ge M_0$ and assume (A1)–(A5) with the window $q_n$
of this $M$. Then for every $n\ge n_0$ with $\sqrt n/\log n\ge M$:
$$
\text{(i)}\quad P^*\Big[\,\Pi\Big(d_H(f,f^*)>\sqrt{M\log n/n}\ \Big|\ D_n\Big)>n^{-cM}\Big]\le n^{-cM}.
$$
*In words.* Except on data sets of probability at most $n^{-cM}$, the posterior gives probability at most $n^{-cM}$ to
draws whose conditional law of $y$ given $x$ is farther than $\sqrt{M\log n/n}$ from the true one in Hellinger distance
averaged over $x$: the posterior contracts at the rate $\sqrt{\log n/n}$.

*Level-M form.* The same constants serve every level $M$ with $M_0\le M\le\sqrt n/\log n$, which may depend on $n$:
whenever $n\ge n_0$ and (A1)–(A5) hold with the window $q_n$ of this $M$, display (i) holds, and also
$$
\text{(ii)}\quad P^*\Big[\,\Pi\big(|S|>s+C_1M\ \big|\ D_n\big)>n^{-cM}\Big]\le n^{-cM}.
$$
The two exceptional sets of data sets can be taken to be the same set, and the bounds are uniform over all laws of the
data that satisfy (A1)–(A5) with the given constants. Statement (ii) bounds the number of selected predictors; it does
not say that they are the true ones.

*Without (A4).* If (A4) is dropped and (A3) is required only for single predictors ($u$ with one nonzero entry), then
$$
\text{(iii)}\quad P^*\Big[\,\Pi\Big(d_H(f,f^*)>\sqrt{M\log n\cdot\log(p_{\mathrm{raw}}\vee n)/n}\ \Big|\ D_n\Big)>n^{-cM}\Big]\le n^{-cM},
$$
and (ii) holds with $s+C_1M\log n$ in place of $s+C_1M$.

**Theorem 9B (parametric rate when the true predictors are detectable).** Assume (A1)–(A5) with the window $q_n$ of $M=1$,
with exactly $s\ge1$ nonzero coordinates of $\beta^*$, and in addition
- **(A6) Detectable signal.** (a) $\lambda_{\min}(\mathrm{Corr}(x_T))\ge\psi$ for a constant $\psi>0$ and every set $T$ of
  at most $(2A+3)s+2$ predictors; (b) $\min\{|\beta^*_j|\,\mathrm{sd}(x_j)/\sigma_*:\beta^*_j\neq0\}\ge b_n$, where $b_n>0$ and
  $b_n^2n/\log n\to\infty$.

Then for every sequence $M_n\to\infty$: $\ \Pi\big(d_H(f,f^*)>M_n/\sqrt n\ \big|\ D_n\big)\to0$ in $P^*$-probability.

**Corollary 9C (the output of the sampler).** The method explores the models with a sequential Monte Carlo sampler; it
does not compute the full posterior (small problems that it solves by exact enumeration are not covered here). A run is
*completed* when the method reports the status "completed"; runs that stop early are not covered. The output of a
completed run contains a list $\mathcal T$ of at most $40p+1$ distinct models: the best-scoring models among those offered to
the final run of the sampler (the models scored in that run, together with models scored earlier and carried into it:
the precomputed tables for small groups of predictors and the models kept from the calibration stage). Each model in the
list comes with the logarithm of its unnormalised posterior weight, taken to be computed in exact arithmetic. The output
contains no draws of $(\beta,\sigma^2)$. Let $\pi(\mathcal T)$ be the posterior probability of the list, and let $\hat\Pi$ (not
computed by the method) be the posterior restricted to the list: the models in $\mathcal T$, weighted in proportion to the
exponentials of their returned log-weights, each with its exact conditional posterior of $(\beta,\sigma^2)$. Under the
conditions of Theorem 9 (level-M form), with $P^*$-probability at least $1-n^{-cM}$ over the data, **every** completed run
(whatever its random numbers) with $\pi(\mathcal T)\ge n^{-cM/2}$ satisfies
$$
\hat\Pi\Big(d_H(f,f^*)>\sqrt{M\log n/n}\Big)\le n^{-cM/2}.
$$
If a completed run scored the true model $\{j:\beta^*_j\neq0\}$ and the posterior probability of that model exceeds $\tfrac12$,
then the list contains it, it is the model the method reports as most probable, and $\pi(\mathcal T)>\tfrac12$. Whether
the list carries enough posterior probability is a property of the run: the corollary does not assert it, and the output
does not certify it.

*Example.* Jointly Gaussian predictors satisfy (A3) with $L=1$; independent predictors satisfy it when each satisfies it
with a common constant $L$. (A4) holds for all large $n$ whenever every $q_n\times q_n$ principal block of the correlation
matrix has smallest eigenvalue at least a fixed $\psi>0$, for instance correlation $\rho^{|j-k|}$ with $|\rho|<1$, or equal
correlation $\rho\in[0,1)$.

### Placements (HQ card 13)
- **Abstract: display (i) only**, at a fixed level: *"If the rows are i.i.d., the response follows a Gaussian linear model
  with at most $s$ nonzero coefficients among at most $n^A$ predictors, the predictors are sub-Gaussian on sparse
  directions, no group of $O(\log n)$ predictors is nearly collinear (smallest correlation eigenvalue at least $c_\psi/n$),
  and each predictor's standardised signal is bounded, then for every fixed level $M\ge M_0$ and all large $n$, except on data sets of
  probability at most $n^{-cM}$, the posterior gives probability at most $n^{-cM}$ to conditional laws of the response
  given the predictors that are farther than $\sqrt{M\log n/n}$ from the true one in Hellinger distance averaged over the
  predictors — with no beta-min condition and no fixed lower bound on eigenvalues."*
- **Body:** the level-M form, (ii), (iii), Theorem 9B, Corollary 9C, and the remark of card row 2.2.

### Comparison with Song and Liang (2015), Theorems 1–2
Page and equation numbers are those of the published paper (J. R. Statist. Soc. B 77, 2015).
- **The analogue is display (i).** Their distance is $d(f_1,f_2)=\{\int\!\!\int(f_1^{1/2}-f_2^{1/2})^2\,dx\,dy\}^{1/2}$ between
  joint densities of $(x,y)$ that share the law of $x$ (§2.1.2, p. 952), so $d^2=2d_H^2$: the same distance. Their
  display (15) (Theorem 1, p. 952; Theorem 2 states the same form, p. 953) reads
  $P^*[\pi\{d(f,f^*)>\varepsilon_n\mid D_n\}>\exp(-c_1n\varepsilon_n^2)]<\exp(-c_1n\varepsilon_n^2)$; display (i) has this form
  with $n\varepsilon_n^2=M\log n$ (and $d_H$ in place of $d$).
- **Stronger.** (1) The prior is the one the method uses, with no tuning. Their theorems assume independent
  Bernoulli$(r_n/P_n)$ inclusion with a hard cap $|\xi|\le\bar r_n$ on the model size and conditions (9)–(14)
  (pp. 951–953), which the method's beta-binomial prior with cap $\min(p,\lfloor n/2\rfloor)$ does not meet. (2) The radius
  is a constant times $\sqrt{\log n/n}$. At polynomial $p$ their Theorem 2 (p. 953) needs $\bar r_n\log n=o(n\varepsilon_n^2)$
  with $\bar r_n\ge r_n\to\infty$ (and their (14)), so $n\varepsilon_n^2/\log n\to\infty$; their Corollary 1 (p. 954) gives
  $\varepsilon_n=O\{n^{-(1-\alpha)/2}\log^{k/2}n\}$. In display (i) the radius constant does not depend on $s$, and the
  smallest level $M_0$ grows at most linearly in $s$ (in the general form of the theorem, where the in-sample signal
  energy and coefficient cost are bounded by fixed constants; under (A5) those bounds themselves grow with $s$).
  (3) Theorem 9B gives the parametric rate $M_n/\sqrt n$ and Corollary 9C covers the sampler's output; their results
  concern the exact posterior only and give no parametric rate. (4) No lower bound on the growth of $p$ is needed; they
  assume $P_n\succ n^\theta$ (p. 950).
- **Weaker.** (1) $p_{\mathrm{raw}}\le n^A$; their Corollary 1 allows $P_n<\exp(Cn^\alpha)$. (2) Exact sparsity; their
  Theorem 1 covers approximate sparsity (their (3): $\lim_n\sum_j|\beta^*_j|<\infty$, with predictors bounded by 1), under
  which the number of nonzero coefficients may grow. (3) $s$ is fixed, with constants depending on $s$; their Theorem 2
  also has a true model of bounded size (their (4), p. 950), so this is weaker only against their Theorem 1. (4) (A4) is
  a condition on the design that their Theorems 1–2 do not have (their eigenvalue conditions, (11) and (14), are on the
  prior covariance).
- **Not the analogue: display (iii)**, the fallback without (A4). Its radius is larger by $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$,
  so its exponent is $c\,n\varepsilon_n^2/\log(p_{\mathrm{raw}}\vee n)$, not $c\,n\varepsilon_n^2$; and, as proved, its squared
  radius at the smallest admissible level is at most of order $(1+s)^3\log n\log(p_{\mathrm{raw}}\vee n)/n$ for fixed $s$
  (an upper bound; the proof is not known to be tight in $s$).
- **Different, not ranked:** tail conditions on the predictors — (A3) and (A5) here; theirs are $|x_i|\le1$ (Theorem 1),
  Condition 1 (an exponential-moment bound on averages of at most $\bar r_n$ predictors, Theorem 2, p. 953) and
  Condition 2 (second moments, for their limit form (16), p. 954).
- **Overall: incomparable** — stronger on the prior, the rate and the coded output; weaker on the range of $p$, on
  approximate sparsity and, for display (i), by (A4).

### Why each assumption
- (A1) It is the model under which the method's likelihood is correct; it gives the posterior a closed form given the
  predictors. $\sigma_*$ is free because rescaling the response leaves the posterior over models unchanged and rescales the
  posterior of $(\beta,\sigma^2)$.
- (A2) Posterior model size is controlled relative to $s$; the constants depend on $s$ and $A$.
- (A3) Only to make the sample variances of the predictors and the sample covariances of small groups of predictors track
  their population values with probability $1-n^{-cM}$. The passage from the sample to the population distance uses no
  tail condition.
- (A4) It keeps in force the prior's penalty for each extra predictor (a factor of order $n^{-1/2}$); this gives the rate
  $\sqrt{\log n/n}$, the level $n^{-cM}$ and the bounded model size. Without it the radius gains the factor
  $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$ (display (iii)). Whether it is needed for the rate $\sqrt{\log n/n}$ is open.
- (A5) It bounds the signal in units of the noise and excludes huge coefficients that cancel.
- (A6) (Theorem 9B only) It makes the posterior select the true model, which removes the logarithm.

### Master theorem
W3-DIST reader versions (`/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/STATEMENT.md` v1.4.10, §1R
:126-269), council R2 PASSED (MANIFEST `c5cd9cdd…`, astra 9.3 PASS, opus 9.2 PASS; CHECKPOINT_3); H5 card 13 AGREED.
Statuses **as the registry tool will record them** (requote verbatim from `claims.tsv` at application):
- Theorem 9 (display (i), level-M form, (ii), (iii)) = `W3-DIST:Thm-A` (:185-207; = DIST-1 (1.1) + bridges B0, B1, B2; the
  sentence without (A4) = DIST-2 (1.2) + B0, B1): **"PROVED-CHECKED, conditional on SOP:TH09 (T01 part)"**.
- Theorem 9B = `W3-DIST:Thm-B` (:209-215): **"PROVED-CHECKED, conditional on W3-POST:Thm-1, SOP:TH09 (T01 part)"**.
- Corollary 9C = `W3-DIST:Cor-C` (:217-238): **"PROVED-CHECKED, conditional on SOP:TH09 (T01 part)"**; exact arithmetic is
  a premise stated in the corollary. DIST-C's delivery statements (not used by 9C): **"PROVED-CHECKED, conditional on
  SOP:TH09 (T01 part), W3-SAMP:D, W3-SAMP:PC, W3-SAMP:LT#, W3-SAMP:C, W3-SAMP:TR"**.
- SOP:TH09 = its T01 part ("T01–T03: PROVED-LOCKED": the coded posterior is the contrast-model posterior).

### Bridges
| # | bridge | mark | detail |
|---|---|---|---|
| B9.0 | renaming: DIST's $p$ ↦ $p_{\mathrm{raw}}$, $r$ ↦ $p$, (A3) constant $K$ ↦ $L$, $\sigma^*$ ↦ $\sigma_*$ | identity | to match `NOTATION.md` §1, §3 (there $K$ is the size cap) |
| B9.1 | Theorem 9 (i), (ii), the "same set" and uniformity sentences, the Example = W3-DIST Theorem A | identity (text) | STATEMENT :185-207 |
| B9.1a | fixed-level statement first, then the level-M form = Theorem A with $M$ constant, then as written (same constants, same $n_0$ for all $M\le\sqrt n/\log n$) | identity (reordering) | STATEMENT :185-191 (the constants, $n_0$ included, depend only on $(s,A,K,c_\psi,\bar b)$; the fixed-level form adds $M\le\sqrt n/\log n$ to $n\ge n_0$) |
| B9.2 | display (iii) = Theorem A's "Without (A4)" sentence written as a display (same level $n^{-cM}$, radius times $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$) | identity (transcription) | STATEMENT :200-202 |
| B9.3 | Theorem 9B, Corollary 9C = W3-DIST Theorem B, Corollary C | identity (text; the mixture sentence of C shortened, no content dropped from the claim) | STATEMENT :209-238 |
| B9.4 | "$p=p_{\mathrm{raw}}$ outside the exceptional sets" | EXISTS-CHECKED (line-checked + council R2) | W3-DIST Setup :150-152 and bridge B1 :391-395 (on B1's event no column is dropped) |
| B9.5 | exponent in (iii): $cM\log n=c\,n\varepsilon_n^2/\log(p_{\mathrm{raw}}\vee n)$ at $\varepsilon_n^2:=M\log n\log(p_{\mathrm{raw}}\vee n)/n$ | VERIFIED (F9) | substitute $\varepsilon_n$ |
| B9.6 | Song–Liang sentences | checked against the paper: `reviews/SL_PDF_CHECK.md` | page / equation / theorem numbers there |
| B9.7 | "what is estimated": $d_H^2(f,f^*)$ = averaged conditional Hellinger distance; plug-in sample-mean intercept; law of $x$ not estimated | EXISTS (W3-DIST §0, council R2) | STATEMENT :42-52 |
| B9.8 | sparsity statements of the comparison: (i) radius constant free of $s$, level at most linear in $s$, in DIST-1's interface form; (iii) as proved, squared radius at most of order $(1+s)^3\log n\log(p_{\mathrm{raw}}\vee n)/n$ for fixed $s$ | EXISTS: (i) DIST-1 (c) :84-87 (TC3, checked D1, D5, both R2 seats); (iii) Dept RT1 (Sol) steps 4–11, W3-DIST `reviews/UNHARVESTED_STRENGTH.md` item 9 | interface form: energy and coefficient-cost bounds held fixed; under (A5) these bounds grow with $s$ (bridge B1 :391-395) |

### Honest limits
Statement (ii) bounds the size of the selected models, not their identity. Corollary 9C does not assert that a run's
list carries enough posterior probability, and the output does not certify it; runs that stop early and the exact
enumeration branch are not covered. Status: the masters' statuses above, with their conditions.

#### Update log (thm9)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes none.
- v0.3 2026-11-16 (proposal, HQ card 13): placeholder → proved version from W3-DIST §1R (council R2 passed): setting,
  numbered assumptions (A1)–(A6), displays (i)–(iii), Theorems 9B and Corollary 9C, Song–Liang comparison (STRONGER:
  placeholder → theorem). F9 repairs to the card rows.
- v0.4 2026-11-16 (proposal, H5 card 13 AGREED): "what is estimated" (conditional law of $y$, Hellinger averaged over
  $x$; law of $x$ not estimated) replaces "joint distribution"; fixed-level display first, level-M form second; the
  Song–Liang analogue is display (i) only, (iii) is the fallback; sparsity statements per B9.8; "s fixed" added to the
  weaker list; every Song–Liang sentence checked against the paper; placements (abstract: display (i) only) (EQUAL on
  the theorems; presentation and comparison only).
<!-- ROW thm9 END -->
````

Variant A, master-status bullets:

- Theorem 9 (display (i), level-M form, (ii), (iii)) = `W3-DIST:Thm-A` (:185-207; = DIST-1 (1.1) + bridges B0, B1, B2; the
  sentence without (A4) = DIST-2 (1.2) + B0, B1): **"PROVED-CHECKED"**.
- Theorem 9B = `W3-DIST:Thm-B` (:209-215): **"PROVED-CHECKED, conditional on W3-POST:Thm-1"** (the condition drops if task
  T also records W3-POST:Thm-1).
- Corollary 9C = `W3-DIST:Cor-C` (:217-238): **"PROVED-CHECKED"**; exact arithmetic is a premise stated in the corollary.
  DIST-C's delivery statements (not used by 9C): **"PROVED-CHECKED, conditional on W3-SAMP:D, W3-SAMP:PC, W3-SAMP:LT#,
  W3-SAMP:C, W3-SAMP:TR"** (as recomputed by the tool).

## 3. Row 2.2 (body remark; no longer a fallback)
Unchanged from the F9 version. Reason: it covers fixed designs and the in-sample distance, which Theorem 9 does not state.

| 2.2 | **Body remark (no longer a fallback):** fixed design; $\bar h_n$ = in-sample average Hellinger distance between the fitted and the true laws of one observation (centred scale). Premises of both parts: Gaussian linear model (G), $s_0\ge1$ fixed and $2\le p\le n^A$ (regime R1), energy bound (E), eigenvalue floor on $S_0$ (F₀); conclusions in probability. (a) If also $1-\pi(S_0\mid y)\to0$ in probability: $\Pi(\bar h_n>M_n/\sqrt n\mid y)\to0$ for every $M_n\to\infty$ (distance, rate $M_n/\sqrt n$). (b) Without beta-min, under the superset Occam-sum condition (OS) instead: $\Pi(\bar h_n^2>C'_H\log n/n\mid y)\to0$ (squared distance $\log n/n$; distance radius $\sqrt{C'_H\log n/n}$). | `W3-POST2:D@1.1.4`: "PROVED-CHECKED, conditional on SOP:TH09, SOP:TH128, W2-APP:POST, W3-POST:Thm-1" [REG-f526]. | Fixed designs and the in-sample distance, which Theorem 9 does not state. | body remark, to write at the freeze if kept |

## 4. Bridges (reader wording ⇒ W3-DIST statement)
In the thm9 block's "Bridges" table: B9.0–B9.4, B9.1a (reordering, identity), B9.5 (VERIFIED by F9), B9.6 (Song–Liang
sentences, `SL_PDF_CHECK.md`), B9.7 (what is estimated; EXISTS, STATEMENT :42-52), B9.8 (sparsity statements; EXISTS:
DIST-1 (c) :84-87 for (i), RT1 + UNHARVESTED item 9 for (iii)). **No NEW step.**
**Checks wanted:** a short diff read of v0.3 → v0.4 (§0 items 1–5), especially B9.8's interface-form qualifier and the
fixed-level form's "$\sqrt n/\log n\ge M$".

## 4b. F9 repairs (2026-11-16)
F9 (Sol; `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/DIST_thm9_fidelity/F9_sol.md`): B9.5 VERIFIED; four card findings repaired:
(1) row 2.1 states the window $q_n(M)$ in place of "any $O(\log n)$ predictors"; (2) row 2.1's sentence without the
collinearity condition adds the size bound $s+C_1M\log n$; (3) row 2.2 labels distance vs squared distance
($\bar h_n$ at $M_n/\sqrt n$; $\bar h_n^2$ at $C'_H\log n/n$); (4) row 2.2 names the premises (R1, G, (E), (F₀), and
$\delta_n\to0$ for (a), (OS) for (b)), in probability. Optional item applied: Song–Liang Corollary 1 written as
$\varepsilon_n^2=\dots$ in the body.

## 5. Changelog tag
Row thm9 v0.4: EQUAL on the theorems (reordering, transcription, added "what is estimated" identity); the comparison is
corrected against the paper. Card row 2.1: "in progress" → proved, abstract = display (i). Row 2.2: body remark, EQUAL.
