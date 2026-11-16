// tables.cpp -- block tables by depth-first enumeration with sorted-prefix reuse (bits of core/cpp/v3_start.h:76-98),
// threaded over blocks; table top stores; size profiles, convolutions, log Zbar0 and sampler tables (bits of
// core/cpp/v3_start.h:101-151), in flat arrays.
#include <omp.h>
#include <algorithm>
#include <atomic>
#include <chrono>
#include "v4/setup.h"
#include "bitscore_ref.h"

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
// bits of core/cpp/v3_score.h:212-217 on route chol.
struct PrefixScorer {
  const Data& D; detail::RefScorer ref; int B;
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
    detail::RefScore o = ref.score(U.data(), k);
    route = o.route;
    return o.logm;
  }
};

struct BlockOut { std::vector<double> logm; uint64_t scored = 0, prefix = 0, fallback = 0, routes[3] = {0, 0, 0}; };

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

// Top-c selection over all table models (global code index g = code_ptr[b] + code), strict order
// (value desc, [size asc,] lex asc) as core/cpp/v3_ledger.h:35-42. Table models are distinct (blocks are disjoint;
// the empty model is taken once, from block 0), so no duplicates arise.
template <class ValFn>
void select_store(const Data& D, const Partition& P, const Tables& T, Store& S, uint64_t cap, Order ord, ValFn val) {
  S.init(cap, ord);
  const int64_t NG = T.code_ptr.back();
  auto popc = [&](int64_t g, int& b, uint32_t& code) {
    b = (int)(std::upper_bound(T.code_ptr.begin(), T.code_ptr.end(), g) - T.code_ptr.begin()) - 1;
    code = (uint32_t)(g - T.code_ptr[b]);
  };
  auto valid = [&](int64_t g) {
    if (std::isnan(T.logr[g])) return false;
    int b; uint32_t code; popc(g, b, code);
    return !(code == 0 && b != 0);
  };
  std::vector<double> tmp; tmp.reserve(NG);
  for (int64_t g = 0; g < NG; ++g) if (valid(g)) tmp.push_back(val(g));
  double vstar = NEG_INF; bool all = tmp.size() <= cap;
  if (!all && cap > 0) {
    std::nth_element(tmp.begin(), tmp.begin() + (cap - 1), tmp.end(), std::greater<double>());
    vstar = tmp[cap - 1];
  }
  std::vector<double>().swap(tmp);
  if (cap == 0) return;
  std::vector<int64_t> sel;
  for (int64_t g = 0; g < NG; ++g) if (valid(g) && (all || val(g) >= vstar)) sel.push_back(g);
  auto members = [&](int64_t g, Model& M) {
    int b; uint32_t code; popc(g, b, code);
    M.clear(); for (int i = 0; i < P.size(b); ++i) if (code & (1u << i)) M.push_back(P.block(b)[i]);
  };
  Model Ma, Mb;
  std::sort(sel.begin(), sel.end(), [&](int64_t a, int64_t b) {
    double va = val(a), vb = val(b);
    if (va != vb) return va > vb;
    members(a, Ma); members(b, Mb);
    if (ord == Order::HPM && Ma.size() != Mb.size()) return Ma.size() < Mb.size();
    return lex_less(Ma, Mb);
  });
  if (sel.size() > cap) sel.resize(cap);
  Model M;
  for (int64_t g : sel) {
    members(g, M);
    S.v.push_back(val(g)); S.off.push_back(S.pool.size()); S.hash.push_back(D.zob.hash(view(M))); S.len.push_back((uint16_t)M.size());
    S.pool.insert(S.pool.end(), M.begin(), M.end());
  }
  S.nsorted = S.v.size();
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
  std::vector<double> logm(T.code_ptr.back(), 0.0);  // transient (dropped after the table top stores)
  const int TH = std::max(1, threads);
  std::vector<BlockOut> outs(TH);
  std::atomic<bool> failed{false}; std::string fail_msg;
#pragma omp parallel num_threads(TH)
  {
    PrefixScorer ps(D, 16);
    BlockOut& bo = outs[omp_get_thread_num()];
#pragma omp for schedule(dynamic, 64)
    for (int b = 0; b < P.J; ++b) {
      if (failed) continue;
      try {
        ps.U.clear();
        score_block(D, P.block(b), P.size(b), ps, &T.logr[T.code_ptr[b]], &logm[T.code_ptr[b]], bo);
      } catch (const Error& e) {
#pragma omp critical
        { if (!failed) { failed = true; fail_msg = e.what(); } }
      }
    }
  }
  if (failed) throw NumericalFailure(fail_msg);
  TableStats st;
  for (auto& o : outs) { st.scored += o.scored; st.prefix_scored += o.prefix; st.fallback_scored += o.fallback; for (int r = 0; r < 3; ++r) st.routes[r] += o.routes[r]; }
  st.seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  if (stores) {
    auto t1 = std::chrono::steady_clock::now();
    const uint64_t p = D.p;
    std::vector<uint8_t> k(T.code_ptr.back());
    for (int b = 0; b < P.J; ++b) for (uint32_t c = 0; c < (1u << P.size(b)); ++c) k[T.code_ptr[b] + c] = (uint8_t)__builtin_popcount(c);
    auto F = [&](int64_t g) { return D.logprior[k[g]] + logm[g]; };       // core/cpp/v3_core.cpp:381
    auto lg0 = [&](int64_t g) { return D.logprior[k[g]] + T.logr[g]; };  // core/cpp/v3_core.cpp:381
    select_store(D, P, T, stores->top, 40 * p + 1, Order::HPM, F);       // core/cpp/v3_ledger.h:78
    select_store(D, P, T, stores->lead0, 20 * p, Order::LEX, lg0);
    select_store(D, P, T, stores->lead1, 20 * p, Order::LEX, F);
    // table HPM = the first entry under the HPM order; provenance = its first table event (block, code) in the order
    // of core/cpp/v3_core.cpp:375-383 (the empty model: block 0, code 0)
    const Store& top = stores->top;
    if (top.size() > 0) {
      stores->hpmS.assign(top.pool.begin() + top.off[0], top.pool.begin() + top.off[0] + top.len[0]);
      stores->hpmF = top.v[0];
      if (stores->hpmS.empty()) { stores->hpm_block = 0; stores->hpm_code = 0; }
      else {
        int b = P.blk[stores->hpmS[0]]; uint32_t c = 0;
        for (int32_t j : stores->hpmS) c |= 1u << P.pos[j];
        stores->hpm_block = b; stores->hpm_code = c;
      }
    }
    st.seconds_stores = std::chrono::duration<double>(std::chrono::steady_clock::now() - t1).count();
  }
  if (stats) *stats = st;
  return T;
}

// ---------------------------------------------------------------- start law
namespace {
// core/cpp/v3_start.h:21-32
void cumulative_from_logs(const double* lp, size_t n, double* c) {
  double m = NEG_INF; for (size_t i = 0; i < n; ++i) m = std::max(m, lp[i]);
  for (size_t i = 0; i < n; ++i) c[i] = 0.0;
  if (m == NEG_INF) return;
  long double s = 0; std::vector<long double> e(n);
  for (size_t i = 0; i < n; ++i) { e[i] = (lp[i] == NEG_INF) ? 0.0L : pm::expl((long double)(lp[i] - m)); s += e[i]; }
  long double acc = 0; int last = -1;
  for (size_t i = 0; i < n; ++i) { acc += e[i]; c[i] = (double)(acc / s); if (e[i] > 0) last = (int)i; }
  for (size_t i = (size_t)last; i < n; ++i) c[i] = 1.0;
}
}  // namespace

// core/cpp/v3_start.h:101-151, in flat arrays (row layouts in v4/setup.h).
void build_start(const Data& D, const Partition& P, Tables& T) {
  const int K = D.K, J = P.J;
  T.K = K; T.J = J;
  T.logprof_ptr.assign(J + 1, 0);
  for (int b = 0; b < J; ++b) T.logprof_ptr[b + 1] = T.logprof_ptr[b] + std::min(P.size(b), K) + 1;
  const int64_t NR = T.logprof_ptr[J];
  T.logprof.assign(NR, NEG_INF);
  T.cbs_ptr.assign(NR + 1, 0);
  for (int b = 0; b < J; ++b) {
    int m = P.size(b), top = std::min(m, K);
    for (uint32_t code = 0; code < (1u << m); ++code) { int j = __builtin_popcount(code); if (j <= top) T.cbs_ptr[T.logprof_ptr[b] + j + 1]++; }
  }
  for (int64_t r = 0; r < NR; ++r) T.cbs_ptr[r + 1] += T.cbs_ptr[r];
  T.codes_by_size.assign(T.cbs_ptr[NR], 0);
  T.sub_cum.assign(T.cbs_ptr[NR], 0.0);
  {
    std::vector<int64_t> fill(T.cbs_ptr.begin(), T.cbs_ptr.end() - 1);
    for (int b = 0; b < J; ++b) {
      int m = P.size(b), top = std::min(m, K);
      for (uint32_t code = 0; code < (1u << m); ++code) {  // increasing code order within each size
        int j = __builtin_popcount(code);
        if (j <= top) T.codes_by_size[fill[T.logprof_ptr[b] + j]++] = code;
      }
    }
  }
  T.sub_ptr = T.cbs_ptr;
  std::vector<double> lv;
  for (int b = 0; b < J; ++b) {
    int top = std::min(P.size(b), K);
    const double* lr = &T.logr[T.code_ptr[b]];
    for (int j = 0; j <= top; ++j) {
      int64_t row = T.logprof_ptr[b] + j, o = T.cbs_ptr[row], e = T.cbs_ptr[row + 1];
      lv.clear(); for (int64_t q = o; q < e; ++q) lv.push_back(lr[T.codes_by_size[q]]);
      T.logprof[row] = log_sum_exp(lv);                         // core/cpp/v3_start.h:117
      cumulative_from_logs(lv.data(), lv.size(), &T.sub_cum[o]);  // core/cpp/v3_start.h:118
    }
  }
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
  // core/cpp/v3_start.h:140-150
  T.cond_ptr.assign((size_t)J * (K + 1) + 1, 0);
  for (int b = 0; b < J; ++b) {
    int npr = (int)(T.logprof_ptr[b + 1] - T.logprof_ptr[b]);
    for (int r = 0; r <= K; ++r) { size_t row = (size_t)b * (K + 1) + r; T.cond_ptr[row + 1] = T.cond_ptr[row] + std::min(npr - 1, r) + 1; }
  }
  T.cond_cum.assign(T.cond_ptr.back(), 0.0);
  std::vector<double> lj;
  for (int b = 0; b < J; ++b) {
    const double* pr = &T.logprof[T.logprof_ptr[b]];
    int npr = (int)(T.logprof_ptr[b + 1] - T.logprof_ptr[b]);
    const double* Fb = &T.logF[(size_t)b * (K + 1)];
    for (int r = 0; r <= K; ++r) {
      lj.clear();
      for (int j = 0; j < npr && j <= r; ++j) lj.push_back(Fb[r - j] == NEG_INF ? NEG_INF : pr[j] + Fb[r - j]);
      size_t row = (size_t)b * (K + 1) + r;
      cumulative_from_logs(lj.data(), lj.size(), &T.cond_cum[T.cond_ptr[row]]);
    }
  }
}

}  // namespace v4::setup
