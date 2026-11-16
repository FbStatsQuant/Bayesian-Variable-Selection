// v4/eval.h -- WP5 evaluator: selection, PIP, evidence, distribution (W3-DIST) metrics, cost (ENGINEERING_SPEC §1 row 6;
// EXPERIMENT_PLAN §3; W3-DIST STATEMENT §0, §2). Namespace v4::eval. Entry point: eval::run (include/v4/stubs.h).
//
// Conventions (INTERFACES §2): models are sorted int32 arrays of INTERNAL 0-based column indices; original 1-based indices
// appear only at file/JSON boundaries (truth.json, records). The truth (β*, S₀, Σ) lives on ORIGINAL indices because
// the population law ν_x is defined on the raw columns.
//
// The working model on the standardised scale (core/cpp/v3_score.h:36-75, 196-212; STATEMENT §0):
//   ys = Xs_S θ + ε, ε ~ N(0, v I);  θ | v ~ N(0, n v A⁻¹), A = G_S + I;  v ~ IG(a0, b0).
//   Posterior: v | S ~ IG(α_n, β_n), α_n = a0 + n/2, β_n = b0 + Q/2;  θ | v, S ~ N(θ̄, n v H⁻¹),
//   H = (n+1) G_S + I, θ̄ = n H⁻¹ z_S, Q = yᵀy − n z_SᵀH⁻¹z_S.
// Response scale (STATEMENT §0 "density attached to a posterior draw"): b_j = s_y θ_j / ŝ_j, â = ȳ − x̄ᵀb, v_resp = s_y² v,
// with ȳ = y_max·y_mean, s_y = y_max·y_sd_scaled, x̄_j = col_max·col_mean, ŝ_j = col_max·col_sd (v3_preprocess.R:24-51).
#pragma once
#include <cstdint>
#include <string>
#include <vector>

#include "v4/data.h"
#include "v4/json.h"
#include "v4/model.h"
#include "v4/rng.h"
#include "v4/status.h"

namespace v4::eval {

// ------------------------------------------------------------------------------------------------ small helpers
inline const Json* jfind(const Json& j, const std::string& k) { return j.contains(k) ? &j.at(k) : nullptr; }
inline double jnum_or(const Json& j, const std::string& k, double d) { const Json* p = jfind(j, k); return (p && p->type() == Json::NUM) ? p->num() : d; }
inline std::string jstr_or(const Json& j, const std::string& k, const std::string& d) { const Json* p = jfind(j, k); return (p && p->type() == Json::STR) ? p->str() : d; }

// response map of Data (INTERFACES §2; prep writes col_* and y_* as v3_standardise returns them)
inline double ybar(const Data& D) { return D.y_max * D.y_mean; }
inline double sy(const Data& D) { return D.y_max * D.y_sd_scaled; }
inline double xbar(const Data& D, int32_t j) { return D.col_max[j] * D.col_mean[j]; }
inline double xsd(const Data& D, int32_t j) { return D.col_max[j] * D.col_sd[j]; }
int32_t internal_of(const Data& D, int32_t orig1);   // −1 if the original column was dropped (orig is increasing)
// Data from raw (X n×p column-major, y) through WP1's prep (drop constant columns, v3_standardise) — tests, competitors.
Data data_from_raw(const double* X, const double* y, int32_t n, int32_t p);

// ------------------------------------------------------------------------------------------------ conjugate posterior
struct ModelPost {
  Model S;                          // internal, sorted
  int route = 0; bool q_recomputed = false;
  double logm = 0, F = 0, Q = 0, logdetH = 0, logdetA = 0;
  double alpha_n = 0, beta_n = 0;
  std::vector<double> theta_bar;    // k, standardised scale
  std::vector<double> LH;           // k×k row-major lower factor with L Lᵀ = H (from the route BitScorer used)
};
// logm, Q, route, log dets: v4::BitScorer (bits of core/cpp/v3_score.h). θ̄ and the factor of H: recomputed on the same
// route with the copied helpers of score.h. F = logprior[k] + logm. Throws NumericalFailure after the last fallback.
ModelPost model_post(const Data& D, const Model& S);

// ------------------------------------------------------------------------------------------------ truth and design law
struct Truth {
  std::string design = "IND";        // IND | AR | ADJ-OPP | BLK | FAC (FAC/MIS only through `params`, not gen)
  double rho = 0.0;
  int32_t block = 20;
  std::vector<int32_t> S0;           // original 1-based, sorted
  std::vector<double> beta;          // β*_{S0}, aligned with S0
  double alpha = 0.0, sigma = 1.0;
  double extra_noise_var = 0.0;      // MIS arm: variance of the omitted independent variable's contribution
  uint64_t seed = 0;                 // data seed
  Json gen_spec;                     // WP1 gen spec (truth.json "spec"), null if absent: test rows then come from draw_x
  double sigma2_eff() const { return sigma * sigma + extra_noise_var; }
};
Truth truth_from_json(const Json& j);
double design_cov(const Truth& T, int32_t j, int32_t l);   // Cov(x_j, x_l) under ν_x, original 1-based indices
std::vector<double> design_cov_matrix(const Truth& T, const std::vector<int32_t>& cols);

// ------------------------------------------------------------------------------------------------ predictive laws
struct Component {
  double w = 1.0;
  std::vector<int32_t> orig;         // 1-based original columns (sorted), aligned with xbar/xsd/theta_bar/b
  std::vector<double> xbar, xsd;
  double ybar = 0, sy = 1;
  bool gaussian = false;             // false: conjugate Student-t component; true: point predictive N(a + xᵀb, sigma2)
  int32_t n = 0; double alpha_n = 0, beta_n = 0;
  std::vector<double> theta_bar, LH;
  double F = 0;
  std::vector<double> b; double a = 0, sigma2 = 0;
  std::vector<double> b_mean() const;
  double a_mean() const;
  double v_mean() const;
};
struct Law {
  std::string name;
  std::vector<Component> comps;
  double dropped_mass = 0;
};
Component component_from_post(const Data& D, const ModelPost& mp, double w);
Component component_gaussian(const std::vector<int32_t>& orig, const std::vector<double>& b, double a, double sigma2, double w = 1.0);

// ------------------------------------------------------------------------------------------------ closed forms (plan §3.3)
double h2_normals(double m1, double v1, double m2, double v2);
struct LinErr { double m = 0, s2 = 0; };
LinErr lin_error(const Truth& T, const std::vector<int32_t>& orig, const std::vector<double>& b, double a);
// d_H² = 1 − sqrt(2 sqrt(v σ²)/(v + σ²)) (1 + 2 a s²)^{−1/2} exp(−a m²/(1 + 2 a s²)), a = 1/(4(v + σ²))  (README_WP5.md)
double h2_plugin(const LinErr& e, double v, double sigma2);
inline double pred_error(const LinErr& e) { return e.m * e.m + e.s2; }

// ------------------------------------------------------------------------------------------------ Monte Carlo pieces
void gauss_hermite(int n, std::vector<double>& t, std::vector<double>& w);
struct XSample {
  std::vector<int32_t> cols;   // sorted original columns
  std::vector<double> X;       // m × |cols| row-major
  size_t m = 0;
  int pos(int32_t orig1) const;
};
// Gaussian rows from ν_x restricted to cols (Cholesky of design_cov; Philox role TEST, xph TEST_X, stage).
XSample draw_x(const Truth& T, const std::vector<int32_t>& cols, size_t m, uint32_t seed, uint32_t stage);
std::vector<double> draw_y(const Truth& T, const XSample& xs, uint32_t seed, uint32_t stage);

struct DistOpts {
  uint32_t seed = 1;           // posterior draws (role POST)
  int n_draws = 10000, n_x = 4000, n_gh = 64, n_test = 10000;
  int threads = 1;
  std::vector<double> eps_c = {0.5, 1, 2, 4, 8};
};
struct DistShared {
  XSample xq;                              // n_x rows for the predictive integrals
  XSample xt; std::vector<double> yt;      // n_test test rows
  std::string source;                      // "gen_test" (WP1 gen, same definition as the data) or "draw_x"
};
// Rows from WP1's gen::generate_test when truth.json carries a gen spec (n_x + n_test rows, split in that order),
// otherwise from draw_x/draw_y with the eval seed.
DistShared make_shared_draws(const Truth& T, const std::vector<int32_t>& cols, const DistOpts& o);

Json dist_metrics(const Law& L, const Truth& T, int32_t n_obs, const DistOpts& o, const DistShared& sh, uint32_t object_id,
                  std::vector<double>* dH_draws = nullptr);
void predictive_at_x(const Law& L, const Truth& T, const XSample& xs, size_t row, const std::vector<double>& ght,
                     const std::vector<double>& ghw, double* affinity, double* kl);
double log_pred_density(const Law& L, const XSample& xs, size_t row, double y);

struct ParamDraw { int comp = 0; std::vector<double> b; double a = 0, v = 0; };
ParamDraw draw_params(const Law& L, uint32_t seed, uint32_t object_id, uint32_t draw);
double gamma_draw(double shape, Address& a);   // Marsaglia–Tsang; consumes slots from a.slot upward
double normal_draw(Address& a);                // Box–Muller on (u, u2) of one address; slot++

// ------------------------------------------------------------------------------------------------ selection / PIP / evidence
struct StoreView {                // a flat store (INTERFACES §4.1), sorted in HPM order; pool holds internal indices
  size_t size = 0;
  const double* v = nullptr; const uint64_t* off = nullptr; const uint16_t* len = nullptr;
  const uint64_t* hash = nullptr; const int32_t* pool = nullptr;
  Model model(size_t i) const { return Model(pool + off[i], pool + off[i] + len[i]); }
};
struct StoreMass { double vmax = 0, logZ_T = 0; size_t n_kept = 0; double dropped_mass = 0; };
StoreMass store_mass(const StoreView& s, double rel_cut);
long store_find(const StoreView& s, const Model& S, uint64_t h);

Json selection_metrics(const Model& S0, const Model& hpm, double F_hpm, const Model& mpm, double F_S0, const Data& D);
Json pip_metrics(const std::vector<double>& pip, const Model& S0, int32_t p);
Json pip_island_spread(const double* pip_r, int32_t Rp, int32_t p, double sd_target);
Json evidence_metrics(double logZ, const std::vector<double>& logZ_r, double logZ_T);
double logZ_occ(const double* F_sorted, size_t M, uint64_t occ, uint64_t total);

// ------------------------------------------------------------------------------------------------ the command
// args: fit (fit.bin) | competitor (competitor json), data (data.bin), truth (truth.json), out (eval.bin; the record is
// <out>.json, written by main), optional law, cost, seed, threads, n_draws, n_x, n_gh, n_test, rel_cut.
Json run(const Json& args);
// Competitor record (tools/competitors; schema smcbvs4.competitor/1) evaluated by the same metrics.
Json run_competitor(const Json& args);

}  // namespace v4::eval
