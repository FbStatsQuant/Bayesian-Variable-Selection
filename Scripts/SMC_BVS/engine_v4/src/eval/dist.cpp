// dist.cpp -- W3-DIST distribution metrics (EXPERIMENT_PLAN §3.3 items 1-4) for one output object, at production scale
// (DECISIONS D-17, PR12 review MAJOR-1): O(M) closed forms over the whole law, sparse draws by binary search, the
// mixture predictive by exact top-K + stratified tail importance sample, row-block streaming over the columns in use.
// Deterministic for any thread count: per-item results are stored, then reduced serially in item order (INTERFACES §7).
#include <algorithm>
#include <cmath>
#include <numeric>

#include "v4/eval.h"
#include "v4/gen.h"
#include "v4/pmath.h"

namespace v4::eval {

// ------------------------------------------------------------------------------------------------ closed forms
double h2_normals(double m1, double v1, double m2, double v2) {
  const double d = m1 - m2, sv = v1 + v2;
  const double la = 0.5 * std::log(2.0 * std::sqrt(v1 * v2) / sv) - d * d / (4.0 * sv);
  return -std::expm1(la);
}

double quad_form(const Truth& T, const std::vector<int32_t>& c, const std::vector<double>& d) {
  const size_t U = c.size();
  const std::string& g = T.design;
  double ss = 0; for (size_t i = 0; i < U; ++i) ss += d[i] * d[i];
  if (g == "IND") return ss;
  if (g == "FAC") { double s = 0; for (double x : d) s += x; return T.rho * s * s + (1 - T.rho) * ss; }
  if (g == "BLK") {   // Σ_b [ρ (Σ_{j∈b} d_j)² + (1 − ρ) Σ_{j∈b} d_j²]
    double acc = 0, bs = 0; int64_t cur = -1;
    for (size_t i = 0; i < U; ++i) {
      const int64_t b = (c[i] - 1) / T.block;
      if (b != cur) { acc += T.rho * bs * bs; bs = 0; cur = b; }
      bs += d[i];
    }
    acc += T.rho * bs * bs;
    return acc + (1 - T.rho) * ss;
  }
  if (g == "AR" || g == "ADJ-OPP") {   // Σ_{i,l} d_i d_l ρ^{|c_i − c_l|} = Σ d_l² + 2 Σ_l d_l S_l, S_l = Σ_{i<l} d_i ρ^{c_l − c_i}
    double acc = ss, S = 0;
    for (size_t l = 1; l < U; ++l) {
      S = (S + d[l - 1]) * std::pow(T.rho, (double)(c[l] - c[l - 1]));
      acc += 2.0 * d[l] * S;
    }
    return acc;
  }
  throw Error(Status::invalid_input, "quad_form: unknown design " + g);
}

LinErr lin_error(const Truth& T, const std::vector<int32_t>& orig, const std::vector<double>& b, double a) {
  // d = b − β* on the sorted union of the predictor's support and S0 (sorted merge, O(k + s0))
  std::vector<int32_t> c; std::vector<double> d;
  c.reserve(orig.size() + T.S0.size()); d.reserve(orig.size() + T.S0.size());
  size_t i = 0, j = 0;
  while (i < orig.size() || j < T.S0.size()) {
    if (j == T.S0.size() || (i < orig.size() && orig[i] < T.S0[j])) { c.push_back(orig[i]); d.push_back(b[i]); ++i; }
    else if (i == orig.size() || T.S0[j] < orig[i]) { c.push_back(T.S0[j]); d.push_back(-T.beta[j]); ++j; }
    else { c.push_back(orig[i]); d.push_back(b[i] - T.beta[j]); ++i; ++j; }
  }
  LinErr e;
  e.m = a - T.alpha;   // μ_x = 0 for every design of plan §2.2 / WP1 gen
  e.s2 = std::max(0.0, quad_form(T, c, d));
  return e;
}

double h2_plugin(const LinErr& e, double v, double s2t) {
  // E_Δ[1 − affinity(N(Δ, v), N(0, σ²))], Δ ~ N(m, s²):  E e^{−aΔ²} = (1 + 2as²)^{−1/2} e^{−a m²/(1 + 2as²)}
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
      for (int j = 0; j < n; ++j) { double p3 = p2; p2 = p1; p1 = z * std::sqrt(2.0 / (j + 1)) * p2 - std::sqrt((double)j / (j + 1)) * p3; }
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
  double u1, u2; uniform2_at(a, u1, u2); a.slot++;
  return std::sqrt(-2.0 * std::log1p(-u1)) * std::cos(2.0 * M_PI * u2);
}
static double unif_draw(Address& a) { double u = uniform_at(a); a.slot++; return u; }

double gamma_draw(double shape, Address& a) {
  if (!(shape > 0)) throw Error(Status::internal_error, "gamma_draw: shape <= 0");
  if (shape < 1.0) { double g = gamma_draw(shape + 1.0, a); double u = unif_draw(a); return g * std::pow(1.0 - u, 1.0 / shape); }
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
  std::vector<double> L = design_cov_matrix(T, xs.cols);
  for (size_t j = 0; j < k; ++j) {
    double d = L[j * k + j];
    for (size_t t = 0; t < j; ++t) d -= L[j * k + t] * L[j * k + t];
    if (!(d > 0)) throw Error(Status::invalid_input, "draw_x: design covariance not positive definite");
    double r = std::sqrt(d); L[j * k + j] = r;
    for (size_t i = j + 1; i < k; ++i) { double s = L[i * k + j]; for (size_t t = 0; t < j; ++t) s -= L[i * k + t] * L[j * k + t]; L[i * k + j] = s / r; }
    for (size_t t = j + 1; t < k; ++t) L[j * k + t] = 0.0;
  }
  xs.X.assign(m * k, 0.0);
  std::vector<double> e(k);
  for (size_t r = 0; r < m; ++r) {
    Address a; a.seed = seed; a.role = R_TEST; a.xph = X_TEST_X; a.stage = stage; a.particle = (uint32_t)r;
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
    Address a; a.seed = seed; a.role = R_TEST; a.xph = X_TEST_NOISE; a.stage = stage; a.particle = (uint32_t)r;
    double mu = T.alpha;
    for (size_t i = 0; i < ps.size(); ++i) mu += xs.X[r * k + ps[i]] * T.beta[i];
    y[r] = mu + sd * normal_draw(a);
  }
  return y;
}

// ------------------------------------------------------------------------------------------------ streamed rows
// Copied from src/common/gen.cpp:80-84 (powi): exponentiation by squaring, so the AR bridge equals gen's bits.
static double powi_gen(double x, int64_t d) { double r = 1.0, b = x; while (d > 0) { if (d & 1) r *= b; b *= b; d >>= 1; } return r; }

static double test_normal(uint32_t seed, uint8_t xph, uint32_t row, uint32_t col) {   // non-gen designs: Philox, role TEST
  Address a; a.seed = seed; a.role = R_TEST; a.xph = xph; a.stage = 7; a.particle = row; a.position = col;
  return normal_draw(a);
}

XSample make_rows(const Truth& T, const std::vector<int32_t>& cols_in, uint32_t row0, uint32_t nrows, uint32_t seed, bool with_y) {
  XSample xs;
  xs.cols = cols_in; xs.cols.insert(xs.cols.end(), T.S0.begin(), T.S0.end());
  std::sort(xs.cols.begin(), xs.cols.end()); xs.cols.erase(std::unique(xs.cols.begin(), xs.cols.end()), xs.cols.end());
  const size_t m = xs.cols.size();
  xs.m = nrows; xs.X.assign((size_t)nrows * m, 0.0);
  if (with_y) xs.y.assign(nrows, 0.0);
  const bool use_gen = !T.gen_spec.is_null();
  gen::Spec sp; if (use_gen) sp = gen::spec_from_json(T.gen_spec);
  if (use_gen) for (int32_t j : xs.cols) if (j < 1 || j > sp.p) throw Error(Status::invalid_input, "make_rows: column out of range");
  std::vector<int> ps(T.S0.size()); for (size_t k = 0; k < T.S0.size(); ++k) ps[k] = xs.pos(T.S0[k]);
  const std::string& d = T.design;
  const bool ar = d == "AR" || d == "ADJ-OPP";
  for (uint32_t r = 0; r < nrows; ++r) {
    const uint32_t i = row0 + r;
    double* row = &xs.X[(size_t)r * m];
    double prev = 0; int64_t jprev = -1;
    double fac = 0; if (!use_gen && d == "FAC") fac = test_normal(seed, X_TEST_FACTOR, i, 0);
    for (size_t c = 0; c < m; ++c) {
      const uint32_t j0 = (uint32_t)(xs.cols[c] - 1);
      double x;
      if (use_gen) {
        // src/common/gen.cpp generate_test (lines 128-147), copied: same addresses, same arithmetic
        if (sp.design == gen::Design::AR || sp.design == gen::Design::ADJOPP) {
          double e = gen::normal_at(sp.seed, X_TEST_X, i, j0);
          if (jprev < 0) x = e;
          else { double rd = powi_gen(sp.rho, (int64_t)j0 - jprev); x = rd * prev + pm::sqrt(1.0 - rd * rd) * e; }
          prev = x; jprev = j0;
        } else if (sp.design == gen::Design::BLK) {
          x = pm::sqrt(sp.rho) * gen::normal_at(sp.seed, X_TEST_FACTOR, i, j0 / (uint32_t)sp.b) +
              pm::sqrt(1.0 - sp.rho) * gen::normal_at(sp.seed, X_TEST_X, i, j0);
        } else {
          x = gen::normal_at(sp.seed, X_TEST_X, i, j0);
        }
      } else if (ar) {
        double e = test_normal(seed, X_TEST_X, i, j0);
        if (jprev < 0) x = e;
        else { double rd = powi_gen(T.rho, (int64_t)j0 - jprev); x = rd * prev + std::sqrt(1.0 - rd * rd) * e; }
        prev = x; jprev = j0;
      } else if (d == "BLK") {
        x = std::sqrt(T.rho) * test_normal(seed, X_TEST_FACTOR, i, j0 / (uint32_t)T.block) + std::sqrt(1.0 - T.rho) * test_normal(seed, X_TEST_X, i, j0);
      } else if (d == "FAC") {
        x = std::sqrt(T.rho) * fac + std::sqrt(1.0 - T.rho) * test_normal(seed, X_TEST_X, i, j0);
      } else {
        x = test_normal(seed, X_TEST_X, i, j0);
      }
      row[c] = x;
    }
    if (with_y) {
      double mu = use_gen ? 0.0 : T.alpha;
      for (size_t k = 0; k < T.S0.size(); ++k) mu += T.beta[k] * row[ps[k]];
      xs.y[r] = use_gen ? mu + sp.sigma * gen::normal_at(sp.seed, X_TEST_NOISE, i, 0)
                        : mu + std::sqrt(T.sigma2_eff()) * test_normal(seed, X_TEST_NOISE, i, 0);
    }
  }
  return xs;
}

// ------------------------------------------------------------------------------------------------ posterior draws
std::vector<double> cumulative_weights(const Law& L) {
  std::vector<double> c(L.comps.size());
  double s = 0; for (size_t i = 0; i < L.comps.size(); ++i) { s += L.comps[i].w; c[i] = s; }
  return c;
}

ParamDraw draw_params(const Law& L, const std::vector<double>& cum, uint32_t seed, uint32_t object_id, uint32_t draw) {
  Address a; a.seed = seed; a.role = R_POST; a.xph = X_POST; a.stage = object_id; a.particle = draw; a.slot = 0;
  ParamDraw d;
  // model ∝ π_𝒯 by binary search on the cumulative weights (one uniform, slot 0)
  const double u = unif_draw(a) * cum.back();
  d.comp = (int)std::min<size_t>(L.comps.size() - 1, (size_t)(std::upper_bound(cum.begin(), cum.end(), u) - cum.begin()));
  const Component& C = L.comps[d.comp];
  if (C.gaussian) { d.b = C.b; d.a = C.a; d.v = C.sigma2; return d; }
  const size_t k = C.orig.size();
  const double v = C.beta_n / gamma_draw(C.alpha_n, a);   // v | S ~ IG(α_n, β_n), standardised scale
  std::vector<double> xi(k), t(k);
  for (size_t i = 0; i < k; ++i) xi[i] = normal_draw(a);
  for (int i = (int)k - 1; i >= 0; --i) {                  // t = L^{-T} ξ, so Cov(t) = H⁻¹
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
// One component at one x: location, scale², and the hoisted log-density constants (D-17 item 6).
struct CompAt { double loc, scale2, lc, hnu, inv; bool gauss; double w; };
static double t_const(double nu) {   // lgamma((ν+1)/2) − lgamma(ν/2) − ½ log(νπ): the same for every conjugate model
  thread_local double last_nu = -1, last_c = 0;
  if (nu != last_nu) { last_nu = nu; last_c = std::lgamma(0.5 * (nu + 1)) - std::lgamma(0.5 * nu) - 0.5 * std::log(nu * M_PI); }
  return last_c;
}
static void comp_at(const Component& C, const XSample& xs, size_t row, double w, CompAt& o) {
  const size_t K = xs.cols.size();
  const double* x = &xs.X[row * K];
  const size_t k = C.orig.size();
  o.w = w;
  if (C.gaussian) {
    double s = C.a;
    for (size_t i = 0; i < k; ++i) { int p = xs.pos(C.orig[i]); if (p < 0) throw Error(Status::internal_error, "comp_at: column missing"); s += x[p] * C.b[i]; }
    o.loc = s; o.scale2 = C.sigma2; o.gauss = true;
    o.lc = -0.5 * std::log(2.0 * M_PI * C.sigma2); o.inv = 0.5 / C.sigma2; o.hnu = 0;
    return;
  }
  double xt[64], wv[64];
  std::vector<double> xtv, wvv;
  double* xtp = xt; double* wp = wv;
  if (k > 64) { xtv.resize(k); wvv.resize(k); xtp = xtv.data(); wp = wvv.data(); }
  double lin = 0;
  for (size_t i = 0; i < k; ++i) {
    int p = xs.pos(C.orig[i]); if (p < 0) throw Error(Status::internal_error, "comp_at: column missing");
    xtp[i] = (x[p] - C.xbar[i]) / C.xsd[i];
    lin += C.theta_bar[i] * xtp[i];
  }
  double q = 0;
  for (size_t i = 0; i < k; ++i) { double s = xtp[i]; for (size_t t = 0; t < i; ++t) s -= C.LH[i * k + t] * wp[t]; wp[i] = s / C.LH[i * k + i]; q += wp[i] * wp[i]; }
  const double nu = 2.0 * C.alpha_n;
  o.loc = C.ybar + C.sy * lin;
  o.scale2 = C.sy * C.sy * (C.beta_n / C.alpha_n) * (1.0 + C.n * q);
  o.gauss = false;
  o.lc = t_const(nu) - 0.5 * std::log(o.scale2);
  o.hnu = 0.5 * (nu + 1); o.inv = 1.0 / (nu * o.scale2);
}
static inline double log_comp(const CompAt& c, double y) {
  const double r = y - c.loc;
  return c.gauss ? c.lc - r * r * c.inv : c.lc - c.hnu * std::log1p(r * r * c.inv);
}
static double comp_var(const CompAt& c) { return c.gauss ? c.scale2 : c.scale2 * (2 * c.hnu - 1) / (2 * c.hnu - 3); }
static double mu_star(const Truth& T, const XSample& xs, size_t row) {
  const size_t K = xs.cols.size(); double mu = T.alpha;
  for (size_t i = 0; i < T.S0.size(); ++i) mu += xs.X[row * K + xs.pos(T.S0[i])] * T.beta[i];
  return mu;
}

// Density estimate at y from groups: exact part (weights w_c) + tail groups (each an equally weighted sample, scaled by
// τ). Returns log of: [0] pooled = exact + τ·mean_g(mean of group g), [1..G] exact + τ·(mean of group g), [G+1] exact/(1−τ).
struct MixAt {
  std::vector<CompAt> ex;                    // exact components (weights w)
  std::vector<std::vector<CompAt>> tail;     // tail groups (weights ignored: equal within a group)
  double tau = 0;
  void eval(double y, double* out) const {   // out: G + 2 log densities
    const size_t G = tail.size();
    double m = -INFINITY;
    thread_local std::vector<double> le, lt;
    le.resize(ex.size());
    for (size_t i = 0; i < ex.size(); ++i) { le[i] = log_comp(ex[i], y); m = std::max(m, le[i]); }
    size_t nt = 0; for (auto& g : tail) nt += g.size();
    lt.resize(nt);
    size_t q = 0;
    for (auto& g : tail) for (auto& c : g) { lt[q] = log_comp(c, y); m = std::max(m, lt[q]); ++q; }
    double se = 0; for (size_t i = 0; i < ex.size(); ++i) se += ex[i].w * std::exp(le[i] - m);
    double pooled_tail = 0; q = 0;
    for (size_t g = 0; g < G; ++g) {
      double sg = 0; for (size_t i = 0; i < tail[g].size(); ++i, ++q) sg += std::exp(lt[q] - m);
      sg /= (double)tail[g].size();
      out[1 + g] = m + std::log(se + tau * sg);
      pooled_tail += sg / G;
    }
    out[0] = m + std::log(se + tau * pooled_tail);
    out[G + 1] = m + std::log(se / (1.0 - tau));
  }
  void moments(double& m1, double& var) const {   // of the pooled estimate (importance centre for GH)
    double s1 = 0, s2 = 0, wsum = 0;
    for (auto& c : ex) { s1 += c.w * c.loc; s2 += c.w * (comp_var(c) + c.loc * c.loc); wsum += c.w; }
    for (auto& g : tail) for (auto& c : g) { const double w = tau / (g.size() * tail.size()); s1 += w * c.loc; s2 += w * (comp_var(c) + c.loc * c.loc); wsum += w; }
    m1 = s1 / wsum; var = std::max(s2 / wsum - m1 * m1, 1e-300);
  }
};

// affinity and KL for each of the G + 2 density versions at one row
static void row_integrals(const MixAt& M, const Truth& T, double ms, const std::vector<double>& ght, const std::vector<double>& ghw,
                          double* aff, double* kl, size_t nv) {
  const double s2 = T.sigma2_eff();
  double m1, vm; M.moments(m1, vm);
  const double prec = 0.5 * (1.0 / vm + 1.0 / s2), sc2 = 1.0 / prec, cen = sc2 * 0.5 * (m1 / vm + ms / s2), sc = std::sqrt(sc2);
  const double lfs_c = -0.5 * std::log(2.0 * M_PI * s2);
  std::vector<double> lf(nv);
  for (size_t v = 0; v < nv; ++v) { aff[v] = 0; kl[v] = 0; }
  for (size_t i = 0; i < ght.size(); ++i) {
    const double y = cen + M_SQRT2 * sc * ght[i];
    M.eval(y, lf.data());
    const double lfs = lfs_c - 0.5 * (y - ms) * (y - ms) / s2, base = std::log(ghw[i]) + ght[i] * ght[i];
    for (size_t v = 0; v < nv; ++v) aff[v] += std::exp(base + 0.5 * (lf[v] + lfs)) * M_SQRT2 * sc;
    const double y2 = ms + M_SQRT2 * std::sqrt(s2) * ght[i];
    M.eval(y2, lf.data());
    const double lfs2 = lfs_c - ght[i] * ght[i];
    for (size_t v = 0; v < nv; ++v) kl[v] += ghw[i] / std::sqrt(M_PI) * (lfs2 - lf[v]);
  }
}

void predictive_at_x(const Law& L, const Truth& T, const XSample& xs, size_t row, const std::vector<double>& ght,
                     const std::vector<double>& ghw, double* affinity, double* kl) {
  MixAt M; M.ex.resize(L.comps.size());
  for (size_t c = 0; c < L.comps.size(); ++c) comp_at(L.comps[c], xs, row, L.comps[c].w, M.ex[c]);
  double a[2], k[2];
  row_integrals(M, T, mu_star(T, xs, row), ght, ghw, a, k, 2);
  *affinity = a[0]; *kl = k[0];
}
double log_pred_density(const Law& L, const XSample& xs, size_t row, double y) {
  MixAt M; M.ex.resize(L.comps.size());
  for (size_t c = 0; c < L.comps.size(); ++c) comp_at(L.comps[c], xs, row, L.comps[c].w, M.ex[c]);
  double out[2]; M.eval(y, out); return out[0];
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
static double sd_over(const std::vector<double>& v) {
  if (v.size() < 2) return 0;
  double m = 0; for (double x : v) m += x; m /= v.size();
  double ss = 0; for (double x : v) ss += (x - m) * (x - m);
  return std::sqrt(ss / (v.size() - 1));
}

namespace {
// The split of a law into the exact top-K and the tail, and the per-block stratified tail samples.
struct Split {
  std::vector<int> top;            // component indices, weight-descending (ties: index)
  std::vector<int> tail;           // the rest, in component order
  std::vector<double> tail_cum;    // cumulative tail weights
  double tau = 0;
  bool exact = false;
  int G = 0, Rg = 0;
};
Split make_split(const Law& L, const DistOpts& o) {
  Split s;
  const size_t M = L.comps.size();
  std::vector<int> ord(M); std::iota(ord.begin(), ord.end(), 0);
  const size_t K = std::min<size_t>(M, (size_t)std::max(1, o.top_k));
  std::partial_sort(ord.begin(), ord.begin() + K, ord.end(), [&](int a, int b) {
    return L.comps[a].w > L.comps[b].w || (L.comps[a].w == L.comps[b].w && a < b); });
  if (M - K <= (size_t)o.tail_r) {   // tail small: everything exact
    s.top = ord; s.exact = true; return s;
  }
  s.top.assign(ord.begin(), ord.begin() + K);
  s.tail.assign(ord.begin() + K, ord.end());
  std::sort(s.tail.begin(), s.tail.end());
  s.tail_cum.resize(s.tail.size());
  long double c = 0; for (size_t i = 0; i < s.tail.size(); ++i) { c += L.comps[s.tail[i]].w; s.tail_cum[i] = (double)c; }
  s.tau = (double)c;
  s.G = std::max(2, o.tail_groups); s.Rg = std::max(1, o.tail_r / s.G);
  return s;
}
// Systematic (stratified) sample of Rg tail components ∝ weight for group g of block b (one uniform offset each).
std::vector<int> tail_sample(const Split& s, uint32_t seed, uint32_t oid, uint32_t stream, uint32_t block, int g) {
  Address a; a.seed = seed; a.role = R_POST; a.xph = X_POST; a.stage = 1000 + oid * 4 + stream; a.particle = block; a.position = (uint32_t)g;
  const double u0 = uniform_at(a);
  std::vector<int> out(s.Rg);
  const double tot = s.tail_cum.back();
  for (int r = 0; r < s.Rg; ++r) {
    const double u = (r + u0) / s.Rg * tot;
    size_t i = (size_t)(std::upper_bound(s.tail_cum.begin(), s.tail_cum.end(), u) - s.tail_cum.begin());
    out[r] = s.tail[std::min(i, s.tail.size() - 1)];
  }
  return out;
}
}  // namespace

Json dist_metrics(const Law& L, const Truth& T, int32_t n_obs, const DistOpts& o, uint32_t oid, std::vector<double>* dH_out,
                  std::vector<ParamDraw>* draws_out) {
  if (L.comps.empty()) throw Error(Status::internal_error, "dist_metrics: empty law");
  const size_t M = L.comps.size();
  const std::vector<double> cum = cumulative_weights(L);
  if (std::fabs(cum.back() - 1.0) > 1e-9) throw Error(Status::internal_error, "dist_metrics: weights do not sum to 1");
  const double s2 = T.sigma2_eff();
  Json J = Json::object();
  J["object"] = L.name;
  J["n_components"] = (uint64_t)M;
  J["dropped_mass"] = L.dropped_mass;

  // 1. plug-in at the law's posterior mean (b̄ over the union of supports, ā, v̄) — closed form, O(Σk log Σk)
  {
    std::vector<std::pair<int32_t, double>> e; e.reserve(M * 8);
    double am = 0, vm = 0;
    for (auto& c : L.comps) {
      std::vector<double> b = c.b_mean();
      for (size_t i = 0; i < c.orig.size(); ++i) e.emplace_back(c.orig[i], c.w * b[i]);
      am += c.w * c.a_mean(); vm += c.w * c.v_mean();
    }
    std::sort(e.begin(), e.end(), [](const auto& x, const auto& y) { return x.first < y.first; });
    std::vector<int32_t> bo; std::vector<double> bv;
    for (auto& x : e) { if (!bo.empty() && bo.back() == x.first) bv.back() += x.second; else { bo.push_back(x.first); bv.push_back(x.second); } }
    LinErr le = lin_error(T, bo, bv, am);
    const double h2p = h2_plugin(le, vm, s2);
    Json P = Json::object();
    P["h2"] = h2p; P["dH"] = std::sqrt(h2p); P["n_h2"] = n_obs * h2p;
    P["m"] = le.m; P["s2"] = le.s2; P["v"] = vm; P["pred_error"] = pred_error(le); P["support_union"] = (uint64_t)bo.size();
    J["plugin"] = P;
  }
  // 2. exact weighted closed forms over the whole law (D-17 item 2)
  {
    std::vector<double> h(M), pe(M);
#pragma omp parallel for schedule(static) num_threads(o.threads)
    for (long c = 0; c < (long)M; ++c) {
      const Component& C = L.comps[c];
      LinErr le = lin_error(T, C.orig, C.b_mean(), C.a_mean());
      h[c] = h2_plugin(le, C.v_mean(), s2); pe[c] = pred_error(le);
    }
    long double sh = 0, sp = 0, sh2 = 0;
    for (size_t c = 0; c < M; ++c) { sh += L.comps[c].w * h[c]; sp += L.comps[c].w * pe[c]; sh2 += L.comps[c].w * h[c] * h[c]; }
    Json W = Json::object();
    W["h2"] = (double)sh; W["n_h2"] = n_obs * (double)sh; W["pred_error"] = (double)sp;
    W["h2_sd"] = std::sqrt(std::max(0.0, (double)(sh2 - sh * sh)));
    J["weighted_plugin"] = W;
  }
  // 3. posterior law of d_H by conjugate draws (model by binary search; D-17 item 3)
  {
    std::vector<double> dh((size_t)o.n_draws);
    if (draws_out) draws_out->assign((size_t)o.n_draws, ParamDraw());
#pragma omp parallel for schedule(static) num_threads(o.threads)
    for (int i = 0; i < o.n_draws; ++i) {
      ParamDraw d = draw_params(L, cum, o.seed, oid, (uint32_t)i);
      const Component& C = L.comps[d.comp];
      dh[i] = std::sqrt(h2_plugin(lin_error(T, C.orig, d.b, d.a), d.v, s2));
      if (draws_out) (*draws_out)[i] = std::move(d);
    }
    std::vector<double> sd = dh; std::sort(sd.begin(), sd.end());
    Json D = Json::object();
    double dm = 0; for (double x : dh) dm += x; dm /= dh.size();
    D["n_draws"] = o.n_draws; D["mean"] = dm;
    D["q05"] = quantile_sorted(sd, 0.05); D["q25"] = quantile_sorted(sd, 0.25); D["q50"] = quantile_sorted(sd, 0.5);
    D["q75"] = quantile_sorted(sd, 0.75); D["q95"] = quantile_sorted(sd, 0.95);
    Json tail = Json::array();
    for (double c : o.eps_c) {
      const double eps2 = c * std::log((double)n_obs) / n_obs;
      size_t cnt = 0; for (double x : dh) if (x * x > eps2) ++cnt;
      Json t = Json::object(); t["c"] = c; t["eps2"] = eps2; t["prob"] = (double)cnt / dh.size();
      tail.push(t);
    }
    D["tail"] = tail;
    J["post_dH"] = D;
    if (dH_out) *dH_out = std::move(dh);
  }
  // 4-5. mixture predictive (top-K exact + stratified tail) on streamed row blocks
  const Split sp = make_split(L, o);
  const size_t G = sp.exact ? 0 : (size_t)sp.G, NV = G + 2;
  std::vector<double> ght, ghw; gauss_hermite(o.n_gh, ght, ghw);
  std::vector<int32_t> top_cols;
  for (int c : sp.top) top_cols.insert(top_cols.end(), L.comps[c].orig.begin(), L.comps[c].orig.end());
  std::sort(top_cols.begin(), top_cols.end()); top_cols.erase(std::unique(top_cols.begin(), top_cols.end()), top_cols.end());
  auto block_mix = [&](uint32_t stream, uint32_t blk, std::vector<std::vector<int>>& groups, std::vector<int32_t>& cols) {
    groups.assign(G, {});
    cols = top_cols;
    for (size_t g = 0; g < G; ++g) {
      groups[g] = tail_sample(sp, o.seed, oid, stream, blk, (int)g);
      for (int c : groups[g]) cols.insert(cols.end(), L.comps[c].orig.begin(), L.comps[c].orig.end());
    }
  };
  auto fill_mix = [&](MixAt& Mx, const XSample& xs, size_t r, const std::vector<std::vector<int>>& groups) {
    Mx.ex.resize(sp.top.size()); Mx.tau = sp.tau;
    for (size_t i = 0; i < sp.top.size(); ++i) comp_at(L.comps[sp.top[i]], xs, r, L.comps[sp.top[i]].w, Mx.ex[i]);
    Mx.tail.assign(G, {});
    for (size_t g = 0; g < G; ++g) { Mx.tail[g].resize(groups[g].size()); for (size_t i = 0; i < groups[g].size(); ++i) comp_at(L.comps[groups[g][i]], xs, r, 0, Mx.tail[g][i]); }
  };
  const uint32_t B = (uint32_t)std::max(1, o.block_rows);
  const bool gen_rows = !T.gen_spec.is_null();
  size_t max_cols = 0;
  // predictive integrals: rows 0 … n_x − 1
  std::vector<double> aff((size_t)o.n_x * NV), klv((size_t)o.n_x * NV);
  for (uint32_t r0 = 0, blk = 0; r0 < (uint32_t)o.n_x; r0 += B, ++blk) {
    const uint32_t nr = std::min<uint32_t>(B, (uint32_t)o.n_x - r0);
    std::vector<std::vector<int>> groups; std::vector<int32_t> cols;
    block_mix(0, blk, groups, cols);
    const XSample xs = make_rows(T, cols, r0, nr, o.seed, false);
    max_cols = std::max(max_cols, xs.cols.size());
#pragma omp parallel for schedule(static) num_threads(o.threads)
    for (long r = 0; r < (long)nr; ++r) {
      MixAt Mx; fill_mix(Mx, xs, (size_t)r, groups);
      row_integrals(Mx, T, mu_star(T, xs, (size_t)r), ght, ghw, &aff[(r0 + r) * NV], &klv[(r0 + r) * NV], NV);
    }
  }
  auto column = [&](const std::vector<double>& a, size_t v) { std::vector<double> c((size_t)o.n_x); for (int i = 0; i < o.n_x; ++i) c[i] = a[(size_t)i * NV + v]; return c; };
  Json Q = Json::object();
  {
    double am, ase, km, kse; mean_se(column(aff, 0), am, ase); mean_se(column(klv, 0), km, kse);
    std::vector<double> hg, kg;
    for (size_t g = 0; g < G; ++g) { double a, s_, k, s2_; mean_se(column(aff, 1 + g), a, s_); mean_se(column(klv, 1 + g), k, s2_); hg.push_back(1 - a); kg.push_back(k); }
    double aK, sK, kK, skK; mean_se(column(aff, NV - 1), aK, sK); mean_se(column(klv, NV - 1), kK, skK);
    Q["h2"] = 1.0 - am; Q["h2_se_x"] = ase; Q["h2_se_tail"] = G ? sd_over(hg) / std::sqrt((double)G) : 0.0;
    Q["n_h2"] = n_obs * (1.0 - am);
    Q["kl"] = km; Q["kl_se_x"] = kse; Q["kl_se_tail"] = G ? sd_over(kg) / std::sqrt((double)G) : 0.0;
    Q["exact"] = sp.exact; Q["top_k"] = (uint64_t)sp.top.size(); Q["tail_components"] = (uint64_t)sp.tail.size();
    Q["tail_r"] = (uint64_t)(G * (size_t)sp.Rg); Q["tail_groups"] = (uint64_t)G; Q["tail_mass"] = sp.tau;
    Q["h2_topK"] = 1.0 - aK; Q["dH_topK"] = std::sqrt(std::max(0.0, 1.0 - aK)); Q["dH_bound"] = std::sqrt(sp.tau);
    Q["kl_topK"] = kK;
    Q["n_x"] = o.n_x; Q["n_gh"] = o.n_gh; Q["block_rows"] = (uint64_t)B; Q["max_block_columns"] = (uint64_t)max_cols;
    Q["rows"] = gen_rows ? "gen_test" : "eval_philox";
  }
  J["predictive"] = Q;
  // test rows: rows n_x … n_x + n_test − 1 (gen) — MSE of the estimated predictive mean, mean log estimated density
  std::vector<double> se2((size_t)o.n_test), lpd((size_t)o.n_test);
  for (uint32_t r0 = 0, blk = 0; r0 < (uint32_t)o.n_test; r0 += B, ++blk) {
    const uint32_t nr = std::min<uint32_t>(B, (uint32_t)o.n_test - r0);
    std::vector<std::vector<int>> groups; std::vector<int32_t> cols;
    block_mix(1, blk, groups, cols);
    const XSample xs = make_rows(T, cols, (uint32_t)o.n_x + r0, nr, o.seed, true);
#pragma omp parallel for schedule(static) num_threads(o.threads)
    for (long r = 0; r < (long)nr; ++r) {
      MixAt Mx; fill_mix(Mx, xs, (size_t)r, groups);
      double m1, vm; Mx.moments(m1, vm);
      std::vector<double> lf(NV); Mx.eval(xs.y[r], lf.data());
      se2[r0 + r] = (xs.y[r] - m1) * (xs.y[r] - m1);
      lpd[r0 + r] = lf[0];
    }
  }
  double mm, mse_, lm, lse; mean_se(se2, mm, mse_); mean_se(lpd, lm, lse);
  Json Tt = Json::object();
  Tt["mse"] = mm; Tt["mse_se"] = mse_; Tt["mlpd"] = lm; Tt["mlpd_se"] = lse; Tt["n_test"] = o.n_test;
  J["test"] = Tt;
  return J;
}

}  // namespace v4::eval
