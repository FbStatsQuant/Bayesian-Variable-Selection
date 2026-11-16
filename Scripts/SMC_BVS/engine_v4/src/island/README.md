# WP3 — the island kernel (`v4::island`)

ENGINEERING_SPEC §0-v2.4, §3, §6; INTERFACES v0.1.1 §3, §4, §6, §7. Entry point:

```cpp
template <Arith A> IslandRun run_island(const Data&, const Start&, const Neighbours&, const IslandConfig&);
v4::IslandResult to_record(const IslandRun&);     // INTERFACES §5.2 record (Ledger with a compacted v4::Store)
```

| file | content |
|---|---|
| `include/v4/island/dep.h` | what the island takes from WP1 (aliases) and the **WP2 stand-ins** (Start, Neighbours) |
| `include/v4/island/amath.h` | 8-lane `v8d` type, `fma8`, class-A vector log / exp (fdlibm algorithms, < 1 ulp) |
| `include/v4/island/kernel.h` | `SupportCache`, flip scores (bit form: sorted-prefix reuse; class A: bordered update), odds |
| `include/v4/island/store.h` | `TopStore` (concurrent top-c, order-free), `ThreadLedger` (counters, island_best, HPM + key) |
| `include/v4/island/island.h`, `src/island/island_impl.h` | the island: init, bridge, burn-in, measured rounds; label-major and particle-major kernels; checkpoints |
| `tests/test_island.cpp` | Philox KAT, kernel bits, class A, store (multi-thread, vs WP1 Store), T3, I2/I4, T6 |
| `tests/test_island_golden.cpp` | golden vs `core/` compiled unchanged: tables, flip scores, **a whole island vs `v3::Engine::run_island`** |
| `tools/bench_island.cpp` | measurements (kernel ns per (support, label), store offers, island end to end) |

## Algorithm (identical output for both kernels, any thread count, G, tile)

`core/cpp/v3_engine.h:269-368` with a fixed grid. Every uniform is read at its INTERFACES §3 address, so the island is
a deterministic function of (data, setup, grid, N, L, Hm, B, seed, island id).

**Label-major round** (spec §3 rules 1–4). Particles in groups of `G`. Per group: round orders (Fisher–Yates on the
addressed uniforms) and their inverses. Then passes until every particle has consumed all m = p + B + 2 positions:

1. *distinct supports* of the active particles, keyed by (hash, log m bits, S) — class A can give one model two path
   values; the cache of each support (Cholesky factors, forward solve, prefix sums, composite blocks, k deletion scores);
2. *phase A*, threads over label tiles: products `x_aᵀx_j` for the active columns (sequential in i, the Gram bits),
   flip scores and odds for every (support, label), and for each particle on the support the first position after its
   current one where its addressed uniform changes the state (`fmin`, an integer atomic min);
3. *walk*, threads over particles: U, N_b, I labels between the current position and `fmin` are executed in position
   order with the scalar steps of core (`v3_engine.h:146-192`); the first that changes the state ends the segment;
4. *phase B*, threads over tiles: the Gibbs labels at positions (q, e] are consumed — RB, held/flip counters,
   island_best, HPM candidate (key of the smallest consuming particle), store offer once per (support, label);
5. the state change is applied; particles that changed take the next pass (M = 1 + changes).

Scores of labels a particle did not consume are discarded (rule 2). With `G = 1` and one thread this is a
particle-serial execution; `KernelKind::ParticleMajor` is core's serial round written out (T3 reference).

## Declared choices (for the reviewer)

1. **RB reduction (spec §3 rule 3, INTERFACES §7 (3)).** Instead of chunked double sums, `o_j` enters as the
   integer `floor(o_j · 2^63)` into unsigned 128-bit accumulators. The sum is exact, so it is independent of particle,
   pass and thread order (stronger than a declared order). Against core's double sum it is class A: error ≤ 2⁻⁶³ per
   term (golden test: ≤ 1e-12 relative on `rb_acc`, `rb_round`, `pip`). Memory 16 B × p per accumulator.
2. **Store (INTERFACES §4.1).** `TopStore` keeps, for each model, its largest offered value; content = top-c under
   the order. Threads append to private buffers; full buffers merge under a mutex; an offer with `v < tau` is dropped,
   `tau` = value of the c-th entry once c distinct models are held (else −∞).
   *Why dropping never changes the result:* at the time of the drop the store holds c distinct models, each with
   value ≥ tau; values only grow, so the final c-th value is ≥ tau > v. If the model ends in the final store its
   final value is ≥ tau > v, so v was not its maximum. Equal values are never dropped (ties are decided by size/lex).
   Tested against WP1's reference `v4::Store` (bit-identical content) and under 3 threads.
3. **Class A path values.** Class-A flip scores (bordered update from S) can differ in the last bits from the score
   of the same model reached otherwise. The particle carries the value it was given; supports are keyed by
   (S, log m bits); the store keeps the largest value per model; the HPM order adds the event key after (F, |S|, lex).
   All of this is deterministic, so T3 holds in class A (tested). Bit form: all values equal, no effect.
4. **Bit form and ISA.** Vector lanes use only IEEE `+ − × ÷ √` (no contraction under `-ffp-contract=off`) and
   scalar `pm::log/exp` per lane: bits are ISA-independent. Class A uses `fma8` (a true FMA when the build has FMA).
   Kernel headers sit in an ISA-tagged inline namespace so translation units built with different `-march` never
   share a copy.
5. **Held states** are counted (`gibbs_held`) but not compared with island_best: a held state was scored by the
   island earlier, so it never changes the maximum (golden test confirms island_best).
6. **Checkpoints** (spec §6) at step boundaries (after init, each bridge stage, each burn-in and measured round), at
   most every `ckpt_every_s` (600 s default); two generations `.a/.b`, written to a temporary name, fsync'd and renamed,
   FNV-1a checksum, configuration fingerprint (not including threads, G, tile or kernel: a resume may change them).
   Production stores no generator state. *Provisional container*: WP1's kind-8 file with SHA-256 sections replaces it.

## Adoption of WP1 / WP2 headers
- WP1 (PR #11): adopted — `Data`, `Model`, `Zobrist`, `rng.h` (Philox addresses), `pm::`, `Scorer<Bit>`, `Status`,
  `Phase/Mech/EventKey/Order`, `MoveStats/StageRow`, `v4::IslandResult` + `Ledger` (via `to_record`).
- WP2: `Start` (tables, sampler, `comp`, π₀ draw) and `Neighbours` are stand-ins in `dep.h` with core's arithmetic
  (golden-tested against `core/` tables). Switch to `setup.h` when it lands: the island uses only `blk`, `pos`, `logr`,
  `comp`, the sampler tables and the CSR rows.
- Not yet wired: the `island` CLI command (`island::run`, still WP1's stub) needs `setup.bin` (WP2) and `calib.bin`
  (WP4) readers; the `island_r.bin` writer follows WP1's `format.h` once those exist.
