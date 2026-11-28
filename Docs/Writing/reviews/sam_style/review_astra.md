# Independent review of A1–A10 and C1–C3

“Spec” means the Theory specification, §5. SAM page numbers are journal pages unless marked “supp.” Designs follow the owner's November 24 grid. A finite grid cannot establish a limit. For growth claims I continue each arm with fixed sparsity, fixed correlation and its stated signal rule, with polynomial dimension. I flag any dependence on that continuation. The design tests below concern the generating law. The computer conventions concern individual runs.

## A1. Gaussian linear model

- **Origin — same.** Spec 5.1, p. 15. SAM (1), p. 947, and joint law (2), p. 950, use linear means and independent Gaussian errors of common variance. Our intercept allows a location shift.
- **Pushback — low.** A standard benchmark model. Clustered errors, heteroskedasticity and heavy tails would need separate justification.
- **S1 — holds.** Independent Gaussian noise with variance one.
- **S2 — holds** within each HTT arm. The positive variance is deterministic given the design parameters and ν. Changing ν changes experiments. For a continuation that also changes support spacing and hence signal variance, fixed noise variance needs a separate check.
- **S3 — plausibly holds.** The usual Gaussian-response construction suffices. The S3 row specifies the predictor correlation and sparsity but leaves the response-noise rule unstated.

## A2. Polynomial dimension

- **Origin — not comparable overall.** Spec 5.2, p. 15. SAM assumes growth faster than some positive power on p. 950. Its density Corollary 1 allows an exponential in a fractional power of n (p. 954), and MAP Corollary S1 allows a power of n proportional to log n (supp. p. 16). Our upper limit is tighter and we allow bounded p.
- **Pushback — medium.** A million predictors in a finite example establishes little about growth. A fixed exponent excludes important ultrahigh-dimensional sequences.
- **S1 — holds.** The largest log(p)/log(n) is 1.371, at (500,5000). A=2 covers the grid.
- **S2 — holds.** The corresponding maximum is 1.766 at (50,1000). A=2 suffices.
- **S3 — holds.** Same sizes as S1.

## A3. Fixed nonempty truth

- **Origin — same for a nonempty truth, stronger than SAM's approximate sparsity.** Spec 5.3, p. 15. SAM (4), p. 950, used by Theorem 2, p. 953, asks for a finite limit of the integer support count, hence eventual constancy, and allows zero. Its (3), used with Theorem 1, permits many small effects.
- **Pushback — medium.** It excludes increasing sparsity and polygenic signals. Theorem 6(a)'s obstruction to the advertised rate only forces an upper order of roughly √log n in its applicable regime.
- **S1 — holds.** Exactly ten active.
- **S2 — holds** armwise with five or ten. The pooled two-point grid changes s, so it supplies no evidence of a single fixed-s trajectory. All specified beta-types have exactly s active entries.
- **S3 — holds** separately for s=5 and s=10.

## A4. Law of the rows

- **Origin — stronger than SAM Condition 1 for centred unit-variance predictors.** Spec 5.4–5.5, p. 16. SAM Theorem 2 and Condition 1, p. 953, control an exponential moment of a bounded-weight average. A closer precedent for (a) is Narisetty–He (2014), Lemma 6.1, arXiv v1 p. 16, for independent isotropic sub-Gaussian rows. Our sparse, variance-scaled bound allows correlated rows. Our (b) requires Gaussianity.
- **Pushback — medium.** The short note's cap qualification is unnecessary: the single-coordinate bound already gives SAM's moment for every cap. With |a_i|≤δ, convexity of exp(t²) bounds the exponential of the squared average by the average of exp((a_i x_i)²). The converse lacks variance-relative control in nearly cancelling directions. Arbitrary unbounded means need centring for this comparison. SAM's bounded-input Theorem 1 (p. 952) and its weaker second-moment Condition 2 (p. 954) are distinct.
- **S1 — holds.** Independent Gaussian rows give the exact MGF in every direction with L=1.
- **S2 — holds.** The HTT Gaussian AR rows satisfy both forms at every ρ.
- **S3 — holds** under the Gaussian-row family specified in BENCH_DESIGN §0. Equicorrelation changes the variance inside the MGF and preserves equality.

## A5. Fixed signals on the raw or standardised scale

- **Origin — stronger as written.** Spec 5.6–5.7, pp. 16–17. SAM (3)–(4), p. 950, and Theorems 2–3, pp. 953, 956, state no uniform beta-min. The sure-screening proof uses the omitted coefficient squared times the identifiability gap divided by the noise variance (supp. pp. 5–6). A genuinely fixed finite vector supplies fixed bounds on its active entries. The proof does not establish screening for arbitrarily shrinking signals.
- **Pushback — high.** A vanishing effect can still be detectable. Also, with raw coefficients fixed, the coefficient on the sample-standardised column is β_j times its random sample SD. Convergence of that SD to one does not make the coefficient deterministic, as Theorem 3 requires.
- **S1 — fails** both forms. Raw beta-min is 2 SNR √(log p/n), from 0.0788 to 0.7831 on the grid and tending to zero under polynomial growth. Standardisation also makes the coefficients random.
- **S2 — holds** for (a): types 1–2 have active coefficients one, type 3 ranges from 0.5 to 10. **Fails** for (b) under the stated raw HTT construction.
- **S3 — not checkable.** The fixed design order does not specify coefficient magnitudes or the scale on which the mean is generated. Fixed raw effects would meet (a), while S1's scaling would fail.

## A6. Population sparse eigenvalue floor

- **Origin — stronger than SAM's Gaussian identifiability test on covered sets, otherwise not comparable in general.** Spec 5.8, p. 17. Condition 3, pp. 955–956, is used by SAM Theorem 3 for an individual true predictor, not by its density Theorem 2. If the cap plus the target fits our window, a fixed floor gives residual variance ≥φ² and a Gaussian imitation gap ≥1−(1+2φ²)^(-1/2). Condition 3 need not protect two duplicate nulls. SAM MAP Theorem S, (22)–(23), supp. p. 13, and (26), supp. p. 15, instead constrain both sample spectral tails and allow moving bounds.
- **Pushback — medium.** Uniform protection of null-only subsets rules out redundant probes even when the truth is distinguishable. A population bound alone cannot certify an observed Gram matrix.
- **S1 — holds.** The AR(1) spectral lower bound (1−ρ)/(1+ρ) is 0.25 for every principal submatrix. This is a uniform lower bound, not the exact finite-matrix minimum.
- **S2 — holds.** The same bound is 1, 0.48148 and 0.17647 for ρ=0, 0.35 and 0.7.
- **S3 — holds.** Every m-column subset with m≥2 has eigenvalues 1−ρ and 1+(m−1)ρ. The exact floors are 0.5 and 0.2, even as the largest eigenvalue grows.

## A7. Distribution-level assumptions

- **Origin — not comparable as a package.** Spec 5.9(a–e), p. 17, specialises the SAM Theorems 1–2 Hellinger setting, pp. 952–954. The joint distance and concentration objective are precedents. Our fixed support bound, polynomial dimension, sparse sub-Gaussian control, population floor cψ/n and bounded individual signal measured in noise SDs are our combination. There is no beta-min, and σ may vary. SAM's ridge of order 1/n (p. 953) regularises a prior matrix and does not impose our population floor.
- **Pushback — medium.** Removing exact duplicates cannot ensure the floor: a correlation of 1−n^(-2) already violates it. A bound on signal in noise units is substantive when noise can vanish.
- **S1 — holds.** Take s=10, A=2, L=1 and cψ=1. A6 covers every window. The largest |β_j|/σ on the grid is 9√(log(5000)/500)=1.175; it stays bounded on the stated continuation.
- **S2 — holds.** Take s=10, A=2, L=1 and cψ=1. Since coefficients and correlations are nonnegative, βᵀΣβ≥max β_j². Thus max |β_j|/σ≤√ν≤√6, including optional type 3.
- **S3 — not checkable** in full. Gaussian rows, s≤10, polynomial p and the floor pass (even cψ=1 works). A Gaussian response with uniformly bounded |β_j|/σ would complete the check.

## A8. Uniform conditional visibility

- **Origin — stronger than SAM Condition 5, p. 958.** Spec 5.10, p. 17. SAM asks for nonzero marginal covariance for its iterative screening argument. Our lower margin must survive every conditioning set of up to 15, including the empty set.
- **Pushback — high.** It depends jointly on effects and correlations and is vulnerable to suppression. A floor for Σ does not prevent cancellation of a true variable's signal covariance.
- **S1 — fails.** At U empty, the second coordinate of Σ times the unscaled coefficient template is −0.16035072 (rounded). Its magnitude multiplied by SNR √(log p/n) tends to zero. One such covariance disproves a uniform positive margin.
- **S2 — holds** for the population coefficient templates of types 1–3. For positive AR(1) the precision is tridiagonal with nonpositive off-diagonals. Its principal submatrices have entrywise nonnegative inverses, so all conditional covariances are nonnegative. The self term alone is at least (min active β)(1−ρ)/(1+ρ), uniformly ≥0.0882 including type 3. This visibility calculation does not supply the missing deterministic standardised truth in A5(b).
- **S3 — not checkable.** With m conditioned columns the partial signal covariance for j outside U equals (1−ρ)θ_j + [ρ(1−ρ)/(1−ρ+mρ)] Σ_{k outside U} θ_k. Fixed same-sign active coefficients bounded away from zero suffice. Mixed signs can cancel, and a shrinking template loses the margin.

## A9. Leakage set, locality, floor and regressions

- **Origin — no comparable SAM assumption as a package.** Spec 5.11(a–c), pp. 17–18. SAM remark (a), p. 958, informally counts correlated predictors. It supplies no conditional decay, uniform local regression approximation or allowance for our model-size cap. The floor component resembles A6.
- **Pushback — high.** These are simultaneous requirements on unknown population regressions designed for Theorem 3's start and local search. In particular, 15b_H+b<1/2 forces b_H<1/30. With any null outside Q, n^(1/30) must exceed or equal s₀+1. At all listed sizes n^(1/30)≤1.259. Since p>√n, Q cannot contain all predictors. This finite-size obstruction even affects independent rows.
- **S1 — fails at grid sizes; plausibly holds asymptotically.** At n=500 even the minimum cap requirement 2s₀+32s₀+1=341 exceeds K=250. In a growing AR sequence choose Q within radius C log n of the support, with C large enough that ρ^(C log n)=o(√(log n/n)). Conditioning in an AR chain blocks paths or reduces their covariance. Logarithmic neighbourhoods of l and the truth ensure locality; the A6 floor holds. Regression uses the nearest selected index on each side. Keeping all Q indices within radius √log n of l discards only coefficients of order ρ^(√log n), uniformly over selected subsets. These sets eventually fit the powers, and K must eventually fit Q.
- **S2 — fails at grid sizes; plausibly holds asymptotically.** K=25 or 50, versus a minimum 34s₀+1 of 171 or 341. For independence Q=S₀, H_l={l}∪S₀ and empty regression neighbourhoods suffice eventually. For positive ρ the S1 argument applies around each of the fixed number of active sites. With p fixed, ultimately Q=all is also possible.
- **S3 — fails at grid sizes and along growing high-dimensional arms with p≥√n.** At U empty every outside null has covariance ρ≥0.5 with each true variable. The no-leak bound tends to zero, forcing Q=all, which violates |Q|≤n^b. A6 supplies the floor throughout. If p is held fixed forever the size obstruction eventually disappears.

## A10. Certified-screening budget

- **Origin — not comparable to SAM sure screening.** Spec 5.12, p. 18, Theorem 4, p. 22. Our fixed-design floor, beta-min, ℓ₁ upper bound and explicit budget jointly bound errors of certified local optima. SAM Condition 3 and Theorem 3, pp. 955–956, address posterior inclusion for an identifiable variable. Its MAP sample-Gram comparison is supp. (22)–(23), p. 13.
- **Pushback — high.** The factor 200 alone rules out every benchmark cell, regardless of sample covariance, budget or signal strength. Since κ≤1 and M₁≥s₀·θ_lower, cn≤n/(200s₀²); even k=0 requires log(pn)≤cn. The theorem bounds a joint error event and does not guarantee a small certified output.
- **S1 — fails.** Right side ≤0.05, left side ≥log(500·500)=12.43. The fixed signal floor also fails along the sequence.
- **S2 — fails.** Right side ≤0.01 in the five-signal arm and ≤0.005 in the ten-signal arm. Left side ≥log(50·1000)=10.82.
- **S3 — fails.** Right side ≤0.2 even at n=1000 and s₀=5. Left side ≥12.43. No sample realisations or coefficient values are needed to reject the conjunction.

## C1. Admissible method

- **Origin — no comparable SAM convention.** Spec 5.22, p. 19, fixes exact arithmetic, the default configuration, a valid input and seed. SAM's fixed-data sampling limits (supp. pp. 9–10, 12–13, 16–17) concern its own algorithm.
- **Pushback — low.** Routine mathematical specification. A claim about a particular executable needs its version, settings and arithmetic.
- **S1 — not checkable.** Gaussian inputs are nondegenerate almost surely. The design supplies no seed, settings or exact-arithmetic execution.
- **S2 — not checkable.** Noise is positive even at the highest ν. The run conventions still require separate evidence.
- **S3 — not checkable.** Positive definite Σ makes constant predictor columns a null event. Response validity and run settings remain separate.

## C2. Delivery and lifted integer limits

- **Origin — no comparable SAM condition.** Spec 5.23–5.24, pp. 19–20, defines C2 and C2p separately. C2 demands an ideal unit-cost machine, functioning dependencies, the specified start-mode tie rule and search, bounded worker/island counts, ideal uniforms, stop rules and sufficient declared resources. C2p additionally lifts two integer caps. Spec Theorem 3, p. 22, guarantees delivery under C2 on its declared domain; the all-admissible-n statement uses C2p.
- **Pushback — high** if described as delivery on real hardware. An operation bound cannot guarantee allocations, no interruptions or exact arithmetic on the reader's machine.
- **S1 — not checkable.** Dimensions do not verify resources, defaults or ideal arithmetic.
- **S2 — not checkable.** Small n supplies no machine or execution guarantee.
- **S3 — not checkable.** Equicorrelation supplies no evidence about the delivery convention.

## C3. Ideal sampling and independent final streams

- **Origin — standard SMC identity; our implementation conditions have no comparable SAM counterpart.** Spec 5.25, p. 20. Schweizer (2012), Proposition 2.3, arXiv:1204.2382 p. 7, gives the unnormalised-measure identity (set f=1), following Del Moral–Miclo (2000), §2. Our proposition conditions on the frozen pilot. C3 also requires the exact start normaliser, exact start draws, correct kernels in state-independent uniformly random order, fresh streams and measurable records.
- **Pushback — low** for the potential uninterrupted run. The identity does not establish unbiasedness conditional on completion if stopping depends on the run. Empirical agreement cannot prove exactness.
- **S1 — not checkable.** The predictor law cannot establish exact kernels or independent final streams.
- **S2 — not checkable.** The same conditions must be imposed for each pilot and ν.
- **S3 — not checkable.** The same identity is design-free once the sampler conditions hold.

## Verdict

A1 and the nonempty strict-sparsity case of A3 match SAM. A2, A4, A5 and A6 are familiar types of restrictions with materially different scope here. Theorem 1's fixed raw beta-min excludes S1. A7 is our particular set of conditions for the SAM-style density conclusion in Theorem 2. It covers S1 and S2 even when selection is hard. The S3 signal/noise specification is needed to claim coverage.

Theorem 3 carries the greatest exposure: A5(b) fixes truth after sample standardisation, A8 strengthens marginal visibility, and A9 restricts leakage and every relevant local regression. The finite A9 size bounds fail throughout. S3 also exposes a population obstruction whenever p grows at least as fast as √n. Theorem 4 avoids visibility and leakage but its explicit A10 inequality fails throughout. These failures concern the sufficient hypotheses, not observed algorithm performance. Proposition 5 is classical under C3. Delivery in Theorem 3 needs the precise C2/C2p distinction. Theorem 6(a) is unconditional; 6(b) adds its own witness condition (Spec 5.13, p. 18), including independent Gaussian null columns or exact orthogonality. Among the grid arms only S2 at ρ=0 supplies the independent-null structure.

## What the sources do not settle

- BENCH_DESIGN §6.1, its CITE_CHECK and the shared simulation citation text fix S3's covariance, sizes and sparsity but do not fix its active coefficients, signal scaling, signs or noise law. Earlier manuscript examples use other design labels and cannot fill these gaps.
- No growth trajectory or simulator execution record accompanies the grid. The asymptotic AR assessments above state their continuation explicitly. No finite simulation establishes exact arithmetic, stream independence or absence of resource stops.
- No SAM condition states our A5(b), A7, A9, A10 or C1–C3 verbatim. Internal spec numbers and pages identify the actual assumptions; a numbered external source is given where there is a matching result or a specific precedent. The Schweizer and Narisetty–He page pointers are supported by the department's source audits, not an independent full-text check in this review.
