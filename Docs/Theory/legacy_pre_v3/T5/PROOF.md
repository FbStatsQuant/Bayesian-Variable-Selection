# Proof of Theorem T5 (Mode loss: the particles are the risk)

Supplement material for *Split-and-merge with an exact merge: composite-start sequential Monte Carlo for Bayesian variable selection*, draft of 14 October 2026. Notation follows Section 2 of the draft. Results assumed: Proposition P6 (kernel correctness; it guarantees that the implemented kernels satisfy the invariance hypothesis of T5 and is not otherwise used), Proposition P7 (frozen-schedule unbiasedness), and the standard unbiasedness of the SMC evidence estimate under unbiased resampling, which is re-proved below in the generality in which it is used (Lemma 3). No other numbered result is used.

**Summary of the outcome.** Parts (i)–(v) of T5 are true as stated, once the particle system is modelled in the standard way (Section 0 below spells this out; the two structural hypotheses (H1) and (H2) are the ones every SMC unbiasedness proof uses; the current draft states both, and (H1) is now in the generality the draft allows, resampling rules that look at particle values included). The coupling in (ii) is an identity between two laws on the same trajectory space, which is finite (Proposition 2); a pathwise coupling follows at once (Remark 2.3). Under an adaptive schedule (part (vi)), parts (i), (ii) and (iv) survive verbatim; part (v) survives with $\sum_tm_t$ replaced by its expectation (or by a deterministic upper bound), and **not** verbatim, since the move counts are then random (audit 2026-10-15); part (iii) survives as a conditional-law statement. The unconditional identity $\mathbb E[\widehat Z]=Z$ and the explicit factor in (iii) do not survive in general: Example 6.4, which satisfies every hypothesis of the adaptive theorem, shows this (Section 6.3; the original two-state Example 6.3 lies outside the non-crossing class). All probabilities in this file are over the algorithm's randomness, with the data (hence $\gamma_0$, $d$ and $\mathcal M$) fixed (audit 2026-10-15).

---

## 0. The setting made precise

### 0.1 The targets

Let $\mathcal S$ be a finite set and $\gamma_0:\mathcal S\to(0,\infty)$, $d:\mathcal S\to\mathbb R$ two functions. For $\phi\in\mathbb R$ put
$$
\gamma_\phi(S)=\gamma_0(S)\,e^{\phi d(S)},\qquad \bar Z_\phi(A)=\sum_{S\in A}\gamma_\phi(S)\quad(A\subseteq\mathcal S),\qquad \bar Z_\phi=\bar Z_\phi(\mathcal S),\qquad q_\phi=\gamma_\phi/\bar Z_\phi .
$$
Then $q_\phi(S)>0$ for every $S\in\mathcal S$ and every $\phi$, and $q_\phi(A)=\bar Z_\phi(A)/\bar Z_\phi$.

In the paper, $\mathcal S=\{S\subseteq[p]:|S|\le k_{\max}\}$ is the support of the model prior, $\gamma_0(S)=p(S)r(S)>0$ on $\mathcal S$, $d$ is the discrepancy of Section 2.2, $q_0=\pi_0$, $q_1=\pi$ and $Z=m(\emptyset)\bar Z_1$. Every kernel of P6 lives on $\mathcal S$ (proposals beyond the cap are rejected). Nothing below uses the specific form of $\gamma_0$ or $d$.

Fix $\mathcal M\subseteq\mathcal S$ with $0<q_0(\mathcal M)<1$, so that $\mathcal M$ and $\mathcal M^c:=\mathcal S\setminus\mathcal M$ are both nonempty, and write
$$
\tilde q_\phi:=q_\phi(\,\cdot\mid\mathcal M^c)=\frac{\gamma_\phi\mathbf 1_{\mathcal M^c}}{\bar Z_\phi(\mathcal M^c)},\qquad
\rho:=\frac{1-q_1(\mathcal M)}{1-q_0(\mathcal M)}=\frac{\bar Z_1(\mathcal M^c)}{\bar Z_1}\cdot\frac{\bar Z_0}{\bar Z_0(\mathcal M^c)} .
$$

### 0.2 The particle system with a frozen schedule

Fix $N\ge1$, a schedule $0=\phi_0<\phi_1<\dots<\phi_T=1$, integers $m_t\ge0$, and for each stage $t$ and each $\ell\in\{1,\dots,m_t\}$ a Markov kernel $K_{t,\ell}$ on $\mathcal S$. (The theorem speaks of "$m_t$ applications of kernels $K_t$"; allowing the $m_t$ kernels of a stage to differ costs nothing and covers a systematic sweep of single-site updates followed by swap moves. The case $K_{t,\ell}=K_t$ for all $\ell$ is the statement's.) Write $\mathcal K_t=K_{t,1}K_{t,2}\cdots K_{t,m_t}$ for the composition, with $\mathcal K_t=I$ if $m_t=0$. The stage-$t$ potential is
$$
G_t(S)=\frac{\gamma_{\phi_t}(S)}{\gamma_{\phi_{t-1}}(S)}=\exp\{(\phi_t-\phi_{t-1})\,d(S)\},\qquad S\in\mathcal S,
$$
so that $w_t^i=G_t(S^i)$ in the notation of Section 2.3.

Two structural hypotheses, implicit in Section 2.3 and in P7, are made explicit.

**(H1) Resampling with conditionally unbiased offspring counts** (generalised, audit 2026-10-15). For each stage $t$ there is a Markov kernel $R_t$ from histories to the set $[N]^N$ of ancestor vectors $a=(a^1,\dots,a^N)$: given the history $h_{t-1}=(X_0,(A_s,Y_{s,\cdot})_{s<t})$, whose last population is $x=X_{t-1}$ with normalised weights $W_t(x)=\big(G_t(x^i)/\sum_kG_t(x^k)\big)_{i\le N}$, the ancestor vector $A_t$ is drawn from $R_t(h_{t-1},\cdot)$ and the resampled population is $\hat x^j=x^{A_t^j}$. Unbiasedness means: for every history $h$ (with last population $x$) and every $i\le N$,
$$
\sum_a R_t(h,a)\,\#\{j:a^j=i\}=NW_t^i(x) .
$$
The restricted run of Section 0.3 uses the *same* kernels $R_t$ (on histories that stay in $\mathcal M^c$). The draft's rule, which depends on the current population "only through the particles' values and weights" and is drawn afresh, is the case $R_t(h,\cdot)=R_t(x,\cdot)$; a rule that sees only the weight vector, $R_t(h,\cdot)=R_N(W_t(x),\cdot)$, is the case treated in the pre-audit version. Multinomial, residual, stratified and systematic resampling, in a fixed index order or after sorting the particles by any function of the population, are all of this form (any auxiliary uniform used by the scheme is integrated out in $R_t$; the identity for each scheme is Lemma 5.4 of `proofs/foundations/PROOF.md`). The identity must hold for every history, not only on average over histories with the same current population or weight vector (`proofs/foundations/PROOF.md`, Propositions 5.13 and 5.14).

**(H2) Mutations are conditionally independent across particles.** Given the resampled population $\hat x$, the $N$ particles are moved independently, particle $j$ through $K_{t,1}$, then $K_{t,2}$, …, then $K_{t,m_t}$.

The trajectory of the system is
$$
\omega=\big(X_0,\ (A_t,\,Y_{t,1},\dots,Y_{t,m_t})_{t=1}^T\big),\qquad X_0,\,Y_{t,\ell}\in\mathcal S^N,\quad A_t\in[N]^N,
$$
where $X_0$ is the initial population, $Y_{t,0}:=\hat X_t:=(X_{t-1}^{A_t^j})_{j\le N}$ is the resampled population, $Y_{t,\ell}$ is the population after the $\ell$-th move of stage $t$, and $X_t:=Y_{t,m_t}$ is the population at the end of stage $t$. The trajectory space $\Omega=\mathcal S^N\times\prod_{t=1}^T\big([N]^N\times(\mathcal S^N)^{m_t}\big)$ is finite. The law of the system is the probability $P$ on $\Omega$ given by
$$
P(\omega)=\prod_{j=1}^Nq_0(X_0^j)\ \prod_{t=1}^T\Big[R_t\big(h_{t-1}(\omega),A_t\big)\prod_{\ell=1}^{m_t}\prod_{j=1}^NK_{t,\ell}\big(Y_{t,\ell-1}^j,Y_{t,\ell}^j\big)\Big]. \tag{0.1}
$$
(audit 2026-10-15: the resampling factor was $R_N(W_t(X_{t-1}),A_t)$; $h_{t-1}(\omega)$ is the prefix of $\omega$ up to $X_{t-1}$.)
This is exactly the algorithm of Section 2.3 under (H1)–(H2): initial particles i.i.d. from $q_0$; at each stage, weights, resampling, $m_t$ moves. The reported evidence estimate is the function
$$
\widehat Z(\omega)=m(\emptyset)\,\bar Z_0\,\Pi_T(\omega),\qquad \Pi_t(\omega):=\prod_{s=1}^t\Big(\frac1N\sum_{i=1}^NG_s(X_{s-1}^i)\Big),\quad\Pi_0:=1 . \tag{0.2}
$$
A *function of the particle system* is any function on $\Omega$: the empirical ESS at each stage, $\Pi_T$, the visited set, the particle PIPs, the HPM over the visited set, and so on.

The event of the theorem is
$$
E=\{\omega:\ X_0^j\in\mathcal M^c\ \text{for all } j\le N\}.
$$

**Hypotheses of T5 on the kernels.** Each $K_{t,\ell}$ is $q_{\phi_t}$-invariant, $q_{\phi_t}K_{t,\ell}=q_{\phi_t}$, and non-crossing, $K_{t,\ell}(S,\mathcal M)=0$ for all $S\in\mathcal M^c$.

### 0.3 The restricted run

The restricted run is the same algorithm applied to the finite set $\mathcal M^c$, the unnormalised targets $\tilde\gamma_\phi:=\gamma_\phi\mathbf 1_{\mathcal M^c}$ (so the normalised targets are $\tilde q_\phi$ and the normalising constants are $\bar Z_\phi(\mathcal M^c)$), the same schedule, the same potentials $G_t$ (which satisfy $G_t=\tilde\gamma_{\phi_t}/\tilde\gamma_{\phi_{t-1}}$ on $\mathcal M^c$), the same resampling kernels $R_t$, and the restricted kernels
$$
\tilde K_{t,\ell}(S,S'):=K_{t,\ell}(S,S'),\qquad S,S'\in\mathcal M^c .
$$
Lemma 1 below shows that $\tilde K_{t,\ell}$ is a Markov kernel on $\mathcal M^c$ and is $\tilde q_{\phi_t}$-invariant, so the restricted run is a legitimate SMC algorithm for the bridge $\tilde q_0\to\tilde q_1$. Its trajectory space is $\tilde\Omega=(\mathcal M^c)^N\times\prod_t\big([N]^N\times((\mathcal M^c)^N)^{m_t}\big)\subseteq\Omega$, its law $\tilde P$ is given by (0.1) with $q_0$ replaced by $\tilde q_0$ and $K_{t,\ell}$ by $\tilde K_{t,\ell}$, extended by $0$ to $\Omega\setminus\tilde\Omega$, and its evidence estimate is
$$
\widehat Z^{\rm res}(\omega)=m(\emptyset)\,\bar Z_0(\mathcal M^c)\,\Pi_T(\omega)=\big(1-q_0(\mathcal M)\big)\,\widehat Z(\omega),\qquad\omega\in\tilde\Omega. \tag{0.3}
$$
Note that $\tilde\Omega\subseteq E$ and that $\Pi_T$, hence the ratio in (0.3), is the same function on both runs; only the constant prefactor differs, because the actual algorithm reports $\bar Z_0$, not $\bar Z_0(\mathcal M^c)$.

---

## 1. Two lemmas on kernels

**Lemma 1 (non-crossing invariant kernels).** Let $q$ be a probability on the finite set $\mathcal S$ with $q(S)>0$ for all $S$, and let $K$ be a $q$-invariant Markov kernel with $K(S,\mathcal M)=0$ for all $S\in\mathcal M^c$. Then:

1. $K(S,\mathcal M^c)=0$ for all $S\in\mathcal M$; that is, both $\mathcal M$ and $\mathcal M^c$ are closed under $K$.
2. The restriction $\tilde K=(K(S,S'))_{S,S'\in\mathcal M^c}$ is a Markov kernel on $\mathcal M^c$ and is $q(\cdot\mid\mathcal M^c)$-invariant. Symmetrically, the restriction of $K$ to $\mathcal M$ is $q(\cdot\mid\mathcal M)$-invariant.
3. If $K_1,\dots,K_m$ are $q$-invariant and non-crossing, then $K_1\cdots K_m$ is $q$-invariant and non-crossing, and its restriction to $\mathcal M^c$ is $\tilde K_1\cdots\tilde K_m$.

*Proof.* (1) By invariance and the hypothesis,
$$
q(\mathcal M)=\sum_{S\in\mathcal S}q(S)K(S,\mathcal M)=\sum_{S\in\mathcal M}q(S)K(S,\mathcal M)\le\sum_{S\in\mathcal M}q(S)=q(\mathcal M),
$$
so equality holds throughout, and since $q(S)>0$ for every $S\in\mathcal M$ this forces $K(S,\mathcal M)=1$, i.e. $K(S,\mathcal M^c)=0$, for every $S\in\mathcal M$.

(2) For $S\in\mathcal M^c$, $\sum_{S'\in\mathcal M^c}\tilde K(S,S')=K(S,\mathcal M^c)=1-K(S,\mathcal M)=1$, so $\tilde K$ is stochastic. For $S'\in\mathcal M^c$, using $K(S,S')=0$ when $S\in\mathcal M$ (part 1),
$$
\sum_{S\in\mathcal M^c}q(S\mid\mathcal M^c)\tilde K(S,S')=\frac1{q(\mathcal M^c)}\sum_{S\in\mathcal S}q(S)K(S,S')=\frac{q(S')}{q(\mathcal M^c)}=q(S'\mid\mathcal M^c).
$$
The statement for $\mathcal M$ is the same computation with the roles exchanged, using part 1.

(3) Invariance of a composition of invariant kernels is immediate. For $S\in\mathcal M^c$, $(K_1K_2)(S,\mathcal M)=\sum_{U}K_1(S,U)K_2(U,\mathcal M)=\sum_{U\in\mathcal M^c}K_1(S,U)K_2(U,\mathcal M)=0$, and for $S,S'\in\mathcal M^c$, $(K_1K_2)(S,S')=\sum_{U\in\mathcal M^c}K_1(S,U)K_2(U,S')=(\tilde K_1\tilde K_2)(S,S')$, because $K_1(S,U)=0$ for $U\in\mathcal M$. Induction on $m$. $\square$

Lemma 1 applies to every $K_{t,\ell}$ with $q=q_{\phi_t}$, since $q_{\phi_t}>0$ on $\mathcal S$. It shows that the "non-crossing" hypothesis, stated only for moves out of $\mathcal M^c$, is automatically two-sided: an invariant kernel that cannot reach the mode cannot leave it either. This is the first sentence of T5(ii).

**Lemma 2 (pathwise confinement).** Let $\omega\in\Omega$ with $P(\omega)>0$ and $\omega\in E$. Then $Y_{t,\ell}^j\in\mathcal M^c$ for every $t\le T$, $0\le\ell\le m_t$ and $j\le N$; in particular $\omega\in\tilde\Omega$. The same holds for any schedule, any resampling kernel and any non-crossing kernels; invariance and unbiasedness are not used.

*Proof.* Induction over the pairs $(t,\ell)$ in lexicographic order. The resampled population $Y_{t,0}=\hat X_t$ consists of copies of entries of $X_{t-1}$, which lie in $\mathcal M^c$ by the induction hypothesis (for $t=1$, by $\omega\in E$). If $Y_{t,\ell-1}^j\in\mathcal M^c$ and $Y_{t,\ell}^j\in\mathcal M$ for some $j$, then the factor $K_{t,\ell}(Y_{t,\ell-1}^j,Y_{t,\ell}^j)\le K_{t,\ell}(Y_{t,\ell-1}^j,\mathcal M)=0$ appears in (0.1), so $P(\omega)=0$, a contradiction. $\square$

---

## 2. Parts (i) and (ii)

**Proof of (i).** By (0.1), $X_0$ has law $q_0^{\otimes N}$, so $P(E)=q_0(\mathcal M^c)^N=(1-q_0(\mathcal M))^N$. For $x\in[0,1]$ and $N\ge1$, $(1-x)^N\ge1-Nx$ (Bernoulli's inequality: the function $x\mapsto(1-x)^N-1+Nx$ vanishes at $0$ and has derivative $N(1-(1-x)^{N-1})\ge0$ on $[0,1]$). The second claim, that on $E$ no particle ever enters $\mathcal M$, is Lemma 2. $\square$

**Proposition 2 (the coupling).** Under the hypotheses of T5 and (H1)–(H2):

1. For every $\omega\in\tilde\Omega$, $P(\omega)=P(E)\,\tilde P(\omega)$.
2. $P(\,\cdot\mid E)=\tilde P$ as probabilities on $\Omega$. Consequently, for every function $F$ on $\Omega$ (with values in any set), the conditional law of $F$ given $E$ under $P$ equals the law of $F$ under $\tilde P$:
$$
P\big(F\in B\mid E\big)=\tilde P\big(F\in B\big)\qquad\text{for all }B .
$$
3. In particular $\widehat Z$ given $E$ has the law of $\widehat Z^{\rm res}/(1-q_0(\mathcal M))$ under the restricted run, by (0.3).

*Proof.* (1) Let $\omega\in\tilde\Omega$, so all $X_0^j$ and all $Y_{t,\ell}^j$ lie in $\mathcal M^c$. In (0.1), $q_0(X_0^j)=q_0(\mathcal M^c)\,\tilde q_0(X_0^j)$ for each $j$; the resampling factor $R_t(h_{t-1},A_t)$ is the same in both runs, since it is the same kernel evaluated at the same history (in particular $W_t$ is computed from the same function $G_t$ on the same points) (audit 2026-10-15); and $K_{t,\ell}(Y_{t,\ell-1}^j,Y_{t,\ell}^j)=\tilde K_{t,\ell}(Y_{t,\ell-1}^j,Y_{t,\ell}^j)$ by the definition of the restriction, both arguments being in $\mathcal M^c$. Multiplying, $P(\omega)=q_0(\mathcal M^c)^N\,\tilde P(\omega)=P(E)\,\tilde P(\omega)$.

(2) By Lemma 2, $P(E\setminus\tilde\Omega)=0$. Hence for every $F\subseteq\Omega$, using (1) and $\tilde P(\Omega\setminus\tilde\Omega)=0$,
$$
P(F\cap E)=P(F\cap\tilde\Omega)=\sum_{\omega\in F\cap\tilde\Omega}P(E)\tilde P(\omega)=P(E)\,\tilde P(F).
$$
Since $P(E)>0$, dividing gives $P(F\mid E)=\tilde P(F)$. (Taking $F=\Omega$ confirms that $\tilde P$ has total mass $1$, as it must.) The statement about functions is the case $F=\{F\in B\}$.

(3) is (0.3) together with (2). $\square$

**Remark 2.1 (what "every function of the particle system" covers).** Proposition 2(2) applies to the whole trajectory, hence jointly to all stage-wise diagnostics: the empirical ESS $\big(\sum_iw_t^i\big)^2/\sum_i(w_t^i)^2$ at every stage, the number of distinct models, the visited set $V$, the particle PIPs, the HPM over $V$, and $\Pi_T$. (audit 2026-10-15: acceptance rates were listed here, but they are not functions on $\Omega$, which records states and not proposals or accept/reject decisions: a self-transition can come from a rejection or from an accepted self-proposal. They are covered once the trajectory is augmented with the proposals and the decisions and the restricted run uses the same proposal mechanism with acceptance computed from $\tilde\gamma_\phi=\gamma_\phi\mathbf 1_{\mathcal M^c}$. For the Metropolis–Hastings kernels of P6 this holds: for $S\in\mathcal M^c$ and a proposal $S'\in\mathcal M$ with $\Pi(S,S')>0$, non-crossing forces $\alpha(S,S')=0$ in the actual run, and $\tilde\gamma(S')=0$ gives $\alpha=0$ in the restricted run; for $S,S'\in\mathcal M^c$ the acceptance probabilities coincide. The factor-by-factor argument of Proposition 2 then applies to the augmented trajectory verbatim. We do not write this out.) Conditionally on $E$, each has exactly the law it would have on the restricted problem, in which $\mathcal M$ does not exist. Only the reported $\widehat Z$ carries a trace of $\mathcal M$, and that trace is the deterministic constant $\bar Z_0/\bar Z_0(\mathcal M^c)$, which the algorithm cannot distinguish from a restricted problem with start constant $\bar Z_0$.

**Remark 2.2 (R independent islands).** Let $\omega_1,\dots,\omega_R$ be independent copies of the system, with law $P^{\otimes R}$ on $\Omega^R$, and let $E_R=\{\omega_r\in E\text{ for all }r\}$. Then $P^{\otimes R}(E_R)=P(E)^R=(1-q_0(\mathcal M))^{NR}$, and for product sets $F_1\times\dots\times F_R$,
$$
P^{\otimes R}\big(F_1\times\dots\times F_R\cap E_R\big)=\prod_rP(F_r\cap E)=P(E)^R\prod_r\tilde P(F_r),
$$
so $P^{\otimes R}(\,\cdot\mid E_R)=\tilde P^{\otimes R}$ on product sets, hence on all of $\Omega^R$ (finite product space; product sets determine the law). Conditionally on $E_R$, the $R$ islands are therefore $R$ independent restricted runs, and every function of all $R$ systems (the island mean $\bar Z_R$ up to the constant factor, the between-island variance, the CLT interval of P7(ii), any disagreement statistic) has its restricted law. Agreement between islands is thus consistent with all of them having lost $\mathcal M$. When the schedule and tuning are frozen by an independent pilot, as in Section 2.3, all of this holds conditionally on the pilot, with $P$ the conditional law of one island given the pilot; the independence of the islands given the pilot is the only thing used.

**Remark 2.3 (a pathwise coupling).** The law identity yields a coupling in the usual sense. Since $0<P(E)<1$, let $\tilde\omega\sim\tilde P$, $\omega'\sim P(\cdot\mid E^c)$ and $\beta\sim\mathrm{Bernoulli}(P(E))$ be independent, and set $\omega=\tilde\omega$ if $\beta=1$, $\omega=\omega'$ if $\beta=0$. Then $\omega\sim P(E)\tilde P+P(E^c)P(\cdot\mid E^c)=P$ by Proposition 2(2), $\{\beta=1\}=\{\omega\in E\}$ up to a null set (because $\tilde P(E)=1$ and $P(E\mid E^c)=0$), and on this event the actual run and the restricted run coincide pathwise: $\omega=\tilde\omega$. For islands, do this independently for each island.

---

## 3. Unbiasedness of the product of weight averages

The following is the standard unbiasedness of the SMC normalising-constant estimate, in the form in which it is applied to the restricted run. P7(i) is the special case $\mathcal S'=\mathcal S$, $\gamma'_t=\gamma_{\phi_t}$; the proof is included because P7 is stated for the composite start of P1, whereas the restricted start $\tilde q_0$ is not of that form.

**Lemma 3.** Let $\mathcal S'$ be a finite set, $\gamma'_0,\dots,\gamma'_T$ strictly positive functions on $\mathcal S'$ with $Z'_t=\sum_S\gamma'_t(S)$ and $q'_t=\gamma'_t/Z'_t$, and $G_t=\gamma'_t/\gamma'_{t-1}$. Run the system of Section 0.2 on $\mathcal S'$: $X_0\sim q_0'^{\otimes N}$, resampling by kernels $R_t$ from histories satisfying (H1) with the unbiasedness identity, and at stage $t$ mutations $\mathcal K_t=K_{t,1}\cdots K_{t,m_t}$ with each $K_{t,\ell}$ $q'_t$-invariant, applied as in (H2). Then for every $t\in\{0,\dots,T\}$ and every $f:\mathcal S'\to\mathbb R$,
$$
\mathbb E\Big[\Pi_t\cdot\frac1N\sum_{j=1}^Nf(X_t^j)\Big]=\frac1{Z'_0}\sum_{S\in\mathcal S'}\gamma'_t(S)f(S)=\frac{Z'_t}{Z'_0}\,q'_t(f). \tag{3.1}
$$
In particular $\mathbb E[\Pi_T]=Z'_T/Z'_0$.

*Proof.* All random variables are bounded (finite space), so all expectations exist. Let $\mathcal G_{t-1}$ be the $\sigma$-field generated by $X_0$ and $(A_s,Y_{s,\cdot})_{s<t}$, and $\hat{\mathcal G}_t$ the one generated by $\mathcal G_{t-1}$ and $A_t$. From (0.1): conditionally on $\mathcal G_{t-1}$, $A_t\sim R_t(h_{t-1},\cdot)$ (audit 2026-10-15; $\mathcal G_{t-1}$ is generated by $h_{t-1}$); conditionally on $\hat{\mathcal G}_t$, the $X_t^j$ are independent with $X_t^j\sim\mathcal K_t(\hat X_t^j,\cdot)$, where $\hat X_t^j=X_{t-1}^{A_t^j}$. Write $O_t^i=\#\{j:A_t^j=i\}$ for the offspring count of particle $i$, so that (H1) gives $\mathbb E[O_t^i\mid\mathcal G_{t-1}]=NW_t^i$ with $W_t^i=G_t(X_{t-1}^i)/\sum_kG_t(X_{t-1}^k)$.

Induction on $t$. For $t=0$, $\Pi_0=1$ and $\mathbb E[f(X_0^j)]=q'_0(f)$ for each $j$, which is (3.1). Suppose (3.1) holds at $t-1$ for every $f$. Then
$$
\mathbb E\Big[\frac1N\sum_jf(X_t^j)\ \Big|\ \hat{\mathcal G}_t\Big]=\frac1N\sum_j(\mathcal K_tf)(X_{t-1}^{A_t^j})=\frac1N\sum_iO_t^i\,(\mathcal K_tf)(X_{t-1}^i),
$$
and taking the conditional expectation given $\mathcal G_{t-1}$,
$$
\mathbb E\Big[\frac1N\sum_jf(X_t^j)\ \Big|\ \mathcal G_{t-1}\Big]=\sum_iW_t^i\,(\mathcal K_tf)(X_{t-1}^i)=\frac{\sum_iG_t(X_{t-1}^i)\,(\mathcal K_tf)(X_{t-1}^i)}{\sum_kG_t(X_{t-1}^k)} .
$$
Since $\Pi_t=\Pi_{t-1}\cdot\frac1N\sum_kG_t(X_{t-1}^k)$ is $\mathcal G_{t-1}$-measurable,
$$
\mathbb E\Big[\Pi_t\,\frac1N\sum_jf(X_t^j)\Big]=\mathbb E\Big[\Pi_{t-1}\cdot\frac1N\sum_i\big(G_t\cdot\mathcal K_tf\big)(X_{t-1}^i)\Big]
=\frac1{Z'_0}\sum_S\gamma'_{t-1}(S)G_t(S)(\mathcal K_tf)(S),
$$
by the induction hypothesis applied to $g=G_t\cdot\mathcal K_tf$. Finally $\gamma'_{t-1}G_t=\gamma'_t$, and $\mathcal K_t$ is $q'_t$-invariant (a composition of invariant kernels), so
$$
\frac1{Z'_0}\sum_S\gamma'_t(S)(\mathcal K_tf)(S)=\frac{Z'_t}{Z'_0}\,q'_t(\mathcal K_tf)=\frac{Z'_t}{Z'_0}\,q'_t(f),
$$
which is (3.1) at $t$. The last claim is $f\equiv1$, $t=T$. $\square$

---

## 4. Part (iii)

**Proof of (iii).** The restricted run satisfies the hypotheses of Lemma 3 with $\mathcal S'=\mathcal M^c$, $\gamma'_t=\gamma_{\phi_t}\mathbf 1_{\mathcal M^c}$ (strictly positive on $\mathcal M^c$), $Z'_t=\bar Z_{\phi_t}(\mathcal M^c)$, $q'_t=\tilde q_{\phi_t}$, the same $G_t$ and $R_t$, and kernels $\tilde K_{t,\ell}$, which are Markov kernels on $\mathcal M^c$ and $\tilde q_{\phi_t}$-invariant by Lemma 1(2). Hence
$$
\mathbb E_{\tilde P}[\Pi_T]=\frac{\bar Z_1(\mathcal M^c)}{\bar Z_0(\mathcal M^c)} .
$$
By Proposition 2(2) applied to $F=\Pi_T$ (a bounded function on $\Omega$), $\mathbb E[\Pi_T\mid E]=\mathbb E_{\tilde P}[\Pi_T]$. Therefore, by (0.2),
$$
\mathbb E[\widehat Z\mid E]=m(\emptyset)\,\bar Z_0\,\frac{\bar Z_1(\mathcal M^c)}{\bar Z_0(\mathcal M^c)}
=m(\emptyset)\bar Z_1\cdot\frac{\bar Z_1(\mathcal M^c)}{\bar Z_1}\cdot\frac{\bar Z_0}{\bar Z_0(\mathcal M^c)}
=Z\cdot\frac{1-q_1(\mathcal M)}{1-q_0(\mathcal M)} .
$$
The unconditional identity $\mathbb E[\widehat Z]=Z$ is P7(i); it is also Lemma 3 with $\mathcal S'=\mathcal S$, $\gamma'_t=\gamma_{\phi_t}$, all hypotheses of which hold for the actual run. $\square$

**Remark 4.1 (reading the factor).** $\rho=(1-q_1(\mathcal M))/(1-q_0(\mathcal M))<1$ if and only if $q_1(\mathcal M)>q_0(\mathcal M)$, i.e. if and only if $\mathcal M$ gains mass along the bridge: an *incoming* mode. In the switch regime of T3 with $\kappa_0>0$ and $\mathcal M=\{S_0\}$ (or any $\mathcal M\ni S_0$ whose start mass is $e^{-\Theta(n)}$, which must then exclude $\tilde S_0$), T3 gives $q_0(\mathcal M)=e^{-\Theta(n)}$ and $q_1(\mathcal M)\to1$, so $\rho\approx1-q_1(\mathcal M)\to0$. (audit 2026-10-15: the pre-audit text said "with $\mathcal M$ a set containing $S_0$, $q_0(\mathcal M)=e^{-\Theta(n)}$". That is false in general: a set containing $S_0$ may also contain $\tilde S_0$ and then has start mass tending to $1$; and if $\kappa_0=0$ (T3(iii)), $q_0(S_0)$ is only polynomially small, e.g. $n^{-1/2}e^{O_{\mathbb P}(1)}$ when $|S_0|-|\tilde S_0|=1$, so the particle requirement $N\gg1/q_0(\mathcal M)$ is polynomial.) For an outgoing set, $\rho>1$ and the conditional mean exceeds $Z$. Combining the two identities of (iii),
$$
\mathbb E[\widehat Z\mid E^c]=Z\,\frac{1-P(E)\rho}{1-P(E)},
$$
so when $\rho<1$ the unbiasedness of $\widehat Z$ is carried entirely by the rare event $E^c$: since $1-P(E)\le Nq_0(\mathcal M)$, the conditional mean given $E^c$ is at least $Z(1-\rho)/(Nq_0(\mathcal M))$, on an event of probability at most $Nq_0(\mathcal M)$.

---

## 5. Parts (iv) and (v)

**Proof of (iv).** Index everything by $n$: $\mathcal S_n$, $\gamma_{0,n}$, $d_n$, $\mathcal M_n$, the schedule, $N=N_n$, the laws $P_n$ and $\tilde P_n$, and $Z_n=m(\emptyset)\bar Z_{1,n}$. The hypothesis of relative consistency says that the restricted run's normalising-constant estimator satisfies
$$
\frac{\bar Z_{0,n}(\mathcal M_n^c)\,\Pi_T}{\bar Z_{1,n}(\mathcal M_n^c)}\ \longrightarrow\ 1\quad\text{in }\tilde P_n\text{-probability}, \tag{5.1}
$$
i.e. $\tilde P_n(|\log\Pi_T-\log\{\bar Z_{1,n}(\mathcal M^c_n)/\bar Z_{0,n}(\mathcal M^c_n)\}|>\varepsilon)\to0$ for every $\varepsilon>0$. (All quantities are strictly positive, so the logarithms are defined: $G_t>0$ because $d_n$ is finite on a finite set.)

By (0.2) and the definition of $\rho_n$,
$$
\log\widehat Z-\log Z_n-\log\rho_n=\log\Pi_T-\log\frac{\bar Z_{1,n}(\mathcal M_n^c)}{\bar Z_{0,n}(\mathcal M_n^c)}=:D_n,
$$
a function on $\Omega_n$. Fix $\varepsilon>0$. Then, by part (i) and Proposition 2(2),
$$
P_n(|D_n|>\varepsilon)\le P_n(E^c)+P_n(\{|D_n|>\varepsilon\}\cap E)\le N_nq_0(\mathcal M_n)+\tilde P_n(|D_n|>\varepsilon)\ \longrightarrow\ 0,
$$
the first term by the hypothesis $N_nq_0(\mathcal M_n)\to0$ and the second by (5.1). This is the claim $\log\widehat Z=\log Z+\log(1-q_1(\mathcal M))-\log(1-q_0(\mathcal M))+o_{P}(1)$. $\square$

**Remark 5.1.** The proof uses multinomial resampling nowhere: it uses only Proposition 2 and the hypothesis (5.1), and so holds for any resampling scheme satisfying (H1). (audit 2026-10-15: the frozen statement named multinomial resampling in (iv); the current draft has dropped it, in line with this remark.) Multinomial resampling is the scheme for which (5.1) is known to hold for a fixed problem as $N\to\infty$ (the LLN of Fact F1); along a triangular array (5.1) is a genuine hypothesis, as the statement says, and it is not proved here. In particular, the reading "the estimate of $Z$ concentrates around $Z\rho$" needs (5.1); without it, (iii) gives only the conditional mean. The same argument gives, for any sequence of bounded functions $f_n$ on $\mathcal S_n$ and the particle averages $\frac1N\sum_jf_n(X_T^j)$: if these converge to $\tilde q_{1,n}(f_n)$ in $\tilde P_n$-probability (a restricted LLN), then they do so in $P_n$-probability. Mode loss replaces every posterior expectation by its conditional version given $\mathcal M^c$, and the particles cannot tell.

**Proof of (v).** Here the hypothesis is $K_{t,\ell}(S,\mathcal M)\le\eta$ for all $S\in\mathcal M^c$, all $t$ and $\ell$; nothing else about the kernels, the schedule or the resampling is used. Let
$$
\mathcal A=\{\exists j:\ X_0^j\in\mathcal M\}\ \cup\ \{\exists\,(t,\ell,j):\ Y_{t,\ell}^j\in\mathcal M\}
$$
be the event that some particle is ever in $\mathcal M$ (the resampled populations $\hat X_t=Y_{t,0}$ are included, though they add nothing, being copies of entries of $X_{t-1}$). Put $\mathcal A_0=\{\exists j:X_0^j\in\mathcal M\}$ and, for $t\le T$, $1\le\ell\le m_t$, $j\le N$,
$$
\mathcal B_{t,\ell,j}=\{Y_{t,\ell-1}^j\in\mathcal M^c,\ Y_{t,\ell}^j\in\mathcal M\}.
$$
*Claim:* $\mathcal A\subseteq\mathcal A_0\cup\bigcup_{t,\ell,j}\mathcal B_{t,\ell,j}$. Indeed, let $\omega\in\mathcal A\setminus\mathcal A_0$ and let $(t,\ell)$ be the lexicographically first pair with $Y_{t,\ell}^j\in\mathcal M$ for some $j$. Then $\ell\ge1$: for $\ell=0$, $Y_{t,0}=\hat X_t$ consists of copies of entries of $X_{t-1}$, which is $X_0$ if $t=1$ and $Y_{t-1,m_{t-1}}$ otherwise, and in both cases lies in $(\mathcal M^c)^N$ by the choice of $(t,\ell)$ and $\omega\notin\mathcal A_0$. By minimality $Y_{t,\ell-1}^j\in\mathcal M^c$, so $\omega\in\mathcal B_{t,\ell,j}$.

By (0.1), conditionally on everything up to and including $Y_{t,\ell-1}$, the state $Y_{t,\ell}^j$ has law $K_{t,\ell}(Y_{t,\ell-1}^j,\cdot)$, so
$$
P(\mathcal B_{t,\ell,j})=\mathbb E\big[\mathbf 1\{Y_{t,\ell-1}^j\in\mathcal M^c\}\,K_{t,\ell}(Y_{t,\ell-1}^j,\mathcal M)\big]\le\eta .
$$
Also $P(\mathcal A_0)\le\sum_jP(X_0^j\in\mathcal M)=Nq_0(\mathcal M)$. The union bound over $\mathcal A_0$ and the $N\sum_tm_t$ events $\mathcal B_{t,\ell,j}$ gives
$$
P(\mathcal A)\le N q_0(\mathcal M)+\eta\,N\sum_{t=1}^Tm_t=N\Big\{q_0(\mathcal M)+\eta\sum_tm_t\Big\}. \qquad\square
$$

**Remark 5.2.** With $\eta=0$, (v) recovers the probabilistic content of (i). For $\eta>0$ the bound is useful only when $\eta\sum_tm_t\ll1/N$; a kernel that enters $\mathcal M$ with probability $e^{-\Theta(n)}$ per move (a single addition of a cancelled variable, say, against a start that penalises it by $e^{-\Theta(n)}$) is for all practical purposes non-crossing. The bound counts entries only; what happens after an entry (whether the mode is then populated through resampling) is not addressed by (v).

---

## 6. Adaptive schedules: what survives

### 6.1 The adaptive system

An adaptive run chooses the stage design from the particles. Formally, let $U$ be a random element with an arbitrary law $\mu$ on some measurable space (the auxiliary randomness of the adaptation rule; $U$ is constant for a deterministic rule), independent of everything else. At stage $t$, after the population $X_{t-1}$ is available, the design
$$
\mathsf D_t=\big(\phi_t,\ R_t,\ m_t,\ K_{t,1},\dots,K_{t,m_t}\big)=\Phi_t\big(U;\ X_0,(A_s,Y_{s,\cdot})_{s<t}\big)
$$
is a fixed measurable function $\Phi_t$ of $U$ and of the history, with $\phi_t\in(\phi_{t-1},1]$, and the run stops at the first stage $T$ with $\phi_T=1$. The weights of stage $t$ are $G_t(S)=\exp\{(\phi_t-\phi_{t-1})d(S)\}$ with the chosen $\phi_t$; resampling and mutation are as in (H1)–(H2) with the chosen resampling kernel and move kernels; every resampling kernel the rule can return satisfies the offspring identity of (H1) for the weights of the chosen $\phi_t$ (audit 2026-10-15: $R_t$ added to the design, which covers a fixed scheme as a special case). The empirical-ESS rule of Section 2.3, with $\phi_t=\sup\{\phi\le1:\ \mathrm{ESS}(\{e^{(\phi-\phi_{t-1})d(X^i_{t-1})}\}_i)\ge\rho N\}$ and $K_{t,\ell}=K_{\phi_t}$ for a fixed family $(K_\phi)$, is the case of a deterministic $\Phi_t$ depending on the history only through $X_{t-1}$ and $\phi_{t-1}$. The hypotheses on the kernels are now imposed on every design the rule can choose:

> **(NC)** for every $\phi\in[0,1]$ and every kernel $K$ that $\Phi_t$ can return at level $\phi$, $K$ is $q_\phi$-invariant and non-crossing.

For the family $K_\phi$ built from P6 this is the assumption that the move set cannot reach $\mathcal M$ from $\mathcal M^c$ at any temperature, which is what "the mutation kernel cannot cross between the two modes" means.

The adaptive restricted run is the *same* rule $\Phi_t$ applied to the restricted problem: initial particles i.i.d. $\tilde q_0$, the same functions $\Phi_t$ evaluated on its own history, kernels restricted to $\mathcal M^c$ (Lemma 1), the same resampling kernels $R_s$ returned by $\Phi_s$ (audit 2026-10-15). Its law is $\tilde P^{\rm ad}$; the law of the actual adaptive run is $P^{\rm ad}$. Trajectories now have random length $T$; the trajectory space is the set of finite sequences of stage outcomes (and $U$). The estimate is $\widehat Z=m(\emptyset)\bar Z_0\Pi_T$ with the random $T$.

To avoid an infinite-stage pathology, assume **(F)**: under both $P^{\rm ad}$ and $\tilde P^{\rm ad}$, $T<\infty$ almost surely. (For the empirical-ESS rule with threshold $\rho<1$ on a finite space this is automatic. The ESS of the weights $e^{\delta d(X^i_{t-1})}$ is a continuous function of the step $\delta\ge0$ that equals $N>\rho N$ at $\delta=0$ and depends on the population only through the multiset $\{d(X^i_{t-1})\}_i$; so the untruncated step $\delta^\ast(\text{multiset})=\sup\{\delta:\mathrm{ESS}\ge\rho N\}\in(0,\infty]$ is strictly positive, and there are finitely many multisets. Put $\delta_{\min}=\min\{1,\min\delta^\ast\}>0$. Every step is at least $\delta_{\min}$ unless it is the final step to $\phi=1$, so $(T-1)\delta_{\min}<1$ and $T\le\max\{1,\lceil1/\delta_{\min}\rceil\}$. (audit 2026-10-15: the truncation at $1$ covers the homogeneous case, e.g. $N=1$ or constant $d$, where every $\delta^\ast=+\infty$ and $T=1$.))

### 6.2 Theorem T5-adaptive

**Theorem (T5 under adaptation).** Under (H1), (H2), (NC), (F):

1. **(i) survives verbatim.** $P^{\rm ad}(E)=(1-q_0(\mathcal M))^N\ge1-Nq_0(\mathcal M)$, and on $E$ no particle ever enters $\mathcal M$.
2. **(ii) survives verbatim.** $P^{\rm ad}(\,\cdot\mid E)=\tilde P^{\rm ad}$ as laws of the entire trajectory, *including* the random schedule $(\phi_t)$, the stage count $T$, the move counts $m_t$ and the chosen kernels. Every function of the adaptive particle system has, given $E$, the law it has under the adaptive restricted run. For $R$ independent adaptive islands the same holds given $E_R$, with probability $(1-q_0(\mathcal M))^{NR}$; for islands frozen from a pilot, conditionally on the pilot (that is the frozen case, Section 2).
3. **(iii) survives only in conditional form.** $\mathbb E[\widehat Z\mid E]=\dfrac{1}{1-q_0(\mathcal M)}\,\mathbb E_{\tilde P^{\rm ad}}\big[\widehat Z^{\rm res}\big]$, where $\widehat Z^{\rm res}=m(\emptyset)\bar Z_0(\mathcal M^c)\Pi_T$ is the adaptive restricted estimate. (The expectations exist: since each $G_t\in[e^{-(\phi_t-\phi_{t-1})\|d\|_\infty},e^{(\phi_t-\phi_{t-1})\|d\|_\infty}]$ and the increments sum to $1$, $\Pi_T\in[e^{-\|d\|_\infty},e^{\|d\|_\infty}]$ whatever the schedule and $T$.) The unconditional identity $\mathbb E[\widehat Z]=Z$, and hence the explicit value $Z\rho$ of the conditional mean, fail in general for adaptive rules satisfying (NC) and (F) (Example 6.4; audit 2026-10-15, previously Example 6.3, which lies outside (NC)). What survives is the transfer principle: the conditional law of $\widehat Z/(Z\rho)$ given $E$ is the law of $\widehat Z^{\rm res}/\big(m(\emptyset)\bar Z_1(\mathcal M^c)\big)$ under the adaptive restricted run. Whatever bias, variance or concentration the adaptive algorithm has on the restricted problem, $\widehat Z$ inherits it, around the wrong centre $Z\rho$.
4. **(iv) survives verbatim**, with the relative-consistency hypothesis (5.1) read for the adaptive restricted run: if $N_nq_0(\mathcal M_n)\to0$ and $\bar Z_{0,n}(\mathcal M_n^c)\Pi_T/\bar Z_{1,n}(\mathcal M_n^c)\to1$ in $\tilde P^{\rm ad}_n$-probability, then $\log\widehat Z=\log Z+\log(1-q_1(\mathcal M))-\log(1-q_0(\mathcal M))+o_P(1)$.
5. **(v) survives with an expected move budget, not verbatim** (audit 2026-10-15). Here (NC) is replaced by the leakage hypothesis: $K(S,\mathcal M)\le\eta$ for every $S\in\mathcal M^c$ and every kernel the rule can choose (invariance is not needed, and neither is (F)). Then
$$
P^{\rm ad}(\mathcal A)\le N\Big\{q_0(\mathcal M)+\eta\,\mathbb E^{\rm ad}\Big[\sum_{t\le T}m_t\Big]\Big\},
$$
and in particular $P^{\rm ad}(\mathcal A)\le N\{q_0(\mathcal M)+\eta\,\bar m\}$ whenever $\sum_{t\le T}m_t\le\bar m$ almost surely for a constant $\bar m$. The bound of (v) with the random $\sum_tm_t$ on the right is false: in the example after the proof, $P^{\rm ad}(\mathcal A)=0.325$ while $N\{q_0(\mathcal M)+\eta\sum_tm_t\}=0.1$ on the event $\{m_1=0\}$, which has probability $\tfrac12$.

*Proof.* Condition on $U=u$ throughout; the statements for a random $U$ follow by integrating over $\mu$, because $E$ does not involve $U$ and $P^{\rm ad}(E\mid U=u)=(1-q_0(\mathcal M))^N$ does not depend on $u$ (the initial draw is independent of $U$). With $u$ fixed, every design is a deterministic function of the discrete history, so the trajectory is a discrete-time process on a countable space, and for every finite prefix $\omega_{\le t}=(X_0,(A_s,Y_{s,\cdot})_{s\le t})$ with $t\le T$ the probability is
$$
P^{\rm ad}(\omega_{\le t}\mid U=u)=\prod_jq_0(X_0^j)\prod_{s=1}^t\Big[R_s\big(h_{s-1},A_s\big)\prod_{\ell=1}^{m_s}\prod_jK_{s,\ell}\big(Y_{s,\ell-1}^j,Y_{s,\ell}^j\big)\Big], \tag{6.1}
$$
where now $\phi_s$, $R_s$, $m_s$, $K_{s,\ell}$ and hence $W_s$ are the values $\Phi_s(u;\omega_{<s})$ returns on this prefix (audit 2026-10-15: the resampling factor was $R_N(W_s(X_{s-1}),A_s)$); (6.1) is (0.1) with the designs evaluated along the path.

(1) $P^{\rm ad}(E)$ is a statement about $X_0$ only. Lemma 2 applies to each prefix: its proof uses only that each factor $K_{s,\ell}$ appearing in (6.1) is non-crossing, which (NC) guarantees for every design the rule can return.

(2) For a prefix with all states in $\mathcal M^c$, the rule $\Phi_s(u;\omega_{<s})$ returns the same design in the actual and the restricted run, since it is the same function of the same history. Hence $W_s$ agrees, the resampling factors agree, and $K_{s,\ell}(y,y')=\tilde K_{s,\ell}(y,y')$ for $y,y'\in\mathcal M^c$. As in Proposition 2(1), $P^{\rm ad}(\omega_{\le t}\mid U=u)=P(E)\,\tilde P^{\rm ad}(\omega_{\le t}\mid U=u)$ for every such prefix. The event $\{T=t\}$ is determined by the prefix $\omega_{\le t}$ (it is $\{\phi_t=1\}$ with $\phi_t$ a function of $\omega_{<t}$), so the identity holds for complete trajectories of every finite length, and by (F) these carry full mass under both laws. Together with Lemma 2 ($P^{\rm ad}(E\setminus\tilde\Omega^{\rm ad})=0$), the argument of Proposition 2(2) gives $P^{\rm ad}(\cdot\mid E,U=u)=\tilde P^{\rm ad}(\cdot\mid U=u)$, and integrating over $u$, $P^{\rm ad}(\cdot\mid E)=\tilde P^{\rm ad}$. The schedule, $T$, the $m_t$ and the kernels are functions of the trajectory and $U$, so their laws transfer too. Islands: as in Remark 2.2.

(3) The identity is (2) applied to $F=\Pi_T$ together with $\widehat Z=\bar Z_0\widehat Z^{\rm res}/\bar Z_0(\mathcal M^c)$ on $\tilde\Omega^{\rm ad}$. The transfer principle is (2) applied to $F=\Pi_T$ and rescaled by constants. The failure of $\mathbb E[\widehat Z]=Z$ under (NC) and (F) is Example 6.4 (audit 2026-10-15; previously Example 6.3).

(4) The proof of (iv) in Section 5 used only part (i), Proposition 2(2) and (5.1); replace them by (1), (2) and the adaptive form of (5.1).

(5) (Rewritten, audit 2026-10-15.) Condition on $U=u$ and let $(t,\ell,j)$ range over all triples with $t\ge1$, $\ell\ge1$, $j\le N$. Let $\mathcal C_{t,\ell}=\{T\ge t,\ m_t\ge\ell\}$, the event that the $\ell$-th move of stage $t$ is made; it is determined by the history before stage $t$'s moves, because $T\ge t$ is $\{\phi_{t-1}<1\}$ and $m_t$ is part of $\mathsf D_t$. The covering argument of the proof of (v) applies to each trajectory, so
$$
\mathcal A\subseteq\mathcal A_0\cup\bigcup_{t,\ell,j}\big(\mathcal C_{t,\ell}\cap\mathcal B_{t,\ell,j}\big).
$$
Given the history up to $Y_{t,\ell-1}$ on $\mathcal C_{t,\ell}$, the state $Y^j_{t,\ell}$ has law $K_{t,\ell}(Y^j_{t,\ell-1},\cdot)$ with $K_{t,\ell}$ the kernel the rule chose, by (6.1). Hence $P^{\rm ad}(\mathcal C_{t,\ell}\cap\mathcal B_{t,\ell,j}\mid U=u)=\mathbb E\big[\mathbf 1_{\mathcal C_{t,\ell}}\mathbf 1\{Y^j_{t,\ell-1}\in\mathcal M^c\}K_{t,\ell}(Y^j_{t,\ell-1},\mathcal M)\mid U=u\big]\le\eta\,P^{\rm ad}(\mathcal C_{t,\ell}\mid U=u)$. Summing this countable union bound,
$$
P^{\rm ad}(\mathcal A\mid U=u)\le Nq_0(\mathcal M)+N\eta\sum_{t\ge1}\sum_{\ell\ge1}P^{\rm ad}(T\ge t,\ m_t\ge\ell\mid U=u)=Nq_0(\mathcal M)+N\eta\,\mathbb E^{\rm ad}\Big[\sum_{t\le T}m_t\ \Big|\ U=u\Big],
$$
by Tonelli. Integrating over $u$ gives the bound; the case $\sum_tm_t\le\bar m$ follows. No step uses invariance, non-crossing or (F) (if $T=\infty$ with positive probability, the expectation is over the infinite sum, and the bound may be infinite). $\square$

*The counterexample to the verbatim form* (Sol's audit, finding 1). $N=1$, a single stage ($\phi_1=1$), $q_0(\mathcal M)=0.1$, $q_1(\mathcal M)=\tfrac12$. With auxiliary randomness $U$, choose $m_1\in\{0,1\}$ with probability $\tfrac12$ each; a move is the independence sampler $K(S,\cdot)=q_1$, which is $q_1$-invariant and has $K(S,\mathcal M)=q_1(\mathcal M)=\tfrac12=:\eta$. Then $P^{\rm ad}(\mathcal A)=0.1+0.9\cdot\tfrac12\cdot\tfrac12=0.325$, which is at most the expectation bound $0.1+\tfrac12\cdot\tfrac12=0.35$, but exceeds the value $0.1$ that the verbatim right side takes on $\{m_1=0\}$. (`proofs/_audit/group_B/check_audit_B.py`, checks T5.F1.)

**Remark 6.1 (why (iii) is lost).** Lemma 3 needs the potential $G_t$ and the kernel $\mathcal K_t$ to be fixed in advance, not chosen from the particles on which they act (audit 2026-10-15: the pre-audit wording "$\mathcal G_{t-1}$-measurable functions chosen independently of the particles" was self-contradictory); more precisely, the step $\mathbb E[\Pi_{t-1}\frac1N\sum_i(G_t\mathcal K_tf)(X_{t-1}^i)]=\frac1{Z'_0}\sum_S\gamma'_{t-1}(S)G_t(S)(\mathcal K_tf)(S)$ applies the induction hypothesis to a *fixed* function $g=G_t\mathcal K_tf$. If $G_t$ depends on $X_{t-1}$ (adaptive $\phi_t$) then $g$ is random and the induction does not apply. This is the content of the frozen-schedule requirement in P7 and of the Remark after P6.

**Remark 6.2 (what the adaptive diagnostics show).** By (2), on $E$ the empirical-ESS schedule is the schedule the restricted bridge $\tilde q_0\to\tilde q_1$ calls for. If the only thing separating $\tilde q_\phi$ from $\tilde q_{\phi'}$ is the spread within $\mathcal M^c$, the run looks easy: few stages, high ESS, no sign of the $\log_2\Delta_0+O(1)$ stages that T4 says the switch would require. The adaptive schedule does not detect the lost mode; it adapts to its absence.

### 6.3 Examples: a particle-dependent schedule is biased

**Example 6.3 (outside the non-crossing class).** Let $\mathcal S=\{a,b\}$, $\gamma_0(a)=\gamma_0(b)=\tfrac12$ (so $\bar Z_0=1$), $d(a)=0$, $d(b)=D>0$, and $N=1$. Then $\bar Z_\phi=\tfrac12(1+e^{\phi D})$ and $\bar Z_1/\bar Z_0=\tfrac12(1+e^D)$. Resampling with one particle is trivial (the single offspring count is $1=NW^1$, so (H1) holds). Take as mutation kernel at level $\phi$ the independence sampler $K_\phi(S,\cdot)=q_\phi(\cdot)$, which is $q_\phi$-invariant, with $m_t=1$. Adaptive rule: if $X_0=a$, take $\phi_1=1$ (one stage); if $X_0=b$, take $\phi_1=\tfrac12$ and then $\phi_2=1$. This is a deterministic function of $X_0$. Then
$$
\mathbb E[\Pi_T]=\tfrac12\cdot e^{d(a)}+\tfrac12\cdot e^{D/2}\,\mathbb E_{q_{1/2}}\big[e^{d/2}\big]
=\tfrac12+\tfrac12\,e^{D/2}\,\frac{\bar Z_1}{\bar Z_{1/2}}
=\tfrac12+\tfrac12\,e^{D/2}\,\frac{1+e^{D}}{1+e^{D/2}} .
$$
Comparing with $\bar Z_1/\bar Z_0=\tfrac12+\tfrac12e^{D}$: the second terms differ by the factor $(1+e^D)/(e^{D/2}+e^D)=(1+e^D)/\{e^{D/2}(1+e^{D/2})\}$, which is $<1$ for every $D>0$ (equivalently $1+e^D<e^{D/2}+e^D$, i.e. $e^{D/2}>1$). So $\mathbb E[\widehat Z]<Z$ strictly. At $D=2$ the ratio of the two means is $\big(\tfrac12+\tfrac12e\,\tfrac{1+e^2}{1+e}\big)/\big(\tfrac12+\tfrac12e^2\big)=3.566/4.195\approx0.85$. The example has no mode set $\mathcal M$ and no non-crossing structure; it only shows that a schedule chosen from the particles breaks the unconditional identity in (iii), which is the one assertion of T5 whose proof passes through Lemma 3 on the full space. (This example is one specific particle-dependent rule, not the empirical-ESS rule; the claim is that unbiasedness is not a consequence of the adaptive structure, not that every adaptive rule is biased.) The script `check_T5.py` in this folder confirms this value by simulation (Monte Carlo mean 3.566, standard error 0.002), and also confirms part (iii) on a four-state example with $N=3$, multinomial resampling and non-crossing kernels: predicted $\mathbb E[\widehat Z\mid E]=1.8636$, observed $1.8635\pm0.0001$, with $\mathbb E[\widehat Z]=2.2435\pm0.0016$ against $Z=2.2442$.

*Scope (audit 2026-10-15).* Example 6.3 is not an instance of the adaptive theorem: it has no set $\mathcal M$, and on a two-point space no biased compliant example exists. With $\mathcal M$ one of the two points, Lemma 1(1) makes both points absorbing, so every invariant non-crossing kernel is the identity; and with identity kernels an adaptive schedule keeps $\widehat Z$ unbiased. Indeed, conditionally on $U=u$ throughout (or with the filtration enlarged by $U$), $H_t:=\Pi_t\cdot\frac1N\sum_ie^{(1-\phi_t)d(X_t^i)}$ satisfies $\mathbb E[H_t\mid\mathcal G_{t-1}]=\Pi_{t-1}\frac1N\sum_iG_t(X_{t-1}^i)e^{(1-\phi_t)d(X_{t-1}^i)}=H_{t-1}$ by (H1). Since $H$ is bounded and $T<\infty$ almost surely, optional stopping gives $\mathbb E[\Pi_T]=\mathbb E[H_T]=\mathbb E[H_0]=\bar Z_1/\bar Z_0$. The example therefore illustrates (iii)'s failure for adaptive rules in general. The in-class example is the next one.

**Example 6.4 (in the class of the adaptive theorem; Sol's audit, finding 2, audit 2026-10-15).** Add an isolated state to Example 6.3 with $D=2$. Let $\mathcal S=\{a,b,c\}$, $\mathcal M=\{c\}$, $\epsilon\in(0,1)$,
$$
\gamma_0(a)=\gamma_0(b)=\tfrac{1-\epsilon}2,\quad\gamma_0(c)=\epsilon\quad(\bar Z_0=1),\qquad d(a)=0,\ d(b)=2,\ d(c)=4,\qquad N=1 .
$$
At level $\phi$ the kernel is $K_\phi(S,\cdot)=q_\phi(\cdot\mid\{a,b\})$ for $S\in\{a,b\}$ and $K_\phi(c,\cdot)=\delta_c$, with $m_t=1$. It is $q_\phi$-invariant: for $S'\in\{a,b\}$, $\sum_{S\in\{a,b\}}q_\phi(S)q_\phi(S'\mid\{a,b\})=q_\phi(S')$, and $c$ is fixed. It is non-crossing: $K_\phi(S,\{c\})=0$ for $S\in\{a,b\}$. The rule is that of Example 6.3 on $\{a,b\}$ and a single stage from $c$: if $X_0\in\{a,c\}$, take $\phi_1=1$; if $X_0=b$, take $\phi_1=\tfrac12$ and then $\phi_2=1$. Resampling with $N=1$ is trivial, and the rule is a deterministic function of $X_0$. So (H1), (H2), (NC) and (F) hold. Then
$$
\mathbb E[\Pi_T]=\tfrac{1-\epsilon}2\cdot1+\tfrac{1-\epsilon}2\cdot e\,\mathbb E_{q_{1/2}(\cdot\mid\{a,b\})}\big[e^{d/2}\big]+\epsilon e^4=(1-\epsilon)B+\epsilon e^4,\qquad B=\tfrac12+\tfrac e2\,\frac{1+e^2}{1+e},
$$
because $q_{1/2}(\cdot\mid\{a,b\})\propto(1,e)$ gives $\mathbb E[e^{d/2}]=(1+e^2)/(1+e)$. On the other hand
$$
\bar Z_1/\bar Z_0=(1-\epsilon)A+\epsilon e^4,\qquad A=\tfrac{1+e^2}2 .
$$
Since $B<A$ (Example 6.3 with $D=2$), $\mathbb E[\widehat Z]<Z$ for every $\epsilon\in(0,1)$, and $\mathbb E[\widehat Z]/Z\to B/A\approx0.85026$ as $\epsilon\downarrow0$. The adaptive identity (3) holds here: $\mathbb E[\widehat Z\mid E]=B=\mathbb E_{\tilde P^{\rm ad}}[\widehat Z^{\rm res}]/(1-\epsilon)$. Exact values for $\epsilon\in\{0.1,0.01,10^{-4}\}$ (ratios $0.9388$, $0.8677$, $0.8505$) are in `proofs/_audit/group_B/check_audit_B.py` (checks T5.F2), which also checks the martingale claim above on a two-state instance with $N=2$.

---

## 7. Summary of the hypotheses used, and of what is proved

| Part | Uses | Hypotheses beyond the statement |
|---|---|---|
| (i) | Lemma 2 | none (non-crossing only; no invariance, no unbiasedness) |
| (ii) | Lemmas 1, 2; Proposition 2 | (H1), (H2); islands independent (given the pilot) |
| (iii) | (ii), Lemma 3 (= standard SMC unbiasedness, re-proved), P7(i) | (H1), (H2) |
| (iv) | (i), (ii) | (5.1) is a hypothesis under $\tilde P_n$; multinomial resampling not used |
| (v) | (0.1) | none (uses only $K(\cdot,\mathcal M)\le\eta$) |
| adaptive | Section 6 | (NC), (F) for (i)–(iv); the rule is the same function of the history in both runs; for (v): leakage $\le\eta$ for every kernel the rule can choose, with $\mathbb E\sum_tm_t$ (or a deterministic cap) in place of $\sum_tm_t$ (audit 2026-10-15) |

### Hypotheses (the current draft states (H1)–(H2) and items 3–4; none restricts the algorithm as implemented)

1. **(H1)** (audit 2026-10-15) The resampling scheme at stage $t$ is a Markov kernel $R_t$ from histories to ancestor vectors, with the offspring identity for every history; the actual and the restricted run use the same kernels. It may use auxiliary randomness and may look at the particle values (e.g. sorting before systematic resampling). The draft's rule, which depends on the current population's values and weights and is drawn afresh, is a special case. (Multinomial, residual, stratified and systematic all qualify, in any population-dependent order.) The pre-audit version required dependence on the weights only, which was narrower than the draft.
2. **(H2)** Mutations are applied independently across particles given the resampled population.
3. The $m_t$ kernels of stage $t$ may differ; each is $q_{\phi_t}$-invariant and non-crossing. (Generalises the statement; the statement's case is $K_{t,\ell}=K_t$.)
4. For $R$ islands: the islands are independent (given the pilot, when a pilot is used).
5. In (iv): the relative-consistency hypothesis is understood under the law $\tilde P_n$ of the restricted run, and "in probability" in the conclusion is under $P_n$. Both laws are explicit in Section 0.
6. For the adaptive theorem: **(NC)** every kernel the rule can choose, at every $\phi\in[0,1]$, is $q_\phi$-invariant and non-crossing; **(F)** the rule terminates almost surely; the rule is a measurable function of the history and of independent auxiliary randomness, the same function in both runs.

### Steps I am not fully sure of

- **None of parts (i)–(v).** Each proof is elementary and self-contained given Section 0; the only external input is the standard SMC unbiasedness, which is re-proved as Lemma 3 in the generality used.
- **Remark 5.1's extension to particle averages** is stated with a sketch of the argument, not a full proof; it is not part of T5.
- **(F)** is assumed for a general adaptive rule and verified only for the empirical-ESS rule (Section 6.1); the frozen-schedule theorem does not need it.
- **Examples 6.3 and 6.4** use an artificial particle-dependent rule to show that unbiasedness is lost under adaptation (Example 6.4 within the class (NC)–(F) of the adaptive theorem, audit 2026-10-15). It does not say anything about the bias of the empirical-ESS rule specifically; that is a known phenomenon in the literature but is not proved here.

---

## Audit revisions (2026-10-15)

Adjudicator B (Opus 5.5), after the GPT-6.1 Sol audit of T5 (`proofs/_audit/T5/SOL_AUDIT.md`), the first independent review of this proof. The pre-audit text is saved as `PROOF_pre_audit.md`. Rulings are in `proofs/_audit/group_B/RULINGS.md`.

1. **Summary of the outcome.** Rewritten: (v) does not survive adaptation verbatim; Example 6.4 is the in-class counterexample; probabilities are over the algorithm's randomness with the data fixed. (Findings 1, 2; draft-consistency note.)
2. **(H1), (0.1), Section 0.3, Proposition 2(1), Lemma 3.** Resampling is now a kernel $R_t(h_{t-1},\cdot)$ from histories, with the offspring identity for every history. This covers the draft's rules, which look at particle values (sorted systematic, for example). The proofs are unchanged in substance: the factorisation uses only that both runs evaluate the same kernel on the same history, and Lemma 3 uses only the conditional expected offspring counts. (Finding 3.)
3. **Remark 2.1.** Acceptance rates are removed from the list of functions on $\Omega$, with a note on the augmented trajectory under which they are covered. (Finding 6.)
4. **Remark 4.1.** The exponential start mass is stated for $\mathcal M=\{S_0\}$ (or any $\mathcal M\ni S_0$ excluding $\tilde S_0$ with start mass $e^{-\Theta(n)}$) and $\kappa_0>0$; the polynomial case $\kappa_0=0$ is noted. (Finding 4.)
5. **Remark 5.1.** The stale reference to multinomial resampling in the statement is dated; concentration around $Z\rho$ needs (5.1). (Finding 4; draft-consistency note.)
6. **Section 6.1.** The design $\mathsf D_t$ includes the resampling kernel. The empirical-ESS termination bound is corrected to $\delta_{\min}=\min\{1,\min\delta^\ast\}$ and $T\le\max\{1,\lceil1/\delta_{\min}\rceil\}$. (Findings 3, 5.)
7. **Section 6.2, item 5 and proof (5).** The adaptive leaky bound is $P^{\rm ad}(\mathcal A)\le N\{q_0(\mathcal M)+\eta\,\mathbb E\sum_{t\le T}m_t\}$ (or with a deterministic cap $\bar m$), under leakage $\le\eta$ for every kernel the rule can choose in place of (NC). It is proved in full, with Sol's counterexample to the verbatim form. (Finding 1, FATAL in the draft's wording.)
8. **Section 6.2, items 3 and (3).** The failure of $\mathbb E[\widehat Z]=Z$ under (NC)–(F) now cites Example 6.4. (Finding 2.)
9. **Remark 6.1.** The self-contradictory phrase "$\mathcal G_{t-1}$-measurable functions chosen independently of the particles" is replaced by "fixed in advance". (Exposition.)
10. **Section 6.3.** Example 6.3 is labelled as outside the non-crossing class, with the martingale argument showing that no two-state compliant example exists. **New Example 6.4** is Sol's three-state in-class example, with $\mathbb E[\widehat Z]/Z\to B/A\approx0.85026$. (Finding 2.)
11. **Section 7.** The table row for the adaptive theorem, the (H1) item and the list of unsure steps are updated.

Checks: `check_T5.py` rerun unchanged (`proofs/_audit/group_B/rerun_check_T5.out`): frozen-schedule check $\mathbb E[\widehat Z\mid E]$ predicted $1.86357$, observed $1.86351$ (se $0.00009$); Example 6.3 exact ratio $0.85026$, Monte Carlo $3.5660$ (se $0.0021$) against exact $3.5664$. New checks T5.F1, T5.F2, T5.F3 and T5.F5 in `proofs/_audit/group_B/check_audit_B.py` all PASS. They include exact enumeration of Proposition 2 and (iii) under value-sorted systematic resampling ($N=3$, four states): the law of $(\Pi_T,X_T)$ given $E$ matches the restricted run to total variation $3\cdot10^{-14}$.

12. **After Sol's confirmation (exchange 1).** Sol confirmed every change and gave the verdict VERIFIED for the corrected statement. Its residual edits were applied: (6.1) and the adaptive restricted-run definition now use the selected kernel $R_s(h_{s-1},\cdot)$ (they still had $R_N$); "no compliant instance exists" became "no biased compliant example exists"; the martingale argument conditions on $U$; the limit is written $B/Approx0.85026$. These edits were not re-sent for confirmation.
