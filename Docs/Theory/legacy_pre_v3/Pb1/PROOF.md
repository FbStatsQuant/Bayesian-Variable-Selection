# Pb1 — Exact selection error of the HPM under orthogonality

Supplement material for *Split-and-merge with an exact merge: composite-start sequential Monte Carlo for Bayesian variable selection* (draft of 15 October 2026). Notation follows Section 2 of the draft; the statements of P3, P4, Pb1 and T8 are frozen verbatim in Section 0. Thread Pb1, lead Fable 5.1 (high). **Version 4 (2026-10-15, after three review rounds; wording changes only relative to the reviewed v3); not adopted.**

**Summary of the outcome.** (Informal; the precise statements, with all hypotheses, are the numbered results.)

Pb1 is a problem, not a theorem. The strongest theorem proved here, in the setting of P4 ($X^\top X=nI_p$, $p\le n$, $\BB(1,p)$ prior with any cap $k_{\max}\ge s_0$, $s_0\ge1$ fixed, $s_0<p$, $|\beta^\star_j|=\beta_n$ on $S_0$, $\lambda_n=n\beta_n^2/\sigma_\star^2$, with $\sigma_\star^2,a_0,b_0$ fixed), is a **sharp threshold with its exact window**. Put
$$\tau_n:=\log D+2\log\frac{2p_n-s_0}{s_0}\qquad\Big(=\log n+2\log\frac{2p_n}{s_0}+o(1)\ \text{when }p_n\to\infty\Big),\qquad c_n:=\sqrt{\lambda_n}-\sqrt{\tau_n}.$$

- **Known variance** ($\sigma^2=\sigma_\star^2$; Theorem 2.5, Corollary 2.6). For all $n,p,s_0$, $\Prob_0(\HPM=S_0)$ is sandwiched between $\psi(\lambda,\tau_1/h)^{s_0}(1-E_n)$ and $\psi(\lambda,\tau_{s_0}/h)^{s_0}\times(\text{a superset factor})$, where $\psi(\lambda,t)=\Prob((\sqrt\lambda+\zeta)^2>t)$, $\tau_k=\log D+2\log\frac{2p-k}{k}$ is the exact penalty of the $k$-th inclusion, and $E_n\le(1-r_n)^{-(s_0+1)}-1$ with $r_n=\sqrt{e\tau_{s_0+1}/(hD)}=O(\sqrt{\log n/n})$ whenever $r_n<1$. Hence $\Prob_0(\HPM=S_0)\to1$ iff $c_n\to+\infty$, $\to0$ iff $c_n\to-\infty$, and $\to\Phi(c)^{s_0}$ if $c_n\to c$. At the scale of the transition, the randomness of $\hat k$ and the noise order statistics reduce to a single comparison, that of the smallest signal score with its inclusion penalty (Proposition 2.1 gives the exact event). When supersets are admissible ($s_0<k_{\max}$) they cost a $\lambda$-free floor $\Prob_0(\HPM\ne S_0)\ge1-(1-q_n)^{p-s_0}\asymp n^{-1/2}(\log n)^{-1/2}$ (Proposition 2.4, Remark 2.7: the probability that a single noise variable clears the first noise penalty).
- **Minimax comparison** (Theorem 3.1, Corollary 3.2; $p_n-s_0\to\infty$). A Bayes argument shows that no selector, even one knowing $s_0$, $\beta_n$, $\sigma_\star$ and the signs, has smaller maximal error over the positive-sign class than the signed top-$s_0$ rule, whose error $\rho_n(\lambda)$, like that of the sign-free top-$s_0$-by-$|z_j|$ rule, tends to $1-\Phi(c)^{s_0}$ when $\sqrt{\lambda_n}-\sqrt{2\log(p_n-s_0)}\to c$ (the two rules differ at finite $n$). The minimax threshold therefore has centre $2\log(p_n-s_0)$ and the same window shape as the HPM's. The literature (Butucea, Ndaoud, Stepanova, Tsybakov 2018; CITED_RESULTS.md) gives the sufficiency side and separable-selector lower bounds, but no all-selector lower bound on the probability of wrong recovery for fixed $s_0$; Theorem 3.1 fills that for the class of Pb1.
- **The heuristic** (Theorem 3.3, Section 3.3). The HPM's threshold exceeds the minimax one by $\log n+O(1)$ on the $\lambda$-scale: the $\log n$ is confirmed and sharp (the gap is $\asymp\sqrt{\log n}$ on the $\sqrt\lambda$-scale, where the windows are $O(1)$). At the level of the leading-order centres the constant is $2\log2-2\log s_0$ for the penalty $\tau_{s_0}$ of the necessary condition and $2\log2$ for the penalty $\tau_1$ of the sufficient condition, so it is $2\log2$ for $s_0=1$; the finite-$n$ constant is not determined by the limit theorems (Section 3.3). The HPM is strictly suboptimal: for $p_n=n^{\vartheta}$ it is consistent when $\lambda_n\ge(1+\epsilon)(1+2\vartheta)\log n$ and inconsistent when $\lambda_n\le(1-\epsilon)(1+2\vartheta)\log n$, whereas $(1+\epsilon)2\vartheta\log n$ suffices for the oracles and $(1-\epsilon)2\vartheta\log n$ defeats every selector (fixed $\epsilon>0$; the sharp conditions are the ones on $c_n$ and $d_n$).
- **Integrated variance** (the paper's prior; Theorems 5.2, 5.5, Corollary 5.6). Under the extra bounded-signal condition $\beta_n^2\le B\sigma_\star^2$, the same trichotomy holds with the same $\tau_n$ and limit $\Phi(c)^{s_0}$. What changes: the thresholds pick up a factor $\gamma_n^\pm=1+O(\sqrt{\log n/n})$ (the residual-variance estimate replacing $\sigma_\star^2$), the coordinates are coupled so the product form and the explicit superset bound are lost, and the superset part is controlled only in probability through Proposition 4.2 and Lemma 3.1 of proofs/T7_T8/PROOF.md (the only external dependence; provisional; quoted in CITED_RESULTS.md). As a by-product, for the HPM-consistency conclusion of T8(ii), T8's beta-min scale $\log n$ is sharp in the orthogonal model with equal signal magnitudes, with constant $1+2\vartheta$ for $p_n=n^{\vartheta}$ (Section 5.5; nothing is claimed about T8(i) or T8(iii)).

Readings adopted are flagged in Section 0.5; flags for the draft are in Section 6. Numerical checks: `check_Pb1.py` → `check_Pb1.out` (operator, single seed, local; included in the review packet).

---

## 0. Statements from the draft, frozen verbatim

### 0.1 Pb1 (the problem)

> \begin{problem}[\textbf{Pb1} $\cdot$ Exact selection error under orthogonality]\label{Pb1}
> \status{Open}
> Under the setting of P4, with $s_0$ fixed, $p=p_n\le n$, known or integrated variance (state which), and signals $|\beta^\star_j|=\beta_n$ for $j\in S_0$:
> \begin{itemize}
> \item Characterise $\Prob_0(\HPM\ne S_0)$, accounting for the random $\hat k$ and the order statistics of $(u_j)$.
> \item Compare the resulting threshold for the signal-to-noise $n\beta_n^2/\sigma_\star^2$ with the minimax threshold for exact support recovery.
> \end{itemize}
> A heuristic claims that the threshold for $n\beta_n^2/\sigma_\star^2$ exceeds the minimax one by about $\log n+2\log2$; this is unverified. \emph{(Supplementary.)}
> \end{problem}

### 0.2 P4 (the setting; used as stated, re-derived in Section 1 for the known-variance case)

> \begin{proposition}[\textbf{P4} $\cdot$ Orthogonal designs: exact odds and the top-$k$ structure]\label{P4}
> \status{Elementary}
> Let $X^\top X=nI_p$, which requires $p\le n$. Put:
> \begin{itemize}
> \item $u_j=z_j^2/n$, $h=n^2/(n^2+n+1)$ and $D=(n^2+n+1)/(n+1)$;
> \item $U_{(k)}$, the sum of the $k$ largest $u_j$.
> \end{itemize}
> \begin{enumerate}
> \item[(i)] $Q_S=y^\top y-h\sum_{j\in S}u_j$ and $D_S=D^{|S|}$. For $j\notin S$ with $|S|=k<k_{\max}$, the \emph{exact} neighbour log-odds are
> \[
> \log\frac{\pi(S\cup\{j\})}{\pi(S)}=\log\frac{w(k+1)}{w(k)}-\tfrac12\log D+\nu\log\frac{2b_0+Q_S}{2b_0+Q_S-hu_j}.
> \]
> \item[(ii)] For each $k$, the best model of size $k$ consists of the $k$ largest $u_j$. Hence $\HPM$ is the top-$\hat k$ set, with
> \[
> \hat k=\operatorname*{arg\,max}_{k\le k_{\max}}\Big\{\log w(k)-\tfrac k2\log D-\nu\log\big(2b_0+y^\top y-hU_{(k)}\big)\Big\}.
> \]
> \item[(iii)] \emph{(Known variance, for intuition.)} If $\sigma^2$ is known, adding $j$ to a size-$k$ model increases the posterior if and only if
> \[
> \frac{hu_j}{\sigma^2}>\log D+2\log\frac{w(k)}{w(k+1)}.
> \]
> For $\BB(1,p)$ the right-hand side is $\approx\log n+2\log\frac{2p-k-1}{k+1}$.
> \end{enumerate}
> \end{proposition}

### 0.3 P3 (the size-only ceiling; context only)

> \begin{proposition}[\textbf{P3} $\cdot$ The size-only ceiling]\label{P3}
> \status{Elementary}
> Let $p(S)\propto w(|S|)$ with $w>0$ on $\{0,\dots,k_{\max}\}$, assume $s_0\le k_{\max}$, and use the fixed tie order of Section~\ref{sec:setup}. For each $k$, let $\hat S_k$ be the order-first maximiser of $m$ over $\{|S|=k\}$. Then
> \[
> \HPM=\hat S_{\hat k},\qquad \hat k=\operatorname*{arg\,max}_{k\le k_{\max}}\ w(k)\,m(\hat S_k).
> \]
> Hence
> \[
> \{\HPM=S_0\}\subseteq\mathcal W:=\{\hat S_{s_0}=S_0\},
> \]
> and $\Prob_0(\HPM=S_0)\le\Prob_0(\mathcal W)$ for every size-only prior. The supremum over strictly positive $w$ equals $\Prob_0(\mathcal W)$, approached by $w$ concentrating on $s_0$, and attained if $w=0$ off $s_0$ is allowed. Such a $w$ depends on the true size, so it is not implementable.
> \end{proposition}

### 0.4 T8 (the general consistency result; its hypotheses are compared with ours in Section 5)

> \begin{theorem}[\textbf{T8} $\cdot$ Selection consistency and the HPM]\label{T8}
> \status{Proved; one blind review round; Sol-audited}
> Assume T7's conditions and the beta-min condition
> \[
> \min_{j\in S_0}(\beta_j^\star)^2\ge M_n^{\beta}\,\frac{\sigma_\star^2\log n}{n\varphi_0^2},\qquad M_n^{\beta}\to\infty .
> \]
> Then:
> \begin{enumerate}
> \item[(i)] $\Pi(S_0\mid y)\to1$ in $\Prob_0$-probability, hence also in $L^1(\Prob_0)$;
> \item[(ii)] $\Prob_0(\HPM\ne S_0)\le2\,\E_0[1-\Pi(S_0\mid y)]\to0$;
> \item[(iii)] $1-\Pi(S_0\mid y)=O_{\Prob}(\sqrt{\log n/n}+e^{-\omega_n})$, hence $O_{\Prob}(\sqrt{\log n/n})$ when $\omega_n\ge\tfrac12\log n$.
> \end{enumerate}
> \end{theorem}

### 0.5 Readings adopted (flagged)

- (R1) Pb1 is a problem, not a theorem; "the strongest theorem we can prove" is delivered. The known-variance case is treated first (Sections 2–4), then the integrated-variance case (Section 5), as the brief asks.
- (R2) "Known variance" means that the known value is the true one, $\sigma^2=\sigma_\star^2$, and that the marginal likelihood is the one of the draft's model with $\sigma^2$ fixed at that value (the normal slab $\beta_S\mid S\sim N(0,\sigma^2\Lambda_S^{-1})$ kept, the inverse-gamma layer removed). Section 1.3 derives it. A misspecified known value is covered by Remark 2.8.
- (R3) The prior is $\BB(1,p)$ with a cap $k_{\max}$ satisfying $s_0\le k_{\max}\le p$ (a cap above $p$ is read as $p$, as the draft says). The results are stated with the cap kept; where the cap matters it is said.
- (R4) $s_0\ge1$ is assumed (for $s_0=0$ the only question is whether a superset beats $\emptyset$, which Proposition 2.4(a),(b) cover with $s_0=0$; part (c) uses $s_0\ge1$), and $p\ge s_0+1$ wherever a noise coordinate is mentioned.
- (R5) The "threshold" is defined through the sharp trichotomy of Corollary 2.6: the centre $\tau_n$ of the transition window on the scale of $\lambda_n=n\beta_n^2/\sigma_\star^2$, the window having width of order $\sqrt{\tau_n}$. A centre is determined by the trichotomy only up to $o(\sqrt{\tau_n})$; the finite-$n$ bounds of Theorem 2.5 involve the two penalties $\tau_{s_0}$ (necessary side) and $\tau_1$ (sufficient side), which differ by at most $2\log(2s_0)$, and no finite-$n$ centre is defined. The comparison with the minimax threshold (Section 3) is made at the level of these centres and of the window shape.
- (R6) Ties among scores have probability zero (all the laws involved are absolutely continuous), so the tie order of the draft plays no role; see Lemma 1.2(e).

---

## 1. Setting and reduction to the Gaussian sequence model

### 1.1 Objects

Throughout, $X\in\R^{n\times p}$ is fixed with $X^\top X=nI_p$ (hence $p\le n$), $y=\mu+\varepsilon$ with $\mu=X\beta^\star$, $\varepsilon\sim N_n(0,\sigma_\star^2I_n)$, $S_0=\operatorname{supp}\beta^\star$, $s_0=|S_0|\ge1$, and $|\beta^\star_j|=\beta_n$ for $j\in S_0$. Put
$$\lambda=\lambda_n:=\frac{n\beta_n^2}{\sigma_\star^2},\qquad h=\frac{n^2}{n^2+n+1},\qquad D=\frac{n^2+n+1}{n+1}=n+\frac1{n+1},\qquad u_j=\frac{z_j^2}{n},\ z_j=x_j^\top y .$$
Note $1-h=\frac{n+1}{n^2+n+1}\le\frac1n$ and $n<D\le n+1$, so $\log D=\log n+\log(1+\frac1{n(n+1)})\in[\log n,\log n+n^{-2}]$.

The prior weights are $w(k)=B(1+k,2p-k)/B(1,p)$, $0\le k\le p$, and (beta-function algebra, as in L6(i) of the draft: $\frac{B(k+2,2p-k-1)}{B(k+1,2p-k)}=\frac{\Gamma(k+2)\Gamma(2p-k-1)}{\Gamma(k+1)\Gamma(2p-k)}=\frac{k+1}{2p-k-1}$)
$$\frac{w(k+1)}{w(k)}=\frac{k+1}{2p-k-1}\quad(0\le k\le p-1),\qquad\text{so}\qquad \frac{w(k)}{w(k-1)}=\frac{k}{2p-k}\quad(1\le k\le p). \tag{1.1}$$
The **inclusion penalties** are
$$\tau_k:=\log D+2\log\frac{2p-k}{k}=\log D+2\log\frac{w(k-1)}{w(k)},\qquad 1\le k\le p . \tag{1.2}$$
They are strictly decreasing in $k$: $\tau_1=\log D+2\log(2p-1)>\tau_2>\dots>\tau_p=\log D$. In particular, for $1\le k\le s_0$,
$$\tau_{s_0}\le\tau_k\le\tau_1,\qquad 2\log s_0\le\tau_1-\tau_{s_0}=2\log\frac{(2p-1)s_0}{2p-s_0}\le2\log(2s_0) , \tag{1.3}$$
the last step because $1\le\frac{2p-1}{2p-s_0}<2$ for $p\ge s_0$. Throughout, $\sigma_\star^2$, $a_0$, $b_0$ and $s_0$ are fixed as $n\to\infty$; every unquantified constant may depend on them.

### 1.2 The sequence-model representation

**Lemma 1.1 (reduction).** Let $\zeta_j:=x_j^\top\varepsilon/(\sqrt n\,\sigma_\star)$ for $j\in[p]$ and $R:=\|(I-P_{[p]})\varepsilon\|^2/\sigma_\star^2$, where $P_{[p]}=\frac1nXX^\top$ is the projection onto the column span of $X$ ($R=0$ if $p=n$). Then:

(a) $\zeta_1,\dots,\zeta_p$ are i.i.d. $N(0,1)$, $R\sim\chi^2_{n-p}$, and $R$ is independent of $(\zeta_j)_{j\le p}$;

(b) $z_j=n\beta^\star_j+\sqrt n\,\sigma_\star\zeta_j$, hence
$$\frac{u_j}{\sigma_\star^2}=\big(\epsilon_j\sqrt\lambda+\zeta_j\big)^2\ \ (j\in S_0),\qquad \frac{u_j}{\sigma_\star^2}=\zeta_j^2\ \ (j\notin S_0),$$
with $\epsilon_j=\operatorname{sign}\beta^\star_j\in\{\pm1\}$;

(c) $\|y\|^2=\sum_{j\le p}u_j+\sigma_\star^2R$, and for every $S\subseteq[p]$, $Q_S=\|y\|^2-h\sum_{j\in S}u_j=\sigma_\star^2R+\sum_{j\notin S}u_j+(1-h)\sum_{j\in S}u_j$;

(d) $\|(I-P_{S_0})\varepsilon\|^2/\sigma_\star^2=R+\sum_{j\notin S_0}\zeta_j^2\sim\chi^2_{n-s_0}$ and is independent of $(\zeta_j)_{j\in S_0}$.

*Proof.* (a) The vector $(x_j^\top\varepsilon/\sqrt n)_{j\le p}=\frac1{\sqrt n}X^\top\varepsilon$ is $N_p(0,\sigma_\star^2\frac1nX^\top X)=N_p(0,\sigma_\star^2I_p)$. The pair $(X^\top\varepsilon,(I-P_{[p]})\varepsilon)$ is jointly Gaussian with cross-covariance $\sigma_\star^2X^\top(I-P_{[p]})=0$ since $P_{[p]}X=X$; so the two blocks are independent, and $\|(I-P_{[p]})\varepsilon\|^2/\sigma_\star^2\sim\chi^2_{n-p}$ because $I-P_{[p]}$ is a projection of rank $n-p$.

(b) $z_j=x_j^\top X\beta^\star+x_j^\top\varepsilon=n\beta^\star_j+\sqrt n\sigma_\star\zeta_j$ by orthogonality, and $u_j=z_j^2/n=(\sqrt n\beta^\star_j+\sigma_\star\zeta_j)^2$; divide by $\sigma_\star^2$ and use $\sqrt n|\beta^\star_j|/\sigma_\star=\sqrt\lambda$ on $S_0$ and $\beta^\star_j=0$ off $S_0$.

(c) $\|y\|^2=\|P_{[p]}y\|^2+\|(I-P_{[p]})y\|^2$; $\|P_{[p]}y\|^2=y^\top P_{[p]}y=\frac1n\|X^\top y\|^2=\sum_ju_j$; and $(I-P_{[p]})y=(I-P_{[p]})\varepsilon$ since $\mu=X\beta^\star$ lies in the column span. The formula for $Q_S$ is P4(i), re-derived: with $G_S=nI$, $H_S=(n(n+1)+1)I$, $t_S=n\,z_S^\top H_S^{-1}z_S=\frac{n}{n^2+n+1}\sum_{j\in S}z_j^2=h\sum_{j\in S}u_j$, and $Q_S=\|y\|^2-t_S$. Substituting $\|y\|^2$ gives the last form.

(d) $P_{S_0}=\frac1nX_{S_0}X_{S_0}^\top$, so $\|P_{S_0}\varepsilon\|^2/\sigma_\star^2=\sum_{j\in S_0}\zeta_j^2$, and $\|(I-P_{S_0})\varepsilon\|^2=\|\varepsilon\|^2-\|P_{S_0}\varepsilon\|^2=\sigma_\star^2(R+\sum_{j\le p}\zeta_j^2)-\sigma_\star^2\sum_{j\in S_0}\zeta_j^2$ (part (c) applied to $\varepsilon$ in place of $y$). Independence and the $\chi^2_{n-s_0}$ law follow from (a). $\square$

**Lemma 1.2 (the one-coordinate law).** Let $\zeta\sim N(0,1)$, $\lambda\ge0$, and define, for $t\in\R$,
$$\psi(\lambda,t):=\Prob\big((\sqrt\lambda+\zeta)^2>t\big)=\begin{cases}\Phi(\sqrt\lambda-\sqrt t)+\Phi(-\sqrt\lambda-\sqrt t),&t\ge0,\\ 1,&t<0.\end{cases}$$
Then: (a) $(\sqrt\lambda+\zeta)^2$ and $(-\sqrt\lambda+\zeta)^2$ have the same law, so the signs $\epsilon_j$ in Lemma 1.1(b) are irrelevant; (b) $\psi$ is nondecreasing in $\lambda$ and nonincreasing in $t$; (c) $\Phi(\sqrt\lambda-\sqrt t)\le\psi(\lambda,t)\le\Phi(\sqrt\lambda-\sqrt t)+\Phi(-\sqrt t)$ for $t\ge0$; (d) $1-\psi(\lambda,t)=\Phi(\sqrt t-\sqrt\lambda)-\Phi(-\sqrt t-\sqrt\lambda)\le\Phi(\sqrt t-\sqrt\lambda)$ for $t\ge0$; (e) for every $\lambda\ge0$ the law of $(\sqrt\lambda+\zeta)^2$ is absolutely continuous.

*Proof.* (a) $\zeta\overset d=-\zeta$. (b) For $t>0$, $\partial_\lambda\psi=\frac1{2\sqrt\lambda}[\phi(\sqrt\lambda-\sqrt t)-\phi(\sqrt\lambda+\sqrt t)]\ge0$ because $|\sqrt\lambda-\sqrt t|\le\sqrt\lambda+\sqrt t$; monotonicity in $t$ is immediate from the definition as a tail probability. (c), (d): $\Phi(-\sqrt\lambda-\sqrt t)\le\Phi(-\sqrt t)$, and $1-\psi=\Prob(-\sqrt t<\sqrt\lambda+\zeta<\sqrt t)$. (e) The map $x\mapsto(\sqrt\lambda+x)^2$ is smooth with a single critical point, and the image of an absolutely continuous law under such a map is absolutely continuous. $\square$

*On ties (reading R6).* All scores below are continuous functions of the vector $(u_j)_{j\le p}$ and of $R$. By Lemma 1.1(a) and Lemma 1.2(e) the vector $(u_j)_{j\le p}$ has an absolutely continuous law, and $R$ is independent of it ($R=0$ when $p=n$). For $S\ne S'$ pick $j\in S\setminus S'$ (or $j\in S'\setminus S$, exchanging the roles); conditionally on $R$ and on $(u_i)_{i\ne j}$, the difference $\mathrm{sc}(S)-\mathrm{sc}(S')$ is strictly increasing in $u_j$: for the known-variance score by (1.5), and for the integrated score because, by Lemma 1.1(c), $\partial A_S/\partial u_j=1-h$ and $\partial A_{S'}/\partial u_j=1$, so
$$\frac{\partial}{\partial u_j}\big[\mathrm{sc}(S)-\mathrm{sc}(S')\big]=\nu\Big(\frac{1}{A_{S'}}-\frac{1-h}{A_S}\Big)=\nu\,\frac{A_S-(1-h)A_{S'}}{A_SA_{S'}}\ \ge\ \nu\,\frac{2b_0h}{A_SA_{S'}}>0,$$
using $Q_S\ge(1-h)(\sigma_\star^2R+\sum_{i\le p}u_i)\ge(1-h)Q_{S'}$ (Lemma 1.1(c)) and $b_0>0$. Hence the tie event $\{\mathrm{sc}(S)=\mathrm{sc}(S')\}$ has conditional probability $0$, hence probability $0$. We ignore ties from now on.

**Lemma 1.3 (chi-square and Gaussian tails; self-contained).** Let $V\sim\chi^2_m$, $m\ge1$.
(a) For $\delta\in(0,1]$ and $t\ge0$: $\Prob(V\ge t)\le\delta^{-m/2}e^{-(1-\delta)t/2}$.
(b) For $\delta\in(0,1)$: $\Prob(V\le m(1-\delta))\le e^{-m\delta^2/4}$.
(c) For $\delta>0$: $\Prob(V\ge m(1+\delta))\le e^{-m\delta^2/(4(1+\delta))}$.
(d) For $x\ge0$: $\bar\Phi(x):=1-\Phi(x)\le\frac12e^{-x^2/2}$; for $x>0$: $\phi(x)(x^{-1}-x^{-3})\le\bar\Phi(x)\le\phi(x)/x$. Hence $\Prob(\chi^2_1\ge t)=2\bar\Phi(\sqrt t)\le e^{-t/2}$ for $t\ge0$.

*Proof.* $\E e^{\theta V}=(1-2\theta)^{-m/2}$ for $\theta<\frac12$. (a) Markov's inequality with $\theta=(1-\delta)/2$: $\Prob(V\ge t)\le(1-2\theta)^{-m/2}e^{-\theta t}=\delta^{-m/2}e^{-(1-\delta)t/2}$. (b) Markov on $e^{-\theta V}$ with $\theta=\delta/(2(1-\delta))>0$: $\Prob(V\le a)\le e^{\theta a}\E e^{-\theta V}=e^{\theta a}(1+2\theta)^{-m/2}$; with $a=m(1-\delta)$ and $1+2\theta=1/(1-\delta)$ this is $\exp\{\frac{m\delta}2+\frac m2\log(1-\delta)\}\le e^{-m\delta^2/4}$ since $\log(1-\delta)\le-\delta-\delta^2/2$ on $(0,1)$. (c) $\theta=\delta/(2(1+\delta))$, $1-2\theta=1/(1+\delta)$: $\Prob(V\ge m(1+\delta))\le\exp\{-\frac m2(\delta-\log(1+\delta))\}\le e^{-m\delta^2/(4(1+\delta))}$, since $g(\delta)=\delta-\log(1+\delta)-\frac{\delta^2}{2(1+\delta)}$ has $g(0)=0$ and $g'(\delta)=\frac{\delta}{1+\delta}-\frac{\delta(2+\delta)}{2(1+\delta)^2}=\frac{\delta^2}{2(1+\delta)^2}\ge0$. (d) First bound: for $x\ge0$, $\bar\Phi(x)=\int_0^\infty\phi(x+v)\,dv=e^{-x^2/2}\int_0^\infty e^{-xv}\phi(v)\,dv\le e^{-x^2/2}\int_0^\infty\phi(v)\,dv=\frac12e^{-x^2/2}$. Mills' upper bound: for $x>0$, $\bar\Phi(x)=\int_x^\infty\phi(u)\,du\le\int_x^\infty\frac ux\phi(u)\,du=\frac{\phi(x)}x$. Lower bound: with $f(x)=\phi(x)(x^{-1}-x^{-3})$, $-f'(x)=\phi(x)(1-3x^{-4})\le\phi(x)$, so $\bar\Phi(x)=\int_x^\infty\phi\ge\int_x^\infty(-f')=f(x)$. The $\chi^2_1$ statement is the first bound with $x=\sqrt t$ and symmetry. $\square$

### 1.3 The scores

**Integrated variance (the draft's model).** By (2.1) of the draft and P4(i), with $A_S:=2b_0+Q_S$,
$$\log\{p(S)m(S)\}=\log w(|S|)-\frac{|S|}2\log D-\nu\log A_S+\text{const},\qquad |S|\le k_{\max},$$
where "const" does not depend on $S$. Write $\mathrm{sc}(S):=\log w(|S|)-\frac{|S|}2\log D-\nu\log A_S$ and call it the **score**. The HPM is the maximiser of $\mathrm{sc}$ over $\{|S|\le k_{\max}\}$ (ties: probability zero).

**Known variance $\sigma^2=\sigma_\star^2$ (reading R2).** Integrating $\beta_S\sim N(0,\sigma^2\Lambda_S^{-1})$ out of $y\mid\beta_S,S\sim N(X_S\beta_S,\sigma^2I)$ gives $y\mid S\sim N_n(0,\sigma^2(I+X_S\Lambda_S^{-1}X_S^\top))$. Under orthogonality $\Lambda_S=\frac{n+1}nI$, so $X_S\Lambda_S^{-1}X_S^\top=\frac n{n+1}X_SX_S^\top$, whose nonzero eigenvalues are $\frac{n^2}{n+1}$ ($|S|$ of them); hence $\det(I+X_S\Lambda_S^{-1}X_S^\top)=(1+\frac{n^2}{n+1})^{|S|}=D^{|S|}$, and by Woodbury $(I+\frac n{n+1}X_SX_S^\top)^{-1}=I-X_S(\frac{n+1}nI+nI)^{-1}X_S^\top=I-\frac{n}{n^2+n+1}X_SX_S^\top$, so $y^\top(I+X_S\Lambda_S^{-1}X_S^\top)^{-1}y=\|y\|^2-h\sum_{j\in S}u_j=Q_S$. Therefore
$$\log m_{\mathrm{kv}}(S)=-\frac n2\log(2\pi\sigma^2)-\frac{|S|}2\log D-\frac{Q_S}{2\sigma^2},$$
and, dropping the terms that do not depend on $S$, the known-variance score is
$$\mathrm{sc}_{\mathrm{kv}}(S):=\log w(|S|)-\frac{|S|}2\log D+\frac{h}{2\sigma^2}\sum_{j\in S}u_j . \tag{1.4}$$
It is **additive over coordinates**: writing $v_j:=hu_j/\sigma^2$,
$$2\,\mathrm{sc}_{\mathrm{kv}}(S)=2\log w(|S|)-|S|\log D+\sum_{j\in S}v_j . \tag{1.5}$$
P4(iii) is the statement $2[\mathrm{sc}_{\mathrm{kv}}(S\cup\{j\})-\mathrm{sc}_{\mathrm{kv}}(S)]=v_j-\tau_{|S|+1}$, which is (1.5) with (1.1)–(1.2).

**Order-statistic form.** Let $u_{(1)}\ge u_{(2)}\ge\dots\ge u_{(p)}$ be the ordered $u_j$ and $v_{(i)}=hu_{(i)}/\sigma^2$. By (1.5), for fixed $k$ the score is maximised by the top-$k$ set (P4(ii)), and
$$f(k):=\max_{|S|=k}2\,\mathrm{sc}_{\mathrm{kv}}(S)=2\log w(0)+\sum_{i=1}^k\big(v_{(i)}-\tau_i\big),\qquad 0\le k\le k_{\max}. \tag{1.6}$$
Thus $\hat k=\arg\max_{k\le k_{\max}}f(k)$ and $\HPM$ is the top-$\hat k$ set. The increments $v_{(i)}-\tau_i$ are *not* monotone in $i$ (both $v_{(i)}$ and $\tau_i$ decrease), which is why $f$ need not be unimodal (Pb2 of the draft) and why the random $\hat k$ has to be handled through the whole profile $f$, not through a stopping rule.

---
## 2. Known variance: the exact event, the sandwich, and the sharp threshold

Throughout this section $\sigma^2=\sigma_\star^2$ is known (reading R2), so $v_j=hu_j/\sigma_\star^2=h(\sqrt\lambda+\zeta_j)^2$ for $j\in S_0$ (Lemma 1.2(a) removes the sign) and $v_j=h\zeta_j^2$ for $j\notin S_0$. The prior is $\BB(1,p)$ with cap $k_{\max}$, $1\le s_0\le k_{\max}\le p$, and $p>s_0$ (reading R4). Scores are $\mathrm{sc}=\mathrm{sc}_{\mathrm{kv}}$ of (1.4)–(1.5). Ties are ignored (probability zero).

### 2.1 The exact event

**Proposition 2.1 (exact characterisation).** With $f$ as in (1.6), $\{\HPM=S_0\}$ is (up to a null set) the intersection of

(a) $\min_{j\in S_0}u_j>\max_{j\notin S_0}u_j$ (the top-$s_0$ set is $S_0$);

(b) $\sum_{i=k+1}^{s_0}\big(v_{(i)}-\tau_i\big)>0$ for every $0\le k<s_0$ (every suffix of the signal increments is positive, so $f(s_0)>f(k)$ for $k<s_0$);

(c) $\sum_{i=s_0+1}^{k}\big(v_{(i)}-\tau_i\big)<0$ for every $s_0<k\le k_{\max}$ (every prefix of the increments beyond $s_0$ is negative, so $f(s_0)>f(k)$ for $k>s_0$).

*Proof.* By (1.6), $\HPM$ is the top-$\hat k$ set with $\hat k=\arg\max_{k\le k_{\max}}f(k)$. Hence $\HPM=S_0$ iff $\hat k=s_0$ and the top-$s_0$ set is $S_0$. The second condition is (a). Given (a), $\hat k=s_0$ iff $f(s_0)>f(k)$ for all $k\ne s_0$ in $[0,k_{\max}]$, and $f(s_0)-f(k)=\sum_{i=k+1}^{s_0}(v_{(i)}-\tau_i)$ for $k<s_0$, $f(s_0)-f(k)=-\sum_{i=s_0+1}^k(v_{(i)}-\tau_i)$ for $k>s_0$. $\square$

This is the characterisation Pb1 asks for, in terms of the order statistics $u_{(i)}$ and the random $\hat k$. It is exact but not directly computable, because the order statistics mix signal and noise coordinates. The rest of the section shows that, near the threshold, (a) and (c) hold with probability tending to one, and (b) reduces to its last term, the comparison of the *smallest signal* $\min_{j\in S_0}v_j$ with the *last signal penalty* $\tau_{s_0}$.

### 2.2 Necessary conditions

**Proposition 2.2 (two one-move comparisons).** If $\HPM=S_0$ then
$$v_j>\tau_{s_0}\quad\text{for every }j\in S_0,\qquad\text{and, if }s_0<k_{\max},\qquad v_j<\tau_{s_0+1}\quad\text{for every }j\notin S_0 .$$
Consequently
$$\Prob_0(\HPM=S_0)\ \le\ \psi\big(\lambda,\tau_{s_0}/h\big)^{s_0}\cdot\Big[2\Phi\big(\sqrt{\tau_{s_0+1}/h}\big)-1\Big]^{(p-s_0)\,\mathbf 1\{s_0<k_{\max}\}} . \tag{2.1}$$

*Proof.* For $j\in S_0$ the model $S_0\setminus\{j\}$ has size $s_0-1\le k_{\max}$, so it is a competitor, and by (1.5), (1.1), (1.2),
$$2\big[\mathrm{sc}(S_0)-\mathrm{sc}(S_0\setminus\{j\})\big]=2\log\frac{w(s_0)}{w(s_0-1)}-\log D+v_j=v_j-\tau_{s_0}.$$
If $\HPM=S_0$ this is positive. For $j\notin S_0$ and $s_0+1\le k_{\max}$, the model $S_0\cup\{j\}$ is a competitor and $2[\mathrm{sc}(S_0\cup\{j\})-\mathrm{sc}(S_0)]=v_j-\tau_{s_0+1}$, which must be negative. For (2.1): $\{v_j>\tau_{s_0}\}=\{(\sqrt\lambda+\zeta_j)^2>\tau_{s_0}/h\}$ has probability $\psi(\lambda,\tau_{s_0}/h)$ for each $j\in S_0$, and $\{v_j<\tau_{s_0+1}\}=\{\zeta_j^2<\tau_{s_0+1}/h\}$ has probability $2\Phi(\sqrt{\tau_{s_0+1}/h})-1$ for each $j\notin S_0$; the $p$ events are independent by Lemma 1.1(a), and the product of their probabilities bounds $\Prob_0(\HPM=S_0)$. $\square$

### 2.3 Sufficient conditions

For $T\subseteq S_0^c:=[p]\setminus S_0$ with $|T|=m\ge1$ define the **superset margin**
$$\Delta_T:=\sum_{i=s_0+1}^{s_0+m}\tau_i-\sum_{j\in T}v_j=m\log D+2\log\frac{w(s_0)}{w(s_0+m)}-\sum_{j\in T}v_j , \tag{2.2}$$
(the two forms agree by (1.2) and (1.1)); when $s_0+m\le k_{\max}$, $\Delta_T=2[\mathrm{sc}(S_0)-\mathrm{sc}(S_0\cup T)]$ by (1.5). For $J\subseteq S_0$ with $|J|=j\ge1$ define the **deletion margin**
$$\Gamma_J:=\sum_{i\in J}v_i-\sum_{i=s_0-j+1}^{s_0}\tau_i=2\big[\mathrm{sc}(S_0)-\mathrm{sc}(S_0\setminus J)\big]. \tag{2.3}$$

**Proposition 2.3 (decomposition of every competitor).** Let $S\ne S_0$ with $|S|\le k_{\max}$, $J=S_0\setminus S$, $T=S\setminus S_0$. Then
$$2\big[\mathrm{sc}(S_0)-\mathrm{sc}(S)\big]\ \ge\ \Gamma_J\,\mathbf 1\{J\ne\emptyset\}+\Delta_T\,\mathbf 1\{T\ne\emptyset\}.$$
Consequently $\HPM=S_0$ on the event
$$\mathcal A\cap\mathcal B,\qquad \mathcal A:=\{\Gamma_J>0\ \ \forall\,\emptyset\ne J\subseteq S_0\},\qquad \mathcal B:=\{\Delta_T>0\ \ \forall\,\emptyset\ne T\subseteq S_0^c\},$$
and $\mathcal A\supseteq\mathcal A':=\{v_j>\tau_1\ \ \forall j\in S_0\}$.

*Proof.* Put $j=|J|$, $m=|T|$, so $|S|=s_0-j+m$. By (1.5),
$$2[\mathrm{sc}(S_0)-\mathrm{sc}(S)]=\sum_{i\in J}v_i-\sum_{i\in T}v_i-(j-m)\log D+2\log\frac{w(s_0)}{w(s_0-j+m)} .$$
Write $2\log\frac{w(s_0)}{w(s_0-j+m)}=2\log\frac{w(s_0)}{w(s_0+m)}+2\log\frac{w(s_0+m)}{w(s_0+m-j)}$, and, by (1.1)–(1.2), for $1\le j\le k\le p$,
$$2\log\frac{w(k)}{w(k-j)}=\sum_{i=k-j+1}^{k}2\log\frac{i}{2p-i}=j\log D-\sum_{i=k-j+1}^{k}\tau_i .$$
With $k=s_0+m$ this gives
$$2[\mathrm{sc}(S_0)-\mathrm{sc}(S)]=\Big[\sum_{i\in J}v_i-\sum_{i=s_0+m-j+1}^{s_0+m}\tau_i\Big]+\Big[m\log D+2\log\frac{w(s_0)}{w(s_0+m)}-\sum_{i\in T}v_i\Big].$$
The second bracket is $\Delta_T$ (zero if $m=0$). In the first bracket, $\tau_i$ is decreasing in $i$, so $\sum_{i=s_0+m-j+1}^{s_0+m}\tau_i\le\sum_{i=s_0-j+1}^{s_0}\tau_i$, and the first bracket is at least $\Gamma_J$ (zero if $j=0$). The cases $j=0$ or $m=0$ (not both) are included. If $\mathcal A\cap\mathcal B$ holds, every competitor has a strictly smaller score than $S_0$, so $\HPM=S_0$. Finally, on $\mathcal A'$, $\Gamma_J>j\tau_1-\sum_{i=s_0-j+1}^{s_0}\tau_i\ge0$ by (1.3). $\square$

The event $\mathcal A'$ depends on $(\zeta_j)_{j\in S_0}$ only, $\mathcal B$ on $(\zeta_j)_{j\notin S_0}$ only; they are independent, and $\Prob(\mathcal A')=\psi(\lambda,\tau_1/h)^{s_0}$.

**Proposition 2.4 (the superset event).** Let $N:=p-s_0\ge1$ and $t_m:=\frac1h\sum_{i=s_0+1}^{s_0+m}\tau_i$ for $1\le m\le N$.

(a) $\displaystyle \Prob(\mathcal B^c)\le E_n:=\sum_{m=1}^{N}\binom Nm\Prob(\chi^2_m\ge t_m)$, and, with
$$r_n:=\sqrt{\frac{e\,\tau_{s_0+1}}{h\,D}}\ \le\ \sqrt{\frac{e\,(\log(n+1)+2\log(2n))}{n}}\cdot\sqrt{\tfrac1h},$$
whenever $r_n<1$,
$$E_n\ \le\ \sum_{m\ge1}\binom{s_0+m}{m}r_n^m=(1-r_n)^{-(s_0+1)}-1 .$$

(b) $\displaystyle \Prob(\mathcal B^c)\ \ge\ 1-\big[2\Phi(\sqrt{t_1})-1\big]^{N}\ \ge\ Nq_n\Big(1-\frac{Nq_n}2\Big),\qquad q_n:=2\bar\Phi(\sqrt{t_1}),\quad t_1=\tau_{s_0+1}/h .$$

(c) (Refined upper bound.) Whenever $r_n<1$,
$$\Prob(\mathcal B^c)\ \le\ Nq_n+\frac{(s_0+1)(s_0+2)}2\,r_n^2\,(1-r_n)^{-(s_0+3)} .$$
Moreover, for $t_1>1$,
$$\frac{N}{2p-s_0-1}\cdot\frac{2(s_0+1)}{\sqrt{2\pi t_1}}\Big(1-\frac1{t_1}\Big)e^{-\tau_{s_0+1}(1/h-1)/2}\,D^{-1/2}\ \le\ Nq_n\ \le\ \frac{N}{2p-s_0-1}\cdot\frac{2(s_0+1)}{\sqrt{2\pi t_1}}\,D^{-1/2}\ \le\ \frac{s_0+1}{\sqrt{2\pi t_1}}\,D^{-1/2},$$
with $\frac{N}{2p-s_0-1}=\frac{p-s_0}{2p-s_0-1}\in[\frac{p-s_0}{2p},\frac12]$. Hence, as $n\to\infty$ (uniformly in $s_0<p\le n$), $\Prob(\mathcal B^c)=Nq_n(1+o(1))\asymp n^{-1/2}(\log n)^{-1/2}$: the probability that some superset margin fails is of exact order $n^{-1/2}(\log n)^{-1/2}$, does not depend on $\lambda$, and depends on $p$ only through the factor $\frac{p-s_0}{2p-s_0-1}$ and through $t_1^{-1/2}$, $t_1=\tau_{s_0+1}/h\in[\log n,\ (\log(n+1)+2\log(2n))/h]$.

*Proof.* (a) For $j\notin S_0$, $v_j=h\zeta_j^2$, so $\Delta_T\le0$ iff $\sum_{j\in T}\zeta_j^2\ge t_m$, and $\sum_{j\in T}\zeta_j^2\sim\chi^2_m$. The union bound over the $\binom Nm$ sets of each size gives $E_n$. Since $t_m\ge m\log D/h>m$ (for $n\ge3$, $\log D/h\ge\log D\ge\log\frac{13}4>1$; for $n=2$, $\log D/h=\frac74\log\frac73>1$), the Chernoff bound $\Prob(\chi^2_m\ge t)\le e^{-\theta t}(1-2\theta)^{-m/2}$ with $\theta=\frac12(1-m/t)$ gives
$$\Prob(\chi^2_m\ge t_m)\le\Big(\frac{t_m}{m}\Big)^{m/2}e^{-(t_m-m)/2}=\Big(\frac{e\,t_m}{m}\Big)^{m/2}e^{-t_m/2}.$$
Since $h\le1$, $t_m\ge m\log D+2\log\frac{w(s_0)}{w(s_0+m)}$ by (2.2), so $e^{-t_m/2}\le D^{-m/2}\frac{w(s_0+m)}{w(s_0)}$; and $t_m/m\le\tau_{s_0+1}/h$ because $t_m/m$ is the average of $\tau_{s_0+1},\dots,\tau_{s_0+m}$ divided by $h$ and $\tau_i$ is decreasing. Next, by (1.1), $\frac{w(s_0+m)}{w(s_0)}=\prod_{i=s_0+1}^{s_0+m}\frac{i}{2p-i}\le\frac{(s_0+m)!}{s_0!\,(2p-s_0-m)^m}$, and $\binom Nm\le\frac{N^m}{m!}$, so
$$\binom Nm\frac{w(s_0+m)}{w(s_0)}\le\binom{s_0+m}{m}\Big(\frac{p-s_0}{2p-s_0-m}\Big)^m\le\binom{s_0+m}{m},\qquad\text{since }m\le p . \tag{2.4}$$
Therefore the $m$-th term of $E_n$ is at most $\binom{s_0+m}{m}\big(e\tau_{s_0+1}/(hD)\big)^{m/2}=\binom{s_0+m}{m}r_n^m$. Summing, $\sum_{m\ge1}\binom{s_0+m}mr^m=(1-r)^{-(s_0+1)}-1$ for $0\le r<1$ (binomial series). The numerical bound on $r_n$ uses $\tau_{s_0+1}\le\tau_1\le\log(n+1)+2\log(2n)$ and $D>n$.

(b) If $v_j\ge\tau_{s_0+1}$ for some $j\notin S_0$ then $\Delta_{\{j\}}\le0$, so $\mathcal B^c\supseteq\bigcup_{j\notin S_0}\{\zeta_j^2\ge t_1\}$, whose probability is $1-(1-q_n)^N$ by independence, $q_n=\Prob(\zeta^2\ge t_1)=2\bar\Phi(\sqrt{t_1})$. And $(1-q)^N\le1-Nq+\binom N2q^2\le1-Nq+\frac{(Nq)^2}2$.

(c) Separate the term $m=1$ of $E_n$, which equals $Nq_n$ exactly, and bound the terms $m\ge2$ as in (a): $\sum_{m\ge2}\binom{s_0+m}mr^m=(1-r)^{-(s_0+1)}-1-(s_0+1)r\le\frac{r^2}2\max_{0\le y\le r}\frac{d^2}{dy^2}(1-y)^{-(s_0+1)}=\frac{r^2}2(s_0+1)(s_0+2)(1-r)^{-(s_0+3)}$ (Taylor's formula with Lagrange remainder). For the size of $Nq_n$: by Lemma 1.3(d) (Mills' bounds), $2\phi(\sqrt{t_1})t_1^{-1/2}(1-t_1^{-1})\le q_n=2\bar\Phi(\sqrt{t_1})\le2\phi(\sqrt{t_1})t_1^{-1/2}$, and $\phi(\sqrt{t_1})=\frac1{\sqrt{2\pi}}e^{-\tau_{s_0+1}/2}e^{-\tau_{s_0+1}(1/h-1)/2}$ with $e^{-\tau_{s_0+1}/2}=D^{-1/2}\frac{s_0+1}{2p-s_0-1}$ by (1.2); multiply by $N$, use $e^{-\tau_{s_0+1}(1/h-1)/2}\le1$ on the upper side, and $\frac{p-s_0}{2p-s_0-1}\le\frac12$ (because $s_0\ge1$) and $\ge\frac{p-s_0}{2p}$ for the range of the prefactor. The last claims follow because $\tau_{s_0+1}(1/h-1)\le\tau_{s_0+1}\frac{n+1}{n^2}\to0$, $t_1\asymp\log n$ (as $\log n\le\tau_{s_0+1}\le\log(n+1)+2\log(2n)$), $D\asymp n$, and $r_n^2=O(\log n/n)=o(D^{-1/2}(\log D)^{-1/2})$. $\square$

**Remark 2.4′ (on the constants).** The bound in (c) is asymptotically of the right order; the closed form in (a) is not ($(1-r_n)^{-(s_0+1)}-1\sim(s_0+1)r_n\asymp\sqrt{\log n/n}$, a factor of order $\log n$ above $Nq_n\asymp1/\sqrt{n\log n}$); and both are loose at moderate $n$: at $n=p=2000$, $s_0=1$, one has $r_n\approx0.18$, so (a) gives $E_n\le0.47$ and (c) gives $\Prob(\mathcal B^c)\le0.0036+0.2$, whereas $Nq_n\approx0.0036$ and the Monte Carlo frequency of $\mathcal B^c$ is $\approx0.004$ (check C3). The slack is entirely in the Chernoff treatment of the $m\ge2$ terms (for $m=2$ the exact value is $\binom N2e^{-t_2/2}\approx\frac{(s_0+1)(s_0+2)}{8D}$, of order $n^{-1}$, against the bound's $3r_n^2\asymp\log n/n$); the $m=1$ term is exact. Nothing in Sections 2–5 depends on the constants, only on $r_n\to0$.

### 2.4 The sandwich and the sharp threshold

**Theorem 2.5 (known variance: nonasymptotic sandwich).** Let $X^\top X=nI_p$, $\sigma^2=\sigma_\star^2$ known, prior $\BB(1,p)$ with cap $k_{\max}$, $1\le s_0\le k_{\max}\le p$, $s_0<p$, $|\beta^\star_j|=\beta_n$ on $S_0$, $\lambda=n\beta_n^2/\sigma_\star^2$. With $\psi$ of Lemma 1.2, $\tau_k$ of (1.2), $E_n$ and $r_n$ of Proposition 2.4:
$$\psi\big(\lambda,\tau_1/h\big)^{s_0}\,(1-E_n)\ \le\ \Prob_0(\HPM=S_0)\ \le\ \psi\big(\lambda,\tau_{s_0}/h\big)^{s_0}\cdot\Big[2\Phi\big(\sqrt{\tau_{s_0+1}/h}\big)-1\Big]^{(p-s_0)\mathbf 1\{s_0<k_{\max}\}}, \tag{2.5}$$
with $E_n\le(1-r_n)^{-(s_0+1)}-1$ whenever $r_n=\sqrt{e\tau_{s_0+1}/(hD)}<1$ (Proposition 2.4(a)).

*Proof.* The upper bound is (2.1). For the lower bound, by Proposition 2.3, $\Prob_0(\HPM=S_0)\ge\Prob(\mathcal A'\cap\mathcal B)=\Prob(\mathcal A')\Prob(\mathcal B)$ by the independence noted after Proposition 2.3, $\Prob(\mathcal A')=\prod_{j\in S_0}\Prob((\sqrt\lambda+\zeta_j)^2>\tau_1/h)=\psi(\lambda,\tau_1/h)^{s_0}$ (Lemma 1.1(b), Lemma 1.2(a)), and $\Prob(\mathcal B)\ge1-E_n$ by Proposition 2.4(a). $\square$

The two sides of (2.5) differ only through $\tau_1$ versus $\tau_{s_0}$ (a shift of at most $2\log(2s_0)$, by (1.3)) and through the superset factors, which tend to $1$. This gives the sharp threshold.

**Corollary 2.6 (known variance: the sharp threshold).** Let $n\to\infty$, $s_0\ge1$ fixed, $p=p_n$ with $s_0<p_n\le n$, and any caps $k_{\max,n}\ge s_0$. Put
$$\tau_n:=\tau_{s_0}=\log D+2\log\frac{2p_n-s_0}{s_0}=\log n+2\log\frac{2p_n}{s_0}+O\Big(\frac{s_0}{p_n}+\frac1{n^2}\Big),\qquad c_n:=\sqrt{\lambda_n}-\sqrt{\tau_n}.$$
Then:

(i) if $c_n\to+\infty$, $\Prob_0(\HPM=S_0)\to1$;

(ii) if $c_n\to-\infty$, $\Prob_0(\HPM=S_0)\to0$;

(iii) if $c_n\to c\in\R$, $\Prob_0(\HPM=S_0)\to\Phi(c)^{s_0}$.

Conversely, $\Prob_0(\HPM=S_0)\to1$ only if $c_n\to+\infty$, and $\to0$ only if $c_n\to-\infty$. In particular $\Prob_0(\HPM=S_0)\to1$ if $\lambda_n\ge(1+\epsilon)\tau_n$ eventually, and $\to0$ if $\lambda_n\le(1-\epsilon)\tau_n$ eventually, for any fixed $\epsilon>0$; and $\lambda_n=\tau_n+2c\sqrt{\tau_n}+O(1)$ gives the limit $\Phi(c)^{s_0}$.

*Proof.* Four facts. (1) $E_n\to0$: $r_n^2=e\tau_{s_0+1}/(hD)=O(\log n/n)\to0$ since $D>n$ and $\tau_{s_0+1}\le\log(n+1)+2\log(2n)$. (2) The superset factor in (2.5) tends to $1$: with $q_n=2\bar\Phi(\sqrt{\tau_{s_0+1}/h})$, $[1-q_n]^{p-s_0}\ge1-(p-s_0)q_n\ge1-\frac{s_0+1}{2}D^{-1/2}\to1$ by Proposition 2.4(c). (3) For $t'_n\in\{\tau_{s_0}/h,\ \tau_1/h\}$, $\sqrt{t'_n}-\sqrt{\tau_n}\to0$: indeed $0\le t'_n-\tau_n\le\frac{\tau_1-\tau_{s_0}}{h}+\tau_{s_0}\big(\tfrac1h-1\big)\le\frac{2\log(2s_0)}{h}+\tau_{s_0}\frac{n+1}{n^2}$ by (1.3), and $\sqrt a-\sqrt b\le\frac{a-b}{2\sqrt b}$ with $b=\tau_n\ge\log n\to\infty$, while $\tau_{s_0}\frac{n+1}{n^2}=O(\log n/n)$. (4) Hence $\sqrt{\lambda_n}-\sqrt{t'_n}\to c$ (resp. $\pm\infty$), and by Lemma 1.2(c), $\psi(\lambda_n,t'_n)$ is squeezed between $\Phi(\sqrt{\lambda_n}-\sqrt{t'_n})$ and $\Phi(\sqrt{\lambda_n}-\sqrt{t'_n})+\Phi(-\sqrt{t'_n})$, where $\Phi(-\sqrt{t_n'})\to0$; so $\psi(\lambda_n,t'_n)\to\Phi(c)$ (resp. $1$, $0$). Inserting (1)–(4) in (2.5) gives (i)–(iii). For the converses: if $\Prob_0(\HPM=S_0)\to1$ but $c_n\not\to+\infty$, some subsequence has $c_n\le c'<\infty$, and along it the upper bound of (2.5) has $\limsup\le\Phi(c')^{s_0}<1$ (using (2)–(4) and the monotonicity of $\Phi$), a contradiction; if $\Prob_0(\HPM=S_0)\to0$ but $c_n\not\to-\infty$, some subsequence has $c_n\ge-c'>-\infty$, along which the lower bound has $\liminf\ge\Phi(-c')^{s_0}>0$. The "in particular" clauses: $\sqrt{(1+\epsilon)\tau_n}-\sqrt{\tau_n}=(\sqrt{1+\epsilon}-1)\sqrt{\tau_n}\to\infty$, similarly for $1-\epsilon$; and $\sqrt{\tau_n+2c\sqrt{\tau_n}+O(1)}-\sqrt{\tau_n}\to c$. The expansion of $\tau_n$: $\log D=\log n+O(n^{-2})$ and $2\log\frac{2p-s_0}{s_0}=2\log\frac{2p}{s_0}+2\log(1-\frac{s_0}{2p})$. $\square$

**Remark 2.7 (what the random $\hat k$ and the order statistics cost).** Corollary 2.6 says that, at the scale of the transition, the random size $\hat k$ and the noise order statistics reduce to a single comparison: the limit $\Phi(c)^{s_0}$ is the probability that *all $s_0$ signal coordinates* clear the last signal penalty, $\min_{j\in S_0}(\sqrt\lambda+\zeta_j)>\sqrt{\tau_n}+o(1)$. The mechanism: on $\mathcal B$ no superset of $S_0$ beats $S_0$, and $\Prob(\mathcal B)=1-O(n^{-1/2}(\log n)^{-1/2})$ for every $\lambda$ (Proposition 2.4), because the largest noise score $h\max_{j\notin S_0}\zeta_j^2\approx2\log p$ sits below the first noise penalty $\tau_{s_0+1}\approx\log n+2\log\frac{2p}{s_0+1}$ by about $\log n$, and the sum over supersets of every size $m$ is controlled by the exact inequality (2.4), in which the per-variable prior factors $\frac{i}{2p-i}$ cancel the $\binom{p-s_0}{m}$ count (for $m\ll p$ these factors are $\approx\frac{i}{2p}$ and the count is $\approx p^m/m!$). On $\mathcal A'\cap\mathcal B$ all three conditions (a)–(c) hold (Proposition 2.3), and condition (b) is the one that carries the transition: $\Prob(\mathcal A')=\psi(\lambda,\tau_1/h)^{s_0}$ tends to $1$, to $\Phi(c)^{s_0}$ or to $0$ according to $c_n$; in particular (a) has probability tending to $0$ when $\lambda_n$ stays bounded (then the signal scores are tight while the noise maximum diverges, for $p_n\to\infty$), so (a) is not free of $\lambda$. Condition (b) reduces to its $k=s_0-1$ term because the other suffix sums add terms $v_{(i)}-\tau_i$ with $v_{(i)}\ge v_{(s_0)}$ and $\tau_i-\tau_{s_0}\le2\log(2s_0)=o(\sqrt{\tau_n})$. The nonasymptotic price of the random $\hat k$ is the floor of Proposition 2.4(b), which is a floor on the HPM's error **when supersets are admissible**, $s_0<k_{\max}$: by Proposition 2.2,
$$\Prob_0(\HPM\ne S_0)\ \ge\ 1-(1-q_n)^{p-s_0}\ \ge\ Nq_n\big(1-\tfrac12Nq_n\big)\asymp n^{-1/2}(\log n)^{-1/2}\qquad\text{for every }\lambda,\ \text{if }s_0<k_{\max},$$
so the HPM is never exactly consistent at a rate faster than $n^{-1/2}(\log n)^{-1/2}$ in this model unless the cap forbids supersets (if $k_{\max}=s_0$ the error can decay exponentially in $\lambda$: for $p=2$, $s_0=k_{\max}=1$ it is at most $\Prob(h(\sqrt\lambda+\zeta_1)^2\le\tau_1)+\Prob(\zeta_2^2\ge(\sqrt\lambda+\zeta_1)^2)$, which is $O(e^{-c\lambda})$ for $\lambda\ge2\tau_1$). This complements T8(iii), whose rate $\sqrt{\log n/n}$ is an upper bound on $1-\Pi(S_0\mid y)$, a different object.

**Remark 2.8 (misspecified known variance; necessary condition only).** If the known value is $\sigma^2=c_\sigma\sigma_\star^2$ with $c_\sigma>0$, then $v_j=hu_j/\sigma^2$, and Proposition 2.2 holds verbatim with $\tau_k/h$ replaced by $c_\sigma\tau_k/h$ and $t_1$ by $c_\sigma t_1$. In particular, if $s_0<k_{\max}$,
$$\Prob_0(\HPM=S_0)\ \le\ \psi(\lambda,c_\sigma\tau_{s_0}/h)^{s_0}\Big[2\Phi\big(\sqrt{c_\sigma\tau_{s_0+1}/h}\big)-1\Big]^{p-s_0}\ \le\ \exp\big\{-(p-s_0)\,2\bar\Phi(\sqrt{c_\sigma t_1})\big\},$$
and by Mills' lower bound $(p-s_0)2\bar\Phi(\sqrt{c_\sigma t_1})\ge c\,(p-s_0)\,t_1^{-1/2}e^{-c_\sigma\tau_{s_0+1}/(2h)}\asymp\frac{p-s_0}{\sqrt{\log n}}\Big(\frac{s_0+1}{2p-s_0-1}\Big)^{c_\sigma}D^{-c_\sigma/2}$. For $p\asymp n$ this tends to infinity when $c_\sigma<\frac23$, so an underestimated variance with $c_\sigma<\frac23$ makes $\Prob_0(\HPM=S_0)\to0$ *whatever the signal*: at least one noise variable then clears its penalty. The signal side of Theorem 2.5 transfers in the same way (replace $\tau_1/h$ by $c_\sigma\tau_1/h$); the superset bound $E_n$ is not re-derived here for $c_\sigma\ne1$, so no sufficiency statement is made for the misspecified case.
## 3. The minimax threshold, and the gap

### 3.1 A Bayes lower bound for every selector (self-contained)

Fix $n,p,s_0,\beta_n,\sigma_\star$ with $1\le s_0<p$ and $\beta_n>0$ (so $\lambda>0$), and let $\mathcal C$ be the class of coefficient vectors $\beta^\star$ with $|\operatorname{supp}\beta^\star|=s_0$ and $|\beta^\star_j|=\beta_n$ on the support (the class of Pb1), and $\mathcal C^+\subset\mathcal C$ its subclass with $\beta^\star_j=+\beta_n$ on the support. A **selector** is any measurable map $\hat S$ from $y$ (and, if one likes, an independent randomisation) to subsets of $[p]$; it may use $n,p,s_0,\beta_n,\sigma_\star$. Write $\Prob_{\beta^\star}$ for the law of $y$ under $\beta^\star$. Define the **oracle errors**
$$\rho_n(\lambda):=\Prob\Big(\min_{1\le i\le s_0}(\sqrt\lambda+\zeta_i)\le\max_{s_0<j\le p}\zeta_j\Big),\qquad \rho_n^{|\cdot|}(\lambda):=\Prob\Big(\min_{1\le i\le s_0}|\sqrt\lambda+\zeta_i|\le\max_{s_0<j\le p}|\zeta_j|\Big),$$
with $\zeta_1,\dots,\zeta_p$ i.i.d. $N(0,1)$. Two selectors are compared with them: the **signed oracle** $\hat S^{\rm sg}$, the set of the $s_0$ largest $z_j$, and the **absolute oracle** $\hat S^{\rm or}$, the set of the $s_0$ largest $|z_j|$ (equivalently of the $s_0$ largest $u_j$). Both use $s_0$ and nothing else.

**Theorem 3.1 (every selector; the two oracles).**
(a) For every selector $\hat S$: $\displaystyle\sup_{\beta^\star\in\mathcal C}\Prob_{\beta^\star}(\hat S\ne S_0)\ \ge\ \sup_{\beta^\star\in\mathcal C^+}\Prob_{\beta^\star}(\hat S\ne S_0)\ \ge\ \rho_n(\lambda)$.
(b) $\Prob_{\beta^\star}(\hat S^{\rm sg}\ne S_0)=\rho_n(\lambda)$ for every $\beta^\star\in\mathcal C^+$ (so $\hat S^{\rm sg}$ is minimax over $\mathcal C^+$), and $\Prob_{\beta^\star}(\hat S^{\rm or}\ne S_0)=\rho_n^{|\cdot|}(\lambda)$ for every $\beta^\star\in\mathcal C$. At finite $n$, $\rho_n\le\rho_n^{|\cdot|}$ with strict inequality in general (for $p=2$, $s_0=1$: $1-\rho_n=\Phi(\sqrt{\lambda/2})$ while $1-\rho_n^{|\cdot|}=\Phi(\sqrt{\lambda/2})^2+\bar\Phi(\sqrt{\lambda/2})^2$).
(c) (Asymptotics.) Let $n\to\infty$, $s_0$ fixed, $N:=p_n-s_0\to\infty$, and $d_n:=\sqrt{\lambda_n}-\sqrt{2\log N}$. Then $\rho_n\to0$ iff $\rho_n^{|\cdot|}\to0$ iff $d_n\to+\infty$; $\rho_n\to1$ iff $\rho_n^{|\cdot|}\to1$ iff $d_n\to-\infty$; and if $d_n\to c\in\R$ then $\rho_n\to1-\Phi(c)^{s_0}$ and $\rho_n^{|\cdot|}\to1-\Phi(c)^{s_0}$.

*Proof.* (a) The first inequality is trivial. For the second, put the uniform prior on the $\binom p{s_0}$ supports $S\subseteq[p]$, $|S|=s_0$, and $\beta^{(S)}=\beta_n\mathbf 1_S\in\mathcal C^+$. For a non-randomised selector, the maximal risk over $\mathcal C^+$ is at least the Bayes risk $\frac1{\binom p{s_0}}\sum_S\Prob_{\beta^{(S)}}(\hat S\ne S)$, which is at least the Bayes risk of the Bayes rule for $0$–$1$ loss, the posterior mode. The likelihood of $y$ under $\beta^{(S)}$ is proportional to $\exp\{-\|y-X\beta^{(S)}\|^2/(2\sigma_\star^2)\}$ and $\|y-X\beta^{(S)}\|^2=\|y\|^2-2\beta_n\sum_{j\in S}z_j+n\beta_n^2s_0$ (orthogonality), so the posterior over $S$ is proportional to $\exp\{\beta_n\sum_{j\in S}z_j/\sigma_\star^2\}$, and its mode is the set of the $s_0$ largest $z_j$, i.e. $\hat S^{\rm sg}$ (ties have probability zero). Its Bayes risk is $\frac1{\binom p{s_0}}\sum_S\Prob_{\beta^{(S)}}(\hat S^{\rm sg}\ne S)$. Under $\beta^{(S)}$, by Lemma 1.1(b), $z_j/(\sqrt n\sigma_\star)=\sqrt\lambda\mathbf 1\{j\in S\}+\zeta_j$ with $(\zeta_j)$ i.i.d. $N(0,1)$, so $\{\hat S^{\rm sg}\ne S\}=\{\min_{i\in S}(\sqrt\lambda+\zeta_i)\le\max_{j\notin S}\zeta_j\}$, whose probability is $\rho_n(\lambda)$ for every $S$ by exchangeability of the $\zeta_j$. For a randomised selector, the Bayes risk is an average over the randomisation of Bayes risks of non-randomised selectors, each at least $\rho_n(\lambda)$, and the maximal risk is at least the Bayes risk.
(b) The first claim was shown in (a). For the second, by Lemma 1.1(b) and Lemma 1.2(a), $|z_j|/(\sqrt n\sigma_\star)\overset d=|\sqrt\lambda+\zeta_j|$ for $j\in S_0$ and $=|\zeta_j|$ for $j\notin S_0$, jointly independent, so $\{\hat S^{\rm or}\ne S_0\}=\{\min_{i\in S_0}|\sqrt\lambda+\zeta_i|\le\max_{j\notin S_0}|\zeta_j|\}$ has probability $\rho^{|\cdot|}_n(\lambda)$, whatever the signs of $\beta^\star$. The inequality $\rho_n\le\rho_n^{|\cdot|}$ is (a) applied to the selector $\hat S^{\rm or}$, whose error on $\mathcal C^+$ is $\rho_n^{|\cdot|}$. The $p=2$, $s_0=1$ formulas: $1-\rho_n=\Prob(\sqrt\lambda+\zeta_1>\zeta_2)=\Phi(\sqrt{\lambda/2})$, and $\{\hat S^{\rm or}=S_0\}=\{|\sqrt\lambda+\zeta_1|>|\zeta_2|\}$, whose probability is computed by conditioning on the signs of $\sqrt\lambda+\zeta_1\pm\zeta_2$: it equals $\Prob(\sqrt\lambda+\zeta_1>|\zeta_2|)+\Prob(\sqrt\lambda+\zeta_1<-|\zeta_2|)=\Prob(\zeta_1-\zeta_2>-\sqrt\lambda,\ \zeta_1+\zeta_2>-\sqrt\lambda)+\Prob(\zeta_1-\zeta_2<-\sqrt\lambda,\ \zeta_1+\zeta_2<-\sqrt\lambda)=\Phi(\sqrt{\lambda/2})^2+\bar\Phi(\sqrt{\lambda/2})^2$, since $\zeta_1\pm\zeta_2$ are independent $N(0,2)$.
(c) *Step 1: the noise maxima.* Let $\mathsf M_N:=\max_{j\le N}\zeta_j$ and $\mathsf M_N^{|\cdot|}:=\max_{j\le N}|\zeta_j|$. We claim $\mathsf M_N-\sqrt{2\log N}\to0$ and $\mathsf M_N^{|\cdot|}-\sqrt{2\log N}\to0$ in probability. For $\eta>0$, by Lemma 1.3(d),
$$\Prob\big(\mathsf M_N^{|\cdot|}\ge\sqrt{2\log N}+\eta\big)\le2N\bar\Phi(\sqrt{2\log N}+\eta)\le Ne^{-(\sqrt{2\log N}+\eta)^2/2}\le e^{-\eta\sqrt{2\log N}}\to0,$$
and with $x_N:=\sqrt{2\log N}-\eta$ (for $N$ so large that $x_N>1$),
$$\Prob(\mathsf M_N\le x_N)=\Phi(x_N)^N\le e^{-N\bar\Phi(x_N)},\qquad N\bar\Phi(x_N)\ge N\phi(x_N)\big(x_N^{-1}-x_N^{-3}\big)=\frac{e^{\eta\sqrt{2\log N}-\eta^2/2}}{\sqrt{2\pi}}\big(x_N^{-1}-x_N^{-3}\big)\to\infty,$$
using $Ne^{-x_N^2/2}=e^{\eta\sqrt{2\log N}-\eta^2/2}$. Since $\mathsf M_N\le\mathsf M_N^{|\cdot|}$, both claims follow.
*Step 2: $\rho_n$.* Let $m_{s_0}:=\min_{i\le s_0}\zeta_i$, independent of $\mathsf M_N$, with continuous distribution function $F(x)=1-\bar\Phi(x)^{s_0}$. Then $\rho_n=\Prob(m_{s_0}\le\mathsf M_N-\sqrt{\lambda_n})=\E F(W_n)$ with $W_n:=\mathsf M_N-\sqrt{\lambda_n}=(\mathsf M_N-\sqrt{2\log N})-d_n$. If $d_n\to c$, then $W_n\to-c$ in probability and, $F$ being bounded and continuous, $\E F(W_n)\to F(-c)=1-\Phi(c)^{s_0}$. If $d_n\to+\infty$ then $W_n\to-\infty$ in probability and $\E F(W_n)\le F(-K)+\Prob(W_n>-K)\to F(-K)$ for every $K$, so $\rho_n\to0$; if $d_n\to-\infty$, symmetrically $\rho_n\to1$.
*Step 3: $\rho_n^{|\cdot|}$.* On the event $\{\min_{i\le s_0}(\sqrt\lambda+\zeta_i)>0\}$, of probability $\Phi(\sqrt\lambda)^{s_0}$, $\min_i|\sqrt\lambda+\zeta_i|=\sqrt\lambda+m_{s_0}$. If $d_n\to c$ or $+\infty$ then $\lambda_n\to\infty$, this event has probability $\to1$, and $\rho_n^{|\cdot|}=\Prob(m_{s_0}\le\mathsf M_N^{|\cdot|}-\sqrt{\lambda_n})+o(1)$, to which Step 2 applies with $\mathsf M_N^{|\cdot|}$ in place of $\mathsf M_N$ (Step 1 covers it). If $d_n\to-\infty$: along any subsequence with $\lambda_n\to\infty$ the same argument gives $\rho_n^{|\cdot|}\to1$; along any subsequence with $\lambda_n$ bounded, $\min_i|\sqrt{\lambda_n}+\zeta_i|$ is tight while $\mathsf M_N^{|\cdot|}\to\infty$ in probability, so $\rho_n^{|\cdot|}\to1$ as well.
*Step 4: the "iff"s.* By Steps 2–3, $d_n\to\pm\infty$ gives the limits $0$, $1$. Conversely, if $\rho_n\to0$ but $d_n\not\to+\infty$, some subsequence has $d_n\le c'$, and along a further subsequence $d_n\to c''\in[-\infty,c']$, where the limit of $\rho_n$ is $1-\Phi(c'')^{s_0}>0$ (or $1$), a contradiction; the other cases are identical. $\square$

**Corollary 3.2 (the minimax threshold for fixed $s_0$).** Let $n\to\infty$ with $s_0$ fixed and $p_n-s_0\to\infty$. In the orthogonal model with known $\sigma_\star^2$, exact support recovery uniformly over $\mathcal C$ (indeed over $\mathcal C^+$) with probability tending to one is possible iff $d_n=\sqrt{\lambda_n}-\sqrt{2\log(p_n-s_0)}\to+\infty$. The "only if" is Theorem 3.1(a),(c). The "if" is attained by $\hat S^{\rm or}$ (Theorem 3.1(b),(c)), and also, without knowledge of $s_0$, by the thresholding selector
$$\hat S^{\rm thr}:=\Big\{j:\frac{|z_j|}{\sqrt n\sigma_\star}>\sqrt{2\log p_n}+\tfrac12d_n'\Big\},\qquad d_n':=\sqrt{\lambda_n}-\sqrt{2\log p_n},$$
which uses $p_n$, $\sigma_\star$ and $\lambda_n$ but not $s_0$: $d'_n-d_n=\sqrt{2\log(p_n-s_0)}-\sqrt{2\log p_n}\to0$, so $d'_n\to\infty$; no false positive occurs when $\mathsf M^{|\cdot|}_{N}<\sqrt{2\log p_n}+\frac12d'_n$, whose complement has probability $\le2Ne^{-(\sqrt{2\log p_n}+d'_n/2)^2/2}\le2e^{-d'_n\sqrt{2\log p_n}/2}\to0$ (Lemma 1.3(d), as in Step 1, with $N\le p_n$); no false negative occurs when $\min_{i\in S_0}|\epsilon_i\sqrt{\lambda_n}+\zeta_i|>\sqrt{2\log p_n}+\frac12d'_n$, which (by Lemma 1.2(a), the signs $\epsilon_i$ being irrelevant to the law, and $|x|\ge x$) has probability at least that of $\min_{i\in S_0}(\sqrt{\lambda_n}+\zeta_i)>\sqrt{2\log p_n}+\frac12d'_n$, i.e. (since $\sqrt{\lambda_n}-\sqrt{2\log p_n}-\frac12d'_n=\frac12d'_n$) when $m_{s_0}>-\frac12d'_n$, whose complement has probability $1-\Phi(\frac12d'_n)^{s_0}\to0$. In the critical regime $d_n\to c$, no selector has maximal error over $\mathcal C^+$ tending below $1-\Phi(c)^{s_0}$; the absolute oracle attains this limit at every point of $\mathcal C$, the signed one at every point of $\mathcal C^+$. So the **minimax threshold** has centre $\tau_n^{\rm mm}:=2\log(p_n-s_0)$ on the $\lambda$-scale, with a window of width $\asymp\sqrt{\log(p_n-s_0)}$ and the same limit shape $\Phi(c)^{s_0}$ as the HPM's (Corollary 2.6).

The achievability side therefore does not need $s_0$, so the lower bound of Theorem 3.1 is not an artefact of giving the oracles $s_0$. When $p_n-s_0$ stays bounded the question is degenerate (any $\lambda_n\to\infty$ gives recovery by the oracles, with no sharp centre); this case is excluded from the comparison below.

### 3.2 Relation to the cited minimax statements (CITED_RESULTS.md)

The relevant source is Butucea, Ndaoud, Stepanova and Tsybakov (2018), entry E1 of CITED_RESULTS.md, whose model (1) is our sequence model with $d=p$, $X_j=z_j/\sqrt n$, $\theta_j=\sqrt n\beta^\star_j$, $\sigma=\sigma_\star$, $a=\sqrt n\beta_n$, so that $a/\sigma=\sqrt{\lambda_n}$ (translation in E1). What the source states, and how it relates to Theorem 3.1:

- E1's Theorem 4.1(ii) characterises *exact recovery in the Hamming sense* (Definition 4.1, (25): $\sup_\theta\E_\theta|\hat\eta-\eta|\to0$) by $s_d\Psi_+(d,s_d,a_d)\to0$, with $\Psi_+$ the explicit two-term Gaussian-tail expression quoted in E1.2, over the larger classes $\Theta_d(s,a)$ ("at most $s$ nonzero, $|\theta_j|\ge a$"). Since $\Prob_\theta(\hat S\ne S)\le\E_\theta|\hat\eta-\eta|$ (their (2)), Hamming-exact recovery implies recovery in probability, so their sufficiency direction gives, for our class, recovery in probability by their thresholding selector (8) with threshold (5) whenever $s_0\Psi_+(p,s_0,\sqrt n\beta_n)\to0$. For fixed $s_0$, the researcher's reading E1.7 (not a statement of the source; checked here) is that this holds iff $\sqrt{\lambda_n}-\sqrt{2\log((p-s_0)/s_0)}\to+\infty$, which coincides with the condition of Corollary 3.2 because $\sqrt{2\log((p-s_0)/s_0)}-\sqrt{2\log(p-s_0)}=O(1/\sqrt{\log p})\to0$. *Check of E1.7:* with $x=a/\sigma$ and $\ell=\log(d/s-1)$, $(x/2+\ell/x)^2=x^2/4+\ell+\ell^2/x^2$, so $(d/s-1)\Phi(-x/2-\ell/x)\le e^{\ell}\cdot\frac12e^{-(x/2+\ell/x)^2/2}=\frac12e^{-(x/2-\ell/x)^2/2}$, and the second term of $\Psi_+$ is $\Phi(-(x/2-\ell/x))$; so $\Psi_+\to0$ iff $x/2-\ell/x=\frac{(x-\sqrt{2\ell})(x+\sqrt{2\ell})}{2x}\to+\infty$ (the second term forces the sign, and if $x/2-\ell/x$ stays bounded above along a subsequence the second term stays bounded away from $0$), which for $x=O(\sqrt\ell)$ is $x-\sqrt{2\ell}\to\infty$, and for $x/\sqrt\ell\to\infty$ holds trivially. So E1.7 is correct.
- The source's *lower bounds* on the probability of wrong recovery (Theorem 2.6, (17)–(18); Theorem 4.5) are over **separable** selectors only (each coordinate decided from its own observation), and its all-selector Hamming lower bound (Theorem 2.2, second inequality) carries a remainder $-\frac{4s'}s\exp\{-(s-s')^2/(2s)\}$ that does not vanish for fixed $s$. The source says (p. 16) that for $\limsup s_d<\infty$ exact and almost full recovery are equivalent and restricts its sharp phase transition (Theorem 4.4, critical value (43) $a_d^*=\sigma(\sqrt{2\log(d-s_d)}+\sqrt{2\log s_d})$) to $s_d\to\infty$. **For fixed $s_0$ no all-selector lower bound on the probability of wrong recovery was found in the sources** (LITERATURE.md; the "only if" of Theorem 4.1(ii) is formally an all-selector Hamming statement without restriction on $s_d$, but the researcher flags that its derivation for bounded $s_d$ is not shown in the source). Theorem 3.1(a),(c) supplies such a bound for the class of Pb1 by the Bayes argument; it is elementary and self-contained, and consistent with E1 where they overlap: for $s_0$ fixed, (43) reads $\sqrt{2\log(p-s_0)}+\sqrt{2\log s_0}$, which differs from our centre $\sqrt{2\log(p-s_0)}$ by the constant $\sqrt{2\log s_0}$ on the $\sqrt\lambda$-scale; Theorem 3.1(c) shows that for fixed $s_0$ this constant is not needed (the oracles already recover when $\sqrt{\lambda_n}-\sqrt{2\log(p-s_0)}\to\infty$), in agreement with the source's own remark that its Theorem 4.4 is stated for $s_d\to\infty$. The signed oracle $\hat S^{\rm sg}$ is the exhaustive-search estimator of E1's Remark 4.1.
- Entries E2–E4 (Ndaoud–Tsybakov 2020, Wainwright 2009, Ji–Jin 2012) concern random Gaussian designs and give the order $\lambda_n\asymp\log p$ with unspecified constants (E2, E3) or the exact-recovery region $r=\lambda_n/(2\log p)>(1+\sqrt{1-\vartheta'})^2$ for polynomially many signals $s=p^{1-\vartheta'}$, $0<\vartheta'<1$ (E4; their sparsity exponent is written $\vartheta'$ here to keep $\vartheta$ for $p_n=n^{\vartheta}$ below), whose formal boundary value at $\vartheta'=1$ is $\lambda_n>2\log p$. None applies to a fixed orthogonal design with fixed $s_0$ as stated; they are consistent with Corollary 3.2 but are not used.

### 3.3 The gap, and the draft's heuristic

**Theorem 3.3 (the gap between the HPM and the minimax threshold; known variance).** In the setting of Corollary 2.6 with $p_n-s_0\to\infty$:

(a) (Centres on the $\lambda$-scale.) $\tau_n-\tau_n^{\rm mm}=\log D+2\log\frac{2p_n-s_0}{s_0(p_n-s_0)}=\log n+2\log2-2\log s_0+2\log\frac{1-s_0/(2p_n)}{1-s_0/p_n}+O(n^{-2})=\log n+2\log2-2\log s_0+o(1)$; and $\tau_1-\tau_n^{\rm mm}=\log n+2\log2+o(1)$.

(b) (Centres on the $\sqrt\lambda$-scale, where the transitions have $O(1)$ windows.) $\sqrt{\tau_n}-\sqrt{\tau_n^{\rm mm}}=\dfrac{\log n+O(1)}{\sqrt{\tau_n}+\sqrt{2\log(p_n-s_0)}}\to+\infty$; for $p_n=n$ this is $\frac{\sqrt{\log n}}{\sqrt3+\sqrt2}(1+o(1))$.

(c) (Strict suboptimality.) There are sequences $\lambda_n$ for which the absolute oracle $\hat S^{\rm or}$ and the thresholding selector of Corollary 3.2 (and, on $\mathcal C^+$, the signed oracle) recover $S_0$ with probability $\to1$ while $\Prob_0(\HPM=S_0)\to0$: any $\lambda_n$ with $\sqrt{\lambda_n}-\sqrt{2\log(p_n-s_0)}\to+\infty$ and $\sqrt{\lambda_n}-\sqrt{\tau_n}\to-\infty$, e.g. $\lambda_n=(\sqrt{2\log n}+\log\log n)^2$ when $p_n=n$. In ratio form: for every fixed $\epsilon>0$, $\lambda_n\ge(1+\epsilon)\tau_n$ eventually gives $\Prob_0(\HPM=S_0)\to1$ and $\lambda_n\le(1-\epsilon)\tau_n$ eventually gives $\to0$ (Corollary 2.6), whereas $\lambda_n\ge(1+\epsilon)2\log(p_n-s_0)$ eventually suffices for the oracles and $\lambda_n\le(1-\epsilon)2\log(p_n-s_0)$ eventually defeats every selector (Corollary 3.2); with $p_n=n^{\vartheta}$, $0<\vartheta\le1$, $\tau_n\sim(1+2\vartheta)\log n$ and $\tau_n^{\rm mm}\sim2\vartheta\log n$, so at leading order the HPM needs $\frac{1+2\vartheta}{2\vartheta}$ times the minimax signal strength ($\frac32$ at $p_n=n$).

*Proof.* (a) is (1.2) with $k=s_0$ (resp. $k=1$) and the expansions $\log D=\log n+O(n^{-2})$, $\frac{2p-s_0}{s_0(p-s_0)}=\frac{2}{s_0}\cdot\frac{1-s_0/(2p)}{1-s_0/p}$, $\frac{2p-1}{p-s_0}\to2$. (b) $\sqrt a-\sqrt b=(a-b)/(\sqrt a+\sqrt b)$ with (a); for $p_n=n$, $\tau_n=3\log n+O(1)$ and $\tau_n^{\rm mm}=2\log n+o(1)$, so the denominator is $(\sqrt3+\sqrt2)\sqrt{\log n}(1+o(1))$. (c) The first claim is Corollary 3.2 together with Corollary 2.6(ii). For the example with $p_n=n$: $\tau_n=\log D+2\log\frac{2n-s_0}{s_0}=3\log n+2\log\frac2{s_0}+o(1)$, hence $\sqrt{\tau_n}=\sqrt{3\log n}+O((\log n)^{-1/2})$, and $\sqrt{\lambda_n}-\sqrt{\tau_n}=(\sqrt2-\sqrt3)\sqrt{\log n}+\log\log n+O((\log n)^{-1/2})\to-\infty$, while $\sqrt{\lambda_n}-\sqrt{2\log(n-s_0)}=\log\log n+o(1)\to\infty$. The ratio form restates the "in particular" clause of Corollary 2.6 and Corollary 3.2 ($\sqrt{(1\pm\epsilon)a}-\sqrt a=(\sqrt{1\pm\epsilon}-1)\sqrt a\to\pm\infty$ for $a\to\infty$). $\square$

**Verdict on the draft's heuristic ("the threshold for $n\beta_n^2/\sigma_\star^2$ exceeds the minimax one by about $\log n+2\log2$").**

- *The $\log n$ is confirmed and sharp.* By Theorem 3.3(a),(b) the HPM's centre exceeds the minimax centre by $\log n+O(1)$ on the $\lambda$-scale, which is $\asymp\sqrt{\log n}$ on the $\sqrt\lambda$-scale where both windows have width $O(1)$. The $\log n$ is the $g=n$ Occam factor $D^{-1/2}\approx(n+1)^{-1/2}$ per variable (P4(i)).
- *The constant $2\log2$: confirmed at the level of the leading-order centres, not determined at finite $n$.* Theorem 3.3(a) compares the two centres that the finite-$n$ bounds of Theorem 2.5 provide for the HPM, $\tau_{s_0}$ (the exact penalty in the necessary condition of Proposition 2.2) and $\tau_1$ (the penalty in the sufficient condition $\mathcal A'$), with the leading-order minimax centre $2\log(p_n-s_0)$ of Corollary 3.2: the gaps are $\log n+2\log2-2\log s_0+o(1)$ and $\log n+2\log2+o(1)$ respectively. For $s_0=1$ both equal $\log n+2\log2+o(1)$, as the draft says. No finer statement follows from the results here: the trichotomies of Corollaries 2.6 and 3.2 are invariant under recentring by $o(\sqrt{\tau_n})$ and $o(\sqrt{\log(p_n-s_0)})$ respectively, so no $O(1)$ constant is visible in the limits; the finite-$n$ bounds of Theorem 2.5 involve the two penalties $\tau_{s_0}$ and $\tau_1$ and define no centre; and the minimax centre $2\log(p_n-s_0)$ is the leading term of the extreme-value centring of the noise maximum, whose second-order terms are of order $\log\log p_n$ on the $\lambda$-scale and are not quantified here. The numerical checks are consistent with this: at $n=p=2000$ the oracle $\hat S^{\rm or}$ succeeds with frequency $0.61$ at $\sqrt\lambda=\sqrt{2\log(p-s_0)}$ for $s_0=1$ (limit $\Phi(0)=0.5$; check C5), i.e. the finite-$n$ minimax crossing lies below $2\log(p-s_0)$, so the finite-$n$ constant measured between the $2^{-s_0}$-crossings exceeds $2\log2$ there (reviewers' numerical integrations, not part of `check_Pb1.py`: `review/round2/opus_B_scratch/mc_K3.out` and `review/round3/opus_A_scratch/k3_crossings.out`; about $4.8$ against the signed oracle and about $3.6$ against the absolute oracle, for $s_0=1$); and the HPM's finite-$n$ transition sits near $\tau_{s_0}/h$ rather than $\tau_1/h$ (check C3). These are observations, not theorems.
- *Where the constant comes from.* $2\log2-2\log s_0$ is the $\BB(1,p)$ per-model odds for the last signal variable, $w(s_0-1)/w(s_0)=(2p-s_0)/s_0\approx2p/s_0$ (L6(i)), measured against the $p-s_0\approx p$ noise coordinates that the oracles must beat; the $2\log2$ alone is the same odds for the first inclusion, $(2p-1)/1$. (At $s_0=2$ the lower-end constant is $0$; for $s_0\ge3$ it is negative, and for $p>2$, $s_0=2$ the exact lower-end gap $\log D+2\log\frac{p-1}{p-2}$ still exceeds $\log n$.)
- *The structural reason:* the HPM compares the smallest signal with the *prior and Occam penalty* $\tau_{s_0}\approx\log n+2\log(2p/s_0)$ of its own inclusion (Proposition 2.2), whereas the oracles compare it with the *largest noise score* $\approx2\log p$. The HPM's transition does not involve the noise maximum: by Proposition 2.4 the noise coordinates are irrelevant at the scale of the transition (their contribution is a $\lambda$-free floor of order $n^{-1/2}(\log n)^{-1/2}$ when $s_0<k_{\max}$). This is what P3 (the size-only ceiling) anticipates: a size-only prior can only decide through its penalty, and $\BB(1,p)$ with $g=n$ pays $\log n$ for the size uncertainty it resolves. It is also the price of a method that needs neither $s_0$ nor $\sigma_\star$ (Section 5) and, in the known-variance case, keeps the superset error at order $n^{-1/2}(\log n)^{-1/2}$ uniformly in $p\le n$ (Proposition 2.4).
## 4. Summary of the known-variance answer to Pb1

For the record, the three questions of Pb1 under known variance:

1. *Characterise $\Prob_0(\HPM\ne S_0)$ accounting for $\hat k$ and the order statistics.* Proposition 2.1 (exact event), Theorem 2.5 (nonasymptotic sandwich), Corollary 2.6 (sharp threshold with the limit $\Phi(c)^{s_0}$), Proposition 2.4 and Remark 2.7 (the $\lambda$-free superset floor of exact order $n^{-1/2}(\log n)^{-1/2}$ when $s_0<k_{\max}$; at the scale of the transition, the random $\hat k$ costs nothing beyond the single comparison of Proposition 2.2, although at a fixed $\lambda$ near $\tau_n$ the wrong-size event has probability of order one, as the limit $\Phi(c)^{s_0}<1$ shows).
2. *Compare with the minimax threshold.* Theorem 3.1, Corollary 3.2 (centre $2\log(p-s_0)$, same window shape), Theorem 3.3 (gap).
3. *The heuristic.* The $\log n$ is confirmed and sharp; the constant $2\log2$ is the leading-order-centre constant for $s_0=1$ (and for the $\tau_1$ centre for every $s_0$); the finite-$n$ constant is not determined by the limit theorems (Section 3.3).

---

## 5. Integrated variance: the paper's prior

Now the variance is integrated against $\IG(a_0,b_0)$, $a_0,b_0>0$, and the score is $\mathrm{sc}(S)=\log w(|S|)-\frac{|S|}2\log D-\nu\log A_S$, $A_S=2b_0+Q_S$, $\nu=a_0+\frac n2$ (Section 1.3). Everything else is as in Section 2: $X^\top X=nI_p$, $1\le s_0\le k_{\max}\le p$, $s_0<p$, $|\beta^\star_j|=\beta_n$ on $S_0$, $\lambda=n\beta_n^2/\sigma_\star^2$. Put
$$A:=A_{S_0}=2b_0+Q_{S_0},\qquad U_T:=\sum_{j\in T}u_j\ (T\subseteq[p]),\qquad R':=\frac{\|(I-P_{S_0})\varepsilon\|^2}{\sigma_\star^2}\sim\chi^2_{n-s_0}.$$
By Lemma 1.1(c),(d), $Q_{S_0}=\sigma_\star^2R'+(1-h)U_{S_0}$, so
$$A=2b_0+\sigma_\star^2R'+(1-h)U_{S_0}\ \ge\ \sigma_\star^2R',\qquad R'\text{ independent of }(\zeta_j)_{j\in S_0}. \tag{5.1}$$
(The independence is recorded for completeness; the bounds below use only union bounds and do not need it.)

### 5.1 Margins and the decomposition

For $\emptyset\ne J\subseteq S_0$ with $|J|=j$ and $\emptyset\ne T\subseteq S_0^c$ with $|T|=m$, since $Q_{S_0\setminus J}=Q_{S_0}+hU_J$ and $Q_{S_0\cup T}=Q_{S_0}-hU_T$ (Lemma 1.1(c)), the one-sided margins are
$$\Gamma^{\rm iv}_J:=2\big[\mathrm{sc}(S_0)-\mathrm{sc}(S_0\setminus J)\big]=2\nu\log\Big(1+\frac{hU_J}{A}\Big)-\sum_{i=s_0-j+1}^{s_0}\tau_i, \tag{5.2}$$
$$\Delta^{\rm iv}_T:=\sum_{i=s_0+1}^{s_0+m}\tau_i-2\nu\log\frac{A}{A-hU_T}, \tag{5.3}$$
where (5.3) is defined for every $T$ ($A-hU_T=2b_0+Q_{S_0\cup T}>0$ by the shrinkage floor (2.2) of the draft, re-derived here: $Q_S\ge\|y\|^2/(n+1)$ since $h\sum_{j\in S}u_j\le h\|P_{[p]}y\|^2\le\frac{n}{n+1}\|y\|^2$) and equals $2[\mathrm{sc}(S_0)-\mathrm{sc}(S_0\cup T)]$ whenever $s_0+m\le k_{\max}$. The identities use $2\log\frac{w(s_0)}{w(s_0-j)}=j\log D-\sum_{i=s_0-j+1}^{s_0}\tau_i$ and $2\log\frac{w(s_0)}{w(s_0+m)}=\sum_{i=s_0+1}^{s_0+m}\tau_i-m\log D$ (proof of Proposition 2.3 and (2.2)). Note that
$$\Delta^{\rm iv}_T\le0\iff\frac{w(s_0+m)\,m(S_0\cup T)}{w(s_0)\,m(S_0)}\ge1, \tag{5.4}$$
because $\frac{m(S_0\cup T)}{m(S_0)}=D^{-m/2}\big(\frac{A}{A-hU_T}\big)^\nu$ by (2.1) of the draft and P4(i).

**Proposition 5.1 (decomposition, integrated variance).** For $S\ne S_0$ with $|S|\le k_{\max}$, $J=S_0\setminus S$, $T=S\setminus S_0$:
$$2\big[\mathrm{sc}(S_0)-\mathrm{sc}(S)\big]\ \ge\ \Gamma^{\rm iv}_J\mathbf 1\{J\ne\emptyset\}+\Delta^{\rm iv}_T\mathbf 1\{T\ne\emptyset\}.$$
Hence $\HPM=S_0$ on $\mathcal A^{\rm iv}\cap\mathcal B^{\rm iv}$, where $\mathcal A^{\rm iv}:=\{\Gamma^{\rm iv}_J>0\ \forall\emptyset\ne J\subseteq S_0\}$ and $\mathcal B^{\rm iv}:=\{\Delta^{\rm iv}_T>0\ \forall\emptyset\ne T\subseteq S_0^c\}$.

*Proof.* If $T=\emptyset$ the claim is (5.2); if $J=\emptyset$ it is (5.3) with $s_0+m=|S|\le k_{\max}$. Otherwise write $2[\mathrm{sc}(S_0)-\mathrm{sc}(S)]=2[\mathrm{sc}(S_0)-\mathrm{sc}(S_0\cup T)]+2[\mathrm{sc}(S_0\cup T)-\mathrm{sc}((S_0\cup T)\setminus J)]$, where $\mathrm{sc}$ is evaluated by its formula whether or not $s_0+m\le k_{\max}$ (the formula is defined for every $S\subseteq[p]$; only the HPM's argmax is restricted to the cap). The first bracket is $\Delta^{\rm iv}_T$. For the second, put $k=s_0+m$ and $A'=A-hU_T=2b_0+Q_{S_0\cup T}$, so that $A_{(S_0\cup T)\setminus J}=A'+hU_J$ (Lemma 1.1(c)). From the definition of $\mathrm{sc}$,
$$2\big[\mathrm{sc}(S_0\cup T)-\mathrm{sc}((S_0\cup T)\setminus J)\big]=2\log\frac{w(k)}{w(k-j)}-j\log D+2\nu\log\frac{A'+hU_J}{A'}$$
(the smaller model has $j$ fewer variables, hence a smaller determinant penalty, which is the $-j\log D$). With $2\log\frac{w(k)}{w(k-j)}=j\log D-\sum_{i=k-j+1}^k\tau_i$ the two $j\log D$ cancel, leaving
$$2\nu\log\Big(1+\frac{hU_J}{A'}\Big)-\sum_{i=k-j+1}^{k}\tau_i\ \ge\ 2\nu\log\Big(1+\frac{hU_J}{A}\Big)-\sum_{i=s_0-j+1}^{s_0}\tau_i=\Gamma^{\rm iv}_J,$$
because $x\mapsto\log(1+hU_J/x)$ is decreasing on $(0,\infty)$ with $0<A'\le A$, and $\sum_{i=k-j+1}^k\tau_i\le\sum_{i=s_0-j+1}^{s_0}\tau_i$ ($\tau_i$ decreasing, $k\ge s_0$). The deletion identity (5.2) is the same computation with $k=s_0$, $A'=A$. $\square$

### 5.2 Upper bound (the $\to0$ direction)

**Theorem 5.2.** For every $\delta\in(0,1)$, with $\gamma_n^-:=\dfrac{(1-\delta)(n-s_0)}{(2a_0+n)\,h}$,
$$\Prob_0(\HPM=S_0)\ \le\ \psi\big(\lambda,\gamma_n^-\tau_{s_0}\big)^{s_0}+e^{-(n-s_0)\delta^2/4}.$$

*Proof.* If $\HPM=S_0$ then $\Gamma^{\rm iv}_{\{j\}}>0$ for every $j\in S_0$ (the model $S_0\setminus\{j\}$ is a competitor), i.e. $2\nu\log(1+hu_j/A)>\tau_{s_0}$. Since $\log(1+x)\le x$, this gives $hu_j/A>\tau_{s_0}/(2\nu)$, and by (5.1), $hu_j>\tau_{s_0}A/(2a_0+n)\ge\tau_{s_0}\sigma_\star^2R'/(2a_0+n)$. On the event $\{R'\ge(n-s_0)(1-\delta)\}$ this yields $hu_j/\sigma_\star^2>\gamma_n^-h\,\tau_{s_0}$, i.e. $(\sqrt\lambda+\zeta_j)^2>\gamma_n^-\tau_{s_0}$, for every $j\in S_0$. Therefore
$$\Prob_0(\HPM=S_0)\le\Prob\big(R'<(n-s_0)(1-\delta)\big)+\Prob\big((\sqrt\lambda+\zeta_j)^2>\gamma_n^-\tau_{s_0}\ \forall j\in S_0\big)=\Prob(R'<(n-s_0)(1-\delta))+\psi(\lambda,\gamma_n^-\tau_{s_0})^{s_0},$$
by Lemma 1.1(a),(b) and Lemma 1.2(a); the first term is at most $e^{-(n-s_0)\delta^2/4}$ by Lemma 1.3(b). $\square$

### 5.3 Lower bound (the $\to1$ direction)

The deletion part is self-contained; the superset part is cited from the T7 proof.

**Lemma 5.3 (deletions).** Let $\delta>0$ and
$$\bar A_n:=\frac{2b_0}{\sigma_\star^2}+(n-s_0)(1+\delta)+\frac{4s_0\lambda}{n},\qquad \gamma_n^+:=\frac{\bar A_n}{(2a_0+n)\,h}\,\exp\Big\{\frac{s_0\tau_1}{2a_0+n}\Big\}.$$
Then
$$\Prob\big((\mathcal A^{\rm iv})^c\big)\ \le\ s_0\,\Phi\big(\sqrt{\gamma_n^+\tau_1}-\sqrt\lambda\big)+e^{-(n-s_0)\delta^2/(4(1+\delta))}+s_0e^{-\lambda/2}.$$

*Proof.* Let $G_R:=\{R'\le(n-s_0)(1+\delta)\}$ and $H:=\{\max_{j\in S_0}|\zeta_j|\le\sqrt\lambda\}$. By Lemma 1.3(c), $\Prob(G_R^c)\le e^{-(n-s_0)\delta^2/(4(1+\delta))}$; by Lemma 1.3(d) and a union bound, $\Prob(H^c)\le2s_0\bar\Phi(\sqrt\lambda)\le s_0e^{-\lambda/2}$. On $H$, $u_j/\sigma_\star^2=(\sqrt\lambda+\zeta_j)^2\le4\lambda$ for $j\in S_0$, so $(1-h)U_{S_0}\le\frac1n\cdot4s_0\lambda\sigma_\star^2$ (as $1-h\le\frac1n$); hence on $G_R\cap H$, by (5.1), $A\le\sigma_\star^2\bar A_n$.

Now fix $J\subseteq S_0$, $|J|=j\ge1$. Since $\sum_{i=s_0-j+1}^{s_0}\tau_i\le j\tau_1$ by (1.3), $\Gamma^{\rm iv}_J>0$ as soon as $2\nu\log(1+hU_J/A)>j\tau_1$. Put $g:=h\min_{i\in S_0}u_i/A$, so $hU_J/A\ge jg$; it suffices that $\log(1+jg)>j\tau_1/(2\nu)$, i.e. $g>(e^{j\tau_1/(2\nu)}-1)/j$. The function $j\mapsto(e^{jx}-1)/j$ ($x>0$) is increasing (the chord slope of the convex function $e^{jx}-1$ from $j=0$), so the condition for all $1\le j\le s_0$ follows from $g>\kappa_n:=(e^{s_0\tau_1/(2\nu)}-1)/s_0$. On $G_R\cap H$, $g\ge h\min_{S_0}u_i/(\sigma_\star^2\bar A_n)$, so
$$\mathcal A^{\rm iv}\ \supseteq\ G_R\cap H\cap\Big\{\min_{i\in S_0}\frac{u_i}{\sigma_\star^2}>t_n\Big\},\qquad t_n:=\frac{\kappa_n\bar A_n}{h}.$$
Finally, with $x=s_0\tau_1/(2\nu)$, $\kappa_n=\frac{\tau_1}{2\nu}\cdot\frac{e^x-1}{x}\le\frac{\tau_1}{2\nu}e^x$, so $t_n\le\gamma_n^+\tau_1$, and by Lemma 1.2(b),(d) and independence (Lemma 1.1(a)), $\Prob(\min_{S_0}u_i/\sigma_\star^2\le t_n)=1-\psi(\lambda,t_n)^{s_0}\le s_0(1-\psi(\lambda,\gamma_n^+\tau_1))\le s_0\Phi(\sqrt{\gamma_n^+\tau_1}-\sqrt\lambda)$. The union bound over the three events finishes the proof. $\square$

**Lemma 5.4 (supersets; cited from proofs/T7_T8/PROOF.md).** Let $n\to\infty$ with $s_0$ fixed, $p=p_n\le n$, $X^\top X=nI_p$, and $s_0\beta_n^2\le M$ for a fixed $M$. Then
$$\Xi_n:=\sum_{\emptyset\ne T\subseteq S_0^c}\frac{w(s_0+|T|)\,m(S_0\cup T)}{w(s_0)\,m(S_0)}\ \longrightarrow\ 0\quad\text{in }\Prob_0\text{-probability},$$
and consequently $\Prob((\mathcal B^{\rm iv})^c)\le\Prob_0(\Xi_n\ge1)\to0$.

*Justification.* The cited material is quoted verbatim in CITED_RESULTS.md, Internal section (I1–I7). Their standing assumptions (A1)–(A4) hold here: (A1) with their exponent $A_{\rm T7}=1$ since $p\le n$; (A2) with the cap read as $k_{\max}=p$, i.e. no cap, which (A2) allows (the quantity $\Xi_n$ does not involve the cap: it is a sum of formal ratios $w(|S|)m(S)/(w(s_0)m(S_0))$ over all supersets); (A3) since $\|\mu\|^2=n\|\beta^\star\|^2=ns_0\beta_n^2\le nM$; (A4) and the sparse eigenvalue condition (SE), for every model size, with $\varphi_0=1$, since $\Gamma_S=I$ for every $S$. Take $\omega_n=\frac12\log n$ and the corresponding $m_n$ of their §0.1. Then: (i) their Proposition 4.2(c) (I6) states that $\sum_{j=1}^{m_n}\Xi_j\to0$ in $\Prob_0$-probability (and $\sum_{j\le m_n}\Xi_j\mathbf 1_{\mathcal G_n}=O_{\Prob}(\sqrt{\log n/n})$ on their good event $\mathcal G_n$, with $\Prob_0(\mathcal G_n^c)\le5/n$ by their Lemma 2.2, I8a), where $\Xi_j$ (their (4.1), I5) is the sum of the ratios over the supersets $S_0\cup T$ with $|T|=j$ (and $\Xi_j=0$ if $s_0+j>p$); this covers every $T$ with $|T|\le m_n$. (ii) Their Lemma 3.1 (I4), through the display (3.1) in its proof ($\Pi(|S|>m\mid y)\le N_n/(p(S_0)m(S_0)/f_0(y))$ with $N_n=\sum_{|S|>m}p(S)m(S)/f_0(y)$, so that the right-hand side is exactly $\sum_{|S|>m}p(S)m(S)/(p(S_0)m(S_0))$) and the "Conclusion" paragraph of that proof (I8b), which bounds this right-hand side by $2^{-m}(2p)^{s_0}(n+1)^{s_0/2}\sqrt n\,\Theta_n^{(m)}$ with $\Theta_n^{(m)}$ tight, gives, with the uncapped prior ($p(S)/p(S_0)=w(|S|)/w(s_0)$ for every $S$, as $W=1$ for the untruncated $\BB(1,p)$ prior) and $m=m_n$, $\sum_{|S|>m_n}\frac{w(|S|)m(S)}{w(s_0)m(S_0)}=O_{\Prob}(e^{-\omega_n})=O_{\Prob}(n^{-1/2})$; this covers every $T$ with $|T|>m_n$ (then $|S_0\cup T|>m_n$), since all terms are nonnegative. Together, $\Xi_n\to0$ in probability (with $\Xi_n=O_{\Prob}(\sqrt{\log n/n})$, using Lemma 2.2 to remove the indicator in (i)). By (5.4), $(\mathcal B^{\rm iv})^c\subseteq\{\Xi_n\ge1\}$. $\square$

(Lemma 5.4 is the only place where this proof depends on another thread's proof. The dependence is on Proposition 4.2(c), Lemma 2.2, and the proof of Lemma 3.1 (display (3.1), the "Numerator" paragraph, (3.3) and the "Conclusion" paragraph) of proofs/T7_T8/PROOF.md, all provisional and not adopted; their hypotheses are verified above. The constants in those results depend on $(s_0,A_{\rm T7},\varphi_0,\sigma_\star^2,M,a_0,b_0)$, all fixed here.)

**Theorem 5.5 (lower bound, integrated variance).** For every $\delta>0$,
$$\Prob_0(\HPM\ne S_0)\ \le\ s_0\,\Phi\big(\sqrt{\gamma_n^+\tau_1}-\sqrt\lambda\big)+e^{-(n-s_0)\delta^2/(4(1+\delta))}+s_0e^{-\lambda/2}+\Prob_0(\Xi_n\ge1),$$
with $\gamma_n^+$ of Lemma 5.3 and $\Xi_n$ of Lemma 5.4. Under the hypotheses of Lemma 5.4 the last term tends to $0$.

*Proof.* Proposition 5.1, then Lemmas 5.3 and 5.4 with a union bound. $\square$

### 5.4 The sharp threshold with integrated variance

**Corollary 5.6.** Let $n\to\infty$, $s_0\ge1$ fixed, $s_0<p_n\le n$, any caps $k_{\max,n}\ge s_0$, $a_0,b_0>0$ fixed, and assume the bounded-signal condition $\beta_n^2\le B\sigma_\star^2$ for a fixed $B$ (equivalently $\lambda_n\le Bn$). With $\tau_n$ and $c_n=\sqrt{\lambda_n}-\sqrt{\tau_n}$ as in Corollary 2.6, the conclusions (i)–(iii) of Corollary 2.6 and their converses hold verbatim for the integrated-variance HPM: $\Prob_0(\HPM=S_0)\to1$ iff $c_n\to+\infty$, $\to0$ iff $c_n\to-\infty$, and $\to\Phi(c)^{s_0}$ if $c_n\to c$.

*Proof.* Take $\delta=\delta_n:=2\sqrt{\log n/(n-s_0)}$ in Theorems 5.2 and 5.5. Then $e^{-(n-s_0)\delta_n^2/4}=n^{-1}$ and $e^{-(n-s_0)\delta_n^2/(4(1+\delta_n))}=n^{-1/(1+\delta_n)}\to0$. Next, $\gamma_n^\pm\to1$: $\gamma_n^-=(1-\delta_n)\frac{n-s_0}{(2a_0+n)h}$ and $\frac{n-s_0}{(2a_0+n)h}=1+O(n^{-1})$; $\gamma_n^+=\frac{2b_0/\sigma_\star^2+(n-s_0)(1+\delta_n)+4s_0\lambda_n/n}{(2a_0+n)h}e^{s_0\tau_1/(2a_0+n)}$, where $4s_0\lambda_n/n\le4s_0B$ and $s_0\tau_1/(2a_0+n)=O(\log n/n)$ (as $\tau_1\le\log(n+1)+2\log(2n)$), so $\gamma_n^+=(1+\delta_n)(1+O(n^{-1}))(1+O(\log n/n))$. Hence $|\gamma_n^\pm-1|=O(\sqrt{\log n/n})$, and for $\tau'\in\{\tau_{s_0},\tau_1\}$,
$$\big|\gamma_n^\pm\tau'-\tau_n\big|\le|\gamma_n^\pm-1|\,\tau'+|\tau'-\tau_n|=O\Big(\log n\sqrt{\tfrac{\log n}n}\Big)+2\log(2s_0),$$
so $\sqrt{\gamma_n^\pm\tau'}-\sqrt{\tau_n}=O\big((\log n)^{3/2}n^{-1/2}+\log(2s_0)\big)/\sqrt{\tau_n}\to0$ (using $|\sqrt a-\sqrt b|\le|a-b|/\sqrt b$ and $\tau_n\ge\log n$). Therefore $\sqrt{\lambda_n}-\sqrt{\gamma_n^\pm\tau'}\to c$ (resp. $\pm\infty$) whenever $c_n$ does.

(i) If $c_n\to+\infty$: $\lambda_n\to\infty$, so $s_0e^{-\lambda_n/2}\to0$, $\Phi(\sqrt{\gamma_n^+\tau_1}-\sqrt{\lambda_n})\to0$, and $\Prob_0(\Xi_n\ge1)\to0$ by Lemma 5.4 (its hypothesis $s_0\beta_n^2\le s_0B\sigma_\star^2=:M$ holds); Theorem 5.5 gives $\Prob_0(\HPM\ne S_0)\to0$.
(ii) If $c_n\to-\infty$: Theorem 5.2 gives $\Prob_0(\HPM=S_0)\le\psi(\lambda_n,\gamma_n^-\tau_{s_0})^{s_0}+n^{-1}\to0$, since $\psi(\lambda_n,t)\le\Phi(\sqrt{\lambda_n}-\sqrt t)+\Phi(-\sqrt t)$ (Lemma 1.2(c)) with $t=\gamma_n^-\tau_{s_0}\to\infty$.
(iii) If $c_n\to c$: the upper bound of Theorem 5.2 tends to $\Phi(c)^{s_0}$ as in Corollary 2.6(4). For the lower bound, the proof of Lemma 5.3 gives $\Prob(\mathcal A^{\rm iv})\ge\psi(\lambda_n,\gamma_n^+\tau_1)^{s_0}-\Prob(G_R^c)-\Prob(H^c)$, so by Proposition 5.1 and Lemma 5.4, $\Prob_0(\HPM=S_0)\ge\psi(\lambda_n,\gamma_n^+\tau_1)^{s_0}-o(1)\to\Phi(c)^{s_0}$ (again $\lambda_n\to\infty$ here).
The converses follow by the subsequence argument of Corollary 2.6, using the two bounds: along a subsequence with $c_n\le c'$ the upper bound has $\limsup\le\Phi(c')^{s_0}<1$; along one with $c_n\ge-c'$ (so $\lambda_n\to\infty$) the lower bound has $\liminf\ge\Phi(-c')^{s_0}>0$. $\square$

### 5.5 What changes with integrated variance, exactly

- *Unchanged:* the centre $\tau_n=\log D+2\log\frac{2p-s_0}{s_0}$ of the transition, its $\sqrt{\tau_n}$-wide window, the limit $\Phi(c)^{s_0}$, hence the gap to the minimax threshold of Theorem 3.3 and the verdict of Section 3.3. In particular the gap is *not* the price of estimating $\sigma_\star^2$: the integrated-variance HPM, which knows neither $s_0$ nor $\sigma_\star^2$, pays exactly what the known-variance HPM pays, up to a factor $\gamma_n^\pm=1+O(\sqrt{\log n/n})$ on the threshold.
- *The thresholds:* the exact known-variance penalties $\tau_{s_0}/h$ and $\tau_1/h$ become $\gamma_n^-\tau_{s_0}$ and $\gamma_n^+\tau_1$. The factor $\gamma_n^\pm$ collects (a) the residual-variance estimate $A/(2\nu)=(2b_0+Q_{S_0})/(2a_0+n)$, which replaces $\sigma_\star^2$ and fluctuates by $O_{\Prob}(n^{-1/2})$, (b) the shrinkage leakage $(1-h)U_{S_0}$ of the fitted signal into $Q_{S_0}$ (Lemma 1.1(c)), which enters $\gamma_n^+$ as the term $4s_0\lambda/n$ relative to $n$, i.e. of order $\lambda/n^2$, and (c) the curvature of $\log(1+x)$ versus $x$, of order $\tau_1/n$. On the $\lambda$-scale the shift is $O((\log n)^{3/2}n^{-1/2})\to0$, far inside the window of width $\asymp\sqrt{\log n}$.
- *Lost:* the coordinate-wise independence of the known-variance scores. The common denominator $A$ couples all coordinates, so (a) the product form $\psi^{s_0}\times(\text{superset factor})$ of (2.1), (b) the exact order-statistic characterisation of Proposition 2.1 in its coordinate-additive form (P4(ii) still gives $\HPM=$ top-$\hat k$, but $f(k)$ becomes $2\log w(k)-k\log D-2\nu\log(2b_0+\|y\|^2-hU_{(k)})$, whose increments $f(k)-f(k-1)$ depend on all of $u_{(1)},\dots,u_{(k)}$ rather than on $u_{(k)}$ alone), and (c) the explicit superset bound $E_n$ of Proposition 2.4. The superset event is controlled only in probability, by Lemma 5.4: the cited results give $\Xi_n=O_{\Prob}(\sqrt{\log n/n})$, hence $\Prob((\mathcal B^{\rm iv})^c)\le\Prob(\Xi_n\ge1)\to0$, but no rate for this probability (an $O_{\Prob}$ statement is a tightness statement; it gives no bound on $\Prob(\Xi_n\ge1)$ beyond $o(1)$).
- *Added hypothesis:* bounded signal, $\beta_n^2\le B\sigma_\star^2$ (T7's (A3) in the orthogonal model), used in Lemma 5.4 and to keep $\gamma_n^+\to1$ (the term $4s_0\lambda/n^2$). It is harmless at the threshold, where $\lambda_n\asymp\log n$. The constants $\sigma_\star^2$, $a_0$, $b_0$ are fixed throughout (Section 1.1).
- *Extra error terms:* $n^{-1}$ (Theorem 5.2), $n^{-1/(1+\delta_n)}$, $s_0e^{-\lambda/2}$ and $\Prob_0(\Xi_n\ge1)$ (Theorem 5.5), in place of the single term $E_n$.
- *Relation to T8 and T7.* T8(ii) gives $\Prob_0(\HPM\ne S_0)\to0$ under the beta-min condition $\lambda_n\ge M_n^\beta\log n/\varphi_0^2$ with $M_n^\beta\to\infty$ (here $\varphi_0=1$). Corollary 5.6 sharpens this conclusion (and only this one: T8(i), the expectation in T8(ii) and the rate in T8(iii) are not addressed) in the orthogonal model with equal signal magnitudes: $\sqrt{\lambda_n}-\sqrt{\tau_n}\to\infty$ suffices, and $\tau_n\le\log n+2\log(2n)+O(1)$, so a beta-min condition with a *constant* $M^\beta$ suffices provided $M^\beta>3$ (for $p\le n$), or $M^\beta>1+2\vartheta$ when $p_n=n^{\vartheta}$ (then, since $\tau_n=(1+2\vartheta)\log n+O(1)$, $\lambda_n\ge M^\beta\log n\ge(1+\epsilon)\tau_n$ eventually for any $0<\epsilon<\frac{M^\beta}{1+2\vartheta}-1$, and Corollary 2.6/5.6 applies; a sequence $M_n^\beta\downarrow1+2\vartheta$ is not covered, e.g. $M_n^\beta=3+1/\log n$ at $p_n=n$ gives $c_n\to0$ and the limit $2^{-s_0}$). Conversely, by Corollary 5.6(ii), $\Prob_0(\HPM\ne S_0)\not\to0$ when $\lambda_n\le(1-\epsilon)(1+2\vartheta)\log n$, so T8's $\log n$ scale is sharp and its constant cannot go below $1+2\vartheta$ in general. The known-variance superset floor of Remark 2.7 (order $n^{-1/2}(\log n)^{-1/2}$ for the probability that some superset beats $S_0$, a lower bound on $\Prob_0(\HPM\ne S_0)$ when $s_0<k_{\max}$; not proved for integrated variance) is consistent with T7's rate $O_{\Prob}(\sqrt{\log n/n})$ for the superset *posterior mass*, which is a different object (Remark 4.4 of the T7 proof discusses its order in the orthogonal case).

---

## 6. Flags for the draft

- **(F1) Pb1 status.** Pb1 can be upgraded from Open to Proved (supplementary) in the following form. *Known variance:* Theorem 2.5 and Corollary 2.6 (sharp threshold $\tau_n=\log D+2\log\frac{2p-s_0}{s_0}$, limit $\Phi(c)^{s_0}$ when $\sqrt{\lambda_n}-\sqrt{\tau_n}\to c$; nonasymptotic sandwich (2.5)); Proposition 2.4 and Remark 2.7 (the superset floor $\asymp n^{-1/2}(\log n)^{-1/2}$ on $\Prob_0(\HPM\ne S_0)$, for every $\lambda$, when $s_0<k_{\max}$). *Integrated variance:* Corollary 5.6, same threshold and limit, under $\beta_n^2\le B\sigma_\star^2$, with the superset part resting on T7's Proposition 4.2 and Lemma 3.1 (provisional).
- **(F2) The heuristic.** Replace "about $\log n+2\log2$; this is unverified" by: for $p_n-s_0\to\infty$ the HPM's threshold exceeds the minimax one by $\log n+O(1)$ on the $\lambda$-scale (Theorem 3.3; the $\log n$ is sharp, the gap being $\asymp\sqrt{\log n}$ on the $\sqrt\lambda$-scale where the windows are $O(1)$ wide); at the level of the leading-order centres the constant is $2\log2-2\log s_0$ for the penalty $\tau_{s_0}$ and $2\log2$ for the penalty $\tau_1$ (hence $2\log2$ for $s_0=1$); the finite-$n$ constant is not determined by the limit theorems, which are invariant under $o(\sqrt{\tau_n})$ and $o(\sqrt{\log(p_n-s_0)})$ recentring respectively. The window widths are $\asymp\sqrt{\tau_n}\asymp\sqrt{\log n}$ for the HPM and $\asymp\sqrt{\log(p_n-s_0)}$ for the minimax threshold.
- **(F3) The minimax threshold.** For fixed $s_0$ the literature found (Butucea et al. 2018) gives the sufficiency side and separable-selector lower bounds, but no all-selector lower bound on the probability of wrong recovery; Theorem 3.1 provides one (Bayes argument, top-$s_0$ oracle), with centre $2\log(p-s_0)$ and the same window shape $\Phi(c)^{s_0}$. The draft should cite Butucea et al. for the sequence-model phase transition and state the fixed-$s_0$ lower bound as proved here.
- **(F4) P3.** In the orthogonal model $\Prob_0(\mathcal W)=1-\rho_n^{|\cdot|}(\lambda)$ (Theorem 3.1(b)), so P3's ceiling is the absolute oracle's success probability, centred at $2\log(p-s_0)$ when $p_n-s_0\to\infty$; $\BB(1,p)$ with $g=n$ sits at $\tau_n$, i.e. $\log n+O(1)$ above the ceiling's leading-order centre (Theorem 3.3(a)). This quantifies the ceiling.
- **(F5) T8.** For the conclusion $\Prob_0(\HPM\ne S_0)\to0$ of T8(ii), in the orthogonal model with equal signal magnitudes and $p_n=n^{\vartheta}$: the beta-min constant cannot go below $1+2\vartheta$ (Section 5.5), and any constant $M^\beta>1+2\vartheta$ suffices for that conclusion in place of $M_n^\beta\to\infty$. Nothing is claimed here about T8(i), the expectation in T8(ii), or the rate in T8(iii) (whose proof uses $M_n^\beta\to\infty$ in an essential way). The note after T8 could say that the $\log n$ scale of the beta-min condition is sharp for HPM consistency (Pb1).
- **(F6) P4(iii).** The approximation "$\approx\log n+2\log\frac{2p-k-1}{k+1}$" is exact with $\log D$ in place of $\log n$, $\log D-\log n\in[0,n^{-2}]$; harmless.
- **(F7) Remark 2.8** (misspecified known variance: $c_\sigma=\sigma^2/\sigma_\star^2<\frac23$ at $p\asymp n$ makes $\Prob_0(\HPM=S_0)\to0$ whatever the signal, when $s_0<k_{\max}$) is a supplementary observation, not needed by the paper.
