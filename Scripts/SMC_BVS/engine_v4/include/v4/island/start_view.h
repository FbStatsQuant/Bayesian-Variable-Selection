// start_view.h -- StartView: the island's start law pi_0 and block tables as FLAT arrays (WP3_DESIGN §1.12, approved
// 11-16; gate P5). Production: a view over WP2's setup.bin sections, mapped and never expanded (INTERFACES §5.1 v0.1.20:
// blk_ptr, blk_members, blk, pos, code_ptr, logr, logprof_ptr, logprof, logF, size_logmass, size_cum, cond0 (D-31),
// scalars_f64[0] = log Zbar0). Tests and the core goldens: an owned copy flattened from dep::Start (the stand-in built by
// core's arithmetic), so every existing test runs the engine through the same type.
//
// What the island reads per draw, and how (same uniforms, same order, same bits as dep::draw_pi0 / draw_pi0_fast):
//  * size k ~ size_cum (cat_draw_gt);
//  * block sizes for b = J-1 .. 0 while r > 0: j = 0 iff u < cond0[b (K+1) + r] (the scan entry = row (b, r)'s first
//    cumulative); otherwise the row is rebuilt on the spot from logprof and logF (D-31: cond_row, core/cpp/v3_start.h:140-150),
//    and j = upper_bound(row, u);
//  * submodels for the blocks that took members, b increasing: the codes of popcount j in increasing order (WP2's static
//    codes_of_size tables for m <= 16; enumerated for larger stand-in blocks) and their within-size law rebuilt from logr
//    (D-18: core/cpp/v3_start.h:108-118), i = upper_bound(sub_cum, u).
// The arithmetic is dep.h's (cumulative_from_logs, the same loop and long double accumulation), so the bits equal the
// expanded tables; tests start_view_* compare every row and every draw with dep::Start, and the island hashes with both types.
//
// Scratch: a draw uses per-thread scratch from prepare(threads), built before the engine's parallel regions (no heap in a
// parallel region on this path; PR50 MAJOR-1 pattern). One engine at a time per view.
#pragma once
#include <omp.h>
#include <algorithm>
#include <cmath>
#include <memory>
#include <string>
#include <vector>
#include "v4/format.h"
#include "v4/island/dep.h"
#include "v4/setup.h"

namespace v4::island {

template <class T> struct Span {
  const T* p = nullptr; size_t n = 0;
  size_t size() const { return n; }
  bool empty() const { return n == 0; }
  const T& operator[](size_t i) const { return p[i]; }
  const T* data() const { return p; }
  const T* begin() const { return p; }
  const T* end() const { return p + n; }
  template <class V> void set(const V& v) { p = v.data(); n = v.size(); }
};

namespace sv_detail {
// dep::cumulative_from_logs (core/cpp/v3_start.h:21-32) into caller storage: c[0..n), e = long double scratch [n]
inline void cumulative(const double* lp, size_t n, double* c, long double* e) {
  double m = NEG_INF; for (size_t i = 0; i < n; ++i) m = std::max(m, lp[i]);
  for (size_t i = 0; i < n; ++i) c[i] = 0.0;
  if (m == NEG_INF) return;
  long double s = 0;
  for (size_t i = 0; i < n; ++i) { e[i] = (lp[i] == NEG_INF) ? 0.0L : std::exp((long double)(lp[i] - m)); s += e[i]; }
  long double acc = 0; int last = -1;
  for (size_t i = 0; i < n; ++i) { acc += e[i]; c[i] = (double)(acc / s); if (e[i] > 0) last = (int)i; }
  for (size_t i = (size_t)last; i < n; ++i) c[i] = 1.0;
}
inline int upper(const double* c, size_t n, double u) { return (int)(std::upper_bound(c, c + n, u) - c); }
inline double binom(int m, int j) { double c = 1; for (int t = 0; t < j; ++t) c = c * (m - t) / (t + 1); return c; }
}  // namespace sv_detail

struct StartView {
  static constexpr int kRow = 24;   // a conditional row has min(top_b, r) + 1 <= 21 entries (blocks <= 20 members)
  int J = 0, K = 0, p = 0, max_m = 0;
  double logZbar0 = 0;
  Span<int32_t> blk, pos, members;
  Span<int64_t> blk_ptr, code_ptr, logprof_ptr;
  Span<double> logr, logprof, logF, size_logmass, size_cum, cond0;
  std::string source;                 // "mapped" (setup.bin sections) | "owned" (flattened from dep::Start)
  std::shared_ptr<const void> keep;   // the mapped fmt::Reader, or the owned arrays

  double lr(int b, uint32_t code) const { return logr[(size_t)code_ptr[b] + code]; }
  int size(int b) const { return (int)(blk_ptr[b + 1] - blk_ptr[b]); }
  int top(int b) const { return (int)(logprof_ptr[b + 1] - logprof_ptr[b]) - 1; }
  double c0(int b, int r) const { return cond0[(size_t)b * (K + 1) + r]; }

  // core/cpp/v3_start.h:54-66 (= dep::Start::comp): blocks met by S, increasing block order, sum from 0
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
      s += lr(b, code);
    }
    return s;
  }

  // ---- per-thread draw scratch ------------------------------------------------------------------------------------
  struct Scratch {
    std::vector<std::pair<int, int>> nz;   // (block, size) of the blocks taking members, b descending
    std::vector<double> lv, sc; std::vector<long double> e; std::vector<uint32_t> codes;
    double lj[kRow], row[kRow]; long double re[kRow];
  };
  mutable std::vector<Scratch> scratch_;
  // Sizes the scratch of `threads` workers (and warms WP2's static code tables). Call before any parallel region that draws.
  void prepare(int threads) const {
    v4::setup::warm_code_tables();
    const size_t sub = (size_t)sv_detail::binom(max_m, max_m / 2);
    if ((int)scratch_.size() < threads) scratch_.resize((size_t)threads);
    for (auto& s : scratch_) {
      if (s.nz.capacity() < (size_t)K + 1) s.nz.reserve((size_t)K + 1);
      if (s.lv.size() < sub) { s.lv.resize(sub); s.sc.resize(sub); s.e.resize(sub); }
      if (max_m > 16 && s.codes.size() < sub) s.codes.resize(sub);
    }
  }
  Scratch& scr() const {
    const int t = omp_get_thread_num();
    if (t >= (int)scratch_.size()) throw v4::Error(v4::Status::internal_error, "StartView: draw scratch not prepared for thread " + std::to_string(t));
    return scratch_[(size_t)t];
  }
  // row (b, r) of the conditional block-size law into s.row; returns its length (dep: cond_cum[b][r]; D-31 cond_row)
  int cond_row(int b, int r, Scratch& s) const {
    const int len = std::min(top(b), r) + 1;
    const double* pr = &logprof[(size_t)logprof_ptr[b]];
    const double* lf = &logF[(size_t)b * (K + 1)];
    for (int j = 0; j < len; ++j) s.lj[j] = lf[r - j] == NEG_INF ? NEG_INF : pr[j] + lf[r - j];
    sv_detail::cumulative(s.lj, (size_t)len, s.row, s.re);
    return len;
  }
  // the size j of block b given r remaining and its uniform u (= cat_draw_gt(cond_cum[b][r], u))
  int block_size(int b, int r, double u, Scratch& s) const {
    if (u < c0(b, r)) return 0;
    const int len = cond_row(b, r, s);
    return sv_detail::upper(s.row, (size_t)len, u);
  }
  // the within-size law of block b at size j into s.sc[0..n) and its codes (increasing order); returns n (dep: sub_cum[b][j],
  // codes_by_size[b][j]; D-18)
  uint32_t sub_row(int b, int j, Scratch& s, const uint32_t*& cs) const {
    const int m = size(b);
    uint32_t nc = 0;
    if (m <= 16) cs = v4::setup::codes_of_size(m, j, &nc);
    else {   // stand-in blocks (tests): codes of popcount j in increasing order
      for (uint32_t c = 0; c < (1u << m); ++c) if (__builtin_popcount(c) == j) s.codes[nc++] = c;
      cs = s.codes.data();
    }
    const double* lr0 = &logr[(size_t)code_ptr[b]];
    for (uint32_t i = 0; i < nc; ++i) s.lv[i] = lr0[cs[i]];
    sv_detail::cumulative(s.lv.data(), nc, s.sc.data(), s.e.data());
    return nc;
  }
  // the submodel of block b of size j for uniform u: appends its members to S
  void submodel(int b, int j, double u, Scratch& s, Model& S) const {
    const uint32_t* cs; const uint32_t nc = sub_row(b, j, s, cs);
    const uint32_t code = cs[sv_detail::upper(s.sc.data(), nc, u)];
    const int m = size(b); const int32_t* mem = &members[(size_t)blk_ptr[b]];
    for (int t = 0; t < m; ++t) if (code & (1u << t)) S.push_back(mem[t]);
  }

  // section bytes the view references (the plan's caller-supplied term for the start law; mapped pages)
  uint64_t bytes() const {
    return 4 * (blk.size() + pos.size() + members.size()) + 8 * (blk_ptr.size() + code_ptr.size() + logprof_ptr.size())
         + 8 * (logr.size() + logprof.size() + logF.size() + size_logmass.size() + size_cum.size() + cond0.size());
  }
  // the per-thread scratch of `threads` workers (prepare), for the plan
  uint64_t scratch_bytes(int threads) const {
    const double sub = sv_detail::binom(max_m, max_m / 2);
    return (uint64_t)((double)threads * (sizeof(Scratch) + 8.0 * (K + 1) + sub * (8 + 8 + 16) + (max_m > 16 ? 4 * sub : 0) + 64));
  }

  // ---- construction ---------------------------------------------------------------------------------------------------
  // An owned flat copy of a dep::Start (tests, the core goldens, the synthetic benchmarks); bits unchanged.
  static StartView from(const dep::Start& st);
  void finish() {   // derived fields after the spans are set
    J = (int)blk_ptr.size() - 1; max_m = 0;
    for (int b = 0; b < J; ++b) max_m = std::max(max_m, size(b));
  }
};

namespace sv_detail {
struct Owned {
  std::vector<int32_t> blk, pos, members;
  std::vector<int64_t> blk_ptr, code_ptr, logprof_ptr;
  std::vector<double> logr, logprof, logF, size_logmass, size_cum, cond0;
};
}  // namespace sv_detail

inline StartView StartView::from(const dep::Start& st) {
  auto o = std::make_shared<sv_detail::Owned>();
  const int J = st.J, K = st.D ? st.D->K : (int)st.size_logmass.size() - 1;
  o->blk.assign(st.blk.begin(), st.blk.end()); o->pos.assign(st.pos.begin(), st.pos.end());
  o->blk_ptr.assign(1, 0);
  for (int b = 0; b < J; ++b) { o->members.insert(o->members.end(), st.blocks[b].begin(), st.blocks[b].end()); o->blk_ptr.push_back((int64_t)o->members.size()); }
  o->code_ptr.assign(st.code_ptr.begin(), st.code_ptr.end()); o->logr = st.logr_flat;
  if (o->code_ptr.size() != (size_t)J + 1) {   // a Start whose flat copy was not built (logr edited without build_sampler)
    o->code_ptr.assign(1, 0); o->logr.clear();
    for (int b = 0; b < J; ++b) { o->logr.insert(o->logr.end(), st.logr[b].begin(), st.logr[b].end()); o->code_ptr.push_back((int64_t)o->logr.size()); }
  }
  o->logprof_ptr.assign(1, 0);
  for (int b = 0; b < J; ++b) { o->logprof.insert(o->logprof.end(), st.logprof[b].begin(), st.logprof[b].end()); o->logprof_ptr.push_back((int64_t)o->logprof.size()); }
  for (int b = 0; b <= J; ++b) o->logF.insert(o->logF.end(), st.logF[b].begin(), st.logF[b].end());
  o->size_logmass = st.size_logmass; o->size_cum = st.size_cum;
  o->cond0.assign((size_t)J * (K + 1), 1.0);
  for (int b = 0; b < J; ++b) for (int r = 0; r <= K; ++r) if (!st.cond_cum[b][r].empty()) o->cond0[(size_t)b * (K + 1) + r] = st.cond_cum[b][r][0];
  StartView v; v.K = K; v.p = (int)st.blk.size(); v.logZbar0 = st.logZbar0; v.source = "owned";
  v.blk.set(o->blk); v.pos.set(o->pos); v.members.set(o->members); v.blk_ptr.set(o->blk_ptr); v.code_ptr.set(o->code_ptr);
  v.logprof_ptr.set(o->logprof_ptr); v.logr.set(o->logr); v.logprof.set(o->logprof); v.logF.set(o->logF);
  v.size_logmass.set(o->size_logmass); v.size_cum.set(o->size_cum); v.cond0.set(o->cond0);
  v.keep = o; v.finish();
  return v;
}

// core/cpp/v3_start.h:165-176 on the view: dep::draw_pi0's consumption (SIZE; BLOCKSIZE b = J-1 .. 0 while r > 0;
// SUBMODEL b increasing for the blocks with k_b > 0) and result. Serial streams (compat) and addressed uniforms.
template <class NextU>
inline void draw_pi0(const StartView& st, NextU&& nu, Model& S) {
  StartView::Scratch& s = st.scr();
  const int k = sv_detail::upper(st.size_cum.data(), st.size_cum.size(), nu(v4::slot_of(v4::SK_PI0_SIZE, 0)));
  s.nz.clear();
  int r = k;
  for (int b = st.J - 1; b >= 0 && r > 0; --b) {
    const int j = st.block_size(b, r, nu(v4::slot_of(v4::SK_PI0_BLOCKSIZE, (uint32_t)b)), s);
    if (j) { s.nz.push_back({b, j}); r -= j; }
  }
  S.clear();
  for (auto it = s.nz.rbegin(); it != s.nz.rend(); ++it)
    st.submodel(it->first, it->second, nu(v4::slot_of(v4::SK_PI0_SUBMODEL, (uint32_t)it->first)), s, S);
  std::sort(S.begin(), S.end());
}
// dep::draw_pi0_fast on the view (addressed uniforms only; L5): 8 BLOCKSIZE uniforms at once against the scan entries
// cond0[(b - l)(K+1) + r] (dep's r-major c0r, gathered with stride K + 1), the full row only for a block that takes members.
template <class NextU, class NextU8>
inline void draw_pi0_fast(const StartView& st, NextU&& nu, NextU8&& nu8, Model& S) {
  StartView::Scratch& s = st.scr();
  const int k = sv_detail::upper(st.size_cum.data(), st.size_cum.size(), nu(v4::slot_of(v4::SK_PI0_SIZE, 0)));
  s.nz.clear();
  int r = k, b = st.J - 1;
  uint32_t slots[8]; double u8[8];
  while (b >= 0 && r > 0) {
    const int nl = std::min(8, b + 1);
    for (int l = 0; l < 8; ++l) slots[l] = v4::slot_of(v4::SK_PI0_BLOCKSIZE, (uint32_t)std::max(0, b - l));
    nu8(slots, u8);
    int l = 0;
    while (l < nl && u8[l] < st.c0(b - l, r)) ++l;
    if (l == nl) { b -= nl; continue; }
    const int bb = b - l;
    const int len = st.cond_row(bb, r, s);
    const int j = sv_detail::upper(s.row, (size_t)len, u8[l]);
    s.nz.push_back({bb, j}); r -= j; b = bb - 1;
  }
  S.clear();
  for (auto it = s.nz.rbegin(); it != s.nz.rend(); ++it)
    st.submodel(it->first, it->second, nu(v4::slot_of(v4::SK_PI0_SUBMODEL, (uint32_t)it->first)), s, S);
  std::sort(S.begin(), S.end());
}

}  // namespace v4::island
