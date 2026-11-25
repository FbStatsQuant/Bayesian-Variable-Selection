# THEORY note: Marion, Mathews and Schmidler (2023), finite-sample complexity of SMC estimators

Reader: Claude (Sonnet 5.5), 2026-11-24. Private to this machine. Page numbers are PDF pages of the local file. "(my inference)" marks anything the paper does not state itself; "(from memory, not checked)" marks facts from outside the paper.

## 0. Bibliographic and file caveat
- Title: Finite sample complexity of sequential Monte Carlo estimators. Authors: J. Marion, J. Mathews, S. C. Schmidler (Duke). Venue: Ann. Statist. (2023), DOI 10.1214/23-AOS2295.
- THE LOCAL FILE IS THE arXiv PREPRINT: stamp "arXiv:1803.09365v3 [math.ST] 18 Aug 2022", header "Submitted to the Annals of Statistics". The published AoS version may differ in constants and numbering. Check before quoting constants.
- Local file: `/home/fb31/SMC_Theory_Department/SMC_LIT/papers/MarionMathewsSchmidler2023_finite_sample_SMC.pdf`, 19 pages. Every page read as an image.

## 1. Coverage log
| PDF pages | Content |
|---|---|
| 1-2 | Abstract, 1 Introduction (literature: asymptotics, Feynman-Kac finite-sample bounds, outline) |
| 2-5 | 2 Sequential Monte Carlo: 2.1 notation (omega-warm, mixing time), 2.2 algorithm, 2.3 probability space, 2.4 coupled variables, Fig 1 |
| 5-6 | 3 Main result: AS1, AS2, Theorem 1, AS3, Corollary 1.1 |
| 6-11 | 4 Error bounds: events A_s, B_s, C_s; 4.1 Lemmas 2, 3, 4, 5, Corollary 5.1, proof of Theorem 1; 4.2 Lemma 6 (approx iid) |
| 11-13 | 5 Geometric mixtures: 5.1 Corollary 6.1; 5.2 comparison with importance sampling; 5.3 comparison with MCMC, Corollary 6.2; 5.3.1 finite spaces |
| 14-15 | 6 Product measures; 6.1 spherical Gaussian and temperature ladder choice |
| 15-16 | 7 Log-concave targets (MALA); 7.1 Bayesian logistic regression; 8 Conclusion |
| 17-18 | Appendix A (the only appendix): explicit maximal coupling, Lemmas 7, 8 |
| 18-19 | References |
All pages read (1-19); nothing skipped.

## 2. Setting
- State space: general measurable space (X, B), dominating measure lambda. Examples: finite spaces (5.3.1), R^d (product measures, Gaussians, log-concave).
- Algorithm (pp.3-4): N particles; X_0^{1:N} iid from mu_0; for s=1..S: (i) weights $w_s(x)=q_s(x)/q_{s-1}(x)$; (ii) multinomial resampling at EVERY step; (iii) t steps of a mu_s-invariant kernel K_s. Estimator $\hat f=N^{-1}\sum_n f(X_S^n)$.
- Bridge: arbitrary sequence mu_0..mu_S=pi in the main theorem; Section 5 specialises to geometric mixtures $q_\beta=q_\pi^\beta q_\nu^{1-\beta}$ (tempering when nu uniform; initial law nu equal to the prior in Bayesian usage), $\beta_s=s/S$, $S=\lceil\log\Gamma\rceil$, where $\Gamma\ge\sup\pi/\nu$.
- Kernels: any mu_s-invariant K_s; GLOBAL mixing needed (AS2/AS3): omega-warm mixing time $\tau_s(\epsilon,\omega)$ or a spectral gap $\rho_s$.
- Schedule: deterministic and fixed in advance. Adaptivity not covered (Conclusion p.16 says the techniques "may be well suited" to adaptive SMC).

## 3. Main theorems (faithful statements)

Notation: $\omega$-warm: $\nu\in\mathcal P_\omega(\mu)$ iff $\sup_B\nu(B)/\mu(B)\le\omega$; mixing time from an omega-warm start $\tau(\epsilon,\omega)=\min\{t:\sup_{\nu\in\mathcal P_\omega(\mu)}\|\nu K^t-\mu\|_{TV}\le\epsilon\}$ (p.3). With a spectral gap $\rho$: $\tau_K(\epsilon,\omega)\le\rho^{-1}(\log(2\epsilon^{-1})+\log(\omega-1))$ (p.3).

**AS1 (p.5).** $\sup_x w_s(x)\le W$ and $z_{s-1}/z_s\le Z$, so that $\dfrac{q_s(x)/z_s}{q_{s-1}(x)/z_{s-1}}\le W Z$ for all $s$.
**AS2.** $K_s$ has limiting distribution $\mu_s$ with mixing time $\tau_s(\epsilon,\omega)$.
**AS3.** $K_s$ is irreducible, aperiodic, $\mu_s$-invariant, with spectral gap $\rho_s$, $0<\rho_s\le\rho\le1$ (as printed; note that the printed inequality chain is odd, the corollary uses $\rho$ as a LOWER bound on gaps in Cor. 6.1 where $\rho=\min_s\rho_{\beta_s}$).

**Theorem 1 (pp.5-6).** Assume AS1 and AS2. Fix $\epsilon>0$ and sample $X_0^{1:N}$ independently from $\mu_0$. Let
1. $N\ge\tfrac12\log(128S)\cdot\max\{9W^2Z^2,\ 1/\epsilon^2\}$,
2. $t\ge\max_s\tau_s\big(\tfrac{1}{8NS},\,2\big)$.

Then for every $f$ with $|f|\le1$, $|\hat f-\pi(f)|\le\epsilon$ with probability at least $3/4$. (Boostable to $1-\delta$ by taking the median of $\mathcal O(\log(1/\delta))$ independent runs, Jerrum-Valiant-Vazirani 1986, quoted p.5; this is a statement in the paper.)

**Corollary 1.1 (p.6).** Under AS1 and AS3: $N\ge\tfrac12\log(128S)\max\{9W^2Z^2,\epsilon^{-2}\}$ and $t\ge\log(16NS)/\rho$ give the same conclusion with probability $\ge3/4$.

Proof architecture (pp.6-10): events $A_s=\{X_s^{1:N}=\bar X_s^{1:N}\}$ (coupling with exactly-$\mu_s$ particles), $B_s=\{|\hat w_{s+1}-\mu_s(w_{s+1})|\le\mu_s(w_{s+1})/3\}$, $C_s=A_s\cap B_s$. Lemma 3: conditional on $C_{s-1}$ the resampled marginal is omega-warm w.r.t. $\mu_s$ (with $\Pr(C_{s-1})\ge3/(2\omega)$). Lemma 2: $\Pr(A_s)\ge(1-\delta)\Pr(C_{s-1})$ for $t\ge\tau_s(\delta/N,\omega)$. Lemma 4: the coupled $\bar X_s^{1:N}$ are iid $\mu_s$. Lemma 5 + Cor 5.1: Hoeffding concentration, $\Pr(C_s)\ge(1-\delta)\Pr(C_{s-1})-\delta'$. Induction with $\delta=1/(8S)$, $\delta'=1/64S$... as printed $\delta'=1/(64S)$, giving $\Pr\ge3/4$. Global mixing is used in Lemma 2 (to make the omega-warm marginal mix to within $\delta/N$ in TV).

**Lemma 6 (p.11).** Under AS1, AS2 the particles $X_s^{1:N}$ are approximately iid: $\|\mathcal L(X_s^{1:N})-\mu_s^{\otimes N}\|_{TV}\le\delta_0/2$ for $t=\tau_s(\delta_0/(2N),2)$.

**Corollary 6.1 (p.12).** For geometric mixtures with $S=\lceil\log\Gamma\rceil$, $\beta_s=s/S$, $\gamma=WZ$, $\rho=\min_s\rho_{\beta_s}$: the number of kernel transitions for $|\hat f-\pi(f)|\le\epsilon$ w.p. $\ge3/4$ is $\mathcal O^\star\big(\frac{\epsilon^{-2}\vee\gamma^2}{\rho}\log\Gamma\log^2\log\Gamma\big)$.
**Corollary 6.2 (p.13).** Plain MCMC (N independent chains from $\nu$, $t'$ steps, $\nu\in\mathcal P_\Gamma(\pi)$): $\mathcal O^\star\big(\frac1{\rho_1}\log\Gamma\,\epsilon^{-2}\big)$. Comparison: SMC pays an extra $\log^2\log\Gamma$ but depends on gap of all tempered kernels ($\rho=\min_s\rho_{\beta_s}$), whereas MCMC depends only on $\rho_1$ (the target's gap). Note: $\rho_{\beta=1}$ is the gap of the target kernel, so under Cor 6.1 the SMC bound contains the target's gap, i.e. it is NO better than MCMC when the target kernel mixes slowly (my inference, direct reading of $\rho=\min_s\rho_{\beta_s}$ with $\beta_S=1$).
**5.3.1 Finite spaces (p.13).** $\mathcal X$ finite, $\pi(x)\propto q(x)$, $0<q\le1$, $\pi_0=\min\pi(x)$, $x_0=\arg\min\pi$, $\nu=\delta_{x_0}$ so $\Gamma\le1/\pi_0$: MCMC $\mathcal O^\star(\rho_1^{-1}\log(1/\pi_0)\epsilon^{-2})$; SMC with $\beta_0=1/\lceil\log(1/\pi_0)\rceil$, $S=\lceil\log(1/\pi_0)\rceil-1$, $\beta_s=(s+1)/\lceil\log(1/\pi_0)\rceil$ so $\gamma\le e$: $\mathcal O^\star\big(\frac{\epsilon^{-2}}{\rho}\log(1/\pi_0)\log^2\log(1/\pi_0)\big)$.
**Section 6 (p.14-15).** Product measures $\pi^d$, $\nu^d$: $S=\mathcal O(d)$, total $\mathcal O(d^2\log^2d)$ (improves Schweizer's $d^3$). Spherical Gaussian with precision $\phi$: linear precision ladder costs $\exp(\phi)$, log-linear $\phi_s=\phi^{s/d}$ gives $\gamma\le\sqrt\phi$, $S=d\lceil\log\phi\rceil$, $\beta_s=\exp(s/d)\wedge1$ gives $\gamma\le e^{1/2}$ and cost $\mathcal O^\star(d^2\log\phi\log^2d/\epsilon^2)$. Message (p.15): for concentrated (large-$\phi$) posteriors the ladder choice matters.
**Section 7 (p.15-16).** Strongly log-concave target, MALA kernel (Wu-Schmidler-Chen 2021), $\mu_0=N(x^*,1/L)$: $\mathcal O^\star(d^{3/2}\kappa^2\log^2(d\kappa))$; 7.1 Bayesian logistic regression with prior $N(0,\frac\alpha n(X^\top X)^{-1})$: $\mathcal O^\star\big((\frac{dn}{\alpha}\frac{\sigma_{\max}}{\sigma_{\min}})^2\log^2(\cdot)\max\{1,\sqrt{\frac n{d\alpha}\frac{\sigma_{\max}}{\sigma_{\min}}}\}\big)$. The paper calls this "to our knowledge the first non-asymptotic SMC bound on a problem of direct interest to Bayesian statistical practice" (p.2). It is a continuous-parameter, log-concave posterior (no model selection).

## 4. Does any result cover ...
- (i) Binary spaces: only through the generic "finite space" example 5.3.1 (any finite X, in particular {0,1}^p, but the bound is in terms of the unknown quantities $\rho$ (min gap of all tempered kernels) and $\pi_0=\min\pi$). No binary-space-specific analysis.
- (ii) BVS / spike-and-slab posterior: NO. The only Bayesian statistics example is logistic regression with a Gaussian prior (log-concave, continuous). No model space.
- (iii) Adaptive tempering: NO (explicitly deferred, p.16).
- (iv) Frozen/fixed schedules: YES, the analysis assumes a schedule fixed in advance (geometric/tempered ladders with $S=\lceil\log\Gamma\rceil$ or similar).
- (v) Evidence / normalising constant: motivation only (Intro p.1 "natural estimate of the normalizing constant"). Event $B_s$ and Lemma 5 give per-step relative accuracy 1/3 for $\hat w_{s+1}$ as an estimator of $z_{s+1}/z_s$ (needed internally; Section 5.2 uses relative accuracy for comparison with importance sampling), but there is NO theorem on the error, unbiasedness or variance of the product estimator $\hat Z=\prod_s\hat w_s$.

## 5. Observations for BVS (my inference)
- Global mixing requirement. AS2/AS3 require a spectral gap or omega-warm mixing for every tempered kernel including the one targeting the posterior ($\beta=1$). For single-flip chains on the trap design family (our P1), that gap is exponentially small, so Theorem 1/Cor 6.1 is vacuous there. This paper itself says so: "The bounds presented in this paper require a global mixing condition and would require modification to show the advantage of SMC [on multimodal targets]" (p.16). The sequel Mathews-Schmidler (2024) removes this by restricted kernels.
- The bound parameters $W,Z$ (A1) are computable for a bounded-range log score; the other ingredients ($\rho$, $\pi_0$) are not, in BVS.
- Our sampler has the moves "independence from $\pi_0$" and swaps, so its kernels are not a single standard chain; the paper's AS2 is about a single K_s. No result for mixtures of kernels, but they are just a kernel and AS2 can hold if the mixture has a gap (my inference).

## 6. Relation to us
- Prop 5 (unbiased evidence, frozen calibration): NOT proved here (no result on $\hat Z$). It is classical. Standard sources (from memory, not verified against the texts): Del Moral (2004, Feynman-Kac Formulae, Ch. 7, unbiasedness of the unnormalised particle approximation, i.e. $\mathbb E[\gamma_n^N(1)]=\gamma_n(1)$), Del Moral-Doucet-Jasra (2006, JRSSB) for the SMC-sampler form with product of mean incremental weights; also Cerou-Del Moral-Guyader (2011, Ann. IHP, ref [23] in this paper) for non-asymptotic bounds on the unnormalised Feynman-Kac particle model (relative $L_2$ bounds on $\hat Z$). The latter bears on the VARIANCE of $\hat Z$ rather than on bias. Proof is a one-line conditioning argument for a deterministic schedule, so we can state it with a short proof and cite these.
- Thm 3 (every run reports the truth on high-probability data events): no overlap. This paper bounds the Monte Carlo error to $\pi(f)$ for fixed $\pi$, w.p. 3/4, under global mixing and bounded weights. It has no data events, no notion of a reported model, and no guarantee that is uniform over seeds or calibration outcomes.
- P1 (trap theorem): SUPPORTS as a negative-side companion: its positive SMC result requires global mixing at every temperature including $\beta=1$ ($\rho=\min_s\rho_{\beta_s}$), so on a family where single-flip chains have exponentially small gap the bound says nothing, and our consistency would then rest on our own Thm 3, not on this theory. It does not compete with P1. For P1's wording: "generic SMC complexity theory (Marion-Mathews-Schmidler 2023) assumes global mixing of the final kernel; on our family that fails exactly for the single-flip and ZR chains".
- The finite-space example gives a clean statement we can quote: with a gap-$\rho$ kernel, SMC costs $\mathcal O^\star(\rho^{-1}\epsilon^{-2}\log(1/\pi_0)\log^2\log(1/\pi_0))$, equal to MCMC up to log factors, so SMC's advantage in their theory is only in settings where the tempered path improves the gap, not a gain for targets whose own kernel is slow.

## 7. Citations we should make
1. Marion, Mathews, Schmidler (2023, Ann. Statist., DOI 10.1214/23-AOS2295): the first non-asymptotic SMC complexity bounds with explicit dependence on weights, normaliser ratios, mixing; includes a finite-space example and log-concave Bayesian logistic regression; requires global mixing.
2. For the discussion of what SMC theory does not cover: "no complexity or consistency result for SMC over a model space"; cite together with Mathews-Schmidler (2024) as the local-mixing extension.
3. For Prop 5: Del Moral (2004) and Del Moral-Doucet-Jasra (2006) (verify the theorem numbers), and Cerou-Del Moral-Guyader (2011) if we mention variance of $\hat Z$.
4. For the temperature-ladder point (log-linear ladders for concentrated posteriors) when we justify ESS-adaptive schedules: Section 6.1 of this paper.
