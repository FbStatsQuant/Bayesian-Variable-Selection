// tables.cpp -- block tables by depth-first enumeration with sorted-prefix reuse (bits of core/cpp/v3_start.h:76-98),
// threaded over blocks; table top stores; size profiles, convolutions, log Zbar0 and sampler tables (bits of
// core/cpp/v3_start.h:101-151), in flat arrays.
#include <omp.h>
#include <algorithm>
#include <atomic>
#include <chrono>
#include "v4/setup.h"
#include "v4/score.h"

namespace v4::setup {

namespace testing { static int g_force_fallback = 0; void set_force_fallback(int every) { g_force_fallback = every; } }

namespace {
// Prefix-reuse scorer for one block. For a sorted model U = (u_0 < ... < u_{k-1}) the Cholesky factors of
// H = (n+1) G_U + I and A = G_U + I computed by core/cpp/v3_score.h:76-90 have rows 0..k-2 equal to the factors of
// U minus its last member: entry (i, j) is (A_ij - sum_{t<j} L_it L_jt) / L_jj with the sum in increasing t, which
// reads only rows <= max(i, j). The same holds for the forward solve w (core/cpp/v3_score.h:92-94) and for the
// sequential sums log det and z'H^{-1}z (core/cpp/v3_score.h:206-217): each is a running sum from index 0, so the value
// for U is the value for the prefix plus one more term, added in the same order. Only row k-1 is new at depth k.
// Entries that leave the plain Cholesky route (a failed pivot in the prefix or now, log m not finite, or Q below
// 1e-8 y'y, which recomputes Q) are scored by the full copy of the v3 scorer (RefScorer); everything else gives the
// bits of core/cpp/v3_score.h:212-217 on route chol. (Entries that leave it are scored by WP1's BitScorer.)
struct PrefixScorer {
  const Data& D; BitScorer ref; int B;
  std::vector<double> LH, LA, w, ldH, ldA, quad;  // stride B; per-depth running sums at index depth
  std::vector<char> okd;                          // prefix of depth d factorised on the chol route
  std::vector<int32_t> U;
  explicit PrefixScorer(const Data& d, int b) : D(d), ref(&d), B(b) {
    LH.assign((size_t)B * B, 0); LA.assign((size_t)B * B, 0); w.assign(B, 0);
    ldH.assign(B + 1, 0); ldA.assign(B + 1, 0); quad.assign(B + 1, 0); okd.assign(B + 1, 1);
  }
  // push member u at depth k-1 (U has k-1 members before); returns false if the chol route fails at this depth
  bool push(int32_t u) {
    U.push_back(u);
    const int k = (int)U.size(), r = k - 1;
    if (!okd[r]) { okd[k] = 0; return false; }
    const double n1 = D.n + 1.0;
    double* lh = &LH[(size_t)r * B]; double* la = &LA[(size_t)r * B];
    for (int c = 0; c < k; ++c) {
      double g = gram(D, U[r], U[c]);
      lh[c] = n1 * g + (r == c ? 1.0 : 0.0);  // core/cpp/v3_score.h:178-181
      la[c] = g + (r == c ? 1.0 : 0.0);
    }
    for (int c = 0; c < r; ++c) {  // row r, columns < r (core/cpp/v3_score.h:83-86)
      double sh = lh[c], sa = la[c];
      const double* hc = &LH[(size_t)c * B]; const double* ac = &LA[(size_t)c * B];
      for (int t = 0; t < c; ++t) { sh -= lh[t] * hc[t]; sa -= la[t] * ac[t]; }
      lh[c] = sh / hc[c]; la[c] = sa / ac[c];
    }
    double dh = lh[r], da = la[r];  // pivots (core/cpp/v3_score.h:78-82); H's factorisation runs first
    for (int t = 0; t < r; ++t) dh -= lh[t] * lh[t];
    for (int t = 0; t < r; ++t) da -= la[t] * la[t];
    if (!(dh > 0) || !std::isfinite(dh) || !(da > 0) || !std::isfinite(da)) { okd[k] = 0; return false; }
    lh[r] = std::sqrt(dh); la[r] = std::sqrt(da);
    ldH[k] = ldH[r] + pm::log(lh[r]); ldA[k] = ldA[r] + pm::log(la[r]);
    double s = D.z[U[r]];
    for (int t = 0; t < r; ++t) s -= lh[t] * w[t];
    w[r] = s / lh[r];
    quad[k] = quad[r] + w[r] * w[r];
    okd[k] = 1;
    return true;
  }
  void pop() { U.pop_back(); }
  // log m and route of the current U (|U| >= 1)
  uint64_t calls = 0;
  double score(int& route, bool& prefix) {
    const int k = (int)U.size();
    ++calls;
    const bool force = testing::g_force_fallback > 0 && calls % testing::g_force_fallback == 0;
    if (okd[k] && !force) {
      double Q = D.yty - D.n * quad[k];
      if (!(Q < 1e-8 * D.yty)) {
        double ldh = ldH[k] * 2, lda = ldA[k] * 2;
        double arg = 2 * D.b0 + Q;
        double lm = (arg > 0) ? D.logCn - 0.5 * (ldh - lda) - D.nu * pm::log(arg) : NEG_INF;
        if (std::isfinite(lm)) { route = 0; prefix = true; return lm; }
      }
    }
    prefix = false;
    ScoreOut o = ref.score(ModelView(U.data(), (uint32_t)k));  // WP1's Bit scorer: the bits of core/cpp/v3_score.h:212-224
    route = o.route;
    return o.logm;
  }
};

struct BlockOut { uint64_t scored = 0, prefix = 0, fallback = 0, routes[3] = {0, 0, 0}; };

void score_block(const Data& D, const int32_t* mem, int m, PrefixScorer& ps, double* logr, double* logm, BlockOut& bo) {
  const uint32_t ncode = 1u << m;
  for (uint32_t c = 0; c < ncode; ++c) { logr[c] = std::numeric_limits<double>::quiet_NaN(); logm[c] = logr[c]; }
  logr[0] = 0.0; logm[0] = D.logm0;  // core/cpp/v3_start.h:93-95 for code 0 (score(empty) = log m0, route chol)
  bo.scored++; bo.routes[0]++;
  // depth-first over subsets in increasing member order; code bit i <-> member i
  struct Fr { int next; uint32_t code; };
  Fr st[17]; int depth = 0; st[0] = {0, 0};
  while (depth >= 0) {
    Fr& f = st[depth];
    if (f.next >= m || depth >= D.K) {  // no extension (|U| would exceed K: entries stay NaN, not scored)
      if (depth > 0) ps.pop();
      --depth; continue;
    }
    int i = f.next++;
    uint32_t code = f.code | (1u << i);
    ps.push(mem[i]);
    int route; bool pre;
    double lm = ps.score(route, pre);
    logm[code] = lm; logr[code] = lm - D.logm0;  // core/cpp/v3_start.h:95
    bo.scored++; bo.routes[route]++; (pre ? bo.prefix : bo.fallback)++;
    st[++depth] = {i + 1, code};
  }
}

// The c-th largest of val(b, code) over all table models (the empty model once), by histogram selection: one pass
// for the range, one histogram pass (2^20 bins, per-thread counts), then the bin holding rank c is collected and
// selected exactly (refined recursively while it is large). Returns -inf if there are at most c table models.
template <class Val>
double kth_largest(const Tables& T, const Partition& P, uint64_t c, int TH, Val val) {
  auto for_all = [&](auto&& f) {   // f(tid, value); per-thread, order-free
#pragma omp parallel for num_threads(TH) schedule(dynamic, 64)
    for (int b = 0; b < P.J; ++b) {
      const int tid = omp_get_thread_num();
      const double* lr = &T.logr[T.code_ptr[b]];
      for (uint32_t code = (b == 0 ? 0u : 1u); code < (1u << P.size(b)); ++code) if (!std::isnan(lr[code])) f(tid, val(b, code));
    }
  };
  double lo = POS_INF, hi = NEG_INF; uint64_t N = 0;
  {
    std::vector<double> l(TH, POS_INF), h(TH, NEG_INF); std::vector<uint64_t> n(TH, 0);
    for_all([&](int t, double v) { l[t] = std::min(l[t], v); h[t] = std::max(h[t], v); n[t]++; });
    for (int t = 0; t < TH; ++t) { lo = std::min(lo, l[t]); hi = std::max(hi, h[t]); N += n[t]; }
  }
  if (N <= c || c == 0) return NEG_INF;
  uint64_t rank = c;   // we want the rank-th largest within [lo, hi]
  for (int depth = 0; depth < 8; ++depth) {
    if (!(hi > lo)) return lo;
    const int NB = 1 << 20;
    const double w = (hi - lo) / NB;
    auto bin = [&](double v) { int k = (int)((v - lo) / w); return std::min(std::max(k, 0), NB - 1); };
    std::vector<std::vector<uint64_t>> cnt(TH, std::vector<uint64_t>(NB, 0));
    for_all([&](int t, double v) { if (v >= lo && v <= hi) cnt[t][bin(v)]++; });
    for (int t = 1; t < TH; ++t) for (int k = 0; k < NB; ++k) cnt[0][k] += cnt[t][k];
    uint64_t above = 0; int kb = NB - 1;
    for (; kb >= 0; --kb) { if (above + cnt[0][kb] >= rank) break; above += cnt[0][kb]; }
    const uint64_t inbin = cnt[0][kb];
    rank -= above;
    // the bin's exact value range: values v with bin(v) == kb
    std::vector<std::vector<double>> got(TH);
    if (inbin <= (uint64_t)50000000 || depth == 7) {
      for_all([&](int t, double v) { if (v >= lo && v <= hi && bin(v) == kb) got[t].push_back(v); });
      std::vector<double> all; for (auto& g : got) all.insert(all.end(), g.begin(), g.end());
      std::nth_element(all.begin(), all.begin() + (rank - 1), all.end(), std::greater<double>());
      return all[rank - 1];
    }
    // refine: new [lo, hi] = the bin's value range
    double nlo = POS_INF, nhi = NEG_INF;
    std::vector<double> l(TH, POS_INF), h(TH, NEG_INF);
    for_all([&](int t, double v) { if (v >= lo && v <= hi && bin(v) == kb) { l[t] = std::min(l[t], v); h[t] = std::max(h[t], v); } });
    for (int t = 0; t < TH; ++t) { nlo = std::min(nlo, l[t]); nhi = std::max(nhi, h[t]); }
    lo = nlo; hi = nhi;
  }
  return lo;
}
}  // namespace

Tables build_tables(const Data& D, const Partition& P, int threads, TableStores* stores, TableStats* stats) {
  auto t0 = std::chrono::steady_clock::now();
  Tables T; T.J = P.J; T.K = D.K;
  T.code_ptr.assign(P.J + 1, 0);
  for (int b = 0; b < P.J; ++b) {
    if (P.size(b) < 1 || P.size(b) > 16) throw Error(Status::invalid_input, "build_tables: block size outside 1..16");
    T.code_ptr[b + 1] = T.code_ptr[b] + ((int64_t)1 << P.size(b));
  }
  T.logr.assign(T.code_ptr.back(), 0.0);
  const int TH = std::max(1, threads);
  const uint64_t p = (uint64_t)D.p;
  if (stores) {  // core/cpp/v3_ledger.h:78 capacities and orders
    stores->top.init(40 * p + 1, Order::HPM); stores->lead0.init(20 * p, Order::LEX); stores->lead1.init(20 * p, Order::LEX);
  }
  // Streaming, two passes (Sol review F1 item 3; PR13 review m2). No per-code log m or route array ever exists
  // globally, and the stores never see more than about their capacity:
  //  pass 1: threads score the blocks in batches of TH * CH consecutive blocks (fixed chunks of CH blocks); only logr
  //          is kept;
  //  thresholds: for each store, the c-th largest value over all table models, found by a histogram selection from
  //          logr alone: lg0 = log varpi(k) + logr is exact; F is approximated by log varpi(k) + (logr + log m0), which
  //          differs from F by a few ulps (logr = fl(log m - log m0)), so the offer bound is lowered by a margin;
  //  pass 2: the batches are re-scored (same bits) and only table models at or above the bounds are offered, serially in
  //          (block, code) order (core/cpp/v3_core.cpp:375-383) with the exact F.
  // Store content is the top-c under a strict total order of everything offered, and every model of the true top-c is
  // offered, so the result is that of offering every table model, for any TH.
  const int CH = 16;
  std::vector<std::vector<double>> lm(TH * CH);  // one buffer per block slot of a batch
  std::vector<BlockOut> outs(TH);
  std::vector<PrefixScorer> ps; ps.reserve(TH);
  for (int t = 0; t < TH; ++t) ps.emplace_back(D, 16);
  std::atomic<bool> failed{false}; std::string fail_msg; Status fail_st = Status::internal_error;
  TableStats st;
  double sec_stores = 0;
  Model U;
  double loF = NEG_INF, lo0 = NEG_INF;
  auto run_pass = [&](bool offer) {
    for (int b0 = 0; b0 < P.J && !failed; b0 += TH * CH) {
      const int b1 = std::min(P.J, b0 + TH * CH);
      const int nch = (b1 - b0 + CH - 1) / CH;
#pragma omp parallel for num_threads(TH) schedule(dynamic, 1)
      for (int c = 0; c < nch; ++c) {
        const int tid = omp_get_thread_num();
        for (int b = b0 + c * CH; b < std::min(b1, b0 + (c + 1) * CH) && !failed; ++b) {
          try {
            std::vector<double>& buf = lm[b - b0];
            buf.resize((size_t)1 << P.size(b));
            ps[tid].U.clear();
            BlockOut dummy;
            score_block(D, P.block(b), P.size(b), ps[tid], &T.logr[T.code_ptr[b]], buf.data(), offer ? dummy : outs[tid]);
          } catch (const Error& e) {
#pragma omp critical(v4_tables_err)
            { if (!failed) { failed = true; fail_msg = e.what(); fail_st = e.st; } }
          } catch (const std::bad_alloc&) {   // PR13 review m8: nothing escapes the OpenMP region
#pragma omp critical(v4_tables_err)
            { if (!failed) { failed = true; fail_msg = "out of memory"; fail_st = Status::resource_limit; } }
          } catch (...) {
#pragma omp critical(v4_tables_err)
            { if (!failed) { failed = true; fail_msg = "unexpected exception"; fail_st = Status::internal_error; } }
          }
        }
      }
      if (failed || !offer) continue;
      auto ts = std::chrono::steady_clock::now();
      for (int b = b0; b < b1; ++b) {
        const int m = P.size(b);
        const double* logm = lm[b - b0].data();
        const double* lr = &T.logr[T.code_ptr[b]];
        for (uint32_t c = (b == 0 ? 0u : 1u); c < (1u << m); ++c) {  // the empty model once (block 0, code 0)
          if (std::isnan(lr[c])) continue;                             // |U| > K: not scored (core/cpp/v3_core.cpp:378)
          const int k = __builtin_popcount(c);
          const double F = D.logprior[k] + logm[c], lg0 = D.logprior[k] + lr[c];   // core/cpp/v3_core.cpp:381
          if (!std::isfinite(F) || !std::isfinite(lg0)) throw Error(Status::internal_error, "tables: non-finite table value");
          const bool tF = F >= loF, t0 = lg0 >= lo0;
          if (!tF && !t0) continue;
          const bool t1 = tF && F >= stores->top.cutoff(), t2 = t0 && lg0 >= stores->lead0.cutoff(), t3 = tF && F >= stores->lead1.cutoff();
          if (!t1 && !t2 && !t3) continue;
          U.clear(); for (int i = 0; i < m; ++i) if (c & (1u << i)) U.push_back(P.block(b)[i]);
          const uint64_t h = D.zob.hash(U);
          if (t1) stores->top.offer(F, U, h);
          if (t2) stores->lead0.offer(lg0, U, h);
          if (t3) stores->lead1.offer(F, U, h);
        }
      }
      sec_stores += std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
    }
  };
  run_pass(false);
  if (!failed && stores) {
    auto ts = std::chrono::steady_clock::now();
    auto Fa = [&](int b, uint32_t c) { return D.logprior[__builtin_popcount(c)] + (T.logr[T.code_ptr[b] + c] + D.logm0); };
    auto L0 = [&](int b, uint32_t c) { return D.logprior[__builtin_popcount(c)] + T.logr[T.code_ptr[b] + c]; };
    const uint64_t capF = 40 * p + 1;   // top (the larger of the two F stores)
    const double vF = kth_largest(T, P, capF, TH, Fa), v0 = kth_largest(T, P, 20 * p, TH, L0);
    // |F - Fa| <= a few ulps of (|log varpi| + |log m| + |log m0|); the margin is generous (candidates in it are few)
    loF = (vF == NEG_INF) ? NEG_INF : vF - 1e-9 * (1.0 + std::fabs(vF) + 2.0 * std::fabs(D.logm0));
    lo0 = v0;
    sec_stores += std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
    run_pass(true);
  }
  if (failed) throw Error(fail_st, "tables: " + fail_msg);
  for (auto& o : outs) { st.scored += o.scored; st.prefix_scored += o.prefix; st.fallback_scored += o.fallback; for (int r = 0; r < 3; ++r) st.routes[r] += o.routes[r]; }
  if (stores) {
    auto ts = std::chrono::steady_clock::now();
    stores->top.compact(); stores->lead0.compact(); stores->lead1.compact();
    // table HPM = the first entry under the HPM order; provenance = its first table event (block, code) in the order
    // of core/cpp/v3_core.cpp:375-383 (the empty model: block 0, code 0)
    const Store& top = stores->top;
    if (top.size() > 0) {
      ModelView h = top.model(0);
      stores->hpmS.assign(h.begin(), h.end());
      stores->hpmF = top.v[0];
      if (stores->hpmS.empty()) { stores->hpm_block = 0; stores->hpm_code = 0; }
      else {
        uint32_t c = 0;
        for (int32_t j : stores->hpmS) c |= 1u << P.pos[j];
        stores->hpm_block = P.blk[stores->hpmS[0]]; stores->hpm_code = c;
      }
    }
    sec_stores += std::chrono::duration<double>(std::chrono::steady_clock::now() - ts).count();
  }
  st.seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  st.seconds_stores = sec_stores;
  if (stats) *stats = st;
  return T;
}

// ---------------------------------------------------------------- start law
// core/cpp/v3_start.h:21-32
void cumulative_from_logs(const double* lp, size_t n, double* c) {
  std::vector<long double> e(n);
  cumulative_from_logs(lp, n, c, e.data());
}
void cumulative_from_logs(const double* lp, size_t n, double* c, long double* e) {
  double m = NEG_INF; for (size_t i = 0; i < n; ++i) m = std::max(m, lp[i]);
  for (size_t i = 0; i < n; ++i) c[i] = 0.0;
  if (m == NEG_INF) return;
  long double s = 0;
  for (size_t i = 0; i < n; ++i) { e[i] = (lp[i] == NEG_INF) ? 0.0L : pm::expl((long double)(lp[i] - m)); s += e[i]; }
  long double acc = 0; int last = -1;
  for (size_t i = 0; i < n; ++i) { acc += e[i]; c[i] = (double)(acc / s); if (e[i] > 0) last = (int)i; }
  for (size_t i = (size_t)last; i < n; ++i) c[i] = 1.0;
}

// One table per block size m (computed once, thread-safe static): all codes sorted by (popcount, code), with the
// offset of each popcount. Same order as core/cpp/v3_start.h:108-112 (increasing code within each size).
namespace {
struct CodeTable { std::vector<uint32_t> codes; uint32_t off[18]; };
const CodeTable& code_table(int m) {
  static const std::vector<CodeTable> tabs = [] {
    std::vector<CodeTable> t(17);
    for (int mm = 0; mm <= 16; ++mm) {
      CodeTable& c = t[mm];
      uint32_t cnt[18] = {0};
      for (uint32_t code = 0; code < (1u << mm); ++code) cnt[__builtin_popcount(code) + 1]++;
      c.off[0] = 0; for (int j = 0; j <= 16; ++j) c.off[j + 1] = c.off[j] + cnt[j + 1];
      c.codes.assign(1u << mm, 0);
      uint32_t fill[17]; for (int j = 0; j <= 16; ++j) fill[j] = c.off[j];
      for (uint32_t code = 0; code < (1u << mm); ++code) c.codes[fill[__builtin_popcount(code)]++] = code;
    }
    return t;
  }();
  return tabs[m];
}
}  // namespace
void warm_code_tables() { (void)code_table(0); }
const uint32_t* codes_of_size(int m, int j, uint32_t* count) {
  if (m < 0 || m > 16 || j < 0 || j > m) throw Error(Status::internal_error, "codes_of_size: m or j out of range");
  const CodeTable& c = code_table(m);
  *count = c.off[j + 1] - c.off[j];
  return c.codes.data() + c.off[j];
}
void sub_cum_of(const Tables& T, int b, int m, int j, std::vector<double>& out) {
  thread_local std::vector<double> lv;
  uint32_t n; const uint32_t* codes = codes_of_size(m, j, &n);
  const double* lr = &T.logr[T.code_ptr[b]];
  lv.resize(n); for (uint32_t q = 0; q < n; ++q) lv[q] = lr[codes[q]];
  out.resize(n);
  cumulative_from_logs(lv.data(), n, out.data());  // core/cpp/v3_start.h:118
}
DrawScratch::DrawScratch(int K) : lv(kMaxSub), sc(kMaxSub), e(kMaxSub) {
  warm_code_tables();
  kb.reserve((size_t)std::max(K, 0) + 1);
}
int sub_cum_of(const Tables& T, int b, int m, int j, DrawScratch& s) {
  uint32_t n; const uint32_t* codes = codes_of_size(m, j, &n);
  const double* lr = &T.logr[T.code_ptr[b]];
  for (uint32_t q = 0; q < n; ++q) s.lv[q] = lr[codes[q]];
  cumulative_from_logs(s.lv.data(), n, s.sc.data(), s.e.data());   // core/cpp/v3_start.h:118
  return (int)n;
}

// core/cpp/v3_start.h:101-151, in flat arrays (row layouts in v4/setup.h).
void build_start(const Data& D, const Partition& P, Tables& T, bool store_sampler) {
  const int K = D.K, J = P.J;
  T.K = K; T.J = J;
  T.logprof_ptr.assign(J + 1, 0);
  for (int b = 0; b < J; ++b) T.logprof_ptr[b + 1] = T.logprof_ptr[b] + std::min(P.size(b), K) + 1;
  const int64_t NR = T.logprof_ptr[J];
  T.logprof.assign(NR, NEG_INF);
  T.cbs_ptr.assign(1, 0); T.codes_by_size.clear(); T.sub_ptr.assign(1, 0); T.sub_cum.clear();
  std::vector<double> lv, sc;
  for (int b = 0; b < J; ++b) {
    int m = P.size(b), top = std::min(m, K);
    const double* lr = &T.logr[T.code_ptr[b]];
    for (int j = 0; j <= top; ++j) {
      int64_t row = T.logprof_ptr[b] + j;
      uint32_t n; const uint32_t* codes = codes_of_size(m, j, &n);   // increasing code order (v3_start.h:108-112)
      lv.resize(n); for (uint32_t q = 0; q < n; ++q) lv[q] = lr[codes[q]];
      T.logprof[row] = log_sum_exp(lv);                              // core/cpp/v3_start.h:117
      if (store_sampler) {                                           // tests only (D-18)
        T.codes_by_size.insert(T.codes_by_size.end(), codes, codes + n);
        sc.resize(n); cumulative_from_logs(lv.data(), n, sc.data());   // core/cpp/v3_start.h:118
        T.sub_cum.insert(T.sub_cum.end(), sc.begin(), sc.end());
        T.cbs_ptr.push_back((int64_t)T.codes_by_size.size());
      }
    }
  }
  if (store_sampler) T.sub_ptr = T.cbs_ptr;
  // core/cpp/v3_start.h:121-131
  T.logF.assign((size_t)(J + 1) * (K + 1), NEG_INF);
  T.logF[0] = 0.0;
  std::vector<double> t;
  for (int b = 1; b <= J; ++b) {
    const double* pr = &T.logprof[T.logprof_ptr[b - 1]];
    const int npr = (int)(T.logprof_ptr[b] - T.logprof_ptr[b - 1]);
    const double* Fp = &T.logF[(size_t)(b - 1) * (K + 1)];
    double* Fb = &T.logF[(size_t)b * (K + 1)];
    for (int k = 0; k <= K; ++k) {
      t.clear();
      for (int j = 0; j < npr && j <= k; ++j) if (Fp[k - j] != NEG_INF) t.push_back(pr[j] + Fp[k - j]);
      Fb[k] = t.empty() ? NEG_INF : log_sum_exp(t);
    }
  }
  // core/cpp/v3_start.h:133-138
  std::vector<double> lk(K + 1);
  for (int k = 0; k <= K; ++k) lk[k] = (T.logF_at(J, k) == NEG_INF) ? NEG_INF : D.logprior[k] + T.logF_at(J, k);
  T.logZbar0 = log_sum_exp(lk);
  T.size_logmass.assign(K + 1, NEG_INF);
  for (int k = 0; k <= K; ++k) T.size_logmass[k] = lk[k] - T.logZbar0;
  T.size_cum.assign(K + 1, 0.0);
  cumulative_from_logs(lk.data(), lk.size(), T.size_cum.data());
  // core/cpp/v3_start.h:140-150. D-31: only the scan table cond0 persists; full rows are recomputed by cond_row.
  T.cond0.assign((size_t)J * (K + 1), 0.0);
  T.cond_ptr.assign(1, 0); T.cond_cum.clear();
  if (store_sampler) {   // tests only
    T.cond_ptr.assign((size_t)J * (K + 1) + 1, 0);
    for (int b = 0; b < J; ++b)
      for (int r = 0; r <= K; ++r) { size_t row = (size_t)b * (K + 1) + r; T.cond_ptr[row + 1] = T.cond_ptr[row] + T.cond_len(b, r); }
    T.cond_cum.assign(T.cond_ptr.back(), 0.0);
  }
  std::vector<double> c;
  for (int b = 0; b < J; ++b)
    for (int r = 0; r <= K; ++r) {
      const size_t row = (size_t)b * (K + 1) + r;
      cond_row(T, b, r, c);
      T.cond0[row] = c[0];
      if (store_sampler) std::copy(c.begin(), c.end(), T.cond_cum.begin() + T.cond_ptr[row]);
    }
}

int cond_row(const Tables& T, int b, int r, CondScratch& s) {
  const int K = T.K;
  const double* pr = &T.logprof[T.logprof_ptr[b]];
  const int npr = (int)(T.logprof_ptr[b + 1] - T.logprof_ptr[b]);
  const int len = std::min(npr - 1, r) + 1;
  if (len > CondScratch::kMax) throw Error(Status::internal_error, "cond_row: a block has more than 16 members");
  const double* Fb = &T.logF[(size_t)b * (K + 1)];
  for (int j = 0; j < len; ++j) s.lj[j] = Fb[r - j] == NEG_INF ? NEG_INF : pr[j] + Fb[r - j];   // core/cpp/v3_start.h:145-147
  cumulative_from_logs(s.lj, (size_t)len, s.row, s.e);
  return len;
}
void cond_row(const Tables& T, int b, int r, std::vector<double>& out) {
  CondScratch s;
  const int len = cond_row(T, b, r, s);
  out.assign(s.row, s.row + len);
}

}  // namespace v4::setup
