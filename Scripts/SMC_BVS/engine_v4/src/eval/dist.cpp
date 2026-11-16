// dist.cpp -- W3-DIST distribution metrics (EXPERIMENT_PLAN §3.3 items 1-4) for one output object.
// Deterministic for any thread count: per-item results are stored, then reduced serially in item order (INTERFACES §7).
#include <algorithm>
#include <cmath>
#include <map>

#include "v4/eval.h"

namespace v4::eval {

using wp5prov::Address;

// ------------------------------------------------------------------------------------------------ closed forms
double h2_normals(double m1, double v1, double m2, double v2) {
  const double d = m1 - m2, sv = v1 + v2;
  const double la = 0.5 * std::log(2.0 * std::sqrt(v1 * v2) / sv) - d * d / (4.0 * sv);
  return -std::expm1(la);
}

LinErr lin_error(const Truth& T, const std::vector<int32_t>& orig, const std::vector<double>& b, double a) {
  // union of the predictor's support and S0, sorted; d = b − β* on it
  std::map<int32_t, double> d;
  for (size_t i = 0; i < orig.size(); ++i) d[orig[i]] += b[i];
  for (size_t i = 0; i < T.S0.size(); ++i) d[T.S0[i]] -= T.beta[i];
  std::vector<int32_t> c; std::vector<double> dv;
  for (auto& kv : d) { c.push_back(kv.first); dv.push_back(kv.second); }
  LinErr e;
  e.m = a - T.alpha;   // μ_x = 0 for every design of plan §2.2
  double s2 = 0;
  for (size_t i = 0; i < c.size(); ++i) {
    if (dv[i] == 0) continue;
    double row = 0;
    for (size_t j = 0; j < c.size(); ++j) if (dv[j] != 0) row += design_cov(T, c[i], c[j]) * dv[j];
    s2 += dv[i] * row;
  }
  e.s2 = std::max(0.0, s2);
  return e;
}

double h2_plugin(const LinErr& e, double v, double s2t) {
  // E_Δ[1 − H-affinity(N(Δ, v), N(0, σ²))] with Δ ~ N(m, s²):  E e^{−aΔ²} = (1 + 2as²)^{−1/2} e^{−a m²/(1 + 2as²)}
  const double sv = v + s2t, a = 1.0 / (4.0 * sv), q = 1.0 + 2.0 * a * e.s2;
  const double la = 0.5 * std::log(2.0 * std::sqrt(v * s2t) / sv) - 0.5 * std::log(q) - a * e.m * e.m / q;
  return -std::expm1(la);
}

// ------------------------------------------------------------------------------------------------ Gauss–Hermite
void gauss_hermite(int n, std::vector<double>& x, std::vector<double>& w) {
  // Newton on the orthonormal Hermite recurrence (Numerical Recipes 3rd ed. §4.6.1, gauher); weight e^{−t²}
  const double EPS = 1e-14, PIM4 = 0.7511255444649425;
  x.assign(n, 0.0); w.assign(n, 0.0);
  const int m = (n + 1) / 2;
  double z = 0, pp = 0;
  for (int i = 0; i < m; ++i) {
    if (i == 0) z = std::sqrt(2.0 * n + 1) - 1.85575 * std::pow(2.0 * n + 1, -0.16667);
    else if (i == 1) z -= 1.14 * std::pow((double)n, 0.426) / z;
    else if (i == 2) z = 1.86 * z - 0.86 * x[0];
    else if (i == 3) z = 1.91 * z - 0.91 * x[1];
    else z = 2.0 * z - x[i - 2];
    int its = 0;
    for (; its < 100; ++its) {
      double p1 = PIM4, p2 = 0.0;
      for (int j = 0; j < n; ++j) {
        double p3 = p2; p2 = p1;
        p1 = z * std::sqrt(2.0 / (j + 1)) * p2 - std::sqrt((double)j / (j + 1)) * p3;
      }
      pp = std::sqrt(2.0 * n) * p2;
      double z1 = z; z = z1 - p1 / pp;
      if (std::fabs(z - z1) <= EPS) break;
    }
    if (its >= 100) throw Error(Status::internal_error, "gauss_hermite: no convergence");
    x[i] = z; x[n - 1 - i] = -z;
    w[i] = w[n - 1 - i] = 2.0 / (pp * pp);
  }
}

// ------------------------------------------------------------------------------------------------ random draws
double normal_draw(Address& a) {
  uint32_t r[4]; wp5prov::philox_at(a, r); a.slot++;
  double u1 = (double)((((uint64_t)r[1] << 32) | r[0]) >> 11) * 0x1.0p-53;
  double u2 = (double)((((uint64_t)r[3] << 32) | r[2]) >> 11) * 0x1.0p-53;
  return std::sqrt(-2.0 * std::log1p(-u1)) * std::cos(2.0 * M_PI * u2);
}
static double unif_draw(Address& a) { double u = wp5prov::uniform_at(a); a.slot++; return u; }

double gamma_draw(double shape, Address& a) {
  if (!(shape > 0)) throw Error(Status::internal_error, "gamma_draw: shape <= 0");
  if (shape < 1.0) {   // boost: G(α) = G(α+1) U^{1/α}
    double g = gamma_draw(shape + 1.0, a);
    double u = unif_draw(a);
    return g * std::pow(1.0 - u, 1.0 / shape);
  }
  const double d = shape - 1.0 / 3.0, c = 1.0 / std::sqrt(9.0 * d);   // Marsaglia & Tsang (2000)
  for (int it = 0; it < 1000; ++it) {
    double x = normal_draw(a), v = 1.0 + c * x;
    if (v <= 0) continue;
    v = v * v * v;
    double u = unif_draw(a);
    if (std::log1p(-u) < 0.5 * x * x + d - d * v + d * std::log(v)) return d * v;
  }
  throw Error(Status::internal_error, "gamma_draw: too many rejections");
}

int XSample::pos(int32_t o) const {
  auto it = std::lower_bound(cols.begin(), cols.end(), o);
  return (it != cols.end() && *it == o) ? (int)(it - cols.begin()) : -1;
}

XSample draw_x(const Truth& T, const std::vector<int32_t>& cols, size_t m, uint32_t seed, uint32_t stage) {
  XSample xs; xs.cols = cols; xs.m = m;
  std::sort(xs.cols.begin(), xs.cols.end());
  xs.cols.erase(std::unique(xs.cols.begin(), xs.cols.end()), xs.cols.end());
  const size_t k = xs.cols.size();
  std::vector<double> L = design_cov_matrix(T, xs.cols);   // Cholesky (lower, row-major), in place
  for (size_t j = 0; j < k; ++j) {
    double d = L[j * k + j];
    for (size_t t = 0; t < j; ++t) d -= L[j * k + t] * L[j * k + t];
    if (!(d > 0)) throw Error(Status::invalid_input, "draw_x: design covariance not positive definite");
    double r = std::sqrt(d); L[j * k + j] = r;
    for (size_t i = j + 1; i < k; ++i) {
      double s = L[i * k + j];
      for (size_t t = 0; t < j; ++t) s -= L[i * k + t] * L[j * k + t];
      L[i * k + j] = s / r;
    }
    for (size_t t = j + 1; t < k; ++t) L[j * k + t] = 0.0;
  }
  xs.X.assign(m * k, 0.0);
  std::vector<double> e(k);
  for (size_t r = 0; r < m; ++r) {
    Address a; a.seed = seed; a.role = wp5prov::R_TEST; a.xph = wp5prov::X_TEST_X; a.stage = stage;
    a.particle = (uint32_t)r; a.position = 0; a.slot = 0;
    for (size_t j = 0; j < k; ++j) e[j] = normal_draw(a);
    double* row = &xs.X[r * k];
    for (size_t i = 0; i < k; ++i) { double s = 0; for (size_t t = 0; t <= i; ++t) s += L[i * k + t] * e[t]; row[i] = s; }
  }
  return xs;
}

std::vector<double> draw_y(const Truth& T, const XSample& xs, uint32_t seed, uint32_t stage) {
  std::vector<int> ps(T.S0.size());
  for (size_t i = 0; i < T.S0.size(); ++i) { ps[i] = xs.pos(T.S0[i]); if (ps[i] < 0) throw Error(Status::internal_error, "draw_y: S0 column missing"); }
  const double sd = std::sqrt(T.sigma2_eff());
  std::vector<double> y(xs.m);
  const size_t k = xs.cols.size();
  for (size_t r = 0; r < xs.m; ++r) {
    Address a; a.seed = seed; a.role = wp5prov::R_TEST; a.xph = wp5prov::X_TEST_NOISE; a.stage = stage; a.particle = (uint32_t)r;
    double mu = T.alpha;
    for (size_t i = 0; i < ps.size(); ++i) mu += xs.X[r * k + ps[i]] * T.beta[i];
    y[r] = mu + sd * normal_draw(a);
  }
  return y;
}

DistShared make_shared_draws(const Truth& T, const std::vector<int32_t>& cols, const DistOpts& o) {
  std::vector<int32_t> c = cols;
  c.insert(c.end(), T.S0.begin(), T.S0.end());
  DistShared sh;
  sh.xq = draw_x(T, c, (size_t)o.n_x, o.seed, 1);
  sh.xt = draw_x(T, c, (size_t)o.n_test, o.seed, 2);
  sh.yt = draw_y(T, sh.xt, o.seed, 2);
  return sh;
}

// ------------------------------------------------------------------------------------------------ posterior draws
ParamDraw draw_params(const Law& L, uint32_t seed, uint32_t object_id, uint32_t draw) {
  Address a; a.seed = seed; a.role = wp5prov::R_POST; a.xph = wp5prov::X_POST; a.stage = object_id; a.particle = draw; a.slot = 0;
  ParamDraw d;
  // component by inverse CDF of the weights (one uniform, slot 0)
  double u = unif_draw(a), acc = 0; d.comp = (int)L.comps.size() - 1;
  for (size_t c = 0; c < L.comps.size(); ++c) { acc += L.comps[c].w; if (u < acc) { d.comp = (int)c; break; } }
  const Component& C = L.comps[d.comp];
  if (C.gaussian) { d.b = C.b; d.a = C.a; d.v = C.sigma2; return d; }
  const size_t k = C.orig.size();
  const double g = gamma_draw(C.alpha_n, a);
  const double v = C.beta_n / g;                       // v | S ~ IG(α_n, β_n), standardised scale
  std::vector<double> xi(k), t(k);
  for (size_t i = 0; i < k; ++i) xi[i] = normal_draw(a);
  for (int i = (int)k - 1; i >= 0; --i) {              // t = L^{-T} ξ, so Cov(t) = H⁻¹
    double s = xi[i];
    for (size_t j = i + 1; j < k; ++j) s -= C.LH[j * k + i] * t[j];
    t[i] = s / C.LH[i * k + i];
  }
  const double sc = std::sqrt(C.n * v);
  d.b.resize(k); d.a = C.ybar;
  for (size_t i = 0; i < k; ++i) {
    const double th = C.theta_bar[i] + sc * t[i];
    d.b[i] = C.sy * th / C.xsd[i];
    d.a -= C.xbar[i] * d.b[i];
  }
  d.v = C.sy * C.sy * v;
  return d;
}

// ------------------------------------------------------------------------------------------------ predictive densities
struct CompAt { double loc, scale2, df; bool gauss; double lw; };
static void comps_at(const Law& L, const XSample& xs, size_t row, std::vector<CompAt>& out) {
  const size_t K = xs.cols.size();
  const double* x = &xs.X[row * K];
  out.resize(L.comps.size());
  std::vector<double> xt, w;
  for (size_t c = 0; c < L.comps.size(); ++c) {
    const Component& C = L.comps[c];
    const size_t k = C.orig.size();
    CompAt& o = out[c];
    o.lw = std::log(C.w);
    if (C.gaussian) {
      double s = C.a;
      for (size_t i = 0; i < k; ++i) { int p = xs.pos(C.orig[i]); if (p < 0) throw Error(Status::internal_error, "comps_at: column missing"); s += x[p] * C.b[i]; }
      o.loc = s; o.scale2 = C.sigma2; o.df = INFINITY; o.gauss = true;
      continue;
    }
    xt.resize(k); w.resize(k);
    double lin = 0;
    for (size_t i = 0; i < k; ++i) {
      int p = xs.pos(C.orig[i]); if (p < 0) throw Error(Status::internal_error, "comps_at: column missing");
      xt[i] = (x[p] - C.xbar[i]) / C.xsd[i];
      lin += C.theta_bar[i] * xt[i];
    }
    double q = 0;
    for (size_t i = 0; i < k; ++i) { double s = xt[i]; for (size_t t = 0; t < i; ++t) s -= C.LH[i * k + t] * w[t]; w[i] = s / C.LH[i * k + i]; q += w[i] * w[i]; }
    o.loc = C.ybar + C.sy * lin;
    o.scale2 = C.sy * C.sy * (C.beta_n / C.alpha_n) * (1.0 + C.n * q);
    o.df = 2.0 * C.alpha_n; o.gauss = false;
  }
}
static double log_comp(const CompAt& c, double y) {
  const double r = y - c.loc;
  if (c.gauss) return -0.5 * std::log(2.0 * M_PI * c.scale2) - 0.5 * r * r / c.scale2;
  const double nu = c.df;
  return std::lgamma(0.5 * (nu + 1)) - std::lgamma(0.5 * nu) - 0.5 * std::log(nu * M_PI * c.scale2) - 0.5 * (nu + 1) * std::log1p(r * r / (nu * c.scale2));
}
static double log_mix(const std::vector<CompAt>& cs, double y) {
  double m = -INFINITY;
  for (auto& c : cs) m = std::max(m, c.lw + log_comp(c, y));
  if (!std::isfinite(m)) return m;
  double s = 0;
  for (auto& c : cs) s += std::exp(c.lw + log_comp(c, y) - m);
  return m + std::log(s);
}
static double mu_star(const Truth& T, const XSample& xs, size_t row) {
  const size_t K = xs.cols.size(); double mu = T.alpha;
  for (size_t i = 0; i < T.S0.size(); ++i) { int p = xs.pos(T.S0[i]); if (p < 0) throw Error(Status::internal_error, "mu_star: S0 column missing"); mu += xs.X[row * K + p] * T.beta[i]; }
  return mu;
}

void predictive_at_x(const Law& L, const Truth& T, const XSample& xs, size_t row, const std::vector<double>& ght,
                     const std::vector<double>& ghw, double* affinity, double* kl) {
  std::vector<CompAt> cs; comps_at(L, xs, row, cs);
  const double ms = mu_star(T, xs, row), s2 = T.sigma2_eff();
  // mixture moments → centre/scale of the GH rule for √(f̄ f*) (the product of two normals' square roots)
  double m1 = 0, m2 = 0;
  for (auto& c : cs) {
    const double w = std::exp(c.lw), var = c.gauss ? c.scale2 : c.scale2 * c.df / (c.df - 2.0);
    m1 += w * c.loc; m2 += w * (var + c.loc * c.loc);
  }
  const double vm = std::max(m2 - m1 * m1, 1e-300);
  const double prec = 0.5 * (1.0 / vm + 1.0 / s2), sc2 = 1.0 / prec, cen = sc2 * 0.5 * (m1 / vm + ms / s2);
  const double sc = std::sqrt(sc2);
  const double lfs_c = -0.5 * std::log(2.0 * M_PI * s2);
  double aff = 0, k = 0;
  for (size_t i = 0; i < ght.size(); ++i) {
    const double y = cen + M_SQRT2 * sc * ght[i];
    const double lf = log_mix(cs, y), lfs = lfs_c - 0.5 * (y - ms) * (y - ms) / s2;
    aff += std::exp(std::log(ghw[i]) + ght[i] * ght[i] + 0.5 * (lf + lfs)) * M_SQRT2 * sc;
    const double y2 = ms + M_SQRT2 * std::sqrt(s2) * ght[i];
    const double lf2 = log_mix(cs, y2), lfs2 = lfs_c - ght[i] * ght[i];
    k += ghw[i] / std::sqrt(M_PI) * (lfs2 - lf2);
  }
  *affinity = aff; *kl = k;
}
double log_pred_density(const Law& L, const XSample& xs, size_t row, double y) {
  std::vector<CompAt> cs; comps_at(L, xs, row, cs); return log_mix(cs, y);
}
double pred_mean(const Law& L, const XSample& xs, size_t row) {
  std::vector<CompAt> cs; comps_at(L, xs, row, cs);
  double m = 0; for (auto& c : cs) m += std::exp(c.lw) * c.loc; return m;
}

// ------------------------------------------------------------------------------------------------ per-object metrics
static double quantile_sorted(const std::vector<double>& s, double q) {   // R type 7
  if (s.empty()) return NAN;
  double h = (s.size() - 1) * q; size_t lo = (size_t)std::floor(h), hi = std::min(lo + 1, s.size() - 1);
  return s[lo] + (h - lo) * (s[hi] - s[lo]);
}
static void mean_se(const std::vector<double>& v, double& mean, double& se) {
  double s = 0; for (double x : v) s += x; mean = s / v.size();
  double ss = 0; for (double x : v) ss += (x - mean) * (x - mean);
  se = v.size() > 1 ? std::sqrt(ss / (v.size() - 1) / v.size()) : NAN;
}

Json dist_metrics(const Law& L, const Truth& T, int32_t n_obs, const DistOpts& o, const DistShared& sh, uint32_t oid,
                  std::vector<double>* dH_out) {
  if (L.comps.empty()) throw Error(Status::internal_error, "dist_metrics: empty law");
  double wsum = 0; for (auto& c : L.comps) wsum += c.w;
  if (std::fabs(wsum - 1.0) > 1e-9) throw Error(Status::internal_error, "dist_metrics: weights do not sum to 1");
  const double s2 = T.sigma2_eff();
  Json J = Json::object();
  J.set("object", L.name);
  J.set("n_components", (int64_t)L.comps.size());
  J.set("dropped_mass", L.dropped_mass);

  // 1. plug-in (posterior mean of (b, a, v)) — closed form
  std::map<int32_t, double> bm; double am = 0, vm = 0;
  for (auto& c : L.comps) {
    std::vector<double> b = c.b_mean();
    for (size_t i = 0; i < c.orig.size(); ++i) bm[c.orig[i]] += c.w * b[i];
    am += c.w * c.a_mean(); vm += c.w * c.v_mean();
  }
  std::vector<int32_t> bo; std::vector<double> bv;
  for (auto& kv : bm) { bo.push_back(kv.first); bv.push_back(kv.second); }
  LinErr e = lin_error(T, bo, bv, am);
  const double h2p = h2_plugin(e, vm, s2);
  Json P = Json::object();
  P.set("h2", h2p); P.set("dH", std::sqrt(h2p)); P.set("n_h2", n_obs * h2p);
  P.set("m", e.m); P.set("s2", e.s2); P.set("v", vm); P.set("pred_error", pred_error(e));
  J.set("plugin", P);

  // 2. posterior law of d_H by conjugate draws
  std::vector<double> dh((size_t)o.n_draws);
#pragma omp parallel for schedule(static) num_threads(o.threads)
  for (int i = 0; i < o.n_draws; ++i) {
    ParamDraw d = draw_params(L, o.seed, oid, (uint32_t)i);
    const Component& C = L.comps[d.comp];
    LinErr ei = lin_error(T, C.orig, d.b, d.a);
    dh[i] = std::sqrt(h2_plugin(ei, d.v, s2));
  }
  std::vector<double> sd = dh; std::sort(sd.begin(), sd.end());
  Json D = Json::object();
  double dm = 0; for (double x : dh) dm += x; dm /= dh.size();
  D.set("n_draws", o.n_draws); D.set("mean", dm);
  D.set("q05", quantile_sorted(sd, 0.05)); D.set("q25", quantile_sorted(sd, 0.25)); D.set("q50", quantile_sorted(sd, 0.5));
  D.set("q75", quantile_sorted(sd, 0.75)); D.set("q95", quantile_sorted(sd, 0.95));
  Json tail = Json::array();
  for (double c : o.eps_c) {
    const double eps2 = c * std::log((double)n_obs) / n_obs;
    size_t cnt = 0; for (double x : dh) if (x * x > eps2) ++cnt;
    Json t = Json::object(); t.set("c", c); t.set("eps2", eps2); t.set("prob", (double)cnt / dh.size());
    tail.push(t);
  }
  D.set("tail", tail);
  J.set("post_dH", D);
  if (dH_out) *dH_out = dh;

  // 3. predictive Hellinger and KL: n_x draws of x × n_gh Gauss–Hermite nodes in y
  std::vector<double> ght, ghw; gauss_hermite(o.n_gh, ght, ghw);
  std::vector<double> aff(sh.xq.m), kl(sh.xq.m);
#pragma omp parallel for schedule(static) num_threads(o.threads)
  for (long r = 0; r < (long)sh.xq.m; ++r) predictive_at_x(L, T, sh.xq, (size_t)r, ght, ghw, &aff[r], &kl[r]);
  double am_, ase, km, kse; mean_se(aff, am_, ase); mean_se(kl, km, kse);
  Json Q = Json::object();
  Q.set("h2", 1.0 - am_); Q.set("h2_se", ase); Q.set("n_h2", n_obs * (1.0 - am_));
  Q.set("kl", km); Q.set("kl_se", kse); Q.set("n_x", (int64_t)sh.xq.m); Q.set("n_gh", o.n_gh);
  J.set("predictive", Q);

  // 4. test rows: MSE of the predictive mean and mean log predictive density
  std::vector<double> se2(sh.xt.m), lpd(sh.xt.m);
#pragma omp parallel for schedule(static) num_threads(o.threads)
  for (long r = 0; r < (long)sh.xt.m; ++r) {
    std::vector<CompAt> cs; comps_at(L, sh.xt, (size_t)r, cs);
    double mu = 0; for (auto& c : cs) mu += std::exp(c.lw) * c.loc;
    se2[r] = (sh.yt[r] - mu) * (sh.yt[r] - mu);
    lpd[r] = log_mix(cs, sh.yt[r]);
  }
  double mm, mse_, lm, lse; mean_se(se2, mm, mse_); mean_se(lpd, lm, lse);
  Json Tt = Json::object();
  Tt.set("mse", mm); Tt.set("mse_se", mse_); Tt.set("mlpd", lm); Tt.set("mlpd_se", lse); Tt.set("n_test", (int64_t)sh.xt.m);
  J.set("test", Tt);
  return J;
}

}  // namespace v4::eval
