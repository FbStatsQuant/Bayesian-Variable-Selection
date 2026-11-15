MANIFEST b643f323a2ac2948975e3f01e54d30c0e64cf6643eebe911d1475fac270c3dc6

# LC2-B independent lemma check — W3-RM2, L5

Verdict per lemma/claim:

- §0 (S2), (S3): VERIFIED.
- Lemma P8: VERIFIED.
- Lemma P9a: VERIFIED-WITH-AMENDMENTS (two minor proof conventions below; no statement falls).
- Lemma P9: VERIFIED.
- Lemma D-loc^b: VERIFIED.
- Lemma P10: VERIFIED, with the stated W2-APP:POST@1.0.1 dependency for p >= 2.
- Theorem RM2-R / (C2): VERIFIED, conditional on W2-APP:POST@1.0.1 as recorded in STATEMENT §5.
- Containment of RM-R / (C4), Gaussian-row half: VERIFIED.

## Findings

1. **MINOR — `lemmas/L5_formR.md:50,66-67` (relative to W3-RM2).** The standing Setting R imported from `lemmas/L4_sandR_b.md:16-18` allows a nonzero raw mean m_n. As written, e = W_l - W_T beta need not have iid *centred* N(0,tau²) entries. Its independence from W_T still holds, but the assertion about its entrywise mean is false without a reduction. This is a proof-convention omission, not a failure of the bound: C and P_T annihilate constant vectors. **Exact correction:** before the definitions in §2, add: “In this section replace W by W - 1 m_n^T, without changing notation. This leaves CW, X, P_T, all Z, and all population covariance/regression hypotheses unchanged; interpret the latent extension and its functionals on this centred row law.” Then the chi-square calculations and the reference/atom identities are literally those claimed. Alternatively use centred residuals throughout. The source template explicitly uses mean-zero rows at `W2-LOC2/lemmas/L2_NAR.md:10-11`; this convention should be made explicit when re-running it here.

2. **MINOR — `lemmas/L5_formR.md:56-64`.** P9a does not explicitly discharge the empty pair set before writing log|P+|. The permitted endpoint Q = S0 = [p], including p = 1, has P+ empty. P9 itself handles empty P at line 88, but P9a's displayed construction then contains log 0. **Exact correction:** begin its proof: “If P+ is empty, interpret (2.1) as the simultaneous, vacuous bound on its members, and take A_n to be the sure event and varsigma_n = 0. Otherwise use the following construction.” One may instead explicitly set max over the empty family of squared statistics to 0. This matches the empty-family clause in the source template at `W2-LOC2/lemmas/L2_NAR.md:53`.

No FATAL or MAJOR finding; neither correction changes a hypothesis, exponent budget, or conclusion. The verification of P9a below supplies both conventions. P9 and the theorem do not acquire an additional substantive premise from them.

## Independent derivations

### 1. Frozen inputs and scope

All 54 SHA-256 entries in MANIFEST_LC2.txt match their files. I read the assigned brief and manifest, the allowed L5/context/template files, and the allowed K11 script/output. I did not consult other review reports, LOG.md, or CHECKPOINT files. The only written file is this review; no git operation was performed.

### 2. Sample floors, signal floor, and uniform conditioning (S2, S3, P8)

On E_W, the entrywise correlation error is at most 3 C_A sqrt(log n/n), where C_A = 8 sqrt(2A+3). For S = Q union {l},

    ||Rhat_S - Sigma_S||op
      <= |S| max_jk |Rhat_jk - Sigma_jk|
      <= 3 C_A (n^b+1) sqrt(log n/n)
      <= 6 C_A n^(b-1/2) sqrt(log n).

This tends to zero for every fixed b < 1/2. Choosing a deterministic threshold at which the last expression is <= c/2 proves all sample floors simultaneously by Weyl. No union over subsets and no upper spectral bound is needed. The event E_W and its entrywise estimate require Gaussian rows, unit marginal variances, and p <= n^A; they do not require the extra bounded-size population floors that P8 does not assume.

Energy obeys ||mu||² <= s0² theta_hi²(n-1) deterministically. Put phi0² = c/2 and alpha = c theta_lo²/(2 sigma²). On E_W,

    lambda_n >= alpha(n-1),
    d_n² + log n <= 2(q+1) + 4 log(2p) + log n
                  <= C(A)(n^b + log n).

Consequently lambda_n/(d_n²+log n) >= c1 n/(n^b+log n), which implies the weaker deterministic rate c2 n^(1-b)/log n used in S3. Thus (BM-W) is uniform in the conditioning design.

For the lattice family, L0 §4(ii) gives log|F_lat| + log|VV_lat| + J_n <= C(s0,A)(q+log n), with J_n=q+1. Every toolkit threshold is therefore bounded using n^b and log n. In particular its small parameters are bounded by constants times n^(-1/3) + (n^b+log n)/n, and their products with log n tend to zero. Gram, energy, and rank thresholds are deterministic too. This verifies the claimed uniformity; a pointwise appeal to an asymptotic fixed-design theorem alone would not have sufficed.

On X_n = E_W intersect {w0_n <= -t_n}, NA-W has s_n >= t_n and its size requirement follows from (3/4)t_n sqrt(log(n+1)) >= 4 kappa_E+2. The conditional failure bound is exp(-t_n²/8). Adding the toolkit failure gives exactly line 39. For TL-W the same addition bound controls Z+ with the extra 2/n term. Its truth-noise event has failure <=1/n. Its remaining deterministic requirements can be enforced uniformly from lambda_n >= alpha(n-1) and the preceding upper bound for d_n². These include the comparisons in L2 lines 211-217 and the final score margin over O(log n). Integrating on X_n and adding P(X_n^c)=o(1) proves both conclusions. If P is empty, its no-addition constraints are vacuous; the truth-removal argument remains available.

### 3. Five-step joint bound (P9a)

Use the centred convention in finding 1, and handle the empty family as in finding 2. Write M=|P+|>=1, ell=log M <= log p+q log 2, N=n-1.

1. N >= q+1 eventually. All relevant population submatrices are positive definite by (N1); centred Gaussian sample matrices of these dimensions have full rank almost surely. There are finitely many for each n. Since P_T C=P_T, h=Ce-P_T e and h is orthogonal to P_T e. Thus ||h||²=||Ce||²-||P_T e||² and the numerator identity in line 63 is exact. Sample standardisation cancels because t_l>0.

2. Set x=ell+2 log n and v=4(ell+q+2 log n). Laurent–Massart applied to two residual-norm tails and one reference-norm tail gives 3M exp(-x)=3n^-2. References of zero variance have zero centred norm and need no division. Conditional on W_T, the residual projection is chi-square of rank d<=q; the mgf at 1/4 gives

       M 2^(q/2) exp(-v/4)
         = n^-2 exp(-(1-log(2)/2)q) <= n^-2.

   Conditional on the design, the same calculation for P_Q epsilon at 4(q+log n) gives failure <=1/n. These are the only events that pay for all M<=p 2^q pairs.

   For each random frame subspace, condition on the whole extended design, independent of epsilon. Its projection is bounded by chi-square_m0. At x'=2 log N_n+(m0+2)log log n, the Chernoff bound after multiplying by N_n is <=(e x'/m0)^(m0/2)(log n)^(-(m0+2)/2)=O(1/log n). No q enters this sharp tail.

   For atoms, condition on epsilon: each inner product is centred Gaussian with variance <=||C epsilon||². The union at y²=2log(2(M_a+1))+2 b_n has failure <=e^-b_n, where M_a is the atom count and b_n=sqrt(log n/(1+L_n²)). If M_a>=1, R2 implies L_n²=o(log n); if M_a=0, L_n=0. Hence b_n tends to infinity and L_n² b_n/log n <= L_n/sqrt(log n) tends to zero. The noise-norm event has failure <=e^(-N/8): Laurent–Massart at x=N/8 has upper threshold N(1+1/sqrt(2)+1/4)<2N. Independence among pairs, atoms, or frames is unnecessary.

3. The reference/atom identity and Cauchy–Schwarz give

       |(Ce)^T epsilon|/(sigma ||Ce||)
         <= sqrt((1+eta')(x')) + L_n y sqrt(4/c) = zeta_n,
       1+eta'=(1+eta)(1+delta)/(1-delta),
       delta=2sqrt(x/N)+2x/N.

   Here the lower bound ||Ce||²>=cN(1-delta)>=cN/2 supplies the constant sqrt(4/c).

4. Since x,v=O(q+log n), delta tends to zero and v/N tends to zero for q/n ->0. The norm ratio is at most 1+omega'=(1-v/[N(1-delta)])^(-1/2). The remaining numerator term is at most

       epsilon_n = 2sqrt(2) sqrt(v(q+log n)/N)
                 = O((q+log n)/sqrt n).

   It tends to zero at q<=n^b, b<1/2. Within these five steps, this is the sole use of the stricter exponent b<1/2, rather than b<1. The separate S2 argument also uses b<1/2.

5. R1 gives x'<=2log p+o(log n). R2 gives L_n² y²=o(log n), including the adaptive b_n term. Expanding zeta_n² gives <=2log p+o(log n), with zeta_n²=O(log n). Expanding B_n=((1+omega')zeta_n+epsilon_n)² gives the same bound. A completely explicit deterministic choice for large n is

       varsigma_n = max(0, (B_n - 2log p)/log n).

   It tends to zero. Values at finitely many earlier n can be enlarged freely. This proves (2.1) on the five-event intersection with deterministic error, not merely an O_P bound. The extension may be latent; the final statistic still depends only on W and epsilon.

### 4. Joint law to conditional width (P9)

For nonempty P let B be its exceedance event at 2log p+varsigma_n log n. The preceding result gives P(B)=o(1); adding P(E_W^c)=o(1) gives pi_n=o(1). Markov on W gives

    P(E_W intersect {P(B|W)>sqrt(pi_n)}) <= sqrt(pi_n).

On the resulting design event W1_n, all directions are defined by S2. Conditioning on W removes any issue concerning latent variables because B uses only W and epsilon; epsilon/sigma is a fresh standard Gaussian. The functional Phi=max_P(|u^T g|-a_delta(|T|)) is 1-Lipschitz and its mean is exactly the defined w_n(delta), not the unshifted maximum's mean.

For delta0 in (0,1-2b), gamma=1-2b-delta0 lies in (0,1). Since |T|+1<=2n^b, the lower comparison radicand is

    2log p + gamma log n - 2log 2.

Eventually it is positive and greater than 2log p+varsigma_n log n. Both comparison radicands are <=(2A+1)log n. Rationalising their square roots bounds Phi on B^c by

    -[(gamma-varsigma_n)log n-2log 2]/[2sqrt((2A+1)log n)]
      <= -gamma sqrt(log n)/[5sqrt(2A+1)] = -s_under_n.

The last inequality follows eventually from varsigma_n+2log 2/log n<=3gamma/5. The probability of this event conditional on W is >=1-sqrt(pi_n)>=1/2. Lower-tail concentration alone yields P(Phi<=E Phi-2)<=e^-2<1/2; hence E Phi < -s_under_n+2. The asserted constant and restriction on delta0 are correct. Finally the level difference between a0 and a_delta is at least delta0 sqrt(log n)/(2sqrt(2A+2)), yielding exactly the stated deterministic t_n once w_n(delta0)<=0. Empty P is explicitly discharged in P9.

### 5. Local regressions (D-loc^b)

N=T intersect N_l is a population regression set with invertible covariance by interlacing (N1). There are at most p 2^nu_n one-functional frames, so log N_n<=log p+nu_n log2=log p+o(log n). Choose r=W_l-W_N beta_N and atoms e_v for v in Q, each of variance one. With lambda=beta_bar_T-beta_bar_N,

    r - W_Q lambda = W_l - W_T beta_T.

The coefficient norm is at most the given L_n; if R2 names its exact maximum instead, that maximum is smaller and still satisfies its bound. The atom condition is exactly L_n²log(q+1)=o(log n). The supplied variance ratio is exactly R3. No polylogarithmic bound on q is used in this construction.

### 6. Posterior input and endpoint (P10)

T1-R is defined in the parent STATEMENT lines 129-132 by the same j0, mbar_n, kbar_n and the same two floors and psi_n rate as LSF in W2-APP L1_POST lines 20-25. Setting R supplies its remaining assumptions when p>=2 (including p>=s0). Part (b) is therefore applicable without a strengthened spectral assumption. Its O_P(sqrt(log n/n)) result gives convergence in probability; boundedness gives E[1-pi(S0)]<=e+P(1-pi(S0)>e), hence convergence in mean. I retain this lemma's dependency status rather than re-certifying its proof.

For p=1, w(0)=w(1)=1/2, G=n-1, H=(n+1)(n-1)+1=n², D=H/(G+1)=n. From the D0 definition Q_A=N-z²/n with z=rhat N and Q_empty=N. Thus

    Delta F = -log(n)/2 - nu log(1-u),
    u = rhat² (n-1)²/[n(n-0.98)],
    Delta F >= -log(n)/2 + nu u.

These are exactly lines 120-122. The centred response has N^-1 x^T Y=theta*+o_P(1) and N^-1||Y||²=theta*²+sigma²+o_P(1), since conditional noise variance of x^T epsilon/N is sigma²/N. Uniformly for theta_lo<=|theta*|<=theta_hi, rhat² differs from theta*²/(theta*²+sigma²) by o_P(1), and the latter is bounded below by theta_lo²/(theta_hi²+sigma²)>0. Hence Delta F tends to infinity in probability, giving posterior mass tending to one and the same bounded-expectation argument.

K11 in the frozen output reports maximum error 1.21e-13 over 200 random cases; its source computes the D0 score independently of its closed expression. I also ran an in-memory Python scalar grid: 4,200 cases, n=20,...,219 and rhat=-1,-0.9,...,1, with maximum absolute discrepancy 2.3874235921539366e-12. This is a formula check, not evidence for an asymptotic probability assertion. The R script was not executed because it writes an additional output file.

### 7. Assembly, all C2 conclusions, containment, and statuses

The supplied SAND-R^b consumes precisely FL-R on bounded-size sets, V-R, L-feas, the polynomial Q/H bounds, the all-conditioning-set leakage bound and r_n->0, with 15rho+b<1/2. P8 additionally consumes the Q union {l} part of FL-R and W-R. P10 consumes T1-R. Thus every interface property required by the parent RM-0 is supplied, with deterministic Q containing S0 and |Q|<=K. RM-0 explicitly allows any fixed or random design; it has no polylogarithmic restriction. Its configuration and E4 premises are imported by §1. There is no independence requirement among the three lattice events or POST.

Let H_n=Sand_n(Q) intersect NA intersect TL. Its probability tends to one. On H_n, RM-0(a) gives exactly |S_tilde0 minus S0|<=|Q minus S0|<=n^b deletion moves, the certified endpoint S0 and a nonbinding cap. Its archive corollary supplies returned=S0, local_certified=true and local_limit=false, interpreted on completed SMC output runs and as hypothetical search on enumeration branches. RM-0(b) gives the common data event G_n=K_n intersect {pi(S0)>1/2} and the exact complement bound in L5 line 138. Therefore all admissible output runs report S0 on this one event, and

    P(O intersect {S_hat+ != S0})=o(1),
    P(O intersect {S_hat+ = S0})=1-P(U_n)-o(1).

This includes the conclusions referenced by C2 through C1. It makes no delivery claim. The fixed-design block-relative extension in C1 is a separate fixed-design assertion, not an additional Gaussian-row hypothesis relaxation being claimed by this proof.

For containment, parent T1-R, FL-R, V-R and L-feas are unchanged. Select, for example, b=1/8 and rho=1/120, so 15rho+b=1/4<1/2; every fixed polylogarithmic bound is eventually below both relevant powers. Parent L-R has ell'_n=C_L n^-1/2 with ell'_n sqrt(n/log n)=C_L/sqrt(log n)->0, and its rate r_n(n log n)^(1/4)->0 implies r_n(n/log n)^(1/4)->0. The accepted L4 §7 item 1 then supplies ell_n=ell'_n+15r_n²/c with ell_n sqrt(n/log n)->0 at every required U. The same H_l and r_n satisfy the new localisation condition. Parent D-R is the same centred latent reference/atom contract on P+, with its polylog size now bounded by n^b. P9 supplies W-R for any fixed delta0<1-2b. Hence the stated hypothesis implication and theorem containment hold with the same Q and H_l.

L5 §5 agrees with RM2 STATEMENT §5: RM-0@1.0.0 and E4@1.0.0 are consumed as PROVED-CHECKED; POST@1.0.1 carries “PROVED (by this seat, unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied” and C2 is conditional on it; B9 is not consumed; NA-R and D-loc are templates re-run here. No hidden promotion of the posterior input's status was found.

## Not checked

- I accepted NA-conv, NA-W, TL-W and Lemma d as directed; I checked their hypotheses and uniform thresholds, not their underlying proofs as new claims.
- I accepted SAND-R^b and L4 §1.1, §1.2(iii), §7 item 1 as directed; I checked the uses and hypothesis mapping. Other L4 lemmas are outside this seat.
- I did not independently re-prove the consumed posterior theorem, E4, the parent descent/reporting engines, or Gaussian concentration. I checked POST's applicability/status and RM-0's stated scope and conclusions.
- I did not review example claims, Form F containment, implementation arithmetic, or other numerical blocks. I inspected K11 and its recorded output and independently checked its scalar formula as described above.
- I did not read any earlier review report or mutate git state. No subagents were started.
