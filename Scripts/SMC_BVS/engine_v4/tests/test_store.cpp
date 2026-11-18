#include <algorithm>
#include <map>
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

TEST(store_cutoff_monotone_and_exact) {
  Zobrist z; z.init(40);
  auto offers = random_offers(3, 20000, 40, 50);
  Store s(100, Order::HPM); double last = s.cutoff();
  CHECK(last == -__builtin_huge_val());
  for (size_t i = 0; i < offers.size(); ++i) {
    s.offer(offers[i].v, offers[i].S, z.hash(offers[i].S));
    if (i % 997 == 0) { s.compact(); CHECK(s.cutoff() >= last); last = s.cutoff(); }
  }
  s.compact();
  CHECK(s.check_invariants() && s.size() == 100 && s.cutoff() == s.v.back());
  // exactness: the same top-c as the reference with no quick rejects at all
  v3::TopStore ref; ref.init(100, true);
  for (auto& o : offers) ref.offer(o.v, std::vector<int>(o.S.begin(), o.S.end()));
  std::vector<std::pair<double, Model>> want;
  for (auto& e : ref.s) want.push_back({e.v, Model(e.S.begin(), e.S.end())});
  CHECK(dump(s) == want);
}

// INTERFACES §4.1 (v0.1.13, R7): class-A values are path-dependent maxima, so one model may be offered with different
// values. The store keeps each model once, with its best value; content = top-c of distinct models by best value,
// independent of offer order, splitting and merge order (the WP4 merge of island stores relies on it).
TEST(store_one_entry_per_model_best_value) {
  Zobrist z; z.init(30);
  std::mt19937_64 g(5);
  std::vector<Offer> offers;
  for (int i = 0; i < 6000; ++i) {
    Model S; int k = (int)(g() % 4);
    while ((int)S.size() < k) { int j = (int)(g() % 30); if (!std::binary_search(S.begin(), S.end(), j)) sorted_insert(S, j); }
    offers.push_back({(double)(g() % 40) * 0.25, S});   // same model, many different values
  }
  for (Order ord : {Order::HPM, Order::LEX})
    for (uint64_t cap : {1ull, 9ull, 120ull, 100000ull}) {
      // reference: best value per model, then the strict order, then the first cap
      std::map<Model, double> best;
      for (auto& o : offers) { auto it = best.find(o.S); if (it == best.end() || o.v > it->second) best[o.S] = o.v; }
      Store tmp(1, ord);
      std::vector<std::pair<double, Model>> all;
      for (auto& [S, v] : best) all.push_back({v, S});
      std::sort(all.begin(), all.end(), [&](auto& a, auto& b) { return tmp.better(a.first, a.second, b.first, b.second); });
      if (all.size() > cap) all.resize(cap);
      for (int perm = 0; perm < 3; ++perm) {
        std::mt19937_64 gp(100 + perm); if (perm) std::shuffle(offers.begin(), offers.end(), gp);
        Store s(cap, ord);
        for (auto& o : offers) s.offer(o.v, o.S, z.hash(o.S));
        s.compact();
        CHECK(s.check_invariants()); CHECK(dump(s) == all);
        Store a(cap, ord), b(cap, ord), c(cap, ord);   // per-"island" stores, merged in two orders
        for (size_t i = 0; i < offers.size(); ++i) (i % 3 == 0 ? a : i % 3 == 1 ? b : c).offer(offers[i].v, offers[i].S, z.hash(offers[i].S));
        Store m1(cap, ord); m1.merge(a); m1.merge(b); m1.merge(c);
        Store m2(cap, ord); m2.merge(c); m2.merge(b); m2.merge(a);
        CHECK(dump(m1) == all); CHECK(dump(m2) == all); CHECK(m1.check_invariants());
      }
    }
}

// PR40 review follow-up: the bulk loader gives the same content (bits) as offer + compact, verifies its input, and the
// stronger check_invariants catches a duplicated model (the old check did not).
TEST(store_bulk_load_equals_offer_path_and_verifies) {
  Zobrist z; z.init(40);
  auto offers = random_offers(21, 5000, 40, 30);
  for (Order ord : {Order::HPM, Order::LEX})
    for (uint64_t cap : {1ull, 50ull, 400ull, 100000ull}) {
      Store src(cap, ord);
      for (auto& o : offers) src.offer(o.v, o.S, z.hash(o.S));
      src.compact();
      Store b(cap, ord);
      b.load_unique_sorted(src.size(), src.v.data(), src.hash.data(), src.off.data(), src.len.data(), src.pool.data(), src.pool.size());
      CHECK(b.check_invariants()); CHECK(b.content_hash() == src.content_hash()); CHECK(same_bits(b.cutoff(), src.cutoff()));
      // a loaded store keeps working: later offers and merges equal the offer-only path
      Store b2 = b, s2 = src;
      for (size_t i = 0; i < 300; ++i) { b2.offer(offers[i].v + 0.125, offers[i].S, z.hash(offers[i].S)); s2.offer(offers[i].v + 0.125, offers[i].S, z.hash(offers[i].S)); }
      b2.compact(); s2.compact();
      CHECK(b2.content_hash() == s2.content_hash() && b2.check_invariants());
      if (src.size() >= 3) {   // corrupt inputs are refused
        std::vector<double> vv = src.v; std::swap(vv[0], vv[1]);
        Store e(cap, ord);
        if (vv[0] != vv[1]) CHECK_THROWS(e.load_unique_sorted(src.size(), vv.data(), src.hash.data(), src.off.data(), src.len.data(), src.pool.data(), src.pool.size()));
        std::vector<uint64_t> oo = src.off; oo[2] = src.pool.size() + 5;
        Store e2(cap, ord);
        CHECK_THROWS(e2.load_unique_sorted(src.size(), src.v.data(), src.hash.data(), oo.data(), src.len.data(), src.pool.data(), src.pool.size()));
      }
      Store full(cap, ord); full.offer(1.0, Model{1}, z.hash(Model{1}));
      CHECK_THROWS(full.load_unique_sorted(src.size(), src.v.data(), src.hash.data(), src.off.data(), src.len.data(), src.pool.data(), src.pool.size()));
    }
  // the same model twice, at two values (strictly sorted, so the old sorted-only check passed): refused and detected
  Model S{3, 9}; uint64_t h = z.hash(S);
  std::vector<double> v = {2.0, 1.5}; std::vector<uint64_t> hh = {h, h}, off = {0, 2}; std::vector<uint16_t> len = {2, 2};
  std::vector<int32_t> pool = {3, 9, 3, 9};
  Store d(10, Order::HPM);
  CHECK_THROWS(d.load_unique_sorted(2, v.data(), hh.data(), off.data(), len.data(), pool.data(), pool.size()));
  CHECK(d.size() == 0);
}
