// test_list_pip.cpp -- list-renormalised PIP fields (SPEC_LIST_PIP.md §7, tests B4-B11 on the function the merge calls; the merge
// end-to-end, the fit.bin sections and the `listpip` tool are in test_wp4_io.cpp; v3 against v4 (B12) is in tests/golden/wp4_golden.R).
#include <algorithm>
#include <cmath>
#include <limits>
#include <random>
#include <set>
#include "tk.h"
#include "v4/list_pip.h"
#include "v4/pmath.h"
using namespace v4;

namespace {
// A compacted store holding the given models (distinct) with the given scores, in the engine's HPM order.
Store make_store(const std::vector<Model>& ms, const std::vector<double>& F, int p, uint64_t cap = 0) {
  Zobrist z; z.init(p);
  Store s(cap ? cap : (uint64_t)ms.size() + 8, Order::HPM);
  for (size_t i = 0; i < ms.size(); ++i) s.offer(F[i], ms[i], z.hash(ms[i]));
  s.compact();
  return s;
}
// a raw (unsorted) list, to exercise the cases a valid Store cannot hold (NaN, duplicates, order)
struct Raw {
  std::vector<double> v; std::vector<uint64_t> off, hash; std::vector<uint16_t> len; std::vector<int32_t> pool;
  Raw(const std::vector<Model>& ms, const std::vector<double>& F, int p) {
    Zobrist z; z.init(p); v = F;
    for (auto& m : ms) { off.push_back(pool.size()); len.push_back((uint16_t)m.size()); hash.push_back(z.hash(m)); pool.insert(pool.end(), m.begin(), m.end()); }
  }
  ListPipSrc src() const { ListPipSrc s; s.n = v.size(); s.v = v.data(); s.off = off.data(); s.len = len.data(); s.hash = hash.data(); s.pool = pool.data(); return s; }
};
bool near(const std::vector<double>& a, const std::vector<double>& b, double tol) {
  if (a.size() != b.size()) return false;
  for (size_t i = 0; i < a.size(); ++i) if (!(std::fabs(a[i] - b[i]) <= tol)) return false;
  return true;
}
}  // namespace

TEST(listpip_b4_hand_case_and_shift_invariance) {
  // store {1}, {1,2}, {3} (1-based in the spec; 0-based here: {0}, {0,1}, {2}) with scores c + log .5, .3, .2
  for (double c : {0.0, 1000.0, -1000.0}) {
    Store s = make_store({{0}, {0, 1}, {2}}, {c + std::log(.5), c + std::log(.3), c + std::log(.2)}, 3);
    ListPip r = compute_list_pip(s, 3);
    CHECK(near(r.pip_list, {.8, .3, .2}, 1e-12));
    CHECK(r.mpm_list == std::vector<int32_t>{0});
    CHECK(std::fabs(r.log_Z_list - c) <= 1e-12 * std::max(1.0, std::fabs(c)));
    CHECK(r.flag.empty() && r.list_size == 3 && !r.list_full && r.source == "store");
  }
}
TEST(listpip_b5_single_model) {
  Store s = make_store({{1, 4}}, {3.25}, 6);
  ListPip r = compute_list_pip(s, 6);
  CHECK(r.pip_list == std::vector<double>({0, 1, 0, 0, 1, 0}));
  CHECK((r.mpm_list == std::vector<int32_t>{1, 4}) && r.log_Z_list == 3.25);
}
TEST(listpip_b6_empty_model_and_tie_at_half) {
  Store s = make_store({{}, {0}}, {0.0, 0.0}, 2);
  ListPip r = compute_list_pip(s, 2);
  CHECK(r.pip_list == std::vector<double>({.5, 0}));   // exactly .5: strict rule leaves it out of mpm_list
  CHECK(r.mpm_list.empty() && std::fabs(r.log_Z_list - std::log(2.0)) <= 1e-15);
}
TEST(listpip_b7_scores_800_apart) {
  Store s = make_store({{0, 2}, {1}}, {0.0, -800.0}, 3);
  ListPip r = compute_list_pip(s, 3);
  bool fin = true; for (double x : r.pip_list) fin = fin && std::isfinite(x);
  CHECK(fin && near(r.pip_list, {1, 0, 1}, 1e-12) && r.log_Z_list == 0.0);
}
TEST(listpip_cases_of_section_4) {
  const double NaN = std::numeric_limits<double>::quiet_NaN(), Inf = std::numeric_limits<double>::infinity();
  { Raw w({{0}, {1}}, {-Inf, -3.0}, 3); ListPip r = compute_list_pip(w.src(), 3, 41);   // -Inf: weight 0
    CHECK(r.pip_list == std::vector<double>({0, 1, 0}) && r.log_Z_list == -3.0 && r.flag.empty()); }
  { Raw w({{0}, {1}}, {NaN, 1.0}, 3); ListPip r = compute_list_pip(w.src(), 3, 41);
    CHECK(r.flag == "nonfinite_score" && std::isnan(r.log_Z_list) && r.mpm_list.empty() && r.pip_list.size() == 3 && std::isnan(r.pip_list[0])); }
  { Raw w({{0}, {1}}, {Inf, 1.0}, 3); CHECK(compute_list_pip(w.src(), 3, 41).flag == "nonfinite_score"); }
  { Raw w({{0}, {1}}, {-Inf, -Inf}, 3); CHECK(compute_list_pip(w.src(), 3, 41).flag == "nonfinite_score"); }
  { Raw w({}, {}, 3); ListPip r = compute_list_pip(w.src(), 3, 41); CHECK(r.flag == "empty_list" && r.list_size == 0 && std::isnan(r.log_Z_list) && r.pip_list.size() == 3); }
  { Raw w({{0}, {1}, {0}}, {0.0, -1.0, -2.0}, 3); CHECK_THROWS(compute_list_pip(w.src(), 3, 41)); }   // a duplicate model: an error, never merged
  { Raw w({{0}, {5}}, {0.0, -1.0}, 3); CHECK_THROWS(compute_list_pip(w.src(), 3, 41)); }              // a column outside [0, p)
  { Store s = make_store({{}}, {-7.0}, 2); ListPip r = compute_list_pip(s, 2);                          // the empty model alone
    CHECK(r.pip_list == std::vector<double>({0, 0}) && r.mpm_list.empty() && r.log_Z_list == -7.0); }
  { Store s = make_store({{0}, {0, 1}}, {0.0, -1.0}, 3, 2); ListPip r = compute_list_pip(s, 3);       // full store; in every / in no listed model
    CHECK(r.list_full && r.pip_list[0] == 1.0 && r.pip_list[2] == 0.0 && r.list_size == 2); }
}
TEST(listpip_summation_is_plain_double_last_to_first) {
  // an independent re-implementation of §2/§3 (explicit loops, std::exp = pm::exp), bit for bit
  std::mt19937_64 g(7); std::exponential_distribution<double> E(1.0 / 5.0);
  const int p = 30; std::set<Model> seen; std::vector<Model> ms; std::vector<double> F;
  while (ms.size() < 2000) {
    Model S; int k = (int)(g() % 6); while ((int)S.size() < k) { int j = (int)(g() % p); if (!std::binary_search(S.begin(), S.end(), j)) sorted_insert(S, j); }
    if (!seen.insert(S).second) continue;
    ms.push_back(S); F.push_back(-E(g));
  }
  Store s = make_store(ms, F, p, 5000);
  ListPip r = compute_list_pip(s, p);
  double Fmax = s.v[0]; for (double x : s.v) Fmax = std::max(Fmax, x);
  std::vector<double> num(p, 0.0); double den = 0.0;
  for (size_t i = s.size(); i-- > 0;) { double u = std::exp(s.v[i] - Fmax); den += u; for (int32_t j : s.model(i)) num[j] += u; }
  bool same = true; for (int j = 0; j < p; ++j) same = same && same_bits(r.pip_list[j], num[j] / den);
  CHECK(same);
  CHECK(same_bits(r.log_Z_list, Fmax + std::log(den)));
  // B10: bounds, support bound, permutation of the entries
  bool bnd = true; for (double x : r.pip_list) bnd = bnd && x >= 0 && x <= 1;
  CHECK(bnd);
  const double w1 = std::exp(s.v[0] - Fmax) / den; double mx = 0;
  for (int j = 0; j < p; ++j) { const bool in = std::binary_search(s.model(0).begin(), s.model(0).end(), j); mx = std::max(mx, std::fabs(r.pip_list[j] - (in ? 1.0 : 0.0))); }
  CHECK(mx <= 1 - w1 + 1e-12);
  { std::vector<size_t> ord(ms.size()); for (size_t i = 0; i < ord.size(); ++i) ord[i] = i;
    std::shuffle(ord.begin(), ord.end(), g);
    std::vector<Model> m2; std::vector<double> F2; for (size_t i : ord) { m2.push_back(ms[i]); F2.push_back(F[i]); }
    Raw w2(m2, F2, p); ListPip r2 = compute_list_pip(w2.src(), p, 5000);
    CHECK(near(r2.pip_list, r.pip_list, 1e-12) && std::fabs(r2.log_Z_list - r.log_Z_list) <= 1e-12); }
}
TEST(listpip_deterministic_and_offer_order_free) {
  // the store is the top-c of everything offered, independent of the order: same fields, bit for bit
  std::mt19937_64 g(3); const int p = 20; Zobrist z; z.init(p);
  std::vector<std::pair<double, Model>> offers;
  for (int i = 0; i < 4000; ++i) { Model S; int k = (int)(g() % 5); while ((int)S.size() < k) { int j = (int)(g() % p); if (!std::binary_search(S.begin(), S.end(), j)) sorted_insert(S, j); }
    uint64_t h = z.hash(S); offers.push_back({-(double)(h % 1000) * 0.01, S}); }
  auto build = [&](bool shuffle) { auto o = offers; if (shuffle) std::shuffle(o.begin(), o.end(), g);
    Store s(100, Order::HPM); for (auto& x : o) s.offer(x.first, x.second, z.hash(x.second)); s.compact(); return compute_list_pip(s, p); };
  ListPip a = build(false), b = build(true), c = build(false);
  bool same = a.list_size == b.list_size && same_bits(a.log_Z_list, b.log_Z_list) && same_bits(a.log_Z_list, c.log_Z_list) && a.mpm_list == b.mpm_list;
  for (int j = 0; j < p; ++j) same = same && same_bits(a.pip_list[j], b.pip_list[j]) && same_bits(a.pip_list[j], c.pip_list[j]);
  CHECK(same); CHECK(a.list_full);
}
