// prep: R's mean/sum arithmetic; golden comparison against R's v3_preprocess (core/v3_preprocess.R) on fixtures
// written by tools/make_fixtures.R (tests/fixtures/prep_*). The golden part is skipped (with a notice) if absent.
#include <cmath>
#include <fstream>
#include "tk.h"
#include "tutil.h"
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
  int ncases = 0;
  for (auto& cs : idx.at("cases").elems()) {
    std::string name = cs.at("name").str();
    int n = (int)cs.at("n").i64(), p_raw = (int)cs.at("p_raw").i64();
    auto X = read_f64(dir + "/prep/" + name + "_X.f64"), y = read_f64(dir + "/prep/" + name + "_y.f64");
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
  std::printf("    %d R golden prep cases compared\n", ncases);
  CHECK(ncases > 0);
}
