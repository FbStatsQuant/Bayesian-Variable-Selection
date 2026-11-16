#include <algorithm>
#include <random>
#include "tk.h"
#include "v4/store.h"
#include "v3_ledger.h"   // core/cpp, unchanged: v3::TopStore is the reference
using namespace v4;

namespace {
struct Offer { double v; Model S; };
std::vector<Offer> random_offers(uint32_t seed, int n, int p, int vals) {
  std::mt19937_64 g(seed); std::vector<Offer> o;
  for (int i = 0; i < n; ++i) {
    int k = (int)(g() % 5); Model S;
    while ((int)S.size() < k) { int j = (int)(g() % p); if (!std::binary_search(S.begin(), S.end(), j)) sorted_insert(S, j); }
    // a model's value is a function of the model (as in the engine): hash of S mapped to a few levels -> many ties
    uint64_t h = 0x1234; for (int j : S) { h ^= (uint64_t)j * 0x9E3779B97F4A7C15ULL; h = splitmix64(h); }
    o.push_back({(double)(h % (uint64_t)vals) * 0.5, S});
  }
  return o;
}
std::vector<std::pair<double, Model>> dump(const Store& s) {
  std::vector<std::pair<double, Model>> d;
  for (size_t i = 0; i < s.size(); ++i) d.push_back({s.v[i], Model(s.model(i).begin(), s.model(i).end())});
  return d;
}
}  // namespace

TEST(store_equals_v3_topstore_any_order) {
  Zobrist z; z.init(40);
  for (Order ord : {Order::HPM, Order::LEX})
    for (uint64_t cap : {1ull, 7ull, 50ull, 5000ull}) {
      auto offers = random_offers(17 + (uint32_t)cap, 3000, 40, 9);
      v3::TopStore ref; ref.init(cap, ord == Order::HPM);
      for (auto& o : offers) ref.offer(o.v, std::vector<int>(o.S.begin(), o.S.end()));
      std::vector<std::pair<double, Model>> want;
      for (auto& e : ref.s) want.push_back({e.v, Model(e.S.begin(), e.S.end())});
      for (int perm = 0; perm < 3; ++perm) {
        std::mt19937_64 g(perm); if (perm) std::shuffle(offers.begin(), offers.end(), g);
        Store s(cap, ord);
        for (auto& o : offers) s.offer(o.v, o.S, z.hash(o.S));
        s.compact();
        CHECK(s.check_invariants());
        CHECK(dump(s) == want);
        // split into 3 stores, merge in two orders
        Store a(cap, ord), b(cap, ord), c(cap, ord);
        for (size_t i = 0; i < offers.size(); ++i) (i % 3 == 0 ? a : i % 3 == 1 ? b : c).offer(offers[i].v, offers[i].S, z.hash(offers[i].S));
        Store m1(cap, ord); m1.merge(a); m1.merge(b); m1.merge(c);
        Store m2(cap, ord); m2.merge(c); m2.merge(a); m2.merge(b);
        CHECK(dump(m1) == want); CHECK(dump(m2) == want); CHECK(m1.content_hash() == m2.content_hash());
      }
    }
}
TEST(store_cap_zero_and_would_enter) {
  Store s(0, Order::HPM); Model S{1, 2}; s.offer(1.0, S, 1); s.compact(); CHECK(s.size() == 0); CHECK(!s.would_enter(9, S));
  Store t(2, Order::HPM); t.offer(1.0, Model{1}, 1); t.offer(2.0, Model{2}, 2); t.compact();
  CHECK(t.would_enter(1.5, Model{3})); CHECK(!t.would_enter(0.5, Model{3}));
  CHECK(t.would_enter(1.0, Model{0}));                  // tie on F and size: lexicographically smaller enters
  CHECK(!t.would_enter(1.0, Model{0, 5}));              // tie on F: larger model is worse under the HPM order
  CHECK(t.better(1.0, Model{0}, 1.0, Model{1}));
}
