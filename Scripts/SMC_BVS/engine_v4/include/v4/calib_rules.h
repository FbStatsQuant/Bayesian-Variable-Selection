// calib_rules.h -- WP4: pure calibration rules (no random numbers, no scoring).
//  * pilot next-temperature rule and candidate-grid construction, copied from core/cpp/v3_calib.h (revision D);
//  * the restricted log-normaliser F_V with two declared summation forms:
//      SumMode::Serial  -- class B: the exact arithmetic of core/cpp/v3_calib.h:11-16 (terms exp(x_i - m) in double,
//                          summed in index order in long double). Terms may be computed by threads (they are
//                          independent); the sum itself is one serial pass. Used by theory mode (T, compat and law).
//      SumMode::Blocked -- class C (declared, spec §0-v2.2 #6 / D-2 "fixed blocked sum"): the same max m; each fixed
//                          block of `block` consecutive members sums its terms in long double; block partials are
//                          combined serially in block order in long double. Independent of the thread count. Used by V.
//  * grid refinement x m (spec §0-v2.2 #7, D-12) and the grid validity check (core/v3_run.R:77-82);
//  * the sample standard deviation with R's arithmetic (for trigger E2, core/v3_calib.R:102).
#pragma once
#include <cmath>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
#include <algorithm>
#include "wp4_par.h"

namespace v4 {
namespace calib {

const double CAL_NEG_INF = -std::numeric_limits<double>::infinity();

// core/cpp/v3_calib.h:11-16 (copied)
inline double lse_cal(const std::vector<double>& x) {
  double m = CAL_NEG_INF; for (double v : x) if (v > m) m = v;
  if (!std::isfinite(m)) return m;
  long double s = 0.0L; for (double v : x) s += std::exp(v - m);
  return m + std::log((double)s);
}
// core/cpp/v3_calib.h:19-23 (copied)
inline double population_ess(const std::vector<double>& d, double delta) {
  std::vector<double> x(d.size()), x2(d.size());
  for (size_t i = 0; i < d.size(); ++i) { x[i] = delta * d[i]; x2[i] = 2 * x[i]; }
  return std::exp(2 * lse_cal(x) - lse_cal(x2));
}
// core/cpp/v3_calib.h:29-46 (copied): pilot next temperature (used by the pilot island, WP3).
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
    double f = std::min(1.0, phi + 1.0 / Te);
    if (f >= 1.0 - 1e-12) f = 1.0;
    return {f, true};
  }
  return {lo, false};
}

enum class SumMode : uint8_t { Serial = 0, Blocked = 1 };
inline const char* sum_mode_name(SumMode m) { return m == SumMode::Serial ? "serial (class B)" : "blocked (class C)"; }

// F_V(t) = log sum_{S in V} gamma_0(S) e^{t d(S)}, summed in the order of V (core/cpp/v3_calib.h:49-53).
// Threaded evaluation with fixed chunks; see the header comment for the two summation forms.
class FV {
 public:
  const std::vector<double>* lg0; const std::vector<double>* d;
  SumMode mode = SumMode::Serial; int threads = 1;
  size_t chunk = 1 << 16;     // work chunk for threads (not part of the arithmetic)
  size_t block = 4096;        // Blocked mode: summation block (part of the declared class-C arithmetic)
  size_t serial_below = 1 << 15;   // below this size, run single-threaded (identical bits in either mode)
  long evals = 0;

  FV(const std::vector<double>& a, const std::vector<double>& b, SumMode m = SumMode::Serial, int th = 1)
      : lg0(&a), d(&b), mode(m), threads(th) {
    if (a.size() != b.size()) throw std::invalid_argument("FV: lg0 and d differ in length");
  }

  double operator()(double t) {
    const size_t n = lg0->size();
    const double* A = lg0->data(); const double* B = d->data();
    if (n == 0) return CAL_NEG_INF;
    const int th = n < serial_below ? 1 : threads;
    // max (exact, order-free)
    const size_t nc = n_chunks(n, chunk);
    std::vector<double> cmax(nc, CAL_NEG_INF);
    for_chunks(n, chunk, th, [&](size_t c, size_t b, size_t e) {
      double m = CAL_NEG_INF;
      for (size_t i = b; i < e; ++i) { double x = A[i] + t * B[i]; if (x > m) m = x; }
      cmax[c] = m;
    });
    double m = CAL_NEG_INF; for (double v : cmax) if (v > m) m = v;
    if (!std::isfinite(m)) return m;
    if (mode == SumMode::Serial) {
      if (th == 1) {   // core/cpp/v3_calib.h:14 arithmetic, without a buffer
        long double s = 0.0L;
        for (size_t i = 0; i < n; ++i) s += std::exp((A[i] + t * B[i]) - m);
        return m + std::log((double)s);
      }
      buf_.resize(n);
      for_chunks(n, chunk, th, [&](size_t, size_t b, size_t e) {
        for (size_t i = b; i < e; ++i) buf_[i] = std::exp((A[i] + t * B[i]) - m);
      });
      long double s = 0.0L;
      for (size_t i = 0; i < n; ++i) s += buf_[i];
      return m + std::log((double)s);
    }
    // Blocked (class C): block partials in long double, combined in block order.
    const size_t nb = n_chunks(n, block);
    part_.assign(nb, 0.0L);
    const size_t blocks_per_chunk = std::max<size_t>(1, chunk / block);
    for_chunks(nb, blocks_per_chunk, th, [&](size_t, size_t bb, size_t be) {
      for (size_t q = bb; q < be; ++q) {
        size_t b = q * block, e = std::min(n, b + block);
        long double s = 0.0L;
        for (size_t i = b; i < e; ++i) s += std::exp((A[i] + t * B[i]) - m);
        part_[q] = s;
      }
    });
    long double s = 0.0L;
    for (size_t q = 0; q < nb; ++q) s += part_[q];
    return m + std::log((double)s);
  }

  // restricted ESS rho_V(u, v) = exp{2 F_V(v) - F_V(u) - F_V(2v - u)} (core/cpp/v3_calib.h:55-58, same expression order)
  // F_V(u) is memoised for the last u (u is fixed during a bisection): F_V is a deterministic function, so the value
  // and every decision are unchanged (class B); `evals` keeps counting 3 per rho as core does (F_V_evaluations).
  double rho(double u, double v) {
    evals += 3;
    if (!(has_u_ && u == u_)) { Fu_ = (*this)(u); u_ = u; has_u_ = true; }
    return std::exp(2 * (*this)(v) - Fu_ - (*this)(2 * v - u));
  }

 private:
  bool has_u_ = false; double u_ = 0, Fu_ = 0;
  std::vector<double> buf_;
  std::vector<long double> part_;
};

// core/cpp/v3_calib.h:65-98 (copied; F_V evaluator injected). Candidate-grid construction on V.
struct GridResult {
  std::vector<double> grid, rho; bool ok = true; std::string reason = "ok"; long evals = 0;
};
inline GridResult build_grid(FV& fv, std::vector<double> targets, int Te) {
  GridResult g;
  long e0 = fv.evals;
  std::sort(targets.begin(), targets.end());
  g.grid.push_back(0.0);
  double u = 0.0;
  auto done = [&]() { g.evals = fv.evals - e0; return g; };
  while (u < 1.0) {
    double b = CAL_NEG_INF;
    for (double t : targets) if (t > u) { b = t; break; }
    if (b == CAL_NEG_INF) { g.ok = false; g.reason = "no_target_above_u"; return done(); }
    double v;
    double rb = fv.rho(u, b);
    if (rb >= 0.90) v = b;
    else {
      double lo = u, hi = b; bool any = false;
      for (int i = 0; i < 60; ++i) {
        double mid = 0.5 * (lo + hi);
        if (fv.rho(u, mid) >= 0.90) { lo = mid; any = true; } else hi = mid;
      }
      if (!any) { g.ok = false; g.reason = "non_progress"; return done(); }
      v = lo;
    }
    if (v >= 1.0 - 1e-12) v = 1.0;   // RC-2 snap (core/cpp/v3_calib.h:89)
    if (!(v > u)) { g.ok = false; g.reason = "non_progress"; return done(); }
    double rv = fv.rho(u, v);
    if (!(rv >= 0.90)) { g.ok = false; g.reason = "validation_failed"; return done(); }
    g.grid.push_back(v); g.rho.push_back(rv);
    if ((int)g.grid.size() - 1 > Te) { g.ok = false; g.reason = "too_many_intervals"; return done(); }
    u = v;
  }
  return done();
}
inline GridResult build_grid(const std::vector<double>& lg0, const std::vector<double>& d, std::vector<double> targets, int Te,
                             SumMode mode = SumMode::Serial, int threads = 1) {
  FV fv(lg0, d, mode, threads);
  return build_grid(fv, std::move(targets), Te);
}

// core/v3_run.R:77-82: finite, length >= 2, starts at exactly 0, ends at exactly 1, strictly increasing.
inline bool check_grid(const std::vector<double>& g) {
  if (g.size() < 2) return false;
  for (double x : g) if (!std::isfinite(x)) return false;
  if (g.front() != 0.0 || g.back() != 1.0) return false;
  for (size_t i = 1; i < g.size(); ++i) if (!(g[i] > g[i - 1])) return false;
  return true;
}

// Grid refinement x m (D-12): every interval (u, v) of the frozen grid is split into m equal parts,
// points u + (v - u) * (k / m), k = 1..m-1 (k/m in double). m = 1 returns the grid unchanged. Throws if the result is
// not a valid grid (an interval too small to split in double), which the caller reports as internal_error.
inline std::vector<double> refine_grid(const std::vector<double>& g, int m) {
  if (m < 1) throw std::invalid_argument("refine_grid: m must be >= 1");
  if (m == 1) return g;
  std::vector<double> out; out.reserve((g.size() - 1) * m + 1);
  out.push_back(g.front());
  for (size_t i = 1; i < g.size(); ++i) {
    double u = g[i - 1], v = g[i];
    for (int k = 1; k < m; ++k) out.push_back(u + (v - u) * ((double)k / (double)m));
    out.push_back(v);
  }
  if (!check_grid(out)) throw std::runtime_error("refine_grid: refined grid is not strictly increasing");
  return out;
}

// R's sd(x) (stats::var -> cov.c, complete observations): mean = sum/n in long double, refined by one correction
// pass (R_FINITE), then sum of squared deviations in long double / (n - 1), sqrt in double. NaN for n < 2.
inline double r_sd(const std::vector<double>& x) {
  size_t n = x.size();
  if (n < 2) return std::numeric_limits<double>::quiet_NaN();
  long double s = 0.0L; for (double v : x) s += v;
  long double xm = s / (long double)n;
  if (std::isfinite((double)xm)) { long double t = 0.0L; for (double v : x) t += (v - xm); xm = xm + t / (long double)n; }
  double xmd = (double)xm;
  long double ss = 0.0L; for (double v : x) ss += (v - xmd) * (v - xmd);   // product in double (cov.c), sum in long double
  return std::sqrt((double)(ss / (long double)(n - 1)));
}

}  // namespace calib
}  // namespace v4
