# KSA independent proof check

Date: 2026-11-12. Checker: gpt-6.1-sol, high reasoning effort.

## Verdicts and findings

| File | Verdict | FATAL | MAJOR | MINOR | NIT |
| --- | --- | ---: | ---: | ---: | ---: |
| `lemmas/S_one_step.md` | VERIFIED | 0 | 0 | 0 | 0 |
| `lemmas/A_log_factor.md` | VERIFIED | 0 | 0 | 0 | 0 |
| Total | | 0 | 0 | 0 | 0 |

No correction is required. In particular, the rank formulation in Proposition A is supported by the spherical proof without an eigenvalue floor. The verifications below supply details of short steps rather than amendments to the hypotheses or conclusions.

## Scope and method

Read the brief first, the two assigned proof files, and PSHARP STATEMENT v1.2. Read W3-POST STATEMENT lines 16–39 for the definition of the target. Also read its §2, including Corollary 1R, as expressly requested by the brief's Remark 2 attack point. No other PSHARP theory, reports, plans, maps, checkpoints, or reviews were consulted. Read the numerical scripts `core.py`, `b_check.py`, `a_orth.py`, `a_sph.py`, `a_boundary.py` and their corresponding output files. Did not read the C numerics. The optional L1a, POST2 lemma and POST2 statement extracts are not quoted by either assigned proof and were not needed or read.

Only this check file and files in `reviews/KSA_scratch/` were written. No commit and no delegation. Numerical execution used `py -3.13 -I`. The independent script and its complete output are `KSA_scratch/check.py`, `KSA_scratch/stdout.txt`, and `KSA_scratch/results.txt`. Imports of existing numerical helpers disabled bytecode writes. Tests are falsification evidence; the analytic checks below establish the inequalities.

All proof-file references below are relative to `Theory_work/Wave3/W3-PSHARP/`. Consecutive lines belonging to one calculation are checked together; every mathematical display and claim in the two files is covered.

## 1. `lemmas/S_one_step.md`

**Overall: VERIFIED.**

### Lines 1–15: setup and Lemma V

**VERIFIED.** The target notation agrees with POST §0 and PSHARP §0. For any subset, including subsets larger than K, G is positive semidefinite, A=G+I is positive definite, and H=(n+1)G+I is positive definite. Expanding the objective gives

`y'y - 2z'v + v'[G+(G+I)/n]v = y'y - 2z'v + v'Hv/n`.

Its derivative vanishes at `v=n H^{-1}z`, and completing the square gives minimum `y'y-n z'H^{-1}z=Q_S`. Both original terms are nonnegative. Because `s_y>0`, the substitution `v=s_y u` in the raw-response objective gives exactly `s_y²` times the standardized objective. For the empty set the minimization is over the sole vector in R^0, both penalties vanish, and Q_empty=y'y=n−1. No full-rank assumption is used.

### Lines 17–35: determinant identity and inequalities

**VERIFIED.** The admissible one-step hypotheses are `n>=3`, `p>=2`, `|S|+1<=K`, and `j notin S`. Standardization gives the lower right blocks `(n+1)(n−1)+1=n²` and `(n−1)+1=n`. Positive definiteness of both block matrices proves strict positivity of their Schur complements. Their determinant ratio is exactly

`D_{S+j}/D_S = [n²-(n+1)²g'H^{-1}g]/[n-g'A^{-1}g]`.

The numerator is at most n². To show the ratio is at most n, subtract n times the denominator from the numerator; the resulting inequality is equivalent to `g'[(n+1)²H^{-1}-n A^{-1}]g>=0`. For each eigenvalue λ>=0 of G the eigenvalue of the bracket is

`[(n+1)λ+n²+n+1]/[((n+1)λ+1)(λ+1)]>0`.

The expansion of the numerator at lines 32–33 is exact. Thus equality is equivalent to g=0, equivalent to orthogonality to the column space even when columns are dependent. For S empty, s=n², denominator n, and the ratio is n, as required.

Iteration over J is legitimate even if `|S∪J|>K`: this is a statement about D, which is defined on every subset, and the block-matrix argument does not use K. For J empty the product is 1. This distinction does not put any model outside Ω into a posterior sum.

### Lines 37–43: fit identity

**VERIFIED.** Block completion of the quadratic form gives the additional term `(z_j-(n+1)g'H^{-1}z_S)²/s`. The scalar in parentheses equals `x_j' rho_tilde_S`. Multiplication by n in the definition of Q yields the claimed gain. Since `0<s<=n²`, the gain is at least `(x_j'rho_tilde_S)²/n`. Lemma V supplies nonnegativity of the new Q. Empty S and zero gain are both included. The inverse block identity does not require full column rank of X.

### Lines 45–52: one-model ratio

**VERIFIED.** Here S=S0 and `s0+1<=K` ensure that both posterior scores exist in Ω. Positivity and finiteness follow from positive determinants and `2b0+Q>=0.02`. The combinatorial prior ratio is exactly `(s0+1)/(2p−1−s0)`; its denominator is positive, since `s0<=p−1`. The determinant ratio bound supplies `n^{-1/2}`. The fit ratio is `1-gamma_j`. Nonnegativity and monotonicity of Q and positivity of b0 imply `0<=gamma_j<1`. The last inequality follows by integrating `1/(1-t)>=1` from 0 to gamma, or by the power series for `-log(1-gamma)`; ν is positive.

### Lines 54–57: sum

**VERIFIED.** Item 4 retains item 3's S=S0 and admissibility hypotheses. Since S0 lies in Ω and has positive mass,

`delta/(1-delta)=(1-pi(S0))/pi(S0)=sum_{S in Ω, S!=S0} score(S)/score(S0)`.

The one-step models are distinct and admissible, and discarded terms are nonnegative. For an empty null index set the result reduces to nonnegativity. No stochastic assumption is needed.

### Lines 59–63: remarks

**VERIFIED.** The n bound is sharp for any column orthogonal to X_S. The substantive comparison to the older n+1 bound is an arithmetic improvement; the older proof itself was not an authorized dependency and was not read. The stated F1 count and errors agree with the recorded output and with the fresh F1 run: 8,064 pairs, relative determinant error 7.8e−13, Q error relative to Q_S 1.2e−14, maximum ratio/n printed as 1.000000000000. The phrase “to 1e−12” is consistent with these errors.

## 2. `lemmas/A_log_factor.md`

**Overall: VERIFIED.**

### Lines 1–10: notation and normalization

**VERIFIED.** With τ=2 log N, `sqrt(2τ/pi)=2 sqrt(log N/pi)`, so `P_n n^{-1/2}N sqrt(2τ/pi)` is exactly Λ_n in STATEMENT line 63. Eventually N>=2 because N→infinity; all finite-N lemmas explicitly require N>=2. The proof's external mathematical facts are elementary and are either expanded there or checked below.

### Lines 12–20: Lemma W

**VERIFIED.** The summands are bounded and independent. Their mean is positive because η<1 and τ>0. The lower threshold is at most `(1-epsilon') E T_N`. Chebyshev gives `Var(T_N)/(epsilon'² (E T_N)²)`. Independence gives `Var(T_N)=N Var(W_1)<=N E W_1²`. Substitution of the moment hypotheses gives

`(1+eta')/[epsilon'²(1-eta)² sqrt(2τ/pi)]`

and hence exactly the displayed factor `sqrt(pi)/(2 sqrt(log N))`. The bound may exceed 1; that does not invalidate it. No other independence is used.

### Lines 22–24: Gaussian moments

**VERIFIED.** For ζ=Z² the first exponential cancels the standard Gaussian density inside `|z|<=sqrt(τ)`, giving exactly `sqrt(2τ/pi)`. For the second moment the remaining exponential is `exp(z²/2)`, bounded by `exp(τ/2)` throughout an interval of length `2sqrt(τ)`. Both constants are correct. Truncation is `ζ<=τ`, equivalently `exp(ζ/2)<=N`.

### Lines 26–39: spherical density, Gamma bounds, and moments

**VERIFIED.** For a unit direction in R^d, ω_1² has Beta parameters `(1/2,(d−1)/2)`. The signed coordinate has density `Gamma(d/2)/(sqrt(pi) Gamma((d−1)/2)) (1-u²)^((d−3)/2)` on (−1,1). Changing variables t=sqrt(d)u introduces `1/sqrt(d)`, giving exactly h_d and c_d at line 27.

Log convexity at `(x,s)` yields `Gamma(x+s)<=x^s Gamma(x)`. Applying it at base `x+s` and increment `1-s` gives `Gamma(x+1)<=(x+s)^(1-s) Gamma(x+s)`. Therefore the lower bound is `Gamma(x+s)>=x Gamma(x)/(x+s)^(1-s)`, equal to the expression at line 31. Substitution `x=(d−1)/2, s=1/2` proves

`(d−1)/d <= c_d sqrt(2pi) <= sqrt((d−1)/d) <= 1`.

For `0<=x<=1/2`, the upper logarithmic inequality is standard; the derivative of `log(1-x)+x+x²` is `x(1−2x)/(1−x)>=0`, proving the lower inequality including both endpoints. Since `(d−3)/2>=0`, multiplication preserves directions. The upper exponent becomes `3t²/(2d)`. The lower becomes `3t²/(2d)−(d−3)t^4/(2d²)`, which is at least `−t^4/(2d)` and hence at least `−τ²/(2d)`. This verifies the entire two-sided pointwise bound, including d=3, where the polynomial exponent is zero. Because τ<=d/2, the integration interval is strictly within the density support.

Integrating the lower bound over length `2sqrt(τ)` and using the Gamma lower bound proves the claimed mean. For the second moment, factor the integrand into `exp(t²/2)[exp(t²/2)h_d(t)]`, bound the first factor by `exp(τ/2)` and the bracket by `c_d exp(3τ/(2d))`, and use the Gamma upper bound. The resulting parameters satisfy `eta in [0,1)` and `eta'>=0`. No asymptotic approximation was used in these finite-d inequalities.

### Lines 41–50: Lemma R and epsilon bookkeeping

**VERIFIED.** The setting and admissibility of S0 are inherited, so Lemma S(4) applies. On `{kappa>=1-c}`, nonnegative ζ implies `nu gamma_j>=(1-c)ζ_j/2`. On the truncated interval, `exp(-cζ_j/2)>=exp(-cτ/2)=exp(-epsilon/2)`; off the interval the right side is zero. This remains valid regardless of the sign of kappa outside the good event. Summation and the exact normalization (0) give the event inclusion at lines 47–48.

For `0<epsilon<1`, Taylor's series gives `exp(epsilon/2)<=1+epsilon/2+epsilon²/4`. Also

`epsilon/2+epsilon²/4 <= epsilon/[2(1-epsilon)]`.

Thus `(1-epsilon)exp(epsilon/2)<=1-epsilon/2`. The subsequent inequality is `1-epsilon/2 <= 1-epsilon/2+epsilon²/16=(1-epsilon/4)²`. Finally `eta<=epsilon/4` gives `(1-epsilon/4)² <= (1-epsilon/4)(1-eta)`. Lemma W with `epsilon'=epsilon/4` produces the coefficient `16/2=8`. The union bound adds the bad-kappa probability; kappa and the ζ_j need not be independent. All thresholds and strict event inclusions have the correct direction.

### Lines 52–59: orthogonal scores

**VERIFIED.** For fixed design, the u_j form a deterministic orthonormal family inside `1^perp`, orthogonal to μ. Gaussianity gives joint covariance identity for `g_j=u_j'epsilon/sigma`, so they are iid standard normals, not merely uncorrelated variables. Centering and `Cy_raw=mu+Cepsilon` give the score at line 56 with exactly one factor `1/s_y`. Orthogonality sets g_{S0,j}=0 and s=n². The fit gain is `(n−1)sigma² g_j²/(n s_y²)`. Dividing by `2b0+Q` defines V and yields `nu gamma_j=kappa_n g_j²/2` with the stated factor `2nu(n−1)/(nV)`. Since 2ν=n+0.02>=n, its lower bound is correct.

### Lines 60–68: orthogonal bound on V

**VERIFIED.** Test the raw-response variational objective at θ*. The squared residual is `||Cepsilon||²`, and the penalty is `(||mu||²+||theta*||²)/n<=M+M'`. Also

`2b0 s_y²=.02 ||mu+Cepsilon||²/(n−1) <= .04(nM+||Cepsilon||²)/(n−1)`.

For n>=3, `n/(n−1)<=3/2`, so the coefficient of M here is at most .06. Adding gives exactly `V<=sigma² E(1+.04/(n−1))+1.06M+M'`. Since C is an orthogonal projection of rank n−1, `E~chi²_(n−1)` and its variance is 2(n−1). One-sided use of Chebyshev is valid with failure at most `1/x²`.

Dividing by `sigma²(n−1)` gives exactly `1+r_n(x)` in line 65. Here r is nonnegative. The reciprocal inequality `1/(1+r)>=1-r` holds for all r>=0. At `x=n^(1/4)`, all terms in r are bounded by a constant times `n^(−1/4)`; for example `C_sigma=3+2(M+M')/sigma²` suffices for n>=3. The dimensional constraint gives N<=n−1. Thus `r*2log N<=epsilon` eventually, and `{kappa<1-epsilon/(2log N)}` is contained in `{kappa<1-r}`. The latter can occur only off the chi-square good event. Its probability is at most n^(−1/2).

### Lines 69–72: orthogonal conclusion and uniformity

**VERIFIED.** Lemma W(i) and R give exactly the stated probability bound. It tends to zero using N→infinity. The good-event threshold depends only on epsilon and `(M+M')/sigma²`; the W term is bounded uniformly by replacing N with the common diverging lower envelope. The g_j enter E and V, so independence between numerator and denominator would be false in general. The proof does not use it: the inequalities hold simultaneously on a single event, and Lemma R explicitly uses a union bound.

### Lines 74–85: spherical scores and conditional law

**VERIFIED.** Deterministic X_S0 and θ* make all truth-model response quantities functions of epsilon alone. An SVD of X_S0 gives positive λ_i and orthonormal centered v_i. The eigenvalues of P_H are `e_i=(n+1)λ_i/((n+1)λ_i+1)` in (0,1), and zero on its orthogonal complement. Thus I−P_H is invertible and preserves `1^perp`. Since s_y>0, standardized y is nonzero, so rho_tilde is nonzero. Under Gaussian noise the excluded s_y=0 event has probability zero.

Substituting `x_j=sqrt(n−1)omega_j` into the fit lower bound gives `gain>=(n−1)<omega_j,rho>²/n=||rho||² ζ_j/n`. Both the definition of kappa' and its lower bound follow, with no missing factor n−1.

Conditionally on epsilon, the normalized residual direction is fixed, and the omega_j remain iid uniform because the entire null block is independent of epsilon. Rotation invariance in dimension d=n−1 gives the product conditional law of `d omega_1²`. This product law is independent of the conditioning value, proving unconditional iid ζ_j with exactly the Lemma W(ii) law. Kappa' is a truth-block response quantity; although independence could also be deduced in this setting, it is not needed. Other columns do not enter these calculations.

### Lines 86–94: rank-only control of kappa'

**VERIFIED.** The quadratic forms are `Q=y'[I-nP_H/(n+1)]y` and `||rho||²=y'(I−P_H)²y`. Subtracting yields `y'[P_H/(n+1)+P_H(I−P_H)]y`, exactly line 87, and it is nonnegative. The first term is at most `(n−1)/(n+1)<=1` because `0<=P_H<=I` and `||y||²=n−1`.

The SVD gives `s_y v_i'y=sqrt(λ_i) w_i'theta*+v_i'epsilon`. For every λ_i>0,

`e_i(1-e_i)λ_i=(n+1)λ_i²/((n+1)λ_i+1)² <=1/(n+1)`,

and `e_i(1-e_i)<=1/4`. Apply `(a+b)²<=2a²+2b²`, sum, and use orthonormality of the w_i to obtain `s_y² y'P_H(I−P_H)y <=2||theta*||²/(n+1)+||P0 epsilon||²/2 <=2M'+sigma² E1/2`. This is where coefficient control is needed; a lower bound on λ_i is not used or hidden.

Dropping the variational penalty gives `s_y² Q>=||(C-P0)epsilon||²=sigma² E2`. The identity uses centered columns, μ in col(X_S0), and `P0 C=P0`. For fixed design, E1 and E2 are chi-square variables with ranks r0 and n−1−r0. They are independent because the two projections are orthogonal, though the proof only needs their marginal laws and that their sum is `||Cepsilon||²/sigma²`.

Since kappa'>=||rho||²/(.02+Q), the upper bound for `1-kappa'` at line 94 follows by the identity above, then replacing denominator `.02+Q` by Q, then using `s_y² Q>=sigma² E2`. Numerators are nonnegative at each replacement. E2 is positive almost surely because its rank is positive. Consequently all these divisions are legitimate almost surely. In the empty-truth case, P0=0, E1=0 (chi-square with zero degrees of freedom), and the same argument applies.

### Lines 95–102: events, constants, and growth conditions

**VERIFIED.** `s0+1<=K<=floor(n/2)` implies `m=n−1−r0>=n−1−s0>=n/2`. For E with mean n−1 and variance 2(n−1), exceeding 2(n−1) has probability at most 2/(n−1). For E2 with mean m and variance 2m, being below m/2 has probability at most 8/m<=16/n. Markov bounds `P(E1>x(r0+1))<=r0/[x(r0+1)]<=1/x` for every x>0, including r0=0. No independence between the three events is needed; use the union bound.

On their intersection,

`s_y² <=2(nM+sigma² E)/(n−1) <=3M+4sigma²`,

using n>=3, and `E2>=m/2>=n/4`. Thus line 94 is at most

`[4(1.02(3M+4sigma²)+2M')/sigma² +2x(r0+1)]/n`.

This is exactly C0 and the coefficient 2 in line 99. Write `a_n=(r0+1)log N/n`. Then `x_n=a_n^(−1/2)→infinity`. Multiplication by 2 log N yields `2C0 log N/n+4 sqrt(a_n)`. Since a_n→0 also forces log N/n→0, this tends to zero. Therefore the bad-kappa probability is bounded by the union of the three bad events, with the sum of probabilities displayed at line 102. Thresholds are eventually valid uniformly with common envelopes for the small-o sequences.

### Lines 103–106: spherical conclusion and uniformity

**VERIFIED.** `(log N)²=o(n)` and N→infinity imply n→infinity, d>=3 eventually, and `τ<=d/2` eventually. The spherical parameters satisfy `eta→0` and `eta'→0` because `τ²/d→0`, `τ/d→0`, and 1/d→0. In particular `eta<=epsilon/4` eventually, as needed in R. Substituting the three-event bound into R proves precisely line 104. Common constants, a common diverging N lower bound, and common small-o envelopes make every remainder and eventual threshold uniform. No other design columns enter a score ratio or the unnormalized lower sum; the global posterior normalizer cancels before those columns can matter. Arbitrary dependence of the unused columns therefore does not invalidate this lower bound.

### Lines 108–112: random truth block

**VERIFIED.** The hypotheses here are conditional hypotheses, not a claim that marginal G alone suffices after arbitrary conditioning. On each truth-block-measurable good event, conditional Gaussian noise and the applicable conditional null-block structure, with the common constants and envelopes specified in Proposition A, allow the corresponding deterministic bound from §3 or §4. Integrating gives failure probability at most `P(A_n^c)+sup_{A_n} P(failure | X_S0,theta*)`. Uniformity makes the supremum tend to zero, and the exceptional probability tends to zero by assumption. When the truth block is random, Λ and the admissible ranks/sizes in this expression are evaluated in the same conditional problem. In the examples these sizes are fixed deterministic sequences. A conditional orthogonal null block can also be conditioned on before applying §3; conditional fixed-design independence from epsilon is part of that witness structure.

### Lines 114–120: Corollary A1 and expectation

**VERIFIED.** Fixed s0 and all nulls give `N=p−s0`, `2N/(2p−1−s0)→1`, and `log N/log p→1`. Hence the asymptotic Λ formula is exact to relative o(1). It tends to zero: for the orthogonal witness log N<=log n; for the spherical witness `(log N)²=o(n)` is more than sufficient. The monotone map `t/(1+t)` gives the first odds-to-delta bound. The second follows from `1/[1+(1-epsilon)Λ]>=1-Λ` for Λ>=0. Taking Λ small gives the `(1-2epsilon)Λ` lower threshold; choosing arbitrary smaller fixed epsilon and absorbing the deterministic relative o(1) gives the stated `1-o_P(1)` lower bound.

Nonnegativity of delta gives `E delta>=P(good)(1-epsilon)(1-Λ)Λ`, with no uniform-integrability assumption or inference of an expectation bound from an O_P statement. Taking liminf, then epsilon down to zero, proves the exact lower constant 1, first relative to Λ and then relative to the equivalent expression in STATEMENT line 72. If `p=floor(n^a)` for a>0, `log p/log n→a`, giving the factor `sqrt(a/pi)` in line 73. This corollary retains the witness hypotheses; incompatible choices of p in the orthogonal witness are not asserted to exist.

### Lines 121–127: Corollary A2

**VERIFIED.** With s0/p→0 the same two asymptotic ratios hold, whether s0 is fixed or grows. Proposition A still applies to odds when Λ does not vanish. If pi(S0)→1, the continuous odds transform implies odds→0 in probability. A deterministic subsequence with Λ bounded below by a positive constant would contradict `P(odds>=Λ/2)→1`; hence Λ→0. This is equivalent to `(s0+1)sqrt(log p/n)→0`. In particular it implies `s0=o(sqrt(n/log p))` as claimed.

For (ii), `r_n→0`, so `delta=O_P(r_n)` gives delta→0 in probability. The preceding part gives Λ→0, allowing the A1 transform to yield `P(delta>=Λ/2)→1`. If Λ/r_n were unbounded along a subsequence, this would contradict tightness of delta/r_n. Thus Λ=O(r_n), and `log p asymp log n` gives s0+1=O(1). The growing-support illustration has exactly `||mu||²=(n−1)sum theta_j²=n−1` and `||theta||²=1`; compatible p,s0 with `s0+1<=K` exist, e.g. p=n−1 and s0 of order n^0.3. It makes no false beta-min claim.

### Lines 129–133: Remark 1, moment asymptotics

**VERIFIED.** For w>=1, `P(exp(Z²/2)>w)=2 Phi_bar(sqrt(2log w))`. Gaussian Mills asymptotics give `1/[w sqrt(pi log w)]`. Truncated mean is exactly `2sqrt(log N/pi)` as already checked. Endpoint integration asymptotics `integral_0^a exp(z²/2) dz ~exp(a²/2)/a`, with `a=sqrt(2log N)`, give the second moment `N/sqrt(pi log N)`. The crude upper bound divided by this asymptotic expression is 2 log N. The E3 output agrees with these formulas; convergence of the moment and tail ratios is slow, as expected.

### Lines 134–145: Remark 2, compatibility with the quoted upper bounds

**VERIFIED as a compatibility check and conditional quotation, not a new proof of the upper bounds.**

For (i), fix a finite nonzero θ* on a fixed support s0>=1. In a centered orthogonal design, `||mu||²=(n−1)||theta*||²<=nM` with M=||theta*||², and `||theta*||²<=nM'` with M'=||theta*||²/3 for n>=3. The all-null orthogonal witness is satisfied eventually and `s0+1<=K` eventually. With `p=min(n−1,floor(n^a))`, 0<a<=1, R1 holds with A=1, and `log p/log n→a`, including a=1. Every nonempty Gram submatrix normalized by n−1 is identity, so the anchored bounded-size and logarithmic-size floors hold with phi0=g0=1. Empty index sets impose no additional floor restriction. Fixed nonzero coefficients give `theta_min² n/(sigma² log n)→infinity`, the stated BM-infinity condition. Thus all the listed Theorem 1 hypotheses, not just Proposition A, are available.

For (ii), take fixed raw nonzero coefficients on a fixed finite support and independent iid standard Gaussian raw columns, with noise independent of the design. Centering a raw null column gives a Gaussian with covariance C, whose direction is uniform in `1^perp`; different columns remain independent, and the directions are independent of the raw truth block and epsilon. Since θ*=D_x β* is determined by the truth block, conditioning on that block and θ* preserves the spherical witness law. On the event that all truth-column sample standard deviations are at most 2, `||theta*||²<=4||beta*||²=M'`. The triangle/Cauchy–Schwarz estimate gives `||mu||²<=s0(n−1)||theta*||²`, proving E with fixed envelope M=s0 M' (the smaller n-dependent expression in the text may simply be bounded by this fixed number). The event has probability tending to one by fixed s0 and convergence of the finitely many sample variances. Rank is at most fixed s0, and polynomial p gives both logarithmic restrictions.

POST §2 line 63 permits polynomial p with A=max(a,1). For Corollary 1R, Sigma=I gives all population floors exactly 1, so its LSF conditions hold with phi=1 and psi_n=1, including `sqrt(n)/(log n)^(3/2)→infinity`. Fixed raw nonzero β* has fixed positive minimum and finite maximum on S0, satisfying the coefficient premise of Corollary 1R(a); its conclusion supplies the common sample floor and beta-min events. Thus the Gaussian example is within the quoted random-design bridge even for a>1. The upper bound is correctly quoted, and its proof was not re-audited here. Combined with A1, these quotations imply the conditional two-sided rate reading in STATEMENT Remark A3. The expectation upper-rate qualification in STATEMENT lines 86–87 remains explicitly conditional on the named POST2 claim and its design-event probability; it is not proved or silently used by either assigned file.

### Lines 146–152: Remark 3, numerical claims

**VERIFIED as descriptions of the recorded numerical evidence.** Orthogonal V1 evaluates the Gamma integral and symmetric-polynomial recursion against exhaustive enumeration of all admissible models on small designs; its worst recorded and rerun relative error is 1.37e−13. The truncated size sum has nonnegative omitted terms in exact arithmetic, and the proof correctly disclaims certified numerical enclosures. V2 checks the size omission and quadrature convergence on the listed examples. Spherical V1 compares the exact one-step formula with generic score ratios and reruns at 1.7e−13 worst relative error. In the reduced spherical simulation the orthonormal basis has s0+1 columns and the orthogonal centered complement has dimension n−2−s0, agreeing with its chi-square normalization for the full-rank Gaussian cases actually simulated.

The displayed spherical medians run from .968 to 1.089, consistent with .97–1.09 rounded. Orthogonal E1 medians run from 1.003 to 1.511, consistent with 1.00–1.51 rounded, with the largest-n p=n−1 entries 1.003 and 1.007. “Decreasing” describes the overall numerical trend rather than a proved monotonicity claim; the table is not strictly monotone at every n. E2 growing-support medians 1.373, 1.275, 1.260 and minimum .983 agree with the rounded description. The equicorrelated boundary script is correctly described as a one-step experiment outside the iid spherical hypothesis. None of these Monte Carlo observations is used as a proof of Proposition A or of an exact upper constant. The large simulations were inspected, not rerun in full.

## 3. Coverage of STATEMENT v1.2

| Statement item | Proof coverage and result |
| --- | --- |
| §0 definitions | Consistent with authorized POST §0; no redefinition of the coded target. |
| §1 Lemma S(1), lines 34–37 | S lines 18–35: VERIFIED, including equality and the arbitrary-J extension. |
| §1 Lemma S(2), line 38 | S lines 37–43 plus Lemma V: VERIFIED. |
| §1 Lemma S(3), lines 39–40 | S lines 45–52: VERIFIED with exactly the stated admissibility assumption. |
| §1 Lemma S(4), lines 41–42 | S lines 54–57: VERIFIED, with item 3's inherited admissibility. |
| §2 Proposition A, lines 48–69 | A §§1–5: VERIFIED under both witnesses, with coefficient/energy assumptions, rank dependence, uniformity and conditional transfer as stated. |
| Corollary A1, lines 71–73 | A §6 A1: VERIFIED, including the expectation lower bound and polynomial constant. |
| Corollary A2, lines 75–77 | A §6 A2: VERIFIED for both necessity conclusions. |
| Remark A3, lines 79–88 | A Remark 2 checks the two examples against the cited hypotheses. Conditional upper-bound readings remain quotations; no unconditional new upper or expectation-upper theorem is proved. The stated unsettled general upper-bound question is not answered by these proofs. |
| §3 Claim B and its consequences, lines 90–114 | No proof in these two files; assigned to `B_sparsity.md` by the statement and outside this brief. Lemma S is a dependency, not a substitute for that proof. |
| §4 Claim C and consequences, lines 116–143 | No proof in these two files; assigned to `C_counterexample.md` and outside this brief. |
| §5 exclusions, lines 145–150 | Consistent with the checked proofs. No sampler or general-design upper result is inferred. The exact orthogonal constant remains numerical evidence. The reference-cost/C remarks are outside these proofs. |

There are **no uncovered in-scope theorem items**. Claims B and C have deliberately not been certified by this review. No stronger hypothesis, such as fixed s0, an eigenvalue floor, or independence of a score from its common denominator, was needed in the proof of Proposition A.

## 4. Independent numerical checks

All checks below passed; full reproducible output is retained in the scratch directory.

1. Sphere constants and moments: 60-digit mpmath evaluation for d in {3,4,5,6,10,100,1000,100000}; τ in {.001, 2log 2, d/2}. Checked the Gamma interval, 2,424 pointwise two-sided density bounds, and 24 pairs of truncated moments. These include the minimum dimension and the exact τ=d/2 boundary.
2. Lemma R: the exponential and epsilon inequality chain on 100,001 points approaching both endpoints 0 and 1.
3. Lemmas V and S: 15,360 one-step pairs on iid, duplicated, nearly duplicated and rank-one standardized designs, for n in {3,4,5,8,20,80}, p=5. Included S empty and all subset sizes, including sizes beyond K to attack the algebraic iteration extension. Checked variational values, determinant identities/bounds, fit identities/bounds, and 9,280 admissible posterior-ratio lower bounds. Maximum relative determinant identity error 6.302e−12; maximum gain error divided by max(Q,1) 2.387e−15; maximum absolute residual quadratic identity error 3.064e−14. Tolerances were numerical, not theoretical relaxations.
4. Raw-response V and spherical rank-only estimates: 600 cases for n in {3,4,8,40,200}, with empty, iid, duplicated and nearly singular truth blocks. Checked the raw V estimate, the spectral second-term bound, the projected residual lower bound for Q, the final ratio estimate for 1−kappa', and `n−1−r0>=n/2`. Rank-zero and coefficient norms of order n were included. A few finite-n chi-square probability bounds exceed 1, which is harmless; these are asymptotic proofs and do not require positive lower probability estimates at every small n.
5. Fresh reruns of existing F1, spherical V1, and orthogonal V1 reproduce their recorded errors and PASS results. Existing Monte Carlo tables were cross-checked against the narrative, but not treated as uniform or asymptotic proofs.

Final finding counts: **FATAL 0; MAJOR 0; MINOR 0; NIT 0.**
