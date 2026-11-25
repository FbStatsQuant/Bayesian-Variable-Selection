# THEORY note: Lee and Santana-Gijzen (2024), convergence bounds for SMC on multimodal distributions using soft decomposition

Reader: Claude (Sonnet 5.5), 2026-11-24. Private to this machine. Page numbers are PDF pages of the local file. "(my inference)" marks anything the paper does not state itself; "(from memory, not checked)" marks facts from outside the paper.

## 0. Bibliographic and file caveat
- Title: Convergence bounds for Sequential Monte Carlo on multimodal distributions using soft decomposition. Authors: Holden Lee and Matheau Santana-Gijzen (Johns Hopkins). arXiv:2405.19553v2 [math.ST], dated 17 Mar 2026 on p.1 (the stamp says v2). I did not find a journal reference in the paper; treat as an arXiv preprint. Version caveat: later versions may change constants and numbering.
- Local file: `/home/fb31/SMC_Theory_Department/SMC_LIT/papers/LeeSantanaGijzen2024_SMC_soft_decomposition.pdf`, 33 pages, all read as images. Note on the file name: it says 2024 (v1), but the file is v2 (2026).
- The paper builds directly on Schweizer's non-asymptotic framework (its refs [24] = Schweizer 2012 multimodal, [25] = Schweizer's thesis) and states its main theorem as "analogous to the main result in [25]". See `THEORY_Schweizer2012.md`.
- Internal inconsistencies found while reading (flagged, not fixed): (a) Assumption 1(4) uses $\mathrm{Ent}\le c_{ki}\mathcal E_{ki}$ but Lemma 29 uses $\mathrm{Ent}\le2c_k\mathcal E$, so a factor 2 in the LSI constant is unreconciled; (b) Lemma 27 says "assume all assumptions from Lemma 3", but no Lemma 3 exists in the text; (c) the exponents of $\gamma$ and $w^*$ in the statement of Theorem 30 do not match Corollary 22 / Lemma 29 ($\gamma^{(2p-1)/p}\theta(p,p/2)$ with $\theta(p,p/2)=(1/w^*)^{1/p}$ versus the printed $\gamma^{(2p-1)/2p}(1/w^*)^{1/2p}$), and the printed lower bound on $N$ lacks the factor $2$ that the proof's last display produces; (d) on p.3, $\nu(f):=\varphi_k\nu_k^N(f)$ is a typo for $\nu_k^N(f)=\varphi_k\eta_k^N(f)$, and $\varphi_k=\prod\eta_j^N(g_{j,j+1})$ is written with the unnormalised ratio (Schweizer uses the normalised $q_{j,j+1}(1)$). Hence quote numerical constants only from Theorem 3 / Corollary 5 with this caveat and prefer to cite the structure of the result.

## 1. Coverage log
| PDF pages | Content |
|---|---|
| 1-2 | Abstract, 1 Introduction, 1.1 overview and Algorithm 1 |
| 3-4 | 1.2 notation (Schweizer's), 1.3 discrete versus continuous-time generators, 1.4 organisation |
| 5-7 | 2 Main result: Assumption 1, Remark 2, Theorem 3, Corollary 4 (high probability), Corollary 5 (total variation) |
| 7-11 | 3 Applications: 3.1 Markov-process decompositions: Prop 6 (Langevin), Prop 7 (Glauber on $\{0,1\}^d$), Prop 8 (Metropolis-Hastings); 3.2.1 Gaussian mixtures with power tempering: Prop 9, Cor 10 |
| 13-16 | 3.2.2 Gaussian convolution and noise contrastive estimation: Props 11, 12, Lemma 13, Prop 14, Remark 15; 3.2.3 TRE |
| 16-17 | 3.3 Initialization and discretization |
| 17-19 | 4 Overview of proof; 5 non-asymptotic variance bounds: Lemma 16, Theorem 17 (from Schweizer), Lemmas 18-20 |
| 19-22 | Lemma 21, Corollary 22 |
| 22-26 | 6 Log-Sobolev bounds and local smoothing: Lemmas 23, 24, Cor 25, Lemma 26 |
| 25-26 | 7 Local mixing time improvements: Lemma 27, Cor 28 |
| 26-30 | 8 Hypercontractivity: Lemma 29 and proof |
| 30-31 | 9 Proof of main result: Theorem 30 (complete MSE bound), proof of Theorem 3 |
| 32-33 | References (28 items) |
All 33 pages read.

## 2. Setting
- State space: general (Polish) $\Omega$; "work for any Markov process whose generator decomposes over components" (p.5); continuous or discrete. Applications: $\mathbb R^d$ (Langevin, Gaussian mixtures) and one discrete example, Glauber dynamics on $\{0,1\}^d$ (Prop 7, p.9), for which ONLY the decomposition inequality (Assumption 1(3)) is verified. No LSI/Poincare constant is computed on the hypercube.
- Target: $\mu_n=\mu$ with density $\propto e^{-V}$. At each level $\mu_k=\sum_{i=1}^{M_k}w_k^{(i)}\mu_k^{(i)}$ (soft decomposition; the decomposition exists but is not known to the algorithm; the number of components may change with $k$; no relation between components at different levels is assumed, Remark 2).
- Algorithm 1 (p.2): $N$ particles from $\mu_1$; for $k=1..n-1$: multinomial resampling with normalised weights $\bar g_{k,k+1}=d\mu_{k+1}/d\mu_k$, then a Markov kernel $P_{k+1}$ (a continuous-time semigroup $P^{t_k}$ with generator $\mathcal L_k$, stationary law $\mu_k$; discrete chains are handled via $P_t=e^{t(P-I)}$, p.4, so $t_k$ counts Poisson-clock time not steps). Resampling at every step; bridge and run lengths deterministic.
- Bridge: arbitrary in the theory. Concrete bridges: power tempering $\pi_i\propto\pi^{\beta_i}$ for Gaussian mixtures (Prop 9) and Gaussian convolution $\mu_k=\mu_n*\varphi_k$ (Prop 12). Adaptivity: none.
- Test functions: bounded $f$; MSE $\mathbb E[(\eta^N_n(f)-\mu_n(f))^2]\le\epsilon$; corollaries give high-probability bound (Chebyshev) and total variation bound of the particle marginal.

## 3. Main theorems (faithful statements)

**Assumption 1 (p.5).** SMC is run with $\mu_1,\dots,\mu_n$ and kernels $P_k=P_k^{t_k}$ ($P_k^t$ the semigroup of $\mathcal L_k$, stationary law $\mu_k$, Dirichlet form $\mathcal E_k(f,f)=-\langle f,\mathcal L_kf\rangle_{\mu_k}$). At every level $k$:
1. $\mu_k=\sum_{i=1}^{M_k}w_k^{(i)}\mu_k^{(i)}$, $w_k^{(i)}>0$, $\sum_iw_k^{(i)}=1$;
2. $\frac{d\mu_k}{d\mu_{k-1}}\le\gamma$ almost everywhere, for all $k$ (uniform upper bound on density ratios);
3. $\langle f,\mathcal L_kf\rangle_{\mu_k}\le\sum_{i=1}^{M_k}w_k^{(i)}\langle f,\mathcal L_{ki}f\rangle_{\mu_k^{(i)}}$ where $\mathcal L_{ki}$ generates a Markov process $P_{ki}$ with stationary law $\mu_k^{(i)}$ (the Dirichlet form of the full chain dominates the mixture of component Dirichlet forms);
4. each $\mu_k^{(i)}$ satisfies a log-Sobolev inequality $\mathrm{Ent}_{\mu_k^{(i)}}[f^2]\le c_{ki}\,\mathcal E_{ki}(f,f)$; $C_k^*=\max_ic_{ki}$.

**Theorem 3 (MSE bound, p.6).** Under Assumption 1, for every $\epsilon>0$, with $M=\max_kM_k$ and $w^*=\min_{k,i}w_k^{(i)}$, choosing
$$N\ge n\cdot\max\Big\{\frac{4\gamma M}{w^*\epsilon}\big(1+3\|f-\mu_n(f)\|_{\sup}^2\big),\ \frac{128\,\gamma^{35/8}M^{7/4}}{(w^*)^{15/8}}\Big\},\qquad t_k\ge2C_k^*\gamma^7,$$
yields $\mathbb E[(\eta_n^N(f)-\mu_n(f))^2]\le\epsilon$. (Proof in Section 9, via Theorem 30.)

**Theorem 30 (complete MSE bound, p.30).** Let $0<\alpha<\gamma^{-(2p-2)}$, $\beta=1+\max_{k}\sum_{i\le M_k}1/w_k^{(i)}$, $p=2^k$, $\delta(2p)=\delta(p)\big(\beta\gamma^{2p-2}/(1-\alpha\gamma^{2p-2})\big)^{1/2p}$, $\delta(1)=1$. Then
$$N\ge\max\Big\{\frac n\epsilon\frac{\gamma\beta}{1-\alpha}\big(1+\|f\|_{L^p(\mu_n)}^2+2\|f-\mu_n(f)\|_{\sup}^2\big),\ 2n(3+\gamma)\gamma^{\frac{2p-1}{2p}}\delta(2p)^2(w^*)^{-1/2p}\Big\},\quad t_k\ge\frac{C_k^*}2\max\Big\{\frac\gamma\alpha,\log\frac{p-1}{p/2-1}\Big\}$$
give $\mathbb E[(\eta_n^N(f)-\mu_n(f))^2]\le\epsilon$ (constants as printed; see the caveat in Section 0). Theorem 3 follows by taking $p=4$, $\alpha=1/(2\gamma^6)$ and $\beta\le2\max_kM_k/w^*$.

**Corollary 4 (high probability, p.6).** Same assumptions, with $\epsilon^2\delta$ in place of $\epsilon$: $N\ge n\max\{\frac{4\gamma M}{w^*\epsilon^2\delta}(1+3\|f-\mu_n(f)\|^2_{\sup}),\frac{128\gamma^{35/8}M^{7/4}}{(w^*)^{15/8}}\}$ and $t_k\ge2C_k^*\gamma^7$ give $|\frac1N\sum_if(\xi_n^{(i)})-\mu_n(f)|\le\epsilon$ with probability at least $1-\delta$ (proof by Chebyshev).

**Corollary 5 (total variation, p.7).** For the marginal law $\hat\mu_n$ of a particle: $N\ge n\max\{\frac{16\gamma M}{w^*\epsilon^2},\frac{128\gamma^{35/8}M^{7/4}}{(w^*)^{15/8}}\}$, $t_k\ge2C_k^*\gamma^7$ give $\|\hat\mu_n-\mu_n\|_{\mathrm{TV}}\le\epsilon$ (by Theorem 3 with $f=\mathbf 1_A$, uniformly in $A$).

**Proposition 6 (Langevin, p.8), Proposition 7 (Glauber on the hypercube, p.9; Prop 8 Metropolis-Hastings, p.10).** For $\mathcal L=P-I$ and a mixture target $p=\sum_kw_kp_k$:
$$\langle f,\mathcal Lf\rangle_p\le\sum_kw_k\langle f,\mathcal L_kf\rangle_{p_k},$$
for (i) Langevin with equality, (ii) Glauber dynamics on $\Omega=\{0,1\}^d$ (pick a uniform coordinate $i$, resample $x_i$ from its full conditional), with the Dirichlet-form inequality derived through Chebyshev's sum inequality, (iii) Metropolis-Hastings with proposal $P$. These verify Assumption 1(3) only.

**Proposition 9 (Gaussian mixtures with power tempering, p.11).** $\pi=\sum_{k\le M}\alpha_kq(\cdot;\mu_k,\Sigma_k)$, $0<\beta_1<\dots<\beta_n=1$, $\pi_i\propto\pi^{\beta_i}$. Then (1) density ratio bound $\gamma_i=\frac1{\min_k\alpha_k}\big(\frac{\beta_i}{\beta_{i-1}}\big)^{d/2}\big(\frac{\max_k|\Sigma_k|}{\min_k|\Sigma_k|}\big)^{\Delta\beta/2}$; (2) local LSI $C_{\mathrm{LSI}}(\nu_k^{(i)})\le\frac1{\min_j\alpha_j}\frac{\lambda_{\max}(\Sigma_k)}{\beta_i}$; (3) $\min_{i,k}w_k^{(i)}\ge\min_k\alpha_k^2$ when all $\Sigma_j$ are equal. **Corollary 10 (p.13; equal covariances $\Sigma$).** TV error $\epsilon$ for the power-tempered Gaussian mixture is reached for
$$N\ge n\max\Big\{\frac{16}{\epsilon^2\min_k\alpha_k^{a}}\max_i\Big(\frac{\beta_i}{\beta_{i-1}}\Big)^{d/2},\ \frac{128M^{7/4}}{\min_k\alpha_k^{b}}\max_i\Big(\frac{\beta_i}{\beta_{i-1}}\Big)^{35d/16}\Big\},\qquad t_k\ge\frac{2C_k^*}{\min_k\alpha_k^{c}}\max_i\Big(\frac{\beta_i}{\beta_{i-1}}\Big)^{7d/2},$$
where $a,b,c$ are positive powers whose digits are too small to read reliably in my rendering of p.13 (they come from $w^*\ge\min_k\alpha_k^2$ and $\gamma_i\propto1/\min_k\alpha_k$); "choosing $\beta_i/\beta_{i-1}=1+O(1/d)$ makes this polynomial in all parameters". Note the explicit $1/\min_k\alpha_k$ dependence: component weights of the TARGET enter polynomially.

**Propositions 11, 12, 14 (Gaussian convolution and TRE, pp.14-16).** For $\mu_k=\mu_n*\varphi_k$, $\varphi_k\propto e^{-\beta_k\|x\|^2/2\sigma^2}$: density ratio $\le\gamma=(\beta_k/\beta_{k-1})^{d/2}$; with $\mu_n=\sum_iw_i\mu_n^{(i)}$ and $C^*=\max_iC_{\mathrm{LSI}}(\mu_n^{(i)})$ (Lemma 13: LSI constants add under convolution), TV error $\epsilon$ is reached for $N\ge n\max\{16\gamma M/(w^*\epsilon^2),128\gamma^{35/8}M^{7/4}/(w^*)^{15/8}\}$ and $t_k\ge2(C^*+\sigma^2/\beta_k)\gamma^7$.

**Lemma 16 and Theorem 17 (p.18; Schweizer's Lemma 2.2 and Theorem 2.1 of the thesis).** $\mathbb E[(\eta^N_n(f)-\mu_n(f))^2]\le2\mathrm{Var}(\nu_n^N(f))+2\|f-\mu_n(f)\|^2_{\sup}\mathrm{Var}(\nu_n^N(1))$ and for $N\ge2\bar c_n$: $\mathrm{Var}(\nu_n^N(f))\le\frac1N\big(\sum_j\mathrm{Var}_{\mu_j}(q_{j,n}f)+2\bar v_n\|f\|^2_{L_p(\mu_n)}\hat c_n/N\big)\le\frac1N(\bar v_n+2\bar v_n\|f\|^2\hat c_n/N)$.

**Lemmas 18-22 and Corollary 22 (pp.19-22; Schweizer's Lemmas 3.2-3.4 adapted to allow $\beta\ge1$).** With the one-step bound (12) $\|\hat q_{k-1,k}f\|^2_{L_2(\mu_{k-1})}\le\alpha\|f\|^2_{L_2(\mu_k)}+\beta\mu_k(f)^2$, $\alpha<1$, $\beta\ge1$: $\|\hat q_{j,k}f\|_{L_2(\mu_j)}\le(\beta/(1-\alpha))^{1/2}\|f\|_{L_2(\mu_k)}$; $L_{2p}$ extension with $\delta(2p)$; $\hat c_n\le n(3+\gamma)\gamma^{(2p-1)/p}\delta(2p)^2\theta(p,p/2)$ and $\bar v_n\le n\gamma\beta/(1-\alpha)$.

**Lemma 24 (intra-mode variance decay, p.23; main technical novelty 1).** If $\langle f,\mathcal Lf\rangle_\pi\le\sum_kw_k\langle f,\mathcal L_kf\rangle_{\pi_k}$ and each $\pi_k$ has Poincare constant $C_k$, $C^*=\max_kC_k$, then $\sum_kw_k\mathrm{Var}_{\pi_k}(P_Tf)\le\frac{C^*}{2T}\mathrm{Var}_\pi(f)$. Corollary 25: $\sum_iw_{k-1}^{(i)}\mathrm{Var}_{\mu^{(i)}_{k-1}}(\hat q_{k-1,k}f)\le\frac{C^*_{k-1}\gamma}{2T}\mu_k(f^2)$.

**Lemma 26 (inter-mode variance, p.24).** $\sum_iw_{k-1}^{(i)}\big(\mu_{k-1}^{(i)}(P^{t}(\bar g_{k-1,k}f))-\mu_{k-1}(\bar g_{k-1,k}f)\big)^2\le\sum_i\frac1{w_i}\mu_k(f)^2$. This is where the minimum weight enters: there is no mixing between modes assumed, so the between-mode term is only controlled by the mass of the smallest component.

**Lemma 27 and Corollary 28 (p.25-26).** For $f\ge0$: $\|\hat q_{k-1,k}f\|^2_{L_2(\mu_{k-1})}\le\lambda_{k-1}\|f\|^2_{L_2(\mu_k)}+\beta_{k-1}\mu_k(f)^2$ with $\lambda_{k-1}=C^*_{k-1}\gamma/(2t_{k-1})$ and $\beta_{k-1}=1+\sum_i1/w_{k-1}^{(i)}$; if $t_k\ge C_k^*\gamma/(2\alpha)$ then $\lambda_k\le\alpha$.

**Lemma 29 (mixture hypercontractivity, p.27; main technical novelty 2).** For reversible $P_t$ with stationary $\pi=\sum_kw_k\pi_k$, generator decomposition (Assumption 1(3)) and component LSI, $q(t)=1+(p-1)e^{2t/C^*}$: $\|P_tf\|_{L^{q(t)}(\pi)}/(w^*)^{1/q(t)}$ is non-increasing, hence $\|P_tf\|_{L^{q(t)}(\pi)}\le(1/w^*)^{1/p-1/q(t)}\|f\|_{L^p(\pi)}$. (For $f>0$; uses the entropy decomposition for mixtures and Chebyshev-type arguments.)

## 4. Does any result cover (i)-(v)?
| Item | Answer |
|---|---|
| (i) $\{0,1\}^p$ | Partly. The framework is general, and the hypercube appears explicitly in Prop 7 (Glauber dynamics for a mixture target on $\{0,1\}^d$), but only to verify the generator decomposition (Assumption 1(3)). No LSI constant, no density-ratio bound, no mixture structure and no sample-complexity statement is worked out for any hypercube target. Everything quantitative (Props 9, 12, 14, Cors 10) is on $\mathbb R^d$ |
| (ii) BVS / spike-and-slab | No. No statistical model, no posterior consistency; targets are abstract mixtures. No discrete example with a uniform $w^*$ |
| (iii) adaptive tempering | No. Deterministic temperature ladders ($\beta_i$ fixed in advance) |
| (iv) frozen schedules | Yes in the trivial sense: all results are for a pre-specified schedule and fixed $t_k$ |
| (v) evidence estimation | No. Only $\mathbb E[(\eta_n^N(f)-\mu_n(f))^2]$ for the self-normalised estimator (and TV). Unbiasedness of $\nu_n^N$ and $\mathrm{Var}(\nu^N_n(1))$ appear only as inherited steps (Lemma 16, Theorem 17); no theorem about $\hat Z$ |

## 5. Observations (my inference)
1. The complexity is polynomial in $1/w^*$ ($w^*$ = smallest component weight over ALL levels and components, including the start law $\mu_1$), in $\gamma$ ($\gamma^{35/8}$ and $t_k\gtrsim\gamma^7$), in $M^{7/4}$, in the local LSI constant $C^*$, and linear in the number of levels $n$. The dependence on the smallest weight is the same mode-mass phenomenon as in Schweizer (Part B) and Mathews-Schmidler ($\mu_*$), here made polynomial instead of exponential because inter-mode mass bottlenecks are absorbed into $1/w^*$.
2. For a consistent BVS posterior with competing local modes whose posterior mass vanishes in $n$ (and with a start law that places little mass near them or near the truth), $w^*$ is exponentially small in the relevant size parameters, so the bound is vacuous in the regime of interest. Equivalent in our language: Assumption 1(1) forces EVERY component to carry weight at least $w^*$ at EVERY level, including the start; Thm 3 does not need that (it only needs visibility of the truth-containing region). This is my inference; the paper does not discuss BVS.
3. Both the decomposition (Assumption 1(1,4)) and the per-component LSI are unverifiable for a BVS posterior on $\{0,1\}^p$ without further work: the paper offers no way to produce a spike-and-slab mixture decomposition with local LSI constants and no bound on $\gamma$ for a geometric tempering of a BVS posterior (Prop 9 handles Gaussian mixtures only; for tempering a discrete BVS likelihood the density-ratio bound $\gamma$ is controlled instead by the increment of $\beta$ and the range of the log-likelihood).
4. Prop 7 shows that single-site Glauber dynamics (the same move class as single-flip chains) satisfies the soft-decomposition inequality on $\{0,1\}^d$ for ANY mixture target. So a theorem of this type would apply to SMC with a single-flip kernel on a trap family provided the components satisfy the LSI with polynomial constants and $w^*$, $\gamma$ are polynomial. This is the structure P1 must negate or avoid: P1's family must be one where our consistency theorem holds without those hypotheses, and where one of them fails for the single-flip chain (for example an exponentially small component weight at some level, or exponentially large local LSI constants); (my inference).
5. They handle Markov chains in continuous time; for a discrete chain $P$ they run $P_t=e^{t(P-I)}$ (p.4). A statement about "number of steps $t_k$" translates to expected Poisson counts, not to the number of single-flip sweeps. Do not quote step counts from this paper for our moves.

## 6. Relation to us

**Prop 5 (unbiased evidence conditional on the frozen calibration).** NO overlap. The unbiasedness of $\nu_n^N$ is quoted as a black box from Schweizer (Lemma 16, Theorem 17); no evidence theorem, no adaptive calibration. Cite Schweizer 2012a Prop 2.3 and Del Moral-Miclo (2000) rather than this paper. Verdict: none.

**Theorem 3 (every run reports the truth on high-probability data events).** The closest statement here is Corollary 5 (TV bound for the particle marginal) combined with posterior concentration: a TV bound of $\epsilon$ plus Theorem 1 (posterior concentration on $S_0$) would give that a single particle returns $S_0$ with probability at least $1-\epsilon-(\text{posterior miss})$. This is an alternative route to a Thm-3-style conclusion, and in that sense it COMPETES in scope (a generic route that includes Glauber on $\{0,1\}^d$ and does not need any kernel to leave a partition element, unlike Schweizer/Paulin et al.). It does not cover: (a) a frozen adaptively-calibrated schedule, (b) our actual kernel set (Gibbs, swap, independence, islands), (c) PIP/list-renormalised estimators, (d) high-probability statements over all $N$ particles/runs (it gives MSE and Chebyshev: probability bounds that depend polynomially on $1/\delta$ and on $1/\epsilon^2$), (e) any regime where $w^*$ is exponentially small, which is exactly the BVS regime with sparse truth and vanishing competing modes (Observation 2). Our visibility/leakage assumption is a one-sided and data-dependent substitute for "$w^*\ge$ inverse polynomial at all levels". Verdict: competes only in a generic "SMC works on multimodal discrete targets with local Glauber mixing" sense; does not cover our regime and does not replace Thm 3.

**P1 (trap theorem).** Not a lower bound; it is a positive upper bound for SMC. It SUPPORTS P1 only in a loose way: it shows that single-site Glauber is compatible with SMC success when the target is a mixture whose components mix locally and have non-negligible weights. It does not say anything about the mixing time of single-flip MCMC (Glauber) on the whole mixture, nor about Zanella-Roberts weighted tempered Gibbs. The citation use is as the closest "positive" generic theorem against which the P1 family is designed: the P1 construction should state explicitly which of $w^*$, $\gamma$, $C^*$ fails or is polynomial in order not to contradict this paper.

**Verdict:** supports (as context for P1; positive generic theorem for SMC with Glauber-type kernels); competes with Thm 3 only in scope, not in hypotheses; none for Prop 5.

## 7. Citations we should make
1. H. Lee and M. Santana-Gijzen (2024/2026), Convergence bounds for Sequential Monte Carlo on multimodal distributions using soft decomposition, arXiv:2405.19553 - for the soft-decomposition framework, Prop 7 (Glauber on $\{0,1\}^d$), Theorem 3 / Corollary 5 and the explicit $1/w^*$ dependence, as the generic upper bound that our Thm 3 does not need.
2. N. Schweizer (2012), arXiv:1204.2382 (Prop 2.3, Theorem 3.2) and arXiv:1205.6733 (Prop 3.2, Prop 4.11); and Schweizer's 2011 Bonn thesis: the framework used here.
3. Ge, Lee and Risteski (2018, 2020), Simulated tempering Langevin Monte Carlo (I, II): the soft Markov chain decomposition that the paper imports (their refs [10], [11]); and Madras and Randall (2002), Markov chain decomposition.
4. Mathews and Schmidler (2024) (see `THEORY_MathewsSchmidler2024.md`) and Paulin, Jasra and Thiery (2019): the predecessors that require no or restricted movement between modes (cited by the authors as [19], [22]).
5. Woodard, Schmidler and Huber (2009a, 2009b): rapid and torpid mixing of parallel and simulated tempering (the comparison class used in Remark 2 and in the Introduction).
