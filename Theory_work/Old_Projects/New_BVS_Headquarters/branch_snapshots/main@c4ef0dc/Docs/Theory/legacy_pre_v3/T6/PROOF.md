# Proof of Theorem T6 (posterior dimension) and verification of Corollary T9a(i)

Supplement material for *Split-and-merge with an exact merge: composite-start sequential Monte Carlo for Bayesian variable selection*, draft of 14 October 2026. Thread: T6. Prover: Fable 5.1 (lead), 14 October 2026. Version 4 (after three review rounds: three Opus 5.5 and three GPT-6 Astra reviewers; rulings in `review/FINDINGS.md`; the v3 to v4 edits are confined to the Section 6.4 remark and the summary, and reduce claims). Status: the proof of T6 (Sections 1 to 4) and the qualified verification of T9a(i) (Section 5) were reported as "every step verified" by the reviewers in round 3; the Section 6.4 remark reports a reviewer's construction that is not proved in this document. Numerical sanity checks in `check_T6.py` (not part of the proof).

Assumed from the draft: only Section 2 (model, priors, the closed form (1) of $m(S)$, the data-generating model, the standing assumptions of Section 4). The parts of Lemma L6 that are used are proved inline (Lemma 3). The closed form (1) is re-derived inline (Lemma 1) because the denominator bound rests on it. No other numbered result of the draft is used. One classical analytic fact is needed, a Stirling-type lower bound for $\Gamma$; a self-contained proof is given (Lemma 5).

**Summary of the outcome.** T6 is true as stated, and the argument gives more than the statement: an explicit nonasymptotic bound (Theorem 8) whose probability bound is uniform in $p$, in the cap, and in the design and $\beta^\star$ subject only to a bound on $\delta$ below, from which T6 and Corollary T9a(i) are read off. No hypothesis is added. The hypothesis $p\le n^A$ is never used in the convergence statement (it only turns $m_n$ into $O(\log n)$ in the "in particular" clause); the design condition $\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2$ and the signal bound $\|\mu\|^2/n\le M$ enter at exactly one point (Lemma 4), through the single number $\delta=(\|\mu\|^2+\|\beta^\star_{S_0}\|^2)/n$. The counting objection of the prover note is examined in Section 6: the exact identity of Proposition 2, together with the denominator bound of Proposition 7, is what disposes of it, and it does so for every polynomial $p$ and indeed for $\log p$ up to a constant times $n$; the shrinkage floor (2) caps what interpolation can earn but does not by itself settle the objection; and for super-exponential $p$ (outside the standing assumptions), with $s_0\ge1$, a reviewer's construction (reported in Section 6.4, not re-derived here, consistent with single-draw numerics) indicates that the objection's scenario does occur, with no contradiction to T6 because $m_n$ then exceeds $n/2$. One inaccuracy in the draft's wording of T9a(i) is corrected in Section 5 ($m_n=O(s_0\ell_n)$ needs $s_0\ge1$; in general $m_n=O((s_0+1)\ell_n)$).

---

## 0. Setting, conventions and notation

All notation is that of Section 2 of the draft. Throughout: $n\ge2$ and $p\ge1$ are integers; the design $X\in\mathbb R^{n\times p}$ is fixed; the hyperparameters $a_0,b_0>0$ are fixed; $\log$ is the natural logarithm; $[p]=\{1,\dots,p\}$; a model is a set $S\subseteq[p]$ with $k=|S|$. Column standardisation ($\|x_j\|^2=n$) is never used.

**Likelihood and priors.** For a model $S$ with $k=|S|$,
$$
y\mid\beta_S,\sigma^2,S\sim N_n(X_S\beta_S,\sigma^2I_n),\qquad
\beta_S\mid\sigma^2,S\sim N_k\big(0,\sigma^2\Lambda_S^{-1}\big),\qquad \Lambda_S=\tfrac1n(G_S+I_k),\qquad
\sigma^2\sim\mathrm{IG}(a_0,b_0),
$$
with $G_S=X_S^\top X_S$ and the inverse-gamma density $g(v)=\frac{b_0^{a_0}}{\Gamma(a_0)}v^{-a_0-1}e^{-b_0/v}$ on $(0,\infty)$. For $k=0$ there is no $\beta_S$ and $X_S\beta_S=0$.

**Marginal likelihood (draft (1)).** With $H_S=(n+1)G_S+I_k$, $D_S=\det H_S/\det(G_S+I_k)$, $z_S=X_S^\top y$, $t_S=n\,z_S^\top H_S^{-1}z_S$, $Q_S=y^\top y-t_S$, $\nu=a_0+n/2$ and $C_n=\pi^{-n/2}(2b_0)^{a_0}\Gamma(\nu)/\Gamma(a_0)$,
$$
m(S)=m(S)(y)=C_n\,D_S^{-1/2}\,(2b_0+Q_S)^{-\nu}. \tag{0.1}
$$
For $k=0$: $D_\emptyset=1$, $t_\emptyset=0$, $Q_\emptyset=y^\top y$.

**Model prior.** $\mathrm{BB}(1,p)$ with cap $k_{\max}\in\{0,\dots,p\}$:
$$
w(k)=\frac{B(1+k,\;2p-k)}{B(1,p)},\qquad p(S)=\frac{w(|S|)\,\mathbf 1\{|S|\le k_{\max}\}}{W},\qquad W=\sum_{k\le k_{\max}}\binom pk w(k).
$$
"No cap" means $k_{\max}=p$; a nominal cap larger than $p$ (e.g. $\lfloor n/2\rfloor$ when $p<n/2$) is the same as no cap, since no model has more than $p$ variables (the sum defining $W$ runs over $k\le\min\{k_{\max},p\}$). For a set $\mathcal A$ of models, $p(\mathcal A)=\sum_{S\in\mathcal A}p(S)$; $\{|S|>m\}$ denotes $\{S\subseteq[p]:|S|>m\}$.

**Posterior.** $\pi(S)=\Pi(S\mid y)=p(S)m(S)/Z$ with $Z=\sum_Sp(S)m(S)$, and $\Pi(\mathcal A\mid y)=\sum_{S\in\mathcal A}\pi(S)$.

**Data-generating model.** $y=\mu+\varepsilon$ with $\mu=X\beta^\star$, $\varepsilon\sim N_n(0,\sigma_\star^2I_n)$, $S_0=\operatorname{supp}(\beta^\star)$, $s_0=|S_0|$, so $\mu=X_{S_0}\beta^\star_{S_0}$. $\mathbb P_0$ and $\mathbb E_0$ are over $\varepsilon$, with $X$, $\beta^\star$, $\sigma_\star^2$ fixed. The density of $y$ is
$$
f_0(y)=(2\pi\sigma_\star^2)^{-n/2}\exp\Big(-\frac{\|y-\mu\|^2}{2\sigma_\star^2}\Big)>0 .
$$
"$A_n\to a$ in probability" means $\mathbb P_0(|A_n-a|>\epsilon)\to0$ for every $\epsilon>0$ (draft, Section 2).

**Standing assumptions of Section 4** (for T6): $n\to\infty$ with $s_0$ fixed and $p=p_n\le n^A$ for some $A\ge1$; the prior $\mathrm{BB}(1,p)$ with any cap $k_{\max}\ge s_0$; $\|\mu\|^2/n\le M$; $\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2>0$ where $\Gamma_{S_0}=G_{S_0}/n$. When $s_0=0$ the last condition is vacuous and $\mu=0$.

**The quantity through which the design enters.**
$$
\delta:=\beta^{\star\top}_{S_0}\Lambda_{S_0}\beta^\star_{S_0}=\frac{\|\mu\|^2+\|\beta^\star_{S_0}\|^2}{n}\qquad(\delta=0\text{ if }s_0=0). \tag{0.2}
$$

**The statement to be proved (T6, Theorem 4.2 of the draft).** Let $\omega_n\to\infty$ and
$$
m_n=\Big\lceil\frac{s_0\log(2p)+\frac{s_0+1}{2}\log n+\omega_n}{\log 2}\Big\rceil .
$$
Under the standing assumptions, $\Pi(|S|>m_n\mid y)\to0$ in probability. In particular, with $\omega_n=\log\log n$ (any $\omega_n\to\infty$ with $\omega_n=O(\log n)$ works) and $p\le n^A$, the posterior lives on models of size $O(\log n)$; this holds under the operational cap $\lfloor n/2\rfloor$, with no condition on the design beyond the standing assumptions.

**Roadmap.** Divide numerator and denominator of $\Pi(|S|>m_n\mid y)$ by $f_0(y)$. The numerator $\sum_{|S|>m_n}p(S)m(S)/f_0(y)$ has $\mathbb P_0$-expectation exactly $p(|S|>m_n)$, because every $m(S)$ is a probability density in $y$ (Section 1); the $\mathrm{BB}(1,p)$ tail makes this at most $2^{1-m_n}$ (Section 2). The denominator is at least $p(S_0)m(S_0)/f_0(y)$, which is bounded below by $(2p)^{-s_0}n^{-(s_0+1)/2}e^{-K}$ outside an event of probability at most $8/n$, with an explicit constant $K$ (Section 3). The choice of $m_n$ makes the ratio $O_{\mathbb P}(e^{-\omega_n})$ (Section 4).

---

## 1. The marginal likelihood is a density, and the exact Markov identity

**Lemma 1.** For every model $S$, the function $y\mapsto m(S)(y)$ is a probability density on $\mathbb R^n$, and it is given by (0.1). Moreover $Q_S\ge0$ for every $y$.

*Proof.* By definition of the marginal likelihood,
$$
m(S)(y)=\int_0^\infty\!\!\int_{\mathbb R^k}\phi_n\big(y;X_S\beta,vI_n\big)\,\phi_k\big(\beta;0,v\Lambda_S^{-1}\big)\,g(v)\,d\beta\,dv,
$$
where $\phi_d(\cdot;a,\Sigma)$ is the $N_d(a,\Sigma)$ density (for $k=0$ the inner integral is absent). The integrand is nonnegative and each factor integrates to one in its own variable, so Tonelli's theorem gives $\int_{\mathbb R^n}m(S)(y)\,dy=1$.

For the closed form, fix $v$. Under the model, $y=X_S\beta+e$ with $\beta\sim N_k(0,v\Lambda_S^{-1})$ and $e\sim N_n(0,vI_n)$ independent, so $y\mid v\sim N_n(0,v\Sigma_S)$ with $\Sigma_S=I_n+X_S\Lambda_S^{-1}X_S^\top\succ0$. By the identity $\det(I_n+AB)=\det(I_k+BA)$,
$$
\det\Sigma_S=\det\big(I_k+\Lambda_S^{-1}G_S\big)=\frac{\det(\Lambda_S+G_S)}{\det\Lambda_S}
=\frac{\det\big(\tfrac1n((n+1)G_S+I_k)\big)}{\det\big(\tfrac1n(G_S+I_k)\big)}=\frac{\det H_S}{\det(G_S+I_k)}=D_S,
$$
since $\Lambda_S+G_S=\frac1n\big((n+1)G_S+I_k\big)=H_S/n$. By the Woodbury identity $(I_n+UCV)^{-1}=I_n-U(C^{-1}+VU)^{-1}V$ with $U=X_S$, $C=\Lambda_S^{-1}$, $V=X_S^\top$,
$$
\Sigma_S^{-1}=I_n-X_S(\Lambda_S+G_S)^{-1}X_S^\top=I_n-n\,X_SH_S^{-1}X_S^\top,
\qquad\text{so}\qquad
y^\top\Sigma_S^{-1}y=y^\top y-n\,z_S^\top H_S^{-1}z_S=Q_S .
$$
In particular $Q_S=y^\top\Sigma_S^{-1}y\ge0$. Hence
$$
m(S)(y)=\int_0^\infty(2\pi v)^{-n/2}D_S^{-1/2}e^{-Q_S/(2v)}\,\frac{b_0^{a_0}}{\Gamma(a_0)}v^{-a_0-1}e^{-b_0/v}\,dv
=(2\pi)^{-n/2}D_S^{-1/2}\frac{b_0^{a_0}}{\Gamma(a_0)}\int_0^\infty v^{-\nu-1}e^{-c/v}\,dv,
$$
with $c=b_0+Q_S/2>0$. The substitution $u=c/v$ gives $\int_0^\infty v^{-\nu-1}e^{-c/v}dv=c^{-\nu}\Gamma(\nu)$, and $c^{-\nu}=2^{\nu}(2b_0+Q_S)^{-\nu}=2^{a_0}2^{n/2}(2b_0+Q_S)^{-\nu}$. Collecting the constants, $(2\pi)^{-n/2}2^{n/2}=\pi^{-n/2}$ and $b_0^{a_0}2^{a_0}=(2b_0)^{a_0}$, which is (0.1). For $k=0$, $\Sigma_\emptyset=I_n$, $D_\emptyset=1$ and $Q_\emptyset=y^\top y$, and the same computation applies. $\blacksquare$

**Proposition 2 (exact Markov identity).** For every set $\mathcal A$ of models, every $p\ge1$, every design $X$, every cap $k_{\max}$, every $\beta^\star$ and every $\sigma_\star^2>0$,
$$
\mathbb E_0\Big[\sum_{S\in\mathcal A}\frac{p(S)\,m(S)(y)}{f_0(y)}\Big]=p(\mathcal A). \tag{1.1}
$$
Consequently, for every $t>0$,
$$
\mathbb P_0\Big(\sum_{S\in\mathcal A}\frac{p(S)\,m(S)(y)}{f_0(y)}>t\,p(\mathcal A)\Big)\le\frac1t. \tag{1.2}
$$

*Proof.* Since $f_0>0$ on $\mathbb R^n$, for every measurable $h\ge0$ one has $\mathbb E_0[h(y)/f_0(y)]=\int_{\mathbb R^n}\frac{h(y)}{f_0(y)}f_0(y)\,dy=\int_{\mathbb R^n}h(y)\,dy$. Apply this to $h=m(S)$ (Lemma 1: $\int m(S)=1$), multiply by $p(S)$ and sum over the finitely many $S\in\mathcal A$; this is (1.1). (1.2) is Markov's inequality applied to the nonnegative variable on the left of (1.1). $\blacksquare$

*Remark 1.1.* (1.1) is an identity, not a bound. Neither the number $|\mathcal A|$ of models in the class, nor the design, nor the signal appears on the right: only the prior mass of the class (which depends on $p$ only through the prior, and which, for the tail classes $\{|S|>m\}$, Lemma 3(c) bounds free of $p$). This is the whole content of the numerator part of T6, and it is what resolves the counting objection (Section 6).

---

## 2. The $\mathrm{BB}(1,p)$ prior: the parts of Lemma L6 that are used

Let $\mathbb P_{\mathrm{BB}}$ denote the uncapped law on subsets of $[p]$ with $\mathbb P_{\mathrm{BB}}(\{S\})=w(|S|)$, and $K=|S|$ its size under this law. (That $\mathbb P_{\mathrm{BB}}$ is a probability law is part (b) below. The letter $K$ is used for this random size only in this section; from Section 3 on, $K$ is the constant of Proposition 7.)

**Lemma 3.** Let $p\ge1$.

(a) For $0\le k\le p$,
$$
w(k)=\frac{p\;k!}{\prod_{i=0}^{k}(2p-i)};\qquad\text{in particular } w(0)=\tfrac12\ \text{ and }\ w(k)\ge\frac{k!}{2\,(2p)^k}.
$$

(b) $\sum_{S\subseteq[p]}w(|S|)=1$. Hence, for every cap $k_{\max}\in\{0,\dots,p\}$, $\tfrac12\le W\le1$; $p(S)\ge w(|S|)$ whenever $|S|\le k_{\max}$; and $p(\mathcal A)\le2\,\mathbb P_{\mathrm{BB}}(\mathcal A)$ for every $\mathcal A$.

(c) For every integer $m$, $\mathbb P_{\mathrm{BB}}(K\ge m)\le2^{1-m}$. Hence, for every cap, $p(|S|>m)\le2^{1-m}$; with no cap, $p(|S|>m)\le2^{-m}$. (For $m\le0$ these bounds are trivial, as the left sides are at most $1$.)

(d) If $s_0\le k_{\max}$, then $\log p(S_0)\ge\log s_0!-\log2-s_0\log(2p)\ge-\log2-s_0\log(2p)$.

*Proof.* (a) With $B(x,z)=\Gamma(x)\Gamma(z)/\Gamma(x+z)$: $B(1,p)=\Gamma(p)/\Gamma(p+1)=1/p$, and $B(1+k,2p-k)=k!\,\Gamma(2p-k)/\Gamma(2p+1)=k!\,(2p-k-1)!/(2p)!$, where $2p-k\ge p\ge1$ because $k\le p$. Since $(2p)!/(2p-k-1)!=\prod_{i=0}^{k}(2p-i)$, the formula follows. For $k=0$ it gives $p/(2p)=\frac12$. Each factor satisfies $2p-i\le2p$, whence $w(k)\ge p\,k!/(2p)^{k+1}=k!/(2(2p)^k)$.

(b) The $\mathrm{Beta}(1,p)$ density is $(1-\theta)^{p-1}/B(1,p)$ on $(0,1)$, and $w(k)=\int_0^1\theta^k(1-\theta)^{p-k}\,\frac{(1-\theta)^{p-1}}{B(1,p)}\,d\theta$ by the definition of the Beta function. Therefore
$$
\sum_{S\subseteq[p]}w(|S|)=\int_0^1\Big[\sum_{k=0}^p\binom pk\theta^k(1-\theta)^{p-k}\Big]\frac{(1-\theta)^{p-1}}{B(1,p)}\,d\theta=\int_0^1\frac{(1-\theta)^{p-1}}{B(1,p)}\,d\theta=1 .
$$
Thus $W=\sum_{k\le k_{\max}}\binom pkw(k)\le\sum_{k\le p}\binom pkw(k)=1$, and $W\ge\binom p0w(0)=\frac12$. For $|S|\le k_{\max}$, $p(S)=w(|S|)/W\ge w(|S|)$. For any $\mathcal A$, $p(\mathcal A)=\mathbb P_{\mathrm{BB}}(\mathcal A\cap\{|S|\le k_{\max}\})/W\le2\,\mathbb P_{\mathrm{BB}}(\mathcal A)$.

(c) $\mathbb P_{\mathrm{BB}}(K=k)=\binom pkw(k)$. For $0\le k\le p-1$, by (a),
$$
\frac{\mathbb P_{\mathrm{BB}}(K=k+1)}{\mathbb P_{\mathrm{BB}}(K=k)}=\frac{\binom p{k+1}}{\binom pk}\cdot\frac{w(k+1)}{w(k)}=\frac{p-k}{k+1}\cdot\frac{k+1}{2p-k-1}=\frac{p-k}{2p-k-1},
$$
and $\frac{p-k}{2p-k-1}\le\frac12$ if and only if $2p-2k\le2p-k-1$, i.e. $k\ge1$. (At $k=0$ the ratio is $p/(2p-1)\ge\frac12$, with equality only in the limit, so the geometric decay starts at $k=1$, as L6(ii) says.) Hence $\mathbb P_{\mathrm{BB}}(K=k)\le2^{-(k-1)}\,\mathbb P_{\mathrm{BB}}(K=1)$ for every $k\ge1$ (trivially for $k>p$). For $m\ge1$,
$$
\mathbb P_{\mathrm{BB}}(K\ge m)\le\mathbb P_{\mathrm{BB}}(K=1)\sum_{k\ge m}2^{1-k}=2^{2-m}\,\mathbb P_{\mathrm{BB}}(K=1)\le2^{1-m},
$$
because $\mathbb P_{\mathrm{BB}}(K=1)\le1-\mathbb P_{\mathrm{BB}}(K=0)=1-w(0)=\frac12$. For $m\le0$ the claim reads $1\le2^{1-m}$. Finally, by (b), $p(|S|>m)\le2\,\mathbb P_{\mathrm{BB}}(K\ge m+1)\le2\cdot2^{-m}=2^{1-m}$; with no cap $W=1$ and $p(|S|>m)=\mathbb P_{\mathrm{BB}}(K\ge m+1)\le2^{-m}$.

(d) By (b) and (a), $p(S_0)\ge w(s_0)\ge s_0!/(2(2p)^{s_0})$, and $s_0!\ge1$. $\blacksquare$

*Correspondence with L6.* (a) is L6(i) specialised to $b_\pi=p$ and L6(v)'s formula; (c) is L6(iii) together with L6(iv); (d) is L6(v). Nothing else from L6 is needed.

---

## 3. The denominator: a lower bound for $p(S_0)m(S_0)/f_0(y)$

Write
$$
E:=\frac{\|\varepsilon\|^2}{\sigma_\star^2}=\sum_{i=1}^n\Big(\frac{\varepsilon_i}{\sigma_\star}\Big)^2 .
$$
$E$ is a sum of $n$ independent squared standard normals, so $E>0$ almost surely, $\mathbb E_0E=n$ and $\mathrm{Var}_0E=2n$ (since $\mathrm{Var}(\xi^2)=\mathbb E\xi^4-1=2$ for $\xi\sim N(0,1)$). Also
$$
f_0(y)=(2\pi\sigma_\star^2)^{-n/2}e^{-E/2}. \tag{3.0}
$$

**Lemma 4 (the fit of the true model).** For every model $S$,
$$
Q_S=\min_{b\in\mathbb R^k}\Big\{\|y-X_Sb\|^2+b^\top\Lambda_Sb\Big\}\qquad(\text{for }k=0\text{, }Q_\emptyset=y^\top y). \tag{3.1}
$$
Consequently
$$
Q_{S_0}\le\|\varepsilon\|^2+\delta=\sigma_\star^2E+\delta, \tag{3.2}
$$
with $\delta$ as in (0.2). Under the standing assumptions, $\delta\le M\big(1+\tfrac{1}{n\varphi_0^2}\big)\le M(1+\varphi_0^{-2})$.

*Proof.* The function $b\mapsto\|y-X_Sb\|^2+b^\top\Lambda_Sb=y^\top y-2b^\top z_S+b^\top(G_S+\Lambda_S)b$ is a strictly convex quadratic, because $G_S+\Lambda_S\succeq\Lambda_S\succ0$. Its minimiser solves $(G_S+\Lambda_S)b=z_S$, i.e. $b^\ast=(G_S+\Lambda_S)^{-1}z_S=nH_S^{-1}z_S$, and the minimum value is $y^\top y-b^{\ast\top}z_S=y^\top y-n\,z_S^\top H_S^{-1}z_S=Q_S$. This is (3.1).

Take $S=S_0$ and the admissible point $b=\beta^\star_{S_0}$ in (3.1): $\|y-X_{S_0}\beta^\star_{S_0}\|^2=\|y-\mu\|^2=\|\varepsilon\|^2$, and
$$
\beta^{\star\top}_{S_0}\Lambda_{S_0}\beta^\star_{S_0}=\frac1n\Big(\beta^{\star\top}_{S_0}G_{S_0}\beta^\star_{S_0}+\|\beta^\star_{S_0}\|^2\Big)=\frac{\|\mu\|^2+\|\beta^\star_{S_0}\|^2}{n}=\delta,
$$
which gives (3.2). Under the standing assumptions, $\|\mu\|^2/n\le M$, and $\|\mu\|^2=\beta^{\star\top}_{S_0}G_{S_0}\beta^\star_{S_0}=n\,\beta^{\star\top}_{S_0}\Gamma_{S_0}\beta^\star_{S_0}\ge n\varphi_0^2\|\beta^\star_{S_0}\|^2$, so $\|\beta^\star_{S_0}\|^2\le M/\varphi_0^2$ and $\delta\le M+M/(n\varphi_0^2)$. $\blacksquare$

*Where the two assumptions enter.* This is the only place in the proof of T6 where $\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2$ and $\|\mu\|^2/n\le M$ are used, and they are used only to bound $\delta$ (the heuristic comparison in Section 6.2 also invokes $\|\mu\|^2/n\le M$). The quantity $\delta$ is the exponent of the coefficient prior at the truth: the $N_{s_0}(0,\sigma^2\Lambda_{S_0}^{-1})$ density evaluated at $\beta^\star_{S_0}$ is proportional to $\exp(-\delta/(2\sigma^2))$. The eigenvalue condition converts the signal bound into a bound on $\|\beta^\star_{S_0}\|^2$; the design enters in no other way, which is the sense in which the $g=n$ prior is design-adapted.

**Lemma 5 (a Stirling-type lower bound).** For every real $x\ge1$,
$$
\log\Gamma(x)\ge\big(x-\tfrac12\big)\log x-x-\tfrac32 .
$$

*Proof.* $\Gamma(x)=\int_0^\infty v^{x-1}e^{-v}dv\ge\int_x^{x+\sqrt x}v^{x-1}e^{-v}dv$. Write $v=x+s$ with $0\le s\le\sqrt x$. Since $\log(1+u)\ge u-u^2/2$ for $u\ge0$ (the difference vanishes at $0$ and has derivative $u^2/(1+u)\ge0$) and $x-1\ge0$,
$$
\log\big(v^{x-1}e^{-v}\big)=(x-1)\log x+(x-1)\log\Big(1+\frac sx\Big)-x-s
\ge(x-1)\log x+(x-1)\Big(\frac sx-\frac{s^2}{2x^2}\Big)-x-s
\ge(x-1)\log x-x-\frac sx-\frac{s^2}{2x}.
$$
For $0\le s\le\sqrt x$ the last two terms are at least $-x^{-1/2}-\tfrac12\ge-\tfrac32$. Integrating over an interval of length $\sqrt x$ gives $\Gamma(x)\ge\sqrt x\;x^{x-1}e^{-x}e^{-3/2}$. $\blacksquare$

(The classical Stirling bound $\Gamma(x)\ge\sqrt{2\pi}\,x^{x-1/2}e^{-x}$ would replace $-\frac32$ by $+\frac12\log(2\pi)$; the weaker self-contained version suffices.)

**Lemma 6 (the determinant term).** For every model $S$ and every design, $1\le D_S\le(n+1)^{|S|}$.

*Proof.* Let $\lambda_1,\dots,\lambda_k\ge0$ be the eigenvalues of $G_S$. The matrices $H_S=(n+1)G_S+I_k$ and $G_S+I_k$ are diagonalised by the same orthogonal matrix, so $D_S=\prod_{i=1}^k\frac{(n+1)\lambda_i+1}{\lambda_i+1}$, and for $\lambda\ge0$, $1\le\frac{(n+1)\lambda+1}{\lambda+1}\le\frac{(n+1)(\lambda+1)}{\lambda+1}=n+1$. $\blacksquare$

**Proposition 7 (denominator lower bound).** Let $n\ge2$ and $s_0\le k_{\max}$. Put
$$
R:=\frac{p(S_0)\,m(S_0)(y)}{f_0(y)},\qquad
K:=\log2+\frac32+a_0\log\frac{\sigma_\star^2}{b_0}+\log\Gamma(a_0)+\frac12\log(1+a_0)+\frac{s_0}{4}+\frac{(1+a_0)(2b_0+\delta)}{\sigma_\star^2}. \tag{3.3}
$$
Let $\mathcal E:=\{E\ge n/2\}$. Then $\mathbb P_0(\mathcal E)\ge1-8/n$, and on $\mathcal E$,
$$
\log R\ \ge\ -s_0\log(2p)-\frac{s_0+1}{2}\log n-K,\qquad\text{i.e.}\qquad R\ge(2p)^{-s_0}\,n^{-(s_0+1)/2}\,e^{-K}. \tag{3.4}
$$
In the language of the prover note, the "$O_{\mathbb P}(1)$ term" is the deterministic constant $K$, valid outside an event of probability at most $8/n$. $K$ depends on $(a_0,b_0,\sigma_\star^2,s_0,\delta)$ only; under the standing assumptions $\delta\le M(1+\varphi_0^{-2})$, so $K\le K_\star$, where $K_\star$ is (3.3) with $\delta$ replaced by $M(1+\varphi_0^{-2})$, a constant depending only on $(a_0,b_0,\sigma_\star^2,M,\varphi_0,s_0)$.

*Proof.* By (0.1) and (3.0),
$$
\log\frac{m(S_0)}{f_0(y)}=\log\Gamma(\nu)-\log\Gamma(a_0)+a_0\log(2b_0)-\frac n2\log\pi+\frac n2\log(2\pi\sigma_\star^2)+\frac E2-\frac12\log D_{S_0}-\nu\log(2b_0+Q_{S_0}). \tag{3.5}
$$

*Step 1 (the fit).* By (3.2), $2b_0+Q_{S_0}\le\sigma_\star^2E+(2b_0+\delta)=\sigma_\star^2E\big(1+\frac{2b_0+\delta}{\sigma_\star^2E}\big)$, and $\log(1+x)\le x$ for $x\ge0$, so
$$
\nu\log(2b_0+Q_{S_0})\le\nu\log\sigma_\star^2+\nu\log E+\frac{\nu(2b_0+\delta)}{\sigma_\star^2E}. \tag{3.6}
$$

*Step 2 (the variance integral).* Since $n\ge2$, $\nu=a_0+n/2\ge1$ and Lemma 5 applies: $\log\Gamma(\nu)\ge(\nu-\frac12)\log\nu-\nu-\frac32$. Write $E=2\nu u$ with $u>0$. Then
$$
\nu\log\nu-\nu+\frac E2-\nu\log E=\nu\log\nu-\nu+\nu u-\nu\log(2\nu u)=-\nu\log2+\nu\,(u-1-\log u)\ \ge\ -\nu\log2, \tag{3.7}
$$
because $\log u\le u-1$ for $u>0$.

*Step 3 (collecting).* Insert (3.6) and Lemma 5 into (3.5) and use (3.7):
$$
\log\frac{m(S_0)}{f_0(y)}\ge-\frac12\log\nu-\frac32-\nu\log2-\log\Gamma(a_0)+a_0\log(2b_0)+\frac n2\log(2\sigma_\star^2)-\nu\log\sigma_\star^2-\frac12\log D_{S_0}-\frac{\nu(2b_0+\delta)}{\sigma_\star^2E},
$$
where $-\frac n2\log\pi+\frac n2\log(2\pi\sigma_\star^2)=\frac n2\log(2\sigma_\star^2)$. Since $\nu=a_0+\frac n2$,
$$
-\nu\log2+\frac n2\log(2\sigma_\star^2)-\nu\log\sigma_\star^2=-a_0\log2-a_0\log\sigma_\star^2=-a_0\log(2\sigma_\star^2),
\qquad
-a_0\log(2\sigma_\star^2)+a_0\log(2b_0)=-a_0\log\frac{\sigma_\star^2}{b_0}.
$$
Hence, for every $y$ with $E>0$, i.e. for every $y\ne\mu$, hence almost surely (this is a deterministic inequality; no probability has been used yet),
$$
\log\frac{m(S_0)}{f_0(y)}\ \ge\ -\frac12\log\nu-\frac12\log D_{S_0}-\frac{\nu(2b_0+\delta)}{\sigma_\star^2E}-\Big[\frac32+a_0\log\frac{\sigma_\star^2}{b_0}+\log\Gamma(a_0)\Big]. \tag{3.8}
$$

*Step 4 (the $\log n$ terms).* By Lemma 6, $\frac12\log D_{S_0}\le\frac{s_0}2\log(n+1)=\frac{s_0}2\log n+\frac{s_0}2\log\big(1+\frac1n\big)\le\frac{s_0}2\log n+\frac{s_0}{2n}\le\frac{s_0}2\log n+\frac{s_0}4$ (as $n\ge2$). And $\nu=a_0+\frac n2\le n(1+a_0)$, so $\frac12\log\nu\le\frac12\log n+\frac12\log(1+a_0)$.

*Step 5 (the event).* By Chebyshev's inequality, $\mathbb P_0(E<n/2)\le\mathbb P_0(|E-n|\ge n/2)\le\frac{\mathrm{Var}_0E}{(n/2)^2}=\frac{2n}{n^2/4}=\frac8n$. On $\mathcal E$, $\frac{\nu}{E}\le\frac{a_0+n/2}{n/2}=1+\frac{2a_0}{n}\le1+a_0$, so $\frac{\nu(2b_0+\delta)}{\sigma_\star^2E}\le\frac{(1+a_0)(2b_0+\delta)}{\sigma_\star^2}$.

*Step 6 (the prior).* By Lemma 3(d), $\log p(S_0)\ge-\log2-s_0\log(2p)$.

Adding Step 6 to (3.8) and using Steps 4 and 5 gives, on $\mathcal E$,
$$
\log R\ge-s_0\log(2p)-\log2-\frac{s_0}2\log n-\frac{s_0}4-\frac12\log n-\frac12\log(1+a_0)-\frac{(1+a_0)(2b_0+\delta)}{\sigma_\star^2}-\frac32-a_0\log\frac{\sigma_\star^2}{b_0}-\log\Gamma(a_0),
$$
which is (3.4) with $K$ as in (3.3). The bound on $\delta$ is Lemma 4. $\blacksquare$

*Remark 3.1 (what each ingredient contributes).* The factor $(2p)^{-s_0}$ is the prior mass of $S_0$ (Lemma 3(d)); $n^{-s_0/2}$ is the Occam factor $D_{S_0}^{-1/2}$ of the $s_0$ coefficients (Lemma 6); the extra $n^{-1/2}$ is the Occam factor of the integrated variance, visible as $-\frac12\log\nu$ in Step 2, where the $\chi^2$ fluctuation $\nu(u-1-\log u)$ was dropped (it is $O_{\mathbb P}(1)$, but the inequality needs only its sign). The signal costs $e^{-(1+a_0)(2b_0+\delta)/\sigma_\star^2}$, through the prior density at $\beta^\star$. This matches the usual Laplace heuristic $m(S_0)/f_0(y)\asymp n^{-(s_0+1)/2}$ without any expansion.

---

## 4. Proof of Theorem T6

**Theorem 8 (nonasymptotic form of T6).** Let $n\ge2$, $p\ge1$, let $X$, $\beta^\star$, $\sigma_\star^2>0$ and the cap $k_{\max}\ge s_0$ be arbitrary, and let $K$ be as in (3.3). Then for every integer $m$ and every $t>0$,
$$
\mathbb P_0\Big(\Pi(|S|>m\mid y)\ >\ 2t\,e^{K}\,2^{-m}(2p)^{s_0}n^{(s_0+1)/2}\Big)\ \le\ \frac1t+\frac8n. \tag{4.1}
$$

*Proof.* Since $s_0\le k_{\max}$, $p(S_0)>0$, and $m(S_0)(y)>0$ by (0.1); hence $Z\ge p(S_0)m(S_0)>0$. Dividing numerator and denominator by $f_0(y)>0$,
$$
\Pi(|S|>m\mid y)=\frac{\sum_{|S|>m}p(S)m(S)(y)}{Z}\le\frac{\sum_{|S|>m}p(S)m(S)(y)}{p(S_0)m(S_0)(y)}=\frac{N}{R},
\qquad N:=\sum_{|S|>m}\frac{p(S)\,m(S)(y)}{f_0(y)},
$$
with $R$ as in Proposition 7. By Proposition 2 with $\mathcal A=\{|S|>m\}$ and Lemma 3(c), $\mathbb E_0N=p(|S|>m)\le2^{1-m}$, so by Markov's inequality $\mathbb P_0(N>t\,2^{1-m})\le1/t$. On the event $\{N\le t\,2^{1-m}\}\cap\mathcal E$, Proposition 7 gives
$$
\frac NR\le t\,2^{1-m}\,(2p)^{s_0}n^{(s_0+1)/2}e^{K}.
$$
The complement of that event has probability at most $1/t+8/n$. $\blacksquare$

**Proof of T6.** Take $m=m_n$ (an integer, possibly negative for finitely many $n$ if $\omega_n$ starts very negative; Theorem 8 covers every integer $m$). By the definition of $m_n$, $m_n\log2\ge s_0\log(2p)+\frac{s_0+1}2\log n+\omega_n$, i.e.
$$
2^{-m_n}(2p)^{s_0}n^{(s_0+1)/2}\le e^{-\omega_n}. \tag{4.2}
$$
Under the standing assumptions, $k_{\max}\ge s_0$ and $K\le K_\star$ (Proposition 7), where $K_\star$ depends only on $(a_0,b_0,\sigma_\star^2,M,\varphi_0,s_0)$, all of which are fixed as $n\to\infty$, and not on $n$, $p$, $X$ or $\beta^\star$. By (4.1) and (4.2), for every $t>0$ and every $n\ge2$,
$$
\mathbb P_0\Big(\Pi(|S|>m_n\mid y)>2t\,e^{K_\star}e^{-\omega_n}\Big)\le\frac1t+\frac8n. \tag{4.3}
$$
Fix $\epsilon>0$ and take $t=t_n:=e^{\omega_n/2}$ in (4.3): since $\omega_n\to\infty$, the threshold $2e^{K_\star}e^{-\omega_n/2}$ is below $\epsilon$ for all large $n$, so
$$
\mathbb P_0\big(\Pi(|S|>m_n\mid y)>\epsilon\big)\le e^{-\omega_n/2}+\frac8n\longrightarrow0 .
$$
This is $\Pi(|S|>m_n\mid y)\to0$ in probability. (4.3) says more: $\Pi(|S|>m_n\mid y)=O_{\mathbb P}(e^{-\omega_n})$.

*The "in particular" clause.* With $p\le n^A$, $s_0$ and $A$ fixed, and $\omega_n=O(\log n)$ (e.g. $\omega_n=\log\log n$),
$$
m_n\le\frac{s_0\big(A\log n+\log2\big)+\frac{s_0+1}{2}\log n+\omega_n}{\log2}+1\le C\log n\quad\text{for all large }n,
$$
with $C$ depending on $(s_0,A)$ and the constant in $\omega_n=O(\log n)$; hence $\Pi(|S|>C\log n\mid y)\le\Pi(|S|>m_n\mid y)\to0$ in probability, which is the clause. The cap enters only through $k_{\max}\ge s_0$; for the operational cap $k_{\max}=\lfloor n/2\rfloor$ this holds as soon as $n\ge2s_0$. The design enters only through Lemma 4. If $m_n\ge k_{\max}$ the posterior probability in question is zero and the statement is trivial. $\blacksquare$

*Remark 4.1 (uniformity).* (4.1) holds for every $n\ge2$, with no limit taken. Its right side, $1/t+8/n$, does not involve $p$, $X$, $\beta^\star$, $k_{\max}$ or $\delta$; the threshold on the left involves $p$ explicitly (through $(2p)^{s_0}$, which $m_n$ is built to absorb) and involves $X$ and $\beta^\star$ only through $K$, i.e. through $\delta$. So, after the substitution $m=m_n$, (4.3) holds uniformly over all designs and all $\beta^\star$ with $\delta\le M(1+\varphi_0^{-2})$, over all $p\ge1$, and over all caps $k_{\max}\ge s_0$, with $(a_0,b_0,\sigma_\star^2,M,\varphi_0,s_0)$ fixed. The bound is also explicit in $s_0$ (through $s_0/4$ in $K$, the discarded $\log s_0!$, and the factor $(2p)^{s_0}n^{(s_0+1)/2}$ already in $m_n$), so for the convergence statement "$s_0$ fixed" is a convenience: $s_0=s_{0,n}$ may grow provided $m_n$ is computed with the actual $s_{0,n}$, $k_{\max}\ge s_{0,n}$, $(a_0,b_0,\sigma_\star^2,M,\varphi_0)$ stay fixed, and $\omega_n-s_{0,n}/4\to\infty$ (the $s_{0,n}/4$ is a rounding artefact of Step 4: keeping $\frac{s_0}{2}\log(n+1)$ in place of $\frac{s_0}{2}\log n$ leaves the factor $(1+\frac1n)^{s_0/2}\le e^{1/2}$, since $s_0\le n$ whenever $\lambda_{\min}(\Gamma_{S_0})>0$). The "in particular" clause $m_n=O(\log n)$ does use $s_0$ fixed.

---

## 5. Corollary T9a(i)

**Statement (draft, Corollary 4.7(i)), three sentences.** (1) T6's conclusion holds for every $p$ (the condition $p\le n^A$ is not used) and for every cap $k_{\max}\ge s_0$, including no cap ($k_{\max}=p$). (2) With $\omega_n=O(\log n)$, $m_n=O(s_0\ell_n)$. (3) The prior itself enforces the dimension bound: no prior cap is needed. Here $\ell_n=\log(p\vee n)$, as defined in the draft just before Theorem T9 (Section 4, "The joint posterior").

**Verification.** Every step of Sections 1 to 4 is checked against the two generalisations.

1. *Every $p$.* Lemma 1 and Proposition 2 hold for every $p\ge1$ and every design (Remark 1.1). Lemma 3 holds for every $p\ge1$; $p$ enters its conclusions only through the explicit factor $(2p)^{-s_0}$ in (d). Lemmas 4 to 6 and Proposition 7 do not involve $p$ except through Lemma 3(d). Theorem 8 is stated for arbitrary $p\ge1$ and its right side is free of $p$. The proof of T6 from Theorem 8 uses only (4.2), which is the definition of $m_n$ and holds for every $p$. Nowhere is $p$ compared with $n$. Hence T6 holds for every sequence $p=p_n\ge1$, including $p_n$ growing exponentially or faster in $n$, with $m_n$ as defined (which then grows accordingly; when $m_n\ge k_{\max}$ the statement is trivially true).

2. *Every cap $k_{\max}\ge s_0$, including none.* The cap enters at three points: $p(S_0)>0$, which needs $s_0\le k_{\max}$ (Theorem 8 and Lemma 3(d)); $p(S_0)\ge w(s_0)$, which uses $W\le1$ (Lemma 3(b), valid for every cap); and $p(|S|>m)\le2^{1-m}$, which uses $W\ge\frac12$ (Lemma 3(c), valid for every cap). With no cap, $W=1$, Lemma 3(c) gives $p(|S|>m)\le2^{-m}$, and (4.1) holds with $2t$ replaced by $t$. So the conclusion holds for every $k_{\max}\in\{s_0,\dots,p\}$. The prior tail $2^{-m}$ (Lemma 3(c)) is what enforces the dimension bound; the cap is not needed for it.

3. *The order of $m_n$.* Let $\omega_n\le c\log n$ for a constant $c$ and let $s_0\ge1$. Since $\log(2p)\le\log2+\ell_n$, $\log n\le\ell_n$ and $\frac{s_0+1}{2}\le s_0$,
$$
m_n\le\frac{s_0\log2+s_0\ell_n+s_0\ell_n+c\,\ell_n}{\log2}+1=\frac{(2s_0+c)\,\ell_n}{\log2}+s_0+1=O(s_0\ell_n).
$$
If $s_0=0$, then $m_n=\lceil(\frac12\log n+\omega_n)/\log2\rceil=O(\ell_n)$, which is not $O(s_0\ell_n)=O(0)$: the $\frac12\log n$ from the integrated variance is present whatever $s_0$ is (counterexample to the literal statement: $s_0=0$, $p=1$, $\omega_n=\log\log n$). The accurate general statement is $m_n=O\big((s_0+1)\ell_n\big)$, which coincides with the draft's $O(s_0\ell_n)$ for $s_0\ge1$. This is an error in the wording of the corollary, not in T6, and the draft should be corrected.

4. *The remark in the prover note.* "The Markov identity, L6(iii) and L6(v) are free of $p$, and the denominator bound concerns $S_0$ alone. Without a cap, use L6(iii) directly; with a cap, L6(iv)." This is exactly the structure of items 1 and 2 above, and it is confirmed.

**Conclusion.** Sentences (1) and (3) of Corollary T9a(i) (every $p$; every cap including none; the prior's tail, not the cap, enforces the bound) are verified as stated (items 1 and 2). Sentence (2) is verified in the corrected form $m_n=O((s_0+1)\ell_n)$, which equals the draft's $O(s_0\ell_n)$ whenever $s_0\ge1$; as literally written it fails at $s_0=0$ (item 3). $\blacksquare$

---

## 6. The counting objection

The prover note records an earlier objection and asks that it be checked. This section states the objection in its strongest form, shows what the shrinkage floor (2) of the draft does and does not do against it, shows that the exact identity (1.1) disposes of it throughout the range of $p$ covered by the standing assumptions (and well beyond, up to $\log p$ of order $n$), and records a reviewer's construction indicating that for super-exponential $p$ the objection's scenario does occur, without contradicting T6.

### 6.1 The objection

Fix $k$ of order $n/2$ and suppose $p\gg n$. There are $\binom pk$ models of size $k$. For a generic design, some of them fit $y$ almost perfectly, in the sense that $\|(I-P_S)y\|^2$ is a vanishing fraction of $y^\top y$; their marginal likelihoods then look enormous, since $(2b_0+Q_S)^{-\nu}$ with $\nu\approx n/2$ is very sensitive to $Q_S$. The per-model prior weight $w(k)\approx k!/(2(2p)^k)$ decays only like $p^{-k}$, while the number of models grows like $\binom pk\approx(ep/k)^k$. Multiplying "number of models" by "best fit" by "prior per model", one concludes that the size-$k$ class outweighs $p(S_0)m(S_0)$ once $p$ is a large enough power of $n$; the note records the threshold $p\gg n^{3/2}$ from such a computation.

### 6.2 What the shrinkage floor does, and does not do

**Lemma 9 (the shrinkage floor, draft (2)).** For every model $S$ and every $y$, $0\le t_S\le\frac{n}{n+1}\|P_Sy\|^2$. Consequently
$$
Q_S\ \ge\ \frac{y^\top y}{n+1}\qquad\text{and}\qquad m(S)(y)\ \le\ (n+1)^{\nu}\,m(\emptyset)(y)\quad\text{for every }S. \tag{6.1}
$$

*Proof.* If $X_S=0$ (in particular if $k=0$) then $t_S=0$. Otherwise let $X_S=U\Sigma V^\top$ be a thin singular value decomposition: $r=\operatorname{rank}X_S\ge1$, $U\in\mathbb R^{n\times r}$ and $V\in\mathbb R^{k\times r}$ with orthonormal columns, $\Sigma=\operatorname{diag}(\sigma_1,\dots,\sigma_r)$ with all $\sigma_i>0$. Then $G_S=V\Sigma^2V^\top$, $H_S=(n+1)V\Sigma^2V^\top+I_k$, and one checks by multiplication that $H_S^{-1}=V\big((n+1)\Sigma^2+I_r\big)^{-1}V^\top+(I_k-VV^\top)$. Hence
$$
X_SH_S^{-1}X_S^\top=U\Sigma\big((n+1)\Sigma^2+I_r\big)^{-1}\Sigma U^\top=U\operatorname{diag}\Big(\frac{\sigma_i^2}{(n+1)\sigma_i^2+1}\Big)U^\top\ \preceq\ \frac1{n+1}UU^\top=\frac1{n+1}P_S,
$$
since $UU^\top$ is the orthogonal projection onto the column span of $X_S$. Therefore $t_S=n\,y^\top X_SH_S^{-1}X_S^\top y\le\frac n{n+1}\|P_Sy\|^2$, and $t_S\ge0$ because $H_S\succ0$. Then $Q_S=y^\top y-t_S\ge y^\top y-\frac{n}{n+1}\|P_Sy\|^2\ge\frac{y^\top y}{n+1}$, so $2b_0+Q_S\ge\frac{2b_0+y^\top y}{n+1}$, and by (0.1) with $D_S\ge1$ (Lemma 6), $m(S)\le C_n(n+1)^{\nu}(2b_0+y^\top y)^{-\nu}=(n+1)^{\nu}m(\emptyset)$. $\blacksquare$

*What the floor does.* It caps what interpolation can earn. A model may well interpolate $y$ in the least-squares sense ($\|(I-P_S)y\|=0$ is possible once $\operatorname{rank}X_S=n$, and $Q_S/y^\top y$ can be arbitrarily close to $1/(n+1)$ (strictly above it), e.g. $Q_S/\|y\|^2=(n+1)/(n^2+n+1)$ for $y$ in the span of one standardised column), but the shrinkage of the unit-information prior keeps $Q_S\ge y^\top y/(n+1)$, so the Bayes factor of any model is at most $(n+1)^{\nu}$, whatever $p$ is and however well $X_S$ spans $y$. So the objection's premise is only half right: least-squares near-interpolation exists, but its reward is bounded. (audit 2026-10-15) Precisely, writing $T=y^\top y$, the floor gives $2b_0+Q_S\ge2b_0+T/(n+1)$ and hence, with $D_S\ge1$, the sharper ceiling
$$
\mathrm{BF}(S)=\frac{m(S)}{m(\emptyset)}\le\Big(\frac{2b_0+T}{2b_0+T/(n+1)}\Big)^{\nu}\ \ \Big(\le(n+1)^{\nu}\Big),
$$
whereas an unshrunk fit with $Q_S\to0$ would reach $\big((2b_0+T)/(2b_0)\big)^{\nu}$. The unshrunk ceiling exceeds the sharper ceiling by the factor $\big(1+T/(2b_0(n+1))\big)^{\nu}$, which grows exponentially in $n$ when $T/n\to c>0$. (It need not exceed the looser ceiling $(n+1)^\nu$: their ratio is $\big((2b_0+T)/(2b_0(n+1))\big)^{\nu}$, which tends to zero exponentially when, e.g., $\mu=0$ and $\sigma_\star^2=b_0$; the earlier wording "enormous when $y^\top y\asymp n$" compared with the looser ceiling and was wrong in general.)

*What the floor does not do.* It does not, by itself, dispose of the objection's conclusion. Combined with counting it gives, for the class $\{|S|=k\}$,
$$
\sum_{|S|=k}p(S)m(S)\le p(|S|=k)\,(n+1)^{\nu}m(\emptyset)\le2^{2-k}(n+1)^{a_0+n/2}m(\emptyset)
$$
(Lemma 3(c) with $m=k-1$), and for $k\approx n/2$ the logarithm of the right side is $\frac n2\log n+O(n)$ relative to $\log m(\emptyset)$. Against this, the true model has $\log\big(m(S_0)/m(\emptyset)\big)=-\frac12\log D_{S_0}+\nu\log\frac{2b_0+y^\top y}{2b_0+Q_{S_0}}$, which is $O_{\mathbb P}(n)$ under the standing assumptions (because $y^\top y/n$ and $Q_{S_0}/n$ are both $O_{\mathbb P}(1)$ and bounded below by $\sigma_\star^2/2$ with probability tending to one). So on the exponential scale the floor-plus-counting bound, $\frac n2\log n$, exceeds the true model's $O_{\mathbb P}(n)$ for large $n$, and the deterministic route leaves the objection open. A different argument is needed.

### 6.3 Why the identity settles it in the polynomial regime, and beyond

Apply Proposition 2 to the class $\mathcal A_k=\{|S|=k\}$ (or to $\{|S|\ge k\}$):
$$
\mathbb E_0\Big[\sum_{|S|=k}\frac{p(S)m(S)(y)}{f_0(y)}\Big]=p(|S|=k)\le2^{2-k}.
$$
The number $\binom pk$ of models in the class does not appear, and nothing is assumed about $p$ or the design. The total weight of the class, relative to the true density, has expectation equal to its prior mass. By Markov, it exceeds $t\,2^{2-k}$ with probability at most $1/t$.

This is where the heuristic of 6.1 goes wrong. It bounds a sum by (number of terms) $\times$ (largest term) and then estimates the largest term by the fit of the best model in the class. But the best-fitting models form a $y$-dependent subset of the class of negligible prior mass. For every fixed model $S$, $m(S)(y)/f_0(y)$ has $\mathbb P_0$-expectation exactly $1$ (Lemma 1 and Proposition 2 with $\mathcal A=\{S\}$), whether $S$ is the truth or a size-$n/2$ noise model: a model that fits exceptionally well on one $y$ pays for it on the others, because $m(S)$ integrates to one. The extreme fit of the best model among $\binom pk$ is large precisely because the class is large, and the two effects cancel exactly in the prior-weighted sum; (1.1) is an equality.

The identity controls only the numerator $N$. Whether the class outweighs the true model is the comparison of $N$ with $R=p(S_0)m(S_0)/f_0(y)$, and both can be small with $R$ the smaller; so the identity settles the objection only together with the denominator bound of Proposition 7, and only in the range where Proposition 7's $(2p)^{-s_0}$ is not too small. That range is now made explicit.

*Quantitatively.* Combining the class bound with Proposition 7, for every integer $k\ge0$,
$$
\Pi(|S|\ge k\mid y)=O_{\mathbb P}\big(2^{-k}(2p)^{s_0}n^{(s_0+1)/2}\big),
$$
uniformly over designs and $\beta^\star$ with $\delta\le M(1+\varphi_0^{-2})$. Take $k=k_n\ge\frac n2-c$ for a constant $c$ (the objection's "size about $n/2$"). The bound tends to zero as soon as $s_0\log_2(2p)+\frac{s_0+1}{2}\log_2 n\le\frac n2-c-\omega_n/\log2$ with $\omega_n\to\infty$. For $s_0\ge1$ this holds for $\log p\le c'n$ with any $c'<\frac{\log2}{2s_0}$, which covers every polynomial regime $p\le n^A$ and more: there is no polynomial regime, and in particular no regime $p\gg n^{3/2}$ with $p$ polynomial, in which models of size about $n/2$ carry posterior mass. For $s_0=0$ the bound has no $p$-dependence at all and the class $\{|S|\ge k_n\}$ is negligible for every sequence $p_n$.

*What the identity does not say.* It does not say that no size-$n/2$ model fits well: on an event of probability at most $1/t$ the class may be heavy, which is what "in probability" allows. And it does not exclude the objection's scenario for every $p$, as the next subsection shows.

### 6.4 Beyond the exponential range the scenario is reported to occur, and T6 still holds

For $s_0\ge1$ the true model's prior mass is tiny when $p$ is huge: by Lemma 3(a),(b), $p(S_0)\le2w(s_0)\le2\,s_0!\,p^{-s_0}$ (each of the $s_0+1$ factors $2p-i$ is at least $p$). Combined with Lemma 9 applied to $S_0$ and with $p(\emptyset)\ge\frac12$, this gives the deterministic bound $\Pi(S_0\mid y)\le p(S_0)m(S_0)/(p(\emptyset)m(\emptyset))\le4\,s_0!\,p^{-s_0}(n+1)^{\nu}$, which tends to zero once $\log p\gg\frac{n}{2s_0}\log n$, whatever the design. Where the posterior mass goes instead depends on the design, and it need not go to large models: if, for instance, every noise column is the same vector, every nonempty noise model has the same column span (their ridge fits $Q_S$ and Occam factors still vary with the size), and a reviewer's calculation (round-2 report of the angle-C Astra reviewer) shows that the prior's geometric tail then makes small models win. The angle-C Astra reviewer gave an explicit construction in which large models win: $\sigma_\star^2=1$, $p=1+2\lceil e^{n^2}\rceil$, one true column $x_1=\sqrt n\,u$ with $\beta^\star_1=\sqrt M$, all other columns copies of $x_\pm=\sqrt{n-\tau/n^2}\,v\pm(\sqrt\tau/n)\,u$ for orthonormal $u,v$, with $\tau=10$ and $M=72\log2/(10-12\log2)$ (this value of $M$ is tuned to $\sigma_\star^2=1$). It satisfies every standing assumption except $p\le n^A$ (all columns have norm $\sqrt n$, $\Gamma_{S_0}=1$, $\|\mu\|^2/n=M$), and the reviewer's calculation (round-1 report, `review/astra_C/ASTRA_REVIEW_C.md`; not re-derived here) concludes that the posterior concentrates on models of size $\frac n2(1+o(1))$, none of which contains the true column. A numerical check on one draw of $y$ per $n$ (`review/check_counterexample_astraC.py`, seed 1, no cap, default $a_0=b_0=0.01$; all models with the same numbers $(k_+,k_-)$ of copies of $x_\pm$ share the same $m(S)$, so each size class is summed exactly; models containing $x_1$ are dropped, which is justified because, with no cap, $p(1\in S)=\mathbb E_{\mathrm{BB}}[K]/p=1/(p+1)$ by exchangeability and $\mathbb E_{\mathrm{BB}}[K]=p/(p+1)$, so Lemma 9 and $p(\emptyset)=\frac12$ give $\Pi(1\in S\mid y)\le2(n+1)^{\nu}/(p+1)$ for every $y$) gave posterior mass $0.60$, $0.73$ and $0.88$ on $\{|\,|S|/n-\tfrac12|\le0.1\}$ at $n=40,80,160$, with the posterior mode at $|S|/n=0.45,0.50,0.49$. Three single-draw values are consistent with the reviewer's conclusion; they do not prove it, and nothing in the proof of T6 or T9a(i) depends on it. (Two Opus reviewers reproduced these numbers independently in round 2. Between the proved range $\log p\le c'n$, $c'<\frac{\log2}{2s_0}$ (which is $c'<\frac{\log2}{2}$ for this construction's $s_0=1$; audit 2026-10-15), and the super-exponential construction, the proof claims nothing either way.)

This is consistent with T6 and with T9a(i): in that construction, with $\omega_n=\log\log n$, $m_n\sim n^2/\log2\gg n/2$, so T6 asserts nothing about sizes near $n/2$, and the statement with the operational cap $\lfloor n/2\rfloor$ is void. Two cautions on reading T6's cutoff. First, $m_n$ (which is $\asymp s_0\log_2 p$ in that construction, and more generally $\asymp(s_0+1)\ell_n$ for $\omega_n=O(\log n)$) is a sufficient cutoff, not a proved sharp posterior scale: for example, Lemma 9 and $p(\emptyset)\ge\frac12$ also give the deterministic, design-free and $p$-free bound $\Pi(|S|\ge m\mid y)\le p(|S|\ge m)\,(n+1)^{\nu}/p(\emptyset)\le2^{3-m}(n+1)^{\nu}$, i.e. a cutoff of order $\frac n2\log_2(n+1)$ for every $p$ whatever. Second, within the standing assumptions ($p\le n^A$) the cutoff is $O(\log n)$; if the reported construction is correct, no cutoff of order $\log n$ can hold uniformly over all $p$ and all designs when $s_0\ge1$, and nothing here locates a boundary between the polynomial and the super-exponential regimes.

*Conclusion on the note.* The prover note's two remarks need one qualification each. "The objection ignored the shrinkage floor": as far as the objection is described in the note, the floor is indeed what bounds the reward for interpolation by $(n+1)^{\nu}$, but the floor does not by itself dispose of the objection (6.2). "It is in any case dominated by this exact argument": true throughout the standing assumptions and, for $s_0\ge1$, for $\log p\le c'n$ with $c'<\frac{\log2}{2s_0}$ (for $s_0=0$, for every $p$) (6.3; constant made explicit, audit 2026-10-15), but not for every $p$ (6.4). For T6 only the second point is needed, and only in the form proved in Section 4.

---

## 7. Hypotheses added, hypotheses not used, and points to flag

**Hypotheses added.** None. Three conventions are made explicit: $n\ge2$ (used so that $\nu\ge1$ and Lemma 5 applies, and in Steps 4 and 5 of Proposition 7 for $\frac{s_0}{2n}\le\frac{s_0}{4}$ and $\frac{2a_0}{n}\le a_0$; the Chebyshev bound $\mathbb P_0(\mathcal E)\ge1-8/n$ is valid for all $n\ge2$ and informative for $n>8$); $p\ge1$; and $k_{\max}\ge s_0$, which is already among the standing assumptions and is needed for $p(S_0)>0$. Implicit in the draft's asymptotic convention and made explicit here: $\sigma_\star^2$, $a_0$, $b_0$, $M$ and $\varphi_0$ are fixed as $n\to\infty$ (so that $K_\star$ is a constant).

**Hypotheses of T6 not used, or used weakly.**
- $p\le n^A$: not used in the convergence statement; used only to make $m_n=O(\log n)$ in the "in particular" clause (Section 5, item 1).
- $s_0$ fixed: used to make $K_\star$ a constant, for $m_n=O(\log n)$, and for $\lfloor n/2\rfloor\ge s_0$ eventually; the bound itself is explicit in $s_0$ (Remark 4.1).
- The cap: used only through $k_{\max}\ge s_0$ (Section 5, item 2).
- $\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2$ and $\|\mu\|^2/n\le M$: used only to bound $\delta=(\|\mu\|^2+\|\beta^\star_{S_0}\|^2)/n$ (Lemma 4). The strongest form of the theorem replaces the pair by the single condition $\delta\le M'$. With no condition on $\delta$ at all, Theorem 8 still holds with $K$ containing $\delta_n$ linearly, so T6 holds (with $\omega_n\to\infty$ as before) if $m_n$ is computed with $\omega_n+(1+a_0)\delta_n/\sigma_\star^2$ in place of $\omega_n$. (Whether the linear dependence of the exponent on $\delta$ is sharp is not proved here; it is plausible, because $e^{-\delta/(2\sigma^2)}$ is the prior density at the truth up to normalisation.)

**Hypotheses of T6 that are genuinely used.** $\varepsilon\sim N_n(0,\sigma_\star^2I_n)$ with fixed design (for $f_0$, for $E$, and for Chebyshev); proper priors on $\beta_S$ and $\sigma^2$ (for Lemma 1, hence the identity); $\mathrm{BB}(1,p)$ (for the geometric tail of Lemma 3(c) and the mass of $S_0$ in Lemma 3(d)); $k_{\max}\ge s_0$; $\delta$ bounded; $\sigma_\star^2,a_0,b_0$ fixed.

**On the base of the logarithm.** Natural logarithms are used throughout. If the draft's $\log$ in $m_n$ were read in another base $b>1$, the terms $s_0\log(2p)+\frac{s_0+1}2\log n$ and the denominator $\log2$ rescale together, while the additive $\omega_n$ does not; the cutoff in base $b$ equals the natural-log cutoff with $\omega_n$ replaced by $\omega_n\ln b$. Since $\omega_n$ is an arbitrary sequence tending to infinity, the theorem is the same statement in every base, although the integer $m_n$ for a given $\omega_n$ is not.

**Points I am not fully sure of.**
1. The objection in Section 6.1 is reconstructed from one line of the prover note; its exact original form (and the origin of the threshold $n^{3/2}$) is unknown to me. The resolution in 6.3 does not depend on the form of the objection: it applies to any argument that bounds a class by its cardinality times a best fit.
2. Section 6.4 reports a reviewer's construction, consistent with single-draw numerics but not re-derived analytically here; it is a remark, and nothing in the proof of T6 or T9a(i) depends on it.
3. The constant $K$ in (3.3) was derived with generous rounding (e.g. $\log s_0!$ discarded, $\frac{s_0}{2n}\le\frac{s_0}{4}$, $\nu\le n(1+a_0)$); it is correct as a bound but not tight. Nothing downstream depends on its value.
4. Lemma 5 is proved from scratch rather than cited; if a reviewer prefers the classical Stirling bound, the constant $-\frac32$ improves to $+\frac12\log(2\pi)$ and nothing else changes.

**Explicit dependence of the final bound.** With no cap, (4.1) holds with $2t$ replaced by $t$. Under the standing assumptions, (4.3) reads: for all $t>0$ and $n\ge2$, $\mathbb P_0\big(\Pi(|S|>m_n\mid y)>2te^{K_\star-\omega_n}\big)\le1/t+8/n$, with
$$
K_\star=\log2+\tfrac32+a_0\log\tfrac{\sigma_\star^2}{b_0}+\log\Gamma(a_0)+\tfrac12\log(1+a_0)+\tfrac{s_0}{4}+\tfrac{(1+a_0)\big(2b_0+M(1+\varphi_0^{-2})\big)}{\sigma_\star^2}.
$$

---

## Audit revisions (2026-10-15)

Sol audit `proofs/_audit/T6/SOL_AUDIT.md` (verdict VERIFIED); rulings in `proofs/_audit/group_C/RULINGS.md`. No step of the proof of T6 (Sections 1 to 4) or of T9a(i) (Section 5) was changed.

1. **§6.2, "What the floor does"** (Sol finding 2, accepted). The claim that the unshrunk ceiling exceeds $(n+1)^\nu$ by a factor "enormous when $y^\top y\asymp n$" was wrong in general (the ratio is $((2b_0+T)/(2b_0(n+1)))^\nu$, which tends to zero when $\mu=0$, $\sigma_\star^2=b_0$). Replaced by the sharper floor ceiling $\mathrm{BF}(S)\le((2b_0+T)/(2b_0+T/(n+1)))^\nu$ and the correct comparison factor $(1+T/(2b_0(n+1)))^\nu$. Checked numerically in `proofs/_audit/group_C/check_audit_C.py` (block T6 #2).
2. **§6.4, closing parenthesis, and §6.4 "Conclusion on the note"** (Sol finding 1, accepted for the draft; clarity edit here). The proved exponential range is $c'<\log2/(2s_0)$ for $s_0\ge1$ (as §6.3 already stated); the §6.4 parenthesis now shows the $s_0$ and notes that it equals $\log2/2$ for the $s_0=1$ construction, and the conclusion paragraph states the constant.
3. Sol finding 3 (the §6.4 construction and numerics are reported, not proved): no change; the existing qualification is retained.
