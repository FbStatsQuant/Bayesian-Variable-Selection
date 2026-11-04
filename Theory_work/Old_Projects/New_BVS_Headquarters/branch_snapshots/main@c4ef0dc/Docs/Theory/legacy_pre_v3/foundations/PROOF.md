# Proofs of the foundational results: Fact F4, Lemma L4, Lemma L6, Proposition P6, Proposition P7

Supplement material for *Split-and-merge with an exact merge: composite-start sequential Monte Carlo for Bayesian variable selection*, draft of 14 October 2026. Thread: foundations. Prover: Fable 5.1 (lead), 14 October 2026. Version 3, final text (after three review rounds with three Opus and three Astra reviewers each; rulings in FINDINGS.md; v1 is kept as review/PROOF.md, v2 as review/PROOF_v2.md, and the round-3 text as review/PROOF_v3.md; the wording changes made after round 3 are listed in FINDINGS.md and were not re-reviewed). Notation follows Section 2 of the draft. Nothing numbered in the draft is assumed; only standard probability, linear algebra and Markov-chain facts are used (each is named where it is used). Numerical sanity checks of the identities, the examples and the counterexamples are in `check_foundations.py` beside this file and in the reviewers' scripts under `review/`; they are not part of the proofs.

**Summary of the outcome.** All five results are true as stated, under the three readings fixed in Section 0.2 (the ones for L6 and P7 are forced by the draft's own text; all three are flagged there). What the proofs add or correct:

- **F4** is proved as a theorem with a unique minimiser, together with the population form used in T3 and T11 (Corollary 1.2).
- **L4(iii)** says the greedy schedule "reaches $\phi=1$"; this needs a proof that it terminates. Theorem 2.4(b) gives the explicit bound $T\le\max\{1,\lceil D/(2\sqrt{\log(1+c)})\rceil\}$ with $D=\max d-\min d$. Minimality is proved against every finite sequence satisfying the $\chi^2$ constraint, monotone or not.
- **L6** holds verbatim for the paper's prior $b_\pi=p$. Parts (iii)–(v) are false for a general $b_\pi$ (Remark 3.4), so the draft's preamble "for the untruncated $\mathrm{BB}(1,b_\pi)$ prior" must attach $b_\pi=p$ to (iii)–(v) as it does to (ii). The "in particular" clause concerns the *size-class* ratio; the *per-model* ratio is $O(1/p)$ for fixed $k$ and these should not be confused (Remark 3.3).
- **P6**: the Metropolis–Hastings kernel is reversible for *every* proposal kernel; the symmetry condition $\Pi_t(S,S')>0\Leftrightarrow\Pi_t(S',S)>0$ is not needed for correctness (Proposition 4.3). The draft's example "swap with a neighbour list built from $X$" satisfies that condition if the neighbour relation is symmetric, and (for $k_{\max}\ge1$) only then; a nearest-neighbour list is not symmetric in general; and the neighbour-swap Hastings ratio is $|N(j)\setminus S|/|N(l)\setminus S'|$ when $j\in N(l)$, and $0$ otherwise (audit 2026-10-15), not $1$ (Remark 4.4). Non-reversibility of sweeps is shown by an explicit two-variable Gibbs sweep, which, for a target on exactly two coordinates with no binding cap ($p=k_{\max}=2$), is reversible if and only if the target is a product (Example 4.7). In general (Proposition 4.7a, audit 2026-10-15): a sweep $G_iG_j$ over two coordinates is reversible if and only if, without a binding cap ($k_{\max}\ge p$), coordinates $i$ and $j$ are conditionally independent under $q$ given the others; with a binding cap ($1\le k_{\max}\le p-1$) it is never reversible. State-dependent selection fails as the draft's remark says (Remark 4.8).
- **P7**: sufficient conditions are (H0)–(H3) of Section 5.1, with the pilot condition (H4) of Section 5.5. One condition of the draft is *insufficient as written*: Section 2.3 asks for unbiased offspring counts "given the weights", whereas the proof needs them given the whole population, (5.1); Proposition 5.13 gives an exact counterexample to P7(i) under the weights-only reading. The four schemes named in P7 satisfy (5.1) (Lemma 5.4), so P7 holds for them and, more generally, under the population-conditional reading of its resampling condition; step 2(c) of the algorithm should be reworded to that reading. The draft's sentence that skipped resampling requires the weighted estimator is proved (Theorem 5.7, Proposition 5.8); the resampling *decisions* may even be adaptive (ESS-triggered) without affecting the weighted estimator, so "resampling times fixed in advance" is stronger than needed. The unweighted product can be biased when resampling is skipped, in either direction depending on the kernel (Proposition 5.8). With resampling skipped at the final stage, the unbiased estimate of $Z\,\pi(f)$ uses the terminal weights, $\widehat Z_w\sum_iu_T^if(X_T^i)/\sum_iu_T^i$; the unweighted terminal average is biased in general (Corollary 5.7a, audit 2026-10-15). The offspring identity must hold given the whole past of the run, not only given the current population (Proposition 5.14, audit 2026-10-15); a scheme applied afresh to the current population, as in (H2), satisfies this. Frozen schedules and kernels cannot be dropped in general: Propositions 5.9 and 5.10 give exact counterexamples for particle-dependent choices. The "finite variance" proviso of (ii) is automatic on a finite space. Section 6 lists the hypotheses added and the flags.

---

## 0. Setting, conventions and the frozen statements

### 0.1 The model space and the bridge

Throughout, $p\ge1$ and $k_{\max}\in\{0,\dots,p\}$ are fixed, and
$$
\mathcal S:=\{S\subseteq[p]:|S|\le k_{\max}\}
$$
is the model space: a nonempty finite set ($\emptyset\in\mathcal S$). Two functions on $\mathcal S$ are given, $\gamma_0:\mathcal S\to(0,\infty)$ and $d:\mathcal S\to\mathbb R$. In the paper $\gamma_0(S)=p(S)r(S)$, which is strictly positive on $\mathcal S$ because $w>0$ and every block table $r_b$ is positive, and $d$ is the discrepancy of Section 2.2; the prior vanishes off $\mathcal S$, so every sum "over $S$" in the draft is a sum over $\mathcal S$. Nothing below uses the specific form of $\gamma_0$ or $d$; the theorems of Sections 2 and 5 and the examples and counterexamples are stated for an arbitrary pair $(\gamma_0,d)$ on a finite set, which is the setting in which the draft states L4 and P7. (Whether a particular counterexample is realised by some design $X$ is not claimed; for instance $p=1$ with one block gives $d\equiv0$.) For $\phi\in\mathbb R$,
$$
\gamma_\phi(S)=\gamma_0(S)e^{\phi d(S)},\qquad \bar Z_\phi=\sum_{S\in\mathcal S}\gamma_\phi(S)\in(0,\infty),\qquad q_\phi=\gamma_\phi/\bar Z_\phi,\qquad F(\phi)=\log\bar Z_\phi .
$$
Thus $q_\phi$ is a probability on $\mathcal S$ with $q_\phi(S)>0$ for every $S$ and every $\phi$; $q_0=\pi_0$ and $q_1=\pi$. For a probability $q$ on $\mathcal S$ and $f:\mathcal S\to\mathbb R$ write $q(f)=\sum_Sq(S)f(S)$.

The evidence is $Z=\sum_Sp(S)m(S)=m(\emptyset)\sum_Sp(S)\mathrm{BF}(S)$, and since $d=\log\mathrm{BF}-\log r$ gives $\gamma_0e^{d}=pr\cdot\mathrm{BF}/r=p\,\mathrm{BF}$,
$$
Z=m(\emptyset)\bar Z_1,\qquad m(\emptyset)>0,\ \bar Z_1>0 . \tag{0.1}
$$

**Chi-square divergence.** For probabilities $q',q$ on $\mathcal S$ with $q>0$,
$$
\chi^2(q'\|q)=\sum_{S\in\mathcal S}\frac{q'(S)^2}{q(S)}-1 .
$$
By the Cauchy–Schwarz inequality, $1=(\sum_Sq'(S))^2=\big(\sum_S\tfrac{q'(S)}{\sqrt{q(S)}}\sqrt{q(S)}\big)^2\le\sum_S\tfrac{q'(S)^2}{q(S)}\sum_Sq(S)$, so $\chi^2(q'\|q)\ge0$, with equality if and only if $q'=q$.

**Kernels.** A Markov kernel on $\mathcal S$ is a function $K:\mathcal S\times\mathcal S\to[0,1]$ with $\sum_{S'}K(S,S')=1$ for every $S$. For a probability $q$ and a function $f$ on $\mathcal S$, $(qK)(S')=\sum_Sq(S)K(S,S')$ and $(Kf)(S)=\sum_{S'}K(S,S')f(S')$, so that $(qK)(f)=q(Kf)$. The composition is $(K_1K_2)(S,S'')=\sum_{S'}K_1(S,S')K_2(S',S'')$, the matrix product; it is associative. $K$ is *$q$-invariant* if $qK=q$, and *$q$-reversible* if $q(S)K(S,S')=q(S')K(S',S)$ for all $S,S'$. Since $\gamma_\phi$ is a positive multiple of $q_\phi$, "$\gamma_\phi$-reversible" and "$q_\phi$-reversible" mean the same thing. A product of two functions $f,g$ on $\mathcal S$ is written $f\cdot g$ or $fg$; a product of two kernels is their composition. Which one is meant is always clear from the types of the factors.

### 0.2 The statements, as frozen from the draft

**Fact F4 (fixed-design projection).** For a full-rank block $X_b$ under a misspecified mean $\mu$, the KL-optimal coefficient is $(X_b^\top X_b)^{-1}X_b^\top\mu$, and the KL-optimal variance is $\sigma_\star^2+\|(I-P_b)\mu\|^2/n$.

**Lemma L4 (monotonicity and optimality of the greedy schedule).** Let $F(\phi)=\log\bar Z_\phi$, which is convex on $\mathbb R$.
(i) $1+\chi^2(q_{\phi+\delta}\|q_\phi)=\exp\{F(\phi+2\delta)+F(\phi)-2F(\phi+\delta)\}$. This is nondecreasing in $\delta\ge0$.
(ii) For fixed $\psi$, $\chi^2(q_\psi\|q_\phi)$ is nonincreasing in $\phi\in(-\infty,\psi]$.
(iii) Consequently the greedy schedule is well defined and strictly increasing. It reaches $\phi=1$ in the minimal number of stages among all schedules satisfying $\chi^2(q_{\phi_t}\|q_{\phi_{t-1}})\le c$ at every stage.
Here the greedy population-ESS schedule with threshold $\rho\in(0,1)$ and $c=\rho^{-1}-1$ is $\phi_0=0$ and $\phi_t=\sup\{\phi\in(\phi_{t-1},1]:\chi^2(q_\phi\|q_{\phi_{t-1}})\le c\}$, and $T$ is the number of stages needed to reach $\phi=1$. (Since $\rho\in(0,1)$, $c>0$.)

**Lemma L6 (the BB(1,p) prior).** For the untruncated $\mathrm{BB}(1,b_\pi)$ prior:
(i) per-model odds: $w(k+1)/w(k)=(k+1)/(b_\pi+p-k-1)$;
(ii) for $b_\pi=p$, size-class odds: $\mathbb P(K=k+1)/\mathbb P(K=k)=(p-k)/(2p-k-1)$, which is at most $\tfrac12$ for $k\ge1$ (with equality at $k=1$);
(iii) $\mathbb P(K=0)=\tfrac12$ and $\mathbb P(K\ge m)\le2^{1-m}$ for $m\ge1$;
(iv) with a cap $k_{\max}\ge0$, retained atoms increase by at most a factor $2$ (since $W\ge\mathbb P(K=0)=\tfrac12$) and excluded atoms become $0$; so $\mathbb P_{\rm cap}(\mathcal A)\le2\mathbb P(\mathcal A)$ for every event $\mathcal A$;
(v) $\log p(S_0)\ge-s_0\log(2p)-\log2$ whenever $s_0\le k_{\max}$.
In particular the size-class ratio tends to $\tfrac12$ for fixed $k$ (or $k=o(p)$). The size tail is geometric. Dimension-prior conditions of the form $\pi_p(s)\le c\,p^{-a}\pi_p(s-1)$ with $a>0$, whose successive-size penalty depends polynomially on $p$, therefore fail.
*Readings.* Parts (iii)–(v) are read with $b_\pi=p$, the paper's prior, as in (ii): they fail in general otherwise (Remark 3.4). $\pi_p(s)$ in the last sentence is the law of the model size, and "fail" means "fail for all large $p$".

**Proposition P6 (kernel correctness).** Let $\Pi_t$ be a proposal kernel on $\{S:|S|\le k_{\max}\}$ with $\Pi_t(S,S')>0\Leftrightarrow\Pi_t(S',S)>0$. Examples are add/delete, uniform swap, and swap with a neighbour list built from $X$. With acceptance probability $\min\{1,\gamma_{\phi_t}(S')\Pi_t(S',S)/(\gamma_{\phi_t}(S)\Pi_t(S,S'))\}$, and proposals beyond the cap rejected, the kernel is reversible with respect to $q_{\phi_t}$. Single-site Gibbs updates are reversible. Systematic sweeps (compositions) and random-scan mixtures with frozen selection probabilities are $q_{\phi_t}$-invariant, but sweeps are in general not reversible.
*Reading.* The neighbour-list example satisfies the displayed condition when the neighbour relation is symmetric, and for $k_{\max}\ge1$ only then (Remark 4.4); the reversibility claim itself needs no condition on the proposal (Proposition 4.3).

**Proposition P7 (frozen schedules: unbiasedness and free lower bounds).** Suppose the schedule, the kernels (including any scan probabilities), the number of moves and the resampling times are fixed in advance. For instance, they may be computed from an independent pilot, as a function of $(y,\text{pilot randomness})$ only; all statements are then conditional on the pilot. Suppose also that the initial particles are i.i.d. from $\pi_0$ (P1), and that resampling is performed at every stage with unbiased offspring counts (multinomial, stratified, systematic or residual). If resampling is skipped at some stages, the weights must be carried forward and the corresponding weighted estimator used; the unweighted product in Section 2 is then not the right estimator. Then (i) $\mathbb E[\widehat Z]=Z$; (ii) for $R$ i.i.d. islands with mean $\bar Z_R$ and any $\alpha\in(0,1)$, $\mathbb P(Z\ge\alpha\bar Z_R)\ge1-\alpha$, and under finite variance a CLT in $R$ gives two-sided intervals for $\mathbb E[\widehat Z]=Z$; (iii) $\mathbb E[\log\widehat Z]\le\log Z$. Here $\widehat Z=m(\emptyset)\bar Z_0\prod_{t=1}^T\big(\tfrac1N\sum_iw_t^i\big)$ with $w_t^i=\exp\{(\phi_t-\phi_{t-1})d(S^i)\}$ computed on the population entering stage $t$, and the algorithm of Section 2.3 asks for "any scheme satisfying $\mathbb E[\#\text{offspring of }i\mid\text{weights}]=Nw_t^i/\sum_jw_t^j$".
*Reading.* "Unbiased offspring counts" is read as (5.1): the expected counts equal $NW^i$ given the whole current population, not only given its weight vector. The four named schemes satisfy (5.1); the weights-only reading is insufficient (Proposition 5.13).

---

## 1. Fact F4: the fixed-design Kullback–Leibler projection

**Theorem 1.1.** Let $n\ge1$, let $X_b\in\mathbb R^{n\times m}$ have full column rank $m$ (so $m\le n$), and let $P_b=X_b(X_b^\top X_b)^{-1}X_b^\top$ be the orthogonal projection onto the column span of $X_b$. Let $\mu\in\mathbb R^n$ and $\sigma_\star^2>0$, and let $P_\star=N_n(\mu,\sigma_\star^2I_n)$. For $\beta\in\mathbb R^m$ and $v>0$ let $Q_{\beta,v}=N_n(X_b\beta,vI_n)$. Then
$$
\mathrm{KL}(P_\star\|Q_{\beta,v})=\frac n2\Big[\log\frac v{\sigma_\star^2}-1+\frac{\sigma_\star^2}v\Big]+\frac{\|\mu-X_b\beta\|^2}{2v}, \tag{1.1}
$$
and $(\beta,v)\mapsto\mathrm{KL}(P_\star\|Q_{\beta,v})$ has the unique minimiser
$$
\bar\beta=(X_b^\top X_b)^{-1}X_b^\top\mu,\qquad \bar v=\sigma_\star^2+\frac{\|(I-P_b)\mu\|^2}n,
$$
with minimal value $\tfrac n2\log(\bar v/\sigma_\star^2)$.

*Proof.* Write $p_\star$ and $q_{\beta,v}$ for the two Lebesgue densities and $\mathbb E_\star$ for expectation under $P_\star$. Then $\mathrm{KL}(P_\star\|Q_{\beta,v})=\mathbb E_\star[\log p_\star(y)-\log q_{\beta,v}(y)]$, where
$$
\log p_\star(y)=-\frac n2\log(2\pi\sigma_\star^2)-\frac{\|y-\mu\|^2}{2\sigma_\star^2},\qquad
\log q_{\beta,v}(y)=-\frac n2\log(2\pi v)-\frac{\|y-X_b\beta\|^2}{2v}.
$$
Under $P_\star$, $y-\mu$ has mean $0$ and $\mathbb E_\star\|y-\mu\|^2=n\sigma_\star^2$; hence
$$
\mathbb E_\star\|y-X_b\beta\|^2=\mathbb E_\star\|(y-\mu)+(\mu-X_b\beta)\|^2=n\sigma_\star^2+2(\mu-X_b\beta)^\top\mathbb E_\star[y-\mu]+\|\mu-X_b\beta\|^2=n\sigma_\star^2+\|\mu-X_b\beta\|^2 .
$$
Therefore
$$
\mathrm{KL}(P_\star\|Q_{\beta,v})=-\frac n2\log(2\pi\sigma_\star^2)-\frac n2+\frac n2\log(2\pi v)+\frac{n\sigma_\star^2+\|\mu-X_b\beta\|^2}{2v},
$$
which is (1.1).

*Minimisation over $\beta$.* For fixed $v>0$, (1.1) is $\|\mu-X_b\beta\|^2/(2v)$ plus a constant, so it is minimised exactly where $r(\beta):=\|\mu-X_b\beta\|^2$ is. Since $X_b\beta$ lies in the column span $\mathcal C$ of $X_b$ and $(I-P_b)\mu\perp\mathcal C$, Pythagoras gives
$$
r(\beta)=\|(I-P_b)\mu\|^2+\|P_b\mu-X_b\beta\|^2\ \ge\ \|(I-P_b)\mu\|^2,
$$
with equality if and only if $X_b\beta=P_b\mu$. Because $X_b$ has full column rank, $X_b^\top X_b$ is invertible and $X_b\beta=P_b\mu$ has the unique solution $\beta=(X_b^\top X_b)^{-1}X_b^\top P_b\mu=(X_b^\top X_b)^{-1}X_b^\top\mu$, using $X_b^\top P_b=X_b^\top$. So for every $v$ the minimiser in $\beta$ is $\bar\beta$, and it does not depend on $v$.

*Minimisation over $v$.* With $\bar r:=\|(I-P_b)\mu\|^2$, the function to minimise is $g(v)=\tfrac n2\log v+\dfrac{n\sigma_\star^2+\bar r}{2v}$ plus a constant, on $(0,\infty)$. It is differentiable with
$$
g'(v)=\frac n{2v}-\frac{n\sigma_\star^2+\bar r}{2v^2}=\frac n{2v^2}\big(v-\bar v\big),\qquad \bar v=\sigma_\star^2+\frac{\bar r}n ,
$$
which is negative on $(0,\bar v)$ and positive on $(\bar v,\infty)$. Hence $\bar v$ is the unique minimiser of $g$. Since the minimiser in $\beta$ is $\bar\beta$ for every $v$, the pair $(\bar\beta,\bar v)$ is the unique joint minimiser. Its value is $\tfrac n2[\log(\bar v/\sigma_\star^2)-1]+\tfrac{n\sigma_\star^2+\bar r}{2\bar v}=\tfrac n2\log(\bar v/\sigma_\star^2)-\tfrac n2+\tfrac{n\bar v}{2\bar v}=\tfrac n2\log(\bar v/\sigma_\star^2)$. $\square$

**Corollary 1.2 (population form).** Let $X\in\mathbb R^{n\times p}$, $\mu=X\beta^\star$, $\Gamma=X^\top X/n$, and let $b\subseteq[p]$ be such that $\Gamma_{bb}\succ0$ (equivalently, $X_b$ has full column rank). Then
$$
\bar\beta=\Gamma_{bb}^{-1}\Gamma_{b,[p]}\beta^\star,\qquad \frac{\|(I-P_b)\mu\|^2}n=\beta^{\star\top}\big(\Gamma-\Gamma_{[p],b}\Gamma_{bb}^{-1}\Gamma_{b,[p]}\big)\beta^\star .
$$
(For the paper: these are the finite-$n$ residual variance $\bar\sigma^2_n(b)$ of Section 3.3 of the draft and the block projection coefficients $\gamma_b$ of Theorem T11, with $\Gamma_n$ in place of its limit; the lead checked the two definitions against the draft, and nothing below uses them.)

*Proof.* $X_b^\top\mu=X_b^\top X\beta^\star=n\Gamma_{b,[p]}\beta^\star$ and $X_b^\top X_b=n\Gamma_{bb}$, giving $\bar\beta$. Next, $\|(I-P_b)\mu\|^2=\mu^\top\mu-\mu^\top P_b\mu$ because $P_b$ is a symmetric idempotent; $\mu^\top\mu=n\beta^{\star\top}\Gamma\beta^\star$ and $\mu^\top P_b\mu=\beta^{\star\top}X^\top X_b(X_b^\top X_b)^{-1}X_b^\top X\beta^\star=n\beta^{\star\top}\Gamma_{[p],b}\Gamma_{bb}^{-1}\Gamma_{b,[p]}\beta^\star$. $\square$

**Remark 1.3.** (a) The divergence minimised is $\mathrm{KL}(P_\star\|Q)$, so that the minimiser is the point of the working family at which the expected log-likelihood under the truth is largest; this is the sense of "KL projection" in the draft. (The reverse divergence $\mathrm{KL}(Q_{\beta,v}\|P_\star)=\tfrac n2[\log(\sigma_\star^2/v)-1+v/\sigma_\star^2]+\|\mu-X_b\beta\|^2/(2\sigma_\star^2)$, by the same computation with the roles exchanged, is minimised at $v=\sigma_\star^2$ for every $\beta$, so it gives a different variance whenever $(I-P_b)\mu\ne0$.) No asymptotic statement is made or needed here. (b) If $X_b$ does not have full column rank, $P_b\mu$ and $\bar v$ are unchanged, but $\bar\beta$ is any solution of $X_b^\top X_b\beta=X_b^\top\mu$ and is not unique; the draft's hypothesis $\Gamma_{C_bC_b}\succ0$ in T11 is what gives uniqueness.

---

## 2. Lemma L4: monotonicity of the chi-square along the bridge and optimality of the greedy schedule

**Lemma 2.1 (the log-partition function).** $F$ is infinitely differentiable on $\mathbb R$, with
$$
F'(\phi)=q_\phi(d),\qquad F''(\phi)=\mathrm{Var}_{q_\phi}(d)=q_\phi(d^2)-q_\phi(d)^2\ \ge0 .
$$
Hence $F$ is convex and $F'$ is nondecreasing. If $d$ is not constant on $\mathcal S$, then $F''>0$ everywhere and $F'$ is strictly increasing. Moreover $F''(\phi)\le D^2/4$ for every $\phi$, where $D:=\max_{\mathcal S}d-\min_{\mathcal S}d$.

*Proof.* $\bar Z_\phi=\sum_S\gamma_0(S)e^{\phi d(S)}$ is a finite sum of positive smooth functions, so $\bar Z$ is smooth and positive and $F=\log\bar Z$ is smooth, with $\bar Z'_\phi=\sum_S\gamma_0(S)d(S)e^{\phi d(S)}$ and $\bar Z''_\phi=\sum_S\gamma_0(S)d(S)^2e^{\phi d(S)}$. Thus $F'=\bar Z'/\bar Z=q_\phi(d)$ and $F''=\bar Z''/\bar Z-(\bar Z'/\bar Z)^2=q_\phi(d^2)-q_\phi(d)^2=\mathrm{Var}_{q_\phi}(d)$. A variance is nonnegative, and it is zero if and only if $d$ is $q_\phi$-a.s. constant, i.e. constant on $\mathcal S$, because $q_\phi$ charges every point of $\mathcal S$. For the bound, let $m=(\max d+\min d)/2$; then $|d-m|\le D/2$ on $\mathcal S$ and $\mathrm{Var}_{q_\phi}(d)=\mathrm{Var}_{q_\phi}(d-m)\le q_\phi((d-m)^2)\le D^2/4$. $\square$

**Proposition 2.2 (L4(i)).** For all $\phi,\delta\in\mathbb R$,
$$
1+\chi^2(q_{\phi+\delta}\|q_\phi)=\frac{\bar Z_{\phi+2\delta}\,\bar Z_\phi}{\bar Z_{\phi+\delta}^2}=\exp\{F(\phi+2\delta)+F(\phi)-2F(\phi+\delta)\} . \tag{2.1}
$$
For fixed $\phi$, the function $\delta\mapsto\chi^2(q_{\phi+\delta}\|q_\phi)$ vanishes at $\delta=0$, is nondecreasing on $[0,\infty)$ and nonincreasing on $(-\infty,0]$; if $d$ is not constant on $\mathcal S$ it is strictly increasing on $[0,\infty)$.

*Proof.* Directly from the definitions,
$$
\sum_S\frac{q_{\phi+\delta}(S)^2}{q_\phi(S)}=\sum_S\frac{\gamma_0(S)^2e^{2(\phi+\delta)d(S)}}{\bar Z_{\phi+\delta}^2}\cdot\frac{\bar Z_\phi}{\gamma_0(S)e^{\phi d(S)}}=\frac{\bar Z_\phi}{\bar Z_{\phi+\delta}^2}\sum_S\gamma_0(S)e^{(\phi+2\delta)d(S)}=\frac{\bar Z_{\phi+2\delta}\bar Z_\phi}{\bar Z_{\phi+\delta}^2},
$$
which is (2.1). Put $h(\delta)=F(\phi+2\delta)+F(\phi)-2F(\phi+\delta)$, so that $1+\chi^2(q_{\phi+\delta}\|q_\phi)=e^{h(\delta)}$ and $h(0)=0$. By Lemma 2.1, $h$ is differentiable with $h'(\delta)=2F'(\phi+2\delta)-2F'(\phi+\delta)$. For $\delta\ge0$ we have $\phi+2\delta\ge\phi+\delta$, so $h'(\delta)\ge0$ because $F'$ is nondecreasing; for $\delta\le0$ the inequality reverses. Since $\exp$ is increasing, the monotonicity of $h$ transfers to $\chi^2$. If $d$ is not constant, $F'$ is strictly increasing and $h'(\delta)>0$ for $\delta>0$. $\square$

**Proposition 2.3 (L4(ii)).** Fix $\psi\in\mathbb R$. For all $\phi\in\mathbb R$,
$$
1+\chi^2(q_\psi\|q_\phi)=\exp\{F(2\psi-\phi)+F(\phi)-2F(\psi)\},
$$
and $\phi\mapsto\chi^2(q_\psi\|q_\phi)$ is nonincreasing on $(-\infty,\psi]$ and nondecreasing on $[\psi,\infty)$, with minimum value $0$ at $\phi=\psi$.

*Proof.* Apply (2.1) with $\phi+\delta=\psi$, i.e. $\delta=\psi-\phi$ and $\phi+2\delta=2\psi-\phi$. The exponent $k(\phi)=F(2\psi-\phi)+F(\phi)-2F(\psi)$ has derivative $k'(\phi)=F'(\phi)-F'(2\psi-\phi)$. For $\phi\le\psi$ we have $\phi\le\psi\le2\psi-\phi$, so $k'(\phi)\le0$; for $\phi\ge\psi$, $k'(\phi)\ge0$. And $k(\psi)=0$. $\square$

**Theorem 2.4 (L4(iii)).** Let $c>0$, and define $\phi_0=0$ and, as long as $\phi_{t-1}<1$,
$$
\Phi_t:=\{\phi\in(\phi_{t-1},1]:\chi^2(q_\phi\|q_{\phi_{t-1}})\le c\},\qquad \phi_t:=\sup\Phi_t .
$$
(a) *Well defined.* $\Phi_t$ is nonempty and contains its supremum, so $\phi_t=\max\Phi_t$ and $\phi_t>\phi_{t-1}$: the schedule is strictly increasing, and it satisfies its own constraint, $\chi^2(q_{\phi_t}\|q_{\phi_{t-1}})\le c$, at every stage.

(b) *Termination.* Let $D=\max_{\mathcal S}d-\min_{\mathcal S}d$. If $D=0$ then $\phi_1=1$ and $T=1$. If $D>0$, put $\delta_c:=2\sqrt{\log(1+c)}/D$; then $\phi_t\ge\min\{1,\phi_{t-1}+\delta_c\}$ for every $t$, so the schedule reaches $1$ after
$$
T\le\Big\lceil\frac{D}{2\sqrt{\log(1+c)}}\Big\rceil
$$
stages, where $T:=\min\{t:\phi_t=1\}$. In both cases $T\le\max\{1,\lceil D/(2\sqrt{\log(1+c)})\rceil\}$.

(c) *Minimality.* Let $(\psi_s)_{s=0}^M$ be any finite sequence of real numbers with $\psi_0=0$, $\psi_M=1$ and $\chi^2(q_{\psi_s}\|q_{\psi_{s-1}})\le c$ for $s=1,\dots,M$. Then $T\le M$. In particular the greedy schedule, which by (a) is itself such a sequence, uses the minimal number of stages among all strictly increasing schedules $0=\psi_0<\psi_1<\dots<\psi_M=1$ satisfying the constraint at every stage.

*Proof.* (a) Fix $t$ with $\phi_{t-1}<1$ and let $u(\phi)=\chi^2(q_\phi\|q_{\phi_{t-1}})$. By (2.1), $u(\phi)=\exp\{F(2\phi-\phi_{t-1})+F(\phi_{t-1})-2F(\phi)\}-1$ is a continuous function of $\phi$ on $\mathbb R$, with $u(\phi_{t-1})=0<c$. By continuity there is $\varepsilon\in(0,1-\phi_{t-1}]$ with $u\le c$ on $[\phi_{t-1},\phi_{t-1}+\varepsilon]$, so $\phi_{t-1}+\varepsilon\in\Phi_t$ and $\Phi_t\neq\emptyset$. The set $C_t=\{\phi\in[\phi_{t-1},1]:u(\phi)\le c\}$ is closed (the preimage of $(-\infty,c]$ under a continuous function, intersected with a closed interval) and bounded, and $\Phi_t=C_t\setminus\{\phi_{t-1}\}$. Let $\phi^\ast=\sup\Phi_t$. Then $\phi^\ast\ge\phi_{t-1}+\varepsilon>\phi_{t-1}$, and $\phi^\ast\in C_t$ because $C_t$ is closed; hence $\phi^\ast\in\Phi_t$. So $\phi_t=\max\Phi_t>\phi_{t-1}$, and $u(\phi_t)\le c$ because $\phi_t\in\Phi_t$.

(b) If $D=0$, $d$ is constant, $q_\phi=q_0$ for all $\phi$ and $u\equiv0$, so $\Phi_1=(0,1]$ and $\phi_1=1$. Let $D>0$ and fix $t$ with $\phi:=\phi_{t-1}<1$. For $\delta\ge0$, with $h$ as in the proof of Proposition 2.2,
$$
h(\delta)=\big[F(\phi+2\delta)-F(\phi+\delta)\big]-\big[F(\phi+\delta)-F(\phi)\big]=\int_0^\delta\big[F'(\phi+\delta+s)-F'(\phi+s)\big]ds=\int_0^\delta\!\!\int_0^\delta F''(\phi+s+r)\,dr\,ds\le\frac{\delta^2D^2}4
$$
by Lemma 2.1 (fundamental theorem of calculus twice; $F$ is $C^2$). Hence $u(\phi+\delta)=e^{h(\delta)}-1\le e^{\delta^2D^2/4}-1\le c$ whenever $0\le\delta\le\delta_c$. So every $\phi'\in(\phi_{t-1},\min\{1,\phi_{t-1}+\delta_c\}]$ belongs to $\Phi_t$, and $\phi_t=\max\Phi_t\ge\min\{1,\phi_{t-1}+\delta_c\}$. By induction $\phi_t\ge\min\{1,t\delta_c\}$, so $\phi_t=1$ as soon as $t\delta_c\ge1$, i.e. $T\le\lceil1/\delta_c\rceil$.

(c) By (b), $T$ is finite. We prove by induction on $t\in\{0,1,\dots,T\}$ the claim
$$
\mathcal C(t):\qquad \phi_t\ \ge\ \min\{1,\psi_s\}\quad\text{for every }s\le\min\{t,M\}.
$$
$\mathcal C(0)$ holds since $\phi_0=0=\psi_0$. Let $1\le t\le T$ and assume $\mathcal C(t-1)$. Since $t\le T$, $\phi_{t-1}<1$, so $\mathcal C(t-1)$ gives $\phi_{t-1}\ge\psi_s$ for every $s\le\min\{t-1,M\}$. As $\phi_t>\phi_{t-1}$, it remains to show $\phi_t\ge\min\{1,\psi_t\}$ when $t\le M$. If $\psi_t\le\phi_{t-1}$ this is immediate. Otherwise $\psi_{t-1}\le\phi_{t-1}<\psi_t$. Put $\psi'=\min\{1,\psi_t\}\in(\phi_{t-1},1]$. By Proposition 2.2 (monotonicity in the endpoint, applied at the base point $\phi_{t-1}$ with $0<\psi'-\phi_{t-1}\le\psi_t-\phi_{t-1}$),
$$
\chi^2(q_{\psi'}\|q_{\phi_{t-1}})\le\chi^2(q_{\psi_t}\|q_{\phi_{t-1}}),
$$
and by Proposition 2.3 (monotonicity in the base point, with $\psi_{t-1}\le\phi_{t-1}\le\psi_t$),
$$
\chi^2(q_{\psi_t}\|q_{\phi_{t-1}})\le\chi^2(q_{\psi_t}\|q_{\psi_{t-1}})\le c .
$$
Hence $\psi'\in\Phi_t$ and $\phi_t=\max\Phi_t\ge\psi'$. This proves $\mathcal C(t)$.

Now suppose $M<T$. Then $M\le T-1$, so $\mathcal C(M)$ applies with $s=M$: $\phi_M\ge\min\{1,\psi_M\}=1$, i.e. $\phi_M=1$. But $T$ is the first index with $\phi_t=1$ and $M<T$: a contradiction. Hence $T\le M$. The "in particular" clause is the special case of strictly increasing sequences in $[0,1]$, the greedy schedule being one of them by (a). $\square$

**Remark 2.5.** (a) The statement fixes $\rho\in(0,1)$, so $c>0$ is automatic; it is used in (a) and (b). (For $c=0$ and non-constant $d$ one would have $\chi^2(q_\phi\|q_{\phi_{t-1}})>0$ for every $\phi\ne\phi_{t-1}$ by Section 0.1, $\Phi_1=\emptyset$, and no schedule.) (b) Part (c) does not require the competing schedule to be monotone or to stay in $[0,1]$: backward steps and overshoots are allowed and never help. (c) The explicit bound in (b) is crude, but it shows that the greedy schedule always terminates, which the statement "reaches $\phi=1$" presupposes. It is of the type of the draft's Lemma L5 (a stage bound from a variance bound), with the global bound $F''\le D^2/4$ in place of L5's local sub-Gaussian hypothesis; L5 is not used. (d) The draft says "the supremum is attained, so it is a maximum" after L4; this is (a).

---

## 3. Lemma L6: the $\mathrm{BB}(1,p)$ prior

Fix an integer $p\ge1$ and $b_\pi>0$. The per-model weight of the untruncated $\mathrm{BB}(1,b_\pi)$ prior is
$$
w(k)=\frac{B(1+k,\,b_\pi+p-k)}{B(1,b_\pi)},\qquad k=0,\dots,p,\qquad B(a,b)=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}=\int_0^1\theta^{a-1}(1-\theta)^{b-1}d\theta\quad(a,b>0),
$$
and the untruncated prior is $p_u(S)=w(|S|)$ for $S\subseteq[p]$. Note $B(1,b)=1/b$. We use two facts about the Gamma function: $\Gamma(a+1)=a\Gamma(a)$ for $a>0$, and the integral representation of $B$ above. In this section $K$ denotes the model size (a random variable), not a kernel.

**Lemma 3.1 ($p_u$ is a probability; the law of the size).** $\sum_{S\subseteq[p]}p_u(S)=\sum_{k=0}^p\binom pkw(k)=1$. Consequently, with $K=|S|$ under $p_u$, $\mathbb P(K=k)=\binom pkw(k)$, and $w(k)>0$ for every $k$.

*Proof.* Let $f(\theta)=(1-\theta)^{b_\pi-1}/B(1,b_\pi)$, the $\mathrm{Beta}(1,b_\pi)$ density on $(0,1)$. Then $w(k)=\int_0^1\theta^k(1-\theta)^{p-k}f(\theta)\,d\theta>0$, and by the binomial theorem $\sum_k\binom pk\theta^k(1-\theta)^{p-k}=1$, so $\sum_k\binom pkw(k)=\int_0^1f(\theta)\,d\theta=1$. $\square$

**Theorem 3.2 (L6).** Let $K$ be the size under the untruncated prior.

(i) For $0\le k\le p-1$ and every $b_\pi>0$: $\dfrac{w(k+1)}{w(k)}=\dfrac{k+1}{b_\pi+p-k-1}$.

(ii) Let $b_\pi=p$. For $0\le k\le p-1$: $\dfrac{\mathbb P(K=k+1)}{\mathbb P(K=k)}=\dfrac{p-k}{2p-k-1}$. This ratio is $\le\tfrac12$ for $k\ge1$, with equality if and only if $k=1$; at $k=0$ it equals $p/(2p-1)\in(\tfrac12,1]$.

(iii) Let $b_\pi=p$. Then $\mathbb P(K=0)=\tfrac12$, and for every integer $m\ge1$, $\mathbb P(K\ge m)\le\dfrac p{2p-1}2^{1-m}\le2^{1-m}$.

(iv) Let $b_\pi=p$ and $k_{\max}\in\{0,\dots,p\}$. The capped prior is $p_{\rm cap}(S)=w(|S|)\mathbf 1\{|S|\le k_{\max}\}/W$ with $W=\sum_{k\le k_{\max}}\binom pkw(k)$. Then $\tfrac12\le W\le1$, $p_{\rm cap}(S)\le2p_u(S)$ for $|S|\le k_{\max}$, $p_{\rm cap}(S)=0$ for $|S|>k_{\max}$, and $\mathbb P_{\rm cap}(\mathcal A)\le2\mathbb P_u(\mathcal A)$ for every $\mathcal A\subseteq2^{[p]}$.

(v) Let $b_\pi=p$, and let $S_0\subseteq[p]$ with $s_0=|S_0|\le k_{\max}$. Then
$$
w(s_0)=\frac{p\,s_0!}{\prod_{i=0}^{s_0}(2p-i)}\ \ge\ \frac{s_0!}{2(2p)^{s_0}},\qquad\text{and}\qquad \log p_{\rm cap}(S_0)\ \ge\ -s_0\log(2p)-\log2 .
$$

*Proof.* (i) For $0\le k\le p-1$ all Beta arguments below are positive ($b_\pi+p-k-1\ge b_\pi>0$). Using $B(a,b)=\Gamma(a)\Gamma(b)/\Gamma(a+b)$ and that $a+b=b_\pi+p+1$ for both numerator and denominator,
$$
\frac{w(k+1)}{w(k)}=\frac{B(k+2,\,b_\pi+p-k-1)}{B(k+1,\,b_\pi+p-k)}=\frac{\Gamma(k+2)}{\Gamma(k+1)}\cdot\frac{\Gamma(b_\pi+p-k-1)}{\Gamma(b_\pi+p-k)}=\frac{k+1}{b_\pi+p-k-1},
$$
by $\Gamma(k+2)=(k+1)\Gamma(k+1)$ and $\Gamma(b_\pi+p-k)=(b_\pi+p-k-1)\Gamma(b_\pi+p-k-1)$.

(ii) By Lemma 3.1 and (i) with $b_\pi=p$,
$$
\frac{\mathbb P(K=k+1)}{\mathbb P(K=k)}=\frac{\binom p{k+1}}{\binom pk}\cdot\frac{w(k+1)}{w(k)}=\frac{p-k}{k+1}\cdot\frac{k+1}{2p-k-1}=\frac{p-k}{2p-k-1}.
$$
Since $2p-k-1>0$, the inequality $(p-k)/(2p-k-1)\le\tfrac12$ is equivalent to $2p-2k\le2p-k-1$, i.e. to $k\ge1$, with equality if and only if $k=1$. At $k=0$ the ratio is $p/(2p-1)$, which is $>\tfrac12$ because $2p>2p-1$, and $\le1$ because $p\ge1$.

(iii) $\mathbb P(K=0)=w(0)=B(1,2p)/B(1,p)=(1/2p)/(1/p)=\tfrac12$. By (ii), $\mathbb P(K=1)=\tfrac12\cdot\tfrac p{2p-1}$, and for $k\ge1$ an induction on (ii) gives $\mathbb P(K=k)\le2^{-(k-1)}\mathbb P(K=1)$. Hence for $m\ge1$
$$
\mathbb P(K\ge m)=\sum_{k=m}^p\mathbb P(K=k)\le\mathbb P(K=1)\sum_{k\ge m}2^{-(k-1)}=\mathbb P(K=1)\,2^{2-m}=\frac p{2p-1}\,2^{1-m}\le2^{1-m},
$$
using $p/(2p-1)\le1$. (For $m>p$ the left side is $0$.)

(iv) $W=\sum_{k\le k_{\max}}\binom pkw(k)=\mathbb P(K\le k_{\max})$ by Lemma 3.1, so $W\le1$ and $W\ge\mathbb P(K=0)=\tfrac12$ because $k_{\max}\ge0$. For $|S|\le k_{\max}$, $p_{\rm cap}(S)=w(|S|)/W\le2w(|S|)=2p_u(S)$; for $|S|>k_{\max}$, $p_{\rm cap}(S)=0\le2p_u(S)$. Summing over $S\in\mathcal A$ gives $\mathbb P_{\rm cap}(\mathcal A)\le2\mathbb P_u(\mathcal A)$.

(v) With $b_\pi=p$, $w(s_0)=B(1+s_0,2p-s_0)/B(1,p)=p\,\Gamma(1+s_0)\Gamma(2p-s_0)/\Gamma(2p+1)$. Since $s_0\le p$, the arguments are positive, and repeated use of $\Gamma(a+1)=a\Gamma(a)$ gives $\Gamma(2p+1)/\Gamma(2p-s_0)=\prod_{i=0}^{s_0}(2p-i)$, a product of $s_0+1$ positive factors each at most $2p$. Hence $w(s_0)=p\,s_0!/\prod_{i=0}^{s_0}(2p-i)\ge p\,s_0!/(2p)^{s_0+1}=s_0!/(2(2p)^{s_0})\ge1/(2(2p)^{s_0})$. Since $s_0\le k_{\max}$ and $W\le1$, $p_{\rm cap}(S_0)=w(s_0)/W\ge w(s_0)$, and taking logarithms, $\log p_{\rm cap}(S_0)\ge-s_0\log(2p)-\log2$. $\square$

**Remark 3.3 (the "in particular" clause).** (a) For fixed $k$, or for $k=k_p=o(p)$, (ii) gives $\mathbb P(K=k+1)/\mathbb P(K=k)=(p-k)/(2p-k-1)\to\tfrac12$ as $p\to\infty$; (iii) is the geometric tail. (b) The dimension-prior condition of the standard templates bounds the *size-class* probabilities, $\pi_p(s)\le c\,p^{-a}\pi_p(s-1)$ for all $s\ge1$, with $a>0$. Under $\mathrm{BB}(1,p)$, for $1\le s\le p/2+1$ the ratio is $\pi_p(s)/\pi_p(s-1)=(p-s+1)/(2p-s)\ge(p-s+1)/(2p)\ge\tfrac14$, so the condition fails as soon as $cp^{-a}<\tfrac14$, i.e. for all large $p$. (c) The *per-model* odds (i) are $w(k+1)/w(k)=(k+1)/(2p-k-1)$, which for fixed $k$ is at most $(k+1)/p=O(1/p)$ (not uniformly in $k$: at $k=p-1$ the ratio is $1$); the binomial factor $\binom p{k+1}/\binom pk=(p-k)/(k+1)$ cancels this. The failure of the templates is a statement about size classes, not about per-model odds.

**Remark 3.4 (parts (iii)–(v) need $b_\pi=p$).** For general $b_\pi>0$, $\mathbb P(K=0)=w(0)=B(1,b_\pi+p)/B(1,b_\pi)=b_\pi/(b_\pi+p)$, which equals $\tfrac12$ if and only if $b_\pi=p$. For instance $p=1$, $b_\pi=\tfrac14$ gives $\mathbb P(K=0)=\tfrac15$, so (iii) fails; with $k_{\max}=0$ the retained atom $\emptyset$ is multiplied by $5$, so (iv) fails; and with no cap and $S_0=\emptyset$, (v) would require $p_u(\emptyset)\ge\tfrac12$, which fails. The draft's L6 states "$b_\pi=p$" only in (ii); the paper's prior is $\mathrm{BB}(1,p)$, so this is a wording point for the draft (Section 6).

---

## 4. Proposition P6: kernel correctness

Fix a stage and write $\phi=\phi_t$, $\gamma=\gamma_\phi$ and $q=q_\phi$; so $\gamma>0$ on $\mathcal S$. It is convenient to extend $\gamma$ to all of $2^{[p]}$ by $\gamma(S')=0$ for $|S'|>k_{\max}$: this is literally $\gamma_\phi(S')=p(S')r(S')e^{\phi d(S')}$ with $p(S')=0$ beyond the cap.

**Lemma 4.1.** A $q$-reversible Markov kernel on $\mathcal S$ is $q$-invariant.

*Proof.* $(qK)(S')=\sum_Sq(S)K(S,S')=\sum_Sq(S')K(S',S)=q(S')\sum_SK(S',S)=q(S')$. $\square$

### 4.1 Metropolis–Hastings kernels with a cap

**Definition 4.2.** A *proposal kernel* is a Markov kernel $\Pi$ from $\mathcal S$ to $2^{[p]}$: for each $S\in\mathcal S$, $\Pi(S,\cdot)$ is a probability on $2^{[p]}$, which may put mass outside $\mathcal S$ (proposals beyond the cap). For $S\in\mathcal S$ and $S'\in\mathcal S\setminus\{S\}$ with $\Pi(S,S')>0$ define the acceptance probability
$$
\alpha(S,S')=\min\Big\{1,\ \frac{\gamma(S')\,\Pi(S',S)}{\gamma(S)\,\Pi(S,S')}\Big\}\in[0,1],
$$
which is well defined because $\gamma(S)>0$ and $\Pi(S,S')>0$. The Metropolis–Hastings kernel on $\mathcal S$ is
$$
K(S,S')=\Pi(S,S')\,\alpha(S,S')\ \ (S'\in\mathcal S\setminus\{S\},\ \Pi(S,S')>0),\qquad K(S,S')=0\ \ (S'\in\mathcal S\setminus\{S\},\ \Pi(S,S')=0),\qquad K(S,S)=1-\sum_{S'\in\mathcal S\setminus\{S\}}K(S,S').
$$
Operationally: propose $S'\sim\Pi(S,\cdot)$; if $S'\notin\mathcal S$ or $S'=S$, stay at $S$; otherwise move to $S'$ with probability $\alpha(S,S')$ and stay otherwise. Since $K(S,S)\ge1-\sum_{S'\ne S}\Pi(S,S')\ge0$, $K$ is a Markov kernel on $\mathcal S$. The operational rule is the definition; it agrees with the acceptance formula applied with the extended $\gamma$ to a proposal $S'\notin\mathcal S$, whatever finite value one assigns to the (undefined) reverse probability $\Pi(S',S)$, because $\gamma(S')=0$ makes the formula give $\alpha=0$.

**Proposition 4.3 (P6, Metropolis–Hastings).** For every proposal kernel $\Pi$, the kernel $K$ of Definition 4.2 is $q$-reversible, hence $q$-invariant. In particular the symmetry condition $\Pi(S,S')>0\Leftrightarrow\Pi(S',S)>0$ is not needed for correctness.

*Proof.* Let $S\ne S'$ in $\mathcal S$; we show $\gamma(S)K(S,S')=\gamma(S')K(S',S)$ (the case $S=S'$ is trivial, and dividing by $\bar Z_\phi$ turns $\gamma$ into $q$). If $\Pi(S,S')=0=\Pi(S',S)$, both sides are $0$. If $\Pi(S,S')>0=\Pi(S',S)$, then $\alpha(S,S')=\min\{1,0\}=0$, so $K(S,S')=0$, and $K(S',S)=0$ by definition: both sides are $0$. The case $\Pi(S,S')=0<\Pi(S',S)$ is symmetric. If both are positive,
$$
\gamma(S)K(S,S')=\gamma(S)\Pi(S,S')\min\Big\{1,\frac{\gamma(S')\Pi(S',S)}{\gamma(S)\Pi(S,S')}\Big\}=\min\{\gamma(S)\Pi(S,S'),\ \gamma(S')\Pi(S',S)\},
$$
which is symmetric in $(S,S')$, so it also equals $\gamma(S')K(S',S)$. Invariance follows from Lemma 4.1. $\square$

**Remark 4.4 (the three proposals of the statement, and what the symmetry condition buys).** The condition $\Pi(S,S')>0\Leftrightarrow\Pi(S',S)>0$ guarantees that every move proposed within $\mathcal S$ has a strictly positive acceptance probability, so that no proposal is wasted for structural reasons; it is a design property, not a correctness property.

1. *Add/delete.* Choose $j$ uniformly in $[p]$ and toggle it: $\Pi(S,S')=1/p$ if $|S\triangle S'|=1$, else $0$. Then $\Pi(S,S')=\Pi(S',S)$, the Hastings ratio is $1$ and $\alpha(S,S')=\min\{1,\gamma(S')/\gamma(S)\}$. From a model with $|S|=k_{\max}$, an addition proposes $S'\notin\mathcal S$ and is rejected.

2. *Uniform swap.* For $1\le|S|=k\le p-1$: choose $j$ uniformly in $S$ and $l$ uniformly in $[p]\setminus S$, and propose $S'=(S\setminus\{j\})\cup\{l\}$; so $\Pi(S,S')=1/(k(p-k))$ for each of the $k(p-k)$ swap neighbours, and $\Pi(S,S)=1$ if $S=\emptyset$ or $S=[p]$. A swap preserves the size, so it stays in $\mathcal S$, and $\Pi(S',S)=\Pi(S,S')$ since $|S'|=k$: the ratio is $1$.

3. *Swap with a neighbour list.* Let $N(j)\subseteq[p]\setminus\{j\}$ be a list for each $j$. If $S=\emptyset$, propose $S$ itself. Otherwise choose $j$ uniformly in $S$, then $l$ uniformly in $N(j)\setminus S$ (if this set is empty, propose $S$ itself), and propose $S'=(S\setminus\{j\})\cup\{l\}$. A swap neighbour $S'$ determines $(j,l)$ uniquely ($\{j\}=S\setminus S'$, $\{l\}=S'\setminus S$), so
$$
\Pi(S,S')=\frac1{|S|}\cdot\frac1{|N(j)\setminus S|}\quad\text{if }l\in N(j),\qquad
\Pi(S',S)=\frac1{|S'|}\cdot\frac1{|N(l)\setminus S'|}\quad\text{if }j\in N(l),\qquad\text{and }0\text{ otherwise}.
$$
Hence the symmetry condition holds for all $S,S'$ as soon as the neighbour relation is symmetric ($l\in N(j)\Leftrightarrow j\in N(l)$ for all $j\ne l$), and it fails in general otherwise (if $l\in N(j)$ but $j\notin N(l)$, take $S=\{j\}$ and $S'=\{l\}$, assuming $k_{\max}\ge1$). Two flags for the implementation: (a) a $k$-nearest-neighbour list built from the correlations of $X$ is *not* symmetric in general and must be symmetrised (take $l\in N(j)$ or $j\in N(l)$) for the statement's condition to hold; without symmetrisation the kernel is still reversible by Proposition 4.3, but moves whose reverse is impossible are always rejected. (b) Even with a symmetric relation, the Hastings ratio is $\Pi(S',S)/\Pi(S,S')=|N(j)\setminus S|/|N(l)\setminus S'|$, which is not $1$ in general; the acceptance probability must contain it. With the acceptance $\min\{1,\gamma(S')/\gamma(S)\}$ instead, $\gamma(S)K(S,S')=\Pi(S,S')\min\{\gamma(S),\gamma(S')\}$, which is symmetric in $(S,S')$ only if $\Pi(S,S')=\Pi(S',S)$; so reversibility fails whenever the two proposal probabilities differ, and in the computed examples (the check scripts in `review/`, not part of this proof) invariance fails as well.

### 4.2 Single-site Gibbs updates

**Proposition 4.5 (P6, Gibbs).** For $j\in[p]$ and $S\in\mathcal S$ let $\mathcal P_j(S)=\{S\setminus\{j\},\,S\cup\{j\}\}\cap\mathcal S$, which contains $S$ and has one or two elements. The single-site Gibbs kernel for coordinate $j$ is
$$
G_j(S,S')=\frac{\gamma(S')}{\sum_{S''\in\mathcal P_j(S)}\gamma(S'')}\ \ (S'\in\mathcal P_j(S)),\qquad G_j(S,S')=0\ \ (S'\notin\mathcal P_j(S)).
$$
$G_j$ is a Markov kernel on $\mathcal S$, $q$-reversible and hence $q$-invariant.

*Proof.* The rows sum to $1$ by construction. If $S'\in\mathcal P_j(S)$, then $S$ and $S'$ differ at most in the coordinate $j$, so $\{S\setminus\{j\},S\cup\{j\}\}=\{S'\setminus\{j\},S'\cup\{j\}\}$ and $\mathcal P_j(S')=\mathcal P_j(S)$; therefore
$$
\gamma(S)G_j(S,S')=\frac{\gamma(S)\gamma(S')}{\sum_{\mathcal P_j(S)}\gamma}=\frac{\gamma(S')\gamma(S)}{\sum_{\mathcal P_j(S')}\gamma}=\gamma(S')G_j(S',S).
$$
If $S'\notin\mathcal P_j(S)$, then also $S\notin\mathcal P_j(S')$ (otherwise $\mathcal P_j(S')=\mathcal P_j(S)$ by the previous sentence, and $S'\in\mathcal P_j(S')=\mathcal P_j(S)$), so both sides vanish. Invariance follows from Lemma 4.1. $\square$

$G_j(S,\cdot)$ is the conditional law of the $j$-th coordinate under $q$ given the other coordinates, restricted to the cap: if $|S|=k_{\max}$ and $j\notin S$, then $\mathcal P_j(S)=\{S\}$ and the update leaves $S$ unchanged.

### 4.3 Compositions and mixtures

**Proposition 4.6 (P6, sweeps and random scans).** Let $K_1,\dots,K_m$ be Markov kernels on $\mathcal S$.
(a) If each $K_i$ is $q$-invariant, the composition $K_1K_2\cdots K_m$ (a systematic sweep) is $q$-invariant.
(b) If $p_1,\dots,p_m\ge0$ are constants with $\sum_ip_i=1$ (frozen selection probabilities, not depending on the state), then $\sum_ip_iK_i$ is $q$-invariant if each $K_i$ is, and $q$-reversible if each $K_i$ is.
(c) A composition of $q$-reversible kernels need not be $q$-reversible (Example 4.7).

*Proof.* (a) By associativity, $q(K_1K_2\cdots K_m)=(qK_1)(K_2\cdots K_m)=q(K_2\cdots K_m)$, and induction on $m$. (b) $q\sum_ip_iK_i=\sum_ip_i\,qK_i=\sum_ip_iq=q$; and $q(S)\sum_ip_iK_i(S,S')=\sum_ip_iq(S')K_i(S',S)=q(S')\sum_ip_iK_i(S',S)$. (c) is Example 4.7. $\square$

**Example 4.7 (a Gibbs sweep that is not reversible).** Let $p=2$, $k_{\max}=2$, so $\mathcal S=\{\emptyset,\{1\},\{2\},\{1,2\}\}$, with $\gamma=(a,b,c,e)$ in this order, all positive. Consider the sweep $G_1G_2$ (update coordinate $1$, then coordinate $2$). From $\emptyset$, $G_1$ leads to $\emptyset$ or $\{1\}$; $G_2$ leads from $\emptyset$ to $\emptyset$ or $\{2\}$ and from $\{1\}$ to $\{1\}$ or $\{1,2\}$. Hence
$$
(G_1G_2)(\emptyset,\{1,2\})=G_1(\emptyset,\{1\})\,G_2(\{1\},\{1,2\})=\frac b{a+b}\cdot\frac e{b+e},\qquad
(G_1G_2)(\{1,2\},\emptyset)=G_1(\{1,2\},\{2\})\,G_2(\{2\},\emptyset)=\frac c{c+e}\cdot\frac a{a+c}.
$$
Reversibility would require $\gamma(\emptyset)(G_1G_2)(\emptyset,\{1,2\})=\gamma(\{1,2\})(G_1G_2)(\{1,2\},\emptyset)$, i.e.
$$
\frac{abe}{(a+b)(b+e)}=\frac{ace}{(c+e)(a+c)}\iff b(c+e)(a+c)=c(a+b)(b+e)\iff(c-b)(bc-ae)=0,
$$
where the last equivalence follows from expanding both sides: $b(c+e)(a+c)-c(a+b)(b+e)=(abc+bc^2+abe+bce)-(abc+ace+b^2c+bce)=bc(c-b)-ae(c-b)$. This is a necessary condition, from one pair of states. For $a=b=e=1$, $c=2$, the two sides are $\tfrac14$ and $\tfrac29$, so the sweep is not reversible; it is $q$-invariant by Proposition 4.6(a).

In fact the sweep is reversible if and only if $ae=bc$, i.e. if and only if $q$ is a product measure. The pair $(\emptyset,\{1\})$ gives $(G_1G_2)(\emptyset,\{1\})=G_1(\emptyset,\{1\})G_2(\{1\},\{1\})=\frac b{a+b}\cdot\frac b{b+e}$ and $(G_1G_2)(\{1\},\emptyset)=G_1(\{1\},\emptyset)G_2(\emptyset,\emptyset)=\frac a{a+b}\cdot\frac a{a+c}$, and balance $a\cdot\frac{b^2}{(a+b)(b+e)}=b\cdot\frac{a^2}{(a+b)(a+c)}$ reduces to $b(a+c)=a(b+e)$, i.e. $bc=ae$: necessity. Conversely, if $ae=bc$ then $q(S)\propto u_1^{\mathbf 1\{1\in S\}}u_2^{\mathbf 1\{2\in S\}}$ with $u_1=b/a$, $u_2=c/a$, so the two coordinates are independent under $q$. Then the conditional law of coordinate $1$ given coordinate $2$ does not depend on coordinate $2$, so $G_1=H_1\otimes I$ and likewise $G_2=I\otimes H_2$ for kernels $H_1,H_2$ on $\{0,1\}$ (each acts on one coordinate and ignores the other), and such tensor products commute: $G_1G_2=H_1\otimes H_2=G_2G_1$. A product of two commuting $q$-reversible kernels is $q$-reversible: writing $K^\ast$ for the adjoint in $L^2(q)$, $(G_1G_2)^\ast=G_2^\ast G_1^\ast=G_2G_1=G_1G_2$. $\square$

The equivalence "reversible iff product" is for a target on exactly two coordinates with no binding cap ($p=k_{\max}=2$). It does not extend verbatim to two updates inside a larger model, nor to a binding cap (audit 2026-10-15, Sol's audit of P6, finding 1). The correct general statement follows.

**Proposition 4.7a (two-coordinate sweeps in general; audit 2026-10-15).** Let $i\ne j$ in $[p]$, let $\gamma>0$ on $\mathcal S=\{S:|S|\le k_{\max}\}$ with $q=\gamma/\sum\gamma$, and let $G_i,G_j$ be the single-site Gibbs kernels of Proposition 4.5.
(a) If $k_{\max}\ge p$ (no binding cap), $G_iG_j$ is $q$-reversible if and only if, under $q$, the indicators $\mathbf 1\{i\in S\}$ and $\mathbf 1\{j\in S\}$ are conditionally independent given $S\setminus\{i,j\}$.
(b) If $1\le k_{\max}\le p-1$, $G_iG_j$ is never $q$-reversible. (If $k_{\max}=0$, $\mathcal S=\{\emptyset\}$ and everything is trivially reversible.)
In particular a sweep can be reversible for a target that is not a product: for $p=3$, no cap, $\gamma(S)=2^{\mathbf 1\{1\in S\}\mathbf 1\{3\in S\}}$, the sweep $G_1G_2$ is reversible (coordinate $2$ is independent of $(1,3)$), although coordinates $1$ and $3$ are dependent.

*Proof.* For $r\subseteq[p]\setminus\{i,j\}$ let $F_r=\{S\in\mathcal S:S\setminus\{i,j\}=r\}$ (the fibre of $r$). $G_i$ and $G_j$ change only coordinates $i$ and $j$, so $G_iG_j(S,S')=0$ unless $S,S'$ lie in the same fibre. Hence $q$-reversibility of $G_iG_j$ holds if and only if, for every $r$ with $F_r\neq\emptyset$, the restriction of $G_iG_j$ to $F_r$ is reversible with respect to $q(\cdot\mid F_r)\propto\gamma|_{F_r}$. On $F_r$, $G_i$ and $G_j$ are the single-site Gibbs kernels for the target $\gamma|_{F_r}$ on the set of allowed values of the pair of coordinates $(i,j)$, because the conditional law of coordinate $i$ given the others is computed within $F_r$.
(a) With no binding cap, every fibre is the full square $\{r,r\cup\{i\},r\cup\{j\},r\cup\{i,j\}\}$, and by Example 4.7 (with $(a,b,c,e)=\gamma(r),\gamma(r\cup\{i\}),\gamma(r\cup\{j\}),\gamma(r\cup\{i,j\})$) the restriction is reversible iff $\gamma(r)\gamma(r\cup\{i,j\})=\gamma(r\cup\{i\})\gamma(r\cup\{j\})$, i.e. iff $q(\cdot\mid F_r)$ is a product of its two coordinates. Requiring this for every $r$ is the conditional independence in (a).
(b) Since $0\le k_{\max}-1\le p-2$, there is $r\subseteq[p]\setminus\{i,j\}$ with $|r|=k_{\max}-1$. Its fibre is $F_r=\{r,\ r\cup\{i\},\ r\cup\{j\}\}$, since $|r\cup\{i,j\}|=k_{\max}+1$. Write $a=\gamma(r)$, $b=\gamma(r\cup\{i\})$, $c=\gamma(r\cup\{j\})$. From $r\cup\{j\}$, $G_i$ stays put (adding $i$ would exceed the cap) and $G_j$ moves to $r$ with probability $a/(a+c)$; from $r$, $G_i$ stays at $r$ with probability $a/(a+b)$ and then $G_j$ moves to $r\cup\{j\}$ with probability $c/(a+c)$. Paths through $r\cup\{i\}$ cannot end at $r\cup\{j\}$, because $G_j$ fixes $r\cup\{i\}$ (adding $j$ exceeds the cap). So
$$
G_iG_j(r,r\cup\{j\})=\frac a{a+b}\cdot\frac c{a+c},\qquad G_iG_j(r\cup\{j\},r)=1\cdot\frac a{a+c},
$$
and detailed balance $a\cdot\frac{ac}{(a+b)(a+c)}=c\cdot\frac a{a+c}$ would force $a/(a+b)=1$, i.e. $b=0$, which is impossible. $\square$

Numerical check: `proofs/_audit/group_B/check_audit_B.py`, checks P6.F1. These cover Sol's example, 100 conditionally independent and 100 generic targets for $p=3$ without a cap, and 200 capped cases with $(p,k_{\max})\in\{(2,1),(3,1),(3,2),(4,2),(4,3)\}$, half of them product targets.

**Remark 4.8 (state-dependent selection probabilities; the draft's remark after P6).** If the mixing probabilities depend on the current state, $\tilde K(S,\cdot)=\sum_ip_i(S)K_i(S,\cdot)$ is a Markov kernel but need not be $q$-invariant even when every $K_i$ is $q$-reversible. The draft's example, on the two-point space $\{0,1\}$ (which is $\mathcal S$ for $p=k_{\max}=1$): $q$ uniform, $K_1(0,1)=K_1(1,0)=1$ (the flip, which is $q$-reversible) and $K_0=\mathrm{Id}$ (the identity kernel); with $p_1(S)=\mathbf 1\{S=0\}$ one gets $\tilde K(0,\cdot)=\tilde K(1,\cdot)=\delta_1$ and $q\tilde K=\delta_1\ne q$. In the particle algorithm, "selection probabilities computed from the current population and applied to its own members" are a function of the particles' states, hence of this type on the product space $\mathcal S^N$; Proposition 5.10 shows that this bias reaches the evidence estimate. The *frozen* selection probabilities of P6 and P7 are constants given $y$ (and the pilot), fixed before the population is drawn.

**Remark 4.9 (which target).** The move kernels of stage $t$ must be invariant for $q_{\phi_t}$, the target *after* the reweighting of stage $t$. This is the form in which P7 uses P6 (hypothesis (H0) below).

---

## 5. Proposition P7: frozen schedules, unbiasedness and lower confidence bounds

### 5.1 The particle system

The hypotheses, stated once and used throughout. They are sufficient conditions; Section 5.3 records which parts of them the proofs use.

**(H0) Frozen settings.** The following are deterministic (given the data $y$; see Section 5.5 for the pilot): the particle number $N\ge1$; the stage number $T\ge1$ and the schedule $0=\phi_0<\phi_1<\dots<\phi_T=1$; the move counts $m_t\ge0$; for each $t\in[T]$ and $\ell\in[m_t]$ a Markov kernel $K_{t,\ell}$ on $\mathcal S$ that is $q_{\phi_t}$-invariant (for instance any kernel of Section 4); and the resampling kernels $R_t$ of (H2) (or their counterparts in Theorem 5.7). Write $\mathcal K_t=K_{t,1}K_{t,2}\cdots K_{t,m_t}$, with $\mathcal K_t=\mathrm{Id}$ (the identity kernel) if $m_t=0$. The stage-$t$ potential is
$$
G_t(S)=\exp\{(\phi_t-\phi_{t-1})d(S)\}=\frac{\gamma_{\phi_t}(S)}{\gamma_{\phi_{t-1}}(S)}>0,\qquad S\in\mathcal S,
$$
so the weights $w_t^i=G_t(X_{t-1}^i)$ of Section 2.3 are strictly positive and the normalised weights $W_t^i(x)=G_t(x^i)/\sum_{k=1}^NG_t(x^k)$ are well defined for every $x\in\mathcal S^N$. ($G_t$ with a stage index is a potential; $G_j$ in Section 4 was a Gibbs kernel.)

**(H1) Initialisation.** $X_0=(X_0^1,\dots,X_0^N)$ is i.i.d. from $q_0=\pi_0$, and the constant $\bar Z_0$ used in $\widehat Z$ is the exact normalising constant of $\gamma_0$.

**(H2) Resampling with unbiased offspring counts given the population, at every stage.** For each $t\in[T]$, $R_t$ is a Markov kernel from $\mathcal S^N$ to $[N]^N$ (the ancestor vectors $a=(a^1,\dots,a^N)$) such that for every population $x\in\mathcal S^N$ and every $i\in[N]$,
$$
\sum_{a\in[N]^N}R_t(x,a)\,\#\{j:a^j=i\}=N\,W_t^i(x). \tag{5.1}
$$
$R_t$ may depend on the particle values as well as on the weights, but (5.1) must hold for every population $x$, not only on average over the populations sharing a weight vector (Proposition 5.13 shows the difference matters); any private randomness of the scheme, such as the uniforms of stratified or systematic resampling, is integrated out in $R_t$. The resampled population is $\widehat X_t^j=X_{t-1}^{A_t^j}$ with $A_t\sim R_t(X_{t-1},\cdot)$ *given the whole past* $\mathcal F_{t-1}$, as (5.2) says: the scheme is applied afresh to the current population, with randomness independent of the past. (audit 2026-10-15) This is stronger than "$\mathbb E[\#\{j:A_t^j=i\}\mid X_{t-1}]=NW_t^i(X_{t-1})$", conditioning on the current population alone: a rule whose randomness is correlated with earlier stages can satisfy that and still bias $\widehat Z$ (Proposition 5.14). What the proofs use is the offspring identity given $\mathcal F_{t-1}$ (Lemma 5.1(c)). The fresh-randomness form (5.2) is one sufficient condition; a history-dependent kernel $R_t(h_{t-1},\cdot)$ satisfying (5.1) for every history $h_{t-1}$ is another, and every proof below goes through for it verbatim.

**(H3) Mutation.** Given the resampled population, the particles are moved independently, each through $K_{t,1}$, then $K_{t,2}$, …, then $K_{t,m_t}$: with $Y_{t,0}=\widehat X_t$, the conditional law of $Y_{t,\ell}$ given everything generated before it is $\prod_{j=1}^NK_{t,\ell}(Y_{t,\ell-1}^j,\cdot)$. The population at the end of stage $t$ is $X_t=Y_{t,m_t}$. The *same* kernel is applied to every particle.

The trajectory is $\omega=\big(X_0,(A_t,Y_{t,1},\dots,Y_{t,m_t})_{t=1}^T\big)$, an element of the finite set $\Omega=\mathcal S^N\times\prod_{t=1}^T\big([N]^N\times(\mathcal S^N)^{m_t}\big)$, and (H1)–(H3) say that its law is
$$
P(\omega)=\prod_{j=1}^Nq_0(X_0^j)\ \prod_{t=1}^T\Big[R_t(X_{t-1},A_t)\prod_{\ell=1}^{m_t}\prod_{j=1}^NK_{t,\ell}\big(Y_{t,\ell-1}^j,Y_{t,\ell}^j\big)\Big]. \tag{5.2}
$$
This is the algorithm of Section 2.3 of the draft, with step 2(c) read as (5.1). The evidence estimate is
$$
\widehat Z=m(\emptyset)\,\bar Z_0\,\Pi_T,\qquad \Pi_t:=\prod_{s=1}^t\Big(\frac1N\sum_{i=1}^NG_s(X_{s-1}^i)\Big),\qquad \Pi_0:=1 . \tag{5.3}
$$
($\Pi_t$ here is a number; the proposal kernel of P6 appears in this section only through the kernels $K_{t,\ell}$.) Since $\Omega$ is finite, every random variable below is bounded and every expectation exists. We write $\mathcal F_{t-1}$ for the $\sigma$-field generated by the trajectory up to and including $X_{t-1}$, $\mathcal F_{t-1}^A$ for the one generated additionally by $A_t$, and $\mathcal F_{t,\ell}$ for the one generated up to and including $Y_{t,\ell}$ (so $\mathcal F_{t,0}=\mathcal F_{t-1}^A$ and $\mathcal F_{t,m_t}=\mathcal F_t$). Note that $\Pi_t$ is $\mathcal F_{t-1}$-measurable: the stage-$t$ weights are computed on $X_{t-1}$, and the moves of stage $T$ do not enter $\widehat Z$.

### 5.2 Two one-step identities

**Lemma 5.1.** Let the trajectory have a law in which, for every $t$, every $\ell\in[m_t]$ and every $j\in[N]$, the conditional law of the single particle $Y_{t,\ell}^j$ given $\mathcal F_{t,\ell-1}$ is $K_{t,\ell}(Y_{t,\ell-1}^j,\cdot)$. (This holds under (5.2) and under (5.5) below, where the conditional law of the whole vector $Y_{t,\ell}$ is the product $\prod_jK_{t,\ell}(Y_{t,\ell-1}^j,\cdot)$ and the single-particle law is its $j$-th marginal; it also holds for laws in which the particles' moves are dependent, for instance driven by common random numbers, as long as each particle's conditional marginal is $K_{t,\ell}$.) Then for every $t\in[T]$, every $f:\mathcal S\to\mathbb R$ and every vector of coefficients $\eta=(\eta^1,\dots,\eta^N)$:

(a) for $\ell\in[m_t]$, if $\eta$ is $\mathcal F_{t,\ell-1}$-measurable: $\ \mathbb E\big[\tfrac1N\sum_j\eta^jf(Y_{t,\ell}^j)\,\big|\,\mathcal F_{t,\ell-1}\big]=\tfrac1N\sum_j\eta^j(K_{t,\ell}f)(Y_{t,\ell-1}^j)$;

(b) if $\eta$ is $\mathcal F_{t-1}^A$-measurable: $\ \mathbb E\big[\tfrac1N\sum_j\eta^jf(X_t^j)\,\big|\,\mathcal F_{t-1}^A\big]=\tfrac1N\sum_j\eta^j(\mathcal K_tf)(\widehat X_t^j)$;

(c) if moreover the conditional law of $A_t$ given $\mathcal F_{t-1}$ is $R_t(X_{t-1},\cdot)$ for a kernel $R_t$ satisfying (5.1) (as under (5.2)), then for every $g:\mathcal S\to\mathbb R$: $\ \mathbb E\big[\tfrac1N\sum_jg(\widehat X_t^j)\,\big|\,\mathcal F_{t-1}\big]=\sum_iW_t^i(X_{t-1})\,g(X_{t-1}^i)$.

*Proof.* (a) By hypothesis $\mathbb E[f(Y_{t,\ell}^j)\mid\mathcal F_{t,\ell-1}]=(K_{t,\ell}f)(Y_{t,\ell-1}^j)$; multiply by the $\mathcal F_{t,\ell-1}$-measurable $\eta^j$ and average over $j$. (That (5.2), and likewise (5.5) below, have the product conditional law is read off their factorisations: the factors after the $(t,\ell)$ block are kernels in their own variables and sum to one when those variables are summed out.) (b) We show by backward induction on $r\in\{0,1,\dots,m_t\}$ that $\mathbb E[f(X_t^j)\mid\mathcal F_{t,r}]=(K_{t,r+1}\cdots K_{t,m_t}f)(Y_{t,r}^j)$ (the empty composition is $\mathrm{Id}$). For $r=m_t$ this reads $f(X_t^j)=f(Y_{t,m_t}^j)$. If it holds for $r\ge1$, then by the tower property and (a) with $\ell=r$,
$$
\mathbb E[f(X_t^j)\mid\mathcal F_{t,r-1}]=\mathbb E\big[(K_{t,r+1}\cdots K_{t,m_t}f)(Y_{t,r}^j)\mid\mathcal F_{t,r-1}\big]=(K_{t,r}K_{t,r+1}\cdots K_{t,m_t}f)(Y_{t,r-1}^j).
$$
At $r=0$ this gives $\mathbb E[f(X_t^j)\mid\mathcal F_{t-1}^A]=(\mathcal K_tf)(\widehat X_t^j)$; multiply by $\eta^j$ and average. (c) $\tfrac1N\sum_jg(\widehat X_t^j)=\tfrac1N\sum_jg(X_{t-1}^{A_t^j})=\tfrac1N\sum_ig(X_{t-1}^i)\,\#\{j:A_t^j=i\}$. The conditional law of $A_t$ given $\mathcal F_{t-1}$ is $R_t(X_{t-1},\cdot)$ (under (5.2) this is read off the factorisation), so by (5.1), $\mathbb E[\#\{j:A_t^j=i\}\mid\mathcal F_{t-1}]=NW_t^i(X_{t-1})$, and the claim follows since $g(X_{t-1}^i)$ is $\mathcal F_{t-1}$-measurable. $\square$

**Lemma 5.2 (reweighting).** For $\phi,\phi'\in\mathbb R$ and $h:\mathcal S\to\mathbb R$, $\ q_\phi\big(e^{(\phi'-\phi)d}h\big)=\dfrac{\bar Z_{\phi'}}{\bar Z_\phi}\,q_{\phi'}(h)$. In particular $q_{\phi_{t-1}}(G_th)=(\bar Z_{\phi_t}/\bar Z_{\phi_{t-1}})\,q_{\phi_t}(h)$.

*Proof.* $\sum_S\gamma_\phi(S)e^{(\phi'-\phi)d(S)}h(S)/\bar Z_\phi=\sum_S\gamma_{\phi'}(S)h(S)/\bar Z_\phi=(\bar Z_{\phi'}/\bar Z_\phi)\,q_{\phi'}(h)$. $\square$

### 5.3 Unbiasedness

**Theorem 5.3 (P7(i), with the unnormalised particle measure).** Under (H0)–(H3), for every $t\in\{0,1,\dots,T\}$ and every $f:\mathcal S\to\mathbb R$,
$$
\mathbb E\Big[\Pi_t\cdot\frac1N\sum_{j=1}^Nf(X_t^j)\Big]=\frac{\bar Z_{\phi_t}}{\bar Z_0}\,q_{\phi_t}(f). \tag{5.4}
$$
In particular ($t=T$, $f\equiv1$) $\mathbb E[\Pi_T]=\bar Z_1/\bar Z_0$ and, by (0.1),
$$
\mathbb E[\widehat Z]=m(\emptyset)\bar Z_0\cdot\frac{\bar Z_1}{\bar Z_0}=m(\emptyset)\bar Z_1=Z;
$$
and ($t=T$, general $f$) $\mathbb E\big[\Pi_T\cdot\tfrac1N\sum_jf(X_T^j)\big]=(\bar Z_1/\bar Z_0)\,\pi(f)$: the unnormalised particle estimate of every posterior expectation is unbiased.

*Proof.* Induction on $t$. For $t=0$, $\Pi_0=1$ and by (H1) $\mathbb E[\tfrac1N\sum_jf(X_0^j)]=q_0(f)=(\bar Z_0/\bar Z_0)q_0(f)$. Let $t\ge1$ and assume (5.4) for $t-1$ and all $f$. Since $\Pi_t$ is $\mathcal F_{t-1}$-measurable,
$$
\mathbb E\Big[\Pi_t\frac1N\sum_jf(X_t^j)\Big]=\mathbb E\Big[\Pi_t\,\mathbb E\Big[\frac1N\sum_jf(X_t^j)\,\Big|\,\mathcal F_{t-1}\Big]\Big].
$$
Put $h:=\mathcal K_tf$. By the tower property, Lemma 5.1(b) (with $\eta\equiv1$) and then Lemma 5.1(c) with $g=h$,
$$
\mathbb E\Big[\frac1N\sum_jf(X_t^j)\,\Big|\,\mathcal F_{t-1}\Big]=\mathbb E\Big[\frac1N\sum_jh(\widehat X_t^j)\,\Big|\,\mathcal F_{t-1}\Big]=\sum_iW_t^i(X_{t-1})\,h(X_{t-1}^i).
$$
Multiplying by $\Pi_t=\Pi_{t-1}\cdot\tfrac1N\sum_kG_t(X_{t-1}^k)$ and using $W_t^i(X_{t-1})=G_t(X_{t-1}^i)/\sum_kG_t(X_{t-1}^k)$,
$$
\Pi_t\sum_iW_t^i(X_{t-1})\,h(X_{t-1}^i)=\Pi_{t-1}\cdot\frac1N\sum_iG_t(X_{t-1}^i)\,h(X_{t-1}^i)=\Pi_{t-1}\cdot\frac1N\sum_ig(X_{t-1}^i),\qquad g:=G_t\cdot h=G_t\cdot(\mathcal K_tf).
$$
By (H0), $g$ is a fixed function on $\mathcal S$ (it does not depend on $\omega$), so the induction hypothesis applies to it:
$$
\mathbb E\Big[\Pi_t\frac1N\sum_jf(X_t^j)\Big]=\mathbb E\Big[\Pi_{t-1}\frac1N\sum_ig(X_{t-1}^i)\Big]=\frac{\bar Z_{\phi_{t-1}}}{\bar Z_0}\,q_{\phi_{t-1}}\big(G_t\,\mathcal K_tf\big)=\frac{\bar Z_{\phi_{t-1}}}{\bar Z_0}\cdot\frac{\bar Z_{\phi_t}}{\bar Z_{\phi_{t-1}}}\,q_{\phi_t}(\mathcal K_tf)
$$
by Lemma 5.2. Finally, each $K_{t,\ell}$ is $q_{\phi_t}$-invariant by (H0), so $\mathcal K_t$ is $q_{\phi_t}$-invariant by Proposition 4.6(a), and $q_{\phi_t}(\mathcal K_tf)=(q_{\phi_t}\mathcal K_t)(f)=q_{\phi_t}(f)$. This is (5.4) for $t$. $\square$

*Where each hypothesis enters, and what is not used.* (H0): $g$ is a fixed function (frozen kernels and schedule), and the kernels of stage $t$ are invariant for $q_{\phi_t}$, the temperature of the weights just computed; the strict monotonicity of the schedule is not used (Lemma 5.2 holds for any $\phi,\phi'$), only $\phi_0=0$ and $\phi_T=1$. (H1): the base case uses only that each $X_0^j$ has law $q_0$, so that $\mathbb E[\tfrac1N\sum_jf(X_0^j)]=q_0(f)$; independence of the initial particles is not used (for instance $X_0^1=\dots=X_0^N$ drawn once from $q_0$ would do), and $\bar Z_0$ must be exact in (5.3). (H2): only the expected offspring counts (5.1), through Lemma 5.1(c). (H3): only the conditional marginal law of each particle given the past, which is the hypothesis of Lemma 5.1, and the fact that all particles use the same kernel (Remark 5.11); the independence across particles built into (5.2) is not used in the proof of (5.4), which goes through verbatim for any law satisfying the hypothesis of Lemma 5.1 and the conditional offspring identity (5.1), for instance with moves driven by common random numbers (where the joint conditional law of $Y_{t,\ell}$ is not a product but each marginal is $K_{t,\ell}$).

**Lemma 5.4 (the four schemes satisfy (5.1)).** Let $\Delta_N=\{W\in[0,1]^N:\sum_iW^i=1\}$, let $W\in\Delta_N$, $C_0=0$ and $C_i=\sum_{k\le i}W^k$, so $(C_{i-1},C_i]$ has length $W^i$ and these intervals tile $(0,1]$. Each of the following ancestor laws has $\mathbb E\#\{j:A^j=i\}=NW^i$ for every $i$, for every fixed $W$; applied with $W=W_t(x)$ for each population $x$, this is (5.1).
(a) *Multinomial:* $A^1,\dots,A^N$ i.i.d. with $\mathbb P(A^j=i)=W^i$.
(b) *Residual:* $n_i=\lfloor NW^i\rfloor$ offspring of $i$ are assigned deterministically; the remaining $R=N-\sum_in_i$ ancestors are i.i.d. with probabilities $(NW^i-n_i)/R$ (nothing is drawn if $R=0$).
(c) *Stratified:* $U_1,\dots,U_N$ independent with $U_j$ uniform on $((j-1)/N,j/N]$, and $A^j=i$ if and only if $U_j\in(C_{i-1},C_i]$.
(d) *Systematic:* $U$ uniform on $(0,1/N]$, $U_j=U+(j-1)/N$, and $A^j=i$ if and only if $U_j\in(C_{i-1},C_i]$.
In (c) and (d) the particles may be ordered by any rule that is a function of the current population (sorting by a statistic), since the computation holds for every fixed order.

*Proof.* (a) $\mathbb E\#\{j:A^j=i\}=\sum_j\mathbb P(A^j=i)=NW^i$. (b) The probabilities $(NW^i-n_i)/R$ are nonnegative and sum to $(N-\sum_in_i)/R=1$; $\mathbb E\#\{j:A^j=i\}=n_i+R\cdot(NW^i-n_i)/R=NW^i$. (c) Writing $\lambda$ for Lebesgue measure and using that $U_j$ has density $N$ on its stratum,
$$
\mathbb E\#\{j:A^j=i\}=\sum_{j=1}^N\mathbb P\big(U_j\in(C_{i-1},C_i]\big)=\sum_{j=1}^NN\lambda\Big((C_{i-1},C_i]\cap\big(\tfrac{j-1}N,\tfrac jN\big]\Big)=N\lambda\big((C_{i-1},C_i]\cap(0,1]\big)=NW^i,
$$
because the strata $((j-1)/N,j/N]$ tile $(0,1]$. (d) $U$ has density $N$ on $(0,1/N]$, so $\mathbb P(U+(j-1)/N\in(C_{i-1},C_i])=N\lambda\big((C_{i-1},C_i]\cap((j-1)/N,j/N]\big)$, the same summands as in (c), and the sum is again $NW^i$. $\square$

Under multinomial resampling every ancestor label $A^j$ has the law $W$; under stratified and systematic resampling the labels $A^j$ need not have identical laws (for $N=2$ and $W=(0.3,0.7)$, systematic resampling gives $A^1=1$ with probability $0.6$ and $A^2=1$ with probability $0$), which matters only for Remark 5.11.

### 5.4 Lower confidence bounds and the log-bias

**Theorem 5.5 (P7(ii)).** Let $\widehat Z_1,\dots,\widehat Z_R$ be the estimates of $R\ge1$ islands run under the same frozen settings, each satisfying $\mathbb E[\widehat Z_r]=Z$ (Theorem 5.3), and let $M_R=\tfrac1R\sum_r\widehat Z_r$ (the draft's $\bar Z_R$; the subscript is an island count, not a temperature).
(a) For every $\alpha\in(0,1)$, $\mathbb P(Z\ge\alpha M_R)\ge1-\alpha$. This holds for every $R$, including $R=1$, and does not require the islands to be independent.
(b) $\sigma_Z^2:=\mathrm{Var}(\widehat Z)<\infty$ automatically, because $\widehat Z$ takes finitely many values ($\Omega$ is finite). Suppose the islands are independent and $R\ge2$, and let $s_R^2=\tfrac1{R-1}\sum_r(\widehat Z_r-M_R)^2$ and $z_{1-\alpha/2}$ be the standard normal quantile. If $\sigma_Z^2>0$, then
$$
\mathbb P\Big(Z\in\Big[M_R-z_{1-\alpha/2}\frac{s_R}{\sqrt R},\ M_R+z_{1-\alpha/2}\frac{s_R}{\sqrt R}\Big]\Big)\longrightarrow1-\alpha\qquad(R\to\infty).
$$
If $\sigma_Z^2=0$ then $\widehat Z=Z$ almost surely and the interval covers $Z$ with probability $1$.

*Proof.* (a) $M_R\ge0$ and $\mathbb E[M_R]=Z>0$. By Markov's inequality, $\mathbb P(M_R>Z/\alpha)\le\alpha\,\mathbb E[M_R]/Z=\alpha$, so $\mathbb P(\alpha M_R\le Z)\ge1-\alpha$. (b) Let $\sigma_Z^2>0$. By the central limit theorem for i.i.d. variables with finite positive variance, $\sqrt R(M_R-Z)/\sigma_Z\Rightarrow N(0,1)$; by the strong law of large numbers $s_R^2\to\sigma_Z^2>0$ almost surely. On the event $\{s_R>0\}$ the coverage event is $\{|\sqrt R(M_R-Z)/s_R|\le z_{1-\alpha/2}\}$, whose probability tends to $1-\alpha$ by Slutsky's theorem; and $\mathbb P(s_R=0)=\sum_v\mathbb P(\widehat Z=v)^R\to0$ because $\max_v\mathbb P(\widehat Z=v)<1$ when $\sigma_Z^2>0$ (the sum is over the finitely many values $v$ of $\widehat Z$). Hence the coverage probability tends to $1-\alpha$. The case $\sigma_Z^2=0$ is immediate. $\square$

The bound (a) is exact for every $R$; the interval (b) is asymptotic in $R$, and nothing is claimed about its coverage at finite $R$ (the draft's remark after P7, and Theorem T5, concern that).

**Theorem 5.6 (P7(iii)).** Under (H0)–(H3), $\widehat Z>0$ surely and $\mathbb E[\log\widehat Z]\le\log Z$, with equality if and only if $\widehat Z=Z$ almost surely.

*Proof.* Every factor in (5.3) is strictly positive ($m(\emptyset)>0$, $\bar Z_0>0$, $G_s>0$), so $\widehat Z>0$ and $\log\widehat Z$ is a bounded random variable. By Jensen's inequality for the concave function $\log$, $\mathbb E[\log\widehat Z]\le\log\mathbb E[\widehat Z]=\log Z$ (Theorem 5.3); since $\log$ is strictly concave, equality holds if and only if $\widehat Z$ is almost surely constant, i.e. equal to its mean $Z$. $\square$

### 5.5 The pilot

**(H4) Independent pilot.** Let $\vartheta=(N,T,(\phi_t),(m_t),(K_{t,\ell}),(R_t))$ be the settings of (H0), and suppose $\vartheta=\vartheta(y,\xi)$ is a measurable function of the data and of the randomness $\xi$ of a pilot run, such that for every $(y,\xi)$ the settings $\vartheta(y,\xi)$ satisfy (H0) and (H2) (schedule from $0$ to $1$, kernels invariant for the temperatures chosen, resampling kernels satisfying (5.1)). Suppose that, conditionally on $(y,\xi)$, each island is generated by (5.2) with settings $\vartheta(y,\xi)$ from randomness independent of $\xi$, and that the islands are conditionally independent given $(y,\xi)$.

**Corollary 5.6a.** Under (H1), (H3) and (H4): $\mathbb E[\widehat Z\mid y,\xi]=Z(y)$, hence $\mathbb E[\widehat Z\mid y]=Z(y)$; Theorem 5.5(a) and Theorem 5.6 hold conditionally on $(y,\xi)$ and, by integrating over $\xi$, unconditionally given $y$; Theorem 5.5(b) holds conditionally on $(y,\xi)$.

*Proof.* Conditionally on $(y,\xi)$ the settings are constants satisfying (H0) and (H2), so Theorems 5.3, 5.5 and 5.6 apply conditionally; $Z(y)$ does not depend on $\xi$. The inequalities $\mathbb P(Z\ge\alpha M_R\mid y,\xi)\ge1-\alpha$ and $\mathbb E[\log\widehat Z\mid y,\xi]\le\log Z(y)$ integrate over $\xi$ (integrability: for every setting, $m(\emptyset)\bar Z_0e^{\min d}\le\widehat Z\le m(\emptyset)\bar Z_0e^{\max d}$ because the schedule increases from $0$ to $1$, so $\widehat Z$ and $\log\widehat Z$ are bounded uniformly in $\xi$). $\square$

*Flags.* (a) (H4) fails if an island reuses the pilot's random stream (for instance the same seed): then the settings and the island's randomness are dependent, the conditional argument breaks, and (i) is not guaranteed. Islands must use random streams independent of the pilot and of each other. (b) The limiting coverage $1-\alpha$ of the CLT interval does not integrate over the pilot in general: if the pilot's choice makes $\sigma_Z^2(y,\xi)=0$ with positive probability (coverage $1$ there), the unconditional limit exceeds $1-\alpha$. The interval is a conditional statement, which is what the draft says ("all statements are then conditional on the pilot").

### 5.6 What is and is not needed: variants and counterexamples

**Theorem 5.7 (resampling at some stages only, with carried weights; adaptive resampling decisions).** Replace (H2) by the following. The state after stage $t$ is $(X_t,u_t)$ with weights $u_t\in(0,\infty)^N$, and $u_0=(1,\dots,1)$. At stage $t$:
1. compute $\tilde u_t^i=u_{t-1}^iG_t(X_{t-1}^i)$;
2. draw a decision $I_t\in\{0,1\}$ from a kernel $\Delta_t(h_{t-1},\cdot)$ on $\{0,1\}$, where $h_{t-1}$ is the history up to $X_{t-1}$ (which determines $\tilde u_t$): i.e. by any rule that depends on the history and on private randomness, the latter independent, given the history, of the resampling and move randomness that follows. Examples: a frozen set of resampling stages $I_t=\mathbf 1\{t\in\mathcal T_R\}$, or an ESS rule $I_t=\mathbf 1\{(\sum_i\tilde u_t^i)^2/\sum_i(\tilde u_t^i)^2<\tau N\}$ with a threshold $\tau\in(0,1]$;
3. if $I_t=1$: draw $A_t$ from a kernel $R_t\big((X_{t-1},\tilde u_t),\cdot\big)$ on $[N]^N$ satisfying, for every population and weight vector, $\sum_aR_t((x,\tilde u),a)\#\{j:a^j=i\}=N\tilde u^i/\sum_k\tilde u^k$; set $\widehat X_t^j=X_{t-1}^{A_t^j}$ and $u_t^j=1$. If $I_t=0$: $A_t=(1,\dots,N)$, so $\widehat X_t=X_{t-1}$, and $u_t=\tilde u_t$;
4. move as in (H3).

The trajectory is now $\omega=\big(X_0,(I_t,A_t,Y_{t,1},\dots,Y_{t,m_t})_{t=1}^T\big)$ and its law is
$$
P(\omega)=\prod_{j=1}^Nq_0(X_0^j)\ \prod_{t=1}^T\Big[\Delta_t(h_{t-1},I_t)\Big(I_t\,R_t\big((X_{t-1},\tilde u_t),A_t\big)+(1-I_t)\,\mathbf 1\{A_t=(1,\dots,N)\}\Big)\prod_{\ell=1}^{m_t}\prod_{j=1}^NK_{t,\ell}\big(Y_{t,\ell-1}^j,Y_{t,\ell}^j\big)\Big], \tag{5.5}
$$
where $\mathcal F_{t-1}$ now includes the past decisions, and $\mathcal F_{t-1}^A$ includes $I_t$ and $A_t$. (What the proof uses is (5.5) itself: given $h_{t-1}$ and $I_t$, the ancestor vector has the law $R_t((X_{t-1},\tilde u_t),\cdot)$ on $\{I_t=1\}$ and is the identity on $\{I_t=0\}$, and the moves have the laws $K_{t,\ell}$. The independence of the decision's private randomness required in step 2 is a sufficient condition on the implementation for (5.5) to hold; an implementation that reuses, say, the uniform of systematic resampling for the decision is outside that condition, and is covered only if its trajectory law still has the form (5.5).) Define $L_t=\prod_{s\le t:\,I_s=1}\big(\tfrac1N\sum_i\tilde u_s^i\big)$ ($L_0=1$) and the weighted estimator
$$
\widehat Z_w=m(\emptyset)\,\bar Z_0\,\Upsilon_T,\qquad \Upsilon_t:=L_t\cdot\frac1N\sum_{i=1}^Nu_t^i\qquad(\Upsilon_0=1;\ \text{the draft's }\Lambda\text{ is the path length and is not used here}).
$$
Then, under (H0), (H1), (H3) and the above, for every $t$ and $f$,
$$
\mathbb E\Big[L_t\cdot\frac1N\sum_ju_t^jf(X_t^j)\Big]=\frac{\bar Z_{\phi_t}}{\bar Z_0}\,q_{\phi_t}(f), \tag{5.6}
$$
and in particular $\mathbb E[\Upsilon_T]=\bar Z_1/\bar Z_0$ and $\mathbb E[\widehat Z_w]=Z$. When $I_t\equiv1$, $u_t\equiv1$, $\tilde u_t^i=G_t(X_{t-1}^i)$, $\Upsilon_T=L_T=\Pi_T$ and $\widehat Z_w=\widehat Z$: Theorem 5.3 is the special case.

*Proof.* Induction on $t$; $t=0$ is (H1). Let $t\ge1$. Under (5.5) the mutation factors are as in (5.2), so the hypothesis of Lemma 5.1 holds and Lemma 5.1(a),(b) applies; the weights $u_t$ and the factor $L_t$ are $\mathcal F_{t-1}^A$-measurable (they are determined by $\tilde u_t$ and $I_t$), so Lemma 5.1(b) with $\eta=u_t$ gives $\mathbb E[\tfrac1N\sum_ju_t^jf(X_t^j)\mid\mathcal F_{t-1}^A]=\tfrac1N\sum_ju_t^j(\mathcal K_tf)(\widehat X_t^j)$. Next condition on $\mathcal F_{t-1}\vee\sigma(I_t)$, which determines $I_t$, $\tilde u_t$ and $L_t$. On $\{I_t=1\}$: $L_t=L_{t-1}\tfrac1N\sum_k\tilde u_t^k$, $u_t^j=1$, and by the offspring identity of step 3 (the argument of Lemma 5.1(c), with the conditional law of $A_t$ given $\mathcal F_{t-1}\vee\sigma(I_t)$ now $R_t((X_{t-1},\tilde u_t),\cdot)$ by (5.5)), $\mathbb E[\tfrac1N\sum_j(\mathcal K_tf)(\widehat X_t^j)\mid\mathcal F_{t-1},I_t]=\sum_i\frac{\tilde u_t^i}{\sum_k\tilde u_t^k}(\mathcal K_tf)(X_{t-1}^i)$, so
$$
\mathbb E\Big[L_t\frac1N\sum_ju_t^j(\mathcal K_tf)(\widehat X_t^j)\,\Big|\,\mathcal F_{t-1},I_t\Big]=L_{t-1}\cdot\frac1N\sum_i\tilde u_t^i(\mathcal K_tf)(X_{t-1}^i).
$$
On $\{I_t=0\}$: $L_t=L_{t-1}$, $u_t=\tilde u_t$ and $\widehat X_t=X_{t-1}$, so the left side equals the same expression identically. Hence the conditional expectation given $\mathcal F_{t-1}\vee\sigma(I_t)$ does not depend on $I_t$, and taking the expectation over $I_t$ (whatever the kernel $\Delta_t$), with $\tilde u_t^i=u_{t-1}^iG_t(X_{t-1}^i)$,
$$
\mathbb E\Big[L_t\frac1N\sum_ju_t^jf(X_t^j)\,\Big|\,\mathcal F_{t-1}\Big]=L_{t-1}\cdot\frac1N\sum_iu_{t-1}^i\,g(X_{t-1}^i),\qquad g:=G_t\cdot(\mathcal K_tf),
$$
a fixed function by (H0). Taking expectations and using (5.6) for $t-1$ with $g$, then Lemma 5.2 and the invariance of $\mathcal K_t$ exactly as in Theorem 5.3, gives (5.6) for $t$. With $t=T$ and $f\equiv1$, $\mathbb E[\Upsilon_T]=\bar Z_1/\bar Z_0$. $\square$

**Corollary 5.7a (posterior expectations with carried weights; audit 2026-10-15, Sol's audit of P7, finding 1).** Under the hypotheses of Theorem 5.7, for every $f$,
$$
\mathbb E\Big[\widehat Z_w\cdot\frac{\sum_iu_T^if(X_T^i)}{\sum_iu_T^i}\Big]=Z\,\pi(f),
$$
because the left side is $m(\emptyset)\bar Z_0\,\mathbb E[L_T\frac1N\sum_iu_T^if(X_T^i)]$, which equals $m(\emptyset)\bar Z_1\pi(f)$ by (5.6) at $t=T$ and (0.1). The *unweighted* terminal average $\widehat Z_w\cdot\frac1N\sum_if(X_T^i)$ is biased in general when the last stage is not resampled ($I_T=0$). Take $T=1$, $I_1=0$, no moves, $G=G_1=e^{d}$; then $\widehat Z_w=m(\emptyset)\bar Z_0\frac1N\sum_iG(X_0^i)$, and independence of the initial particles gives
$$
\mathbb E\Big[\widehat Z_w\cdot\frac1N\sum_if(X_0^i)\Big]-Z\pi(f)=-m(\emptyset)\bar Z_0\Big(1-\frac1N\Big)\mathrm{Cov}_{q_0}(G,f).
$$
For instance $\gamma_0=(1,1)$, $G=(1,2)$, $N=2$, $m(\emptyset)=1$ and $f=\mathbf 1\{\text{second state}\}$ give $\tfrac74$ against $Z\pi(f)=2$. If $I_T=1$ then $u_T\equiv1$ and the two averages coincide; this includes resampling at every stage, Theorem 5.3. (Checks P7.F1 in `proofs/_audit/group_B/check_audit_B.py`: the example, and 20 random three-state instances with the final stage not resampled. On these the weighted estimate is exact to $2\cdot10^{-14}$ and the unweighted one is off by up to $0.68$.)

So the draft's sentence "if resampling is skipped at some stages, the weights must be carried forward and the corresponding weighted estimator used" is proved, and more: the resampling *decisions* need not be fixed in advance, so "resampling times fixed in advance" in P7 is stronger than necessary for the weighted estimator. What the next proposition shows is that the unweighted product of Section 2.3 cannot be relied on when resampling is skipped.

**Proposition 5.8 (the bias of the unweighted product when resampling is skipped).** Let $T=2$, $0<\phi_1<1$, no resampling at stage $1$ ($I_1=0$), $N\ge2$, and let $\mathcal K_1$ be the (frozen, $q_{\phi_1}$-invariant) composition of the stage-1 moves. Then the unweighted product satisfies
$$
\mathbb E[\Pi_2]-\frac{\bar Z_1}{\bar Z_0}=-\Big(1-\frac1N\Big)\mathrm{Cov}_{q_0}\big(G_1,\ \mathcal K_1G_2\big),
$$
whereas the normalised weighted factor $\Upsilon_2$ of Theorem 5.7 (so that $\widehat Z_w=m(\emptyset)\bar Z_0\Upsilon_2$) has mean $\bar Z_1/\bar Z_0$. The sign depends on $\mathcal K_1$:
(a) if $\mathcal K_1=\mathrm{Id}$ (the identity kernel) and $d$ is non-constant, the bias is strictly negative;
(b) if $\mathcal K_1(x,\cdot)=q_{\phi_1}$ for every $x$ (perfect mixing), the bias is $0$;
(c) it can be strictly positive: on the two-point space with $\gamma_0=(1,1)$, $d=(0,\log4)$, $\phi_1=\tfrac12$, $N=2$ and the $q_{1/2}$-invariant kernel $\mathcal K_1=\begin{pmatrix}0&1\\ \tfrac12&\tfrac12\end{pmatrix}$, $\mathbb E[\Pi_2]=\tfrac{41}{16}>\tfrac{40}{16}=\bar Z_1/\bar Z_0$.

*Proof.* With $X_1^i$ obtained from $X_0^i$ by $\mathcal K_1$ (no resampling), Lemma 5.1(b) gives $\mathbb E[G_2(X_1^k)\mid X_0]=(\mathcal K_1G_2)(X_0^k)$, so
$$
\mathbb E[\Pi_2]=\frac1{N^2}\sum_{i,k}\mathbb E\big[G_1(X_0^i)(\mathcal K_1G_2)(X_0^k)\big]=\frac1N\,q_0\big(G_1\cdot\mathcal K_1G_2\big)+\Big(1-\frac1N\Big)q_0(G_1)\,q_0(\mathcal K_1G_2),
$$
since $X_0^1,\dots,X_0^N$ are i.i.d. $q_0$ (here (H1) is used in full). By Lemma 5.2 and invariance, $q_0(G_1\cdot\mathcal K_1G_2)=(\bar Z_{\phi_1}/\bar Z_0)q_{\phi_1}(\mathcal K_1G_2)=(\bar Z_{\phi_1}/\bar Z_0)q_{\phi_1}(G_2)=\bar Z_1/\bar Z_0$, which gives the displayed identity. (a) With $\mathcal K_1=\mathrm{Id}$: for $X,X'$ i.i.d. $q_0$, $2\,\mathrm{Cov}_{q_0}(G_1,G_2)=\mathbb E[(G_1(X)-G_1(X'))(G_2(X)-G_2(X'))]\ge0$, because $G_1=e^{\phi_1d}$ and $G_2=e^{(1-\phi_1)d}$ are strictly increasing functions of $d$, so the product inside is $\ge0$, and it is $>0$ on the event $\{d(X)\ne d(X')\}$, which has positive probability since $d$ is non-constant and $q_0$ charges every point. (b) $\mathcal K_1G_2$ is constant, so the covariance is $0$. (c) $q_{1/2}=(1,2)/3$ and $q_{1/2}\mathcal K_1=(\tfrac23\cdot\tfrac12,\ \tfrac13+\tfrac23\cdot\tfrac12)=(\tfrac13,\tfrac23)$: invariant. $G_1=G_2=(1,2)$, $\mathcal K_1G_2=(2,\tfrac32)$, $q_0=(\tfrac12,\tfrac12)$: $q_0(G_1\cdot\mathcal K_1G_2)=\tfrac{2+3}2=\tfrac52$, $q_0(G_1)=\tfrac32$, $q_0(\mathcal K_1G_2)=\tfrac74$, so $\mathbb E[\Pi_2]=\tfrac12\cdot\tfrac52+\tfrac12\cdot\tfrac32\cdot\tfrac74=\tfrac54+\tfrac{21}{16}=\tfrac{41}{16}$, while $\bar Z_1/\bar Z_0=\tfrac{1+4}2=\tfrac52$. The mean of $\Upsilon_2$ is Theorem 5.7. $\square$

So the unweighted product is unbiased exactly when the covariance vanishes. The sign and size of the covariance depend on the kernel through expectations under the target, so they are not known in advance (a perfectly mixing kernel, case (b), makes it vanish, but such a kernel is not available in practice); carrying the weights (Theorem 5.7) restores unbiasedness for every kernel. (Other unbiased estimators exist, for instance $m(\emptyset)\bar Z_0\tfrac1N\sum_ie^{d(X_0^i)}$ from the initial particles alone; the point is only that the stagewise product must be the weighted one.)

**Proposition 5.9 (a particle-dependent schedule breaks (i)).** Let $\mathcal S=\{0,1\}$ (the model space for $p=k_{\max}=1$), $\gamma_0=(1,1)$, $d=(0,D)$ with $D>0$, $N=1$ and $T=2$, and let the intermediate temperature be chosen from the particle: $\phi_1=\theta_{X_0}$ with constants $\theta_0,\theta_1\in(0,1)$. Let the stage-1 kernel be the exact sampler $K_1(x,\cdot)=q_{\phi_1}$ (which is $q_{\phi_1}$-invariant for every $\phi_1$). Then
$$
\frac{\mathbb E[\widehat Z]}Z=q_{\theta_0}(0)+q_{\theta_1}(1)=1-\big[\sigma(\theta_0D)-\sigma(\theta_1D)\big],\qquad \sigma(u)=\frac{e^u}{1+e^u},
$$
which is $<1$ if $\theta_0>\theta_1$, $>1$ if $\theta_0<\theta_1$, and $=1$ for a frozen schedule $\theta_0=\theta_1$. For instance $D=2$, $\theta_0=\tfrac34$, $\theta_1=\tfrac14$ give $\mathbb E[\widehat Z]/Z=1-[\sigma(1.5)-\sigma(0.5)]\approx0.805$.

*Proof.* Here $\Pi_2=e^{\theta_{X_0}d(X_0)}\,e^{(1-\theta_{X_0})d(X_1)}$ with $X_1\sim q_{\theta_{X_0}}$ given $X_0$, so by Lemma 5.2 (with $\phi=\theta_x$, $\phi'=1$)
$$
\mathbb E[\Pi_2]=\sum_xq_0(x)e^{\theta_xd(x)}q_{\theta_x}\big(e^{(1-\theta_x)d}\big)=\sum_xq_0(x)e^{\theta_xd(x)}\frac{\bar Z_1}{\bar Z_{\theta_x}}=\frac{\bar Z_1}{\bar Z_0}\sum_x\frac{\gamma_0(x)e^{\theta_xd(x)}}{\bar Z_{\theta_x}}=\frac{\bar Z_1}{\bar Z_0}\sum_xq_{\theta_x}(x).
$$
With two states, $q_\theta(1)=\sigma(\theta D)$ and $q_\theta(0)=1-\sigma(\theta D)$, so $\sum_xq_{\theta_x}(x)=1-\sigma(\theta_0D)+\sigma(\theta_1D)$, and $\sigma$ is strictly increasing. $\square$

**Proposition 5.10 (a particle-dependent choice among invariant kernels breaks (i)).** Same space, $N=1$, $T=2$, frozen $\phi_1=\tfrac12$, so $G_1=G_2=(1,e^{D/2})$ and $\bar Z_1/\bar Z_0=(1+e^D)/2$. Let the stage-1 kernel be chosen from the particle: the exact sampler $q_{1/2}$ if $X_0=0$, the identity if $X_0=1$. Both are $q_{1/2}$-invariant, yet
$$
\mathbb E[\Pi_2]-\frac{\bar Z_1}{\bar Z_0}=\frac12\cdot\frac{e^D-e^{D/2}}{1+e^{D/2}}>0 .
$$
With the opposite rule (identity if $X_0=0$, exact sampler if $X_0=1$) the bias is $-\tfrac12(e^D-e^{D/2})/(1+e^{D/2})<0$.

*Proof.* $q_{1/2}=(1,e^{D/2})/(1+e^{D/2})$ and $q_{1/2}(G_2)=(1+e^D)/(1+e^{D/2})$. Hence $\mathbb E[\Pi_2]=\tfrac12\cdot1\cdot q_{1/2}(G_2)+\tfrac12e^{D/2}\cdot e^{D/2}=\tfrac12\frac{1+e^D}{1+e^{D/2}}+\tfrac12e^D$, and subtracting $\tfrac12(1+e^D)$ gives $\tfrac12\big[\frac{1+e^D}{1+e^{D/2}}-1\big]=\tfrac12\frac{e^D-e^{D/2}}{1+e^{D/2}}$. For the opposite rule, $\mathbb E[\Pi_2]=\tfrac12\cdot1\cdot1+\tfrac12e^{D/2}q_{1/2}(G_2)$, and $\tfrac12+\tfrac12e^{D/2}\frac{1+e^D}{1+e^{D/2}}-\tfrac12(1+e^D)=\tfrac12\frac{e^{D/2}+e^{3D/2}-e^D-e^{3D/2}}{1+e^{D/2}}=-\tfrac12\frac{e^D-e^{D/2}}{1+e^{D/2}}$. $\square$

The mechanism is Remark 4.8: the kernel actually applied, $\tilde K(x,\cdot)=K^{c(x)}(x,\cdot)$, is a state-dependent mixture of invariant kernels and is not invariant ($q_{1/2}\tilde K\ne q_{1/2}$). With $N$ particles, choosing the kernel (or its scan probabilities) from the current population is the same phenomenon on $\mathcal S^N$. Propositions 5.9 and 5.10 show that the guarantee (i) fails for *some* particle-dependent rules, so (H0) cannot be dropped from P7 in general; they do not say that every adaptive rule is biased (with $N=1$ and identity moves, any particle-dependent $\phi_1$ gives $\Pi_2=e^{d(X_0)}$, which is unbiased), and they are not the empirical-ESS rule (Remark 5.12).

**Remark 5.11 (particle-specific kernels).** The proof of Theorem 5.3 uses that the same kernel is applied to every particle. If particle $j$ used its own invariant kernel $K^{(j)}_{t,\ell}$, Lemma 5.1(c) would be needed in the form $\mathbb E[\tfrac1N\sum_jg_j(\widehat X_t^j)\mid\mathcal F_{t-1}]=\sum_iW_t^i\tfrac1N\sum_jg_j(X_{t-1}^i)$ for arbitrary $g_1,\dots,g_N$. A sufficient condition is $\mathbb P(A_t^j=i\mid\mathcal F_{t-1})=W_t^i$ for every $j$ (every ancestor label has the law $W_t$: multinomial resampling, or any scheme followed by a uniform random permutation of the offspring); it is not necessary (on a population with all particles equal, any assignment works). Stratified and systematic resampling do not have this property in general, and with particle-specific kernels they can bias $\widehat Z$; this is not proved here (exact examples with $N=3$ were produced during the review and are recorded under review/). The draft does not use particle-specific kernels; the remark only records why "the same kernel for all particles" is part of (H3).

**Remark 5.12 (adaptive schedules).** The empirical-ESS schedule of the implemented algorithm chooses $\phi_t$ from the particles. Nothing in this section applies to it, and nothing is claimed about it here: Proposition 5.9 uses a different particle-dependent rule (with $N=1$ the empirical relative ESS is identically $1$, so an ESS rule would jump straight to $\phi=1$). The draft states (i) for frozen schedules only, which is correct.

**Proposition 5.13 (unbiased counts given the weights only are not enough).** Let $\mathcal S=\{s_1,s_2,s_3,s_4\}$, $\gamma_0\equiv1$, $d=(0,0,0,\log4)$, $N=2$, $T=2$, $\phi_1=\tfrac12$. Then $G_1=G_2=G=(1,1,1,2)$, $q_{1/2}=(1,1,1,2)/5$ and $\bar Z_1/\bar Z_0=\tfrac74$. Let the frozen stage-1 kernel be $K(s_1,s_4)=1$, $K(s_2,s_2)=K(s_3,s_3)=1$, $K(s_4,s_1)=K(s_4,s_4)=\tfrac12$ (one move, $m_1=1$), let stage 2 have multinomial resampling and no moves ($m_2=0$; neither enters $\Pi_2$), and let stage-1 resampling be multinomial except on the populations $(s_1,s_2)$ and $(s_2,s_1)$, where both offspring are given to the particle in state $s_1$. Then:
(a) $K$ is $q_{1/2}$-reversible;
(b) the rule satisfies the draft's condition $\mathbb E[\#\text{offspring of }i\mid\text{weights}]=NW^i$ for $i=1,2$ (the conditional expectation given the weight vector $(w^1,w^2)$ of the population), but violates (5.1) at $x=(s_1,s_2)$, where the counts are $(2,0)$ instead of $(1,1)$;
(c) $\mathbb E[\Pi_2]=\tfrac{29}{16}\ne\tfrac74$, so $\mathbb E[\widehat Z]\ne Z$.

*Proof.* (a) $q_{1/2}(s_1)K(s_1,s_4)=\tfrac15=\tfrac25\cdot\tfrac12=q_{1/2}(s_4)K(s_4,s_1)$; all other off-diagonal entries vanish on both sides. (b) The weight vector is $(1,1)$ exactly when both particles lie in $\{s_1,s_2,s_3\}$; given this, the nine ordered populations are equally likely (each has probability $\tfrac1{16}$ under $q_0^{\otimes2}$). For the first index the expected count is $2$ on $(s_1,s_2)$, $0$ on $(s_2,s_1)$ and $1$ on the other seven, so the average is $\tfrac{2+0+7}9=1=NW^1$; the same holds for the second index by symmetry. For every other weight vector the rule is multinomial, so the draft's condition holds. At $x=(s_1,s_2)$ the counts are $(2,0)$, so (5.1) fails. (c) Let $x$ be the initial population. The first factor of $\Pi_2$ is $\tfrac12\sum_iG(x^i)$, and given $x$ and the ancestors, the conditional mean of the second factor is $\tfrac12\sum_j(KG)(x^{A^j})$, where $KG=(2,1,1,\tfrac32)$. Under multinomial resampling the conditional mean of the second factor given $x$ is $\sum_iW^i(x)(KG)(x^i)$, and Theorem 5.3 gives $\mathbb E[\Pi_2]=\tfrac74$ for the multinomial rule. The modified rule differs only on $x\in\{(s_1,s_2),(s_2,s_1)\}$, each of probability $\tfrac1{16}$, where the first factor is $1$ and the conditional mean of the second factor is $(KG)(s_1)=2$ instead of $\tfrac{2+1}2=\tfrac32$. Hence $\mathbb E[\Pi_2]=\tfrac74+2\cdot\tfrac1{16}\cdot\big(2-\tfrac32\big)=\tfrac74+\tfrac1{16}=\tfrac{29}{16}$. $\square$

The same construction with the stage-1 kernel replaced by the identity shows nothing (then $KG=G$ is constant on $\{s_1,s_2,s_3\}$); the bias arises because, among particles of equal weight, the rule favours the state from which the move is more likely to gain weight. Ties in the weights are not exotic in the paper's bridge: $d$ takes equal values on many models (for instance $d(\emptyset)=0$ and $d=0$ on every model contained in one block). The conclusion is that step 2(c) of the algorithm must be read as (5.1), "given the current population". For a rule that depends on the population only through its weight vector and the index order, $R_t(x,\cdot)=\tilde R_t(W_t(x),\cdot)$, the two readings coincide: the expected counts given $x$ are a function of $W_t(x)$, so the draft's condition "for every weight vector" is (5.1) for every population. The four schemes of Lemma 5.4, taken with a fixed index order, are of this type and satisfy it; their value-sorted variants are not of this type, but satisfy (5.1) directly by Lemma 5.4. A rule that looks at the particle values must satisfy (5.1) population by population, and Proposition 5.13 shows that satisfying the draft's condition on average over the populations with a given weight vector is not enough.

**Proposition 5.14 (unbiased counts given the current population only are not enough; audit 2026-10-15, Sol's audit of P7, finding 2).** Let $\mathcal S=\{0,1\}$, $\gamma_0=(1,1)$, $d=(0,\log8)$, $N=2$, $T=3$, $\phi_t=t/3$. Then $G_t=G=(1,2)$ at every stage and $\bar Z_1/\bar Z_0=\tfrac92$. Stage 1: multinomial resampling, then one move by the exact sampler $K(x,\cdot)=q_{1/3}=(\tfrac13,\tfrac23)$, which is $q_{1/3}$-invariant. Stages 2 and 3: no moves. Stage 3: multinomial resampling. Stage 2: put $H=2\cdot\mathbf 1\{X_0^1=1\}-1\in\{\pm1\}$. If $X_1$ is mixed (one particle in each state), give both offspring to the particle in state $1$ with probability $\tfrac23+\tfrac H3$, and both to the particle in state $0$ otherwise. If $X_1$ is homogeneous, resample multinomially. Then:
(a) $\mathbb E[\#\{j:A_2^j=i\}\mid X_1]=NW_2^i(X_1)$ for $i=1,2$: the counts are unbiased given the current population;
(b) the conditional law of $A_2$ given $\mathcal F_1$ depends on $X_0$ through $H$, so (5.2) and the identity of Lemma 5.1(c) given $\mathcal F_1$ fail;
(c) $\mathbb E[\Pi_3]=\tfrac92+\tfrac1{18}$, so $\mathbb E[\widehat Z]\ne Z$.

*Proof.* The exact sampler ignores its input, so $X_1$ is i.i.d. $q_{1/3}$ and independent of $(X_0,A_1)$, hence of $H$; and $\mathbb E[H]=0$. (a) On a mixed $X_1$, $W_2=\tfrac13$ for the particle in state $0$ and $\tfrac23$ for the particle in state $1$. Given $X_1$, the expected count of the particle in state $1$ is $2(\tfrac23+\tfrac13\mathbb E[H\mid X_1])=\tfrac43=NW_2$, and that of the particle in state $0$ is $\tfrac23$. On homogeneous $X_1$ the rule is multinomial. (b) is clear. (c) $\Pi_3=\Pi_1F_2F_3$ with $F_2=\frac12\sum_iG(X_1^i)$ and $F_3=\frac12\sum_jG(X_1^{A_2^j})$. Replace the stage-2 rule by multinomial resampling; this gives $\Pi_3^{\rm std}$, with $\mathbb E[\Pi_3^{\rm std}]=\tfrac92$ by Theorem 5.3. The two rules differ only on mixed $X_1$. There the conditional mean of $F_3$ given $\mathcal F_1$ is $2(\tfrac23+\tfrac H3)+1\cdot(\tfrac13-\tfrac H3)=\tfrac53+\tfrac H3$, against $\sum_iW_2^iG(X_1^i)=\tfrac53$ for multinomial, and $F_2=\tfrac32$. Hence, by the independence of $X_1$ from $(X_0,A_1)$,
$$
\mathbb E[\Pi_3]-\tfrac92=\mathbb E\big[\Pi_1H\big]\cdot\mathbb P(X_1\text{ mixed})\cdot\tfrac32\cdot\tfrac13=\tfrac14\cdot\tfrac49\cdot\tfrac12=\tfrac1{18},
$$
where $\mathbb E[\Pi_1H]=\tfrac12\mathbb E[G(X_0^1)H]+\tfrac12\mathbb E[G(X_0^2)]\mathbb E[H]=\tfrac12(\tfrac12\cdot2-\tfrac12\cdot1)=\tfrac14$ and $\mathbb P(X_1\text{ mixed})=2\cdot\tfrac13\cdot\tfrac23=\tfrac49$. $\square$

Exact enumeration in `proofs/_audit/group_B/check_audit_B.py` (checks P7.F2) gives $\mathbb E[\Pi_3]=\tfrac{41}9=\tfrac92+\tfrac1{18}$ and confirms (a). The mechanism is the one of Proposition 5.13, moved from the populations with a given weight vector to the histories with a given current population. The offspring identity must hold conditionally on everything the rule can see. The draft's "given the current population" is enough when the scheme is applied afresh to the current population, as all four named schemes are.

---

## 6. Hypotheses added, readings, conditions made explicit, and flags for the draft

**Readings and hypotheses (all satisfied by the algorithm of Section 2.3 of the draft, read as stated here).**

1. *Common setting (Section 0.1).* $\gamma_0>0$ on the capped model space $\mathcal S$, all sums over $\mathcal S$, $\chi^2$ defined with both measures supported on $\mathcal S$. The identity $Z=m(\emptyset)\bar Z_1$ is verified from the definitions in (0.1). The theorems are proved in the abstract setting (any $(\gamma_0,d)$ on a finite set), which contains the paper's bridge; the counterexamples are stated there too, and realisability by a design is not claimed here (configurations of the paper's form with the same biases were produced during the review and are recorded under review/; they are not part of the proofs).
2. *F4.* "Full-rank" means full column rank; the divergence is $\mathrm{KL}(P_\star\|Q)$; the minimiser is unique (Theorem 1.1). The population identity with $\Gamma$ is Corollary 1.2. No asymptotic claim is made.
3. *L4.* Nothing added: $c>0$ follows from $\rho\in(0,1)$. The explicit termination bound $T\le\max\{1,\lceil D/(2\sqrt{\log(1+c)})\rceil\}$ (Theorem 2.4(b)) shows the greedy schedule reaches $1$ in finitely many stages, which the statement presupposes. Minimality holds against arbitrary finite sequences satisfying the constraint, not only monotone schedules.
4. *L6.* Reading: $b_\pi=p$ in (iii)–(v), as in (ii); $\pi_p$ is the size law. *Flag:* the draft's preamble "for the untruncated $\mathrm{BB}(1,b_\pi)$ prior" attaches $b_\pi=p$ only to (ii), but (iii)–(v) are false for general $b_\pi$ (Remark 3.4: $p=1$, $b_\pi=\tfrac14$); since the paper's prior is $\mathrm{BB}(1,p)$ this is a wording point. Remark 3.3 separates the size-class ratio (which tends to $\tfrac12$) from the per-model ratio (which is $O(1/p)$ for fixed $k$).
5. *P6.* (a) Reversibility of Metropolis–Hastings needs no condition on the proposal; the symmetry condition is a design property (Proposition 4.3). (b) *Flag:* the draft's example "swap with a neighbour list built from $X$" satisfies the symmetry condition if the neighbour relation is symmetric and, for $k_{\max}\ge1$, only then; a nearest-neighbour list is not symmetric in general; symmetrise the list, or accept that moves whose reverse is impossible are always rejected. The neighbour-swap acceptance must contain the Hastings ratio, which is $|N(j)\setminus S|/|N(l)\setminus S'|$ when the reverse move is available ($j\in N(l)$) and $0$ otherwise, in which case the move is always rejected (Remark 4.4; audit 2026-10-15, Sol's audit of P6, finding 2: the cardinality formula alone is wrong when $j\notin N(l)$, e.g. $N(1)=\{2\}$, $N(2)=\{3\}$, $N(3)=\{1\}$, $S=\{1\}$, $S'=\{2\}$ give $\Pi(S,S')=1$, $\Pi(S',S)=0$, while the formula gives $1$). (c) Gibbs updates are the conditionals restricted to the cap (Proposition 4.5). (d) Selection probabilities and sweep order are constants given $(y,\text{pilot})$ (Remark 4.8). (e) The stage-$t$ kernels target $q_{\phi_t}$ (Remark 4.9). (f) (Corrected, audit 2026-10-15.) For a target on exactly two coordinates with no binding cap ($p=k_{\max}=2$), the Gibbs sweep is reversible if and only if the target is a product (Example 4.7). In general, a sweep $G_iG_j$ over two coordinates is reversible iff coordinates $i,j$ are conditionally independent given the others when $k_{\max}\ge p$, and is never reversible when $1\le k_{\max}\le p-1$ (Proposition 4.7a). The pre-audit wording "a Gibbs sweep on two coordinates is reversible iff the target is a product" is false for two updates inside a larger model without a binding cap (Sol's counterexample $\gamma(S)=2^{\mathbf 1\{1\in S\}\mathbf 1\{3\in S\}}$, $p=3$). (Under a binding cap $1\le k_{\max}\le p-1$ it holds vacuously, since the sweep is never reversible and $q$, supported on a non-product set, is never a product.)
6. *P7.* Sufficient conditions: (H0) frozen settings with $q_{\phi_t}$-invariant kernels; (H1) i.i.d. initial draws from $\pi_0$ and exact $\bar Z_0$; (H2) unbiased offspring counts (5.1) *given the population*, with multinomial, residual, stratified and systematic resampling verified in Lemma 5.4 (for any population-dependent ordering); (H3) the same kernel applied to every particle, each particle's conditional law being the kernel; (H4) islands use randomness independent of the pilot and of each other, and the pilot's settings satisfy (H0) and (H2) for every pilot outcome, so that all statements hold conditionally on the pilot. *Flags:* (a) *the draft's step 2(c), "$\mathbb E[\#\text{offspring of }i\mid\text{weights}]=Nw_t^i/\sum_jw_t^j$", is insufficient as written when the resampling rule may look at particle values* (Proposition 5.13: an exact counterexample with every other hypothesis of P7 satisfied, $\mathbb E[\widehat Z]/Z=\tfrac{29}{28}$); it should read "given the current population", i.e. (5.1). P7 is proved under that reading; the four schemes it names satisfy (5.1), and so does every rule that sees the population only through its weights and satisfies the draft's condition for every weight vector. (a') (audit 2026-10-15) Conditioning on the current population is itself not enough if the rule's randomness may depend on the earlier history: the identity must hold given the whole past, as in (5.2) (fresh randomness) (Proposition 5.14: $\mathbb E[\widehat Z]/Z=1+\tfrac1{81}$ with counts unbiased given the current population). (b) Reusing the pilot's random stream violates (H4) (Section 5.5). (c) The draft's sentence on skipped resampling is proved (Theorem 5.7, Proposition 5.8); moreover the resampling *decisions* may be adaptive (ESS-triggered) without affecting (i) for the weighted estimator $\widehat Z_w$, so "resampling times fixed in advance" is stronger than needed; the unweighted product can be biased when resampling is skipped, in either direction depending on the kernel, and is unbiased for a perfectly mixing kernel (Proposition 5.8); with skipped resampling at the last stage, the estimate of $Z\pi(f)$ must use the terminal weights (Corollary 5.7a, audit 2026-10-15). (d) The schedule and the kernels cannot be chosen from the run's particles in general (Propositions 5.9 and 5.10); nothing is claimed about the empirical-ESS rule (Remark 5.12). (e) In (ii), "under finite variance" is automatic on a finite space; the Markov bound is exact for every $R\ge1$ and needs only unbiasedness; the CLT interval is asymptotic in $R$ and conditional on the pilot (Theorem 5.5, Corollary 5.6a). (f) In (iii), $\widehat Z>0$ surely, and the inequality is strict unless $\widehat Z$ is almost surely constant (Theorem 5.6). (g) The unnormalised particle estimate of every posterior expectation is also unbiased ((5.4) at $t=T$) when every stage resamples; with carried weights it is $\widehat Z_w\sum_iu_T^if(X_T^i)/\sum_iu_T^i$ (Corollary 5.7a; audit 2026-10-15). (h) Not used by the proofs, and therefore stronger than needed in the draft's hypotheses: independence of the initial particles (only their common law $q_0$ enters (5.4); Proposition 5.8 does use independence), independence of the moves across particles (only each particle's conditional law enters), and strict monotonicity of the schedule.

**What was found false or imprecise in the draft.** (1) L6's preamble must attach $b_\pi=p$ to (iii)–(v) (item 4). (2) P6's example "swap with a neighbour list built from $X$" needs a symmetric list when $k_{\max}\ge1$ (item 5(b)). (3) The resampling condition of Section 2.3 must condition on the population, not only on the weights (item 6(a)). Every other part of F4, L4, L6, P6 and P7 holds as stated under the readings of Section 0.2; the draft's hypotheses found stronger than necessary are listed in items 5(a) and 6(c),(h).

(audit 2026-10-15) Found in the Sol audit of the current draft (15 October), in addition: (4) P6's final sentence, "a two-coordinate Gibbs sweep is reversible if and only if the target is a product": Example 4.7 proves this for exactly two coordinates without a binding cap; for two updates inside a larger uncapped model it is false, and the general criterion is Proposition 4.7a (item 5(f)). (5) The neighbour-swap Hastings ratio is $0$ when the reverse move is unavailable (item 5(b)). (6) P7(i)'s "more generally" clause needs the terminal weights when resampling is skipped at the last stage (Corollary 5.7a). (7) "Unbiased given the current population" must be read with the scheme applied afresh, i.e. given the whole past (Proposition 5.14). (8) Bias under skipped resampling or particle-dependent choices is possible, not inevitable (Proposition 5.8(b); the remark after Proposition 5.10).

---

## Audit revisions (2026-10-15)

Adjudicator B (Opus 5.5), after the GPT-6.1 Sol audits of F4, L4, L6, P6 and P7 (`proofs/_audit/<ID>/SOL_AUDIT.md`). The pre-audit text is saved as `PROOF_pre_audit.md`. F4, L4 and L6 are unchanged. Rulings are in `proofs/_audit/group_B/RULINGS.md`.

1. **Summary (P6 bullet):** the two-variable sweep criterion is scoped to $p=k_{\max}=2$; the general criterion (Proposition 4.7a) is quoted. (P6 finding 1.)
2. **New Proposition 4.7a** (after Example 4.7): two-coordinate sweeps in a model with $p$ coordinates are reversible iff conditional independence given the rest (no binding cap), and never under a binding cap $1\le k_{\max}\le p-1$; Sol's three-coordinate example included. (P6 finding 1.)
3. **Section 6, item 5(b):** the neighbour-swap ratio is $0$ when $j\notin N(l)$. (P6 finding 2.)
4. **Section 6, item 5(f):** corrected statement. (P6 finding 1.)
5. **Summary (P7 bullet):** Corollary 5.7a and Proposition 5.14 are quoted. (P7 findings 1, 2.)
6. **Section 5.1, (H2):** the conditioning is made explicit. $A_t\sim R_t(X_{t-1},\cdot)$ holds given the whole past (fresh randomness); conditioning on the current population alone is insufficient. History-dependent kernels satisfying (5.1) for every history are also covered. (P7 finding 2.)
7. **New Corollary 5.7a** (after Theorem 5.7): with carried weights the unbiased estimate of $Z\pi(f)$ is $\widehat Z_w\sum_iu_T^if(X_T^i)/\sum_iu_T^i$; the unweighted terminal average is biased in general, with the covariance formula and Sol's $7/4$ versus $2$ example. (P7 finding 1.)
8. **New Proposition 5.14** (after Proposition 5.13): Sol's exact counterexample, in which counts are unbiased given the current population but $\mathbb E[\Pi_3]=\tfrac92+\tfrac1{18}$. (P7 finding 2.)
9. **Section 6, item 6:** new flag (a'); flags (c) and (g) updated. (P7 findings 1–3.)
10. **"What was found false":** items (4)–(8) appended.

Checks: `check_foundations.py` rerun unchanged, 111/111 PASS (`proofs/_audit/group_B/rerun_check_foundations.out`). New checks P6.F1, P6.F2, P7.F1 and P7.F2 in `proofs/_audit/group_B/check_audit_B.py` all PASS (`check_audit_B.out`).

11. **After Sol's confirmations (P6 exchange 1, P7 exchange 1).** Both gave the verdict VERIFIED. The residual P6 edits were applied: the Summary's neighbour ratio is conditional on $j\in N(l)$; Proposition 4.7a ranges over nonempty fibres; item 5(f) no longer calls the old equivalence false "under a binding cap", where it holds vacuously; "What was found false" item (4) is reworded. P7 asked only for draft wording ($\widehat Z$ means $\widehat Z_w$ throughout (ii)–(iii) when weights are carried), which goes into PAPER_CHANGES. These edits were not re-sent for confirmation.
