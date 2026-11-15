MANIFEST 960c9069b362a251403f6aed9cd804c96870fd63775a72ebf307588b45a10730
Verdict: CONTINUE WITH CHANGES

The key lemma stands. I found no FATAL or MAJOR mathematical gap in L0–L3 or in (C1), read with its explicitly conditional posterior input in STATEMENT §5. Proceed with the remaining proofs. The required changes below correct supporting records; they do not require strengthening (C1)'s assumptions or changing L2's argument.

All paths below are relative to Theory_work/Wave3/W3-RM2 unless another root is given. I verified all 52 file hashes in the manifest: zero mismatches. This was a blind review of the allowed inputs; no earlier review report was read.

Findings

1. MINOR — ASSUMPTION_MAP.md:25. The assertion that the sample Gram floor “holds for Gaussian rows iff b < ½-type” is false as a necessity assertion. The entrywise-to-operator-norm argument supplies a sufficient bound q sqrt(log n/n) -> 0; it does not establish an obstruction at b = 1/2. For example, iid Gaussian columns with polynomially many Q-plus-one sets retain their sample floors for q = n^b, b < 1, by rectangular Gaussian singular-value bounds. Exact correction: replace “holds ... iff” by “is supplied here by the sufficient entrywise bound q sqrt(log n/n) -> 0 (in particular b < 1/2); necessity is not asserted.” STATEMENT P8 itself is correctly phrased.

2. MINOR — PLAN.md:12,15,45–46 and ASSUMPTION_MAP.md:31,52. Some supporting prose exceeds the proved route statement: “survives iff”, “exact complexity condition”, “route cannot do with less”, and the unqualified “Not necessary for the conclusion” are stronger than the divergence dichotomy and finite-n observations. W-conv rules out positive diverging gaps for high-probability whole-lattice NA; it does not prove that negative divergence is necessary, nor establish an asymptotic reported-model counterexample to necessity. Exact correction: describe beta(eta,A)-b as the positive margin of this proof, and W as a sufficient negative-gap condition with a positive-gap obstruction and an unresolved bounded-gap regime. Describe B2 as finite-n LS0 success despite observed NA violations, not as a proof that W is unnecessary for asymptotic reporting. STATEMENT.md:279–293 and L2_width.md:114–117 already have the appropriate qualifications; use them consistently in the supporting records.

3. MINOR — ASSUMPTION_MAP.md:9,27,46–54,56. The numerical record is stale: the available RESULTS.md:99–106 records 208 runs, 204 successes, and four failures out of six in the eta=1, n=1600 cell, rather than 207/204 and three out of five. No n=3200 run finished. Moreover “Inside every assumption” is stronger than the numerical certification: SPEC.md and RESULTS.md expressly call classifications nominal and do not certify the fixed-design hypotheses. Exact correction: update the counts and swap range (19–73 for failures), state that completed sizes were 400 and 1600, and replace “Inside every assumption” by “Nominal baseline cells B1 at b <= 0.375.” Keep the LS0-only scope. The statement's limits remark already agrees with the addendum.

4. NIT — lemmas/L3_assemblyF.md:19–20. “Bounded convergence” is imprecise when the input is convergence in probability. The conclusion is correct. Replace it by the explicit bound E[1-pi(S0)] <= epsilon + P(1-pi(S0)>epsilon), followed by n -> infinity and epsilon -> 0, or say boundedness gives uniform integrability. No stronger posterior input is required.

Independent derivations

1. Toolkit and actual lattice cost (L0).
   For each A, RSS_A = Lambda_A + 2<r_A,epsilon> + ||C epsilon||^2 - ||P_A epsilon||^2. Completing the square in sqrt(Lambda_A) loses only sigma^2 h_n^2. The chi-square projection bound at t_n=4(log|F|+2 log n+J_n) has union failure at most n^-2; the linear Gaussian union has failure at most 2/n. This gives the stated RSS floor and omega_n.
   The lattice family includes additions even when their size is K+1, as auxiliary regression objects. They are contained in Q union {l}; FL-Q supplies the inverse and the toolkit is not restricted to feasible models. Thus the swaps at the cap do not introduce an undefined regression. Its log cardinality and vector-family log cardinality are O(q+log n), so q log n/n -> 0 is sufficient for omega_n log n and vartheta_n log n to vanish.
   Diagonalising G_A gives log D_A = |A|log(n+1)+eta_A with |eta_A| <= 2|A|/((n-1)phi0^2). The ridge correction to RSS in standardised response units is at most 1.01, and the added 0.02 gives at most 1.03. Multiplication by nu/RSS^y is bounded. The uniform constant remainder therefore remains valid at polynomial q; there is no hidden O(q) remainder in the score increment. The upper likelihood ratio uses the RSS of the larger model in its denominator; the lower bound for a truth-containing model uses RSS_T <= sigma^2 n(1+4n^-1/3). Both directions are correct.

2. NA-conv (L2:54–64).
   Put a^2=log(n+1)+2 log(p/(k+1)). The prior is at most (k+1)/p. On Z_n, the nested RSS reduction is sigma^2 Z^2 with Z^2 <= a^2-4 kappa_E-2 = O(log n). Uniformly, x <= 4(A+1)log n/n, and the error in replacing the likelihood gain by Z^2/2 is at most
   (A+1)log n [vartheta_n+2x+2x vartheta_n] = o(1).
   Taking it <=1/2 yields the exact cancellation
   -a^2/2 + (a^2-4 kappa_E-2)/2 + 1/2 + 2 kappa_E = -1/2.
   All feasible additions are covered on one toolkit event; the threshold depends on k as required, not merely on q.

3. NA-W and the rate (L2:66–86).
   Phi(g)=max_pairs(|u'g|-a) is 1-Lipschitz for the Euclidean metric. With E Phi=-s<0, concentration gives P(Phi>-s/2)<=exp(-s^2/8). No independence of directions is used. Also Phi(g)>=-a_min, hence s<=a_min<=a for every pair. On the complementary event,
   Z^2 <= (a-s/2)^2 = a^2-as+s^2/4 <= a^2-(3/4)as.
   Thus (3/4)s sqrt(log(n+1)) >= 4 kappa_E+2 implies Z_n. This verifies the factor 1/8 and the constant subtraction without an invalid squaring of a negative upper bound.
   The level difference is at least delta0 sqrt(log n)/(2 sqrt(2A+2)); squaring and dividing by 8 gives exactly c*=delta0^2/[32(2A+2)]. Under bare W the bound need not be polynomial, as the statement correctly says. The empty pair family is vacuous and should be read with exp(-infinity)=0; no concentration argument is needed there.

4. W-conv (L2:90–112).
   If E Phi=s>0, the lower-tail event Phi>=s/2 has failure at most exp(-s^2/8). At an attaining pair, Z^2 >= a^2+as. The lower prior bound contributes -a^2/2-log 2. Consequently the score increment is at least
   (as/2)(1-4n^-1/3)-2n^-1/3 a^2-log 2-2 kappa_E.
   For large n this is >=as/4-1-log 2-2 kappa_E, strictly positive when s sqrt(log(n+1))>=8 kappa_E+8. The selected addition is feasible by the definition of the pair family. This proves the claimed converse for NA, not a converse for reporting. The stated older converse follows by subtracting the squared levels and rationalising their difference.

5. Sufficient forms (L2 §3).
   W-unif -> W-delta: k+1<=n^b+1 costs at most 2b log n+2 log 2 in the squared threshold; the spare delta log n absorbs 2 log 2.
   W-ref -> W-unif: the expectation of the maximum frame projection is at most sqrt(m0)+sqrt(2 log|V|); atoms cost L sqrt(2 log(2|A|)); the remainder costs rho[sqrt(q+1)+sqrt(2 log p)]. The last two terms and the variance inflation are o(sqrt(log n)). With delta=(1-2b-2h)/4, the target leading square root exceeds sqrt(2 log p+2h log n) by at least delta sqrt(log n)/sqrt(2A+1). This absorbs every remainder.
   W-loc -> W-ref: writing B=T intersect N_l and lambda=beta_bar(T,l)-beta_bar(B,l), the exact residual is (I-P_B)x_l-X_Q lambda. Division by ||(I-P_T)x_l|| gives the reference line, coefficient budget L/phi0, and zero remainder. There are at most p 2^nu reference lines. Orthogonality of X_Q lambda to the T-residual gives the claimed variance-ratio bound 1+L^2/phi0^2.
   W-chi -> W-delta: the orthogonal decomposition against Q minus {l} yields (u'g)^2 <= (u_Ql'g)^2+||(P_Q-P_S0)g||^2. The expected squared maximum is bounded by 2 log p+O(log log n)+(1-delta1)log n. The minimum squared level is at least 2 log p+(1-delta0)log n-O(log log n). Every delta0<delta1 leaves positive slack. The case p=1 is vacuous. I also checked the Gaussian squared-maximum mgf calculation in Lemma 0.

6. Truth removal (L2:180–219).
   For A deleting truth i, or swapping it for l, B=A union {i} equals T or T union {l}. Since all other truths lie in A,
   u_Ai'Y = theta_i ||(I-P_A)x_i|| + sigma Z_Ai.
   Subtracting the two nested RSS identities gives exactly (4.1), with the addition square present only for swaps. The sign of theta_i causes no problem: |a+z|>=|a|-|z|.
   On B_n the truth-noise term is at most sqrt(2d_n^2+4 log n)=o(sqrt(lambda_n)). The positive square is at least sigma^2 lambda_n/4. Z_n^+ bounds the subtracted square by sigma^2(2A+2)log n<=sigma^2 lambda_n/8. Hence RSS_A-RSS_T>=sigma^2 lambda_n/8. The score penalty for a deletion is at most log(2p)+log(n+1)/2+2 kappa_E; a swap costs less. T4(b) converts the RSS gap into a dominating score decrease since lambda_n/log n -> infinity.
   Crucially, BM-W alone is not claimed to supply Z_n^+. W supplies Z_n, and at |T|=K the only possible lattice T is Q (q=K); at most p additional standard normals cost 2/n. This closes the cap endpoint and establishes the stated dependence on W. The width d_n is finite, deterministic for fixed X, and well-defined under FL-Q.

7. Sandwich, assembly, containment and uniformity.
   In L1, the chi-square block count and dyadic ladder use no independence between blocks. With epsilon1 chosen so A epsilon1+(1+1/epsilon1)eta/2<1/2, the ladder sum is geometric and its probability bound vanishes. It bounds every maximiser on a common event. Feasibility then permits adding any missing truth (or Q=[p] and a saturated maximiser already contains it). Visibility makes its score gain dominate O(log n). After truth inclusion, deleting junk has margin [beta(eta,A)-b]log n-o(log n). This establishes exactly SAND, including “every maximiser.”
   The parent RM-0 at Theory_work/Wave3/W3-RM/STATEMENT.md:160–176 and its L0_core proof require only deterministic Q, Q containing S0, q<=K, the interface events and implementation premises. No polylogarithmic restriction survives into that core. Independently, NA at C minus an extra makes that deletion improve F and makes every extra-removing swap inferior to its corresponding deletion; TL excludes truth removal. This proves the deletion-only path at arbitrary q. The pinned engine scans precisely these neighbours and tests strict improvement before the cap; the shipped cap exceeds the needed number of moves.
   POST plus boundedness supplies its expectation version. With G_n=K_n intersect {pi(S0)>1/2}, the reporting argument is pathwise on one data event; no union over seeds or calibration outcomes is required. The archive assertion is understood through the imported RM-0 convention: an actual LS0 archive on completed SMC runs, a hypothetical search on enumeration branches. It is not a claim about the final public certification flag.
   All n0 choices may depend on the fixed constants and the assumed rate sequences (visibility, q log n/n, BM-W and W); none depends on the maximiser or run. No uniform rate over arbitrary unboundedly slow sequences is proved or needed by C1.
   The registry records RM-0 and E4 as ACTIVE/PROVED-CHECKED, and records the weaker posterior/toolkit statuses as quoted in §5. The new toolkit is self-contained; its old unchecked source is not needed as a mathematical premise. C1 still remains conditional on SOP:TH09. Parent containment follows by choosing b<beta and, under N-D, b<1/2-h; N-chi supplies BM-W through d_n^2=O(log n), and N-D(ii) supplies it through BM-Q.

Assessment of the statement and remaining plan

W is a genuine deterministic geometric condition on (X,S0,Q), not an assumption about the realised noise or the selected path. It is close to the Gaussian crossing problem underlying this particular route, but its sufficient forms are independently checkable and do not repeat the reported-model conclusion. It is not vacuous at polynomial q.

A concrete natural fixed-design witness has p=floor(n/3), s0=1, q=floor(n^b) with 0<b<1/2, and centred orthonormal coordinates e_j. Set x1=sqrt(n-1)e1; for 2<=j<=q put x_j=sqrt(n-1)(r_n e1+sqrt(1-r_n^2)e_j), where r_n=sqrt(C log n/n); use orthogonal outside columns. Take Q={1,...,q} and a fixed nonzero truth coefficient of sufficiently small magnitude to meet the energy constant. The full Gram matrix tends to identity in operator norm because sqrt(q)r_n+q r_n^2 -> 0. Thus all required sparse and Q-plus-one floors hold. Outside columns have zero conditional gain for every conditioning subset, giving eta=0. Conditioning on at most 15 proxies leaves truth gain of order n, while each proxy has marginal signal gain of order log n: this is a genuine polynomial family of weak signal proxies, not just padding Q with independent nulls. Once truth 1 is conditioned on, every remaining proxy residual is its own e_j. W-loc holds exactly using N_l={1} for proxies and empty neighbourhoods outside, with L=0; take any small h>0 with h+b<1/2. BM-Q, hence BM-W, follows from fixed signal and q=o(n). L-feas holds eventually. This confirms compatibility of the actual C1 hypotheses. It does not substitute for the planned p>>n examples.

BM-W is well-posed and can be weaker than BM-Q. Its swap directions are essential. The statement honestly leaves necessity, bounded width gaps, delivery, binary64 behaviour and reported-model failure rates unclaimed. The limits remark agrees with the allowed RESULTS addendum and correctly separates LS0 probes from the full method. The finite-n probes do not certify the asymptotic assumptions, and the named equicorrelated example remains explicitly a candidate.

The remaining plan is sound, with P7 (Gaussian-row sandwich) the highest-risk step. An X-measurable selected block must not be treated as a fixed block while applying spherical tails. Re-run selection removal uniformly over all small conditioning sets via deterministic H_l references; track the n^(15rho) count and the full range of t in the spherical bound. The slower localisation calculation must retain
sqrt(n log n) r_n^2 + (log n)^(3/2)/sqrt(n) + n r_n^4 + (log n)^2/n = o(1).
The assumed r_n(n log n)^(1/4)->0 suffices. After counting references, the ladder needs 15rho<1/2; final junk exclusion needs the strictly stronger 15rho+b<1/2. Sample response standardisation must remain uniform in the fixed coefficient box, as in the parent proof. Merely citing the polylogarithmic theorem would not discharge this step.

P8 looks routine given explicit deterministic envelopes: q sqrt(log n/n)->0 supplies sample floors; bounded fixed-sparsity coefficients supply energy and lambda_n of order n; d_n^2=O(q+log n)=o(n) supplies BM-W; W-R supplies a deterministic diverging width margin. Conditional L0/L2 bounds can then be integrated without design-dependent uncontrolled n0.

P9 is the second point to spell out carefully. The NA-R population/sample comparison error becomes O((q+log n)/sqrt(n))=o(1). The reference/atom proof supplies a joint high-probability upper bound sqrt(2 log p)+o(sqrt(log n)). For any delta0<1-2b there is deterministic slack of order sqrt(log n) below the minimum a_(n,delta0). Convert joint crossing control to a high-probability conditional bound using Markov on the conditional failure probability, then Gaussian concentration (or median–mean control) for the conditional 1-Lipschitz maximum. A joint probability statement alone is not an expectation bound; the proposed median–mean step is sufficient when written with that slack. P10 must retain the recorded conditional status of its posterior input and the p=1 endpoint. Examples and sharpness remain separate proof obligations; the polynomial-decay budgets have room exactly as stated when alpha>17/2.

Not checked

- C2, C5 and C6 as finished theorems: their proofs are not yet written. The discussion above assesses feasibility and identifies obligations, not verification of absent proofs.
- The posterior concentration theorem underlying SOP:TH09, or the full implementation proof of E4. Their recorded contracts/statuses were checked and consumed; they were not independently reproved.
- An exhaustive audit of production score code, start-mode DP, all inherited engines, or every transitive dependency. The LS0 scan/cap pins and deterministic descent were checked directly.
- Re-execution or full code audit of the numerical experiments, Monte Carlo widths, or the polynomial inverse-decay lemma. Numerical findings were assessed as observations only.
- Literature priority, external sources, and any files outside the manifest whitelist. In particular, no other review report, LOG, CHECKPOINT, forbidden memo worktree, or external HOLD file was consulted.

Verdict: CONTINUE WITH CHANGES
