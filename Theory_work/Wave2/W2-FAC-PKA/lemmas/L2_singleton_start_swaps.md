# L2: singleton start and an early-swap obstruction to LS0-only discovery

Status: PROVED (by this seat), lemma check R04 VERIFIED-WITH-AMENDMENTS (reviews/R04_L2_claude.md); wording/citation amendments applied in reviews/R04_disposition.md. Not PROVED-CHECKED. SINGLETON_TARGET v2. This is one self-contained lemma; no use of L0/L1 as downstream inputs. Exact CS, singleton partition, fixed c in (1/2,1), p=floor(c n), K=floor(n/2), rho=1/2, sigma=1, s0 in {1,2}, truth coefficients all 1. No production-partition claim.

Method fidelity: LS0 maximizes the full F, not gamma0 (Scripts/SMC_BVS/core/cpp/v3_engine.h:97 and Scripts/SMC_BVS/core/cpp/v3_engine.h:408). The cap test follows the completed scan (Scripts/SMC_BVS/core/cpp/v3_engine.h:409), and its cap is ell+|start| (Scripts/SMC_BVS/core/cpp/v3_core.cpp:473). K is min(p,n/2) (Scripts/SMC_BVS/core/cpp/v3_score.h:40).

## 1. Gaussian representation and probability-one score domain

Because Sigma is positive definite, rank X=p; because X is centered, P_X<=C. Orthogonal Gaussian projections P_X e and (C-P_X)e are independent, which gives the independence of g and r used below.

Let h=n-1, e=C epsilon. Since X'X=h Sigma, g=X'e/sqrt(h) is N(0,Sigma). On an enlarged space take g=(eta 1+xi)/sqrt(2), with independent standard Gaussian eta and xi_j. The orthogonal residual r=||(C-P_X)e||^2 is independent chi-square with n-1-p degrees of freedom. For each n the sufficient-statistic law is unchanged by this representation. Put s^2=||X theta+e||^2/h. Then s^2 converges in probability to v=theta'Sigma theta+1, and ||e||^2/n->1; Gaussian variance calculations suffice. We work on events s bounded above and below, |eta|<=sqrt(log n), max_j|xi_j|<=2sqrt(log n), all with probability ->1. The last bound follows from p<=n and the Gaussian tail union bound.

Write z_j=b+d xi_j+f theta_j, b=(h s0/2+sqrt(h/2)eta)/s, d=sqrt(h/2)/s, f=h/(2s). Hence all null z_j are positive and truth z's exceed all null z's with probability ->1, uniformly, since the deterministic gap is f of order n and all noise differences are O(sqrt(n log n)). No independent-noise assumption on standardized y is made.

## 2. Exact singleton start

For singleton blocks the log start score at S is log w(|S|)+sum_{j in S} log BF_j plus a common constant. Every singleton marginal likelihood is strictly increasing in z_j^2: G_j=h, H_j=(n+1)h+1, and Q_j=h-n z_j^2/H_j. All Q_j are positive. The singleton population marginal covariance is s0/2 for nulls and (s0+1)/2 for truths; residual variance of Y given any one variable is >=1. Uniform Gaussian maximum bounds and s^2->v therefore imply min_j log BF_j>=b_* n for some fixed b_*>0 eventually on an event of probability ->1 (the limiting n^-1 log BF_j is -.5 log(1-a_j^2/v)>0, a_j one of these two covariances). The prior cost for any k<K is at most log(2p)=O(log n). Thus all start maximizers have size K; the selected variables are the largest K squared z_j. Truths lead all nulls, null z's are positive, so the unique null selection is the largest K-s0 xi_j. Distinct null z's have probability-one distinct values. Ordering within the selected truth set is irrelevant.

Let q_n=(K-s0)/(p-s0)->q=1/(2c), t=Phi^-1(1-q), and mu=phi(t)/q. Empirical quantile/trimmed-mean limits follow from the weak LLN applied to the iid coordinates within each row of this triangular array; no coupling across n is required. The selected threshold converges in probability to t since empirical counts above t±epsilon converge to their strictly different Gaussian probabilities; sandwich the selected sum between sums above those thresholds, control the discrepancy on [t-epsilon,t+epsilon], and then send epsilon down to zero. Gaussian first moment integrability controls the upper tail. Hence the selected-null mean ->mu in probability. In particular mu>t and mu is a finite constant. Subtracting the global mean xi, which tends to zero, gives the coupling-free centered-g version of the same limit.

Detailed justification (R05): let m=p-s0, r=K-s0 and A_n be the top-r null indices. For fixed epsilon>0, the weak LLN for indicators at t±epsilon and r/m->q imply that the smallest selected coordinate lies in [t-epsilon,t+epsilon] with probability ->1. On that event the symmetric difference of A_n and {j:xi_j>t} lies in this interval. Therefore
|m^-1 sum_{A_n}xi_j - m^-1 sum_j xi_j 1{xi_j>t}| <= (|t|+epsilon)m^-1 sum_j 1{|xi_j-t|<=epsilon}.
The right side converges in probability to (|t|+epsilon)P(|Z-t|<=epsilon), which vanishes as epsilon decreases to zero. For the unbounded truncated variable Z 1{Z>t}, first restrict |Z|<=M and apply the weak LLN; the expected discarded absolute tail is E[|Z|1{|Z|>M}]->0, so Markov's inequality controls the empirical discarded tail uniformly in m. Sending M to infinity establishes convergence of the second sum to E[Z1{Z>t}]=phi(t). Finally divide by r/m->q. This proves the trimmed mean in probability without assuming any coupling across n. The maximum-coordinate event in section 1 includes the truth coordinates, since it runs over all p. The residual-variance lower bound in section 2 guarantees a_j^2/v<1, keeping the limiting log BF finite.

## 3. Exact score identities, rederived

Put alpha=(n^2-1)/2+1, beta=(n^2-1)/2, alpha'=h/2+1, beta'=h/2, gamma_k=beta/(alpha+k beta). Sherman–Morrison gives H_U^-1=alpha^-1(I-gamma_|U| J), so quad_U=(sum_U z_j^2-gamma_|U|(sum_U z_j)^2)/alpha. Also L_k=(k-1)log(alpha/alpha')+log((alpha+k beta)/(alpha'+k beta')), L_0=0, and F(U)=log w(k)-L_k/2-nu log(.02+Q_U), Q_U=h-n quad_U, nu=n/2+.01.

For T of size k, c_T=gamma_k sum_T z_j, t_j=z_j-c_T. Expanding the quadratic forms (using gamma_{k-1}=gamma_k/(1-gamma_k)) yields

quad_{T-j}-quad_T=-(1+gamma_{k-1})t_j^2/alpha;
quad_{T-j+l}-quad_T=[t_l^2-t_j^2-gamma_k(t_l-t_j)^2]/alpha.

Therefore every deletion gain is <=Delta_k=log((2p-k)/k)+(L_k-L_{k-1})/2. At k=K~n/2, direct substitution in L shows L_K-L_{K-1}=log n+O(1/n), so Delta_K=.5 log n+log((2p-K)/K)+O(1/n), with log((2p-K)/K)->log(4c-1). Constants may depend on fixed c. No upper bound on the deletion residual statistic is needed.

If T contains all truths, t_j=d(xi_j-x_T)+f theta_j, where
x_T=gamma_k sum_T xi_j-[b(1-k gamma_k)-gamma_k f s0]/d.
The offset in square brackets divided by d is O((|eta|+1)/k) for k~n: indeed 1-k gamma_k=alpha/(alpha+k beta), and alpha-beta=1 cancels the order-n signal term in b alpha-beta f s0. Thus x_T is a shrunk selected-noise mean, up to this offset. At the initial T0, x_T0->mu by section 2.

## 4. Uniform early candidate supply

Fix C>0 and L=ceil(C log n). Consider ALL T obtained from T0 by at most L null-null swaps, not merely the chosen adaptive path. Such T have size K and contain truth. Their xi sums differ from that at T0 by at most 4L sqrt(log n); hence sup_T |x_T-x_T0|=O(log(n)^(3/2)/n)=o(1). This deterministic estimate on the maximum-coordinate event avoids adaptive independence assumptions.

Choose fixed delta>0 with delta<1/4 and 3delta<mu-t. Intersect the events |x_T0-mu|<=delta/2 and sup_T |x_T-x_T0|<=delta/2, each of probability tending to one. The empirical count of null xi in [mu-delta,mu+delta] is bounded below by a positive constant times n with probability ->1. All these points belong to T0 eventually, since its selected threshold ->t. Removing at most L leaves a retained null j with |xi_j-x_T|<=2delta<1, uniformly for the above T.

Let a_n=sqrt(1.5 log n). The number of null xi<=-a_n is binomial with expectation asymptotic to a positive constant times n^(1/4)/sqrt(log n). This diverges faster than L; elementary Gaussian tail bounds and binomial variance/Chebyshev imply that count exceeds 2L with probability ->1. Such variables are all outside T0 eventually (threshold ->t finite). At most L can have entered T, leaving an outside null l with xi_l<=-a_n. Uniform boundedness of x_T then gives

V_jl=(xi_l-x_T)^2-(xi_j-x_T)^2-gamma_K(xi_l-xi_j)^2 >=1.5 log n-O(sqrt(log n))-O(1)-O(log n/n) >=1.4 log n

eventually. All events used here have probability ->1 for each fixed C.

## 5. Adaptive residual control and strict preference for null swaps

Every G_U is nonsingular for nonempty U, because each principal Sigma_U is positive definite; this justifies the inverse comparisons and positivity of Q_U below. The empty-set case is immediate from Q_empty=y'y.

For T containing truth, RSS_T=||(I-P_T)e||^2<=||e||^2. Uniformly over T, 0<=Q_T-RSS_T/s^2<=1+2/(n-1). To see this, diagonalize G_T, whose least eigenvalue is >=h/2. The difference between its inverse and n((n+1)G_T+I)^-1, relative to G_T^-1, is (g+1)/((n+1)g+1)<=1/(n+1)+1/((n+1)g). Since z_T'G_T^-1z_T<=y'y=h, the stated bound follows. In particular psi_T=.02+Q_T<=(||e||^2/s^2)+1.02+2/h.

Define M_T=nu n d^2/(alpha psi_T). Multiplying the last bound by s^2 and using d^2=h/(2s^2), alpha~n^2/2, ||e||^2/n->1 and s bounded gives inf_T M_T>=.5-o(1). This argument controls all adaptive T containing truth and needs no lower residual chi-square bound.

For the null pair in section 4, the swap gain equals -nu log(1-n d^2 V_jl/(alpha psi_T))>=M_T V_jl>=.68 log n eventually. The logarithm's argument is positive because it is psi_{T-j+l}/psi_T; Q_U>=y'y/(n+1)>0 follows from nH_U^-1 <= n/(n+1)G_U^-1. This gain strictly exceeds every deletion gain, which is at most .5 log n+O(1). Additions are infeasible at K.

A truth-out swap cannot compete. Uniformly over considered T, t_j=f+O(sqrt(n log n)) for truth j, whereas t_l=O(sqrt(n log n)) for every outside null l. Hence t_l^2-t_j^2-gamma_K(t_l-t_j)^2<0 eventually, so every truth-out swap has negative gain. All truths are retained, so outside variables are null. The best neighbor is therefore a strictly improving null-null swap, regardless of ties between such swaps.

Induct on the first L steps: the initial T is in the family of section 4; at each step <L the best move is a null swap, keeping the next T in that family. Strict improvement guarantees the path does not terminate before L. Thus the first ceil(C log n) moves are null swaps with probability ->1, for every fixed C>0.

## 6. LS0-only cap obstruction and scope

Take C>1/log(2), so eventually L>=ell+s0+2. Set L0=ell+s0+2. Starting size k0=K, cap a=ell+K. For t<L0 scanned centres have size K; for L0<=t<=min(a,m*) they have size at least K-(t-L0)>=L0-ell=s0+2. Each feasible neighbor reduces size by at most one, so neither a centre nor any neighbor is S0. Therefore P(S0 not in N_LS0)->1. This uses no late-path description and makes no full-method failure claim.

For s0=1 the full method already scores S0 through table ingestion (Scripts/SMC_BVS/core/cpp/v3_core.cpp:372 and Scripts/SMC_BVS/core/cpp/v3_core.cpp:408); D_n=0 under the ideal output contract. For s0=2 with singleton blocks S0 is not a block-table model, but SMC/final search might still score it. Thus the result only refutes a uniform-partition LS0-alone discovery guarantee under the original cap. It neither settles production partitions nor proves a sufficient/minimal cap remedy.

Falsification: numerics/n3_singletons.py and N3_singletons.jsonl; additional two-truth, exact-enumeration and early-gain checks in numerics/n4_singleton_controls.py and N4_singleton_controls.json. Independent rederivation and simulator evidence are documented in reviews/R04_L2_claude.md and its named R04_scratch scripts/outputs. Those experiments test the conclusion and score identities; they do not numerically verify section 4's asymptotic tail-count mechanism. That step is analytic. Not PROVED-CHECKED.
