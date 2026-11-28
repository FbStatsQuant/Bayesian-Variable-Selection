// store.cpp -- flat top-c store (INTERFACES §4.1).
#include "v4/store.h"
#include <algorithm>
#include <cstring>
#include <numeric>
#include "v4/status.h"

namespace v4 {

Store& Store::operator=(const Store& o) {
  if (this == &o) return *this;
  cap = o.cap; ord = o.ord; v = o.v; off = o.off; hash = o.hash; len = o.len; pool = o.pool; nkept_ = o.nkept_; hidx_ = o.hidx_;
  cut_.store(o.cut_.load(std::memory_order_relaxed), std::memory_order_relaxed);
  return *this;
}

void Store::init(uint64_t c, Order o) {
  cap = c; ord = o; v.clear(); off.clear(); hash.clear(); len.clear(); pool.clear(); nkept_ = 0; hidx_.clear();
  cut_.store(-__builtin_huge_val(), std::memory_order_relaxed);
}

void Store::release() {
  std::vector<double>().swap(v); std::vector<uint64_t>().swap(off); std::vector<uint64_t>().swap(hash); std::vector<uint16_t>().swap(len);
  std::vector<int32_t>().swap(pool); std::vector<uint32_t>().swap(hidx_); nkept_ = 0;
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
  if (value != value) throw Error(Status::internal_error, "store: NaN value (breaks the strict order)");
  if (value < cutoff()) return;                            // strictly worse than c entries already offered
  if (nkept_ == cap && !better(value, S, v[nkept_ - 1], model(nkept_ - 1))) return;   // not better than the worst kept
  if (S.k > 65535) throw Error(Status::internal_error, "store: model too large");
  v.push_back(value); hash.push_back(h); len.push_back((uint16_t)S.k); off.push_back(pool.size());
  pool.insert(pool.end(), S.begin(), S.end());
  if (staging() >= trigger()) compact();
}

bool Store::key_less(uint32_t a, uint32_t b) const {
  if (hash[a] != hash[b]) return hash[a] < hash[b];
  return lex_less(model(a), model(b));
}

void Store::compact() {
  const size_t m = v.size(), ns = m - nkept_;
  if (ns == 0) return;
  std::vector<char> drop(m, 0);
  // 1. one entry per model (INTERFACES §4.1, class-A values are path-dependent maxima): staged entries grouped by
  //    (hash, model), best first; then matched against the kept run through its (hash, model) index (linear walk).
  //    The key sort runs on contiguous (hash, index) pairs, so most comparisons never touch hash[] or the pool.
  std::vector<uint32_t> sh(ns);
  {
    std::vector<std::pair<uint64_t, uint32_t>> kp(ns);
    for (size_t t = 0; t < ns; ++t) kp[t] = {hash[nkept_ + t], (uint32_t)(nkept_ + t)};
    std::sort(kp.begin(), kp.end(), [&](const std::pair<uint64_t, uint32_t>& x, const std::pair<uint64_t, uint32_t>& y) {
      if (x.first != y.first) return x.first < y.first;
      const uint32_t a = x.second, b = y.second;
      if (lex_less(model(a), model(b))) return true;
      if (lex_less(model(b), model(a))) return false;
      return better(v[a], model(a), v[b], model(b));
    });
    for (size_t t = 0; t < ns; ++t) sh[t] = kp[t].second;
  }
  {
    size_t k = 0;
    for (size_t t = 0; t < ns; ++t) {
      uint32_t a = sh[t];
      if (t > 0 && hash[a] == hash[sh[t - 1]] && same_model(model(a), model(sh[t - 1]))) { drop[a] = 1; continue; }   // worse copy
      while (k < hidx_.size() && key_less(hidx_[k], a)) ++k;
      if (k < hidx_.size() && hash[hidx_[k]] == hash[a] && same_model(model(hidx_[k]), model(a))) {
        uint32_t kept = hidx_[k];
        if (better(v[a], model(a), v[kept], model(kept))) drop[kept] = 1; else drop[a] = 1;
      }
    }
  }
  // 2. sort the surviving staged entries by the store order
  std::vector<uint32_t> st; st.reserve(ns);
  for (size_t t = 0; t < ns; ++t) if (!drop[nkept_ + t]) st.push_back((uint32_t)(nkept_ + t));
  std::sort(st.begin(), st.end(), [&](uint32_t a, uint32_t b) { return better(v[a], model(a), v[b], model(b)); });
  // 3. merge with the kept run [0, nkept_) (skipping replaced entries), truncate at cap
  std::vector<uint32_t> sel; sel.reserve(std::min<size_t>(cap, m));
  size_t i = 0, j = 0; uint64_t pool_need = 0;
  while (sel.size() < cap && (i < nkept_ || j < st.size())) {
    if (i < nkept_ && drop[i]) { ++i; continue; }
    uint32_t a;
    if (j >= st.size() || (i < nkept_ && !better(v[st[j]], model(st[j]), v[i], model(i)))) a = (uint32_t)i++;
    else a = st[j++];
    sel.push_back(a); pool_need += len[a];
  }
  st.clear(); st.shrink_to_fit();
  // 4. the new (hash, model) index: merge of the old index and the staged order sh, both restricted to selected entries
  std::vector<uint32_t> newpos(m, UINT32_MAX);
  for (size_t t = 0; t < sel.size(); ++t) newpos[sel[t]] = (uint32_t)t;
  std::vector<uint32_t> nh_idx; nh_idx.reserve(sel.size());
  {
    size_t a = 0, b = 0;
    while (a < hidx_.size() || b < sh.size()) {
      if (a < hidx_.size() && newpos[hidx_[a]] == UINT32_MAX) { ++a; continue; }
      if (b < sh.size() && newpos[sh[b]] == UINT32_MAX) { ++b; continue; }
      if (a >= hidx_.size()) { nh_idx.push_back(newpos[sh[b++]]); continue; }
      if (b >= sh.size()) { nh_idx.push_back(newpos[hidx_[a++]]); continue; }
      if (key_less(sh[b], hidx_[a])) nh_idx.push_back(newpos[sh[b++]]); else nh_idx.push_back(newpos[hidx_[a++]]);
    }
  }
  sh.clear(); sh.shrink_to_fit(); newpos.clear(); newpos.shrink_to_fit();
  // 5. build the new kept run; reserve room for the next staging run too, so appends never reallocate geometrically
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
  hidx_.swap(nh_idx);
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
    if (!better(v[i - 1], model(i - 1), v[i], model(i))) return false;   // strictly sorted (not enough for one per model)
  if (cap > 0 && v.size() == cap && cutoff() != v.back()) return false;
  // one entry per model, independent of the index: a fresh (hash, model) sort has no equal neighbours
  {
    std::vector<std::pair<uint64_t, uint32_t>> kp(v.size());
    for (size_t i = 0; i < v.size(); ++i) kp[i] = {hash[i], (uint32_t)i};
    std::sort(kp.begin(), kp.end(), [&](const std::pair<uint64_t, uint32_t>& x, const std::pair<uint64_t, uint32_t>& y) {
      if (x.first != y.first) return x.first < y.first;
      return lex_less(model(x.second), model(y.second));
    });
    for (size_t t = 1; t < kp.size(); ++t)
      if (kp[t].first == kp[t - 1].first && same_model(model(kp[t].second), model(kp[t - 1].second))) return false;
  }
  // the index: same size, every entry in range (checked before any key_less read), strictly increasing keys
  // (size + range + strict order => a permutation of the kept run in key order)
  if (hidx_.size() != v.size()) return false;
  for (uint32_t x : hidx_) if (x >= v.size()) return false;
  for (size_t t = 1; t < hidx_.size(); ++t) if (!key_less(hidx_[t - 1], hidx_[t])) return false;
  return true;
}

void Store::load_unique_sorted(size_t n, const double* vv, const uint64_t* hh, const uint64_t* oo, const uint16_t* ll,
                               const int32_t* pp, size_t pool_n) {
  if (!v.empty()) throw Error(Status::internal_error, "load_unique_sorted: the store is not empty");
  if (n > cap) throw Error(Status::invalid_input, "store load: " + std::to_string(n) + " entries > cap " + std::to_string(cap));
  uint64_t pool_need = 0;
  for (size_t i = 0; i < n; ++i) {
    if (ll[i] > pool_n || oo[i] > pool_n - ll[i]) throw Error(Status::invalid_input, "store load: pool range out of bounds");
    if (vv[i] != vv[i]) throw Error(Status::invalid_input, "store load: NaN value");
    ModelView S(pp + oo[i], ll[i]);
    if (!is_sorted_unique(S)) throw Error(Status::invalid_input, "store load: a model is not sorted / has repeats");
    if (i > 0 && !better(vv[i - 1], ModelView(pp + oo[i - 1], ll[i - 1]), vv[i], S))
      throw Error(Status::invalid_input, "store load: entries not strictly sorted under the store order");
    pool_need += ll[i];
  }
  v.assign(vv, vv + n); hash.assign(hh, hh + n); len.assign(ll, ll + n);
  off.resize(n); pool.clear(); pool.reserve(pool_need);
  for (size_t i = 0; i < n; ++i) { off[i] = pool.size(); pool.insert(pool.end(), pp + oo[i], pp + oo[i] + ll[i]); }
  // the model index by one pair sort; equal neighbours = the same model twice = not a valid store
  std::vector<std::pair<uint64_t, uint32_t>> kp(n);
  for (size_t i = 0; i < n; ++i) kp[i] = {hash[i], (uint32_t)i};
  std::sort(kp.begin(), kp.end(), [&](const std::pair<uint64_t, uint32_t>& x, const std::pair<uint64_t, uint32_t>& y) {
    if (x.first != y.first) return x.first < y.first;
    return lex_less(model(x.second), model(y.second));
  });
  hidx_.resize(n);
  for (size_t t = 0; t < n; ++t) {
    if (t > 0 && kp[t].first == kp[t - 1].first && same_model(model(kp[t].second), model(kp[t - 1].second))) {
      init(cap, ord);
      throw Error(Status::invalid_input, "store load: the same model appears twice (I1)");
    }
    hidx_[t] = kp[t].second;
  }
  nkept_ = n;
  if (n == cap && cap > 0 && v[n - 1] > cutoff()) cut_.store(v[n - 1], std::memory_order_relaxed);
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
  return v.capacity() * 8 + off.capacity() * 8 + hash.capacity() * 8 + len.capacity() * 2 + pool.capacity() * 4 + hidx_.capacity() * 4;
}

}  // namespace v4
