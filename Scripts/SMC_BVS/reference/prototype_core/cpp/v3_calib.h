// v3_calib.h -- pure calibration rules: pilot next-temperature rule (M §6.6) and candidate-grid construction on a
// frozen candidate set V (M §6.7). CORE_SPEC v2 §10. No random numbers, no scoring.
#pragma once
#include "v3_util.h"

namespace v3 {

// Log-sum-exp used by the calibration rules, with its arithmetic fixed so that an independent implementation can
// reproduce every bisection decision bit for bit: m = max_i x_i; terms exp(x_i - m) in double; summed in index order
// in long double; the sum rounded to double; result m + log(sum) in double. (Identical to R's m + log(sum(exp(x - m))).)
inline double lse_cal(const std::vector<double>& x) {
  double m = NEG_INF; for (double v : x) if (v > m) m = v;
  if (!std::isfinite(m)) return m;
  long double s = 0.0L; for (double v : x) s += std::exp(v - m);
  return m + std::log((double)s);
}
// Population ESS of the weights exp(delta * d_i): (sum w)^2 / sum w^2 = exp(2 LSE(delta d) - LSE(2 delta d))
// (log-sum-exp form; replaces summing raw exponentials).
inline double population_ess(const std::vector<double>& d, double delta) {
  std::vector<double> x(d.size()), x2(d.size());
  for (size_t i = 0; i < d.size(); ++i) { x[i] = delta * d[i]; x2[i] = 2 * x[i]; }
  return std::exp(2 * lse_cal(x) - lse_cal(x2));
}

// Pilot next temperature (M §6.6): the largest phi' with population ESS of exp{(phi' - phi) d} >= 0.90 H, found as
// follows (documented): if phi' = 1 passes, phi' = 1 (so the pilot ends exactly at 1); otherwise 60 bisection halvings
// on (phi, 1] with lo = phi, hi = 1 (mid passes -> lo = mid, else hi = mid) and phi' = lo. Exploratory floor: if
// phi' - phi < 1/T_e then phi' = min(1, phi + 1/T_e) and the step is counted as forced.
struct NextPhi { double phi; bool forced; };
inline NextPhi pilot_next_phi(const std::vector<double>& d, double phi, double H, int Te) {
  const double thr = 0.90 * H;
  if (population_ess(d, 1.0 - phi) >= thr) return {1.0, false};
  double lo = phi, hi = 1.0;
  for (int i = 0; i < 60; ++i) {
    double mid = 0.5 * (lo + hi);
    if (population_ess(d, mid - phi) >= thr) lo = mid; else hi = mid;
  }
  if (lo - phi < 1.0 / Te) {
    // floor step; snapped to exactly 1 when within 1e-12 of 1, so accumulated rounding of phi + 1/T_e cannot create an
    // extra stage (lead ruling RC-2: a fully forced pilot has exactly T_e stages)
    double f = std::min(1.0, phi + 1.0 / Te);
    if (f >= 1.0 - 1e-12) f = 1.0;
    return {f, true};
  }
  return {lo, false};
}

// Restricted log-normaliser F_V(t) = log sum_{S in V} gamma_0(S) e^{t d(S)} (M §6.7), summed in the order of V.
inline double F_V(const std::vector<double>& lg0, const std::vector<double>& d, double t) {
  std::vector<double> x(lg0.size());
  for (size_t i = 0; i < lg0.size(); ++i) x[i] = lg0[i] + t * d[i];
  return lse_cal(x);
}
// Restricted ESS rho_V(u, v) = exp{2 F_V(v) - F_V(u) - F_V(2v - u)} (evaluating F_V beyond 1 is a finite sum).
inline double rho_V(const std::vector<double>& lg0, const std::vector<double>& d, double u, double v, long* evals = nullptr) {
  if (evals) *evals += 3;
  return std::exp(2 * F_V(lg0, d, v) - F_V(lg0, d, u) - F_V(lg0, d, 2 * v - u));
}

// Candidate-grid construction (M §6.7): start at u = 0 with the pilot temperatures as targets. Next target b = the
// smallest pilot temperature > u. If rho_V(u, b) >= 0.90 append b; otherwise bisect on (u, b] with u fixed, 60 halvings
// (lo = u, hi = b; mid passes -> lo = mid, else hi = mid) and append lo, the largest tested endpoint that passed (none
// passed -> non-progress). Each appended v is validated: v > u (strict numerical progress) and rho_V(u, v) >= 0.90.
// More than T_e intervals -> failure. Ends when u = 1.
struct GridResult {
  std::vector<double> grid, rho; bool ok = true; std::string reason = "ok"; long evals = 0;
};
inline GridResult build_grid(const std::vector<double>& lg0, const std::vector<double>& d, std::vector<double> targets, int Te) {
  GridResult g;
  std::sort(targets.begin(), targets.end());
  g.grid.push_back(0.0);
  double u = 0.0;
  while (u < 1.0) {
    double b = NEG_INF;
    for (double t : targets) if (t > u) { b = t; break; }
    if (b == NEG_INF) { g.ok = false; g.reason = "no_target_above_u"; return g; }
    double v;
    double rb = rho_V(lg0, d, u, b, &g.evals);
    if (rb >= 0.90) v = b;
    else {
      double lo = u, hi = b; bool any = false;
      for (int i = 0; i < 60; ++i) {
        double mid = 0.5 * (lo + hi);
        if (rho_V(lg0, d, u, mid, &g.evals) >= 0.90) { lo = mid; any = true; } else hi = mid;
      }
      if (!any) { g.ok = false; g.reason = "non_progress"; return g; }
      v = lo;
    }
    if (v >= 1.0 - 1e-12) v = 1.0;   // an appended point within 1e-12 of 1 is snapped to 1 (lead ruling RC-2)
    if (!(v > u)) { g.ok = false; g.reason = "non_progress"; return g; }
    double rv = rho_V(lg0, d, u, v, &g.evals);
    if (!(rv >= 0.90)) { g.ok = false; g.reason = "validation_failed"; return g; }
    g.grid.push_back(v); g.rho.push_back(rv);
    if ((int)g.grid.size() - 1 > Te) { g.ok = false; g.reason = "too_many_intervals"; return g; }
    u = v;
  }
  return g;
}

}  // namespace v3
