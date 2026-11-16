// store.cpp -- flat top-c store (INTERFACES §4.1).
#include "v4/store.h"
#include <algorithm>
#include <cstring>
#include <numeric>
#include "v4/status.h"

namespace v4 {

void Store::init(uint64_t c, Order o) {
  cap = c; ord = o; v.clear(); off.clear(); hash.clear(); len.clear(); pool.clear();
  compacted_ = true; full_ = false; since_compact_ = 0;
}

// core/cpp/v3_ledger.h:35-42 (TopCmp): a before b iff a.v > b.v; HPM order then smaller size; then lexicographic.
bool Store::better(double v1, ModelView S1, double v2, ModelView S2) const {
  if (v1 != v2) return v1 > v2;
  if (ord == Order::HPM && S1.k != S2.k) return S1.k < S2.k;
  return lex_less(S1, S2);
}

bool Store::would_enter(double value, ModelView S) const {
  if (cap == 0) return false;
  if (!full_) return true;
  size_t w = v.size() - 1;
  return better(value, S, v[w], model(w));
}

void Store::offer(double value, ModelView S, uint64_t h) {
  if (cap == 0) return;
  if (S.k > 65535) throw Error(Status::internal_error, "store: model too large");
  if (full_ && compacted_) {
    size_t w = v.size() - 1;
    if (!better(value, S, v[w], model(w))) return;   // not better than the worst of a full compacted store: never kept
  }
  v.push_back(value); hash.push_back(h); len.push_back((uint16_t)S.k); off.push_back(pool.size());
  pool.insert(pool.end(), S.begin(), S.end());
  compacted_ = false; ++since_compact_;
  if (since_compact_ >= std::max<uint64_t>(cap, 1024)) compact();
}

void Store::compact() {
  if (compacted_) { since_compact_ = 0; return; }
  const size_t m = v.size();
  std::vector<uint32_t> ix(m);
  std::iota(ix.begin(), ix.end(), 0u);
  std::sort(ix.begin(), ix.end(), [&](uint32_t a, uint32_t b) { return better(v[a], model(a), v[b], model(b)); });
  std::vector<double> nv; std::vector<uint64_t> noff, nh; std::vector<uint16_t> nl; std::vector<int32_t> np;
  nv.reserve(std::min<size_t>(m, cap)); noff.reserve(nv.capacity()); nh.reserve(nv.capacity()); nl.reserve(nv.capacity());
  for (size_t t = 0; t < m && nv.size() < cap; ++t) {
    uint32_t a = ix[t];
    // equal models have equal values, so after sorting duplicates are adjacent to the last kept entry
    if (!nv.empty() && nv.back() == v[a] && nh.back() == hash[a] &&
        same_model(ModelView(np.data() + noff.back(), nl.back()), model(a))) continue;
    nv.push_back(v[a]); nh.push_back(hash[a]); nl.push_back(len[a]); noff.push_back(np.size());
    np.insert(np.end(), pool.begin() + (ptrdiff_t)off[a], pool.begin() + (ptrdiff_t)(off[a] + len[a]));
  }
  v.swap(nv); off.swap(noff); hash.swap(nh); len.swap(nl); pool.swap(np);
  compacted_ = true; full_ = (v.size() == cap); since_compact_ = 0;
}

void Store::merge(const Store& o) {
  for (size_t i = 0; i < o.v.size(); ++i) offer(o.v[i], o.model(i), o.hash[i]);
  compact();
}

bool Store::check_invariants() const {
  if (!compacted_ || v.size() > cap) return false;
  for (size_t i = 1; i < v.size(); ++i)
    if (!better(v[i - 1], model(i - 1), v[i], model(i))) return false;   // strict => sorted and no duplicates
  return true;
}

uint64_t Store::content_hash() const {
  uint64_t x = 0x9E3779B97F4A7C15ULL ^ v.size();
  auto mix = [&](uint64_t a) { x ^= a; x = splitmix64(x); };
  for (size_t i = 0; i < v.size(); ++i) {
    uint64_t b; std::memcpy(&b, &v[i], 8); mix(b); mix(len[i]);
    for (int32_t j : model(i)) mix((uint64_t)(uint32_t)j);
  }
  return x;
}

}  // namespace v4
