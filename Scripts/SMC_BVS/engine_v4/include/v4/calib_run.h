// calib_run.h -- WP4: one calibration end to end, over any IslandRunner (spec §1 row 3; INTERFACES §5.1 calib.bin).
//   budgets(n, p)         core/v3_preprocess.R:19-33 (K, B, ell, L, N0, H0, T0, tiers e = 0, 1)
//   calibrate_with(...)   Driver (calib.h) + LedgerBackend (calib_backend.h) on the calibration ledger, then the
//                         inherited export (core/cpp/v3_core.cpp:728-740): the models of top u lead0 u lead1 in
//                         lexicographic order, each with F, lg0, log m from the scorer.
// The command (`smcbvs4 calibrate`, src/calib/calib_run.cpp) wires data.bin / setup.bin / calib.bin around it; the
// island runner comes from WP3 (calibration roles) and is the only part not yet available.
#pragma once
#include <algorithm>
#include <cmath>
#include <vector>
#include "v4/calib.h"
#include "v4/calib_backend.h"
#include "v4/merge.h"
#include "v4/tail.h"

namespace v4::calib {

struct Budgets { int64_t n = 0, p = 0; int K = 0, B = 0, ell = 0, L = 0; int N0 = 0, H0 = 0, T0 = 0; int N[2]{}, H[2]{}, T[2]{}; };
// core/v3_preprocess.R:14-33, copied (integer arithmetic): K = min(p, n %/% 2); B = min(isqrt n, isqrt p, 16);
// ell = ceil_log2(n + p + 1); L = max(4, ceil_log2(n + 1)); N0 = max(2500, n, p); H0 = ceiling(512 N0 / 2500);
// T0 = max(1000, ell^2); tier e: (N, H, T) = 4^e (N0, H0, T0).
inline Budgets budgets(int64_t n, int64_t p) {
  auto isqrt = [](int64_t x) { int64_t r = (int64_t)std::floor(std::sqrt((double)x)); while ((r + 1) * (r + 1) <= x) ++r; while (r * r > x) --r; return r; };
  auto clog2 = [](int64_t x) { int c = 0; while ((int64_t)1 << c < x) ++c; return c; };
  Budgets b; b.n = n; b.p = p;
  b.K = (int)std::min<int64_t>(p, n / 2);
  b.B = (int)std::min<int64_t>(std::min(isqrt(n), isqrt(p)), 16);
  b.ell = clog2(n + p + 1);
  b.L = std::max(4, clog2(n + 1));
  b.N0 = (int)std::max<int64_t>(std::max<int64_t>(2500, n), p);
  b.H0 = (int)((512LL * b.N0 + 2499) / 2500);
  b.T0 = std::max(1000, b.ell * b.ell);
  for (int e = 0; e < 2; ++e) { const int m = e ? 4 : 1; b.N[e] = m * b.N0; b.H[e] = m * b.H0; b.T[e] = m * b.T0; }
  return b;
}
// V-1M (D-1, D-26): no tier escalation; the calibration islands have H = 512 particles and the final islands N = 2,500,
// whatever p. Theory mode (coded rule) keeps v3's budgets (tiers e = 0, 1).
constexpr int V_H = 512, V_N = 2500;
inline Settings settings_from(const Budgets& b, Rule rule) {
  Settings s; s.rule = rule;
  for (int e = 0; e < 2; ++e) { s.tiers[e].tier = e; s.tiers[e].H = b.H[e]; s.tiers[e].Te = b.T[e]; s.tiers[e].L = b.L; s.tiers[e].Hm = 4; s.tiers[e].ell = b.ell; }
  if (rule == Rule::bounded) {
    s.sum_mode = SumMode::Blocked;
    s.tiers[0].H = V_H;               // D-26
    s.tiers[1] = TierSettings();      // no tier 1 in V
    s.tiers[1].tier = 1;
    // I_max is NOT clamped to ell here (review PR37 m-5): the Driver refuses I_max > ell (D-26)
  }
  return s;
}
// The final islands' N frozen with the grid: v3's N_e of the frozen tier (coded), or V_N (bounded).
inline int frozen_N(const Budgets& b, Rule rule, int tier) { return rule == Rule::bounded ? V_N : b.N[tier]; }

// Inherited models as flat arrays (review PR37 m-6): no per-model heap allocation at 8.10^7 models.
struct InheritedFlat {
  std::vector<int64_t> ptr{0}; std::vector<int32_t> idx; std::vector<double> F, lg0, logm, d;
  size_t size() const { return F.size(); }
  ModelView model(size_t i) const { return ModelView(idx.data() + ptr[i], (uint32_t)(ptr[i + 1] - ptr[i])); }
};

struct CalibOutcome {
  CalibOut co;
  Ledger led;                                   // the calibration ledger at the end (stores, HPM + provenance, counters)
  std::vector<StageRecord> stages;
  InheritedFlat inherited;                      // models of top u lead0 u lead1 (lexicographic), scored (F, lg0, log m, d); ok only
  double k_store = 0;                           // mean |S| of the calibration top store (INTERFACES v0.1.12 §7 admission)
};

// Memory plan of the calibration process (review PR37 M-5, N-1, N-2; ESTIMATE, bytes), on IslandSpec's rule:
//   resident      = the calibration ledger's three stores at their staging peak (2.5 x entries) + the flat V / export
//                   (pool + offsets + 4 values + a view each). Passed to every island as resident_bytes.
//   island_ledger = one island's own ledger (the same caps, 2.5 x): the least any island plan holds.
//   inputs        = data.bin + setup.bin bytes (mapped): counted once, here and in the island's plan, never in resident.
//   total         = resident + inputs + island_ledger: the smallest whole-task footprint with one island running. The
//                   command refuses (resource_limit) before building anything when total > --mem-budget.
// kbar = the plan's mean model size (calib_k_plan).
struct CalibMemPlan { uint64_t ledger = 0, island_ledger = 0, export_ = 0, inputs = 0, resident = 0, total = 0; };
inline CalibMemPlan calib_memory_plan(int64_t p, double kbar, uint64_t inputs_bytes) {
  const double entries = 40.0 * p + 1 + 2 * 20.0 * p, entry = 30.0 + 4.0 * kbar;   // v4::Store: 26 + 4k data + 4 index
  CalibMemPlan m;
  m.ledger = (uint64_t)(2.5 * entries * entry);
  m.island_ledger = (uint64_t)(2.5 * entries * entry);
  m.export_ = (uint64_t)(entries * (4.0 * kbar + 8 + 4 * 8 + 16));
  m.inputs = inputs_bytes;
  m.resident = m.ledger + m.export_;   // held while an island runs (the export only at the end; counted conservatively)
  m.total = m.resident + m.inputs + m.island_ledger;
  return m;
}
// The plan's k (INTERFACES §7; review PR37 N-2): max(8, q90(pi_0 size) + 1) from setup.bin's size_logmass -- the same
// arithmetic as WP3's plan_island (src/island/island_impl.h:1020-1024; calibration runs before any k_store exists).
// q90 = the smallest k with P(|S| <= k) >= 0.90 (0 if rounding never reaches 0.90, as WP3).
inline double calib_k_plan(const std::vector<double>& size_logmass) {
  double k_pi0 = 0, acc = 0;
  for (size_t k = 0; k < size_logmass.size(); ++k) { acc += std::exp(size_logmass[k]); if (acc >= 0.90) { k_pi0 = (double)k; break; } }
  return std::max(8.0, k_pi0 + 1.0);
}

// led: the calibration ledger with the tables already offered (leaders on, cfg.islands = 4). The evaluator factory
// scores V, the local searches and the inherited export. resident_bytes / mem_budget: passed unchanged to every island
// (IslandSpec's rule: mem_budget is the whole task's budget, resident_bytes = CalibMemPlan::resident).
template <class Factory>
CalibOutcome calibrate_with(IslandRunner& runner, Ledger&& led, Factory& fac, const Settings& s, const merge::TailSettings& ts,
                            uint64_t resident_bytes = 0, uint64_t mem_budget = 0, bool test_force_local_limit_pilot = false) {
  CalibOutcome out;
  out.led = std::move(led);
  LedgerBackend<Factory> be(runner, out.led, fac, ts, s.threads);
  be.resident_bytes = resident_bytes; be.mem_budget = mem_budget; be.test_force_local_limit_pilot = test_force_local_limit_pilot;
  Driver drv(be, s);
  out.co = drv.run();
  out.stages = be.stages();
  out.led.compact();
  // inherited export (core/cpp/v3_core.cpp:728-736): every model of the three stores, lexicographic, scored -- only for
  // a completed calibration: a non-ok calib.bin carries no inherited models (wp4_io.h), and scoring them after a stop
  // could replace the stop's status with a scorer failure (review PR37 N-3: a data-level numerical failure stops the
  // pilot while the stores hold table models that the scorer would now fail on). Core's export only lists the models.
  if (out.co.status == CalStatus::ok) {
    std::vector<ModelView> U = sorted_unique_models({&out.led.top, &out.led.lead0, &out.led.lead1}, false);
    InheritedFlat& f = out.inherited;
    for (auto& v : U) { f.idx.insert(f.idx.end(), v.begin(), v.end()); f.ptr.push_back((int64_t)f.idx.size()); }
    f.F.assign(U.size(), 0); f.lg0.assign(U.size(), 0); f.logm.assign(U.size(), 0); f.d.assign(U.size(), 0);
    for_chunks(U.size(), 256, s.threads, [&](size_t, size_t b, size_t e) {
      auto ev = fac.make(); Model S;
      for (size_t i = b; i < e; ++i) { ModelView v = f.model(i); S.assign(v.begin(), v.end()); ev(S, f.logm[i], f.lg0[i], f.d[i], f.F[i]); }
    });
  }
  const Store& t = out.led.top;
  out.k_store = t.size() ? (double)t.pool.size() / (double)t.size() : 0.0;
  return out;
}

}  // namespace v4::calib
