# AUDIT2 — the comparison labels changed after reading Song–Liang's supplement

Material for a blind review. Every excerpt of ours is verbatim with its file and line numbers; Song–Liang
passages carry the journal page (main text) or the supplement page ("supp p.") and the display number, and
are transcriptions of the printed pages. Status labels have been replaced by [status omitted] or [review omitted].

## 1. Our theorem statements (verbatim)
Standing assumptions (S1)–(S3) of the reader versions:
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 28–31:
```
   28| (S1) Model of §1 of the notation: Gaussian errors with fixed variance $\sigma_*^2>0$, independent of the design.
   29| (S2) Asymptotics: $n\to\infty$, $p=p_n$ with $2\le p\le n^A$ for a fixed $A\ge1$ ($p\gg n$ allowed).
   30| (S3) "The method" means the method as coded, under the standing conventions of `NOTATION.md` §5 (exact arithmetic,
   31| shipped configuration, admissible runs). (S3) matters only for Theorems 5–8.
```

Reader statement of Theorem 1 and Theorem 1′ (fixed design; row 1.1):
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 103–134:
```
  103| **Theorem 1.** Let the design be fixed. Assume
  104| - **(A1) Model.** (S1) and (S2).
  105| - **(A2) Sparsity.** $s_0\ge1$ is fixed.
  106| - **(A3) Bounded coefficients.** $\max_{j}|\theta^*_j|\le\bar\theta$ for a fixed $\bar\theta<\infty$.
  107| - **(A4) Sparse eigenvalue floor.** $\lambda_{\min}(\hat R_S)\ge\varphi_0^2$ for every $S\subseteq[p]$ with
  108|   $|S|\le 2(A+1)s_0+2$, for a fixed $\varphi_0\in(0,1]$.
  109| - **(A5) No near-collinearity among $O(\log n)$ columns.** $\lambda_{\min}(X_S^\top X_S)\ge g_0$ for every $S$ with
  110|   $|S|\le 3(A+1)(s_0+1)\log n$, for a fixed $g_0>0$.
  111| - **(A6) Beta-min.** $\theta^*_{\min}\ge C_\beta\,\sigma_*\sqrt{\log n/n}$ with a fixed $C_\beta>0$ such that
  112|   $C_\beta^2\varphi_0^2>c_0(s_0,A)$ [S1-F1]; or $\theta^*_{\min}\sqrt{n/\log n}\to\infty$.
  113| 
  114| Then there are $n_0$ and $C$, depending only on $(s_0,A,\sigma_*^2,\bar\theta,\varphi_0,g_0,C_\beta)$, such that for every
  115| $n\ge n_0$ and every design and $\theta^*$ satisfying (A1)–(A6) at that $n$ [H5-1]
  116| $$
  117| E\big[1-\pi(S_0\mid y)\big]\ \le\ C\sqrt{\tfrac{\log n}{n}},
  118| $$
  119| and consequently, along any sequence satisfying (A1)–(A6),
  120| $$
  121| P\big(\mathrm{HPM}=\mathrm{MPM}=S_0\big)\ \ge\ 1-4C\sqrt{\tfrac{\log n}{n}}\ \to1,\qquad
  122| \max_{j\le p}\big|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}\big|\le 1-\pi(S_0\mid y)=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big).
  123| $$
  124| (Expectation over the noise, design fixed. With the second form of (A6), $n_0$ depends also on the divergence of
  125| $\theta^*_{\min}\sqrt{n/\log n}$.)
  126| 
  127| **Theorem 1′ (no eigenvalue condition off $S_0$ beyond the vanishing floor (A5)).** Replace (A4) by
  128| - **(A4′) Floor on the truth and an identifiability margin.** $\lambda_{\min}(\hat R_{S_0})\ge\varphi_0^2$, and every model
  129|   $S$ with $|S|\le K$, $S_0\not\subseteq S$ and at most $j_0:=\lceil(2A+1)s_0\rceil+1$ variables outside $S_0$ leaves
  130|   residual signal $\|(I-P_S)X\theta^*\|^2\ge c\,\sigma_*^2\log n$, with a fixed $c>c_1(s_0,A)$, where $c_1(s_0,A)$ is an
  131|   explicit constant, not optimised [H5-6],
  132| 
  133| and drop (A6). Then the conclusions of Theorem 1 hold (the expectation bound with constants depending on
  134| $(s_0,A,\sigma_*^2,\bar\theta,\varphi_0,g_0,c)$). [H5-1]
```

Reader statement of Theorem 2 (Gaussian rows; row 1.2), with its remark:
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 269–285:
```
  269| **Theorem 2.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a correlation matrix, and
  270| assume
  271| - **(A1) Model.** (S1) and (S2).
  272| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ is fixed and $b_{\mathrm{lo}}\le|\beta^*_j|\le b_{\mathrm{hi}}$ for
  273|   $j\in S_0$, with fixed $0<b_{\mathrm{lo}}\le b_{\mathrm{hi}}<\infty$.
  274| - **(A3) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge\varphi^2$ for every $S$ with
  275|   $|S|\le 5(A+1)(s_0+1)\log n$, for a fixed $\varphi\in(0,1]$ (for instance, $\lambda_{\min}(\Sigma_n)\ge\varphi^2$).
  276| 
  277| Then, under the joint law of design and noise, the three conclusions of Theorem 1 hold:
  278| $$
  279| 1-\pi(S_0\mid y)=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big),\qquad P(\mathrm{HPM}=\mathrm{MPM}=S_0)\to1,\qquad
  280| \max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big).
  281| $$
  282| 
  283| *Remarks.* No upper eigenvalue bound on $\Sigma_n$ and no beta-min beyond (A2) are needed; $p\gg n$ is allowed. The
  284| master allows the floor on sets of size $O(\log n)$ to vanish slowly ($\psi_n\gg(\log n)^{3/2}/\sqrt n$); the reader
  285| version uses a constant for simplicity.
```

Reader statement of Theorem 6 (the coded method reports the model; row 3.1):
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 666–697:
```
  666| **Theorem 6.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a positive definite
  667| correlation matrix, and $y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with deterministic $\theta^*$. Fix
  668| $b\in(0,\tfrac12)$ and $\rho>0$ with $15\rho+b<\tfrac12$. Assume
  669| - **(A1) Model.** (S1), (S2) ($p\gg n$ allowed), (S3).
  670| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  671|   $S_0$.
  672| - **(A3) Visibility.** $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a>0$ for every $j\in S_0$ and every
  673|   $U\not\ni j$ with $|U|\le15$.
  674| - **(A4) Polynomial leakage set.** There is a deterministic $Q\supseteq S_0$ with $|Q|\le n^b$ and, for large $n$,
  675|   $|Q|\le K$ and ($Q=[p]$ or $K\ge2|Q|+32s_0+1$), such that:
  676|   (i) *(no leak outside $Q$)* there is a deterministic $\varpi_n$ with $\varpi_n\sqrt{n/\log n}\to0$ such that
  677|   $|\operatorname{Cov}(W_l,W_j\mid W_U)|\le\varpi_n$ for all $l\notin Q$, $j\in S_0\setminus U$, $|U|\le15$;
  678|   (ii) *(locality)* there is a deterministic $r_n\to0$, and every $l\notin Q$ has a deterministic
  679|   $H_l\supseteq\{l\}\cup S_0$, $|H_l|\le n^{\rho}$, such that for all $l\notin Q$, all $U\not\ni l$ with $|U|\le15$
  680|   and $U_0:=U\cap H_l$: $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|\le r_n$ and
  681|   $|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for all $v\in U\setminus H_l$, $j\in S_0\setminus U_0$ [S1-F3].
  682| - **(A5) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c>0$ for every $S$ with
  683|   $|S|\le5(A+1)(s_0+1)\log n$ and for every $S=Q\cup\{l\}$, $l\in[p]$.
  684| - **(A6) Local regressions within $Q$.** There are deterministic sequences $\nu_n=o(\log n)$ and $L_n$, and for every
  685|   $l\in[p]$ a deterministic $N_l\subseteq Q\setminus\{l\}$ with $|N_l|\le\nu_n$ [S1-F3], such that
  686|   $\|\bar\beta_{T,l}-\bar\beta_{T\cap N_l,l}\|_1\le L_n$ for every $T$ with $S_0\subseteq T\subseteq Q$, $l\notin T$,
  687|   where $L_n\to0$ and $L_n^2\log(|Q|+1)=o(\log n)$ (bars: population regression coefficients, zero-padded).
  688| 
  689| Then, under the joint law of design and noise, there are data events $\mathcal G_n$ with $P(\mathcal G_n)\to1$ on
  690| which **every** admissible run that produces output reports $\hat S=S_0$, whatever its seed and the outcome of its
  691| internal calibration; in particular $P(\text{output and }\hat S\neq S_0)\to0$. If moreover the delivery conventions (S4)(i)–(iv) hold [S1-F2], $P(\text{the run produces output})=1$ for every admissible
  692| $n\ge3$ with $(n,p_{\mathrm{raw}})$ in the bounded domain $\mathfrak D$ of (S4)(v), where the code's two fixed integer limits are not
  693| reached. If in addition IDEAL-W⁺ holds ((S4)(v): the two limits lifted),
  694| $$
  695| P(\text{the run produces output})=1\ \ \text{for every admissible }n\ge3,\qquad P(\hat S=S_0)\to1 .
  696| $$
  697| The delivery statement idealises two fixed integer limits in the code (a base search cap of $10^6$, `v3_run.R:96`, and a 32-bit integer bound $2^{31}-1$ on the search cap, `cpp/v3_core.cpp:474`): the first can bind only when $n+p+1$ exceeds $2^{10^6}$, the second only when the starting model has more than about $2.1\times10^9$ variables, which needs $n\gtrsim4.3\times10^9$ since $|\tilde S_0|\le\lfloor n/2\rfloor$; without the idealisation, delivery holds on the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, and with it (IDEAL-W⁺) for every $n$ [RM2R-5].
```

Reader version of Theorem 9 (the posterior finds the distribution; row 2.1), its assumptions:
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1031–1042:
```
 1031| the largest number of predictors that (A3) and (A4) constrain jointly (of order $\log n$ for a fixed level).
 1032| 
 1033| ### Assumptions
 1034| - **(A1) Gaussian linear model.** $y=\alpha^*+x^\top\beta^*+\varepsilon$ with $\varepsilon\sim N(0,\sigma_*^2)$, $\sigma_*^2>0$,
 1035|   independent of $x$ ($\alpha^*$, $\beta^*$, $\sigma_*$ and the law of $x$ may depend on $n$).
 1036| - **(A2) Sparsity and dimension.** At most $s$ coordinates of $\beta^*$ are nonzero, and $2\le p_{\mathrm{raw}}\le n^A$.
 1037| - **(A3) Sub-Gaussian predictors on sparse directions.** Every predictor has positive variance, and for every
 1038|   $u\in\mathbb R^{p_{\mathrm{raw}}}$ with at most $q_n$ nonzero entries and every $\lambda\in\mathbb R$:
 1039|   $E\exp(\lambda u^\top z)\le\exp\big(L^2\lambda^2\,\mathrm{Var}(u^\top z)/2\big)$.
 1040| - **(A4) No near-exact collinearity.** $\lambda_{\min}(\mathrm{Corr}(x_T))\ge c_\psi/n$ for every set $T$ of at most $q_n$
 1041|   predictors.
 1042| - **(A5) Bounded signal.** $|\beta^*_j|\,\mathrm{sd}(x_j)\le\bar b\,\sigma_*$ for every $j$.
```

Reader statement of Corollary 9C (the output of the sampler):
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1081–1099:
```
 1081| **Corollary 9C (the output of the sampler).** The method explores the models with a sequential Monte Carlo sampler; it
 1082| does not compute the full posterior (small problems that it solves by exact enumeration are not covered here). A run is
 1083| *completed* when the method reports the status "completed"; runs that stop early are not covered. The output of a
 1084| completed run contains a list $\mathcal T$ of at most $40p+1$ distinct models: the best-scoring models among those offered to
 1085| the final run of the sampler (the models scored in that run, together with models scored earlier and carried into it:
 1086| the precomputed tables for small groups of predictors and the models kept from the calibration stage). Each model in the
 1087| list comes with the logarithm of its unnormalised posterior weight, taken to be computed in exact arithmetic. The output
 1088| contains no draws of $(\beta,\sigma^2)$. Let $\pi(\mathcal T)$ be the posterior probability of the list, and let $\hat\Pi$ (not
 1089| computed by the method) be the posterior restricted to the list: the models in $\mathcal T$, weighted in proportion to the
 1090| exponentials of their returned log-weights, each with its exact conditional posterior of $(\beta,\sigma^2)$. Under the
 1091| conditions of Theorem 9 (level-M form), with $P^*$-probability at least $1-n^{-cM}$ over the data, **every** completed run
 1092| (whatever its random numbers) with $\pi(\mathcal T)\ge n^{-cM/2}$ satisfies
 1093| $$
 1094| \hat\Pi\Big(d_H(f,f^*)>\sqrt{M\log n/n}\Big)\le n^{-cM/2}.
 1095| $$
 1096| If a completed run scored the true model $\{j:\beta^*_j\neq0\}$ and the posterior probability of that model exceeds $\tfrac12$,
 1097| then the list contains it, it is the model the method reports as most probable, and $\pi(\mathcal T)>\tfrac12$. Whether
 1098| the list carries enough posterior probability is a property of the run: the corollary does not assert it, and the output
 1099| does not certify it.
```

Master: our posterior π (prior, standardisation, outputs) and the truth:
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 18–34:
```
   18| Data (X^r, y^r), n ≥ 3, with non-constant y^r (s_y > 0; a.s. under G) [R01-4]. p = number of **retained** (non-constant)
   19| raw columns (the code drops constant columns before K and the prior are formed, `Scripts/SMC_BVS/core/v3_preprocess.R:111-127`);
   20| X = CX^rD_x⁻¹ = standardised design of the retained columns (centred, ‖x_j‖² = n − 1), y = Cy^r/s_y with
   21| s_y² = ‖Cy^r‖²/(n − 1). Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋). G_S = X_SᵀX_S, H_S = (n + 1)G_S + I,
   22| D_S = det H_S / det(G_S + I), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S (z_S = X_Sᵀy), ν = 0.01 + n/2;
   23| m(S) ∝ D_S^{−1/2}(2b₀ + Q_S)^{−ν}, a₀ = b₀ = 0.01; prior ϖ(S) = w(|S|)/W_K, w(k) = ½/C(2p − 1, k) (capped BB(1, p));
   24| π(S) ∝ ϖ(S)m(S) on Ω. (Definitions: `ARC/main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md:9-14`; code:
   25| `Scripts/SMC_BVS/core/cpp/v3_score.h:40-71, 196-224` — K = min(p, n/2), ν = a₀ + n/2, H = (n+1)G + I, A = G + I,
   26| log w(k) = −log 2 − log C(2p−1, k).) Equivalently π is the exact posterior under the **working** likelihood
   27| y | S, β_S, σ² ~ N_n(X_Sβ_S, σ²I) with β_S | S, σ² ~ N(0, nσ²(G_S + I)⁻¹), σ² ~ IG(0.01, 0.01) on the standardised
   28| scale (the standardised y does not have this law under the truth; the proofs treat it as a working model, [P1]
   29| lines 155-221) [R01-4]. π is the real-arithmetic target of the code; floating-point fidelity is not part of this file.
   30| 
   31| Truth: y^r = α*1 + X^rβ* + ε, ε ~ N_n(0, σ*²I) (**G**), μ := CX^rβ* = Xθ*, θ* = D_xβ*, S₀ = supp θ*, s₀ = |S₀|,
   32| r_n := √(log n/n). Exact posterior outputs: δ_n := 1 − π(S₀) (π(S₀) := 0 if s₀ > K); PIP_j := π(j ∈ S);
   33| HPM := argmax_Ω π (any tie rule); MPM := {j : PIP_j > ½}; ξ_q := {j : PIP_j > q}. These are properties of π, not of the
   34| sampler.
```

Master Theorem 1 (fixed design), regime, hypotheses and conclusions 1–4:
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 63–75:
```
   63| **Regime R1.** Triangular array, n → ∞; s₀ ≥ 1 fixed; 2 ≤ p = p_n ≤ n^A ([T03R] line 9 assumes p ≥ 2) [C1B-F3] for a fixed A ≥ 1 (p ≫ n allowed); s₀ ≤ K
   64| eventually; σ*² > 0 fixed; G.
   65| 
   66| **Hypotheses on (X, θ*)** (fixed design; fixed constants 0 < φ₀ ≤ 1, 0 < g₀ < ∞, 0 ≤ M < ∞ [R01-4]; j₀ := ⌈(2A + 1)s₀⌉ + 1):
   67| - **(E) energy**: ‖μ‖² ≤ nM.
   68| - **(F_λ) anchored floor, bounded size** = SE_λ(j₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}/(n−1)) ≥ φ₀² for every J ⊆ [p]∖S₀ with
   69|   |J| ≤ j₀ (J = ∅ included: this contains R's condition on S₀). *By interlacing it implies* λ_min(R_S) ≥ φ₀² for
   70|   **every** S with |S| ≤ j₀ (S ⊆ S₀ ∪ S), so it excludes e.g. duplicated null columns [R02-F2].
   71| - **(F_w) anchored unnormalised floor, logarithmic size** = SE_w(m♯_n; g₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ g₀ for every
   72|   J ⊆ [p]∖S₀ with |J| ≤ m♯_n (m♯_n = O(log n) under R1). By interlacing it implies λ_min(G_S) ≥ g₀ for every S with
   73|   |S| ≤ m♯_n: no exact linear dependence among ≤ m♯_n columns [R02-F2].
   74| - **(BM) beta-min**, either BM-∞: θ*²_min nφ₀²/(σ*² log n) → ∞; or BM(c): θ*²_min ≥ cσ*² log n/(nφ₀²) with a fixed
   75|   c > c₀(s₀, A) := max{4C_*, 32[s₀(A + 1) + 2]} (C_* the [P3] proof constant; a proof artefact, not sharp).
```
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 80–86:
```
   80| **Theorem 1.** In R1 under G, (E), (F_λ), (F_w):
   81| 1. **(Rate)** Under (BM): δ_n = 1 − π(S₀) = O_P(r_n).
   82| 2. **(Exact HPM, MPM, thresholded models)** Under (BM): P(HPM = S₀) ≥ P(δ_n < ½) → 1 and P(HPM ≠ S₀) ≤ 2Eδ_n → 0;
   83|    P(MPM = S₀) → 1; P(ξ_{q_n} = S₀) → 1 for every deterministic q_n ∈ (0, 1) with r_n = o(min(q_n, 1 − q_n)).
   84| 3. **(PIPs)** For every data set, max_j |PIP_j − 1{j ∈ S₀}| ≤ δ_n; under (BM) this is O_P(r_n) (sensitivity and
   85|    specificity uniformly in j), and E max_j |PIP_j − 1{j ∈ S₀}| → 0 (no expectation rate claimed).
   86| 4. **(Size, functionals)** Under (BM): π(|S| = s₀) = 1 − O_P(r_n); sup_{h:Ω→[0,1]} |π(h) − h(S₀)| = O_P(r_n).
```


## 2. Song–Liang (2015), main text (transcribed)
Song & Liang (2015), p. 947, §1, model (1) [SL-M1; transcribed from p. 947 image]:
```
Consider the problem of variable selection for the linear regression model:
    y = Xβ* + ε,    (1)
where y = (y_1, …, y_n)^T ∈ ℝ^n is the response vector, n is the sample size, X = (x_1, …, x_{P_n}) ∈ ℝ^{n×P_n} is the design matrix, P_n is the number of explanatory variables (which are also known as predictors), β* is the vector of unknown regression coefficients and ε = (ε_1, …, ε_n)^T ∼ N_n(0, σ*²) is Gaussian random error. In this paper, we use the bold letter x_i to denote an n-vector realization of the ith predictor. The subscript n in P_n means that P_n is a non-decreasing function of n. … In this paper, our study of variable selection will focus on the scenario P_n ≫ n, i.e. the column dimension of X is ultrahigh.
```
Song & Liang (2015), p. 950, §2.1, growth of P_n; sparsity conditions (3) and (4) [SL-M3; transcribed from p. 950 image]:
```
As in conventional studies of high dimensional variable selection, we consider the asymptotics of the SAM approach under the assumption that P_n increases as n increases. To be specific, we assume that P_n ≻ n^θ for some θ > 0, where b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0. In addition, we assume that the true model is sparse. Two sparseness conditions are considered in this paper. One states that most components of β* are very small such that
    lim_{n→∞} Σ_{j=1}^{P_n} |β*_j| < ∞,    (3)
where β*_j denotes the jth entry of β*. The other one is stronger but more usual, which requires that most components of β* are 0 such that
    lim_{n→∞} Σ_{j=1}^{P_n} 1{β*_j ≠ 0} < ∞.    (4)
Let ξ ⊂ {1, …, P_n} denote a subset model, which includes the indices of all selected predictors. Let |ξ| denote the number of predictors included in ξ. Thus, the strict sparsity condition (4) implies that the true model t = {i : β*_i ≠ 0, 1 ≤ i ≤ P_n} has a finite model size.
```
Song & Liang (2015), p. 951, §2.1.1, prior (6) [SL-P6; transcribed from p. 951 image]:
```
For the model ξ, we assume that each predictor has a prior probability λ_n = r_n/P_n, independent of other predictors, to be included in the model ξ. Further, we impose a constraint on the model size such that |ξ| ≤ r̄_n, where the upper bound r̄_n is prespecified. Then the prior probability of ξ can be expressed as
    π(ξ) ∝ λ_n^{|ξ|} (1 − λ_n)^{P_n−|ξ|} I(|ξ| ≤ r̄_n).    (6)
… We let the variance σ² be subject to an inverse gamma prior distribution with the hyperparameters a_0 and b_0, i.e. σ² ∼ IG(a_0, b_0). Conditioned on the model ξ and σ², we let β_ξ be subject to a Gaussian prior:
    β_ξ | ξ, σ² ∼ N_{|ξ|}(0, σ² V_ξ),
where V_ξ is a positive definite matrix depending on ξ. … In this paper, we assume that λ_n → 0 as P_n → ∞, which corresponds to condition (13) in theorem 1.
```
Song & Liang (2015), p. 951, §2.1.1, the posterior of ξ, (7) [SL-P7; transcribed from p. 951 image]:
```
To facilitate computation, we integrate out β_ξ and σ² from the posterior distribution (5). The resulting posterior distribution of ξ is given by
    π(ξ|D_n) ∝ (r_n/P_n)^{|ξ|} (1 − r_n/P_n)^{P_n−|ξ|} √det(V_ξ^{−1}) / √det(X_ξ^T X_ξ + V_ξ^{−1})
               × {2b_0 + y^T(I − X_ξ(X_ξ^T X_ξ + V_ξ^{−1})^{−1} X_ξ^T)y}^{−n/2−a_0} I(|ξ| ≤ r̄_n).    (7)
```
Song & Liang (2015), p. 952, §2.1.2, Hellinger distance; eigenvalue notation; B(r_n), B̃_n, Δ(p) [SL-H; transcribed from p. 952 image]:
```
In what follows, we study the asymptotics of the posterior distribution with respect to the Hellinger distance under appropriate conditions of r_n, r̄_n and V_ξ. For two density functions f_1(x, y) and f_2(x, y), the Hellinger distance is defined as
    d(f_1, f_2) = √( ∫∫ {f_1^{1/2}(x, y) − f_2^{1/2}(x, y)}² dx dy ).
For a matrix Σ, we let ch_i(Σ) denote the ith largest eigenvalue, and let ch′_i(Σ) denote the ith smallest eigenvalue. Define B(r_n) = sup_{ξ:|ξ|=r_n} ch_1(V_ξ^{−1}), B̄(r_n) = sup_{ξ:|ξ|=r_n} ch_1(V_ξ), B̃_n = sup_{ξ:|ξ|≤r̄_n} ch_1(V_ξ) and Δ(p) = inf_{ξ:|ξ|=p} Σ_{i∉ξ} |β*_i|.
Theorem 1 follows from Jiang (2007). Here we consider the simple situation that all predictors have been standardized and uniformly bounded, and the sparsity condition (3) holds.
```
Song & Liang (2015), p. 952, Theorem 1 and conditions (8)–(15) [SL-T1; transcribed from p. 952 image]:
```
Theorem 1 (posterior consistency). Assume that the data set D_n is drawn from model (1) and all predictors |x_i| ≤ 1. If there is a sequence {ε_n} ∈ (0, 1) such that nε_n² ≻ 1, and the following conditions hold,
    Δ(r_n) ≺ ε_n,    (8)
    r̄_n ln(1/ε_n²) ≺ nε_n²,    (9)
    r̄_n ln(P_n) ≺ nε_n²,    (10)
    r̄_n ln(nε_n² B̃_n) ≺ nε_n²,    (11)
    1 ≤ r_n ≤ r̄_n < P_n,    (12)
    r_n ≺ P_n,    (13)
    B(r_n) ≺ nε_n²,    (14)
then the posterior consistency holds, i.e. there is a constant c_1 > 0 such that
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²),    (15)
for sufficiently large n, where the Hellinger distance is
    d²(f, f*) = ∫∫ |φ^{1/2}(y; x^Tβ*, σ*) − φ^{1/2}(y; x^Tβ, σ)|² ν_x(dx) dy,
f* is as defined in expression (2), f is the density function for a model simulated from the posterior and P* denotes the probability measure of data generation.
```
Song & Liang (2015), p. 953, choices of V_ξ; 'ridge prior' [SL-V; transcribed from p. 953 image]:
```
The validity of this theorem depends on the choice of the prior covariance matrix V_ξ or, more precisely, the largest eigenvalues of V_ξ and V_ξ^{−1}. For most choices of V_ξ, B(r_n) ≤ B r_n^v and B̃_n ≤ B r_n^v hold for some positive constants B and v. For example, if V_ξ = c I_{|ξ|}, where I_p is an identity matrix of order p, then both B(r_n) and B̃_n are constants. One can also set V_ξ^{−1} = c E(x_ξ^T x_ξ) as in Zellner (1986) and Liang et al. (2008), where the expectation is replaced by its sample empirical estimator. If all x_i s are standardized with zero mean and equal variance, then B(r_n) ≤ r_n. Furthermore, if x_i has some specific covariance structure, then B̃_n can be shown to be bounded. For example, if all pairwise covariances cov(x_i, x_j) = ρ ∈ (0, 1), then B̃_n = 1 − ρ; if x_i is generated from a finite order auto-regressive or moving average model without root for the characteristic polynomial on the unit circle, then B̃_n is also bounded by some constant (Bickel and Levina, 2004). In general, for standardized x_i s, we can choose a 'ridge prior' as suggested by Gupta and Ibrahim (2009): let V_ξ^{−1} = E(x_ξ^T x_ξ) + c_n I_{|ξ|}; then B(r_n) ≤ r_n + c_n and B̃_n ≤ c_n^{−1}, where c_n is proportional to 1/n, i.e. c_n ∝ n^{−1}.
```
Song & Liang (2015), p. 953, Condition 1 and the two sufficient cases [SL-C1; transcribed from p. 953 image]:
```
Theorem 1 assumes that all the predictors are uniformly bounded. However, this condition might not be satisfied for continuous predictors. In what follows, we relax this condition.
Condition 1. There are some constants M > 0 and δ > 0 such that for any subvector of x, (x_{j_1}, …, x_{j_r})^T with 1 ≤ j_1 < … < j_r ≤ P_n, r ≤ r̄_n, and |a_i| ≤ δ for i = 1, …, r, we have
    E[ exp{ ( Σ_{i=1}^r a_i x_{j_i} / r )² } ] ≤ exp(M),
where the expectation is taken with respect to the distribution of the random variables x_{j_i}.
Condition 1 controls the tail distribution of x such that the marginal distribution of y does not change dramatically in the sense of d_1-divergence (which is defined in the on-line supplementary material) with respect to the change of β. If x has a heavy tail distribution, the prior information around f* will be too weak to induce good posterior asymptotics. If all the variables are bounded by some constant m, as assumed in theorem 1, then
    E[ exp{ ( Σ_{i=1}^r a_i x_{j_i} / r )² } ] ≤ exp(δ² m)
and thus condition 1 holds. If x follows a Gaussian process with zero mean and var(x_i) = 1, then (Σ_{i=1}^r a_i x_{j_i})² follows the sχ²_1-distribution, where the scale s ≤ δ² r². Therefore, by the moment-generating function of the χ²_1-distribution,
    E[ exp{ ( Σ_{i=1}^r a_i x_{j_i} )² / r² } ] ≤ (1 − 2δ²)^{−1/2},
condition 1 holds.
```
Song & Liang (2015), p. 953, Theorem 2 (pp. 953–954, with the note on (8)) [SL-T2; transcribed from p. 953 image]:
```
Theorem 2. Assume that the data set D_n is generated from model (1) and all the predictors satisfy condition 1. Given a sequence {ε_n}, ε_n → 0, and nε_n² → ∞, if the conditions (9)–(14) of theorem 1 hold, the model is strictly sparse, i.e. condition (4) holds, and r_n ≻ 1, then the posterior consistency still holds, i.e. there is a constant c_1 > 0 such that, for sufficiently large n,
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²).
Note that condition (8) of theorem 1 is redundant here as, for large n, r_n > |t| and Δ(r_n) = 0 hold under the sparseness condition (4). [the last words, from 'hold under', are on p. 954]
```
Song & Liang (2015), p. 954, Corollary 1 [SL-CO1; transcribed from p. 954 image]:
```
Corollary 1. Consider a strict sparse model, i.e. condition (4) holds. Suppose that P_n < exp(Cn^α) for some α ∈ (0, 1), and the prior specification in Section 2.1.1 is used such that B(r_n) ≤ B r_n^v and B̃_n ≤ B n^v for some positive constants B and v. Take
    r_n < r̄_n ≺ log^k(n),
or
    r_n < r̄_n ≺ n^q,
for some k > 0 or some 0 < q < min{1 − α, 1/v}. Then the convergence rate in theorem 2 can be taken as
    ε_n = O{n^{−(1−α)/2} log^{k/2}(n)},
or
    ε_n = O(n^{−(min{1−α−q, 1−vq})/2}).
```
Song & Liang (2015), p. 955, §2.2, marginal inclusion probability; Condition 3 [SL-C3; transcribed from p. 955 image]:
```
Let q_j denote the marginal inclusion probability of the predictor x_j, which is given by
    q_j = π(j ∈ ξ | D_n) = Σ_{ξ∈{ξ̃: j∈ξ̃}} π(ξ | D_n).
… Therefore, to select true predictors consistently, it is necessary to control the severeness of multicollinearity. For this purpose, we introduce the following identifiability condition which controls the severeness of multicollinearity through the sequence {ε_n}.
Condition 3. A predictor x_k is said to be identifiable among all other predictors, if, for any 1 ≤ j_1, …, j_{r̄_n} ≤ P_n (j_i ≠ k for all i) and b_i ∈ ℝ,
    E[ exp{ −( x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i} )² } ] ≤ 1 − δ_n,    δ_n ≻ ε_n²,
where x_l denotes a generic observation of the predictor x_l.
This condition states that, if a predictor x_k is identifiable, then there does not exist a linear combination of other predictors in X which can mimic it.
```
Song & Liang (2015), p. 955, sufficient forms of Condition 3 (pp. 955–956) [SL-C3S; transcribed from p. 955 image]:
```
If all the predictors have mean 0 and are bounded with |x_i| ≤ 1, then
    E[ exp{ −( x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i} )² } ] ≤ E[ 1 − ( 1 − exp{ −(1 + Σ_i |b_i|)² } ) / (1 + Σ_i |b_i|)² · ( x_k + Σ_i b_i x_{j_i} )² ]
        ≤ 1 − {1 − exp(−1)} var( x_k + Σ_i b_i x_{j_i} ) / (1 + Σ |b_i|)²
        ≤ 1 − (1 − exp(−1))/(r̄_n + 1) · ch′_1{var(x̃)},
where x̃ = (x_k, x_{j_1}, …, x_{j_{r̄_n}})^T, and ch′_1{var(x̃)} is the smallest eigenvalue of the covariance matrix of x̃. Hence, if ch′_1{var(x̃)} ≻ r̄_n ε_n² for any choice of x̃, x_t is identifiable. Furthermore, if ch′_1{var(x)} ≻ r̄_n ε_n², then all the predictors are identifiable, where x = (x_1, …, x_{P_n})^T denotes a generic observation of all predictors.
If all the predictors follow the standard normal distribution, by the moment-generating function of the χ²-distribution, we have
    E[exp{−(x_k + Σ b_i x_{j_i})²}] = { 1 + 2 var( x_k + Σ_i b_i x_{j_i} ) }^{−1/2} < max{ 0.5, 1 − var( x_k + Σ_i b_i x_{j_i} )/8 }.
Thus, if var(x_k + Σ_i b_i x_{j_i}) ≻ ε_n², then the identifiability condition is satisfied. Since [p. 956]
    var( x_k + Σ_i b_i x_{j_i} ) ≥ var(x_k | x̃∖x_k) ≥ ch′_1{var(x̃)} ≥ ch′_1{var(x)},
by the same arguments, all predictors are identifiable if ch′_1{var(x)} ≻ ε_n². Further, it can be shown (in the proof of theorem 3) that, if a true predictor x_t is identifiable, then d(f*, f) ≥ ε_n for any density f that does not select x_t. Therefore, we have the following sure screening property.
```
Song & Liang (2015), p. 956, Theorem 3 (sure screening) and the paragraphs after it [SL-T3; transcribed from p. 956 image]:
```
Theorem 3 (sure screening). Assume that all the conditions of theorem 2 hold. If a true predictor x_t (t ∈ t) is identifiable, then P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] < exp(−c_1 nε_n²), where ξ denotes a model sampled from the posterior distribution. Furthermore, if condition 2 holds, then the weaker convergence holds: lim_n P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] = 0.
The proof of theorem 3 can be found in the on-line supplementary material. Let ξ_q = {i : 1 ≤ i ≤ P_n, q_i > q} denote a model including all the predictors with the marginal inclusion probability greater than a threshold value of q ∈ (0, 1). Then it follows from theorem 3 that π(t ⊂ ξ_q) →^p 1 if all true predictors are identifiable. … Theorem S in the on-line supplementary material establishes the consistency of MAP models. Thus, we have two criteria for variable selection, by either marginal inclusion probabilities or the MAP model. Although theorem 3 states only the sure screening property (the sensitivity is asymptotically 1, but the specificity is not controlled), we suggest the use of marginal inclusion probabilities as the criterion for variable selection.
```
Song & Liang (2015), p. 959, §3.1 (SAM steps) and §3.2 (sampler) [SL-SAM; transcribed from p. 959 image]:
```
3.1. Split-and-merge approach
Based on the priors given in Section 2, the SAM approach can be summarized as follows.
(a) Split P_n predictors into K_n groups, s_1, …, s_{K_n}, with max_{i=1,…,K_n} |s_i| ≤ s for a prespecified value of s.
(b) Stage 1: apply the iterative procedure, proposed in Section 2.3, to select predictors from each subset D_n^{s_i} = {y, X_{s_i}}, i = 1, …, K_n, at an FDR level of α_1. At each iteration, the Bayesian variable selection is subject to the prior setting π(σ) ∼ IG(a_0, b_0), π(ξ) = λ_s^{|ξ|}(1 − λ_s)^{|s|−|ξ|} I(|ξ| ≤ s̄) and π(β_ξ | ξ, σ) ∼ N{0, σ²(X_ξ^T X_ξ + τI)/n}, where s̄ denotes the upper bound of the size of the models that are considered for each subset of data. Let s̃_1, …, s̃_{K_n} denote the sets of indices of the selected predictors from the K_n subsets.
(c) Stage 2: merge the sets s̃_1, …, s̃_{K_n} into a single set S̃ = ∪_{i=1}^{K_n} s̃_i, and define p_n = |S̃|. Perform Bayesian variable selection on the subset data D_n^{S̃} = {y, X_{S̃}} at an FDR level of α_2. The Bayesian variable selection is subject to the prior setting π(σ) ∼ IG(a_0, b_0), π(ξ) = (r_n/p_n)^{|ξ|}(1 − r_n/p_n)^{p_n−|ξ|} I(|ξ| ≤ r̄_n) and π(β_ξ | ξ, σ) ∼ N{0, σ²(X_ξ^T X_ξ + τI)/n}.
Clearly, it follows from the theory that was developed in Section 2 that the SAM approach will lead to a consistent selection of true predictors. In step 3, the predictors can also be selected according to the MAP model.
3.2. Simulation and hyperparameter setting
Since different predictors can be highly correlated, the posterior (7) can have a rugged energy landscape for some problems. Conventional MCMC algorithms, such as the Metropolis–Hasting algorithm, tend to become trapped in a local mode in simulations. To avoid this problem, the stochastic approximation Monte Carlo (SAMC) algorithm (Liang et al., 2007) was used in this paper. … Refer to the on-line supplementary material for the details of implementation of this algorithm.
```

## 3. Song–Liang (2015), on-line supplement (transcribed)
Song & Liang (2015), on-line supplement, supp p. 1, organisation; §1.1 opening [SS-ORG; transcribed from supp p. 1 image]:
```
This supplementary material is organized as follows. §1 gives the proofs of the main theoretical results of this paper. §2 describes the SAMC algorithm and its implementation for high dimensional regression, §3 studies properties of the MAP model under our prior setting, and §4 presents a comparison study for the performance of the horseshoe prior and the prior used in this paper.
1 Proofs of Main Theoretical Results
1.1 Proofs of Theorem 2.1 and Theorem 2.2
Let 𝒫 denote a set of probability densities which form the support of the prior. In case of Theorem 2.1 and Theorem 2.2, 𝒫 = {f(x, y|ξ, β_ξ, σ²) : |ξ| ≤ r̄_n, β_ξ ∈ ℝ^{|ξ|}, σ² > 0}. …
```
Song & Liang (2015), on-line supplement, supp p. 5–6, §1.2, proof of Theorem 2.3 (complete) [SS-T23; transcribed from supp p. 5 and supp p. 6 images]:
```
1.2 Proof of Theorem 2.3
Proof of Theorem 2.3. Assume that a model ξ does not include the true predictor x_t, f is conditional density corresponding to this mode ξ with some arbitrary β_ξ and σ_2². Then, for the Hellinger distance between true f* and f, we have
    d²(f*, f) = 1 − √( 2σ*σ_2/(σ*² + σ_2²) ) ∫_x exp{ −Δh²/(4(σ*² + σ_2²)) } ν_x(dx),
where Δh = β_ξ^T x_ξ − β*_t^T x_t is a linear function of the vector x. Recall that x represents a generic observation of P_n predictors, x_t denotes a generic observation of the true predictors, t ∈ t, and x_t denotes a generic observation of the predictor x_t. Since t ∈ t and t ∉ ξ, we can write Δh = −β*_t x_t + Σ_{i≠t} Δβ_i x_i. Thus, by condition (B_1),
    ∫_x exp(−Δh²/β*_t²) ν_x(dx) ≤ 1 − δ_n.
If 4(σ*² + σ_2²)/β*_t² ≤ 1, then
    ∫_x exp{ −Δh²/(4(σ*² + σ_2²)) } ν_x(dx) ≤ 1 − δ_n, and thus d²(f*, f) ≥ δ_n.
If 4(σ*² + σ_2²)/β*_t² > 1, by Jensen's Inequality,
    ∫_x exp{ −Δh²/(4(σ*² + σ_2²)) } ν_x(dx) ≤ (1 − δ_n)^{β*_t²/(4σ_2² + 4σ*²)} ≤ 1 − β*_t²/(4(σ_2² + σ*²)) · δ_n.
One can show that
    √( 2σ*σ_2/(σ*² + σ_2²) ) ∫_x exp{ −Δh²/(4(σ*² + σ_2²)) } ν_x(dx) ≤ max{ √(4/5), 1 − β*_t²/(20σ*²) · δ_n },
[p. 6] which implies d²(f*, f) ≥ min{ δ_n, β*_t² δ_n/20σ*², 1 − √0.8 }. Combining with the facts that δ_n ≻ ε_n² and ε_n → 0, we conclude d(f*, f) > ε_n, i.e., all the models which do not include the true predictor x_t are outside the ε_n-ball of f*. Because P*{π[d(f, f*) > ε_n | D_n] > e^{−c_1 nε_n²}} < e^{−c_1 nε_n²},
    P*{π[t ∈ ξ | D_n] < 1 − e^{−c_1 nε_n²}} < e^{−c_1 nε_n²}.    □
```
Song & Liang (2015), on-line supplement, supp p. 9–10, §2.1, SAMC weight estimates, (13) [SS-P9; transcribed from supp p. 9 and supp p. 10 images]:
```
Let θ_{ti} denote the working estimate of log(ω_i/π_i) obtained at iteration t, let θ_t = (θ_{t1}, …, θ_{tm})^T, and let {a_t} denote a positive, non-increasing sequence satisfying the conditions … (9) …
Under mild conditions, Liang et al. (2007) showed that as t → ∞,
    θ_{ti} → Const + log(ω_i) − log(π_i + π̄_0), if E_i ≠ ∅;   θ_{ti} → −∞, if E_i = ∅,    (13)
[p. 10] where π̄_0 = Σ_{j∈{i:E_i=∅}} π_j/(m − m_0) and m_0 is the number of empty subregions, and Const represents an arbitrary constant. The subregion E_i is called an empty subregion if ω_i = 0.
```
Song & Liang (2015), on-line supplement, supp p. 10, §2.1, importance weights, (14)–(15) [SS-P10; transcribed from supp p. 10 image]:
```
Furthermore, Liang (2009) showed that SAMC is invariant with respect to an importance weight. Mathematically, this can be explained as follows. Let (x_1, w_1), …, (x_N, w_N) denote a set of samples collected at the sampling step of SAMC, where
    w_t = Σ_{i=1}^m e^{θ_{ti}} I(x_t ∈ E_i).    (14)
Let y_1, …, y_{N′} denote the distinct samples among x_1, …, x_N. If we generate a random sample Y such that
    P(Y = y) = Σ_{t=1}^N w_t I(x_t = y) / Σ_{t=1}^N w_t,   y ∈ {y_1, …, y_{N′}},
then Y is asymptotically distributed with respect to the density f(x). This property implies that SAMC can be used as a usual importance sampling algorithm. For any integrable function h(x), the expectation E_f h(x) = ∫ h(x) f(x) dx can be estimated by
    Ê_f h(x) = Σ_{t=1}^N w_t h(x_t) / Σ_{t=1}^N w_t,    (15)
and, as n → ∞ [as printed], Ê_f h(x) → E_f h(x) almost surely for the same reason that the usual importance sampling estimate converges.
```
Song & Liang (2015), on-line supplement, supp p. 12–13, §2.4, estimated inclusion probabilities, (21) [SS-P12; transcribed from supp p. 12 and supp p. 13 images]:
```
2.4 Estimation of Marginal Inclusion Probability
Suppose that the sample space of the posterior π(ξ|D^n) has been partitioned according to the energy function U(ξ) into m subregions. Let (ξ_1, w_1), …, (ξ_T, w_T) denote a set of models collected in a run of SAMC, where w_t is as defined in (14). Then the marginal inclusion probability can be estimated by
    q̂_j = Σ_{t=1}^T w_t I(j ∈ ξ_t) / Σ_{t=1}^T w_t,   j = 1, …, P_n,    (21)
[p. 13] where I(·) is the indicator function. It follows from Liang (2009) that q̂_j → q_j almost surely as N → ∞, where q_j denotes the true marginal inclusion probability of variable x_j and has been defined in Section 3.1 of the main text.
```
Song & Liang (2015), on-line supplement, supp p. 13, §3.1, Theorem S, (22)–(25) [SS-TS; transcribed from supp p. 13 image]:
```
3 MAP Model and Its Consistency
3.1 MAP Model
Many Bayesian studies suggest that the MAP model is potentially a good estimator of the true model, see e.g., Freeman and Smith (2011) and Gupta (2008). In what follows, we establish the consistency of the MAP model with two different choices of V_ξ: V_ξ^{−1} = I and V_ξ^{−1} = X_ξ^T X_ξ/n.
Theorem S. (Consistency of the MAP model) Let D_n be a dataset generated from model (1) of the main text with a sparse true model t. Assume condition (12) of the main text and the following eigen-structure conditions hold: For any model ζ with size |ζ| = min{|t| + r̄_n, n}, there exist a non-increasing sequence {l_n} and a non-decreasing sequence {l′_n} such that
    n l_n < ch′_1(X_ζ^T X_ζ) ≤ ch_1(X_ζ^T X_ζ) < n l′_n,    (22)
    r̄_n log P_n ≺ n l_n.    (23)
If, further, one of the following two condition holds:
  1. n l_n ≻ log l′_n, log(√(n l_n)/r_n) ≻ √(log P_n), and we set V_ξ^{−1} = I for any ξ; or
  2. n l_n ≻ l′_n, log(√n/r_n) ≻ √(log P_n), and we set V_ξ^{−1} = X_ξ^T X_ξ/n for any ξ,
then, for any model k, the posterior probability (7) of the main text satisfies:
    max_{k≠t} π(k|D_n)/π(t|D_n) →_p 0.    (24)
Proof. Under the eigen-structure condition of X, V_ξ^{−1}'s eigenvalues are bounded by two values λ_1 and λ_2. For example, λ_1 = l_n, λ_2 = l′_n in the case V_ξ^{−1} = X_ξ^T X_ξ/n; and λ_1 = λ_2 = 1 in the case V_ξ^{−1} = I. Define R_ξ = y^T(I − X_ξ(X_ξ^T X_ξ + V_ξ^{−1})^{−1} X_ξ^T)y and R*_ξ = y^T(I − X_ξ(X_ξ^T X_ξ)^{−1} X_ξ^T)y. Let β̂_ξ denote the OLS estimator of β_ξ. Then we have R*_ξ < R_ξ < R*_ξ + ω_ξ, where ω_ξ = λ_2 β̂′_ξ β̂_ξ.
For any model k and the true model t,
    π(k|D_n)/π(t|D_n) ≤ (r_n/(P_n − r_n))^{|k|−|t|} · K_2^{|t∖k|}/K_1^{|k∖t|} · {(2b_0 + R_t)/(2b_0 + R_k)}^{n/2+a_0}
                      ≤ (r_n/(P_n − r_n))^{|k|−|t|} · K_2^{|t∖k|}/K_1^{|k∖t|} · {(1 + 2b_0/R*_t + ω_t/R*_t)/(R*_k/R*_t)}^{n/2+a_0},    (25)
where K_1 = K_2 = √(n + 1) if V_ξ^{−1} = X_ξ^T X_ξ/n; and K_1 = √(n l_n + 1), K_2 = √(n l′_n + 1) if V_ξ = I [as printed].
```
Song & Liang (2015), on-line supplement, supp p. 14, proof of Theorem S, continued [SS-P14; transcribed from supp p. 14 image]:
```
Since R*_t follows σ*²χ²_{n−|t|}, we have R*_t = σ*² n(1 + ε_n) as n becomes large, where ε_n = o_p(1), since R*_t/(n − |t|) →^{a.s.} 1. The OLS estimator β̂_t follows a normal distribution with mean β*_t and covariance matrix (X_t^T X_t)^{−1}. Since the eigenvalue of (X_t^T X_t)^{−1} is smaller than 1/(n l_n), we have Var(ω_t) is of smaller order than λ_2²/n² l_n² and ω_t = λ_2 Σ_{i∈t} |β*_i|² + o_p(1). Therefore, {1 + 2b_0/R*_t + ω_t/R*_t}^{n/2+a_0} = O_p(1).
For the rest terms, we first consider the case that t ⊂ k and |k| − |t| = d. … By log(K_1/r_n) ≻ √(log(P_n)) and [display omitted] →_p 0, we conclude that sup_{t⊂k} π(k|D_n)/π(t|D_n) →_p 0.
Now we consider the case k ⊄ t. Let u = t ∪ k and d′ = |u| − |k| = |t∖k| < |t|, then
    R*_t/R*_k = (R*_t/R*_u)(R*_u/R*_k).
```
Song & Liang (2015), on-line supplement, supp p. 15, proof of Theorem S, end; remark on (22) and (26) [SS-P15; transcribed from supp p. 15 image]:
```
It suffices to show
    max_{k⊄t} [R*_u/R*_k]^{n/2+a_0} (P_n K_2/r_n)^{d′} = o_p(1).
We know that (R*_k − R*_u)/σ*² and R*_u/σ*² are independent. The former follows χ²_{d′}(C), and the latter follows χ²_{n−|u|}, where the noncentrality parameter C = β*_t^T X_t^T (P_{X_u} − P_{X_k}) X_t β*_t = β*_t^T X_t^T (I − P_{X_k}) X_t β*_t ≥ n l_n c², P. is the projection matrix, n l_n is the lower bound of the eigenvalues of X_u^T X_u, and c = min_{i∈t} |β*_i|. Therefore,
    R*_u/R*_k = R*_u/(R*_u + (R*_k − R*_u)) ≤ R*_t/(R*_t + (R*_k − R*_u)).
By Theorem 2.1 of Inglot (2010), with probability (1 − 2e_2),
    max_{k⊄t} (R*_k − R*_u)/σ² > { √(n l_n c²) − √(2 log(r̄_n P_n^{r̄_n}/e_2)) }².
Because n l_n ≻ log r̄_n + r̄_n log P_n, we have max_{k⊄t} (R*_k − R*_u)/σ² > n l c²(1 + o(1)) [as printed]. Therefore, with probability (1 − 2e_2),
    max_{k⊄t} (K_2 P_n/r_n)^{d′} (R*_u/R*_k)^{n/2+a_0} ≤ exp{ −(n/2 + a_0) log[1 + l_n c² (1 + o(1))/(1 + ε_n)] + d′ log P_n − d′ log r_n + d′ log K_2 }.
Since n l_n ≻ log P_n + log K_2, we conclude that max_{k⊄t} [R*_u/R*_k]^{n/2+a_0} = o_p{(r_n/K_2 P_n)^{d′}}.
In summary, we have max_{k≠t} π(k|D_n)/π(t|D_n) →_p 0.    □
This theorem implies that the true model t can be identified asymptotically by just finding out the MAP model under the posterior (7) of the main text. Regarding the eigen-structure condition (22) and the choice of V_ξ, we have the following remarks:
• It is worth noting that the eigenvalue condition (22) is hardly satisfied, although similar conditions have been used in the literature, see e.g., Johnson and Rossel (2012). A feasible condition can be as follows: There exist two sequences {l_n} and {l′_n} and a constant C such that for any model |ζ| = r̄_n + |t|,
    Pr{ n l_n > ch′_1(X_ζ^T X_ζ) or ch_1(X_ζ^T X_ζ) > n l′_n } < e^{−nC}.    (26)
Since the condition r̄_n ln P_n ≺ n holds, (26) implies that, for sufficiently large n,
    Pr{ ∃ |ζ| = r̄_n + |t|, n l > ch′_1(X_ζ^T X_ζ) or ch_1(X_ζ^T X_ζ) > n l′ } < e^{−nC/2}  [subscripts of l, l′ as printed].
Hence, if (22) is replaced by (26), Theorem S still holds. The condition (26) does not require the eigenvalues of the sample covariance matrix to be bounded, but restricts the tail distribution of eigenvalues. Hence, it is more reasonable and acceptable.
```
Song & Liang (2015), on-line supplement, supp p. 16–17, remarks; Corollary S_1; §3.2 and Lemma S_2 [SS-P16; transcribed from supp p. 16 and supp p. 17 images]:
```
• The condition (26) is similar to but somewhat weaker than the concentration condition used in Fan and Lv (2008). The concentration condition constrains the eigen-structure of any n × p̃ subdata matrix for any p̃ > cn for some constant c, while the condition (26) only constrains the eigen-structure of n × (r̄_n + |t|) subdata matrix. In particular, condition (26) holds when x follows a Gaussian process, and the eigenvalues of Var(x) are bounded by l_n and l′_n (see Appendix A.7 of Fan and Lv (2008)). For a further study of the limit behavior of the spectral structure, see e.g. Silverstein (1985), Bai and Yin (1993), and Ledoux (2007).
• Choosing V_ξ^{−1} as a function of the sample covariance matrix makes use of the data information in the prior, and as a result, a slightly weaker condition is required for the consistency of variable selection. It follows from the theory of least square regression, a natural choice of V_ξ^{−1} is V_ξ^{−1} = X_ξ^T X_ξ/n. However, for binary data, even if n > |ξ|, one may still encounter the problem of singularity of X_ξ^T X_ξ. To address this issue, we set V_ξ^{−1} = (X_ξ^T X_ξ + τI)/n for some small τ in our simulations. It can be shown that this choice leads to the same consistency result as with the sample covariance matrix (see Lemma A.2 of the Appendix). This choice also automatically meets the eigenvalue condition of V_ξ in Corollary 2.1 of the main text for a standardized dataset.
Corollary S_1 Consider a linear regression with a sparse true model t. Assume that P_n < n^{κ log n} for some κ ∈ (0, 1/4), and the prior in Section 2.1.1 of the main text is used with V_ξ^{−1} = X_ξ^T X_ξ/n or V_ξ^{−1} = X_ξ^T X_ξ/n + τI/n. Let
    r̄_n ≺ log^{k_1}(n), or r̄_n ≺ n^q,
for some k_1 > 0 or q ≤ 1/2 − √κ, and
    l′_n = l_n^{−1} = √n/log^{k_2}(n),
for some k_2 > 0. Then the consistency of the MAP model holds.
3.2 Search for the MAP model
To search for the MAP model, a straightforward algorithm is simulated annealing (Kirkpatrick et al., 1983). However, as known by many people, simulated annealing can get trapped into a local mode due to the use of a non-logarithmic cooling schedule. Since SAMC has been applied to simulate from the posterior distribution for estimating the marginal inclusion probability, it is natural to use the sampled highest posterior probability model to estimate the MAP model. It follows from the following lemma that this estimator is consistent. In the context of MAP model searching, the function g(·) in Lemma S_2 can be interpreted as the posterior probability of a subset model.
Lemma S_2 Let X, X_1, …, X_n denote a sequence of random variables drawn from a sample space 𝒳. Let g : 𝒳 → R be a Borel function. Suppose that g is continuous with P_X probability 1, where P_X is the probability measure induced by the random variable X.
[p. 17] (i) If X_n ⇒ X, then g(X_n) ⇒ g(X), where ⇒ denotes convergences in distribution (Serfling, 1980, p.24).
(ii) If there exists a subsequence {X_{n_k}} such that {g(X_{n_k})} are mutually independent, then max_n g(X_n) → g* = sup{x : Pr(g(X) > x) > 0} in probability.
Proof. Part (i) is a partial restatement of a Theorem in Serfling (1980, p.24). Part (ii) can be proved as follows. … which concludes the proof of part (ii).    □
```

[Preparer's note, not a quotation.] The supplement has 20 pages: §1 proofs of the main results (pp. 1–8: Theorems
2.1–2.4, Lemmas 1.1, 1.2), §2 the SAMC algorithm and its implementation (pp. 8–13), §3 the MAP model (pp. 13–17:
Theorem S, Corollary S_1, Lemma S_2), §4 a simulation comparison with the horseshoe prior (pp. 17–19), references
(pp. 19–20). It numbers the main-text results as Theorems 2.1–2.4 and refers to conditions (A_1), (A_2), (B_1) without
defining these labels; matching by content, Theorem 2.3 is the main text's Theorem 3 (same conclusion, p. 956) and
(B_1) is used as the main text's Condition 3 (p. 955) is. "Lemma A.2 of the Appendix" (p. 16) is not in the
supplement. Statements about what the sampler returns: the preparer searched the text of all 20 pages for "converg"
and "consisten" and read each hit; those on the sampler are on pp. 9–10, 12–13, 16–17 and are all excerpted above.

## 4. Items under test

### item1 — B4: size of the nonzero coefficients
**(a) Our text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 106–106:
```
  106| - **(A3) Bounded coefficients.** $\max_{j}|\theta^*_j|\le\bar\theta$ for a fixed $\bar\theta<\infty$.
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 111–112:
```
  111| - **(A6) Beta-min.** $\theta^*_{\min}\ge C_\beta\,\sigma_*\sqrt{\log n/n}$ with a fixed $C_\beta>0$ such that
  112|   $C_\beta^2\varphi_0^2>c_0(s_0,A)$ [S1-F1]; or $\theta^*_{\min}\sqrt{n/\log n}\to\infty$.
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 272–273:
```
  272| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ is fixed and $b_{\mathrm{lo}}\le|\beta^*_j|\le b_{\mathrm{hi}}$ for
  273|   $j\in S_0$, with fixed $0<b_{\mathrm{lo}}\le b_{\mathrm{hi}}<\infty$.
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 670–671:
```
  670| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  671|   $S_0$.
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1042–1042:
```
 1042| - **(A5) Bounded signal.** $|\beta^*_j|\,\mathrm{sd}(x_j)\le\bar b\,\sigma_*$ for every $j$.
```

**(b) Song–Liang passages** (in §2–§3 above): SL-M3, SL-C3, SL-T2, SL-T3, SS-T23, SS-TS, SS-P14, SS-P15
**(c) The audit's sentences under test (verbatim).**
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 99–109:
```
   99| ## B4. Signal size: bounded above, and fixed nonzero or beta-min at √(log n/n) below
  100| (Thm 1 (A3), (A6); Thm 2 (A2); Thm 6 / 10 (A2); Thm 9 (A5); none below in Thm 9.)
  101| **Verdict: stronger than what Song–Liang state** under strict sparsity (4), on both sides; comparable to their Theorem 1
  102| on the upper side only. Above: their (3) with |x_i| ≤ 1 (Theorem 1, p. 952) bounds the signal; under (4) alone their
  103| main text states no bound. Below: their Theorem 3 (p. 956) states **no** beta-min; a true predictor needs only to be
  104| "identifiable" (Condition 3, p. 955). **In substance the same as the setting their proofs use** (v1.3): the proof of
  105| their Theorem 3 gives d²(f*, f) ≥ min{1, β*_t²/(4σ*² + 4σ₂²)}·δ_n (supp p. 5), so "d(f*, f) ≥ ε_n" needs β*_t bounded away
  106| from zero; the proof of Theorem S uses the constant c = min_{i∈t}|β*_i| (supp p. 15). A coefficient of size 1/n
  107| satisfies (4) and their stated conditions, and violates ours — and their conclusions. Our fixed-design theorem goes
  108| below their implicit level, to √(log n/n). **Does it matter
  109| for our designs? No:** all have fixed nonzero coefficients.
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 293–294:
```
  293| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  294| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 298–298:
```
  298| | B4 | signal bounded; fixed nonzero or beta-min (1, 2, 6, 10; 9 above only) | same as the setting of their proofs (coefficients treated as constants, supp pp. 5, 15); stronger than their statements, which give no size condition; Thm 1 allows smaller signals | in | in | in |
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 379–380:
```
  379| | Item | Label | Why (page / equation) |
  380| |---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 383–383:
```
  383| | B4 signal size | **changed**: "stronger than what they state" → same as the setting of their proofs; stronger than their statements only | proof of their Thm 3: d² ≥ min{1, β*_t²/(4σ*² + 4σ₂²)}δ_n (supp p. 5); proof of Theorem S: c = min\|β*_i\| constant (supp p. 15) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ f98cf498, lines 49, 83, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   49| | Beta-min at √(log n/n) (Thm 1 (A6)); fixed nonzero signals (Thm 2 (A2)) | fixed signals: same as the setting of their proofs (supp pp. 5, 15), not stated in their theorems; Thm 1's beta-min: weaker (smaller signals allowed) |
   83| | (A2) s₀ fixed, fixed nonzero signals | sparsity: same as (4), p. 950; signal size: same as the setting of their proofs (supp pp. 5, 15), stronger than their statements |
```
`Theory_work/Wave3/W3-AUDIT/WRITING_DELTA_v1.3.md` @ f98cf498, lines 16–19:
```
   16| **Four sentences to change wherever they appear.**
   17| 1. Coefficient size. Old: "stronger than what Song–Liang state". New: "Song–Liang's theorems state no condition on the
   18|    size of the nonzero coefficients, but their proofs treat them as constants (supplement pp. 5 and 15); our theorems
   19|    state this, and the fixed-design theorem allows signals down to √(log n/n)."
```

**(d) Verdicts under test.**
- `item1:B4.PROOFS` — "same as the setting of their proofs": their proofs treat the nonzero coefficients as constants (supp pp. 5 and 15), so "d(f*, f) ≥ ε_n" needs β*_t bounded away from zero and the proof of Theorem S uses c = min_{i∈t}|β*_i| as a constant (TRACK_B.md:104-107, :298, :383; AUDIT.md:49, :83; WRITING_DELTA_v1.3.md:17-19)
- `item1:B4.STATED` — "stronger than their statements, which give no size condition": a coefficient of size 1/n satisfies (4) and their stated conditions, violates ours and their conclusions; and our fixed-design theorem allows signals down to √(log n/n), below their implicit level (TRACK_B.md:101-108, :298; AUDIT.md:49; WRITING_DELTA_v1.3.md:17-19)

### item2 — B5 and B6 against Theorem S
**(a) Our text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 107–110:
```
  107| - **(A4) Sparse eigenvalue floor.** $\lambda_{\min}(\hat R_S)\ge\varphi_0^2$ for every $S\subseteq[p]$ with
  108|   $|S|\le 2(A+1)s_0+2$, for a fixed $\varphi_0\in(0,1]$.
  109| - **(A5) No near-collinearity among $O(\log n)$ columns.** $\lambda_{\min}(X_S^\top X_S)\ge g_0$ for every $S$ with
  110|   $|S|\le 3(A+1)(s_0+1)\log n$, for a fixed $g_0>0$.
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 128–131:
```
  128| - **(A4′) Floor on the truth and an identifiability margin.** $\lambda_{\min}(\hat R_{S_0})\ge\varphi_0^2$, and every model
  129|   $S$ with $|S|\le K$, $S_0\not\subseteq S$ and at most $j_0:=\lceil(2A+1)s_0\rceil+1$ variables outside $S_0$ leaves
  130|   residual signal $\|(I-P_S)X\theta^*\|^2\ge c\,\sigma_*^2\log n$, with a fixed $c>c_1(s_0,A)$, where $c_1(s_0,A)$ is an
  131|   explicit constant, not optimised [H5-6],
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 274–276:
```
  274| - **(A3) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge\varphi^2$ for every $S$ with
  275|   $|S|\le 5(A+1)(s_0+1)\log n$, for a fixed $\varphi\in(0,1]$ (for instance, $\lambda_{\min}(\Sigma_n)\ge\varphi^2$).
  276| 
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1040–1041:
```
 1040| - **(A4) No near-exact collinearity.** $\lambda_{\min}(\mathrm{Corr}(x_T))\ge c_\psi/n$ for every set $T$ of at most $q_n$
 1041|   predictors.
```
`Theory_work/Wave3/W3-POST/STATEMENT.md` @ e8b5351c, lines 68–73:
```
   68| - **(F_λ) anchored floor, bounded size** = SE_λ(j₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}/(n−1)) ≥ φ₀² for every J ⊆ [p]∖S₀ with
   69|   |J| ≤ j₀ (J = ∅ included: this contains R's condition on S₀). *By interlacing it implies* λ_min(R_S) ≥ φ₀² for
   70|   **every** S with |S| ≤ j₀ (S ⊆ S₀ ∪ S), so it excludes e.g. duplicated null columns [R02-F2].
   71| - **(F_w) anchored unnormalised floor, logarithmic size** = SE_w(m♯_n; g₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ g₀ for every
   72|   J ⊆ [p]∖S₀ with |J| ≤ m♯_n (m♯_n = O(log n) under R1). By interlacing it implies λ_min(G_S) ≥ g₀ for every S with
   73|   |S| ≤ m♯_n: no exact linear dependence among ≤ m♯_n columns [R02-F2].
```

**(b) Song–Liang passages** (in §2–§3 above): SL-C3, SL-C3S, SL-T3, SS-TS, SS-P15, SS-P16
**(c) The audit's sentences under test (verbatim).**
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 117–121:
```
  117| ## B5. Eigenvalue floor on small sets (Thm 1 (A4) / (A4′); Thm 2 (A3); Thm 6 / 10 floors; Thm 9B (A6a))
  118| **Verdict: stronger than Song–Liang's Condition 3 in level** (fixed against vanishing), for a stronger conclusion than
  119| their Theorem 3; **not ordered in set size.** Theorem 2's sets have O(log n) columns and theirs r̄_n + 1 with any
  120| r̄_n → ∞: ours are the larger when r̄_n ≺ log n (then, for Gaussian predictors, our floor implies their condition) and
  121| the smaller when r̄_n ≻ log n. Only the bounded-set floors (Thm 1 (A4), (A4′)) are on smaller sets throughout.
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 129–133:
```
  129| conclude exact selection with a rate. *Against Theorem S (v1.3; details in §S):* **not ordered.** Its condition (22)–(23)
  130| (supp p. 13) is two-sided and on every model of |t| + r̄_n columns: n·l_n < ch′₁(X_ζᵀX_ζ) ≤ ch₁(X_ζᵀX_ζ) < n·l′_n with
  131| r̄_n log P_n ≺ n·l_n. Ours is stronger only in asking a fixed level on bounded sets; it is weaker in having no upper
  132| bound, a floor of order 1/n on O(log n) columns (B6) and nothing on larger sets. Both are implied by λ_min(Σ_n) ≥ c, the form a reader will check first. **No upper
  133| eigenvalue bound is used**, so pervasive factors are allowed. Thm 1′ replaces the floor off S₀ by a residual-signal
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 147–151:
```
  147| ## B6. No near-exact collinearity among O(log n) columns
  148| (Thm 1 (A5): λ_min(X_SᵀX_S) ≥ g₀; Thm 9 (A4): λ_min(Corr(x_T)) ≥ c_ψ/n.)
  149| **Verdict, two comparators.** *Against their Theorems 1–2 (Hellinger; the comparator of Thm 9 (A4)):* **stronger** —
  150| they have no design eigenvalue condition. *Against their Theorem 3 (selection; the comparator of Thm 1 (A5)):*
  151| **weaker in level on sets that contain a true predictor, additional on sets of null columns only.** Condition 3
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 154–157:
```
  154| ask nothing, because Theorem 3 does not control specificity. *Against Theorem S (v1.3):* **weaker** — its floor (22)
  155| covers every model of |t| + r̄_n columns, null-only ones included, at a level l_n ≻ r̄_n log P_n / n far above ours; so the
  156| "additional on null-only sets" holds against Theorem 3 only. The floor is very weak in absolute terms and of the same
  157| order as a ridge term SL put in their prior. Thm 1 (A5) is a condition on the sample Gram matrix; Thm 9 (A4) on the
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 293–294:
```
  293| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  294| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 299–300:
```
  299| | B5 | eigenvalue floor on small sets (1, 2, 6, 10, 9B) | against Condition 3 / Thm 3: stronger in level, set size not ordered. Against Theorem S (22)–(23), supp p. 13: not ordered — stronger only in the fixed level on bounded sets; no upper bound, nothing on larger sets | in | **in** | in |
  300| | B6 | no near-exact collinearity on O(log n) sets (1, 9) | against Thm 1–2: stronger (none there). Against Thm 3: weaker in level on sets with a true predictor, additional on null-only sets. Against Theorem S: weaker (their floor covers all sets at a higher level) | in | in | in |
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 379–380:
```
  379| | Item | Label | Why (page / equation) |
  380| |---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 384–385:
```
  384| | B5 eigenvalue floor | **changed against the new comparator**: stronger in level (against Condition 3) → not ordered against Theorem S | (22)–(23), supp p. 13: two-sided, vanishing level, on \|t\| + r̄_n columns |
  385| | B6 collinearity floor | **changed in part**: "additional on null-only sets" holds against Thm 3 only; against Theorem S ours is weaker | (22) covers every model ζ, null-only included |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ f98cf498, lines 47, 48, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   47| | Sparse eigenvalue floor on bounded sets (Thm 1 (A4)); floor on S₀ + residual-signal margin (Thm 1′ (A4′)); population floor (Thm 2 (A3)) | against Theorem S (22)–(23), supp p. 13: not ordered — stronger in the fixed level on bounded sets; weaker in having no upper bound and nothing on larger sets. Against Condition 3, p. 955: stronger in level, set size not ordered |
   48| | No near-collinearity among O(log n) columns (Thm 1 (A5)) | against Theorem S (22): weaker (g₀/n against n·l_n with l_n ≻ r̄_n log P_n / n, all sets). Against Thm 3 / Condition 3, p. 955: weaker on sets with a true predictor, additional on null-only sets |
```
`Theory_work/Wave3/W3-AUDIT/WRITING_DELTA_v1.3.md` @ f98cf498, lines 20–22:
```
   20| 2. Eigenvalue floor. Keep "stronger in level than their Condition 3". Add: "Their selection theorem (Theorem S) asks
   21|    two-sided eigenvalue bounds on every model of |t| + r̄_n columns ((22)–(23)); ours has no upper bound and, beyond
   22|    bounded sets, only a 1/n-level floor on O(log n) columns."
```

**(d) Verdicts under test.**
- `item2:B5.S` — B5 against Theorem S is "not ordered": ours is stronger only in asking a fixed level on bounded sets, and weaker in having no upper bound, a floor of order 1/n on O(log n) columns and nothing on larger sets (TRACK_B.md:129-132, :299, :384; AUDIT.md:47; WRITING_DELTA_v1.3.md:20-22)
- `item2:B6.S` — B6 against Theorem S is "weaker": their floor (22) covers every model of |t| + r̄_n columns, null-only ones included, at a level l_n ≻ r̄_n log P_n / n far above ours, so "additional on null-only sets" holds against their Theorem 3 only (TRACK_B.md:154-156, :300, :385; AUDIT.md:48)

### item3 — What Song–Liang prove about their sampler's output
**(a) Our text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 689–697:
```
  689| Then, under the joint law of design and noise, there are data events $\mathcal G_n$ with $P(\mathcal G_n)\to1$ on
  690| which **every** admissible run that produces output reports $\hat S=S_0$, whatever its seed and the outcome of its
  691| internal calibration; in particular $P(\text{output and }\hat S\neq S_0)\to0$. If moreover the delivery conventions (S4)(i)–(iv) hold [S1-F2], $P(\text{the run produces output})=1$ for every admissible
  692| $n\ge3$ with $(n,p_{\mathrm{raw}})$ in the bounded domain $\mathfrak D$ of (S4)(v), where the code's two fixed integer limits are not
  693| reached. If in addition IDEAL-W⁺ holds ((S4)(v): the two limits lifted),
  694| $$
  695| P(\text{the run produces output})=1\ \ \text{for every admissible }n\ge3,\qquad P(\hat S=S_0)\to1 .
  696| $$
  697| The delivery statement idealises two fixed integer limits in the code (a base search cap of $10^6$, `v3_run.R:96`, and a 32-bit integer bound $2^{31}-1$ on the search cap, `cpp/v3_core.cpp:474`): the first can bind only when $n+p+1$ exceeds $2^{10^6}$, the second only when the starting model has more than about $2.1\times10^9$ variables, which needs $n\gtrsim4.3\times10^9$ since $|\tilde S_0|\le\lfloor n/2\rfloor$; without the idealisation, delivery holds on the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, and with it (IDEAL-W⁺) for every $n$ [RM2R-5].
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1088–1099:
```
 1088| contains no draws of $(\beta,\sigma^2)$. Let $\pi(\mathcal T)$ be the posterior probability of the list, and let $\hat\Pi$ (not
 1089| computed by the method) be the posterior restricted to the list: the models in $\mathcal T$, weighted in proportion to the
 1090| exponentials of their returned log-weights, each with its exact conditional posterior of $(\beta,\sigma^2)$. Under the
 1091| conditions of Theorem 9 (level-M form), with $P^*$-probability at least $1-n^{-cM}$ over the data, **every** completed run
 1092| (whatever its random numbers) with $\pi(\mathcal T)\ge n^{-cM/2}$ satisfies
 1093| $$
 1094| \hat\Pi\Big(d_H(f,f^*)>\sqrt{M\log n/n}\Big)\le n^{-cM/2}.
 1095| $$
 1096| If a completed run scored the true model $\{j:\beta^*_j\neq0\}$ and the posterior probability of that model exceeds $\tfrac12$,
 1097| then the list contains it, it is the model the method reports as most probable, and $\pi(\mathcal T)>\tfrac12$. Whether
 1098| the list carries enough posterior probability is a property of the run: the corollary does not assert it, and the output
 1099| does not certify it.
```

**(b) Song–Liang passages** (in §2–§3 above): SL-T3, SL-SAM, SS-P9, SS-P10, SS-P12, SS-P16
**(c) The audit's sentences under test (verbatim).**
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 367–375:
```
  367| **Against core 3** (the reported model). Song–Liang's statement about what their sampler reports is: "use the sampled
  368| highest posterior probability model to estimate the MAP model. It follows from the following lemma that this estimator
  369| is consistent" (supp p. 16), where Lemma S₂(ii) says that the maximum of g over draws with a mutually independent
  370| subsequence converges in probability to the essential supremum of g (supp pp. 16–17); and "it follows from Liang (2009)
  371| that q̂_j → q_j almost surely as N → ∞" for the estimated inclusion probabilities (supp pp. 12–13). Both are limits in
  372| the number of iterations N at fixed data. **Label: Song–Liang have a weaker counterpart, not none.** Ours (Theorem 6) is
  373| about the coded run at its actual budget, jointly with n, for every seed. Earlier sentences of ours that say they
  374| "prove nothing about" the sampler's output are corrected in v1.3 to "prove nothing at a finite computational budget or
  375| jointly in n". Theorem S adds no condition of the visibility or leakage kind; those comparisons (B8, B9) are unchanged.
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 226–229:
```
  226| it as a hypothesis with a rate: nulls whose conditional covariance with a truth is above o(√(log n/n)) must lie in a set
  227| of at most n^b columns; correlations below that level do not count. SL's statements on their sampler's output are limits in the number of iterations at fixed data (supp pp. 12–13,
  228| 16–17; §S), with no design condition of this kind
  229| (§3.2, p. 959, cites the SAMC algorithm), so there is no formal counterpart to compare levels with.
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 379–380:
```
  379| | Item | Label | Why (page / equation) |
  380| |---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 389–389:
```
  389| | Sampler output (core 3, core 4, Cor 9C) | **changed**: "no counterpart" → weaker counterpart | limits as N → ∞ at fixed data (supp pp. 12–13, 16–17) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ f98cf498, lines 71, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   71| | Cor 9C: returned list and its log-weights are as described | weaker counterpart: limits in the number of iterations at fixed data (supp pp. 12–13, 16–17); nothing at a finite budget or jointly in n |
```
`Theory_work/Wave3/W3-AUDIT/WRITING_DELTA_v1.3.md` @ f98cf498, lines 26–29:
```
   26| 4. Sampler output (also card row 3.1 and Corollary 9C's comparison). Old: "they prove nothing about its selection
   27|    output". New: "their statements on the sampler's output are limits in the number of iterations at fixed data (their
   28|    Lemma S₂ and a citation, supplement pp. 12–13, 16–17); they prove nothing at a finite computational budget or
   29|    jointly in n."
```

**(d) Verdicts under test.**
- `item3:SAMP.LABEL` — "Song–Liang have a weaker counterpart, not none": their statements on the sampler's output are limits in the number of iterations N at fixed data (Lemma S_2 and a citation, supp pp. 12–13, 16–17) (TRACK_B.md:367-373, :226-229, :389; AUDIT.md:71; WRITING_DELTA_v1.3.md:26-29)
- `item3:SAMP.ABSENCE` — "they prove nothing at a finite computational budget or jointly in n" (TRACK_B.md:374; AUDIT.md:71; WRITING_DELTA_v1.3.md:28-29)

### item4 — The new headline sentence
**(a) Our text.**
(our theorem statements: §1 above)

**(b) Song–Liang passages** (in §2–§3 above): all of §2 and §3
**(c) The audit's sentences under test (verbatim).**
`Theory_work/Wave3/W3-AUDIT/WRITING_DELTA_v1.3.md` @ f98cf498, lines 5–14:
```
    5| **The headline changed.** Replace the v1.2 sentence "Their assumptions are of the same kinds as Song–Liang's … where they
    6| differ ours are the stronger as stated …" by:
    7| 
    8| > The posterior theorems hold on all our designs. Their assumptions are of the same kinds as Song–Liang's and are
    9| > neither uniformly stronger nor uniformly weaker. Against their selection theorem (Theorem S of their supplement) we
   10| > ask a narrower range of p (n^A against n^{κ log n}) and a fixed eigenvalue floor on bounded sets; we ask less elsewhere:
   11| > no upper eigenvalue bound, only a 1/n-level floor on O(log n) columns and nothing on larger sets, no tuning of the
   12| > prior, and signals as small as √(log n/n) in the fixed-design theorem. Against their Hellinger theorems (1–2) we add
   13| > the range of p, a c/n collinearity floor and a row law. Our conclusions are stronger, and none of these differences
   14| > excludes any of our designs.
```
The same answer as worded in TRACK_B (context; the clauses on designs are not under test):
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 14–24:
```
   14| 1. **The posterior theorems (core 1: the true model; core 2: the true distribution) hold on all our designs** — the
   15|    2,400-fit study, P6 with its strong factors, and the 1M plan. **Their assumptions are of the same kinds as
   16|    Song–Liang's, and are neither uniformly stronger nor uniformly weaker.** The same: the model (B1), exact sparsity
   17|    (B3) and nonzero coefficients that do not shrink (B4; explicit here, implicit in their proofs).
   18|    *Against their selection theorem (Theorem S, supp p. 13)* we ask more in two places — a narrower range of p (n^A
   19|    against n^{κ log n}, B2) and a fixed floor on bounded sets (B5) — and less in four: no upper eigenvalue bound, only a
   20|    1/n-level floor on O(log n) columns and nothing on larger sets (B5, B6), no tuning of the prior, and signals as
   21|    small as √(log n/n) in the fixed-design theorem.
   22|    *Against their Hellinger theorems (1–2)* we ask more: the range of p (B2), a c/n collinearity floor (B6) and the row
   23|    law (B7). **None of these differences excludes any of our designs**, and our conclusions are stronger (posterior
   24|    mass on the true model with a rate, which implies their mode statement (24); a radius of order √(log n/n)).
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 308–312:
```
  308| **Reading.** The two posterior theorems (core 1, core 2) hold on every one of our designs, strong factors included. Their
  309| assumptions are of the same kinds as Song–Liang's and are not ordered as a whole: against their selection theorem
  310| (Theorem S) ours ask a narrower range of p and a fixed floor on bounded sets, and less everywhere else; against their
  311| Hellinger theorems ours add the range of p, a c/n collinearity floor and the row law. Our conclusions are stronger, and
  312| none of the differences excludes a design of ours. The reported-model theorem (core 3) adds two
```

**(d) Verdicts under test.**
- `item4:HEAD.ORDER` — "Their assumptions are of the same kinds as Song–Liang's and are neither uniformly stronger nor uniformly weaker" (WRITING_DELTA_v1.3.md:8-9)
- `item4:HEAD.S` — "Against their selection theorem (Theorem S of their supplement) we ask a narrower range of p (n^A against n^{κ log n}) and a fixed eigenvalue floor on bounded sets; we ask less elsewhere: no upper eigenvalue bound, only a 1/n-level floor on O(log n) columns and nothing on larger sets, no tuning of the prior, and signals as small as √(log n/n) in the fixed-design theorem" (WRITING_DELTA_v1.3.md:9-12)
- `item4:HEAD.H` — "Against their Hellinger theorems (1–2) we add the range of p, a c/n collinearity floor and a row law" (WRITING_DELTA_v1.3.md:12-13)
- `item4:HEAD.CONC` — "Our conclusions are stronger" (WRITING_DELTA_v1.3.md:13)

### item5 — Theorem S against our cores 1 and 3 (TRACK_B §S)
**(a) Our text.**
(our theorem statements and our posterior: §1 above)

**(b) Song–Liang passages** (in §2–§3 above): SL-M1, SL-M3, SL-P6, SL-P7, SL-T1, SL-T3, SS-TS, SS-P14, SS-P15, SS-P16
**(c) The audit's sentences under test (verbatim).**
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 340–365:
```
  340| ## S. Song–Liang's Theorem S (MAP consistency) against core 1 and core 3 (v1.3)
  341| 
  342| **Theorem S, hypotheses and conclusion as printed (supp p. 13).** "Let D_n be a dataset generated from model (1) of the
  343| main text with a sparse true model t. Assume condition (12) of the main text and the following eigen-structure
  344| conditions hold: For any model ζ with size |ζ| = min{|t| + r̄_n, n}, there exist a non-increasing sequence {l_n} and a
  345| non-decreasing sequence {l′_n} such that
  346|   n·l_n < ch′₁(X_ζᵀX_ζ) ≤ ch₁(X_ζᵀX_ζ) < n·l′_n, (22)   r̄_n log P_n ≺ n·l_n. (23)
  347| If, further, one of the following two condition holds: 1. n·l_n ≻ log l′_n, log(√(n·l_n)/r_n) ≻ √(log P_n), and we set
  348| V_ξ⁻¹ = I for any ξ; or 2. n·l_n ≻ l′_n, log(√n/r_n) ≻ √(log P_n), and we set V_ξ⁻¹ = X_ξᵀX_ξ/n for any ξ, then, for any
  349| model k, the posterior probability (7) of the main text satisfies: max_{k≠t} π(k | D_n)/π(t | D_n) →_p 0. (24)"
  350| Relation signs checked on the page image. Remarks (supp pp. 15–16): (22) "is hardly satisfied"; it may be replaced by
  351| the probabilistic (26), Pr{n·l_n > ch′₁(X_ζᵀX_ζ) or ch₁(X_ζᵀX_ζ) > n·l′_n} < e^{−nC} for |ζ| = r̄_n + |t|, which holds for a
  352| Gaussian process whose Var(x) has eigenvalues between l_n and l′_n. Corollary S₁ (supp p. 16): P_n < n^{κ log n},
  353| κ ∈ (0, ¼), r̄_n ≺ log^{k₁}(n) or r̄_n ≺ n^q with q ≤ ½ − √κ, l′_n = l_n⁻¹ = √n/log^{k₂}(n).
  354| 
  355| **Against core 1** (Theorem 1 is the like-for-like: fixed design, sample conditions; Theorem 2 corresponds to (26)).
  356| 
  357| | Item | Theorem S | Ours | Label for ours |
  358| |---|---|---|---|
  359| | Model, sparsity | model (1), "sparse true model t" | Gaussian linear model, s₀ fixed | **same** |
  360| | Prior | (12): 1 ≤ r_n ≤ r̄_n < P_n; V_ξ⁻¹ = I or X_ξᵀX_ξ/n; r_n tied to n and P_n by condition 1 or 2 | the coded prior, no tuning | **weaker** (no condition on hyperparameters) |
  361| | Dimension | log(√n/r_n) ≻ √(log P_n); Cor S₁: P_n < n^{κ log n} | p ≤ n^A | **stronger**, by little |
  362| | Lower eigenvalue bound | (22)–(23): above n·l_n, l_n ≻ r̄_n log P_n / n, on every model of \|t\| + r̄_n columns | fixed φ₀² on sets of ≤ 2(A + 1)s₀ + 2 columns; g₀/n on O(log n) columns; nothing beyond | **not ordered**: stronger on bounded sets (fixed level), weaker on larger sets |
  363| | Upper eigenvalue bound | (22): below n·l′_n, with n·l_n ≻ l′_n (condition 2) | none | **weaker** |
  364| | Signal size | none stated; the proof uses c = min_{i∈t}\|β*_i\| as a constant and needs n·l_n·c² to dominate r̄_n log P_n (supp p. 15) | explicit; down to C_β σ√(log n/n) | **same** as their implicit setting for fixed signals; **weaker** in Theorem 1 |
  365| | Conclusion | (24): the posterior mode is t, in probability; no rate; no claim that π(t \| D_n) → 1 | 1 − π(S₀ \| y) = O_P(√(log n/n)); HPM = MPM = S₀; PIPs | **stronger** (ours implies (24)) |
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ f98cf498, lines 80–82:
```
   80| *Against Theorem S (model selection; added in v1.3):* still stronger, by much less — their MAP consistency needs
   81| log(√n/r_n) ≻ √(log P_n) (supp p. 13, condition 2), hence log P_n ≺ (log n)²/4; Corollary S₁ (supp p. 16) states
   82| P_n < n^{κ log n}, κ ∈ (0, ¼). The range exp(Cn^α) belongs to their Hellinger theorem only.
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ f98cf498, lines 52, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   52| | HPM, MPM, PIPs from 1 − π(S₀ \| y) | Thm 3 gives screening only; their Theorem S (supp p. 13) gives the posterior mode only, (24): max_{k≠t} π(k \| D_n)/π(t \| D_n) →_p 0, with no rate; ours implies it |
```
`Theory_work/Wave3/W3-AUDIT/WRITING_DELTA_v1.3.md` @ f98cf498, lines 23–25:
```
   23| 3. Their MAP result. Old: "their MAP consistency is in their supplement" (not compared). New: "Their Theorem S gives the
   24|    posterior mode only, max_{k≠t} π(k | D_n)/π(t | D_n) → 0 in probability, with no rate; our rate for 1 − π(S₀ | y)
   25|    implies it."
```
(The core 3 paragraph of §S, TRACK_B.md:367-375, is quoted under item3.)

**(d) Verdicts under test.**
- `item5:S.QUOTE` — the audit's quotation of Theorem S, (26) and Corollary S_1 "as printed" (TRACK_B.md:342-353) agrees with the supplement
- `item5:S.MODEL` — Model, sparsity: "same" (TRACK_B.md:359)
- `item5:S.PRIOR` — Prior: ours "weaker (no condition on hyperparameters)" (TRACK_B.md:360)
- `item5:S.DIM` — Dimension: ours "stronger, by little"; their condition 2 gives log P_n ≺ (log n)²/4 (TRACK_B.md:361; TRACK_B.md:80-82 is the B2 wording)
- `item5:S.LOWER` — Lower eigenvalue bound: "not ordered: stronger on bounded sets (fixed level), weaker on larger sets" (TRACK_B.md:362)
- `item5:S.UPPER` — Upper eigenvalue bound: ours "weaker" (none) (TRACK_B.md:363)
- `item5:S.SIGNAL` — Signal size: "same as their implicit setting for fixed signals; weaker in Theorem 1" (TRACK_B.md:364)
- `item5:S.CONC` — Conclusion: ours "stronger", and "ours implies (24)" — 1 − π(S₀ | y) = O_P(√(log n/n)) implies max_{k≠t} π(k | D_n)/π(t | D_n) →_p 0 (TRACK_B.md:365, :24; AUDIT.md:52; WRITING_DELTA_v1.3.md:23-25)
- `item5:S.CORE3` — "Theorem S adds no condition of the visibility or leakage kind" (TRACK_B.md:375)

---

## Task (sent as a separate block)

Break the comparison; findings only.

Verdicts to judge (19), in this order; return one machine line for each:
item1:B4.PROOFS
item1:B4.STATED
item2:B5.S
item2:B6.S
item3:SAMP.LABEL
item3:SAMP.ABSENCE
item4:HEAD.ORDER
item4:HEAD.S
item4:HEAD.H
item4:HEAD.CONC
item5:S.QUOTE
item5:S.MODEL
item5:S.PRIOR
item5:S.DIM
item5:S.LOWER
item5:S.UPPER
item5:S.SIGNAL
item5:S.CONC
item5:S.CORE3
