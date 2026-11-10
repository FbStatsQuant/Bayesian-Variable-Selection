# R01 adversarial recheck — W3-POST

Reviewer: GPT-6 Astra, high effort. Review performed from the proofs and code, not from recorded verdicts. No source files were changed.

## 1. Component verdicts

| Component | Verdict | Scope |
|---|---|---|
| [T03R] T02(i♯), E1/E2 | VERIFIED | With E2's own restrictions on omega and s0. The unrestricted transcription in STATEMENT is false. |
| [T03R] Lemma B | VERIFIED | B1/B3 do not need a normalised floor on the large comparison union. |
| [T03R] T02(ii♯) | VERIFIED | No beta-min or SE_lambda(j0) is needed beyond the normalised floor on S0 already in R. |
| [T03R] T03♯ | VERIFIED | C1–C10 and the inherited final assembly work with fixed positive phi0 and g0. |
| [P1]/[P3] load-bearing steps relied on | VERIFIED | Contrast identity, mixed-endpoint transfer, denominator, spectral/prior bounds, Gaussian events, truncated moments, and underfit assembly. |
| L1_POST | VERIFIED | Including its explicit raw-design convention at lines 12–18; the raw variant must use that convention, not condition only on standardised X. |
| SL0/SL1/SL1′ | VERIFIED | The deterministic bounds and their probabilistic consequences are valid with the stated empty-set and feasible-truth conventions. |
| L1a′ | VERIFIED-WITH-AMENDMENTS | The lemma and its uniform bound are valid. Remarks 2 and 5 contain false or overstated assertions. |
| STATEMENT fidelity | VERIFIED-WITH-AMENDMENTS | Main concentration conclusions match the proof with the intended positive constants. The unrestricted cutoff display is false; several domain/hypothesis conventions need restoration. |

No FATAL or MAJOR mathematical defect was found in the concentration proof. This does not certify sharpness, a sampler guarantee, or exact floating-point implementation of the real-arithmetic posterior. The findings below are corrections required before presenting the consolidated statement as a self-contained theorem.

Aliases below are exactly those in STATEMENT.md: [P1], [P3], [T03R], [POST], [SL]. All other paths are repository-relative.

## 2. Findings

### 1. MINOR — the unrestricted cutoff upper bound is false

**Location:** `Theory_work/Wave3/W3-POST/STATEMENT.md:31–33`; compare `[T03R]:50–54`.

The transcription omits E2(ii)'s restrictions omega >= 0 and s0 >= 1. The surrounding definition allows real omega, and Lemma 1a explicitly allows every deterministic real sequence omega_n. A negative right-hand side cannot upper-bound a cutoff defined to be at least s0.

**Failing computation:** n=100, p=10, s0=1, omega=-100, K=10. Exact summation gives R_1=9, whereas the cutoff threshold is exp(100)/100. Thus m♯_n(omega)=1. The displayed upper bound is

`min(10, 1 + ceil((log(10) + log(100) - 100)/log(2))) = -133`.

This is a literal contradiction, not an asymptotic objection. Also, “Always s0 <= m♯ <= K” requires s0 <= K; the paragraph has not yet imposed it.

**Fix:** restore the source restrictions to this display. Alternatively, for s0 >= 1 and arbitrary real omega, put `max{s0, s0 + ceil(...)}` inside the minimum with K. State s0 <= K, and state that the minimisation is over integers. The default omega=(log n)/2 used in the concentration theorem is unaffected.

### 2. MINOR — the near-collinear example gives an incorrect ridge-bias asymptotic

**Location:** `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:48–50`.

The claim “ridge bias asymp L^2/n” is false over the stated range L^2 >> n. The variational penalty at the true coefficient is an upper bound on the optimum, not its asymptotic value. In particular, it cannot grow beyond the zero-fit objective ||mu||^2.

For standardised columns with correlation 1-eta, let `g=(n-1)eta` be the difference-direction Gram eigenvalue. With mu=L(x1-x2), the exact signal contribution to Q is

`mu'(I-M_{12})mu = 2 L^2 g (g+1)/((n+1)g+1)`.

Take eta=n^-4 and L^2=n^4. These satisfy L^2 eta=1 and L^2 >> n. The expression is asymptotic to 2n, whereas L^2/n=n^3. At n=100 the exact values are approximately 197.9804 and 1,000,000, respectively; ||mu||^2=198. If “bias” means squared prediction bias instead, the expression is `2 L^2 g ((g+1)/((n+1)g+1))^2`, and the asserted asymptotic still fails.

**Fix:** give the exact formula, or qualify the L^2/n comparison by the additional range n << L^2 << n^2 and specify that it concerns the signal contribution to Q. The example motivates trouble with the reference denominator; it does not by itself prove that the coefficient hypothesis is necessary for every possible size-tail theorem. The actual proof of L1a′ is unaffected.

### 3. MINOR — the sharpness remark has the wrong constant and omits its regime

**Location:** `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:54–58`; compare `[T03R]:63–70`.

At omega=(log n)/2, fixed t=s0 and p asymptotic to n^A, the leading coefficient of log n from the exact-tail route is

`[s0 A + (s0+2)/2]/log(2) = [(A+1/2)s0 + 1]/log(2)`.

The remark reports `(A+1/2)s0/log(2)`, omitting `1/log(2)`. For example, s0=A=1 gives 2.5/log(2), not 1.5/log(2).

Nor is `m^T_n-t asymp log n` true generally immediately after a growing-s0 remark: if t=K then m^T_n=t exactly; with fixed p the cutoff is bounded. Proposition D is a worst-case necessity example, not a lower bound for every design, and E3 assumes fixed positive sparsity and polynomial lower growth of p.

**Fix:** correct the constant and restrict the order comparison to fixed sparsity and polynomially growing p in the cited regime. Phrase the necessity as worst-case necessity for a uniform assertion. This does not alter the proved tail bound.

### 4. MINOR — restore the positivity and input conventions from the sources

**Locations:** `Theory_work/Wave3/W3-POST/STATEMENT.md:17–24,59–66,83–87`; `[T03R]:129,162`; `[POST]:23–30`; `Scripts/SMC_BVS/core/v3_preprocess.R:111–127`; `00_COMMON.md:9–11,36`.

The consolidated hypotheses say phi0 and g0 are “fixed,” without explicitly requiring positivity; item 6 similarly omits fixed phi>0 and positive finite signal-bound endpoints. These are explicit source requirements, not arbitrary real constants. The proof uses 1/g0, 1/phi0^2, and a positive beta-min envelope. The random-design bridge specifically supplies phi0^2=phi^2/2 and g0=1. Retaining only a reference to LSF does not make this a fully self-contained statement of those hypotheses.

For code fidelity, p must be the number of retained nonconstant predictors. The code drops constant raw columns before constructing K and the BB prior. The formula `X=C X^r D_x^-1` is undefined if unretained constant columns are included. A nonconstant response, equivalently s_y>0, is also required for a dataset-level statement (it holds almost surely under G). Finally, the “equivalently” sentence lists priors but should also specify the working likelihood `y | beta_S,sigma^2,S ~ N_n(X_S beta_S,sigma^2 I_n)`. The actual standardised response does not have that sampling distribution under the truth; the proofs correctly treat it as a working likelihood.

**Fix:** state `0<phi0,g0<infinity`, finite M, `0<phi<=1`, and `0<b_lo<=b_hi<infinity` or `0<theta_lo<=theta_hi<infinity`, with absolute values in the standardised-signal alternative. Define retained p, D_x and valid input, and include the working likelihood. Describe pi as the exact real-arithmetic target of the code. These are explicit statement repairs; I found no discrepancy in the score/prior formulas themselves.

## 3. Steps checked and found correct

1. **Exact prior tail:** [T03R] E1(a)–(d), lines 20–40. The multiplicity cancels the apparent per-model p penalty. The i=0 exception is handled in E1(b); the lower bound correctly starts at s0>=1. E2's minimum exists at K, and its upper/lower estimates follow under its stated restrictions. Independent numerical checks of E1's upper bound and applicable lower bound passed for 37,819 triples with 2<=p<=60, 0<=s0<=m<p, K=p. This numerical check supplements the product/geometric-series derivation.

2. **Response scaling and contrast dimension:** [P1] lines 155–221,235–264; [P3] lines 64–85. The unscaled contrast response has N=n-1 independent Gaussian noise coordinates. The working n-dimensional score transforms to an IG shape 0.51 contrast model, so `0.51+(n-1)/2=0.01+n/2` exactly. The random rate is b0*s_y^2. No Gaussian law conditional on s_y or B_n is used. The IG density comparison is pointwise, so substitution of the random rate between fixed endpoints is legitimate.

3. **Scale event:** [P1] lines 244–250. The covariance between the centred noise square and the linear noise term vanishes by symmetry. The variance bound and `(8+24M/sigma^2)/(n-1)` exceptional probability track correctly.

4. **Numerator and denominator:** [P1] lines 317–359; [T03R] lines 89–97. The numerator is a proper density at a data-free rate, giving expectation equal to prior mass without a rank assumption. Restriction of the variance integral to an interval of length sigma^2/sqrt(n) gives the stated denominator. The exponent inequality, IG minimum and expectation of Lambda are valid. Keeping R_m exactly removes the old separate prior bounds without losing a factor. The Markov split requires no independence.

5. **New design-free denominator:** L1a′ lines 25–40. Evaluating the variational objective at an exact representation gives Q_T^c <= ||epsilon_c||^2+M+M'. No invertibility of G_T is needed. D_T <= (n+1)^t holds even with zero eigenvalues. The displayed C'_Lambda is correct. Uniformity follows from constants depending only on the specified bounds. Growing t does not break the conclusion: t<=K<=n/2 gives `(1+1/n)^(t/2)<=exp(1/4)`. A bounded coordinate vector gives ||theta||^2<=n theta_hi^2/2, but the energy hypothesis remains required.

6. **Ranks and ridge penalties:** [P1] lines 90–110; [P3] lines 94–151; [T03R] B1–B3. Interlacing gives the determinant ratio lower bound `[(n+1)/(1+1/g0)]^j`, not an unjustified full `(n+1)^j` bound. Zero eigenvalues contribute 1 to D. Rank-deficient models above the sieve are covered by the density argument; within the comparison range F_w excludes them. B3's upper smoother bound requires the normalised floor on its smaller model S0 only.

7. **T02(ii♯) without beta-min:** [P1] lines 387–469 and [T03R] lines 149–156. The residual lower bound uses projection rank at most model size. The smoother error uses only R on S0. The only changed large-union spectral use is the determinant penalty. The Bayes-factor bound holds for every b>0, hence also the data-dependent rate. Item 5(a) is proved under R1 and its listed weaker design assumptions. It controls strict supersets, not false inclusions in underfitting models.

8. **Middle-range union bounds:** [P3] lines 171–203 and [T03R] C2. G2 uses rank<=|T| even for unrelated singular T; G3 uses B1's exact chi-square_j law; G4 needs full rank only for |J'|<=j0. Independence between different model statistics is never required. The sums of exceptional probabilities are bounded by geometric sums, giving 5/n. C_A=8+3A and C_* depend on fixed A,s0,j0, not on m♯. Since m♯=O(log n), delta_n log n tends to zero.

9. **C3–C5 and truncated moments:** [P3] lines 205–277; [T03R] lines 176–185. Restricting the upper residual bound to small J' supplies every needed normalised floor. The algebra retaining the 0.02n+1 correction in upsilon_n is correct. The exact truncated expectation is `(tau/2)^(j/2)/Gamma(j/2+1)`. The extra factor `(1+1/g0)^(j/2)` is absorbed into q_n, not treated as a uniform constant in j. For fixed positive g0, q_n<=c_q r_n and eventually q_n<=1/2. K_{s0,j1} is finite for the two needed fixed indices j1=0,j0; the proof does not require uniformity in a growing j1.

10. **Large underfits and beta-min:** [T03R] C6–C10; [P3] lines 284–378. Monotonicity of the smoother gives the crude bound with no eigenvalue or signal requirement. Determinant interlacing bounds D_{S'}/D_S from above by (n+1)^{|J|}. Each comparison union has at most 2^{s0}-1 underfit preimages. The exponent `(j0+1)/2 >= s0(A+1/2)+1` leaves an n^-1 factor after the crude penalty; its logarithmic factor is o(r_n). For small J', the signal lower bound and c>c0 give `(1-1/n)c>=L_*` eventually. Missing one strong coordinate suffices for the strong-signal clause. Comparison models outside Omega are only algebraic devices; no posterior mass outside the cap is assumed.

11. **Random-design bridge:** [POST] lines 37–69 and `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:85–104`. Gaussian polarization and a union bound give entrywise error O(sqrt(log n/n)) without an AR assumption or a global spectral upper bound. Standardisation preserves that order. Multiplying by O(log n) in the operator-norm bound gives the stated error; LSF(ii) dominates it and yields a fixed unnormalised sample floor. The coarse geometric prior bound gives m♯<=mbar. Energy follows from trace(Rhat_S0)=s0. The every-sequence/common-envelope contradiction establishes uniform tightness before integrating over design. With fixed raw slopes, use the raw-design event including the sample-SD bounds, as already instructed at lines 12–18. UNI-P is consistent with this route.

12. **Consequences and coded target:** [SL] lines 20–68 and STATEMENT items 2–4,5(b). The PIP, threshold, HPM and size bounds follow deterministically from delta. The bounded-functional supremum equals delta exactly; boundedness gives expectation convergence without an expectation rate. The code's K, nu, logw, W_K, H, A and Q match the displayed real-arithmetic target (`v3_score.h:40–71,175–223`). The nonnegative Q fallback is the same variational quadratic at its minimiser. Preprocessing uses n-1 sample standard deviations, as required.

Review conclusion: retain the concentration theorem and the new size-tail lemma after the statement/remark repairs above. The proposed attacks on the middle range, data-dependent response scale, and missing full Occam penalty do not break the proof under the intended hypotheses.
