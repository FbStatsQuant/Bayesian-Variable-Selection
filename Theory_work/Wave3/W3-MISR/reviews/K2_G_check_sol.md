# K2 — blind line check of G_corollaries.md

Scope: the brief's permitted inputs only; R_reduction.md and M_misr.md taken as given. The only other review content inspected was L01_statement_lock_sol.md finding 1, for the example. No inherited POST2 or C-MIS proof was re-audited.

## Per-item verdicts

| Item | Verdict |
|---|---|
| Corollary G(a) | VERIFIED |
| Corollary G(b) | VERIFIED-WITH-AMENDMENTS |
| Corollary H(a) | VERIFIED |
| Corollary H(b) | VERIFIED |
| Reference law | VERIFIED |
| Remark SNR | VERIFIED |
| Remark P: MIS(i) | VERIFIED |
| Remark P: MIS(ii), (ii′) | VERIFIED |
| Remark P: Theorem F, F(a), F(b) | VERIFIED |
| Remark P: example | VERIFIED |
| Remark U | VERIFIED |

## Findings

1. **MINOR — G(b)'s status omits its declared A0 dependency.**

   Evidence: `Theory_work/Wave3/W3-MISR/lemmas/G_corollaries.md:3-4` makes G(b) conditional only on POST2:C. Its construction of the envelope uses POST2 Lemma A0 at `G_corollaries.md:29-30,35-36`. This is an additional input, expressly identified with the same inherited status as the POST2 rows at `Theory_work/Wave3/W3-MISR/STATEMENT.md:222`; the bridge and its constants are stated at `Theory_work/Wave3/W3-POST2/lemmas/A_occam.md:14-15,25-27`.

   Required change: make the G(b) status conditional on POST2:A0 as well as POST2:C. The proof already names the bridge; no change to the mathematical conclusion is required. H's declared D/C dependencies and U's C dependency match their uses. SNR and P expressly retain the statuses of the claims transferred.

2. **MINOR — Step 2 conflates the raw sparse-eigenvalue event with the standardised conclusion requiring step 1.**

   Evidence: `Theory_work/Wave3/W3-MISR/lemmas/G_corollaries.md:34-35` attributes probability at least `1 − 2k_n n^{-2}` directly to the bounds on the standardised Gram matrices. The cited argument at `Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md:94-99` obtains that failure bound for the raw matrices W_T and then explicitly uses event (1), the SD bounds, to obtain the standardised bounds. The SD event has its own failure allowance `2n^{-2}` at G lines 32-33. The cited derivation does not establish the displayed standalone probability for the standardised event as written.

   Required change: define step 2's event as `lambda_min(W_T^T W_T) >= c_pop N/2` for every nonempty T of size at most `min(p_C,k_n)`, with failure probability at most `2k_n n^{-2}`; say that **on its intersection with step 1**, standardisation gives `lambda_min(Rhat_T) >= c_pop/(4C_0) >= phi_0^2`. Define A_n using these raw, SD and energy events. This yields exactly the final union bound at G line 45, without another probability term. No stronger population assumption is needed.

## Checks against the seven questions

### G.1 and Corollary G(a)

At a single n the Gaussian residual decomposition at `G_corollaries.md:16-21` uses only the Gaussian block-conditioning identity in `C-MIS/lemmas/L2_gaussian.md:40-45`. The Schur complement may be singular and sigma squared may be zero. The sum xi + epsilon is independent of the entire candidate design and has covariance vI whenever v = sigma_C squared is positive. U is deterministic, so multiplication by U transpose and division by the deterministic positive square root of v give precisely the independent standard N-dimensional Gaussian required by GR^c. Dependence of the deterministic parameters on n introduces no further condition.

Positive candidate marginal variances imply that each of the finitely many columns is nonconstant almost surely for n >= 2. On that probability-one event the configuration is measurable in the stated Borel configuration space (`MISR/STATEMENT.md:27-31`). An arbitrary fixed valid configuration can be assigned on the null complement if a configuration-valued random variable everywhere is desired. Positive v also implies a nonconstant response almost surely. The final centred-row support identification in statement line 168 follows from the expressly permitted input Proposition P(b), `C-MIS/lemmas/L2_gaussian.md:21-25,45-46`; it requires no variance fixed across n.

### G.2 and Corollary G(b)

The contrasts remove m exactly: W has independent N(0,Sigma_CC) rows (`L2_gaussian.md:88-90`). Steps 1, 2 and 5 involve only the design and support. With finding 2's event formulation, the union bound is the one at `L2_gaussian.md:91-105`.

For energy, q = beta_C^T Sigma_CC beta_C is positive because s >= 1 and Sigma_CC is positive definite. Thus norm(W beta_C)^2/q is chi-square_N. The bound chi-square_N <= 2N with failure <= 1/n holds eventually, by taking x = log n in the cited chi-square inequality (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex:154-157`). Consequently energy <= 2NM_0 v <= n(2M_0+1)v. Step 4 gives the relative beta-min bound for any fixed c eventually, with an onset depending on the deterministic BM sequence.

All class conditions are accounted for: s(kappa_n)=s; nonconstant columns; positive v; SZ since p_C>=s by the definition of support and n>=2s; E^sigma; F_0; F_lambda; BM^sigma; and both OS inequalities after the A0 onset. The constants phi_0 squared = c_pop/(8C_0), M=2M_0+1, g_0=1 and c_D=1/2 are admissible. In particular c_pop<=C_0 follows from singleton subsets, so phi_0<=1. The raw eigenvalue argument only ranges over existing subsets, with size <=min(p_C,k_n); it does not need k_n<=p_C. Since k_n=O(log n), it is also <=N eventually. Nonzero beta_C and p_C>=s are consequences, not missing assumptions.

Include the MIS-R theorem's n_0 in the eventual starting threshold when applying it. Then A_n is design-measurable and has complement O(1/n). MIS-R(ii)(a), `M_misr.md:132-143`, supplies E delta_n <= Cr_n + P(A_n complement) and the corresponding HPM bound; O(1/n)=O(r_n). The hypotheses of statement section 5(b) suffice.

### G.3: H(a), H(b), reference law

The unit-noise array has exactly R1, E, F_0 and OS (`R_reduction.md:93-108`; `W3-POST/STATEMENT.md:63-64`). POST2:D(b), `W3-POST2/STATEMENT.md:112-116`, supplies C_H(s,A,1) and C_H prime = 1+C_H/4. The map T is a bijection on the disjoint union of parameter spaces, and divides squared mean error by v_n and posterior variance by v_n. Thus the displayed bad sets and posterior masses correspond exactly (`G_corollaries.md:58-64`). R′(b) explicitly covers the parameter posterior, not merely model probabilities (`R_reduction.md:67-71`).

The normal Hellinger formula (`W3-POST2/lemmas/D_hellinger.md:12`) is invariant under this simultaneous positive scaling. Both the squared-distance threshold of H(b) and H(a)'s unsquared threshold are unchanged. For H(a), MIS-R(i) gives E delta_n=O(r_n), hence delta_n tends to zero in probability also under the unit-noise law by the posterior-law identity. This is precisely D(a)'s additional hypothesis (`W3-POST2/STATEMENT.md:107-111`). Its four-part bad set pulls back to the four events at G lines 71-72; the coefficient threshold is M_n sqrt(v_n/n), using zero-padding to the same R^p. No uniformity in an unnormalised variance is being requested from D.

For the reference paragraph, GR supplies the conditional law given the entire candidate design (`C-MIS/STATEMENT.md:54-58`). Subtraction of the sample average of the conditional mean leaves marginal mean Cx beta_C and variance v. Actual centring of the response instead yields covariance vC and marginal variance v(1-1/n). Under Corollary G, integrating the omitted Gaussian covariates out gives the product conditional law with the stated linear mean and positive scalar variance; it belongs to the proposed conditional Gaussian family, so its KL divergence to itself is zero. This interpretation is limited to that conditional experiment. It is not a KL claim conditional on the realised omitted columns, consistently with `C-MIS/lemmas/L1_reduction.md:69-74` and statement section 6.

### G.4: Remark SNR

For Theorem 1 items 1-5, A1, C and E, the conclusions depend on model-space probabilities, the unchanged target support, and relative inclusion/margin sets. Size masses and the supremum over bounded functionals in Theorem 1 item 4 are included in that argument. Item 5(c)'s size cutoff and normalisation are design/prior objects, hence unchanged. The deterministic PIP inequalities hold under either parametrisation. Scaling E by the noise variance, BM by its existing variance denominator, and ID/ID^M by their variance factors gives exactly the unit-noise hypotheses (`W3-POST/STATEMENT.md:67-100`; `W3-POST2/STATEMENT.md:54-55,85-94,128-133`).

For random-design clauses, the conditional Gaussian assumption in G lines 92-94 is essential and is stated there. Normalised noise has constant conditional standard-normal law given (X,theta*), hence is independent of that pair and of the smaller pair (X,theta*/sigma*). Support and the measurable envelope events are preserved by a positive scale; if necessary the diagonal argument can be indexed by the original pair, since each realised scaled pair has the same fixed constants. A common OS onset is retained. A marginal Gaussian assumption without that conditional assumption would not suffice, but is not what this proof uses.

For B, `W3-POST2/lemmas/B_tail_approx.md:7-14` allows an arbitrary mean and a deterministic reference. Scaling the mean and reference divides the entire reference cost by t^2. D_T, R_m^T and A_m^T are unchanged, so Theta double-prime is unchanged, including its zero-normaliser convention. The required original-unit cost is B_T(vartheta)<=Bt^2. Evaluate c-sharp and the displayed bound at variance one. The overloading of t for the noise SD and reference size in the cited notation does not affect this calculation. For D the parameter transformation and thresholds are those already checked in G.3; its random-design version uses the same conditioning argument. The list in statement section 7 is covered.

### G.5: Remark P

**MIS(i).** C-MIS permits tau^2=0 and xi=0 (`C-MIS/STATEMENT.md:55`; `C-MIS/lemmas/L1_reduction.md:38-39`). The synthetic problem at G lines 104-108 has fixed positive noise variance one, deterministic candidate coefficient beta_C/t and zero omitted contribution; beta_C/t may vary along the deterministic array. Only the aggregate candidate coefficient, mean and variance enter H-MIS. A zero omitted contribution is permitted: if the formal full-model convention S_0 not contained in C must be retained, append an omitted raw zero column with nonzero coefficient. No condition is imposed on omitted columns forbidding this. The original proxy/cancellation consequences follow from the resulting candidate PIP and wrong-model bounds with the original support labels; they do not require preservation of the synthetic full-model labels. Both BM alternatives and J_n are mapped relative to the aggregate variance.

**MIS(ii), (ii′).** The synthetic full-model candidate coefficient is fixed at zero; its omitted contribution and GR coefficients are measurable functions of the candidate design, as allowed by `C-MIS/STATEMENT.md:54-55` and `L1_reduction.md:92-103,122-123`. For example it can be realised by one omitted raw column equal to the specified omega with fixed coefficient one. The ordinary noise is now independent standard Gaussian, xi=0 and tau^2=0. The effective slope gamma(x)=beta_C(x)/sigma_C(x), not the full-model zero coefficient, determines the target support. The original envelope sets satisfy the same finite-n bounds and BM(c) or common deterministic BM-infinity envelope after scaling. Dropping BM gives precisely (ii′). No design-dependent ordinary-noise variance is passed to the old theorem.

**Theorem F and its corollaries.** The scaled contrast experiment has deterministic mean mu_c/t, deterministic EP coefficient theta_C/t and residual r/t, with fixed Gaussian variance one. EP orthogonality and support are unchanged. The energy hypothesis gives Delta_n/t^2<=2M, and therefore aggregate variance divided by t^2 lies in [1,1+2M]. All table rows at G lines 122-130 match `C-MIS/STATEMENT.md:124-141` and `C-MIS/lemmas/L4_theoremF.md:17-20,117-121,150-161,193-194`: floors, sizes and cutoffs are design/prior quantities; BM-infinity must contain sigma_n^2 in its denominator; BM(c) and J_n use sigma_n^2+Delta_n; TAIL is on the invariant posterior; TL is the unchanged dimensionless ratio. F(a)'s eventual equality m-sharp=K persists; F(b)'s m_n^T and final cutoff persist because their constants depend on kappa,s,A. No variance-dependent hypothesis is omitted from the table.

**Example.** The allowed source finding 1 is at `MISR/reviews/L01_statement_lock_sol.md:7-13`. For n large choose two orthogonal centred columns of norm sqrt(N), phi_0=1 and m_n=K=2. With theta=(1,0), r=0, variance n^2, the original BM-infinity expression diverges, energy in noise units and the floors hold, and TAIL is zero. The scaled mean has squared norm N/n^2. More explicitly KL(N(mu_c/n,I),N(0,I))=N/(2n^2), so total variation is at most sqrt(N)/(2n), tending to zero. `C-MIS/lemmas/L6_null.md:6-12` permits r=0, fixed unit variance and bounded p with a fixed positive Gram floor; thus the pure-noise posterior has mass tending to one on the empty model. Apply the TV bound to the measurable events {pi(empty)<1-epsilon}, then use pi({1})<=1-pi(empty) and response-scale invariance. This proves the example's claimed failure; no extension of Lemma Z to changing variance is used.

### G.6 and coverage

For U, the hypotheses mean that the same response law satisfies GR^c at both configurations. MIS-R(i) applies separately with each class's admissible constants and margin threshold. Taking the maxima of the two n_0 and C values gives both lower bounds on expected target mass under that same law. Distinct models have masses summing to at most one pointwise, contradicting two expectations greater than one half. Coefficient uniqueness is neither used nor asserted.

Statement sections 5-7 are covered by these transfers, including the centred-row support identification supplied by Proposition P(b), all four H(a) events, both Hellinger clauses, the restricted reference-law interpretation, and both F corollaries. The amendments above concern an event/probability presentation and dependency bookkeeping; no additional mathematical hypothesis or weaker conclusion is required.

Finding counts: **FATAL 0; MAJOR 0; MINOR 2; NIT 0.**
