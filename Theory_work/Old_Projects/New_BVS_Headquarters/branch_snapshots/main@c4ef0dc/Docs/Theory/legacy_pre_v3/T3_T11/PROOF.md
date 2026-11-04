# Proof of Theorem T3 (the start's limit and the switch gap) and Theorem T11 (what the start screens), with the sufficiency of $\|\Gamma_n-\Gamma\|=O(n^{-1/2})$ (hence of $O(1/n)$) for (R)

Lead: Fable 5.1 (theorem-proving protocol). Date: 14 October 2026. Status: **not adopted** (the proof enters the paper only after the person has walked through it).

Notation follows Section 2 of the draft; the few additions are introduced in §0–§1. Results proved here are numbered Lemma 1–4 and Proposition 6; the draft's results are cited by their identifiers (T3, T11, F4, ...); auxiliary facts inside proofs are labelled (N1)–(N4) to avoid clashing with the draft's Facts F1–F4. Nothing from the draft other than Fact F4 and standard probability and linear algebra is assumed, and F4 is in fact not needed (Lemma 1 re-derives the finite-$n$ projection it describes).

---

## 0. Setting and frozen statements

### 0.1 Setting (S)

Throughout, $n\to\infty$ along a sequence of fixed designs $X=X_n\in\mathbb R^{n\times p}$, and:

* (S1) $p$, the partition $[p]=C_1\cup\dots\cup C_L$ (with $|C_b|\le B$), $\beta^\star\in\mathbb R^p$, $\sigma_\star^2>0$ and the hyperparameters $a_0,b_0>0$ are fixed. $S_0=\operatorname{supp}(\beta^\star)$, $s_0=|S_0|$.
* (S2) The model prior is a fixed size-only prior, $p(S)=w(|S|)\mathbf 1\{|S|\le k_{\max}\}/W$, with $w(k)>0$ for $0\le k\le p$, and the cap satisfies $k_{\max}=k_{\max}(n)\ge p$ for all large $n$. (The operational cap $\lfloor n/2\rfloor$ qualifies as soon as $n\ge 2p$; so does "no cap". This is **added hypothesis H1**; it is what "the prior is $O(1)$" in the prover note means.)
* (S3) Columns are standardised, $\|x_j\|^2=n$, and $\Gamma_n:=X_n^\top X_n/n\to\Gamma\succ0$ (entrywise; all norms on $\mathbb R^{p\times p}$ are equivalent).
* (S4) $y=\mu+\varepsilon$ with $\mu=X_n\beta^\star$ and $\varepsilon\sim N_n(0,\sigma_\star^2 I_n)$; $\mathbb P_0$ is the law of $\varepsilon$ (the design is fixed). "In probability" refers to $\mathbb P_0$.

Standard notation (Section 2 of the draft): for $T\subseteq[p]$, $X_T$, $G_T=X_T^\top X_T$, $z_T=X_T^\top y$, $P_T$ the orthogonal projection onto $\operatorname{col}(X_T)$; $H_T=(n+1)G_T+I$, $D_T=\det H_T/\det(G_T+I)$, $t_T=n\,z_T^\top H_T^{-1}z_T$, $Q_T=y^\top y-t_T$, $\nu=a_0+n/2$; $m(T)=C_nD_T^{-1/2}(2b_0+Q_T)^{-\nu}$, $\mathrm{BF}(T)=m(T)/m(\emptyset)$. For $T=\emptyset$: $P_\emptyset=0$, $D_\emptyset=1$, $t_\emptyset=0$, $Q_\emptyset=y^\top y$. For a model $S$, $S_b=S\cap C_b$. Start and posterior:
$$
\pi_0(S)=\frac{p(S)\prod_b \mathrm{BF}(S_b)}{\bar Z_0},\qquad \pi(S)=\frac{p(S)\,\mathrm{BF}(S)}{\sum_{S'}p(S')\mathrm{BF}(S')}.
$$

### 0.2 Residual variances, (U), (R)

For $T\subseteq[p]$ with $\Gamma_{n,TT}\succ0$ (automatic for large $n$ by (S3)) put
$$
\bar\sigma^2_n(T)=\sigma_\star^2+\beta^{\star\top}\big(\Gamma_n-\Gamma_{n,\cdot T}\Gamma_{n,TT}^{-1}\Gamma_{n,T\cdot}\big)\beta^\star,\qquad
\bar\sigma^2(T)=\sigma_\star^2+\beta^{\star\top}\big(\Gamma-\Gamma_{\cdot T}\Gamma_{TT}^{-1}\Gamma_{T\cdot}\big)\beta^\star,
$$
with the convention that the subtracted term is absent when $T=\emptyset$. Lemma 1(d) below shows $\bar\sigma^2_n(T)\to\bar\sigma^2(T)$, so this agrees with the draft's definition $\bar\sigma^2(T)=\lim_n\bar\sigma^2_n(T)$. For $T\subseteq C_b$ the draft writes $\bar\sigma^2_b(T):=\bar\sigma^2(T)$ ("the variance seen by block $b$ alone").

A set $T\subseteq C_b$ is a **population minimiser** (for block $b$) if $\bar\sigma^2(T)=\min_{T'\subseteq C_b}\bar\sigma^2(T')$.

* **(U)** For each $b$, the population minimisers for block $b$ have a unique element $\tilde T_b$ of minimal cardinality.
* **(R)** For each $b$ and each $T\subseteq C_b$: (R1) $n[\bar\sigma_n^2(T)-\bar\sigma_n^2(\tilde T_b)]=O(1)$ if $T\supsetneq\tilde T_b$ and $T$ is a population minimiser; (R2) $n[\bar\sigma_n^2(T)-\bar\sigma_n^2(\tilde T_b)]\ge\omega_n\log n$ for every other $T\ne\tilde T_b$, where $\omega_n\to\infty$ (one sequence for all $b,T$, which is no loss since there are finitely many pairs).

$\tilde S_0=\bigcup_b\tilde T_b$. For each block, $\gamma_b=\Gamma_{C_bC_b}^{-1}\Gamma_{C_b,[p]}\beta^\star\in\mathbb R^{C_b}$ (well defined because $\Gamma\succ0$ implies $\Gamma_{C_bC_b}\succ0$), and $b(j)$ is the block containing $j$.

### 0.3 Statements proved

**Theorem T3.** Under (S), (U) and (R), in probability:

1. $\pi_0(\tilde S_0)\to1$ and $\pi(S_0)\to1$.
2. $\Delta_0(n):=\log\{\pi_0(\tilde S_0)/\pi_0(S_0)\}$ satisfies $\Delta_0(n)/n\to\kappa_0:=\tfrac12\sum_b\log\{\bar\sigma^2_b(S_0\cap C_b)/\bar\sigma^2_b(\tilde T_b)\}\in[0,\infty)$.
3. If $\kappa_0=0$ but $\tilde S_0\neq S_0$, then $|S_0|>|\tilde S_0|$ and $\Delta_0(n)=\tfrac{|S_0|-|\tilde S_0|}{2}\log n+O_{\mathbb P}(1)$.
4. If $\tilde S_0\not\supseteq S_0$, then $\tfrac1n\log\{\pi(S_0)/\pi(\tilde S_0)\}\to\kappa_1:=\tfrac12\log\{\bar\sigma^2(\tilde S_0)/\sigma_\star^2\}>0$. If $\tilde S_0\supsetneq S_0$, then $\log\{\pi(S_0)/\pi(\tilde S_0)\}=\tfrac{|\tilde S_0|-|S_0|}{2}\log n+O_{\mathbb P}(1)$.

**Claim (R-suff).** Under (S), $\|\Gamma_n-\Gamma\|=O(n^{-1/2})$ implies (R); in particular the draft's sufficient condition $\|\Gamma_n-\Gamma\|=O(1/n)$ does. ((U) holds under (S) alone.) The rate $n^{-1/2}$ cannot be weakened to $n^{-1/2+\epsilon}$: see Remark 5.1.

**Theorem T11.** Items 1–3 are under (S) (which already gives $\Gamma_{C_bC_b}\succ0$ for every $b$). Item 4 is **not** under (S): the draft states it with $p\le n^A$, $|C_b|\le B$ and a margin $M_n\to\infty$, i.e. for a triangular array in which $p$, the design, the partition and $S_0$ may vary with $n$; its exact setting is (H) in §7. (The draft's T11 preamble "in the fixed-$p$ setting of T3" conflicts with item (iv)'s own hypothesis $p\le n^A$; we read (iv) in the growing-$p$ sense, which is the only one in which it says something new: under (S) the operational cap is eventually inactive and (iv) is a special case of Proposition 6.)

1. $\tilde T_b=\operatorname{supp}(\gamma_b)$; in particular (U) holds, and $\tilde S_0=\bigcup_b\operatorname{supp}(\gamma_b)$.
2. $S_0\setminus\tilde S_0=\{j\in S_0:\gamma_{b(j),j}=0\}$ and $\tilde S_0\setminus S_0=\{j\notin S_0:\gamma_{b(j),j}\ne0\}$.
3. If no true variable is cancelled ($\gamma_{b(j),j}\ne0$ for all $j\in S_0$), then $\tilde S_0\supseteq S_0$; under (R), $\pi_0(\{S:S\supseteq S_0\})\to1$ in probability; every switch then consists of deletions only (passing from $\tilde S_0$ to $S_0$ removes $\tilde S_0\setminus S_0$ and adds nothing); if moreover $\tilde S_0\ne S_0$ then $\log\{\pi(S_0)/\pi(\tilde S_0)\}=\tfrac{|\tilde S_0|-|S_0|}{2}\log n+O_{\mathbb P}(1)$ while $\Delta_0(n)$ may be linear in $n$; and if $\Gamma_{C_b,C_b^c}\beta^\star_{C_b^c}=0$ for every $b$ then $\gamma_b=\beta^\star_{C_b}$ for every $b$ and $\tilde S_0=S_0$.
4. (High-dimensional screening, setting (H) of §7.) **False as stated** with the operational cap $k_{\max}=\lfloor n/2\rfloor$ once $p\ge k_{\max}+2$, which the hypothesis $p\le n^A$ permits exactly when $A\ge1$ (counterexample in §7.1, which satisfies every hypothesis listed in (iv) with $p=n$, $B=1$, $s_0=2$, and the nonzero entries of $\beta^\star$ fixed; for $A<1$ the operational cap is eventually inactive and (iv) is true by Proposition 6). **True for the $\mathrm{BB}(1,p)$ prior without a cap** ($k_{\max}\ge p$), and in general true up to the start's mass above $k_{\max}-B$ (Proposition 6 in §7.2).

Remarks on hypotheses. (a) T3 is stated "with (U) and (R)"; under (S), (U) is automatic (Lemma 1(b)), and the proof uses it only in the form of Lemma 1(b). (b) (R) is used only in T3(i) (for the start), T3(iii), and T11(iii); the posterior statement $\pi(S_0)\to1$, T3(ii) and T3(iv) need only (S). (c) The second bullet of (R) is consistent with the first only because every population minimiser contains $\tilde T_b$ (Lemma 1(b), which needs $\Gamma_{C_bC_b}\succ0$); without that, a population minimiser $T\not\supseteq\tilde T_b$ would be required to have a gap $\ge\omega_n\log n$, which $\|\Gamma_n-\Gamma\|=O(n^{-1/2})$ rules out. This is why Claim (R-suff) needs the block-wise positive definiteness that $\Gamma\succ0$ supplies, and not merely (U).

---

## 1. Preliminaries

### 1.1 The prior is $O(1)$

By (S2), for $n$ large the cap is inactive and $p(S)=w(|S|)/W$ with $W=\sum_k\binom pk w(k)$ fixed. Put $c_w=\min_{0\le k\le p}w(k)/\max_{0\le k\le p}w(k)\in(0,1]$. Then for all models $S,S'$,
$$
|\log\{p(S)/p(S')\}|\le\log(1/c_w)=:C_w<\infty. \tag{1.1}
$$

### 1.2 Bayes factors in a convenient form

Put $\tilde Q_T:=2b_0+Q_T=2b_0+y^\top y-t_T$. Since $t_\emptyset=0$, $\tilde Q_\emptyset=2b_0+y^\top y=A_0$ and $(2b_0+Q_T)/(2b_0+Q_\emptyset)=1-t_T/A_0$, which recovers the draft's $\mathrm{BF}(S)=D_S^{-1/2}(1-t_S/A_0)^{-\nu}$. For any two models $T,T'\subseteq[p]$,
$$
\log\mathrm{BF}(T)-\log\mathrm{BF}(T')=-\tfrac12\log\frac{D_T}{D_{T'}}-\nu\log\frac{\tilde Q_T}{\tilde Q_{T'}} . \tag{1.2}
$$
Hence, for models $S,S'$,
$$
\log\frac{\pi_0(S)}{\pi_0(S')}=\log\frac{p(S)}{p(S')}+\sum_b\Big[\log\mathrm{BF}(S_b)-\log\mathrm{BF}(S'_b)\Big],\qquad
\log\frac{\pi(S)}{\pi(S')}=\log\frac{p(S)}{p(S')}+\log\mathrm{BF}(S)-\log\mathrm{BF}(S'). \tag{1.3}
$$
Note $\tilde Q_T>0$ always: in an eigenbasis $(u_i,g_i)$ of $G_T$, $t_T=n\sum_i(u_i^\top z_T)^2/((n+1)g_i+1)$; since $z_T=X_T^\top y\in\operatorname{range}(X_T^\top)=\operatorname{range}(G_T)$, the directions with $g_i=0$ contribute nothing, and on the others $n/((n+1)g_i+1)<1/g_i$, so $t_T\le\sum_{g_i>0}(u_i^\top z_T)^2/g_i=\|P_Ty\|^2\le\|y\|^2$. (Lemma 2(b) below refines this when $G_T\succ0$.)

### 1.3 Residual variances as squared distances

**Lemma 1 (geometry of $\bar\sigma^2$).** Let $A\in\mathbb R^{p\times p}$ be symmetric positive semidefinite, write $A=V^\top V$ with $V\in\mathbb R^{m\times p}$ (any such factorisation), let $v_j$ be the $j$-th column of $V$, and put $f=V\beta^\star=\sum_j\beta^\star_jv_j$. For $T\subseteq[p]$ with $A_{TT}\succ0$ (and for $T=\emptyset$) define
$$
R_A(T)=\beta^{\star\top}\big(A-A_{\cdot T}A_{TT}^{-1}A_{T\cdot}\big)\beta^\star ,\qquad R_A(\emptyset)=\beta^{\star\top}A\beta^\star .
$$
Let $\Pi_T$ be the orthogonal projection of $\mathbb R^m$ onto $\operatorname{span}\{v_j:j\in T\}$ ($\Pi_\emptyset=0$). Then:

* (a) $R_A(T)=\|f-\Pi_Tf\|^2=\operatorname{dist}(f,\operatorname{span}\{v_j:j\in T\})^2$. In particular $R_A\ge0$ and $R_A(T)\ge R_A(T')$ whenever $T\subseteq T'$.
* (b) Let $C\subseteq[p]$ with $A_{CC}\succ0$ and $\gamma:=A_{CC}^{-1}A_{C,[p]}\beta^\star\in\mathbb R^{C}$. Then $\Pi_Cf=\sum_{j\in C}\gamma_jv_j$, this representation is unique, $\gamma_j=\beta^\star_j+[A_{CC}^{-1}A_{C,C^c}\beta^\star_{C^c}]_j$, and for $T\subseteq C$: $R_A(T)=R_A(C)$ if and only if $\operatorname{supp}(\gamma)\subseteq T$. Consequently the minimisers of $R_A$ over $2^{C}$ are exactly the sets $T$ with $\operatorname{supp}(\gamma)\subseteq T\subseteq C$, and $\operatorname{supp}(\gamma)$ is the unique minimiser of minimal cardinality.
* (c) If $A\succ0$, then $R_A(S)=0$ if and only if $S\supseteq S_0$.
* (d) (Finite $n$ and the limit.) With $A=\Gamma_n$ one may take $V=X_n/\sqrt n$, so $f=\mu/\sqrt n$, $\Pi_T=P_T$ and
  $$
  \bar\sigma^2_n(T)-\sigma_\star^2=R_{\Gamma_n}(T)=\tfrac1n\|(I-P_T)\mu\|^2 .
  $$
  With $A=\Gamma$, $\bar\sigma^2(T)-\sigma_\star^2=R_\Gamma(T)$. Moreover, with $\lambda:=\lambda_{\min}(\Gamma)>0$ and $\|\cdot\|$ the spectral norm, there is a constant $K$ (depending on $\Gamma$, $\beta^\star$ and $p$ only) such that for every $T\subseteq[p]$,
  $$
  |\bar\sigma^2_n(T)-\bar\sigma^2(T)|\le K\,\|\Gamma_n-\Gamma\|\qquad\text{whenever }\|\Gamma_n-\Gamma\|\le\lambda/2. \tag{1.4}
  $$
  In particular $\bar\sigma^2_n(T)\to\bar\sigma^2(T)$ under (S3).
* (e) (Second-order gaps above a minimiser.) Let $C\subseteq[p]$, $\gamma=\Gamma_{CC}^{-1}\Gamma_{C,[p]}\beta^\star$, $\tilde T=\operatorname{supp}(\gamma)$, and $\tilde T\subseteq T\subseteq C$. There is a constant $K'$ (depending on $\Gamma$, $\beta^\star$, $p$) such that for every symmetric $A'$ with $\|A'-\Gamma\|\le\lambda/2$,
  $$
  0\le R_{A'}(\tilde T)-R_{A'}(T)\le K'\,\|A'-\Gamma\|^2 . \tag{1.4$'$}
  $$
  In particular, under (S3), $0\le n[\bar\sigma_n^2(\tilde T)-\bar\sigma_n^2(T)]\le K'n\|\Gamma_n-\Gamma\|^2$ for $n$ large.

*Proof.* (a) For $T=\emptyset$ both sides equal $\|f\|^2$. For $T\neq\emptyset$, $A_{TT}=V_T^\top V_T\succ0$ means $V_T$ has full column rank, so $\Pi_T=V_T(V_T^\top V_T)^{-1}V_T^\top$ and
$\beta^{\star\top}A_{\cdot T}A_{TT}^{-1}A_{T\cdot}\beta^\star=f^\top V_T(V_T^\top V_T)^{-1}V_T^\top f=\|\Pi_Tf\|^2$, while $\beta^{\star\top}A\beta^\star=\|f\|^2$. Pythagoras gives $R_A(T)=\|f\|^2-\|\Pi_Tf\|^2=\|f-\Pi_Tf\|^2$. Monotonicity: the span grows with $T$.

(b) $\Pi_Cf=V_C(V_C^\top V_C)^{-1}V_C^\top V\beta^\star=V_CA_{CC}^{-1}A_{C,[p]}\beta^\star=V_C\gamma$. Since $V_C$ has full column rank, the coefficient vector of any element of $\operatorname{span}(v_C)$ is unique. The alternative formula follows from $A_{C,[p]}\beta^\star=A_{CC}\beta^\star_C+A_{C,C^c}\beta^\star_{C^c}$. For $T\subseteq C$: $\operatorname{span}(v_T)\subseteq\operatorname{span}(v_C)$, so $\operatorname{dist}(f,\operatorname{span}v_T)\ge\operatorname{dist}(f,\operatorname{span}v_C)$, with equality iff the nearest point $\Pi_Cf$ of $\operatorname{span}(v_C)$ lies in $\operatorname{span}(v_T)$ (if it does, $\Pi_Tf=\Pi_Cf$; if the distances agree, $\Pi_Tf\in\operatorname{span}(v_C)$ is a nearest point of $\operatorname{span}(v_C)$, hence equals $\Pi_Cf$ by uniqueness of the nearest point). If $\Pi_Cf=\sum_{j\in T}c_jv_j$ then, extending $c$ by zero to $C$, uniqueness of coefficients gives $c=\gamma$, hence $\operatorname{supp}(\gamma)\subseteq T$; the converse is immediate. The description of the minimisers follows, and among the supersets of $\operatorname{supp}(\gamma)$ only $\operatorname{supp}(\gamma)$ has minimal cardinality.

(c) If $A\succ0$ then $V$ has rank $p$, so $v_1,\dots,v_p$ are linearly independent. $R_A(S)=0$ iff $f\in\operatorname{span}(v_S)$ iff the unique representation $f=\sum_j\beta^\star_jv_j$ has support in $S$, i.e. $S_0\subseteq S$.

(d) With $V=X_n/\sqrt n$, $V^\top V=\Gamma_n$, $f=\mu/\sqrt n$ and $\Pi_T=P_T$; apply (a). For (1.4): if $\|\Gamma_n-\Gamma\|\le\lambda/2$ then $\lambda_{\min}(\Gamma_{n,TT})\ge\lambda_{\min}(\Gamma_n)\ge\lambda/2$ (Cauchy interlacing for principal submatrices, Weyl's inequality for the perturbation), and $\lambda_{\min}(\Gamma_{TT})\ge\lambda$. For symmetric $M,M'\succeq(\lambda/2)I$, $\|M^{-1}-M'^{-1}\|=\|M^{-1}(M'-M)M'^{-1}\|\le(2/\lambda)^2\|M-M'\|$. Writing $\Phi_T(A)=A_{\cdot T}A_{TT}^{-1}A_{T\cdot}$ and using $\|E_1E_2E_3-E_1'E_2'E_3'\|\le\|E_1-E_1'\|\|E_2\|\|E_3\|+\|E_1'\|\|E_2-E_2'\|\|E_3\|+\|E_1'\|\|E_2'\|\|E_3-E_3'\|$ with $\|\Gamma_n\|\le\|\Gamma\|+\lambda/2$ and $\|\Gamma_{n,TT}^{-1}\|\le2/\lambda$, one gets $\|\Phi_T(\Gamma_n)-\Phi_T(\Gamma)\|\le K_0\|\Gamma_n-\Gamma\|$ with $K_0=K_0(\|\Gamma\|,\lambda)$. Then $|\bar\sigma_n^2(T)-\bar\sigma^2(T)|\le\|\beta^\star\|^2(1+K_0)\|\Gamma_n-\Gamma\|$. For $T=\emptyset$ the bound is $\|\beta^\star\|^2\|\Gamma_n-\Gamma\|$.

(e) Let $E:=T\setminus\tilde T$; if $E=\emptyset$ there is nothing to prove. For $\|A'-\Gamma\|\le\lambda/2$ we have $A'_{TT}\succeq(\lambda/2)I$ as in (d); factor $A'=V'^\top V'$, put $f'=V'\beta^\star$, and let $\Pi'_T,\Pi'_{\tilde T}$ be the projections of (a). By (a) and Pythagoras, $R_{A'}(\tilde T)-R_{A'}(T)=\|\Pi'_Tf'\|^2-\|\Pi'_{\tilde T}f'\|^2=\|(\Pi'_T-\Pi'_{\tilde T})f'\|^2\ge0$. The subspace $\operatorname{col}(V'_T)\ominus\operatorname{col}(V'_{\tilde T})$ is spanned by the columns of $W':=(I-\Pi'_{\tilde T})V'_E$, which are linearly independent because $V'_T$ has full column rank; hence $\Pi'_T-\Pi'_{\tilde T}=W'(W'^\top W')^{-1}W'^\top$ and
$$
R_{A'}(\tilde T)-R_{A'}(T)=s(A')^\top\big(W'^\top W'\big)^{-1}s(A'),\qquad s(A'):=W'^\top f'=A'_{E,\cdot}\beta^\star-A'_{E\tilde T}(A'_{\tilde T\tilde T})^{-1}A'_{\tilde T,\cdot}\beta^\star ,
$$
where $W'^\top W'=A'_{EE}-A'_{E\tilde T}(A'_{\tilde T\tilde T})^{-1}A'_{\tilde TE}$ is the Schur complement of $A'_{\tilde T\tilde T}$ in $A'_{TT}$ (when $\tilde T=\emptyset$ read $s(A')=A'_{E,\cdot}\beta^\star$ and $W'^\top W'=A'_{EE}$). A Schur complement of a positive definite matrix satisfies $v^\top(W'^\top W')v=\min_u\binom uv^\top A'_{TT}\binom uv\ge\lambda_{\min}(A'_{TT})\|v\|^2$, so $\lambda_{\min}(W'^\top W')\ge\lambda/2$. The map $A'\mapsto s(A')$ is rational with denominators bounded away from zero on $\{\|A'-\Gamma\|\le\lambda/2\}$ (the same three-term estimate as in (d)), hence Lipschitz there: $\|s(A')-s(\Gamma)\|\le L_s\|A'-\Gamma\|$ (explicitly, $L_s\le\|\beta^\star\|(1+K_0)$, since $A\mapsto A_{E\tilde T}A_{\tilde T\tilde T}^{-1}A_{\tilde T,\cdot}$ is a row block of $\Phi_{\tilde T}(A)$). Finally $s(\Gamma)=0$: by (b), $\Pi_Tf=\Pi_Cf=\Pi_{\tilde T}f$ because $\operatorname{supp}(\gamma)\subseteq\tilde T\subseteq T\subseteq C$, so $W(W^\top W)^{-1}W^\top f=0$, and multiplying by $W^\top$ gives $W^\top f=s(\Gamma)=0$. Therefore $R_{A'}(\tilde T)-R_{A'}(T)\le\|s(A')\|^2/\lambda_{\min}(W'^\top W')\le(2L_s^2/\lambda)\|A'-\Gamma\|^2$, so $K'=2L_s^2/\lambda$ (a common constant over the finitely many triples $(C,\tilde T,T)$ is obtained by taking the maximum). $\square$

**Consequences used below.** Under (S):

* (1.5) For every $b$, the population minimisers for block $b$ are exactly $\{T:\operatorname{supp}(\gamma_b)\subseteq T\subseteq C_b\}$; hence (U) holds with $\tilde T_b=\operatorname{supp}(\gamma_b)$, and **every population minimiser contains $\tilde T_b$**. (Lemma 1(b) with $A=\Gamma$, $C=C_b$.)
* (1.6) $\bar\sigma^2(S)=\sigma_\star^2$ iff $S\supseteq S_0$; and $\bar\sigma^2_n(S)=\sigma_\star^2$ exactly, for every $n$ at which $\bar\sigma^2_n(S)$ is defined ($\Gamma_{n,SS}\succ0$, hence for all large $n$), when $S\supseteq S_0$ (because then $\mu=X_{S_0}\beta^\star_{S_0}\in\operatorname{col}(X_S)$, so $(I-P_S)\mu=0$). (Lemma 1(c),(d).)
* (1.7) For $T\subseteq T'$: $a_n(T,T'):=n[\bar\sigma^2_n(T)-\bar\sigma^2_n(T')]=\|(I-P_T)\mu\|^2-\|(I-P_{T'})\mu\|^2=\|(P_{T'}-P_T)\mu\|^2\ge0$, because $P_{T'}-P_T$ is the orthogonal projection onto $\operatorname{col}(X_{T'})\ominus\operatorname{col}(X_T)$ and $(I-P_T)\mu=(I-P_{T'})\mu+(P_{T'}-P_T)\mu$ is an orthogonal decomposition.

---

## 2. Deterministic facts about $D_T$ and $t_T$

**Lemma 2.** Let $T\ne\emptyset$ with $G_T\succ0$ and $g_T:=\lambda_{\min}(G_T)$. Then

* (a) $|T|\log(n+1)-|T|/g_T\le\log D_T\le|T|\log(n+1)$; moreover $D_T\ge1$, since each factor $\frac{(n+1)g_i+1}{g_i+1}$ is $\ge1$.
* (b) $d_T:=\|P_Ty\|^2-t_T$ satisfies $0\le d_T\le\dfrac{1+1/g_T}{n+1}\,\|P_Ty\|^2$.

For $T=\emptyset$, $\log D_\emptyset=0$ and $d_\emptyset=0$. Consequently, for every $T$,
$$
\tilde Q_T=2b_0+\mathrm{RSS}_T+d_T,\qquad \mathrm{RSS}_T:=\|(I-P_T)y\|^2 . \tag{2.0}
$$

*Proof.* Diagonalise $G_T=\sum_ig_iu_iu_i^\top$ with $g_i\ge g_T>0$; then $H_T=\sum_i((n+1)g_i+1)u_iu_i^\top$ and $G_T+I=\sum_i(g_i+1)u_iu_i^\top$.

(a) $D_T=\prod_i\frac{(n+1)g_i+1}{g_i+1}$ and $\frac{(n+1)g+1}{g+1}=(n+1)\Big(1-\frac{n}{(n+1)(g+1)}\Big)$. With $u=\frac{n}{(n+1)(g+1)}\in(0,\frac1{g+1}]$ we have $\log(1-u)\le0$ and $\log(1-u)\ge-\frac{u}{1-u}\ge-\frac{1/(g+1)}{g/(g+1)}=-\frac1g\ge-\frac1{g_T}$. Sum over $i$.

(b) $P_T=X_TG_T^{-1}X_T^\top$ gives $\|P_Ty\|^2=z_T^\top G_T^{-1}z_T$, and $t_T=n\,z_T^\top H_T^{-1}z_T$. In the common eigenbasis,
$$
G_T^{-1}-nH_T^{-1}=\sum_i\Big[\frac1{g_i}-\frac{n}{(n+1)g_i+1}\Big]u_iu_i^\top=\sum_i\frac{g_i+1}{g_i\,((n+1)g_i+1)}\,u_iu_i^\top ,
$$
so $d_T=\sum_i\frac{g_i+1}{(n+1)g_i+1}\cdot\frac{(u_i^\top z_T)^2}{g_i}$. Each coefficient $\frac{g_i+1}{(n+1)g_i+1}$ lies in $\big(0,\frac{1+1/g_T}{n+1}\big]$ (since $\frac{g+1}{(n+1)g+1}\le\frac{g+1}{(n+1)g}=\frac{1+1/g}{n+1}$), and $\sum_i(u_i^\top z_T)^2/g_i=\|P_Ty\|^2$. Finally (2.0): $\tilde Q_T=2b_0+\|y\|^2-t_T=2b_0+(\|y\|^2-\|P_Ty\|^2)+d_T$. $\square$

Under (S): since $\Gamma_n\to\Gamma$, there is $n_0$ with $\lambda_{\min}(\Gamma_n)\ge\lambda/2$ for $n\ge n_0$ ($\lambda=\lambda_{\min}(\Gamma)$), hence $g_T\ge n\lambda/2$ for every $T\ne\emptyset$ (interlacing), and for $n\ge\max(n_0,2/\lambda)$:
$$
\log D_T=|T|\log n+r_T,\quad |r_T|\le |T|\Big(\frac1n+\frac{2}{n\lambda}\Big); \qquad 0\le d_T\le\frac{2\|y\|^2}{n+1}. \tag{2.1}
$$
(The first uses $0\le\log(n+1)-\log n\le1/n$; the second uses $\|P_Ty\|^2\le\|y\|^2$ and $1+1/g_T\le2$.)

---

## 3. The stochastic comparison lemma

For $T\subseteq U\subseteq[p]$ put $a_n(T,U):=\|(P_U-P_T)\mu\|^2=\|(I-P_T)\mu\|^2-\|(I-P_U)\mu\|^2\ge0$ (as in (1.7); under (S) this equals $n[\bar\sigma_n^2(T)-\bar\sigma_n^2(U)]$).

**Lemma 3 (exact decomposition; purely algebraic, any design).** Let $T,T'\subseteq[p]$, $U:=T\cup T'$, and $a:=\|(I-P_T)\mu\|^2-\|(I-P_{T'})\mu\|^2=a_n(T,U)-a_n(T',U)$. Then
$$
\tilde Q_T-\tilde Q_{T'}=a+\xi+\eta,\qquad \xi:=2\mu^\top(P_{T'}-P_T)\varepsilon,\qquad \eta:=\varepsilon^\top(P_{T'}-P_T)\varepsilon+d_T-d_{T'},
$$
where $\xi\sim N\big(0,\,4\sigma_\star^2\|(P_{T'}-P_T)\mu\|^2\big)$ with $\|(P_{T'}-P_T)\mu\|\le\sqrt{a_n(T,U)}+\sqrt{a_n(T',U)}$, and $|\eta|\le2\,\varepsilon^\top P_U\varepsilon+d_T+d_{T'}$. If $T\subseteq T'$ then $U=T'$, $a=a_n(T,T')\ge0$, $\|(P_{T'}-P_T)\mu\|^2=a$ and $\varepsilon^\top(P_{T'}-P_T)\varepsilon\ge0$. If $T\supseteq T'$ then $U=T$, $a=-a_n(T',T)\le0$, $\|(P_{T'}-P_T)\mu\|^2=-a$ and $\varepsilon^\top(P_{T'}-P_T)\varepsilon\le0$.

*Proof.* By (2.0), $\tilde Q_T-\tilde Q_{T'}=\mathrm{RSS}_T-\mathrm{RSS}_{T'}+d_T-d_{T'}$. Since $I-P_T$ is symmetric idempotent, $\mathrm{RSS}_T=\|(I-P_T)\mu\|^2+2\mu^\top(I-P_T)\varepsilon+\varepsilon^\top(I-P_T)\varepsilon$, and subtracting the same expansion for $T'$ gives $\mathrm{RSS}_T-\mathrm{RSS}_{T'}=a+2\mu^\top(P_{T'}-P_T)\varepsilon+\varepsilon^\top(P_{T'}-P_T)\varepsilon$. The variable $\xi$ is a linear functional of the Gaussian vector $\varepsilon$, hence Gaussian with variance $4\sigma_\star^2\|(P_{T'}-P_T)\mu\|^2$. Since $T,T'\subseteq U$, $P_U-P_T$ and $P_U-P_{T'}$ are orthogonal projections (onto $\operatorname{col}(X_U)\ominus\operatorname{col}(X_T)$, resp. $\ominus\operatorname{col}(X_{T'})$), and $P_{T'}-P_T=(P_U-P_T)-(P_U-P_{T'})$. Therefore $\|(P_{T'}-P_T)\mu\|\le\|(P_U-P_T)\mu\|+\|(P_U-P_{T'})\mu\|=\sqrt{a_n(T,U)}+\sqrt{a_n(T',U)}$, and $|\varepsilon^\top(P_{T'}-P_T)\varepsilon|\le\varepsilon^\top(P_U-P_T)\varepsilon+\varepsilon^\top(P_U-P_{T'})\varepsilon\le2\varepsilon^\top P_U\varepsilon$ (each quadratic form of a projection $\preceq P_U$ is between $0$ and $\varepsilon^\top P_U\varepsilon$). The nested case is immediate. $\square$

**Lemma 4 (three regimes).** Assume (S). Let $T,T'\subseteq[p]$ be fixed, $U=T\cup T'$, and $a=a_n(T,U)-a_n(T',U)=n[\bar\sigma^2_n(T)-\bar\sigma^2_n(T')]$. Then, in probability:

* (a) (Linear scale; always.) $\dfrac1n\big[\log\mathrm{BF}(T)-\log\mathrm{BF}(T')\big]\to-\tfrac12\log\dfrac{\bar\sigma^2(T)}{\bar\sigma^2(T')}$.
* (b) (Bounded gap.) If $a_n(T,U)=O(1)$ and $a_n(T',U)=O(1)$ (equivalently $a=O(1)$ and $a_n(T',U)=O(1)$; for $T\supsetneq T'$ this is just $a=O(1)$), then
  $$
  \log\mathrm{BF}(T)-\log\mathrm{BF}(T')=-\frac{|T|-|T'|}{2}\log n-\frac{a+\xi+\eta}{2\bar\sigma^2(T')}+o_{\mathbb P}(1)=-\frac{|T|-|T'|}{2}\log n+O_{\mathbb P}(1). \tag{3.1}
  $$
* (c) (Gap growing faster than $\log n$.) If $a\ge\omega_n\log n$ with $\omega_n\to\infty$ and $a_n(T',U)=O(1)$, then $\log\mathrm{BF}(T)-\log\mathrm{BF}(T')\to-\infty$.

*Proof.* We first record facts that hold simultaneously for the finitely many subsets of $[p]$.

* (N1) $\varepsilon^\top\varepsilon/n\to\sigma_\star^2$ (law of large numbers); for each $U$, $\varepsilon^\top P_U\varepsilon\sim\sigma_\star^2\chi^2_{\operatorname{rank}P_U}=O_{\mathbb P}(1)$; $\|y\|^2\le2\|\mu\|^2+2\|\varepsilon\|^2=O_{\mathbb P}(n)$ because $\|\mu\|^2=n\beta^{\star\top}\Gamma_n\beta^\star=O(n)$; hence by (2.1) $d_T=O_{\mathbb P}(1)$ for every $T$.
* (N2) $\mu^\top(I-P_T)\varepsilon/n\to0$: it is $N(0,\sigma_\star^2\|(I-P_T)\mu\|^2/n^2)$ and $\|(I-P_T)\mu\|^2\le\|\mu\|^2=O(n)$.
* (N3) $\tilde Q_T/n\to\bar\sigma^2(T)\ \ (\ge\sigma_\star^2>0)$: by (2.0), $\tilde Q_T/n=2b_0/n+\mathrm{RSS}_T/n+d_T/n$ and $\mathrm{RSS}_T/n=(\bar\sigma_n^2(T)-\sigma_\star^2)+2\mu^\top(I-P_T)\varepsilon/n+\varepsilon^\top\varepsilon/n-\varepsilon^\top P_T\varepsilon/n\to\bar\sigma^2(T)-\sigma_\star^2+0+\sigma_\star^2-0$, by Lemma 1(d), (N1), (N2).
* (N4) By (2.1), $-\tfrac12\log(D_T/D_{T'})=-\tfrac{|T|-|T'|}{2}\log n+O(1/n)$.

(a) Divide (1.2) by $n$. The $D$-term is $O(\log n/n)\to0$ by (N4). Next $\nu/n\to\tfrac12$ and $\log(\tilde Q_T/\tilde Q_{T'})=\log\big((\tilde Q_T/n)/(\tilde Q_{T'}/n)\big)\to\log(\bar\sigma^2(T)/\bar\sigma^2(T'))$ by (N3) and the continuous mapping theorem (both limits are positive).

(b) By Lemma 3, $\tilde Q_T-\tilde Q_{T'}=a+\xi+\eta$ with $a=O(1)$; $\operatorname{Var}\xi\le4\sigma_\star^2(\sqrt{a_n(T,U)}+\sqrt{a_n(T',U)})^2=O(1)$, so $\xi=O_{\mathbb P}(1)$; and $|\eta|\le2\varepsilon^\top P_U\varepsilon+d_T+d_{T'}=O_{\mathbb P}(1)$ by (N1). Put $x:=(\tilde Q_T-\tilde Q_{T'})/\tilde Q_{T'}$. By (N3), $x=(a+\xi+\eta)/(n\bar\sigma^2(T')(1+o_{\mathbb P}(1)))=O_{\mathbb P}(1/n)$. Since $|\log(1+x)-x|\le x^2$ for $|x|\le\tfrac12$, $\nu\log(1+x)=(\tfrac n2+a_0)(x+O_{\mathbb P}(n^{-2}))=\tfrac n2x+o_{\mathbb P}(1)=\dfrac{a+\xi+\eta}{2\bar\sigma^2(T')}+o_{\mathbb P}(1)$. Insert into (1.2) with (N4).

(c) By Lemma 3, $\operatorname{Var}\xi\le4\sigma_\star^2\big(\sqrt{a+a_n(T',U)}+\sqrt{a_n(T',U)}\big)^2\le4\sigma_\star^2\big(\sqrt a+2\sqrt{a_n(T',U)}\big)^2=O(a)$, because $a\to\infty$ and $a_n(T',U)=O(1)$ (note $a_n(T,U)=a+a_n(T',U)\ge0$). Hence $\xi/a=O_{\mathbb P}(a^{-1/2})=o_{\mathbb P}(1)$, and $\eta/a=o_{\mathbb P}(1)$ since $\eta=O_{\mathbb P}(1)$. So $\tilde Q_T-\tilde Q_{T'}=a(1+\zeta_n)$ with $\zeta_n\to0$ in probability. Let $x=(\tilde Q_T-\tilde Q_{T'})/\tilde Q_{T'}$; by (N3), $x=a(1+\zeta_n)/\big(n\bar\sigma^2(T')(1+o_{\mathbb P}(1))\big)$, so with probability tending to one $x\ge\dfrac{2a}{3n\bar\sigma^2(T')}\ge0$. For $x\ge0$, concavity of $\log(1+x)$ on $[0,1]$ and monotonicity give $\log(1+x)\ge(\log2)\min(x,1)$. Therefore, with probability tending to one,
$$
\nu\log(1+x)\ \ge\ \frac n2\log2\cdot\min\Big(\frac{2a}{3n\bar\sigma^2(T')},\,1\Big)=\log2\cdot\min\Big(\frac{a}{3\bar\sigma^2(T')},\,\frac n2\Big)\ \ge\ \log2\cdot\min\Big(\frac{\omega_n\log n}{3\bar\sigma^2(T')},\,\frac n2\Big).
$$
By (1.2) and (N4), $\log\mathrm{BF}(T)-\log\mathrm{BF}(T')\le\tfrac p2\log n+O(1/n)-\log2\cdot\min\big(\tfrac{\omega_n\log n}{3\bar\sigma^2(T')},\tfrac n2\big)$, and the right side tends to $-\infty$ because $\omega_n\to\infty$ and $n/\log n\to\infty$. $\square$

*Remark 3.1 (the $O_{\mathbb P}(1)$ in (3.1) is genuinely random).* When $T\supsetneq T'$, $\eta=-\varepsilon^\top(P_T-P_{T'})\varepsilon+d_T-d_{T'}$ and $\varepsilon^\top(P_T-P_{T'})\varepsilon\sim\sigma_\star^2\chi^2_{|T|-|T'|}$ (the columns in $T\setminus T'$ add exactly $|T|-|T'|$ dimensions because $G_T\succ0$). Also $d_T-d_{T'}=O_{\mathbb P}(1/n)$ in this regime (by Lemma 2(b), $d_T=\|P_Ty\|^2/(n+1)+O_{\mathbb P}(1/n)$ and $\|P_Ty\|^2-\|P_{T'}y\|^2=\mathrm{RSS}_{T'}-\mathrm{RSS}_T=O_{\mathbb P}(1)$). So the remainder in (3.1) converges in distribution to a non-degenerate law whenever $a$ converges, and cannot be replaced by a deterministic constant or by $o_{\mathbb P}(1)$. This is the source of the "$+O_{\mathbb P}(1)$" in T3(iii)–(iv).

*Remark 3.2 (what each regime needs).* (b) uses $a=O(1)$ **together with** $a_n(T',U)=O(1)$; the second condition cannot be dropped: with $\Gamma_n=I_3$, $\beta^\star=(1,1,0)$, $T=\{1,3\}$, $T'=\{2\}$ one has $a=0$ but $a_n(T,U)=a_n(T',U)=n$ and $\operatorname{Var}\xi=8\sigma_\star^2n$, so the log Bayes factor ratio fluctuates on the scale $\sqrt n$. Keeping $a_n(T',U)=O(1)$ and weakening $a=O(1)$ to $a=o(\log n)$, the same computation gives $-\frac{|T|-|T'|}{2}\log n+o_{\mathbb P}(\log n)$, still $\to-\infty$ when $|T|>|T'|$, which suffices for T3(i)–(ii) but not for the $O_{\mathbb P}(1)$ remainder in T3(iii). (c) needs the gap to dominate $\frac p2\log n$; the rate $\omega_n\log n$ with $\omega_n\to\infty$ is the weakest form independent of $p$ and $\bar\sigma^2$.

---

## 4. Proof of Theorem T3

Assume (S), (U), (R). By (1.5), $\tilde T_b=\operatorname{supp}(\gamma_b)$ and every population minimiser of block $b$ contains $\tilde T_b$; hence the two cases of (R) are exhaustive and read: (R1) for $T\supsetneq\tilde T_b$, $n[\bar\sigma_n^2(T)-\bar\sigma_n^2(\tilde T_b)]=O(1)$; (R2) for $T\subseteq C_b$ with $T\not\supseteq\tilde T_b$, $n[\bar\sigma_n^2(T)-\bar\sigma_n^2(\tilde T_b)]\ge\omega_n\log n$.

**Step 1 (block comparisons).** Fix $b$ and $T\subseteq C_b$ with $T\ne\tilde T_b$. Then, in probability,
$$
\text{if }T\supsetneq\tilde T_b:\quad \log\mathrm{BF}(T)-\log\mathrm{BF}(\tilde T_b)=-\frac{|T|-|\tilde T_b|}{2}\log n+O_{\mathbb P}(1)\ \to-\infty; \tag{4.1}
$$
$$
\text{if }T\not\supseteq\tilde T_b:\quad \log\mathrm{BF}(T)-\log\mathrm{BF}(\tilde T_b)\to-\infty. \tag{4.2}
$$
*Proof of (4.1).* Lemma 4(b) with $T'=\tilde T_b$, $U=T$: $a=n[\bar\sigma_n^2(T)-\bar\sigma_n^2(\tilde T_b)]=O(1)$ by (R1), $a_n(T,U)=0$ and $a_n(\tilde T_b,T)=-a=O(1)$. Since $|T|>|\tilde T_b|$ the right side tends to $-\infty$.
*Proof of (4.2).* Lemma 4(c) with $T'=\tilde T_b$ and $U=T\cup\tilde T_b\supseteq\tilde T_b$: $a\ge\omega_n\log n$ by (R2), and $a_n(\tilde T_b,U)=n[\bar\sigma_n^2(\tilde T_b)-\bar\sigma_n^2(U)]=O(1)$: if $U=\tilde T_b$ (the case $T\subsetneq\tilde T_b$) it is $0$; otherwise $U\supsetneq\tilde T_b$ is a superset of $\tilde T_b$ inside $C_b$, hence a population minimiser by (1.5), and (R1) applies to $U$. $\square$

**Step 2 (T3(i), the start).** Let $S\ne\tilde S_0$. By (1.3),
$$
\log\frac{\pi_0(S)}{\pi_0(\tilde S_0)}=\log\frac{p(S)}{p(\tilde S_0)}+\sum_b\big[\log\mathrm{BF}(S_b)-\log\mathrm{BF}(\tilde T_b)\big].
$$
The prior term is bounded by $C_w$ (1.1). Blocks with $S_b=\tilde T_b$ contribute $0$; at least one block has $S_b\ne\tilde T_b$ (because $S=\bigcup_bS_b$ and $\tilde S_0=\bigcup_b\tilde T_b$ with disjoint blocks), and each such block contributes a term $\to-\infty$ by Step 1. Hence $\pi_0(S)/\pi_0(\tilde S_0)\to0$ in probability for each of the finitely many $S\ne\tilde S_0$, and
$$
\pi_0(\tilde S_0)=\Big[1+\sum_{S\ne\tilde S_0}\frac{\pi_0(S)}{\pi_0(\tilde S_0)}\Big]^{-1}\to1 .
$$

**Step 3 (T3(i), the posterior; uses only (S)).** Let $S\ne S_0$. By (1.3), $\log\{\pi(S)/\pi(S_0)\}=\log\{p(S)/p(S_0)\}+\log\mathrm{BF}(S)-\log\mathrm{BF}(S_0)$, the prior term being $O(1)$.
If $S\supsetneq S_0$: Lemma 4(b) with $T=S$, $T'=S_0$, $U=S$. By (1.6), $\bar\sigma^2_n(S)=\bar\sigma_n^2(S_0)=\sigma_\star^2$ exactly, so $a=0$, $a_n(S,U)=0$, $a_n(S_0,S)=0$; thus $\log\mathrm{BF}(S)-\log\mathrm{BF}(S_0)=-\frac{|S|-|S_0|}{2}\log n+O_{\mathbb P}(1)\to-\infty$.
If $S\not\supseteq S_0$: by (1.6), $\bar\sigma^2(S)>\sigma_\star^2=\bar\sigma^2(S_0)$, and Lemma 4(a) gives $\frac1n[\log\mathrm{BF}(S)-\log\mathrm{BF}(S_0)]\to-\frac12\log\{\bar\sigma^2(S)/\sigma_\star^2\}<0$, so $\log\mathrm{BF}(S)-\log\mathrm{BF}(S_0)\to-\infty$.
Conclude exactly as in Step 2: $\pi(S_0)\to1$.

**Step 4 (T3(ii); uses only (S)).** By (1.3),
$$
\Delta_0(n)=\log\frac{p(\tilde S_0)}{p(S_0)}+\sum_b\big[\log\mathrm{BF}(\tilde T_b)-\log\mathrm{BF}(S_0\cap C_b)\big]. \tag{4.3}
$$
The prior term is $O(1)$. Fix $b$ and write $T_b^0:=S_0\cap C_b$. Lemma 4(a) with $T=\tilde T_b$, $T'=T_b^0$ (it needs no gap condition) gives $\frac1n[\log\mathrm{BF}(\tilde T_b)-\log\mathrm{BF}(T_b^0)]\to-\frac12\log\frac{\bar\sigma^2(\tilde T_b)}{\bar\sigma^2(T^0_b)}=\frac12\log\frac{\bar\sigma^2_b(T^0_b)}{\bar\sigma^2_b(\tilde T_b)}$, whether or not the two variances coincide (when they do, the limit is $0$).
Summing over $b$: $\Delta_0(n)/n\to\kappa_0$. Each term of $\kappa_0$ is $\ge0$ because $\tilde T_b$ minimises $\bar\sigma^2$ over $2^{C_b}$, and finite because all values lie in $[\sigma_\star^2,\infty)$; so $\kappa_0\in[0,\infty)$.

**Step 5 (T3(iii)).** If $\kappa_0=0$, every term vanishes, so $\bar\sigma^2(T_b^0)=\bar\sigma^2(\tilde T_b)$ for all $b$; by (1.5), $T^0_b\supseteq\tilde T_b$ for all $b$, i.e. $S_0\supseteq\tilde S_0$ block by block. If moreover $\tilde S_0\ne S_0$, then $S_0\supsetneq\tilde S_0$ and $|S_0|>|\tilde S_0|$. In (4.3) every block with $T^0_b=\tilde T_b$ contributes $0$ and every block with $T^0_b\supsetneq\tilde T_b$ contributes $\frac{|T^0_b|-|\tilde T_b|}{2}\log n+O_{\mathbb P}(1)$ by (4.1); the prior term is $O(1)$. Since the blocks are disjoint, $\sum_b|T^0_b|=|S_0|$ and $\sum_b|\tilde T_b|=|\tilde S_0|$, whence $\Delta_0(n)=\frac{|S_0|-|\tilde S_0|}{2}\log n+O_{\mathbb P}(1)$. (By (3.1) and Remark 3.1 the $O_{\mathbb P}(1)$ is $+\sum_{b:T^0_b\ne\tilde T_b}\frac{a_b+\xi_b+\eta_b}{2\bar\sigma^2(\tilde T_b)}+\log\frac{p(\tilde S_0)}{p(S_0)}+o_{\mathbb P}(1)$, where $(a_b,\xi_b,\eta_b)$ is the triple of Lemma 3 for $(T,T')=(T^0_b,\tilde T_b)$; the sign is $+$ because (4.3) contains $\log\mathrm{BF}(\tilde T_b)-\log\mathrm{BF}(T^0_b)$, the negative of (3.1). It is non-degenerate.)

**Step 6 (T3(iv); uses only (S)).** By (1.3), $\log\{\pi(S_0)/\pi(\tilde S_0)\}=\log\{p(S_0)/p(\tilde S_0)\}+\log\mathrm{BF}(S_0)-\log\mathrm{BF}(\tilde S_0)$, with prior term $O(1)$.
*Case $\tilde S_0\not\supseteq S_0$.* By (1.6), $\bar\sigma^2(\tilde S_0)>\sigma_\star^2=\bar\sigma^2(S_0)$. Lemma 4(a) with $T=S_0$, $T'=\tilde S_0$: $\frac1n[\log\mathrm{BF}(S_0)-\log\mathrm{BF}(\tilde S_0)]\to-\frac12\log\frac{\sigma_\star^2}{\bar\sigma^2(\tilde S_0)}=\kappa_1>0$, and the prior term is $O(1/n)$ after division by $n$.
*Case $\tilde S_0\supsetneq S_0$.* Lemma 4(b) with $T=\tilde S_0$, $T'=S_0$, $U=\tilde S_0$: by (1.6), $a=0$ and $a_n(S_0,\tilde S_0)=0$ exactly, so $\log\mathrm{BF}(\tilde S_0)-\log\mathrm{BF}(S_0)=-\frac{|\tilde S_0|-|S_0|}{2}\log n+O_{\mathbb P}(1)$, i.e. $\log\{\pi(S_0)/\pi(\tilde S_0)\}=\frac{|\tilde S_0|-|S_0|}{2}\log n+O_{\mathbb P}(1)$ (the prior term is absorbed).

**The closing sentence of T3.** If $\tilde S_0\ne S_0$, (i) says the start and the posterior concentrate on different models. If $\kappa_0>0$, (i)–(ii) give $\pi_0(S_0)=\pi_0(\tilde S_0)e^{-\Delta_0(n)}=\exp\{-\kappa_0n(1+o_{\mathbb P}(1))\}$. (The draft writes $o(1)$; the exponent is random, so $o_{\mathbb P}(1)$ is the correct reading.) $\blacksquare$

*Which hypotheses were used where.* (R1) in (4.1) and, for the union set $U$, in (4.2); hence in T3(i) (start) and (iii). (R2) in (4.2), hence in T3(i) (start) only. T3(i) for the posterior, T3(ii) and T3(iv) use only (S). (U) was used only through (1.5), which under (S) holds without assuming (U).

---

## 5. Proof of Claim (R-suff): $\|\Gamma_n-\Gamma\|=O(n^{-1/2})$ implies (R)

Assume (S) and $\|\Gamma_n-\Gamma\|\le K_1n^{-1/2}$ for all $n$ (spectral norm; any norm gives the same statement up to the constant). By (1.5), (U) holds with $\tilde T_b=\operatorname{supp}(\gamma_b)$, and the population minimisers of block $b$ are exactly the sets $T$ with $\tilde T_b\subseteq T\subseteq C_b$. Fix $b$ and $T\subseteq C_b$, $T\ne\tilde T_b$, and let $n\ge n_1:=\lceil(2K_1/\lambda)^2\rceil$, so that $\|\Gamma_n-\Gamma\|\le\lambda/2$.

*Case $T\supsetneq\tilde T_b$.* By Lemma 1(e) with $C=C_b$, $\tilde T=\tilde T_b$ and $A'=\Gamma_n$,
$$
-K'K_1^2\ \le\ -K'n\|\Gamma_n-\Gamma\|^2\ \le\ n\big[\bar\sigma_n^2(T)-\bar\sigma_n^2(\tilde T_b)\big]=-n\big[R_{\Gamma_n}(\tilde T_b)-R_{\Gamma_n}(T)\big]\ \le\ 0 ,
$$
which is (R1). (These are all the sets covered by (R1): a population minimiser $\ne\tilde T_b$ is a strict superset of $\tilde T_b$.)

*Case $T\not\supseteq\tilde T_b$.* $T$ is not a population minimiser, so $g(T):=\bar\sigma^2(T)-\bar\sigma^2(\tilde T_b)>0$. Let $g_{\min}:=\min\{g(T):\ b\in[L],\ T\subseteq C_b,\ T\not\supseteq\tilde T_b\}>0$ (a minimum over finitely many positive numbers; the index set is nonempty in this case, since it contains $T$. If no block has such a $T$, for instance when $\beta^\star=0$ and every $\tilde T_b=\emptyset$, then (R2) is vacuous and there is nothing to prove; audit 2026-10-15). By (1.4) applied to $T$ and to $\tilde T_b$,
$$
\Big|\,n\big[\bar\sigma_n^2(T)-\bar\sigma_n^2(\tilde T_b)\big]-n\big[\bar\sigma^2(T)-\bar\sigma^2(\tilde T_b)\big]\Big|\le 2nK\|\Gamma_n-\Gamma\|\le 2KK_1\sqrt n , \tag{5.1}
$$
so $n[\bar\sigma_n^2(T)-\bar\sigma_n^2(\tilde T_b)]\ge ng_{\min}-2KK_1\sqrt n\ge\omega_n\log n$ with $\omega_n:=(ng_{\min}-2KK_1\sqrt n)/\log n\to\infty$ (for $n$ large enough that $\omega_n>0$). This is (R2). $\blacksquare$

*Remark 5.1 (what the rate does, and sharpness).* (R2) needs only $\Gamma_n\to\Gamma$: by (1.4), $n[\bar\sigma^2_n(T)-\bar\sigma^2_n(\tilde T_b)]=ng(T)+o(n)$. (R1) is where the rate enters, and it enters *squared*: for $T\supsetneq\tilde T_b$ the gap $n[\bar\sigma_n^2(\tilde T_b)-\bar\sigma_n^2(T)]=\|(P_T-P_{\tilde T_b})\mu\|^2$ is the squared length of a component that vanishes in the limit, hence $O(n\|\Gamma_n-\Gamma\|^2)$ by Lemma 1(e). So $\|\Gamma_n-\Gamma\|=O(n^{-1/2})$ suffices, and the draft's $O(1/n)$ is stronger than needed. The exponent $1/2$ is sharp: in the draft's example $\Gamma_{13,n}=n^{-1/4}$ (column $3$ in a block of its own, irrelevant in the limit, $\mu=\beta x_1$) the superset gap is $\|P_{\{3\}}\mu\|^2=n\beta^2\Gamma_{13,n}^2=\beta^2\sqrt n\gg\log n$, (R1) fails, and so does the start-concentration half of T3(i) (the start includes column $3$, so $\pi_0(\tilde S_0)\to0$ with $\tilde S_0=S_0=\{1\}$; T3(iii) is not at issue there since its antecedent $\tilde S_0\ne S_0$ fails). More generally, for every $0<\alpha<1/2$ there are designs in (S) with $\|\Gamma_n-\Gamma\|=n^{-\alpha}$ and superset gaps $n^{1-2\alpha}\gg\log n$: take $p=2$, singleton blocks, $\beta^\star=\beta e_1$, $\Gamma_n=\begin{pmatrix}1&n^{-\alpha}\\ n^{-\alpha}&1\end{pmatrix}$ and $X_n=\sqrt n\,Q_n\Gamma_n^{1/2}$ with $Q_n^\top Q_n=I_2$ (standardised, $\Gamma_n\to I_2$); then $\tilde T_2=\emptyset$ and $n[\bar\sigma_n^2(\emptyset)-\bar\sigma^2_n(\{2\})]=n\beta^2\Gamma_{12,n}^2=\beta^2n^{1-2\alpha}$. (audit 2026-10-15: $\alpha>0$ is needed for $\Gamma_n\to I_2\succ0$. At $\alpha=0$, $\Gamma_n$ is singular, and for $\alpha<0$ it is not positive semidefinite.) (The revision record of the draft preferred $O(1/n)$ over a reviewer's $O(n^{-1/2})$ on the grounds that $n\cdot O(n^{-1/2})=O(\sqrt n)$ would break the $\log n$ statements; that reasoning overlooks the quadratic structure and should be corrected in the paper.)

---

## 6. Proof of Theorem T11(i)–(iii)

Assume (S). ($\Gamma_{C_bC_b}\succ0$ for every $b$ is implied by $\Gamma\succ0$.)

**(i)** is (1.5): Lemma 1(b) with $A=\Gamma$, $C=C_b$ identifies the population minimisers of block $b$ as the supersets of $\operatorname{supp}(\gamma_b)$ within $C_b$; thus (U) holds with $\tilde T_b=\operatorname{supp}(\gamma_b)$ and $\tilde S_0=\bigcup_b\operatorname{supp}(\gamma_b)$.

**(ii)** Since the blocks are disjoint, $j\in\tilde S_0$ iff $j\in\tilde T_{b(j)}$ iff $\gamma_{b(j),j}\ne0$ by (i). Hence $S_0\setminus\tilde S_0=\{j\in S_0:\gamma_{b(j),j}=0\}$ and $\tilde S_0\setminus S_0=\{j\notin S_0:\gamma_{b(j),j}\ne0\}$.

**(iii)** If no true variable is cancelled, (ii) gives $S_0\setminus\tilde S_0=\emptyset$, i.e. $\tilde S_0\supseteq S_0$. Under (R), T3(i) gives $\pi_0(\tilde S_0)\to1$, and since $\tilde S_0\in\{S:S\supseteq S_0\}$, $\pi_0(\{S:S\supseteq S_0\})\ge\pi_0(\tilde S_0)\to1$ in probability. The passage from $\tilde S_0$ to $S_0$ removes $\tilde S_0\setminus S_0$ and adds nothing: deletions only. If $\tilde S_0\ne S_0$ then $\tilde S_0\supsetneq S_0$ and the second case of T3(iv) (which needs only (S)) gives $\log\{\pi(S_0)/\pi(\tilde S_0)\}=\frac{|\tilde S_0|-|S_0|}{2}\log n+O_{\mathbb P}(1)$. That $\Delta_0(n)$ can nevertheless be linear in $n$ is shown by Example Ex1, verified in Remark 6.1 (this uses T3(ii), which needs only (S), so no check of (R) is required for the example). Finally, if $\Gamma_{C_b,C_b^c}\beta^\star_{C_b^c}=0$ for every $b$, the alternative formula of Lemma 1(b) gives $\gamma_b=\beta^\star_{C_b}$, so $\operatorname{supp}(\gamma_b)=S_0\cap C_b$ and $\tilde S_0=\bigcup_b(S_0\cap C_b)=S_0$. $\blacksquare$

*Remark 6.0 (what "deletions only" means; audit 2026-10-15, Sol's audit of T11, finding 1).* (iii) is a statement about the two endpoint models: the net change from $\tilde S_0$ to $S_0$ removes variables and adds none. It says nothing about the modes of the intermediate bridge $q_\phi$, and it does not say that a single move crosses the switch, since several deletions may be needed. An intermediate mode can even add a variable outside $\tilde S_0$, under (S), (R) and no cancellation. Let $u,v,w,z$ be orthonormal in $\mathbb R^4$ and take the limiting standardised column directions $x_1/\sqrt n=(u+z)/\sqrt2$, $x_2/\sqrt n=(3u+w)/\sqrt{10}$, $x_3/\sqrt n=(u+3v)/\sqrt{10}$, $x_4/\sqrt n=(u-3v)/\sqrt{10}$, with $\Gamma_n=\Gamma\succ0$ constant (so (R) holds), blocks $\{1\}$ and $\{2,3,4\}$, $\beta^\star=e_1$ and $\sigma_\star^2=1$. Then $\gamma_{\{2,3,4\}}=(0,\tfrac{\sqrt5}2,\tfrac{\sqrt5}2)$, there is no cancelled true variable, and $\tilde S_0=\{1,3,4\}$. The best block residual variances by size $0,1,2,3$ are $2,\tfrac{31}{20},\tfrac32,\tfrac32$, attained by $\emptyset,\{2\},\{3,4\},\{2,3,4\}$. Along $\phi_n(\tau)=1-\tau\log n/n$, the log-score of $\{1\}\cup T$ relative to $\{1\}$, divided by $\log n$, tends to $h_\tau(T)=\frac\tau2\log\frac2{\bar\sigma^2(T)}-\frac{|T|}2$, while models without variable $1$ lose at order $n$. The maximiser is $\{3,4\}$ at $\tau=100$ and $\{2\}$ at $\tau=10$, strictly. Indeed $\log\{\gamma_{\phi_n(\tau)}(\{1\}\cup T)/\gamma_{\phi_n(\tau)}(\{1\})\}=h_\tau(T)\log n+o_{\mathbb P}(\log n)$. The start term contributes $(\tau\log n/n)\cdot\{\tfrac n2\log(\bar\sigma^2(\emptyset)/\bar\sigma^2(T))+O_{\mathbb P}(\sqrt n)+O(\log n)\}$, and the posterior term $-\tfrac{|T|}2\log n+O_{\mathbb P}(1)$ (nested supersets of $S_0$). There are finitely many models and the maximisers are strict, so at $\phi_n(100)$ and $\phi_n(10)$ the bridge concentrates on $\{1,3,4\}$ and $\{1,2\}$ respectively, whereas $q_1$ concentrates on $\{1\}$ (T3(i)). An intermediate mode thus contains variable $2$, which is absent from both endpoint models; further intervening modes are not excluded. (Numbers checked in `proofs/_audit/group_B/check_audit_B.py`, checks T11.F1; wording and argument per Sol's confirmation, audit 2026-10-15.)

*Remark 6.1 (Example Ex1 checked).* Setup: $1\in C_1$, $3\in C_2$, $\Gamma_{13}=r$ with $0<|r|<1$, columns $1$ and $3$ exactly uncorrelated with all other columns at every $n$ (hence also in the limit; with $\Gamma\succ0$ assumed as in (S)), $\beta^\star=\beta e_1$, $\beta\ne0$. Then $\mu=\beta x_1$ and $S_0=\{1\}$. Since $\Gamma_{C_1C_1}e_1=e_1$ (column $1$ has unit norm and is orthogonal to the rest of $C_1$), $\gamma_1=\beta\,\Gamma_{C_1C_1}^{-1}\Gamma_{C_1,1}=\beta\,\Gamma_{C_1C_1}^{-1}e_1=\beta e_1$, so $\tilde T_1=\{1\}$. Likewise $\Gamma_{C_2,1}=re_3$ and $\Gamma_{C_2C_2}e_3=e_3$, so $\gamma_2=\beta r\,e_3$ and $\tilde T_2=\{3\}$; every other block has $\Gamma_{C_b,1}=0$, $\gamma_b=0$, $\tilde T_b=\emptyset$. Thus $\tilde S_0=\{1,3\}\supsetneq S_0$: no cancellation, one proxy. By Lemma 1(a), $\bar\sigma^2_2(\emptyset)=\sigma_\star^2+\beta^2$ and $\bar\sigma^2_2(\{3\})=\sigma_\star^2+\beta^2(1-r^2)$ (distance of $\beta v_1$ from the line spanned by $v_3$, with $\langle v_1,v_3\rangle=r$), so $\kappa_0=\frac12\log\frac{\sigma_\star^2+\beta^2}{\sigma_\star^2+\beta^2(1-r^2)}>0$ (blocks $b\ne2$ contribute $\log1=0$ since $S_0\cap C_b=\tilde T_b$), while T3(iv) gives $\log\{\pi(S_0)/\pi(\tilde S_0)\}=\frac12\log n+O_{\mathbb P}(1)$.

---

## 7. Theorem T11(iv): a counterexample with the operational cap, and the true variant

**Setting (H) (the hypotheses listed in T11(iv)).** A triangular array indexed by $n$: $p=p_n\le n^A$, a partition of $[p_n]$ into blocks with $|C_b|\le B$, a design $X_n$ with $\|x_j\|^2=n$, $\beta^\star=\beta^\star_n$ with $|S_0|=s_0$, $\mu=X_n\beta^\star$, $\|\mu\|^2/n\le M$, $\lambda_{\min}(\Gamma_{n,C_bC_b})\ge\varphi_0^2$ for every $b$, $\varepsilon\sim N_n(0,\sigma_\star^2I)$, and $\gamma_{b,n}:=G_{C_bC_b}^{-1}X_{C_b}^\top\mu$; the constants $A,B,s_0,M,\varphi_0,\sigma_\star^2,a_0,b_0$ are fixed. The margin is
$$
\min_{j\in S_0}\gamma_{b(j),n,j}^2\ \ge\ M_n\,\frac{(\sigma_\star^2+M)\log n}{n\varphi_0^2},\qquad M_n\to\infty \tag{7.0}
$$
(vacuous if $S_0=\emptyset$, in which case the conclusion $\pi_0(\{S\supseteq S_0\})=1$ is trivial). The statement under examination: under (H), $\pi_0(\{S:S\supseteq S_0\})\to1$ in probability. The draft's default prior is $\mathrm{BB}(1,p)$ with cap $k_{\max}=\lfloor n/2\rfloor$; (iv) does not say which cap, so we examine the default. Note that (H) is not (S): (S) is the special case with everything fixed, in which the operational cap is eventually inactive.

### 7.1 Counterexample under the cap $k_{\max}=\lfloor n/2\rfloor$

**Construction.** Let $n\ge8$, $p=n$ (so $A=1$), singleton blocks $C_j=\{j\}$ ($B=1$), any size-only prior (in particular $\mathrm{BB}(1,p)$) with cap $k_{\max}=\lfloor n/2\rfloor$. With $e_1,\dots,e_n$ the standard basis of $\mathbb R^n$ put
$$
x_1=\sqrt n\,e_1,\qquad x_2=\sqrt n\big(-\tfrac12e_1+\tfrac{\sqrt3}{2}e_2\big),\qquad x_j=\tfrac12x_2+\tfrac{\sqrt3}{2}\sqrt n\,e_j\quad(3\le j\le n).
$$
Then $\|x_j\|^2=n$ for all $j$ ($x_2\perp e_j$ for $j\ge3$), $\Gamma_{n,12}=-\tfrac12$, $\Gamma_{n,1j}=-\tfrac14$, $\Gamma_{n,2j}=\tfrac12$ and $\Gamma_{n,jk}=\tfrac14$ for $3\le j\ne k\le n$. Singleton blocks give $\lambda_{\min}(\Gamma_{n,C_bC_b})=1=:\varphi_0^2$. The coefficient vector is **fixed**:
$$
\beta^\star=(1,\ \tfrac32,\ 0,\dots,0),\qquad S_0=\{1,2\},\ s_0=2,\qquad \mu=x_1+\tfrac32x_2 .
$$
*Hypotheses.* $\|\mu\|^2/n=1+2\cdot\tfrac32\Gamma_{n,12}+\tfrac94=\tfrac74\le3=:M$. For singleton blocks $\gamma_{j,n,j}=x_j^\top\mu/n=\Gamma_{n,j1}+\tfrac32\Gamma_{n,j2}$, so
$$
\gamma_{1,n,1}=1-\tfrac34=\tfrac14,\qquad \gamma_{2,n,2}=-\tfrac12+\tfrac32=1,\qquad \gamma_{j,n,j}=-\tfrac14+\tfrac34=\tfrac12\ \ (j\ge3).
$$
Thus $\min_{j\in S_0}\gamma_{b(j),n,j}^2=\tfrac1{16}$, and (7.0) holds with $M_n:=n/(16(\sigma_\star^2+M)\log n)\to\infty$. All other hypotheses hold as listed: $p=n\le n^A$ with $A=1$, $B=1$, $s_0=2$ fixed, $\|\mu\|^2/n\le M$, $\varphi_0=1$. Only the design and $p$ vary with $n$, as the hypothesis $p\le n^A$ requires.

**Claim.** $\pi_0(\{S:1\in S\})\to0$ in probability; hence $\pi_0(\{S:S\supseteq S_0\})\le\pi_0(\{S:1\in S\})\to0$, and the statement fails.

*Proof.* Write $\mathrm{BF}_j:=\mathrm{BF}(\{j\})$; for singleton blocks $r(S)=\prod_{j\in S}\mathrm{BF}_j$.

(a) *A good event.* Each $x_j^\top\varepsilon/n\sim N(0,\sigma_\star^2/n)$, and $\mathbb P(|N(0,1)|>t)\le e^{-t^2/2}$ for $t\ge1$ (Mills' ratio: $\mathbb P(|Z|>t)\le\frac{2}{t\sqrt{2\pi}}e^{-t^2/2}$), so with $t=\sqrt{4\log n}$, $\mathbb P(|N(0,1)|>\sqrt{4\log n})\le n^{-2}$ and with $\rho_n:=\sigma_\star\sqrt{4\log n/n}\to0$, $\mathbb P\big(\max_{j\le n}|x_j^\top\varepsilon|/n>\rho_n\big)\le n^{-1}$. Let $E_n$ be the event that this maximum is $\le\rho_n$ and that $\|\varepsilon\|^2\le\tfrac32n\sigma_\star^2$. By the above and the law of large numbers for $\chi^2_n$, $\mathbb P(E_n)\to1$. On $E_n$, for $n$ large:

(b) *Fitted norms.* $\|P_jy\|^2=(x_j^\top y)^2/n=n\big(\gamma_{j,n,j}+x_j^\top\varepsilon/n\big)^2$. For $j\ge3$: $\|P_jy\|^2\ge n(\tfrac12-\rho_n)^2$. For $j=1$: $\|P_1y\|^2\le n(\tfrac14+\rho_n)^2$.

(c) *The null quantity.* $\tilde Q_\emptyset=2b_0+\|y\|^2\le2b_0+2\|\mu\|^2+2\|\varepsilon\|^2\le(\tfrac72+3\sigma_\star^2+1)n=:c_+n$ for $n\ge2b_0$.

(d) *Every proxy beats the weak true variable by a factor $e^{c_2n}$.* Fix $j\ge3$. Both $\{1\}$ and $\{j\}$ have $G=n$, so $D_1=D_j$ and (1.2) gives $\log\mathrm{BF}_1-\log\mathrm{BF}_j=-\nu\log(\tilde Q_1/\tilde Q_j)=\nu\log\big(1-(\tilde Q_1-\tilde Q_j)/\tilde Q_1\big)\le-\nu(\tilde Q_1-\tilde Q_j)/\tilde Q_1$ (using $\log(1-u)\le-u$ for $u<1$; here $u<1$ because $\tilde Q_j>0$). Now $\tilde Q_1-\tilde Q_j=t_j-t_1$, and by Lemma 2(b) with $g_{\{j\}}=n$, $t_j\ge\big(1-\tfrac{1+1/n}{n+1}\big)\|P_jy\|^2=(1-\tfrac1n)\|P_jy\|^2$, while $t_1\le\|P_1y\|^2$. Hence, on $E_n$,
$$
\tilde Q_1-\tilde Q_j\ \ge\ n\Big[(1-\tfrac1n)(\tfrac12-\rho_n)^2-(\tfrac14+\rho_n)^2\Big]\ \ge\ \tfrac{3}{32}n\qquad(n\text{ large, since }\tfrac14-\tfrac1{16}=\tfrac3{16}),
$$
and $0<\tilde Q_1\le\tilde Q_\emptyset\le c_+n$. Therefore $\log\mathrm{BF}_1-\log\mathrm{BF}_j\le-\tfrac n2\cdot\tfrac{3n/32}{c_+n}=-c_2n$ with $c_2:=3/(64c_+)$, simultaneously for all $j\ge3$.

(e) *Swapping the true variable for a proxy.* For a model $S$ with $1\in S$ and $|S|\le k_{\max}$, let $j(S):=\min\{j\ge3:j\notin S\}$; it exists because $|S\cap\{3,\dots,n\}|\le k_{\max}-1<n-2$. Put $S':=(S\setminus\{1\})\cup\{j(S)\}$. Then $|S'|=|S|\le k_{\max}$, so $p(S')=p(S)$ (size-only prior), and $\pi_0(S)/\pi_0(S')=\mathrm{BF}_1/\mathrm{BF}_{j(S)}\le e^{-c_2n}$ on $E_n$. The map $S\mapsto S'$ is at most $n$-to-one ($S$ is recovered from $S'$ by choosing which of its at most $n$ elements to replace by $1$). Therefore, on $E_n$,
$$
\pi_0(\{S:1\in S\})=\sum_{S\ni1}\pi_0(S)\le e^{-c_2n}\sum_{S\ni1}\pi_0(S')\le n\,e^{-c_2n}\to0 ,
$$
because $\sum_{S\ni1}\pi_0(S')\le n\sum_{S'}\pi_0(S')=n$. Since $\mathbb P(E_n)\to1$, the claim follows. $\blacksquare$

*Diagnosis.* The hypotheses of (iv) bound neither the number of proxies (variables outside $S_0$ with a non-zero block projection) nor their strength. When the proxies outnumber the cap and each beats a true variable within its own block, the swap argument excludes that true variable whatever the size-only prior; under the default $\mathrm{BB}(1,p)$ prior the start moreover fills its cap with proxies (adding a proxy multiplies the start weight by at least $e^{c_2n}/(2p)$, by Step 4 of §7.2 and (d)), though this saturation is not needed for the refutation and can fail for priors with exponentially decaying size weights. The margin (7.0) only guarantees that a true variable beats *the empty model within its own block*; under a binding cap it must also beat the competitors for a slot, which (7.0) does not control. Without a cap the two requirements coincide, which is why the variant below holds. The counterexample does not depend on $w$ or on the hyperparameters; $p=n$ is used only to have more proxies than $k_{\max}$, and the same argument works for any $p\le n^A$ with $p\ge k_{\max}+2$ (so that a model of size $\le k_{\max}$ containing $1$ always leaves a proxy unused) after replacing $\sqrt{4\log n}$ in (a) by $\sqrt{2(A+1)\log n}$ (the union bound over $p$ columns is then $\le n^{-1}$) and noting that the swap map is at most $k_{\max}$-to-one. In the fixed-$p$ setting of T3 (where $k_{\max}=\lfloor n/2\rfloor\ge p$ eventually) the cap is inactive and (iv) is true by Proposition 6; the failure is specific to $p$ growing past the cap, which the hypothesis $p\le n^A$ permits.

### 7.2 The true variant

**Proposition 6 (T11(iv$'$): start screening without a binding cap).** Assume (H) with the prior $\mathrm{BB}(1,p)$ and an arbitrary cap $k_{\max}$, and the margin (7.0). Then, with $F_{b(j)}:=\operatorname{supp}(\gamma_{b(j),n})$,
$$
\max_{j\in S_0}\ \pi_0\big(\{S:\ j\notin S,\ |S\cup F_{b(j)}|\le k_{\max}\}\big)\to0\quad\text{in probability}
$$
(a maximum over the $s_0$ indices of $S_0=S_0(n)$, which may vary with $n$).
Consequently $\pi_0(\{S:S\not\supseteq S_0\})\le o_{\mathbb P}(1)+\pi_0(\{S:|S|>k_{\max}-B\})$, and if $k_{\max}\ge p$ (no cap) then $\pi_0(\{S:S\supseteq S_0\})\to1$ in probability.

*Proof.* Fix $j\in S_0$ and write $b=b(j)$, $F=F_b\subseteq C_b$. Note $j\in F$ because $\gamma_{b,n,j}^2>0$ by (7.0).

*Step 1 (block gain).* Let $T\subseteq C_b$ with $j\notin T$ and $T':=T\cup F$. Since $P_{C_b}\mu=X_{C_b}\gamma_{b,n}=X_{T'}(\gamma_{b,n})_{T'}\in\operatorname{col}(X_{T'})\subseteq\operatorname{col}(X_{C_b})$ and $\mu-P_{C_b}\mu\perp\operatorname{col}(X_{C_b})\supseteq\operatorname{col}(X_{T'})$, we get $P_{T'}\mu=P_{T'}P_{C_b}\mu=P_{C_b}\mu$; likewise $P_T\mu=P_TP_{C_b}\mu$ is the nearest point of $\operatorname{col}(X_T)$ to $P_{C_b}\mu$. Hence
$$
a_n(T,T')=\|(P_{T'}-P_T)\mu\|^2=\min_{c\in\mathbb R^T}\|X_{C_b}\gamma_{b,n}-X_Tc\|^2\ \ge\ \lambda_{\min}(G_{C_bC_b})\min_{c\in\mathbb R^T}\|\gamma_{b,n}-\iota(c)\|^2\ \ge\ n\varphi_0^2\gamma_{b,n,j}^2\ \ge\ m_n:=M_n(\sigma_\star^2+M)\log n,
$$
where $\iota(c)\in\mathbb R^{C_b}$ extends $c$ by zero; the $j$-th coordinate of $\gamma_{b,n}-\iota(c)$ is $\gamma_{b,n,j}$ because $j\notin T$.

*Step 2 (a good event).* The pairs $(T,T')$ that arise, over $j\in S_0$ and $T\subseteq C_{b(j)}$ with $j\notin T$, number at most $s_02^B$. Let $E_n$ be the event that $\|\varepsilon\|^2\le2n\sigma_\star^2$ and that $|\xi_{T,T'}|\le a_n(T,T')/2$ for every such pair, where $\xi_{T,T'}=2\mu^\top(P_{T'}-P_T)\varepsilon\sim N(0,4\sigma_\star^2a_n(T,T'))$ (Lemma 3, nested case). Since $\mathbb P(|N(0,4\sigma_\star^2a)|>a/2)\le2e^{-a/(32\sigma_\star^2)}$ and $a_n(T,T')\ge m_n\to\infty$, $\mathbb P(E_n)\to1$.

*Step 3 (Bayes factor ratio).* On $E_n$ and for $n$ large: $\tilde Q_\emptyset=2b_0+\|y\|^2\le2b_0+2Mn+4n\sigma_\star^2\le c_+n$ with $c_+:=2M+4\sigma_\star^2+1$; for every nonempty $T''\subseteq C_b$, $g_{T''}\ge\lambda_{\min}(G_{C_bC_b})\ge n\varphi_0^2$ (interlacing), so Lemma 2(b) gives $d_{T''}\le(1+\tfrac1{n\varphi_0^2})\|y\|^2/(n+1)\le2c_+$, and $d_\emptyset=0$; and $0<\tilde Q_{T''}\le\tilde Q_\emptyset\le c_+n$ because $t_{T''}\ge0$. (Throughout this step the case $T=\emptyset$ is allowed; there $D_\emptyset=1$, $d_\emptyset=0$, and every term of the form $|T|/g_T$ is read as $0$.) By Lemma 3 (nested case, $T\subseteq T'$), $\tilde Q_T-\tilde Q_{T'}=a_n(T,T')+\xi_{T,T'}+\varepsilon^\top(P_{T'}-P_T)\varepsilon+d_T-d_{T'}\ge a_n(T,T')/2-2c_+\ge m_n/4$. With $x:=(\tilde Q_T-\tilde Q_{T'})/\tilde Q_{T'}>0$ and $\log(1+x)\ge x/(1+x)$,
$$
-\nu\log\frac{\tilde Q_{T'}}{\tilde Q_T}=\nu\log(1+x)\ \ge\ \nu\,\frac{\tilde Q_T-\tilde Q_{T'}}{\tilde Q_T}\ \ge\ \frac n2\cdot\frac{m_n/4}{c_+n}=\frac{m_n}{8c_+}.
$$
By Lemma 2(a), $-\tfrac12\log(D_{T'}/D_T)\ge-\tfrac{|T'|-|T|}{2}\log(n+1)-\tfrac{|T|}{2g_T}\ge-\tfrac B2\log(n+1)-1$. So by (1.2),
$$
\log\mathrm{BF}(T')-\log\mathrm{BF}(T)\ \ge\ -\tfrac B2\log(n+1)-1+\frac{m_n}{8c_+}. \tag{7.1}
$$

*Step 4 (prior ratio).* For $\mathrm{BB}(1,p)$, $w(k)=B(1+k,2p-k)/B(1,p)$, so $w(k+1)/w(k)=\dfrac{\Gamma(k+2)\Gamma(2p-k-1)}{\Gamma(k+1)\Gamma(2p-k)}=\dfrac{k+1}{2p-k-1}\ge\dfrac1{2p}$ for $0\le k\le p-1$. Hence for $S\subseteq S'$ with $|S'|-|S|\le B$ and $|S'|\le k_{\max}$: $p(S')/p(S)=w(|S'|)/w(|S|)\ge(2p)^{-B}\ge(2n^A)^{-B}$.

*Step 5 (mapping).* Let $\mathcal S_j:=\{S:\ j\notin S,\ |S\cup F|\le k_{\max}\}$, and for $S\in\mathcal S_j$ put $S':=S\cup F$. Then $|S'|\le k_{\max}$, $|S'|-|S|\le|F|\le B$, $S'_b=S_b\cup F$ and $S'_{b'}=S_{b'}$ for $b'\ne b$. By (1.3), Step 4 and (7.1) (applied with $T=S_b$, which satisfies $j\notin T$), on $E_n$,
$$
\log\frac{\pi_0(S')}{\pi_0(S)}=\log\frac{p(S')}{p(S)}+\log\mathrm{BF}(S_b\cup F)-\log\mathrm{BF}(S_b)\ \ge\ -B\log(2n^A)-\tfrac B2\log(n+1)-1+\frac{m_n}{8c_+}=:L_n ,
$$
and $L_n\to\infty$ because $m_n/\log n=M_n(\sigma_\star^2+M)\to\infty$. The map $S\mapsto S'$ on $\mathcal S_j$ is at most $2^B$-to-one ($S'$ determines $S$ outside $C_b$, and $S_b\subseteq S'_b\subseteq C_b$ leaves at most $2^{B}$ possibilities). Hence on $E_n$, $\pi_0(\mathcal S_j)\le e^{-L_n}\sum_{S\in\mathcal S_j}\pi_0(S')\le2^Be^{-L_n}\to0$.

*Step 6.* $\{S\not\supseteq S_0\}\subseteq\bigcup_{j\in S_0}\{j\notin S\}\subseteq\bigcup_{j\in S_0}\mathcal S_j\cup\{|S|>k_{\max}-B\}$ (if $|S|\le k_{\max}-B$ then $|S\cup F_{b(j)}|\le k_{\max}$). Summing over the $s_0$ indices gives the displayed bound. If $k_{\max}\ge p$, then $|S\cup F|\le p\le k_{\max}$ for every $S$, so $\mathcal S_j=\{j\notin S\}$ and $\pi_0(\{S\not\supseteq S_0\})\le s_02^Be^{-L_n}\to0$ on $E_n$. $\blacksquare$

*Remarks.* (1) No union bound over $p$ is needed: only the $s_02^B$ block-level comparisons enter, and $p$ appears only through the prior cost $B\log(2p)\le B\log2+AB\log n$, which the margin $M_n\log n$ dominates. (2) For a general size-only prior the proof goes through verbatim if $w(k+1)/w(k)\ge p^{-C_0}$ for $0\le k<p$ (replace $-B\log(2n^A)$ by $-BC_0A\log n$). (3) The condition $k_{\max}\ge p$ cannot be dropped in favour of $k_{\max}=\lfloor n/2\rfloor$: §7.1. Under a cap, the missing ingredient is a dimension bound $\pi_0(|S|>k_{\max}-B)\to0$ for the *start*, which is not available in general (in §7.1 with the $\mathrm{BB}(1,p)$ prior the start's mode has size $k_{\max}$).

---

## 8. Summary for the lead and reviewers

**Hypotheses added (beyond the draft's statements).**
1. H1: the model prior is a fixed size-only prior with $w(k)>0$ for $0\le k\le p$ and cap $k_{\max}(n)\ge p$ for large $n$ (true for the operational cap $\lfloor n/2\rfloor$ once $n\ge2p$). Used for (1.1), hence in T3 and in the concentration half of T11(iii); T11(i)–(ii) are purely geometric and use neither the prior nor the error law. Column standardisation ($\|x_j\|^2=n$) is not used in the fixed-$p$ arguments beyond $\Gamma_n\to\Gamma\succ0$; it enters only the examples and §7.
2. Gaussian errors, $\varepsilon\sim N_n(0,\sigma_\star^2I)$, as in Section 2 of the draft (used for the exact Gaussian/$\chi^2$ laws of $\xi$ and $\varepsilon^\top P_U\varepsilon$; with i.i.d. errors having four moments the same proofs go through with $O_{\mathbb P}$ bounds, but this was not written out).
3. In T3, (U) is not needed as a hypothesis: it follows from $\Gamma\succ0$ (Lemma 1(b)); the proof uses the stronger structural fact (1.5) that every population minimiser contains $\tilde T_b$, which is what makes (R) consistent and Claim (R-suff) true.
4. Proposition 6 (the true variant of T11(iv)) assumes $k_{\max}\ge p$ (or is stated up to $\pi_0(|S|>k_{\max}-B)$) and the $\mathrm{BB}(1,p)$ prior (or $w(k+1)/w(k)\ge p^{-C_0}$).
5. (R) is read with the two bullets exhaustive as in §0.2; $\omega_n$ is taken common to all $(b,T)$, which is no loss.
6. The counterexample in §7.1 keeps $\beta^\star$, $\sigma_\star^2$, $s_0$ and the hyperparameters fixed and varies only $p=n$ and the design, exactly as the hypothesis $p\le n^A$ of (iv) allows; it is not a fixed-$p$ example (and cannot be, since with $p$ fixed the operational cap is inactive and (iv) holds).

**Constants left implicit.** $K,K_0$ in (1.4) and $K',L$ in (1.4$'$) (explicit in terms of $\|\Gamma\|$, $\lambda_{\min}(\Gamma)$, $\|\beta^\star\|$ but not written out); $C_w$ in (1.1); the $O_{\mathbb P}(1)$ in (3.1), (4.1), T3(iii)–(iv), which is identified as $-(a+\xi+\eta)/(2\bar\sigma^2(T'))+o_{\mathbb P}(1)$ plus the prior log-ratio; $c_+,c_2$ in §7.1 and $c_+$, $L_n$ in §7.2 are explicit but crude.

**Changes to the draft's statements that this proof recommends.**
1. Claim (R-suff): the sufficient rate can be relaxed from $\|\Gamma_n-\Gamma\|=O(1/n)$ to $O(n^{-1/2})$, and $n^{-1/2}$ is sharp (Remark 5.1). The draft's revision record rejected $O(n^{-1/2})$ for a reason that does not hold.
2. T11(iv): add "the cap is inactive ($k_{\max}\ge p$)" or state the conclusion up to $\pi_0(|S|>k_{\max}-B)$; with the operational cap and $p>k_{\max}+2$ it is false (§7.1).
3. T3's closing sentence: $e^{-\kappa_0n(1+o_{\mathbb P}(1))}$.

**Steps I am least sure of (none believed wrong).**
1. The reading of (R2) as "$T\not\supseteq\tilde T_b$": the draft says "every other $T\ne\tilde T_b$". Under (S) these coincide (Lemma 1(b)); if the paper ever drops $\Gamma\succ0$ in favour of (U) alone, Claim (R-suff) becomes false (§0.3, remark (c)) and T3(iii) needs the extra fact that population minimisers contain $\tilde T_b$.
2. Lemma 1(e): the Lipschitz constant $L$ of the rational map $s(\cdot)$ is asserted, not computed; the argument is the same three-term product estimate as in (d) and I see no obstacle, but it is the least explicit step.
3. Lemma 4(c): the inequality $\log(1+x)\ge(\log2)\min(x,1)$ and the passage from "$\ge\frac{2a}{3n\bar\sigma^2(T')}$ with probability $\to1$" to the displayed bound; routine but the constants were chosen for convenience.
4. The counterexample §7.1: the constants in (b)–(d) were checked by hand and by a single-seed computation (review/check_counterexample.py: at $n=3200$ the largest $\log(\mathrm{BF}_1/\mathrm{BF}_j)$ over proxies is about $-87$ against the bound $-c_2n=-20$); the mechanism does not depend on them.

---

## Audit revisions (2026-10-15)

Adjudicator B (Opus 5.5), after the GPT-6.1 Sol audits of T3 and T11 (`proofs/_audit/T3/SOL_AUDIT.md`, `proofs/_audit/T11/SOL_AUDIT.md`, both VERIFIED). The pre-audit text is saved as `PROOF_pre_audit.md`. Rulings are in `proofs/_audit/group_B/RULINGS.md`. No load-bearing step changed.

1. **Section 5, Case $T\not\supseteq\tilde T_b$.** The index set of $g_{\min}$ is nonempty in this case. When no such $T$ exists (e.g. $\beta^\star=0$), (R2) is vacuous. (T3 finding 1.)
2. **Remark 5.1.** The sharpness construction is stated for $0<\alpha<1/2$, with the reason. (T3 finding 2.)
3. **New Remark 6.0** (before Remark 6.1). "Deletions only" in T11(iii) is the net endpoint change. It neither implies that every intermediate bridge mode is nested nor that a single move crosses. It includes Sol's four-column example, in which an intermediate bridge mode adds a variable outside $\tilde S_0$; the example is checked numerically at the level of limiting scores. (T11 finding 1.)
4. **Historical notes.** The header's "not adopted" refers to the person's adoption of the proof (the research-code rule), not to review status, and stays as is. The §8 "Changes to the draft's statements that this proof recommends" have all been adopted in the draft of 15 October. (T3 and T11 draft-consistency notes, T11 finding 3.)

Checks: this folder has no top-level `check_*.py`; the review-round scripts under `review/` were not rerun. New checks T3.F2 and T11.F1 in `proofs/_audit/group_B/check_audit_B.py` PASS.

5. **After Sol's confirmations (T3 and T11, exchange 1 each).** Both gave the verdict VERIFIED. Remark 6.0's mode-sequence sentence was narrowed as Sol asked, and Sol's short analytic argument for the concentration at $\phi_n(100)$ and $\phi_n(10)$ replaces the "not proved here" caveat. T3's only request (Ex2: "its probability tends to zero by T3(i)") is draft wording, recorded in PAPER_CHANGES. These edits were not re-sent for confirmation.
