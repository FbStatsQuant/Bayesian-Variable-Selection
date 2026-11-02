# Proofs of Examples Ex1 and Ex2, Corollary C1, Propositions P3 and P4, and Problem Pb2 (elementary_II thread)

Supplement material for *Split-and-merge with an exact merge: composite-start sequential Monte Carlo for Bayesian variable selection*, draft of 15 October 2026 (after the proof audit). Thread: elementary_II. Prover: Fable 5.1 (lead), 15 October 2026. Status: **not adopted** (the proofs enter the paper only after the person has walked through them). Numerical checks in `check_elementary_II.py`, output in `check_elementary_II.out` (single seed, local; not part of the proofs).

**What is assumed.** Section 2 of the draft (model, priors, the closed form (eq:m), the data-generating model, the composite start), and the following results from the read-only proof folders, used as black boxes under exactly their stated hypotheses: from `proofs/T3_T11/PROOF.md`: the setting (S), Lemma 1 (geometry of $\bar\sigma^2$), Lemma 2 and its consequence (2.1), Lemma 3 (exact decomposition), Lemma 4 (three regimes), Claim (R-suff), Theorems T3 and T11(i)–(iii) as proved there; from `proofs/foundations/PROOF.md`: Theorem 3.2 (L6), part (i) and Lemma 3.1; from `proofs/T6`, `proofs/T7_T8` and `proofs/T9_C9`: only their lists of hypotheses (Sections 0 and 6–8), for Corollary C1(i). Lemma L3 of the draft (`proofs/elementary_I`) is used once, in Section 5.4. No other numbered result is used. No external literature is used; one attribution in the draft (Song and Liang 2015, Condition 5) is reported as the draft's and is not verified here.

**Summary of the outcome.**
- **P3**: true as stated, with the tie convention made explicit (Section 2).
- **P4**: true as stated; the known-variance marginal of part (iii) is defined in Section 3.3 (the draft does not define it); the "top-$k$" statements are exact up to ties, which the fixed order resolves (Section 3).
- **Pb2**: solved by an explicit instance with $n=10$ (Section 4): $y=(3,0,-1,0,2,0,2,0,2,0)$ on the two orthogonal columns $x_1=\mathbf 1$, $x_2=(1,-1,1,-1,\dots)$. The size-class maxima relative to $\emptyset$ are $1,\ 0.4803,\ 1.3574$: not unimodal; greedy stopping returns $\emptyset$ while the HPM is $\{1,2\}$. The hint's inequality $\mathrm{BF}(\{1,2\})>\mathrm{BF}(\{1\})\mathrm{BF}(\{2\})$ is proved for every orthogonal design and every $y$ with $u_1u_2>0$.
- **Ex1**: every displayed claim is true (Section 5): $\bar\sigma^2_2(T)=\sigma_\star^2+\beta^2(1-r^2\mathbf 1\{3\in T\})$ for all $T\subseteq C_2$, $\tilde T_2=\{3\}$, $\tilde S_0=\{1,3\}$, $\kappa_0>0$, no cancellation, exactly one proxy, deletions only (one deletion), and aligned blocks give $\tilde S_0=S_0$. The identities need only the regime-(b) setting (S); the existence of the switch (concentration of the start at $\tilde S_0$) needs (R), as T3 does.
- **C1**: (i) true: the hypotheses of T6, T7, T8, T9, T9a, C9 and T10, as listed in their proofs, involve neither $x_j^\top y$, $x_j^\top\mu$ nor $\gamma_b$, and the example of (ii) satisfies all of them with $x_1^\top\mu=0$ (Section 6). (ii) true, with (U), (R), the three variances of the note, $\gamma_1=0$, $\gamma_2=\beta(1-\rho^2)$, $\kappa_0=0$, $\Delta_0(n)=\tfrac12\log n+O_{\mathbb P}(1)$ and the single addition all verified; the hypotheses of T8, T11 and T3 are checked one by one.
- **Ex2**: the identities, $\tilde S_0=S_0$, $\kappa_0=0$, the exact finite-sample switch conditions, and the equivalence $L>4\kappa_{\rm pair}\iff\bar\sigma^2_1(\{1\})^2>\bar\sigma^2_1(\emptyset)\sigma_\star^2$ are proved (Section 7). **Strengthening:** the inequality holds for *every* $\rho\in(0,1)$ and $\beta\neq0$, not only for $\rho$ near $1$ (the difference equals $2\sigma_\star^2\beta^2\rho(1-\rho)+\beta^4(1-\rho^2)^2>0$). **The window paragraph:** the label "heuristic" is accurate and is kept. A precise second-order expansion is proved instead (Proposition 7.4): with $\Gamma_n=\Gamma$ exactly,
  $\log a_j=n\kappa_{\rm pair}-\tfrac12\log n+\sqrt n\,V^{(j)}_n+O_{\mathbb P}(1)$ and $\log a_{12}=\tfrac n2L-\log n+\sqrt n\,V^{(12)}_n+O_{\mathbb P}(1)$, where $V^{(j)}_n$ and $V^{(12)}_n$ converge in law to centred normals with explicit, strictly positive variances. So the deterministic parts displayed in the draft are the correct centrings, but the quantities the window compares differ by $O(\log n)$ while the fluctuations are of exact order $\sqrt n$; the paragraph therefore establishes neither a window nor its probability, as the draft says. What is proved: the exponential rates ($\tfrac1n\log a_1a_2\to2\kappa_{\rm pair}$, $\tfrac1n\log a_{12}\to L/2$), the finite-sample switch has positive probability (an explicit $y$ at $n=100$, $\rho=0.9$), and the switch probability tends to $0$.

---

## 0. Setting, conventions and the frozen statements

### 0.1 Conventions

All notation is that of Section 2 of the draft. $n\ge1$, $p\ge1$; a model is $S\subseteq[p]$, $k=|S|$; $\log$ is the natural logarithm. For $S\neq\emptyset$, $X_S$, $G_S=X_S^\top X_S$, $\Gamma_S=G_S/n$, $z_S=X_S^\top y$, $H_S=(n+1)G_S+I_k$, $D_S=\det H_S/\det(G_S+I_k)$, $t_S=n\,z_S^\top H_S^{-1}z_S$, $Q_S=y^\top y-t_S$, $\nu=a_0+\tfrac n2$ with $a_0,b_0>0$; for $S=\emptyset$, $D_\emptyset=1$, $t_\emptyset=0$, $Q_\emptyset=y^\top y$. The marginal likelihood is (eq:m), $m(S)=C_nD_S^{-1/2}(2b_0+Q_S)^{-\nu}$, and $\mathrm{BF}(S)=m(S)/m(\emptyset)$. We write $\tilde Q_S=2b_0+Q_S$ and $A_0=\tilde Q_\emptyset=2b_0+y^\top y$. By the shrinkage floor (eq:floor), $Q_S\ge y^\top y/(n+1)\ge0$, so $\tilde Q_S\ge2b_0>0$ and $m(S)>0$ for every $S$ and every $y$.

**Prior and cap.** $p(S)=w(|S|)\mathbf 1\{|S|\le k_{\max}\}/W$. As in `proofs/elementary_I` (Section 0.1) and the draft's Section 2, a cap above $p$ is read as $\min\{k_{\max},p\}$; so $0\le k_{\max}\le p$ throughout and $w(k)>0$ is required only for $0\le k\le k_{\max}$. For $\mathrm{BB}(1,p)$, $w(k)=B(1+k,2p-k)/B(1,p)$, and by L6(i) (Theorem 3.2(i) of `proofs/foundations/PROOF.md` with $b_\pi=p$), $w(k+1)/w(k)=(k+1)/(2p-k-1)$ for $0\le k\le p-1$.

**Ties and the order.** A total order $\prec$ on the models is fixed once and for all (draft, Section 2, "Decisions"). For a nonempty finite set $\mathcal V$ of models and $f:\mathcal V\to\mathbb R$, the *order-first maximiser* of $f$ over $\mathcal V$ is the $\prec$-least element of $\arg\max_{\mathcal V}f$. The HPM is the order-first maximiser of $S\mapsto p(S)m(S)$ over all $S\subseteq[p]$; since $p(\emptyset)m(\emptyset)>0$, it lies in the support $\{|S|\le k_{\max}\}$.

**Data-generating model and regime (b).** $y=\mu+\varepsilon$, $\mu=X\beta^\star$, $\varepsilon\sim N_n(0,\sigma_\star^2I_n)$, $S_0=\operatorname{supp}\beta^\star$, $s_0=|S_0|$; $\mathbb P_0$, $\mathbb E_0$ are over $\varepsilon$ with $X$ fixed. For Ex1, Ex2 and C1(ii) the standing setting is the draft's **regime (b)**, which is the setting (S) of `proofs/T3_T11/PROOF.md` Section 0.1: (S1) $p$, the partition $[p]=C_1\cup\dots\cup C_L$, $\beta^\star$, $\sigma_\star^2$, $a_0,b_0$ fixed; (S2) a fixed size-only prior with $w(k)>0$ for $0\le k\le p$ and $k_{\max}\ge p$ for all large $n$ (the operational cap $\lfloor n/2\rfloor$ qualifies once $n\ge2p$); (S3) standardised columns and $\Gamma_n=X_n^\top X_n/n\to\Gamma\succ0$; (S4) Gaussian errors as above. For $T\subseteq[p]$,
$$
\bar\sigma^2_n(T)=\sigma_\star^2+\beta^{\star\top}\big(\Gamma_n-\Gamma_{n,\cdot T}\Gamma_{n,TT}^{-1}\Gamma_{n,T\cdot}\big)\beta^\star,\qquad
\bar\sigma^2(T)=\sigma_\star^2+\beta^{\star\top}\big(\Gamma-\Gamma_{\cdot T}\Gamma_{TT}^{-1}\Gamma_{T\cdot}\big)\beta^\star,
$$
the subtracted term being absent for $T=\emptyset$; for $T\subseteq C_b$ the draft writes $\bar\sigma^2_b(T)=\bar\sigma^2(T)$. Conditions (U) and (R), the sets $\tilde T_b$, $\tilde S_0=\bigcup_b\tilde T_b$, the block projections $\gamma_b=\Gamma_{C_bC_b}^{-1}\Gamma_{C_b,[p]}\beta^\star$, the start $\pi_0$, the deficit $\Delta_0(n)=\log\{\pi_0(\tilde S_0)/\pi_0(S_0)\}$ and $\kappa_0=\tfrac12\sum_b\log\{\bar\sigma^2_b(S_0\cap C_b)/\bar\sigma^2_b(\tilde T_b)\}$ are as in the draft (Section 3.3) and in `proofs/T3_T11` Section 0.2.

**Facts imported from `proofs/T3_T11/PROOF.md`** (cited by their numbers there; all under (S) unless said otherwise).
- **(F-geo)** Lemma 1: with $A$ symmetric positive semidefinite, $A=V^\top V$, $f=V\beta^\star$ and $R_A(T)=\beta^{\star\top}(A-A_{\cdot T}A_{TT}^{-1}A_{T\cdot})\beta^\star$: (a) $R_A(T)=\operatorname{dist}(f,\operatorname{span}\{v_j:j\in T\})^2$; (b) for $C\subseteq[p]$ with $A_{CC}\succ0$ and $\gamma=A_{CC}^{-1}A_{C,[p]}\beta^\star$, the minimisers of $R_A$ over $2^C$ are exactly the $T$ with $\operatorname{supp}(\gamma)\subseteq T\subseteq C$, and $\gamma_j=\beta^\star_j+[A_{CC}^{-1}A_{C,C^c}\beta^\star_{C^c}]_j$; (c) if $A\succ0$, $R_A(S)=0$ iff $S\supseteq S_0$; (d) $\bar\sigma^2_n(T)-\sigma_\star^2=\tfrac1n\|(I-P_T)\mu\|^2$ and $\bar\sigma^2_n(T)\to\bar\sigma^2(T)$. Consequence (1.5): $\tilde T_b=\operatorname{supp}(\gamma_b)$ and every population minimiser of block $b$ contains $\tilde T_b$. Consequence (1.7): for $T\subseteq T'$, $n[\bar\sigma^2_n(T)-\bar\sigma^2_n(T')]=\|(P_{T'}-P_T)\mu\|^2\ge0$.
- **(F-det)** Lemma 2 and (2.1): for $T\ne\emptyset$ with $g_T=\lambda_{\min}(G_T)>0$, $\tilde Q_T=2b_0+\mathrm{RSS}_T+d_T$ with $\mathrm{RSS}_T=\|(I-P_T)y\|^2$ and $0\le d_T\le\frac{1+1/g_T}{n+1}\|P_Ty\|^2$; and, for $n\ge\max(n_0,2/\lambda)$ with $\lambda=\lambda_{\min}(\Gamma)$, $\log D_T=|T|\log n+r_T$ with $|r_T|\le|T|(\tfrac1n+\tfrac2{n\lambda})$ and $0\le d_T\le2\|y\|^2/(n+1)$.
- **(F-dec)** Lemma 3 with $T'=\emptyset$: $\tilde Q_T=\tilde Q_\emptyset-\|P_T\mu\|^2-2\mu^\top P_T\varepsilon-\varepsilon^\top P_T\varepsilon+d_T$, and $\tilde Q_\emptyset=2b_0+\|\mu\|^2+2\mu^\top\varepsilon+\|\varepsilon\|^2$.
- **(F-rate)** Lemma 4(a): for fixed $T,T'$, $\tfrac1n[\log\mathrm{BF}(T)-\log\mathrm{BF}(T')]\to-\tfrac12\log\{\bar\sigma^2(T)/\bar\sigma^2(T')\}$ in probability.
- **(F-R)** Claim (R-suff): $\|\Gamma_n-\Gamma\|=O(n^{-1/2})$ implies (R); (U) holds under (S).
- **(F-T3)** Theorem T3 as proved there; (i) for the start and (iii) need (R); (i) for the posterior, (ii) and (iv) need only (S). **(F-T11)** Theorem T11(i)–(iii) as proved there (under (S); the start-concentration clause of (iii) under (R)).

### 0.2 The statements, as frozen from the draft (verbatim)

**Example Ex1 (A proxy in another block: linear gap).** *[Status: Elementary]* Setup: $C_1\ni1$ and $C_2\ni3$; $\Gamma_{13}=r$ with $0<|r|<1$, and columns $1$ and $3$ are exactly uncorrelated with all other columns at every $n$; $\beta^\star=\beta e_1$ with $\beta\ne0$. Then: $\bar\sigma^2_2(\emptyset)=\sigma_\star^2+\beta^2$ and $\bar\sigma^2_2(\{3\})=\sigma_\star^2+\beta^2(1-r^2)$, so $\tilde T_2=\{3\}$ and $\tilde S_0=\{1,3\}\supsetneq S_0$; $\kappa_0=\tfrac12\log\frac{\sigma_\star^2+\beta^2}{\sigma_\star^2+\beta^2(1-r^2)}>0$. The switch here is a single deletion, as T11(iii) predicts: $\gamma_{2,3}=r\beta\ne0$ makes $3$ a proxy. Whether local kernels cross it is a quantitative question (Problem Pb4). Blocks aligned with the correlation of $X$ (putting $1$ and $3$ together) remove the switch altogether.

**Example Ex2 (A split cancelling pair: a finite-$n$ switch).** *[Status: Elementary]* Setup: $C_1=\{1\}$ and $C_2=\{2\}$; $\Gamma_{12}=\rho\in(0,1)$; $\beta^\star=(\beta,-\beta)$. Then $\bar\sigma^2_1(\emptyset)=\sigma_\star^2+2\beta^2(1-\rho)$ and $\bar\sigma^2_1(\{1\})=\sigma_\star^2+\beta^2(1-\rho^2)$, so $\tilde S_0=S_0$ and $\kappa_0=0$. Yet the per-block log-gain
$\kappa_{\rm pair}=\tfrac12\log\frac{\sigma_\star^2+2\beta^2(1-\rho)}{\sigma_\star^2+\beta^2(1-\rho^2)}$
is small when $\rho$ is near $1$.
*Exact finite-sample switch conditions* for $p=2$, cap $2$, $\mathrm{BB}(1,2)$ prior. Here $w(0):w(1):w(2)=3:1:1$. Write $a_j=\mathrm{BF}(\{j\})$ and $a_{12}=\mathrm{BF}(\{1,2\})$. Ignoring ties, the start's mode is $\emptyset$ and the posterior's mode is $S_0=\{1,2\}$ if and only if
$\max(a_1,a_2)<3,\quad a_1a_2<3,\quad a_{12}>\max(3,a_1,a_2).$
Asymptotically: $\log a_j\approx n\kappa_{\rm pair}-\tfrac12\log n$; $\log a_{12}\approx\tfrac n2\log\big(1+2\beta^2(1-\rho)/\sigma_\star^2\big)-\log n$.
Put $L=\log(1+2\beta^2(1-\rho)/\sigma_\star^2)$. Then $a_1a_2\approx e^{2n\kappa_{\rm pair}}/n$ and $a_{12}\approx e^{nL/2}/n$, so a window of $n$ in which the switch exists requires $L>4\kappa_{\rm pair}$. Equivalently, $\bar\sigma^2_1(\{1\})^2>\bar\sigma^2_1(\emptyset)\,\sigma_\star^2$, which holds for $\rho$ near $1$ (lead's derivation). This calculation is heuristic: it keeps only the leading terms, whereas $\log a_j$ and $\log a_{12}$ fluctuate by $O_{\mathbb P}(\sqrt n)$, so it does not establish a window or its probability. A finite-sample switch is then possible; its probability tends to zero as $n\to\infty$, by T3(i).

**Corollary C1 (No marginal-correlation condition).** *[Status: Elementary given T3, T8, T11]* (i) T6–T10 impose no condition on the marginal covariances $x_j^\top y/n$, nor on the block projections $\gamma_b$. In particular they hold when a true variable is marginally uncorrelated with the response, i.e. when the condition $|\mathrm{cov}(x_j,y)|>0$ for all $j\in S_0$ (Song and Liang 2015, Condition 5) fails. (ii) *Example.* Let $p=2$, $\Gamma_n=\Gamma=\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix}$ exactly for every $n$, with $\rho\in(0,1)$, and $\beta^\star=(-\rho\beta,\beta)$ with $\beta\ne0$. Then $x_1^\top\mu=0$ for every $n$, yet $\Pi(S_0\mid y)\to1$ by T8. With singleton blocks, variable $1$ is cancelled ($\gamma_{1}=0$, $\gamma_2=\beta(1-\rho^2)\neq0$), so by T11 $\tilde S_0=\{2\}$. Here $\kappa_0=0$, and by T3(iii) $\Delta_0(n)=\tfrac12\log n+O_{\mathbb P}(1)$: the start misses variable $1$, but only by a polynomial factor, and the switch is a single addition. With both variables in one block, $\tilde S_0=S_0$ and there is no switch.
*Notes.* (ii): $\bar\sigma^2(\{1\})=\bar\sigma^2(\emptyset)=\sigma_\star^2+\beta^2(1-\rho^2)$ and $\bar\sigma^2(\{2\})=\sigma_\star^2+\beta^2\rho^2(1-\rho^2)$. Condition (R) holds because the cancellation is exact at every $n$. Check (U), (R) and the constants. By T4, the bridge needs about $\log_2\log\sqrt n$ stages for this switch. Whether the particles cross it is Problem Pb4: a single addition, which single-site Gibbs proposes directly.

**Proposition P3 (The size-only ceiling).** *[Status: Elementary]* Let $p(S)\propto w(|S|)$ with $w>0$ on $\{0,\dots,k_{\max}\}$, assume $s_0\le k_{\max}$, and use the fixed tie order of Section 2. For each $k$, let $\hat S_k$ be the order-first maximiser of $m$ over $\{|S|=k\}$. Then
$\mathrm{HPM}=\hat S_{\hat k},\qquad \hat k=\operatorname{arg\,max}_{k\le k_{\max}}\ w(k)\,m(\hat S_k).$
Hence $\{\mathrm{HPM}=S_0\}\subseteq\mathcal W:=\{\hat S_{s_0}=S_0\}$, and $\mathbb P_0(\mathrm{HPM}=S_0)\le\mathbb P_0(\mathcal W)$ for every size-only prior. The supremum over strictly positive $w$ equals $\mathbb P_0(\mathcal W)$, approached by $w$ concentrating on $s_0$, and attained if $w=0$ off $s_0$ is allowed. Such a $w$ depends on the true size, so it is not implementable.

**Proposition P4 (Orthogonal designs: exact odds and the top-$k$ structure).** *[Status: Elementary]* Let $X^\top X=nI_p$, which requires $p\le n$. Put: $u_j=z_j^2/n$, $h=n^2/(n^2+n+1)$ and $D=(n^2+n+1)/(n+1)$; $U_{(k)}$, the sum of the $k$ largest $u_j$.
(i) $Q_S=y^\top y-h\sum_{j\in S}u_j$ and $D_S=D^{|S|}$. For $j\notin S$ with $|S|=k<k_{\max}$, the *exact* neighbour log-odds are
$\log\frac{\pi(S\cup\{j\})}{\pi(S)}=\log\frac{w(k+1)}{w(k)}-\tfrac12\log D+\nu\log\frac{2b_0+Q_S}{2b_0+Q_S-hu_j}.$
(ii) For each $k$, the best model of size $k$ consists of the $k$ largest $u_j$. Hence $\mathrm{HPM}$ is the top-$\hat k$ set, with
$\hat k=\operatorname{arg\,max}_{k\le k_{\max}}\Big\{\log w(k)-\tfrac k2\log D-\nu\log\big(2b_0+y^\top y-hU_{(k)}\big)\Big\}.$
(iii) *(Known variance, for intuition.)* If $\sigma^2$ is known, adding $j$ to a size-$k$ model increases the posterior if and only if
$\frac{hu_j}{\sigma^2}>\log D+2\log\frac{w(k)}{w(k+1)}.$
For $\mathrm{BB}(1,p)$ the right-hand side is $\approx\log n+2\log\frac{2p-k-1}{k+1}$.
*Notes.* Direct computation from (eq:m). Part (ii) holds because, for fixed size, $m(S)$ is increasing in $\sum_{j\in S}u_j$.

**Problem Pb2 (Greedy stopping fails).** *[Status: Elementary]* Construct an orthogonal instance in which $k\mapsto\max_{|S|=k}\log\{p(S)m(S)\}$ is not unimodal. In such an instance, forward selection that stops at the first non-improving addition misses the HPM.
Hint: $\mathrm{BB}(1,2)$, cap $2$, orthogonal predictors with equal singleton Bayes factors $2$. Orthogonality forces $\mathrm{BF}(\{1,2\})>4$, so the relative scores of $\emptyset$, a singleton and the pair are $1$, $2/3$ and $>4/3$. Exhibit $n$ and $y$; $n=10$ should be possible.

### 0.3 Readings adopted (flagged)

- **(Rd1) P3, ties in $\hat k$.** If several sizes attain $\max_kw(k)m(\hat S_k)$, "$\hat k=\arg\max_k$" is read as the $k$ among them whose $\hat S_k$ is $\prec$-least; this is the only reading under which $\mathrm{HPM}=\hat S_{\hat k}$ holds for every $y$ (Section 2). The supremum statement is read with $w$ ranging over all strictly positive weights on $\{0,\dots,k_{\max}\}$.
- **(Rd2) P4(ii), ties in $u$.** "The best model of size $k$ consists of the $k$ largest $u_j$" is read as: every maximiser of $m$ over $\{|S|=k\}$ has $\sum_{j\in S}u_j=U_{(k)}$, and every set of $k$ indices carrying the $k$ largest values (any such set, when values tie) is a maximiser. "HPM is the top-$\hat k$ set" is read with the fixed order resolving ties, as in (Rd1). $k$ ranges over $0\le k\le\min\{k_{\max},p\}$.
- **(Rd3) P4(iii), known variance.** The draft does not define the known-variance posterior. It is read as: $\sigma^2$ fixed and known, $\beta_S\mid S\sim N_k(0,\sigma^2\Lambda_S^{-1})$ as in Section 2, the same model prior; the marginal $m_\sigma(S)=\int N_n(y;X_S\beta_S,\sigma^2I)N_k(\beta_S;0,\sigma^2\Lambda_S^{-1})\,d\beta_S$ (Section 3.3). "$\approx$" in the last sentence is made explicit: the difference is $\log\big(1+\tfrac1{n(n+1)}\big)\in(0,\tfrac1{n(n+1)})$.
- **(Rd4) Ex1.** $C_1$ and $C_2$ are two distinct blocks of the partition; $\Gamma_{13}=r$ refers to the limit $\Gamma$ (it may or may not hold at every $n$); "exactly uncorrelated at every $n$" means $x_1^\top x_j=0=x_3^\top x_j$ for all $j\notin\{1,3\}$ and all $n$, hence also $\Gamma_{1j}=\Gamma_{3j}=0$ in the limit. The regime-(b) setting (S) is in force (in particular $\Gamma\succ0$ and $p\ge3$). The claims about $\bar\sigma^2$, $\tilde T_b$, $\gamma_b$, $\kappa_0$ and the structure of the switch are proved under (S); the sentence "the switch" (the start concentrating at $\tilde S_0$ while the posterior concentrates at $S_0$) is T3(i) and needs (R), which the example does not assert; this is flagged in Section 8.
- **(Rd5) Ex2.** "Cap $2$" is no cap ($\min\{k_{\max},p\}=2$); the $\mathrm{BB}(1,2)$ prior has $p=2$. "Ignoring ties" means that the three displayed strict inequalities are shown equivalent to the conjunction "the maximiser of $\gamma_0$ is $\emptyset$ and the maximiser of $p\cdot\mathrm{BF}$ is $\{1,2\}$, both unique". The asymptotic displays with "$\approx$" are read as the second-order expansions of Proposition 7.4, proved under $\Gamma_n=\Gamma$ exactly; the "window" paragraph is read as the draft labels it, heuristic, and its status is assessed in Section 7.5.
- **(Rd6) C1(i).** "T6–T10" is read as T6, T7, T8, T9, T9a, C9 and T10, i.e. every numbered result of the draft's Section 4 between T6 and T10; "impose no condition on" means that none of their hypotheses, as listed in the proofs, constrains $x_j^\top y/n$, $x_j^\top\mu/n$ or $\gamma_b$, and that these quantities are not determined by the hypotheses (witnessed by the example of (ii)). The fixed-design reading of "$\mathrm{cov}(x_j,y)$" is $x_j^\top\mu/n$ (its random version $x_j^\top y/n$ is also covered).
- **(Rd7) C1(ii).** The cap is the operational one, $\lfloor n/2\rfloor$ (so $k_{\max}\ge2=p$ for $n\ge4$); "$\Pi(S_0\mid y)\to1$ by T8" is read as an application of Theorem 8.1 of `proofs/T7_T8/PROOF.md`, whose hypotheses are checked in Section 6.2.
- **(Rd8) Pb2.** "An orthogonal instance" means $n$, $X$ with $X^\top X=nI_p$, a prior and a $y$, all explicit. "Greedy stopping" is forward selection from $\emptyset$ that adds the best single variable while the score $p(S)m(S)$ increases and stops at the first non-improving step.

---

## 1. Preliminaries

**Lemma 1.1 (Bayes factor differences).** For any models $T,T'$,
$$
\log\mathrm{BF}(T)-\log\mathrm{BF}(T')=-\tfrac12\log\frac{D_T}{D_{T'}}-\nu\log\frac{\tilde Q_T}{\tilde Q_{T'}} ,\qquad \log\frac{p(T)m(T)}{p(T')m(T')}=\log\frac{w(|T|)}{w(|T'|)}+\log\mathrm{BF}(T)-\log\mathrm{BF}(T')
$$
for $|T|,|T'|\le k_{\max}$. *Proof.* Take logarithms in (eq:m); $C_n$ and $m(\emptyset)$ cancel. $\square$

**Lemma 1.2 (the $\mathrm{BB}(1,2)$ weights).** For $p=2$: $w(0)=\tfrac12$, $w(1)=w(2)=\tfrac16$; hence $w(0):w(1):w(2)=3:1:1$ and $\sum_k\binom2kw(k)=1$.
*Proof.* $B(1,2)=\tfrac12$; $w(0)=B(1,4)/B(1,2)=\tfrac14\cdot2=\tfrac12$; $w(1)=B(2,3)/B(1,2)=\frac{\Gamma(2)\Gamma(3)}{\Gamma(5)}\cdot2=\frac{2}{24}\cdot2=\tfrac16$; $w(2)=B(3,2)/B(1,2)=\tfrac16$ by symmetry of $B$. Alternatively L6(i): $w(1)/w(0)=1/(2p-1)=\tfrac13$, $w(2)/w(1)=2/(2p-2)=1$. $\square$

**Lemma 1.3 (a design with a prescribed Gram matrix).** For every $n\ge p$ and every $\Gamma\succ0$ with unit diagonal there is $X\in\mathbb R^{n\times p}$ with $X^\top X=n\Gamma$ (hence standardised columns): $X=\sqrt n\,Q\Gamma^{1/2}$ with $Q\in\mathbb R^{n\times p}$ having orthonormal columns. In particular "$\Gamma_n=\Gamma$ exactly for every $n$" (C1(ii)) and "$X^\top X=nI_p$" (P4, Pb2) are realisable for every $n\ge p$, and $X^\top X=nI_p$ forces $p=\operatorname{rank}(X^\top X)\le n$. $\square$

---

## 2. Proposition P3: the size-only ceiling

Throughout this section $X$ and $y$ are arbitrary (then $y$ is random); $w(k)>0$ for $0\le k\le k_{\max}\le p$, $s_0\le k_{\max}$. For $0\le k\le k_{\max}$ the class $\{|S|=k\}$ is nonempty because $k\le p$, so $\hat S_k$ is well defined; it depends on $y$, the order and $k$ only, not on $w$.

**Theorem 2.1 (P3, first display).** Let $M=\max_{S\subseteq[p]}p(S)m(S)$ and $K^\ast=\{k\le k_{\max}:w(k)m(\hat S_k)=WM\}$. Then $K^\ast\ne\emptyset$, and with $\hat k$ the unique $k\in K^\ast$ such that $\hat S_k\preceq\hat S_{k'}$ for all $k'\in K^\ast$ (reading (Rd1)),
$$
\mathrm{HPM}=\hat S_{\hat k}.
$$
When $K^\ast$ is a singleton, $\hat k$ is the plain $\arg\max_{k\le k_{\max}}w(k)m(\hat S_k)$.

*Proof.* Models with $|S|>k_{\max}$ have $p(S)m(S)=0<p(\emptyset)m(\emptyset)$, so $M=\max_{k\le k_{\max}}\max_{|S|=k}w(k)m(S)/W=\max_{k\le k_{\max}}w(k)m(\hat S_k)/W$, using $w(k)>0$ and the definition of $\hat S_k$ as a maximiser of $m$ over $\{|S|=k\}$. Hence $K^\ast\ne\emptyset$. Within a size class $k$, $p(S)m(S)=w(k)m(S)/W$ is a positive multiple of $m(S)$, so $\arg\max_{|S|=k}p\,m=\arg\max_{|S|=k}m=:\mathcal M_k$, whose $\prec$-least element is $\hat S_k$. Therefore
$$
\arg\max_Sp(S)m(S)=\bigcup_{k\in K^\ast}\mathcal M_k .
$$
The $\prec$-least element of a finite union is the $\prec$-least among the $\prec$-least elements of the parts; the $\prec$-least element of $\mathcal M_k$ is $\hat S_k$; and the sets $\hat S_k$, $k\in K^\ast$, are pairwise distinct (distinct sizes), so exactly one of them is $\prec$-least, namely $\hat S_{\hat k}$. Hence $\mathrm{HPM}=\hat S_{\hat k}$. $\square$

**Theorem 2.2 (P3, the ceiling).** (a) $\{\mathrm{HPM}=S_0\}\subseteq\mathcal W=\{\hat S_{s_0}=S_0\}$, for every $y$ and every $w$; hence $\mathbb P_0(\mathrm{HPM}=S_0)\le\mathbb P_0(\mathcal W)$ for every size-only prior, and $\mathcal W$ does not depend on $w$.
(b) $\sup_w\mathbb P_0(\mathrm{HPM}_w=S_0)=\mathbb P_0(\mathcal W)$, the supremum over all strictly positive $w$ on $\{0,\dots,k_{\max}\}$; it is approached along $w_\epsilon(k)=\mathbf 1\{k=s_0\}+\epsilon\mathbf 1\{k\ne s_0\}$ as $\epsilon\downarrow0$.
(c) If $w=\mathbf 1\{k=s_0\}$ is allowed, then $\{\mathrm{HPM}=S_0\}=\mathcal W$ exactly.

*Proof.* (a) If $\mathrm{HPM}=S_0$ then by Theorem 2.1 $S_0=\hat S_{\hat k}$, so $\hat k=|S_0|=s_0$ and $S_0=\hat S_{s_0}$. Since $\hat S_{s_0}$ is defined from $m$, the order and $s_0$ alone, $\mathcal W$ is the same event for every $w$.
(b) Fix $\epsilon\in(0,1)$ and let $A_\epsilon=\{m(S_0)>\epsilon\max_{S\subseteq[p]}m(S)\}$. On $\mathcal W\cap A_\epsilon$: $w_\epsilon(s_0)m(\hat S_{s_0})=m(S_0)>\epsilon\max_Sm(S)\ge\epsilon\,m(\hat S_k)=w_\epsilon(k)m(\hat S_k)$ for every $k\ne s_0$, so $K^\ast=\{s_0\}$, $\hat k=s_0$ and $\mathrm{HPM}_{w_\epsilon}=\hat S_{s_0}=S_0$ by Theorem 2.1. Hence $\mathbb P_0(\mathrm{HPM}_{w_\epsilon}=S_0)\ge\mathbb P_0(\mathcal W\cap A_\epsilon)$. The events $A_\epsilon$ increase as $\epsilon\downarrow0$ to $\{m(S_0)>0\}$, which is the sure event because $m>0$ (Section 0.1); by continuity of $\mathbb P_0$ from below, $\mathbb P_0(\mathcal W\cap A_\epsilon)\uparrow\mathbb P_0(\mathcal W)$. With (a), $\sup_w\mathbb P_0(\mathrm{HPM}_w=S_0)=\mathbb P_0(\mathcal W)$.
(c) With $w=\mathbf 1\{k=s_0\}$, $p(S)m(S)$ vanishes off $\{|S|=s_0\}$ and is a positive multiple of $m$ on it, so the HPM is the order-first maximiser of $m$ over $\{|S|=s_0\}$, i.e. $\hat S_{s_0}$; thus $\mathrm{HPM}=S_0$ iff $\hat S_{s_0}=S_0$. $\square$

*Remark 2.3.* (a) The hypothesis $s_0\le k_{\max}$ is used in (b)–(c): if $s_0>k_{\max}$ then $p(S_0)=0$, $\mathrm{HPM}\ne S_0$ always, and the supremum is $0$, while $\mathbb P_0(\mathcal W)$ can be positive. (b) The last sentence of P3 ("such a $w$ depends on the true size, so it is not implementable") is a remark, not a mathematical claim. (c) Nothing about the form of $m$ was used beyond $m>0$; the result holds for any positive model score with a size-only prior.

---

## 3. Proposition P4: orthogonal designs

Throughout, $X^\top X=nI_p$ (so $p\le n$, Lemma 1.3), $u_j=z_j^2/n$ with $z_j=x_j^\top y$, $h=n^2/(n^2+n+1)$, $D=(n^2+n+1)/(n+1)$, and $0\le k_{\max}\le p$.

### 3.1 Part (i)

**Lemma 3.1.** For every $S\subseteq[p]$ with $|S|=k$: $G_S=nI_k$, $H_S=(n^2+n+1)I_k$, $D_S=D^k$, $t_S=h\sum_{j\in S}u_j$ and $Q_S=y^\top y-h\sum_{j\in S}u_j$. In particular $\tilde Q_S=A_0-h\sum_{j\in S}u_j>0$.

*Proof.* For $k=0$ all statements are the conventions ($D_\emptyset=1$, $t_\emptyset=0$). For $k\ge1$, $G_S=X_S^\top X_S=nI_k$ because the columns are orthogonal with squared norm $n$; hence $H_S=(n+1)nI_k+I_k=(n^2+n+1)I_k$, $G_S+I_k=(n+1)I_k$, and $D_S=\big(\tfrac{n^2+n+1}{n+1}\big)^k=D^k$. Next $t_S=n\,z_S^\top H_S^{-1}z_S=\frac{n}{n^2+n+1}\sum_{j\in S}z_j^2=\frac{n^2}{n^2+n+1}\sum_{j\in S}\frac{z_j^2}{n}=h\sum_{j\in S}u_j$, and $Q_S=y^\top y-t_S$. Positivity of $\tilde Q_S$ is Section 0.1. $\square$

**Theorem 3.2 (P4(i)).** For $j\notin S$ with $|S|=k<k_{\max}$,
$$
\log\frac{\pi(S\cup\{j\})}{\pi(S)}=\log\frac{w(k+1)}{w(k)}-\tfrac12\log D+\nu\log\frac{2b_0+Q_S}{2b_0+Q_S-hu_j}.
$$
*Proof.* Both $S$ and $S\cup\{j\}$ have size $\le k_{\max}$, so $\pi(S\cup\{j\})/\pi(S)=\frac{w(k+1)m(S\cup\{j\})}{w(k)m(S)}$. By Lemma 1.1 and Lemma 3.1, $\log\frac{m(S\cup\{j\})}{m(S)}=-\tfrac12\log\frac{D^{k+1}}{D^k}-\nu\log\frac{\tilde Q_{S\cup\{j\}}}{\tilde Q_S}$, and $\tilde Q_{S\cup\{j\}}=\tilde Q_S-hu_j=2b_0+Q_S-hu_j$. $\square$

### 3.2 Part (ii)

**Theorem 3.3 (P4(ii)).** (a) For fixed $k$, $m(S)=C_nD^{-k/2}\big(A_0-h\sum_{j\in S}u_j\big)^{-\nu}$ is a strictly increasing function of $\sum_{j\in S}u_j$ on $\{|S|=k\}$. Hence $\max_{|S|=k}m(S)=C_nD^{-k/2}(A_0-hU_{(k)})^{-\nu}$, the maximisers are exactly the $S$ with $\sum_{j\in S}u_j=U_{(k)}$, and every set of $k$ indices carrying $k$ largest values of $u$ is a maximiser; if the $k$-th and $(k+1)$-th largest values of $u$ differ, the maximiser is unique and equals the top-$k$ set.
(b) With $\hat S_k$ the order-first maximiser over $\{|S|=k\}$ (Section 2),
$$
\log\{w(k)m(\hat S_k)\}=\log C_n+\log w(k)-\tfrac k2\log D-\nu\log\big(2b_0+y^\top y-hU_{(k)}\big),
$$
so the $\hat k$ of Theorem 2.1 is the $\arg\max$ over $0\le k\le k_{\max}$ of the braces in P4(ii) (ties as in (Rd1)), and $\mathrm{HPM}=\hat S_{\hat k}$ is a top-$\hat k$ set.

*Proof.* (a) By Lemma 3.1, $m(S)=C_nD^{-k/2}(A_0-hs)^{-\nu}$ with $s=\sum_{j\in S}u_j$; since $h>0$, $\nu>0$ and $A_0-hs>0$, this is strictly increasing in $s$. The maximum of $s$ over $k$-subsets is $U_{(k)}$, attained exactly by the sets carrying $k$ largest values; the uniqueness claim is immediate. (b) Insert (a) into $\log w(k)+\log m(\hat S_k)$; the constant $\log C_n$ does not affect the $\arg\max$. Theorem 2.1 gives $\mathrm{HPM}=\hat S_{\hat k}$, and by (a) $\hat S_{\hat k}$ carries the $\hat k$ largest values of $u$. $\square$

### 3.3 Part (iii): known variance

**Definition (reading (Rd3)).** For known $\sigma^2>0$, put
$$
m_\sigma(S)=\int_{\mathbb R^k}N_n(y;X_S\beta_S,\sigma^2I_n)\,N_k(\beta_S;0,\sigma^2\Lambda_S^{-1})\,d\beta_S,\qquad \Lambda_S=\tfrac1n(G_S+I_k),
$$
with $m_\sigma(\emptyset)=N_n(y;0,\sigma^2I_n)$, and $\pi_\sigma(S)\propto p(S)m_\sigma(S)$.

**Lemma 3.4 (the known-variance marginal; any design).** $m_\sigma(S)=(2\pi\sigma^2)^{-n/2}D_S^{-1/2}\exp\{-Q_S/(2\sigma^2)\}$.

*Proof.* For $k=0$ this is the definition ($D_\emptyset=1$, $Q_\emptyset=y^\top y$). For $k\ge1$, integrating the Gaussian in $\beta_S$ gives $y\mid S\sim N_n(0,\sigma^2\Sigma_S)$ with $\Sigma_S=I_n+X_S\Lambda_S^{-1}X_S^\top$. By Sylvester's determinant identity, $\det\Sigma_S=\det(I_k+\Lambda_S^{-1}G_S)=\det(\Lambda_S+G_S)/\det\Lambda_S=\det\big(\tfrac1n((n+1)G_S+I_k)\big)/\det\big(\tfrac1n(G_S+I_k)\big)=D_S$. By the Woodbury identity, $\Sigma_S^{-1}=I_n-X_S(\Lambda_S+G_S)^{-1}X_S^\top$, and $\Lambda_S+G_S=\tfrac1nH_S$, so $y^\top\Sigma_S^{-1}y=y^\top y-n\,z_S^\top H_S^{-1}z_S=Q_S$. Hence $m_\sigma(S)=(2\pi\sigma^2)^{-n/2}(\det\Sigma_S)^{-1/2}\exp\{-y^\top\Sigma_S^{-1}y/(2\sigma^2)\}$ is as claimed. $\square$

**Theorem 3.5 (P4(iii)).** In the orthogonal design, for $j\notin S$, $|S|=k<k_{\max}$,
$$
\log\frac{\pi_\sigma(S\cup\{j\})}{\pi_\sigma(S)}=\log\frac{w(k+1)}{w(k)}-\tfrac12\log D+\frac{hu_j}{2\sigma^2},
$$
which is $>0$ if and only if $\frac{hu_j}{\sigma^2}>\log D+2\log\frac{w(k)}{w(k+1)}$. For $\mathrm{BB}(1,p)$ and $0\le k\le p-1$ the right-hand side equals $\log n+\log\big(1+\tfrac1{n(n+1)}\big)+2\log\frac{2p-k-1}{k+1}$, and $0<\log(1+\tfrac1{n(n+1)})<\tfrac1{n(n+1)}$.

*Proof.* By Lemma 3.4 and Lemma 3.1, $\log\frac{m_\sigma(S\cup\{j\})}{m_\sigma(S)}=-\tfrac12\log D+\frac{Q_S-Q_{S\cup\{j\}}}{2\sigma^2}=-\tfrac12\log D+\frac{hu_j}{2\sigma^2}$; add the prior ratio. Multiplying the positivity condition by $2$ gives the displayed inequality. For $\mathrm{BB}(1,p)$, L6(i) gives $w(k)/w(k+1)=(2p-k-1)/(k+1)$, and $D=\frac{n^2+n+1}{n+1}=n\cdot\frac{n^2+n+1}{n^2+n}=n\big(1+\tfrac1{n(n+1)}\big)$; finally $0<\log(1+x)<x$ for $x>0$. $\square$

*Remark 3.6.* (a) The identity of Lemma 3.4 is the known-variance analogue of (eq:m): integrating $m_\sigma(S)$ against the $\mathrm{IG}(a_0,b_0)$ prior for $\sigma^2$ gives $C_nD_S^{-1/2}(2b_0+Q_S)^{-\nu}$, which is (eq:m); so the reading (Rd3) is the one consistent with the draft's model. (b) Part (iii) requires nothing of $k_{\max}$ beyond $k+1\le k_{\max}$, and (i)–(ii) require $k\le\min\{k_{\max},p\}$.

---

## 4. Problem Pb2: an instance where greedy stopping fails

### 4.1 The structure forced by orthogonality

**Lemma 4.1.** Let $X^\top X=nI_2$ ($p=2$) and $y\in\mathbb R^n$. Then $\mathrm{BF}(\{1,2\})\ge\mathrm{BF}(\{1\})\mathrm{BF}(\{2\})$, with strict inequality if and only if $u_1u_2>0$.

*Proof.* By Lemma 3.1, $\mathrm{BF}(\{j\})=D^{-1/2}\big(\tfrac{A_0}{A_0-hu_j}\big)^\nu$ and $\mathrm{BF}(\{1,2\})=D^{-1}\big(\tfrac{A_0}{A_0-hu_1-hu_2}\big)^\nu$, all denominators positive. Now $(A_0-hu_1)(A_0-hu_2)=A_0(A_0-hu_1-hu_2)+h^2u_1u_2\ge A_0(A_0-hu_1-hu_2)>0$, with equality iff $u_1u_2=0$. Taking reciprocals, multiplying by $A_0^2$ and raising to the power $\nu>0$ gives $\big(\tfrac{A_0}{A_0-hu_1-hu_2}\big)^\nu\ge\big(\tfrac{A_0}{A_0-hu_1}\big)^\nu\big(\tfrac{A_0}{A_0-hu_2}\big)^\nu$, with the same equality case; multiply by $D^{-1}$. $\square$

**Corollary 4.2 (the hint).** Under $\mathrm{BB}(1,2)$ with cap $2$ (Lemma 1.2: weights $3:1:1$), write $a_j=\mathrm{BF}(\{j\})$, $a_{12}=\mathrm{BF}(\{1,2\})$. The size-class maxima of $p(S)m(S)$, relative to $p(\emptyset)m(\emptyset)$, are $1$, $\max(a_1,a_2)/3$ and $a_{12}/3$. If $a_1=a_2=2$ then they are $1$, $2/3$ and $a_{12}/3>4/3$ (Lemma 4.1 with $u_1u_2>0$, which holds because $a_j>1$ forces $u_j>0$). $\square$

### 4.2 The explicit instance

**Instance.** $n=10$, $x_1=(1,1,1,1,1,1,1,1,1,1)^\top$, $x_2=(1,-1,1,-1,1,-1,1,-1,1,-1)^\top$, so $X^\top X=10I_2$ (orthogonal, standardised); prior $\mathrm{BB}(1,2)$, cap $2$, hyperparameters $a_0=b_0=0.01$ (the draft's defaults), so $\nu=5.01$; and
$$
y=(3,0,-1,0,2,0,2,0,2,0)^\top .
$$

**Proposition 4.3 (Pb2).** In this instance: $z_1=z_2=8$, $u_1=u_2=6.4$, $y^\top y=22$, $A_0=22.02$, $h=100/111$, $D=111/11$,
$$
a_1=a_2=\Big(\tfrac{11}{111}\Big)^{1/2}\Big(\tfrac{22.02}{22.02-640/111}\Big)^{5.01}=1.4408\ldots,\qquad a_{12}=\tfrac{11}{111}\Big(\tfrac{22.02}{22.02-1280/111}\Big)^{5.01}=4.0721\ldots
$$
(four decimals; the exact values are the displayed closed forms). Hence:
(a) the size-class maxima of $\log\{p(S)m(S)\}$, shifted by $-\log\{p(\emptyset)m(\emptyset)\}$, are $\log1=0$, $\log(a_1/3)=\log0.4803\ldots<0$ and $\log(a_{12}/3)=\log1.3574\ldots>0$: the map $k\mapsto\max_{|S|=k}\log\{p(S)m(S)\}$ decreases from $k=0$ to $k=1$ and increases from $k=1$ to $k=2$, so it is not unimodal;
(b) the HPM is $\{1,2\}$ (its score exceeds those of $\emptyset$, $\{1\}$, $\{2\}$ strictly);
(c) forward selection from $\emptyset$ stops at $\emptyset$: both single additions lower the score ($a_1/3=a_2/3<1$), so the first step is non-improving. It misses the HPM.

*Proof.* $y$ is supported on the even positions $1,3,5,7,9$ (1-based), where both $x_1$ and $x_2$ equal $1$, so $z_1=z_2=3-1+2+2+2=8$ and $u_j=64/10$; $y^\top y=9+1+4+4+4=22$. Lemma 3.1 gives $Q_{\{j\}}=22-\tfrac{100}{111}\cdot6.4=22-\tfrac{640}{111}$ and $Q_{\{1,2\}}=22-\tfrac{1280}{111}$, and $\mathrm{BF}(S)=D^{-|S|/2}(A_0/\tilde Q_S)^\nu$ by Lemma 1.1 with $D_S=D^{|S|}$. The numerical values follow by evaluation (checked to double precision in `check_elementary_II.py`, block Pb2: $a_1=a_2=1.440812$, $a_{12}=4.072086$, $a_{12}/(a_1a_2)=1.9616$). (a)–(c): with the weights $3:1:1$ (Lemma 1.2), $p(S)m(S)/\{p(\emptyset)m(\emptyset)\}$ equals $1$, $a_1/3$, $a_2/3$, $a_{12}/3$ for $S=\emptyset,\{1\},\{2\},\{1,2\}$; the stated orderings are $1.4408<3<4.0721$. $\square$

*Remark 4.4.* (a) The instance does not have singleton Bayes factors exactly $2$ as the hint suggests; the hint's role is to show the mechanism (Corollary 4.2), and any $y$ with $\max(a_1,a_2)<3<a_{12}$ (and the maximiser of size $2$ unique) works. In the family $y=a(x_1+x_2)+r$ with $r\perp x_1,x_2$, the member $a=1$, $\|r\|^2=8$ gives $a_1=a_2=2.198$ and $a_{12}=17.28$ (script output), close to the hint. The chosen $y$ has integer entries so that it is reproducible exactly. (b) Because $a_1=a_2$, the order-first maximiser among singletons is whichever of $\{1\},\{2\}$ the fixed order prefers; this does not affect (a)–(c). (c) Since $z_1$, $z_2$, $y^\top y$ are integers and $h$, $D$ are rational, the only transcendental step is the power $\nu=5.01$; with $a_0=b_0$ replaced by any other positive defaults the same $y$ gives the same qualitative picture as long as $a_1<3<a_{12}$, which the script can re-check.

---

## 5. Example Ex1: a proxy in another block

Standing setting: (S) of Section 0.1 (regime (b)), with reading (Rd4): $p\ge3$; $1\in C_1$, $3\in C_2$, $C_1\ne C_2$; $\beta^\star=\beta e_1$ with $\beta\ne0$, so $S_0=\{1\}$ and $\mu=\beta x_1$; for every $n$, $x_1^\top x_j=0=x_3^\top x_j$ for all $j\notin\{1,3\}$; $\Gamma_{13}=r$ with $0<|r|<1$; $\Gamma_{11}=\Gamma_{33}=1$ (standardisation). Passing to the limit in (S3), $\Gamma_{1j}=\Gamma_{3j}=0$ for $j\notin\{1,3\}$, and $\Gamma\succ0$ (in particular $|r|<1$ is forced, since $\det\Gamma_{\{1,3\}}=1-r^2>0$).

Two elementary facts are used repeatedly. For a block $C$ not containing $1$ (resp. containing $1$) and the limit $\Gamma$:
$$
\Gamma_{C,1}=r\,e_3\ \text{ if }3\in C,\qquad \Gamma_{C,1}=0\ \text{ if }3\notin C\ (\text{and }1\notin C);\qquad \Gamma_{C,1}=e_1\ \text{ if }1\in C,\ 3\notin C, \tag{5.1}
$$
where $e_j$ denotes the coordinate vector of $\mathbb R^C$ at $j$. And, if $j\in\{1,3\}$ lies in $C$ while the other element of $\{1,3\}$ does not, then $e_j$ is an eigenvector of $\Gamma_{CC}$ with eigenvalue $1$:
$$
\Gamma_{CC}e_j=(\Gamma_{ij})_{i\in C}=e_j ,\qquad\text{hence}\qquad \Gamma_{CC}^{-1}e_j=e_j , \tag{5.2}
$$
because $\Gamma_{jj}=1$ and $\Gamma_{ij}=0$ for every $i\in C\setminus\{j\}$ (such $i$ is neither $1$ nor $3$). $\Gamma_{CC}\succ0$ by $\Gamma\succ0$, so the inverse exists.

### 5.1 The block-$2$ residual variances and $\tilde T_2$

**Proposition 5.1.** For every $T\subseteq C_2$,
$$
\bar\sigma^2_2(T)=\sigma_\star^2+\beta^2\big(1-r^2\,\mathbf 1\{3\in T\}\big).
$$
In particular $\bar\sigma^2_2(\emptyset)=\sigma_\star^2+\beta^2$ and $\bar\sigma^2_2(\{3\})=\sigma_\star^2+\beta^2(1-r^2)$; the population minimisers of block $2$ are exactly the $T\subseteq C_2$ with $3\in T$, and $\tilde T_2=\{3\}$.

*Proof.* $\beta^{\star\top}\Gamma\beta^\star=\beta^2\Gamma_{11}=\beta^2$. For $T=\emptyset$ this gives $\bar\sigma^2_2(\emptyset)=\sigma_\star^2+\beta^2$. For $T\ne\emptyset$, $\Gamma_{T\cdot}\beta^\star=\beta\,\Gamma_{T,1}$, which by (5.1) (with $C=T\subseteq C_2$, $1\notin T$) equals $\beta r\,e_3$ if $3\in T$ and $0$ otherwise. If $3\notin T$ the subtracted term vanishes and $\bar\sigma^2_2(T)=\sigma_\star^2+\beta^2$. If $3\in T$, by (5.2) with $C=T$, $\Gamma_{TT}^{-1}e_3=e_3$, so $\beta^{\star\top}\Gamma_{\cdot T}\Gamma_{TT}^{-1}\Gamma_{T\cdot}\beta^\star=\beta^2r^2\,e_3^\top\Gamma_{TT}^{-1}e_3=\beta^2r^2$ and $\bar\sigma^2_2(T)=\sigma_\star^2+\beta^2(1-r^2)$. Since $\beta^2r^2>0$, the minimum over $2^{C_2}$ is $\sigma_\star^2+\beta^2(1-r^2)$, attained exactly when $3\in T$; the unique minimiser of minimal cardinality is $\{3\}$, so (U) holds for block $2$ with $\tilde T_2=\{3\}$. $\square$

### 5.2 The block projections and $\tilde S_0$

**Proposition 5.2.** $\gamma_1=\beta e_1$, $\gamma_2=r\beta\,e_3$, and $\gamma_b=0$ for every block $b\notin\{1,2\}$. Consequently (F-T11(i)) $\tilde T_1=\{1\}$, $\tilde T_2=\{3\}$, $\tilde T_b=\emptyset$ otherwise, and $\tilde S_0=\{1,3\}\supsetneq S_0=\{1\}$. In particular $\gamma_{1,1}=\beta\ne0$ (variable $1$ is not cancelled) and $\gamma_{2,3}=r\beta\ne0$ (variable $3$ is a proxy).

*Proof.* $\gamma_b=\Gamma_{C_bC_b}^{-1}\Gamma_{C_b,[p]}\beta^\star=\beta\,\Gamma_{C_bC_b}^{-1}\Gamma_{C_b,1}$. For $b=1$: $3\notin C_1$ (the blocks are disjoint and $3\in C_2\ne C_1$), so by (5.1) $\Gamma_{C_1,1}=e_1$ and by (5.2) $\Gamma_{C_1C_1}^{-1}e_1=e_1$: $\gamma_1=\beta e_1$. For $b=2$: $1\notin C_2$, $3\in C_2$, so $\Gamma_{C_2,1}=re_3$ and $\Gamma_{C_2C_2}^{-1}e_3=e_3$: $\gamma_2=r\beta e_3$. For other $b$, $1,3\notin C_b$ and $\Gamma_{C_b,1}=0$. T11(i) identifies $\tilde T_b=\operatorname{supp}(\gamma_b)$ (this also re-proves $\tilde T_2=\{3\}$ and shows that (U) holds in every block), and $\tilde S_0=\bigcup_b\tilde T_b=\{1,3\}$. $\square$

### 5.3 The constant $\kappa_0$

**Proposition 5.3.** $\kappa_0=\tfrac12\log\dfrac{\sigma_\star^2+\beta^2}{\sigma_\star^2+\beta^2(1-r^2)}>0$.

*Proof.* $\kappa_0=\tfrac12\sum_b\log\{\bar\sigma^2_b(S_0\cap C_b)/\bar\sigma^2_b(\tilde T_b)\}$. Block $1$: $S_0\cap C_1=\{1\}=\tilde T_1$, term $0$. Block $2$: $S_0\cap C_2=\emptyset$, $\tilde T_2=\{3\}$, term $\tfrac12\log\{\bar\sigma^2_2(\emptyset)/\bar\sigma^2_2(\{3\})\}$ with the two values of Proposition 5.1. Every other block: $S_0\cap C_b=\emptyset=\tilde T_b$, term $0$. The ratio exceeds $1$ because $\beta^2r^2>0$. $\square$

### 5.4 The switch is a single deletion; what needs (R)

**Proposition 5.4.** Under (S):
(a) no true variable is cancelled, $S_0\setminus\tilde S_0=\emptyset$ and $\tilde S_0\setminus S_0=\{3\}$ (F-T11(ii)); the net change from $\tilde S_0$ to $S_0$ is one deletion and no addition (F-T11(iii), first clause);
(b) $\Delta_0(n)/n\to\kappa_0>0$ in probability (F-T3(ii)), and $\log\{\pi(S_0)/\pi(\tilde S_0)\}=\tfrac12\log n+O_{\mathbb P}(1)$ (F-T3(iv), second case, as $\tilde S_0\supsetneq S_0$ with $|\tilde S_0|-|S_0|=1$); $\pi(S_0)\to1$ in probability (F-T3(i), posterior half).
Under (S) and (R) in addition: $\pi_0(\tilde S_0)\to1$ in probability (F-T3(i), start half), so $\pi_0(S_0)=\pi_0(\tilde S_0)e^{-\Delta_0(n)}=\exp\{-\kappa_0n(1+o_{\mathbb P}(1))\}$: the bridge must move the mass from $\{1,3\}$ to $\{1\}$, and the incoming mode's start mass is exponentially small while the posterior's preference for it is only $\tfrac12\log n+O_{\mathbb P}(1)$. A sufficient condition for (R) is $\|\Gamma_n-\Gamma\|=O(n^{-1/2})$ (F-R), e.g. $\Gamma_n=\Gamma$ for all $n$.

*Proof.* (a) is Proposition 5.2 read through T11(ii)–(iii). (b) and the last paragraph are the cited parts of T3 applied with $\tilde S_0=\{1,3\}$, $S_0=\{1\}$ and $\kappa_0$ from Proposition 5.3, under the hypotheses indicated in (F-T3). $\square$

*Remark 5.5 (what "as T11(iii) predicts" means).* T11(iii) is a statement about the endpoints $\tilde S_0$ and $S_0$: without cancellation the start's mode contains $S_0$, and the net change is deletions only; here exactly one. T11(iii) does not say that a single move of a local kernel crosses the switch; that is Problem Pb4, as the example says. Also, T3 says nothing about the modes of the intermediate bridge; `proofs/T3_T11` Remark 6.0 shows that an intermediate mode can add a variable in a related example. Neither remark affects Ex1's claims.

### 5.5 Aligned blocks remove the switch

**Proposition 5.6.** Suppose the partition is changed so that $1$ and $3$ lie in the same block $C'$ (the other blocks arbitrary), everything else as above. Then $\Gamma_{C_b,C_b^c}\beta^\star_{C_b^c}=0$ for every block $b$; hence (F-T11(iii), last clause) $\gamma_b=\beta^\star_{C_b}$ for every $b$, $\tilde S_0=S_0=\{1\}$ and $\kappa_0=0$. Under (R) in addition, $\pi_0(S_0)\to1$ and $\pi(S_0)\to1$ (F-T3(i)), hence $\inf_{\phi\in[0,1]}q_\phi(S_0)\to1$ (Lemma L3): there is no switch.

*Proof.* For the block $C'\ni1$: $\beta^\star_{C'^c}=0$ since $\operatorname{supp}\beta^\star=\{1\}\subseteq C'$, so $\Gamma_{C',C'^c}\beta^\star_{C'^c}=0$. For any other block $C_b$: $1\notin C_b$, so $\Gamma_{C_b,C_b^c}\beta^\star_{C_b^c}=\beta\,\Gamma_{C_b,1}$, and $\Gamma_{C_b,1}=0$ because $C_b$ contains neither $1$ nor $3$ (both are in $C'$) and column $1$ is uncorrelated with every column other than $3$. This is the no-leakage condition of T11(iii), whose last clause gives $\gamma_b=\beta^\star_{C_b}$ and $\tilde S_0=S_0$. Then $\kappa_0=0$ since every term has $S_0\cap C_b=\tilde T_b$. The rest is T3(i) and L3 (draft, with $S^\ast=S_0$, $p(S_0)>0$). $\square$

*Remark 5.7 (direct check of Proposition 5.6 without T11).* With $C'\ni1,3$, $\gamma_{C'}=\beta\Gamma_{C'C'}^{-1}\Gamma_{C',1}=\beta\Gamma_{C'C'}^{-1}(\Gamma_{C'C'}e_1)=\beta e_1$ since $\Gamma_{C',1}$ is the column of $\Gamma_{C'C'}$ indexed by $1$. So $\operatorname{supp}\gamma_{C'}=\{1\}$ directly.

*Numerical check (Section 9, block Ex1).* With $p=5$, blocks $\{1,2\},\{3,4\},\{5\}$, $r=0.6$, $\beta=1.3$, $\sigma_\star^2=1$ and additional correlations among columns $2,4,5$: Propositions 5.1–5.3 and 5.6 verified to machine precision; with $\Gamma_n=\Gamma$ exactly, one draw per $n$, $\Delta_0(n)/n=0.1258$ at $n=3200$ against $\kappa_0=0.1282$, the start's mode is $\{1,3\}$ and the posterior's mode is $\{1\}$ at every $n\in\{50,200,800,3200\}$, and $\log\{\pi(S_0)/\pi(\tilde S_0)\}-\tfrac12\log n$ stays within $[-0.2,1.4]$.

---

## 6. Corollary C1: no marginal-correlation condition

### 6.1 Part (i)

**Theorem 6.1 (C1(i)).** Let $\mathcal H$ denote the union of the hypotheses of T6, T7, T8, T9, T9a, C9 and T10 as they are listed in the proofs (`proofs/T6/PROOF.md` Sections 0 and 7; `proofs/T7_T8/PROOF.md` Sections 0.1 and 6.1; `proofs/T9_C9/PROOF.md` Sections 0, 7.1, 8 and 9). Then:
(a) every hypothesis in $\mathcal H$ is a condition on one of the following: the integers $n,p,s_0$ and the constant $A$ (e.g. $p\le n^A$, $s_0$ fixed, $\ell_n^2=o(n)$); the model prior ($\mathrm{BB}(1,p)$, $k_{\max}\ge s_0$, in T9a(iii) $k_{\max}\ge m_n+s_0$); the hyperparameters $a_0,b_0>0$; the signal size $\|\mu\|^2/n\le M$; eigenvalues of principal submatrices of $\Gamma_n$ ($\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2$; (SE) up to size $m_n+s_0$) or, for C9, of $\Sigma_x$, together with centring and a uniform sub-Gaussian constant for the rows and $\beta^{\star\top}\Sigma_x\beta^\star\le M/2$; the column norms ($\|x_j\|^2=n$, used only in Section 9 of `proofs/T9_C9`); the magnitudes of the true coefficients (beta-min in T8, (BM); the set $J_n$ in T10); and the error law $\varepsilon\sim N_n(0,\sigma_\star^2I)$;
(b) none of them mentions, or is a function of, the marginal covariances $x_j^\top y/n$, their means $x_j^\top\mu/n=(\Gamma_n\beta^\star)_j$, or the block projections $\gamma_b$ (nor any partition into blocks: none of T6–T10 refers to the blocks);
(c) the hypotheses do not force $x_j^\top\mu\ne0$ for $j\in S_0$: the design of C1(ii) (Section 6.2) satisfies every hypothesis of T6, T7, T8, T9, T9a(i)–(iii) and T10 and has $x_1^\top\mu=0$ for every $n$ with $1\in S_0$; and there $x_1^\top y/n=x_1^\top\varepsilon/n\sim N(0,\sigma_\star^2/n)\to0$ in probability, so the sample marginal covariance also vanishes asymptotically.
Hence T6–T10 hold when a true variable is marginally uncorrelated with the response.

*Proof.* (a)–(b) are read off the hypothesis lists cited; they are reproduced here for the record.
- T6 (`proofs/T6`, Section 0 "Standing assumptions", Section 7): $n\ge2$, $p\ge1$, $s_0$ fixed, $p\le n^A$ (used only for $m_n=O(\log n)$), $\mathrm{BB}(1,p)$ with $k_{\max}\ge s_0$, $\|\mu\|^2/n\le M$, $\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2$, $a_0,b_0,\sigma_\star^2,M,\varphi_0$ fixed; the design enters only through $\delta=(\|\mu\|^2+\|\beta^\star_{S_0}\|^2)/n$.
- T7, T8, T10 (`proofs/T7_T8`, Section 0.1): (A1) $s_0$ fixed, $p\le n^A$; (A2) $\mathrm{BB}(1,p)$, $k_{\max}\ge s_0$; (A3) $\|\mu\|^2\le nM$; (A4) $\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2$; (SE) $\lambda_{\min}(\Gamma_S)\ge\varphi_0^2$ for $|S|\le m_n+s_0$; $\omega_n\to\infty$, $\omega_n=O(\log n)$; for T8, (BM) $\min_{j\in S_0}\beta_j^{\star2}\ge M_n^\beta\sigma_\star^2\log n/(n\varphi_0^2)$; for T10 the set $J_n$; $a_0,b_0>0$ (Section 6.1, item 4).
- T9, T9a (`proofs/T9_C9`, Section 0 and Section 8 items 1–3, 5): $n\ge4$, $s_0$ fixed, $\mathrm{BB}(1,p)$ with $k_{\max}\ge s_0$, $\|\mu\|^2/n\le M$, $\lambda_{\min}(\Gamma_{S_0})\ge\varphi_0^2$, $\ell_n^2=o(n)$ for T9(ii); for T9a(iii) in Section 9: $p\le n^A$, standardised columns, (SE) up to $m_n+s_0$, $k_{\max}\ge m_n+s_0$.
- C9 (`proofs/T9_C9`, Section 7.1 and Section 8 item 4): i.i.d. centred rows with a sub-Gaussian constant uniform in $n$, covariance $\Sigma_x$ with $\kappa\le\lambda_{\min}(\Sigma_{x,TT})\le\lambda_{\max}(\Sigma_{x,TT})\le K$ for $|T|\le m_n+s_0$, $\beta^{\star\top}\Sigma_x\beta^\star\le M/2$, $s_0$ fixed, $\ell_n^2=o(n)$, $\mathrm{BB}(1,p)$ with $k_{\max}\ge s_0$, rows independent of $\varepsilon$.
Each item is of one of the kinds listed in (a); none involves $x_j^\top y$, $x_j^\top\mu$ or $\gamma_b$ (in the random design of C9 the population marginal covariance is $(\Sigma_x\beta^\star)_j$, and the hypotheses bound only quadratic forms and eigenvalues of $\Sigma_x$, not the entries of $\Sigma_x\beta^\star$). (c) is Proposition 6.3 below together with $x_1^\top y=x_1^\top\mu+x_1^\top\varepsilon=x_1^\top\varepsilon\sim N(0,\sigma_\star^2\|x_1\|^2)=N(0,n\sigma_\star^2)$. $\square$

*Remark 6.2.* (a) The draft attributes the condition "$|\mathrm{cov}(x_j,y)|>0$ for all $j\in S_0$" to Song and Liang (2015, Condition 5). That source was not consulted in this thread; the attribution is the draft's and is marked **unverified** here (CITED_RESULTS.md). The mathematical content of C1(i) does not depend on it. (b) A warning on scope: C1(i) says that no marginal-correlation condition is *imposed*; it does not say that a marginally uncorrelated true variable is *easy* for the composite start. Part (ii) shows the opposite: such a variable is cancelled in a singleton block and the start misses it (by a polynomial factor).

### 6.2 Part (ii): the example

Setting: $p=2$, $X_n$ with $X_n^\top X_n=n\Gamma$ exactly for every $n\ge2$, $\Gamma=\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix}$, $\rho\in(0,1)$ (realisable by Lemma 1.3; $\Gamma\succ0$ since $\det\Gamma=1-\rho^2>0$, eigenvalues $1\pm\rho$); $\beta^\star=(-\rho\beta,\beta)$ with $\beta\ne0$, so $S_0=\{1,2\}$, $s_0=2$; $\mu=X\beta^\star$; prior $\mathrm{BB}(1,2)$ with the operational cap $\lfloor n/2\rfloor$, which equals $2=p$ for $n\ge4$ (reading (Rd7)); $a_0,b_0>0$, $\sigma_\star^2>0$ fixed; singleton blocks $C_1=\{1\}$, $C_2=\{2\}$ unless said otherwise.

**Proposition 6.3 (the deterministic identities).** For every $n$:
(a) $x_1^\top\mu=n(\Gamma\beta^\star)_1=n(-\rho\beta+\rho\beta)=0$, and $x_2^\top\mu=n(\Gamma\beta^\star)_2=n\beta(1-\rho^2)\ne0$;
(b) $\|\mu\|^2/n=\beta^{\star\top}\Gamma\beta^\star=\beta^2(1-\rho^2)$;
(c) $\bar\sigma^2_n(T)=\bar\sigma^2(T)$ for every $T$ (since $\Gamma_n=\Gamma$), with
$\bar\sigma^2(\emptyset)=\bar\sigma^2(\{1\})=\sigma_\star^2+\beta^2(1-\rho^2)$, $\bar\sigma^2(\{2\})=\sigma_\star^2+\beta^2\rho^2(1-\rho^2)$, $\bar\sigma^2(\{1,2\})=\sigma_\star^2$;
(d) with singleton blocks, $\gamma_1=(\Gamma\beta^\star)_1=0$ and $\gamma_2=(\Gamma\beta^\star)_2=\beta(1-\rho^2)\ne0$; with the single block $\{1,2\}$, $\gamma=\Gamma^{-1}\Gamma\beta^\star=\beta^\star$;
(e) $\lambda_{\min}(\Gamma_S)\ge1-\rho$ for every $S\subseteq[2]$ ($\Gamma_{\{j\}}=1$, $\lambda_{\min}(\Gamma)=1-\rho$).

*Proof.* (a) $\Gamma\beta^\star=(-\rho\beta+\rho\beta,\ -\rho^2\beta+\beta)=(0,\beta(1-\rho^2))$, and $x_j^\top\mu=(X^\top X\beta^\star)_j=n(\Gamma\beta^\star)_j$. (b) $\beta^{\star\top}\Gamma\beta^\star=\beta^{\star\top}(0,\beta(1-\rho^2))=\beta^2(1-\rho^2)$. (c) $\bar\sigma^2(\emptyset)=\sigma_\star^2+\beta^2(1-\rho^2)$ by (b). $\bar\sigma^2(\{j\})=\bar\sigma^2(\emptyset)-(\Gamma_{j\cdot}\beta^\star)^2/\Gamma_{jj}=\bar\sigma^2(\emptyset)-(\Gamma\beta^\star)_j^2$: for $j=1$ the subtracted term is $0$; for $j=2$ it is $\beta^2(1-\rho^2)^2$, and $\beta^2(1-\rho^2)-\beta^2(1-\rho^2)^2=\beta^2(1-\rho^2)\rho^2$. $\bar\sigma^2(\{1,2\})=\sigma_\star^2$ by (F-geo)(c) since $\{1,2\}\supseteq S_0$. (d) $\gamma_b=\Gamma_{bb}^{-1}\Gamma_{b,[2]}\beta^\star=(\Gamma\beta^\star)_b$ for singleton blocks, by (a); for the single block, $\gamma=\Gamma^{-1}\Gamma\beta^\star=\beta^\star$. (e) Direct. $\square$

**Proposition 6.4 (hypotheses of T8, hence $\Pi(S_0\mid y)\to1$).** The hypotheses of Theorem 8.1 of `proofs/T7_T8/PROOF.md` hold with $A=1$, $M=\beta^2(1-\rho^2)$, $\varphi_0^2=1-\rho$, any $\omega_n\to\infty$ with $\omega_n=O(\log n)$ (e.g. $\omega_n=\tfrac12\log n$), and $M_n^\beta=\rho^2\beta^2(1-\rho)\,n/(2\sigma_\star^2\log n)$. Consequently $\Pi(S_0\mid y)\to1$ in $\mathbb P_0$-probability; with $\omega_n=\tfrac12\log n$, $1-\Pi(S_0\mid y)=O_{\mathbb P}(\sqrt{\log n/n})$ and $\mathbb P_0(\mathrm{HPM}\ne S_0)\to0$.

*Proof.* (A1): $s_0=2$ fixed and $p=2\le n=n^1$ for $n\ge2$. (A2): $\mathrm{BB}(1,2)$ with $k_{\max}=\lfloor n/2\rfloor\ge2=s_0$ for $n\ge4$. (A3): $\|\mu\|^2=n\beta^2(1-\rho^2)=nM$ (Proposition 6.3(b)). (A4) and (SE): every $S\subseteq[2]$ has $\lambda_{\min}(\Gamma_S)\ge1-\rho=\varphi_0^2>0$ (Proposition 6.3(e)), whatever $m_n$ is. (BM): $\min_j\beta_j^{\star2}=\min(\rho^2\beta^2,\beta^2)=\rho^2\beta^2$, and $M_n^\beta\sigma_\star^2\log n/(n\varphi_0^2)=\rho^2\beta^2/2<\rho^2\beta^2$ with the stated $M_n^\beta\to\infty$. Columns are standardised and $a_0,b_0>0$. Theorem 8.1(i)–(iii) there give the conclusions. $\square$

**Proposition 6.5 (hypotheses of T11 and T3; (U), (R)).** (a) The setting (S) holds: $p=2$, the partition, $\beta^\star$, $\sigma_\star^2$, $a_0,b_0$ are fixed; the prior is $\mathrm{BB}(1,2)$, a fixed size-only prior with $w(k)>0$ for $k\le2$ (Lemma 1.2), and the cap $\lfloor n/2\rfloor\ge p$ for $n\ge4$; columns are standardised and $\Gamma_n=\Gamma\succ0$. Hence T11(i)–(iii) and T3(ii), (iv) apply.
(b) (U) holds (automatic under (S)); with singleton blocks $\tilde T_1=\operatorname{supp}(\gamma_1)=\emptyset$, $\tilde T_2=\operatorname{supp}(\gamma_2)=\{2\}$, so $\tilde S_0=\{2\}$; variable $1$ is cancelled and there is no proxy: $S_0\setminus\tilde S_0=\{1\}$, $\tilde S_0\setminus S_0=\emptyset$ (T11(ii)).
(c) (R) holds. Block $1$: the only $T\subseteq C_1$ with $T\ne\tilde T_1=\emptyset$ is $T=\{1\}$, a population minimiser ($\bar\sigma^2(\{1\})=\bar\sigma^2(\emptyset)$) and a strict superset of $\tilde T_1$, so (R1) applies to it and requires $n[\bar\sigma^2_n(\{1\})-\bar\sigma^2_n(\emptyset)]=O(1)$; by (F-geo)(1.7) this quantity is $-\|P_{\{1\}}\mu\|^2=-(x_1^\top\mu)^2/n=0$ for every $n$ (Proposition 6.3(a)). Block $2$: the only $T\ne\tilde T_2=\{2\}$ is $T=\emptyset$, not a population minimiser, so (R2) applies and requires $n[\bar\sigma^2_n(\emptyset)-\bar\sigma^2_n(\{2\})]\ge\omega_n\log n$; by Proposition 6.3(c) the left side is $n\beta^2(1-\rho^2)^2$, so $\omega_n:=\beta^2(1-\rho^2)^2n/\log n\to\infty$ works. (Alternatively: $\|\Gamma_n-\Gamma\|=0=O(n^{-1/2})$ and (F-R).) Hence T3(i) and (iii) also apply.
(d) $\kappa_0=\tfrac12\big[\log\{\bar\sigma^2_1(\{1\})/\bar\sigma^2_1(\emptyset)\}+\log\{\bar\sigma^2_2(\{2\})/\bar\sigma^2_2(\{2\})\}\big]=0$, and $\kappa_1=\tfrac12\log\{\bar\sigma^2(\tilde S_0)/\sigma_\star^2\}=\tfrac12\log\big(1+\beta^2\rho^2(1-\rho^2)/\sigma_\star^2\big)>0$.

*Proof.* (a) is a list check against (S1)–(S4) of Section 0.1. (b) is Proposition 6.3(d) with T11(i)–(ii). (c) as written; note that the note's reason, "the cancellation is exact at every $n$", is exactly what makes the (R1) gap vanish identically, while (R2) uses only that $\Gamma_n=\Gamma$ (indeed only $\Gamma_n\to\Gamma$, by Remark 5.1 of `proofs/T3_T11`). (d) $S_0\cap C_1=\{1\}$, $\tilde T_1=\emptyset$ and $\bar\sigma^2(\{1\})=\bar\sigma^2(\emptyset)$; $S_0\cap C_2=\{2\}=\tilde T_2$. $\kappa_1$ from Proposition 6.3(c). $\square$

**Theorem 6.6 (C1(ii)).** In the setting above, in $\mathbb P_0$-probability:
(a) $x_1^\top\mu=0$ for every $n$ and $\Pi(S_0\mid y)\to1$ (Propositions 6.3(a), 6.4);
(b) with singleton blocks, $\tilde S_0=\{2\}$, variable $1$ is cancelled, $\kappa_0=0$ (Proposition 6.5);
(c) $\Delta_0(n)=\log\{\pi_0(\{2\})/\pi_0(\{1,2\})\}=\tfrac12\log n+O_{\mathbb P}(1)$ (T3(iii): $\kappa_0=0$, $\tilde S_0\ne S_0$, $|S_0|-|\tilde S_0|=1$), and $\pi_0(\tilde S_0)\to1$ (T3(i) under (R)); hence $\pi_0(S_0)=n^{-1/2}e^{-O_{\mathbb P}(1)}$: the start misses variable $1$ by a polynomial factor only;
(d) the switch is a single addition: $S_0\setminus\tilde S_0=\{1\}$, $\tilde S_0\setminus S_0=\emptyset$; moreover $\tfrac1n\log\{\pi(S_0)/\pi(\tilde S_0)\}\to\kappa_1>0$ (T3(iv), first case, since $\tilde S_0\not\supseteq S_0$);
(e) with both variables in one block, $\gamma=\beta^\star$, $\tilde S_0=S_0$, $\kappa_0=0$, and $\pi_0(S_0)\to1$, $\pi(S_0)\to1$: no switch.

*Proof.* (a)–(d): assembled from Propositions 6.3–6.5 and the cited parts of T3 and T11, whose hypotheses were verified in Proposition 6.5. In (c), $\pi_0(S_0)=\pi_0(\tilde S_0)e^{-\Delta_0(n)}$ with $\pi_0(\tilde S_0)\to1$ gives $\log\pi_0(S_0)=-\tfrac12\log n+O_{\mathbb P}(1)$. (e): with the single block, the start is $\pi_0(S)\propto p(S)\mathrm{BF}(S)=\pi(S)$ exactly (one block, $r(S)=\mathrm{BF}(S)$), so $\pi_0=\pi$ and $\pi(S_0)\to1$ by (a); T11(iii)'s last clause gives the same through $\gamma=\beta^\star$ (no leakage, as $C^c=\emptyset$). $\square$

*Remark 6.7 (the note's remaining sentences).* (a) "By T4, the bridge needs about $\log_2\log\sqrt n$ stages for this switch": T4(ii) concerns the two-state model with start deficit $\Delta_0$; with $\Delta_0=\tfrac12\log n+O_{\mathbb P}(1)$ it gives $T=\log_2\Delta_0+O(1)=\log_2\log\sqrt n+O(1)$ stages *for the two-state reduction*. The passage from the regression bridge to the two-state model is Problem Pb3; so the sentence is a heuristic consequence of T4, not a theorem about this example. (b) The last sentence (single-site Gibbs proposes the addition directly) is a description of the kernel, not a claim about its acceptance probability, which is Pb4.

*Numerical check (Section 9, block C1).* $\rho=0.7$, $\beta=\sigma_\star=1$: the identities of Proposition 6.3 verified to machine precision; with $\Gamma_n=\Gamma$ exactly and one draw per $n\in\{50,\dots,12800\}$, $x_1^\top\mu=0$ to rounding, the start's mode is $\{2\}$ and the posterior's mode is $\{1,2\}$ at every $n$, $\Delta_0(n)-\tfrac12\log n\in[-0.94,-0.09]$, and $\tfrac1n\log\{\pi(S_0)/\pi(\tilde S_0)\}\in[0.10,0.14]$ against $\kappa_1=0.1115$.

---

## 7. Example Ex2: a split cancelling pair

Standing setting: (S) of Section 0.1 with $p=2$, $C_1=\{1\}$, $C_2=\{2\}$, $\beta^\star=(\beta,-\beta)$ with $\beta\ne0$ (so $S_0=\{1,2\}$), $\Gamma=\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix}$ with $\rho\in(0,1)$ ($\Gamma\succ0$), $\sigma_\star^2,a_0,b_0>0$ fixed, prior $\mathrm{BB}(1,2)$, cap $2$ (reading (Rd5)). Sections 7.4–7.6 assume in addition $\Gamma_n=\Gamma$ exactly for every $n\ge2$ (realisable by Lemma 1.3). Abbreviations:
$$
\bar\sigma^2_\emptyset:=\bar\sigma^2(\emptyset),\qquad \bar\sigma^2_1:=\bar\sigma^2(\{1\}),\qquad \kappa_{\rm pair}=\tfrac12\log\frac{\bar\sigma^2_\emptyset}{\bar\sigma^2_1},\qquad L=\log\frac{\bar\sigma^2_\emptyset}{\sigma_\star^2},\qquad a_j=\mathrm{BF}(\{j\}),\quad a_{12}=\mathrm{BF}(\{1,2\}).
$$

### 7.1 The identities, $\tilde S_0=S_0$ and $\kappa_0=0$

**Proposition 7.1.** (a) $\bar\sigma^2(\emptyset)=\sigma_\star^2+2\beta^2(1-\rho)$; $\bar\sigma^2(\{1\})=\bar\sigma^2(\{2\})=\sigma_\star^2+\beta^2(1-\rho^2)$; $\bar\sigma^2(\{1,2\})=\sigma_\star^2$. Hence $L=\log(1+2\beta^2(1-\rho)/\sigma_\star^2)$, as in the draft.
(b) $\gamma_1=\beta(1-\rho)\ne0$ and $\gamma_2=-\beta(1-\rho)\ne0$: no true variable is cancelled, $\tilde T_1=\{1\}$, $\tilde T_2=\{2\}$, $\tilde S_0=S_0$, and $\kappa_0=0$.
(c) $\kappa_{\rm pair}>0$ for every $\rho\in(0,1)$, and $\kappa_{\rm pair}\to0$ as $\rho\uparrow1$. By (F-rate), $\tfrac1n\log a_j\to\kappa_{\rm pair}$ in probability: $\kappa_{\rm pair}$ is the exponential rate of each block's Bayes factor, the "per-block log-gain".

*Proof.* (a) $\Gamma\beta^\star=(\beta-\rho\beta,\ \rho\beta-\beta)=\beta(1-\rho)(1,-1)$, so $\beta^{\star\top}\Gamma\beta^\star=\beta(1-\rho)(\beta+\beta)=2\beta^2(1-\rho)$, which gives $\bar\sigma^2(\emptyset)$. For a singleton, $\bar\sigma^2(\{j\})=\bar\sigma^2(\emptyset)-(\Gamma\beta^\star)_j^2/\Gamma_{jj}=\sigma_\star^2+2\beta^2(1-\rho)-\beta^2(1-\rho)^2=\sigma_\star^2+\beta^2(1-\rho)(1+\rho)$. $\bar\sigma^2(\{1,2\})=\sigma_\star^2$ by (F-geo)(c). (b) $\gamma_j=\Gamma_{jj}^{-1}\Gamma_{j,[2]}\beta^\star=(\Gamma\beta^\star)_j$; T11(i)–(ii). $\kappa_0=0$ since $S_0\cap C_b=\tilde T_b$ for both blocks. (c) $\bar\sigma^2_\emptyset-\bar\sigma^2_1=\beta^2(1-\rho)^2>0$ gives $\kappa_{\rm pair}>0$; both variances tend to $\sigma_\star^2$ as $\rho\uparrow1$. (F-rate) with $T=\{j\}$, $T'=\emptyset$ gives the limit $-\tfrac12\log(\bar\sigma^2_1/\bar\sigma^2_\emptyset)=\kappa_{\rm pair}$. $\square$

### 7.2 The exact finite-sample switch conditions

**Proposition 7.2 (Ex2, exact conditions).** Fix $y\in\mathbb R^n$ and the design. With weights $w(0):w(1):w(2)=3:1:1$ (Lemma 1.2), the start and the posterior are, up to normalisation,
$$
\gamma_0(\emptyset):\gamma_0(\{1\}):\gamma_0(\{2\}):\gamma_0(\{1,2\})=3:a_1:a_2:a_1a_2,\qquad
p\,\mathrm{BF}(\emptyset):p\,\mathrm{BF}(\{1\}):p\,\mathrm{BF}(\{2\}):p\,\mathrm{BF}(\{1,2\})=3:a_1:a_2:a_{12}.
$$
Consequently: $\emptyset$ is the unique maximiser of $\gamma_0$ **and** $\{1,2\}$ is the unique maximiser of $p\cdot\mathrm{BF}$ if and only if
$$
\max(a_1,a_2)<3,\qquad a_1a_2<3,\qquad a_{12}>\max(3,a_1,a_2).
$$
Separately: $\emptyset$ is the unique start mode iff the first two inequalities hold; $\{1,2\}$ is the unique posterior mode iff the third holds.

*Proof.* With singleton blocks, $r_b(\emptyset)=\mathrm{BF}(\emptyset)=1$ and $r_b(\{j\})=a_j$, so $r(S)=\prod_{j\in S}a_j$ and $\gamma_0(S)=p(S)r(S)=w(|S|)r(S)/W$; multiply by $W/w(1)=6W$ and use Lemma 1.2 to get the first display. The second is $p(S)\mathrm{BF}(S)=w(|S|)\mathrm{BF}(S)/W$ with $\mathrm{BF}(\emptyset)=1$. The maximiser statements are the comparisons of the four numbers in each display: $\emptyset$ is the unique maximiser of the first iff $3>a_1$, $3>a_2$ and $3>a_1a_2$; $\{1,2\}$ is the unique maximiser of the second iff $a_{12}>3$, $a_{12}>a_1$ and $a_{12}>a_2$. $\square$

*Remark.* The conjunction is strictly stronger than $\max(a_1,a_2)<3<a_{12}$: e.g. $a_1=a_2=2$ gives $a_1a_2=4>3$ and the start's mode is $\{1,2\}$ although each singleton is below $3$. Nothing is assumed about $y$; the conditions are exact for every $y$, every $n$ and every design.

### 7.3 The equivalence, and a strengthening

**Proposition 7.3.** (a) $L>4\kappa_{\rm pair}\iff\bar\sigma^2_1(\{1\})^2>\bar\sigma^2_1(\emptyset)\,\sigma_\star^2$.
(b) For every $\rho\in(0,1)$, $\beta\ne0$ and $\sigma_\star^2>0$,
$$
\bar\sigma^2_1(\{1\})^2-\bar\sigma^2_1(\emptyset)\,\sigma_\star^2=2\sigma_\star^2\beta^2\rho(1-\rho)+\beta^4(1-\rho^2)^2>0 .
$$
So the inequality of (a) holds for **every** $\rho\in(0,1)$, not only for $\rho$ near $1$; both sides of $L>4\kappa_{\rm pair}$ tend to $0$ as $\rho\uparrow1$.

*Proof.* (a) $L=\log(\bar\sigma^2_\emptyset/\sigma_\star^2)$ and $4\kappa_{\rm pair}=2\log(\bar\sigma^2_\emptyset/\bar\sigma^2_1)=\log(\bar\sigma^{4}_\emptyset/\bar\sigma^{4}_1)$. Since $\log$ is increasing and all quantities are positive, $L>4\kappa_{\rm pair}\iff\bar\sigma^2_\emptyset/\sigma_\star^2>\bar\sigma^4_\emptyset/\bar\sigma^4_1\iff\bar\sigma^4_1>\bar\sigma^2_\emptyset\sigma_\star^2$. (b) Expand with Proposition 7.1(a): $\bar\sigma^4_1=\sigma_\star^4+2\sigma_\star^2\beta^2(1-\rho^2)+\beta^4(1-\rho^2)^2$ and $\bar\sigma^2_\emptyset\sigma_\star^2=\sigma_\star^4+2\sigma_\star^2\beta^2(1-\rho)$; the difference is $2\sigma_\star^2\beta^2[(1-\rho^2)-(1-\rho)]+\beta^4(1-\rho^2)^2=2\sigma_\star^2\beta^2(1-\rho)\rho+\beta^4(1-\rho^2)^2$, a sum of two positive terms. $\square$

### 7.4 A precise second-order expansion of $\log a_j$ and $\log a_{12}$

In this subsection $\Gamma_n=\Gamma$ exactly for every $n$. Put
$$
G_n:=\frac{\mu^\top\varepsilon}{\sqrt n},\qquad G^{(j)}_n:=\frac{\mu^\top P_{\{j\}}\varepsilon}{\sqrt n}\ (j=1,2),\qquad W_n:=\sqrt n\Big(\frac{\|\varepsilon\|^2}{n}-\sigma_\star^2\Big),
$$
and the constants
$$
c_1:=\tfrac12\Big(\frac1{\bar\sigma^2_\emptyset}-\frac1{\bar\sigma^2_1}\Big)<0,\qquad c_2:=\frac1{\bar\sigma^2_1}>0,\qquad d_1:=\frac1{\bar\sigma^2_\emptyset}>0,\qquad d_2:=\tfrac12\Big(\frac1{\bar\sigma^2_\emptyset}-\frac1{\sigma_\star^2}\Big)<0 .
$$

**Lemma 7.4.1 (the ingredients and their joint limit).** (a) $\|\mu\|^2=n(\bar\sigma^2_\emptyset-\sigma_\star^2)$, $\|P_{\{j\}}\mu\|^2=n(\Gamma\beta^\star)_j^2=n\beta^2(1-\rho)^2=n(\bar\sigma^2_\emptyset-\bar\sigma^2_1)$, and $P_{\{1,2\}}\mu=\mu$.
(b) $(G_n,G^{(1)}_n,G^{(2)}_n)$ is a centred Gaussian vector whose covariance matrix does not depend on $n$:
$\operatorname{Var}G_n=\sigma_\star^2(\bar\sigma^2_\emptyset-\sigma_\star^2)$, $\operatorname{Var}G^{(j)}_n=\operatorname{Cov}(G_n,G^{(j)}_n)=\sigma_\star^2(\bar\sigma^2_\emptyset-\bar\sigma^2_1)$, $\operatorname{Cov}(G^{(1)}_n,G^{(2)}_n)=-\rho\,\sigma_\star^2\beta^2(1-\rho)^2$.
(c) $(G_n,G^{(1)}_n,G^{(2)}_n,W_n)\Rightarrow(G,G^{(1)},G^{(2)},W)$, where $(G,G^{(1)},G^{(2)})$ has the law in (b) and $W\sim N(0,2\sigma_\star^4)$ is independent of it.

*Proof.* (a) $\|\mu\|^2=n\beta^{\star\top}\Gamma\beta^\star$ and Proposition 7.1(a). $\|P_{\{j\}}\mu\|^2=(x_j^\top\mu)^2/\|x_j\|^2=(n(\Gamma\beta^\star)_j)^2/n=n\beta^2(1-\rho)^2$, and $\bar\sigma^2_\emptyset-\bar\sigma^2_1=2\beta^2(1-\rho)-\beta^2(1-\rho^2)=\beta^2(1-\rho)^2$. $\mu=X\beta^\star\in\operatorname{col}(X_{\{1,2\}})$.
(b) Each coordinate is $v^\top\varepsilon/\sqrt n$ for a fixed vector $v\in\{\mu,P_{\{1\}}\mu,P_{\{2\}}\mu\}$; the vector is Gaussian and centred with $\operatorname{Cov}(v^\top\varepsilon,v'^\top\varepsilon)/n=\sigma_\star^2v^\top v'/n$. Now $\mu^\top P_{\{j\}}\mu=\|P_{\{j\}}\mu\|^2$ (projection), and $(P_{\{1\}}\mu)^\top(P_{\{2\}}\mu)=\frac{(x_1^\top\mu)(x_2^\top\mu)(x_1^\top x_2)}{\|x_1\|^2\|x_2\|^2}=\frac{n(\Gamma\beta^\star)_1\cdot n(\Gamma\beta^\star)_2\cdot n\rho}{n^2}=n\rho\,\beta(1-\rho)\cdot(-\beta(1-\rho))$. Divide by $n$ and use (a).
(c) Let $V=\operatorname{span}\{\mu,P_{\{1\}}\mu,P_{\{2\}}\mu\}\subseteq\operatorname{col}(X)$, $d=\dim V\le2$, and decompose $\varepsilon=P_V\varepsilon+(I-P_V)\varepsilon$ into independent Gaussian vectors. The triple in (b) is a linear function of $P_V\varepsilon$ (since $v^\top\varepsilon=v^\top P_V\varepsilon$ for $v\in V$). Also $\|\varepsilon\|^2=\|P_V\varepsilon\|^2+\|(I-P_V)\varepsilon\|^2$ with $\|(I-P_V)\varepsilon\|^2\sim\sigma_\star^2\chi^2_{n-d}$ independent of $P_V\varepsilon$ and $\|P_V\varepsilon\|^2\sim\sigma_\star^2\chi^2_d$. Write $W_n=W_n'+\|P_V\varepsilon\|^2/\sqrt n$ with $W_n':=\sqrt n(\|(I-P_V)\varepsilon\|^2/n-\sigma_\star^2)=\sigma_\star^2\frac{\chi^2_{n-d}-(n-d)}{\sqrt n}-\frac{\sigma_\star^2d}{\sqrt n}$. Since $\chi^2_{n-d}$ is a sum of $n-d$ i.i.d. $\chi^2_1$ variables with variance $2$, the central limit theorem and Slutsky's lemma give $W_n'\Rightarrow N(0,2\sigma_\star^4)$; and $\|P_V\varepsilon\|^2/\sqrt n\to0$ in probability. The pair (triple, $W_n'$) has a product law (independence of $P_V\varepsilon$ and $(I-P_V)\varepsilon$) whose first factor does not depend on $n$ and whose second factor converges weakly; hence the pair converges weakly to the product limit, and Slutsky's lemma absorbs the vanishing term. $\square$

**Lemma 7.4.2 (the three normalised residual quantities).** Let $R_T:=(d_T-\varepsilon^\top P_T\varepsilon)/n$ for $T\in\{\{1\},\{2\},\{1,2\}\}$, with $d_T$ from (F-det). Then $nR_T=O_{\mathbb P}(1)$, and
$$
v_n:=\frac{\tilde Q_\emptyset}{n}=\bar\sigma^2_\emptyset+\frac{2G_n+W_n}{\sqrt n}+\frac{2b_0}{n},\qquad
u^{(j)}_n:=\frac{\tilde Q_{\{j\}}}{n}=\bar\sigma^2_1+\frac{2G_n+W_n-2G^{(j)}_n}{\sqrt n}+\frac{2b_0}{n}+R_{\{j\}},\qquad
u^{(12)}_n:=\frac{\tilde Q_{\{1,2\}}}{n}=\sigma_\star^2+\frac{W_n}{\sqrt n}+\frac{2b_0}{n}+R_{\{1,2\}} .
$$
*Proof.* By (F-dec), $\tilde Q_\emptyset=2b_0+\|\mu\|^2+2\mu^\top\varepsilon+\|\varepsilon\|^2$ and $\tilde Q_T=\tilde Q_\emptyset-\|P_T\mu\|^2-2\mu^\top P_T\varepsilon+nR_T$. Divide by $n$ and insert Lemma 7.4.1(a): $\|\mu\|^2/n=\bar\sigma^2_\emptyset-\sigma_\star^2$, $\|\varepsilon\|^2/n=\sigma_\star^2+W_n/\sqrt n$, $2\mu^\top\varepsilon/n=2G_n/\sqrt n$, $\|P_{\{j\}}\mu\|^2/n=\bar\sigma^2_\emptyset-\bar\sigma^2_1$, $2\mu^\top P_{\{j\}}\varepsilon/n=2G^{(j)}_n/\sqrt n$, and for $T=\{1,2\}$: $\|P_T\mu\|^2/n=\bar\sigma^2_\emptyset-\sigma_\star^2$ and $2\mu^\top P_T\varepsilon=2\mu^\top\varepsilon$, so the $G_n$ terms cancel. For $nR_T$: $\varepsilon^\top P_T\varepsilon\sim\sigma_\star^2\chi^2_{|T|}=O_{\mathbb P}(1)$; and $g_T=\lambda_{\min}(G_T)=n\lambda_{\min}(\Gamma_T)\ge n(1-\rho)\ge1$ for $n\ge1/(1-\rho)$, so by (F-det) $0\le d_T\le\frac{2}{n+1}\|P_Ty\|^2\le\frac{2\|y\|^2}{n+1}$, and $\|y\|^2\le2\|\mu\|^2+2\|\varepsilon\|^2=O_{\mathbb P}(n)$. $\square$

**Lemma 7.4.3 (a logarithmic expansion).** Let $\sigma^2>0$ be a constant and $(t_n)$ random variables with $\sqrt n\,t_n=O_{\mathbb P}(1)$. Then $n\log(\sigma^2+t_n)=n\log\sigma^2+n\,t_n/\sigma^2+O_{\mathbb P}(1)$ (the left side being defined with probability tending to one).
*Proof.* Put $x_n=t_n/\sigma^2=O_{\mathbb P}(n^{-1/2})$, so $\mathbb P(|x_n|>\tfrac12)\to0$. On $\{|x_n|\le\tfrac12\}$, $|\log(1+x_n)-x_n|\le x_n^2$, hence $n|\log(1+x_n)-x_n|\le nx_n^2=O_{\mathbb P}(1)$. $\square$

**Proposition 7.4 (second-order expansions).** With $\Gamma_n=\Gamma$ exactly, as $n\to\infty$,
$$
\log a_j=n\kappa_{\rm pair}-\tfrac12\log n+\sqrt n\,V^{(j)}_n+O_{\mathbb P}(1),\qquad V^{(j)}_n:=c_1(2G_n+W_n)+c_2G^{(j)}_n\quad(j=1,2),
$$
$$
\log a_{12}=\tfrac n2L-\log n+\sqrt n\,V^{(12)}_n+O_{\mathbb P}(1),\qquad V^{(12)}_n:=d_1G_n+d_2W_n ,
$$
and $(V^{(1)}_n,V^{(2)}_n,V^{(12)}_n)$ converges in law to a centred Gaussian vector with
$$
v_j^2:=\lim\operatorname{Var}V^{(j)}_n=2\sigma_\star^4c_1^2+4c_1^2\operatorname{Var}G+c_2^2\operatorname{Var}G^{(j)}+4c_1c_2\operatorname{Cov}(G,G^{(j)})\ \ge\ 2\sigma_\star^4c_1^2>0,
$$
$$
v_{12}^2:=\lim\operatorname{Var}V^{(12)}_n=d_1^2\operatorname{Var}G+2\sigma_\star^4d_2^2\ \ge\ 2\sigma_\star^2\beta^2(1-\rho)\,d_1^2>0,
$$
the variances and covariances being those of Lemma 7.4.1(b). In particular $\log a_j-n\kappa_{\rm pair}$ and $\log a_{12}-\tfrac n2L$ are of exact order $\sqrt n$: divided by $\sqrt n$ they converge to non-degenerate normal laws.

*Proof.* By Lemma 1.1, $\log a_T=-\tfrac12\log D_T-\nu\log(\tilde Q_T/\tilde Q_\emptyset)$ with $\nu=\tfrac n2+a_0$.

*Determinants.* $G_{\{j\}}=\|x_j\|^2=n$, so $D_{\{j\}}=\frac{(n+1)n+1}{n+1}=n\big(1+\frac1{n(n+1)}\big)$ and $-\tfrac12\log D_{\{j\}}=-\tfrac12\log n+O(n^{-2})$. For $T=\{1,2\}$, (F-det)(2.1) with $\lambda=1-\rho$ (and $n_0=1$, since $\Gamma_n=\Gamma$) gives $-\tfrac12\log D_{\{1,2\}}=-\log n+O(1/n)$.

*The $a_0$ part.* By Lemma 7.4.2, $u^{(j)}_n\to\bar\sigma^2_1$, $u^{(12)}_n\to\sigma_\star^2$ and $v_n\to\bar\sigma^2_\emptyset$ in probability (every correction is $O_{\mathbb P}(n^{-1/2})$), all limits positive; so $-a_0\log(u_n/v_n)=O_{\mathbb P}(1)$ in both cases.

*The main part, singletons.* Apply Lemma 7.4.3 twice: with $\sigma^2=\bar\sigma^2_1$ and $t_n=u^{(j)}_n-\bar\sigma^2_1=n^{-1/2}(2G_n+W_n-2G^{(j)}_n)+2b_0/n+R_{\{j\}}$ (so $\sqrt nt_n=O_{\mathbb P}(1)$ by Lemmas 7.4.1(c) and 7.4.2), and with $\sigma^2=\bar\sigma^2_\emptyset$ and $t_n'=v_n-\bar\sigma^2_\emptyset=n^{-1/2}(2G_n+W_n)+2b_0/n$:
$$
-\tfrac n2\big[\log u^{(j)}_n-\log v_n\big]=-\tfrac n2\log\frac{\bar\sigma^2_1}{\bar\sigma^2_\emptyset}-\tfrac n2\Big[\frac{t_n}{\bar\sigma^2_1}-\frac{t_n'}{\bar\sigma^2_\emptyset}\Big]+O_{\mathbb P}(1)
= n\kappa_{\rm pair}-\frac{\sqrt n}2\Big[\frac{2G_n+W_n-2G^{(j)}_n}{\bar\sigma^2_1}-\frac{2G_n+W_n}{\bar\sigma^2_\emptyset}\Big]+O_{\mathbb P}(1),
$$
where the terms $\tfrac n2\cdot2b_0/n$ and $\tfrac n2R_{\{j\}}$ were absorbed into $O_{\mathbb P}(1)$ (Lemma 7.4.2). The bracket times $-\tfrac{\sqrt n}2$ equals $\sqrt n\,[c_1(2G_n+W_n)+c_2G^{(j)}_n]$. Adding the determinant and $a_0$ parts gives the first display.

*The main part, the pair.* Likewise with $\sigma^2=\sigma_\star^2$, $t_n=u^{(12)}_n-\sigma_\star^2=n^{-1/2}W_n+2b_0/n+R_{\{1,2\}}$:
$-\tfrac n2[\log u^{(12)}_n-\log v_n]=-\tfrac n2\log\frac{\sigma_\star^2}{\bar\sigma^2_\emptyset}-\tfrac{\sqrt n}2\big[\frac{W_n}{\sigma_\star^2}-\frac{2G_n+W_n}{\bar\sigma^2_\emptyset}\big]+O_{\mathbb P}(1)=\tfrac n2L+\sqrt n\,[d_1G_n+d_2W_n]+O_{\mathbb P}(1)$.

*The limit law.* $(V^{(1)}_n,V^{(2)}_n,V^{(12)}_n)$ is a fixed linear image of $(G_n,G^{(1)}_n,G^{(2)}_n,W_n)$, so Lemma 7.4.1(c) and the continuous mapping theorem give joint convergence to a centred Gaussian vector. With $W$ independent of the triple, $\operatorname{Var}[c_1(2G+W)+c_2G^{(j)}]=\operatorname{Var}[2c_1G+c_2G^{(j)}]+c_1^2\operatorname{Var}W$, which is the formula for $v_j^2$; the lower bound drops the first (nonnegative) variance and uses $c_1\ne0$ (because $\bar\sigma^2_1<\bar\sigma^2_\emptyset$). Similarly $\operatorname{Var}[d_1G+d_2W]=d_1^2\operatorname{Var}G+d_2^2\cdot2\sigma_\star^4$, and $\operatorname{Var}G=2\sigma_\star^2\beta^2(1-\rho)>0$. $\square$

*Numerical check (Section 9, block Ex2).* For $\rho=0.9$, $\beta=\sigma_\star=1$: $v_1^2=0.006978$, $v_{12}^2=0.152778$; Monte Carlo with $2000$ draws (seed $1$) gives, at $n=3200$, sample standard deviations $0.0831$ and $0.3923$ of $(\log a_1-n\kappa_{\rm pair}+\tfrac12\log n)/\sqrt n$ and $(\log a_{12}-\tfrac n2L+\log n)/\sqrt n$, against $\sqrt{v_1^2}=0.0835$ and $\sqrt{v_{12}^2}=0.3909$, with means $0.0085$ and $0.0056$.

### 7.5 The status of the "window" paragraph

**Proposition 7.5.** (a) The draft's displays $\log a_j\approx n\kappa_{\rm pair}-\tfrac12\log n$ and $\log a_{12}\approx\tfrac n2L-\log n$ are correct in exactly this sense: their right-hand sides are the deterministic parts of the expansions of Proposition 7.4, and the remainders are $\sqrt n\,V_n+O_{\mathbb P}(1)$ with $V_n$ asymptotically $N(0,v^2)$, $v>0$. (Under (S) alone, without $\Gamma_n=\Gamma$, what remains true is the leading order: $\tfrac1n\log a_j\to\kappa_{\rm pair}$ and $\tfrac1n\log a_{12}\to L/2$, by (F-rate).)
(b) Consequently $\log(a_1a_2)=2n\kappa_{\rm pair}-\log n+\sqrt n\,(V^{(1)}_n+V^{(2)}_n)+O_{\mathbb P}(1)$ and $\log a_{12}=\tfrac n2L-\log n+\sqrt n\,V^{(12)}_n+O_{\mathbb P}(1)$. The window argument compares $2n\kappa_{\rm pair}-\log n$ and $\tfrac n2L-\log n$ with $\log3$; the quantities it keeps beyond the linear terms are $O(\log n)$, while the terms it drops are of exact order $\sqrt n$. Hence the paragraph does not establish, for any $n$, that the switch conditions of Proposition 7.2 hold, nor with what probability; **the draft's label "heuristic" is accurate, and the paragraph is not upgraded here.**
(c) The one inference the paragraph draws at the level of rates, "a window requires $L>4\kappa_{\rm pair}$", compares the exponential rates $2\kappa_{\rm pair}$ of $a_1a_2$ and $L/2$ of $a_{12}$, which are correct (part (a)); and by Proposition 7.3 the inequality $L>4\kappa_{\rm pair}$ holds for every $\rho\in(0,1)$. So the necessary condition the paragraph identifies is never violated in the example's setting; "which holds for $\rho$ near $1$" can be replaced by "which holds for every $\rho\in(0,1)$".
(d) What is proved about finite-$n$ switches is Proposition 7.6 below: they occur with positive probability (an explicit instance at $n=100$), and their probability tends to zero.

*Proof.* (a)–(b) restate Proposition 7.4 and (F-rate). (c) is Proposition 7.3. (d) is Proposition 7.6. $\square$

*Remark (why a sharper statement is not attempted).* A rigorous "window" statement would be an asymptotic formula for $\mathbb P_0(\text{switch at }n)$ as a function of $n$, which by Proposition 7.4 is governed by Gaussian fluctuations of size $\sqrt n\,v$ around trends $n\kappa_{\rm pair}$ and $\tfrac n2L$; the interesting range of $n$ (where $n\kappa_{\rm pair}$ is comparable with $\log3+\tfrac12\log n$) is one where the $O_{\mathbb P}(1)$ remainders are not negligible against $\sqrt n\,v_j$ when $v_j$ is small (for $\rho=0.9$, $v_1\approx0.08$). The Monte Carlo profile in the script (switch frequency $0.20,0.48,0.80,0.88,0.74,0.30,0.00,0.00$ at $n=20,50,100,200,400,800,1600,3200$) illustrates the window but is not a theorem.

### 7.6 A finite-sample switch is possible, and its probability vanishes

**Proposition 7.6.** Assume $\Gamma_n=\Gamma$ exactly.
(a) *(Vanishing.)* $\mathbb P_0(\text{the conditions of Proposition 7.2 hold})\le\mathbb P_0(a_1<3)\to0$ as $n\to\infty$. Also, by T3(i) (whose hypotheses (S), (U), (R) hold here: (S) as in Proposition 6.5(a) with the present $\beta^\star$; (U) automatic; (R) by (F-R) since $\|\Gamma_n-\Gamma\|=0$), $\pi_0(S_0)\to1$ and $\pi(S_0)\to1$: eventually both modes are $S_0$ and there is no switch.
(b) *(Positive probability at finite $n$.)* Let $\rho=0.9$, $\beta=1$, $\sigma_\star^2=1$, $a_0=b_0=0.01$, $n=100$, $X$ any design with $X^\top X=100\,\Gamma$ (Lemma 1.3), and $y=\mu=X\beta^\star$. Then $a_1=a_2=1.2632$, $a_1a_2=1.5956$ and $\log a_{12}=217.2$ (so $a_{12}\approx2.07\cdot10^{94}$): the conditions of Proposition 7.2 hold at $y=\mu$. The set of $y\in\mathbb R^n$ satisfying the three strict inequalities is open and contains $\mu$; since $y\sim N_n(\mu,\sigma_\star^2I_n)$ has a strictly positive density, $\mathbb P_0(\text{switch})>0$ at $n=100$. (Monte Carlo with $1000$ draws: $0.80$.)
(c) *(Reproducibility.)* For every $n$, the law of $(a_1,a_2,a_{12})$ under $\mathbb P_0$, hence $\mathbb P_0(\text{switch})$, depends on the design only through $\Gamma_n$; so (b) and the Monte Carlo profile are determined by $(n,\Gamma,\beta^\star,\sigma_\star^2,a_0,b_0)$ and the seed.

*Proof.* (a) The three conditions imply $a_1<3$. By Proposition 7.1(c), $\tfrac1n\log a_1\to\kappa_{\rm pair}>0$ in probability, so $\mathbb P_0(\log a_1<\log3)\le\mathbb P_0(\tfrac1n\log a_1<\tfrac12\kappa_{\rm pair})\to0$ for $n>2\log3/\kappa_{\rm pair}$. The T3 statement is (F-T3) under the hypotheses listed.
(b) The numbers are computed in `check_elementary_II.py` (block Ex2, "y = mu"); they are functions of $(z_1,z_2,\|y\|^2)=(n(\Gamma\beta^\star)_1,n(\Gamma\beta^\star)_2,n\beta^{\star\top}\Gamma\beta^\star)=(10,-10,20)$ and of $\Gamma$, $n$, $a_0$, $b_0$ only, by (eq:m) and $H_S=(n+1)n\Gamma_S+I$. Each of $a_1,a_2,a_{12}$ is a continuous function of $y$ ($\tilde Q_S$ is a positive continuous function of $y$, Section 0.1), so the three strict inequalities define an open set; it contains $\mu$; a Gaussian law with positive density charges every nonempty open set.
(c) $\mathrm{BF}(S)$ is a function of $(z_S,\|y\|^2)$ and of $G_S=n\Gamma_{n,S}$. Write $\varepsilon=P_X\varepsilon+(I-P_X)\varepsilon$. Then $X^\top y=n\Gamma_n\beta^\star+X^\top\varepsilon$ with $X^\top\varepsilon=X^\top P_X\varepsilon\sim N_2(0,\sigma_\star^2n\Gamma_n)$, and $\|y\|^2=\|\mu\|^2+2\beta^{\star\top}X^\top\varepsilon+\|P_X\varepsilon\|^2+\|(I-P_X)\varepsilon\|^2$ with $\|P_X\varepsilon\|^2=(X^\top\varepsilon)^\top(n\Gamma_n)^{-1}(X^\top\varepsilon)$ and $\|(I-P_X)\varepsilon\|^2\sim\sigma_\star^2\chi^2_{n-2}$ independent of $X^\top\varepsilon$. So the joint law of $(X^\top y,\|y\|^2)$ is determined by $(n,\Gamma_n,\beta^\star,\sigma_\star^2)$. $\square$

*Remark 7.7 (relation to the draft's last two sentences).* "A finite-sample switch is then possible" is Proposition 7.6(b) (as an existence statement; the draft's "then" suggests that it follows from the window heuristic, which it does not; it follows from an explicit instance). "Its probability tends to zero as $n\to\infty$, by T3(i)" is Proposition 7.6(a), which gives the direct reason ($a_j\to\infty$ exponentially fast, so the start's mode is eventually $S_0$) as well as the T3 reason.

---

## 8. Hypotheses added, readings, and flags for the draft

**Hypotheses and conventions made explicit (none changes a displayed claim).**
1. *Global.* $m(S)>0$ for every $S$ and $y$ (shrinkage floor and $b_0>0$); a cap above $p$ is read as $\min\{k_{\max},p\}$; the fixed total order resolves every tie (readings (Rd1), (Rd2)).
2. *P3.* $w>0$ on $\{0,\dots,k_{\max}\}$ and $s_0\le k_{\max}$ (the latter is used for the supremum and the attainment, Remark 2.3(a)); the tie rule for $\hat k$ (Rd1). Nothing about the form of $m$ is used beyond positivity.
3. *P4.* $X^\top X=nI_p$ (hence $p\le n$); $k\le\min\{k_{\max},p\}$ in (ii); in (i) and (iii), $|S|=k<k_{\max}$ so that $S\cup\{j\}$ is in the support. Part (iii) uses the known-variance marginal of Definition 3.3 (reading (Rd3)), which the draft does not define; for $\mathrm{BB}(1,p)$ the ratio $w(k)/w(k+1)=(2p-k-1)/(k+1)$ needs $0\le k\le p-1$ (L6(i)).
4. *Pb2.* The instance uses the draft's default hyperparameters $a_0=b_0=0.01$; the qualitative conclusion (size maxima $1$, $<1$, $>1$; greedy stops at $\emptyset$; HPM $=\{1,2\}$) depends on $(a_0,b_0)$ only through $a_1<3<a_{12}$, which is what the script checks.
5. *Ex1.* Reading (Rd4): distinct blocks $C_1\ne C_2$, $p\ge3$, the regime-(b) setting (S) (in particular $\Gamma\succ0$, a fixed size-only prior with an eventually inactive cap). The identities (Propositions 5.1–5.3) and the deletion structure (5.4(a)) need only (S); the concentration of the start at $\tilde S_0$, i.e. the switch itself, needs (R), exactly as T3 does; $\|\Gamma_n-\Gamma\|=O(n^{-1/2})$ suffices.
6. *C1(i).* Reading (Rd6): the claim is about the hypotheses as listed in the proofs of T6, T7, T8, T9, T9a, C9, T10, and is witnessed by (ii). The attribution "Song and Liang (2015, Condition 5)" is the draft's and is not verified here.
7. *C1(ii).* Reading (Rd7): the cap is $\lfloor n/2\rfloor$, inactive for $n\ge4$; $n\ge4$ is assumed where T8's (A2) and (S2) need it. T8 is applied as Theorem 8.1 of `proofs/T7_T8` with the constants of Proposition 6.4.
8. *Ex2.* Reading (Rd5). Proposition 7.2 needs nothing (exact algebra). Propositions 7.4–7.6 assume $\Gamma_n=\Gamma$ **exactly** for every $n$; this is an added hypothesis for the second-order expansion (the draft's "$\approx$" displays) and for the explicit finite-$n$ instance. Under (S) alone, Proposition 7.5(a) records what survives (the exponential rates). With $\|\Gamma_n-\Gamma\|=o(n^{-1/2})$ the expansion of Proposition 7.4 would hold with $\kappa_{{\rm pair},n}$ and $L_n$ computed from $\Gamma_n$ in place of $\Gamma$; this is not proved here and not needed.
9. *Probability conventions.* "In probability" and $O_{\mathbb P}$, $o_{\mathbb P}$ are under $\mathbb P_0$ (the law of $\varepsilon$ with $X$ fixed), as in the draft's Section 2 and in `proofs/T3_T11`.

**Flags for the draft (no statement is false; all are wording or strengthening).**
- *P3.* Say how ties in $\hat k$ are broken: "with ties among sizes broken by the order of the $\hat S_k$" (Rd1); otherwise "$\mathrm{HPM}=\hat S_{\hat k}$" is ambiguous on a null set of $y$'s. Optionally note that the result uses only $m>0$.
- *P4(ii).* Add "up to ties among the $u_j$, resolved by the fixed order" (Rd2), and restrict $k\le\min\{k_{\max},p\}$.
- *P4(iii).* Define the known-variance posterior (Definition 3.3); the "$\approx$" can be made exact: the right-hand side is $\log n+\log(1+\tfrac1{n(n+1)})+2\log\frac{2p-k-1}{k+1}$.
- *Pb2.* Can be re-tagged "Solved" with the instance of Proposition 4.3: $n=10$, $x_1=\mathbf 1$, $x_2=(1,-1,\dots)$, $y=(3,0,-1,0,2,0,2,0,2,0)$, $a_0=b_0=0.01$: size maxima $1,\ 0.480,\ 1.357$ relative to $\emptyset$; greedy stopping returns $\emptyset$, the HPM is $\{1,2\}$. The hint's "equal singleton Bayes factors $2$" is a mechanism, not a requirement; the hint's inequality $\mathrm{BF}(\{1,2\})>\mathrm{BF}(\{1\})\mathrm{BF}(\{2\})$ is proved (Lemma 4.1) for every orthogonal $p=2$ design and every $y$ with $u_1u_2>0$.
- *Ex1.* (a) The sentence "the switch here is a single deletion" presupposes T3(i), hence (R); add "under (R)" or "e.g. if $\Gamma_n=\Gamma$", or say "the net change from $\tilde S_0$ to $S_0$ is a single deletion". (b) State that $C_1\ne C_2$ (two blocks). (c) One may add the full formula $\bar\sigma^2_2(T)=\sigma_\star^2+\beta^2(1-r^2\mathbf 1\{3\in T\})$ for all $T\subseteq C_2$, and the posterior side $\log\{\pi(S_0)/\pi(\tilde S_0)\}=\tfrac12\log n+O_{\mathbb P}(1)$ (T3(iv)), which makes the contrast "linear deficit of the start versus logarithmic preference of the posterior" explicit in the example.
- *Ex2.* (a) **Strengthening:** "which holds for $\rho$ near $1$" can read "which holds for every $\rho\in(0,1)$, since $\bar\sigma^2_1(\{1\})^2-\bar\sigma^2_1(\emptyset)\sigma_\star^2=2\sigma_\star^2\beta^2\rho(1-\rho)+\beta^4(1-\rho^2)^2>0$" (Proposition 7.3). (b) The label "heuristic" is accurate and should stay. If the paper wants a precise statement next to it, Proposition 7.4 is available: with $\Gamma_n=\Gamma$, $\log a_j=n\kappa_{\rm pair}-\tfrac12\log n+\sqrt n\,V^{(j)}_n+O_{\mathbb P}(1)$ and $\log a_{12}=\tfrac n2L-\log n+\sqrt n\,V^{(12)}_n+O_{\mathbb P}(1)$ with asymptotically normal $V$'s of explicit positive variance; this is what "fluctuate by $O_{\mathbb P}(\sqrt n)$" means, and shows the order $\sqrt n$ is exact. (c) "A finite-sample switch is then possible" does not follow from the heuristic; it is an existence statement, proved by the instance of Proposition 7.6(b) ($n=100$, $\rho=0.9$, $\beta=\sigma_\star=1$, $y=\mu$; Monte Carlo frequency $\approx0.80$). Suggested wording: "A finite-sample switch does occur (for $\rho=0.9$, $\beta=\sigma_\star=1$ it has probability about $0.8$ at $n=100$); its probability tends to zero as $n\to\infty$, by T3(i)." (d) The exact conditions can note that $a_1a_2<3$ is not implied by $\max(a_1,a_2)<3$ (Section 7.2, Remark).
- *C1(i).* "T6–T10" should list what it covers (T6, T7, T8, T9, T9a, C9, T10), and the Song–Liang attribution should be checked against the source by whoever has it (unverified here). The scope warning of Remark 6.2(b) may be worth a clause: no marginal-correlation condition is *imposed*, but a cancelled variable is exactly what the composite start misses.
- *C1(ii), note.* "Condition (R) holds because the cancellation is exact at every $n$" is right for (R1) (the gap $n[\bar\sigma^2_n(\{1\})-\bar\sigma^2_n(\emptyset)]=-(x_1^\top\mu)^2/n$ vanishes identically); (R2) holds because $\Gamma_n\to\Gamma$ (here $\Gamma_n=\Gamma$). One may add $\kappa_1=\tfrac12\log(1+\beta^2\rho^2(1-\rho^2)/\sigma_\star^2)$ (T3(iv)), and that with a single block $\pi_0=\pi$ exactly. The sentence "By T4, the bridge needs about $\log_2\log\sqrt n$ stages" is the two-state count; the reduction of the regression bridge to two states is Pb3 (Remark 6.7).
- *Dependency map (Appendix).* Ex2's "window heuristic" entry is consistent with this proof; Pb2 can be moved from "Elem." to "solved (one explicit instance)".

---

## 9. Numerical checks

`check_elementary_II.py` (seed $1$, local, NumPy/SciPy; output in `check_elementary_II.out`): **32 checks, 32 pass.**
- **P4** ($n=12$, $p=5$, random orthogonal design, $\mathrm{BB}(1,5)$, cap $5$): $Q_S=y^\top y-h\sum_Su_j$ and $D_S=D^{|S|}$ on all $32$ models; the neighbour log-odds identity on all $(S,j)$ pairs; size-$k$ maximisers are top-$k$ sets and $\mathrm{HPM}$ is the top-$\hat k$ set with $\hat k$ from the braces; the known-variance marginal equals $(2\pi\sigma^2)^{-n/2}D_S^{-1/2}e^{-Q_S/(2\sigma^2)}$ (Lemma 3.4) and the known-variance log-odds identity on all $(S,j)$; the $\mathrm{BB}(1,p)$ right-hand side against $\log n+2\log\frac{2p-k-1}{k+1}$ (difference $0.0064<\tfrac1{n(n+1)}$).
- **Pb2**: $\mathrm{BB}(1,2)$ weights $3:1:1$; the family $y=a(x_1+x_2)+r$; instance C: $a_1=a_2=1.440812$, $a_{12}=4.072086$, size maxima $1,0.480271,1.357362$, greedy stops at $\emptyset$, HPM $=\{1,2\}$; Lemma 4.1 on $200$ random $y$.
- **Ex1** ($p=5$, three blocks, $r=0.6$, $\beta=1.3$, extra correlations among the other columns): Propositions 5.1–5.3, 5.6 to machine precision; finite-$n$ behaviour with $\Gamma_n=\Gamma$ (Section 5.5).
- **C1(ii)** ($\rho=0.7$): Proposition 6.3 to machine precision; finite-$n$ behaviour (Section 6.2).
- **Ex2** ($\rho=0.9$): Proposition 7.1; the equivalence and the closed form of Proposition 7.3 on a grid of $99\times3\times3$ parameter triples; Proposition 7.2 against brute-force modes on $300$ draws at $n=100$ (switch frequency $0.81$); the instance $y=\mu$ of Proposition 7.6(b); the variances of Proposition 7.4 against Monte Carlo ($2000$ draws at $n\in\{200,800,3200\}$); the switch-frequency profile over $n$.
- **P3** ($n=15$, $p=4$, equicorrelated design, $s_0=2$, $400$ draws, four priors including $w_\epsilon$ with $\epsilon=10^{-3},10^{-8}$): $\mathrm{HPM}=\hat S_{\hat k}$ with the tie rule, $\{\mathrm{HPM}=S_0\}\subseteq\mathcal W$, and $\mathbb P(\mathrm{HPM}=S_0)\le\mathbb P(\mathcal W)$ with equality for $\epsilon=10^{-8}$ on these draws.
