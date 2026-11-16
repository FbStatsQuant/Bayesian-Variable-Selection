// calib.h -- WP4: the calibration driver (spec §1 row 3, §0-v2.2 #6/#7, §6; DECISIONS D-2, D-12).
//
// Two rules over one driver:
//  * Rule::coded   (theory mode T) = core/v3_calib.R:28-193 (v3_cal_tier + v3_calibrate) exactly: pilot, preliminary
//    grid, up to ell rebuilds with bitwise grid convergence, the seven triggers (E1, E2, E3, forced_pilot_steps,
//    grid_failure, grid_unconverged, local_limit), at most one escalation (preflight before it), the C-DLV fallback.
//  * Rule::bounded (V-1M) = pilot + preliminary grid + at most I_max rebuilds (default 3); the only escalation is on a
//    grid-construction failure; otherwise the last grid is frozen with flag grid_unconverged; every trigger is still
//    recorded. Grid refinement x m (default 1) is applied to the frozen grid.
//
// The islands (pilot, diagnostic islands with their local searches) and the candidate set V are supplied by a Backend
// (WP3's island in compat or law mode; in the golden tests: the core/ engine itself). V is re-scored by the threaded
// helper rescore_V (class B: each member's score is independent). Grid construction uses calib_rules.h's FV in
// SumMode::Serial (T, class B) or SumMode::Blocked (V, class C, declared).
#pragma once
#include <array>
#include <chrono>
#include <memory>
#include <string>
#include <vector>
#include "v4/calib_rules.h"
#include "v4/model.h"
#include "v4/status.h"

namespace v4 {
namespace calib {

enum class Rule : uint8_t { coded = 0, bounded = 1 };

// Calibration status strings exactly as core/v3_calib.R ("ok", "resource_limit", "numerical_failure",
// "schedule_limit", "grid_failure_no_escalation"); task_status() maps them to INTERFACES §7 statuses.
enum class CalStatus : uint8_t { ok = 0, resource_limit, numerical_failure, schedule_limit, grid_failure_no_escalation };
inline const char* cal_status_name(CalStatus s) {
  static const char* nm[] = {"ok", "resource_limit", "numerical_failure", "schedule_limit", "grid_failure_no_escalation"};
  return nm[(int)s];
}
// schedule_limit / grid_failure_no_escalation (no valid grid after the coded rules) have no spec §6 status; they map to
// resource_limit (the schedule budget T_e is a resource) -- open issue for the manager.
inline Status task_status(CalStatus s) {
  switch (s) {
    case CalStatus::ok: return Status::completed;
    case CalStatus::numerical_failure: return Status::numerical_failure;
    default: return Status::resource_limit;
  }
}

struct TierSettings { int tier = 0, H = 0, Te = 0, L = 0, Hm = 4, ell = 0; };   // core/v3_calib.R:9-13

struct Settings {
  Rule rule = Rule::coded;
  int tier0 = 0;                        // starting tier (v3_calibrate(tier = 0))
  bool grid_fallback = true;            // C-DLV B (core/v3_calib.R:141-143)
  int I_max = 3;                        // bounded rule: maximum rebuilds
  int refine_m = 1;                     // grid refinement x m, applied to the frozen grid
  SumMode sum_mode = SumMode::Serial;   // T: Serial (class B); V: Blocked (class C)
  int threads = 1;
  std::array<TierSettings, 2> tiers;    // budgets of tier 0 and tier 1
};

// ---- what the backend returns ---------------------------------------------------------------------------------------
struct PilotOut {
  CalStatus status = CalStatus::ok; std::string message;
  std::vector<double> schedule;         // 0 followed by the pilot temperatures (core/cpp/v3_core.cpp:636)
  int forced = 0; bool has_forced = false;   // has_forced = false on numerical failure (core: field absent)
  double best_before_F = 0, best_after_F = 0;
  bool local_limit = false;
};
struct DiagOut {
  CalStatus status = CalStatus::ok; std::string message;
  std::vector<double> logZ_r, island_best;   // 4 diagnostic islands
  double best_before_F = 0, best_after_F = 0;
  bool local_limit = false;
};
struct VOut {
  CalStatus status = CalStatus::ok; std::string message;
  std::vector<double> lg0, d;           // in V order (lexicographic order of the sorted index vectors)
};
struct Backend {
  virtual ~Backend() = default;
  virtual PilotOut pilot(const TierSettings& ts) = 0;                                       // pilot + its local search
  virtual DiagOut diag(const TierSettings& ts, const std::vector<double>& grid, int iter) = 0;   // 4 islands + local search
  virtual VOut candidate_set() = 0;                                                         // V with lg0, d (rescore_V)
  // runtime guard after a grid construction (core/v3_calib.R:75-76); true = stop with resource_limit
  virtual bool grid_stop(double /*seconds*/, int /*tier*/, int /*index*/) { return false; }
  // preflight before the escalation (core/v3_calib.R:157); true = allocation exceeded, escalation blocked
  virtual bool preflight_exceeds(int /*tier*/) { return false; }
};

// ---- the archive --------------------------------------------------------------------------------------------------
struct Triggers {   // names and order as core/v3_calib.R:60-61
  bool E1 = false, E2 = false, E3 = false, forced_pilot_steps = false, grid_failure = false, grid_unconverged = false, local_limit = false;
  bool any() const { return E1 || E2 || E3 || forced_pilot_steps || grid_failure || grid_unconverged || local_limit; }
  std::vector<std::string> fired() const {
    std::vector<std::string> f;
    if (E1) f.push_back("E1"); if (E2) f.push_back("E2"); if (E3) f.push_back("E3");
    if (forced_pilot_steps) f.push_back("forced_pilot_steps"); if (grid_failure) f.push_back("grid_failure");
    if (grid_unconverged) f.push_back("grid_unconverged"); if (local_limit) f.push_back("local_limit");
    return f;
  }
};
struct GridRecord {
  std::string label; std::vector<double> grid, rho; bool ok = true; std::string reason; long evals = 0; double seconds = 0;
  size_t V_size = 0;
};
struct Iteration {
  int iter = 0; std::vector<double> grid, rho_V; std::string grid_label;
  std::vector<double> logZ_r, island_best; double overall_best = 0;
  bool E1 = false, E2 = false, E3 = false, complete = false;
};
struct TierOut {
  int tier = 0; TierSettings settings; CalStatus status = CalStatus::ok; std::string message;
  bool has_triggers = false; Triggers triggers;
  PilotOut pilot;
  std::vector<GridRecord> grids; std::vector<Iteration> iterations;
  bool converged = false; int rebuilds = 0;
  bool has_grid = false, has_rho = false; std::vector<double> grid, rho_V; std::string grid_label, grid_source = "candidate grid";
  bool has_fallback = false; std::vector<double> fallback_grid, fallback_rho; bool fallback_has_rho = false;
  std::string fallback_label, fallback_source;
  double seconds_grid = 0; long evals = 0;
};
struct Flags {
  bool escalated = false; std::string escalation_blocked;   // "" = NULL
  int checks_passed_calibration = -1;                        // -1 = NA
  int forced_pilot_steps = 0; bool grid_unconverged = false;
  std::vector<std::string> triggers_fired; std::string grid_fallback;   // "" = absent
};
struct Frozen {
  std::vector<double> grid;            // after refinement x m (what the final islands use)
  std::vector<double> grid_unrefined;  // the calibrated grid
  int tier = 0, refine_m = 1; std::vector<double> rho_V; bool has_rho = false; std::string grid_label, source = "calibration";
};
struct CalibOut {
  CalStatus status = CalStatus::ok; Rule rule = Rule::coded; int tier_final = 0; bool escalated = false;
  std::string escalation_blocked; std::vector<TierOut> tiers; Flags flags;
  bool has_frozen = false; Frozen frozen; int I_used = 0;   // rebuilds of the frozen tier
  std::string message;
};

// ---- V re-scoring (threaded, class B) -----------------------------------------------------------------------------
// Each member is scored independently by a per-chunk evaluator; outputs land at the member's index, so the result is
// independent of the thread count. Factory: `auto ev = fac.make(); ev(S, logm, lg0, d, F)` (throws NumericalFailure).
// On failure the message of the smallest failing index is reported (= core/cpp/v3_core.cpp:713-721, which stops at the
// first failure in V order) and no partial V is returned.
template <class Factory>
VOut rescore_V(const std::vector<Model>& V, Factory& fac, int threads, size_t chunk = 256) {
  VOut out; out.lg0.assign(V.size(), 0); out.d.assign(V.size(), 0);
  try {
    for_chunks(V.size(), chunk, threads, [&](size_t, size_t b, size_t e) {
      auto ev = fac.make();
      double lm, lg0, d, F;
      for (size_t i = b; i < e; ++i) { ev(V[i], lm, lg0, d, F); out.lg0[i] = lg0; out.d[i] = d; }
    });
  } catch (const NumericalFailure& e) {
    VOut f; f.status = CalStatus::numerical_failure; f.message = e.what(); return f;
  }
  return out;
}

// ---- the driver -----------------------------------------------------------------------------------------------------
class Driver {
 public:
  Driver(Backend& b, const Settings& s) : be_(b), s_(s) {}

  // core/v3_calib.R:28-137 (v3_cal_tier), with the rebuild cap ell (coded) or I_max (bounded).
  TierOut run_tier(int tier) {
    const TierSettings& cs = s_.tiers[tier];
    TierOut out; out.tier = tier; out.settings = cs;
    PilotOut pil = be_.pilot(cs);
    out.pilot = pil;
    if (pil.status != CalStatus::ok) { out.status = pil.status; out.message = pil.message; return out; }
    Triggers trig;
    trig.E3 = pil.best_after_F > pil.best_before_F;                 // core/v3_calib.R:25, 59
    trig.forced_pilot_steps = pil.forced > 0;
    trig.local_limit = pil.local_limit;
    out.has_triggers = true;
    auto fail = [&](CalStatus st, const std::string& msg) { out.status = st; out.message = msg; out.triggers = trig; return out; };
    // build(): V, grid, record, runtime check (core/v3_calib.R:64-78)
    struct Built { bool numfail = false, resource = false; std::string msg; GridResult g; std::string label; };
    auto build = [&](const std::string& label) {
      Built r; r.label = label;
      auto t0 = std::chrono::steady_clock::now();
      VOut V = be_.candidate_set();
      if (V.status == CalStatus::numerical_failure) { r.numfail = true; r.msg = V.message; return r; }
      auto tg = std::chrono::steady_clock::now();
      FV fv(V.lg0, V.d, s_.sum_mode, s_.threads);
      r.g = build_grid(fv, pil.schedule, cs.Te);
      double sec = std::chrono::duration<double>(std::chrono::steady_clock::now() - tg).count();
      GridRecord rec; rec.label = label; rec.grid = r.g.grid; rec.rho = r.g.rho; rec.ok = r.g.ok; rec.reason = r.g.reason;
      rec.evals = r.g.evals; rec.seconds = sec; rec.V_size = V.lg0.size();
      out.grids.push_back(rec);
      out.seconds_grid += sec; out.evals += r.g.evals;
      double sec_build = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
      r.resource = be_.grid_stop(sec_build, tier, (int)out.grids.size() - 1);
      return r;
    };
    Built g = build("preliminary");
    if (g.numfail) return fail(CalStatus::numerical_failure, g.msg);
    if (g.resource) return fail(CalStatus::resource_limit, "resource_limit");
    if (!g.g.ok) trig.grid_failure = true;
    bool converged = false;
    const int cap = s_.rule == Rule::coded ? cs.ell : s_.I_max;
    if (g.g.ok) {
      for (int it = 1; it <= cap; ++it) {
        DiagOut dg = be_.diag(cs, g.g.grid, it);
        Iteration rec; rec.iter = it; rec.grid = g.g.grid; rec.rho_V = g.g.rho; rec.grid_label = g.label;
        rec.logZ_r = dg.logZ_r; rec.island_best = dg.island_best;
        out.iterations.push_back(rec);
        if (dg.status != CalStatus::ok) return fail(dg.status, dg.message);
        bool E1 = false;
        for (double ib : dg.island_best) if (ib < dg.best_after_F - 1) E1 = true;    // core/v3_calib.R:101
        bool E2 = r_sd(dg.logZ_r) > 1;                                                // core/v3_calib.R:102
        bool E3it = dg.best_after_F > dg.best_before_F;
        Iteration& last = out.iterations.back();
        last.overall_best = dg.best_after_F; last.E1 = E1; last.E2 = E2; last.E3 = E3it; last.complete = true;
        trig.E1 = E1; trig.E2 = E2;
        trig.E3 = trig.E3 || E3it; trig.local_limit = trig.local_limit || dg.local_limit;
        Built gn = build("rebuild_" + std::to_string(it));
        if (gn.numfail) return fail(CalStatus::numerical_failure, gn.msg);
        if (gn.resource) return fail(CalStatus::resource_limit, "resource_limit");
        if (!gn.g.ok) { trig.grid_failure = true; break; }
        if (gn.g.grid == g.g.grid) { g = gn; converged = true; break; }   // bitwise identical temperatures
        g = gn;
      }
      if (!trig.grid_failure && !converged) trig.grid_unconverged = true;
    }
    // C-DLV B (core/v3_calib.R:120-125): fallback grid on a tier-1 construction failure
    if (s_.grid_fallback && trig.grid_failure && tier == 1) {
      out.has_fallback = true;
      if (g.g.ok) { out.fallback_grid = g.g.grid; out.fallback_rho = g.g.rho; out.fallback_has_rho = true; out.fallback_label = g.label; out.fallback_source = "last_successful_construction"; }
      else { out.fallback_grid = pil.schedule; out.fallback_has_rho = false; out.fallback_label = "pilot_schedule"; out.fallback_source = "pilot_schedule"; }
    }
    if (!trig.grid_failure) { out.has_grid = true; out.has_rho = true; out.grid = g.g.grid; out.rho_V = g.g.rho; out.grid_label = g.label; }
    out.converged = converged; out.rebuilds = (int)out.iterations.size();
    out.triggers = trig;
    return out;
  }

  // core/v3_calib.R:144-193 (v3_calibrate). Bounded rule: escalation only on grid_failure.
  CalibOut run() {
    CalibOut co; co.rule = s_.rule;
    CalStatus status = CalStatus::ok; int e = s_.tier0; std::string blocked;
    while (true) {
      TierOut a = run_tier(e);
      co.tiers.push_back(a);
      if (a.status != CalStatus::ok) { status = a.status; co.message = a.message; break; }
      bool fired = s_.rule == Rule::coded ? a.triggers.any() : a.triggers.grid_failure;
      if (!fired || e == 1) break;
      if (be_.preflight_exceeds(1)) { status = CalStatus::resource_limit; blocked = "resource_limit"; break; }
      e = 1;
    }
    TierOut& last = co.tiers.back();
    std::string fallback;
    if (status == CalStatus::ok && !last.has_grid && e == 1 && s_.grid_fallback && last.has_fallback && check_grid(last.fallback_grid)) {
      fallback = last.fallback_source;
      last.has_grid = true; last.has_rho = last.fallback_has_rho; last.grid = last.fallback_grid; last.rho_V = last.fallback_rho; last.grid_label = last.fallback_label;
      last.grid_source = "fallback: " + fallback;
    }
    if (status == CalStatus::ok && !last.has_grid) status = (e == 1) ? CalStatus::schedule_limit : CalStatus::grid_failure_no_escalation;
    co.status = status; co.tier_final = e; co.escalated = (e == 1 && s_.tier0 == 0); co.escalation_blocked = blocked;
    Flags& f = co.flags;
    f.escalated = co.escalated; f.escalation_blocked = blocked;
    f.checks_passed_calibration = (last.status == CalStatus::ok && last.has_triggers) ? (last.triggers.any() ? 0 : 1) : -1;
    for (auto& t : co.tiers) f.forced_pilot_steps += t.pilot.has_forced ? t.pilot.forced : 0;
    f.grid_unconverged = last.has_triggers && last.triggers.grid_unconverged;
    if (last.has_triggers) f.triggers_fired = last.triggers.fired();
    f.grid_fallback = fallback;
    if (status == CalStatus::ok) {
      co.has_frozen = true;
      co.frozen.grid_unrefined = last.grid;
      co.frozen.refine_m = s_.refine_m;
      co.frozen.grid = refine_grid(last.grid, s_.refine_m);   // throws (internal_error) only for an unsplittable interval
      co.frozen.tier = e; co.frozen.rho_V = last.rho_V; co.frozen.has_rho = last.has_rho;
      co.frozen.grid_label = last.grid_label;
      co.I_used = last.rebuilds;
    }
    return co;
  }

 private:
  Backend& be_;
  Settings s_;
};

}  // namespace calib
}  // namespace v4
