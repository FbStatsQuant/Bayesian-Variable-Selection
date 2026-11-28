# THEORY note: Paulin, Jasra and Thiery (2019), error bounds for SMC samplers on multimodal distributions

Reader: Claude (Sonnet 5.5), 2026-11-24. Private to this machine. Page numbers are PDF pages of the local file. "(my inference)" marks anything the paper does not state itself; "(from memory, not checked)" marks facts from outside the paper.

## 0. Bibliographic and file caveat
- Title: Error bounds for sequential Monte Carlo samplers for multimodal distributions. Authors: D. Paulin, A. Jasra, A. Thiery (NUS). Venue: Bernoulli 25(1):310-340 (2019), DOI 10.3150/17-BEJ988.
- THE LOCAL FILE IS THE arXiv PREPRINT: stamp "arXiv:1509.08775v4 [math.PR] 24 Jan 2018", dated "January 25, 2018" on p.1. Published Bernoulli numbering/constants may differ.
- Local file: `/home/fb31/SMC_Theory_Department/SMC_LIT/papers/PaulinJasraThiery2019_SMC_multimodal_error_bounds.pdf`, 42 pages, every page read as an image.

## 1. Coverage log
| PDF pages | Content |
|---|---|
| 1-3 | Abstract, 1 Introduction, 1.1 Notation |
| 3-5 | 2 Preliminaries: Polish space, bounded Radon-Nikodym derivatives $\Gamma_g$, SMC algorithm, CLT (2.2), asymptotic variance (2.3) |
| 5-6 | 3 Bounds on asymptotic variance; 3.1 global mixing, Theorem 3.1 |
| 6-8 | 3.2 multimodal case with mixing between modes: metastable approximation (3.6), Theorem 3.2 |
| 8-10 | 3.3 framework for metastable approximation: Theorem 3.3 |
| 10-11 | 4 Interpolation to independence sequence |
| 11-14 | 5 Application to the 3-colour mean-field Potts model: 5.1 intro, Fig 1, 5.2 Theorem 5.1 |
| 14-26 | 6 Proofs for the Potts model: 6.1 Props 6.1-6.4 and proof of Thm 5.1; 6.2 Lemmas 6.5-6.8; 6.3 Lemma 6.9; 6.4 Prop 6.10; 6.5 Prop 6.3 proof; 6.6 Prop 6.4 proof (Prop 6.13, Lemma 6.14); Acknowledgements |
| 26-29 | References (39 items) |
| 29-31 | Appendix A.1: Theorem A.1 (no mixing between modes) and a 4-point counterexample |
| 32-33 | A.2 proof of Lemma 6.9 |
| 33-35 | A.3 proofs of Lemmas 6.5, 6.7, 6.8 |
| 35-37 | A.4 proof of Prop 6.13 (curvature), Fig 6 |
| 38-41 | A.5 proof of Prop 6.2 (Lemmas A.1, A.2) |
| 41-42 | A.6 proof of Lemma 6.14 |
All 42 pages read.

## 2. Setting
- State space: a Polish space $(E,\mathcal E)$. Application: $\Omega=\{1,2,3\}^M$ (3-colour Potts on the complete graph, $M$ spins). Finite, NOT binary (q=3). The general theory covers any $E$.
- Target: $\mu_n=\mu$. Interpolating sequence $\mu_0,\dots,\mu_n$ with $\mu_{k+1}\ll\mu_k$ and $\Gamma_g=\max_k\|g_{k,k+1}\|_\infty<\infty$, $g_{k,k+1}=d\mu_{k+1}/d\mu_k$ (standing assumption p.4).
- Algorithm (p.4): $N$ iid draws from $\mu_0$; then for each $k$: mutation with a $\mu_k$-invariant kernel $\boldsymbol K_k$ (independently per particle), then multinomial resampling with weights $g_{k,k+1}$ (mutate-then-resample order), at EVERY step. Kernel $\boldsymbol K_k=\boldsymbol P_k^{t_k}$ for a base kernel $\boldsymbol P_k$.
- Bridge: arbitrary in the theory. Two cases: (a) standard tempering $\mu_i=\mu^{\mathrm{Potts}}_{\tilde\beta_c\cdot i/n,M}$ (discussed heuristically as bad, p.13); (b) the new "interpolation to independence" sequence (Sec 4): $\mu_k$ has the first $k$ coordinates distributed as the $k$-spin version $\eta_k$ of the model and the remaining coordinates iid uniform; kernels first move the first $k$ coordinates (Glauber) and then redraw the rest independently.
- Adaptivity: none. Deterministic schedule. (Adaptive SMC is cited as related work only, e.g. [15] Del Moral-Doucet-Jasra 2012; [17] Giraud-Del Moral.)
- The result is ASYMPTOTIC in $N$ (CLT). Its quantities are the asymptotic variance $V_n(\varphi)$; nothing at finite $N$ (p.2: "Proving non-asymptotic bounds under similar conditions is an interesting problem for further research").

## 3. Main theorems (faithful statements)

**CLT and variance formula (pp.4-5; from Chopin 2004 / Del Moral-Miclo 2000, quoted).** For $\varphi\in L_0^{2+}(\mu)$ (mean zero, finite moment of order $2+\varepsilon$), $N^{1/2}[\mu_n^N-\mu](\varphi)\Rightarrow\mathcal N(0,V_n(\varphi))$ with
$$V_n(\varphi)=\sum_{k=0}^nV_{k,n}(\varphi),\qquad V_{k,n}(\varphi)=\big\|\boldsymbol G_{k,k+1}\boldsymbol K_{k+1}\boldsymbol G_{k+1,k+2}\cdots\boldsymbol G_{n-1,n}\boldsymbol K_n\varphi\big\|^2_{L^2(\mu_k)},\quad \boldsymbol G_{k,k+1}\varphi=g_{k,k+1}\varphi,$$
$V_{n,n}=\mathrm{Var}_\mu\varphi$.

**Theorem 3.1 (global mixing; p.5).** Let $\gamma_{\boldsymbol K}:=1-\max_{1\le k\le n}\|\boldsymbol K_k-\mu_k\|_{L^2(\mu_k)}$ and suppose $\Gamma_g<1/(1-\gamma_{\boldsymbol K})^2$. Then the CLT holds with
$$V_n(\varphi)\le\frac{1}{1-(1-\gamma_{\boldsymbol K})^2\Gamma_g}\,\mathrm{Var}_{\mu_n}(\varphi).$$
(Independent of the number of stages $n$; improves a quadratic bound of Schweizer's thesis.) Needs a uniform spectral gap for all $K_k$ (global mixing; for reversible kernels $\gamma_{\boldsymbol K}$ is a lower bound on the absolute spectral gap).

**Theorem 3.2 (multimodal, mixing between modes allowed; p.7).** Partitions $E=\bigsqcup_{j=1}^{m(k)}F_k^{(j)}$ that may vary with $k$; growth-within-mode constant $B_{k,k+1}=\max_r\mu_{k+1}(F_k^{(r)})/\mu_k(F_k^{(r)})$; metastable approximation $\widehat{\boldsymbol\mu}_k(x,\varphi)=\sum_{r}\alpha_{k,r}(x)\,\mu_{k,r}(\varphi_{|F_k^{(r)}})$ with $\sum_r\alpha_{k,r}(x)\le1$ ($\mu_{k,r}$ = restriction of $\mu_k$ to $F_k^{(r)}$). Assume $\Gamma_g<\infty$. For bounded measurable $\varphi$, the CLT holds with $V_n=\sum_kV_{k,n}$ and
$$V_{k,n}(\varphi)\le\Gamma_g\prod_{j=k+1}^{n-1}\big\{B_{j,j+1}+\Gamma_g\|\boldsymbol K_j-\widehat{\boldsymbol\mu}_j\|_\infty\big\}\,\|\varphi\|_\infty^2 .$$
(Sup-norm, so bounded test functions only; p.8.)

**Theorem 3.3 (quality of metastable approximation; p.9).** Modes split into inner regions $\mathcal I^{(i)}$ and border regions $\mathcal B^{(i)}$; $\widehat\pi^{(t)}(x,dy)=\mu^{(j)}(dy)$ for $x\in\mathcal I^{(j)}$, $=\sum_jq^{(j)}(x,\lfloor t/2\rfloor)\mu^{(j)}(dy)$ for $x\in\mathcal B$, where $q^{(i)}(x,t)=\mathbb P(X_{\tau_{\mathcal B}}\in\mathcal I^{(i)},\tau_{\mathcal B}\le t\mid X_0=x)$. Then
$$\|\boldsymbol P^t-\widehat\pi^{(t)}\|_\infty\le\max_{x\in\mathcal B}\mathbb P(S_{\mathcal B}(x,\lfloor t/2\rfloor))+2\max_{i}\max_{\lceil t/2\rceil\le r\le t}\sup_{x\in\mathcal I^{(i)}}d_{TV}(\boldsymbol P^r(x,\cdot),\mu^{(i)}),$$
$S_{\mathcal B}(x,t)$ = "start at $x\in\mathcal B$ and stay in $\mathcal B$ for $t$ steps".

**Theorem A.1 (no mixing between modes; Appendix A.1, pp.29-31).** If $\boldsymbol K_k(x_r,F^{(r)})=1$ (no crossing), $A=\max\{\mu_k(F^{(r)})/\mu_j(F^{(r)}):0\le j<k\le n\}$, $\gamma^{loc}_{\boldsymbol K}$ the uniform local gap of restricted kernels, and $\Gamma_g<1/(1-\gamma^{loc}_{\boldsymbol K})^2$, then
$$V_n(\varphi)\le\Big(1+\frac{nA\Gamma_g}{1-(1-\gamma^{loc}_{\boldsymbol K})^2\Gamma_g}\Big)\mathrm{Var}_\mu(\varphi).$$
(Grows linearly in $n$; the paper notes this cannot be removed in general (p.31).) Counterexample (pp.31-32): a 4-state, 2-stage SMC where allowing mixing between modes INCREASES the asymptotic variance (0.1669 vs 0.1579), so "mixing between modes can only help" is false in general.

**Theorem 5.1 (3-colour mean-field Potts at the critical temperature; p.13).** Complete graph, $q=3$, $\tilde\beta=\tilde\beta_c=2\log2$, $\mu_k$ = interpolation-to-independence sequence, $\boldsymbol K_k=\boldsymbol P_k^{t_k}$ with $\boldsymbol P_k$ one Glauber step on the first $k$ spins plus redrawing the rest independently, and $t_k=\lceil C_1\log(k)^2\rceil$. Then there are absolute constants $C_1,C_2$ with
$$V_M(f)\le C_2\,M\,\|f\|_\infty^2\quad\text{for every bounded }f:\Omega\to\mathbb R.$$
Total effort for unit variance $\mathcal O(M^3\log^2M)$ (p.13-14), improving the polynomial rate of Bhatnagar-Randall (2015) for simulated tempering with entropy-dampening distributions. Authors "believe" it extends to any $\tilde\beta$ and $q$ but prove only $\tilde\beta_c$.
Key propositions (pp.15-16): Prop 6.1 $\Gamma_g\le\exp(2\tilde\beta_c)$; Prop 6.2 $B_{j,j+1}\le1+C\log(j)^5/j^{3/2}$, so $\prod_jB_{j,j+1}\le C_B<\infty$; Prop 6.3 hitting time of a mode centre within $CM\log M$ steps; Prop 6.4 local TV mixing after $k\ge330M\log M$ Glauber steps, $d_{TV}\le C/M^2+3k^2\exp(-C'M)$. Supporting Lemmas 6.5-6.14, Prop 6.10, 6.13 (coarse Ricci curvature of the restricted magnetisation chain, via Ollivier 2009), A.1, A.2.

## 4. Does any result cover ...
- (i) Binary spaces {0,1}^p: NOT binary; discrete product space $\{1,2,3\}^M$. The general theorems (3.1-3.3, A.1) hold on any Polish space, including $\{0,1\}^p$, but need the user to supply partitions, $B$-constants and local mixing. The "interpolation to independence" bridge is defined for product spaces $\Lambda^d$ (any finite $\Lambda$) and requires a SCALE-INVARIANT family of targets in increasing dimension (modes' number, positions and masses essentially constant after coordinate scaling).
- (ii) BVS / spike-and-slab posterior: NO.
- (iii) Adaptive tempering: NO.
- (iv) Frozen schedules: YES, only fixed schedules (in the sense that the schedule and kernels are deterministic).
- (v) Evidence / normalising constants: NO result.

## 5. Observations relevant to us (my inference unless marked)
1. The paper is the clearest published instance of the pattern behind P1 on a discrete product space: local single-site dynamics (Glauber) mix exponentially slowly at and beyond criticality (Cuff et al. 2012, cited p.13; from memory, not checked in detail), standard tempering-based PT/ST are torpid (Bhatnagar-Randall 2004, Woodard et al. 2009b), yet an SMC sampler with a well-chosen BRIDGE (not temperature) and only local Glauber moves is polynomial. This supports the narrative of P1 and of our design: success is by the bridge plus local moves, not by global kernel mixing.
2. It names exactly the difficulty our "visibility/leakage assumption" in Thm 3 addresses: "some of the modes have exponentially small probability according to the initial distribution, and thus they might take exponentially long time to be discovered" (p.11, p.13). Our start law $\pi_0$ (block-exact marginals) is designed to make the right mode visible; their interpolation to independence makes all modes appear at constant relative mass from the start. This is the closest conceptual cousin of our assumption. Cite for the motivation of start-law visibility.
3. The claim that SMC with geometric tempering fails on Potts is heuristic here: "it is not difficult to see heuristically... (we have some numerical evidence for this)" and "the product of the growth-within-mode constants grows exponentially with M" (p.13). No theorem. (Proved negative results are for PT/ST.) So there is no proved lower bound for tempered SMC in this paper.
4. All results are asymptotic in $N$ at fixed system size. The variance bounds give a CLT scaling $V/N$, not a finite-$N$, finite-$p$ guarantee, and say nothing about the probability of an event such as "the output model equals $S_0$".
5. Theorem 3.2's constants are not directly usable for BVS without computing $B_{j,j+1}$ and $\|K_j-\widehat\mu_j\|_\infty$; for the posterior-concentration regime the mode masses move from order-one under the early bridge to $\mathrm{e}^{-cn}$ at the end, so $\prod_jB_{j,j+1}$ would be exponentially large for any fixed partition that tracks a vanishing mode, the same obstruction as for Mathews-Schmidler.

## 6. Relation to us
- Prop 5 (unbiased evidence): no overlap; the paper has no evidence result. Classical source for the unnormalised-measure unbiasedness and for the CLT/variance of $\hat Z$ with fixed schedule: Del Moral (2004, Feynman-Kac Formulae) and Del Moral-Doucet-Jasra (2006) [refs [12], [14] of this paper], plus Chopin (2004) for the CLT; the variance formula here (2.3) is the Chopin/Del Moral-Miclo one. For frozen-calibration unbiasedness cite the first two (from memory; verify theorem numbers).
- Thm 3 (every run reports the truth): no overlap. Different object (asymptotic variance of an empirical average for a fixed target) and different mode of guarantee (asymptotic in $N$, no data events).
- P1: SUPPORTS the story and the method of proof (metastability, local Glauber, bridge design) on a discrete multimodal target; does not compete (no BVS, no weighted tempered Gibbs, no lower bound for MCMC chains on BVS). It also does not provide a lower bound technique for our single-flip chain; for that use Woodard-Schmidler-Huber (persistence/overlap) and Yang-Wainwright-Jordan-type canonical-path arguments (see notes on those papers).
- Possible referee question: "The Potts result shows SMC polynomial where tempering is torpid; does it show our sampler is polynomial on the trap family?" Answer: no; it supports the design principle only, and our consistency theorem rests on Thm 3.

## 7. Citations we should make
1. Paulin, Jasra, Thiery (2019, Bernoulli 25:310-340), as the nearest asymptotic-variance theory for SMC on a multimodal DISCRETE space, with local Glauber moves and a non-tempering bridge, and for the visibility-of-modes motivation.
2. Cuff, Ding, Louidor, Lubetzky, Peres, Sly (2012, J. Stat. Phys. 149:432-477) for slow mixing of Glauber dynamics on mean-field Potts; Bhatnagar and Randall (2004) for torpid tempering; Woodard-Schmidler-Huber (2009b) for sufficient conditions for torpid mixing of PT/ST (these are the tools P1 can parallel).
3. Chopin (2004, Ann. Statist. 32:2385-2411) and Del Moral-Miclo (2000) for the CLT and variance formula (2.3); Del Moral (2004), Del Moral-Doucet-Jasra (2006) for the standard SMC-sampler framework and unbiased normalising-constant estimation (Prop 5).
