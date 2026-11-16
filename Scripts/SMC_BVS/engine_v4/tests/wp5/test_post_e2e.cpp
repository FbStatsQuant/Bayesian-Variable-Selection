// test_post_e2e.cpp -- end to end on WP1's real pipeline: `gen` (raw.bin, truth.json) → `prep` (data.bin) → a fit.bin
// built by exact enumeration at p = 12 (standing in for an engine fit) → `post` (law.bin) and `eval` (record, eval.bin);
// competitor path; failure paths (corrupt input, incomplete fit, wrong kind, missing arguments).
#include <unistd.h>

#include <algorithm>
#include <cstdio>
#include <fstream>
#include <random>

#include "v4/eval.h"
#include "v4/format.h"
#include "v4/gen.h"
#include "v4/post.h"
#include "v4/prep.h"
#include "wp5_tk.h"

using namespace v4;
using namespace v4::eval;

namespace {

std::string tdir() {
  static std::string d;
  if (d.empty()) { d = std::string(std::getenv("TMPDIR") ? std::getenv("TMPDIR") : ".") + "/wp5_e2e_" + std::to_string(getpid()); std::string c = "mkdir -p " + d; if (std::system(c.c_str())) {} }
  return d;
}

struct Synthetic { Data D; std::string dir; std::vector<Model> models; std::vector<double> F; double logZ; std::vector<double> pip; int p = 0; };

void enumerate(const Data& D, Synthetic& s) {
  s.p = D.p;
  for (uint32_t code = 0; code < (1u << D.p); ++code) {
    Model S; for (int j = 0; j < D.p; ++j) if (code >> j & 1) S.push_back(j);
    if ((int)S.size() > D.K) continue;
    s.models.push_back(S); s.F.push_back(model_post(D, S).F);
  }
  double mx = *std::max_element(s.F.begin(), s.F.end()); long double z = 0;
  for (double f : s.F) z += std::exp((long double)(f - mx));
  s.logZ = mx + (double)std::log(z);
  s.pip.assign(D.p, 0.0);
  for (size_t m = 0; m < s.models.size(); ++m) for (int32_t j : s.models[m]) s.pip[j] += std::exp(s.F[m] - s.logZ);
}

// gen (AR, n = 100, p = 12, s0 = 3, amplitude amp) → prep → load; then enumerate every model.
Synthetic make_synthetic(uint32_t seed, double amp, const std::string& tag) {
  Synthetic s; s.dir = tdir() + "/" + tag; std::string c = "mkdir -p " + s.dir; if (std::system(c.c_str())) {}
  Json spec = Json::object(); spec["design"] = "AR"; spec["n"] = 100; spec["p"] = 12; spec["seed"] = (int64_t)seed; spec["s0"] = 3; spec["a"] = amp;
  Json ga = Json::object(); ga["spec"] = spec; ga["out"] = s.dir + "/raw.bin"; ga["truth"] = s.dir + "/truth.json";
  gen::run(ga);
  Json pa = Json::object(); pa["in"] = s.dir + "/raw.bin"; pa["out"] = s.dir + "/data.bin";
  prep::run(pa);
  s.D = prep::load_data(s.dir + "/data.bin");
  enumerate(s.D, s);
  return s;
}

// fit.bin: the top store = 40p + 1 best models (HPM order), exact PIPs as pip_eq/pip_Z, store-renormalised pip_T,
// 16 "islands" with noise around the exact values. status overridable for the GUARD-W test.
void write_fit_bin(const Synthetic& s, const std::string& path, const std::string& status, uint64_t seed) {
  const int p = s.p, R = 16;
  std::vector<size_t> ord(s.models.size()); for (size_t i = 0; i < ord.size(); ++i) ord[i] = i;
  std::sort(ord.begin(), ord.end(), [&](size_t a, size_t b) {   // hpm_better (core/cpp/v3_util.h:121-126)
    if (s.F[a] != s.F[b]) return s.F[a] > s.F[b];
    if (s.models[a].size() != s.models[b].size()) return s.models[a].size() < s.models[b].size();
    return std::lexicographical_compare(s.models[a].begin(), s.models[a].end(), s.models[b].begin(), s.models[b].end());
  });
  const size_t cap = std::min(ord.size(), (size_t)(40 * p + 1));
  std::vector<double> v; std::vector<uint64_t> off, hash; std::vector<uint16_t> len; std::vector<int32_t> pool;
  std::vector<double> pipT(p, 0.0); long double zt = 0;
  for (size_t i = 0; i < cap; ++i) {
    const Model& S = s.models[ord[i]];
    v.push_back(s.F[ord[i]]); off.push_back(pool.size()); len.push_back((uint16_t)S.size()); hash.push_back(s.D.zob.hash(S));
    pool.insert(pool.end(), S.begin(), S.end());
    zt += std::exp((long double)(s.F[ord[i]] - s.F[ord[0]]));
  }
  for (size_t i = 0; i < cap; ++i) for (int32_t j : s.models[ord[i]]) pipT[j] += (double)(std::exp((long double)(s.F[ord[i]] - s.F[ord[0]])) / zt);
  std::mt19937_64 g(seed); std::normal_distribution<double> N(0, 1);
  std::vector<double> lr(R), pr((size_t)R * p);
  for (int r = 0; r < R; ++r) { lr[r] = s.logZ + 0.3 * N(g); for (int j = 0; j < p; ++j) pr[(size_t)r * p + j] = std::clamp(s.pip[j] + 0.003 * N(g), 0.0, 1.0); }
  std::vector<double> pe(p, 0.0); for (int r = 0; r < R; ++r) for (int j = 0; j < p; ++j) pe[j] += pr[(size_t)r * p + j] / R;
  fmt::Writer W(fmt::K_FIT, fmt::M_V);
  W.add("top_v", v); W.add("top_off", off); W.add("top_len", len);
  W.add("top_hash", hash); W.add("top_pool", pool);
  W.add("hpm_S", s.models[ord[0]]);
  W.add("logZ_r", lr);
  W.add("pip_eq", pe); W.add("pip_Z", s.pip); W.add("pip_T", pipT);
  W.add("pip_r", pr.data(), pr.size(), (uint64_t)R, (uint64_t)p);
  std::vector<uint64_t> occ(1000, 0); const uint64_t tot = 16 * 2500;   // occupancy ∝ exact posterior mass
  for (size_t i = 0; i < std::min<size_t>(1000, cap); ++i) occ[i] = (uint64_t)std::llround(tot * std::exp(s.F[ord[i]] - s.logZ));
  W.add("occ_top", occ);
  double mx = *std::max_element(lr.begin(), lr.end()); double sw = 0; for (double x : lr) sw += std::exp(x - mx);
  Json m = Json::object();
  m["status"] = (status); m["logZ"] = (mx + std::log(sw / R)); m["hpm_F"] = (s.F[ord[0]]); m["Rp"] = (R); m["occ_total"] = (tot);
  m["hpm_phase"] = ("measured"); m["local_certified"] = (true);
  Json tm = Json::object(); tm["islands_s"] = (12.5); m["timings"] = (tm);
  W.add_json("meta", m);
  W.write(path);
}

Json args(std::initializer_list<std::pair<const char*, Json>> kv) { Json a = Json::object(); for (auto& x : kv) a[x.first] = x.second; return a; }
Status status_of(const std::function<void()>& f) { try { f(); } catch (const Error& e) { return e.st; } return Status::completed; }

}  // namespace

TEST(wp5_e2e_post_and_eval) {
  Synthetic s = make_synthetic(4242, 1.0, "strong");
  const std::string d = s.dir;
  write_fit_bin(s, d + "/fit.bin", "completed", 5);
  // post
  Json pj = post::run(args({{"fit", d + "/fit.bin"}, {"data", d + "/data.bin"}, {"out", d + "/law.bin"}, {"draws", 500}, {"seed", 3}}));
  CHECK(pj.at("status").str() == "completed");
  CHECK(pj.at("max_abs_dF").num() == 0.0);   // model_post reproduces the stored F in bits
  std::string lh;
  post::LawFile L = post::read_law(d + "/law.bin", &lh);
  CHECK(lh == pj.at("outputs").at("law.bin").str());
  CHECK(L.models.size() == (size_t)pj.at("M").num() && L.models.size() > 10);
  double ws = 0; for (double w : L.w) ws += w; CHECK_NEAR(ws, 1.0, 1e-12);
  { fmt::Reader B(d + "/law.bin"); CHECK(B.has("draw_b") && B.entry("draw_b").dims[0] == 500); }
  ModelPost mp = model_post(s.D, L.models[3].S);
  CHECK(mp.theta_bar == L.models[3].theta_bar && mp.beta_n == L.models[3].beta_n);
  // eval (built-in law) and eval (with law.bin) must agree on Π̂^𝒯
  auto ea = [&](const std::string& out, bool with_law) {
    Json a = args({{"fit", d + "/fit.bin"}, {"data", d + "/data.bin"}, {"truth", d + "/truth.json"}, {"out", d + "/" + out},
                   {"n_draws", 2000}, {"n_x", 400}, {"n_test", 2000}, {"threads", 2}});
    if (with_law) a["law"] = d + "/law.bin";
    return eval::run(a);
  };
  Json e1 = ea("eval1.bin", false), e2 = ea("eval2.bin", true);
  CHECK(e1.at("status").str() == "completed");
  CHECK(e1.at("dist").at("T").dump() == e2.at("dist").at("T").dump());
  CHECK(e1.at("params").at("test_rows").str() == "gen_test");   // WP1 gen test rows (same definition as the data)
  const Json& sel = e1.at("selection");
  CHECK(sel.at("hpm_eq_S0").boolean() && sel.at("outcome_class").str() == "correct");
  CHECK(sel.at("S0_in_store").boolean() && sel.at("F_S0_ledger_abs_diff").num() == 0.0);
  // HPM = S0 → Π̂^H = oracle: every ratio is exactly 1
  CHECK(e1.at("dist").at("ratio_to_oracle").at("H").at("plugin_h2").num() == 1.0);
  CHECK(e1.at("dist").at("ratio_to_oracle").at("H").at("predictive_h2").num() == 1.0);
  const Json& st = e1.at("store");
  CHECK(st.at("pi_T_hat").num() > 0.5 && st.at("size").num() == 40 * 12 + 1);
  // log Ẑ_occ with exact occupancies recovers the exact log Z (rounding of the counts only)
  CHECK_NEAR(e1.at("evidence").at("logZ_occ").at("M10").num(), s.logZ, 2e-3);
  CHECK(e1.at("evidence").at("R_eff").num() > 1 && e1.at("evidence").at("R_eff").num() <= 16);
  CHECK(e1.at("pip").at("island_spread").at("Rp").num() == 16);
  CHECK(e1.at("pip").at("eq_T_target_met").boolean());
  CHECK(e1.at("pip").at("eq").at("min_true").num() > 0.9);
  CHECK(e1.at("params").at("seed").num() == 4242);
  fmt::Reader EB(d + "/eval1.bin");
  CHECK(EB.kind() == fmt::K_EVAL && EB.entry("dH_draws_T").length == 2000 * 8);
  CHECK(EB.content_hash() == e1.at("outputs").at("eval1.bin").str());
  std::printf("    e2e: law M=%d, pi_T_hat=%.4f, d_H^2 plug-in H=%.4g T=%.4g oracle=%.4g, predictive T=%.4g, eval wall %.2f s\n",
              (int)L.models.size(), st.at("pi_T_hat").num(), e1.at("dist").at("H").at("plugin").at("h2").num(),
              e1.at("dist").at("T").at("plugin").at("h2").num(), e1.at("dist").at("oracle").at("plugin").at("h2").num(),
              e1.at("dist").at("T").at("predictive").at("h2").num(), e1.at("cost").at("eval_wall_s").num());
  // competitor path: a Gaussian point predictive (OLS-like on S0) and a model law
  {
    std::ofstream f(d + "/comp.json");
    f << "{\"schema\": \"smcbvs4.competitor/1\", \"method\": \"test_gauss\", \"status\": \"completed\", \"wall_s\": 0.1,"
         " \"selected\": [1, 3, 6], \"pip\": {\"default\": 0, \"idx\": [1, 3, 6, 9], \"val\": [1, 0.99, 0.97, 0.2]},"
         " \"predictive\": {\"type\": \"gaussian\", \"intercept\": 0.0, \"idx\": [1, 3, 6], \"coef\": [1.0, -0.8, 0.9], \"sigma2\": 1.0}}\n";
  }
  Json ec = eval::run(args({{"competitor", d + "/comp.json"}, {"data", d + "/data.bin"}, {"truth", d + "/truth.json"},
                            {"n_draws", 500}, {"n_x", 200}, {"n_test", 1000}}));
  CHECK(ec.at("selection").at("hpm_eq_S0").boolean());
  // the true parameters as a point predictive: plug-in d_H² = 0 exactly
  CHECK(ec.at("dist").at("C").at("plugin").at("h2").num() == 0.0);
  CHECK(ec.at("pip").at("C").at("n_null_gt_0.1").num() == 1);
  {
    std::ofstream f(d + "/comp2.json");
    f << "{\"schema\": \"smcbvs4.competitor/1\", \"method\": \"test_law\", \"status\": \"completed\", \"selected\": [1, 3, 6],"
         " \"predictive\": {\"type\": \"model_law\", \"models\": [[1, 3, 6], [1, 3, 6, 9]], \"weights\": [3, 1]}}\n";
  }
  Json ec2 = eval::run(args({{"competitor", d + "/comp2.json"}, {"data", d + "/data.bin"}, {"truth", d + "/truth.json"},
                             {"n_draws", 500}, {"n_x", 200}, {"n_test", 1000}}));
  CHECK(ec2.at("dist").at("C").at("n_components").num() == 2);
}

TEST(wp5_e2e_failure_paths) {
  Synthetic s = make_synthetic(32, 0.5, "weak");
  const std::string d = s.dir;
  auto base = [&](const std::string& fit, const std::string& out) {
    return args({{"fit", fit}, {"data", d + "/data.bin"}, {"truth", d + "/truth.json"}, {"out", d + "/" + out}, {"n_draws", 200}, {"n_x", 100}, {"n_test", 200}});
  };
  // incomplete fit: GUARD-W, no metrics, eval itself completed
  write_fit_bin(s, d + "/fit_inc.bin", "resource_limit", 6);
  Json ji = eval::run(base(d + "/fit_inc.bin", "ev_inc.bin"));
  CHECK(ji.at("fit_status").str() == "resource_limit" && !ji.contains("selection") && !ji.contains("dist"));
  // corrupt fit.bin: invalid_input
  write_fit_bin(s, d + "/fit_bad.bin", "completed", 7);
  { fmt::Reader B(d + "/fit_bad.bin"); uint64_t off = B.entry("pip_eq").offset;
    std::fstream f(d + "/fit_bad.bin", std::ios::in | std::ios::out | std::ios::binary); f.seekp((std::streamoff)off); char c = 1; f.write(&c, 1); }
  CHECK(status_of([&] { eval::run(base(d + "/fit_bad.bin", "ev_bad.bin")); }) == Status::invalid_input);
  // wrong kind (data.bin passed as fit)
  CHECK(status_of([&] { eval::run(base(d + "/data.bin", "ev_kind.bin")); }) == Status::invalid_input);
  // missing arguments
  CHECK(status_of([&] { eval::run(args({{"out", d + "/x.bin"}})); }) == Status::invalid_input);
  CHECK(status_of([&] { post::run(args({{"out", d + "/x.bin"}})); }) == Status::invalid_input);
  // a competitor that failed is recorded, without metrics
  { std::ofstream f(d + "/cfail.json"); f << "{\"schema\": \"smcbvs4.competitor/1\", \"method\": \"susie\", \"status\": \"package_missing\", \"reason\": \"susieR not installed\"}\n"; }
  Json cf = eval::run(args({{"competitor", d + "/cfail.json"}, {"data", d + "/data.bin"}, {"truth", d + "/truth.json"}}));
  CHECK(cf.at("competitor_status").str() == "package_missing" && !cf.contains("dist"));
}
