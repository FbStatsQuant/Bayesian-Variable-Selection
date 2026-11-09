# L1: size saturation without truth inclusion

Status: PROVED (by this seat), lemma check R02 VERIFIED (reviews/R02_lemmas_claude.md); evidence repairs in reviews/R02_disposition.md, numerics/n5_review_repairs.py, N5_saturation.json and N5_adapter_controls.json. Target T1a. No claim about truth inclusion, uniqueness, swaps or SMC discovery. Not PROVED-CHECKED.

Under statement G with fixed rho, sigma, s0 and coefficients, theta_bar!=0, p<=n-1 and p-16s0>=K=floor(n/2), with probability tending to one every start-law maximizer has size K. The probability bound is uniform over deterministic partitions with block size at most 16; in fact the event below covers all such partitions simultaneously.

## Uniform small-set event

Let v=theta'Sigma theta+sigma^2, fixed positive. Put q=X'Y/(n-1), vhat=Y'Y/(n-1). Each noise component q_j-(Sigma theta)_j is centered Gaussian with variance sigma^2/(n-1); a union bound over p<=n gives max error O_P(sqrt(log n/n)). Gaussian mean/variance calculations give vhat-v=O_P(n^-1/2): ||X theta||^2=(n-1)theta'Sigma theta, E||C epsilon||^2=(n-1)sigma^2, Var||C epsilon||^2=2(n-1)sigma^4, and Var(2 theta'X'epsilon)=4sigma^2(n-1)theta'Sigma theta. These calculations do not use n-1-p residual degrees of freedom.

For all U with |U|<=16 the exact Gram Sigma_U has eigenvalues bounded below by 1-rho; the vectors (Sigma theta)_U are bounded in norm uniformly. It follows directly by expanding quadratic forms that

Rhat_U := vhat-q_U'Sigma_U^-1 q_U = R_U+O_P(sqrt(log n/n)),

uniformly over every such U, including the empty set, where R_U=v-(Sigma theta)_U'Sigma_U^-1(Sigma theta)_U. R_U>=sigma^2 and R_U<=v. All uniform errors follow from the single maximum-coordinate event above; no independent-subset assumption is used.

For U disjoint from S0, |U|=u<=15, and null l outside U, the population conditional covariance with signal is

c_u=rho theta_bar (1-rho)/(1+(u-1)rho),

with u=0 interpreted by the same expression, giving rho theta_bar. Conditional predictor variance t_u=1-rho^2 u/(1+(u-1)rho) is positive and <=1. Population residual decrease is delta_u=c_u^2/t_u. Because u belongs to the finite set 0,...,15 and theta_bar!=0, delta_min=min delta_u>0. Hence R_U/R_{U+l}>=1+delta_min/v, uniformly for these pairs.

## Transfer to the exact shipped block score

Explicitly, s^2=vhat>=sigma^2/2 with probability tending to one. This lower bound controls both z and all residual denominators below. Near k=K the actual prior increment is O(1); the -log(2p) bound used in the proof is deliberately uniform down to k=0.

For |U|<=16, write h=n-1, G_U=h Sigma_U. The fitted coefficient matrix n[(n+1)G_U+I]^-1 differs from G_U^-1 by operator norm O(n^-2), uniformly, since its eigenvalue at g is n/((n+1)g+1) and the inverse has eigenvalue 1/g, with g>=h(1-rho). Also ||z_U||=O_P(n) uniformly because z=h q/s and s^2=vhat is bounded away from zero. Thus

Q_U = RSS_U(y)+O_P(1) = h Rhat_U/vhat+O_P(1),

uniformly. Therefore (.02+Q_U)/(.02+Q_{U+l}) converges uniformly to R_U/R_{U+l}; it is at least 1+delta_min/(2v) with probability tending to one for the pairs above. The determinant penalty log det H_U-log det(G_U+I) is |U| log n+O(1), uniformly; its increment is log n+O(1). Consequently

log m(U+l)-log m(U) >= (n/2) log(1+delta_min/(2v)) - .5 log n - O(1)

on one event of probability tending to one. Only positivity of an order-n term is needed. The prior increment at k<K is log((k+1)/(2p-1-k))>=-log(2p), so every such null addition to a truth-free block strictly improves gamma0, uniformly in the global model of size k<K, for all sufficiently large n.

## Maximizer argument

At most s0 blocks contain truth, covering at most 16s0 variables. There are therefore at least p-16s0>=K variables in truth-free blocks. Any S of size <K omits one such variable l. Its within-block selected U has at most 15 elements and no truth, so the preceding strictly improving addition applies. S cannot maximize gamma0. The event is uniform and includes every maximizing S. This proves saturation, but supplies neither which variables enter nor the subsequent path.

Boundary: p-16s0>=K holds eventually for fixed p/n in (1/2,1), and also allows p=n-1. For p-K=O(1) it need not hold; no claim there. The proof uses only bounded-size regressions, not FAC-B's residual-r bound.

Initial falsification script: numerics/n2_checks.py; output numerics/N2_checks.json (random increments alone were inadequate, R02). Repaired direct start-mode tests: numerics/n5_review_repairs.py, r02_start_dp_reference.py, N5_saturation.json; dense adapter controls N5_adapter_controls.json. T1b/T2 for production partitions remain OPEN.
