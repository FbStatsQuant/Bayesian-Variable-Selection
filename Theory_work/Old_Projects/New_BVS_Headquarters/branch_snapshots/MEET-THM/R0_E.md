# Round 0, Advisor E (raw gpt-6-astra, Codex, high; one shot): theory plan from the method alone

Verbatim copy of /home/fb31/fresh_eyes/astra/THEORY_PLAN.md (thread completed 2026-11-04 00:57 UTC). Same isolation and packet as Seat D. Advisor E leaves after Round 0. Everything in it is the author's proposal, unchecked.

---

# Theory plan for SMC-BVS v3.1

**Status: independent proposals and PROOF SKETCHES, unchecked.** Nothing below is a completed proof, a referee endorsement, or a Lean certificate. The supplied method is the object of study; references to existing project theorems in that method are not assumed true and were not investigated. This plan uses only BRIEF.md, METHOD_v3.md, METHOD_v3.1_ADDITIONS.md and selected files under code/ in this folder, plus published literature. No other machine directory was inspected.

The central opportunity is an exact-target, finite-state Feynman–Kac theory with two distinct consistency axes: increasing particles within an island, and increasing independent islands **without increasing their particle count**. The second axis works for evidence-weighted summaries because the *unnormalized* summary is unbiased. It does not generally work for equal-weight pooling. This is the mathematical foundation for the parallel story.

The central qualification is equally important: correlation does not invalidate the target or the ideal algorithm, but it can destroy practical accuracy at the declared budget. Shared variance integration, the size prior, masking, and the cap also produce dependence. Neither a restricted ESS check nor four agreeing islands certifies accuracy. Moreover, suppressing an output after a randomness-dependent resource stop does not preserve unbiasedness conditional on delivery.

## Scope, notation, and the implementation boundary

Use the v3.1 additions when they supersede v3: primary pooling is evidence-weighted; the final island count is R=4k; failed/incomplete fits return NA estimate fields; n=2 is allowed through enumeration; LS0 and the run card are additions. Statements about general R and N are mathematical extensions of the declared-budget procedure, not a claim that four islands or N=max(2500,n,p) meet an error tolerance.

Unless stated otherwise, every computational theorem has the following standing hypotheses, abbreviated **A**:

- Fixed finite data with n>=2, at least one retained nonconstant column, and nonconstant response; exact real arithmetic; K=min(p,floor(n/2)); the specified proper prior and working likelihood. Degenerate-input statements are separately identified.
- Ω={S subset of [p]: |S|<=K}; all model scores are evaluated by the prescribed formula, without clipping or screening away states. A partition into nonempty blocks of size <=B<=K is used. All exact sampling statements refer to ideal independent uniforms, not a deterministic seed treated as random by fiat.
- A successful calibration record C is frozen before final randomness. It specifies a finite increasing grid 0=φ0<...<φT=1, N>=1, R>=1, all move settings, and a finite collection H of bounded model functions. These may depend on data and C. Final streams are mutually independent conditional on C and independent of calibration.
- Every final stage uses multinomial resampling followed by the specified invariant move round. Every island completes all its stages and terminal rounds. Local searches and ledgers do not modify particles, weights, or subsequent transition laws. No selection of final runs by their values is permitted.

The last assumption is a statement about the ideal, fully executed random experiment. It does **not** follow by conditioning an actual run on `completed`; see T15 and T43. Statements conditional on C apply to any successful frozen record, whether or not calibration flags pass. A failed calibration has no posterior estimator.

Write

- a=a0+n/2, c=2b0, Y=y'y=n-1, F(S)=log varpi(S)+log m(S).
- Aφ=sum_S γ0(S)exp(φd(S)), qφ(S)=γ0(S)exp(φd(S))/Aφ; q1=π; Z=m(empty)A1; A0=Zbar0.
- d-=minΩ d, d+=maxΩ d, D=d+-d-; these are finite but usually unknown. D_V is the corresponding range on V. Bounds using them are analytical, not an extra exhaustive step of the method.
- Zi is the final evidence estimate of island i, Hi(h) its measured summary, Pi,j its conditional-update PIP. Define U_i(h)=Zi Hi(h), U_i(j)=Zi Pi,j, Zbar=R^-1 sum_i Zi, and μhat_w(h)=sum_i U_i(h)/sum_i Zi.
- Objectives **O1**: posterior/evidence accuracy; **O2**: particle/island scalability; **O3**: variable-selection accuracy. “Exact target” does not mean a normalized finite-particle estimator is unbiased or an exact posterior draw.

### Specification versus supplied code: proof obligations, not changes made here

The supplied code is v3, not an implementation certificate for v3.1. In particular, code/v3_run.R computes equal-island primary PIPs; v3.1 changes the primary estimator and adds general summaries, stacking, LS0 and run-card outputs. code/v3_preprocess.R rejects n<3 and zero input columns, whereas v3.1 changes those branches. Existing resource returns may retain a partial HPM; v3.1 requires all estimate fields to be NA.

Two less obvious issues need resolution before linking proofs to an executable:

1. code/cpp/v3_start.h computes a start-mode DP but enumerates optimal traceback ties subject to a default cap of 1,000,000. A truncated tie traversal does not establish the globally prescribed lexicographic winner. T07 gives a tie-aware DP route; the existing helper alone is not a complete LS0 certificate.
2. code/README.md describes an uncapped threshold graph without a forced partner, but the actual neighbour_graph function in code/cpp/v3_blocks.h implements the capped, forced-partner symmetric graph in the supplied method. The specification and actual function are the basis of T08–T10; the README is not reliable evidence of another implemented graph. The complete-linkage code explicitly says “typical” quadratic work; its repeated full-row recomputations do not by themselves prove the report's O(p² log p) worst-case bound.

All bitwise-reproducibility statements require a fixed arithmetic environment and deterministic reductions. Independent pseudorandom streams and exact real-valued sampling are distinct assumptions. No production code was changed or executed for this plan.

## 1. Component × property map

Each cell names candidate results, with its intended property, or states why the property is not relevant. “No” here means **nothing of that particular kind is claimed**, not that the component has no theory.

| Component | Fixed-data validity / exactness | Bias, consistency, finite error | Correlation / selection / limitations | Work, depth, reproducibility |
|---|---|---|---|---|
| Input checks and preprocessing | T01: transformations and degenerate branches | T29: perturbation scope | T01,T37: labels versus identifiable effects | T31: data and Gram costs |
| Working likelihood and evidence scale | T02: integration and contrast reduction | T02,T23: score envelopes and evidence bounds | T35–T37: selection needs a sampling model | T29,T31: score arithmetic |
| BB prior and cap | T03: normalization and size law | T33,T34: posterior-odds bounds | T03,T37: dilution, cap, nonidentifiability | T04,T06: finite cardinality and DP |
| Exact branch | T04: exhaustive posterior and decisions | T04: zero Monte Carlo error | T35: eventual fixed-p enumeration | T04,T31: E scores; streaming sums |
| Clustering and packing | T05: valid deterministic partition | T12: no posterior-error guarantee from clustering alone | T05,T12: separation sufficient, masking not encoded | T05,T31: actual block count and table bound |
| Block likelihood tables | T02,T06: exhaustive local scores | T11,T12: start discrepancy | T12,T38: shared variance and masking | T05,T31,T32: independent table tasks |
| Composite start, normalizer, sampler | T06: exact full-support law | T11,T19: mismatch enters constants | T12: orthogonal blocks need not factor | T06,T07: sum-product/max-product DP |
| Neighbour graph | T08,T09: proposal support and correction | nothing provable / not relevant: an edge threshold alone is not an accuracy certificate | T08,T38: degree and proxy movement | T08,T31: O(pB) edges, possible O(p) degree |
| Gibbs, swaps, independence move | T09: detailed balance and invariance | T10,T20: contraction under explicit bounds | T10,T38: full support is not fast mixing | T32: serial coordinate dependence within particle |
| Random-order round | T09: averaged reversibility | T17: pre-draw conditional identities | T09: realized order need not be reversible | T30,T32: stream ownership and round span |
| Multinomial resampling | T16: conditional offspring identity | T19,T42: variance and genealogical collapse | T42: high ESS can coexist with few ancestors | T31,T32: linear work and collective span |
| Pilot and candidate grid | T13: restricted ESS identity and construction | T14: full-space transfer needs missing-mass control | T38,T39: unseen modes and pair crossings | T13,T31: stage and rebuild bounds |
| Calibration and escalation | T15: conditioning on a frozen record | T16,T18: fresh-run guarantees survive calibration | T39,T43: diagnostics/selection cannot certify | T31,T32: serial rebuild/tier critical path |
| Final islands | T16,T17: unbiased unnormalized measures | T18–T21: N and R limits | T19,T20: weak versus useful constants | T30–T32: independent islands |
| Stacking | T21: ratio pooling | T21,T22: fixed-N consistency, CLT | T27,T43: baseline preservation and stopping traps | T27,T32: work grows with R, span need not |
| PIP poolings | T17: conditional-update numerator identity | T21: primary consistent in R; equal pool can retain bias | T28: threshold margins and finite-output coherence | T31: O(Rp) merge |
| General h, sizes, joint inclusion | T17: end-of-round numerator identity | T19,T21: simultaneous finite-list control | T28,T44: coherent summaries and decision transfer | T31: evaluation/storage depends on H |
| Evidence and log evidence | T16: Zi unbiased; log generally downward biased | T19,T21,T23: variance, averaging, one-sided coverage | T39,T43: no generic accuracy from agreement | T30,T31: deterministic log-sum-exp merge |
| HPM and score ledger | T25: maximum over all scored states | T25: discovery bounds and consistency | T26,T37: found mode versus truth | T27,T30: associative top-store/max merge |
| Local search | T26: improvement and local certificate | nothing provable / not relevant: optimization is not posterior sampling | T26,T41: local traps; no global implication | T26,T31,T32: bounded scans, parallel candidates |
| LS0 | T07,T26: exact start-mode launch | T25: deterministic extra discovery | T07,T38: start mode may be globally poor | T07,T32: DP and sequential search moves |
| MPMs | T28: Bayes action for Hamming loss | T28,T44: threshold-margin recovery | T28,T37: cap violation and duplicates | T31: O(p) thresholding |
| Top-store run-card mass | T24: deterministic partial partition sum | T23,T24: lower bound; optional rigorous brackets | T24,T39: observed store cannot certify omitted mass alone | T24,T31: deduplication and bounded store |
| Flip/swap and subset gaps, branch-and-bound | T26,T41: exact local/region certificates | nothing provable / not relevant: deterministic gaps need extra bounds for probabilistic calibration | T41: unresolved is not certified | T31,T41: subset scan can be exponential |
| Floating-point fallback and comparisons | T29: algebraic identities, conditional error certificates | T29: target and implementation perturbation bounds | T29: stable computation is not exact comparison | T29,T30: deterministic arithmetic assumptions |
| Status/guard/all-NA rules | T15,T43: no partial estimates relabelled complete | T43: censoring can bias delivered estimates | T39,T43: availability is not accuracy | T31,T43: preflight is an estimate unless bounded |
| Parallel execution and random streams | T30: same law; stronger bitwise conditions | T21: independent replication reduces variance | T40: no universal advantage over MCMC | T31,T32: work/span/memory limits |
| Statistical asymptotics and finite-n selection | T33–T37: explicit odds/design conditions | T34–T36,T44: finite-n and asymptotic bounds | T37,T38: correlated identifiability and masking | T44: statistical and computational budgets jointly |

## 2. Candidate theorems

There are **44 candidate theorem packages**, T01–T44. A package can contain a theorem and closely related lemmas/counterexamples. Every statement below is a **PROPOSAL, UNCHECKED**; every argument is a **PROOF SKETCH, UNCHECKED**. Difficulty concerns a publishable proof for this method. “New” means a potentially method-specific contribution, not a priority claim. Shared hypotheses A apply wherever referenced.

### T01. Preprocessing equivariance and the precise estimand

**Draft statement.** On finite nonconstant data, in real arithmetic, centering/sample-SD scaling commutes with separate nonzero affine transformations of each predictor and the response up to coordinate signs. The integrated score of every relabelled model, Z on the working scale, and its posterior probability are unchanged. Column permutations preserve the posterior after relabelling. The complete randomized procedure is permutation-equivariant only when clustering/decision ties are absent or tie-breaking labels are transported; raw numerical index tie-breaking can change its path. Dropped constant variables are outside the estimand, not variables whose posterior PIP was proved zero. For the zero-centered constant-response extension y=0, the empty model is a score maximizer and wins the prescribed tie rule; v3.1 may still suppress every estimate field on that return. With n=2, K=1 and E=1+p, the declared enumeration threshold admits every representable p passing allocation checks.

**Meaning/objective.** The target has a clear, scale-invariant interpretation; preprocessing does not establish algorithmic affine invariance in floating point. O1/O3.

**Route/key lemma.** Sign conjugation of G and H, invariance of quadratic forms/determinants; permutation bijection; direct K=1 cardinality. **Literature:** routine linear algebra; no special citation needed. **Difficulty:** routine. **Lean:** finite bijections and score identities; analytic Gaussian interpretation belongs to T02. **Dependencies:** T02 for marginal score and constant-response comparison.

### T02. Proper target, score envelopes, and contrast reduction

**Draft statement.** Under A, H=(n+1)G+I and G+I are positive definite even for rank-deficient X_S. Gaussian and inverse-gamma integration gives exactly the displayed m(S), including C_n. Put D_S=det H/det(G+I). Then 1<=D_S<=(n+1)^|S|, Y/(n+1)<=Q_S<=Y, and

`-(|S|/2)log(n+1) <= log BF(S) <= u := a log[(c+Y)/(c+Y/(n+1))]`.

Consequently every state has positive finite posterior and start mass. With beta_hat=nH^-1 z,

`Q=||y-X_S beta_hat||²+(||X_S beta_hat||²+||beta_hat||²)/n`.

The n-dimensional centered working likelihood has the same *model posterior* as the specified n-1 contrast regression with IG shape a0+1/2 and rate b0 s_y² after response rescaling; its model-independent normalizing factor is different. This is a data-dependent working prior on the raw scale, not an ordinary raw-data evidence identity. Replacing rate b by zero in a log Bayes factor changes its Q-dependent term by at most `2 a b |1/Q1-1/Q2|`; the report's n b bound omits the positive 2a0 b term and should not be used literally.

**Meaning/objective.** Perfect collinearity cannot make the mathematical score undefined, and universal finite envelopes exist. O1/O3.

**Route/key lemma.** Spectral diagonalization, Woodbury identity, completing the square, gamma integral, and the mean-value theorem for log(1+2b/Q). **Literature:** standard conjugacy; method-specific reduction/constants need checking. **Difficulty:** routine/substantial for full reduction. **Lean:** SPD/eigenvalue inequalities and Q identity; integration theorem imported or separately formalized. **Dependencies:** none.

### T03. Prior normalization, multiplicity correction, and cap conditioning

**Draft statement.** For p>=1, mixing iid inclusions with theta~Beta(1,p) gives per-model mass `w(k)=1/[2 choose(2p-1,k)]` and total mass one on all subsets. Conditioning on k<=K divides by W_K exactly once. The uncapped mean size is p/(p+1); conditioning on the cap cannot increase it. The size-mass ratio is `(p-k)/(2p-k-1)` for k<p, and the per-model addition odds are `(k+1)/(2p-k-1)`. For p>=2, successive size masses decrease at least geometrically with ratio at most q=p/(2p-1)<=2/3, giving a computable geometric upper bound on the capped or uncapped size tail after normalization. A comparison of two feasible models cancels W_K, but evidence does not. Adding retained predictors changes the prior even for old models.

**Meaning/objective.** The prior's sparsity and multiplicity adjustment can be proved exactly; a geometric size tail must not be mistaken for the stronger p-dependent size penalties of every sparse-prior theorem. O1/O3.

**Route/key lemma.** Beta integral plus binomial theorem; ratio recurrence; stochastic truncation. **Literature:** beta-binomial identities, known. **Difficulty:** routine. **Lean:** finite sums, factorial identities, tail inequality. **Dependencies:** none.

### T04. Enumeration and eventual fixed-p exact computation

**Draft statement.** For E=sum_{k<=K} choose(p,k), enumeration of each feasible subset exactly once, correct normalized prior, exact summation, and validated comparisons returns Z, all requested finite-list moments, PIPs and the prescribed global HPM exactly. Streaming needs no E-sized score store. Saturating arithmetic suffices for the branch decision if it only saturates above the comparison threshold. For every fixed p, N0>=n makes `(5H0+4N0)p` eventually exceed E<=2^p; hence the mathematical algorithm eventually takes the exact branch, conditional on supported arithmetic and sufficient allocation. This says nothing about feasible wall time for a large fixed p.

**Meaning/objective.** Fixed-p computational consistency is stronger than a Monte Carlo limit: eventual enumeration. O1/O3.

**Route/key lemma.** Enumeration bijection and finite-sum invariants. **Literature:** elementary. **Difficulty:** routine. **Lean:** an excellent first certificate, including tie order and branch predicate. **Dependencies:** T02,T03,T29 for numerical certification.

### T05. Partition guarantees, separation, and table counts

**Draft statement.** For B>=1 and a valid binary dendrogram, the size cut and next-fit packing form a partition with 1<=|C_b|<=B. Adjacent packed-block sizes have sum>B, so J<2p/B+1 and J>=ceil(p/B). Moreover `sum_b 2^|C_b| <= p 2^B/B`, including B=1,2. If a true partition has group sizes <=B and every within-group distance is strictly smaller than every between-group distance, complete linkage forms each true group before any between-group merge; cutting/packing can combine but cannot split those groups. With no separation hypothesis, no statistical quality guarantee follows from this deterministic rule. The size cut is not a correlation threshold cut.

**Meaning/objective.** Exhaustive local work is controlled and genuinely correlated separated groups can be retained intact. O1/O2.

**Route/key lemma.** Induction on tree nodes; next-fit pairing argument; `2^b/b<=2^B/B` for 1<=b<=B; complete-linkage separation induction. **Literature:** standard clustering/bin-packing facts; application-specific packaging. **Difficulty:** routine. **Lean:** all finite combinatorial cores. **Dependencies:** none.

### T06. Exact sum-product start and iid backward sampling

**Draft statement.** Under A, let `P_b(z)=sum_{U subset C_b} r_b(U) z^|U|`. If c_k is the coefficient of z^k in product_b P_b truncated above K, then `A0=sum_{k<=K} w(k)c_k/W_K`. The backwards block-size conditionals and within-size table draws yield iid π0 draws exactly, with all feasible S in support. The dependence induced by the prior and cap is retained: π0 is a product of block *factors*, not generally a product probability law over blocks. Precomputation takes O(JKB+sum_b 2^|C_b|) scalar operations beyond scoring, with O(JKB) memory if all conditional categorical arrays are materialized, or O(JK) for prefix profiles with conditional reconstruction. Sampling costs must include categorical lookup and set construction, not just J random draws.

**Meaning/objective.** Local enumeration produces an exactly normalized and sampleable global starting law, despite a nonproduct size prior. O1/O2.

**Route/key lemma.** Generating-function coefficient identity and telescoping backward conditional probabilities. **Literature:** sum-product dynamic programming, known; this prior/table combination is method-specific. **Difficulty:** routine. **Lean:** coefficient convolution and sampler probabilities. **Dependencies:** T02,T03,T05.

### T07. Exact start-mode DP and LS0 launch certificate

**Draft statement.** Under A, define `M_b(k)=max_{|U|=k,U subset C_b} log r_b(U)` locally and perform max-plus convolution across blocks, adding log w(k)-log W_K only at the final total size. With each DP state retaining a maximizing subset and a consistent lexicographic comparison at equal value, the resulting mode is the global maximizer of π0 with the prescribed size/lex tie rule. For equal-size partial sets and a fixed disjoint continuation, lexicographic order is preserved by union, justifying tie-aware traceback without enumerating all ties. Lexicographic bookkeeping adds up to O(p) per comparison in a simple implementation. LS0 is deterministic conditional on data and frozen scoring arithmetic; its evaluations enlarge the scored set without changing any estimator law. No claim identifies its mode with the posterior HPM.

**Meaning/objective.** LS0 has a global certificate for its *launch point* and a safe, deterministic search contribution. O1/O3.

**Route/key lemma.** Max-plus Bellman optimality and union-order lemma; audit the existing capped tie enumerator. **Literature:** DP known; exact tie and LS0 integration are method-specific. **Difficulty:** routine/substantial. **Lean:** max-plus recurrence and tie certificates. **Dependencies:** T06,T26,T30.

### T08. Graph size, fallback, and what its threshold does not mean

**Draft statement.** For p>1 and B>=1, choosing at most B directed neighbours per vertex, at least one, and symmetrizing produces no isolated vertex, at most pB undirected edges, and total degree <=2pB; the maximum degree can be p-1. If sqrt(2 log p/n)>=1, the strict threshold admits no correlation edge and the best-partner rule defines the graph. For any symmetric graph, the neighbour-swap reverse denominator is positive for a proposed edge and the MH correction in the method is valid. No false-edge or block-recovery probability is asserted without a stochastic design model; even under independent Gaussian columns, a heuristic for a single vertex's maximum is not a familywise guarantee over all pairs, and forced edges deliberately include null neighbours.

**Meaning/objective.** Graph proposals are valid under arbitrarily strong correlation, but degree and threshold interpretations need care. O1/O2.

**Route/key lemma.** Edge counting and explicit forward/reverse probabilities `1/(|S| |N(j)\S|)`. **Literature:** elementary MH/combinatorics. **Difficulty:** routine. **Lean:** graph support and probability ratio. **Dependencies:** T02.

### T09. Invariant elementary moves and reversible random-order rounds

**Draft statement.** Under A, every Gibbs, uniform swap, neighbour swap, and independence kernel satisfies detailed balance with qφ, including cap boundaries and self-loops. Any fixed composition preserves qφ. If the law of the list permutation is invariant under reversal and independent of the particle state, its averaged round kernel Kφ is self-adjoint on L²(qφ). A realized order need not be self-adjoint. Fresh independent orders per particle support the conditional-independence arguments used later. Caching exact scores and recording rejected proposals do not change the kernel.

**Meaning/objective.** The algorithm targets the exact bridge at every temperature; no block-independence assumption is needed. O1.

**Route/key lemma.** Detailed balance case analysis; `(K1...Km)*=Km...K1` and reversal bijection on permutations. **Literature:** standard Gibbs/MH/operator identities. **Difficulty:** routine. **Lean:** finite transition-matrix identities, permutation reversal, cap cases. **Dependencies:** T06,T08.

### T10. Uniform ergodicity from the start proposal, even with singular designs

**Draft statement.** Under A, let `Mφ=max_S qφ(S)/π0(S)=exp(φ d+)/E_π0 exp(φd)`. The independence kernel minorizes qφ by εφ=1/Mφ>=exp(-φD). A round containing that step, with any state-independent order of invariant steps before and after it, also satisfies `Kφ(S,A)>=εφ qφ(A)`. Thus `||νKφ^l-qφ||TV <=(1-εφ)^l`. No lower sparse-eigenvalue condition is needed. At φ=1, L burn-in rounds have a valid bias bound, but the declared L=O(log n) need not make it small when ε1 is tiny.

**Meaning/objective.** Correlation cannot remove reachability or the existence of convergence; it can make the explicit convergence rate nearly useless. O1/O2.

**Route/key lemma.** Bounded importance-ratio minorization and preservation of a common minorization through invariant compositions. **Literature:** independence-sampler theory is known; see [Mengersen and Tweedie (1996)](https://www.stat.rice.edu/~dcox/Stat552/Mcmc/MengersonTweedieAnnStat1996.pdf). The round-level application is a direct derivation. **Difficulty:** routine. **Lean:** finite minorization/composition and geometric inequality; TV coupling can be imported. **Dependencies:** T02,T06,T09,T11.

### T11. Discrepancy as a complete bridge-coordinate and information identities

**Draft statement.** Under A, `qφ/π0=exp(φd)/E_π0 exp(φd)` and q1=π exactly. For F(t)=log A_t at every real t, `F'=E_qt d`, `F''=Var_qt(d)`; `log E_π0 exp d = log[Z/(m(empty)A0)]`. The endpoint KL divergences sum to `E_π d-E_π0 d=integral_0^1 Var_qt(d)dt`. Bounds on D control all bridge density ratios, whereas D=0 is equivalent to π0=π. A universal finite envelope is obtained from T02: putting Lk=(K/2)log(n+1), J*=min(J,K), `-Lk-J*u <=d(S)<=u+Lk`, hence `D<=(J*+1)u+2Lk`. It is deliberately coarse.

**Meaning/objective.** The relevant computational quantity is global-to-local score discrepancy, not pairwise correlation alone. O1/O2.

**Route/key lemma.** Differentiation of a finite log-sum-exp and integration of its second derivative. **Literature:** exponential-family/thermodynamic identities known; explicit method envelope is a candidate lemma. **Difficulty:** routine. **Lean:** finite derivative identities and inequalities; integration needs standard analysis. **Dependencies:** T02,T06.

### T12. Orthogonal-block interaction and a perturbation route for correlated blocks

**Draft statement.** Under A, suppose the Gram matrix is block diagonal for the chosen partition. For a feasible S write `v_b=n z_b'H_b^-1 z_b`, `t_b=v_b/(c+Y)`; then t_b>=0, sum t_b<1, and

`d(S)=a log[ product_b(1-t_b)/(1-sum_b t_b)] >=0`.

It is strictly positive when two block contributions are positive. Therefore orthogonal predictor blocks do not make this integrated-variance composite start exact. If sum t_b<=r<1, Taylor bounds give an interaction upper bound, for example `d(S)<=a (sum_b t_b)^2/[2(1-r)]`, with a sharper pairwise version to derive. For general G_S let G_D be its block diagonal part, E=G_S-G_D, A=G_D+I, H_D=(n+1)G_D+I. If `||A^-1/2 E A^-1/2||<=δA<1` and `||(n+1)H_D^-1/2 E H_D^-1/2||<=δH<1`, log-determinant errors are bounded by `|S| max{-log(1-δ),log(1+δ)}` for each matrix, and

`|Q-Q_D| <= n [δH/(1-δH)] z'H_D^-1 z`.

If c+Q_D>0 and the last bound is <=η(c+Q_D), 0<=η<1, it gives a log-residual error <=-log(1-η). Summing these terms bounds d minus its block-diagonal formula for the same z,Y.

**Meaning/objective.** A design-dependent bridge theorem must account for shared variance and energy as well as cross-block correlation. O1/O2.

**Route/key lemma.** Additivity of determinants/quadratic gains, `product(1-t_b)>=1-sum t_b`, log expansion, relative matrix perturbation and resolvent identity. **Literature:** matrix inequalities known; decomposition is a promising method-specific result. **Difficulty:** substantial. **Lean:** scalar product inequality and matrix perturbation cores. **Dependencies:** T02,T11.

### T13. Restricted ESS geometry and honest stage-count bounds

**Draft statement.** For any finite nonempty V with positive γ0, define F_V as in the method. Then `ρ_V(u,u+δ)=1/(1+CV²)` exactly, lies in (0,1], and is nonincreasing in δ>=0, since its log derivative is `2F'_V(u+δ)-2F'_V(u+2δ)<=0`. Moreover `ρ_V>=exp(-D_V² δ²/4)`. For target ρ*=0.9 and D_V>0, every δ<=h=2sqrt(log(1/ρ*))/D_V passes. Exact maximal feasible insertion between P fixed pilot targets uses at most P+ceil(1/h) intervals up to harmless endpoint rounding. For bisection, a certified lower endpoint within h/2 of the maximal endpoint gives P+ceil(2/h); sixty halvings suffice for that accuracy only if the initial search interval divided by 2^60 is <=h/2. D_V=0 needs no insertions. Finite precision, underflow, strict progress, and the stage ceiling can still force failure. Grid equality is a finite termination criterion, not convergence of V or proof that unseen modes are absent.

**Meaning/objective.** There is a real stage-depth theorem for the restricted construction, with a numerical-resolution condition. O1/O2.

**Route/key lemma.** Convex log-sum-exp; `F''<=D_V²/4`; integrate the second finite difference; count full versus target-truncated steps. **Literature:** ESS/moment identities standard; precise grid bound method-specific. **Difficulty:** substantial. **Lean:** convexity inequalities, bisection invariant, interval-count combinatorics. **Dependencies:** T11.

### T14. The exact missing-mass correction to restricted ESS

**Draft statement.** Under A, for u<v put w=2v-u and a_t=q_t(V), where q_t is the finite exponential family even for w>1. Then

`ρ_full(u,v)=ρ_V(u,v) a_u a_w/a_v²`.

Consequently, if a_u,a_w>=1-η, the restricted guarantee implies `ρ_full>=(1-η)²ρ_V`; controlling mass only at u and v is not enough. Independently, if weights g=exp((v-u)d) lie in [l,h] and q_u(V^c)<=η, their first and second moments differ from restricted moments by bounded terms of order ηh and ηh², giving another explicit transfer bound. Without an outside-mass or weight-range bound, restricted ESS arbitrarily close to one is compatible with arbitrarily small full ESS.

**Meaning/objective.** This identifies precisely what the candidate grid knows and what an additional coverage theorem must supply. O1.

**Route/key lemma.** Substitute `A_V(t)=a_t A(t)` in the three-normalizer formula; construct a two/three-state rare-weight example. **Literature:** elementary identity; potentially useful method-specific diagnostic theorem. **Difficulty:** routine/substantial. **Lean:** finite sums and algebra, counterexample. **Dependencies:** T11,T13.

### T15. Calibration conditioning and the availability boundary

**Draft statement.** Under A, any measurable calibration rule yielding a finite legal grid and budgets independently of fresh final randomness preserves all conditional final-run identities in T16–T21. The rule may use failed diagnostics, forced pilot steps, a nonconverged grid, and tier escalation; none is needed for unbiasedness once the grid is legal. However, for a delivery event A_out depending on final trajectories, generally `E[Zi|C,A_out] != Z`. Even an unbiased random variable taking values 0 and 2Z equally can have conditional mean 2Z if only its second outcome is delivered; positive-value variants avoid the zero if desired. This applies to time guards or LS0/worker failures when their occurrence depends on sampled states or resulting search centres. Independence of A_out from all final estimates conditional on C, or guaranteed completion, is sufficient to restore conditional delivery claims.

**Meaning/objective.** Fresh final randomness protects against calibration adaptation, but all-or-nothing output suppression is not an unbiasedness theorem. O1/O2.

**Route/key lemma.** Conditional expectation and selection/censoring counterexample. **Literature:** elementary probability. **Difficulty:** routine, with substantial software-contract consequences. **Lean:** finite conditional-expectation counterexample; general disintegration imported. **Dependencies:** T16 for the preserved identity; T43 for reporting safeguards.

### T16. Finite-N unbiased evidence and unnormalized empirical measures

**Draft statement.** Under A, for every N>=1 and every bounded f on Ω, the terminal post-resampling/post-move empirical measure η_T^N satisfies

`E[Zi | C]=Z`, and `E[Zi η_T^N(f) | C]=Z π(f)`.

The result holds for every finite legal grid, arbitrary invariant move kernels (including the identity), and any number of subsequent invariant rounds. It does not assert that E η_T^N(f)=π(f). The factor m(empty)A0 and the prior normalization W_K occur exactly once. The average of R independent islands is unbiased with conditional variance Var(Z1|C)/R. By Jensen, E[log Zi|C]<=log Z, with equality only when Zi is constant, and averaging *log* estimates is not unbiased evidence pooling.

**Meaning/objective.** Evidence and unnormalized posterior information are correct at finite computational budgets without a mixing assumption. O1/O2.

**Route/key lemma.** Induct on the identity `E[offspring average(f)|particles]=weighted average(Kf)`; the unnormalized Feynman–Kac recursion telescopes. **Literature:** this is established SMC theory, not a new claim; [Del Moral, Doucet and Jasra (2006)](https://www.stats.ox.ac.uk/~doucet/delmoral_doucet_jasra_sequentialmontecarlosamplersJRSSB.pdf) is the relevant sampler reference. **Difficulty:** routine/substantial for the complete implementation match. **Lean:** finite resampling/weighting induction; probability infrastructure for expectations. **Dependencies:** T06,T09,T15.

### T17. Unbiased marked measures for conditional PIPs and general summaries

**Draft statement.** Under A, for every measured terminal round and coordinate j, the conditional inclusion probability recorded immediately before j's Gibbs draw obeys `E[Zi (N^-1 sum_i o_ij)|C]=Z π(j in S)`. Averaging over the four measured rounds preserves the identity. Likewise, for each C-measurable bounded h, measured *after each complete round*, `E[U_i(h)|C]=Zπ(h)`. Conditional on a particular state-independent step permutation, every prefix consists of invariant steps; the random location of coordinate j is therefore harmless. For a single pre-draw record, conditioning replaces the Bernoulli indicator by its expectation and decreases its conditional variance. This does not establish a variance ordering for a correlated four-round sum, an end-of-round statistic, or the evidence-weighted ratio.

**Meaning/objective.** The actual reported PIPs, not merely terminal particle indicators, support correct stacking; joint-inclusion and size summaries do too. O1/O2.

**Route/key lemma.** Extend T16 to invariant-kernel prefixes and auxiliary marks; tower property for the Gibbs draw. **Literature:** conditional expectation and Feynman–Kac marked-measure arguments are known; the within-random-scan application needs its own proof. **Difficulty:** substantial. **Lean:** finite prefix invariance and conditional Bernoulli identity; variance decomposition. **Dependencies:** T09,T16.

### T18. Particle consistency, joint CLT, and random-calibration mixtures

**Draft statement.** Under A, for fixed data, fixed C, fixed finite T and fixed R, as N→∞, Zi→Z and all finite-list island/pooled summaries converge in probability to their posterior values. The vector of evidence and unnormalized summaries has a sqrt(N) CLT, possibly degenerate; ratio limits follow by the delta method. Its covariance includes resampling ancestry, random orders, terminal rounds and PIP marks, rather than treating 4N observations as independent. If C remains random, the unconditional CLT is generally a mixture of conditional normals. If calibration changes with N, a uniform finite-error bound such as T19 with `(T_N+1)e^(2D)/N→0` supplies consistency; a single fixed-grid CLT alone does not establish that triangular-array claim.

**Meaning/objective.** Increasing particles recovers the whole finite list of posterior quantities, with honest uncertainty about the appropriate asymptotic variance. O1.

**Route/key lemma.** Finite-state conditional multinomial LLN/CLT induction with terminal marked kernels; delta method and conditioning. **Literature:** standard SMC limit theory in the preceding sampler framework; no unverified theorem number asserted. **Difficulty:** substantial. **Lean:** finite recursion and covariance identities; general CLT/delta method cited or imported. **Dependencies:** T16,T17,T19.

### T19. Explicit, design-unrestricted finite error bounds

**Draft statement.** Under A, scale potentials to `g_t(S)=exp[(φ_t-φ_{t-1})(d(S)-d-)]`, so 1<=g_t<=exp(Δφ_t D). For any reported mark taking values in [0,1], propose the universal bounds

`Var(Zi/Z | C) <= C_T/N`,

`E[{Zi(Hi(h)-πh)/Z}² | C] <= C_T/N`, where `C_T=(T+1)e^(2D)`.

The second bound also applies to conditional-update PIP marks. For R independent islands and M such quantities, a common-denominator argument gives

`P(max_h |μhat_w(h)-πh|>ε | C) <= min(1, [4 C_T/(NR)] [1+M/ε²])`,

and `P(|Zbar/Z-1|>ε|C)<=min(1,C_T/(NR ε²))`. Bounded signed h can be shifted/scaled. A deterministic denominator bound also gives a conservative ratio MSE bound of order `(T+1)e^(4D)/(NR)` for one [0,1] summary. These constants are not advertised as practical.

**Meaning/objective.** Fixed-data correctness has a nonasymptotic, all-design version, even without fast mixing. O1/O2.

**Route/key lemma.** Unnormalized empirical-measure martingale decomposition: each conditional independent sampling error has variance <=1/N times its squared envelope; past normalizer times future semigroup envelope is <=e^D. Fold all terminal mark simulation into the final particle transition, rather than adding four independent observation assumptions. Orthogonality gives T+1 terms; divide by the true scaled normalizer, which is >=1. Apply Chebyshev, a denominator event >=1/2, and a union bound. **Literature:** standard martingale technique; the displayed crude constants are this plan's proposed derivation and need line-by-line checking. **Difficulty:** substantial. **Lean:** finite martingale-difference algebra and envelope inequalities; concentration inequality imported. **Dependencies:** T11,T16,T17.

### T20. Useful variance bounds require stability, not restricted ESS alone

**Draft statement.** Under A, let Q_{s,t} be the unnormalized Feynman–Kac semigroup from stage s to t, with the actual move kernels. Derive its exact finite-N two-lineage/coalescence expansion for E[(Zi/Z)²], including initial sampling and terminal marks. A concrete sufficient-condition version to pursue is: if each log-potential range is <=b, every K_t minorizes q_t by ε>0, and `κ=e^b(1-ε)<1` uniformly, then there are finite constants C(b,ε), independent of n,p,T,N, such that for N>=C(b,ε)(T+1), relative evidence variance and centered unnormalized [0,1]-summary second moments are <=`C(b,ε)(T+1)/N`. The proof campaign must derive a valid explicit C from semigroup oscillation bounds; it is not supplied by a 0.9 ESS rule. This is a conditional stability theorem; T10's universal ε>=e^-D usually does not meet it.

For the distinct idealized algorithm that independently refreshes every particle from each q_t, the exact benchmark is `Var(Zi/Z)=product_t(1+CV_t²/N)-1`; if full CV_t²<=1/9, this is <=exp(T/(9N))-1. This ideal-refresh formula must never be substituted for the implemented kernel without a comparison proof.

**Meaning/objective.** This is the route from existence-level bounds to particles proportional to bridge depth, and states what remains to be shown. O1/O2.

**Route/key lemma.** Coalescent expansion and uniformly bounded normalized semigroups; nonlinear-flow contraction under κ<1. **Literature:** [Cérou, Del Moral and Guyader (2011)](https://www.numdam.org/item/10.1214/10-AIHP358.pdf) establishes nonasymptotic unnormalized-particle theory under regularity conditions; exact translation to these hypotheses and marked summaries is still required. **Difficulty:** hard. **Lean:** two-lineage finite recurrences; analytic stability/probability imported. **Dependencies:** T10,T13,T14,T16,T17.

### T21. Fixed-particle stacking consistency and its CLT

**Draft statement.** Under A, fix N,T,C and let R→∞ through multiples of four using iid final islands, with the baseline C and per-island N unchanged. Then almost surely `Zbar→Z`, and for every finite-list bounded h and every PIP, `μhat_w→πh`. All moments exist at fixed data/grid because `m(empty)A0 exp(d-)<=Zi<=m(empty)A0 exp(d+)`. The joint sqrt(R) CLT has summary variance

`σ_h² = Var[Zi(Hi(h)-πh)|C]/Z²`,

with the analogous cross-covariances. The equal-island pool converges instead to E[Hi(h)|C], which need not be πh at fixed N and fixed terminal mixing. Leading ratio bias is generally O(1/R); its sign is not fixed. Averaging more islands reduces evidence variance exactly by 1/R but does not guarantee a smaller realized summary error on every stacked run.

**Meaning/objective.** Adding intact independent islands is a mathematically valid route to arbitrary posterior accuracy at unchanged per-island particle count. O1/O2.

**Route/key lemma.** T16–T17 plus iid vector strong law, CLT and ratio delta method. **Literature:** self-normalized importance-ratio reasoning is classical; the method's unnormalized PIP identity is the essential adaptation. **Difficulty:** substantial. **Lean:** algebra and finite bounds; SLLN/CLT imported. **Dependencies:** T15–T17,T19.

### T22. Meaning and limitations of R_eff and island uncertainty estimates

**Draft statement.** Under T21's assumptions, `R_eff/R→Z²/E[Zi²|C]=1/(1+CV²(Zi|C))` almost surely. It measures evidence-weight dispersion across islands, not independence of particles, target coverage, or summary-specific precision. A consistent large-R estimate of the variance of μhat_w(h) is

`[1/(R(R-1) Zbar²)] sum_i [Zi(Hi(h)-μhat_w(h))]²`.

Joint covariances use the corresponding cross-products. Finite R=4 provides neither asymptotic coverage nor a reliable tail estimate. Equal Zi can coexist with poor h estimates; rare high-Z islands can be absent from all four draws.

**Meaning/objective.** R_eff gets a precise interpretation, and a principled path to large-stack uncertainty is available without pretending four islands suffice. O1/O2.

**Route/key lemma.** SLLN for first/second moments and sandwich/delta algebra; rare-island counterexample. **Literature:** standard ratio-estimator theory. **Difficulty:** routine/substantial. **Lean:** ratio and covariance identities; probability limits imported. **Dependencies:** T21.

### T23. Evidence lower bounds and optional rigorous confidence brackets

**Draft statement.** Under A, for α in (0,1), `P(α Zbar<=Z|C)>=1-α`. If any random deduplicated store Tset has exact unnormalized mass Z_Tset, then `P(max(Z_Tset,αZbar)<=Z|C)>=1-α`; independence between the store and Zbar is unnecessary because Z_Tset<=Z pointwise. This is a one-sided lower confidence bound, not a relative-accuracy interval. If certified d- and d+ are available, the deterministic island interval [z-,z+] from T21 and Hoeffding give a two-sided evidence interval of half-width `(z+-z-)sqrt[log(2/α)/(2R)]`. Similar simultaneous bounds on U_i(h) and Zi yield ratio confidence intervals after intersecting the denominator with its positive deterministic range. These are optional analytical extensions, not currently reported intervals, and may be vacuous.

**Meaning/objective.** The 0.05 evidence bound is valid and can be strengthened by stored exact mass without a multiple-testing penalty. O1.

**Route/key lemma.** Markov inequality, pointwise subset bound, bounded iid concentration and ratio interval arithmetic. **Literature:** classical inequalities. **Difficulty:** routine. **Lean:** finite inequalities and max event; probability bounds imported. **Dependencies:** T16,T21,T24,T29.

### T24. Run-card partial sums, posterior brackets, and multiplicity certificates

**Draft statement.** Under A and deduplicated exact scores, `Z_Tset=sum_{S in Tset} exp F(S)<=Z` for any data- or trajectory-dependent reported store. From T02 obtain the computable deterministic residual upper bound

`U_rest=m(empty) exp(u) [1-sum_{S in Tset} varpi(S)]`.

Thus `Z_Tset<=Z<=Z_Tset+U_rest` and, if Z_Tset>0, `π(Tset)>=Z_Tset/(Z_Tset+U_rest)`. For 0<=h<=1 and stored numerator A_Tset, `A_Tset/(Z_Tset+U_rest)<=πh<=(A_Tset+U_rest)/(Z_Tset+U_rest)`; sharper region-specific score/prior bounds improve this. Conversely, a lower bound on Z alone gives an *upper*, not lower, bound on π(Tset). If the second-best distinct scored state has score F2 and the winner F1, then `π(winner)<=1/[1+exp(F2-F1)]`; several near ties sharpen the denominator. This is an upper certificate on concentration even if the winner is not global.

**Meaning/objective.** Stored scores carry rigorous information about evidence, uncertainty and near-tie multiplicity, not only optimization progress. O1/O3.

**Route/key lemma.** Positive finite sums, prior residual mass, monotonicity of `(A+x)/(Z+x)`, and denominator lower bounds. **Literature:** elementary bounded-sum certificates; method-specific run-card use. **Difficulty:** routine/substantial. **Lean:** finite subset/ratio inequalities and deduplication. **Dependencies:** T02,T03,T25,T29.

### T25. HPM discovery, rejected proposals, and nonasymptotic success

**Draft statement.** Under A, the ledger winner is exactly the best model in the union of all scored states under the strict score/size/lex order, regardless of acceptance, cache eviction, or phase. Let S* be the globally prescribed HPM and a*=π0(S*)>0. Conditional on C, if Q independent π0 draws are scored, the probability the ledger misses S* is at most `(1-a*)^Q<=exp(-Qa*)`. Final initialization and independence proposals alone provide the deterministic count `Q=RN[1+T+L+4]` under completed fixed settings; other scoring only helps. Thus HPM recovery occurs in probability as N or R grows, and almost surely along a nested stack R→∞. For a target set A* of maximizers or ε-optimal models, replace a* by π0(A*). Discovery does not require accepting the proposed model. There is no assertion that these bounds are useful if π0(S*) is exponentially small.

**Meaning/objective.** Every scored rejected proposal contributes formally to optimization accuracy, and HPM consistency has an especially simple parallel proof. O1/O2/O3.

**Route/key lemma.** Independent proposal-miss product and monotone union of scored sets. **Literature:** elementary random-search bound; method-specific ledger use. **Difficulty:** routine. **Lean:** total-order max reduction and finite Bernoulli product; almost-sure extension imported. **Dependencies:** T06,T07,T27,T30.

### T26. Local-search monotonicity, path termination, and exact local certificates

**Draft statement.** For finite Ω, exact F and the specified frozen-centre scan, every accepted move strictly improves F, so an unrestricted search cannot revisit a centre and makes at most E-1 moves. The budgeted search scans at most ell+1 centres. A no-improvement full scan certifies only its scanned centre as flip/swap-local optimal. The returned global ledger winner is certified locally only if it is that centre and the stored scan covers its complete feasible neighbourhood; an equal-score lex change can invalidate this equality. LS0 can improve or tie the ledger but cannot lower its score. If the final allowed scan finds an improving unscanned model, that model may become the ledger winner without a local certificate.

**Meaning/objective.** Local-search flags have a precise deterministic meaning and never imply global optimality. O3/O1.

**Route/key lemma.** Strict ascent on a finite total-score order; neighbourhood enumeration. **Literature:** elementary local optimization. **Difficulty:** routine. **Lean:** finite path, scan completeness, tie edge cases. **Dependencies:** T25,T41.

### T27. Stacking preserves a baseline only if its scored work is retained

**Draft statement.** Couple the R=4 and R'=4k runs using the same frozen C, same first-four streams, same arithmetic, and the same first-four local-search start/ledger. If the expanded run retains all baseline-scored models, executes that baseline search, and then merges all added-island/search scores, its HPM score is at least the baseline HPM score and its tie-order winner is no worse. Finite-size top-M stores can be merged exactly by `top_M(union of local top_M stores)` under a fixed total order and deduplication. Every state in a global top-M list must be in a local top-M list for each source in which enough better states would otherwise displace it. Baseline preservation also requires its LS0 results: deterministic LS0 from the same start mode is reusable if scoring/search behavior is independent of the global ledger, or must be rerun. Evidence and PIP errors have no pathwise monotonicity. A genuine fixed-capacity top-M store ranked by F, as in the supplied ledger, also has nondecreasing summed mass under enlargement of the scored set: every ordered retained score is nondecreasing. This stronger run-card monotonicity needs the top-by-F rule, not merely an arbitrary truncated reported subset.

**Meaning/objective.** Stacking can guarantee nondecreasing optimization quality, but only with the baseline-work inclusion contract in v3.1 made exact. O2/O3.

**Route/key lemma.** Coupled stream-prefix equality, set inclusion and mergeable order statistics. **Literature:** standard streaming/reduction facts; baseline/LS0 issue is method-specific. **Difficulty:** substantial. **Lean:** top-M union and max monotonicity; implementation coupling obligations in T30. **Dependencies:** T07,T25,T26,T30.

### T28. MPM decisions, cap violations, and summary coherence

**Draft statement.** For the exact posterior on |S|<=K, unrestricted Hamming-loss Bayes actions include all j with PIP_j>1/2, with arbitrary choices at equality; the method chooses exclusion at equality. The exact MPM can exceed K but has size <2K and <=p. If actions are constrained to |S|<=K, the optimal Hamming action instead chooses up to K largest PIPs exceeding 1/2. If `min_j |PIP_j-1/2|=δ>0`, any uniform PIP error <δ recovers the exact threshold MPM. Fixed-list joint-inclusion indicators and size indicators accumulated on the same states obey probability/size identities exactly within their own common empirical measure and after positive island pooling. Conditional-update PIPs are measured at different within-round states: their finite-sample vector need not obey sum_j PIPhat_j<=K or exact compatibility with separately measured joint summaries. Predictive optimality of this MPM under arbitrary correlated designs is not asserted.

**Meaning/objective.** Both MPMs have a defensible decision interpretation and a clear approximation margin, but they are not automatically feasible posterior models. O1/O3.

**Route/key lemma.** Coordinatewise posterior expected Hamming loss; sum of exact PIPs equals E|S|; threshold perturbation. **Literature:** [Barbieri and Berger (2004)](https://arxiv.org/abs/math/0406464) and [Barbieri et al. (2018)](https://arxiv.org/abs/1807.08336) address predictive MPM claims under additional conditions; those cannot be transferred automatically to this ridge, cap and design. **Difficulty:** routine/substantial. **Lean:** finite decision inequalities and coherence identities. **Dependencies:** T17,T19,T21,T37.

### T29. Numerical identities, perturbation certificates, and exactness limits

**Draft statement.** Suppose approximate final log masses satisfy `|F_tilde(S)-F(S)|<=ε` for every feasible S. Then `exp(-ε)<=Z_tilde/Z<=exp(ε)`, and the normalized target satisfies `||π_tilde-π||TV<=tanh(ε)` (a conservative valid bound). A unique score winner with gap >2ε is unchanged. Interval enclosures can instead certify individual score comparisons and sums; overlapped intervals are unresolved, never exact ties. Cholesky success and the nonnegative Q identity alone do not provide those enclosures. For an implementation with transition error <=δ_t in total variation at stage t, a path coupling bounds the probability of any discrepancy by at most sum_t δ_t, with analogous bounds for initialization/resampling/terminal transitions. A score-error bound alone does not automatically control floating-point sampling or MH acceptance errors, which must be included separately. Underflow that deletes a positive state invalidates literal full-support arguments unless covered by such an error bound.

**Meaning/objective.** “Exact” can be separated into exact mathematics, stable arithmetic, and actually certified comparisons. O1.

**Route/key lemma.** Exponential mass sandwich, normalization inequalities, score-gap stability and telescoping kernel couplings; backward error/interval analysis for the scorer. **Literature:** standard perturbation techniques; no unverified implementation certificate claimed. **Difficulty:** substantial/hard. **Lean:** real-arithmetic identities and interval inequalities; floating-point correctness is a separate project. **Dependencies:** T02,T04,T09.

### T30. Serial/parallel equivalence and the random-stream contract

**Draft statement.** Under A, allocating independent island streams makes concurrent and serial execution have the same conditional law if scores, settings and reductions depend only on their declared inputs. Stronger bitwise equality requires identical island-local operation order and streams; deterministic local score results; reproducible reductions ordered by canonical island/model IDs; the same baseline/expanded search sequence; no shared mutable cache changing numerical results; and no scheduling-dependent guards or failure differences. Provenance must use the earliest canonical serial event key for a winning model, not whichever worker finishes first. A top-store/HPM merge can be associative and commutative mathematically because its key order is total, whereas floating-point addition/log-sum-exp is not associative. Particle-parallel equality to a new serial reference is possible with counter-based streams indexed by island, stage, particle and purpose, but this is the declared future path, not an existing v3.1 feature. A finite integer seed and deterministic PRNG define reproducibility, not literal iid uniforms or an R→∞ independent-stream theorem on a finite stream namespace.

**Meaning/objective.** Parallelism can preserve the statistical experiment and, under a stronger contract, its bits. O1/O2.

**Route/key lemma.** Task-dependency graph, stream ownership, deterministic reduction and coupling. **Literature:** standard parallel simulation principles; implementation-specific theorem is new work. **Difficulty:** substantial. **Lean:** stream-index injectivity, total-order reductions and dependency scheduling; PRNG quality is not proved by this certificate. **Dependencies:** T09,T15,T27,T29,T43.

### T31. Complete work and memory accounting, including omitted costs

**Draft statement.** Count arithmetic work with s(k)=O(k³) for a fresh Gram-based score and O(nk²) for QR fallback, without assuming cache hits. Let m=p+B+2, Dloc=max_{k<=K}[k+(p-k)1{k<K}+k(p-k)], and Cdraw be the actual start-sampler work. A final island costs at most order

`N s(K) + N(T+L+4)[m s(K)+Cdraw+move/bookkeeping overhead] + TN`

plus its summary evaluations. Final work multiplies by R. At tier e, pilot plus at most ell diagnostic batches costs order `(1+4ell)H_e(T_e+L+4)m s(K)`, with corresponding sampler/resampling terms, plus at most ell+1 grid constructions of O(60|V|T_e), and all local searches. Two tiers are added, not replaced by the selected tier alone. One local search costs O((ell+1)Dloc s(K)); `Dloc<=p+k0(p-k0)` with k0=min(K,floor(p/2)). The report's p+K(p-K) is a valid upper bound only in the relevant K<=p/2 range, not for all allowed K.

Preprocessing/Gram work is O(np²), table work is `sum_b 2^|C_b| s(|C_b|)`, start-profile work/memory follow T06. A direct implementation of the supplied clustering row-recomputation strategy has a conservative O(p³) distance-comparison bound, with extra lex-comparison cost at ties; O(p² log p) requires a proved implementation/algorithm choice. Dense Gram storage is Θ(p²), in addition to O(np), table entries, O(JKB) categorical data, particle model representations/factors, worker-private caches and stores, QR scratch, and O(R|H|+Rp) summaries. If per-particle state includes a p-bit mask, charge N ceil(p/w) words per island. Cache/model keys and stored subsets have nonconstant length and must be counted. Computing all proper-subset run-card gaps adds up to 2^|S_hat|-1 scores. Evaluating a user-supplied h has its own cost; boundedness is not a computational-cost bound.

**Meaning/objective.** The actual parallel budget includes calibration, initialization, summaries, and certification—not just final bridge scoring. O2.

**Route/key lemma.** Count task invocations, model-space neighbours, data structures and DP states. **Literature:** elementary complexity; code-specific proof required. **Difficulty:** substantial. **Lean:** counts/cardinality and overflow-safe bounds; empirical timing is not a theorem. **Dependencies:** T04–T08,T13,T26,T41.

### T32. Parallel work/span theorem and hard scalability ceilings

**Draft statement.** For a deterministic task graph with total work W and critical-path span S, an ideal work-conserving scheduler on P processors has time O(W/P+S), under unit-cost communication or with communication separately charged. In v3.1, island parallelism lowers final-island span to a single island's time when P>=R, but each process still executes its N particle rounds serially. Diagnostic batches parallelize over four islands; pilot, grid rebuilds, tier decisions, DP dependencies, and consecutive local-search centres remain on the critical path. Parallel scan scoring replaces Dloc score depth by one score plus a deterministic max-reduction, but cannot parallelize successive search moves. Block tables are independent tasks; model-key/score reductions remain.

For the **future** particle-parallel layer, with ideal parallel resampling/prefix primitives, a stage has span at least a serial elementary-step round of order m scores, plus resampling/reduction and communication span (often O(log N)); it is not p-variable parallelism. The full bridge needs T such synchronization stages. With worker-private copies, memory can grow as Θ(P_island p²) for Gram matrices; sharing read-only memory reduces copies only on an appropriate machine. The current dense scorer cannot handle p beyond its Θ(p²) memory limit by adding particles or islands. N0>=p makes final work at least quadratic in p per stage in the scoring-count model, even if P grows.

**Meaning/objective.** The method has a rigorous parallel axis and an equally rigorous ceiling; scaling to previously inaccessible p needs an implementation and resource regime, not just a consistency theorem. O2.

**Route/key lemma.** Work/span scheduling bound and dependency-chain lower bounds; explicit task-graph construction. **Literature:** standard parallel algorithm theory. **Difficulty:** substantial. **Lean:** finite DAG work/span accounting and deterministic reductions; machine/communication model declared externally. **Dependencies:** T30,T31.

### T33. Finite-data posterior odds and deterministic selection certificates

**Draft statement.** For a designated feasible S0, define `R(S,S0)=exp[F(S)-F(S0)]` and `A(S0)=sum_{S!=S0}R(S,S0)`. Exactly `π(S0)=1/(1+A(S0))`. If A(S0)<=η, then posterior error is <=η/(1+η), every true-coordinate PIP is >=1/(1+η), every false-coordinate PIP is <=η/(1+η), and η<1 implies both the exact HPM and MPM equal S0. For any feasible S, the log odds have the exact decomposition

`log[w(|S|)/w(|S0|)] - (1/2)log[D_S/D_S0] - a log[(c+Q_S)/(c+Q_S0)]`.

Replacing a full sum by verified classwise upper bounds yields a finite-data certificate; observing only that S0 beats all *scored* states does not bound the sum.

**Meaning/objective.** A single finite-data odds calculation links posterior concentration, HPM, PIPs and MPM. O1/O3.

**Route/key lemma.** Finite normalization and coordinate-event containment. **Literature:** elementary posterior-odds arguments. **Difficulty:** routine. **Lean:** particularly suitable finite core. **Dependencies:** T02,T03,T24.

### T34. Finite-n selection bounds from fractional posterior odds

**Draft statement.** Specify a sampling law P0 for raw data and a feasible true support S0 of size s; preprocessing is part of the random-data map. For any fixed q in (0,1), let B_q=sum_{S!=S0} E0[R(S,S0)^q]. Then

`E0[1-π(S0)]<=B_q`,

`P0(π(S0)<=1-ε) <= ((1-ε)/ε)^q B_q` for 0<ε<1.

If for every class with a deletions from S0 and b additions outside it, the fractional odds moment is bounded by M_{a,b}, then

`B_q<=sum_{(a,b)!=(0,0), s-a+b<=K} choose(s,a) choose(p-s,b) M_{a,b}`.

The same construction bounds posterior mass on oversized models, false-inclusion events or missing groups by summing only their classes. If those sums vanish, corresponding posterior/decision consistency follows. Every M_{a,b} must be derived for this ridge g=n slab, BB prior, cap and response-dependent scale; an assumed moment envelope is explicitly an assumption, not a theorem about X.

**Meaning/objective.** This provides a rigorous finite-n and growing-p framework without hiding multiplicity in an informal “beta-min” condition. O3.

**Route/key lemma.** `(sum x_i)^q<=sum x_i^q`, `A/(1+A)<=min(1,A^q)`, Markov and class counting; Gaussian quadratic-form bounds supply actual M_{a,b}. **Literature:** fractional-moment arguments are standard. [Castillo, Schmidt-Hieber and van der Vaart (2015)](https://arxiv.org/abs/1403.0735) provides relevant sparse-regression theory, but its priors/conditions are not an automatic match. **Difficulty:** routine for the reduction, hard for useful model-specific envelopes. **Lean:** fractional-sum/counting core; Gaussian integrals and concentration imported. **Dependencies:** T01–T03,T33.

### T35. Fixed-p selection consistency with a real sampling model

**Draft statement.** Let p be fixed, raw data follow `y^r=α1+X^r β*+ε`, ε~N(0,σ*²I_n), σ*²>0, with a fixed identifiable support S0. After deterministic centering/column scaling suppose `X'X/n→Σ` positive definite, coefficients on the corresponding standardized design converge to finite nonzero values on S0, and the limiting response variance is finite positive. Then propose `π(S0|data)→1` in P0 probability for the specified working posterior. Underfitted models lose an order-n residual-fit term; overfitted models lose `(extra size/2)log n+O_P(1)` in determinant penalty; finitely many comparisons complete the proof. Eventually K>=p, and eventually the algorithm enumerates by T04, so its delivered decisions and exact posterior summaries inherit this result, conditional on allocation sufficient for the exact branch. This does not prove consistency for fixed N SMC on a growing model space.

**Meaning/objective.** There is a clean baseline statistical theorem that respects the response standardization and working prior. O3/O1.

**Route/key lemma.** Uniform-over-finitely-many-models ridge-to-projection expansion, contrast chi-square residual asymptotics and model-odds comparison. **Literature:** classical BIC/g-prior consistency mechanism; this precise data-dependent-scale formulation needs verification. **Difficulty:** substantial. **Lean:** determinant expansions/finite odds reduction; LLN and Gaussian asymptotics imported. **Dependencies:** T01–T04,T33,T34.

### T36. A conservative correlated growing-p theorem, and an explicit high-dimensional frontier

**Draft statement to attempt.** In the same Gaussian raw-data model, take deterministic standardized X_n with `cI <= X_n'X_n/n <= CI`, fixed 0<c<C<infinity, fixed support size s, coefficients bounded in absolute value by Cβ, noise variance bounded above/below, and `n beta_min²/log n→infinity`. Let p_n→infinity with `p_n² log n/n→0`. Then propose posterior support consistency for the actual ridge-BB working posterior. This class permits, for example, separated blocks with fixed correlation 0.9 and bounded block size; it is not an orthogonal-design theorem. The growth condition is intentionally conservative, not claimed sharp. A proof must control overfits uniformly up to K=p_n, not silently stop at a multiple of s; a q=1/2 fractional-odds calculation suggests why a p/√n scale enters.

For p>>n, do **not** claim that theorem under a full-Gram lower eigenvalue. The proposed extension is T34 with: (i) restricted eigenvalues for unions of S0 and candidate models up to a declared size m_n; (ii) a projected-signal gap for each omitted-support class; and (iii) a separately proved fractional-odds sum over all sizes m_n<|S|<=K tending to zero. Under those three *explicit*, quantitative conditions, T34 gives consistency. Deriving (iii) from usable design conditions for this BB(1,p) prior is an open proof target here, not a borrowed result. The size prior has only geometric total-size decay, which makes that step consequential.

**Meaning/objective.** A believable first correlated-selection theorem is available, while genuinely high-dimensional selection remains a separate hard campaign. O3.

**Route/key lemma.** Uniform ridge-determinant comparison, projected Gaussian quadratic-form fractional moments, small/large-model split, response-scale concentration. **Literature:** related sparse-regression literature exists as cited in T34; no citation verified for this exact prior/slab/regime. **Difficulty:** hard. **Lean:** finite model-class sums and sufficient inequalities; random-design/quadratic-form estimates cited/imported. **Dependencies:** T02,T03,T34,T35.

### T37. Correlated identifiability limits, duplicate symmetry, and cap impossibility

**Draft statement.** If two standardized columns are identical up to sign, exchanging their labels (and coefficient sign) preserves m(S) and the exchangeable model prior. Their exact PIPs are equal. If a group of d interchangeable predictors has posterior probability 1-o(1) of selecting exactly one member, each PIP tends to 1/d while group inclusion tends to one; for d>=3 the exact MPM excludes all of them. No estimator can consistently identify which duplicate label generated an otherwise identical distribution. More quantitatively, for two raw Gaussian mean alternatives μ1,μ2 with common σ², equal-prior support-testing error is at least `(1-sqrt(KL/2))/2` when the right side is positive, with `KL=||μ1-μ2||²/(2σ²)`; bounded/tiny prediction separation obstructs label recovery. If |S0|>K, the posterior assigns S0 probability zero. Near-duplicate threshold components alone do not imply exact posterior symmetry or quantitative PIP equality without conditioning/score-perturbation bounds.

**Meaning/objective.** Exact posterior recovery remains meaningful when exact variable-label recovery is impossible; correlated group summaries can be the identifiable target. O1/O3.

**Route/key lemma.** Signed-permutation invariance, symmetry of finite sums, and two-point testing/TV inequality. **Literature:** information-theoretic support limits are also studied by [Wainwright (2009)](https://arxiv.org/abs/math/0702301), but the displayed duplicate/mean-distance argument is a direct derivation, not a claim that that paper covers this fixed design. **Difficulty:** routine/substantial. **Lean:** finite symmetry and cap exclusion; Gaussian KL/testing inequality imported. **Dependencies:** T01–T03,T28,T29.

### T38. Masking, mode crossings, and separate occupancy barriers

**Draft statement.** Consider two designated states A,B on a finite bridge, with `q0(B)/q0(A)=exp(-a)` and `d(B)-d(A)=b>0`. Their restricted odds are `exp(-a+bφ)` and the crossing is φ*=a/b when 0<φ*<1. A pair-dominated bridge with both states in V exposes this crossing in F_V'' and the restricted ESS; a V containing only A does not. If initial probability of a necessary basin is η, RN iid starts miss it with probability (1-η)^(RN). If, on histories still outside it, each of Q later proposal/transition opportunities enters with conditional probability at most ξ, the probability of ever visiting is at most RNη+Qξ. Refining the grid alone cannot remove that occupancy barrier. Additional transition opportunities can help, so it is incorrect to claim refinement has no effect whatsoever.

The regression realization to investigate is a highly correlated pair with opposing coefficients: small marginal z_j but a large joint gain when the pair is included. Use the exact ridge score and cap to demonstrate a parameter family where split-block π0 suppresses that pair while π favors it. If clustering puts the whole pair in one block, this particular block-level masking mechanism is alleviated; higher-order or cross-block masking can remain. Numerical or asymptotic examples must report the actual partition, not impose an incompatible split.

**Meaning/objective.** Temperature resolution and particle discovery are different costs of correlation/masking. O1/O2/O3.

**Route/key lemma.** Two-state logistic bridge, binomial absence probability, sequential hazard union bound; explicit 2x2/embedded Gram score algebra for the regression family. **Literature:** metastability/rare-event reasoning standard; exact family is a proposed method-specific result. **Difficulty:** substantial/hard. **Lean:** two-state formulas and finite event bounds; asymptotic regression construction separate. **Dependencies:** T02,T05,T11–T14,T25.

### T39. No diagnostic-only certificate of unseen posterior mass

**Draft statement.** In the class of arbitrary positive finite-state targets accessed only through scored states and the resulting particle/ledger summaries, fix a transcript that leaves some state unqueried. Altering that state's positive mass leaves the scores in the transcript unchanged but can make posterior mass and evidence arbitrarily different. On a coupled event avoiding that state, empirical ESS, inter-island agreement, local-search flags and the restricted grid can all agree across the two experiments. Consequently those diagnostics alone cannot yield a nontrivial uniform bound on unseen mass without score envelopes, coverage, structural assumptions, or exhaustive/valid branch bounds. This is an oracle limitation: a fixed regression dataset already determines all scores, so a claim of arbitrary score alteration *within the regression family* requires a separate realizability construction, such as the campaign in T38. The elementary oracle argument must not be oversold as that construction.

**Meaning/objective.** Passing diagnostics is useful evidence of no detected problem, never global posterior certification. O1.

**Route/key lemma.** Indistinguishable finite query transcripts and a hidden-mass perturbation; positive probability of avoiding a rare state. **Literature:** standard information/query lower-bound argument, adapted here. **Difficulty:** routine for oracle theorem, hard for sharp regression-specific version. **Lean:** finite transcript/counterexample construction. **Dependencies:** T13,T14,T38.

### T40. Comparisons with split-and-merge and plain MCMC: what is defensible

**Draft statement.** Under A, the uncorrected composite posterior π0 equals π iff d is constant on Ω. In a two-block binary model with four feasible configurations, any proposed strictly product probability law must obey `q(00)q(11)=q(01)q(10)`; an exact posterior violating this identity cannot be recovered by an uncorrected product merge. For this method's size-coupled π0, use the d-constant criterion instead of falsely calling π0 a product probability law. Tempering corrects its discrepancy without requiring variable separation. No analogous universal criticism covers split methods that retain all interactions or add an exact correction.

There is no uniform work-normalized variance or wall-time dominance over MCMC. If π0=π and exact start draws are cheap, iid draws need no bridge or burn-in; redundant resampling/moves can add cost. If a local MCMC kernel has a conductance bottleneck, independent islands and bridging can help under quantified overlap and mixing conditions, but those conditions need proof. MCMC with the same full-support independence proposal is also uniformly ergodic by T10. The distinctive provable benefits here are unbiased evidence/unnormalized summaries, local enumeration, and consistent island stacking, not an exclusive claim to correctness under correlation.

**Meaning/objective.** The paper can make a strong structural comparison without an unjustified “beats MCMC” theorem. O1/O2.

**Route/key lemma.** Density-ratio equality, 2x2 cross-product identity, easy-target counterexample and matched-kernel comparison. **Literature:** standard dependence and Monte Carlo principles. **Difficulty:** substantial for nontrivial positive comparison; routine for limitations. **Lean:** finite identities and counterexamples; conductance results imported if used. **Dependencies:** T06,T10–T12,T21,T42.

### T41. Local traps, proper-subset gaps, and budgeted region certification

**Draft statement.** On general finite capped-set score functions, strict flip/swap local maxima need not be global maxima, and can have a better proper subset obtained by deleting two or more variables. Thus a complete local scan does not certify all proper-subset gaps. For a selected model of size k, there are 2^k-1 proper subsets; a literal complete subset-gap report must evaluate them or provide a valid pruning bound. Suppose a branch-and-bound partitions a declared region into scored leaves and unvisited nodes with certified upper bounds on their maximal F. If every remaining upper bound is below the incumbent score (or resolves the total tie order), the incumbent is certified within that region. Exhaustion without this condition is unresolved. A global certificate requires covering all Ω and validated numerics; v3.1's `global_certified` field remains restricted by its specification to the exact branch.

If the run-card computation scores a previously unscored better model, the “HPM over every model ever scored” definition requires an updated ledger and recomputed relevant gaps, or an explicit distinction between the pre-card estimate and card discoveries. This ordering issue must be resolved in v3.1 implementation; passive reporting cannot silently coexist with a stale all-scored maximum. General-score lower bounds are not a proof of NP-hardness for this particular integrated score.

**Meaning/objective.** Search certificates can be formal and useful, but subset reporting has an exponential worst-case cost and a reporting-order obligation. O1/O2/O3.

**Route/key lemma.** Finite landscape counterexample, subset cardinality, branch-bound covering invariant. **Literature:** standard optimization verification; exact score-family traps are a separate construction. **Difficulty:** routine/substantial. **Lean:** excellent finite certificates, including unresolved status. **Dependencies:** T24–T26,T29,T31.

### T42. Flat weights do not prevent genealogical collapse

**Draft statement.** In multinomial resampling of N equally weighted particles, expected distinct parent indices after one resampling is `N[1-(1-1/N)^N]`. Two distinct children choose the same parent with probability 1/N. In a flat-potential experiment with identity mutation, the probability that two distinct terminal particle lineages have coalesced within t backward resampling steps is `1-(1-1/N)^t`. Empirical ESS is N throughout, yet diversity collapses. This is a counterexample to interpreting ESS as a genealogy/mixing certificate, not a claim that the method's actual nonidentity move kernel has the same law. Under q0=π and exact initialization, Zi=Z deterministically even though resampling can worsen Monte Carlo summary variance relative to independent starts.

**Meaning/objective.** Evidence accuracy, ESS and posterior-summary accuracy are distinct quantities, even on an easy bridge. O1/O2.

**Route/key lemma.** Occupancy indicators and two-lineage backward recursion. **Literature:** elementary multinomial genealogy. **Difficulty:** routine. **Lean:** finite occupancy and coalescence calculations. **Dependencies:** T16,T40.

### T43. Final-run selection, adaptive summary requests, and unavailable outputs

**Draft statement.** Under A, a fixed predeclared R and C-measurable finite H preserve T16–T23. Selecting the most favorable island, changing R based on observed Zi/PIPs without a separate stopping theorem, replacing failed final estimates by calibration estimates, or choosing h after inspecting final particles can violate their identities/coverage. For postselected h, the identity is valid only through an appropriately proved simultaneous guarantee over a predeclared class, not because every fixed h individually satisfies it. Repeating until successful completion samples a delivery-conditioned law; all-NA failure returns prevent partial estimates from being mistaken for completed estimates but do not cure that selection.

A useful unconditional reporting guarantee remains: if a hypothetical complete run has a valid bound L, and an incomplete run reports no bound (or mathematical value zero for a nonnegative lower-bound analysis), then `P(delivery and L>Z)<=α`. It does not imply `P(L>Z|delivery)<=α`; the latter can be as large as α/P(delivery). Allocation depending only on data/C is harmless for the conditional law if it guarantees completion, whereas a realized runtime guard may be informative. Availability probabilities and failures should be reported alongside accuracy.

**Meaning/objective.** This protects the precise scope of the paper's unbiasedness and confidence claims. O1/O2.

**Route/key lemma.** Conditioning, optional-selection counterexamples and joint versus conditional error events. **Literature:** standard probability/selection logic. **Difficulty:** routine/substantial for implementation governance. **Lean:** finite counterexamples and event containment; general stopping theory only if an extension is pursued. **Dependencies:** T15,T16,T21,T23,T30.

### T44. End-to-end separation of statistical and computational error

**Draft statement.** Let raw data follow P0, with true feasible S0. Suppose with P0 probability >=1-α_stat the exact posterior has π(S0)>=1-η for η<1/2. On this event exact PIPs have threshold margin at least 1/2-η. Suppose the complete computation, conditional on each such dataset and successful C, has uniform PIP error <1/2-η with probability >=1-α_MC. Then the reported primary MPM equals S0 with joint probability >=1-α_stat-α_MC. If the true posterior HPM is S0 and final independent start proposals have π0(S0)>=a_min on the same data event, the all-scored HPM succeeds with probability >=1-α_stat-exp(-Qa_min). Additional failure-to-deliver probability α_avail and certified numerical error probability α_num can be added by a union bound when a single unconditional delivered-correct-output claim is wanted. They cannot be dropped by conditioning on successful output.

For a sequence n,p_n, choose N_n,R_n,T_n so the T19/T20 computational error and proposal-miss bounds vanish alongside T34–T36 statistical error. The advertised default budgets do not automatically satisfy these conditions. For all bounded finite-list posterior summaries, combine their conditional Monte Carlo bounds with posterior concentration or contraction for the relevant estimand; accurate computation cannot repair a statistically misspecified or nonidentifiable target.

**Meaning/objective.** This joins all three objectives while keeping their distinct failure mechanisms visible. O1/O2/O3.

**Route/key lemma.** Threshold margins, proposal-miss bound, conditioning and union bounds. **Literature:** standard two-level error decomposition; method-specific assembled theorem. **Difficulty:** substantial, with hard statistical inputs. **Lean:** finite event algebra and decision implications; statistical and Monte Carlo inputs imported. **Dependencies:** T19–T21,T25,T28–T30,T33–T37,T43.

## 3. Negative results and limitations worth proving explicitly

These are proposed results, not apologetic footnotes. They define the limits of the headline and protect the paper from overclaiming.

1. **Finite normalized estimators are generally biased (T16–T22).** Unbiased evidence and unbiased evidence-times-summary do not imply unbiased PIPs. Equal-island averaging need not become correct as R grows at fixed N. The ratio-pool CLT contains summary/evidence covariance; R_eff alone does not determine it. Four measured rounds are not 4N independent observations. Rao–Blackwellization at one Gibbs draw is not a free variance-ordering theorem for every pooled estimator.
2. **Successful delivery is a selected experiment (T15,T43).** A guard can fail preferentially on large or difficult models. All estimates being NA on failure is a good output contract, but it does not establish unbiasedness among completed fits. The paper should state its ideal complete-experiment identities and separately quantify, assume away, or report delivery failures. Retrying until completed changes the law. Even “bitwise identical serial and parallel output” needs a completion/guard qualification because runtimes change with scheduling.
3. **Zero cross-block correlation does not mean zero discrepancy (T12).** Integrating one common variance makes the block Bayes factors interact through a shared residual denominator. The prior and cap further prevent treating π0 as a product probability distribution. A theorem phrased solely in terms of inter-block correlations will miss this dependence.
4. **No fixed budget works uniformly over designs and signals (T10,T19,T38).** A finite-state positive chain can have exponentially small minorization or basin probability. N0, four islands, two tiers and T0 are resource conventions, not an accuracy theorem. A finite grid with good restricted ESS can still yield a poor estimate. The universal variance constants can grow exponentially in D.
5. **Fine temperatures do not ensure occupied modes (T14,T38).** The grid sees a competing model only after it is scored and retained. Even full population ESS controls one-step weight dispersion, not all genealogical or mutation effects. The pair-dominated ideal-refresh variance formula is not a proof for the actual population kernel.
6. **No diagnostic transcript can rule out all hidden mass without more structure (T39).** This includes agreement of four island HPMs, small log-evidence SD, no local improvement, high empirical ESS and a stable candidate grid. The oracle impossibility is immediate; a sharp counterexample within the exact regression/partition family is a separate research task. A 40p+1 candidate/store ceiling can miss exponentially many modest-mass states even when it retains the HPM.
7. **No universally valid label-selection theorem under arbitrary correlation (T37).** Duplicate labels generate identical sampling laws. A strong posterior for a group can coexist with no group member in the MPM. The ridge resolves matrix singularity, not statistical identifiability. A truth larger than K has zero posterior probability. Dropping constants changes the model universe; inserting duplicate or irrelevant retained columns changes the p-dependent prior and need not leave other PIPs invariant.
8. **Local success is not global success (T26,T41).** Strict ascent and a local certificate do not imply the HPM was found. Proper-subset gaps are a stronger check than single deletions and can cost exponentially many scores. A budget-exhausted branch search is unresolved, and a region certificate does not certify its complement. Do not claim computational hardness of this specific score merely from general subset-search intuition.
9. **An MPM need not be in the support of the posterior (T28).** The exact MPM can exceed K. The empirical RB vector need not even satisfy the exact expected-size identity because its coordinates come from different conditional-update times. The general-h empirical size distribution remains coherent within its own estimator. Predictive-optimality claims require their own hypotheses and loss.
10. **The run-card lower bound is not an accuracy interval (T23,T24).** `max(Z_Tset,0.05 Zbar)` is a valid one-sided lower confidence statement under the complete experiment. It supplies no useful omitted-mass upper bound by itself. A near-tie list gives a concentration upper bound, not a certificate that all comparable models were found. Pointwise lower confidence coverage and conditional-on-delivery coverage differ.
11. **Parallel accuracy is not unlimited dimensional scalability (T30–T32).** Current Gram memory is quadratic in p. Process workers can multiply that memory. Calibration rebuilds and per-particle sequential coordinate updates impose span. More islands can lower error without increasing the dimension a single process can store. Particle parallelism and Gram-free scoring are future changes, not v3.1 facts. A finite checked stream namespace also limits literal implementable R.
12. **No universal superiority to MCMC or every split-and-merge method (T40,T42).** Some targets are already easy to sample from π0. Some MCMC algorithms use the same global independence proposal. Exact interaction-preserving split methods need not fail under correlation. Comparisons must specify the competitor, data/design class, equal work or hardware budget, and performance functional.
13. **Exact arithmetic and machine output are different theorems (T29).** Floating-point equality is not a real-number tie certificate. Stable Cholesky/QR can still misorder nearly tied models. Underflow can break full support. Finite PRNG seeds are not independent continuous uniforms. These limitations need stated numerical contracts, not a fictitious claim that every stochastic theorem is literally a theorem of the compiled executable.
14. **Response-dependent preprocessing constrains statistical transfer (T01,T02,T34–T36).** The target is a proper working posterior at the observed standardized data, but raw-data repeated-sampling proofs must account for the random scale. A theorem for an unrelated spike-and-slab or known-variance likelihood does not transfer by analogy. Fixed-p eventual enumeration cannot be used as evidence of growing-p scalability.
15. **Growing p without signal control can fail despite multiplicity adjustment (T03,T34).** Per-model prior penalties and combinatorial model counts must be balanced explicitly. BB(1,p) total-size tails are geometric; a proof that needs much stronger complexity-prior tails may fail for this prior. Small sparse eigenvalues can make the required beta-min diverge. Masked signals can be detectable jointly but hard for the algorithm to discover locally.

## 4. Design conditions: exactly where correlation matters

### 4.1 Hierarchy of assumptions

| Design/data condition | Candidate results that use it | What it buys | Does it cover genuinely correlated designs? |
|---|---|---|---|
| Arbitrary finite retained X, nonconstant y; exact score and full support | T01–T04,T06–T11,T13–T19,T21–T33,T39–T44, except their explicitly statistical or stability subclaims | Proper target, exact bridge, finite-N unnormalized identities, finite-error bounds, asymptotic N/R correctness | Yes, including rank deficiency and perfect duplicates; accuracy constants may be terrible |
| Strict within/between complete-linkage separation, groups no larger than B | T05 | True small groups are never split by clustering/cut/packing | Yes: within-group correlations can be arbitrarily high; requires a strict distance gap, not merely “block structure” |
| Actual block-orthogonal Gram matrix | Exact first part of T12 | Separates determinant interaction from shared-variance residual interaction | Allows strong correlation inside blocks; does **not** make the composite likelihood exact |
| Relative cross-block operator norms δA,δH<1 and positive residual margin c+Q_D; relative Q error <1 | Perturbation part of T12 | Quantitative score-discrepancy control, feeding T11,T13,T19 | Yes, including ill-conditioned within-block matrices because ridge-scaled norms are used; useful small constants still need signal/residual control |
| Bounds on d range or all density ratios | T10,T11,T19,T23 | Explicit overlap, minorization and conservative concentration | Correlation unrestricted as a formal matter; obtaining small bounds is the substantive problem |
| Full/restricted mass control at u and 2v-u, or bounded outside weights | T14 | Transfers restricted ESS to full ESS | Not a pure X condition; depends on y, the candidate set and the bridge |
| Uniform step range b and round minorization ε with e^b(1-ε)<1 | Conditional useful-rate part of T20 | A route to O(T/N) unnormalized relative variance | Can include correlated modes if moves bridge them efficiently; not guaranteed by the graph or temperature rule |
| Fixed-p positive-definite limiting standardized Gram, identifiable finite coefficients, Gaussian noise | T35 | Standard underfit/overfit separation | Yes, arbitrary fixed correlation with limiting minimum eigenvalue >0; excludes exact duplicates |
| Full-Gram eigenvalues between cn and Cn, fixed s, beta-min and conservative p² log n=o(n) | Proposed T36 first theorem | A first uniform growing-p support theorem | Yes: persistent nonzero correlation, e.g. bounded-size 0.9-correlation blocks; not p>>n and not correlations approaching one without rate changes |
| Sparse eigenvalues on S0∪S to size m_n, projected-signal gaps, plus an all-large-model odds-tail bound | T34,T36 high-dimensional extension | A possible p>>n selection theorem with explicit tail obligation | Yes if sparse identifiability survives; full-Gram rank deficiency is allowed; duplicates in identifiable sets are excluded |
| Nearly indistinguishable prediction vectors ||μ1-μ2||/σ small | T37 | Quantitative impossibility of exact label recovery | Precisely a highly correlated-design limitation; group/prediction recovery may remain possible |
| Masked z_j but substantial joint fit gain; actual clustering leaves relevant interaction across blocks | T38 | A bridge-discovery difficulty family | Yes, but the example must respect the prescribed partition and cap; simply forcing correlated variables into separate blocks is insufficient |

### 4.2 A useful design theorem should control both matrix and signal terms

A sensible proof chain is

`within-block capture + cross-block relative perturbation + residual-energy margin -> D or semigroup-overlap bound -> grid/mixing/particle error bound`.

The first arrow is not supplied by complete linkage alone. The squared correlations used in clustering are not the signed inverse-Gram interactions controlling suppression/masking. Unit ridge guarantees invertibility, but a relative perturbation small on the design matrix can still be large relative to a nearly exhausted residual. Orthogonal blocks remove cross-Gram interaction while retaining the common-variance interaction quantified in T12.

For selection, work with the signal gap

`Δ(S)=||(I-P_S)X_{S0}β*||²/σ*²`

on the raw/contrast scale, where P_S is the orthogonal projection onto the candidate column span. This makes masking and collinearity visible: large individual coefficients do not imply large Δ(S) if another set closely approximates their combined mean. Sparse-eigenvalue/beta-min assumptions are sufficient devices for lower-bounding Δ(S), not the scientific estimand itself. The ridge fit requires a controlled comparison to these projections and includes a shrinkage term of order determined by n, support size and coefficient energy.

Do not assume the cap “does not bind” as a consequence of its definition. Prove a posterior size-tail statement under T34's classwise bounds. Do not infer posterior contraction or exact support recovery solely from computational consistency. If p increases so fast that r_n>=1, the best-partner graph remains a valid proposal device, but its threshold has lost any sparse-edge interpretation.

### 4.3 What to report for correlated-design evidence in the paper

Alongside ordinary correlations, report block sizes and whether the relevant signal groups were split, projected-signal gaps in controlled examples, exact/approximated d distributions where enumeration is feasible, and separate occupancy, transition and weight-dispersion measurements. These are evidence for the hypotheses, not replacements for proofs. For duplicates, report group inclusion and joint/size summaries as well as PIPs; a group-summary h fixed before final randomness is already covered by T17/T21. For near duplicates, quantify score sensitivity rather than invoking exact exchangeability from the reporting threshold.

## 5. Recommended paper-1 theorem list, proof campaigns, and deferrals

I recommend **17 main theorem packages**, ranked below. Several combine candidate IDs to keep a Biometrika paper coherent; the remaining results belong in lemmas, supplementary propositions or a later paper. The ranking follows posterior accuracy, then parallel scalability, then statistical selection. The first five are my highest-priority contributions.

| Rank | Main theorem package | Candidate IDs | Essential lemmas and concrete proof-campaign finish line |
|---|---|---|---|
| 1 | End-to-end unnormalized posterior validity for the actual outputs | T15–T17 | Prior counted once; exact start; all kernel balances; random-order prefix identity; multinomial offspring expectation; marked PIP/general-h recursion; explicit completion scope |
| 2 | Consistent parallel stacking at fixed N, with joint CLT | T21,T22 | Finite island envelopes; iid vector SLLN/CLT; ratio delta method; PIP numerator identity; equal-pool contrast; R_eff limit and covariance formula |
| 3 | Local-to-global bridge geometry, including nuisance-variance interaction | T11–T14 | Endpoint identity; log-partition derivatives; orthogonal-block discrepancy; relative perturbation bounds; exact missing-mass ESS formula; validated grid count |
| 4 | Finite-N,R accuracy and a stability-refined particle/depth tradeoff | T19,T20 | Martingale envelope bound; terminal marked-kernel reduction; two-lineage expansion; verified semigroup hypotheses; simultaneous ratio bounds. If the useful-rate theorem fails, publish the honest coarse bound and exact variance recursion rather than an ESS-only rate |
| 5 | Deterministic parallel equivalence, stacking preservation, work/span | T27,T30–T32 | Stream ownership; canonical provenance; top-store merge; baseline-search inclusion; task DAG; dense-memory lower bound; corrected cost counts |
| 6 | Exact finite-state target and prior, with a precise working-model interpretation | T01–T03 | Conjugate marginal integral; Q identity; spectral bounds; contrast/scale reduction; beta-binomial normalization and cap conditioning |
| 7 | Exact local enumeration start and exact LS0 launch | T05–T07 | Tree partition and packing counts; sum-product convolution; backward sampler; max-plus mode DP; lex-union tie rule; remove dependence on capped tie enumeration |
| 8 | Move-round invariance, reversibility and global minorization | T08–T10 | Neighbour Hastings ratio; cap boundaries; reversal of compositions; independence-proposal density-ratio bound; round-level minorization |
| 9 | All-scored HPM discovery and deterministic improvement | T25–T27 | Independent start/proposal miss bounds; rejected proposals counted; cache-safe ledger; strict search ascent; baseline/expanded coupling |
| 10 | Run-card evidence, near-tie and region certificates | T23,T24,T41 | Pointwise partial sum; Markov-max bound without independence; residual mass envelope; near-tie concentration upper bound; branch-bound covering invariant; reporting-order resolution |
| 11 | Candidate-grid limitations and correlated masking examples | T13,T14,T38,T39 | Two-state crossing; full versus restricted ESS; occupancy hazard; one realizable regression masking family using actual clustering; oracle limitation clearly separated |
| 12 | Exact-branch theorem and fixed-p eventual exactness | T04 | Enumeration bijection; streaming moment accumulators; validated maximum; saturating threshold arithmetic; eventual threshold domination |
| 13 | Finite-n posterior-odds and decision-transfer theorem | T28,T33,T34,T44 | Fractional-odds class counts; threshold margins; posterior-size/joint-event variants; statistical/Monte Carlo/availability union bound |
| 14 | One honest correlated-design selection theorem | T35,T36 | Fixed-p proof first; ridge-to-projection approximation; response-scale control; underfit gap; overfit fractional moments and all-size tail. Include conservative growing-p result only after the full tail proof succeeds |
| 15 | Identifiability and MPM limitations under correlation | T28,T37 | Duplicate symmetry; group versus individual inclusion; two-point testing bound; cap exclusion; Hamming-optimal action with/without cap |
| 16 | Numerical certification and implementation contract | T29,T30 | Score-gap/target perturbation bounds; interval comparison route; sampling error accounting; canonical reductions. Separate proved algebra from unverified floating-point software |
| 17 | Diagnostic, genealogy and availability limitations | T15,T39,T42,T43 | Unseen-mass transcript construction; flat-weight ancestry calculation; censored unbiased-estimator counterexample; postselection/optional-stack warnings |

### 5.1 Proof order and finite cores for certification

A useful dependency order is:

1. **Target and finite objects:** T02,T03 -> T01,T04,T05 -> T06,T07,T08.
2. **Markov and particle identities:** T09 -> T10,T16 -> T17 -> T18,T19,T21,T22,T23.
3. **Bridge quality:** T11 -> T12,T13,T14 -> T20,T38. These sharpen rates; they are not prerequisites for basic unbiasedness.
4. **Deterministic outputs and parallel execution:** T25,T26 -> T27,T30,T31,T32, with T24,T29,T41 for certificates.
5. **Selection:** T33 -> T34 -> T35/T36, with T37 limiting the allowed scope and T44 joining statistical and computational results.

Logical dependency cycles in descriptive candidate lists are not intended proof cycles: for example, T15's calibration-preservation statement invokes T16, while T16 uses only T15's independence hypothesis, which is definitional. Similarly, LS0 needs the independent local-search invariant in T26, not the later optimization-consistency theorem.

Lean should first certify the smallest reusable finite core: model-space cardinality and cap; prior recurrences; block convolution and max-plus recurrences; tie order/merge identities; detailed-balance matrices; permutation reversal; the resampling expectation identity; unnormalized recursion; subset-sum/Markov-max event algebra; neighbourhood counts; local-search and branch-bound certificates; and missing-mass ESS algebra. Formalizing Gaussian integration, conditional expectations, LLN/CLT and all matrix perturbation analysis is a different layer. A finite certificate is valuable but must not be described as proving an imported probabilistic theorem or the floating-point executable.

For small enumerated regression instances, a proof campaign should compare exact Ω sums against start DP, transition-matrix row sums/detailed balance, marked PIP expectations and exact second moments. This is mathematical verification of the finite core, not a substitute for the symbolic proof. It is particularly important to test caps, duplicate predictors, score ties, n=2, p=1, graph stars, multiple optimal start-mode tracebacks, and resource/NA branches.

### 5.2 What I would defer

- A sharp p>>n support-recovery/contraction theorem for the exact BB-ridge/response-standardized posterior, unless the all-large-model fractional-odds tail is genuinely solved. The fixed-p and conservative correlated growing-p results do not settle this.
- Uniformly polynomial mixing or particle budgets under arbitrary correlation; such a claim is implausible without strong quantitative overlap/energy assumptions.
- A claim that the prescribed complete-linkage partition is optimal, minimizes D, or even improves D monotonically with B. Shared-variance and packing interactions prevent an obvious monotonicity theorem.
- A universal efficiency ordering against MCMC, different resamplers, or split-and-merge algorithms. First prove a tightly specified comparison family.
- A general “Rao–Blackwellization always reduces the final estimator variance” theorem. One-step variance reduction is straightforward; four-round, random-order, ratio-pooled variance requires a separate covariance/operator argument.
- Adaptive final stopping based on R_eff or evidence stabilization, reuse of final randomness for calibration, and final-data-selected summaries. These need new optional-stopping or simultaneous-inference results.
- Counter-based particle parallelism and a Gram-free scorer: important engineering/theory extensions, explicitly outside v3.1.
- Full end-to-end IEEE floating-point/PRNG verification. Begin with real-arithmetic cores and validated comparisons/enclosures on the claimed certificates.
- Predictive MPM optimality for arbitrary correlated designs with this ridge prior. Hamming optimality and approximation-margin results already provide clean, correct decisions.

## 6. The single headline theorem

### Proposed headline: exact posterior target with independent-island consistency; dependence changes the computational burden

**PROPOSAL / PROOF SKETCH, UNCHECKED.** Fix any finite standardized (X,y) in the nondegenerate v3.1 domain, allowing arbitrary column correlation and rank deficiency. Let Ω, varpi, m, π0 and d be exactly those of the method, with an exact full-support start and exact working scores. Conditional on any successful frozen calibration record C specifying a legal finite grid, N>=1 and a predeclared bounded finite collection H, execute R independent final islands completely with the specified multinomial resampling, invariant rounds, four measured rounds, and the within-round conditional PIP records. Local searches/LS0 and stores may add score discoveries but may not alter particle evolution or select estimates.

Then the proposed conclusions are:

1. **Correct target at every design:** q1=π, and every move preserves its exact bridge law; a round at φ minorizes qφ by at least exp(-φD). No block-separation, incoherence or sparse-eigenvalue assumption is required for these statements.
2. **Exact finite-budget unnormalized identities:** for every island, `E[Zi|C]=Z`, `E[Zi Hi(h)|C]=Zπh`, and `E[Zi Pi,j|C]=ZPIP_j`. These apply even when the island particles have not mixed well. They do not assert unbiased normalized PIPs or posterior draws.
3. **Two routes to exact posterior recovery:** with fixed data and grid, N→∞ at fixed R gives consistent evidence/PIPs/bounded summaries; with fixed N, R→∞ gives almost-sure consistency of averaged evidence and evidence-weighted PIPs/summaries. For each finite list, the fixed-N stack has the ratio CLT of T21. At fixed N, equal-weight pooling has no analogous general consistency guarantee.
4. **An explicit universal cost of mismatch:** writing C_T=(T+1)e^(2D), the T19 bounds give relative evidence error of order at most sqrt(C_T/(NR)) and finite-list ratio error controlled by `4C_T(1+M/ε²)/(NR)`. These are conservative probability bounds, not a promise that N0,R=4 succeed. When the additional semigroup stability assumptions of T20 hold, replace the exponential mismatch envelope by a useful constant and obtain the desired O(T/(NR)) second-moment scaling.
5. **A separate sequential-depth statement:** a globally range-controlled bridge admits a grid with steps at most `2sqrt(log(1/0.9))/D`, so a uniform such grid uses at most `max(1,ceil[D/(2sqrt(log(1/0.9)))])` stages and has full one-step ESS fraction at least 0.9. This is an *existence/comparison grid*, not a claim that the implemented restricted grid knows D or always realizes it. For the actual construction, use T13's pilot-target/bisection bound and T14's missing-mass transfer. A fixed stage ceiling can prevent output.
6. **Parallel optimization and execution:** scoring Q independent π0 proposals misses any specified global HPM S* with probability at most exp[-Qπ0(S*)]; rejected proposals count. Under the canonical-stream/reduction contract, final islands can be executed in parallel with the same law, and with additional arithmetic conditions the same bits, while their work/span and memory obey T31–T32. The present island-parallel layer does not remove dense-Gram memory or serial per-particle coordinate dependence.

**Scope of the slogan.** A defensible wording is:

> In local-to-global SMC, correlation and other block interactions change overlap, mixing, sequential depth and the particles or islands needed for accuracy; they do not change the exact target or the complete-experiment unnormalized identities.

“Correlation costs sequential depth and particles, never correctness” is acceptable only as shorthand for that statement. It is **not** a claim of exact finite-budget normalized output, monotone complexity in a correlation coefficient, uniformly manageable resources, or true-support recovery under nonidentifiability. It also does not survive unqualified conditioning on a randomness-dependent successful-delivery event. Real arithmetic/ideal streams, delivery, numerical certification, and statistical identifiability are separate scopes, explicitly exposed above.

**PROOF SKETCH.** T02,T03 give positive finite scores and the prior. T06 identifies and samples π0. The exponential tilt in T11 identifies q1. T09,T10 prove invariant kernels and minorization. T16's Feynman–Kac induction and T17's marked-prefix extension give unbiased numerators. T19 gives finite-error control and particle consistency; T21 applies iid laws to independent islands and takes ratios. T13/T14 provide the honest bridge-depth qualifications. T25,T27,T30–T32 establish discovery and parallel execution. None of those steps assumes uncorrelated predictors. Statistical support results enter only through T33–T37 and the two-level transfer T44.

## Verification record and literature boundaries

### Small checks actually run

One single-process Python calculation was run in this folder, using only standard scalar math and finite enumeration; it completed in under one second. No R/C++ production fit, simulation study, compilation, external project search, or other-directory inspection was performed. The checks are sanity checks of formulas, **not proofs or algorithm validation**:

- For orthogonal-block normalized gains t1=0.2,t2=0.3 and a=10.01, T12's shared-variance discrepancy is 1.1344201399231006, strictly positive despite zero cross-block Gram entries.
- In a three-state positive exponential family, the T14 restricted/full ESS transfer identity agreed to displayed floating-point precision (absolute difference 0 in that calculation).
- Exact enumeration of the two-state, one-stage, N=2 importance/multinomial-resampling experiment with π0=(0.9,0.1), weights (1,9), and identity mutation gave E[Zhat]=1.8 and E[Zhat H]=0.9, matching Z and the unnormalized numerator, but E[H]=0.172 while πh=0.5. This is an abstract Feynman–Kac illustration, **not** a test or counterexample of the complete v3.1 Gibbs/move implementation. It isolates why numerator unbiasedness does not imply normalized unbiasedness.
- 1,450 finite cases on a six-element universe checked preservation of lex order for equal-size sets after union with a common disjoint set, the tie-aware DP lemma in T07.
- For p=K=8, exhaustive neighbourhood counting gives maximum 24 flips/swaps, whereas p+K(p-K)=8. This checks why the report's local-search bound needs its K<=p/2 qualification.

### Published sources consulted; no project theory used

Only published-literature searches were used, with no search for the project, its authors, or its code. These citations establish known lines of theory; none is claimed to prove the entire method-specific theorem attached to it.

- [Del Moral, Doucet and Jasra (2006), *Sequential Monte Carlo samplers*, JRSS B 68, 411–436](https://www.stats.ox.ac.uk/~doucet/delmoral_doucet_jasra_sequentialmontecarlosamplersJRSSB.pdf): established SMC-sampler framework.
- [Cérou, Del Moral and Guyader (2011), *A nonasymptotic theorem for unnormalized Feynman–Kac particle models*, AIHP 47, 629–649](https://www.numdam.org/item/10.1214/10-AIHP358.pdf): nonasymptotic unnormalized-particle and coalescence/semigroup methods; hypotheses must be matched explicitly.
- [Mengersen and Tweedie (1996), *Rates of convergence of the Hastings and Metropolis algorithms*](https://www.stat.rice.edu/~dcox/Stat552/Mcmc/MengersonTweedieAnnStat1996.pdf): independence-sampler convergence. The finite minorization in T10 can also be proved directly.
- [Whiteley, Lee and Heine, *On the role of interaction in sequential Monte Carlo algorithms*](https://arxiv.org/abs/1309.2918), published Bernoulli 22 (2016), 494–529: interaction and generalized ESS theory. It is related background, not a theorem that restricted candidate ESS ensures this method's stability.
- [Barbieri and Berger (2004), *Optimal predictive model selection*](https://arxiv.org/abs/math/0406464), and [Barbieri, Berger, George and Rockova (2018 preprint), *The Median Probability Model and Correlated Variables*](https://arxiv.org/abs/1807.08336): scope and limitations of predictive MPM arguments.
- [Castillo, Schmidt-Hieber and van der Vaart (2015), *Bayesian linear regression with sparse priors*, Annals of Statistics 43, 1986–2018](https://arxiv.org/abs/1403.0735): related sparse-posterior contraction/selection theory; no verified direct transfer to this BB-ridge/empirical-scale target.
- [Wainwright (2009), *Information-theoretic limits on sparsity recovery in the high-dimensional and noisy setting*](https://arxiv.org/abs/math/0702301): support-recovery information limits; T37's fixed-design duplicate argument is proved separately.
- [Liu, Wong and Kong (1994), *Covariance structure of the Gibbs sampler with applications to the comparisons of estimators and augmentation schemes*](https://www2.stat.duke.edu/homeweb/scs/Courses/Stat376/Papers/ConvergeRates/GibbsSampling/LiuWongKongBiometrika1994.pdf), and [their 1995 scan/covariance paper](https://statweb.rutgers.edu/rongchen/papers/covarianceGibbs.pdf): relevant routes for a future estimator-variance comparison. No blanket variance reduction for the current four-round ratio output is inferred from them.

The strongest new methodological opportunity is the combination of **exact block-start algebra, unbiased within-round posterior marks, and fixed-N consistent parallel stacking**. The most underrated deterministic opportunity is to turn the score ledger into **valid evidence/posterior-mass and near-tie certificates**, while preserving exactly what each certificate does and does not cover.
