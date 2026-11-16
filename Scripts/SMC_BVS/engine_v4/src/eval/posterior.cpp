// posterior.cpp -- conjugate posterior of one model on top of WP1's BitScorer (INTERFACES §6), and Data from raw.
#include <algorithm>
#include <cmath>

#include "v4/eval.h"
#include "v4/prep.h"
#include "v4/score.h"

namespace v4::eval {

int32_t internal_of(const Data& D, int32_t o) {
  const int32_t* e = D.orig + D.p;
  const int32_t* it = std::lower_bound(D.orig, e, o);
  return (it != e && *it == o) ? (int32_t)(it - D.orig) : -1;
}

Data data_from_raw(const double* X, const double* y, int32_t n, int32_t p) {
  prep::Result r = prep::preprocess(X, y, n, p);
  if (r.status != "ok") throw Error(Status::invalid_input, "data_from_raw: " + r.status + " " + r.reason);
  Data D = make_data(r.own, n, r.p);
  D.p_raw = r.p_raw;
  D.y_max = r.ystd.max; D.y_mean = r.ystd.mean; D.y_sd_scaled = r.ystd.sd;
  return D;
}

ModelPost model_post(const Data& D, const Model& S) {
  ModelPost o; o.S = S;
  const int k = (int)S.size();
  if (!is_sorted_unique(S)) throw Error(Status::invalid_input, "model_post: model not sorted/unique");
  if (k > D.K) throw Error(Status::invalid_input, "model_post: |S| > K");
  BitScorer sc(&D);
  const ScoreOut so = sc.score(S);                 // bits of core/cpp/v3_score.h:214-224 (throws NumericalFailure)
  o.logm = so.logm; o.Q = so.Q; o.route = so.route; o.q_recomputed = so.q_recomputed;
  o.logdetH = so.logdetH; o.logdetA = so.logdetA;
  o.F = D.logprior[k] + o.logm;
  o.alpha_n = D.a0 + D.n / 2.0;
  o.beta_n = D.b0 + o.Q / 2.0;
  if (k == 0) return o;
  // the factor of H on the route the scorer used (core/cpp/v3_score.h:162-191): Cholesky of (n+1)G_S + I, or R of the
  // augmented QR [sqrt(n+1) X_S; I_k]; then θ̄ = n H⁻¹ z_S by the same two solves as q_nonneg (v3_score.h:147-160)
  if (so.route != ROUTE_QR) {
    const double n1 = D.n + 1.0;
    o.LH.assign((size_t)k * k, 0.0);
    for (int a = 0; a < k; ++a)
      for (int b = 0; b <= a; ++b) {
        const double g = gram(D, S[a], S[b]);
        o.LH[a * k + b] = n1 * g + (a == b ? 1.0 : 0.0);
        o.LH[b * k + a] = o.LH[a * k + b];
      }
    if (!chol_inplace(o.LH, k)) throw Error(Status::internal_error, "model_post: Cholesky failed on the scorer's route");
  } else {
    const int n = D.n, m = n + k;
    std::vector<double> MH((size_t)m * k, 0.0), v;
    const double s1 = std::sqrt(n + 1.0);
    for (int a = 0; a < k; ++a) {
      const double* xa = D.col(S[a]);
      for (int i = 0; i < n; ++i) MH[(size_t)a * m + i] = s1 * xa[i];
      MH[(size_t)a * m + n + a] = 1.0;
    }
    if (!householder_lower(MH, m, k, o.LH, v)) throw Error(Status::internal_error, "model_post: QR failed on the scorer's route");
  }
  std::vector<double> zs(k), w(k), th(k);
  for (int a = 0; a < k; ++a) zs[a] = D.z[S[a]];
  forward_solve(o.LH, k, zs.data(), w.data());
  backward_solve(o.LH, k, w.data(), th.data());
  o.theta_bar.resize(k);
  for (int a = 0; a < k; ++a) o.theta_bar[a] = D.n * th[a];
  return o;
}

}  // namespace v4::eval
