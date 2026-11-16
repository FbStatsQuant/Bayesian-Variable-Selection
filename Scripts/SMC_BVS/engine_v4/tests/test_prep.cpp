// prep: R's mean/sum arithmetic; golden comparison against R's v3_preprocess (core/v3_preprocess.R) on fixtures
// written by tools/make_fixtures.R (tests/fixtures/prep_*). The golden part is skipped (with a notice) if absent.
#include <cmath>
#include <fstream>
#include "tk.h"
#include "tutil.h"
#include "v4/score.h"
#include "v4/format.h"
#include "v4/json.h"
using namespace v4;

namespace {
std::vector<double> read_f64(const std::string& f) {
  std::ifstream in(f, std::ios::binary | std::ios::ate);
  if (!in) return {};
  size_t n = (size_t)in.tellg() / 8; in.seekg(0);
  std::vector<double> v(n); in.read((char*)v.data(), (std::streamsize)(n * 8)); return v;
}
}  // namespace

TEST(prep_r_mean_two_pass) {
  // the correction pass matters: values where a one-pass long double mean differs in the last bit are common;
  // here only properties are checked (golden values come from R below).
  double x[] = {1.0, 1e-16, -1.0, 3.0};
  CHECK(prep::r_mean(x, 4) == 0.75);
  double y[] = {0.1, 0.2, 0.3};
  CHECK(std::fabs(prep::r_mean(y, 3) - 0.2) < 1e-16);
  CHECK(prep::r_sum(y, 3) == (double)(0.1L + 0.2L + 0.3L));
}
TEST(prep_drop_and_status) {
  std::vector<double> X = {1, 1, 1, 1, 2, 3, 4, 5, 7, 7, 7, 7}, y = {1, 2, 3, 4};
  auto r = prep::preprocess(X.data(), y.data(), 4, 3);
  CHECK(r.status == "ok" && r.kept == (std::vector<int32_t>{2}) && r.dropped == (std::vector<int32_t>{1, 3}));
  std::vector<double> yc = {2, 2, 2, 2};
  CHECK(prep::preprocess(X.data(), yc.data(), 4, 3).status == "y_constant");
  std::vector<double> Xc = {1, 1, 1, 1};
  CHECK(prep::preprocess(Xc.data(), y.data(), 4, 1).status == "no_predictors");
  std::vector<double> Xn = {1, NAN, 1, 2};
  CHECK(prep::preprocess(Xn.data(), y.data(), 4, 1).status == "invalid_input");
  // anchored branch (near-constant column): standardised values are finite with unit sample sd
  std::vector<double> xa = {1.0, 1.0 + 1e-12, 1.0 - 2e-12, 1.0 + 3e-12}; std::vector<double> z(4);
  auto c = prep::standardise(xa.data(), 4, z.data());
  double ss = 0; for (double v : z) ss += v * v;
  CHECK(c.anchored && std::fabs(ss / 3 - 1) < 1e-12);
}
TEST(prep_bits_equal_R_v3_preprocess) {
  std::string dir = V4_FIXTURE_DIR;
  Json idx;
  try { idx = read_json_file(dir + "/prep/index.json"); } catch (...) { std::printf("    SKIP: no prep fixtures (run tools/make_fixtures.R)\n"); return; }
  int ncases = 0, anchored = 0;
  for (auto& cs : idx.at("cases").elems()) {
    anchored += (int)cs.at("anchored").i64();
    std::string name = cs.at("name").str();
    int n = (int)cs.at("n").i64(), p_raw = (int)cs.at("p_raw").i64();
    std::vector<double> X, y;
    if (cs.at("stored_X").boolean()) { X = read_f64(dir + "/prep/" + name + "_X.f64"); y = read_f64(dir + "/prep/" + name + "_y.f64"); }
    else {
      // regenerate with gen and check the raw content hash recorded when the fixture was made
      std::string f = tmp_path(name + "_raw.bin");
      Json a = Json::object(); Json sp = Json::object();
      sp["design"] = cs.at("design"); sp["n"] = n; sp["p"] = p_raw; sp["seed"] = cs.at("seed");
      a["spec"] = sp; a["out"] = f;
      Json rec = gen::run(a);
      CHECK_MSG(rec.at("raw_content_sha256").str() == cs.at("raw_sha256").str(), name + ": gen output changed since the fixture was made");
      fmt::Reader rd(f); X = rd.vec<double>("X_cm"); y = rd.vec<double>("y");
      std::remove(f.c_str());
    }
    auto Xs = read_f64(dir + "/prep/" + name + "_Xs.f64"), ys = read_f64(dir + "/prep/" + name + "_ys.f64");
    auto stats = read_f64(dir + "/prep/" + name + "_stats.f64");   // col_max, col_mean, col_sd (p each), then y_max, y_mean, y_sd
    CHECK_MSG(X.size() == (size_t)n * p_raw && y.size() == (size_t)n, name);
    auto r = prep::preprocess(X.data(), y.data(), n, p_raw);
    CHECK_MSG(r.status == "ok", name);
    if (r.status != "ok") continue;
    int p = r.p;
    std::vector<int32_t> kept; for (auto& v : cs.at("kept").elems()) kept.push_back((int32_t)v.i64());
    CHECK_MSG(kept == r.kept, name);
    size_t bad = 0;
    for (size_t i = 0; i < (size_t)n * p; ++i) bad += !same_bits(Xs[i], r.own->X[i]);
    for (int i = 0; i < n; ++i) bad += !same_bits(ys[i], r.own->y[i]);
    for (int j = 0; j < p; ++j) bad += !same_bits(stats[j], r.own->col_max[j]) + !same_bits(stats[p + j], r.own->col_mean[j]) + !same_bits(stats[2 * p + j], r.own->col_sd[j]);
    bad += !same_bits(stats[3 * p], r.ystd.max) + !same_bits(stats[3 * p + 1], r.ystd.mean) + !same_bits(stats[3 * p + 2], r.ystd.sd);
    CHECK_MSG(bad == 0, name + ": " + std::to_string(bad) + " mismatching values");
    ++ncases;
  }
  std::printf("    %d R golden prep cases compared (incl. %d anchored columns)\n", ncases, anchored);
  CHECK(ncases > 0);
}

namespace {
std::vector<int32_t> read_i32(const std::string& f) {
  std::ifstream in(f, std::ios::binary | std::ios::ate);
  if (!in) return {};
  size_t n = (size_t)in.tellg() / 4; in.seekg(0);
  std::vector<int32_t> v(n); in.read((char*)v.data(), (std::streamsize)(n * 4)); return v;
}
v4::Data data_from_R(const std::string& name, int n, int p) {
  std::string dir = std::string(V4_FIXTURE_DIR) + "/prep/";
  auto own = std::make_shared<DataOwned>();
  own->X = read_f64(dir + name + "_Xs.f64"); own->y = read_f64(dir + name + "_ys.f64");
  return make_data(own, n, p);
}
}  // namespace

// Golden: the Bit scorer on R's standardised data against core cpp_score (R-compiled revision D, Makevars.v3).
TEST(score_bits_equal_R_cpp_score) {
  std::string dir = std::string(V4_FIXTURE_DIR) + "/score/";
  Json idx;
  try { idx = read_json_file(dir + "index.json"); } catch (...) { std::printf("    SKIP: no score fixtures\n"); return; }
  int total = 0;
  for (auto& cs : idx.at("cases").elems()) {
    std::string nm = cs.at("name").str(); int n = (int)cs.at("n").i64(), p = (int)cs.at("p").i64();
    Data D = data_from_R(nm, n, p);
    auto consts = read_f64(dir + nm + "_consts.f64");
    CHECK_MSG(same_bits(consts[0], D.logCn) && same_bits(consts[1], D.logm0) && same_bits(consts[2], D.logWK) && same_bits(consts[3], D.yty), nm + " constants");
    auto ptr = read_i32(dir + nm + "_ptr.i32"), idxs = read_i32(dir + nm + "_idx.i32"), route = read_i32(dir + nm + "_route.i32");
    auto lm = read_f64(dir + nm + "_logm.f64"), Q = read_f64(dir + nm + "_Q.f64");
    BitScorer sc(&D); int bad = 0;
    for (size_t m = 0; m + 1 < ptr.size(); ++m) {
      ModelView S(idxs.data() + ptr[m], (uint32_t)(ptr[m + 1] - ptr[m]));
      ScoreOut o = sc.score(S);
      if (!same_bits(o.logm, lm[m]) || !same_bits(o.Q, Q[m]) || o.route != route[m]) ++bad;
      ++total;
    }
    CHECK_MSG(bad == 0, nm + ": " + std::to_string(bad) + " mismatches");
  }
  std::printf("    %d R golden scores compared\n", total);
}
// Golden: table scores log m(U) of every block subset (core v3_setup tables) by the Bit scorer.
TEST(table_scores_equal_R_v3_setup) {
  std::string dir = std::string(V4_FIXTURE_DIR) + "/setup/";
  Json idx;
  try { idx = read_json_file(dir + "index.json"); } catch (...) { std::printf("    SKIP: no setup fixtures\n"); return; }
  int total = 0;
  for (auto& cs : idx.at("cases").elems()) {
    std::string nm = cs.at("name").str(); int n = (int)cs.at("n").i64(), p = (int)cs.at("p").i64();
    Data D = data_from_R(nm, n, p);
    auto bptr = read_i32(dir + nm + "_blk_ptr.i32"), mem = read_i32(dir + nm + "_blk_members.i32"), cptr = read_i32(dir + nm + "_code_ptr.i32");
    auto logr = read_f64(dir + nm + "_logr.f64");
    BitScorer sc(&D); int bad = 0; Model U;
    for (size_t b = 0; b + 1 < bptr.size(); ++b) {
      int m = bptr[b + 1] - bptr[b];
      for (uint32_t code = 0; code < (1u << m); ++code) {
        U.clear(); for (int i = 0; i < m; ++i) if (code & (1u << i)) U.push_back(mem[bptr[b] + i]);
        double want = logr[cptr[b] + code];
        if ((int)U.size() > D.K) { if (!std::isnan(want)) ++bad; continue; }
        // core/cpp/v3_start.h:95: log r = log m(U) - log m(empty), 0 for the empty code
        double got = code == 0 ? 0.0 : sc.score(U).logm - D.logm0;
        if (!same_bits(got, want)) ++bad;
        ++total;
      }
    }
    CHECK_MSG(bad == 0, nm + ": " + std::to_string(bad) + " table mismatches");
  }
  std::printf("    %d R golden table entries compared\n", total);
}
