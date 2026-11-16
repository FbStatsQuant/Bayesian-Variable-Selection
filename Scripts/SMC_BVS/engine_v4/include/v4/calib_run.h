// calib_run.h -- WP4: one calibration end to end, over any IslandRunner (spec §1 row 3; INTERFACES §5.1 calib.bin).
//   budgets(n, p)         core/v3_preprocess.R:19-33 (K, B, ell, L, N0, H0, T0, tiers e = 0, 1)
//   calibrate_with(...)   Driver (calib.h) + LedgerBackend (calib_backend.h) on the calibration ledger, then the
//                         inherited export (core/cpp/v3_core.cpp:728-740): the models of top u lead0 u lead1 in
//                         lexicographic order, each with F, lg0, log m from the scorer.
// The command (`smcbvs4 calibrate`, src/calib/calib_run.cpp) wires data.bin / setup.bin / calib.bin around it; the
// island runner comes from WP3 (calibration roles) and is the only part not yet available.
#pragma once
#include <set>
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
inline Settings settings_from(const Budgets& b, Rule rule) {
  Settings s; s.rule = rule;
  for (int e = 0; e < 2; ++e) { s.tiers[e].tier = e; s.tiers[e].H = b.H[e]; s.tiers[e].Te = b.T[e]; s.tiers[e].L = b.L; s.tiers[e].Hm = 4; s.tiers[e].ell = b.ell; }
  if (rule == Rule::bounded) { s.sum_mode = SumMode::Blocked; s.I_max = std::min(s.I_max, b.ell); }
  return s;
}

struct CalibOutcome {
  CalibOut co;
  Ledger led;                                   // the calibration ledger at the end (stores, HPM + provenance, counters)
  std::vector<StageRecord> stages;
  std::vector<merge::InheritedModel> inherited; // models of top u lead0 u lead1 (lexicographic), scored
};

// led: the calibration ledger with the tables already offered (leaders on, cfg.islands = 4). The evaluator factory
// scores V, the local searches and the inherited export.
template <class Factory>
CalibOutcome calibrate_with(IslandRunner& runner, Ledger&& led, Factory& fac, const Settings& s, const merge::TailSettings& ts) {
  CalibOutcome out;
  out.led = std::move(led);
  LedgerBackend<Factory> be(runner, out.led, fac, ts, s.threads);
  Driver drv(be, s);
  out.co = drv.run();
  out.stages = be.stages();
  out.led.compact();
  // inherited export (core/cpp/v3_core.cpp:728-736): every model of the three stores, lexicographic, scored
  std::set<Model> U;
  for (const Store* st : {&out.led.top, &out.led.lead0, &out.led.lead1})
    for (size_t i = 0; i < st->size(); ++i) { ModelView v = st->model(i); U.insert(Model(v.begin(), v.end())); }
  std::vector<Model> Um(U.begin(), U.end());
  out.inherited.resize(Um.size());
  for_chunks(Um.size(), 256, s.threads, [&](size_t, size_t b, size_t e) {
    auto ev = fac.make(); double d;
    for (size_t i = b; i < e; ++i) { auto& m = out.inherited[i]; m.S = Um[i]; ev(m.S, m.logm, m.lg0, d, m.F); }
  });
  return out;
}

}  // namespace v4::calib
