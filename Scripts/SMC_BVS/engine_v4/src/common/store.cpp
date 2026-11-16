// store.cpp -- flat top-c store (INTERFACES §4.1).
#include "v4/store.h"
#include <algorithm>
#include <cstring>
#include <numeric>
#include "v4/status.h"

namespace v4 {

Store& Store::operator=(const Store& o) {
  if (this == &o) return *this;
  cap = o.cap; ord = o.ord; v = o.v; off = o.off; hash = o.hash; len = o.len; pool = o.pool; nkept_ = o.nkept_;
  cut_.store(o.cut_.load(std::memory_order_relaxed), std::memory_order_relaxed);
  return *this;
}

void Store::init(uint64_t c, Order o) {
  cap = c; ord = o; v.clear(); off.clear(); hash.clear(); len.clear(); pool.clear(); nkept_ = 0;
  cut_.store(-__builtin_huge_val(), std::memory_order_relaxed);
}

// core/cpp/v3_ledger.h:35-42 (TopCmp): a before b iff a.v > b.v; HPM order then smaller size; then lexicographic.
bool Store::better(double v1, ModelView S1, double v2, ModelView S2) const {
  if (v1 != v2) return v1 > v2;
  if (ord == Order::HPM && S1.k != S2.k) return S1.k < S2.k;
  return lex_less(S1, S2);
}

bool Store::would_enter(double value, ModelView S) const {
  if (cap == 0) return false;
  if (nkept_ < cap) return true;
  return better(value, S, v[nkept_ - 1], model(nkept_ - 1));
}

void Store::offer(double value, ModelView S, uint64_t h) {
  if (cap == 0) return;
  if (value < cutoff()) return;                            // strictly worse than c entries already offered
  if (nkept_ == cap && !better(value, S, v[nkept_ - 1], model(nkept_ - 1))) return;   // not better than the worst kept
  if (S.k > 65535) throw Error(Status::internal_error, "store: model too large");
  v.push_back(value); hash.push_back(h); len.push_back((uint16_t)S.k); off.push_back(pool.size());
  pool.insert(pool.end(), S.begin(), S.end());
  if (staging() >= trigger()) compact();
}

void Store::compact() {
  const size_t m = v.size(), ns = m - nkept_;
  if (ns == 0) return;
  // 1. sort the staging run (index permutation)
  std::vector<uint32_t> st(ns);
  std::iota(st.begin(), st.end(), (uint32_t)nkept_);
  std::sort(st.begin(), st.end(), [&](uint32_t a, uint32_t b) { return better(v[a], model(a), v[b], model(b)); });
  // 2. merge with the kept run [0, nkept_), dropping exact duplicates (equal models compare equal, so they are adjacent)
  std::vector<uint32_t> sel; sel.reserve(std::min<size_t>(cap, m));
  size_t i = 0, j = 0; uint64_t pool_need = 0;
  auto same_as_last = [&](uint32_t a) {
    if (sel.empty()) return false;
    uint32_t b = sel.back();
    return v[a] == v[b] && hash[a] == hash[b] && same_model(model(a), model(b));
  };
  while (sel.size() < cap && (i < nkept_ || j < ns)) {
    uint32_t a;
    if (j >= ns || (i < nkept_ && !better(v[st[j]], model(st[j]), v[i], model(i)))) a = (uint32_t)i++;
    else a = st[j++];
    if (same_as_last(a)) continue;
    sel.push_back(a); pool_need += len[a];
  }
  st.clear(); st.shrink_to_fit();
  // 3. build the new kept run; reserve room for the next staging run too, so appends never reallocate geometrically
  //    (peak during compact: old kept + staging, and new kept + room for staging: about 2.5 c entries)
  const size_t room = sel.size() + (size_t)std::min<uint64_t>(trigger(), cap);
  const size_t avg_len = sel.empty() ? 8 : (size_t)(pool_need / sel.size()) + 1;
  std::vector<double> nv; std::vector<uint64_t> noff, nh; std::vector<uint16_t> nl; std::vector<int32_t> np;
  nv.reserve(room); noff.reserve(room); nh.reserve(room); nl.reserve(room); np.reserve(pool_need + (room - sel.size()) * avg_len);
  for (uint32_t a : sel) {
    nv.push_back(v[a]); nh.push_back(hash[a]); nl.push_back(len[a]); noff.push_back(np.size());
    np.insert(np.end(), pool.begin() + (ptrdiff_t)off[a], pool.begin() + (ptrdiff_t)(off[a] + len[a]));
  }
  v.swap(nv); off.swap(noff); hash.swap(nh); len.swap(nl); pool.swap(np);
  nkept_ = v.size();
  if (nkept_ == cap && cap > 0) {
    double w = v[nkept_ - 1], old = cutoff();
    if (w > old) cut_.store(w, std::memory_order_relaxed);   // monotone by construction; never lowered
  }
}

void Store::merge(const Store& o) {
  for (size_t i = 0; i < o.v.size(); ++i) offer(o.v[i], o.model(i), o.hash[i]);
  compact();
}

bool Store::check_invariants() const {
  if (staging() != 0 || v.size() > cap) return false;
  for (size_t i = 1; i < v.size(); ++i)
    if (!better(v[i - 1], model(i - 1), v[i], model(i))) return false;   // strict => sorted and no duplicates
  if (cap > 0 && v.size() == cap && cutoff() != v.back()) return false;
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

size_t Store::bytes_reserved() const {
  return v.capacity() * 8 + off.capacity() * 8 + hash.capacity() * 8 + len.capacity() * 2 + pool.capacity() * 4;
}

}  // namespace v4
