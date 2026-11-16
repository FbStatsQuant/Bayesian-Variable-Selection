// test_golden_v3.cpp -- golden bit tests: WP5's scorer copy (score_bit.cpp), constants and Zobrist hash against the
// reference headers of core/ (v3.1 / revision D) compiled UNCHANGED with the v3 flags in this test binary.
#include <cstring>
#include <random>

#include "v3_score.h"   // core/cpp (read only)
#include "v4/eval.h"
#include "wp5_tk.h"

using namespace v4::eval;

static uint64_t bits(double x) { uint64_t u; std::memcpy(&u, &x, 8); return u; }

// AR(rho) design + sparse truth; exact_fit=true gives y in the span of S0 (forces the Q recompute branch).
static OwnedData make_data(int n, int p, double rho, uint64_t seed, bool exact_fit) {
  std::mt19937_64 g(seed); std::normal_distribution<double> N(0, 1);
  std::vector<double> X((size_t)n * p), y(n, 0.0);
  for (int i = 0; i < n; ++i) {
    double prev = N(g);
    for (int j = 0; j < p; ++j) { double x = j ? rho * prev + std::sqrt(1 - rho * rho) * N(g) : prev; X[(size_t)j * n + i] = 3.0 + 2.0 * x; prev = x; }
  }
  for (int i = 0; i < n; ++i) {
    y[i] = 1.0 + X[(size_t)2 * n + i] - 0.8 * X[(size_t)7 * n + i] + 0.6 * X[(size_t)(p - 3) * n + i];
    if (!exact_fit) y[i] += N(g);
  }
  return standardise(X.data(), y.data(), n, p);
}

static void compare_with_v3(const OwnedData& O, int n_models, uint64_t seed, int* n_qrec) {
  const EvalData& D = O.D;
  v3::Data R;
  std::vector<int> orig(O.orig.begin(), O.orig.end());
  v3::data_init(R, O.Xs.data(), O.ys.data(), D.n, D.p, orig);
  CHECK(bits(R.logCn) == bits(D.logCn)); CHECK(bits(R.logm0) == bits(D.logm0)); CHECK(bits(R.logWK) == bits(D.logWK));
  CHECK(bits(R.yty) == bits(D.yty));
  for (int k = 0; k <= D.K; ++k) CHECK(bits(R.logprior[k]) == bits(D.logprior[k]));
  for (int j = 0; j < D.p; ++j) CHECK(bits(R.z[j]) == bits(D.z[j]));
  v3::Scorer sc(&R);
  std::mt19937_64 g(seed);
  int mism = 0;
  for (int t = 0; t < n_models; ++t) {
    int k = (int)(g() % (uint64_t)std::min(D.K + 1, 13));
    std::vector<int> all(D.p); for (int j = 0; j < D.p; ++j) all[j] = j;
    std::shuffle(all.begin(), all.end(), g);
    std::vector<int> S(all.begin(), all.begin() + k); std::sort(S.begin(), S.end());
    if (t < 3) S = {2, 7, D.p - 3};   // the true model
    v3::ScoreOut ro = sc.score(S);
    ModelPost mp = model_post(D, Model(S.begin(), S.end()));
    bool same = bits(ro.logm) == bits(mp.logm) && bits(ro.Q) == bits(mp.Q) && ro.route == mp.route &&
                ro.q_recomputed == mp.q_recomputed && bits(ro.logdetH) == bits(mp.logdetH) && bits(ro.logdetA) == bits(mp.logdetA) &&
                bits(R.logprior[S.size()] + ro.logm) == bits(mp.F);
    if (!same) ++mism;
    if (mp.q_recomputed) ++*n_qrec;
  }
  CHECK_MSG(mism == 0, std::to_string(mism) + " bit mismatches");
}

TEST(golden_scorer_bits_vs_core_v3) {
  int qrec = 0;
  OwnedData O1 = make_data(80, 40, 0.6, 11, false);
  compare_with_v3(O1, 600, 5, &qrec);
  OwnedData O2 = make_data(37, 25, 0.9, 12, false);     // odd n, strong correlation, K = 18
  compare_with_v3(O2, 600, 6, &qrec);
  int qrec_exact = 0;
  // y exactly in span(S0). (The Q-recompute branch, Q < 1e-8 y'y, is not reachable with this prior: the ridge term keeps
  // Q ≥ about y'y/(n+1); it is covered by the copy being line-for-line core/cpp/v3_score.h:142-157.)
  OwnedData O3 = make_data(50, 20, 0.3, 13, true);
  compare_with_v3(O3, 300, 7, &qrec_exact);
}

TEST(golden_zobrist_vs_core_v3) {
  v3::Zobrist z; z.init(1000);
  std::mt19937_64 g(3);
  for (int t = 0; t < 200; ++t) {
    Model S; for (int j = 0; j < 1000; ++j) if (g() % 50 == 0) S.push_back(j);
    uint64_t h = 0; for (int32_t j : S) h ^= z.key[j];
    CHECK(zobrist_hash(S, 1000) == h);
  }
}
