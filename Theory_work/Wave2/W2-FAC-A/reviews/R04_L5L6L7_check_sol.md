L5.0 / Proposition L5.1: VERIFIED-WITH-AMENDMENTS.
Lemma κ: VERIFIED-WITH-AMENDMENTS.
Instances (I)(a)–(b), GC-CS ⇒ TV: VERIFIED-WITH-AMENDMENTS.
Lemma P5: VERIFIED.
S5 TV certificate / instances (I)(c)–(d): VERIFIED-WITH-AMENDMENTS.
L6 / Proposition SHARP: VERIFIED-WITH-AMENDMENTS.
L7 / Proposition F-FAC: VERIFIED-WITH-AMENDMENTS.

Review scope: checked the specified statements, source arguments and numerical code. No FATAL finding or counterexample to the principal conclusions. One MAJOR proof defect occurs in the definition of the CS signal minimum for bounded p; it has a direct repair. The S5 floating-point certificate is independently strengthened below to exact rational minima. References below use file basenames within W2-FAC-A unless another path is supplied.

1. **MAJOR — L5_random_instances.md:67–73: GC-CS does not imply positivity of the enlarged minimum as defined.**

   The displayed minimum ranges over V ⊆ S₀\{j} and every u = |V|,…,15, including configurations requiring more null variables than exist. GC-CS quantifies over actual U ⊆ [p]\{j}. These conditions differ for bounded p, which the locked statement allows. Also, the minimum must be of absolute values, not signed expressions.

   Concrete counterexample to the claimed implication: take p = s₀ = 2, a = 1/2 and θ* = (1,−3), fixed as n grows. The actual GC-CS expressions are −1 and 3/2 for j = 1, and −5 and −9/2 for j = 2, so GC-CS holds. But the enlarged list includes j = 1, V = ∅, u = 1, whose expression is 1 + (1/2)(−2)/(1/2+1/2) = 0. There is no null coordinate with which to realize this U. Thus even interpreting g₀ as a minimum of absolute values, the asserted g₀ > 0 is false.

   **Exact fix:** take the minimum of absolute values over configurations realized at some n in the sequence. At a given n, feasibility means |V| ≤ u ≤ min(15, |V| + p_n − s₀). The union over n is still a subset of one fixed finite list because s₀ and the coefficients are fixed. GC-CS makes every member of that realized list nonzero, so its absolute minimum is positive. Use this corrected constant in both (I)(a) and (I)(b). Alternatively, explicitly strengthen GC-CS to the enlarged list, but that unnecessarily excludes valid bounded-p instances. The existing cert_cs routine computes the enlarged, conservative minimum; a positive answer remains sufficient, while a zero answer need not refute the actual GC-CS condition at small p.

2. **MINOR — L5_random_instances.md:54–55: the equality λ_min(Ψ) = d has a singleton exception.**

   If all groups are singletons, H = I and Ψ = (b+d)I, so λ_min(Ψ) = b+d, not d. If at least one group has size at least two, the equality with d is correct. This affects neither admissibility nor κ.

   **Exact fix:** write λ_min(Ψ) ≥ d > 0, with equality whenever a group has at least two members. The separate CS representation Ψ = (1−a)I is valid. All substantive closed forms check:

   λ̃ = √ρ_b d/(d+ub),
   ψ = d[d+(u+1)b]/(d+ub),
   c_min = ρ_b/(d+b),
   λ̃²/(ψ c_min) = d(d+b)/[(d+ub)(d+(u+1)b)].

   The final ratio is at most one and attains one at u = 0, proving κ = 1 and α₀ = 1/6.

3. **MINOR — L5.0:8–14, through L3_NA_TL.md §L3.0: the literal “as written” uniformity claim inherits an impossible feasibility assertion.**

   L3.0 says “p + 1 ≤ K (true eventually …)”. Since K = min(p, floor(n/2)), this is never true. This is a local typo, not a failure of the event proof: the proof only needs feasible sets of size at most p, including additions to T with |T| ≤ p−1.

   **Exact fix:** replace that assertion by “K = p eventually; every subset A ⊆ [p] is feasible.” Then (0.1) follows with genuinely common envelopes. In particular, Corollary U uses κ′_bd ≤ κ̄/√ψ₀, so its varying representation parameter c_min introduces no hidden design dependence. The block-family cardinality is bounded uniformly by 2^16 p, and L3's deterministic score thresholds depend on the listed constants and envelopes. L4 introduces no additional stochastic bound. There is no need for uniformity over unrestricted designs or over sequences lacking common envelopes.

4. **MINOR — L5_random_instances.md:91–111 and tv_cert.py: replace the floating-point positivity assertion by an exact certificate.**

   The combinatorial reduction is correct for the three stated layouts: each group contains at most one truth. The code includes zero, one and two other groups; the two-group cases exhaust two truth groups, one truth plus one null group, and two distinct null groups. In another truth group it includes both truth-exclusion and truth-inclusion, together with every possible number of its four null coordinates. In the target's own group, mates[:m0] covers the five cardinalities 0,…,4 because all four mates are null and exchangeable. A null group contributes cardinalities 0,…,5. The two representative null groups are distinct. These choices therefore cover every required orbit, with harmless duplicates when a chosen group contributes no variables to U. No configuration is lost by the len(U) > 15 filter: the largest block has 15 members, so actually |U| ≤ 14.

   However, numpy.linalg.solve and six printed decimals alone are not an exact positivity certificate. This is repaired by the independent rational calculation below, which gives the exact minima 2023/32500 for the diagnostic layout and 7/2080 for each study layout. Thus this finding is closed mathematically by this review; it does not leave the S5 instance open.

   **Exact fix:** record those fractions and the following rational enumeration formula, or add a rational/validated-interval certificate implementing it. Let u_g = |U ∩ g|, Θ_g^rem = Σ_{i∈g\U}θ_i, d = 3/10, b = 4/10, r = 3/10, w_g = d/(d+b u_g), and s = Σ_g r u_g/(d+b u_g). For j ∉ U in group h,

   Σ_{jμ|U} = d θ_j + b w_h Θ_h^rem + r w_h [Σ_g w_g Θ_g^rem]/(1+s),
   Σ_{jj|U} = d + b w_h + r w_h²/(1+s).

   Every quantity is rational for the specified coefficients. Unselected groups have u_g = 0 and w_g = 1: their truths remain in the signal sum. Additional all-null groups contribute zero, explaining exactly why their number is irrelevant. Use τ₀ = c²·2023/32500 or c²·7/2080 as appropriate. The two study spacings are equivalent by group and within-group permutations.

5. **MINOR — L6_sharp.md:30–40: make the small-model extension and the high-probability score event explicit.**

   The central argument is correct even for p comparable to n, but L3's surrounding hypotheses include (P), which is deliberately violated here. Only its deterministic identities (E1) and (E2) transfer. Their proofs use the Gram floor on the particular scored sets; they do not require p = o(n), K = p, or L3's lower RSS bound. The latter lower bound must not be imported when p is comparable to n.

   There are three minor omissions in the written inequality chain. First, replacing the denominator by an upper bound requires the lower numerator σ²Z²/s_Y² − 2 to be nonnegative; this holds eventually on the witness event because Z² → ∞ and s_Y² is bounded. Second, the sharp noise-norm upper bound displayed at line 34 is an additional Laurent–Massart event; it is not the upper bound defining L3's E_Y. Third, (6−o(1))log p − log n is not literally bounded below by ε log n − O(1) merely from 6 log p ≥ (1+ε)log n.

   **Exact fix:** state that (E1),(E2) are reused by their algebraic proofs on T,A; intersect the witness event with E_Y and the additional event
   ‖Cε‖²/σ² ≤ n−1+2√((n−1)log n)+2log n,
   whose complement has probability at most 1/n; note numerator positivity before changing denominators. Choose a strict margin 6 log p ≥ (1+2ε)log n, and then absorb the o(log p) term to obtain ε log n − O(1). Since p ≤ n−1, o(log p) = o(log n). These changes justify the displayed conclusion without any full-model RSS lower bound.

   The determinant sign is correct: −2(ρ_A−ρ_T) ≥ 2ρ_T ≥ −k/[(n−1)(1−a)]. The prior lower bound is correct. The upper bound RSS_T ≤ ‖Cε‖²/s_Y² holds pointwise for the data-selected T because T contains S₀. Thus selecting T from the noise introduces no union-bound or conditioning problem.

6. **MINOR — L7_delivery.md:6–11,32–35: allocation shorthand should retain the precise A1/A4 inequalities.**

   The text says “mem_n, time_n ≥ the A1 envelopes W_G, M_G plus the A4 preflight terms”. Taken literally, this suppresses MACH conversion constants, the maxima with preflight bounds, and the correct pairing of memory with M_G and time with W_G. The opening reference to exactly FINAL Proposition F's allocation repairs the intended meaning, so I do not find a missing substantive premise.

   **Exact fix:** replace the shorthand by “the complete allocation inequalities of FINAL s6 Proposition F, including MACH conversion constants, original preflight/certificate bounds, and A4's P_e + A and P̄_LS0 bounds, evaluated at (n,p_raw).” As in A3's amendment, explicitly replace the old LS0 score count by ≤ 1+(ℓ_n+K+1)q(p), increasing the total by Kq(p). No enlargement beyond the already amended W_G,M_G and A4 allocation is needed for factor designs.

7. **MINOR — fna_check.py, draw(): the large-df simulation is approximate despite the “draw z exactly” description.**

   For n−1−p ≥ 10^9, the code replaces the independent χ²_{n−1−p} variate by its normal approximation. This changes the joint response normalization and hence z. The exact algebraic add-gain identity is correct, but the large-n generated data are not exactly distributed as claimed. Also, absence of failures among the scanned one-sided/random sets does not establish NA over the full lattice.

   **Exact fix:** label the large-df branch as approximate, or use rng.chisquare for it as well. Describe a positive scanned gain as a certified witness of NA failure and a nonpositive scanned maximum as “no witness found”. This numerical issue does not affect L6's analytic proof.

Further checked arguments:

The L5.1 design bound is sufficient: with δ′_n = O(√(log n/n)) and p ≤ n^α₁, α₁ < 1/6,
δ_n√(p log log n) = O(n^{3α₁/2−1/2}√(log n log log n)) → 0.
The crude Frobenius bound pδ′_n is valid; no independence among correlations is needed. The energy inequality is valid and can be simplified to ‖μ‖² ≤ (n−1)s₀‖θ*‖² directly from the unit diagonal and positive semidefiniteness.

The partial-signal map in L5.1 is the correct standardized add-direction signal even when U overlaps S₀. On the fixed-size correlation submatrices and their line segments, the common eigenvalue floor bounds inverse matrices and keeps the Schur denominator away from zero. The Lipschitz constant is uniform over all labels and blocks. In particular, an error ≤ (1−1/√2)√τ₀ implies f(R̂_V)² ≥ τ₀/2; this establishes the stated deterministic TV envelope. The posterior diagonal argument is valid: a nonvanishing supremum of conditional expectations supplies a deterministic subsequence, extendible to a design sequence in the good sets; T03♯ then gives convergence in probability, and boundedness by one gives convergence of expectations. It does not infer an expectation rate from O_P.

The CS partial covariance at L5:65 is correct, and Σ_{jj|U} = (1−a)[1+a/(1−a+au)] lies in (0,1]. Once finding 1 is repaired, |U| ≤ 15 suffices for every block of size at most 16, regardless of how it was formed.

P5's complete-linkage induction is correct. While any group is unfinished, a within-group pair of current clusters has distance < 1/2 and every cross-group pair has distance > 1/2. Consequently all groups become subtrees before the first cross-group merge. A top-down cut only visits a proper descendant of a group node if that group node is split, which cannot happen at B ≥ 5. Whole-cluster next-fit packing cannot split a group. Ties inside either distance class do not affect this conclusion; a tie across the classes is excluded by the strict margin. No divisibility of B by five is needed: block sizes remain multiples of five and at most 5 floor(B/5). Thus B = 6,…,9 permits only one group, B = 11,…,14 at most two, and B = 16 at most three. I checked the actual top-down/packing rules in Scripts/SMC_BVS/core/cpp/v3_blocks.h:121–140 as well as FINAL s1. The general fixed-size block-CS margin argument transfers as stated once B ≥ g.

For L6, substitution into L1 (1.1) gives exactly
Z_{T,l} = [η_l − H_T/(k+c) + √c ξ₀/(k+c)]/√[1+1/(k+c)].
Both order-statistics bounds hold: Mills' ratio gives expected exceedance count of order log N′ at the minimum threshold and of order m log(N′/m) at the m-th-largest threshold. The latter divided by m tends to infinity, so the binomial lower-tail probability vanishes. The fixed number of truth-coordinate noises and the common-factor noise are negligible. This yields Z² ≥ (8−o(1))log p, and the repaired score bound yields 2ΔF ≥ (6−o(1))log p−log n−O(1). The selected sets have size O(log p) < K eventually even when p = n−1. Their ordering is also original-space measurable because g_j = √a ξ₀ + √(1−a)η_j preserves coordinate ranks. L6 drops the locked statement's extra p ≤ K restriction; this is a valid stronger conclusion by the same small-model proof, but should be recorded as a scope strengthening.

L7's A2 transfer is valid under the expressly inherited ideal-machine, fallback and allocation premises. Nonconstant Gaussian columns and a nonzero centred response hold almost surely at each finite n,p; conditional nondegeneracy of Cε is the correct argument for the standardized-scale random-design generator. Positive definite ridge matrices and Q_S ≥ (n−1)/(n+1) exclude scorer failure without full-design rank. Neither the allocation argument nor the finite-n delivery assertion requires the asymptotic design event. The event 𝒦_n, rather than D_n, is used in the correct direction, and the scored-set implication on output is exactly D′'s pathwise argument. CAL and successful calibration need not be assumed. The explicit P1/S.3 audit and operational-premise qualifications must remain; this is not an unconditional reliability claim about an ordinary finite-precision execution.

Numerical checks actually run:

- All Python commands ran with py -3.13 -B from the Windows temporary directory, using in-memory scripts. No numerical source/output file in the repository was modified.
- Independent Fraction enumeration, using the rational block formula above: 11,060 configurations for s₀ = 4 gave min τ = 2023/32500 = 0.06224615384615385. The minimizing target has coefficient −1 and U consists of a truth with coefficient −1.2 in another group.
- Independent Fraction enumeration: 612,710 configurations for s₀ = 14 gave min τ = 7/2080 = 0.0033653846153846156. A minimizing target has coefficient −1 and U consists of the two truths with coefficient −1.6 in distinct other groups. Both step-7 and step-13 layouts have exactly this group/coefficients configuration and identical minima.
- Checked the independent block partial-covariance and partial-variance formulas against direct covariance-matrix solves for 100 random conditioning configurations: maximum absolute discrepancy 2.78×10^−16.
- Executed kappa.py's algebraic enumeration in memory: all four CS cases and all four block-CS cases reproduce κ = 1 and α₀ = 0.16667, with c_min matching the closed form.
- Compared L6's witness innovation formula against direct Gaussian innovation solves at a = 0.1, 0.3, 0.7, 0.9: maximum absolute discrepancy 4.22×10^−15.
- Checked the bounded-p GC-CS counterexample with exact fractions: actual expressions −1, 3/2, −5, −9/2; the infeasible enlarged-list expression is exactly zero.
- Inspected tv_cert.py, fna_check.py and their saved summaries. I did not rerun the full FNA Monte Carlo grid or claim its finite simulations prove the asymptotic threshold.
