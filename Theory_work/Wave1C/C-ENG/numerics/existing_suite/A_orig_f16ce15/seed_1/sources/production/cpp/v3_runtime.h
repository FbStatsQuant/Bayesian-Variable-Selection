// Lead rulings 2026-10-22, RULINGS_2 G1 and RULINGS_3 N6:
// operational guard, not a statistical setting. One clock covers the complete fit.
#pragma once
#include "v3_ledger.h"

namespace v3 {
struct GuardRecord {
  double elapsed, operation, allocation;
  std::string checkpoint;
  EventCtx event;
  bool exceeded;
};
struct RuntimeGuard {
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  double elapsed_before = 0, allocation = 24 * 3600;
  bool exceeded = false;
  std::vector<GuardRecord> records;
  double elapsed() const {
    return elapsed_before + std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
  }
  bool check(double operation, const std::string& checkpoint, const EventCtx& event) {
    double now = elapsed();
    bool stop = now + operation > allocation;
    records.push_back(GuardRecord{now, operation, allocation, checkpoint, event, stop});
    exceeded = exceeded || stop;
    return exceeded;
  }
};
inline RuntimeGuard* runtime_ptr(SEXP x) {
  return Rf_isNull(x) ? nullptr : Rcpp::XPtr<RuntimeGuard>(x).get();
}
inline EventCtx local_event(int tier, int iter) {
  EventCtx e; e.phase = PH_LOCAL; e.tier = tier; e.iter = iter; e.phi = 1;
  return e;
}
}  // namespace v3
