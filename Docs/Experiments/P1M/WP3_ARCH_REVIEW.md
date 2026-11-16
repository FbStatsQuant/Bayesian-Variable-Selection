# WP3_ARCH_REVIEW — cost architecture of the island at 10⁶, design risks, builder split

**WP3 architect (Fable 5.2, high), 2026-11-16. For the Engineering manager.**
Brief: `briefs/BRIEF_fable_wp3_architect.md`. Prototypes: branch `exp/P1M-wp3-arch` (3 commits on top of
`exp/P1M-engine` + PR #26 head `5c8ab8a5`; prototypes only, no PR). Every number is labelled MEASURED (machine, command
in §6) or ESTIMATE. "Owls" = Xeon Gold 6148, gcc 11.5, `-march=x86-64-v4` for the island sources, 3 threads, `nice -n 19`,
machine load 21–29 during the runs. "SPR" = NOTS Sapphire Rapids, job 2748756 unless stated.

## 0. Summary

1. **Late 10⁶ rounds can go well under the plan.** Measured 287 ns·CPU per pair (job 2748756) and 240–254 with L5
   (job 2749328). The store check moved off the step path, bounded scoring and Gram-row reuse give **≈ 120 ns·CPU per
   pair**, ≈ 102–110 if L5's compaction regression is recovered (ESTIMATE on SPR, §1.1 and §2; plan 200). On Owls the same two late rounds of a 10⁶ island went from 47.1 s to 28.1 s (−40%) with
   an identical output hash (MEASURED).
2. **About 24% of a late round is a serial debug check that no counter shows.** `check_store` is on by default and
   verifies the whole store after every step: 6.6 s per step at 4·10⁷ entries (MEASURED, Owls); ≈ 5.7 s of every round
   is in no counter on SPR, before and after L5 (§1.1). Moving it off the step path alone gives ≈ 184 ns·CPU per pair.
3. **The late-round figure is not the cost of a fit.** No SPR run so far has measured a bridge. Early bridge stages
   carry π₀-sized supports and many sweeps per particle. At 10⁶ with the stand-in start law a step costs
   **13–16 µs of thread time, about 25× a late round and about 45× the plan** (MEASURED, Owls). The prototype brings
   that to 3.1–3.6 µs (÷ 4, identical state hash). It cannot bring it to the plan: an exact flip score on a support of
   k unshared columns needs k·n multiply-adds. The 1M budget must be re-sized from a per-stage profile (§1.3, §3 R1).
4. Two more design risks: calibration islands carry leader stores that compact serially (+42% at 3 threads, MEASURED),
   and the top store is rewritten about once per bridge stage (§3 R2, R3).
5. The SPR confirmation is one job of ≈ 40 core-h (§5).
6. Addendum §7: the L5 batch confirms the uncounted check on SPR (≈ 5.7 s per step in both islands); the real setup
   tables cost under 2% in phase A but 8–35 GB of memory, depending on how the island holds them.
7. Addendum §8: the per-stage re-size of one 1M fit against H-10's 1,188 core-h, by start-law size E₀ = 10 / 25 / 56
   (ESTIMATE): today's code 2,575 / 4,136 / 9,937; levers 1–3 with the sort fix 1,159 / 1,609 / 2,624; with the offer
   floor 895 / 1,264 / 2,112. Job 2749483 confirmed the late round on SPR: 236 → 116 ns·CPU per pair, same bits.

## 1. Cost model

### 1.1 A late 10⁶ round on SPR, before and after L5 (MEASURED; G = 256, 96 threads on one socket, same data and stream)

Before = job 2748756 (commit efc0dfd0), after = job 2749328 (commit be24e9d), round 5, island 1; island 2 of the second
job is within 0.2 s on every line. 9.72·10⁹ (support, label) pairs, M = 3.89. One second of wall = 9.87 ns·CPU per pair.
Phase times are differences of the cumulative `[island]` counters; compaction is from the `[round]` line.

| part | before, s | after L5, s | after, ns·CPU per pair | nature |
|---|---|---|---|---|
| phase A: products | 4.5 | 4.7 | 46 | core throughput; hyperthreads add nothing (job 2748105: 49.5 → 98.8 thread-ns from 48 to 96 threads) |
| phase A: flips, odds, uniform scan | 6.5 | 7.2 | 71 | throughput |
| **store invariant check (in no counter)** | ≈ 5.9 | **≈ 5.7** | **≈ 56** | serial, once per step |
| phase B | 1.9 | 2.7 | 27 | throughput, memory-bound |
| compaction | 0.7 | 1.7 | 16 | one compaction per late round in both jobs |
| orders | 2.9 | 1.7 | 17 | throughput, random memory access |
| walk | 3.5 | 0.6 | 6 | was latency-bound on one π₀ draw per pass |
| build | 3.1 | 0.0 | 0 | was the serial zero-fill of the score rows |
| **round** | **29.1** | **24.3** | **240** (rounds 4–5: 247) | plan 200 |

- **The check.** The counted phases sum to 22.4 s before and 16.9 s after; with the compaction, 5.9 s and 5.7 s of each
  round are in no counter (5.8 and 5.8 in round 4; the same in island 2). The amount does not depend on L5, on G (it was
  the same at G = 64) or on the number of passes: it is per step. `check_store` is on by default in both commits and
  verifies the whole store, serially, after every step. Alone it costs 6.64 s at c = 4·10⁷, k = 6 on Owls (MEASURED,
  `v4_bench_arch check 40000001 6 3`; 166 ns per entry: one random index lookup each). If the late compaction runs
  between phase-B waves, it is counted inside phase B as well and the check is then 7.4 s; 5.7 s is the lower bound.
- **Why L5 gave 247 and not 215.** WP3's projection removed 7.4 s (walk, build, orders, apply) from 29.1 s. The
  measured counters removed 7.2 s there: that part landed. Three things moved the other way: phase A + 0.9 s (+ 8%;
  products 44.4 → 46.5 thread-ns per pair; cause not identified, possibly the node), phase B + 0.8 s and compaction
  + 0.9 s (m3).
- **m3, from the store counters.** The number of compactions per round did not change (29–31, 14–16, 6–7, 2, 1). The
  time per compaction did: 0.72–0.76 s in rounds 2–5 before, 1.56–1.73 s after; round 1 is unchanged at ≈ 1.6 s.
  So about 0.9 s was added to every compaction. Diagnosis from the code, not measured: `psort_noalloc` replaced the
  library's parallel sort by a pairwise merge tree, and the last levels of that tree run on 1–3 threads over all staged
  entries, twice per compaction. A bucket sort on the leading key (the hash, then the value) with per-bucket sorts has no
  such levels and gives the same unique order. Phase B's own rise may be the same seconds seen twice (a compaction between
  waves sits inside the phase-B timer), so the regression is 0.9–1.7 s per late round.
- A linear fit of phase A over the two islands of the first job (ESTIMATE from two MEASURED points, G = 64 and 256)
  gives ≈ 9 ms of wall per pass that does not depend on the pairs: 1.2 s per round at 131 passes.
- Round 1 (π₀ → φ = 1 in one stage, M ≈ 55): 540 → 533 s. It is not a model of a bridge stage: the one-stage jump
  collapses the population onto a few ancestors, so its supports are shared. §1.3 measures real early stages.

### 1.2 Three structural causes

1. **Most scores are never consumed.** A pass scores every label for every support. A particle consumes only the labels
   between its last change and its next one. At M = 3.9, 74% of the flip evaluations are discarded (spec §3 rule 2).
   In early bridge stages M is 10–21 and the discarded share is 90–95%.
2. **The same Gram entries are recomputed in every pass.** The product xₐᵀx_j depends on the column only. A column that
   stays in a particle's support is recomputed for all p labels in each of its M passes.
3. **Serial or latency-bound work sits on the step path**: the store check, zero-fills, one slow particle in the walk.
   96 billed CPUs wait for one thread. L5 removes most of it; the check remains.

### 1.3 The bridge: cost against support size and sweeps (MEASURED, Owls)

Kernel alone, dense scoring (`v4_bench_island kernel 100000 3 64 k div A 128`), ns of thread time per pair:

| supports | products | flips + odds | total |
|---|---|---|---|
| k = 6, 5 members shared by all supports | 19 | 66 | 85 |
| k = 6, all members distinct | 73 | 58 | 131 |
| k = 20, all distinct | 220 | 103 | 322 |
| k = 50, all distinct | 598 | 416 | 1,014 |

A full bridge at 10⁵ (N = 256, G = 256, core's pilot rule with floor 1/30: 25 stages, then 2 + 2 rounds), reference =
PR #26 head without the check:

| stage φ | mean \|S\| | M | reference ns per step | prototype ns per step | flips per step, ref → prototype |
|---|---|---|---|---|---|
| 0.067 | 23.5 | 9.8 | 2,512 | 1,187 | 9.3 → 1.46 |
| 0.33 | 16.7 | 8.7 | 1,675 | 863 | 8.2 → 1.36 |
| 0.60 | 6.9 | 6.0 | 1,014 | 659 | 5.3 → 1.24 |
| 0.78 | 5.6 | 3.1 | 397 | 285 | 2.5 → 1.06 |
| 1 (last round) | 5.8 | 3.4 | 438 | 271 | 2.9 → 1.03 |
| **whole run** | | 6.6 | **1,301** (322 s) | **705** (174 s) | |

The two runs print the same output hash (`925cfff768fd65af`). The bridge-averaged cost per step is 3.0× the late-round
cost in the reference and 2.6× in the prototype. Note M: 10 in the first stages, not 3–4.

The first three stages of a bridge at 10⁶ (N = 24, φ = 0.01, 0.02, 0.03; stand-in start law, E_π₀|S| = 56):

| | mean \|S\| | M | ns per step | flips per step | columns whose products are computed, per pass |
|---|---|---|---|---|---|
| reference | 55 | 20–22 | 12,975–15,921 | 19.7–21.4 | 154–167 |
| prototype (bounded scoring + Gram rows) | 55 | 20–22 | 3,073–3,628 (stages 2, 3) | 1.44–1.56 | 12.5–15 |

Same state hash after stage 3 (`0b26e3b8848270dd`). Late rounds of a 10⁶ island on the same machine cost 551 ns per
step (reference) and 330 (prototype).

**What this means for the budget.** The plan charges 300 ns of thread time per step in every stage. H-9 scales the 1M
block by 1.44 from late rounds. If the production start law at 10⁶ has supports near the stand-in's 56 members, an
early stage costs about 45× the plan with today's code and about 10× with the prototype. The share of such stages in a
calibrated schedule is not known to me. ESTIMATE (Owls thread time), if the 10⁶ profile has the shape measured at 10⁵:
a bridge-averaged cost near 25× the plan today and 6–7× with the prototype. This is the largest open number of the 1M
budget, and it is conditional on the stand-in start law.

### 1.4 The model

Per step (one particle, one label), with k the support size, u the number of its columns not shared with other
supports of the pass, n = 200, and M sweeps per particle-round:

- today: `M · [ (u + shared/supports) · n · c_fma + c_flip(k) ] + c_fixed`
- with the recommendations: `[ (u + adds) · n · c_fma ] + E · c_flip(k) + c_fixed`, where E ≈ 1.0–1.5 flips per step
  (MEASURED at every stage above) and "adds" ≈ (M − 1)/2 new columns per round.
- c_fma ≈ 0.10 ns·core per multiply-add on SPR (ESTIMATE: 44.4 ns of thread time per pair, MEASURED, for ≈ 213
  multiply-adds, two threads per core); 0.067 on Owls, 0.045 with FMA (MEASURED, `v4_bench_arch products 80 2048 3`).
- c_flip(k) grows as k²: 58–66 ns at k = 6, 416 ns at k = 50 on Owls. At large k it is bound by the latency of one
  dependency chain (the forward substitution), not by throughput.
- Floor: one consumed flip on a support of u unshared columns needs u·n multiply-adds, in any design that keeps the
  exact scores. At u = 50 that is ≈ 0.5 µs·core per step.

The unit "ns per (support, label) pair" stops meaning anything once whole supports are no longer scored. I use
**ns·CPU per step** below (plan: 600) and give the per-pair equivalent at M = 3.89 for the late round.

## 2. Recommendations, ranked

Expected gain = late 10⁶ round on SPR, ns·CPU per pair-equivalent, **on the measured L5 basis of §1.1 (240, round 5)**
(ESTIMATE unless marked). "Same bits" = the output hash is unchanged, checked on Owls in both arithmetic forms where it
applies.

| # | lever | output | expected on SPR, from 240 | MEASURED on Owls | state |
|---|---|---|---|---|---|
| 0 | L5 as built by WP3 (PR #26) | same bits | done: 287 → 240 (MEASURED, round 5) | π₀ draw 60 → 4.3 ms, round order 40 → 20 ns per label | merged basis |
| 1 | store check: parallel, and only before a checkpoint or the final write | same bits | **−56** | 6.64 s per step serial; 1.2 s with 3 threads | one-day change |
| 2 | bounded scoring: score a (support, label) only if a particle can still consume it; bounded uniform scan; one-particle phase B | same bits | **−43** | late 10⁶ round 47.1 → 34.0 s; flips 3.83 → 1.37 per step | prototype |
| 3 | Gram rows of active columns kept across passes | same bits | **−19** | 34.0 → 28.1 s; products 31 → 15 thread-s; early 10⁶ stages ÷ 4 with #2 | prototype |
| 4 | Philox 32×32 multiply (`vpmuludq` instead of the 64-bit lane multiply) | same bits | −3.5 | round order 19.7 → 15.6 ns per label; π₀ draw 4.27 → 3.03 ms; a 16-draw look-ahead adds −12% | prototype |
| m3 | compaction sort without the serial merge levels (§1.1) | same bits | −9 to −17 | not measured (diagnosis) | WP3 |
| 5 | rolling admission: a finished particle's slot goes to the next particle, so every pass stays full | same bits | −15 | not built (from the 9 ms per pass of §1.1 and ≈ 45 passes per round instead of 131) | design |
| 6 | FMA in the class-A products | **other class-A bits**; label-major = particle-major kept | −5 to −8 | products 15.3 → 12.4 thread-s; kernel 0.067 → 0.045 ns per multiply-add | prototype; your decision |
| 7 | large supports: full 8-label groups across tiles, several groups per flip call, deletion scores from the cached Gram | same bits | small late; ≈ ÷ 1.5–2 on early stages | interleaving alone: no gain (most calls hold 1–2 groups) | design |
| 8 | offer floor from calibration (§3 R3) | **island file content changes**; fit identical | −5 late; −10 to −20% of a bridge stage; −10 to −15 GB | compaction = 30% of the prototype's 10⁵ bridge | needs a contract decision |

Levers 1–4: 240 → **≈ 120 ns·CPU per pair-equivalent ≈ 460 ns·CPU per step** at M = 3.89; with m3, ≈ 102–110
(ESTIMATE; plan 200 per pair, 600 per step at M = 3). Lever 1 alone gives ≈ 184. The M risk of H-9 is absorbed in late
rounds: the cost no longer scales with M, because the flips per step stay near 1.0–1.5 whatever M is.

How the ESTIMATE is built: the measured L5 phases of §1.1 with the Owls ratios of the same two rounds applied to phase A
(× 0.67 with bounded scoring and scan: 25.3 / 37.5 s; × 0.54 with Gram rows: 20.4 / 37.5), to phase B (× 0.81, × 0.69)
and to the orders (× 0.79). 24.3 − 5.6 (check) = 18.7 s → 14.3 s → 12.0 s.

### 2.1 Lever 2, bounded scoring (the main design change)

- A non-member label j is scored for support s only if some particle i on s has `q_i < inv_i[j] < fmin_i`. Here q_i is
  the particle's consumed prefix and fmin_i its running first change, which only decreases during a pass.
- The deletion odds of the k members are already in the support cache. So the first member that its uniform deletes is
  known **before** any tile is scored, and it initialises fmin_i. About half of the changes are deletions; for those
  passes nothing is scored beyond what is consumed.
- The needed labels of a tile are packed 8 to a vector. A lane's result does not depend on the other lanes, so the bits
  do not change.
- Why the output cannot change: every label a particle consumes has a position ≤ its final e ≤ fmin at any time, so it
  passed the test when its tile was scored. Phase B, the walk and the apply step read only such values. Which
  unconsumed labels are scored now depends on thread timing; they are never read.
- Test to add for production: fill the score rows with NaN before each pass (test build) so that any read of a value
  not computed in the pass fails loudly.
- MEASURED: hashes unchanged at p = 2·10⁴ (class A `263474601a55acb1`, bit form `f9c6272ed1ffbae5`, 1 and 3 threads),
  at 10⁵ over a whole bridge, and at 10⁶ (late rounds and early stages).

### 2.2 Lever 3, Gram rows

- One row X ᵀxₐ (p doubles, the bits of `tile_products`) per active column, in a slot it keeps while any active particle
  holds the column. A pass computes products only for columns that are new; a pass with no new column does not read X.
- MEASURED at 10⁶ late rounds: 66% of (column, pass) products reused. Early stages: 92%.
- Memory: slots × 8 MB at 10⁶. 640 slots (5 GB) cover G = 256 in late rounds. With π₀-sized supports G·k slots would be
  needed (G = 256, k = 56: 115 GB), so the group size must follow the support size (G·k̄ ≤ slots) or the columns without
  a slot fall back to per-pass products (prototype: tested with 24 slots, same hash). The memory plan needs the term.
- Limit found: at large k the flips then wait on memory (k cache lines per needed label). For passes that need few
  labels, computing the k dot products of just those labels from the tile is cheaper than caching whole rows
  (ESTIMATE 0.3 µs·core per flip at k = 55). This belongs to lever 7.

### 2.3 The candidates named in the brief

| candidate | verdict |
|---|---|
| X / score-row layout and blocking | Keep the 128-label row-major tiles and the 4-column products block. Reuse Gram rows instead of re-blocking (lever 3). The score rows stay; software prefetch one (support, tile) ahead in phase B is a cheap follow-up. |
| tile size | Keep 128. With Gram rows the per-thread product buffer holds only new columns, so the large-support blow-up of that buffer (14 MB per thread at G·k = 14,000 columns) goes away. |
| G > 256 with inverse-only orders | Not needed. Drop the stored order anyway (saves G·m·4 bytes: 1 GB at G = 256), but spend the effort on rolling admission (lever 5), which removes the tail of nearly empty passes without the 4 GB of extra score rows that G = 512 costs. |
| fusing walk and build | No. After L5 both are small. Precompute the I-step proposals in the order phase instead: their address does not depend on the state, and it removes the one latency-bound item left in the walk. |
| socket-local placement, first touch | Keep H-9 (one island per socket, `numactl --membind`). All large arrays are first touched by the master thread, which is correct only under that binding: make the binding a checked precondition of the `island` command at p ≥ 10⁵. |
| SMT | Keep 96 threads per socket. Billing is per hardware thread, products gain nothing from the second thread, the flip and scan code gains (1.15× overall, job 2748105). |
| per-pass synchronisation | Not a bottleneck after L5 (≈ 5 parallel regions and ≈ 20 phase-B waves per pass, tens of µs each). The per-pass cost that remains is the 9 ms of phase A, which levers 3 and 5 remove. |

### 2.4 Can the island reach 200 ns·CPU per pair?

- **Late rounds: yes**, ≈ 120, and ≈ 102–110 with the compaction sort fixed (ESTIMATE), to be confirmed on SPR (§5).
  The store check alone brings the measured 240 to ≈ 184.
- **Early bridge stages: no.** The prototype reaches 3.1–3.6 µs of thread time per step at 10⁶ with 55-member supports
  (MEASURED), against 0.3 in the plan. Lever 7, a cheaper deletion score and the offer floor may give another factor of
  about 2 (ESTIMATE). The floor of §1.4 (u·n multiply-adds per consumed flip) stays. What decides the bill is how many
  stages a calibrated 10⁶ schedule spends at large supports, and how large the production start law's supports are.
  Neither is an engineering lever of the kernel: the grid refinement m (D-12) multiplies exactly these stages.

## 3. Design-risk findings

**R1 (budget, high). The 1M block is sized from late rounds; the bridge is where the cost is.** Evidence in §1.3.
Actions, in order: (a) ask WP2 for E_π₀|S| and its 90% quantile at 10⁶ from the production tables (the size masses are
in setup; no run needed); (b) T5 records, per stage, wall, mean |S|, M, flips per step and active columns per pass
(the prototype prints them as `[arch]` lines); (c) the early-stage probe of §5 at 10⁶ on SPR (≈ 3 core-h); (d) re-size
the 1M block per stage, not by one ratio. If the total passes ≈ 30k, H-9 sends it back to HQ: say so early.

**R2 (calibration, medium–high). Leader stores compact serially under the store lock.** `lead0` and `lead1` (cap 20p
each) are never deferred: a flush that fills their staging area runs `compact_locked` (serial sort, merge and index
rebuild of up to 2·10⁷ entries) while the other threads wait. MEASURED on the 10⁵ bridge, 3 threads: 174 s → 248 s
(+42%), phase B 47 → 105 s. At 96 threads the serial part does not shrink. Calibration is 3 of 19 island-equivalents
in the plan and has never run at 10⁶. Fix: give the leader stores the deferred parallel compaction of the top store
(same class, same proof) and measure one calibration-shaped island on SPR (`V4_LEADERS=1`).

**R3 (cost and memory, medium). The top store is rewritten about once per bridge stage.** On the 10⁵ bridge 98.6·10⁶
offers were buffered for a store of 4·10⁶ (≈ 1.1 capacities per stage) and compaction took 52 s of the prototype's
174 s. Each stage's models are better than the last one's, so almost none of the bridge offers survive. They also set
the memory peak (π₀-sized models: plan 37.9 / 44.0 GiB against H-9's 40 GB task).
Option (contract change): the final ledger inherits calibration's three stores before the islands
(`core/cpp/v3_core.cpp:418-428`, `:728-738`), so the fit's cut-off is at least calibration's c-th value τ_cal. An island
that drops offers below τ_cal produces the same fit store. Its own file then holds "the top c of the offers ≥ floor".
It needs: τ_cal in `calib.bin`, the floor recorded in `island_r.bin`, a merge check `floor ≤ cut-off after tables and
inherited`, and a WP4 confirmation that no per-island output reads the tail of an island store.

**R4 (operations, medium). The store check.** Beyond its cost (§1.1): it is the only run-time proof of I1, so do not
drop it. Run it in parallel (same predicate over index ranges: `v4_bench_arch` has it) before every checkpoint and
before the final write.

**R5 (restart, medium). Restart becomes critical-path infrastructure.** With early stages of minutes each, a 10⁶ island
will not fit one 2-hour job unless R1 turns out mild. Then every island restarts several times. Today restart is
proven in unit tests only (T6 at small p, simulated kills). Needed before the 1M pilot: T6 by a real kill at 10⁵ on
NOTS, the resubmission chain in the WP5 driver, and a checkpoint whose checksum is not a serial byte loop (FNV-1a at
≈ 1 ns per byte: 10–13 s for a 10 GB store of π₀-sized models, each stage).

**R6 (integration, low–medium). `k_store` for the first calibration island.** `run_island` refuses p ≥ 10⁵ without
`k_store`, and only calibration measures it. The pilot island needs a declared source (for example the π₀ quantile the
plan already uses). One line in INTERFACES §7.

**R7 (arithmetic, low). Class-A values are path-dependent maxima.** A model reached by two flips can carry two class-A
values; the store keeps the larger and the HPM provenance is the first event *with that larger value*. This is
deterministic and T3-invariant. It should be written in INTERFACES §4.1, which still says "a model's value is a
deterministic function of S". If lever 6 or a class-A deletion score is wanted, decide before any V fixture or overlap
result is frozen: both change class-A bits.

**R8 (benchmarks, low). The benches use a stand-in partition (blocks of 4).** I checked the one place where the
production tables (≈ 7 GB) could hurt the kernel, the composite-table read per flip: 11–22 ns per flip, almost all of it
the block search, not the table (MEASURED, `v4_bench_arch comp 200000 14 64 3 {0,1}`). No action beyond vectorising
that sum with the flips (lever 7).

What I checked and found sound: the store determinism argument (WP3_DESIGN §1.3) including stale cut-offs and the
snapshot filter; the address map's injectivity; the event-key rule under one-offer-per-(support, label, pass); restart
equivalence (nothing thread- or pass-dependent is carried over a step boundary; the prototypes add no checkpointed
state); the two-generation checkpoint order after a resume.

## 4. Work split for builders 6 and 7

First, a file split so that three people do not edit one 1,100-line header: `island_impl.h` →
`island_run.h` (run loop, barrier, ledger sync, checkpoints), `island_lm.h` (the label-major round), `island_pm.h`
(the reference). WP3's builder does it in one mechanical PR before the others start.

| who | packages, in order | gate | depends on |
|---|---|---|---|
| **WP3 builder (stays)** | calibration roles with WP4 (critical path); the `island` command with the setup and calib readers; `k_store` for the pilot (R6); compat island | golden tests vs core | WP2 reader, WP4 runner |
| **Builder 6 — kernel cost, same bits** (owns `island_lm.h`) | K1 bounded scoring, bounded scan, one-particle phase B (from the prototype branch); K2 Philox multiply, inverse-only orders, I-step proposals in the order phase; K3 Gram rows with the slot allocator, the memory-plan term and G following the support size; K4 large supports (lever 7); K5 rolling admission | unchanged T3 hashes in both forms for every package; the NaN-row test (§2.1); `nots_bench_arch.sh` after K1 and K3 | the file split |
| **Builder 7 — island operations and T5** (owns `island_run.h`, `store.h`) | O1 parallel store check at checkpoints and final write (R4); O2 per-stage cost record in the island file's meta (R1); O3 leader stores with deferred parallel compaction, measured at 10⁶ (R2); O4 restart at scale: real-kill T6 at 10⁵, resubmission with WP5, parallel checksum (R5); O5 the T5 harness at 10⁵ and the 10⁶ early-stage probe; O6 the offer floor, if you decide it (R3) | T6; T5 numbers recorded; store tests | WP5 driver for O4, WP4 for O6 |

Decisions the split needs from you before day 1 of the new builders: lever 6 and class-A deletion scores (yes / no);
the offer floor (yes / no, with WP1 and WP4); the per-stage record fields (O2), so T5 produces what the re-size needs.

Order of value: O1 (one day, −19% of a late round) → K1 → O2 + T5 → K3 → O3 → K2 → K4 → K5.

## 5. SPR measurement to confirm (the manager submits; I have no NOTS access)

One job, one task, one socket. The script builds in the job, runs one island through its transient with a checkpoint,
then resumes each variant from that checkpoint for the two measured rounds and refuses unless all same-bits variants
print the same hash.

```
cd <clone of exp/P1M-wp3-arch, head>/Scripts/SMC_BVS/engine_v4
export TMPDIR=/scratch/fb31/SMC_Engineering_Department/tmp/<job>
sbatch --partition=commons --constraint=<Sapphire Rapids 8468> --nodes=1 --ntasks=1 --cpus-per-task=96 \
       --mem=72G --time=00:50:00 --wrap \
  "V4_BENCH_EARLY=1 tools/nots_bench_arch.sh /scratch/fb31/SMC_Engineering_Department/scratch/runs/wp3_arch/build"
```
(Use the same binding as job 2748756: the 96 CPUs of one socket and its memory.)

| step | what | ESTIMATE wall | expected result (ESTIMATE) |
|---|---|---|---|
| transient | π₀ → φ = 1 in one stage, 2 burn-in rounds, checkpoint | ≈ 10 min | — |
| `ref` | PR #26 behaviour, check on | 2.5 min | ≈ 24 s per round (240 ns·CPU per pair, as job 2749328); the `[arch]` line shows the check ≈ 5.7 s |
| `check` | check off | 2.5 min | ≈ 18.5 s (≈ 184) |
| `bounded` | lever 2 | 2.5 min | ≈ 14.3 s (≈ 141) |
| `gram` | + lever 3 (640 slots, + 5.1 GB) | 2.5 min | ≈ 12 s (≈ 120) |
| `fma` | + lever 6 (its hash differs by design) | 2.5 min | ≈ 11.5 s |
| early stages (`V4_BENCH_EARLY=1`) | N = G = 64, φ = 0.01, 0.02, 0.03, reference and `gram` (4,000 slots, 32 GB) | ≈ 2 min | reference ≈ 15–18 µs·CPU per step, `gram` ≈ 3.5–4 |

Cost: ≈ 25 min × 96 CPUs ≈ **40 core-h** (worst case 50 min × 96 = 80). Optional variants `g64` and `smt48` add ≈ 4
core-h each. A calibration-shaped island (R2) is a separate ≈ 20 core-h run: the same `island` line as job 2748756
with `V4_LEADERS=1`, after builder 7's O3, to compare with its top-store-only twin.

## 6. Evidence

All on Owls (owls.stat.rice.edu), builds under `/home/fb31/SMC_Engineering_Department/tmp/20261116-wp3arch/` (removed
at the end), `-DV4_TESTS=OFF -DV4_ISLAND_ISA=x86-64-v4`, `OMP_NUM_THREADS=3`, `nice -n 19`. Raw logs:
`Scripts/SMC_BVS/engine_v4/tools/arch_evidence/` on branch `exp/P1M-wp3-arch` (with a copy of this file).
`tools/nots_bench_arch.sh` was dry-run end to end on Owls at p = 2·10⁴ (exit 0, hashes identical across variants).

| claim | command | result |
|---|---|---|
| store check cost | `v4_bench_arch check 40000001 6 3` | serial 6.64 s (166 ns per entry); 3 threads 1.23 s |
| T3 hashes, small | `v4_bench_island island 20000 300 1,3 {A,bit} lm 64 128 geo:4 1 1` with and without `V4_NO_BOUNDED`, `V4_GRAM_SLOTS=24\|400`, `V4_FLIP_GROUPS=4` | A `263474601a55acb1`, bit `f9c6272ed1ffbae5` in every case (the PR #26 reviewer's hashes) |
| FMA keeps T3 | same with `V4_PRODUCTS_FMA=1`, `lm` and `pm` | both `e61f1491ddcfa372` |
| late 10⁶ rounds | `island 1000000 256 3 A lm 256 128 steps:1 2 2 200 4000001`, stopped after step 3 (`V4_CKPT`, `V4_STOP_AFTER=3`), then resumed per variant | round 5 wall: dense 47.06 s; bounded 39.94; + scan 34.03; + Gram rows 28.14 (hash `c2e25e70c7e6f5e9` in all four); + FMA 27.24 (`589ca76ee5d1a9a9`) |
| 10⁵ bridge | `island 100000 256 3 A lm 256 128 adaptive:30 2 2`, `V4_NO_BOUNDED=1` vs `V4_GRAM_SLOTS=4500` | 322.0 s vs 174.4 s, hash `925cfff768fd65af`; with `V4_LEADERS=1` 247.9 s |
| 10⁶ early stages | `island 1000000 24 3 A lm 24 128 steps:0.01,0.02,0.03,1 0 1 200 4000001`, stop after step 3 | §1.3 table; hash `0b26e3b8848270dd` in all variants |
| kernel vs k | `v4_bench_island kernel 100000 3 64 {6,20,50} {0,1} A 128` | §1.3 table |
| products, orders, π₀ draw, composite read | `v4_bench_arch products 80 2048 3`, `fy 1000016 3 4`, `comp 200000 14 64 3 {0,1}`; `v4_bench_island overheads 1000000` | block-4 0.067, FMA 0.045 ns per multiply-add; Fisher–Yates 19.7 → 15.6 ns per label with the Philox multiply (`overheads`), 14.7 → 12.9 with a 16-draw look-ahead (`fy`); π₀ draw 4.27 → 3.03 ms; composite 11–22 ns |

Limits of this evidence:
- Owls is a loaded Skylake with 3 threads; SPR ratios will differ, mostly in the memory-bound phases. §5 exists for that.
- The 10⁶ runs use N = 256 or 24 (one group). Per-pass costs are those of production; per-round costs that scale with
  the number of groups (131 passes at N = 2,500) are not exercised.
- Start law, partition and neighbours are the bench's stand-ins. The size of π₀'s supports drives R1 and is not the
  production value.
- The prototypes are not production code: no unit tests added, switches through environment variables, and the Gram
  rows are outside the memory plan. The `ref` variant of my build already contains lever 4.
- Lever 5, lever 7 beyond interleaving, and the offer floor are designs with estimates, not measurements.

## 7. Addendum (2026-11-16, later): the L5 SPR batch and WP2's real setup tables

Inputs: `results/WP3_L5_SPR.md` with the logs of job 2749328 (commit be24e9d), and WP2's 10⁶ counts (LOG 05:04 and
05:06). Where this section gives a number that differs from §0–§5, this section wins.

### 7.1 The L5 batch against the cost model

Now §1.1 (before and after, per phase) and the lever table of §2, which are rebuilt on the measured L5 numbers. Two
facts from it that matter here: the uncounted ≈ 5.7 s per step is unchanged by L5 and be24e9d still has
`check_store = true`; and the memory of the job was 19.5 GB steady after round 1 and 34.8 GB at the peak in round 1
(the store full of π₀-sized models), with ≈ 2.5 GB of stand-in tables. So the island without tables is ≈ 17 GB steady
and ≈ 32 GB at the peak.

### 7.2 Table lookups in phase A with production-sized tables (MEASURED, Owls)

Phase A reads one table entry per flip: the singleton code of the label, `logr[code_ptr[b] + (1 << pos)]`. With the
stand-in (32 MB) that entry sits in L2/L3. With blocks of 14 the table is 9.4 GB: the read is one DRAM cache line and,
on 4 KB pages, 0.43 page walks per label (MEASURED count: the singleton codes touch 18.8% of the table's pages,
1.63 GB). But the entry is the same for every support of the pass, and the supports are scored one after the other
inside a tile. So the miss is paid once per (label, tile visit), not once per flip.

`v4_bench_arch comp 1000000 14 <supports> 3 <scatter> <small_pages>` (the loop shape of phase A: tiles, then
supports, then labels), ns of thread time per (support, label) for the composite sum:

| supports that need the label | stand-in table | 9.4 GB table, huge pages | 9.4 GB table, 4 KB pages | with a singleton array |
|---|---|---|---|---|
| 64 | 10.7 | 14.7 | 13.2 | 9.3–9.5 |
| 4 | — | 29.5 | 27.6 | 9.6–10.0 |
| 1 | — | 73.6 | 88.6 | 9.8–10.4 |
| 64, labels scattered over blocks | — | — | 27.9 | 25.3 |
| 4, scattered | — | — | 61.6 | 22.0 |

- **Cost of the real table: 64–78 ns per (label, tile visit)**, divided by the number of supports that need the label.
- In the island:
  - reference code, ≈ 74 supports per pass: ≈ +1 ns per pair (under 1% of 240);
  - bounded scoring, late rounds (≈ 27 of 74 supports need a given label): ≈ +3 ns per flip, 1–2% of the round;
  - early stages (G·k limits the group to 24–64 supports, 7% of the labels needed): +14–46 ns on a flip of ≈ 1 µs.
- **So the real tables do not move any per-pair figure by more than ≈ 2%** (ESTIMATE from these measurements). The
  per-tile working set is unchanged: 128 table lines (8 KB) beside a 205 KB tile.
- The fix costs nothing: a p-indexed array `lr1[j]` of the singleton terms (8 MB, read sequentially). The sum is the
  same doubles added in the same order (checked: identical bit sums). It removes the miss and, more important, takes
  the 1.63 GB of singleton pages out of the island's hot set (7.3).
- The second column pair shows what the block search costs when a design's blocks are not contiguous in the label
  index (branch mispredictions: 25 vs 9.5 ns). AR and IND pack by minimum index, so they are on the first rows.

### 7.3 Island memory with the real tables (10⁶, n = 200, G = 256, 96 threads; GB)

Non-table part from 7.1: ≈ 17 steady, ≈ 32 at the peak (MEASURED minus the stand-in). Tables for IND at n = 200:
logr 9.25 (WP2), plus cond_cum ≈ 0.9, logF 0.06, neighbours ≈ 0.15 (ESTIMATE): ≈ 10.4 in `setup.bin`.

| how the island holds the start law | tables in memory | island peak | task request (peak + 15%) |
|---|---|---|---|
| (a) today: `dep::Start` (nested vectors, a flat copy of logr, stored sampler tables) | 26–35 (2.5–3.4 × setup.bin, WP2); 37.9 at IND n = 1,000 | ≈ 58–67 | ≈ 68–78 |
| (b) WP2's flat `setup::Start`, read into memory | ≈ 10.4 | ≈ 43 | ≈ 48–50 |
| (c) flat `setup::Start` as a read-only file mapping, with the hot arrays copied: `lr1` (8 MB), `blk`/`pos` (8 MB), the π₀ scan table (58 MB at n = 200, 286 MB at n = 1,000), neighbours | ≈ 1 resident in late rounds (ESTIMATE); the rest is page cache the kernel may drop | ≈ 33.5 | ≈ 40 (H-9 holds) |
| (c) with Gram rows (+5.1), inverse-only orders (−1.0) | | ≈ 37.6 | ≈ 44 |
| (c) with those and the offer floor of R3 (store peak ≈ −12, ESTIMATE) | | ≈ 26 | ≈ 30 |

- Without `lr1`, layout (c) touches 1.63 GB of logr in every pass; those pages must stay resident.
- What stays cold in (c): logr is then read only for labels in a block that meets a support and for π₀ draws. Late
  rounds: at most a few thousand distinct blocks × 131 KB (ESTIMATE ≤ 0.7 GB). Early stages touch most blocks over time,
  one cache line at a time; under memory pressure the kernel drops and re-reads them.
- cond_cum (4.5 GB at n = 1,000): the island needs only the selected rows of a draw and the scan table of first
  entries P(k_b = 0 | r). If the island builds the scan table by reading cond_cum it touches all of it once. Have
  WP2 write the scan table into `setup.bin`, or build it from logF and logprof (same function, same bits), so that
  cond_cum can go on demand as WP2 proposes.
- Two islands of one node map the same file. Its pages live on the socket of whichever island touched them first. With
  the hot arrays copied into each island's own memory this does not reach phase A.
- **The admission plan** counts the caller's `inputs_bytes` in full: with real tables it prints ≈ 53 GiB for this
  configuration (45.1 − 2.5 + 10.4), so a 40 or 48 GB task is refused before it starts. Decide one rule: either the task
  request follows the plan (≈ 56 GB), or the plan counts hot table bytes and reports mapped, droppable sections on a
  separate line. I recommend the second with layout (c).

### 7.4 What changes in the recommendations

1. Lever 1 (the store check) is confirmed on SPR: ≈ 56 ns·CPU per pair, the difference between 1.23× and ≈ 0.92× of
   the plan. It is a one-day change (builder 7, O1): do it before the next SPR batch.
2. New package for the WP3 builder, with the flat-Start reader: layout (c), `lr1`, the scan table from `setup.bin` or
   from logF, and the two plan lines. No output change.
3. The memory order of work for the island task: flat Start (−16 to −25 GB) → offer floor (−12) → Gram rows (+5).
4. The benches should take a table-size option (blocks of 14 with synthetic values, as `v4_bench_arch comp` does) so
   that SPR numbers include the real footprint from now on.

## 8. Addendum: per-stage re-size of one V-1M fit (R1)

Inputs: the SPR job of my script (`results/WP3_ARCH_SPR.md`, job 2749483), the two G0 stage records (real partition,
real start law, calibrated grids: `records/G0/stage_2747799` p = 5,000, 16 islands; `stage_2747372` p = 10,000,
8 islands), and the 10⁵ bridge of §1.3. The production E_π₀|S| at 10⁶ is not in yet, so everything is given for
E₀ = 10, 25, 56. The model is `tools/arch_resize_model.py` on the branch (standard library only; it prints the tables
below). **Every core-h figure in this section is an ESTIMATE built from the MEASURED anchors listed.**

### 8.1 What the G0 records say about the schedule and M (MEASURED)

| | p = 5,000 (T = 36) | p = 10,000 (T = 28) |
|---|---|---|
| M at stage 1 → lowest → last stage | 7.0 → 4.1 → 5.5 | 4.9 → 4.1 → 5.5 |
| M in the 12 terminal rounds | 5.47–5.53 | 5.50–5.56 |
| mean M over the island | 5.6 | 5.0 |
| of which Gibbs changes / N-swap / independence acceptances per particle-round, stage 1 | 3.5 / 1.6 / 0.83 | 1.9 / 1.1 / 0.86 |
| stages with φ ≤ 0.2 / ≤ 0.4 / ≤ 0.6 / all | 7 / 29 / 31 / 36 | 2 / 22 / 23 / 28 |
| π₀-like share of the population, mean over the stages | 0.21 | 0.36 |

- M = 1 + accepted state changes per particle-round. "π₀-like share" = the acceptance rate of the independence step,
  normalised by its value at stage 1: it falls to zero at φ ≈ 0.30 (5k) and 0.34 (10k).
- **In the real method M is nearly flat, 4 to 7, over the whole calibrated schedule, and 5.5 in the terminal rounds
  at both sizes.** The plan has 3; the bench's stand-in at 10⁶ has 3.9 in late rounds.
- **A calibrated grid puts about 80% of its stages at φ ≤ 0.4**, most of them packed around the point where the
  population leaves π₀. The stages where part of the population is still π₀-like are 20 of 36 and 14 of 28.
- These runs do not record support sizes. Their M at stage 1 (7.0 and 4.9) is close to their late M (5.5), so the
  π₀-like stages cost no more sweeps than the late ones there; by the stand-in relation of 8.2 that corresponds to
  E₀ of at most ≈ 10–16. Whether that holds at 10⁶ is what WP2's number decides.

### 8.2 The model

One fit = 16 final islands + calibration = 3 island-equivalents (your figure), each of N = 2,500, p = 10⁶,
T = 120 bridge stages + 8 + 4 rounds, 2.5·10⁹ steps per round. The plan is 600 ns·CPU per step: 55 core-h per island.

**Per stage t**, with w_t the π₀-like share:
- support size k_t = 6 + (E₀ − 6)·w_t; sweeps M_t = M_late + (M₀ − M_late)·w_t with M₀ = max(M_late, 1 + 0.37·E₀).
  - 6 = late mean |S| (MEASURED in every 10⁶ run). 0.37: MEASURED on the stand-in (M = 10.1 at E₀ = 24; 21–22 at 56).
  - w_t: three profiles, each stretched to 120 stages (the refinement m keeps the distribution over φ): the two G0
    grids and the 10⁵ stand-in bridge (mean share 0.21, 0.36, 0.43).
  - M_late: 3.9 (stand-in at 10⁶) or 5.5 (G0); both are tabulated.

**Cost per step, ns·CPU (SPR, one socket, 96 threads):**

| term | today (be24e9d) | levers 1–3 | source |
|---|---|---|---|
| kernel | M_t × (164 + 12.8·(k_t − 6)) | flips 142 + 27.7·(k_t − 6); products 32·(M_t − 1); build 300·(M_t/20)·(k_t/55)³; phase B 60 + 2,000 × offers; orders and walk 85 | MEASURED at k = 6 (late round 5: 180 and 116 per pair) and at k = 55, M = 20 (early stage 3: reference 790 per pair; `gram` phase A 2,100, build ≈ 300 per step); linear in k between them |
| store check | 220 | 0 | MEASURED: 23.90 − 18.18 s per round |
| compaction | merges × seconds × 38.4, merges = offers × 2.5·10⁹ / 1.15·10⁷, seconds = 0.8 + 0.0146·(26 + 4·k_t) | same; − 0.9 s per merge with the sort fix (m3) | 1.15·10⁷ staged entries and 1.6 s per compaction MEASURED at stored \|S\| 6–8.5; the growth with model size is an ESTIMATE |
| calibration islands | + 0.33 µs of wall per top-store offer (serial leader stores) | compaction × 2 (leader stores made parallel, O3) | MEASURED: 157 s for 355·10⁶ offers, 39 s for 180·10⁶ (leaders island, rounds 1–2) |

The model reproduces the two late rounds it is anchored on: 921 vs 918 measured (today), 453 vs 452 (levers 1–3).

**Offers per step in a bridge stage** is the least known input. Central 0.03, bracket 0.01–0.10.
- MEASURED analogues: 0.14, 0.07, 0.03, 0.01 in rounds 1–4 of the φ = 1 transient at N = 2,500; 0.18 on the 10⁵ bridge
  at N = 256, which is 1.1 store capacities per stage or 39% of what a fully new population would insert.
- The same 39% at N = 2,500 and 10⁶ is 0.03 per step (two capacities per stage). Late rounds: 0.005 (MEASURED).
- The early-stage runs of job 2749483 cannot pin it: with N = 64 a stage offers barely more than one capacity.
- With the offer floor (D-29) the final islands' bridge stages are taken at the late rate; calibration islands keep
  their full traffic, because they build the stores that define the floor.

### 8.3 Core-h per 1M fit (ESTIMATE; central [low, high]; H-10 has 1,188)

Central = mean over the three stage profiles at 0.03 offers per step. Low and high = the extremes over the profiles
and the offer bracket.

**Late M = 3.9 (bench stand-in at 10⁶)**

| E_π₀\|S\| | state | fit, core-h | × H-10 | 16 islands | calibration | mean M | a π₀-like stage, ns·CPU per step: kernel + compaction |
|---|---|---|---|---|---|---|---|
| 10 | today's code | 2,575 [1,916, 4,699] | 2.2 | 1,965 | 610 | 4.1 | 1,231 + 442 |
| 10 | levers 1–3 | 1,579 [993, 3,576] | 1.3 | 1,244 | 335 | 4.1 | 576 + 442 |
| 10 | levers 1–3 and the sort fix | 1,159 [848, 2,192] | 1.0 | 938 | 221 | 4.1 | 576 + 216 |
| 10 | + offer floor | **895** [797, 1,168] | 0.8 | 675 | 221 | 4.1 | 526 + 36 |
| 25 | today's code | 4,136 [2,791, 7,051] | 3.5 | 3,280 | 857 | 5.8 | 4,389 + 661 |
| 25 | levers 1–3 | 2,029 [1,219, 4,551] | 1.7 | 1,607 | 422 | 5.8 | 1,182 + 661 |
| 25 | levers 1–3 and the sort fix | 1,609 [1,074, 3,167] | 1.4 | 1,302 | 307 | 5.8 | 1,182 + 436 |
| 25 | + offer floor | **1,264** [1,013, 1,749] | 1.1 | 957 | 307 | 5.8 | 1,132 + 73 |
| 56 | today's code | 9,937 [5,962, 15,250] | 8.4 | 8,165 | 1,772 | 9.3 | 17,656 + 1,114 |
| 56 | levers 1–3 | 3,044 [1,730, 6,677] | 2.6 | 2,430 | 614 | 9.3 | 2,736 + 1,114 |
| 56 | levers 1–3 and the sort fix | 2,624 [1,585, 5,293] | 2.2 | 2,125 | 499 | 9.3 | 2,736 + 889 |
| 56 | + offer floor | **2,112** [1,503, 3,060] | 1.8 | 1,613 | 499 | 9.3 | 2,686 + 148 |

**Late M = 5.5 (G0, real data at 5k–10k)**, central values: E₀ = 10: 2,991 / 1,655 / 1,234 / **971**; E₀ = 25:
4,511 / 2,091 / 1,671 / **1,327**; E₀ = 56: 10,404 / 3,107 / 2,687 / **2,175** (same four states). The late M moves
today's code by 4–16% and the lever states by 2–8%: after bounded scoring the cost hardly depends on M.

How to read it:
1. **Today's code does not fit H-10 at any start-law size**: 2.2× at E₀ = 10, 8.4× at 56. Even with small supports the
   sum of M ≈ 4–5.5 instead of 3, the store check, the bridge compaction and the serial leader stores is ≈ 2×.
2. **Levers 1–3 with the sort fix reach H-10 at E₀ = 10 (1.0×) and miss it by 1.4× at 25 and 2.2× at 56.**
3. **With the offer floor: 0.8× at E₀ = 10, 1.1× at 25, 1.8× at 56.** So H-10 holds if the production start law has
   supports up to about 20 members; at 56 one fit costs about two.
4. Where the remainder is at E₀ = 56 with all of it: a π₀-like stage costs 2.7 µs·CPU per step (flips on 56-member
   supports 1.5, new Gram rows 0.7, support builds 0.3), and calibration is 24% of the fit (its islands keep the full
   store traffic). Lever 7 of §2 addresses
   the first; a floor for the later calibration rounds would address the second and needs its own argument.
5. The offer rate is worth a factor 0.6–2.3 on the lever states and almost nothing once the floor is in. The floor is
   therefore also what makes the re-size predictable.
6. Not in these figures: setup, merge, tail and evaluation; the memory-driven task shape of §7.3; lever 5.

### 8.4 The single most valuable measurement

**The calibration pilot island at 10⁶ on the production `setup.bin`** (pilot rule, N = 2,500, H = 512), with the
per-stage record: wall by phase, mean |S|, M, flips per step, offers buffered, compactions and their seconds.
- It gives, at the target size and with the real start law and neighbours, the three curves the model takes from
  elsewhere: M(φ) and |S|(φ) (now from a stand-in and from 5k–10k) and the offers per stage at production N (now a
  bracket of 10×). With the calibrated grid's stage positions, 8.2 then has no free input.
- It is the first task of any 1M fit, so the code path is the production one; if the configuration is already the
  frozen one, the run is not spent.
- Cost (ESTIMATE from the model: ≈ 20 pilot stages + 12 rounds, one calibration-shaped island): **≈ 50 / 70 / 145
  core-h with today's code at E₀ = 10 / 25 / 56**, and ≈ 27 / 34 / 50 with the lever switches of the prototype build.
  One socket, ≈ 56 GB with the real tables (48.6 GB MEASURED for the calibration shape with stand-in tables).
- It needs the island to read WP2's flat Start and the pilot role, which WP3 has as its next items. Nothing else of
  the pipeline (calibrate loop, merge, evaluation) is needed.
- T5 at 10⁵ stays necessary as the end-to-end gate, and it will give the calibrated grid's shape. It cannot replace
  this: at 10⁵ the stand-in start law is half the size it is at 10⁶ (24 vs 56), and the question is the 10⁶ size.
- Until then, the cheapest useful number is WP2's E_π₀|S| itself: read the row of 8.3.

### 8.5 Limits of this model

- The k and M of a stage are interpolated with one weight; the cost between k = 6 and k = 55 is taken linear. The Owls
  kernel at k = 20 (§1.3) is 22% below that line, so the model overstates mid-sized supports. The split of phase B into
  60 + 2,000 per offer is an ESTIMATE.
- The early anchors are from N = 64 runs; I use thread time, not wall, for the phases that wait on one particle there.
  The manager's wall-based figure without compaction is 4–5 µs·CPU per step against my 2.7 at production N.
- M₀ = 1 + 0.37·E₀ comes from the stand-in. G0 has a larger share of non-Gibbs acceptances than the bench.
- Calibration is taken as three final-island equivalents. Its islands run pilot-length schedules with leader stores;
  only the leader term is modelled separately.
