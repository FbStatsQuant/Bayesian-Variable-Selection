# A-DRAFT — novelty, posterior expectations, and naive merging

Research date: 2026-11-02. Branch: `theory/A-DRAFT`; base `325b0d8`.
This is an independent research report, not an adoption or amendment of the locked register.
**PROVED** below means a complete argument is supplied here or an explicitly identified source labels its result PROVED; campaign results remain candidates. **PROOF SKETCH**, **COUNTEREXAMPLE**, **CONJECTURE**, and **OPEN** retain their meanings. No source result is upgraded by this report.

The defensible contribution is a particular exactly sampleable, globally size-coupled block start, together with analysis of when its information survives or is repaired by the actual BVS computation. Generic local-to-global correction, SMC consistency, Gibbs invariance and Rao–Blackwellisation are established ideas. The draft's §13.1 is correct if “ground truth” means the exact working posterior expectation and its limit is specified. It is false for arbitrary bounded functions if “ground truth” means the value at the generating parameter.

## 1. Adversarial novelty audit

### 1.1 Sources and scope

I read the supplied draft, `Docs/Methodology/METHODOLOGY_v3.md`, `Docs/THEORY_PRIORITIES.md`, `Docs/Theory/theorems/00_COMMON.md`, the locked register and relevant locked statements, and inspected the W-branch reports, emphasizing their statements, corrections and remaining obligations. The report snapshots are pinned in [campaign_refs.txt](results/campaign_refs.txt). `W3-PGD/REPORT.md` at that snapshot has only a draft header and an empty headline, not a completed result. The methodology's original “not implemented/not proved” header is historical; later proof-register entries are the authority for proof status, and campaign candidates are a further, separate layer.

| Requested reference | Repository availability | Primary source actually examined |
|---|---|---|
| Song & Liang (2015), *A split-and-merge Bayesian variable selection approach for ultrahigh dimensional regression*, JRSSB 77, 947–972 | **Not in `Papers/`**, including its core index. The methodology mentions a historical Windows copy, not a present repository file. | [Publisher full text](https://academic.oup.com/jrsssb/article/77/5/947/7040600), especially summary and §§2.2–2.3; DOI 10.1111/rssb.12095. |
| Zanella & Roberts (2019), *Scalable Importance Tempering and Bayesian Variable Selection* | `Papers/Core_bibliography/14_2019_Zanella_Roberts_Scalable_Importance_Tempering_and_Bayesian_Variable_Selection.pdf` | Repository PDF, especially Proposition 1, Theorem 1 and §§4.4–4.5; [author preprint](https://arxiv.org/abs/1805.00541). |
| Lindsten et al. (2017), *Divide-and-Conquer With Sequential Monte Carlo*, JCGS 26, 445–458 | **Not in `Papers/`**. | [Author preprint, §§3.3 and 4.2](https://arxiv.org/html/1406.4993), checked against [publication metadata](https://doi.org/10.1080/10618600.2016.1237363). The examined preprint is v2 (2015), not asserted identical to the journal version. |
| Schäfer & Chopin (2013), *Sequential Monte Carlo on large binary sampling spaces* | `Papers/Core_bibliography/07_2013_Schafer_Chopin_Sequential_Monte_Carlo_on_large_binary_sampling_spaces.pdf` | Repository PDF, especially §§4.1–4.3 and §5.2; [author preprint](https://arxiv.org/abs/1101.6037). |
| Del Moral, Doucet & Jasra (2006), *Sequential Monte Carlo samplers*, JRSSB 68, 411–436 | `Papers/SMC/Del_Moral_Doucet_Jasra_2006_Sequential_Monte_Carlo_samplers.pdf` | Repository journal PDF, especially §§3.3–3.4, Proposition 2, and discussion of ESS/path adaptation. |
| Gutierrez & Guhaniyogi (2022), *Bayesian Dynamic Feature Partitioning in High-Dimensional Regression With Big Data*, Technometrics 64, 224–240 | **Not in `Papers/`**. | [NSF-hosted journal PDF](https://par.nsf.gov/servlets/purl/10325416), DOI 10.1080/00401706.2021.1952899, especially §§3 and 6. Downloaded only to ignored reading space. Its separate theoretical supplement was not retrieved; no claim below certifies those proofs. |

This is a comparison against the six specified works, not proof of worldwide priority. Citations to absent repository papers are explicit primary-source additions, not invented local PDFs.

### 1.2 What v3 actually contributes, paper by paper

**Song–Liang.** Their method selects within predictor subsets, aggregates selected variables, then selects again on the aggregate. It already addresses misspecified local regressions; Theorem 3 gives sure screening, Theorem 4 concerns misspecified-posterior consistency, and the text identifies a supplementary MAP-consistency result. Thus it is inaccurate to describe their complete algorithm as merely a naive union. [Primary source](https://academic.oup.com/jrsssb/article/77/5/947/7040600).

The v3 distinction is keeping every feasible support available through strictly positive block tables and a global size prior, then targeting the specified full posterior rather than restricting inference to a screened union. **T03** is for v3's particular ridge/unit-information/BB posterior, not the first BVS consistency theorem. **T21/T38** address the finite-budget *reported*, best-ever-scored HPM; the substantive addition must be an actual discovery route. **Theorem B** concerns v3's random-order Gibbs/swap execution, not screening. **T12/T31** validate v3 evidence and marked PIP products, while **T26** concerns actual-budget evidence/PIPs in a favourable-start regime. Referee attack: if screening succeeds, a second-stage global analysis may already give adequate uncertainty; the §3 counterexample below refutes naive union, **not Song–Liang's second selection stage**. A comparative uncertainty claim about their complete method remains OPEN here.

**Zanella–Roberts.** TGS chooses coordinates state-dependently, samples modified conditionals and corrects by importance weights; Proposition 1 gives consistency of the weighted expectation estimator. Theorem 1 bounds asymptotic variance relative to Gibbs, and §4.4 explicitly provides Rao–Blackwell PIPs. Section 4.5 studies computational complexity in orthogonal and collinear BVS examples. [Primary source](https://arxiv.org/abs/1805.00541).

v3 uses an annealed particle bridge with target-invariant moves, not their modified stationary law. Its distinctive object is the block start and its discrepancy, not “tempering for BVS” or “RB PIPs.” **T03** is statistical target analysis; **T21/T38** concern scored-HPM discovery; **Theorem B** is a finite-round scoring bound for this mixed move list. **T12/T31** concern a normalising-constant product and a one-sided certificate. **T26** concerns sample-size-indexed particle budgets, not the TGS chain-length limit. Referee attack: their variance/mixing comparisons may be stronger computational results than a conditional HPM theorem. No superiority over TGS follows from any v3 theorem listed here.

**Lindsten et al.** This is the closest conceptual antecedent to the draft's broad framework. D&C-SMC recursively builds local particle populations, merges and importance-corrects them. Proposition 1 gives unbiased normalising constants; Proposition 2 gives weighted-particle consistency. Section 4.2 already bridges merged approximations to the target by geometric tempering, and its examples use conditional-ESS adaptation. [Primary source](https://arxiv.org/html/1406.4993).

v3 replaces the general recursive tree construction with exact block enumeration and a size-profile convolution that samples a globally capped, BB-coupled support law. This is a concrete BVS construction, not a new local-to-global paradigm. **T03** supplies model-specific statistical concentration. **T21/T38/Theorem B** can supply new support-discovery and repair content beyond generic particle convergence. **T12** and the fixed-data part of §2 below are specialisations; **T31** is Markov's inequality applied to a nonnegative unbiased estimator. **T26** adds a particular triangular-array sufficient condition, if its inputs hold. Referee attack: present the bridge as a specialised SMC sampler/D&C-style correction and show why the exact start plus repair analysis matters; a renamed framework alone will not survive this comparison.

**Schäfer–Chopin.** Their binary-space SMC uses a geometric bridge, ESS-controlled increments found by bisection, resampling, and fitted proposals, including a logistic-conditionals family for dependent binary variables. It recommends a broad uniform start while noting that other dominating initial distributions are possible. These ingredients already instantiate SMC for BVS. [Primary source](https://arxiv.org/abs/1101.6037).

The deltas in v3 are the specific composite start, exact capped-prior convolution, discrepancy-based candidate grid, fresh frozen final islands, and the particular mixed move round. **T03** is target-specific; **T21/T38/Theorem B** aim at support-discovery mechanisms that ordinary binary-space SMC does not automatically establish. **T12/T31** are careful estimator bookkeeping, not a new Monte Carlo principle. **T26** goes beyond a fixed-target particle limit but only under favourable-start concentration. Referee attack: the ordinary geometric bridge and even ESS bisection are not novel. Restricted candidate-set ESS does not by itself certify unseen-mode coverage, full-space weight stability or mixing.

**Del Moral–Doucet–Jasra.** SMC samplers for sequences of static distributions, their backward-kernel construction, normalising-constant estimation and particle-limit asymptotics are foundational here. Section 3.4, Proposition 2 already treats expectation and log-normaliser CLTs, including multinomial resampling at every stage. The article also discusses moving adaptively along a path using ESS. [Repository journal PDF](../../Papers/SMC/Del_Moral_Doucet_Jasra_2006_Sequential_Monte_Carlo_samplers.pdf).

v3's exact start and BVS kernels instantiate that framework. **T12** adds execution-specific recording-position and independent-calibration checks; **T31** is an immediate probabilistic corollary. Neither is a broad new SMC theorem. **T03** is a different statistical limit. **T21/T38/Theorem B** analyse scores and discovery in the concrete algorithm, which generic SMC consistency does not cover. **T26** couples the statistical sequence to budgets through a particular first-moment bound. Referee attack: re-proving the finite-state LLN is useful validation, but should not be sold as a main novelty; variance/overlap assumptions must be discharged, not hidden inside “standard regularity conditions.”

**Gutierrez–Guhaniyogi.** DFP is an online/streaming regression approach: parameter partitions and sufficient statistics support parallel approximate conditional updates, using point estimates of complementary parameters. The main paper describes pseudo-posterior convergence as data accumulate; §6 explicitly distinguishes its fixed-partition theory from a future adaptive-partition extension. This audit does not independently verify the supplementary convergence theorem. [Primary source](https://par.nsf.gov/servlets/purl/10325416).

v3's target is the exact specified finite-data support posterior; its block law is an initial distribution that is corrected, rather than the final approximation. **T03** concerns this posterior's support concentration. **T21/T38/Theorem B** concern support scoring and repair within v3's computation. **T12/T31** address unbiased evidence and islandwise RB products for a frozen final particle system. **T26** gives a conditional actual-budget conclusion, not a general result for streaming partitions. Referee attack: “partition then regain global uncertainty” already has close relatives, and an exact target with poor finite-budget overlap can be less useful than a well-performing approximation. The draft's proposed random/inferred partition (§13.3) is not the deterministic X-dependent partition of v3 and has no theorem here.

### 1.3 The theorem set: genuine content and its attack surface

| Result | Exact claim worth retaining | Status and adversarial limit |
|---|---|---|
| **T03**, with T01/T02 | Concentration of the specified standardised-data working posterior: `1−π(S0)=O_P(sqrt(log n/n))`, under its design, sparse-eigenvalue and beta-min premises. | **PROVED**, locked, under stated hypotheses. Target-specific, not an algorithm theorem. W1-T03R/W2-VT03R sharpen the size tail and restate eigenvalue conditions as candidates. They do **not** reduce the SE-free cutoff to `s0+O(s0 log n/log p)`; proof thresholds remain far beyond the study scale. |
| **T21** | Failure separates into no output, posterior failure, and truth never scored; rejected proposals count as scores. | **PROVED**, locked conditional composition. Its elementary inequality is not a strong standalone novelty. Its mathematical value comes from proving a nontrivial discovery term for actual execution. Scoring is not occupancy and does not imply accurate PIPs/evidence. |
| **T38** | Assemble a valid statistical target and a budget-valid discovery route into `P(output and wrong HPM)→0`. | Campaign **PROVED** conditional compositions; not a new locked entry. W4's fully instantiated masked LS0 route changes the method. W3-PXN's p≫n joint-family claim remains a candidate; the no-tweak one-mask NB step is **PROOF SKETCH**. W4-SHARE has conditional delivery bounds but BVS TRACK/OSC instances are **CONJECTURE/OPEN**. No general masked PIP/evidence theorem follows. |
| **Theorem B** (restated T24, not W2-T26's similarly named composition) | From an eligible state, `P(truth unscored in H rounds) ≤ P(Bin(H,c*)<v)+Hη`, with algorithm-specific progress and bad-event rates; many particles give a conditional product bound. | Campaign **PROVED** candidate inequality after W2-VT24G's first-failure repair; W2-PREM supplies a changed look-alike-family B♯. The bound may be ≥1; eligibility and small bad-event rates are substantive assumptions. A finite inequality alone is not useful finite-budget consistency. |
| **T12 / T31(i)** | `E[Zhat_r]=Z`, `E[Zhat_r RB_rj]=Z PIP_j`; nonnegative pooled evidence yields a 95% lower bound `0.05 Zhat`. | **PROVED**, locked under EX-A/EX-S/CAL. Not unbiased normalised PIPs, not a relative-error interval, not an identity for pooled evidence times primary PIP. W2-BOOK's potential-run/output bookkeeping matters because completion may be path-dependent. |
| **T26(i)–(ii)** | W2-T26 premise `(T_n+1)Δ_n→0` gives relative evidence and uniform primary-PIP consistency at actual budgets; `Δ_n=max(1−π0(S0),1−π(S0))`. | W2-T26 labels its composition **PROVED**, candidate; its ORTH compatibility proposition is **PROOF SKETCH**. No upgrade here. Favourable-start theory only. If the start already concentrates on truth, HPM discovery needs little SMC; the result supports evidence/PIPs but does not explain masked-regime success. |

Campaign corrections used rather than ignored: W3-VT37R invalidates literal truth-dominance implications and repairs them at their original proof/sketch levels; W3-VT38E repairs D2's ESS constant and the reversible extinction example; W2-VT24G corrects the original block-packing numerical implementation; W2-PREM separates terminal-trajectory independence from small acceptance of bad independence proposals. W1-EXP and W3-VEXP provide candidate progress on EXP′ but do not make all visibility/leakage/partition premises automatic. W4-T38FULL distinguishes LS0 from unmodified v3. None of these authorises calling every original conjecture proved.

**Referee verdict.** Risk 2 is real. The most plausible substantial contributions are (i) the concrete start law with exact global prior/cap handling, (ii) a jointly verified family exhibiting poor truth mass at the start but successful budgeted correction/discovery, and (iii) quantitative weight/estimator control in regimes where correction is actually needed. Item (iii) in the masked regime remains OPEN in this report; O-WSTAB's work is not presumed completed. A safe paper claim is “a BVS-specific construction and analysis within established SMC principles.” “First local-to-global Bayesian correction,” “new generic SMC consistency,” and “all uncertainty estimates are unbiased” are not defensible claims.

## 2. What convergence of posterior expectations means for v3

### 2.1 Targets and estimators

Fix valid data, `n,p`, and the v3 working model on standardised `(X,y)`. Let

\[
\Omega=\{S\subset[p]:|S|\le K\},\quad
\Pi(dS,d\beta,dv\mid y)=\pi(S\mid y)\,\kappa_S(d\beta,dv),\quad v=\sigma^2.
\]

All support masses are positive (proper priors and ridge). For bounded measurable `h`, `|h|≤M`, define

\[
f_h(S)=\int h(S,\beta,v)\,\kappa_S(d\beta,dv),\qquad
\mu_h=\Pi h=\pi f_h.
\]

The exact conditional extension is available from conjugacy:

\[
v\mid S,y\sim IG(a_0+n/2,b_0+Q_S/2),\qquad
\beta_S\mid v,S,y\sim N(nH_S^{-1}z_S,\;nvH_S^{-1}),
\]

with inactive coefficients zero. These are the **working-scale** parameters. An original/contrast-scale functional must use the preprocessing map, e.g. `θ=s_y β`, `v_raw=s_y² v`, and the column scales when raw coefficients are requested. T01 explains the contrast-model interpretation; working evidence is not raw-data evidence.

v3 currently specifies HPM, evidence and PIPs, **not an implemented general-purpose h-estimator**. The following are the precise natural estimators for the existing particle output, with the production PIP estimator identified exactly:

1. **Self-normalised terminal particle estimate.** Immediately before terminal resampling, use the last incremental weights `G_T` on the stage `T−1` population:
   \[
   \widetilde\mu_{r,N}(h)=
   \frac{\sum_iG_T(S_{r,T-1}^i) f_h(S_{r,T-1}^i)}{\sum_iG_T(S_{r,T-1}^i)}.
   \]
   After terminal resampling/mutation, normalised weights are `1/N`. One may instead use `N^{-1}Σ_i f_h(S^i)` at a fixed terminal boundary, or average the four measured-round endpoints. Old importance weights must **not** be reapplied after resampling.
2. **Joint draws.** Replace each `f_h(S^i)` by `h(S^i,β^i,v^i)` using fresh independent draws from `κ_{S^i}` conditional on the support history. This estimates the full joint posterior expectation. It is an optional conditional extension, not a claim that v3 already stores coefficient draws.
3. **Rao–Blackwell estimate.** Integrating the continuous parameters gives `f_h`. Further integrate a Gibbs label `j` by
   \[
   (K_j f_h)(S)=o_j(S,1)f_h(S^+)+(1-o_j(S,1))f_h(S^-),
   \]
   dropping the infeasible addition when the cap binds. For `Y^i_{r,u,j}` immediately before Gibbs-j in measured round `u`, define
   \[
   \widehat\mu^{RB,j}_{r,N}(h)=\frac1{4N}\sum_{u=1}^4\sum_i(K_j f_h)(Y^i_{r,u,j}).
   \]
   For `h_j=1{j∈S}`, `K_jf_{h_j}=o_j`; this is **exactly v3's recorded island PIP**. The primary estimate is the equal average over four islands. A fixed convex combination over labels is also valid for a general h.

The HPM over scored models and a point mass at that HPM are different objects; neither is a finite-data posterior expectation estimator.

### 2.2 Theorem A — fixed-data particle consistency (PROVED, candidate)

Assume EX-A, EX-S, START (locked T09(i)) and CAL. Condition on a successful calibration `c`, fixing the finite grid, move kernels, tier, `L`, four measured rounds and four islands, but let the final particle count `N→∞`. Consider the **potential uninterrupted run** (guards removed, otherwise identical).

For every bounded measurable h, all the estimators in §2.1 converge in probability and in `L²` to `μ_h`, islandwise and under primary pooling. The terminal weighted support law and every fixed terminal/prefix support law converge to `π` in total variation. Also `Zhat_r/Z→1` and `Zhat/Z→1`. In particular

\[
\max_{j\le p}|\widehat{PIP}_j-PIP_j|\longrightarrow0.
\]

For fixed `(data,c)` the mean-square errors are `O_{data,c,h}(N^{-1})`. This is an idealised particle family, not an accuracy rate claimed for the two production tiers. On the exact branch, posterior sums are already exact for the support law and any exactly evaluated `f_h`.

**Proof.** Write `q_t=q_{φ_t}` and `η_t^N=N^{-1}Σ_iδ_{S_t^i}`. At stage 0 the particles are iid from `q_0=π0` by T09(i). Thus for every state, and hence on the finite simplex, `η_0^N→q_0` in `L²` with squared error `O(N^{-1})`.

For a probability measure `η`, put

\[
\Psi_t(\eta)(f)=\frac{\eta(G_t f)}{\eta(G_t)},\qquad
\Phi_t(\eta)=\Psi_t(\eta)K_t.
\]

On the finite state space, `0<min G_t≤max G_t<∞`. Consequently `Ψ_t` is Lipschitz on the whole probability simplex: in the `l¹` norm, a valid constant is `2 max G_t/min G_t`. Markov kernels are contractions for that norm. T09 gives `q_t K_t=q_t`, so `Φ_t(q_{t−1})=q_t`.

Conditionally on the previous population, multinomial resampling followed by independent mutation makes the new particles iid from `Φ_t(η_{t−1}^N)`. For every bounded f,

\[
E[\eta_t^N f\mid\mathcal F_{t-1}]=\Phi_t(\eta_{t-1}^N)f,\qquad
\operatorname{Var}(\eta_t^N f\mid\mathcal F_{t-1})\le\|f\|_\infty^2/N.
\]

Summing state-coordinate bounds and using the Lipschitz property proves by induction the `L²`, `N^{-1}` mean-square bound and TV convergence at each of the finitely many stages. It also proves consistency of `Ψ_T(η_{T−1}^N)`, the terminal self-normalised law.

After stage T, particles are conditionally independent but need not be identically distributed given their entering states. The empirical mean after any fixed terminal transition `R` has conditional mean `η^N Rf` and conditional variance at most `M²/N`. Since `πR=π`, the same induction applies. For the pre-Gibbs-j position, define `R_j` as the mixture over uniformly random orders of the prefix preceding label j. Each fixed prefix is a product of π-invariant elementary kernels; its length depends only on the independently drawn order. Thus `πR_j=π`. Applying the same argument to `R_j` and to the bounded reward `K_j f_h`, for which `πK_j f_h=πf_h`, proves the stated recorded-RB result. Correlation between rounds does not invalidate convergence of their finite average.

The normaliser product

\[
\widehat Z_r=m(\varnothing)\bar Z_0\prod_{t=1}^T\eta_{t-1}^N(G_t)
\]

converges in `L²` at the same rate to the telescoping product `Z`. Every factor is deterministically bounded above and below for fixed data and grid. Primary pooling preserves these conclusions without needing an increasing number of islands.

For optional joint draws, conditioning on the support history leaves independent centred bounded errors with average conditional variance at most `M²/N` at an equally weighted boundary. For the terminal weighted version it is at most `M²Σ_i w_i²≤M²(max G_T/min G_T)²/N`. They vanish in `L²`. Finally, fixed p permits a finite union bound over PIPs. This proves all assertions. ∎

**CAL and adaptive ESS.** The pilot may use arbitrary ESS-driven temperature choices and select a tier. Given its complete output, the final grid is deterministic and final streams are fresh. This is exactly where CAL is used. An N-independent random calibration may be averaged out by dominated convergence. Even an N-dependent independent calibration is allowed for the fixed-n consistency conclusion if its number of stages and terminal rounds have fixed ceilings: with `D=osc(d)` and `m=|Ω|`, the simplex sampling error satisfies

\[
a_t:=\{E\|\eta_t^N-q_t\|_1^2\}^{1/2}
\le\sqrt{m/N}+2e^{(\phi_t-\phi_{t-1})D}a_{t-1}.
\]

Unrolling gives `a_t≤(t+1)2^t e^D sqrt(m/N)`, uniform over such grids. The remaining terminal steps and the evidence product have finite uniform bounds as well. The bound can be enormous and is **not** uniform in growing n,p. Without a bounded-stage or other uniform-control hypothesis, conditional convergence at each fixed calibration does not imply a triangular-array limit. If final particles themselves choose their temperatures, the conditional-iid recursion above no longer applies as written; that alternative algorithm needs a separate adaptive-SMC argument. The observed final ESS in v3 is only a flag.

### 2.3 Exact finite-N identities, and what they do not prove

**Corollary A1 (PROVED from locked T12).** At a fixed admissible terminal boundary, a pre-label recording position, or for a fixed convex average of the marked RB rewards above,

\[
E_c[\widehat Z_r\widehat\mu_r(h)]=Z\mu_h,
\qquad E_c\widehat Z_r=Z.
\tag{I}
\]

For the terminal pre-resampling estimator this also holds: multiply its ratio by `Zhat_T` to cancel its denominator, then apply T12(i.a) at stage T−1 to `G_T f_h`. For the other positions use T12(i.b,c) with `f_h` or `K_j f_h`; T09 gives `πK_j f_h=πf_h`. Conditional expectation over any optional coefficient draws preserves (I). Thus the numerator `Zhat_r muhat_r` is unbiased; the self-normalised or RB estimate itself generally is not.

In particular, for identically distributed islands given c,

\[
E_c\widehat\mu_r-\mu_h
=-\operatorname{Cov}_c(\widehat Z_r,\widehat\mu_r)/Z.
\]

The unbiased pooled numerator is `(1/4)Σ_r Zhat_r muhat_r`. Independence of the four islands conditional on c gives

\[
E_c[\widehat Z\,\overline\mu]-Z\mu_h
=-\tfrac34\operatorname{Cov}_c(\widehat Z_1,\widehat\mu_1).
\]

The primary PIP in v3 is `overline mu`, not an evidence-weighted ratio. At fixed four islands both poolings are consistent as N grows by Theorem A. At fixed N and an increasing number of independent frozen islands, only the evidence-weighted ratio is guaranteed consistent by (I) and the iid law of large numbers; equal pooling converges to the generally biased mean. This is the distinction already anticipated by T16(ii), not a reason to silently change the production estimator.

T31's `0.05 Zhat` bound follows by Markov from `E Zhat=Z`; unbiasedness alone does **not** imply concentration or fixed-N accuracy. Likewise, kernel invariance alone does not assert that particles from a poor start are already posterior draws. The resampling LLN in Theorem A and the bound below supply the missing limit arguments.

### 2.4 Theorem D — n-indexed budgets, conditional on T26's premise (PROVED, candidate)

Let n increase, with p, the design, true support, working posterior and budgets indexed by n. Use the actual four islands, `N_e=4^e max(2500,n,p)`, `T≤4 max(1000,ceil(log2(n+p+1))²)`, `L=max(4,ceil(log2(n+1)))`, and four measured rounds. Let `G_n` denote successful SMC calibration and `E_n` the exact branch. Assume EX-A, EX-S, START, CAL and **OUT**: whenever estimates are reported they equal their potential uninterrupted-run values; exact-branch output equals the exact posterior calculation. Let `O_n` be the output-available event. Assume

\[
P_0(S_{0,n}\notin\Omega_n)\to0,
\quad
\Delta_n=\sup_{0\le\phi\le1}\{1-q_{n,\phi}(S_{0,n})\},
\]
\[
P\{G_n\cap[(T_n+1)\Delta_n>\epsilon]\}\to0,
\quad
P_0\{E_n\cap[1-\pi_n(S_{0,n})>\epsilon]\}\to0
\quad(\epsilon>0).
\tag{P1}
\]

These are W2-T26's premise form, including its exact-branch clause. For any data-measurable sequence `h_n` bounded by one fixed M, independent of final-run randomness, put `μ_n=Π_n h_n`.

Then for the integrated terminal self-normalised, endpoint and fixed-label RB estimators of §2.1, islandwise and primary pooled,

\[
P\{O_n\cap[|\widehat\mu_n-\mu_n|>\epsilon]\}\to0.
\tag{D1}
\]

The same holds with the optional independent exact conditional parameter draws. Evidence satisfies `P{O_n∩[|Zhat/Z−1|>ε]}→0`, and the actual production PIPs satisfy

\[
P\{O_n\cap[\max_{j\le p_n}|\widehat{PIP}_{n,j}
-1\{j\in S_{0,n}\}|>\epsilon]\}\to0,
\tag{D2}
\]

and hence also uniform convergence to the full posterior PIPs, and `P(O_n, MPMhat≠S0,n)→0`. No assertion that `P(O_n)→1` is included. For an unconditional successful-output guarantee add that operational assumption. Conditional-on-completion consistency can be deduced if `liminf P(O_n)>0`, by division of the displayed joint-error bounds, but no conditional unbiasedness or calibration identity follows.

**Proof, with an explicit bound.** Fix data and successful calibration, with `S0∈Ω`. Write `δ=1−π(S0)`, `W_r=Zhat_r/Z`. Locked T22(iv-b), or Hölder applied to the bridge normaliser, gives

\[
\Delta=\max\{1-\pi_0(S_0),\,1-\pi(S_0)\}.
\tag{D3}
\]

Locked T14(i) gives, for **every** N,

\[
E_c|W_r-1|\le b_c:=\frac{2(T+1)\Delta}{1-\Delta}.
\tag{D4}
\]

Here is a direct sharpening of the occupancy step used in W2-T26. For any admissible terminal empirical support measure `η_r` (including any state-independent prefix), T12 yields `E_c[W_r η_r(S0^c)]=δ`. Therefore

\[
E_c\eta_r(S_0^c)
=\delta+E_c[(1-W_r)\eta_r(S_0^c)]
\le\delta+E_c|W_r-1|\le\delta+b_c.
\tag{D5}
\]

This uses `0≤η_r(S0^c)≤1`; it is not a lower-tail conditioning argument. For any `|f|≤M`, pathwise

\[
|\eta_r f-\pi f|
\le 2M\{\eta_r(S_0^c)+\delta\}.
\]

Taking expectations gives

\[
E_c|\eta_r f-\pi f|\le2M(2\delta+b_c).
\tag{D6}
\]

Apply it to `f=f_{h_n}` at terminal boundaries. Apply it to `f=K_j f_{h_n}` at the pre-label population for the general RB version, using `πK_jf=πf`. The terminal pre-resampling law has the same identity (I), so (D5)–(D6) apply there too. This controls bounded h uniformly in dimension without needing a finite-state LLN constant uniform in n. In fact the conditional mixture measures formed by integrating `κ_S` inherit support-TV control. Finite empirical continuous-parameter draws do **not** converge in TV to a continuous posterior; their bounded-functional convergence is the claim here.

For simultaneous PIPs, avoid a union bound proportional to p. Let `A_{r,u}` be the fraction of trajectories in measured round u that start off S0 or ever leave S0. With `u_π=δ/(1−δ)`, elementary reversibility gives

\[
\bar\rho:=P_{S_0}\{\text{one round ever leaves }S_0\}
\le (B+3)u_\pi.
\tag{D7}
\]

Indeed, Gibbs-j departures lead to distinct `S0 Δ {j}`, so their probabilities sum to at most `u_π`; each of the B+2 other labels contributes at most `u_π`. A first-departure union bound proves (D7), even though the labels are ordered randomly. On a trajectory that stays at S0, every recorded Gibbs conditional differs from the truth indicator by at most `u_π`. Thus, simultaneously in j,

\[
\max_j|\widehat{PIP}_{r,j}-1\{j\in S_0\}|
\le\frac14\sum_{u=1}^4 A_{r,u}+u_\pi.
\]

Use (D5) at the **start of each measured round**, justified by T12(i.b), and fresh round randomness, to obtain

\[
E_c\max_j|\widehat{PIP}_{r,j}-1\{j\in S_0\}|
\le\min\{1,\delta+b_c\}+\bar\rho+u_\pi.
\tag{D8}
\]

The right side may be capped at one. Pooling preserves the bound. Notice that no factor L appears: the evidence identity re-controls occupancy at every measured-round start. This independently justifies W2-T26's removal of the older `(L+4)ρ*→0` premise, using only locked identities.

On `G_n∩{(T+1)Δ≤x}` with `x≤1/4`, we have `δ≤Δ≤x/2`, `b_c≤3x`, `u_π≤x`, and `B≤16`; thus (D6) is at most `8Mx` and (D8) at most `24x`. Markov's inequality bounds the joint error probability by a constant times `x/ε`, plus the probability of the excluded event in (P1), plus `P(S0∉Ω)`. First let n grow and then x decrease to zero. Exact-branch expectations equal the target, while its truth-PIP error is ≤δ and is handled by the exact clause of (P1). OUT transfers errors by event inclusion, not by conditioning on completion.

For conditional draws after resampling, bounded conditional noise has variance at most `M²/N_e`, which vanishes since `N_e≥n`. For draws attached to terminal **weighted pre-resampling** particles the variance is at most `M²Σ_i w_i²`; here weight dispersion must also be justified. In fact (P1) supplies it. Apply T14 and T12 to the truncated bridge ending at T−1 (including stage 0 if T=1). Its relative-evidence L¹ error is at most `b_c`, and its target deficit is at most Δ. Thus the number `m_0` of S0 particles before terminal reweighting satisfies `E_c(1−m_0/N_e)≤Δ+b_c`, so `m_0/N_e→1` on the good-calibration events above. Let `v_out` be the terminal normalised weight outside S0. The pre-resampling version of (D5) gives `E_c v_out≤δ+b_c`, hence `v_out→0`. All m_0 copies of S0 receive the same weight, so, when `m_0>0`,

\[
\sum_i w_i^2\le\frac{(1-v_{out})^2}{m_0}+v_{out}^2
\le\frac1{m_0}+v_{out}^2\longrightarrow0.
\]

Conditional Chebyshev and the bound `Σw_i²≤1` eliminate the additional simulation noise. Thus weighted augmentation also works under (P1); it does not follow from an integrated-functional argument alone. On the exact branch use the exact integrated sum, not one continuous draw per enumerated model. ∎

**Scope clarification.** The fixed-N independence of (D4)–(D8) is not a claim that one particle accurately estimates an arbitrary continuous posterior at finite n. Support concentration makes every bounded integrated functional nearly its true-support conditional expectation. Additional conditional simulation noise still needs enough draws.

**Relation to existing results.** T16(i), in `theorems/T16_T9_frozen_limits.md`, already states the evidence/PIP fixed-calibration limits and a CLT, but is marked **CONJECTURE** and is not a locked entry. Theorem A proves the bounded-functional consistency/MSE portion directly; it does **not** prove or upgrade T16's joint CLT. W2-T26 already gives the premise-form actual-budget evidence/PIP conclusions as a **PROVED candidate composition**. Theorem D extends its target to bounded integrated h, supplies the shorter occupancy bound (D5), and separates conditional parameter simulation. Neither T16 nor T26 alone asserts `Π_n h→h(θ*)` for all bounded h.

A sufficient deterministic version of (P1) is `(T_n^max+1)Δ_n→0`. In R1, `T_n^max=O(log²n)`; T03 controls the posterior endpoint and T22(iii) controls the start endpoint under its own EXP′/visibility/leakage assumptions. W2-T26's discharged composition is exactly this route. Later EXP candidates do not remove the other design hypotheses. This is a favourable-start theorem, not a general theorem about correction from a badly distorted product law.

### 2.5 “Ground truth” at a generating parameter

**Corollary D1 (PROVED, conditional statistical implication).** Suppose, in addition to Theorem D, the full posterior concentrates about a generating parameter `θ*_n` in a specified metric after back-transformation, and `h_n` is uniformly locally continuous there: for every ε>0 there is r>0 with

\[
\sup_n\sup_{d(\vartheta,\vartheta_n^*)<r}
|h_n(\vartheta)-h_n(\vartheta_n^*)|\le\epsilon.
\]

Then `Π_n h_n−h_n(θ*_n)→0` in data probability, because its absolute value is at most `ε+2M Π_n{d≥r}`. Add (D1) to obtain generating-value consistency on the output event. Appropriate statistical contraction, e.g. a correctly matched T04 conclusion, is an additional input; T03 supplies support concentration alone. For support indicators and bounded support functions, T03 suffices directly: `|π_n f_n−f_n(S0,n)|≤2Mδ_n`. For inclusion indicators, (D2) is the sharper simultaneous statement.

**COUNTEREXAMPLE to unrestricted bounded h.** Let `h(S,θ,v)=1{θ_j=θ_j^*}` for an active nonzero coefficient in contrast coordinates. Its posterior expectation is zero: the active slab is continuous and the inactive atom is at zero. But its value at the generating parameter is one. This remains true even under posterior concentration and exact computation. Thus “all bounded h converge to the generating value” is false. Also, for fixed n even perfect computation converges to a posterior expectation, not generally to a frequentist truth.

**Suggested replacement for draft §13.1.** “For each fixed data set and successful independently calibrated final schedule, the SMC particle estimates and the recorded Rao–Blackwell inclusion estimates converge to their exact working-posterior expectations as the number of final particles increases. Under the stated favourable-start, posterior-concentration and operational conditions, the actual n-indexed budgets also give posterior-functional consistency and uniform inclusion recovery. Convergence of general parameter functionals to their generating values requires an additional posterior-contraction and continuity argument.”

## 3. Naive union/product merging distorts uncertainty

### 3.1 Proposition M — an identifiable cross-block proxy (COUNTEREXAMPLE; proof complete)

For each n≥4 choose centred deterministic columns with

\[
X_n'X_n=(n-1)\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix},
\qquad 0<|\rho|<1,
\]

and generate `y_raw=b x1+ε`, with fixed `b≠0` and `ε~N(0,σ_*² I_n)`. Standardise the response exactly as v3 does. The true support is `S0={1}`. Set the hypothetical local blocks to `{1}` and `{2}`. They are also v3's prescribed component blocks at p=2, since B=1 (the actual exact branch skips building them).

In each singleton block perform the exact one-variable working Bayesian analysis, with the same slab and variance conventions and any fixed strictly positive prior odds for inclusion (the numerical illustration uses local BB(1,1), odds one). Let `l_{n,j}` be its PIP and let `q_n` be the product of these two local posterior laws. Let `U_n^H` and `U_n^M` be the unions of their local HPMs and MPMs. Let `π_n` be v3's **full** p=2 posterior, with global BB(1,2) prior, cap K=2 and the ridge slab.

Then, in data probability,

\[
l_{n,1}\to1,\quad l_{n,2}\to1,\quad
\pi_n(S_0)\to1,
\]
\[
q_n(2\in S)\to1,\quad q_n(\{1,2\}\subset S)\to1,
\qquad
\pi_n(2\in S)\to0,\quad\pi_n(\{1,2\}\subset S)\to0.
\tag{M1}
\]

Moreover `P(U_n^H=U_n^M={1,2})→1`. If a deterministic union is represented by the degenerate measure `δ_{U_n}`, its proxy PIP and joint-inclusion probability both equal one with probability tending to one. Thus, for any fixed `0<c<1`, each of these naive-versus-full probability errors exceeds c with probability tending to one. In fact `||q_n−π_n||_TV→1`, and likewise for the point-mass union measures. A point decision by itself has no posterior uncertainty: this last formulation explicitly states the degenerate uncertainty interpretation rather than pretending an HPM naturally supplies PIPs.

The actual global-prior composite start

\[
\pi_{0,n}(S)\ \propto\ w(|S|)\,BF_n(S\cap\{1\})BF_n(S\cap\{2\})
\]

is **not** the product q_n, but it too concentrates on `{1,2}`. Thus the example shows why even v3's globally coupled start needs correction; it does not misidentify that start as a product posterior.

**Proof.** Write `t=b²+σ_*²`. In raw centred coordinates the least-squares residual sums divided by n converge respectively to

\[
R_\varnothing/n\to t,\quad
R_{\{1\}}/n\to\sigma_*^2,\quad
R_{\{2\}}/n\to\sigma_*^2+b^2(1-\rho^2),\quad
R_{\{1,2\}}/n\to\sigma_*^2.
\]

These follow directly by projecting the Gaussian noise onto the fixed rank-zero, rank-one and rank-two design spaces. The sample response variance converges to t. After standardisation, divide each displayed limit by t. For every nonempty fixed support the Gram eigenvalues are of order n and bounded away from zero after division by n. Consequently the v3 determinant factor has

\[
\log D_S=|S|\log n+o(1),
\]

and its regularised residual `Q_S` differs from the ordinary standardised residual sum by `O_P(1)`. To see the latter, the shrinkage eigenvalues are `nλ/((n+1)λ+1)`: their difference from one is `O(1/n)` while the squared response projection is `O_P(n)`. There are at most two dimensions. The `2b0` term also changes the log marginal score only by `O_P(1)` since residual sums are of order n.

It follows that the local log Bayes factors satisfy

\[
\frac1n\log BF_n(\{1\})\to
c_1:=\tfrac12\log\frac{b^2+\sigma_*^2}{\sigma_*^2}>0,
\]
\[
\frac1n\log BF_n(\{2\})\to
c_2:=\tfrac12\log\frac{b^2+\sigma_*^2}{\sigma_*^2+b^2(1-\rho^2)}>0.
\tag{M2}
\]

Fixed positive local prior odds cannot change these exponential rates. Both local PIPs tend to one, and eventually exceed 1/2 with probability tending to one, proving the union claim and the product-law statements.

For the full posterior, the empty model loses to `{1}` exponentially. The wrong singleton loses exponentially as well:

\[
\frac1n\log\frac{m(\{2\})}{m(\{1\})}
\to-\tfrac12\log\left(1+\frac{b^2(1-\rho^2)}{\sigma_*^2}\right)<0.
\]

The extra variable in `{1,2}` explains only a fixed-rank Gaussian noise projection, of order `O_P(1)`. The ridge-residual correction is also `O_P(1)`, whereas the determinant penalty supplies

\[
\log\frac{m(\{1,2\})}{m(\{1\})}
=-\tfrac12\log n+O_P(1)\longrightarrow-\infty
\quad\text{in probability}.
\tag{M3}
\]

All four global model-prior masses are fixed and positive, so the three competitor odds tend to zero and `π_n({1})→1`. This also follows from locked T03: p=2, s0=1, fixed signal, bounded energy and minimum correlation eigenvalue `1−|ρ|>0` satisfy its eventual regime/eigenvalue/beta-min conditions. The finite-support proof above avoids depending on T03's conservative numerical constants.

Under π0 the odds of `{1,2}` versus `{1}` equal `[w(2)/w(1)] BF_n({2})`, which diverge exponentially by (M2); likewise versus `{2}` and the empty support. This proves π0 concentrates on the wrong union. The event `{2∈S}` gives the TV lower bound approaching one. All assertions follow. ∎

### 3.2 What v3 correction is and is not proved to do here

**PROVED — actual small-p v3.** For p=2 and n≥4, v3 takes its exact branch: all four models fit far below the enumeration threshold. Its reported PIPs, joint-inclusion probability if accumulated, evidence and HPM are the full-posterior quantities. By Proposition M/T03, its proxy PIP and joint inclusion tend to zero and its HPM/MPM tend to `{1}` with probability tending to one, subject to output availability and exact arithmetic. This establishes the requested existence contrast for the **actual method**, not a pretend SMC run at p=2.

**PROVED — SMC component, different limit.** If one deliberately runs the specified SMC component on these same data instead of its exact branch, Theorem A gives convergence of its self-normalised/RB estimates to the full posterior for each n as `N→∞`. Hence the iterated limit, first N then n, is also correct. An arbitrarily large enough diagonal N_n can be selected from these pointwise limits; they do not identify the prescribed production N_n.

**T26 boundary.** On this family, `π0,n(S0)→0`, so `Δ_n→1`; T26's favourable-start SMC premise fails. T26 **cannot** be cited to claim production-budget SMC PIP/evidence consistency for this example. The actual method's exact branch is covered by T26's separate exact-branch clause together with T03. In growing-p settings where (P1) does hold, Theorem D/T26 gives the corresponding actual-budget estimator conclusion. This distinction is necessary: the supplied theorem set does not prove general masked-regime PIP/evidence consistency, and an HPM discovery theorem cannot supply it.

The example uses distinct predictors and a fixed eigenvalue lower bound; it therefore avoids the identifiability problem of exact duplicates. The draft's alternative picture of two persistent competing singletons is a useful finite-data intuition, but if both singleton masses remain substantial asymptotically, T03's unique-support concentration cannot simultaneously hold. No such incompatible assumptions are used here.

### 3.3 Exact small-p numerical illustration

Script: [scripts/naive_merge.py](scripts/naive_merge.py). Outputs: [CSV](results/naive_merge.csv), [run log](results/run.txt), [metadata](results/metadata.json), [PNG](results/naive_merge.png), [SVG](results/naive_merge.svg).

Run, **one small job at a time**, through the mandatory wrapper:

```bash
/home/fb31/.config/bvs-hq/owls/owls_run -j 2 -- \
  uv run --no-project --cache-dir theory_campaign/A-DRAFT/reading/uv-cache \
  --with numpy --with matplotlib \
  python theory_campaign/A-DRAFT/scripts/naive_merge.py \
  > theory_campaign/A-DRAFT/results/run.txt
```

Parameters: p=2, `ρ=0.8`, `b=σ*=1`, base seed `20261102`; an independent deterministic seed keyed by n is used in each row. This is **exact summation over four models using floating-point v3 scores**, not an SMC approximation, not symbolic/rational arithmetic, and not a Monte Carlo estimate of an across-data error rate. Randomness generates one data set per n. Gaussian sufficient statistics are sampled exactly: `X'ε~N(0,σ²G)` and the independent centred residual noise norm is `σ² χ²_{n−3}`. No large design matrix or enumeration campaign is needed.

| n | Full proxy PIP | Product proxy PIP | Full joint inclusion | Product joint inclusion | Full truth mass |
|---:|---:|---:|---:|---:|---:|
| 40 | 0.169997 | 0.998530 | 0.169972 | 0.998530 | 0.830003 |
| 100 | 0.254240 | 0.999995 | 0.254240 | 0.999995 | 0.745760 |
| 400 | 0.067198 | 1.000000 | 0.067198 | 1.000000 | 0.932802 |
| 1,600 | 0.045383 | 1.000000 | 0.045383 | 1.000000 | 0.954617 |
| 6,400 | 0.016079 | 1.000000 | 0.016079 | 1.000000 | 0.983921 |
| 25,600 | 0.006214 | 1.000000 | 0.006214 | 1.000000 | 0.993786 |

Both local HPM and MPM unions are `{1,2}` in every row; the full HPM is `{1}` in every row. The composite start also assigns proxy PIP essentially one; it is computed separately using the global prior. Values displayed as one are rounded, not exact certainty; very small start truth masses can underflow, so `log_start_truth` is preserved in the CSV. The n=100 increase in full proxy probability reflects fresh Gaussian noise; a convergence-in-probability theorem does not assert sample-path monotonicity across these independent data sets.

![Exact four-model comparison](results/naive_merge.png)

Verification: all four probabilities normalise; the ridge residual lower bound is checked; each score is checked against an independently written covariance/determinant-lemma expression for the Gaussian marginal likelihood. The largest log-BF discrepancy in these six cases is below `10^{-11}`. These checks validate this illustration, not the complete production engine or floating-point identities of T12. The first attempted system-Python launch lacked NumPy; the successful run used the isolated uv dependency cache under this task folder.

### 3.4 Confidence card and remaining obligations

| Claim | Status in this report | Confidence and exact boundary | Method/implementation change? |
|---|---|---|---|
| Fixed-data posterior-functional LLN and MSE, Theorem A | **PROVED**, candidate | High. Finite-state positivity, exact start, independent final streams and conditional resampling variance are sufficient. No joint CLT claimed. | None for existing PIPs; general h requires recording/evaluating the stated functional. |
| Islandwise bounded-h unnormalised identity | **PROVED** from locked T12 | High. Applies at admissible boundaries/marks; not at state-dependent stops or after completion selection. | Optional exact conditional integration/draws for continuous h. |
| Actual-budget bounded integrated-h consistency under (P1), Theorem D | **PROVED**, candidate | High conditional confidence; full proof uses locked T14/T12 and a bounded-occupancy inequality. No general proof of (P1) on masked designs. | None for PIPs. Conditional parameter draws are an optional extension; their required weight dispersion is proved under (P1). |
| Uniform PIPs without `(L+4)ρ*→0` | **PROVED**, candidate | High. Re-control each measured-round start via T12, pay only one-round departure. Independently supports W2-T26's premise reduction. | No. |
| All bounded h converge to a generating value | **COUNTEREXAMPLE** | Certain: singleton equality events under continuous slabs. Continuity/contraction repairs the statement. | A statement correction. |
| Naive union/product failure, Proposition M | **COUNTEREXAMPLE**, complete proof | High. Identifiable fixed-p design; no near-singularity or growing-p loophole. | No. |
| Actual v3 consistent on the counterexample | **PROVED** | High under exact scores and output availability, because actual v3 enumerates. The forced-SMC production-budget claim is **OPEN here**, not attributed to T26. | No; forced SMC would bypass the actual branch. |
| Generic local-to-global/SMC novelty | **OPEN** as a priority claim; adverse evidence strong | Lindsten and binary-space SMC are direct precedents. This six-paper audit cannot certify global priority. | Reframe contribution. |
| Stronger uncertainty performance than complete Song–Liang | **OPEN** | The naive union example does not analyse their second selection stage. Requires a faithful comparator. | Benchmark/theorem work beyond this report. |
| Masked-regime PIP/evidence guarantees for unmodified v3 | **OPEN** | T38 scores the truth; it does not establish these estimator guarantees. O-WSTAB is separate ongoing work. | No method change asserted. |

The proofs here have been self-checked but have not received independent review. Suggested review targets are Theorem A's marked-prefix argument, Theorem D's pre-resampling weight-dispersion argument, and the raw-to-standardised residual comparison in Proposition M. The results do not edit the locked register or any other agent's files.

### Source locations for the internal mathematical dependencies

- `Docs/Theory/proofs/T09_T7_kernel_validity/STATEMENT.md`: exact start and invariant elementary/round kernels.
- `Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md`: §3(i.a–c), (ii), (iii), (iv.b–f).
- `Docs/Theory/proofs/T14_LFM_first_moment_evidence/STATEMENT.md`: (i-b), the first-moment evidence bound.
- `Docs/Theory/proofs/T22_T16_start_aggregation/STATEMENT.md`: singleton bridge-mass lower bound (iv-b).
- `Docs/Theory/proofs/T23_T18_basin_prefix/STATEMENT.md`: recorded-PIP pathwise bounds; §2.4 gives their direct argument.
- `Docs/Theory/proofs/T03_A2_selection_consistency/STATEMENT.md`: statistical support concentration.
- `Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md`, `Docs/Theory/proofs/T31_T22_certificates/STATEMENT.md`, and `Docs/Theory/proofs/LOCKED_PROOFS.md`.
- `Docs/Theory/theorems/T16_T9_frozen_limits.md`: still **CONJECTURE**, not silently used as a locked theorem.
- `origin/theory/W2-T26:theory_campaign/W2-T26/REPORT.md`: premise-form Theorem A and discharged Theorem B (different from the repair Theorem B).
- `origin/theory/W2-BOOK:theory_campaign/W2-BOOK/REPORT.md`: potential-run/output split and pooled-product correction.
- The other W snapshots and their precise heads are recorded in [campaign_refs.txt](results/campaign_refs.txt); §1.3 states which updates affect this audit.
