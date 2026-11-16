L5 line check — sha256 S.md 45f03a2d7c719720 V.md dffd4ca5f2889158

Independent review of Lemma S, Corollaries S.1–S.2, and Lemma V(a)–(c). S.md's final Amendments section is included in the reviewed version. All six mathematical items are verified with the explicit K-truncated definition of R in S.md. There is no CRITICAL or MAJOR finding. The remaining findings concern a false numerical validation claim, the master statement's ambiguous summation convention, and a degenerate-Gaussian endpoint in the toolbox.

## Findings

### L5-01 — MINOR — Incorrect joint law in the bracket-tail simulation

Files/sections: [c_checks.py:231](/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/work/C_size/c_checks.py:231), `check_Bn_tail`, especially lines 237–239; [c_checks_out.txt:9](/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/work/C_size/c_checks_out.txt:9), the three `B_n` lines; [S.md:161](/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/work/C_size/S.md:161), Remark R6.

The simulation draws E1 ~ chi-square(N) and Zmu ~ N(0, sigma² nM) independently, then forms `(n*M + 2*Zmu + sigma²*E1)/N`. In the actual experiment E1 = ||e||²/sigma² and Zmu = mu_cᵀe involve the same Gaussian vector. They are uncorrelated but not independent when mu is nonzero. The simulated quantity can even be negative, whereas a sample variance cannot. Consequently the displayed frequencies are not Monte Carlo estimates of P(B_n^c), contrary to R6 and the script's docstring.

For the stated sigma² = M = 1 and ||mu||² = nM, the exact law is N*s_y² ~ noncentral-chi-square(N, n). Independent evaluation of its CDF/survival function gives bracket-failure probabilities approximately 1.08219e-4, 2.84187e-8, and 3.26439e-15 for n = 20, 40, and 80. These differ from the stored simulation's 2.20e-3, 3.50e-5, and zero. Also, all three displayed upper bounds exceed one, so these experiments cannot meaningfully challenge the bound even after repairing the joint law.

Minimal repair: draw z ~ N(0,1) and w ~ chi-square(N-1) independently, set E1 = z² + w and Zmu = sigma*sqrt(nM)*z, then recompute the bracket frequencies; alternatively sample the noncentral chi-square directly. Replace or withdraw the existing `B_n` output and the corresponding numerical-validation claim. This does not invalidate Step 6: its union bound uses marginal tails and never assumes independence.

### L5-02 — MINOR — The capped cutoff needs an explicit K-truncated tail in the master statement

Files/sections: [STATEMENT.md:310](/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/STATEMENT.md:310), Lemma S, especially lines 313–315; [S.md:125](/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/work/C_size/S.md:125), Corollary S.1; S.md Amendment A-4.

S.md correctly defines R_m^T with upper endpoint K. STATEMENT writes only sum over k > m. Amendment A-4 correctly explains that the main probability implication remains valid if that sum is instead taken through p: the larger sum imposes a stronger hypothesis. However, that observation does not make the accompanying assertion “m = m_n(t) qualifies” true under the full-p interpretation when m_n(t) = K < p.

A concrete family breaks that literal qualification assertion. Take any sufficiently large n (also above the stated corollary threshold), p = 2^n, and all p columns equal to a centered vector x of squared norm n-1. Set theta*_1 = 1 and all other coefficients zero, sigma² = M = M′ = 1, T = S0 = {1}, and t = log n. Then B_T(theta*) = 1 <= M+M′, s0 = 1, and m_n(t) = K = floor(n/2). The prescribed upper range t <= n^(1-kappa0) holds for sufficiently large n for every fixed kappa0 in (0,1).

Let k = K+1. Since q_0 = 1/2 and q_(r+1)/q_r = (p-r)/(2p-r-1),

q_k >= 2^(-k-1)*(1-k/p)^k >= 2^(-k-2)

for this family with n sufficiently large. Since 1/w(1) = 2(2p-1) >= 2p, the full-p sum satisfies

R_K^{S0} >= q_(K+1)/w(1) >= 2^(n-k-1) > 1.

Its hypothesis's left side is therefore positive, while -2t is negative. The cutoff does not qualify under that interpretation. The posterior probability of |S| > K is nevertheless identically zero, so this is not a counterexample to Corollary S.1's probability bound or to Lemma S's implication.

Minimal repair: define R_m^T in STATEMENT explicitly as sum from max(m+1,0) through K, matching S.md and the permitted predecessor proofs. Alternatively say that the cutoff either satisfies the full-p hypothesis when uncapped or has identically zero posterior tail at the cap. A-4 should distinguish the main implication from the cutoff-qualification sentence.

### L5-03 — NIT — Gaussian toolbox statement needs the nondegenerate hypothesis

File/section: [S.md:51](/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/work/C_size/S.md:51), Toolbox (G).

As written, `g ~ N(0,s²)` permits s = 0, but P(|g| >= s*sqrt(2x)) <= 2 exp(-x) is then false for x > log 2: the left side is one. The displayed Chernoff calculation also divides by s². The actual proof is unaffected: Step 5 explicitly handles r = 0, Step 6 explicitly handles mu = 0, and the events whose probabilities are needed use strict exceedance.

Minimal repair: state (G) for s > 0, with the degenerate case handled separately as already done in the proof; alternatively use a strict exceedance event and supply that separate case in the toolbox.

## Line-check record

### Lemma S

- **Setting and inherited identities.** The centered response and contrast formulas, N = n-1, the proper IG shape 0.51, posterior identification, and endpoints b_minus = 0.01*sigma²/2 and b_plus = 0.01*(2*(sigma²+M)+1) agree with the permitted locked [P1] source. Its deterministic T01(i), T01(ii), and thm:Ta establish the response-scale mixed-endpoint inequality. Using only the first inequality of thm:Ta and then Z_(b_plus) >= varpi(T)*m_(b_plus)(T) correctly replaces the original reference by any T in Omega.
- **Numerator.** For each fixed design, a design-measurable reference and every fixed model event are nonrandom with respect to the noise. At the data-free b_minus, the slab and variance priors are proper, including for singular Gram matrices because G+I is positive definite. Tonelli therefore gives exactly E[m_(b_minus)(S)/f0] = 1 for all models through K, without an eigenvalue condition. Normalizing by v_m gives E[Theta_m^(1)] = 1. No conditional-on-B_n Gaussian assertion or response-dependent reference is used.
- **Reference and denominator.** The trial coefficient vartheta yields Q_T^c <= sigma² E′ + B + 2|epsilonᵀr| with ||r||² <= B. The contrast inner product and norm identifications are correct, including T empty and means outside col X. The exponent inequalities in Step 3 have the correct directions: u-1 is nonnegative, 1/u >= 2-u, and the nonnegative reference cost can be bounded using 1/u <= 1. The restricted integration interval has length sigma²/sqrt(n), producing precisely D_T^(-1/2)*c_IG*sigma²*n^(-1/2)*exp(-Lambda″). The explicit lower bound on c_IG and the expression for c-sharp are correct.
- **Lambda″ tails.** The stated chi-square bounds follow from the Gaussian-square log-MGF bounds; no additional source is needed to verify their specialization here. On A_t the three summands are bounded by sqrt(t)+t/sqrt(n), 1/2+sqrt(t)+t/sqrt(n), and B/(2sigma²)+sqrt(2B)*sqrt(t)/sigma, respectively. C1 >= 2 pays the combined linear-in-t term. P(A_t^c) <= 4 exp(-t) follows by a union bound, without independence.
- **Bracket event.** The inclusion B_n^c subset {|Delta_n| > sigma²/2} is valid for every n >= 3 because n/(n-1) <= 3/2. The split thresholds N/4 and N*sigma²/8 are correct. The chi-square choices N/100 and N/64, and the Gaussian exponent N²*sigma²/(128||mu||²), give 2 exp(-n/150)+2 exp(-n*sigma²/(288M)). Thus the advertised c_B and 4 exp(-c_B*n) bound are correct, including M = 0. The simulation error in L5-01 is absent from this proof.
- **Assembly and quantifiers.** W_K cancels exactly in v_m/varpi(T), and the final Markov step costs exp(-t). C_S >= 5 absorbs both numerical probability constants and the log c-sharp term. This proves the main statement for every n >= 3 and t > 0, with constants independent of kappa0. It implies the restricted STATEMENT form. Negative m cannot qualify; m >= K gives an empty tail. Monotonicity supplies simultaneous validity over qualifying m for a fixed t and reference. Amendment A-2 correctly supplies the certain event when R_(m*) = 0; there is no division by zero after that amendment. This does not assert a simultaneous event over all references or all t.

### Corollary S.1, including A-1

T = S0 is admissible for n >= 2s0^r and has cost at most M+M′. For uncapped m, q_k <= 2^(-k), 1/w(s0) <= 2(2p)^s0, and D_S0 <= (n+1)^s0 give the stated bound of -3t before the C_S surcharge. Dropping the extra nonnegative s0*log 2 from the cutoff only weakens the estimate. For n >= 4 C_S², the linear surcharge is at most t/2; for t >= (2C_S+1)², the remaining C_S(1+sqrt(t)) is at most t/2. The original astronomical n_S and the practical A-1 range both follow. A single threshold works for every s0 <= s0^r, including s0 = 0. At the cap, the posterior tail is exactly zero and the K-truncated hypothesis holds with log R = -infinity. See L5-02 only for the ambiguous alternative full-p notation in STATEMENT.

### Corollary S.2, including A-3

n >= (1/c_B)^(1/kappa0) implies n^(1-kappa0) <= c_B*n, so the bracket term can be absorbed and the total constant is 9. In the rescaled form, apply S.1 at t′ = c*t; require t′ >= log n, t′ <= n^(1-kappa0), and n >= n_S′, exactly as completed by A-3. Since m_n(t′) <= m_n(t), posterior-tail monotonicity gives the displayed bound at m_n(t). No extra restriction on p is required. A-1 can also be used with its own explicit lower bound on t′ and the corresponding absorption threshold; it does not silently remove that lower bound.

### Lemma V(a)

The variational representation follows by completing the square in the positive-definite matrix G+a(G+I)/n. The functional-calculus representation h_a(XXᵀ) and both monotonicities are valid even when G is singular. Zero-padding preserves the principal-block penalty, which is the necessary point for monotonicity across models. Young's upper and lower inequalities give coefficients (1+1/eta) and 1/eta on rho′, respectively, hence exactly 1+2/eta after subtraction. The embedded truth has penalty theta*ᵀ(G_S0+I)theta*/n as specified in the brief. Finally 0 <= D′ <= M_S^(1/c) and the spectrum of that smoother give ||D′|| < cn/(cn+1) < 1. Empty truth, empty added set, and empty total model are covered.

### Lemma V(b)

Woodbury gives I-M_T^(a) = (Sigma_T^(a))^(-1); Sylvester gives D_T^(a) = product g_a(lambda), and D_T^(1) = D_T. The Gaussian integral is finite because every eigenvalue of D′ is below one. The comparison identity

I - Sigma0^(1/2)*D′*Sigma0^(1/2) = Sigma0^(1/2)*SigmaS^(-1)*Sigma0^(1/2) > 0

establishes both the determinant ratio and the otherwise essential strict upper spectral bound. The two congruence products have the same eigenvalues, while D′^(1/2)*Sigma0*D′^(1/2) >= D′. Eigenvalue monotonicity therefore gives the stated determinant inequality in the correct direction; it does not require the matrices to commute. The two scalar comparisons g_(1/c) <= c*g_1 and g_1 <= c*g_c then give the sharper exponent (r0+rS)/2, hence s0+|J|/2. Zero Gram eigenvalues contribute exactly one. Fixed-design determinant factors may be taken outside the expectation.

### Lemma V(c)

M_S^(1/c) <= P_S gives the stated Loewner upper bound with R0 = P_S0-M_S0^(c), and 0 <= R0 <= P_S0. Because the spaces are nested, P_S-P_S0 is an orthogonal projection of rank d_J <= |J|, orthogonal to P_S0. The resulting two squared Gaussian projection norms have the claimed independent chi-square laws, including degree zero. This supplies a pathwise coupling for the chi-square notation in STATEMENT. Duplicates and singularity reduce ranks; no inverse of a singular Gram matrix is used. All arguments allow |S| through K and indeed beyond K when considered solely as linear-algebra identities.

## Falsification and limits of this review

I checked the empty-reference and zero-truth cases, the capped tail, duplicated columns with a canceling truth, arbitrarily weak directions, exact and approximate references, J empty, and maximal permitted model size. No counterexample to either lemma, or either probability corollary with the explicit amended conventions, was found. The family in L5-02 refutes only the full-p reading of the cutoff's qualification assertion.

An independent, in-memory numerical check covered 648 deterministic V configurations at n in {3,4,8,16,32}, including duplicates, orthogonal columns, nearly duplicated columns, random designs, empty truth/model, J empty, the cap, and eta from 0.001 to 100. For part (a) it checked the joint block quadratic form in e and theta*, rather than only sampled noise vectors. The minimum computed PSD eigenvalue was approximately -2.3e-10 in the ill-conditioned cases; the minimum moment log-slack was zero. These floating-point checks found no violation beyond numerical error and are supplementary to the proofs above. Exact noncentral-chi-square probabilities independently diagnose L5-01.

I read only the brief and its permitted files. No source file was edited, no git command was run, and no agent was started. The existing S/V check code and output were inspected; the full supplied script was not rerun, and its unrelated X checks were not validated. H1, X12.md, T03R, other reviews, and other excluded dependencies were not opened; provenance claims about their exact contents or line numbers were not verified. The S and V arguments used here are re-derived in the allowed files and checked against the permitted locked [P1] identities, so those inaccessible provenance assertions are not proof premises. The two source hashes were rechecked immediately before writing this report.

## Verdicts

- Lemma S: VERIFIED — the stronger n >= 3, t > 0 result holds; existing A-2 handles the empty-tail nesting event.
- Corollary S.1: VERIFIED — original and A-1 forms, s0 = 0, and m = K; qualification uses the explicit K-truncated R.
- Corollary S.2: VERIFIED — including the range conditions supplied by existing A-3.
- Lemma V (a): VERIFIED.
- Lemma V (b): VERIFIED.
- Lemma V (c): VERIFIED.

Overall verdict: VERIFIED-WITH-AMENDMENTS — all six mathematical items are verified with S.md's existing amendments; correct the supporting simulation, make the master tail-sum endpoint explicit, and qualify the toolbox's degenerate case.
