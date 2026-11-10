DO-NOT-LOCK

Independent statement-lock review, R01 (Sol, high). Scope: the requested statement, code check, plan, program/protocol, origin passages, chapter setting, and production source on the current filesystem. No git state-changing commands were run. No proof is accepted by this review. The main non-asymptotic screening target is sound in form; the package needs the corrections below before locking. Findings distinguish an actual missing growth hypothesis from a failure of the proposed local-optimum proof route.

1. **BLOCKER ? A1 loses all control of dimensionality when q_n = 0.**

   **Location:** `Theory_work/Wave3/W3-SCR/STATEMENT.md:73-77` (compare :60-64 and :112-116).

   **What is wrong:** The corollary allows q_n=0, but q_n log p + log n <= c1 n then says nothing about p. The response-scale threshold still contains log p. The asserted corollary does not follow from A-infinity and, under the stated unrestricted dimensional regime, has a counterexample. A polynomial-p restriction is not stated in A1; it cannot be silently borrowed from the old chapter after :63 explicitly broadens the regime.

   **Evidence/derivation:** Take s0=1, theta_1=b>0 fixed, sigma fixed, and every design column equal to x_1, centered with norm squared n-1. Set q_n=0. The required floor is only on singleton sets, so kappa=1, theta_min=b, and ||theta||_1=b satisfy the hypotheses. The empty model's best missing-truth gain is asymptotically n b^2, while tau_n^2 -> b^2+sigma^2. Choose log p ~ c n with c sufficiently large, or log p ~ n^2. In the latter case there is a deterministic bound, uniformly in standardized y: Q_S >= (n-1)/(n+1) for every S, so the entire possible log-likelihood advantage is O(n log n), whereas every nonempty feasible model pays at least log(2p-1) ~ n^2 in prior cost. The determinant term is nonpositive. Thus the empty model is the unique global maximizer for all large n, is LO, and misses S0, despite every displayed A1 hypothesis holding. Every completed, certified fit necessarily reports it. The output-event convention does not repair this implication; a possible lack of computational delivery is not a statistical growth hypothesis. The same example directly refutes the uniform-LO corollary the proposed proof would establish.

   **Fix:** Replace q_n log p by (q_n vee 1) log p (with a suitable constant), or explicitly impose polynomial p in A1, or restrict this corollary to q_n>=1 and state a separate q_n=0 condition. Preserve the intended polynomial-p PROGRAM card. Give c1 and an eventual-n qualification in L3.

2. **MAJOR ? SCR-C's hypotheses permit false LO supersets; the proposed certificate-only proof is insufficient.**

   **Location:** `STATEMENT.md:79-84`; `PLAN.md` L5 and Risks. This concerns the unrestricted growing-s0 regime actually allowed by :60-64, :80.

   **What is wrong:** The floor 2 log p/(2 log p+log n)+epsilon does not imply that every small LO superset equals S0. At size k the actual size-prior contribution to a deletion is log((2p-k)/k), not log(2p). The log k term cannot simply be discarded when k grows. The following construction satisfies the stated hypotheses but has false LO supersets with probability tending to one. Therefore a proof that uses only 'certified implies LO' cannot establish SCR-C. This is a counterexample to that structural implication, not a demonstrated counterexample to the full coded-output probability: the latter needs a separate discovery/HPM argument if SCR-C is retained.

   **Evidence/derivation:** Let p=n-1, s0=floor(n^a), a=.49, q=s0+2, sigma=1, and theta_t=1/sqrt(s0) on the truth. Use the normalized Gram matrix with an identity true block, zero true/noise cross block, and an equicorrelated noise block with rho=.30. This is positive definite of dimension n-1 and is realizable by centered columns in R^n. This is only a counterexample/example, not a proposed family assumption.

   Every superset of S0 of size <=q contains at most two noise columns, so phi_n(q)=1-rho=.70 > 2/3+epsilon, e.g. epsilon=.02. Every missing true column is orthogonal to the other columns, so Gamma_n(q) ~ n/s0. Also ||theta||_2=1 and q log p=o(n). The A-infinity ratio diverges because sqrt(n/s0)/sqrt(q log p) ~ n^.01/sqrt(log n). Thus all displayed SCR-C hypotheses hold.

   Conditional noise correlations with the noise columns, normalized by sqrt(n-1), have the representation Z_j=sqrt(rho)Z_0+sqrt(1-rho)Z_j^ind. Pick the largest positive and most negative correlations. Both extrema are +/-sqrt(2(1-rho)log p)+O_P(1). The opposite-extreme pair maximizes the pair regression score asymptotically; take the exact maximizing opposite-extreme pair to settle swaps. With S=S0 union this pair, deletion gains for either selected noise column are

       [2(1+rho)+o_P(1)] log n = [2.6+o_P(1)] log n,

   in raw-noise quadratic units. The largest gain from adding any other noise column is

       [2(1+rho)/(1+2rho)+o_P(1)] log n = [1.625+o_P(1)] log n.

   To see the second constant, after fitting the pair the conditional noise-column norm squared, divided by n-1, is d=(1-rho)(1+2rho)/(1+rho); the extreme remaining numerator squared is [2(1-rho)+o_P(1)]log p. The common-factor component and the sum of the two opposite extrema contribute only lower-order terms. Ridge corrections vanish at this order.

   In contrast the score's actual addition/deletion threshold at k~s0 is

       2 log((2p-k)/k) + log n = [3-2a+o(1)]log n = [2.02+o(1)]log n.

   The residual variance after fitting the truths tends to sigma^2, so response standardization cancels out of these comparisons. Both noise deletions are unfavorable and every remaining noise addition is unfavorable, with strict asymptotic margins. Swaps between noise pairs cannot improve an exactly maximizing pair; deleting/swapping a true variable costs order n/s0 >> log n and is also unfavorable. Hence S is a false LO superset with probability tending to one. The elementary leading-constant checks are in `reviews/R01_scratch/check_constants.py` (2.6 > 2.02 > 1.625, floor .70 > 2/3).

   **Important limit on this objection:** The pair's *total* likelihood benefit is [2+o_P(1)]log n, below its [2.02+o(1)]log n total prior/determinant cost; S0 scores better. I am not claiming the code must report this pair. This is exactly why the lead must distinguish a local certificate from a global best/discovery argument. Merely citing the floor and a uniform noise bound will not close the gap for arbitrary certified archives.

   **Fix:** Do not lock SCR-C in its present certificate-only form. A simple first repair to investigate is fixed s0 (and an actual proof of the first-order threshold); alternatively formulate an explicit size-aware sufficient inequality using k, number of extras, the true-model conditioning, and the exact size prior. A code-dependent theorem would need additional discovery/archive exclusions and would no longer be the advertised pure LO argument. The floor on supersets is a natural conditioning domain after screening; enlarging its domain alone does not fix this construction, since the full Gram already has floor .70.

3. **MAJOR ? SCR-N is not a real-valued statement on its declared domain.**

   **Location:** `STATEMENT.md:91-96`.

   **What is wrong:** The sole restriction 4 sqrt(x/(n-1))<1 does not ensure 1-u_n/2>=0. Arbitrarily large p is allowed; L_n>2(n+.02) makes c_n(x) imaginary. The hypotheses and conclusion cannot be evaluated as real inequalities.

   **Evidence:** For example n=100, x=1, p=ceil(exp(200)) gives 4/sqrt(99)<1 but L_n/(100.02)>2. This is a domain error, not an asymptotic Taylor remainder.

   **Fix:** Require u_n<2 explicitly (or <=2, with its usually impossible zero-RHS edge), or replace c_n sqrt(L_n) by the exact nonnegative threshold below. State n>=3 as required by the code.

4. **MAJOR ? A-infinity needs a different union bound from the one in PLAN/SCR-A.**

   **Location:** `STATEMENT.md:38,60-64`; `PLAN.md` first paragraph and L3.

   **What is wrong:** The displayed non-asymptotic r_n contains log s0, but A-infinity omits it and explicitly allows growing s0. It is not legitimate just to replace r_n by sqrt(2q log p). At q=0, for example, r_n(0,x)=sqrt(2log(2s0)+2x), while the asymptotic displayed noise term is zero. This is a proof-interface gap, not a counterexample to A-infinity itself.

   **Evidence/fix:** Choose one deterministic noiseless maximizer t(S) in S0\S for each offending S, before observing the errors. Only N_q Gaussian variables then need to be bounded. Prove the strengthened version with r*_n=sqrt(2log(2N_q)+2x). At q=0 the resulting O(sqrt(x)) error is negligible relative to tau_n sqrt(log n), for a slowly diverging x. For q>=1, log N_q <= q log p+log(q+1); the extra terms can be handled with the log n term and the strict liminf gap (or a sharper entropy bound). Choose x_n->infinity slowly enough that x_n/n->0 and all remainders are negligible. This fixes the arbitrary-s0 claim without imposing fixed support. Add the deterministic-witness argument to PLAN/L2/L3 rather than silently dropping log s0.

5. **MINOR ? Define the certified-model set and empty-set conventions explicitly.**

   **Location:** `STATEMENT.md:20-23,36-47,57-58,87-89`.

   **What is wrong:** 'These (at most three)' does not formally specify whether an archive from an ultimately failed run belongs to C, whether the exact-branch HPM belongs, or what an intersection over no certificates means. phi_n(q) is a minimum over an empty family if q<s0, which is allowed (especially q=0); its value is then unstated. q is used in finite sums and size floors without explicitly declaring it an integer.

   **Fix:** Define C as the union of {hpm: top-level local_certified is TRUE} and the certified archive endpoints only when status is completed. For exact output this gives the HPM singleton. State that an empty certificate intersection is [p]. Either use phi=+infinity for an empty indexing family and say SCR-C/R are vacuous after screening when q<s0, or restrict those two theorems to q>=s0. State q in {0,...,K-1}, n>=3, p>=1 (p>=2 in asymptotic formulas). On completed runs the top-level certified HPM equals an archive endpoint, so there are actually at most two distinct models there; 'at most three' is harmless but imprecise. R_S, a, gamma, Gamma and Delta are otherwise well-defined, since s0>=1 makes their offending family nonempty via S=empty.

6. **MINOR ? 'Changes vs the card' overstates the primitive-to-visibility implication.**

   **Location:** `STATEMENT.md:112-116`; compare :41,67-75; `PROGRAM.md:26-27`; `CRITIQUE_fable.md:245`.

   **What is wrong:** A floor, an anchored floor, or a positive identifiability margin plus bounded ||theta||_1 does not by itself imply the quantitative MC or A-infinity hypothesis. Signal size and dimensional growth still matter. E.g. orthogonal columns have floor 1 even with theta_min=n^-2 and Gamma tending to zero. A merely positive Delta can likewise tend to zero too fast. The current sentence 'implied by the floor ... and by the identifiability margin with bounded ||theta||_1' is too broad if 'visibility' denotes the theorem's usable hypothesis rather than a defined numerical functional.

   **Fix:** Say that Lemma B gives lower bounds for Gamma, and A1 supplies explicit coefficient/growth conditions making the required visibility margin hold. With finding 1 fixed, A1 recovers the adopted polynomial-p, fixed-coefficient card. The non-asymptotic strengthening, endpoint extension, and design-agnostic formulation are appropriate. Do not advertise the exactness extension as settled until finding 2 is closed.

7. **NOTE ? CC1-CC5 pass under EX-A, with an exact-branch qualification to 'scanned centre'.**

   **Location/evidence:** `cpp/v3_engine.h:379-414`, `cpp/v3_core.cpp:453-480,524-556`, `v3_run.R:119-149,174-200`, `v3_exact.R:6-18`, `v3_fit.R:73-86,97-131,133-173`, all under `Scripts/SMC_BVS/core/`.

   CC1: the frozen centre is completely scanned across every deletion, feasible addition, and swap. A.local_certified is set only at :414, after the :407 complete-scan record and the strict improvement test :408. On a move-cap exit :410 it remains false and returns the improving neighbor. No cycle can make that strictly better neighbor an earlier visited centre under EX-A.

   CC2: failed final statuses return before flag assembly and explicitly set FALSE (`v3_run.R:143-149`). Early preprocessing/preflight/setup/calibration failures preserve the initial FALSE (`v3_fit.R:76,99-102,117,134-137,154-159`). A successful exact branch sets the flag only at status exact (`v3_exact.R:15`; `v3_fit.R:125-130`); recursion scores every feasible set and updates the maximum (`cpp/v3_core.cpp:537-556`). Thus certified implies status exact or completed, precisely O in `s1_setting.tex:24`. Exact certification proves LO by enumeration, not by an actual local-search-centre scan. The question's literal 'is a scanned centre' is therefore false for that branch, but its essential 'no strictly better neighbor' assertion is correct.

   For completed SMC, :179 requires equality of HPM and the certified final endpoint. LS0 is joined only with the same equality test (:193-195). An equal-score ledger tie that changes the HPM cannot transfer an archive's certificate to the new model; identical integer vectors are required. The ls0=FALSE path still has the final-endpoint equality test. Failed LS0 cannot leak a top-level TRUE through the failed-status branch. Calibration/inherited best models cannot bypass either equality test.

   CC3: certified archive endpoints on completed runs are LO independently of the top-level flag, by the same scan argument. CC4: additions are skipped exactly at >=K (`v3_engine.h:397`); q<=K-1 is necessary for the screening proof. Deletions and swaps still apply at K. CC5: the score is exactly the stated formula up to constants (`v3_score.h:40,57-70,175-183,215-223`); standardization uses sample n-1 (`v3_preprocess.R:35-68,118-127`). Duplicates are not dropped as constants (:111-115), so collinear cases are within the ridge score's domain.

   Cache hits do not skip logical scoring or comparisons: `v3_engine.h:89-99` loads logm, recomputes F using the same size prior, and emits a ledger event. Cache hash collisions also cannot alias different models: `v3_score.h:271-277` checks the full sorted model vector in addition to the hash. Under EX-A this is the same score. Small p and K=p do not create an exception: infeasible additions vanish and the other neighbors are still scanned; exact enumeration is stronger. No code counterexample to CC1-CC5 was found. This is not a floating-point robustness guarantee: mathematical LO requires EX-A exactly as the statement says.

   **Proposed wording:** 'Certified HPM is LO; on SMC completed paths it is a certified scanned centre, and on exact paths it is an enumerated global maximum.' Keep local_limit separate from the negation of local_certified.

8. **NOTE ? Independent one-step derivation supports SCR-A, its T_n, MC, and the probability constant.**

   **Location:** `STATEMENT.md:14-15,30-41,51-58`; `v3_score.h:175-223`; `PLAN.md` first paragraph.

   Put lambda=1/(n+1), a=a(t|S), and b=1+x_t'[I-X_S(G_S+I)^-1 X_S']x_t. Schur complements give

       det H_(S+t)/det H_S = (n+1)a,
       det(G_(S+t)+I)/det(G_S+I) = b,
       d := Q_S-Q_(S+t) = [n/(n+1)] (x_t'R_S y)^2/a.

   Consequently for k=|S|<K the exact score increment is

       F(S+t)-F(S)
       = -log((2p-1-k)/(k+1))
         -.5 log((n+1)a/b)
         +nu [-log(1-d/(.02+Q_S))].

   This re-derives the gamma identity with precisely the statement's factor (n+1)/n. Since R_S(lambda)<=R_S(1) and lambda<=1, a<=b; indeed (n+1)a>=b, so the determinant cost lies between 0 and .5log(n+1). The prior cost is <=log(2p-1), even where it is negative. Also .02+Q_S<=n-.98 and nu=(n+.02)/2, so the likelihood increase is at least d/2 (strictly larger for positive d). Thus g_y=(x_t'R_S y)^2/a > (1+1/n)[2log(2p-1)+log(n+1)]=T_n is sufficient for an improving addition. The .02 constant has not disappeared by approximation: these finite-n inequalities use its actual value.

   For unscaled y_c, the signed noise statistic is x_t'R_S C epsilon/sqrt(a). The columns are centered, R_S preserves the centered subspace, and R_S^2<=R_S, giving variance <=sigma^2 x_t'R_S x_t/a<=sigma^2. A union bound over at most s0 N_q pairs yields failure <=e^-x for the displayed r_n. Gaussian norm concentration in the n-1 dimensional centered subspace gives tau_hat<=tau_n[1+2sqrt(x/(n-1))] with failure <=e^-x (the displayed constant is conservative). No independence between tau_hat and the projection statistics is needed. On these two events, MC ensures that every offending S has a missing truth with standardized gain >T_n. It cannot be LO. A bound 1-2e^-x is already plausible from these ingredients; 1-3e^-x is conservative and credible. Strict '>' in MC correctly matches the strict move rule and handles score ties.

   R_S is positive definite even for singular Gram matrices. a has the stated range (its lower endpoint is only a weak bound). tau_n is the square root of E[tau_hat^2], not E[tau_hat]; rename its parenthetical description if desired. All displayed definitions in this part are algebraically correct. The PLAN's schematic 'nu log(1+gain/RSS)' should specify d/(.02+Q_(S+t)), or use the exact expression above, to avoid confusing ridge gain g_y with Q decrease d.

9. **NOTE ? B1 and B2 have viable ridge proofs; no missing factor was found.**

   **Location:** `STATEMENT.md:43-47,66-71`; `PLAN.md` L4.

   Let T=S0\S, v=(I-P_S)mu, lambda=1/(n+1), E=mu'R_S mu, and c=X_T'R_S mu. The variational ridge identity gives E>=||v||^2, while the ridge normal equations imply

       theta_T'c = E-theta_S'X_S'R_S mu
                  >= E-sqrt(lambda)||theta_S||_2 sqrt(E).

   Here ||X_S'R_S mu||^2<=lambda E, by diagonalizing X_S'X_S. Since a(t|S)<=n and ||c||_infinity>=theta_T'c/||theta_T||_1, monotonicity of E-sqrt(lambda)||theta||_2 sqrt(E) for E>=lambda||theta||_2^2 yields exactly B1, including its denominator n||theta||_1^2.

   For B2 put d=(n-1)phi^a(q), m=|T|. Then ||v||^2>=d||theta_T||_2^2, proving the Delta inequalities, including min over nonempty T equal to theta_min^2. Using ||theta_T||_1<=sqrt(m)||theta_T||_2 and ||theta_T||_2>=sqrt(m)theta_min in the preceding energy bound gives

       ||c||_infinity >= sqrt(d)[sqrt(d)theta_min-sqrt(lambda)||theta||_2],

   whenever the displayed bracket is nonnegative. Dividing its square by n gives B2. In fact the intermediate error term can be smaller by sqrt(m); the stated bound is conservative. Thus the apparently absent ||theta||_1 factor in B2 is not an error. The sparse-floor-to-anchored-floor implication follows by minimizing ||X_T u-X_S v||^2 over v and applying the eigenvalue floor to S union T, whose size is <=q+s0. This works for centered fixed designs without selecting a design family.

10. **NOTE ? SCR-R is a valid adaptive-model refit bound, once C and empty-floor conventions are fixed.**

    **Location:** `STATEMENT.md:86-89`; `PLAN.md` L2/L5.

    Screening ensures S0 subset C. Then X(theta_hat_C-theta*)=P_C C epsilon and the coefficient error is supported on C. For a fixed k-set the Gaussian norm tail is bounded by sigma[sqrt(k)+sqrt(2t)]. Set t=k log(ep/k)+2 log n. Since binom(p,k)<=(ep/k)^k, a union bound over all k-sets costs <=n^-2 per size. Summing k<=q<=n/2 costs O(1/n). This is exactly the displayed prediction bound, including 4log n. The superset floor then gives ||X error||^2>=(n-1)phi ||error||_2^2 and invertibility of G_C. It needs no sample split, conditional-on-selection normality, upper sparse eigenvalue floor, or fixed support. Use y_c as stated, or explicitly multiply the standardized-response refit by tau_hat; the production standardized regression coefficients alone have a different scale. This is a theorem about a proposed OLS refit, not evidence the fit already outputs that refit.

11. **NOTE ? SCR-N's algebra is sound after fixing its domain; qualify both sharpness consequences.**

    **Location:** `STATEMENT.md:91-101`; `PLAN.md` L6.

    At the empty set, a=n^2/(n+1), so gamma(j|empty)=(x_j'mu)^2(n+1)/n^2 exactly. The determinant ratio for the first addition is n, making the exact penalty L_n/2. Write A=.02+Q_empty=n-.98. The exact condition for that addition not to improve is

        g_y <= B_n := [(n+1)/n](n-.98)[1-exp(-L_n/(n+.02))].

    With u=L_n/(n+.02) in [0,2], 1-e^-u >= u(1-u/2) and

        [(n+1)(n-.98)]/[n(n+.02)] >= 1-n^-2.

    Therefore B_n >= (1-n^-2)(1-u/2)L_n, explaining the stated c_n. A two-sided scale event tau_hat>=tau_n(1-4sqrt(x/(n-1))) and the two Gaussian union bounds in (i),(ii) plausibly fit inside the stated 5e^-x allowance (it is conservative). A proof must work with centered noncentral Gaussian norms; treating tau_hat as independent or central chi-square would be wrong. Replacing c_n sqrt(L_n) by (1-4sqrt(x/(n-1)))sqrt(B_n) repairs the domain issue without a Taylor truncation.

    Consequence (1) needs an exhibited sequence, not the assertion that (i)-(ii) permit arbitrary near-threshold visibility. A valid route is fixed s0=1, log p asymptotic to A log n, truth orthogonal to all noise columns, gamma_true/tau_n^2=(1-delta)^2(2log p+log n), and x_n->infinity with x_n=o(log n). Take sigma fixed and theta_true of order sqrt(log n/n); tau_n/sigma->1. Condition (i)'s noise term is negligible, and (ii) has strict slack because sqrt(2A)<sqrt(2A+1). This demonstrates sharpness of the *uniform LO exclusion threshold*. To transfer it to the exact coded-output statement, still address whether the algorithm returns a certified empty HPM; existence of a bad LO model alone is not automatically a failure probability for that output.

    Consequence (2)'s exact two-column formula is gamma_max=(n-1)^2(n+1)b^2(1-r)^2/n^2, so the displayed approximation and Delta_empty=2(n-1)b^2(1-r) are correct. To demonstrate failure of a Delta-only substitute at the screening scale, one can take s0=p=2, 1-r=n^-1, b^2=(log n)^2: Delta~2(log n)^2 >> log n, but gamma_max~(log n)^2/n << log n and tau_n->sigma. Then x_n->infinity, x_n=o(log n) satisfies SCR-N's two truth inequalities and there are no nontruths. The empty model is LO with probability tending to one. State the precise proposed Delta-only replacement being refuted; this does not disprove bounds that also control ||theta|| or that force Delta large enough to imply visibility via B1.

12. **MINOR ? State the scope of the implementation idealization and separate unsupported example claims.**

    **Location:** `STATEMENT.md:7-12,25-26,109-120`; `s1_setting.tex:7,20,24,31-32`; `v3_preprocess.R:103-127`.

    The mathematical model is properly a deterministic standardized-design triangular array, not automatically a theorem for random standardized designs or fixed raw coefficients. A random-design corollary must condition on the design, require independent errors, and establish the post-standardization floors and coefficient bounds. The chapter fixes s0, polynomial p and sigma; this ticket broadens s0 and p and should mark that explicitly rather than only saying 'as' the old setting. If sigma is intended fixed along n, say so; if sigma_n is allowed, verify each asymptotic remainder under that convention. Specify that p refers to retained nonconstant columns and translate original indices when constant raw columns have been removed. The code requires n>=3 and finite inputs; tau_hat>0 is almost sure under this Gaussian model.

    EX-A is a named idealization, not proof that floating-point TRUE flags imply exact mathematical inequalities. The coded flags do not apply numerical score-error margins to each local comparison. That limitation is already consistent with the chapter's EX-A description; keep it explicit and do not claim an unconditional floating-point certificate. No premise concerning ideal uniforms, start mode, e4, calibration success, leakage, blocks, or a particular seed is needed for SCR-A once an actual LO certificate exists. Resource failures are handled by O and false top-level flags, not by assuming delivery. The old chapter's 'LS0 not merged to main' remark (:20) is stale relative to the source read here; do not import that remark as a current implementation fact.

    The Gaussian-row example at :109-111 needs an exact cited result plus the conditions on marginal variances/standardization. A raw covariance lower bound alone does not imply a uniform eigenvalue floor after column normalization: e.g. a 2x2 covariance with diagonals M and off-diagonal M-1 has raw minimum eigenvalue 1 but correlation minimum eigenvalue 1/M. Thus lambda_min(Sigma)>=c by itself is insufficient as written without bounded/normalized diagonal variances. Do not use the example as evidence for a theorem hypothesis until this is repaired. Families do not appear in the theorem statements; the design-agnostic requirement in PROGRAM:8-10 and PROTOCOL:20 is met.

    The numerics library also has a harmless-for-search but real normalization discrepancy: `numerics/scr_lib.py`, `Score.__init__`, defines logWK=logsumexp(logw), omitting binom(p,k), whereas `v3_score.h:66-68` includes it. This shifts every F by one constant, so it cannot invalidate neighbor comparisons or the threshold derivations; it does mean numerical agreement up to a constant does not independently validate posterior normalization. Correct or label it before reusing that library for evidence/PIPs.

Disposition: preserve SCR-A, the primitive bridges, the corrected A-infinity route, and SCR-R. Fix A1's growth condition and SCR-N's domain before locking. SCR-C requires a new argument or a revised hypothesis/conclusion; the certificate-only proof path presently permits false LO supersets. The PROGRAM screening target is viable and recoverable without the disputed exactness extension.
