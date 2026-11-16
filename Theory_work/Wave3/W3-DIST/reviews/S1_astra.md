S1 blind read — manifest fb6d0dab98b8083273c1df73693af90831329776915737bda397c39ec024b62e

Independent statement review. I used only the brief, manifest, INPUTS list, and the permitted sources. Song–Liang was read on journal pp. 950–956, PDF pages 4–10. No agents, git commands, or writes to other project files were used. This is a review of candidate statements and routes, not certification of unwritten proofs.

The main exponential contraction target survived my counterexample attempts after the domain repairs below. Lemma T is literally false on its stated dimension range. The blanket impossibility assertion following DIST-3 is false, and bridge B1 has a separate substantive counterexample. The distinction matters: these do not constitute a counterexample to DIST-1 under its explicitly stated sample interfaces.

## Findings

### S1-01 — MAJOR — Lemma T is false when its permitted dimension exceeds the range of the growth-function estimate

**Statement concerned:** Lemma T, its exact remainder, and ROUTES §2 Step 2.

Take n = 100, p = d = 10,000, and δ = 1/2. These satisfy every numerical restriction in T. Its displayed remainder is

    (4/100)[10000 + 20002 log(400e/10001) + log 8]
      = -1375.274996298749.

Choose a = 0 and u = 0, with any c > 0 and any design law. Both population and empirical truncated losses are zero. The claimed simultaneous inequality therefore requires 0 ≤ -1375.27, which fails for every sample. This is a deterministic counterexample, not a failure of a concentration constant.

The source of the problem is applying a Sauer-type polynomial bound beyond its applicable VC-dimension/sample-size range. The growth function must be saturated at the all-labelings bound when the dimension is too large. It cannot acquire a negative logarithm.

The intended reduction itself is good. For each support of size at most d, enlarge it to a support of exactly d. A level set of the truncated square is

    {x : |a + uᵀx| > sqrt(c z)},  0 < z < 1.

It is contained in the class of unions of two affine halfspaces on that coordinate subspace. On the intended sparse range, a valid growth-function upper bound is the number of supports times the square of the halfspace growth bound. The simultaneous class includes all intercepts, all coefficient magnitudes, and all levels. If the quoted relative-deviation inequality holds with η, layer-cake and Cauchy–Schwarz give

    Pg - P_n g ≤ η ∫₀¹ sqrt(P(g > z)) dz ≤ η sqrt(Pg).

Then η sqrt(Pg) ≤ (Pg + η²)/2 yields exactly Pg ≤ 2P_n g + η². No extra integration factor is missing. Dropping columns that happen to be constant in the training sample is also covered: the difference b - β* is supported on S ∪ supp β*, including the dropped true coordinates. Data-dependent centring and standardisation only select a member of this simultaneous raw-coordinate class.

**Minimal repair:** restrict T to 1 ≤ d ≤ min(p, n - 1), which covers the eventual theorem applications, or replace the growth-function formula by a correctly saturated bound. In the applications use d = min(p_raw, d_t + s₀^r), and the analogous capped value for DIST-2. Handle the intercept-only case explicitly. The Anthony–Shawe-Taylor source is not in the permitted packet, so I could not independently verify that attribution, its exact constant 4, or any small-n side condition. The proof leg must provide the precise inequality or prove the needed version; the layer-set and integration arguments do not resolve that bibliographic issue.

### S1-02 — MAJOR — Original dimension and retained dimension are conflated in the coded-posterior definition

**Statement concerned:** RD, the exact posterior in §0, m_n(t), DIST-1/2, and their assembly.

RD defines p_n as the dimension of the raw row x. The coded prior, cap, and store capacity instead use the number of retained columns. W3-POST §0 explicitly distinguishes this operational convention. Under the arbitrary design laws allowed here, these two numbers can differ with positive probability or probability one.

For a concrete discrepancy, take three raw coordinates, the first two independent continuous variables and the third identically zero. The code has p_ret = 2. The prior odds for a particular singleton relative to the empty model are 1/(2p_ret - 1) = 1/3. Substituting RD's p_raw = 3 gives 1/5. Thus this is not just an entropy notation issue: one reading of the formula identifies a different posterior. If all coordinates are population constants, RD still permits p_raw ≥ 2, while p_ret = 0. The inherited p ≥ 2 lemmas then do not apply, and the stated BB(1,p) convention needs a separate zero-column definition. A retained dimension of one is also possible.

Additionally s₀, p_ret, and hence the displayed m_n(t) are design-measurable when columns can be dropped. Calling this cutoff “data-free” is incorrect in the unconditional random-design experiment. It is deterministic after conditioning on X. This does not itself invalidate Lemma S, provided conditional uniformity is used correctly.

**Minimal repair:** introduce distinct symbols for p_raw and p_ret(X); use p_ret in w, Ω, K, ND, and the store capacity, and p_raw in the distribution-free transfer class. Use p_ret ≤ p_raw ≤ n^A in bounds. Either prove the p_ret ∈ {0,1} cases directly, or add their event to the stated failure remainder rather than silently excluding these laws. State the cutoff as X-measurable. Explicitly cover all s₀ ∈ {0,…,s₀^r}; “R1 sizes” in X must not import W3-POST's s₀ ≥ 1 restriction.

### S1-03 — MAJOR — The impossibility explanation after DIST-3 confuses model-selection error with Hellinger error

**Statement concerned:** the parenthesis after DIST-3 and the corresponding sharpness discussion.

The claimed reason that “no exponential inner threshold is possible” is invalid. W3-POST Proposition LB, as stated in the permitted W3-POST STATEMENT, bounds 1 - π(S₀), and requires 1 ≤ s₀ < p and s₀ + 1 ≤ K. These restrictions are absent from the parenthesis. It does not directly state a universal absolute lower bound on π(S ⊋ S₀). The deterministic superset comparison gives a bound relative to π(S₀), from which an absolute asymptotic bound follows when π(S₀) → 1. More fundamentally, neither bound says those models are Hellinger-far.

With a fixed-dimensional regular Gaussian design, a strong true singleton, and one independent null coordinate, the extra coordinate in the conditional posterior has coefficient mean O_P(n^(-1/2)) and standard deviation O_P(n^(-1/2)). Conditional draws in the one-extra-variable model consequently have joint Hellinger distance O_P(n^(-1/2)), not necessarily order sqrt(log n/n). A maximum over many candidate coordinates can produce a logarithm; this is not a property of every one-extra-variable model.

There is also a counterexample to the blanket impossibility assertion within the stated RD domain: p = s₀^r = 2, independent standard Gaussian coordinates, and two fixed nonzero coefficients. For all large n, K = p and there are no strict supersets. Underfitted models lose a fixed amount of signal and have exponentially small posterior mass outside exponentially unlikely data events. The full-model normal/inverse-gamma posterior has the usual chi-square/Gamma concentration. Thus for 1 ≪ u ≪ n, constants can be chosen to give an exponential inner and outer bound at radius C sqrt(u/n). Taking u = M_n² along, for example, a slowly divergent sequence gives the parametric contraction scale asserted in DIST-3, with an exponential threshold in M_n². All its energy, true-support floor, selection, and TR₀ assumptions hold.

**Minimal repair:** delete the blanket impossibility statement and the assertion about all one-extra-variable models. Say instead that mere δ_n → 0 gives no specified exponential control of the contribution δ_n, so the stated assumptions and assembly yield only the displayed in-probability conclusion. Any impossibility claim needs a separate example of Hellinger-far posterior mass and a specified range of M_n. The displayed contraction conclusion of DIST-3 survives this finding.

### S1-04 — MAJOR — The Song–Liang rate comparison and literal prior-condition claims need correction

**Statements concerned:** DIST-1(c), DIST-2's “short of [SL] by a logarithm,” ROUTES §1, and prior-probe §1/A1.

The supplied article has genuine little-o conditions (9)–(14); its Corollary 1 has fixed α ∈ (0,1). At p = n^A, A ≥ 1, the coded cap is floor(n/2). Conditions (9), (10), and (11), evaluated with that cap at either proposed rate, fail. The corrected reading of (11) in ROUTES is right: the harmless bound on the largest slab eigenvalue does not remove its factor r̄_n. A statement that (11) holds would be wrong.

The algebraic covariance envelopes are also right:

    λ_max(V_S^(-1)) = (λ_max(G_S) + 1)/n ≤ |S| + 1,
    λ_max(V_S) ≤ n.

However, these imply (14) only for a specified sequence r_n = o(n ε_n²). The coded beta-binomial mixture does not supply the fixed Bernoulli parameter r_n/P_n appearing in Song–Liang's theorem. Calling (14) a literal satisfied condition for that mixture is imprecise; the legitimate conclusion is that the relevant small-model precision envelope is benign. The empirical Gram and response-dependent IG rate are additional reasons a direct invocation is unavailable.

There is a specific little-o error in the helper report: at p = n^A, fixed s₀ > 0, and n ε_n² = u log n with fixed u, the support cost is asymptotic to s₀ A log n. Its ratio to n ε_n² tends to s₀ A/u, not zero. A sufficiently large fixed u can meet a constant-factor prior-mass requirement, but cannot establish the helper's displayed “≺” claim.

For Corollary 1, polynomial p satisfies its growth envelope for every fixed α > 0. The printed logarithmic branch gives ε_n² = O(n^(-(1-α)) log^k n). One may not substitute α = 0 or α_n → 0 into that fixed-α statement without a new argument. For every fixed α > 0, this displayed rate is slower than both log n/n and log² n/n. Alternatively, applying Theorem 2 directly to polynomial p requires r_n → ∞, r̄_n ≥ r_n, and r̄_n log n = o(n ε_n²). This allows many slowly varying losses, but does not produce a single canonical log n/n rate against which DIST-2 is exactly one logarithm short. DIST-2 is one logarithm slower than DIST-1 at polynomial p; that comparison is valid.

The no-identifiability comparison is fair only with its qualification: Song–Liang Theorems 1–2 do not assume Condition 3, which is introduced later for selection. They do impose envelopes on V and V^(-1), but choosing a data-free identity or ridge covariance does not require a predictor covariance eigenvalue floor. DIST-1's ND is therefore an additional geometric interface absent from those distribution-consistency theorems. “No eigenvalue floor” is a literal description of ND's form, not a proof that the design assumptions are weaker overall.

**Minimal repair:** compare the exact formulas and domains separately. Retain the metric normalization, exponential-form comparison, strict-sparsity limitation, and corrected failure of (9)–(11). Replace “short of [SL] by a logarithm” by “one logarithm slower than DIST-1 at polynomial p.” Describe (14) through its covariance envelope and a chosen reference dimension. Replace the helper's little-o prior-mass statement by a constant-factor bound.

### S1-05 — MAJOR — Bridge B1's exponential claim fails without coefficient-weighted tail control

**Statement concerned:** B1's claim that uniformly sub-Gaussian true coordinates and signal give exponentially small failure probability for (E) and (C).

Use the allowed triangular-array setting. Let B_n be Bernoulli(q_n), where

    q_n = 1/(100 n² log n).

Set x₁ = x₂ = B_n and β₁* = 3n, β₂* = -3n. Add two independent bounded continuous null coordinates so at least two columns are retained almost surely. Set M = M′ = 1 and use any fixed positive Gaussian noise variance. The true support has fixed size two. Every raw true coordinate is bounded by one, with a common sub-Gaussian bound, and xᵀβ* = 0 identically, also sub-Gaussian. Moreover

    Var(xᵀβ*) = 0,
    Σ_j β_j*² Var(x_j) = 18 n² q_n(1-q_n) < 1/2

for all large n. Even the squares of the weighted coordinates 3n B_n are uniformly integrable: their second moments are 9/(100 log n), tending to zero, and a tail beyond a growing cutoff can only arise at growing n. Thus a reasonable interpretation of the preceding uniform-integrability qualification does not rescue the exponential clause.

Let R be the number of Bernoulli successes among the n training rows. On R = 1 the unbiased sample variance of each of x₁ and x₂ is exactly 1/n. Both are retained, and

    ||θ*||² = 2(3n)²/n = 18n > nM′.

Energy (E) still holds identically because the two signal columns cancel. But

    P(R = 1) = n q_n (1-q_n)^(n-1) ~ 1/(100 n log n),

so the claimed exponential upper bound on the interface failure probability is false. The ordinary probability-to-one assertion is not contradicted.

**Minimal repair:** impose uniform sub-Gaussian control on the coefficient-weighted true coordinates β_j*(x_j - E x_j), or explicitly bound the true raw coefficients together with the existing coordinate tail controls. Constants must depend on these weighted tail bounds. B1 is an optional bridge, so this does not refute DIST-1/2 with their honest interface-failure remainder. It does prevent using B1 as written to discharge that remainder exponentially.

### S1-06 — MINOR — The X4 route omits factors that must be paid before uniform exponential conclusions can be claimed

**Statements concerned:** Lemma X, ROUTES §2 X4, and the consumption of helper Lemma V/Theorem P.

Without F₀, Lemma V(c) leaves a true-support residual R₀ ≤ P_{S₀}. It yields

    eᵀD′e ≤ σ*² χ²_{d_J} + ||P_{S₀}e||².

The second term cannot be discarded or called O(1) on an event with failure e^(-ct). It costs exp(Ct + C s₀ log n) in the likelihood bound on such an event. The helper's A3 explicitly includes this factor; ROUTES X4(b)'s displayed truncated-moment expression does not. The non-superset comparison contributes its additional polynomial factor in p and n. These are repairable by enlarging the constant in d_t - s₀, but they must be included before applying Markov.

For growing t, the variance denominator also needs a bound appropriate to each size. A safe envelope through j ≤ m_n(t) is

    ν/(2b + Q_{S₀∪J}) ≤ (1 + ε_{n,t})/(2σ*²),
    ε_{n,t} = O(sqrt(t/n) + (m_n(t)+s₀) log n/n).

Its truncated-MGF surcharge is of order ε_{n,t}(j log n + t), not just the single term displayed in the route. Uniformly for log n ≲ t ≤ n^(1-κ₀), ε_{n,t} → 0; for j beyond a sufficiently large multiple of t/log n, this surcharge can be absorbed in the negative determinant exponent. This supports the route, but requires a uniform calculation. The helper's Theorem P has n₀(u), so it cannot be substituted verbatim for a lemma with one n₀ working for every t in the full interval.

Finally the formal conclusion of X only states mean/variance contraction, while the distribution-free transfer also needs exponentially small posterior mass above d_t. X4 states that as structure, but the eventual lemma must include it as an actual conclusion on the same controlled event.

**Minimal repair:** retain the R₀ factor, the union-model multiplicity factor, and the full variance-denominator surcharge; choose C′ after budgeting all of them. Prove uniformity over t, and append the size-tail conclusion to X. I found no counterexample to X from these factors: t ≤ n^(1-κ₀) supplies enough asymptotic room. This is a route omission, not a claim that a candidate theorem must already have a finished proof.

### S1-07 — MINOR — Quantifiers, null truth, and small-p rates are inconsistent

**Statements concerned:** DIST-1(c), DIST-2, X′, S, and the common setting.

DIST-2 uses κ₀ without fixing it or allowing its constants/onset to depend on it. That dependence is needed by the route: on its good models the deterministic variance displacement is O(t log(p∨n)/n). To retain X's variance radius sqrt(t/n), one uses

    sqrt(t/n) log(p∨n) ≤ A n^(-κ₀/2) log n → 0,

whose onset depends on κ₀. DIST-2 also fixes s₀ although §0 allows design-measurable s₀; the uniform parameter should be s₀^r or a fixed upper bound.

The phrases M₀ “of order s₀(A+1)” and best squared rate “s₀ log n · log p/n” cannot cover s₀ = 0. The posterior still estimates variance and the plug-in intercept. For fixed p the latter DIST-2 rate also differs from the displayed t log(p∨n)/n rate. There is no general equivalence log p ≍ log n on 2 ≤ p ≤ n^A.

**Minimal repair:** fix κ₀ ∈ (0,1) in DIST-2/X′/S and list it in constant dependencies; use s₀^r as the uniform sparsity parameter; write 1+s₀ where an intercept/variance contribution persists. State the rate using log(p∨n), specializing to p = n^A only where that extra assumption is actually made. Treat s₀ = 0 explicitly in inherited R1-based arguments.

### S1-08 — MINOR — DIST-C needs explicit population-rate premises and a joint probability law

**Statement concerned:** DIST-C, especially (C-iii)/(C-iv).

The store and HPM deterministic transfers are correct under the stated exact-arithmetic convention. If π(B) ≤ q, then π({S: Π(B|S)>sqrt(q)}) ≤ sqrt(q); a ledger model with mass greater than sqrt(q) forces the maximum-score model outside that bad class. If π(S₀)>1/2 and S₀ is offered, both HPM identification and top-store retention follow directly from the inspected code. None of these steps requires a particle approximation to be returned.

Selection equality alone, however, is not the hypothesis of the supplied population-parametric theorem. DIST-3 also assumes the energy event, F₀, and TR₀. The sentences “with selection … which contracts at the parametric rate of DIST-3” and “on {MPM=S₀} … parametric rate as in DIST-3” should explicitly import those remaining hypotheses. The equality of conditional posteriors is deterministic; contraction is a statement along an experiment and is not a property of the equality event for an arbitrary single data set. I am identifying a missing qualification in this assembly, not asserting a counterexample to every possible stronger oracle theorem.

Also P* was defined as the law of the data alone. Events involving completion, the ledger, or MPM need the joint data/algorithm law, as W3-SAMP carefully specifies. The data-only bounds extend to that joint law because the bad output event is contained in the bad data event; independence is not needed for this deterministic inclusion. To invoke the stochastic delivery results one must retain their own ideal-stream and algorithm premises.

**Minimal repair:** use a separately defined joint law for DIST-C; explicitly attach DIST-3's other hypotheses to the parametric consequences; keep every sampler-delivery conclusion intersected with completion. D-iv, LT-e, C-v, and TR-d supply the stated types of conclusions under their own premises. Discovery itself can be obtained from D-i and P-OVL without P-MAP; the latter is needed for identification, not for a draw hitting S₀. No claim that completion probability tends to one is justified or needed.

### S1-09 — MINOR — A genuine flat-intercept posterior changes the variance shape unless the prior is adjusted

**Statement concerned:** the flat-prior-intercept remark in §0.

Augmenting an existing draw from the coded posterior by an independent conditional α ~ N(â,v/n) is a valid postprocessing convention. The rate arguments can accommodate its extra normal fluctuation. It is not automatically the same as fitting an uncentred model with a flat intercept prior and retaining IG(0.01,b).

In that genuine model, integrating the flat intercept removes one likelihood dimension, giving posterior shape 0.01+(n-1)/2 rather than the code's ν = 0.01+n/2. The permitted T04 statement and proof explicitly use IG(0.51,b) in n-1 contrast dimensions to recover the coded shape. The conditional intercept formula alone does not establish equality of the model weights or the joint posterior.

**Minimal repair:** call the extra intercept draw a postprocessing extension of the coded posterior, or specify the adjusted IG(0.51,b) prior for an equivalent full model. Distinguish equality of targets from equality of asymptotic rates. The default plug-in-intercept target is unaffected.

### S1-10 — MINOR — The numerical interpretation tests different objects from several asserted asymptotic claims

**Statements concerned:** ASSUMPTION_MAP §3 and the unchecked numerical report's interpretation.

N5 has p = 12 and all twelve coefficients nonzero. That is still strict sparsity as defined here: |supp β*| is a fixed finite number, twelve. It does not violate the stated asymptotic sparsity hypothesis. Its finite-n changes can illustrate delayed inclusion of small signals, but cannot establish what happens outside strict sparsity.

The reported tail slopes are from pooled posterior draws across data replications, estimating an averaged posterior exceedance probability. DIST-1/2 instead concern the distribution across data sets of the conditional posterior tail. A pooled slope is not a direct check of that nested-probability inequality, particularly at thresholds beyond the per-replication 1/4000 resolution. The report discloses this resolution limit but then calls the tail “genuinely sub-exponential” and infers the conditional logarithmic slope. Those are stronger conclusions than these checks establish.

Finally, the dangerous Schur scale identified in prior-probe §3 is γ ≍ log n/n for an unnormalised Gram. In a near-copy construction x_new = x₁ + τ z, the residual Gram scale is approximately nτ². Thus this particular regime requires τ² ≍ log n/n²; the listed τ² = log n/n does not test it. The n^-2 choice probes the constant effective-penalty scale, not the missing logarithmic scale.

**Minimal repair:** relabel N5 as fixed-dimensional weak-signal evidence; describe pooled tails as finite-n averaged-tail diagnostics; and, if this dangerous regime is to be probed later, add τ² ≍ log n/n². Do not use the existing simulations to discharge any theorem premise. I did not read the numerical scripts or raw arrays, which were not authorized inputs, so the implementation itself is not independently audited here.

### S1-11 — NIT — Manifest normalization and two literal qualifications

**Statements concerned:** review provenance; P6; predictive-consequence wording.

All permitted candidate documents and external inputs were hash-checked against the supplied manifest. Two raw-byte hashes differ: T04 PROOF_v2.tex and v3_ledger.h. In both cases converting CRLF to LF reproduces the manifest hash exactly (593 and 115 CRLF sequences respectively). Thus there is no detected content discrepancy, but the manifest's apparent raw-byte interpretation is not portable to this checkout. State the newline normalization used when freezing it.

P6's second bound requires a > 0; a = 0 is undefined and a < 0 can make the right side negative. Add this qualification. DIST-1(e) and C-i should say “on the complementary success event where posterior bad mass is at most the threshold,” since the event inside the preceding probability display is the failure event.

## Checks that did not produce a counterexample

**H.** The proof is sound for v>0. For r=v/σ*², the variance-affinity term obeys

    1-A ≤ 1-A² = (sqrt(r)-1)²/(r+1) ≤ (r-1)².

The mean-affinity bound and truncation are valid pointwise without moments. The sample identity Δ_i = ε̄ + (μ̂-μ)_i and its orthogonal squared-norm decomposition remain valid when true columns were dropped. A dropped column contributes its training constant to the fitted intercept comparison, while its out-of-sample variation remains in Δ(x).

**S, including the response-dependent IG rate and the n/2 cap.** I found no counterexample and the proposed strengthening looks viable. Here is a more explicit check of its slack. On a fixed-design response-variance bracket with failure at most C exp(-c n), the permitted size-tail proof gives

    π(|S|>m) ≤ A_m c_sharp exp(Λ_n) Θ_m,
    E Θ_m = 1,
    A_m = R_m sqrt(D_{S₀}) sqrt(n).

Use the proper, fixed-rate contrast-model mixture in Θ_m; this avoids taking an expectation of a response-dependent prior. The bracket is justified directly by Gaussian concentration of ||μ+e||²/(n-1) under (E), with fixed positive lower and finite upper endpoints. Nothing in the numerator integration requires small |S|: the Gaussian slab and IG prior are proper, including for singular design matrices, and every model up to K contributes a normalized density.

For m_n(t)<K, the elementary bounds R_m ≤ 2(2p)^s₀ 2^(-m) and D_{S₀} ≤ (n+1)^s₀ give

    A_m ≤ 2^(1-s₀) sqrt(n)/(n+1) exp(-3t).

This holds also when s₀=0. The cap case m_n(t)=K has identically zero tail. Gaussian/chi-square concentration gives Λ_n ≤ C₀+C₁ sqrt(t)+C₂t/sqrt(n) on exponentially likely events; uniformly for t≥log n this is at most t for sufficiently large n. The leftover n^(-1/2) factor absorbs the fixed c_sharp. Markov at Θ_m>exp(t), with a small allocation of the probability budget to the bracket and chi-square events, leaves the stated exp(-t) inner threshold and 2exp(-t) outer bound. This explains why the literal 3t cutoff is plausible, rather than merely asserting that Chebyshev can be replaced.

**X and DIST-1.** The coefficient cost is useful: the variational comparison gives L_{S₀} ≤ (||μ||²+||θ*||²)/n ≤ M+M′, even with a nearly singular true support. This blocks the obvious counterexample in which adding a proxy releases an arbitrarily large ridge bias. For small models, uniform noise and cross-term bounds give exponentially small mass to large ridge loss, while the conditional Gaussian and IG tails handle good models. For large models, the ND average is compatible with replacing the rank-dependent truncated moment by a uniform upper envelope before averaging. The extended ND range reaches the comparison unions through their added sets J. After the factors in S1-06 are retained, a sufficiently large size cut proportional to t/log n still has enough determinant decay to pay for them.

I tried the natural obstructions: duplicate/near-duplicate predictors, singular or weak true-support directions with compensating coefficients, rare unsampled design points, and underfitted proxies. Duplicates defeat the sharper size tail without ND but not with its stated range and constant. For a bounded-size sparse direction, a population truncated loss of order t/n that is invisible in the sample is precisely the kind of event controlled at order exp(-ct) by the repaired T; dropping a rare true column is not an automatic counterexample. I did not obtain a design satisfying (E),(C),(ND) on which Hellinger-far posterior mass is polynomially large on an event too likely for (1.1). This is not a proof that none exists.

**X′ and DIST-2.** Removing ND leaves m_n(t)=O(log n+t), so the fit/loss and transfer complexity are O(t log(p∨n)). The variance estimate initially contains both sqrt(t/n) and t log(p∨n)/n. The latter is absorbed by the former on the stated sublinear t-range once κ₀-dependent constants are restored. I found no need for an extra dependence/eigenvalue condition on the predictors. Independent Gaussian noise conditional on X and the coefficient-cost interface remain essential premises of this route; the theorem title should not suggest that (E) is literally its only interface.

**DIST-3 and TR₀.** Its displayed conclusion follows by conditioning on S=S₀, then adding δ_n and applying H and TR₀. TR₀ must use the original true support, as it does, so that missing in-sample constant true columns are not lost. Its fixed-law finite-second-moment example is correct even with singularity: for z=(1,x_T), population-null directions satisfy aᵀz=0 almost surely; restrict to the fixed range of E zzᵀ, where the smallest positive eigenvalue is fixed, and apply the matrix law of large numbers. This establishes the relative comparison for any C_T>1 eventually. It does not establish the same automatic comparison for arbitrary triangular arrays with shrinking positive eigenvalues or changing tails. Those arrays still need TR₀ as an explicit assumption.

**Code and DIST-C.** The inspected R output assembly has hpm at line 142, log_Z at 154, pip_r/pip_primary at 159–162, strict-threshold mpm at 163, and top_store at 210. The inspected ledger retains at most 40p_ret+1 distinct offered models ordered by score, and the inspected C++ serialization returns their models and values. No parameter draws, predictive distribution, or particle population is present in these final-output definitions. “Store BMA” is honest as a reconstructed, store-conditioned posterior; “HPM/MPM plug-in” is honest if understood as plugging in the model and retaining its conditional parameter posterior, not plugging in parameter point estimates. The definitions say this clearly. W3-SAMP explicitly excludes its separate exact-enumeration branch, so the code claim here should be scoped to this final-run/SMC output interface. I checked the allowed output and ledger files, not the unlisted scoring/engine/preprocessing files; exact score identification beyond these pins uses the supplied CC statement.

The deterministic retention assertion needs no inaccessible M4 proof: top-store ordering and π(S₀)>1/2 prove it directly. The permitted SAMP statements preserve joint-with-output localization and do not certify P-STORE without selection. The named RM2/START proof files and registry were not authorized inputs, so I did not independently verify those alternative source claims or their recorded statuses. They should remain cited conditional alternatives, not new premises silently treated as checked here.

## Verdict per statement

| Statement | Verdict | Scope of verdict / minimal action |
|---|---|---|
| DIST-1 | REPAIRABLE | Separate raw/retained dimensions and low retained counts; repair T; fix null-truth/rate wording. No counterexample found to (1.1) on the coherent p_ret≥2 domain. X4 still needs the uniform proof described above. |
| DIST-2 | REPAIRABLE | Same domain and T repairs; fix κ₀, sparsity, and log(p∨n) quantifiers; correct the SL comparison. No geometric design assumption beyond the listed interfaces was found necessary for this route. |
| DIST-3 | REPAIRABLE | Displayed contraction is SOUND-AS-STATED on a well-defined posterior domain; delete the false impossibility parenthesis and make empty-support conventions explicit. |
| DIST-C | REPAIRABLE | Deterministic transfers are sound under EX-A; specify the joint law, explicitly import the oracle population premises, and scope the code claim to the inspected final-run interface. |
| H | SOUND-AS-STATED | For the defined posterior draws v>0; proof checked, including centring and dropped columns. |
| T | FALSE-AS-STATED | Explicit negative-remainder counterexample; restrict dimension or saturate the growth bound and verify the quoted deviation inequality. |
| X | REPAIRABLE | No counterexample to the numerical core; fix s₀=0/domain conventions, include its needed size-tail conclusion, and retain the missing X4 factors. |
| X′ | REPAIRABLE | No counterexample to the numerical core; fix κ₀ and domain conventions and explicitly absorb the variance displacement. |
| S | SOUND-AS-STATED | On its fixed-design p≥2, feasible-reference domain, with fixed κ₀ and sufficiently large constants-dependent n₀; the cutoff and IG-rate mechanism survived checking. |
| P6 | REPAIRABLE | First inequality sound; add a>0 to the second. |

“SOUND-AS-STATED” here means no defect found at this statement-review stage, not that an unwritten proof has been completed or that inherited status labels have been upgraded.

## Better theorem

**1. Remove the true-support eigenvalue floor from the parametric distribution theorem.** In DIST-3 replace F₀ by (C), or more generally by a common bound L_{S₀}≤B with probability tending to one, while retaining (E), selection consistency, and TR₀. This is strictly weaker for the distribution target: F₀ supplies coefficient estimation in D(a), which is unnecessary here. Indeed D1 gives ||M_{S₀}y-μ||²≤2||P_{S₀}e||²+2L_{S₀}=O_P(1), and the conditional fitted-mean covariance has trace at most v s₀. Its residual sum of squares differs from ||e||² by O_P(1), because the cross term has variance at most σ*²L_{S₀}. Thus v-σ*² is posterior-tight at n^(-1/2), the in-sample mean error is posterior-tight at order one, and H+TR₀ plus δ_n→0 give the same conclusion. The stronger actual interface L_{S₀}≤B can hold even when (C) fails. No coefficient recovery claim should accompany this weaker version.

**2. State an oracle exponential bound with an additive selection error.** Under the preceding bounded-ridge-loss and energy interfaces and a realized TR₀ event with constant C_T, conditional Gaussian/Gamma concentration gives constants such that, for 1≤u≤n^(1-κ), outside a noise event of probability C exp(-cu),

    Π(d_H>C sqrt(u/n) | D_n) ≤ δ_n + C exp(-cu).

For a selected-model posterior equal to Π(·|S₀,D_n), the δ_n term is absent. Add the probabilities of the energy/ridge-loss/transfer events failing when integrating over X. The proof uses only one true support, so its projection rank is bounded and no union over p models or log n complexity payment is needed; the noise mean contributes another one-dimensional Gaussian tail. This gives an exponential statement in many oracle/output cases without asserting an exponential selection rate, and makes the actual obstruction to a pure exponential exact-posterior bound explicit. Applying the same argument with u=M_n² recovers the parametric in-probability theorem, including when M_n diverges slowly.

**3. Make the size lemma reference-adaptive and remove the unnecessary polynomial-p restriction from that lemma.** Given any design-measurable reference (T,ϑ), let B_T(ϑ)=||μ-X_Tϑ||²+(||X_Tϑ||²+||ϑ||²)/n≤B. The permitted approximate-reference proof and Gaussian concentration give a finite-sample exponential bound whenever

    log R_m^T + (1/2)log D_T + (1/2)log n
      + C[1+B+sqrt((1+B)t)+t/sqrt(n)] ≤ -2t,

with a bracket failure C exp(-cn). Markov on its normalized fixed-rate numerator then yields π(|S|>m)≤exp(-t) except with probability C exp(-t)+C exp(-cn). Constants depend on the energy/noise bracket, not on p. This keeps the exact determinant instead of (n+1)^|T|, permits a smaller approximate reference, and covers arbitrary p whenever the displayed cutoff is feasible. The proof is the checked S mechanism with the Gaussian approximate-reference cross term restored. It is a size theorem; it does not by itself justify the proposed population S-APX statement, whose out-of-sample approximation term still needs control.

**4. Give one output-transfer theorem for any distribution of model weights.** Let an output-dependent law Q on models satisfy Q(S)≤L_n π(S) for all S, and let the reconstructed parameter posterior use the exact conditional kernels Π(·|S,D_n). Then QΠ(B)≤L_n Π(B) pathwise for every measurable B. Store BMA has L_n=1/π(𝒯), and a selected model has L_n=1/π(Ŝ). Hence the exact-posterior exponential bound transfers whenever log L_n≤λt with λ<c, with inner exponent c-λ. This strictly extends the fixed-η store formulation by allowing exponentially vanishing retained mass when the exponent budget permits it, and includes arbitrary admissible reweightings. For HPM the existing P-HIT argument supplies the domination bound through a discovered model's mass. Keep the observable output construction distinct from the unobservable domination premise, and intersect stochastic delivery conclusions with completion as before.

Overall verdict for a proof leg: GO-WITH-REPAIRS — the main conjugate/transfer route remains plausible, but repair the false transfer domain, false bridge and impossibility claims, and the posterior-domain/comparison qualifications before locking statements for proof.
