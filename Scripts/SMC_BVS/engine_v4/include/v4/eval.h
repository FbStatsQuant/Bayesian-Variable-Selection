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
#include <cstdio>
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
// INTERFACES §5.1 (v0.1.2): u64 values are hex strings "0x…" in JSON; plain numbers are accepted too
inline uint64_t ju64_or(const Json& j, const std::string& k, uint64_t d) {
  const Json* p = jfind(j, k);
  if (!p) return d;
  if (p->type() == Json::STR) { const std::string& s = p->str(); return std::stoull(s, nullptr, (s.rfind("0x", 0) == 0 || s.rfind("0X", 0) == 0) ? 16 : 10); }
  if (p->type() == Json::NUM) return (uint64_t)p->num();
  return d;
}
inline std::string hex_u64(uint64_t v) { char b[24]; std::snprintf(b, sizeof b, "0x%llx", (unsigned long long)v); return b; }
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
// x rows (and y for test rows) restricted to a sorted column set.
struct XSample {
  std::vector<int32_t> cols;   // sorted original columns
  std::vector<double> X;       // m × |cols| row-major
  std::vector<double> y;       // m (test rows) or empty
  size_t m = 0;
  int pos(int32_t orig1) const;
};
// Small-case Gaussian rows by Cholesky of design_cov (tests, T7c). Philox role TEST, xph TEST_X, stage.
XSample draw_x(const Truth& T, const std::vector<int32_t>& cols, size_t m, uint32_t seed, uint32_t stage);
std::vector<double> draw_y(const Truth& T, const XSample& xs, uint32_t seed, uint32_t stage);
// Rows row0 … row0 + nrows − 1 of a row-addressable stream, only the columns `cols` (∪ S0), O(|cols|) per row (D-17 item 5).
//   gen designs (truth.json has a gen spec): exactly gen::generate_test's definition (src/common/gen.cpp, copied below
//   with gen::normal_at), rows 0 … n_x − 1 for the predictive integrals and n_x … for the test rows;
//   otherwise (FAC, MIS, intercept): the same Markov / factor constructions with Philox normals (role TEST, eval seed).
XSample make_rows(const Truth& T, const std::vector<int32_t>& cols, uint32_t row0, uint32_t nrows, uint32_t seed, bool with_y);
// dᵀΣd for d on sorted original columns, O(|cols|) for IND / AR / ADJ-OPP / BLK / FAC (no |cols|² matrix).
double quad_form(const Truth& T, const std::vector<int32_t>& cols, const std::vector<double>& d);

struct DistOpts {
  uint32_t seed = 1;           // posterior draws and tail samples (role POST); non-gen rows (role TEST)
  int n_draws = 10000, n_x = 4000, n_gh = 64, n_test = 10000;
  int threads = 1;
  int top_k = 1000;            // exact components of the mixture predictive (D-17 item 4)
  int tail_r = 1000;           // stratified tail importance sample per row block, in tail_groups independent groups
  int tail_groups = 4;
  int block_rows = 500;        // rows per block; the tail sample is refreshed per block
  std::vector<double> eps_c = {0.5, 1, 2, 4, 8};
};

// Per-object distribution metrics (plan §3.3 items 1-4; D-17). Fields:
//   plugin            closed form at the law's posterior mean (b̄, ā, v̄) (plan item 1), and its prediction error;
//   weighted_plugin   exact E_π[d_H²(f_{S,θ̄_S,v̄_S}, f*)] and E_π[prediction error] over the whole law (O(M));
//   post_dH           the posterior law of d_H from n_draws conjugate draws (model by binary search on cumulative weights);
//   predictive        mixture predictive d_H² and KL: exact top-K + stratified tail sample (unbiased density at each node),
//                     x-MC SE, tail-MC SE (from tail_groups independent groups), tail mass τ, the top-K-only value and
//                     the bound |d_H(f̄, f*) − d_H(f̄_K, f*)| ≤ √τ; exact when the tail has ≤ tail_r components;
//   test              MSE of the predictive mean and mean log predictive density on n_test rows (same estimator).
Json dist_metrics(const Law& L, const Truth& T, int32_t n_obs, const DistOpts& o, uint32_t object_id,
                  std::vector<double>* dH_draws = nullptr, std::vector<struct ParamDraw>* draws_out = nullptr);
// The exact full mixture at one row (tests): ∫ sqrt(f̄ f*) dy and ∫ f* log(f*/f̄) dy.
void predictive_at_x(const Law& L, const Truth& T, const XSample& xs, size_t row, const std::vector<double>& ght,
                     const std::vector<double>& ghw, double* affinity, double* kl);
double log_pred_density(const Law& L, const XSample& xs, size_t row, double y);

struct ParamDraw { int comp = 0; std::vector<double> b; double a = 0, v = 0; };
std::vector<double> cumulative_weights(const Law& L);   // prefix sums in component order (last = Σ w)
ParamDraw draw_params(const Law& L, const std::vector<double>& cum, uint32_t seed, uint32_t object_id, uint32_t draw);
inline ParamDraw draw_params(const Law& L, uint32_t seed, uint32_t object_id, uint32_t draw) { return draw_params(L, cumulative_weights(L), seed, object_id, draw); }
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
