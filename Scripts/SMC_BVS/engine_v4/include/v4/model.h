// model.h -- model identity: sorted int32 supports, Zobrist hash, strict orders (INTERFACES §2).
#pragma once
#include <algorithm>
#include <cstdint>
#include <vector>

namespace v4 {

using Model = std::vector<int32_t>;                        // owning, sorted, duplicate-free, internal 0-based indices
struct ModelView {
  const int32_t* idx = nullptr; uint32_t k = 0;
  ModelView() = default;
  ModelView(const int32_t* i, uint32_t n) : idx(i), k(n) {}
  ModelView(const Model& m) : idx(m.data()), k((uint32_t)m.size()) {}  // NOLINT: implicit by design
  const int32_t* begin() const { return idx; }
  const int32_t* end() const { return idx + k; }
  int32_t operator[](size_t i) const { return idx[i]; }
  size_t size() const { return k; }
};

// core/cpp/v3_util.h:36-41 (splitmix64), copied.
inline uint64_t splitmix64(uint64_t& x) {
  uint64_t z = (x += 0x9E3779B97F4A7C15ULL);
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
  return z ^ (z >> 31);
}

// core/cpp/v3_util.h:102-109 (Zobrist), copied: keys are successive splitmix64 outputs from a fixed constant.
struct Zobrist {
  std::vector<uint64_t> key;
  void init(int32_t p) {
    key.resize((size_t)p);
    uint64_t x = 0x5EEDB175C0DE2026ULL;
    for (int32_t j = 0; j < p; ++j) key[(size_t)j] = splitmix64(x);
  }
  uint64_t hash(ModelView S) const { uint64_t h = 0; for (int32_t j : S) h ^= key[(size_t)j]; return h; }
};

inline bool same_model(ModelView a, ModelView b) { return a.k == b.k && std::equal(a.begin(), a.end(), b.begin()); }
// core/cpp/v3_util.h:117-119: strict lexicographic order (a proper prefix precedes the longer vector).
inline bool lex_less(ModelView a, ModelView b) { return std::lexicographical_compare(a.begin(), a.end(), b.begin(), b.end()); }
// core/cpp/v3_util.h:121-126: HPM strict order: larger F; exact ties -> smaller |S|; then lexicographically smaller.
inline bool hpm_better(double F1, ModelView S1, double F2, ModelView S2) {
  if (F1 > F2) return true;
  if (F1 < F2) return false;
  if (S1.k != S2.k) return S1.k < S2.k;
  return lex_less(S1, S2);
}
inline bool is_sorted_unique(ModelView S) {
  for (uint32_t i = 1; i < S.k; ++i) if (!(S.idx[i - 1] < S.idx[i])) return false;
  return true;
}
// Sorted insert / erase (core/cpp/v3_util.h:129-130).
inline void sorted_insert(Model& v, int32_t j) { v.insert(std::lower_bound(v.begin(), v.end(), j), j); }
inline void sorted_erase(Model& v, int32_t j) { v.erase(std::lower_bound(v.begin(), v.end(), j)); }

}  // namespace v4
