# INTERFACES — engine v4 contract between WP1–WP5

**v0.1.5 (binding; changes only by the WP1 owner with a changelog line).** 2026-11-15. Source: ENGINEERING_SPEC §0-v2,
§1–§3, §6. Where this file is silent, the spec rules; where the spec is silent, `core/` (v3.1 / revision D) rules.
Questions and change requests: to the WP1 owner through the manager. Line references `core/...:N` are to revision D.

## 1. Layout, namespaces, build, tests
```
Scripts/SMC_BVS/engine_v4/
  CMakeLists.txt   cmake/flags.cmake      INTERFACES.md (copy of this file)
  include/v4/      public headers, one per component (names below)
  src/             library sources: common/ (WP1) setup/ (WP2) island/ (WP3) calib/ merge/ (WP4) eval/ post/ (WP5)
  src/cli/         main.cpp + one cmd_<name>.cpp per command
  tests/           test_<component>.cpp, golden/ (bit tests vs core/), fixtures/ (≤ 20 MB), run_tests.sh
  tools/           R / Python helpers (reference generation from core/, Slurm driver, competitors)
```
- Namespace `v4` for everything; sub-namespaces `v4::fmt` (files), `v4::gen`, `v4::prep`, `v4::setup`, `v4::island`,
  `v4::calib`, `v4::merge`, `v4::eval`, `v4::post`. Code copied from `core/` keeps v3 names where possible and cites
  `core/...:line` above each copied block.
- **One binary** `smcbvs4 <command> [--key value ...]`, commands `gen gen-test prep setup calibrate island merge eval post
  info version` (`info` prints a file's header and section table and verifies hashes; `version` prints the binary block). Every command takes `--manifest <json>` or flags,
  writes `<out>.json` (record + status) next to its binary output.
- CMake targets: `v4_bit` (static lib; flags **`-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`**, every kernel
  that must equal v3 bits), `v4_a` (static lib; class-A kernels; `-march=x86-64-v2` unless `-DV4_WIDE_ISA=ON` →
  `-march=x86-64-v3`, FMA only through explicit intrinsics / `std::fma`), `smcbvs4` (CLI), `v4_tests` (all unit + golden
  tests, own minimal harness `tests/tk.h`; it also compiles the core/ headers unchanged with the v3 flags for golden
  comparisons; links libquadmath), tools `v4_pmath_check`, `v4_bench_score`. C++20, GCC ≥ 11. OpenMP required. No network at configure or build time.
- Test runner: `engine_v4/tests/run_tests.sh [--quick|--full] [--threads k] [--fixtures]` = configure + build (`make -j3`,
  `nice -n 19`, build dir under `$TMPDIR`, which must be set) + run `v4_tests`. Golden comparisons against `core/` are
  inside `v4_tests` (core headers compiled unchanged, and fixtures written by R-compiled `core/` via
  `tools/make_fixtures.R`; `--fixtures` regenerates them). A missing fixture is a FAIL. Exit 0 iff all pass.

## 2. Core types (`include/v4/data.h`, `model.h`, `score.h`)
Indices: **internal 0-based int32 over kept columns**; original 1-based indices only at file/JSON boundaries via
`Data::orig`. A model is a **sorted, duplicate-free int32 array**. `p ≤ 2^31−1`, `n ≤ 2^31−1`, `K = min(p, n/2)`.
```cpp
struct ModelView { const int32_t* idx; uint32_t k; };          // non-owning; sorted
using Model = std::vector<int32_t>;                           // owning; sorted
struct Data {                                                 // read-only after prep; arrays may be mmap views
  int32_t n, p, p_raw, K;
  const double* Xs;      // n×p column-major, standardised; col(j) = Xs + (size_t)j*n
  const double* ys;      // n
  const double* z;       // p, z_j = Σ_i x_ij y_i (sequential in i, core/cpp/v3_score.h:54-55)
  const double* diagG;   // p, G_jj = Σ_i x_ij x_ij (sequential in i, core/cpp/v3_score.h:45-53)
  const double *col_max, *col_mean, *col_sd;   // p each (v3_preprocess.R:24-51 outputs)
  const int32_t* orig;   // p, 1-based original column of internal j (kept map); dropped list in data.bin
  double yty, a0 = 0.01, b0 = 0.01, nu, logCn, logm0, logWK;   // as core/cpp/v3_score.h:56-71
  std::vector<double> logw, logprior;                           // k = 0..K
  Zobrist zob;                                                  // keys over internal j
  double y_max, y_mean, y_sd_scaled;                            // response map
};
```
- `Data` holds **no Gram**. Every Gram entry is `gram(a,b) = Σ_{i=0}^{n−1} x_{i,min(a,b)} · x_{i,max(a,b)}` in double,
  sequential in i, no FMA — the bits of `core/cpp/v3_score.h:45-53`. `data_constants(Data&)` fills the scalars and
  `logw/logprior` exactly as `core/cpp/v3_score.h:56-71`.
- **Hash** (`model.h`): Zobrist exactly as `core/cpp/v3_util.h:102-109`: `key[j]` = successive `splitmix64` outputs from
  `x = 0x5EEDB175C0DE2026`; `hash(S) = XOR_j key[j]`. Collisions are resolved by comparing the index arrays. Strict
  orders: `lex_less`, `hpm_better` (F desc, |S| asc, lex asc) as `core/cpp/v3_util.h:117-126`.
- **Score** (`score.h`): `struct ScoreOut { double logm, Q, logdetH, logdetA, cond_H, cond_A; int8_t route;
  bool q_recomputed; }`, routes `CHOL=0, REFACTOR=1, QR=2` as `core/cpp/v3_score.h:27`. Derived per model:
  `F = logprior[k] + logm`, `lg0 = logprior[k] + comp(S)`, `d = (logm − logm0) − comp(S)` (`core/cpp/v3_engine.h:89-97`).
- **Neighbours** (WP2, `setup.h`): CSR `struct Neighbours { std::vector<int64_t> ptr; std::vector<int32_t> idx; }`,
  `ptr.size() = p+1`, each row sorted ascending; content = `core/cpp/v3_blocks.h:149-170`. Size bound: at most pB
  directed selections and at most 2pB adjacency entries in total after symmetrising; **no per-column maximum** (a hub
  can have degree p − 1; tests include hubs). The uncapped threshold graph of the partition is a different object
  with its own edge-count guard (WP2).
- **Partition** (WP2): `struct Partition { int32_t J, B; std::vector<int64_t> bptr; std::vector<int32_t> members;
  std::vector<int32_t> blk, pos; }` — block b = `members[bptr[b]..bptr[b+1])`, sorted, packing order; `blk[j], pos[j]`
  as `core/cpp/v3_start.h:38`. Plus the duplicate components and the cut-group record (CSR each).
- **Tables** (WP2): `struct Tables { std::vector<int64_t> code_ptr; std::vector<double> logr; ... }` — block b's
  `logr` for codes `0..2^{m_b}−1` at `logr[code_ptr[b] + code]`, NaN where |U| > K; code bit i ↔ i-th member
  (`core/cpp/v3_start.h:76-98`). `logprof`, `logF` ((J+1)×(K+1) row-major), `size_logmass`, `size_cum`, `cond_cum`:
  flat arrays + offsets, same values as `core/cpp/v3_start.h:101-157`. **`codes_by_size` and `sub_cum` are not stored
  (D-18)**: they are recomputed on demand for each block a π₀ draw selects, with the same values and bits —
  `codes_by_size[b][j]` = the codes of popcount j in increasing order, `sub_cum[b][j]` = `cumulative_from_logs` of
  their `logr` (`core/cpp/v3_start.h:101-116`). Gate: draws identical with and without the stored sections.
- **Start** (WP2): `struct Start { const Data* D; const Partition* P; const Tables* T; double logZbar0;
  double comp(ModelView) const; double log_gamma0(ModelView) const; void draw_pi0(UniformSource&, Address, Model&) const;
  ModeResult mode; }`. `comp` = the ordered block sum of `core/cpp/v3_start.h:54-66` (same bits).

## 3. Uniforms: addresses, Philox, compat streams (`include/v4/rng.h`)
**Generator: Philox4x32-10** (Salmon et al. 2011, Random123). Reasons: counter-based (stateless, any execution order
gives the same value, so threads/groups/tiles/passes cannot change results: T3); passes BigCrush; 32×32→64 multiplies
vectorise on x86-64-v2/v3/AVX-512 (≈ 2–5 ns per call scalar); a public reference with known-answer vectors (the
Random123 KAT file; tests use them); used by cuRAND, NumPy, C++26 `std::philox4x32`. 10 rounds, constants
`M0=0xD2511F53, M1=0xCD9E8D57, W0=0x9E3779B9, W1=0xBB67AE85`.
```cpp
enum Role  : uint8_t { R_FINAL=0, R_PILOT=1, R_DIAG=2, R_POST=3, R_GEN=4, R_TEST=5 };
enum XPh   : uint8_t { X_INIT=0, X_RESAMPLE=1, X_BRIDGE=2, X_BURN=3, X_MEASURED=4, X_POST=5,
                       X_GEN_X=8, X_GEN_NOISE=9, X_GEN_FACTOR=10, X_TEST_X=11, X_TEST_NOISE=12, X_TEST_FACTOR=13 };
struct Address { uint32_t seed; uint8_t role, tier, iter; uint32_t island;   // key
                 uint8_t xph; uint32_t stage; uint32_t particle, position, slot; };   // counter
// key  = { seed, (role<<28) | (tier<<26) | (iter<<20) | island }      island < 2^20, iter < 64, tier < 4
// ctr  = { slot, position, particle, (xph<<24) | stage }              stage (or round) < 2^24
// x[0..3] = Philox4x32_10(ctr, key);  u  = ((uint64(x[1])<<32 | x[0]) >> 11) * 2^-53   ∈ [0,1)
//                                     u2 = ((uint64(x[3])<<32 | x[2]) >> 11) * 2^-53   (second variate, gen only)
inline double uniform_at(const Address&);
struct UniformSource { virtual double u(const Address&) = 0; };   // AddressedSource (Philox), CompatSource (below)
```
**The address domain (production; v0.1.5).** Every uniform has an address fixed by the control flow before its value
is read (spec §3 rule 1). Fields, widths and limits; the packing is a bijection onto (key, counter), so distinct
addresses give distinct Philox inputs:
| field | width | meaning | limit |
|---|---|---|---|
| seed | key[0], 32 b | fit seed (data seed for role GEN) | 1 … 2³¹−1 |
| role | key[1] bits 28–31 | FINAL 0, PILOT 1, DIAG 2, POST 3, GEN 4, TEST 5 | < 16 |
| tier | key[1] bits 26–27 | calibration tier e (FINAL: 0) | < 4 |
| iter | key[1] bits 20–25 | rebuild iteration: 0 = pilot, k = rebuild k (FINAL: 0) | < 64 |
| island | key[1] bits 0–19 | final island r = 1…R′, diagnostic island r = 1…4, pilot 0 | < 2²⁰ |
| xph | ctr[3] bits 24–31 | INIT, RESAMPLE, BRIDGE, BURN, MEASURED, POST; GEN/TEST rows for gen | < 256 |
| stage | ctr[3] bits 0–23 | bridge stage t (INIT 0); BURN: round l; MEASURED: round h | < 2²⁴ |
| particle | ctr[2], 32 b | the **destination** particle i = 1…N (after resampling, never an inherited stream) | < 2³² |
| position | ctr[1], 32 b | round position q = 1…m (m = p + B + 2); 0 for order draws, resampling, initial draws | < 2³² |
| slot | ctr[0], 32 b | `(kind << 28) | index`, kinds below | index < 2²⁸ |

Slot kinds (`SlotKind`, rng.h): `SK_ORDER` 0 (Fisher–Yates draw d = 0…m−2), `SK_RESAMPLE` 1, `SK_PI0_SIZE` 2 (total size
k), `SK_PI0_BLOCKSIZE` 3 (index = block b), `SK_PI0_SUBMODEL` 4 (index = block b), `SK_MOVE_J` 5, `SK_MOVE_L` 6,
`SK_ACCEPT` 7 (`SLOT_ACCEPT`). So J < 2²⁸ and m − 1 < 2²⁸.
| draw | xph | stage | particle | position | slot |
|---|---|---|---|---|---|
| initial π₀ draw of particle i | INIT | 0 | i | 0 | PI0_SIZE 0; PI0_BLOCKSIZE b for b = J−1…0 while r > 0; PI0_SUBMODEL b for k_b > 0 (`core/cpp/v3_start.h:158-176`) |
| resampling uniform of destination i at stage t | RESAMPLE | t | i | 0 | RESAMPLE 0 |
| round order of particle i | BRIDGE / BURN / MEASURED | t / l / h | i | 0 | ORDER d, d = 0…m−2 in draw order (`core/cpp/v3_engine.h:193-211`) |
| step at round position q | as its round | as its round | i | q | G: ACCEPT. U, N_b: MOVE_J, MOVE_L, ACCEPT. I: the π₀ slots above, then ACCEPT |

Unused slots (self-loops, empty N(j)\S) are simply not read. Diagnostic islands of different rebuild iterations get
fresh addresses (law-equivalent to v3's continued streams; class L). `post` draws: role POST, xph POST. Role GEN uses
slot = polar-method attempt number (no kinds). **I5** is checked by `CheckedSource` (rng.h): UNIQUE (production) or
INCREASING in `serial_less` (compat, per stream). The test `i5_multi_rebuild_calibration_and_final` drives the full
control flow of 2 tiers × (pilot + 3 rebuilds × 4 islands) + 16 final islands through it. WP3/WP4 wrap their
sources with it in tests, and always when `v4::kCheckAddresses` is true (CMake `-DV4_CHECK_ADDRESSES=ON`).

**Compat mode** (`CompatSource`): ignores the address and returns the next `Xoshiro256ss::uniform()` of the unit's v3
stream (`core/cpp/v3_util.h:43-61`, copied), seeded `seed_stream(seed, stream)` with stream = 0 pilot tier 0, 1–4 diag
tier 0 islands 1–4, 5 pilot tier 1, 6–9 diag tier 1, 9 + r final island r = 1…4 (`core/v3_run.R:8-11`,
`core/cpp/v3_core.cpp:444`); streams 0–9 continue across rebuilds; 200 = test draws (`core/v3_setup.R:47`). Compat
code must request uniforms in exactly v3's serial order (`core/v3_run.R:24-37`); the address argument is then only a
label (`CheckedSource` in increasing mode checks the serial order). Compat streams exist only for tiers 0 and 1. Checkpoints
store the xoshiro state and `count` in compat, nothing in production.

## 4. Store and Ledger (`include/v4/store.h`, `ledger.h`; reference implementation WP1, optimisation WP3)
### 4.1 Store: top-c of everything offered, independent of offer order
```cpp
enum class Order : uint8_t { HPM, LEX };    // HPM: v desc, |S| asc, lex asc; LEX: v desc, lex asc (core/cpp/v3_ledger.h:35-42)
struct Store {
  uint64_t cap; Order ord;
  std::vector<double> v; std::vector<uint64_t> off, hash; std::vector<uint16_t> len; std::vector<int32_t> pool;
  void offer(double v, ModelView S, uint64_t h);   // quick reject if v < cutoff(); else append to the staging run
  void compact();     // sort the staging run, merge it with the kept run (drop exact duplicates), keep the first cap
  void merge(const Store& o);                       // = offer every entry of o, then compact()
  double cutoff() const;                            // −inf until cap entries are kept, then the worst kept value
  bool would_enter(double v, ModelView S) const;    // after compact(): cap not reached or better than the worst kept
};
```
After `compact()`: entries strictly sorted under `ord`, no duplicates, size ≤ cap (invariant I1). Staging is compacted
when it reaches max(cap/4, 4096) entries, so the peak is ≈ 2.5·cap entries (kept + staging + the new kept run with room).
`cutoff()` is **monotone non-decreasing** (the worst of the top-c of a growing set never decreases) and is published
atomically, so other threads may read it at any time. Caps: top = 40p + 1 (HPM order, value F); lead0 = 20p (LEX,
value lg0); lead1 = 20p (LEX, value F); leader stores exist only in calibration and compat mode (D-7). A model's value
is a deterministic function of S, so duplicates are equal entries.

### 4.2 Ledger (one per island) and ThreadLedger (one per worker thread)
```cpp
enum Phase { PH_TABLE=0, PH_PILOT, PH_DIAG, PH_FINAL_INIT, PH_FINAL_BRIDGE, PH_BURN_IN, PH_MEASURED, PH_LOCAL,
             PH_INHERITED, PH_TEST, PH_LS0, N_PHASE };          // = core/cpp/v3_ledger.h:11 (names identical)
enum Mech  { ME_TABLE=0, ME_INIT, ME_GIBBS_HELD, ME_GIBBS_FLIP, ME_USWAP, ME_NSWAP, ME_INDEP, ME_LOCAL,
             ME_INHERITED, N_MECH };                            // = core/cpp/v3_ledger.h:14
enum Segment : uint8_t { SG_TABLE=0, SG_INHERITED=1, SG_CALIB=2, SG_FINAL=3, SG_LOCAL=4, SG_LS0=5 };
struct EventKey {   // total order = lexicographic in field order = v3's serial execution order
  uint8_t seg, tier; int8_t iter; uint32_t unit;   // unit: island r (pilot 0); 0xFFFFFFFF = the local search of (tier, iter)
  uint8_t xph; uint32_t stage, round, particle, position; uint8_t sub; };   // xph = execution phase (INIT<BRIDGE<BURN<MEASURED)
struct EventCtx { int phase /*reported label*/, mech; EventKey key; double phi; };
struct Tally {                               // the small, per-thread part of a ledger
  bool has_hpm; Model hpmS; double hpmF, hpm_logm; EventCtx hpm_ev;
  uint64_t logical[N_PHASE][N_MECH], fresh[N_PHASE][N_MECH];   // `fresh` only in compat (OD-3)
  std::vector<double> island_best;           // index r = 0..R′
};
struct Ledger : Tally {                      // ONE per island (calibration process, merge job): owns the stores
  Store top, lead0, lead1;
  void event(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx&, bool offer);   // serial use
  void absorb(ThreadLedger& t);              // flush t's buffers into the stores, merge t's tally, reset t
  void merge(const Ledger& o);               // whole ledgers (diagnostic islands, island files): order-free
};
struct ThreadLedger : Tally {                // one per worker thread; NO stores
  ThreadLedger(Ledger& island, size_t buf_cap = 65536);
  void event(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx&, bool offer);
  // offers: dropped if v < island.store.cutoff(); else appended to a bounded OfferBuffer (one per store);
  // a full buffer is flushed into the island store at once (under the island ledger's lock)
};
```
- **EventKey assignment (v0.1.5).** Lexicographic key order = the serial reference traversal of `core/cpp/v3_core.cpp:
  408-476`: tables → inherited → each island entirely, in order → final local search → LS0 (calibration: tables, then per
  tier e: pilot, its local search, then per rebuild k: diagnostic islands 1–4 and their local search). `sub` is the
  within-step event ordinal.
  | event | seg | tier | iter | unit | xph | stage | round | particle | position | sub |
  |---|---|---|---|---|---|---|---|---|---|---|
  | table code c of block b | TABLE | 0 | −1 | 0 | 0 | b + 1 | 0 | 0 | c | 0 |
  | inherited model i (input order) | INHERITED | 0 | −1 | 0 | 0 | 0 | 0 | i | 0 | 0 |
  | final island r | FINAL | frozen tier | −1 | r | INIT / BRIDGE / BURN / MEASURED | INIT 0, BRIDGE t, BURN and MEASURED T | INIT 0, BRIDGE t, BURN l, MEASURED h | i | q (INIT 0) | G: held 0, flip 1; else 0 |
  | calibration island (pilot r = 0, diagnostic r = 1–4) | CALIB | e | k | r | as above | as above | as above, MEASURED L + h | i | q | as above |
  | local search | CALIB (unit `UNIT_LOCAL`), LOCAL, or LS0 | e / frozen tier | k / −1 | 0 or `UNIT_LOCAL` | 0 | scan s (centre 0) | moves so far | 0 | scan index (centre 0) | 0 |

  stage / round / particle / position take v3's own EventCtx values (`core/cpp/v3_engine.h:274-372` islands, `:379-422` local search), so
  provenance exports to the v3 fingerprint unchanged; `xph` orders the phases of an island.

  The inherited HPM keeps its calibration key (`core/cpp/v3_core.cpp:433-437`). Provenance = the smallest key among the
  winning model's events, which is its first event in the serial traversal.
- **Logical events by mechanism (v0.1.5; `core/cpp/v3_engine.h:84-196`, `v3_core.cpp:372-427`).**
  | step / source | condition | events (mechanism) | uniforms |
  |---|---|---|---|
  | initial draw | always | 1 INIT | π₀ |
  | G at label j | j ∈ S or \|S\| < K | **2**: GIBBS_HELD (sub 0, not fresh) + GIBBS_FLIP (sub 1) | 1 |
  | G at label j | j ∉ S and \|S\| = K (cap) | 1: GIBBS_HELD | 1 |
  | U | \|S\| ∈ {0, p} (self-loop) | 0 | 0 |
  | U | otherwise | 1 USWAP | 3 |
  | N_b | S empty (self-loop) | 0 | 0 |
  | N_b | N(j) \ S empty (no score) | 0 | 1 |
  | N_b | otherwise | 1 NSWAP | 3 |
  | I | always | 1 INDEP | π₀ + 1 |
  | local search | each scanned neighbour; the centre only when emitted (LS0) | 1 LOCAL | 0 |
  | tables | each code with \|U\| ≤ K, **once per ledger that ingests tables** (calibration ledger; the fit's merge ledger), never per island | 1 TABLE | 0 |
  | inherited models | offered to stores and HPM only | 0 | 0 |

  An unsaturated round therefore has ≈ 2Np Gibbs events, not Np. **I4** (replaces "events = steps", spec §5): per round
  and phase, `logical` increments equal `i4_expected(MoveStats)` (records.h): held = G steps, flip = G steps − cap
  steps, USWAP = executed U, NSWAP = executed N − no-score N, INDEP = I steps.
- `event` counts `logical[phase][mech]`; updates `island_best[r]` for the island's own events exactly as
  `core/cpp/v3_ledger.h:104-113`; if `offer`, offers to HPM and stores. Production offers every consumed score
  (`offer = true`, no cache); compat offers on fresh evaluations exactly as v3. Rule (spec §3.2): scores of labels a
  particle did not consume are not events.
- **Island protocol.** Workers record into their own `ThreadLedger`. At every stage end (and before anything reads the
  island store, a checkpoint included) the island calls `absorb` for each thread ledger **in thread-index order**.
- **Exact and deterministic.** The store holds the top-c of all offers whatever the order and timing of flushes (4.1);
  the cut-off drops only entries strictly worse (by value) than c entries already offered (ties are kept: the tie order
  may admit them). Tally merges are order-free: HPM by `hpm_better`, and for the same model the **smaller EventKey**
  keeps the provenance (= v3's "first score" rule); `island_best` by max; counters by sum.
- **Memory.** One island store (≈ 2.5c entries at peak), plus threads × (1 or 3) × `buf_cap` buffered entries.

## 5. Records and files (`include/v4/format.h`, `records.h`)
### 5.1 Binary container (every `.bin`)
Little-endian: `FileHeader` (128 B) | `SectionEntry[n]` (128 B each) | sections at 64-byte aligned offsets. Written to
`<name>.tmp.<pid>`, fsync'd, renamed (directory fsync'd). Readers mmap read-only and verify every hash.
```cpp
struct FileHeader {               // 128 bytes
  char magic[8];                  // "SMCBVS4\0"
  uint32_t format_version;        // 1
  uint32_t kind;                  // 1 raw, 2 data, 3 setup, 4 calib, 5 island, 6 fit, 7 law, 8 ckpt, 9 eval
  uint32_t mode;                  // 0 none (gen / prep outputs: no engine mode), 1 compat, 2 law (theory mode, addressed), 3 V
  uint32_t n_sections;
  uint64_t file_bytes;
  uint8_t  table_sha256[32];      // SHA-256 of the section table bytes
  uint8_t  content_sha256[32];    // SHA-256 of (this header with both hash fields zeroed ‖ section table)
  uint8_t  reserved[32];          // zero
};
struct SectionEntry {             // 128 bytes
  char name[48];                  // NUL-padded, unique in the file
  uint32_t dtype;                 // 1 f64, 2 i32, 3 u32, 4 i64, 5 u64, 6 u8, 7 u16, 8 f32, 9 json (UTF-8)
  uint32_t ndim; uint64_t dims[2];   // row-major dims; column-major arrays say so in their name (suffix _cm)
  uint64_t offset, length;        // bytes
  uint8_t  sha256[32];
  uint8_t  reserved[8];           // zero
};
```
Hash of a file "by content" = `content_sha256`: it covers the header (magic, version, kind, mode, sizes) and the section
table, which contains every section hash. Readers verify both header hashes and every section hash. SHA-256 is bundled
(`src/common/sha256.cpp`). A `meta` json section in every file holds scalars, its inputs' content hashes, the mode and
the binary block (§5.3), so the content hash changes with the binary. Three identities, never mixed:
- **File identity = `content_sha256`, always**: manifests, the merge's input validation, restart from a checkpoint.
  The merge checks that every island's `meta.inputs` equal its manifest's `data/setup/calib` content hashes (part of the
  meaning of engine files lives in `meta`: calib N, L, tier; island logZ, status).
- **Data identity across builds = named data sections only**: `X_cm`, `y` of `raw.bin` (`gen` records `X_sha256`,
  `y_sha256`) and `Xs_cm`, `ys`, `kept` of `data.bin`. Never used for setup, calib, island, fit or law files.
- **Cross-machine bit identity (T2)** compares the section hashes of all sections except `meta`, or the fit fingerprint;
  never content hashes.
- **Binary consistency** (one helper, `binary_compatible(a, b, use)` / `require_binary_compatible`, provenance.h): merge
  (V) needs both libm self-tests passed and equal flags and libm binding; merge (theory mode) also needs equal git
  commits that are clean (no `-dirty`) and known; a checkpoint restart also needs the same executable (sha256) and git
  commit. `git_commit` = 40-hex HEAD + `-dirty` when tracked files differ, refreshed at every build.
JSON numbers are doubles: every u64 value (hashes, Zobrist keys, large counters) is written as a hex string `"0x…"`.
Sections (names fixed; WPs may add sections, never rename):
- `raw.bin` (gen): `X_cm` f64 n×p, `y` f64 n, `meta`. `truth.json`: design, params, seed, S₀ (1-based), β*, σ*.
- `data.bin` (prep): `Xs_cm`, `ys`, `z`, `diagG`, `col_max`, `col_mean`, `col_sd`, `kept` i32 (1-based), `dropped`
  i32, `meta` {n, p_raw, p, K, yty, logCn, logm0, logWK, y_max, y_mean, y_sd_scaled, prep_class: "B"|"A"}, `logw`, `logprior`.
- `setup.bin` (WP2): `nb_ptr` i64, `nb_idx` i32, `dup_ptr/dup_idx`, `cut_ptr/cut_idx`, `blk_ptr/blk_members`, `blk`,
  `pos`, `code_ptr`, `logr`, `logprof_ptr/logprof`, `logF`, `size_logmass`, `size_cum`, `cond_ptr/cond_cum`,
  `mode_S`, table top stores `tstore_{top,lead0,lead1}_{v,off,len,hash,pool}`, `meta`.
- `calib.bin` (WP4): `grid`, `meta` {tier, N, L, Hm, I_used, flags, triggers}, `grids_all_ptr/grids_all`, stage
  records, calibration stores (as stores), HPM (`hpm_S`, `hpm_ev`), `logical` u64 N_PHASE×N_MECH.
- `island_r.bin` (WP3): stage table (`st_phi, st_inc, st_ess, st_cum, st_distinct_res, st_distinct_moved`, moves
  u64 T×11), `logZ` in meta, `rb_acc` p, `rb_round` 4×p, `pip_r` p, `top_*` (flat store, sorted), `hpm_*`,
  `island_best`, `logical`, `status`/timings in meta; optional `terminal_S_ptr/terminal_S`.
- `fit.bin` + `fit.json` (WP4): merged `top_*`, `hpm_*` + provenance, `hpm_before_local_*`, local-search archive,
  `mode_S`, LS0, near ties, `logZ_r`, `pip_eq`, `pip_Z`, `pip_T`, `rb_*`, flags; `fit.json` scalars and hashes only.
- `law.bin` (WP5): models (ptr/idx), weights, conjugate parameters, standardisation constants, dropped mass.
- `island_r.ckpt.{a,b}` (WP3): kind 8; newest valid generation wins.

### 5.2 Records (in-memory; serialised into the sections above)
```cpp
struct StageRow { double phi, inc, ess, cum; int32_t distinct_res, distinct_moved; MoveStats moves; };  // MoveStats = core/cpp/v3_engine.h:25-29
struct IslandResult { Status status; int32_t r, N, T, L, Hm; double logZ; std::vector<StageRow> stages;
  std::vector<double> rb_acc, pip; std::vector<std::vector<double>> rb_round; Ledger led; Timings t; };
struct CalibResult  { Status status; int32_t tier, N, L, I_used; std::vector<double> grid; std::vector<std::vector<double>> grids_all;
  uint32_t flags /*grid_fallback, grid_unconverged, escalated*/; std::vector<IslandResult> pilot_diag; Ledger led; };
struct FitResult    { Status status; int32_t Rp; double logZ; std::vector<double> logZ_r, pip_eq, pip_Z, pip_T;
  Model hpm, hpm_before_local, mpm, mode_S; EventCtx hpm_ev; LocalArchive local, ls0; Store top; uint32_t flags; };
```
### 5.3 JSON manifest (one per job; written before the first output; job refuses on any hash mismatch)
```json
{ "schema": "smcbvs4.manifest/1", "command": "island", "run_id": "...", "mode": "compat|law|V",
  "binary": {"sha256": "...", "git_commit": "...", "compiler": "g++ 11.5.0", "flags": "...",
             "libm": {"path": "...", "sha256": "...", "glibc": "2.34", "fma_variant": true}},
  "inputs": {"data.bin": "<content sha256>", "setup.bin": "...", "calib.bin": "..."},
  "params": {"seed": 1, "island": 3, "Rp": 16, "N": 2500, "threads": 48, "...": "..."},
  "reference": {"name": "...", "core_commit": "...", "core_files_sha256": {"cpp/v3_score.h": "...", "...": "..."},
                "R": "...", "compiler": "...", "flags": "...", "libm": {"path": "...", "sha256": "...", "glibc": "..."}},
  "budget": {"task_seconds": 7200, "fit_core_h": 1000, "retries": 2},
  "machine": {"host": "...", "node_type": "...", "slurm_job_id": "..."},
  "outputs": {"island_3.bin": null} }
```
The job fills `outputs` with content hashes and `status` in `<out>.json` when it ends. **`reference`** (v0.1.5; Sol
F10) names the exact reference that compat and T bit tests compare against: the `core/` commit and per-file SHA-256,
R, compiler, flags and libm. It is the block written by `tools/make_fixtures.R` into `tests/fixtures/MANIFEST.json`,
and the test `fixtures_pinned_reference_matches_core` fails if `core/` drifts from it. Compat runs copy it into their
manifests; "revision D" alone is not an identifier. Every command writes the
`binary` block (`v4::binary_block()`, `include/v4/provenance.h`) into its record and into the `meta` of each file.

## 6. Scorer, two arithmetic forms, one interface (`include/v4/score.h`)
```cpp
enum class Arith { Bit, ClassA };
template <Arith A> class Scorer {               // A = Bit lives in v4_bit, A = ClassA in v4_a
 public:
  explicit Scorer(const Data*);
  ScoreOut score(ModelView S);                  // Bit: bits of core/cpp/v3_score.h:139-246, Gram-free entries; throws NumericalFailure
  void flip_scores(ModelView S, const int32_t* labels, size_t nl, double* logm_out, int8_t* route_out);
                                                // entry t = score(S △ labels[t]); infeasible (|S ∪ j| > K) → NaN, route −1
};
using BitScorer = Scorer<Arith::Bit>;  using AScorer = Scorer<Arith::ClassA>;
```
Bit form: each entry equal in bits to `score(S △ j)` (sorted-prefix reuse allowed only if it reproduces the same
operation order, spec §1). Class A: same exact-arithmetic map, any rounding; agreement target ≤ 1e-9 relative on logm
against Bit; fallback to the Bit form whenever the class-A Cholesky pivot test fails (so routes are identical). The
kernel (WP3) is templated on `Arith`; T always instantiates `Bit`, V `ClassA`. Pinned transcendental functions:
all scorer/engine code calls `v4::pm::*` (`include/v4/pmath.h`), never `std::` directly. **Binding: glibc 2.34 libm
(no bundling)**; a correctly rounded libm would change the v3.1 bits.
- **Bit form uses only `pm::log, exp, lgamma, sqrt`** and the x87 `pm::logl, expl` of `log_sum_exp` (→ log W_K → log ϖ →
  every F; WP2's `cumulative_from_logs`). The double functions are bit-equal on Owls and NOTS although the libm files
  differ (MEASURED, `results/PMATH_NOTS.md`); the x87 rows are Owls references until the NOTS re-run.
- **`log1p` / `expm1` never appear in bit-form paths.** They exist only as `pm::machine::log1p, expm1` for class A; their
  bits differ between Owls and NOTS, and their results never enter a fixture or a bit test. (`core/` never calls them:
  `log_add` and `log1mexp_v3` are unused.)
- **Guard**: every command except `info`/`version` calls `require_bit_libm()` (`provenance.h`; `require_fma_variant()`
  is an alias). It runs `pm::self_test()`: log, exp and lgamma on the six fixed rows of `v4_pmath_check`, plus the x87
  rows `expl` ([−11000, 0]) and `logl` ([1, 1001), 64-bit mantissas; 80-bit results hashed), 2·10⁶ arguments each, must
  reproduce the measured reference hashes, otherwise `invalid_input`. `info` skips it (`self_test: "not run"`). It keys on function results,
  not on the libm file hash. The binary block records the libm path, its SHA-256, the glibc version, `fma_variant` and
  the self-test result. Evidence: `engine_v4/tests/PMATH_REPORT.md`.

## 7. Statuses, errors, threads (`include/v4/status.h`, `threads.h`)
```cpp
enum class Status : uint8_t { completed=0, resource_limit=1, numerical_failure=2, invalid_input=3, io_error=4, internal_error=5 };
struct Error : std::runtime_error { Status st; };                // thrown inside the engine
struct NumericalFailure : Error { };                            // = core/cpp/v3_util.h:26-28 semantics
Status fit_status(span<Status>);   // first that applies: invalid_input, internal_error, numerical_failure, resource_limit, io_error, completed
```
- Commands catch everything at `main`, write `<out>.json` with `status`, `reason`, and exit with `0` (completed) or
  `10 + status`. No estimate field is written unless status is `completed` (GUARD-W). Invariant violations (I1–I7) →
  `internal_error`. Hash or format mismatch at start → `invalid_input`. Write/rename failure → `io_error`.
- **Data outcomes of `prep`** (v3 returns them as fit outcomes with an empty HPM, `core/v3_preprocess.R:111-114`):
  `no_predictors` and `y_constant`. The task status is `completed`, the record has `prep_status` and `hpm: []`, no
  `data.bin` is written, and the exit code is **20** (`no_predictors`) or **21** (`y_constant`). The driver (WP5) ends
  that fit's pipeline and records the outcome; it never starts `setup`.
- **Threads: OpenMP** (`--threads k`, default `OMP_NUM_THREADS`). Rules: (1) no result depends on the thread count or
  schedule; (2) work is cut into **fixed chunks independent of the thread count** (default 64 items; label blocks and
  tiles are parameters, not part of the law); (3) floating-point reductions sum per-chunk partials, then combine chunk
  results serially in chunk order; no floating atomics, no `omp reduction` on floats; (4) **one `Ledger` (stores) per
  island; one `ThreadLedger` per worker with bounded offer buffers, absorbed at stage ends in thread-index order;
  quick rejects against the island store's monotone cut-off (§4.2)**; (5) uniforms come only from addresses, never from thread state; (6) the stage barrier
  (weights, LSE, ESS, resampling) is serial in particle order (`core/cpp/v3_engine.h:316-327`).

## 8. Owned by WP1 and delivered with the skeleton
`data.h model.h rng.h store.h ledger.h format.h records.h score.h(Bit) pmath.h provenance.h status.h threads.h json.h
sha256.h`,
`gen`, `prep` (compat bits of `v3_preprocess.R:35-51` or R-standardised input), the compat Bit scorer, fixtures, the
libm decision. Stubs (declarations + `throw Error(internal_error, "not implemented")`) for every other WP's entry
point, so all WPs link from day one: `setup::run`, `island::run`, `calib::run`, `merge::run`, `eval::run`, `post::run`.

## Changelog
- v0.1 (2026-11-15, WP1) — first binding version.
- v0.1.1 (2026-11-15, WP1) — §5.1 `SectionEntry` gets `reserved[8]` (the entry is 128 B, as stated; the field list
  summed to 120). `fmt::Writer::add` keeps a pointer to the caller's buffer (no copy) until `write()`. §6 libm binding
  decided (glibc FMA variant + run-time check). §1: no separate `v3ref` target (`v4_tests` includes the core/ headers).
  §5.3: manifest `inputs` keys are file paths; the CLI verifies each `.bin` content hash before running.
- v0.1.2 (2026-11-15, WP1; review PR11 #1, #2, #5, #7, #8, #9, #12) — **§4.2 / §7(4): one store-owning `Ledger` per
  island; per-thread `ThreadLedger`s with bounded offer buffers, absorbed at stage ends in thread-index order; shared
  monotone cut-off `Store::cutoff()` for quick rejects** (replaces per-thread full ledgers). §4.1 staging compaction
  (peak ≈ 2.5c). §3: I accept slot = `SLOT_ACCEPT` (0xFFFFFFFF), π₀ uniforms at slots 0…u−1; `CheckedSource` for I5;
  compat tiers 0–1 only. §5.1: header `content_sha256` covers header + table (the file content hash); mode 0 = none;
  u64 in JSON as hex strings; data identity by section hashes (`X_sha256`, `y_sha256`). §5.3/§6: binary block in every record and meta; `require_fma_variant()` at every command.
  §7: prep data outcomes exit 20/21. §1/§8: file names and runner description corrected (no `types.h`).
- v0.1.3 (2026-11-15, WP1; re-check R1, R2; NOTS libm result) — §5.1: file identity = content hash (manifests, merge
  input validation, restart); data identity across builds = named data sections of raw/data files only; T2 compares
  non-meta section hashes; the merge checks binary consistency across islands; restart refuses a different binary
  block. §3: CMake option `V4_CHECK_ADDRESSES` → `v4::kCheckAddresses`. §6: bit form uses only log/exp/lgamma/sqrt;
  log1p/expm1 are class A only (`pm::machine::`); the guard is `require_bit_libm()` = function-result self-test, not
  the libm file hash. Store/ThreadLedger refuse NaN values (internal_error).
- v0.1.4 (2026-11-15, WP1; D-18; PR14 review F1–F3) — §5.1/§2: `setup.bin` no longer stores `codes_by_size` / `sub_cum`
  (recomputed on demand per selected block, same bits). §6: x87 `expl`/`logl` rows in the self-test guard; `info` skips
  the self-test. §5.1: `binary_compatible()` is the one binary-consistency rule; `git_commit` with `-dirty`.
- v0.1.5 (2026-11-15, WP1; Sol review EXP_CP1 F4, F10, F11) — §3: the address domain made explicit and injective
  (field widths and limits, destination particle, slot kinds ORDER / RESAMPLE / PI0_SIZE / PI0_BLOCKSIZE /
  PI0_SUBMODEL / MOVE_J / MOVE_L / ACCEPT); I5 test over a full multi-rebuild calibration. §4.2: EventKey assignment
  per event kind along the serial reference traversal (tier, iter, within-step ordinal `sub`); logical events by
  mechanism (feasible G = 2 events; cap, self-loop and no-score cases); table counts once per table-ingesting ledger,
  inherited 0; I4 corrected (`i4_expected`). §5.3: `reference` (pinned core commit, file hashes, compiler, flags, libm).
  §2: neighbour graph ≤ pB selections / ≤ 2pB entries, no per-column maximum.
