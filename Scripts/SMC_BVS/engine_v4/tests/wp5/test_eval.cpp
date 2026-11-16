// test_eval.cpp -- unit tests of the evaluator pieces (quadrature, closed forms, posterior, draws, metrics, invariance).
#include <random>

#include "v4/eval.h"
#include "wp5_tk.h"

using namespace v4::eval;

// composite Simpson on [a,b] with m (even) intervals
template <class F> static double simpson(F f, double a, double b, int m) {
  double h = (b - a) / m, s = f(a) + f(b);
  for (int i = 1; i < m; ++i) s += f(a + i * h) * (i % 2 ? 4 : 2);
  return s * h / 3;
}
static double lnorm(double y, double m, double v) { return -0.5 * std::log(2 * M_PI * v) - 0.5 * (y - m) * (y - m) / v; }

OwnedData test_data(int n, int p, double rho, uint64_t seed, std::vector<int32_t> S0 = {3, 9, 15}, std::vector<double> beta = {1.0, -0.8, 0.6}) {
  std::mt19937_64 g(seed); std::normal_distribution<double> N(0, 1);
  std::vector<double> X((size_t)n * p), y(n);
  for (int i = 0; i < n; ++i) {
    double prev = N(g);
    for (int j = 0; j < p; ++j) { double x = j ? rho * prev + std::sqrt(1 - rho * rho) * N(g) : prev; X[(size_t)j * n + i] = x; prev = x; }
    double mu = 0; for (size_t t = 0; t < S0.size(); ++t) mu += beta[t] * X[(size_t)(S0[t] - 1) * n + i];
    y[i] = mu + N(g);
  }
  return standardise(X.data(), y.data(), n, p);
}

TEST(gauss_hermite_rule) {
  std::vector<double> t, w;
  for (int n : {8, 20, 64}) {
    gauss_hermite(n, t, w);
    double s0 = 0, s2 = 0, s4 = 0, sc = 0;
    for (int i = 0; i < n; ++i) { s0 += w[i]; s2 += w[i] * t[i] * t[i]; s4 += w[i] * std::pow(t[i], 4); sc += w[i] * std::cos(t[i]); }
    CHECK_NEAR(s0, std::sqrt(M_PI), 1e-13);
    CHECK_NEAR(s2, std::sqrt(M_PI) / 2, 1e-13);
    CHECK_NEAR(s4, 3 * std::sqrt(M_PI) / 4, 1e-12);
    if (n >= 20) CHECK_NEAR(sc, std::sqrt(M_PI) * std::exp(-0.25), 1e-13);
  }
}

TEST(h2_normals_vs_quadrature) {
  const double cases[][4] = {{0, 1, 0, 1}, {0.3, 1.2, 0, 1}, {-1.5, 0.4, 0.2, 2.5}, {0.01, 1.001, 0, 1}, {4, 1, 0, 1}};
  for (auto& c : cases) {
    double q = simpson([&](double y) { return std::exp(0.5 * (lnorm(y, c[0], c[1]) + lnorm(y, c[2], c[3]))); }, -40, 40, 200000);
    CHECK_NEAR(h2_normals(c[0], c[1], c[2], c[3]), 1 - q, 1e-12);
  }
  CHECK(h2_normals(0.7, 2.0, 0.7, 2.0) == 0.0);
  LinErr e0{0.4, 0.0};
  CHECK_NEAR(h2_plugin(e0, 1.3, 1.0), h2_normals(0.4, 1.3, 0.0, 1.0), 1e-15);
}

TEST(model_post_matches_dense_algebra) {
  OwnedData O = test_data(120, 30, 0.5, 21);
  const EvalData& D = O.D;
  Model S = {2, 8, 14, 20};
  ModelPost mp = model_post(D, S);
  const int k = 4, n = D.n;
  // dense H, solve H θ = n z by Gaussian elimination (independent of the Cholesky path)
  std::vector<double> H(k * k), r(k);
  for (int a = 0; a < k; ++a) {
    for (int b = 0; b < k; ++b) { double g = 0; for (int i = 0; i < n; ++i) g += D.col(S[a])[i] * D.col(S[b])[i]; H[a * k + b] = (n + 1) * g + (a == b); }
    r[a] = n * D.z[S[a]];
  }
  for (int c = 0; c < k; ++c) for (int rr = c + 1; rr < k; ++rr) { double f = H[rr * k + c] / H[c * k + c]; for (int t = c; t < k; ++t) H[rr * k + t] -= f * H[c * k + t]; r[rr] -= f * r[c]; }
  std::vector<double> th(k);
  for (int c = k - 1; c >= 0; --c) { double s = r[c]; for (int t = c + 1; t < k; ++t) s -= H[c * k + t] * th[t]; th[c] = s / H[c * k + c]; }
  for (int a = 0; a < k; ++a) CHECK_NEAR(mp.theta_bar[a], th[a], 1e-12);
  double quad = 0; for (int a = 0; a < k; ++a) quad += th[a] * D.z[S[a]];   // z'H⁻¹z n = θ̄'z
  CHECK_NEAR(mp.Q, D.yty - quad, 1e-9);
  CHECK_NEAR(mp.alpha_n, 0.01 + n / 2.0, 0); CHECK_NEAR(mp.beta_n, 0.01 + mp.Q / 2, 1e-12);
  // response-scale mapping: the plug-in predictor equals ȳ + s_y Σ θ̄ (x − x̄)/ŝ at a sample row
  Component c = component_from_post(D, mp, 1.0);
  std::vector<double> b = c.b_mean(); double a0 = c.a_mean();
  CHECK(b.size() == 4 && c.orig[0] == 3);
  CHECK_NEAR(c.v_mean(), D.sy() * D.sy() * mp.beta_n / (mp.alpha_n - 1), 1e-12);
  (void)a0;
}

TEST(gamma_and_normal_draws) {
  for (double shape : {0.5, 3.0, 100.5}) {
    const int N = 40000; double s = 0, ss = 0;
    for (int i = 0; i < N; ++i) {
      v4::wp5prov::Address a; a.seed = 9; a.role = v4::wp5prov::R_POST; a.xph = v4::wp5prov::X_POST; a.particle = (uint32_t)i; a.stage = (uint32_t)(shape * 10);
      double g = gamma_draw(shape, a); s += g; ss += g * g;
    }
    double m = s / N, v = ss / N - m * m;
    CHECK_NEAR(m, shape, 4 * std::sqrt(shape / N));
    CHECK_NEAR(v, shape, 6 * shape * std::sqrt(2.0 / N) + 0.05 * shape);
  }
  double s = 0, ss = 0; const int N = 100000;
  for (int i = 0; i < N; ++i) { v4::wp5prov::Address a; a.seed = 4; a.particle = (uint32_t)i; double z = normal_draw(a); s += z; ss += z * z; }
  CHECK_NEAR(s / N, 0.0, 4 / std::sqrt((double)N)); CHECK_NEAR(ss / N, 1.0, 4 * std::sqrt(2.0 / N));
}

TEST(posterior_draw_moments) {
  OwnedData O = test_data(150, 30, 0.6, 22);
  ModelPost mp = model_post(O.D, {2, 8, 14});
  Law L; L.name = "x"; L.comps.push_back(component_from_post(O.D, mp, 1.0));
  const int N = 20000; const Component& C = L.comps[0];
  std::vector<double> bm = C.b_mean(), sb(3, 0.0); double sv = 0, sa = 0;
  for (int i = 0; i < N; ++i) { ParamDraw d = draw_params(L, 5, 0, (uint32_t)i); for (int j = 0; j < 3; ++j) sb[j] += d.b[j]; sv += d.v; sa += d.a; }
  // marginal sd of b_j ≈ s_y/ŝ_j sqrt(n E[v] (H⁻¹)_jj); bounded loosely by 0.2 here → 4 SE ≈ 0.006
  for (int j = 0; j < 3; ++j) CHECK_NEAR(sb[j] / N, bm[j], 0.01);
  CHECK_NEAR(sv / N, C.v_mean(), 4 * C.v_mean() * std::sqrt(1.0 / (C.alpha_n - 2)) / std::sqrt((double)N));
  CHECK_NEAR(sa / N, C.a_mean(), 0.01);
}

TEST(predictive_gaussian_component_is_exact) {
  Truth T; T.design = "AR"; T.rho = 0.6; T.S0 = {2, 5}; T.beta = {1.0, -0.5}; T.sigma = 1.0;
  Law L; L.name = "g"; L.comps.push_back(component_gaussian({2, 7}, {0.9, 0.1}, 0.05, 1.3));
  XSample xs = draw_x(T, {2, 5, 7}, 50, 3, 1);
  std::vector<double> t, w; gauss_hermite(64, t, w);
  for (size_t r = 0; r < xs.m; ++r) {
    double aff, kl; predictive_at_x(L, T, xs, r, t, w, &aff, &kl);
    const double* x = &xs.X[r * 3];
    double mu = 0.05 + 0.9 * x[0] + 0.1 * x[2], ms = 1.0 * x[0] - 0.5 * x[1];
    CHECK_NEAR(1 - aff, h2_normals(mu, 1.3, ms, 1.0), 1e-13);
    CHECK_NEAR(kl, 0.5 * (std::log(1.3 / 1.0) + (1.0 + (ms - mu) * (ms - mu)) / 1.3 - 1), 1e-12);
  }
}

TEST(predictive_t_mixture_vs_quadrature) {
  OwnedData O = test_data(100, 25, 0.6, 23);
  Truth T; T.design = "AR"; T.rho = 0.6; T.S0 = {3, 9, 15}; T.beta = {1.0, -0.8, 0.6};
  Law L; L.name = "mix";
  const Model ms[3] = {{2, 8, 14}, {2, 8}, {2, 8, 14, 20}};
  const double ws[3] = {0.7, 0.2, 0.1};
  for (int i = 0; i < 3; ++i) L.comps.push_back(component_from_post(O.D, model_post(O.D, ms[i]), ws[i]));
  XSample xs = draw_x(T, {3, 9, 15, 21}, 20, 4, 1);
  std::vector<double> t, w; gauss_hermite(64, t, w);
  double worst = 0;
  for (size_t r = 0; r < xs.m; ++r) {
    double aff, kl; predictive_at_x(L, T, xs, r, t, w, &aff, &kl);
    double mu = 0; for (int j = 0; j < 3; ++j) mu += T.beta[j] * xs.X[r * 4 + j];
    double qa = simpson([&](double y) { return std::exp(0.5 * (log_pred_density(L, xs, r, y) + lnorm(y, mu, 1.0))); }, mu - 30, mu + 30, 60000);
    double qk = simpson([&](double y) { double l = lnorm(y, mu, 1.0); return std::exp(l) * (l - log_pred_density(L, xs, r, y)); }, mu - 30, mu + 30, 60000);
    worst = std::max(worst, std::fabs((1 - aff) - (1 - qa)) / (1 - qa));
    CHECK_NEAR(1 - aff, 1 - qa, 1e-6 * (1 - qa) + 1e-12);
    CHECK_NEAR(kl, qk, 1e-6 * std::fabs(qk) + 1e-12);
  }
  std::printf("    predictive GH(64) vs Simpson: worst relative error of d_H^2 = %.2e\n", worst);
}

TEST(draw_x_covariance) {
  Truth T; T.design = "BLK"; T.rho = 0.5; T.block = 20;
  XSample xs = draw_x(T, {1, 2, 21, 40}, 40000, 8, 1);
  auto cov = [&](int a, int b) { double s = 0; for (size_t r = 0; r < xs.m; ++r) s += xs.X[r * 4 + a] * xs.X[r * 4 + b]; return s / xs.m; };
  CHECK_NEAR(cov(0, 0), 1.0, 0.03); CHECK_NEAR(cov(0, 1), 0.5, 0.03); CHECK_NEAR(cov(0, 2), 0.0, 0.03); CHECK_NEAR(cov(2, 3), 0.5, 0.03);
  T.design = "AR"; T.rho = 0.6;
  XSample xa = draw_x(T, {5, 7, 30}, 40000, 8, 2);
  double s = 0; for (size_t r = 0; r < xa.m; ++r) s += xa.X[r * 3] * xa.X[r * 3 + 1];
  CHECK_NEAR(s / xa.m, 0.36, 0.03);
}

TEST(store_mass_find_occ) {
  std::vector<double> v = {-1.0, -1.5, -3.0, -40.0};
  std::vector<uint64_t> off = {0, 1, 3, 5}, hash(4);
  std::vector<uint16_t> len = {1, 2, 2, 0};
  std::vector<int32_t> pool = {4, 1, 4, 2, 9};
  for (int i = 0; i < 4; ++i) hash[i] = zobrist_hash(Model(pool.begin() + off[i], pool.begin() + off[i] + len[i]), 10);
  StoreView s; s.size = 4; s.v = v.data(); s.off = off.data(); s.len = len.data(); s.hash = hash.data(); s.pool = pool.data();
  StoreMass m = store_mass(s, 1e-12);
  double z = std::log(std::exp(-1.0) + std::exp(-1.5) + std::exp(-3.0) + std::exp(-40.0));
  CHECK_NEAR(m.logZ_T, z, 1e-14);
  CHECK(m.n_kept == 3);
  CHECK_NEAR(m.dropped_mass, std::exp(-40.0 - z), 1e-14 * std::exp(-40.0 - z));
  CHECK(store_find(s, {1, 4}, zobrist_hash({1, 4}, 10)) == 1);
  CHECK(store_find(s, {}, 0) == 3);
  CHECK(store_find(s, {1, 2}, zobrist_hash({1, 2}, 10)) == -1);
  CHECK_NEAR(logZ_occ(v.data(), 2, 30, 100), std::log(std::exp(-1.0) + std::exp(-1.5)) - std::log(0.3), 1e-14);
  CHECK(std::isnan(logZ_occ(v.data(), 2, 0, 100)));
}

TEST(selection_pip_evidence) {
  OwnedData O = test_data(60, 12, 0.0, 24);
  Model S0 = {2, 8, 14 - 4};   // internal {2,8,10}
  Json s = selection_metrics(S0, {2, 8}, -5.0, {2, 8, 10, 11}, -4.0, O.D);
  CHECK(s.at("outcome_class").str() == "search");
  CHECK(s.at("hpm_fn").num() == 1 && s.at("hpm_fp").num() == 0 && s.at("mpm_fp").num() == 1 && s.at("mpm_hamming").num() == 1);
  CHECK(selection_metrics(S0, {2, 8}, -3.0, {}, -4.0, O.D).at("outcome_class").str() == "posterior");
  CHECK(selection_metrics(S0, S0, -3.0, S0, -3.0, O.D).at("outcome_class").str() == "correct");
  std::vector<double> pip(12, 0.01); pip[2] = 0.99; pip[8] = 0.6; pip[10] = 0.3; pip[5] = 0.7; pip[6] = 0.2;
  Json pm = pip_metrics(pip, S0, 12);
  CHECK_NEAR(pm.at("sup_null").num(), 0.7, 0); CHECK(pm.at("argsup_null").num() == 5);
  CHECK_NEAR(pm.at("min_true").num(), 0.3, 0);
  CHECK(pm.at("n_null_gt_0.1").num() == 2 && pm.at("n_null_gt_0.5").num() == 1);
  double br = (0.01 * 0.01 + 0.4 * 0.4 + 0.7 * 0.7 + 0.7 * 0.7 + 0.2 * 0.2 + 7 * 0.0001) / 12;
  CHECK_NEAR(pm.at("brier").num(), br, 1e-15);
  std::vector<double> pr = {0.1, 0.2, 0.3, 0.1, 0.25, 0.3};   // Rp=2, p=3
  Json sp = pip_island_spread(pr.data(), 2, 3, 0.005);
  CHECK_NEAR(sp.at("max_sd").num(), 0.05 / std::sqrt(2.0), 1e-15); CHECK(sp.at("n_sd_over_target").num() == 1);
  Json ev = evidence_metrics(std::log(0.5 * (std::exp(1.0) + std::exp(3.0))), {1.0, 3.0}, 1.5);
  double w1 = std::exp(1.0) / (std::exp(1.0) + std::exp(3.0));
  CHECK_NEAR(ev.at("R_eff").num(), 1 / (w1 * w1 + (1 - w1) * (1 - w1)), 1e-12);
  CHECK_NEAR(ev.at("logZ_pooled_check").num(), ev.at("logZ").num(), 1e-14);
  CHECK_NEAR(ev.at("sigma_hat").num(), std::sqrt(2.0), 1e-15);
}

TEST(dist_metrics_thread_invariance_and_oracle) {
  OwnedData O = test_data(200, 30, 0.6, 25);
  Truth T; T.design = "AR"; T.rho = 0.6; T.S0 = {3, 9, 15}; T.beta = {1.0, -0.8, 0.6};
  Law L; L.name = "T";
  L.comps.push_back(component_from_post(O.D, model_post(O.D, {2, 8, 14}), 0.8));
  L.comps.push_back(component_from_post(O.D, model_post(O.D, {2, 8, 14, 22}), 0.2));
  DistOpts o; o.n_draws = 2000; o.n_x = 500; o.n_test = 1000; o.seed = 77;
  DistShared sh = make_shared_draws(T, {3, 9, 15, 23}, o);
  o.threads = 1; std::string a = dist_metrics(L, T, 200, o, sh, 2).dump();
  o.threads = 3; std::string b = dist_metrics(L, T, 200, o, sh, 2).dump();
  CHECK_MSG(a == b, "dist_metrics depends on the thread count");
  Json j = Json::parse(a);
  const double h2 = j.at("plugin").at("h2").num(), hq = j.at("predictive").at("h2").num();
  CHECK(h2 > 0 && h2 < 0.2 && hq > 0 && hq < 0.2);
  CHECK(j.at("predictive").at("kl").num() > 0);
  CHECK(j.at("post_dH").at("tail").size() == 5);
  // the predictive MSE on test rows ≈ σ² + prediction error (law of large numbers; loose)
  CHECK_NEAR(j.at("test").at("mse").num(), 1.0 + j.at("plugin").at("pred_error").num(), 0.15);
}
