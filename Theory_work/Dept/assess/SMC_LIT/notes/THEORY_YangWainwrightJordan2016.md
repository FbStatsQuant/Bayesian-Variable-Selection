# THEORY note: Yang, Wainwright and Jordan (2016), on the computational complexity of high-dimensional Bayesian variable selection (MCMC comparator for P1)

Reader: Claude (Sonnet 5.5), 2026-11-24. Private to this machine. Page numbers are PDF pages of the local file. "(my inference)" marks anything the paper does not state itself; "(from memory, not checked)" marks facts from outside the paper.

## 0. Bibliographic and file caveat
- Title: On the Computational Complexity of High-Dimensional Bayesian Variable Selection. Authors: Yun Yang, Martin J. Wainwright, Michael I. Jordan (UC Berkeley). Local file is arXiv:1505.07925v1 [math.ST], dated 1 June 2015, 42 pages. Published in Annals of Statistics 2016 (vol. 44, no. 6; pages from memory, not checked). The published version may differ from v1 in constants and numbering; quote constants only with this caveat.
- Local file: `/home/fb31/SMC_Theory_Department/SMC_LIT/papers/YangWainwrightJordan2016_complexity_BVS.pdf`.
- Read as comparator for P1 only: main theorems, assumptions, lower-bound / slow-mixing example (Appendix A.2) in full; the proofs were read to the level needed to know which assumptions are used where. Appendix B and C case analyses were read but are summarised, not restated.
- Typographical slips noticed (not fixed): the last line of B.3 refers to "(62)" which is an equation in Appendix C; (47) writes $n^\kappa$ where the general formula has $p^\kappa$ (they set $p=n$ there).

## 1. Coverage log
| PDF pages | Content |
|---|---|
| 1-3 | Abstract, 1 Introduction (motivation, literature, contributions, outline) |
| 4-6 | 2 Background: 2.1 BVS notation, 2.2 MH random walks (single flip plus double flip, eq. (3)), 2.3 mixing times (eq. (4)) |
| 6-8 | 3.1 Hierarchical model (5a)-(5d), Assumptions A (conditions on $\beta^*$), B (RE and sparse projection), C (hyperparameters), D (sparsity control) |
| 9-10 | 3.2 Theorem 1 (posterior concentration), Corollary 1; 3.3 Theorem 2 (rapid mixing), Corollary 2 |
| 10-14 | 3.4 Simulations: 3.4.1 mixing comparison (Fig. 1, Tables 1-2); 3.4.2 Bayes versus Lasso (Fig. 2, $\Sigma_{\text{bad}}$) |
| 15-25 | 4 Proofs: 4.1 proof of Theorem 2 (lazy chain, sandwich (14), canonical paths (16), memoryless path ensemble, Lemma 1, Lemmas 2-6 on the transition function $\mathcal G$ and events, congestion bound, gap (15)); 4.2-4.4 proof of Theorem 1 (Lemmas 3 and 7, steps 1-2) |
| 26-28 | End of proof of Theorem 1 ((35)-(40)); 4.5 proof of Corollary 2; 5 Discussion |
| 28-30 | Appendix A: MAP / $\ell_0$ connection and marginal likelihood (A.1, eq. (41)-(42)); A.2 example of slow mixing, conductance argument (43)-(46) |
| 31 | End of A.2: eq. (47)-(49) |
| 31-36 | Appendix B: proof of inequality (23a) in Lemma 4: B.1 overfitted, B.2 underfitted-unsaturated, B.3 underfitted-saturated, B.4 Lemma 8 and proof |
| 37-39 | Appendix C: proof of Lemma 7 (overfitted and underfitted cases) |
| 40-42 | References (41 items) |
All 42 pages read.

## 2. Setting
- Gaussian linear model $Y=X\beta^*+w$, $w\sim N(0,\sigma_0^2 I_n)$, $p\ge n$ (high-dimensional), columns normalised $\|X_j\|_2^2=n$. Frequentist truth; the Bayesian posterior is analysed under the true law.
- Hierarchical prior $\mathbb M_\gamma$ (eq. (5)): $\pi(\phi)\propto 1/\phi$; $(\beta_\gamma\mid\gamma)\sim N(0,g\phi^{-1}(X_\gamma^TX_\gamma)^{-1})$ (Zellner $g$-prior); $\pi(\gamma)\propto p^{-\kappa|\gamma|}\,\mathbb I[|\gamma|\le s_0]$ (truncated sparsity prior). Closed form $\pi_n(\gamma\mid Y)\propto p^{-\kappa|\gamma|}(1+g)^{-|\gamma|/2}\big(1+g(1-R_\gamma^2)\big)^{-n/2}$, $R_\gamma^2=Y^T\Phi_\gamma Y/\|Y\|_2^2$ (eq. (42)).
- Chain: reversible Metropolis-Hastings on $\mathscr M=\{\gamma:|\gamma|\le s_0\}\subset\{0,1\}^p$, each step a single flip or a double flip (swap one active with one inactive index), each with probability $1/2$ (eq. (3)); the lazy version $\mathbf P=\tilde{\mathbf P}/2+I/2$ is analysed. Mixing time $\tau_\epsilon=\max_\gamma\min\{t:\Delta_\gamma(t')\le\epsilon\ \forall t'\ge t\}$, worst-case start (eq. (4)).
- True set: $S=\{j:|\beta^*_j|\ge C_\beta\}$, $\gamma^*=1_S$, $s^*=|S|$.

## 3. Main theorems (faithful statements)

### Assumptions (pp. 7-8)
- **Assumption A** (conditions on $\beta^*$): $\big\|\tfrac1{\sqrt n}X\beta^*\big\|_2^2\le g\sigma_0^2\tfrac{\log p}{n}$ and $\big\|\tfrac1{\sqrt n}X_{S^c}\beta^*_{S^c}\big\|_2^2\le\tilde L\sigma_0^2\tfrac{\log p}{n}$ for a universal constant $\tilde L$. (If $\beta^*$ is exactly $S$-sparse the second holds with $\tilde L=0$.)
- **Assumption B** (design, at level $s$): $\|X_j\|_2^2=n$, and there are $\nu>0$, $L<\infty$ with
$$\text{RE}(s):\ \min_{|\gamma|\le s}\lambda_{\min}\big(\tfrac1nX_\gamma^TX_\gamma\big)\ge\nu,\qquad \text{SI}(s):\ \mathbb E_Z\Big[\max_{|\gamma|\le s}\max_{k\in[p]\setminus\gamma}\tfrac1{\sqrt n}\big|\langle(I-\Phi_\gamma)X_k,Z\rangle\big|\Big]\le\tfrac12\sqrt{L\nu\log p},$$
with $Z\sim N(0,I_n)$, $\Phi_\gamma$ the projection onto $\mathrm{span}\{X_j,j\in\gamma\}$. The paper notes SI($s$) always holds with $L=4\nu^{-1}s$ and, for orthogonal columns, with $L=4\nu^{-1}$ (p. 8).
- **Assumption C** (hyperparameters): $g\asymp p^{2\alpha}$ for some $\alpha>0$, and $\kappa+\alpha\ge C_1(L+\tilde L)+2$ for a universal $C_1$.
- **Assumption D** (sparsity control), for a constant $C_0>4$ one of:
  - **D($s^*$)**: $s_0:=p$ and $s^*\le\frac1{8C_0K}\big\{\frac n{\log p}-16\tilde L\sigma_0^2\big\}$ with $K\ge4+\alpha+c\tilde L$;
  - **D($s_0$)**: $(2\nu^{-2}\omega(X)+1)s^*\le s_0\le\frac1{8C_0K}\big\{\frac n{\log p}-16\tilde L\sigma_0^2\big\}$, where $\omega(X)=\max_{\gamma\in\mathscr M}\|(X_\gamma^TX_\gamma)^{-1}X_\gamma^TX_{\gamma^*\setminus\gamma}\|_{\mathrm{op}}^2$.
- **Signal regimes** (eq. (9)): High SNR: $S=\{j:\beta_j^*\ne0\}$ and $\min_{j\in S}|\beta_j^*|^2\ge c_0(\alpha+\kappa+L)\sigma_0^2\frac{\log p}n$. Low SNR: $S=\emptyset$ and $\|\tfrac1{\sqrt n}X\beta^*\|_2^2\le\big(\frac{\alpha+\kappa-2}{C_1}-L\big)\sigma_0^2\frac{\log p}n$. The intermediate regime (10) is explicitly NOT covered.

### Theorem 1 (posterior concentration, p. 9)
Suppose Assumption A, Assumption B with $s=Ks^*$, Assumption C, Assumption D($s^*$). If the threshold satisfies $C_\beta^2\ge c_0(L+\tilde L+\alpha+\kappa)\sigma_0^2\frac{\log p}n$ (eq. (8)), then
$$\pi_n(\gamma^*\mid Y)\ge1-c_1p^{-1}\quad\text{with probability at least }1-c_2p^{-c_3}.$$
Corollary 1: under the high-SNR condition (9a) the posterior concentrates on $\gamma^*$; under the low-SNR condition (9b) it concentrates on the null model $\gamma_0$, both with the same bound and probability.

### Theorem 2 (rapid mixing, p. 10)
Suppose Assumption A, Assumption B with $s=s_0$, Assumption C, Assumption D($s_0$) hold. Then under either the high-SNR (9a) or low-SNR (9b) condition there are universal constants $c_1,c_2$ such that for any $\epsilon\in(0,1)$ the $\epsilon$-mixing time of the MH chain (3) satisfies
$$\tau_\epsilon\le c_1\,p\,s_0^2\Big(c_2\,\alpha\,(n+s_0)\log p+\log(1/\epsilon)+2\Big)\quad(11)$$
with probability at least $1-4p^{-c_1}$ (probability over the data). Worst-case start; the $n$ term can be dropped if one starts at $\gamma^*$ (paper's remark, p. 10).

### Corollary 2 (p. 10)
Under the conditions of Theorem 2, for any fixed iterate $t\ge c_1ps_0^2\big(c_2\alpha(n+s_0)\log p+\log p+2\big)$, $\gamma_t=\gamma^*$ with probability at least $1-c_2p^{-c_3}$.

### Proof architecture of Theorem 2 (pp. 15-25, my summary of what was read)
1. Sandwich (14): $\frac12\frac{1-\mathrm{Gap}}{\mathrm{Gap}}\log\frac1{2\epsilon}\le\tau_\epsilon\le\frac{\log[1/\min_\gamma\pi(\gamma)]+\log(1/\epsilon)}{\mathrm{Gap}}$ for the lazy chain. Sufficient: $\mathrm{Gap}(\mathbf P)\ge c_2/(ps_0^2)$ (15) with probability $\ge1-4p^{-c_1}$. The lower bound on $\min_\gamma\pi(\gamma\mid Y)$ uses Theorem 1 and (42).
2. Canonical paths (Sinclair 1992, eq. (16)): $\mathrm{Gap}\ge1/(\rho(\mathcal T)\ell(\mathcal T))$ with $\rho$ the congestion and $\ell$ the longest path length.
3. A memoryless canonical-path ensemble towards the true model $\gamma^*$ is built from a transition function $\mathcal G$ (Lemma 1: valid if $d_H(\mathcal G(\gamma),\gamma^*)<d_H(\gamma,\gamma^*)$). $\mathcal G$ mimics greedy stepwise selection: overfitted $\gamma$ drops an uninfluential index $\ell_\gamma$; underfitted and unsaturated $\gamma$ adds the influential index $j_\gamma$ maximising $\|\Phi_{\gamma\cup\{j\}}X_{\gamma^*}\beta^*_{\gamma^*}\|^2$; underfitted and saturated ($|\gamma|=s_0$) swaps (add $j_\gamma$, remove $k_\gamma$).
4. Lemma 4 (inequality (23a)): on a high-probability event the posterior ratio $\pi_n(\gamma\mid Y)/\pi_n(\mathcal G(\gamma)\mid Y)\le p^{-2}$ (overfitted) or $\le p^{-3}$ (underfitted) (B.1-B.3, eq. (50), (53), and the saturated case). This is the "global drift towards the truth" that makes paths cheap. Lemma 8 (B.4) is the swap lemma that needs $s_0\ge(2\nu^{-2}\omega(X)+1)s^*$.
5. Appendix C, Lemma 7: for any $\gamma\ne\gamma^*$ in $\mathbb M_S$, $\pi_n(\gamma\mid Y)/\pi_n(\gamma^*\mid Y)\le p^{-2|\gamma\setminus\gamma^*|}$ (overfitted) or $p^{-2|\gamma|-2}$ (underfitted); a counting argument gives $\pi_n(\mathbb M_S\mid Y)\le3p^{-1}$, which is used for Theorem 1 and for the lower bound on $\pi_n$ in step 1.

### Slow-mixing example (Appendix A.2, pp. 30-31) (the only "lower bound")
Setting: $p=n$, $g=p^{2\alpha}$ with $\alpha>1$, $Y=w\sim N(0,I_n)$ (null truth), and the UNTRUNCATED prior $\pi(\gamma)=Cp^{-\kappa|\gamma|}$ on all of $\{0,1\}^p$. Claim: with probability at least $1/2$ over $w$, the mixing time of chain (3) "grows exponentially in $n$"; the example satisfies the conditions of Theorem 1 (so posterior consistency holds).
Proof device: conductance. For reversible finite chains $1-\lambda_2\le2\Phi_{\mathcal C}$ with $\Phi_{\mathcal C}=\min_{0<\pi(B)<1}\frac{\sum_{\gamma\in B}\pi(\gamma)P(\gamma,B^c)}{\pi(B)\pi(B^c)}$ (eq. (43)-(44), Sinclair 1992). Take $B=\{\mathbf 1\}$ (full model). Its only neighbours are $\mathbf 1_{-j}$, so
$$1-\lambda_2\le\frac{\sum_{j=1}^n\min\{1,\pi_n(\mathbf 1_{-j}\mid Y)/\pi_n(\mathbf 1\mid Y)\}}{n(1-\pi_n(\mathbf 1\mid Y))}\quad(46).$$
Under the null truth (47): $\frac{\pi_n(\mathbf1_{-j}|Y)}{\pi_n(\mathbf1|Y)}=\frac{n^\kappa(1+g)^{1/2}}{(1+gw^T(I-P_{-j})w/w^Tw)^{n/2}}$. Via chi-square tails and a union bound, with probability $\ge1/2$: $\min_j\pi_n(\mathbf1_{-j}|Y)/\pi_n(\mathbf1|Y)\le e^{-c_3gn^{-2}}$ (48), and $\pi_n(\mathbf1|Y)\le1/2$ (49). Hence
$$\mathbb P\big(1-\lambda_2\le2e^{-c_3gn^{-2}}\big)\ge\tfrac12.$$
Observation (my inference from (48)): with $g=p^{2\alpha}=n^{2\alpha}$ the bound reads $e^{-c_3n^{2\alpha-2}}$. This is super-polynomially small for every $\alpha>1$ and exponential in $n$ only when $2\alpha-2\ge1$, i.e. $\alpha\ge3/2$. The text says "exponentially in $n$" without this qualification. Note also that the displayed inequality is on the spectral gap of the lazy-or-not chain via the Cheeger-type upper bound; slow mixing in $\tau_\epsilon$ then follows from the left side of the sandwich (14).

## 4. Does any result cover (i)-(v)?
- (i) $\{0,1\}^p$: yes for the chain's state space, with the constraint $|\gamma|\le s_0$ (Theorem 2) or none (A.2). Results concern MH on this space, not SMC.
- (ii) BVS posterior: yes, but only the Zellner-$g$-prior model with truncated $p^{-\kappa|\gamma|}$ sparsity prior, $g\asymp p^{2\alpha}$, $\sigma$ integrated with Jeffreys prior. The paper states the conclusions "remain valid" for the independent prior and spike-and-slab "with much longer proofs" (p. 7); no proof is given. Our prior (beta-binomial on size, $g=n$ with unit ridge, IG(0.01,0.01) on $\sigma^2$, $K=\lfloor n/2\rfloor$) is outside Assumption C and D (my inference: $g=n$ is not $\asymp p^{2\alpha}$ for $p\gg n$, and $K=n/2$ exceeds the allowed $s_0\lesssim n/\log p$).
- (iii) adaptive tempering: no.
- (iv) frozen schedules: no. No tempering at all.
- (v) evidence / normalising constant: no. Only the closed-form marginal likelihood of a single $\gamma$ (41).
- Also not covered: any SMC, particle method, or Zanella-Roberts / weighted tempered Gibbs; the intermediate-SNR regime; a rigorous lower bound that holds under the posterior-consistency conditions (the A.2 example has an untruncated prior and null truth; for the intermediate regime they only "suspect" slow mixing and give simulations, pp. 10, 12).

## 5. Observations (my inference)
- Theorem 2 is an UPPER bound for single-plus-double-flip MH on the posterior over $\mathscr M(s_0)$. It limits what P1 can claim: single/double-flip MH is provably rapidly mixing, with $\tau\lesssim ps_0^2(n+s_0)\log p$, whenever A, B($s_0$), C, D($s_0$) and high or low SNR hold. A P1 statement must therefore be made on a design family that violates at least one of: RE($s_0$) (a restricted eigenvalue lower bound at level $s_0$), SI($s_0$), the sparsity window $(2\nu^{-2}\omega(X)+1)s^*\le s_0$, Assumption C on $(g,\kappa)$, or the signal regimes (9a)/(9b) (intermediate SNR, eq. (10)). Theorem 2 includes the swap (double flip) in its chain, so a P1 lower bound for a chain with swaps needs the design to break these conditions; a lower bound for pure single flip is a separate matter.
- The intermediate-SNR regime is where the paper itself reports slow mixing in simulation with correlated design: Table 2, $(n,p)=(500,5000)$, SNR $=1$, success proportion $15\%$ (GR$\le1.5$ within $20p$ iterations), and $(500,1000)$ SNR $=1$, $95\%$; with $n=1000$ all settings succeed. This is empirical motivation for P1, not a proof (p. 12).
- Templates available for P1: (a) the conductance bound with $B$ a mode set (A.2) is the standard route; the lower-bound direction needs a set $B$ with small boundary flow, i.e. a bottleneck in posterior mass between modes, and uses only $1-\lambda_2\le2\Phi$ (Sinclair 1992) plus the sandwich (14). (b) Their multimodality example is a local mode of size $n$ (the full model), reachable only through single deletions each of ratio $e^{-c\,gn^{-2}}$; it relies on an untruncated prior and a null truth, so it does not by itself show slow mixing "where consistency holds with a truncation".
- Mode-mass connection to the other papers: the A.2 argument is the MCMC counterpart of the Schweizer / Mathews-Schmidler growth criterion (conductance of a mode versus mass gain); (my inference) P1 can be organised as: same design, same posterior, (a) conductance of single-flip and weighted tempered Gibbs bounded by $e^{-cn^{\delta}}$, (b) our SMC consistency by Theorem 3, with the tempered path bridging the modes.
- The paper contains no result that depends on the number of chains, restarts, or independence moves; our independence proposals from $\pi_0$ and the island structure are outside its scope.

## 6. Relation to us
- **Prop 5 (unbiased evidence given frozen calibration):** no relation. The paper does not treat SMC or normalising constants; cite Schweizer 2012a / Del Moral for Prop 5.
- **Thm 3 (every run reports the truth on high-probability data events):** supports only in the following limited sense. Theorem 1 (with Corollary 1) is a posterior-concentration result of exactly the type our Thm 1/2 need as an ingredient (concentration of the posterior on $\gamma^*$ with probability $1-c_2p^{-c_3}$ over data), and it uses the same flavour of conditions (RE, sparse-projection, beta-min, sparsity). It is not a theorem about a sampler's output, and its model (Zellner $g=p^{2\alpha}$, truncated $p^{-\kappa|\gamma|}$ prior) differs from ours. Cite it as a related posterior consistency result for the $g$-prior BVS with $p\gg n$; compare conditions with ours before claiming overlap. Theorem 2 and Corollary 2 give the analogous sampler-output statement for single/double-flip MH ("$\gamma_t=\gamma^*$ w.h.p. after $O(\alpha nps_0^2\log p)$ steps") and so are a benchmark: our Thm 3 should say it holds beyond the regime where they apply.
- **P1 (trap theorem):** competes in the following precise sense and limits the statement. Theorem 2 proves rapid mixing of single plus double flip MH under A-D and (9a)/(9b); P1's design family must lie outside these conditions (see Section 5) and must be shown to do so. Conversely, the A.2 example and the simulations in Table 2 give precedent that posterior consistency does not imply rapid mixing ("sharp concentration of the posterior need not lead to rapid mixing", p. 10), which is the same message as P1, but only for single/double flip MH, with an untruncated prior and null truth. They do not cover Zanella-Roberts weighted tempered Gibbs, and give no lower bound in the regime of positive signal. So P1 is a new result relative to this paper, and this paper is the key prior art that P1's introduction must position against.

## 7. Citations we should make
1. Yang, Wainwright and Jordan (2016), Ann. Statist. 44(6), arXiv:1505.07925: Theorem 2 (rapid mixing of single/double-flip MH under RE/SI/signal conditions) and Appendix A.2 (conductance-based slow mixing though posterior consistency holds). Cite as the baseline P1 must be compared to; state which of their Assumptions A-D the P1 design violates.
2. Sinclair (1992), Combinatorics, Probability and Computing 1:351-370 (canonical paths, conductance; both used in the paper). Diaconis and Stroock (1991), Ann. Appl. Probab. 1:36-61.
3. Narisetty and He (2014), Ann. Statist. 42:789-817 (BVS consistency with $p$ nearly exponential in $n$), as cited by the paper, for the posterior-consistency side of our Thm 1/2 comparison.
4. Zhou et al. (2022) for the dimension-free spectral-gap statement of locally-balanced MCMC (see `THEORY_ZhouEtAl2022.md`) in the same P1 discussion.
5. Lawler and Sokal (1988) for the Cheeger-type two-sided bound between conductance and spectral gap (from memory, not checked; the paper itself cites only Sinclair for (43)).
