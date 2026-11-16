// model.cpp -- truth / design law (ν_x of EXPERIMENT_PLAN §2.2 and WP1 gen) and predictive components.
#include <algorithm>
#include <cctype>
#include <cmath>

#include "v4/eval.h"

namespace v4::eval {

static std::string upper(std::string s) { for (auto& c : s) c = (char)std::toupper((unsigned char)c); return s; }

Truth truth_from_json(const Json& j) {
  // WP1 gen (src/common/gen.cpp truth_json): {generator, spec{design, n, p, seed, rho, b, a, s0, sigma}, S0, beta, sigma}.
  // Also accepted: design / params at the top level (competitor fixtures; FAC and MIS arms, which gen does not make).
  Truth T;
  const Json* sp = jfind(j, "spec");
  const Json& top = sp ? *sp : j;
  if (sp) T.gen_spec = *sp;
  T.design = upper(jstr_or(top, "design", jstr_or(j, "design", "IND")));
  if (T.design == "ADJOPP") T.design = "ADJ-OPP";
  const Json* P = jfind(j, "params");
  const Json& prm = P ? *P : top;
  const double rdef = (T.design == "AR" || T.design == "ADJ-OPP") ? 0.6 : (T.design == "BLK" ? 0.5 : (T.design == "FAC" ? 0.3 : 0.0));
  T.rho = jnum_or(prm, "rho", jnum_or(top, "rho", rdef));
  T.block = (int32_t)jnum_or(prm, "block", jnum_or(top, "b", 20));
  T.alpha = jnum_or(prm, "alpha", jnum_or(j, "alpha", 0.0));
  T.extra_noise_var = jnum_or(prm, "extra_noise_var", 0.0);
  if (const Json* mb = jfind(prm, "mis_beta")) if (mb->type() == Json::NUM) T.extra_noise_var += mb->num() * mb->num();
  if (T.extra_noise_var != 0 || T.alpha != 0 || T.design == "FAC") T.gen_spec = Json();   // not a gen design: draw_x rows
  T.seed = (uint64_t)jnum_or(top, "seed", jnum_or(j, "seed", 0));
  T.sigma = jnum_or(j, "sigma", jnum_or(top, "sigma", 1.0));
  const Json& s0 = j.at("S0");
  const Json& bt = j.at("beta");
  if (s0.size() != bt.size()) throw Error(Status::invalid_input, "truth.json: S0 and beta lengths differ");
  std::vector<std::pair<int32_t, double>> sb;
  for (size_t i = 0; i < s0.size(); ++i) sb.emplace_back((int32_t)s0.at(i).i64(), bt.at(i).num());
  std::sort(sb.begin(), sb.end());
  for (size_t i = 0; i < sb.size(); ++i) {
    if (sb[i].first < 1 || (i && sb[i].first == sb[i - 1].first)) throw Error(Status::invalid_input, "truth.json: bad S0");
    T.S0.push_back(sb[i].first); T.beta.push_back(sb[i].second);
  }
  if (!(T.sigma > 0)) throw Error(Status::invalid_input, "truth.json: sigma must be > 0");
  return T;
}

// ν_x (unit variances): IND; AR / ADJ-OPP Toeplitz ρ^{|j−l|} (the stationary AR(1) recursion of gen.h); BLK blocks of
// `block` consecutive columns, within-block correlation ρ (gen.h: √ρ f + √(1−ρ) e); FAC compound symmetry ρ.
double design_cov(const Truth& T, int32_t j, int32_t l) {
  if (j == l) return 1.0;
  const std::string& d = T.design;
  if (d == "IND") return 0.0;
  if (d == "AR" || d == "ADJ-OPP") return std::pow(T.rho, (double)std::abs(j - l));
  if (d == "BLK") return ((j - 1) / T.block == (l - 1) / T.block) ? T.rho : 0.0;
  if (d == "FAC") return T.rho;
  throw Error(Status::invalid_input, "unknown design " + d);
}
std::vector<double> design_cov_matrix(const Truth& T, const std::vector<int32_t>& c) {
  const size_t k = c.size();
  std::vector<double> S(k * k);
  for (size_t a = 0; a < k; ++a) for (size_t b = 0; b < k; ++b) S[a * k + b] = design_cov(T, c[a], c[b]);
  return S;
}

Component component_from_post(const Data& D, const ModelPost& mp, double w) {
  if (!D.col_max) throw Error(Status::invalid_input, "component_from_post: Data has no column statistics");
  Component c; c.w = w; c.gaussian = false; c.n = D.n;
  c.alpha_n = mp.alpha_n; c.beta_n = mp.beta_n; c.theta_bar = mp.theta_bar; c.LH = mp.LH; c.F = mp.F;
  c.ybar = ybar(D); c.sy = sy(D);
  for (int32_t j : mp.S) { c.orig.push_back(D.orig[j]); c.xbar.push_back(xbar(D, j)); c.xsd.push_back(xsd(D, j)); }
  return c;
}
Component component_gaussian(const std::vector<int32_t>& orig, const std::vector<double>& b, double a, double sigma2, double w) {
  Component c; c.w = w; c.gaussian = true; c.orig = orig; c.b = b; c.a = a; c.sigma2 = sigma2;
  if (b.size() != orig.size()) throw Error(Status::invalid_input, "component_gaussian: sizes differ");
  for (size_t i = 1; i < orig.size(); ++i) if (!(orig[i - 1] < orig[i])) throw Error(Status::invalid_input, "component_gaussian: orig not sorted");
  if (!(sigma2 > 0)) throw Error(Status::invalid_input, "component_gaussian: sigma2 must be > 0");
  return c;
}
std::vector<double> Component::b_mean() const {
  if (gaussian) return b;
  std::vector<double> r(orig.size());
  for (size_t i = 0; i < orig.size(); ++i) r[i] = sy * theta_bar[i] / xsd[i];
  return r;
}
double Component::a_mean() const {
  if (gaussian) return a;
  std::vector<double> bm = b_mean();
  double s = ybar;
  for (size_t i = 0; i < orig.size(); ++i) s -= xbar[i] * bm[i];
  return s;
}
double Component::v_mean() const {
  if (gaussian) return sigma2;
  return sy * sy * beta_n / (alpha_n - 1.0);   // E[v] of IG(α_n, β_n), response scale
}

}  // namespace v4::eval
