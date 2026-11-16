// wp1_shim.h -- TEMPORARY stand-ins for the WP1-owned headers of INTERFACES.md v0.1 §2, §5, §7, §8
// (types.h data.h model.h store.h format.h status.h pmath.h sha256). WP2 codes against the declared names only.
// When WP1's headers land on exp/P1M-engine, this file is replaced by `#include <v4/...>` lines and deleted; nothing
// else in src/setup/ should need to change. Everything here follows INTERFACES v0.1 or copies core/ (cited).
#pragma once
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace v4 {

// ---- status.h (INTERFACES §7) ----
enum class Status : uint8_t { completed = 0, resource_limit = 1, numerical_failure = 2, invalid_input = 3, io_error = 4, internal_error = 5 };
inline const char* status_name(Status s) {
  static const char* nm[] = {"completed", "resource_limit", "numerical_failure", "invalid_input", "io_error", "internal_error"};
  return nm[(int)s];
}
struct Error : std::runtime_error {
  Status st;
  Error(Status s, const std::string& m) : std::runtime_error(m), st(s) {}
};
// core/cpp/v3_util.h:26-28 semantics
struct NumericalFailure : Error {
  explicit NumericalFailure(const std::string& m) : Error(Status::numerical_failure, "numerical_failure: " + m) {}
};

// ---- pmath.h (INTERFACES §6): binding decided by WP1; glibc here ----
namespace pm {
inline double log(double x) { return std::log(x); }
inline double exp(double x) { return std::exp(x); }
inline double log1p(double x) { return std::log1p(x); }
inline double expm1(double x) { return std::expm1(x); }
inline double lgamma(double x) { return std::lgamma(x); }
inline long double expl(long double x) { return std::exp(x); }
inline long double logl(long double x) { return std::log(x); }
}  // namespace pm

const double NEG_INF = -std::numeric_limits<double>::infinity();
const double POS_INF = std::numeric_limits<double>::infinity();

// ---- model.h (INTERFACES §2) ----
struct ModelView { const int32_t* idx; uint32_t k; };
using Model = std::vector<int32_t>;
inline ModelView view(const Model& m) { return ModelView{m.data(), (uint32_t)m.size()}; }

// core/cpp/v3_util.h:36-41
inline uint64_t splitmix64(uint64_t& x) {
  uint64_t z = (x += 0x9E3779B97F4A7C15ULL);
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
  return z ^ (z >> 31);
}
// core/cpp/v3_util.h:102-109
struct Zobrist {
  std::vector<uint64_t> key;
  void init(int p) {
    key.resize(p);
    uint64_t x = 0x5EEDB175C0DE2026ULL;
    for (int j = 0; j < p; ++j) key[j] = splitmix64(x);
  }
  uint64_t hash(ModelView S) const { uint64_t h = 0; for (uint32_t i = 0; i < S.k; ++i) h ^= key[S.idx[i]]; return h; }
};
// core/cpp/v3_util.h:117-126
inline bool lex_less(ModelView a, ModelView b) { return std::lexicographical_compare(a.idx, a.idx + a.k, b.idx, b.idx + b.k); }
inline bool lex_less(const Model& a, const Model& b) { return std::lexicographical_compare(a.begin(), a.end(), b.begin(), b.end()); }
inline bool hpm_better(double F1, ModelView S1, double F2, ModelView S2) {
  if (F1 > F2) return true;
  if (F1 < F2) return false;
  if (S1.k != S2.k) return S1.k < S2.k;
  return lex_less(S1, S2);
}

// ---- data.h (INTERFACES §2) ----
struct Data {
  int32_t n = 0, p = 0, p_raw = 0, K = 0;
  const double* Xs = nullptr;
  const double* ys = nullptr;
  const double* z = nullptr;
  const double* diagG = nullptr;
  const double *col_max = nullptr, *col_mean = nullptr, *col_sd = nullptr;
  const int32_t* orig = nullptr;
  double yty = 0, a0 = 0.01, b0 = 0.01, nu = 0, logCn = 0, logm0 = 0, logWK = 0;
  std::vector<double> logw, logprior;
  Zobrist zob;
  double y_max = 0, y_mean = 0, y_sd_scaled = 0;
  inline const double* col(int64_t j) const { return Xs + (size_t)j * n; }
};
// INTERFACES §2: gram(a,b) = sum_i x_{i,min(a,b)} x_{i,max(a,b)}, sequential in i, no FMA (core/cpp/v3_score.h:45-53).
inline double gram(const Data& D, int a, int b) {
  const double* xa = D.col(std::min(a, b));
  const double* xb = D.col(std::max(a, b));
  double s = 0;
  for (int i = 0; i < D.n; ++i) s += xa[i] * xb[i];
  return s;
}
// core/cpp/v3_util.h:74-81
inline double log_sum_exp(const double* x, size_t n) {
  double m = NEG_INF;
  for (size_t i = 0; i < n; ++i) if (x[i] > m) m = x[i];
  if (m == NEG_INF || !std::isfinite(m)) return m;
  long double s = 0.0L;
  for (size_t i = 0; i < n; ++i) s += pm::expl((long double)(x[i] - m));
  return m + (double)pm::logl(s);
}
inline double log_sum_exp(const std::vector<double>& x) { return log_sum_exp(x.data(), x.size()); }
inline double lchoose_d(double n, double k) { return pm::lgamma(n + 1.0) - pm::lgamma(k + 1.0) - pm::lgamma(n - k + 1.0); }
// Scalars of core/cpp/v3_score.h:56-71 (z, yty, constants, log w, log prior). Owning holder for tests and tools.
struct DataOwner {
  std::vector<double> X, y, z, dg, cmax, cmean, csd;
  std::vector<int32_t> orig;
  Data D;
  void init(const double* Xin, const double* yin, int n, int p) {
    X.assign(Xin, Xin + (size_t)n * p); y.assign(yin, yin + n);
    orig.resize(p); for (int j = 0; j < p; ++j) orig[j] = j + 1;
    D = Data(); D.n = n; D.p = p; D.p_raw = p; D.K = std::min(p, n / 2);
    D.Xs = X.data(); D.ys = y.data(); D.orig = orig.data();
    z.assign(p, 0.0); dg.assign(p, 0.0);
    for (int a = 0; a < p; ++a) {
      const double* xa = D.col(a); double s = 0, g = 0;
      for (int i = 0; i < n; ++i) s += xa[i] * y[i];
      for (int i = 0; i < n; ++i) g += xa[i] * xa[i];
      z[a] = s; dg[a] = g;
    }
    D.z = z.data(); D.diagG = dg.data();
    D.yty = 0; for (int i = 0; i < n; ++i) D.yty += y[i] * y[i];
    D.nu = D.a0 + n / 2.0;
    D.logCn = D.a0 * pm::log(2 * D.b0) + pm::lgamma(D.a0 + n / 2.0) - (n / 2.0) * pm::log(M_PI) - pm::lgamma(D.a0);
    D.logm0 = D.logCn - D.nu * pm::log(2 * D.b0 + D.yty);
    D.logw.assign(D.K + 1, 0.0);
    std::vector<double> terms(D.K + 1);
    for (int k = 0; k <= D.K; ++k) { D.logw[k] = -M_LN2 - lchoose_d(2.0 * p - 1.0, k); terms[k] = lchoose_d((double)p, k) + D.logw[k]; }
    D.logWK = log_sum_exp(terms);
    D.logprior.assign(D.K + 1, 0.0);
    for (int k = 0; k <= D.K; ++k) D.logprior[k] = D.logw[k] - D.logWK;
    D.zob.init(p);
  }
};

// ---- rng.h (INTERFACES §3), only what draw_pi0 needs ----
struct Address { uint32_t seed = 0; uint8_t role = 0, tier = 0, iter = 0; uint32_t island = 0;
                 uint8_t xph = 0; uint32_t stage = 0; uint32_t particle = 0, position = 0, slot = 0; };
struct UniformSource { virtual double u(const Address&) = 0; virtual ~UniformSource() {} };

// ---- store.h (INTERFACES §4.1), minimal reference: buffer + compact ----
enum class Order : uint8_t { HPM, LEX };
struct Store {
  uint64_t cap = 0; Order ord = Order::HPM;
  std::vector<double> v; std::vector<uint64_t> off, hash; std::vector<uint16_t> len; std::vector<int32_t> pool;
  size_t nsorted = 0;  // entries [0, nsorted) are compacted
  void init(uint64_t c, Order o) { cap = c; ord = o; v.clear(); off.clear(); hash.clear(); len.clear(); pool.clear(); nsorted = 0; }
  size_t size() const { return v.size(); }
  ModelView S(size_t i) const { return ModelView{pool.data() + off[i], len[i]}; }
  bool less(size_t a, size_t b) const {  // core/cpp/v3_ledger.h:35-42
    if (v[a] != v[b]) return v[a] > v[b];
    if (ord == Order::HPM && len[a] != len[b]) return len[a] < len[b];
    return lex_less(S(a), S(b));
  }
  void offer(double val, ModelView s, uint64_t h) {
    if (cap == 0) return;
    v.push_back(val); off.push_back(pool.size()); hash.push_back(h); len.push_back((uint16_t)s.k);
    pool.insert(pool.end(), s.idx, s.idx + s.k);
    if (v.size() >= 2 * cap + 1024) compact();
  }
  void compact() {
    std::vector<uint32_t> o(v.size());
    for (size_t i = 0; i < o.size(); ++i) o[i] = (uint32_t)i;
    std::sort(o.begin(), o.end(), [&](uint32_t a, uint32_t b) { return less(a, b); });
    std::vector<double> v2; std::vector<uint64_t> off2, h2; std::vector<uint16_t> l2; std::vector<int32_t> p2;
    for (uint32_t i : o) {
      if (v2.size() >= cap) break;
      if (!v2.empty()) {  // exact duplicate (same S => same value): adjacent after the sort
        size_t lst = v2.size() - 1;
        if (l2[lst] == len[i] && v2[lst] == v[i] && std::equal(p2.begin() + off2[lst], p2.begin() + off2[lst] + l2[lst], pool.begin() + off[i])) continue;
      }
      v2.push_back(v[i]); off2.push_back(p2.size()); h2.push_back(hash[i]); l2.push_back(len[i]);
      p2.insert(p2.end(), pool.begin() + off[i], pool.begin() + off[i] + len[i]);
    }
    v.swap(v2); off.swap(off2); hash.swap(h2); len.swap(l2); pool.swap(p2); nsorted = v.size();
  }
  void merge(const Store& o) { for (size_t i = 0; i < o.size(); ++i) offer(o.v[i], o.S(i), o.hash[i]); compact(); }
};

}  // namespace v4
