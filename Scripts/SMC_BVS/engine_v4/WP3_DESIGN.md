# WP3_DESIGN — the island: stores, addressed sampling, label-major round, restart

**v0.1, 2026-11-15, WP3 builder (Opus 5.5). Status: PROVISIONAL, for design review.** Branch `exp/P1M-wp3-island`
(stacked on WP1's PR #11). Inputs: ENGINEERING_SPEC §0-v2, §3, §6; INTERFACES v0.1.3 (v0.1.5 announced: RNG domain and
event key); Sol EXP-CP1 review §F2, §F4, §F5 (T3, T6); manager directives of 11-15 (D-21 scope cut, G ≤ 256, mem budget).
Code references: `include/v4/island/*.h`, `src/island/island_impl.h`, `tests/test_island*.cpp`. Every number below
is labelled MEASURED (Owls, command given) or ESTIMATE.

**What exists and passes today** (Owls, gcc 11.5, 3 threads, `v4_tests`: 41 cases, 0 failures, in the default build
and in an `x86-64-v4` build):
- particle-major island, bit form, **bit-identical to `core/` `v3::Engine::run_island`** (core compiled unchanged, fed the
  same addressed uniforms through an adapter): log Ẑ, stage table, moves, distinct counts, init hash, HPM + provenance,
  island_best, every logical counter, the top store; RB/PIP to 1e-12 (declared fixed-point reduction, §3.6);
- label-major island in bit form and class A, identical output hash to the particle-major island of the same arithmetic
  for threads 1–3, G ∈ {1, 7, 16, 48}, tiles 64–256 (T3); restart from checkpoints after 6 different steps with changed
  threads/G/kernel (T6); flip kernels 0 mismatches of 16,000 (bit) / ≤ 7.8e-16 relative (class A vs bit).

Under D-21 the bit-form label-major kernel is **not part of the deliverable**: T runs particle-major. The code exists
and is tested; §5 Q1 asks whether to keep it as a test-only path or delete it.

---

## 1. Deterministic stores under threads

### 1.1 Data structures (`include/v4/island/store.h`)
| object | owner | content | bound |
|---|---|---|---|
| `TopStore` (island) | one per island process | kept run: sorted arrays `v, hash, off, len` + `pool` (HPM order, value F); hash index (open addressing, u32 slot = entry+1); staging run (`StoreBuffer`); atomic `tau` | kept ≤ c = 40p + 1; staging ≤ max(c/4, 4096); index 2c…4c slots |
| `StoreBuffer` (offer buffer) | one per worker thread | appended (v, hash, len, off) + pool | ≤ `buf_limit` = 65,536 entries (INTERFACES v0.1.2) |
| `ThreadLedger` (tally) | one per worker thread | logical[N_PHASE][N_MECH], island_best, HPM candidate (S, F, log m, EventKey, phase, mech), MoveStats, its `StoreBuffer` | O(K + buf_limit) |
| island `master` tally | one per island | the absorbed tallies | O(K) |

### 1.2 Algorithm
- **offer(v, S, h)** (worker, hot path): `if v < tau: drop` (relaxed atomic load; ties kept); else append to the worker's
  buffer; if the buffer holds `buf_limit` entries → **flush**.
- **flush(buffer)**: take the island mutex; append the buffer to the staging run; clear the buffer; if staging ≥
  `stage_limit` → **compact** (still under the mutex).
- **compact()**: (1) sort staging by (hash, |S|, S, v desc) and keep the first entry of each model (its largest value);
  (2) look each one up in the kept run through the hash index: if the kept copy has a value ≥ the staged one, drop the
  staged one, else mark the kept copy dead (class A only: one model can carry two path values, §3.7); (3) sort the
  survivors under the store order; (4) linear merge of kept (skipping dead) and survivors, stop at c; (5) rebuild pool
  and index; (6) `tau ← v[c−1]` if c entries are kept, else −∞ (release store). Cost O(c + s log s).
- **absorb protocol** (INTERFACES §4.2 / §7(4)): at every step boundary (after init, after every bridge stage, every
  burn-in and measured round) and before any read or checkpoint, the island flushes each thread's buffer and merges its
  tally **in thread-index order**, then calls compact(). The kernels run only between step boundaries, so the absorb
  is single-threaded.

### 1.3 Why the content is deterministic (independent of threads, schedule, flush timing, merge order, G, tiles)
Define Ω = the multiset of (model, value) offers of the step so far. Claim: after compact(), kept = top-c (under the
strict store order) of {(S, max value of S in Ω)}. Proof sketch:
1. Without drops, compact() computes exactly that set: dedupe-by-max then truncation commute with union
   (top_c(top_c(A) ∪ B) = top_c(A ∪ B) for a strict total order on distinct models, and max is associative).
2. **Drops never change it.** A drop at time t has v < tau_t, where tau_t = the value of the c-th of c distinct kept
   models at t. Values per model only grow, and kept models only get replaced by better ones, so the final c-th value
   is ≥ tau_t > v. If S ends in the final top-c its final value ≥ tau_t > v, so v was not its maximum; if S does not,
   the offer is irrelevant. Equal values (v = tau_t) are never dropped because the tie order (|S|, lex) may admit them.
3. `tau` is read stale by other threads: a stale tau is ≤ the current one, so a stale read only drops less.
Tally merge: counters by sum, island_best by max, HPM by (F desc, |S| asc, lex asc, EventKey asc) — a strict total
order on events, so the max is order-free; for one model the smallest EventKey wins (= core's "first score" rule).

### 1.4 The one-worker-supplies-all-winners case (Sol F2)
Nothing in the design partitions capacity by worker: buffers are bounded only in **entries in flight**, and a full
buffer is flushed into the single island store. If worker 0 offers all c winners and the others only losers, worker 0
flushes ⌈c/65,536⌉ times; content = top-c. Test (to add, `store_one_worker_all_winners`): 3 threads, c = 10⁵; thread 0
offers the c best of 3c models, threads 1–2 offer the rest interleaved; compare with WP1's `v4::Store` reference and
with a serial run (both orders). Existing tests: `store_order_free_multithread` (caps 1…10⁵, buffer limits 1/37/10⁵,
1 and 3 threads, permuted order, value ties, two-value models) and `store_equals_wp1_reference_store`.

### 1.5 Peak-live memory of the store path (ESTIMATE; formula exact in entries)
Entry = 8 v + 8 hash + 8 off + 2 len + 4k pool bytes = 26 + 4k B. Let c = 40p + 1, s = stage_limit = c/4, T = threads.
- kept run c entries; during compaction a new kept run (≤ c) + staged refs (s × 32 B) + dead flags (c B) + index
  (≤ 4c × 4 B): **peak ≈ 2c entries + 1.25c × 32 B + 16c B** plus staging s entries.
- per worker: buf_limit entries (65,536 × (26 + 4k) B ≈ 3.5 MB at k = 7, 28 MB at k = K = 100).
At p = 10⁶, k = 7 (c = 4·10⁷): kept 2.2 GB, peak ≈ 2.2 + 2.2 + 0.55 (staging) + 1.6 (refs) + 0.64 (index) ≈ **7.2 GB**,
workers 48 × 3.5 MB = 0.17 GB. At the admission bound k = K = 100 the per-entry size is 426 B: c × 426 B = 17 GB kept —
**the store cannot be admitted at K-sized supports at 1M**; the admission check (§1.6) uses the pool's actual size, so
it refuses on growth with a named reason rather than OOM. (Q4 asks for the policy.)
MEASURED (Owls, `v4_bench_island store 4000001 3 2e7`): fill 2.1 µs per accepted new model, mixed traffic (90 % below
tau, 10 % duplicates of kept models) 213 ns per offer — the duplicates dominate: each costs a compaction share. At
p = 10⁴ islands, 5 % of consumed flip events pass tau (MEASURED, 53.7 M of 1.05·10⁹). Lever (Q5): a worker-side
duplicate filter against an immutable snapshot of the index.

### 1.6 `--mem-budget` admission (to implement; manager item 3)
`island_memory(cfg, p, n, K)` sums, before any allocation: X tiles (n·p·8, a second tiled copy), store peak (§1.5 with
k = the running mean support size, re-checked at every compaction with the real pool size), staging, index, worker
buffers (T × buf_limit × (26 + 4k)), RB accumulators (16 B × p × 2: current round and total; particle-major: + T × 16 p),
group buffers (G × m × 4 B × 2 for orders + inverses; nsup × p × 16 B for the per-support score and odds rows;
|A| × n × 8 gathered columns; T × |A| × tile × 8 products), particles (N × (k × 4 + 48) × 2), checkpoint serialisation
(the byte image ≈ store + particles + 16 p, written from a buffer: Q6). Refusal: status `resource_limit`, reason
`"mem_budget: <component> <bytes> > budget"`, deterministic (a function of the configuration and of the run's own
state at a step boundary). Config checks: **G ≤ 256** (manager item 2), tile multiple of 64, N ≥ 1, grid strictly
increasing from 0 to 1, B ≥ 0.

---

## 2. Addressed sampling

### 2.1 Address map (INTERFACES §3; Philox4x32-10, key = {seed, role<<28 | tier<<26 | iter<<20 | island},
counter = {slot, position, particle, xph<<24 | stage}); `particle` is always the **destination** index 1…N
| consumer | xph | stage | particle | position | slot | code |
|---|---|---|---|---|---|---|
| initial π₀ draw of particle i | INIT | 0 | i | 0 | 0…u−1 in the documented order: size, block sizes J…1, submodels 1…J | `run()` init |
| resampling uniform i at stage t | RESAMPLE | t | i (the i-th draw of `resample`) | 0 | 0 | `resample()` |
| round order, Fisher–Yates step t = m−1…1 | BRIDGE / BURN / MEASURED | t / l / h | i | 0 | m−1−t | `draw_order()` |
| Gibbs label at position q | as round | as round | i | q | 0 | phase A (label-major), `pm_round` |
| U swap at q | as round | as round | i | q | 0 j, 1 l, 2 accept | `step_nongibbs` |
| N_b swap at q | as round | as round | i | q | 0 j, 1 l, 2 accept | `step_nongibbs` |
| I at q | as round | as round | i | q | 0…u−1 the π₀ draw, `SLOT_ACCEPT` = 0xFFFFFFFF accept | `step_nongibbs` |
**Destination rule.** After resampling, particle i is a copy of ancestor a_i, but every later uniform uses address
particle = i (its destination), stage/round = the current one: no stream state is inherited (production stores no
generator state at all). **Injectivity.** (xph, stage) identifies the phase and the stage/round; position 0 within a
round phase is the order draw only, positions 1…m are the steps; within a step the slot is the ordinal of the uniform
in that step's documented order (variable-length π₀ draws included, u ≤ 1 + 2J < 2³²−1, so they never reach
SLOT_ACCEPT); INIT and RESAMPLE have their own xph. The key separates role/tier/iter/island. Hence distinct consumers
get distinct counters. Widths: island < 2²⁰, iter < 64, tier < 4, stage/round < 2²⁴, particle < 2³², position ≤ m =
p + B + 2 < 2³², slot < 2³²; WP1's `address_key/ctr` throw on overflow. Final islands: role FINAL, tier = iter = 0.
I5 is checked by WP1's `CheckedSource` in tests (to wire; the island currently calls `uniform_at` directly).
**v0.1.5** will add Sol's slot taxonomy (order / resampling / categorical sizes / submodels / acceptances); the island
code computes every address in four functions (`addr`, `draw_order`, `step_nongibbs`, init), so adopting a new map is
local. Any map change changes the trajectories (law-equivalent, class L) and the golden adapter changes with it.

### 2.2 Event key (provenance) and logical counts
EventKey = (seg = FINAL, tier, iter, unit = r, xph, stage, round, particle, position, sub). Today `sub` = 0 for every
event; v0.1.5 (Sol F4) adds the within-step ordinal: proposed **sub = 0 held, 1 flip (Gibbs); 0 the proposal (U/N/I);
0 init**. Held events are never offered, so the HPM key of a Gibbs flip is (…, q, 1). The serial traversal across
units (tables → inherited → islands → final LS → LS0) is the merge's (WP4) concern; inside an island the key order
equals core's serial order (particle-major) — golden-tested on provenance.
Logical counts, by mechanism (fixes spec I4, Sol F4): per particle-round, `gibbs_held` = p (every Gibbs step);
`gibbs_flip` = p − #(additions refused at |S| = K); `uswap` = 1 − self-loops; `nswap` = B − self-loops − empty N(j)\S;
`indep` = 1; `init` = N once. Test `logical_counts_and_invariants` checks held = N·p·rounds and the U/N/I identities;
the flip identity check is to add.

---

## 3. The label-major round (class A for V; spec §3 rules 1–4)

### 3.1 Notation
m = p + B + 2 labels; particle i has round order ord_i and inverse inv_i (1-based positions); its state at the start of
pass r is (S, log m, lg0, d) and its consumed prefix is positions 1…q_i.

### 3.2 Group formation and buffers
Particles [g0, g0 + G) in index order, **G ≤ 256** (memory: orders + inverses 2 G m × 4 B = 2 GB at 10⁶, G = 256; the
per-support rows nsup × p × 16 B ≤ G × 16 MB = 4 GB at 10⁶: **G = 64 at 10⁶**, Q3). Groups are processed one after the
other; inside a group, threads work over tiles (phase A, B), supports (cache build) or particles (orders, walk).

### 3.3 One pass
1. **Distinct supports** of the active particles, key (hash, bits of log m, S); particle lists sorted by index.
2. **Cache** per support: Cholesky factors of H and A, forward solve, prefix sums, composite blocks, k deletion scores
   (WP1 Bit scorer), odds of members.
3. **Active columns** A = ∪ members of supports that can add; gathered contiguous (|A| × n).
4. **Phase A** (threads over tiles of 128 labels, X pre-tiled row-major, 64-B aligned): products x_aᵀx_j (sequential in
   i), flip scores and odds for every (support, label) into row buffers; for each particle on the support, the first
   position > q_i whose addressed uniform changes its state (8-lane Philox, `fmin` = integer atomic min).
5. **Walk** (threads over particles): U/N/I labels with q_i < position < fmin_i executed in position order on the
   unchanged state; the first that changes the state ends the segment: e_i = that position; else e_i = fmin_i (Gibbs
   change) or m (no change).
6. **Phase B** (threads over tiles): Gibbs labels at positions (q_i, e_i] are consumed: RB, held/flip counters,
   island_best, HPM candidate with the key of the smallest consuming particle, one store offer per (support, label).
7. **Apply**: new state (Gibbs: S △ j with the row-buffer log m; U/N/I: the walk's state), q_i ← e_i; done iff e_i = m.

### 3.4 Sweeps per particle (M) and re-entry
A particle takes one pass per state change plus one: M = 1 + (Gibbs changes + accepted U/N/I) per round. A moved
particle re-enters the next pass with its new support and its consumed prefix q_i; positions ≤ q_i are never re-read.
MEASURED (Owls, `v4_bench_island island 10000 2500 3 A lm 256 128 30 8 4`, AR(0.6), n = 200, geometric 30-stage grid
— **not a calibrated grid**): M = 4.19; (support, label) pairs per particle-round = 2.96 p (sharing); 1.4 Gibbs
changes per particle-round at φ = 1, 2.4 at φ ≈ 0; 57.8 distinct supports per pass (G = 256).

### 3.5 Equality with the particle-major algorithm (same arithmetic)
For each particle the label-major round performs **the same sequence of state transitions** as `pm_round`:
- position by position, the state used at position t is the state after the last change before t (a segment never
  crosses a change: fmin and the walk stop at the first change);
- every value used at a position is the same function of (state, label, address): flip score and odds come from the
  same 8-lane primitives (`eval8_add`/`eval1`, lane-wise identical ops whatever the other lanes), the uniform from the
  same address, the U/N/I steps from the same function;
- labels after the change are recomputed in the next pass from the new state (their first computation is discarded,
  rule 2), so a value is never used with a stale state.
The ledger receives the same events (same model, F, key, phase, mech) — stores and tallies are order-free (§1.3) —
and RB the same per-(particle, label) odds (exact sum, §3.6). Particles are independent within a round (no shared
state but the order-free ledger), so group boundaries and thread schedules do not matter. Hence identical outputs; T3
tests the hash in both arithmetic forms.

### 3.6 Reduction order (RB) — declared choice
`o_j` enters as the integer ⌊o_j · 2⁶³⌋ into unsigned 128-bit accumulators (current measured round and total). The
sum is exact, so it does not depend on particle, pass, group or thread order (stronger than spec §3 rule 3's "particle
order in chunks of 64"); against core's double sum it is class A, |error| ≤ 2⁻⁶³ per term (golden: ≤ 1e-12 relative).
Writes are race-free: phase B threads own disjoint label tiles (particle-major: per-thread arrays summed exactly).
Memory 32 B × p (+ 16 B × p × T particle-major). Q2 asks to confirm this instead of chunked double sums.

### 3.7 Class-A path values
A class-A flip score (bordered update from S) can differ in the last bits from the value of the same model reached
otherwise (full Bit score after U/N/I, or a flip from another support). Consequences, all deterministic: the particle
keeps the value it was given; supports are keyed by (S, log m bits); the store keeps the largest value per model;
the HPM order adds the key after (F, |S|, lex). Bit form: no effect. (Alternative, Q2b: canonicalise every accepted
state by a full Bit score — +1 score per change, removes path dependence.)

---

## 4. Restart (spec §6; T6; D-21: stage boundaries only)
**When.** After a step (init, each bridge stage, each burn-in and measured round), after the absorb, at most every
`ckpt_every_s` (600 s) and always at `stop_after_step` (tests).
**Content.** Configuration fingerprint (seed, island, N, grid, L, Hm, B, cap, n, p, y'y, log Z̄₀, J, arithmetic — not
threads, G, tile or kernel: a resume may change them); step index; log Ẑ so far; init hash; particles (S, h, log m,
lg0, d, F); stage table, terminal moves and distinct counts; `rb_round` so far; the 128-bit RB totals; the master tally
(counters, island_best, HPM + key); the compacted store (v, hash, off, len, pool). No generator state (addresses are
recomputed). Compat mode (not built by WP3) would add the xoshiro state.
**Atomicity.** Two generations `<path>.a/.b` written alternately: payload → `<file>.tmp.<pid>`, `fsync`, `rename`.
Header: magic, generation, length, FNV-1a checksum (provisional; WP1's kind-8 file with SHA-256 sections replaces it).
A load reads both, keeps those with valid magic, length, checksum and fingerprint, takes the larger generation.
**Equivalence.** Every output of the remaining steps is a function of exactly the checkpointed state and the
addresses (store: top_c(top_c(A) ∪ B) = top_c(A ∪ B); tallies: sums/max/strict-order max; RB: exact integers), so a
resumed run produces identical bytes. **Tests**: `t6_restart_bit_identical` — interrupt after steps 0, 2, 5, 6, last
and resume with other threads/G/kernel; corrupt newest generation → resume from the older one. **To add** (Sol F5,
manager item 7): kill during write = truncated `.tmp` and truncated generation file (simulated), crash between
fsync and rename, repeated resubmission (resume twice), resume with a different binary/config → refusal.

---

## 5. Open questions and decisions needed from the manager
1. **Bit-form label-major kernel** (exists, tested, T3-equal): keep as a test-only path (config check refuses it in
   production; zero maintenance cost so far) or delete? Recommendation: keep test-only.
2. **RB reduction**: approve the exact 128-bit fixed-point sum (§3.6) in place of spec §3 rule 3's chunked double
   sum. (2b) Class-A path values (§3.7): accept, or canonicalise accepted states by a full Bit score?
3. **G at 10⁶**: G = 64 (row buffers 1 GB) vs 256 (4 GB); smaller G costs more passes per particle. Recommend G = 64
   at 10⁶, 256 at ≤ 10⁵, set by the admission check from `--mem-budget`.
4. **Store at large supports**: the top store's pool grows with k; at 1M and k ≈ 20 the kept run alone is ≈ 4.2 GB.
   Policy on refusal vs a capped pool (e.g. refuse when the admission check fails at a compaction)?
5. **Store offer cost** (MEASURED 213 ns per offer in a duplicate-heavy mix at c = 4·10⁶): approve a worker-side
   duplicate filter against an immutable index snapshot (double-buffered index: + 4c × 4 B), or accept the cost?
6. **Checkpoint size at 10⁶** (≈ store 2.2–4.5 GB + 16 p): write streamed from the arrays (no byte image) — needed to
   keep the peak inside the budget; OK to implement now (it is in the uncontested restart part)?
7. **v0.1.5 event key**: confirm `sub` = 0 held / 1 flip / 0 proposals / 0 init (§2.2).
8. **The `island` CLI command and `island_r.bin`** wait for WP2 (`setup.bin`) and WP4 (`calib.bin` grid) readers;
   until then `run_island()` takes in-memory Data/Start/Neighbours. Who owns the `island_r.bin` section writer — WP3
   (my assumption, per INTERFACES §5.1)?
9. **Measured cost vs plan** (Owls, loaded, 3 threads; to be re-measured on SPR at G0-style thread counts): class-A
   island at 10⁴ c = **545 ns** per elementary step (plan 300) with M = 4.19 (plan 3) on an uncalibrated grid;
   bit-form label-major 994 ns. Kernel per (support, label) at 10⁵: class A 147 ns (256 distinct supports, |A| = 1,273;
   products 90 + flip/odds 57) and 66 ns (64 copies of S₀); bit form 282 / 187 ns. Within the G0 bound (700 ns) but
   above the precise-plan value; levers: phase B (96 ns per step), M, products sharing, offers.
