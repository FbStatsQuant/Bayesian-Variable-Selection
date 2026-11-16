// test_t7.cpp -- gate T7 (ENGINEERING_SPEC §5; plan G-A): the closed forms of the evaluator against brute-force Monte
// Carlo on 20 fixtures, to 3 significant digits. Declared before the run (tests/wp5/README_T7.md):
//   T7a  plug-in d_H² (closed form, plan §3.3 item 1) vs MC over x ~ ν_x (mt19937_64, independent of the eval's Philox),
//        the y-integral by the normal–normal affinity (checked against quadrature in test h2_normals_vs_quadrature);
//   T7b  prediction error m² + s² vs MC over x of (â + xᵀb − α* − xᵀβ*)²;
//   pass: |closed − MC| ≤ ½ unit of the 3rd significant digit of the closed form, with the MC standard error ≤ ⅓ of that
//        tolerance (the MC size doubles from 2²⁰ up to 2²⁷ draws until the SE condition holds; failing it is a FAIL).
//   T7c  (sanity, not part of the 3-digit criterion) joint (x, y) MC of d_H² within 4 SE, 2²² draws.
// Fixtures: the posterior-mean plug-in of a model near S₀ on generated data, 4 designs × n ∈ {100, 200, 400} × models
// with false positives / false negatives, so (m, s², v) cover the range seen in practice. Output: TSV in $TMPDIR.
#include <unistd.h>

#include <cstdio>
#include <random>

#include "v4/eval.h"
#include "wp5_tk.h"

using namespace v4::eval;

namespace {

struct Fixture { std::string name; Truth T; std::vector<int32_t> orig; std::vector<double> b; double a, v; };

Fixture make_fixture(int id) {
  static const char* designs[4] = {"IND", "AR", "BLK", "FAC"};
  static const int ns[3] = {100, 200, 400}; const int n = ns[id % 3];
  const std::string des = designs[id % 4];
  const int p = 60;
  Truth T; T.design = des; T.rho = des == "AR" ? 0.6 : (des == "BLK" ? 0.5 : (des == "FAC" ? 0.3 : 0.0)); T.block = 20;
  const double amp = (id % 5 == 4) ? 0.6 : 1.0;   // weak arm in 4 of 20
  T.S0 = {6, 18, 30, 42, 54}; T.beta = {amp * 1.0, amp * -0.8, amp * 0.9, amp * -0.7, amp * 0.6}; T.sigma = 1.0;
  if (id == 7) T.alpha = 0.3;
  // generate (X, y) from ν_x (mt19937_64; Cholesky of Σ) and fit the model's posterior mean
  std::mt19937_64 g(1000 + id); std::normal_distribution<double> N(0, 1);
  std::vector<int32_t> all(p); for (int j = 0; j < p; ++j) all[j] = j + 1;
  std::vector<double> Sig = design_cov_matrix(T, all), L(Sig);
  for (int j = 0; j < p; ++j) { double d = L[j * p + j]; for (int t = 0; t < j; ++t) d -= L[j * p + t] * L[j * p + t]; double r = std::sqrt(d); L[j * p + j] = r;
    for (int i = j + 1; i < p; ++i) { double s = L[i * p + j]; for (int t = 0; t < j; ++t) s -= L[i * p + t] * L[j * p + t]; L[i * p + j] = s / r; } }
  std::vector<double> X((size_t)n * p), y(n), e(p);
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < p; ++j) e[j] = N(g);
    for (int j = 0; j < p; ++j) { double s = 0; for (int t = 0; t <= j; ++t) s += L[j * p + t] * e[t]; X[(size_t)j * n + i] = s; }
    double mu = T.alpha; for (int t = 0; t < 5; ++t) mu += T.beta[t] * X[(size_t)(T.S0[t] - 1) * n + i];
    y[i] = mu + N(g);
  }
  OwnedData O = standardise(X.data(), y.data(), n, p);
  Model S;   // internal = orig − 1 (no dropped columns for continuous designs)
  switch (id % 4) {
    case 0: S = {5, 17, 29, 41, 53}; break;                 // S0
    case 1: S = {5, 17, 29, 41, 53, 11}; break;             // + a false positive
    case 2: S = {5, 17, 29, 41}; break;                     // − the smallest effect
    default: S = {5, 18, 29, 41, 53}; break;                // a neighbour of a truth (AR proxy / BLK partner)
  }
  std::sort(S.begin(), S.end());
  if (id >= 16) S = {5, 29};                                // badly misspecified: large m, s²
  Component c = component_from_post(O.D, model_post(O.D, S), 1.0);
  Fixture f; f.name = "f" + std::to_string(id) + "_" + des + "_n" + std::to_string(n);
  f.T = T; f.orig = c.orig; f.b = c.b_mean(); f.a = c.a_mean(); f.v = c.v_mean();
  return f;
}

double tol3(double x) { double e = std::floor(std::log10(std::fabs(x))); return 0.5 * std::pow(10.0, e - 2); }

// MC over x: returns mean and SE of g(Δ(x)) using `draws` draws in chunks (3 threads, one engine per chunk; deterministic)
template <class G>
void mc_x(const Fixture& f, G gfun, uint64_t draws, uint64_t seed, double& mean, double& se) {
  std::vector<int32_t> cols = f.orig; cols.insert(cols.end(), f.T.S0.begin(), f.T.S0.end());
  std::sort(cols.begin(), cols.end()); cols.erase(std::unique(cols.begin(), cols.end()), cols.end());
  const int k = (int)cols.size();
  std::vector<double> L = design_cov_matrix(f.T, cols);
  for (int j = 0; j < k; ++j) { double d = L[j * k + j]; for (int t = 0; t < j; ++t) d -= L[j * k + t] * L[j * k + t]; double r = std::sqrt(d); L[j * k + j] = r;
    for (int i = j + 1; i < k; ++i) { double s = L[i * k + j]; for (int t = 0; t < j; ++t) s -= L[i * k + t] * L[j * k + t]; L[i * k + j] = s / r; } }
  std::vector<double> d(k, 0.0);   // coefficient of x in Δ = (a − α*) + xᵀ(b − β*)
  for (size_t i = 0; i < f.orig.size(); ++i) d[std::lower_bound(cols.begin(), cols.end(), f.orig[i]) - cols.begin()] += f.b[i];
  for (size_t i = 0; i < f.T.S0.size(); ++i) d[std::lower_bound(cols.begin(), cols.end(), f.T.S0[i]) - cols.begin()] -= f.T.beta[i];
  const uint64_t CH = 1 << 18, nch = (draws + CH - 1) / CH;
  std::vector<long double> s1(nch), s2(nch);
#pragma omp parallel for schedule(dynamic) num_threads(3)
  for (long c = 0; c < (long)nch; ++c) {
    std::mt19937_64 g(seed * 1000003ULL + (uint64_t)c); std::normal_distribution<double> N(0, 1);
    std::vector<double> e(k), x(k);
    long double a1 = 0, a2 = 0;
    for (uint64_t r = 0; r < CH; ++r) {
      for (int j = 0; j < k; ++j) e[j] = N(g);
      double D = f.a - f.T.alpha;
      for (int i = 0; i < k; ++i) { double s = 0; for (int t = 0; t <= i; ++t) s += L[i * k + t] * e[t]; D += d[i] * s; }
      double v = gfun(D); a1 += v; a2 += (long double)v * v;
    }
    s1[c] = a1; s2[c] = a2;
  }
  long double A = 0, B = 0; for (uint64_t c = 0; c < nch; ++c) { A += s1[c]; B += s2[c]; }
  const double Nn = (double)(nch * CH);
  mean = (double)(A / Nn); se = std::sqrt((double)(B / Nn - (A / Nn) * (A / Nn)) / Nn);
}

}  // namespace

TEST_SLOW(gate_T7_closed_forms_vs_monte_carlo) {
  const std::string tsv = std::string(std::getenv("TMPDIR") ? std::getenv("TMPDIR") : ".") + "/T7_result.tsv";
  FILE* fo = std::fopen(tsv.c_str(), "w");
  std::fprintf(fo, "fixture\tquantity\tclosed\tmc\tmc_se\ttol3\tdraws\tpass\n");
  int pass = 0, total = 0;
  for (int id = 0; id < 20; ++id) {
    Fixture f = make_fixture(id);
    const double s2t = f.T.sigma2_eff();
    LinErr e = lin_error(f.T, f.orig, f.b, f.a);
    const double h2c = h2_plugin(e, f.v, s2t), pec = pred_error(e);
    // T7a: E_x[1 − affinity(N(Δ, v), N(0, σ²))] = 1 − E_x affinity; MC the affinity's complement directly
    struct Q { const char* name; double closed; std::function<double(double)> g; };
    const Q qs[2] = {{"plugin_h2", h2c, [&](double D) { return h2_normals(D, f.v, 0.0, s2t); }},
                     {"pred_error", pec, [&](double D) { return D * D; }}};
    for (const Q& q : qs) {
      const double tol = tol3(q.closed);
      double m = 0, se = 0; uint64_t draws = 1ull << 20;
      while (true) {
        mc_x(f, q.g, draws, 17 + id, m, se);
        if (se <= tol / 3 || draws >= (1ull << 27)) break;
        draws *= 2;
      }
      const bool ok = se <= tol / 3 && std::fabs(q.closed - m) <= tol;
      ++total; pass += ok;
      std::fprintf(fo, "%s\t%s\t%.10g\t%.10g\t%.3g\t%.3g\t%llu\t%d\n", f.name.c_str(), q.name, q.closed, m, se, tol, (unsigned long long)draws, ok);
      std::printf("    %-16s %-10s closed=%.6g mc=%.6g se=%.2g tol=%.2g draws=2^%d %s\n", f.name.c_str(), q.name, q.closed, m, se, tol,
                  (int)std::log2((double)draws), ok ? "PASS" : "FAIL");
      CHECK_MSG(ok, f.name + " " + q.name);
    }
    // T7c: joint (x, y) MC of 1 − E √(f/f*) under y ~ f* (sanity, 4 SE)
    {
      std::mt19937_64 g(99 + id); std::normal_distribution<double> N(0, 1);
      std::vector<int32_t> cols = f.orig; cols.insert(cols.end(), f.T.S0.begin(), f.T.S0.end());
      std::sort(cols.begin(), cols.end()); cols.erase(std::unique(cols.begin(), cols.end()), cols.end());
      XSample xs = draw_x(f.T, cols, 1 << 22, 123 + id, 9);   // x by the eval sampler (Philox) — y by mt19937
      long double a1 = 0, a2 = 0;
      for (size_t r = 0; r < xs.m; ++r) {
        double mu = f.a, ms = f.T.alpha; const double* x = &xs.X[r * cols.size()];
        for (size_t i = 0; i < f.orig.size(); ++i) mu += f.b[i] * x[xs.pos(f.orig[i])];
        for (size_t i = 0; i < f.T.S0.size(); ++i) ms += f.T.beta[i] * x[xs.pos(f.T.S0[i])];
        double y = ms + std::sqrt(s2t) * N(g);
        double lr = 0.5 * (-0.5 * std::log(f.v / s2t) - 0.5 * (y - mu) * (y - mu) / f.v + 0.5 * (y - ms) * (y - ms) / s2t);
        double v = std::exp(lr); a1 += v; a2 += (long double)v * v;
      }
      double m = (double)(a1 / xs.m), se = std::sqrt((double)(a2 / xs.m - (a1 / xs.m) * (a1 / xs.m)) / xs.m);
      bool ok = std::fabs((1 - m) - h2c) <= 4 * se;
      std::fprintf(fo, "%s\tplugin_h2_joint_xy\t%.10g\t%.10g\t%.3g\tNA\t%zu\t%d\n", f.name.c_str(), h2c, 1 - m, se, xs.m, ok);
      CHECK_MSG(ok, f.name + " joint (x,y) MC outside 4 SE");
    }
  }
  std::fclose(fo);
  std::printf("    gate T7: %d / %d closed-form checks pass (3 significant digits); table: %s\n", pass, total, tsv.c_str());
  CHECK(pass == total && total == 40);
}
