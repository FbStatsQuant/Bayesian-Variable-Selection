# INTERFACES — engine v4 contract between WP1–WP5

**v0.1.25 (binding; changes only by the WP1 owner with a changelog line).** 2026-11-18. Source: ENGINEERING_SPEC §0-v2,
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
- **`smcbvs4 merge` argument forms** (WP4, PR #33):
  - **Driver form:** `merge --manifest merge.json --out fit.bin [--threads k] [--mem-budget BYTES]`. The manifest is
    authoritative:
    - R′ = `params.Rp`; the mode is the manifest's `mode`;
    - inputs are found by base name among the manifest's `inputs`: `data.bin`, `setup.bin`, `calib.bin` and
      `island_<r>.bin` for r = 1…R′ (leading zeros allowed, at most 9 digits);
    - any explicit `--Rp`, `--islands`, `--data`, `--setup`, `--calib` or `--mode` that **disagrees** with the manifest
      is refused (`invalid_input`, exit 13), in either argument order; agreeing ones are accepted.
  - **Explicit form:** `merge --data D --setup S --calib C --islands i1,…,iR --Rp R --mode compat|law|V --out fit.bin
    [--threads k] [--mem-budget BYTES]`. `--islands` is a comma list or a JSON array of exactly R′ distinct paths;
    island r = position r.
  - In both forms `--out` is required. `--mem-budget` is a whole number of bytes in [0, 2⁵⁰] (0 = off; `--mem-budget-gb`
    is an alias; giving both is refused).
  - Exit codes (§7): 0 completed, 11 `resource_limit` (including not admitted), 13 `invalid_input`, 14 `io_error` (a
    missing island file).
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
  `logr` for codes `0..2^{m_b}−1` at `logr[code_ptr[b] + code]`, NaN where |U| > K. **`code_ptr` has J + 1 entries, like
  `blk_ptr` and `nb_ptr` (CSR): `code_ptr[0] = 0`, `code_ptr[b+1] − code_ptr[b] = 2^{m_b}`, `code_ptr[J] = |logr|`
  (v0.1.19).** Code bit i ↔ i-th member
  (`core/cpp/v3_start.h:76-98`). `logprof` (with `logprof_ptr`), `logF` ((J+1)×(K+1) row-major), `size_logmass` and
  `size_cum` retain the core values and bits (`core/cpp/v3_start.h:101-157`). **`cond_ptr` and `cond_cum` are not stored
  (D-31)**: `cond0` is f64 J×(K+1), b-major, with `cond0[b*(K+1)+r]` equal bit-for-bit to entry 0 of core's conditional
  cumulative row (b, r) (`core/cpp/v3_start.h:140-150`); on reachable rows this is P(k_b=0 | remaining r).
  `cond_row(T,b,r,out)` reconstructs the whole row from `logprof` and `logF`, with exactly the core operation order and
  bits; its length is min(top_b,r)+1, where top_b = logprof_ptr[b+1] − logprof_ptr[b] − 1; all-minus-infinity rows contain
  zeros and are never reached by a valid draw. For 0≤b<J, 0≤r≤K and 0≤u<1, `pi0_block_size(T,b,r,u)` returns 0 iff
  u < cond0[b*(K+1)+r], otherwise the `upper_bound` index on that row. The caller-scratch forms (`CondScratch`,
  `DrawScratch`; `Start::draw_pi0(…, DrawScratch&)`) perform no heap allocation. Gate: identical row bits, models and
  uniform consumption with and without stored rows, against core. **`codes_by_size` and `sub_cum` are not stored
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
  void compact();     // sort the staging run, merge it with the kept run (one entry per model, its best value), keep the first cap
  void merge(const Store& o);                       // = offer every entry of o, then compact()
  void load_unique_sorted(size_t n, const double* v, const uint64_t* hash, const uint64_t* off, const uint16_t* len,
                          const int32_t* pool, size_t pool_n);   // bulk load of a valid store into an EMPTY one (n ≤ cap)
  double cutoff() const;                            // −inf until cap entries are kept, then the worst kept value
  bool would_enter(double v, ModelView S) const;    // after compact(): cap not reached or better than the worst kept
};
```
After `compact()`: entries strictly sorted under `ord`, **one entry per model**, size ≤ cap (invariant I1;
`check_invariants` verifies one-per-model by an independent (hash, model) sort). One entry per model is verified
**assuming correct hashes**: the readers named here check each stored hash against its model's Zobrist hash
(WP4 `read_store` / `load_island_full`; WP3 `read_island_file` with `verify`); WP5's `load_fit` checks one entry per
model by (hash, model) only and relies on fit.bin's own content hash (v0.1.17, review PR45 MINOR-4). Staging is compacted when it reaches
max(cap/4, 4096) entries, so the peak is ≈ 2.5·cap entries (kept + staging + the new kept run with room). An entry
costs **30 + 4k bytes** kept (26 + 4k data, plus 4 for the one-entry-per-model index), plus about 9 B per entry
transient inside `compact()`. **Bulk load (v0.1.14):** a store that is already valid (island records and files,
stored sections) is loaded with `load_unique_sorted`. It verifies the strict order, the pool ranges and one entry per
model, refuses invalid input with `invalid_input` (the store is left empty), and runs no compaction. Preconditions:
the target store is empty (else `internal_error`); n > cap is refused, never truncated (the offer path would
truncate). For **valid** input its content equals the offer + compact path, bit for bit.
`cutoff()` is **monotone non-decreasing** (the worst of the top-c of a growing set never decreases) and is published
atomically, so other threads may read it at any time. Caps: top = 40p + 1 (HPM order, value F); lead0 = 20p (LEX,
value lg0); lead1 = 20p (LEX, value F). Leader stores exist only inside calibration, where they feed V (D-7). **Final-run
leader stores are not engine outputs in any mode, compat included** (D-7, confirmed safe by Theory PSMC-S0): final-run
ledgers are built with `leaders = false`, and compat comparisons against v3 put v3's final `leaders` on the exclusion
list.

**Values (v0.1.13; WP3_ARCH_REVIEW R7).**
- **Bit form:** a model's value is a deterministic function of S, so duplicates are equal entries.
- **Class A:** values are path-dependent maxima. A model reached by two flips can carry two class-A values. The store
  keeps each model once, with the larger value, and the HPM provenance is the first event (smallest key) with that
  larger value. This is deterministic and T3-invariant.
- Every store (island, reference `Store`, merge) therefore holds **one entry per model, with its best offered value**,
  and its content is the top-c of distinct models by best value, independent of offer order.

**Offer floor (v0.1.15; D-29; V-mode final islands only).** A V-mode final island may run its top store under an
**offer floor** f = calib.bin `meta.tau_cal` (§5.1):
- the store drops an offer iff v < f (**ties are kept**), in addition to its own cut-off rule. I1 is unchanged;
- HPM and provenance, `logical` counters, `island_best` and every Tally field still see **every** event (V counts every
  consumed score; a dropped offer still counts);
- the island store is then "the top c of the offers with v ≥ f" and may hold **fewer than c** entries.

**An island store under a floor has no standalone meaning.** It is not that island's top c, and no consumer may use an
island store on its own (as a per-island log Z_T, PIP_T, top-c or occupancy). Only the **merged** store has meaning;
it equals the unfloored merge because the merge's pre-island cut-off (tables + inherited) is ≥ τ_cal ≥ f (§7, merge
check). f = −∞ means no floor and is required for compat and law islands and for every calibration island (pilot and
diagnostic), whose ledgers define τ_cal.

**Where the floor lives and where it comes from (v0.1.17; review PR45 MINOR-1, MINOR-2; WP7 O6):**
- The floor is a constant of the island's **top** store only (`TopStore::floor`, set from `IslandConfig::offer_floor`
  before the run). The effective reject threshold of an offer is max(`cutoff()`, f). `cutoff()` itself is unchanged
  (still −∞ below c entries), and `compact`, `merge(Store)`, `load_unique_sorted`, `would_enter` and the duplicate filter
  never apply the floor. Leader stores never have one.
- A final island gets f from its calib.bin: f = `meta.tau_cal_hex` when the mode is V, else −∞; a calib.bin without
  `tau_cal` (fewer than c inherited models, older files) gives −∞ (`include/v4/offer_floor.h` `offer_floor_from_calib`).
  The `island` command passes it as `IslandConfig::offer_floor` with `offer_floor_calib` = that calib.bin's content hash,
  **after the same semantic check `read_calib` makes** (`wp4io::check_calib_tau_cal`, light: mapped arrays): the
  inherited models are **distinct** (strictly increasing in the exporter's lexicographic order, else proved by a sort;
  duplicates → `invalid_input`) and `tau_cal_hex` is bit-equal to the c-th best F over those distinct models (c = 40p + 1;
  −∞ below c). A tampered finite tau_cal is refused by the command before any island work (review PR54 MAJOR-1/2).
- The island side enforces the roles: `run_island` refuses (`invalid_input`) a floor > −∞ unless the island is class A
  (V), not compat, without leader stores and in the final role; it refuses a NaN or +∞ floor and a floor without its
  calib hash. Calibration islands never write an `island_r.bin`, so this, not the merge, is their guard. The floor is
  in the checkpoint fingerprint: a resume under another floor is refused.
- Every `island_r.bin` field other than `top_*` is floor-independent: log Z_r, `pip_r`, `rb_*`, the stage table and
  ess, terminal supports, HPM and provenance, `logical`, `island_best` (review PR45 INFO-3; island_run.h writes nothing
  else derived from its store, and `meta.cost`'s store columns are execution statistics, not science).

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
  // offers: dropped if v < max(island.store.cutoff(), floor) (floor: the top store's D-29 offer floor, else -inf);
  // else appended to a bounded OfferBuffer (one per store);
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

  **Every inherited-step offer of the calibration HPM model carries that model's CALIBRATION EventCtx (its calibration
  provenance), never an INHERITED key**, so the smallest-key rule reproduces v3's provenance replacement
  (`core/cpp/v3_core.cpp:428-440`) instead of yielding "inherited"; all other inherited models carry INHERITED keys. Provenance = the smallest key among the
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
  (V) needs both libm self-tests passed, equal flags and libm binding, **and one class-A FMA family** (D-32, v0.1.18:
  `island_fma`, else known `island_isa` names; the V merge also checks every island against calib.bin's block); merge
  (theory mode) also needs equal git
  commits that are clean (no `-dirty`) and known; a checkpoint restart also needs the same executable (sha256) and git
  commit. `git_commit` = 40-hex HEAD + `-dirty` when tracked files differ, refreshed at every build.
JSON numbers are doubles: every u64 value (hashes, Zobrist keys, large counters) is written as a hex string `"0x…"`.
Sections (names fixed; WPs may add sections, never rename):
- `raw.bin` (gen): `X_cm` f64 n×p, `y` f64 n, `meta`. `truth.json`: design, params, seed, S₀ (1-based), β*, σ*.
- `data.bin` (prep): `Xs_cm`, `ys`, `z`, `diagG`, `col_max`, `col_mean`, `col_sd`, `kept` i32 (1-based), `dropped`
  i32, `meta` {n, p_raw, p, K, yty, logCn, logm0, logWK, y_max, y_mean, y_sd_scaled, prep_class: "B"|"A"}, `logw`, `logprior`.
- `setup.bin` (WP2): `nb_ptr` i64, `nb_idx` i32, `dup_ptr/dup_idx`, `cut_ptr/cut_idx`, `blk_ptr/blk_members`, `blk`,
  `pos`, `code_ptr` (J + 1 entries, `code_ptr[J] = |logr|`), `logr`, `logprof_ptr/logprof`, `logF`, `size_logmass`, `size_cum`,
  **`cond0`** (f64 J×(K+1), b-major; D-31), `mode_S`, table top stores `tstore_{top,lead0,lead1}_{v,off,len,hash,pool}`, `meta`.
  **`setup.bin` carries no `meta.stores`** (v0.1.19): the table stores' caps and orders are §4.1's (top 40p + 1 in HPM
  order, lead0 and lead1 20p in LEX order); a reader derives them and ignores any `meta.stores` it finds. (`calib.bin`,
  `island_r.bin` and `fit.bin` do carry `meta.stores`, as written by `add_store`.)
- `calib.bin` (WP4):
  - always: `grids_all_ptr/grids_all`, the stage records (when any island ran) and `meta`;
  - **only when the status is ok:** the calibration stores (as stores), HPM (`hpm_S`, `hpm_ev`), `logical` u64
    [N_PHASE × N_MECH] and the inherited models (`inh_*`); otherwise `meta.has_hpm` = false and the HPM so far is in
    `meta`, labelled incomplete. `grid` (the frozen grid) when a grid was frozen;
  - `meta` {tier, N, L, Hm, I_used, flags, triggers, ...}, including:
    - **`k_store`** (double): the calibration top store's mean stored |S|, i.e. the k of §7's admission rule; present
      only when the status is ok;
    - **`iterations`**: one row per rebuild with `tier`, `iteration`, `grid_label`, `complete`, `logZ_r` and
      `island_best` (null for −∞); `overall_best` and E1–E3 **only when `complete`**;
    - **`tau_cal`** (v0.1.15, D-29; f64): the offer floor for V-mode final islands = the **c-th best F**, c = 40p + 1,
      in HPM order, over the distinct inherited models that this calib.bin exports; **−∞ if there are fewer than c**
      (no floor). Written only for a completed (status ok) V-mode calibration. Encoding: `tau_cal_hex` (the f64 bits,
      "0x…", authoritative) and `tau_cal` (number, "-Inf" for −∞; for reading);
  - **`stage_stream`**: the initial-draws hash and the stream positions (start and end) of each calibration island;
  - **`inh_d`**: d of each inherited model, **on the flat-export path only** (`inh_ptr/inh_idx`); the legacy `inh`
    model path has no `inh_d`.
- `island_r.bin` (WP3; `include/v4/island/island_file.h`):
  - `meta` holds r, N, T, L, Hm, p, status, reason, inputs, binary, timings, `logZ_hex` and `init_hash`.
  - **Offer floor (v0.1.15, D-29):** `meta.offer_floor_hex` (f64 bits, "0x…", authoritative), `meta.offer_floor`
    (number, "-Inf" = no floor) and `meta.offer_floor_calib` (the content hash of the calib.bin whose `tau_cal` it is;
    null when the floor is −∞). An island store written under a floor > −∞ is the top c of the offers v ≥ floor (§4.1)
    and has no standalone meaning. A file without these keys has floor −∞.
  - Schedule: `grid` f64 [T+1].
  - Stage table (f64 / i32 [T]): `st_phi`, `st_ess`, `st_inc`, `st_cum`, `st_distinct_res`, `st_distinct_moved`.
  - Moves: `st_moves` u64 [T × 12] (MoveStats in records.h field order, `gibbs_cap` included); `term_moves` u64
    [(L + Hm) × 12] (burn-in rounds, then measured rounds); `term_distinct` i32 [L + Hm].
  - Store: `top_v`, `top_hash`, `top_off`, `top_len`, `top_pool` (compacted, sorted).
  - HPM: `hpm_S` i32 [k]; `hpm_val` f64 [2] (F, log m); `hpm_ev` i64 [12] (seg, tier, iter, unit, xph, stage, round,
    particle, position, sub, phase, mech).
  - `island_best` f64 [r + 1] (entry r = this island's maximum, the others −inf); `logical` u64 [N_PHASE × N_MECH].
  - Estimates, written only if status = completed (GUARD-W): `logZ` f64 [1], `st_inc`, `st_cum`, `rb_acc` and `pip_r`
    f64 [p], `rb_round` f64 [**Hm** × p].
  - Terminal supports, also completed only: `terminal_S_ptr` i64 [N + 1] and `terminal_S` i32, the N supports after the
    last measured round, in particle order (WP4: occupancy, Ẑ_occ).
  - `meta.cost` (D-30; WP7 O2, review PR49): **the authoritative per-step execution record**, schema `smcbvs4.cost/1`,
    written when the island ran at least its initial draws (any status). Header: r, role, tier, iter, N, p, m (= p + B +
    2), threads, G, tile, kernel, arith, segment. `rows` = the rows closed: completed = T + L + Hm + 2 (step 0 = the
    initial draws, the T bridge stages, L burn-in and Hm measured rounds, then the exit row); a stopped island = its
    closed steps + the exit row. `columns` = one array per `StepCost` field (`include/v4/island/island.h`), one entry
    per row (a new column `t_compact_lead` since v0.1.25: the wall seconds the two leader stores of a calibration island
    spent compacting; 0 on final islands); `flips` = `KernelStats::flip_evals`, the addition flips evaluated on fast supports (K1: with bounded
    scoring only those it scores). Rows are contiguous intervals of the island's lifetime: a row closes right after its step's ledger sync
    (before that step's checkpoint, whose seconds go to the next row) and is final then; the exit row (kind 4) covers
    the last checkpoint, a failed or interrupted partial step, the I1 check on exit and the result assembly. The
    checkpoint carries the rows and the lifetime totals at the last close, so after a resume (segment = resumes before
    the row) the rows sum exactly to the island's totals (counts) and to `t_total` (seconds). After a resume these are
    the totals of the work the result continues from: the dead job's work after its last row close (its last
    checkpoint write, exit check and assembly, and any partial step) is in neither, so `t_total` is not the sum of the
    job segments' wall times (use the scheduler's accounting for that; review PR49 re-check NIT-1). Values: counts are JSON
    numbers (a bounded-count exception to the hex rule of this section: per-row counts are exact below 2^53, and the
    writer refuses more); a field the row's kernel does not measure is `"NaN"` (the particle-major kernel measures
    particle_rounds, t_pm, the store, check, checkpoint and memory fields; the label-major kernel all but t_pm). The
    exit row's `phi` is `"NaN"` too, as are the fields its kernel does not measure (NIT-2).
    Execution statistics only: not in `IslandRun::hash` / `meta.output_hash` nor in any non-meta section hash (T2, the
    merge never reads it); like all of `meta` it is in the container's content hash.
  - The sidecar `IslandConfig::cost_path` is a **non-authoritative progress log** of the same rows (a header line, one
    JSON line per row, one `write()` each). At the first row close of every process (job segment) it is rebuilt from
    the rows the run continues from (a segment killed before its first close leaves the old file until the next
    process rebuilds it; NIT-3); a write failure cuts it back to whole lines and disables it without failing the island. Calibration
    islands get it from `calibrate --cost-dir` (WP7 O5), one file per calibration island
    (`cost_<pilot|diag>_t<tier>_k<iter>_r<island>.jsonl`).
- `fit.bin` + `fit.json` (WP4): merged `top_*` (the only store with meaning when islands ran under a floor, §4.1), `hpm_*` + provenance, `hpm_before_local_*`, local-search archive,
  `mode_S`, LS0, near ties, `logZ_r`, `pip_eq`, `pip_Z`, `pip_T`, `rb_*`, flags; `fit.json` scalars and hashes only.
  v0.1.18 (WP7 O5): `fit.json` also carries `island_isa` (D-32 (4), the merge binary's) and `timings` (as fit.bin
  `meta.timings`): `merge_tail_seconds` (the whole command), `merge_islands_seconds` (island stream + merge),
  `tail_local_seconds` (final local search), `ls0_seconds` (LS0); execution statistics, not hashed (meta).
  No leader stores in `island_r.bin` or `fit.bin`, in any mode (§4.1; on the compat exclusion list).
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
             "island_isa": "sapphirerapids", "island_fma": true,
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
  differ, and so are the x87 rows (MEASURED, `results/PMATH_NOTS.md`, jobs 2747666 and 2747875).
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
enum class Status : uint8_t { completed=0, resource_limit=1, numerical_failure=2, invalid_input=3, io_error=4, internal_error=5,
                              schedule_limit=6 };   // exit 16; theory/compat calibration only (v3: tier-1 grid failure, no fallback)
struct Error : std::runtime_error { Status st; };                // thrown inside the engine
struct NumericalFailure : Error { };                            // = core/cpp/v3_util.h:26-28 semantics
Status fit_status(span<Status>);   // first that applies: invalid_input, internal_error, numerical_failure, resource_limit, schedule_limit, io_error, completed
```
- Commands catch everything at `main`, write `<out>.json` with `status`, `reason`, and exit with `0` (completed) or
  `10 + status`. `schedule_limit` (exit 16) is the theory/compat calibration outcome of `core/v3_calib.R:170`: tier-1 grid
  construction failed and no fallback grid exists. It cannot arise in V-1M (D-26). No estimate field is written unless status is `completed` (GUARD-W). Invariant violations (I1–I7) →
  `internal_error`. Hash or format mismatch at start → `invalid_input`. Write/rename failure → `io_error`.
- **Resumable stop (v0.1.23, WP7 O4).** `smcbvs4 island --stop-after-s S` (S > 0 seconds, measured from the start of the
  command; needs checkpoints) is a soft stop: at the first step boundary after S seconds, before the last step, the island
  writes a checkpoint and exits with code **22**. Like the prep outcomes (20 / 21) it is not a failure and not a
  completion: the record has `status` "completed", `island_status` = "interrupted_resumable" (also `stopped_after_step`,
  `resumed_from_step`, `reason`), and **no `island_bin` and no island file**. A rerun with the same arguments resumes from
  `island_r.ckpt.{a,b}`. `--stop-after-s` with `--ckpt 0` or S <= 0 is `invalid_input`. The WP5 driver's restart chain
  (`restart` plan key) treats 22 as "attempt ended cleanly, resume next".
- **Memory admission (`--mem-budget`, bytes; 0 = off).** It is the **whole task's** memory, not the island store's.
  The island's peak-live plan (`include/v4/island/memory.h`, WP3) counts:
  - X, z and diag(G);
  - the store with its sort scratch and staging growth;
  - the leader stores when they are on;
  - one stale snapshot generation;
  - the setup inputs (tables, neighbour graph), whose size the **caller** supplies.

  Admission at task start plans the store with model size **k = max(q90(π₀ size) + 1 from setup, calibration's
  measured mean |S| when calib.bin exists, i.e. `calib.bin` `meta.k_store`, §5.1)**. At p ≥ 10⁵:
  - a final island without a calib.bin k is refused with `invalid_input`;
  - calibration islands, which run before calib.bin exists, use the setup-derived k.

  Over budget, admission refuses deterministically with `resource_limit`, before any allocation. The check at every step boundary uses the store's **actual** size. With G = 0
  the island chooses the largest G ≤ 256 that fits. The merge applies the same rule to its own plan (`merge.h`, WP4).
- **Merge check of the offer floor (v0.1.15, D-29; WP4).** After the tables and the inherited models are offered to
  the pre-island ledger, and before any island is merged, every island must have:
  - floor = −∞ unless `meta.mode` = "V" (compat and law islands with a floor are refused; calibration islands are
    refused on the island side, §4.1, since they write no `island_r.bin`; v0.1.17, MINOR-2);
  - a floor is −∞ or finite (NaN, +∞ → `invalid_input`; v0.1.17, MINOR-3); an island's `meta.mode` must equal its
    container header's mode, and a finite floor needs `meta.mode` = "V" (`head_island`; review PR54 MINOR);
  - floor > −∞ only with `offer_floor_calib` = the island's `meta.inputs` calib content hash, **and `offer_floor_hex`
    bit-equal to that calib.bin's `tau_cal_hex`** (v0.1.17, MINOR-3; `read_calib` also checks that `tau_cal` is the
    c-th best F of the inherited models it reads);
  - **floor ≤ `pre.top.cutoff()`** (`≤`, not `<`: offers equal to the floor are kept).

  (`merge::offer_floor_refusal`; a refused island is `Load::floor_refused`.)

  Otherwise the merge refuses with `invalid_input` and writes no estimate (GUARD-W). The merge's memory estimate is
  unchanged (its kbar from the island store sections stays an upper bound).
- **Calibration memory rule** (WP4; effective with WP4 PR #46, `exp/P1M-wp4-calib2`, review PR37 N-1/N-2):
  - Calibration islands receive `mem_budget` = the whole task's budget, and `resident_bytes` = the calibration
    process's own state: the calibration ledger plus the inherited export. Data and setup inputs are excluded, because
    the island's own plan counts them.
  - A calibration island is admitted iff resident_bytes + its plan ≤ mem_budget.
  - `calibrate` refuses up front (`resource_limit`, before any allocation) iff resident + inputs + one island ledger >
    `--mem-budget`. Its plan's k = max(8, q90(π₀ size) + 1), from setup.bin `size_logmass`.
- **Data outcomes of `prep`** (v3 returns them as fit outcomes with an empty HPM, `core/v3_preprocess.R:111-114`):
  `no_predictors` and `y_constant`. The task status is `completed`, the record has `prep_status` and `hpm: []`, no
  `data.bin` is written, and the exit code is **20** (`no_predictors`) or **21** (`y_constant`). The driver (WP5) ends
  that fit's pipeline and records the outcome; it never starts `setup`.
- **Threads: OpenMP** (`--threads k`, default `OMP_NUM_THREADS`). Rules: (1) no result depends on the thread count or
  schedule; (2) work is cut into **fixed chunks independent of the thread count** (default 64 items; label blocks and
  tiles are parameters, not part of the law); (3) floating-point reductions sum per-chunk partials, then combine chunk
  results serially in chunk order; no floating atomics, no `omp reduction` on floats; (4) **one `Ledger` (stores) per
  island (or merge job). Island stages: one `ThreadLedger` per worker with bounded offer buffers, absorbed at stage
  ends in thread-index order; quick rejects against the island store's monotone cut-off (§4.2). The tail (final local
  search, LS0): no `ThreadLedger`, because its early flushes are irrevocable. Instead it uses chunk-ordered wave
  buffers of at most 4·threads·chunk offers, filtered by `v ≥ cutoff()` read at the wave start, and applied in chunk
  order after each wave. On a numerical failure, the failing chunk's earlier offers are applied and later ones are
  dropped. This is exact and thread-invariant, including on the failure path (HPM incomplete)**; (5) uniforms come only from addresses, never from thread state; (6) the stage barrier
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
- v0.1.6 (2026-11-15, WP1; PR15 review) — §4.2: the inherited calibration HPM is offered with its calibration EventCtx
  (never an INHERITED key). `gen::generate_test_rows` (rows [a, b), same bits as the full test design). §6: the x87
  rows are measured equal on NOTS (job 2747875); all 8 guarded rows match there.
- v0.1.7 (2026-11-15, WP1; D-26, D-7 / PSMC-S0) — §7: status `schedule_limit` (6, exit 16; theory/compat calibration
  only; fit precedence after `resource_limit`). §4.1/§5.1: final-run leader stores are not outputs in any mode; compat
  comparisons exclude them.
- v0.1.8 (2026-11-16, WP1; PR21 review m1) — §5.1 `island_r.bin` aligned with WP3's code (no code change): `st_moves`
  T × 12 (`gibbs_cap`), `rb_round` Hm × p, terminal supports N, and the sections `grid`, `term_moves`, `term_distinct`,
  `hpm_val`, `hpm_ev`; estimate sections (incl. `st_inc`, `st_cum`) only when completed.
- v0.1.9 (2026-11-16, WP1; PR16 re-check) — §7(4): the tail (final local search, LS0) uses chunk-ordered wave buffers
  (≤ 4·threads·chunk offers) with the cut-off filter instead of `ThreadLedger`; exact and thread-invariant on the
  failure path. Island stages keep `ThreadLedger`.
- v0.1.10 (2026-11-16, WP1; WP3 PR #24 fixes) — §7: `--mem-budget` is the whole task's memory. The island plan counts
  X, z, diag(G), sort scratch, staging growth, the leader stores when on, one stale snapshot, and the caller-supplied
  setup input size. Admission uses calibration's mean |S| when given; the step-boundary check uses the store's actual
  size.
- v0.1.11 (2026-11-16, WP1; WP4 PR #33) — §1: `smcbvs4 merge` argument forms (driver form with an authoritative
  manifest, where a disagreeing explicit argument exits 13; explicit form; base-name input rules; `--mem-budget` range;
  exit codes).
- v0.1.12 (2026-11-16, WP1; PR #26 re-check m2) — §7: the admission plan's k = max(q90(π₀ size) + 1 from setup,
  calibration's mean |S| when calib.bin exists). At p ≥ 10⁵ a final island without a calib.bin k is `invalid_input`;
  calibration islands use the setup-derived k.
- v0.1.13 (2026-11-16, WP1; WP4 PR #37, WP3_ARCH_REVIEW R7) — §5.1: `calib.bin` `meta.k_store` (calibration top store
  mean |S|), cross-referenced from §7 admission. §4.1: class-A values are path-dependent maxima; every store keeps one
  entry per model with its best value (the reference `Store` now de-duplicates by model; deterministic, T3-invariant).
- v0.1.14 (2026-11-16, WP1; PR40 review follow-ups) — §4.1: `Store::load_unique_sorted` (verified bulk load of a valid
  store, used for island records / island files / stored sections; same bits as offer + compact); I1 includes one entry
  per model, checked independently of the index; entry cost 30 + 4k bytes. §5.1 (WP4 PR #37 re-check): `calib.bin`
  `meta.k_store` (only when the status is ok), `meta.iterations`, the `stage_stream` and `inh_d` sections. §7: the
  calibration memory rule (islands get the task budget plus resident bytes; up-front refusal; plan k from setup).
- v0.1.15 (2026-11-16, WP1; PR45 review MINOR-1–4; D-29 / reviews/D29_WP4_answer.md) — §4.1: `compact()` comment (one
  entry per model, best value); `load_unique_sorted` preconditions (empty target, n ≤ cap, same bits for valid input);
  one entry per model assumes correct hashes, and untrusted readers check hashes. §5.1 `calib.bin`: which sections are
  conditional (status ok; `complete` rows; `inh_d` flat path only). **D-29 offer floor (contract; builder 7 implements,
  O6):** `calib.bin` `meta.tau_cal`; `island_r.bin` `meta.offer_floor` + `offer_floor_calib` (drop only v < floor, ties
  kept); §4.1 a floored island store has no standalone meaning; §7 merge refuses (`invalid_input`) unless
  floor ≤ cut-off after tables and inherited, and floor = −∞ outside V final islands. §7's calibration memory rule
  marked effective with WP4 PR #46.
- v0.1.16 (2026-11-17, WP7 O2 for WP1; D-30; review PR49) — §5.1: `island_r.bin` `meta.cost`, the authoritative per-step
  cost record (schema `smcbvs4.cost/1`; contiguous final rows + an exit row, lifetime totals across resume; counts as
  bounded JSON numbers; unmeasured fields "NaN"; outside the scientific-output hashes, inside the container hash), and
  the non-authoritative JSON-lines progress log. Numbering: WP1's v0.1.14–v0.1.15 (PR #45) precede it; D-29's O6 line
  is v0.1.17. The header line moves to v0.1.16 when PR #45 lands (WP1).
- v0.1.17 (2026-11-17, WP7 O6 for WP1; D-29; reviews/PR45_recheck.md MINOR-1–4, INFO-3) — §4.1: the floor is a constant
  of the island's top store (effective threshold max(cutoff, f); the other store operations unchanged); its source
  (calib.bin `tau_cal_hex` for V final islands, else −∞; `offer_floor.h`); `run_island` refuses a floor in compat, law,
  leader or calibration islands and NaN / +∞ floors; the floor is in the checkpoint fingerprint; every `island_r.bin`
  field but `top_*` is floor-independent. §4.2: the offer reject line names the floor. §7 merge check: V mode only, the
  floor bit-equal to calib.bin's `tau_cal_hex`, NaN / +∞ refused, calibration islands guarded on the island side.
  §4.1 hashes: the named readers check them; `load_fit` relies on fit.bin's content hash. (O2's `meta.cost` line is
  v0.1.16.)
- v0.1.18 (2026-11-17, WP7 O5 for WP1; D-32 revised 11-17; review PR55 m4, m6) — §5.3 binary block: `island_isa` (the
  island sources' -march, "x86-64-v3" for a V4_WIDE_ISA build without one, else "portable") and `island_fma` (whether
  class A uses a true FMA, from the class-A unit itself); binary consistency: the V merge needs one FMA family, island
  against island and against calib.bin. §5.1 `fit.json`: `island_isa` and `timings` (merge, tail local search, LS0
  seconds). §1 commands: `info --meta 1` prints a file's meta section; `calibrate --cost-dir DIR` (one D-30 progress
  log per calibration island) and `--verbose 1` change no output bit (tested); the tool `v4_pilot_island`
  (`include/v4/island/pilot_only.h`) runs the first island of `calibrate --mode V` alone (H-11's 10⁶ pilot). (O6's
  offer-floor line is v0.1.17.)
- v0.1.19 (2026-11-16, WP4; manager decision 11-16 on PR #46, WP3's finding that `read_setup` could not read WP2's real
  setup.bin) — §2 Tables / §5.1 `setup.bin`: `code_ptr` has **J + 1 entries** like `blk_ptr` / `nb_ptr`, with
  `code_ptr[0] = 0`, `code_ptr[b+1] − code_ptr[b] = 2^{m_b}` and `code_ptr[J] = |logr|`; `setup.bin` carries **no
  `meta.stores`**, the table stores' caps and orders being those of §4.1. WP4's `read_setup` / `write_setup_min` adapt
  (WP2's writer already conforms); WP3's `load_start` accepts the J + 1 form. (v0.1.14–v0.1.18 are in PRs #45, O2, O6 and
  O5 (#55); this line is numbered after them.)
- v0.1.20 (2026-11-17, WP2 for WP1; D-31; PR #50 re-check F1) — §2 / §5.1: `setup.bin` no longer stores `cond_ptr` /
  `cond_cum`; it stores `cond0` (f64 J×(K+1), b-major, entry 0 of each conditional row = P(k_b=0 | r)). `cond_row(T,b,r,out)`
  recomputes a row with the core's bits; `pi0_block_size(T,b,r,u)` = 0 iff u < cond0, else `upper_bound` on the row; draws
  are allocation-free with caller scratch. A setup.bin without `cond0` is refused by the reader. Numbering: v0.1.15 (PR #45),
  v0.1.16 (O2), v0.1.17 (O6), v0.1.18 (O5), v0.1.19 (WP4's reader line) precede it; the header line moves with those PRs (WP1).

- v0.1.21 (2026-11-17, WP7 for WP1; review PR59) — §5.1 `calib.bin` `tau_cal`: computed (writer and reader) by an
  allocation-free radix select, bit-identical to the c-th largest value, with −0.0 treated as +0.0 (so the result is +0.0
  for a ±0 tie). The writer refuses a non-finite inherited F (`internal_error`). The distinctness proof of the inherited
  models is a linear scan for the exporter's canonical (strictly lexicographic) list, which has no size limit; any other
  order needs an index sort and is refused above 2^24 inherited models (`invalid_input`).
- v0.1.22 (2026-11-18, WP7 O4 for WP1; WP3_ARCH_REVIEW R5) — §5.1 `island_r.ckpt.{a,b}`: the checkpoint checksum is the
  parallel block checksum of `include/v4/island/ckpt_sum.h` (1 MiB blocks by stream position, FNV-1a 64 per block, FNV-1a 64
  over the length and the block hashes in order): a function of the bytes alone, independent of thread count and of the
  write / read chunking, so a checkpoint written with k threads resumes with any other. Magic `SMCV4CK2`; a file with the
  earlier magic (`SMCV4CKP`, serial FNV-1a) is refused with `invalid_input`, never treated as "no checkpoint".
- v0.1.23 (2026-11-18, WP7 O4 for WP1; R5) — §7: `island --stop-after-s S` and the resumable exit 22 (record `island_status`
  "interrupted_resumable", no island file); the checkpoint written at the stop is the ordinary `island_r.ckpt.{a,b}`
  (v0.1.22 checksum). Driver: plan keys `restart` (the islands' resubmission chain) and `t6` / `t6_only` (T6 by real kills,
  `tools/slurm/p1m_t6.py`).
- v0.1.25 (2026-11-18, WP7 O3 for WP1) — §5.1 `meta.cost`: new column `t_compact_lead` (the calibration islands' two
  leader stores' compaction seconds, a separate execution statistic; `t_compact` stays the top store's). Execution only:
  the leader stores of a label-major calibration island now compact by the same deferred parallel merge as the top store
  (all threads, between waves and at pass boundaries); their content, the leader order and every output bit are unchanged
  (tested against the particle-major serial reference, both arithmetics). The island memory plan counts the leader stores
  with the deferred-store peak when the island is deferred.
