# Proof of Theorems T7 (no supersets) and T8 (selection consistency and the HPM), with T10 (per-variable screening) as a by-product

Supplement material for *Split-and-merge with an exact merge: composite-start sequential Monte Carlo for Bayesian variable selection*, draft of 14 October 2026. Notation follows Section 2 of the draft; the standing assumptions are those of Section 4 ("Standing assumptions for Theorems T6–T8"). Results assumed: Theorem T6 exactly as stated, and Lemma L6 (parts (i), (iii), (iv), (v)). No other numbered result is used. In particular T9 and T10 are not used; T10 is proved here.

**Summary of the outcome.**

*(audit 2026-10-15)* Throughout this document, "the draft", "the statement" and "as stated" refer to the draft frozen on 14 October 2026, from which the statements of §0.2 were taken. The current draft has since incorporated the precisions recorded here: T7 names $\omega_n$ and states the rate $O_{\mathbb P}(\sqrt{\log n/n}+e^{-\omega_n})$, and T8 and T10 state the beta-min condition with $\sigma_\star^2$ in place of $\sigma_\star^2+M$. Theorems 7.1, 8.1 and 8.2 cover the current T7, T8 and T10 exactly.

- **T7 (convergence) is true as stated**, for every $\omega_n\to\infty$. **T7 (rate) is true once the $m_n$ in its hypothesis is made precise:** the proof gives
$$\Pi(\{S\supsetneq S_0\}\mid y)=O_{\mathbb P}\big(\sqrt{\log n/n}+e^{-\omega_n}\big),$$
so the stated rate $O_{\mathbb P}(\sqrt{\log n/n})$ holds when the sparse eigenvalue condition is assumed up to $m_n+s_0$ with $\omega_n\ge\tfrac12\log n$ (Theorem 7.1; the explicit size range is displayed there). With T6's example $\omega_n=\log\log n$ the proof gives only $O_{\mathbb P}(\sqrt{\log n/n}+1/\log n)$. The term $e^{-\omega_n}$ is the posterior mass above $m_n$; the supersets of size at most $m_n$ contribute $O_{\mathbb P}(\sqrt{\log n/n})$ for every $\omega_n=O(\log n)$ under (SE) at that $m_n$. The supersets are counted size by size, with the exact integrated-variance Bayes factor and a truncated exponential moment of a $\chi^2$ variable: the posterior sum is never bounded by a count of models times a maximal Bayes factor (the only union bounds are the ones defining the good event of Section 2), and the approximation $e^{\chi^2/2}$ is never integrated.
- **T8 (i), (ii) are true as stated, and (iii) holds in the same form as T7's rate** (Theorem 8.1). The proof uses the beta-min condition only through the weaker requirement $\min_{j\in S_0}(\beta_j^\star)^2\ge M_n^\beta\,\sigma_\star^2\log n/(n\varphi_0^2)$: the factor $\sigma_\star^2+M$ of the statement can be replaced by $\sigma_\star^2$, because every underfitting model is compared with its union with $S_0$, which fits the whole signal, so the unfitted signal never inflates the relevant residual variance (Remark 8.3).
- **T10 is true as stated** and falls out of the underfitting step of T8 with the beta-min condition applied to one coordinate (Theorem 8.2).

The dependence on T6 is confined to the convergence statements. The rate statements use Lemma 3.1, which is T6's argument made quantitative; it is proved in full below, so the rate statements do not rest on T6.

---

## 0. Setting, notation and the precise statements

### 0.1 Standing assumptions and the objects used

Throughout, $n\to\infty$ along a sequence of fixed designs $X=X_n\in\mathbb R^{n\times p}$ with standardised columns $\|x_j\|^2=n$, and:

- (A1) $s_0=|S_0|$ is fixed ($s_0\ge 0$) and $p=p_n\le n^A$ for a fixed $A\ge1$;
- (A2) the model prior is $\mathrm{BB}(1,p)$ with a cap $k_{\max}\ge s_0$ (any cap; $\lfloor n/2\rfloor$ in particular);
- (A3) $\|\mu\|^2\le nM$ for a fixed $M\ge 0$, where $\mu=X\beta^\star$;
- (A4) $\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2>0$, i.e. $\lambda_{\min}(G_{S_0})\ge n\varphi_0^2$.

The data are $y=\mu+\varepsilon$, $\varepsilon\sim N_n(0,\sigma_\star^2 I_n)$; $\mathbb P_0$ and $\mathbb E_0$ refer to $\varepsilon$. The variance prior is $\mathrm{IG}(a_0,b_0)$ with $a_0,b_0>0$ and density $p_{\mathrm{IG}}(v)=\frac{b_0^{a_0}}{\Gamma(a_0)}v^{-a_0-1}e^{-b_0/v}$. We use the quantities of Section 2.1 of the draft:
$$G_S=X_S^\top X_S,\quad H_S=(n+1)G_S+I_{|S|},\quad D_S=\frac{\det H_S}{\det(G_S+I)},\quad t_S=n\,z_S^\top H_S^{-1}z_S,\quad Q_S=y^\top y-t_S,\quad \nu=a_0+\tfrac n2,$$
$$m(S)=C_n\,D_S^{-1/2}(2b_0+Q_S)^{-\nu},\qquad C_n=\pi^{-n/2}(2b_0)^{a_0}\frac{\Gamma(\nu)}{\Gamma(a_0)} .$$
$P_S$ is the orthogonal projection onto the column span of $X_S$ ($P_\emptyset=0$). The per-model prior weights are $w(k)=B(1+k,\,2p-k)/B(1,p)$, and $p(S)=w(|S|)\mathbf 1\{|S|\le k_{\max}\}/W$. For $|S|,|S'|\le k_{\max}$ one has $p(S)/p(S')=w(|S|)/w(|S'|)$; the ratios $w(k)/w(k')$ are defined for all $0\le k,k'\le p$ whether or not the sizes are below the cap, and every comparison below is written with $w$ so that the cap never obstructs a comparison. The posterior is $\Pi(S\mid y)=p(S)m(S)/Z$ with $Z=\sum_S p(S)m(S)\ge p(S_0)m(S_0)$ (recall $s_0\le k_{\max}$).

**The dimension threshold.** For a sequence $\omega_n\to\infty$ put, as in T6,
$$m_n=\Big\lceil\frac{s_0\log(2p)+\frac{s_0+1}{2}\log n+\omega_n}{\log 2}\Big\rceil .$$
We take $\omega_n=O(\log n)$, as in T6's "in particular" clause; with $p\le n^A$ this gives $m_n\le C_m\log n$ for all $n\ge3$, with $C_m=C_m(s_0,A,\sup_{n\ge3}\omega_n/\log n)$. This restriction costs nothing: $m_n$ is nondecreasing in $\omega_n$, so if (SE) below holds for $m_n(\omega_n)$ with some $\omega_n\to\infty$, it holds for $m_n(\omega_n')$ with $\omega_n'=\min(\omega_n,\tfrac12\log n)$, which still tends to infinity, and every statement below applied with $\omega_n'$ gives the corresponding statement for $\omega_n$ (the rate statements because $\omega_n'\ge\frac12\log n$ whenever $\omega_n\ge\frac12\log n$). Nothing else about $\omega_n$ is used except in the rate statements, where $e^{-\omega_n}$ appears explicitly.

**The sparse eigenvalue condition** (hypothesis of T7, inherited by T8 and T10):
$$\text{(SE)}\qquad \lambda_{\min}(\Gamma_S)\ge\varphi_0^2\quad\text{for every }S\subseteq[p]\text{ with }|S|\le m_n+s_0 .$$
Under (SE), $X_S$ has full column rank for every $|S|\le m_n+s_0$. (SE) implies (A4). For the rate statements the relevant instance is $\omega_n=\frac12\log n$, i.e.
$$\text{(SE}_{1/2}\text{)}\qquad \lambda_{\min}(\Gamma_S)\ge\varphi_0^2\quad\text{for every }|S|\le s_0+\Big\lceil\frac{s_0\log(2p)+(\frac{s_0}2+1)\log n}{\log2}\Big\rceil .$$

**Sets attached to a model.** For a model $S$ write
$$J(S)=S_0\setminus S,\qquad J'(S)=S\setminus S_0,\qquad S'=S\cup S_0=S_0\cup J'(S).$$
$S$ is a *superset* if $J(S)=\emptyset$ and $J'(S)\ne\emptyset$; it is *underfitting* if $J(S)\ne\emptyset$. If $|S|\le m_n$ then $|S'|\le m_n+s_0$, so (SE) applies to $S$ and to $S'$.

**Constants.** The following constants depend only on $(s_0,A)$ and are fixed throughout:
$$C_A=8+3A,\qquad j_0=\lceil(2A+1)s_0\rceil+1,\qquad C_2=2s_0+3\big(Aj_0+s_0+\log(j_0+1)+1\big).$$
Also $\eta_n=\dfrac{1}{n(n+1)\varphi_0^2}$ and $\tau_j=C_A\,j\log n$ for $j\ge1$. The symbol $n_0$ denotes a threshold depending only on $(s_0,A,\varphi_0,\sigma_\star^2,M,a_0,b_0,C_m)$, enlarged finitely many times; "for $n\ge n_0$" means "for all $n$ beyond that threshold". Constants named $K$ with subscripts are finite and depend only on the same quantities.

**Probabilistic notation.** $B_n=O_{\mathbb P}(a_n)$ means that $B_n/a_n$ is tight under $\mathbb P_0$; $B_n=o_{\mathbb P}(1)$ means $B_n\to0$ in $\mathbb P_0$-probability. The letter $K$ denotes a Markov constant in Proposition 4.2 and Theorem 7.1; the size variable of the untruncated prior in Lemma 3.1 is written $K_{\mathrm{BB}}$. When $s_0=0$, a minimum over the empty set is $+\infty$, so (BM) below is void.

### 0.2 The precise statements proved

**Theorem 7.1 (T7, made precise).** Assume (A1)–(A4), let $\omega_n\to\infty$ with $\omega_n=O(\log n)$, and assume (SE) for the corresponding $m_n$. Then

(a) $\Pi(\{S\supsetneq S_0,\ |S|\le m_n\}\mid y)=O_{\mathbb P}(\sqrt{\log n/n})$;

(b) $\Pi(\{S\supsetneq S_0\}\mid y)\to0$ in $\mathbb P_0$-probability;

(c) $\Pi(\{S\supsetneq S_0\}\mid y)=O_{\mathbb P}\big(\sqrt{\log n/n}+e^{-\omega_n}\big)$. In particular, under (SE$_{1/2}$) (the case $\omega_n=\tfrac12\log n$, which keeps $m_n=O(\log n)$; equivalently, under (SE) for any $\omega_n\ge\tfrac12\log n$), $\Pi(\{S\supsetneq S_0\}\mid y)=O_{\mathbb P}(\sqrt{\log n/n})$, which is T7's rate.

**Theorem 8.1 (T8, made precise).** Assume the hypotheses of Theorem 7.1 and the beta-min condition
$$\min_{j\in S_0}(\beta_j^\star)^2\ \ge\ M_n^\beta\,\frac{\sigma_\star^2\log n}{n\varphi_0^2},\qquad M_n^\beta\to\infty, \tag{BM}$$
which is implied by the condition of T8 since $M\ge0$. Then

(i) $\Pi(S_0\mid y)\to1$ in $\mathbb P_0$-probability, hence also in $L^1(\mathbb P_0)$;

(ii) $\mathbb P_0(\mathrm{HPM}\ne S_0)\le 2\,\mathbb E_0[1-\Pi(S_0\mid y)]\to0$;

(iii) $1-\Pi(S_0\mid y)=O_{\mathbb P}\big(\sqrt{\log n/n}+e^{-\omega_n}\big)$; in particular $O_{\mathbb P}(\sqrt{\log n/n})$ under (SE$_{1/2}$), i.e. when $\omega_n\ge\tfrac12\log n$.

**Theorem 8.2 (T10).** Assume the hypotheses of Theorem 7.1, let $M_n^\beta\to\infty$ and
$$J_n=\Big\{j\in S_0:(\beta_j^\star)^2\ge M_n^\beta\,\frac{(\sigma_\star^2+M)\log n}{n\varphi_0^2}\Big\}.$$
Then $\Pi(\{S:S\supseteq J_n\}\mid y)\to1$ in $\mathbb P_0$-probability; more precisely $1-\Pi(\{S\supseteq J_n\}\mid y)=O_{\mathbb P}(\sqrt{\log n/n}+e^{-\omega_n})$. In particular $\min_{j\in J_n}\mathrm{PIP}_j\to1$ in probability and $\mathbb P_0(J_n\subseteq\text{median model})\to1$. The conclusion holds with $\sigma_\star^2$ in place of $\sigma_\star^2+M$ in the definition of $J_n$.

In Theorem 8.2 no condition is imposed on the coefficients outside $J_n$.

### 0.3 Plan

Section 1 collects deterministic facts: the ridge smoother $M_S$ and its monotonicity in $S$ (Lemma 1.1), determinant ratios (Lemma 1.2), prior ratios (Lemma 1.3), the signal lower bound (Lemma 1.4) and two $\chi^2$ facts (Lemma 1.5). Section 2 defines the good event $\mathcal G_n$ and lists what holds on it. Section 3 proves the quantitative dimension bound (Lemma 3.1). Section 4 bounds the supersets size by size (Proposition 4.1) and proves Theorem 7.1. Section 5 bounds a single underfitting model against its union with $S_0$ (Lemma 5.1), adds the signal (Lemma 5.2), and proves Theorems 8.1 and 8.2. Section 6 lists hypotheses added, where T6 is used, and the steps to re-check.

---

## 1. Deterministic preliminaries

### 1.1 The ridge smoother and its monotonicity

For a model $S$ define the $n\times n$ matrix
$$M_S:=n\,X_SH_S^{-1}X_S^\top,\qquad\text{so that}\qquad t_S=y^\top M_Sy,\qquad Q_S=y^\top(I-M_S)y .$$
Let $h(\lambda)=\dfrac{n\lambda}{(n+1)\lambda+1}$ for $\lambda\ge0$.

**Lemma 1.1.** (a) $M_S=h(X_SX_S^\top)$ in the sense of the functional calculus for symmetric positive semidefinite matrices. Consequently $M_S$ has the same eigenvectors as $X_SX_S^\top$; its eigenvalue on an eigenvector of $X_SX_S^\top$ with eigenvalue $\lambda$ is $h(\lambda)$, and $M_S$ vanishes on the orthogonal complement of the column span of $X_S$.

(b) $0\preceq M_S\preceq\frac{n}{n+1}P_S\preceq P_S$.

(c) If $X_S$ has full column rank and $\lambda_{\min}(G_S)\ge n\varphi_0^2$, then $M_S\succeq(1-\eta_n)\frac{n}{n+1}P_S$ with $\eta_n=\dfrac{1}{n(n+1)\varphi_0^2}$.

(d) If $S\subseteq T$ then $M_S\preceq M_T$; hence $t_S\le t_T$ and $Q_S\ge Q_T$.

*Proof.* (a) With $a=n+1$, the push-through identity $X_S(aX_S^\top X_S+I)^{-1}=(aX_SX_S^\top+I)^{-1}X_S$ (both sides equal $(aX_SX_S^\top+I)^{-1}X_S(aX_S^\top X_S+I)(aX_S^\top X_S+I)^{-1}$, and $X_S(aX_S^\top X_S+I)=(aX_SX_S^\top+I)X_S$) gives
$$M_S=n\,(aX_SX_S^\top+I)^{-1}X_SX_S^\top=h(X_SX_S^\top),$$
since $h(\lambda)=n\lambda/(a\lambda+1)$ and the two matrices $(aX_SX_S^\top+I)^{-1}$ and $X_SX_S^\top$ commute. The remaining claims restate the functional calculus; the nonzero eigenvalues of $X_SX_S^\top$ are those of $G_S$, and the column span of $X_S$ is the span of the eigenvectors with nonzero eigenvalue.

(b) $h$ is increasing on $[0,\infty)$ with $h(0)=0$ and $h(\lambda)<\lim_{\lambda\to\infty}h(\lambda)=\frac{n}{n+1}$. By (a), $M_S$ has eigenvalues in $[0,\frac n{n+1})$ on the column span of $X_S$ and $0$ on its complement, which is (b).

(c) Under the hypotheses, the nonzero eigenvalues of $X_SX_S^\top$ are the eigenvalues of $G_S$, all at least $n\varphi_0^2$, and the eigenvectors with nonzero eigenvalue span the column space of $X_S$. By (a) and the monotonicity of $h$, on that column space $M_S\succeq h(n\varphi_0^2)P_S$, and
$$h(n\varphi_0^2)=\frac{n}{n+1}\cdot\frac{n\varphi_0^2}{n\varphi_0^2+\frac1{n+1}}=\frac{n}{n+1}\Big(1-\frac{1}{(n+1)n\varphi_0^2+1}\Big)\ \ge\ \frac{n}{n+1}(1-\eta_n).$$

(d) Write $h(\lambda)=\frac{n}{n+1}\big(1-\frac{1}{(n+1)\lambda+1}\big)$. If $0\preceq B_1\preceq B_2$ then $(n+1)B_1+I\preceq(n+1)B_2+I$, both positive definite, so $((n+1)B_2+I)^{-1}\preceq((n+1)B_1+I)^{-1}$ and therefore $h(B_1)\preceq h(B_2)$: $h$ is operator monotone on the positive semidefinite cone. Since $X_SX_S^\top=\sum_{i\in S}x_ix_i^\top\preceq X_TX_T^\top$ for $S\subseteq T$, (a) gives $M_S\preceq M_T$. $\square$

**Corollary 1.1′ (differences).** Let $S\subseteq T$, with $X_T$ of full column rank and $\lambda_{\min}(G_T)\ge n\varphi_0^2$ (so $X_S$ also has full column rank and $\lambda_{\min}(G_S)\ge n\varphi_0^2$ by interlacing). Then for every $u\in\mathbb R^n$,
$$\frac{n}{n+1}\Big[\|(P_T-P_S)u\|^2-\eta_n\|P_Tu\|^2\Big]\ \le\ u^\top(M_T-M_S)u\ \le\ \frac{n}{n+1}\Big[\|(P_T-P_S)u\|^2+\eta_n\|P_Su\|^2\Big].$$

*Proof.* Upper bound: $M_T\preceq\frac n{n+1}P_T$ and $M_S\succeq(1-\eta_n)\frac n{n+1}P_S$ give $M_T-M_S\preceq\frac n{n+1}(P_T-P_S)+\eta_n\frac n{n+1}P_S$, and $P_T-P_S$ is the orthogonal projection onto $\mathrm{range}(X_T)\ominus\mathrm{range}(X_S)$ since $\mathrm{range}(X_S)\subseteq\mathrm{range}(X_T)$. Lower bound: symmetric, with the roles of the two bounds of Lemma 1.1 exchanged. $\square$

### 1.2 Determinant ratios

Let $f(\lambda)=\dfrac{(n+1)\lambda+1}{\lambda+1}$ for $\lambda\ge0$; $f$ is increasing, $f(0)=1$, $f(\lambda)<n+1$, and $D_S=\prod_{i=1}^{|S|}f(\lambda_i(G_S))$ because $H_S$ and $G_S+I$ are simultaneously diagonalisable. In particular $1\le D_S\le(n+1)^{|S|}$ for every $S$.

**Lemma 1.2.** Let $S\subseteq T$ and $j=|T|-|S|$.

(a) $D_T/D_S\le(n+1)^{j}$.

(b) If $\lambda_{\min}(G_T)\ge n\varphi_0^2$, then $D_T/D_S\ge f(n\varphi_0^2)^{j}\ge\Big[(n+1)\Big(1+\frac{1}{n\varphi_0^2}\Big)^{-1}\Big]^{j}$.

*Proof.* Order eigenvalues increasingly. $G_S$ is a principal submatrix of $G_T$, so by Cauchy interlacing $\lambda_i(G_T)\le\lambda_i(G_S)\le\lambda_{i+j}(G_T)$ for $1\le i\le|S|$. Since $f$ is increasing,
$$\prod_{i=1}^{|S|}f(\lambda_i(G_T))\ \le\ D_S\ \le\ \prod_{i=1}^{|S|}f(\lambda_{i+j}(G_T))=\prod_{i=j+1}^{|T|}f(\lambda_i(G_T)).$$
Dividing $D_T=\prod_{i=1}^{|T|}f(\lambda_i(G_T))$ by the left inequality gives $D_T/D_S\le\prod_{i=|S|+1}^{|T|}f(\lambda_i(G_T))\le(n+1)^j$, which is (a). Dividing by the right inequality gives $D_T/D_S\ge\prod_{i=1}^{j}f(\lambda_i(G_T))\ge f(n\varphi_0^2)^j$, and
$$f(n\varphi_0^2)=\frac{(n+1)n\varphi_0^2+1}{n\varphi_0^2+1}\ \ge\ (n+1)\frac{n\varphi_0^2}{n\varphi_0^2+1}=(n+1)\Big(1+\frac1{n\varphi_0^2}\Big)^{-1}. \qquad\square$$

### 1.3 Prior ratios under $\mathrm{BB}(1,p)$

By L6(i) with $b_\pi=p$, $w(k+1)/w(k)=(k+1)/(2p-k-1)$ for $0\le k\le p-1$.

**Lemma 1.3.** (a) For $0\le k<k'\le p$: $\dfrac{w(k)}{w(k')}\le(2p)^{k'-k}$.

(b) For $j\ge1$ with $s_0+j\le p$:
$$\sum_{J\subseteq[p]\setminus S_0,\ |J|=j}\frac{w(s_0+j)}{w(s_0)}=\binom{p-s_0}{j}\frac{w(s_0+j)}{w(s_0)}\ \le\ 2\binom{s_0+j}{j}2^{-j}\ \le\ 2\,(j+1)^{s_0}2^{-j}.$$
(If $s_0\ge1$ the factor $2$ can be dropped.)

*Proof.* (a) $w(k)/w(k+1)=(2p-k-1)/(k+1)\le2p$; multiply $k'-k$ such ratios. (b) Writing both factors as products over $i=0,\dots,j-1$,
$$\binom{p-s_0}{j}\frac{w(s_0+j)}{w(s_0)}=\prod_{i=0}^{j-1}\frac{p-s_0-i}{i+1}\cdot\frac{s_0+i+1}{2p-s_0-i-1}=\binom{s_0+j}{j}\prod_{i=0}^{j-1}\frac{p-s_0-i}{2p-s_0-i-1}.$$
Each factor satisfies $2(p-s_0-i)\le2p-s_0-i-1$ as soon as $s_0+i\ge1$, which holds for every $i\ge1$ and, if $s_0\ge1$, for $i=0$ as well; when $s_0=0$ the factor for $i=0$ equals $p/(2p-1)\le1$. The denominators are positive because $i\le j-1\le p-s_0-1$ gives $2p-s_0-i-1\ge p$. Finally $\binom{s_0+j}{j}=\prod_{i=1}^{s_0}\frac{j+i}{i}\le(j+1)^{s_0}$. $\square$

### 1.4 The signal left by an underfitting model

**Lemma 1.4.** Let $S$ be a model with $J=S_0\setminus S\ne\emptyset$ and $S'=S\cup S_0$, and assume $\lambda_{\min}(G_{S'})\ge n\varphi_0^2$. Then
$$\Delta_S:=\|(I-P_S)\mu\|^2\ \ge\ n\varphi_0^2\,\|\beta^\star_J\|^2 .$$

*Proof.* $\mu=X_{S_0}\beta^\star_{S_0}=X_{S_0\cap S}\beta^\star_{S_0\cap S}+X_J\beta^\star_J$ and $(I-P_S)X_{S_0\cap S}=0$, so $(I-P_S)\mu=(I-P_S)X_J\beta^\star_J$. The residual of an orthogonal projection is a minimum: $\|(I-P_S)X_J\beta^\star_J\|^2=\min_{\gamma\in\mathbb R^{|S|}}\|X_J\beta^\star_J-X_S\gamma\|^2$. Since $J\cap S=\emptyset$ and $S'=S\sqcup J$, every vector $X_J\beta^\star_J-X_S\gamma$ equals $X_{S'}\theta$ with $\theta=(\beta^\star_J,-\gamma)$ in the coordinates of $S'$, and $\|X_{S'}\theta\|^2=\theta^\top G_{S'}\theta\ge\lambda_{\min}(G_{S'})\|\theta\|^2\ge n\varphi_0^2\|\beta^\star_J\|^2$. $\square$

### 1.5 Two chi-square facts

**Lemma 1.5.** Let $\chi^2_d$ denote a chi-square variable with $d\ge1$ degrees of freedom.

(a) (Laurent–Massart) For every $x>0$: $\mathbb P(\chi^2_d\ge d+2\sqrt{dx}+2x)\le e^{-x}$ and $\mathbb P(\chi^2_d\le d-2\sqrt{dx})\le e^{-x}$. Moreover $d+2\sqrt{dx}+2x\le2d+3x$.

(b) (Truncated exponential moment) For every $\tau>0$,
$$\mathbb E\big[e^{\chi^2_d/2}\,\mathbf 1\{\chi^2_d\le\tau\}\big]=\frac{(\tau/2)^{d/2}}{\Gamma(d/2+1)}\ \le\ \Big(\frac{e\,\tau}{d}\Big)^{d/2}.$$

*Proof.* (a) is Lemma 1 of Laurent and Massart (2000, Ann. Statist. 28, 1302–1338), and $2\sqrt{dx}\le d+x$. (b) The density of $\chi^2_d$ is $x^{d/2-1}e^{-x/2}/(2^{d/2}\Gamma(d/2))$, so the truncated moment equals $\int_0^\tau x^{d/2-1}dx/(2^{d/2}\Gamma(d/2))=\tau^{d/2}/(2^{d/2}(d/2)\Gamma(d/2))$, which is the stated equality. The inequality $\Gamma(x+1)\ge(x/e)^x$ for $x>0$ (from $\Gamma(x+1)=\int_0^\infty t^xe^{-t}dt\ge x^x\int_x^\infty e^{-t}dt=x^xe^{-x}$) gives the bound. $\square$

Lemma 1.5(b) is the only place where the exponential of a chi-square is integrated, and it is integrated only after truncation; the exact Bayes factor is never replaced by $e^{\chi^2/2}$.

---

## 2. The good event

Fix the sequence $\omega_n$ and hence $m_n\le C_m\log n$. Recall $C_A=8+3A$, $\tau_j=C_Aj\log n$, $j_0=\lceil(2A+1)s_0\rceil+1$, $C_2=2s_0+3(Aj_0+s_0+\log(j_0+1)+1)$.

For $J\subseteq[p]\setminus S_0$ with $X_{S_0\cup J}$ of full column rank put
$$\chi^2_J:=\sigma_\star^{-2}\|(P_{S_0\cup J}-P_{S_0})\varepsilon\|^2 ,$$
which is a chi-square variable with $|J|$ degrees of freedom, because $P_{S_0\cup J}-P_{S_0}$ is an orthogonal projection of rank $|S_0\cup J|-|S_0|=|J|$ (Corollary 1.1′). For an underfitting model $S$ (with $S'=S\cup S_0$ of full column rank) put
$$N_S:=\|(P_{S'}-P_S)\varepsilon\|^2,\qquad \sigma_\star^{-2}N_S\sim\chi^2_{|J(S)|},\quad |J(S)|\le s_0 .$$

**Definition 2.1 (the good event).** $\mathcal G_n$ is the intersection of the four events

- (G1) $\big|\,\|\varepsilon\|^2-n\sigma_\star^2\big|\le3\sigma_\star^2\sqrt{n\log n}$;
- (G2) $\|P_T\varepsilon\|^2\le\sigma_\star^2\,C_A(m_n+s_0)\log n$ for every $T$ with $1\le|T|\le m_n+s_0$;
- (G3) $\chi^2_J\le\tau_{|J|}$ for every $J\subseteq[p]\setminus S_0$ with $1\le|J|\le m_n$;
- (G4) $N_S\le\sigma_\star^2C_2\log n$ for every underfitting $S$ with $|S|\le m_n$ and $|J'(S)|\le j_0$.

**Lemma 2.2.** Under (A1) and (SE), for $n\ge9$: $\mathbb P_0(\mathcal G_n^c)\le5/n$.

*Proof.* (G1): apply Lemma 1.5(a) to $\|\varepsilon\|^2/\sigma_\star^2\sim\chi^2_n$ with $x=\log n$: outside an event of probability $2/n$, $n-2\sqrt{n\log n}\le\|\varepsilon\|^2/\sigma_\star^2\le n+2\sqrt{n\log n}+2\log n$, and $2\log n\le\sqrt{n\log n}$ for $n\ge9$.

(G2): for $|T|=k$, $\|P_T\varepsilon\|^2/\sigma_\star^2$ is chi-square with $\mathrm{rank}(X_T)\le k$ degrees of freedom, hence stochastically at most $\chi^2_k$. There are $\binom pk\le p^k$ such $T$. With $x_k=k(\log p+1)+\log n$, Lemma 1.5(a) and a union bound give
$$\mathbb P_0\Big(\exists T,\ |T|=k:\ \|P_T\varepsilon\|^2/\sigma_\star^2>k+2\sqrt{kx_k}+2x_k\Big)\le p^ke^{-x_k}=\frac{e^{-k}}{n},$$
and summing over $k\ge1$ gives at most $1/n$. On the complement, for every $k\le m_n+s_0$,
$$k+2\sqrt{kx_k}+2x_k\le2k+3x_k=5k+3k\log p+3\log n\le 5k\log n+3Ak\log n+3k\log n=C_Ak\log n,$$
using $\log n\ge1$ and $\log p\le A\log n$; the maximum over $k\le m_n+s_0$ is at most $C_A(m_n+s_0)\log n$.

(G3): the same computation with the $\binom{p-s_0}{j}\le p^j$ variables $\chi^2_J$, $|J|=j$, each exactly $\chi^2_j$, for $1\le j\le m_n$; the exceptional probability is at most $1/n$ and the threshold is $C_Aj\log n=\tau_j$.

(G4): the number of underfitting $S$ with $|J'(S)|\le j_0$ is at most $(2^{s_0}-1)\sum_{j'\le j_0}\binom{p}{j'}\le2^{s_0}(j_0+1)p^{j_0}$ (choose $J'$, then the nonempty $J\subseteq S_0$). Each $N_S/\sigma_\star^2$ is stochastically at most $\chi^2_{s_0}$. Apply Lemma 1.5(a) with $x=j_0\log p+s_0\log2+\log(j_0+1)+\log n$: the union bound gives exceptional probability at most $1/n$, and on the complement $N_S/\sigma_\star^2\le2s_0+3x\le C_2\log n$, using $\log p\le A\log n$, $\log 2\le\log n$, $1\le\log n$. (If $s_0=0$ there is no underfitting model and (G4) is void.)

Altogether $\mathbb P_0(\mathcal G_n^c)\le(2+1+1+1)/n$. $\square$

**Lemma 2.3 (what holds on $\mathcal G_n$).** Assume (A1)–(A4) and (SE). There is $n_0$ such that for $n\ge n_0$, on $\mathcal G_n$:

(a) $\|y\|^2\le4n(M+\sigma_\star^2)$.

(b) For every $S\supseteq S_0$ with $|S|\le m_n+s_0$: $Q_S\ge n\sigma_\star^2(1-\delta_n)$, where
$$\delta_n:=3\sqrt{\frac{\log n}{n}}+\frac{C_A(m_n+s_0)\log n}{n}\ \le\ \tfrac12,\qquad \delta_n\log n\to0 .$$

(c) For every underfitting $S$ with $|S|\le m_n$, writing $V_S:=\|(P_{S'}-P_S)y\|^2$,
$$2b_0+Q_S\ \le\ E_n+V_S,\qquad E_n:=2b_0+\|\varepsilon\|^2+\frac{2}{n+1}\|y\|^2,\qquad n\sigma_\star^2(1-\delta_n)\le E_n\le n\sigma_\star^2(1+\delta_n'') ,$$
where $\delta_n'':=3\sqrt{\log n/n}+\big(2b_0+8(M+\sigma_\star^2)\big)/(n\sigma_\star^2)\to0$.

(d) Put $\rho_n:=\dfrac{16(M+\sigma_\star^2)}{n\varphi_0^2\sigma_\star^2}$. Whenever $B\ge n\sigma_\star^2(1-\delta_n)$,
$$\nu\,\frac n{n+1}\,\frac{\eta_n\|y\|^2}{B}\ \le\ \rho_n .$$
In particular this applies with $B=2b_0+Q_S$ for $S\supseteq S_0$, $|S|\le m_n+s_0$ (by (b)), and with $B=E_n$ (by (c)).

*Proof.* (a) $\|y\|^2\le2\|\mu\|^2+2\|\varepsilon\|^2\le2nM+2n\sigma_\star^2(1+3\sqrt{\log n/n})\le4n(M+\sigma_\star^2)$ by (A3) and (G1), once $3\sqrt{\log n/n}\le1$.

(b) For $S\supseteq S_0$, $(I-P_S)\mu=0$, so by Lemma 1.1(b) $Q_S=y^\top(I-M_S)y\ge y^\top(I-P_S)y=\|(I-P_S)\varepsilon\|^2=\|\varepsilon\|^2-\|P_S\varepsilon\|^2$, and (G1)–(G2) give $Q_S\ge n\sigma_\star^2-3\sigma_\star^2\sqrt{n\log n}-\sigma_\star^2C_A(m_n+s_0)\log n$. Since $m_n\le C_m\log n$, $\delta_n\log n\le3\sqrt{\log^3n/n}+C_A(C_m\log n+s_0)\log^2n/n\to0$, so $\delta_n\le\frac12$ for $n\ge n_0$.

(c) By (SE), Lemma 1.1(c) applies to $S$: $I-M_S\preceq(I-P_S)+\big(\tfrac1{n+1}+\eta_n\tfrac n{n+1}\big)P_S$, hence $Q_S\le\|(I-P_S)y\|^2+\big(\tfrac1{n+1}+\eta_n\big)\|y\|^2\le\|(I-P_S)y\|^2+\frac{2}{n+1}\|y\|^2$ as soon as $n\varphi_0^2\ge1$ (so that $\eta_n\le\frac1{n+1}$). Since $P_S\preceq P_{S'}$, Pythagoras gives $\|(I-P_S)y\|^2=\|(I-P_{S'})y\|^2+\|(P_{S'}-P_S)y\|^2$, and $(I-P_{S'})y=(I-P_{S'})\varepsilon$ because $S'\supseteq S_0$. Thus $\|(I-P_S)y\|^2\le\|\varepsilon\|^2+V_S$, which gives the first claim. The bounds on $E_n$ follow from (G1), (a), and $\frac{2}{n+1}\|y\|^2\le8(M+\sigma_\star^2)$.

(d) $\nu\frac n{n+1}\le\frac n2(1+\frac{2a_0}{n})$ and $\eta_n\|y\|^2\le\frac{4n(M+\sigma_\star^2)}{n(n+1)\varphi_0^2}$ by (a); dividing by $n\sigma_\star^2(1-\delta_n)\ge\frac12n\sigma_\star^2$ gives at most $\frac{(1+2a_0/n)\,4(M+\sigma_\star^2)}{(n+1)\varphi_0^2\sigma_\star^2}\cdot2\le\rho_n$ for $n\ge2a_0$. The same bound holds with $E_n$ in the denominator by (c). $\square$

The reader may note that $E_n$ contains $\|\varepsilon\|^2$ and not $\|y\|^2$: an underfitting model is always compared with $S'=S\cup S_0$, whose residual is pure noise. This is what removes the factor $\sigma_\star^2+M$ from the beta-min condition (Remark 8.3).

---

## 3. Posterior dimension with a rate (T6 made quantitative)

Theorem T6 gives $\Pi(|S|>m_n\mid y)\to0$ in probability. The rate statements need the size of this tail. The following lemma is T6's argument (the note after T6 in the draft) carried out with explicit constants; it is proved in full and uses only L6 and (A3)–(A4).

**Lemma 3.1.** Assume (A2)–(A4). Let $m\ge0$ be any integer sequence. Then
$$\Pi(|S|>m\mid y)\ \le\ 2^{-m}\,(2p)^{s_0}(n+1)^{s_0/2}\,\sqrt n\;\Theta_n^{(m)},\qquad \Theta_n^{(m)}=O_{\mathbb P}(1)\ \text{uniformly in }m,$$
in the sense that $\sup_m\mathbb P_0(\Theta_n^{(m)}>K)\to0$ as $K\to\infty$, uniformly in $n$. In particular, for $m=m_n$ as in T6,
$$\Pi(|S|>m_n\mid y)\ \le\ (1+1/n)^{s_0/2}\,e^{-\omega_n}\,\Theta_n^{(m_n)}=O_{\mathbb P}(e^{-\omega_n}) .$$
No condition on $p$ and no sparse eigenvalue condition is used.

*Proof.* Let $f_0(y)=(2\pi\sigma_\star^2)^{-n/2}\exp\{-\|\varepsilon\|^2/(2\sigma_\star^2)\}$ be the true density of $y$, which is positive everywhere. Since $Z\ge p(S_0)m(S_0)$,
$$\Pi(|S|>m\mid y)\le\frac{N_n}{p(S_0)\,m(S_0)/f_0(y)},\qquad N_n:=\sum_{|S|>m}p(S)\frac{m(S)}{f_0(y)} . \tag{3.1}$$

*Numerator.* Each $m(S)$ is the marginal density of $y$ under a proper prior (a normal slab and a proper inverse-gamma), so $\int m(S)(y)\,dy=1$ by Tonelli's theorem applied to the joint density of $(y,\beta_S,\sigma^2)$, and $\mathbb E_0[m(S)(y)/f_0(y)]=1$. Hence $\mathbb E_0N_n=\sum_{|S|>m}p(S)=p(|S|>m)$. By L6(iii), the untruncated $\mathrm{BB}(1,p)$ size variable $K_{\mathrm{BB}}$ satisfies $\mathbb P(K_{\mathrm{BB}}\ge m+1)\le2^{-m}$, and by L6(iv) the cap multiplies the probability of any event by at most $2$; thus $\mathbb E_0N_n\le2^{1-m}$ and, by Markov's inequality, $N_n=2^{1-m}\,\Theta_n^{(1)}$ with $\Theta_n^{(1)}:=N_n/2^{1-m}\ge0$ and $\mathbb E_0\Theta_n^{(1)}\le1$ for every $m$, so $\mathbb P_0(\Theta_n^{(1)}>K)\le1/K$ uniformly in $n$ and $m$.

*Denominator: the prior.* By L6(v), $p(S_0)\ge\frac{1}{2(2p)^{s_0}}$ since $s_0\le k_{\max}$.

*Denominator: the marginal likelihood.* Integrating $\beta_{S_0}$ out at fixed $\sigma^2=v$ gives (this is the computation behind (2.1) of the draft, i.e. $\det(I_n+X_S\Lambda_S^{-1}X_S^\top)=D_S$ and $y^\top(I_n+X_S\Lambda_S^{-1}X_S^\top)^{-1}y=Q_S$ by Woodbury)
$$m(S_0)=\int_0^\infty(2\pi v)^{-n/2}D_{S_0}^{-1/2}e^{-Q_{S_0}/(2v)}\,p_{\mathrm{IG}}(v)\,dv ,$$
so that
$$\frac{m(S_0)}{f_0(y)}=D_{S_0}^{-1/2}\int_0^\infty\Big(\frac v{\sigma_\star^2}\Big)^{-n/2}\exp\Big\{\frac{\|\varepsilon\|^2}{2\sigma_\star^2}-\frac{Q_{S_0}}{2v}\Big\}p_{\mathrm{IG}}(v)\,dv . \tag{3.2}$$
Two bounds on the integrand. First, $D_{S_0}\le(n+1)^{s_0}$ (Section 1.2). Second, by (A4) and Lemma 1.1(c), $I-M_{S_0}\preceq(I-P_{S_0})+(\frac1{n+1}+\eta_n)P_{S_0}$, and $(I-P_{S_0})y=(I-P_{S_0})\varepsilon$, so
$$Q_{S_0}\le\|(I-P_{S_0})\varepsilon\|^2+R_n\le\|\varepsilon\|^2+R_n,\qquad R_n:=\Big(\frac1{n+1}+\eta_n\Big)\|y\|^2\le\frac{2\|y\|^2}{n+1}\quad(n\varphi_0^2\ge1).$$
Since $\|y\|^2\le2nM+2\|\varepsilon\|^2$ and $\|\varepsilon\|^2/n\to\sigma_\star^2$ in probability, $R_n=O_{\mathbb P}(1)$.

Restrict the integral in (3.2) to $v=\sigma_\star^2u$ with $u\in[1,1+n^{-1/2}]$ and write $E'=\|\varepsilon\|^2/\sigma_\star^2\sim\chi^2_n$. On this range, using $-\frac n2\log u\ge-\frac n2(u-1)$ and $\frac{E'}{2}(1-\frac1u)=\frac{E'(u-1)}{2u}$,
$$-\frac n2\log u+\frac{\|\varepsilon\|^2}{2\sigma_\star^2}-\frac{Q_{S_0}}{2\sigma_\star^2u}\ \ge\ \frac{u-1}{2}\Big(\frac{E'}{u}-n\Big)-\frac{R_n}{2\sigma_\star^2u}\ \ge\ -\frac{u-1}{2}\Big(|E'-n|+\frac{E'}{\sqrt n}\Big)-\frac{R_n}{2\sigma_\star^2},$$
because $\frac{E'}{u}-n\ge E'(1-(u-1))-n\ge-(|E'-n|+E'n^{-1/2})$ for $u-1\le n^{-1/2}$. With $u-1\le n^{-1/2}$ the right-hand side is at least $-\Omega_n$, where
$$\Omega_n:=\frac{|E'-n|}{2\sqrt n}+\frac{E'}{2n}+\frac{R_n}{2\sigma_\star^2}=O_{\mathbb P}(1)$$
(since $(E'-n)/\sqrt n$ has mean $0$ and variance $2$, and $E'/n\to1$ in probability). Finally $\int_{\sigma_\star^2}^{\sigma_\star^2(1+n^{-1/2})}p_{\mathrm{IG}}(v)\,dv\ge c_{\mathrm{IG}}\,\sigma_\star^2n^{-1/2}$ with $c_{\mathrm{IG}}:=\min_{v\in[\sigma_\star^2,2\sigma_\star^2]}p_{\mathrm{IG}}(v)>0$. Therefore
$$\frac{p(S_0)m(S_0)}{f_0(y)}\ \ge\ \frac{1}{2(2p)^{s_0}}\,(n+1)^{-s_0/2}\,c_{\mathrm{IG}}\sigma_\star^2\,n^{-1/2}\,e^{-\Omega_n}. \tag{3.3}$$

*Conclusion.* Insert the numerator bound and (3.3) into (3.1):
$$\Pi(|S|>m\mid y)\le2^{1-m}\Theta_n^{(1)}\cdot2(2p)^{s_0}(n+1)^{s_0/2}\frac{\sqrt n\,e^{\Omega_n}}{c_{\mathrm{IG}}\sigma_\star^2}=2^{-m}(2p)^{s_0}(n+1)^{s_0/2}\sqrt n\;\Theta_n^{(m)},\qquad\Theta_n^{(m)}:=\frac{4\,e^{\Omega_n}\Theta_n^{(1)}}{c_{\mathrm{IG}}\sigma_\star^2},$$
and $\Theta_n^{(m)}$ is tight uniformly in $m$ as a product of two tight sequences ($\mathbb P_0(AB>K^2)\le\mathbb P_0(A>K)+\mathbb P_0(B>K)$; $\Omega_n$ does not depend on $m$, and the bound on $\Theta_n^{(1)}$ is uniform in $m$). For $m=m_n$, the definition of $m_n$ gives $m_n\log2\ge s_0\log(2p)+\frac{s_0+1}2\log n+\omega_n$, i.e. $2^{-m_n}\le(2p)^{-s_0}n^{-(s_0+1)/2}e^{-\omega_n}$, and $(n+1)^{s_0/2}n^{-s_0/2}=(1+1/n)^{s_0/2}$. $\square$

**Remark 3.2.** The tightness of $\Theta_n$ comes from Markov's inequality on the numerator, so Lemma 3.1 gives an in-probability rate and nothing stronger; this is the source of the "in probability only" qualification in the rate statements of T7 and T8.

---

## 4. Supersets: proof of Theorem 7.1

For $j\ge1$ define the size-$j$ superset sum
$$\Xi_j:=\sum_{J\subseteq[p]\setminus S_0,\ |J|=j}\frac{w(s_0+j)}{w(s_0)}\cdot\frac{m(S_0\cup J)}{m(S_0)} ,$$
with $\Xi_j=0$ if $s_0+j>p$. Since $Z\ge p(S_0)m(S_0)$ and $p(S)\le w(|S|)/W$ for every $S$,
$$\Pi(\{S\supsetneq S_0,\ |S|\le m_n\}\mid y)\ \le\ \sum_{j=1}^{m_n-s_0}\Xi_j . \tag{4.1}$$

### 4.1 One superset, exactly

**Lemma 4.1.** Assume (A1)–(A4) and (SE), and let $n\ge n_0$. On $\mathcal G_n$, for every $J\subseteq[p]\setminus S_0$ with $1\le|J|=j\le m_n$ and $S=S_0\cup J$,
$$\frac{m(S)}{m(S_0)}\ \le\ (n+1)^{-j/2}\Big(1+\frac1{n\varphi_0^2}\Big)^{j/2}\exp\Big\{\frac{\theta_n}{2}\chi^2_J+\rho_n\Big\},\qquad \theta_n:=\frac{1+2a_0/n}{1-\delta_n},$$
with $\delta_n$ and $\rho_n$ from Lemma 2.3. Moreover $\theta_n-1\le2(\delta_n+2a_0/n)$ and
$$\epsilon_n:=\frac{(\theta_n-1)\,C_A\log n}{2}\ \longrightarrow\ 0 .$$

*Proof.* By the definition of $m$,
$$\frac{m(S)}{m(S_0)}=\Big(\frac{D_{S_0}}{D_S}\Big)^{1/2}\Big(\frac{2b_0+Q_{S_0}}{2b_0+Q_S}\Big)^{\nu}=\Big(\frac{D_{S_0}}{D_S}\Big)^{1/2}\Big(1+\frac{t_S-t_{S_0}}{2b_0+Q_S}\Big)^{\nu}. \tag{4.2}$$
This is the exact integrated-variance Bayes factor; nothing is approximated. The three ingredients:

*Determinant.* $|S|=s_0+j\le m_n+s_0$, so (SE) gives $\lambda_{\min}(G_S)\ge n\varphi_0^2$ and Lemma 1.2(b) yields $(D_{S_0}/D_S)^{1/2}\le(n+1)^{-j/2}(1+1/(n\varphi_0^2))^{j/2}$.

*Numerator of the variance ratio.* By Lemma 1.1(d), $t_S-t_{S_0}\ge0$, and by Corollary 1.1′ (with $S_0\subseteq S$, condition (SE) on $S$) and $u=y$,
$$t_S-t_{S_0}=y^\top(M_S-M_{S_0})y\le\frac n{n+1}\Big[\|(P_S-P_{S_0})y\|^2+\eta_n\|P_{S_0}y\|^2\Big]\le\frac n{n+1}\Big[\sigma_\star^2\chi^2_J+\eta_n\|y\|^2\Big],$$
because $(P_S-P_{S_0})\mu=0$ ($\mu$ lies in the column span of $X_{S_0}$, which is contained in that of $X_S$), so $(P_S-P_{S_0})y=(P_S-P_{S_0})\varepsilon$.

*Denominator of the variance ratio.* By Lemma 2.3(b), $2b_0+Q_S\ge n\sigma_\star^2(1-\delta_n)$ on $\mathcal G_n$.

Now $\log(1+x)\le x$ for $x\ge0$ gives
$$\Big(1+\frac{t_S-t_{S_0}}{2b_0+Q_S}\Big)^{\nu}\le\exp\Big\{\nu\frac{t_S-t_{S_0}}{2b_0+Q_S}\Big\}\le\exp\Big\{\frac{\nu\frac n{n+1}\sigma_\star^2}{n\sigma_\star^2(1-\delta_n)}\chi^2_J+\nu\frac n{n+1}\frac{\eta_n\|y\|^2}{2b_0+Q_S}\Big\}\le\exp\Big\{\frac{\theta_n}2\chi^2_J+\rho_n\Big\},$$
since $\nu\frac n{n+1}\le\nu=\frac n2(1+2a_0/n)$ and Lemma 2.3(d) bounds the second term by $\rho_n$. Finally $\theta_n-1=\frac{2a_0/n+\delta_n}{1-\delta_n}\le2(\delta_n+2a_0/n)$ because $\delta_n\le\frac12$, and $\epsilon_n\le(\delta_n+2a_0/n)C_A\log n\to0$ by Lemma 2.3(b). $\square$

### 4.2 Summing over supersets of each size

**Proposition 4.2.** Assume (A1)–(A4) and (SE). Define the nonnegative random variable
$$U_n:=\sum_{j=1}^{m_n}\ \sum_{J\subseteq[p]\setminus S_0,\ |J|=j}\frac{w(s_0+j)}{w(s_0)}\,(n+1)^{-j/2}\Big(1+\frac1{n\varphi_0^2}\Big)^{j/2}e^{j\epsilon_n}\,e^{\chi^2_J/2}\,\mathbf 1\{\chi^2_J\le\tau_j\}$$
(a sum over sets $J$ with $s_0+j\le p$). Then:

(a) on $\mathcal G_n$, for $n\ge n_0$: $\ \sum_{j=1}^{m_n}\Xi_j\le e^{\rho_n}\,U_n$;

(b) for $n\ge n_0$: $\ \mathbb E_0U_n\le2K_{s_0}\,r_n$, where
$$r_n:=\Big[\frac{e\,C_A\log n}{4(n+1)}\Big(1+\frac1{n\varphi_0^2}\Big)e^{2\epsilon_n}\Big]^{1/2}\le\sqrt{\frac{eC_A\log n}{n}},\qquad K_{s_0}:=\sum_{j\ge1}(j+1)^{s_0}2^{-(j-1)}<\infty ;$$

(c) consequently $\sum_{j=1}^{m_n}\Xi_j\,\mathbf 1_{\mathcal G_n}=O_{\mathbb P}(\sqrt{\log n/n})$, and in particular $\sum_{j=1}^{m_n}\Xi_j\to0$ in $\mathbb P_0$-probability.

The tail sums are also controlled: for every fixed integer $j_1\ge0$,
$$\mathbb E_0\,U_n^{>j_1}\le2K_{s_0,j_1}\,r_n^{j_1+1},\qquad K_{s_0,j_1}:=\sum_{i\ge0}(j_1+2+i)^{s_0}2^{-i}, \tag{4.3}$$
where $U_n^{>j_1}$ is the part of $U_n$ with $j>j_1$, and on $\mathcal G_n$ one has $\sum_{j=j_1+1}^{m_n}\Xi_j\le e^{\rho_n}U_n^{>j_1}$.

*Proof.* (a) On $\mathcal G_n$, Lemma 4.1 bounds each term of $\Xi_j$. By (G3), $\chi^2_J\le\tau_j$ for every $J$ in the sum, so $\mathbf 1\{\chi^2_J\le\tau_j\}=1$ there, and, since $\theta_n\ge1$ (as $1+2a_0/n\ge1\ge1-\delta_n$), $\exp\{\theta_n\chi^2_J/2\}=\exp\{\chi^2_J/2\}\exp\{(\theta_n-1)\chi^2_J/2\}\le\exp\{\chi^2_J/2\}e^{(\theta_n-1)\tau_j/2}=e^{\chi^2_J/2}e^{j\epsilon_n}$, by the definition of $\epsilon_n$ and $\tau_j=C_Aj\log n$. Inserting this in Lemma 4.1 and summing gives (a); the same argument restricted to $j>j_1$ gives the last claim.

(b) The weights $w$, $(n+1)^{-j/2}$, $(1+1/(n\varphi_0^2))^{j/2}$, $e^{j\epsilon_n}$ and $\tau_j$ are deterministic, and for each $J$ with $|J|=j$ the variable $\chi^2_J$ is exactly chi-square with $j$ degrees of freedom. By Lemma 1.5(b),
$$\mathbb E_0\big[e^{\chi^2_J/2}\mathbf 1\{\chi^2_J\le\tau_j\}\big]\le\Big(\frac{e\tau_j}{j}\Big)^{j/2}=\big(eC_A\log n\big)^{j/2}.$$
Hence, using Lemma 1.3(b) for the sum of the prior ratios over $J$,
$$\mathbb E_0U_n\le\sum_{j=1}^{m_n}2\binom{s_0+j}{j}2^{-j}(n+1)^{-j/2}\Big(1+\frac1{n\varphi_0^2}\Big)^{j/2}e^{j\epsilon_n}\big(eC_A\log n\big)^{j/2}=\sum_{j=1}^{m_n}2\binom{s_0+j}{j}\,r_n^{\,j}.$$
For $n\ge n_0$ we have $r_n\le\frac12$ (as $\epsilon_n\to0$ and $\log n/n\to0$), and $\binom{s_0+j}{j}\le(j+1)^{s_0}$, so
$$\mathbb E_0U_n\le2r_n\sum_{j\ge1}(j+1)^{s_0}r_n^{\,j-1}\le2r_n\sum_{j\ge1}(j+1)^{s_0}2^{-(j-1)}=2K_{s_0}r_n .$$
The bound $r_n\le\sqrt{eC_A\log n/n}$ holds once $(1+1/(n\varphi_0^2))e^{2\epsilon_n}\le4(n+1)/n$. The tail bound (4.3) is the same computation: $\sum_{j>j_1}(j+1)^{s_0}r^j=r^{j_1+1}\sum_{i\ge0}(j_1+2+i)^{s_0}r^i\le K_{s_0,j_1}r^{j_1+1}$ for $r\le\frac12$.

(c) By (a) and (b), for every $K>0$ and $n\ge n_0$,
$$\mathbb P_0\Big(\sum_{j\le m_n}\Xi_j\,\mathbf 1_{\mathcal G_n}>K\,e^{\rho_n}2K_{s_0}r_n\Big)\le\mathbb P_0(U_n>K\,\mathbb E_0U_n)\le\frac1K$$
by Markov's inequality, and $e^{\rho_n}2K_{s_0}r_n\le K'\sqrt{\log n/n}$. The statement without the indicator follows because $\mathbb P_0(\mathcal G_n^c)\le5/n\to0$ (Lemma 2.2). $\square$

**Remark 4.3 (why no union bound is needed, and where the truncation enters).** The sum over the $\binom{p-s_0}{j}$ sets $J$ of size $j$ is taken in expectation, where each term contributes the same truncated moment $(eC_A\log n)^{j/2}$; the prior ratio summed over those sets is at most $2(j+1)^{s_0}2^{-j}$ regardless of $p$ (Lemma 1.3(b)). The only union bound is the one defining $\mathcal G_n$, which holds with probability $1-O(1/n)$ and whose role is to make the truncation indicators equal to one on the event on which the posterior is bounded. Without the truncation the expectation of $e^{\chi^2_J/2}$ is infinite; the exact Bayes factor (4.2) has finite expectation, but it is bounded above on $\mathcal G_n$ by $e^{\theta_n\chi^2_J/2}$ with $\theta_n>1$, which does not, so the bound is applied only on $\mathcal G_n$. The price is that the rate holds in probability, with exceptional probability $O(1/n)$.

### 4.3 Proof of Theorem 7.1

(a) By (4.1), on $\mathcal G_n$ the posterior mass of the supersets of size at most $m_n$ is at most $\sum_{j\le m_n}\Xi_j$, which is $O_{\mathbb P}(\sqrt{\log n/n})$ by Proposition 4.2(c); off $\mathcal G_n$ the mass is at most $1$, and $\mathbb P_0(\mathcal G_n^c)\le5/n$ by Lemma 2.2. Hence for every $K>0$,
$$\mathbb P_0\Big(\Pi(\{S\supsetneq S_0,|S|\le m_n\}\mid y)>K'K\sqrt{\log n/n}\Big)\le\frac1K+\frac5n ,$$
which is (a).

(b) $\Pi(\{S\supsetneq S_0\}\mid y)\le\Pi(\{S\supsetneq S_0,|S|\le m_n\}\mid y)+\Pi(|S|>m_n\mid y)$. The first term is $o_{\mathbb P}(1)$ by (a); the second is $o_{\mathbb P}(1)$ by **Theorem T6** (assumed; this is its only use in the proof of T7).

(c) In the same decomposition bound the second term by Lemma 3.1: $\Pi(|S|>m_n\mid y)=O_{\mathbb P}(e^{-\omega_n})$. With (a) this gives $O_{\mathbb P}(\sqrt{\log n/n}+e^{-\omega_n})$. If $\omega_n\ge\frac12\log n$ then $e^{-\omega_n}\le n^{-1/2}\le\sqrt{\log n/n}$, and $\omega_n=\frac12\log n$ is $O(\log n)$, so $m_n=O(\log n)$ and (SE) is still a condition on models of size $O(\log n)$. $\square$

**Remark 4.4 (on the order of the bound; heuristic, not proved).** The expected truncated contribution of the supersets of size $j$ is of order $(j+1)^{s_0}(C\log n/n)^{j/2}$, so the sum is dominated by $j=1$, and the large $j$ (up to $m_n$) cost only a geometric tail. For $j=1$, *for orthogonal designs* (more generally, when the singleton noise scores are close to independent; audit 2026-10-15), the order $\sqrt{\log n/n}$ appears to be the true order of the size-$(s_0+1)$ posterior mass when $p$ grows polynomially: a single noise variable $k$ enters with Bayes factor $\asymp n^{-1/2}e^{\chi^2_{\{k\}}/2}$ and prior ratio $\asymp(s_0+1)/(2p)$, and the sum over the $p-s_0$ values of $k$ of $e^{\chi^2_{\{k\}}/2}$ restricted to $\chi^2_{\{k\}}\le2\log p$ has expectation $\asymp p\sqrt{\log p}$. The order is design dependent, and (SE) with polynomial $p$ does not imply it *(audit 2026-10-15, example from the Sol audit)*: with $S_0=\emptyset$, $p=\lfloor n/2\rfloor$ and equicorrelated columns $x_j=\sqrt n(\sqrt r\,u_0+\sqrt{1-r}\,u_j)$ ($u_0,\dots,u_p$ orthonormal, $0<r<1$; every Gram submatrix of $X/\sqrt n$ has $\lambda_{\min}\ge1-r$, so (SE) holds), the singleton scores are $W_j=\sqrt r\,Z_0+\sqrt{1-r}\,Z_j$ with independent standard normals $Z_i$, $\frac1p\sum_je^{W_j^2/2}\to r^{-1/2}e^{Z_0^2/2}$ conditionally on $Z_0$, and the singleton mass is $O_{\mathbb P}(n^{-1/2})=o_{\mathbb P}(\sqrt{\log n/n})$. A matching lower bound on the posterior mass, under suitable design assumptions, is not proved here (it would need a lower bound on the singleton numerator together with an *upper* bound on $Z$, or control of $Z/[p(S_0)m(S_0)]$, and a concentration statement for a sum of variables with a tail of index one; audit 2026-10-15: the earlier text said "a lower bound on $Z$", which is the wrong direction), and the paper does not need it.

---

## 5. Underfitting models: proofs of Theorems 8.1 and 8.2

Throughout this section $S$ is an underfitting model with $|S|\le m_n$: $J=J(S)=S_0\setminus S\ne\emptyset$, $J'=J'(S)=S\setminus S_0$, $S'=S\cup S_0$, $|S'|=|S|+|J|\le m_n+s_0$, so (SE) applies to $S$ and $S'$. Recall $V_S=\|(P_{S'}-P_S)y\|^2$, $\Delta_S=\|(I-P_S)\mu\|^2$, $N_S=\|(P_{S'}-P_S)\varepsilon\|^2$, and $E_n$, $\delta_n''$, $\rho_n$ from Lemma 2.3.

### 5.1 One underfitting model against its union with $S_0$

**Lemma 5.1.** Assume (A1)–(A4) and (SE), and let $n\ge n_0$. On $\mathcal G_n$, for every underfitting $S$ with $|S|\le m_n$,
$$\frac{w(|S|)\,m(S)}{w(|S'|)\,m(S')}\ \le\ (2p)^{|J|}(n+1)^{|J|/2}\exp\Big\{-\nu\frac n{n+1}\frac{V_S}{E_n+V_S}+\rho_n\Big\}\ \le\ (2p)^{|J|}(n+1)^{|J|/2}\exp\Big\{-\min\Big(\frac{V_S}{8\sigma_\star^2},\frac n5\Big)+\rho_n\Big\}. \tag{5.1}$$
In particular, dropping the signal term, $\dfrac{w(|S|)m(S)}{w(|S'|)m(S')}\le(2p)^{s_0}(n+1)^{s_0/2}e^{\rho_n}$.

*Proof.* *Prior.* $|S'|=|S|+|J|\le p$, so Lemma 1.3(a) gives $w(|S|)/w(|S'|)\le(2p)^{|J|}$.

*Determinant.* $S\subseteq S'$ with $|S'|-|S|=|J|$, so Lemma 1.2(a) gives $(D_{S'}/D_S)^{1/2}\le(n+1)^{|J|/2}$.

*Variance.* Exactly,
$$\frac{m(S)}{m(S')}=\Big(\frac{D_{S'}}{D_S}\Big)^{1/2}\Big(\frac{2b_0+Q_{S'}}{2b_0+Q_S}\Big)^{\nu},\qquad \frac{2b_0+Q_{S'}}{2b_0+Q_S}=1-\frac{t_{S'}-t_S}{2b_0+Q_S}.$$
By Lemma 1.1(d), $t_{S'}-t_S\ge0$, and the ratio is positive, so $x:=(t_{S'}-t_S)/(2b_0+Q_S)\in[0,1)$ and $\log(1-x)\le-x$ gives $\big(\tfrac{2b_0+Q_{S'}}{2b_0+Q_S}\big)^\nu\le\exp\{-\nu x\}$. For $x$: the lower bound of Corollary 1.1′ (with $S\subseteq S'$, (SE) on $S'$, $u=y$) and $\|P_{S'}y\|^2\le\|y\|^2$ give $t_{S'}-t_S\ge\frac n{n+1}\big[V_S-\eta_n\|y\|^2\big]$, while Lemma 2.3(c) gives $2b_0+Q_S\le E_n+V_S$. Hence
$$\nu x\ \ge\ \nu\frac n{n+1}\,\frac{V_S-\eta_n\|y\|^2}{E_n+V_S}\ \ge\ \nu\frac n{n+1}\frac{V_S}{E_n+V_S}-\nu\frac n{n+1}\frac{\eta_n\|y\|^2}{E_n}\ \ge\ \nu\frac n{n+1}\frac{V_S}{E_n+V_S}-\rho_n ,$$
by Lemma 2.3(d) with $B=E_n$. This is the first inequality of (5.1). Two sign remarks. The first "$\ge$" replaces the denominator $2b_0+Q_S$ by the larger $E_n+V_S$: if $V_S-\eta_n\|y\|^2\ge0$ this decreases the quotient; if $V_S-\eta_n\|y\|^2<0$ the right-hand side is negative while $x\ge0$, so the inequality holds in either case. The second "$\ge$", $\frac{V-\eta\|y\|^2}{E+V}\ge\frac{V}{E+V}-\frac{\eta\|y\|^2}{E}$, holds whatever the sign of $V-\eta\|y\|^2$, since $E+V\ge E>0$.

For the second inequality, $\frac{V}{E_n+V}\ge\min\big(\frac{V}{2E_n},\frac12\big)$ (if $V\le E_n$ the first, otherwise the second), $\nu\frac n{n+1}\ge\frac n2\cdot\frac n{n+1}\ge\frac{n-1}2$, and $E_n\le n\sigma_\star^2(1+\delta_n'')$ by Lemma 2.3(c). Thus
$$\nu\frac n{n+1}\frac{V_S}{2E_n}\ge\frac{(n-1)V_S}{4n\sigma_\star^2(1+\delta_n'')}\ge\frac{V_S}{4\sigma_\star^2}\Big(1-\frac1n\Big)(1-\delta_n'')\ge\frac{V_S}{8\sigma_\star^2},\qquad \nu\frac n{n+1}\cdot\frac12\ge\frac{n-1}4\ge\frac n5,$$
for $n\ge n_0$ (so that $(1-1/n)(1-\delta_n'')\ge\frac12$ and $n\ge5$). The final claim uses $V_S\ge0$ and $|J|\le s_0$. $\square$

### 5.2 Adding the signal

**Lemma 5.2.** Assume (A1)–(A4) and (SE), and let $n\ge n_0$. On $\mathcal G_n$, for every underfitting $S$ with $|S|\le m_n$, $|J'(S)|\le j_0$, and
$$\Delta_S\ \ge\ L\,\sigma_\star^2\log n\qquad\text{for some }L\ge4C_2,$$
one has
$$\frac{w(|S|)\,m(S)}{w(|S'|)\,m(S')}\ \le\ \exp\Big\{s_0(A+1)\log n+\rho_n-\min\Big(\frac{L\log n}{32},\frac n5\Big)\Big\}. \tag{5.2}$$
Moreover, by Lemma 1.4, $\Delta_S\ge n\varphi_0^2\|\beta^\star_{J(S)}\|^2$, so the hypothesis on $\Delta_S$ holds as soon as $n\varphi_0^2\|\beta^\star_{J(S)}\|^2\ge L\sigma_\star^2\log n$.

*Proof.* Since $P_{S'}\mu=\mu$ ($S'\supseteq S_0$), $(P_{S'}-P_S)\mu=(I-P_S)\mu$, so $(P_{S'}-P_S)y=(I-P_S)\mu+(P_{S'}-P_S)\varepsilon$ and the triangle inequality gives
$$\sqrt{V_S}\ \ge\ \sqrt{\Delta_S}-\sqrt{N_S}. \tag{5.3}$$
There is no Gaussian cross term to control: (5.3) is a norm inequality. By (G4) and the hypothesis on $\Delta_S$, $N_S\le\sigma_\star^2C_2\log n\le\frac{C_2}{L}\Delta_S\le\frac14\Delta_S$, so $\sqrt{V_S}\ge\frac12\sqrt{\Delta_S}$ and $V_S\ge\frac14\Delta_S\ge\frac14L\sigma_\star^2\log n$. Then $\frac{V_S}{8\sigma_\star^2}\ge\frac{L\log n}{32}$, and (5.1) gives the exponential factor in (5.2). For the prefactor, $|J|\le s_0$ and, for $n\ge5$, $\log2+\frac12\log(n+1)\le\log n$, so $(2p)^{|J|}(n+1)^{|J|/2}\le\exp\{s_0(\log2+A\log n+\frac12\log(n+1))\}\le\exp\{s_0(A+1)\log n\}$. $\square$

### 5.3 Assembling the underfitting mass

The next lemma is the step that avoids the union bound over $p^{m_n}$ models. Underfitting models are grouped by their union $S'$ with $S_0$; each $S'$ collects at most $2^{s_0}-1$ of them; the sum over $S'$ is the superset sum of Section 4, which is already controlled; and for $|J'|>j_0$ the superset sum alone is small enough that no signal is needed.

**Lemma 5.3.** Assume (A1)–(A4) and (SE), let $n\ge n_0$, and let $\mathcal U$ be any collection of underfitting models with $|S|\le m_n$. Put
$$\kappa_n(\mathcal U):=\max\Big\{\frac{w(|S|)m(S)}{w(|S'|)m(S')}:\ S\in\mathcal U,\ |J'(S)|\le j_0\Big\}\quad(\max\emptyset:=0).$$
Then on $\mathcal G_n$,
$$\sum_{S\in\mathcal U}\frac{w(|S|)\,m(S)}{w(s_0)\,m(S_0)}\ \le\ 2^{s_0}\kappa_n(\mathcal U)\big(1+e^{\rho_n}U_n\big)+2^{s_0}(2p)^{s_0}(n+1)^{s_0/2}e^{2\rho_n}\,U_n^{>j_0}, \tag{5.4}$$
with $U_n$ and $U_n^{>j_0}$ as in Proposition 4.2. Moreover
$$(2p)^{s_0}(n+1)^{s_0/2}\,U_n^{>j_0}=O_{\mathbb P}\Big(\frac{(\log n)^{(j_0+1)/2}}{n}\Big)=o_{\mathbb P}\big(\sqrt{\log n/n}\big). \tag{5.5}$$

*Proof.* For $S\in\mathcal U$ factor
$$\frac{w(|S|)m(S)}{w(s_0)m(S_0)}=\frac{w(|S|)m(S)}{w(|S'|)m(S')}\cdot\frac{w(|S'|)m(S')}{w(s_0)m(S_0)} .$$
Each $S'=S_0\cup J'$ arises from at most $2^{s_0}-1$ underfitting $S$, namely $S=J'\cup(S_0\setminus I)$ with $\emptyset\ne I\subseteq S_0$. Split $\mathcal U$ according to $|J'(S)|\le j_0$ or $>j_0$; note $|J'(S)|\le|S|\le m_n$ always.

For $|J'|\le j_0$, bound the first factor by $\kappa_n(\mathcal U)$ and sum the second factor over the distinct $S'$: the term $S'=S_0$ (if $J'=\emptyset$) contributes $1$, and the others are among the terms of $\sum_{j=1}^{m_n}\Xi_j$, which is at most $e^{\rho_n}U_n$ on $\mathcal G_n$ by Proposition 4.2(a).

For $|J'|>j_0$, bound the first factor by $(2p)^{s_0}(n+1)^{s_0/2}e^{\rho_n}$ (Lemma 5.1, last claim) and the sum of the second factor over the distinct $S'$ by $\sum_{j=j_0+1}^{m_n}\Xi_j\le e^{\rho_n}U_n^{>j_0}$ (Proposition 4.2, last claim). This proves (5.4).

For (5.5), by (4.3) with $j_1=j_0$ and $r_n\le\sqrt{eC_A\log n/n}$,
$$\mathbb E_0\big[(2p)^{s_0}(n+1)^{s_0/2}U_n^{>j_0}\big]\le2K_{s_0,j_0}\,2^{s_0}n^{s_0A}(n+1)^{s_0/2}\Big(\frac{eC_A\log n}{n}\Big)^{(j_0+1)/2}.$$
By the choice $j_0=\lceil(2A+1)s_0\rceil+1$ we have $\frac{j_0+1}2\ge s_0(A+\frac12)+1$, so $n^{s_0A}(n+1)^{s_0/2}n^{-(j_0+1)/2}\le(1+1/n)^{s_0/2}n^{-1}\le2/n$, and the expectation is at most $K'''(\log n)^{(j_0+1)/2}/n$. Markov's inequality gives (5.5); the last equality holds because $(\log n)^{(j_0+1)/2}/n=\sqrt{\log n/n}\cdot(\log n)^{j_0/2}/\sqrt n\to0$ faster. $\square$

### 5.4 Proof of Theorem 8.1

Let $\mathcal U$ be the collection of all underfitting models with $|S|\le m_n$. Every model other than $S_0$ is either of size $>m_n$, or a superset of size $\le m_n$, or in $\mathcal U$:
$$1-\Pi(S_0\mid y)\le\Pi(|S|>m_n\mid y)+\Pi(\{S\supsetneq S_0,|S|\le m_n\}\mid y)+\Pi(\mathcal U\mid y), \tag{5.6}$$
with equality as soon as $m_n\ge s_0$, which holds for $n\ge n_0$.

*The underfitting term.* Since $Z\ge p(S_0)m(S_0)=w(s_0)m(S_0)/W$ and $p(S)\le w(|S|)/W$,
$$\Pi(\mathcal U\mid y)\le\sum_{S\in\mathcal U}\frac{w(|S|)m(S)}{w(s_0)m(S_0)} .$$
Under (BM), for every $S\in\mathcal U$, Lemma 1.4 gives $\Delta_S\ge n\varphi_0^2\|\beta^\star_{J(S)}\|^2\ge n\varphi_0^2\min_{j\in S_0}(\beta_j^\star)^2\ge M_n^\beta\sigma_\star^2\log n$, because $J(S)\ne\emptyset$. Let $n_1\ge n_0$ be such that for $n\ge n_1$: $M_n^\beta\ge4C_2$, $M_n^\beta/32\ge s_0(A+1)+2$ and $n/5\ge(s_0(A+1)+2)\log n$ (possible since $M_n^\beta\to\infty$). Then Lemma 5.2 with $L=M_n^\beta$ gives, on $\mathcal G_n$ and for $n\ge n_1$,
$$\kappa_n(\mathcal U)\le\exp\{s_0(A+1)\log n+\rho_n-(s_0(A+1)+2)\log n\}=e^{\rho_n}n^{-2}.$$
By Lemma 5.3, on $\mathcal G_n$,
$$\Pi(\mathcal U\mid y)\le2^{s_0}e^{\rho_n}n^{-2}\big(1+e^{\rho_n}U_n\big)+2^{s_0}e^{2\rho_n}(2p)^{s_0}(n+1)^{s_0/2}U_n^{>j_0}=O_{\mathbb P}(n^{-2})+O_{\mathbb P}\Big(\frac{(\log n)^{(j_0+1)/2}}{n}\Big), \tag{5.7}$$
using $U_n=O_{\mathbb P}(\sqrt{\log n/n})$ (Proposition 4.2(b) and Markov) and (5.5). Since $\mathbb P_0(\mathcal G_n^c)\le5/n\to0$, (5.7) holds without the restriction to $\mathcal G_n$ as an $O_{\mathbb P}$ statement.

*Part (i).* In (5.6): the first term is $o_{\mathbb P}(1)$ by **Theorem T6** (assumed), the second by Theorem 7.1(a), the third by (5.7). Hence $1-\Pi(S_0\mid y)\to0$ in probability. Since $0\le1-\Pi(S_0\mid y)\le1$, bounded convergence gives $\mathbb E_0[1-\Pi(S_0\mid y)]\to0$, i.e. convergence in $L^1(\mathbb P_0)$.

*Part (ii).* If $\Pi(S_0\mid y)>\frac12$ then every other model has posterior probability $<\frac12<\Pi(S_0\mid y)$, so $S_0$ is the unique maximiser of $p(S)m(S)$ and $\mathrm{HPM}=S_0$ whatever the tie-breaking order. Hence $\{\mathrm{HPM}\ne S_0\}\subseteq\{1-\Pi(S_0\mid y)\ge\frac12\}$, and Markov's inequality gives $\mathbb P_0(\mathrm{HPM}\ne S_0)\le2\,\mathbb E_0[1-\Pi(S_0\mid y)]$, which tends to $0$ by (i). This part uses nothing about the model beyond (i).

*Part (iii).* In (5.6) bound the first term by Lemma 3.1, $O_{\mathbb P}(e^{-\omega_n})$; the second by Theorem 7.1(a), $O_{\mathbb P}(\sqrt{\log n/n})$; the third by (5.7), $o_{\mathbb P}(\sqrt{\log n/n})$. Hence $1-\Pi(S_0\mid y)=O_{\mathbb P}(\sqrt{\log n/n}+e^{-\omega_n})$, and $O_{\mathbb P}(\sqrt{\log n/n})$ when $\omega_n\ge\frac12\log n$. $\square$

### 5.5 Proof of Theorem 8.2 (T10)

If $J_n=\emptyset$ there is nothing to prove. Otherwise, for $j\in J_n$ let $\mathcal U_j$ be the collection of models $S$ with $|S|\le m_n$ and $j\notin S$. Every $S\in\mathcal U_j$ is underfitting, since $j\in S_0\setminus S=J(S)$, and Lemma 1.4 gives
$$\Delta_S\ge n\varphi_0^2\|\beta^\star_{J(S)}\|^2\ge n\varphi_0^2(\beta_j^\star)^2\ge M_n^\beta(\sigma_\star^2+M)\log n\ge M_n^\beta\sigma_\star^2\log n .$$
This uses the beta-min condition for the single coordinate $j$ and nothing about the other coordinates of $\beta^\star$, which may be zero or arbitrarily small: they are fitted by $S'=S\cup S_0$, so they never appear in the comparison of $S$ with $S'$. Exactly as in the proof of Theorem 8.1(i), with $n_1$ chosen from the sequence $M_n^\beta$, Lemma 5.2 gives $\kappa_n(\mathcal U_j)\le e^{\rho_n}n^{-2}$ on $\mathcal G_n$ for $n\ge n_1$, and Lemma 5.3 gives, on $\mathcal G_n$,
$$\Pi(\mathcal U_j\mid y)\le\sum_{S\in\mathcal U_j}\frac{w(|S|)m(S)}{w(s_0)m(S_0)}\le2^{s_0}e^{\rho_n}n^{-2}\big(1+e^{\rho_n}U_n\big)+2^{s_0}e^{2\rho_n}(2p)^{s_0}(n+1)^{s_0/2}U_n^{>j_0},$$
a bound that does not depend on $j$. Since $\{S\not\supseteq J_n\}\subseteq\{|S|>m_n\}\cup\bigcup_{j\in J_n}\mathcal U_j$ and $|J_n|\le s_0$,
$$1-\Pi(\{S\supseteq J_n\}\mid y)\le\Pi(|S|>m_n\mid y)+s_0\max_{j\in J_n}\Pi(\mathcal U_j\mid y)=\Pi(|S|>m_n\mid y)+O_{\mathbb P}\Big(n^{-2}+\frac{(\log n)^{(j_0+1)/2}}n\Big).$$
The first term is $o_{\mathbb P}(1)$ by **Theorem T6** (assumed) and $O_{\mathbb P}(e^{-\omega_n})$ by Lemma 3.1, which gives both forms of the conclusion. For the "in particular" clause: for $j\in J_n$, $\mathrm{PIP}_j=\Pi(\{S\ni j\}\mid y)\ge\Pi(\{S\supseteq J_n\}\mid y)\to1$ in probability, and on the event $\{\Pi(\{S\supseteq J_n\}\mid y)>\frac12\}$, whose probability tends to $1$, every $j\in J_n$ has $\mathrm{PIP}_j>\frac12$ and so belongs to the median model. The last sentence of Theorem 8.2 holds because only $\Delta_S\ge M_n^\beta\sigma_\star^2\log n$ was used. $\square$

**Remark 8.3 (on the beta-min scale).** T8 and T10 are stated with the threshold $M_n^\beta(\sigma_\star^2+M)\log n/(n\varphi_0^2)$; the proofs use only $M_n^\beta\sigma_\star^2\log n/(n\varphi_0^2)$. The factor $\sigma_\star^2+M$ would arise from bounding the residual sum of squares of an underfitting model by $\|y\|^2\approx n(\sigma_\star^2+M)$. Comparing $S$ with $S'=S\cup S_0$ instead of with $S_0$ replaces that residual by $\|(I-P_{S'})\varepsilon\|^2+V_S$ (Lemma 2.3(c)), in which the unfitted signal appears only through $V_S$, and the penalty $\nu V_S/(E_n+V_S)$ is increasing in $V_S$. The unfitted signal therefore never works against the comparison. Since $M\ge0$, the stated conditions imply the ones used, so T8 and T10 hold as stated; the sharper scale is what the proof delivers.

**Remark 8.4 (what the choice of $j_0$ does).** For $|J'(S)|>j_0$ the superset sum $\sum_{j>j_0}\Xi_j=O_{\mathbb P}((\log n/n)^{(j_0+1)/2})$ beats the crude factor $(2p)^{s_0}(n+1)^{s_0/2}\le2^{s_0}(1+1/n)^{s_0/2}n^{s_0(A+1/2)}$ that one pays for removing the missing true variables without using the signal. This is where the condition $p\le n^A$ enters the underfitting step: it fixes $j_0=\lceil(2A+1)s_0\rceil+1$, which is finite, and for the finitely many sizes $|J'|\le j_0$ the uniform noise bound (G4) over $O(p^{j_0})$ models costs only $O(\log n)$, which $M_n^\beta\to\infty$ absorbs. A union bound over all $p^{m_n}$ models would instead cost $O(m_n\log p)=O(\log^2n)$ and would force $\beta_{\min}^2\gg\log^2n/n$.

---

## 6. Hypotheses added, use of T6, and steps to re-check

### 6.1 Hypotheses added or made precise

1. **$\omega_n=O(\log n)$, without loss of generality.** The proofs use $m_n\le C_m\log n$, through $\delta_n\log n\to0$ (Lemma 2.3(b)) and $r_n\to0$ (Proposition 4.2). As explained in §0.1, this is no restriction: (SE) for a larger $m_n$ implies (SE) for the $m_n$ built from $\omega_n'=\min(\omega_n,\frac12\log n)$, and the theorems applied with $\omega_n'$ give the conclusions for $\omega_n$.
2. **The rate needs the tail above $m_n$ to be small; this is the one genuine precision.** The term $\Pi(|S|>m_n\mid y)$ is $O_{\mathbb P}(e^{-\omega_n})$ (Lemma 3.1) and nothing better in general. The rate $O_{\mathbb P}(\sqrt{\log n/n})$ of T7 and of T8(iii) is proved under (SE$_{1/2}$), i.e. (SE) with $\omega_n\ge\frac12\log n$; the required size range is displayed in §0.1. For a general $\omega_n$ the rate is $O_{\mathbb P}(\sqrt{\log n/n}+e^{-\omega_n})$; with T6's example $\omega_n=\log\log n$ this is only $O_{\mathbb P}(\sqrt{\log n/n}+1/\log n)$, and the band of sizes between the two thresholds cannot be handled without (SE) there. The frozen draft's T7 did not say which $\omega_n$ defines its $m_n$; the current draft names it and states the two-term rate (audit 2026-10-15). The difference in $m_n$ is small in practice: $(\frac12\log n-\log\log n)/\log2$ sizes.
3. **The beta-min condition is weakened, not strengthened.** (BM) uses $\sigma_\star^2$ where the frozen T8 and T10 used $\sigma_\star^2+M$ (Remark 8.3). The frozen T8 and T10 follow, and so do the current ones, which use $\sigma_\star^2$ (audit 2026-10-15).
4. **$a_0,b_0>0$** (proper inverse-gamma prior): used in Lemma 3.1, where the marginal $m(S)$ must be a probability density and $p_{\mathrm{IG}}$ must be bounded below on $[\sigma_\star^2,2\sigma_\star^2]$; and in $\nu=a_0+n/2$. This is the draft's standing choice.
5. **Thresholds $n\ge n_0$; the bounds are asymptotic, not quantitative.** All bounds hold for $n$ beyond a threshold depending on $(s_0,A,\varphi_0,\sigma_\star^2,M,a_0,b_0,\sup_n\omega_n/\log n)$; the thresholds $n_1$ in Section 5 depend in addition on the sequence $M_n^\beta$. None of the constants is optimised, and they are far from sharp. *(audit 2026-10-15)* Since $m_n=O(\log n)$, the definition $\delta_n=3\sqrt{\log n/n}+C_A(m_n+s_0)\log n/n$ gives $\delta_n\sim3\sqrt{\log n/n}$ (the second term is $O(\log^2n/n)$; the first comes from the fluctuation of $\|\varepsilon\|^2/n$, i.e. of the residual variance), and then $\theta_n-1=(\delta_n+2a_0/n)/(1-\delta_n)\sim\delta_n$ and $\epsilon_n=(\theta_n-1)C_A\log n/2\sim\frac{3C_A}{2}(\log n)^{3/2}/\sqrt n$. (The previous wording, $\delta_n\asymp C_Am_n\log n/n$ and $\epsilon_n$ of order $C_A^2m_n\log^2n/n$, omitted the dominant term; the proof itself always uses the exact definitions and needs only $\delta_n\log n\to0$ and $\epsilon_n\to0$.) At moderate $n$ the second term of $\delta_n$ is nevertheless the larger one numerically, because $C_A\ge11$: with $s_0=2$, $A=1$, $p=n$, $\omega_n=\frac12\log n$, $a_0=0.01$ and $\varphi_0^2=1$, it dominates up to about $n=1.4\times10^6$, and $r_n\le\frac12$ holds for every $n\ge3.84\times10^5$ checked on a grid of step $1000$ up to $2\times10^6$, and fails at $n=3.83\times10^5$ (this agrees with reviewer C's "order $10^6$"; computation in `proofs/_audit/group_C/check_audit_C.py` and its `.out` file). The rates are correct as asymptotic statements; the explicit constants should not be quoted as finite-$n$ bounds.
6. **$s_0\ge1$ is not needed** ($s_0=0$ is allowed; then T8 reduces to T7 plus the tail).
7. Nothing is assumed about $p$ beyond $p\le n^A$: no lower bound on $p$ (Lemma 1.3(b) holds for every $p\ge s_0+j$), and the cap $k_{\max}\ge s_0$ is arbitrary (all comparisons are written with $w$, Section 0.1).
8. **Hypotheses not used.** The column standardisation $\|x_j\|^2=n$ is never invoked ((SE) at $|S|=1$ already gives $\|x_j\|^2\ge n\varphi_0^2$). The restriction $A\ge1$ is never used: every use of $A$ is through $\log p\le A\log n$, which works for any $A>0$. (A4) is implied by (SE) and is used on its own only in Lemma 3.1.

### 6.2 Where T6 is used

- Theorem 7.1(b) (convergence in T7): for $\Pi(|S|>m_n\mid y)=o_{\mathbb P}(1)$.
- Theorem 8.1(i)–(ii) (T8(i)–(ii)): the same term in (5.6).
- Theorem 8.2 (T10), convergence form: the same term.

T6 is used only as stated (a $o_{\mathbb P}(1)$ tail). The rate statements, Theorem 7.1(c), Theorem 8.1(iii) and the rate form of Theorem 8.2, use Lemma 3.1 instead, which is proved here from L6 and (A2)–(A4). Lemma 3.1 implies T6 for every $\omega_n\to\infty$ and every cap, so every citation of T6 above can be replaced by Lemma 3.1 and the supplement then depends on L6 alone; the citations are kept because the task statement allows T6 and the draft's dependency map lists T7 and T8 as using it.

Lemma L6 is used in: Lemma 1.3 (part (i)), Lemma 3.1 (parts (iii), (iv), (v)).

### 6.3 Steps the author is least sure of, and suggested checks

1. **Lemma 1.1(a)** (the identity $M_S=h(X_SX_S^\top)$ and the eigenvalue description). It is the push-through identity plus the functional calculus, and it is checked numerically in `check_T7_T8.py` together with the monotonicity (d) and the bounds (b)–(c). A reviewer should confirm that Corollary 1.1′ uses the right inequality on each side.
2. **Lemma 3.1, the lower bound on the inverse-gamma integral** (the Laplace-type step giving $n^{-1/2}$ rather than $n^{-1}$). The inequalities are elementary but the direction of each should be re-read: $-\frac n2\log u\ge-\frac n2(u-1)$ for $u\ge1$, and $E'/u\ge E'(1-(u-1))$ for $u\ge1$. The exponent $\frac{s_0+1}{2}\log n$ of T6 is recovered exactly, which is a consistency check.
3. **Proposition 4.2(a)**, the passage from $\theta_n>1$ to the truncated moment at $\theta=1$: $e^{\theta_n\chi^2/2}\le e^{\chi^2/2}e^{(\theta_n-1)\tau_j/2}$ on $\{\chi^2\le\tau_j\}$, and the indicator is $1$ on $\mathcal G_n$ by (G3). A reviewer should confirm that $U_n$ is defined with deterministic weights only, so that $\mathbb E_0U_n$ is computed termwise.
4. **Lemma 2.3(c)**: $\|(I-P_S)y\|^2=\|(I-P_{S'})\varepsilon\|^2+V_S$ needs $P_S\preceq P_{S'}$ (true, $S\subseteq S'$) and $(I-P_{S'})\mu=0$ (true, $S'\supseteq S_0$). This is the step that removes $M$ from the beta-min condition; if it were wrong, the theorems would still hold with the stated $\sigma_\star^2+M$ by bounding $Q_S\le\|y\|^2$ instead, at the cost of replacing $E_n$ by $2b_0+\|y\|^2$ throughout Section 5.
5. **The constants $C_A$, $C_2$, $j_0$** and the inequalities $2k+3x_k\le C_Ak\log n$, $2s_0+3x\le C_2\log n$ in Lemma 2.2. They are deliberately loose; only their finiteness matters, but a slip would change $n_0$, not the statements.
6. **Remark 4.4** is a heuristic about sharpness and is not part of the proof.
7. **The one external citation.** Lemma 1.5(a) is quoted as Lemma 1 of Laurent and Massart (2000); the statement is the standard one, but the reference and the exact form should be checked against the source before publication (CITED_RESULTS.md).

---

## Audit revisions (2026-10-15)

Sol audits `proofs/_audit/{T7,T8,T10}/SOL_AUDIT.md` (all VERIFIED); rulings in `proofs/_audit/group_C/RULINGS.md`. No step of any proof was changed; all edits are to explanatory text.

1. **Summary** (T8 finding 3). Added a note that "the draft"/"as stated" refer to the draft frozen on 14 October 2026 and that the current draft has incorporated the precisions (named $\omega_n$, two-term rate, beta-min with $\sigma_\star^2$).
2. **§6.1 items 2 and 3** (T8 finding 3). The comparisons with the draft are now marked as comparisons with the frozen draft.
3. **§6.1 item 5** (T7 finding 1, T8 finding 2). Corrected asymptotic orders: $\delta_n\sim3\sqrt{\log n/n}$, $\epsilon_n\sim\frac{3C_A}{2}(\log n)^{3/2}/\sqrt n$; noted that, in reviewer C's setting completed with $a_0=0.01$, $\varphi_0^2=1$, the second term of $\delta_n$ dominates numerically up to about $n=1.4\times10^6$ and that $r_n\le\frac12$ holds from $n\approx3.84\times10^5$ on (grid of step 1000; `proofs/_audit/group_C/check_audit_C.py`). The parameter setting and the crossing point were added after the Sol confirmation exchanges (the T7 and T8 auditors objected to the earlier, underspecified wording).
4. **Remark 4.4** (T7 findings 2 and 3). The sharpness heuristic is restricted to orthogonal (nearly independent-score) designs, with the Sol equicorrelated example showing that (SE) and polynomial $p$ allow the smaller order $O_{\mathbb P}(n^{-1/2})$ (checked numerically, block T7 #2); the direction "lower bound on $Z$" is corrected to "upper bound on $Z$ (or control of $Z/[p(S_0)m(S_0)]$)".
