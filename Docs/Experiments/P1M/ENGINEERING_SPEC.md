# ENGINEERING_SPEC v2 — large-p SMC-BVS engine ("v4") and the 1M variant V-1M

**Status: v2 DRAFT (EXP-CP1 v2), 2026-11-15.** SMC - Engineering Department. v2 adds §0-v2: the owner's scope change
(the 1M run is an engineered variant validated on an overlap rung) and the feasibility study (`FEASIBILITY_fable.md`,
`FEASIBILITY_disposition.md`). Where §0-v2 and §0–§7 disagree, **§0-v2 wins**.

**Sources.**
- Built from the independent skeleton `SPEC_SKELETON_fable.md` (Fable 5.2), adopted with the amendments in §0 and
  dispositioned in `REVIEW_disposition.md`.
- Supersedes `ENGINEERING_STRATEGY.md` v0.1.
- Reference engine: v3.1 / revision D (`Scripts/SMC_BVS/core/`).
- Sizes use n = 200, N = 2,500, R′ = 16, K = 100, B = 14 and a mean block size of 9 (measured on Owls, plan §6.1).
- **(guess)** marks an estimate that a gate must replace by a measurement.

## 0-v2. The 1M variant V-1M, the theory mode, and how they are validated (v2; supersedes §0.1–§0.3 where they conflict)

### 0-v2.1 Two configurations of one engine
- **Theory mode (T).** The theorem-covered method as coded: N = max(2500, n, p), R = 4, coded calibration with
  escalation, exact complete linkage, multinomial resampling, the v3 scorer's bits (bit-form kernel). It is run in two
  ways:
  - **compat** (serial v3.1 streams; bit-identical to revision D; gate T2) where it fits in 24 h, i.e. p ≤ 5k;
  - **law** (addressed streams, threaded, checkpointed) at 10⁴, and at 10⁵ if the owner buys that overlap.
- **V-1M (V).** The engineered variant for the 1M run. The changes from T are the complete list below. The paper presents
  V as an engineered variant validated against T (POLICIES §8).

### 0-v2.2 Complete list of changes V vs T (requirement (a))
| # | change | default in V | decided by | D |
|---|---|---|---|---|
| 1 | fixed N per island | 2,500 (N = 10⁴ arm in the precision study; one 1M doubling fit) | precision study | D-1 |
| 2 | R′ = 16 process islands + merge (union stores; equal-weight RB PIP primary) | 16 | — | D-6, D-11 |
| 3 | position-addressed counter-based uniforms | on | — | D-5 |
| 4 | **label-major batched kernel, class-A arithmetic** (bordered update, FMA, vector log/exp; ≈ 10⁻⁹ relative agreement with the coded scorer) | on | measured (F1) | D-15 |
| 5 | partition: complete linkage truncated at 1 − τ_n (τ_n = r_n, edges \|r\| ≥ τ_n), coded top-down cut, packing by minimum index | on | A3 paired comparison | D-4 |
| 6 | bounded calibration: pilot + at most I_max rebuilds, no escalation except construction failure | I_max ∈ {0, 3} | precision study | D-2 |
| 7 | grid refinement: every interval of the frozen grid split into m equal parts | m ∈ {1, 4} | precision study | D-12 |
| 8 | new estimators beside the coded ones: log Z_𝒯 (deterministic lower bound), **log Ẑ_occ** (store sum over the top-M models / terminal occupancy of them), PIP_𝒯 | on (additions) | T8 exact reference | D-8, D-13 |
| 9 | systematic resampling; more N-swap labels per round | off unless the precision study shows a gain | precision study | D-14 |
| 10 | no score cache, no `fresh`, no leader stores in final islands | on | — | D-3, D-7 |

### 0-v2.3 Precision targets at 10⁶ (reported per fit; never used to switch estimators)
- Selection: the same best model in 16 of 16 islands; the merged HPM certified by the final local search.
- PIP: sd over islands ≤ 0.005 for every variable; max_j |PIP_eq − PIP_𝒯| ≤ 0.01 + (1 − π̂(𝒯)).
- Evidence: sd over islands of log Ẑ_occ,r ≤ 0.05; the SMC log Ẑ within 3 s.e. of it; σ̂(log Ẑ_r) reported (goal ≤ 0.5).
- Island homogeneity of the top-M occupancies (flag only; invariant I7).

### 0-v2.4 Kernels and build order (replaces §0.2 item 1 and WP3)
- The **label-major kernel is built first**:
  1. tiles of 64–128 columns copied to row-major;
  2. products X_Aᵀx_j for the group's active set (sequential in i per label);
  3. per (support, label): score, odds, addressed uniform, accept.
- A particle that moves takes a new sweep for the rest of its round (factor M).
- Two arithmetic forms behind one interface:
  - **bit form** (sorted-prefix reuse, scalar libm): equals `v3::Scorer` in bits (measured: 0 mismatches of 4,096 at 10⁵
    and 10⁶). Used by **T**;
  - **class A**: used by **V**.
- Particle-major direct code is kept only as the one-thread reference of T3.
- Measured on Owls (FEASIBILITY §4, loaded Skylake, 8 threads):
  - direct step 2,100–2,700 ns;
  - per (support, label): 42–128 ns class A, 163–288 ns bit form.

  Planning cost per step c = M·c_s + c_f = 3·90 + 30 = 300 ns (class A); 660 ns (bit form).

### 0-v2.5 Cost (billed core-h, n = 200; planning values; gate G0 re-sizes them)
| fit | V (class A) | T in the new engine (bit form) |
|---|---|---|
| 10⁴ precise | ≈ 10 | 52–115 (coded calibration with escalation) |
| 10⁵ precise | ≈ 96 | ≈ 6,100 (one dataset, escalated) |
| 10⁶ baseline (T ≈ 30) / precise (T ≈ 120 on the final islands) | 363 / **963** | not run |
| 10⁶ precise, N = 10⁴ | 3,600 | — |

One precise 1M fit is ≈ 2.2 h of wall time at the 1,536-CPU cap; no job is longer than 2 h. Island tasks: 64 CPUs +
32 GB by default (NOTS_FACTS: free memory binds; 96 CPUs when available).

### 0-v2.6 Gates (replace plan §2.3 gates)
| gate | content | pass → |
|---|---|---|
| **G0** (now; HQ batch ≤ 5 core-h + ≈ 60) | kernel on one SPR node at 1/24/48/96 threads incl. store offers; M from P6 stage tables; per-stage increment variance over 16–64 islands at 5k–10k (stage-level records) | c ≤ 700 ns → precise plan; 700–1,500 → baseline precision, 3 fits at 1M; > 1,500 → stop and report |
| **G-A** | T3 invariance; T8 exact reference for every Δ/C change and Ẑ_occ; the 5k anchor; the 10⁴ overlap within tolerance; the precision study freezes (N, m, resampling, I_max) | 10⁴ science, then 10⁵ |
| **G-B** | one 10⁵ pilot ≤ 1.5× model, precision targets met, memory < request | 10⁵ rung |
| **G-C** | 10⁵ ≥ 90% complete; forced-kill restart at 10⁵; configuration, evaluator and competitors frozen by hash | the 1M pilot alone; kill rule 2× model at 50% |
| **G-C2** | pilot meets the targets | remaining 1M fits + the N = 10⁴ doubling fit |

### 0-v2.7 Overlap-rung validation (requirement (b))
| level | runs | datasets | cost |
|---|---|---|---|
| exact | p ≤ 25, SMC branch forced, against enumeration: Ẑ_r/Z, Ẑ_occ/Z, PIPs within 3 s.e. | 20 fixtures × 400 islands | < 50 |
| anchor 5k | T by the **existing unmodified code** (revision D) vs T in the new engine (bit form, compat) vs V; plus a 20-seed law test at 2k | 3 | ≈ 300 |
| overlap 10⁴ | T (new engine, law mode) vs V, 2 seeds each | 10: AR-strong 4, AR-weak 2, ADJ-OPP 2, IND 1, null 1 | 1,040–2,500 |
| overlap 10⁵ (owner option) | T vs V | 1 | ≈ 6,100 |
| 1M self-check | V vs V(N = 10⁴); island homogeneity; deterministic bounds | 1 | 3,600 |

Tolerances, per dataset (the yardstick is T's own seed-to-seed spread):
- HPM(V) = HPM(T) as sets in ≥ 9 of 10 datasets, and T never reports a model with a higher F than V's; MPM equal.
- max_j |PIP_V − PIP_T| ≤ max(0.01, 3 combined s.e.).
- |log Ẑ_V − log Ẑ_T| ≤ 3 combined s.e., and |log Ẑ_occ,V − log Ẑ_occ,T| ≤ 0.05.
- The Hellinger distance between the store-BMA predictives of V and T is ≤ 10% of T's distance to f*.

### 0-v2.8 Budget (planning; FEASIBILITY §3.3)
Gates and benchmarks 400 · 5k anchor 300 · overlap 10⁴ 2,500 · precision study 950 · 10⁴ science 2,000 · 10⁵ 1,500 ·
**10⁶: 5 precise fits + the doubling fit 8,400** · competitors 300 → subtotal 16,350; **total ≈ 20.5k with 25%
contingency**. The 10⁵ T overlap (option) adds 6,100, giving ≈ 26.6k. The owner chooses (owner sheet).

---

## 0. Amendments, decisions assumed, and build plan (Engineering manager)

### 0.1 Decisions this spec assumes (pending with the owner; OWNER_DECISIONS v0.2)
| OD | assumption here | if decided otherwise |
|---|---|---|
| OD-1 | fixed N = 2,500 per island | 1M is infeasible; the spec stops at 10⁵ |
| OD-2 | bounded calibration: I_max (default 3), no escalation except construction failure | the coded rule runs in compat mode only; production cost ×4 |
| OD-3 | B2-3: `logical` counts published; no `fresh` in production | production must keep a serial cache path; OD-8 benefits shrink |
| OD-5 | complete linkage truncated at 1 − τ_n, τ_n = r_n | the 1M rung cannot run |
| OD-8 | position-addressed counter-based uniforms (production) | particle-serial streams: the same class, but fewer execution freedoms |
| OD-13 | top store 40p + 1 kept; leader stores only in calibration | +2 GB and +minutes per ledger at 1M |
| OD-15 | PIP_𝒯, log Z_𝒯, `law.bin`, terminal supports returned or archived | `eval` computes them outside the fit |
| OD-16 | label-major kernel optional, behind gate T5 | production stays particle-major |

### 0.2 Amendments to the skeleton
1. **Two production kernels, one output.**
   - The particle-major kernel (one thread per particle group, the direct Gram-free scorer with per-particle sorted-prefix
     reuse) is built **first**.
   - The label-major kernel (skeleton §3) is an optional drop-in, built only if the Owls prototype (OD-16) beats
     particle-major by ≥ 2× at p = 10⁵.
   - Position addressing makes both produce identical bytes (T3), so swapping kernels never changes a result.
2. **Planning cost** (§7) is the direct kernel at c = 2 µs per step (pessimistic, measured at 10k), with the bounded
   calibration. Label-major numbers stay **(guess)** and enter no budget.
3. **Calibration in production**: I_max = 3 unless the three-arm comparison at 10⁴ (plan A2, ≈ 300 core-h) says
   otherwise. Diagnostic islands run as 4 threads-groups of one process, so the rebuild ledger merge happens in memory.
4. **Memory request**: 32 GB per island task (skeleton §2); 96 CPUs (one socket) unless T5 shows earlier saturation.
5. **Theory hand-off**: §4.2 is the premise table for SMC-Theory (tickets T-N, T-PART, T-STREAM, T-CAL, T-MERGE).

### 0.3 Work packages (HQ approves; builders per OD-11)
| WP | content | spec § | gates | size (agent-days) | owner |
|---|---|---|---|---|---|
| WP1 | binary skeleton, file formats, manifests, `gen`, `prep`, compat-mode scorer and kernels from the v3 headers, pinned libm + rebuilt reference | 1, 2, 4.1 | T1, T2 | 8 | SCALE A |
| WP2 | `setup`: correlation tiles, neighbour graph, truncated linkage, tables (sorted-prefix DFS), table top stores, iterative `start_mode` | 1, 5 | T1, T11 | 7 | SCALE B |
| WP3 | production island: addressed uniforms, particle-major threads, flat stores, per-thread ledgers, RB chunked reduction, checkpoints | 3, 6 | T3, T4, T6 | 9 | SCALE A |
| WP4 | `calibrate` (bounded rule + compat rule), `merge` + tail (threaded scans), statuses | 3, 6 | T8, T9, T10 | 7 | SCALE B |
| WP5 | `eval` (selection, PIP, DIST closed forms, cost), `post` (`law.bin`), Slurm driver with pipelining, competitor harness | 1, 7 | T7 | 8 | ENG (this dept) |
| WP6 | Owls micro-benchmarks: bandwidth curve and direct step at 10⁵–10⁶; label-major prototype (OD-16) | 7 | T5 | 3 | ENG |
| WP7 | NOTS gates (≈ 150 core-h + ≈ 20 task-h reference rebuild), Sol code review | all | T1–T11 | 3 | SCALE + ENG; HQ submits or delegates |

Total ≈ 45 agent-days, 3–4 calendar weeks with three builders. The Minimal tier is the stated expectation for December
(REVIEW §4.8).

---

Preservation classes: **B** same bits as the reference; **A** same exact-arithmetic map, rounding differs;
**L** same law under ideal streams; **C** changes only the frozen calibration; **Δ** changes the law.

Two execution modes of one binary:
- **compat**: v3.1 stream layout (one serial stream per island, `v3_util.h:47-51`), one thread, v3.1 rules for N, R′ = 4,
  partition and calibration. Must reproduce the reference bit for bit.
- **production**: position-addressed uniforms, fixed N, R′ from the manifest, sparse partition, bounded calibration.

---

## 1. Components and interfaces

All files: little-endian; a fixed header (magic, format version, mode, section table with offset, length and SHA-256
per section); arrays 64-byte aligned; written to a temporary name and renamed. Every job has a JSON manifest that
names its inputs by hash, the binary hash, the compiler flags and the pinned math-library hash. A job refuses to start
on a hash mismatch.

| # | command | inputs | outputs | notes |
|---|---|---|---|---|
| 0 | `gen` | design id, p, n, data seed | `raw.bin` (X column-major f64, y), `truth.json` (S₀, β*, σ*, Σ parameters) | one sequential recursion over columns for AR; the same definition gives test rows for any column subset. Not kept: regenerated and checked by hash |
| 1 | `prep` | `raw.bin` (or R-standardised X in compat gates) | `data.bin`: Xs (n × p f64, column-major), ys, z = Xsᵀys, diag(G), column statistics, kept-column map, drop list | copies the arithmetic of `v3_preprocess.R:35-51` (R's two-pass long-double mean) or is declared class A |
| 2 | `setup` | `data.bin` | `setup.bin`: neighbour lists (CSR), duplicate components, cut-group record, blocks, `blk`/`pos`, block tables (`logr`), sampler tables, log Zbar₀, start mode, **table top stores** (top-c of all table models under each of the three store orders) | correlations by streamed tiles; nothing p × p is stored |
| 3 | `calibrate` | `data.bin`, `setup.bin`, seed | `calib.bin`: frozen grid, tier, N, L, triggers by tier and iteration, every grid built, stage records of pilot and diagnostic islands, calibration stores (flat, with stored F, log γ₀, d), HPM with event key, logical counters, stream addresses used | the only sequential stage |
| 4 | `island --id r` | `data.bin`, `setup.bin`, `calib.bin` (grid, N, L, tier only) | `island_r.bin`: stage table, log increments, log Ẑ_r, `rb_acc`, `rb_round` (4 × p), `pip_r`, top store (flat, sorted), HPM with event key, `island_best`, logical counters, status, timings; optional terminal supports; `island_r.ckpt.{a,b}` | an island never reads another island's files. Its ledger starts empty (no table or inherited models) |
| 5 | `merge` | manifest of R′ islands, `calib.bin`, `setup.bin`, `data.bin` | `fit.bin` + `fit.json`: merged top store, HPM and provenance, `hpm_before_local`, final local search, start mode, LS0, near ties, flags, log Ẑ, PIPs (equal-weight, evidence-weighted, store-renormalised), diagnostics | runs only when every manifest island is present and valid; then the tail exactly as `v3_core.cpp:453-481` |
| 6 | `eval` (EXP) | `fit.bin`, `truth.json`, columns of ∪S | per-fit record (flat table row + arrays) | selection, PIP, DIST objects, cost |
| 7 | `post` (option) | `fit.bin`, columns of the store's leading models | `law.bin`: store-BMA law (models, weights, conjugate parameters); draws on request from streams disjoint from 0…9 + R′ | never touches engine outputs |

Interfaces inside the engine (C++; one implementation each, shared by both modes):

| interface | contract |
|---|---|
| `score(S)` → log m(S) | bits of `v3_score.h:176-224` on the Cholesky route for a sorted S; Gram entries by the sequential sum of `v3_score.h:45-53`. Fallback routes unchanged |
| `flip_scores(S, labels)` → log m(S △ j) for many j | each entry equal in bits to `score(S △ j)`. Implemented by prefix reuse: rows before the sorted insertion position are shared, later rows are recomputed in the same order; labels between two members of S share one code path |
| `comp(S)` | ordered block sum of `v3_start.h:54-66` |
| `uniform(address)` | production: counter-based generator, address = (seed, island or calibration role, phase, stage or round, particle, position in the round, slot). compat: the next value of the island's xoshiro256** stream |
| `Store` | top-c of everything offered under a strict total order (`v3_ledger.h:35-42`); content independent of offer order; flat arrays (score, offset, length, hash) + integer pool |
| `Ledger.merge(a, b)` | stores by top-c of the union; HPM by `hpm_better` (`v3_util.h:121-126`); provenance = smallest event key (role, island, stage, round, particle, position); `island_best` by maximum; logical counters by sum |

Decisions the skeleton assumed (see §0.1 for the spec's list): OD-1 fixed N; OD-3 = B2-3 (logical counts published; no `fresh`);
OD-8(b) with position addressing; bounded calibration (REVIEW R1); truncated-linkage partition (REVIEW R3).

## 2. Data layout and memory budget

Per process, n = 200. "Shared" = file-backed, read-only, one copy per node. For other n: X scales with n; tables are
about 10× larger at n ≥ 256 (B = 16).

| component | layout | p = 10⁴ | p = 10⁵ | p = 10⁶ | status |
|---|---|---|---|---|---|
| Xs | f64, column-major, shared | 16 MB | 160 MB | 1.6 GB | exact |
| z, diag(G), column statistics, maps | 6 arrays of p | 0.5 MB | 5 MB | 48 MB | exact |
| neighbour lists | CSR, int32; ≤ 2B per column after symmetrising | ≤ 1.2 MB | ≤ 12 MB | ≤ 120 MB | bound for typical designs; hubs can exceed it |
| partition | `blk`, `pos` int32 | 0.1 MB | 0.8 MB | 8 MB | exact |
| tables `logr` | f64 per code; 210 codes per column (measured, plan §6.1) | 17 MB | 170 MB | 1.7 GB | measured count |
| sampler tables | `sub_cum` f64 + `codes_by_size` u32 per code; `cond_cum` ≈ 8 KB per block; `logF` (J + 1)(K + 1) f64 | 35 MB | 350 MB | 3.5 GB | **(guess ±30%)** |
| `logm_tab`, `route_tab` | per code; setup only, dropped after the table top stores are built | 25 MB | 250 MB | 2.5 GB transient | exact per code |
| **setup total, persistent, shared** | | **70 MB** | **0.7 GB** | **≈ 7 GB** | |
| setup transient: correlation tiles | 2,048 × 2,048 f64 per thread, 96 threads | 3.2 GB | 3.2 GB | 3.2 GB | choice |
| setup transient: top-B heaps and edge list | 12 B × (pB + edges) | 2 MB | 20 MB | 0.2–0.5 GB | **(guess)** |
| particles | sparse supports + (log m, log γ₀, d, F, hash); two populations | < 1 MB | < 1 MB | < 1 MB | v3.1 uses p/8 bytes per particle: 0.6 GB at 1M |
| RB arrays | `rb_acc`, 4 × `rb_round`, `pip` | 0.5 MB | 5 MB | 48 MB | exact |
| top store, island (ONE per island; INTERFACES v0.1.2) | c = 40p + 1 entries; MEASURED (WP1, Owls, k = 7): 68.5 B per kept entry, 136 B per cap entry at peak (staging merge ≈ 2.25c) | 27–54 MB | 0.27–0.54 GB | **2.7 GB kept, ≈ 5.4 GB peak (worst case)** | measured at c = 4·10⁶ (517 MB peak), scaled |
| per-thread offer buffers | 65,536 entries × ≈ 70 B per thread | 4.6 MB/thread | same | ≈ 0.4 GB at 96 threads | WP1 default |
| leader stores | 2 × 20p × ≈ 56 B; calibration only | 22 MB | 0.22 GB | 2.2 GB | final islands: none |
| label-major working set | round orders (u32 × p per particle, groups of G = 256 particles), gathered X_A, products for a block of 4,096 labels, odds for the distinct supports | 0.1 GB | 0.3 GB | 1.5–3 GB | **(guess)**; G is a free parameter, not part of the law |
| score cache | none in production; ≤ 64 MB per thread if a memo is kept | 0 | 0 | 0 | OD-3 |
| **island task, private** | | **0.2 GB** | **1 GB** | **5–9 GB** | |
| **island task, request (`--mem`)** | private + shared pages + margin | 2 GB | 4 GB | **32 GB** | plan note says 20 GB |
| calibrate | ledger with three stores + V arrays (2 f64 per V member) | 0.2 GB | 1.2 GB | 9–12 GB private; request 32 GB | |
| merge | streaming R′-way merge, O(c) memory | 0.1 GB | 0.5 GB | 5 GB; request 16 GB | |
| scratch per fit, before cleanup | R′ island files + calibration + setup | 0.6 GB | 6 GB | ≈ 50 GB | 16 × 2.3 GB + 5 GB + 7 GB |
| archive per fit | `fit.bin` with the full merged store | 30 MB | 0.3 GB | 2.3 GB | or the top 10⁶ models + dropped mass: 60 MB |

Rules:
- Nothing of size p² exists at any time. Nothing of size N × p exists except the round orders of one particle group.
- No R objects, no per-model heap allocations, no `std::set` in stores.
- All p-wide outputs are binary arrays; `fit.json` holds scalars and hashes only.

## 3. Parallel decomposition and communication

| level | unit | how many at 1M | communication | determinism |
|---|---|---|---|---|
| fit pipeline | Slurm jobs chained by `afterok`: setup → calibrate → islands (array) → merge → eval | 1 + 1 + 16 + 1 + 1 tasks | files on /scratch only | manifests with hashes |
| replicates | independent pipelines | up to the 1,536-CPU cap | none | — |
| islands | one process per island, one socket (48 cores) each; two per node | 16 | **none** between islands | island r depends only on (data, setup, frozen grid, seed, r) |
| calibration rebuild | 4 diagnostic islands as threads of one process, or as 4 tasks with a ledger merge | I_max + 1 sequential rounds | ledger merge between rounds | by `Ledger.merge` (order-free) |
| inside an island, per round | (a) draw the round orders, threads over particles; (b) pass q: threads over label blocks × distinct supports; (c) each particle finds its first accepted move from its own addressed uniforms; (d) particles that moved form pass q + 1 | passes per round ≈ 1 + the largest number of accepted moves of one particle **(guess 4–8)** | shared read-only X, tables; per-thread ledgers | by uniform addresses: the result does not depend on thread count, block size, G or pass structure |
| stage barrier | weights, log-sum-exp, ESS, multinomial resampling: serial in particle order (`v3_engine.h:316-327`) | O(N) | — | unchanged arithmetic |
| setup | tiles of the correlation pass; blocks for tables | threads | none | fixed tile order for the per-column top-B selection; canonical sums |
| merge and tail | R′-way store merge (serial stream); local-search scans threaded over labels with a max-reduction that keeps the tie rule (`v3_engine.h:392`) | 1 task | — | reduction order fixed |

Rules for the label-major round (production):
1. Uniform addresses are fixed by the algorithm's control flow before the value is read. A Gibbs label uses slot 0 of
   its position; U, N_b and I use slots 0… of their positions (`v3_run.R:25-37` gives the order within a step).
2. Scores computed for a support at labels the particle did not visit while on that support are **discarded**: they
   are not offered to the stores, not counted, and do not touch `island_best`. Events are recorded at consumption.
3. RB accumulation: `rb_acc[j]` receives the odds at the state the particle held when it visited j, summed over
   particles in a declared order (particle order within chunks of 64, chunks in order). Class A against compat.
4. With one group and one thread the same code is the particle-serial reference of production mode.

Request shape: island task = 96 CPUs (one socket) unless gate T5 shows the direct scorer saturates earlier; then
request the saturating count. Hyperthreads are not assumed to help.

## 4. Output-preservation contract

### 4.1 Compat mode against v3.1 / revision D

| output | class | test |
|---|---|---|
| every field of the fit fingerprint (version 2, `scripts/bitid_compare.R`): log Ẑ, log Ẑ_r, PIPs, RB arrays, MPM, HPM and provenance, snapshots, top store, near ties, stage and terminal tables, flags, logical counts, stream positions | **B** | T2: PROD-H 24 + supplementary 10 + setup objects at 5k/10k/20k, fail-closed |
| setup objects (blocks, tables, neighbours, start, start mode, duplicate components, cut group) | **B** | T1: 50-case unit harness + setup hashes |
| leader stores | **B** | T2 (they are returned outputs, `v3_run.R:210`) |
| `fresh` counts, cache statistics, numerical-route counters | may differ (OD-3) | named in the comparison's exclusion list; nothing else is excluded |
| timings, memory, preflight record | may differ | — |
| admission decisions (preflight) | may differ; compared separately | as CP2 §1 |

If the math library is pinned, the reference is v3.1 rebuilt against the same routines; old and new reference records
are compared once and the result recorded (expected identical or class A).

### 4.2 Production mode: each change, its class, and what must be re-checked

| change | class | theorem premises to re-check | test |
|---|---|---|---|
| position-addressed counter streams | **L** | O5 (ideal-stream premise EX-S for the new generator), O18 (independence across the enlarged address map), variate-order documentation | T4; T3 |
| label-major execution, threads, groups | none beyond the row above: **B** against production's particle-serial reference | — | T3 |
| RB reduction in chunks | **A** against compat | exact-arithmetic premise only | T3 (thread invariance); T4 covers the law |
| fixed N per island (OD-1) | **Δ** | T-N: TH01(e)(f)(i), TH06, TH08 for general (N, R′); confirm RM-0, LT♯, TR, D need nothing | T8 |
| R′ ≠ 4, islands as processes, merge | **L** for per-island outputs; pooled outputs are new functions of them | O1 (merge), O10 (union stores), O19 (lower bound), O20 (flags at R′ ≠ 4), O21 (card items on the merged HPM) | T9: at R′ = 4 with v3.1's N, merge output = serial output, class B except counters |
| partition by truncated complete linkage | **Δ** on π₀ | T-PART: START, START2, RM2, (V) | T8; A3 paired comparison |
| bounded calibration, no escalation except construction failure | **C** | C-DLV; card items reading E2 or `grid_unconverged` | T8; A-rung three-arm comparison |
| table and inherited models offered at the merge, not per island | **B** for stores and HPM (order-free); `island_best` unaffected (island 0 events) | — | T9 |
| leader stores absent from final islands | reporting change | owner | — |
| new outputs (PIP_𝒯, log Z_𝒯, terminal supports, `law.bin`) | additions; **B** for existing outputs | W3-DIST for what may be claimed | T7 |

### 4.3 What must hold in every mode

- The same (data, seed, binary, mode, manifest) gives the same bytes on any node of the pinned type, for any thread
  count, and after any restart.
- No estimate field is produced unless every manifest island and the tail completed (GUARD-W; `v3_run.R:106-116`).
- R′ and N are fixed in the manifest before any final address is read. No final quantity triggers a rerun or changes them.

## 5. Invariants and test gates

Invariants checked at run time (cheap; a violation is `internal_error`, never a silent continue):
- I1. Every store is the top-c of what was offered; no duplicates; sorted under its comparator.
- I2. log Z_𝒯 ≤ log Ẑ + a declared margin is **not** asserted (Ẑ is noisy); it is recorded. What is asserted: HPM F ≥ every
  store F; F(HPM) recomputed by `score` equals the stored value.
- I3. Per stage: weights finite, ESS in [1, N], grid strictly increasing from 0 to 1.
- I4. Logical counts per round equal the number of executed steps (N × (p + B + 2) minus recorded self-loops).
- I5. Each uniform address is used at most once (debug builds: address log on small cases).
- I6. Every scanned centre of a local search has a complete scan or the search is marked incomplete.

Gates (each with a declared threshold, written before the run):

| gate | content | pass criterion |
|---|---|---|
| T1 kernels | scorer, flip scores, tables, start, steps, resampling, grid construction against the v3 headers | byte-identical dumps: the 50 cases + new cases at p ≥ 10⁵ + flip scores at every insertion position, k = 0…K |
| T2 compat | §4.1 | 34 of 34 units IDENTICAL; setup hashes identical |
| T3 execution invariance | production: 1, 8, 48, 96 threads; G ∈ {1, 64, 256, N}; label block ∈ {64, 4,096}; label-major against particle-serial | identical output hash in every configuration |
| T4 law | compat against production, 200 seeds at p ≤ 1k, three designs | declared two-sample tests on log Ẑ, PIPs, HPM frequency, T, ESS; Bonferroni level fixed beforehand |
| T5 scale and bandwidth | Owls or one NOTS node: random column reads per second with 1, 12, 24, 48, 96 threads; step cost of the direct scorer and of the label-major kernel at p = 10⁵ and 10⁶ (setup + one stage) | numbers recorded; they set the request shape and the budget. Decision gate for the label-major build |
| T6 restart | forced kill at a random stage at 10⁵; resume | byte-identical `island_r.bin` |
| T7 evaluator | closed-form Hellinger against brute-force Monte Carlo, 20 fixtures | 3 significant digits (plan G-A) |
| T8 exact reference | p ≤ 25, SMC branch forced, each Δ and C change on: 400 islands | mean Ẑ_r / Z within 3 standard errors of 1; PIPs within 3 standard errors of the enumeration branch |
| T9 merge equivalence | R′ = 4, v3.1 N: process islands + merge against the serial run | class B on everything but counters and timings |
| T10 failure paths | missing island, corrupt file, hash mismatch, numerical failure in an island, in the tail | the declared status; no estimate field |
| T11 sparse partition | truncated linkage against the exact dendrogram cut at 1 − τ_n, p ≤ 20k, AR, BLK, IND, tie cases | identical clusters |

Entry to rung A needs T1–T4, T7–T11. Entry to 10⁵ needs T5. Entry to 10⁶ needs T6 and a 10⁵ fit within 1.5× of §7.

## 6. Failure modes, checkpoint/restart, statuses

Checkpoint (island and calibration):
- At a stage boundary, at most every 10 min of wall time: stage index, particles (supports and scores), cumulative
  log Ẑ, stage records so far, RB accumulators (measured rounds only), ledger, counters. Production mode stores no
  generator state (addresses are recomputed). Compat mode stores the stream state and position.
- Two generations, written atomically with a checksum. A restart loads the newest valid one.
- The top store dominates the size (2.2 GB at 1M): write it as a base file plus the entries added since the last
  checkpoint **(guess: needed only if a full write exceeds 30 s)**.

| failure | detection | action | fit status |
|---|---|---|---|
| wall-time limit or preemption of an island | Slurm signal; missing final file | resubmit the same island id; resume from checkpoint; result identical (T6) | unaffected |
| node failure | missing file after the job ends | same | unaffected |
| island killed by memory | Slurm state | resubmit once with the declared larger request; then stop | `resource_limit` if it repeats |
| input hash mismatch | at job start | job refuses; pipeline stops | `invalid_input` |
| numerical failure in a score | exception (`v3_util.h:26-28`) | deterministic: no retry | `numerical_failure`; HPM so far labelled incomplete; no estimates |
| calibration construction failure | grid result not ok | tier-1 fallback grid as coded (`v3_calib.R:122-124`) | `completed`, flag `grid_fallback` |
| calibration unconverged at I_max | rebuild count | freeze the last grid; flag | `completed`, flag `grid_unconverged` |
| missing or invalid island at merge | manifest check | merge refuses; never pools a subset | `incomplete` until resubmitted; `resource_limit` after the retry budget |
| failure in the tail (local search, LS0) | status of the tail | no output (GUARD-W) | `resource_limit` or `numerical_failure` |
| scratch purge or quota | missing inputs | regenerate data and setup from seeds (hash-checked); islands rerun | unaffected if hashes match |
| stack or recursion limits | — | removed by design: `start_mode` enumeration is iterative (reference: `v3_start.h:281-301`) | — |

Statuses: task level {`completed`, `resource_limit`, `numerical_failure`, `invalid_input`, `io_error`,
`internal_error`}; fit level takes the first that applies in the order `invalid_input`, `internal_error`,
`numerical_failure`, `resource_limit`, `io_error`, `completed`. Retry budget per task: 2. Budgets are per task and
per fit (one runtime guard cannot span processes); both are in the manifest. Every submitted fit is logged, completed
or not.

## 7. Performance targets per stage

n = 200, one Sapphire Rapids socket (48 cores) per task unless stated. "Direct" = the plan's Gram-free scorer with
per-particle threads; "label-major" = REVIEW R2. Island steps = N(p + 16)(T + L + 4) with T = 30, L = 8.
All label-major numbers and all 10⁵–10⁶ numbers are **(guess)** until gate T5.

| stage | p = 10⁴ | p = 10⁵ | p = 10⁶ | basis |
|---|---|---|---|---|
| gen + prep | 1 s | 10 s | 2 min | sequential generation; standardisation threaded |
| setup: correlation pass (n p²/2 multiply-adds) | 1 s | 10 s | 10–20 min | 10¹⁰ / 10¹² / 10¹⁴; plan §5 gives the same range |
| setup: partition, tables (≈ 210 codes per column), start, mode | 1 s | 5 s | 0.5–2 min | revision D: tables 0.07–0.11 s at 10k–20k, serial (`leg_b_setup_compare_roundD.tsv`); block Grams and the size convolution added |
| island, direct, thread-hours | 0.3–0.6 | 3–6 | 30–60 | 0.9–1.8 µs measured to 20k (CP1 §1.2); bandwidth floor 0.4–0.8 µs at 1M |
| island, label-major, thread-hours | 0.05–0.1 | 0.4–0.8 | 3–8 | 40–200 ns per score, ≈ 1,500 distinct supports per round |
| island wall on one socket | 1–2 min | 5–10 min | direct 0.7–1.5 h; label-major 5–15 min | |
| calibration, coded rule (I = ℓ = 14 / 17 / 20) | 8–12 island-equivalents | 9–14 | 10.5–16.5 | B3: 0.5–0.8 per rebuild |
| calibration, bounded (I_max = 3) | 2–3 island-equivalents | 2–3 | 2–3 | REVIEW R1 |
| calibration serial part per rebuild (V scores + grid build) | < 1 s | 5–40 s | 1–8 min unless threaded with a fixed blocked sum (class C) | 1–10 µs per V member, `profile_v31_stages.tsv` |
| merge of 16 stores | 5 s | 30 s | 3–5 min | 6.4·10⁸ entries streamed |
| tail: one scan = p + k(p − k) scores | < 1 s | 1 s | 5–20 s | 6·10⁶ scores at k = 5, one pass over X |
| eval | 1 min | 2 min | 5 min | closed forms; columns of ∪S only |
| **fit, billed core-h, PLANNING** (direct, c = 2 µs, bounded calibration, R′ = 16) | 27 | 272 | 2,720 | adopted for budgets (OWNER_DECISIONS OD-7 v0.2) |
| **fit, billed core-h** (R′ = 16), skeleton ranges | plan 38; direct + bounded calibration ≈ 12–25; label-major + bounded ≈ 2–4 | 377; ≈ 120–250; ≈ 15–30 | 3,770; ≈ 1,200–2,400; **≈ 110–300** | billed = 2 × thread-hours; bounded calibration = 19 island-equivalents |
| **fit, wall time** at the 1,536-CPU cap | < 15 min | < 1 h | direct ≈ 3–4 h; label-major ≈ 1 h | calibration depth 4 rounds |

Acceptance for the 1M pilot: measured core-h within 1.5× of the row adopted at G-C; peak resident memory under the
§2 request; T3 hash check repeated on the pilot's first stage with two thread counts.
