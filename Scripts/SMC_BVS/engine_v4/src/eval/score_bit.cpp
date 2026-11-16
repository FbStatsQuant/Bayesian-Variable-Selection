// score_bit.cpp -- WP5's bit-form scorer + conjugate posterior parameters (compiled with the v3 flags:
// -O2 -fno-math-errno -ffp-contract=off). PROVISIONAL: when WP1's BitScorer (INTERFACES §6) lands, model_post() keeps
// only the parameter extraction and calls BitScorer::score for logm/route (the golden test then compares both).
#include <algorithm>
#include <cmath>
#include <limits>

#include "v4/eval.h"

namespace v4::eval {

static const double NEG_INF = -std::numeric_limits<double>::infinity();

static double lchoose_d(double n, double k) { return std::lgamma(n + 1.0) - std::lgamma(k + 1.0) - std::lgamma(n - k + 1.0); }

int32_t EvalData::internal_of(int32_t o) const {
  const int32_t* e = orig + p;
  const int32_t* it = std::lower_bound(orig, e, o);
  return (it != e && *it == o) ? (int32_t)(it - orig) : -1;
}

// Copied from core/cpp/v3_score.h:57-75 (constants of the target) and core/cpp/v3_util.h:75-83 (log_sum_exp, long double).
void data_constants(EvalData& D) {
  const int n = D.n, p = D.p;
  D.K = std::min(p, n / 2);
  D.nu = D.a0 + n / 2.0;
  D.logCn = D.a0 * std::log(2 * D.b0) + std::lgamma(D.a0 + n / 2.0) - (n / 2.0) * std::log(M_PI) - std::lgamma(D.a0);
  D.logm0 = D.logCn - D.nu * std::log(2 * D.b0 + D.yty);
  std::vector<double> logw(D.K + 1), terms(D.K + 1);
  for (int k = 0; k <= D.K; ++k) {
    logw[k] = -M_LN2 - lchoose_d(2.0 * p - 1.0, k);
    terms[k] = lchoose_d((double)p, k) + logw[k];
  }
  double m = NEG_INF;
  for (double v : terms) if (v > m) m = v;
  long double s = 0.0L;
  for (double v : terms) s += std::exp((long double)(v - m));
  D.logWK = m + (double)std::log(s);
  D.logprior.assign(D.K + 1, 0.0);
  for (int k = 0; k <= D.K; ++k) D.logprior[k] = logw[k] - D.logWK;
}

// Copied from core/cpp/v3_score.h:79-91 (chol_inplace), :93-100 (forward/backward solves).
static bool chol_inplace(std::vector<double>& A, int k) {
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
static void forward_solve(const std::vector<double>& L, int k, const double* b, double* w) {
  for (int i = 0; i < k; ++i) { double s = b[i]; for (int t = 0; t < i; ++t) s -= L[i * k + t] * w[t]; w[i] = s / L[i * k + i]; }
}
static void backward_solve(const std::vector<double>& L, int k, const double* w, double* x) {
  for (int i = k - 1; i >= 0; --i) { double s = w[i]; for (int t = i + 1; t < k; ++t) s -= L[t * k + i] * x[t]; x[i] = s / L[i * k + i]; }
}
// Copied from core/cpp/v3_score.h:105-136 (householder_lower).
static bool householder_lower(std::vector<double>& M, int m, int k, std::vector<double>& L) {
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

// Gram entry: INTERFACES §2, gram(a,b) = Σ_i x_{i,min} x_{i,max}, sequential in i (core/cpp/v3_score.h:45-53).
static double gram(const EvalData& D, int32_t a, int32_t b) {
  if (a > b) std::swap(a, b);
  const double* xa = D.col(a); const double* xb = D.col(b);
  double s = 0;
  for (int i = 0; i < D.n; ++i) s += xa[i] * xb[i];
  return s;
}
static double zval(const EvalData& D, int32_t a) {
  if (D.z) return D.z[a];
  const double* xa = D.col(a); double s = 0;   // core/cpp/v3_score.h:56
  for (int i = 0; i < D.n; ++i) s += xa[i] * D.ys[i];
  return s;
}

// Copied from core/cpp/v3_score.h:142-157 (q_nonneg): Q = ||y − X_S b||² + (||X_S b||² + ||b||²)/n, b = n H⁻¹ z_S.
static double q_nonneg(const EvalData& D, const Model& S, const std::vector<double>& LH) {
  int k = (int)S.size(), n = D.n;
  std::vector<double> w(k), beta(k), tmp(k);
  for (int a = 0; a < k; ++a) tmp[a] = n * zval(D, S[a]);
  forward_solve(LH, k, tmp.data(), w.data());
  backward_solve(LH, k, w.data(), beta.data());
  double rss = 0, fit2 = 0, b2 = 0;
  for (int i = 0; i < n; ++i) {
    double f = 0; for (int a = 0; a < k; ++a) f += D.col(S[a])[i] * beta[a];
    double r = D.ys[i] - f; rss += r * r; fit2 += f * f;
  }
  for (int a = 0; a < k; ++a) b2 += beta[a] * beta[a];
  return rss + (fit2 + b2) / n;
}

// Copied from core/cpp/v3_score.h:196-212 (finish_from_factors).
static void finish(const EvalData& D, const Model& S, const std::vector<double>& LH, const std::vector<double>& LA, ModelPost& o) {
  int k = (int)S.size();
  double ldH = 0, ldA = 0;
  for (int a = 0; a < k; ++a) { ldH += std::log(LH[a * k + a]); ldA += std::log(LA[a * k + a]); }
  ldH *= 2; ldA *= 2;
  std::vector<double> w(k), tmp(k);
  for (int a = 0; a < k; ++a) tmp[a] = zval(D, S[a]);
  forward_solve(LH, k, tmp.data(), w.data());
  double quad = 0; for (int a = 0; a < k; ++a) quad += w[a] * w[a];
  double Q = D.yty - D.n * quad;
  o.q_recomputed = false;
  if (Q < 1e-8 * D.yty) { Q = q_nonneg(D, S, LH); o.q_recomputed = true; }
  o.Q = Q; o.logdetH = ldH; o.logdetA = ldA;
  double arg = 2 * D.b0 + Q;
  o.logm = (arg > 0) ? D.logCn - 0.5 * (ldH - ldA) - D.nu * std::log(arg) : NEG_INF;
  // posterior mean θ̄ = n H⁻¹ z_S (WP5 addition; same solves as q_nonneg)
  std::vector<double> th(k);
  backward_solve(LH, k, w.data(), th.data());
  o.theta_bar.resize(k);
  for (int a = 0; a < k; ++a) o.theta_bar[a] = D.n * th[a];
}

ModelPost model_post(const EvalData& D, const Model& S) {
  ModelPost o; o.S = S;
  const int k = (int)S.size();
  for (int a = 1; a < k; ++a) if (!(S[a - 1] < S[a])) throw Error(Status::invalid_input, "model_post: model not sorted/unique");
  if (k > D.K) throw Error(Status::invalid_input, "model_post: |S| > K");
  o.alpha_n = D.a0 + D.n / 2.0;
  if (k == 0) {
    o.logm = D.logm0; o.Q = D.yty; o.route = 0;
  } else {
    // routes CHOL (= REFACTOR in v4: Data holds no Gram, both recompute the entries the same way) then QR (v3_score.h:214-224)
    const double n1 = D.n + 1.0;
    std::vector<double> Gs((size_t)k * k);
    for (int a = 0; a < k; ++a) for (int b = 0; b <= a; ++b) { double g = gram(D, S[a], S[b]); Gs[a * k + b] = g; Gs[b * k + a] = g; }
    std::vector<double> H((size_t)k * k), A((size_t)k * k);
    for (int a = 0; a < k; ++a) for (int b = 0; b < k; ++b) {
      H[a * k + b] = n1 * Gs[a * k + b] + (a == b ? 1.0 : 0.0);
      A[a * k + b] = Gs[a * k + b] + (a == b ? 1.0 : 0.0);
    }
    bool ok = chol_inplace(H, k) && chol_inplace(A, k);
    if (ok) { finish(D, S, H, A, o); ok = std::isfinite(o.logm); if (ok) { o.route = 0; o.LH = H; } }
    if (!ok) {
      const int n = D.n, m = n + k;
      std::vector<double> MH((size_t)m * k, 0.0), MA((size_t)m * k, 0.0), LH, LA;
      double s1 = std::sqrt(n + 1.0);
      for (int a = 0; a < k; ++a) {
        const double* xa = D.col(S[a]);
        for (int i = 0; i < n; ++i) { MH[(size_t)a * m + i] = s1 * xa[i]; MA[(size_t)a * m + i] = xa[i]; }
        MH[(size_t)a * m + n + a] = 1.0; MA[(size_t)a * m + n + a] = 1.0;
      }
      if (!householder_lower(MH, m, k, LH) || !householder_lower(MA, m, k, LA)) throw NumericalFailure("model_post: all routes failed");
      finish(D, S, LH, LA, o);
      if (!std::isfinite(o.logm)) throw NumericalFailure("model_post: non-finite logm on the QR route");
      o.route = 2; o.LH = LH;
    }
  }
  o.F = D.logprior[k] + o.logm;
  o.beta_n = D.b0 + o.Q / 2.0;
  return o;
}

}  // namespace v4::eval
