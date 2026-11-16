// v4/post.h -- WP5 `post`: the store-BMA law Π̂^𝒯 of W3-DIST STATEMENT §2 as a file (`law.bin`, kind 7; D-8).
//
// law.bin sections (INTERFACES §5.1 container; names fixed from v0.1 on):
//   meta        json  {schema "smcbvs4.law/1", n, p, M, rel_cut, vmax, logZ_T, dropped_mass, n_store, ybar, sy, a0, b0,
//                      max_abs_dF, inputs{fit.bin, data.bin}, draws{n, seed} | null}
//   model_ptr   i64   M+1        model m = model_idx[model_ptr[m] .. model_ptr[m+1])  (internal 0-based, sorted)
//   model_idx   i32
//   F           f64   M          log ϖ(|S|) + log m(S) as stored in the fit's top store (HPM order kept)
//   w           f64   M          e^{F − vmax} normalised over the kept models (Σ w = 1)
//   logm, Q, alpha_n, beta_n  f64 M;  route u8 M
//   theta_bar   f64   Σk         posterior mean on the standardised scale, aligned with model_idx
//   LH_ptr      i64   M+1        packed lower-triangular Cholesky factor of H = (n+1)G_S + I, row-major, k(k+1)/2 each
//   LH          f64
//   cols        i32   C          union of the kept models (internal, sorted)
//   cols_orig   i32   C          1-based original columns
//   cols_xbar   f64   C          x̄_j (response map, v3_preprocess.R:35-51)
//   cols_xsd    f64   C          ŝ_j
//   optional draws (post --draws N; Philox role POST, never streams 0…9 + R′):
//   draw_model  i32 N;  draw_a f64 N;  draw_v f64 N;  draw_b f64 N×C (row-major over cols, zeros off the model)
#pragma once
#include <string>
#include <vector>

#include "v4/eval.h"

namespace v4::post {

struct LawFile {
  int32_t n = 0, p = 0;
  double rel_cut = 1e-12, vmax = 0, logZ_T = 0, dropped_mass = 0, max_abs_dF = 0;
  uint64_t n_store = 0;
  double ybar = 0, sy = 1, a0 = 0.01, b0 = 0.01;
  std::vector<eval::ModelPost> models;   // F field = the store's value
  std::vector<double> w;
  std::vector<int32_t> cols, cols_orig;
  std::vector<double> cols_xbar, cols_xsd;
  Json meta_extra = Json::object();
};

// Kept = store entries with F ≥ vmax + log(rel_cut) (at most max_models); conjugate parameters recomputed from Xs.
// max_abs_dF = max |F_store − F_recomputed| (class A engines differ at ≈ 1e-9 relative; recorded, not asserted).
LawFile build_law(const Data& D, const eval::StoreView& s, double rel_cut = 1e-12, size_t max_models = 1000000);
std::string write_law(const LawFile& L, const std::string& path, int n_draws = 0, uint32_t draw_seed = 0);
LawFile read_law(const std::string& path, std::string* content_hash = nullptr);
eval::Law to_eval_law(const LawFile& L, const std::string& name = "T");

// post::run: --fit fit.bin --data data.bin --out law.bin [--rel_cut 1e-12] [--max_models M] [--draws N --seed s]
// (include/v4/stubs.h signature; main writes the record <out>.json)
Json run(const Json& args);

}  // namespace v4::post
