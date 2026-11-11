# R02 — Better-theorem review (Astra, high)

Independent mathematical review, 2026-11-09. Scope: improvements, not a correctness review of the locked target. No method change. All conclusions below are asymptotic, retain polynomial p (including p much larger than n), and retain the implementation premises. Recommendations concern proposed statements and proof work, not an upgrade of inherited proof statuses.

**Verdict:** there are safe, strictly weaker hypotheses available now. In particular the entropy assumptions spend only an o(log n) portion of a log n allowance; the fixed-design leakage argument discards its RSS denominator; and n^{-2} localisation is substantially stronger than the selection-removal calculation needs. Polynomial Q is also accessible without putting a design family in the statement. I do **not** establish that floors, visibility and leakage alone suffice without lattice control, and do not have a counterexample satisfying all those hypotheses in the small-Q regime.

Sources read: the locked STATEMENT and ASSUMPTION_MAP; Wave3 PROTOCOL and PROGRAM; GROW L1_descent, L2_NA_TL, L3_sandwich; LOC2 L1_toolkit and L2_NAR; UNI L2_k0 (especially §§4–7); targeted passages of APP L5_VN, FAC-PK REPORT and GEN STATEMENT C6; production v3_engine.h:370–430. References below use these short names. Logarithms are natural.

## P1. Spend the available entropy budget in (N-D) and (D-R)

**(a) Statement.** In Form F replace (N-D)(i)'s cardinality bound by

    log |U_n| <= log p + h log n,       0 <= h < 1/2 fixed,

retaining its approximation condition rho_n^2(q+log n)=o(log n), q=|Q|, and BM-Q. The same conclusion holds. In its sufficient (N-loc) condition one may consequently replace nu_n=o(log n) by

    limsup nu_n/log n < 1/(2 log 2).

In Form R replace (R1)'s log N_n <= log p+o(log n) by log N_n <= log p+h log n for fixed h<1/2, retaining the other (D-R) conditions. These replacements can be stated as alternatives to the old branches, so no existing case is lost.

**(b) Improvement.** Strict weakening of (N-D), (N-loc), and (D-R)/(R1). It admits polynomially many extra reference patterns, rather than only subpolynomially many. This matters when Q is larger than logarithmic; it is not merely an improvement of the constant in the small-Q branch.

**(c) Proof.** Conditional Gaussian union bounds give, for any fixed small epsilon>0,

    max_v |v'epsilon/sigma|^2 <= 2 log p + (2h+epsilon) log n

with probability tending to one. The approximation error is bounded by

    rho_n max_l ||P_{Q union {l}} epsilon||/sigma
        = O_P(rho_n sqrt(q+log n)) = o_P(sqrt(log n)).

Thus max Z^2 <= 2 log p+(2h+epsilon+o_P(1))log n. Compare with GROW L2.2's threshold

    c_n = 2 log p + log n - 2 log(q+1) - O(1).

For polylogarithmic q, choose epsilon<1-2h. The strict margin survives the score expansion. LOC2 NA-R Steps 2–5 give the identical conclusion for frames: the fixed frame dimension contributes only O(log log n), atoms contribute o_P(sqrt(log n)), and sample/population comparison contributes o_P(1). No new geometry is needed.

A more flexible final wording is an explicit positive margin between the squared reference-plus-remainder bound and c_n. The displayed h-version is easier to audit and already strictly better.

**(d) Risk/effort:** LOW; approximately half a proof day, including updating the locality corollaries. Do not simultaneously relax the atom or approximation bounds without budgeting their cross terms.

**(e) ADOPT NOW.**

## P2. RSS-normalised leakage in Form F

**(a) Statement.** Replace (L-gain) by

    delta_{U,l}^2 <= eta tau_U^2 log n,
    tau_U^2 := sigma^2 + ||(I-P_U)mu||^2/(n-1),   eta<eta_A,

with the same quantifiers as (L-gain). The corresponding block-relative version has the same restricted quantifiers as (L_b). Keep the remaining hypotheses. All original reported-model and descent conclusions continue to hold.

**(b) Improvement.** This is weaker because tau_U^2>=sigma^2, and is strictly weaker when a block leaves a nonvanishing amount of mean energy unexplained. It preserves design-agnosticism and the full range of p.

**(c) Proof.** On the block family, Gaussian quadratic and linear concentration, energy O(n), and bounded block dimension give uniformly

    RSS_U / ((n-1)tau_U^2) = 1+o_P(1),

with an error times log n tending to zero. In the add/delete comparison replace the crude lower bound RSS>=n sigma^2 by this expansion. The controlling statistic becomes

    (delta_{U,l}+sigma Z_{U,l})^2/tau_U^2
       <= (sqrt(eta log n)+|Z_{U,l}|)^2.

Hence the final junk-exclusion margin is still

    [1/2-eta/2-sqrt(2A eta)]log n - log k - o(log n)>0.

For the size ladder, remove all junk in one block. Let d be its size, U the retained block subset, and V the selected subset. Along any ordering of the d junk additions, tau_{U_s}^2<=tau_U^2 and

    ||(P_V-P_U)mu||^2 <= d eta tau_U^2 log n.

The total mean-energy change is O(log n), so tau_V^2/tau_U^2=1+O(log n/n). In the multi-junk RSS comparison the noise projection divided by tau_U is bounded by the old sigma-normalised chi-square variable. GROW L3 equations (3.3)–(3.4) and its ladder then run with the same strict exponent margin. Visibility and descent proofs are unaffected.

**(d) Risk/effort:** LOW; roughly one proof day. Explicitly carry the denominator through the multi-junk comparison, rather than changing sigma to tau in only the last deletion step.

**(e) ADOPT NOW.**

### Does this alone make Form R conditional Form F? No.

The random design contributes genuinely random off-block signal to delta/tau. Its maximum need not satisfy the small eta_A bound, even after normalisation. A deterministic-X counting assumption would need the whole ladder, not merely a bound on the number of exceptionally large individual leaks.

An exact possible interface is: for each dyadic k and each good-block pair U subset V, with d=|V\U|>=1 and V\U outside Q, bound the **sum of conditional Gaussian probabilities** of

    ||(P_V-P_U)(mu+epsilon)||^2/(d tau_U^2)
        >= log n + 2 log(p/k) - o(log n).

Require these sums divided by k to be summable to o(1) over the ladder, and require their analogue for one-junk deletions at k<=2(q+16s0) to be o(1). These are computable noncentral chi-square tails conditional on X, with a fixed strict margin in the thresholds. Markov plus per-block optimality then proves the sandwich. This is a useful proof interface, but not yet a cleaner primitive condition: proving it in probability over X for an X-measurable partition is the same selection problem Form R solves. **MEDIUM, several proof days; SEPARATE TICKET.** Do not advertise the simple tau substitution as a unification of F and R.

## P3. Relax Gaussian localisation and allow logarithmic-scale leakage

### P3a. Replace n^{-2} decorrelation by a much slower rate

**(a) Statement.** In (L-loc-R), replace C_L n^{-2} in both inequalities by a deterministic r_n satisfying

    r_n = o((n log n)^(-1/4)).

Keep the original n^{-1/2} leakage, or use P3b below. The conclusions are unchanged. For example, r_n=n^{-1/3} is allowed. Keep H_l polylogarithmic and retain all population floors.

**(b) Improvement.** Strict weakening of (L-loc-R), uniformly over arbitrary X-measurable partitions; no special property of the clustering algorithm is invoked.

**(c) Proof.** Write d_n=O(sqrt(log n/n)) for the augmented sample covariance error, U0=U intersection H_l, V=U\H_l. Both conditional covariance vectors between V and the two residual coordinates have entries O(r_n+d_n). In bounded dimension, the Schur update changes their covariance and variances by O((r_n+d_n)^2). With residual variances bounded below, the sample partial correlations obey

    |rho_hat_{U,l}-rho_hat_{U0,l}| <= C(r_n+d_n)^2.

The reference correlations are O(sqrt(log n/n)), including P3b. For h=-N log(1-rho_hat^2), Taylor expansion gives

    |h_U-h_U0| <= C sqrt(n log n)(r_n+d_n)^2
                      + C n(r_n+d_n)^4 = o(1).

This is precisely the selection-removal conclusion needed in UNI L2_k0 §4, with the same p n^{o(1)} reference count and subsequent spherical tail. The calculation is uniform over bounded deterministic response coefficients, then evaluated at theta_j/t_j; never condition on the random scales.

**(d) Risk/effort:** LOW; one proof day to spell out the bounded-dimensional Schur update. The requirement that **both** cross-covariance vectors are small is essential for this quadratic error bound.

**(e) ADOPT NOW.**

### P3b. A primitive, standardised leakage budget

**(a) Statement.** For l outside Q and U0 as above, let J=S0\U0 and set

    a=Cov(W_J,W_l | W_U0),   G=Var(W_J | W_U0),
    v=Var(W_l | W_{U0 union S0}).

Replace (L-gain-R) by

    n a'G^{-1}a/v <= eta log n,       eta<eta_A fixed,

uniformly in l,U0 (interpret the numerator as zero when J is empty). Retain localisation, floors and other hypotheses. This permits pairwise leaks of order sqrt(log n/n). A convenient sufficient condition is

    max_j |Cov(W_l,W_j | W_U0)|
         <= c sqrt(eta/s0) sqrt(log n/n),

where c is the common lower variance/eigenvalue bound. Use a strict eta<eta_A, not equality.

**(b) Improvement.** The original O(n^{-1/2}) condition implies this eventually for every fixed positive eta. The new hypothesis allows an unbounded, logarithmic noncentrality budget and is expressed entirely in population quantities. The normalisation avoids hiding relevant constants in an unspecified C_L.

**(c) Proof.** Regress W_l on W_{U0 union S0}. The residual component explained by J has variance a'G^{-1}a. Conditional on these columns, the spherical proof in UNI §5 has noncentral mean m and innovation variance v. Uniform small-set concentration yields

    ||m||/sqrt(v) <= sqrt((eta+o(1))log n).

Here m means the residual mean after projecting off U0. The original O(1) shift is thus replaced by O(sqrt(log n)). The upper tail at a squared threshold t has exponent

    -1/2 (sqrt(t)-sqrt((eta+o(1))log n))_+^2,

up to subpolynomial factors. Equivalently use Young's inequality with a fixed epsilon>0. The ladder closes when

    A epsilon + (1+1/epsilon)eta/2 < 1/2,

which is possible exactly for eta<eta_A. This is the same optimisation as GROW L3.2. Reference counts and the O(log n) number of ladder levels are subpolynomial. Junk exclusion has the same positive margin as P2. Integrate over the conditioning columns, with uniform sample-scale bounds as in UNI §4–5.

**(d) Risk/effort:** MEDIUM; two to three proof days to redo the noncentral spherical tail and global ladder. This is a proof extension, not an already checked lemma.

**(e) SEPARATE TICKET**, or incorporate before the main B7 proof if that proof is not yet written. P3a can be adopted independently.

### Removing localisation altogether

The fact that the partition uses sample correlations does not imply independence of the selected off-block signal statistic. Conditional on X the off-block signal is fixed, and its correlation with selected residual directions has already been selected. A union over all p^{15} candidates spends far more than the available log n budget. I cannot justify eliminating (L-loc-R) by this argument. A new selection theorem for the actual clustering rule could do so, but is HIGH risk and multi-week work. **DO NOT PURSUE as a shortcut in this ticket**; this is not a necessity claim or a counterexample.

## P4. Joint visibility: useful block-relative relaxation, not an automatic partition-free relaxation

**(a) Statement.** Replace (V_b) by (JV_b): for each actual block C and U subset C with M=(C intersection S0)\U nonempty,

    ||(P_{U union M}-P_U)mu||^2 >= |M| M_n log n,   M_n -> infinity.

Keep the other block-relative assumptions and the lattice hypotheses. Then the same sandwich, deletion descent and reported-model conclusions hold. This is an alternative block-relative theorem, with no design family specified.

**(b) Improvement.** (V_b) implies (JV_b) by adding missing truths sequentially. The converse fails: the joint signal can be visible even if one missing truth is cancelled marginally by another. For an illustration only, a two-truth block with correlation r in (0,1) and coefficients (1,-1/r) has zero marginal gain for the first truth, but a positive order-n joint gain and positive order-n gains when either truth is conditioned on the other. Positive Gram floors hold. Extra unrelated columns can be supplied separately; this example illustrates the local condition, not a claimed full-method counterexample.

**(c) Proof.** The size ladder is unchanged: it used at most s0 bad blocks, not individual visibility. If a start maximiser misses M in C, compare it with its union with M. The Gaussian cross term and projection noise are O_P(sqrt(Delta log p)+log p), uniformly over the O(p 2^16) block pairs, where Delta is the displayed mean gain. Hence

    log gamma0(S union M)-log gamma0(S)
       >= Delta/(4 C_R)-|M|(A+1/2)log n-O(log n)>0.

The comparison is feasible eventually: when K=p every union is feasible; otherwise K=floor(n/2), whereas the ladder bounds |S| by a polylogarithm. After the truths enter, junk exclusion and the original deletion lemma apply unchanged. No joint move is added to LS0: joint comparison is only a proof of global start-mode optimality.

**Partition-free caveat.** Simply quantifying (JV_b) over every hypothetical block C of size at most 16 does not weaken (V). Take C=U union {j}; its only missing truth can be j, so the condition includes every original one-coordinate visibility test. The genuine gain is in the actual-block corollary, not in relabelling the partition-free hypothesis.

**(d) Risk/effort:** LOW; one proof day for the block-relative extension. **(e) ADOPT NOW as a block-relative alternative.**

**Dropping visibility entirely:** not established. An exact replacement sufficient for a general search theorem is an attraction region containing all possible start modes, with a strictly increasing rank along the coded best-neighbour choice and total rank length at most ell_n+|start| (or one additional scanned step for discovery alone). Without a primitive proof of that property it is a circular interface, not a better theorem. GEN's bounded relevance-set argument does not automatically extend to growing Q. **HIGH, SEPARATE TICKET**; keep joint visibility distinct from masked-truth re-addition.

## P5. Polynomial Q under primitive hypotheses, not a named design family

**(a) Statement.** A conservative extension already available from these calculations is:

* Form F, (N-D) branch: replace q<=log^kappa n by q<=n^b, where 0<b<1/4 is fixed and

      b < 1/2-eta/2-sqrt(2A eta).

  Retain BM-Q, the original subpolynomial reference count, and rho_n^2(q+log n)=o(log n). Keep feasibility, floors, T1-F and visibility. Either original leakage or P2 works.
* Form R: replace q<=log^kappa n by q<=n^b, 0<b<1/4 fixed, retaining the original (L-R), with H_l still polylogarithmic, and the actual (R1)–(R3) conditions of (D-R). In particular retain L_n^2 log(|atoms|+1)=o(log n). All original asymptotic conclusions persist.

These are design-agnostic polynomial-Q alternatives. The b<1/4 choice is deliberately conservative, not an optimal exponent claim. Existing polylogarithmic cases satisfy the F inequality for some positive b because eta<eta_A.

**(b) Improvement.** Removes the polylogarithmic restriction on (L-size), with no restriction on p beyond p<=n^A. Does not put a structural family in either theorem. Constant atom coefficient bounds do not automatically verify (R2) when the atom count is polynomial: this is a genuine verification cost, not a new hidden theorem assumption.

**(c) Proof.** Re-run LOC2 L0' with actual cardinalities, giving t_n+h_n^2=O(q+log n). The sufficient analytic conditions are

    (q+log n)log n/n ->0,    BM-Q,

so the score/TL steps remain valid. In F the approximation estimate of P1 remains valid. The NA threshold now has

    c_n-2 log p >= (1-2b)log n-O(1),

which still dominates o(log n). The F size ladder still applies (its q-dependent factor is favourable); the final junk-exclusion margin loses b log n, precisely the displayed restriction on b.

In R the existing entrywise transfer of the Gram floor costs q sqrt(log n/n)=o(1). NA-R's sample/population errors obey

    delta_n=O(sqrt((q+log n)/n)),
    omega'_n=O((q+log n)/n),
    epsilon_n=O((q+log n)/sqrt(n))=o(1).

Thus its final bound remains 2 log p+o(log n), below c_n. The spherical sandwich uses only the polylogarithmic size of H_l, not Q, in its reference count. Its ladder remains O(log n) levels. The inherited junk-exclusion display in UNI §6 is at least (1/4)log n-log k-O(1), positive for b<1/4. Truth inclusion is feasible and TL uses fixed nonzero signals. Assemble as before.

If combined with P1, replace h<1/2 by h<1/2-b. If combined with P3b, budget its noncentrality against the reduced junk margin rather than assuming unchanged constants.

**(d) Risk/effort:** MEDIUM; three to five proof days to make the toolkit extension explicit and audit every size use. **(e) SEPARATE TICKET**, high priority: this is more consequential than optimising constants inside logarithmic Q.

**Natural obstructions.** The current routes lose 2 log q in NA, log q in junk exclusion, q/sqrt(n) in Gaussian residual comparison, and require signal energy to dominate q+log n for TL. The cap/feasibility obstruction is separate. APP VN proves large or saturated start modes under pervasive exposure, not failure of reported-model consistency. FAC-PK NEG proves long swap phases for its saturated-start construction, not a counterexample with q=O(log n), (L-feas) and all the present assumptions. GEN C6's old-cap obstruction cannot be imported to the shipped cap. None of these establishes that arbitrary polynomial Q is impossible.

## P6. Can (N) or (D-R) simply be dropped? Not resolved; reject the proposed shortcut

**(a) Candidate assessed.** Floors, (V), (L), T1, q<=C log n for arbitrary C (or polylog q), with no lattice control, imply coded-LS0 discovery. I neither prove nor refute this statement. It should remain open, not be asserted false.

**(b) What the weak-extra argument actually proves.** Residualise the extras E=T\S0 against S0, obtaining Z with normalised Gram H>=phi0^2 I. If z=P_span(Z)epsilon and b_hat is its least-squares coefficient vector, the deletion losses D_e satisfy

    sum_{e in E} D_e
       = sum_e b_hat_e^2/[(Z'Z)^(-1)]_ee
       <= (n-1)||b_hat||^2 <= ||z||^2/phi0^2.

The first inequality uses residual column norms at most sqrt(n-1). Therefore

    min_e D_e/sigma^2 <= ||(P_Q-P_S0)epsilon||^2/(sigma^2 phi0^2 |E|).

This gives an inexpensive extra deletion when |E| is large relative to q/log n. It does **not** control the best swap or addition, and becomes weak when few extras remain. In particular the maximal swap is compared to its own base T\{e}, not necessarily the best-deletion base. This is why the existing deterministic lemma invokes NA at those deletion bases too.

**(c) Path and budget issues.** There are only O(q) visited sets if descent is already known. A union over those sets cannot be charged as O(q) deterministic Gaussian tests: the visited sets depend on epsilon. Likewise, strict improvement alone supplies no positive lower bound on improvement per swap. To use cap slack, one needs a quantitative potential argument bounding the number of non-deletion moves by ell_n+s0 (relative to the deletion count), not just existence of an improving deletion. The displayed floor inequality provides no such bound. Full-lattice NA failure would not itself prove LS0 failure.

**(d) Risk/effort:** HIGH; open research, potentially weeks. No valid counterexample under all the requested assumptions was found in this review. **(e) SEPARATE TICKET** for adaptive-path control; **DO NOT PURSUE** the unsupported inference that small deletion t-statistics alone remove (N). Adopt P1/P5 meanwhile.

## P7. Stronger output description and rates

**(a) Statement.** Under either primitive form, with probability tending to one the actual LS0 archive, when that branch executes, has

    returned=S0, local_certified=true, local_limit=false,
    moves=|start\S0|,  number of complete scans=moves+1.

This is an archive-level assertion; on the enumeration branch refer only to the hypothetical search. It is not automatically an assertion about a differently named top-level output field.

**(b) Improvement.** Adds exact code-level certificate and scan-count information. Exact move count, the polylogarithmic start-size bound, and a terminal scan already follow from RM-0; do not sell those alone as new stronger conclusions.

**(c) Proof.** The deterministic deletion argument leaves at least s0 unused moves in the cap ell_n+|start|. At S0 the next scan has no strict improvement. The else branch in v3_engine.h:370–430 sets local_certified=true, returned=C.S, and termination="no_improvement"; local_limit is set only in the strict-improvement/cap branch. Each loop iteration pushes exactly one completed scan.

There is no uniform polynomial error rate justified by the current assumptions: POST is only convergence in expectation, M_n may diverge arbitrarily slowly, and the approximation/atom remainders have no prescribed speed. The useful asymptotic rate interface is O(r_n+d_n) whenever E[1-pi(S0)]=O(r_n) and the combined search bad-event probability is O(d_n); the locked core already supplies that interface. Do not infer an expectation rate directly from an O_P posterior rate.

**(d) Risk/effort:** LOW; a few hours for archive wording, more if a public output field is to be identified. **(e) ADOPT NOW as a corollary**, not as the principal response to the owner's sharpness concern.

## Ranked recommendations

1. **P2 — ADOPT NOW:** RSS-normalised fixed-design leakage; broadens the primitive class cheaply.
2. **P3a — ADOPT NOW:** replace n^{-2} localisation by r_n=o((n log n)^{-1/4}).
3. **P1 — ADOPT NOW:** polynomial reference-entropy allowance in both lattice engines.
4. **P5 — SEPARATE TICKET, high priority:** polynomial Q in design-agnostic F/R statements; explicit size-budget proof above.
5. **P3b — SEPARATE TICKET:** standardised Gaussian leakage of order sqrt(log n/n).
6. **P4 — ADOPT NOW, block-relative corollary:** joint missing-truth visibility; no change to LS0.
7. **P7 — ADOPT NOW, small corollary:** exact LS0 archive certification and scan count.
8. **P6 — SEPARATE TICKET:** removal of lattice control remains genuinely unresolved; neither the weak-extra argument nor the cited limits settle it. Counting unification and complete removal of localisation likewise need new selection arguments.
