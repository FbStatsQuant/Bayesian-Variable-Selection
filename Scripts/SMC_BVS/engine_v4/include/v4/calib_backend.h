// calib_backend.h -- WP4: the calibration backend over an island runner (spec §1 row 3, §3 "calibration rebuild").
//
// The calibration Driver (calib.h) asks a Backend for the pilot, the diagnostic islands of rebuild k and the candidate
// set V. This backend implements those three on ONE calibration Ledger it owns, exactly as core's persistent CalState
// (core/cpp/v3_core.cpp:585-740):
//  * the ledger starts with the tables (from setup.bin; offered by the caller) and keeps leader stores (they feed V);
//  * every calibration island is run by an IslandRunner (WP3's island in production; core's engine in the golden
//    harness) on its OWN empty ledger, which is then merged into the calibration ledger with Ledger::merge (order-free:
//    stores = top-c of the union, HPM = smallest event key, island_best by max, counters by sum);
//  * after the pilot and after the 4 diagnostic islands of rebuild k, one local search from the calibration HPM runs
//    on the calibration ledger (tail.h, keys CALIB / tier e / iter k / UNIT_LOCAL; core v3_core.cpp:642, 689);
//  * island_best of the calibration ledger is reset before each rebuild's diagnostic islands (core v3_core.cpp:662);
//  * V = {empty} u models of lead0 u models of lead1, in lexicographic order (core v3_core.cpp:705-716), re-scored by
//    calib::rescore_V (threaded, class B).
// The runner contract (what an island must return) is the whole interface: swapping the runner changes no calib.bin
// bits as long as the runner returns the same IslandOut.
#pragma once
#include <set>
#include <string>
#include <vector>
#include "v4/calib.h"
#include "v4/ledger.h"
#include "v4/records.h"
#include "v4/tail.h"

namespace v4::calib {

enum class IslandRole : uint8_t { Pilot = 1, Diag = 2 };

// One calibration island (INTERFACES §3 addresses: role, tier e, iter k, island r).
struct IslandSpec {
  IslandRole role = IslandRole::Pilot;
  int tier = 0, iter = 0, island = 0;       // pilot: iter 0, island 0; diag: iter k >= 1, island 1..4
  int H = 0;                                // particles
  bool adaptive = false; int Te = 0;        // pilot: core's adaptive rule (calib_rules.h pilot_next_phi), floor 1/Te
  std::vector<double> grid;                 // diag: the candidate grid (0 = phi_0 < ... < phi_T = 1)
  int L = 0, Hm = 4;
};
// What an island returns. On resource_limit (partial = true): the schedule, forced count, stages and ledger so far; on
// numerical_failure: status, message and (if available) the ledger so far, which the backend merges (core's shared
// ledger keeps a stopped island's events; core v3_core.cpp:637-651, 673-681).
struct IslandOut {
  Status status = Status::completed; std::string message; bool partial = false;
  double logZ = 0;
  std::vector<double> schedule;             // phi_1..phi_T used (pilot: adaptive; diag: grid[1..])
  int forced = 0;                           // pilot: forced (floor) steps
  std::vector<StageRow> stages;             // bridge stages
  std::vector<double> pip;
  Ledger led;                               // the island's own ledger: CALIB keys, leaders on, cfg.islands = 4
  double position_start = 0, position_end = 0;   // compat stream positions (informational)
};
struct IslandRunner {
  virtual ~IslandRunner() = default;
  virtual IslandOut run(const IslandSpec& spec) = 0;
};

// Stage record of one calibration island (calib.bin `stage_*` sections).
struct StageRecord { int tier = 0, iter = 0, island = 0; bool partial = false; double logZ = 0; std::vector<StageRow> stages; };

template <class Factory>
class LedgerBackend : public Backend {
 public:
  // led: the calibration ledger (tables already offered; leaders on; cfg.islands = 4). fac: per-thread evaluator for
  // V and the local searches. ts: tail settings (p, K, zob, threads, chunk); tier / iter / calib are set per search.
  LedgerBackend(IslandRunner& runner, Ledger& led, Factory& fac, const merge::TailSettings& ts, int threads)
      : run_(runner), led_(led), fac_(fac), ts_(ts), threads_(threads) {}

  PilotOut pilot(const TierSettings& cs) override {
    IslandSpec sp; sp.role = IslandRole::Pilot; sp.tier = cs.tier; sp.iter = 0; sp.island = 0; sp.H = cs.H;
    sp.adaptive = true; sp.Te = cs.Te; sp.L = cs.L; sp.Hm = cs.Hm;
    PilotOut o;
    IslandOut io = run_.run(sp);
    merge_partial(io);
    if (io.status == Status::numerical_failure) { o.status = CalStatus::numerical_failure; o.message = io.message; return o; }
    if (io.status != Status::completed && !io.partial) { o.status = CalStatus::numerical_failure; o.message = "pilot: " + io.message; return o; }
    stages_.push_back({cs.tier, 0, 0, io.partial, io.logZ, io.stages});
    o.schedule.push_back(0.0); o.schedule.insert(o.schedule.end(), io.schedule.begin(), io.schedule.end());
    o.forced = io.forced; o.has_forced = true;
    if (!merged_) led_.merge(io.led);
    if (io.partial) { o.status = CalStatus::resource_limit; o.message = "resource_limit"; return o; }
    o.best_before_F = led_.hpmF;
    if (!search(cs, 0, o.local_limit, o.status, o.message)) return o;
    o.best_after_F = led_.hpmF;
    return o;
  }

  DiagOut diag(const TierSettings& cs, const std::vector<double>& grid, int iter) override {
    DiagOut o;
    std::fill(led_.island_best.begin(), led_.island_best.end(), CAL_NEG_INF);   // core v3_core.cpp:662
    for (int r = 1; r <= 4; ++r) {
      IslandSpec sp; sp.role = IslandRole::Diag; sp.tier = cs.tier; sp.iter = iter; sp.island = r; sp.H = cs.H;
      sp.grid = grid; sp.L = cs.L; sp.Hm = cs.Hm;
      IslandOut io = run_.run(sp);
      merge_partial(io);
      if (io.status == Status::numerical_failure) { o = DiagOut(); o.status = CalStatus::numerical_failure; o.message = io.message; return o; }
      if (io.status != Status::completed && !io.partial) { o = DiagOut(); o.status = CalStatus::numerical_failure; o.message = "diag: " + io.message; return o; }
      stages_.push_back({cs.tier, iter, r, io.partial, io.logZ, io.stages});
      if (!merged_) led_.merge(io.led);
      o.logZ_r.push_back(io.logZ);
      if (io.partial) { o.status = CalStatus::resource_limit; o.message = "resource_limit"; return o; }
    }
    o.island_best.assign(led_.island_best.begin() + 1, led_.island_best.begin() + 5);
    o.best_before_F = led_.hpmF;
    if (!search(cs, iter, o.local_limit, o.status, o.message)) return o;
    o.best_after_F = led_.hpmF;
    return o;
  }

  VOut candidate_set() override {
    // core v3_core.cpp:705-716: {empty} u lead0 u lead1, lexicographic order of the sorted index vectors
    std::set<Model> V; V.insert(Model());
    led_.compact();
    for (const Store* s : {&led_.lead0, &led_.lead1})
      for (size_t i = 0; i < s->size(); ++i) { ModelView v = s->model(i); V.insert(Model(v.begin(), v.end())); }
    std::vector<Model> Vm(V.begin(), V.end());
    return rescore_V(Vm, fac_, threads_);
  }

  const std::vector<StageRecord>& stages() const { return stages_; }

 private:
  IslandRunner& run_;
  Ledger& led_;
  Factory& fac_;
  merge::TailSettings ts_;
  int threads_;
  std::vector<StageRecord> stages_;
  bool merged_ = false;
  // A stopped island's ledger-so-far is merged too (core's shared ledger keeps those events): always on a numerical
  // failure, if the runner returns one (cfg.p set); a completed or resource-stopped island is merged by the caller.
  void merge_partial(const IslandOut& io) {
    merged_ = false;
    if (io.status == Status::numerical_failure && io.led.cfg.p == led_.cfg.p && io.led.cfg.islands == led_.cfg.islands) { led_.merge(io.led); merged_ = true; }
  }

  // one calibration local search from the current HPM (core v3_core.cpp:642 / 689: E.local_search(hpmS, ell, tier,
  // false, iter)); returns false and sets the status on a numerical failure
  bool search(const TierSettings& cs, int iter, bool& local_limit, CalStatus& st, std::string& msg) {
    merge::TailSettings t = ts_; t.tier = cs.tier; t.calib = true; t.iter = iter;
    try {
      LocalArchive A = merge::local_search(led_.hpmS, cs.ell, false, PH_LOCAL, led_, fac_, t);
      local_limit = A.local_limit;
    } catch (const NumericalFailure& e) { st = CalStatus::numerical_failure; msg = e.what(); return false; }
    return true;
  }
};

}  // namespace v4::calib
