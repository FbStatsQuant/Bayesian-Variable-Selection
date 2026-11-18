// data.h -- the standardised data and the constants of the target (INTERFACES §2). No Gram is stored: every Gram
// entry is the sequential dot product of core/cpp/v3_score.h:45-53 (gram()).
#pragma once
#include <cstdint>
#include <limits>
#include <memory>
#include <vector>
#include "v4/model.h"
#include "v4/pmath.h"

namespace v4 {

constexpr double NEG_INF = -std::numeric_limits<double>::infinity();
constexpr double POS_INF = std::numeric_limits<double>::infinity();

struct Data {
  int32_t n = 0, p = 0, p_raw = 0, K = 0;
  const double* Xs = nullptr;     // n x p column-major, standardised
  const double* ys = nullptr;     // n
  const double* z = nullptr;      // p
  const double* diagG = nullptr;  // p
  const double *col_max = nullptr, *col_mean = nullptr, *col_sd = nullptr;  // p each (may be null for bare contexts)
  const int32_t* orig = nullptr;  // p, 1-based original column index
  double yty = 0, a0 = 0.01, b0 = 0.01, nu = 0, logCn = 0, logm0 = 0, logWK = 0;
  std::vector<double> logw, logprior;  // k = 0..K
  Zobrist zob;
  double y_max = 0, y_mean = 0, y_sd_scaled = 0;
  std::shared_ptr<const void> keep;    // owner of the arrays (heap vectors or a mapped file)
  inline const double* col(int32_t j) const { return Xs + (size_t)j * (size_t)n; }
};

// Heap owner used by prep and by tests.
struct DataOwned {
  std::vector<double> X, y, z, diagG, col_max, col_mean, col_sd;
  std::vector<int32_t> orig, dropped;
};

// Gram entry G_ab: core/cpp/v3_score.h:45-53 -- s = 0; for i: s += x_{i,min} * x_{i,max} (double, no FMA).
inline double gram(const Data& D, int32_t a, int32_t b) {
  const double* xa = D.col(a < b ? a : b);
  const double* xb = D.col(a < b ? b : a);
  double s = 0;
  for (int32_t i = 0; i < D.n; ++i) s += xa[i] * xb[i];
  return s;
}

// Build a Data view over an owner whose X, y are standardised; computes z, diag(G), y'y and every constant exactly as
// core/cpp/v3_score.h:39-72 (data_init without the Gram). orig defaults to 1..p.
Data make_data(std::shared_ptr<DataOwned> own, int32_t n, int32_t p);
// Constants only (z, diagG, yty must be set): K, nu, log C_n, log m0, log w(k), log W_K, log varpi(k), Zobrist keys.
void data_constants(Data& D);

// core/cpp/v3_util.h:74-80 and :94, copied (log-sum-exp with long double accumulation; lchoose via lgamma).
inline double log_sum_exp(const std::vector<double>& x) {
  double m = NEG_INF;
  for (double v : x) if (v > m) m = v;
  if (m == NEG_INF || !std::isfinite(m)) return m;
  long double s = 0.0L;
  for (double v : x) s += pm::expl((long double)(v - m));
  return m + (double)pm::logl(s);
}
inline double lchoose_d(double n, double k) { return pm::lgamma(n + 1.0) - pm::lgamma(k + 1.0) - pm::lgamma(n - k + 1.0); }

}  // namespace v4
