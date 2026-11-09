# SMC-BVS: proposed consistency package

OpenAI / gpt-6-astra, 9 November 2026. Research proposal; candidate results below are not represented as established theorems.

**Blindness disclosure.** I made a source-scope error: the initial read printed the whole permitted notation file `A_notation.tex`, rather than only its method symbols. Its output exposed descriptions of previous theory and assumptions. I opened no other theory files beyond the brief, the permitted method section, and that appendix, and did not follow their references. Nevertheless this submission must be labelled **scope-contaminated, not a valid fully blind proposal**. The recommendations below are offered for substantive review, not as an independent blind vote. No subagents or git commands were used.

## 1. Recommendation and the actual object of inference

I would fund a statistical backbone plus a separate discovery theorem, with a conditional SMC accuracy extension. The statistical backbone should establish posterior concentration on the true support for the **actual capped ridge score**, and derive sure screening and population HPM consistency. The discovery theorem should exploit the fact that the reported HPM is the best model ever scored, including rejected proposals and local-search scans. LS0 is the most promising carrier of a seed-independent reported-model guarantee. A complete SMC approximation theorem is valuable for PIPs and evidence, but should not be a prerequisite for proving the reported HPM correct.

The distinction matters: posterior concentration alone cannot force a sampler to discover the concentrated mass; discovery of one optimal model cannot make a particle population representative. Neither implication can be supplied by an empirical ESS diagnostic.

### Code facts that determine the theorem statements

I inspected `v3_fit.R`, `v3_run.R`, `v3_calib.R`, `cpp/v3_start.h`, and relevant portions of `cpp/v3_engine.h`, `cpp/v3_core.cpp`, and `cpp/v3_score.h` in the allowed production directory. Source comments referencing other theory were not followed.

* On standardized data, (K=\min(p,\lfloor n/2\rfloor)), (g=n), ridge (=1), and (a_0=b_0=.01). For (G_S=X_S^TX_S), (z_S=X_S^Ty),
  \[
  H_S=(n+1)G_S+I,\quad Q_S=y^Ty-nz_S^TH_S^{-1}z_S,
  \]
  \[
  m(S)=C_n\{\det H_S/\det(G_S+I)\}^{-1/2}(.02+Q_S)^{-(n/2+.01)}.
  \]
  The individual-model prior is proportional to (w(k)=1/[2\binom{2p-1}{k}]), not to the prior probability of the entire size class. Write (F(S)=\log\varpi(S)+\log m(S)).
* The block start is (\gamma_0(S)=\varpi(S)\prod_b m(S\cap C_b)/m(\varnothing)). The prior couples block sizes; this is not an independent product law on blocks. The convolution sampler and normalizer account for that coupling.
* `v3_core.cpp:460–480` executes LS0 **after** the final particle run and final local search, when the run has not stopped. It emits the start-mode centre and scores every feasible add, delete, and swap neighbour. The shipped default move cap is (\ell_n+|\widetilde S_0|), with (\ell_n=\lceil\log_2(n+p+1)\rceil), not merely (\ell_n). An additional neighbourhood scan occurs after the move cap.
* `v3_run.R` assembles **equal-weight** island PIPs, `rowMeans(P)`, from within-island Gibbs conditional probabilities recorded during four measured rounds. The permitted method text describes evidence-weighted primary PIPs; the inspected code does not implement that description. This proposal targets the inspected code. Evidence is the arithmetic average of island evidence estimates, assembled on the log scale.
* The default has four islands, (N_e=4^e\max(2500,n,p)), two possible tiers, logarithmically growing terminal burn-in, and a stage ceiling eventually of order (\log^2(n+p)). Calibration freezes the final grid. The production code includes a grid fallback; failure of a restricted-grid construction does not always imply failure to deliver.
* The all-scored ledger, rather than empirical particle frequency, determines the reported HPM. `local_certified` is a neighbourhood statement. The score-error quantity used by `global_certified` is explicitly heuristic.

The code/text differences should be settled in the paper's method description before claiming that a theorem covers a different output formula. No code modification is proposed here.

## 2. Assumptions: what is statistical and what is computational

Use a triangular array of fixed designs after deterministic column centering and scaling, with (\|x_j\|^2=n-1). Generate the raw response by
\[
y^r=\alpha\mathbf1+X\theta^*+\epsilon,\qquad
\epsilon\sim N(0,\sigma_*^2 I_n),
\]
then apply the actual response preprocessing. All probabilities in the statistical results are over the raw response. Conditional random-design extensions follow when the stated design events hold with probability tending to one.

**S1 — polynomial dimension and fixed sparse truth.** (p\le n^A), for an arbitrary fixed (A<\infty); (s=|S_*|) is fixed, (s\le K) eventually. Fixed sparsity is a defensible first theorem, also used in Song–Liang's strict-sparsity setting. Constants may depend on (A,s). The same production prior is used for every (A). Growing sparsity is an extension, not silently covered.

**S2 — nondegenerate scale.** (0<c\le\sigma_*^2\le C) and (\|X\theta^*\|^2/n\le C). Consequently the response sample variance lies in a fixed positive compact interval with probability tending to one. This permits a rigorous treatment of the response-dependent rescaling and prevents nearly noiseless interpolation from dominating the asymptotics. It is a standard bounded signal-to-noise regime, not a design-family restriction.

**S3 — sparse conditioning on a logarithmic sieve.** Choose (m_n=\lceil C_0\log n\rceil). Require
\[
 c\le\lambda_{\min}(X_U^TX_U/n)
 \le\lambda_{\max}(X_U^TX_U/n)\le C
 \quad (|U|\le m_n+s).
\]
This is a conventional sparse eigenvalue assumption. It allows (p\gg n), since (m_n+s=o(n)), and imposes no invertibility on the full Gram matrix or all size-(K) models. It excludes exact duplicate columns in the relevant sieve; exact support identification cannot generally survive interchangeable copies of a true column. It is stronger than necessary and stronger than a truth-specific projection-separation condition. Do not describe it as universally mild. Its benefit is that the first proof has a clear matrix domain; later work can replace it by eigenvalue conditions anchored at the truth and determinant bounds for competing models.

**S4 — separation from underfitting.** With (P_S) the orthogonal projector onto the centered columns in (S), set
\[
 \Delta_n=\min_{|S|\le m_n,\ S\not\supseteq S_*}
 \|(I-P_S)X\theta^*\|^2/\sigma_*^2.
\]
Require (\Delta_n/[m_n\log(p\vee n)]\to\infty). Under S3 a sufficient condition is (n\min_{j\in S_*}|\theta_j^*|^2/\log^2 n\to\infty). This deliberately conservative beta-min target gives room for a uniform sieve argument. It includes fixed nonzero signals and allows shrinking signals. Sharpening to a constant or diverging multiple of (\log p+\log n) should be a second-stage improvement, not a prerequisite for the first valid theorem.

There is no statistical assumption here that the block start is close to the posterior. That belongs in a separate computational theorem. Likewise, no irreducibility statement should masquerade as a bound on the shipped number of moves.

### Comparison with Song–Liang Conditions 1–5

The supplied PDF, pp. 953–958, makes the distinctions unusually clear. Conditions 1 and 2 concern predictor tails/moments for random-design density consistency; Condition 3 concerns identifiability; Condition 4 gives a second-moment assumption for a fixed misspecified subset; Condition 5 asks that each true predictor have nonzero marginal covariance with the response. S2–S4 are fixed-design, quantitative counterparts of scale control and identifiability, not literal restatements of those conditions. A population Hellinger theorem would additionally need a design distribution and appropriate moments. The main fixed-design result should not claim it.

Condition 5 does not imply that this block start, with blocks of at most 16 variables, has the right mode or that its greedy search reaches the truth. Conversely, the full posterior theorem does not need marginal signal: jointly identifiable variables with cancelling marginal effects should remain in scope. A computational theorem may require stronger visibility or a search-basin assumption and must say so. Song–Liang's marginal-inclusion screening theorem is not itself strong posterior model-selection consistency; their main text points to supplementary Theorem S for MAP consistency. Their prior and size restriction also differ from ours, so the paper is a narrative and proof template, not a theorem to invoke verbatim.

## 3. Proposed numbered theorem package

### Theorem 1 — posterior concentration for the full production cap

**Candidate statement.** Under S1–S4, for sufficiently large fixed (C_0=C_0(A,s,c,C)), the exact posterior induced by the production score satisfies
\[
 \Pi_n(S_*\mid X,y)\longrightarrow1
 \quad\text{in }P_*\text{-probability},
\]
while retaining the actual support restriction (K=\min(p,\lfloor n/2\rfloor)). In particular the logarithmic sieve is an analytical device, not a smaller computational cap. Include (S_*=\varnothing) separately, with the underfitting requirement omitted.

**What it buys.** This is the central statistical result. It includes polynomial dimensions with any fixed exponent and avoids assuming all production-size Gram matrices are well conditioned. It is stronger than a prediction-only consistency theorem and supports the complete variable-selection story.

**Proof strategy.** Split posterior odds into (i) sizes above (m_n), (ii) underfitted models within the sieve, and (iii) proper supermodels within it.

1. Prove an exact preprocessing reduction on the (n-1) centered contrast coordinates. Do not apply an iid Gaussian likelihood directly to the standardized response. Re-express the model odds on the raw response scale; the induced inverse-gamma shape is shifted by (1/2), and its scale depends on the response variance. On the S2 event, dominate this family of proper prior densities by a constant multiple of a single fixed proper prior. This creates a legitimate integrated-likelihood envelope for the tail argument.
2. Exploit the **size-class** prior. If (a_k=\binom pk w(k)), then
   \[
   a_{k+1}/a_k=(p-k)/(2p-1-k).
   \]
   For growing (p\ge2), this is uniformly bounded above by a constant below one. Thus the prior tail beyond (m_n) is exponentially small in (m_n). Combine an integrated-likelihood expectation bound with a polynomial lower bound on the truth's posterior denominator. The lower bound must include the individual truth prior mass, of order (p^{-s}), and parameter integration losses. Taking (C_0) large enough should suppress the tail. Fixed (p) is easier and eventually has no tail.
3. On the sieve, derive determinant and ridge-residual expansions uniformly in (S). The (g=n) determinant penalty supplies approximately (\frac12|S|\log n). The per-model prior increment supplies approximately \(\log p-\log(|S|+1)+\log2\). Retain factorial terms for growing sieve sizes; do not replace the BB prior by independent Bernoulli inclusion without an error bound.
4. Control underfitting by noncentral Gaussian projection inequalities and S4. Control overfitting by fractional moments of Bayes factors, summing by the number of extra variables. For intuition, a fractional exponent (a\in(0,1)) yields a multiplicity-versus-penalty factor resembling (p^{(1-a)r}n^{-ar/2}); for every fixed (A), an (a>2A/(2A+1)) is available. This is a proof guide, not a proved uniform bound for the unknown-variance ridge score. The exact likelihood-ratio moment calculation is required.

**Hardest step and risk: medium–high.** The large-model tail must be proved for the response-rescaled score, not an imaginary fixed-scale marginal likelihood. The overfit summation must remain uniform up to (C_0\log n). A failure of the proper-prior envelope or a loss exponential in (\log^2 n) could defeat the proposed sieve. Resolve these two issues before investing in delicate sampler geometry. The spectral assumption is intentionally localized so that a failure here is not hidden behind impossible global invertibility when (p>n).

### Theorem 2 — screening, ideal HPM, and estimation consequences

**Statement conditional on Theorem 1.** Let (q_{nj}=\Pi_n(j\in S\mid y)), and let (S_n^{\rm MAP}) maximize the exact posterior. Then
\[
 P_*(S_n^{\rm MAP}=S_*)\to1,\qquad
 \max_{j\le p}|q_{nj}-1\{j\in S_*\}|\to0
 \quad\text{in probability}.
\]
For every fixed (t\in(0,1)), (\{j:q_{nj}>t\}=S_*) with probability tending to one, hence sure screening follows. More weakly, posterior mass on supersets tending to one already gives simultaneous sure screening of the fixed true support, without a false-positive conclusion.

If the coefficient posterior is included in the paper, a further candidate consequence under S2–S3 is
\[
 \Pi_n\{\|X(\theta-\theta^*)\|^2/n>M_n/n\mid y\}\to0
\]
for every (M_n\to\infty), with coefficients mapped back to raw response scale. This is in-sample prediction contraction for fixed (s), not a population-density assertion.

**Proof and assumptions.** Each PIP error is bounded by (1-\Pi_n(S_*)), so no union bound over (p) is needed. Posterior mass above (1/2) makes the truth the unique MAP. On the true model, conjugate Gaussian/inverse-gamma calculations give fixed-dimensional contraction; the remaining posterior mass vanishes. These arguments use no further design restriction or sampler premise.

**Risk: low after Theorem 1.** The only substantive extra work is the raw-scale coefficient conversion. These conclusions concern exact posterior quantities, and must not be labelled guarantees for the computed PIPs before Theorem 5 applies.

### Theorem 3 — discovery transfers to the actual reported HPM

**Statement.** Let \(\mathcal V_n\) be all models scored in the potential completed production computation, including setup tables, inherited calibration models, held/proposed Gibbs states, independence proposals, final-search scans, and LS0 scans. Let \(\mathcal O_n\) mean complete output is delivered. If the ledger and score comparisons are faithful, then
\[
 P\{\mathcal O_n,\widehat S_n\ne S_*\}
 \le P\{S_*\text{ is not the unique maximizer of }F\}
      +P\{S_*\notin\mathcal V_n\}.
\]
Thus Theorem 1 plus a vanishing discovery failure implies a vanishing probability of a wrong delivered HPM. To conclude \(P(\mathcal O_n,\widehat S_n=S_*)\to1\), additionally prove \(P(\mathcal O_n)\to1\).

Two sufficient discovery mechanisms should be stated separately.

**(a) Exact start-draw mechanism.** In the ideal-uniform interpretation of the existing sampler, its first (N_e) final start draws are conditionally iid from (\pi_0\). Consequently (N_0\pi_0(S_*)\to\infty) in data probability suffices for discovery with probability tending to one, regardless of resampling or later mixing. Every draw is evaluated. This is a weak sufficient condition on mass compared with start concentration, but it is still a computational overlap assumption. A sharp mode need not carry enough mass. A model proposed and rejected later also counts, although that can only improve this bound.

**(b) LS0 mechanism.** Define (A_n=\ell_n+|\widetilde S_0|). If the deterministic LS0 routine, using its actual comparisons and tie rule, scores (S_*) within its (A_n) moves plus terminal scan with probability tending to one over data, the reported HPM is consistent on delivery. No distributional approximation of the particle population or randomness assumption is then needed for the discovery part. The truth need not be the search's final returned centre: being scored suffices.

**Proof.** A unique global maximizer, once entered into a correctly implemented best-score ledger, cannot be displaced by another model. For (a), condition on data and frozen calibration and use \((1-\pi_0(S_*))^{N_e}\le\exp[-N_0\pi_0(S_*)]\). For (b), verify centre emission, complete scans, the last scan, and ledger retention directly against `v3_engine.h` and `v3_core.cpp`. This is an implementation lemma, not a new statistical argument.

**Risk: low for transfer; high for deriving discovery from mild design assumptions.** Fixed resource limits can prevent LS0 from being reached even when its hypothetical trajectory is perfect. Delivery is a separate claim. Intersecting a bad event with delivery is safe; conditioning on delivery without controlling its probability is not a substitute for unconditional consistency.

### Theorem 4 — a quantitative, design-agnostic LS0 basin theorem

**Candidate statement with explicit additional assumptions.** Let (\mathcal R_n\subseteq\Omega_n) be a deterministic set of models containing (S_*). Let (V_n:\mathcal R_n\to\mathbb N_0) vanish only at (S_*). Suppose, on an event of probability tending to one:

1. The computed start mode belongs to \(\mathcal R_n\), and (V_n(\widetilde S_0)\le A_n).
2. At every (S\in\mathcal R_n\setminus\{S_*\}), the **actual highest-scoring feasible neighbour**, with the production tie rule, improves (F(S)), stays in \(\mathcal R_n\), and decreases (V_n) by at least one.
3. Scores and comparisons obey the stated numerical margin requirement below, and the search completes its scans.

Then LS0 scores the truth by at most (A_n) moves; combined with Theorems 1 and 3 this yields consistent reported HPMs on delivery. No assumption about behaviour outside the basin is required.

**Why retain a theorem this conditional?** It exposes the exact missing computational ingredient instead of pretending sparse eigenvalues imply greedy convergence. These are not mild statistical assumptions. A proof that simply renames success as a basin condition would add little. The research contribution must be a verifiable sufficient condition in terms of (X,\theta^*,\sigma_*\) and the actual block partition.

**Proposed route to primitive conditions.** Use the deterministic comparison scores (\bar F(S)=E_*F(S)) and \(\bar G_0(S)=E_*\log\gamma_0(S)\), including preprocessing in these expectations. Establish uniform, edge-specific stochastic deviations
\[
 |[F(T)-F(S)]-[\bar F(T)-\bar F(S)]|\le h_n(S,T)
\]
on the basin and its feasible neighbours. Require a population margin large enough that at least one decreasing neighbour improves the centre and every maximizing neighbour is decreasing, after allowing all relevant error radii. Require also that the population start-mode margin between the basin and its complement dominates the uniform start-score error. These are deterministic, quantitative signal-geometry requirements, although still stronger than S3–S4.

Crucially, use different deviation scales for signal moves and removal of irrelevant variables. A uniform (O_P(\sqrt n)) score-error bound would swamp the (\log n+\log p) penalty that makes deletion of an irrelevant variable attractive. For nested supermodels the signal cancels, allowing chi-square-scale noise control. For underfitted comparisons the noncentral term remains. Schur complements provide the exact ridge increments; compare them with residualized-signal contrasts before making an asymptotic expansion.

For fixed (s), the natural rank is a weighted count of missing and surplus variables. If it decreases by one at every step and the start has (O(\log n)) mistakes, the shipped cap may suffice. The default extra \(|\widetilde S_0|\) term makes deletion-heavy starts less problematic than a pure logarithmic cap. Prove the actual inequality (V_n(\widetilde S_0)\le A_n); do not infer it merely from an (O(\log n)) bound with unspecified constants.

**Risk: high for primitive conditions, low for the descent lemma.** Correlated surrogate variables, marginal cancellation, and cross-block omitted signals can make the best move go away from the truth even when some improving path exists. Existence of a good neighbour is insufficient for best-improvement search. I would allow one week to derive a useful sufficient condition, then retain the transparent conditional theorem if it requires near-orthogonality or a special design family. Do not reorganize the paper around such families.

### Theorem 5 — computed PIPs and evidence under a genuine bridge-accuracy condition

**Candidate sufficient condition.** Condition on data and successful frozen calibration. Let
\[
 D_n=\sup_{S\in\Omega_n}d(S)-\inf_{S\in\Omega_n}d(S),
 \qquad d(S)=\log[m(S)/m(\varnothing)]-\sum_b\log r_b(S\cap C_b).
\]
In the exact-arithmetic, independent-uniform realization of the coded transitions, suppose (D_n=o_P(\log n)) and the frozen grid has (T_n=O(\log^2(n+p))) stages. Then the target extension to prove is
\[
 \widehat Z/Z\to1,\qquad
 \max_{j\le p}|\widehat q_j-q_{nj}|\to0
 \quad\text{in probability}.
\]
Here \(\widehat q_j\) is the **equal-island average of the recorded Gibbs conditional probabilities**, not an empirical inclusion frequency and not an evidence-weighted estimator. Theorem 2 then transfers to the computed MPM. Relative evidence consistency implies \(\log\widehat Z-\log Z\to0\). The target (Z) is the working standardized-data evidence.

**Assumptions and scope.** The global oscillation condition is a deliberately strong bridge-stability condition, not a consequence of S1–S4 and not advertised as mild. It is a clean initial sufficient condition that permits an arbitrary data-dependent grid frozen before final randomness. It is probably too restrictive for the main statistical theorem. A later replacement should bound normalized Feynman–Kac continuation operators on high-probability regions, together with a genuine escape/tail bound; checking a restricted calibration store is not enough.

**Proof plan.** First verify each actual kernel preserves \(\pi_\varphi\), including the neighbour-swap proposal ratio and random permutation of elementary moves. Conditional on frozen calibration, identify the exact initial law, multinomial resampling, incremental weights, and normalizing-constant estimator. Del Moral–Doucet–Jasra supplies the framework, not an automatic growing-dimension theorem. For a positive incremental potential, its max/min ratio is bounded by \(\exp(\Delta\varphi D_n)\); products of these bounds over the bridge are at most \(e^{D_n}\). Develop a martingale bound with polynomial dependence on (T_n) and (e^{D_n}). Even a conservative error scale of order
\[
 T_n e^{2D_n}\sqrt{\log(p+1)/N_0}
\]
vanishes under the proposed condition. **This displayed scale is a proof target, not an established inequality.** The operator calculation must verify it before the theorem is accepted.

Treat each recorded conditional probability as a bounded functional at the precise within-round recording time. Under a stationary input its expectation is the target PIP; a random-order sweep still requires accounting for all intervening kernels. Then prove simultaneous concentration using a tail inequality and a \(\log p\) factor. Coordinatewise (L^2) convergence followed by an uncontrolled (p\)-fold union bound is inadequate for arbitrary polynomial dimension. Four islands and four measured rounds only change constants. Terminal invariant kernels preserve approximation but should not be credited with an unproved mixing acceleration.

**Risk: medium for a strong-condition theorem; high for useful weaker assumptions.** The chief obstacle is controlling bridge accuracy in a growing state space, not proving fixed-(n) convergence as (N\to\infty). Separate theoretical unbiasedness of an individual evidence estimate under ideal resampling from relative consistency: the former permits huge variance. Restricted ESS and agreement of four islands do not establish either uniform overlap or a relative variance bound.

### Theorem 6 — misspecification: projection targets and honest screening

**Candidate first statement.** Consider a fixed candidate subset (J) of bounded size, possibly omitting true variables, with (X_J^TX_J/n\to\Sigma_J\succ0), (X_J^TX\theta^*/n\to c_J), and omitted mean energy per observation converging. Define \(b_J^\dagger=\Sigma_J^{-1}c_J\) and \(S_J^\dagger=\operatorname{supp}(b_J^\dagger)\). Assume its nonzero coordinates are bounded away from zero and the limiting residual variance is positive. For the production score restricted to models (S\subseteq J), using either the original (p\le n^A) prior indexing or a declared refit with (p=|J|), posterior mass on (S_J^\dagger\) tends to one. State which prior is used; neither conditional analysis changes the implemented algorithm.

**What it buys.** This gives the correct explanation of what a small block fitted against the full response learns. It learns projection coefficients, which can include surrogates and can omit genuine variables whose projected coefficients cancel. A variable (j\in S_*\cap J) is screened in by this argument only if (b_{J,j}^\dagger\ne0). This is the relevant Song–Liang misspecification story, without asserting that the block table itself is a reported posterior or that a blockwise result automatically controls the globally size-coupled start law.

**Proof and risk: medium.** For finitely many submodels, Gaussian quadratic-form concentration gives limiting residual contrasts. Models missing a nonzero projection coefficient lose order (n) in log fit. Supermodels of the projection support only fit noise, and lose to the determinant/prior penalty. Account for finite-(n) projection coefficients: convergence to zero alone is insufficient to discard a coordinate. Require coordinates outside (S_J^\dagger\) to be exactly zero in the finite-(n) projection, or their squared coefficients times (n\) to be (o(\log n+\log p)\), with a sharper threshold analysis if needed. This extra assumption prevents an incorrect selection claim based only on a limiting zero coefficient.

Uniformity over all growing numbers of blocks requires rates and uniform projection gaps, beyond the fixed-subset assertion. General nonlinear misspecification should initially receive a set-valued approximation statement: mass outside a suitably separated set of best approximations vanishes. A unique pseudo-true support and exact selection require extra identifiability and complexity separation. Do not promise original-support recovery under arbitrary misspecification.

## 4. Which mechanism should carry the paper?

The central diagram is logical, not architectural:

1. **Statistical concentration + all-scored discovery → reported HPM.** Prove the score ranks the truth first, then prove the routine evaluates it. LS0 is the preferred discovery mechanism because it is deterministic once data and settings are fixed; accepted particle trajectories need not be representative. The obstacle is quantitative basin entry and best-neighbour geometry, not posterior odds.
2. **Statistical concentration + SMC approximation → computed PIPs/MPM.** This needs the actual recorded Rao–Blackwell quantities and equal-weight island aggregation. Its obstacle is dimension-uniform particle accuracy under the shipped budgets.
3. **SMC normalizer approximation → evidence.** This is a separate claim about a scalar normalizer, not an automatic consequence of recovering the truth. A sampler can discover the HPM and still miss important normalization mass or carry unstable weights.

A hybrid can use LS0 for the main reported-model theorem while retaining Theorem 5 as an explicitly conditional guarantee for all numerical summaries. If initial start mass can be bounded directly, Theorem 3(a) provides a second HPM route with less geometry. The main risk is overinvesting in proving global resemblance between \(\pi_0\) and \(\pi_1\) when HPM discovery only needs one well-placed score event.

## 5. Numerical and operational scope; what not to claim

The code uses double arithmetic and a finite-state pseudorandom generator initialized from an integer seed. Fresh named streams are not literally independent continuous uniforms. A theorem should identify its probability space instead of quietly changing the executable.

For LS0, require that numerical score errors on compared models are smaller than half the relevant strict comparison margins, including the global truth-versus-competitor margin for the ledger. If score error is bounded by (e_n\), the corresponding pairwise margin must exceed (2e_n\). The start-mode DP likewise needs an argmax-stability bound or direct validation of the computed mode's basin membership. This produces a guarantee for the actual executed comparisons when the numerical event holds, uniformly over seeds for the search component. The production heuristic error flag does not prove that event.

For stochastic theorems, first prove the coded mathematical algorithm under ideal uniforms, then state a separate coupling requirement: discrepancy in the relevant output law between the implemented generator/arithmetic and that mathematical algorithm tends to zero. This is an additional unproved implementation premise, not something supplied by SMC theory. Deterministic LS0 is attractive precisely because its statistical correctness can avoid that premise, provided score comparisons and delivery are justified. Fixed hardware with fixed memory cannot deliver (p\to\infty\); asymptotic delivery requires a declared allocation sequence sufficient for the existing computation. This changes delivery capacity, not the estimator's statistical tuning.

Do not claim:

* the exact global HPM was found merely because the code names its best scored model `hpm`;
* posterior concentration implies polynomial-time discovery under arbitrary identifiable designs;
* strong exact-support identification with exchangeable duplicate true columns;
* that conditioning on successful delivery removes algorithmic failure;
* that a local optimum certificate is a global one;
* that finite-block projection consistency proves consistency of the full block start;
* that LS0 repairs PIPs or evidence—it does not change the particles;
* that a fixed-dimensional SMC CLT establishes the joint (n,p,N,T\) limit here;
* that standardized working evidence equals an ordinary raw-data marginal likelihood;
* super-polynomial dimension, growing support size, or unrestricted misspecification under the first package.

## 6. Proving budget and final recommendation

First prove the preprocessing/envelope lemma and the logarithmic posterior sieve, then the overfit and underfit odds sums. These are the go/no-go gates for the central claim. In parallel only in the intellectual sense—not as a request for additional agents—write the short ledger/discovery transfer proof and audit the exact source contracts. Next spend a bounded effort on primitive LS0 basin margins. If those force a special design family, keep a conditional basin theorem rather than weakening the design-agnostic statistical result. Finally establish the strong bridge-stability theorem and the fixed-subset misspecification theorem. Every proposed rate above needs its own derivation; none is borrowed wholesale from Song–Liang.

**Recommendation.** I would bet the multi-week budget on Theorems 1–3 and 6, plus a carefully delimited Theorem 4 as the route to reported-model consistency. Theorem 1 should retain the production cap and prove its own logarithmic sieve under fixed sparsity, sparse eigenvalues, bounded scale, and explicit beta-min separation. State the screening and ideal-HPM consequences immediately, then make discovery and delivery visible in the reported-HPM theorem. Treat a useful primitive LS0 basin condition as the main computational research question. Include Theorem 5 only with an honestly stated bridge-stability premise until its growing-dimension error bound has been proved. This gives a coherent Song–Liang-shaped paper about the actual score and actual reported model without making accurate SMC integration the price of every selection result.

## References actually used

* Song, Q. and Liang, F. (2015). *A split-and-merge Bayesian variable selection approach for ultrahigh dimensional regression*. JRSS B **77**(5), 947–972. [DOI](https://doi.org/10.1111/rssb.12095). Conditions 1–5 and main-text Theorems 1–4 were checked against the supplied local PDF, especially pp. 952–958. Its supplementary Theorem S was not read; only the main text's description is used.
* Del Moral, P., Doucet, A. and Jasra, A. (2006). *Sequential Monte Carlo samplers*. JRSS B **68**(3), 411–436. [Author-hosted paper](https://www.stats.ox.ac.uk/~doucet/delmoral_doucet_jasra_sequentialmontecarlosamplersJRSSB.pdf). Framework reference; not claimed to prove our proposed dimension-uniform bound.
* Chopin, N. (2004). *Central limit theorem for sequential Monte Carlo methods and its application to Bayesian inference*. Annals of Statistics **32**(6), 2385–2411. [Author preprint](https://arxiv.org/abs/math/0508594). Background on particle asymptotics; not used to justify a simultaneous growing-dimension limit.

All project claims in this proposal are based on the permitted method text and inspected production code. The source-scope error disclosed at the beginning remains a limitation on the independence of this submission.
