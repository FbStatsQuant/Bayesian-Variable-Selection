# R03 — adversarial lemma check: X1, X2, X3

Scope: locked W2-FAC-X STATEMENT v3; the three requested lemma files, with FACB D0 and L1/L3/L4 as context. Line numbers refer to the versions inspected for this review. No source lemmas or locked statements were changed.

Verdicts:

- **X1: VERIFIED-WITH-AMENDMENTS.** The stated scalar independence, RSS/reference identities, and gain formulas (g1)–(g5) survive checking. Correct the conditional-independence wording described below.
- **X2: VERIFIED-WITH-AMENDMENTS.** The perturbation bound and one-null-move corollary hold, including bounded p. The probability proof and its quantifiers need the minor repairs below.
- **X3: FAILED as written.** Claim (iii) contains a false direction-independent distance bound and a false strict inequality. Explicit one-step counterexamples satisfy the stated hypotheses. The weaker crossing-width conclusions, and the subsequent prefix/containment mechanism, survive the proposed repair.

No FATAL issue found. The MAJOR issue is X3 issue 1. These findings do not by themselves refute the locked theorem; this review does not certify X4 or its use of these lemmas.

## X1 — VERIFIED-WITH-AMENDMENTS

1. **MINOR — X1.1 proof, lines 25–30: ambient residual is not independent of the random direction.**

   The sentence asserting that f_perp is independent of e1 is false when f_perp is regarded as an ambient n-vector. Conditional on e1 its covariance is C − e1 e1^T, which depends on e1; also f_perp is constrained to be orthogonal to e1. The analogous residual vectors live in the random space V3. This does **not** invalidate the scalar/Wishart independence in the lemma statement.

   **Fix:** state that, conditional on e1, eta and f_perp are independent, and that the conditional joint law of (eta, phi) is the product N(0,1) times the chi radius law and does not depend on e1. Conditional on the frame (e1,e2), the coordinates of the u residuals in an orthonormal basis of V3 are independent standard Gaussians. Their Gram law and its independence of (xi,a) do not depend on the frame. This proves exactly the claimed independence of (||e||,eta,phi,xi,a,W), without asserting independence of the ambient vectors from the frame.

Checked claims and constants:

- **X1.1 statement:** the dimensions n−1, n−2 and N=n−3 are correct. Norm/direction independence and the frame-conditioned Gaussian decomposition give all stated scalar laws and the independent W_p(N,I) law. The rotation is defined almost surely for sufficiently large n; eventual p<N follows from the locked hypotheses.
- **X1.2(a)–(c):** verified. The raw Gram is (1−rho)(A+v1 v1^T), and the cross-product with e1 is sqrt(1−rho)v1. Sherman–Morrison gives q/(1+q). The Schur difference is omega_j squared, with positive sign. Subtracting residual norms yields the two denominator factors in (c). The null condition is essential and is imposed.
- **X1.3:** verified, including both drift identities. The offset is kappa ell eta = varrho; the inverse has diagonal N^−1(1−gamma_k). The square-root normalization of omega is correct, including its sign. The reference identity is an exact substitution, not an approximation to the realized score.
- **(g1):** verified for sufficiently large n. The principal-minor determinant identity gives the displayed inverse-diagonal ratio with the stated sign. The inverse comparison and logarithm bound justify 3/[c0(n−1)].
- **(g2):** verified. The ridge Schur statistic has factor n/(n+1). Compare the absolute values of the signed normalized coefficients to handle possible sign changes at zero. The coefficient perturbation is O(n^−2), the normalized perturbation is O(n^−3/2)(1+sqrt(P0)), and squaring gives the claimed O(n^−3/2)(1+P0) absolute remainder. A particularly direct uniform coefficient bound is ||b(0)|| <= ||y||/sqrt(lambda_min(G)) <= c0^−1/2; this avoids any concern about importing a fixed-design coefficient bound. On X2's event the asserted raw scale bound also gives ||theta*|| <= 2||vartheta||.
- **(g3):** verified. Exactly epsilon_d=omega_j^2/(1+q_{T−j}), hence it is nonnegative and at most omega_j^2 (the stated factor 2 is safe). With R_e=||e||^2/s^2, one has psi=R_e/(1+q)+d, 0.02<=d<=1.1 eventually. Consequently

      M_T = [nu n/((n+1)N)] / [(1+q)(1+d(1+q)/R_e)].

  Here the bracket in the numerator is (1/2)(1+O(1/n)) and R_e>=c n. This proves the upper bound and even a lower bound (1/2)(1−q−C/n), stronger than the stated lower bound. P0<=C tau_hat^2 and psi>=c n give the stated n^−5/2 remainder. The determinant error enters with minus one half, as written.
- **(g4):** verified. Negating the deletion gain at T union {l} and applying log(1+u)<=u is valid even if the ridge approximation remainder is negative, because the exact logarithm argument is positive. The transformed reference statistic and the identity yielding 1−gamma_{k+1} are correct.
- **(g5):** verified. The determinant difference and gain signs agree with D0. The common base T−j=T'−l gives Q_T−Q_T'=(Q_base−Q_T')−(Q_base−Q_T). Also q_T−q_T'=omega_j(T)^2−omega_l(T')^2, so the multiplier ratio is 1+O(max omega^2). The reference algebra expands to (1−gamma_k)tau_l^2+2gamma_k tau_j tau_l−(1+gamma_k)tau_j^2, exactly V_jl. Since k>=s0+1>=2, 1+gamma_{k−1}<2. The reference incoming statistic at T' is the convex combination (1−gamma_k)tau_l+gamma_k tau_j, hence is at most 3 Hbar under the stated envelopes. Comparing squares gives the safe coefficient 12 Hbar for the linear delta terms. The quadratic coefficient 4 and the looser C Hbar^4 max(omega^2) remainder are safe eventually (Hbar>=1). Multiplying the ridge remainders by nu/(M psi)=O(1) gives the stated n^−3/2 remainder. The Hbar envelope is required for that remainder, as in the final qualification of (g5).

## X2 — VERIFIED-WITH-AMENDMENTS

1. **MINOR — D6 proof, lines 39–42: grid cardinality and binomial law.**

   The inequality 2 Hbar/w+4<=5n is false at w=1/n, since Hbar grows even for bounded p. Also the count over null indices has law Bin(m_all,q), not Bin(p,q); Bin(p,q) is a valid stochastic upper bound.

   **Fix:** use O(n(Hbar+1)) grid cells, at most O(n sqrt(log n)) under (P-1/2). The union failure probability is O(sqrt(log n)/n^2), still vanishing. Say explicitly that the null count is dominated by Bin(p,q). The Chernoff threshold in the proof is at most the displayed D6 bound, so the extra factor 2 in D6 is safe.

2. **MINOR — D6 definition/lemma, lines 20–24: fix the width quantifier unambiguously.**

   The leading wording “for w in [1/n,1]” looks simultaneous, whereas the parenthesis and Lemma X2.1 explicitly assert one deterministic width at a time. The proof establishes the latter. A countably infinite collection cannot be justified by the displayed single-width union bound alone.

   **Fix:** define E_n(w_n) for any specified deterministic sequence w_n in [1/n,1], or intersect over the finitely many deterministic multiples of varpi_n actually needed later. Each such intersection has probability tending to one. A simultaneous-in-width version would need an additional argument (e.g. a dyadic grid). No randomness of the path endpoints is a problem: the interval locations are already uniform for a fixed width.

3. **MINOR — Proposition step (v), lines 97–98: displayed estimate is false for small bounded p.**

   (#Band+17)<=2p is not true, for example at p=2 and empty band. This is a proof-line error, not a counterexample to Proposition X2.

   **Fix:** use #Band+17<=p+17<=18p for p>=1. Then (p+17)sqrt(log n/n)=o(1) uniformly for p<=n^{A1}, A1<1/2, including bounded p.

4. **MINOR — deductions after the event, lines 44–48: incomplete citations for the standing assumptions.**

   Bounding raw column scales uses D4 as well as D1–D3, since the e1 component contains xi. The displayed paragraph also does not explicitly supply s^2 bounds, though it says these are the standing assumptions of X1.4. FACB's exact-Gram version is not a literal random-design proof.

   **Fix:** cite D1–D4 and add the finite-support calculation. On this event, G^r_{S0,S0}/(n−1)=Sigma_{S0,S0}+o(1), uniformly for the fixed-size support, and e^T mu/(n−1)=O(Hbar/sqrt(n))=o(1). Thus s^2=sigma^2+vartheta^T Sigma_{S0,S0}vartheta+o(1), a positive finite limit; choose fixed lower and upper bounds accordingly. Also omega_j(T)^2<=q_T by the Schur identity. These supply the missing explicit deductions without enlarging the event.

Probability audit:

- **D1:** the singular-value tail is 2/n at t=sqrt(2 log n). Writing u=(sqrt(p)+t)/sqrt(N), the two eigenvalue deviations are bounded by 2u+u^2<=3u eventually. The constants in r_n are sufficient.
- **D2:** Laurent–Massart with t=2 log n gives diagonal deviation at most 2 sqrt(2 log n/N)+4 log n/N<=3 sqrt(log n/N) eventually, with failure at most 2p/n^2. This also gives the norm bound 2N. Off-diagonal conditional tails at sqrt(6 log n) have failure at most 2p(p−1)n^−3; on the norm event their magnitude is at most sqrt(12N log n), below the stated constant 4. Use p^2<=n eventually under A1<1/2.
- **D3:** the chi-square deviations have exponentially small failure on the n^{1/3} scale (the one-degree difference between E phi^2=n−2 and N=n−3 is negligible). The eta failure is at most 1/log n eventually, and the a-coordinate union is at most 2p/n^2.
- **D4:** the Hbar union bound is at most 1/log n; the fixed support contributes at most s0/log n. This includes m_all=0, with empty null conditions interpreted vacuously.
- **D5 conditioning is legitimate.** To make the argument fully explicit, first condition on the frame as well as (u_j^perp,xi). In that frame all residual columns other than j are independent standard N-dimensional Gaussians independent of xi. The conditional law of (W_jl)_{l!=j} is a product Gaussian with variance ||u_j^perp||^2, a law independent of the frame. Integrating out the frame retains this conditional law. Every A excludes j; there is no hidden diagonal term. The family depends on xi alone, not on W. Its cardinality is at most (p+1)^2+1, and the two sums need no mutual independence for the union bound. The stated 32 n^−3 bound is safe. Arbitrary real endpoints in the proposition select the same consecutive runs as endpoints chosen among adjacent observed null coordinates and infinities; thus D5 covers them too, almost surely with distinct coordinates.
- **D6:** valid with issues 1–2 repaired. Do not condition the binomial calculation on D4: bound the deterministic grid failures unconditionally, then add P(D4^c).

Proposition audit, with h=Hbar+|x_T| and t=sqrt(log n/n):

- **(i):** the denominator 1+||b||^2>=c_rho k absorbs the k from both perturbations of S(b). The coordinate and norm errors are C_rho t h and C_rho sqrt(k)t h. No stochastic cancellation involving a is needed.
- **(ii):** the remainder is bounded by C h[p^{3/2}/n+sqrt(p)log n/n]. The first term is at most sqrt(p/n) when p<=sqrt(n); the second divided by sqrt(p log n/n) is sqrt(log n/n). Both fit the claimed budget, also for bounded p.
- **(iii):** the common rank-one term is O(r_n h), with no remaining sqrt(k), because ||b||>=c_rho sqrt(k). This fits sqrt(p log n/n)h.
- **(iv):** D5 controls the full-row sum minus an interval-row sum. D2 controls every arbitrary exceptional/band change individually, so membership may depend on W. The error is at most C h[sqrt(p log n/n)+(#Band+17)t]. There is no illicit conditioning on the path set.
- **(v):** the diagonal resolvent error is O(r_n). Perturbing b contributes O(t/k) to b_j^2/(1+||b||^2). The reference diagonal stays above a positive rho-dependent constant, so the square-root denominator is uniformly safe. Together with the corrected bounded-p estimate, the numerator is at most 2h eventually and the normalization error is O(r_n h). All terms fit one C_X, with no n- or p-dependence in that constant.
- **Corollary:** the symmetric-difference argument is valid for null deletions/additions/swaps: exceptional sizes become at most 16 or 17, and S0 is retained. A deletion down to S0 does not require a null statistic at that resulting set; every incoming statistic or null statistic actually used has size at least s0+1. The absorption remark follows from p Hbar sqrt(log n/n)->0 and the n^−1/3 floor as claimed.

## X3 — FAILED as written

1. **MAJOR — claim (iii), lines 26–28, proof lines 49–54: wrong side for a left deletion, and an unjustified strict inequality.**

   Take varpi=1, kappa'=2, K0 consisting of the three coordinates {0.1,−2.1,−10}, B=12, I=1, and delete −2.1. Then x0=0 and x1=0.525. The retained point 0.1 lies strictly between the two centres, so this is a crossing. The deletion rule holds with equality: 2.1=d0+2 varpi, d0=0.1. Nondegeneracy holds for every coordinate at both centres. But L0=2.1, whereas the claimed upper bound is 2/(3−2+2)=2/3. Thus the claimed L_i bound is false under the stated hypotheses. The phrase “the other case is symmetric” changes L to R; it cannot prove the displayed direction-independent L bound.

   Independently, reflect this configuration: coordinates {−0.1,2.1,10}, B=−12, delete 2.1. Then x0=0, x1=−0.525, L0=0.1, R0=2.1, and omega0=2.2=2 L0+2 varpi. This is another legitimate crossing satisfying the rule with equality. The claimed strict inequality omega_i<2 L_i+2 varpi fails even for a right deletion. The proof itself only derives <= at line 53.

   **Fix:** formulate the direction-specific result with D_i^opp=L_i for a deletion above x_i and D_i^opp=R_i for a deletion below x_i:

       D_i^opp < 2 varpi/(|K_i|−2+kappa'),
       omega_i <= 2 D_i^opp + 2 varpi.

   Equivalently, the side-free version can use d_i: crossing forces the opposite-side distance to be the smaller one. Indeed, the deleted-side distance is at least (|K_i|−1+kappa')D_i^opp>D_i^opp. Hence d_i=D_i^opp. The corrected claim is therefore

       d_i < 2 varpi/(|K_i|−2+kappa'),
       omega_i <= 2 d_i + 2 varpi.

   Both desired strict width conclusions still follow: omega_i<4 varpi when |K_i|>=3, and omega_i<c(kappa')varpi generally. No constant enlargement is necessary. The supplied n3x_softgap.py tests the weaker width bound, not either false subclaim, explaining why its numerical result cannot certify (iii) as written.

2. **MINOR — setting line 13 versus (i), lines 24 and 44: terminal empty set is permitted.**

   The setting requires nonempty K_i only for i<I, but (i) asserts a nonempty side at all states and its proof assumes K_i is nonempty. For example, N={1}, xi=1, B=0, kappa'=2, I=1, deleting its sole point satisfies the exact rule and nondegeneracy. At i=1, K1 is empty, a1=−infinity, b1=+infinity, and neither side is nonempty.

   **Fix:** qualify that sentence of (i) by K_i!=empty, or restrict its domain to i<I (and to terminal states with nonempty K_I). If full exhaustion is retained, define the empty-state hole as the whole line. The containment and sparse conclusions then remain meaningful and true at the empty state. This issue does not affect (vii)–(viii), whose size assumption prevents an empty terminal state for a nontrivial prefix.

Remaining deterministic claims, after the correction to (iii):

- **(i)–(ii):** definitions and the approximate-minimum rule give the asserted empty kept gap and deletion band; only the terminal qualification above is missing.
- **(iv):** verified. No crossing plus nondegeneracy rules out a kept point at or between the two centres. Deleting above preserves the lower endpoint and can only increase the upper endpoint; deleting below is symmetric.
- **(v)–(vi):** verified for the actual step range i<I. The corrected strict width bound excludes crossings at width >=4 varpi with at least three kept points. Induction gives nesting, and (ii) then gives the closed 2 varpi band for all intervening deletions.
- **(vii):** verified for arbitrary prefixes. The denominator |K0|−Q−1+kappa' is positive since Q<=|K0| and kappa'>1. If M>=Q+1, precisely Q+1 deletion steps 0 through Q exist and are narrow; only Q increments are needed to bound their pre-deletion centres. Their distinct deleted points lie in a common interval of length 8.2 varpi, contradicting the definition of Q. Once M<=Q is established, the same increment bound includes x_M. Nothing beyond the supplied prefix is used.
- **(viii):** verified. Before M, endpoint/centre comparisons actually leave at least 0.1 varpi slack relative to the 4.3 varpi band. After M, nesting transports the initial deleted cluster, and (vi) covers all later deletions. The reverse inclusion follows directly from the empty kept gap. For varpi=0, i0=M=0; exact deletions cannot cross, and distinctness excludes deleted points from the kept endpoints, supplying the strict open containment even though a positive band margin is unavailable.
- **(ix):** verified. Minimal spacing contradicts the corrected general crossing-width bound. Nesting and (ii) leave at most 2 varpi overshoot at either endpoint; spacing excludes every distinct deleted point from those endpoint bands. The argument works with one-sided gaps and with two or one kept points. At full exhaustion use the empty-state convention from issue 2.

## Independent computational checks

Ran inline Python 3.13 with NumPy, without creating scratch artifacts. Both explicit crossing configurations above reproduce the violations. An independent Gaussian sufficient-statistic construction at n=2000, p=7, rho=0.6 gave Schur q-difference residual 1.36e−20 and zero numerical residual for the exact swap gain/logarithm identity. A 10,000-case randomized expansion of the reference swap identity had maximum absolute residual 3.56e−15. These are algebra checks/evidence only; the verdicts above rest on the proofs and exact counterexamples.
