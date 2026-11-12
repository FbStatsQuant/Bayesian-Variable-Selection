LOCK-WITH-AMENDMENTS

Findings: FATAL 0; MAJOR 1; MINOR 2; NIT 0.

Scope: blind first read of the brief and its six listed source files only. No proof files, plans, logs, numerics, or other reviews from W3-PSHARP were consulted. All locations below refer to Theory_work/Wave3/W3-PSHARP/STATEMENT.md unless explicitly qualified. The permitted scratch computation is reviews/L01_scratch/check.py. No parent theorem was independently audited beyond the allowed statements and definitions.

## Findings

### MAJOR M1 — B3 omits the hypotheses needed for its asserted growing-sparsity rate obstruction

Place: STATEMENT.md:100-104 (especially lines 101-103).

Claim A concerns N_n selected null columns and supplies a lower bound proportional to
(s0+1) [2N_n/(2p-1-s0)] sqrt(log N_n/n).
It does not, merely from the presence of its witnesses, supply the displayed lower rate (s0+1)sqrt(log p/(pi n)). That substitution is justified by A2's all-null and s0/p -> 0 hypotheses. Even under those additional hypotheses, failure of the rate r_n when s0 -> infinity requires a comparison between log p and log n. Proposition A permits log p = o(log n). The assertion that growing s0 alone rules out r_n is therefore false as written.

For a concrete counterexample to that last assertion, take orthogonal columns, s0=floor(log log log n), p=s0^2, all p-s0 nulls as witnesses, and theta_j=1/sqrt(s0) on the truth. Work for sufficiently large n. Energy is at most n, coefficient norm is one, and s0/p -> 0. The maximal squared null-noise coordinate is O_P(log p); exact orthogonal scores then bound the total overfit odds by n^(-1/2) times a fixed power of s0 and p on events of arbitrarily high probability. Underfit scores lose order n/s0 in their log likelihood, dominating the O(p log n) model/prior penalties. Consequently delta_n = o_P(sqrt(log n/n)), despite s0 -> infinity. This also lies within the recorded sparsity target. The example is an analytic counterexample, not a finite-n numerical claim.

Exact correction proposed: replace the first two sentences of B3 with:
“On the witness sequences of Corollary A2 with log p asymptotic to log n up to fixed positive factors, the recorded growing-s0 target cannot retain the rate r_n when s0 -> infinity. On those sequences a concentration theorem must allow at least the rate (s0+1)sqrt(log p/n), and consistency requires s0=o(sqrt(n/log p)). For a general witness block use Lambda_n in Proposition A.”
Retain the final every-design obstruction with the domain in line 95 made explicit.

### MINOR m1 — the limit for c(p,0) needs p -> infinity

Place: STATEMENT.md:93, final clause.

The statement c(p,s0)/(s0+1) -> 1/2 when s0/p -> 0 is false for the allowed empty truth with bounded p. For p=2 and s0=0 at every n, the premise holds identically but the ratio equals 2/3.

Exact correction proposed: “c(p,s0)/(s0+1) -> 1/2 when p -> infinity and s0/p -> 0.” The finite-n bounds are correct. This was checked algebraically; no simulation is needed.

### MINOR m2 — the orthogonal example has an infeasible endpoint

Place: STATEMENT.md:79.

At a=1 the prescription p=floor(n^a)=n contradicts the stated p<=n-1: centered, nonzero, mutually orthogonal columns live in a space of dimension n-1.

Exact correction proposed: prescribe p=min(n-1,floor(n^a)), 0<a<=1. This leaves log p/log n -> a, all floors, and the resulting sharpness constant unchanged. Checked by dimension counting.

## Claim-by-claim checks and derivations

### Lemma S, items 1-4 — derived; items 1-2 and the implied odds bounds tested numerically

For A=G_S+I, H=(n+1)G_S+I, a=g^T A^(-1)g and b=g^T H^(-1)g, the two Schur complements are n-a and n^2-(n+1)^2 b. They are strictly positive since the enlarged matrices are positive definite, including at rank-deficient designs. This yields exactly the determinant ratio in item 1 and 0<s<=n^2.

To check the improved n bound and equality condition, diagonalize G_S. The scalar coefficients of (n+1)^2 H^(-1)-n A^(-1) are
[(n+1)lambda+n^2+n+1]/[((n+1)lambda+1)(lambda+1)] > 0.
Thus s<=n(n-a), strictly unless g=0. Equality is precisely x_j perpendicular to col(X_S). Iteration gives the multicolumn assertion (the matrix definitions themselves extend to every subset, even if the posterior cap makes a subset infeasible).

Block inversion of H gives the fit decrement n(x_j^T rho_tilde_S)^2/s. The residual score is nonnegative: on a singular direction with Gram eigenvalue lambda, its fitted eigenvalue is n lambda/((n+1)lambda+1)<1. Items 2 and the signs follow.

The exact prior ratio is (s0+1)/(2p-1-s0). Positivity of 2b0+Q makes gamma in [0,1); the likelihood ratio is (1-gamma)^(-nu), and -log(1-gamma)>=gamma. Summing distinct feasible one-step supersets proves items 3-4. The lemma's stated cardinality premise must continue to apply when setting S=S0, as its present layout indicates.

### Proposition A — derived asymptotically; no numerical test of its probability limit

The constant 1/sqrt(pi) and the factor 2N_n/(2p-1-s0) are correct. If Z is standard normal, truncation at |Z|<=sqrt(2 log N) gives exactly
E[exp(Z^2/2) 1{|Z|<=sqrt(2 log N)}] = 2 sqrt(log N/pi).
Its second moment is O(N/sqrt(log N)); independent truncations concentrate relative to their mean. One can first truncate at sqrt(2 alpha log N), alpha<1, and then let alpha approach one, which suffices for every fixed epsilon in the proposition.

For W-orth, unstandardized residual inner products with the witness directions are independent sigma* Z_j. The exact reference representation gives Q^raw_S0 <= ||C epsilon||^2+M+M', uniformly; also s_y^2=O_P(1). Hence nu gamma_j >= (1-o_P(1/log N))Z_j^2/2, since N<=n and Gaussian norm fluctuations are O_P(n^(-1/2)). Multiplying the truncated sum by the prior/determinant factor in S.4 yields Lambda_n.

For W-sph, condition on the raw response and its ridge residual r. Witness inner products are independent sphere coordinates. Writing A0=(n+1)X_S0 H_S0^(-1)X_S0^T, the difference Q^raw_S0-||r||^2 is the quadratic form with matrix (1+1/(n+1))A0-A0^2. The reference ridge penalty bounds its mean contribution, and its Gaussian contribution is O_P(s0+1). Also ||r||^2 is of order n uniformly, since rank(X_S0)<=s0=o(n). Therefore the exponent coefficient differs from one by O_P((s0+1)/n). The sphere density agrees with the normal density uniformly through squared coordinate size O(log N) when (log N)^2=o(n). The extra error in the exponent vanishes under (s0+1)log N=o(n). The same truncated-sum argument applies conditionally.

These estimates are uniform with the stated constants, common little-o envelopes, and lower envelope for N. Conditional transfer follows by conditioning and adding the probability of the exceptional event. The spherical construction genuinely allows p>>n: iid directions need not be orthogonal, and N (or p when all nulls are used) may be polynomial in n, or larger subject to the logarithmic restrictions. The phrase “any p” in its example must be read together with those explicit restrictions on the chosen witness block.

### Corollaries A1 and A2 — derived

A1: N=p-s0 gives 2N/(2p-1-s0)->1 and log N/log p->1. The witness hypotheses force log p/n->0. Convert odds to delta by x/(1+x); since the deterministic comparison tends to zero, the same lower bound holds for delta. Restricting the expectation to the high-probability lower-bound event proves the stated liminf without a uniform-integrability assumption.

A2: with s0/p->0 the same simplification holds. A lower bound in probability on the odds forces (s0+1)sqrt(log p/n)->0 under consistency. Combining it with delta=O_P(r_n) and log p comparable to log n forces s0=O(1). These are necessary conditions only, as stated.

### Remark A3 — derived subject to m2 and the cited parent results

For the corrected orthogonal example, energy is bounded with fixed truth coefficients, normalized floor one and unnormalized floor at least one; BM-infinity holds. R1 permits A=1. For iid Gaussian raw columns and fixed polynomial p, Sigma=I satisfies both population floor conditions of Corollary 1R. Raw coefficients bounded above and away from zero transfer on its design events, giving the claimed joint-law conclusion and W-sph conditional on the true block. For the expectation statement one also needs the bad-design-event term in P2S Claim C to be O(r_n); iid Gaussian restricted Gram concentration gives exponentially small failure after a union bound over O(log n)-sized subsets, whose logarithmic count is O((log n)^2). Thus the expectation assertion is justified in these examples, not just by an unquantified P(event)->1 statement. No other cited report or external proof was read.

### Corollary B — derived and tested numerically; final limit needs m1

For j added columns, iteration of S gives determinant penalty at least n^(-j/2), and the fit ratio is at least one. The total number of distinct additions is C(p-s0,j). Its product with w(s0+j)/w(s0) equals
C(s0+j,j) product_{i=0}^{j-1} (p-s0-i)/(2p-1-s0-i).
This proves the full finite sum. The first term gives c(p,s0)/sqrt n and pi(S0)<=sqrt n/(sqrt n+c).

For s0<=p/2, 3(p-s0)>=(2p-1-s0). For s0>=1 the ratio c is minimized at p=s0+1, where it equals one. For s0=0 it equals p/(2p-1)>1/2. These prove all finite-n constants. In particular, the bound contains LB on LB's full domain, without requiring s0<=p/2, and strengthens n+1 to n.

B1: derived pathwise from a deterministic bound, so “surely” is justified, including the asserted zero limit. The sparsity sequence here is deterministic. Convergence along a subsequence imposes the necessary sparsity condition along that subsequence.

B2: derived. From delta>=a/(1+a), a=(s0+1)/(3sqrt n), delta=O_P(rho_n), rho_n->0, first obtain a->0 and then a=O(rho_n), since a is deterministic. Thus s0+1=O(sqrt n rho_n); the two specializations follow. If random support sizes are intended in a later extension, these deterministic O/o conclusions must instead be O_P/o_P.

B3: not verified as written; see M1.

### Proposition C.1 — derived; reference cost tested numerically

The vectors exist by k+1<=n-1 for n>=200, and k+2<=floor(n/2) on that range. The lower bound on b_n is feasible eventually for every fixed positive sigma* and bbar; the finite-n assertions are conditional on that lower bound, not a claim that it is feasible at n=200.

The displayed coefficients give x1-x2/c=eta u and therefore represent mu exactly. Their squared norm is b_n^2(1+c^(-2))/(eta^2 k), so the claimed lower bound holds. The imposed signal condition makes ||theta||^2/n diverge.

In the orthonormal observation basis x1/sqrt(n-1), u/sqrt(k(n-1)), the reference matrix is
B=sqrt(n-1) [[1,c],[0,-c eta sqrt k]].
Minimized reference cost is mu^T[I-n B(I+(n+1)B^TB)^(-1)B^T]mu. Its value along the second basis vector is at least half the squared signal norm (the direct inverse formula gives a ratio close to one). Taking zero coefficients supplies the upper bound. Taking the true coefficients in T' gives cost exactly b_n^2. All other hypotheses of L1a' are retained for reference T. G does not require reference T to equal the support of the generating parameter.

### Proposition C.2 — derived and tested numerically

The prior layer ratio q_(l+1)/q_l=(p-l)/(2p-1-l)<=a:=p/(2p-1). Thus
R_m^T <= C(2p-1,2) a^(m+1)/(1-a).
With k=ceil(12 log n), m=floor(k/2), this is <=n^(-2) for n>=200. For example a^(m+1)<=exp(1/3)2^(-k/2); the resulting bound is at most 3p^2 n^(-6 log 2), whose n^2 multiple is below one at n=200 and decreases thereafter. Since m>=2, this proves the reference cutoff bound directly from its definition.

Using tr(G_T)=2(n-1) and det(G_T)=(n-1)^2 c^2 eta^2 k gives
D_T=[1+(n+1)tr(G_T)+(n+1)^2 det(G_T)]/[1+tr(G_T)+det(G_T)] <=4n.
Consequently A_m^T<=2/n<=n^(-1/2). The intentionally loose constants suffice.

### Proposition C.3 — derived asymptotically; no exhaustive numerical test at its logarithmic p

Put E=||mu||^2=(n-1)b_n^2 and V=sigma*^2+bbar^2. A model of size at most m observes at most m of the k orthogonal signal directions directly. Even allowing both proxy columns, their residual weak direction has ridge fitted eigenvalue O(k/n^2). Uniformly over such models, signal ridge loss is therefore at least (1/2-o(1))E. The T' signal ridge loss is O(b_n^2).

Every model lies in the same p-dimensional column space. With probability tending to one, ||P_col(X) epsilon||^2=O(k). Cauchy-Schwarz controls all noise-signal cross terms simultaneously by O_P(sqrt(E k)); the differences of pure-noise quadratic forms are O_P(k). Since E>= (1-o(1))1200 V(log n)^2 and k=O(log n), these errors are o_P(E). Uniformly, Q_S^raw-Q_T'^raw>=E/3 eventually with probability tending to one. On the same event 2b0 s_y^2+Q_T'^raw<=3Vn.

The likelihood ratio to T' is consequently at most exp(-E/(20V)) for all these models, eventually. Determinants cost at most n^(k/2), by Lemma S starting at the empty model. The sum of prior ratios is at most 2^(3p), since w(S)/w(k)<=C(2p-1,k)<=2^(2p-1). Therefore
pi(|S|<=m) <= exp[(k/2)log n+3p log 2-E/(20V)]
with probability tending to one. The signal threshold with C_b=1200 absorbs the positive terms with ample margin, yielding, for example, an eventual bound exp(-E/(40V)). Since E/(n b_n^2)->1, this proves the existence of c1 in item 3. This is a mathematical derivation, not an assertion of a finite-n probability bound at n0.

By C.2 the reference normalizations tend to zero (for L1a', at most (1+1/n)n^(-1/2); for 1a'', at most 2/n), whereas the tails tend to one. Both Theta quantities diverge in probability. Thus the stated parent conclusions really do fail when the corresponding reference coefficient/cost hypothesis is removed. To refute a proposed cost allowance B_n/(log n)^2->infinity, choose n b_n^2 a sufficiently large fixed multiple of V(log n)^2: the reference cost is then below B_n eventually and the same failure persists. The counterexample concerns reference T; it does not contradict either parent at the bounded-cost reference T'.

## Numerical verification record

Ran py -3.13 -I on the scratch script. Exact model enumeration used n in {6,9,16}, p in {2,4,6}, twelve independent draws per pair, including duplicated columns on every third draw. All 6,576 one-step comparisons passed. Maximum absolute determinant-identity error: 1.39e-13; maximum fit-identity error: 5.78e-15. The largest full B lower-bound/exact-odds ratio was 0.976369, below one.

Checked C's exact combinatorial tail and stable two-dimensional reference calculation for every integer n from 200 through 20,000 and n=100,000, 1,000,000, 1,000,000,000. Maximum R_m n^2: 0.000519285; maximum A_m/(2/n): 0.000260013; minimum minimized-reference-cost/E: 0.9992046. A first direct inversion in coefficient coordinates became numerically singular at the largest n; the scratch script was corrected to use the observation-coordinate inverse and explicit trace/determinant formula. No numerical failure was interpreted as a mathematical counterexample. These checks support, but do not replace, the derivations above.
