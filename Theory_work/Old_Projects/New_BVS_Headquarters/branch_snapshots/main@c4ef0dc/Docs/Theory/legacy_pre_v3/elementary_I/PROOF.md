# Proofs of Proposition P1, Theorem T1 and Lemmas L1, L2, L3, L7, L5

Supplement material for *Split-and-merge with an exact merge: composite-start sequential Monte Carlo for Bayesian variable selection*, draft of 14 October 2026. Thread: elementary_I. Prover: Fable 5.1 (lead), 14 October 2026. Version 4 (after review rounds 1 to 3: three Opus and three Astra blind reviewers per round; rulings in FINDINGS.md; v1 kept as review/PROOF.md, v2 and v3 as review/PROOF_v2.md and review/PROOF_v3.md; v4 differs from the reviewed v3 by wording only). Notation follows Section 2 of the draft. Assumed: Lemma L4 (used only in Section 0.1, for the well-definedness, strict increase and termination of the greedy schedule, and through Section 0.1 in Sections 7 and 8; the stage bounds proved there give termination independently under their own hypotheses), standard linear algebra and standard probability. No other numbered result of the draft is used. Numerical sanity checks of the identities and of the examples are in `check_elementary_I.py` beside this file (single seed `default_rng(1)`, local; output in `check_elementary_I.out`, 36 checks, 36 pass); they are not part of the proofs.

**Summary of the outcome.** All seven results are true as stated, under the readings fixed in Section 0.3. The readings do three things: they fix conventions the draft leaves implicit (block order of columns; empty models and blocks; a cap above $p$), they restrict two side sentences to the non-degenerate cases in which they are true (P1's "not a product" sentence, read as the absence of any factorisation over blocks, needs $k_{\max}\ge1$ and at least two blocks, while its literal reading holds for every beta-binomial prior with $p\ge2$; L7's consequence needs $\delta>0$), and they read the complexity sentence of P1 as an arithmetic count. None affects the displayed identities and bounds; all are flagged where they occur and listed in Section 9. Remarks that comment on the draft's other results (T2, Assumption Regime (a)) are orientation only and are not claims proved here. What the proofs add:

- **P1.** The procedure of (ii) is well defined (every normaliser it divides by is positive on the paths it can take), and it draws exactly from $\pi_0$ (Theorem 2.3). The arithmetic cost is stated precisely as a set-up cost $O(\sum_b2^{|C_b|}+L\,k_{\max}B)$ plus a per-draw cost $O(k_{\max}+p)$ after an $O(\sum_b2^{|C_b|})$ preprocessing, for every cap including $k_{\max}=0$ (Proposition 2.4). The "not a product" sentence is proved as a precise statement: for $\mathrm{BB}(1,p)$ with $p\ge2$, at least two blocks and $k_{\max}\ge1$, $\pi_0$ is not a product over blocks for any tables (Proposition 2.6).
- **T1.** Proved by direct substitution after one bookkeeping convention (block ordering of the columns of $X_S$, Section 1.2). The claim "$x_\Sigma<1$ is not automatic" is witnessed by the instance $n=4$ with both columns equal to $y=\mathbf 1_4$, $b_0=0.01$, where $x_\Sigma=1.516$ (Example 3.3). In (iii) the equality case is characterised: under block-orthogonality $d(S)=0$ if and only if $y$ is orthogonal to the columns of all but at most one block of $S$ (Theorem 3.4).
- **L1.** Both bounds hold. The first bound is only meaningful with $\varphi^2(S)>0$, and its $O(|S|/n)$ reading over a family of models follows once $\varphi^2(S)\ge\varphi_0^2>0$ *uniformly over that family* (a sufficient condition): two identical columns in different blocks give $\Delta_{\det}(S)=\tfrac12\log n+o(1)$, so without such a bound the second (logarithmic) bound is sharp up to a factor $2$ (Remark 4.3). A slightly sharper first bound is recorded (4.2). In addition, the determinant term is never negative: $\Delta_{\det}(S)\ge0$, with equality if and only if $S$ is block-orthogonal (Theorem 4.4, pointed out by two reviewers); so the determinant part of the discrepancy also works against the start ($d(S)\ge\nu\Psi(S)$ for every $S$), by at most the L1 bounds.
- **L2.** Both bounds hold; in fact $\|M\|<\kappa$ strictly whenever the off-block part is nonzero. The $O(n\kappa)$ reading of $\nu\Psi_{\rm off}$ needs, besides $\kappa\le\kappa_0<1$, the residual fractions $1-x_\Sigma(S)$ and $1-x(S)$ bounded below by some $\eta>0$; then $\nu|\Psi_{\rm off}(S)|\le\frac{\nu\kappa}{(1-\kappa_0)\eta}$ (Corollary 5.3). Also $\kappa(S)<1$ forces $G_S\succ0$.
- **L3.** Holds; the hypothesis $p(S^\ast)>0$ (with the positive tables, equivalently $|S^\ast|\le k_{\max}$) is exactly what is needed and cannot be dropped (Remark 6.4). The proof gives more: $\log O_\phi$ is convex on $\mathbb R$, so for every interval $[\phi_a,\phi_b]$, $\inf_{\phi\in[\phi_a,\phi_b]}q_\phi(S^\ast)=\min\{q_{\phi_a}(S^\ast),q_{\phi_b}(S^\ast)\}$ (Theorem 6.2). The "hence" clause holds for deterministic convergence, convergence in probability and almost sure convergence alike.
- **L7.** The identity holds for all real $\phi$ and $\delta$ (not only $\delta\ge0$), and the consequence needs $\delta>0$. By Theorem 6.2 the hypothesis "for all $\psi\in[0,1+\delta]$" reduces to the two endpoint conditions $\pi_0(S^\ast)\ge(1+c)^{-1/2}$ and $q_{1+\delta}(S^\ast)\ge(1+c)^{-1/2}$ (Corollary 7.3), which is the form T2(iii) should use.
- **L5.** Holds as stated, with the greedy schedule read as in the draft (supremum attained, by L4). The bound $\Lambda\le\sigma_d$ uses that local sub-Gaussianity on $\lambda\in(0,2\lambda_0]$ already implies $\mathrm{Var}_{q_\phi}(d)\le\sigma_d^2$ (Lemma 8.2).

Section 9 lists the hypotheses added and the flags for the draft.

---

## 0. Setting, conventions and the frozen statements

### 0.1 The model space, the prior weights and the bridge

Throughout, $p\ge1$ and $n\ge1$. A model is $S\subseteq[p]$ and $k=|S|$. The blocks $C_1,\dots,C_L$ ($L\ge1$) form a partition of $[p]$ into nonempty sets, $|C_b|\le B$, and $S_b=S\cap C_b$. The size weights are numbers $w(k)>0$, $0\le k\le p$, and the cap is an integer with $0\le k_{\max}\le p$. (A cap larger than $p$ is the same as $k_{\max}=p$, since no model has more than $p$ elements; we therefore replace $k_{\max}$ by $\min\{k_{\max},p\}$ throughout, which avoids evaluating $w(k)$ at $k>p$; the draft's beta-binomial formula $B(\alpha_\pi+k,\beta_\pi+p-k)/B(\alpha_\pi,\beta_\pi)$ has a pole at every $k\ge\beta_\pi+p$ when $\beta_\pi$ is an integer, i.e. at $k\ge2p$ for $\mathrm{BB}(1,p)$, which the operational cap $\lfloor n/2\rfloor$ reaches when $n\ge4p$, and for non-integer $\beta_\pi$ it is finite but not a meaningful weight for $k>p$ (it can be negative); that cap exceeds $p$ as soon as $n\ge2p+2$; so this normalisation should be stated in the draft too.) $W>0$ is a constant (in the draft $W=\sum_{k\le k_{\max}}\binom pkw(k)$, but nothing below uses its value). The model prior is $p(S)=W^{-1}w(|S|)\mathbf 1\{|S|\le k_{\max}\}$, and
$$
\mathcal S=\{S\subseteq[p]:|S|\le k_{\max}\}=\{S:p(S)>0\}
$$
is the support of the prior, a nonempty finite set ($\emptyset\in\mathcal S$). Block tables are functions $r_b:2^{C_b}\to(0,\infty)$; $r(S)=\prod_br_b(S_b)$, $\gamma_0(S)=p(S)r(S)$, $\bar Z_0=\sum_S\gamma_0(S)$ and $\pi_0=\gamma_0/\bar Z_0$. Since $\gamma_0>0$ exactly on $\mathcal S$, $\pi_0$ is a probability on $\mathcal S$ with full support, and every sum "over $S$" in the draft is a sum over $\mathcal S$ (terms off $\mathcal S$ vanish).

For a function $d:\mathcal S\to\mathbb R$ and $\phi\in\mathbb R$,
$$
\gamma_\phi(S)=\gamma_0(S)e^{\phi d(S)},\qquad \bar Z_\phi=\sum_{S\in\mathcal S}\gamma_\phi(S)\in(0,\infty),\qquad q_\phi=\gamma_\phi/\bar Z_\phi,\qquad F(\phi)=\log\bar Z_\phi .
$$
Thus $q_\phi(S)>0$ for every $S\in\mathcal S$ and every real $\phi$, and $q_0=\pi_0$. When $d$ is the discrepancy of Section 1.3 below, $\gamma_1=\gamma_0e^{d}=p\,r\cdot\mathrm{BF}/r=p\,\mathrm{BF}=p\,m/m(\emptyset)$, so $q_1=\gamma_1/\bar Z_1=p\,m/\sum_Sp(S)m(S)=\pi$ and $Z=m(\emptyset)\bar Z_1$. In Sections 6 to 8, which are stated for an abstract pair $(\gamma_0,d)$, the symbol $\pi$ means $q_1$. Sections 6 to 8 use only this abstract structure (an arbitrary positive $\gamma_0$ and an arbitrary real $d$ on a finite set), which is the generality in which the draft states L3, L7 and L5. For a probability $q$ on $\mathcal S$ and $f:\mathcal S\to\mathbb R$, $q(f)=\mathbb E_q f=\sum_Sq(S)f(S)$ and $\mathrm{Var}_q(f)=q(f^2)-q(f)^2$, $\mathrm{sd}_q(f)=\mathrm{Var}_q(f)^{1/2}$. The chi-square divergence of probabilities $q',q$ on $\mathcal S$ with $q>0$ is $\chi^2(q'\|q)=\sum_Sq'(S)^2/q(S)-1\ge0$ (Cauchy–Schwarz). The path length is $\Lambda=\int_0^1\mathrm{sd}_{q_\phi}(d)\,d\phi$; the integrand is continuous in $\phi$ (a finite combination of exponentials), so the integral exists.

**The greedy schedule.** For a threshold $\rho\in(0,1)$ put $c=\rho^{-1}-1>0$ (the draft uses the letter $c$ both for this threshold and for the convolution sequence $c=c^{(L)}$ of P1; we keep both; the sequence appears in the statement of P1 (Section 0.3) and in Section 2, the threshold in (0.1) below, in the statements of L7 and L5 (Section 0.3) and in Sections 7 to 9, and the two are told apart by context. Likewise, following the draft, $\rho$ is the ESS threshold and $\rho_b$ a block profile; $\delta$ is a step of the bridge and $\delta(S)$ the off-block term; $T$ is the stage count and $T,T_b$ are subsets of blocks; $B$ is the block-size bound and $B(\cdot,\cdot)$ the beta function; each pair is told apart by its arguments or indices, and the stage count $T$ from a subset $T$ by context), $\phi_0=0$ and, while $\phi_{t-1}<1$,
$$
\phi_t=\sup\{\phi\in(\phi_{t-1},1]:\chi^2(q_\phi\|q_{\phi_{t-1}})\le c\}. \tag{0.1}
$$
The set in (0.1) is nonempty (its elements near $\phi_{t-1}$ have $\chi^2\to0$ by continuity), so $\phi_t\in(\phi_{t-1},1]$. By L4(iii), which we assume, the supremum is attained, $\phi_t>\phi_{t-1}$, and the schedule reaches $1$; $T=\min\{t:\phi_t=1\}$. Sections 7 and 8 use (0.1) only through the following trivial consequence: *if $\phi'\in(\phi_{t-1},1]$ satisfies $\chi^2(q_{\phi'}\|q_{\phi_{t-1}})\le c$, then $\phi_t\ge\phi'$.*

### 0.2 The regression quantities

$X\in\mathbb R^{n\times p}$ is fixed, $y\in\mathbb R^n$. For $S\neq\emptyset$ with columns listed in some order, $X_S\in\mathbb R^{n\times k}$, $G_S=X_S^\top X_S\succeq0$, $z_S=X_S^\top y$, $H_S=(n+1)G_S+I_k\succ0$,
$$
D_S=\frac{\det H_S}{\det(G_S+I_k)},\qquad t_S=n\,z_S^\top H_S^{-1}z_S,\qquad Q_S=y^\top y-t_S,\qquad \nu=a_0+\tfrac n2,
$$
with $a_0,b_0>0$. For $S=\emptyset$: $D_\emptyset=1$, $t_\emptyset=0$ (empty matrices; equivalently, the formulas with $k=0$). The marginal likelihood is *defined* by the draft's display (eq:m),
$$
m(S)=C_n\,D_S^{-1/2}(2b_0+Q_S)^{-\nu},\qquad C_n=\pi^{-n/2}(2b_0)^{a_0}\Gamma(\nu)/\Gamma(a_0),
$$
and $A_0=2b_0+y^\top y$, $\mathrm{BF}(S)=m(S)/m(\emptyset)$. (That (eq:m) is the integral of the Gaussian likelihood against the stated priors is not part of any statement proved here; it is verified by quadrature in check C0 of the script. The standardisation $\|x_j\|^2=n$ is never used in the proofs; the examples of Sections 3 and 4 use standardised columns only so that they are admissible designs for the draft.)

### 0.3 The statements, as frozen from the draft

**Proposition P1 (exact composite start).** Let $r_b:2^{C_b}\to(0,\infty)$ be arbitrary positive tables. Let $w$ be per-model size weights with cap $k_{\max}$, and set $\gamma_0(S)=W^{-1}w(|S|)\mathbf 1\{|S|\le k_{\max}\}\prod_br_b(S_b)$. Define the block size profiles $\rho_b(j)=\sum_{T\subseteq C_b,|T|=j}r_b(T)$; the partial convolutions $c^{(b)}=\rho_1*\dots*\rho_b$, with $c^{(0)}_j=\mathbf 1\{j=0\}$; and $c=c^{(L)}$. All out-of-range coefficients are zero.
(i) $\bar Z_0=W^{-1}\sum_{k=0}^{k_{\max}}w(k)c_k$. No additional binomial factor appears.
(ii) Consider the procedure: (a) draw $K$ with $\mathbb P(K=k)\propto w(k)c_k$; (b) given $K=k$, draw block sizes backwards for $b=L,\dots,1$: $\mathbb P(J_b=j\mid J_{b+1},\dots,J_L)\propto\rho_b(j)\,c^{(b-1)}_{k-j-\sum_{b'>b}J_{b'}}$; (c) draw $T_b\subseteq C_b$ with $|T_b|=J_b$ with probability $r_b(T_b)/\rho_b(J_b)$, independently over $b$. Then $S=\bigcup_bT_b$ has law exactly $\pi_0$. Given the tables, the arithmetic cost is $O(\sum_b2^{|C_b|}+Lk_{\max}B)$. Building the tables costs $\sum_b2^{|C_b|}$ marginal-likelihood evaluations.
(iii) (Size-tilted marginals.) Let $c^{(-b)}=\ast_{b'\ne b}\rho_{b'}$. For $T\subseteq C_b$, $\pi_0(S_b=T)=r_b(T)\sum_{k\le k_{\max}}w(k)c^{(-b)}_{k-|T|}\big/\sum_{k\le k_{\max}}w(k)c_k$. Conditional on $|S|=k$, the block configurations are independent block draws $r_b(\cdot)/\sum_Tr_b(T)$, conditioned on $\sum_b|S_b|=k$.
In particular, under a BB prior $\pi_0$ is not a product of independent block posteriors; it is a size-coupled product.
*Readings.* In (a), $k$ ranges over $\{0,\dots,k_{\max}\}$. "Arithmetic cost" is the number of arithmetic operations and table look-ups, the tables $r_b$ being given; it covers the set-up (profiles and convolutions) and one draw. The last sentence is read as Proposition 2.6.

**Theorem T1 (discrepancy identity).** With $r_b(T)=\mathrm{BF}(T)$ for $T\subseteq C_b$, $d(S)=\log\mathrm{BF}(S)-\log r(S)$, $x_b(S)=t_{S_b}/A_0$, $x(S)=t_S/A_0$, $G_{S,0}=\mathrm{blockdiag}_b(G_{S_b})$, $H_{S,0}=(n+1)G_{S,0}+I$ and $\delta(S)=n\,z_S^\top(H_{S,0}^{-1}-H_S^{-1})z_S$. For every model $S$:
(i) $t_S=\sum_bt_{S_b}-\delta(S)$, and $d(S)=\Delta_{\det}(S)+\nu\Psi(S)$ with $\Delta_{\det}(S)=\tfrac12[\sum_b\log D_{S_b}-\log D_S]$ and $\Psi(S)=\sum_b\log(1-x_b(S))-\log(1-x(S))$.
(ii) On the event $x_\Sigma(S):=\sum_bx_b(S)<1$, $\Psi=\Psi_{\rm sh}+\Psi_{\rm off}$ with $\Psi_{\rm sh}(S)=\sum_b\log(1-x_b)-\log(1-\sum_bx_b)\ge0$ and $\Psi_{\rm off}(S)=\log(1-x_\Sigma)-\log(1-x_\Sigma+\delta(S)/A_0)$. Here $\Psi_{\rm sh}(S)=0$ if and only if at most one $x_b(S)$ is positive. The condition $x_\Sigma<1$ is not automatic: separately fitted blocks can jointly "explain" more than $y^\top y$.
(iii) If $S$ is block-orthogonal ($X_{S_b}^\top X_{S_{b'}}=0$ for $b\ne b'$), then $\Delta_{\det}(S)=0$, $\delta(S)=0$, $x_\Sigma(S)=x(S)<1$ and $d(S)=\nu\Psi_{\rm sh}(S)\ge0$.
*Reading.* $G_S$, $z_S$ and $H_S$ are taken with the columns of $X_S$ in block order (Section 1.2); $t_S$, $D_S$ and $d(S)$ do not depend on the order.

**Lemma L1 (determinant term).** Let $\varphi^2(S)=\lambda_{\min}(G_S)/n>0$. Then $|\Delta_{\det}(S)|\le|S|/(2n\varphi^2(S))$, and always $|\Delta_{\det}(S)|\le\tfrac{|S|}2\log(n+1)$.

**Lemma L2 (off-block term).** Assume $G_{S,0}\succ0$ and let $\kappa(S)=\|G_S-G_{S,0}\|_{\rm op}/\lambda_{\min}(G_{S,0})$. If $\kappa(S)<1$, then $|\delta(S)|\le\frac{\kappa(S)}{1-\kappa(S)}\sum_bt_{S_b}$. If moreover $x_\Sigma(S)<1$, then $|\Psi_{\rm off}(S)|\le\frac{\kappa}{1-\kappa}\cdot\frac{x_\Sigma(S)}{\min\{1-x_\Sigma(S),\,1-x(S)\}}$.

**Lemma L3 (concentration propagates along the bridge).** For any model $S^\ast$ with $p(S^\ast)>0$ and any $\phi\in[0,1]$, let $O_\phi=(1-q_\phi(S^\ast))/q_\phi(S^\ast)$. Then $O_\phi\le O_0^{1-\phi}O_1^\phi\le\max\{O_0,O_1\}$. Hence if $\pi_0(S^\ast)\to1$ and $\pi(S^\ast)\to1$, then $\inf_{\phi\in[0,1]}q_\phi(S^\ast)\to1$.

**Lemma L7 (single-model identity for $\chi^2$).** For every model $S^\ast$ with $p(S^\ast)>0$, every $\phi\in\mathbb R$ and every $\delta\ge0$,
$$
1+\chi^2(q_{\phi+\delta}\|q_\phi)=\frac{\bar Z_{\phi+2\delta}\bar Z_\phi}{\bar Z_{\phi+\delta}^2}=\frac{q_{\phi+\delta}(S^\ast)^2}{q_\phi(S^\ast)\,q_{\phi+2\delta}(S^\ast)}\le\frac1{q_\phi(S^\ast)\,q_{\phi+2\delta}(S^\ast)} .
$$
Consequently, suppose $q_\psi(S^\ast)\ge(1+c)^{-1/2}$ for all $\psi\in[0,1+\delta]$. Then every greedy step that does not end at $\phi=1$ has length at least $\delta$, and $T\le\lceil1/\delta\rceil$. No moment condition is needed.
*Reading.* In the consequence, $\delta>0$ (for $\delta=0$ the conclusion is empty).

**Lemma L5 (stage count under local sub-Gaussianity).** Suppose there are $\sigma_d>0$ and $\lambda_0>0$ such that, for all $\phi\in[0,1]$ and $\lambda\in[0,2\lambda_0]$, $\log\mathbb E_{q_\phi}\exp\{\lambda(d-\mathbb E_{q_\phi}d)\}\le\lambda^2\sigma_d^2/2$. Then each greedy step satisfies $\phi_t-\phi_{t-1}\ge\min\{\lambda_0,\sqrt{\log(1+c)/2}/\sigma_d,1-\phi_{t-1}\}$. Hence $T\le\lceil\max\{1/\lambda_0,\sigma_d\sqrt{2/\log(1+c)}\}\rceil$ and $\Lambda\le\sigma_d$.

---

## 1. Preliminaries

### 1.1 Elementary properties of $t_S$ and $D_S$

**Lemma 1.1.** For every $S$: (a) $t_S$ and $D_S$ are unchanged when the columns of $X_S$ are permuted; (b) $0\le t_S\le\frac n{n+1}\|P_Sy\|^2\le\frac n{n+1}y^\top y$, where $P_S$ is the orthogonal projection onto the column span of $X_S$; (c) $0\le t_S\le\frac n{n+1}y^\top y<A_0$, so $x(S)=t_S/A_0\in[0,\frac n{n+1})\subset[0,1)$ and $\mathrm{BF}(S)=D_S^{-1/2}(1-x(S))^{-\nu}$; (d) $t_S=0$ if and only if $z_S=0$, i.e. $X_S^\top y=0$; (e) $D_S\ge1$.

*Proof.* (a) A permutation $\Pi$ of the columns replaces $G_S$ by $\Pi^\top G_S\Pi$, $H_S$ by $\Pi^\top H_S\Pi$ and $z_S$ by $\Pi^\top z_S$; determinants and the quadratic form $z^\top H^{-1}z$ are invariant.
(b) $t_S=y^\top A y$ with $A=nX_SH_S^{-1}X_S^\top\succeq0$ (as $H_S\succ0$), so $t_S\ge0$. Let $G_S=U\,\mathrm{diag}(\lambda_i)\,U^\top$ be a spectral decomposition, $\lambda_i\ge0$. Then $H_S^{-1}=U\,\mathrm{diag}(((n+1)\lambda_i+1)^{-1})U^\top$ and, with $V=X_SU$ (columns $v_i$, $\|v_i\|^2=\lambda_i$, mutually orthogonal), $A=\sum_i\frac{n}{(n+1)\lambda_i+1}v_iv_i^\top$. Hence $y^\top Ay=\sum_{i:\lambda_i>0}\frac{n\lambda_i}{(n+1)\lambda_i+1}\,\frac{(v_i^\top y)^2}{\lambda_i}\le\frac n{n+1}\sum_{i:\lambda_i>0}\frac{(v_i^\top y)^2}{\|v_i\|^2}=\frac n{n+1}\|P_Sy\|^2$, because $n\lambda/((n+1)\lambda+1)<n/(n+1)$ for $\lambda>0$, the nonzero $v_i$ form an orthogonal basis of the column span of $X_S$, and $\|P_Sy\|^2\le\|y\|^2$.
(c) From (b), $t_S\le\frac n{n+1}y^\top y<y^\top y+2b_0=A_0$ (also when $y=0$, as $b_0>0$), and $t_S/A_0\le\frac n{n+1}y^\top y/A_0<\frac n{n+1}$. Then $m(S)/m(\emptyset)=D_S^{-1/2}\big((2b_0+y^\top y-t_S)/A_0\big)^{-\nu}=D_S^{-1/2}(1-t_S/A_0)^{-\nu}$, using $D_\emptyset=1$, $t_\emptyset=0$.
(d) $H_S^{-1}\succ0$, so $z_S^\top H_S^{-1}z_S=0$ iff $z_S=0$.
(e) In the eigenbasis of $G_S$, $D_S=\prod_i\frac{(n+1)\lambda_i+1}{\lambda_i+1}\ge1$ since each factor is $\ge1$. $\square$

### 1.2 Block ordering and the block-diagonal part

Fix a model $S$ with $S_b=S\cap C_b$. *Block order* lists the columns of $X_S$ block by block, $X_S=[X_{S_1}\ X_{S_2}\ \cdots\ X_{S_L}]$ (empty blocks contribute no columns; within a block, in increasing index). By Lemma 1.1(a) the choice of order does not affect $t_S$, $D_S$, $Q_S$, $m(S)$ or $\mathrm{BF}(S)$, and we use block order whenever $G_S$ is compared with the block-diagonal matrix $G_{S,0}=\mathrm{blockdiag}_b(G_{S_b})$ (which is only defined in block order). In block order,
$$
G_S=\begin{pmatrix}G_{S_1}&X_{S_1}^\top X_{S_2}&\cdots\\ X_{S_2}^\top X_{S_1}&G_{S_2}&\cdots\\ \vdots&\vdots&\ddots\end{pmatrix},\qquad z_S=\begin{pmatrix}z_{S_1}\\ z_{S_2}\\ \vdots\end{pmatrix},\qquad G_{S,0}=\mathrm{blockdiag}_b(G_{S_b}),
$$
and $E_S:=G_S-G_{S,0}$ is the symmetric matrix of off-block Gram cross-products $X_{S_b}^\top X_{S_{b'}}$, $b\ne b'$.

**Lemma 1.2.** In block order, $H_{S,0}=(n+1)G_{S,0}+I_k=\mathrm{blockdiag}_b(H_{S_b})\succ0$, and
$$
n\,z_S^\top H_{S,0}^{-1}z_S=\sum_bt_{S_b},\qquad \det H_{S,0}=\prod_b\det H_{S_b},\qquad \det(G_{S,0}+I_k)=\prod_b\det(G_{S_b}+I_{|S_b|}),
$$
where blocks with $S_b=\emptyset$ contribute $t_\emptyset=0$ and empty determinants equal $1$.

*Proof.* The identity matrix is block diagonal with the same block structure, so $H_{S,0}$ is block diagonal with blocks $(n+1)G_{S_b}+I=H_{S_b}$; its inverse is $\mathrm{blockdiag}_b(H_{S_b}^{-1})$, and a block-diagonal quadratic form splits as $z_S^\top H_{S,0}^{-1}z_S=\sum_bz_{S_b}^\top H_{S_b}^{-1}z_{S_b}$. Determinants of block-diagonal matrices are products of the block determinants. $\square$

### 1.3 The discrepancy for the paper's tables

With $r_b(T)=\mathrm{BF}(T)$, Lemma 1.1(c) gives, for every $S$ (empty blocks contributing $0$),
$$
\log r(S)=\sum_b\log\mathrm{BF}(S_b)=\sum_b\Big[-\tfrac12\log D_{S_b}-\nu\log(1-x_b(S))\Big],\qquad \log\mathrm{BF}(S)=-\tfrac12\log D_S-\nu\log(1-x(S)). \tag{1.1}
$$

---

## 2. Proposition P1: the exact composite start

Throughout this section the tables $r_b$ are arbitrary positive functions on $2^{C_b}$ and the weights satisfy $w(k)>0$; $W>0$. Sequences such as $\rho_b$, $c^{(b)}$, $c$, $c^{(-b)}$ are indexed by all integers, with the stated values on their natural range and $0$ elsewhere; the convolution of two such sequences is $(f*g)_k=\sum_{j\in\mathbb Z}f_jg_{k-j}$ (a finite sum), which is commutative and associative, and $c^{(0)}=\mathbf 1\{\cdot=0\}$ is its unit. Thus $c^{(b)}=c^{(b-1)}*\rho_b$ for $b\ge1$. Note $\rho_b(j)>0$ for $0\le j\le|C_b|$ and $\rho_b(j)=0$ otherwise.

**Lemma 2.1 (what the convolutions count).** For $0\le b\le L$ and every integer $k$,
$$
c^{(b)}_k=\sum_{\substack{(T_1,\dots,T_b):\ T_{b'}\subseteq C_{b'},\\ |T_1|+\dots+|T_b|=k}}\ \prod_{b'=1}^br_{b'}(T_{b'}) , \tag{2.1}
$$
an empty product being $1$ (so (2.1) at $b=0$ reads $c^{(0)}_k=\mathbf 1\{k=0\}$). In particular $c^{(b)}_k>0$ for $0\le k\le|C_1|+\dots+|C_b|$ and $c^{(b)}_k=0$ otherwise; and $c_k=c^{(L)}_k=\sum_{S\subseteq[p],|S|=k}r(S)$, which is $>0$ for $0\le k\le p$ and $0$ otherwise.

*Proof.* Induction on $b$. For $b=0$ both sides are $\mathbf 1\{k=0\}$. For $b\ge1$, split the sum in (2.1) according to $j=|T_b|$:
$$
\sum_{j}\ \sum_{T_b\subseteq C_b,|T_b|=j}r_b(T_b)\sum_{\substack{(T_1,\dots,T_{b-1}):\\ |T_1|+\dots+|T_{b-1}|=k-j}}\prod_{b'<b}r_{b'}(T_{b'})=\sum_j\rho_b(j)\,c^{(b-1)}_{k-j}=(c^{(b-1)}*\rho_b)_k=c^{(b)}_k ,
$$
by the induction hypothesis. Positivity: the sum (2.1) is nonempty exactly when $0\le k\le\sum_{b'\le b}|C_{b'}|$ (choose $T_{b'}$ of any sizes adding to $k$), and all its terms are positive. For the last claim, the map $S\mapsto(S_1,\dots,S_L)$ is a bijection from $2^{[p]}$ onto $\prod_b2^{C_b}$ (the blocks partition $[p]$), with $|S|=\sum_b|S_b|$ and $r(S)=\prod_br_b(S_b)$. $\square$

**Theorem 2.2 (P1(i)).** $\bar Z_0=W^{-1}\sum_{k=0}^{k_{\max}}w(k)c_k>0$.

*Proof.* Group the sum defining $\bar Z_0$ by size: $\bar Z_0=\sum_{k=0}^{k_{\max}}W^{-1}w(k)\sum_{|S|=k}r(S)=W^{-1}\sum_{k=0}^{k_{\max}}w(k)c_k$ by Lemma 2.1. The $k=0$ term is $W^{-1}w(0)\prod_br_b(\emptyset)>0$. No binomial coefficient appears because $c_k$ is a sum over the individual models of size $k$, each counted once with its own weight $r(S)$; a factor $\binom pk$ arises only when a size-$k$ class is replaced by its cardinality, as in the prior normaliser $W$, which is a fixed constant computed from the prior alone. $\square$

**Theorem 2.3 (P1(ii): the sampler is exact).** Let $(K,J_L,J_{L-1},\dots,J_1,T_1,\dots,T_L)$ be a random vector whose law is specified sequentially by
1. $\mathbb P(K=k)=\dfrac{w(k)c_k}{\sum_{k'=0}^{k_{\max}}w(k')c_{k'}}$ for $k\in\{0,\dots,k_{\max}\}$;
2. for $b=L,L-1,\dots,1$, with $m_b:=K-\sum_{b'>b}J_{b'}$,
$$
\mathbb P(J_b=j\mid K,J_{b+1},\dots,J_L)=\frac{\rho_b(j)\,c^{(b-1)}_{m_b-j}}{\sum_{j'}\rho_b(j')\,c^{(b-1)}_{m_b-j'}}=\frac{\rho_b(j)\,c^{(b-1)}_{m_b-j}}{c^{(b)}_{m_b}},\qquad j\in\mathbb Z ; \tag{2.2}
$$
3. given $(K,J_1,\dots,J_L)$, the sets $T_1,\dots,T_L$ are conditionally independent with $\mathbb P(T_b=T\mid K,J)=r_b(T)\mathbf 1\{|T|=J_b\}/\rho_b(J_b)$ for $T\subseteq C_b$.

Then: (a) every denominator in 1 to 3 is strictly positive on every path the procedure can take, so the law is well defined; (b) almost surely $0\le J_b\le|C_b|$ for every $b$ and $\sum_bJ_b=K$; (c) $S:=\bigcup_bT_b$ satisfies $\mathbb P(S=s)=\pi_0(s)$ for every $s\subseteq[p]$.

*Proof.* (a) and (b). The law is constructed stage by stage; at each stage we check that the next conditional law is well defined on the support of what has been built so far (on the complement, a null set, it may be defined arbitrarily). The denominator in 1 is $W\bar Z_0>0$ (Theorem 2.2), so the law of $K$ is well defined, and it is supported on $\{k:c_k>0\}$, i.e. $c^{(L)}_{m_L}=c^{(L)}_K>0$ on the support. The two denominators in (2.2) agree because $\sum_j\rho_b(j)c^{(b-1)}_{m-j}=(c^{(b-1)}*\rho_b)_m=c^{(b)}_m$. Now let $b\in\{L,\dots,1\}$ and suppose the law of $(K,J_L,\dots,J_{b+1})$ has been built and is supported on histories with $c^{(b)}_{m_b}>0$. On that support, (2.2) is a well-defined probability on $\mathbb Z$ (finitely many nonzero terms, positive total $c^{(b)}_{m_b}$), and it gives positive probability only to values $j$ with $\rho_b(j)c^{(b-1)}_{m_b-j}>0$, hence with $0\le j\le|C_b|$ and $c^{(b-1)}_{m_{b-1}}=c^{(b-1)}_{m_b-j}>0$; so the law of $(K,J_L,\dots,J_b)$ is built and supported on histories with $c^{(b-1)}_{m_{b-1}}>0$, which is the hypothesis for the next stage. At $b=1$, $c^{(0)}_{m_1-j}=\mathbf 1\{j=m_1\}$, so $J_1=m_1$ on the support, i.e. $\sum_bJ_b=K$. Finally $\rho_b(J_b)>0$ since $0\le J_b\le|C_b|$, so 3 is well defined, and $T_b$ is a draw with positive probabilities among the $\binom{|C_b|}{J_b}$ subsets of size $J_b$.

(c) Fix $s\subseteq[p]$ and put $t_b=s\cap C_b$, $j_b=|t_b|$, $k=|s|=\sum_bj_b$. Since the blocks partition $[p]$, the event $\{S=s\}$ equals $\{T_b=t_b\ \forall b\}$, which by (b) is contained in $\{J_b=j_b\ \forall b,\ K=k\}$. If $k>k_{\max}$ the event is impossible and $\mathbb P(S=s)=0=\pi_0(s)$. If $k\le k_{\max}$, every factor below is well defined and positive along the path of $s$: $\mathbb P(K=k)>0$ because $c_k>0$ for $0\le k\le p$ (Lemma 2.1); $m_b=\sum_{b'\le b}j_{b'}\in[0,\sum_{b'\le b}|C_{b'}|]$, so $c^{(b)}_{m_b}>0$ (Lemma 2.1); and $\rho_b(j_b)>0$ since $0\le j_b\le|C_b|$. The chain rule for the sequential specification gives
$$
\mathbb P(S=s)=\mathbb P(K=k)\prod_{b=L}^{1}\frac{\rho_b(j_b)\,c^{(b-1)}_{m_b-j_b}}{c^{(b)}_{m_b}}\prod_{b=1}^L\frac{r_b(t_b)}{\rho_b(j_b)},\qquad m_b=k-\sum_{b'>b}j_{b'} .
$$
Since $m_{b-1}=m_b-j_b$ and $m_L=k$, $m_1-j_1=0$, the middle product telescopes:
$$
\prod_{b=L}^{1}\frac{\rho_b(j_b)\,c^{(b-1)}_{m_{b-1}}}{c^{(b)}_{m_b}}=\prod_b\rho_b(j_b)\cdot\frac{c^{(0)}_0}{c^{(L)}_k}=\frac{\prod_b\rho_b(j_b)}{c_k}.
$$
Hence
$$
\mathbb P(S=s)=\frac{w(k)c_k}{W\bar Z_0}\cdot\frac{\prod_b\rho_b(j_b)}{c_k}\cdot\prod_b\frac{r_b(t_b)}{\rho_b(j_b)}=\frac{W^{-1}w(|s|)\prod_br_b(s_b)}{\bar Z_0}=\frac{\gamma_0(s)}{\bar Z_0}=\pi_0(s). \qquad\square
$$

**Proposition 2.4 (cost).** Given the tables $r_b$ as arrays indexed by the subsets of $C_b$:
(a) the profiles $\rho_b(j)$, $0\le j\le|C_b|$, cost $\sum_b2^{|C_b|}$ additions (the size $|T|$ of each table index is read off the index, at $O(1)$ amortised cost when the subsets are enumerated in Gray-code or binary order);
(b) the truncated convolutions $c^{(b)}_m$, $0\le m\le k_{\max}$, $b=1,\dots,L$, cost at most $\sum_b(k_{\max}+1)(\min\{|C_b|,k_{\max}\}+1)\le\sum_b(k_{\max}+1)(|C_b|+1)$ multiply-adds, since $c^{(b)}_m=\sum_{j=0}^{\min(|C_b|,m)}\rho_b(j)c^{(b-1)}_{m-j}$ and only indices $m\le k_{\max}$ are ever used (in Theorem 2.2, $k\le k_{\max}$; in (2.2), $m_b\le K\le k_{\max}$). Storage is $O(L(k_{\max}+1))$;
(c) one draw of $S$ costs $O(k_{\max}+1)$ operations for $K$, $O(\min\{|C_b|,k_{\max}\}+1)$ for each $J_b$ (the candidate values are $0\le j\le\min\{|C_b|,m_b\}$), and $O(2^{|C_b|})$ for each $T_b$ by a linear scan of the size-$J_b$ entries of the table, hence $O(\sum_b2^{|C_b|}+k_{\max}+\sum_b|C_b|)=O(\sum_b2^{|C_b|}+k_{\max})$ in total (as $|C_b|\le2^{|C_b|}$); after a one-time $O(\sum_b2^{|C_b|})$ preprocessing (cumulative sums of each table within each size class), a draw of $T_b$ by binary search costs $O(|C_b|)$ and a draw of $S$ costs $O(k_{\max}+p)$.
Hence set-up plus one draw cost $O\big(\sum_b2^{|C_b|}+\sum_b(k_{\max}+1)(|C_b|+1)\big)$. Since $(k_{\max}+1)(|C_b|+1)=(|C_b|+1)+k_{\max}(|C_b|+1)\le2^{|C_b|}+2k_{\max}|C_b|$ (using $|C_b|+1\le2^{|C_b|}$ and $|C_b|+1\le2|C_b|$ for $|C_b|\ge1$), the total is $O(\sum_b2^{|C_b|}+k_{\max}\sum_b|C_b|)=O(\sum_b2^{|C_b|}+k_{\max}p)\subseteq O(\sum_b2^{|C_b|}+Lk_{\max}B)$, for every $k_{\max}\ge0$ (at $k_{\max}=0$ the bound reads $O(\sum_b2^{|C_b|})$, as P1 claims) and with $B$ any upper bound on the block sizes. Building the tables $r_b(T)=\mathrm{BF}(T)=m(T)/m(\emptyset)$, $T\subseteq C_b$, requires the values $m(T)$ for the $\sum_b2^{|C_b|}$ pairs $(b,T)$; since the empty subset is shared by all blocks, these are $1+\sum_b(2^{|C_b|}-1)=\sum_b2^{|C_b|}-L+1$ distinct marginal likelihoods, at most $\sum_b2^{|C_b|}$.

*Proof.* Each count is read off the definitions and (2.2); in (b), the restriction to $m\le k_{\max}$ is justified in the statement. $\square$

**Theorem 2.5 (P1(iii)).** (a) For every $b$ and $T\subseteq C_b$,
$$
\pi_0(S_b=T)=\frac{r_b(T)\sum_{k=0}^{k_{\max}}w(k)\,c^{(-b)}_{k-|T|}}{\sum_{k=0}^{k_{\max}}w(k)\,c_k}.
$$
(b) Let $R_b=\sum_{T\subseteq C_b}r_b(T)=\sum_j\rho_b(j)$ and let $\tilde T_1,\dots,\tilde T_L$ be independent with $\mathbb P(\tilde T_b=T)=r_b(T)/R_b$. For every $k$ with $\pi_0(|S|=k)>0$ (i.e. $0\le k\le\min\{p,k_{\max}\}$) and every $(t_b)_b$ with $t_b\subseteq C_b$,
$$
\pi_0\big(S_1=t_1,\dots,S_L=t_L\ \big|\ |S|=k\big)=\mathbb P\Big(\tilde T_1=t_1,\dots,\tilde T_L=t_L\ \Big|\ \sum_b|\tilde T_b|=k\Big).
$$

*Proof.* (a) By Lemma 2.1 applied to the blocks $b'\ne b$ (the proof did not use the order of the blocks; when $L=1$ the convolution over no blocks is the unit $c^{(-b)}=\mathbf 1\{\cdot=0\}$, as at $b=0$ in Lemma 2.1), $c^{(-b)}_m=\sum\prod_{b'\ne b}r_{b'}(T_{b'})$ over families $(T_{b'})_{b'\ne b}$ with $\sum_{b'\ne b}|T_{b'}|=m$. Hence, grouping the models with $S_b=T$ by size,
$$
\sum_{S:S_b=T}\gamma_0(S)=W^{-1}\sum_{k=0}^{k_{\max}}w(k)\sum_{\substack{S:\ S_b=T,\\ |S|=k}}r_b(T)\prod_{b'\ne b}r_{b'}(S_{b'})=W^{-1}r_b(T)\sum_{k=0}^{k_{\max}}w(k)\,c^{(-b)}_{k-|T|},
$$
and dividing by $\bar Z_0=W^{-1}\sum_kw(k)c_k$ (Theorem 2.2) gives the formula; both $W^{-1}$ cancel. (If $|T|>k_{\max}$ every $c^{(-b)}_{k-|T|}$ with $k\le k_{\max}$ has a negative index and vanishes, consistent with $\pi_0(S_b=T)=0$.)
(b) $\pi_0(|S|=k)=W^{-1}w(k)c_k/\bar Z_0$ is positive iff $c_k>0$ iff $0\le k\le p$, within $k\le k_{\max}$. For such $k$ and $(t_b)$ with $\sum|t_b|=k$ (otherwise both sides are $0$), the left side is $\gamma_0(s)/\sum_{|s'|=k}\gamma_0(s')=\prod_br_b(t_b)/c_k$ with $s=\bigcup t_b$, by Lemma 2.1; the right side is $\prod_b(r_b(t_b)/R_b)\big/\sum_{(t'_b):\sum|t'_b|=k}\prod_b(r_b(t'_b)/R_b)=\prod_br_b(t_b)/c_k$, by (2.1) again. $\square$

**Proposition 2.6 (the start is not a product over blocks).** Say $\pi_0$ is a *product over blocks* if there are functions $f_b:2^{C_b}\to[0,\infty)$ with $\pi_0(S)=\prod_bf_b(S_b)$ for all $S\subseteq[p]$. (a) If $k_{\max}=0$, $\pi_0=\delta_\emptyset$ is a product. (b) Suppose $L\ge2$ and $k_{\max}\ge1$. If $\pi_0$ is a product over blocks, then $w(0)w(2)=w(1)^2$ when $k_{\max}\ge2$, and this is impossible when $k_{\max}=1$. (c) For the beta-binomial weights $w(k)=B(\alpha_\pi+k,\beta_\pi+p-k)/B(\alpha_\pi,\beta_\pi)$ with $\alpha_\pi,\beta_\pi>0$ and $p\ge2$, $w(0)w(2)\ne w(1)^2$. Hence for every beta-binomial prior, in particular $\mathrm{BB}(1,p)$, with $p\ge2$, $L\ge2$ and $k_{\max}\ge1$, $\pi_0$ is not a product over blocks, whatever the tables.
(d) (The draft's sentence, literally.) Let $\pi_0^{\rm prod}(S)=\prod_br_b(S_b)/R_b$ with $R_b=\sum_{T\subseteq C_b}r_b(T)$ be the product of the independent block posteriors. For every beta-binomial prior with $p\ge2$ (in particular $\mathrm{BB}(1,p)$), every $L\ge1$, every $k_{\max}\ge0$ and all positive tables, $\pi_0\ne\pi_0^{\rm prod}$. (For $p=1$ this can fail: $\mathrm{BB}(\alpha_\pi,\alpha_\pi)$ with $k_{\max}=1$ has $w(0)=w(1)$ and $\pi_0=\pi_0^{\rm prod}$.)
(e) (Binding cap.) If $L\ge2$ and $1\le k_{\max}<p$, then $\pi_0$ is not a product over blocks for *any* positive weights $w$.

*Proof.* (a) is clear. (b) Suppose $\pi_0=\prod_bf_b(S_b)$. Pick $i_1\in C_1$, $i_2\in C_2$ and consider the four models $S^{\epsilon_1\epsilon_2}=\{i_1\}^{\epsilon_1}\cup\{i_2\}^{\epsilon_2}$, $\epsilon\in\{0,1\}^2$ (where $A^1=A$, $A^0=\emptyset$). Their $\pi_0$-masses are $\bar Z_0^{-1}W^{-1}w(\epsilon_1+\epsilon_2)\mathbf 1\{\epsilon_1+\epsilon_2\le k_{\max}\}r_1(\{i_1\}^{\epsilon_1})r_2(\{i_2\}^{\epsilon_2})\prod_{b\ge3}r_b(\emptyset)$, and also $f_1(\{i_1\}^{\epsilon_1})f_2(\{i_2\}^{\epsilon_2})\prod_{b\ge3}f_b(\emptyset)$. The constant $\prod_{b\ge3}f_b(\emptyset)$ is positive, since otherwise $\pi_0(\emptyset)=0$, whereas $\pi_0(\emptyset)>0$. Dividing by the positive table values, there are numbers $g_1(\epsilon_1)=f_1(\{i_1\}^{\epsilon_1})/r_1(\{i_1\}^{\epsilon_1})\ge0$, $g_2(\epsilon_2)\ge0$ defined likewise, and a constant $\mathrm{const}>0$, with $w(\epsilon_1+\epsilon_2)\mathbf 1\{\epsilon_1+\epsilon_2\le k_{\max}\}=\mathrm{const}\cdot g_1(\epsilon_1)g_2(\epsilon_2)$ for all four $\epsilon$. Since $k_{\max}\ge1$, the cases $\epsilon=(0,0),(1,0),(0,1)$ give $\mathrm{const}\cdot g_1(0)g_2(0)=w(0)>0$, $\mathrm{const}\cdot g_1(1)g_2(0)=w(1)>0$ and $\mathrm{const}\cdot g_1(0)g_2(1)=w(1)>0$; multiplying the last two and dividing by the first, $\mathrm{const}\cdot g_1(1)g_2(1)=w(1)^2/w(0)$. The case $(1,1)$ then reads $w(2)\mathbf 1\{2\le k_{\max}\}=w(1)^2/w(0)>0$. For $k_{\max}=1$ the left side is $0$, a contradiction; for $k_{\max}\ge2$ it is $w(0)w(2)=w(1)^2$. (c) $w(k+1)/w(k)=\frac{B(\alpha_\pi+k+1,\beta_\pi+p-k-1)}{B(\alpha_\pi+k,\beta_\pi+p-k)}=\frac{\alpha_\pi+k}{\beta_\pi+p-k-1}$ for $0\le k<p$ (from $B(a+1,b-1)/B(a,b)=a/(b-1)$). Thus $w(0)w(2)=w(1)^2$ iff $w(2)/w(1)=w(1)/w(0)$ iff $(\alpha_\pi+1)(\beta_\pi+p-1)=\alpha_\pi(\beta_\pi+p-2)$ iff $\beta_\pi+p-1=-\alpha_\pi$, which is impossible for $\alpha_\pi,\beta_\pi>0$. (For $\mathrm{BB}(1,p)$: $w(k+1)/w(k)=(k+1)/(2p-k-1)$, and $2/(2p-2)=1/(2p-1)$ iff $p=0$.) Now apply (b).
(d) If $k_{\max}<p$, $\pi_0^{\rm prod}$ has full support on $2^{[p]}$ while $\pi_0$ vanishes on the models of size $k_{\max}+1\le p$, so they differ. If $k_{\max}=p$, then $\pi_0(S)/\pi_0^{\rm prod}(S)=\mathrm{const}\cdot w(|S|)$ for every $S$, so $\pi_0=\pi_0^{\rm prod}$ would force $w(0)=w(1)=w(2)$ (models of sizes $0,1,2$ exist as $p\ge2$), i.e. $w(1)/w(0)=w(2)/w(1)=1$; by the ratio in (c) this means $\alpha_\pi=\beta_\pi+p-1$ and $\alpha_\pi+1=\beta_\pi+p-2$, which are incompatible. (For $p=1$, $k_{\max}=1$, only $w(1)=w(0)$ is required, which holds when $\alpha_\pi=\beta_\pi$.)
(e) Suppose $\pi_0=\prod_bf_b(S_b)$ with $L\ge2$ and $1\le k_{\max}<p$, and let $U_b=\{T\subseteq C_b:f_b(T)>0\}$. The support of the product is $\{S:S_b\in U_b\ \forall b\}$, and it must equal the support of $\pi_0$, which is $\{S:|S|\le k_{\max}\}$. Every $T\subseteq C_b$ with $|T|\le k_{\max}$ is itself a model of size $\le k_{\max}$, so $T=T_b\in U_b$. Now choose $S$ with $|S_b|=\min\{|C_b|,k_{\max}\}$ for every $b$. Each $S_b\in U_b$, so $S$ lies in the product support; but $|S|=\sum_b\min\{|C_b|,k_{\max}\}\ge k_{\max}+1$: if some block has $|C_b|\ge k_{\max}$ it contributes $k_{\max}$ and any other block (there is one, $L\ge2$, and blocks are nonempty) contributes at least $1$; otherwise all $|C_b|<k_{\max}$ and $|S|=\sum_b|C_b|=p>k_{\max}$. So $\pi_0(S)=0$ while the product is positive at $S$, a contradiction. $\square$

*Remark 2.7.* Proposition 2.6(b) shows what "size-coupled" means. The argument of (b), run over all pairs $(j_1,j_2)$ with $0\le j_1\le|C_1|$, $0\le j_2\le|C_2|$ (take $T_1\subseteq C_1$ of size $j_1$, $T_2\subseteq C_2$ of size $j_2$, other blocks empty), shows that if $\pi_0$ is a product over blocks and $k_{\max}\ge|C_1|+|C_2|$, then $w(j_1+j_2)=\mathrm{const}\cdot\tilde g_1(j_1)\tilde g_2(j_2)$ for all such pairs, with $\tilde g_b(j)=f_b(T_b^{(j)})/r_b(T_b^{(j)})$ for a fixed representative $T_b^{(j)}\subseteq C_b$ of each size $j$. Hence, for $j_2<|C_2|$, $w(j_1+j_2+1)/w(j_1+j_2)=\tilde g_2(j_2+1)/\tilde g_2(j_2)$ does not depend on $j_1$, and for $j_1<|C_1|$ it equals $\tilde g_1(j_1+1)/\tilde g_1(j_1)$, which does not depend on $j_2$; so both ratios equal one constant $\theta_0$, and $w(k+1)/w(k)=\theta_0$ for $0\le k<|C_1|+|C_2|$: the size weights must be geometric on that range. For $L\ge3$ and $k_{\max}\ge p$, repeat the argument with the other blocks held at fixed subsets of total size $s$: the factors $\tilde g_1,\tilde g_2$ are unchanged (only the constant absorbs the other blocks, through $\prod_{b\ge3}f_b(T_b^0)/r_b(T_b^0)$, which is positive because $\pi_0>0$ on every model when there is no cap), so the same $\theta_0$ is the ratio on every window $[s,s+|C_1|+|C_2|)$, $0\le s\le\sum_{b\ge3}|C_b|$, hence on all of $[0,p)$: without a cap, only geometric weights can give a product. For geometric weights $w(k)=\theta^k$ without a cap (the independent-Bernoulli prior), $\pi_0(S)\propto\prod_b\theta^{|S_b|}r_b(S_b)$ is indeed a product over blocks. Conversely, the generating-function identity behind Lemma 2.1, $\sum_kc_kz^k=\prod_b\sum_j\rho_b(j)z^j$, shows that $\pi_0$ *conditioned on the size* is always the law of independent block draws *conditioned on their total size* (Theorem 2.5(b)); the conditioned blocks are of course dependent in general (two singleton blocks with unit tables, given $|S|=1$: each is included with probability $\tfrac12$, both with probability $0$). The coupling is entirely through $|S|$.

---

## 3. Theorem T1: the discrepancy identity

Fix a model $S$ and use block order (Section 1.2). Recall $x_b=x_b(S)=t_{S_b}/A_0$, $x=x(S)=t_S/A_0$, $x_\Sigma=\sum_bx_b$; by Lemma 1.1(c), $x_b,x\in[0,1)$.

**Theorem 3.1 (T1(i)).** $t_S=\sum_bt_{S_b}-\delta(S)$ and $d(S)=\Delta_{\det}(S)+\nu\Psi(S)$.

*Proof.* By Lemma 1.2, $n z_S^\top H_{S,0}^{-1}z_S=\sum_bt_{S_b}$, so by the definition of $\delta$,
$$
\delta(S)=n z_S^\top H_{S,0}^{-1}z_S-n z_S^\top H_S^{-1}z_S=\sum_bt_{S_b}-t_S .
$$
For the second identity, subtract the two displays of (1.1):
$$
d(S)=\log\mathrm{BF}(S)-\log r(S)=\tfrac12\Big[\sum_b\log D_{S_b}-\log D_S\Big]+\nu\Big[\sum_b\log(1-x_b)-\log(1-x)\Big]=\Delta_{\det}(S)+\nu\Psi(S).\qquad\square
$$

**Theorem 3.2 (T1(ii)).** Assume $x_\Sigma(S)<1$. Then $1-x_\Sigma+\delta(S)/A_0=1-x(S)>0$, so $\Psi_{\rm off}$ is well defined, and $\Psi=\Psi_{\rm sh}+\Psi_{\rm off}$. Moreover $\Psi_{\rm sh}\ge0$, with equality if and only if at most one of the $x_b$ is positive.

*Proof.* By Theorem 3.1, $1-x_\Sigma+\delta/A_0=1-\big(\sum_bt_{S_b}-\delta\big)/A_0=1-t_S/A_0=1-x>0$. Hence
$$
\Psi_{\rm sh}+\Psi_{\rm off}=\Big[\sum_b\log(1-x_b)-\log(1-x_\Sigma)\Big]+\Big[\log(1-x_\Sigma)-\log(1-x)\Big]=\sum_b\log(1-x_b)-\log(1-x)=\Psi .
$$
For the sign, we prove by induction on $m$ the *Weierstrass inequality*: for $u_1,\dots,u_m\in[0,1)$,
$$
\Theta_m:=\prod_{i\le m}(1-u_i)-\Big(1-\sum_{i\le m}u_i\Big)\ \ge0,\qquad\text{with }\Theta_m=0\iff\text{at most one }u_i>0. \tag{3.1}
$$
For $m=1$, $\Theta_1=0$. For $m\ge1$, expanding $\prod_{i\le m+1}(1-u_i)=(1-u_{m+1})\prod_{i\le m}(1-u_i)=(1-u_{m+1})\big[\Theta_m+1-\sum_{i\le m}u_i\big]$ gives
$$
\Theta_{m+1}=(1-u_{m+1})\Theta_m+u_{m+1}\sum_{i\le m}u_i .
$$
Both terms are $\ge0$ (as $1-u_{m+1}>0$, $\Theta_m\ge0$ by induction, and $u_i\ge0$), so $\Theta_{m+1}\ge0$; and $\Theta_{m+1}=0$ iff $\Theta_m=0$ and $u_{m+1}\sum_{i\le m}u_i=0$, iff [at most one of $u_1,\dots,u_m$ is positive] and [$u_{m+1}=0$ or $u_1=\dots=u_m=0$], iff at most one of $u_1,\dots,u_{m+1}$ is positive. Apply (3.1) with $u_b=x_b\in[0,1)$: $\prod_b(1-x_b)\ge1-x_\Sigma>0$, and since $\log$ is strictly increasing, $\Psi_{\rm sh}=\log\prod_b(1-x_b)-\log(1-x_\Sigma)\ge0$ with equality iff $\Theta_L=0$. $\square$

**Example 3.3 ($x_\Sigma<1$ is not automatic).** Let $n=4$, $p=2$, and let both columns of $X$ equal $\mathbf 1_4=(1,1,1,1)^\top$ (standardised: $\|\mathbf 1_4\|^2=4=n$), two singleton blocks, $y=\mathbf 1_4$ and $b_0=0.01$. For $S_b=\{j\}$: $G=4$, $H=5\cdot4+1=21$, $z=\mathbf 1_4^\top y=4$, $t_{\{j\}}=4\cdot16/21=64/21=3.0476$. With $A_0=0.02+4=4.02$ and $S=\{1,2\}$, the fractions are $x_1(S)=x_2(S)=\frac{64/21}{4.02}=\frac{3200}{4221}=0.7581$ and $x_\Sigma(S)=\frac{6400}{4221}=1.516>1$: the separately fitted blocks jointly "explain" $\sum_bt_{S_b}=128/21=6.095>4=y^\top y$. (Check "T1(ii) example x_Sigma>1" in the script.) In general $x_\Sigma(S)\le\frac n{n+1}\sum_b\|P_{S_b}y\|^2/A_0$ by Lemma 1.1(b), and $\sum_b\|P_{S_b}y\|^2$ can exceed $\|y\|^2$ by up to a factor $L$ when the blocks' column spans overlap; the condition $x_\Sigma<1$ holds, for instance, whenever the column spans of $X_{S_1},\dots,X_{S_L}$ are mutually orthogonal (then $\sum_b\|P_{S_b}y\|^2=\|P_Sy\|^2\le\|y\|^2$), which is the situation of (iii).

**Theorem 3.4 (T1(iii)).** If $X_{S_b}^\top X_{S_{b'}}=0$ for all $b\ne b'$, then $\Delta_{\det}(S)=0$, $\delta(S)=0$, $x_\Sigma(S)=x(S)<1$, and $d(S)=\nu\Psi_{\rm sh}(S)\ge0$. Moreover $d(S)=0$ if and only if at most one block $b$ has $X_{S_b}^\top y\ne0$.

*Proof.* In block order the off-block entries of $G_S$ are the matrices $X_{S_b}^\top X_{S_{b'}}=0$, so $G_S=G_{S,0}$, $H_S=H_{S,0}$ and $\delta(S)=nz_S^\top(H_{S,0}^{-1}-H_{S,0}^{-1})z_S=0$. By Theorem 3.1, $t_S=\sum_bt_{S_b}$, so $x_\Sigma=x<1$ (Lemma 1.1(c)). By Lemma 1.2, $\det H_S=\prod_b\det H_{S_b}$ and $\det(G_S+I)=\prod_b\det(G_{S_b}+I)$, so $D_S=\prod_bD_{S_b}$ and $\Delta_{\det}(S)=\tfrac12[\sum_b\log D_{S_b}-\sum_b\log D_{S_b}]=0$. Since $x_\Sigma<1$, Theorem 3.2 applies: $\Psi_{\rm off}=\log(1-x_\Sigma)-\log(1-x_\Sigma+0)=0$, so $\Psi=\Psi_{\rm sh}$ and, by Theorem 3.1, $d(S)=0+\nu\Psi_{\rm sh}(S)\ge0$ ($\nu>0$). Finally $d(S)=0$ iff $\Psi_{\rm sh}=0$ iff at most one $x_b>0$ (Theorem 3.2) iff at most one $t_{S_b}>0$ iff at most one $z_{S_b}=X_{S_b}^\top y\ne0$ (Lemma 1.1(d)). $\square$

*Remark 3.5 (the message of (iii), quantified).* Under block-orthogonality, $d(S)=\nu\Psi_{\rm sh}(S)$ with $\nu=a_0+n/2$, and $\Psi_{\rm sh}$ is a function of the fractions $x_b(S)\in[0,1)$ only. Write $\Psi_{\rm sh}$ as $f(u_1,\dots,u_m)=\sum_i\log(1-u_i)-\log(1-\sum_iu_i)$ on $\{u\in[0,1)^m:\sum u_i<1\}$. Adding a variable never decreases $f$: with $s=\sum_{i\le m}u_i$, $f(u_1,\dots,u_{m+1})-f(u_1,\dots,u_m)=\log\frac{(1-u_{m+1})(1-s)}{1-s-u_{m+1}}\ge0$ because $(1-u_{m+1})(1-s)=1-s-u_{m+1}+u_{m+1}s$. Hence if two blocks carry fractions $x_b,x_{b'}\ge\xi>0$ (and $x_\Sigma<1$, which (iii) guarantees),
$$
\Psi_{\rm sh}(S)\ \ge\ \log\frac{(1-x_b)(1-x_{b'})}{1-x_b-x_{b'}}=\log\Big(1+\frac{x_bx_{b'}}{1-x_b-x_{b'}}\Big)\ \ge\ \log(1+\xi^2)\ \ge\ \tfrac12\xi^2 ,
$$
using $x_bx_{b'}\ge\xi^2$, $1-x_b-x_{b'}\le1$, and $\log(1+u)\ge u/2$ on $[0,1]$. So the start under-rewards every model whose signal is spread over two or more blocks by $d(S)\ge\nu\log(1+\xi^2)\ge\nu\xi^2/2$, which is of order $n$ when the fractions are bounded away from $0$; and the lower bound $\log\frac{(1-x_b)(1-x_{b'})}{1-x_b-x_{b'}}$ grows without bound as $x_b+x_{b'}\uparrow1$ with $x_b,x_{b'}\ge\xi$. (Not used elsewhere.)

---

## 4. Lemma L1: the determinant term

**Lemma 4.1.** For $\lambda\ge0$ put $g(\lambda)=\log\dfrac{\lambda+1}{\lambda+1/(n+1)}$. Then $g$ is strictly decreasing on $[0,\infty)$, $g(0)=\log(n+1)$, $g(\lambda)>0$, and for $\lambda>0$
$$
g(\lambda)\le\frac{n}{(n+1)\lambda+1}\le\frac1\lambda .
$$
Moreover, if $\lambda_1,\dots,\lambda_k$ are the eigenvalues of $G_S$ (with multiplicity), then $\log D_S=\sum_{i=1}^k[\log(n+1)-g(\lambda_i)]$.

*Proof.* $g'(\lambda)=\frac1{\lambda+1}-\frac1{\lambda+1/(n+1)}<0$. $g(0)=\log(n+1)$. Writing $g(\lambda)=\log\big(1+\frac{1-1/(n+1)}{\lambda+1/(n+1)}\big)$ and using $\log(1+u)\le u$ for $u\ge0$ gives $g(\lambda)\le\frac{n/(n+1)}{\lambda+1/(n+1)}=\frac{n}{(n+1)\lambda+1}$, and $\frac n{(n+1)\lambda+1}\le\frac n{(n+1)\lambda}<\frac1\lambda$ for $\lambda>0$. For the last claim, in the eigenbasis of $G_S$, $\det H_S=\prod_i((n+1)\lambda_i+1)$ and $\det(G_S+I)=\prod_i(\lambda_i+1)$, so $\log D_S=\sum_i\log\frac{(n+1)\lambda_i+1}{\lambda_i+1}=\sum_i\big[\log(n+1)+\log\frac{\lambda_i+1/(n+1)}{\lambda_i+1}\big]$. $\square$

**Theorem 4.2 (L1).** Let $S\ne\emptyset$, $k=|S|$, and let $\lambda_{\min}=\lambda_{\min}(G_S)\ge0$. Then
$$
|\Delta_{\det}(S)|\le\frac k2\,g(\lambda_{\min})\le\frac k2\log(n+1),\qquad\text{and if }\varphi^2(S)=\lambda_{\min}/n>0:\quad |\Delta_{\det}(S)|\le\frac k2\cdot\frac{n}{(n+1)\lambda_{\min}+1}\le\frac{k}{2n\varphi^2(S)} .
$$
For $S=\emptyset$, $\Delta_{\det}=0$ and the bounds hold trivially, with the conventions $\lambda_{\min}$ of a $0\times0$ matrix $=+\infty$, $\varphi^2(\emptyset)=+\infty$ and $g(+\infty)=\lim_{\lambda\to\infty}g(\lambda)=0$ (so every bound reads $0\le0$).

*Proof.* Let $\lambda_1,\dots,\lambda_k$ be the eigenvalues of $G_S$ and, for each $b$ with $S_b\ne\emptyset$, $\lambda^{(b)}_1,\dots,\lambda^{(b)}_{|S_b|}$ those of $G_{S_b}$. Since $\sum_b|S_b|=k$, the $\log(n+1)$ terms of Lemma 4.1 cancel:
$$
2\Delta_{\det}(S)=\sum_b\log D_{S_b}-\log D_S=\sum_b\sum_{i}\big[\log(n+1)-g(\lambda^{(b)}_i)\big]-\sum_{i=1}^k\big[\log(n+1)-g(\lambda_i)\big]=\sum_{i=1}^kg(\lambda_i)-\sum_b\sum_ig(\lambda^{(b)}_i). \tag{4.1}
$$
In block order, $G_{S_b}$ is a principal submatrix of $G_S$, so by the Cauchy interlacing theorem (equivalently, by $\lambda_{\min}(G_{S_b})=\min_{\|v\|=1}v^\top G_{S_b}v=\min\{u^\top G_Su:\|u\|=1,\ u\text{ supported on block }b\}\ge\lambda_{\min}(G_S)$) every $\lambda^{(b)}_i\ge\lambda_{\min}$, and trivially every $\lambda_i\ge\lambda_{\min}$. As $g$ is decreasing and positive, every $g$-value in (4.1) lies in $(0,g(\lambda_{\min})]$. Both sums in (4.1) have exactly $k$ terms, so their difference lies in $[-k\,g(\lambda_{\min}),\,k\,g(\lambda_{\min})]$:
$$
|\Delta_{\det}(S)|\le\tfrac k2\,g(\lambda_{\min}). \tag{4.2}
$$
The displayed bounds follow from Lemma 4.1: $g(\lambda_{\min})\le g(0)=\log(n+1)$ always, and $g(\lambda_{\min})\le\frac n{(n+1)\lambda_{\min}+1}\le\frac1{\lambda_{\min}}=\frac1{n\varphi^2(S)}$ when $\lambda_{\min}>0$. $\square$

*Remark 4.3 (a uniform eigenvalue bound is sufficient for the $O(k/n)$ reading, but not necessary; the logarithmic bound is sharp).* (a) The first bound of L1 is a statement about one model at a time, with its own $\varphi^2(S)$. The reading "$\Delta_{\det}(S)=O(|S|/n)$" used in the introduction follows from L1 *uniformly over a family $\mathcal M$ of models* once one assumes $\inf_{S\in\mathcal M}\varphi^2(S)\ge\varphi_0^2>0$; then $\sup_{S\in\mathcal M}|\Delta_{\det}(S)|\le\max_{S\in\mathcal M}|S|/(2n\varphi_0^2)$. (Orientation only, not checked here: the draft supplies such a bound in its Assumption "Regime (a)" through a restricted-eigenvalue condition, and in its fixed-$p$ setting through $\Gamma_n\to\Gamma\succ0$.)
(b) Without it the determinant term is not small. Take two identical standardised columns $x_1=x_2$ in different blocks and $S=\{1,2\}$. Then $G_S=n\begin{pmatrix}1&1\\1&1\end{pmatrix}$ has eigenvalues $2n$ and $0$, so $\varphi^2(S)=0$, and by Lemma 4.1 (with $g(0)=\log(n+1)$)
$$
\Delta_{\det}(S)=\tfrac12\big[2\log D_{\{1\}}-\log D_S\big]=\tfrac12\Big[2\log\tfrac{(n+1)n+1}{n+1}-\log\tfrac{(n+1)2n+1}{2n+1}\Big]=\tfrac12\log n+o(1)\qquad(n\to\infty).
$$
(Numerically, $\Delta_{\det}=2.3002$ at $n=100$ and $4.6051$ at $n=10^4$, against $\tfrac12\log n=2.3026$ and $4.6052$; checks "L1 example identical columns" in the script.) So for some singular $G_S$ the determinant term can be of the order of the second bound $\tfrac{|S|}2\log(n+1)$ (here $\log(n+1)$), up to the factor $2$; the second bound is therefore sharp up to a constant.
(c) The sharper form (4.2), $|\Delta_{\det}(S)|\le\frac{|S|}2\log\frac{\lambda_{\min}+1}{\lambda_{\min}+1/(n+1)}$, interpolates between the two bounds of L1 and is what one gets from the proof.
(d) The uniform eigenvalue bound in (a) is sufficient, not necessary: for a design whose blocks are mutually orthogonal, $\Delta_{\det}\equiv0$ (Theorem 3.4) whatever $\varphi^2(S)$ does (take $n\ge3$, $C_1=\{1,2\}$, $C_2=\{3\}$ with $G=n\begin{pmatrix}1&1-1/n&0\\1-1/n&1&0\\0&0&1\end{pmatrix}$, so that $\varphi^2(\{1,2,3\})=1/n\to0$).

**Theorem 4.4 (the determinant term is nonnegative).** For every model $S$, $\Delta_{\det}(S)\ge0$, with equality if and only if $E_S=0$, i.e. $S$ is block-orthogonal. Consequently $d(S)\ge\nu\Psi(S)$ for every $S$.

*Proof.* For $S=\emptyset$ both sides are $0$. Let $S\ne\emptyset$, $k=|S|$, and put $f(\lambda)=\log\frac{(n+1)\lambda+1}{\lambda+1}=\log(n+1)-g(\lambda)$ for $\lambda\ge0$. Then $f'(\lambda)=\frac{n+1}{(n+1)\lambda+1}-\frac1{\lambda+1}=\frac{n}{((n+1)\lambda+1)(\lambda+1)}$ is strictly decreasing, so $f$ is strictly concave on $[0,\infty)$. By Lemma 4.1, $\log D_S=\operatorname{tr}f(G_S)$, and by Lemma 1.2 (block order) $\sum_b\log D_{S_b}=\operatorname{tr}f(G_{S,0})$, since $f$ of a block-diagonal matrix is block diagonal with blocks $f(G_{S_b})$. Let $v_1,\dots,v_k$ be an orthonormal eigenbasis of the block-diagonal matrix $G_{S,0}$ with each $v_i$ supported on a single block (concatenate eigenbases of the blocks $G_{S_b}$), $G_{S,0}v_i=\mu_iv_i$. Since the diagonal blocks of $E_S$ vanish and $v_i$ is supported on one block, $v_i^\top E_Sv_i=0$, so $v_i^\top G_Sv_i=\mu_i$. Write $G_S=\sum_j\lambda_ju_ju_j^\top$ with $(u_j)$ orthonormal. For each $i$ the weights $(v_i^\top u_j)^2$ sum to $1$, so Jensen's inequality for the concave $f$ gives
$$
v_i^\top f(G_S)v_i=\sum_jf(\lambda_j)(v_i^\top u_j)^2\le f\Big(\sum_j\lambda_j(v_i^\top u_j)^2\Big)=f(v_i^\top G_Sv_i)=f(\mu_i).
$$
Summing over $i$, $\operatorname{tr}f(G_S)=\sum_iv_i^\top f(G_S)v_i\le\sum_if(\mu_i)=\operatorname{tr}f(G_{S,0})$, i.e. $2\Delta_{\det}(S)=\operatorname{tr}f(G_{S,0})-\operatorname{tr}f(G_S)\ge0$. Equality holds iff every Jensen step is an equality iff, by strict concavity, for each $i$ all $\lambda_j$ with $v_i^\top u_j\ne0$ are equal, i.e. $v_i$ lies in an eigenspace of $G_S$, necessarily with eigenvalue $v_i^\top G_Sv_i=\mu_i$. Then $G_Sv_i=\mu_iv_i=G_{S,0}v_i$ for a basis, so $G_S=G_{S,0}$ and $E_S=0$. Conversely $E_S=0$ gives $\Delta_{\det}=0$ (Theorem 3.4). The last claim is Theorem 3.1. $\square$

*Remark 4.5.* An equivalent route (suggested by a reviewer): with $\mathcal F(t)=\sum_b\log\det(I+tG_{S_b})-\log\det(I+tG_S)$ (not to be confused with the log-normaliser $F(\phi)$ of Section 0.1 or the family $\mathcal M$ of Remark 4.3), $2\Delta_{\det}=\mathcal F(n+1)-\mathcal F(1)$ and $\mathcal F'(t)=t^{-1}[\operatorname{tr}(I+tG_S)^{-1}-\sum_b\operatorname{tr}(I+tG_{S_b})^{-1}]\ge0$, because each diagonal block of $(I+tG_S)^{-1}$ dominates the inverse of the corresponding diagonal block of $I+tG_S$ (Schur complement). Note that Theorem 4.4 is the endpoint inequality $\mathcal F(n+1)\ge\mathcal F(1)$, implied by the monotonicity $\mathcal F'\ge0$, and not the same as Fischer's inequality $\mathcal F(t)\ge0$ at each fixed $t$ (the latter follows from the proof of Theorem 4.4 with $f$ replaced by the concave function $\lambda\mapsto\log(1+t\lambda)$); Fischer's inequality alone would not give Theorem 4.4, since $\mathcal F(1)>0$ whenever $E_S\ne0$ (by the equality case of the same Jensen argument, $\lambda\mapsto\log(1+\lambda)$ being strictly concave).

---

## 5. Lemma L2: the off-block term

*Conventions for empty pieces.* For $S=\emptyset$ all matrices are $0\times0$; we set $\kappa(\emptyset)=0$, and $\delta(\emptyset)=0$, $x_\Sigma(\emptyset)=x(\emptyset)=0$, $\Psi_{\rm off}(\emptyset)=0$ by the empty-sum conventions of Section 0.2, so both bounds of L2 hold trivially (as $0\le0$) and L2 is proved for $S=\emptyset$. For $S\ne\emptyset$, blocks with $S_b=\emptyset$ contribute no rows or columns to $G_{S,0}$ and are ignored in the minima below.

Fix $S\ne\emptyset$ in block order, $E=E_S=G_S-G_{S,0}$ (symmetric), and assume $G_{S,0}\succ0$, i.e. $G_{S_b}\succ0$ for every block with $S_b\ne\emptyset$ (each block's columns of $S$ are linearly independent). Then $\lambda_{\min}(G_{S,0})=\min_{b:S_b\ne\emptyset}\lambda_{\min}(G_{S_b})>0$ and $\kappa=\kappa(S)=\|E\|_{\rm op}/\lambda_{\min}(G_{S,0})$ is well defined.

**Lemma 5.1.** Let $M=(n+1)H_{S,0}^{-1/2}EH_{S,0}^{-1/2}$ (symmetric). Then $\|M\|_{\rm op}\le\frac{(n+1)\|E\|}{(n+1)\lambda_{\min}(G_{S,0})+1}\le\kappa$, the second inequality being strict when $E\ne0$. If $\kappa<1$, then $I+M$ is invertible, $H_S=H_{S,0}^{1/2}(I+M)H_{S,0}^{1/2}$,
$$
H_{S,0}^{-1}-H_S^{-1}=H_{S,0}^{-1/2}\,M(I+M)^{-1}\,H_{S,0}^{-1/2},\qquad \|M(I+M)^{-1}\|_{\rm op}\le\frac{\|M\|}{1-\|M\|}\le\frac{\kappa}{1-\kappa},
$$
and $G_S\succ0$.

*Proof.* $H_{S,0}=(n+1)G_{S,0}+I\succ0$ has $\lambda_{\min}(H_{S,0})=(n+1)\lambda_{\min}(G_{S,0})+1$, so $\|H_{S,0}^{-1/2}\|^2=\|H_{S,0}^{-1}\|=1/\lambda_{\min}(H_{S,0})$ and $\|M\|\le(n+1)\|H_{S,0}^{-1/2}\|^2\|E\|=\frac{(n+1)\|E\|}{(n+1)\lambda_{\min}(G_{S,0})+1}\le\frac{\|E\|}{\lambda_{\min}(G_{S,0})}=\kappa$, strictly when $\|E\|>0$ because of the $+1$ in the denominator (if $E=0$ then $M=0$ and $\kappa=0$, and the lemma is trivial). Next, $H_S=(n+1)(G_{S,0}+E)+I=H_{S,0}+(n+1)E=H_{S,0}^{1/2}\big(I+(n+1)H_{S,0}^{-1/2}EH_{S,0}^{-1/2}\big)H_{S,0}^{1/2}=H_{S,0}^{1/2}(I+M)H_{S,0}^{1/2}$. If $\|M\|<1$, the eigenvalues $m_i$ of the symmetric $M$ satisfy $|m_i|\le\|M\|<1$, so $I+M$ is invertible, $H_S^{-1}=H_{S,0}^{-1/2}(I+M)^{-1}H_{S,0}^{-1/2}$ and
$$
H_{S,0}^{-1}-H_S^{-1}=H_{S,0}^{-1/2}\big[I-(I+M)^{-1}\big]H_{S,0}^{-1/2}=H_{S,0}^{-1/2}\,M(I+M)^{-1}\,H_{S,0}^{-1/2},
$$
since $I-(I+M)^{-1}=(I+M-I)(I+M)^{-1}$. The symmetric matrix $M(I+M)^{-1}$ has eigenvalues $m_i/(1+m_i)$, and $|m/(1+m)|\le\|M\|/(1-\|M\|)$ for $|m|\le\|M\|<1$ (the function $m\mapsto|m|/(1+m)$ on $[-\|M\|,\|M\|]$ is maximised at $m=-\|M\|$); as $s\mapsto s/(1-s)$ is increasing on $[0,1)$, the bound in $\kappa$ follows. Finally $G_S=G_{S,0}+E\succeq(\lambda_{\min}(G_{S,0})-\|E\|)I=(1-\kappa)\lambda_{\min}(G_{S,0})I\succ0$. $\square$

**Theorem 5.2 (L2).** Assume $G_{S,0}\succ0$ and $\kappa(S)<1$. Then
$$
|\delta(S)|\le\frac{\kappa}{1-\kappa}\sum_bt_{S_b}. \tag{5.1}
$$
If moreover $x_\Sigma(S)<1$, then
$$
|\Psi_{\rm off}(S)|\le\frac{\kappa}{1-\kappa}\cdot\frac{x_\Sigma(S)}{\min\{1-x_\Sigma(S),\,1-x(S)\}}. \tag{5.2}
$$

*Proof.* Put $u=H_{S,0}^{-1/2}z_S$. By Lemma 1.2, $n\|u\|^2=nz_S^\top H_{S,0}^{-1}z_S=\sum_bt_{S_b}$, and by Lemma 5.1, $\delta(S)=nz_S^\top(H_{S,0}^{-1}-H_S^{-1})z_S=n\,u^\top M(I+M)^{-1}u$, so $|\delta(S)|\le n\|u\|^2\|M(I+M)^{-1}\|\le\frac{\kappa}{1-\kappa}\sum_bt_{S_b}$, which is (5.1).
For (5.2): by Theorem 3.2, $\Psi_{\rm off}=\log(1-x_\Sigma)-\log(1-x)$ with $1-x_\Sigma>0$ and $1-x>0$. For $s_1,s_2>0$, the mean value theorem gives $|\log s_1-\log s_2|=|s_1-s_2|/\bar s$ for some $\bar s$ between $s_1$ and $s_2$, so $|\log s_1-\log s_2|\le|s_1-s_2|/\min\{s_1,s_2\}$. With $s_1=1-x_\Sigma$, $s_2=1-x$: $|s_1-s_2|=|x-x_\Sigma|=|t_S-\sum_bt_{S_b}|/A_0=|\delta(S)|/A_0\le\frac{\kappa}{1-\kappa}\sum_bt_{S_b}/A_0=\frac{\kappa}{1-\kappa}x_\Sigma$ by (5.1). $\square$

**Corollary 5.3 (the $O(n\kappa)$ reading).** Let $\kappa_0\in(0,1)$ and $\eta\in(0,1]$. For every model $S$ with $G_{S,0}\succ0$, $\kappa(S)\le\kappa_0$, $x_\Sigma(S)<1$ and $\min\{1-x_\Sigma(S),1-x(S)\}\ge\eta$,
$$
\nu\,|\Psi_{\rm off}(S)|\le\frac{\nu}{(1-\kappa_0)\eta}\,\kappa(S)=\frac{a_0+n/2}{(1-\kappa_0)\eta}\,\kappa(S)\le\frac{a_0+\tfrac12}{(1-\kappa_0)\eta}\;n\,\kappa(S) ,
$$
the last step for $n\ge1$. Thus $\nu|\Psi_{\rm off}(S)|=O(n\kappa(S))$ with the constant $(a_0+\tfrac12)/((1-\kappa_0)\eta)$, uniform in $n$ and over all such $S$ when $(a_0,\kappa_0,\eta)$ are fixed; if instead $a_0\le An$, $\kappa_0\le1-\epsilon$ and $\eta\ge\epsilon$ with fixed $A>0$ and $\epsilon\in(0,1)$, the middle expression gives the constant $(A+\tfrac12)/\epsilon^2$.

*Proof.* Insert $x_\Sigma<1$, $1-\kappa\ge1-\kappa_0$ and the lower bound $\eta$ into (5.2) and multiply by $\nu=a_0+n/2\le(a_0+\tfrac12)n$. $\square$

*Remark 5.4.* (a) The hypothesis $G_{S,0}\succ0$ is needed to define $\kappa$; it says each block's columns of $S$ are linearly independent (so $|S_b|\le n$). It does not require $G_S\succ0$, but $\kappa<1$ implies it (Lemma 5.1). (b) The two residual fractions enter separately: $1-x_\Sigma$ is the fraction of $A_0$ left unexplained by the blocks fitted separately, $1-x$ the fraction left by the joint fit; both must be bounded away from $0$ for the $O(n\kappa)$ bound, and this is why Corollary 5.3 carries $\eta$. Near $x_\Sigma\uparrow1$ the bound (5.2) blows up, and so can $\Psi_{\rm off}$: $\Psi_{\rm off}=\log(1-x_\Sigma)-\log(1-x)\to-\infty$ when $x_\Sigma\to1$ with $x$ fixed. (c) The bound (5.1) is of the right form: $\delta$ is a quadratic form in $u$ with matrix $M(I+M)^{-1}$ whose norm is $\|M\|/(1-\|M\|)$ when $M$ has eigenvalue $-\|M\|$, and $\|M\|$ can approach $\kappa$ as $n\to\infty$ with $G_S/n$ fixed.

---

## 6. Lemma L3: concentration propagates along the bridge

This section is in the abstract setting of Section 0.1: $\gamma_0>0$ on the finite set $\mathcal S$, $d:\mathcal S\to\mathbb R$ arbitrary. Fix $S^\ast\in\mathcal S$; thus $p(S^\ast)>0$ and $q_\phi(S^\ast)>0$ for every real $\phi$. For $\phi\in\mathbb R$ put
$$
O_\phi=\frac{1-q_\phi(S^\ast)}{q_\phi(S^\ast)}=\sum_{S\in\mathcal S\setminus\{S^\ast\}}\frac{q_\phi(S)}{q_\phi(S^\ast)}=\sum_{S\ne S^\ast}\frac{\gamma_0(S)}{\gamma_0(S^\ast)}\,e^{\phi\,(d(S)-d(S^\ast))}\in[0,\infty). \tag{6.1}
$$
If $\mathcal S=\{S^\ast\}$ then $O_\phi=0$ for all $\phi$ and every statement below is trivial (with $0^0=1$); assume henceforth $|\mathcal S|\ge2$, so $O_\phi>0$ for all $\phi$.

**Lemma 6.1 (log-convexity of the odds).** $\phi\mapsto\log O_\phi$ is convex on $\mathbb R$. Equivalently, for $\phi_a<\phi_b$, $\theta\in[0,1]$ and $\phi=(1-\theta)\phi_a+\theta\phi_b$,
$$
O_\phi\le O_{\phi_a}^{1-\theta}O_{\phi_b}^{\theta}\le\max\{O_{\phi_a},O_{\phi_b}\}. \tag{6.2}
$$

*Proof.* Write $a_S=\gamma_0(S)/\gamma_0(S^\ast)>0$ and $\zeta_S=d(S)-d(S^\ast)$, so that $O_\phi=\sum_{S\ne S^\ast}a_Se^{\phi\zeta_S}$. For $\phi=(1-\theta)\phi_a+\theta\phi_b$,
$$
a_Se^{\phi\zeta_S}=\big(a_Se^{\phi_a\zeta_S}\big)^{1-\theta}\big(a_Se^{\phi_b\zeta_S}\big)^{\theta}.
$$
For $\theta\in(0,1)$, Hölder's inequality with exponents $1/(1-\theta)$ and $1/\theta$ gives $\sum_SA_S^{1-\theta}B_S^\theta\le(\sum_SA_S)^{1-\theta}(\sum_SB_S)^\theta$ for nonnegative $A_S,B_S$, which is the first inequality in (6.2); for $\theta\in\{0,1\}$ it is an equality. The second inequality is $u^{1-\theta}v^\theta\le\max\{u,v\}$ for $u,v>0$. The convexity statement is (6.2) read as $\log O_\phi\le(1-\theta)\log O_{\phi_a}+\theta\log O_{\phi_b}$. (Alternatively: $\log O_\phi$ is a log-sum-exp of affine functions of $\phi$, which is convex.) $\square$

**Theorem 6.2 (L3, and its interval form).** For every $\phi\in[0,1]$, $O_\phi\le O_0^{1-\phi}O_1^\phi\le\max\{O_0,O_1\}$. More generally, for every interval $[\phi_a,\phi_b]\subset\mathbb R$,
$$
\inf_{\phi\in[\phi_a,\phi_b]}q_\phi(S^\ast)=\min\{q_{\phi_a}(S^\ast),q_{\phi_b}(S^\ast)\},\qquad\text{in particular}\qquad \inf_{\phi\in[0,1]}q_\phi(S^\ast)=\min\{q_0(S^\ast),q_1(S^\ast)\}=\min\{\pi_0(S^\ast),\pi(S^\ast)\}, \tag{6.3}
$$
where the last equality is the specialisation $q_0=\pi_0$, $q_1=\pi$ of the paper's bridge (Section 0.1).

*Proof.* The first claim is (6.2) with $[\phi_a,\phi_b]=[0,1]$ and $\theta=\phi$. For (6.3), $q_\phi(S^\ast)=1/(1+O_\phi)$ is a decreasing function of $O_\phi$, so (6.2) gives $q_\phi(S^\ast)\ge1/(1+\max\{O_{\phi_a},O_{\phi_b}\})=\min\{q_{\phi_a}(S^\ast),q_{\phi_b}(S^\ast)\}$ for all $\phi\in[\phi_a,\phi_b]$; the reverse inequality holds because the endpoints belong to the interval. $\square$

**Corollary 6.3 (the "hence" clause).** Let $(\gamma_0^{(n)},d^{(n)},\mathcal S^{(n)},S^{\ast(n)})$ be a sequence of such data (possibly random, as in the draft where they depend on $y$). If $\pi_0(S^\ast)\to1$ and $\pi(S^\ast)\to1$, then $\inf_{\phi\in[0,1]}q_\phi(S^\ast)\to1$, where all three convergences are understood in the same sense: deterministically, in probability, or almost surely.

*Proof.* By (6.3), $1-\inf_{\phi\in[0,1]}q_\phi(S^\ast)=\max\{1-\pi_0(S^\ast),1-\pi(S^\ast)\}\le(1-\pi_0(S^\ast))+(1-\pi(S^\ast))$, pointwise in the data. In the random case the infimum over the uncountable set $[0,1]$ is a random variable because, by (6.3), it equals the minimum of the two random variables $\pi_0(S^\ast)$ and $\pi(S^\ast)$. Each mode of convergence is preserved by the pointwise domination. $\square$

*Remark 6.4 (the hypothesis $p(S^\ast)>0$).* If $p(S^\ast)=0$ (i.e. $|S^\ast|>k_{\max}$), then $\gamma_\phi(S^\ast)=0$ and $q_\phi(S^\ast)=0$ for every $\phi$, the odds $O_\phi$ are $+\infty$, and the lemma is void; its "hence" clause cannot even be triggered, since $\pi_0(S^\ast)=\pi(S^\ast)=0$. So the hypothesis $p(S^\ast)>0$, which for positive tables is equivalent to $S^\ast\in\mathcal S$, is exactly the hypothesis needed, and it is the one the draft states. (Orientation only: in the draft's T2 it is satisfied by $S^\ast=S_0$ once $s_0\le k_{\max}$.)

*Remark 6.5.* Lemma 6.1 is stronger than the concavity of $\phi\mapsto\log q_\phi(S^\ast)=\log\gamma_0(S^\ast)+\phi d(S^\ast)-F(\phi)$ (which follows from the convexity of $F$): $\log O$ convex implies $\log(1+O)=\log(1+e^{\log O})$ convex, since $u\mapsto\log(1+e^u)$ is convex and increasing, but not conversely. Both give (6.3).

---

## 7. Lemma L7: the single-model identity for $\chi^2$

Abstract setting of Section 0.1. Recall $\bar Z_\psi=\sum_S\gamma_0(S)e^{\psi d(S)}$ is defined and positive for every real $\psi$, including $\psi>1$ (the over-tempered range, where $q_\psi\propto p\,r^{1-\psi}\mathrm{BF}^\psi$ in the paper's notation).

**Theorem 7.1 (L7, identity).** For every $S^\ast\in\mathcal S$ and all real $\phi$ and $\delta$,
$$
1+\chi^2(q_{\phi+\delta}\|q_\phi)=\frac{\bar Z_{\phi+2\delta}\bar Z_\phi}{\bar Z_{\phi+\delta}^2}=\frac{q_{\phi+\delta}(S^\ast)^2}{q_\phi(S^\ast)\,q_{\phi+2\delta}(S^\ast)}\le\frac1{q_\phi(S^\ast)\,q_{\phi+2\delta}(S^\ast)} . \tag{7.1}
$$

*Proof.* By definition,
$$
1+\chi^2(q_{\phi+\delta}\|q_\phi)=\sum_S\frac{q_{\phi+\delta}(S)^2}{q_\phi(S)}=\sum_S\frac{\gamma_0(S)^2e^{2(\phi+\delta)d(S)}}{\bar Z_{\phi+\delta}^2}\cdot\frac{\bar Z_\phi}{\gamma_0(S)e^{\phi d(S)}}=\frac{\bar Z_\phi}{\bar Z_{\phi+\delta}^2}\sum_S\gamma_0(S)e^{(\phi+2\delta)d(S)}=\frac{\bar Z_{\phi+2\delta}\bar Z_\phi}{\bar Z_{\phi+\delta}^2}.
$$
For the second equality, $\bar Z_\psi=\gamma_\psi(S^\ast)/q_\psi(S^\ast)=\gamma_0(S^\ast)e^{\psi d(S^\ast)}/q_\psi(S^\ast)$ for every $\psi$ (as $q_\psi(S^\ast)>0$). Substituting at $\psi=\phi+2\delta$, $\phi$ and $\phi+\delta$,
$$
\frac{\bar Z_{\phi+2\delta}\bar Z_\phi}{\bar Z_{\phi+\delta}^2}=\frac{\gamma_0(S^\ast)^2\,e^{[(\phi+2\delta)+\phi]d(S^\ast)}}{\gamma_0(S^\ast)^2\,e^{2(\phi+\delta)d(S^\ast)}}\cdot\frac{q_{\phi+\delta}(S^\ast)^2}{q_\phi(S^\ast)q_{\phi+2\delta}(S^\ast)}=\frac{q_{\phi+\delta}(S^\ast)^2}{q_\phi(S^\ast)q_{\phi+2\delta}(S^\ast)},
$$
the exponents cancelling exactly. The inequality is $q_{\phi+\delta}(S^\ast)^2\le1$. $\square$

**Theorem 7.2 (L7, consequence).** Let $c>0$, $\delta>0$ and $S^\ast\in\mathcal S$, and suppose
$$
q_\psi(S^\ast)\ge(1+c)^{-1/2}\qquad\text{for all }\psi\in[0,1+\delta]. \tag{7.2}
$$
Then for every stage $t$ with $\phi_{t-1}<1$ of the greedy schedule (0.1), $\phi_t\ge\min\{\phi_{t-1}+\delta,\,1\}$: every greedy step that does not end at $\phi=1$ has length at least $\delta$. Consequently $\phi_t\ge\min\{t\delta,1\}$ for $0\le t\le T$, and $T\le\lceil1/\delta\rceil$.

*Proof.* Let $\phi=\phi_{t-1}\in[0,1)$ (all greedy points lie in $[0,1]$) and $\phi'=\min\{\phi+\delta,1\}$, so $\phi'\in(\phi,1]$ and $\delta':=\phi'-\phi\in(0,\delta]$. Both $\phi$ and $\phi+2\delta'$ lie in $[0,1+\delta]$: indeed $\phi\ge0$ and $\phi+2\delta'=\phi'+\delta'\le1+\delta$. By (7.1) and (7.2),
$$
1+\chi^2(q_{\phi'}\|q_\phi)\le\frac1{q_\phi(S^\ast)\,q_{\phi+2\delta'}(S^\ast)}\le(1+c)^{1/2}(1+c)^{1/2}=1+c ,
$$
so $\phi'$ belongs to the set in (0.1) and $\phi_t\ge\phi'$. By induction from $\phi_0=0$, $\phi_t\ge\min\{t\delta,1\}$ as long as the schedule has not stopped; at the first $t$ with $t\delta\ge1$, i.e. $t=\lceil1/\delta\rceil$, the point $\phi'=1$ is feasible, so $\phi_t=1$ and $T\le\lceil1/\delta\rceil$. $\square$

**Corollary 7.3 (endpoint form of the hypothesis).** By Theorem 6.2 applied to the interval $[0,1+\delta]$, (7.2) is equivalent to the two conditions
$$
\pi_0(S^\ast)=q_0(S^\ast)\ge(1+c)^{-1/2}\qquad\text{and}\qquad q_{1+\delta}(S^\ast)\ge(1+c)^{-1/2}.
$$
Hence the conclusion of Theorem 7.2 holds under these two endpoint conditions alone. (Orientation only: for the draft's T2(iii) it therefore suffices to prove concentration of $\pi_0$ and of the single over-tempered target $q_{1+\delta}$ at $S_0$, rather than of $q_\psi$ uniformly over $\psi\in[0,1+\delta]$.)

*Remark 7.4.* (a) No moment condition is needed: (7.2) is a statement about one atom of each $q_\psi$. (b) The identity (7.1) holds for negative $\delta$ as well; only the consequence uses $\delta>0$. (c) The middle expression in (7.1) is $\exp\{F(\phi+2\delta)+F(\phi)-2F(\phi+\delta)\}$, which is L4(i); the proof above re-derives it rather than citing L4. (d) Since $1+\chi^2\ge1$, (7.1) also shows $q_{\phi+\delta}(S^\ast)^2\ge q_\phi(S^\ast)q_{\phi+2\delta}(S^\ast)$: $\psi\mapsto\log q_\psi(S^\ast)$ is midpoint-concave, in agreement with Remark 6.5.

---

## 8. Lemma L5: stage count under local sub-Gaussianity

Abstract setting of Section 0.1. For $\phi\in\mathbb R$ write $\mu_\phi=\mathbb E_{q_\phi}d$ and $U_\phi=d-\mu_\phi$ (a centred function on $\mathcal S$ under $q_\phi$). The hypothesis of L5 is
$$
\mathcal K_\phi(\lambda):=\log\mathbb E_{q_\phi}e^{\lambda U_\phi}\le\frac{\lambda^2\sigma_d^2}2\qquad\text{for all }\phi\in[0,1],\ \lambda\in[0,2\lambda_0]. \tag{8.1}
$$

**Lemma 8.1 (one-step bound).** For every real $\phi$ and $\delta$,
$$
1+\chi^2(q_{\phi+\delta}\|q_\phi)=\frac{\mathbb E_{q_\phi}e^{2\delta U_\phi}}{\big(\mathbb E_{q_\phi}e^{\delta U_\phi}\big)^2}\le\mathbb E_{q_\phi}e^{2\delta U_\phi}=e^{\mathcal K_\phi(2\delta)} .
$$
Consequently, under (8.1), for $\phi\in[0,1]$ and $0\le\delta\le\lambda_0$: $\chi^2(q_{\phi+\delta}\|q_\phi)\le e^{2\delta^2\sigma_d^2}-1$.

*Proof.* For every $\psi$, $\bar Z_{\phi+\psi}/\bar Z_\phi=\sum_S\frac{\gamma_0(S)e^{\phi d(S)}}{\bar Z_\phi}e^{\psi d(S)}=\mathbb E_{q_\phi}e^{\psi d}=e^{\psi\mu_\phi}\,\mathbb E_{q_\phi}e^{\psi U_\phi}$. Insert this at $\psi=2\delta$ and $\psi=\delta$ into the first identity of (7.1):
$$
1+\chi^2(q_{\phi+\delta}\|q_\phi)=\frac{\bar Z_{\phi+2\delta}/\bar Z_\phi}{(\bar Z_{\phi+\delta}/\bar Z_\phi)^2}=\frac{e^{2\delta\mu_\phi}\mathbb E_{q_\phi}e^{2\delta U_\phi}}{e^{2\delta\mu_\phi}(\mathbb E_{q_\phi}e^{\delta U_\phi})^2}=\frac{\mathbb E_{q_\phi}e^{2\delta U_\phi}}{(\mathbb E_{q_\phi}e^{\delta U_\phi})^2}.
$$
By Jensen's inequality (convexity of $\exp$) and $\mathbb E_{q_\phi}U_\phi=0$, $\mathbb E_{q_\phi}e^{\delta U_\phi}\ge e^{\delta\,\mathbb E_{q_\phi}U_\phi}=1$, which gives the inequality. Under (8.1) with $\lambda=2\delta\in[0,2\lambda_0]$, $\mathcal K_\phi(2\delta)\le(2\delta)^2\sigma_d^2/2=2\delta^2\sigma_d^2$. $\square$

**Lemma 8.2 (local sub-Gaussianity bounds the variance).** If, for some fixed $\phi$, $\mathcal K_\phi(\lambda)\le\lambda^2\sigma_d^2/2$ for all $\lambda\in(0,\lambda_1]$ with $\lambda_1>0$, then $\mathrm{Var}_{q_\phi}(d)\le\sigma_d^2$.

*Proof.* On the finite set $\mathcal S$, $\lambda\mapsto\mathbb E_{q_\phi}e^{\lambda U_\phi}$ is a finite positive combination of exponentials, hence $C^\infty$ and strictly positive, so its logarithm $\mathcal K_\phi$ is $C^\infty$ on $\mathbb R$ (and $\mathcal K_\phi\equiv0$ when $d$ is constant on $\mathcal S$, in which case the claim is trivial). Direct differentiation gives $\mathcal K_\phi(0)=0$, $\mathcal K_\phi'(0)=\mathbb E_{q_\phi}U_\phi=0$ and $\mathcal K_\phi''(0)=\mathbb E_{q_\phi}U_\phi^2-(\mathbb E_{q_\phi}U_\phi)^2=\mathrm{Var}_{q_\phi}(d)$. By Taylor's theorem, $\mathcal K_\phi(\lambda)/\lambda^2\to \mathcal K_\phi''(0)/2=\mathrm{Var}_{q_\phi}(d)/2$ as $\lambda\downarrow0$. Since $\mathcal K_\phi(\lambda)/\lambda^2\le\sigma_d^2/2$ for all $\lambda\in(0,\lambda_1]$, the limit satisfies $\mathrm{Var}_{q_\phi}(d)/2\le\sigma_d^2/2$. $\square$

**Theorem 8.3 (L5).** Under (8.1), with $c>0$:
(a) for every stage $t$ with $\phi_{t-1}<1$ of the greedy schedule (0.1),
$$
\phi_t-\phi_{t-1}\ \ge\ \delta_\ast(\phi_{t-1}):=\min\Big\{\lambda_0,\ \frac{\sqrt{\log(1+c)/2}}{\sigma_d},\ 1-\phi_{t-1}\Big\}>0 ;
$$
(b) $T\le\big\lceil\max\{1/\lambda_0,\ \sigma_d\sqrt{2/\log(1+c)}\}\big\rceil$;
(c) $\mathrm{sd}_{q_\phi}(d)\le\sigma_d$ for every $\phi\in[0,1]$, hence $\Lambda=\int_0^1\mathrm{sd}_{q_\phi}(d)\,d\phi\le\sigma_d$.

*Proof.* (a) Let $\phi=\phi_{t-1}\in[0,1)$, $\delta=\delta_\ast(\phi)\in(0,\lambda_0]$ and $\phi'=\phi+\delta\in(\phi,1]$. By Lemma 8.1 (applicable since $\phi\in[0,1]$ and $0<\delta\le\lambda_0$) and $\delta\le\sqrt{\log(1+c)/2}/\sigma_d$, i.e. $2\delta^2\sigma_d^2\le\log(1+c)$,
$$
\chi^2(q_{\phi'}\|q_\phi)\le e^{2\delta^2\sigma_d^2}-1\le(1+c)-1=c .
$$
So $\phi'$ belongs to the set in (0.1), and $\phi_t\ge\phi'=\phi_{t-1}+\delta_\ast(\phi_{t-1})$.
(b) Put $\delta_0=\min\{\lambda_0,\sqrt{\log(1+c)/2}/\sigma_d\}>0$. By (a), as long as $\phi_{t-1}<1$, either $\phi_t\ge\phi_{t-1}+\delta_0$ or $\phi_t\ge\phi_{t-1}+(1-\phi_{t-1})=1$, i.e. $\phi_t\ge\min\{\phi_{t-1}+\delta_0,1\}$; by induction $\phi_t\ge\min\{t\delta_0,1\}$, and at $t=\lceil1/\delta_0\rceil$ the point $1$ is feasible so $\phi_t=1$. Hence $T\le\lceil1/\delta_0\rceil=\lceil\max\{1/\lambda_0,\sigma_d\sqrt{2/\log(1+c)}\}\rceil$.
(c) For each $\phi\in[0,1]$, (8.1) gives the hypothesis of Lemma 8.2 with $\lambda_1=2\lambda_0$, so $\mathrm{Var}_{q_\phi}(d)\le\sigma_d^2$. Integrate $\mathrm{sd}_{q_\phi}(d)\le\sigma_d$ over $[0,1]$. $\square$

*Remark 8.4.* (a) Parts (a) and (b) of Theorem 8.3 use (8.1) only at $\phi=\phi_{t-1}\in[0,1)$ and $\lambda=2\delta\le2\lambda_0$; part (c) uses it at every $\phi\in[0,1]$ as $\lambda\downarrow0$. No property of the over-tempered targets $q_\psi$, $\psi>1$, enters, although $\bar Z_{\phi+2\delta}$ with $\phi+2\delta>1$ appears in the identity. (b) The restriction $\lambda\le2\lambda_0$ is what makes the hypothesis local. What forces a large $\sigma_d$ is not the range of $d$ but *mass far out in the upper tail*: suppose that under some $q_\phi$, $\phi\in[0,1]$, a model $S'$ has $q_\phi(S')\ge e^{-an}$ and $d(S')-\mathbb E_{q_\phi}d\ge n/2$, with $a>0$. Then $\mathcal K_\phi(\lambda)\ge\log q_\phi(S')+\lambda(d(S')-\mathbb E_{q_\phi}d)\ge-an+\lambda n/2$, so at $\lambda=4a$ the hypothesis (8.1) would require $8a^2\sigma_d^2\ge an$, i.e. $\sigma_d^2\ge n/(8a)$, *whenever* $2\lambda_0\ge4a$. Hence, in the draft's situation (far models whose $d$ exceeds the mean by $\Theta(n)$ at mass $e^{-\Theta(n)}$), (8.1) can hold with $\sigma_d=O(1)$ only for $\lambda_0$ below a constant, which is why L5 is stated locally. The range alone forces nothing: two models $S_1,S_2$ with $d(S_1)=0$, $d(S_2)=n$ and masses $\gamma_0(S_1)=e^{-n}$, $\gamma_0(S_2)=1$ (the small mass on the *lower* value of $d$) satisfy $\mathcal K_\phi''(\lambda)=\mathrm{Var}_{q_{\phi+\lambda}}(d)=n^2q_{\phi+\lambda}(S_1)q_{\phi+\lambda}(S_2)\le n^2e^{-n}$ for all $\phi,\lambda\ge0$; since $\mathcal K_\phi(0)=\mathcal K_\phi'(0)=0$, $\mathcal K_\phi(\lambda)=\int_0^\lambda(\lambda-u)\mathcal K_\phi''(u)\,du\le\lambda^2n^2e^{-n}/2$, so (8.1) holds globally with $\sigma_d^2=n^2e^{-n}\to0$ (a reviewer's example). (c) The step bound in (a) is attained by the greedy schedule only as a lower bound; the greedy step may be much longer.

---

## 9. Hypotheses added, readings, and flags for the draft

**Hypotheses and conventions made explicit (none changes a displayed identity or bound).**
1. *Global.* $n\ge1$, $p\ge1$, $L\ge1$, nonempty blocks; $w(k)>0$ for $0\le k\le p$; an integer cap $0\le k_{\max}\le p$ (a larger cap is replaced by $p$, Section 0.1; the draft should say so, since its operational cap $\lfloor n/2\rfloor$ exceeds $p$ as soon as $n\ge2p+2$ and its $\mathrm{BB}(1,p)$ formula for $w(k)$ has a pole at every integer $k\ge2p$); $W>0$; positive tables $r_b$; $a_0,b_0>0$. Columns of $X_S$ are taken in block order whenever $G_S$ is compared with $G_{S,0}$ (Section 1.2); $t_S$, $D_S$, $m(S)$, $\mathrm{BF}(S)$, $d(S)$ are order-invariant (Lemma 1.1(a)). Empty pieces: $t_\emptyset=0$, $D_\emptyset=1$, empty determinants $1$, $\lambda_{\min}$ of a $0\times0$ matrix $=+\infty$ (so $\varphi^2(\emptyset)=+\infty$), $g(+\infty)=0$, $\kappa(\emptyset)=0$ (Sections 0.2, 4, 5). In the abstract Sections 6 to 8, $\pi$ means $q_1$ (Section 0.1). The empty convolution ($L=1$ in Theorem 2.5(a)) is the unit $\mathbf 1\{\cdot=0\}$, and $0^0=1$ when the model space is a singleton (Section 6).
2. *P1(ii).* The draw of $K$ is over $k\in\{0,\dots,k_{\max}\}$. The cost claim is read as: set-up (profiles and truncated convolutions) plus one draw, in arithmetic operations and table look-ups, given the tables; it holds for every $k_{\max}\ge0$ and any upper bound $B$ on the block sizes (Proposition 2.4), with per-draw cost $O(k_{\max}+p)$ after an $O(\sum_b2^{|C_b|})$ preprocessing. The draft's last sentence of P1 is read in two ways, both proved: literally ($\pi_0$ differs from the product of the independent block posteriors $r_b/R_b$: Proposition 2.6(d), for every beta-binomial prior with $p\ge2$, every $L\ge1$ and every $k_{\max}\ge0$; for $p=1$ it can fail) and in the strong sense (no factorisation over blocks at all: Proposition 2.6(b)–(c), which needs $L\ge2$ and $k_{\max}\ge1$ and is false at $k_{\max}=0$; under a binding cap $1\le k_{\max}<p$ no weights factorise, Proposition 2.6(e)).
3. *T1.* Nothing beyond the definitions; (ii) requires $x_\Sigma(S)<1$ as stated, and the proof shows $1-x_\Sigma+\delta/A_0=1-x>0$, so $\Psi_{\rm off}$ is always defined on that event.
4. *L1.* The first bound requires $\varphi^2(S)>0$ (i.e. $G_S\succ0$), as the statement says. The $O(|S|/n)$ reading over a family of models follows from L1 under a *uniform* lower bound $\varphi^2(S)\ge\varphi_0^2>0$ on that family; this is sufficient, not necessary (Remark 4.3(a),(d)); without it $\Delta_{\det}$ can be $\tfrac12\log n+o(1)$ (Remark 4.3(b)). Added: $\Delta_{\det}(S)\ge0$ always, with equality iff $S$ is block-orthogonal (Theorem 4.4).
5. *L2.* $G_{S,0}\succ0$ (as stated; it concerns the nonempty blocks of $S$) and $\kappa(S)<1$; the $O(n\kappa)$ reading of $\nu\Psi_{\rm off}$ needs in addition $\kappa\le\kappa_0<1$ and residual fractions $1-x_\Sigma(S),1-x(S)\ge\eta>0$, with a constant depending on $(a_0,\kappa_0,\eta)$, or $(A+\tfrac12)/\epsilon^2$ when $a_0\le An$, $1-\kappa_0\ge\epsilon$, $\eta\ge\epsilon$ (Corollary 5.3).
6. *L3.* $p(S^\ast)>0$, i.e. $S^\ast\in\mathcal S$ (as stated; Remark 6.4). The "hence" clause holds for any one of deterministic, in-probability or almost-sure convergence (Corollary 6.3).
7. *L7.* The consequence needs $\delta>0$ (at $\delta=0$ the draft's $\lceil1/\delta\rceil$ is undefined); the identity needs nothing and holds for all real $\delta$. The greedy schedule is used only through "a feasible $\phi'$ gives $\phi_t\ge\phi'$" (Section 0.1); $T$ is finite by L4(iii) and, independently, by the bound proved.
8. *L5.* $\sigma_d,\lambda_0>0$ and $c>0$ as stated; (8.1) is used at $\lambda=2\delta$ with $\delta\le\lambda_0$ and $\phi=\phi_{t-1}$ for the step bound, and at every $\phi\in[0,1]$ as $\lambda\downarrow0$ for the variance bound.

**Flags for the draft (wording, not mathematics).**
- *Section 2, cap.* State $k_{\max}\le p$ (or replace $k_{\max}$ by $\min\{k_{\max},p\}$), see item 1.
- *P1(ii) cost.* Suggest "set-up $O(\sum_b2^{|C_b|}+Lk_{\max}B)$ arithmetic operations given the tables, and $O(k_{\max}+p)$ per draw after preprocessing".
- *P1, last sentence.* Suggest "under a beta-binomial prior with $p\ge2$, $\pi_0$ is not the product of the block posteriors; indeed with at least two blocks and $k_{\max}\ge1$ it does not factorise over blocks at all (Proposition 2.6)". Do not write "never factorises": at $k_{\max}=0$ it does (Proposition 2.6(a)). With at least two blocks: under a binding cap $1\le k_{\max}<p$ no size weights give a product (Proposition 2.6(e)), and without a cap only geometric weights can (Remark 2.7); with one block every distribution is trivially a product.
- *T1.* The determinant term can be stated with its sign: $\Delta_{\det}\ge0$, equality iff block-orthogonal (Theorem 4.4). Then $d(S)\ge\nu\Psi(S)$ for every $S$.
- *L1.* Any use of L1's first bound to conclude $\Delta_{\det}=O(|S|/n)$ uniformly over a family of models should state the uniform lower bound on $\varphi^2$ over that family; Remark 4.3(b) gives the example showing that some such hypothesis is needed for that conclusion, and Remark 4.3(d) that this particular one is not necessary. (The first bound also yields weaker rates, e.g. $O(|S|/\sqrt n)$ when $\varphi^2\ge n^{-1/2}$, and the second bound needs no eigenvalue hypothesis at all.)
- *L2.* State the interpretation as Corollary 5.3, with the two residual fractions bounded below.
- *L3.* The lemma can be stated in the sharper form (6.3): $\inf_{\phi\in[0,1]}q_\phi(S^\ast)=\min\{\pi_0(S^\ast),\pi(S^\ast)\}$, and on any interval.
- *L7.* Its hypothesis can be replaced by the two endpoint conditions of Corollary 7.3; the stage count for T2(iii) then needs concentration of $q_{1+\delta}$ at $S_0$ only, not of $q_\psi$ uniformly in $\psi\in(1,1+\delta]$. "for every $\delta\ge0$" can read "for every real $\delta$" in the identity; the consequence needs $\delta>0$.
- *L5, note for the prover.* The sentence on far models should say that mass $e^{-\Theta(n)}$ at distance $\Theta(n)$ *above the mean* forces $\sigma_d^2=\Omega(n)$ once $\lambda_0$ exceeds a constant (Remark 8.4(b)); the range of $d$ alone forces nothing.
- *Notation.* The draft uses $c$, $\rho$, $\delta$, $T$ and $B$ each with two meanings; this proof keeps the draft's symbols and disambiguates in Section 0.1.

**Numerical checks** (`check_elementary_I.py`, seed 1, local, output in `check_elementary_I.out`): (eq:m) against quadrature over $\sigma^2$ (3 models); P1(i) normaliser, P1(ii) exact law of the sampler by enumeration of all paths ($p=7$, three blocks, $k_{\max}=3$, max abs error $6\cdot10^{-17}$) and a $2\cdot10^5$-draw Monte Carlo $\chi^2$ test, P1(iii) marginals and conditional-on-size product form, the $\mathrm{BB}(1,p)$ non-factorisation for $p\in\{2,5,20\}$; T1(i)–(ii) on all $64$ models of a correlated $n=30$, $p=6$ design (48 of them have $x_\Sigma<1$), T1(iii) on a block-orthogonal design (all 64 models), Example 3.3 ($x_\Sigma=1.516$); L1 both bounds on all models and the identical-columns example for $n\in\{10,10^2,10^3,10^4\}$; Theorem 4.4 on 30 designs (including singular ones) and the equality case on a block-orthogonal design; L2 both bounds on all models with $\kappa<1$; L3 on random bridges, including the interval form; L7's three expressions for $\phi\in\{-0.7,0,0.2,0.4,1\}$ and $\delta\in\{-0.3,0.25,0.3,0.5,1.1\}$, and its consequence on an instance with $q_\psi(S^\ast)\ge0.72$ on $[0,1.25]$ but $q_2(S^\ast)=5.6\cdot10^{-4}$ (greedy schedule $0,0.668,1$; $T=2\le4$); L5 on a random bridge with $(\lambda_0,\sigma_d)=(0.4,1.89)$ computed from (8.1) ($T=2\le4$, $\Lambda=1.30\le1.89$); the two bridges of Remark 8.4(b); Proposition 2.6(d) for beta-binomial priors with $p\in\{2,3,4\}$ including $\alpha_\pi=\beta_\pi+p-1$, $L=1$ and $k_{\max}=p$ (96 cases, all differ) and the $p=1$ exception; Remark 2.7 with three blocks (geometric weights factorise, pairwise-window-geometric and $\mathrm{BB}(1,p)$ weights do not). 36 checks, 36 pass. Independent check scripts by the reviewers are under `review/opus_A/`, `review/opus_B/` and `review/opus_C/`.
