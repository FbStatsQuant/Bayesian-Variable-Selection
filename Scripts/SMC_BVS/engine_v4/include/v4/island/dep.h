// dep.h -- PROVISIONAL stand-ins for the WP1 / WP2 types the island needs (INTERFACES v0.1 §2, §3, §6).
//
// WP3 (island kernel) started before WP1's headers existed. Everything in namespace v4::island::dep is a minimal,
// self-contained copy of the contract so that the island can be built and tested now. When WP1's `types.h data.h
// model.h rng.h score.h pmath.h` and WP2's `setup.h` land, these definitions are replaced by thin aliases (see
// engine_v4/src/island/README.md, "Adoption of WP1/WP2 headers"). Nothing here is meant to survive that switch except
// the arithmetic, which is copied from core/ and cited line by line.
//
// Copied arithmetic (bits must equal core/):
//   Data constants ............ core/cpp/v3_score.h:39-72 (Gram dropped: INTERFACES §2 "Data holds no Gram")
//   Zobrist, splitmix64 ....... core/cpp/v3_util.h:36-41, 99-108
//   log_sum_exp, plogis_log ... core/cpp/v3_util.h:66-91
//   scorer .................... core/cpp/v3_score.h:76-238 (Gram-free: entries by the sequential sum of :45-53)
//   start tables / pi0 draw ... core/cpp/v3_start.h:14-31, 54-66, 76-176
#pragma once
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace v4::island::dep {

const double NEG_INF = -std::numeric_limits<double>::infinity();
const double POS_INF = std::numeric_limits<double>::infinity();

using Model = std::vector<int32_t>;
struct ModelView { const int32_t* idx; uint32_t k; };

struct NumericalFailure : public std::runtime_error {
  explicit NumericalFailure(const std::string& m) : std::runtime_error("numerical_failure: " + m) {}
};

// pinned math (INTERFACES §6: v4::pm::*). Bound to glibc here, exactly as core/ is compiled; WP1 decides the binding.
namespace pm {
inline double log(double x) { return std::log(x); }
inline double exp(double x) { return std::exp(x); }
inline double log1p(double x) { return std::log1p(x); }
inline double lgamma(double x) { return std::lgamma(x); }
}  // namespace pm

// core/cpp/v3_util.h:36-41
inline uint64_t splitmix64(uint64_t& x) {
  uint64_t z = (x += 0x9E3779B97F4A7C15ULL);
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
  return z ^ (z >> 31);
}
// core/cpp/v3_util.h:66-81 (log_sum_exp with long double accumulation)
inline double log_sum_exp(const std::vector<double>& x) {
  double m = NEG_INF;
  for (double v : x) if (v > m) m = v;
  if (m == NEG_INF || !std::isfinite(m)) return m;
  long double s = 0.0L;
  for (double v : x) s += std::exp((long double)(v - m));
  return m + (double)std::log(s);
}
// core/cpp/v3_util.h:88-92
inline double plogis_log(double la) {
  if (la >= 0) return 1.0 / (1.0 + pm::exp(-la));
  double e = pm::exp(la);
  return e / (1.0 + e);
}
inline double lchoose_d(double n, double k) { return pm::lgamma(n + 1.0) - pm::lgamma(k + 1.0) - pm::lgamma(n - k + 1.0); }
// core/cpp/v3_util.h:116-126
inline bool lex_less(const int32_t* a, size_t na, const int32_t* b, size_t nb) {
  return std::lexicographical_compare(a, a + na, b, b + nb);
}
inline bool lex_less(const Model& a, const Model& b) { return lex_less(a.data(), a.size(), b.data(), b.size()); }
inline bool hpm_better(double F1, const Model& S1, double F2, const Model& S2) {
  if (F1 > F2) return true;
  if (F1 < F2) return false;
  if (S1.size() != S2.size()) return S1.size() < S2.size();
  return lex_less(S1, S2);
}
inline void sorted_insert(Model& v, int32_t j) { v.insert(std::lower_bound(v.begin(), v.end(), j), j); }
inline void sorted_erase(Model& v, int32_t j) { v.erase(std::lower_bound(v.begin(), v.end(), j)); }
inline bool contains(const Model& v, int32_t j) { return std::binary_search(v.begin(), v.end(), j); }

// ---------------------------------------------------------------------------------------------------------------
// Data (INTERFACES §2), owning storage. Constants exactly as core/cpp/v3_score.h:56-72.
// ---------------------------------------------------------------------------------------------------------------
struct Data {
  int32_t n = 0, p = 0, K = 0;
  std::vector<double> X, y, z, diagG;
  double yty = 0, a0 = 0.01, b0 = 0.01, nu = 0, logCn = 0, logm0 = 0, logWK = 0;
  std::vector<double> logw, logprior;
  std::vector<uint64_t> zkey;  // Zobrist keys (core/cpp/v3_util.h:99-108)
  inline const double* col(int j) const { return &X[(size_t)j * n]; }
};
inline void data_init(Data& D, const double* X, const double* y, int n, int p) {
  D.n = n; D.p = p; D.K = std::min(p, n / 2);
  D.X.assign(X, X + (size_t)n * p);
  D.y.assign(y, y + n);
  // diag(G) by the sequential sum of core/cpp/v3_score.h:45-53 (a == b)
  D.diagG.assign(p, 0.0);
  for (int a = 0; a < p; ++a) { const double* xa = D.col(a); double s = 0; for (int i = 0; i < n; ++i) s += xa[i] * xa[i]; D.diagG[a] = s; }
  // core/cpp/v3_score.h:54-70
  D.z.assign(p, 0.0);
  for (int a = 0; a < p; ++a) { const double* xa = D.col(a); double s = 0; for (int i = 0; i < n; ++i) s += xa[i] * D.y[i]; D.z[a] = s; }
  D.yty = 0; for (int i = 0; i < n; ++i) D.yty += D.y[i] * D.y[i];
  D.nu = D.a0 + n / 2.0;
  D.logCn = D.a0 * pm::log(2 * D.b0) + pm::lgamma(D.a0 + n / 2.0) - (n / 2.0) * pm::log(M_PI) - pm::lgamma(D.a0);
  D.logm0 = D.logCn - D.nu * pm::log(2 * D.b0 + D.yty);
  D.logw.assign(D.K + 1, 0.0);
  std::vector<double> terms(D.K + 1);
  for (int k = 0; k <= D.K; ++k) {
    D.logw[k] = -M_LN2 - lchoose_d(2.0 * p - 1.0, k);
    terms[k] = lchoose_d((double)p, k) + D.logw[k];
  }
  D.logWK = log_sum_exp(terms);
  D.logprior.assign(D.K + 1, 0.0);
  for (int k = 0; k <= D.K; ++k) D.logprior[k] = D.logw[k] - D.logWK;
  // core/cpp/v3_util.h:101-106
  D.zkey.resize(p);
  uint64_t x = 0x5EEDB175C0DE2026ULL;
  for (int j = 0; j < p; ++j) D.zkey[j] = splitmix64(x);
}
inline uint64_t zobrist(const Data& D, const Model& S) { uint64_t h = 0; for (int j : S) h ^= D.zkey[j]; return h; }

// ---------------------------------------------------------------------------------------------------------------
// Uniforms: Philox4x32-10 at position addresses (INTERFACES §3).
// ---------------------------------------------------------------------------------------------------------------
enum Role : uint8_t { R_FINAL = 0, R_PILOT = 1, R_DIAG = 2, R_POST = 3, R_GEN = 4, R_TEST = 5 };
enum XPh : uint8_t { X_INIT = 0, X_RESAMPLE = 1, X_BRIDGE = 2, X_BURN = 3, X_MEASURED = 4, X_POST = 5 };
struct Address {
  uint32_t seed = 0; uint8_t role = 0, tier = 0, iter = 0; uint32_t island = 0;       // key
  uint8_t xph = 0; uint32_t stage = 0; uint32_t particle = 0, position = 0, slot = 0;  // counter
};
struct Philox4x32 {
  static inline void mulhilo(uint32_t a, uint32_t b, uint32_t& hi, uint32_t& lo) {
    uint64_t pr = (uint64_t)a * (uint64_t)b; hi = (uint32_t)(pr >> 32); lo = (uint32_t)pr;
  }
  // Random123 philox4x32 with R = 10 rounds; key bumped by (W0, W1) between rounds.
  static inline void gen(const uint32_t in[4], const uint32_t k[2], uint32_t out[4]) {
    uint32_t c0 = in[0], c1 = in[1], c2 = in[2], c3 = in[3], k0 = k[0], k1 = k[1];
    for (int r = 0; r < 10; ++r) {
      if (r) { k0 += 0x9E3779B9u; k1 += 0xBB67AE85u; }
      uint32_t hi0, lo0, hi1, lo1;
      mulhilo(0xD2511F53u, c0, hi0, lo0);
      mulhilo(0xCD9E8D57u, c2, hi1, lo1);
      uint32_t n0 = hi1 ^ c1 ^ k0, n1 = lo1, n2 = hi0 ^ c3 ^ k1, n3 = lo0;
      c0 = n0; c1 = n1; c2 = n2; c3 = n3;
    }
    out[0] = c0; out[1] = c1; out[2] = c2; out[3] = c3;
  }
};
inline void address_words(const Address& a, uint32_t ctr[4], uint32_t key[2]) {
  key[0] = a.seed;
  key[1] = ((uint32_t)a.role << 28) | ((uint32_t)(a.tier & 3u) << 26) | ((uint32_t)(a.iter & 63u) << 20) | (a.island & 0xFFFFFu);
  ctr[0] = a.slot; ctr[1] = a.position; ctr[2] = a.particle; ctr[3] = ((uint32_t)a.xph << 24) | (a.stage & 0xFFFFFFu);
}
inline double uniform_at(const Address& a) {
  uint32_t ctr[4], key[2], x[4];
  address_words(a, ctr, key);
  Philox4x32::gen(ctr, key, x);
  uint64_t w = ((uint64_t)x[1] << 32) | x[0];
  return (double)(w >> 11) * 0x1.0p-53;
}

// ---------------------------------------------------------------------------------------------------------------
// Bit scorer, Gram-free (INTERFACES §6, Arith::Bit; core/cpp/v3_score.h:76-238).
// ---------------------------------------------------------------------------------------------------------------
enum Route : int8_t { ROUTE_CHOL = 0, ROUTE_REFACTOR = 1, ROUTE_QR = 2 };
// core/cpp/v3_score.h:76-90
inline bool chol_inplace(double* A, int k) {
  for (int j = 0; j < k; ++j) {
    double d = A[j * k + j];
    for (int t = 0; t < j; ++t) d -= A[j * k + t] * A[j * k + t];
    if (!(d > 0) || !std::isfinite(d)) return false;
    double L = std::sqrt(d);
    A[j * k + j] = L;
    for (int i = j + 1; i < k; ++i) {
      double s = A[i * k + j];
      for (int t = 0; t < j; ++t) s -= A[i * k + t] * A[j * k + t];
      A[i * k + j] = s / L;
    }
  }
  return true;
}
// core/cpp/v3_score.h:92-98
inline void forward_solve(const double* L, int k, const double* b, double* w) {
  for (int i = 0; i < k; ++i) { double s = b[i]; for (int t = 0; t < i; ++t) s -= L[i * k + t] * w[t]; w[i] = s / L[i * k + i]; }
}
inline void backward_solve(const double* L, int k, const double* w, double* x) {
  for (int i = k - 1; i >= 0; --i) { double s = w[i]; for (int t = i + 1; t < k; ++t) s -= L[t * k + i] * x[t]; x[i] = s / L[i * k + i]; }
}
// core/cpp/v3_score.h:103-135
inline bool householder_lower(std::vector<double>& M, int m, int k, std::vector<double>& L) {
  std::vector<double> v(m);
  for (int j = 0; j < k; ++j) {
    double nrm = 0; for (int i = j; i < m; ++i) nrm += M[(size_t)j * m + i] * M[(size_t)j * m + i];
    nrm = std::sqrt(nrm);
    if (!(nrm > 0) || !std::isfinite(nrm)) return false;
    double x0 = M[(size_t)j * m + j];
    double alpha = (x0 > 0) ? -nrm : nrm;
    for (int i = j; i < m; ++i) v[i] = M[(size_t)j * m + i];
    v[j] -= alpha;
    double vn = 0; for (int i = j; i < m; ++i) vn += v[i] * v[i];
    if (vn > 0) {
      for (int c = j; c < k; ++c) {
        double s = 0; for (int i = j; i < m; ++i) s += v[i] * M[(size_t)c * m + i];
        double f = 2 * s / vn;
        for (int i = j; i < m; ++i) M[(size_t)c * m + i] -= f * v[i];
      }
    }
  }
  L.assign((size_t)k * k, 0.0);
  for (int i = 0; i < k; ++i)
    for (int j = i; j < k; ++j) {
      double r = M[(size_t)j * m + i];
      if (i == j) r = std::fabs(r);
      L[j * k + i] = r;
    }
  for (int i = 0; i < k; ++i) {
    if (M[(size_t)i * m + i] < 0) for (int j = i + 1; j < k; ++j) L[j * k + i] = -L[j * k + i];
  }
  for (int i = 0; i < k; ++i) if (!(L[i * k + i] > 0) || !std::isfinite(L[i * k + i])) return false;
  return true;
}
// Gram entry by the sequential sum (core/cpp/v3_score.h:45-53 / :170).
inline double gram(const Data& D, int a, int b) {
  const double* xa = D.col(a); const double* xb = D.col(b); double g = 0;
  for (int i = 0; i < D.n; ++i) g += xa[i] * xb[i];
  return g;
}
struct ScoreOut { double logm = 0, Q = 0; int8_t route = 0; bool q_recomputed = false; };

class BitScorer {
 public:
  const Data* D;
  std::vector<double> bufH, bufA, w, beta, tmp, Gs, LH;
  explicit BitScorer(const Data* d) : D(d) {}
  // core/cpp/v3_score.h:147-160
  double q_nonneg(const Model& S, const std::vector<double>& L) {
    int k = (int)S.size(), n = D->n;
    w.resize(k); beta.resize(k); tmp.resize(k);
    for (int a = 0; a < k; ++a) tmp[a] = n * D->z[S[a]];
    forward_solve(L.data(), k, tmp.data(), w.data());
    backward_solve(L.data(), k, w.data(), beta.data());
    double rss = 0, fit2 = 0, b2 = 0;
    for (int i = 0; i < n; ++i) {
      double f = 0; for (int a = 0; a < k; ++a) f += D->col(S[a])[i] * beta[a];
      double r = D->y[i] - f; rss += r * r; fit2 += f * f;
    }
    for (int a = 0; a < k; ++a) b2 += beta[a] * beta[a];
    return rss + (fit2 + b2) / n;
  }
  // core/cpp/v3_score.h:204-224
  void finish(const Model& S, const std::vector<double>& L_H, const std::vector<double>& L_A, ScoreOut& o) {
    int k = (int)S.size();
    double ldH = 0, ldA = 0;
    for (int a = 0; a < k; ++a) { ldH += pm::log(L_H[a * k + a]); ldA += pm::log(L_A[a * k + a]); }
    ldH *= 2; ldA *= 2;
    w.resize(k); tmp.resize(k);
    for (int a = 0; a < k; ++a) tmp[a] = D->z[S[a]];
    forward_solve(L_H.data(), k, tmp.data(), w.data());
    double quad = 0; for (int a = 0; a < k; ++a) quad += w[a] * w[a];
    double Q = D->yty - D->n * quad;
    o.q_recomputed = false;
    if (Q < 1e-8 * D->yty) { Q = q_nonneg(S, L_H); o.q_recomputed = true; }
    o.Q = Q;
    double arg = 2 * D->b0 + Q;
    o.logm = (arg > 0) ? D->logCn - 0.5 * (ldH - ldA) - D->nu * pm::log(arg) : NEG_INF;
  }
  // core/cpp/v3_score.h:176-188 with Gs supplied (row-major k x k, entries = sequential sums).
  bool try_chol_gs(const Model& S, const double* G, ScoreOut& o) {
    int k = (int)S.size(); double n1 = D->n + 1.0;
    bufH.assign((size_t)k * k, 0.0); bufA.assign((size_t)k * k, 0.0);
    for (int a = 0; a < k; ++a) for (int b = 0; b < k; ++b) {
      bufH[a * k + b] = n1 * G[a * k + b] + (a == b ? 1.0 : 0.0);
      bufA[a * k + b] = G[a * k + b] + (a == b ? 1.0 : 0.0);
    }
    if (!chol_inplace(bufH.data(), k) || !chol_inplace(bufA.data(), k)) return false;
    LH = bufH;
    finish(S, bufH, bufA, o);
    return std::isfinite(o.logm);
  }
  // core/cpp/v3_score.h:190-202
  bool try_qr(const Model& S, ScoreOut& o) {
    int k = (int)S.size(), n = D->n, m = n + k;
    std::vector<double> MH((size_t)m * k, 0.0), MA((size_t)m * k, 0.0), LA;
    double s1 = std::sqrt(n + 1.0);
    for (int a = 0; a < k; ++a) {
      const double* xa = D->col(S[a]);
      for (int i = 0; i < n; ++i) { MH[(size_t)a * m + i] = s1 * xa[i]; MA[(size_t)a * m + i] = xa[i]; }
      MH[(size_t)a * m + n + a] = 1.0; MA[(size_t)a * m + n + a] = 1.0;
    }
    if (!householder_lower(MH, m, k, LH) || !householder_lower(MA, m, k, LA)) return false;
    finish(S, LH, LA, o);
    return std::isfinite(o.logm);
  }
  // Full score from a supplied Gram (rows/cols in S order). Route chol, else QR: the refactor route of
  // core/cpp/v3_score.h:234 recomputes identical entries, so it fails exactly when chol fails.
  ScoreOut score_gs(const Model& S, const double* G) {
    ScoreOut o; int k = (int)S.size();
    if (k > D->K) throw std::runtime_error("score: |S| > K");
    if (k == 0) { o.logm = D->logm0; o.Q = D->yty; o.route = ROUTE_CHOL; return o; }
    if (try_chol_gs(S, G, o)) { o.route = ROUTE_CHOL; return o; }
    if (try_qr(S, o)) { o.route = ROUTE_QR; return o; }
    throw NumericalFailure("score failed after Cholesky and augmented QR, |S| = " + std::to_string(k));
  }
  ScoreOut score(const Model& S) {
    int k = (int)S.size();
    Gs.assign((size_t)k * k, 0.0);
    for (int a = 0; a < k; ++a) for (int b = 0; b <= a; ++b) { double g = gram(*D, S[a], S[b]); Gs[a * k + b] = g; Gs[b * k + a] = g; }
    return score_gs(S, Gs.data());
  }
};

// ---------------------------------------------------------------------------------------------------------------
// Partition, tables, start law pi_0 (WP2 stand-in; arithmetic of core/cpp/v3_start.h).
// The stand-in partition is contiguous blocks of `bsz` columns (WP2 delivers truncated complete linkage).
// ---------------------------------------------------------------------------------------------------------------
// core/cpp/v3_start.h:14-31
inline int cat_draw_gt(const std::vector<double>& cum, double u) {
  return (int)(std::upper_bound(cum.begin(), cum.end(), u) - cum.begin());
}
inline std::vector<double> cumulative_from_logs(const std::vector<double>& lp) {
  double m = NEG_INF; for (double v : lp) m = std::max(m, v);
  std::vector<double> c(lp.size(), 0.0);
  if (m == NEG_INF) return c;
  long double s = 0; std::vector<long double> e(lp.size());
  for (size_t i = 0; i < lp.size(); ++i) { e[i] = (lp[i] == NEG_INF) ? 0.0L : std::exp((long double)(lp[i] - m)); s += e[i]; }
  long double acc = 0; int last = -1;
  for (size_t i = 0; i < lp.size(); ++i) { acc += e[i]; c[i] = (double)(acc / s); if (e[i] > 0) last = (int)i; }
  for (size_t i = (size_t)last; i < lp.size(); ++i) c[i] = 1.0;
  return c;
}
struct Start {
  const Data* D = nullptr;
  int J = 0;
  std::vector<std::vector<int>> blocks;
  std::vector<int> blk, pos;
  std::vector<std::vector<double>> logr, logprof, logF;
  double logZbar0 = 0;
  std::vector<double> size_logmass, size_cum;
  std::vector<std::vector<std::vector<double>>> cond_cum, sub_cum;
  std::vector<std::vector<std::vector<int>>> codes_by_size;
  // core/cpp/v3_start.h:54-66: blocks met by S, increasing block order, sum from 0.
  double comp(const Model& S) const {
    std::pair<int, int> sc[128]; std::vector<std::pair<int, int>> big;
    std::pair<int, int>* a = sc; size_t k = S.size();
    if (k > 128) { big.resize(k); a = big.data(); }
    for (size_t i = 0; i < k; ++i) a[i] = {blk[S[i]], pos[S[i]]};
    std::sort(a, a + k);
    double s = 0; size_t i = 0;
    while (i < k) {
      int b = a[i].first; uint32_t code = 0;
      while (i < k && a[i].first == b) { code |= (1u << a[i].second); ++i; }
      s += logr[b][code];
    }
    return s;
  }
};
// core/cpp/v3_start.h:76-98 (tables) and :101-157 (start), with the stand-in scorer.
inline void build_start(Start& st, const Data& D, const std::vector<std::vector<int>>& blocks) {
  st.D = &D; st.blocks = blocks; st.J = (int)blocks.size();
  int K = D.K, J = st.J;
  st.blk.assign(D.p, -1); st.pos.assign(D.p, -1);
  for (int b = 0; b < J; ++b) for (size_t i = 0; i < blocks[b].size(); ++i) { st.blk[blocks[b][i]] = b; st.pos[blocks[b][i]] = (int)i; }
  st.logr.assign(J, {});
  BitScorer sc(&D); Model U;
  for (int b = 0; b < J; ++b) {
    int m = (int)blocks[b].size(); uint32_t ncode = 1u << m;
    st.logr[b].assign(ncode, std::numeric_limits<double>::quiet_NaN());
    for (uint32_t code = 0; code < ncode; ++code) {
      U.clear();
      for (int i = 0; i < m; ++i) if (code & (1u << i)) U.push_back(blocks[b][i]);
      if ((int)U.size() > K) continue;
      ScoreOut o = sc.score(U);
      st.logr[b][code] = (code == 0) ? 0.0 : o.logm - D.logm0;
    }
  }
  st.logprof.assign(J, {}); st.codes_by_size.assign(J, {}); st.sub_cum.assign(J, {});
  for (int b = 0; b < J; ++b) {
    int m = (int)blocks[b].size(), top = std::min(m, K);
    st.codes_by_size[b].assign(top + 1, {});
    for (uint32_t code = 0; code < (1u << m); ++code) { int j = __builtin_popcount(code); if (j <= top) st.codes_by_size[b][j].push_back(code); }
    st.logprof[b].assign(top + 1, NEG_INF); st.sub_cum[b].assign(top + 1, {});
    for (int j = 0; j <= top; ++j) {
      std::vector<double> lv; for (uint32_t c : st.codes_by_size[b][j]) lv.push_back(st.logr[b][c]);
      st.logprof[b][j] = log_sum_exp(lv);
      st.sub_cum[b][j] = cumulative_from_logs(lv);
    }
  }
  st.logF.assign(J + 1, std::vector<double>(K + 1, NEG_INF));
  st.logF[0][0] = 0.0;
  for (int b = 1; b <= J; ++b) {
    const auto& pr = st.logprof[b - 1];
    for (int k = 0; k <= K; ++k) {
      std::vector<double> t;
      for (int j = 0; j < (int)pr.size() && j <= k; ++j) if (st.logF[b - 1][k - j] != NEG_INF) t.push_back(pr[j] + st.logF[b - 1][k - j]);
      st.logF[b][k] = t.empty() ? NEG_INF : log_sum_exp(t);
    }
  }
  std::vector<double> lk(K + 1);
  for (int k = 0; k <= K; ++k) lk[k] = (st.logF[J][k] == NEG_INF) ? NEG_INF : D.logprior[k] + st.logF[J][k];
  st.logZbar0 = log_sum_exp(lk);
  st.size_logmass.assign(K + 1, NEG_INF);
  for (int k = 0; k <= K; ++k) st.size_logmass[k] = lk[k] - st.logZbar0;
  st.size_cum = cumulative_from_logs(lk);
  st.cond_cum.assign(J, {});
  for (int b = 0; b < J; ++b) {
    st.cond_cum[b].assign(K + 1, {});
    const auto& pr = st.logprof[b];
    for (int r = 0; r <= K; ++r) {
      std::vector<double> lj;
      for (int j = 0; j < (int)pr.size() && j <= r; ++j) lj.push_back(st.logF[b][r - j] == NEG_INF ? NEG_INF : pr[j] + st.logF[b][r - j]);
      st.cond_cum[b][r] = cumulative_from_logs(lj);
    }
  }
}
// core/cpp/v3_start.h:165-176. `nu()` returns the next uniform of the draw (slot 0, 1, ... of the caller's address).
template <class NextU>
inline void draw_pi0(const Start& st, NextU&& nu, Model& S) {
  int J = st.J;
  int k = cat_draw_gt(st.size_cum, nu());
  std::vector<int> kb(J, 0);
  int r = k;
  for (int b = J - 1; b >= 0 && r > 0; --b) { int j = cat_draw_gt(st.cond_cum[b][r], nu()); kb[b] = j; r -= j; }
  S.clear();
  for (int b = 0; b < J; ++b) {
    if (kb[b] == 0) continue;
    int i = cat_draw_gt(st.sub_cum[b][kb[b]], nu());
    uint32_t code = (uint32_t)st.codes_by_size[b][kb[b]][i];
    for (size_t t = 0; t < st.blocks[b].size(); ++t) if (code & (1u << t)) S.push_back(st.blocks[b][t]);
  }
  std::sort(S.begin(), S.end());
}
inline std::vector<std::vector<int>> contiguous_blocks(int p, int bsz) {
  std::vector<std::vector<int>> b;
  for (int j0 = 0; j0 < p; j0 += bsz) { std::vector<int> v; for (int j = j0; j < std::min(p, j0 + bsz); ++j) v.push_back(j); b.push_back(v); }
  return b;
}

// Neighbours (INTERFACES §2, CSR, rows sorted). Stand-in rule: core/cpp/v3_blocks.h:149-172 restricted to the
// window |l - j| <= w (the exact rule scans all p columns; WP2 delivers it by streamed tiles).
struct Neighbours { std::vector<int64_t> ptr; std::vector<int32_t> idx; };
inline Neighbours window_neighbours(const Data& D, int B, int w) {
  int p = D.p; double rn = std::sqrt(2.0 * std::log((double)p) / D.n);
  std::vector<std::vector<int>> N(p);
  auto corr = [&](int a, int b) {  // columns are standardised with sample sd 1: r = g / (n - 1)
    return gram(D, a, b) / std::sqrt(D.diagG[a] * D.diagG[b]);
  };
  for (int j = 0; j < p && p > 1; ++j) {
    std::vector<std::pair<double, int>> c;
    for (int l = std::max(0, j - w); l <= std::min(p - 1, j + w); ++l) if (l != j) c.push_back({-std::fabs(corr(j, l)), l});
    std::stable_sort(c.begin(), c.end());
    int above = 0; for (auto& e : c) { if (-e.first > rn) ++above; else break; }
    int keep = std::min((int)c.size(), std::min(B, std::max(1, above)));
    for (int t = 0; t < keep; ++t) { N[j].push_back(c[t].second); N[c[t].second].push_back(j); }
  }
  Neighbours nb; nb.ptr.assign(p + 1, 0);
  for (int j = 0; j < p; ++j) { std::sort(N[j].begin(), N[j].end()); N[j].erase(std::unique(N[j].begin(), N[j].end()), N[j].end()); nb.ptr[j + 1] = nb.ptr[j] + (int64_t)N[j].size(); }
  for (int j = 0; j < p; ++j) nb.idx.insert(nb.idx.end(), N[j].begin(), N[j].end());
  return nb;
}

// Synthetic AR(rho) design for tests and benchmarks (WP1 `gen` stand-in): columns restarted every 1,024 columns,
// standardised to mean 0 and sample sd 1; y = X_S0 beta + eps standardised; S0 = 5 equally spaced columns.
struct XorShiftNormal {
  uint64_t s;
  explicit XorShiftNormal(uint64_t seed) : s(seed * 0x9E3779B97F4A7C15ULL + 1) {}
  double u() { uint64_t x = splitmix64(s); return ((double)(x >> 11) + 0.5) * 0x1.0p-53; }
  double norm() { double a = u(), b = u(); return std::sqrt(-2 * std::log(a)) * std::cos(2 * M_PI * b); }
};
inline void make_ar_data(Data& D, int n, int p, double rho, uint64_t seed, double beta_scale = 1.0) {
  std::vector<double> X((size_t)n * p), y(n);
  const int CH = 1024;
  #pragma omp parallel for schedule(dynamic, 1)
  for (int c0 = 0; c0 < p; c0 += CH) {
    XorShiftNormal r(seed * 1000003ULL + (uint64_t)c0);
    std::vector<double> prev(n, 0.0);
    for (int j = c0; j < std::min(p, c0 + CH); ++j) {
      double* x = &X[(size_t)j * n];
      for (int i = 0; i < n; ++i) { double e = r.norm(); x[i] = (j == c0) ? e : rho * prev[i] + std::sqrt(1 - rho * rho) * e; prev[i] = x[i]; }
      double m = 0; for (int i = 0; i < n; ++i) m += x[i]; m /= n;
      double s = 0; for (int i = 0; i < n; ++i) { x[i] -= m; s += x[i] * x[i]; }
      s = std::sqrt(s / (n - 1)); for (int i = 0; i < n; ++i) x[i] /= s;
    }
  }
  const double beta[5] = {1.0, -0.8, 0.9, -0.7, 0.6};
  XorShiftNormal r(seed + 777);
  for (int i = 0; i < n; ++i) {
    double v = r.norm();
    for (int k = 0; k < 5 && p >= 5; ++k) v += beta_scale * beta[k] * X[(size_t)((int)std::floor((k + 0.5) * p / 5)) * n + i];
    y[i] = v;
  }
  double m = 0; for (double v : y) m += v; m /= n;
  double s = 0; for (double& v : y) { v -= m; s += v * v; }
  s = std::sqrt(s / (n - 1)); for (double& v : y) v /= s;
  data_init(D, X.data(), y.data(), n, p);
}

}  // namespace v4::island::dep
