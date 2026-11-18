// v3_util.h -- shared numerical and bookkeeping utilities for the SMC-BVS v3 core layer.
// Spec: CORE_SPEC v2 §§4.1, 5 (random streams, variate conventions); M §6.13 (log-sum-exp).
#pragma once
#include <cstdint>
#include <vector>
#include <cmath>
#include <limits>
#include <algorithm>
#include <string>
#include <stdexcept>
#include <sstream>
#include <functional>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <iterator>
#include <chrono>

namespace v3 {

const double NEG_INF = -std::numeric_limits<double>::infinity();
const double POS_INF = std::numeric_limits<double>::infinity();

// Thrown when a score fails after every fallback (M §6.13: Cholesky -> refactor -> augmented QR -> numerical_failure).
struct NumericalFailure : public std::runtime_error {
  explicit NumericalFailure(const std::string& m) : std::runtime_error("numerical_failure: " + m) {}
};

// ---------------------------------------------------------------------------------------------
// Random streams (CORE_SPEC §5). Seeding function (documented, reproducible):
//   x = seed * 2^32 + stream  (seed in [1, 2^31-1], stream in [0, 2^32-1]; distinct pairs give distinct x)
//   xoshiro256** state s[0..3] = four successive SplitMix64 outputs from x.
// Uniform u = (next() >> 11) * 2^-53, in [0, 1) with 53 random bits.
// ---------------------------------------------------------------------------------------------
inline uint64_t splitmix64(uint64_t& x) {
  uint64_t z = (x += 0x9E3779B97F4A7C15ULL);
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
  return z ^ (z >> 31);
}

struct Xoshiro256ss {
  uint64_t s[4];
  uint64_t count = 0;  // number of 64-bit draws consumed since seeding (stream position; R6 instrumentation)
  static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
  void seed_stream(uint64_t seed, uint64_t stream) {
    uint64_t x = (seed << 32) + stream;
    for (int i = 0; i < 4; ++i) s[i] = splitmix64(x);
    count = 0;
  }
  inline uint64_t next() {
    ++count;
    const uint64_t result = rotl(s[1] * 5, 7) * 9;
    const uint64_t t = s[1] << 17;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3];
    s[2] ^= t; s[3] = rotl(s[3], 45);
    return result;
  }
  inline double uniform() { return (double)(next() >> 11) * 0x1.0p-53; }
};

// ---------------------------------------------------------------------------------------------
// Log-space helpers (M §6.13: log-sum-exp for every sum of weights, profiles and evidence).
// ---------------------------------------------------------------------------------------------
// log(exp(a) + exp(b)) without overflow; replaces the textbook sum of exponentials.
inline double log_add(double a, double b) {
  if (a == NEG_INF) return b;
  if (b == NEG_INF) return a;
  if (a < b) std::swap(a, b);
  return a + std::log1p(std::exp(b - a));
}
// log sum_i exp(x_i), max-shifted.
inline double log_sum_exp(const std::vector<double>& x) {
  double m = NEG_INF;
  for (double v : x) if (v > m) m = v;
  if (m == NEG_INF || !std::isfinite(m)) return m;
  long double s = 0.0L;  // long double accumulation: guards relative error when many terms are summed
  for (double v : x) s += std::exp((long double)(v - m));
  return m + (double)std::log(s);
}
// log(1 - exp(x)) for x <= 0, stable on both ends (Maechler 2012); replaces 1 - p on rounded probabilities.
inline double log1mexp_v3(double x) {
  if (x > 0) return std::numeric_limits<double>::quiet_NaN();
  if (x == 0) return NEG_INF;
  return (x > -M_LN2) ? std::log(-std::expm1(x)) : std::log1p(-std::exp(x));
}
// Logistic a/(1+a) from log a; stable for |log a| large (replaces exp(la)/(1+exp(la))).
inline double plogis_log(double la) {
  if (la >= 0) return 1.0 / (1.0 + std::exp(-la));
  double e = std::exp(la);
  return e / (1.0 + e);
}
inline double lchoose_d(double n, double k) { return std::lgamma(n + 1.0) - std::lgamma(k + 1.0) - std::lgamma(n - k + 1.0); }

// ---------------------------------------------------------------------------------------------
// Model identity for arbitrary p (CORE_SPEC engineering requirement).
// A model is (a) its sorted list of internal 0-based indices and (b) a bitset of W = ceil(p/64) words.
// Hash = Zobrist hash: XOR of fixed pseudo-random 64-bit keys of the members, so toggling j is O(1).
// Collisions are resolved by comparing the full bitset, so the hash never changes which model is meant.
// ---------------------------------------------------------------------------------------------
struct Zobrist {
  std::vector<uint64_t> key;
  void init(int p) {
    key.resize(p);
    uint64_t x = 0x5EEDB175C0DE2026ULL;  // fixed constant: hashes are deterministic across runs
    for (int j = 0; j < p; ++j) key[j] = splitmix64(x);
  }
};

inline int nwords(int p) { return (p + 63) / 64; }
inline bool bit_get(const std::vector<uint64_t>& b, int j) { return (b[j >> 6] >> (j & 63)) & 1ULL; }
inline void bit_flip(std::vector<uint64_t>& b, int j) { b[j >> 6] ^= (1ULL << (j & 63)); }
inline void bit_set(std::vector<uint64_t>& b, int j) { b[j >> 6] |= (1ULL << (j & 63)); }

// Strict lexicographic order on sorted index vectors (a proper prefix precedes the longer vector).
inline bool lex_less(const std::vector<int>& a, const std::vector<int>& b) {
  return std::lexicographical_compare(a.begin(), a.end(), b.begin(), b.end());
}
// HPM strict order (M §6.10): larger F first; exact ties -> smaller |S|; then lexicographically smaller set.
inline bool hpm_better(double F1, const std::vector<int>& S1, double F2, const std::vector<int>& S2) {
  if (F1 > F2) return true;
  if (F1 < F2) return false;
  if (S1.size() != S2.size()) return S1.size() < S2.size();
  return lex_less(S1, S2);
}

// Insert j into / erase j from a sorted vector (models are kept sorted at all times).
inline void sorted_insert(std::vector<int>& v, int j) { v.insert(std::lower_bound(v.begin(), v.end(), j), j); }
inline void sorted_erase(std::vector<int>& v, int j) { v.erase(std::lower_bound(v.begin(), v.end(), j)); }

inline std::string join_idx(const std::vector<int>& S, const std::vector<int>& orig) {
  std::ostringstream o;
  for (size_t i = 0; i < S.size(); ++i) { if (i) o << ','; o << orig[S[i]]; }
  return o.str();
}

}  // namespace v3
