# SCALING_DESIGN_v0 — SMC-BVS at p = 10⁴ – 10⁶ on NOTS (design only)

**Status:** PLAN ONLY. Nothing here has been built, changed or launched. No production file, configuration, branch or
commit was touched. Author: design sub-agent, 2026-11-10.
**Scope:** re-engineering of SMC-BVS v3.1 (production core `Scripts/SMC_BVS/core/`, method spec
`Theory_work/State_of_Project/sections/02_method.tex`) so that it runs where sequential BVS breaks (p = 10k, 100k,
ideally 1M) on the NOTS Slurm cluster, with many islands (100s–1000s) as the parallel unit.
**Evidence used:** a full read of the production C++ headers and R drivers; the method spec; Song & Liang (2015, JRSSB)
§3 and §6 (`Papers/Core_bibliography/32_*.pdf`); local micro-benchmarks at p ≤ 5,000 (about 1.5 CPU-minutes,
`Theory_work/Pause_2026-11/scaling_scratch/`, results in `RESULTS_2026-11-10.txt`, harness `bench.cpp`).

### Tags used throughout

| tag | meaning | what must be re-checked |
|---|---|---|
| **[OP-bit]** | output-preserving, bit for bit: same (X, y, seed, binary) gives the same output bits as v3.1 (diagnostic counters and timings may differ; each such case is named) | nothing; a bitwise regression test |
| **[OP-law]** | same law of every output in exact arithmetic (premise EX-A), but different floating-point bits or different random-number consumption | the bitwise claims (Prop W, "deterministic function of the model" in the stores), the variate-order documentation; the theorems that rest on EX-A/EX-S stand |
| **[Δ𝒞]** | changes only how the frozen calibration 𝒞 is computed | none of the "given any frozen 𝒞" results; Theorem G if the grid rule changes; delivery statistics |
| **[Δlaw]** | target unchanged, but the sampler's law changes (budgets, kernel, start π₀, island layout) | the named theorem premises (Section 4) |
| **[Δtarget]** | the posterior that is reported changes (e.g. screening) | the target theory itself |
| **UNVERIFIED** | not checked by me (not run, not read, or extrapolated beyond p = 5,000) | — |

Notation: n samples, p predictors, K = min(p, ⌊n/2⌋), B = min(⌊√n⌋, ⌊√p⌋, 16), J ≈ blocks (measured
J ≈ 0.105 p at B = 14), k = |S| of a typical model, N particles per island (now N_e = 4^e·max(2500, n, p)),
H ≈ 0.2 N calibration particles, T bridge stages (ceiling T_e), L = max(4, ⌈log₂(n+1)⌉) burn-in rounds, Hm = 4 measured
rounds, R (= R′) final islands, ℓ = ⌈log₂(n+p+1)⌉, m = p + B + 2 steps per round, W = ⌈p/64⌉ bitset words,
c = 40p + 1 top-store capacity, I = rebuild iterations actually used.
Worked numbers use n = 200 (K = 100, B = 14, L = 8) and **T = 30 (UNVERIFIED: I found no recorded typical stage count;
the code ceiling is T₀ = 1000)**, so one island does T + L + Hm = 42 population rounds.

---

## 0. Executive summary

1. **Four walls, in the order they are hit at n = 200** (by code reading and extrapolation of local timings):
   - **The v3.1 default preflight refuses fits from p ≈ 2,300** at the default 24 h allocation, before any work. The
     LS0 worst-case time charge uses a scan size p + p²/4 (`v3_fit.R:44`) and the time of a size-K score; at
     p = 2,500 this projects about 30 h (Section 1.3). This is a delivery rule only (Lemma RO), so fixing it is
     output-preserving on the output event. UNVERIFIED by execution.
   - **O(p²) memory of the setup**: the Gram (`v3_score.h:44-53`), the correlation copy and the distance matrix
     (`v3_blocks.h:12,54`) are alive together: 24p² bytes, about 2.4 GB at p = 10k, 240 GB at 100k, 24 TB at 1M. The
     preflight memory model reproduces this and stops at p ≈ 18.8k at 8 GiB (`02_method.tex:658`, settings row 44).
   - **Θ(N·p) elementary steps per population round with N ≥ p**: each island does
     N(T+L+4)(p+B+2) steps; at a measured 3 µs per step this is about 3.5 CPU-h per island at p = 10k, about
     350 CPU-h at 100k and about 4 CPU-years at 1M. With N tied to p, no amount of island parallelism fixes 1M.
   - **Per-step O(p) overheads that are invisible at p ≤ 5,000**: every elementary step copies the whole particle,
     including a p-bit bitset (`v3_engine.h:120,131,152,172,185`); the cost grows like 8W bytes per step and
     overtakes scoring around p ≈ 200k (extrapolated). Score cache (500p entries; about 51 GB at 1M), stores held as
     `std::set` of vectors (about 10 GB at 1M), block tables (32 B per subset code; about 55 GB at 1M) and the R-side
     copies (tables, stores, `pip_r`, `rb`) scale the same way.
2. **Most of the speed can be had bit for bit.** Measured locally with the production headers and production compiler
   flags (0 mismatches in every check):
   - block tables by DFS with a bordered (prefix-reused) Cholesky: **5–8× faster, bitwise identical**;
   - Gram entries by lane-parallel sequential sums: **1.5–3.5× faster, bitwise identical** (AVX2 build included);
   - Gram-free scoring from X columns gives **identical bits** to the Gram route; so an O(np)-memory canonical scorer
     is possible without changing outputs;
   - neighbour graph by partial selection instead of a full stable sort: **8–14× faster, identical**.
3. **The parallel unit is the island**, as the owner wants. Islands share one setup and one frozen 𝒞, run on disjoint
   streams with no communication, write one record each, and are merged once: Ẑ pooled, PIPs evidence-weighted
   (the v3.1 *specified* primary; the production code still ships the equal-weight mean, `v3_run.R:162`), the HPM and
   the top store taken from the union of all scored models (Lemma S), then one parallel final local search and LS0.
4. **1M needs one method decision**: decoupling the per-island particle count from p (N_isl fixed, e.g.
   max(2500, n), and R′ large). This reverses the v3.1 ruling "N_e is never split" (C8, `02_method.tex:377,390`), so it
   is [Δlaw] and opens theory obligations (Section 4: O3, O4). With it and the [OP-bit]/[OP-law] engineering, a
   p = 1M fit is about 15 CPU-h per island (target per-step cost 0.5 µs, UNVERIFIED) and about 4,000 CPU-h for
   R′ = 256: roughly 8 h of wall time on 500 cores.
5. **The open statistical risk is weight degeneracy of the Ẑ_r across islands at high p.** The design makes it
   measurable before final randomness (an *island census* inside calibration, Section 3.4.3) and declares fallbacks
   that never select estimates from final outputs.

---

## 1. Component inventory

### 1.1 Measured constants (local i7-6700, GCC 14.3, production flags, one thread)

| quantity | value | source |
|---|---|---|
| Gram entry (sequential mult-add over n) | ≈ 1.1 ns per (i, pair) | `gram` runs, p = 1k–4k |
| score via stored Gram, k = 1/5/10/20/50/100 | 0.43 / 1.1 / 3.1 / 7.0 / 67 / 375 µs | `score` run, p = 5,000 |
| table score (production `build_tables`) | 1.0–1.6 µs | `tables` |
| table score (DFS bordered Cholesky) | 0.18–0.19 µs | `tables` |
| elementary step inside a real island (k ≈ 10) | 3.1–3.9 µs, cache hit rate 0.33–0.47 | `engine`, p = 1k–4k |
| flip eval, cache miss / hit | 2.8–4.3 / 0.24–0.32 µs | `engine` micro |
| complete linkage | 0.04 / 0.24 / 1.15 s at p = 1k / 2k / 4k (≈ p^2.3) | `setup` |
| neighbour graph (stable sort) / partial selection | 2.7 s / 0.19 s at p = 4k | `setup` |

NOTS per-core speed relative to this PC is UNVERIFIED; the extrapolations below use these constants unchanged.

### 1.2 Inventory: complexity and pointers

Time is single-thread unless stated. "Mem" is peak resident bytes of that component.

| # | component | where | time | memory | notes |
|---|---|---|---|---|---|
| C1 | preprocessing (R): constant check, per-column standardisation | `v3_preprocess.R:97-132` (`apply` at 111, R loop 118-122) | Θ(np) plus p R-level calls | 3–4 copies of n×p doubles (X, `storage.mode` copy, Xs) | R overhead per column; at p = 1M about 10⁶ closures. |
| C2 | context: Gram, z, constants | `v3_score.h:39-72` (Gram loop 45-53); `v3_core.cpp:91-106` | Θ(np²/2), scalar, no BLAS | 8p² (Gram) + 8np (copy of X in `Data`) | the Θ(p²) storage wall. |
| C3 | duplicate components, cut_group | `v3_core.cpp:746-760`, `794-819` | Θ(p²) passes over the Gram | O(p) + Gram | needs the Gram. |
| C4 | correlation + complete linkage + cut + packing | `v3_blocks.h:10-17`, `46-108`, `124-144` | Θ(p²) typical, O(p³) worst (`recompute_row` cascades); measured ≈ p^2.3 | r (8p²) and dist (8p²) alive together, plus Gram | `make_blocks` calls `complete_linkage`, which builds its own correlation matrix. |
| C5 | neighbour graph | `v3_blocks.h:149-173` (stable_sort at 160) | Θ(p² log p) | another correlation matrix 8p² + O(pB) | rebuilt from scratch; full sort only to keep ≤ B. |
| C6 | block tables (scores of all 2^B subsets of each block) | `v3_start.h:76-98` | J·2^B scores, each Θ(B³) | 32 B per code in C++ (`logr`, `logm_tab`, `route_tab`, `codes_by_size`, `sub_cum`) + ≈ 24 B per code in the R copy (`v3_core.cpp:306-312`) | ≈ 1,720 p scores at B = 14. |
| C7 | start: profiles, convolution, sampler tables, Z̄₀ | `v3_start.h:101-151` | Θ(J·K·B) + Θ(J·2^B) | `cond_cum` 8·J(K+1)(B+1), `logF` 8·J(K+1) | small except `cond_cum` at large K. |
| C8 | start mode, tie DP | `v3_start.h:195-305` | Θ(J·K·B) DP; tie DP Θ(p·J·K·B) worst | O(JK) | p·J·K·B ≈ 10¹⁵ at 1M if the tie DP fires (rare: 0/2,400 in the study). |
| C9 | exact draw from π₀ | `v3_start.h:158-176` | Θ(K + J + k log k) per draw (upper_bound per block) | — | once per particle at init + once per independence step. |
| C10 | score (Cholesky of H and A, Q, fallbacks) | `v3_score.h:139-247` (`gram_sub` 163-173, `try_chol` 176-188) | Θ(k³) flops + k² random Gram reads + 4 heap allocations | O(k²) scratch | k² Gram reads miss cache at large p. |
| C11 | score cache | `v3_score.h:255-294`, capacity 500p (`v3_run.R:92`, `v3_calib.R:147`) | O(k) per lookup | 29 B × 2^⌈log₂(1000p)⌉ slots + 4k B per entry | does not affect outputs (a hit returns the same bits). |
| C12 | elementary steps, round | `v3_engine.h:113-214` | per step: one eval (C10/C11) + particle copy Θ(k + W) + `comp` Θ(k log k); per round: m − 1 uniforms + a p-int permutation | particle = sorted S + W-word bitset | `tmpQ = P` at 120, 152, 172, 185; `P = tmpQ` on acceptance. |
| C13 | one island: init, T stages (reweight, LSE, resample, round), L burn-in, Hm measured | `v3_engine.h:274-368` | Θ(N·(T+L+Hm)·m) steps; resampling Θ(N·(k+W)) per stage | 2N particles; RB p-vector + Hm·p `rb_round` | `before = rb_acc` copies p doubles per measured round (353). |
| C14 | ledger: HPM, top store (c = 40p+1), leaders (20p, 20p), counters | `v3_ledger.h:43-113` (`init` at 76-80) | O(log c · k) per fresh offer | ≈ 120 B per entry as `std::set<TopEntry>` → ≈ 9.6 KB × p | a full ledger per process. |
| C15 | final run driver: 4 islands **in sequence**, then local search, LS0 | `v3_core.cpp:391-518` (loop 443-452, streams 9 + r at 444) | sum of islands | one cache, one ledger | serial loop; the process-worker layer of v3.1 (MD04) is not in this tree. |
| C16 | local search (centre frozen; flips then swaps) | `v3_engine.h:379-419` | (p + k(p−k)) evals per scan × (moves + 1) scans; ≤ ℓ + 1 scans | O(scans·k) archive | every scanned model is a score event. |
| C17 | LS0 (start mode → local search) | `v3_core.cpp:465-481` | C8 + C16 with cap ℓ + \|S̃₀\| | — | preflight charges its worst case (C21). |
| C18 | calibration: pilot, ≤ ℓ rebuilds × 4 diagnostic islands (serial loop), local search per iteration | `v3_core.cpp:623-698` (loop 666-682), `v3_calib.R:28-137` | ≈ (1 + 4I)·(H/N) final-island equivalents per tier | one ledger, one cache | the rebuild loop is sequential depth. |
| C19 | candidate set V and grid construction | `v3_core.cpp:703-724`; `v3_calib.h:49-98` | rescoring \|V\| ≤ 40p+1 models; grid ≈ 3·61·T·\|V\| `exp` in long double per construction (upper bound), ≤ ℓ + 1 constructions per tier | `std::set<vector<int>>` of \|V\| models | `F_V(u)` is recomputed for every bisection step at fixed u. |
| C20 | exact branch (enumeration) | `v3_core.cpp:524-568` | Σ_{k≤K} C(p,k) scores | top store | small p only; DFS in increasing index order (benefits from the C6 trick). |
| C21 | preflight | `v3_fit.R:26-68` (SMC memory 36-41, LS0 worst case 43-48) | one size-K timing | — | delivery only (Lemma RO). |
| C22 | R assembly and R-side objects | `v3_run.R:119-220`, `v3_core.cpp:327-371` | O(R·p) + list conversions of 80p models | `pip_r` p×R, `rb` (Hm+1)·p·R, stores as 80p R vectors, tables as J R lists | the R boundary converts every stored model to an R vector. |
| C23 | compile and load | `v3.R:22-71` | once per process | — | a lock-protected shared cache; fine for array jobs. |

### 1.3 Which components dominate (current code, n = 200, tier 0, R = 4, one core per island)

Times extrapolate the local constants; memory follows the code. **All entries beyond p = 5,000 are UNVERIFIED
extrapolations.**

| component | p = 1k | p = 10k | p = 100k | p = 1M |
|---|---|---|---|---|
| C2 Gram time / memory | 0.1 s / 8 MB | 11 s / 0.8 GB | 18 min / 80 GB | 31 h / 8 TB |
| C2+C4+C5 setup peak memory (24p²) | 24 MB | 2.4 GB | 240 GB | 24 TB |
| C4 complete linkage | 0.04 s | ≈ 9 s | ≈ 30 min | ≈ 4 days (worst case O(p³)) |
| C5 neighbour graph | 0.1 s | ≈ 19 s | ≈ 40 min | ≈ 80 h |
| C6 tables time / C++ memory | 2 s / 55 MB | 19 s / 0.55 GB | 3 min / 5.5 GB | 32 min / 55 GB |
| N = N₀ | 2,500 | 10,000 | 100,000 | 1,000,000 |
| C13 one island, rounds (3 µs/step) | 5 min | 3.5 h | ≈ 350 h | ≈ 4 years |
| C12 particle copy per step (8W bytes at ≈ 10 GB/s) | 0.04 µs | 0.13 µs | 1.3 µs | 12.5 µs |
| C11 cache memory (k ≈ 10) | 50 MB | 0.7 GB | 6 GB | 51 GB |
| C14 stores memory (one ledger) | 10 MB | 0.1 GB | 1 GB | 10 GB |
| C16 one local-search scan (k = 10, 3 µs) | 0.03 s | 0.3 s | 3.3 s | 33 s |
| C19 one grid construction (\|V\| = 40p, T = 30, upper bound) | 2 s | 22 s | 4 min | 37 min (× ≤ ℓ+1 per tier) |
| C21 preflight verdict at 24 h | runs | **refused (LS0 worst case)** | refused | refused |
| **dominant** | particle rounds | particle rounds; preflight refusal | setup memory, then rounds | everything; rounds are 4 CPU-years per island |

How the C21 row was derived (UNVERIFIED by execution): with LS0 on by default, `ls0_wc` is TRUE (`v3_fit.R:114`) and
the charge is 2 × (ℓ + K + 1) × (p + p²/4) × s_K (`v3_fit.R:44,47`), with s_K the measured time of one size-K score
(≈ 300–375 µs at K = 100 locally). At p = 2,000 this is ≈ 19 h; at p = 2,500 ≈ 30 h > 24 h, so the fit returns
`resource_limit`. The method's own bound on a scan is p + k*(p − k*) with k* = min(K, ⌊p/2⌋)
(`02_method.tex:412-413`), much smaller than p²/4 when K ≪ p.

Per-island step counts (N·(T+L+Hm)·m, T = 30): 1.1·10⁸ (1k), 4.2·10⁹ (10k), 4.2·10¹¹ (100k), 4.2·10¹³ (1M).
Calibration adds about (1 + 4I)·0.2 final-island equivalents per tier (≈ 2.6 at I = 3; 0.0512 + 0.2048·I relative to
the 4 final islands, `02_method.tex:409-412`); escalation to tier 1 multiplies N by 4 and allows 4× the stages.

---

## 2. Per-component efficiency ideas

Ordered by component. Every idea carries a tag; "measured" means verified locally (Appendix A).

### 2.1 Scoring (C10) — the inner loop

| idea | tag | expected effect | notes |
|---|---|---|---|
| S1. Remove heap traffic from `score`: preallocated per-thread scratch for `Gs`, `bufH`, `bufA`, `LH` (now `assign`, a local `std::vector`, and the copy `LH = bufH`, `v3_score.h:165,178-179,185`) | [OP-bit] | 1.5–3× at k ≤ 20 (UNVERIFIED) | same arithmetic, same order. |
| S2. **Canonical Gram-free columns**: G entries computed on demand by the same sequential sum as `data_init`; removes the 8p² Gram | [OP-bit] — **measured: 0 mismatches for k = 1…100** | removes the O(p²) wall; per-entry cost ≈ n mult-adds instead of one cache-missing read | multiplication commutes in IEEE, and the summation order over i is unchanged, so the bits match (`gram`, `score` runs). |
| S3. **Lane-parallel canonical dot products**: compute the k entries G_{jS} together, one SIMD lane per member, each lane summing over i in order | [OP-bit] — **measured on the Gram: 0 mismatches**, 1.5× (SSE2) to 3.5× (AVX2) | makes S2 cheap: k·n/4 vector ops per flip | needs X row-major tiles or a packed X_S per particle; `-ffp-contract=off` must stay. |
| S4. **Prefix-reused canonical Cholesky**: the factor of a sorted model's leading rows depends only on those rows, in the same operation order (`chol_inplace`, `v3_score.h:76-90`; forward solve, running sums of log diag and of w²). For an addition at sorted position q, rows < q are reused and rows ≥ q recomputed; a deletion likewise. Appending the largest index costs O(k²) | [OP-bit] — **measured for appends (tables): 0 mismatches** | ≈ 2–3× fewer flops on average for Gibbs flips; O(k²) instead of O(k³) for appends (tables, exact branch, local-search additions above max S) | requires a per-particle cache of the current model's canonical factors (O(k²) doubles per particle). Fallback routes (refactor, QR, Q recompute) call the full scorer. |
| S5. Schur-complement (rank-one) delta scores: log m(S ∪ j) − log m(S) from G_{jS}, H_S⁻¹-solves, in O(k² + kn) | [OP-law] | 5–10× at k ≈ 10–50 (UNVERIFIED) | different rounding from the canonical route, so a model's F would depend on the path. Use only behind S6. |
| S6. **Filter-then-canonical**: use S5 (fast) values plus a numerical margin to decide (i) Gibbs/MH outcomes and (ii) store/HPM entry; compute the canonical score only when the uniform falls inside the margin, the model may enter a store or the HPM, or the model becomes a particle state | [OP-bit] **conditional on a numerical premise NUM-MARGIN (O7)**; otherwise [OP-law] | most flips need no canonical score | needs a rigorous bound on \|fast − canonical\|; the current η is heuristic (`v3_score.h:242-246`, `02_method.tex:654`). |
| S7. Reorder X for locality: store X column-major for single columns and row-major tiles for lane kernels; float64 only | [OP-bit] | memory bandwidth | float32 X would be [OP-law] at best (it changes scores), so it is not recommended. |

### 2.2 Gram and sufficient statistics (C2, C3)

- G1. **Drop the dense Gram** in favour of S2/S3 for scoring and of streamed correlation *tiles* for the structures
  (C3–C5). [OP-bit]. Memory goes from 8p² to O(np) for X plus O(pB + edges) for the structures.
- G2. **Canonical tiles, parallel**: tile (a-range × b-range) jobs computing the same sequential sums with lane-parallel
  kernels; deterministic results whatever the tile schedule. [OP-bit]. 1M: ≈ 10¹⁴ mult-adds ≈ 8 core-hours at the
  measured AVX2 rate (UNVERIFIED on NOTS) → minutes on 256 cores.
- G3. **BLAS filter + canonical verify** (when canonical tiles are too slow): dgemm tiles to find candidate pairs with
  \|r\| near a threshold or a top-B boundary, then canonical recomputation of the candidates only. [OP-bit] provided the
  filter margin exceeds the dgemm error bound (≈ n·ε·‖x_a‖‖x_b‖, a standard bound; use a generous multiple).
- G4. `z = Xᵀy`, `yᵀy` computed once with the same order. [OP-bit].
- G5. Duplicate components and cut_group become streaming threshold passes over tiles with union-find (partition is
  order-independent). [OP-bit].

### 2.3 Blocks, neighbour graph (C4, C5)

- B1. **Neighbour graph by partial selection** (`nth_element` + sort of the top `keep` under the same total order
  "|r| desc, index asc"); threshold count by one pass. [OP-bit] — **measured: identical, 8–14× faster**. Streaming
  version over tiles: per-column top-B heaps; O(pB) memory.
- B2. **Exact complete linkage with less memory**: build only the condensed distance (p(p−1)/2 doubles: 0.4 GB at 10k,
  40 GB at 100k) directly from canonical tiles; do not hold G and r alongside. [OP-bit]. Feasible to ≈ 100k–150k on a
  large-memory node (NOTS node sizes UNVERIFIED); impossible at 1M (4 TB).
- B3. Faster exact linkage (declared v3.2 item C11): nearest-neighbour-chain is O(p²) for complete linkage, but with
  the R13 lexicographic tie order it is only guaranteed to match the greedy order when the composite order is
  reducible. [OP-bit] **if** that equivalence is proved (O16). UNVERIFIED.
- B4. **Sparse exact-below-threshold partition** for p ≥ p_CL (≈ 150k): threshold graph E_τ = {|r| ≥ τ} from tiles;
  connected components; exact complete linkage inside each component; a deterministic order of the retained clusters;
  next-fit packing as now. All merges of the exact dendrogram below height 1 − τ involve only pairs in E_τ, so every
  cluster formed below 1 − τ is reproduced exactly; only the grouping and packing of clusters joined above 1 − τ
  (weak, |r| < τ, mostly noise correlation) changes. [Δlaw] (π₀ changes). Validity results hold for any deterministic
  X-measurable partition; partition theorems need re-checking (O8). A natural τ is the method's own r_n = √(2 log p / n)
  (0.37 at n = 200, p = 1M).
- B5. Packing order and `subtree_leaves` need no change.

### 2.4 Block tables and the start (C6–C9)

- T1. **DFS table scoring with a bordered Cholesky** (S4 applied to the code tree: children add positions above the
  current maximum, so each new subset appends one row). [OP-bit] — **measured: 0 mismatches over 7.6·10⁵ table
  scores, 5–8× faster**. At 1M: 1.7·10⁹ scores × 0.18 µs ≈ 5 core-minutes.
- T2. **Tables computed once** by the setup job, in parallel over blocks (MD04 (h)), written once, memory-mapped
  read-only by every island process on a node. [OP-bit].
- T3. **Lean table memory**: the island engine needs `logr` (8 B per code) for `comp`, and the within-size law for
  `draw_pi0`. `codes_by_size` can be generated by combinatorial unranking; `sub_cum[b][j]` can be rebuilt on demand from
  `logr` with the same `cumulative_from_logs` (only for blocks with k_b > 0 in a draw); `logm_tab`/`route_tab` are needed
  only once, for table ingestion in the merge. [OP-bit]. Memory: 32 B → 8 B per code (1M, B = 14: 55 GB → 14 GB per
  node; B = 16 when n ≥ 256: 34 GB per node).
- T4. Do not return tables to R at large p (`v3_core.cpp:306-312`); return a file handle and a hash. [OP-bit] for
  estimates; a reporting-object change.
- T5. Start mode tie DP (C8): its worst case Θ(p·J·K·B) is reached only under ties; keep the enumeration fast path; if
  ever needed, the feasibility check can be made incremental per block. [OP-bit]. Low priority.

### 2.5 SMC stages, particles, moves (C9, C12, C13)

- P1. **No bitset in the particle**: membership by binary search in the sorted S (k ≤ K), `nth_nonmember` by walking S,
  `distinct` by Zobrist hash plus S. Flips **in place with undo** instead of `tmpQ = P` / `P = tmpQ`. [OP-bit]. Removes
  the Θ(W) per-step term (12.5 µs per step at 1M, extrapolated).
- P2. **Per-particle canonical factor cache** (S4) so that a flip reuses the current state's factor. [OP-bit].
- P3. Incremental `comp`: only the flipped block's code changes, but the block sum is ordered, so recompute the
  ordered sum over the k blocks met (as now) without the sort (keep the blocks met in a sorted small array). [OP-bit].
- P4. **Per-particle counter-based streams** (declared v3.2 item C6): Philox/Threefry keyed by (seed, stream) with
  counter (particle, stage, round, slot). Enables particle-parallel moves inside an island with output independent of
  the thread count. [OP-law] (random consumption changes). Obligation O5.
- P5. Fixed-chunk deterministic reductions for the RB accumulators (`rb_acc[j] += o_j`, `v3_engine.h:128`) — or exact
  (fixed-point/binned) accumulation — so the PIP bits do not depend on the thread count. [OP-law] versus v3 bits;
  deterministic per binary.
- P6. Resampling, ESS, log-increment stay serial in particle order (they are O(N)). [OP-bit] given P4.
- P7. `draw_order`: reuse the permutation buffer; one allocation per thread. [OP-bit].
- P8. **Lazy measured-round bookkeeping**: `before = rb_acc` and the per-round `diff` (`v3_engine.h:353,357`) are
  O(p) per round, fine; but `rb_round` (Hm×p per island) and `rb_acc` should be written to the island record, not kept
  in the R fit (C22). [OP-bit] for estimates.
- P9. *(law-changing options for 1M, Phase 4 only)* (a) **N decoupled from p** (N_isl fixed, R′ large) [Δlaw];
  (b) **Metropolised coordinate updates with cheap screening proposals during bridge and burn-in, exact Gibbs in the 4
  measured rounds** (keeps the RB-PIP record exact; each step reversible) [Δlaw]; (c) informed/screened swap proposals
  with correct Hastings ratios [Δlaw]; (d) random-subset sweeps (a uniformly chosen subset of labels per round, random
  order) [Δlaw]. A rigorous *exact skip* of Gibbs coordinates by score bounds was examined and rejected: a bound tight
  enough to skip null coordinates needs \|P_S x_j\|², i.e. the same k dot products as the exact score.

### 2.6 Calibration (C18, C19)

- K1. Cache F_V(u) during the bisection at fixed u (it is recomputed for every halving; `v3_calib.h:55-58,81-85`);
  compute F_V(mid) and F_V(2·mid − u) in one pass over V. [OP-bit]. Saves about one third to one half of the `exp`
  calls.
- K2. **Absorption skip in `lse_cal`**: in round-to-nearest long-double accumulation, a term below half an ulp of the
  running sum leaves the sum unchanged; skip its `exp`. [OP-bit] given a short lemma on the x87 precision mode actually
  in force (64-bit on Linux; UNVERIFIED for the NOTS build). Large saving when V is dominated by a few models.
- K3. Keep V in C++ (no R list of 40p models, `v3_core.cpp:711-723`); flat pool storage. [OP-bit] for 𝒞.
- K4. Run the 4 diagnostic islands concurrently (MD04 (b); W-cal not yet executed, `02_method.tex:396`), each
  particle-parallel (P4). [OP-bit] for (b) by code reading; [OP-law] with P4.
- K5. Parallel tree reductions for F_V. [Δ𝒞] (changes rounding of the grid construction); validity "given any frozen
  𝒞" unaffected.
- K6. Cap |V| at huge p (e.g. min(40p + 1, V_max)). [Δ𝒞]. Only if K1–K3 are not enough.

### 2.7 Local searches (C16, C17)

- L1. **Parallel scan with a max-reduction** that keeps the tie rule (largest F, then plain lexicographic order;
  MD04 (c)). [OP-bit]. The scan is embarrassingly parallel: p flips + k(p − k) swaps.
- L2. Scan scoring by S4 (prefix reuse from the frozen centre: additions above max S are O(k²) appends) and S6 for
  swaps. [OP-bit] (S4) / conditional [OP-bit] (S6).
- L3. Prune the store/HPM offers by a rigorous upper bound only for counters; every scanned model must still count as
  scored. Note: the ledger "logical/fresh" counters are diagnostics; changing them is a reporting change.
- L4. **Preflight fix** (C21): charge LS0 with the method's bound p + k*(p − k*) and the parallel, incremental scan cost,
  or rely on the stop-only guard. Delivery only (Lemma RO); estimates on the output event unchanged.

### 2.8 Ledger, stores, cache (C11, C14)

- D1. **Flat top-c stores**: models in an int pool, entries (F, offset, size, hash) in a vector; when it holds 2c
  entries, `nth_element` + truncate to c under the strict total order. The final content is top_c of everything offered
  (Lemma S), identical to `std::set`. [OP-bit]. ≈ 56 B per entry at k = 10 instead of ≈ 120 B.
- D2. **Cache capped by bytes, not by 500p** (e.g. 1–2 GB per worker), and optionally shared lock-free inside an island.
  [OP-bit] for estimates and stores (a hit returns the same bits; stores are idempotent and order-independent); the
  reported cache counters and "fresh" counts change.
- D3. Final-run leader stores (γ₀, γ₁) are used only to build V in calibration; in final islands they are reporting
  only (`v3_run.R:210`). Dropping them from final islands is a reporting change. UNVERIFIED: whether any card reads the
  final-run leaders.
- D4. HPM provenance under concurrency: define it as the minimum event key (island, phase order, stage, round,
  particle, position) among events that scored the HPM model; this equals the serial "first score" rule and is
  independent of thread interleaving. [OP-bit] for serial-equivalent provenance.

### 2.9 Memory layout, R overhead, I/O (C1, C22, C23)

- M1. Preprocessing in C++ with R's arithmetic (R's `mean` is a two-pass long-double mean; `sum` accumulates in long
  double). [OP-bit] if replicated exactly; UNVERIFIED until tested against `v3_preprocess.R`.
- M2. **One X per node**: a memory-mapped read-only file (1.6 GB at n = 200, p = 1M). [OP-bit].
- M3. Huge-p pipeline as C++ executables with binary records; R only for the final assembly of small objects (no
  per-model R vectors, no p×R matrices in the fit object). [OP-bit] for estimates.
- M4. Keep the pinned build (`Makevars.v3:6`, `-ffp-contract=off -march=x86-64-v2`). An AVX2 build kept bitwise
  equality for the lane Gram locally; whether all NOTS node types support AVX2, and whether glibc's runtime-selected
  `exp`/`log` variants are identical across node types, is UNVERIFIED and matters for every bitwise claim.

---

## 3. Parallel architecture

### 3.1 Pipeline on Slurm

```
J0  build (once)        one binary, pinned flags; hash recorded
J1  setup (1 node, t threads)
      preprocess -> canonical tiles -> dup/cut_group/neighbour graph/blocks -> tables (DFS, parallel) -> start
      writes setup.bin (+ sha256); X.bin (mmap)
J2  calibration (1 node, or 1 + 4 nodes)
      pilot island (particle-parallel) -> V -> grid -> [4 diagnostic islands concurrently -> local search -> V -> grid]*
      -> triggers -> (escalation) -> island census (3.4.3) -> FREEZE C = (grid, tier, N_isl, R', L, inherited stores, HPM)
      writes calib.bin (+ sha256)
J3  final islands: job array r = 1..R' (throttled %M), each task = 1 island with t threads
      reads setup.bin, calib.bin (mmap); streams 9 + r (+ per-particle counters)
      checkpoint per stage on node-local disk, mirrored to scratch; writes island_r.rec atomically
J4  merge (1 node, many threads; afterok:J3)
      validates R' records -> pooled estimates -> union store and HPM -> final local search (parallel scan)
      -> extra search from c_4 (baseline record, if R' > 4) -> LS0 -> card -> fit.rds (small) + fit.bin (large)
```

Setup and calibration are computed **once** and shared; only J3 scales with R′. Islands never communicate.

### 3.2 Islands across nodes

- Island r is a deterministic function of (X, y, seed, r, binary, 𝒞). Final streams stay 10, …, 9 + R′
  (`02_method.tex:376-377`); the seeding x = seed·2³² + stream admits R′ < 2³² − 10.
- Packing: several islands per node, each with t threads (t chosen so that t·(per-thread memory) + shared node data
  fits; Section 3.7). One island per Slurm task keeps failure domains small.
- Shared per node, read-only via `mmap`: X, tables (`logr`), start arrays, neighbour graph, calib.bin.
- Per island: particles (sparse), canonical-factor caches, a byte-capped score cache, a flat ledger, RB accumulators.

### 3.3 Within-island parallelism

| level | what runs in parallel | determinism | tag |
|---|---|---|---|
| tables (setup) | blocks | per-block code unchanged | [OP-bit] |
| correlation tiles (setup) | tiles | canonical sums | [OP-bit] |
| particle moves | particles within a stage (independent given the population) | per-particle counter streams; per-thread scratch; per-thread ledgers merged by Lemma S; HPM by the strict order; provenance by minimum event key; RB by fixed-chunk or exact reduction | [OP-law] (P4, P5) |
| reweight, LSE, resampling | serial in particle order (O(N)) | unchanged arithmetic | [OP-bit] |
| neighbourhood scoring | scan candidates (local search, LS0) | max-reduction with the tie rule | [OP-bit] |
| diagnostic islands | 4 per rebuild | W-cal (not executed) | [OP-bit] by reading |

Expected speed-up of the particle level is near-linear up to the point where the serial O(N) per-stage work and
memory bandwidth bind; at N = 2,500 and p = 1M a round per particle is ≈ 0.5 s (target cost), so 16–64 threads
per island are reasonable (UNVERIFIED).

### 3.4 The merge

#### 3.4.1 Estimators (fixed island-index order, long double, as in `v3_run.R:154`)

- log Ẑ = LSE_r(log Ẑ_r) − log R′ (unbiased Ẑ given 𝒞; TH01.a).
- W_r = Ẑ_r / Σ_s Ẑ_s.
- **Primary PIP (v3.1 spec):** PIP_Z,j = Σ_r W_r ĥ_rj (`02_method.tex:442`). Consistent as R′ → ∞ for any fixed N,
  because E[Ẑ_r ĥ_rj | 𝒞] = Z·PIP_j and E[Ẑ_r | 𝒞] = Z, even if each island is biased. **Code gap:** production
  still computes the equal-weight mean as `pip_primary` (`v3_run.R:162`).
- **Secondary:** PIP_eq,j = mean_r ĥ_rj (keeps the per-island bias for every R′).
- General declared 𝓗: μ̂(h) = Σ_r W_r H_r(h) (`02_method.tex` §general-h).
- MC standard error of PIP_Z (delta method for a ratio of means): SE_j² = Σ_r W_r² (ĥ_rj − PIP_Z,j)². Reported, not
  used for selection.

#### 3.4.2 Degeneracy diagnostics (reported, never used to switch estimators)

- R_eff = 1/Σ W_r² (`02_method.tex:446`) and R_eff/R′; max_r W_r.
- σ̂ = SD_r(log Ẑ_r) (the many-island analogue of E2). For log-normal Ẑ_r, R_eff/R′ ≈ e^{−σ²}: σ = 1 → 0.37,
  σ = 2 → 0.018, σ = 3 → 1.2·10⁻⁴. So R′ must exceed about e^{σ²} times the wanted R_eff.
- k̂: generalised-Pareto shape fitted to the upper tail of the W_r (Pareto-smoothed importance-sampling diagnostic;
  k̂ < 0.5 finite variance, k̂ > 0.7 unreliable — thresholds from that literature, UNVERIFIED for this use).
- Flag `merge_degenerate` iff R_eff < R_min (declared, e.g. 30) or k̂ > 0.7.

#### 3.4.3 Fallback without selecting estimates from final outputs

The method forbids final observations from revising the schedule or selecting replacement estimates, and forbids an
adaptive R′ (`02_method.tex:389`; TH01 (c) counterexample). So:

1. **Island census inside calibration.** After the grid is frozen and before stream 10, run R_c census islands
   (e.g. R_c = 32) on calibration streams at a ladder of candidate N (N₀, 2N₀, 4N₀, …). Record σ̂(N) and per-island
   cost. A **declared rule** chooses (N_isl, R′): the smallest N on the ladder with σ̂(N) ≤ σ_max (e.g. 1.5), then
   R′ = the budget divided by the per-island cost, capped. Census islands are calibration randomness: their scored
   models may be inherited into the stores (as calibration's are, `v3_core.cpp:419-441`), but they never enter Ẑ or the
   PIPs. This keeps 𝒞 frozen before final randomness (obligation O3).
2. **At the merge:** always report both PIPs, R_eff, σ̂, k̂ and the flag. No switch.
3. **If the census shows σ̂ > σ_max at the largest affordable N:** the fit reports `merge_degenerate` and proceeds, or
   (declared alternative) uses the island-resampling design below.
4. **Island-level resampling (optional, later):** at each stage, islands send one scalar (their log increment) to a
   coordinator, which resamples islands (the "island particle model" of Vergé, Dubarry, Del Moral and Moulines, 2015;
   details UNVERIFIED). This breaks "no communication" (one scalar per island per stage, plus population copies of
   N·k integers when an island is duplicated), but it attacks degeneracy at its source. New theory (O11).

#### 3.4.4 Union of scored models: HPM, stores, card

- HPM = maximum, under the strict order `hpm_better` (`v3_util.h:121-126`), of all island HPMs, the table HPM, the
  inherited calibration HPM and the merge-time searches. Order-independent, so bitwise reproducible.
- Top store T = top_c(∪_r T_r) (Lemma S). Each island's own top-c suffices: a model in the global top-c is beaten
  by fewer than c models in every island that scored it.
- **I/O protocol for T at huge p.** Each island writes its top-c sorted by the total order. The merge does a k-way merge
  with deduplication by (hash, model) and stops after c distinct entries. A lower bound on the global threshold,
  τ_lo = max_r F_r^(c) (each island's c-th best), lets islands skip entries below τ_lo. Worst-case volume R′·c entries
  (≈ 56 B each: at p = 1M, c = 4·10⁷, R′ = 256 → ≈ 570 GB; typical much less because islands overlap). If this is
  too much, c itself is a (b)/(c) setting; reducing it is a reporting change for the card (O13).
- Final local search from the merged HPM (parallel scan, L1), the extra search from c_4 and the baseline record when
  R′ > 4 (`02_method.tex:378-382`), then LS0. Their scored models enter the union store and HPM.
- Card G1/G2/L3 read T and Ẑ exactly as now; a larger union T makes Z_T larger and G2 tighter.

### 3.5 Island record (binary, one file per island, checksummed)

header (seed, r, stream, 𝒞 hash, setup hash, binary hash, N, T, status) · log Ẑ_r and per-stage increments, ESS,
distinct counts, move statistics · ĥ_r (p doubles) · declared 𝓗 accumulators (sparse: pair counts only where
non-zero) · rb_round (Hm × p) · island_best · HPM with provenance key · top-c store (flat, sorted) · counters ·
timings and peak memory. Size at p = 1M: ≈ 40 MB plus the store (≈ 2.2 GB for c = 4·10⁷; written once).

### 3.6 Fault tolerance and determinism on Slurm

- **Replay, never drop.** A failed or pre-empted island is rerun from its last checkpoint or from the start; because
  the island is a deterministic function of its inputs, the rerun produces the same record. Dropping failed islands
  would bias the merge whenever failure correlates with the island's trajectory (e.g. a time-out on an island that
  wandered into large models). The output event is "all R′ islands completed"; P(no output) stays an operational
  frequency (`02_method.tex` output convention; Lemma RO, GUARD-W; obligation O6).
- **Checkpoint consistency.** A checkpoint holds the population at a stage boundary, the cumulative log Ẑ, and the
  ledger state **at the same boundary** (HPM, stores, counters, island_best), written atomically (tmp file + rename +
  checksum). With per-particle counter streams no generator state is needed; with the v3 serial stream, save the stream
  position. The cache is not checkpointed (it does not affect outputs).
- Slurm mechanics: job array with throttle (`--array=1-R%M`), `--requeue`, a checkpoint signal before the time limit
  (`--signal=B:USR1@300`), node-local disk for frequent checkpoints mirrored to shared scratch, `afterok` dependency
  for the merge, one file per island (no small-file storms). NOTS partition limits, node-local disk and scratch quotas
  are UNVERIFIED.
- Every record carries the binary hash and the 𝒞/setup hashes; the merge refuses mixed records.

### 3.7 Sizing examples (targets, UNVERIFIED)

Target per-step cost after Phases 1–2: 0.5 µs (S1–S4, P1–P3; from 3 µs now). T = 30.

| p | N per island | steps per island | CPU per island | R′ | final CPU | shared node data | per-island memory |
|---|---|---|---|---|---|---|---|
| 10k (N₀ rule, bitwise) | 10,000 | 4.2·10⁹ | 0.6 h | 4 | 2.3 h | < 1 GB | < 2 GB |
| 100k (N₀ rule) | 100,000 | 4.2·10¹¹ | 58 h (≈ 1 h on 64 threads) | 4 | 230 h | ≈ 6 GB | ≈ 3–6 GB |
| 100k (N_isl = 2,500) | 2,500 | 1.05·10¹⁰ | 1.5 h | 64–256 | 94–375 h | ≈ 6 GB | ≈ 2 GB |
| 1M (N_isl = 2,500) | 2,500 | 1.05·10¹¹ | 15 h (≈ 1 h on 16 threads) | 256 | ≈ 3,800 h | ≈ 17 GB (X 1.6, `logr` 14, `cond_cum` 1.3) | ≈ 3–8 GB |

Add calibration (≈ 1–3 island-equivalents per tier with H = 0.2·N_isl, plus the census) and setup (1M: ≈ 8
core-hours of canonical tiles, minutes of tables). A 1M fit with R′ = 256 is therefore ≈ 4,000 CPU-h, about 8 h on 500
cores.

---

## 4. Theory obligations created by this design

Each item names the premise or theorem to re-check. IDs refer to `04_theory.tex` / `02_method.tex`.

| ID | obligation | triggered by | premises/theorems touched | expected difficulty |
|---|---|---|---|---|
| O1 | **Merge consistency at fixed N, R′ → ∞**: PIP_Z → PIP and μ̂(h) → π(h) a.s.; CLT with the ratio-estimator variance; finite moments (Ẑ_r is bounded on a finite space, so all moments exist). | 3.4.1 | TH01.a (island identities), IND-T extended to R′ islands, N1 for general h | short (SLLN + delta method), but must be stated for the **primary** PIP |
| O2 | **Weight degeneracy at high p**: bound E[(Ẑ_r/Z)²] (relative variance) in terms of stages, per-stage χ² dispersion and kernel mixing; how σ²(log Ẑ_r) grows with p at fixed N; conditions under which R_eff/R′ stays bounded below; or a lower bound showing exponential growth (which would make island resampling necessary). | 3.4.2 | the restricted-ESS grid controls dispersion on V only (`02_method.tex:330-331`) | open research; the main statistical risk |
| O3 | **Census inside 𝒞**: (N_isl, R′) chosen from census islands on calibration streams is 𝒞-measurable, so the adaptive-R′ counterexample does not apply; census models inherited into the stores keep card G1/G2/L3. | 3.4.3 | calibration contract (`02_method.tex:344-350`), TH01 (c) | moderate (mostly a careful statement) |
| O4 | **N decoupled from p (reversal of C8 "N_e is never split")**: restate TH01 (e)(f)(i) with general (N, R′); re-check every result that uses N₀ ≥ p or "common N at N_e": settings rows 14, 18; TH08 (depth/work); TH06 (discovery counts depend on draws and particles). | P9a, 3.7 | `02_method.tex:377,390`; TH01, TH06, TH08 | moderate |
| O5 | **Per-particle counter-based streams (C6)**: EX-S/H-U and IND-T for a counter-based generator; new variate-order documentation; Prop W restated as "deterministic given (seed, binary) for any thread count". | P4, 3.3 | EX-S, IND-T, Prop W, MD04 | moderate; partly an audit |
| O6 | **Replay fault tolerance**: retries do not change outputs; the output event is "all R′ islands completed"; GUARD-W/Lemma RO restated for array jobs. | 3.6 | Lemma RO, GUARD-W, output convention | short; plus a code audit |
| O7 | **NUM-MARGIN**: a rigorous bound on \|fast score − canonical score\| (or on both errors) so that filter-then-canonical decisions equal canonical ones outside a flagged set. Without it, S5/S6 are [OP-law] only. | S5, S6, L2 | EX-A, SC(η_F), VAL-FP (card header) | hard if rigorous; an empirical audit is easy |
| O8 | **Sparse exact-below-threshold partition** (B4): validity unchanged for any deterministic partition; re-check partition theorems (TH11 SIZE/PART-pairing, OB08), the identity of TH03 M3(d), statements of TH06 that use actual blocks, and LH non-vacuity (groups with within-correlation above τ are reproduced exactly). | B4 | TH11, OB08, TH03, TH06 | moderate |
| O9 | **Kernel changes** (P9b–d): reversibility and self-adjointness of the new round (N9: TH12/OB09); the terminal-round prefix identity of N1 assumes a uniformly random order of the full label list; the RB-PIP identity needs exact Gibbs conditionals at the recorded steps (so measured rounds keep the exact Gibbs sweep). | P9 | N9, N1, TH01.a/b | moderate to hard |
| O10 | **Union-store reporting with R′ islands**: card items with T = top_c(∪_r T_r), HPM(R′) ⪰ HPM(4) with the extra search from c_4. | 3.4.4 | Lemma S, Cor W-R, card G1/G2/L3 | already covered in v3.1 (re-cite) |
| O11 | **Island-level resampling** (optional): unbiasedness of the island-level Feynman–Kac estimator, new degeneracy bounds. | 3.4.3 (4) | new | research |
| O12 | **Screening front-end** (Song–Liang-type, Appendix B): sure screening of S₀ and selection consistency on the screened set. | not recommended by default | target theory | hard |
| O13 | Smaller store capacity c at huge p (if I/O forces it): G1/G2/L3 remain true but weaker; near-tie truncation more frequent. | 3.4.4 | card | short |
| O14 | Preflight change (L4): delivery only; P(no output) changes, no estimate changes. | L4 | Lemma RO | none (record it) |
| O15 | Calibration numerics (K5, K6): the law of 𝒞 changes; validity given any frozen 𝒞 unaffected; Theorem G needs the same 0.90 rule for pilot and grid. | K5, K6 | Theorem G, calibration contract | short |
| O16 | NN-chain (or other O(p²)) complete linkage equals the greedy R13 linkage, including exact ties. | B3 | none (implementation identity) | moderate |

---

## 5. Generic versus BVS-specific layers

The same machinery should later serve graphical models, trees and other large discrete spaces. Proposed split (C++
interfaces; R only at the edges):

| layer | generic contents | interface it consumes | BVS instantiation |
|---|---|---|---|
| G-RNG | counter-based streams keyed by (seed, stream, particle, stage, round, slot); stream map and variate-order record | — | stream map 0–9 calibration, 10..9+R′ final |
| G-Score | scoring service with a canonical deterministic `score(state)`; optional fast delta path + canonical verify (NUM-MARGIN); byte-capped cache keyed by a Zobrist-type hash and exact state equality | `State` (canonical encoding, hash, total order), `canonical_score` | g-prior score with Cholesky of H and A; S2–S6 |
| G-Start | **exact start laws over decomposable structures**: components with enumerable local configurations and local scores; a global additive statistic (here size) with a prior depending only on it; exact normaliser by convolution along a chain/tree of components; exact backward sampler; max-plus mode with a tie-aware DP | `components()`, `local_configs(c)`, `local_score(c, x)`, `statistic(x)`, `prior_of_statistic(s)` | blocks of ≤ B predictors, BB(1,p) size prior, tables by DFS bordered Cholesky |
| G-SMC | island engine: tempered bridge γ_φ = γ₀ e^{φd}, reweight/LSE/multinomial resampling, labelled reversible steps composed in a uniformly random order, measured-round accumulators for a declared 𝓗 with RB hooks, checkpoints, per-thread ledgers | `start_sampler`, `discrepancy d`, `moves: list of labelled reversible steps`, `rb_hook` | Gibbs coordinates, uniform swap, neighbour swap, independence proposal; RB-PIPs |
| G-Calib | pilot ESS rule, restricted candidate set V from leader stores, grid construction, rebuild loop, triggers, census, freeze | scored (log γ₀, d) pairs | as now |
| G-Ledger | strict total order on states; HPM running best; top-c stores (flat, Lemma S merge); provenance by minimum event key | total order, hash | `hpm_better` (F, size, lexicographic) |
| G-Merge | pooled Ẑ, evidence-weighted declared functionals, R_eff/σ̂/k̂ diagnostics, union store, record validation | island records | PIPs, MPMs, edge-pair 𝓗 |
| G-Local | centre-frozen neighbourhood scan with parallel max-reduction and tie rule; move cap; local certificate (L1/L2 items) | `neighbourhood(state)` generator | flips + swaps (feasible, ≤ K) |
| G-Exec | Slurm pipeline J0–J4, mmap of shared read-only data, atomic records, replay | — | — |

BVS-specific only: preprocessing and standardisation, the g-prior score and its numerics, canonical X columns and
correlation tiles, complete linkage/neighbour graph/cut_group/duplicates, the four BVS moves, PIP/MPM semantics, the
size cap K and B rule. For a graphical-model instantiation the components of G-Start would be, for example, edge blocks
or per-node parent sets (with the global statistic the edge count), and G-Local would scan edge additions, deletions
and reversals; whether those spaces admit an exact decomposable start with a single global statistic is a research
question, not assumed here.

---

## 6. Profiling plan (later, on NOTS) and phased roadmap

### 6.1 Profiling plan (Phase 0; no code change in the core beyond timers behind a compile flag in a *copy*)

**What to time** (per phase and per mechanism, with peak RSS `VmHWM` read at each checkpoint, as `v3_fit.R:2-7` already
does once):

1. setup: Gram, correlation, complete linkage, cut/pack, tables, start, neighbour graph, dup/cut_group, R conversion;
2. per island: init draws; per stage: reweight + LSE, resampling copy, `distinct`, round; inside rounds by mechanism:
   Gibbs flip (cache hit/miss, score route), held events, uniform swap, neighbour swap, independence (draw_pi0 + score),
   order draw; particle copies; ledger offers;
3. calibration: pilot, each diagnostic island, V rescoring, each grid construction (F_V evaluations, seconds), local
   searches;
4. final local search and LS0 per scan; preflight decisions; R assembly and `saveRDS`;
5. distributions: model sizes k of scored models, cache hit rate, fraction of fresh scores, stage count T, rebuilds I.

**Sizes** (n = 200 and n = 1,000; designs: null, LH-type correlated groups with s₀ = 10, and the study generators if
they exist at larger p — UNVERIFIED):

| run set | p | N | purpose |
|---|---|---|---|
| A (current core, preflight bypassed in a copy) | 1k, 2k, 5k, 10k, 15k | N₀ rule | baseline exponents per component; confirm the LS0 preflight refusal at ≈ 2.3k; real T and I |
| B (current core, single island only, reduced N) | 10k, 20k (large-memory node) | 500, 2,500 | per-step cost vs p (copy term), cache behaviour |
| C (Phase 1 build) | same as A | same | speed-ups and **bitwise** equality with A |
| D (Phase 2–3 build) | 10k, 50k, 100k, 200k | N₀ and 2,500 | memory, thread scaling (1–64), σ̂(log Ẑ_r) vs (p, N) with R_c = 32 census islands |
| E (Phase 3 array) | 100k | 2,500 | weak scaling R′ = 16, 64, 256, 1,024: Slurm overheads, I/O volume of stores, merge time, R_eff/R′ |

**Expected outputs:** fitted exponents and constants per component (time ∝ p^a, memory ∝ p^b); per-step cost
breakdown; the p at which each wall binds on NOTS hardware; a table of σ̂(log Ẑ_r) and R_eff/R′ against p and N
(the empirical answer to O2); thread efficiency; merge I/O volume; a calibrated version of the Section 1.3 and 3.7
tables replacing every UNVERIFIED extrapolation.

### 6.2 Roadmap with acceptance and kill criteria

| phase | content | acceptance | kill / redirect criteria |
|---|---|---|---|
| **0. Profile** | Section 6.1 sets A, B on NOTS; no core change | profiles and exponents recorded | if the measured order of walls differs from Section 1.3, re-rank Phases 1–2 before coding |
| **1. Bitwise engineering** [OP-bit] | S1, S4 (tables T1, exact branch), B1, P1–P3, P7, D1, D2, K1–K3, L1, M2–M3, T2–T4; preflight fix L4 (delivery only) | **bitwise** regression of the full output against v3.1 on the study designs and smoke tests (A_build harness); ≥ 3× fewer seconds per step; p = 10k delivered in ≤ 24 h | any unexplained bit mismatch → stop and bisect; if the per-step gain < 2× → profile again before Phase 2 |
| **2. O(np)-memory canonical core** [OP-bit] | S2, S3, G1–G5, B2, T3, M1; per-particle factor cache | bitwise equality with Phase 1 at p ≤ 15k; p = 50k–100k delivered (N₀ rule, threads) | if exact complete linkage exceeds the largest node (memory) or 12 h at the target p → adopt B4 in Phase 4 for p above that point; if the canonical scorer is > 2× slower than the Gram scorer at k ≤ 20 → keep a Gram for p ≤ 20k |
| **3. Many-island layer** [OP-law] + method decision | P4–P6, K4, D4, Section 3 pipeline (census, merge, union store, replay), primary PIP_Z in code; owner decision on N_isl (O4) | determinism for any thread count; R′ = 256 at p = 100k end to end; merge reproduces the serial R′ = 4 result when R′ = 4 and threads = 1 (except the documented [OP-law] changes) | **if the census gives σ̂(log Ẑ_r) > 2.5 at the largest affordable N at p = 100k** (R_eff/R′ < 0.2%), Ẑ-weighting cannot work with hundreds of islands → stop scaling R′; go to island resampling (O11) or kernel work (Phase 4); if Slurm/merge overhead > 20% of island CPU → repack islands per task |
| **4. 1M feasibility** [Δlaw] | B4 partition at p ≥ p_CL; P9a (if not already adopted), optionally P9b–d; S5/S6 with the O7 audit | p = 1M fit delivered in ≤ 24 h wall on ≤ 1,000 cores; on p = 100k benchmarks where Phase 3 also runs, HPM recovery, PIP error and Ẑ coverage within declared tolerances of the Phase 3 method | per-island CPU at 1M > 24 h after all optimisations with N_isl = 2,500 → the full p-sweep per round is the binding cost; only P9b–d (kernel changes, O9) remain; if accuracy at 100k degrades beyond tolerance under any Δlaw change → reject that change |

Theory track (parallel to Phases 3–4): O1, O3, O5, O6 first (they gate the many-island claims), then O2 (the
degeneracy question), then O4, O8, O9 as the corresponding changes are adopted.

---

## Appendix A. Micro-benchmarks (local, p ≤ 5,000)

Harness `scaling_scratch/bench.cpp` includes the production headers unchanged (read-only) with stubs for the three Rcpp
symbols of `v3_runtime.h`; built with the production flags of `Makevars.v3` under GCC 14.3 (the NOTS compiler version
named in `core/README.md`). Raw output: `scaling_scratch/RESULTS_2026-11-10.txt`.

| test | what was checked | result |
|---|---|---|
| `gram` | lane-parallel Gram vs `data_init`, every entry compared with `memcmp` | 0 mismatches of 2.1·10⁷ entries; 1.5–2.3× (SSE2), 3.5× (AVX2 build) |
| `score` | Gram-free columns (`try_chol(S, true)`) vs `score(S)`, random S, k = 1…100 | 0 mismatches of 82,400 scores; Gram-free *full recomputation* is 1.7–8× slower (the incremental version needs only k dot products) |
| `tables` | DFS bordered Cholesky vs `build_tables`, every table entry | 0 mismatches of 762,000 scores; 5.2–8.2× faster; no fallbacks |
| `setup` | partial-selection neighbour graph vs `neighbour_graph` | identical graphs; 8–14× faster; complete linkage ≈ p^2.3 |
| `engine` | one real `run_island` (N = 64, T = 8, B = 10) | 3.1–3.9 µs per elementary step; cache hit rate 0.33–0.47; flip miss 2.8–4.3 µs, hit 0.24–0.32 µs; particle copy 0.04–0.06 µs at W ≤ 63 |

Limits: one CPU type; synthetic data; small N and T; times at p > 5,000 are extrapolations. The bitwise results
concern the specific routes exercised (Cholesky route, Q not recomputed); the fallback routes call the production
scorer unchanged.

## Appendix B. Song & Liang (2015) split-and-merge, relative to this design

- **SAM** splits the *predictors* into K_n subsets, runs BVS on each subset's data (stage 1, screening by marginal
  inclusion probability), then BVS on the union of the survivors (stage 2) (`32_*.pdf` §3.1). Stage 1 posteriors are
  sub-model posteriors, so the reported posterior is that of the screened problem: in our tags, [Δtarget], with a
  sure-screening theorem as the price.
- **Complexity (§6):** per subset O(n(P/K_n)²) + {O(s³) + O(P/K_n)}·T; with T = O((P/K_n)^ξ) and K_n = O(√P) the
  parallel time is O(P^{(1+ξ)/2}) + O(nP), against O(nP²) for the lasso.
- **Comparison.** Our islands split *Monte Carlo replicates* of the same target, so no screening theory is needed and
  the merge is exact in expectation (Ẑ-weighting). The per-island cost here is linear in p for fixed N (Θ(N·p·rounds)),
  plus a one-time Θ(np²) flop setup for the correlation structures (parallel; memory O(pB) except exact linkage).
  SAM's √P splitting would cut that setup to Θ(nP²/K_n) total, but only by giving up all-pairs structures.
- **What we can borrow without changing the target:** (i) cheap screening statistics as *proposal* weights (informed
  swaps, P9c, with Hastings correction); (ii) π₀ marginal inclusion probabilities (exactly computable by the block DP)
  as a diagnostic. **Caution:** the study found the start masked almost everywhere (median log₁₀ π₀(S₀) down to −25.6,
  `03_empirics.tex:559`; "about 7 of the 14 truths are invisible at n = 200", `02_method.tex:241`), so π₀-based
  *screening* would drop truths; it is not recommended as a front end.

## Appendix C. UNVERIFIED items (collected)

NOTS hardware (cores, memory and AVX2 per node type; scratch and node-local disk; partition limits); typical stage count
T and rebuild count I; every number beyond p = 5,000 in Sections 1.3 and 3.7; the target per-step cost 0.5 µs; the
LS0 preflight refusal point (by reading, not executed); glibc runtime selection of `exp`/`log` variants across node
types; the x87 precision mode in the NOTS build (K2); NN-chain equivalence under R13 ties (B3, O16); Pareto-k̂
thresholds for this use; details of the island particle model of Vergé et al. (2015); whether any card reads the
final-run leader stores (D3); exact replication of R's `mean`/`sum` in C++ (M1); availability of the study data
generators at larger p.
