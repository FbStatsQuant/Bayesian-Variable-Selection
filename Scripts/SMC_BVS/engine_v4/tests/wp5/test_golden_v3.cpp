// test_golden_v3.cpp -- golden bit test of eval::model_post (scores through WP1's BitScorer; θ̄ and the factor of H
// recomputed by WP5) against the reference headers of core/ (v3.1 / revision D) compiled unchanged in this binary:
// logm, Q, route, log dets and F = logprior[k] + logm must equal v3::Scorer's bits; θ̄ must equal v3's own posterior
// mean b = n H⁻¹ z_S of q_nonneg (core/cpp/v3_score.h:142-157) to rounding (it is recomputed, so 1e-13 relative).
#include <cstring>
#include <random>

#include "v3_score.h"   // core/cpp (read only)
#include "v4/eval.h"
#include "wp5_tk.h"

using namespace v4;
using namespace v4::eval;

static Data make_golden_data(int n, int p, double rho, uint64_t seed, bool exact_fit) {
  std::mt19937_64 g(seed); std::normal_distribution<double> N(0, 1);
  std::vector<double> X((size_t)n * p), y(n, 0.0);
  for (int i = 0; i < n; ++i) {
    double prev = N(g);
    for (int j = 0; j < p; ++j) { double x = j ? rho * prev + std::sqrt(1 - rho * rho) * N(g) : prev; X[(size_t)j * n + i] = 3.0 + 2.0 * x; prev = x; }
  }
  for (int i = 0; i < n; ++i) {
    y[i] = 1.0 + X[(size_t)2 * n + i] - 0.8 * X[(size_t)7 * n + i] + 0.6 * X[(size_t)(p - 3) * n + i];
    if (!exact_fit) y[i] += N(g);
  }
  return data_from_raw(X.data(), y.data(), n, p);
}

static void compare_with_v3(const Data& D, int n_models, uint64_t seed) {
  v3::Data R;
  std::vector<int> orig(D.orig, D.orig + D.p);
  v3::data_init(R, D.Xs, D.ys, D.n, D.p, orig);
  for (int k = 0; k <= D.K; ++k) CHECK(same_bits(R.logprior[k], D.logprior[k]));
  v3::Scorer sc(&R);
  std::mt19937_64 g(seed);
  int mism = 0, theta_bad = 0;
  for (int t = 0; t < n_models; ++t) {
    int k = (int)(g() % (uint64_t)std::min(D.K + 1, 13));
    std::vector<int> all(D.p); for (int j = 0; j < D.p; ++j) all[j] = j;
    std::shuffle(all.begin(), all.end(), g);
    std::vector<int> S(all.begin(), all.begin() + k); std::sort(S.begin(), S.end());
    if (t < 3) S = {2, 7, D.p - 3};   // the true model
    v3::ScoreOut ro = sc.score(S);
    ModelPost mp = model_post(D, Model(S.begin(), S.end()));
    bool same = same_bits(ro.logm, mp.logm) && same_bits(ro.Q, mp.Q) && ro.route == mp.route &&
                ro.q_recomputed == mp.q_recomputed && same_bits(ro.logdetH, mp.logdetH) && same_bits(ro.logdetA, mp.logdetA) &&
                same_bits(R.logprior[S.size()] + ro.logm, mp.F);
    if (!same) ++mism;
    // v3's posterior mean: q_nonneg's beta = n H⁻¹ z_S (reproduced here with v3's own solves on v3's Cholesky)
    if (!S.empty()) {
      const int kk = (int)S.size();
      std::vector<double> H((size_t)kk * kk), w(kk), b(kk), z(kk);
      for (int a = 0; a < kk; ++a) { z[a] = D.n * R.z[S[a]]; for (int c = 0; c < kk; ++c) H[a * kk + c] = (D.n + 1.0) * R.Gat(S[a], S[c]) + (a == c); }
      v3::chol_inplace(H, kk); v3::forward_solve(H, kk, z.data(), w.data()); v3::backward_solve(H, kk, w.data(), b.data());
      for (int a = 0; a < kk; ++a) if (std::fabs(b[a] - mp.theta_bar[a]) > 1e-13 * std::max(1.0, std::fabs(b[a]))) { ++theta_bad; break; }
    }
  }
  CHECK_MSG(mism == 0, std::to_string(mism) + " bit mismatches");
  CHECK_MSG(theta_bad == 0, std::to_string(theta_bad) + " posterior means differ");
}

TEST(wp5_golden_model_post_vs_core_v3) {
  compare_with_v3(make_golden_data(80, 40, 0.6, 11, false), 600, 5);
  compare_with_v3(make_golden_data(37, 25, 0.9, 12, false), 600, 6);   // odd n, strong correlation, K = 18
  // y exactly in span(S0). (The Q-recompute branch, Q < 1e-8 y'y, is not reachable with this prior: the ridge term keeps
  // Q ≥ about y'y/(n+1); WP1's test_score covers it through the score_route hook.)
  compare_with_v3(make_golden_data(50, 20, 0.3, 13, true), 300, 7);
}
