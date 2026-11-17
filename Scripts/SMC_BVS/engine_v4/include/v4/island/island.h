// island.h -- one production island (ENGINEERING_SPEC §0-v2.4, §3, §6; INTERFACES §3, §4, §5.2, §7).
//
// The algorithm is core/cpp/v3_engine.h:269-368 (run_island_s with a fixed grid): N iid pi_0 draws; T bridge stages
// (reweight by exp{(phi_t - phi_{t-1}) d}, log increment, ESS, multinomial resampling, one round at phi_t); L burn-in
// and Hm measured rounds at phi = 1 with Rao-Blackwell accumulation. Every uniform is read at its position address
// (INTERFACES §3 table), so the output does not depend on threads, group size G, tile size or kernel (T3).
//
// Two kernels, one output:
//  * LabelMajor (production): particles in groups of G; per pass, the distinct supports of the group's active particles
//    are scored for all p labels tile by tile (products X_A^T x_j sequential in i, then 8-lane flip scores and odds);
//    each particle finds its first state change from its own addressed uniforms (Gibbs labels from the pass, U/N/I
//    labels executed in position order); the labels it consumed before the change are then recorded (RB, events,
//    stores); particles that changed take a new pass (spec §3 rules 1-4). Scores of labels a particle did not consume
//    are discarded (rule 2).
//  * ParticleMajor (T3 reference): core's serial round, one label at a time, through the same 8-lane primitives.
//
// RB accumulation: o_j is added as a 63-bit fixed-point integer (floor(o * 2^63)) into unsigned 128-bit accumulators:
// the sum is exact, hence independent of the order of the particles (declared reduction; class A against core's
// double sum, |error| <= 2^-63 per term). See src/island/README.md.
#pragma once
#include <chrono>
#include <string>
#include "v4/island/kernel.h"
#include "v4/island/store.h"
#include "v4/island/memory.h"

namespace v4::island {

enum class KernelKind : int { LabelMajor = 0, ParticleMajor = 1 };
// Calibration roles (WP3_DESIGN §1.11, agreed with WP4): addresses role PILOT / DIAG with tier e, iter k, island r
// (pilot 0, diagnostic 1..4); every event labelled PH_PILOT / PH_DIAG with key (CALIB, e, k, r, ...), MEASURED round
// L + h (core/cpp/v3_engine.h:269-372 phase_override); leaders on; the ledger so far is returned on a stop.
enum class IslandRole : int { Final = 0, Pilot = 1, Diag = 2 };

// the identity string the CLI binds into the checkpoint (IslandConfig::input_id): the three content hashes
inline std::string input_identity(const std::string& data, const std::string& setup, const std::string& calib) { return data + "|" + setup + "|" + calib; }

struct IslandConfig {
  uint32_t seed = 1; uint32_t island = 1;  // final island r = 1..R'; calibration: pilot 0, diagnostic 1..4
  IslandRole role = IslandRole::Final;
  uint32_t iter = 0;                        // calibration rebuild iteration k (pilot 0); final islands: 0
  int N = 2500; std::vector<double> grid; int L = 8; int Hm = 4;
  int B = 14;                               // number of N-swap labels (core: labels N1..NB)
  KernelKind kernel = KernelKind::LabelMajor;
  int G = 256; int tile = 128; int threads = 1;   // execution parameters: never part of the law (G = 0: largest G <= 256 that fits mem_budget)
  double k_store = 0;                       // admission: calibration-measured mean stored |S| (calib.bin). A FINAL island
                                            // with a memory budget at p >= 1e5 requires it (review PR24 r1 / PR26 m2);
                                            // calibration islands run before calib.bin exists and plan with
                                            // max(8, q90(pi_0 size) + 1, k_store if given) from the setup alone
  bool k_store_optional = false;            // tests / benchmarks only: a final island at p >= 1e5 without k_store
  double inputs_bytes = 0;                  // admission: setup / calib inputs mapped by the caller (X, z, diag(G) are in the plan)
  double test_admission_k = 0;              // tests only: force the admission's k (forces a step-boundary refusal)
  int test_oom_pass = -1;                   // tests only: throw std::bad_alloc inside phase A at this pass (resource_limit path)
  int test_oom_merge = -1;                  // tests only: throw std::bad_alloc in the parallel compaction from this merge on
  int test_corrupt_store_step = -1;         // tests only: break I1 of the top store's kept run after this step (O1 wiring test)
  uint64_t mem_budget = 0;                  // bytes; 0 = no admission check (--mem-budget; manager Q3/Q4)
  uint64_t store_cap = 0;                   // 0: 40 p + 1 (OD-13)
  std::string input_id;                     // identity of the inputs the caller verified (the data / setup / calib content
                                            // hashes, as the CLI joins them): part of the checkpoint fingerprint, so a restart on
                                            // other inputs is refused (invalid_input) before any state is loaded (INTERFACES §5.1:
                                            // restart identifies its files by content_sha256; review PR52 MAJOR-1). Empty: tests
  std::string ckpt_path;                    // empty: no checkpoints; else <path>.a / <path>.b
  double ckpt_every_s = 600;                // spec §6: at most every 10 min
  int stop_after_step = -1;                 // testing (T6): write a checkpoint after step s and return `interrupted`
  bool resume = true;
  bool keep_terminal = true;               // terminal supports (N, after the last measured round) -> island_r.bin
  uint32_t tier = 0;                        // frozen calibration tier (event key, INTERFACES v0.1.5 §4.2)
  bool allow_test_kernels = false;          // tests only: the bit-form label-major kernel (manager Q1)
  bool compat = false;                      // v3 serial streams (CompatSource 9 + r), core's double RB sum;
                                            // requires Arith::Bit, particle-major, 1 thread (manager Q2: the <= 5k bit anchor)
  v4::CompatSource* compat_src = nullptr;   // compat: the caller's stream (required for calibration roles: streams 0 / 5
                                            // pilot, 1-4 / 6-9 diagnostic, continued across rebuilds by the caller); the
                                            // island draws from it and leaves it advanced. Null: a final island's own 9 + r
  bool leaders = false;                     // leader stores (lead0 log gamma_0, lead1 F): NEVER in a final run (INTERFACES
                                            // v0.1.7, D-7); calibration islands and golden tests only; never written to island_r.bin
  bool store_dup_filter = true;             // exact snapshot duplicate filter (execution parameter; content unchanged)
  bool store_parallel_compact = true;       // compaction at pass/step boundaries with all threads (content unchanged)
  bool check_store = true;                  // I1 on the top store (and the leader stores), in parallel over index ranges,
                                            // before every checkpoint and on every exit of the run, whatever its status
                                            // (before any island file can be written; review PR47 finding 1),
                                            // whenever the store changed since the last check (WP3_ARCH_REVIEW R4, O1).
                                            // The only run-time proof of I1: production never turns it off
  bool check_store_each_step = false;       // tests / debugging: also after every step (the pre-O1 behaviour; ~5.7 s per
                                            // step at 4e7 entries on SPR, MEASURED job 2749328)
  bool bounded_scoring = true;              // label-major (K1, WP3_ARCH_REVIEW §2.1): a (support, label) is scored only if a
                                            // particle on the support can still consume it; bounded uniform scan; one-particle
                                            // phase B. Execution parameter: outputs unchanged (false = the dense reference)
  bool test_nan_rows = false;               // tests only: poison the label-major score rows before every pass; any read of a
                                            // value not computed in the pass is an internal_error (review §2.1 NaN-row test)
  int gram_slots = -1;                      // label-major with bounded scoring (K3, WP3_ARCH_REVIEW §2.2): Gram rows X^T x_a of
                                            // active columns kept across passes, one slot of p doubles each. -1 = auto
                                            // (gram_slots_of: 5 G / 2, 640 at G = 256); 0 = off. Execution parameter (same
                                            // bits); counted in the memory plan (gram_rows)
  int test_bound_shrink = 0;                // tests only: bounded scoring skips the last s positions below the running first
                                            // change (a deliberate bug: the negative control of test_nan_rows)
  int products_block = 0;                   // tile products: 4 = 4 active columns x 32 labels per sweep, 1 = the original loop
                                            // (same bits); 0 = auto: 4 when the island ISA has AVX-512, else 1 (review PR26
                                            // B2, MEASURED: block 4 is -27% on AVX-512 and +17% on x86-64-v2)
  bool verbose = false;                     // progress line per step on stderr (benchmarks)
  // adaptive schedule (core's pilot rule: largest phi' with population ESS >= 0.9 H, floor 1/Te). Benchmarks and
  // pilot-like grids only; production islands use the frozen grid from calib.bin.
  bool adaptive = false; double adaptive_H = 0; int adaptive_Te = 30;
};

// Gram-row slots of a label-major island with G particles per group (K3): -1 = auto, 5 G / 2 (640 at G = 256; the
// measured late 10^6 rounds use ~151 active columns per pass at G = 256, production supports have E|S| ~ 3.6-3.9),
// at least 16; never more than p. Columns without a slot fall back to per-pass products (same bits).
inline int gram_slots_of(const IslandConfig& c, int G, int p) {
  if (c.kernel != KernelKind::LabelMajor || !c.bounded_scoring || c.gram_slots == 0) return 0;
  const int g = std::max(1, std::min(G, c.N));
  return std::min(p, c.gram_slots > 0 ? c.gram_slots : std::max(16, (5 * g + 1) / 2));
}

// the products block a configuration uses (0 = auto by the island ISA; review PR26 B2)
inline int products_block_of(const IslandConfig& c) {
  if (c.products_block > 0) return c.products_block;
#if defined(__AVX512F__)
  return 4;
#else
  return 1;
#endif
}

using v4::StageRow;

struct KernelStats {   // execution statistics (not part of the law, not hashed)
  uint64_t particle_rounds = 0, particle_sweeps = 0, passes = 0, support_label_pairs = 0, supports = 0;
  uint64_t gram_rows_new = 0, gram_rows_reused = 0, gram_rows_noslot = 0;   // K3: active columns per pass whose Gram row is
                                                                             // computed into a slot / read from a slot / without a slot
  uint64_t flip_evals = 0;   // label-major: addition flips evaluated on fast supports (bounded scoring: the needed ones only)
  uint64_t slow_supports = 0, store_merges = 0, store_buffered = 0, store_dup_dropped = 0, store_serial_merges = 0;
  double t_store_compact = 0, t_compact_pass = 0;   // wall seconds compacting (all paths) / at pass boundaries
  int kept_live_max = 0;   // most kept runs alive at once in this process (M2 bound; process-wide counter)
  double t_products = 0;   // thread-seconds inside phase A spent on the tile products
  double t_init = 0, t_orders = 0, t_build = 0, t_phaseA = 0, t_walk = 0, t_phaseB = 0, t_apply = 0, t_barrier = 0,
         t_pm = 0, t_ckpt = 0, t_total = 0;
  double t_check = 0;      // wall seconds in the I1 store checks (O1; included in t_ckpt when the check precedes a checkpoint)
  uint64_t store_checks = 0;   // I1 checks run (top store; leader stores counted with it)
};

struct Particle { Model S; uint64_t h = 0; double logm = 0, lg0 = 0, d = 0, F = 0; };

struct IslandRun {
  int status = 0;   // 0 completed, 1 interrupted (stop_after_step), 2 numerical_failure, 3 resource_limit (mem_budget)
  std::string reason;
  IslandRole role = IslandRole::Final; uint32_t tier = 0, iter = 0;
  int forced = 0;                    // adaptive schedule: forced (floor 1/T_e) steps (core's res.forced)
  bool partial = false;              // calibration role stopped by resource_limit: schedule, stages, logZ and ledger so far
  uint64_t stream_start = 0;         // compat: stream position (xoshiro draws) at the island's start
  int r = 0, N = 0, T = 0, L = 0, Hm = 0, p = 0;
  double logZ = NEG_INF; uint64_t init_hash = 0;
  std::vector<double> grid;   // the schedule used (= cfg.grid, or the adaptive one)
  std::vector<StageRow> stages;
  std::vector<MoveStats> terminal_moves; std::vector<int32_t> terminal_distinct;
  std::vector<double> rb_acc, pip; std::vector<std::vector<double>> rb_round;
  uint64_t logical[N_PHASE][N_MECH] = {}; double island_best = NEG_INF; HpmRec hpm;
  std::vector<double> top_v; std::vector<uint64_t> top_hash, top_off; std::vector<uint16_t> top_len; std::vector<int32_t> top_pool;
  std::vector<Model> terminal;
  int resumed_from_step = -1;
  int G_used = 0; std::string mem_plan;
  bool compat = false; uint64_t stream_count = 0;   // compat: xoshiro draws consumed
  bool leaders = false;                              // lead0_* / lead1_* filled (in memory only)
  std::vector<double> lead0_v, lead1_v; std::vector<uint64_t> lead0_hash, lead0_off, lead1_hash, lead1_off;
  std::vector<uint16_t> lead0_len, lead1_len; std::vector<int32_t> lead0_pool, lead1_pool;      // admission: the group size used and the peak-live plan (text)
  KernelStats ks;
  uint64_t hash() const;   // FNV-1a over every law output (T3 / T6 comparisons)
};

// The INTERFACES §5.2 record (records.h): stage table, RB arrays, Ledger (HPM + provenance, island_best, logical
// counters, top store as a compacted v4::Store). Leader stores are absent in final islands (D-7).
v4::IslandResult to_record(const IslandRun& r);

// The --mem-budget admission plan of an island (manager Q3/Q4, review PR24 P2): the group size it would use (largest
// G <= 256 that fits mem_budget when cfg.G == 0), the plan's k, the sizes. Used by run_island and by the bench.
MemPlan plan_island(const Data& D, const Start& st, const IslandConfig& cfg, MemSizes* z = nullptr, double* k = nullptr, int* G = nullptr);

// The same plan from sizes alone (no data, no Start: `--plan-only` before the files exist; k is then the caller's):
// plan_sizes() fills MemSizes exactly as plan_island does, plan_with_budget() applies its G rule (cfg.G = 0 and a
// budget: the largest G <= 256 that fits). Test `plan_from_sizes_equals_plan_island` pins the two paths equal.
inline MemSizes plan_sizes(int n, int p, int K, const IslandConfig& cfg) {
  const bool lm = cfg.kernel == KernelKind::LabelMajor;
  MemSizes z; z.n = n; z.p = p; z.K = K; z.N = cfg.N; z.B = cfg.B; z.Hm = cfg.Hm; z.threads = cfg.threads;
  z.tile = std::max(64, (cfg.tile + 63) / 64 * 64); z.cap = cfg.store_cap ? cfg.store_cap : 40ULL * (uint64_t)p + 1; z.label_major = lm;
  z.deferred = cfg.store_parallel_compact && cfg.threads > 1 && lm; z.leaders = cfg.leaders || cfg.role != IslandRole::Final;
  z.compat = cfg.compat; z.inputs_bytes = cfg.inputs_bytes; z.calib = cfg.role != IslandRole::Final;
  return z;
}
inline MemPlan plan_with_budget(MemSizes& z, double k, const IslandConfig& cfg) {
  int G = cfg.G ? cfg.G : 256;
  z.G = G; z.gram_slots = gram_slots_of(cfg, G, z.p); MemPlan mp = island_memory(z, k);
  if (cfg.mem_budget && cfg.G == 0) while (G > 1 && mp.total > cfg.mem_budget) { --G; z.G = G; z.gram_slots = gram_slots_of(cfg, G, z.p); mp = island_memory(z, k); }
  return mp;
}

template <Arith A>
IslandRun run_island(const Data& D, const Start& st, const Neighbours& nb, const IslandConfig& cfg);

extern template IslandRun run_island<Arith::Bit>(const Data&, const Start&, const Neighbours&, const IslandConfig&);
extern template IslandRun run_island<Arith::ClassA>(const Data&, const Start&, const Neighbours&, const IslandConfig&);

}  // namespace v4::island
