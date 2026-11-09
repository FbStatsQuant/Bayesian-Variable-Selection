L1_toolkit.md: VERIFIED-WITH-AMENDMENTS
L3_CTd.md: VERIFIED-WITH-AMENDMENTS

Review R02 — line-by-line source and constant audit

Scope: the two requested lemma files, GEN L1, GROW L0/L2.0–L2.2, GROW L6.2 (including its A_score paragraph), APP L3.2 and predecessor CT/CD, locked STATEMENT (A)/(D1), and n4 Part 1. Line references below are to the files as read. No theorem-level counterexample to (A) or to these analytic inputs for (D1) was found. The conditional-covariance proof contains a false identity unless its indexing is repaired; the repair preserves the stated constants. No finite-n objection is raised. No source files or numerics were edited and no git commands were used.

1. MAJOR — L3_CTd.md:50,53–54: distinguish the full unconditioned complement from a subvector; the displayed inverse identity is false for an arbitrary V.

   The statement says “every conditional covariance matrix Cov(W_V | W_U)” without specifying V disjoint from U. Taken literally, V intersecting U gives zero conditional variances, contradicting the positive lower spectral bound. More substantively, the proof writes Cov(W_V | W_U) = (Theta_VV)^(-1). That identity holds when V = [p] minus U, not for every V contained in that complement. Marginalizing unobserved coordinates differs from conditioning on them.

   Explicit algebraic counterexample to the identity: take the three-coordinate AR(1) correlation matrix Sigma_ij = (1/2)^|i-j|, U empty, V = {1}. Then Cov(W_V) = 1 but (Theta_11)^(-1) = 3/4. This is a LOC_d matrix (already d = 1). The discrepancy persists if this block is embedded in arbitrarily large block-diagonal LOC matrices with separated sites; it is not a finite-n issue.

   Concrete fix: state (b) for V contained in [p] minus U. In the proof set H := [p] minus U. Establish Cov(W_H | W_U) = (Theta_HH)^(-1), apply CT_d to Theta_HH, and obtain the result for arbitrary V contained in H by taking a principal submatrix of that conditional covariance. For (a), j,k belong to H. Interlacing yields the spectrum in [c,C] for every such V, while conditioning reduces each individual variance from its marginal value 1. This is exactly the distinction made correctly in predecessor APP L2_CT, Lemma CD. Keep K_2 = 2C and t_2 as written. Do not apply CT_d directly to Theta_VV for an arbitrary subvector V.

2. MINOR — L1_toolkit.md:28–30,44–46,50–52: the application proves big-O envelopes, whereas L0-prime assumes coefficient-one envelopes at the same exponent.

   From q <= (log n)^kappa - 1 one does get J_n <= (log n)^kappa, but log|F| = O((log n)^kappa) and log|VV| <= log 2 + 2 log|F| need not be <= (log n)^kappa. At kappa = 1, for instance, the p factor alone can contribute A log n with A > 1. Moreover locked (A) allows q <= (log n)^kappa rather than the stricter q <= (log n)^kappa - 1 used here. For (D1), q = O((log n)^d) also has a fixed multiplicative constant. These are missing envelope conversions, not an obstruction to polylogarithmic growth.

   Concrete fix: explicitly invoke L0-prime with a larger fixed exponent, e.g. kappa_tool := kappa + 1, so that q+1, log|F|, and log|VV| satisfy its three coefficient-one bounds eventually. For (D1) use d+1. Continue to define t_n and h_n using the actual family cardinalities and J_n = q+1; those formulas do not depend on the chosen envelope exponent. Consequently their sharper O((log n)^kappa) orders remain true. Alternatively state and prove L0-prime with arbitrary fixed multiplicative envelope constants and allow n_0 to depend on them. The enlargement also covers the bounded-size polynomial family when kappa = 1.

3. MINOR — L1_toolkit.md:37–38: convergence of omega_n to zero alone is insufficient for the NA likelihood-error bound.

   The final sentence says that the argument depends only on c_n = O(log n) and omega_n -> 0. The displayed excess actually needs log n times vartheta_n -> 0 (equivalently here log n times omega_n -> 0). For example omega_n = 1/sqrt(log n) tends to zero but fails this requirement. The needed stronger rate is already available in line 17, so this is a false sufficiency claim within an otherwise valid proof.

   Concrete fix: replace the final sentence with the explicit calculation

       omega_n log n = O(n^(-1/3) log n + (log n)^(kappa+1)/n) -> 0,
       vartheta_n = O(omega_n + 1/n),
       O(log n)(vartheta_n + log n/n) -> 0.

   The prior bound log(q+1)-log p is unchanged. With q <= p, c_n = log n + O(log p + log(q+1)) = O(log n), and its leading positive log n term is not endangered by q being polylogarithmic. Thus x <= 1/4 eventually and the same final strict negative score margin follows. No weakening of the NA threshold is necessary.

4. MINOR — L3_CTd.md:4–6, numerical evidence: the printed numerical L_0 is a truncated sum, not the lemma's infinite bound.

   n4_nar_check.py Part 1 computes L0 with m = 1,...,4000. All omitted terms are positive. Thus the displayed value is a lower approximation to the analytic L_0, not a certified evaluation or upper bound for it. The omitted mass is material for the smallest t*: using the rounded c,t* in n4_out.txt gives infinite/truncated ratios about 1.17 for phi = 1.2 and 51.1 for phi = 2. The latter infinite L_0 is approximately 2.79e13, versus the printed 5.45e11. This does not falsify RB: the actual analytic bound is larger, and the observed coefficient norms are still tiny by comparison.

   Concrete fix: qualify the lemma header as comparison with a truncated numerical approximation, or, in a separately authorized numerical update, evaluate the d=2 infinite sum exactly. For q = exp(-t),

       sum_{m>=1}(2m+3)^2 q^m
       = 4q(1+q)/(1-q)^3 + 12q/(1-q)^2 + 9q/(1-q).

   Similarly, a finite-series root search for t* is not formally a certified solution of the infinite-series equation: S_4000 <= S implies its computed root can be slightly too large. Here a-t* is approximately at least 0.499, so that omitted tail is negligible for the observed CT experiment; the analytic proof, rather than this root search, supplies the certificate. Do not describe the numerics as an independent proof of CT_d/CD_d/RB/TAIL. Part 1 directly probes CT_d and sampled regression norms, not arbitrary conditioning or TAIL.

5. NIT — L3_CTd.md:26–27,72–73: two harmless notation precisions.

   If “terms” means terms of S including K, the uniform-convergence majorant should include K: K(2m+3)^d exp(-epsilon m). A fixed positive K does not change convergence. In TAIL the symbol c is used both for the spectral floor and the covariance vector in c^T M^(-1)c; rename the vector b to make the estimate Var D <= ||b||_2^2/c unambiguous. Neither changes any constant.

Checked steps without additional findings

6. L1_toolkit.md — exhaustive dependency audit of J, D, D_V, t_n, h_n in the requested source chain.

   (a) GEN L1.1: J enters the chi-square mgf factor 2^(rank/2), D enters the family union and t_n, and D_V enters the vector union and h_n. The replacement thresholds cancel the actual cardinalities exactly. Since rank <= J_n, 2^(rank/2) exp(-J_n) <= 1. Hence the new failure bounds are n^(-2), 2/n, and the unchanged 2 exp(-n^(1/3)). No independence across projections, contrasts, or events is needed. These bounds are uniform in the conditioned raw design.

   (b) GEN L1.2: the only growth-sensitive quantity is h_n^2+t_n in the completed-square RSS lower bound. It is o(n). The ceiling C_R = 3(M+sigma^2), scaled RSS floor c_E = sigma^2/[12(M+sigma^2)], and upper RSS bound remain valid. The sentence that (b)–(d) do not involve F should be understood as no additional cardinality dependence: (c) uses the floor in (a).

   (c) GEN L1.3 E1: the individual log-determinant error is bounded by 2|A|/[(n-1)phi_0^2]. Summing eigenvalue errors now costs J_n, and J_n/n -> 0 controls this exactly. E2 is dimension-free because z_A^T G_A^(-1)z_A <= ||y||^2 = n-1; no hidden J_n multiplies its ridge correction. E4 therefore still gives R_A in [-0.52/c_E, J_n/((n-1)phi_0^2)] and the same kappa_E = 0.52/c_E+1. E6 and all within-block contrasts inherit the same 2 kappa_E bound.

   (d) GEN L1.4: the contrast term uses h_n and the projection loss uses t_n; (b) needs the RSS ceiling and floor; (c) is the scalar square-completion inequality. None requires h_n^2 or t_n to be O(log n). The terminal source counting rule D_V = 2D is replaced by log|VV| <= log 2+2 log|F|; this suffices after finding 2's envelope conversion.

   (e) GROW L0.1: the old C_J log n compensation in t_n is replaced by J_n itself. Both uses of J in its proof (mgf and determinant remainder) have been covered above. GROW L0.2(a) needs (h_n^2+t_n)/n -> 0. L0.2(b) needs its floor and the stipulated x <= 1/4; L0.2(c) needs E4. The prior ratios are exact algebra independent of the polylogarithmic family growth.

   (f) GROW L2.0: all move sets lie in Q union {l}, so (G2) gives their common floor. Rank <= q+1 and log|F| <= O(q+log p) are correct; all pairwise residual contrasts fit in VV with log size O(q+log p). The fixed s_0 convention is inherited. The family contains the empty model. The identities r_T=0 and RSS_T-RSS_(T+l)=sigma^2 Z_(T,l)^2 remain exact.

   (g) GROW L2.1: with fixed theta_lo > 0, L'_n >= (n-1)phi_0^2 theta_lo^2 is of order n. Consequently sigma^2(2h_n^2+t_n) = o(L'_n), the RSS gap is at least Lambda_A/4, and the O(log n) prior/dimension penalty is dominated by L'_n/(8C_R). This explicitly uses the locked fixed beta-min, not the weaker source BM-infinity alone. No invalid extension to shrinking coefficients is made.

   (h) GROW L2.2: all source uses of q, t_n and h_n pass through the family, prior bound, omega_n, x, and the vanishing likelihood excess. Finding 3 supplies the exact rate required by the last step. No claim to extend L2.3's chi-square sufficient condition to arbitrary polylogarithmic q is made or justified here; the reviewed consequence properly stops at L2.2.

7. L1_toolkit.md — sample-regularity “unchanged” claims.

   The polynomial p assumption, fixed s_0, bounded coefficients, independent Gaussian noise, and PTV are inherited from the locked setting and the cited regularity sources. Under these premises, the augmented entrywise Gaussian event remains valid because it unions over (p+1)^2 entries, not over the exponentially many subsets. Standardization preserves the entrywise O(sqrt(log n/n)) error. Multiplication by any fixed polylogarithmic size still gives o(1) operator error, so all required sample floors follow without a new subset union.

   m_n^sharp = O(log n) is a prior-tail calculation independent of q. SE_w involves anchored sets of size s_0+O(log n), which the global floor and the same entrywise event cover even if the coefficient-one J_n convention at kappa=1 needs enlarging. Its g_0=1 requirement follows from eigenvalues of X_S^T X_S growing linearly with n. Energy follows deterministically from ||X_j||=sqrt(n-1) and fixed s_0,theta_hi. BM-infinity follows from the fixed lower coefficient bound. None of these claims requires a population upper spectral bound.

   TV uses PTV on sets of size at most 15 and a bounded-dimensional Schur-complement perturbation. A_cov involving Y also uses only bounded-size design sets and the fixed truth support. As in GROW L6.2, write the raw-scale signal coefficients as theta_j/t_j; they differ from theta_j by O(hbar_n) and remain bounded. The algebraic perturbation is uniform over those coefficients, so their sample dependence causes no independence error. Noise supplies the positive population residual variance sigma^2. The two score families have common energy/floors after conditioning on the raw design, and their failure probabilities are uniform; integration is valid even for an X-selected partition.

   The parenthetical relaxation to floors only on Q union {l} is explicitly restricted to (N1). It cannot supply global SE_w, floors for all size-16 subsets, or all bounded-set A_cov claims; keep that restriction when reusing this paragraph. Under (D1) the global spectral floor is available, so this causes no gap there.

   G1 follows from the enlargement rule: when Q is retained, p >= 2q+32s_0+1 and n/2 eventually dominates this polylogarithmic quantity. In the enlarged case p <= 2|Q^0|+32s_0 is polylogarithmic and eventually K_n=p. Fixed multiplicative size constants require the same envelope convention as finding 2, but do not alter the argument.

8. L3_CTd.md — packing, t*, radial conjugation, RB and TAIL.

   Packing at separation one is correct using open radius-1/2 balls; equality of separation causes no volume-overlap problem. The shell bound (2m+3)^d is deliberately crude (order m^d rather than the sharper m^(d-1)) but sufficient for every exponential series used. It also permits the O((log n)^d) relevance-set bound in locked (D1); closed-radius ball counts follow by the same volume argument or a decreasing limit of open-radius bounds.

   The S(t) terms are increasing in t. Uniform convergence on compact subintervals gives continuity; divergence as t increases to a follows from the displayed finite partial sums. These facts establish that the sublevel set is a nonempty closed interval bounded away from a and containing some positive t. Its maximum exists inside (0,a). In fact strict increase also follows termwise, although uniqueness is not needed. The threshold is independent of the finite site set.

   The radial function ||y-x_j|| is 1-Lipschitz and equals zero at the target j. The conjugated error need not be symmetric: the proof correctly bounds both row and column sums using the symmetric distance majorant. For m <= distance < m+1 the two factors are bounded in opposite directions exactly as written; no monotonicity of their product is assumed. The Schur bound gives ||E||_2 <= alpha/2. The Neumann argument works for this non-symmetric conjugated matrix, and its (i,j) inverse entry has the required positive exponential factor. Large radial weights introduce no extra condition because the index set is finite and only the conjugation-error bound is used. CT_d is verified with the stated constants.

   CD_d follows from CT_d once finding 1's complement/subvector distinction is restored. Both branches for covariance versus precision decay and both conversions in (c) track their lower spectral bound and envelope constants correctly.

   RB uses the inverse of the principal covariance matrix on A union {l}, not a principal block of the full precision matrix. Its identity beta_v = -Psi_vl/Psi_ll is correct. The unit marginal variance yields Psi_ll = 1/Var(W_l|W_A) >= 1, so there is no missing multiplicative factor. The two branches for (K_Sigma,t_Sigma,t'_Sigma) match the required CT_d applications. Shell summation gives the claimed dimension-uniform-in-p finite L_0.

   TAIL's residualized far variables have covariance M with eigenvalue floor c by the corrected CD_d(b). The coefficient formula for the projection difference and Var D = b^T M^(-1)b are correct. CD_d(a) controls each b_v, giving Var D <= (K_2^2/c) sum_v exp(-2t_2 d_lv). For d_lv>r, floor(d_lv) >= floor(r), so the stated shell tail is a valid overestimate, including integer r and r<1. It tends to zero uniformly as r tends to infinity. Orthogonality of the full residual to every function linear in W_T gives the exact variance decomposition in (b). Empty far sets give D=0. No additional hypothesis or constant is needed.

Disposition: apply findings 1–3 to the proofs and qualify the numerical description in finding 4; finding 5 is optional cleanup. The source audit supports locked claim (A) and the CT/CD/RB/TAIL inputs to (D1) after these amendments. This review does not certify the separate LOC-d sandwich/NA assembly files.
