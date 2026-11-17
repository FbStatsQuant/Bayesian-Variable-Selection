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
#include <algorithm>
#include <initializer_list>
#include <string>
#include <vector>
#include "v4/calib.h"
#include "v4/ledger.h"
#include "v4/records.h"
#include "v4/tail.h"

namespace v4::calib {

// Role of a calibration island. Maps to WP3's IslandConfig::role (WP3_DESIGN §1.11): Pilot -> IslandRole::Pilot,
// Diag -> IslandRole::Diag (WP3 also has Final, which calibration never uses).
enum class IslandRole : uint8_t { Pilot = 1, Diag = 2 };

// One calibration island (INTERFACES §3 addresses: role, tier e, iter k, island r).
// The runner is a STATEFUL object created once per calibration: it holds the data, setup, seed, mode, N-independent
// settings and, in compat, the v3 streams 0 / 5 (pilot) and 1-4 / 6-9 (diagnostic islands), which continue across
// rebuilds (core v3_core.cpp:593-596, R6). The spec carries only what changes per island.
struct IslandSpec {
  IslandRole role = IslandRole::Pilot;
  int tier = 0, iter = 0, island = 0;       // pilot: iter 0, island 0; diag: iter k >= 1, island 1..4
  int H = 0;                                // particles
  bool adaptive = false; int Te = 0;        // pilot: core's adaptive rule (calib_rules.h pilot_next_phi), floor 1/Te
  std::vector<double> grid;                 // diag: the candidate grid (0 = phi_0 < ... < phi_T = 1)
  int L = 0, Hm = 4;
  // memory (INTERFACES §7 "whole task"; review PR37 N-1). One rule, each byte counted once:
  //   mem_budget     = the WHOLE calibration task's budget (--mem-budget, unchanged; 0 = no admission check), the same
  //                    meaning as IslandConfig::mem_budget;
  //   resident_bytes = the calibration state this process holds outside the island: the calibration ledger (three
  //                    stores at their staging peak) and the inherited export. It EXCLUDES X / z / diag(G) and the
  //                    setup inputs, which the island's own plan already counts;
  //   the island is admitted iff resident_bytes + island_plan.total <= mem_budget (island_plan as INTERFACES §7:
  //   data, setup inputs, store, leaders, snapshots, working set).
  uint64_t resident_bytes = 0, mem_budget = 0;
};
// What an island returns.
//  * completed: everything below.
//  * resource_limit with partial = true: the island started and stopped (core v3_core.cpp:637-640, 673-681): schedule,
//    forced, stages, logZ and the ledger so far.
//  * resource_limit with partial = false: refused at admission, nothing ran (INTERFACES §7); no ledger needed.
//  * numerical_failure: status, message and the ledger so far (WP3_DESIGN §1.11: the serial prefix of the events).
//  * invalid_input / internal_error / io_error: status and message; the calibration ends with that status.
// The ledger (also so far) must be the island's own: cfg.islands = 4, leaders on, caps 40p + 1 / 20p / 20p, no table,
// inherited or local-search events; the backend refuses anything else (internal_error).
struct IslandOut {
  Status status = Status::completed; std::string message; bool partial = false;
  double logZ = 0;
  std::vector<double> schedule;             // phi_1..phi_T used (pilot: adaptive; diag: grid[1..])
  int forced = 0;                           // pilot: forced (floor) steps
  std::vector<StageRow> stages;             // bridge stages
  std::vector<double> pip;
  Ledger led;                               // the island's own ledger (see above)
  uint64_t init_hash = 0;                   // hash of the initial draws (core IslandResult::init_hash)
  uint64_t position_start = 0, position_end = 0;   // compat: stream positions (xoshiro draws consumed); law: 0
};
struct IslandRunner {
  virtual ~IslandRunner() = default;
  virtual IslandOut run(const IslandSpec& spec) = 0;
};

// Stage record of one calibration island (calib.bin `stage_*` sections).
struct StageRecord {
  int tier = 0, iter = 0, island = 0; bool partial = false; double logZ = 0; std::vector<StageRow> stages;
  uint64_t init_hash = 0, position_start = 0, position_end = 0;
};

// V and the inherited export as flat views into the calibration stores (review PR37 m-6): sorted lexicographically and
// de-duplicated without per-model heap copies. The views stay valid while the stores are not modified.
inline std::vector<ModelView> sorted_unique_models(std::initializer_list<const Store*> stores, bool with_empty) {
  std::vector<ModelView> v;
  if (with_empty) v.push_back(ModelView());
  for (const Store* s : stores) for (size_t i = 0; i < s->size(); ++i) v.push_back(s->model(i));
  std::sort(v.begin(), v.end(), [](const ModelView& a, const ModelView& b) { return lex_less(a, b); });
  v.erase(std::unique(v.begin(), v.end(), [](const ModelView& a, const ModelView& b) { return same_model(a, b); }), v.end());
  return v;
}

template <class Factory>
class LedgerBackend : public Backend {
 public:
  // led: the calibration ledger (tables already offered; leaders on; cfg.islands = 4). fac: per-thread evaluator for
  // V and the local searches. ts: tail settings (p, K, zob, threads, chunk); tier / iter / calib are set per search.
  LedgerBackend(IslandRunner& runner, Ledger& led, Factory& fac, const merge::TailSettings& ts, int threads)
      : run_(runner), led_(led), fac_(fac), ts_(ts), threads_(threads) {}

  uint64_t resident_bytes = 0, mem_budget = 0;   // passed unchanged to every IslandSpec (IslandSpec's rule; calib_run.h's plan)
  bool test_force_local_limit_pilot = false;    // TEST ONLY (golden): the pilot's search reports local_limit (as core's R wrapper)

  PilotOut pilot(const TierSettings& cs) override {
    IslandSpec sp; sp.role = IslandRole::Pilot; sp.tier = cs.tier; sp.iter = 0; sp.island = 0; sp.H = cs.H;
    sp.adaptive = true; sp.Te = cs.Te; sp.L = cs.L; sp.Hm = cs.Hm; sp.resident_bytes = resident_bytes; sp.mem_budget = mem_budget;
    PilotOut o;
    IslandOut io = run_.run(sp);
    CalStatus st = take(io, cs.tier, 0, 0);
    if (st == CalStatus::numerical_failure) { o.status = st; o.message = io.message; return o; }
    if (st == CalStatus::resource_limit && !io.partial) { o.status = st; o.message = io.message.empty() ? "resource_limit (admission)" : io.message; return o; }
    o.schedule.push_back(0.0); o.schedule.insert(o.schedule.end(), io.schedule.begin(), io.schedule.end());
    o.forced = io.forced; o.has_forced = true;
    if (st == CalStatus::resource_limit) { o.status = st; o.message = "resource_limit"; return o; }
    o.best_before_F = led_.hpmF;
    if (!search(cs, 0, o.local_limit, o.status, o.message)) return o;
    if (test_force_local_limit_pilot) o.local_limit = true;
    o.best_after_F = led_.hpmF;
    return o;
  }

  DiagOut diag(const TierSettings& cs, const std::vector<double>& grid, int iter) override {
    DiagOut o;
    std::fill(led_.island_best.begin(), led_.island_best.end(), CAL_NEG_INF);   // core v3_core.cpp:662
    for (int r = 1; r <= 4; ++r) {
      IslandSpec sp; sp.role = IslandRole::Diag; sp.tier = cs.tier; sp.iter = iter; sp.island = r; sp.H = cs.H;
      sp.grid = grid; sp.L = cs.L; sp.Hm = cs.Hm; sp.resident_bytes = resident_bytes; sp.mem_budget = mem_budget;
      IslandOut io = run_.run(sp);
      CalStatus st = take(io, cs.tier, iter, r);
      if (st == CalStatus::numerical_failure) { o = DiagOut(); o.status = st; o.message = io.message; return o; }
      if (st == CalStatus::resource_limit && !io.partial) { o.status = st; o.message = io.message.empty() ? "resource_limit (admission)" : io.message; return o; }
      o.logZ_r.push_back(io.logZ);
      if (st == CalStatus::resource_limit) { o.status = st; o.message = "resource_limit"; return o; }
    }
    o.island_best.assign(led_.island_best.begin() + 1, led_.island_best.begin() + 5);
    o.best_before_F = led_.hpmF;
    if (!search(cs, iter, o.local_limit, o.status, o.message)) return o;
    o.best_after_F = led_.hpmF;
    return o;
  }

  VOut candidate_set() override {
    // core v3_core.cpp:705-716: {empty} u lead0 u lead1, lexicographic order of the sorted index vectors
    led_.compact();
    std::vector<ModelView> V = sorted_unique_models({&led_.lead0, &led_.lead1}, true);
    VOut out; out.lg0.assign(V.size(), 0); out.d.assign(V.size(), 0);
    try {
      for_chunks(V.size(), 256, threads_, [&](size_t, size_t b, size_t e) {
        auto ev = fac_.make(); double lm, lg0, d, F; Model S;
        for (size_t i = b; i < e; ++i) { S.assign(V[i].begin(), V[i].end()); ev(S, lm, lg0, d, F); out.lg0[i] = lg0; out.d[i] = d; }
      });
    } catch (const NumericalFailure& e) { VOut f; f.status = CalStatus::numerical_failure; f.message = e.what(); return f; }
    return out;
  }

  const std::vector<StageRecord>& stages() const { return stages_; }

 private:
  IslandRunner& run_;
  Ledger& led_;
  Factory& fac_;
  merge::TailSettings ts_;
  int threads_;
  std::vector<StageRecord> stages_;

  // Review PR37 M-3 (WP3_DESIGN §1.11): an island ledger must be the island's own, configured like the calibration
  // ledger: same p, 4 islands, leaders on, the same caps and orders, and no table, inherited or local-search events.
  void check_island_ledger(const Ledger& l, int r) const {
    auto fail = [&](const std::string& w) { throw Error(Status::internal_error, "calibration island " + std::to_string(r) + ": ledger " + w); };
    if (l.cfg.p != led_.cfg.p || l.cfg.islands != led_.cfg.islands || !l.cfg.leaders) fail("config differs (p, islands = 4, leaders on)");
    const Store* a[3] = {&l.top, &l.lead0, &l.lead1}; const Store* b[3] = {&led_.top, &led_.lead0, &led_.lead1};
    for (int q = 0; q < 3; ++q) if (a[q]->cap != b[q]->cap || a[q]->ord != b[q]->ord) fail("store caps / orders differ");
    for (int m = 0; m < N_MECH; ++m)
      if (l.logical[PH_TABLE][m] || l.logical[PH_INHERITED][m] || l.logical[PH_LOCAL][m] || l.logical[PH_LS0][m]) fail("has table / inherited / local-search events");
  }
  // Review PR37 M-2: the island's status, mapped; its ledger (so far) merged whenever it ran. Statuses the calibration
  // cannot continue from as a calibration outcome (invalid_input, internal_error, io_error) end the task with that status.
  CalStatus take(IslandOut& io, int tier, int iter, int r) {
    switch (io.status) {
      case Status::completed: break;
      case Status::resource_limit: break;
      case Status::numerical_failure: break;
      default: throw Error(io.status, "calibration island (tier " + std::to_string(tier) + ", iter " + std::to_string(iter) + ", island " +
                                       std::to_string(r) + "): " + io.message);
    }
    const bool ran = io.status != Status::resource_limit || io.partial;
    if (ran && io.led.cfg.p != 0) { check_island_ledger(io.led, r); led_.merge(io.led); }
    else if (ran && io.status != Status::numerical_failure) check_island_ledger(io.led, r);   // a ran island must bring its ledger
    if (ran && io.status != Status::numerical_failure)
      stages_.push_back({tier, iter, r, io.partial, io.logZ, io.stages, io.init_hash, io.position_start, io.position_end});
    if (io.status == Status::numerical_failure) return CalStatus::numerical_failure;
    if (io.status == Status::resource_limit) return CalStatus::resource_limit;
    return CalStatus::ok;
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
