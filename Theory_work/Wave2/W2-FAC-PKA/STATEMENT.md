# W2-FAC-PKA statement v2 — LOCKED target programme

R01 LOCK-WITH-CHANGES applied (reviews/R01_disposition.md). These are targets, not established conclusions. Independent of W2-FAC-PK; no method change adopted.

## Explicit hypotheses

R02 wording clarifications: theta_bar is computed in the column-sign frame with positive-CS Gram; a global sign flip preserves its nonvanishing. SoP G is Theory_work/State_of_Project/sections/04_theory.tex:74. Taking raw X already centered with column norm squared n-1 makes standardization return X; centering raw response yields Y=X theta+C epsilon and then y=Y/s. Exact neighbor ties use lexicographic order of the resulting sorted internal-index model (proper prefix first), not scan order.

G: fixed centered standardized X, X'X=(n-1)Sigma, Sigma=(1-rho)I+rho11', fixed rho in (0,1). Y=X theta+C epsilon, C=I-11'/n, epsilon~N(0,sigma^2 I), sigma>0 fixed. y=Y/s, s^2=Y'Y/(n-1). Support S0 has fixed size s0>=1 and fixed nonzero coefficients, positions arbitrary. Column signs can be absorbed. Assume theta_bar=sum theta!=0 for saturation. Truth inclusion is not assumed; FAC-B FS nonvanishing does not establish it under saturation.

Primary P': p/n->c in (1/2,1), p<=n-1, K=floor(n/2). Boundary cases p-K=O(1) and n-1-p=o(n) are separate. Saturation alone targets the wider p-16s0>=K. Iid Gaussian population-CS is a chosen additional model for p>=n, not a necessary one; fixed p/n>1 and p/n->infinity with p<=n^A are distinct evidence targets.

Partition: uniform claims concern every deterministic partition with blocks of size <=B=min(floor(sqrt(n)),floor(sqrt(p)),16). This includes deterministic exact-CS linkage tie conventions. Finer allocation/path results must specify the block profile and truth placement. An arbitrary allowed partition is not claimed to be the production partition.

D0: G_U=X_U'X_U, z_U=X_U'y, H_U=(n+1)G_U+I, Q_U=y'y-n z_U'H_U^-1 z_U, nu=.01+n/2. log m(U)=constant-.5 log(det H_U/det(G_U+I))-nu log(.02+Q_U); w(k)=1/[2 binom(2p-1,k)], F=log w+log m. gamma0(S) proportional to w(|S|) product_b m(S intersect C_b)/m(empty), |S|<=K. Sources: Theory_work/State_of_Project/sections/04_theory.tex:70 (data), Theory_work/State_of_Project/sections/04_theory.tex:71 (score), Theory_work/State_of_Project/sections/04_theory.tex:72 (prior), Theory_work/State_of_Project/sections/04_theory.tex:73 (start).

Method: Scripts/SMC_BVS/core; complete flip/swap scans; best strict improvement, lexicographic neighbor ties. LS0 emitted centre is an exact start maximizer (e4'); EX-A, EX-S, SR, GUARD-W, OP-LS0 and complete scans are premises. LS0 cap a=ell+|start|, ell=ceil(log2(n+p+1)); final search retains ell and precedes LS0. D_n=P(potential output and S0 not scored). Delivery additionally requires FINAL Proposition F's total fallback, ideal machine and explicit allocation, recharged if cap changes; CAL only when a cited input requires it.

## Target claims and alternatives

T0: centered standardized exact-CS designs exist iff p<=n-1. This does not settle K<p<n.

T1a: under G, theta_bar!=0, p-16s0>=K, p<=n-1, uniformly over partitions, P(every start maximizer has size K)->1.

T1b: characterize population allocation, truth inclusion and noise-selected retained nulls. Identical null blocks have population ties; no uniqueness, retained sign symmetry or truth inclusion follows from FS alone. Any allocation-gap or truth-priority hypothesis is a separately reviewed refinement, not silently assumed.

T2 (key path target): either prove P(LS0(a) scores S0)->1 in an explicitly stated subclass, with bounds for deletions, null swaps and truth-in swaps, or specify an admissible design/coefficient/partition sequence with liminf P(LS0(a) misses S0)>0. An arbitrary-partition counterexample refutes only a uniform-partition claim. Finite diagnostic misses are not asymptotic counterexamples.

Exact discovery criterion: S0 is the initial centre or a feasible neighbor of C_t for some t<=min(a,m*), m* the uncapped termination time. Arrival in d<=a+1 moves is sufficient, not necessary (a scanned neighbor need not be selected). If the path starts containing truth and uses only deletions and swaps to first arrival, d=|start|-s0+swaps, so swaps<=ell+s0+1 suffices. With A additions the identity is d=|start|-s0+2A+swaps. Failure requires checking neighborhoods, not only arrival time.

T3: conditional on T2-positive, prove D_n->0 and P(output and reported model!=S0)->0, then delivery with separate premises. Check H0 using p<=n (A=1), fixed sparse coefficients and principal Gram eigenvalues >=(n-1)(1-rho). If T2-negative, OP alone is inconclusive about D_n and full-method consistency. Full SMC/final-search discovery remains a target needing its own scored-set probability bound.

T4: prove a cap remedy if needed, including sufficiency and any claimed minimality. ell+2|start| is only a candidate, with sufficient arrival bound d<=ell+2|start|+1. General score charge is 1+(a+1)max_{k<=K}[p+k(p-k)]; update production preflight, archive and Proposition F envelopes if a increases. Final search cap remains ell.

T5: population-CS p>=n initially yields evidence and missing-input inventory, not a theorem. Missing: replacement exact reduction, X-measurable partition/start analysis, adaptive path and SMC discovery. Sparse Gaussian eigenvalues up to m_sharp=O(log n) are a separate plausible H0 input. Numerical trends do not establish limits.

Not inherited: FAC-B (P), full start S*, L3 E2 residual lower bound, L4.0(d) noise multiplier bound, retained-null sign symmetry or bulk-centre control. At p=n-1 the residual chi-square r is zero. Boundary saturation requires separate treatment of zero-increment nulls. All statuses follow protocol.
