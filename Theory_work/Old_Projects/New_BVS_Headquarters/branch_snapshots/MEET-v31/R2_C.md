# Seat C — Round 2 rebuttal

I support retaining the v3 statistical construction, with weighted primary PIPs, additive LS0, and the proposed parallel execution layer. I accept the chair’s distinction between a settled method decision and an unproved property, subject to the qualifications below.

This review was read-only. I fetched the evidence branches, inspected the specification and core, and performed small calculations on existing CSVs. No fits, jobs, or subagents were launched. At my final fetch, ABL-START remained **DRAFT, results pending**.

References below use **M** for `Docs/Methodology/METHODOLOGY_v3.md` and **C/** for `Scripts/SMC_BVS/core/`. Statements marked **PROVED** below have an argument given here; campaign results retain their recorded qualifications.

## 1. Disputes D1–D8

### D1 — Start-ablation decision rule: HOLD, with the intervention audit substantially closed

Before reading results, I retained this rule: reconsider the start for a reproducible improvement in total computational cost at matched posterior accuracy, or a reproducible improvement in posterior accuracy at matched cost, without concentrated deterioration in weak S4/S5. A null result removes a computational-advantage claim; it does not, by itself, meet ground rule 5’s burden for replacement.

The arm construction now answers my principal Round 1 objection. In `theory/ABL-START:theory_campaign/ABL-START/scripts/abl_exports.cpp`, `Bst` changes the start partition, while `g->B = B` and `neighbour_graph(D, B)` retain the production round and graph. The independence proposal and bridge necessarily change with the start. Arm B should be called **singleton-factor start with the capped size prior**, not independent Bernoulli sampling.

Three qualifications remain before interpreting the eventual comparison:

1. **Charge the complete cost.** Arm D loads precomputed backfit tables before its fit timer starts: `theory/ABL-START:theory_campaign/ABL-START/scripts/abl_fit.R`, initialization of `BF`, followed by `t0`. Its table-generation cost must be added. All arms also retain complete-linkage setup through `make_blocks`, even when `Bst = 1`; the comparison therefore measures the implemented arms, not an optimized singleton implementation.
2. **The reference measures agreement, not certified error.** Leave-one-arm-out pooling uses a different reference for each arm; runs share the study seed; and retaining only available estimates can introduce completion selection. Unbiased potential-run evidence does not make a completed-only reference unbiased. These issues are visible in `scripts/summarise.R`, reference construction.
3. **Equal declared budgets are not equal realized compute.** Calibration, escalation, and stage counts vary. Report the cost–accuracy tradeoff, including setup, calibration, final work, and hardware allocation. A stage-count win alone is insufficient.

**What changes my mind:** the completed audited paired table, with these accounting qualifications resolved, showing a stable cost–accuracy advantage that survives reasonable reference choices and is not driven by deterioration in S4/S5. One seed on twelve designs may be inconclusive; inconclusive evidence retains the baseline without a speed claim.

I also amend the synthesis’s “HPM counts cannot discriminate the arms.” The existing study’s posterior-miss classification concerns its existing scored sets. Another start can change discovery, and another search can discover a competitor even on a current recovery. HPM counts remain useful observations, but they do not measure objective 1 and are not mathematically fixed under replacement.

### D2 — O-CERT card: COMPROMISE; adopt checked components, not the report wholesale

I support a **POST HOC** card containing:

- deduplicated \(Z_{\mathcal T}\), restricted PIPs, and explicitly restricted posterior summaries;
- the underestimation implication \(\widehat Z<Z_{\mathcal T}\Rightarrow\widehat Z<Z\);
- the simultaneous upper bound
  \[
  \pi(S)\le \min\!\left\{1,\frac{e^{F(S)}}{\max(Z_{\mathcal T},\,0.05\widehat Z)}\right\},
  \]
  with its output-event coverage interpretation;
- local certificates attached to the actual returned model;
- optional box certificates, identifying the region and reporting “unresolved” when their declared computation budget ends.

The exact-arithmetic monotonicity and box inequalities have a sound route in `theory/O-CERT:theory_campaign/O-CERT/REPORT.md`, Lemma M and C4: adding columns increases \(X_SX_S^\top\), decreases \(Q_S\), and increases the determinant ratio. This supplies legitimate region bounds.

Several statements must be corrected before adoption:

- A bound on posterior mass **outside the reported store** is not a lower bound on mass never scored. Some scored models were evicted.
- C1(a)’s best-of-scored ratio inequality must exclude \(\widehat S\) itself, as C3(c) does.
- C4’s conditional-mass expression requires isolating \(\{\widehat S\}\) as a leaf, or otherwise handling its containing leaf correctly.
- Higher-precision agreement does not establish the score-error contract SC.
- No branch-and-bound cost guarantee follows merely from the number of “ambiguous” variables.
- The illustrative “16 best additions” is not automatically a new method setting. If retained for optional cards, declare it as a region-computation budget.

A failed optional certificate calculation must not retrospectively invalidate an otherwise completed SMC fit.

**Closing check:** one corrected card specification checked against C1/C3/C4/C6, including region definitions, output-event coverage, and numerical labels. I do not require a new simulation panel for the elementary implications.

One additional correction to the Round 1 discussion: \(\delta_1<1/3\) is unnecessarily strong for the top-store MPM. If \(S_0\in\mathcal T\) and \(\pi(S_0)>1/2\), then
\[
\pi(S_0\mid\mathcal T)=\frac{\pi(S_0)}{\pi(\mathcal T)}>1/2.
\]
Every true inclusion consequently exceeds \(1/2\), and every false inclusion is below \(1/2\). **PROVED:** the same \(1/2\) concentration threshold suffices. This does not change my preference for HPM as the primary selection decision.

### D3a — Preserve the four-island local search under stacking: HOLD

Retain the baseline four-island search candidate if claiming that stacking is additive to the complete baseline computation or that its final HPM cannot worsen in posterior score.

A higher initial score need not lead bounded greedy search to a higher terminal score. Corollary W-R explicitly acknowledges this in `theory/METH-AUDIT:theory_campaign/METH-AUDIT/PROOFS.md`. Preserving only the pre-search maximum does not preserve the old post-search candidate.

**What changes my mind:** either a valid monotonicity proof for this particular bounded search, or an explicit decision to withdraw complete-run nesting and post-search monotonicity claims. No such proof is currently supplied.

### D3b — Flags under stacking: COMPROMISE

Use **all \(R'\) islands for the expanded run’s reported diagnostics**. Preserve a separately named four-island baseline diagnostic record only when claiming baseline reproducibility.

The baseline record must include its original HPM/search reference. E1 for islands 1–4 compared with an expanded HPM is not the baseline E1. Source: `C/v3_run.R:149`.

This is a settled specification choice; no statistical test is needed.

### D3c — LS0 neutrality: HOLD, and correct “stores nested”

The accurate claim is:

> Appending LS0 preserves the preceding sampler computation and its evidence/PIPs; it enlarges the all-scored set and cannot decrease the best score. The existing side audit found no HPM change in 2,394 completed fits.

**Bounded stores are not nested as sets.** New entries can evict old entries. Rather,
\[
\mathcal T_{\rm new}
=\operatorname{top}_c(\mathcal T_{\rm old}\cup\mathcal S_{\rm added}).
\]
This is **PROVED** by the top-\(c\) invariant in `C/cpp/v3_ledger.h:41` and METH-AUDIT Lemma S. Near ties, provenance, flags, and certification can change.

**Closing check:** integrated LS0 replay against the export, including stream endpoints, selected-model certification, and a deterministic eviction/tie example. A replay supports implementation fidelity; it does not make all output fields bitwise unchanged.

### D3d — Scope of scalability and C6: HOLD on claims; reject an artificial publication threshold

There is no methodological discontinuity at \(p=2500\). That is a particle-budget floor; \(N_0\) also grows when **\(n>2500\)**.

With island parallelism alone, the particle-round contribution to depth remains
\[
N_e(T+L+4)(p+B+2),
\]
plus calibration and setup. Particle parallelism removes that multiplicative \(N_e\) from the move-round contribution, but retains population reductions and other dependencies.

Therefore:

- An island-parallel paper may report \(p>2500\), with its actual cost and depth.
- A claim of particle-parallel depth requires an implemented and checked particle execution.
- A claim of practical superiority over sequential MCMC requires a stated comparator and matched posterior accuracy/resources.
- “The entire algorithm is free of \(N,H,R\)” must be removed.

Source: `theory/METH-AUDIT:theory_campaign/METH-AUDIT/PROOFS.md`, Proposition D, whose displayed formula already includes a population-reduction term.

**What changes my mind:** a complete work/depth account and the implementation evidence corresponding to the claimed execution level—not a single demonstration at an arbitrary dimension.

### D3e — Additional parallel stages: CONCEDE completeness

Include block-table evaluation explicitly. Include Gram/correlation construction, linkage, neighbour construction, convolution, grid reductions, and store pooling in the roadmap and cost account.

Do not silently change floating-point summation order while claiming bitwise equivalence. Exact parallel table scoring is straightforward; parallel convolution/reductions require a separately specified arithmetic order or a narrower numerical-equivalence claim.

### D3f — Thread safety: HOLD; issue confirmed

Use process workers, or separate mutable counters from shared immutable arrays and merge private counters afterward. `C/cpp/v3_score.h:20` and `:231` contain the mutable counters and writes.

**Closing check:** ownership inspection of the actual production worker implementation. A process-based harness does not validate an unsafe threaded implementation.

### D4 — Calibration bottleneck: CONCEDE the empirical uncertainty is resolved on the supplied example

Calibration can dominate: the committed S4 record gives 1,184.5 seconds of calibration versus 671.8 seconds for the serial final run. This supports prioritizing W-cal.

It does not establish universal dominance, nor identify a beneficial replacement calibration. Keep the rule; correct the cost discussion. Source: `theory_campaign/MEET-v31/evidence/2026-11-03_concurrency_runs.md`.

### D5 — Primary PIP: HOLD weighted primary; reject the truth-based gate

The primary estimator should follow the posterior estimand and intended island-scaling axis. Conditional island identities imply
\[
\frac{\sum_r\widehat Z_r\widehat{\mathrm{PIP}}_{rj}}
     {\sum_r\widehat Z_r}\longrightarrow\mathrm{PIP}_j,
\]
whereas equal pooling retains any fixed-\(N\) island bias. Source: METH-AUDIT `PROOFS.md`, Proposition P(i)–(ii).

This does not prove weighted pooling has smaller finite-\(R\) MSE. Nevertheless, MPM recovery against \(S_0\) is not a valid gate for deciding which estimator primarily estimates the posterior.

The newly filed rescore is narrower than commissioned: only three replay designs have the requisite local per-island records. Their MPMs agree under both poolings; the complete-study weighted comparison is unavailable here. Source: `evidence/2026-11-03_pip_rescore/REPORT.md`, Main finding, Part A, and Caveats.

**What changes my mind:** a demonstrated failure of the required measured-round island identity, or a change in the declared primary estimand/scaling objective. A finite-budget accuracy comparison can motivate reporting and cautions; it cannot establish posterior accuracy by proximity to binary truth.

### D6 — Inherent limitations: HOLD the distinctions, with proof checks

**(i) Memory.** An \(8p^2\) Gram matrix is an implementation choice. Exact submodel scores can be calculated from the relevant columns. Access to all predictors during a full coordinate round does not prove that every worker must privately hold all of \(X\), either: shared or distributed access is possible. Its communication cost must then be counted.

**(ii) An upper bound on \(Z\).** My Round 1 bound is **PROVED** directly from M §5. If \(\lambda_i\ge0\) are eigenvalues of \(G_S\),
\[
D_S=\prod_i\frac{1+(n+1)\lambda_i}{1+\lambda_i}\ge1.
\]
The nonzero eigenvalues of \(nX_SH_S^{-1}X_S^\top\) are
\[
\frac{n\lambda_i}{1+(n+1)\lambda_i}\le\frac n{n+1},
\]
so \(Q_S\ge y^\top y/(n+1)\). The normalized prior therefore gives
\[
Z\le U(X,y):=
C_n\left(2b_0+\frac{y^\top y}{n+1}\right)^{-\nu}.
\]
This is valid for rank-deficient designs and arbitrary \(p/n\). It may be extremely loose. “No useful tight upper bound follows from the sampled record alone” is defensible; “no run can upper-bound \(Z\)” is false.

**(iii) Lower bounds.** Since \(Z_{\mathcal T}\le Z\) pointwise,
\[
P\{\mathcal O,\ \max(Z_{\mathcal T},\alpha\widehat Z)>Z\}
=P\{\mathcal O,\ \alpha\widehat Z>Z\}\le\alpha.
\]
**PROVED** under the potential-run unbiasedness and stop-only coupling assumptions. This is not coverage conditional on completion.

Markov is sharp when only nonnegativity and the first moment are supplied: a two-point distribution attains the bound, or approaches it with strictly positive values. Additional information can improve it.

**(iv) Masked variance.** Large variance is an established failure mechanism in specified constructions. Its severity for the production grid is **OPEN**. It is not an impossibility theorem for every resolved bridge or mutation mechanism.

**What changes my mind:** an error in the displayed spectral or event-inclusion arguments, or a theorem establishing the claimed unavoidable variance for the actual production assumptions. Another seat’s broader wording is insufficient.

### D7 — Outputs required by the theory: HOLD, with the estimator fixed now

For a declared list of bounded functions \(h\), define
\[
H_r(h)=\frac1{4N_e}\sum_{q=1}^{4}\sum_{i=1}^{N_e}h(S_{rqi}),
\]
where \(S_{rqi}\) is particle \(i\) **after the complete measured round \(q\)**. Report
\[
\widehat\mu(h)=\frac{\sum_r\widehat Z_rH_r(h)}{\sum_r\widehat Z_r}.
\]

This is deterministic summary accumulation and **ADDITIVE**. Pair indicators \(1\{j,k\in S\}\) and normalized model size are examples. Do not multiply marginal RB-PIPs to estimate joint inclusion. Do not implicitly promise all exponentially many joint events.

The current accumulation point is identifiable in `C/cpp/v3_engine.h:351–359`; endpoint summaries would be accumulated immediately after `population_round`.

For bounded functions of continuous parameters, the corresponding model-space function is
\[
\bar h(S)=E[h(S,\beta_S,\sigma^2)\mid S,X,y].
\]
Analytic conditional integration or a separately specified approximation is required. The discrete accumulator alone does not implement every continuous functional.

The proof route is concrete. Conditional on calibration, the finite-state resample–move recursion gives
\[
E[\widehat Z_r\eta_{r,T}(f)]=Z\pi(f).
\]
Terminal rounds preserve \(\pi\), so this identity extends to each measured endpoint and their average. This is a **PROOF SKETCH** pending the implementation-level recursion check.

Given that identity, iid islands, \(0\le H_r\le1\), and \(M=E[(\widehat Z_r/Z)^2]\), my scalar bound is **PROVED**:
\[
P(|\widehat\mu-\mu|>\epsilon)
\le \min\!\left\{1,\frac{4(M-1)}R+\frac{4M}{R\epsilon^2}\right\}.
\]
Apply Chebyshev to \(\bar W<1/2\) and to
\(\overline{W(H-\mu)}\). A simultaneous bound over \(q_n\) summaries needs a multiplicity argument; the scalar result is not dimension-free uniform accuracy.

I also hold the corrections to “downward only,” ideal-grid versus production-grid laws, and LH scope. A nonconstant nonnegative unbiased estimator cannot be below its mean almost surely: **COUNTEREXAMPLE** to the literal downward-only assertion.

Discovery-to-retention can sometimes be repaired rather than merely flagged: if \(S_0\) is scored and \(\pi(S_0)>1/2\), it is the unique global maximizer and must remain in any nonempty top store. Thus an asymptotic result may separate the event \(\{\pi(S_0)\le1/2\}\). Unqualified finite-sample retention remains false.

**Closing check:** the explicit endpoint estimator and its finite-state identity. Weight-stability, useful moment bounds, and broader statistical scope then belong to the theorem meeting.

### D8 — Six resource stops: CONCEDE optional operational value

A six-fit replay can measure whether the new execution rescues those specific jobs. It cannot establish \(P(U)\to0\), guarantee rescue, or erase the original study’s six stops.

Record any reruns as a separately identified execution result. Their scheduling is an HQ resource decision, not an unresolved method choice. I launched none.

## 2. What chair facts 0.1–0.5 change

| Fact | Effect on my position |
|---|---|
| **0.1: third concurrency PASS** | Upgrade the executed evidence to smoke plus three study designs. The committed log resolves that provenance objection. It supports the listed final-run comparisons, not W-cal, integrated LS0, arbitrary worker configurations, or a four-core speedup. |
| **0.2: calibration can dominate** | Resolve my previous empirical uncertainty on S4. Prioritize concurrent diagnostic islands and report measured phase costs. Keep the calibration rule. |
| **0.3: ablation arm construction** | Close the main graph/move-count confounding objection after source inspection. Retain the cost/reference qualifications in D1. ABL-START remained unfinished at my final fetch. |
| **0.4: mutable counters** | Confirm the required ownership fix. Process workers avoid the particular shared-counter race; future threads need private counters or synchronization. |
| **0.5: PIP rescore** | The filed result is partial because the original per-island production bundles are not local. Three replay designs cannot close the full-study comparison. This does not change the primary-estimator decision. |

The \(R=32,N=312\) experiments in the concurrency log are **population-splitting experiments**, not the proposed stacking operation at unchanged \(N_e\). They must not be presented as its validation.

## 3. Procedural rule and disposition of my Round 1 open list

**Accept, with two amendments.**

First, a theorem obligation must have a named statement, assumptions, status, and consequence if it fails. Moving a property to the theorem meeting closes a method question only when the method decision really does survive its plausible outcomes. It cannot silently waive ground rule 7.

Second, the examples of inherent limitations need precise scope:

- Masking results apply to their specified product construction/design assumptions, not every conceivable product start.
- Blind-run diagnostics lack a universal detection guarantee from their observed record alone; a particular positive certificate can still detect some failures.
- The 565 posterior misses are facts about those data and the fixed target, not a universal statistical error rate.
- Finite-machine inability to handle unrestricted dimensions is inherent; a particular quadratic representation is not.

Disposition of **R1_C §5**:

| Original item | Disposition |
|---|---|
| **1. ABL intervention and outcome** | **(i) Method question still open:** replacement remains contingent on the final audited comparison. Arm construction is substantially settled. Closer: the completed cost/reference audit and paired result under D1’s rule. |
| **2. Estimators and outputs** | Decisions are fixed by this position: weighted primary, named equal secondary, \(R'=4\) default, optional predeclared stacking, endpoint \(h\)-summaries, strict unavailable-output fields. **(iv) Specification/engineering:** one consistent implementation checklist. |
| **3. Parallel fidelity** | **(iv) Engineering:** persistent worker streams, state ownership, deterministic merges, baseline search preservation, W-cal, and integrated LS0. Closer: the existing three-design replay harness plus deterministic boundary cases. |
| **4. Required posterior-accuracy theorem** | The required interface is fixed-data consistency plus an explicit finite-error bound, with separate growing-dimension conditions. **(ii) Theorem obligation:** the endpoint identity and useful control of its constants. An unspecified island budget is not an efficiency theorem. |
| **5. Proposal §5.3** | **(ii) Theorem obligation:** jointly satisfiable weak-dependence/overlap assumptions for the actual block-product construction, including common noise integration. Failure of one sufficient condition is not inherent impossibility. |
| **6. Calibration claims** | Method decision settled: keep calibration and its valid-grid contract. **(ii) Theorem obligations:** production candidate coverage, stage counts, delivery, and any claimed rebuild convergence. **(iii) Inherent:** restriction to \(V\) does not, by definition, inspect its complement; without additional assumptions it cannot bound arbitrary omitted mass. |
| **7. Correct event/numerical object** | **(iv) Engineering/specification:** unavailable-field fixes and removal of unsupported certificate language. **(ii) Theorem obligation:** rigorous numerical-error transfer if exact numerical certification is claimed. |
| **8. “Scale \(p\)” evidence** | **(iv) Specification/engineering** for the actual implementation and cost account; **(ii) theorem/performance obligation** for accuracy at growing budgets. **(iii) Inherent to this kernel:** sequential dependence across its \(p+B+2\) steps. Comparative wall-clock superiority remains an empirical claim requiring its stated comparison. |

None of the original eight questions becomes an inherent limitation merely because it is difficult.

## 4. Item 9 — Generality in \((n,p)\)

### 4.1 Interpretation and audit table

Three claims must be separated:

1. **Definition:** the target and mathematical algorithm are specified for admissible inputs.
2. **Delivery:** a finite implementation completes within a declared allocation.
3. **Accuracy:** its finite-budget output approximates the target, or recovers a generating support, under stated conditions.

Generality of definition does not imply universal delivery or accuracy.

Classes below follow Amendment 01. Some settings combine a dimension-dependent formula **(b)** with a resource constant **(c)**. Reclassifying a constant as a budget does not make its value optimal or statistically necessary. Changing a calibration/population budget can change the sampling law even though it leaves the target unchanged.

| Setting | Value/formula and source | Class | Reason | Behaviour across regimes | Action |
|---|---|---|---|---|---|
| Input dimensions | Current \(n\ge3,p_{\rm raw}\ge1\); `C/v3_preprocess.R:103–107` | **(e)** for blanket rejection of \(n=2\) | Standardization and the proper ridge target are defined for nonconstant data at \(n=2\). | Tiny \(n\) is excluded unnecessarily. At \(n=1\), centered sample scaling is undefined. | Extend \(n=2\); explicitly handle empty/degenerate inputs. E1 below. |
| Constant columns/response; scaling | Exact equality; center and sample-SD scale with denominator \(n-1\); M §4 | **(a), (b)** | Defines the working model and removes undefined scales. | All regimes; dropping columns changes retained \(p\). Tiny samples can be uninformative without making the posterior improper. | Keep; distinguish valid degenerate-status returns from posterior estimates. |
| Near-constant numerical scaling | Anchored two-pass route when centered scaled magnitude \(\le\sqrt{\epsilon_{\rm mach}}\); `C/v3_preprocess.R:47` | **(d)** | Cancellation protection, not variable screening. | Important for badly scaled inputs at any dimension. No asymptotic accuracy guarantee follows. | Keep and document. |
| Slab | \(g=n,\tau=1\); M §5; `C/cpp/v3_score.h:175` | **(a), (b)** | Unit-information convention and proper ridge regularization. | Defined for \(p\ll n,p\approx n,p\gg n\), including singular subdesigns. Penalty changes with \(n\). | Keep. |
| Noise prior | \(a_0=b_0=0.01\); M §5; `C/cpp/v3_score.h:14` | **(a)** | Proper prior on the standardized working scale. | Fixed in every regime; not automatically negligible at tiny \(n\). | Keep as a modelling convention; avoid universal “vague” or negligible-effect claims. |
| Model prior | BB\((1,p)\), \(w(k)=\tfrac12/\binom{2p-1}{k}\), normalized after capping; M §5 | **(a), (b)** | Sparse multiplicity-aware prior. | Uncapped mean size \(p/(p+1)\); dense growing truths are not its default regime. Defined for every finite retained \(p\). | Keep; print the exact normalization. |
| Size cap | \(K=\min(p,\lfloor n/2\rfloor)\); M §3/§5 | **(a), (b)** | Deliberate exclusion of large models, not required for propriety. | Eventually inactive if \(p\ll n\); active near/above \(n\); tiny \(n\) allows very few variables. | Keep; support recovery is impossible when \(s_0>K\), by definition. |
| Block width | \(B=\min(\lfloor\sqrt n\rfloor,\lfloor\sqrt p\rfloor,16)\); `C/v3_preprocess.R:22`; `C/cpp/v3_core.cpp:142` | **(b), (c)** | Bound exhaustive local-table cost. | When both dimensions grow, \(B\) reaches 16; \(p\gg n\) also has the \(\sqrt n\) bound. Tiny \(n\) yields small blocks. | Keep, explicitly as a local-enumeration budget. Do not promise recovery of arbitrary-size correlation groups. |
| Clustering, cut, packing | Complete linkage on \(1-|r|\); split nodes with size \(>B\); next-fit whole clusters; M §6.3; `C/cpp/v3_blocks.h:121` | **(b), (c)** | Deterministic \(X\)-dependent partition under a table budget. | No correlation-height cutoff exists. Packing can merge separated population groups; setup remains quadratic in storage. | Keep; correct any description suggesting a correlation-height cut. |
| Local tables/start | Every block subset, exponent 1, full \(y\), normalized capped size convolution; M §6.3 | **(a), (b)** | Specified composite approximation, corrected at the endpoint. | Constant \(B\) bounds each table; number of blocks grows with \(p\). Common integrated noise prevents general factorization even for orthogonal blocks. | Keep pending D1; no start-only posterior claim. |
| Neighbour threshold | \(r_n=\sqrt{2\log p/n}\), strict exceedance, forced best partner, at most \(B\) outgoing choices, symmetric union; M §6.4; `C/cpp/v3_blocks.h:146` | **(b), (c)** | Correlation proposal heuristic with bounded outgoing construction. | Tends to zero when \(\log p=o(n)\); can approach/exceed 1 otherwise, leaving forced partners. Symmetric degrees can exceed \(B\). | Keep; correct the threshold and remove any familywise screening interpretation. |
| `cut_group` | Uncapped graph \(|r|\ge r_n\), no forced partner; `C/cpp/v3_core.cpp:760` | **(b)** | Descriptive partition diagnostic. | May produce large connected components or none; differs from the move graph in every regime. | Keep as descriptive; not a partition-recovery certificate. |
| Final population | \(N_0=\max(2500,n,p)\); M §3 | **(b), (c)** | Baseline effort floor plus growth with dimension/sample size. | Dominated by \(n\) for large \(p\ll n\), by the larger dimension otherwise; constant floor at small sizes. | Keep. The inherited floor is a resource choice, not an accuracy theorem. |
| Calibration population | \(H_0=\lceil512N_0/2500\rceil\); `C/v3_preprocess.R:26` | **(b), (c)** | Declared calibration-to-final effort ratio. | \(H_0\sim0.2048N_0\), so it grows in every unbounded joint regime. | Keep; 512/2500 is not statistically derived. |
| Stage ceiling | \(T_0=\max(1000,\ell^2)\); M §3 | **(b), (c)** | Finite work ceiling. | Eventually \(O(\log^2(n+p))\); the 1000 floor dominates over a very large practical range. | Keep; hitting the ceiling yields an explicit failure, not an accuracy conclusion. |
| Rebuild/search budget | \(\ell=\lceil\log_2(n+p+1)\rceil\); ≤\(\ell\) rebuilds and ≤\(\ell+1\) scans; M §§3, 6.7, 6.10 | **(b), (c)** | Slowly growing bounded effort. | Grows with either dimension; does not guarantee enough search moves for growing support size or grid convergence. | Keep; expose the corresponding theorem premises. |
| Burn-in | \(L=\max(4,\lceil\log_2(n+1)\rceil)\); M §3 | **(b), (c)** | Terminal mutation budget. | Grows with \(n\), not with \(p\) at fixed \(n\). No general mixing-time domination. | Keep; classify mixing/delivery as OPEN. |
| Island counts | Four diagnostic and four final islands; optional \(R'=4k\) final islands; M §§3, 6.8; dossier §2 | **(c)** | Replication and parallel width. | Fixed four does not guarantee growing-dimension accuracy. Extra final islands retain \(N_e\). | Keep default; declare \(R'\) before final randomness. |
| Measured rounds | Four; `C/v3_run.R:87`, `C/v3_calib.R:12` | **(c)** | Fixed averaging effort after burn-in. | Constant in all regimes; averaging correlated rounds is not four independent replications. | Keep; define general-\(h\) accumulation explicitly. |
| Tiers | \(e\in\{0,1\}\), \((N_e,H_e,T_e)=4^e(N_0,H_0,T_0)\); M §3 | **(c)** | Bounded escalation policy. | At most approximately 16-fold bridge work per trajectory population when both population and ceiling multiply. No unbounded rescue mechanism. | Keep; calibration triggers and failure statuses remain explicit. |
| ESS threshold | 0.90 in pilot/grid; M §§6.6–6.7; `C/cpp/v3_calib.h:31,79` | **(c)** | Declared one-step dispersion/effort budget; restricted population CV² threshold \(1/9\). | Dimensionless across regimes, but a fixed local threshold need not control accumulated error or omitted mass. | Keep; it is not a numerical rounding tolerance or full-space accuracy guarantee. |
| Bisection and endpoint arithmetic | 60 halvings; endpoint snap \(10^{-12}\); strict progress and post-snap validation; `C/cpp/v3_calib.h:34–43,82–94` | **(d)** | Finite-precision implementation of the schedule rule. | At very sharp crossings, double precision can fail to resolve progress. Snap may fail validation, which is reported. | Keep as numerical conventions; preserve failure reporting. No universal numerical-resolution claim. |
| Pilot floor | \(1/T_e\), pilot only; M §6.6 | **(b), (c)** | Ensures exploratory progress within bounded effort. | Decreases as the ceiling grows; can violate the desired empirical ESS, explicitly flagged. | Keep; do not transfer forced-step logic to final islands. |
| Move round/resampling | \(p\) Gibbs, one uniform swap, \(B\) neighbour swaps, one independence move; fresh random order; multinomial each stage; M §§6.5–6.6 | **(b), (c)** | Fixed invariant-kernel construction and mutation allocation. | At least linear sequential coordinate dependence per particle for all large-\(p\) regimes; cap handled explicitly. | Keep; changing counts/order/kernel is WORKHORSE unless separately proved equivalent. |
| Candidate leaders and grid set | Top \(20p\) under each endpoint ordering, plus empty; \(|V|\le40p+1\); M §6.7; `C/cpp/v3_ledger.h:76` | **(b), (c)** | Linear-size discovery summary. | Fraction of model space retained can vanish rapidly in all growing-\(p\) regimes. Does not guarantee omitted-mass control. | Keep; discovery, retention, and posterior coverage are distinct. |
| Reported top store | \(40p+1\); M §6.10; `C/cpp/v3_ledger.h:76` | **(b), (c)** | Bounded reporting/certificate budget. | May truncate many near-equivalent models. Running HPM survives eviction. | Keep; restricted PIPs must be labelled restricted. |
| Score cache | \(500p\), clear when full; `C/v3_run.R:89`; `C/cpp/v3_score.h:249` | **(b), (c)** | Reuse deterministic scores. | Entry count is linear, but keys cost up to \(O(K)\), yielding up to \(O(pK)\) key storage. | Keep; eviction affects cost, not potential-run scores or target. |
| Near ties/duplicate report | \(10^{-9}\) nat near-tie window; duplicate correlation \(1-10^{-10}\); M §§4, 6.10 | **(d)** | Descriptive numerical neighbourhoods; neither changes the HPM order or drops near-duplicates. | Absolute log-score window need not track growing floating-point error. Duplicate ambiguity persists at any dimension. | Keep as reporting tolerances; do not use as rigorous error bounds. |
| Operational flags | E1/E2: 1 nat; E3: strict improvement; final ESS flag \(0.5N\); M §6.9; `C/v3_run.R:149–154` | **(c), (b)** | Declared escalation/diagnostic criteria; one nat corresponds to an odds factor \(e\). | Power is not guaranteed as dimensions grow; disagreement can be absent under common failure. | Keep thresholds; label heuristics. They are not numerical tolerances. |
| Exact branch | \(E=\sum_{k\le K}\binom pk\le(5H_0+4N_0)p\); M §6.2; `C/cpp/v3_core.cpp:69` | **(b), (c)** | Deterministic enumeration-versus-sampling work proxy. | Fixed \(p\): eventually exact as \(n\) grows. Growing \(p\ll n\) need not be exact. Tiny \(n\): small cap can make enumeration easy even at large \(p\). | Keep; this is a dispatch budget, not an accurate universal runtime equivalence. |
| Evidence confidence/MPM threshold | \(\alpha=0.05\); MPM uses \(>1/2\); M §§6.11–6.12 | **(a)** | Declared confidence level and Hamming-loss decision convention. | Dimension-independent definitions; simultaneous PIP accuracy requires additional analysis. MPM can exceed \(K\). | Keep; report exact-branch evidence directly as well as any common-format bound. |
| Score numerics | Cholesky/refactor/augmented QR; \(Q<10^{-8}y^\top y\) triggers nonnegative formula; M §6.13; `C/cpp/v3_score.h:219` | **(d)** | Stable evaluation of one mathematical score. | Conditioning/error can worsen with \(n,K\); positive ridge ensures mathematical propriety, not arbitrary-precision accuracy in double. | Keep; numerical failure remains explicit. |
| Numerical certification factor | Heuristic \(64\epsilon_{\rm mach}\) error expression, used by `global_certified`; `C/cpp/v3_score.h:240`; `C/cpp/v3_core.cpp:531` | **(e)** as a rigorous certificate; **(d)** as an indicator | The source explicitly says the bound is heuristic. | No uniform validity across dimensions or conditioning has been established. | Separate heuristic numerical margin from rigorous certification. E3 below. |
| LS0 mode ties | `start_mode(..., cap=1000000)`; `C/cpp/v3_start.h:183–238` | **(e)** for an unconditional lexicographic-mode claim | Truncation can prevent examining every maximizing tie. | Tied modes can proliferate with duplicates/symmetry at any \(p/n\). | Resolve the selected tie exactly without relying on exhaustive tie enumeration. E2 below. |
| Allocation and guard | Default 8 GiB/24 h; stop-only clock; `C/v3_fit.R:49`; `C/cpp/v3_runtime.h:15–25` | **(c)**; **(e)** if hidden by “seed alone” | Operational delivery depends on allocation and environment. | Fixed resources cannot support unrestricted joint growth. Identical inputs/seed can have different completion statuses. | Make the operational contract explicit. E6 below. |
| Memory preflight | Includes \(\lceil p/B\rceil(K+1)(B+1)\) convolution proxy; `C/v3_fit.R:27–32` | **(c)** estimate; **(e)** if treated as a safe bound | Packing leaves gaps, so \(\lceil p/B\rceil\) is not an upper bound on \(J\). Parallel ownership changes peak memory. | Defect exists already at study size; replication becomes more consequential with many workers. | Correct dimension accounting and label estimates honestly. E4 below. |
| Archive/export limits | \(V\) snapshots: all if \(p\le25\), otherwise at most \(10^4\); R Gram copy only by default for \(p\le2000\); `C/v3_calib.R:15–20`; `C/v3_setup.R:9` | **(c)** | Storage/export choices. Full \(V\) still constructs the grid; C++ still holds the Gram. | Archive truncation begins as \(V\) grows. The 2000 threshold does not remove quadratic scorer storage. | Keep, expose truncation, never reconstruct a “full” \(V\) from a truncated snapshot. |
| RNG/representation | One seed, fixed stream map, 53-bit uniforms, integer dimensions; `C/v3_run.R:7–40`; `C/cpp/v3_util.h:43–60,111` | **(d), (c)**; **(e)** if unbounded implementation support is asserted | Reproducibility conventions and finite machine representation. Distinct pseudorandom seeds are not a proof of independent random streams. | Mathematical independent-uniform theory and finite implementation must remain distinct; very large dimensions/budgets can exceed integer ranges. | Add checked range/allocation arithmetic; scope bitwise claims to the numerical environment. E5 below. |
| Other operational constants | Exact-branch timing: 200 scores and at least 64 columns; duplicate-check chunk 512; compiler-lock waits; `C/v3_fit.R:9–13`; `C/v3_preprocess.R:73`; `C/v3.R:21,54–56` | **(c)** | Profiling, workspace, and build-management budgets. | Affect execution/availability, not the target. Timing extrapolation is hardware-dependent. | Keep as operational defaults, outside statistical theory. |

### 4.2 Resolution of every category-(e) issue

No production edit is proposed in this read-only review. The following are concrete required fixes or justified reclassifications.

| Issue | Resolution and change class | Effect on the 2,400 study fits | Proof/check route |
|---|---|---|---|
| **E1: tiny-input domain** | **ADDITIVE** extension: accept nonconstant \(n=2\) data under the same target/scaling; route \(n=1\) and zero-predictor inputs explicitly to degenerate/unavailable statuses; reject \(n=0\). | No change at \(n=200\). | For \(n=2\), \(K=1\), \(B=1\), \(E=p+1\), so the existing dispatch selects exact enumeration. Check centering, normalization, and boundary returns on tiny deterministic inputs. This is a **PROOF SKETCH** for the extension, not a claim that current code supports it. |
| **E2: LS0 tie cap** | **ADDITIVE** to v3.1 LS0: retain the existing fast path when enumeration is untruncated; on truncation use deterministic tie-aware max-plus reconstruction that selects the prescribed smallest-size/lexicographic maximizer without enumerating all tied models. Resource failure remains an explicit incomplete LS0 status. | I directly inspected `/home/fb31/ls0_work/agg_final/ls0_per_fit.csv`: all 2,400 rows have `start_ties=1`, `start_truncated=FALSE`. The proposed truncation-only fallback changes none of those recorded centers. Original production had no LS0. | Prove the score/order dynamic-programming invariant and test a symmetric case with more than one million tied optima. Preserve arithmetic conventions on the existing fast path. Numerical/exact-score correspondence remains separate. |
| **E3: heuristic certification** | **POST HOC / ADDITIVE interface correction:** retain the numeric margin as a heuristic field; reserve rigorous certification for validated score intervals and validated sums/comparisons. | No target, score, HPM, PIP, or budget changes. The study uses the SMC branch; it cannot gain a global certificate from this exact-branch heuristic. | Source inspection already establishes the mismatch. A rigorous replacement requires an error-bound proof; extended-precision replay alone is insufficient. |
| **E4: preflight dimensions and worker accounting** | **ADDITIVE engineering:** use a valid pre-setup bound such as \(J\le p\), then actual block sizes after setup; account separately for shared arrays and each concurrent worker’s private populations/cache/archive. Keep “estimated memory,” not “certified peak,” until all allocations are bounded. | The formula changes, but statistical settings do not. Recorded \(J\) ranges are 46–60 at \(p=500\), versus \(\lceil p/14\rceil=36\), and 95–120 at \(p=1000\), versus 72. Replacing just that convolution proxy by \(J_{\max}=p\) leaves both tiers below the default 8 GiB at both study dimensions. Full concurrent peak/stop behaviour still needs its allocation audit. | Direct dimension accounting against `C/cpp/v3_start.h:121–148` and the worker ownership map. My small calculation is not a proof that the entire old estimate underestimates or bounds actual peak memory. |
| **E5: finite representation limits** | **ADDITIVE engineering:** validate integer conversions, products, stream identifiers, and allocation sizes before use; return an explicit unsupported-resource status instead of overflow. Correct the stale “up to 20” block-width comment: the actual bound is 16. | Study dimensions and budgets are safely inside the relevant ranges; no values change. | Checked-arithmetic boundary tests and source audit. Extending the implementation beyond those ranges requires a separate representation change, not a new prior. |
| **E6: “seed alone” versus resources** | **ADDITIVE specification correction; reclassify allocation as (c):** inputs and seed determine default statistical settings and a potential uninterrupted computation. A recorded allocation/execution environment determines whether that computation is delivered. | No values or historical outcomes change by relabelling. New concurrent executions can change completion; do not claim otherwise. | Stop-only coupling and explicit unavailable fields; never condition unbiasedness on observed completion. |
| **Suspected arbitrariness of 16, 2500, 512/2500, 1000, 4, 20p/40p, 500p, 0.90** | Retain and explicitly justify as **(c)** resource/dispersion budgets. This is **ADDITIVE specification**, not a new statistical law. Their exact values are conventions, not derived optima. | No value actually used changes. | Existing normalization/invariance arguments work for positive admissible budgets; performance results must state their additional budget conditions. Altering these settings later is not automatically law-preserving. |

This resolves arbitrariness by making the role of each constant explicit, not by inventing a formula that happens to reproduce the study values.

### 4.3 \(B^*=16\) and W7-PART

Retain the cap. Exhaustive tables cost exponentially in block width; a fixed enumeration budget is legitimate under ground rule 9.

The theorem condition concerns a population group size \(g_{\rm grp}\), **not** the slab’s \(g=n\):
\[
g_{\max}\le B<2g_{\min}.
\]

For equal group sizes:

- At study size \(B=14\), the condition is \(8\le g_{\rm grp}\le14\).
- Once \(B=16\), it is \(9\le g_{\rm grp}\le16\).
- Groups larger than \(B\) cannot be returned intact as individual blocks.
- The study’s groups of five fall outside the equality-of-blocks-and-groups theorem because \(2g_{\rm grp}\le B\).

Source: `theory/W7-PART:theory_campaign/W7-PART/REPORT.md`, §2, SIZE and Theorem A3; use the reviewed qualifications in `theory/T38-RECORD:theory_campaign/T38-RECORD/REGISTRY_v2.md`, PART rows. Under appropriate separation, unions of whole groups may still be recovered; which groups are combined remains consequential.

Removing the ceiling would not automatically solve the theorem problem. If fixed groups eventually satisfy \(2g_{\rm grp}\le B_n\), packing can combine them. A growing \(B_n\) also increases enumeration cost. A group-recovery-oriented cut or new width rule would change \(\pi_0\), the graph/move budget if coupled to \(B\), and the bridge: **WORKHORSE** unless explicitly separated and analyzed.

The cap reaches 16 when both square-root floors reach 16; it strictly restricts the uncapped rule when both dimensions reach 289. These are implementation arithmetic facts, not statistical transitions.

### 4.4 Thresholds, exact dispatch, and resources

**Neighbour graph.** HQ’s \(\sqrt{\log n/n}\) description is only a comparable scale under polynomial relationships between \(p\) and \(n\). The actual rule uses \(\log p\). It is not a familywise null-correlation bound over all pairs. Its forced partner and symmetric union also prevent interpreting it as a thresholded support estimator. Correctness rests on the Hastings ratio and the other valid moves, not on graph recovery.

**Clustering.** There is no fixed correlation-height cut to tune. The hierarchy is cut by node size. This distinction matters because a theorem about thresholded population groups is not automatically a theorem about complete linkage plus packing.

**Exact dispatch.** The coefficient \(5H_0+4N_0\) represents one pilot plus four diagnostic populations and four final populations in a rough work proxy. It does not account for the actual number of rebuilds/stages. Keep it as a deterministic resource rule. For fixed \(p\), its threshold grows without bound with \(n\), so eventual exact dispatch is **PROVED**. This does not extend to every growing sequence with \(p\ll n\).

**Resources.** The statement suitable for the paper is:

> The procedure requires no statistical tuning beyond its published defaults and one seed. It records the computational allocation and execution configuration. Resource or numerical interruption returns an explicitly incomplete result; mathematical guarantees distinguish the potential uninterrupted computation from the event that output is delivered.

The literal stronger statement that the complete operational output is a function of \(X,y,\text{seed}\) alone is false for the current clock-based guard.

### 4.5 Regimes and theorem scope

| Regime | Method applicability | Current theoretical scope and its cause |
|---|---|---|
| **Tiny \(n\)** | Current code admits \(n\ge3\); E1 extends meaningful exact computation to \(n=2\). At \(n=1\), centering leaves no variation to standardize. The cap is extremely restrictive. | Fixed-data posterior/enumeration identities remain meaningful where the working model is defined. Large-\(n\) recovery theorems say nothing about tiny samples. Lack of identifiability is not a sampler defect. |
| **Fixed \(p\), \(n\to\infty\)** | Eventually exact under the existing dispatch. | Then output claims reduce to target-posterior theory and numerical/delivery conditions. A fixed-\(p\) Gibbs theorem can be a component result without describing the eventual production branch. |
| **Growing \(p\ll n\)** | Same target/rules; eventually \(K=p\), but enumeration can still be infeasible. | Polynomial-dimensional target results can apply under their other assumptions. Slow logarithmic burn-in is not automatically enough for every growing-\(p\) kernel. |
| **\(p\approx n\)** | Ridge target remains proper; \(K\) is approximately \(n/2\). | Centered designs have rank at most \(n-1\), so assumptions requiring a positive-definite full Gram cannot simply extend to \(p\ge n\). Sparse-eigenvalue conditions may still be possible. This is a geometric restriction on those proof families, not failure of the target definition. |
| **Polynomial \(p\gg n\)** | Same method, bounded local tables, growing populations, and substantial setup/memory costs. | Polynomial target results may apply under sparse identifiability. The exact-Gram LH theorem does not cover this regime. The LH-iid route retains the recorded joint-route gaps; groups-of-five packing is an additional issue. Source: `theory/T38-RECORD:theory_campaign/T38-RECORD/T38_STATEMENT.md`, “(b1-LH-iid).” |
| **\(p\le e^{Cn^\alpha}\), \(0<\alpha<1\)** | Mathematically defined for each finite pair. Here \(r_n=O(n^{(\alpha-1)/2})\to0\), while \(N_0\ge p\) and quadratic setup can be enormous. | The present polynomial-\(p\) results do not justify this broader statistical claim. Song–Liang’s Corollary 1 uses its own prior, support-size, tail, and covariance conditions: `theory_campaign/inputs/SongLiang2015.pdf`, §2.1.2, Corollary 1. Their result cannot simply be imported. No supplied counterexample proves our prior incapable of this scope. |
| **More general joint growth** | Budgets remain explicit, but finite hardware/precision eventually limits implementation. If \(\log p/n\) is not small, the neighbour threshold behaves differently; forced partners keep the graph defined. | General consistency or useful precision is **OPEN** and requires signal, complexity, overlap/mixing, numerical, and delivery assumptions. No method can promise exact support recovery for arbitrary unidentified or vanishing-signal sequences. |

There are genuine method-induced restrictions:

- the support cap excludes larger truths;
- the fixed block ceiling excludes growing groups from the particular whole-group recovery route;
- bounded stores can omit substantial posterior mass;
- logarithmic terminal/search budgets may be insufficient for a proposed proof route;
- \(N_0\ge p\), full-coordinate mutation, and current quadratic setup impose real computational growth.

There are also **unproved extensions**, including subexponential-dimensional posterior theory, production-grid moment bounds, and the study-generator theorem. They must not all be blamed on the prior or classified as impossible.

**Separate \(p\ll n\) and \(p\gg n\) statistical rules are not currently needed.** The cap and exact dispatch already handle a major structural distinction, and ridge scoring remains defined in both regimes. Separate execution strategies—Gram versus on-demand scoring, shared versus distributed storage—may be useful while preserving the mathematical target. Any altered partition, prior, or kernel requires its own classification and proof.

## 5. Final decision list

I consider the following decisions settled:

- Retain the target prior, cap, block/composite construction, bridge, move round, calibration law, and declared resource defaults.
- Retain HPM as the primary selection decision; add LS0 after the baseline computation.
- Use weighted primary PIPs and named equal-weight secondary PIPs; report their MPMs descriptively.
- Default to four final islands; allow predeclared stacking at unchanged per-island population.
- Preserve the baseline search candidate if claiming complete-run nesting.
- Adopt safe concurrent execution, with claims limited to what the implementation and replay establish.
- Keep existing diagnostic triggers; add checked, correctly labelled post-hoc certificate components.
- Define measured-endpoint estimators for bounded model summaries now.
- Accept the chair’s procedural distinction, with explicit theorem obligations and narrowly stated inherent limitations.
- Keep the audited constants as declared modelling, dimension, resource, or numerical conventions; make E1–E6 concrete implementation/specification actions.

The remaining items have distinct closers:

| Remaining item | Single closing test or check |
|---|---|
| **Start replacement / computational advantage — method OPEN** | Final ABL-START paired report with complete cost accounting and an audited reference interpretation under D1’s declared rule. Until then retain the start without an established speed advantage. |
| **Worker, W-cal, stacking, and LS0 fidelity — engineering** | One integrated replay/checklist on the existing three designs plus deterministic tie, eviction, and stop cases. |
| **General-functional estimator identity — theorem obligation** | Finite-state resample–move proof at the specified measured-round endpoint. |
| **Certificate release semantics — specification/proof check** | Corrected card checked for region scope, output-event coverage, and validated-versus-heuristic arithmetic. |
| **Generality repairs E1–E6 — engineering/specification** | Boundary-case and allocation audit against the unchanged study settings, including LS0 tie reconstruction. |
| **Complete-study weighted PIP summaries — post-hoc reporting** | Run the already supplied rescore over the original per-island production bundles; no refitting is needed. |
| **Growing-dimension accuracy, delivery, weak-dependence stability, and study-generator scope — theorem obligations OPEN** | Theorem meeting freezes explicit assumptions and budgets, then supplies a proof or counterexample for each claim. These are not closed by another small empirical panel. |
| **Comparative large-\(p\) performance — empirical claim OPEN** | A specified matched-accuracy/resource comparison at the implemented execution level, if that claim is retained. |

I approve moving to the theorem meeting with these method decisions and named obligations. I do **not** approve recording the unfinished ablation, missing implementation checks, or broader accuracy properties as proved or as inherent impossibilities.
