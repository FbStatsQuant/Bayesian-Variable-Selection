// Golden bit test: Scorer<Arith::Bit> (Gram-free) against v3::Scorer (core/cpp/v3_score.h compiled unchanged with the
// v3 flags, stored Gram). Every route (chol, refactor, QR) and the non-negative-Q path are exercised.
#include <random>
#include "tk.h"
#include "tutil.h"
#include "v4/score.h"
#include "v3_score.h"
using namespace v4;

namespace {
struct Pair { Data D; v3::Data R; };
// v3 context on the same standardised X, y (orig 1..p)
void v3_ctx(const Data& D, v3::Data& R) {
  std::vector<int> orig(D.p); for (int j = 0; j < D.p; ++j) orig[j] = D.orig[j];
  v3::data_init(R, D.Xs, D.ys, D.n, D.p, orig);
}
int compare_models(const Data& D, const v3::Data& R, const std::vector<Model>& models, int* routes_seen) {
  BitScorer a(&D); v3::Scorer b(&R);
  int bad = 0;
  for (auto& S : models) {
    std::vector<int> s(S.begin(), S.end());
    ScoreOut x; v3::ScoreOut y; bool ta = false, tb = false;
    try { x = a.score(S); } catch (NumericalFailure&) { ta = true; }
    try { y = b.score(s); } catch (v3::NumericalFailure&) { tb = true; }
    if (ta != tb) { ++bad; continue; }
    if (ta) continue;
    if (!same_bits(x.logm, y.logm) || !same_bits(x.Q, y.Q) || x.route != y.route || x.q_recomputed != y.q_recomputed ||
        !same_bits(x.logdetH, y.logdetH) || !same_bits(x.logdetA, y.logdetA) || !same_bits(x.cond_H, y.cond_H)) ++bad;
    if (routes_seen) routes_seen[x.route]++;
  }
  return bad;
}
std::vector<Model> random_models(const Data& D, uint32_t seed, int count, int kmax) {
  std::mt19937_64 g(seed); std::vector<Model> out;
  for (int c = 0; c < count; ++c) {
    int k = (int)(g() % (uint64_t)(std::min(kmax, D.K) + 1)); Model S;
    while ((int)S.size() < k) { int j = (int)(g() % (uint64_t)D.p); if (!std::binary_search(S.begin(), S.end(), j)) sorted_insert(S, j); }
    out.push_back(S);
  }
  return out;
}
}  // namespace

TEST(constants_equal_v3) {
  for (auto d : {gen::Design::AR, gen::Design::IND}) {
    Data D = make_test_data(d, 120, 300, 11);
    v3::Data R; v3_ctx(D, R);
    CHECK(same_bits(D.logCn, R.logCn) && same_bits(D.logm0, R.logm0) && same_bits(D.logWK, R.logWK) && same_bits(D.yty, R.yty) && D.K == R.K);
    bool ok = true;
    for (int k = 0; k <= D.K; ++k) ok = ok && same_bits(D.logprior[k], R.logprior[k]) && same_bits(D.logw[k], R.logw[k]);
    for (int j = 0; j < D.p; ++j) ok = ok && same_bits(D.z[j], R.z[j]) && same_bits(D.diagG[j], R.Gat(j, j)) && D.zob.key[j] == R.zob.key[j];
    for (int a = 0; a < 50; ++a) for (int b = 0; b < D.p; b += 7) ok = ok && same_bits(gram(D, a, b), R.Gat(a, b));
    CHECK(ok);
  }
}
TEST(score_bits_equal_v3_random_models) {
  int routes[3] = {0, 0, 0};
  for (auto d : {gen::Design::AR, gen::Design::IND, gen::Design::BLK, gen::Design::ADJOPP}) {
    Data D = make_test_data(d, 200, 1000, 21);
    v3::Data R; v3_ctx(D, R);
    CHECK_EQ(compare_models(D, R, random_models(D, 3, 3000, 12), routes), 0);
  }
  // n = 30: K = 15, models up to K (ill-conditioned at large k)
  Data D = make_test_data(gen::Design::AR, 30, 200, 5);
  v3::Data R; v3_ctx(D, R);
  CHECK_EQ(compare_models(D, R, random_models(D, 9, 3000, D.K), routes), 0);
  CHECK(routes[0] > 0);
}
TEST(score_bits_equal_v3_fallback_routes) {
  // duplicated / collinear columns force the refactor and QR routes; y in span(X) forces the non-negative Q.
  const int n = 40, p = 12;
  gen::Spec s; s.design = gen::Design::IND; s.n = n; s.p = p; s.seed = 3; s.a = 0;
  std::vector<double> X, y; gen::generate(s, X, y);
  for (int i = 0; i < n; ++i) { X[(size_t)1 * n + i] = X[(size_t)0 * n + i] * (1 + 1e-15); X[(size_t)2 * n + i] = X[i] + 1e-13 * X[(size_t)3 * n + i];
                                X[(size_t)5 * n + i] = 2 * X[(size_t)4 * n + i] - X[(size_t)6 * n + i]; }
  for (int i = 0; i < n; ++i) y[i] = X[(size_t)7 * n + i] - 0.5 * X[(size_t)8 * n + i];   // exact fit by {7, 8}
  prep::Result r = prep::preprocess(X.data(), y.data(), n, p);
  Data D = make_data(r.own, n, r.p);
  v3::Data R; v3_ctx(D, R);
  std::vector<Model> ms = {{}, {0}, {0, 1}, {0, 2}, {0, 1, 2}, {4, 5, 6}, {0, 1, 4, 5, 6}, {7, 8}, {7, 8, 9}, {0, 7, 8}, {1, 2, 3}};
  for (int a = 0; a < p; ++a) for (int b = a + 1; b < p; ++b) ms.push_back({a, b});
  int routes[3] = {0, 0, 0};
  CHECK_EQ(compare_models(D, R, ms, routes), 0);
  std::printf("    routes seen by score(): chol %d refactor %d qr %d\n", routes[0], routes[1], routes[2]);
  // On standardised data H = (n+1)G_S + I and A = G_S + I have eigenvalues >= 1, so the Cholesky route practically never
  // fails, and Q >= y'y/(n+1) >> 1e-8 y'y. Each route is therefore also compared directly (forced), including the
  // non-negative Q helper.
  BitScorer sc(&D); v3::Scorer ref(&R);
  int bad = 0, n_route = 0;
  for (auto& S : ms) {
    std::vector<int> s3(S.begin(), S.end());
    for (int route = 0; route < 3; ++route) {
      ScoreOut x; v3::ScoreOut y; std::vector<double> LH;
      bool okx = sc.score_route(S, route, x);
      bool oky = route == 2 ? ref.try_qr(s3, y, LH) : ref.try_chol(s3, route == 1, y, LH);
      if (okx != oky || (okx && (!same_bits(x.logm, y.logm) || !same_bits(x.Q, y.Q) || !same_bits(x.logdetA, y.logdetA)))) ++bad;
      ++n_route;
    }
    if (!S.empty()) {
      v3::ScoreOut y; std::vector<double> LH;
      if (!ref.try_chol(s3, false, y, LH) || !same_bits(sc.q_nonneg_after_chol(S), ref.q_nonneg(s3, LH))) ++bad;
    }
  }
  CHECK_EQ(bad, 0);
  // non-finite data: every route fails on both sides -> NumericalFailure on both sides
  auto own = std::make_shared<DataOwned>(*std::static_pointer_cast<const DataOwned>(D.keep));
  own->X[3] = NAN;
  Data Dn = D; Dn.Xs = own->X.data(); Dn.keep = own;
  v3::Data Rn; v3_ctx(Dn, Rn);
  BitScorer sn(&Dn); v3::Scorer rn(&Rn);
  bool t1 = false, t2 = false;
  try { sn.score(Model{0, 1}); } catch (NumericalFailure&) { t1 = true; }
  try { rn.score(std::vector<int>{0, 1}); } catch (v3::NumericalFailure&) { t2 = true; }
  CHECK(t1 && t2);
  std::printf("    forced-route comparisons: %d (0 mismatches required)\n", n_route);
}
TEST(flip_scores_equal_scores) {
  Data D = make_test_data(gen::Design::AR, 100, 400, 8);
  BitScorer sc(&D);
  Model S = {3, 50, 51, 200};
  std::vector<int32_t> labels; for (int j = 0; j < D.p; ++j) labels.push_back(j);
  std::vector<double> lm(labels.size()); std::vector<int8_t> rt(labels.size());
  sc.flip_scores(S, labels.data(), labels.size(), lm.data(), rt.data());
  bool ok = true;
  for (size_t t = 0; t < labels.size(); ++t) {
    Model T = S; auto it = std::lower_bound(T.begin(), T.end(), labels[t]);
    if (it != T.end() && *it == labels[t]) T.erase(it); else T.insert(it, labels[t]);
    ok = ok && same_bits(sc.score(T).logm, lm[t]);
  }
  CHECK(ok);
  Model big; for (int j = 0; j <= D.K; ++j) big.push_back(j);
  CHECK_THROWS(sc.score(big));   // |S| > K -> internal_error (callers never pass these)
}
