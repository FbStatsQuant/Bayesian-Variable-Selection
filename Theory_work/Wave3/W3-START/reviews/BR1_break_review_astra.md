MANIFEST 053bc169c5da3c032943e217e7bd5ddb76d4268ba821b09579be126d9961a155
Verdict: NOT VERIFIED ? lemmas/L9_BR.md against the literal locked (B-R) and (T3)(b) target.

The main Gaussian-row argument survives this review after the explicit constant correction below. The NOT VERIFIED verdict is driven by the literal (B-R) conclusion's inclusion of all of (E): the hypotheses permit p = s0, whereas (E) forbids it. Thus not every repair leaves STATEMENT.md unchanged, as VERIFIED-WITH-AMENDMENTS requires. I found no counterexample to the leakage bounds or to (T3)(b). Narrowing the substantive (T3)(b) rate is not warranted by these findings.

Findings

1. CRITICAL (false scope claim). Locations: lemmas/L9_BR.md:47 and :148; STATEMENT.md:129 and :231, compared with :63-65 and :154-161.
   L9.2 proves the energy inequality, not all of (E). The latter includes "p > s0 for all large n". Setting R, (FL-R16), (V-R), and (L-R) do not imply that condition. Counterexample: p = s0 = 1, Sigma = [1], theta* = 1, sigma = 1, Q = S0 = {1}, A = 1, c_Sigma = a_V = theta_lo = theta_hi = 1, kappa_Q = 1, C_L = r_n = 0. For all sufficiently large n, |Q| <= log n and |Q| <= K; (L-R) is vacuous outside Q, visibility holds for the sole possible set U = empty, and the population floor holds. All hypotheses of (B-R) hold. Nevertheless (E) is false deterministically. The separate p = s0 discussion in L9.7 does not repair the earlier bridge assertion.
   Exact proposed repair: in STATEMENT.md:231 replace "satisfies (E)" by "satisfies the energy bound in (E) (with M = s0^2 theta_hi^2), together with the p and support-size restrictions of Setting R"; make the same qualification at L9:47,148. Alternatively explicitly restrict (B-R) to p > s0 and separately state its energy/floor/visibility/leakage conclusions at equality. The former preserves the intended Gaussian theorem in full. No repair of the literal implication is possible with STATEMENT.md unchanged. This is a scope defect, not a failure of the probabilistic bridge mechanism.

2. MINOR (undefined constant, fully local repair). Location: lemmas/L9_BR.md:79-82.
   The displayed c_d uses sqrt(Delta_loc_Sigma/2), printed as "sqrt(Delta_loc_Sigma/2)" with the original symbol sequence Delta_loc_?/2. That quantity is not defined. The denominator actually supplied by line 80 is sqrt(Delta_lo * c_Sigma/2), since the two residual squared norms divided by N are at least Delta_lo and c_Sigma/2.
   Exact repair: set c_d := sqrt(15) s0 theta_hi / sqrt(Delta_lo c_Sigma/2). Keep the displayed formulas for C4 and C5 with this corrected c_d. Then ||d|| <= c_d epsilon_n, and every subsequent inequality follows with fixed constants. Neither C_B nor C_R depends on this correction; only eventual thresholds do.

3. CRITICAL as a literal mathematical claim (local explanatory repair, no rate consequence). Locations: lemmas/L9_BR.md:144-146; numerics/lemmas/RESULTS_LEMMAS.md:36.
   The summands of Psi_n do NOT have infinite variance at finite n. Always |g| <= sqrt(N), 0 < a <= 1, and |Z| <= z_n, so
       0 <= F(g,a) <= exp((sqrt(N) + z_n)^2/2).
   Indicators only decrease this deterministic bound. For fixed n, p and the reference family are finite; every summand and Psi_n have finite moments of every order. A Gaussian upper envelope or an asymptotic limiting variable may lack a second moment, but those are different random variables.
   Exact repair: replace the parenthetical explanation by "The first-moment estimate and Markov's inequality establish tightness. No concentration argument across columns is supplied; a fixed-constant bound with probability tending to one is not established by this proof." Make the same correction to RESULTS_LEMMAS.md. Delete the inference that a Monte Carlo mean is uninformative merely because finite-n variance is infinite. The O_P conclusion itself is valid. This finding is classified CRITICAL under the brief's 'claim is false' definition, but the false remark is not used in any proof inequality.

Checks performed

Frozen inputs and scope
- Ran the authorized manifest verification command with python -B: OK, with the digest printed above. Read all of L9, the relevant locked definitions and conclusions, L3's Lemma J, all of L5, L6 and L8, and the cited lattice/visibility material in L1 and L4. Read the supplied numerical script and results. No registry premise or result from W3-RM was imported.
- Compared (B-R) and (T3)(b) against the locked text, including p = s0, growing Q, all fixed visibility levels, default truncation, and joint-law probability. The only target-scope mismatch found is Finding 1. L3's J3 and L8.2's decreasing-epsilon clause match their uses.

L9.0-L9.1
- Orthogonal rotation into 1-perp gives N = n-1 independent centered Gaussian rows even when the full covariance is singular; unit diagonal suffices. The raw mean vanishes. Polarisation has variances 2+2rho and 2-2rho, whose quarter-sum is one. The two chi-square bounds cost 4 exp(-x); union over p^2 pairs at x=(2A+2)log n gives 4n^-2. Degenerate plus/minus vectors cause no problem.
- Normalising costs at most 2h/(1-h) <= 3h when h <= 1/4. Entrywise perturbation on T costs |T|h'. The inverse identity gives Schur error h'[1+15/c+450/c^2+30/c], exactly C_S h'. Schur-complement floors follow by minimizing the full quadratic form over eliminated coordinates.
- Set sizes are legitimate: the perturbation uses at most 17 indices, allowed since s0 >= 1; the sample floors only use <=16+s0. The threshold involving 17+s0 does not assert a population floor at that size.

L9.2-L9.3
- ||mu|| <= s0 theta_hi sqrt(N) holds on every standardized design. The sample normalized floor implies the unnormalized floor with g_* = c_Sigma/2 because N >= 1.
- Residual mean inner products are sums of sample partial covariances over S0 minus U. The population sum is precisely the conditional covariance in (V-R); truths already in U contribute zero. The error is at most s0 theta_hi C_S h', yielding a_V/2, delta^2 >= N a_V^2/4, and visibility at every specified fixed c_V eventually.
- For missing truths, the Schur complement on U union S0 gives Delta_U >= Delta_lo; its size is <=15+s0. Upper energy Delta_hi is deterministic. If all truths are present, J3 applies exactly.
- Substituting delta = sqrt(Delta_U) g yields F. Symmetric integration yields the cosh expression and monotonicity in |g| for 0<=a<=1. The two square-root derivatives give precisely L_a on [a_lower,a_upper]; bounding the difference of squares proves F2, including its deliberately slack exponent.

L9.4
- Residualizing V after U0 gives both displayed identities via the Gram matrix of normalized residual remote columns. S0 subset H_l ensures all truths in U are already in U0: no truth coefficient is lost from the residual sum.
- (L-loc-R) is needed only for l versus a remote column and each remaining truth versus that column. No small covariance between two remote columns is required. Their residual covariance Schur complement has floor c_Sigma/2, and its diagonal is <=1, so its correlation matrix has the same lower floor.
- With Finding 2 repaired, ||a|| <= c_a epsilon_n and ||d|| <= c_d epsilon_n follow. q_a,q_d <=1/4 eventually, P <=2 and P-1 <=2(q_a+q_d); these give C4 exactly as displayed. The reciprocal-variance identity gives C5. The claimed rate is valid: sqrt(n log n) r_n^2 ->0 and sqrt(n log n) h_n'^2 = O((log n)^(3/2)/sqrt(n)) ->0. All these controls are uniform over the finite family of all 15-sets.

L9.5
- The population regression uses D=U0 union S0, with l outside D. The innovation is independent of W_D by joint Gaussian regression. The floor on D union {l}, of size <=16+s0, gives tau_e^2 >= c_Sigma and ||gamma^2|| <= sqrt(s0) C_L/(c_Sigma sqrt(n)).
- Pi=(I-P_U0)C is an orthogonal projection of rank N-|U0| almost surely; the finite-set population floor guarantees full sample rank for large n. Conditional on W_D, Pi, the true-column scales, mu, v, a_U0, m, and CN are fixed. Conditional on these columns, not on E_cov, e retains its Gaussian law. The bounds m_bar and d_bar follow from CN and the regression bound.
- The factor t_l is positive and cancels from the normalized residual correlation. Centering is already accounted for by Pi; it does not induce a further conditioning step. Orthogonal Gaussian components give independent xi and R conditional on W_D. R has N-|U0|-1 degrees of freedom and the appropriate noncentrality. Thus (9.1) is exact.
- Residual mu is nonzero almost surely for reference pairs at sufficiently large n, by full rank on U0 union S0 and the nonzero missing coefficients. Consequently the zero-residual convention causes no event-definition problem after modifying a null set.
- The chi-square lower-tail threshold N-16-2sqrt(Nx) is below k-2sqrt(kx) for k>=N-16, and noncentrality improves the tail. The Gaussian xi tail costs 2exp(-x). On E_R, |g| <= kappa|xi+d0|; monotonicity permits dropping E_R after upper bounding. There is no assertion of a Gaussian law given E_R, E_cov, or t_l.
- a_U0 >= a_lower holds globally, without E_cov, because standardized true columns have norm sqrt(N). Integrating xi gives (1-s'^2)^(-1/2) exp(c^2/[2(1-s'^2)]). Its denominator is >= a_lower/2. The three exponent bounds are respectively eta z_bar^2/a_lower, 2d_bar z_bar/a_lower, and d_bar^2/a_lower. This establishes Phi_n with the printed constants. CN is W_D-measurable, so the final expectation is legitimate.

L9.6
- The number of reference subsets is at most (1+|H_l|)^15, hence N_ref; no factor p^15 appears in the event union. Its failure probability is <=(4+3N_ref)n^-2 ->0 for every fixed kappa_Q.
- On E, the bound for reference |g| is O(sqrt(log n)); localisation adds iota_n<=1. F2 gives a multiplicative exp(o(1)), since iota_n sqrt(log n)->0 and epsilon_n^2 log n->0. Every U either contains all truths or reduces to a reference U0. Thus the maximum covers every X-measurable partition without requiring independence of the partition.
- Averaging divides by p, and expectation linearity needs no independence between columns. Markov gives (9.2). The log of the remaining prefactor is O(log log n), so the added 1 in C_B absorbs it for lambda=log n. eta_n z_bar_n^2 ->0. For C_L=0, the principal coefficient in e N_ref Phi_n is at most 2^17 e/sqrt(pi) times sqrt((2A+1)/a_lower), strictly below C6=2^18 sqrt((2A+1)/a_lower); the base term fits the slack eventually. These constants work for every A>0, not only A>=1.
- Tightness follows, and any diverging deterministic multiplier of its stated scale gives a probability-tending-to-one bound directly. The proof does not establish optimality of that scale or impossibility of a fixed-constant high-probability bound. More is true in some admissible cases (for example p=s0 gives leakage identically zero). No general impossibility result is justified by the false variance remark. I did not prove a general sharper concentration theorem.

L9.7-L9.8
- For p>s0 the raw-design sets are measurable and satisfy L8.0 with the stated fixed constants. Conditions involving the raw column scales are allowable because the transfer conditions on raw X. Taking c_V=2A+4 gives kappa_V=3/2 and permits kappa=1. Polylogarithmic |Q| suffices for rho_bar ->0 and rho_bar <= c_0,n eventually; bounded Q is unnecessary.
- Checked L6.0' against the actual L5.2 proof, not just its statement: epsilon only enters the Markov constants and 2exp(-n^(1/3))+2/n+1/log n <= epsilon/2. With epsilon_n=4/log n, the latter holds eventually. The other thresholds depend on the fixed constants and kappa only. Thus C_n=43s0' c_L log n, and C_R=C_B+1 absorbs C_n and the added n^-1.
- At p=s0, L8.2 is not literally applicable because its admissibility definition requires s0<p. L9 explicitly supplies a proof extension. It is valid for part (i): Q=S0=[p], U_Q=0, the lattice bound uses only s0<=K, and one omits the T1/Markov event M0 used for part (ii). L4.2's truth-addition chain and L1's lattice bound remain valid. This handles the theorem's equality case but cannot make (E)'s false strict inequality true.
- For C_L=0, the design failure limsup is <=epsilon/4, conditional transfer contributes epsilon/4, and the default tail budget is eventually <=epsilon/4. Equivalently the printed limsup <=epsilon/2 leaves strict slack below epsilon. n^-1 is absorbed by the proposed rate. No hidden global spectral bound, column independence, A>=1, or floor on sets larger than 16+s0 is used.

Independent numerical falsification
- Ran inline Python with seed 11112026; no script or output files were created. NumPy was unavailable, so the completed checks used standard-library composite Simpson quadrature (600 panels) and elementary two-dimensional matrix arithmetic.
- F2: 300 random tests with a in [0.07,0.94], |g|<=8 and z in [1,8]; zero violations, maximum left/right ratio 0.8496407715.
- Phi bound: 45 combinations, a in {0.02,0.1,0.5,0.95,1}, eta in {0,a/8,a/2}, d in {0,0.2,-1.5}, z=5; zero violations, maximum ratio 0.7071067812. At d=eta=0 the relative error against a^(-1/2)sqrt(2/pi)z was <=4.11e-15.
- Localisation: 10,000 valid residual correlation configurations with remote pair correlation in [-0.7,0.7], small a,d and |z0|<=0.9; zero violations against corrected C4, maximum ratio 7.55e-5. This is a deliberately conservative algebra/constant check, not a test of the probability of E_cov or the full 15-column case.
- The supplied script's Part A tests identities, F1/F2, and the Gaussian integral bound; it does not test covariance-event probabilities, localisation rates, actual reference-family counting, conditional independence, or leakage tightness. Its comment at line 8 still says "numerical double integral", whereas lines 61-71 correctly describe and implement one-dimensional checks. RESULTS_LEMMAS.md acknowledges most scope limits, but its variance rationale requires Finding 3's repair. I did not rerun the supplied R script.

Not checked
- Independent proofs of L1-L5 or L8 beyond the requested citation/threshold/equality-case checks; these were accepted where permitted by the brief.
- Other theorem targets (L7, L10, L11), the compiled scorer, empirical validity of the population assumptions, or any registry claim.
- A universal sharper high-probability bound in the C_L=0 case, or optimality of the polylogarithmic exponent.
- Numerical checks are falsification attempts only, not evidence for uniform asymptotic thresholds.

Only this review file was written. No git operation or subagent was used.
