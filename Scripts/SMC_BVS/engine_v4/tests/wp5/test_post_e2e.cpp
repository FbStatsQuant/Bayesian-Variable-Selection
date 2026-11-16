// test_post_e2e.cpp -- end to end: synthetic data.bin + fit.bin (exact enumeration at p = 12 standing in for an engine fit)
// + truth.json → `post` (law.bin) and `eval` (eval.json/eval.bin); failure paths (corrupt input, incomplete fit).
#include <unistd.h>

#include <algorithm>
#include <cstdio>
#include <fstream>
#include <random>

#include "v4/eval.h"
#include "v4/post.h"
#include "wp5_tk.h"

using namespace v4::eval;
using v4::wp5prov::BinWriter;

namespace {

std::string tdir() {
  static std::string d;
  if (d.empty()) { d = std::string(std::getenv("TMPDIR") ? std::getenv("TMPDIR") : ".") + "/wp5_e2e_" + std::to_string(getpid()); std::string c = "mkdir -p " + d; if (std::system(c.c_str())) {} }
  return d;
}

struct Synthetic { OwnedData O; std::vector<Model> models; std::vector<double> F; double logZ; std::vector<double> pip; int p = 0; };

void enumerate(const EvalData& D, Synthetic& s) {
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

Synthetic make_synthetic(uint64_t seed, double amp) {
  const int n = 100, p = 12;
  std::mt19937_64 g(seed); std::normal_distribution<double> N(0, 1);
  std::vector<double> X((size_t)n * p), y(n);
  for (int i = 0; i < n; ++i) {
    double prev = N(g);
    for (int j = 0; j < p; ++j) { double x = j ? 0.6 * prev + 0.8 * N(g) : prev; X[(size_t)j * n + i] = x; prev = x; }
    y[i] = amp * (1.0 * X[(size_t)1 * n + i] - 0.8 * X[(size_t)5 * n + i] + 0.9 * X[(size_t)9 * n + i]) + N(g);
  }
  Synthetic s{standardise(X.data(), y.data(), n, p), {}, {}, 0, {}, 0};
  enumerate(s.O.D, s);
  return s;
}

void write_data_bin(const OwnedData& O, const std::string& path) {
  const EvalData& D = O.D;
  BinWriter W(v4::wp5prov::K_DATA, v4::wp5prov::M_V);
  W.add("Xs_cm", v4::wp5prov::DT_F64, O.Xs.data(), O.Xs.size() * 8, 2, (uint64_t)D.p, (uint64_t)D.n);
  W.add_vec("ys", v4::wp5prov::DT_F64, O.ys); W.add_vec("z", v4::wp5prov::DT_F64, O.z);
  W.add_vec("col_max", v4::wp5prov::DT_F64, O.col_max); W.add_vec("col_mean", v4::wp5prov::DT_F64, O.col_mean); W.add_vec("col_sd", v4::wp5prov::DT_F64, O.col_sd);
  W.add_vec("kept", v4::wp5prov::DT_I32, O.orig);
  W.add_vec("logprior", v4::wp5prov::DT_F64, D.logprior);
  Json m = Json::object();
  m.set("n", D.n); m.set("p_raw", D.p_raw); m.set("p", D.p); m.set("K", D.K); m.set("yty", D.yty); m.set("logCn", D.logCn);
  m.set("logm0", D.logm0); m.set("logWK", D.logWK); m.set("y_max", D.y_max); m.set("y_mean", D.y_mean); m.set("y_sd_scaled", D.y_sd_scaled);
  m.set("prep_class", "A");
  W.add_json("meta", m.dump());
  W.write(path);
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
    v.push_back(s.F[ord[i]]); off.push_back(pool.size()); len.push_back((uint16_t)S.size()); hash.push_back(zobrist_hash(S, p));
    pool.insert(pool.end(), S.begin(), S.end());
    zt += std::exp((long double)(s.F[ord[i]] - s.F[ord[0]]));
  }
  for (size_t i = 0; i < cap; ++i) for (int32_t j : s.models[ord[i]]) pipT[j] += (double)(std::exp((long double)(s.F[ord[i]] - s.F[ord[0]])) / zt);
  std::mt19937_64 g(seed); std::normal_distribution<double> N(0, 1);
  std::vector<double> lr(R), pr((size_t)R * p);
  for (int r = 0; r < R; ++r) { lr[r] = s.logZ + 0.3 * N(g); for (int j = 0; j < p; ++j) pr[(size_t)r * p + j] = std::clamp(s.pip[j] + 0.003 * N(g), 0.0, 1.0); }
  std::vector<double> pe(p, 0.0); for (int r = 0; r < R; ++r) for (int j = 0; j < p; ++j) pe[j] += pr[(size_t)r * p + j] / R;
  BinWriter W(v4::wp5prov::K_FIT, v4::wp5prov::M_V);
  W.add_vec("top_v", v4::wp5prov::DT_F64, v); W.add_vec("top_off", v4::wp5prov::DT_U64, off); W.add_vec("top_len", v4::wp5prov::DT_U16, len);
  W.add_vec("top_hash", v4::wp5prov::DT_U64, hash); W.add_vec("top_pool", v4::wp5prov::DT_I32, pool);
  W.add_vec("hpm_S", v4::wp5prov::DT_I32, s.models[ord[0]]);
  W.add_vec("logZ_r", v4::wp5prov::DT_F64, lr);
  W.add_vec("pip_eq", v4::wp5prov::DT_F64, pe); W.add_vec("pip_Z", v4::wp5prov::DT_F64, s.pip); W.add_vec("pip_T", v4::wp5prov::DT_F64, pipT);
  W.add("pip_r", v4::wp5prov::DT_F64, pr.data(), pr.size() * 8, 2, R, p);
  std::vector<uint64_t> occ(1000, 0); const uint64_t tot = 16 * 2500;   // occupancy ∝ exact posterior mass
  for (size_t i = 0; i < std::min<size_t>(1000, cap); ++i) occ[i] = (uint64_t)std::llround(tot * std::exp(s.F[ord[i]] - s.logZ));
  W.add_vec("occ_top", v4::wp5prov::DT_U64, occ);
  double mx = *std::max_element(lr.begin(), lr.end()); double sw = 0; for (double x : lr) sw += std::exp(x - mx);
  Json m = Json::object();
  m.set("status", status); m.set("logZ", mx + std::log(sw / R)); m.set("hpm_F", s.F[ord[0]]); m.set("Rp", R); m.set("occ_total", tot);
  m.set("hpm_phase", "measured"); m.set("local_certified", true);
  Json tm = Json::object(); tm.set("islands_s", 12.5); m.set("timings", tm);
  W.add_json("meta", m.dump());
  W.write(path);
}

void write_truth(const std::string& path, double amp) {
  std::ofstream f(path);
  f << "{\"design\": \"AR\", \"params\": {\"rho\": 0.6}, \"seed\": 4242, \"S0\": [2, 6, 10], \"beta\": [" << amp << ", " << -0.8 * amp << ", " << 0.9 * amp << "], \"sigma\": 1.0}\n";
}

int call(int (*fn)(int, char**), std::vector<std::string> args) {
  std::vector<char*> av; static std::string prog = "x"; av.push_back(prog.data());
  for (auto& s : args) av.push_back(s.data());
  return fn((int)av.size(), av.data());
}

}  // namespace

TEST(e2e_post_and_eval) {
  const std::string d = tdir();
  Synthetic s = make_synthetic(31, 1.0);
  write_data_bin(s.O, d + "/data.bin");
  write_fit_bin(s, d + "/fit.bin", "completed", 5);
  write_truth(d + "/truth.json", 1.0);
  // post
  int rc = call(v4::post::run, {"--fit", d + "/fit.bin", "--data", d + "/data.bin", "--out", d + "/law", "--draws", "500", "--seed", "3"});
  CHECK(rc == 0);
  Json pj = Json::parse_file(d + "/law.json");
  CHECK(pj.at("status").str() == "completed");
  CHECK(pj.at("max_abs_dF").num() == 0.0);   // the scorer reproduces the stored F in bits
  v4::post::LawFile L = v4::post::read_law(d + "/law.bin");
  CHECK(L.models.size() == (size_t)pj.at("M").num() && L.models.size() > 10);
  double ws = 0; for (double w : L.w) ws += w; CHECK_NEAR(ws, 1.0, 1e-12);
  { v4::wp5prov::BinReader B(d + "/law.bin"); CHECK(B.has("draw_b") && B.entry("draw_b").dims[0] == 500); }
  // the law's parameters equal a fresh computation
  ModelPost mp = model_post(s.O.D, L.models[3].S);
  CHECK(mp.theta_bar == L.models[3].theta_bar && mp.beta_n == L.models[3].beta_n);
  // eval (built-in law) and eval (with law.bin) must agree on Π̂^𝒯
  const std::vector<std::string> common = {"--fit", d + "/fit.bin", "--data", d + "/data.bin", "--truth", d + "/truth.json",
                                           "--n-draws", "2000", "--n-x", "400", "--n-test", "2000", "--threads", "2"};
  std::vector<std::string> a1 = common; a1.insert(a1.end(), {"--out", d + "/eval1"});
  std::vector<std::string> a2 = common; a2.insert(a2.end(), {"--out", d + "/eval2", "--law", d + "/law.bin"});
  CHECK(call(v4::eval::run, a1) == 0);
  CHECK(call(v4::eval::run, a2) == 0);
  Json e1 = Json::parse_file(d + "/eval1.json"), e2 = Json::parse_file(d + "/eval2.json");
  CHECK(e1.at("status").str() == "completed");
  CHECK(e1.at("dist").at("T").dump() == e2.at("dist").at("T").dump());
  const Json& sel = e1.at("selection");
  CHECK(sel.at("hpm_eq_S0").boolean() && sel.at("outcome_class").str() == "correct");
  CHECK(sel.at("S0_in_store").boolean() && sel.at("F_S0_ledger_abs_diff").num() == 0.0);
  // HPM = S0 → Π̂^H = oracle: every ratio is exactly 1
  CHECK(e1.at("dist").at("ratio_to_oracle").at("H").at("plugin_h2").num() == 1.0);
  CHECK(e1.at("dist").at("ratio_to_oracle").at("H").at("predictive_h2").num() == 1.0);
  // store mass: Σ_𝒯 e^F / Ẑ with the exact enumeration ≤ 1 up to the island noise in Ẑ
  const Json& st = e1.at("store");
  CHECK(st.at("pi_T_hat").num() > 0.5 && st.at("size").num() == 40 * 12 + 1);
  // evidence: log Ẑ_occ with exact occupancies recovers the exact log Z (rounding of counts only)
  CHECK_NEAR(e1.at("evidence").at("logZ_occ").at("M10").num(), s.logZ, 2e-3);
  CHECK(e1.at("evidence").at("R_eff").num() > 1 && e1.at("evidence").at("R_eff").num() <= 16);
  CHECK(e1.at("pip").at("island_spread").at("Rp").num() == 16);
  CHECK(e1.at("pip").at("eq_T_target_met").boolean());
  CHECK(e1.at("pip").at("eq").at("min_true").num() > 0.9);
  // eval.bin
  v4::wp5prov::BinReader EB(d + "/eval1.bin");
  CHECK(EB.header().kind == v4::wp5prov::K_EVAL && EB.entry("dH_draws_T").length == 2000 * 8);
  std::printf("    e2e: law M=%d, pi_T_hat=%.4f, d_H^2 plug-in H=%.4g T=%.4g oracle=%.4g, predictive T=%.4g, eval wall %.2f s\n",
              (int)L.models.size(), st.at("pi_T_hat").num(), e1.at("dist").at("H").at("plugin").at("h2").num(),
              e1.at("dist").at("T").at("plugin").at("h2").num(), e1.at("dist").at("oracle").at("plugin").at("h2").num(),
              e1.at("dist").at("T").at("predictive").at("h2").num(), e1.at("cost").at("eval_wall_s").num());
}

TEST(e2e_failure_paths) {
  const std::string d = tdir();
  Synthetic s = make_synthetic(32, 0.5);
  write_data_bin(s.O, d + "/data_f.bin");
  write_truth(d + "/truth_f.json", 0.5);
  // incomplete fit: GUARD-W, no metrics, eval itself completed
  write_fit_bin(s, d + "/fit_inc.bin", "resource_limit", 6);
  CHECK(call(v4::eval::run, {"--fit", d + "/fit_inc.bin", "--data", d + "/data_f.bin", "--truth", d + "/truth_f.json", "--out", d + "/ev_inc"}) == 0);
  Json ji = Json::parse_file(d + "/ev_inc.json");
  CHECK(ji.at("fit_status").str() == "resource_limit" && !ji.has("selection") && !ji.has("dist"));
  // corrupt fit.bin: invalid_input (exit 13), no estimate fields
  write_fit_bin(s, d + "/fit_bad.bin", "completed", 7);
  { v4::wp5prov::BinReader B(d + "/fit_bad.bin"); uint64_t off = B.entry("pip_eq").offset;
    std::fstream f(d + "/fit_bad.bin", std::ios::in | std::ios::out | std::ios::binary); f.seekp((std::streamoff)off); char c = 1; f.write(&c, 1); }
  CHECK(call(v4::eval::run, {"--fit", d + "/fit_bad.bin", "--data", d + "/data_f.bin", "--truth", d + "/truth_f.json", "--out", d + "/ev_bad"}) == 13);
  Json jb = Json::parse_file(d + "/ev_bad.json");
  CHECK(jb.at("status").str() == "invalid_input" && !jb.has("selection"));
  // wrong kind (data.bin passed as fit)
  CHECK(call(v4::eval::run, {"--fit", d + "/data_f.bin", "--data", d + "/data_f.bin", "--truth", d + "/truth_f.json", "--out", d + "/ev_kind"}) == 13);
  // missing argument
  CHECK(call(v4::eval::run, {"--out", d + "/ev_noarg"}) == 13);
  CHECK(call(v4::post::run, {"--out", d + "/law_noarg"}) == 13);
}

#include "eval/io.h"
// Cross-WP check (runs when V4_WP1_FILES names a directory with WP1's data.bin and truth.json from `smcbvs4 gen/prep`):
// WP5 reads WP1's container, data.bin sections and truth.json; logprior bits must agree (load_data checks them).
TEST(e2e_wp1_files) {
  const char* dir = std::getenv("V4_WP1_FILES");
  if (!dir) { std::printf("    skipped: V4_WP1_FILES not set\n"); return; }
  const std::string d = dir, o = tdir();
  v4::eval::io::DataFile df; v4::eval::io::load_data(d + "/data.bin", df);
  Synthetic s; enumerate(df.D, s);
  write_fit_bin(s, o + "/fit_wp1.bin", "completed", 9);
  CHECK(call(v4::eval::run, {"--fit", o + "/fit_wp1.bin", "--data", d + "/data.bin", "--truth", d + "/truth.json", "--out", o + "/ev_wp1",
                             "--n-draws", "1000", "--n-x", "200", "--n-test", "1000"}) == 0);
  Json e = Json::parse_file(o + "/ev_wp1.json");
  CHECK(e.at("status").str() == "completed");
  std::printf("    WP1 files: p=%d, HPM=%s, outcome=%s, plug-in d_H^2 (H)=%.4g, seed=%g\n", df.D.p, e.at("selection").at("hpm").dump().c_str(),
              e.at("selection").at("outcome_class").str().c_str(), e.at("dist").at("H").at("plugin").at("h2").num(), e.at("params").at("seed").num());
  CHECK(e.at("params").at("seed").num() == 4242);
}
