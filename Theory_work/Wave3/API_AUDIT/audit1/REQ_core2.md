# AUDIT1 — core2: row 2.1 (Theorem 9, 9B, Corollary 9C: the posterior finds the true distribution)

Material for a blind review of the audit's Song–Liang comparisons and inside/outside verdicts. Every excerpt is
verbatim with its file and line numbers; Song–Liang passages carry the journal page and display or condition
number. Status labels have been replaced by [status omitted] or [review omitted].

## 0. Conventions
Meaning of inside / outside (the audit's convention):
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 55–57:
```
   55| "Inside / outside" means: the design, continued as a sequence in n with its structure and s₀ fixed, satisfies the
   56| assumption. The dossiers judge the qualitative conditions (a floor bounded below, a signal on the √(log n/n) scale, a
   57| leakage set of size n^b). The explicit constants in the proofs are conservative and are not part of the judgement
```

Track C = internal proxy computations on simulated designs (no proofs, no fits of the method). Legend of its table:
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 13–18:
```
   13| ## How to read
   14| Trend is along the p = n series, n = 200 → 1600 (log-log slope in brackets). **IN↑** = inside, improving with n;
   15| **IN** = inside, bounded/flat; **UNCL↑** = unclear now, moving toward inside; **UNCL** = unclear; **OUT** = outside.
   16| Search-based floors and visibility are upper bounds (they can refute, not certify); population floors are certified by
   17| λ_min(Σ) > 0; P5 leak sets are subsets (never "inside", only "not refuted"; written IN for brevity). sp = spread truth
   18| (study positions, signs + − + −), cl = clustered (four adjacent columns, aligned signs).
```


## 1. Our theorem statements (verbatim)
Reader version, Theorem 9 / 9B / Corollary 9C (row 2.1), setting through the corollary:
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 996–1099:
```
  996| ### Setting and notation
  997| The data are $n$ independent copies $(x_i,y_i)$, $i=1,\dots,n$, of a pair $(x,y)$: $x\in\mathbb R^{p_{\mathrm{raw}}}$ is the
  998| vector of all observed predictors (a row of $X^{\mathrm r}$, §1 of the notation) and $y\in\mathbb R$ the response (an entry of
  999| $y^{\mathrm r}$). $D_n$ denotes the data set. $p_{\mathrm{raw}}$ may grow with $n$ and may be much larger than $n$; the law of
 1000| $(x,y)$ may change with $n$. As in every theorem, $p\le p_{\mathrm{raw}}$ is the number of predictors not constant in the
 1001| sample, and the method runs on these (standardisation §2, prior $\mathrm{BB}(1,p)$ capped at $\min(p,\lfloor n/2\rfloor)$, slab
 1002| and inverse-gamma prior §3; no tuning). $\Pi(\cdot\mid D_n)$ is the resulting exact posterior of $(S,\beta,\sigma^2)$, mapped
 1003| back to the original units: $S$ is the set of included predictors, $\beta\in\mathbb R^{p_{\mathrm{raw}}}$ the coefficient vector
 1004| (zero outside $S$ and on removed predictors), $\sigma^2$ the noise variance. If fewer than two predictors remain, or the
 1005| response is constant in the sample, the posterior is not defined; under the assumptions below such data sets have
 1006| probability smaller than the exceptional probabilities in the theorems and are counted in them (and $p=p_{\mathrm{raw}}$
 1007| outside them).
 1008| 
 1009| *What is estimated.* A draw $(S,\beta,\sigma^2)$ defines a conditional law of $y$ given $x$,
 1010| $N\big(\bar y+(x-\bar x)^\top\beta,\ \sigma^2\big)$, with the sample-mean intercept ($\bar y$, $\bar x$ are the sample means). The
 1011| law of $x$ is **not** estimated: $f$ denotes the joint density of $(x,y)$ in which $x$ has its true law and $y$ given $x$
 1012| has the law above, and $f^*$ is the true joint density. Because $f$ and $f^*$ share the law of $x$,
 1013| $$
 1014| d_H^2(f,f^*)=E_x\Big[H^2\Big(N\big(\bar y+(x-\bar x)^\top\beta,\sigma^2\big),\ N\big(\alpha^*+x^\top\beta^*,\sigma_*^2\big)\Big)\Big],
 1015| $$
 1016| the squared Hellinger distance between the fitted and the true conditional laws of $y$ given $x$, averaged over $x$ (with
 1017| $x$ independent of the data). This is the joint-density distance of Song and Liang (2015), Theorems 1–2 (they use
 1018| $\int(\sqrt f-\sqrt{f^*})^2=2d_H^2$).
 1019| 
 1020| *Further notation.* $H^2(P,Q):=1-\int\sqrt{dP\,dQ}$ and $d_H(f,g):=\big(1-\int\sqrt{fg}\big)^{1/2}$. $P^*$ is the distribution
 1021| of the data. $\mathrm{sd}$, $\mathrm{Var}$, $\mathrm{Corr}$ are population standard deviations, variances and correlation
 1022| matrices; $z_j:=(x_j-Ex_j)/\mathrm{sd}(x_j)$ and $z:=(z_1,\dots,z_{p_{\mathrm{raw}}})$; $x_T$ is the sub-vector of $x$ indexed by a
 1023| set $T$; $|S|$ is the number of predictors in $S$; $a\vee b:=\max(a,b)$; $\log$ is the natural logarithm.
 1024| 
 1025| *Constants, level and window.* $s\ge0$ is an integer and $A\ge1$, $L\ge1$, $c_\psi>0$, $\bar b>0$ are constants; none depends
 1026| on $n$. The reader fixes a **level** $M\ge1$ (a larger $M$ gives a larger ball and a smaller exceptional probability). The
 1027| **window** is
 1028| $$
 1029| q_n:=\min\big\{p_{\mathrm{raw}},\ \lceil C_qM\log n\rceil\big\},\qquad C_q:=2\big(s(A+2)+4\big)/\log 2 ,
 1030| $$
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
 1043| 
 1044| No lower bound on the nonzero coefficients (no beta-min condition) and no fixed lower bound on eigenvalues is assumed:
 1045| under (A4) predictors may be correlated up to $1-c_\psi/n$.
 1046| 
 1047| ### Reader statement
 1048| **Theorem 9 (distribution-level consistency).** There are constants $c>0$, $C_1$, $M_0$ and $n_0$, depending only on
 1049| $(s,A,L,c_\psi,\bar b)$, such that the following holds. Fix a level $M\ge M_0$ and assume (A1)–(A5) with the window $q_n$
 1050| of this $M$. Then for every $n\ge n_0$ with $\sqrt n/\log n\ge M$:
 1051| $$
 1052| \text{(i)}\quad P^*\Big[\,\Pi\Big(d_H(f,f^*)>\sqrt{M\log n/n}\ \Big|\ D_n\Big)>n^{-cM}\Big]\le n^{-cM}.
 1053| $$
 1054| *In words.* Except on data sets of probability at most $n^{-cM}$, the posterior gives probability at most $n^{-cM}$ to
 1055| draws whose conditional law of $y$ given $x$ is farther than $\sqrt{M\log n/n}$ from the true one in Hellinger distance
 1056| averaged over $x$: the posterior contracts at the rate $\sqrt{\log n/n}$.
 1057| 
 1058| *Level-M form.* The same constants serve every level $M$ with $M_0\le M\le\sqrt n/\log n$, which may depend on $n$:
 1059| whenever $n\ge n_0$ and (A1)–(A5) hold with the window $q_n$ of this $M$, display (i) holds, and also
 1060| $$
 1061| \text{(ii)}\quad P^*\Big[\,\Pi\big(|S|>s+C_1M\ \big|\ D_n\big)>n^{-cM}\Big]\le n^{-cM}.
 1062| $$
 1063| The two exceptional sets of data sets can be taken to be the same set, and the bounds are uniform over all laws of the
 1064| data that satisfy (A1)–(A5) with the given constants. Statement (ii) bounds the number of selected predictors; it does
 1065| not say that they are the true ones.
 1066| 
 1067| *Without (A4).* If (A4) is dropped and (A3) is required only for single predictors ($u$ with one nonzero entry), then
 1068| $$
 1069| \text{(iii)}\quad P^*\Big[\,\Pi\Big(d_H(f,f^*)>\sqrt{M\log n\cdot\log(p_{\mathrm{raw}}\vee n)/n}\ \Big|\ D_n\Big)>n^{-cM}\Big]\le n^{-cM},
 1070| $$
 1071| and (ii) holds with $s+C_1M\log n$ in place of $s+C_1M$.
 1072| 
 1073| **Theorem 9B (parametric rate when the true predictors are detectable).** Assume (A1)–(A5) with the window $q_n$ of $M=1$,
 1074| with exactly $s\ge1$ nonzero coordinates of $\beta^*$, and in addition
 1075| - **(A6) Detectable signal.** (a) $\lambda_{\min}(\mathrm{Corr}(x_T))\ge\psi$ for a constant $\psi>0$ and every set $T$ of
 1076|   at most $(2A+3)s+2$ predictors; (b) $\min\{|\beta^*_j|\,\mathrm{sd}(x_j)/\sigma_*:\beta^*_j\neq0\}\ge b_n$, where $b_n>0$ and
 1077|   $b_n^2n/\log n\to\infty$.
 1078| 
 1079| Then for every sequence $M_n\to\infty$: $\ \Pi\big(d_H(f,f^*)>M_n/\sqrt n\ \big|\ D_n\big)\to0$ in $P^*$-probability.
 1080| 
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

Master §1R (setup, prior, assumptions, Theorems A, B, Corollary C):
`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 136–162:
```
  136| **Setup.** We observe D_n = {(x_i, y_i) : i = 1, …, n}: n independent copies of a pair (x, y), where x ∈ ℝ^p is a
  137| vector of p predictors and y is a real response. The number of predictors p may grow with n and may be much larger
  138| than n; the law of (x, y) may change with n.
  139| 
  140| *What the method does.* (1) It removes the predictors that are constant in the sample, and centres and scales every
  141| other predictor, and the response, by its sample mean and sample standard deviation. Let r be the number of predictors
  142| that remain (r ≤ p). (2) On the standardised data it uses one fixed prior, with no tuning parameter: the number of
  143| included predictors has the beta-binomial BB(1, r) distribution restricted to at most min(r, ⌊n/2⌋), and given that
  144| number all sets S of that size are equally likely; given S and the noise variance, the coefficients of the predictors
  145| in S are jointly normal with mean zero and covariance n × (noise variance) × (G_S + I)⁻¹, where G_S is the sample Gram
  146| matrix of the standardised predictors in S and I is the identity matrix of the same size; the noise variance has an
  147| inverse-gamma prior with shape 0.01 and rate 0.01. (3) The posterior is mapped back to the original units.
  148| Π(· | D_n) denotes the resulting posterior distribution of (S, β, σ²): S is the set of included predictors, β ∈ ℝ^p the
  149| coefficient vector in the original units (zero outside S and for removed predictors), and σ² the noise variance in the
  150| original units. If fewer than two predictors remain, or the response is constant in the sample, the posterior is not
  151| defined here; under the assumptions below such data sets have probability smaller than the exceptional probabilities
  152| in the theorems and are counted in them (in particular r = p outside them).
  153| 
  154| *The distribution attached to a posterior draw.* A draw (S, β, σ²) defines a joint density f for a new pair (x, y): x
  155| has its true distribution and, given x, y is normal with mean ȳ + (x − x̄)ᵀβ and variance σ², where ȳ and x̄ are the
  156| sample means of the response and of the predictors. f* is the true joint density of (x, y).
  157| 
  158| *Notation.* d_H(f, g) = (1 − ∫√(fg))^{1/2} is the Hellinger distance between two densities. P* is the distribution of the
  159| data D_n. sd(·), Var(·) and Corr(·) are population standard deviations, variances and correlation matrices.
  160| z_j = (x_j − E x_j)/sd(x_j) is the j-th standardised predictor and z = (z_1, …, z_p). For a set T of predictors, x_T is
  161| the sub-vector of x. λ_min(·) is the smallest eigenvalue of a symmetric matrix. |S| is the number of predictors in S.
  162| log is the natural logarithm.
```
`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 164–238:
```
  164| **Constants, the level M and the window q_n.** s ≥ 0 is an integer and A ≥ 1, K ≥ 1, c_ψ > 0, b̄ > 0 are constants; none
  165| depends on n. Fix a number M ≥ 1, the *level*: a larger M gives a larger ball and a smaller exceptional probability.
  166| The *window* is
  167| 
  168|     q_n = min{ p, ⌈C_q·M·log n⌉ },   where C_q = 2(s(A + 2) + 4)/log 2.
  169| 
  170| It is the largest number of predictors that assumptions (A3) and (A4) constrain jointly; for a fixed level M it is of
  171| order log n. (K below is the constant of (A3); the cap on the model size is always written min(r, ⌊n/2⌋).)
  172| 
  173| **Assumptions.**
  174| - **(A1) Gaussian linear model.** y = α* + xᵀβ* + ε, where ε is normal with mean 0 and variance σ*² > 0 and is independent
  175|   of x. (α*, β*, σ* and the law of x may depend on n.)
  176| - **(A2) Sparsity and dimension.** At most s coordinates of β* are nonzero, and 2 ≤ p ≤ n^A.
  177| - **(A3) Sub-Gaussian predictors.** Every predictor has positive variance, and for every vector u ∈ ℝ^p with at most q_n
  178|   nonzero entries and every real λ:   E exp(λ·uᵀz) ≤ exp(K²λ²·Var(uᵀz)/2).
  179| - **(A4) No near-exact collinearity.** For every set T of at most q_n predictors:   λ_min(Corr(x_T)) ≥ c_ψ/n.
  180| - **(A5) Bounded signal.** |β*_j|·sd(x_j) ≤ b̄·σ* for every j.
  181| No lower bound on the nonzero coefficients is assumed (no beta-min condition), and no fixed lower bound on
  182| eigenvalues: under (A4) predictors may be correlated up to 1 − c_ψ/n. ((A4) still makes sparse coefficient vectors
  183| distinguishable in principle; the statement without (A4) below needs no such condition.)
  184| 
  185| **Theorem A (the posterior recovers the joint distribution of predictors and response).** There are constants c > 0,
  186| C₁, M₀ and n₀, depending only on (s, A, K, c_ψ, b̄), such that the following holds whenever n ≥ n₀, M₀ ≤ M ≤ √n/log n and
  187| (A1)–(A5) hold with the window q_n of this M:
  188| 
  189|     (i)   P*[ Π( d_H(f, f*) > √(M·log n / n) | D_n ) > n^{−cM} ] ≤ n^{−cM},
  190| 
  191|     (ii)  P*[ Π( |S| > s + C₁·M | D_n ) > n^{−cM} ] ≤ n^{−cM}.
  192| 
  193| In words. (i) Except on a set of data sets of probability at most n^{−cM}, the posterior gives probability at most
  194| n^{−cM} to joint distributions farther than √(M log n/n) from the truth in Hellinger distance: the posterior contracts
  195| at the rate √(log n/n). (ii) On the same data sets the posterior gives probability at most n^{−cM} to models with more
  196| than s + C₁M predictors. Statement (ii) bounds the number of selected predictors; it does not say that they are the
  197| true ones. The two exceptional sets of data sets can be taken to be the same set. The bounds are uniform over all laws
  198| of the data that satisfy (A1)–(A5) with the given constants.
  199| 
  200| *Without (A4).* If (A4) is dropped, and (A3) is required only for single predictors (vectors u with one nonzero
  201| entry), then (i) holds with the radius √(M·log n·log(p ∨ n)/n), which is larger by the factor √(log(p ∨ n)), and (ii) holds
  202| with s + C₁·M·log n in place of s + C₁·M. (Here p ∨ n is the larger of p and n.)
  203| 
  204| *Example.* Jointly Gaussian predictors satisfy (A3) with K = 1; independent predictors satisfy it when each of them
  205| satisfies it with a common constant K. (A4) holds for all large n whenever every q_n × q_n principal block of the correlation matrix has
  206| smallest eigenvalue at least a fixed ψ > 0: for instance correlation ρ^{|j−k|} with |ρ| < 1, or equal correlation
  207| ρ ∈ [0, 1).
  208| 
  209| **Theorem B (parametric rate when the true predictors are detectable).** Assume (A1)–(A5) with the window q_n of M = 1
  210| and with exactly s ≥ 1 nonzero coordinates of β*, **and in addition**
  211| - **(A6) Detectable signal.** (a) λ_min(Corr(x_T)) ≥ ψ for a constant ψ > 0 and every set T of at most (2A + 3)s + 2
  212|   predictors; (b) min{ |β*_j|·sd(x_j)/σ* : β*_j ≠ 0 } ≥ b_n, where b_n > 0 and b_n²·n/log n → ∞.
  213| Then for every sequence M_n → ∞:
  214| 
  215|     Π( d_H(f, f*) > M_n/√n | D_n ) → 0   in P*-probability.
  216| 
  217| **Corollary C (the output of the sampler).** The method uses a sequential Monte Carlo sampler to explore the models and to compute summaries
  218| of the posterior; it does not compute the full posterior
  219| (small problems that it solves by exact enumeration are not covered here). A run is *completed* when the method
  220| reports the status "completed"; runs that stop early are not covered. The output of a completed run contains a list 𝒯
  221| of at most 40r + 1 distinct models: the best-scoring models among those offered to the final run of the sampler —
  222| the models scored in that run, together with models the method scored earlier and carries into it (its precomputed
  223| tables for small groups of predictors, and models kept from its calibration stage). Each model in the list comes with
  224| the logarithm of its unnormalised posterior weight, which we take to be computed in exact arithmetic. The output
  225| contains no draws of (β, σ²). Let π(𝒯) be the posterior probability of the list, and let Π̂ — not computed by the method —
  226| be the posterior restricted to the list: the models in 𝒯, weighted in proportion to the exponentials of their returned
  227| log-weights, each with its exact conditional posterior distribution of (β, σ²). Under the conditions of Theorem A,
  228| with P*-probability at least 1 − n^{−cM} over the data, **every** completed run (whatever its random numbers) with
  229| π(𝒯) ≥ n^{−cM/2} satisfies
  230| 
  231|     Π̂( d_H(f, f*) > √(M·log n / n) ) ≤ n^{−cM/2}.
  232| 
  233| If a completed run scored the true model {j : β*_j ≠ 0} and the posterior probability of that model exceeds ½, then the
  234| list contains it, it is the model the method reports as most probable, and π(𝒯) > ½. More generally π(𝒯) is the total
  235| posterior probability of the listed models, and no single model needs to carry most of it: the posterior is in general
  236| a mixture over many models (typically the true model together with many models that add one predictor to it), and the
  237| condition above concerns the list as a whole. Whether the list carries enough posterior probability is a property of the
  238| run: this corollary does not assert it, and the output does not certify it.
```


## 2. Our designs (verbatim)
The audit's summary of our designs:
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 40–48:
```
   40| **Our designs** (all have i.i.d. Gaussian rows, σ = 1, fixed nonzero coefficients):
   41| - **Study** = the 2,400-fit study: n = 200, p ∈ {500, 1000}, s₀ = 14 (one truth per group of 5, coefficients ±0.8…1.8
   42|   times c ∈ {1, 0.5}); S1 identity; S2 AR(1) 0.5; S3 / S4 blocks of 5 with correlation 0.7 / 0.85; S5 = blocks of 5 at 0.7
   43|   **plus a global factor** (0.3 between all columns); S6 blocks of 5 with correlation 0.4–0.9
   44|   (`Scripts/Data_generators/gen_dev_data.R:18-41`; `Theory_work/Pause_2026-11/RERUN_SPEC.md:41-42`).
   45| - **P6** = strong factors, n ∈ {50,…,150}, p up to 10n, s₀ ∈ {4, 8}: `cs(ρ)` one factor, ρ ∈ {0.3, 0.5, 0.7}; `fac2` two
   46|   pervasive factors; `s5` (= S5) (`Theory_work/Wave3/W3-P6/DESIGN.md:13-17`).
   47| - **1M** = the p = 10⁶ plan: IND; AR Toeplitz 0.6 (primary); BLK blocks of 20 at 0.5; FAC `cs(0.3)` (contingent, 10⁴
   48|   only); s₀ = 5 (`/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/EXPERIMENT_PLAN.md:87-92`, untracked).
```

Generator of the 2,400-fit study (scenarios S1–S6 = cases 1–6; truth):
`Scripts/Data_generators/gen_dev_data.R` @ e8b5351c, lines 18–41:
```
   18| scenario_covariance <- function(scenario, p=500L) {
   19|   stopifnot(length(scenario)==1L, scenario %in% 1:6, p>=1L, p==as.integer(p))
   20|   group <- ceiling(seq_len(p)/5)
   21|   H <- outer(group,group,"==")
   22|   I <- diag(p)
   23|   switch(as.integer(scenario),
   24|     I,
   25|     0.5^abs(outer(seq_len(p),seq_len(p),"-")),
   26|     0.7*H+0.3*I,
   27|     0.85*H+0.15*I,
   28|     0.3*matrix(1,p,p)+0.4*H+0.3*I,
   29|     {rho <- 0.4+0.1*((group-1L)%%6L); S <- H*matrix(rho,p,p); diag(S)<-1; S})
   30| }
   31| 
   32| # Port of tools/scenario_check.py::truth (§II.3, §II.9). Uses no random numbers.
   33| truth <- function(p) {
   34|   s0   <- c(`30` = 5L, `500` = 14L, `1000` = 14L)[[as.character(p)]]
   35|   step <- c(`30` = 1L, `500` = 7L, `1000` = 13L)[[as.character(p)]]
   36|   pos  <- c(3L, 2L, 4L, 1L, 5L, 3L)
   37|   pattern <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
   38|   k <- 0:(s0 - 1L)
   39|   block <- 1L + step * k
   40|   active <- 5L * (block - 1L) + pos[(k %% 6L) + 1L]
   41|   list(active = active, beta = pattern[(k %% 6L) + 1L], block = block)
```

Study specification (designs, truth, signal):
`Theory_work/Pause_2026-11/RERUN_SPEC.md` @ e8b5351c, lines 37–42:
```
   37| | n | 200 | `RES/HEADLINE_H.md:3`; `ops/PRODH_COMPLETION_20261102.md:3` |
   38| | p | 500, 1000 | `CAMP/conformance/jobs/PROD_H/JOB.md:7` |
   39| | Designs | S1 independent; S2 AR(1) 0.5^\|j−k\|; S3 0.7H+0.3I; S4 0.85H+0.15I; S5 0.3J+0.4H+0.3I; S6 heterogeneous blocks ρ_b = 0.4+0.1((b−1) mod 6). Population blocks of 5 | `Docs/Methodology/MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.md:648–666` |
   40| | s0 / truth | 14 signals; β = (1.4, −1.0, 1.8, −1.2, 0.8, −1.6) cycled. Active p500: 3, 37, 74, 106, 145, 178, 213, 247, 284, 316, 355, 388, 423, 457. Active p1000: 3, 67, 134, 196, 265, 328, 393, 457, 524, 586, 655, 718, 783, 847 | MASTER `:621–646` |
   41| | Signal | y_c = c·Xβ + ε, σ = 1, no intercept. c ∈ {1.00 (`c100`), 0.50 (`c050`)}, both scales on the same X and ε (paired). Nominal SNR at c = 1: 24.64 (S5: 17.44) | MASTER `:609–620, 667–686`; `PROD_H/JOB.md:7` |
   42| | Reps | r001–r100 per (p, S) → 1,200 datasets × 2 scales = **2,400 fits** | `PROD_H/tables/units.tsv` (2,400 rows, 100 per p×S×c, checked by awk) |
```

P6 designs:
`Theory_work/Wave3/W3-P6/DESIGN.md` @ e8b5351c, lines 13–17:
```
   13| * **Designs (iid Gaussian rows, unit variances; the method standardises):**
   14|   `cs(ρ)` x = √ρ f + √(1−ρ) e, ρ ∈ {0.3, 0.5, 0.7}; `fac2` x_j = √.35 f₁ + √.25 (−1)^j f₂ + √.40 e_j (corr .60 / .10,
   15|   two pervasive factors); `s5` x_j = √.3 f + √.4 g_{group(j)} + √.3 e_j, groups of 5 consecutive columns (corr .7 / .3).
   16| * **Truth:** S₀_k = (k−1)·step + 3 + ((k−1) mod 2), step = ⌊p/s₀⌋ rounded down to even (v2, R01-8; v1 = ⌊p/s₀⌋, same when even), s₀ ∈ {4, 8}; β = (1.4, 1.0, 1.8, 1.2) repeated, aligned signs
   17|   (factor signal bᵀθ ≠ 0, the NEG regime); σ = 1. Truths in distinct s5 groups and alternating fac2 parity.
```

1M plan designs and truth:
`/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/EXPERIMENT_PLAN.md` (untracked file), lines 84–92:
```
   84| ### 2.2 Design families (examples only)
   85| | code | law of x (unit variances) | role | random access for test points |
   86| |---|---|---|---|
   87| | IND | iid N(0, 1) | no correlation: the cleanest feasibility case | yes |
   88| | AR | Toeplitz 0.6^{\|j−l\|} (AR(1) recursion along the columns) | metric-local (UNI-0 example), the **primary** design | yes (Markov bridge on any sorted subset) |
   89| | BLK | blocks of 20 consecutive columns, within-block correlation 0.5 (x_j = √.5 f_b + √.5 e_j) | grouped proxies, (V)/(L) with a non-trivial Q | yes |
   90| | FAC (C9) | one factor, cs ρ = 0.3 | D1 only, at 10⁴, contingent | yes |
   91| 
   92| Truth: S₀ spread evenly (k-th truth at ⌊(k − ½)p/5⌋, shifted so that no two truths share a BLK block).
```


## 3. Track C table (internal proxy computations; verbatim)
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 21–41:
```
   21| | D | design | P1–P3 floors: sample φ̂²(k=16) at n=1600 [slope]; pop λ_min(Σ) | P4 visibility v̂ = δ̂²/log n (sample) / pop | P5 leak size \|Q̂\| (pop, ε=0.2), n=200→1600 | P6 local-regression ℓ¹ tail (ν=4, q99) | P9 width 𝔴̂⁰ | P7 BM rate, margin/log n | P8 𝒪¹/r_n | P10 |
   22| |---|---|---|---|---|---|---|---|---|---|
   23| | 01 | IND | IN↑ 0.60 [+.42]; 1 | IN↑ both [+1.5] / 1 | IN 4 → 4 | IN 0 | IN −0.77 | IN↑ | IN | OUT |
   24| | 02 | AR0.5 | IN↑ 0.29 [+.28]; 0.33 | IN↑ both / 0.6 | IN sp 32→46, cl 8→10 (slow) | IN↑ 2.5→1.2 | IN↑ sp +.02→−.19 | IN↑ | IN | OUT |
   25| | 03 | AR0.8 | IN↑ 0.10 [+.19]; 0.11 | IN↑ (sp 0.005→26) / 0.22 | IN sp 109→137, cl 19→23 (slow) | IN↑ 18→6.5 | sp UNCL↑ +.54→+.02; cl IN | IN↑ | IN | OUT |
   26| | 04 | AR0.95 | IN↑ but small 0.024 [+.23]; 0.026 | sp UNCL↑ (≈0 to n=800, 0.7 at 1600); cl IN↑ / 0.05 | sp UNCL 200→585 (n^0.5); cl IN 70→87 | sp UNCL; cl IN↑ 22→8 | sp UNCL↑ +.79→+.52; cl IN↑ | IN↑ (margin small, 1.6→10) | IN | OUT |
   27| | 05 | BLK5-0.7 | IN↑ 0.22 [+.33]; 0.3 | IN↑ both / 0.37 | IN 20, 5 (bounded) | IN↑ 1.8→0.6 | IN | IN↑ | IN | OUT |
   28| | 06 | BLK5-0.85 | IN↑ 0.11 [+.33]; 0.15 | IN↑ both / 0.19 | IN 20, 5 | IN↑ | IN | IN↑ | IN | OUT |
   29| | 07 | BLK√p-0.5 | IN↑ 0.34 [+.39]; 0.5 | IN↑ both / 0.53 | UNCL sp 60→160, cl 15→40 (n^0.5 = block size √p, by design) | IN (flat ≈5 sp, ≈1 cl) | sp UNCL↑ +.26→+.07; cl IN | IN↑ | IN | OUT |
   30| | 08 | TOEP α=1 | IN↑ 0.34 [+.30]; 0.39 | IN↑ both / 0.61 | UNCL sp 180→508 (n^0.5), cl 33→76 (n^0.4) | sp UNCL ≈10–20; cl IN 2.6→2.1 | sp UNCL +.77→+.61; cl IN weak (−.02→−.11) | IN↑ | IN | OUT |
   31| | 09 | TOEP α=2 | IN↑ 0.52 [+.37]; 0.65 | IN↑ both / 0.88 | IN sp 32→53 (n^0.24), cl 8→11 | IN↑ | IN↑ | IN↑ | IN | OUT |
   32| | 10 | FAC a=.5 k=1 | IN↑ 0.59 [+.43]; 0.97–0.99 | IN↑ both / 0.79–0.99 | IN↑ Q̂ = [p] at n ≤ 400, = S₀ from n = 800 (weak factor falls below √(log n/n)) | IN (0 from n = 800) | IN from n = 800 | IN↑ | IN | OUT |
   33| | 11 | FAC a=.5 k=3 | IN↑ 0.59; 0.97–0.99 | IN↑ both / 0.79–0.99 | IN↑ as D10 | IN from n = 800 | IN from n = 800 | IN↑ | IN | OUT |
   34| | 12 | FAC a=.75 k=1 | IN↑ 0.56 [+.44]; 0.87–0.92 | IN↑ both / sp 0.38→0.58 | OUT Q̂ = [p] | OUT (≈9–17, flat) | OUT +0.84 flat | IN↑ | IN | OUT |
   35| | 13 | FAC a=.75 k=3 | IN↑ 0.56; 0.87–0.92 | IN↑ both / sp 0.38→0.58 | OUT Q̂ = [p] | OUT | OUT +0.83 | IN↑ | IN | OUT |
   36| | 14 | FAC a=1 k=1 (cs .5) | IN↑ 0.30 [+.40]; 0.5 | **sp OUT** (pop 0; sample 4e-4→0.13); cl IN↑ / 0.53 | OUT Q̂ = [p] | OUT | OUT +0.85 | IN↑ | IN | OUT |
   37| | 15 | FAC a=1 k=3 | IN↑ 0.32 [+.42]; 0.5 | **sp OUT** (pop 0; sample ≈1e-10, falling); cl IN↑ / 0.54 | OUT Q̂ = [p] | OUT | OUT +0.86 | IN↑ | IN | OUT |
   38| | 16 | S5 (0.3 global + block) | IN↑ 0.22 [+.32]; 0.3 | IN↑ both (sp 0.55→18) / sp 0.06, cl 0.36 | OUT Q̂ = [p] (global factor) | OUT | OUT +0.84 | IN↑ | IN | OUT |
   39| | 17 | S6 (blocks ρ .4–.9) | IN↑ 0.16 [+.34]; 0.1 | IN↑ both (sp ≈0 at n = 200 only) / 0.25–0.71 | IN 20, 5 | IN↑ 1.5→0.5 | IN | IN↑ | IN | OUT |
   40| | 18 | riboflavin-like | IN↑ but small 0.09 [+.21]; 0.1 | **OUT both** (pop ≈0; sample ≈0 at every n) | OUT Q̂ = [p] | OUT (≈13–21) | OUT +0.85 | IN↑ (margin 4→35) | IN | OUT |
   41| | 19 | FRED-QD-like | IN↑ but small 0.09 [+.23]; 0.1 | sp UNCL↑ (≈0 to n = 400, 10.7 at 1600; pop 0.15); cl IN↑ / 0.08 | UNCL whole 170-blocks: sp 170→672 (= 4 tiles × 170, then bounded), cl 170 | sp UNCL ≈17–19; cl IN↑ 17→8 | sp UNCL +.73→+.61; cl UNCL↑ +.75→+.13 | IN↑ | IN | OUT |
```


## 4. Items under test

### core2:B1 — (A1) Gaussian linear model, any noise level
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1034–1035:
```
 1034| - **(A1) Gaussian linear model.** $y=\alpha^*+x^\top\beta^*+\varepsilon$ with $\varepsilon\sim N(0,\sigma_*^2)$, $\sigma_*^2>0$,
 1035|   independent of $x$ ($\alpha^*$, $\beta^*$, $\sigma_*$ and the law of $x$ may depend on $n$).
```

`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 174–175:
```
  174| - **(A1) Gaussian linear model.** y = α* + xᵀβ* + ε, where ε is normal with mean 0 and variance σ*² > 0 and is independent
  175|   of x. (α*, β*, σ* and the law of x may depend on n.)
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 947, §1, model (1) [SL-M1; transcribed from p. 947 image]:
```
Consider the problem of variable selection for the linear regression model:
    y = Xβ* + ε,    (1)
where y = (y_1, …, y_n)^T ∈ ℝ^n is the response vector, n is the sample size, X = (x_1, …, x_{P_n}) ∈ ℝ^{n×P_n} is the design matrix, P_n is the number of explanatory variables (which are also known as predictors), β* is the vector of unknown regression coefficients and ε = (ε_1, …, ε_n)^T ∼ N_n(0, σ*²) is Gaussian random error. In this paper, we use the bold letter x_i to denote an n-vector realization of the ith predictor. The subscript n in P_n means that P_n is a non-decreasing function of n. … In this paper, our study of variable selection will focus on the scenario P_n ≫ n, i.e. the column dimension of X is ultrahigh.
```
Song & Liang (2015), p. 950, §2.1, density (2) [SL-M2; transcribed from p. 950 image]:
```
Let D_n = {y; x_1, …, x_{P_n}} denote a data set of n observations drawn from model (1). Let x = (x_1, …, x_{P_n})^T denote a generic observation of the P_n predictors, and let y denote a generic observation of the response variable corresponding to x. Let ν_x denote the probability measure of x. Then the true probability density of (y, x) is given by
    f*(y, x) dx dy = (1/(√(2π) σ*)) exp{−(y − x^Tβ*)²/(2σ*²)} ν_x(dx) dy = φ(y; x^Tβ*, σ*) ν_x(dx) dy,    (2)
where φ(·; μ, σ) denotes a Gaussian density function with mean μ and standard deviation σ.
```
**(c) Verdict(s) under test.**
- `core2:B1.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 63–63:
```
   63| **Verdict: same as Song–Liang** (their model (1) and density (2), p. 950).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 56–58, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   56| | Assumption | Song–Liang (2015) |
   58| | (A1) Gaussian linear model, any noise level | same: (1)–(2), p. 950 |
```

- `core2:B1.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–244:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
  244| | B1 | Gaussian linear model (all) | same: (1)–(2), p. 950 | in / in / in / in | in | in / in / in / in |
```

**(d) Track C evidence.**
(none)

### core2:B3 — (A2) at most s nonzero coefficients
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1036–1036:
```
 1036| - **(A2) Sparsity and dimension.** At most $s$ coordinates of $\beta^*$ are nonzero, and $2\le p_{\mathrm{raw}}\le n^A$.
```

`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 176–176:
```
  176| - **(A2) Sparsity and dimension.** At most s coordinates of β* are nonzero, and 2 ≤ p ≤ n^A.
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 950, §2.1, growth of P_n; sparsity conditions (3) and (4) [SL-M3; transcribed from p. 950 image]:
```
As in conventional studies of high dimensional variable selection, we consider the asymptotics of the SAM approach under the assumption that P_n increases as n increases. To be specific, we assume that P_n ≻ n^θ for some θ > 0, where b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0. In addition, we assume that the true model is sparse. Two sparseness conditions are considered in this paper. One states that most components of β* are very small such that
    lim_{n→∞} Σ_{j=1}^{P_n} |β*_j| < ∞,    (3)
where β*_j denotes the jth entry of β*. The other one is stronger but more usual, which requires that most components of β* are 0 such that
    lim_{n→∞} Σ_{j=1}^{P_n} 1{β*_j ≠ 0} < ∞.    (4)
Let ξ ⊂ {1, …, P_n} denote a subset model, which includes the indices of all selected predictors. Let |ξ| denote the number of predictors included in ξ. Thus, the strict sparsity condition (4) implies that the true model t = {i : β*_i ≠ 0, 1 ≤ i ≤ P_n} has a finite model size.
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
Song & Liang (2015), p. 953, Theorem 2 (pp. 953–954, with the note on (8)) [SL-T2; transcribed from p. 953 image]:
```
Theorem 2. Assume that the data set D_n is generated from model (1) and all the predictors satisfy condition 1. Given a sequence {ε_n}, ε_n → 0, and nε_n² → ∞, if the conditions (9)–(14) of theorem 1 hold, the model is strictly sparse, i.e. condition (4) holds, and r_n ≻ 1, then the posterior consistency still holds, i.e. there is a constant c_1 > 0 such that, for sufficiently large n,
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²).
Note that condition (8) of theorem 1 is redundant here as, for large n, r_n > |t| and Δ(r_n) = 0 hold under the sparseness condition (4). [the last words, from 'hold under', are on p. 954]
```
**(c) Verdict(s) under test.**
- `core2:B3.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 78–79:
```
   78| **Verdict: same as Song–Liang** (their strict sparsity (4), p. 950, used by Theorems 2–3; their Theorem 1 alone allows
   79| the weaker (3)).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 56–57, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   56| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 59–59, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   59| | (A2) at most s nonzero coefficients; p ≤ n^A | same as (4), p. 950 (Thm 2); narrower than (3) (Thm 1); p as in row 1 |
```

- `core2:B3.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 246–246:
```
  246| | B3 | s₀ fixed (all) | same: (4), p. 950 | in (as a sequence) | in | in |
```

**(d) Track C evidence.**
(none)

### core2:B2 — (A2) dimension 2 ≤ p ≤ n^A
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1036–1036:
```
 1036| - **(A2) Sparsity and dimension.** At most $s$ coordinates of $\beta^*$ are nonzero, and $2\le p_{\mathrm{raw}}\le n^A$.
```

`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 176–176:
```
  176| - **(A2) Sparsity and dimension.** At most s coordinates of β* are nonzero, and 2 ≤ p ≤ n^A.
```

**(b) Song–Liang text.**
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
**(c) Verdict(s) under test.**
- `core2:B2.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 69–70:
```
   69| **Verdict: stronger than Song–Liang on the upper range** (their Corollary 1, p. 954, allows P_n < exp(Cn^α), α ∈ (0, 1));
   70| **weaker on the lower range** (they assume P_n ≻ n^θ for some θ > 0, p. 950; we need no growth of p).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 56–57, cells 'Assumption' and 'Song–Liang (2015)' only ("p as in row 1"):
```
   56| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 59–59, cells 'Assumption' and 'Song–Liang (2015)' only ("p as in row 1"):
```
   59| | (A2) at most s nonzero coefficients; p ≤ n^A | same as (4), p. 950 (Thm 2); narrower than (3) (Thm 1); p as in row 1 |
```

- `core2:B2.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 245–245:
```
  245| | B2 | p ≤ n^A (all) | stronger above (Cor 1, p. 954); weaker below (P_n ≻ n^θ, p. 950) | in | in | in (A ≈ 2.6) |
```

**(d) Track C evidence.**
(none)

### core2:B7 — (A3) sub-Gaussian predictors on sparse directions
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1037–1039:
```
 1037| - **(A3) Sub-Gaussian predictors on sparse directions.** Every predictor has positive variance, and for every
 1038|   $u\in\mathbb R^{p_{\mathrm{raw}}}$ with at most $q_n$ nonzero entries and every $\lambda\in\mathbb R$:
 1039|   $E\exp(\lambda u^\top z)\le\exp\big(L^2\lambda^2\,\mathrm{Var}(u^\top z)/2\big)$.
```

`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 177–178:
```
  177| - **(A3) Sub-Gaussian predictors.** Every predictor has positive variance, and for every vector u ∈ ℝ^p with at most q_n
  178|   nonzero entries and every real λ:   E exp(λ·uᵀz) ≤ exp(K²λ²·Var(uᵀz)/2).
```

**(b) Song–Liang text.**
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
**(c) Verdict(s) under test.**
- `core2:B7.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 140–140:
```
  140| **Verdict: Thm 9 (A3) is stronger than Song–Liang's Condition 1 and implies it; Gaussian rows are stronger still.**
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 56–57, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   56| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 60–60, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   60| | (A3) sub-Gaussian predictors on sparse directions | stronger than Condition 1, p. 953 (implies it); same for Gaussian rows |
```

- `core2:B7.LEMMA`
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 181–182, cells 'Assumption' and 'Song–Liang (2015)' only (the implication proposed as a lemma; under test as stated):
```
  181| lemmas for the report: Thm 9 (A3) ⇒ their Condition 1, for every r, with δ = √(3/8)/L and M = log 2 on standardised
  182| predictors (dossier B7);
```

- `core2:B7.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 250–250:
```
  250| | B7 | Gaussian rows (2, 6, 10); sub-Gaussian sparse directions (9) | stronger than Condition 1, p. 953 (implies it) | in | in | in |
```

**(d) Track C evidence.**
(none)

### core2:B6 — (A4) no near-exact collinearity, floor c_ψ/n on O(log n) sets
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1040–1041:
```
 1040| - **(A4) No near-exact collinearity.** $\lambda_{\min}(\mathrm{Corr}(x_T))\ge c_\psi/n$ for every set $T$ of at most $q_n$
 1041|   predictors.
```
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1067–1071:
```
 1067| *Without (A4).* If (A4) is dropped and (A3) is required only for single predictors ($u$ with one nonzero entry), then
 1068| $$
 1069| \text{(iii)}\quad P^*\Big[\,\Pi\Big(d_H(f,f^*)>\sqrt{M\log n\cdot\log(p_{\mathrm{raw}}\vee n)/n}\ \Big|\ D_n\Big)>n^{-cM}\Big]\le n^{-cM},
 1070| $$
 1071| and (ii) holds with $s+C_1M\log n$ in place of $s+C_1M$.
```

`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 179–179:
```
  179| - **(A4) No near-exact collinearity.** For every set T of at most q_n predictors:   λ_min(Corr(x_T)) ≥ c_ψ/n.
```
`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 200–202:
```
  200| *Without (A4).* If (A4) is dropped, and (A3) is required only for single predictors (vectors u with one nonzero
  201| entry), then (i) holds with the radius √(M·log n·log(p ∨ n)/n), which is larger by the factor √(log(p ∨ n)), and (ii) holds
  202| with s + C₁·M·log n in place of s + C₁·M. (Here p ∨ n is the larger of p and n.)
```

**(b) Song–Liang text.**
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
Song & Liang (2015), p. 953, Theorem 2 (pp. 953–954, with the note on (8)) [SL-T2; transcribed from p. 953 image]:
```
Theorem 2. Assume that the data set D_n is generated from model (1) and all the predictors satisfy condition 1. Given a sequence {ε_n}, ε_n → 0, and nε_n² → ∞, if the conditions (9)–(14) of theorem 1 hold, the model is strictly sparse, i.e. condition (4) holds, and r_n ≻ 1, then the posterior consistency still holds, i.e. there is a constant c_1 > 0 such that, for sufficiently large n,
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²).
Note that condition (8) of theorem 1 is redundant here as, for large n, r_n > |t| and Δ(r_n) = 0 hold under the sparseness condition (4). [the last words, from 'hold under', are on p. 954]
```
**(c) Verdict(s) under test.**
- `core2:B6.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 125–126:
```
  125| **Verdict: stronger than Song–Liang's Theorems 1–2, which have no design eigenvalue condition;** very weak in absolute
  126| terms, and it is the population twin of a term SL put in their prior.
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 56–57, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   56| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 61–61, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   61| | (A4) no near-exact collinearity, floor c_ψ/n on O(log n) sets | stronger: Thm 1–2 have none; (11), (14), p. 952, are on the prior, and their ridge c_n ∝ 1/n, p. 953, is of the same order |
```

- `core2:B6.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 249–249:
```
  249| | B6 | no near-exact collinearity on O(log n) sets (1, 9) | stronger: none in Thm 1–2 ((11), (14) are on the prior, p. 952); same order as their ridge c_n ∝ 1/n, p. 953 | in | in | in |
```

**(d) Track C evidence.**
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 46–47:
```
   46| P8: 𝒪¹_n/r_n (j = 1 and 2 terms) = 1.08 → 0.92, the same in every design (the j = 1 term is design-insensitive at
   47| p = n); bounded and decreasing, not refuted. P10: δ̂_n√(p log log n) grows like n^0.55–1.1 everywhere (pre-announced).
```


### core2:B4 — (A5) bounded standardised signal
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1042–1042:
```
 1042| - **(A5) Bounded signal.** $|\beta^*_j|\,\mathrm{sd}(x_j)\le\bar b\,\sigma_*$ for every $j$.
```

`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 180–180:
```
  180| - **(A5) Bounded signal.** |β*_j|·sd(x_j) ≤ b̄·σ* for every j.
```

**(b) Song–Liang text.**
Song & Liang (2015), p. 950, §2.1, growth of P_n; sparsity conditions (3) and (4) [SL-M3; transcribed from p. 950 image]:
```
As in conventional studies of high dimensional variable selection, we consider the asymptotics of the SAM approach under the assumption that P_n increases as n increases. To be specific, we assume that P_n ≻ n^θ for some θ > 0, where b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0. In addition, we assume that the true model is sparse. Two sparseness conditions are considered in this paper. One states that most components of β* are very small such that
    lim_{n→∞} Σ_{j=1}^{P_n} |β*_j| < ∞,    (3)
where β*_j denotes the jth entry of β*. The other one is stronger but more usual, which requires that most components of β* are 0 such that
    lim_{n→∞} Σ_{j=1}^{P_n} 1{β*_j ≠ 0} < ∞.    (4)
Let ξ ⊂ {1, …, P_n} denote a subset model, which includes the indices of all selected predictors. Let |ξ| denote the number of predictors included in ξ. Thus, the strict sparsity condition (4) implies that the true model t = {i : β*_i ≠ 0, 1 ≤ i ≤ P_n} has a finite model size.
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
**(c) Verdict(s) under test.**
- `core2:B4.SL`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 89–92:
```
   89| **Verdict: comparable to Song–Liang.** Above: their (3) with |x_i| ≤ 1 (Theorem 1, p. 952) bounds the signal; under (4)
   90| alone their main text states no bound. Below: their Theorem 3 (p. 956) states **no** beta-min; a true predictor needs
   91| only to be "identifiable" (Condition 3, p. 955), and the step "d(f*, f) ≥ ε_n for any density f that does not select x_t"
   92| is in their supplement (not inspected).
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 56–57, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   56| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 62–62, cells 'Assumption' and 'Song–Liang (2015)' only:
```
   62| | (A5) bounded standardised signal | comparable: (3) with \|x_i\| ≤ 1 (Thm 1) |
```

- `core2:B4.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 247–247:
```
  247| | B4 | signal bounded; fixed nonzero or beta-min (1, 2, 6, 10; 9 above only) | comparable: (3), p. 950; no beta-min stated in Thm 3, p. 956 | in | in | in |
```

**(d) Track C evidence.**
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 45–45:
```
   45| P7: BM rate θ_min²nφ̂₀²/log n and margin Δ̂/log n grow like n^0.7–1.15 in every design and placement; M̂ is bounded.
```


### core2:A6-9B — (A6) of Theorem 9B: fixed floor on bounded sets; beta-min (parametric rate)
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1073–1079:
```
 1073| **Theorem 9B (parametric rate when the true predictors are detectable).** Assume (A1)–(A5) with the window $q_n$ of $M=1$,
 1074| with exactly $s\ge1$ nonzero coordinates of $\beta^*$, and in addition
 1075| - **(A6) Detectable signal.** (a) $\lambda_{\min}(\mathrm{Corr}(x_T))\ge\psi$ for a constant $\psi>0$ and every set $T$ of
 1076|   at most $(2A+3)s+2$ predictors; (b) $\min\{|\beta^*_j|\,\mathrm{sd}(x_j)/\sigma_*:\beta^*_j\neq0\}\ge b_n$, where $b_n>0$ and
 1077|   $b_n^2n/\log n\to\infty$.
 1078| 
 1079| Then for every sequence $M_n\to\infty$: $\ \Pi\big(d_H(f,f^*)>M_n/\sqrt n\ \big|\ D_n\big)\to0$ in $P^*$-probability.
```

`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 209–215:
```
  209| **Theorem B (parametric rate when the true predictors are detectable).** Assume (A1)–(A5) with the window q_n of M = 1
  210| and with exactly s ≥ 1 nonzero coordinates of β*, **and in addition**
  211| - **(A6) Detectable signal.** (a) λ_min(Corr(x_T)) ≥ ψ for a constant ψ > 0 and every set T of at most (2A + 3)s + 2
  212|   predictors; (b) min{ |β*_j|·sd(x_j)/σ* : β*_j ≠ 0 } ≥ b_n, where b_n > 0 and b_n²·n/log n → ∞.
  213| Then for every sequence M_n → ∞:
  214| 
  215|     Π( d_H(f, f*) > M_n/√n | D_n ) → 0   in P*-probability.
```

**(b) Song–Liang text.**
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
Song & Liang (2015), p. 956, Theorem 3 (sure screening) and the paragraphs after it [SL-T3; transcribed from p. 956 image]:
```
Theorem 3 (sure screening). Assume that all the conditions of theorem 2 hold. If a true predictor x_t (t ∈ t) is identifiable, then P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] < exp(−c_1 nε_n²), where ξ denotes a model sampled from the posterior distribution. Furthermore, if condition 2 holds, then the weaker convergence holds: lim_n P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] = 0.
The proof of theorem 3 can be found in the on-line supplementary material. Let ξ_q = {i : 1 ≤ i ≤ P_n, q_i > q} denote a model including all the predictors with the marginal inclusion probability greater than a threshold value of q ∈ (0, 1). Then it follows from theorem 3 that π(t ⊂ ξ_q) →^p 1 if all true predictors are identifiable. … Theorem S in the on-line supplementary material establishes the consistency of MAP models. Thus, we have two criteria for variable selection, by either marginal inclusion probabilities or the MAP model. Although theorem 3 states only the sure screening property (the sensitivity is asymptotically 1, but the specificity is not controlled), we suggest the use of marginal inclusion probabilities as the criterion for variable selection.
```
**(c) Verdict(s) under test.**
- `core2:A6-9B.SL`
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 56–57, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   56| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 63–63, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   63| | (A6) of Thm 9B: fixed floor on bounded sets; beta-min | no parametric-rate result in SL |
```

[Index compiled by the preparer, not a quotation.] The formal results stated in the main text of Song and Liang (2015)
are: Theorem 1 (p. 952), Theorem 2 (p. 953), Corollary 1 (p. 954), Theorem 3 (p. 956), Theorem 4 (p. 957), Corollary 2
(p. 957); Theorem S (consistency of MAP models) is in the on-line supplement, cited on p. 956, and was not read by the
audit. The main text also contains result (16) (p. 954). Sections 4–7 (pp. 959–971) are numerical studies, a
time-complexity analysis and a discussion; the preparer found no further theorem, corollary or lemma statement there.
- `core2:A6-9B.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 242–243:
```
  242| | # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
  243| |---|---|---|---|---|---|
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 247–248:
```
  247| | B4 | signal bounded; fixed nonzero or beta-min (1, 2, 6, 10; 9 above only) | comparable: (3), p. 950; no beta-min stated in Thm 3, p. 956 | in | in | in |
  248| | B5 | eigenvalue floor on small sets (1, 2, 6, 10, 9B) | comparable to Condition 3, p. 955: fixed level against vanishing, smaller sets, stronger conclusion | in | **in** | in |
```

**(d) Track C evidence.**
`Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md` @ 56dafbdd, lines 43–45:
```
   43| Rows P2 (unanchored floor at the size cutoff m♯_n, m♯ = 49–80) and P3 (FL-Q, where Q̂ fits the lattice cap) follow
   44| the P1 column: rising in n in all 19 designs (P2 slopes +0.46 to +0.68), at levels 0.017–0.35 at n = 1600.
   45| P7: BM rate θ_min²nφ̂₀²/log n and margin Δ̂/log n grow like n^0.7–1.15 in every design and placement; M̂ is bounded.
```


### core2:H — Hellinger distance (averaged conditional = joint; d² = 2d_H²)
**(a) Our assumption text.**
`Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ 7eb818e6, lines 1009–1023:
```
 1009| *What is estimated.* A draw $(S,\beta,\sigma^2)$ defines a conditional law of $y$ given $x$,
 1010| $N\big(\bar y+(x-\bar x)^\top\beta,\ \sigma^2\big)$, with the sample-mean intercept ($\bar y$, $\bar x$ are the sample means). The
 1011| law of $x$ is **not** estimated: $f$ denotes the joint density of $(x,y)$ in which $x$ has its true law and $y$ given $x$
 1012| has the law above, and $f^*$ is the true joint density. Because $f$ and $f^*$ share the law of $x$,
 1013| $$
 1014| d_H^2(f,f^*)=E_x\Big[H^2\Big(N\big(\bar y+(x-\bar x)^\top\beta,\sigma^2\big),\ N\big(\alpha^*+x^\top\beta^*,\sigma_*^2\big)\Big)\Big],
 1015| $$
 1016| the squared Hellinger distance between the fitted and the true conditional laws of $y$ given $x$, averaged over $x$ (with
 1017| $x$ independent of the data). This is the joint-density distance of Song and Liang (2015), Theorems 1–2 (they use
 1018| $\int(\sqrt f-\sqrt{f^*})^2=2d_H^2$).
 1019| 
 1020| *Further notation.* $H^2(P,Q):=1-\int\sqrt{dP\,dQ}$ and $d_H(f,g):=\big(1-\int\sqrt{fg}\big)^{1/2}$. $P^*$ is the distribution
 1021| of the data. $\mathrm{sd}$, $\mathrm{Var}$, $\mathrm{Corr}$ are population standard deviations, variances and correlation
 1022| matrices; $z_j:=(x_j-Ex_j)/\mathrm{sd}(x_j)$ and $z:=(z_1,\dots,z_{p_{\mathrm{raw}}})$; $x_T$ is the sub-vector of $x$ indexed by a
 1023| set $T$; $|S|$ is the number of predictors in $S$; $a\vee b:=\max(a,b)$; $\log$ is the natural logarithm.
```

`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 154–159:
```
  154| *The distribution attached to a posterior draw.* A draw (S, β, σ²) defines a joint density f for a new pair (x, y): x
  155| has its true distribution and, given x, y is normal with mean ȳ + (x − x̄)ᵀβ and variance σ², where ȳ and x̄ are the
  156| sample means of the response and of the predictors. f* is the true joint density of (x, y).
  157| 
  158| *Notation.* d_H(f, g) = (1 − ∫√(fg))^{1/2} is the Hellinger distance between two densities. P* is the distribution of the
  159| data D_n. sd(·), Var(·) and Corr(·) are population standard deviations, variances and correlation matrices.
```

**(b) Song–Liang text.**
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
**(c) Verdict(s) under test.**
- `core2:H.SL`
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 56–57, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   56| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 64–64, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   64| | Hellinger distance facts (averaged conditional = joint; d² = 2d_H²) | same distance (§2.1.2, p. 952) |
```

**(d) Track C evidence.**
(none)

### core2:C9C — Corollary 9C: the sampler's returned list
**(a) Our assumption text.**
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

`Theory_work/Wave3/W3-DIST/STATEMENT.md` @ e8b5351c, lines 217–238:
```
  217| **Corollary C (the output of the sampler).** The method uses a sequential Monte Carlo sampler to explore the models and to compute summaries
  218| of the posterior; it does not compute the full posterior
  219| (small problems that it solves by exact enumeration are not covered here). A run is *completed* when the method
  220| reports the status "completed"; runs that stop early are not covered. The output of a completed run contains a list 𝒯
  221| of at most 40r + 1 distinct models: the best-scoring models among those offered to the final run of the sampler —
  222| the models scored in that run, together with models the method scored earlier and carries into it (its precomputed
  223| tables for small groups of predictors, and models kept from its calibration stage). Each model in the list comes with
  224| the logarithm of its unnormalised posterior weight, which we take to be computed in exact arithmetic. The output
  225| contains no draws of (β, σ²). Let π(𝒯) be the posterior probability of the list, and let Π̂ — not computed by the method —
  226| be the posterior restricted to the list: the models in 𝒯, weighted in proportion to the exponentials of their returned
  227| log-weights, each with its exact conditional posterior distribution of (β, σ²). Under the conditions of Theorem A,
  228| with P*-probability at least 1 − n^{−cM} over the data, **every** completed run (whatever its random numbers) with
  229| π(𝒯) ≥ n^{−cM/2} satisfies
  230| 
  231|     Π̂( d_H(f, f*) > √(M·log n / n) ) ≤ n^{−cM/2}.
  232| 
  233| If a completed run scored the true model {j : β*_j ≠ 0} and the posterior probability of that model exceeds ½, then the
  234| list contains it, it is the model the method reports as most probable, and π(𝒯) > ½. More generally π(𝒯) is the total
  235| posterior probability of the listed models, and no single model needs to carry most of it: the posterior is in general
  236| a mixture over many models (typically the true model together with many models that add one predictor to it), and the
  237| condition above concerns the list as a whole. Whether the list carries enough posterior probability is a property of the
  238| run: this corollary does not assert it, and the output does not certify it.
```

**(b) Song–Liang text.**
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
**(c) Verdict(s) under test.**
- `core2:C9C.SL`
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 56–57, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   56| | Assumption | Song–Liang (2015) |
```
`Theory_work/Wave3/W3-AUDIT/AUDIT.md` @ 56dafbdd, lines 65–65, cells 'Assumption' and 'Song–Liang (2015)' only (Song–Liang column only is under test):
```
   65| | Cor 9C: returned list and its log-weights are as described | none: SL prove nothing on their sampler's output (§3.2, p. 959) |
```

[Index compiled by the preparer, not a quotation.] The formal results stated in the main text of Song and Liang (2015)
are: Theorem 1 (p. 952), Theorem 2 (p. 953), Corollary 1 (p. 954), Theorem 3 (p. 956), Theorem 4 (p. 957), Corollary 2
(p. 957); Theorem S (consistency of MAP models) is in the on-line supplement, cited on p. 956, and was not read by the
audit. The main text also contains result (16) (p. 954). Sections 4–7 (pp. 959–971) are numerical studies, a
time-complexity analysis and a discussion; the preparer found no further theorem, corollary or lemma statement there.
**(d) Track C evidence.**
(none)

### core2:SCOPE — Core-level verdict for the posterior theorems
**(a) Our assumption text.**
(core-level verdict; see §1 and the items above)
**(b) Song–Liang text.**
(none cited by the audit for this item)
**(c) Verdict(s) under test.**
- `core2:SCOPE.IO`
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 14–17:
```
   14| 1. **The posterior theorems (core 1: the true model; core 2: the true distribution) hold on all our designs** — the
   15|    2,400-fit study, P6 with its strong factors, and the 1M plan — **under assumptions that are the same as, or comparable
   16|    to, Song–Liang's.** Three items are stronger than theirs: the range of p (p ≤ n^A, B2), a collinearity floor of order
   17|    c/n on O(log n) columns (B6), and the law of the rows (Gaussian or sub-Gaussian, B7).
```
`Theory_work/Wave3/W3-AUDIT/TRACK_B.md` @ 56dafbdd, lines 24–26:
```
   24| | Core theorem | Assumptions against Song–Liang | Our designs inside |
   25| |---|---|---|
   26| | 1 and 2 (posterior) | same or comparable; stronger: B2, B6, B7 | **all** |
```

**(d) Track C evidence.**
(none)

---

## Task (sent as a separate block)

Break the comparison; findings only.

Verdicts to judge (18), in this order; return one machine line for each:
core2:B1.SL
core2:B1.IO
core2:B3.SL
core2:B3.IO
core2:B2.SL
core2:B2.IO
core2:B7.SL
core2:B7.LEMMA
core2:B7.IO
core2:B6.SL
core2:B6.IO
core2:B4.SL
core2:B4.IO
core2:A6-9B.SL
core2:A6-9B.IO
core2:H.SL
core2:C9C.SL
core2:SCOPE.IO
