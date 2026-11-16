// model.cpp -- standardisation (provisional prep path), truth/design law, predictive components.
#include <algorithm>
#include <cctype>
#include <cmath>

#include "v4/eval.h"

namespace v4::eval {

void OwnedData::bind() {
  D.Xs = Xs.data(); D.ys = ys.data(); D.z = z.empty() ? nullptr : z.data();
  D.col_max = col_max.data(); D.col_mean = col_mean.data(); D.col_sd = col_sd.data(); D.orig = orig.data();
}

// v3_standardise main branch (core/v3_preprocess.R:35-51): x1 = x / max|x|; mu = mean(x1); s = sd(x1 − mu); z = (x1 − mu)/s.
// R's mean() is a two-pass long-double mean; here: long-double sum then one correction pass (class A; prep bits are WP1's).
static bool std_one(const double* x, int n, double* out, double& mx, double& mu, double& s) {
  mx = 0; for (int i = 0; i < n; ++i) mx = std::max(mx, std::fabs(x[i]));
  if (!(mx > 0)) return false;
  long double acc = 0; for (int i = 0; i < n; ++i) acc += (long double)(x[i] / mx);
  long double m = acc / n, c = 0; for (int i = 0; i < n; ++i) c += (long double)(x[i] / mx) - m;
  mu = (double)(m + c / n);
  double ss = 0; for (int i = 0; i < n; ++i) { double d = x[i] / mx - mu; ss += d * d; }
  s = std::sqrt(ss / (n - 1));
  if (!(s > 1e-12)) return false;
  for (int i = 0; i < n; ++i) out[i] = (x[i] / mx - mu) / s;
  return true;
}

OwnedData standardise(const double* X, const double* y, int32_t n, int32_t p) {
  OwnedData O;
  O.ys.resize(n);
  double ymx, ymu, ysd;
  if (!std_one(y, n, O.ys.data(), ymx, ymu, ysd)) throw Error(Status::invalid_input, "standardise: constant response");
  std::vector<double> col(n);
  for (int32_t j = 0; j < p; ++j) {
    double mx, mu, s;
    if (!std_one(X + (size_t)j * n, n, col.data(), mx, mu, s)) continue;   // dropped column
    O.Xs.insert(O.Xs.end(), col.begin(), col.end());
    O.col_max.push_back(mx); O.col_mean.push_back(mu); O.col_sd.push_back(s); O.orig.push_back(j + 1);
  }
  const int32_t pk = (int32_t)O.orig.size();
  O.z.resize(pk);
  for (int32_t j = 0; j < pk; ++j) { double s = 0; const double* xj = &O.Xs[(size_t)j * n]; for (int i = 0; i < n; ++i) s += xj[i] * O.ys[i]; O.z[j] = s; }
  O.D.n = n; O.D.p = pk; O.D.p_raw = p;
  double yty = 0; for (int i = 0; i < n; ++i) yty += O.ys[i] * O.ys[i];
  O.D.yty = yty; O.D.y_max = ymx; O.D.y_mean = ymu; O.D.y_sd_scaled = ysd;
  data_constants(O.D);
  O.bind();
  return O;
}

// ---------------------------------------------------------------------------------------------------- truth
static std::string upper(std::string s) { for (auto& c : s) c = (char)std::toupper((unsigned char)c); return s; }

Truth truth_from_json(const Json& j) {
  Truth T;
  T.design = upper(j.str_or("design", "IND"));
  const Json* P = j.find("params");
  const Json& prm = P ? *P : j;
  T.rho = prm.num_or("rho", T.design == "AR" || T.design == "ADJ" || T.design == "ADJ-OPP" ? 0.6 : (T.design == "BLK" ? 0.5 : (T.design == "FAC" ? 0.3 : 0.0)));
  T.block = (int32_t)prm.num_or("block", 20);
  T.alpha = prm.num_or("alpha", j.num_or("alpha", 0.0));
  T.extra_noise_var = prm.num_or("extra_noise_var", 0.0);
  if (const Json* mb = prm.find("mis_beta")) if (mb->is_num()) T.extra_noise_var += mb->num() * mb->num();   // MIS: omitted N(0,1) variable
  T.sigma = j.num_or("sigma", j.num_or("sigma_star", 1.0));
  T.seed = (uint64_t)j.num_or("seed", 0);
  const Json& s0 = j.has("S0") ? j.at("S0") : j.at("S0_orig");
  const Json& bt = j.has("beta") ? j.at("beta") : j.at("beta_star");
  if (s0.size() != bt.size()) throw Error(Status::invalid_input, "truth.json: S0 and beta lengths differ");
  std::vector<std::pair<int32_t, double>> sb;
  for (size_t i = 0; i < s0.size(); ++i) sb.emplace_back((int32_t)s0[i].num(), bt[i].num());
  std::sort(sb.begin(), sb.end());
  for (size_t i = 0; i < sb.size(); ++i) {
    if (sb[i].first < 1 || (i && sb[i].first == sb[i - 1].first)) throw Error(Status::invalid_input, "truth.json: bad S0");
    T.S0.push_back(sb[i].first); T.beta.push_back(sb[i].second);
  }
  if (!(T.sigma > 0)) throw Error(Status::invalid_input, "truth.json: sigma must be > 0");
  return T;
}

// ν_x of EXPERIMENT_PLAN §2.2 (unit variances): IND; AR/ADJ/ADJ-OPP Toeplitz ρ^{|j−l|}; BLK blocks of `block` consecutive
// columns with within-block correlation ρ; FAC one factor, compound symmetry ρ.
double design_cov(const Truth& T, int32_t j, int32_t l) {
  if (j == l) return 1.0;
  const std::string& d = T.design;
  if (d == "IND") return 0.0;
  if (d == "AR" || d == "ADJ" || d == "ADJ-OPP") return std::pow(T.rho, (double)std::abs(j - l));
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

// ---------------------------------------------------------------------------------------------------- components
Component component_from_post(const EvalData& D, const ModelPost& mp, double w) {
  Component c; c.w = w; c.gaussian = false; c.n = D.n;
  c.alpha_n = mp.alpha_n; c.beta_n = mp.beta_n; c.theta_bar = mp.theta_bar; c.LH = mp.LH; c.F = mp.F;
  c.ybar = D.ybar(); c.sy = D.sy();
  for (int32_t j : mp.S) { c.orig.push_back(D.orig[j]); c.xbar.push_back(D.xbar(j)); c.xsd.push_back(D.xsd(j)); }
  return c;
}
Component component_gaussian(const std::vector<int32_t>& orig, const std::vector<double>& b, double a, double sigma2, double w) {
  Component c; c.w = w; c.gaussian = true; c.orig = orig; c.b = b; c.a = a; c.sigma2 = sigma2;
  if (b.size() != orig.size()) throw Error(Status::invalid_input, "component_gaussian: sizes differ");
  for (size_t i = 1; i < orig.size(); ++i) if (!(orig[i - 1] < orig[i])) throw Error(Status::invalid_input, "component_gaussian: orig not sorted");
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
