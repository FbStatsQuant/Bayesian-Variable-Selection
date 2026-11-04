# Proof of Theorem T9 (prediction and variance contraction) and Corollary C9 (random-design Hellinger contraction), with Corollary T9a(iii) for polynomial $p$

Supplement material for *Split-and-merge with an exact merge: composite-start sequential Monte Carlo for Bayesian variable selection*, draft of 14 October 2026. Thread: T9 / C9. Prover: Fable 5.1 (lead), 14 October 2026. Version 3 (after two review rounds: round 1 on v1 by three Opus 5.5 and three GPT-6 Astra reviewers; round 2 on v2 by three GPT-6 Astra reviewers, the three Opus round-2 reviewers having been interrupted by a session reset; reports in `review/round1/` and `review/round2/`, rulings in `review/FINDINGS.md`; every finding accepted and fixed; round 2 found no fatal or gap finding in any theorem, only in side remarks, which v3 corrects). Status: see `review/VERIFICATION_REPORT.md`. Numerical sanity checks of the algebraic identities in `check_T9_C9.py` and `check_section9.py` (not part of the proof).

**Assumed from the draft.** Section 2 (model, priors, the closed form (1) of $m(S)$, the joint posterior of $(S,\beta_S,\sigma^2)$ stated before T9, the data-generating model); Lemma L6, of which two parts are used: L6(v) in the form $p(S_0)\ge\frac12(2p)^{-s_0}$ when $s_0\le k_{\max}$ (Lemma 3(d) of `proofs/T6/PROOF.md`), and L6(i), $w(k)/w(k+1)=(2p-k-1)/(k+1)$ (Section 9 only); Theorem T6 together with Corollary T9a(i), in the nonasymptotic form proved as Theorem 8 of `proofs/T6/PROOF.md` and restated as Fact D below. For C9 only: one standard concentration result for Gram matrices of sub-Gaussian rows, stated as Fact G in Section 7.3 and verified against its source (`CITED_RESULTS.md`). No other numbered result of the draft is used; in particular T7, T8 and T10 are not used.

**Summary of the outcome.**
- T9 is true as stated, for every sequence $p=p_n$ and every cap $k_{\max}\ge s_0$. Part (i) does not even need $\ell_n^2=o(n)$; that hypothesis is used only in part (ii), and there only to make $\varepsilon_n\to0$. The fixed-design argument (Sections 1 to 5) was verified step by step by all six reviewers of round 1.
- Part (ii) holds in the sharper form conjectured in the prover note: for every sequence $u_n\to\infty$ with $u_n\le\sqrt{n/8}$, $\Pi\big(|\sigma^2/\sigma_\star^2-1|>C(\varepsilon_n^2+u_nn^{-1/2})\mid y\big)\to0$ in probability (Corollary 5.1). The factor $u_n\to\infty$ cannot be replaced by a constant: for every $y$ and every design, the posterior mass of $\{|\sigma^2/\sigma_\star^2-1|\le cn^{-1/2}\}$ is bounded away from $1$ (Remark 6.2, with proof). With $u_n=\varepsilon_n\sqrt n$ the rate $C\varepsilon_n$ of the statement follows.
- The proof is organised around a master theorem (Theorem 5) in which the dimension bound is a free parameter $d$: if the posterior puts small mass on $\{|S|>d\}$, then prediction contracts at the rate $(d+s_0+1)\ell_n/n$ and the variance at the rate $(d+s_0+1)\ell_n/n+u_nn^{-1/2}$. With $d=m_n=O((s_0+1)\ell_n)$ from T6 this is T9. With $d=C_1'(s_0+1)$ it is the implication asserted in Corollary T9a(iii), with a constant that depends also on $C_1'$ (Section 5; this dependence is what the argument gives, and it is recorded as a wording amendment of the corollary; whether it can be removed is not settled here).
- The hypothesis of that implication, a dimension bound of order $s_0+1$, is proved in Section 9 for polynomial $p$ ($p\le n^A$) under T7's sparse eigenvalue condition, column standardisation and a cap of at least $m_n+s_0$: $\Pi(|S|>s_0+\lceil s_0(2A+1)\rceil\mid y)\to0$ (Theorem 13), hence T9 at the sharp rate $(s_0+1)\ell_n/n$ with a constant depending also on $A$ (Corollary 14). For super-polynomial $p$ the sharp dimension bound remains open (Remark 9.1).
- **C9 needs one amendment.** The frozen statement assumes "i.i.d. sub-Gaussian rows with covariance $\Sigma_x$" and does not assume centred rows. Read with sub-Gaussianity allowed to depend on $n$, it is false: with uncentred rows of mean of order $n$ the regression function has $\|\mu\|^2/n\to\infty$, the shrinkage floor forces every $Q_S\ge\|y\|^2/(n+1)$, the posterior of $\sigma^2$ sits at order $n$, and the Hellinger distance tends to $1$ (Remark 7.3; counterexample raised by two Astra reviewers and confirmed by computation). Read with a sub-Gaussian constant fixed in $n$, (R2), the mean of the rows is bounded and this mechanism disappears, but the proof still needs centred rows, (R1), to identify the second-moment matrix with $\Sigma_x$ in Lemmas 6 to 8; whether (R1) can be dropped under (R2) is not settled here. C9 is proved under (R1) and (R2) for the posterior computed either from the raw design or from the column-standardised design (Section 7); the prediction loss is invariant under column rescaling, and only the eigenvalue constant changes. The sparse eigenvalue condition is required up to $m_n+s_0$ with T6's $m_n$ for any admissible $\omega_n$ (the proof is written for an arbitrary $\omega_n\to\infty$ with $\omega_n\le\ell_n$).
- In the fixed-design part, the only union bound over models is the size-by-size bound of Lemma 3, which costs $k\,\ell_n$ for a model of size $k$; the sum over models in the comparison step costs nothing because $\sum_Sp(S)=1$ (Proposition 4). It is exactly what produces the factor $\ell_n$ in $\varepsilon_n^2$. The random-design part takes one more union bound, over supports, in Lemma 7.
- All constants are explicit in the proofs (collected in Section 8). The constant $C$ of T9 depends only on $(\sigma_\star^2,M,\varphi_0,a_0,b_0)$, as the statement requires; the thresholds "$n$ large" depend also on $s_0$ (through Fact D's constant) and, in Section 7, on the sub-Gaussian constant.

---

## 0. Setting, conventions and notation

All notation is that of Section 2 of the draft. Throughout, $n\ge4$ and $p\ge1$ are integers, $X\in\mathbb R^{n\times p}$ is fixed, $a_0,b_0>0$ are fixed, $\log$ is the natural logarithm, $[p]=\{1,\dots,p\}$, and a model is a set $S\subseteq[p]$ with $k=|S|$. Column standardisation ($\|x_j\|^2=n$) is never used in Sections 1 to 6; its role in C9 is discussed in Section 7.3, and it is a hypothesis in Section 9. We write
$$
\ell_n:=\log(p\vee n)\ \ (\ge\log n\ge\log4>1),\qquad \varepsilon_n^2:=\frac{(s_0+1)\ell_n^2}{n}.
$$
The inequalities $\log p\le\ell_n$, $\log n\le\ell_n$, $\log2<1\le\ell_n$ and $\log(n+1)\le2\log n\le2\ell_n$ (valid for $n\ge2$) are used without comment.

**Model and priors.** For a model $S$ with $k=|S|$: $G_S=X_S^\top X_S$, $\Gamma_S=G_S/n$, $z_S=X_S^\top y$, $\Lambda_S=\frac1n(G_S+I_k)$,
$$
y\mid\beta_S,\sigma^2,S\sim N_n(X_S\beta_S,\sigma^2I_n),\qquad \beta_S\mid\sigma^2,S\sim N_k(0,\sigma^2\Lambda_S^{-1}),\qquad \sigma^2\sim\mathrm{IG}(a_0,b_0),
$$
model prior $\mathrm{BB}(1,p)$ with cap $k_{\max}$: $p(S)=w(|S|)\mathbf 1\{|S|\le k_{\max}\}/W$. For $k=0$ there is no $\beta_S$ and $X_S\beta_S=0$.

**Marginal likelihood (draft (1)).** $H_S=(n+1)G_S+I_k$, $D_S=\det H_S/\det(G_S+I_k)$, $t_S=n\,z_S^\top H_S^{-1}z_S$, $Q_S=y^\top y-t_S$, $\nu=a_0+n/2$,
$$
m(S)=C_n\,D_S^{-1/2}(2b_0+Q_S)^{-\nu},\qquad C_n=\pi^{-n/2}(2b_0)^{a_0}\Gamma(\nu)/\Gamma(a_0). \tag{0.1}
$$

**The joint posterior (draft, Section 4, "The joint posterior").** With $\pi(S)=p(S)m(S)/Z$, $Z=\sum_Sp(S)m(S)$,
$$
S\sim\pi,\qquad \sigma^2\mid S,y\sim\mathrm{IG}\Big(\nu,\frac{2b_0+Q_S}{2}\Big),\qquad \beta_S\mid\sigma^2,S,y\sim N_k\big(\hat\beta_S,\ n\sigma^2H_S^{-1}\big),\quad \hat\beta_S:=nH_S^{-1}z_S. \tag{0.2}
$$
Here $\mathrm{IG}(\nu,b)$ has density $\propto v^{-\nu-1}e^{-b/v}$, so that $b/\sigma^2\sim\mathrm{Gamma}(\nu,1)$ (shape $\nu$, rate $1$). $\Pi(\cdot\mid y)$ denotes this joint posterior as well as its marginal on $S$; for a set $\mathcal A$ of models, $\Pi(\mathcal A\mid y)=\sum_{S\in\mathcal A}\pi(S)$. (The conditional laws (0.2) are the standard conjugate updates; they are taken from the draft. Lemma 1(c) exhibits the quadratic form of the posterior kernel in $\beta_S$, and the inverse-gamma update is read off the $v$-integral in Lemma 1 of `proofs/T6/PROOF.md`; three reviewers re-derived (0.2) independently.)

**Data-generating model.** $y=\mu+\varepsilon$, $\mu=X\beta^\star=X_{S_0}\beta^\star_{S_0}$, $\varepsilon\sim N_n(0,\sigma_\star^2I_n)$, $S_0=\operatorname{supp}\beta^\star$, $s_0=|S_0|$. $\mathbb P_0,\mathbb E_0$ are over $\varepsilon$ with $X,\beta^\star,\sigma_\star^2$ fixed. We write
$$
E:=\|\varepsilon\|^2/\sigma_\star^2\sim\chi^2_n,\qquad \mathbb E_0E=n,\quad \mathrm{Var}_0E=2n .
$$

**Standing assumptions (draft, Section 4, as modified in T9).** $s_0$ fixed; the prior $\mathrm{BB}(1,p)$ with any cap $k_{\max}\ge s_0$; bounded signal $\|\mu\|^2/n\le M$; $\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2>0$ (vacuous if $s_0=0$); and, for T9(ii) only, $\ell_n^2=o(n)$. As in T6, the design and the signal enter only through
$$
\delta:=\beta^{\star\top}_{S_0}\Lambda_{S_0}\beta^\star_{S_0}=\frac{\|\mu\|^2+\|\beta^\star_{S_0}\|^2}{n}\ \le\ M\big(1+\varphi_0^{-2}\big)=:\bar\delta \tag{0.3}
$$
($\delta=0$ if $s_0=0$). The bound: $\|\mu\|^2=n\,\beta^{\star\top}_{S_0}\Gamma_{S_0}\beta^\star_{S_0}\ge n\varphi_0^2\|\beta^\star_{S_0}\|^2$, so $\|\beta^\star_{S_0}\|^2\le M/\varphi_0^2$ and $\delta\le M+M/(n\varphi_0^2)\le\bar\delta$.

**Two constants used throughout.**
$$
B:=2\big(b_0+M+2\sigma_\star^2\big),\qquad c_0:=\frac1{2B}=\frac1{4(b_0+M+2\sigma_\star^2)} . \tag{0.4}
$$

**The statements to be proved.**

*Theorem T9 (draft, Theorem 4.6).* Under the standing assumptions, there is a constant $C$ depending only on $(\sigma_\star^2,M,\varphi_0,a_0,b_0)$ such that, in $\mathbb P_0$-probability,
(i) $\Pi(\|X_S\beta_S-\mu\|^2/n>C\varepsilon_n^2\mid y)\to0$; (ii) $\Pi(|\sigma^2/\sigma_\star^2-1|>C\varepsilon_n\mid y)\to0$.

*Corollary T9a(iii) (draft, Corollary 4.7(iii)).* "If $\Pi(|S|>C(s_0+1)\mid y)\to0$ in probability for a constant $C$, then T9 holds with $\varepsilon_n^2=(s_0+1)\ell_n/n$, and (ii) extends to $0<\alpha<1$" (where (ii) refers to T9a(ii): $\log p\asymp n^\alpha$ gives $\varepsilon_n^2\asymp(s_0+1)n^{\alpha-1}$). We write $C_1'$ for the constant in the hypothesis. *Ruling on the wording (round 1, finding 4).* The constant in the conclusion depends on $C_1'$ as well as on $(\sigma_\star^2,M,\varphi_0,a_0,b_0)$; this is what the argument gives (the noise budget of every model is linear in its dimension); whether it can be removed is not settled here, and the corollary is proved in this form (Section 5). The dimension bound itself is proved in Section 9 for polynomial $p$, with $C_1'$ depending on $A$.

*Corollary C9 (draft, Corollary 4.8).* Stated in Section 7, with the amendment (R1) and the two clarifications (R2), (R4).

**Fact D (T6 in nonasymptotic form; Theorem 8 and Remark 4.1 of `proofs/T6/PROOF.md`).** Let $n\ge2$, $p\ge1$, $k_{\max}\ge s_0$, and let $X,\beta^\star,\sigma_\star^2$ be arbitrary with $\delta\le\bar\delta$. There is a constant $K_\star$ depending only on $(a_0,b_0,\sigma_\star^2,M,\varphi_0,s_0)$ such that for every integer $m$ and every $t>0$,
$$
\mathbb P_0\Big(\Pi(|S|>m\mid y)>2t\,e^{K_\star}\,2^{-m}(2p)^{s_0}n^{(s_0+1)/2}\Big)\le\frac1t+\frac8n .
$$
(T6's Theorem 8 has its constant $K$ of (3.3) there in place of $K_\star$; $K$ is nondecreasing in $\delta$ and $K_\star$ is its value at $\bar\delta$, so the event above is contained in T6's.) Fix once and for all a sequence $(\omega_n)$ with
$$
\omega_n\to\infty,\qquad \omega_n\le\ell_n
$$
(for instance the draft's $\omega_n=\log\log n$, or $\omega_n=\ell_n$), and let
$$
m_n:=\Big\lceil\frac{s_0\log(2p)+\frac{s_0+1}2\log n+\omega_n}{\log2}\Big\rceil \tag{0.5}
$$
be T6's cutoff for this $\omega_n$. Then $2^{-m_n}(2p)^{s_0}n^{(s_0+1)/2}\le e^{-\omega_n}$, and Fact D with $t=e^{\omega_n/2}$ gives
$$
\mathbb P_0\Big(\Pi(|S|>m_n\mid y)>2e^{K_\star}e^{-\omega_n/2}\Big)\le e^{-\omega_n/2}+\frac8n=:q_n^D\longrightarrow0 . \tag{0.6}
$$
This is the only place where the dimension bound enters; it uses no condition on $p$ (Corollary T9a(i)). Moreover, by $\omega_n\le\ell_n$,
$$
m_n\le\frac{s_0(\log2+\ell_n)+\frac{s_0+1}2\ell_n+\ell_n}{\log2}+1\le s_0+1+\frac{3(s_0+1)\ell_n}{2\log2}\le4(s_0+1)\ell_n , \tag{0.7}
$$
using $\frac{3}{2\log2}<2.17$ and $s_0+1\le(s_0+1)\ell_n$. Everything below holds for every admissible choice of $(\omega_n)$, with constants that do not depend on it; only the exceptional probability $q_n^D$ and the posterior tail bound $2e^{K_\star}e^{-\omega_n/2}$ do. Since $\omega_n\to\infty$, $m_n\ge1$ for all large $n$; the finite-$n$ statements of Sections 7 and 9 that involve $m_n$ (Lemmas 7, 8, 10, Proposition 12) are made for such $n$.

**Roadmap.** Section 1 isolates the conditional structure: the fitted vector $X_S\hat\beta_S=M_Sy$ for a matrix $0\preceq M_S\preceq P_S$, the exact decomposition $Q_S=a_S+2W_S+\varepsilon^\top(I-M_S)\varepsilon$ with the deterministic *ridge approximation error* $a_S=\mu^\top(I-M_S)\mu$ and the Gaussian cross term $W_S$, and the bounds $a_{S_0}\le\delta$, $1\le D_S\le(n+1)^{|S|}$. Section 2 proves the uniform noise bounds, size by size. Section 3 shows that models with $a_S$ large lose against $S_0$, deterministically on the good event, with a bound summed against the prior. Section 4 assembles the master theorem for a generic dimension $d$. Section 5 derives T9 and the T9a(iii) implication. Section 6 collects remarks (where hypotheses enter; sharpness of the $n^{-1/2}$ term). Section 7 proves C9. Section 8 lists hypotheses added, constants, and the least certain steps. Section 9 proves the sharp dimension bound for polynomial $p$, and with it Corollary T9a(iii) in that regime.

---
## 1. The conditional structure

Define, for every model $S$,
$$
M_S:=nX_SH_S^{-1}X_S^\top\in\mathbb R^{n\times n},\qquad a_S:=\mu^\top(I_n-M_S)\mu,\qquad W_S:=\mu^\top(I_n-M_S)\varepsilon,\qquad v_S:=\|(I_n-M_S)\mu\|^2
$$
(for $k=0$: $M_\emptyset=0$, $a_\emptyset=\|\mu\|^2$, $W_\emptyset=\mu^\top\varepsilon$).

**Lemma 1 (algebra of the conditional posterior).** For every model $S$ with $k=|S|$ and every $y\in\mathbb R^n$:

(a) $M_S$ is symmetric, $0\preceq M_S\preceq\frac n{n+1}P_S\preceq P_S$, $M_S^2\preceq M_S$, $\operatorname{tr}M_S\le k$, and $0\preceq I-M_S\preceq I$ with $(I-M_S)^2\preceq I-M_S$.

(b) $X_S\hat\beta_S=M_Sy$ and $Q_S=y^\top(I-M_S)y$. In particular $0\le Q_S\le y^\top y$.

(c) For every $w\in\mathbb R^n$, $w^\top(I-M_S)w=\min_{b\in\mathbb R^k}\{\|w-X_Sb\|^2+b^\top\Lambda_Sb\}$ (for $k=0$ the right side is $\|w\|^2$). Consequently $0\le a_S\le\|\mu\|^2$, $a_{S_0}\le\delta$, and $v_S\le a_S$.

(d) $Q_S=a_S+2W_S+\sigma_\star^2E-\varepsilon^\top M_S\varepsilon$ with $0\le\varepsilon^\top M_S\varepsilon\le\|P_S\varepsilon\|^2$. Hence
$$
|Q_S-\sigma_\star^2E|\le a_S+2|W_S|+\|P_S\varepsilon\|^2 . \tag{1.1}
$$

(e) $1\le D_S\le(n+1)^k$.

(f) Given $(\sigma^2,S,y)$, $X_S\beta_S-M_Sy\sim N_n(0,\sigma^2M_S)$; hence $\mathbb E\big[\|X_S\beta_S-M_Sy\|^2\mid\sigma^2,S,y\big]=\sigma^2\operatorname{tr}M_S\le\sigma^2k$. Given $(S,y)$, if $\nu>1$ then $\mathbb E[\sigma^2\mid S,y]=\frac{2b_0+Q_S}{2(\nu-1)}=\frac{2b_0+Q_S}{n+2a_0-2}$.

(g) Pointwise,
$$
\|M_Sy-\mu\|^2\le2a_S+2\|P_S\varepsilon\|^2,\qquad \|X_S\beta_S-\mu\|^2\le2\|X_S\beta_S-M_Sy\|^2+4a_S+4\|P_S\varepsilon\|^2 . \tag{1.2}
$$

*Proof.* (a) Let $G_S=U\operatorname{diag}(\lambda_1,\dots,\lambda_k)U^\top$ be a spectral decomposition, $\lambda_i\ge0$. Then $H_S^{-1}=U\operatorname{diag}\big(((n+1)\lambda_i+1)^{-1}\big)U^\top$, so $M_S=nX_SU\operatorname{diag}\big(((n+1)\lambda_i+1)^{-1}\big)U^\top X_S^\top$. The columns $X_SUe_i$ are orthogonal with squared norms $\lambda_i$; for $\lambda_i>0$ put $q_i=X_SUe_i/\sqrt{\lambda_i}$, an orthonormal family spanning the column space of $X_S$ (the $i$ with $\lambda_i=0$ contribute $X_SUe_i=0$). Then
$$
M_S=\sum_{i:\lambda_i>0}\frac{n\lambda_i}{(n+1)\lambda_i+1}\,q_iq_i^\top,\qquad P_S=\sum_{i:\lambda_i>0}q_iq_i^\top .
$$
Since $0\le\frac{n\lambda}{(n+1)\lambda+1}<\frac{n}{n+1}<1$ for $\lambda>0$, all claims in (a) follow: $M_S$ is symmetric with eigenvalues in $[0,1)$ on the column space and $0$ on its orthogonal complement, so $M_S\preceq\frac n{n+1}P_S$, $M_S^2\preceq M_S$, $\operatorname{tr}M_S\le\operatorname{rank}X_S\le k$, and $I-M_S$ has eigenvalues in $(0,1]$, whence $(I-M_S)^2\preceq I-M_S\preceq I$.

(b) $X_S\hat\beta_S=nX_SH_S^{-1}X_S^\top y=M_Sy$, and $Q_S=y^\top y-n\,y^\top X_SH_S^{-1}X_S^\top y=y^\top(I-M_S)y$. The bounds follow from $0\preceq I-M_S\preceq I$.

(c) The function $b\mapsto\|w-X_Sb\|^2+b^\top\Lambda_Sb=w^\top w-2b^\top X_S^\top w+b^\top(G_S+\Lambda_S)b$ is a strictly convex quadratic ($G_S+\Lambda_S\succeq\Lambda_S\succ0$) with minimiser $b^\ast=(G_S+\Lambda_S)^{-1}X_S^\top w$ and minimum value $w^\top w-w^\top X_S(G_S+\Lambda_S)^{-1}X_S^\top w$. Since $G_S+\Lambda_S=\frac1n\big((n+1)G_S+I_k\big)=H_S/n$, this minimum is $w^\top w-n\,w^\top X_SH_S^{-1}X_S^\top w=w^\top(I-M_S)w$. (This is also Lemma 4 of `proofs/T6/PROOF.md` with $y$ replaced by $w$.) Taking $w=\mu$: $b=0$ gives $a_S\le\|\mu\|^2$, and $a_S\ge0$ by (a). For $S=S_0$ take $b=\beta^\star_{S_0}$: $\|\mu-X_{S_0}\beta^\star_{S_0}\|^2=0$ and $\beta^{\star\top}_{S_0}\Lambda_{S_0}\beta^\star_{S_0}=\delta$, so $a_{S_0}\le\delta$. Finally $v_S=\mu^\top(I-M_S)^2\mu\le\mu^\top(I-M_S)\mu=a_S$ by (a).

(d) Expand $Q_S=(\mu+\varepsilon)^\top(I-M_S)(\mu+\varepsilon)=a_S+2W_S+\varepsilon^\top\varepsilon-\varepsilon^\top M_S\varepsilon$ and use $\varepsilon^\top\varepsilon=\sigma_\star^2E$ and $0\preceq M_S\preceq P_S$.

(e) With the eigenvalues of (a), $D_S=\prod_{i=1}^k\frac{(n+1)\lambda_i+1}{\lambda_i+1}$ and $1\le\frac{(n+1)\lambda+1}{\lambda+1}\le n+1$ for $\lambda\ge0$. (Lemma 6 of `proofs/T6/PROOF.md`.)

(f) By (0.2), $\beta_S-\hat\beta_S\sim N_k(0,n\sigma^2H_S^{-1})$ given $(\sigma^2,S,y)$, so $X_S(\beta_S-\hat\beta_S)\sim N_n(0,\sigma^2nX_SH_S^{-1}X_S^\top)=N_n(0,\sigma^2M_S)$, with second moment $\sigma^2\operatorname{tr}M_S$. For $\mathrm{IG}(\nu,b)$ with $\nu>1$ the mean is $b/(\nu-1)$; here $b=(2b_0+Q_S)/2$ and $2(\nu-1)=n+2a_0-2$.

(g) $M_Sy-\mu=-(I-M_S)\mu+M_S\varepsilon$, so $\|M_Sy-\mu\|^2\le2v_S+2\|M_S\varepsilon\|^2\le2a_S+2\varepsilon^\top M_S^2\varepsilon\le2a_S+2\|P_S\varepsilon\|^2$ by (a), (c). Then $\|X_S\beta_S-\mu\|^2\le2\|X_S\beta_S-M_Sy\|^2+2\|M_Sy-\mu\|^2$. $\blacksquare$

*Remark 1.1 (the role of $a_S$).* $a_S=\min_b\{\|\mu-X_Sb\|^2+b^\top\Lambda_Sb\}$ is the best approximation error of the regression function by model $S$, penalised by the prior precision; it satisfies $\|(I-P_S)\mu\|^2\le a_S$, and it is small for the true model ($a_{S_0}\le\delta=O(1)$) because the unit-information prior puts the truth at $O(1)$ penalty. It is the quantity that the posterior drives down: Proposition 4 shows that models with $a_S\gg(|S|+s_0+1)\ell_n$ have negligible posterior mass, which is a statement about prediction, not about support recovery, and so needs no beta-min condition.

---

## 2. Uniform noise bounds

**Lemma 2 (two tail bounds).** (a) If $\xi\sim\chi^2_r$ with $r\ge0$ an integer ($\chi^2_0\equiv0$), then $\mathbb P(\xi\ge2r\log2+4\tau)\le e^{-\tau}$ for every $\tau\ge0$. (b) If $\zeta\sim N(0,v)$ with $v\ge0$, then $\mathbb P(|\zeta|>\sqrt{2v\tau})\le2e^{-\tau}$ for every $\tau\ge0$.

*Proof.* (a) $\mathbb Ee^{\xi/4}=(1-\frac12)^{-r/2}=2^{r/2}$, so by Markov $\mathbb P(\xi\ge x)\le2^{r/2}e^{-x/4}$; put $x=2r\log2+4\tau$. (b) For $v=0$ the claim is trivial. Otherwise $\zeta/\sqrt v\sim N(0,1)$ and $\mathbb P(N(0,1)>x)\le e^{-x^2/2}$ for $x\ge0$ (Chernoff: $\mathbb P(N>x)\le e^{-\lambda x}\mathbb Ee^{\lambda N}=e^{-\lambda x+\lambda^2/2}$ at $\lambda=x$); apply it to $\pm\zeta/\sqrt v$ with $x=\sqrt{2\tau}$. $\blacksquare$

**Lemma 3 (uniform bounds, size by size).** Define the events
$$
\mathcal E_1:=\{E\le2n\},\qquad
\mathcal E_2:=\Big\{\|P_S\varepsilon\|^2\le14\,\sigma_\star^2|S|\,\ell_n\ \text{ for every model }S\Big\},\qquad
\mathcal E_3:=\Big\{|W_S|\le2\sigma_\star\sqrt{a_S(|S|+1)\ell_n}\ \text{ for every model }S\Big\},
$$
and $\Omega_n:=\mathcal E_1\cap\mathcal E_2\cap\mathcal E_3$. Then
$$
\mathbb P_0(\mathcal E_1^c)\le\frac2n,\qquad \mathbb P_0(\mathcal E_2^c)\le e^{-\ell_n}\le\frac1n,\qquad \mathbb P_0(\mathcal E_3^c)\le4e^{-\ell_n}\le\frac4n,\qquad \mathbb P_0(\Omega_n^c)\le\frac7n .
$$
These bounds involve neither $p$, nor the design, nor $\beta^\star$, nor the cap. On $\mathcal E_1$, moreover,
$$
y^\top y\le2\|\mu\|^2+2\|\varepsilon\|^2\le2nM+4n\sigma_\star^2\le nB-2b_0,\qquad\text{so}\qquad 2b_0+Q_S\le2b_0+y^\top y\le nB\ \text{ for every }S . \tag{2.1}
$$

*Proof.* $\mathcal E_1$: by Chebyshev, $\mathbb P_0(E>2n)\le\mathbb P_0(|E-n|\ge n)\le\mathrm{Var}_0E/n^2=2/n$. (2.1): $\|y\|^2\le2\|\mu\|^2+2\|\varepsilon\|^2$, $\|\mu\|^2\le nM$, $\|\varepsilon\|^2=\sigma_\star^2E\le2n\sigma_\star^2$ on $\mathcal E_1$, and $2nM+4n\sigma_\star^2+2b_0\le n(2M+4\sigma_\star^2+2b_0)=nB$ for $n\ge1$; then $Q_S\le y^\top y$ by Lemma 1(b).

$\mathcal E_2$: for a model $S$ with $|S|=k\ge1$, $\|P_S\varepsilon\|^2/\sigma_\star^2\sim\chi^2_r$ with $r=\operatorname{rank}X_S\le k$, because $P_S$ is an orthogonal projection of rank $r$ and $\varepsilon/\sigma_\star$ is standard Gaussian. Put $\tau_k:=k\log p+k\log2+\ell_n$. By Lemma 2(a) with $r\le k$,
$$
\mathbb P_0\big(\|P_S\varepsilon\|^2\ge\sigma_\star^2(2k\log2+4\tau_k)\big)\le e^{-\tau_k}=p^{-k}2^{-k}e^{-\ell_n}.
$$
There are $\binom pk\le p^k$ models of size $k$, so the union over all models of all sizes $k\ge1$ has probability at most $\sum_{k\ge1}p^k\,p^{-k}2^{-k}e^{-\ell_n}=e^{-\ell_n}$. On its complement, for every $S$ with $|S|=k\ge1$,
$$
\|P_S\varepsilon\|^2<\sigma_\star^2\big(2k\log2+4k\log p+4k\log2+4\ell_n\big)\le\sigma_\star^2\big(6k+4k+4k\big)\ell_n=14\sigma_\star^2k\ell_n ,
$$
using $\log2\le\ell_n$, $\log p\le\ell_n$ and $1\le k$. For $S=\emptyset$ both sides are $0$. Hence $\mathbb P_0(\mathcal E_2^c)\le e^{-\ell_n}\le e^{-\log n}=1/n$.

$\mathcal E_3$: $W_S=\mu^\top(I-M_S)\varepsilon\sim N(0,\sigma_\star^2v_S)$ with $v_S\le a_S$ (Lemma 1(c)). With the same $\tau_k$ (now for all $k\ge0$; $\tau_0=\ell_n$ and there is one model of size $0$), Lemma 2(b) gives $\mathbb P_0(|W_S|>\sigma_\star\sqrt{2v_S\tau_k})\le2e^{-\tau_k}$, and the union over all models has probability at most $2e^{-\ell_n}\big(1+\sum_{k\ge1}2^{-k}\big)=4e^{-\ell_n}$. On its complement, since $\tau_k\le k\ell_n+k\ell_n+\ell_n=(2k+1)\ell_n\le2(k+1)\ell_n$,
$$
|W_S|\le\sigma_\star\sqrt{2a_S\cdot2(k+1)\ell_n}=2\sigma_\star\sqrt{a_S(k+1)\ell_n}.
$$
Finally $\mathbb P_0(\Omega_n^c)\le2/n+1/n+4/n$. $\blacksquare$

*Remark 2.1 (the cost of the union bounds).* The union over the $\binom pk$ models of size $k$ costs $k\log p\le k\ell_n$ in the exponent, and the sum over $k$ costs a further $k\log2$, both linear in $k$. This is the only union bound over models in the fixed-design part of the proof (Sections 1 to 6; the random-design part takes one more, over supports, in Lemma 7), and its cost, $O(k\ell_n)$ for $|S|=k\le d$, is exactly the budget $O(d\ell_n)$ of the master theorem. No union bound over the $p^{m_n}$ models of size at most $m_n$ is taken anywhere with a cost exceeding this.

---

## 3. Models with a large approximation error lose

**Proposition 4 (bad models lose; deterministic on $\Omega_n$).** Let $d\ge0$ be an integer and put
$$
C_1:=22\sigma_\star^2+2\delta,\qquad \rho(d):=\frac2{c_0}\big[3(s_0+1)+1\big]\ell_n+2C_1(d+s_0+1)\ell_n\ \le\ C_a(d+s_0+1)\ell_n,\qquad C_a:=\frac8{c_0}+2C_1 , \tag{3.1}
$$
and $\mathcal B(d):=\{S:|S|\le d,\ a_S>\rho(d)\}$. Assume $s_0\le k_{\max}$. Then on $\Omega_n$,
$$
\Pi(\mathcal B(d)\mid y)\le e^{-\ell_n}\le\frac1n .
$$
(The second inequality in (3.1): $\frac2{c_0}(3(s_0+1)+1)\le\frac8{c_0}(s_0+1)\le\frac8{c_0}(d+s_0+1)$.)

*Proof.* Fix $S\in\mathcal B(d)$ with $k=|S|$ and $p(S)>0$ (models with $p(S)=0$ have $\pi(S)=0$ and contribute nothing). Write $\Delta_S:=Q_S-Q_{S_0}$.

*Step 1 (a lower bound for $\Delta_S$ on $\Omega_n$).* By Lemma 1(d) applied to $S$ and to $S_0$,
$$
\Delta_S=a_S-a_{S_0}+2W_S-2W_{S_0}-\varepsilon^\top M_S\varepsilon+\varepsilon^\top M_{S_0}\varepsilon\ \ge\ a_S-a_{S_0}-2|W_S|-2|W_{S_0}|-\|P_S\varepsilon\|^2 .
$$
On $\mathcal E_3$, $2|W_S|\le4\sigma_\star\sqrt{a_S(k+1)\ell_n}\le\frac{a_S}2+8\sigma_\star^2(k+1)\ell_n$ (as $4\sqrt{xy}=2\sqrt{(x/2)(8y)}\le x/2+8y$), and, since $a_{S_0}\le\delta$ and $|S_0|=s_0$, $2|W_{S_0}|\le4\sigma_\star\sqrt{\delta(s_0+1)\ell_n}\le\delta+4\sigma_\star^2(s_0+1)\ell_n$. On $\mathcal E_2$, $\|P_S\varepsilon\|^2\le14\sigma_\star^2k\ell_n$. With $a_{S_0}\le\delta$,
$$
\Delta_S\ \ge\ \frac{a_S}2-2\delta-\sigma_\star^2\big[8(k+1)+4(s_0+1)+14k\big]\ell_n\ \ge\ \frac{a_S}2-C_1(k+s_0+1)\ell_n , \tag{3.2}
$$
because $8(k+1)+4(s_0+1)+14k=22k+4s_0+12\le22(k+s_0+1)$ and $2\delta\le2\delta(k+s_0+1)\ell_n$ (as $\ell_n\ge1$).

*Step 2 ($\Delta_S>0$ on $\mathcal B(d)$).* Since $k\le d$, (3.1) gives $\frac{\rho(d)}2\ge C_1(d+s_0+1)\ell_n\ge C_1(k+s_0+1)\ell_n$, so $a_S>\rho(d)$ and (3.2) give $\Delta_S\ge\frac{a_S}2-C_1(k+s_0+1)\ell_n\ge\frac{a_S}2-\frac{\rho(d)}{2}>0$.

*Step 3 (the Bayes factor).* By (0.1) and Lemma 1(e) ($D_S\ge1$, $D_{S_0}\le(n+1)^{s_0}$),
$$
\log\frac{m(S)}{m(S_0)}=-\frac12\log D_S+\frac12\log D_{S_0}-\nu\log\frac{2b_0+Q_S}{2b_0+Q_{S_0}}\le\frac{s_0}2\log(n+1)-\nu\log\Big(1+\frac{\Delta_S}{2b_0+Q_{S_0}}\Big).
$$
Since $\Delta_S>0$ and $\log(1+x)\ge\frac{x}{1+x}$ for $x\ge0$,
$$
\nu\log\Big(1+\frac{\Delta_S}{2b_0+Q_{S_0}}\Big)\ge\nu\,\frac{\Delta_S}{2b_0+Q_{S_0}+\Delta_S}=\frac{\nu\,\Delta_S}{2b_0+Q_S}\ge\frac{n}{2}\cdot\frac{\Delta_S}{nB}=c_0\Delta_S ,
$$
using $\nu\ge n/2$ and (2.1) (valid on $\mathcal E_1$). Hence $\log\frac{m(S)}{m(S_0)}\le\frac{s_0}2\log(n+1)-c_0\Delta_S\le s_0\ell_n-c_0\Delta_S$.

*Step 4 (the prior).* By L6(v) (Lemma 3(d) of `proofs/T6/PROOF.md`), $-\log p(S_0)\le\log2+s_0\log(2p)\le\log 2+s_0\log2+s_0\ell_n\le(2s_0+1)\ell_n$, using $s_0\le k_{\max}$ and $\log2\le\ell_n$. Together with Step 3,
$$
\log\frac{p(S)m(S)}{p(S_0)m(S_0)}\le\log p(S)+(2s_0+1)\ell_n+s_0\ell_n-c_0\Delta_S\le\log p(S)+3(s_0+1)\ell_n-c_0\Delta_S .
$$

*Step 5 (the margin).* By (3.2) and $a_S>\rho(d)$,
$$
c_0\Delta_S\ \ge\ \frac{c_0a_S}2-c_0C_1(k+s_0+1)\ell_n\ >\ \frac{c_0\rho(d)}2-c_0C_1(d+s_0+1)\ell_n=\big[3(s_0+1)+1\big]\ell_n ,
$$
by the definition (3.1) of $\rho(d)$. Hence $\log\frac{p(S)m(S)}{p(S_0)m(S_0)}<\log p(S)-\ell_n$.

*Step 6 (summation).* Since $p(S_0)m(S_0)>0$ (as $s_0\le k_{\max}$ and $m(S_0)>0$ by (0.1)), $Z\ge p(S_0)m(S_0)$ and
$$
\Pi(\mathcal B(d)\mid y)=\sum_{S\in\mathcal B(d)}\frac{p(S)m(S)}{Z}\le\sum_{S\in\mathcal B(d)}\frac{p(S)m(S)}{p(S_0)m(S_0)}<e^{-\ell_n}\sum_{S}p(S)=e^{-\ell_n}\le\frac1n .\qquad\blacksquare
$$

*Remark 3.1 (where the rate comes from).* The threshold $\rho(d)$ has three parts: the cost $3(s_0+1)\ell_n$ of the prior and Occam factor of $S_0$ (through $(2p)^{s_0}$ and $(n+1)^{s_0/2}$); the noise cost $C_1(d+s_0+1)\ell_n$ from Lemma 3, which is the dominant term and is linear in the dimension $d$ because every model is charged for its own projected noise $\|P_S\varepsilon\|^2$ and its own cross term $W_S$; and a margin $\ell_n$. The summation over models costs nothing: the prior masses $p(S)$ sum to one, so no multiplicity enters at this step. With $d=m_n=O((s_0+1)\ell_n)$ the threshold is $O((s_0+1)\ell_n^2)=O(n\varepsilon_n^2)$, and the factor $\ell_n^2$ (rather than $\ell_n$) is entirely due to $d$, as the prover note anticipated.

*Remark 3.2 (no comparison with $S\cup S_0$).* The comparison is made directly with $S_0$, which is possible here because the quantity controlled is $a_S$ itself: a model with large $a_S$ fits worse than $S_0$ by at least $a_S/2$ minus noise terms, whatever its support. The cross term $W_S$ is absorbed into $a_S/2$ by the arithmetic–geometric mean inequality, which is exactly what makes a beta-min condition unnecessary (a weak true variable missed by $S$ costs $S$ little in $a_S$, and the posterior is allowed to miss it).

---


## 4. The master theorem: contraction given a dimension bound

For an integer $d\ge0$ put
$$
L(d):=(d+s_0+1)\,\ell_n,\qquad \mathcal G(d):=\{S:\ |S|\le d,\ a_S\le\rho(d)\},\qquad r_n(d,u):=\frac{L(d)}{n}+\frac{u}{\sqrt n}\quad(u\ge1),
$$
with $\rho(d)\le C_aL(d)$ from (3.1), and for $u\ge1$ the event $\mathcal E_4(u):=\{|E-n|\le u\sqrt{2n}\}$, which by Chebyshev has $\mathbb P_0(\mathcal E_4(u)^c)\le u^{-2}$.

**Theorem 5 (master theorem).** Let $n\ge4$, $p\ge1$, $k_{\max}\ge s_0$, and let $X$, $\beta^\star$, $\sigma_\star^2>0$ be arbitrary with $\|\mu\|^2/n\le M$ and $\delta<\infty$ as in (0.3). Put
$$
C_b:=2C_a+28\sigma_\star^2,\qquad C_f:=2C_b+2,\qquad C_c:=3C_a+16\sigma_\star^2,\qquad C_d:=\frac{2b_0+2a_0\sigma_\star^2+C_c}{\sigma_\star^2}+\sqrt2,\qquad C_e:=2C_d+2\sqrt2 .
$$
Then for every integer $d\ge0$:

(i) on $\Omega_n$,
$$
\Pi\Big(\|X_S\beta_S-\mu\|^2>C_f\,L(d)\ \Big|\ y\Big)\ \le\ \Pi(|S|>d\mid y)+e^{-\ell_n}+\frac{2B}{\ell_n};
$$

(ii) for every $u\in[1,\sqrt{n/8}]$, on $\Omega_n\cap\mathcal E_4(u)$,
$$
\Pi\Big(\Big|\frac{\sigma^2}{\sigma_\star^2}-1\Big|>C_e\,r_n(d,u)\ \Big|\ y\Big)\ \le\ \Pi(|S|>d\mid y)+e^{-\ell_n}+\frac1{u^2}.
$$

Here $\mathbb P_0(\Omega_n^c)\le7/n$ and $\mathbb P_0((\Omega_n\cap\mathcal E_4(u))^c)\le7/n+u^{-2}$ (Lemma 3), free of $p$, $d$, the design, $\beta^\star$ and the cap. The constants $C_a,\dots,C_e$ depend only on $(\sigma_\star^2,M,\delta,a_0,b_0)$ and are nondecreasing in $\delta$. *They may be evaluated at any $\delta'\ge\delta$, in particular at $\bar\delta$ under the standing assumptions:* (3.2) holds for every $C_1\ge22\sigma_\star^2+2\delta$, Proposition 4 and this theorem use $\rho(d)$ only through its definition (3.1), and their conclusions are monotone in the thresholds $C_fL(d)$ and $C_er_n(d,u)$; so every statement remains true with the constants computed from $\delta'$. At $\delta'=\bar\delta$ they depend only on $(\sigma_\star^2,M,\varphi_0,a_0,b_0)$.

*Proof.* Throughout we work on $\Omega_n$ (and on $\mathcal E_4(u)$ in (ii)) and with $S\in\mathcal G(d)$; write $k=|S|\le d$. By Proposition 4,
$$
\Pi(\mathcal G(d)^c\mid y)\le\Pi(|S|>d\mid y)+\Pi(\mathcal B(d)\mid y)\le\Pi(|S|>d\mid y)+e^{-\ell_n}. \tag{4.1}
$$

*(i).* By (1.2), Lemma 3 ($\mathcal E_2$) and $a_S\le\rho(d)\le C_aL(d)$,
$$
\|M_Sy-\mu\|^2\le2a_S+2\|P_S\varepsilon\|^2\le2C_aL(d)+28\sigma_\star^2k\ell_n\le C_bL(d),
$$
so that $\|X_S\beta_S-\mu\|^2\le2\|X_S\beta_S-M_Sy\|^2+2C_bL(d)$ and therefore
$$
\{\|X_S\beta_S-\mu\|^2>C_fL(d)\}\cap\{S\in\mathcal G(d)\}\subseteq\{\|X_S\beta_S-M_Sy\|^2>L(d)\}\cap\{S\in\mathcal G(d)\}.
$$
For fixed $S\in\mathcal G(d)$, by Lemma 1(f) and Markov's inequality conditionally on $(\sigma^2,S,y)$, then integrating over $\sigma^2\mid S,y$,
$$
\Pi\big(\|X_S\beta_S-M_Sy\|^2>L(d)\ \big|\ S,y\big)\le\frac{\mathbb E[\sigma^2\mid S,y]\operatorname{tr}M_S}{L(d)}\le\frac{k}{L(d)}\cdot\frac{2b_0+Q_S}{n+2a_0-2}\le\frac{d}{(d+s_0+1)\ell_n}\cdot\frac{nB}{n-2}\le\frac{2B}{\ell_n},
$$
using $\nu>1$ (as $n\ge4$), (2.1), and $n/(n-2)\le2$ for $n\ge4$. Summing against $\pi(S)$ over $S\in\mathcal G(d)$ and adding (4.1) gives (i).

*(ii).* For $S\in\mathcal G(d)$, by (1.1), Lemma 3 ($\mathcal E_2,\mathcal E_3$), $a_S\le\rho(d)$ and the inequality $4\sqrt{xy}\le2x+2y$,
$$
|Q_S-\sigma_\star^2E|\le\rho(d)+4\sigma_\star\sqrt{\rho(d)(k+1)\ell_n}+14\sigma_\star^2k\ell_n\le3\rho(d)+2\sigma_\star^2(k+1)\ell_n+14\sigma_\star^2k\ell_n\le\big(3C_a+16\sigma_\star^2\big)L(d)=C_cL(d).
$$
Put $x_S:=\dfrac{2b_0+Q_S}{2\nu\sigma_\star^2}=\dfrac{2b_0+Q_S}{(n+2a_0)\sigma_\star^2}$. On $\mathcal E_4(u)$,
$$
|x_S-1|=\frac{|2b_0+Q_S-(n+2a_0)\sigma_\star^2|}{(n+2a_0)\sigma_\star^2}\le\frac{2b_0+2a_0\sigma_\star^2+|Q_S-\sigma_\star^2E|+\sigma_\star^2|E-n|}{n\sigma_\star^2}\le\frac{2b_0+2a_0\sigma_\star^2}{\sigma_\star^2}\cdot\frac1n+\frac{C_c}{\sigma_\star^2}\cdot\frac{L(d)}n+\frac{\sqrt2\,u}{\sqrt n}\le C_d\,r_n(d,u),
$$
since $\frac1n\le\frac u{\sqrt n}\le r_n(d,u)$ for $u\ge1$.

Under $\Pi(\cdot\mid S,y)$, by (0.2), $G:=\frac{2b_0+Q_S}{2\sigma^2}\sim\mathrm{Gamma}(\nu,1)$, so that
$$
\frac{\sigma^2}{\sigma_\star^2}=\frac{2b_0+Q_S}{2\nu\sigma_\star^2}\cdot\frac{\nu}{G}=x_S\cdot\frac\nu G,\qquad \mathbb E[G\mid S,y]=\nu,\quad \mathrm{Var}(G\mid S,y)=\nu .
$$
By Chebyshev, $\Pi(|G-\nu|>u\sqrt\nu\mid S,y)\le u^{-2}$. On $\{|G-\nu|\le u\sqrt\nu\}$: since $\nu\ge n/2$ and $u\le\sqrt{n/8}\le\sqrt\nu/2$, we have $G\ge\nu-u\sqrt\nu\ge\nu/2$, hence
$$
\Big|\frac\nu G-1\Big|=\frac{|\nu-G|}{G}\le\frac{u\sqrt\nu}{\nu/2}=\frac{2u}{\sqrt\nu}\le\frac{2\sqrt2\,u}{\sqrt n}\le1 .
$$
For reals $x,g$ with $|g-1|\le1$, $|xg-1|\le|x-1|\,g+|g-1|\le2|x-1|+|g-1|$. Therefore, on $\{|G-\nu|\le u\sqrt\nu\}$,
$$
\Big|\frac{\sigma^2}{\sigma_\star^2}-1\Big|\le2C_dr_n(d,u)+\frac{2\sqrt2\,u}{\sqrt n}\le\big(2C_d+2\sqrt2\big)r_n(d,u)=C_er_n(d,u).
$$
Hence $\Pi\big(|\sigma^2/\sigma_\star^2-1|>C_er_n(d,u)\ \big|\ S,y\big)\le u^{-2}$ for every $S\in\mathcal G(d)$; summing against $\pi(S)$ and adding (4.1) gives (ii).

*Dependence of the constants.* $B$ and $c_0$ depend on $(b_0,M,\sigma_\star^2)$; $C_1$ on $(\sigma_\star^2,\delta)$; $C_a=8/c_0+2C_1$; $C_b,C_c$ on $(C_a,\sigma_\star^2)$; $C_d$ additionally on $(a_0,b_0)$; all are nondecreasing in $\delta$. $\blacksquare$

*Remark 4.1 (uniformity).* Theorem 5 is a statement about every $n\ge4$, with explicit exceptional probabilities. In (i) and (ii) nothing depends on $p$ except through $\ell_n$, nothing on the design and $\beta^\star$ except through $\delta$ and $M$, and nothing on the cap except through $s_0\le k_{\max}$. This is what allows the conditional application to a random design in Section 7.

---

## 5. Proofs of Theorem T9 and of the implication in Corollary T9a(iii)

Throughout this section the constants of Theorem 5 are evaluated at $\delta'=\bar\delta$, which is legitimate under the standing assumptions (Theorem 5, last paragraph), so that they depend only on $(\sigma_\star^2,M,\varphi_0,a_0,b_0)$.

**Proof of Theorem T9.** Take $d=m_n$ as in (0.5). By (0.7),
$$
L(m_n)=(m_n+s_0+1)\ell_n\le\big(4(s_0+1)\ell_n+(s_0+1)\big)\ell_n\le5(s_0+1)\ell_n^2=5n\varepsilon_n^2 . \tag{5.1}
$$
Let $F_n:=\{\Pi(|S|>m_n\mid y)\le2e^{K_\star}e^{-\omega_n/2}\}$; by (0.6), $\mathbb P_0(F_n^c)\le q_n^D\to0$.

*(i).* By Theorem 5(i) with $d=m_n$ and (5.1), on $\Omega_n\cap F_n$,
$$
\Pi\Big(\frac{\|X_S\beta_S-\mu\|^2}{n}>5C_f\,\varepsilon_n^2\ \Big|\ y\Big)\le2e^{K_\star}e^{-\omega_n/2}+e^{-\ell_n}+\frac{2B}{\ell_n}=:\eta^{(i)}_n\longrightarrow0 .
$$
Let $\eta>0$ and let $n_0=n_0(\eta;\sigma_\star^2,M,\varphi_0,a_0,b_0,s_0,(\omega_n))$ be such that $\eta^{(i)}_n\le\eta$ for $n\ge n_0$. Then for $n\ge n_0$,
$$
\mathbb P_0\Big(\Pi\big(\|X_S\beta_S-\mu\|^2/n>5C_f\varepsilon_n^2\ \big|\ y\big)>\eta\Big)\le\mathbb P_0(\Omega_n^c)+\mathbb P_0(F_n^c)\le\frac7n+q_n^D\longrightarrow0 . \tag{5.2}
$$
This is (i) with $C=5C_f$. Note that $\ell_n^2=o(n)$ has not been used: (i) holds for every sequence $p=p_n$.

*(ii).* Put $u_n:=\sqrt{s_0+1}\,\ell_n=\varepsilon_n\sqrt n$. Then $u_n\ge\ell_n\ge1$, and $u_n\le\sqrt{n/8}$ if and only if $\varepsilon_n^2\le1/8$, which holds for all large $n$ because $\varepsilon_n^2=(s_0+1)\ell_n^2/n\to0$ under $\ell_n^2=o(n)$ with $s_0$ fixed. For such $n$, by (5.1), $r_n(m_n,u_n)\le5\varepsilon_n^2+\varepsilon_n\le6\varepsilon_n$ (as $\varepsilon_n\le1$), and Theorem 5(ii) gives, on $\Omega_n\cap\mathcal E_4(u_n)\cap F_n$,
$$
\Pi\Big(\Big|\frac{\sigma^2}{\sigma_\star^2}-1\Big|>6C_e\,\varepsilon_n\ \Big|\ y\Big)\le2e^{K_\star}e^{-\omega_n/2}+e^{-\ell_n}+\frac1{(s_0+1)\ell_n^2}=:\eta^{(ii)}_n\longrightarrow0 .
$$
Hence, for every $\eta>0$ and all $n$ large enough that $\varepsilon_n^2\le1/8$ and $\eta^{(ii)}_n\le\eta$,
$$
\mathbb P_0\Big(\Pi\big(|\sigma^2/\sigma_\star^2-1|>6C_e\varepsilon_n\ \big|\ y\big)>\eta\Big)\le\frac7n+\frac1{(s_0+1)\ell_n^2}+q_n^D\longrightarrow0 . \tag{5.3}
$$
This is (ii) with $C=6C_e$. Taking $C:=\max\{5C_f,6C_e\}$ proves Theorem T9. $\blacksquare$

**Corollary 5.1 (the sharper form of T9(ii)).** Under the standing assumptions *without* $\ell_n^2=o(n)$, for every sequence $(u_n)$ with $u_n\to\infty$ and $1\le u_n\le\sqrt{n/8}$,
$$
\Pi\Big(\Big|\frac{\sigma^2}{\sigma_\star^2}-1\Big|>C_e\big(5\varepsilon_n^2+u_nn^{-1/2}\big)\ \Big|\ y\Big)\longrightarrow0\quad\text{in }\mathbb P_0\text{-probability}.
$$
(Any sequence $u_n\to\infty$ may be used after replacing it by $\min\{u_n,\sqrt{n/8}\}$, which still tends to infinity and only shrinks the threshold.)

*Proof.* Theorem 5(ii) with $d=m_n$, (5.1) and $F_n$, exactly as in (5.3): the posterior probability is at most $2e^{K_\star}e^{-\omega_n/2}+e^{-\ell_n}+u_n^{-2}\to0$ outside an event of probability at most $7/n+u_n^{-2}+q_n^D\to0$. $\blacksquare$

So the proof gives the rate $\varepsilon_n^2+n^{-1/2}$ conjectured in the prover note, with a factor $u_n\to\infty$ (arbitrarily slow) in front of $n^{-1/2}$; Remark 6.2 shows that this factor cannot be dropped. The hypothesis $\ell_n^2=o(n)$ is used in T9 only to pass from $5\varepsilon_n^2+\varepsilon_n$ to $6\varepsilon_n$ and to make $u_n=\varepsilon_n\sqrt n$ admissible; nothing is needed for Corollary 5.1.

**Proof of the implication in Corollary T9a(iii).** Suppose $\Pi(|S|>C_1'(s_0+1)\mid y)\to0$ in $\mathbb P_0$-probability for some constant $C_1'\ge0$. Put
$$
d_n^\flat:=\lceil C_1'(s_0+1)\rceil,\qquad \bar\varepsilon_n^2:=\frac{(s_0+1)\ell_n}{n}.
$$
Then $d_n^\flat+s_0+1\le(C_1'+2)(s_0+1)$, so $L(d_n^\flat)\le(C_1'+2)(s_0+1)\ell_n=(C_1'+2)\,n\bar\varepsilon_n^2$, and $\Pi(|S|>d_n^\flat\mid y)\le\Pi(|S|>C_1'(s_0+1)\mid y)\to0$ in probability.

*(i), no growth condition on $p$.* By Theorem 5(i) with $d=d_n^\flat$, on $\Omega_n$,
$$
\Pi\Big(\frac{\|X_S\beta_S-\mu\|^2}n>C_f(C_1'+2)\,\bar\varepsilon_n^2\ \Big|\ y\Big)\le\Pi(|S|>d_n^\flat\mid y)+e^{-\ell_n}+\frac{2B}{\ell_n}.
$$
Let $\eta>0$ and let $n$ be so large that $e^{-\ell_n}+2B/\ell_n\le\eta/2$. On $\Omega_n\cap\{\Pi(|S|>d_n^\flat\mid y)\le\eta/2\}$ the left side is at most $\eta$, so
$$
\mathbb P_0\Big(\Pi\big(\|X_S\beta_S-\mu\|^2/n>C_f(C_1'+2)\bar\varepsilon_n^2\ \big|\ y\big)>\eta\Big)\le\frac7n+\mathbb P_0\big(\Pi(|S|>d_n^\flat\mid y)>\eta/2\big)\longrightarrow0 .
$$

*(ii), under $\ell_n=o(n)$.* Put $u_n:=\bar\varepsilon_n\sqrt n=\sqrt{(s_0+1)\ell_n}\ge1$. Since $\ell_n=o(n)$ and $s_0$ is fixed, $\bar\varepsilon_n\to0$, so for all large $n$ both $u_n\le\sqrt{n/8}$ and $\bar\varepsilon_n\le1$ hold, and then $r_n(d_n^\flat,u_n)\le(C_1'+2)\bar\varepsilon_n^2+\bar\varepsilon_n\le(C_1'+3)\bar\varepsilon_n$. Theorem 5(ii) gives, on $\Omega_n\cap\mathcal E_4(u_n)$,
$$
\Pi\Big(\Big|\frac{\sigma^2}{\sigma_\star^2}-1\Big|>C_e(C_1'+3)\,\bar\varepsilon_n\ \Big|\ y\Big)\le\Pi(|S|>d_n^\flat\mid y)+e^{-\ell_n}+\frac1{(s_0+1)\ell_n},
$$
and, for $\eta>0$ and $n$ so large that $e^{-\ell_n}+1/((s_0+1)\ell_n)\le\eta/2$,
$$
\mathbb P_0\Big(\Pi\big(|\sigma^2/\sigma_\star^2-1|>C_e(C_1'+3)\bar\varepsilon_n\ \big|\ y\big)>\eta\Big)\le\frac7n+\frac1{(s_0+1)\ell_n}+\mathbb P_0\big(\Pi(|S|>d_n^\flat\mid y)>\eta/2\big)\longrightarrow0 .
$$

Hence T9 holds with $\varepsilon_n$ replaced by $\bar\varepsilon_n$ and with the constant $\max\{C_f(C_1'+2),\,C_e(C_1'+3)\}$, which depends on $(\sigma_\star^2,M,\varphi_0,a_0,b_0)$ and on $C_1'$. Part (i) of the conclusion needs no growth condition on $p$; part (ii) needs $\ell_n=o(n)$ (weaker than T9's $\ell_n^2=o(n)$, and necessary for the next sentence to have content). For $\log p\asymp n^\alpha$ with $0<\alpha<1$, $\ell_n=o(n)$ and $\bar\varepsilon_n^2\asymp(s_0+1)n^{\alpha-1}\to0$, so the rate statement T9a(ii) extends to this range, as the corollary asserts. $\blacksquare$

The hypothesis of this implication is proved in Section 9 for polynomial $p$ under additional conditions.

---

## 6. Remarks

**6.1 Where each hypothesis is used.**
- $\|\mu\|^2/n\le M$: in (2.1), through $B$ (the scale of $2b_0+Q_S$), and in $\bar\delta$.
- $\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2$: only to bound $\delta\le\bar\delta$ in (0.3) (and inside Fact D, for the same purpose). No eigenvalue condition on any other model is used in Sections 1 to 6: for $S\ne S_0$ the Occam factor is bounded by $D_S\ge1$, and the fit by $a_S$, both of which need nothing from the design. (Sections 7 and 9 are different: Section 7 uses (R4) on all supports of size at most $\bar d_n$, Section 9 uses (SE).)
- The cap: only $s_0\le k_{\max}$, so that $p(S_0)>0$ and L6(v) applies.
- $p$: only through $\ell_n$ in the union bounds (Lemma 3) and the prior mass of $S_0$ (Step 4 of Proposition 4). No comparison of $p$ with $n$ is made; Fact D holds for every $p$ (Corollary T9a(i)).
- $\ell_n^2=o(n)$: only at the end of the proof of T9(ii), to replace $5\varepsilon_n^2+\varepsilon_n$ by $6\varepsilon_n$ and to make $u_n=\varepsilon_n\sqrt n\le\sqrt{n/8}$. T9(i) and Corollary 5.1 do not use it.
- $s_0$ fixed: through the constant $K_\star$ of Fact D (which depends on $s_0$) and through "$n$ large" in (5.2), (5.3) and in the T9a(iii) implication, where $\varepsilon_n\to0$ and $\bar\varepsilon_n\to0$ use it. The constant $C$ of T9 is free of $s_0$; $s_0$ enters the bounds of Theorem 5 only through $L(d)=(d+s_0+1)\ell_n$, i.e. through the factor $(s_0+1)$ already present in $\varepsilon_n^2$.
- No beta-min condition and no condition on the design beyond the standing ones (Remark 3.2).

**6.2 The $n^{-1/2}$ term in (ii) is genuine (a model-free statement).** For $c>0$ and $x>0$ let $G\sim\mathrm{Gamma}(\nu,1)$ and
$$
\pi_n(x,c):=\mathbb P\Big(\Big|x\frac\nu G-1\Big|\le\frac{c}{\sqrt n}\Big),\qquad \bar\pi_n(c):=\sup_{x>0}\pi_n(x,c).
$$
*Claim.* For every $c>0$, $\limsup_{n\to\infty}\bar\pi_n(c)\le\max\{2\phi(1),\ \mathbb P(|N(0,2)|\le c)\}<1$, where $\phi$ is the standard normal density ($2\phi(1)\approx0.484$).

*Consequence.* For every $y$, every design and every $n$: under $\Pi(\cdot\mid S,y)$, $\sigma^2/\sigma_\star^2=x_S\,\nu/G$ with $x_S=(2b_0+Q_S)/(2\nu\sigma_\star^2)>0$ deterministic given $y$ (proof of Theorem 5(ii)), so $\Pi(|\sigma^2/\sigma_\star^2-1|\le cn^{-1/2}\mid S,y)=\pi_n(x_S,c)\le\bar\pi_n(c)$, and after mixing over $S$,
$$
\Pi\big(|\sigma^2/\sigma_\star^2-1|>c\,n^{-1/2}\ \big|\ y\big)\ \ge\ 1-\bar\pi_n(c)\qquad\text{for every }y .
$$
By the claim, the right side is bounded below by a positive constant for all large $n$. So no threshold of the form $c\,n^{-1/2}$ with a fixed $c$ can make the posterior probability in T9(ii) tend to zero, for any design; the factor $u_n\to\infty$ in Corollary 5.1 is necessary. (The sharpness statement has content only when $\varepsilon_n^2=O(n^{-1/2})$, i.e. $(s_0+1)\ell_n^2=O(\sqrt n)$; otherwise the term $\varepsilon_n^2$ dominates.)

*Proof of the claim.* Write $Z_n:=(G-\nu)/\sqrt\nu$. The law $\mathrm{Gamma}(\nu,1)$ is that of a sum of $\lfloor\nu\rfloor$ i.i.d. standard exponential variables plus, when $\nu\notin\mathbb N$, an independent $\mathrm{Gamma}(\nu-\lfloor\nu\rfloor,1)$ variable; since $\nu\to\infty$, the central limit theorem gives $Z_n\Rightarrow N(0,1)$ (the fractional part contributes $O_{\mathbb P}(1)/\sqrt\nu\to0$), and since the limit has a continuous distribution function, the convergence is uniform (Pólya's theorem): $\Delta_n:=\sup_{t\in\mathbb R}|\mathbb P(Z_n\le t)-\Phi(t)|\to0$. Let $n$ be so large that $c/\sqrt n\le\frac12$.

*Case $x\ge2$.* If $|x\nu/G-1|\le c/\sqrt n$ then $\nu/G\le(1+c/\sqrt n)/x\le\frac34$, i.e. $G\ge\frac43\nu$, so $\pi_n(x,c)\le\mathbb P(G-\nu\ge\nu/3)\le9/\nu$ by Chebyshev. Hence $\sup_{x\ge2}\pi_n(x,c)\to0$.

*Case $0<x<2$.* The event $\{|x\nu/G-1|\le c/\sqrt n\}$ is $\{G\in[a_x,b_x]\}$ with $a_x=x\nu/(1+c/\sqrt n)$, $b_x=x\nu/(1-c/\sqrt n)$, i.e. $\{Z_n\in J_x\}$ with $J_x:=[(a_x-\nu)/\sqrt\nu,(b_x-\nu)/\sqrt\nu]$, an interval with midpoint and half-length
$$
\mathsf m_x=\sqrt\nu\Big(\frac{x}{1-c^2/n}-1\Big),\qquad \mathsf h_x=\frac{x\,c\sqrt{\nu/n}}{1-c^2/n}\ \le\ \frac{2c\sqrt{\nu/n}}{1-c^2/n}=:\bar{\mathsf h}_n\longrightarrow\sqrt2\,c
$$
(using $a_x+b_x=2x\nu/(1-c^2/n)$ and $b_x-a_x=2x\nu(c/\sqrt n)/(1-c^2/n)$). Then $\pi_n(x,c)\le\mathbb P(N\in J_x)+2\Delta_n$ with $N\sim N(0,1)$, and for an interval with midpoint $\mathsf m$ and half-length $\mathsf h$,
$$
\mathbb P(N\in[\mathsf m-\mathsf h,\mathsf m+\mathsf h])\le\min\Big\{2\mathsf h\,\phi\big((|\mathsf m|-\mathsf h)_+\big),\ \mathbb P(|N|\le\mathsf h)\Big\}
$$
(the first bound because $\phi$ is maximal, on the interval, at the point closest to $0$; the second because, among intervals of a given length, the centred one has the largest Gaussian probability). If $|\mathsf m_x|\ge2\mathsf h_x$, the first bound gives $\pi_n(x,c)\le2\mathsf h_x\phi(\mathsf h_x)+2\Delta_n\le2\phi(1)+2\Delta_n$, since $\sup_{t>0}2t\phi(t)=2\phi(1)$. If $|\mathsf m_x|<2\mathsf h_x\le2\bar{\mathsf h}_n$, then $|x/(1-c^2/n)-1|<2\bar{\mathsf h}_n/\sqrt\nu\to0$, so such $x$ satisfy $|x-1|\le\gamma_n$ for a sequence $\gamma_n\to0$ not depending on $x$, whence $\mathsf h_x\le\frac{(1+\gamma_n)c\sqrt{\nu/n}}{1-c^2/n}\to c/\sqrt2$, and the second bound gives $\pi_n(x,c)\le\mathbb P(|N|\le\mathsf h_x)+2\Delta_n\le\mathbb P\big(|N|\le\tfrac{(1+\gamma_n)c\sqrt{\nu/n}}{1-c^2/n}\big)+2\Delta_n\to\mathbb P(|N|\le c/\sqrt2)=\mathbb P(|N(0,2)|\le c)$. Combining the two cases, $\limsup_n\bar\pi_n(c)\le\max\{2\phi(1),\mathbb P(|N(0,2)|\le c)\}$, and both numbers are $<1$. $\blacksquare$

(The sup in the claim was also computed numerically by a round-1 reviewer, `review/round1/check_opus_C3.py`: for $n$ from $10^2$ to $10^6$ it equals $\mathbb P(|N(0,2)|\le c)$ to four digits. This remark is not used elsewhere.)

**6.3 On the sharp dimension bound (the hypothesis of T9a(iii)).** The route of T6 cannot give $\Pi(|S|>C(s_0+1)\mid y)\to0$: its numerator bound is in $\mathbb P_0$-expectation, and $\mathbb E_0[m(S)/f_0(y)]=1$ for every $S$, whereas for a typical $y$ and a well-conditioned superset $S=S_0\cup J$, $|J|=j$, the ratio $m(S)/m(S_0)$ is of order $n^{-j/2}e^{\chi^2_j/2}$; the expectation is carried by rare $y$. A sharp bound must work with typical values of the Bayes factors, which is what Section 9 does: supersets of $S_0$ are summed in expectation after truncation on the uniform noise event of Lemma 3 (Lemma 11, Proposition 12), and an arbitrary model $S$ is compared with $S\cup S_0$ (Lemma 10). For $p\le n^A$, under T7's sparse eigenvalue condition, column standardisation and a cap of at least $m_n+s_0$, this gives $\Pi(|S|>s_0+\lceil s_0(2A+1)\rceil\mid y)\to0$ (Theorem 13) and hence Corollary T9a(iii) in that regime (Corollary 14). For super-polynomial $p$ the argument of Section 9 does not apply as written (Remark 9.1), and the sharp dimension bound, and with it the sharp rate for $\log p\asymp n^\alpha$ with $\alpha\ge\frac12$, remain open.

**6.4 The Markov step.** The term $2B/\ell_n$ in Theorem 5(i) comes from a Markov inequality for the conditional posterior spread $\|X_S(\beta_S-\hat\beta_S)\|^2$; it decays slowly, but T9 asserts only convergence to $0$, and no sharpening is claimed here.

---

## 7. Corollary C9: random design, Hellinger contraction

### 7.1 Setting and statement

Let $x_1,\dots,x_n$ be i.i.d. random vectors in $\mathbb R^p$ ($p=p_n$), independent of $\varepsilon\sim N_n(0,\sigma_\star^2I_n)$, and let $X$ be the $n\times p$ matrix with rows $x_i^\top$, so that $y=X\beta^\star+\varepsilon$, i.e. $y_i=x_i^\top\beta^\star+\varepsilon_i$. We assume:

- (R1) *Centred rows.* $\mathbb Ex_i=0$ and $\Sigma_x:=\mathbb E[x_ix_i^\top]$ (the covariance matrix) is finite. **This hypothesis is not in the frozen statement of C9 and is a correction of it:** without it, and without a raw sub-Gaussian constant uniform in $n$, the frozen C9 is false (Remark 7.3). *(audit 2026-10-15)* The counterexample violates (R2) as well, so it does not show that centring alone is needed once (R2) is kept; that question is open (Remark 7.3).
- (R2) *Sub-Gaussian rows, uniformly in $n$.* There is a constant $\varsigma<\infty$, not depending on $n$, such that for every $n$ and every $v\in\mathbb R^{p_n}$, $\|v^\top x_i\|_{\psi_2}\le\varsigma\|v\|_2$, where $\|\xi\|_{\psi_2}:=\inf\{t>0:\mathbb E\exp(\xi^2/t^2)\le2\}$. (The frozen statement says "sub-Gaussian"; the uniformity in $n$ is the standard reading and is what the uniform Gram-concentration argument of Lemma 7 uses, Remark 7.4; whether it is necessary for the contraction conclusion itself is not established, audit 2026-10-15.)
- (R3) $s_0$ fixed, $\beta^{\star\top}\Sigma_x\beta^\star\le M/2$, and $\ell_n^2=o(n)$. The prior is $\mathrm{BB}(1,p)$ with any cap $k_{\max}\ge s_0$.
- (R4) *Sparse eigenvalues.* With $m_n$ as in (0.5) (T6's cutoff, for the fixed admissible sequence $\omega_n$) and $\bar d_n:=m_n+s_0$ ($\ge1$ for all large $n$; see Section 0), $\kappa\le\lambda_{\min}(\Sigma_{x,TT})\le\lambda_{\max}(\Sigma_{x,TT})\le K$ for all $T\subseteq[p]$ with $1\le|T|\le\bar d_n$, where $0<\kappa\le K<\infty$ are fixed.

*The posterior and its two conventions.* Let $\mathrm R=\operatorname{diag}(r_1,\dots,r_p)$ with $r_j>0$ and $\tilde X:=X\mathrm R^{-1}$. The posterior $\Pi(\cdot\mid y,X)$ is the joint posterior (0.2) of the draft computed with the design matrix $\tilde X$ in place of $X$; its parameter is $\theta=(S,\tilde\beta_S,\sigma^2)$, and the regression coefficient vector it represents is $\beta=\beta(\theta)\in\mathbb R^p$ with $\beta_S=\mathrm R_S^{-1}\tilde\beta_S$ and $\beta_j=0$ for $j\notin S$ ($\mathrm R_S$ the $S$-block of $\mathrm R$), so that $x^\top\beta=(\mathrm R^{-1}x)^\top\tilde\beta$ and $\tilde X_S\tilde\beta_S=X_S\beta_S$. Two cases are covered:

- *raw design:* $\mathrm R=I_p$;
- *standardised design:* $r_j:=\|x_j\|/\sqrt n$ if $x_j\ne0$ and $r_j:=1$ if $x_j=0$, so that $\|\tilde x_j\|^2=n$ for every nonzero column (the draft's convention). The convention $r_j=1$ for a zero column makes the posterior defined for every $X$; on the good design event of Section 7.4 every column is nonzero, so the convention is never active there.

Write $\tilde\beta^\star:=\mathrm R\beta^\star$; then $\operatorname{supp}\tilde\beta^\star=S_0$ and $\tilde X\tilde\beta^\star=X\beta^\star=\mu$.

*Densities and Hellinger distance.* Let $P_X$ be the law of $x_i$. For $\theta$ with coefficient vector $\beta$ and variance $\sigma^2$, $f_\theta(x,y):=\phi_\sigma(y-x^\top\beta)$ is the density of $(x_i,y_i)$ with respect to $P_X\otimes\mathrm{Leb}$ under the model $(\beta,\sigma^2)$, where $\phi_\sigma$ is the $N(0,\sigma^2)$ density; $f_{\theta^\star}$ is the true density, with $(\beta^\star,\sigma_\star^2)$. (If $P_X$ has a density $p_X$, this is the draft's $f_\theta(x,y)=p_X(x)\phi_\sigma(y-x^\top\beta)$ up to the choice of reference measure, which does not affect the Hellinger distance. Under the standardised convention, $f_\theta$ is formed with the raw-scale coefficient vector $\beta(\theta)$; this is the only meaningful reading, since $\mathrm R$ depends on the sample.) $h^2(f,g):=1-\int\sqrt{fg}\,d(P_X\otimes\mathrm{Leb})$.

**Corollary C9 (as proved here).** Under (R1) to (R4), for each of the two conventions, there is a constant $C$ depending only on $(\sigma_\star^2,M,\kappa,K,a_0,b_0)$ (on $K$ only in the standardised case) such that
$$
\Pi\big(h(f_\theta,f_{\theta^\star})>C\varepsilon_n\ \big|\ y,X\big)\longrightarrow0\qquad\text{in probability over }(X,\varepsilon).
$$

### 7.2 The Hellinger distance between two Gaussian regressions

**Lemma 6.** For every $\beta\in\mathbb R^p$ and $\sigma^2>0$, with $\theta$ the corresponding parameter,
$$
h^2(f_\theta,f_{\theta^\star})\ \le\ \Big(\frac{\sigma^2}{\sigma_\star^2}-1\Big)^2+\frac{(\beta-\beta^\star)^\top\Sigma_x(\beta-\beta^\star)}{4\sigma_\star^2} .
$$
(Only $\Sigma_x=\mathbb E[x_ix_i^\top]$ is used; for uncentred rows the same bound holds with the second-moment matrix in place of the covariance.)

*Proof.* For two normal densities with means $m_1,m_2$ and variances $s_1^2,s_2^2$,
$$
\int\sqrt{\phi_{s_1}(y-m_1)\phi_{s_2}(y-m_2)}\,dy=\sqrt{\frac{2s_1s_2}{s_1^2+s_2^2}}\exp\Big(-\frac{(m_1-m_2)^2}{4(s_1^2+s_2^2)}\Big). \tag{7.1}
$$
Indeed $\sqrt{\phi_{s_1}(y-m_1)\phi_{s_2}(y-m_2)}=(2\pi s_1s_2)^{-1/2}\exp\{-q(y)\}$ with $q(y):=\frac{(y-m_1)^2}{4s_1^2}+\frac{(y-m_2)^2}{4s_2^2}$, a convex quadratic in $y$ with leading coefficient $\frac{s_1^2+s_2^2}{4s_1^2s_2^2}$ and minimum value $\min_yq(y)=\frac{(m_1-m_2)^2}{4(s_1^2+s_2^2)}$ (for $A,B>0$, $\min_y\{\frac{(y-a)^2}A+\frac{(y-b)^2}B\}=\frac{(a-b)^2}{A+B}$, with $A=4s_1^2$, $B=4s_2^2$). Hence $\int e^{-q}=\sqrt{\pi\cdot4s_1^2s_2^2/(s_1^2+s_2^2)}\,e^{-\min q}$, and the integral in (7.1) equals $(2\pi s_1s_2)^{-1/2}\sqrt{4\pi s_1^2s_2^2/(s_1^2+s_2^2)}\,e^{-(m_1-m_2)^2/(4(s_1^2+s_2^2))}$, which is (7.1).

Apply (7.1) with $m_1=x^\top\beta$, $m_2=x^\top\beta^\star$, $s_1=\sigma$, $s_2=\sigma_\star$, and integrate over $x\sim P_X$:
$$
\int\sqrt{f_\theta f_{\theta^\star}}\,d(P_X\otimes\mathrm{Leb})=\alpha\,\mathbb E_x\big[e^{-Z(x)}\big],\qquad \alpha:=\sqrt{\frac{2\sigma\sigma_\star}{\sigma^2+\sigma_\star^2}}\in(0,1],\quad Z(x):=\frac{(x^\top(\beta-\beta^\star))^2}{4(\sigma^2+\sigma_\star^2)}\ge0 .
$$
With $b:=\mathbb E_xe^{-Z}\in(0,1]$, $h^2=1-\alpha b=(1-\alpha)+\alpha(1-b)\le(1-\alpha)+(1-b)$. For the first term, write $\alpha=\sqrt{1-\xi}$ with $\xi=1-\frac{2\sigma\sigma_\star}{\sigma^2+\sigma_\star^2}=\frac{(\sigma-\sigma_\star)^2}{\sigma^2+\sigma_\star^2}\in[0,1)$; since $\sqrt{1-\xi}\ge1-\xi$, $1-\alpha\le\xi\le\frac{(\sigma-\sigma_\star)^2}{\sigma_\star^2}=(\sqrt r-1)^2$ with $r=\sigma^2/\sigma_\star^2$, and $|\sqrt r-1|=\frac{|r-1|}{\sqrt r+1}\le|r-1|$, so $1-\alpha\le(r-1)^2$. For the second term, $e^{-z}\ge1-z$ gives $1-b\le\mathbb E_xZ=\frac{\mathbb E_x(x^\top(\beta-\beta^\star))^2}{4(\sigma^2+\sigma_\star^2)}\le\frac{(\beta-\beta^\star)^\top\Sigma_x(\beta-\beta^\star)}{4\sigma_\star^2}$, since $\mathbb E_x(x^\top v)^2=v^\top\Sigma_xv$. $\blacksquare$

### 7.3 Uniform concentration of sparse Gram matrices

The following external result is used; it is the one place where the sub-Gaussian hypothesis enters. It was verified against the source by the researcher (`CITED_RESULTS.md`): Vershynin, *High-Dimensional Probability*, First Edition (Cambridge University Press, 2018), Theorem 4.6.1, whose proof establishes the display (4.22) below with the same probability.

**Fact G (sub-Gaussian isotropic Gram matrices; Vershynin 2018, Theorem 4.6.1 and its display (4.22); verified against the source).** Let $z_1,\dots,z_n$ be independent mean-zero random vectors in $\mathbb R^d$ with $\mathbb E[z_iz_i^\top]=I_d$ and $\sup_{\|u\|_2=1}\|u^\top z_i\|_{\psi_2}\le K_z$ for all $i$. There is an absolute constant $c_1>0$ such that for every $t\ge0$, with probability at least $1-2e^{-t^2}$,
$$
\Big\|\frac1n\sum_{i=1}^nz_iz_i^\top-I_d\Big\|_{\mathrm{op}}\le K_z^2\max(\eta,\eta^2),\qquad \eta:=c_1\Big(\sqrt{\frac dn}+\frac{t}{\sqrt n}\Big).
$$
(The source states the bound with $K=\max_i\|z_i\|_{\psi_2}$, the sub-Gaussian norm of the vector, in place of an upper bound $K_z$; since the bound is increasing in $K$, the form above follows.)

Let $\Gamma_n:=X^\top X/n$ and
$$
\Delta_n:=\max_{T\subseteq[p]:\ 1\le|T|\le\bar d_n}\big\|\Gamma_{n,TT}-\Sigma_{x,TT}\big\|_{\mathrm{op}} .
$$

**Lemma 7.** Under (R1), (R2), (R4), with probability at least $1-2/n$,
$$
\Delta_n\le\frac{K\varsigma^2}{\kappa}\max(\varrho_n,\varrho_n^2),\qquad \varrho_n:=3c_1\sqrt{\frac{\bar d_n\ell_n}{n}}\le3\sqrt5\,c_1\,\varepsilon_n .
$$
In particular, under (R3), $\mathbb P(\Delta_n>\kappa/2)\le2/n$ for all large $n$ (the threshold depending on $\varsigma,\kappa,K,c_1,s_0$ and the sequence $\ell_n^2/n$).

*Proof.* Fix $T$ with $|T|=d\in[1,\bar d_n]$. By (R4), $\Sigma_{TT}\succ0$; put $z_i:=\Sigma_{TT}^{-1/2}x_{i,T}$. Then $\mathbb Ez_i=0$ (by (R1)), $\mathbb E[z_iz_i^\top]=I_d$, and for a unit vector $u\in\mathbb R^d$, letting $v\in\mathbb R^p$ be $\Sigma_{TT}^{-1/2}u$ on $T$ and $0$ off $T$, $u^\top z_i=v^\top x_i$, so by (R2) $\|u^\top z_i\|_{\psi_2}\le\varsigma\|v\|_2=\varsigma\|\Sigma_{TT}^{-1/2}u\|_2\le\varsigma\kappa^{-1/2}$. Apply Fact G with $K_z=\varsigma\kappa^{-1/2}$ and $t=t_d:=\sqrt{d\log p+d\log2+\log n}$: with probability at least $1-2e^{-t_d^2}=1-2p^{-d}2^{-d}n^{-1}$,
$$
\Big\|\frac1n\sum_iz_iz_i^\top-I_d\Big\|\le\frac{\varsigma^2}{\kappa}\max(\eta,\eta^2),\qquad\eta=c_1\Big(\sqrt{\frac dn}+\frac{t_d}{\sqrt n}\Big)\le c_1\Big(\sqrt{\frac dn}+\sqrt{\frac{3d\ell_n}{n}}\Big)\le c_1(1+\sqrt3)\sqrt{\frac{d\ell_n}{n}}\le\varrho_n ,
$$
where $t_d^2\le d\ell_n+d\ell_n+\ell_n\le3d\ell_n$ (as $d\ge1$ and $\log2,\log p,\log n\le\ell_n$) and $\ell_n\ge1$, $d\le\bar d_n$, $1+\sqrt3<3$ were used. Since $\Gamma_{n,TT}=\frac1n\sum_ix_{i,T}x_{i,T}^\top=\Sigma_{TT}^{1/2}\big(\frac1n\sum_iz_iz_i^\top\big)\Sigma_{TT}^{1/2}$,
$$
\|\Gamma_{n,TT}-\Sigma_{TT}\|=\Big\|\Sigma_{TT}^{1/2}\Big(\frac1n\sum_iz_iz_i^\top-I_d\Big)\Sigma_{TT}^{1/2}\Big\|\le\|\Sigma_{TT}\|\cdot\frac{\varsigma^2}{\kappa}\max(\eta,\eta^2)\le\frac{K\varsigma^2}{\kappa}\max(\varrho_n,\varrho_n^2),
$$
using monotonicity of $\eta\mapsto\max(\eta,\eta^2)$. The union over all $T$ with $1\le|T|\le\bar d_n$ has probability at most $\sum_{d=1}^{\bar d_n}\binom pd\cdot2p^{-d}2^{-d}n^{-1}\le\frac2n\sum_{d\ge1}2^{-d}=\frac2n$. Finally $\bar d_n=m_n+s_0\le4(s_0+1)\ell_n+(s_0+1)\le5(s_0+1)\ell_n$ by (0.7), so $\bar d_n\ell_n/n\le5\varepsilon_n^2$; under (R3) $\varepsilon_n\to0$, so, $\varsigma,\kappa,K$ being fixed, $\frac{K\varsigma^2}{\kappa}\max(\varrho_n,\varrho_n^2)\le\kappa/2$ for all large $n$. $\blacksquare$

### 7.4 On the good design event the fixed-design hypotheses hold

Let $\mathcal D_n:=\{\Delta_n\le\kappa/2\}$.

**Lemma 8.** On $\mathcal D_n$:

(a) $\|\mu\|^2/n\le M$.

(b) *Every column satisfies* $\kappa/2\le\|x_j\|^2/n\le K+\kappa/2$; in particular no column is zero. *Raw design:* $\lambda_{\min}(\Gamma_{n,S_0S_0})\ge\kappa/2$. *Standardised design:* $r_j^2=\|x_j\|^2/n\in[\kappa/2,K+\kappa/2]$ for all $j$, and $\tilde\Gamma:=\tilde X^\top\tilde X/n=\mathrm R^{-1}\Gamma_n\mathrm R^{-1}$ satisfies $\lambda_{\min}(\tilde\Gamma_{S_0S_0})\ge\dfrac{\kappa/2}{K+\kappa/2}$.

(c) For every $v\in\mathbb R^p$ supported on a set $T$ with $|T|\le\bar d_n$: $v^\top\Sigma_xv\le2\|Xv\|^2/n$.

*Proof.* Since $\bar d_n\ge1$, (R4) applies to every singleton: $|\Gamma_{n,jj}-\Sigma_{jj}|\le\Delta_n\le\kappa/2$ with $\Sigma_{jj}\in[\kappa,K]$, hence $\|x_j\|^2/n=\Gamma_{n,jj}\in[\kappa/2,K+\kappa/2]$, which is the first part of (b) and gives $r_j^2\in[\kappa/2,K+\kappa/2]$ in the standardised case. If $s_0=0$ then $\mu=0$ and (a) and the eigenvalue parts of (b) are vacuous; so let $s_0\ge1$ for them, noting $s_0\le\bar d_n$ so that (R4) applies to $T=S_0$.

(a) $\|\mu\|^2/n=\beta^{\star\top}_{S_0}\Gamma_{n,S_0S_0}\beta^\star_{S_0}\le\beta^{\star\top}_{S_0}\Sigma_{S_0S_0}\beta^\star_{S_0}+\Delta_n\|\beta^\star_{S_0}\|^2$, and $\|\beta^\star_{S_0}\|^2\le\kappa^{-1}\beta^{\star\top}_{S_0}\Sigma_{S_0S_0}\beta^\star_{S_0}\le M/(2\kappa)$; so $\|\mu\|^2/n\le M/2+(\kappa/2)(M/(2\kappa))\le M$.

(b) Raw: by Weyl's inequality, $\lambda_{\min}(\Gamma_{n,S_0S_0})\ge\lambda_{\min}(\Sigma_{S_0S_0})-\|\Gamma_{n,S_0S_0}-\Sigma_{S_0S_0}\|\ge\kappa-\kappa/2$. Standardised: for $w\in\mathbb R^{s_0}$, $w^\top\tilde\Gamma_{S_0S_0}w=(\mathrm R_{S_0}^{-1}w)^\top\Gamma_{n,S_0S_0}(\mathrm R_{S_0}^{-1}w)\ge\frac\kappa2\|\mathrm R_{S_0}^{-1}w\|^2\ge\frac\kappa2\cdot\frac{\|w\|^2}{\max_jr_j^2}\ge\frac{\kappa/2}{K+\kappa/2}\|w\|^2$.

(c) $v^\top\Sigma_xv=v_T^\top\Sigma_{TT}v_T\le v_T^\top\Gamma_{n,TT}v_T+\Delta_n\|v_T\|^2=\|Xv\|^2/n+\Delta_n\|v_T\|^2$, and $\|v_T\|^2\le\kappa^{-1}v_T^\top\Sigma_{TT}v_T$ (if $T=\emptyset$ there is nothing to prove). Hence $(1-\Delta_n/\kappa)\,v^\top\Sigma_xv\le\|Xv\|^2/n$ with $1-\Delta_n/\kappa\ge1/2$. $\blacksquare$

### 7.5 Proof of Corollary C9

Fix the convention and set $\varphi_0^2:=\kappa/2$ (raw) or $\varphi_0^2:=\frac{\kappa/2}{K+\kappa/2}$ (standardised). Let $C_9:=\max\{5C_f,6C_e\}$ be the constant of Theorem T9 for the parameters $(\sigma_\star^2,M,\varphi_0,a_0,b_0)$ (Section 5), and put
$$
C:=\Big(C_9^2+\frac{C_9}{2\sigma_\star^2}\Big)^{1/2}.
$$
The map $(X,\varepsilon)\mapsto\Pi(A\mid y,X)$ is jointly Borel measurable for each of the posterior events $A$ below: the model weights $\pi(S\mid y,X)$ are Borel functions of $(X,y)$ (ratios, with positive denominators, of Borel functions built from (0.1); the standardisation map $X\mapsto\mathrm R$ is Borel), and the conditional probabilities of the events in $(\tilde\beta_S,\sigma^2)$ given $(S,y,X)$ are Borel functions of $(X,y)$, being integrals of indicator functions against Gaussian and inverse-gamma kernels whose parameters (0.2) are Borel in $(X,y)$. The conditional probabilities and expectations below are therefore well defined.

*Step 1 (conditioning on the design).* Fix $X\in\mathcal D_n$. Conditionally on $X$, $y=\tilde X\tilde\beta^\star+\varepsilon$ with $\varepsilon\sim N_n(0,\sigma_\star^2I_n)$ (independence of $\varepsilon$ and $X$), a fixed-design instance of the model of Section 0 with design $\tilde X$, true coefficient $\tilde\beta^\star$ supported on $S_0$, regression function $\tilde X\tilde\beta^\star=\mu$, prior $\mathrm{BB}(1,p)$ with cap $k_{\max}\ge s_0$, and posterior $\Pi(\cdot\mid y,X)$ as in (0.2). By Lemma 8(a), (b), this instance satisfies $\|\mu\|^2/n\le M$ and $\lambda_{\min}(\tilde\Gamma_{S_0S_0})\ge\varphi_0^2$, hence $\tilde\delta:=(\|\mu\|^2+\|\tilde\beta^\star_{S_0}\|^2)/n\le M(1+\varphi_0^{-2})=\bar\delta$ by (0.3). Therefore Theorem 5 (with its constants at $\bar\delta$) and Fact D apply to this instance, with exceptional probabilities that do not depend on $X$ (Remark 4.1 and Fact D). Concretely, with $u_n:=\varepsilon_n\sqrt n$ and for all $n$ so large that $\varepsilon_n^2\le1/8$, consider the event
$$
\Omega_n\cap\mathcal E_4(u_n)\cap F_n,\qquad F_n:=\Big\{\Pi(|S|>m_n\mid y,X)\le2e^{K_\star}e^{-\omega_n/2}\Big\},
$$
whose conditional probability given $X$ is at least $1-q_n$, $q_n:=\frac7n+\frac1{(s_0+1)\ell_n^2}+q_n^D$ (Lemma 3, Chebyshev for $\mathcal E_4(u_n)$, and (0.6)). On this event, Theorem 5(i) with $d=m_n$ and (5.1), Theorem 5(ii) with $d=m_n$, $u=u_n$ and (5.1), and the definition of $F_n$ bound the three posterior probabilities
$$
\Pi(A_1\mid y,X),\ \ \Pi(A_2\mid y,X),\ \ \Pi(A_3\mid y,X),\qquad A_1:=\{|S|>m_n\},\ \ A_2:=\Big\{\Big|\frac{\sigma^2}{\sigma_\star^2}-1\Big|>C_9\varepsilon_n\Big\},\ \ A_3:=\Big\{\frac{\|\tilde X_S\tilde\beta_S-\mu\|^2}{n}>C_9\varepsilon_n^2\Big\},
$$
respectively by $2e^{K_\star}e^{-\omega_n/2}$, by $\Pi(A_1\mid y,X)+e^{-\ell_n}+\frac1{(s_0+1)\ell_n^2}$ (as $6C_e\le C_9$ and $r_n(m_n,u_n)\le6\varepsilon_n$), and by $\Pi(A_1\mid y,X)+e^{-\ell_n}+\frac{2B}{\ell_n}$ (as $5C_f\le C_9$). Hence on that event
$$
\Pi(A_1\cup A_2\cup A_3\mid y,X)\le\zeta_n:=6e^{K_\star}e^{-\omega_n/2}+2e^{-\ell_n}+\frac{2B}{\ell_n}+\frac1{(s_0+1)\ell_n^2}\longrightarrow0,
$$
and $q_n\to0$; both sequences are deterministic and free of $X$.

*Step 2 (Hellinger small off $A_1\cup A_2\cup A_3$).* Still on $\mathcal D_n$, let $\theta=(S,\tilde\beta_S,\sigma^2)\notin A_1\cup A_2\cup A_3$, with coefficient vector $\beta$. Then $v:=\beta-\beta^\star$ is supported on $T:=S\cup S_0$ with $|T|\le m_n+s_0=\bar d_n$, and $Xv=X_S\beta_S-X_{S_0}\beta^\star_{S_0}=\tilde X_S\tilde\beta_S-\mu$. By Lemma 8(c) and $\theta\notin A_3$, $v^\top\Sigma_xv\le2\|\tilde X_S\tilde\beta_S-\mu\|^2/n\le2C_9\varepsilon_n^2$. By Lemma 6 and $\theta\notin A_2$,
$$
h^2(f_\theta,f_{\theta^\star})\le C_9^2\varepsilon_n^2+\frac{2C_9\varepsilon_n^2}{4\sigma_\star^2}=C^2\varepsilon_n^2 .
$$
Thus $\{h(f_\theta,f_{\theta^\star})>C\varepsilon_n\}\subseteq A_1\cup A_2\cup A_3$ on $\mathcal D_n$, and by Step 1, for all large $n$ and every $X\in\mathcal D_n$,
$$
\mathbb P\Big(\Pi\big(h(f_\theta,f_{\theta^\star})>C\varepsilon_n\ \big|\ y,X\big)>\zeta_n\ \Big|\ X\Big)\le q_n .
$$

*Step 3 (integrating over the design).* By Lemma 7, $\mathbb P(\mathcal D_n^c)\le2/n$ for all large $n$. Hence
$$
\mathbb P\Big(\Pi\big(h(f_\theta,f_{\theta^\star})>C\varepsilon_n\ \big|\ y,X\big)>\zeta_n\Big)\le\mathbb P(\mathcal D_n^c)+\mathbb E\Big[\mathbf 1_{\mathcal D_n}\,\mathbb P\Big(\Pi\big(h>C\varepsilon_n\mid y,X\big)>\zeta_n\ \Big|\ X\Big)\Big]\le\frac2n+q_n\longrightarrow0 .
$$
Since $\zeta_n\to0$, this is $\Pi(h(f_\theta,f_{\theta^\star})>C\varepsilon_n\mid y,X)\to0$ in probability over $(X,\varepsilon)$. The constant $C$ depends on $(\sigma_\star^2,M,\varphi_0,a_0,b_0)$, i.e. on $(\sigma_\star^2,M,\kappa,K,a_0,b_0)$ ($K$ only through $\varphi_0$ in the standardised case); $\varsigma$, $c_1$, $s_0$, $K_\star$ and the sequence $(\omega_n)$ enter only the threshold "$n$ large" and the rates $q_n$, $\zeta_n$. $\blacksquare$

*Remark 7.1 (the standardisation convention).* The two conventions define different posteriors (the unit ridge $I_k$ in $\Lambda_S$ is not scale-invariant), but the prediction $\tilde X_S\tilde\beta_S=X_S\beta_S$, the regression function $\mu$ and the Hellinger distance are the same functions of the coefficient vector $\beta$ in both. T9 never uses $\|x_j\|^2=n$, so it applies to either design; the only change is the eigenvalue constant $\varphi_0$ of the standardised design, which Lemma 8(b) bounds below by $(\kappa/2)/(K+\kappa/2)$, using that on $\mathcal D_n$ every column norm is controlled. This is the "rescale $\beta^\star$ and check that T9's constants survive" option of the prover note; they survive with $\varphi_0^2$ replaced as stated. The "drop the convention" option is the raw case. That the Hellinger loss is evaluated at the raw-scale coefficients $\beta(\theta)=\mathrm R^{-1}\tilde\beta$ is a reading of the frozen statement, recorded in Section 8.

*Remark 7.2 (what the sparse eigenvalue condition is used for).* (R4) is used only through Lemma 7 (to make $\Delta_n$ small; the union over the $\binom pd$ sets of size $d$ costs $d\ell_n\le\bar d_n\ell_n=O((s_0+1)\ell_n^2)$ and is the origin of the requirement $\varepsilon_n\to0$, i.e. $\ell_n^2=o(n)$) and Lemma 8 (to transfer the fixed-design conclusions to the population quadratic form, for differences supported on at most $\bar d_n$ coordinates). It is not used in the fixed-design part, which needs only $\lambda_{\min}(\tilde\Gamma_{S_0S_0})\ge\varphi_0^2$.

*Remark 7.3 (the frozen C9 is false without centring and without a uniform raw sub-Gaussian constant; the counterexample; heading qualified, audit 2026-10-15).* Take $p=1$, $x_i=n+Z_i$ with $Z_i$ i.i.d. $N(0,1)$, $\beta^\star=1$, $\sigma_\star^2=1$, $k_{\max}=1$ (any cap containing the true singleton), $M=2$, $\kappa=K=1$. The rows are Gaussian with covariance $\Sigma_x=1$, $\beta^{\star\top}\Sigma_x\beta^\star=1=M/2$, and $\ell_n^2=\log^2n=o(n)$. The centred rows $Z_i$ have a fixed $\psi_2$ norm, but the raw $\psi_2$ norm of $x_i$ is of order $n$ (by Jensen, $\mathbb Ee^{x_i^2/t^2}\ge e^{(n^2+1)/t^2}$, so $\|x_i\|_{\psi_2}^2\ge(n^2+1)/\log2$). So every hypothesis of the frozen C9 holds under the reading in which "sub-Gaussian" places no bound on the raw norm that is uniform in $n$; the example does not satisfy (R2). But $\mathbb E[x_i^2]=n^2+1$, so $\|\mu\|^2/n\approx n^2$ and $\|y\|^2/n^3\to1$ in probability. By the shrinkage floor (draft, (2)), $Q_S\ge\|y\|^2/(n+1)\asymp n^2$ for both models, for either design convention. Under $\Pi(\cdot\mid S,y)$, $\sigma^2=(2b_0+Q_S)/(2G)$ with $G\sim\mathrm{Gamma}(\nu,1)$ and $\nu\asymp n$, so $\Pi(\sigma^2\ge cn\mid S,y)\to1$ for a suitable $c>0$, uniformly in $S$. By (7.1) the affinity between $N(m_1,\sigma^2)$ and $N(m_2,1)$ is at most $\sqrt{2\sigma/(\sigma^2+1)}$ whatever $m_1,m_2$, which tends to $0$ as $\sigma^2\to\infty$; hence $h(f_\theta,f_{\theta^\star})\to1$ on posterior mass tending to one, while $C\varepsilon_n\to0$. So C9 fails as frozen under that reading; the mechanism is that the frozen signal bound $\beta^{\star\top}\Sigma_x\beta^\star\le M/2$ does not control $\|\mu\|^2/n$ when the rows are not centred, and the unit-information prior (through the shrinkage floor) cannot fit a regression function of size $\gg n$. The counterexample was raised independently by two reviewers (Astra B and C) and verified by computation for $n\in\{50,200,1000,5000\}$ and both conventions (`review/round1/check_counterexample_C9.py`: posterior mass on $\{h\ge1/2\}$ equal to $1$ to machine precision; posterior mean of $\sigma^2/n$ between $1.00$ and $1.05$). With centred rows, (R1), the mechanism disappears: $\mathbb E[x_ix_i^\top]=\Sigma_x$ and Lemma 8(a) bounds $\|\mu\|^2/n$ by $M$. Under (R2) alone the mechanism is also excluded, because Jensen gives $|v^\top\mathbb Ex_i|\le\varsigma\sqrt{\log2}\,\|v\|$, so the mean of the rows is bounded; but the proof given here still uses (R1), in Lemma 7 (Fact G needs mean-zero vectors), Lemma 8(a) and Lemma 8(c) (where $\Sigma_x$ must be the second-moment matrix). Treating uncentred rows under (R2) would need Gram concentration around the second-moment matrix $\Sigma_x+mm^\top$ ($m=\mathbb Ex_i$) and control of its sparse eigenvalues, where $\|m_T\|^2$ may grow with $|T|$; this is not done here, and whether (R1) can be dropped under (R2) is left open. Centring is the natural hypothesis for a model without intercept.

*Remark 7.4 (the uniform sub-Gaussian constant is used for Gram concentration; heading qualified, audit 2026-10-15).* If $\varsigma$ were allowed to depend on $n$, Lemma 7 could fail. Reviewers gave examples with $p=1$, centred rows of variance $1$, and an $n$-dependent law under which the single column is zero, or nearly zero, with probability bounded away from $0$ (for instance $x_i=0$ with probability $1-1/n$ and $x_i=\pm\sqrt n$ with probability $1/(2n)$ each: then $\mathbb P(X^\top X=0)=(1-1/n)^n\to e^{-1}$, while $\|x_i\|_{\psi_2}^2=n/\log(n+1)\to\infty$). Then $\Delta_n\not\to0$ in probability and the good design event fails. So (R2) with a fixed $\varsigma$ is the reading of "sub-Gaussian" under which this proof works, and only the threshold "$n$ large", not the constant $C$, depends on $\varsigma$. *(audit 2026-10-15)* The example shows that Lemma 7 (uniform Gram concentration) fails without uniform norm control; it does not show that C9's conclusion fails. In it, a nonzero predictor has population probability $1/n$, so with matching variances any regression-mean error confined to those predictor values contributes at most $1/n$ to $h^2$, below $\varepsilon_n^2\asymp\log^2n/n$. Whether (R2) is necessary for Hellinger contraction is not established here.

---

## 8. Hypotheses added, constants left implicit, and the steps I am least sure of

**Hypotheses added, amended, or made explicit.**
1. $n\ge4$ throughout (so that $\ell_n\ge1$, $\nu>1$ and $n/(n-2)\le2$); immaterial for asymptotic statements.
2. T9: none added. One hypothesis is shown to be superfluous for part (i) ($\ell_n^2=o(n)$ is used only in (ii), and there only in the last step). The dimension input is used in the nonasymptotic form Fact D (T6's Theorem 8), for an arbitrary admissible $\omega_n$; for T9 alone the asymptotic T6/T9a(i) would suffice, but C9 needs the uniformity over designs, which Fact D provides.
3. T9a(iii): the implication is proved with a constant that depends also on the dimension constant $C_1'$ of its hypothesis (Section 5); the frozen wording "T9 holds" should be read, or amended, accordingly (round-1 ruling 4). Part (ii) of the conclusion is proved under $\ell_n=o(n)$. The dimension bound itself is proved in Section 9 for polynomial $p$ under (H1) to (H4), with $C_1'=2A+2$; for super-polynomial $p$ it remains open.
4. C9: **(R1), centred rows, is an added hypothesis**: the frozen statement is false without it when sub-Gaussianity is read without a constant uniform in $n$ (Remark 7.3), and whether it can be dropped under the uniform reading (R2) is not settled here; it must go to the person for sign-off. (R2) makes explicit that the sub-Gaussian constant does not depend on $n$ (used for the uniform Gram-concentration argument, Lemma 7 and Remark 7.4; its necessity for the contraction conclusion is not established; audit 2026-10-15). The dimension input $\Pi(|S|>m_n\mid y,X)\to0$ (Fact D, i.e. T6/T9a(i)) is used separately from T9's conclusions, through the event $A_1$ in Step 2 of §7.5, to make $\beta-\beta^\star$ $(m_n+s_0)$-sparse so that Lemma 8(c) applies (noted for the draft's dependency table, audit 2026-10-15). (R4) is the frozen condition, for T6's $m_n$ with any admissible $\omega_n$ (the proof carries an arbitrary $\omega_n\to\infty$, $\omega_n\le\ell_n$); the condition is also used for singletons, which is automatic as $\bar d_n\ge1$. The Hellinger distance is taken with respect to $P_X\otimes\mathrm{Leb}$, which coincides with the draft's definition when the rows have a density. Both the raw and the standardised posterior are covered, with different $\varphi_0$; for the standardised posterior the convention $r_j=1$ on a zero column makes it everywhere defined, and the Hellinger loss is evaluated at the raw-scale coefficients $\beta(\theta)=\mathrm R^{-1}\tilde\beta$ (a reading of the frozen statement, the only meaningful one). Fact G is the single external result used; it is verified against its source.
5. Section 9 (the sharp dimension bound) assumes in addition (H1) $p\le n^A$, (H2) standardised columns (only to bound $\lambda_{\max}(G_{JJ})\le n|J|$; Remark 9.2), (H3) T7's sparse eigenvalue condition up to $m_n+s_0$, and (H4) $k_{\max}\ge m_n+s_0$. None of these is used before Section 9.

**Constants left implicit.** The constant $C$ of T9 is $\max\{5C_f,6C_e\}$ with
$$
B=2(b_0+M+2\sigma_\star^2),\ \ c_0=\tfrac1{2B},\ \ C_1=22\sigma_\star^2+2\bar\delta,\ \ C_a=\tfrac8{c_0}+2C_1,\ \ C_b=2C_a+28\sigma_\star^2,\ \ C_f=2C_b+2,\ \ C_c=3C_a+16\sigma_\star^2,\ \ C_d=\tfrac{2b_0+2a_0\sigma_\star^2+C_c}{\sigma_\star^2}+\sqrt2,\ \ C_e=2C_d+2\sqrt2,
$$
and $\bar\delta=M(1+\varphi_0^{-2})$; it is explicit but loose by a large factor (a round-1 reviewer found $\rho(d)$ above $\max_Sa_S$ in every enumerated instance with $n\le5000$; the bounds are asymptotic, as T9 claims). The constant $K_\star$ of Fact D is explicit in `proofs/T6/PROOF.md` (its (3.3) with $\delta=\bar\delta$). The thresholds "$n$ large" in Sections 5, 7 and 9 are not made explicit; they depend on $K_\star$ (hence on $s_0$), on $B$, on the sequence $(\omega_n)$, in Section 7 also on $\varsigma$, $\kappa$, $K$ and the absolute constant $c_1$ of Fact G (which is not explicit), and in Section 9 on $A$, $\varphi_0$, $\bar\delta$ and $\sigma_\star^2$. The constant of C9 is $C=(C_9^2+C_9/(2\sigma_\star^2))^{1/2}$; that of Corollary 14 is $\max\{C_f(2A+4),C_e(2A+5)\}$.

**Steps I am least sure of.**
1. *Section 9* is new in v2. *(audit 2026-10-15: the earlier "has not been reviewed" was stale.)* It was reviewed in round 2 by the three Astra reviewers only (no fatal or gap finding on Theorem 13 or Corollary 14; review/FINDINGS_round2.md), the v3 changes to it (Remark 9.1, (H4)) were not re-reviewed in that thread, and on 2026-10-15 the T9 parts of v3 (T9, Corollary 5.1 and T9a(iii), with focus on Sections 0 to 6, 8 and 9) were audited by GPT-6.1 Sol (`proofs/_audit/T9/SOL_AUDIT.md`, VERIFIED), and the C9 parts by a separate Sol audit (`proofs/_audit/C9/SOL_AUDIT.md`, VERIFIED). Its delicate points are the Schur-complement bounds of Lemma 9(c) (in particular $\lambda_{\min}$ of a Schur complement being at least $\lambda_{\min}$ of the matrix, and the use of $\lambda_{\max}(G_{JJ})\le\operatorname{tr}G_{JJ}$), the truncation argument of Proposition 12 (that the global event $\mathcal E_2$ implies the per-model truncation $\chi^2_J\le\tau_j$, so that the expectation can be taken model by model), and the bookkeeping of $\psi_j$ in Step 3 of Theorem 13, where the polynomial hypothesis (H1) is what makes $\beta_n=O(\sqrt{\log n})$ negligible against $\log n$.
2. *Remark 6.2* uses Pólya's theorem for the uniform CLT approximation and two elementary Gaussian interval bounds; it is not used anywhere else. The decomposition of $\mathrm{Gamma}(\nu,1)$ into exponentials plus a fractional-shape remainder is standard.
3. *Uniformity in Section 7, Step 1.* The claim that the event-level bounds of Theorem 5 and (0.6) hold conditionally on $X\in\mathcal D_n$ with $X$-free exceptional probabilities rests on Remark 4.1 and on Fact D's uniformity in the design subject to $\delta\le\bar\delta$ (Remark 4.1 of `proofs/T6/PROOF.md`); all three Opus reviewers of round 1 confirmed that no step in Sections 2 to 5 uses the design beyond $\|\mu\|^2/n\le M$ and $\delta\le\bar\delta$.
4. *The size-by-size union bound in Lemma 3* uses $\binom pk\le p^k$ and the geometric weights $2^{-k}$; this is where the factor $\ell_n$ per variable enters. It is sharp up to constants in the worst case over designs (for orthogonal columns the maximum of the $\binom pk$ projected chi-squares is $\sigma_\star^2$ times the sum of the $k$ largest of $p$ independent $\chi^2_1$ variables, of order $k\log(ep/k)$, hence of order $k\log p$ when $k\le p^{1-\delta}$ for a fixed $\delta>0$; audit 2026-10-15: e.g. for $k=p=n$ it is $\sigma_\star^2\chi^2_n\asymp n$, not $n\log n$), though not for every design (with identical columns it is $O_{\mathbb P}(1)$). Within the master theorem it cannot be avoided; what removes a factor $\ell_n$ from the rate is a sharper dimension bound, which is Section 9.
5. *The reading of the frozen statements* at two points: the constant of T9a(iii) (item 3 above) and the centring in C9 (item 4). Both are recorded as amendments for the draft and need the person's decision; neither amendment is proved to be necessary.

---

## 9. The sharp dimension bound for polynomial $p$, and the sharp rate (Corollary T9a(iii))

This section proves the hypothesis of the implication of Section 5 in the polynomial regime, under T7's sparse eigenvalue condition, and so proves Corollary T9a(iii) there. The proof is self-contained (it does not use T7, T8 or T10); it shares with T7's route the two ideas that an underfitting model is compared with its union with $S_0$, and that supersets are summed in expectation after truncation. Additional hypotheses in this section:

- (H1) $p\le n^A$ for a fixed $A\ge1$; hence $\ell_n\le A\log n$.
- (H2) the columns are standardised, $\|x_j\|^2=n$ for all $j$ (the draft's convention; see Remark 9.2 for what is used).
- (H3) the sparse eigenvalue condition (SE) of T7: $\lambda_{\min}(\Gamma_S)\ge\varphi_0^2$ for all $S$ with $|S|\le m_n+s_0$, with $m_n$ as in (0.5).
- (H4) the cap satisfies $k_{\max}\ge\min\{p,\,m_n+s_0\}$ (true with no cap, $k_{\max}=p$, and for the operational cap $\lfloor n/2\rfloor$ for all large $n$, since $m_n+s_0=O(\log n)$).

Throughout this section $u^\sharp_n:=\log n$, and all events are those of Lemma 3 and Section 4.

### 9.1 Monotonicity, Occam ratios and two more facts about $M_S$

**Lemma 9.** Let $S\subseteq S'$ be models and $J:=S'\setminus S$, $j:=|J|$.

(a) $Q_{S'}\le Q_S$ for every $y\in\mathbb R^n$; consequently $M_S\preceq M_{S'}$.

(b) $D_{S'}/D_S\le(n+1)^j$.

(c) If $G_{S'}\succ0$ with $\lambda_{\min}(G_{S'})\ge n\varphi_0^2$ and $\|x_i\|^2=n$ for every $i\in J$, then
$$
\frac{D_{S'}}{D_S}\ \ge\ \Big(\frac{n\varphi_0^2}{j+1}\Big)^{j}.
$$

(d) If $\lambda_{\min}(G_S)\ge n\varphi_0^2>0$, then $M_S\succeq\big(1-\frac{1+\varphi_0^{-2}}{n}\big)P_S$.

(e) If $S'\supseteq S_0$ then $a_{S'}\le\delta$.

*Proof.* (a) By Lemma 1(c) with $w=y$, $Q_S=\|y-X_Sb\|^2+b^\top\Lambda_Sb$ at the minimiser $b$. Let $b'\in\mathbb R^{|S'|}$ be $b$ on $S$ and $0$ on $J$. Then $X_{S'}b'=X_Sb$ and $b'^\top\Lambda_{S'}b'=\frac1n(\|X_{S'}b'\|^2+\|b'\|^2)=\frac1n(\|X_Sb\|^2+\|b\|^2)=b^\top\Lambda_Sb$, so $Q_{S'}\le\|y-X_{S'}b'\|^2+b'^\top\Lambda_{S'}b'=Q_S$. Since $Q_S=y^\top(I-M_S)y$ (Lemma 1(b)), $y^\top M_{S'}y\ge y^\top M_Sy$ for all $y$, i.e. $M_S\preceq M_{S'}$.

(b), (c) Order the coordinates of $S'$ as $(S,J)$ and write $G_{S'}=\begin{pmatrix}G_S&G_{SJ}\\G_{JS}&G_{JJ}\end{pmatrix}$. By Lemma 1(e)'s formula $D_T=\det((n+1)G_T+I)/\det(G_T+I)$ and the Schur determinant identity,
$$
\det\big((n+1)G_{S'}+I\big)=\det\big((n+1)G_S+I\big)\det\big((n+1)R_2+I\big),\qquad \det(G_{S'}+I)=\det(G_S+I)\det(R_1+I),
$$
where
$$
R_2:=G_{JJ}-(n+1)G_{JS}\big((n+1)G_S+I\big)^{-1}G_{SJ},\qquad R_1:=G_{JJ}-G_{JS}(G_S+I)^{-1}G_{SJ}
$$
(indeed the Schur complement of the block $(n+1)G_S+I$ in $(n+1)G_{S'}+I$ is $(n+1)G_{JJ}+I-(n+1)^2G_{JS}((n+1)G_S+I)^{-1}G_{SJ}=(n+1)R_2+I$). Hence
$$
\frac{D_{S'}}{D_S}=\frac{\det((n+1)R_2+I)}{\det(R_1+I)} . \tag{9.1}
$$
Both $(n+1)R_2+I$ and $R_1+I$ are positive definite, being Schur complements of the positive definite matrices $(n+1)G_{S'}+I$ and $G_{S'}+I$. Since $(n+1)((n+1)G_S+I)^{-1}=(G_S+\frac1{n+1}I)^{-1}\succeq(G_S+I)^{-1}$, we have $R_2\preceq R_1$. Moreover $R_1\succeq0$: it is the Schur complement of the positive definite block $G_S+I$ in the positive semidefinite matrix $G_{S'}+\operatorname{diag}(I_{|S|},0)$, and for $x\in\mathbb R^j$, $x^\top R_1x=\min_z\binom zx^\top\big(G_{S'}+\operatorname{diag}(I,0)\big)\binom zx\ge0$.

(b) $(n+1)R_2+I\preceq(n+1)R_1+I\preceq(n+1)(R_1+I)$, and the determinant is monotone on positive definite matrices, so $\det((n+1)R_2+I)\le(n+1)^j\det(R_1+I)$.

(c) Here $G_S\succ0$ (a principal submatrix of $G_{S'}\succ0$). Since $(G_S+\frac1{n+1}I)^{-1}\preceq G_S^{-1}$, $R_2\succeq R_0:=G_{JJ}-G_{JS}G_S^{-1}G_{SJ}$, the Schur complement of $G_S$ in $G_{S'}$. For $x\in\mathbb R^j$, $x^\top R_0x=\min_z\binom zx^\top G_{S'}\binom zx\ge\lambda_{\min}(G_{S'})\|x\|^2\ge n\varphi_0^2\|x\|^2$. Hence $(n+1)R_2+I\succeq\big((n+1)n\varphi_0^2+1\big)I$ and $\det((n+1)R_2+I)\ge((n+1)n\varphi_0^2+1)^j$. On the other side $R_1\preceq G_{JJ}$ and $\lambda_{\max}(G_{JJ})\le\operatorname{tr}G_{JJ}=\sum_{i\in J}\|x_i\|^2=nj$, so $\det(R_1+I)\le(nj+1)^j$. By (9.1),
$$
\frac{D_{S'}}{D_S}\ge\Big(\frac{(n+1)n\varphi_0^2+1}{nj+1}\Big)^j\ge\Big(\frac{(n+1)n\varphi_0^2}{n(j+1)}\Big)^j\ge\Big(\frac{n\varphi_0^2}{j+1}\Big)^j .
$$

(d) In the notation of the proof of Lemma 1(a), $M_S=\sum_i\frac{n\lambda_i}{(n+1)\lambda_i+1}q_iq_i^\top$ and $P_S=\sum_iq_iq_i^\top$ over the $i$ with $\lambda_i>0$ (here all $i$, as $\lambda_i\ge n\varphi_0^2>0$). For $\lambda\ge n\varphi_0^2$,
$$
\frac{n\lambda}{(n+1)\lambda+1}=\frac{n}{n+1}\cdot\frac{1}{1+\frac1{(n+1)\lambda}}\ge\frac n{n+1}\Big(1-\frac1{(n+1)\lambda}\Big)\ge1-\frac1{n+1}-\frac1{(n+1)n\varphi_0^2}\ge1-\frac{1+\varphi_0^{-2}}{n}.
$$

(e) Let $b'\in\mathbb R^{|S'|}$ be $\beta^\star_{S_0}$ on $S_0$ and $0$ on $S'\setminus S_0$. Then $X_{S'}b'=\mu$ and $b'^\top\Lambda_{S'}b'=\frac1n(\|\mu\|^2+\|\beta^\star_{S_0}\|^2)=\delta$, so $a_{S'}\le\delta$ by Lemma 1(c) with $w=\mu$. $\blacksquare$

### 9.2 Underfitting models are dominated by their union with $S_0$

**Lemma 10.** Assume (H4). For every model $S$ with $|S|\le m_n$, writing $S':=S\cup S_0$,
$$
\frac{p(S)\,m(S)}{p(S_0)\,m(S_0)}\ \le\ (2p)^{s_0}(n+1)^{s_0/2}\ \frac{p(S')\,m(S')}{p(S_0)\,m(S_0)} .
$$

*Proof.* $|S'|\le\min\{p,|S|+s_0\}\le\min\{p,m_n+s_0\}\le k_{\max}$ by (H4), so $p(S')=w(|S'|)/W>0$ and $p(S)/p(S')=w(|S|)/w(|S'|)$. By L6(i) with $b_\pi=p$, $w(k)/w(k+1)=(2p-k-1)/(k+1)\le2p$ for $0\le k\le p-1$, hence $w(|S|)/w(|S'|)\le(2p)^{|S'|-|S|}\le(2p)^{s_0}$. By (0.1) and Lemma 9(a), (b),
$$
\frac{m(S)}{m(S')}=\Big(\frac{D_{S'}}{D_S}\Big)^{1/2}\Big(\frac{2b_0+Q_{S'}}{2b_0+Q_S}\Big)^{\nu}\le\Big(\frac{D_{S'}}{D_S}\Big)^{1/2}\le(n+1)^{|S'\setminus S|/2}\le(n+1)^{s_0/2},
$$
since $|S'\setminus S|=|S_0\setminus S|\le s_0$. Multiply the two bounds. $\blacksquare$

### 9.3 A truncated exponential moment

**Lemma 11.** Let $\xi\sim\chi^2_j$ with $j\ge1$, and let $\eta\ge0$, $\tau>0$. Then
$$
\mathbb E\big[e^{(1+\eta)\xi/2}\,\mathbf 1\{\xi\le\tau\}\big]\le\Big(\frac{e\tau}{j}\Big)^{j/2}e^{\eta\tau/2}.
$$

*Proof.* With the $\chi^2_j$ density $x^{j/2-1}e^{-x/2}/(2^{j/2}\Gamma(j/2))$,
$$
\mathbb E\big[e^{(1+\eta)\xi/2}\mathbf 1\{\xi\le\tau\}\big]=\frac1{2^{j/2}\Gamma(j/2)}\int_0^\tau x^{j/2-1}e^{\eta x/2}\,dx\le\frac{e^{\eta\tau/2}}{2^{j/2}\Gamma(j/2)}\cdot\frac{\tau^{j/2}}{j/2}=\frac{(\tau/2)^{j/2}e^{\eta\tau/2}}{\Gamma(j/2+1)} .
$$
Finally $\Gamma(x+1)\ge(x/e)^x$ for $x>0$ (as $\Gamma(x+1)=\int_0^\infty t^xe^{-t}dt\ge\int_x^\infty t^xe^{-t}dt\ge x^xe^{-x}$), so $(\tau/2)^{j/2}/\Gamma(j/2+1)\le(\tau/2)^{j/2}(2e/j)^{j/2}=(e\tau/j)^{j/2}$. $\blacksquare$

### 9.4 Supersets of $S_0$

Recall $\bar\delta=M(1+\varphi_0^{-2})\ge\delta$ (0.3). Define the deterministic sequences
$$
\theta_n:=\frac{\sqrt2\,u^\sharp_n}{\sqrt n}+\frac{4\sqrt{\bar\delta\,(m_n+s_0+1)\ell_n}}{\sigma_\star\,n}+\frac{14(m_n+s_0)\ell_n}{n},\qquad
\eta_n:=\frac{1+2a_0/n}{1-\theta_n}-1\quad(\text{when }\theta_n<1),
$$
and, for $j\ge1$,
$$
\xi_j:=\delta+8\sigma_\star\sqrt{\delta(s_0+j+1)\ell_n}+\frac{14(1+\varphi_0^{-2})\sigma_\star^2s_0\ell_n}{n},\qquad \tau_j:=14(s_0+j)\ell_n .
$$
Under (H1), $m_n\le4(s_0+1)\ell_n\le4A(s_0+1)\log n$ by (0.7), so $\theta_n=O(\log n/\sqrt n)+O(\log^2n/n)\to0$ and $\eta_n\to0$; more precisely, once $\theta_n\le\frac12$, $\eta_n=\frac{2a_0/n+\theta_n}{1-\theta_n}\le2\theta_n+\frac{4a_0}n$, so that $\eta_n\ell_n\to0$.

For $J\subseteq[p]\setminus S_0$ put $S'=S_0\cup J$ and
$$
\chi^2_J:=\frac{\|(P_{S'}-P_{S_0})\varepsilon\|^2}{\sigma_\star^2},\qquad \tilde T_j:=\sum_{J\subseteq[p]\setminus S_0,\ |J|=j}e^{(1+\eta_n)\chi^2_J/2}\,\mathbf 1\{\chi^2_J\le\tau_j\} .
$$

**Proposition 12 (supersets).** Assume the standing assumptions, (H1), (H2), (H3), and let $n$ be so large that $\theta_n\le\frac12$. On the event $\mathcal E_2\cap\mathcal E_3\cap\mathcal E_4(u^\sharp_n)$, for every $1\le j\le m_n$,
$$
\sum_{J\subseteq[p]\setminus S_0,\ |J|=j}\frac{p(S_0\cup J)\,m(S_0\cup J)}{p(S_0)\,m(S_0)}\ \le\ \Phi_j\,\tilde T_j,\qquad
\Phi_j:=\Big(\frac{s_0+j}{p}\Big)^j\Big(\frac{j+1}{n\varphi_0^2}\Big)^{j/2}\exp\Big(\frac{1+\eta_n}{2\sigma_\star^2}\,\xi_j\Big), \tag{9.2}
$$
and
$$
\mathbb E_0\big[\Phi_j\tilde T_j\big]\ \le\ \Big(\frac{28e^3(s_0+1)^2(s_0+j)\ell_n}{n\varphi_0^2}\Big)^{j/2}\exp\Big(7\eta_n(s_0+j)\ell_n+\frac{1+\eta_n}{2\sigma_\star^2}\xi_j\Big). \tag{9.3}
$$

*Proof.* Fix $J$ with $|J|=j\in[1,m_n]$ and $S'=S_0\cup J$, so $|S'|=s_0+j\le m_n+s_0$, and by (H3) $G_{S'}\succ0$ with $\lambda_{\min}(G_{S'})\ge n\varphi_0^2$; in particular $X_{S'}$ has full column rank, $P_{S'}-P_{S_0}$ is an orthogonal projection of rank $j$, and $\chi^2_J\sim\chi^2_j$ under $\mathbb P_0$. Also $G_{S_0}\succ0$ with $\lambda_{\min}(G_{S_0})\ge n\varphi_0^2$ (if $s_0\ge1$; for $s_0=0$, $P_{S_0}=M_{S_0}=0$ and the terms involving $S_0$ below vanish).

*Prior.* By L6(i), $\frac{w(s_0+j)}{w(s_0)}=\prod_{i=s_0}^{s_0+j-1}\frac{i+1}{2p-i-1}\le\Big(\frac{s_0+j}{2p-s_0-j}\Big)^j\le\Big(\frac{s_0+j}{p}\Big)^j$, because $s_0+j=|S'|\le p$ gives $2p-s_0-j\ge p$. Since $|S'|\le\min\{p,m_n+s_0\}\le k_{\max}$ by (H4) (or simply because the bound is only needed when $p(S')>0$), $p(S')/p(S_0)=w(s_0+j)/w(s_0)$.

*Occam factor.* By Lemma 9(c) with $S=S_0$ and (H2), $D_{S'}/D_{S_0}\ge(n\varphi_0^2/(j+1))^j$.

*Fit.* By Lemma 9(a), $Q_{S'}\le Q_{S_0}$, and by $\log(1+x)\le x$,
$$
\nu\log\frac{2b_0+Q_{S_0}}{2b_0+Q_{S'}}\le\frac{\nu\,(Q_{S_0}-Q_{S'})}{2b_0+Q_{S'}} .
$$
*Upper bound for $Q_{S_0}-Q_{S'}$.* By Lemma 1(d) for $S_0$ and $S'$,
$$
Q_{S_0}-Q_{S'}=(a_{S_0}-a_{S'})+2(W_{S_0}-W_{S'})+\varepsilon^\top(M_{S'}-M_{S_0})\varepsilon .
$$
Here $a_{S_0}-a_{S'}\le\delta$ (Lemma 1(c), $a_{S'}\ge0$). On $\mathcal E_3$, using $a_{S_0}\le\delta$ and $a_{S'}\le\delta$ (Lemma 9(e)), $2|W_{S_0}|+2|W_{S'}|\le4\sigma_\star\sqrt{\delta(s_0+1)\ell_n}+4\sigma_\star\sqrt{\delta(s_0+j+1)\ell_n}\le8\sigma_\star\sqrt{\delta(s_0+j+1)\ell_n}$. Finally, by $M_{S'}\preceq P_{S'}$ (Lemma 1(a)) and Lemma 9(d) for $S_0$,
$$
\varepsilon^\top(M_{S'}-M_{S_0})\varepsilon\le\varepsilon^\top(P_{S'}-P_{S_0})\varepsilon+\varepsilon^\top(P_{S_0}-M_{S_0})\varepsilon\le\sigma_\star^2\chi^2_J+\frac{1+\varphi_0^{-2}}{n}\|P_{S_0}\varepsilon\|^2\le\sigma_\star^2\chi^2_J+\frac{14(1+\varphi_0^{-2})\sigma_\star^2s_0\ell_n}{n},
$$
the last step on $\mathcal E_2$. Altogether, $Q_{S_0}-Q_{S'}\le\sigma_\star^2\chi^2_J+\xi_j$.

*Lower bound for $2b_0+Q_{S'}$.* By Lemma 1(d), $Q_{S'}=a_{S'}+2W_{S'}+\sigma_\star^2E-\varepsilon^\top M_{S'}\varepsilon\ge-2|W_{S'}|+\sigma_\star^2E-\|P_{S'}\varepsilon\|^2$. On $\mathcal E_2\cap\mathcal E_3\cap\mathcal E_4(u^\sharp_n)$, with $\delta\le\bar\delta$ and $j\le m_n$,
$$
2b_0+Q_{S'}\ge\sigma_\star^2\big(n-u^\sharp_n\sqrt{2n}\big)-4\sigma_\star\sqrt{\bar\delta(m_n+s_0+1)\ell_n}-14\sigma_\star^2(m_n+s_0)\ell_n=n\sigma_\star^2(1-\theta_n)\ \ (>0).
$$
Hence $\frac{\nu}{2b_0+Q_{S'}}\le\frac{(n+2a_0)/2}{n\sigma_\star^2(1-\theta_n)}=\frac{1+\eta_n}{2\sigma_\star^2}$, and since $Q_{S_0}-Q_{S'}\ge0$,
$$
\nu\log\frac{2b_0+Q_{S_0}}{2b_0+Q_{S'}}\le\frac{1+\eta_n}{2\sigma_\star^2}\big(\sigma_\star^2\chi^2_J+\xi_j\big)=\frac{1+\eta_n}2\chi^2_J+\frac{1+\eta_n}{2\sigma_\star^2}\xi_j .
$$

*Assembly of (9.2).* By (0.1),
$$
\frac{p(S')m(S')}{p(S_0)m(S_0)}=\frac{w(s_0+j)}{w(s_0)}\Big(\frac{D_{S'}}{D_{S_0}}\Big)^{-1/2}\exp\Big(\nu\log\frac{2b_0+Q_{S_0}}{2b_0+Q_{S'}}\Big)\le\Phi_j\,e^{(1+\eta_n)\chi^2_J/2} .
$$
On $\mathcal E_2$, $\sigma_\star^2\chi^2_J\le\|P_{S'}\varepsilon\|^2\le14\sigma_\star^2(s_0+j)\ell_n$, i.e. $\chi^2_J\le\tau_j$, so $e^{(1+\eta_n)\chi^2_J/2}=e^{(1+\eta_n)\chi^2_J/2}\mathbf 1\{\chi^2_J\le\tau_j\}$. Summing over $J$ gives (9.2).

*Proof of (9.3).* $\Phi_j$ is deterministic. There are $\binom{p-s_0}j\le p^j/j!$ sets $J$, and for each, by Lemma 11 (applicable since $\chi^2_J\sim\chi^2_j$),
$$
\mathbb E_0\tilde T_j\le\frac{p^j}{j!}\Big(\frac{e\tau_j}j\Big)^{j/2}e^{\eta_n\tau_j/2}=\frac{p^j}{j!}\Big(\frac{14e(s_0+j)\ell_n}j\Big)^{j/2}e^{7\eta_n(s_0+j)\ell_n}.
$$
Hence
$$
\mathbb E_0[\Phi_j\tilde T_j]\le\frac{(s_0+j)^j}{j!}\Big(\frac{(j+1)\cdot14e(s_0+j)\ell_n}{j\,n\varphi_0^2}\Big)^{j/2}\exp\Big(7\eta_n(s_0+j)\ell_n+\frac{1+\eta_n}{2\sigma_\star^2}\xi_j\Big),
$$
and $\frac{(s_0+j)^j}{j!}\le\big(\frac{e(s_0+j)}j\big)^j\le(e(s_0+1))^j$ (as $j!\ge(j/e)^j$ and $j\ge1$), $\frac{j+1}j\le2$. Since $(e(s_0+1))^j=\big(e^2(s_0+1)^2\big)^{j/2}$, this is (9.3). $\blacksquare$

### 9.5 The sharp dimension bound

**Theorem 13 (posterior dimension $O((s_0+1)A)$).** Assume the standing assumptions (Section 0), (H1) to (H4), and put
$$
j_0:=\lceil s_0(2A+1)\rceil,\qquad d^\sharp:=s_0+j_0\ \le\ (2A+2)(s_0+1).
$$
Then $\Pi(|S|>d^\sharp\mid y)\to0$ in $\mathbb P_0$-probability.

*Proof.* *Step 1 (reduction to supersets).* By Fact D, $\Pi(|S|>m_n\mid y)\to0$ in probability, so it suffices to treat $\mathcal M:=\{S:d^\sharp<|S|\le m_n\}$ (for all large $n$, $d^\sharp<m_n$, as $m_n\ge\frac{s_0+1}2\log n/\log2\to\infty$; if $\mathcal M=\emptyset$ there is nothing to prove). For $S\in\mathcal M$ put $S'=S\cup S_0=S_0\cup J$ with $J=S\setminus S_0$; then $j:=|J|\ge|S|-s_0>j_0$ and $j\le|S|\le m_n$. The map $S\mapsto S'$ is at most $2^{s_0}$-to-one (given $S'$, $S$ is determined by $S\cap S_0\subseteq S_0$). By Lemma 10 (which needs (H4)) and $Z\ge p(S_0)m(S_0)>0$,
$$
\Pi(\mathcal M\mid y)\le\sum_{S\in\mathcal M}\frac{p(S)m(S)}{p(S_0)m(S_0)}\le(2p)^{s_0}(n+1)^{s_0/2}2^{s_0}\sum_{j=j_0+1}^{m_n}\ \sum_{J\subseteq[p]\setminus S_0,\ |J|=j}\frac{p(S_0\cup J)m(S_0\cup J)}{p(S_0)m(S_0)} .
$$
*Step 2 (the superset sum on the good event).* Let $n$ be so large that $\theta_n\le\frac12$. On $\mathcal E_2\cap\mathcal E_3\cap\mathcal E_4(u^\sharp_n)$, by Proposition 12,
$$
\Pi(\mathcal M\mid y)\le\Xi_n:=(2p)^{s_0}(n+1)^{s_0/2}2^{s_0}\sum_{j=j_0+1}^{m_n}\Phi_j\tilde T_j .
$$
*Step 3 (the expectation of $\Xi_n$).* By (9.3), $\mathbb E_0[\Phi_j\tilde T_j]\le\kappa_n^{j/2}e^{\psi_j}$ for $1\le j\le m_n$, where, using $s_0+j\le5(s_0+1)\ell_n$ (from $j\le m_n\le4(s_0+1)\ell_n$),
$$
\kappa_n:=\frac{140e^3(s_0+1)^3\ell_n^2}{n\varphi_0^2},\qquad \psi_j:=7\eta_n(s_0+j)\ell_n+\frac{1+\eta_n}{2\sigma_\star^2}\xi_j .
$$
We bound $\psi_j$ linearly in $j$. Since $j\ge1$, $s_0+j\le(s_0+1)j$ and $s_0+j+1\le2(s_0+1)j$; also $\sqrt{j\ell_n}\le j\sqrt{\ell_n}$ and $\delta\le\bar\delta$. Hence
$$
\psi_j\le\alpha_nj+\beta_nj+\gamma_n,\qquad \alpha_n:=7(s_0+1)\eta_n\ell_n,\quad \beta_n:=\frac{(1+\eta_n)\,4\sqrt{2\bar\delta(s_0+1)}}{\sigma_\star}\sqrt{\ell_n},\quad \gamma_n:=\frac{1+\eta_n}{2\sigma_\star^2}\Big(\bar\delta+\frac{14(1+\varphi_0^{-2})\sigma_\star^2s_0\ell_n}{n}\Big).
$$
Under (H1): $\alpha_n\to0$ (as $\eta_n\ell_n\to0$), $\beta_n=O(\sqrt{\log n})$, $\gamma_n=O(1)$. Therefore $\kappa_n^{j/2}e^{\psi_j}\le e^{\gamma_n}(\kappa_n')^{j/2}$ with
$$
\kappa_n':=\kappa_ne^{2\alpha_n+2\beta_n},\qquad \log\kappa_n'=-\log n+2\log\ell_n+2\alpha_n+2\beta_n+O(1)=-\log n\,(1+o(1)),
$$
because $\log\ell_n=O(\log\log n)$ and $\beta_n=O(\sqrt{\log n})$. In particular $\kappa_n'\le\frac14$ for all large $n$, and then $\sum_{j>j_0}(\kappa_n')^{j/2}\le2(\kappa_n')^{(j_0+1)/2}$. Consequently
$$
\bar\Xi_n:=\mathbb E_0\Xi_n\le(2p)^{s_0}(n+1)^{s_0/2}2^{s_0}\cdot2e^{\gamma_n}(\kappa_n')^{(j_0+1)/2},
$$
and, using $p\le n^A$ and $\log(n+1)\le\log n+1$,
$$
\log\bar\Xi_n\le s_0A\log n+\frac{s_0}2\log n-\frac{j_0+1}2\log n\,(1+o(1))+O(1)=-\frac{\log n}{2}\Big[(j_0+1)-s_0(2A+1)+o(1)\Big]+O(1)\longrightarrow-\infty,
$$
since $j_0+1>s_0(2A+1)$ by the choice of $j_0$. So $\bar\Xi_n\to0$.

*Step 4 (conclusion).* By Markov's inequality, $\mathbb P_0(\Xi_n>\sqrt{\bar\Xi_n})\le\sqrt{\bar\Xi_n}$. On $\mathcal E_2\cap\mathcal E_3\cap\mathcal E_4(u^\sharp_n)\cap\{\Xi_n\le\sqrt{\bar\Xi_n}\}$, whose complement has probability at most $\frac1n+\frac4n+\frac1{\log^2n}+\sqrt{\bar\Xi_n}\to0$ (Lemma 3 and Chebyshev), $\Pi(\mathcal M\mid y)\le\sqrt{\bar\Xi_n}\to0$. Together with Step 1 this gives $\Pi(|S|>d^\sharp\mid y)\le\Pi(|S|>m_n\mid y)+\Pi(\mathcal M\mid y)\to0$ in probability. Finally $d^\sharp=s_0+\lceil s_0(2A+1)\rceil\le s_0+s_0(2A+1)+1=(2A+2)s_0+1\le(2A+2)(s_0+1)$. $\blacksquare$

**Corollary 14 (Corollary T9a(iii) for polynomial $p$).** Under the hypotheses of Theorem 13, Theorem T9 holds with $\varepsilon_n^2$ replaced by
$$
\bar\varepsilon_n^2=\frac{(s_0+1)\ell_n}{n}\le\frac{(s_0+1)A\log n}{n},
$$
with a constant depending only on $(\sigma_\star^2,M,\varphi_0,a_0,b_0,A)$.

*Proof.* Theorem 13 gives $\Pi(|S|>C_1'(s_0+1)\mid y)\to0$ with $C_1'=2A+2$; apply the implication proved in Section 5 (its hypothesis $\ell_n=o(n)$ holds since $\ell_n\le A\log n$). The constant is $\max\{C_f(2A+4),C_e(2A+5)\}$. $\blacksquare$

*Remark 9.1 (what was used, and what remains open).* The polynomial hypothesis (H1) enters in Step 3 only, in two places: to make the conversion cost $(2p)^{s_0}$ a fixed power $n^{s_0A}$ of $n$, and to make $\beta_n=O(\sqrt{\ell_n})$ negligible against $\log n$. It also enters earlier, through $\theta_n\to0$ and $\eta_n\ell_n\to0$ in Section 9.4, which use $m_n\ell_n=O(\log^2n)$. For super-polynomial $p$ (say $\ell_n\asymp n^{\alpha}$) the argument does not apply as written: once $\theta_n\le\frac12$, $\eta_n\ell_n=O\big(\ell_n\log n/\sqrt n+\ell_n^3/n\big)$ (the first term from $u^\sharp_n=\log n$; audit 2026-10-15, replacing an incorrect "$\eta_n\ell_n\asymp\ell_n^3/n$"), and this bound need not tend to zero (it does not once $\ell_n\gtrsim n^{1/3}$), $\beta_n=O(\sqrt{\ell_n})$ is no longer negligible against $\log n$, and the conversion cost $(2p)^{s_0}$ would have to be absorbed by the Occam gain. No dimension bound is claimed in that regime, and the sharp rate for $\alpha\ge\frac12$ is open. (H3) is used only through Lemma 9(c), (d) and the full rank of $X_{S'}$; (H2) only in Lemma 9(c); (H4) only in Lemma 10. The exceptional probability in Step 4 is $\frac5n+\frac1{\log^2n}+\sqrt{\bar\Xi_n}$; the $1/\log^2n$ comes from Chebyshev for $E$ at $u^\sharp_n=\log n$, and the Markov term is bounded by $n^{-[(j_0+1)-s_0(2A+1)]/4+o(1)}$ (Step 3 gives an upper bound, not a rate). No beta-min condition is used: a weak true variable missed by $S$ is simply added in $S'=S\cup S_0$, at the fixed cost $(2p)^{s_0}(n+1)^{s_0/2}2^{s_0}$ that $j_0$ is chosen to absorb.

*Remark 9.2 (the standardisation).* (H2) is used only to bound $\lambda_{\max}(G_{JJ})\le nj$ in Lemma 9(c). It can be replaced by $\max_j\|x_j\|^2\le\bar\lambda n$, in which case $(n\varphi_0^2/(j+1))^j$ becomes $(n\varphi_0^2/(\bar\lambda j+1))^j$ and the constants change accordingly.

---

## Audit revisions (2026-10-15)

Sol audits `proofs/_audit/T9/SOL_AUDIT.md` and `proofs/_audit/C9/SOL_AUDIT.md` (both VERIFIED); rulings in `proofs/_audit/group_C/RULINGS.md`. No step of any proof was changed and no statement was changed; all edits are to remarks and annotations.

1. **Remark 9.1** (T9 finding 1). The incorrect equivalence $\eta_n\ell_n\asymp\ell_n^3/n$ is replaced by the bound $\eta_n\ell_n=O(\ell_n\log n/\sqrt n+\ell_n^3/n)$ (the first term from $u_n^\sharp=\log n$), which need not tend to zero for super-polynomial $p$. The qualitative conclusion is unchanged. Checked numerically (`proofs/_audit/group_C/check_audit_C.py`, block T9 #1).
2. **§8, "Steps I am least sure of", item 4** (T9 finding 2). The orthogonal-design scale is now $k\log(ep/k)$, which is of order $k\log p$ only when $k\le p^{1-\delta}$; counterexample $k=p=n$ noted.
3. **§8, "Steps I am least sure of", item 1** (T9 finding 3). The stale "Section 9 ... has not been reviewed" is replaced by its actual review history (round 2, three Astra reviewers; v3 changes not re-reviewed in the thread; Sol audits of 2026-10-15, with the scope of each stated; the scope wording was corrected after the T9 confirmation exchange).
4. **(R1) and the heading of Remark 7.3** (C9 finding 2). Qualified: the counterexample refutes the frozen C9 without centring *and* without a uniform raw sub-Gaussian constant; it does not show that centring alone is needed under (R2), which remains open.
5. **(R2), the heading and last sentence of Remark 7.4, and §8 item 4** (C9 finding 3). "Necessary" is replaced by "used for the uniform Gram-concentration argument (Lemma 7)"; the rare-spike example shows that Lemma 7 fails, not that C9's conclusion fails (the mean part of $h^2$ is at most $1/n<\varepsilon_n^2$ there).
6. **§8 item 4** (C9 finding 4, bookkeeping). Notes that the dimension input $\Pi(|S|>m_n\mid y,X)\to0$ (Fact D) is used separately from T9's conclusions, in Step 2 of §7.5; this is for the draft's dependency table.
7. C9 finding 1 (reference measure $P_X\otimes\mathrm{Leb}$): no change; the proof already uses it (§7.1). Draft change only.
