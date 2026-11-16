# INTERFACES — engine v4 contract between WP1–WP5

**v0.1.1 (binding; changes only by the WP1 owner with a changelog line).** 2026-11-15. Source: ENGINEERING_SPEC §0-v2,
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
- **One binary** `smcbvs4 <command> [--key value ...]`, commands `gen prep setup calibrate island merge eval post info`
  (`info` prints a file's header and section table and verifies hashes). Every command takes `--manifest <json>` or flags,
  writes `<out>.json` (record + status) next to its binary output.
- CMake targets: `v4_bit` (static lib; flags **`-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`**, every kernel
  that must equal v3 bits), `v4_a` (static lib; class-A kernels; `-march=x86-64-v2` unless `-DV4_WIDE_ISA=ON` →
  `-march=x86-64-v3`, FMA only through explicit intrinsics / `std::fma`), `smcbvs4` (CLI), `v4_tests` (all unit + golden
  tests, own minimal harness `tests/tk.h`; it also compiles the core/ headers unchanged with the v3 flags for golden
  comparisons; links libquadmath), tools `v4_pmath_check`, `v4_bench_score`. C++20, GCC ≥ 11. OpenMP required. No network at configure or build time.
- Test runner: `engine_v4/tests/run_tests.sh [--quick|--full] [--threads k]` = configure + build (`make -j3`, `nice -n 19`)
  + run `v4_tests` + R golden scripts if R is present. Exit 0 iff all pass. Prints machine, compiler, flags, libm hash.

## 2. Core types (`include/v4/types.h`, `data.h`, `model.h`)
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
  `ptr.size() = p+1`, each row sorted ascending; content = `core/cpp/v3_blocks.h:149-170`.
- **Partition** (WP2): `struct Partition { int32_t J, B; std::vector<int64_t> bptr; std::vector<int32_t> members;
  std::vector<int32_t> blk, pos; }` — block b = `members[bptr[b]..bptr[b+1])`, sorted, packing order; `blk[j], pos[j]`
  as `core/cpp/v3_start.h:38`. Plus the duplicate components and the cut-group record (CSR each).
- **Tables** (WP2): `struct Tables { std::vector<int64_t> code_ptr; std::vector<double> logr; ... }` — block b's
  `logr` for codes `0..2^{m_b}−1` at `logr[code_ptr[b] + code]`, NaN where |U| > K; code bit i ↔ i-th member
  (`core/cpp/v3_start.h:76-98`). `logprof`, `logF` ((J+1)×(K+1) row-major), `size_logmass`, `size_cum`, `cond_cum`,
  `codes_by_size`, `sub_cum`: flat arrays + offsets, same values as `core/cpp/v3_start.h:101-157`.
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
**Address assignment (production; fixed by control flow before the value is read; spec §3 rule 1).**
| draw | xph | stage | particle | position | slot |
|---|---|---|---|---|---|
| initial π₀ draw of particle i | INIT | 0 | i (1-based) | 0 | 0,1,… in the π₀ draw's order (`core/cpp/v3_start.h:158-176`) |
| resampling uniform i at stage t | RESAMPLE | t | i | 0 | 0 |
| round order (Fisher–Yates step i = m−1…1) | BRIDGE (stage t) / BURN (round l) / MEASURED (round h) | t / l / h | i | 0 | m−1−i (draw order 0,1,…) |
| step at round position q (1-based) | same as its round | same | i | q | G: 0. U: 0 j, 1 l, 2 accept. N_b: 0 j, 1 l, 2 accept. I: 0…k−1 the π₀ draw, then k accept |
Unused slots (self-loops, empty N(j)\S) are simply not read. Calibration uses role PILOT/DIAG, `tier`, `iter`
(0 = pilot, k = rebuild k), island = diagnostic island r (pilot 0); diagnostic islands of different iterations
therefore get fresh addresses (law-equivalent to v3's continued streams; class L). Final islands: role FINAL, island r
= 1…R′, tier/iter = 0. `post` draws: role POST, xph POST. Debug builds log every address and assert uniqueness (I5).

**Compat mode** (`CompatSource`): ignores the address and returns the next `Xoshiro256ss::uniform()` of the unit's v3
stream (`core/cpp/v3_util.h:43-61`, copied), seeded `seed_stream(seed, stream)` with stream = 0 pilot tier 0, 1–4 diag
tier 0 islands 1–4, 5 pilot tier 1, 6–9 diag tier 1, 9 + r final island r = 1…4 (`core/v3_run.R:8-11`,
`core/cpp/v3_core.cpp:444`); streams 0–9 continue across rebuilds; 200 = test draws (`core/v3_setup.R:47`). Compat
code must request uniforms in exactly v3's serial order (`core/v3_run.R:24-37`); the address argument is then only a
label (debug builds check that the address sequence is strictly increasing in the serial order of §4.2). Checkpoints
store the xoshiro state and `count` in compat, nothing in production.

## 4. Store and Ledger (`include/v4/store.h`, `ledger.h`; reference implementation WP1, optimisation WP3)
### 4.1 Store: top-c of everything offered, independent of offer order
```cpp
enum class Order : uint8_t { HPM, LEX };    // HPM: v desc, |S| asc, lex asc; LEX: v desc, lex asc (core/cpp/v3_ledger.h:35-42)
struct Store {
  uint64_t cap; Order ord;
  std::vector<double> v; std::vector<uint64_t> off, hash; std::vector<uint16_t> len; std::vector<int32_t> pool;
  void offer(double v, ModelView S, uint64_t h);   // append to a buffer; compact() when buffer ≥ cap
  void compact();     // sort by ord, drop exact duplicates (same S), keep the first cap; rebuild pool in sorted order
  void merge(const Store& o);                       // = offer every entry of o, then compact()
  bool would_enter(double v, ModelView S) const;    // after compact(): cap not reached or better than the worst kept
};
```
After `compact()`: entries strictly sorted under `ord`, no duplicates, size ≤ cap (invariant I1). Caps: top = 40p + 1
(HPM order, value F); lead0 = 20p (LEX, value lg0); lead1 = 20p (LEX, value F); leader stores exist only in calibration
and compat mode (D-7). A model's value is a deterministic function of S, so duplicates are equal entries.

### 4.2 Ledger: events, HPM + provenance, counters, island_best; per-thread instances, deterministic merge
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
struct Ledger {
  bool has_hpm; Model hpmS; double hpmF, hpm_logm; EventCtx hpm_ev;
  Store top, lead0, lead1;
  uint64_t logical[N_PHASE][N_MECH];          // no `fresh` counters in production (OD-3); compat keeps them
  std::vector<double> island_best;           // index r = 0..R′
  void event(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx&, bool offer);
  void merge(const Ledger& o);               // order-free, see below
};
```
`event` counts `logical[phase][mech]`; updates `island_best[r]` for the island's own events exactly as
`core/cpp/v3_ledger.h:104-113`; if `offer`, offers to HPM and stores. `merge`: stores by top-c of the union; HPM by
`hpm_better`, and for the same model the **smaller EventKey** wins provenance (equals the serial "first score" rule);
`island_best` by max; `logical` by sum. Production offers every scored model (`offer = true`, no cache); compat
offers on fresh evaluations exactly as v3. Rule (spec §3.2): scores of labels a particle did not consume are not events.

## 5. Records and files (`include/v4/format.h`, `records.h`)
### 5.1 Binary container (every `.bin`)
Little-endian. Layout: `FileHeader` (128 B) | `SectionEntry[n]` (128 B each) | sections, each starting at a 64-byte
aligned offset. Written to `<name>.tmp.<pid>`, fsync'd, renamed. Readers mmap read-only and verify every hash.
```cpp
struct FileHeader {               // 128 bytes
  char magic[8];                  // "SMCBVS4\0"
  uint32_t format_version;        // 1
  uint32_t kind;                  // 1 raw, 2 data, 3 setup, 4 calib, 5 island, 6 fit, 7 law, 8 ckpt, 9 eval
  uint32_t mode;                  // 1 compat, 2 law (theory mode, addressed), 3 V
  uint32_t n_sections;
  uint64_t file_bytes;
  uint8_t  table_sha256[32];      // SHA-256 of the section table bytes
  uint8_t  reserved[64];
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
Hash of a file "by content" = SHA-256 of the section table (it contains every section hash). SHA-256 is bundled
(`src/common/sha256.cpp`). A `meta` json section in every file holds scalars, its inputs' content hashes and the mode.
Sections (names fixed; WPs may add sections, never rename):
- `raw.bin` (gen): `X_cm` f64 n×p, `y` f64 n, `meta`. `truth.json`: design, params, seed, S₀ (1-based), β*, σ*.
- `data.bin` (prep): `Xs_cm`, `ys`, `z`, `diagG`, `col_max`, `col_mean`, `col_sd`, `kept` i32 (1-based), `dropped`
  i32, `meta` {n, p_raw, p, K, yty, logCn, logm0, logWK, y_max, y_mean, y_sd_scaled, prep_class: "B"|"A"}, `logw`, `logprior`.
- `setup.bin` (WP2): `nb_ptr` i64, `nb_idx` i32, `dup_ptr/dup_idx`, `cut_ptr/cut_idx`, `blk_ptr/blk_members`, `blk`,
  `pos`, `code_ptr`, `logr`, `logprof_ptr/logprof`, `logF`, `size_logmass`, `size_cum`, `cond_ptr/cond_cum`,
  `cbs_ptr/codes_by_size`, `sub_ptr/sub_cum`, `mode_S`, table top stores `tstore_{top,lead0,lead1}_{v,off,len,hash,pool}`, `meta`.
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
  "binary": {"sha256": "...", "git_commit": "...", "compiler": "g++ 11.5.0", "flags": "...", "libm": {"path": "...", "sha256": "..."}},
  "inputs": {"data.bin": "<content sha256>", "setup.bin": "...", "calib.bin": "..."},
  "params": {"seed": 1, "island": 3, "Rp": 16, "N": 2500, "threads": 48, "...": "..."},
  "budget": {"task_seconds": 7200, "fit_core_h": 1000, "retries": 2},
  "machine": {"host": "...", "node_type": "...", "slurm_job_id": "..."},
  "outputs": {"island_3.bin": null} }
```
The job fills `outputs` with content hashes and `status` in `<out>.json` when it ends.

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
all scorer/engine code calls `v4::pm::log, exp, log1p, expm1, lgamma` (`include/v4/pmath.h`), never `std::` directly.
**Binding (v0.1.1): glibc 2.34 libm, FMA/AVX2 ifunc variants** (the v3.1 records' bits; a correctly rounded libm would
change them). `pm::fma_variant_expected()` must be true for any bit-form run; the manifest records libm path + SHA-256
and `libm_fma_variant`. Evidence: `engine_v4/tests/PMATH_REPORT.md`.

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
- **Threads: OpenMP** (`--threads k`, default `OMP_NUM_THREADS`). Rules: (1) no result depends on the thread count or
  schedule; (2) work is cut into **fixed chunks independent of the thread count** (default 64 items; label blocks and
  tiles are parameters, not part of the law); (3) floating-point reductions sum per-chunk partials, then combine chunk
  results serially in chunk order; no floating atomics, no `omp reduction` on floats; (4) per-thread `Ledger`s merged
  by `Ledger::merge` (order-free); (5) uniforms come only from addresses, never from thread state; (6) the stage barrier
  (weights, LSE, ESS, resampling) is serial in particle order (`core/cpp/v3_engine.h:316-327`).

## 8. Owned by WP1 and delivered with the skeleton
`types.h data.h model.h rng.h store.h ledger.h format.h records.h score.h(Bit) pmath.h status.h threads.h sha256`,
`gen`, `prep` (compat bits of `v3_preprocess.R:35-51` or R-standardised input), the compat Bit scorer, fixtures, the
libm decision. Stubs (declarations + `throw Error(internal_error, "not implemented")`) for every other WP's entry
point, so all WPs link from day one: `setup::run`, `island::run`, `calib::run`, `merge::run`, `eval::run`, `post::run`.

## Changelog
- v0.1 (2026-11-15, WP1) — first binding version.
- v0.1.1 (2026-11-15, WP1) — §5.1 `SectionEntry` gets `reserved[8]` (the entry is 128 B, as stated; the field list
  summed to 120). `fmt::Writer::add` keeps a pointer to the caller's buffer (no copy) until `write()`. §6 libm binding
  decided (glibc FMA variant + run-time check). §1: no separate `v3ref` target (`v4_tests` includes the core/ headers).
  §5.3: manifest `inputs` keys are file paths; the CLI verifies each `.bin` content hash before running.
