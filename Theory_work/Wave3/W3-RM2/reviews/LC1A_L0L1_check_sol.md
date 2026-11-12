MANIFEST 0caea883fcf38765f1ebe5b264e8300622f80f6e444a49855ad91725e06f1558
Verdict per lemma: Toolkit-b VERIFIED-WITH-AMENDMENTS; SAND-F^b VERIFIED; B1 VERIFIED

Findings:

1. MINOR — `Theory_work/Wave3/W3-RM2/lemmas/L0_toolkit_b.md:62-64` (interface completeness only). STATEMENT.md:219 promises the score/contrast conclusions of GEN-L1 L1.2–L1.4. GEN-L1 L1.4(c), at `Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md:96`, is absent from the numbered conclusions of Toolkit-b. Add after (T4)(b): “(c) For every e in (0,1] and x >= 0, 2 sigma h_n sqrt(x) <= e x + sigma^2 h_n^2/e (every n). Proof: (sqrt(e x) - sigma h_n/sqrt(e))^2 >= 0.” This is an elementary missing interface statement, not a probabilistic gap or a new hypothesis. All the conclusions actually stated in Toolkit-b are verified. This one-line addition suffices to make the literal (P0) interface complete; SAND-F^b does not need this omitted clause.

2. NIT — `Theory_work/Wave3/W3-RM2/lemmas/L1_sandF_b.md:94-95`. For eta = 0, “the minimum over epsilon_1 > 0” is an infimum, not an attained minimum. Replace that sentence by: “For eta > 0 the minimum is sqrt(2 A eta) + eta/2, attained at epsilon_1 = sqrt(eta/(2A)); for eta = 0 the infimum is zero, and any 0 < epsilon_1 < 1/(2A) suffices.” The existing explicit eta = 0 choice already makes the proof correct, so this wording correction is optional and does not qualify the SAND verdict.

No FATAL or MAJOR finding. No additional amendment to the mathematical proof is required.

Checks performed:

1. Scope, frozen files, and interfaces.
   - Read the supplied brief first, then the manifest and INPUTS. SHA256 values of L0, L1, STATEMENT.md, lemma_checks.R, lemma_checks_out.txt, and RESULTS.md match their manifest entries. The digest above is the manifest header verbatim; I did not independently reconstruct the aggregate manifest digest.
   - Compared L0 with STATEMENT.md:219 (P0), and L1 with STATEMENT.md:113-121,154-155,178-180,220 (partition-free assumptions, C1 and P1). L0 uses precisely the general deterministic-family, Gram-floor, energy and cardinality hypotheses of P0. It does not impose polynomial family cardinality or bounded J_n. L1 uses the weaker block-relative visibility and leakage forms that P1 requests. Its explicit q <= K and feasibility alternatives are exactly the imported L-feas assumptions.
   - Read the source toolkit and sandwich templates, including GEN L1, C-GROW L0 and L3, RM L1b_rss and L1_fixed. L0 derives the RSS identity, probability bounds, determinant bounds, score expansion and contrast inequalities afresh. No conclusion from an unchecked source is consumed as an input to L0. Standard linear algebra, Gaussian identities, Laurent–Massart and elementary inequalities suffice. L1 consumes only L0 and supplies its own counting and tau-normalisation arguments.
   - c'_n is allowed to depend on Y; it is common to A, which is what score subtraction requires. F and table differences cancel the correct normalisers. Empty-set matrices are interpreted by the usual empty determinant/quadratic-form conventions, also explicitly handled in the proof.

2. L0 (T1), lines 34-48 and 76-82.
   - Since P_A <= C and C has rank n-1, the stated centred-noise chi-square law and Laurent–Massart substitution x = n^(1/3) give the D1 bound. The symmetric event has a larger lower-tail allowance than necessary, which is harmless.
   - For D2, rank(P_A) <= J_n and the exact exponential moment at 1/4 is 2^(rank/2). Substituting the ACTUAL log|F| in t_n gives |F|^(-1) n^(-2) exp[J_n((log 2)/2 - 1)] <= |F|^(-1) n^(-2). The union bound is exactly n^(-2).
   - For D3, h_n^2 = 2(log|VV| + log n) gives 2/(|VV| n) per nonzero vector. Zero vectors contribute no failure. The total is <= 2/n, including when VV has cardinality one. Neither union bound assumes independence or distinct projection directions.
   - H-S implies (h_n^2+t_n)log n/n -> 0, including the additional (log n)^2/n term. Consequently omega_n log n -> 0, theta_n log n -> 0 and J_n/n -> 0.

3. L0 (T2) and n0, lines 41-42,50-52,84-91.
   - Completing the square in sqrt(Lambda_A) costs exactly sigma^2 h_n^2. The D1 lower fluctuation is at most 4 n^(2/3); the centring loss of one is present in omega_n. Thus RSS_A >= sigma^2 n(1-omega_n).
   - The ceiling calculation is valid: 2 M n + 2 sigma^2 n + 8 sigma^2 n^(2/3) <= 3(M+sigma^2)n when n >= 512. RSS_A <= ||Y||^2 follows because C-P_A is an orthogonal projector. Rescaling gives (n-1)sigma^2/[6(M+sigma^2)] >= c_E n for n >= 2.
   - If Lambda_A = 0, the cross term vanishes and subtracting ||P_A epsilon||^2 yields the sharper pure-noise ceiling.
   - The explicit n0 list is sufficient for all of L0: n >= 512, omega_n <= 1/2, and (n-1)phi0^2 >= max(J_n,100). H-S guarantees such an eventual threshold. Dependence on the specified cardinality/size sequences and fixed constants is sufficient; no dependence on a selected maximiser or orientation of X is hidden here.

4. L0 (T3), (E1), (E2), (E4), lines 93-108.
   - For each Gram eigenvalue g >= (n-1)phi0^2, the determinant ratio is (n+1)(1 - n/[(n+1)(g+1)]). Each subtracted fraction is <= 0.01. Applying log(1-x) >= -2x gives the stated signed eta_A bound.
   - The matrix identity G^(-1)-n H^(-1) = G^(-1)(G+I)H^(-1) is exact. The middle eigenvalue factor is positive and <= (1+1/g)/(n+1) <= 1.01/(n+1). Since ||P_A y||^2 <= n-1, Q_A-RSS_A^y lies in [0,1.01], including A empty. Therefore a_A lies in [0.02,1.03].
   - (1/2+0.01/n)*1.03 < 0.52 for n >= 3 (at n=3 it is approximately 0.518434). This verifies the requested 0.52/c_E bound with slack. The determinant contribution -eta_A/2 is nonnegative and <= |A|/[(n-1)phi0^2] <= 1. Hence R_A is in the displayed asymmetric interval and |R_A| <= kappa_E = 0.52/c_E+1, exactly the source constant.
   - The RSS rescaling sign in c'_n and both score-difference signs are correct. Subtraction gives |R_A-R_A'| <= 2 kappa_E; the table formula holds for arbitrary two members of a block, not only one-column changes.

5. L0 (T4), lines 62-64,110-112.
   - Subtracting the two exact RSS identities cancels the common noise norm. D3 controls r_A-r_A'; D2 costs only one t_n, since the other projection norm has the favourable sign. This gives (a) with the stated constants at every n.
   - For (b), log u >= 1-1/u produces the denominator RSS_A, the larger RSS. The ceiling C_R n and nu >= n/2 give precisely 1/(2 C_R). Positivity of both RSS values is supplied by T2.
   - The omitted elementary Young inequality is addressed in Finding 1; its addition needs no event, Gram restriction or asymptotic argument.

6. L0 (T5) and prior, lines 66-72,114-123.
   - (a) uses log u <= u-1 and the SMALLER RSS_A' in the denominator, bounded below by sigma^2 n(1-omega_n). The exact multiplier is (1+0.02/n)/(1-omega_n); no small-gain assumption is needed.
   - (b) uses -log(1-x) <= x+x^2 <= x(1+2x) on [0,1/2], so certainly on the stated [0,1/4]. The denominator RSS_A in nu*x is controlled by T2. The bound is valid (and is weaker than (a), which already applies to the same nested pair).
   - (c) uses -log(1-x) >= x and the PURE-NOISE ceiling for RSS_A, hence 1/(1+4n^(-1/3)) >= 1-4n^(-1/3). Nesting also forces Lambda_A' = 0, though the proof does not need to invoke it separately. Zero gain causes no exception.
   - The exact binomial prior ratios, their index ranges and both inequalities in lines 71-72 are correct, including p=1 and k=p-1. Deletion ratios have the lower bound p/k; this is the bound needed in L1.

7. L0 two families, lines 125-144.
   - For blocks, the count <= 2^16 p and J_n=16 are valid even for singleton blocks or p<16. The union of residuals and pairwise differences has cardinality <= |F|+|F|^2 <= 2|F|^2. Its logarithm is O(log n) under p <= n^A.
   - Each lattice-family member is a subset of Q union {l} for some available index l; sets requiring no new column can use any l in [p]. Since S0 is nonempty, p>=1. Interlacing gives exactly the required Gram floor. The five types in the union contribute the stated bound 1+2^(q-s0)(1+p+s0+s0 p), and all sizes are <= q+1.
   - With s0 fixed, log|F_lat|+log|VV_lat|+J_n = O(q+log n). Thus q log n/n -> 0 is sufficient, in particular q<=n^b for EVERY fixed b<1. No b<1/2 restriction is needed for this toolkit application. For every T in the lattice, r_T=0.
   - The remark correctly identifies the O(q) charge in the lattice contrast bound; the score regularity itself remains valid. I did not inspect the downstream file referenced by that remark.

8. L1 hypotheses, B1, initial events, lines 13-52.
   - Residual directions exist by the block Gram floor. Their exact rank-one RSS and mean-energy identities hold after centring because each direction is perpendicular to 1. The tau monotonicity direction is correct.
   - B1 is pure quantifier restriction: block subsets have size <=16; deletion contexts have size <=15; and U union {j} has size <=16. The extra condition that U contains its block's truths only narrows the leakage contexts. Constants M_n, eta, Q and phi0 do not change. No global Gram assumption beyond FL-16 is required for these implications.
   - The number of (U,l) pairs per block of size m is m*2^(m-1), bounded by the looser 16*2^16 used in the proof. At most p blocks gives <=2^20 p. With z_n^2 = 2 log(2^21 p)+2 log log n the union bound is exactly <=1/log n. All these directions and events are deterministic functions of X, mu and Q, never of a maximiser.
   - Fact 1: P_V-P_(V\N) is a rank-|N| projector by full column rank within a block. The chi-square Chernoff bound is (tau exp(1-tau))^(d/2); for tau>1 its base lies in (0,1), so replacing d>=1 by 1 is in the correct direction. There are <=3^16 pairs. Expectation of the count needs no independence between blocks.

9. L1 Fact 2, lines 54-61.
   - AM-GM gives 2 sigma h_n sqrt(Lambda_U) <= [h_n/sqrt(n-1)] [(n-1)sigma^2+Lambda_U]. The remaining D1 and D2 losses are <= tau_U^2(4 n^(2/3)+t_n), since sigma^2<=tau_U^2. This proves the exact stated floor.
   - Taking the reciprocal floor for the smaller nested RSS_U' gives multiplier (n+0.02)/[(n-1)(1-omega_n^tau)], as written; using tau_U instead would be unjustified here. Both omega_n^tau log n and theta_n^tau log n tend to zero for the block family.
   - L1's n0 can and must be enlarged to ensure omega_n^tau<1 and, later, zeta_n<1; this is an eventual deterministic choice, consistent with the asymptotic statement.

10. L1 Step 1 through (2.2), lines 63-92.
    - Per-block optimality follows by replacing only the block factor and the model-size prior. Pure deletion of d columns is always feasible, including at k_tilde=K.
    - At most s0 blocks are bad: each has a missing truth, and blocks are disjoint. Bounding their junk by 16 s0 is valid even when s0>=17, when one block is filled by truths, or when many truths share a block. A good block has <=16 junk columns, giving (2.1) with k0=q+16 s0.
    - Multiplying d successive prior deletion ratios gives >= (p/k_tilde)^d; each intermediate size is <=k_tilde. This proves the LOWER bound on the block likelihood difference.
    - The projector Pi=P_Uhat-P_U is rank d, and Young's two-vector inequality has the stated coefficients 1+epsilon_1 and 1+1/epsilon_1. Every sequential addition context contains the block's truths, excludes the added column and stays within that block. L_b therefore gives ||Pi mu||^2 <= d eta tau_U^2 log n.
    - The mean-energy identity gives tau_Uhat^2 >= tau_U^2(1-zeta_n), zeta_n=16 eta log n/(n-1). This bound retains the essential factor 1/(1-zeta_n) on passing to the likelihood upper bound. Also ||Pi epsilon||^2 <= sigma^2 d W_b <= tau_U^2 d W_b.
    - Dividing line 87 by d/2 gives a remainder 4 kappa_E/d. Replacing it by 4 kappa_E (d>=1) weakens the lower threshold, exactly as (2.2) requires. There is no missing factor 16 or 32 in this display. theta_n'' log n -> 0 because theta_n^tau log n -> 0 and zeta_n log n = O((log n)^2/n) -> 0.

11. L1 epsilon choice, (2.3), ladder, lines 94-112.
    - For eta>0, epsilon_1=sqrt(eta/(2A)) yields limiting xi = 1/2-eta/2-sqrt(2A eta) = beta(eta,A)>0. For eta=0, epsilon_1=1/(4A) yields limiting xi=1/4. Thus xi>=xi0>0 eventually in either case. epsilon_2>=epsilon_1 and epsilon_2<=2 epsilon_1+1 eventually, providing a uniform positive exponent and bounded denominators.
    - tau_n(k) and its lower bound decrease in k; C(tau) is non-increasing. The lower threshold is >=3 eventually uniformly for k<=p, and is <=(2A+2)log n. The function sqrt(e tau) exp(-tau/2) decreases for tau>=1. Applying Fact 1 at the LOWER threshold therefore gives an upper bound on E C(tau_n(k)).
    - Expanding exp(-tau_lower/2) gives n^(-(1-eta1)/(2(1+epsilon2))) (k/p)^(1/(1+epsilon2)) exp(2 kappa_E/(1+epsilon2)). Since epsilon2>=0, the last factor is <=exp(2 kappa_E), which verifies the exact C1 in (2.3).
    - If k_tilde>2 k0, the dyadic intervals (m_i,m_(i+1)] cover it, including exact dyadic endpoint sizes. From 16 C >= k_tilde-k0 > m_i/2 one gets C > m_i/32. This verifies the factor 32 in Markov and the factor 64 after bounding 2^(1/(1+epsilon2)) by 2.
    - The clipped argument min(m_(i+1),K) lies in [1,p] and is >=k_tilde for the relevant interval. The resulting count event is independent of the CHOICE of maximiser. Union over these deterministic events proves the assertion for all maximisers without counting maximisers or choosing a measurable selector.
    - The powers of p and n combine to n^(-xi/(1+epsilon2)). The remaining sum is bounded by sum_i 2^(-(i+1)epsilon2/(1+epsilon2)), uniformly <=1/(1-2^(-epsilon1/(1+epsilon1))). The exponent remains bounded away from zero. This proves convergence of the stated ladder bound. No upper bound on q is used here: its factor k0^(-epsilon2/(1+epsilon2)) was simply discarded.

12. L1 Step 2(a), lines 116-126.
    - The good event includes the size conclusion for EVERY maximiser. When Q=[p], q<=K<=p forces K=p; a maximiser of size K then includes all truths. In all other cases requiring an addition, k_tilde<K: L-feas gives K>=2q+32s0+1=2k0+1. Hence an omitted truth can always be added.
    - The score lower bound has the correct prior, determinant and remainder signs. T4(b) supplies gain/(2 C_R). The elementary inequality (delta+sigma Z)^2 >= delta^2/2-sigma^2 Z^2 gives the stated RSS gain.
    - Explicitly, with z_n^2<=2(A+1)log n, the SCORE improvement is at least
      [M_n/(4 C_R)-sigma^2(A+1)/C_R-A-1/2] log n - log 2 - (1/2)log(1+1/n) - 2 kappa_E.
      This tends positive by M_n->infinity. Thus the proof has more than positivity of the RSS gain: it dominates every O(log n) score cost. n0 must depend on the convergence rate of M_n, as the text expressly states.
    - Full truth blocks cause no omitted-truth addition problem: a block already filled by its truths either satisfies inclusion or still has an available omitted index. A singleton block uses U=empty and the same identities.

13. L1 Step 2(b), lines 128-145: complete accounting of the margin.
    - Q=[p] is vacuous for junk exclusion. Otherwise deletion is feasible at any size, including the cap. After Step 2(a) its context U contains all block truths, so L_b applies.
    - The tau conversion again uses 1/(1-zeta_n). The bound (delta+sigma Z)^2/tau_U^2 <= (sqrt(eta log n)+z_n)^2 uses absolute values and sigma/tau_U<=1; no sign assumption on delta is needed.
    - Write t=log n, L=log p, c=42 log 2+2 log log n. Expanding the square yields eta t+2L+c+2 sqrt(2L eta t)+2 sqrt(c eta t). The L term cancels the leading prior log p, leaving coefficient 1/2-eta/2-sqrt(2A eta) before log k_tilde.
    - More explicitly the losses beyond beta(eta,A)t-log k_tilde can be bounded by
      2 kappa_E + c/2 + sqrt(c eta t)
      + theta_n''[(eta/2+A+sqrt(2A eta))t+c/2+sqrt(c eta t)].
      Here c=O(log log n), sqrt(c eta t)=O(sqrt(log n log log n)), and theta_n'' log n->0. Each loss is o(log n). This also verifies line 139's slightly looser coefficient A+1+eta+sqrt(2A eta), after absorbing the remaining c terms in its O term. Replacing log(n+1) by log n discards a favourable term; nu's 0.01 is already included in theta_n''.
    - Finally k_tilde<=2q+32s0<=(2+32s0)n^b, so log k_tilde<=b log n+log(2+32s0). The constant is absorbed in o(log n), and beta(eta,A)-b is fixed and strictly positive. The contradiction is simultaneous for every maximiser.
    - This final log k_tilde bound is the only use of the polynomial upper bound on q in L1. There is no independent use of b<1/2: it follows from b<beta(eta,A)<=1/2. For eta=0 all leakage and zeta terms vanish, and the same argument gives margin (1/2-b)log n-o(log n).

14. L1 remarks and boundary checks, lines 147-159.
    - The failure probability is the union of the toolkit failure, Z failure and ladder failure, once n is above all deterministic thresholds. The displayed bound follows. Replacing 2 log log n by 2 c log n gives Z failure <=n^(-c); the square-root splitting bounds the additional margin cost by c+sqrt(2 c eta), as stated, up to o(1) in its coefficient. A sufficiently small fixed c preserves beta-b>0.
    - The interpretation of the budget as sufficient, rather than necessary for reporting, is accurate. The source relationships are correct at the level of the reconstructed arguments; they are not being invoked outside the source cardinality ranges.
    - Checked eta=0, singleton blocks, s0>=17, a block completely filled by truths, k_tilde=K, p<n, p much larger than n, Q=[p], and q=s0+1. No step uses full rank of the entire design: only block floors are needed for L1 and Q union {l} floors for L0's lattice application. Thus p much larger than n is permitted. For small p with Q proper, L-feas may be impossible; such sequences are outside the hypotheses, not counterexamples. For Q=[p] it correctly supplies the separate saturated case.

15. Supplied falsification numerics.
    - Inspected lemma_checks.R and its recorded output, concentrating on K1 and K2, and RESULTS.md section 5. K1 computes the exact D0 remainder and checks the asymmetric remainder interval on sampled sets, including sizes up to 400. Its recorded remainders [-7.9147,-0.0100] are within the reported conservative bounds. K2 compares 1428 nested production-table pairs: differences [-0.2779,0.0093] are within +/-140.4, and the observed minimum tau-normalised RSS ratio is 0.938.
    - These are useful falsification checks, not proofs of the event assumptions. K1's sample-specific eigenvalue checks do not by themselves verify all eventual n0 hypotheses; K2's finite-n ratio is not an asymptotic floor test. No claim in this review relies on interpreting them as such. I did not execute the script: its top-level code also runs the out-of-scope L2 checks and rewrites a recorded output file.

Not checked:

- L2_width.md, L3_assemblyF.md, other review files, LOG.md and CHECKPOINT files were not read. No downstream assembly, lattice width theorem, truth-removal theorem, or reported-model consistency result is certified here.
- Did not independently audit production score implementation end to end. Limited searches of the three permitted pinned C++ files confirmed the exposed score/prior/table interfaces; the mathematical D0 score and prior stipulated in Setting F were the inputs to this review.
- Did not rerun the R numerics, perform a new Monte Carlo study, verify numerical floating-point guarantees, or certify finite-n optimality. All mathematical conclusions are under the stated Gaussian, exact-score and asymptotic assumptions.
- Did not reconstruct the aggregate manifest digest, check every external-input hash, or assess the provenance/status of unrelated registered results.
- No git commands were run, no git state was changed, and no file other than this review was written.
