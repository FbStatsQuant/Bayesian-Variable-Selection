// score.cpp -- Scorer<Arith::Bit>: the arithmetic of core/cpp/v3_score.h, Gram-free. Every block below is copied from
// core/ with only these changes: scratch buffers are members (no per-call allocation; same values), the Gram entry is
// gram() (the same sequential sum the v3 Gram was filled with), std:: transcendental calls go through v4::pm.
#include "v4/score.h"
#include <cmath>
#include <limits>
#include <string>

namespace v4 {

// core/cpp/v3_score.h:76-90 (chol_inplace), copied.
bool chol_inplace(std::vector<double>& A, int k) {
  for (int j = 0; j < k; ++j) {
    double d = A[j * k + j];
    for (int t = 0; t < j; ++t) d -= A[j * k + t] * A[j * k + t];
    if (!(d > 0) || !std::isfinite(d)) return false;
    double L = pm::sqrt(d);
    A[j * k + j] = L;
    for (int i = j + 1; i < k; ++i) {
      double s = A[i * k + j];
      for (int t = 0; t < j; ++t) s -= A[i * k + t] * A[j * k + t];
      A[i * k + j] = s / L;
    }
  }
  return true;
}
// core/cpp/v3_score.h:92-98 (forward_solve, backward_solve), copied.
void forward_solve(const std::vector<double>& L, int k, const double* b, double* w) {
  for (int i = 0; i < k; ++i) { double s = b[i]; for (int t = 0; t < i; ++t) s -= L[i * k + t] * w[t]; w[i] = s / L[i * k + i]; }
}
void backward_solve(const std::vector<double>& L, int k, const double* w, double* x) {
  for (int i = k - 1; i >= 0; --i) { double s = w[i]; for (int t = i + 1; t < k; ++t) s -= L[t * k + i] * x[t]; x[i] = s / L[i * k + i]; }
}
// core/cpp/v3_score.h:103-137 (householder_lower), copied; the scratch vector v is passed in.
bool householder_lower(std::vector<double>& M, int m, int k, std::vector<double>& L, std::vector<double>& v) {
  v.assign((size_t)m, 0.0);
  for (int j = 0; j < k; ++j) {
    double nrm = 0; for (int i = j; i < m; ++i) nrm += M[(size_t)j * m + i] * M[(size_t)j * m + i];
    nrm = pm::sqrt(nrm);
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

// core/cpp/v3_score.h:147-160 (q_nonneg), copied.
double BitScorer::q_nonneg(ModelView S, const std::vector<double>& LH) {
  int k = (int)S.k, n = D->n;
  w_.resize(k); beta_.resize(k); tmp_.resize(k);
  for (int a = 0; a < k; ++a) tmp_[a] = n * D->z[S[a]];
  forward_solve(LH, k, tmp_.data(), w_.data());
  backward_solve(LH, k, w_.data(), beta_.data());
  double rss = 0, fit2 = 0, b2 = 0;
  for (int i = 0; i < n; ++i) {
    double f = 0; for (int a = 0; a < k; ++a) f += D->col(S[a])[i] * beta_[a];
    double r = D->ys[i] - f; rss += r * r; fit2 += f * f;
  }
  for (int a = 0; a < k; ++a) b2 += beta_[a] * beta_[a];
  return rss + (fit2 + b2) / n;
}

// core/cpp/v3_score.h:163-174 (gram_sub). Route chol: v3 reads the stored Gram, filled by the sequential sum over i of
// x_{i,min} x_{i,max} (v3_score.h:45-53) -> gram(). Route refactor: recomputed from X in the order (S[a], S[b]), copied.
void BitScorer::gram_sub(ModelView S, bool from_X) {
  int k = (int)S.k, n = D->n;
  Gs_.assign((size_t)k * k, 0.0);
  for (int a = 0; a < k; ++a)
    for (int b = 0; b <= a; ++b) {
      double g;
      if (!from_X) g = gram(*D, S[a], S[b]);
      else { const double* xa = D->col(S[a]); const double* xb = D->col(S[b]); g = 0; for (int i = 0; i < n; ++i) g += xa[i] * xb[i]; }
      Gs_[a * k + b] = g; Gs_[b * k + a] = g;
    }
}

// core/cpp/v3_score.h:176-188 (try_chol), copied.
bool BitScorer::try_chol(ModelView S, bool from_X, ScoreOut& o) {
  int k = (int)S.k; double n1 = D->n + 1.0;
  gram_sub(S, from_X);
  bufH_.assign((size_t)k * k, 0.0); bufA_.assign((size_t)k * k, 0.0);
  for (int a = 0; a < k; ++a) for (int b = 0; b < k; ++b) {
    bufH_[a * k + b] = n1 * Gs_[a * k + b] + (a == b ? 1.0 : 0.0);
    bufA_[a * k + b] = Gs_[a * k + b] + (a == b ? 1.0 : 0.0);
  }
  if (!chol_inplace(bufH_, k) || !chol_inplace(bufA_, k)) return false;
  LH_ = bufH_;
  finish_from_factors(S, bufH_, bufA_, o);
  return std::isfinite(o.logm);
}
// core/cpp/v3_score.h:190-202 (try_qr), copied.
bool BitScorer::try_qr(ModelView S, ScoreOut& o) {
  int k = (int)S.k, n = D->n, m = n + k;
  MH_.assign((size_t)m * k, 0.0); MA_.assign((size_t)m * k, 0.0);
  double s1 = pm::sqrt(n + 1.0);
  for (int a = 0; a < k; ++a) {
    const double* xa = D->col(S[a]);
    for (int i = 0; i < n; ++i) { MH_[(size_t)a * m + i] = s1 * xa[i]; MA_[(size_t)a * m + i] = xa[i]; }
    MH_[(size_t)a * m + n + a] = 1.0; MA_[(size_t)a * m + n + a] = 1.0;
  }
  if (!householder_lower(MH_, m, k, LH_, hv_) || !householder_lower(MA_, m, k, LA_, hv_)) return false;
  finish_from_factors(S, LH_, LA_, o);
  return std::isfinite(o.logm);
}
// core/cpp/v3_score.h:204-225 (finish_from_factors), copied.
void BitScorer::finish_from_factors(ModelView S, const std::vector<double>& LH, const std::vector<double>& LA, ScoreOut& o) {
  int k = (int)S.k;
  double ldH = 0, ldA = 0, mxH = 0, mnH = POS_INF, mxA = 0, mnA = POS_INF;
  for (int a = 0; a < k; ++a) {
    double h = LH[a * k + a], g = LA[a * k + a];
    ldH += pm::log(h); ldA += pm::log(g);
    mxH = std::max(mxH, h); mnH = std::min(mnH, h); mxA = std::max(mxA, g); mnA = std::min(mnA, g);
  }
  ldH *= 2; ldA *= 2;
  w_.resize(k); tmp_.resize(k);
  for (int a = 0; a < k; ++a) tmp_[a] = D->z[S[a]];
  forward_solve(LH, k, tmp_.data(), w_.data());
  double quad = 0; for (int a = 0; a < k; ++a) quad += w_[a] * w_[a];
  double Q = D->yty - D->n * quad;
  o.q_recomputed = false;
  if (Q < 1e-8 * D->yty) { Q = q_nonneg(S, LH); o.q_recomputed = true; }
  o.Q = Q; o.logdetH = ldH; o.logdetA = ldA;
  o.cond_H = (mxH / mnH) * (mxH / mnH); o.cond_A = (mxA / mnA) * (mxA / mnA);
  double arg = 2 * D->b0 + Q;
  o.logm = (arg > 0) ? D->logCn - 0.5 * (ldH - ldA) - D->nu * pm::log(arg) : NEG_INF;
}

// core/cpp/v3_score.h:227-239 (score), copied; counters are per scorer.
ScoreOut BitScorer::score(ModelView S) {
  ScoreOut o;
  int k = (int)S.k;
  if (k > D->K) throw Error(Status::internal_error, "score: |S| > K (infeasible model; callers never pass these, R1)");
  if (k == 0) { o.logm = D->logm0; o.Q = D->yty; o.route = ROUTE_CHOL; cnt.routes[ROUTE_CHOL]++; return o; }
  if (try_chol(S, false, o)) { o.route = ROUTE_CHOL; cnt.routes[ROUTE_CHOL]++; if (o.q_recomputed) cnt.q_recomputed++; return o; }
  if (try_chol(S, true, o)) { o.route = ROUTE_REFACTOR; cnt.routes[ROUTE_REFACTOR]++; if (o.q_recomputed) cnt.q_recomputed++; return o; }
  if (try_qr(S, o)) { o.route = ROUTE_QR; cnt.routes[ROUTE_QR]++; if (o.q_recomputed) cnt.q_recomputed++; return o; }
  cnt.numerical_failures++;
  throw NumericalFailure("score failed after Cholesky, refactor and augmented QR for a model of size " + std::to_string(k));
}

void BitScorer::flip_scores(ModelView S, const int32_t* labels, size_t nl, double* logm_out, int8_t* route_out) {
  for (size_t t = 0; t < nl; ++t) {
    int32_t j = labels[t];
    flip_.assign(S.begin(), S.end());
    auto it = std::lower_bound(flip_.begin(), flip_.end(), j);
    if (it != flip_.end() && *it == j) flip_.erase(it);
    else {
      if ((int)S.k >= D->K) { logm_out[t] = std::numeric_limits<double>::quiet_NaN(); if (route_out) route_out[t] = -1; continue; }
      flip_.insert(it, j);
    }
    ScoreOut o = score(flip_);
    logm_out[t] = o.logm;
    if (route_out) route_out[t] = o.route;
  }
}

// core/cpp/v3_score.h:242-246 (error_bound), copied.
double BitScorer::error_bound(const ScoreOut& o, int k) const {
  const double eps = std::numeric_limits<double>::epsilon();
  return 64 * eps * (D->nu * (D->yty / o.Q) * (1 + k * o.cond_H) + k * (o.cond_H + o.cond_A) + std::fabs(D->logCn) +
                     D->nu * std::fabs(pm::log(2 * D->b0 + o.Q)));
}

}  // namespace v4
