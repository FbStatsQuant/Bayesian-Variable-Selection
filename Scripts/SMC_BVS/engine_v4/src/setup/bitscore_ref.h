// bitscore_ref.h -- Gram-free copy of the v3 scorer (core/cpp/v3_score.h:74-224), used by the table builder for the
// rare entries that leave the plain Cholesky route (pivot failure, non-finite log m, Q recomputed) and as the
// one-entry reference of the prefix-reuse path. TEMPORARY: replaced by WP1's v4::BitScorer (INTERFACES §6) once it
// lands; the golden tests compare both against core/ directly. Gram entries: v4::gram (sequential in i, no FMA), which
// equals both the stored Gram of route chol and the recomputed Gram of route chol_refactor (core/cpp/v3_score.h:163-172).
#pragma once
#include <vector>
#include "wp1_shim.h"

namespace v4::setup::detail {

struct RefScore { double logm = 0, Q = 0; int route = 0; bool q_recomputed = false; };

// core/cpp/v3_score.h:74-90
inline bool chol_inplace(std::vector<double>& A, int k) {
  for (int j = 0; j < k; ++j) {
    double d = A[j * k + j];
    for (int t = 0; t < j; ++t) d -= A[j * k + t] * A[j * k + t];
    if (!(d > 0) || !std::isfinite(d)) return false;
    double L = std::sqrt(d);
    A[j * k + j] = L;
    for (int i = j + 1; i < k; ++i) {
      double s = A[i * k + j];
      for (int t = 0; t < j; ++t) s -= A[i * k + t] * A[j * k + t];
      A[i * k + j] = s / L;
    }
  }
  return true;
}
// core/cpp/v3_score.h:91-98
inline void forward_solve(const std::vector<double>& L, int k, const double* b, double* w) {
  for (int i = 0; i < k; ++i) { double s = b[i]; for (int t = 0; t < i; ++t) s -= L[i * k + t] * w[t]; w[i] = s / L[i * k + i]; }
}
inline void backward_solve(const std::vector<double>& L, int k, const double* w, double* x) {
  for (int i = k - 1; i >= 0; --i) { double s = w[i]; for (int t = i + 1; t < k; ++t) s -= L[t * k + i] * x[t]; x[i] = s / L[i * k + i]; }
}
// core/cpp/v3_score.h:100-135
inline bool householder_lower(std::vector<double>& M, int m, int k, std::vector<double>& L) {
  std::vector<double> v(m);
  for (int j = 0; j < k; ++j) {
    double nrm = 0; for (int i = j; i < m; ++i) nrm += M[(size_t)j * m + i] * M[(size_t)j * m + i];
    nrm = std::sqrt(nrm);
    if (!(nrm > 0) || !std::isfinite(nrm)) return false;
    double x0 = M[(size_t)j * m + j];
    double alpha = (x0 > 0) ? -nrm : nrm;
    for (int i = j; i < m; ++i) v[i] = M[(size_t)j * m + i];
    v[j] -= alpha;
    double vn = 0; for (int i = j; i < m; ++i) vn += v[i] * v[i];
    if (vn > 0) {
      for (int c = j; c < k; ++c) {
        double s = 0; for (int i = j; i < m; ++i) s += v[i] * M[(size_t)c * m + i];
        double f = 2 * s / vn;
        for (int i = j; i < m; ++i) M[(size_t)c * m + i] -= f * v[i];
      }
    }
  }
  L.assign((size_t)k * k, 0.0);
  for (int i = 0; i < k; ++i)
    for (int j = i; j < k; ++j) {
      double r = M[(size_t)j * m + i];
      if (i == j) r = std::fabs(r);
      L[j * k + i] = r;
    }
  for (int i = 0; i < k; ++i) {
    if (M[(size_t)i * m + i] < 0) for (int j = i + 1; j < k; ++j) L[j * k + i] = -L[j * k + i];
  }
  for (int i = 0; i < k; ++i) if (!(L[i * k + i] > 0) || !std::isfinite(L[i * k + i])) return false;
  return true;
}

class RefScorer {
 public:
  const Data* D;
  std::vector<double> bufH, bufA, w, beta, tmp;
  explicit RefScorer(const Data* d) : D(d) {}
  // core/cpp/v3_score.h:147-161
  double q_nonneg(const int32_t* S, int k, const std::vector<double>& LH) {
    int n = D->n;
    w.resize(k); beta.resize(k); tmp.resize(k);
    for (int a = 0; a < k; ++a) tmp[a] = n * D->z[S[a]];
    forward_solve(LH, k, tmp.data(), w.data());
    backward_solve(LH, k, w.data(), beta.data());
    double rss = 0, fit2 = 0, b2 = 0;
    for (int i = 0; i < n; ++i) {
      double f = 0; for (int a = 0; a < k; ++a) f += D->col(S[a])[i] * beta[a];
      double r = D->ys[i] - f; rss += r * r; fit2 += f * f;
    }
    for (int a = 0; a < k; ++a) b2 += beta[a] * beta[a];
    return rss + (fit2 + b2) / n;
  }
  // core/cpp/v3_score.h:163-188 (both Gram sources give v4::gram's bits; the refactor route is kept for the route label)
  bool try_chol(const int32_t* S, int k, RefScore& o, std::vector<double>& LH) {
    double n1 = D->n + 1.0;
    std::vector<double> Gs((size_t)k * k);
    for (int a = 0; a < k; ++a) for (int b = 0; b <= a; ++b) { double g = gram(*D, S[a], S[b]); Gs[a * k + b] = g; Gs[b * k + a] = g; }
    bufH.assign((size_t)k * k, 0.0); bufA.assign((size_t)k * k, 0.0);
    for (int a = 0; a < k; ++a) for (int b = 0; b < k; ++b) {
      bufH[a * k + b] = n1 * Gs[a * k + b] + (a == b ? 1.0 : 0.0);
      bufA[a * k + b] = Gs[a * k + b] + (a == b ? 1.0 : 0.0);
    }
    if (!chol_inplace(bufH, k) || !chol_inplace(bufA, k)) return false;
    LH = bufH;
    finish(S, k, bufH, bufA, o);
    return std::isfinite(o.logm);
  }
  // core/cpp/v3_score.h:189-202
  bool try_qr(const int32_t* S, int k, RefScore& o, std::vector<double>& LH) {
    int n = D->n, m = n + k;
    std::vector<double> MH((size_t)m * k, 0.0), MA((size_t)m * k, 0.0), LA;
    double s1 = std::sqrt(n + 1.0);
    for (int a = 0; a < k; ++a) {
      const double* xa = D->col(S[a]);
      for (int i = 0; i < n; ++i) { MH[(size_t)a * m + i] = s1 * xa[i]; MA[(size_t)a * m + i] = xa[i]; }
      MH[(size_t)a * m + n + a] = 1.0; MA[(size_t)a * m + n + a] = 1.0;
    }
    if (!householder_lower(MH, m, k, LH) || !householder_lower(MA, m, k, LA)) return false;
    finish(S, k, LH, LA, o);
    return std::isfinite(o.logm);
  }
  // core/cpp/v3_score.h:203-221 (condition estimates omitted: not used by setup)
  void finish(const int32_t* S, int k, const std::vector<double>& LH, const std::vector<double>& LA, RefScore& o) {
    double ldH = 0, ldA = 0;
    for (int a = 0; a < k; ++a) { ldH += pm::log(LH[a * k + a]); ldA += pm::log(LA[a * k + a]); }
    ldH *= 2; ldA *= 2;
    w.resize(k); tmp.resize(k);
    for (int a = 0; a < k; ++a) tmp[a] = D->z[S[a]];
    forward_solve(LH, k, tmp.data(), w.data());
    double quad = 0; for (int a = 0; a < k; ++a) quad += w[a] * w[a];
    double Q = D->yty - D->n * quad;
    o.q_recomputed = false;
    if (Q < 1e-8 * D->yty) { Q = q_nonneg(S, k, LH); o.q_recomputed = true; }
    o.Q = Q;
    double arg = 2 * D->b0 + Q;
    o.logm = (arg > 0) ? D->logCn - 0.5 * (ldH - ldA) - D->nu * pm::log(arg) : NEG_INF;
  }
  // core/cpp/v3_score.h:212-224
  RefScore score(const int32_t* S, int k) {
    RefScore o;
    if (k > D->K) throw Error(Status::internal_error, "score: |S| > K");
    if (k == 0) { o.logm = D->logm0; o.Q = D->yty; o.route = 0; return o; }
    std::vector<double> LH;
    if (try_chol(S, k, o, LH)) { o.route = 0; return o; }
    if (try_chol(S, k, o, LH)) { o.route = 1; return o; }
    if (try_qr(S, k, o, LH)) { o.route = 2; return o; }
    throw NumericalFailure("score failed after Cholesky, refactor and augmented QR for a model of size " + std::to_string(k));
  }
};

}  // namespace v4::setup::detail
