Batch: LC-A   Statement: STATEMENT.md v1.1 sha256 a2e399a8d3087371   PROOF.md sha256 1497376391655759

Overall: VERIFIED

GAP steps: 0. ERROR steps: 0.

Hashes computed from the files read:

- STATEMENT.md: `a2e399a8d30873713a950f5c16de58614901dbf6f8ad9d6e40285f8556ae6bef`
- sources/W1-T03R/PROOF.md: `1497376391655759bb8d0479b4f344c10f3c9e1a476182cd1881ee28868e9bd4`

Paths in the table are relative to this ticket directory. “W1” means `sources/W1-T03R/PROOF.md`; “P1” means `sources/P1/PROOF_v3.tex`. Verdicts use the locked STATEMENT's explicit readings, including its definition of R_m for negative m and its p=1 specialization. No GAP/ERROR requiring a C/S/F/E tag was found. Two notation/scope observations are recorded below without treating an already specified reading, or an inaccurate sentence in the review brief, as a mathematical failure of the proof.

| step | file:lines | verdict | note (what was checked) |
|---|---|---|---|
| Tail definition and cancellation | W1:15–17; STATEMENT:48–52 | VERIFIED | The cap normalizer W_K cancels exactly. Interpret the sum with lower limit max(m+1,0), as expressly defined in STATEMENT. For m<0 the event is all of Omega; for m>=K both its prior and posterior masses vanish. See N2 for the notation correction. |
| E1(a) | W1:20–22,32 | VERIFIED | Twice the numerator of rho_i is (2p-1-i)-(i-1). The consecutive-size ratio is (p-i)/(2p-1-i); telescoping from q_s0/w(s0)=binom(p,s0) proves the product, including the empty product at k=s0. All denominators are positive for the specified indices. |
| E1(b) | W1:24–25,34–36 | VERIFIED | For i>=1, x=(i-1)/(2p-1-i) is in [0,1), and x>=(i-1)/(2p-2). For i=0, log(1+1/(2p-1))<=1/(2p-1)<=1/(2p-2). Summing i-1 gives [(k-1)(k-2)-(s0-1)(s0-2)]/2, also for s0=0. Integer t(t-1) is nondecreasing for t>=0, including the equality at 0,1. The remaining infinite geometric sum is exactly 2^{-(m-s0)}. If m>=K the finite sum is empty, so no out-of-range rho_i is evaluated. This step is on its stated p>=2 domain. |
| E1(d) | W1:30,40; P1:117–118,128–130 | VERIFIED | The older upper bounds divide to 4(2p)^s0 2^{-m}. The new upper bound is at most this divided by 4 s0! exp(gamma_m). For m>=s0>=1, gamma_m>=0: s0(s0-1)-(s0-1)(s0-2)=2(s0-1)>=0. This comparison concerns bounds, not a claim that the posterior tail itself has this ratio. |
| Definition, existence, and cap bound for m-sharp | W1:44–47 | VERIFIED | The admissible integers are bounded below by s0 and contain K when s0<=K, because the positive threshold exceeds R_K=0. Thus a minimum exists and is between s0 and K, for every real omega. It is deterministic, depending only on n,p,s0,omega. |
| E2(i) | W1:49–52,59 | VERIFIED | For omega>=0 the ceiling defining m_n(omega) is >=s0 and makes 2^{-m}<=(2p)^{-s0} n^{-(s0+1)/2} exp(-omega). E1(b),(d) therefore make m admissible for s0>=1. On the extra s0=0 branch, n>=5 gives m>=2 and gamma_m>=0. Combining with m-sharp<=K proves the stated minimum bound. p=1 is supplied directly as in N1, without dividing by p-1. |
| Excluded-step dependency check | W1:59–70,160–207 | VERIFIED | T03-sharp uses E2(i) in C1 and T02(i-sharp) in C9; it uses neither E2(ii),(iii) nor E3. E2(i) needs only E1(b),(d); E2(iii) invokes E1(c), and E3 invokes E2(iii). Caveat to the brief's global wording: the excluded Proposition D also says “as in E1(c)” at W1:117 and reuses its product-bound argument. Thus “only E2(iii)/E3” is correct for the relevant location-bound route, not as a literal description of every occurrence in the whole file. This does not put E1(c) on the T03-sharp dependency chain. |
| P1 setting and contrast identities | P1:40–59 | VERIFIED | Fixed orthonormal U gives U^T1=0, U^TC=U^T, X=UX_c and y=Uy_c/s_y, hence equal Gram matrices and norm identities. Nondegenerate Gaussian noise on the n-1 dimensional contrast space makes s_y>0 almost surely. This construction uses no design rank assumption. Empty-model conventions and proper fixed-rate priors agree with the locked definitions. |
| P1 lem:slab | P1:62–81 | VERIFIED | G+I and H are positive definite even if the design is singular. Completing the square gives precision H/(nv), mean n H^{-1} A^T Y, minimum Q>=0, and determinant factor det(G+I)^{1/2}/det(H)^{1/2}. The Gaussian normalization cancels the powers of nv exactly. The k=0 case is explicitly covered. |
| P1 lem:IGint | P1:83–88 | VERIFIED | t=b/v gives b^{-a} times the Gamma(a) integral; both parameters are positive at each subsequent use. |
| P1 lem:spec(a) | P1:90–93,101 | VERIFIED | The intertwining identity with c=n+1 transfers the inverse through A and gives M=h(AA^T); substituting in Q gives the quadratic-form representation. Ridge inverses exist for any A. |
| P1 lem:spec(b) | P1:94,103 | VERIFIED | h(0)=0 and 0<=h(lambda)<n/(n+1). The positive eigenspace is the column span, so both asserted Loewner lower bounds for I-M and both bounds for Q follow, including for rank-deficient A. |
| P1 lem:spec(c) | P1:95,105 | VERIFIED | Its explicit hypothesis lambda_min(G)>=g>0 supplies full column rank. On the column span h(lambda)>=n/(n+1)[1-1/((n+1)g)], and 1-h(lambda)=(lambda+1)/((n+1)lambda+1)<=(1+1/g)/(n+1). Off the span M=0. The first lower coefficient may be negative; this does not invalidate the inequality. At the denominator use, g=(n-1)phi0^2 comes from R alone. |
| P1 lem:spec(d) | P1:96,107 | VERIFIED | Adjoining columns increases AA^T in Loewner order; h(B)=n/(n+1)[I-((n+1)B+I)^{-1}] is operator monotone by order reversal under inversion. Q consequently decreases. No full-rank condition is hidden here. |
| P1 lem:spec(e) | P1:97,109–110 | VERIFIED | f(lambda)=((n+1)lambda+1)/(lambda+1) is increasing, with 1<=f<n+1, proving 1<=D<=(n+1)^k. With j new columns, increasing-order interlacing gives lambda_i(G)<=lambda_{i+j}(G'), leaving j factors >=f(g). Finally f(g)>=(n+1)g/(g+1). The lower ratio explicitly assumes lambda_min(G')>=g; the upper bound used in den-prime does not. |
| P1 lem:prior(a) | P1:113–115,123–124 | VERIFIED | B(k+1,2p-k)/B(1,p)=k!(2p-1-k)!/[2(2p-1)!]. Summing the beta mixture by the binomial theorem yields total mass one. The k=0 term is 1/2, so 1/2<=W_K<=1. These facts also hold at p=1. |
| P1 lem:prior(b) | P1:116,126 | VERIFIED | Consecutive binomial coefficients give (k+1)/(2p-1-k), with positive denominator throughout 0<=k<=p-1, including p=1. |
| P1 lem:prior(c) | P1:117,128 | VERIFIED | q_1=p/[2(2p-1)]<=1/2; all subsequent ratios are <=1/2. Thus q_k<=2^{-k} for k>=1. For m>=0 the infinite geometric upper sum is 2^{-m}, and division by W_K costs at most 2. For m<0 the displayed upper bound exceeds one. |
| P1 lem:prior(d) | P1:118,130 | VERIFIED | W_K<=1 and binom(2p-1,s0)<=(2p-1)^s0<=(2p)^s0 give the stated lower bound, whenever s0<=K. The empty-support convention also works. |
| P1 lem:chi(a) | P1:139–142,148 | VERIFIED | The mgf at 1/4 is 2^{r/2}; multiplication by exp[-(2d log 2+4x)/4] gives at most exp(-x) for r<=d. The degenerate r=0 case causes no exception, including zero threshold. |
| P1 lem:chi(b) | P1:143,149 | VERIFIED | Var(chi_d^2)=2d gives Chebyshev's bound and the absolute-deviation bound by Cauchy–Schwarz. Denominator use has d=n-1>=2. |
| P1 lem:chi(c) | P1:144,150 | VERIFIED | The exponential cancels the density's exponential and integration gives (tau/2)^{d/2}/Gamma(d/2+1). For x=d/2>0, Gamma(x+1)>=integral_x^infinity t^x exp(-t)dt>=x^x exp(-x), yielding (e tau/d)^{d/2}. |
| P1 prop:closed | P1:153–171 | VERIFIED | Tonelli, slab integration and the IG integral give exactly the two closed forms. Original-model shape is a0+n/2=nu; contrast-model shape is 0.51+(n-1)/2=nu. The powers of 2 give (2b0)^a0/pi^{n/2} in m(S). b+Q/2 is strictly positive. The conditional normal and IG distributions have the stated means, covariances, shapes and rates. |
| P1 thm:T01i | P1:173–209 | VERIFIED | z_c=s_y z and Q_c=s_y^2 Q. With s=s_y, the inverse transformation Jacobian is s^{-k-2}; likelihood, slab and IG scaling factors are s^n,s^k,s^2. Absorbing v^{-1/2} shifts the IG shape by 1/2 and contributes b^{-1/2}=(b0 s^2)^{-1/2}. This yields c_n(s)=s^{n-1}Gamma(0.51)/[sqrt(2 pi b0)Gamma(0.01)], independent of S, and all posterior and conditional identities follow after normalization. No probabilistic conditioning on s_y is used. |
| P1 thm:T01ii | P1:213–222 | VERIFIED | The IG density ratio is (b/b')^{0.51} exp[-(b-b')/v]. Comparing to each endpoint gives the two pointwise envelopes. Integration preserves them and division by the lower bound on Z_b costs the second kappa factor. Because the inequality is simultaneous for all observed y_c and b in the interval, evaluating b at b0 s_y^2 is legitimate. |
| P1 thm:T01iii | P1:232–251 | VERIFIED | eps_c is exactly Gaussian with covariance sigma_*^2 I. For N=n-1, Delta=sigma_*^2(E'/N-1)+2 mu^T eps/N. The odd cross moment vanishes, so E Delta^2=2 sigma_*^4/N+4 sigma_*^2 norm(mu)^2/N^2<=(2 sigma_*^4+6 sigma_*^2 M)/N, using n/N<=3/2. Both failures of the scale event imply abs(Delta)>sigma_*^2/2. Chebyshev gives precisely (8+24 M/sigma_*^2)/N. No column rank or eigenvalue condition is used. |
| P1 thm:Ta | P1:253–265 | VERIFIED | T01i identifies the posterior at observed b; T01ii applies pointwise on B_n. Z^c_bplus>=varpi(S0)m^c_bplus(S0) when s0<=K. Adding P(B_n^c) to the tail probability proves both asserted transfer consequences, including for measurable data-dependent parameter events. This pointwise allowance is not used to claim a density expectation for a data-dependent model collection. |
| P1 lem:num | P1:313–322 | VERIFIED | At fixed data-free b, the slab and IG priors are proper even for singular X_c,S. Tonelli makes m_b^c(S) a probability density in y_c. Division by the everywhere positive true density and integration gives expectation one; summing a deterministic model collection gives exactly its prior mass. E_m is deterministic at every fixed integer m. |
| P1 lem:den | P1:324–360 | VERIFIED | Re-derived in detail below. R on S0 supplies exactly the positive eigenvalue needed for spec(c); signal containment removes the residual mean. The restricted variance interval, exponent bound, determinant bound and prior factor yield the displayed inequality. Each of the three nonnegative terms in Lambda has the claimed expectation bound. |
| Lemma den-prime | W1:89–91; P1:324–360 | VERIFIED | The P1 proof gives the marginal-density lower bound before multiplying by varpi(S0). Omitting that multiplication leaves the same Lambda and C_Lambda and removes the entire prior factor, with no new hypothesis. In particular it is extracted from the proof, not inferred by dividing the weaker stated lower bound in lem:den. |
| P1 thm:T02i | P1:362–382 | VERIFIED | The deterministic event's numerator expectation is <=2^{1-m}, uniformly for every integer m. The denominator bound and mixed-endpoint transfer leave c1=4 kappa^2/(c_IG sigma_*^2). Splitting the product at sqrt(L), and applying Markov separately to the numerator normalization and Lambda, gives the stated bound uniformly in m. The ceiling inequality cancels the factors (2p)^s0 and n^{(s0+1)/2}; fixed s0 bounds (1+1/n)^{s0/2}. The initial restriction to sufficiently large n with s0<=K is legitimate for this asymptotic statement. Neither restriction on omega_n quoted in the inherited statement is needed by this proof. |
| T02(i-sharp), definition and finite-n bound | W1:74–82,85,93–97 | VERIFIED | For R_m>0 set v_m=varpi(E_m)=R_m varpi(S0). lem:num gives E[N_m/v_m]=1, exactly and uniformly in m. Mixed-endpoint transfer and den-prime give Theta-sharp<=c-sharp exp(Lambda) Theta^(1) on B_n, with c-sharp=kappa^2/(c_IG sigma_*^2). For L>(c-sharp)^2 the logarithmic Markov threshold is positive. The union bound needs no independence, and its right side is exactly the displayed sum of the scale-event bound, 1/sqrt(L), and C_Lambda/log(sqrt(L)/c-sharp). For R_m=0 the mass is identically zero and the chosen Theta is consistent. |
| T02(i-sharp), quantifier and consequence | W1:83–84,97–99 | VERIFIED | The same right side bounds every fixed-m probability, so taking sup_m outside P_0 is valid. It tends to zero after limsup_n and then L to infinity. Since m-sharp_n(omega_n) is deterministic for every deterministic real sequence omega_n, its probability is bounded by that supremum. The definition of the cutoff gives the exact remaining factor (1+1/n)^{s0/2} exp(-omega_n); s0 fixed makes it bounded. No union bound over m, random cutoff, or P_0(sup_m Theta>L) is asserted or used. This proof works at every valid finite n with s0<=K for the finite-n inequalities. |

Re-derivation of the denominator, without the prior bound:

Put N=n-1, sigma2=sigma_*^2, P=P_{S0}, and gamma=(1+1/(N phi0^2))/(n+1). Under R, spec(c) gives

`Q_c(S0) <= norm((I-P)y_c)^2 + gamma norm(P y_c)^2 <= sigma2 E' + R_n`,

where E'=norm(eps_c)^2/sigma2 and R_n=gamma norm(P y_c)^2>=0. The signal is in the column span of X_c,S0. For s0=0, P=0, the signal vanishes, and the same bound holds with R_n=0.

The slab integral divided by the true density has integrand exponent

`-N log(u)/2 + E'/2 - Q_c(S0)/(2 sigma2 u)`, with u=v/sigma2.

For 1<=u<=1+n^{-1/2}, log(u)<=u-1, 1/u>=2-u, and R_n/u<=R_n imply successively

`exponent >= (u-1)[E'/u-N]/2 - R_n/(2 sigma2)`

`>= (u-1)[E'-N-E'(u-1)]/2 - R_n/(2 sigma2)`

`>= -abs(E'-N)/(2 sqrt(n)) - E'/(2n) - R_n/(2 sigma2) = -Lambda_n`.

The variance interval has length sigma2/sqrt(n), lies inside [sigma2,2 sigma2], and its IG density is >=c_IG>0. Thus

`m^c_bplus(S0)/f0 >= D_S0^{-1/2} c_IG sigma2 n^{-1/2} exp(-Lambda_n)`

`>= (n+1)^{-s0/2} c_IG sigma2 n^{-1/2} exp(-Lambda_n)`.

The last step uses only spec(e)'s universal determinant upper bound. The first two expectation terms are <=1/sqrt(2) and <=1/2. For s0>=1,

`E R_n <= gamma [norm(mu)^2 + N sigma2] <= gamma n(M+sigma2) <= (1+1/(2 phi0^2))(M+sigma2)`.

This gives precisely C_Lambda. For s0=0 its last term disappears. Multiplying this established marginal bound by the independently verified prior lower bound recovers P1 lem:den; leaving it unmultiplied proves den-prime.

Named points (N1, N2, N3, N4):

**N1 — confirmed, with the stated specialization.** Under the locked s0>=1 and s0<=K, p=1 forces s0=K=1. R_m=0 for m>=1, so m-sharp_n(omega)=1 for every real omega. For omega>=0, m_n(omega)=ceil([log 2+log n+omega]/log 2)>=1; in particular the proposed local repair `m-sharp_n <= K=1 <= m_n(half log n)` is correct. The expressions containing 1/(p-1) in E1(b),(d) and the E2(i) derivation must remain on their explicitly stated p>=2 domain; they are not formulas to evaluate at p=1. E1(a) itself is defined at p=1. No further argument in the checked portion of section 2 or its P1 dependencies needs p>=2: the prior, ridge, contrast, density and denominator arguments all permit p=1. The section 2 size tail at its cutoff is identically zero. This verifies the section 1 input needed by T03-sharp, not the brief's broader claim that every excluded statement is trivial or void at p=1.

**N2 — confirmed under the required reading.** The literal sum printed at W1:16 and referenced at :79–80 should have lower index max(m+1,0); otherwise it asks for undefined negative-index q_k when m<=-2. The ratio of prior masses at :16 already defines the intended object, and STATEMENT:48–49 explicitly supplies the corrected sum. For every m<0, E_m=Omega, v_m=1, R_m=1/varpi(S0), and Theta^(1)=Z^c_bminus/f0 has expectation one by lem:num. All lines of the probability proof remain valid without alteration. Negative m values give the same event and the same normalization to one another, and m>=K gives Theta-sharp=0, so neither extreme damages sup_m P_0(Theta-sharp>L). This is a notation correction already resolved by the locked definition, not a strengthening of the theorem or a change to the placement of its supremum.

**N3 — confirmed / moot for this statement.** The special n>=5 condition in E2(i) is used only to force m>=2 when s0=0, making its gamma nonnegative. The locked hypothesis s0>=1 excludes that branch. For p>=2, s0>=1, n>=3, the proof works as written. For p=1 use N1.

**N4 — confirmed.** None of E1(a),(b),(d), the cutoff definition, E2(i), den-prime, T02(i-sharp), or the checked P1 proofs uses p<=n^A or A>=1. The inherited P1/common R bundles list these conditions, but direct inspection and re-derivation establish the consumed results under G, fixed s0, the signal-energy bound, R's eigenvalue bound on S0, and eventual membership S0 in Omega. Accordingly their use at the record's unchanged A introduces no strength gap in this batch. W1:99 is correct. The uses of polynomial growth in the excluded E3 or in downstream C1/C8 are not conclusions of this batch and are not being certified here.

Hidden-hypothesis inventory:

- **Contrast space:** C is a deterministic orthogonal projection of rank n-1, with fixed orthonormal basis U. Thus X_c^T X_c=X^T X and U^T eps has covariance sigma_*^2 I_{n-1}. The basis and Gaussian law come from the setting and G, not a sparse eigenvalue assumption or conditioning on s_y/B_n.
- **Ridge inverses and proper slabs:** every G=A^T A is positive semidefinite, so G+I and H=(n+1)G+I are positive definite, for every set in Omega. This supplies all inverses, positive determinants, proper slab densities and finite closed forms in lem:slab, prop:closed, T01i, T01ii, Ta and lem:num. Singular candidate designs are allowed.
- **Smoother spectrum, spec(a),(b):** the nonzero eigenspaces of AA^T span col(A); SVD or the spectral theorem supplies this fact without full column rank. h(0)=0 supplies all zero-eigenvalue cases and the empty model.
- **Positive minimum, spec(c):** the lemma explicitly assumes lambda_min(G)>=g>0; it therefore has full column rank on exactly that A. In the consumed denominator use, A=X_c,S0 and g=N phi0^2 are supplied by R: lambda_min(R_S0)>=phi0^2. No condition on a competing model is used.
- **Nested smoother monotonicity, spec(d):** adjoining columns adds a positive semidefinite matrix to AA^T, and ridge inversion reverses Loewner order. No rank increase is assumed.
- **Determinant bound, spec(e):** D<=(n+1)^k follows from nonnegative Gram eigenvalues alone. The separate determinant-ratio lower bound uses principal-submatrix interlacing and the lemma's explicit lambda_min(G')>=g. That conditional lower bound is checked as a lemma but is not needed in den-prime or the size-tail proof; no full SE is needed to apply the determinant upper bound.
- **Truth containment:** by the definition of S0, mu_c=X_c theta* lies in col(X_c,S0); consequently (I-P_S0)mu_c=0. R supplies full rank on S0 when s0>=1, although containment itself does not need it. The denominator uses only the projection contraction, not an assumed rank or chi-square distribution for P_S0 eps_c.
- **Noise chi-square:** E'=norm(eps_c)^2/sigma_*^2 has exactly n-1 degrees of freedom by fixed U and G. The general chi-square lemma takes its degrees as explicit hypotheses. No set-dependent exact degrees are silently required in this batch.
- **Scale event:** G and norm(mu)^2<=nM are sufficient for its mean, variance and probability bounds; no eigenvalues enter. n>=3 supplies n/(n-1)<=3/2 and 1/(n-1)<=1/2 in the constants.
- **Prior denominator and finite set:** s0<=K supplies S0 in Omega and varpi(S0)>0 at every finite-n use in den-prime/T02(i-sharp). R1 supplies this eventually for asymptotic results. The cutoff is defined only on that domain. Positive prior weights imply R_m=0 exactly when the model event is empty.
- **Other ranges:** p>=2 is needed only for the displayed E1(b),(d) denominators and their E2(i) use; N1 handles p=1 directly. s0>=1 gives gamma_m>=0 without the empty-support side condition. Fixed s0 bounds the residual (1+1/n)^{s0/2} in the O_P consequence. Constants M,phi0,sigma_*^2 are fixed; c_IG and c-sharp are finite constants independent of n,p,m. Deterministic design makes m-sharp data-free. No SE_lambda, SE_w, full SE, beta-min, p<=n^A or A>=1 is used by this batch's size-tail proof.

Not checked:

- E1(c), E2(ii),(iii), E3: their mathematical proofs and conclusions were not checked. Only their dependency relationship and absence from the T03-sharp route were inspected.
- Proposition D, section 3: not checked. The search hit at W1:117 is recorded solely to qualify the brief's “only” claim about E1(c).
- P1 lem:prior(e); T01(iv), Tb1, Tb, and section T02(ii), including lem:good/onG/one and thm:T02ii: not checked. The occurrence of the latter labels in W1:205 does not make them dependencies of the section 2 proof.
- W1 sections 4–5 and the P3 proofs: not checked. W1:160–207 was read only to establish which section 1–2 conclusions T03-sharp consumes; no verdict on C1–C10 or Assembly is issued here.
- Full T03-sharp selection, PIP, HPM, partial-signal and scale-invariance conclusions: outside this batch.
- No other review, log, checkpoint, report, notes, other-ticket material, earlier verification, or web source was consulted. No subagents, computations, scratch files or git commands were used.
