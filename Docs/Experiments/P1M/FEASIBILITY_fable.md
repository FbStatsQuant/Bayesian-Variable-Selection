# FEASIBILITY — joint SMC-BVS at p = 10⁶ on NOTS (independent expert, Fable 5.2, 2026-11-15)

**Deliverable chosen: (1) A PLAN.** No binding obstruction was found. Verdict in the brief's terms: **FEASIBLE-IF**
(the conditions are three measurements, listed at the end of this opening section; none is a known blocker).

Scope read: the brief and its three addenda (final owner mandate), `HOLDS.md` (empty at 19:40 CST), the P1M
documents, W3-SCALE CP2 / DESIGN_v1 / `results/*.tsv`, the core (`Scripts/SMC_BVS/core/`). Benchmarks were run on
Owls in `/home/fb31/p1m_feas_bench/` (§4). **(measured)** marks a number from those runs; **(guess)** marks an
estimate that a gate must replace.

## 0. The answer

**The scheme ("V-1M").** The same target posterior on all p columns (no screening, no splitting), the same start law
family π₀, bridge γ_φ and labelled round (random-order Gibbs over all p labels + U + N_b + I), run as 16 independent
islands and merged. Changes from the theorem-covered method (v3.1 as coded), all of them:

| # | change | class | premises touched |
|---|---|---|---|
| 1 | fixed N per island (2,500; up to 10⁴ if the precision study asks) instead of max(2500, n, p) | Δ | T-N: TH01(e)(f)(i), TH06, TH08 |
| 2 | R′ = 16 process islands + merge (union stores; equal-weight RB PIP primary) | L per island | T-MERGE: O1, O10, O19–O21 |
| 3 | position-addressed counter-based uniforms | L | T-STREAM: EX-S, O5, O18 |
| 4 | **label-major batched kernel**, class-A arithmetic (bordered update, FMA, vector log/exp) | A | exact-arithmetic premise only |
| 5 | partition: complete linkage truncated at 1 − τ_n, minimum-index packing | Δ on π₀ | T-PART: START, START2, RM2, (V) |
| 6 | bounded calibration: pilot + at most 3 rebuilds, no escalation except construction failure | C | T-CAL: C-DLV, items reading E2 / tiers |
| 7 | **grid refinement**: every interval of the frozen grid split into m equal parts (default m = 4) | C | still a frozen schedule; items that use ρ_V ≥ 0.9 "as built" |
| 8 | **new estimators** next to the coded ones: log Z_𝒯 (deterministic lower bound), **log Ẑ_occ = log Z_A − log π̂(A)** (store sum over a model set A divided by the terminal particles' occupancy of A), PIP_𝒯 | additions | none for existing outputs; Ẑ_occ needs a particle-frequency statement (LT♯/TR type) |
| 9 | conditional, only if the 10⁴ precision study shows a gain: systematic resampling; more N-swap labels per round | Δ sampler | N1 holds for any unbiased resampling; LT♯/TR proofs to be checked |
| 10 | no score cache, no `fresh` counters, no leader stores in final islands | reporting | — |

**Precision targets at 10⁶** (checked per fit, never used to switch estimators):
- selection: 16 of 16 islands report the same best model; the merged HPM is certified by the final local search;
- PIP: sd over islands ≤ 0.005 for every variable (pooled s.e. ≤ 0.0013); max_j |PIP_eq − PIP_𝒯| ≤ 0.01 + (1 − π̂(𝒯));
- evidence: sd over islands of log Ẑ_occ,r ≤ 0.05 (expected 0.02–0.03, §2.2); the unbiased SMC log Ẑ within 3 s.e.
  of it; goal σ̂(log Ẑ_r) ≤ 0.5 after refinement (today 0.8–1.3), reported whatever it is.

**Cost per 1M fit (n = 200), billed core-h, from the measured kernel (§4) and a stated cost model (§1.1):**

| configuration | V-1M kernel (class A) | bit-form kernel | direct kernel (the plan) |
|---|---|---|---|
| baseline precision (N = 2,500, T ≈ 30) | 363 | 762 | 2,690 |
| **precise (T ≈ 120 on the final islands)** | **963** | 2,080 | 7,490 |
| precise + N = 10⁴ | 3,600 | — | — |

Wall time of one precise fit at the 1,536-CPU cap: about **2.2 h** (setup 0.3 h, calibration 0.9 h, 16 islands 0.6 h
in parallel, merge and tail 0.3 h). No job is longer than 2 h. Memory: 16 tasks × 32 GB = 512 GB of the 2,304 GB.
**Whole experiment: about 20.5k billed core-h with 25% contingency (26.6k with a 10⁵ theory-method overlap); limit 30k** (§3.3).

**Overlap-rung validation** (§3.2): 10 datasets at p = 10⁴, the theory's method and V-1M on the same data, two seeds
each; a 5k anchor with the existing, unmodified code; exact enumeration at p ≤ 25; optionally one dataset at 10⁵.

**What must be measured first** (each is cheap; none needs the full engine):
1. the kernel on one Sapphire Rapids node at 1, 24, 48, 96 threads (my numbers are from a loaded Skylake machine) — < 5 core-h;
2. accepted Gibbs moves and distinct supports per particle-round, from the stage tables of fits that already exist
   (`gibbs_change`, `distinct_moved`) — zero cost. They set the factor M of §1.1 (I use 3; expected 1.5);
3. where the dispersion of log Ẑ_r arises: per-stage variance of the log increments over 16–64 islands at 5k–10k
   (≈ 60 core-h, already planned) — it decides which of the precision levers of §2.2 are switched on.

---

## 1. Blocker (a): memory bandwidth of the Gram-free step — removed by the batched kernel (measured)

### 1.1 What was measured, and the cost model

The direct step reads one random column of X per elementary step (1.6 KB), 168 TB per island. A label-major pass
reads X **once, sequentially**, for a whole group of particles, and does everything else in cache:

1. copy a tile of 64–128 consecutive columns into row-major form;
2. for every column a of the group's active set A (union of the supports), form x_aᵀx_j for all j of the tile, by a
   sum that is sequential in the row index for each j (vectorised across labels, no FMA): **the same bits as the
   coded Gram entry**;
3. for every support S and every label j of the tile, compute log m(S ∪ {j}), the Gibbs odds, the particle's
   addressed uniform at the label's position in its round order, and the accept test.

Measured on Owls (8 threads, p = 10⁶, n = 200, AR(0.6), §4):

| quantity | value (measured) |
|---|---|
| direct Gram-free step, cached support, no ledger; bits equal to `v3::Scorer` (0 mismatches of 16,000) | 2,086 ns (1 thread), 2,664–2,705 ns (8 threads) |
| products, step 2 | 0.086–0.090 ns per multiply-add = 17–18 ns per label per active column; unchanged from \|A\| = 69 to 1,279 |
| score + odds + uniform, step 3, **bit form** (sorted-prefix reuse; scalar glibc log/exp); bits equal to `v3::Scorer` (0 of 4,096 at 10⁵ and at 10⁶) | 133–154 ns per score at k = 5–6; 220 ns at k = 8 |
| same arithmetic with vector log/exp (stand-in for a pinned vector log) | 81–89 ns at k = 6; 122 ns at k = 8 |
| step 3, **class A** (bordered update, FMA, vector log/exp; agrees to 10⁻⁹ relative, 0 of 4,096) | 27–33 ns per score, k = 5–8 |
| whole kernel per (support, label): class A | 42 (S₀ alone), 54–56 (S₀ + 1 null), 100 (k = 8), 121–128 (256 fully distinct supports) |
| whole kernel per (support, label): bit form | 163–187 (k = 5–6), 223 (256 distinct supports), 288 (k = 8) |
| round order (Fisher–Yates) + its inverse, per label | 8.8 ns single thread; 16–22 ns with 8 threads running |
| sequential read bandwidth | 5.9 / 10.6 / 20.3 / 38.1 GB/s at 1 / 2 / 4 / 8 threads |

Cost model per elementary step (thread time): **c = M · c_s + c_f**.
- c_s = kernel cost per (support, label). Planning values: 90 ns (class A), 210 ns (bit form).
- c_f = 30 ns: round order and inverse (measured 9–20) plus store offers (**not measured**; 10 is a guess).
- M = label sweeps per particle-round = 1 + accepted Gibbs moves per round, because a particle that moves needs the
  scores of its new support for the rest of the round. Measured on the benchmark data: Σ_{j ∉ S₀} o_j(S₀) = 1.02 at
  φ = 1, so about one addition and one deletion per round, **M ≈ 3** without sharing. Particles on the same support
  share step 3, which I expect to bring M to about 1.5 **(guess)**; no credit is taken for it.

So c = 300 ns (class A), 660 ns (bit form), against 2,400 ns for the direct step on the same machine: **8× and 3.6×**
at planning values, 15× if M = 1.5. The earlier review's "5–15× (guess)" stands; its 40–200 ns per score was right
for the kernel but left out M.

One island at 1M (N = 2,500, 42 rounds, 1.05·10¹¹ steps): 8.75 thread-h = **17.5 billed core-h** (class A); 38.5
(bit form); 140 (direct). X traffic of a precise island (132 rounds, groups of 256 particles, M = 3): about 3,960
passes × 1.6 GB = 6.3 TB in 0.57 h = **3 GB/s per socket**, against 528 TB for the direct step. Bandwidth no longer
binds.

### 1.2 Ranked kernel paths

| rank | path | gain at 1M | class | build cost | cheap test |
|---|---|---|---|---|---|
| 1 | **Label-major, class-A arithmetic, addressed uniforms** (recommended for 1M) | 8× (planning) to 15× over direct | A + L | 8–12 agent-days in WP3; the benchmark file is a working core of steps 1–3 | T3 hash invariance (threads, group, tile); class-A agreement with the bit form at 10⁴; the T8 exact reference |
| 2 | Label-major, bit form (bits of the v3 scorer), addressed uniforms | 3.6× to 7×; 5.6× with a pinned vector log | L only | + 3 agent-days (prefix-reuse kernel; pinned log is optional) | bit dump against `v3::Scorer`, as in §4 |
| 3 | Direct particle-major threads (the plan's baseline) | 1× | L | in the spec | — |
| 4 | Serial-stream, bit-identical to v3.1 (batched scores, serial commit in particle order) | ≈ 2× at 10⁴, wall-bound | B | 4 agent-days | PROD-H bit gates |

Path 2 is the right engine for the **theory's method on the overlap rung** (identical scores). Path 4 is worth
building only if the owner wants v3.1 bits beyond p = 5k.

Recommendation on build order: the spec builds particle-major first and label-major "if the prototype wins by 2×".
It wins by 3.6–8× measured; build label-major first and keep particle-major as its one-thread reference (T3).

Options the brief asked about, assessed and not recommended:
- **Low-precision or bit-packed X.** Halves traffic that is no longer the limit, and changes the arithmetic beyond
  class A. No.
- **Caching Gram blocks of candidate neighbourhoods; block sparsity of the neighbour graph.** A Gibbs round visits
  all p labels; almost every score involves a column outside any neighbourhood. The tile products of step 2 are the
  general form of this cache.
- **Sufficient statistics.** XᵀX is 8 TB. The only p-wide statistics that fit (z, diag G, singleton table entries)
  are already used.
- **Exact skipping of null labels by a bound.** It would change which models are offered to the stores, and step 3
  costs 27–150 ns anyway.

## 2. Blockers (b) and (c): evidence-weight degeneracy and calibration

### 2.1 What the numbers say about the cause (hypothesis, to be decided by measurement 3)

- Frozen grids are built for a restricted ESS share ≥ 0.9, yet the islands record minimum ESS shares of 0.31–0.54 at
  p ≥ 5k (`b3_census.tsv`).
- If the particles of a stage were independent draws, the variance of a log increment would be at most CV²/N. With
  the worst recorded share 0.31 (CV² = 2.2) that is sd ≤ 0.03 per stage and **≤ 0.16 over 30 stages**. Observed:
  0.76–1.35.
- So the particles are far from independent in the weight variable d(S): the effective number of independent
  particles per stage is about N/20 to N/70, i.e. 35–125. Two things produce that, and the code has both:
  multinomial resampling after **every** reweighting (`v3_engine.h:324`), which merges lineages even when the weights
  are nearly equal; and one round per stage, which redraws every single coordinate exactly but moves between
  alternative cores only through U and the B neighbour swaps.
- This matches the three observed signs: a right tail (an island whose few early lineages in the better core were
  amplified), no cure from 4× more particles on the same grid, and every island ending at the same best model.

I could not test this: the census records have no stage tables (REQUESTS R6). It is a hypothesis.

A fact about the target that matters here **(measured on one synthetic dataset)**: at p = 10⁶, n = 200 the posterior
is not concentrated on one model. Σ_{j ∉ S₀} o_j(S₀) = 1.02, so π(S₀ | data) is roughly 0.3–0.45 and the rest sits on
S₀ plus a few null columns. Every island must therefore estimate occupancies, not just find S₀.

### 2.2 Ranked precision levers

| rank | lever | expected gain | class / premises | build | cheap test |
|---|---|---|---|---|---|
| 1 | **Store/occupancy evidence** log Ẑ_occ = log Σ_{S∈A} e^{F(S)} − log π̂(A), A = the top-M models of the merged store (M = 1, 10, 100, 1,000 all reported), π̂(A) = share of terminal particles in A. Reported with log Z_𝒯 (certain lower bound) and the unbiased SMC log Ẑ | relative sd ≈ √((1 − π_A)/(π_A N)): **0.024 per island, 0.006 pooled** at π_A = 0.4, N = 2,500. Independent of the tempering noise | addition; consistent in N, not unbiased; needs terminal particles ≈ π, the premise the PIPs already use | 1 agent-day in the merge | p ≤ 25 against enumeration; 10⁴ against the theory method's Ẑ |
| 2 | **PIP_𝒯** on the merged store, with the bound 1 − π̂(𝒯) | no Monte Carlo noise; error ≤ mass outside the store | addition (DIST-C(i) marginal) | in the spec (OD-15) | same |
| 3 | **Grid refinement ×m** (m = 4) | variance of log Ẑ_r falls like 1/m if the path is quasi-static and up to 1/m² if it is lag-driven: σ̂ 1.0 → 0.25–0.5 **(guess)** | C | 0.5 agent-day | 64 islands at 10⁴, m ∈ {1, 4} |
| 4 | **Systematic resampling** | removes the lineage loss at near-equal weights; large if §2.1 is right | Δ sampler; N1 unaffected; LT♯/TR to check | 1 agent-day | same study, two arms |
| 5 | More particles (N = 10⁴) | 2× in σ̂ under independence; little at 5k in B3 | as change 1 | none | same study |
| 6 | More neighbour-swap labels per round | faster exchange between alternative cores | Δ kernel parameter | 0.5 agent-day | stage tables: lineage counts |
| 7 | More islands (R′ = 64) | s.e. of pooled quantities ∝ 1/√R′ only | L | none | — |

Not recommended:
- islands that target disjoint parts of the space, and islands that interact: neither reduces the variance of a
  tempered evidence at equal work, and both need new theory;
- a schedule adapted inside each final island: it breaks the frozen-𝒞 premise and the unbiasedness of Ẑ_r.

Pooling: keep equal-weight RB PIPs as primary and the union store for the HPM and PIP_𝒯; report PIP_Z with R_eff. Add
one check per fit: a homogeneity test of the islands' occupancy of the top-M models. If it fails, the fit is flagged.

**Is (b) a feasibility blocker? No.** No selection, PIP or distribution output uses the evidence weights. With levers
1–2 the evidence and the PIPs have estimators whose precision does not depend on σ̂(log Ẑ_r).

### 2.3 Calibration (c)

- Bounded rule (change 6): pilot + 3 rebuilds = 3 island-equivalents on the unrefined grid, sequential depth 4.
  At 1M: 52 billed core-h and about 0.9 h of wall time, of which up to 8 min per rebuild is the serial V re-scoring
  and grid build unless they are threaded (worth 1 agent-day).
- Refinement (change 7) costs nothing in calibration: it is applied to the frozen grid.
- I_max ∈ {0, 3} and m ∈ {1, 4} are fixed by the 10⁴ precision study before any 10⁵ run, then frozen.

## 3. The recommended path

### 3.1 Gates on the ladder

| gate | content | pass → go | fail → |
|---|---|---|---|
| **G0** (now) | measurements 1–2 of §0; store-offer cost added to the prototype | c ≤ 700 ns per step per thread at 10⁶ on SPR (then a precise fit ≤ 2,200 core-h) | 700–1,500 ns: 1M at baseline precision, 3 fits. > 1,500 ns: stop and report (direct-kernel regime, 2,700 per baseline fit) |
| **G-A** (enter 10⁴ science) | T3 invariance; T8 exact reference at p ≤ 25 for every Δ and C change and for Ẑ_occ; 5k anchor; the overlap comparison of §3.2; the precision study | every tolerance of §3.2 met; (N, m, resampling, I_max) frozen | the failing change is removed or repaired; nothing proceeds on a failed tolerance |
| **G-B** (enter 10⁵) | one 10⁵ pilot | cost ≤ 1.5× model (96 core-h precise); precision targets of §0 met; peak memory < request | re-size or stop |
| **G-C** (enter 10⁶) | 10⁵ rung complete (≥ 90%); forced-kill restart at 10⁵; T-PART answered; configuration, evaluator and competitor settings frozen by hash | 1M pilot submitted alone; kill rule: any island > 2× its model at 50% progress | return to HQ |
| **G-C2** | pilot complete and its targets met | remaining four fits + the doubling fit | — |

### 3.2 Overlap-rung validation design

"T" = the theory's method (every coded rule: N = max(2500, n, p), R = 4, coded calibration with escalation, exact
complete linkage, multinomial resampling). "V" = V-1M.

A constraint first: **T as coded cannot run at 10⁴ inside 24 h.** Its calibration is serial and, with the escalation
that R6 shows is certain at p ≥ 5k, a 10⁴ fit is about 300 island-units of 0.7 h. The existing code reaches 5k
(12.2 h measured). So:

| level | what runs | datasets | compared | cost (billed core-h) |
|---|---|---|---|---|
| exact | p ≤ 25, SMC branch forced, against enumeration (T8) | 20 fixtures × 400 islands | mean Ẑ_r/Z, Ẑ_occ/Z, PIPs within 3 s.e. | < 50 |
| **anchor, 5k** | T by the **existing unmodified code** (revision D) against T by the new engine (bit-form kernel, theory mode) and against V | 3 datasets; plus 20 seeds at 2k for a law test | as below; plus two-sample tests over seeds at 2k | ≈ 300 |
| **overlap, 10⁴** | T by the new engine in theory mode (same law, class L) and V, **2 seeds each** | 10: AR-strong × 4, AR-weak × 2, ADJ-OPP × 2, IND × 1, null × 1 | as below | T: 52–115 per fit → 1,040–2,300; V: 200 |
| overlap, 10⁵ (optional) | T in the new engine (N = 10⁵, H = 20,480, ℓ = 17, escalated) and V | 1 | as below | ≈ 6,100 |
| self-check, 10⁶ | V against V with N = 10⁴ on one dataset; island homogeneity; deterministic bounds | 1 | targets of §0 | 3,600 |

Comparisons and tolerances per dataset (the yardstick is the seed-to-seed difference inside T):
- **Selection.** HPM(V) = HPM(T) as sets. F is deterministic, so any difference names a winner; required: T never
  reports a model with higher F than V's, and equality in ≥ 9 of 10. MPM equal.
- **PIPs.** max_j |PIP_V − PIP_T| ≤ max(0.01, 3 combined s.e. from the island spread). Both within 0.01 + (1 − π̂(𝒯))
  of PIP_𝒯 on the union of the two stores.
- **Evidence.** |log Ẑ_V − log Ẑ_T| ≤ 3 combined s.e.; both ≥ log Z_𝒯(union) − 3 s.e.; |log Ẑ_occ,V − log Ẑ_occ,T| ≤ 0.05.
- **Distribution.** Hellinger distance of the store-BMA predictive of V to that of T ≤ 10% of T's distance to f*.

### 3.3 Budget (billed core-h; planning values M = 3, class-A kernel, Owls per-core speed)

| item | cost |
|---|---|
| gates, NOTS kernel benchmark, exact reference | 400 |
| 5k anchor | 300 |
| overlap at 10⁴ (upper value) | 2,500 |
| precision study at 10⁴: 64 islands × 2 datasets × 2 resampling rules × (N, m) ∈ {2,500, 10⁴} × {1, 4} | 950 |
| 10⁴ science (n-trend, designs, ablations, null, second seed; ≈ 150 fits) | 2,000 |
| 10⁵: 12 precise fits (96 each) + a 64-island precision check | 1,500 |
| **10⁶: 5 precise fits (963 each) + the N = 10⁴ doubling fit (3,600)** | **8,400** |
| competitors | 300 |
| **subtotal** | **16,350** |
| contingency 25% | 4,100 |
| **total** | **≈ 20,500** |
| option: theory method at 10⁵, one dataset | + 6,100 → ≈ 26,600 |

If G0 returns the expected M = 1.5, a precise 1M fit is about 545 and the subtotal falls by about 4k.
If the bit-form kernel were required at 1M, the 1M row becomes 5 × 2,080 = 10,400 and the option is dropped.

## 4. Measurements made

Machine: Owls, 2 × Xeon Gold 6148 (Skylake, 2.4 GHz, 20 cores per socket, L2 1 MB per core), shared: load average
19–23 during the runs. `nice -n 19`, at most 8 threads, peak memory about 4 GB, **0.16 core-hours in total**.
Expect ±20%. NOTS nodes are Sapphire Rapids; nothing here was measured there.

Build: `g++ -O3 -march=native -ffp-contract=off -fno-math-errno -fopenmp -std=c++17 -o feas_bench feas_bench.cpp -lmvec -lm`
(gcc 11.5). Reference for bit checks: `v3::Scorer::try_chol(S, from_X = true)` from a copy of the core headers.
Data: n = 200, AR(0.6) columns (restarted every 1,024 columns), standardised; 5 truths, β = (1, −0.8, 0.9, −0.7, 0.6).
Logs with every command and output line: `/home/fb31/p1m_feas_bench/run1.log`, `run2.log`.

| command (`feas_bench …`) | result |
|---|---|
| `bw 4 T`, T = 1, 2, 4, 8 (`OMP_PROC_BIND=spread`) | 5.9, 10.6, 20.3, 38.1 GB/s |
| `perm 1000000 5` | Fisher–Yates 5.22 ns per label, inverse 3.55 ns per label |
| `direct 100000 T 1000000 1`, T = 1, 8 | 2,236 and 2,107 ns per step; 0 bit mismatches of 1,999 and 15,999 |
| `direct 1000000 T 1000000 1`, T = 1, 8 | 2,086 and 2,705 ns per step; 0 of 2,000 and 16,000 |
| `direct 1000000 8 1000000 3` / `… 0` (k = 8 / 5) | 2,679 / 2,664 ns per step |
| `batch 1000000 8 64 1 0 v 128`, v = 0, 1, 2 | 187 / 112 / 56 ns per (support, label); products 0.079–0.095 ns per multiply-add |
| `CHECK=1 batch 1000000 1 64 1 0 v 128 0.25` | v = 0: 0 bit mismatches of 4,096; v = 1, 2: 0 of 4,096 beyond 10⁻⁹ relative |
| `batch 100000 8 64 1 0 v 128` | 179 / 117 / 59 ns; same check results at 10⁵ |
| `batch 1000000 8 256 0 1 v 128`, 256 distinct supports, \|A\| = 1,279 | v = 2: 121 ns; v = 0: 223 ns |
| `batch 1000000 8 256 0 1 2 64` (tile 64) | 128 ns |
| `batch 1000000 8 256 1 0 2 128` (S₀ + 1 null, \|A\| = 261) | 54 ns |
| `batch 1000000 8 64 3 0 v 128` (k = 8) | 288 / 189 / 100 ns |
| `batch 1000000 8 64 0 0 v 128` (S₀ alone) | v = 0: 163 ns; v = 2: 42 ns; Σ_j o_j(S₀) = 65.10 / 64 = 1.02 |

Not measured: store offers; the label sweeps M on real fits; anything on Sapphire Rapids; 48-thread scaling;
setup stages (the correlation pass at 0.09 ns per multiply-add would be 10¹⁴ × 0.09 ns = 2.5 thread-h).
The benchmark is not engine code: the composite term uses singleton table entries, the uniform is a SplitMix
stand-in, and labels inside a support take a scalar path.

## 5. Risks and questions for the owner

Risks, largest first:
1. **M and the store cost are unmeasured.** If M were 6 the precise fit is 1,800 core-h and five fits still fit; the
   G0 thresholds cover this.
2. **Sapphire Rapids may not match Owls per core** under 48 busy threads (frequency, L2 contention). Measurement 1.
3. **The cause of the evidence dispersion is a hypothesis.** If refinement and resampling do not bring σ̂ down, the
   SMC evidence at 1M stays imprecise (σ̂ ≈ 1); the precise evidence is then Ẑ_occ, which has no theorem yet.
4. **The theory's method is itself expensive on the overlap rung** (escalation is part of it). The 10⁵ overlap is
   6k core-h for one dataset; I list it as an option, not as part of the plan.
5. **Diffuse posterior at 1M, n = 200** (π(S₀ | data) ≈ 0.3–0.45 on my synthetic draw). PIPs of null columns up to
   about 0.1–0.2 are to be expected there; B3 recorded 0.03–0.12 at 2k–20k. The 1M claims should be worded with that in mind.
6. Sizes not re-derived by me: tables at n = 200 (2·10⁸ codes), the sparse partition, T and I at 10⁵–10⁶. I took the
   plan's values.

Questions:
- **Q1.** Is the class-A kernel acceptable at 1M (scores agree with the coded scorer to about 10⁻⁹ relative, not in
  bits), with the bit-form kernel used for the theory's method on the overlap rung? Bit form at 1M costs 2.2× more.
- **Q2.** May the headline evidence at 1M be log Ẑ_occ with its lower bound log Z_𝒯, the unbiased SMC log Ẑ and σ̂
  reported beside it?
- **Q3.** Do you want the 10⁵ overlap with the theory's method (≈ 6,100 core-h, one dataset), or is 10⁴ + the 5k
  anchor + the 1M self-check enough?
- **Q4.** May resampling and the number of swap labels change in V-1M if, and only if, the 10⁴ precision study
  shows a gain?
- **Q5.** The 5k anchor uses the existing code untouched. Is "bits at ≤ 5k, law at 10⁴" an acceptable meaning of
  "validated against the theorem-covered method"?
