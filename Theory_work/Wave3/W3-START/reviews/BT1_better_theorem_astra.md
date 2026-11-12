MANIFEST b3fafa79685f4562886d5e268432b95eba30fc75075cc50eaa30591e3546b7b2

Independent better-theorem review BT1. The 33 file hashes in the manifest match the worktree. These are proposed improvements, with proof sketches, not certifications of the currently unproved target. No prior review was read.

## P1. Replace the correlation-matrix floor by a constant unnormalised Gram floor

- **Statement.** In START-F (T1), replace (FL-16) by

  (GF-16) There is a fixed g_* > 0 such that lambda_min(X_T'X_T) >= g_* for every nonempty T with |T| <= 16.

  Keep (E), visibility and (AL). Retain the conclusions and exponents of (T1)(a)-(d), with constants depending on g_* instead of phi_0. The same substitution applies to the fixed-design NEC and OVL claims and the transfer hypothesis in (T3)(a). For F2 retain its **separate** floor on Rhat_{S0}; GF-16 alone does not supply its lower bound on unexplained signal. Replace [TK] by the same concentration events and an O(1) score-remainder bound with a new constant; do not claim the old numerical remainder constant survives.

- **Why strictly better.** The existing hypothesis demands lambda_min(G_T) >= (n-1)phi_0^2. The proposed one allows correlation eigenvalues of order 1/n, including the near-twin scale of numerics (e), with the same rates. This weakens the floor on every small set, not just null-only sets. All old admissible arrays satisfy GF-16 eventually. It retains polynomial p, including p >> n, and uses no partition hypothesis beyond the coded size cap.

- **Proof sketch.** The Gaussian events and RSS floor in C-GROW:L0.1/L0.2 and GEN Lemmas L1.1-L1.2 use projection ranks, Gaussian contrasts and (E), not a lower eigenvalue. Redo only GEN L1.3 directly from the pinned scorer. For k <= 16 and Gram eigenvalues g_i >= g_*, write

  D_T/(n+1)^k = product_i [(g_i + 1/(n+1))/(g_i+1)].

  Each factor lies in [g_*/(g_*+1), 1], so

  |log D_T - k log(n+1)| <= 16 log(1+1/g_*).

  Also the exact spectral identity used in GEN (E2) gives

  0 <= Q_T - RSS_T^y
     <= [(1+1/g_*)/(n+1)] ||P_T y||^2
     <= 1+1/g_*.

  On the unchanged concentration event, RSS_T^y >= c_E n. Consequently

  log m(T) = c'_n - (k/2)log(n+1) - nu log RSS_T + R_T,
  sup_T |R_T| <= 8 log(1+1/g_*) + C(c_E,g_*).

  This is exactly the O(1) expansion needed in B-L, B-V1/B-V2 and NEC. Its constant need not tend to zero: the leakage rate is an O_P bound, and visibility absorbs constants into its strict exponent slack. AGG is unaffected; the first-order conclusion compares the odds with the **exact** T1, so it does not require an asymptotically exact approximation of individual scores. Extend the toolkit locally; the existing checked toolkit is not itself asserted to have weaker hypotheses.

- **Risk / refutation test.** The proposal stops at g_* > 0 fixed. Letting g_* tend to zero destroys both displayed uniform constants. An algebraic refutation would be a positive Gram matrix with eigenvalues >= g_* violating either spectral bound; both reduce to scalar inequalities. A useful numerical test is the existing near-twin construction, checking the score remainder on every table against a bound depending on the realised minimum unnormalised eigenvalue. Sample near-twins alone do not verify GF-16 over every 16-set. Any later use of a **normalised** floor to lower-bound signal must retain that floor explicitly, as in F2.

- **Your rating: ADOPT NOW (cheap and safe).** This is a bounded-remainder extension, not a new concentration argument.

## P2. Allocate the Gaussian truncation budget by column

- **Statement.** Generalise (AL), Lemma J and the fixed-design leakage bridge as follows. Choose deterministic, partition-free levels h_l = h_l(X,theta*) for l outside Q such that

  1 <= h_l <= z_n,
  b_n := 2^16 sum_{l outside Q} exp(-h_l^2/2) -> 0.

  Let J_h(d,t) = E[exp((d+sigma Z)^2/(2t^2)) 1{|Z|<=h}], and define

  L_h(Q) = p^(-1) sum_{l outside Q} max_{U: l notin U, |U|<=15} J_{h_l}(delta_{U,l},tau_U).

  Replace (AL) by (|Q|+1)n^(-1/2)L_h(Q) -> 0. Under the remaining hypotheses of T1, retain its lattice conclusion with this new rate. At Q=S0 replace its leading functional by

  L_h^0 = p^(-1) sum_{l outside S0} max_{U proper subset S0, |U|<=15} J_{h_l}(delta_{U,l},tau_U)
          + 15 sqrt(2/pi) z_n/p,                         if s0>=1;
  L_h^0 = p^(-1) sum_l sqrt(2/pi) h_l,                   if s0=0.

  Then the proposed no-leakage bound is

  o0 = O_P(n^(-1/2)L_h^0 + n^(-1)L_h(S0)^2) + o_P(n^(-kappa)), kappa<kappa_V.

  The first-order conclusion follows if kappa_V>1/2 and n^(-1/2)L_h(S0)^2->0. For the finite-n uniformity clause (T1)(d), include an explicit exceptional-probability term b_n (or prescribe a deterministic envelope b_n<=bar_b_n->0); do not hide this additional convergence requirement in n_0.

- **Why strictly better.** Choosing every h_l=z_n recovers the original condition and bounds, since b_n=O(1/log n). Smaller levels can be assigned to a deterministic handful of columns with large gains while retaining z_n for the other columns. This removes the artificial log p-sized noise excursion assigned to each isolated leaker. It changes neither scores nor the method and does not require enlarging the target lattice Q.

  A concrete separation of the hypotheses is possible with p asymptotic to n/2, one truth with ||mu||^2=B sigma^2 log n, and one null whose squared marginal mean gain is 2 sigma^2 log n. Take their correlation sqrt(2/B), and make the remaining predictors mutually orthogonal and orthogonal to these two. Fix B sufficiently large that B-2>3 with slack. These arrays have a constant normalised small-set floor and satisfy (V-c) for some c_V>3. All conditioning gains of the exceptional null are either its marginal gain or zero; all other null gains vanish. Give it h=sqrt(4 log log n), eventually below z_n, and give other nulls z_n. Its contribution to n^(-1/2)L_h is n^(-1/2+o(1)), and the bulk contributes O(sqrt(log n/n)). In contrast, because tau_empty^2/sigma^2=1+O(log n/n), its J_{z_n} is n^{3+o(1)}: the original n^(-1/2)L_n diverges as n^{3/2+o(1)}. This example establishes strictness of the primitive hypotheses regardless of the coded partition. The theorem itself has no design-family restriction and applies also for p>>n.

- **Proof sketch.** Conditional on a fixed design, a column participates in at most 2^15 actual within-block conditioning sets. Hence the probability that any relevant |Z_{U,l}| exceeds h_l is at most b_n, with no independence assumption. The union bound is over the actual tables, **not** all partition-free 15-sets. The latter appear only in the deterministic dominating functional.

  The small-gain deduction survives: symmetry and cosh(x)>=1 give, uniformly for h>=1 and t>=sigma,

  J_h(d,t) >= P(|Z|<=1) exp(d^2/(2t^2)).

  Thus the new averaged condition still forces every relevant d^2/t^2=O(log n), as required by B-L. On the common good event apply the same table-step bound. Expectation of a maximum over the at most 2^15 steps for one column is bounded by their sum, hence by 2^15 times the largest J_{h_l}. Markov yields U_Q=O_P(n^(-1/2)L_h(Q)); the singleton sum gives the leading bound. The at most 15 columns sharing a block containing all truths are covered by the unchanged 15 sqrt(2/pi)z_n/p term. Assemble by AGG/ASM. Under (V-c), use this new control of U_Q in the existing e_n-to-Xi route; under (V-m), the visibility bridge is unchanged.

  In the separating example, expansion of the Gaussian integral gives J_z approximately exp(d^2/(2sigma^2)) integral_{-z}^z exp(d u/sigma) du/sqrt(2pi), since the remaining quadratic coefficient is O(log n/n). With d/sigma approximately sqrt(2 log n) and z approximately sqrt(2 log n), its logarithm is 3 log n+o(log n). Replacing z by sqrt(4 log log n) changes this to log n+o(log n).

- **Risk / refutation test.** Levels chosen using Y would invalidate this argument; they must be functions of (X,theta*) only. Tail budgets must sum to o(1); merely requiring each tail to vanish is insufficient. Check the preceding two-variable signal construction algebraically, and compare the two J integrals and exact table odds. Any claimed proof that unions over p^15 sets using the same budget has lost the key fixed-partition counting argument. This is an enlargement of sufficient conditions, not a claim that L_h is necessary or that the leading functional alone controls higher-order models.

- **Your rating: WORTH A TICKET.** The central bound is short, but the new budget must be propagated through visibility, uniformity and transfer rather than appended only to Lemma J.

## P3. Transfer uniformly to design-measurable coefficients and supports

- **Statement.** Enlarge (T3)(a), and consequently the random-candidate clause of (T6), to the following conditional model:

  Y = X theta*(X^r) + C epsilon,
  epsilon | X^r ~ N(0,sigma^2 I_n),

  where theta* is measurable in the raw design, S0(X^r)=supp theta*(X^r) has a fixed cardinality s0 on the good-design sets, and Q(X^r) is a measurable design-only superset. Keep all the finite-n inequalities of (T3)(a), evaluated at these realised objects, with the same fixed constants and deterministic rate envelopes. Then retain its lattice and odds conclusions under the joint law, now relative to S0(X^r) and Q(X^r). No population bridge beyond the one already stated is claimed.

  In T6, allow the conditional candidate decomposition

  omega = a(X_C^r)1 + X_C^r gamma(X_C^r) + xi,

  with (epsilon,xi) conditionally independent centred Gaussians of fixed variances sigma^2 and tau^2. Coefficients beta^C=beta_C+gamma(X_C^r) and their supports may be measurable in X_C^r. Apply the enlarged transfer whenever the substituted finite-n bounds and deterministic rate envelopes hold. This replaces the explicit exclusion of design-measurable candidate coefficients in T6 and Section 6.

- **Why strictly better.** T3(a) currently allows deterministic raw beta or deterministic standardised theta*, and T6 explicitly excludes measurable candidate coefficients. The enlarged formulation includes both and additional conditional mean functions; support locations may vary too. It adds no partition condition, preserves all p-ranges and rates, and addresses a case already represented in the permitted MIS reduction source.

- **Proof sketch.** For each fixed x in the good-design set, the coefficient, support, Q and actual partition are fixed, while the conditional noise has precisely Setting F's law. Apply T1(d) uniformly at that x. For a representative bad event B_n at the deterministic envelope rate,

  P(B_n) <= P(X^r outside X_n) + sup_{x in X_n} P(B_n | X^r=x).

  Uniformity constants depend on support cardinality and the displayed bounds, not its labels or the function producing its coefficients. Integrate and use arbitrary epsilon in T1(d) to obtain the claimed O_P and o_P bounds. No union over possible supports is needed. For candidates, conditional Gaussian addition gives epsilon+xi | X_C^r ~ N(0,(sigma^2+tau^2)I); centring eliminates the measurable intercept. This is the direct conditioning argument displayed in the permitted C-MIS L1_reduction.md, Section L1.4, specialised to the new start theorem. It is rederived here, not consumed as a checked premise.

- **Risk / refutation test.** This does not cover response-selected coefficients, supports or candidate sets unless the stated conditional Gaussian model is independently established. For example, selecting a support using the largest X_j'epsilon cannot be justified by conditioning only on X. A positive sanity test is a coefficient sign or support label chosen solely from a raw design entry; conditional on that design the same fixed-design bound applies. The enlarged random-target result does not automatically rewrite the consumers' definitions of their truth model or establish their other premises.

- **Your rating: ADOPT NOW (cheap and safe).** This is an immediate use of the uniform theorem that the ticket already plans to prove.

## No credible improvement found for

- **Removing the Gram floor altogether while retaining the stated rates.** P1 reaches the 1/n correlation-eigenvalue scale. Beyond it, the determinant is no longer uniformly (n+1)^k times bounded constants. For a Gram eigenvalue tending to zero, its factor is ((n+1)g+1)/(g+1), and at g=0 there is no dimension penalty at all. A different rank-sensitive aggregation argument would be necessary. Near-twin numerics at g of constant order do not establish the floor-free result.
- **Replacing L_n(S0) entirely by the leading functional.** Truth-only conditioning does not control joint null configurations. Two correlated nulls can have cancelling marginal signal correlations but a much larger gain after one is conditioned on. T1 controls only singleton additions; the remainder in AGG genuinely requires another bound. P2 improves this bound but does not eliminate it.
- **A cleaner universally weaker replacement for (V-m).** Direct log residual-variance ratios look promising, but for nonnested U,T the noise contrast involves their residual-mean difference, not just Lambda_U-Lambda_T. A deterministic difference of nearly equal energies can coexist with a large stochastic contrast. A proposed replacement must pay for that contrast and the prior weight, including swaps. I do not have a verified improvement over the current margin with that payment included.
- **Deleting the energy bound outright.** It supplies RSS_T^y >= c n. If total signal energy is unbounded and a table explains most of it, the normalised residual can be small and the scorer's fixed 0.02 plus ridge remainder is no longer an O(1) perturbation of log likelihood. The energy numerics do not control this case. P1 retains (E).
- **Removing localisation or the exp(C_R sqrt(log n)) factor in the Gaussian-row theorem under its existing hypotheses.** At the critical Gaussian exponential moment, a bounded nonzero mean shift contributes exp(d h) at truncation h of order sqrt(log n); it is not uniformly replaceable by a polylogarithm using that argument. Removing localisation also reintroduces the maximum over polynomially many selected conditioning sets. Neither obstacle is resolved by simply integrating untruncated Gaussian moments.
- **Growing s0 and non-Gaussian noise.** Growing s0 changes both the aggregation factors and the number of truth-table contrasts; fixed-s0 visibility estimates cannot be reused verbatim. Non-Gaussian noise changes both the quadratic-form toolkit and J's exact critical-tail calculation. Neither is a cheap consequence of the displayed bounds.
- **A universal sqrt(log p/n) lower bound or a universal law for sqrt(n)o0.** The assumptions impose no sufficient decorrelation among the null projections, and unexplained signal can move the leading exponential moment away from its critical variance. T0's universal floor cannot be promoted to that logarithmic lower bound by counting columns alone. Additional partition-free covariance/spectral hypotheses and a separate dependence argument would be needed.
