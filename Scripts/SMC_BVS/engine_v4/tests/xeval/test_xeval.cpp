// test_xeval.cpp -- smcbvs4_xeval / v4::xeval::cross_h2 (cross predictive Hellinger of two store-BMA laws):
//   d_H(A, A) = 0, symmetry, agreement with the engine's own d_H(A, f*) when B is the truth, a hand case, an independent
//   Simpson integration of mixture vs mixture, GH-order doubling.
#include <unistd.h>

#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <filesystem>
#include <random>
#include <stdexcept>

#include "eval/io.h"
#include "v4/eval.h"
#include "v4/format.h"
#include "v4/gen.h"
#include "v4/post.h"
#include "v4/sha256.h"
#include "v4/prep.h"
#include "wp5_tk.h"
#include "xeval/xeval.h"

using namespace v4;
using namespace v4::eval;

namespace {
Truth gen_truth(const std::string& design, int32_t p, uint32_t seed, double rho = 0.6) {
  Json sp = Json::object(); sp["design"] = design; sp["n"] = 200; sp["p"] = p; sp["seed"] = (int64_t)seed; sp["rho"] = rho; sp["b"] = 20; sp["s0"] = 5; sp["a"] = 1.0;
  gen::Spec s = gen::spec_from_json(sp);
  gen::Truth t = gen::truth(s);
  Json tj = Json::object(); tj["spec"] = gen::spec_to_json(s); tj["S0"] = Json::array_of(t.S0); tj["beta"] = Json::array_of(t.beta); tj["sigma"] = 1.0; tj["seed"] = (int64_t)seed;
  return truth_from_json(tj);
}
struct Fix { Truth T; Data D; };
Fix make_fix(const std::string& design, int32_t p, uint32_t seed) {
  Fix f; f.T = gen_truth(design, p, seed);
  gen::Spec sp = gen::spec_from_json(f.T.gen_spec);
  std::vector<double> X, y; gen::generate(sp, X, y);
  f.D = data_from_raw(X.data(), y.data(), sp.n, sp.p);
  return f;
}
// a store-like law: S0, S0 + j (all j), S0 + j + l (random pairs); weights ∝ e^{temp (F − Fmax)}; M models in total
Law make_law(const Fix& f, size_t M, double temp, uint64_t rs, const std::string& name) {
  Model S0; for (int32_t o : f.T.S0) S0.push_back(o - 1);
  std::vector<Model> ms = {S0};
  for (int32_t j = 0; j < f.D.p && ms.size() < M; ++j) if (!std::binary_search(S0.begin(), S0.end(), j)) { Model m = S0; sorted_insert(m, j); ms.push_back(m); }
  std::mt19937_64 g(rs);
  while (ms.size() < M) {
    int32_t j = (int32_t)(g() % f.D.p), l = (int32_t)(g() % f.D.p); Model m = S0;
    if (j == l || std::binary_search(m.begin(), m.end(), j) || std::binary_search(m.begin(), m.end(), l)) continue;
    sorted_insert(m, j); sorted_insert(m, l); ms.push_back(m);
  }
  std::shuffle(ms.begin() + 1, ms.end(), g);
  if (ms.size() > M) ms.resize(M);
  std::vector<ModelPost> mp(ms.size());
  for (size_t i = 0; i < ms.size(); ++i) mp[i] = model_post(f.D, ms[i]);
  double fmax = -INFINITY; for (auto& m : mp) fmax = std::max(fmax, m.F);
  std::vector<double> w(ms.size()); double ws = 0;
  for (size_t i = 0; i < ms.size(); ++i) { w[i] = std::exp(temp * (mp[i].F - fmax)); ws += w[i]; }
  Law L; L.name = name;
  for (size_t i = 0; i < ms.size(); ++i) L.comps.push_back(component_from_post(f.D, mp[i], w[i] / ws));
  return L;
}
xeval::CrossOpts small_opts(uint32_t seed) {
  xeval::CrossOpts o; o.seed = seed; o.n_x = 300; o.n_gh = 64; o.threads = 1; o.top_k = 300; o.tail_r = 400; o.tail_groups = 8; o.block_rows = 100;
  return o;
}
}  // namespace

// d_H(A, A) = 0: the affinity of a density with itself is ∫ f = 1; the numerical value is 0 to the quadrature error
TEST(xeval_self_distance_zero) {
  const Fix f = make_fix("AR", 300, 11);
  const Law L = make_law(f, 40, 0.5, 1, "A");   // exact mixture (40 ≤ top_k)
  const xeval::CrossResult r = xeval::cross_h2(L, L, f.T, small_opts(5), 2, 6);
  std::printf("    d_H^2(A,A) exact mixture: %.3e\n", r.h2);
  CHECK(r.exact_a && r.exact_b);
  CHECK_NEAR(r.h2, 0.0, 1e-12);
  // single Gaussian-truth component: the same law twice
  const Law Tl = xeval::truth_law(f.T);
  const xeval::CrossResult r0 = xeval::cross_h2(Tl, Tl, f.T, small_opts(5), 2, 6);
  std::printf("    d_H^2(f*,f*): %.3e\n", r0.h2);
  CHECK_NEAR(r0.h2, 0.0, 1e-13);
  // a large law (tail sampled): the same law with the same stream ids gives the identical estimate, hence ≈ 0
  const Law Lb = make_law(f, 1500, 0.25, 2, "B");
  const xeval::CrossResult rb = xeval::cross_h2(Lb, Lb, f.T, small_opts(5), 2, 2);
  std::printf("    d_H^2(B,B) tail-sampled, same streams: %.3e\n", rb.h2);
  CHECK(!rb.exact_a);
  CHECK_NEAR(rb.h2, 0.0, 1e-10);
}

// symmetry: d_H(A, B) = d_H(B, A), bit-equal when the stream ids travel with the laws (exact and tail-sampled)
TEST(xeval_symmetric) {
  const Fix f = make_fix("AR", 300, 12);
  const Law A = make_law(f, 60, 0.5, 3, "A"), B = make_law(f, 60, 1.0, 4, "B");
  const xeval::CrossResult ab = xeval::cross_h2(A, B, f.T, small_opts(7), 2, 6), ba = xeval::cross_h2(B, A, f.T, small_opts(7), 6, 2);
  std::printf("    exact laws: h2(A,B) = %.12g, h2(B,A) = %.12g\n", ab.h2, ba.h2);
  CHECK(ab.h2 > 1e-6);
  CHECK(same_bits(ab.h2, ba.h2));
  const Law A2 = make_law(f, 1500, 0.25, 5, "A2"), B2 = make_law(f, 1200, 0.35, 6, "B2");
  const xeval::CrossResult c = xeval::cross_h2(A2, B2, f.T, small_opts(7), 2, 6), d = xeval::cross_h2(B2, A2, f.T, small_opts(7), 6, 2);
  std::printf("    tail-sampled laws: h2(A,B) = %.12g, h2(B,A) = %.12g (tail SE %.2e)\n", c.h2, d.h2, c.se_tail);
  CHECK(!c.exact_a && !c.exact_b && c.h2 > 1e-6);
  CHECK(same_bits(c.h2, d.h2));
  CHECK(same_bits(c.se_tail, d.se_tail));
}

// B = the truth reproduces the engine's own d_H(A, f*) (dist_metrics "predictive"): same rows, same GH, same tail streams
TEST(xeval_equals_engine_dH_to_truth) {
  const Fix f = make_fix("AR", 400, 31);
  for (size_t M : {size_t(50), size_t(1500)}) {   // exact mixture and top-K + tail
    const Law L = make_law(f, M, 0.25, 9, "T");
    DistOpts eo; eo.n_draws = 10; eo.n_test = 2; eo.n_x = 300; eo.top_k = 300; eo.tail_r = 400; eo.block_rows = 100; eo.seed = 21; eo.threads = 1;
    const Json j = dist_metrics(L, f.T, f.D.n, eo, 2);
    const Json& q = j.at("predictive");
    const xeval::CrossResult r = xeval::cross_h2(L, xeval::truth_law(f.T), f.T, small_opts(21), 2, 6);
    std::printf("    M=%zu: engine h2 %.15g, xeval h2 %.15g, |diff| %.2e (tail SE %.2e)\n", M, q.at("h2").num(), r.h2, std::fabs(q.at("h2").num() - r.h2), r.se_tail);
    CHECK_EQ(q.at("exact").boolean(), r.exact_a);
    CHECK_NEAR(q.at("h2").num(), r.h2, 1e-12);
    CHECK_NEAR(q.at("h2_se_x").num(), r.se_x, 1e-12);
    CHECK_NEAR(q.at("h2_se_tail").num(), r.se_tail, 1e-12);
    CHECK_NEAR(q.at("h2_topK").num(), r.h2_topK, 1e-12);
    // the oracle and a one-model law (Student predictive vs the truth) as well
    const Law Hm = make_law(f, 1, 1.0, 1, "H");
    const Json jh = dist_metrics(Hm, f.T, f.D.n, eo, 0);
    CHECK_NEAR(jh.at("predictive").at("h2").num(), xeval::cross_h2(Hm, xeval::truth_law(f.T), f.T, small_opts(21), 0, 6).h2, 1e-12);
  }
}

// hand case: two Gaussian point predictives on an IND design. Per x, ∫√(f_A f_B) dy is the closed form h2_normals; the cross
// value must be the average over the SAME rows of 1 − that closed form (to the GH accuracy, ≈ 1e-13).
TEST(xeval_hand_case_two_gaussians) {
  const Truth T = gen_truth("IND", 200, 41);
  const std::vector<int32_t> cols = {3, 17, 90};
  Law A; A.name = "A"; A.comps.push_back(component_gaussian(cols, {0.9, -0.4, 0.2}, 0.1, 1.2, 1.0));
  Law B; B.name = "B"; B.comps.push_back(component_gaussian(cols, {1.0, -0.1, 0.0}, -0.2, 0.8, 1.0));
  xeval::CrossOpts o = small_opts(3); o.n_x = 250; o.block_rows = 80;
  const xeval::CrossResult r = xeval::cross_h2(A, B, T, o, 2, 6);
  // the hand value: rows 0 … 249 of the same design
  double acc = 0;
  for (uint32_t r0 = 0; r0 < 250; r0 += 80) {
    const uint32_t nr = std::min<uint32_t>(80, 250 - r0);
    const XSample xs = make_rows(T, cols, r0, nr, o.seed, false);
    for (uint32_t i = 0; i < nr; ++i) {
      double ma = 0.1, mb = -0.2;
      for (size_t k = 0; k < cols.size(); ++k) { const double x = xs.X[i * xs.cols.size() + xs.pos(cols[k])]; ma += x * std::vector<double>{0.9, -0.4, 0.2}[k]; mb += x * std::vector<double>{1.0, -0.1, 0.0}[k]; }
      acc += h2_normals(ma, 1.2, mb, 0.8);
    }
  }
  const double hand = acc / 250;
  std::printf("    hand h2 = %.15g, xeval h2 = %.15g\n", hand, r.h2);
  CHECK(hand > 1e-3);
  CHECK_NEAR(r.h2, hand, 1e-12);
}

// independent check of mixture vs mixture: Simpson integration of √(f̄_A f̄_B) over y at each row (the engine's exact mixture
// density log_pred_density), and the doubling of the GH order (64 → 128) changes h2 by ≤ 1e-8
TEST(xeval_mixture_vs_simpson_and_gh_doubling) {
  const Fix f = make_fix("AR", 300, 51);
  const Law A = make_law(f, 30, 0.5, 13, "A"), B = make_law(f, 30, 1.0, 14, "B");
  xeval::CrossOpts o = small_opts(9); o.n_x = 6; o.block_rows = 6;
  const xeval::CrossResult r = xeval::cross_h2(A, B, f.T, o, 2, 6);
  std::vector<int32_t> cols;
  for (const Law* L : {&A, &B}) for (auto& c : L->comps) cols.insert(cols.end(), c.orig.begin(), c.orig.end());
  const XSample xs = make_rows(f.T, cols, 0, 6, o.seed, false);
  double acc = 0;
  for (size_t i = 0; i < 6; ++i) {
    const double lo = -50, hi = 50; const int N = 100000; const double h = (hi - lo) / N;
    double s = 0;
    for (int k = 0; k <= N; ++k) {
      const double y = lo + k * h, v = std::exp(0.5 * (log_pred_density(A, xs, i, y) + log_pred_density(B, xs, i, y)));
      s += (k == 0 || k == N) ? v : (k % 2 ? 4 * v : 2 * v);
    }
    acc += 1.0 - s * h / 3.0;
  }
  std::printf("    Simpson h2 = %.12g, xeval h2 = %.12g\n", acc / 6, r.h2);
  CHECK(r.h2 > 1e-5);
  CHECK_NEAR(r.h2, acc / 6, 1e-8);
  xeval::CrossOpts o2 = small_opts(9); o2.n_gh = 128;
  const xeval::CrossResult a64 = xeval::cross_h2(A, B, f.T, small_opts(9), 2, 6), a128 = xeval::cross_h2(A, B, f.T, o2, 2, 6);
  std::printf("    GH 64 vs 128: %.15g vs %.15g (diff %.2e)\n", a64.h2, a128.h2, std::fabs(a64.h2 - a128.h2));
  CHECK_NEAR(a64.h2, a128.h2, 1e-8);
}

// the command on real law.bin files (gen -> prep -> law.bin from two different store subsets): record layout (the `pairs`
// object compare_overlap.py reads), equality with the library call, symmetry in the files (a <-> b), --b_truth, and the
// refusal of two laws built on different data
namespace {
std::string tdir() {
  static std::string d;
  if (d.empty()) {
    const char* td = std::getenv("TMPDIR");
    if (!td || !*td) throw std::runtime_error("TMPDIR is not set (tests write only under $TMPDIR)");
    d = std::string(td) + "/xeval_cmd_" + std::to_string(getpid());
    std::filesystem::create_directories(d);
    static struct Rm { ~Rm() { std::error_code ec; if (!d.empty() && !std::getenv("V4_XEVAL_KEEP")) std::filesystem::remove_all(d, ec); } } rm;   // V4_XEVAL_KEEP=1 keeps the files (CLI smoke test)
  }
  return d;
}
struct Prep { std::string dir, data, truth, dhash; Data D; };
Prep make_prep(uint32_t seed, const std::string& tag) {
  Prep r; r.dir = tdir() + "/" + tag; std::filesystem::create_directories(r.dir);
  Json spec = Json::object(); spec["design"] = "AR"; spec["n"] = 100; spec["p"] = 12; spec["seed"] = (int64_t)seed; spec["s0"] = 3; spec["a"] = 1.0;
  Json ga = Json::object(); ga["spec"] = spec; ga["out"] = r.dir + "/raw.bin"; ga["truth"] = r.dir + "/truth.json"; gen::run(ga);
  Json pa = Json::object(); pa["in"] = r.dir + "/raw.bin"; pa["out"] = r.dir + "/data.bin"; prep::run(pa);
  r.data = r.dir + "/data.bin"; r.truth = r.dir + "/truth.json";
  r.D = prep::load_data(r.data, &r.dhash);
  return r;
}
// a law.bin from the best `cap` models of size <= 3 (a stand-in for a fit's store), recorded inputs.data.bin = the data hash
void write_store_law(const Prep& P, size_t cap, const std::string& path) {
  std::vector<Model> ms; std::vector<double> F;
  for (uint32_t code = 0; code < (1u << P.D.p); ++code) {
    Model S; for (int j = 0; j < P.D.p; ++j) if (code >> j & 1) S.push_back(j);
    if (S.size() > 3) continue;
    ms.push_back(S); F.push_back(model_post(P.D, S).F);
  }
  std::vector<size_t> ord(ms.size()); for (size_t i = 0; i < ord.size(); ++i) ord[i] = i;
  std::sort(ord.begin(), ord.end(), [&](size_t a, size_t b) { return F[a] > F[b] || (F[a] == F[b] && a < b); });
  std::vector<double> v; std::vector<uint64_t> off, hash; std::vector<uint16_t> len; std::vector<int32_t> pool;
  for (size_t i = 0; i < std::min(cap, ord.size()); ++i) {
    const Model& S = ms[ord[i]];
    v.push_back(F[ord[i]]); off.push_back(pool.size()); len.push_back((uint16_t)S.size()); hash.push_back(P.D.zob.hash(S));
    pool.insert(pool.end(), S.begin(), S.end());
  }
  StoreView sv; sv.size = v.size(); sv.v = v.data(); sv.off = off.data(); sv.len = len.data(); sv.hash = hash.data(); sv.pool = pool.data();
  post::LawFile L = post::build_law(P.D, sv, 1e-12, 1000000, 1);
  Json inp = Json::object(); inp["data.bin"] = P.dhash; L.meta_extra["inputs"] = inp;
  post::write_law(L, path, 0, 0, 3);
}
Json xargs(const std::string& a, const std::string& b, const Prep& P, const std::string& out, bool with_data = true) {
  Json j = Json::object();
  j["a"] = a; if (!b.empty()) j["b"] = b; else j["b_truth"] = 1;
  j["truth"] = P.truth; if (with_data) j["data"] = P.data; j["out"] = out;
  j["dataset"] = "4-AR-n200-r01"; j["seed_id"] = 1; j["n_x"] = 200; j["block_rows"] = 100; j["top_k"] = 20; j["tail_r"] = 30;
  return j;
}
// the same X / y written with another meta block (what another binary's provenance block does to a data.bin): identical sections,
// different whole-file hash
Prep meta_variant(const Prep& P, const std::string& tag) {
  Prep r = P; r.dir = tdir() + "/" + tag; std::filesystem::create_directories(r.dir);
  prep::Result res; res.n = P.D.n; res.p = P.D.p; res.p_raw = P.D.p_raw;
  { fmt::Reader rd(P.data); res.dropped = rd.vec<int32_t>("dropped"); }
  Json inputs = Json::object(); inputs["raw.bin"] = "another build";
  r.data = r.dir + "/data.bin";
  r.dhash = prep::write_data(r.data, P.D, res, "meta_variant", inputs);
  std::string chk; r.D = prep::load_data(r.data, &chk);
  return r;
}
std::string section_sha(const std::string& path, const char* sec) { fmt::Reader rd(path); return hex(rd.entry(sec).sha256, 32); }
}  // namespace

// data identity guard: two data.bin with identical X / y but different meta (e.g. the T and V builds) are ACCEPTED; a different X
// (or y) is refused; so is a file that is not the data.bin its law recorded, and unverifiable recorded-hash differences
TEST(xeval_data_identity_guard_xy_sections) {
  const Prep P = make_prep(4242, "id_p"), Q = make_prep(777, "id_q"), R = meta_variant(P, "id_r");
  CHECK(R.dhash != P.dhash);                                             // whole-file hashes differ (meta block) ...
  CHECK(section_sha(R.data, "Xs_cm") == section_sha(P.data, "Xs_cm"));   // ... the X and y sections are bit-identical
  CHECK(section_sha(R.data, "ys") == section_sha(P.data, "ys"));
  CHECK(section_sha(Q.data, "Xs_cm") != section_sha(P.data, "Xs_cm"));
  write_store_law(P, 150, P.dir + "/law_V.bin"); write_store_law(R, 60, R.dir + "/law_T.bin"); write_store_law(Q, 60, Q.dir + "/law_T.bin");
  // accepted: identical X/y, different meta (both orders)
  Json ok = xargs(P.dir + "/law_V.bin", R.dir + "/law_T.bin", P, P.dir + "/g1.json"); ok["data_b"] = R.data;
  const Json r1 = xeval::run(ok);
  CHECK(r1.at("status").str() == "completed");
  CHECK(r1.at("inputs").at("data_identity").at("X_section_sha256").str() == section_sha(P.data, "Xs_cm"));
  CHECK(r1.at("inputs").at("data_identity").at("y_section_sha256").str() == section_sha(P.data, "ys"));
  CHECK(r1.at("inputs").at("data.bin").str() == P.dhash && r1.at("inputs").at("data_b.bin").str() == R.dhash);
  Json ok2 = xargs(R.dir + "/law_T.bin", P.dir + "/law_V.bin", R, P.dir + "/g2.json"); ok2["data_b"] = P.data;
  const Json r2 = xeval::run(ok2);
  CHECK(same_bits(r1.at("pairs").at("4-AR-n200-r01").at("1").at("h2").num(), r2.at("pairs").at("4-AR-n200-r01").at("1").at("h2").num()));
  // refused: a different X (law B and its data.bin from another dataset, same n and p)
  Json bad = xargs(P.dir + "/law_V.bin", Q.dir + "/law_T.bin", P, P.dir + "/g3.json"); bad["data_b"] = Q.data;
  CHECK_THROWS(xeval::run(bad));
  // refused: --data-b is not the data.bin law B recorded
  Json wrong = xargs(P.dir + "/law_V.bin", R.dir + "/law_T.bin", P, P.dir + "/g4.json"); wrong["data_b"] = P.data;
  CHECK_THROWS(xeval::run(wrong));
  // refused: the recorded whole-file hashes differ and no data files are given (identity cannot be shown)
  CHECK_THROWS(xeval::run(xargs(P.dir + "/law_V.bin", R.dir + "/law_T.bin", P, P.dir + "/g5.json", false)));
  // --data-b without --data / with --b-truth is an argument error
  Json nb = xargs(P.dir + "/law_V.bin", "", P, P.dir + "/g6.json"); nb["data_b"] = R.data;
  CHECK_THROWS(xeval::run(nb));
}

TEST(xeval_command_record_layout_and_pairing) {
  const Prep P = make_prep(4242, "d1"), Q = make_prep(777, "d2");
  write_store_law(P, 150, P.dir + "/law_V.bin"); write_store_law(P, 60, P.dir + "/law_T.bin"); write_store_law(Q, 60, Q.dir + "/law_T.bin");
  const Json ab = xeval::run(xargs(P.dir + "/law_V.bin", P.dir + "/law_T.bin", P, P.dir + "/c1.json"));
  const Json ba = xeval::run(xargs(P.dir + "/law_T.bin", P.dir + "/law_V.bin", P, P.dir + "/c2.json"));
  CHECK(ab.at("schema").str() == "overlap1e4.cross_vt/1" && ab.at("status").str() == "completed");
  const Json& cell = ab.at("pairs").at("4-AR-n200-r01").at("1");   // exactly what compare_overlap.py load_cross reads: pairs[dataset][seed].h2
  const double h2 = cell.at("h2").num();
  std::printf("    CLI h2(V,T) = %.12g, h2(T,V) = %.12g, se %.2e, tail comps %g\n", h2, ba.at("pairs").at("4-AR-n200-r01").at("1").at("h2").num(), cell.at("se").num(), ab.at("xeval").at("tail_components_a").num());
  CHECK(h2 > 0 && cell.at("se").num() >= 0);
  CHECK(!ab.at("xeval").at("exact_a").boolean());   // top_k = 20 < 150 models: the tail path is exercised
  CHECK(same_bits(h2, ba.at("pairs").at("4-AR-n200-r01").at("1").at("h2").num()));   // symmetric in the files (stream ids by content hash)
  // the library call with the same laws
  const Truth T = truth_from_json(read_json_file(P.truth));
  xeval::CrossOpts o; o.seed = (uint32_t)(T.seed & 0xffffffffu); o.n_x = 200; o.block_rows = 100; o.top_k = 20; o.tail_r = 30;
  std::string ha, hb;
  const Law la = post::to_eval_law(post::read_law(P.dir + "/law_V.bin", &ha), "A"), lb = post::to_eval_law(post::read_law(P.dir + "/law_T.bin", &hb), "B");
  const xeval::CrossResult r = hb < ha ? xeval::cross_h2(la, lb, T, o, 6, 2) : xeval::cross_h2(la, lb, T, o, 2, 6);
  CHECK(same_bits(r.h2, h2));
  // --b_truth equals the engine's d_H(A, f*) path and carries no pairs cell without --dataset
  Json jt = xargs(P.dir + "/law_V.bin", "", P, P.dir + "/c3.json");
  const Json bt = xeval::run(jt);
  const xeval::CrossResult rt = xeval::cross_h2(la, xeval::truth_law(T), T, o, 2, 6);
  CHECK(same_bits(bt.at("xeval").at("h2").num(), rt.h2));
  // pairing guard: laws on different data are refused; a --data of another dataset too
  CHECK_THROWS(xeval::run(xargs(P.dir + "/law_V.bin", Q.dir + "/law_T.bin", P, P.dir + "/c4.json")));
  CHECK_THROWS(xeval::run(xargs(P.dir + "/law_V.bin", P.dir + "/law_T.bin", Q, P.dir + "/c5.json")));
  // argument errors
  Json bad = Json::object(); bad["a"] = "x"; bad["truth"] = "y";
  CHECK_THROWS(xeval::run(bad));
}
