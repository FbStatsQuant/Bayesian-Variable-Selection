# Proofs of Propositions P5, P8, P9, P10 and P11

Supplement material for *Split-and-merge with an exact merge: composite-start sequential Monte Carlo for Bayesian variable selection*, draft of 15 October 2026 (`paper_draft/paper_draft.tex`). Thread: elementary_III. Prover: Fable 5.1 (lead), 15 October 2026. Version 2 (after review round 1; v1 is kept as `review/PROOF.md`, the changes are listed in FINDINGS.md). Notation follows Section 2 of the draft. Of the draft's numbered results only P7 is used (in P10(iii)), in the form proved in `proofs/foundations/PROOF.md`: Theorem 5.3 (unbiasedness), Theorem 5.5(a) (the Markov bound), Theorem 5.7 (the weighted estimator when resampling is skipped) and Corollary 5.6a with (H4) (the pilot); everything else is proved from the definitions with standard linear algebra and probability (each fact is named where it is used). Numerical checks of the exact formulas, the examples and the counterexamples are in `check_elementary_III.py` beside this file (output in `check_elementary_III.out`); they are not part of the proofs.

**Summary of the outcome.** Four of the five propositions are true as stated, under the readings fixed in Section 0.3 (each is flagged there and collected in Section 6); P8(iii) is true in a corrected form (Theorem 2.3): as literally written it fails when $p(S)m(S)$ has tied maximisers, and it presupposes $U\ge Z$ (Example 2.3a). What the proofs add or make precise:

- **P5(iii).** The capped minimiser is proved by a rearrangement argument; it is unique if and only if condition (U) of Theorem 1.3 holds (no tie at the cut when $N_+>k_{\max}$; no $\mathrm{PIP}_j=\tfrac12$ when $N_+<k_{\max}$; and always when $N_+=k_{\max}$, even if some $\mathrm{PIP}_j=\tfrac12$). The median model can have more than $k_{\max}$ elements (Example 1.4), so the cap can bind.
- **P8(iv), (iv′).** The shrinkage floor (eq:floor of the draft) is re-derived in a form valid for every $|S|$, including $|S|>n$ (Lemma 2.1). In (iv′) the hypothesis $p<n$ can be weakened to $\lambda_{\min}(G_{[p]})>0$ (which forces $p\le n$); the $Q_S$ part needs no hypothesis at all; and interlacing gives the sharper $D_S\ge\prod_{i\le|S|}h(\lambda_i(G_{[p]}))$ (Theorem 2.4). The ratio of the bound (iv) to $m(\emptyset)$ is exactly $\big(A_0/(2b_0+y^\top y/(n+1))\big)^{\nu}\in[1,(n+1)^{\nu})$: it is $1$ at $y=0$ and tends to $(n+1)^{\nu}$ as $b_0/y^\top y\to0$, the regime of the draft's "about $(n+1)^{n/2}$".
- **P8(iii).** As literally written the statement is false in two ways: the $U$ of (iii) must be the $U\ge Z$ of (ii) (with $U=Z_V$ the hypothesis is vacuous), and when $p(S)m(S)$ has tied maximisers an $\hat S\in\arg\max_V$ that is not $\prec$-first is not the HPM (Example 2.3a). The corrected statement is Theorem 2.3: under $U\ge Z$, every global maximiser lies in $V$, so the HPM over $V$ is the global HPM and $\hat S$ is a global maximiser.
- **P9(i).** The exact relation $\mathrm{PIP}_j=(1-f)\,\mathrm{PIP}_{j,V}+\pi(\{S\ni j\}\cap V^c)$ gives the two-sided interval $(1-f)\mathrm{PIP}_{j,V}\le\mathrm{PIP}_j\le(1-f)\mathrm{PIP}_{j,V}+f$, which implies $|\mathrm{PIP}_j-\mathrm{PIP}_{j,V}|\le f$ and is P8(ii) with $U=Z$.
- **P10.** The probability model is made explicit: $V=V(y,\zeta)$ for the run's randomness $\zeta$, and the validation draws are i.i.d. $\pi(\cdot\mid y)$ and independent of $\zeta$ given $y$. (i) The safeguard's bias is given exactly (a finite sum); its sign depends on $(M,f)$ (non-negative when $M(1-f)\ge2$, negative at $M=1$ when $f>0$), and a second safeguard $Z_V(M+1)/(K_{\rm in}+1)$ with closed-form bias $-Zf^{M+1}$ is recorded. (ii) is proved for any non-randomised upper confidence bound based on $K_{\rm out}$ (Definition 4.4), Clopper–Pearson's validity is proved, and the failure of conditional coverage is exact: for $f\in((1-\alpha)^{1/M},1)$ the coverage conditional on a finite bound is $0$, and for $f\le(1-\alpha)^{1/M}$ it is positive. If the draws are not independent of $V$ (for instance $V$ is the set of the draws themselves), coverage can be $0$ unconditionally (Example 4.7). (iii) is an unconditional statement (given $y$); it needs the hypotheses of P7(i) as made precise in `foundations`, applied island by island conditionally on the pilot, and the validation draws must be exact posterior draws given everything $V$ was built from (hence independent of the islands when $V$ comes from them); the union bound needs no joint law of the two events.
- **P11.** The statement is written with an explicit sub-$\sigma$-field; "zero conditional variance" means $\mathrm{Var}(X\mid\mathcal F)=\mathbb E[(X-\mathbb E[X\mid\mathcal F])^2\mid\mathcal F]=0$ a.s., which is equivalent to $\mathcal F$-measurability. The law of total variance makes "does not remove inherited error" exact. Example 5.3 (two particles, weights $2^{\gamma_i}$ normalised after the update) has $\mathbb E[\sum_iW_io_{ij}]=\tfrac{37}{96}\ne\tfrac{11}{24}=\mathbb E[T]$ and $\mathrm{Var}(\sum_iW_io_{ij}\mid\mathcal F)>0$.

Flags for the draft are collected in Section 6.

---

## 0. Setting, conventions and the frozen statements

### 0.1 The model space, the posterior and the decisions

Throughout, $n,p\ge1$, the design $X\in\mathbb R^{n\times p}$ has standardised columns ($\|x_j\|^2=n$), $y\in\mathbb R^n$, and $a_0,b_0>0$. For $S\subseteq[p]$ with $k=|S|$: $G_S=X_S^\top X_S$, $z_S=X_S^\top y$, $H_S=(n+1)G_S+I_k$, $D_S=\det H_S/\det(G_S+I_k)$, $t_S=n\,z_S^\top H_S^{-1}z_S$, $Q_S=y^\top y-t_S$, $\nu=a_0+\tfrac n2$, and
$$
m(S)=C_n\,D_S^{-1/2}(2b_0+Q_S)^{-\nu},\qquad C_n=\pi^{-n/2}(2b_0)^{a_0}\frac{\Gamma(\nu)}{\Gamma(a_0)}>0 .
$$
For $S=\emptyset$ the conventions are $D_\emptyset=1$, $t_\emptyset=0$, $Q_\emptyset=y^\top y$, so $m(\emptyset)=C_n(2b_0+y^\top y)^{-\nu}$. $P_S$ is the orthogonal projection onto the column span of $X_S$ ($P_\emptyset=0$), and $A_0=2b_0+y^\top y$. Since $H_S\succ0$ and $Q_S\ge0$ (Lemma 2.1), $m(S)$ is well defined and $m(S)>0$ for every $S$.

The model prior is $p(S)=w(|S|)\mathbf 1\{|S|\le k_{\max}\}/c_w$ with $w(k)>0$ for $0\le k\le p$, an integer cap $0\le k_{\max}\le p$ (a larger cap is read as $p$, as the draft says) and the normaliser $c_w=\sum_{k\le k_{\max}}\binom pkw(k)$. Its support is $\mathcal S=\{S\subseteq[p]:|S|\le k_{\max}\}$, which is finite and contains $\emptyset$. The evidence and the posterior are
$$
Z=\sum_{S\subseteq[p]}p(S)m(S)=\sum_{S\in\mathcal S}p(S)m(S)>0,\qquad \pi(S)=\frac{p(S)m(S)}{Z},
$$
so $\pi$ is a probability on $2^{[p]}$ with $\pi(S)>0$ exactly for $S\in\mathcal S$. The *size-$k$ prior mass* is $p(|S|=k)=\sum_{|S|=k}p(S)=\binom pkw(k)/c_w$ for $0\le k\le k_{\max}$.

*Decisions.* A fixed total order $\prec$ on $2^{[p]}$ breaks ties. Write $\mathcal A_j=\{S\subseteq[p]:j\in S\}$ and $\mathrm{PIP}_j=\pi(\mathcal A_j)$. The *median model* is $\{j:\mathrm{PIP}_j>\tfrac12\}$. For a nonempty $V\subseteq2^{[p]}$, the *HPM over $V$* is the $\prec$-first element of $\arg\max_{S\in V}p(S)m(S)$; the *global HPM* is the HPM over $2^{[p]}$ (equivalently over $\mathcal S$, since $p(S)m(S)=0$ off $\mathcal S$ and $>0$ on it). Only the products $p(S)m(S)$ enter Sections 1, 3, 4 and 5; nothing there uses the specific form of $m$.

*Certificates.* For a nonempty $V\subseteq2^{[p]}$: $Z_V=\sum_{S\in V}p(S)m(S)$, $A_j=A_j(V)=\sum_{S\in V,\,j\in S}p(S)m(S)$ and $B_j=Z_V-A_j$ (the draft's $A_j$ is this number; the event $\{S\ni j\}$ is written $\mathcal A_j$ to avoid the clash). "Scored models" means models whose $p(S)m(S)$ has been computed; $V$ may contain models outside $\mathcal S$, which contribute $0$. $\pi(V)=Z_V/Z$ and $f=\pi(V^c)=1-Z_V/Z$. The *truncated posterior* is $\pi(\cdot\mid V)=\pi(\cdot\cap V)/\pi(V)$ when $\pi(V)>0$, and $\mathrm{PIP}_{j,V}=\pi(\mathcal A_j\mid V)=A_j/Z_V$.

*Total variation.* For probabilities $\mu,\mu'$ on a finite set, $\|\mu-\mu'\|_{\rm TV}=\sup_A|\mu(A)-\mu'(A)|$, the supremum over all subsets, as the draft's P9(ii) prescribes. (It equals $\sum_S(\mu(S)-\mu'(S))^+$; this is recalled and proved in Lemma 3.1, not assumed.)

### 0.2 The statements, as frozen from the draft (verbatim)

The five statements are copied from `paper_draft.tex` (15 October 2026); the LaTeX is reproduced, with the draft's macros expanded only where Markdown needs it ($\PIP\to\mathrm{PIP}$, $\HPM\to$ HPM, $\Prob\to\mathbb P$, $\E\to\mathbb E$, $\Zhat\to\widehat Z$, $\pihat\to\hat\pi$, $\TV\to{\rm TV}$). Each carries the status line `\status{Elementary}` in the draft, omitted here.

**Proposition P5 (Decisions, supplementary).**
(i) The HPM is the Bayes action for 0–1 loss on models.
(ii) $\{j:\mathrm{PIP}_j>\tfrac12\}$ minimises posterior expected Hamming loss over all subsets.
(iii) Under the cap, the constrained minimiser keeps the $\min\{k_{\max},\#\{j:\mathrm{PIP}_j>\tfrac12\}\}$ coordinates with the largest $\mathrm{PIP}_j$.

**Proposition P8 (Certificates and a universal evidence bound).**
Let $V$ be any nonempty set of scored models. Put $Z_V=\sum_{S\in V}p(S)m(S)$, $A_j=\sum_{S\in V,j\in S}p(S)m(S)$ and $B_j=Z_V-A_j$.
(i) $Z_V\le Z$.
(ii) If $U\ge Z$, then $A_j/U\le\mathrm{PIP}_j\le1-B_j/U$ for every $j$.
(iii) If $\hat S\in\arg\max_{S\in V}p(S)m(S)$ and $U-Z_V<p(\hat S)m(\hat S)$, then $\hat S$ is the global HPM.
(iv) *(Universal bound.)* $Z\le C_n\big(2b_0+y^\top y/(n+1)\big)^{-\nu}$, since $D_S\ge1$, by (eq:floor), and since $\sum_Sp(S)=1$. This is valid but numerically vacuous: it exceeds $m(\emptyset)$ by about $(n+1)^{n/2}$.
(iv′) *(Size-aware bound, $p<n$.)* Suppose $\lambda_{\min}(G_{[p]})\ge n\varphi^2>0$, and put $\varrho=((n+1)n\varphi^2+1)/(n\varphi^2+1)$. Then
$$
Z\le C_n\big(2b_0+\mathrm{RSS}_{[p]}+\|P_{[p]}y\|^2/(n+1)\big)^{-\nu}\sum_{k\le k_{\max}}p(|S|=k)\,\varrho^{-k/2},
$$
since $Q_S\ge y^\top y-\tfrac n{n+1}\|P_{[p]}y\|^2$ and $D_S\ge\varrho^{|S|}$ by interlacing.
(v) If $V=\{S\in W:\log p(S)m(S)\ge M_W-\Delta\}$ with $M_W=\max_W\log p(S)m(S)$, then $Z_W-Z_V\le|W\setminus V|\,e^{M_W-\Delta}$.

(The draft's equation (eq:floor) is: $0\le t_S\le\tfrac{n}{n+1}\|P_Sy\|^2$, $Q_S\ge\frac{y^\top y}{n+1}$, stated under the heading "Shrinkage floor" in Section 2.1 with the one-line justification "the eigenvalues of $nX_SH_S^{-1}X_S^\top$ are $n\lambda/((n+1)\lambda+1)<n/(n+1)$, where $\lambda$ ranges over the eigenvalues of $G_S$". It is re-proved here as Lemma 2.1, since P8(iv) cites it.)

**Proposition P9 (Truncation and decision agreement).**
(i) Let $f=\pi(V^c)<1$. Then $\|\pi-\pi(\cdot\mid V)\|_{\rm TV}=f$ and $|\mathrm{PIP}_j-\mathrm{PIP}_{j,V}|\le f$ for every $j$.
(ii) If $\max_j|\hat\pi_j-\mathrm{PIP}_j|\le\delta<\min_j|\mathrm{PIP}_j-\tfrac12|$, then the estimated and exact median models $\{j:\hat\pi_j>\tfrac12\}$ and $\{j:\mathrm{PIP}_j>\tfrac12\}$ coincide. Here $\|\cdot\|_{\rm TV}=\sup_A|\cdot|$.
(iii) Under a fixed tie rule, the HPM over $V$ equals the global HPM if and only if the global HPM lies in $V$.

**Proposition P10 (Visited-set estimator and confidence bound).**
Let $V$ be frozen with $Z_V>0$, and let $f=\pi(V^c)$. Then $Z=Z_V/(1-f)$ exactly. Let $K_{\rm in}$ be the number of $M$ i.i.d. *exact* posterior draws falling in $V$, where the draws are independent of the construction of $V$ given $y$.
(i) If $f>0$, the classical estimator $Z_VM/K_{\rm in}$ is infinite with probability $f^M>0$. Finite-sample bias and variance statements therefore require a safeguard, for instance $Z_VM/\max(K_{\rm in},1)$, whose bias must then be stated.
(ii) Let $f_U$ be a $(1-\alpha)$ upper confidence bound for $f$ (e.g. Clopper–Pearson). Set $U_V=Z_V/(1-f_U)$, with $U_V=+\infty$ when $f_U=1$. Then $\mathbb P(Z\le U_V)\ge1-\alpha$ unconditionally. Coverage conditional on reporting a finite bound need not hold.
(iii) With P7(ii), $[\alpha\bar Z_R,\ U_V]$ covers $Z$ with probability at least $1-2\alpha$.
For SMC (non-exact) validation draws, (ii) requires a bound on the joint law of the draws. This is not available and is deferred.

**Proposition P11 (Rao–Blackwellised PIPs, supplementary).**
Let $\mathcal F$ be the $\sigma$-field of the population just before the final update of coordinate $j$. Suppose:
- the normalised weights $W_i$ and the conditional probabilities $o_{ij}$ are $\mathcal F$-measurable;
- the update is a Gibbs draw $\gamma_{ij}$ with $\mathbb E(\gamma_{ij}\mid\mathcal F)=o_{ij}$.
Then $\sum_iW_io_{ij}=\mathbb E(\sum_iW_i\gamma_{ij}\mid\mathcal F)$, and it has zero conditional variance given $\mathcal F$. Weights that depend on the post-update state invalidate this. It does not remove error inherited from earlier stages.

**P7(ii), as used in P10(iii)** (frozen in `proofs/foundations/PROOF.md`, Section 0.2, and proved there as Theorem 5.5): *For $R$ i.i.d. islands with mean $\bar Z_R$ and any $\alpha\in(0,1)$: $\mathbb P(Z\ge\alpha\bar Z_R)\ge1-\alpha$. Under finite variance, a CLT in $R$ gives two-sided intervals for $\mathbb E[\widehat Z]=Z$.* Only the first sentence is used, in the form of Theorem 5.5(a) there: it holds for every $R\ge1$, needs only $\mathbb E[\widehat Z_r]=Z$ for each island (Theorem 5.3 there, under (H0)–(H3), or Theorem 5.7 when resampling is skipped), not independence of the islands; and it holds conditionally on the pilot, hence unconditionally given $y$, when each island's conditional law given the pilot is the one of Theorem 5.3 or 5.7 (Theorem 4.8(A); Corollary 5.6a there is the version for conditionally independent islands).

### 0.3 Readings adopted (each flagged in Section 6)

- **R1 (P5, loss functions).** 0–1 loss on models: $L(a,S)=\mathbf 1\{a\ne S\}$; Hamming loss: $L(a,S)=|a\,\triangle\,S|$. The action $a$ ranges over all subsets of $[p]$ in (i)–(ii) and over $\{a:|a|\le k_{\max}\}$ in (iii). "The constrained minimiser" in (iii) is read as "a constrained minimiser, and the unique one in the absence of ties" (Theorem 1.3 states exactly when it is unique). "The coordinates with the largest $\mathrm{PIP}_j$" is read as: any set $a^\ast$ of that size, drawn from $J_+=\{j:\mathrm{PIP}_j>\tfrac12\}$, such that no coordinate of $J_+\setminus a^\ast$ has a larger PIP than a coordinate of $a^\ast$ ($\min_{a^\ast}\mathrm{PIP}_j\ge\max_{J_+\setminus a^\ast}\mathrm{PIP}_j$, with $\min\emptyset=+\infty$ and $\max\emptyset=-\infty$); ties at the cut are immaterial.
- **R2 (P8(iii), $U$ and ties; a correction, not a reading).** The $U$ of (iii) is the $U$ of (ii), so $U\ge Z$ is presupposed (without it the hypothesis $U-Z_V<p(\hat S)m(\hat S)$ holds for $U=Z_V$ and every $V$, and the conclusion is false: Example 2.3a(b)). With ties the literal conclusion is false (Example 2.3a(a)); "$\hat S$ is the global HPM" is proved in the corrected form: every global maximiser of $p(S)m(S)$ lies in $V$, so the HPM over $V$ is the global HPM, and every $\hat S\in\arg\max_V$ is a global maximiser. If $\arg\max_V$ has several elements, only the $\prec$-first of them is *the* HPM.
- **R3 (P8(iv′)).** The heading's "$p<n$" is read as the hypothesis actually used, $\lambda_{\min}(G_{[p]})>0$, which forces $p\le n$ ($G_{[p]}$ has rank $\le n$); $p=n$ with $X$ invertible is allowed. $\mathrm{RSS}_{[p]}=\|(I-P_{[p]})y\|^2$.
- **R4 (P9).** In (i), $V\subseteq2^{[p]}$ is any set with $\pi(V)>0$; $\pi(\cdot\mid V)$ is the truncated posterior of Section 0.1. In (ii), $\hat\pi_j\in\mathbb R$ are arbitrary numbers (estimates); the sentence "Here $\|\cdot\|_{\rm TV}=\sup_A|\cdot|$" belongs to (i). In (iii), "a fixed tie rule" is the draft's fixed total order $\prec$, applied in the same way over $V$ and over all models; $V$ is nonempty.
- **R5 (P10, the probability model).** Section 4.1: the data $y$ are fixed; $V=V(y,\zeta)$ is a measurable function of $y$ and of the randomness $\zeta$ of its construction (the SMC run, the pilot, any auxiliary randomness); the validation draws $\Sigma_1,\dots,\Sigma_M$ are, conditionally on $(y,\zeta)$, i.i.d. $\pi(\cdot\mid y)$ (this is "exact draws independent of the construction of $V$ given $y$"); $K_{\rm in}=\#\{m:\Sigma_m\in V\}$ and $K_{\rm out}=M-K_{\rm in}$. "Frozen" means that the statements of the preamble, of (i) and of (ii) are made conditionally on $(y,\zeta)$; "unconditionally" means after integrating $\zeta$ out (given $y$). $x/0=+\infty$ for $x>0$. A "$(1-\alpha)$ upper confidence bound for $f$" is a non-randomised function $f_U:\{0,\dots,M\}\to[0,1]$ of $K_{\rm out}$ alone with $\mathbb P_f(f_U(K_{\rm out})\ge f)\ge1-\alpha$ for every $f\in[0,1]$ when $K_{\rm out}\sim\mathrm{Bin}(M,f)$ (Definition 4.4); "reporting a finite bound" is the event $\{f_U<1\}$. Part (iii) is read as an unconditional statement given $y$ (over the pilot, the islands, $\zeta$ and the draws): $\bar Z_R$ is the mean of $R$ island estimates each satisfying the hypotheses of P7(i) as made precise in `foundations`, conditionally on the pilot (Theorem 4.8(A)); the islands' randomness may be part of $\zeta$ (for instance $V$ is their visited set), in which case the validation draws must be independent of the islands; the same $\alpha$ is used in both bounds. The conditional (given $\zeta$) form of (iii) holds when the islands are not part of $\zeta$ (Remark 4.9).
- **R6 (P11).** "The $\sigma$-field of the population just before the final update of coordinate $j$" is read as the $\sigma$-field of the run's whole history up to that moment (the current population and its carried weights included), for a fixed sweep order; Section 5.1 and Remark 5.2. $\gamma_{ij}=\mathbf 1\{j\in S^i\}$ evaluated immediately after the Gibbs update of coordinate $j$ of particle $i$; $W_i\ge0$, $\sum_iW_i=1$; $o_{ij}\in[0,1]$. "Zero conditional variance given $\mathcal F$" means $\mathrm{Var}(Y\mid\mathcal F):=\mathbb E[(Y-\mathbb E[Y\mid\mathcal F])^2\mid\mathcal F]=0$ almost surely. "Weights that depend on the post-update state invalidate this" is read as: if $W_i$ is not $\mathcal F$-measurable, both conclusions can fail (Example 5.3). "Does not remove error inherited from earlier stages" is read as Theorem 5.1(d): the bias and the variance of the conditional mean are unchanged.

### 0.4 Standard facts used

(F-a) *Cauchy interlacing*, in the form: if $G$ is a real symmetric $p\times p$ matrix and $G_S$ is a $k\times k$ principal submatrix, then $\lambda_i(G_S)\ge\lambda_i(G)$ for $i=1,\dots,k$ (eigenvalues in increasing order); in particular every eigenvalue of $G_S$ is $\ge\lambda_{\min}(G)$. (F-b) *Push-through identity*: for $A\in\mathbb R^{n\times k}$ and $c>0$, $A(cA^\top A+I_k)^{-1}=(cAA^\top+I_n)^{-1}A$ (multiply out: both sides equal $(cAA^\top+I_n)^{-1}\big[(cAA^\top+I_n)A\big](cA^\top A+I_k)^{-1}=(cAA^\top+I_n)^{-1}A(cA^\top A+I_k)(cA^\top A+I_k)^{-1}$). (F-c) Conditional expectation: linearity, "taking out what is known" (for $Y$ $\mathcal F$-measurable and bounded and $X$ integrable, $\mathbb E[YX\mid\mathcal F]=Y\,\mathbb E[X\mid\mathcal F]$), the tower property, and the law of total variance $\mathrm{Var}(X)=\mathbb E[\mathrm{Var}(X\mid\mathcal F)]+\mathrm{Var}(\mathbb E[X\mid\mathcal F])$ for square-integrable $X$. (F-d) Markov's inequality. (F-e) Jensen's inequality (conditional form included). (F-f) For $K\sim\mathrm{Bin}(M,q)$ with $0<q\le1$: $\mathbb P(K=0)=(1-q)^M$, $\mathbb E[K]=Mq$, and $\mathbb E[1/(K+1)]=(1-(1-q)^{M+1})/((M+1)q)$ (proved in Lemma 4.2). (F-g) For a function $F:[0,1]\to[0,1]$ that is continuous and strictly decreasing with $F(0)=1$, $F(1)=0$, the equation $F(f)=\alpha\in(0,1)$ has a unique root (intermediate value theorem).

---

## 1. Proposition P5: decisions

Throughout this section $\pi$ is the posterior of Section 0.1 (a probability on $2^{[p]}$ with support $\mathcal S$), the *posterior expected loss* of an action $a\subseteq[p]$ under a loss $L$ is $\rho_L(a)=\sum_S\pi(S)L(a,S)$, and a *Bayes action* over a class $\mathcal C$ of actions is a minimiser of $\rho_L$ over $\mathcal C$. Only $\pi$ enters; the form of $m$ is irrelevant.

**Theorem 1.1 (P5(i)).** For the 0–1 loss $L(a,S)=\mathbf 1\{a\ne S\}$, $\rho_{01}(a)=1-\pi(a)$ for every $a\subseteq[p]$. Hence the Bayes actions over $2^{[p]}$ are exactly the maximisers of $\pi$, which are the maximisers of $p(S)m(S)$ over $2^{[p]}$ and lie in $\mathcal S$; the HPM (the $\prec$-first of them) is a Bayes action, and it is the unique one if and only if $p(S)m(S)$ has a unique maximiser (so "the Bayes action" of the draft is "a Bayes action" when there are ties).

*Proof.* $\rho_{01}(a)=\sum_S\pi(S)\mathbf 1\{S\ne a\}=1-\pi(a)$. Minimising $1-\pi(a)$ is maximising $\pi(a)=p(a)m(a)/Z$, and $Z>0$ does not depend on $a$. Since $\pi>0$ on $\mathcal S\ne\emptyset$ and $\pi=0$ off $\mathcal S$, every maximiser lies in $\mathcal S$. The HPM is by definition one of the maximisers. $\square$

**Theorem 1.2 (P5(ii)).** For the Hamming loss $L(a,S)=|a\,\triangle\,S|$,
$$
\rho_H(a)=\sum_{j=1}^p\Big[\mathbf 1\{j\in a\}(1-\mathrm{PIP}_j)+\mathbf 1\{j\notin a\}\mathrm{PIP}_j\Big]=\sum_{j=1}^p\mathrm{PIP}_j+\sum_{j\in a}(1-2\,\mathrm{PIP}_j)\qquad(a\subseteq[p]).\tag{1.1}
$$
The median model $a_{\rm med}=\{j:\mathrm{PIP}_j>\tfrac12\}$ minimises $\rho_H$ over $2^{[p]}$, with minimum $\sum_j\min(\mathrm{PIP}_j,1-\mathrm{PIP}_j)$; the minimiser is unique if and only if no $\mathrm{PIP}_j$ equals $\tfrac12$.

*Proof.* $|a\triangle S|=\sum_j\big[\mathbf 1\{j\in a,\,j\notin S\}+\mathbf 1\{j\notin a,\,j\in S\}\big]$. Taking $\pi$-expectations term by term and using $\pi(\{S:j\in S\})=\mathrm{PIP}_j$ gives the first form of (1.1); the second follows from $\mathbf 1\{j\notin a\}=1-\mathbf 1\{j\in a\}$. The $j$-th summand of the first form depends on $a$ only through $\mathbf 1\{j\in a\}$ and equals $1-\mathrm{PIP}_j$ if $j\in a$ and $\mathrm{PIP}_j$ if $j\notin a$; its minimum over the two choices is $\min(\mathrm{PIP}_j,1-\mathrm{PIP}_j)$, attained by $j\in a$ when $\mathrm{PIP}_j>\tfrac12$, by $j\notin a$ when $\mathrm{PIP}_j<\tfrac12$, and by both when $\mathrm{PIP}_j=\tfrac12$. Since the $p$ choices are independent of one another and there is no constraint on $a$, $\rho_H$ is minimised by minimising each summand, which $a_{\rm med}$ does; the minimiser is unique exactly when every coordinate's choice is forced. $\square$

**Theorem 1.3 (P5(iii)).** Let $J_+=\{j:\mathrm{PIP}_j>\tfrac12\}$, $J_0=\{j:\mathrm{PIP}_j=\tfrac12\}$, $N_+=|J_+|$ and $\ell=\min\{k_{\max},N_+\}$. Let $a^\ast\subseteq J_+$ be a set of $\ell$ coordinates with the largest PIPs, i.e. $|a^\ast|=\ell$ and $\min_{j\in a^\ast}\mathrm{PIP}_j\ge\max_{j\in J_+\setminus a^\ast}\mathrm{PIP}_j$ (with $\min\emptyset=+\infty$ and $\max\emptyset=-\infty$; any choice when there are ties at the cut). Then
$$
\rho_H(a^\ast)\le\rho_H(a)\qquad\text{for every }a\subseteq[p]\text{ with }|a|\le k_{\max},\tag{1.2}
$$
so $a^\ast$ minimises the posterior expected Hamming loss under the cap. The set of minimisers is $\{a^\ast\}$ if and only if **(U)**: when $N_+>k_{\max}\ge1$, the $k_{\max}$-th largest PIP in $J_+$ is strictly larger than the $(k_{\max}+1)$-th; and when $N_+<k_{\max}$, $J_0=\emptyset$. (When $N_+=k_{\max}$, $a^\ast=J_+$ is always the unique minimiser; when $k_{\max}=0$, $a^\ast=\emptyset$ is the only admissible action, hence the unique minimiser, and (U) is read as satisfied.)

*Proof.* Write $c_j=1-2\,\mathrm{PIP}_j$, so that by (1.1) $\rho_H(a)=\sum_j\mathrm{PIP}_j+\sum_{j\in a}c_j$ and (1.2) is equivalent to $\sum_{j\in a^\ast}c_j\le\sum_{j\in a}c_j$. Note $c_j<0$ on $J_+$, $c_j=0$ on $J_0$, $c_j>0$ elsewhere, and $c_j$ is a strictly decreasing function of $\mathrm{PIP}_j$, so "the $\ell$ largest PIPs in $J_+$" are "the $\ell$ smallest $c_j$ in $J_+$". Let $|a|\le k_{\max}$ and $a'=a\cap J_+$. Three inequalities:

(a) $\sum_{j\in a}c_j\ge\sum_{j\in a'}c_j$, since every removed term has $c_j\ge0$.

(b) $|a'|\le\min\{|a|,N_+\}\le\min\{k_{\max},N_+\}=\ell$.

(c) For $r\le\ell$, the sum of any $r$ of the numbers $\{c_j:j\in J_+\}$ is at least the sum of the $r$ smallest of them, which is at least the sum of the $\ell$ smallest, because the $\ell-r$ further terms are negative. Applied with $r=|a'|$: $\sum_{j\in a'}c_j\ge\sum_{j\in a^\ast}c_j$ (the sum of the $\ell$ smallest $c_j$ in $J_+$ is $\sum_{j\in a^\ast}c_j$ whatever choice was made at a tie, since tied values contribute equally).

Together, $\sum_{j\in a}c_j\ge\sum_{j\in a^\ast}c_j$, which is (1.2); $a^\ast$ itself satisfies $|a^\ast|=\ell\le k_{\max}$.

*Uniqueness.* Let $a\ne a^\ast$ with $|a|\le k_{\max}$ be another minimiser. Then the two sum inequalities (a) and (c) hold with equality. Equality in (a) forces $a\setminus J_+\subseteq J_0$. Equality in (c) forces $|a'|=\ell$ (if $|a'|<\ell$ the $\ell-|a'|$ extra terms are strictly negative) and that $a'$ has the same multiset of $c$-values as $a^\ast$, which for $a'\ne a^\ast$ requires a tie at the cut with $N_+>\ell$, i.e. $N_+>k_{\max}$, and $\ell=k_{\max}\ge1$ (if $k_{\max}=0$ then $a'=\emptyset=a^\ast$). If $a'=a^\ast$ then $a\setminus J_+\ne\emptyset$, so $J_0\ne\emptyset$ and $|a|=\ell+|a\setminus J_+|\le k_{\max}$ forces $\ell<k_{\max}$, i.e. $N_+<k_{\max}$. So a second minimiser exists only if (U) fails. Conversely, if $N_+>k_{\max}$ and there is a tie at the cut, exchanging a tied element of $a^\ast$ for a tied element outside gives a second minimiser; if $N_+<k_{\max}$ and $j_0\in J_0$, then $a^\ast\cup\{j_0\}$ has size $\le k_{\max}$ and the same $\rho_H$. $\square$

**Example 1.4 (the cap can bind).** Let $p=3$, $k_{\max}=2$ and let $\pi$ be uniform on the three pairs $\{1,2\},\{1,3\},\{2,3\}$. Then $\mathrm{PIP}_j=\tfrac23$ for all $j$, the median model is $\{1,2,3\}$, of size $3>k_{\max}$, with $\rho_H=2-1=1$; under the cap, $\ell=2$ and every pair is a minimiser, with $\rho_H=2-\tfrac23=\tfrac43$. This $\pi$ is not itself a posterior of the form of Section 0.1 (a posterior is positive on all of $\mathcal S$), but the theorems of this section use nothing but the PIPs, and genuine posteriors behave in the same way: with an orthogonal standardised design ($n\ge3$, $X^\top X=nI_3$), the $\mathrm{BB}(1,3)$ prior, $k_{\max}=2$ and a response $y$ with equal strong effects on the three columns, the symmetry of the design and of $y$ gives equal PIPs, and a strong signal pushes the posterior onto the three pairs, so $\mathrm{PIP}_j\to\tfrac23$ for all $j$ and the median model has three elements. (The check script exhibits such an instance with $n=40$, exact PIPs $0.6666$, and brute-forces (1.2) on it, on random posteriors and on the posterior of a small correlated design.)

**Remark 1.5 (when the cap binds).** Let $k_{\max}\ge1$ (for $k_{\max}=0$, $\pi=\delta_\emptyset$, $N_+=0$ and nothing binds). $\sum_j\mathrm{PIP}_j=\mathbb E_\pi|S|\le k_{\max}$ because $\pi$ is supported on $\mathcal S$. If $N_+\ge1$ then $\sum_{j\in J_+}\mathrm{PIP}_j>N_+/2$, so $N_+<2k_{\max}$ (and this also holds when $N_+=0$): the capped minimiser differs from the median model only when $k_{\max}<N_+<2k_{\max}$, and then it drops the $N_+-k_{\max}$ coordinates of $J_+$ with the smallest PIPs. In the draft's phrase, "keeps the $\min\{k_{\max},N_+\}$ coordinates with the largest $\mathrm{PIP}_j$" is exactly $a^\ast$; the words "with the largest PIPs" must be read inside $J_+$, which is automatic since $\ell\le N_+$.

---

## 2. Proposition P8: certificates and evidence bounds

### 2.1 The shrinkage floor, for every model size

Let $h(\lambda)=\dfrac{(n+1)\lambda+1}{\lambda+1}$ for $\lambda\ge0$. Then $h(0)=1$, $h'(\lambda)=n/(\lambda+1)^2>0$, so $h$ is strictly increasing, and $h(\lambda)<n+1$ for every $\lambda\ge0$ (since $(n+1)\lambda+1<(n+1)(\lambda+1)$).

**Lemma 2.1 (shrinkage floor; the draft's (eq:floor)).** Let $S\subseteq[p]$ with $k=|S|\ge1$, and let $\lambda_1,\dots,\lambda_k\ge0$ be the eigenvalues of $G_S$.
(a) $D_S=\prod_{i=1}^kf(\lambda_i)$; hence $1\le D_S<(n+1)^k$, and $D_S>1$ unless $G_S=0$ (which standardised columns exclude).
(b) Put $R_S=nX_SH_S^{-1}X_S^\top$ ($n\times n$). Then $t_S=y^\top R_Sy$, $R_S$ is symmetric positive semidefinite, and $0\preceq R_S\preceq\tfrac n{n+1}P_S$. Consequently
$$
0\le t_S\le\tfrac n{n+1}\|P_Sy\|^2\le\tfrac n{n+1}\,y^\top y,\qquad Q_S\ge y^\top y-\tfrac n{n+1}\|P_Sy\|^2\ge\frac{y^\top y}{n+1}\ge0 .
$$
Both statements hold for every $k$, including $k>n$ (where $G_S$ is singular).

*Proof.* (a) Let $G_S=\sum_i\lambda_iv_iv_i^\top$ be a spectral decomposition ($v_i$ orthonormal in $\mathbb R^k$). Then $H_S=\sum_i((n+1)\lambda_i+1)v_iv_i^\top$ and $G_S+I_k=\sum_i(\lambda_i+1)v_iv_i^\top$, so $\det H_S=\prod_i((n+1)\lambda_i+1)$ and $\det(G_S+I_k)=\prod_i(\lambda_i+1)$, and $D_S=\prod_ih(\lambda_i)$. The bounds follow from $1=h(0)\le h(\lambda_i)<n+1$, with $h(\lambda_i)=1$ iff $\lambda_i=0$; $G_S=0$ is impossible when $k\ge1$ and $\|x_j\|^2=n>0$ (the diagonal of $G_S$ is $n$).

(b) $t_S=n\,z_S^\top H_S^{-1}z_S=n\,y^\top X_SH_S^{-1}X_S^\top y=y^\top R_Sy$. By the push-through identity (F-b) with $A=X_S$ and $c=n+1$, $X_SH_S^{-1}=X_S\big((n+1)X_S^\top X_S+I_k\big)^{-1}=\big((n+1)X_SX_S^\top+I_n\big)^{-1}X_S$, so
$$
R_S=n\big((n+1)\Gamma_S+I_n\big)^{-1}\Gamma_S,\qquad \Gamma_S=X_SX_S^\top\ (n\times n,\ \text{symmetric positive semidefinite}).
$$
Let $\Gamma_S=\sum_{l=1}^n\mu_lu_lu_l^\top$ be a spectral decomposition, $\mu_l\ge0$. Then $((n+1)\Gamma_S+I_n)^{-1}=\sum_l((n+1)\mu_l+1)^{-1}u_lu_l^\top$ and
$$
R_S=\sum_{l=1}^n g(\mu_l)\,u_lu_l^\top,\qquad g(\mu)=\frac{n\mu}{(n+1)\mu+1}\in\Big[0,\frac n{n+1}\Big),\quad g(\mu)=0\iff\mu=0 .
$$
So $R_S$ is symmetric positive semidefinite with $t_S\ge0$. The column span of $\Gamma_S=X_SX_S^\top$ equals that of $X_S$ (for any matrix $A$, $\ker(AA^\top)=\ker(A^\top)$, so $\mathrm{col}(AA^\top)=\ker(AA^\top)^\perp=\ker(A^\top)^\perp=\mathrm{col}(A)$), and it is spanned by the $u_l$ with $\mu_l>0$; hence $P_S=\sum_{l:\mu_l>0}u_lu_l^\top$ and
$$
R_S=\sum_{l:\mu_l>0}g(\mu_l)u_lu_l^\top\preceq\frac n{n+1}\sum_{l:\mu_l>0}u_lu_l^\top=\frac n{n+1}P_S .
$$
Thus $t_S=y^\top R_Sy\le\tfrac n{n+1}y^\top P_Sy=\tfrac n{n+1}\|P_Sy\|^2\le\tfrac n{n+1}\|y\|^2$ ($P_S$ is an orthogonal projection), and the bounds on $Q_S=y^\top y-t_S$ follow. $\square$

*Note on the draft's one-line justification.* The nonzero eigenvalues of $\Gamma_S=X_SX_S^\top$ and of $G_S=X_S^\top X_S$ coincide, so the draft's "eigenvalues $n\lambda/((n+1)\lambda+1)$, $\lambda$ over the eigenvalues of $G_S$" lists the nonzero eigenvalues of $R_S$ correctly (padded with zeros when $k<n$, with the zero eigenvalues of $G_S$ dropped when $k>n$); the argument above is the same one, written to cover $k>n$ explicitly.

### 2.2 Certificates from a visited set

**Theorem 2.2 (P8(i)–(ii)).** Let $V\subseteq2^{[p]}$ be nonempty. (i) $Z_V\le Z$, with equality if and only if $V\supseteq\mathcal S$. (ii) If $U\ge Z$ then, for every $j\in[p]$,
$$
\frac{A_j}U\le\frac{A_j}Z\le\mathrm{PIP}_j\le1-\frac{B_j}Z\le1-\frac{B_j}U .
$$

*Proof.* (i) $Z-Z_V=\sum_{S\notin V}p(S)m(S)\ge0$, as every term is $\ge0$; it is $0$ iff no $S\in\mathcal S$ lies outside $V$, since $p(S)m(S)>0$ exactly on $\mathcal S$. (ii) $Z\,\mathrm{PIP}_j=\sum_{S\ni j}p(S)m(S)\ge\sum_{S\in V,\,S\ni j}p(S)m(S)=A_j$, and $Z(1-\mathrm{PIP}_j)=\sum_{S\not\ni j}p(S)m(S)\ge\sum_{S\in V,\,S\not\ni j}p(S)m(S)=Z_V-A_j=B_j$. Dividing by $Z>0$ gives the two inner inequalities; the outer ones follow from $0<Z\le U$ and $A_j,B_j\ge0$. $\square$

**Theorem 2.3 (P8(iii)).** Let $V$ be nonempty, let $U\ge Z$, and suppose $\hat S\in\arg\max_{S\in V}p(S)m(S)$ satisfies $U-Z_V<p(\hat S)m(\hat S)$. Then every global maximiser of $S\mapsto p(S)m(S)$ lies in $V$, so $\arg\max_{S\subseteq[p]}p(S)m(S)=\arg\max_{S\in V}p(S)m(S)$; in particular $\hat S$ is a global maximiser, and the HPM over $V$ is the global HPM. If $\hat S$ is the HPM over $V$ (for instance if $\arg\max_V$ is a singleton), then $\hat S$ is the global HPM.

*Proof.* For $S\notin V$: $p(S)m(S)\le\sum_{S'\notin V}p(S')m(S')=Z-Z_V\le U-Z_V<p(\hat S)m(\hat S)$. So no model outside $V$ attains the maximum over $V$, let alone the global maximum, and $\max_{S\subseteq[p]}p(S)m(S)=\max\{\max_V,\ \max_{V^c}\}=\max_V=p(\hat S)m(\hat S)$ (with $\max_{V^c}=-\infty$ when $V^c=\emptyset$); the two argmax sets coincide. The HPM over $V$ and the global HPM are the $\prec$-first elements of the same set. $\square$

**Example 2.3a (the literal (iii) fails with ties, or without $U\ge Z$).** Let $n=p=1$, $X=(1)$ (standardised: $\|x_1\|^2=1=n$), $y=0$ and $k_{\max}=1$. Then $Q_\emptyset=Q_{\{1\}}=0$ and $D_{\{1\}}=h(1)=\tfrac32$ (Lemma 2.1(a) with $G_{\{1\}}=(1)$), so $m(\{1\})=m(\emptyset)\sqrt{2/3}$.
(a) *Ties.* Take $w(0)=1$ and $w(1)=\sqrt{3/2}$. Then $p(\emptyset)m(\emptyset)=p(\{1\})m(\{1\})$: both models are global maximisers, and with the order $\emptyset\prec\{1\}$ the global HPM is $\emptyset$. Take $V=\{\emptyset,\{1\}\}$, $U=Z$ and $\hat S=\{1\}\in\arg\max_V$. The hypothesis $U-Z_V=0<p(\hat S)m(\hat S)$ holds, but $\hat S$ is not the global HPM. Theorem 2.3's conclusion does hold: $\hat S$ is a global maximiser, and the HPM over $V$, which is $\emptyset$, is the global HPM.
(b) *$U<Z$.* Take $w(0)=w(1)=1$, so that $p(\emptyset)m(\emptyset)>p(\{1\})m(\{1\})>0$ and the global HPM is $\emptyset$. Take $V=\{\{1\}\}$, $\hat S=\{1\}$ and $U=Z_V<Z$. Then $U-Z_V=0<p(\hat S)m(\hat S)$, but $\hat S$ is not even a global maximiser. So the $U$ of (iii) must be the $U\ge Z$ of (ii).
(Both found by the round-1 reviewers; checked numerically in the script.)

### 2.3 The universal and the size-aware evidence bounds

**Theorem 2.4 (P8(iv) and (iv′)).**
(iv) $Z\le C_n\big(2b_0+y^\top y/(n+1)\big)^{-\nu}=:U_{\rm univ}$, and
$$
\frac{U_{\rm univ}}{m(\emptyset)}=\Big(\frac{2b_0+y^\top y}{2b_0+y^\top y/(n+1)}\Big)^{\nu}\in\big(1,(n+1)^{\nu}\big)\quad(y\ne0),\qquad\nu=a_0+\tfrac n2,
$$
and this ratio increases to $(n+1)^{\nu}=(n+1)^{n/2}(n+1)^{a_0}$ as $b_0/y^\top y\downarrow0$.
(iv′) Suppose $\lambda_{\min}(G_{[p]})\ge n\varphi^2>0$ (this forces $p\le n$), put $\varrho=h(n\varphi^2)=\dfrac{(n+1)n\varphi^2+1}{n\varphi^2+1}\in(1,n+1)$, $P=P_{[p]}$ and $\mathrm{RSS}_{[p]}=\|(I-P)y\|^2$. Then for every $S\subseteq[p]$,
$$
Q_S\ \ge\ y^\top y-\tfrac n{n+1}\|Py\|^2=\mathrm{RSS}_{[p]}+\frac{\|Py\|^2}{n+1}\qquad\text{and}\qquad D_S\ \ge\ \prod_{i=1}^{|S|}h\big(\lambda_i(G_{[p]})\big)\ \ge\ \varrho^{|S|},\tag{2.1}
$$
where $\lambda_1(G_{[p]})\le\dots\le\lambda_p(G_{[p]})$, and consequently
$$
Z\ \le\ C_n\Big(2b_0+\mathrm{RSS}_{[p]}+\frac{\|Py\|^2}{n+1}\Big)^{-\nu}\sum_{S\in\mathcal S}p(S)\prod_{i=1}^{|S|}h\big(\lambda_i(G_{[p]})\big)^{-1/2}\ \le\ C_n\Big(2b_0+\mathrm{RSS}_{[p]}+\frac{\|Py\|^2}{n+1}\Big)^{-\nu}\sum_{k=0}^{k_{\max}}p(|S|=k)\,\varrho^{-k/2}=:U_{\rm size}.\tag{2.2}
$$
The first inequality in (2.1) holds for every design, without the eigenvalue hypothesis; and $U_{\rm size}\le U_{\rm univ}$ always.

*Proof.* (iv) By Lemma 2.1(a), $D_S^{-1/2}\le1$ for every $S$ (and $D_\emptyset=1$); by Lemma 2.1(b), $Q_S\ge y^\top y/(n+1)$ for every $S$ (and $Q_\emptyset=y^\top y\ge y^\top y/(n+1)$); since $\nu>0$, $x\mapsto(2b_0+x)^{-\nu}$ is decreasing on $[0,\infty)$. Hence
$$
Z=C_n\sum_{S\in\mathcal S}p(S)D_S^{-1/2}(2b_0+Q_S)^{-\nu}\le C_n\big(2b_0+y^\top y/(n+1)\big)^{-\nu}\sum_{S\in\mathcal S}p(S)=U_{\rm univ},
$$
using $\sum_{S\in\mathcal S}p(S)=1$. The ratio to $m(\emptyset)=C_n(2b_0+y^\top y)^{-\nu}$ is as displayed. For $y\ne0$ the base exceeds $1$ because $y^\top y>y^\top y/(n+1)$, and it is below $n+1$ because $2b_0+y^\top y<(n+1)2b_0+y^\top y$. Writing the base as $(n+1)\cdot\dfrac{2b_0+y^\top y}{2b_0(n+1)+y^\top y}$, the second factor increases to $1$ as $b_0/y^\top y\downarrow0$.

(iv′) *First inequality of (2.1).* By Lemma 2.1(b), $Q_S\ge y^\top y-\tfrac n{n+1}\|P_Sy\|^2$. Since $\mathrm{col}(X_S)\subseteq\mathrm{col}(X)$, $P_SP=P_S$ and $\|P_Sy\|=\|P_SPy\|\le\|Py\|$. Hence $Q_S\ge y^\top y-\tfrac n{n+1}\|Py\|^2$, and $y^\top y=\|Py\|^2+\|(I-P)y\|^2$ (Pythagoras) turns the right side into $\mathrm{RSS}_{[p]}+\|Py\|^2/(n+1)$. Nothing about $\lambda_{\min}$ was used.

*Second inequality of (2.1).* Let $k=|S|\ge1$ (for $S=\emptyset$ both sides are $1=\varrho^0$). $G_S$ is the $k\times k$ principal submatrix of $G_{[p]}=X^\top X$ with rows and columns in $S$. By Cauchy interlacing (F-a), $\lambda_i(G_S)\ge\lambda_i(G_{[p]})$ for $i=1,\dots,k$ (both in increasing order), and $\lambda_i(G_{[p]})\ge\lambda_1(G_{[p]})=\lambda_{\min}(G_{[p]})\ge n\varphi^2$. Since $h$ is increasing, Lemma 2.1(a) gives $D_S=\prod_{i=1}^kf(\lambda_i(G_S))\ge\prod_{i=1}^kf(\lambda_i(G_{[p]}))\ge h(n\varphi^2)^k=\varrho^k$. That $\varrho\in(1,n+1)$ follows from $h(0)=1$, $h$ strictly increasing, $n\varphi^2>0$ and $h<n+1$; with standardised columns, $\lambda_{\min}(G_{[p]})\le\operatorname{tr}G_{[p]}/p=n$, so in fact $\varrho\le h(n)=n+\tfrac1{n+1}$. The hypothesis $\lambda_{\min}(G_{[p]})>0$ forces $\operatorname{rank}G_{[p]}=p$, and $\operatorname{rank}G_{[p]}=\operatorname{rank}X\le n$, so $p\le n$.

*The bound (2.2).* Insert both parts of (2.1) into $Z=C_n\sum_{S\in\mathcal S}p(S)D_S^{-1/2}(2b_0+Q_S)^{-\nu}$, using again that $(2b_0+x)^{-\nu}$ is decreasing in $x$ and that $D^{-1/2}$ is decreasing in $D$; then group the terms of the second sum by $|S|=k$, which gives $\sum_{k=0}^{k_{\max}}\varrho^{-k/2}\sum_{|S|=k}p(S)=\sum_kp(|S|=k)\varrho^{-k/2}$ (the models of size $k\le k_{\max}$ are exactly the elements of $\mathcal S$ of that size, and $k_{\max}\le p$).

*$U_{\rm size}\le U_{\rm univ}$.* $\mathrm{RSS}_{[p]}+\|Py\|^2/(n+1)\ge(\mathrm{RSS}_{[p]}+\|Py\|^2)/(n+1)=y^\top y/(n+1)$, so the first factor of $U_{\rm size}$ is at most that of $U_{\rm univ}$; and $\sum_kp(|S|=k)\varrho^{-k/2}\le\sum_kp(|S|=k)=1$ because $\varrho\ge1$. $\square$

**Remark 2.5 (reading (iv′)).** Relative to $m(\emptyset)$, exactly,
$$
\frac{U_{\rm size}}{m(\emptyset)}=\Big(\frac{2b_0+y^\top y}{2b_0+y^\top y-\tfrac n{n+1}\|Py\|^2}\Big)^{\nu}\sum_{k\le k_{\max}}p(|S|=k)\varrho^{-k/2}
=\Big(1-\frac{n}{n+1}\,\frac{\|Py\|^2}{2b_0+y^\top y}\Big)^{-\nu}\sum_{k\le k_{\max}}p(|S|=k)\varrho^{-k/2},
$$
and for $y\ne0$, as $b_0/y^\top y\to0$, the first factor tends to $\big((n+1)/(1+n(1-R^2_{[p]}))\big)^{\nu}$ with $R^2_{[p]}=\|Py\|^2/y^\top y$ the full model's coefficient of determination; this limit lies between $1$ ($R^2_{[p]}=0$) and $(n+1)^{\nu}$ ($R^2_{[p]}=1$) and is close to $(1-R^2_{[p]})^{-\nu}$ only when $n(1-R^2_{[p]})\gg1$. So, relative to $m(\emptyset)$ and for small $b_0$, the size-aware bound improves on $U_{\rm univ}$ through its first factor only when the full model's $R^2$ is well below $1$; the second factor adds the size penalty. This says nothing about $U_{\rm size}/Z$, the ratio that matters for a certificate: it can be close to $1$ even when $R^2_{[p]}=1$ (for instance $n=2$, $p=k_{\max}=1$, $X=(1,1)^\top$, $y=\varepsilon(1,1)^\top$, $w(0)=w(1)$: $R^2_{[p]}=1$, the $D_S$ bound is exact since $\lambda_{\min}(G_{[p]})=n$, $Q_{\{1\}}=\tfrac67\varepsilon^2$ against the bound $\tfrac23\varepsilon^2$, and $U_{\rm size}/Z\to1$ as $\varepsilon\to0$; checked numerically). The intermediate bound in (2.2) (the product of $h(\lambda_i(G_{[p]}))$ over the $|S|$ smallest eigenvalues of $G_{[p]}$) is sharper than $U_{\rm size}$ and costs one eigendecomposition; it is not in the draft. Which bound is "useful" is a numerical matter and not part of the statement; the check script reports $U_{\rm univ}/Z$ and $U_{\rm size}/Z$ on a small instance.

### 2.4 Pruning a scored set

**Theorem 2.6 (P8(v)).** Let $W$ be a nonempty finite set of models, $M_W=\max_{S\in W}\log\{p(S)m(S)\}$ (with $\log0=-\infty$; $M_W>-\infty$ iff $W\cap\mathcal S\ne\emptyset$), $\Delta\in\mathbb R$, and $V=\{S\in W:\log p(S)m(S)\ge M_W-\Delta\}$. Then
$$
0\le Z_W-Z_V\le|W\setminus V|\,e^{M_W-\Delta},
$$
with strict inequality on the right when $W\setminus V\ne\emptyset$ (and $0=0$ otherwise). If $\Delta\ge0$ and $M_W>-\infty$, then $V\ne\emptyset$ (it contains every maximiser over $W$).

*Proof.* $V\subseteq W$, so $Z_W-Z_V=\sum_{S\in W\setminus V}p(S)m(S)\ge0$. For $S\in W\setminus V$, $\log p(S)m(S)<M_W-\Delta$, i.e. $p(S)m(S)<e^{M_W-\Delta}$ (this includes $p(S)m(S)=0$, i.e. $S\notin\mathcal S$, for which the logarithm is $-\infty$). Summing over the $|W\setminus V|$ terms gives the bound, strictly if there is at least one term. If $\Delta\ge0$, a maximiser $S^\ast\in W$ has $\log p(S^\ast)m(S^\ast)=M_W\ge M_W-\Delta$, so $S^\ast\in V$. $\square$

*Use.* With $U\ge Z$ available (Theorem 2.4) and $V\ne\emptyset$ (guaranteed when $\Delta\ge0$ and $M_W>-\infty$), Theorems 2.2–2.3 apply to the pruned set $V$ with $Z_V\ge Z_W-|W\setminus V|e^{M_W-\Delta}$, which is how the draft intends (v) to be read; no further claim is made.

---

## 3. Proposition P9: truncation and decision agreement

**Lemma 3.1 (total variation on a finite set).** Let $\mu,\mu'$ be probabilities on a finite set $E$. Then
$$
\sup_{A\subseteqE}|\mu(A)-\mu'(A)|=\sum_{\omega\inE}\big(\mu(\omega)-\mu'(\omega)\big)^+=\sum_{\omega\inE}\big(\mu'(\omega)-\mu(\omega)\big)^+,
$$
and the supremum is attained at $A_+=\{\omega:\mu(\omega)>\mu'(\omega)\}$.

*Proof.* For any $A$, $\mu(A)-\mu'(A)=\sum_{\omega\in A}(\mu-\mu')(\omega)\le\sum_{\omega\in A}(\mu-\mu')^+(\omega)\le\sum_{\omega\inE}(\mu-\mu')^+(\omega)$, with equality throughout at $A=A_+$. Since $\sum_\omega(\mu-\mu')(\omega)=1-1=0$, $\sum(\mu-\mu')^+=\sum(\mu-\mu')^-=\sum(\mu'-\mu)^+$, so the same bound holds for $\mu'(A)-\mu(A)$, and $|\mu(A)-\mu'(A)|\le\sum(\mu-\mu')^+$ for every $A$, with equality at $A_+$. $\square$

**Theorem 3.2 (P9(i), with the exact relation).** Let $V\subseteq2^{[p]}$ with $\pi(V)>0$, $f=\pi(V^c)\in[0,1)$, and $\pi(\cdot\mid V)=\pi(\cdot\cap V)/(1-f)$. Then:
(a) for every $A\subseteq2^{[p]}$, $\pi(A)-\pi(A\mid V)=\pi(A\cap V^c)-\dfrac f{1-f}\,\pi(A\cap V)\in[-f,f]$, so $\|\pi-\pi(\cdot\mid V)\|_{\rm TV}=\sup_A|\pi(A)-\pi(A\mid V)|=f$, attained at $A=V^c$ and at $A=V$;
(b) for every $j$, $\mathrm{PIP}_j=(1-f)\,\mathrm{PIP}_{j,V}+\pi(\mathcal A_j\cap V^c)$ with $0\le\pi(\mathcal A_j\cap V^c)\le f$; hence
$$
(1-f)\,\mathrm{PIP}_{j,V}\ \le\ \mathrm{PIP}_j\ \le\ (1-f)\,\mathrm{PIP}_{j,V}+f,\qquad -f\,\mathrm{PIP}_{j,V}\ \le\ \mathrm{PIP}_j-\mathrm{PIP}_{j,V}\ \le\ f\,(1-\mathrm{PIP}_{j,V}),
$$
and in particular $|\mathrm{PIP}_j-\mathrm{PIP}_{j,V}|\le f$.

*Proof.* (a) $\pi(A)=\pi(A\cap V)+\pi(A\cap V^c)$ and $\pi(A\mid V)=\pi(A\cap V)/(1-f)$, so $\pi(A)-\pi(A\mid V)=\pi(A\cap V^c)-\pi(A\cap V)\big(\tfrac1{1-f}-1\big)=\pi(A\cap V^c)-\tfrac f{1-f}\pi(A\cap V)$. The first term lies in $[0,\pi(V^c)]=[0,f]$ and the second in $[0,\tfrac f{1-f}\pi(V)]=[0,f]$, so the difference lies in $[-f,f]$; it equals $f$ at $A=V^c$ and $-f$ at $A=V$. Hence the supremum of $|\cdot|$ is $f$. (The same follows from Lemma 3.1: $(\pi-\pi(\cdot\mid V))^+$ equals $\pi$ on $V^c$, where $\pi(\cdot\mid V)=0$, and vanishes on $V$, where $\pi(S)\le\pi(S)/(1-f)$; its sum is $\pi(V^c)=f$.)
(b) Apply the decomposition in (a) to $A=\mathcal A_j$: $\mathrm{PIP}_j=\pi(\mathcal A_j\cap V)+\pi(\mathcal A_j\cap V^c)=(1-f)\pi(\mathcal A_j\mid V)+\pi(\mathcal A_j\cap V^c)$ and $0\le\pi(\mathcal A_j\cap V^c)\le\pi(V^c)=f$. Subtracting $\mathrm{PIP}_{j,V}$ gives $\mathrm{PIP}_j-\mathrm{PIP}_{j,V}=\pi(\mathcal A_j\cap V^c)-f\,\mathrm{PIP}_{j,V}\in[-f\,\mathrm{PIP}_{j,V},\,f(1-\mathrm{PIP}_{j,V})]\subseteq[-f,f]$. $\square$

*Consistency with P8(ii).* Since $A_j/Z=\pi(\mathcal A_j\cap V)=(1-f)\mathrm{PIP}_{j,V}$ and $1-B_j/Z=1-\pi(V\setminus\mathcal A_j)=1-(1-f)(1-\mathrm{PIP}_{j,V})=(1-f)\mathrm{PIP}_{j,V}+f$, the two-sided bound in (b) is Theorem 2.2(ii) with $U=Z$; P9(i) is the special case of that certificate in which the exact missing mass is known.

**Theorem 3.3 (P9(ii)).** Let $\hat\pi_1,\dots,\hat\pi_p\in\mathbb R$ and $\delta\ge0$ satisfy $\max_j|\hat\pi_j-\mathrm{PIP}_j|\le\delta<\min_j|\mathrm{PIP}_j-\tfrac12|$. Then $\{j:\hat\pi_j>\tfrac12\}=\{j:\mathrm{PIP}_j>\tfrac12\}$. The strict inequality cannot be weakened to $\delta\le\min_j|\mathrm{PIP}_j-\tfrac12|$: if $\mathrm{PIP}_{j_0}-\tfrac12=\delta>0$ for some $j_0$, then $\hat\pi_{j_0}=\tfrac12$ is within $\delta$ of $\mathrm{PIP}_{j_0}$ and drops $j_0$ from the median model.

*Proof.* The hypothesis implies $|\mathrm{PIP}_j-\tfrac12|>\delta\ge0$ for every $j$, so no $\mathrm{PIP}_j$ equals $\tfrac12$. If $\mathrm{PIP}_j>\tfrac12$ then $\mathrm{PIP}_j-\tfrac12>\delta$ and $\hat\pi_j\ge\mathrm{PIP}_j-\delta>\tfrac12$. If $\mathrm{PIP}_j<\tfrac12$ then $\tfrac12-\mathrm{PIP}_j>\delta$ and $\hat\pi_j\le\mathrm{PIP}_j+\delta<\tfrac12$. So $\hat\pi_j>\tfrac12$ iff $\mathrm{PIP}_j>\tfrac12$, coordinate by coordinate. $\square$

(The sentence "Here $\|\cdot\|_{\rm TV}=\sup_A|\cdot|$", printed in (ii), concerns (i); Theorem 3.2 uses exactly that definition. Flag in Section 6.)

**Theorem 3.4 (P9(iii)).** Let $V\subseteq2^{[p]}$ be nonempty, let $S^\ast$ be the global HPM and $S^\ast_V$ the HPM over $V$, both defined with the same fixed total order $\prec$ (Section 0.1). Then $S^\ast_V=S^\ast$ if and only if $S^\ast\in V$.

*Proof.* ($\Rightarrow$) $S^\ast_V\in V$ by definition. ($\Leftarrow$) Let $S^\ast\in V$. Write $\mathcal M=\arg\max_{S\subseteq[p]}p(S)m(S)$ and $\mathcal M_V=\arg\max_{S\in V}p(S)m(S)$. Since $S^\ast\in\mathcal M\cap V$, the maximum over $V$ equals the global maximum, so $\mathcal M_V=\mathcal M\cap V$. $S^\ast$ is the $\prec$-first element of $\mathcal M$ and belongs to the subset $\mathcal M\cap V$, hence it is the $\prec$-first element of $\mathcal M\cap V=\mathcal M_V$, which is $S^\ast_V$. $\square$

*What "fixed tie rule" must mean.* The proof uses one property of the rule: for nonempty $B\subseteq C$, if the rule's choice from $C$ lies in $B$, it is also its choice from $B$. A fixed total order has it. A choice function that does not depend on $V$ but is not induced by a total order need not (for instance $c(\{A,B,C\})=A$ but $c(\{A,B\})=B$), and neither does a rule that depends on $V$ (for instance "the first tied model in the order the run visited them"); in either case "$\Leftarrow$" can fail when $\mathcal M$ has two elements in $V$.

---

## 4. Proposition P10: the visited-set estimator and the confidence bound

### 4.1 The probability model

The data $y$ are fixed throughout, so $\pi=\pi(\cdot\mid y)$, $Z$, $p(S)m(S)$ are constants. A probability space $(\Omega,\mathcal H,\mathbb P)$ carries:

- the randomness $\zeta$ of the *construction* of $V$ (the SMC run or runs, a pilot, any auxiliary randomness), and the visited set $V=V(y,\zeta)\subseteq2^{[p]}$, a function of $\zeta$ taking values in the finite set of subsets of $2^{[p]}$, with $Z_V>0$ (i.e. $V\cap\mathcal S\ne\emptyset$) for every $\zeta$;
- the *validation draws* $\Sigma_1,\dots,\Sigma_M$ ($M\ge1$), which conditionally on $\zeta$ are i.i.d. with law $\pi$. Equivalently: $(\Sigma_m)_{m\le M}$ are i.i.d. $\pi$ and independent of $\zeta$. This is the draft's "exact posterior draws, independent of the construction of $V$ given $y$".

Put $f=f(V)=\pi(V^c)$ (a random variable through $V$, constant given $\zeta$), $K_{\rm in}=\#\{m:\Sigma_m\in V\}$ and $K_{\rm out}=M-K_{\rm in}$. "Frozen $V$" means "conditionally on $\zeta$"; a statement holds *unconditionally* if it holds after $\zeta$ is integrated out. Conditional probabilities given $\zeta$ are written $\mathbb P(\cdot\mid\zeta)$; since $\zeta$ ranges over a general space, "for every $\zeta$" means "for $\mathbb P$-almost every $\zeta$".

**Lemma 4.1.** (a) $Z=Z_V/(1-f)$, and $1-f=\pi(V)=Z_V/Z\in(0,1]$. (b) Conditionally on $\zeta$, $K_{\rm out}\sim\mathrm{Bin}(M,f)$ and $K_{\rm in}\sim\mathrm{Bin}(M,1-f)$; in particular $\mathbb P(K_{\rm in}=0\mid\zeta)=f^M$.

*Proof.* (a) $Z_V=\sum_{S\in V}p(S)m(S)=Z\pi(V)=Z(1-f)$; $Z_V>0$ gives $\pi(V)>0$. (b) Given $\zeta$, $V$ is a fixed set and the indicators $\mathbf 1\{\Sigma_m\in V^c\}$, $m\le M$, are i.i.d. Bernoulli with success probability $\pi(V^c)=f$. $\square$

**Lemma 4.2 (binomial facts).** Let $K\sim\mathrm{Bin}(M,q)$ with $q=1-f\in(0,1]$. Then
$$
\mathbb E\Big[\frac1{K+1}\Big]=\frac{1-f^{M+1}}{(M+1)q},\qquad
\mathbb E\Big[\frac1{\max(K,1)}\Big]=f^M+\sum_{k=1}^M\frac1k\binom Mkq^kf^{M-k},\qquad
\mathbb E\Big[\frac M{\max(K,1)}\Big]\ \ge\ Mf^M+\frac{(1-f^M)^2}{q}.
$$

*Proof.* First identity: $\binom Mk\frac1{k+1}=\frac1{M+1}\binom{M+1}{k+1}$, so $\mathbb E[1/(K+1)]=\frac1{(M+1)q}\sum_{k=0}^M\binom{M+1}{k+1}q^{k+1}f^{M-k}=\frac1{(M+1)q}\big[(q+f)^{M+1}-f^{M+1}\big]$ and $q+f=1$. Second: the definition of the expectation, with $\mathbb P(K=0)=f^M$. Third: on $\{K\ge1\}$, which has probability $1-f^M>0$, Jensen's inequality for the convex function $x\mapsto1/x$ under the conditional law gives $\mathbb E[1/K\mid K\ge1]\ge1/\mathbb E[K\mid K\ge1]=(1-f^M)/(Mq)$, because $\mathbb E[K\mid K\ge1]=\mathbb E[K]/\mathbb P(K\ge1)=Mq/(1-f^M)$ ($K=0$ contributes nothing to $\mathbb E[K]$). Hence $\mathbb E[M/\max(K,1)]=Mf^M+(1-f^M)\,\mathbb E[M/K\mid K\ge1]\ge Mf^M+(1-f^M)^2/q$. $\square$

### 4.2 The classical estimator and its safeguards: P10(i)

**Theorem 4.3 (P10(i)).** Let $\widehat Z_{\rm cl}=Z_VM/K_{\rm in}$ (with $x/0=+\infty$), $\widehat Z_{\max}=Z_VM/\max(K_{\rm in},1)$ and $\widehat Z_{+1}=Z_V(M+1)/(K_{\rm in}+1)$. Conditionally on $\zeta$ (so $f$, $Z_V$ are constants and $q=1-f$):
(a) If $f>0$: $\mathbb P(\widehat Z_{\rm cl}=+\infty\mid\zeta)=f^M>0$, so $\mathbb E[\widehat Z_{\rm cl}\mid\zeta]=+\infty$ and $\widehat Z_{\rm cl}$ has no finite moment of any order. If $f=0$: $K_{\rm in}=M$ almost surely and $\widehat Z_{\rm cl}=Z_V=Z$.
(b) $\widehat Z_{max}\le Z_VM$ and $\widehat Z_{+1}\le Z_V(M+1)$ are bounded, so all their moments are finite, and
$$
\mathbb E[\widehat Z_{max}\mid\zeta]=Z\,qM\Big[f^M+\sum_{k=1}^M\frac1k\binom Mkq^kf^{M-k}\Big],\qquad
\mathbb E[\widehat Z_{+1}\mid\zeta]=Z\,(1-f^{M+1}) .
$$
So $\widehat Z_{+1}$ has bias exactly $-Zf^{M+1}$ (downward, and $0$ iff $f=0$), while the bias of $\widehat Z_{\max}$ satisfies
$$
\mathbb E[\widehat Z_{max}\mid\zeta]-Z\ \ge\ Z\,f^M\big(Mq-2+f^M\big),
$$
which is $\ge0$ whenever $M(1-f)\ge2$; the sign is not fixed: for $M=1$, $\widehat Z_{\max}=Z_V$ surely and the bias is $-Zf\le0$.
(c) The same holds unconditionally with $f$ random: $\mathbb P(\widehat Z_{\rm cl}=+\infty)=\mathbb E[f^M]$, which is $>0$ as soon as $\mathbb P(f>0)>0$; $\mathbb E[\widehat Z_{+1}]=Z(1-\mathbb E[f^{M+1}])$.

*Proof.* (a) By Lemma 4.1(b), $\{\widehat Z_{\rm cl}=+\infty\}=\{K_{\rm in}=0\}$ has conditional probability $f^M$, positive when $f>0$; a random variable equal to $+\infty$ with positive probability has infinite expectation and no finite moments. If $f=0$ then $\Sigma_m\in V$ almost surely and $K_{\rm in}=M$, so $\widehat Z_{\rm cl}=Z_V=Z$ by Lemma 4.1(a).
(b) $\max(K_{\rm in},1)\ge1$ and $K_{\rm in}+1\ge1$ give the bounds. With $Z_V=Zq$ (Lemma 4.1(a)) and $K_{\rm in}\sim\mathrm{Bin}(M,q)$ given $\zeta$: $\mathbb E[\widehat Z_{max}\mid\zeta]=ZqM\,\mathbb E[1/\max(K_{\rm in},1)]$ and $\mathbb E[\widehat Z_{+1}\mid\zeta]=Zq(M+1)\mathbb E[1/(K_{\rm in}+1)]=Zq(M+1)\cdot\frac{1-f^{M+1}}{(M+1)q}=Z(1-f^{M+1})$, both by Lemma 4.2. For the sign bound, Lemma 4.2's third display gives $\mathbb E[\widehat Z_{max}\mid\zeta]\ge Zq\big[Mf^M+(1-f^M)^2/q\big]=Z\big[qMf^M+1-2f^M+f^{2M}\big]$, and subtracting $Z$ gives $Zf^M(qM-2+f^M)$, which is $\ge0$ when $qM\ge2$. For $M=1$, $\max(K_{\rm in},1)=1$, so $\widehat Z_{\max}=Z_V=Z(1-f)$.
(c) Take expectations over $\zeta$ (tower property); $\mathbb E[f^M]>0$ iff $f>0$ with positive probability. $\square$

*Reading.* The draft asks that the safeguard's bias "be stated"; the two displays do that. $\widehat Z_{+1}$ is the natural choice when a closed form is wanted (its conditional mean is $Z$ times $1-f^{M+1}$, the probability that at least one of $M+1$ draws lands in $V$); $\widehat Z_{\max}$ has a bias of either sign (positive also for some $(M,f)$ with $M(1-f)<2$, e.g. $M=2$, $f=\tfrac1{20}$: bias $+0.0426\,Z$). Neither is the object of (ii): the confidence bound $U_V$ below is not built from a point estimate.

### 4.3 The upper confidence bound: P10(ii)

**Definition 4.4.** A *$(1-\alpha)$ upper confidence bound for $f$ based on $K_{\rm out}$* is a map $f_U:\{0,1,\dots,M\}\to[0,1]$ such that, for every $f\in[0,1]$, if $K\sim\mathrm{Bin}(M,f)$ then $\mathbb P_f\big(f_U(K)\ge f\big)\ge1-\alpha$. "Reporting a finite bound" is the event $\{f_U(K_{\rm out})<1\}$.

**Lemma 4.5 (Clopper–Pearson upper bound).** Fix $\alpha\in(0,1)$ and $M\ge1$. For $x\in\{0,\dots,M-1\}$ let $F_x(f)=\mathbb P_f(K\le x)=\sum_{i=0}^x\binom Mif^i(1-f)^{M-i}$ ($K\sim\mathrm{Bin}(M,f)$). Then:
(a) for $x\le M-1$, $F_x$ is continuous and strictly decreasing on $[0,1]$ with $F_x(0)=1$ and $F_x(1)=0$, so $F_x(f)=\alpha$ has a unique root $f_U(x)\in(0,1)$; put $f_U(M)=1$;
(b) $x\mapsto f_U(x)$ is nondecreasing, $f_U(x)<1$ iff $x\le M-1$, $f_U(0)=1-\alpha^{1/M}$ and $f_U(M-1)=(1-\alpha)^{1/M}$;
(c) $f_U$ is a $(1-\alpha)$ upper confidence bound in the sense of Definition 4.4; in fact $\mathbb P_f(f_U(K)\ge f)>1-\alpha$ for every $f\in[0,1]$.

*Proof.* (a) $F_x$ is a polynomial, hence continuous; $F_x(0)=\mathbb P_0(K\le x)=1$ (then $K=0$) and $F_x(1)=\mathbb P_1(K\le x)=0$ for $x<M$ (then $K=M$). Strict decrease: let $0\le f<f'\le1$ and couple $K(f)=\sum_m\mathbf 1\{U_m\le f\}$, $K(f')=\sum_m\mathbf 1\{U_m\le f'\}$ with $U_1,\dots,U_M$ i.i.d. uniform on $[0,1]$; then $K(f)\le K(f')$ pointwise, so $\{K(f')\le x\}\subseteq\{K(f)\le x\}$ and $F_x(f)-F_x(f')=\mathbb P(K(f)\le x<K(f'))$. This is positive in every case. If $0<f<f'<1$: it is at least $\mathbb P(U_1,\dots,U_x\le f;\ U_{x+1}\in(f,f'];\ U_{x+2},\dots,U_M>f')=f^x(f'-f)(1-f')^{M-x-1}>0$. If $f'=1$: $K(f')=M>x$ surely, so the probability is $\mathbb P(K(f)\le x)\ge\mathbb P(K(f)=0)=(1-f)^M>0$ as $f<1$. If $f=0$ and $0<f'<1$: $K(f)=0\le x$ surely, so the probability is $\mathbb P(K(f')>x)\ge\binom M{x+1}f'^{\,x+1}(1-f')^{M-x-1}>0$ (the case $f=0$, $f'=1$ is covered by the previous case). The root exists and is unique by (F-g), and lies in $(0,1)$ since $\alpha\in(0,1)$.
(b) $F_x\le F_{x+1}$ pointwise (more terms), so $F_{x+1}(f_U(x))\ge F_x(f_U(x))=\alpha=F_{x+1}(f_U(x+1))$, and strict decrease of $F_{x+1}$ gives $f_U(x)\le f_U(x+1)$ for $x+1\le M-1$; $f_U(M-1)<1=f_U(M)$. The two values: $F_0(f)=(1-f)^M=\alpha$ gives $f=1-\alpha^{1/M}$; $F_{M-1}(f)=1-f^M=\alpha$ gives $f=(1-\alpha)^{1/M}$.
(c) Fix $f\in[0,1]$ and let $K\sim\mathrm{Bin}(M,f)$. On $\{f_U(K)<f\}$ we have $K\le M-1$ (since $f_U(M)=1\ge f$) and, by strict decrease of $F_K$, $F_K(f)<F_K(f_U(K))=\alpha$. Let $\mathcal X=\{x\le M-1:F_x(f)<\alpha\}$. Since $F_x(f)$ is nondecreasing in $x$, $\mathcal X$ is either empty or $\{0,1,\dots,x^\ast\}$ for $x^\ast=\max\mathcal X$. If empty, $\mathbb P_f(f_U(K)<f)=0$. Otherwise $\{f_U(K)<f\}\subseteq\{K\le x^\ast\}$ and $\mathbb P_f(f_U(K)<f)\le F_{x^\ast}(f)<\alpha$. In both cases $\mathbb P_f(f_U(K)\ge f)>1-\alpha$. $\square$

**Theorem 4.6 (P10(ii)).** Let $f_U$ be any $(1-\alpha)$ upper confidence bound in the sense of Definition 4.4, and $U_V=Z_V/(1-f_U(K_{\rm out}))$, with $U_V=+\infty$ when $f_U(K_{\rm out})=1$. Then:
(a) pointwise on $\Omega$, $\{Z\le U_V\}=\{f\le f_U(K_{\rm out})\}$;
(b) $\mathbb P(Z\le U_V\mid\zeta)\ge1-\alpha$ for every $\zeta$, hence $\mathbb P(Z\le U_V)\ge1-\alpha$ (unconditionally, after integrating over the construction of $V$); with Clopper–Pearson the inequalities are strict;
(c) *(conditional coverage can fail)* with the Clopper–Pearson bound of Lemma 4.5, for every $\zeta$ such that $f\in\big((1-\alpha)^{1/M},1\big)$:
$$
\mathbb P\big(Z\le U_V\ \big|\ \zeta,\ f_U(K_{\rm out})<1\big)=0\qquad\text{while}\qquad\mathbb P(Z\le U_V\mid\zeta)=f^M\ge1-\alpha ;
$$
still with Clopper–Pearson, for every $\zeta$ with $0<f<1$, $\mathbb P(Z\le U_V\mid\zeta,f_U<1)=\dfrac{\mathbb P(Z\le U_V\mid\zeta)-f^M}{1-f^M}$, which is below $1-\alpha$ whenever $\mathbb P(Z\le U_V\mid\zeta)<1-\alpha+\alpha f^M$; and for $0<f\le(1-\alpha)^{1/M}$ the conditional coverage is positive (it is $1$ when $f\le1-\alpha^{1/M}$), so $\big((1-\alpha)^{1/M},1\big)$ is exactly the set of $f$ on which it is $0$.

*Proof.* (a) By Lemma 4.1(a), $Z=Z_V/(1-f)$ with $Z_V>0$ and $1-f>0$. If $f_U(K_{\rm out})=1$ then $U_V=+\infty\ge Z$ and $f\le1=f_U(K_{\rm out})$: both events hold. If $f_U(K_{\rm out})<1$ then $Z\le U_V\iff\frac{Z_V}{1-f}\le\frac{Z_V}{1-f_U}\iff1-f_U\le1-f\iff f\le f_U$, since $Z_V>0$ and both denominators are positive.
(b) Given $\zeta$, $f$ is a constant and $K_{\rm out}\sim\mathrm{Bin}(M,f)$ (Lemma 4.1(b)), so by (a) and Definition 4.4, $\mathbb P(Z\le U_V\mid\zeta)=\mathbb P_f(f_U(K_{\rm out})\ge f)\ge1-\alpha$ (strictly for Clopper–Pearson, Lemma 4.5(c)). Integrating over $\zeta$: $\mathbb P(Z\le U_V)=\mathbb E[\mathbb P(Z\le U_V\mid\zeta)]\ge1-\alpha$.
(c) With Clopper–Pearson, $f_U(K_{\rm out})<1$ iff $K_{\rm out}\le M-1$, and then $f_U(K_{\rm out})\le f_U(M-1)=(1-\alpha)^{1/M}<f$ (Lemma 4.5(b)); by (a) the coverage event fails on all of $\{f_U<1\}$, which has conditional probability $1-f^M>0$. So the conditional coverage is $0$. On the complement $\{K_{\rm out}=M\}$, of conditional probability $f^M$, $U_V=+\infty$ and the event holds; thus $\mathbb P(Z\le U_V\mid\zeta)=f^M$, and $f^M\ge1-\alpha$ exactly because $f\ge(1-\alpha)^{1/M}$. The general formula: with Clopper–Pearson $\{Z\le U_V\}\supseteq\{f_U=1\}=\{K_{\rm out}=M\}$, so $\mathbb P(Z\le U_V\mid\zeta)=f^M+\mathbb P(Z\le U_V,\ f_U<1\mid\zeta)$, and dividing the second term by $\mathbb P(f_U<1\mid\zeta)=1-f^M$ gives the conditional coverage. Finally, if $0<f\le(1-\alpha)^{1/M}=f_U(M-1)$, the event $\{K_{\rm out}=M-1\}$ has conditional probability $Mf^{M-1}(1-f)>0$, lies in $\{f_U<1\}$, and on it $f\le f_U(K_{\rm out})$, so the conditional coverage is positive; and if $f\le1-\alpha^{1/M}=f_U(0)\le f_U(x)$ for every $x$, the coverage event holds on every outcome. $\square$

*What (c) says.* The bound is valid in the frequentist sense of (b), but its validity is carried, for a visited set that misses most of the mass, by the runs that report $U_V=+\infty$; every *finite* bound reported in that regime is wrong. The user of $U_V$ cannot tell which regime applies from $K_{\rm out}$ alone. This is the sense of the draft's last sentence of (ii). Part (c) is stated given $\zeta$; for a deterministic $V$ (trivial $\zeta$) it is an unconditional statement, and instances exist: the check script's $V$ (the lowest-mass models carrying about $1\%$ of the posterior of a small instance; $M=5$, $\alpha=0.1$) has $f=0.987>(0.9)^{1/5}=0.979$, conditional coverage $0$ and coverage $f^M=0.938$.

**Example 4.7 (the independence hypothesis cannot be dropped).** Let $V$ be the set of the validation draws themselves, $V=\{\Sigma_1,\dots,\Sigma_M\}$ (so $\zeta$ and the draws are dependent, in violation of Section 4.1), and use Clopper–Pearson. Then $K_{\rm out}=0$ surely, $f_U=1-\alpha^{1/M}$ and $U_V=Z_V\alpha^{-1/M}$; by Theorem 4.6(a) (whose proof uses only $Z=Z_V/(1-f)$) coverage holds iff $\pi(V)\ge\alpha^{1/M}$. Since $\pi(V)\le M\max_S\pi(S)$, if $\max_S\pi(S)<\alpha^{1/M}/M$ then $\mathbb P(Z\le U_V)=0$. For instance, $\pi$ uniform on $|\mathcal S|=1000$ models, $M=10$, $\alpha=0.05$: $\alpha^{1/M}=0.741$ and $\pi(V)\le0.01$. The checked version in the script uses a random posterior on a small model space.

*SMC validation draws.* The draft defers (ii) for non-exact draws; nothing is claimed here. Theorem 4.6(b) uses the law of $K_{\rm out}$ given $\zeta$ only through Definition 4.4. For the Clopper–Pearson bound, which is nondecreasing in $K_{\rm out}$, the failure event $\{f_U(K_{\rm out})<f\}$ is a lower set $\{K_{\rm out}\le x^\ast(f)\}$ (proof of Lemma 4.5(c)), so a non-exact version of (b) for that bound needs only the lower-tail domination $\mathbb P(K_{\rm out}\le x\mid\zeta)\le F_x(f)$ for all $x$, a statement about the joint law of the draws. For a bound in Definition 4.4 that is not monotone in $K_{\rm out}$ lower-tail domination is not enough (e.g. $M=2$, $\alpha=\tfrac12$, $f_U(0)=f_U(2)=1$, $f_U(1)=\tfrac12$, which satisfies Definition 4.4 since its failure probability is $0$ for $f\le\tfrac12$ and $2f(1-f)\le\tfrac12$ otherwise; the law $\mathbb P(K_{\rm out}=1)=1-f^2$, $\mathbb P(K_{\rm out}=2)=f^2$ is dominated in the lower tail by $\mathrm{Bin}(2,f)$, yet at $f=0.6$ its coverage is $f^2=0.36<\tfrac12$).

### 4.4 The two-sided interval: P10(iii)

**Theorem 4.8 (P10(iii)).** Suppose:
(A) *(islands)* Let $\xi$ be the randomness of a pilot run that chooses the settings $\vartheta(y,\xi)=(N,T,(\phi_t),(m_t),(K_{t,\ell}),(R_t))$ ($\xi$ is a constant if there is no pilot), with $\vartheta(y,\xi)$ satisfying (H0) of `proofs/foundations/PROOF.md`, Section 5.1, for every value of $\xi$. There are $R\ge1$ islands with estimates $\widehat Z_1,\dots,\widehat Z_R$, and for each $r$, conditionally on $\xi$, the trajectory of island $r$ has the law (5.2) of `foundations` Section 5.1 with settings $\vartheta(y,\xi)$ (that is, (H1)–(H3) there hold for the conditional law) and $\widehat Z_r$ is its estimate (5.3); or, if island $r$ skips resampling at some stages, its trajectory has the law (5.5) of `foundations` Theorem 5.7 with those settings and $\widehat Z_r=\widehat Z_w$ is the weighted estimator defined there. Nothing is assumed about the joint law of the islands (they may be dependent). Let $\bar Z_R=\frac1R\sum_r\widehat Z_r$.
(B) *(validation)* $V$, the validation draws and $f_U$ are as in Section 4.1 and Theorem 4.6; the construction randomness $\zeta$ may include $\xi$ and the islands' randomness (for instance $V$ is the islands' visited set), and the validation draws are i.i.d. $\pi$ conditionally on $\zeta$ (hence independent of the islands when $\zeta$ contains them).
Then, with the same $\alpha\in(0,1)$ in both bounds, unconditionally given $y$ (over $\xi$, the islands, $\zeta$ and the draws),
$$
\mathbb P\big(\alpha\bar Z_R\le Z\le U_V\big)\ \ge\ 1-2\alpha,
$$
and with levels $\alpha_1$ (lower) and $\alpha_2$ (upper), the coverage is at least $1-\alpha_1-\alpha_2$. The interval may be empty ($\alpha\bar Z_R>U_V$); this is counted as non-coverage and is within the $2\alpha$.

*Proof.* *Lower bound.* Fix a value of $\xi$. Under (A) the conditional law of island $r$ given $\xi$ is a law of the form (5.2) (or (5.5)) with settings satisfying (H0), on the finite trajectory space of `foundations` Section 5.1; `foundations` Theorem 5.3 (or Theorem 5.7) is a statement about every such law, so $\mathbb E[\widehat Z_r\mid\xi]=Z$ for each $r$, hence $\mathbb E[\bar Z_R\mid\xi]=Z$, and $\bar Z_R\ge0$. (This is the argument of `foundations` Corollary 5.6a, island by island; the conditional independence of the islands assumed there is not needed for the conditional mean of one island.) Markov's inequality (F-d) applied to the conditional law, as in the proof of Theorem 5.5(a) there: $\mathbb P(\bar Z_R>Z/\alpha\mid\xi)\le\alpha\,\mathbb E[\bar Z_R\mid\xi]/Z=\alpha$. Integrating over $\xi$ (tower property): $\mathbb P(Z<\alpha\bar Z_R)\le\alpha$. Neither independence of the islands, nor $R\ge2$, nor finite variance was used. *Upper bound.* Under (B), Theorem 4.6(b) gives $\mathbb P(Z>U_V\mid\zeta)\le\alpha$ for every $\zeta$, hence $\mathbb P(Z>U_V)\le\alpha$; its proof conditions on $\zeta$, which may contain $\xi$ and the islands, and needs only that the validation draws are i.i.d. $\pi$ given $\zeta$. *Union.* The complement of $\{\alpha\bar Z_R\le Z\le U_V\}$ is $\{Z<\alpha\bar Z_R\}\cup\{Z>U_V\}$, whose probability is at most $\alpha+\alpha$. No joint law of the two events is used. $\square$

**Remark 4.9 (conditional form).** P10's preamble says "let $V$ be frozen", i.e. conditionally on $\zeta$. The statement of (iii) conditional on $\zeta$, $\mathbb P(\alpha\bar Z_R\le Z\le U_V\mid\zeta)\ge1-2\alpha$, holds when the islands' conditional law given $(\xi,\zeta)$ is still (5.2)/(5.5) with settings $\vartheta(y,\xi)$ (for instance when $V$ is built from a separate run, so that $\zeta$ contains $\xi$ but is independent of the islands given $\xi$): then $\mathbb E[\bar Z_R\mid\xi,\zeta]=Z$ and the same two steps go through given $\zeta$. It fails in general when $V$ is built from the islands themselves: then $\bar Z_R$ is a function of $\zeta$, so $\mathbb P(\alpha\bar Z_R\le Z\mid\zeta)=\mathbf 1\{\alpha\bar Z_R\le Z\}$, which is $0$ on the event $\{\alpha\bar Z_R>Z\}$, of probability up to $\alpha$ (a round-1 reviewer exhibited an exact instance with one island and $N=1$ in which this event has probability $0.014$ and the conditional coverage on it is $0$). The draft's (iii) is therefore read unconditionally (R5).

*Remarks on the hypotheses (context only; items (1)–(4) and (6) refer to results of `foundations` Section 5.6 and to T5 that are outside this proof and are not used by it).* (1) Unbiasedness needs settings frozen given $(y,\xi)$: an empirical-ESS *schedule*, kernels tuned on the run's own particles, or resampling schemes whose offspring counts are not unbiased given the past are *not* covered (`foundations`, Propositions 5.9, 5.10, 5.13, 5.14); an ESS-based resampling *decision* is covered by the law (5.5) of Theorem 5.7. (2) Resampling: unbiased offspring counts given the whole past; multinomial, residual, stratified and systematic resampling applied afresh qualify. (3) Skipped resampling: the weighted product $\widehat Z_w$ must be used; the unweighted product can be biased in either direction (`foundations`, Proposition 5.8). (4) Islands reusing the pilot's random stream violate the conditional-law hypothesis in (A). (5) The Markov bound is exact for every $R\ge1$ and does not need finite variance (automatic on a finite space) or independent islands; the CLT part of P7(ii) is not used. (6) Mode loss (T5) concerns what the particles see, not the identity $\mathbb E[\widehat Z_r\mid\xi]=Z$, which under (A) holds whether or not the islands find every mode; so the lower bound stays valid under mode loss. In that regime the typical run underestimates $Z$ and $\{\alpha\bar Z_R\le Z\}$ holds with room to spare on it: the bound is loose there, not invalid.

---

## 5. Proposition P11: Rao–Blackwellised PIPs

### 5.1 The statement with an explicit $\sigma$-field

Let $(\Omega,\mathcal H,\mathbb P)$ be the probability space of the run and $\mathcal F\subseteq\mathcal H$ a sub-$\sigma$-field: in the algorithm, $\mathcal F$ is generated by everything the run has produced up to the moment just before coordinate $j$ is updated for the last time (the whole population, its carried weights, the schedule, and all earlier draws; for a fixed sweep order that moment is a fixed step of the run). This is reading R6: the draft's "$\sigma$-field of the population" is taken to include the carried weights and the history, which is what makes the weights of Remark 5.2 measurable. Only the following is used. Fix $j\in[p]$ and $N\ge1$. The data are:

- *weights* $W_1,\dots,W_N$: $\mathcal F$-measurable random variables with $W_i\ge0$ and $\sum_iW_i=1$;
- *conditional inclusion probabilities* $o_{1j},\dots,o_{Nj}$: $\mathcal F$-measurable random variables with values in $[0,1]$;
- *the draws* $\gamma_{1j},\dots,\gamma_{Nj}$: random variables with values in $\{0,1\}$ (the indicator that $j$ belongs to particle $i$ immediately after its update) such that $\mathbb E[\gamma_{ij}\mid\mathcal F]=o_{ij}$ almost surely for every $i$.

Define the *plain* and the *Rao–Blackwellised* estimates $T=\sum_iW_i\gamma_{ij}$ and $T_{\rm RB}=\sum_iW_io_{ij}$; both lie in $[0,1]$. For an integrable random variable $Y$, the *conditional variance given $\mathcal F$* is $\mathrm{Var}(Y\mid\mathcal F)=\mathbb E\big[(Y-\mathbb E[Y\mid\mathcal F])^2\,\big|\,\mathcal F\big]$, the conditional expectation of a non-negative variable: a $[0,\infty]$-valued $\mathcal F$-measurable random variable (here every variable is bounded, so it is finite). "Zero conditional variance given $\mathcal F$" means $\mathrm{Var}(Y\mid\mathcal F)=0$ almost surely.

**Theorem 5.1 (P11).** Under the hypotheses above:
(a) $\mathbb E[T\mid\mathcal F]=T_{\rm RB}$ almost surely.
(b) $\mathrm{Var}(T_{\rm RB}\mid\mathcal F)=0$ almost surely. In general, for a bounded $Y$: $\mathrm{Var}(Y\mid\mathcal F)=0$ a.s. $\iff$ $Y=\mathbb E[Y\mid\mathcal F]$ a.s. $\iff$ $Y$ coincides a.s. with an $\mathcal F$-measurable random variable. So "zero conditional variance" says exactly that $T_{\rm RB}$ is (a.s. equal to) a function of the pre-update history: the final draw contributes no randomness to it.
(c) $\mathbb E[T_{\rm RB}]=\mathbb E[T]$, and $\mathrm{Var}(T)=\mathrm{Var}(T_{\rm RB})+\mathbb E[\mathrm{Var}(T\mid\mathcal F)]\ge\mathrm{Var}(T_{\rm RB})$. If moreover $\gamma_{1j},\dots,\gamma_{Nj}$ are conditionally independent given $\mathcal F$, then $\mathrm{Var}(T\mid\mathcal F)=\sum_iW_i^2o_{ij}(1-o_{ij})$.
(d) *(Inherited error is untouched.)* For every constant $\theta$ (for instance the exact $\mathrm{PIP}_j$),
$$
\mathbb E\big[(T-\theta)^2\big]=\mathbb E\big[(T_{\rm RB}-\theta)^2\big]+\mathbb E[\mathrm{Var}(T\mid\mathcal F)],\qquad \mathbb E[T_{\rm RB}]-\theta=\mathbb E[T]-\theta .
$$
Rao–Blackwellisation removes exactly the final-draw variance $\mathbb E[\mathrm{Var}(T\mid\mathcal F)]$; the bias and the variance $\mathrm{Var}(T_{\rm RB})=\mathrm{Var}(\mathbb E[T\mid\mathcal F])$, which are functionals of the law of the pre-update population (of $\mathcal F$), are unchanged.

*Proof.* (a) Each $W_i$ is $\mathcal F$-measurable and bounded, and each $\gamma_{ij}$ is bounded; by linearity of conditional expectation and "taking out what is known" (F-c), $\mathbb E[T\mid\mathcal F]=\sum_iW_i\,\mathbb E[\gamma_{ij}\mid\mathcal F]=\sum_iW_io_{ij}=T_{\rm RB}$ a.s.
(b) $T_{\rm RB}$ is a finite sum of products of $\mathcal F$-measurable variables, hence $\mathcal F$-measurable and bounded, so $\mathbb E[T_{\rm RB}\mid\mathcal F]=T_{\rm RB}$ a.s. and $\mathrm{Var}(T_{\rm RB}\mid\mathcal F)=\mathbb E[0\mid\mathcal F]=0$. For the equivalences: if $\mathrm{Var}(Y\mid\mathcal F)=0$ a.s., then $\mathbb E[(Y-\mathbb E[Y\mid\mathcal F])^2]=\mathbb E[\mathrm{Var}(Y\mid\mathcal F)]=0$, so $Y=\mathbb E[Y\mid\mathcal F]$ a.s., which is $\mathcal F$-measurable; conversely, if $Y=Y'$ a.s. with $Y'$ $\mathcal F$-measurable, then $\mathbb E[Y\mid\mathcal F]=Y'=Y$ a.s. and the conditional variance vanishes.
(c) The tower property and (a) give $\mathbb E[T]=\mathbb E[\mathbb E[T\mid\mathcal F]]=\mathbb E[T_{\rm RB}]$. The law of total variance (F-c) with (a) gives the decomposition; the second term is $\ge0$. Under conditional independence, the conditional variance of a sum is the sum of the conditional variances, and a $\{0,1\}$-valued variable with conditional mean $o$ has conditional variance $o(1-o)$; the $W_i^2$ come out as in (a).
(d) Conditionally on $\mathcal F$, $\mathbb E[(T-\theta)^2\mid\mathcal F]=\mathrm{Var}(T\mid\mathcal F)+(\mathbb E[T\mid\mathcal F]-\theta)^2=\mathrm{Var}(T\mid\mathcal F)+(T_{\rm RB}-\theta)^2$ by (a); take expectations. The bias identity is (c). $\square$

*Hypotheses used.* $\mathcal F$-measurability of the $W_i$ in (a) and (b), of the $o_{ij}$ in (b); $W_i\ge0$, $\sum_iW_i=1$, $o_{ij}\in[0,1]$ and $\gamma_{ij}\in\{0,1\}$ only for boundedness, which gives the integrability needed in (F-c) and the square-integrability needed in (c) and (d) (and $o_{ij}\in[0,1]$ a.s. is in fact implied by $\mathbb E[\gamma_{ij}\mid\mathcal F]=o_{ij}$); conditional independence only in the last formula of (c). With the trivial $\sigma$-field, "$\mathcal F$-measurable" means constant and (a)–(d) reduce to $\mathbb E[T]=T_{\rm RB}$.

**Remark 5.2 (the Gibbs update satisfies the hypotheses; what the weights may be).** In the algorithm of Section 2.3 of the draft, with a frozen schedule and kernels (as in P6 and P7 of the draft; context only): let the final update of coordinate $j$ be a single-site Gibbs step at temperature $\phi$ (in the last stage $\phi=1$). For particle $i$ in state $S^i$ before the step, the full conditional is
$$
o_{ij}=\frac{\gamma_\phi(S^i\cup\{j\})}{\gamma_\phi(S^i\cup\{j\})+\gamma_\phi(S^i\setminus\{j\})},\qquad\text{with }\gamma_\phi(S^i\cup\{j\})=0\text{ if }|S^i\cup\{j\}|>k_{\max},
$$
a function of $S^i\setminus\{j\}$ and of the frozen $\phi$, hence $\mathcal F$-measurable; the draw is $\gamma_{ij}=\mathbf 1\{U_{ij}\le o_{ij}\}$ with $U_{ij}$ uniform on $[0,1]$ and independent of $\mathcal F$, so $\mathbb E[\gamma_{ij}\mid\mathcal F]=o_{ij}$; with independent $U_{ij}$ across $i$ the draws are conditionally independent given $\mathcal F$. The weights are $W_i=1/N$ if the last resampling preceded the step, or the normalised carried weights $u^i/\sum_lu^l$ of P7, which are functions of the population history up to the step; both are $\mathcal F$-measurable. If the $N$ particles are updated one after another rather than simultaneously, take $\mathcal F$ to be the history up to the first of the $N$ updates of coordinate $j$ in the final sweep: the $o_{ij}$ depend only on $S^i\setminus\{j\}$ and on $\phi$, which those $N$ updates do not change, the weights are not touched by them, and the uniforms $U_{ij}$ are independent of $\mathcal F$ and of each other; so the hypotheses of Theorem 5.1 hold with that $\mathcal F$. Theorem 5.1 uses nothing about invariance or about the temperature: the identity (a) holds for any $o_{ij}$ and any draw with that conditional mean. That $\mathbb E[T]$ (equivalently $\mathbb E[T_{\rm RB}]$) is an estimate of $\mathrm{PIP}_j$ is a property of the population, not of P11: it needs the step to be at $\phi=1$ and the population to target $\pi$ (at $\phi<1$ the same construction estimates $q_\phi(\mathcal A_j)$); P11 only says that Rao–Blackwellisation changes neither the mean nor the inherited error. If coordinate $j$ is altered again after this step by a later move in the same sweep (an add/delete/swap proposal), then the final state's indicator is no longer $\gamma_{ij}$, and $T_{\rm RB}$ estimates the inclusion frequency *at the Gibbs step*, not at the end of the run; under invariant kernels both have the same target.

**Example 5.3 (post-update weights invalidate both conclusions).** Let $N=2$ and $\mathcal F=\{\emptyset,\Omega\}$ (the trivial $\sigma$-field; so "$\mathcal F$-measurable" means "constant"). Let $o_{1j}=\tfrac12$ and $o_{2j}=\tfrac14$ be constants and $\gamma_{1j},\gamma_{2j}$ independent Bernoulli draws with these means, so the second hypothesis of P11 holds. Let the weights be computed *after* the update from the post-update states, as the incoming weights of a next stage would be with potential $G(S)=2^{\mathbf 1\{j\in S\}}$:
$$
W_i=\frac{2^{\gamma_{ij}}}{2^{\gamma_{1j}}+2^{\gamma_{2j}}}\qquad(i=1,2).
$$
These $W_i$ are not $\mathcal F$-measurable. On the four outcomes $(\gamma_{1j},\gamma_{2j})=(0,0),(1,0),(0,1),(1,1)$, of probabilities $\tfrac38,\tfrac38,\tfrac18,\tfrac18$:

| $(\gamma_{1j},\gamma_{2j})$ | $\mathbb P$ | $(W_1,W_2)$ | $T=\sum_iW_i\gamma_{ij}$ | $T_{\rm RB}=\sum_iW_io_{ij}$ |
|---|---|---|---|---|
| $(0,0)$ | $3/8$ | $(\tfrac12,\tfrac12)$ | $0$ | $3/8$ |
| $(1,0)$ | $3/8$ | $(\tfrac23,\tfrac13)$ | $2/3$ | $5/12$ |
| $(0,1)$ | $1/8$ | $(\tfrac13,\tfrac23)$ | $2/3$ | $1/3$ |
| $(1,1)$ | $1/8$ | $(\tfrac12,\tfrac12)$ | $1$ | $3/8$ |

Hence $\mathbb E[T\mid\mathcal F]=\mathbb E[T]=\tfrac38\cdot\tfrac23+\tfrac18\cdot\tfrac23+\tfrac18=\tfrac{11}{24}$, a constant, whereas $T_{\rm RB}$ takes three distinct values: the identity $\mathbb E[T\mid\mathcal F]=T_{\rm RB}$ fails on every outcome, $\mathrm{Var}(T_{\rm RB}\mid\mathcal F)=\mathrm{Var}(T_{\rm RB})>0$, and even the means differ: $\mathbb E[T_{\rm RB}]=\tfrac38\cdot\tfrac38+\tfrac38\cdot\tfrac5{12}+\tfrac18\cdot\tfrac13+\tfrac18\cdot\tfrac38=\tfrac{37}{96}\ne\tfrac{44}{96}=\mathbb E[T]$. (Checked numerically by exact enumeration.) The mechanism: $\mathbb E[W_i\gamma_{ij}\mid\mathcal F]=\mathbb E[W_i\gamma_{ij}]\ne\mathbb E[W_i]\,o_{ij}$ when $W_i$ and $\gamma_{ij}$ are dependent, and "taking out what is known" is exactly what fails. With post-update weights, the correct Rao–Blackwellisation must condition on $\mathcal F$ the whole product $W_i\gamma_{ij}$, i.e. compute $\mathbb E[W_i\gamma_{ij}\mid\mathcal F]$ from the weight rule; it is not $W_io_{ij}$.

---

## 6. Readings, hypotheses made explicit, and flags for the draft

P5, P8(i), (ii), (iv), (iv′), (v), P9, P10 and P11 are true as stated under the readings R1–R6 of Section 0.3; P8(iii) is false as literally written (Example 2.3a) and is proved in the corrected form of Theorem 2.3. The following points should be changed or added in the draft.

1. **P5(iii).** "The constrained minimiser" should read "a constrained minimiser"; it is unique if and only if condition (U) of Theorem 1.3 holds (no tie at the cut when $N_+>k_{\max}$; no $\mathrm{PIP}_j=\tfrac12$ when $N_+<k_{\max}$). The phrase "the coordinates with the largest $\mathrm{PIP}_j$" is to be read among $\{j:\mathrm{PIP}_j>\tfrac12\}$. Worth adding: the cap binds only when $k_{\max}<N_+<2k_{\max}$ (Remark 1.5), and it can bind (Example 1.4). In (i)–(ii), the loss functions and the action spaces (all subsets) should be named.

2. **P8(iii)** (corrected). Two changes. (a) State the hypothesis $U\ge Z$ (the $U$ of (ii)): with $U=Z_V$ the hypothesis $U-Z_V<p(\hat S)m(\hat S)$ holds for every $V$ and the conclusion fails (Example 2.3a(b)). (b) With ties, "$\hat S\in\arg\max_{S\in V}$" should be "$\hat S$ the HPM over $V$", or the conclusion should read "every global maximiser lies in $V$, so the HPM over $V$ is the global HPM"; an $\hat S\in\arg\max_V$ that is not $\prec$-first is not the HPM (Example 2.3a(a)). Without ties and with $U\ge Z$ the draft's wording is correct (Theorem 2.3).

3. **P8(iv).** The ratio to $m(\emptyset)$ is exactly $\big((2b_0+y^\top y)/(2b_0+y^\top y/(n+1))\big)^{\nu}$, which lies in $[1,(n+1)^{\nu})$: it equals $1$ at $y=0$ (then $U_{\rm univ}=m(\emptyset)$, and $=Z$ if also $k_{\max}=0$), is close to $1$ when $y^\top y\ll b_0$, and tends to $(n+1)^{\nu}=(n+1)^{n/2}(n+1)^{a_0}$ as $b_0/y^\top y\to0$. The draft's "exceeds $m(\emptyset)$ by about $(n+1)^{n/2}$" holds in that last regime (the usual one, $b_0$ small), up to the factor $(n+1)^{a_0}$, and should say so. The one-line justification of (eq:floor) lists the *nonzero* eigenvalues of $nX_SH_S^{-1}X_S^\top$; for $|S|>n$ the zero eigenvalues of $G_S$ must be dropped (Lemma 2.1 covers every $|S|$).

4. **P8(iv′).** The heading's "$p<n$" is not what is used: the hypothesis is $\lambda_{\min}(G_{[p]})\ge n\varphi^2>0$, which forces $p\le n$ and allows $p=n$. The $Q_S$ bound holds for every design. Interlacing gives the sharper $D_S\ge\prod_{i\le|S|}h(\lambda_i(G_{[p]}))$ (smallest eigenvalues of the full Gram matrix), at the cost of one eigendecomposition (Theorem 2.4, (2.2)). Also $\varrho\le n+1/(n+1)$ with standardised columns, and $U_{\rm size}\le U_{\rm univ}$ always. Whether (iv′) is "the useful bound" (dependency map) is a numerical question about $U_{\rm size}/Z$ that the statement does not address; Remark 2.5 gives the exact ratio $U_{\rm size}/m(\emptyset)$ and its small-$b_0$ limit $\big((n+1)/(1+n(1-R^2_{[p]}))\big)^{\nu}\sum_kp(|S|=k)\varrho^{-k/2}$, which is large when $R^2_{[p]}$ is near $1$, while $U_{\rm size}/Z$ can be near $1$ even then.

5. **P9(i).** The sharper two-sided form $(1-f)\mathrm{PIP}_{j,V}\le\mathrm{PIP}_j\le(1-f)\mathrm{PIP}_{j,V}+f$ holds and is P8(ii) at $U=Z$ (Theorem 3.2). **P9(ii).** The sentence "Here $\|\cdot\|_{\rm TV}=\sup_A|\cdot|$" belongs in (i). The strict inequality $\delta<\min_j|\mathrm{PIP}_j-\tfrac12|$ cannot be relaxed to $\le$. **P9(iii).** "A fixed tie rule" must be the same fixed total order used for the global HPM; a rule that depends on $V$ (e.g. visiting order) does not work (Theorem 3.4 and the note after it).

6. **P10, probability model.** State it: $V=V(y,\zeta)$; the validation draws are i.i.d. $\pi(\cdot\mid y)$ conditionally on $\zeta$; $K_{\rm out}\sim\mathrm{Bin}(M,f)$ given $\zeta$; "unconditionally" means after integrating over the construction of $V$ (Section 4.1). **P10(i).** The bias of $Z_VM/\max(K_{\rm in},1)$ is the finite sum of Theorem 4.3(b); its sign depends on $(M,f)$ (non-negative when $M(1-f)\ge2$, negative at $M=1$). The alternative safeguard $Z_V(M+1)/(K_{\rm in}+1)$ has bias exactly $-Zf^{M+1}$ and may be preferable. **P10(ii).** Valid for any $(1-\alpha)$ upper confidence bound (Definition 4.4); Clopper–Pearson's validity is Lemma 4.5. The failure of conditional coverage is exact and should be stated: for $f\in((1-\alpha)^{1/M},1)$ every finite reported bound is wrong (conditional coverage $0$), the unconditional coverage being $f^M\ge1-\alpha$ (Theorem 4.6(c)). The independence of the draws from the construction of $V$ cannot be dropped (Example 4.7). **P10(iii).** The hypotheses are those of P7(i) as fixed in `foundations` ((H0)–(H4): frozen settings, i.i.d. start with exact $\bar Z_0$, offspring counts unbiased given the past, the same kernel for all particles, independent pilot; the weighted estimator when resampling is skipped); no independence between the islands and the validation step is needed; the same $\alpha$ is used in both bounds (otherwise $1-\alpha_1-\alpha_2$); the interval may be empty. The lower bound needs only $\mathbb E[\widehat Z_r]=Z$ and holds for $R=1$.

7. **P11.** Write the $\sigma$-field and the conditional-variance claim as in Section 5.1: $\mathrm{Var}(T_{\rm RB}\mid\mathcal F)=0$ a.s., equivalently $T_{\rm RB}$ is $\mathcal F$-measurable. "Does not remove error inherited from earlier stages" is Theorem 5.1(d): the mean squared error splits as $\mathbb E[(T_{\rm RB}-\theta)^2]+\mathbb E[\mathrm{Var}(T\mid\mathcal F)]$, and only the second term is removed. "Weights that depend on the post-update state invalidate this" is Example 5.3: $\mathbb E[T\mid\mathcal F]=\tfrac{11}{24}$ against $T_{\rm RB}\in\{\tfrac38,\tfrac5{12},\tfrac13\}$ and $\mathbb E[T_{\rm RB}]=\tfrac{37}{96}$. Invariance of the kernel is not needed for the identity, only for its interpretation as a PIP estimate; if coordinate $j$ is touched by a later move in the same sweep, $T_{\rm RB}$ refers to the state at the Gibbs step (Remark 5.2).

8. **Draft remark after P7** ("valid upper bounds come from outside the particles: deterministically from P8(iv)–(iv′), or from validated missing mass in P10"): consistent with the above; the P10 bound's validity rests on the exact validation draws, and for a $V$ that misses most of the mass it is carried by the runs that report $+\infty$ (Theorem 4.6(c)). The lower bound $\alpha\bar Z_R$ needs only $\mathbb E[\widehat Z_r\mid y,\xi]=Z$, which holds whether or not the islands find every mode; no analogy between the two mechanisms is claimed.

## 7. Results used from outside this file

- `proofs/foundations/PROOF.md`: Theorem 5.3 (P7(i), for the trajectory law (5.2)) and Theorem 5.7 (for the law (5.5), weighted estimator), each applied to the conditional law of one island given the pilot, and the Markov argument of Theorem 5.5(a); Corollary 5.6a there is the same argument for conditionally independent islands. Used only in Theorem 4.8. The remarks after Theorem 4.8 mention `foundations` Propositions 5.8–5.14 and T5 for context only; nothing is derived from them.
- Standard facts (F-a)–(F-g) of Section 0.4. Clopper–Pearson validity is proved here (Lemma 4.5) rather than cited.
