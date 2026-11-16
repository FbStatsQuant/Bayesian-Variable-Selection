# ENGINEERING_STRATEGY — the large-p engine ("v4") (draft v0.1, 2026-11-15, owner conversation)

Proposal only. Engine code on `main` is HQ's call, and the engine's builder is the W3-SCALE leg-C team (OD-11). This file
complements EXPERIMENT_PLAN §5 (the gap list) with *how* to build it.

## 1. Principle: one C++ engine binary; R leaves the production path
- **`smcbvs`**: a standalone C++20 executable (CMake, static where possible). R and Rcpp are not used in any NOTS job.
- R keeps two roles:
  - **reference oracle**: v3.1 via `v3_fit`, used in the equivalence tests at small p;
  - **analysis**.
- **Copy the math, rewrite the plumbing.** The numerical kernels are taken verbatim from the v3 headers, so their bits
  are anchored by the existing 50-case unit harness: the scorer arithmetic (`v3_score.h`), the start law and tables
  (`v3_start.h`), the four elementary steps, resampling, calibration rules (`v3_engine.h`, `v3_calib.h`). New are memory
  layout, threading, I/O, checkpoints and orchestration.
- Today's R jobs at 1M would hit:
  - R loops over p (`apply` in preprocessing);
  - O(np²) `crossprod` for duplicate columns;
  - R lists of 4·10⁷ store models;
  - n·p < 2³¹ indexing;
  - the cost of copying to R.

  The standalone binary removes all of these.

## 2. Pipeline: subcommands, one Slurm job each, files on /scratch
| step | command | CPUs | output (binary + JSON manifest with hashes) |
|---|---|---|---|
| 0 | `smcbvs gen` (or in-process) | — | data regenerated from (design, seed); only a hash is stored |
| 1 | `smcbvs setup` | 96–192 | `setup.bin`, one mmap file: standardised X (column-major, 64-byte aligned), z, column stats, neighbour lists (CSR), partition, block tables, sampler tables, start mode |
| 2 | `smcbvs calibrate` | 4 × 96 | `grid.bin` (frozen schedule), inherited ledger |
| 3 | `smcbvs island --id r` | 16 × 96 | `island_r.bin`: stage table, RB arrays, PIPs, Ẑ_r, top-c store, leaders, HPM, counters; checkpoints |
| 4 | `smcbvs merge` | 96 | merged store and HPM; then the tail (final local search, LS0); `fit.bin` + `fit.json` |
| 5 | `smcbvs eval` (EXP) | 8–96 | selection, PIP, DIST (closed-form Hellinger), cost records |

- **Orchestration**: a small Python driver writes the sbatch files with `--dependency=afterok`.
- Replicates are pipelined: fit k+1 calibrates while fit k runs its islands.
- Every job validates its inputs by hash before it starts. Publication is atomic (write, then rename).

## 3. Hot path: the elementary step (≈ 99% of the core-hours)
Measured today: 1.2–2 µs per step (revision D, n = 200, with the Gram). The 1M budget scales linearly in this number.
| angle | what | tag | expected effect |
|---|---|---|---|
| Gram-free score with a **per-particle factor cache** | keep the Cholesky factor of the particle's current S; scoring S ∪ j or S \ j is a bordered update: k dot products of length n (lane-parallel across the k products) + O(k²) | [OP-bit] per score (same operation sequence) | no p² memory; ≈ 0.1–0.3 µs of arithmetic at n = 200, k ≈ 5 |
| no copies | toggle in place, undo on reject (today `tmpQ = P` copies a p-bit bitset: 125 KB at 1M) | [OP-bit] | removes a cost that would otherwise dominate at 1M |
| memory layout | X contiguous, huge pages; threads pinned to one socket (a 96-CPU task is about one socket); first-touch per socket | none | fewer cache and TLB misses on 1.6 GB of X |
| pinned transcendental functions | exp, log, log1p, lgamma from one bundled implementation, not glibc's CPU-dependent variants | [OP-bit] across node types | removes the open "glibc variant" item (DESIGN_v1 appendix) |
| SIMD only where proven | lane-parallel kernels (independent sums per lane, no FMA: `-ffp-contract=off` as now); AVX-512 only in kernels that pass the bit tests | [OP-bit] | 2–4× on the setup kernels |
| per-thread ledger buffers | each thread keeps a bounded top-c heap and counters; merged at each stage end in particle order | deterministic | removes locks from the hot path |
| cache | per-thread memo with a fixed size, or none | needs OD-3 (B2-3) | memory flat in p |

**Target**: 0.5–1.0 µs per step. **Plan value**: 1.2 µs. A micro-benchmark on Owls at p = 10⁵–10⁶ (in RAM, a few cores)
comes before any number is promised. At 0.6 µs a 1M fit is ≈ 1,100 billed core-h and ≈ 1.5–2 h at the cap.

## 4. Parallel model
- **Across islands**: processes, no communication.
- **Inside an island**: threads over **particles**. Each particle has its own xoshiro256** stream, seeded by
  SplitMix64(seed, island, stage, particle) (OD-8(b), [OP-law]). Stage barrier: reweight, resample, reduce. Every reduction
  is done in particle order, so **the output is identical for any thread count** (gate T3).
- Expected scaling: ≈ linear to 48 threads per island (52 particles per core in the final islands; ≈ 10 in calibration).
- Synchronisation per stage: ≈ milliseconds against ≈ 100 s of work.
- **Compat mode**: the same binary with the v3 serial stream layout and one thread. It must reproduce v3.1 bit for bit
  (gate T2). That isolates the single law-level change (the stream layout) from all the plumbing.

## 5. Setup kernels (once per dataset)
- **Correlations** (neighbour graph, duplicates, partition): tiles of X_aᵀX_b. Each entry is a sequential dot product (same
  order as `data_init`), with lanes over pairs. n·p² = 2·10¹⁴ at n = 200 → ≈ 10–20 min on 96 CPUs. Only the top-B per
  column and the {|r| ≥ τ} edges are kept: O(pB) memory.
- **Partition** (OD-5): union-find on the threshold graph, then the exact v3 complete linkage inside each component.
- **Tables**: depth-first enumeration with a bordered Cholesky (v0 measured 5–8×, identical bits), threaded over blocks;
  ≈ 2·10⁸ codes at n = 200.

## 6. Checkpoint and restart
- At every stage boundary, write the particles (sparse supports), the stream states, the per-thread ledger heaps and the
  accumulators. Write atomically; keep the last two.
- A restart from a checkpoint must reproduce the uninterrupted run bit for bit (gate T6, forced kill at 10⁵).
- Side benefit: 1-hour `scavenge` jobs become usable for islands (checkpoint every stage). This is optional, after asking
  HQ about billing and preemption.

## 7. Gates (all automated in CI where possible)
- **T1 kernels**: scorer, tables, start, steps, resampling are bit-identical to the v3 headers (existing 50 cases, plus new
  ones at p ≥ 10⁵).
- **T2 compat mode**: equal to v3.1 on PROD-H 24 + supplementary + revision D setups at 5k/10k/20k.
- **T3 thread invariance**: production mode, identical output for 1, 8, 48 and 96 threads.
- **T4 law check** (the [OP-law] change):
  - compat vs production over 200 seeds at p ≤ 1k;
  - two-sample tests on log Ẑ, PIPs, HPM frequency, stage counts;
  - thresholds declared beforehand.
- **T5 scale**: Owls at 10⁵ (full fit, a few cores) and 10⁶ (setup plus one stage), before NOTS.
- **T6 restart**: bit-identical resume.
- **T7 evaluator**: the closed-form Hellinger against brute-force Monte Carlo on fixtures.

## 8. Work split and sequence (≈ 3 weeks of engineering; HQ approves)
1. Week 1, skeleton:
   - setup.bin + compat mode + T1/T2 (SCALE A);
   - generator + evaluator (EXP);
   - Owls micro-benchmark of the step (EXP, local).
2. Week 2:
   - particle threading, per-particle streams, T3/T4 (SCALE A);
   - correlation tiles + partition + tables (SCALE B);
   - merge + tail + checkpoint (SCALE B).
3. Week 3:
   - Slurm driver and pipelining (EXP);
   - T5/T6 on NOTS (≈ 150 core-h);
   - Sol code review → rung A.
