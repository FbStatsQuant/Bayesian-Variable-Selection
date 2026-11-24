# EXP-CP1 independent review — Sol

**Recommendation: GO-WITH-CHANGES for engineering and the overlap study; no production-rung approval from this review.** A joint 1M-predictor fit is plausible on NOTS. The requested v1 specification does not yet justify its memory requests, precision, or total budgets. Two concrete memory omissions can break the proposed implementation before the statistical questions are reached.

## Scope and evidence

Reviewed BRIEF, EXPERIMENT_PLAN v0.2, ENGINEERING_SPEC **v1**, OWNER_DECISIONS v0.2, NOTS_FACTS, REQUESTS including R6, REVIEW_fable, SPEC_SKELETON_fable, REVIEW_disposition, and the relevant current R/C++ core. Read W3-SCALE CHECKPOINT_2 and all results TSVs from `origin/theory/W3-SCALE` at `299cbc582b45dcf5cb6cb88d56e32d9763847c82`. The checkout HEAD at the first engine audit was `c639c95c7e5689cd0f0de9cfe2c47ebc6719aced`; CP2's measured revision D is `6866f57`, core key `dd37d323a353`. These are distinct reference artifacts.

**Concurrent-edit qualification.** ENGINEERING_SPEC changed to v2 during this review. `ES1:L` below means `Docs/Experiments/P1M/ENGINEERING_SPEC.md`, **v1 line L as read at the start**, not the newly inserted v2 material. In the v2 copy inspected subsequently, the retained v1 body from its original line 13 onward is shifted by +92 lines. Thus, for example, ES1:110 is then ENGINEERING_SPEC.md:202. Other P1M paths below are relative to `Docs/Experiments/P1M/`; core paths are relative to `Scripts/SMC_BVS/core/`. SCALE paths identify files on the pinned remote branch. This verdict does **not** approve v2's newer kernel timings, occupancy evidence estimator, or replacement budget.

No cluster jobs, code changes, git-state changes, or external communications were performed. Arithmetic below is independently recomputed; unmeasured performance ranges are explicitly estimates. Finding totals count F1–F11 once each: **2 CRITICAL, 8 MAJOR, 1 MINOR**.

## 1. Feasibility: the likely breakpoints

| p | Single most likely failure point in the proposed ladder | Consequence and required evidence |
|---|---|---|
| 10⁴ | The changed start/bridge/calibration combination produces inadequate evidence precision even when all islands select the same HPM. | R6 already reports E2 at 10k, an unconverged grid, and only 6/16 completed census islands. Require completed, stage-recorded, paired overlap runs, including weak and masked signals, before extrapolating precision. |
| 10⁵ | The first genuinely parallel Gram-free implementation misses its cost or memory model through store/reduction overhead and bandwidth saturation. | This is the decisive end-to-end engineering rung; a scorer-only microbenchmark cannot clear it. |
| 10⁶ | Tables and replicated worker ledgers exceed the 32 GB task request. | Recompute table counts under the **new** partition and specify bounded-memory store merging before submission. |

Evidence: REQUESTS.md:62–87; ES1:104–126, 138–153, 215–224; EXPERIMENT_PLAN.md:122–136. These are failure predictions, not claims that any p level is intrinsically impossible.

### F1 — CRITICAL: the new partition invalidates the table-memory calibration

The spec carries over “mean block size 9” and approximately 210 table codes per column from the old dense partition (ES1:10, 110–124; EXPERIMENT_PLAN.md:260–263). OD-5 instead orders the truncated-linkage forest by minimum index and next-fit packs its roots (OWNER_DECISIONS.md:78–85; REQUESTS.md:110–121). For singleton roots, this creates blocks of **14**, not 9. Sparse noise graphs can give almost-full blocks; measuring the old rule does not establish the new rule's counts. The relevant quantity is **C = Σ_b 2^{|C_b|}**, not mean block size: the exponential makes the histogram essential.

For the full-block packing case at p = 1,000,000 and B = 14:

- C = 71,428 × 16,384 + 256 = **1,170,276,608 codes**, about **5.6×** the planned 210 million.
- `logr` alone uses **9.36 GB**. The retained `logr` + `sub_cum` + u32 `codes_by_size` need **23.41 GB** before conditional tables, convolution arrays, X, maps, stores, and workspaces. X adds 1.6 GB; conditional tables are roughly another 0.9 GB for full blocks.
- Keeping the planned setup-only `logm_tab` and int32 routes adds **14.04 GB**, rather than the advertised 2.5 GB. Those arrays plus retained per-code arrays already total **37.45 GB**, before X and setup workspaces.
- At n = 400, full B = 16 blocks give **4.096 billion codes**: **81.92 GB** retained per-code arrays and **131.07 GB** including the same setup-only arrays. The Full tier requires a separate memory configuration.

This is a counterexample to the **capacity model**, not a claim that every AR replicate attains full packing. IND and weakly connected regions make it particularly relevant. The engine indeed enumerates every code and builds the additional sampler arrays (`cpp/v3_start.h:76–95, 104–118, 139–148`). A 32 GB calibration request cannot hold approximately 26 GB of shared data plus the claimed 9–12 GB private allocation. File-backed mappings still count toward job memory when resident; mmap does not erase the working set.

**Required change:** compute actual block histograms and C with the production partition on every proposed design, including n = 400, before table allocation. Use exact byte accounting and a deterministic refusal/reconfiguration rule. Stream/drop setup arrays as early as their consumers allow, increase task requests, or document a variant with smaller table blocks. None of these resource corrections requires an impossibility claim about NOTS.

### F2 — CRITICAL: “per-thread ledgers” multiply an unbudgeted multi-GB object

WP3 explicitly includes per-thread ledgers; the parallel decomposition also says per-thread ledgers (ES1:46, 142). The memory table budgets **one** 40p + 1 store per island, approximately 2.2–4.5 GB including compaction (ES1:118–124). At 48 workers, independently retaining full-capacity stores can require **over 100 GB** even before compaction and shared tables. Four diagnostic ledgers also cannot be silently counted as one calibration ledger.

The algebra “top-c of the union of each worker's top-c” is correct, but it does not supply an O(c) implementation. Setting each worker's capacity to c/48 is incorrect: all global winners may originate in one worker. The current semantics are explicit top-c distinct-model stores (`cpp/v3_ledger.h:32–62, 72–78`).

There are further omitted peak terms: per-worker RB accumulators or fixed-chunk buffers, duplicate indexes, pool alignment, sorting/compaction scratch, and order arrays. With G = N = 2,500, the order array alone is **10 GB** at 1M, although T3 lists that G as a configuration (ES1:120, 214). The 56-byte store entry assumes k ≈ 7; supports may be as large as K = 100, so it is not a safe admission bound.

**Required change:** specify one bounded-memory store algorithm per process, with bounded worker buffers, exact threshold/deduplication semantics, deterministic flushes, and a peak-live-buffer calculation. Alternatively shard exact stores to external runs with a proved merge bound. Test the case where one worker supplies all winners. Budget all four diagnostic islands and RB scratch explicitly. This must precede WP3 implementation, not be deferred to the 1M pilot.

### F3 — MAJOR: cost arithmetic is defensible; the confidence attached to it is not

The historical approximately 3.8k billed CPU-h estimate is reproducible from the plan's formula:

`t_island = 2500 × (10^6 + 16) × (30 + 21.6) × 2 microseconds = 71.67 physical worker-hours`.

The old 26.34 island-equivalent fit therefore costs approximately **3,775 billed CPU-h**; the bounded 19-equivalent fit costs approximately **2,723 billed CPU-h**. This explains the revised 27 / 272 / 2,720 figures. The spec's separate 42-round formula gives 58.33 worker-hours per island; its difference from the 51.6-round effective formula must be labelled as measured/assumed overhead, not silently interchanged (EXPERIMENT_PLAN.md:255–274; ES1:258–277).

However, c = 2 microseconds was inferred from a **Gram-resident, cached** engine. CP2 does not measure the proposed Gram-free threaded scorer. The stored Gram access is visible at `cpp/v3_score.h:163–184`, and the old cache hit rate is approximately 0.31–0.38 in SCALE `results/profile_v31_step_cost.tsv:2–5`. Removing that cache and recomputing k correlations changes the work. The estimate can be a planning scenario, not a demonstrated pessimistic bound.

| Stage | Assessment of ES1:262–278 |
|---|---|
| Generate/preprocess | 1.6 / 3.2 / 8 GB for X at n = 200 / 400 / 1,000 is correct. Seconds-to-minutes is plausible; measure the actual generator, standardisation, hashes, and any per-worker regeneration. |
| Correlation tiles | Approximately 10¹⁴ multiply-adds, or 2 × 10¹⁴ flops, at (1M, 200) is correct. A 10–20 minute threaded pass is plausible only with measured canonical dot-product throughput and cache reuse. BLAS throughput with different reduction order does not validate a bit-preserving pass. |
| Partition/tables/start | The 0.5–2 minute setup claim is unsupported under F1. Include all table-store ingestion, size convolutions, iterative mode extraction, and tie fallback. Making recursion iterative removes stack overflow, not tie-DP complexity (`cpp/v3_start.h:237–268, 271–303`). |
| One island | 42 rounds contain approximately 1.05 × 10¹¹ elementary steps. At c = 2 microseconds, an ideal 48-core island is 1.22 h before the additional effective-overhead allowance, approximately 1.49 h with it; a 32-core task is approximately 2.24 h with that allowance. These require end-to-end efficiency measurements. |
| Calibration | Bounded rebuilds are a useful saving. But v1 explicitly puts four diagnostic groups in **one process** (ES1:36–38). With one socket total, three island-equivalents consume approximately **4.5 h**, then the final islands approximately 1.5 h. The 3–4 h fit latency instead needs more concurrent calibration cores, or cheaper work. Four separate socket tasks and four groups sharing one socket are different resource models. |
| Merge/tail/eval | Streaming roughly 36 GB of island-store payload in 3–5 minutes requires approximately 120–200 MB/s plus comparison/deduplication work. Plausible, unmeasured. A single k = 5 scan is approximately 6 million scores, but each search can perform many scans; calibration has searches too (`cpp/v3_engine.h:370–415`). Evaluation cost depends on retained mixture complexity, not solely p. |

The 168 TB/island X-traffic estimate is a useful **minimum-traffic scenario**, not a measured bandwidth bound. Label-major savings depend on actual accepted-state changes, distinct supports, special moves, store offers, and repeated passes. An aggregate cache hit rate cannot establish 1,500 distinct supports per round. Keep that kernel optional in the v1 budget until a complete round is timed.

**Budgets:** Minimal 11k, Standard 26k/31k, and Full 42k are plausible envelopes, not auditable totals yet. The authoritative v0.2 errata supersedes the old table, but no replacement cell-by-cell ledger reconciles it with added nulls, seed repeats, precision arms, ablations and census work (EXPERIMENT_PLAN.md:18–34, 278–294; OWNER_DECISIONS.md:101–115). Three Minimal 1M fits alone cost **8,160 CPU-h**, leaving 2,840 for everything else; five Standard fits cost **13,600**, leaving 12,400. An additional Standard 1M algorithm seed costs another **2,720**, approximately 10% of 26k. It must have a named row. A 20% contingency does not absorb a major efficiency or table-capacity miss.

**NOTS is not an allocation impossibility:** 16 × 96 CPUs = 1,536 billed hardware threads = **768 physical cores**, not 1,536 compute cores. At 32 GB/task that is 512 GB, below 2,304 GB. Even substantially larger requests can fit the aggregate cap, although node placement will worsen. The later memory-aware inventory finds only **10** nodes with 96 free CPUs and 32 GB unallocated, versus 19 at 64 CPUs (NOTS_FACTS.md:5–18, 38–41). Use actual allocated CPUs × elapsed time, including idle serial phases, failed jobs and retries. The absolute throughput lower bounds for 11k / 26k / 31k / 42k are approximately **7.2 / 16.9 / 20.2 / 27.3 h** at a continuously full cap, not completion promises. The 24 h/job and 150-task limits do not prevent this layout; dependency depth, fragmentation and memory do.

**I/O correction:** 50 GB scratch/fit excludes two checkpoint generations. Two full 2.2 GB generations × 16 islands add approximately **70 GB**, before calibration checkpoints, temporary outputs and retained input files (ES1:126, 228–234). Incremental checkpoints need a deletion/eviction representation and compaction policy, not only added entries: top-c stores evict models. Verify scratch purge/retention and log/cache paths; current free aggregate scratch is not a per-user storage guarantee (NOTS_FACTS.md:23–36).

### Work-package estimates, attached to F3

All reserves below are reviewer planning judgments, not benchmarks. The v1 package list is ES1:41–53.

| WP / v1 estimate | Credibility and risk-adjusted reserve |
|---|---|
| WP1 / 8 agent-days | Plausible but tight for binary formats, preprocessing edge cases, numerical fallbacks and a pinned reference. Reserve 8–10. |
| WP2 / 7 | Low: sparse linkage correctness, the changed block histogram, table stores, convolution and mode/tie handling are separate problems. Reserve 10–14. |
| WP3 / 9 | Low until F2/F4 are resolved. Deterministic stores, addressed sampling, RB reductions and restart are the hardest integration. Reserve 12–18. |
| WP4 / 7 | Tight: two calibration policies, diagnostic-state merges, global provenance, failure paths and tail flags. Reserve 8–12. |
| WP5 / 8 | Low for the entire statistical evaluator, predictive objects, fair competitors and scheduler harness. Reserve 10–14. |
| WP6 / 3 | Credible for a narrow prototype and bandwidth decision. Reserve 3–4; this does not fund a production label-major kernel. |
| WP7 / 3 | Credible only if every prior gate passes first time. Reserve 4–7 and explicitly fund reruns and code review fixes. |

That is approximately **55–80 agent-days**, with dependencies and review rounds. Three builders do not turn all tasks into independent work. Treat 3–4 calendar weeks as an optimistic schedule; approximately 4–6 working weeks is a more defensible reserve, with December's Minimal deliverable conditional on the early gates. This is schedule risk, not a reason to abandon 1M.

## 2. What preservation can actually mean

### F4 — MAJOR: the RNG, event ordering and counter contracts are incomplete

The decomposition is achievable in principle, subject to a more precise contract:

| Change/output | Required relationship |
|---|---|
| Compat scoring, tables, π₀, categorical boundaries, move order, resampling, serial reductions, stores, HPM/provenance, PIPs, evidence, flags and logical events | Bit identity to one **pinned** reference on admitted cases. Maintain an explicit exclusion list for timing, admission metadata, routes/cache/fresh counters as authorised. |
| New addressed streams with otherwise identical algorithm/configuration | Same law under the ideal independent-uniform premise; not the old seed-to-output map. |
| Threads, groups, scheduling and restart within one production arithmetic/configuration | Identical semantic output bytes to its particle-serial production reference, including all consumed events and reductions. |
| Chunked RB sums versus old serial sums | Class A: same exact-arithmetic expression, changed rounding. This is not a literal floating-point equal-law theorem. |
| Fixed N, changed R, changed partition and bounded calibration | New full-run laws. Same target is weaker than same output law. Freezing calibration preserves applicable conditional results; it does not reproduce the previous unconditional fit distribution. |

This largely matches ES1:159–195 and corrects overly broad readings of “position addressing makes both produce identical bytes” (ES1:28–35). Addresses cannot compensate for different scores, reduction trees, cached-state errors or event ordering.

**Missing RNG detail:** the tuple in ES1:92 lacks explicit calibration **tier and rebuild iteration**, and “stage or round” and “slot” are not an injective domain specification. Initial draws and independence proposals consume variable numbers of block categoricals (`cpp/v3_start.h:153–174`); permutations consume p + B + 1 uniforms (`cpp/v3_engine.h:193–211`); resampling has a separate purpose. State whether “calibration role” encodes every tier/iteration/island and whether slots separate order generation, resampling, categorical sizes/submodels and acceptances. Descendants of a resampled particle need fresh addresses by destination particle and time, rather than inherited stream state. Document integer widths, overflow limits and collision-free packing into the chosen generator's key/counter space. Debug I5 must exercise complete multi-rebuild calibrations.

**Missing event detail:** the merge key in ES1:94 omits tier, rebuild iteration and within-step event order. Current EventCtx carries tier and iter (`cpp/v3_ledger.h:24–30`), and the serial traversal is tables → inherited models → each entire island → final local search → LS0 (`cpp/v3_core.cpp:408–476`). A phase-first lexicographic key is not necessarily that traversal. Preserve the winning model's earliest **serial-reference** event with a complete event ordinal. Top-c content is order-independent; provenance is not. Table/inherited counters must be replayed with the original multiplicity even if their models are offered only once.

**An actual wrong invariant:** I4 equates logical counts with executed steps (ES1:204). An ordinary feasible Gibbs step emits a held event **and** a flip event, so an unsaturated round has approximately **2Np**, not Np, Gibbs logical events (`cpp/v3_engine.h:113–129`; `cpp/v3_ledger.h:104–112`). Define event identities by mechanism, including cap/self-loop cases. Otherwise correct runs fail the invariant or the new published cost measure silently changes meaning.

### F5 — MAJOR: T1–T7 do not establish the stated contract; T8 needs correction too

The new T8–T11 are valuable additions, but their current criteria leave gaps (ES1:210–224).

| Gate | What it establishes, and necessary repair |
|---|---|
| T1 | Kernel bit tests are useful. Include full-cap models, zero uniforms/categorical boundaries, near ties, nonnegative-Q and QR fallback routes, preprocessing's anchored branch, graph hubs and mode tie fallback. At p ≥ 10⁵ compare a sampled set of canonical Gram entries against a direct oracle; do not recreate the full p² reference in the scale harness. |
| T2 | Good regression anchor, not proof for every input. Pin source/compiler/libm/input hashes and compare the original reference as well as any rebuilt reference. If the rebuild changes bits, call that class A and keep both records; do not move the byte-identity baseline silently. |
| T3 | Strong execution check if it compares declared **semantic payloads**. A whole output file also contains timings/status metadata, so full-file hashes contradict permitted timing differences. Specify canonical payload hashes. Exercise late-arriving winners, repeated models, all special moves and different flush orders; one-thread and threaded paths can share the same bug. |
| T4 | “Compat against production” confounds RNG changes with deliberate partition/calibration/R changes. Hold data, N, R, partition and frozen grid fixed to test the RNG substitution; test each Δ separately as a target/accuracy comparison. Non-rejection of a Bonferroni two-sample test is not evidence of equivalence. Predeclare practical error margins, power and simultaneous uncertainty. |
| T5 | Scorer timing plus “numbers recorded” is not a pass threshold. Time an entire stage with permutation generation, all moves, RB accumulation, stores and checkpoints; separately time setup and calibration. Replace the budget with measured allocated CPU-h and memory high-water marks. Validate the actual NOTS node type, not only Owls. |
| T6 | A stage-boundary kill tests only that boundary. Also test calibration restart after V/grid replacement, kills during checkpoint writes/compaction, checksum fallback and repeated resubmission. Persist table mode, ledger thresholds, event provenance and all consumed-address coordinates. A slow stage cannot satisfy an unconditional ten-minute checkpoint interval without intra-stage checkpoints (ES1:228–234). |
| T7 | Covers one closed-form component, not predictive mixtures, quadrature, raw-scale conversion, calibration plots or store-law truncation. See F9. |

**T8's PIP criterion is not a valid unbiasedness test as written.** For finite N and finite burn-in, equal-weight RB PIPs can be biased; averaging 400 islands converges to that biased mean. A correct engine can therefore fail “PIPs within 3 s.e. of enumeration.” Conversely a noisy biased engine can pass. Distinguish (i) the unbiased evidence moment E[Ẑ_r] = Z; (ii) any **proved** unnormalised RB moment E[Ẑ_r ĥ_r] = Zπ(h), verified for the actual measured-round estimator; (iii) finite-N bias of PIP_eq and ratio-estimator error. Compare unnormalised moments where justified, and test a prespecified N/grid refinement ladder for approximation accuracy. Do not assume a terminal-particle identity automatically covers the coded RB statistic. Exact tests at small p validate implementation, not 1M mixing.

## 3. Evidence variance and pooling

### F6 — MAJOR: the plan diagnoses degeneracy but does not yet design for precision

The R6 answer materially qualifies the headline evidence (REQUESTS.md:62–88; SCALE CHECKPOINT_2.md:46–72 and results/b3_census.tsv:4–7):

- At 5k, N = 2,500 gives **16/16** islands, σ̂ = 0.755 and R_eff = **8.93**, not 1.6–4.2.
- The R_eff = **1.58** observation is the 5k N = 10,000 run with **14/16** islands. At 10k only **6/16** completed, R_eff = 1.97; at 20k **11/12** completed, R_eff = 4.22.
- These are one dataset per p and mostly incomplete runs. They establish a serious right-tail warning, not that increasing N cannot improve precision or that σ stays near one at 1M. At 5k robust σ fell from approximately 1.00 to 0.54 when N quadrupled; one tail observation raised the ordinary SD.
- Completed islands having the same best F resolves the apparent HPM discrepancy. It does not establish equal distributions, independent exploration, or accurate evidence. The census omitted the stage/store records needed to locate the variance.

For intuition only, a lognormal approximation with σ(log Ẑ) = 1 gives CV²(Ẑ) = e − 1 ≈ 1.72 and relative standard error **sqrt(1.72/16) ≈ 33%** for the pooled normaliser. Its asymptotic effective-island fraction is approximately e⁻¹. Heavy tails make this approximation optimistic. R = 16 does not amount to precise evidence just because selection is stable; a second seed and the same common calibration do not explore calibration uncertainty either.

**The three PIPs answer different questions.** PIP_eq retains finite-island bias as R increases. Evidence-weighted pooling can remove that bias as R → ∞ only under the appropriate unnormalised-moment identity and integrability, and can be unstable at finite R. PIP_𝒯 is exactly the posterior conditional on the visited store, with error bounded by omitted posterior mass; it can be confidently wrong if important models are absent. Agreement among all three can reflect common missed mass. The union HPM is insensitive to evidence weights but is still search-dependent (OWNER_DECISIONS.md:63–70, 193–225; EXPERIMENT_PLAN.md:309).

**Required design before G-C:** make a completed 64-island, stage-recorded precision study mandatory at selected overlap datasets, including one weak/ADJ-OPP dataset, rather than a Full-tier option. Cross N = 2,500 versus 10,000 and coarse versus refined frozen grids on a small subset; retain independent calibration seeds and final seeds. Compare cumulative log-increment variance, ESS, ancestors/distinct supports, store lower bounds, PIPs and predictive summaries. Pick N/grid/calibration settings from this independent study, then freeze them before final runs. Report uncertainty across independent fits, not a standard error that treats all measured RB contributions as independent.

Do **not** repair this by clipping large evidence weights, using median log evidence as log Z, or selecting completed/easy islands: those change the estimator or introduce selection bias. Keep the arithmetic mean normaliser and its limitations. Bounded calibration fixes cost and validity conditional on the grid; it does not guarantee a good grid. More particles/temperatures at the stages losing mass, stronger invariant moves, or more independent islands are design remedies to compare. A different estimator is **not forced by the existing data**, but “high precision at 1M” needs this study or must be withdrawn from the claim. The 64-island census costs quoted in OD-9 (approximately 150/1,500 CPU-h at 10⁴/10⁵) are a reasonable explicit reserve, subject to F3.

## 4. Experimental credibility

### F7 — MAJOR: the revised cells help, but calibration and replication remain underspecified

The spread of n at 10⁴, AR/IND/BLK examples, oracle predictive benchmark, nulls, second seeds, ablations and ADJ-OPP/weak 1M cells are useful. A three-replicate AR-strong 1M result can support an existence/scaling demonstration, not estimate selection consistency. The plan now mostly says this correctly (EXPERIMENT_PLAN.md:79–114, 138–186; OWNER_DECISIONS.md:204–215).

Three repairs are still needed:

1. **Make adopted arms executable.** The errata says nulls, seed repeats, ablations and ADJ-OPP are added, but the detailed cell table still lists ADJ as optional at 10⁴ and no corresponding mandatory 10⁵ stress cell. The second-seed 1M run becomes “if budget” in REVIEW_disposition.md:40. Publish a single manifest with exact cell/seed counts and costs. Freeze the configuration before the pilot if it counts as replicate one; if the pilot changes the method, retain it as pilot evidence and run a fresh confirmatory replicate (EXPERIMENT_PLAN.md:26–33, 98–114, 133–136; REVIEW_disposition.md:37–45).
2. **Call the proposed reliability curve what it measures.** With fixed deterministic S₀ and frequentist data replicates, binned inclusion frequency is a useful repeated-sampling diagnostic, but posterior probabilities need not be frequency-calibrated under that fixed truth. Add exact-PIP approximation error at small p and a separate prior-predictive calibration experiment if claiming Bayesian calibration. Five truths × 20 datasets supply only 100 positive labels per cell, while p nulls dominate the Brier score. Report active/null components, bin counts, uncertainty clustered by dataset, and the distribution of intermediate PIPs (EXPERIMENT_PLAN.md:149–152; OWNER_DECISIONS.md:96; REVIEW_disposition.md:69).
3. **Replicate uncertainty, not only fitted curves.** Use paired datasets/seeds for method differences and dataset-level intervals for selection/prediction. Two n points at 10⁵ cannot distinguish a stable slope from finite-sample curvature; a single n at 1M cannot demonstrate decay there. Keep C5's 1M claim at an out-of-sample accuracy point consistent with lower-rung trends. Define ADJ-OPP's full five-coordinate truth, placement and amplitude rule before running it; “screening drops it” is a hypothesis to measure, not a guaranteed property of every realised dataset (OWNER_DECISIONS.md:207–215).

Ablations can show whether start mode + LS0 already delivers the selected model. If so, justify the SMC expenditure through **measured uncertainty, PIP or predictive improvements**, not the same selection indicator. The optional occupancy-versus-store comparison must condition on the compared set consistently and carry omitted-mass uncertainty; it is not a mixing certificate.

### F8 — MAJOR: competitor “yes” and the 1–2% budget are unvalidated

The table names plausible methods but no pinned package versions, working individual-level code paths, convergence criteria, tuning costs or demonstrated large-p memory/time (EXPERIMENT_PLAN.md:201–219; OWNER_DECISIONS.md:140–148). Package names such as “ncvreg / biglasso” do not establish that each requested penalty is available through the intended mapped-data interface. Nor does a variational PIP automatically supply a complete predictive density.

Require a small harness acceptance run for each retained competitor, with the actual package/version, data conversion, tuning and prediction code. Count CV folds, restarts and all threads. Verify that large-p paths avoid hidden p² sufficient-statistic arrays. Report timeouts/convergence failures as outcomes with their allocated cost; do not remove difficult datasets.

Minimum convincing comparisons:

| p | Core comparison set |
|---|---|
| 10⁴ | Penalised baseline, at least one working variational BVS baseline, SIS → the same BVS engine, and equal-CPU-budget model-space MCMC with the **same prior/scorer**. Include T-versus-variant overlap and all selection ablations. |
| 10⁵ | Working lasso/variational baselines and SIS → the same engine. Retain a cost-matched sampler on at least one stress dataset if feasible; otherwise report the bounded-budget failure. |
| 10⁶ | At least a verified individual-level lasso and joint variational baseline, SIS → the same engine, and ablations on the identical primary/stress datasets. Claim joint scalability, not superiority to unrun samplers. |

For methods with different priors, evidence values are not directly comparable. If all selected supports are refitted through a common conjugate evaluator, label those results as common refits; separately evaluate each method's native predictive when defined. Establish residual-variance estimation and predictive uncertainty without test-data leakage. The proposed under-10-CPU-h aggregate competitor cost at 1M is an estimate to benchmark, not a launch assumption.

### F9 — MAJOR: the DIST evaluator needs error control beyond the closed form

The Gaussian single-density Hellinger formula in EXPERIMENT_PLAN.md:165–168 is correct for the stated Δ ~ N(m,s²), including its factor of two convention. That does not validate the Student-t mixture predictive calculation, standardised-to-raw coefficient/intercept transforms, or posterior-law sampling (EXPERIMENT_PLAN.md:154–179; ES1:218).

Required fixtures: identical densities, known mean/variance shifts, zero signal, empty support, nonzero sample centring, unequal column scales, finite mixtures, and the near-constant preprocessing branch (`v3_preprocess.R:35–67`). Check response variance scaling and the intended intercept convention against the actual W3-DIST object. Double the quadrature order and increase x draws until the reported numerical error is below a prespecified absolute tolerance; attach Monte Carlo uncertainty. “Three significant digits” against a random Monte Carlo reference is not a well-defined universal threshold near zero distance. Validate native predictive log scores separately from posterior-draw Hellinger.

Also distinguish **Z_𝒯 ≤ Z** from **Z_𝒯/Ẑ**. Only the former is a deterministic lower bound. The latter can exceed one and is not a reliable bound on store mass when Ẑ is noisy; do not silently clip it and certify P-STORE (EXPERIMENT_PLAN.md:178–179; REQUESTS.md:189–203; `v3_run.R:150–155`). A Markov lower confidence bound, 0.05Ẑ, provides no upper bound on Z and therefore does not certify small omitted mass.

The per-model relative cutoff 10⁻¹² is also not the same law as the complete store BMA. At 40 million entries the crude discarded relative-mass bound is as large as **4 × 10⁻⁵**; compute and report the actual omitted **sum**, propagate its distance/error contribution, and call the saved law a truncated approximation (OWNER_DECISIONS.md:220–223; REQUESTS.md:169–175). Truncation is inexpensive under concentration, but weak-signal mixtures need a measured model-count/cost guard.

### F10 — MAJOR: reconcile the reference contract and current owner scope before claims are attached

v1 promises “the same theorems, with each premise re-checked” for the shipped method (OWNER_DECISIONS.md:180–191; ES1:175–188). The later owner rule explicitly permits an engineered 1M variant, keeps theory attached to the coded 10⁴ method, and requires documented changes plus paired overlap validation, with the paper describing the 1M result as a variant (POLICIES.md:160–168; REQUESTS.md:213–220). Respect that newer scope; do not require cancelled premise tickets as an inferred permission barrier, and do not claim overlap agreement proves theorem transfer.

For the requested preservation assessment, retain a **pinned compatibility/reference configuration** separately from the engineered configuration. The current core includes the anchored standardisation branch and has a different source revision from CP2. ES1's generic “v3.1 / revision D” and the option to rebuild the reference under a new libm are insufficient version identifiers (ES1:9, 61–63, 165–173; EXPERIMENT_PLAN.md:9–10, 223; `v3_preprocess.R:37–67`). Hash the exact reference and new engine, fixtures, compiler flags, numerical libraries and manifests. Record compatibility differences against both the archived D outputs and the chosen current reference. The same-data overlap must compare the **whole chosen variant** against the reference; A1's N/R comparison plus A3's isolated partition comparison does not alone validate their interaction with bounded calibration and new arithmetic.

### F11 — MINOR: two reporting statements need precise qualifiers

- “3/3 gives a 95% lower bound of 0.37” is the **one-sided** exact binomial bound. A two-sided 95% interval has lower endpoint approximately **0.292**. Label the convention wherever it appears (EXPERIMENT_PLAN.md:29; OWNER_DECISIONS.md:215).
- “≤ 2B per column after symmetrising” is not a maximum-degree guarantee. The directed top-B graph has at most pB selections and at most 2pB total adjacency entries after symmetrisation; a single hub can have degree p − 1 (`cpp/v3_blocks.h:146–171`; ES1:108). The uncapped threshold graph used by the partition is a different object and needs its own edge-count guard. Test hubs rather than encoding a false per-column bound.

## 5. Five changes with the largest payoff, ranked

Costs are incremental reviewer reserves; avoid counting overlapping tasks twice.

| Rank | Change | Cost | Payoff |
|---|---|---|---|
| **1** | Replace the memory model with production-partition code counts and a bounded-memory exact store design; include diagnostic replicas, RB buffers, orders and checkpoint peaks. Resolve F1/F2 before WP2/WP3. | Approximately 3–5 agent-days for the capacity/design audit; approximately 20–50 billed CPU-h for targeted measurements, then implementation inside the relevant WPs. | Prevents an immediate 1M out-of-memory failure and determines whether n = 400 is a different resource class. |
| **2** | Complete and freeze a precision study: stage records, independent calibration/final seeds, weak/ADJ cases, N and grid refinements; keep the unbiased evidence estimator and quantify its error. | Approximately 2–3 analysis days plus an explicit approximately 1–2k CPU-h overlap-study reserve, resized from measured costs. | Replaces “islands agree” with evidence about accuracy; decides whether 1M produces scientifically useful posterior summaries. |
| **3** | Make T5 an end-to-end NOTS gate and produce one costed cell/seed manifest for Minimal/Standard/Full. Choose CPUs from the measured saturation curve and current memory placement. | Approximately 2–3 agent-days and approximately 100–200 CPU-h for bounded full-stage/setup/calibration pilots; reuse these measurements in WP6/WP7. | Validates the 2,720/3,800 CPU-h scenarios, exposes serial calibration latency, and prevents contingency from hiding missing cells or low parallel efficiency. |
| **4** | Freeze the reference, injective RNG domains, serial event ordering and logical-event definition; repair T3/T4/T8 and extend restart/failure tests. | Approximately 4–6 agent-days, largely within WP1/WP3/WP7; gate compute separately ledgered. | Makes compatibility claims reviewable, prevents address reuse/provenance drift, and separates target accuracy from equality of sampler laws. |
| **5** | Publish the executable science/competitor manifest and validate all predictive objects. Protect lower-rung calibration/null/stress replication before buying more easy 1M examples. | Approximately 3–5 agent-days plus harness pilots; a second 1M seed is explicitly another approximately 2,720 CPU-h under v1. Reallocate cells within the chosen ceiling. | Produces referee-relevant accuracy/cost comparisons and defensible predictive/calibration conclusions instead of a scale-only demonstration. |

Release the ladder only against measured capacity, cost and accuracy gates. None of these findings establishes a NOTS infrastructure obstruction to joint SMC-BVS at 1M; they establish that the requested v1 plan needs the listed corrections before its production promises can be accepted.

EXP-CP1 VERDICT=GO-WITH-CHANGES critical=2 major=8
