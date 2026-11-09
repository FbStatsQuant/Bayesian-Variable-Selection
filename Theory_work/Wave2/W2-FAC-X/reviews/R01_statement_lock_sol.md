# R01 — independent STATEMENT-LOCK review

**Verdict: REJECT.**

Reviewed STATEMENT v1 and PLAN against FAC-B STATEMENT v3.1 and L1–L5, FAC-A L5.1, and the Wave 2, Wave 1C and Wave 1 protocols. Also read `numerics/iid_core.py` and `numerics/iid_selftest_out.txt`. Review is analytical; the constructions below are explicit counterexamples to proposed auxiliary assertions, not claims of numerical simulation. No file other than this review was edited.

The statistical target is the right one. The draft preserves the merged method, score, prior, move rule and MR1 cap, and its strict limsup condition means that some fixed A < 1/2 bounds p eventually. Allowing bounded or irregular p is appropriate. The arbitrary raw mean disappears on centring; fixed raw coefficients and random standardised coefficients are correctly distinguished. I find no counterexample here to the eventual consistency conclusion on the intended nonempty-support class. However, two central assertions in the proposed proof architecture are false. Consequently the advertised band width and path conclusion cannot be locked on this plan. This rejection is not an asymptotic-versus-finite-sample objection.

## Required changes

1. **Replace PLAN X3: approximate argmin plus exact centre drift does not imply the claimed O(beta) window or the 8 beta band.**

   References: PLAN lines 20–24; STATEMENT lines 72, 75–76. Here is an explicit deterministic counterexample even with approximation tolerance beta, rather than the statement's larger tolerance 2 beta.

   Fix beta > 0, s0 = 1, kappa = 1 and varrho = 0. Start with M + 2 nulls and one truth. Define

   ```text
   x_0 = 0,
   x_{i+1} = x_i - beta/(M + 3 - i),       0 <= i < M,
   y_i = x_i + beta,
   L = sum_{r=4}^{M+3} 1/r,
   x_M = -beta L.
   ```

   Give the M nulls to be deleted the fixed coordinates y_0,...,y_{M-1}; give the two surviving nulls coordinates x_M - beta/4 and x_M + beta/4; and give the truth coordinate 2x_M. These are consistent with the stipulated centre formula: the sum of the y_i is -4x_M, so the initial total is zero. At step i there are k_i = M + 3 - i variables, and deleting y_i gives exactly the displayed drift, since k_i - 1 + kappa = M + 3 - i. Thus the actual reference centre is x_i throughout.

   Every chosen deletion satisfies

   ```text
   |y_i - x_i| = beta <= min_kept_null |xi - x_i| + beta.
   ```

   At the last set, a = x_M - beta/4 and b = x_M + beta/4. The first deleted point y_0 = beta is outside (a - 8 beta, b + 8 beta) whenever L > 29/4. Such M exist since the harmonic sum diverges. The centre travels beta L, of order beta log M, rather than O(beta). Distinctness can be ensured by an arbitrarily small generic perturbation without eliminating the strict band violation.

   This disproves X3(c),(d) as universal deterministic assertions. The inference that small-hole crossings form a spatially confined initial phase is unsupported: local bounds on a crossing and monotonicity on steps without crossings do not bound the cumulative displacement during crossings. The construction can be scaled to arbitrarily small beta. It is not a high-probability Gaussian counterexample, since its point configuration is specially arranged. A viable repair could use a genuinely probabilistic anti-concentration/density hypothesis to prevent such a configuration, or a wider invariant with recalculated perturbation bounds. That hypothesis and its proof must be explicit. Merely adjusting 4 to 8 does not fix the logarithmic accumulation. Also reconcile X3's beta tolerance with X2(i)'s 2 beta tolerance.

2. **Remove the uniform no-addition assertion over the entire structured family in PLAN X4; prove the needed bound only with additional path balance restrictions, including the intermediate sets used for swaps.**

   References: PLAN lines 26–30; FAC-B L4.3–L4.5. The phrase “any addition to any T in [the structured family]” is false for the natural family defined only by the proposed band-controlled interval hole, even with band width zero.

   Take p = floor(n^A), with 1/6 < A < 1/2, one fixed truth, and bounded positive limiting kappa. Among the iid null coordinates let T retain just the m largest positive coordinates, where m = floor((log p)^(1/4)), together with the truth. Write H = sqrt(2 log p). With probability tending to one these retained coordinates are H + O(log log p/H), the most negative outside coordinate is -H + o(H), and the truth/offset contribution is negligible. The reference centre is

   ```text
   x_T = m H/(m + s0 + kappa) + o(H/m).
   ```

   It is below the smallest retained null: the displacement H/m dominates the top-order-statistic spread. Hence a_T = -infinity and b_T is the smallest retained coordinate. Every deleted null lies strictly below b_T. This is an exact interval-hole configuration, with no band defects.

   Adding the most negative outside coordinate has squared residual statistic (4 + o(1))H^2, with the addition normalisation tending to one. Its likelihood gain is (4A + o(1)) log n, whereas the determinant plus BB size penalty is (1/2 + A + o(1)) log n. Its total gain is

   ```text
   (3A - 1/2 + o(1)) log n > 0.
   ```

   This calculation already holds in the ideal reference score; the iid perturbations at these coordinate-defined, small retained sets do not supply a log n correction that could reverse it. It directly contradicts PLAN X4's proposed family-wide negative bound. FAC-B itself warns in L4.5(3) that no-addition fails on unrestricted retained sets. A hole constraint alone does not supply the bulk small-centre bound or end-phase imbalance dynamics proved there.

   For swaps, the identity G_swap(j,l;T) = G_del(j;T) + G_add(l;T-minus-j) is valid. But the second term must be bounded at every required null-deleted intermediate set, not merely at visited sets. Such a set need not inherit the balance invariant for the chosen deletion. State and prove the enlarged invariant actually needed for this comparison, or retain FAC-B's direct swap analysis with controlled errors. The counterexample is not a claim that the production path reaches these unbalanced sets.

3. **Correct the first-order perturbation scaling and specify absolute score/statistic errors sufficient for the scan comparisons.**

   References: STATEMENT lines 26–28; PLAN lines 9–18. With W ~ Wishart(N,I), an off-diagonal W_jl has standard deviation sqrt(N). The displayed `(1/sqrt(N)) sum_l (W-NI)_jl (xi_l-x_T)` therefore has generic size sqrt(p), not sqrt(p/n). The inverse expansion in PLAN uses R = (W-NI)/N; its first-order contribution is a projected expression involving `-(W-NI)/N`, together with the outer reference inverse. Write the actual formula with the correct normalisation and sign, rather than identifying the displayed expression as the first-order term.

   PLAN X1's claim about “every exact neighbour gain” having relative O(1/n) errors also needs replacement or a carefully delimited definition. Likelihood increments can vanish, and total gains can approach zero by cancellation. A relative approximation to those quantities is not supplied by a Q-versus-RSS sandwich. Ridge produces nonzero corrections even at an exact zero least-squares residual correlation; determinant corrections also vary by set. Give separate uniform absolute bounds for the signed partial statistic, determinant increments, and residual/likelihood multiplier, and show they imply the advertised approximate argmin and strict move comparisons. FAC-B L1's exact ridge centre also has a signal-dependent offset and a different kappa; the W=NI, a=0 identity here is an RSS reference analogue, not literally FAC-B's entire exact score reduction.

4. **Specify the treatment of the random partition and N0 without assuming independent selected noise coordinates or a Gaussian adaptive Wishart row sum.**

   References: STATEMENT lines 53–61; PLAN lines 15–18, 27, 33–35; FAC-B L2.4 remark (2), L3 E1/E5/E6. The unconditional independence of W from xi is correct, but it does not imply independence after selecting the realised partition. The raw Gram matrix is a function of xi, eta, a, phi and W, so the X-measurable N0 is generally dependent on them. Cardinality at most 15 does not justify applying fixed-index Gaussian bounds to xi restricted to N0. Nor are the signs in the selected complement automatically iid conditional on its magnitudes.

   A valid plan should say which estimates are proved over the full deterministic null set, how deleting at most 15 adaptively selected coordinates changes the balance/extreme-order bounds, and which zero-pair bounds are proved conditionally on X (where the block is fixed and the noise is Gaussian). Do not directly import FAC-B's E1 claim that max over N0 is at most log log n from its deterministic-partition proof.

   In X2's rowwise conditional Gaussian argument, separate the diagonal R_jj term before conditioning on u_j-perp. Also separate the random scalar coefficients: c_l = xi_l - x_T in the reference case, and x_T depends on phi, hence on W if a set is adaptively selected using W. For xi-defined intervals one can bound linear sums with weights xi_l and 1 separately and then multiply by a bounded x_T; for N0 and band selections use genuinely uniform crude bounds. Define the structured family, its band-count envelope nu_n(w), and its endpoints precisely enough that the stated event is not circular. This is an obligation to repair the argument, not an assertion that these dependencies make the target theorem impossible.

5. **Make the support and FS-prime hypotheses unambiguous for a random partition.**

   References: STATEMENT lines 40, 47–49; FAC-B STATEMENT model G and C1-M. Explicitly require s0 >= 1. The new Model R replaces FAC-B's G and does not itself restate its nonempty-support assumption. If the empty support is allowed literally, FS is vacuous, and every block contains all truths. With fixed p = 17 and beta = 0, the union definition inherited from FAC-B gives N0 = [p], contradicting |N0| <= 15 and X1's m0 >= p - s0 - 15 (here m0 = 0 but the lower bound is 2). If the singular phrase “the block” is used instead, N0 is undefined because no unique block is identified. Preserve the intended nonempty class explicitly.

   FS itself can and should be stated as a finite population condition on the fixed raw vector and rho. FS-prime, however, also contains the requirement that each masked truth's realised block contain a null. That is not just a condition on vartheta and rho when the partition is random. State whether this block event holds almost surely by construction, with probability tending to one under a proved property of the method, or is an additional hypothesis. An implication only conditional on a realised block event does not give unconditional joint-law conclusions unless that event has probability tending to one. Restating the actual FS/FS-prime conditions locally will make this distinction visible.

6. **Present the A < 1/2 bootstrap as conditional on a repaired path invariant, and correct the frontier algebra.**

   References: STATEMENT lines 65–67, 88–90; PLAN lines 16–18. The proposed beta rate itself is consistent with P-half: for some A < 1/2, beta is O(n^(-(1-A)/2) log n + n^(-1/3)), so beta <= n^(-c) eventually for a suitable smaller c > 0. The crude second-order p^(3/2)/n term is also absorbed, since its ratio to the main beta term is O(p/(sqrt(n) Hbar sqrt(log n))) = o(1). These are not grounds for rejection.

   If w = 8 beta really were available, the displayed band absorption coefficient is O(p Hbar sqrt(log n/n)), which tends to zero for A < 1/2. This is a plausible conditional perturbation bootstrap. It does not establish w = 8 beta: that currently rests on the false deterministic assertion in item 1.

   STATEMENT's `p beta Hbar/sqrt(n) asymp p/sqrt(n)` is not an equality of orders. The expression on the left has extra beta Hbar, and comparison with the error budget requires division by beta (and the row maximum introduces logarithmic factors). State the actual error and its ratio to the budget. Describe leave-one-out as a possible approach, rather than claiming it “would remove” the obstruction without an argument. Do not advertise 1/2 as a checked frontier of this proof until the invariant and the path balance estimates have survived review.

## Representation independently checked

The central independence claim in STATEMENT section 3 is correct under the joint model, with phi taken nonnegative and for sufficiently large n (which is all this target requires).

Work in the d = n-1 dimensional centred subspace. Write f and u_j as independent standard Gaussian vectors there, independent of e. Conditional on e/||e||, put eta = <f,e/||e||> and let phi be the length of the remaining factor component. Then eta is standard normal and phi^2 is chi-square with d-1 = n-2 degrees of freedom, independent of eta and ||e||. Rotate the remaining subspace so that its first axis is that factor component. Conditional on this frame, each u_j has independent coordinates xi_j, a_j and v_j in dimensions 1, 1 and d-2. The conditional distribution of these coordinates does not depend on the frame or the factor/noise variables. Thus all xi_j, a_j and v_j are mutually independent standard Gaussian coordinates, independent of (||e||,eta,phi). Consequently W = (v_j'v_l) is Wishart_p(n-3,I), independent of (||e||,eta,phi,xi,a). No independence from the realised design/partition follows.

With v1 = xi + ell eta 1 and v2 = ell phi 1 + a, the raw centred Gram, after division by 1-rho, is

```text
v1 v1' + v2 v2' + W.
```

The noise/design cross-products are proportional to ||e|| v1. Sherman–Morrison gives RSS_T = ||e||^2/(1+q_T), with q_T = v1_T'(W_T+v2_T v2_T')^(-1)v1_T, for T containing all truths. Standardising columns does not change their spans. At W=NI and a=0, the signed Schur statistic gives exactly the displayed reference-centre identity, with kappa=N/(ell^2 phi^2), varrho=N eta/(ell phi^2). The corresponding inverse/signed-statistic formulas, rather than an independence claim conditional on X, are the useful valid starting point.

## Assessment of the remaining claims

X1 under FS looks plausible. Uniform fixed-size sample partial-covariance concentration gives the nonzero population pairs a fixed positive margin; for zero pairs, the signal projection is exactly zero and conditional-on-X Gaussian estimates apply to the realised block. Fixed raw coefficients require an explicit sample-sd event when applying fixed-design posterior results to random theta-star. This is available with probability tending to one.

X2's pure-deletion path and strict swap comparison remain plausible as goals, but the stated width and PLAN's shortcut do not yet have a viable proof. A minimum spacing bound for the top O(log log n) extremes can make a polynomially vanishing band empty with high probability; however it only helps after one has proved that the retained points are precisely in that extreme family. Spacing alone does not supply the missing balance or extreme-set membership.

X3 and X4 plausibly follow once discovery is proved: on an appropriate design event, sample sds are bounded above and below, signal energy is O(n), minimum signal is bounded away from zero, and sample Gram minimum eigenvalues have a common positive lower bound. For this regime a full operator bound from the entrywise correlation error already tends to zero. FAC-A L5.1's every-sequence argument then supplies the posterior integration step, and FAC-B L5's operational/delivery arguments can be reused with their recorded premises. This does not transfer the unproved discovery step automatically.

## Optional suggestions

1. Keep the Wishart representation as the first separately checked lemma. Its validity is independent of the soft-gap failure and is useful beyond this target.
2. Split the future path proof into an initial dense region with an explicit Gaussian occupancy invariant, a balanced bulk phase, and a controlled extreme phase. Identify precisely which set families each perturbation estimate covers, including swap intermediates.
3. Distinguish PLAN lemma labels X1–X6 from STATEMENT claim labels X1–X4 in review references, and use a separate symbol for perturbation beta_n versus the raw regression coefficient beta.
4. Retain the simulator self-test as evidence for the scorer and law implementation only. Its recorded agreement does not validate the new soft-gap invariant or family-wide no-addition bound.
