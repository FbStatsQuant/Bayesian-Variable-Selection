# W4-SHARE repairs and Astra-authored candidates

All source versions are pinned in SOURCE_MANIFEST.json. Original verdicts remain unchanged. A candidate below is not adopted and requires a Claude referee. This is an analytic proof review; no new numerical experiment is claimed.

## Re-review

D4 and D5: VERIFIED in their conditional, exact-arithmetic formulation. For D4 the event that the envelope has survived through stage t is measurable before the stage-t draws. Killing the Laplace process on envelope failure therefore gives the supermartingale inequality. The chord inequality for exp(-theta h), h in [0,1], has the required direction. For D5 separate H=0 and H=N before the weighted-average algebra; the resulting envelope is exp(-Gamma_t) product(1-eta_s). Neither theorem supplies confinement or terminal repair for BVS. The conditional B2-W4 bound remains VERIFIED with the exact product and a uniform REPAIR hypothesis.

SH: the exact binomial mixture and parts (i),(ii) remain VERIFIED. The unrestricted sharp-transition wording remains GAP. With pi0(o)=1/N, probability of no initial outsider tends to exp(-1), so extinction cannot tend to one at any fitness advantage. F-SHARE §2 repeats the erroneous assertion that order-one N*pi0(o) suffices for extinction tending to one; this is ERROR with this same counterexample. Its conditional F1/F3 statements do not use that assertion.

G: the convex-combination identity Gamma=sum Delta_t*kappa_t<=max kappa_t remains VERIFIED. The universal BVS/grid conclusion remains GAP. Neutral two-state identity mutation with repeated multinomial resampling has perfect ESS and eventually loses a class at fixed N. This proves an abstract ESS-only obstruction, not impossibility under every grid restriction for the production BVS kernel and budget. Later closed-class arguments supply additional hypotheses, not a proof of that universal claim.

M(a): VERIFIED; the Schur-complement lower bound followed by Cauchy yields max delta_j² >= (n-1)lambda² ||theta_M||_2^4/||theta_M||_1².

M(b): original ERROR and path GAP persist. Orthogonal centered p=n-1, theta=1, sigma²=1 gives exact gain/n -> log(2)/2 but quadratic term/n ->1/4. With theta²=C log(n)/n and fixed C satisfying BM-C, the crossing ratio tends to 3/C, not zero. These are analytic counterexamples, not fresh simulated data.

W5-B2ENV Prop M-LH is a narrower, valid exact-Gram/fixed-coefficient lattice replacement (VERIFIED conditional on its exact RSS expansion). It uses -nu log(RSS_new/RSS_old), not the invalid quadratic equality. Its g_* is strictly smaller than the least limiting edge gain: its denominator sigma²+sum R includes even the R_i removed by that edge. There is consequently fixed positive slack, sufficient to absorb the o(1) fluctuation and O(log n) penalties without redefining the printed g_*. This justifies its displayed crossing bound eventually. Its statements concern the lattice only, with fixed nonzero coefficients (hence BM-infinity), and not the general BM-C region. B2-LH explicitly does not depend on M-LH and still needs STAB-LH. The source reports STAB failures; those reports are not fresh validation here.

O-BGIBBS BG3 is VERIFIED as a conditional template: union-bound initial failure and first exits; on survival, sequential conditioning at each terminal particle-round gives the product bound (1-beta1)^{N(L+4)} without conditioning fresh draws on the future survival event. Its LH-lock application remains GAP as a sketch with population-gap and uniformity obligations. The p-fixed application is not a repair of p>>n. F-SHARE F1 is likewise VERIFIED as a first-exit bound, but F2 and its terminal repair remain GAP, explicitly depending on PK, DOM and sketch estimates. An uphill addition path does not establish any of these inputs.

F-SHARE Lemma 1.2 as displayed has a GAP: it states odds at initial x, but the proof uses suprema over intermediate y and a neighbor-swap Hastings multiplier absent from that display. Use its subsequent (1.1), with the supremum outside the sum and the (B+1) swap factor, as the sufficient bound; do not cite the pointwise display as proved. F-SHARE §5.2 also writes product(1-eta_s)>=exp(-T eta); this is ERROR already for one stage eta=1/2 (1/2<exp(-1/2)). The correct direction is opposite. Its proposed leaky-class theorem remains a conjecture, not a repair of D5.

F-MASKPIP N-c cites W4 M for the no-barrier interpretation. Replace that dependency by the restricted candidate below (or exact-Gram M-LH), and retain a separate traversal/deletion/REPAIR hypothesis. F-SHARE §4.1 can use an exact RSS gain bound for its stated fixed-coefficient family; its §4.3 conjecture and F2 Gaussian sketch remain independent gaps. No claim that all downstream uses are consistent is justified.

## A-REV6 candidate M-star: bounded-size favorable additions

**Astra-authored; GAP for adoption pending Claude verification.** Fix integers s,d, constants A,M,sigma²>0 and lambda>0. Let centered standardized fixed-design Gaussian regression have |S0|=s, p<=n^A, ||mu||²<=Mn, and every normalized Gram matrix R_U=X_U'X_U/(n-1), U=T union S0, have minimum eigenvalue at least lambda, for T with at most d extras and T missing truth. Assume these sets and their additions are feasible (in particular s+d<=K). Set theta_min²=M_n log(n)/n with M_n->infinity. The score is the campaign's exact ridge marginal score and Beta size prior. Then constants c,C>0 give, with probability tending to one,

    min_T max_{j in S0 minus T} [F(T+j)-F(T)] >= (c M_n-C) log n =: g_n.

For any start satisfying log kappa0(T,j)>=-lambda_n on these additions, with lambda_n=O(log n), each such T has a favorable bridge addition at every phi>=lambda_n/(lambda_n+g_n)->0. Repeating additions reaches S0 union (T minus S0) in at most s steps. No deletion, traversal-time, survival or scoring-probability conclusion is included.

**Proof.** There are at most C_s p^d models and at most s additions per model. Each normalized residual noise projection Z is standard normal conditionally on the fixed design. A Gaussian union bound gives max Z²<=C_1 log n with probability tending to one; independence is unnecessary. Noncentral chi-square lower tails and the fixed dimension bound give min RSS_T >= c_0 n with exponentially small failure per model; ||Y||²<=C_0 n with exponentially high probability. Thus normalized response residual sums of squares also have uniform order-n lower bounds. The exact ridge algebra (W1-EXP Lemmas 1.1–1.3, which uses eigenvalues, not block membership) gives uniformly

    log BF(T+j)/BF(T) = -1/2 log(n+1)
        + nu log(RSS_T/RSS_{T+j}) + O(1).

To see uniformity directly, Q_T-RSS_T^y is bounded by 1+1/(n lambda), the determinant increment differs from log(n+1) by O(1/n), and nu times the log Q/RSS correction is O(1) on the residual floor. These are deterministic bounds on the common event, so no unstated block-family lemma is needed.

Write D=(delta+sigma Z)^2=RSS_T-RSS_{T+j}. Since -log(1-D/RSS_T)>=D/RSS_T, nu/RSS_T is bounded below by a positive constant, and D>=delta²/2-sigma² Z², the likelihood gain is at least c_2 delta²-C_2 log n. The size prior increment log((|T|+1)/(2p-1-|T|)) is at least -log(2p). M(a) gives a missing j with delta²>=(n-1)lambda² theta_min². Combining proves the bound. Bridge log odds equal (1-phi)log kappa0+phi log kappa1, hence the threshold. Each addition preserves the extras and reduces the number of missing truths, proving the finite path assertion. For random X apply these conditional bounds on a high-probability design event with common constants, then add its complement. QED.

This repairs only the addition-gain part of M(b). Under BM-C the same inequality may give a positive constant crossing bound if cC-C'>0, but does not give convergence to zero. Extra deletion and actual random-order traversal remain GAP.

## A-REV6 candidate EXIT-star

**Astra-authored; GAP for adoption pending Claude verification.** Keep D5's exact sufficient condition

    Gamma - sum_s log(1-eta_s)
       <= log(N*pi0(h0)/T_e)-omega(1),

along with vanishing confinement error and uniform repair failure. If eta_s<=a<1, a sufficient stronger condition replaces the negative-log sum by sum eta_s/(1-a). For a=1/2 use 2 sum eta_s. Proof: -log(1-x)=integral_0^x (1-u)^(-1)du<=x/(1-a), and substitute in the already verified D5 bound. A coefficient-one replacement is permissible only if the additional quadratic loss sum eta_s²/(1-a) is retained or shown negligible relative to the available diverging slack.

The original coefficient-one §7 condition is ERROR: take h=1_{a}, initial population all a, neutral weights, and a one-way a-to-o mutation with retention 1/2 per round. At T=floor(1.6 log N), sum eta=T/2~0.8 log N satisfies the printed criterion (including its log T slack), yet E n_T(a)=N 2^{-T}->0, so extinction tends to one. Markov's inequality proves the contradiction. This also explains why an exact retention product must survive every downstream substitution.

## A-REV6 candidate SH-star

**Astra-authored; GAP for adoption pending Claude verification.** In SH's one-stage setting put a=pi0(a), b=1-a and assume Na,Nb->infinity. Let L=N a exp(-kappa)/b. If L->infinity, extinction probability tends to zero; if L->0, it tends to one. If L->ell in (0,infinity), it tends to exp(-ell). Proof: binomial counts concentrate relative to Na and Nb. Conditional survivor probability q=n0/[n0+(N-n0)exp(kappa)] obeys Nq=L(1+o_P(1)) in the finite-L regime; then (1-q)^N->exp(-ell). For L->infinity, Nq->infinity (also if q is not small), and for L->0, Nq->0. Bounded convergence in probability passes these conditional extinction probabilities to expectations. Boundary cases Nb=O(1) must instead retain the exact binomial mixture.
