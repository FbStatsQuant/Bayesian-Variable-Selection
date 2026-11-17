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
#include <atomic>
#include <chrono>
#include <limits>
#include <string>
#include "v4/island/kernel.h"
#include "v4/island/store.h"
#include "v4/island/memory.h"
#include "v4/island/start_view.h"
#include "v4/json.h"

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
  double stop_after_s = 0;                  // WP7 O4: a SOFT time stop. At the first step boundary after this many seconds of run()
                                            // (before the last step) a checkpoint is written (unless this step's was) and the
                                            // island returns status 1 with time_stopped = true: the resumable outcome of a task
                                            // that must end before its Slurm limit. 0 = off. Needs a checkpoint path
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
  double offer_floor = -__builtin_huge_val(); // D-29 (INTERFACES v0.1.15 §4.1, v0.1.17): the top store drops offers v < floor;
                                            // > -inf only for a V-mode (Arith::ClassA) final island, never compat / leaders /
                                            // calibration roles; finite or -inf (run_island refuses anything else).
                                            // Value: calib.bin meta.tau_cal_hex (offer_floor_for(), island/offer_floor.h)
  std::string offer_floor_calib;            // the content hash of the calib.bin the floor came from (required when floor > -inf)
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
  bool rolling_admission = true;            // label-major (K5, WP3_ARCH_REVIEW §2 lever 5): a slot whose particle finished its
                                            // round takes the next particle, so the passes stay full (false = groups of G one
                                            // after the other). Execution parameter: outputs unchanged
  int gram_slots = -1;                      // label-major with bounded scoring (K3, WP3_ARCH_REVIEW §2.2): Gram rows X^T x_a of
                                            // active columns kept across passes, one slot of p doubles each. -1 = auto
                                            // (gram_slots_of: 5 G / 2, 640 at G = 256); 0 = off. Execution parameter (same
                                            // bits); counted in the memory plan (gram_rows)
  std::atomic<bool>* test_order_phase = nullptr;   // tests only: set true around the label-major order phase's parallel region
                                            // (an operator-new counting test asserts that the region does not allocate)
  int test_fail_indep = -1, test_fail_indep_stage = 1;   // tests only: the I proposal of particle i (0-based) in bridge stage
                                            // s fails its score (K2: label-major draws it ahead and must fail where core does)
  int test_bound_shrink = 0;                // tests only: bounded scoring skips the last s positions below the running first
                                            // change (a deliberate bug: the negative control of test_nan_rows)
  int products_block = 0;                   // tile products: 4 = 4 active columns x 32 labels per sweep, 1 = the original loop
                                            // (same bits); 0 = auto: 4 when the island ISA has AVX-512, else 1 (review PR26
                                            // B2, MEASURED: block 4 is -27% on AVX-512 and +17% on x86-64-v2)
  bool verbose = false;                     // progress line per step on stderr (benchmarks)
  std::string cost_path;                    // D-30 (O2): a best-effort, NON-authoritative progress log of IslandRun::cost: a header
                                            // line, then one JSON line per closed row (one write() each). At the start of every job
                                            // segment it is rebuilt from the rows the run continues from (checkpoint), so it never
                                            // holds duplicate, missing or torn rows of a finished segment; a write failure disables
                                            // it (cost_log_error) and never fails the island. The record is meta.cost. Empty: none
  int test_cost_log_short = -1;             // tests only: the k-th sidecar line (0-based, after the rebuild) is written short
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
  uint64_t store_floor_dropped = 0;   // offers dropped by the D-29 offer floor (v < floor)
  double t_store_compact = 0, t_compact_pass = 0;   // wall seconds compacting (all paths) / at pass boundaries
  int kept_live_max = 0;   // most kept runs alive at once in this process (M2 bound; process-wide counter)
  double t_products = 0;   // thread-seconds inside phase A spent on the tile products
  double t_init = 0, t_orders = 0, t_build = 0, t_phaseA = 0, t_walk = 0, t_phaseB = 0, t_apply = 0, t_barrier = 0,
         t_pm = 0, t_ckpt = 0, t_total = 0;
  uint64_t act_cols = 0;     // label-major: sum over passes of the active columns (distinct members of fast supports that can add)
  double t_check = 0;      // wall seconds in the I1 store checks (O1; included in t_ckpt when the check precedes a checkpoint)
  uint64_t store_checks = 0;   // I1 checks run (top store; leader stores counted with it)
};

// D-30 (WP7 O2): the per-step execution record. Rows are CONTIGUOUS intervals of the island's lifetime wall clock: row k
// covers the time from the close of row k-1 (or the start of run(), in each job segment) to its own close, which is
// right after step k's ledger sync, before that step's checkpoint. So:
//   * step 0 = the initial draws (with the tiled copy of X), then the T bridge stages, the L burn-in and the Hm measured
//     rounds; the checkpoint written after step k (and its I1 check) is charged to row k+1;
//   * a closing row of kind 4 ("exit") covers what follows the last closed step: the last checkpoint, a failed or
//     interrupted partial step, the I1 check on exit and the result assembly;
//   * a row is final when it closes and is checkpointed as such; the checkpoint also carries the lifetime totals at that
//     close, so after a resume the totals are lifetime totals and the rows sum to them exactly (counts) and to
//     t_total (seconds; the dead job's work after its last row close is in neither).
// Execution statistics only, not the law: not in IslandRun::hash / meta.output_hash or any non-meta section hash
// (island_r.bin meta.cost; it is in the container's content hash like all of meta). Every field is 8 bytes (raw rows
// are checkpointed). A field the row's kernel does not measure is NaN in the JSON (cost_row_json), never 0.
struct StepCost {
  int64_t step = 0, kind = 0, segment = 0;   // kind 0 init, 1 bridge, 2 burn-in, 3 measured, 4 exit; segment = resumes before it
  int64_t kernel = 0;                        // 0 label-major, 1 particle-major (which fields are measured)
  double phi = 0;                            // the step's phi (exit row: NaN)
  double wall = 0;                           // the row's interval (lifetime wall clock)
  double t_orders = 0, t_build = 0, t_phaseA = 0, t_products = 0 /* thread-seconds */, t_walk = 0, t_phaseB = 0, t_apply = 0,
         t_barrier = 0, t_pm = 0;
  double t_compact = 0, t_compact_pass = 0;  // store compaction, all paths / of which at pass boundaries
  double t_check = 0, t_ckpt = 0;            // I1 checks (O1) / checkpoint writes in the interval (t_ckpt includes its check)
  double mean_S = 0;                         // population mean |S| at the close
  double store_mean_k = 0;                   // mean |S| of the stored models at the close
  uint64_t particle_rounds = 0, sweeps = 0, passes = 0, supports = 0, pairs = 0, act_cols = 0, slow_supports = 0;
  uint64_t flips = 0;                        // KernelStats::flip_evals (K1): addition flips evaluated on fast supports
  uint64_t offers = 0, dup_dropped = 0, merges = 0, store_size = 0;   // top store: offers buffered / dropped by the snapshot filter
  uint64_t rss_kb = 0, hwm_kb = 0;           // VmRSS at the close / VmHWM (process peak so far)
};
static_assert(sizeof(StepCost) == 8 * 35, "StepCost: 8-byte fields only (raw checkpoint rows, no padding)");

// one row as a JSON object: the raw fields plus three ratios (M = sweeps / particle-rounds, flips per elementary step =
// flips / (particle-rounds x m), active columns per pass; m = p + B + 2). Counts are JSON numbers (bounded counts,
// exact below 2^53; INTERFACES §5.1 v0.1.16). Fields the kernel does not measure are NaN: the particle-major kernel
// counts particle-rounds and t_pm only; the label-major kernel everything except t_pm.
inline v4::Json cost_row_json(const StepCost& c, int m) {
  const double nan = std::numeric_limits<double>::quiet_NaN();
  const bool lm = c.kernel == 0;
  auto L = [&](double x) { return v4::Json(lm ? x : nan); };   // label-major only
  v4::Json j = v4::Json::object();
  j["step"] = c.step; j["kind"] = c.kind; j["segment"] = c.segment; j["kernel"] = lm ? "lm" : "pm"; j["phi"] = c.phi; j["wall"] = c.wall;
  j["t_orders"] = L(c.t_orders); j["t_build"] = L(c.t_build); j["t_phaseA"] = L(c.t_phaseA); j["t_products"] = L(c.t_products);
  j["t_walk"] = L(c.t_walk); j["t_phaseB"] = L(c.t_phaseB); j["t_apply"] = L(c.t_apply); j["t_barrier"] = c.t_barrier;
  j["t_pm"] = lm ? v4::Json(nan) : v4::Json(c.t_pm);
  j["t_compact"] = c.t_compact; j["t_compact_pass"] = L(c.t_compact_pass); j["t_check"] = c.t_check; j["t_ckpt"] = c.t_ckpt;
  j["mean_S"] = c.mean_S; j["store_mean_k"] = c.store_mean_k;
  j["particle_rounds"] = c.particle_rounds;
  j["sweeps"] = L((double)c.sweeps); j["passes"] = L((double)c.passes); j["supports"] = L((double)c.supports); j["pairs"] = L((double)c.pairs);
  j["flips"] = L((double)c.flips); j["act_cols"] = L((double)c.act_cols); j["slow_supports"] = L((double)c.slow_supports);
  j["offers"] = c.offers; j["dup_dropped"] = c.dup_dropped; j["merges"] = c.merges; j["store_size"] = c.store_size;
  j["rss_kb"] = c.rss_kb; j["hwm_kb"] = c.hwm_kb;
  const double steps = (double)c.particle_rounds * (double)m;
  j["M"] = L(c.particle_rounds ? (double)c.sweeps / (double)c.particle_rounds : 0.0);
  j["flips_per_step"] = L(steps > 0 ? (double)c.flips / steps : 0.0);
  j["act_cols_per_pass"] = L(c.passes ? (double)c.act_cols / (double)c.passes : 0.0);
  return j;
}

struct Particle { Model S; uint64_t h = 0; double logm = 0, lg0 = 0, d = 0, F = 0; };

struct IslandRun {
  int status = 0;   // 0 completed, 1 interrupted (stop_after_step / stop_after_s), 2 numerical_failure, 3 resource_limit (mem_budget)
  bool time_stopped = false;   // status 1 because of stop_after_s (a resumable stop), not stop_after_step (tests)
  int stopped_after_step = -1; // the step whose checkpoint the interrupted island left
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
  double offer_floor = -__builtin_huge_val(); std::string offer_floor_calib;   // D-29: the floor the store ran under (island_r.bin meta)
  KernelStats ks;
  std::vector<StepCost> cost;   // D-30 per-step cost record (O2): the authoritative record; kept across checkpoints
  std::string cost_log_error;   // the sidecar progress log (cost_path) was disabled after this error (best effort; empty = ok)
  v4::Json cost_header;         // its configuration line: schema, r, role, N, p, m, threads, G, tile, kernel, arith, segment
  uint64_t hash() const;   // FNV-1a over every law output (T3 / T6 comparisons)
};

// The INTERFACES §5.2 record (records.h): stage table, RB arrays, Ledger (HPM + provenance, island_best, logical
// counters, top store as a compacted v4::Store). Leader stores are absent in final islands (D-7).
v4::IslandResult to_record(const IslandRun& r);

// The --mem-budget admission plan of an island (manager Q3/Q4, review PR24 P2): the group size it would use (largest
// G <= 256 that fits mem_budget when cfg.G == 0), the plan's k, the sizes. Used by run_island and by the bench.
MemPlan plan_island(const Data& D, const StartView& st, const IslandConfig& cfg, MemSizes* z = nullptr, double* k = nullptr, int* G = nullptr);
inline MemPlan plan_island(const Data& D, const dep::Start& st, const IslandConfig& cfg, MemSizes* z = nullptr, double* k = nullptr, int* G = nullptr) {
  return plan_island(D, StartView::from(st), cfg, z, k, G);   // tests: the stand-in Start, flattened
}

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

// The engine reads the start law through StartView (the flat tables: mapped setup.bin sections in production).
template <Arith A>
IslandRun run_island(const Data& D, const StartView& st, const Neighbours& nb, const IslandConfig& cfg);

extern template IslandRun run_island<Arith::Bit>(const Data&, const StartView&, const Neighbours&, const IslandConfig&);
extern template IslandRun run_island<Arith::ClassA>(const Data&, const StartView&, const Neighbours&, const IslandConfig&);

// Tests, goldens and benchmarks build the stand-in dep::Start (core's arithmetic): flattened into an owned view per call.
template <Arith A>
inline IslandRun run_island(const Data& D, const dep::Start& st, const Neighbours& nb, const IslandConfig& cfg) {
  const StartView v = StartView::from(st);
  return run_island<A>(D, v, nb, cfg);
}

}  // namespace v4::island
