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

struct IslandConfig {
  uint32_t seed = 1; uint32_t island = 1;  // final island r = 1..R'
  int N = 2500; std::vector<double> grid; int L = 8; int Hm = 4;
  int B = 14;                               // number of N-swap labels (core: labels N1..NB)
  KernelKind kernel = KernelKind::LabelMajor;
  int G = 256; int tile = 128; int threads = 1;   // execution parameters: never part of the law (G = 0: largest G <= 256 that fits mem_budget)
  double k_store = 0;                       // admission: calibration-measured mean stored |S| (0: estimate from pi_0)
  double inputs_bytes = 0;                  // admission: setup / calib inputs mapped by the caller (X, z, diag(G) are in the plan)
  double test_admission_k = 0;              // tests only: force the admission's k (forces a step-boundary refusal)
  int test_oom_pass = -1;                   // tests only: throw std::bad_alloc inside phase A at this pass (resource_limit path)
  uint64_t mem_budget = 0;                  // bytes; 0 = no admission check (--mem-budget; manager Q3/Q4)
  uint64_t store_cap = 0;                   // 0: 40 p + 1 (OD-13)
  std::string ckpt_path;                    // empty: no checkpoints; else <path>.a / <path>.b
  double ckpt_every_s = 600;                // spec §6: at most every 10 min
  int stop_after_step = -1;                 // testing (T6): write a checkpoint after step s and return `interrupted`
  bool resume = true;
  bool keep_terminal = true;               // terminal supports (N, after the last measured round) -> island_r.bin
  uint32_t tier = 0;                        // frozen calibration tier (event key, INTERFACES v0.1.5 §4.2)
  bool allow_test_kernels = false;          // tests only: the bit-form label-major kernel (manager Q1)
  bool compat = false;                      // v3 serial streams (CompatSource 9 + r), core's double RB sum;
                                            // requires Arith::Bit, particle-major, 1 thread (manager Q2: the <= 5k bit anchor)
  bool leaders = false;                     // leader stores (lead0 log gamma_0, lead1 F): NEVER in a final run (INTERFACES
                                            // v0.1.7, D-7); calibration islands and golden tests only; never written to island_r.bin
  bool store_dup_filter = true;             // exact snapshot duplicate filter (execution parameter; content unchanged)
  bool store_parallel_compact = true;       // compaction at pass/step boundaries with all threads (content unchanged)
  bool check_store = true;                  // I1 after every step (linear; O(c) hash lookups)
  int products_block = 4;                   // tile products: 4 active columns x 32 labels per sweep (1: the original loop); same bits
  bool verbose = false;                     // progress line per step on stderr (benchmarks)
  // adaptive schedule (core's pilot rule: largest phi' with population ESS >= 0.9 H, floor 1/Te). Benchmarks and
  // pilot-like grids only; production islands use the frozen grid from calib.bin.
  bool adaptive = false; double adaptive_H = 0; int adaptive_Te = 30;
};

using v4::StageRow;

struct KernelStats {   // execution statistics (not part of the law, not hashed)
  uint64_t particle_rounds = 0, particle_sweeps = 0, passes = 0, support_label_pairs = 0, supports = 0;
  uint64_t slow_supports = 0, store_merges = 0, store_buffered = 0, store_dup_dropped = 0, store_serial_merges = 0;
  double t_store_compact = 0, t_compact_pass = 0;   // wall seconds compacting (all paths) / at pass boundaries
  int kept_live_max = 0;   // most kept runs alive at once in this process (M2 bound; process-wide counter)
  double t_products = 0;   // thread-seconds inside phase A spent on the tile products
  double t_init = 0, t_orders = 0, t_build = 0, t_phaseA = 0, t_walk = 0, t_phaseB = 0, t_apply = 0, t_barrier = 0,
         t_pm = 0, t_ckpt = 0, t_total = 0;
};

struct Particle { Model S; uint64_t h = 0; double logm = 0, lg0 = 0, d = 0, F = 0; };

struct IslandRun {
  int status = 0;   // 0 completed, 1 interrupted (stop_after_step), 2 numerical_failure, 3 resource_limit (mem_budget)
  std::string reason;
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

template <Arith A>
IslandRun run_island(const Data& D, const Start& st, const Neighbours& nb, const IslandConfig& cfg);

extern template IslandRun run_island<Arith::Bit>(const Data&, const Start&, const Neighbours&, const IslandConfig&);
extern template IslandRun run_island<Arith::ClassA>(const Data&, const Start&, const Neighbours&, const IslandConfig&);

}  // namespace v4::island
