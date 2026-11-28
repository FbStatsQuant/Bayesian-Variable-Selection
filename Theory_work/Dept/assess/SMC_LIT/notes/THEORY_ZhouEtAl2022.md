# THEORY note: Zhou, Yang, Vats, Roberts and Rosenthal (2022), dimension-free mixing for high-dimensional Bayesian variable selection (MCMC comparator for P1)

Reader: Claude (Sonnet 5.5), 2026-11-24. Private to this machine. Page numbers are PDF pages of the local file. "(my inference)" marks anything the paper does not state itself; "(from memory, not checked)" marks facts from outside the paper.

## 0. Bibliographic and file caveat
- Title: Dimension-free mixing for high-dimensional Bayesian variable selection. Authors: Quan Zhou (Texas A&M), Jun Yang (Oxford), Dootika Vats (IIT Kanpur), Gareth O. Roberts (Warwick), Jeffrey S. Rosenthal (Toronto). Local file: arXiv:2105.05719v3 [stat.ME], dated 23 Apr 2022, 58 pages (main text pp. 1-31 with references pp. 31-33; supplement pp. 34-58). Published in J. R. Stat. Soc. B (2022); volume and pages from memory, not checked. Constants and numbering may differ in the published version.
- Local file: `/home/fb31/SMC_Theory_Department/SMC_LIT/papers/ZhouEtAl2022_dimension_free_mixing.pdf`.
- Read as comparator for P1 only. I read all 58 pages; the lower-bound-type content is only Example 1 (pp. 3-4, proof p. 50) and the empirical failure of locally balanced proposals (Table 1, Section 7.2-7.3). The paper contains no lower bound for the Zanella-Roberts tempered Gibbs sampler.
- Symbol note: in Theorem S2 (p. 39) the constants in assumptions A, C, D, E, F are printed in a fraktur font ($\mathfrak C_0,\mathfrak C_1$ and a third constant in (A) that I could not read unambiguously from the rendering); I write them as $\mathfrak C_0,\mathfrak C_1$ and describe (A) in words.
- Notation clash in the paper (not an error): in Example 1, $\nu$ is simultaneously the design correlation ($X_1^\top X_2=(\nu-1)n$) and the proposal exponent in $K_\nu$.

## 1. Coverage log
| PDF pages | Content |
|---|---|
| 1-2 | Abstract, 1 Introduction, 1.1 background and contributions (informed proposals, Zanella 2020, tempered Gibbs of Zanella and Roberts 2019) |
| 3-4 | 1.2 motivation: informed proposals $K_\nu\propto\pi^\nu$, Example 1 (slow mixing of the informed MH chain) |
| 4-6 | 1.3 two-stage drift condition; 1.4 organisation |
| 6-9 | 2.1 model and prior (3)-(6); 2.2 RW-MH and Yang et al. review; Condition 1; Definition 1 (unimodality) |
| 9-11 | 2.3 LIT-MH algorithm (9)-(11); 3 dimension-free mixing: weights (13), chain (14), drift (15) |
| 12-14 | 3.1 two drift functions (16), Lemma 1, Props 1-2; 3.2 Theorem 1, Remark 2 |
| 15-19 | 4 general two-stage drift condition: Assumption A, Theorem 2, Corollaries 1-2, Remarks 3-6, 4.3 comparison with drift-and-minorization, 4.4 applications |
| 20-27 | 5 simulations (Tables 1-2, Fig. 1); 6 GWAS analysis (Tables 3-5) |
| 27-31 | 7 Discussion: 7.1 swap moves; 7.2 LIT-MH on general discrete spaces, Lemma 2; 7.3 LB-MH-1; 7.4 closing remarks, mention of Zanella-Roberts tempered Gibbs |
| 31-33 | Acknowledgements, references |
| 34-39 | Supplement S1 (drift lemmas, Theorem S1 from Jerison 2016), S2 proof of Theorem 2, S3 Theorem S2 (Yang et al. conditions imply Condition 1) |
| 40-49 | S3 proof sketch; S4 more simulation results (S4.1-S4.4), Figs 3-5, Tables 6-8 |
| 50-57 | S5 proofs: Example 1, Lemma 1, Lemmas S2-S6, Props 1-2, Theorem 1, Lemma 2; S6 data and code availability |
| 57-58 | References for the supplement |
All 58 pages read.

## 2. Setting
- Same model as Yang et al.: $y=X_\gamma\beta_\gamma+e$, $e\sim N(0,\phi^{-1}I_n)$, $g$-prior $\beta_\gamma\mid\gamma\sim N(0,g\phi^{-1}(X_\gamma^\top X_\gamma)^{-1})$, $\pi_0(\phi)\propto\phi^{-1}$, $\pi_0(\gamma)\propto p^{-\kappa_0|\gamma|}\mathbb 1_{\mathcal M(s_0)}(\gamma)$, $1+g=p^{2\kappa_1}$, $\kappa=\kappa_0+\kappa_1$. Marginal posterior over $\mathcal M(s_0)=\{\gamma:|\gamma|\le s_0\}$:
$$\pi_n(\gamma)\propto p^{-\kappa|\gamma|}\big(g^{-1}y^\top y+y^\top P_\gamma^\perp y\big)^{-n/2}\mathbb 1_{\mathcal M(s_0)}(\gamma)\quad(4),$$
and posterior ratio $B(\gamma,\gamma')=\pi_n(\gamma')/\pi_n(\gamma)=p^{\kappa(|\gamma|-|\gamma'|)}\{1+\frac{y^\top(P_\gamma-P_{\gamma'})y}{g^{-1}y^\top y+y^\top P_{\gamma'}^\perp y}\}^{-n/2}$ (5).
- Neighbourhoods (6): addition $\mathcal N_a$, deletion $\mathcal N_d$, swap $\mathcal N_s$. $\gamma^*=\{j:|\beta_j^*|\ge\beta_{\min}\}$ (8), $s^*=|\gamma^*|\le s_0$, regime $s_0\log p=O(n)$, $p\gg n$ allowed.
- Samplers: RW-MH (7) with constant move-type probabilities and uniform within type (Yang et al.'s chain); LIT-MH ("Metropolis-Hastings with Locally Informed and Thresholded proposal distributions"), the new chain; LB-MH-1 / LB-MH-2, locally balanced proposals with $f(b)=\sqrt b$ (Zanella 2020).
- LIT-MH proposal (9)-(10): $K_{\rm lit}(\gamma,\gamma')=\sum_{\star\in\{a,d,s\}}\frac{h_\star(\gamma)w_\star(\gamma'|\gamma)}{Z_\star(\gamma)}\mathbb 1_{\mathcal N_\star(\gamma)}(\gamma')$, $Z_\star(\gamma)=\sum_{\tilde\gamma\in\mathcal N_\star(\gamma)}w_\star(\tilde\gamma|\gamma)$, $w_\star(\gamma'|\gamma)=p^{\ell_\star}\vee B(\gamma,\gamma')\wedge p^{L_\star}$. For the analysis (12)-(13): for $|\gamma|<s_0$ propose add or delete with probability $1/2$ each, at $|\gamma|=s_0$ propose swap or delete; $w_a=B\wedge p^{c_1}$, $w_d=1\vee B\wedge p^{c_0}$, $w_s=ps_0\vee B\wedge p^{c_1}$. Acceptance (14): $P_{\rm lit}(\gamma,\gamma')=K_{\rm lit}(\gamma,\gamma')\min\{1,\frac{\pi_n(\gamma')K_{\rm lit}(\gamma',\gamma)}{\pi_n(\gamma)K_{\rm lit}(\gamma,\gamma')}\}$.

## 3. Main theorems (faithful statements)

### Condition 1 (p. 8; the key hypothesis, a property of the posterior)
There are $\gamma^*\in\mathcal M(s_0)$ and constants $c_0,c_1>0$ (not depending on $\gamma$) such that, with "overfitted" meaning $\gamma^*\subseteq\gamma$ and "underfitted" meaning $\gamma^*\not\subseteq\gamma$:
- (1a) for any overfitted $\gamma\in\mathcal M(s_0)$ and $j\notin\gamma$: $B(\gamma,\gamma\cup\{j\})\le p^{-c_0}$;
- (1b) for any underfitted $\gamma\in\mathcal M(s_0)$ there is some $j\in\gamma^*\setminus\gamma$ with $B(\gamma,\gamma\cup\{j\})\ge p^{c_1}$;
- (1c) for any underfitted $\gamma$ with $|\gamma|=s_0$ there are $j\in\gamma^*\setminus\gamma$, $k\in\gamma\setminus\gamma^*$ with $B(\gamma,(\gamma\cup\{j\})\setminus\{k\})\ge p^{c_1}$.
Paper's reading (p. 9): Condition 1 "essentially assumes that $\pi_n$ is unimodal on $\mathcal M(s_0)$ with respect to the add-delete-swap neighbourhood" (Definition 1: $\gamma$ is a local mode w.r.t. $\mathcal N$ if $\pi_n(\gamma)\ge\max_{\gamma'\in\mathcal N(\gamma)}\pi_n(\gamma')$; unimodal if there is only one local mode). It also implies tails decay fast: $\pi_n(\mathcal S_k)\le p^{1-c_0}\pi_n(\mathcal S_{k-1})$ when $c_1>2c_0>2$.

### Theorem S2 (Yang et al. 2016, Lemma 4, restated in the supplement, p. 39)
Take $\sigma_z^2=1$ and finite constants $\mathfrak C_0\ge0$, $\mathfrak C_1>0$, $\zeta\in(0,1]$ with $\mathfrak C_1\zeta\ge4$. Assume: (A) $\|X\beta^*\|_2^2$ is at most a constant times $\log p$ and $\|X_{u^*}\beta^*_{u^*}\|_2^2\le\mathfrak C_0\log p$ where $u^*=[p]\setminus\gamma^*$; (B) $X_j^\top X_j=n$ and $\min_{\gamma\in\mathcal M(s_0)}\Lambda_{\min}(X_\gamma^\top X_\gamma)\ge n\zeta$; (C) $\mathbb E[\max_{\gamma\in\mathcal M(s_0)}\max_{k\notin\gamma}|X_k^\top P_\gamma^\perp z|]\le\frac12\sqrt{\mathfrak C_1\zeta n\log p}$ for $z\sim N(0,I_n)$; (D) $\kappa_0\ge2$, $\kappa_1\ge1/2$, $\kappa\ge4(\mathfrak C_0+\mathfrak C_1)+2$; (E) $\max\{1,(2\zeta^{-2}\Psi(X)+1)s^*\}\le s_0\le\frac n{32\log p}-\frac{\mathfrak C_0}4$, $\Psi(X)=\max_{\gamma\in\mathcal M(s_0)}\|(X_\gamma^\top X_\gamma)^{-1}X_\gamma^\top X_{\gamma^*\setminus\gamma}\|_{\rm op}^2$; (F) $\beta_{\min}^2\ge\frac{128(\kappa+\mathfrak C_0+\mathfrak C_1)\log p}{\zeta^2n}$. Then with probability $1-O(p^{-a})$ (universal $a>0$), Condition 1 holds with $c_0=2$, $c_1=4$ (design treated as fixed; randomness is the noise).
(Paper notes Yang et al. state $c_1=3$ but the argument gives 4.)

### Proposition 1 (overfitted models, p. 13) and Proposition 2 (underfitted, p. 14)
With $V_1(\gamma)=\big(1+\frac{y^\top P_\gamma^\perp y}{g^{-1}y^\top y}\big)^{1/\log(1+g)}$ and $V_2(\gamma)=e^{|\gamma\setminus\gamma^*|/s_0}$ (16), both in $[1,e]$ (Lemma 1):
- Prop 1: if Condition 1 holds with $c_0\ge2$, $c_1\ge1$, then for overfitted $\gamma\ne\gamma^*$, $|\gamma|\le s_0$: $\frac{(P_{\rm lit}V_2)(\gamma)}{V_2(\gamma)}=1-\frac1{4s_0}+O\big(\frac1{ps_0}\big)$.
- Prop 2: if $n=O(p)$, $s_0\log p=O(n)$, $\kappa=O(s_0)$ and Condition 1 holds with $(c_0+1)\vee4\le c_1\le n\kappa_1-\kappa$, then for every underfitted $\gamma\in\mathcal M(s_0)$: $\frac{(P_{\rm lit}V_1)(\gamma)}{V_1(\gamma)}\le1-\frac{c_1}{8n\kappa_1}+o\big(\frac1{n\kappa_1}\big)$.

### Theorem 1 (dimension-free mixing of LIT-MH, p. 14)
Let $T_{\rm mix}=\sup_{\gamma\in\mathcal M(s_0)}\min\{t\ge0:\|P^t_{\rm lit}(\gamma,\cdot)-\pi_n\|_{\rm TV}\le1/4\}$. Suppose $n=O(p)$, $s_0\log p=O(n)$, $\kappa=O(s_0)$, and Condition 1 holds with $c_0=2$ and $4\le c_1\le n\kappa_1-\kappa$. Then for sufficiently large $n$
$$T_{\rm mix}\le800\max\Big\{\frac{n\kappa_1}{c_1},\,3s_0\Big\}.$$
No dependence on $p$ in the iteration count. Remark 2 compares with the RW-MH bound of Yang et al.: $O(ps_0^2(n\kappa_1+s_0\kappa_1+s_0\kappa_0)\log p)$. Remark 1: on the overfitted set the order $s_0$ is sharp ($\gamma^*=\emptyset$, $|\gamma|=s_0$ needs about $2s_0$ steps). Computation per step (p. 10): $O(p|\gamma|^2)$ for LIT-MH versus $O(|\gamma|^2)$ for RW-MH given precomputed $X^\top X$, $X^\top y$; the "dimension-free" statement is about iterations, not cost (my inference: total cost still scales linearly in $p$ for LIT-MH).

### Theorem 2 (general two-stage drift condition, p. 16)
Assumption A: a reversible Markov chain with kernel $P$ on a countably generated space, stationary $\pi$, non-negative spectrum (the lazy version always qualifies, Remark 3). Suppose there are drift functions $V_1,V_2:\mathcal X\to[1,\infty)$, constants $\lambda_1,\lambda_2\in(0,1)$, a set $\mathsf A\in\mathcal E$ and $x^*\in\mathsf A$ such that
(i) $PV_1\le\lambda_1V_1$ on $\mathsf A^c$; (ii) $PV_2\le\lambda_2V_2$ on $\mathsf A\setminus\{x^*\}$; and for some $M\ge2$, $K\ge1$:
(iii) for $x\in\mathsf A$: $V_1(x)=1$ and, if $P(x,\mathsf A^c)>0$, $\mathbb E_x[V_1(X_1)\mid X_1\in\mathsf A^c]\le M/2$;
(iv) for $x\in\mathsf A$: $V_2(x)\le K$ and, if $P(x,\mathsf A^c)>0$, $\mathbb E_x[V_2(X_1)\mid X_1\in\mathsf A^c]\ge V_2(x)$;
(v) for $x\in\mathsf A$: $P(x,\mathsf A^c)\le q$ for a constant $q<\min\{1-\lambda_1,(1-\lambda_2)/K\}$.
Then for every $x\in\mathcal X$, $t\in\mathbb N$,
$$\|P^t(x,\cdot)-\pi\|_{\rm TV}\le4\alpha^{t+1}\Big(1+\frac{V_1(x)}M\Big),\quad\alpha=\frac{1+\rho^r}2=\frac{1+M^r/u}2\in(1-q/4,1),$$
$\rho=\frac{qK}{1-\lambda_2}$, $u=\frac1{1-q/2}$, $r=\frac{\log u}{\log(M/\rho)}$.
- Corollary 1: for a sequence of chains with $\lambda_1,\lambda_2\to1$ and $q\le\min\{1-\lambda_1,(1-\lambda_2)/CK\}$ for a universal $C>1$: $1-\alpha\sim\frac{(1-\lambda^*)\log C}{4\log(MC)}$, $1-\lambda^*=\min\{1-\lambda_1,\frac{1-\lambda_2}{CK}\}$.
- Corollary 2: $T_{\rm mix}(\epsilon)\lesssim\frac{4\log(6/\epsilon)}{\log C}\log(CM)\max\{\frac1{1-\lambda_1},\frac{CK}{1-\lambda_2}\}$.
- Proof (S2, pp. 35-39): split the path into excursions in $\mathsf A$ and $\mathsf A^c$ (auxiliary Bernoulli($q$) variables), bound the generating function of the hitting time of $x^*$, then use Theorem S1 (Jerison 2016 Theorem 4.5 version): if $\mathbb E_x[\lambda^{-\tau^*}]\le V(x)$ then $\|P^t(x,\cdot)-\pi\|_{\rm TV}\le2V(x)\lambda^{t+1}$ and $\|P^t(x^*,\cdot)-\pi\|_{\rm TV}\le\lambda^{t+1}$; Remark S1: this implies $\pi(x^*)\ge1-\lambda$.

### Lemma 2 (truncated locally balanced proposal, p. 29)
For arbitrary $\pi$ on a discrete space with neighbourhoods $\mathcal N(x)$, and $\tilde K_{\rm lb}(x,x')=\frac{\underline f\vee f(\pi(x')/\pi(x))\wedge\overline f}{\tilde Z_f(x)}\mathbb 1_{\mathcal N(x)}(x')$: if $f$ is non-decreasing, $f(b^{-1})\le\underline f$ and $b\ge\frac{\overline f}{\underline f}\max_x|\mathcal N(x)|$, then any proposed move with $\pi(x')/\pi(x)\ge b$ is accepted with probability $1$.

### Example 1 (pp. 3-4; proof S5.1, p. 50), the only slow-mixing statement
Two influential covariates $X_1,X_2$; design: $X_j^\top X_j=n$, $X_1^\top X_2=(\nu-1)n$, $X_i^\top X_j=0$ otherwise ($i<j$, other pairs); $y=X_1+X_2+z$ with deterministic $z$, $X^\top z=0$, $z^\top z=n$; hyperparameters $\kappa,g>0$, $p,\nu,\kappa,g$ fixed, $n\to\infty$; proposal $K_\nu(\gamma,\gamma')=\pi_n(\gamma')^\nu/\sum_{\tilde\gamma\in\mathcal N_1(\gamma)}\pi_n(\tilde\gamma)^\nu$ on single flips with $\nu\in(0,1]$. Then there are constants $a_1,a_2>0$ (depending on $\nu,g$) such that
$$K_\nu(\emptyset,\{1\}\cup\{2\})=1-O(e^{-a_1n}),\qquad P_\nu(\emptyset,\{1\}\cup\{2\})=O(e^{-a_2n}),$$
so $P_\nu(\emptyset,\emptyset)=1-O(e^{-a_1n})-O(e^{-a_2n})$: the MH chain with informed proposal stays at the null model for exponentially many steps although $\pi_n(\{1,2\})\gg\pi_n(\{i\})\gg\pi_n(\emptyset)\gg\pi_n(\{j\})$. Mechanism: the proposal is nearly deterministic towards $\{1\}$ or $\{2\}$ but the reverse proposal probability from $\{1\}$ back to $\emptyset$ is tiny ($\le(\pi_n(\emptyset)/\pi_n(\{1,2\}))^\nu$), so the acceptance ratio (2) is exponentially small. The paper states that RW-MH on the same example is rapidly mixing by the path method of Yang et al. (proof omitted). Note (my inference): the posterior in Example 1 is unimodal with respect to single flips (every state except $\{1,2\}$ has a strictly better neighbour in the chain's moves), so the failure is by rejection, not by a bottleneck of posterior mass.

## 4. Does any result cover (i)-(v)?
- (i) $\{0,1\}^p$: yes; state space $\mathcal M(s_0)\subset\{0,1\}^p$; Section 7.2 and Lemma 2 discuss general discrete spaces heuristically, Theorem 2 covers general reversible chains.
- (ii) BVS posterior: yes, the same Zellner-$g$-prior truncated-sparsity model as Yang et al. (not spike-and-slab; the introduction of Yang et al. makes the same remark). Our prior (beta-binomial on size, $g=n$ with unit ridge, $K=\lfloor n/2\rfloor$) is outside the stated assumptions (my inference, same reasons as in `THEORY_YangWainwrightJordan2016.md`: $g=p^{2\kappa_1}$ and $s_0\lesssim n/\log p$ are required).
- (iii) adaptive tempering: no. Only a remark (p. 31) that LIT-MH "can be combined with other MCMC techniques such as tempering, blocking and adaptive proposals", with no theory.
- (iv) frozen schedules: no.
- (v) evidence / normalising constant estimation: no.
- Also not covered: SMC or population methods; any multimodal posterior (Condition 1 is unimodality; the paper's own multimodal case, simulation II, is explicitly outside it: "severely multimodal and violate Condition 1", p. 44); a lower bound for the Zanella-Roberts tempered Gibbs sampler (it is only compared in words, p. 30); a lower bound for locally balanced MH on BVS (only simulation, Table 1, and the heuristic in 7.2-7.3).

## 5. Observations (my inference)
- Theorem 1 and Theorem S2 together say: when the posterior is unimodal in the add/delete/swap sense (Condition 1; high SNR or null truth plus RE-type design conditions, as in Yang et al.), a thresholded informed chain mixes in $O(n\kappa_1/c_1\vee s_0)$ steps. So for P1 the "trap" family must violate Condition 1, i.e. contain a local mode other than $\gamma^*$ under single flips (and, for chains with swaps, under swaps at the relevant sizes). The paper itself names the main mechanism: several influential covariates with large effects missing from $\gamma$, whose effects cancel through correlation, so that adding any one of them does not improve fit (S4.2, p. 44, and Section 2.2, p. 8). A P1 design with groups of such covariates is exactly a Condition-1 violation (inference).
- Evidence that informed single-flip chains can be slow also under Condition 1-like unimodality: Example 1 (proved) and Table 1, LB-MH-2 (locally balanced, $f=\sqrt b$, no move-type separation): at SNR $=3$ the number of successful runs out of 100 was 12 ($n=500,p=1000$, independent), 4 (correlated), 4 ($n=1000,p=5000$, independent), 0 (correlated) in 2000 iterations, while RW-MH after $10^5$ iterations succeeded in 100, 89, 99, 94. This is a simulation (acceptance rates collapse because $Z_f(x)$ varies sharply between neighbours, p. 28-29), not a theorem. The paper says LB-MH-1 (separate move types) behaves well in simulation but it is unclear whether it can attain a dimension-free rate (p. 30).
- Therefore the paper supports a P1 statement of the form "informed chains are not uniformly better", but gives no proof for Zanella-Roberts weighted tempered Gibbs. Zanella-Roberts tempered Gibbs is described as "conceptually very similar" to LIT-MH, selecting the coordinate from local posterior information, with an importance weight per iteration that "may reduce the efficiency when unbounded" (p. 30); this is a remark, not a result.
- Technical tool of independent interest: the two-stage drift condition (Theorem 2). For us it is a positive MCMC tool for unimodal posteriors; it needs a single fixed point $x^*$ and says nothing about SMC.
- Per-iteration cost: LIT-MH step costs $O(p|\gamma|^2)$ versus $O(|\gamma|^2)$ for RW-MH (p. 10), so iteration counts are not directly comparable (the paper presents this as paid for by the gain in iterations).
- Note on theory versus practice in this paper: Theorem 1 conditions on Condition 1 for the realised data (deterministic given the data); the probability statement is only in Theorem S2 through Yang et al.'s Lemma 4. This is a cleaner "data event then sampler theorem" structure than Yang et al.'s Theorem 2 and is the same logical form as our Thm 3 (high-probability data events, then a conclusion about the sampler output) (my inference).

## 6. Relation to us
- **Prop 5 (unbiased evidence given frozen calibration):** no relation (no SMC, no normalising constant). Cite Schweizer 2012a / Del Moral instead.
- **Thm 3 (every run reports the truth on high-probability data events):** supports in structure only. Theorem S2 gives a high-probability data event (Condition 1) on which Theorem 1 yields a quantitative statement about the sampler (rapid mixing, and by Remark S1 that the chain's stationary mass concentrates on $\gamma^*$, $\pi_n(\gamma^*)\ge1-\lambda$). Our Thm 3 should be positioned as the SMC analogue; the difference is that Condition 1 requires unimodality, while an SMC theorem need not (my inference; the Thm 3 hypotheses should be checked against this when writing the comparison). It does not compete as a result about SMC output.
- **P1 (trap theorem):** competes only in the sense of defining the boundary of where P1 can hold. (a) P1's design family must violate Condition 1 (a non-$\gamma^*$ local mode under add/delete/swap) and, if the target includes chains with swaps, the swap-trap must be shown separately. (b) Example 1 is a proved slow-mixing result for a different mechanism (informed single-flip proposals with exponent $\nu$, fixed $p$, $n\to\infty$), unimodal posterior; it does not cover Zanella-Roberts and does not use multimodality. (c) The simulation 5.3 / S4.3 show that on multimodal designs RW-MH has far worse effective sample size per second than LIT-MH, and that the number of discovered local modes keeps growing with run length (Table 7: from 6.2 to 37.6 at $\sigma_\beta=0.2$ going from 2K to 500K iterations); empirical support that multimodality is practically relevant, not a lower bound. (d) The paper's positive result for LIT-MH cannot be used against P1 unless the P1 family satisfies Condition 1, which by design it will not. So P1 remains open for single-flip RW-MH on a multimodal family, for locally balanced chains, and for weighted tempered Gibbs, and this paper plus Yang et al. are the prior art against which P1 must be positioned.

## 7. Citations we should make
1. Zhou, Yang, Vats, Roberts and Rosenthal (2022), arXiv:2105.05719 (JRSS-B 2022, from memory): Theorem 1 (LIT-MH $T_{\rm mix}\le800\max\{n\kappa_1/c_1,3s_0\}$ under Condition 1) and Condition 1 / Definition 1 (unimodality); Example 1 (proved slow mixing of informed single-flip MH, exponent $\nu$).
2. Zhou et al. Theorem 2 (two-stage drift condition) only if we need a unimodal-posterior MCMC mixing tool.
3. Yang, Wainwright and Jordan (2016) for the RW-MH rapid-mixing result under the same conditions (see `THEORY_YangWainwrightJordan2016.md`) and Theorem S2 / Lemma 4 for how Condition 1 arises.
4. Zanella (2020), J. Amer. Statist. Assoc. 115:852-865 (locally balanced proposals) and Zanella and Roberts (2019), J. R. Stat. Soc. B 81:489-517 (tempered Gibbs, scalable importance tempering), as the chains P1 targets. Note: Zhou et al. do not prove anything about the latter.
5. Jerison (2016), PhD thesis, Stanford (drift and hitting times; Theorem S1) only if the two-stage drift route is used.
