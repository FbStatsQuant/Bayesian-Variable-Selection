# R02 ? Cross-family adversarial check of L1?L3 (Codex Sol)

Reviewed against locked STATEMENT.md v2, the three FAC-B reference lemmas, SoP/04_theory.tex:69?74, and FINAL/s1_setting.tex:7?18. Locations below are line numbers in the submitted S5 files. Only this review file was written.

**L1: FAILED as written.** The exact reduction and conditioning identities check, but the asserted uniform error rate in L1.4:77 is false. It has a straightforward repair; this verdict does not assert failure of the intended path theorem.

**L2: VERIFIED-WITH-AMENDMENTS.** The start-mode conclusion holds under the locked assumptions, including the full range p ? floor(n/2). Supply the determinant-increment justification in item 3 and make the positive-pair denominator explicit.

**L3: VERIFIED-WITH-AMENDMENTS.** P(E_n) ? 1 and all pair counts/tail bounds check. Correct the inherited error estimate in (c4), and restrict the multiplier assertion in (c1) to the sublinear-p regime.

## Numbered findings

1. **MAJOR ? Missing sqrt(n) when converting signal leakage to noise units; k/n? is false.** Location: L1_bcs_reduction.md:71?78, specifically :77; inherited at L3_event.md:30?31.

   The bounds on beta_tilde, sigma_j, beta_tilde ? beta, and the noise and variance perturbations at :73?75 are valid. In particular, ||beta_tilde|| ? sqrt(k)/d is justified by the spectral floor and the Euclidean norm of Sigma_Rj. The error occurs only in the next conversion. The exact dimensionless error is

       epsilon_j = (sqrt(v_j/v_tilde_j) ? 1) tau_j
                 + (beta ? beta_tilde)^T g_R / sqrt(v_tilde_j)
                 + sqrt(n?1) sigma_j / (sigma sqrt(v_tilde_j)).

   Thus the stated estimates imply the uniform bound

       |epsilon_j| ? C [ (1 + |tau_j| + G_n) k/n? + sqrt(k)/n^(3/2) ],

   with the analogous bound using k+1 for addition to a size-k base. The signal term cannot in general be absorbed into k/n?: their ratio is sqrt(n/k).

   **Counterexample:** take p=2, singleton BCS groups, rho_b=0.3, rho_w=0.7, S0={1}, theta_1=1, sigma=1, T={1,2}, and delete j=2. This is permitted by BCS; rho_w need not occur off diagonal when groups are singletons. Put g=0. With a=n??1,

       beta_tilde = 0.3/(1+1/a),
       v_tilde = 1+1/a ? 0.3 beta_tilde,
       tau = G_n = 0,
       epsilon = sqrt(n?1) beta_tilde/(a sqrt(v_tilde))
               ~ (0.3/sqrt(0.91)) n^(?3/2).

   No fixed C can bound this by C k/n?. This is also a failure on bounded-noise neighborhoods, not an artifact requiring a positive probability for g=0: their noise perturbation is O(n^(?2)), and the deterministic n^(?3/2) term persists. One can realize the displayed point on E_n by taking the latent normals zero and r=n?1; s?=2. All constants allowed in the submitted bound stay bounded there.

   **Concrete fix:** replace L1.4:77 with the two-term bound above. In L3(c4), replace the first upper bound by

       C [ (1+H_q+kappa0(G_n+2L_n)+G_n) p/n? + sqrt(p)/n^(3/2) ].

   For p ? n^alpha with fixed alpha<1 this still is eventually ? n^(?1/2), uniformly over the relevant sets and nulls. Consequently the coarse final inequality in (c4) survives. Do not retain the stronger intermediate k/n? or p/n? assertion. Check later uses against the corrected bound rather than citing the false rate.

2. **MAJOR ? L3(c1) does not state the growth restriction needed for its multiplier conclusion.** Location: L3_event.md:6?7, :25?27; compare L1_bcs_reduction.md:82?85 and locked STATEMENT.md:62, :106?107.

   L1.4.2 explicitly assumes p ? n^alpha for a fixed alpha<1, and under that hypothesis its multiplier estimate, including the eventual constant 8, checks. L3(c1), under its shared setting, asserts the same conclusion without this qualification. The setting also covers the C1 regime p ? n/2, where the conclusion is false.

   **Counterexample to the unqualified consequence:** let p=floor(n/2), take T=[p], and use any permitted BCS sequence with fixed nonzero truth (one positive truth suffices for FS-BCS). Then RSS_T=sigma? r with r~chi?_(n?1?p), while the Q-versus-RSS bound gives s? psi_T=sigma? r+O(1) on E_n. Hence

       M_T = (n/2+0.01) [n/(n+1)] sigma?/(s? psi_T) ? 1,

   rather than 1/2. This occurs with probability tending to one, including on E_n. The event E2 controls the total projected noise only by p+n^(2/3); it cannot make a projection of dimension n/2 negligible.

   **Concrete fix:** split (c1). State the s? bounds under the C1 range p ? n/2, and assert M_T=1/2(1+eta_T), |eta_T|?eta_n only when p ? n^alpha for a fixed alpha<1 (in particular under P_alpha for the path). Explicitly retain the same restriction for (c4). The start proof does not use M_T?1/2 and therefore retains its n/2 range. No change to E_n or P(E_n)?1 is required.

3. **MINOR ? Correct block determinant upper bound, incomplete reason; make the positive-pair denominator explicit.** Location: L2_start.md:32?35, especially :34; L1_bcs_reduction.md:67?70.

   L1.4.1 itself is valid: write L(T)=k log(n+1)?e_T with 0?e_T?2k/((n?1)d), and subtract. However, f?log(n+1) alone is not a proof that the increment of the sum of f over two different principal spectra is ?log(n+1). That stronger inequality used in L2 is true, but needs interlacing or a Schur-complement argument.

   **Concrete fix:** let S=Sigma_(U?l), and write

       s(t)=1+t?Sigma_lU(Sigma_UU+tI)^(-1)Sigma_Ul.

   Then s'(t)=1+Sigma_lU(Sigma_UU+tI)^(-2)Sigma_Ul>0, and exactly

       L(U?l)?L(U)=log(n+1)+log[s(1/a)/s(1/a')]
                  ? log(n+1),  a'=n?1.

   The lower bound needed in the zero-pair proof follows directly from L1.4.1 with k?16. Alternatively use its two-sided O(1/n) increment bound for both flip proofs, absorbing this into their slack.

   At :32 the signal term also has a divisor sqrt(v_tilde). To make the displayed inequality literal, start with

       |t_tilde| ? (n?1)(c_FS?C/a)/(s sqrt(1+1/a))
                   ? sigma sqrt(n?1)(1+16/d)G_n/(s sqrt(d)).

   It still exceeds c_FS n/(2 s_max) eventually. The factor can also be absorbed into a newly specified O(a^(?1)) term. This is a proof-presentation repair, not a counterexample to the positive-pair improvement or C1.

4. **MINOR ? Numerical evidence overstates which quantities and swaps were checked.** Location: L1_bcs_reduction.md:3?7; numerics/l1_identities.py:5, :6?40; numerics/bcs_selftest.py:35?45, :48?51; corresponding output files.

   l1_identities.py checks the five conditioning/noise quantities, but its `score_tau` accumulator is initialized to zero and never updated. It contains neither a ridge/leakage error-rate test nor a test of M_T. Its zero `score_tau` output supplies no evidence for L1.4. This explains why item 1 is not challenged by the otherwise useful identity experiment.

   bcs_selftest.py compares every deletion and addition gain, but compares only the maximum exhaustive swap gain with the reference maximum. It does not compare each swap pair. Its recorded largest flip discrepancy is 5.21540641784668e?7 (slightly above the claimed 5e?7), and its largest absolute F discrepancy is 8.344650268554688e?7.

   **Concrete fix:** describe the existing test as ?all flips and the best exhaustive swap gain,? use an accurate tolerance (e.g. 9e?7 covering the displayed absolute discrepancies), and remove the unused score diagnostic from the claimed evidence. If every-swap or leakage-rate validation is wanted, actually compute those quantities in a future test; the current logs do not certify them.

## Coverage and surviving calculations

- **L1.0?L1.2:** sign conjugation preserves the score and block/start quantities. The exact-Gram data representation, independent chi-square remainder, and response normalization agree with D0. The Sherman?Morrison inverse formula is correct within and across groups. Applying it to W=U?{l,i}, then inverting its 2-by-2 precision block, correctly gives strictly positive conditional covariances. The regularized matrix has the stated spectral floor.
- **L1.3:** the normal equation has the correct minus sign on the weighted group noise means. Its weights form a convex combination of h and the negative group means. The residual a_j(U) is independent of (h,g_R), including u=0; its variance and the c_u? V_R term are correct. c_u/s_u decreases from (1?rho_b)^(?1/2), proving the requested tau bound. The rotation identity follows by subtracting the two nested Schur-complement increments. These identities hold for each deterministic R and simultaneously as algebraic identities; no unjustified independence of adaptively selected residuals is used.
- **L1.4 except item 1:** Schur scaling, deletion/addition signs, exact swap decomposition, and the prior ratio (2p?k)/k match the actual score. The eigenvalue bound for f and L1.4.1 are valid and uniformly o(1) when p?n^alpha, alpha<1. Under the explicitly stated sublinear-p assumption, Q-versus-RSS and E2 give RSS_T/sigma? in [n?1?p?2n^(2/3), n?1+n^(2/3)] uniformly over all T?S0, enough for L1.4.2. The response bounds follow from all three clauses of E2, including the theta*g bound. The logarithmic inequalities are correct on their stated domains; the final addition upper bound is correspondingly for M_T(tau+epsilon)??nu/2. The corrected uniform noise bounds make that domain automatic eventually in the intended growth regimes.
- **L2:** c(U,l) is determined by finitely many group-incidence patterns with truth labels retained, despite moving indices and blocks. At most 15 conditioned indices and fixed s0 suffice; unobserved group sizes do not enter the marginal covariance. Each nonempty missing-truth pattern gives a proper hyperplane because its coefficients are positive, including the conditional variance coefficient when l is itself a truth. Thus FS-BCS supplies a fixed c_FS>0. The positive-pair gain is order n, exceeding the O(log n) prior and determinant costs uniformly for p?n/2. In the zero-pair case E_S bounds the standardized noise, leakage in t_tilde is O(1/n) because the block size is bounded, RSS_U is order n, and the likelihood increment is O(log log n); the negative half-log-n determinant cost dominates. The omitted addition prior is nonpositive for k?p?1, and the deletion prior is nonnegative for k?p, so both flip signs are correct. The finite-state uniqueness argument covers S missing an element of S* and S strictly containing S*. No exponential-in-p union over start states is required.
- **L3 union bounds:** |eta| contributes an omitted-but-immediate tail ?2 exp(?L_n?/2). For E1, 2 Phi_bar(x)?exp(?x?/2) for x?0 gives 1/(2 log n). For E2, Laurent?Massart with t=log n works uniformly for p?n/2: 2 sqrt(p log n)+2 log n?n^(2/3) eventually; total noise has n?1 degrees of freedom; the remaining scalar Gaussian tail tends to zero. E3 has at most s0*2^(qbar?1) normals and fixed s0,qbar. E_A has at most p*2^(qbar?1) normals; its displayed bound is exactly 1/(2 log n), requiring no independence between pairs. For E_S there is at most one block containing S0, since s0?1. There are at most 16*2^15 pairs (indeed at most 16*2^14 when a truth is mandatory). The identity Var(g_l?beta_tilde^T g_U)=v_tilde?(1+||beta_tilde||?)/a is correct. Thus the looser displayed 2^20*2 exp[?2(20+L_n)] bound is valid. All five event failures vanish. (c2) and (c3) then hold uniformly without a union over all 2^p retained sets.

## Validation performed

Re-ran `py -3.13` on l1_identities.py: reproduced maximum normal-equation error 1.4210854715202004e?14, residual-decomposition error 9.43689570931383e?16, variance error 4.996003610813204e?16, covariance/independence error 1.1102230246251565e?16, and zero tau-bound violations. Independently evaluated the exact two-variable counterexample in item 1: n^(3/2) epsilon approaches 0.3/sqrt(0.91), while epsilon/(2/n?) diverges. Inspected the self-test implementation and stored output rather than treating its best-swap comparison as a pairwise check. Inspected s4_start.py and S4_out.txt: all 36 recorded start modes equal S* and are unique; these finite experiments support, but are not the proof of, L2.

No fatal obstruction to the intended reduction theorem was found in L1?L3. The submitted L1 error rate is nonetheless mathematically false and must be amended before these files are used as checked dependencies. This review does not verify L4, KL, or the unconditional theorem.
