// dep.h -- what the island takes from WP1 (adopted: INTERFACES v0.1.1, PR #11) and the WP2 stand-ins it still needs.
//
// From WP1 (used directly): Data / DataOwned / make_data / gram / log_sum_exp / lchoose_d (data.h), Model /
// ModelView / Zobrist / lex_less / hpm_better / sorted_insert (model.h), Philox addresses (rng.h), pm:: (pmath.h),
// Scorer<Arith::Bit> (score.h), Status / NumericalFailure (status.h), Phase / Mech / Segment / EventKey / Order
// (ledger.h, store.h), MoveStats / StageRow (records.h).
// Stand-ins kept here until WP2's setup.h lands (arithmetic copied from core/ and cited):
//   Start (blocks, tables, sampler, comp, pi0 draw) .... core/cpp/v3_start.h:14-31, 54-66, 76-176
//   Neighbours CSR + a windowed neighbour rule ........ core/cpp/v3_blocks.h:149-172 (window |l - j| <= w)
//   synthetic AR(rho) data for tests and benchmarks ... (WP1 gen + prep give the production data)
#pragma once
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <limits>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
#include "v4/data.h"
#include "v4/ledger.h"
#include "v4/model.h"
#include "v4/pmath.h"
#include "v4/records.h"
#include "v4/rng.h"
#include "v4/score.h"
#include "v4/status.h"
#include "v4/store.h"

namespace v4::island::dep {
using v4::Data; using v4::DataOwned; using v4::Model; using v4::ModelView; using v4::NEG_INF; using v4::POS_INF;
using v4::NumericalFailure; using v4::BitScorer; using v4::Address; using v4::uniform_at;
using v4::ScoreOut; using v4::gram; using v4::log_sum_exp; using v4::lchoose_d; using v4::splitmix64; using v4::sorted_insert; using v4::sorted_erase;
using v4::hpm_better; using v4::R_FINAL; using v4::X_INIT; using v4::X_RESAMPLE; using v4::X_BRIDGE; using v4::X_BURN; using v4::X_MEASURED;
namespace pm = v4::pm;

// core/cpp/v3_util.h:88-92 (plogis_log), copied
inline double plogis_log(double la) {
  if (la >= 0) return 1.0 / (1.0 + pm::exp(-la));
  double e = pm::exp(la);
  return e / (1.0 + e);
}
inline bool lex_less(const int32_t* a, size_t na, const int32_t* b, size_t nb) { return std::lexicographical_compare(a, a + na, b, b + nb); }
inline bool lex_less(const Model& a, const Model& b) { return lex_less(a.data(), a.size(), b.data(), b.size()); }
inline bool contains(const Model& v, int32_t j) { return std::binary_search(v.begin(), v.end(), j); }
inline uint64_t zobrist(const Data& D, const Model& S) { return D.zob.hash(S); }

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
  std::vector<int64_t> code_ptr; std::vector<double> logr_flat;   // flat copy (INTERFACES §2 Tables layout)
  // r-major table of P(k_b = 0 | remaining r) = cond_cum[b][r][0], (K+1) x J, for the vectorised pi_0 draw (L5)
  std::vector<double> c0r;
  inline double lr(int b, uint32_t code) const { return logr_flat[code_ptr[b] + code]; }
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
inline void build_sampler(Start& st, const Data& D);
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
  build_sampler(st, D);
}
// The sampler tables and log Zbar_0 from st.logr (second half of core/cpp/v3_start.h:101-157); tests may edit logr first.
inline void build_sampler(Start& st, const Data& D) {
  const int K = D.K, J = st.J;
  st.code_ptr.assign(J + 1, 0);
  for (int b = 0; b < J; ++b) st.code_ptr[b + 1] = st.code_ptr[b] + (int64_t)st.logr[b].size();
  st.logr_flat.clear(); for (int b = 0; b < J; ++b) st.logr_flat.insert(st.logr_flat.end(), st.logr[b].begin(), st.logr[b].end());
  st.logprof.assign(J, {}); st.codes_by_size.assign(J, {}); st.sub_cum.assign(J, {});
  for (int b = 0; b < J; ++b) {
    int m = (int)st.blocks[b].size(), top = std::min(m, K);
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
  st.c0r.assign((size_t)(K + 1) * J, 0.0);
  for (int b = 0; b < J; ++b) for (int r = 0; r <= K; ++r) st.c0r[(size_t)r * J + b] = st.cond_cum[b][r].empty() ? 1.0 : st.cond_cum[b][r][0];
}
// core/cpp/v3_start.h:165-176. `nu(slot)` returns the uniform at the caller's address with that slot; slots follow
// INTERFACES v0.1.5 §3: PI0_SIZE 0, PI0_BLOCKSIZE b (b = J-1 .. 0 while r > 0), PI0_SUBMODEL b (k_b > 0, b increasing).
template <class NextU>
inline void draw_pi0(const Start& st, NextU&& nu, Model& S) {
  int J = st.J;
  int k = cat_draw_gt(st.size_cum, nu(v4::slot_of(v4::SK_PI0_SIZE, 0)));
  std::vector<int> kb(J, 0);
  int r = k;
  for (int b = J - 1; b >= 0 && r > 0; --b) { int j = cat_draw_gt(st.cond_cum[b][r], nu(v4::slot_of(v4::SK_PI0_BLOCKSIZE, (uint32_t)b))); kb[b] = j; r -= j; }
  S.clear();
  for (int b = 0; b < J; ++b) {
    if (kb[b] == 0) continue;
    int i = cat_draw_gt(st.sub_cum[b][kb[b]], nu(v4::slot_of(v4::SK_PI0_SUBMODEL, (uint32_t)b)));
    uint32_t code = (uint32_t)st.codes_by_size[b][kb[b]][i];
    for (size_t t = 0; t < st.blocks[b].size(); ++t) if (code & (1u << t)) S.push_back(st.blocks[b][t]);
  }
  std::sort(S.begin(), S.end());
}
// The same draw as draw_pi0 (identical uniforms, identical result), for addressed uniforms (L5): block b takes size
// 0 exactly when u_b < cond_cum[b][r][0] (cat_draw_gt: the smallest index with cum > u), so 8 blocks are checked at
// once against the r-major table c0r with 8 uniforms nu8(slots) of the BLOCKSIZE slots; the full categorical runs only
// for the blocks that take members. Lanes past the stopping point are computed but never used (a computed value is
// not a consumed one). Not for serial streams (compat), whose consumption must stop exactly where core's does.
template <class NextU, class NextU8>
inline void draw_pi0_fast(const Start& st, NextU&& nu, NextU8&& nu8, Model& S) {
  const int J = st.J;
  int k = cat_draw_gt(st.size_cum, nu(v4::slot_of(v4::SK_PI0_SIZE, 0)));
  thread_local std::vector<std::pair<int, int>> nz; nz.clear();   // (block, size) of the blocks taking members, b descending
  int r = k, b = J - 1;
  uint32_t slots[8]; double u8[8];
  while (b >= 0 && r > 0) {
    const int nl = std::min(8, b + 1);
    for (int l = 0; l < 8; ++l) slots[l] = v4::slot_of(v4::SK_PI0_BLOCKSIZE, (uint32_t)std::max(0, b - l));
    nu8(slots, u8);
    const double* c0 = &st.c0r[(size_t)r * J];
    int l = 0;
    while (l < nl && u8[l] < c0[b - l]) ++l;
    if (l == nl) { b -= nl; continue; }
    const int bb = b - l;
    const int j = cat_draw_gt(st.cond_cum[bb][r], u8[l]);
    nz.push_back({bb, j}); r -= j; b = bb - 1;
  }
  S.clear();
  for (auto it = nz.rbegin(); it != nz.rend(); ++it) {   // submodels for b increasing, as draw_pi0
    const int bb = it->first, kb = it->second;
    int i = cat_draw_gt(st.sub_cum[bb][kb], nu(v4::slot_of(v4::SK_PI0_SUBMODEL, (uint32_t)bb)));
    uint32_t code = (uint32_t)st.codes_by_size[bb][kb][i];
    for (size_t t = 0; t < st.blocks[bb].size(); ++t) if (code & (1u << t)) S.push_back(st.blocks[bb][t]);
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
  auto own = std::make_shared<DataOwned>();
  std::vector<double>& X = own->X; std::vector<double>& y = own->y;
  X.assign((size_t)n * p, 0.0); y.assign(n, 0.0);
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
  D = make_data(own, n, p);
}

}  // namespace v4::island::dep
