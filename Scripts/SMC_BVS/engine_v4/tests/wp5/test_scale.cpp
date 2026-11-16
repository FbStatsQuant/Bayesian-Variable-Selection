// test_scale.cpp -- D-17 (PR12 review MAJOR-1) and MINOR-6: O(U) quadratic forms, streamed rows equal to WP1 gen,
// design_cov against gen-sampled covariances, the top-K + tail mixture predictive against the exact full mixture
// (M ≈ 5,000, within 3 SE), and the scale test T7′ (synthetic M = 10⁵ and 10⁶ laws at p = 10⁶; wall time and peak RSS
// asserted against the driver limits).
#include <sys/resource.h>

#include <chrono>
#include <random>

#include "v4/eval.h"
#include "v4/gen.h"
#include "wp5_tk.h"

using namespace v4;
using namespace v4::eval;

namespace {
Truth gen_truth(const std::string& design, int32_t p, uint32_t seed, double rho = 0.6, int32_t b = 20) {
  Json sp = Json::object(); sp["design"] = design; sp["n"] = 200; sp["p"] = p; sp["seed"] = (int64_t)seed; sp["rho"] = rho; sp["b"] = b; sp["s0"] = 5; sp["a"] = 1.0;
  gen::Spec s = gen::spec_from_json(sp);
  gen::Truth t = gen::truth(s);
  Json tj = Json::object(); tj["spec"] = gen::spec_to_json(s); tj["S0"] = Json::array_of(t.S0); tj["beta"] = Json::array_of(t.beta); tj["sigma"] = 1.0;
  return truth_from_json(tj);
}
double peak_rss_gb() { struct rusage ru; getrusage(RUSAGE_SELF, &ru); return ru.ru_maxrss / 1048576.0; }
}  // namespace

TEST(wp5_quad_form_matches_dense) {
  std::mt19937_64 g(5); std::normal_distribution<double> N(0, 1);
  const char* des[5] = {"IND", "AR", "ADJ-OPP", "BLK", "FAC"};
  for (const char* d : des) {
    Truth T; T.design = d; T.rho = std::string(d) == "FAC" ? 0.3 : 0.6; T.block = 20;
    std::vector<int32_t> c = {1, 2, 5, 19, 20, 21, 40, 41, 77, 300, 301, 1000};   // AR gaps, BLK boundaries
    std::vector<double> v(c.size()); for (auto& x : v) x = N(g);
    std::vector<double> S = design_cov_matrix(T, c);
    double dense = 0; for (size_t i = 0; i < c.size(); ++i) for (size_t j = 0; j < c.size(); ++j) dense += v[i] * S[i * c.size() + j] * v[j];
    CHECK_NEAR(quad_form(T, c, v), dense, 1e-12 * std::max(1.0, std::fabs(dense)));
  }
}

TEST(wp5_make_rows_equal_gen_test) {
  for (const char* d : {"AR", "BLK", "IND", "ADJ-OPP"}) {
    Truth T = gen_truth(d, 500, 77);
    gen::Spec sp = gen::spec_from_json(T.gen_spec);
    std::vector<int32_t> cols = {3, 4, 20, 21, 22, 199, 333};
    std::vector<int32_t> oc; std::vector<double> Xt, yt;
    gen::generate_test(sp, 60, cols, oc, Xt, yt);
    XSample xs = make_rows(T, cols, 20, 40, 1, true);   // rows 20 … 59
    CHECK(xs.cols == oc);
    int bad = 0;
    for (uint32_t r = 0; r < 40; ++r) {
      for (size_t c = 0; c < oc.size(); ++c) if (!same_bits(xs.X[r * oc.size() + c], Xt[c * 60 + 20 + r])) ++bad;
      if (!same_bits(xs.y[r], yt[20 + r])) ++bad;
    }
    CHECK_MSG(bad == 0, std::string(d) + ": " + std::to_string(bad) + " values differ from gen::generate_test");
  }
}

TEST(wp5_design_cov_matches_gen_rows) {   // PR12 MINOR-6: the plug-in's Σ against the rows the predictive uses
  for (const char* d : {"AR", "BLK", "ADJ-OPP"}) {
    Truth T = gen_truth(d, 400, 91);
    std::vector<int32_t> cols = {19, 20, 21, 23, 40, 41, 100};   // AR gaps 1, 2, 17; BLK boundary 20 | 21, 40 | 41
    const uint32_t N = 40000;
    XSample xs = make_rows(T, cols, 0, N, 1, false);
    std::vector<int32_t> c2 = xs.cols; const size_t k = c2.size();
    double worst = 0;
    for (size_t a = 0; a < k; ++a) for (size_t b = a; b < k; ++b) {
      double s = 0; for (uint32_t r = 0; r < N; ++r) s += xs.X[r * k + a] * xs.X[r * k + b];
      worst = std::max(worst, std::fabs(s / N - design_cov(T, c2[a], c2[b])));
    }
    CHECK_MSG(worst < 0.03, std::string(d) + ": max |empirical − design_cov| = " + std::to_string(worst));
  }
}

// A law with M ≈ 5,000 conjugate components from real data (S0, S0 + j, S0 + j + l) at p = 2,000 (IND gen design, so
// rows do not depend on the column set and both estimates see the same x): approximate vs exact full mixture.
TEST_SLOW(wp5_mixture_topk_tail_vs_exact) {
  Truth T = gen_truth("IND", 2000, 13);
  gen::Spec sp = gen::spec_from_json(T.gen_spec);
  std::vector<double> X, y; gen::generate(sp, X, y);
  Data D = data_from_raw(X.data(), y.data(), sp.n, sp.p);
  Model S0; for (int32_t o : T.S0) S0.push_back(o - 1);
  std::vector<Model> ms = {S0};
  for (int32_t j = 0; j < D.p && ms.size() < 2001; ++j) if (!std::binary_search(S0.begin(), S0.end(), j)) { Model m = S0; sorted_insert(m, j); ms.push_back(m); }
  std::mt19937_64 g(3);
  while (ms.size() < 5000) { int32_t j = (int32_t)(g() % D.p), l = (int32_t)(g() % D.p); Model m = S0; if (j == l || std::binary_search(m.begin(), m.end(), j) || std::binary_search(m.begin(), m.end(), l)) continue; sorted_insert(m, j); sorted_insert(m, l); ms.push_back(m); }
  std::vector<ModelPost> mp(ms.size());
#pragma omp parallel for schedule(dynamic, 64) num_threads(3)
  for (long i = 0; i < (long)ms.size(); ++i) mp[i] = model_post(D, ms[i]);
  double fmax = -INFINITY; for (auto& m : mp) fmax = std::max(fmax, m.F);
  // flatten the weights a little (temperature 0.25) so that the tail carries visible mass: a hard case for the estimator
  std::vector<double> w(ms.size()); double ws = 0;
  for (size_t i = 0; i < ms.size(); ++i) { w[i] = std::exp(0.25 * (mp[i].F - fmax)); ws += w[i]; }
  Law L; L.name = "T";
  for (size_t i = 0; i < ms.size(); ++i) L.comps.push_back(component_from_post(D, mp[i], w[i] / ws));
  DistOpts o; o.n_draws = 1000; o.n_x = 1000; o.n_test = 1000; o.threads = 3; o.seed = 21;
  DistOpts ex = o; ex.top_k = 5000;
  Json ja = dist_metrics(L, T, D.n, o, 2), je = dist_metrics(L, T, D.n, ex, 2);
  const Json &qa = ja.at("predictive"), &qe = je.at("predictive");
  CHECK(qe.at("exact").boolean() && !qa.at("exact").boolean());
  const double h2a = qa.at("h2").num(), h2e = qe.at("h2").num(), sea = qa.at("h2_se_tail").num();
  const double kla = qa.at("kl").num(), kle = qe.at("kl").num(), ska = qa.at("kl_se_tail").num();
  std::printf("    M=%zu tail mass %.3f: d_H^2 exact %.6f approx %.6f (tail SE %.2e, x SE %.2e); KL exact %.6f approx %.6f (tail SE %.2e); dH_topK %.4f bound %.4f\n",
              L.comps.size(), qa.at("tail_mass").num(), h2e, h2a, sea, qa.at("h2_se_x").num(), kle, kla, ska, qa.at("dH_topK").num(), qa.at("dH_bound").num());
  CHECK_MSG(std::fabs(h2a - h2e) <= 3 * sea + 1e-12, "predictive d_H^2: approx outside 3 tail SE of the exact mixture");
  CHECK_MSG(std::fabs(kla - kle) <= 3 * ska + 1e-12, "KL: approx outside 3 tail SE of the exact mixture");
  CHECK(std::fabs(std::sqrt(h2e) - qa.at("dH_topK").num()) <= qa.at("dH_bound").num() + 1e-12);
  // the exact parts agree exactly (same rows, same components)
  CHECK(ja.at("weighted_plugin").dump() == je.at("weighted_plugin").dump());
  CHECK(ja.at("plugin").dump() == je.at("plugin").dump());
}

// T7′: a synthetic store law at p = 10⁶ (S0 + one null column each; M = 10⁵ and 10⁶), production settings.
namespace {
Law synthetic_law(const Truth& T, size_t M, uint64_t seed) {
  std::mt19937_64 g(seed); std::uniform_real_distribution<double> U(0, 1);
  Law L; L.name = "T"; L.comps.reserve(M);
  const int32_t n = 200; const double alpha = 0.01 + n / 2.0;
  std::vector<double> wv(M); double ws = 0;
  for (size_t m = 0; m < M; ++m) { wv[m] = m == 0 ? 0.4 * M : -std::log(U(g)); ws += wv[m]; }
  for (size_t m = 0; m < M; ++m) {
    Component c; c.w = wv[m] / ws; c.n = n; c.alpha_n = alpha; c.beta_n = 0.5 * alpha; c.ybar = 0; c.sy = 1;
    std::vector<int32_t> s = T.S0;
    if (m > 0) { int32_t j; do { j = 1 + (int32_t)(g() % 1000000); } while (std::binary_search(T.S0.begin(), T.S0.end(), j)); s.push_back(j); std::sort(s.begin(), s.end()); }
    const size_t k = s.size();
    c.orig = s; c.xbar.assign(k, 0.0); c.xsd.assign(k, 1.0); c.theta_bar.assign(k, 0.0); c.LH.assign(k * k, 0.0);
    for (size_t i = 0; i < k; ++i) {
      auto it = std::find(T.S0.begin(), T.S0.end(), s[i]);
      c.theta_bar[i] = it != T.S0.end() ? T.beta[it - T.S0.begin()] * (1 + 0.05 * (U(g) - 0.5)) : 0.02 * (U(g) - 0.5);
      c.LH[i * k + i] = std::sqrt((n + 1.0) * n);
    }
    L.comps.push_back(std::move(c));
  }
  return L;
}
}  // namespace

TEST_SLOW(wp5_T7prime_scale) {
  // law build throughput (model_post per kept store model) on real data at n = 200, extrapolated to M = 10⁶ (ESTIMATE)
  {
    Truth Tb = gen_truth("AR", 2000, 5);
    gen::Spec sp = gen::spec_from_json(Tb.gen_spec);
    std::vector<double> X, y; gen::generate(sp, X, y);
    Data D = data_from_raw(X.data(), y.data(), sp.n, sp.p);
    Model S0; for (int32_t o : Tb.S0) S0.push_back(o - 1);
    const long NM = 20000;
    std::vector<Model> ms(NM);
    for (long i = 0; i < NM; ++i) { Model m = S0; int32_t j = (int32_t)((i * 7919) % D.p); if (!std::binary_search(m.begin(), m.end(), j)) sorted_insert(m, j); ms[i] = m; }
    auto t0 = std::chrono::steady_clock::now();
    std::vector<double> F(NM);
#pragma omp parallel for schedule(dynamic, 256) num_threads(3)
    for (long i = 0; i < NM; ++i) F[i] = model_post(D, ms[i]).F;
    const double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    std::printf("    T7' law build: %.1f us per model (3 threads, Owls) -> ESTIMATE %.0f s for 10^6 models on 3 threads, %.0f s on 8\n",
                1e6 * s / NM, s / NM * 1e6, s / NM * 1e6 * 3 / 8);
  }
  Truth T = gen_truth("AR", 1000000, 4242);
  DistOpts o; o.threads = 3; o.seed = 4242;   // production sizes: 10⁴ draws, 4,000 x × 64 GH, 10⁴ test rows, K = R = 1,000
  struct Lim { size_t M; double wall_s; double rss_gb; const char* rung; };
  // driver limits (D-17 item 7): 10⁴ rung 20 min on 4 CPUs, 8 GB; 10⁶ rung 1 h on 8 CPUs, 16 GB. Owls runs 3 threads:
  // the wall limits are scaled by 4/3 and 8/3 (CPU-equivalent).
  const Lim lims[2] = {{100000, 1200.0 * 4 / 3, 8.0, "1e4 limits"}, {1000000, 3600.0 * 8 / 3, 16.0, "1e6 limits"}};
  for (const Lim& l : lims) {
    auto t0 = std::chrono::steady_clock::now();
    Law L = synthetic_law(T, l.M, 7 + l.M);
    const double t_build = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    auto t1 = std::chrono::steady_clock::now();
    Json j = dist_metrics(L, T, 200, o, 2);
    const double wall = std::chrono::duration<double>(std::chrono::steady_clock::now() - t1).count();
    const double rss = peak_rss_gb();
    std::printf("    T7' M=%zu: dist_metrics wall %.1f s (synthetic law build %.1f s), peak RSS %.2f GB, max block columns %g, tail mass %.3f, "
                "predictive d_H^2 %.5f (tail SE %.1e, x SE %.1e) [%s: wall <= %.0f s, RSS <= %.0f GB]\n",
                l.M, wall, t_build, rss, j.at("predictive").at("max_block_columns").num(), j.at("predictive").at("tail_mass").num(),
                j.at("predictive").at("h2").num(), j.at("predictive").at("h2_se_tail").num(), j.at("predictive").at("h2_se_x").num(),
                l.rung, l.wall_s, l.rss_gb);
    CHECK_MSG(wall <= l.wall_s, "T7': dist_metrics wall above the driver limit");
    CHECK_MSG(rss <= l.rss_gb, "T7': peak RSS above the driver limit");
  }
}
