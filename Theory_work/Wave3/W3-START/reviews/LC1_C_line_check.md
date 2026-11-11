MANIFEST 867e1c933d6fbbcbfd47b5deccf3b7f132d156fef1a29113de20e55eb5fefe38

Verdict: VERIFIED-WITH-AMENDMENTS — lemmas/L3_LEAK.md
Verdict: VERIFIED — lemmas/L5_ASM_STARTF.md

Findings

1. MINOR — lemmas/L3_LEAK.md:46–47. The sentence “all four depend only on (n, A)” is literally false: g_n, x̄_n and ς_n use z_n, which depends on p. Their uniform upper envelopes depend only on (n, A), and those envelopes suffice for the claimed uniform n₂(A). Exact repair: replace the sentence by “g⁰_n depends only on (n,A); the other three quantities admit upper bounds depending only on (n,A), uniformly over p ≤ n^A. Choose n₂(A) using these upper bounds.” Explicitly set z̄_n² = 2 log(2²¹) + 2A log n + 2 log log n, G_n = 2g⁰_n + 2z̄_n², X_n = G_n/((n−1)(1−ω̄_n)), and S_n = (G_n/2)[(1+ϑ̄_n)(1+X_n)−1]. For n ≥ n₁, these dominate g_n, x̄_n, ς_n respectively. Choose n₂ with X_n ≤ 1/2 and S_n ≤ 1 thereafter. No statement change or new hypothesis is needed.

2. MINOR — lemmas/L3_LEAK.md:102–104. The displayed default-level “charge ... in ϱ_n” omits the multiplier |Q|+1. The preceding line 100 includes it correctly. Exact repair: say “a charge ... in ϱ_n/(|Q|+1), hence (|Q|+1) times this charge in ϱ_n.” Retain the final exponent threshold as a threshold for this normalized charge, or qualify it by bounded |Q|. With growing Q that threshold alone does not imply that the contribution to ϱ_n tends to zero. This is a correction to the explanatory remark, not to F4's proved bound or hypotheses; STATEMENT.md:267–269 already includes the multiplier and its required growth restriction. Its subsequent informal per-column charge can be read as the normalized charge.

No CRITICAL or MAJOR finding. Neither issue invalidates the leakage bridge, ASM, or START-F. I found no mismatch in the cited L1/L2/L4 conclusions that L3/L5 actually use. I found no additional hypothesis required for (C1) or (T1)(a)–(d).

Checks performed

Frozen inputs and scope

- Read the brief first, then the manifest and INPUTS.txt. Independently computed SHA-256 for all 47 listed content entries; every entry matched. The digest line above is copied verbatim from the manifest. No other review, LOG, or CHECKPOINT was read. No registry result was used as a premise.
- Read all lines of L3 and L5; compared the definitions, hypotheses and conclusions with STATEMENT.md §§1–4, §5.1 (C1), §5.2 (B1)/(B-L), §5.3 (T0)/(T1)/(F4), and the uniformity consumed in (T3)(a). Read the cited L1 statements and L2/L4 interfaces and propositions. Accepted L1/L2/L4 results as directed, rather than independently certifying those files.

L3.1: J0–J4 (lines 9–21)

- Factoring out exp(d²/(2t²)), symmetry replaces the linear exponential by cosh; exp(σ²z²/(2t²)) ≥ 1. This gives the stronger P(|Z|≤1) lower bound and hence 1/4, for either sign of d and every h≥1, including t=σ.
- Completing the Gaussian square gives J1 with denominator t²−σ² only when t>σ. Cancelling at most the standard Gaussian quadratic gives J2's exact factor 2h/sqrt(2π). At d=0,t=σ the integrand is constant, giving J3. Monotonicity J4 follows from nonnegativity. None uses independence between directions.

L3.2: levels, budget and domination (lines 25–40)

- GF-16 makes each residualized block direction nonzero; its unit-vector noise projection is standard normal. At most 2¹⁵ subsets per column times the two-sided tail factor 2 gives 2¹⁶, with no independence requirement. Default z_n yields exactly the stated upper bound 1/(32 log n).
- The partition and levels are deterministic in Setting F. In a conditional-design use, conditioning is on the design, not on the truncation event or response. No conditioning-set-dependent level is introduced.
- B1(i) is inclusion of the block conditioning family in all sets of size at most 15; B1(ii) includes the base truth configuration in that block family. For B1(iii), proper subsets of S₀ enter the leading maximum. If a block contains all nonempty S₀, it is the unique such block and has at most 16−s₀≤15 nulls; their residual mean is zero and τ=σ. The added 15 sqrt(2/π) z_n/p covers them even for unequal h_l. For s₀=0 every base configuration is empty, μ=0, and equality with the separately defined leading functional holds.

L3.3: step bound and small gains (lines 44–63)

- With the uniform-envelope clarification in finding 1, g_n=O(log n), x̄_n=O(log n/n), ϑ̄_n=O(n^(−1/3)), and ς_n=O(n^(−1/3) log n)→0. Merely ω_n→0 would not justify this step; the stronger rate ω_n log n→0 from L2 is available.
- TK-d supplies −(1/2)log(n+1) and the additive 2κ_E. TK-e gives the exact RSS decrement (δ+σZ)². The inequality (δ+σZ)²≤2δ²+2σ²Z²≤τ²g_n and TK-a bound x by x̄_n. Applying TK-f(f3) gives an excess over (δ+σZ)²/(2τ²) of at most ς_n. Thus the bound with e^(2κ_E+1) follows, and retaining ς_n proves the e^(2κ_E+o(1)) form requested in B-L.
- J0 and J≤p sqrt(n) imply δ²/τ²≤2 log(4p)+log n≤g⁰_n. Each summand maximum is at most p times its averaged functional. This proves SG-b, SG-0 and SG with exactly their stated conditioning families. SG-0 needs only the base truth configuration; it does not quietly require a bound on all intermediate null additions.

L3.4: bridge (lines 67–89)

- The maximum of the positive step ratios is bounded by the sum of their truncated exponential bounds on E^blk intersect Z_h. Outside that event no pointwise comparison is asserted.
- E V is an unconditional Gaussian expectation under the fixed design, so each term equals J without needing independence or Gaussianity after conditioning on Z_h. Bounding the sum over each column's conditioning sets by 2¹⁵ times its largest J gives c_L=2¹⁵ exp(2κ_E+1). Markov and the two event complements yield precisely (a).
- If [p]\Q is empty, both U_Q and its proposed scale are zero. The proof correctly handles that case before dividing by the scale. Otherwise J0 makes the scale positive.
- For (b), s₀<K≤p ensures 2p−1−s₀≥p and nonempty null set. The prior factor is at most (s₀+1)/p. There is only one base conditioning set per column, so E V₀=L^(b,0), with no 2¹⁵ loss. The resulting finite-n tail bounds imply the claimed O_P statements once the toolkit and level failure probabilities vanish. I found no counterexample exploiting large intermediate gains: the appropriate small-gain bound is forced by the respective premise before linearization.

L3.5: F4 (lines 93–104)

- For n≥4 both levels in the minimum exceed 1. Exponentiating minus one-half the squared minimum gives the maximum of the two tails, yielding the stated budget, which tends to zero for bounded |I_n|.
- J2 gives a prefactor sqrt(4 log log n) and log-exponent (c/2)log n + sqrt(4c log n log log n). Thus each exceptional term is n^(c/2+o(1)). For a nonempty exceptional set its gain hypothesis entails c≥0; if c<0 that set must be empty and its contribution is simply zero.
- Combining division by p with p≥n^(A_lower−o(1)) and n^(−1/2) gives exponent −(1+2A_lower−c)/2. The strict slack κ₁<(1+2A_lower−c)/2 absorbs the o(1); the stated growth condition on |Q|+1 finishes AL. The default-charge quadratic in sqrt(c) has root sqrt(4A+1)−sqrt(2A), strictly below sqrt(1+2A) for A>0, subject to finding 2's normalization.

L5.0–L5.1: elementary bounds and ASM

- e1 follows directly from c_Q=|Q|+15s₀, including s₀=0. In e2 the logarithmic upper bound x is at most 1/2+1/3=5/6; e^x−1≤2x gives exactly 2s₀Ξ+(8/3)(c_Q+1)U_Q. For e3, the second derivative is c(c+1)(1−u)^(−c−2); Taylor on [0,1/4] gives the displayed coefficient.
- In ASM(a), the interface rate makes the good event have probability tending to one; AGG-a and e2 give the stated two rates. A negligible-probability complement is legitimate even for unbounded odds: its contribution, set to zero on the good event, is o_P of any positive deterministic rate. This justifies the high-probability-to-O_P step also in (b).
- ASM(b) uses AGG-b with c=s₀+1, giving exponent s₀+3 in the Taylor constant and 16s₀+1 in the truth-block factor. B1(ii) supplies the separate premise for T₁. ASM(c) uses T0 only after establishing s₀<K eventually, and its two normalized remainders are O_P(n^(−1/2)(L^b)²) and O(n^(1/2−κ)). These vanish under precisely (C1)(c).

L5.2: uniform finite-n assertion

- λ=4c_L/ε pays ε/4 for U_Q and at most ε/4 for T₁. E^blk and X together cost at most ε/2 at the selected n₀. Z_h is paid once, at b_n(h); the proof uses restricted Markov failures rather than adding full Proposition L3.4 bounds twice. Total: ε+b_n(h).
- c₀=1/(64s₀'λ) ensures (c_Q+1)U_Q≤1/4, hence U_Q≤1/4 and c_QU_Q≤1. L4.2 therefore applies under V-c; L4.1 needs no extra leakage premise under V-m. For s₀=0, X is the sure event and Ξ=0.
- κ'=(κ+κ_V)/2 provides a strict exponent gap. The n₀ conditions absorb the truth-block remainder and enforce s₀Ξ≤1/2. Since (8/3)16=128/3<43, C=43s₀'λ covers the lattice coefficient. C' is the sum of the two nonnegative coefficients in the odds bound and therefore bounds both by one constant. Both final B1 substitutions have the correct direction.
- κ_E depends only on (g_*,M,σ²); L2's envelope and repaired n₂ are uniform in p and design; the cited n₃/n₄ depend only on the displayed constants and exponent. All remaining n₀ conditions involve only those constants and ε,κ. No maximum observed response or design-specific convergence rate enters n₀. The restriction ε∈(0,1) in the proposition loses nothing for the target's ε>0: apply it with a smaller ε when needed. Taking max(C,C') matches the single constant in (T1)(d).

L5.3: asymptotic conclusions

- Applying L5.2 at κ''>κ and defining A_n=(X_n−n^(−κ''))_+ gives exactly the asserted O_P plus o_P decomposition, including zero leakage scale when Q=[p]. Part (b) uses the same construction.
- The leading functional is bounded by L plus its explicit 15 sqrt(2/π) z_n/p allowance when s₀≥1. For s₀=0 its empty-set terms are already in L. Hence AL makes both terms in the odds rate vanish.
- In (c), T₁≥(1/2)(n+1)^(−1/2), with p>s₀ and eventual s₀<K, is the cited T0 conclusion. On the uniform good event the two remainders after division by T₁ tend to zero for fixed ε, since n^(−1/2)L²→0 and κ'>1/2. Letting ε decrease proves convergence in probability. L5.2 internally uses an even larger visibility exponent; weakening it to κ' in L5.3 is valid.

Independent numerical falsification

All new code ran inline in R; no script or numerical output file was created. Seed 771103 unless specified. R emitted locale startup warnings but completed successfully.

- Numerical integration of J on 150 combinations: t/σ in {1,1.0001,1.2,3,20}, d/σ in {−6,−1,0,0.1,2,7}, h in {1,1.01,2,4,8}. Checked J0–J3 and monotonicity at h+0.1. No violations; min J/J0=2.731752, max J/J1=1, max J/J2=1 to printed precision.
- 10,000 randomized checks each of e2 and e3, including s₀=0 and varying |Q|: no violations.
- 60 actual scored datasets, n=100,p=8, two four-column blocks, s₀ in {0,1,2}; exhaustive enumeration using the permitted scorer/helper definitions. Tested Q=S₀, an expanded Q and Q=[p]: 180 lattice configurations. Tested the odds assembly bound in all 37 cases meeting its premises. No violations. All 60 T₁ lower bounds passed; minimum sqrt(n+1)T₁=0.589262.
- 100,000 draws of four correlated standard-normal directions (common correlation 0.8), with distinct fixed levels {1,1.7,2.5,4} and differing means/residual variances. Truncated maximum never exceeded the truncated sum. Quadrature E V=26.05717; Monte Carlo mean=25.32677, discrepancy 0.8506542 estimated standard errors. This probes expectation accounting without independence; it is not an asymptotic rate proof or a realizable-design counterexample.
- Seed 771104: 9,000 scalar checks of the L3.3 linearization for A in {0.1,1,5}, n in {10^12,10^16,10^24}, with the uniform z-envelope, admissible normalized gains/noise, and RSS relative errors throughout [−ω̄_n,ω̄_n]. All cases had x̄≤1/2 and ς≤1; no violations of ν[−log(1−x)]≤gain/2+ς. Largest excess/ς=0.7406986. This checks the numerical inequality, not the scorer or probability of the toolkit event at these n.

Audit of the lead's numerical coverage

Read RESULTS_LEMMAS.md and the relevant R scripts; did not rerun their full suites. Their simulations do not establish uniformity, as the results file acknowledges. In falsify_L2_L3.R:50–63, the L3.3 diagnostic uses realized c_E and sampled gmin and filters on small mean gain only; it does not enforce n≥n₂, the fixed toolkit event, or |Z|≤z_n. It is an exploratory step-remainder check, not a test of the complete stated implication with its fixed constants. Likewise the comment/report that rho_U is checked “against omega_n” exceeds the implementation: the script records/prints them but has no corresponding violation assertion. falsify_L4_L5.R correctly labels the L4 statistic as the largest Ξ term rather than the whole sum; its L5 part checks finite-n assembly and reports first-order ratios, not uniform n₀. These coverage limitations do not supply evidence against the proofs.

Not checked

- Independent proofs of L1, L2, L4 (accepted as instructed), other theorem items, or any registry claim.
- Pinned C++/R implementation equivalence, floating-point guarantees, or random-design results beyond the uniform conditional bound needed for their transfer.
- Full reruns of the lead's suites, numerical certification of the enormous uniform n₀, or empirical proof of an O_P/o_P claim. No such finite numerical exercise can prove the asymptotic assertions.
- No git state was changed; the sole written file is this review.
