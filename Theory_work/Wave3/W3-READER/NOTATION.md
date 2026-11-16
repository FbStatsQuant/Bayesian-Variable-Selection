# Setup and notation (reader-facing; for the chapter, the paper and the advisor report)

*Draft v0.1, W3-READER, 2026-11-15. Everything above the line "Traceability" is meant to be pasted into a document a
peer reads; it contains no internal names. The traceability section at the end maps each definition to the code and to
the registered statements, and must be stripped from reader-facing copies.*

---

## 1. Data and model

We observe a response vector $y^{\mathrm r}\in\mathbb R^n$ and an $n\times p_{\mathrm{raw}}$ matrix of predictors
$X^{\mathrm r}$. Predictor columns that are constant are removed by the method before anything else is computed; $p$
denotes the number of **retained** (non-constant) columns, indexed by $[p]=\{1,\dots,p\}$.

**Model.** The data follow a Gaussian linear model with an intercept,
$$
y^{\mathrm r}=\alpha^*\mathbf 1_n+X^{\mathrm r}\beta^*+\varepsilon,\qquad \varepsilon\sim N_n(0,\sigma_*^2 I_n),
$$
with $\sigma_*^2>0$ and $\varepsilon$ independent of $X^{\mathrm r}$. Two kinds of design are considered.

* **Fixed design.** $X^{\mathrm r}$ is deterministic; probability refers to $\varepsilon$ only.
* **Random Gaussian design.** The rows of $X^{\mathrm r}$ are i.i.d. $N_p(m_n,\Sigma_n)$. Since the method standardises
  every column (§2), we may and do take $\Sigma_n$ to be a **correlation matrix** (unit diagonal). Probability then
  refers to the joint law of $(X^{\mathrm r},\varepsilon)$. A generic population row is written
  $W=(W_1,\dots,W_p)\sim N_p(0,\Sigma_n)$ (the mean plays no role).

**Truth.** $S_0:=\operatorname{supp}\beta^*=\{j:\beta^*_j\neq 0\}$ is the true model, $s_0:=|S_0|$ its size.

## 2. Standardisation (what the method actually sees)

Let $C:=I_n-\tfrac1n\mathbf 1\mathbf 1^\top$ be the centring matrix and $D$ the diagonal matrix of the sample standard
deviations of the retained columns of $X^{\mathrm r}$. The method works with
$$
X:=CX^{\mathrm r}D^{-1}\quad(\text{columns }x_j\text{ centred, }\|x_j\|^2=n-1),\qquad
y:=Cy^{\mathrm r}/s_y,\quad s_y^2:=\|Cy^{\mathrm r}\|^2/(n-1).
$$
On this scale the true coefficients and the mean signal are
$$
\theta^*:=D\beta^*\ \ (\text{standardised coefficients}),\qquad \mu:=CX^{\mathrm r}\beta^*=X\theta^*\in\mathbb R^n,
$$
and $\theta^*_{\min}:=\min_{j\in S_0}|\theta^*_j|$. Note $\operatorname{supp}\theta^*=S_0$. For a fixed design
$\theta^*$ is deterministic; for a random design it is random through $D$ (when a statement is made on the standardised
scale this is said explicitly).

**Sub-matrices.** For $S\subseteq[p]$: $X_S$ is the $n\times|S|$ sub-matrix of the columns in $S$,
$G_S:=X_S^\top X_S$, $\hat R_S:=G_S/(n-1)$ the **sample correlation matrix** of the columns in $S$, and $P_S$ the
orthogonal projection onto the column span of $X_S$ ($P_\emptyset=0$). $\lambda_{\min}(\cdot)$ is the smallest
eigenvalue. For a population correlation matrix, $\Sigma_{n,S}$ is the principal sub-matrix indexed by $S$.

## 3. The prior, as coded

The model space is the set of models with at most $K$ predictors,
$$
\Omega:=\{S\subseteq[p]:|S|\le K\},\qquad K:=\min(p,\lfloor n/2\rfloor).
$$
The prior is a hierarchical conjugate prior on $(S,\beta_S,\sigma^2)$ for the standardised data:

1. **Model prior (capped beta-binomial).** $\varpi(S)\propto w(|S|)$ on $\Omega$, with
   $$w(k)=\frac{1}{2\binom{2p-1}{k}} .$$
   This is the beta-binomial prior in which each predictor enters independently with probability $q$,
   $q\sim\mathrm{Beta}(1,p)$, restricted to $|S|\le K$. Its prior mean model size is about one; adding one variable to
   a model of size $k$ costs about $\log(2p/(k+1))$ in log prior odds.
2. **Coefficients (ridge-stabilised $g$-prior, $g=n$).** Given $S$ and $\sigma^2$,
   $\beta_S\sim N\big(0,\;n\sigma^2(G_S+I)^{-1}\big)$.
3. **Noise variance.** $\sigma^2\sim\mathrm{IG}(a_0,b_0)$ with $a_0=b_0=0.01$.
4. **Intercept.** Removed by centring (equivalent to a flat prior on the intercept).

The working likelihood is $y\mid S,\beta_S,\sigma^2\sim N_n(X_S\beta_S,\sigma^2 I_n)$. It is a *working* model: the
theorems are proved under the true model of §1, not under the prior.

## 4. The posterior

Integrating out $\beta_S$ and $\sigma^2$ gives the marginal likelihood of model $S$ in closed form:
$$
m(S)\ \propto\ \Big(\frac{\det H_S}{\det(G_S+I)}\Big)^{-1/2}\,(2b_0+Q_S)^{-\nu},\qquad
H_S:=(n+1)G_S+I,\quad Q_S:=y^\top y-n\,z_S^\top H_S^{-1}z_S,
$$
with $z_S:=X_S^\top y$ and $\nu:=a_0+n/2$. ($Q_S$ is a ridge-shrunk residual sum of squares; the determinant ratio is
the Occam factor, about $(n+1)^{|S|/2}$ for well-conditioned $X_S$.) The **posterior over models** is
$$
\pi(S\mid y)=\frac{w(|S|)\,m(S)}{\sum_{V\in\Omega}w(|V|)\,m(V)},\qquad S\in\Omega,
$$
and $F(S):=\log w(|S|)+\log m(S)$ is the **log score** of $S$ (posterior up to a constant). The method's target is
exactly this $\pi(\cdot\mid y)$. Because $y$ is standardised, $\pi(\cdot\mid y)$ is unchanged if $y^{\mathrm r}$ is
shifted or rescaled.

**Posterior summaries** (properties of $\pi$, not of any algorithm):
* posterior inclusion probabilities $\mathrm{PIP}_j:=\pi(j\in S\mid y)=\sum_{S\ni j}\pi(S\mid y)$;
* the highest posterior model $\mathrm{HPM}:=\arg\max_{S\in\Omega}\pi(S\mid y)$;
* the median probability model $\mathrm{MPM}:=\{j:\mathrm{PIP}_j>1/2\}$;
* the **posterior miss** $\delta_n:=1-\pi(S_0\mid y)$ (set $\pi(S_0\mid y)=0$ if $S_0\notin\Omega$).

Elementary but useful: for every data set, $\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|\le\delta_n$, and
$\delta_n<1/2$ forces $\mathrm{HPM}=\mathrm{MPM}=S_0$.

## 5. What the method returns

The method is a sequential Monte Carlo sampler over $\Omega$ with a deterministic start, calibration and local search
(the stages are explained in the companion "intuitive overview"). For the theory, four of its objects matter.

* **The start law $\pi_0$.** The method partitions the predictors into blocks $C_1,\dots,C_J$ of at most $16$ columns
  each (by complete-linkage clustering on $1-|\text{sample correlation}|$; only "a function of $X$, blocks of size
  $\le16$" is used in the theory). Within each block it scores every subset exactly. The start law is
  $$
  \pi_0(S)\propto w(|S|)\prod_{b=1}^{J}r_b(S\cap C_b),\qquad r_b(U):=m(U)/m(\emptyset),
  $$
  on $\Omega$: the posterior with all interactions *between* blocks ignored. It can be computed and sampled exactly.
  The **start mode** $\tilde S_0$ is a maximiser of $\pi_0$ over $\Omega$.
* **Local search from the start mode.** Starting at $\tilde S_0$, the method repeatedly scans all *neighbours* of the
  current model (every single deletion, every single addition when the size is below $K$, and every swap of one member
  for one non-member), moves to the best neighbour if it strictly improves the score $F$, and stops when a complete scan
  finds no strict improvement or when a move cap of about $\log_2(n+p)+|\tilde S_0|$ moves is reached.
* **The reported model $\hat S$.** Every model the run scores (by the sampler, by the local searches) is recorded; the
  reported model is the best-scoring recorded model. It is reported as **certified** when it is the end point of a
  local search whose last complete scan found no strict improvement (i.e. it is verified to be a local optimum of $F$
  in the neighbourhood above).
* **Estimated summaries.** The method also returns estimated PIPs, the MPM built from them, and an estimate of the
  normalising constant (the evidence) $\hat Z$.

**Output.** A run either returns these estimates ("produces output") or stops without them (for example when its
computing allocation is exhausted). $\mathcal O$ denotes the event that a run produces output.

**Standing conventions about "the method as coded".** All statements about what the method returns assume: (i) exact
arithmetic (scores and comparisons computed without rounding error); (ii) the shipped configuration (in particular the
local search from the start mode is switched on, with the move cap above); (iii) a computing allocation large enough
that the run is not stopped by its resource guard. Statements hold for every random seed and every outcome of the
method's internal calibration unless said otherwise.

## 6. Design quantities used in the assumptions

**Fixed design (sample quantities).** For $U\subseteq[p]$ and $l\notin U$:
* the **signal gain** of $l$ given $U$: $\delta^2_{U,l}:=\|(P_{U\cup\{l\}}-P_U)\mu\|^2$, the increase in explained
  mean signal when $x_l$ joins $X_U$;
* the **residual variance** left by $U$: $\tau^2_U:=\sigma_*^2+\|(I-P_U)\mu\|^2/(n-1)$ (noise plus unexplained signal
  energy per observation);
* the sample regression coefficient of $x_l$ on $X_U$: $\hat\beta_{U,l}:=(X_U^\top X_U)^{-1}X_U^\top x_l$,
  zero-padded to a vector indexed by a larger set when needed.

**Random Gaussian design (population quantities).** With $W\sim N_p(0,\Sigma_n)$:
* the **partial covariance** $\operatorname{Cov}(W_j,W_l\mid W_U)$ of $W_j$ and $W_l$ given $(W_k)_{k\in U}$;
* the population regression coefficient $\beta_{U,l}:=\Sigma_{n,UU}^{-1}\Sigma_{n,Ul}$ of $W_l$ on $W_U$, and the
  conditional variance $\operatorname{Var}(W_l\mid W_U)$.

**Leakage set and lattice.** A *leakage set* is a deterministic set $Q$ with $S_0\subseteq Q\subseteq[p]$ that
contains every column able to imitate part of the signal; the *lattice* of $Q$ is
$\mathcal L(Q):=\{T:S_0\subseteq T\subseteq Q\}$. "No leakage" means $Q=S_0$.

**Visibility.** A truth $j\in S_0$ is *visible* if its signal cannot be explained away by any $15$ other predictors
($15=$ largest block size minus one): the gain $\delta^2_{U,j}$ (fixed design) or the partial covariance
$\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)$ (random design) stays large for every $U\not\ni j$ with $|U|\le15$.

## 7. Asymptotic conventions and constants

All results are asymptotic in $n\to\infty$ along a sequence of problems (a *triangular array*): $p=p_n$, the design,
$\beta^*$ and $S_0$ may change with $n$; $s_0$ is fixed unless said otherwise.

* $p\le n^A$ for a fixed $A\ge1$; the regime $p\gg n$ is allowed and is the main case.
* $r_n:=\sqrt{\log n/n}$ is the **reference rate**.
* $X_n=O_P(a_n)$: for every $\epsilon>0$ there is $C$ with $P(|X_n|>Ca_n)\le\epsilon$ for all large $n$;
  $X_n=o_P(a_n)$: $X_n/a_n\to0$ in probability. "With probability tending to one" (w.p. $\to1$) means
  $P(\cdot)\to1$.
* $a_n\asymp b_n$: $a_n/b_n$ is bounded away from $0$ and $\infty$; $a_n\ll b_n$: $a_n/b_n\to0$; $a_n\gg b_n$:
  $b_n/a_n\to0$.
* $\log$ is the natural logarithm, $\log_2$ the binary one; $\lceil\cdot\rceil$ rounds up.
* **Constants.** $A$ (dimension exponent), $s_0$, $\sigma_*^2$, eigenvalue floors $\varphi_0,\varphi,c$, the
  collinearity floor $g_0$, coefficient bounds $\bar\theta$, $b_{\mathrm{lo}},b_{\mathrm{hi}}$, and leakage exponents
  $b,\rho$ are fixed (do not depend on $n$). $c_0(s_0,A)$ denotes the beta-min constant of the posterior theorem, a
  fixed number depending only on $(s_0,A)$ (§ remarks there). $C$ denotes a constant depending only on fixed
  quantities; its value may change from line to line.

## 8. Notation table

| Symbol | Meaning | Defined in |
|---|---|---|
| $n$, $p$ | sample size; number of retained (non-constant) predictors | §1 |
| $y^{\mathrm r}$, $X^{\mathrm r}$ | raw response and predictors | §1 |
| $\alpha^*,\beta^*,\sigma_*^2$ | true intercept, coefficients, noise variance | §1 |
| $S_0$, $s_0$ | true model $\operatorname{supp}\beta^*$; its size | §1 |
| $\Sigma_n$, $W$ | population correlation matrix of a row; a population row | §1 |
| $C$, $D$, $s_y$ | centring matrix; diagonal of column sample s.d.; response s.d. | §2 |
| $X$, $x_j$, $y$ | standardised design and column $j$ ($\|x_j\|^2=n-1$); standardised response | §2 |
| $\theta^*$, $\mu$, $\theta^*_{\min}$ | standardised coefficients $D\beta^*$; mean signal $X\theta^*$; smallest true $|\theta^*_j|$ | §2 |
| $X_S$, $G_S$, $\hat R_S$, $P_S$ | columns in $S$; Gram matrix; sample correlation matrix; projection | §2 |
| $\Sigma_{n,S}$, $\lambda_{\min}$ | population sub-matrix; smallest eigenvalue | §2 |
| $\Omega$, $K$ | model space $\{|S|\le K\}$; size cap $\min(p,\lfloor n/2\rfloor)$ | §3 |
| $w(k)$, $\varpi$ | model-size weight $1/(2\binom{2p-1}{k})$; capped beta-binomial model prior | §3 |
| $a_0,b_0$ | inverse-gamma hyperparameters ($0.01$ each) | §3 |
| $m(S)$, $H_S$, $Q_S$, $z_S$, $\nu$ | marginal likelihood and its ingredients | §4 |
| $\pi(S\mid y)$, $F(S)$ | posterior over models; log score | §4 |
| $\mathrm{PIP}_j$, HPM, MPM | inclusion probability; highest posterior model; median probability model | §4 |
| $\delta_n$ | posterior miss $1-\pi(S_0\mid y)$ | §4 |
| $C_b$, $J$ | blocks of the method's partition ($|C_b|\le16$); number of blocks | §5 |
| $\pi_0$, $r_b$, $\tilde S_0$ | start law; within-block score ratios; start mode | §5 |
| $\hat S$ | reported model (best-scoring model recorded by the run) | §5 |
| $\mathcal O$ | event that the run produces output | §5 |
| $\delta^2_{U,l}$, $\tau^2_U$ | signal gain of $l$ given $U$; residual variance left by $U$ | §6 |
| $\hat\beta_{U,l}$, $\beta_{U,l}$ | sample / population regression coefficient of column $l$ on $U$ | §6 |
| $\operatorname{Cov}(\cdot,\cdot\mid W_U)$ | partial covariance given $W_U$ | §6 |
| $Q$, $\mathcal L(Q)$ | leakage set; its lattice $\{T:S_0\subseteq T\subseteq Q\}$ | §6 |
| $A$, $r_n$ | dimension exponent ($p\le n^A$); reference rate $\sqrt{\log n/n}$ | §7 |
| $O_P,o_P,\asymp,\ll,\gg$ | asymptotic notation | §7 |
| $\varphi_0,\varphi,c,g_0,\bar\theta,b_{\mathrm{lo}},b_{\mathrm{hi}},b,\rho$ | fixed constants of the assumptions | §7 |
| $c_0(s_0,A)$ | beta-min constant of the posterior theorem | §7 |

---

## Traceability (internal; strip before use)

* Preprocessing (constant columns dropped; centring; scaling to $\|x_j\|^2=n-1$; $y=Cy^{\mathrm r}/s_y$):
  `Scripts/SMC_BVS/core/v3_preprocess.R:111-127` (as cited in W3-POST STATEMENT §0, line 19) and `:37-68`, `:123-127`
  (W3-MISR STATEMENT R′(a″), lines 79-83). To be re-confirmed by the helper file `helpers/CODE_FACTS.md`.
* Prior, score, $K$, $\nu$, $H_S$, $a_0=b_0=0.01$, $\log w(k)=-\log2-\log\binom{2p-1}{k}$:
  `Scripts/SMC_BVS/core/cpp/v3_score.h:40-71, 196-224` (W3-POST STATEMENT.md:21-29). Working-model reading
  (coefficient prior $N(0,n\sigma^2(G_S+I)^{-1})$, IG(0.01, 0.01)): W3-POST STATEMENT.md:26-29.
* Beta-binomial identity: under $q\sim\mathrm{Beta}(1,p)$ and independent inclusion, a given model of size $k$ has
  probability $B(k+1,2p-k)/B(1,p)=\tfrac12/\binom{2p-1}{k}$ (direct computation; code comment `cpp/v3_score.h:15`;
  "capped BB(1, p)" in W3-POST STATEMENT.md:23).
* Partition (complete linkage on $1-|\hat r|$, cut at $\min(\lfloor\sqrt n\rfloor,\lfloor\sqrt p\rfloor,16)$, next-fit
  packing), tables $r_b$, start law, start mode: W3-START STATEMENT.md:47-61 (pins `cpp/v3_blocks.h:124-144`,
  `cpp/v3_start.h:68-137`, `v3_preprocess.R:22`); start mode is a maximiser of $\pi_0$: W3-RM:E4@1.0.0
  (W3-RM/STATEMENT.md:219-230), "PROVED-CHECKED".
* Local search neighbourhood, strict-improvement rule, certification, move cap $\ell_n+|\tilde S_0|$ with
  $\ell_n=\lceil\log_2(n+p+1)\rceil$: W3-RM2 STATEMENT.md:60-67 (pins `cpp/v3_engine.h:392-414`,
  `cpp/v3_core.cpp:465-476`); W3-RM STATEMENT.md:45.
* Reported model = ≻-maximum of the scored set; certified set: W3-SCR STATEMENT.md:29-44; C-DLV `lemmas/L4_delivery.md:66-70`.
* Output event, resource guard: `Scripts/SMC_BVS/core/README.md` (runtime guard; `resource_limit`); delivery fallback
  (tier-1 grid freezing, default on): `Scripts/SMC_BVS/core/v3_calib.R:120-124, 141-151`.
* Standing conventions (i)–(iii) = implementation premises EX-A; OP-LS0 with configuration `ls0 = TRUE`,
  `ls0_ell = ℓ_n`, `ls0_cap = "ell_n_plus_mode"`, `ls0_tie_dp = TRUE`; allocation inequalities and GUARD-W (W3-RM
  STATEMENT.md:55-68; W2-UNI `lemmas/L5_delivery.md:7-12`). The convention list must be checked against each master's
  exact premise list (see READER_VERSIONS "Standing conventions" note).
* $\delta^2_{U,l}$, $\tau^2_U$, $u_{U,l}$: W3-RM STATEMENT.md:38-40, :99-100; W3-START STATEMENT.md:74-80.
