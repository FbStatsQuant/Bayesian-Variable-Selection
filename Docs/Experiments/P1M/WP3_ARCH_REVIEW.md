# WP3_ARCH_REVIEW — cost architecture of the island at 10⁶, design risks, builder split

**WP3 architect (Fable 5.2, high), 2026-11-16. For the Engineering manager.**
Brief: `briefs/BRIEF_fable_wp3_architect.md`. Prototypes: branch `exp/P1M-wp3-arch` (3 commits on top of
`exp/P1M-engine` + PR #26 head `5c8ab8a5`; prototypes only, no PR). Every number is labelled MEASURED (machine, command
in §6) or ESTIMATE. "Owls" = Xeon Gold 6148, gcc 11.5, `-march=x86-64-v4` for the island sources, 3 threads, `nice -n 19`,
machine load 21–29 during the runs. "SPR" = NOTS Sapphire Rapids, job 2748756 unless stated.

## 0. Summary

1. **Late 10⁶ rounds can go well under the plan.** Measured 287 ns·CPU per pair (job 2748756). L5 as built, the
   store check moved off the step path, bounded scoring and Gram-row reuse together give **≈ 105 ns·CPU per pair**
   (ESTIMATE on SPR; plan 200). On Owls the same two late rounds of a 10⁶ island went from 47.1 s to 28.1 s (−40%) with
   an identical output hash (MEASURED).
2. **About 19% of a late round is a serial debug check that no counter shows.** `check_store` is on by default and
   verifies the whole store after every step: 6.6 s per step at 4·10⁷ entries (MEASURED, Owls). WP3's time split read it
   as per-pass overhead, so the L5 estimate (215) still contains it.
3. **The late-round figure is not the cost of a fit.** No SPR run so far has measured a bridge. Early bridge stages
   carry π₀-sized supports and many sweeps per particle. At 10⁶ with the stand-in start law a step costs
   **13–16 µs of thread time, about 25× a late round and about 45× the plan** (MEASURED, Owls). The prototype brings
   that to 3.1–3.6 µs (÷ 4, identical state hash). It cannot bring it to the plan: an exact flip score on a support of
   k unshared columns needs k·n multiply-adds. The 1M budget must be re-sized from a per-stage profile (§1.3, §3 R1).
4. Two more design risks: calibration islands carry leader stores that compact serially (+42% at 3 threads, MEASURED),
   and the top store is rewritten about once per bridge stage (§3 R2, R3).
5. The SPR confirmation is one job of ≈ 40 core-h (§5).

## 1. Cost model

### 1.1 A late 10⁶ round on SPR (MEASURED, job 2748756, round 5, G = 256, 96 threads on one socket)

Wall 29.06 s for 9.72·10⁹ (support, label) pairs = 287 ns·CPU per pair = 1,116 ns·CPU per step (M = 3.89). From the
`[island]` and `[round]` lines of `results/levers_2748756/socket1.log`:

| part | wall s | share | ns·CPU per pair | nature |
|---|---|---|---|---|
| phase A: products | 4.5 | 15% | 44 | core throughput; hyperthreads add nothing (49.5 → 98.8 ns thread-time from 48 to 96 threads, job 2748105) |
| phase A: flips, odds, uniform scan | 6.5 | 22% | 64 | throughput |
| store invariant check (in no counter; ESTIMATE as the residual) | ≈ 5.5 | 19% | ≈ 54 | **serial**, once per step |
| walk | 3.5 | 12% | 35 | latency: one π₀ draw (59 ms on Owls before L5) holds every pass |
| build | 3.1 | 11% | 31 | serial zero-fill of the score rows per group (before L5) |
| orders | 2.9 | 10% | 29 | throughput, random memory access |
| phase B | 1.9 | 7% | 19 | throughput, memory-bound |
| compaction | 0.7 | 3% | 7 | |

- The check is the residual: the counted phases sum to ≈ 23.3 s. The residual is 4.3–6.6 s in every round of both
  islands (G = 64 and G = 256, 131 to 845 passes), so it is per step, not per pass. The check alone costs 6.64 s at
  c = 4·10⁷, k = 6 on Owls (MEASURED, `v4_bench_arch check 40000001 6 3`; 166 ns per entry: one random index lookup each).
- A linear fit of phase A over the two islands (ESTIMATE from two MEASURED points) gives ≈ 9 ms of wall per pass that
  does not depend on the pairs: 1.2 s per round at 131 passes.

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

Expected gain = late 10⁶ round on SPR, ns·CPU per pair-equivalent, baseline 287 (ESTIMATE unless marked). "Same bits"
= the output hash is unchanged, checked on Owls in both arithmetic forms where it applies.

| # | lever | output | expected on SPR | MEASURED on Owls | state |
|---|---|---|---|---|---|
| 0 | L5 as built by WP3 (PR #26) | same bits | −72 (WP3's estimate) | π₀ draw 60 → 4.3 ms, round order 40 → 20 ns per label | built |
| 1 | store check: parallel, and only before a checkpoint or the final write | same bits | **−54** | 6.64 s per step serial; 1.2 s with 3 threads | one-day change |
| 2 | bounded scoring: score a (support, label) only if a particle can still consume it; bounded uniform scan; one-particle phase B | same bits | **−30 to −35** | late 10⁶ round 47.1 → 34.0 s; flips 3.83 → 1.37 per step | prototype |
| 3 | Gram rows of active columns kept across passes | same bits | **−20** | 34.0 → 28.1 s; products 31 → 15 thread-s; early 10⁶ stages ÷ 4 with #2 | prototype |
| 4 | Philox 32×32 multiply (`vpmuludq` instead of the 64-bit lane multiply) | same bits | −3 | round order 19.7 → 15.6 ns per label; π₀ draw 4.27 → 3.03 ms; a 16-draw look-ahead adds −12% | prototype |
| 5 | rolling admission: a finished particle's slot goes to the next particle, so every pass stays full | same bits | −15 | not built (from the 9 ms per pass of §1.1 and ≈ 45 passes per round instead of 131) | design |
| 6 | FMA in the class-A products | **other class-A bits**; label-major = particle-major kept | −5 to −8 | products 15.3 → 12.4 thread-s; kernel 0.067 → 0.045 ns per multiply-add | prototype; your decision |
| 7 | large supports: full 8-label groups across tiles, several groups per flip call, deletion scores from the cached Gram | same bits | small late; ≈ ÷ 1.5–2 on early stages | interleaving alone: no gain (most calls hold 1–2 groups) | design |
| 8 | offer floor from calibration (§3 R3) | **island file content changes**; fit identical | −5 late; −10 to −20% of a bridge stage; −10 to −15 GB | compaction = 30% of the prototype's 10⁵ bridge | needs a contract decision |

Levers 0–4 together: 287 → **≈ 105 ns·CPU per pair-equivalent ≈ 410 ns·CPU per step** at M = 3.89 (ESTIMATE; plan 600
per step at M = 3). The M risk of H-9 is then absorbed in late rounds: the cost no longer scales with M, because
the flips per step stay near 1.0–1.5 whatever M is.

How the ESTIMATE is built: SPR phases after L5 (WP3's deltas), minus the check, with the Owls ratios applied to
phase A (20.4 / 37.5) and phase B (4.3 / 6.2): 6.0 + 1.3 + orders 1.2 + build 0.9 + walk 0.3 + compaction 0.7 + 0.2
≈ 10.6 s per round.

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

- **Late rounds: yes**, ≈ 105 (ESTIMATE), to be confirmed on SPR (§5).
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
| `ref` | PR #26 behaviour, check on | 2.5 min | ≈ 21–22 s per round (215 ns·CPU per pair); `[arch]` line shows the check ≈ 5 s |
| `check` | check off | 2.5 min | ≈ 16.5 s (163) |
| `bounded` | lever 2 | 2.5 min | ≈ 12.5–13 s (≈ 126) |
| `gram` | + lever 3 (640 slots, + 5.1 GB) | 2.5 min | ≈ 10.5–11 s (≈ 105) |
| `fma` | + lever 6 (its hash differs by design) | 2.5 min | ≈ 10–10.5 s |
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
