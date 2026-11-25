# THEORY note: Schweizer (2012), two arXiv papers on non-asymptotic error bounds for sequential MCMC

Reader: Claude (Sonnet 5.5), 2026-11-24. Private to this machine. Page numbers are PDF pages of the local files. "(my inference)" marks anything the paper does not state itself; "(from memory, not checked)" marks facts from outside the paper.

This file covers TWO papers by the same author. Part A is the generic non-asymptotic bound under GLOBAL mixing (and contains the unbiasedness/variance proposition that is the standard citation for our Prop 5). Part B is the multimodal follow-up (trees, local mixing, resampling versus weighting).

## 0. Bibliographic and file caveat
- Part A: N. Schweizer, "Non-asymptotic error bounds for sequential MCMC and stability of Feynman-Kac propagators", arXiv:1204.2382v1 [math.PR], 11 Apr 2012 (dated March 2012). Local file `/home/fb31/SMC_Theory_Department/SMC_LIT/papers/Schweizer2012_nonasymptotic_SMC_Feynman-Kac.pdf`, 27 pages, all read as images. As far as I recall it stayed an arXiv preprint (from memory, not checked); extracted from the author's Bonn dissertation (2011).
- Part B: N. Schweizer, "Non-asymptotic error bounds for sequential MCMC methods in multimodal settings", arXiv:1205.6733v1 [math.PR], 30 May 2012 (dated March 2012). Local file `/home/fb31/SMC_Theory_Department/SMC_LIT/papers/Schweizer2012_SMC_multimodal.pdf`, 36 pages, all read as images. Preprint; the multimodal paper is the "follow-up [21]" announced in Part A (p.3).
- Cite as arXiv preprints (or the Bonn thesis, Univ. of Bonn 2011). Numbering below is that of the local files.

## 1. Coverage log

### Part A (27 pp.)
| PDF pages | Content |
|---|---|
| 1-3 | Abstract, 1 Introduction (literature, comparison with Whiteley 2011, Eberle-Marinelli) |
| 3-5 | 2.1 notation, 2.2 measure-valued model ($g_{k-1,k},K_k,q_{j,k}$), 2.3 particle system (algorithm) |
| 5-10 | Lemma 2.1, 2.4 variance of weighted averages, Lemma 2.2, **Proposition 2.3**, Lemmas 2.4-2.5 and proof |
| 11-12 | 3 Non-asymptotic bounds: Assumption A, Prop 3.1, **Theorem 3.2** |
| 12-19 | 4 $L_p$-stability: 4.1 setting, Lemma 4.1; 4.2 Assumptions B, C, Lemmas 4.2-4.4, Thm 4.5, Cor 4.6, 4.7, Lemma 4.8, Cor 4.9, Prop 4.10 |
| 20-25 | 5 Poincare / log-Sobolev: Assumption D, Lemmas 5.1-5.2, Cor 5.3; 5.2 Assumption E, Prop 5.4, Cor 5.5, 5.6, numerical illustration, proofs |
| 25-26 | 6 Dimension dependence ($O(d^3)$ for product measures) |
| 26-27 | References (22 items) |
All 27 pages read.

### Part B (36 pp.)
| PDF pages | Content |
|---|---|
| 1-4 | Abstract, 1 Introduction |
| 4-9 | 2 Preliminaries: 2.1-2.3 setting and algorithm, 2.4 Lemma 2.1, Theorem 2.2 (from Part A), Theorem 2.3 (new) |
| 9-13 | 3 Sequential MCMC on trees: 3.1 model, Lemma 3.1, 3.2 Prop 3.2, Prop 3.3 |
| 13-14 | 3.3 Sequential importance sampling (SIS), Lemma 3.4 |
| 14-23 | 3.4 Example "weighting or resampling": 3.4.1 model (Fig 1, Cor 3.5), 3.4.2 Lemmas 3.6-3.7, Cor 3.8, 3.4.3 Props 3.9, 3.11, Cor 3.10, Lemma 3.12, 3.4.4 Cor 3.13 (SIS degeneracy), 3.4.5 further examples |
| 23-33 | 4 $L_p$ bounds under local mixing: 4.1 model, Assumption A; Prop 4.1 (p.24); 4.2 Assumption B, C, D, Lemmas 4.2-4.6, Prop 4.7, Cor 4.8, 4.9, Lemma 4.10, **Prop 4.11** (p.32) |
| 33-35 | 5 Outlook (Potts, Ising, mixtures, SMC vs tempering) |
| 35-36 | References (30 items) |
All 36 pages read.

## 2. Setting (both parts)
- State space: Polish space (complete separable metric space) $E$ (Part A allows a sequence $E_k$). Part B Section 3 uses FINITE trees $I_0,\dots,I_n$; Section 4 uses a common $E$ with increasingly fine partitions. Nothing is specific to $\{0,1\}^p$; a finite space is covered as a special case (finite $E$ is Polish).
- Target and bridge: $\mu_0,\dots,\mu_n=\mu$ with $\mu_k(f)=\mu_{k-1}(g_{k-1,k}K_k f)/\mu_{k-1}(g_{k-1,k})$ for positive bounded (UNNORMALISED) relative densities $g_{k-1,k}$ and kernels $K_k$ (Part A p.4). In the main application $K_k$ is $\mu_k$-invariant and $g_{k-1,k}\propto d\mu_k/d\mu_{k-1}$. The bridge is ARBITRARY in the theory; tempering $\mu_k\propto e^{-\beta_kH}\pi$ is only the motivating example (p.3 Part A; p.1 Part B).
- Algorithm (Part A p.5): $N$ iid draws from $\mu_0$; for $k=1,\dots,n$: (a) multinomial resampling with weights $g_{k-1,k}(\xi_{k-1}^i)$, (b) independent mutation by $K_k$. Resampling at EVERY step, deterministic bridge and deterministic number of MCMC steps. $\eta_n^N$ = empirical measure; weighted measure $\nu_k^N=\varphi_k\eta_k^N$, $\varphi_k=\prod_{j<k}\eta_j^N(q_{j,j+1}(1))$, $q_{j,j+1}(1)=g_{j,j+1}/\mu_j(g_{j,j+1})$, so $\varphi_k$ is the product of the empirical mean incremental weights DIVIDED by their true means, i.e. $\hat Z_k/Z_k$ (my inference from the definitions).
- Adaptivity: NONE. The bridge $(\mu_k)$, the $g$'s and the kernels $K_k$ are fixed and deterministic. Adaptive tempering is not mentioned in either paper.
- Test functions: bounded measurable $f\in B(E)$ throughout (Part A p.10: "the results on the weighted particle measures do not rely on boundedness").
- Error criterion: mean squared error $\mathbb E|\eta_n^N(f)-\mu_n(f)|^2$, bounded at finite $N$ (non-asymptotic), with leading coefficient equal to the CLT asymptotic variance of Del Moral and Miclo (Part A p.3; Part B p.9).

## 3. Main theorems (faithful statements)

### Part A

**Lemma 2.1 (p.6).** With $\mathcal F_{k-1}=\sigma(\xi_0,\hat\xi_1,\xi_1,\dots,\xi_{k-1})$: $\mathbb E[\eta_k^N(f)\mid\mathcal F_{k-1}]=\eta_{k-1}^N(q_{k-1,k}f)/\eta_{k-1}^N(q_{k-1,k}(1))$, and the same for a single particle. Consequently $\mathbb E[\nu_k^N(f)\mid\mathcal F_{k-1}]=\nu_{k-1}^N(q_{k-1,k}f)$ (eq. (1)), and $\nu_{k+1}^N(1)=\varphi_{k+1}=\nu_k^N(q_{k,k+1}(1))$ (eq. (2)).

**Lemma 2.2 (p.7).** For $f_n=f-\mu_n(f)$:
$$\mathbb E\big[(\eta_n^N(f)-\mu_n(f))^2\big]\le 2\,\mathrm{Var}(\nu_n^N(f_n))+2\|f_n\|_{\sup}^2\,\mathrm{Var}(\nu_n^N(1)),$$
and an analogous $L^1$ bound (eq. (4)).

**Proposition 2.3 (p.7; unbiasedness and exact finite-$N$ variance; attributed to Del Moral and Miclo 2000, Section 2, "stated and proved for completeness").** For all $f\in B(E_n)$,
$$\mathbb E[\nu_n^N(f)]=\mu_n(f),\qquad \mathbb E\big[|\nu_n^N(f)-\mu_n(f)|^2\big]=\frac1N\mathrm{Var}_{\mu_n}(f)+\frac1N\mathbb E\Big[\sum_{j=0}^{n-1}V^N_{j,n}(f)\Big],$$
$$V^N_{j,n}(f)=\nu_j^N(1)\,\nu_j^N(q_{j,n}(f)^2)-\nu_j^N(q_{j,n}(f))^2+\big(\nu_j^N(q_{j,j+1}(1))-1\big)\,\nu_j^N(q_{j,n}(f^2)).$$
In particular (with $f\equiv1$) $\mathbb E[\varphi_n]=\mathbb E[\nu_n^N(1)]=1$ (p.6, p.7). Proof (pp.8-10): $A_j=\nu_j^N(q_{j,n}(f))$ is an $(\mathcal F_j)$-martingale by (1) and the semigroup property; the quadratic variation is computed in Lemma 2.4; Lemma 2.5 gives two further martingales.

**Assumption A (p.11).** There are constants $c_{j,k}$ with, for all $f\in B(E_k)$, $\max\big(\|1\|_j\|q_{j,k}(f)^2\|_j,\ \|q_{j,k}(f)\|_j^2,\ \|q_{j,k}(f^2)\|_j\big)\le c_{j,k}\|f\|_k^2$, for norms $\|\cdot\|_j$ on $B(E_j)$.

**Proposition 3.1 (p.11).** $\mathbb E[V^N_{j,n}(f)]\le V_{j,n}(f)+c_{j,n}\|f\|_n^2(2+\|q_{j,j+1}(1)-1\|_j)\,\varepsilon_j^N$ with $V_{j,n}(f)=\mathrm{Var}_{\mu_j}(q_{j,n}(f))$, $\varepsilon_j^N=\sup\{\mathbb E|\nu_j^N(f)-\mu_j(f)|^2:\|f\|_j\le1\}$.

**Theorem 3.2 (p.12).** Define $\hat c_k=\sum_{j<k}c_{j,k}(2+\|q_{j,j+1}(1)-1\|_j)$, $\hat v_k=\sup\{\sum_{j\le k}\mathrm{Var}_{\mu_j}(q_{j,k}(f)):\|f\|_k\le1\}$, $\bar c_k=\max_{j\le k}\hat c_j$, $\bar v_k=\max_{j\le k}\hat v_j$, $\bar\varepsilon_k^N=\max_{j\le k}\varepsilon_j^N$. Then for all $f\in B(E_n)$
$$N\,\mathbb E\big[|\nu_n^N(f)-\mu_n(f)|^2\big]\le\sum_{j=0}^n\mathrm{Var}_{\mu_j}(q_{j,n}(f))+\|f\|_n^2\,\hat c_n\,\bar\varepsilon_n^N,\qquad\text{and if }N\ge2\bar c_n:\ \bar\varepsilon_n^N\le 2\bar v_n/N.$$

**Setting for Section 4 (p.13).** Common $E$; $K_k$ stationary for $\mu_k$ (so $\hat\mu_k=\mu_k$); $\bar g_{k-1,k}=g_{k-1,k}/\mu_{k-1}(g_{k-1,k})$.

**Assumption B (p.14).** There is $\gamma>1$ with $\bar g_{k-1,k}(x)\le\gamma$ for all $x\in E$ and $1\le k\le n$ (uniform UPPER bound on normalised relative densities; no lower bound needed).

**Assumption C (p.15).** There are $\alpha\in(0,1)$, $\beta\in[0,1]$ with $\|\hat q_{k-1,k}(f)\|_{L_2(\mu_{k-1})}^2\le\alpha\|f\|_{L_2(\mu_k)}^2+\beta\mu_k(f)^2$ for all $f\in B(E)$, where $\hat q_{k-1,k}(f)=K_{k-1}(\bar g_{k-1,k}f)$.

**Theorem 4.5 (p.16).** For $p=2^r$ and $\alpha\gamma^{p-2}<1$, for $1\le j<k\le n$:
$$\|\hat q_{j,k}(f)\|_{L_p(\mu_j)}\le\delta(p)\|f\|_{L_p(\mu_k)},\qquad \delta(p)=\prod_{i=1}^r\frac{\gamma^{1-2^{-(i-1)}}}{(1-\alpha\gamma^{2^i-2})^{2^{-i}}}<\frac{\gamma^{r-2+2^{-(r-1)}}}{1-\alpha\gamma^{2^r-2}}.$$
Corollary 4.6 extends this to $p\in[2^r,2^{r+1}]$ by Riesz-Thorin. Corollary 4.7 / Lemma 4.8 / Corollary 4.9 (pp.17-18) give $L_p$-$L_q$ bounds for the true propagator, $\|q_{j,k}f\|_{L_p(\mu_j)}\le\tilde c_{j,k}(p,q)\|f\|_{L_q(\mu_k)}$ with $\tilde c_{j,k}(p,q)=\theta(p,q)\gamma^{(p-1)/p}\gamma^{(q-1)/q}\delta(q)$, under a hypercontractivity-type assumption $\|K_j f\|_{L_p(\mu_j)}\le\theta(p,q)\|f\|_{L_q(\mu_j)}$.

**Proposition 4.10 (p.18).** For $p=2^r\ge2$ with $\theta_p=\alpha\gamma^{p-2}<1$ and $\mu_k(f)=0$: $\|\hat q_{j,k}(f)\|^p_{L_p(\mu_j)}\le\lambda_p\theta_p^{k-j}\|f\|^p_{L_p(\mu_k)}$ (exponential decay in $k-j$), $\lambda_2=1$, $\lambda_{2p}=1+\lambda_p^2(\alpha(1-\alpha/\gamma^2))^{-1}$.

**Lemma 5.1 and 5.2 (pp.20-21).** If $\mathrm{Var}_{\mu_k}(K_kf)\le(1-\rho)\mathrm{Var}_{\mu_k}(f)$ (Assumption D) and Assumption B holds, then Assumption C holds with $\alpha=(1-\rho)\gamma$, $\beta=\rho$. A reversible kernel with Poincare constant $\lambda_k$ satisfies Assumption D with $\rho=\min_k(1-\lambda_k)^2$.

**Assumption E and Proposition 5.4 (p.22).** With $t_k$ MCMC steps in $K_k$: $\|K_k^{t_k}f\|_{L_{q(p,t_k)}(\mu_k)}\le\|f\|_{L_p(\mu_k)}$, $q(p,t)=1+(p-1)e^{2a_k^*t}$ (log-Sobolev), and $\|K_k^{t_k}f-\mu_k f\|_{L_2}\le e^{-2b_k^*t_k}\|f-\mu_kf\|_{L_2}$ (Poincare). If $t_l\ge\frac1{2b_l^*}[(p-1)\log\gamma-\log(1-\tau)]$ for $j\le l\le k$, then $\|q_{j,k}f\|_{L_p(\mu_j)}\le\frac{\gamma^{s-1+1/p}}{\tau}\|f\|_{L_p(\mu_k)}$ ($p=2^s$).

**Corollary 5.6 (p.23).** Under the conditions on $t_l$ of Cor 5.5, with $\tau\in(0,1)$, $p=2^s$:
$$N\,\mathbb E|\nu_n^N(f)-\mu_n(f)|^2\le\|f\|^2_{L_p(\mu_n)}\Big[1+n\gamma\tau^{-2}+n((1+\gamma)\vee3)\gamma^{2s+p^{-1}}\tau^{-2}\bar\varepsilon_n^{N,p}\Big],$$
and if $N\ge2((1+\gamma)\vee3)n\gamma^{2s+p^{-1}}\tau^{-2}$ then $\bar\varepsilon_n^{N,p}\le2(1+n\gamma\tau^{-2})/N$. Illustration (p.24): $\gamma=2,\tau=0.8,p=4$ gives $\mathbb E|\nu_n^N(f)-\mu_n(f)|^2\le\|f\|^2_{L_4(\mu_n)}[(1+4n)/N+(180n+560n^2)/N^2]$ for $N\ge180$. Result is LINEAR in the number $n$ of levels at leading order.

**Section 6 (pp.25-26).** For product measures on $\mathbb R^d$ with dimension-free log-Sobolev constants, the cost is $O(d^3)$ (one $d$ for the kernel cost, one for the number of levels, one for $N$).

### Part B

**Lemma 2.1 and Theorem 2.2 (pp.7-8).** Same as Part A Lemma 2.2 and Theorem 3.2 (restated).

**Theorem 2.3 (p.8; new).** Under the variant of Assumption A with constants $d_{j,k}$ for $0\le j\le k\le n$ (note: includes $j=k$), $\max(\|1\|_j\|q_{j,k}(f)^2\|_j,\|q_{j,k}(f)\|_j^2)\le d_{j,k}\|f\|_k^2$, define $\hat d_k=2\sum_{j\le k}d_{j,k}$, $\bar d_k=\max_{j\le k}\hat d_j$. Then
$$N\,\mathbb E|\nu_n^N(f)-\mu_n(f)|^2\le\sum_{j=0}^n\mathrm{Var}_{\mu_j}(q_{j,n}(f))+\|f\|_n^2\bar d_n\bar\varepsilon_n^N,\qquad N\ge2\bar d_n\Rightarrow\bar\varepsilon_n^N\le2\bar v_n/N.$$
The leading coefficient is the CLT asymptotic variance of Del Moral and Miclo (p.9).

**Tree model (pp.9-10).** Finite sets $I_k$, a predecessor map $p_k$, successor sets $s_k(x)$, no branch dies out; $\mu_k^{\to j}$ for $j<k$ is the projection of $\mu_k$ to $I_j$ ($\mu_k^{\to j}(x)=\mu_k(s_k(x))$); $g_{k,k+1}$ is the unnormalised relative density between $\mu_k$ and $\mu_{k+1}^{\to k}$; $K_{k+1}(x,y)=\mu_{k+1}(y)/\mu_{k+1}(s_{k+1}(x))$ for $y\in s_{k+1}(x)$, else $0$. Particles move between branches only through resampling.

**Lemma 3.1 (p.11).** For $x\in I_j$, $f\in B(I_k)$: $q_{j,k}(f)(x)=\mu_k(f\mathbf 1_{s_k(x)})/\mu_j(x)$.

**Proposition 3.2 (p.11).** With $\|\cdot\|_j=\max$-norm, the constants
$$d_{j,k}=\Big(\max_{x\in I_j}\frac{\mu_k^{\to j}(x)}{\mu_j(x)}\Big)^2$$
satisfy (16), $\mathrm{Var}_{\mu_j}(q_{j,k}(f))\le\sqrt{d_{j,k}}\|f\|_k^2$, $\hat v_k\le\sum_{j\le k}\sqrt{d_{j,k}}$. A sharper version uses $\tilde d_{j,k}=\sum_x\mu_k^{\to j}(x)^2/\mu_j(x)$ (p.13). Interpretation (p.12): $d_{j,k}$ is large when a node with small mass at level $j$ has offspring carrying much more mass at level $k$. It does NOT see later branching.

**Proposition 3.3 (p.12).** For the test function $1$, the asymptotic variance
$$\mathrm{Var}_k^{as}(1)=\sum_{j=0}^k\sum_{x\in I_j}\mu_k^{\to j}(x)\Big(\frac{\mu_k^{\to j}(x)}{\mu_j(x)}-1\Big)=\sum_{j=0}^k\mu_k^{\to j}(q_{j,k}(1)-1).$$
(This is the asymptotic variance of the evidence-type weight $\varphi_k$ on the tree; my inference from $\nu_k^N(1)=\varphi_k$.)

**Lemma 3.4 and SIS (pp.13-14).** The SIS estimator $\tilde\eta_n(f)=N^{-1}\sum f(\tilde\xi_n^i)\omega_n(\tilde\xi_n^i)$, $\omega_n=\mu_n/\pi_n$, $\pi_n=\mu_0K_1\cdots K_n$, is unbiased and for $f=\mathbf 1_{\{x\}}$: $\mathbb E|\tilde\eta_n(f)-\mu_n(f)|^2=\frac{\mu_n(x)^2}{N}\big(\frac1{\pi_n(x)}-1\big)$.

**Example (Figure 1, pp.14-22).** $I_k=\{0_k,\dots,k_k\}$, the largest node $k_k$ doubles at each level with weight $g_{k,k+1}(k_k)=2\theta$, others weight 1; $\mu_k$ geometric with $\mu_k(j_k)=\theta^{j+1}/Z_k$ ($j<k$), $\mu_k(k_k)=\theta^k/Z_k$ (Cor 3.5). Results:
- Prop 3.9: for $\theta>1$, $N>\rho(\theta)^4(n+1)$, $\rho(\theta)=2+1/(\theta-1)$:
$\mathbb E|\nu_n^N(f)-\mu_n(f)|^2\le\|f\|_n^2\big(\frac{\rho(\theta)^2}2\frac{n+1}N+\rho(\theta)^6\frac{(n+1)^2}{N^2}\big)$.
- Prop 3.11: for $\theta\ge1$, $N>(n+2)^5/16$: $\mathbb E|\nu_n^N(f)-\mu_n(f)|^2\le\|f\|_n^2\big(\frac18\frac{(n+2)^3}N+\frac1{128}\frac{(n+2)^8}{N^2}\big)$ (polynomial in $n$).
- Lemma 3.12: for $\theta=1$, $\mathrm{Var}_n^{as}(1)=n^2(n-1)/(12(n+1))$ (quadratic in $n$; the polynomial rate is real, not an artefact).
- Cor 3.13: for $f=\mathbf 1_{\{n_n\}}$, SIS error is $\frac{2^n-1}{N(1+\frac\theta{\theta-1}(1-\theta^{-n}))^2}$ ($\theta\ne1$), $\frac{2^n-1}{N(n+1)^2}$ ($\theta=1$), exponential in $n$ whenever $\theta>2^{-1/2}$. So resampling beats weighting on this tree (the paper's point).
- 3.4.5 (pp.21-22): a counter-pairing where SIS beats SMC (asymptotic variance $\frac14(1/\alpha+1)$ for SMC versus SIS error independent of $\alpha$); "for both algorithms it is easy to construct examples where they perform arbitrarily badly" (p.23).

**Part B Section 4 (local mixing; pp.23-33).**
- Setting: increasingly finer partitions $(F_j)_{j\in I_k}$ of $E$ ($F_i\subseteq F_{p_k(i)}$), $\mu_0(F_j)>0$.
- **Assumption A (p.23).** $K_k(\mathbf 1_{F_j})(x)=0$ for $x\notin F_j$, $j\in I_k$ (kernels never leave partition elements; "an approximation of the fact that particles move between modes only extremely rarely", and the author flags it is not literally true in applications, p.34).
- Norms $\|f\|_{k,p}=\max_{j\in I_k}\|f\|_{k,j,p}$, $\|f\|_{k,j,p}=\mu_{k,j}(|f|^p)^{1/p}$ with $\mu_{k,j}$ the restriction of $\mu_k$ to $F_j$.
- Mass-change constants: $m_{k,k+1}(j)=\mu_{k+1}(F_j)/\mu_k(F_j)$; $M_{j,k}(i)=\max_{l\in s_k(i)}\prod_{r=j}^{k-1}m_{r,r+1}(p_r(l))$; $A_{j,k}=\max_{i\in I_j}M_{j,k}(i)$.
- **Assumption B (p.25).** Uniform bound on RESTRICTED relative densities: $\bar g_{k,k+1,j}(x)=\frac{\mu_k(F_j)}{\mu_{k+1}(F_j)}\bar g_{k,k+1}(x)\le\gamma$ for $x\in F_j$ (i.e. relative-density variation WITHIN a mode is bounded by $\gamma$).
- **Assumption C (p.27).** Local contraction: $\|\hat q_{k,k+1}f\|^2_{k,i,2}\le m_{k,k+1}(i)^2(\alpha\|f\|^2_{k+1,i,2}+\beta\mu_{k+1,i}(f)^2)$ (follows from a local Poincare inequality, via $\rho$ with $\alpha=(1-\rho)\gamma,\beta=\rho$). **Assumption D (p.31):** local hypercontractivity $\|K_jf\|_{j,i,p}\le\theta_j(p,q)\|f\|_{j,i,q}$.
- **Proposition 4.1 (p.24).** For $p>2$, $c_{j,k}(p)=\max(\tilde c_{j,k}(p,p/2),\tilde c_{j,k}(2p,p)^2)$ satisfies (3) with norms $\|\cdot\|_{k,p}$; $\mathrm{Var}_{\mu_j}(q_{j,k}f)\le\tilde c_{j,k}(2,2)\|f\|_{k,2}^2$.
- **Proposition 4.7 (p.30).** For $p=2^r$, $\alpha\gamma^{p-2}<1$: $\|\hat q_{j,k}f\|_{j,i,p}\le M_{j,k}(i)\delta(p)\max_{l\in s_k(i)}\|f\|_{k,l,p}$ and $\|\hat q_{j,k}f\|_{j,p}\le A_{j,k}\delta(p)\|f\|_{k,p}$ with the same $\delta(p)$ as in Part A Theorem 4.5.
- **Proposition 4.11 (p.32).** For $q\in[2^r,2^{r+1}]$, $\alpha\gamma^{2^{r+1}-2}<1$: $\|q_{j,k}f\|_{j,p}\le\tilde c_{j,k}(p,q)\|f\|_{k,q}$, $\tilde c_{j,k}(p,q)=A_{j,k}\theta_j(p,q)\gamma^{(p-1)/p}\gamma^{(q-1)/q}\delta(q)$. Compared with Part A, the only new ingredient is the mass-shift factor $A_{j,k}$; with one component and $F=E$, $A_{j,k}=1$ and Part A is recovered; for invariant partitions $A_{j,k}=\max_i\mu_k(F_i)/\mu_j(F_i)$ (eq. (56), the discrete-time analogue of Eberle-Marinelli).
- Then Theorem 2.2 gives an explicit error bound proportional to powers of $A_{j,k}$ (the leading term is the asymptotic variance; p.33). With $\gamma=1$ (relative densities constant on components) one gets $\|q_{j,k}f\|_{j,p}\le A_{j,k}\theta(p,q)(1-\alpha)^{-1}\|f\|_{k,q}$.
- **Outlook (pp.33-35), statements of the author:** the bad performance of SMC "is not a property of the target distribution $\mu_n$ but a property of the approximating sequence $\mu_0,\dots,\mu_{n-1}$"; problems from components gaining mass "can generally not be alleviated by increasing the number of interpolating distributions: adding steps can only increase $d_{j,k}$ and $A_{j,k}$" (p.34); the only fix is a different sequence. Heuristics (not theorems): mean-field Potts (Bhatnagar-Randall 2004) gives $d_{j,k}\propto\varepsilon^{-2}$ for tempering; mean-field Ising (Madras-Zheng 2002) gives $d_{j,k}=1$ so SMC should work.

## 4. Does any result cover (i)-(v)?

| Item | Part A | Part B |
|---|---|---|
| (i) $\{0,1\}^p$ | Any Polish space, so formally yes (finite spaces); no binary-specific statement; the $O(d^3)$ product-measure discussion is on $\mathbb R^d$ | Finite trees and finite index sets $I_k$; formally includes $\{0,1\}^p$ with a partition into mode cells, but no binary-space example |
| (ii) BVS / spike-and-slab posterior | No | No. No statistical model appears; no posterior-consistency or selection statement (examples are abstract trees; the only named models are Ising, Potts, Gaussian mixtures in the Outlook, heuristic only) |
| (iii) adaptive tempering | No (deterministic bridge, deterministic $t_k$) | No |
| (iv) frozen schedules | Yes, in the sense that EVERY result is for a deterministic, fixed schedule (that is the only case treated) | Yes, same |
| (v) evidence / normalising constant | Prop 2.3 with $f\equiv1$: $\mathbb E[\varphi_n]=1$, i.e. $\hat Z_n/Z_n$ is unbiased with exact variance $\frac1N\mathbb E\sum_jV_{j,n}^N(1)$. Theorems 3.2 and Cor 5.6 bound $\mathbb E|\nu^N_n(1)-1|^2$ under global mixing | Prop 3.3 gives the asymptotic variance of the evidence-type weight on trees; Prop 4.11 / Theorem 2.2 bound $\mathbb E|\nu_n^N(1)-1|^2$ under local mixing. Neither calls it an evidence estimator explicitly (my inference) |

## 5. Observations (my inference)
1. The estimator proved unbiased in Part A Prop 2.3 is $\nu_n^N(f)=\varphi_n\eta_n^N(f)$ with $\varphi_n=\prod_{j<n}\eta_j^N(g_{j,j+1})/\mu_j(g_{j,j+1})$. With unnormalised $g_{j,j+1}=Z_{j+1}\pi_{j+1}/(Z_j\pi_j)$-type weights, $\mu_j(g_{j,j+1})=Z_{j+1}/Z_j$, so $\prod_j\eta_j^N(g_{j,j+1})$ is unbiased for $Z_n/Z_0$. That is exactly our $\hat Z$ as a product of mean incremental weights.
2. The proof covers a DETERMINISTIC schedule, multinomial resampling at every step, and fixed kernels. It does not cover (a) adaptive resampling triggered by ESS, (b) an adaptively chosen grid, (c) several islands or a swap move that depends on the whole population. Our Prop 5 handles (b) by conditioning on the frozen calibration (the schedule becomes deterministic given the pilot) - the martingale argument is then exactly Part A's. The extension to random resampling times is known (Del Moral, Doucet and Jasra 2012 for adaptive SMC, from memory, not checked); whether islands/swaps remain covered must be checked in our own proof.
3. The mode-mass criterion. Prop 3.2 (tree) and Prop 4.11 (local mixing) say the error constant is governed by how much a component (mode) can GAIN mass relative to the earlier level: $d_{j,k}$ through $\mu_k^{\to j}(x)/\mu_j(x)$, $A_{j,k}$ through $\mu_k(F_i)/\mu_j(F_i)$. For a component with end-mass $\approx1$ and start-mass $\delta$, the constant is of order $\delta^{-2}$ ($d_{j,k}$) or $\delta^{-1}$-times-$\gamma$-powers ($A_{j,k}$). Hence a bound of this type is finite and polynomial in $1/\delta$ only if the start law gives the truth-containing region visible mass. This is the same dependence as the visibility/leakage assumption in our Theorem 3, but Schweizer proves a squared-error bound for a fixed integrand, not a "reports $S_0$ with high probability on data events" statement.
4. Both papers state that interpolating more distributions cannot repair mass-gain bottlenecks (Part B p.34). This matches why our start law is "block-exact" (a choice of $\mu_0$), not a longer tempering ladder.
5. Part A's bound is linear in the number of levels $n$ at leading order, and Part B shows $n^2$-type asymptotic variance on the tree at $\theta=1$ (Lemma 3.12). So the number of stages enters polynomially; this is relevant for choosing the length of our frozen grid in any finite-$N$ bound.

## 6. Relation to us

**Prop 5 (unbiased evidence conditional on the frozen calibration).** Schweizer 2012a, Proposition 2.3 (p.7) with $f\equiv1$ is a self-contained finite-$N$ statement and proof (martingale argument, pp.8-10), and it also gives the exact variance. Its own attribution is Del Moral and Miclo (2000, Section 2). Because the result is classical, Prop 5 should be stated as "a direct application of the classical unbiasedness of the Feynman-Kac particle approximation of the unnormalised measure; given the frozen calibration the schedule is deterministic". Primary citations: Del Moral (1996, 2004, Feynman-Kac Formulae, Chap. 7), Del Moral and Miclo (2000, Section 2), and Schweizer 2012a Prop 2.3 as the most explicit modern statement; for evidence estimation by SMC samplers, Del Moral, Doucet and Jasra (2006). SUPPORTS Prop 5 (it is the same result in the deterministic case); it does not cover adaptive resampling times, islands or swaps (see Observation 2). It gives no competing statement.

**Theorem 3 (every run reports the truth on high-probability data events).** NEITHER paper proves a selection or consistency statement and neither concerns a statistical posterior. What they provide is a structural analogue: the error of the particle approximation to $\mu_n(f)$ is bounded by $(1/N)\times$ [sum of variances] with constants controlled by the mass-gain ratios between levels (tree: $d_{j,k}$; local mixing: $A_{j,k}$). In our Thm 3 the visibility/leakage assumption on the start law plays the role of bounding those ratios at the truth-containing cell (Observation 3). One could cite Schweizer 2012b as a precedent that "mass of a mode must not grow much between level $j$ and level $k$" is the right type of hypothesis. SUPPORTS in spirit; no overlap in conclusion. Caveat: Part B's bounds are at fixed $f$, for the idealised kernels of Assumption A; they do not control the probability that a particular finite-$N$ run misses a mode (no hitting-probability statement).

**P1 (trap theorem: single-flip chains and Zanella-Roberts weighted tempered Gibbs mix slowly where our consistency holds).** Not proved here: neither paper has a lower bound for MCMC. What is relevant: (a) Part B Section 5 reports that TEMPERING-based chains (parallel and simulated tempering) are known to mix torpidly on the mean-field Potts model (Bhatnagar and Randall 2004) but rapidly on mean-field Ising (Madras and Zheng 2002), and that SMC should be judged by the mass-gain constant $d_{j,k}$ rather than by mixing; (b) the tree example shows SMC with resampling beats pure weighting by an exponential factor in $n$ (Cor 3.13), supporting the use of resampling over SIS/annealed IS as the comparator side. These are heuristics for P1 and cannot be quoted as a proof of slow mixing of single-flip chains. SUPPORTS (as background on "metastable targets, tempering-based MCMC slow versus SMC"); does not compete.

**Verdicts.** Part A: supports (Prop 5). Part B: supports (mass-gain criterion; no BVS; no selection theorem; asymptotic-variance and squared-error at fixed $f$).

## 7. Citations we should make
1. N. Schweizer (2012), Non-asymptotic error bounds for sequential MCMC and stability of Feynman-Kac propagators, arXiv:1204.2382, Proposition 2.3 (unbiasedness and exact variance of the weighted particle measure) - for Prop 5.
2. P. Del Moral and L. Miclo (2000), Branching and interacting particle systems approximations of Feynman-Kac formulae with applications to non-linear filtering, Seminaire de Probabilites XXXIV, LNM 1729, Section 2 (original source of the unbiasedness and the variance decomposition; the asymptotic variance coefficient, p.45 there).
3. P. Del Moral (2004), Feynman-Kac Formulae (Springer), unbiasedness of the unnormalised measure (chapter on unnormalised particle models; theorem numbers not checked) and non-asymptotic bounds (Thm 7.4.4 as cited by Schweizer).
4. P. Del Moral, A. Doucet and A. Jasra (2006), Sequential Monte Carlo samplers, JRSS B 68:411-436 - the SMC-sampler framework and the evidence estimator.
5. F. Cerou, P. Del Moral and A. Guyader (2011), A nonasymptotic variance theorem for unnormalized Feynman-Kac particle models, Ann. IHP 47:629-649 - relative variance of the unnormalised estimator.
6. N. Schweizer (2012), Non-asymptotic error bounds for sequential MCMC methods in multimodal settings, arXiv:1205.6733 - for the mass-gain criterion (Prop 3.2, Prop 4.11) and the resampling-versus-weighting comparison (Cor 3.13) when motivating the visibility/leakage hypothesis in Thm 3.
7. A. Eberle and C. Marinelli (2010, J. Math. Anal. Appl. 365:120-134; 2013, PTRF), $L^p$ estimates and quantitative approximation for continuous-time particle systems on disconnected components (cited by Schweizer for the invariant-partition case).
8. D. B. Woodard, S. C. Schmidler and M. Huber (2009a Ann. Appl. Probab. 19:617-640; 2009b EJP 14:780-804) for torpid/rapid mixing of parallel and simulated tempering, as the MCMC-side counterpart (read by Schweizer as comparators; not read by me here).
9. Where relevant for a competing non-asymptotic framework: N. Whiteley (2011/2013), SMC samplers: error bounds and insensitivity to initial conditions (minorisation/drift conditions; not read).
