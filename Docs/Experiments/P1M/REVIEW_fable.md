# REVIEW — p = 10⁶ experiment plan (independent review, Fable 5.2, 2026-11-15)

Scope: `EXPERIMENT_PLAN.md` v0.1, `ENGINEERING_STRATEGY.md` v0.1, `OWNER_DECISIONS.md` v0.1, `NOTS_FACTS.md`, W3-SCALE
CP1/CP2/DESIGN_v1 rev 3 and `results/*.tsv`, the core at `Scripts/SMC_BVS/core/` (main checkout), PROGRAM, theory status
11-13, W3-DIST STATEMENT v1.3.1 §0 and §2, SCALING_DESIGN_v0. `HOLDS.md` was empty at 19:05 CST.
Read-only review: nothing was built or run. Every number marked **(guess)** is my estimate and has to be measured.

Preservation classes used below (the plan's tags, plus one it lacks):

| class | meaning |
|---|---|
| **B** = [OP-bit] | same output bits as the reference engine |
| **A** (new) | same map from (data, uniforms) to output in exact arithmetic; only rounding differs (summation order, vector `log`). Covered by the theorems' exact-arithmetic premise (EX-A), but a run can diverge from the reference at a tie |
| **L** = [OP-law] | same law of every output under the ideal-stream premise; different use of the streams |
| **C** = [Δ𝒞] | changes only how the frozen calibration is computed |
| **Δ** = [Δlaw] | changes the law; premises to re-check are named |

---

## 0. Verdict in six lines

1. The plan's ladder, gates and budget logic are sound, and its two law-level findings (fixed N, partition wall) are right.
2. **Three things in the plan are wrong or incomplete and each one blocks 1M**: the escalation fix (OD-2) misses two
   triggers that fire at large p; the partition rule (OD-5/G3) recreates the p² wall on the primary design AR(0.6);
   the threading plan ignores that the Gram-free step is bound by memory bandwidth at 1M.
3. Calibration is about 40% of the cost and all of the sequential depth. The data say its rebuild loop does not converge
   at p ≥ 5k. A bounded calibration (class C) is the cheapest large saving available.
4. The hot path can probably be made 5–15× cheaper **(guess)** in the same class the plan already accepts (L), by
   addressing uniforms by position and sweeping labels, not particles, through X.
5. The evidence-variance problem should be diagnosed from records that already exist before any design choice rests on it.
6. As designed, the 1M rung shows feasibility but not that the joint SMC run was needed. Two extra cells and three
   ablations fix that.

---

## 1. Ranked improvement opportunities

### R1. Calibration: close the escalation hole and bound the rebuild loop — blocks feasibility; −30 to −40% cost

**What.** (a) In large-p mode, no trigger escalates except grid-construction failure. (b) Replace "rebuild until the
grid is bit-identical, at most ℓ times" by a declared bounded rule (I_max rebuilds, I_max = 2 or 3; or the pilot
schedule alone). (c) Decide (b) from a three-arm comparison at 10⁴.

**Why.**
- `fired <- any(unlist(a$triggers))` (`v3_calib.R:154-155`) tests **seven** triggers: E1, E2, E3, forced pilot steps,
  grid failure, **`grid_unconverged`** and **`local_limit`** (`v3_calib.R:60-61, 118`). OD-2 option (b) disables E2 only
  and lists five triggers. The other two still escalate.
- Convergence means `identical(gn$grid, g$grid)` (`v3_calib.R:115`): a bitwise fixed point of a grid built from V,
  where V is the two leader stores (up to 40p + 1 models, `v3_core.cpp:703-716`). Each rebuild adds scored models, so
  V keeps changing at large p.
- B3 (`results/b3_census.tsv`, H = 512): rebuilds = 8, **13, 14, 15** at p = 2k, 5k, 10k, 20k. The cap is
  ℓ = ⌈log₂(n + p + 1)⌉ = 12, **13, 14, 15** (`v3_preprocess.R:23`). The loop hit its cap in 3 of 3 runs at p ≥ 5k.
  The `converged` flag is in the `.rds` on NOTS but not in the table; if it is FALSE, `grid_unconverged` fires on
  every large fit and the ×4 escalation survives OD-2(b). **Ask HQ to read `calibration$converged` and
  `calibration$triggers` from the three records.**
- E2 itself is a noisy test: a standard deviation from 4 islands (3 degrees of freedom). At true σ = 1 it fires with
  probability 0.39, at σ = 1.4 (the 5k diagnostic median, CP1 §4) with 0.68. Escalation did not cure the 5k tail (CP2 §3).
- Hidden serial work per rebuild at 1M, absent from the plan's wall-time model: V is re-scored from scratch
  (`v3_core.cpp:713-716`, 4·10⁷ scores, 20–80 s **(guess)**), and the grid construction sums over V in a fixed order
  for every bisection (`v3_calib.h:11-16, 55-58, 81-85`). Measured grid build: 8.07 s at |V| = 8·10⁵
  (`profile_v31_stages.tsv`), so 0.7–7 min per build at |V| = 4·10⁷ (extrapolated; the table does not say whether
  the 1k–5k values are per build). With 20 rebuilds that is 0.5–2.5 h of single-thread time inside a "threaded" calibration.

**Effect.** At 1M with I = ℓ = 20 a fit is 16 + 0.82·20 + 0.5 = 32.9 island-equivalents. With I_max = 3 it is 19.0
(−42%); with the pilot schedule alone 16.2 (−51%). Sequential depth falls from 21 island-rounds to 4 or 1. The OD note's
"calibration ≈ 4.5 h of a 6.5 h fit" becomes about 1 h.

**Class.** C. Results stated "for any frozen 𝒞" (LT♯, TR, RM-0, N1) are untouched. Re-check: C-DLV (which uses the
tier-1 fallback on construction failure, kept), and any card item that reads E2 or `grid_unconverged`. The pilot
schedule as a grid is already a coded path (`v3_calib.R:122-124`).

**Cost.** 1–2 agent-days in the engine. Evidence arm at 10⁴ (5 datasets × 3 calibrations × 16 islands, same data):
about 300 core-h. Metrics: σ̂(log Ẑ_r), minimum ESS share, PIP agreement, HPM, T. Free first step: the per-iteration
grids are archived (`calibration$tiers[[e]]$grids`); compute max_t |φ_t^{(it)} − φ_t^{(it−1)}| on the saved B3 fits.

Note on the plan's cost model: it assumes I = 12 at 0.82 island-equivalents per rebuild. B3 gives I = ℓ at 0.5–0.8
per rebuild (10k: 5.91 h against a 0.70 h island; 20k: 6.68 h against 0.82 h). At 1M that is 10.5–16.5
island-equivalents against the plan's 10.3: the two errors cancel if the 10k–20k value (0.5–0.6) holds, and the
calibration is up to 60% dearer if the 2k–5k value (0.8) holds. The escalation logic is what fails either way.

### R2. Hot path: the 1M step is bound by memory bandwidth; sweep labels, not particles — cost 5–15× (guess), removes a scaling risk

**What.** (a) Address every uniform by (island, stage or round, particle, position in the round, slot) with a
counter-based generator, instead of one sequential stream per (stage, particle). (b) Use that to run each round
**label-major**: one pass over X serves all particles. Pass 1 computes, for each label j, the products X_Aᵀx_j for the
active set A (union of the particles' supports) and the Gibbs odds of every distinct support; each particle then finds
its first accepted flip from its own uniforms; particles that changed state go to pass 2 with their new support; and
so on. (c) Before building it, measure the bandwidth limit (T5).

**Why.**
- A Gram-free Gibbs step must read column x_j: 8n = 1.6 KB at n = 200 (`v3_score.h:163-173` shows the entries needed).
  One island is 2,500 × 10⁶ × 42 rounds = 1.05·10¹¹ steps, so 168 TB of column traffic. A fit with I = 12 is about 4.4 PB.
- A Sapphire Rapids socket delivers 100–200 GB/s usable **(guess; not measured on NOTS)**. So the direct scorer needs
  at least 6–12 socket-hours per fit, i.e. 600–1,200 billed core-h, whatever the code quality. Per thread, with 48
  threads on a socket, a step cannot cost less than 0.4–0.8 µs.
- The plan's target (0.5–1.0 µs, "≈ linear to 48 threads", ENGINEERING_STRATEGY §3–§4) sits at that floor. Hyperthreads
  add nothing there, and the nodes are shared (NOTS_FACTS: no SPR node fully idle). SCALING_DESIGN_v0 §3.3 named
  bandwidth as the limit but nobody has sized it.
- Per-particle streams are already the plan's recommendation (OD-8(b), class L, obligation O5). Position addressing
  costs no extra theory and is what makes any execution order legal: every uniform has an address fixed before its
  value is read. Within a Gibbs segment each label consumes exactly one uniform (`v3_run.R:32`), so addresses do not
  depend on the state.
- The population is diverse: hit rate 0.38 and 127 cache clears in a 20k island (`profile_v31_step_cost.tsv`) imply
  about 1,500 distinct supports per round among 2,500 particles. So the saving is per score (vectorised across labels,
  in cache), not in the number of scores.

**Effect (guess, to be replaced by a prototype number).** X traffic per round falls from N passes to (number of passes
× N / G) for particle groups of size G (G = 256: about 60 passes instead of 2,500). Per score 40–200 ns instead of
600–2,000 ns; the low end needs a vector `log`/`exp` that returns the scalar routine's bits (the plan's pinned
transcendental functions). Island at 1M: 3–8 thread-h against 22 (plan target 0.6 µs), 43 (plan value 1.2 µs) or 72
(planning cost 2 µs). A 1M fit: 150–450 billed core-h instead of 1,100–3,770.

**Class.** L, the same as OD-8(b). Within production mode, label-major and particle-major execution must give the
same bits (a deterministic gate). Compat mode (serial v3 stream) keeps the scalar path; the kernels are shared, so
T1/T2 still anchor the arithmetic.

**Cost.** 2 agent-days for a kernel prototype on Owls at p = 10⁵ (decision gate), then 8–12 agent-days in place of
G8's 3–5. If the prototype misses, the fallback is the plan's design with three cheap items, all class B once OD-3
is decided:
- no global score cache (a probe into a multi-GB hash table costs about as much as the score it saves; `v3_score.h:274-293`);
- software prefetch of upcoming columns (the round order is drawn before the steps, `v3_engine.h:202-203`);
- cached Gram rows for long-lived members (halves the traffic **(guess)**; about half of the null inclusions involve
  variables outside any affordable row cache).

Two corrections to ENGINEERING_STRATEGY §3–§4 that apply either way:
- "Bordered update, [OP-bit]" holds only as **prefix reuse in sorted order**: the model is kept sorted
  (`v3_util.h:129`) and the Cholesky runs row by row (`v3_score.h:76-90`), so inserting j at sorted position q
  recomputes rows ≥ q. A rank-one update or downdate changes the bits (class A). The labels between two members of S
  share q, which is what makes the vector version regular.
- "Every reduction in particle order, so identical for any thread count" does not cover the RB accumulators
  (`v3_engine.h:128`): p-wide floating-point sums over particles. They need a declared reduction order (v0 P5). With
  fixed chunks the result is thread-invariant but class A against compat mode.

### R3. Partition rule: the proposed rule fails on AR(0.6) — blocks 1M on the primary design

**What.** Replace "exact complete linkage inside the connected components of {|r| ≥ τ_n}" (G3, OD-5(c)) by **complete
linkage truncated at height 1 − τ_n**, computed on the sparse threshold graph: merge two clusters only while every
cross pair is an edge. Then the existing top-down cut for clusters larger than B, and next-fit packing with clusters
ordered by minimum index.

**Why.** With τ_n = r_n = √(2 log p / n) = 0.372 at (10⁶, 200) and 0.263 at n = 400, every adjacent AR(0.6) pair is an
edge (population r = 0.6; lag 2 is 0.36). The threshold graph is one component of size p, and "exact linkage inside
the component" is again the 16p²-byte problem (`v3_blocks.h:53-55`). BLK (components of 20) and IND (mostly
singletons: about 7.5·10⁴ null edges expected at 1M) are fine. The truncated rule needs only the edges, O(pB) memory,
and it equals the exact dendrogram below height 1 − τ_n (complete linkage merges in increasing height), so the same
tie rule R13 applies. This is DESIGN_v1 §5's "sparse exact-below-threshold partition" (v0 B4); the P1M wording
drifted from it.

**Effect.** Removes the wall on all three design families. Memory O(edges): about 2–3 p edges for AR.

**Class.** Δ on π₀ only, as in the plan. T-PART must be asked about this rule, including the new packing order
(minimum index instead of dendrogram leaf order). A3 at 10⁴ stays as the paired comparison.

**Cost.** Unchanged (5 agent-days + T-PART), but the theory question changes, so settle the wording before T-PART starts.

### R4. Evidence variance: diagnose from saved records first; report a deterministic bound; add a weight-free PIP

**What.**
1. Zero-cost analyses on the six B3 fits (records on NOTS):
   - variance over islands of the cumulative log increment, by stage (`cum_log_Z` per island and stage is in every
     stage table, `v3_run.R:57, 158`). This locates where the dispersion and the right tail are created;
   - **log Z_𝒯 := log Σ_{S∈𝒯} e^{F(S)}** against each log Ẑ_r. Z_𝒯 ≤ Z is a deterministic lower bound, because F is the
     exact log of the unnormalised posterior mass (`v3_engine.h:97`). If most islands sit below it, the typical
     island under-estimates and the "lucky" island is the accurate one.
2. Report the evidence as a sandwich: log Z_𝒯 (certain), log Ẑ and σ̂, `log_Z_lower95` (Markov). No estimator switch.
3. Add **PIP_𝒯,j = Σ_{S∈𝒯, j∈S} e^{F(S)} / Σ_{S∈𝒯} e^{F(S)}** on the merged store as a third reported PIP. It needs no
   island weights, it is the marginal of the store-BMA law of DIST-C(i), and its error is at most the posterior mass
   outside 𝒯.
4. Keep equal-weight `pip_primary` as primary (OD-4 is right). Do not use R′ = 8 if PIP_Z is reported: at σ = 1,
   R_eff/R′ ≈ e^{−σ²} = 0.37, so 3 effective islands.

**Why.** DESIGN_v1 §4.4 lists "why the right tail occurs" as unknown, yet the per-stage increments were saved. At 5k
the median log Ẑ_r rose by 0.6 from N = 2,500 to 10,000 while one island sat 4.4 above the median (b3_census.tsv):
that pattern is an estimator dominated by rare events in some stage, and the stage is identifiable from the records.
A likely mechanism **(guess)**: with N fixed, the expected number of particles carrying the mass at an early stage
falls like 1/p; the v3.1 rule N = p kept it constant.

**Also check.** `b3_census.tsv` has `islands_same_best = FALSE` in three rows (5k N = 10⁴, 10k, 20k), all with status
`resource_limit`. CP2 §3 says every island found the same best model. The column is
`length(unique(round(island_best, 8))) == 1` (`analysis/b3_census_table.R`), so unfinished islands may explain it, but
the plan's trigger "islands disagree on the HPM" (R1 of its risk register) depends on which reading is true.

**Effect.** Turns R1 of the risk register from "report" into a diagnosed mechanism, and gives C7 a number that is not
noisy. If the dispersion is created in the first stages, the remedy is more particles there (Δ), not more islands.

**Class.** B for all existing outputs (additions only). **Cost.** 1 agent-day of analysis; PIP_𝒯 is a few lines in the merge.

### R5. Make the 1M rung convincing, not only feasible

**What and why.**
- **Ablations on every dataset** (cheap: no islands needed): (i) the start mode alone, (ii) start mode + LS0,
  (iii) pilot + final local search, (iv) the full fit. With s₀ = 5 strong signals spread evenly and one truth per block
  (plan §2.2), π₀ probably puts S₀ at its mode (claim C3 says π₀(S₀) → 1). If (ii) already returns S₀, a referee will
  ask what 99% of the core-hours bought. The honest answer is PIPs, the evidence and the store-BMA law, and the tables
  should say so.
- **One screening-adversarial cell at every rung, 1M included.** Example: two adjacent AR truths of opposite sign
  (β = 1 and −0.8 at ρ = 0.6: the second has marginal effect −0.2, so −0.2·√200 = 2.8 against the 1M noise maximum
  5.3). SIS → BVS drops it; a joint method need not. Without such a cell, "SIS → exact BVS" will tie the method at 1M
  for 10⁻³ of the cost. The plan has ADJ as an optional arm at 10⁴ only.
- **One weak-signal cell at 1M** (a = 0.6). Otherwise every PIP at 1M is 0 or 1 and C4/C5 are trivially met there.
- **Wording of C2 at 1M.** Three fits cannot estimate a probability: 3 of 3 gives a one-sided 95% lower bound of 0.37
  (5 of 5: 0.55). State the 1M rung as feasibility plus agreement with the trend of the lower rungs.
- **Separate data noise from algorithm noise.** Every replicate draws fresh data. Add a second seed on the same
  dataset (10 datasets at 10⁴, one at 1M) and report output agreement across seeds.
- **A sampler check that needs no ground truth, at any p:** occupancy frequency of the terminal particles against the
  exact renormalised weights e^{F(S)} / Σ_𝒯 e^{F} on the visited models. This needs the terminal supports (§3).
- **Null control:** y independent of X (s₀ = 0 is covered by W3-DIST §0) at 10⁴ and 10⁵: HPM = ∅, largest PIP reported.
- **Equal-budget model-space MCMC** at 10⁴ and 10⁵ (add–delete–swap or wTGS on CPU, given the same core-hours).
- **Exact reference for the new engine:** at p ≤ 25 force the SMC branch and compare PIPs and mean Ẑ/Z with the
  enumeration branch, for fixed N, the new partition and the new calibration. This is the direct test of every law change.
- **Freeze before rung C:** configuration hash, evaluator version and competitor settings fixed before the 1M pilot.
  The pilot counts as replicate 1 only if nothing changes after it. Report every submitted fit, including failures.

**Class.** n/a (design). **Cost.** Ablations and the null control: under 100 core-h. The two extra 1M cells cost two
fits; with R1 + R2 they fit inside the Standard tier, without them they replace IND at 1M.

### R6. Memory and I/O items missing from the gap list

| item | evidence | consequence at 1M | fix, class |
|---|---|---|---|
| Leader stores | `v3_ledger.h:72, 78`: two more stores of 20p each; `std::set` of vectors (`:46`), about 120 B per entry | 4·10⁷ further entries per ledger; G7 sizes the top store only. As coded, 80p entries ≈ 9.6 GB per ledger | final islands do not need them (they feed V only); dropping them from the final output is a reporting change (owner). Flat stores: B (top-c under a strict order does not depend on insertion order) |
| Table ingestion per ledger | `v3_core.cpp:372-386, 408, 613` | 2·10⁸ ledger events in every island and in calibration | ingest once in setup into a table top store; merge unions it. B |
| Inherited models | `v3_core.cpp:419-428, 728-735` | up to 8·10⁷ models passed as a list and re-scored per final run | binary store with stored scores; offered once at the merge. B |
| `start_mode` recursion | `v3_start.h:281-301`: `std::function` recursion of depth J | J ≈ p/9 ≈ 1.1·10⁵ frames: stack overflow risk under the default 8 MB limit | iterative enumeration. B |
| Tie-aware DP | `v3_start.h:237-270`: p calls of an O(J·K·B) feasibility pass | ≈ 1.6·10¹⁴ operations if the tie enumeration is ever truncated | incremental feasibility, or a declared refusal status at large p. B |
| Standardisation | `v3_preprocess.R:35-51, 111`: R's `mean` (two passes, long double) | a C++ port will not match bits unless it copies that arithmetic | give compat mode the R-standardised X as binary input; gate the C++ standardiser separately (B if it matches, else A) |
| Capacities ∝ p | store 40p + 1, leaders 20p, V ≤ 40p + 1 | the plan decouples N and the cache from p but keeps these; they set the store memory and the grid-build time | owner question Q3; class C for V, reporting for the store |
| Task memory | OD note 2: `--mem ≈ 20G` per 96-CPU task | X 1.6 GB + tables ≈ 5 GB (file-backed pages are charged to the job) + top store 2.2–4.5 GB + working set | plan 32 GB per island task; SPEC_SKELETON §2 |

### R7. Use of the allocation

- Bill by socket, not by thread: if the direct scorer is kept, find the thread count at which a socket saturates
  (T5) and request that many CPUs. Billing is allocated CPUs × wall (NOTS_FACTS).
- A1 at 10⁴ compares N = 10⁴ × 4 islands with N = 2,500 × 16 islands: the same 40,000 final particles. Say so in the
  write-up; it makes A1 an equal-particle comparison of "few large" against "many small" islands.
- With R1 + R2 an island at 1M takes under one hour of wall time on a socket **(guess)**, so the 1-hour `scavenge`
  queue with stage checkpoints becomes a real option (ENGINEERING_STRATEGY §6 mentions it).

---

## 2. Screening-free versus screened: assessment

- Keep the claim screening-free. Every particle sees all p labels in every round; the block tables and the neighbour
  graph are built from all columns. Nothing in R1–R3 changes that.
- Do not adopt v0's law-changing shortcuts (P9: screened proposals, random-subset sweeps). With R2 the full sweep is
  affordable, and each shortcut would need its own kernel theory. v0 already showed that an exact skip of null
  coordinates costs the same dot products as the score.
- The comparison must contain a case where screening loses (R5). Add "SIS to d = 10⁴ → our own method" as a competitor:
  it isolates what the joint run adds over the same method on a screened set.

## 3. Option (not a default): returning posterior draws or a predictive

What the run could return, and what each costs at p = 10⁶. All are additions: every existing output keeps its bits
(class B), provided the post-processing reads streams disjoint from the SMC streams.

| object | what it is | cost at 1M | buys the theory | buys the experiment |
|---|---|---|---|---|
| Terminal particle supports | the N models of each island after the last measured round (they exist in memory and are dropped, `v3_engine.h:351-367`) | about 100 KB per island (sparse supports); no time | nothing by itself: DIST-C makes no statement about a particle approximation (STATEMENT §2 "honest label"). A law built from them needs a new sampler statement for the terminal population, probably a corollary of TR (to be checked by theory) | the occupancy check of R5; a mode-occupancy record for the right tail (R4); model-size and credible-set summaries |
| Store-BMA law as a file | models of the merged store above relative weight 10⁻¹², weights e^{F}, and per model the conjugate parameters (mean, factor, shape, Q_S) with the standardisation constants of its columns | a few KB to MB; seconds | this is Π̂^𝒯 of DIST-C(i), exactly; conditional on P-STORE as stated there | the predictive density, quantiles and Hellinger metrics become functions of one small file; competitors can be scored by the same evaluator |
| Draws of (model, β, σ²) | M draws: a model from a chosen law Q (store weights, HPM, MPM, or particles), then the conjugate draw given the model | M = 10⁴: about 1 MB, under a minute; needs only the columns in the drawn models | for Q = store weights: draws from Π̂^𝒯, covered by DIST-C(i). For Q = particles: not covered | interval coverage, posterior of d_H (plan §3.3 item 2 already draws these inside the evaluator) |
| Predictive at new x | mixture over models of Student-t densities | negligible; only columns in ∪S | f̄^𝒯 is the object of DIST-C(i)'s second display | log score and coverage on fresh rows |

Recommendation if the owner wants the option: archive the terminal supports always, labelled as a diagnostic and not
an estimate; make the store-BMA file the method's "distribution output", since it is the one object the candidate
theorem covers; keep particle-based laws out of headline claims until theory supplies the terminal-population
statement. New returned fields change the "method as coded", so they need a registry entry.

## 4. Risks and blind spots of the plan

1. **Escalation through `grid_unconverged` / `local_limit`** (R1). Probability high, impact ×4 cost.
2. **Bandwidth** (R2): the thread-scaling assumption is unverified and the floor is close to the target. No gate
   measures it before G-B. Add it to T5.
3. **Partition rule on AR** (R3).
4. **The 1M design is the friendliest possible** (strong, isolated, evenly spaced truths). Selection there is probably
   decided by the start law (R5).
5. **Theory coverage of the shipped method.** The briefing's sentence is "an output-identical engine inherits every
   theorem". The 1M method is not output-identical in five places: fixed N, R′ = 16, stream layout, partition,
   calibration rule. Each needs its row in a premise table (SPEC_SKELETON §4); the plan has tickets for two (T-N,
   T-PART). The stream layout (O5, O18) and the calibration rule have no ticket.
6. **One n at 1M.** C5 is a statement about decay in n; at 1M the Standard tier has n = 200 only. With R1 + R2 the
   n = 400 cell is affordable, but its tables are about 2·10⁹ codes (plan §6.1): roughly 16 GB for `logr` alone and
   10× the setup. Check the table memory before promising it.
7. **PIP calibration is thin.** s₀ = 5 with 5–10 replicates gives about 50 true variables and a handful of nulls with
   intermediate PIP: a reliability curve in ten bins has about 5 points per bin. Use a dedicated arm at smaller p with
   more replicates, or report agreement with exact PIPs at small p instead.
8. **Timeline.** 46 agent-days of engine work are placed in 11-23 → 12-11, across Thanksgiving week, with the Sol
   review inside the same window. The plan's own risk R11 covers the slip; the Minimal tier should be the stated
   expectation for December.
9. **Reference for bit tests after pinning libm.** Pinned `log`/`exp` will not reproduce the v3.1 records if glibc's
   FMA variants were used on the reference nodes (DESIGN_v1 appendix lists this as unverified). Rebuild v3.1 against
   the pinned routines and regenerate the 34 reference units (about 20 task-hours), then compare old and new records once.
10. **Data generator.** "One stream per column chunk" does not define AR(1) across chunk boundaries. Define the
    generator as one sequential recursion over columns (seconds at 1M), with test rows from the same definition.

## 5. Points in the plan I think are wrong (with evidence)

| # | statement | where | evidence |
|---|---|---|---|
| 1 | OD-2(b): "E2 does not escalate; grid failure, E1 and E3 still escalate" is the full list | OWNER_DECISIONS OD-2; plan §0 item 1 | seven triggers, `v3_calib.R:60-61, 118, 154-155`; rebuilds = ℓ in 3 of 3 B3 runs at p ≥ 5k |
| 2 | Threshold components + exact linkage inside removes the memory wall | plan G3, OD-5(c), ENGINEERING_STRATEGY §5 | AR(0.6): r = 0.6 > r_n = 0.372, one component of size p |
| 3 | "≈ linear to 48 threads per island"; target 0.5–1.0 µs per step | ENGINEERING_STRATEGY §3–§4 | 1.6 KB of X per step; 168 TB per island; floor 0.4–0.8 µs per thread at 48 threads (bandwidth figure is a guess, the traffic is not) |
| 4 | "I ≈ 12 at every p" | plan §6.1 | b3_census.tsv: 13, 14, 15 = ℓ |
| 5 | Calibration per rebuild 0.82 island-equivalents | plan §6.1 | measured 0.5–0.8 (10k: 5.91 h / 0.70 h; 20k: 6.68 h / 0.82 h; 5k: 1.89 h / 0.17 h). Errors 4 and 5 cancel only at the low end |
| 6 | "Output is identical for any thread count" as stated | ENGINEERING_STRATEGY §4 | RB sums, `v3_engine.h:128`, need a declared reduction order (v0 P5) |
| 7 | Factor cache with a bordered update is [OP-bit] | ENGINEERING_STRATEGY §3 | only prefix reuse in sorted order is; `v3_score.h:76-90`, `v3_util.h:129` |
| 8 | G7 covers the stores | plan §5 | leader stores are 4·10⁷ further entries; `v3_ledger.h:72, 78` |
| 9 | C2 "at every p of the ladder" as a probability statement | plan §1 | 3 replicates at 1M |
| 10 | `--mem ≈ 20G` per island task | OD note 2 | R6, last row |

## 6. Questions for the owner

- **Q1.** May the large-p calibration be a declared bounded rule (no escalation except on construction failure, at
  most I_max rebuilds), given that the theorems hold for any frozen schedule? Which delivered statements mention E2,
  tiers or grid convergence?
- **Q2.** The shipped 1M method will differ from v3.1 in law in five places (fixed N, R′, streams, partition,
  calibration). Is the paper's parallel-method claim then "the same theorems, premises re-checked change by change",
  with v3.1 bits kept only in compat mode?
- **Q3.** The store, leader-store and V capacities scale with p (40p + 1, 20p). Keep them at 1M (2–10 GB per ledger,
  minutes per grid build), or cap them? The DIST statement names the 40p + 1 store.
- **Q4.** Should the 1M rung contain a case where the joint SMC run is needed (weak or masked signal), at the price of
  one or two fits, or is a pure feasibility result on the easy design enough?
- **Q5.** Do you want new returned objects (terminal supports, store-BMA file, PIP_𝒯)? They are free to compute but
  change the method's output list.
- **Q6.** Is one week for a kernel prototype (R2) acceptable before the engine build is fixed? It decides between a
  1M fit of about 300 and about 2,000 core-h.
- **Q7.** One n at 1M: is "decay in n shown at 10⁴ and 10⁵, one point at 10⁶" acceptable for the distribution-consistency claim?
- **Q8.** Are the final-run leader stores (`v3_run.R:210`) read by anything you care about?

## 7. Requests that cost nothing (for HQ, read-only on NOTS)

1. From `/scratch/fb31/w3scale/out/b3_p*/res/census_p*.rds`: `calibration$converged`, `calibration$triggers`,
   `calibration$diag_sd`, and `runs[[N]]$island_best`.
2. From the same records: per-island `cum_log_Z` by stage (variance by stage), and log Σ e^{F} over the top store
   against `log_Z_r`.
3. From any saved fit: `acc_gibbs_change` and `distinct_moved` by stage (they size R2's number of passes and
   distinct supports).
