#include <cmath>
#include "tk.h"
#include "tutil.h"
#include "v4/format.h"
#include "v4/sha256.h"
#include "v4/rng.h"
#include "v4/threads.h"
using namespace v4;

namespace {
std::string digest(const std::vector<double>& X, const std::vector<double>& y) {
  Sha256 s; s.update(X.data(), X.size() * 8); s.update(y.data(), y.size() * 8); return hex(s.final());
}
}

TEST(gen_thread_invariance) {
  for (auto d : {gen::Design::AR, gen::Design::IND, gen::Design::BLK, gen::Design::ADJOPP}) {
    gen::Spec s; s.design = d; s.n = 50; s.p = 333; s.seed = 99; if (d == gen::Design::BLK) s.rho = 0.5;
    std::vector<std::string> h;
    for (int t : {1, 2, 3}) { set_threads(t); std::vector<double> X, y; gen::generate(s, X, y); h.push_back(digest(X, y)); }
    CHECK(h[0] == h[1] && h[1] == h[2]);
  }
  set_threads(1);
}
TEST(gen_truth_layout) {
  gen::Spec s; s.p = 1000000;
  auto t = gen::truth(s);
  CHECK(t.S0 == (std::vector<int32_t>{100000, 300000, 500000, 700000, 900000}));
  CHECK(t.beta == (std::vector<double>{1.0, -0.8, 0.9, -0.7, 0.6}));
  s.design = gen::Design::ADJOPP; t = gen::truth(s);
  CHECK(t.S0 == (std::vector<int32_t>{100000, 100001, 500000, 700000, 900000}));
  s.design = gen::Design::BLK; s.p = 130; s.b = 30; t = gen::truth(s);   // 13,39,65,91,117 -> 117 shares block 3 with 91
  CHECK(t.S0 == (std::vector<int32_t>{13, 39, 65, 91, 121}));
  s.p = 120; CHECK_THROWS(gen::truth(s));                                // truths cannot be placed in distinct blocks
  s.p = 200; s.a = 0.6; t = gen::truth(s); CHECK(std::fabs(t.beta[0] - 0.6) < 1e-15 && t.S0.size() == 5);
  s.a = 0; CHECK(gen::truth(s).S0.empty());
}
TEST(gen_moments_sanity) {
  // AR(0.6): lag-1 correlation ~0.6, unit variance; BLK(20, 0.5): within-block correlation ~0.5
  gen::Spec s; s.n = 4000; s.p = 40; s.seed = 4; s.a = 0;
  std::vector<double> X, y; gen::generate(s, X, y);
  double v = 0, c = 0; for (int i = 0; i < s.n; ++i) { v += X[(size_t)10 * s.n + i] * X[(size_t)10 * s.n + i]; c += X[(size_t)10 * s.n + i] * X[(size_t)11 * s.n + i]; }
  CHECK(std::fabs(v / s.n - 1) < 0.08); CHECK(std::fabs(c / s.n - 0.6) < 0.06);
  s.design = gen::Design::BLK; s.rho = 0.5; gen::generate(s, X, y);
  c = 0; for (int i = 0; i < s.n; ++i) c += X[(size_t)1 * s.n + i] * X[(size_t)2 * s.n + i];
  double c2 = 0; for (int i = 0; i < s.n; ++i) c2 += X[(size_t)1 * s.n + i] * X[(size_t)25 * s.n + i];
  CHECK(std::fabs(c / s.n - 0.5) < 0.06); CHECK(std::fabs(c2 / s.n) < 0.06);
}
TEST(gen_test_rows) {
  for (auto d : {gen::Design::AR, gen::Design::IND, gen::Design::BLK}) {
    gen::Spec s; s.design = d; s.n = 20; s.p = 200; s.seed = 7; if (d == gen::Design::BLK) s.rho = 0.5;
    std::vector<int32_t> all; for (int j = 1; j <= s.p; ++j) all.push_back(j);
    std::vector<int32_t> oc, oc2; std::vector<double> Xt, yt, Xs, ys;
    gen::generate_test(s, 15, all, oc, Xt, yt);
    CHECK(oc == all);
    // full set: AR test rows follow the same recursion as training (on the test addresses): check one entry
    if (d == gen::Design::AR) {
      double rho = s.rho, c = std::sqrt(1 - rho * rho);
      double x2 = rho * Xt[(size_t)1 * 15 + 3] + c * gen::normal_at(s.seed, X_TEST_X, 3, 2);
      CHECK(same_bits(x2, Xt[(size_t)2 * 15 + 3]));
    }
    // subset (S0 always added): IND and BLK values equal the full-set values
    gen::generate_test(s, 15, {2, 40}, oc2, Xs, ys);
    auto S0 = gen::truth(s).S0;
    for (int32_t j : S0) CHECK(std::binary_search(oc2.begin(), oc2.end(), j));
    if (d != gen::Design::AR) {
      CHECK(ys == yt);   // y only depends on the S0 columns and the noise
      bool ok = true;
      for (size_t c = 0; c < oc2.size(); ++c) for (int i = 0; i < 15; ++i) ok = ok && same_bits(Xs[c * 15 + i], Xt[(size_t)(oc2[c] - 1) * 15 + i]);
      CHECK(ok);
    }
  }
}
TEST(gen_command_writes_raw_and_truth) {
  std::string f = tmp_path("raw.bin"), t = tmp_path("truth.json");
  Json a = Json::object(); a["spec"] = Json::parse("{\"design\":\"AR\",\"n\":30,\"p\":100,\"seed\":5}"); a["out"] = f; a["truth"] = t;
  Json r1 = gen::run(a), r2 = gen::run(a);
  CHECK(r1.at("raw_content_sha256").str() == r2.at("raw_content_sha256").str());   // same binary -> same file
  CHECK(r1.at("X_sha256").str() == r2.at("X_sha256").str());
  fmt::Reader rd(f);
  CHECK(rd.entry("X_cm").dims[0] == 30 && rd.entry("X_cm").dims[1] == 100);
  Json tj = read_json_file(t);
  CHECK(tj.at("S0").size() == 5 && tj.at("raw_content_sha256").str() == rd.content_hash());
  CHECK(tj.at("X_sha256").str() == hex(rd.entry("X_cm").sha256, 32));
  std::remove(f.c_str()); std::remove(t.c_str());
}

// Row ranges (for WP5's chunked evaluation): rows [a, b) equal the same rows of the full test design, bit for bit.
TEST(gen_test_row_ranges) {
  for (auto d : {gen::Design::AR, gen::Design::IND, gen::Design::BLK, gen::Design::ADJOPP}) {
    gen::Spec s; s.design = d; s.n = 20; s.p = 200; s.seed = 11; if (d == gen::Design::BLK) s.rho = 0.5;
    std::vector<int32_t> cols = {3, 50, 120}, oc, oc2; std::vector<double> Xt, yt, Xr, yr;
    const int nt = 37; gen::generate_test(s, nt, cols, oc, Xt, yt);
    bool ok = true;
    for (auto [a, b] : std::vector<std::pair<int, int>>{{0, 37}, {5, 6}, {10, 30}, {36, 37}, {12, 12}}) {
      gen::generate_test_rows(s, a, b, cols, oc2, Xr, yr);
      ok = ok && oc2 == oc && yr.size() == (size_t)(b - a);
      for (int i = a; i < b; ++i) {
        ok = ok && same_bits(yr[(size_t)(i - a)], yt[(size_t)i]);
        for (size_t c = 0; c < oc.size(); ++c) ok = ok && same_bits(Xr[c * (size_t)(b - a) + (size_t)(i - a)], Xt[c * nt + (size_t)i]);
      }
    }
    CHECK(ok);
    CHECK_THROWS(gen::generate_test_rows(s, 5, 4, cols, oc2, Xr, yr));
  }
}
