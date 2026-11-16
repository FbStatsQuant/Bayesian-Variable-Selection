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

namespace v4::island {

enum class KernelKind : int { LabelMajor = 0, ParticleMajor = 1 };

struct IslandConfig {
  uint32_t seed = 1; uint32_t island = 1;  // final island r = 1..R'
  int N = 2500; std::vector<double> grid; int L = 8; int Hm = 4;
  int B = 14;                               // number of N-swap labels (core: labels N1..NB)
  KernelKind kernel = KernelKind::LabelMajor;
  int G = 256; int tile = 128; int threads = 1;   // execution parameters: never part of the law
  uint64_t store_cap = 0;                   // 0: 40 p + 1 (OD-13)
  std::string ckpt_path;                    // empty: no checkpoints; else <path>.a / <path>.b
  double ckpt_every_s = 600;                // spec §6: at most every 10 min
  int stop_after_step = -1;                 // testing (T6): write a checkpoint after step s and return `interrupted`
  bool resume = true;
  bool keep_terminal = false;
};

using v4::StageRow;

struct KernelStats {   // execution statistics (not part of the law, not hashed)
  uint64_t particle_rounds = 0, particle_sweeps = 0, passes = 0, support_label_pairs = 0, supports = 0;
  uint64_t slow_supports = 0, store_merges = 0, store_buffered = 0;
  double t_init = 0, t_orders = 0, t_build = 0, t_phaseA = 0, t_walk = 0, t_phaseB = 0, t_apply = 0, t_barrier = 0,
         t_pm = 0, t_ckpt = 0, t_total = 0;
};

struct Particle { Model S; uint64_t h = 0; double logm = 0, lg0 = 0, d = 0, F = 0; };

struct IslandRun {
  int status = 0;   // 0 completed, 1 interrupted (stop_after_step), 2 numerical_failure
  std::string reason;
  int r = 0, N = 0, T = 0, L = 0, Hm = 0, p = 0;
  double logZ = NEG_INF; uint64_t init_hash = 0;
  std::vector<StageRow> stages;
  std::vector<MoveStats> terminal_moves; std::vector<int32_t> terminal_distinct;
  std::vector<double> rb_acc, pip; std::vector<std::vector<double>> rb_round;
  uint64_t logical[N_PHASE][N_MECH] = {}; double island_best = NEG_INF; HpmRec hpm;
  std::vector<double> top_v; std::vector<uint64_t> top_hash, top_off; std::vector<uint16_t> top_len; std::vector<int32_t> top_pool;
  std::vector<Model> terminal;
  int resumed_from_step = -1;
  KernelStats ks;
  uint64_t hash() const;   // FNV-1a over every law output (T3 / T6 comparisons)
};

// The INTERFACES §5.2 record (records.h): stage table, RB arrays, Ledger (HPM + provenance, island_best, logical
// counters, top store as a compacted v4::Store). Leader stores are absent in final islands (D-7).
v4::IslandResult to_record(const IslandRun& r);

template <Arith A>
IslandRun run_island(const Data& D, const Start& st, const Neighbours& nb, const IslandConfig& cfg);

extern template IslandRun run_island<Arith::Bit>(const Data&, const Start&, const Neighbours&, const IslandConfig&);
extern template IslandRun run_island<Arith::ClassA>(const Data&, const Start&, const Neighbours&, const IslandConfig&);

}  // namespace v4::island
