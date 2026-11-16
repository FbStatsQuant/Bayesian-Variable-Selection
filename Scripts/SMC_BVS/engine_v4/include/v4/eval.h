// v4/eval.h -- WP5 evaluator: selection, PIP, evidence, distribution (W3-DIST) metrics, cost (ENGINEERING_SPEC §1 row 6;
// EXPERIMENT_PLAN §3; W3-DIST STATEMENT §0, §2). Namespace v4::eval.
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
// with ȳ = y_max·y_mean, s_y = y_max·y_sd_scaled, x̄_j = col_max·col_mean, ŝ_j = col_max·col_sd (v3_preprocess.R:35-51).
#pragma once
#include <cstdint>
#include <string>
#include <vector>

#include "v4/wp5prov/json.h"
#include "v4/wp5prov/prov.h"

namespace v4::eval {

using wp5prov::Json;
using Model = std::vector<int32_t>;

// ------------------------------------------------------------------------------------------------ data
// The subset of v4::Data (INTERFACES §2) that eval/post read. Arrays are non-owning (mmap views of data.bin, or OwnedData).
struct EvalData {
  int32_t n = 0, p = 0, p_raw = 0, K = 0;
  const double* Xs = nullptr;        // n×p column-major, standardised
  const double* ys = nullptr;        // n
  const double* z = nullptr;         // p (may be null: then computed per model, sequential in i)
  const double* col_max = nullptr;
  const double* col_mean = nullptr;
  const double* col_sd = nullptr;
  const int32_t* orig = nullptr;     // p, 1-based original column of internal j
  double yty = 0, a0 = 0.01, b0 = 0.01, nu = 0, logCn = 0, logm0 = 0, logWK = 0;
  std::vector<double> logprior;      // k = 0..K
  double y_max = 1, y_mean = 0, y_sd_scaled = 1;
  const double* col(int32_t j) const { return Xs + (size_t)j * (size_t)n; }
  double ybar() const { return y_max * y_mean; }
  double sy() const { return y_max * y_sd_scaled; }
  double xbar(int32_t j) const { return col_max[j] * col_mean[j]; }
  double xsd(int32_t j) const { return col_max[j] * col_sd[j]; }
  int32_t internal_of(int32_t orig1) const;   // −1 if the original column was dropped (binary search; orig is increasing)
};
// Fills nu, logCn, logm0, logprior, logWK from (n, p, K, yty, a0, b0): copy of core/cpp/v3_score.h:57-75.
void data_constants(EvalData& D);

// Owning container for tests, competitors and the provisional prep path.
struct OwnedData {
  std::vector<double> Xs, ys, z, col_max, col_mean, col_sd;
  std::vector<int32_t> orig;
  EvalData D;
  void bind();   // points D's arrays at the vectors
};
// Standardise raw X (n×p column-major) and y as v3_standardise (core/v3_preprocess.R:35-51, main branch; class A here,
// prep's bits are WP1's). Columns with zero sample variance are dropped (kept map in orig).
OwnedData standardise(const double* X, const double* y, int32_t n, int32_t p);

// ------------------------------------------------------------------------------------------------ scorer + posterior
struct ModelPost {
  Model S;                          // internal, sorted
  int route = 0; bool q_recomputed = false;
  double logm = 0, F = 0, Q = 0, logdetH = 0, logdetA = 0;
  double alpha_n = 0, beta_n = 0;
  std::vector<double> theta_bar;    // k, standardised scale
  std::vector<double> LH;           // k×k row-major lower Cholesky factor of H (route CHOL/REFACTOR) or of MᵀM (QR)
};
// Bit form of the v3 scorer on the Gram-free path (INTERFACES §2, §6): Gram entries sequential in i, Cholesky route,
// QR fallback; F = logprior[k] + logm. Throws NumericalFailure after the last fallback.
ModelPost model_post(const EvalData& D, const Model& S);
inline double score_F(const EvalData& D, const Model& S) { return model_post(D, S).F; }

// ------------------------------------------------------------------------------------------------ truth and design law
struct Truth {
  std::string design = "IND";        // IND | AR | ADJ | ADJ-OPP | BLK | FAC (case-insensitive)
  double rho = 0.0;                  // AR / FAC / BLK correlation
  int32_t block = 20;                // BLK block size
  std::vector<int32_t> S0;           // original 1-based, sorted
  std::vector<double> beta;          // β*_{S0}, aligned with S0
  double alpha = 0.0, sigma = 1.0;   // α*, σ*
  double extra_noise_var = 0.0;      // MIS arm: variance of the omitted independent variable's contribution
  uint64_t seed = 0;                 // data seed (eval draws use a derived seed)
  double sigma2_eff() const { return sigma * sigma + extra_noise_var; }
};
Truth truth_from_json(const Json& j);           // truth.json (INTERFACES §5.1: design, params, seed, S₀ 1-based, β*, σ*)
double design_cov(const Truth& T, int32_t j, int32_t l);   // Cov(x_j, x_l) under ν_x, original 1-based indices
std::vector<double> design_cov_matrix(const Truth& T, const std::vector<int32_t>& cols);   // row-major |cols|²

// ------------------------------------------------------------------------------------------------ predictive laws
// One mixture component of an output object, on the response scale.
struct Component {
  double w = 1.0;
  std::vector<int32_t> orig;         // 1-based original columns (sorted), aligned with xbar/xsd/theta_bar/b
  std::vector<double> xbar, xsd;
  double ybar = 0, sy = 1;
  bool gaussian = false;             // false: conjugate Student-t component; true: point predictive N(a + xᵀb, sigma2)
  // conjugate component (standardised-scale parameters)
  int32_t n = 0; double alpha_n = 0, beta_n = 0;
  std::vector<double> theta_bar, LH;
  double F = 0;                      // log score of the model (for records)
  // gaussian component (response-scale)
  std::vector<double> b; double a = 0, sigma2 = 0;
  // posterior-mean plug-in on the response scale
  std::vector<double> b_mean() const;
  double a_mean() const;
  double v_mean() const;             // E[v_resp]
};
struct Law {
  std::string name;
  std::vector<Component> comps;
  double dropped_mass = 0;           // store BMA: relative mass dropped by the truncation
};
Component component_from_post(const EvalData& D, const ModelPost& mp, double w);
Component component_gaussian(const std::vector<int32_t>& orig, const std::vector<double>& b, double a, double sigma2, double w = 1.0);

// ------------------------------------------------------------------------------------------------ closed forms (plan §3.3)
// H²(N(m1, v1), N(m2, v2)) = 1 − sqrt(2 sqrt(v1 v2)/(v1 + v2)) exp(−(m1 − m2)²/(4(v1 + v2))), affinity form.
double h2_normals(double m1, double v1, double m2, double v2);
// Linear predictor a + xᵀb on original columns; its error Δ(x) against the truth is N(m, s²) under Gaussian ν_x (mean 0).
struct LinErr { double m = 0, s2 = 0; };
LinErr lin_error(const Truth& T, const std::vector<int32_t>& orig, const std::vector<double>& b, double a);
// Plug-in Hellinger, closed form (plan §3.3 item 1; derivation in tests/wp5/README_T7.md):
//   d_H² = 1 − sqrt(2 sqrt(v σ²)/(v + σ²)) (1 + 2 a s²)^{−1/2} exp(−a m²/(1 + 2 a s²)),  a = 1/(4(v + σ²)).
double h2_plugin(const LinErr& e, double v, double sigma2);
// E_x (â + xᵀb − α* − xᵀβ*)² = m² + s² (plan §3.3 item 4).
inline double pred_error(const LinErr& e) { return e.m * e.m + e.s2; }

// ------------------------------------------------------------------------------------------------ Monte Carlo pieces
// Gauss–Hermite rule with weight e^{−t²} (Golub–Welsch free; Newton on the Hermite recurrence, as NR §4.6).
void gauss_hermite(int n, std::vector<double>& t, std::vector<double>& w);

// x rows from ν_x restricted to `cols` (original, sorted), Gaussian with covariance design_cov, Philox normals.
struct XSample {
  std::vector<int32_t> cols;   // sorted original columns
  std::vector<double> X;       // m × |cols| row-major
  size_t m = 0;
  int pos(int32_t orig1) const;   // column position, −1 if absent
};
XSample draw_x(const Truth& T, const std::vector<int32_t>& cols, size_t m, uint32_t seed, uint32_t stage);
// y for test rows: α* + xᵀβ* + N(0, σ²_eff), Philox role TEST, xph TEST_NOISE.
std::vector<double> draw_y(const Truth& T, const XSample& xs, uint32_t seed, uint32_t stage);

struct DistOpts {
  uint32_t seed = 1;           // eval seed (Philox key; role POST / TEST)
  int n_draws = 10000;         // posterior law of d_H
  int n_x = 4000;              // x draws for the predictive Hellinger / KL
  int n_gh = 64;               // Gauss–Hermite nodes in y
  int n_test = 10000;          // fresh test rows
  int threads = 1;
  std::vector<double> eps_c = {0.5, 1, 2, 4, 8};   // ε² = c log n / n
};
struct DistShared {            // draws shared by all objects (common random numbers make the oracle ratios sharper)
  XSample xq;                  // n_x rows for the predictive integrals
  XSample xt; std::vector<double> yt;   // n_test test rows
};
DistShared make_shared_draws(const Truth& T, const std::vector<int32_t>& cols, const DistOpts& o);

// Per-object distribution metrics (plan §3.3 items 1-4). Returns a JSON object; `dH_draws` gets the 10⁴ draws of d_H.
Json dist_metrics(const Law& L, const Truth& T, int32_t n_obs, const DistOpts& o, const DistShared& sh, uint32_t object_id,
                  std::vector<double>* dH_draws = nullptr);
// Predictive Hellinger affinity and KL at one x (exposed for tests): ∫ sqrt(f̄ f*) dy and ∫ f* log(f*/f̄) dy.
void predictive_at_x(const Law& L, const Truth& T, const XSample& xs, size_t row, const std::vector<double>& ght,
                     const std::vector<double>& ghw, double* affinity, double* kl);
double log_pred_density(const Law& L, const XSample& xs, size_t row, double y);
double pred_mean(const Law& L, const XSample& xs, size_t row);

// One posterior draw (b, a, v_resp) from a law (exposed for tests).
struct ParamDraw { int comp = 0; std::vector<double> b; double a = 0, v = 0; };
ParamDraw draw_params(const Law& L, uint32_t seed, uint32_t object_id, uint32_t draw);
double gamma_draw(double shape, wp5prov::Address& a);   // Marsaglia–Tsang; consumes slots from a.slot upward
double normal_draw(wp5prov::Address& a);                // Box–Muller on (u, u2) of one address; slot++

// ------------------------------------------------------------------------------------------------ selection / PIP / evidence
struct StoreView {                // a flat store (INTERFACES §4.1), sorted in HPM order; pool holds internal indices
  size_t size = 0;
  const double* v = nullptr; const uint64_t* off = nullptr; const uint16_t* len = nullptr;
  const uint64_t* hash = nullptr; const int32_t* pool = nullptr;
  Model model(size_t i) const { return Model(pool + off[i], pool + off[i] + len[i]); }
};
struct StoreMass { double vmax = 0, logZ_T = 0; size_t n_kept = 0; double dropped_mass = 0; };
StoreMass store_mass(const StoreView& s, double rel_cut);          // log Σ e^F over the whole store; truncation count
long store_find(const StoreView& s, const Model& S, uint64_t h);   // index or −1
uint64_t zobrist_hash(const Model& S, int32_t p);                  // INTERFACES §2 (core/cpp/v3_util.h:99-108)

Json selection_metrics(const Model& S0, const Model& hpm, double F_hpm, const Model& mpm, double F_S0,
                       const EvalData& D);
Json pip_metrics(const std::vector<double>& pip, const Model& S0, int32_t p);
Json pip_island_spread(const double* pip_r, int32_t Rp, int32_t p, double sd_target);
Json evidence_metrics(double logZ, const std::vector<double>& logZ_r, double logZ_T);
// log Ẑ_occ = log Σ_{top-M} e^F − log(occupancy of the top-M models among the terminal particles / N_total) (D-13).
double logZ_occ(const double* F_sorted, size_t M, uint64_t occ, uint64_t total);

// ------------------------------------------------------------------------------------------------ the command
// eval::run: --fit fit.bin --data data.bin --truth truth.json --out eval  [--law law.bin] [--cost cost.json]
//            [--islands dir] [--seed s] [--threads k] [--n-draws ..] [--n-x ..] [--n-test ..]
// Writes <out>.json (record + status) and <out>.bin (kind 9). Exit code 0 or 10 + status (INTERFACES §7).
int run(int argc, char** argv);

}  // namespace v4::eval
