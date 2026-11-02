// lowp_enum.cpp -- exact enumerator of all 2^p models (p <= 62) with the SMC core's scorer arithmetic (vendored
// v3_score.h / v3_util.h), plus the T37 truth-dominance audit. Design: LOWP_SPEC §L.7, INTERFACES §I2.
//
// The depth-first search appends one row to row-major lower Cholesky factors of H = (n+1)G_S + I and A = G_S + I per
// included variable, with exactly the operation order of v3::chol_inplace / forward_solve / finish_from_factors, so
// that F(S) = logprior[|S|] + log m(S) is bit-identical to v3::Scorer::score (verified empirically, VALIDATION.md).
// Models whose Q < 1e-8 y'y, whose log m is not finite, or whose pivot fails (and all descendants of a failed pivot)
// are rescored by v3::Scorer::score itself.
// [[Rcpp::plugins(openmp)]]
#include <Rcpp.h>
#include <omp.h>
#include <memory>
#include <atomic>
#include <cstring>
#include <cstdint>
#include "v3_score.h"

using namespace Rcpp;
using namespace v3;

// ---------------------------------------------------------------------------------------------
// Model order (HPM rule of master §I.6): larger F, then smaller size, then lexicographically smaller sorted
// index vector. On bitmasks (bit j = internal variable j) with equal size, the set that contains the smallest index at
// which the two sets differ is lexicographically smaller (equal sizes: neither is a prefix of the other).
// ---------------------------------------------------------------------------------------------
struct Ent { double F; uint64_t m; int k; };
static inline bool better_m(double F1, int k1, uint64_t m1, double F2, int k2, uint64_t m2) {
  if (F1 > F2) return true;
  if (F1 < F2) return false;
  if (k1 != k2) return k1 < k2;
  uint64_t d = m1 ^ m2;
  if (!d) return false;
  uint64_t low = d & (~d + 1);
  return (m1 & low) != 0;
}
static inline bool better_e(const Ent& a, const Ent& b) { return better_m(a.F, a.k, a.m, b.F, b.k, b.m); }

static std::vector<int> mask_to_vec(uint64_t m) {
  std::vector<int> v;
  while (m) { int j = __builtin_ctzll(m); v.push_back(j); m &= m - 1; }
  return v;
}

// ---------------------------------------------------------------------------------------------
// Accumulators (one per scale per task, and one global per scale)
// ---------------------------------------------------------------------------------------------
struct SAcc {
  double mx = NEG_INF;
  long double total = 0;
  std::vector<long double> numer, sizem, T;
  bool has = false;
  Ent hpm{NEG_INF, 0, 0};
  double hpm_eta = 0;
  double up1 = NEG_INF, up2 = NEG_INF;
  uint64_t upm1 = 0, upm2 = 0;
  std::vector<Ent> top;
  uint64_t n_rescale = 0, n_fb = 0, n_slow = 0, n_qre = 0, n_nonfin = 0, n_rechk = 0, n_mis = 0, n_mis_eta = 0;
  double max_dF = 0;
  void init(int p, int K) { numer.assign(p, 0.0L); sizem.assign(K + 1, 0.0L); T.assign(K + 2, 0.0L); }
};

struct Cfg {
  int n = 0, p = 0, K = 0, nS = 0, KS = 0;
  double n1 = 0;
  std::vector<const Data*> D;
  const double* G = nullptr;
  size_t top_cap = 1000;
  int recheck_stride = 0;
  double qthr = 1e-8;
  std::vector<char> fail_var;
  std::vector<double*> collect;
};

#ifdef LOWP_LONG_EXP
static inline long double wexp(double x) { return std::exp((long double)x); }
#else
static inline long double wexp(double x) { return (long double)std::exp(x); }
#endif

struct Worker {
  const Cfg& C;
  std::vector<double> LH, LA, ldH, ldA, mxH, mnH, mxA, mnA;
  std::vector<std::vector<double>> wv, quad;
  std::vector<int> S;
  std::vector<std::unique_ptr<Data>> loc;
  std::vector<std::unique_ptr<Scorer>> fb;
  std::vector<Scorer> eb;
  std::vector<SAcc>* acc = nullptr;
  uint64_t nodes = 0, count = 0;
  uint32_t last_fb = 0;
  std::vector<int> tmpS;

  explicit Worker(const Cfg& c) : C(c) {
    int KS = C.KS;
    LH.assign((size_t)KS * KS, 0.0); LA = LH;
    ldH.assign(KS + 1, 0.0); ldA = ldH; mxH = ldH; mnH = ldH; mxA = ldH; mnA = ldH;
    wv.assign(C.nS, std::vector<double>(KS, 0.0)); quad.assign(C.nS, std::vector<double>(KS + 1, 0.0));
    S.assign(KS, 0);
    loc.resize(C.nS); fb.resize(C.nS);
    for (int s = 0; s < C.nS; ++s) eb.emplace_back(C.D[s]);
    reset_root();
  }
  void reset_root() {
    ldH[0] = 0; ldA[0] = 0; mxH[0] = 0; mxA[0] = 0; mnH[0] = POS_INF; mnA[0] = POS_INF;
    for (int s = 0; s < C.nS; ++s) quad[s][0] = 0.0;
  }
  Scorer& fbs(int s) {
    if (!fb[s]) { loc[s].reset(new Data(*C.D[s])); fb[s].reset(new Scorer(loc[s].get())); }
    return *fb[s];
  }

  // Append variable j as row k of the row-major lower factors of H and A, with exactly the arithmetic and operation
  // order of v3::chol_inplace (row k, entries t < k, then the diagonal), v3::forward_solve and finish_from_factors.
  // Returns false on a failed pivot (or the test hook); the caller then rescoring the whole subtree with v3::Scorer.
  bool append_row(int k, int j) {
    if (!C.fail_var.empty() && C.fail_var[j]) return false;
    const int p = C.p, KS = C.KS;
    const double n1 = C.n1;
    const double* G = C.G;
    double* Hk = &LH[(size_t)k * KS];
    double* Ak = &LA[(size_t)k * KS];
    for (int t = 0; t < k; ++t) {
      double g = G[(size_t)j * p + S[t]];
      double sH = n1 * g + 0.0;
      double sA = g + 0.0;
      const double* Lt = &LH[(size_t)t * KS];
      const double* At = &LA[(size_t)t * KS];
      for (int u = 0; u < t; ++u) { sH -= Hk[u] * Lt[u]; sA -= Ak[u] * At[u]; }
      Hk[t] = sH / Lt[t];
      Ak[t] = sA / At[t];
    }
    double gjj = G[(size_t)j * p + j];
    double dH = n1 * gjj + 1.0, dA = gjj + 1.0;
    for (int t = 0; t < k; ++t) { dH -= Hk[t] * Hk[t]; dA -= Ak[t] * Ak[t]; }
    if (!(dH > 0) || !std::isfinite(dH) || !(dA > 0) || !std::isfinite(dA)) return false;
    double h = std::sqrt(dH), g = std::sqrt(dA);
    Hk[k] = h; Ak[k] = g;
    ldH[k + 1] = ldH[k] + std::log(h); ldA[k + 1] = ldA[k] + std::log(g);
    mxH[k + 1] = std::max(mxH[k], h); mnH[k + 1] = std::min(mnH[k], h);
    mxA[k + 1] = std::max(mxA[k], g); mnA[k + 1] = std::min(mnA[k], g);
    for (int s = 0; s < C.nS; ++s) {
      double sw = C.D[s]->z[j];
      const double* w = wv[s].data();
      for (int t = 0; t < k; ++t) sw -= Hk[t] * w[t];
      double wk = sw / Hk[k];
      wv[s][k] = wk;
      quad[s][k + 1] = quad[s][k] + wk * wk;
    }
    return true;
  }

  // F and eta of the current model (size k, sorted members S[0..k-1]) for every scale.
  void score_current(int k, bool slow, double* F, double* eta, bool check) {
    last_fb = 0;
    for (int s = 0; s < C.nS; ++s) {
      const Data& D = *C.D[s];
      SAcc* a = acc ? &(*acc)[s] : nullptr;
      ScoreOut o;
      if (k == 0) { o.logm = D.logm0; o.Q = D.yty; F[s] = D.logprior[0] + o.logm; eta[s] = eb[s].error_bound(o, 0); continue; }
      int why = slow ? 1 : 0;
      if (!slow) {
        double ldH2 = ldH[k] * 2, ldA2 = ldA[k] * 2;
        double Q = D.yty - D.n * quad[s][k];
        if (Q < C.qthr * D.yty) why = 2;
        else {
          double arg = 2 * D.b0 + Q;
          double logm = (arg > 0) ? D.logCn - 0.5 * (ldH2 - ldA2) - D.nu * std::log(arg) : NEG_INF;
          if (!std::isfinite(logm)) why = 3;
          else {
            o.logm = logm; o.Q = Q;
            o.cond_H = (mxH[k] / mnH[k]) * (mxH[k] / mnH[k]);
            o.cond_A = (mxA[k] / mnA[k]) * (mxA[k] / mnA[k]);
          }
        }
      }
      if (why) {
        tmpS.assign(S.begin(), S.begin() + k);
        o = fbs(s).score(tmpS);
        last_fb |= (1u << s);
        if (a) { a->n_fb++; if (why == 1) a->n_slow++; else if (why == 2) a->n_qre++; else a->n_nonfin++; }
      }
      F[s] = D.logprior[k] + o.logm;
      eta[s] = eb[s].error_bound(o, k);
      if (!why && check && a) {
        tmpS.assign(S.begin(), S.begin() + k);
        ScoreOut o2 = fbs(s).score(tmpS);
        double F2 = D.logprior[k] + o2.logm, e2 = eb[s].error_bound(o2, k);
        a->n_rechk++;
        if (std::memcmp(&F[s], &F2, sizeof(double)) != 0) { a->n_mis++; a->max_dF = std::max(a->max_dF, std::fabs(F[s] - F2)); }
        if (std::memcmp(&eta[s], &e2, sizeof(double)) != 0) a->n_mis_eta++;
      }
    }
  }

  inline void accum(SAcc& a, int k, double F, double eta, uint64_t mask) {
    if (F > a.mx) {
      long double sc = (a.mx == NEG_INF) ? 0.0L : std::exp((long double)(a.mx - F));
      a.total *= sc;
      for (auto& v : a.numer) v *= sc;
      for (auto& v : a.sizem) v *= sc;
      for (auto& v : a.T) v *= sc;
      a.mx = F; a.n_rescale++;
    }
    long double w = wexp(F - a.mx);
    a.total += w; a.sizem[k] += w; a.T[k] += w;
    if (!a.has || better_m(F, k, mask, a.hpm.F, a.hpm.k, a.hpm.m)) { a.has = true; a.hpm = Ent{F, mask, k}; a.hpm_eta = eta; }
    // bounded top store (heap, worst at the front)
    if (a.top.size() < C.top_cap) { a.top.push_back(Ent{F, mask, k}); std::push_heap(a.top.begin(), a.top.end(), better_e); }
    else if (F >= a.top.front().F) {
      Ent e{F, mask, k};
      if (better_e(e, a.top.front())) { std::pop_heap(a.top.begin(), a.top.end(), better_e); a.top.back() = e; std::push_heap(a.top.begin(), a.top.end(), better_e); }
    }
    double up = F + eta;
    if (up > a.up1) { a.up2 = a.up1; a.upm2 = a.upm1; a.up1 = up; a.upm1 = mask; }
    else if (up > a.up2) { a.up2 = up; a.upm2 = mask; }
  }

  void node(int k, int start, bool slow, uint64_t mask, int kr) {
    ++nodes; ++count;
    double F[8], eta[8];
    bool check = C.recheck_stride > 0 && (nodes % (uint64_t)C.recheck_stride == 0);
    score_current(k, slow, F, eta, check);
    for (int s = 0; s < C.nS; ++s) {
      accum((*acc)[s], k, F[s], eta[s], mask);
      if (!C.collect.empty()) C.collect[s][mask] = F[s];
    }
    if (k < C.K) {
      for (int j = start; j < C.p; ++j) {
        S[k] = j;
        bool cs = slow;
        if (!slow) cs = !append_row(k, j);
        node(k + 1, j + 1, cs, mask | (1ULL << j), kr);
      }
    }
    if (k > kr) {
      int last = S[k - 1];
      for (int s = 0; s < C.nS; ++s) {
        SAcc& a = (*acc)[s];
        a.numer[last] += a.T[k]; a.T[k - 1] += a.T[k]; a.T[k] = 0.0L;
      }
    }
  }

  // Run one task: models whose intersection with {0..m-1} is the pattern `pat`. Returns false if |pat| > K.
  bool run_task(uint64_t pat, int m, std::vector<SAcc>& out) {
    int kr = __builtin_popcountll(pat);
    if (kr > C.K) return false;
    acc = &out; nodes = 0; count = 0;
    reset_root();
    bool slow = false; int k = 0; uint64_t mask = 0;
    for (int j = 0; j < m; ++j) if ((pat >> j) & 1ULL) {
      S[k] = j;
      if (!slow) slow = !append_row(k, j);
      ++k; mask |= (1ULL << j);
    }
    node(kr, m, slow, mask, kr);
    for (int s = 0; s < C.nS; ++s) {
      SAcc& a = out[s];
      for (int j = 0; j < kr; ++j) a.numer[S[j]] += a.T[kr];
    }
    return true;
  }
};

static void merge_into(SAcc& g, SAcc& t, size_t cap) {
  g.n_rescale += t.n_rescale; g.n_fb += t.n_fb; g.n_slow += t.n_slow; g.n_qre += t.n_qre; g.n_nonfin += t.n_nonfin;
  g.n_rechk += t.n_rechk; g.n_mis += t.n_mis; g.n_mis_eta += t.n_mis_eta; g.max_dF = std::max(g.max_dF, t.max_dF);
  if (!t.has) return;
  if (g.mx == NEG_INF) {
    g.mx = t.mx; g.total = t.total; g.numer = t.numer; g.sizem = t.sizem;
  } else {
    double nm = std::max(g.mx, t.mx);
    long double sg = (g.mx < nm) ? std::exp((long double)(g.mx - nm)) : 1.0L;
    long double st = (t.mx < nm) ? std::exp((long double)(t.mx - nm)) : 1.0L;
    g.total = g.total * sg + t.total * st;
    for (size_t i = 0; i < g.numer.size(); ++i) g.numer[i] = g.numer[i] * sg + t.numer[i] * st;
    for (size_t i = 0; i < g.sizem.size(); ++i) g.sizem[i] = g.sizem[i] * sg + t.sizem[i] * st;
    g.mx = nm;
  }
  if (!g.has || better_e(t.hpm, g.hpm)) { g.hpm = t.hpm; g.hpm_eta = t.hpm_eta; }
  g.has = true;
  auto ins = [&](double up, uint64_t m) {
    if (!(up > NEG_INF)) return;
    if (up > g.up1) { g.up2 = g.up1; g.upm2 = g.upm1; g.up1 = up; g.upm1 = m; }
    else if (up > g.up2) { g.up2 = up; g.upm2 = m; }
  };
  ins(t.up1, t.upm1); ins(t.up2, t.upm2);
  g.top.insert(g.top.end(), t.top.begin(), t.top.end());
  std::sort(g.top.begin(), g.top.end(), better_e);
  if (g.top.size() > cap) g.top.resize(cap);
}

// Shared Data construction: one per response, with the bitwise-identical-Gram check.
static void build_data(NumericMatrix X, NumericMatrix Y, IntegerVector orig, std::vector<std::unique_ptr<Data>>& Ds) {
  int n = X.nrow(), p = X.ncol();
  if (Y.nrow() != n) stop("Y has %d rows, X has %d", Y.nrow(), n);
  std::vector<int> o(orig.begin(), orig.end());
  if ((int)o.size() != p) stop("orig has wrong length");
  for (int s = 0; s < Y.ncol(); ++s) {
    Ds.emplace_back(new Data());
    NumericVector ys = Y(_, s);
    data_init(*Ds.back(), X.begin(), ys.begin(), n, p, o);
    if (s > 0 && std::memcmp(Ds[0]->G.data(), Ds.back()->G.data(), sizeof(double) * (size_t)p * p) != 0) stop("Gram matrices of the scales differ bitwise");
  }
}

// [[Rcpp::export]]
List cpp_enum(NumericMatrix X, NumericMatrix Y, IntegerVector orig, int top, int threads, int task_bits,
              IntegerVector task_subset, int recheck_stride, double qthr, IntegerVector fail_vars, bool collect_F) {
  int n = X.nrow(), p = X.ncol();
  if (p > 62) stop("lowp_enum: p must be <= 62");
  if (Y.ncol() < 1 || Y.ncol() > 8) stop("1..8 scales supported");
  std::vector<std::unique_ptr<Data>> Ds;
  build_data(X, Y, orig, Ds);
  Cfg C;
  C.n = n; C.p = p; C.K = Ds[0]->K; C.nS = Y.ncol(); C.KS = C.K + 1; C.n1 = n + 1.0; C.G = Ds[0]->G.data();
  for (auto& d : Ds) C.D.push_back(d.get());
  C.top_cap = (size_t)std::max(top, 2); C.recheck_stride = recheck_stride; C.qthr = qthr;
  if (fail_vars.size()) { C.fail_var.assign(p, 0); for (int v : fail_vars) { if (v < 0 || v >= p) stop("fail_vars out of range"); C.fail_var[v] = 1; } }
  std::vector<std::vector<double>> store;
  if (collect_F) {
    if (p > 26) stop("collect_F requires p <= 26");
    store.assign(C.nS, std::vector<double>((size_t)1 << p, NA_REAL));
    for (auto& v : store) C.collect.push_back(v.data());
  }
  if (task_bits < 0 || task_bits > 20) stop("task_bits must be in 0..20");
  if (threads < 1 || threads > 1024) stop("threads must be in 1..1024");
  if (top < 2 || top > 100000) stop("top must be in 2..100000");
  int m = std::min(task_bits, p);
  uint64_t ntask = 1ULL << m;
  std::vector<uint64_t> tasks;
  if (task_subset.size()) { for (int t : task_subset) { if (t < 0 || (uint64_t)t >= ntask) stop("task index out of range"); tasks.push_back((uint64_t)t); }
    std::sort(tasks.begin(), tasks.end()); tasks.erase(std::unique(tasks.begin(), tasks.end()), tasks.end()); }
  else for (uint64_t t = 0; t < ntask; ++t) tasks.push_back(t);
  size_t nt = tasks.size();

  std::vector<SAcc> G(C.nS);
  for (auto& g : G) g.init(p, C.K);
  std::vector<std::vector<SAcc>> res(nt);
  std::vector<char> done(nt, 0);
  std::vector<double> ttime(nt, 0.0);
  std::vector<double> tcount(nt, 0.0);
  size_t next = 0;
  double total_count = 0;
  std::atomic<bool> failed(false);
  std::string errmsg;
  double t0 = omp_get_wtime();
  int nth = std::max(1, threads);
#pragma omp parallel num_threads(nth)
  {
    Worker W(C);
#pragma omp for schedule(dynamic, 1)
    for (long ti = 0; ti < (long)nt; ++ti) {
      if (failed.load()) continue;
      std::vector<SAcc> out(C.nS);
      for (auto& a : out) a.init(p, C.K);
      double ts = omp_get_wtime();
      bool ok = true; bool ran = false;
      try { ran = W.run_task(tasks[ti], m, out); }
      catch (std::exception& e) {
        ok = false;
#pragma omp critical(lowp_err)
        { errmsg = e.what(); failed.store(true); }
      }
      double te = omp_get_wtime();
#pragma omp critical(lowp_merge)
      {
        ttime[ti] = te - ts; tcount[ti] = ran ? (double)W.count : 0.0;
        if (ok) { res[ti] = std::move(out); }
        done[ti] = 1;
        while (next < nt && done[next]) {
          if (!res[next].empty()) {
            for (int s = 0; s < C.nS; ++s) merge_into(G[s], res[next][s], C.top_cap);
            total_count += tcount[next];
            std::vector<SAcc>().swap(res[next]);
          }
          ++next;
        }
      }
    }
  }
  double wall = omp_get_wtime() - t0;

  // coverage: every feasible model (|S| <= K) scored exactly once
  unsigned __int128 expect = 0, cc = 1;
  for (int k = 0; k <= C.K; ++k) { if (k > 0) cc = cc * (unsigned __int128)(p - k + 1) / (unsigned __int128)k; expect += cc; }
  double models_expected = (double)expect;
  bool complete = (!failed.load()) && (nt == ntask) && (total_count == models_expected);
  List scales(C.nS);
  for (int s = 0; s < C.nS; ++s) {
    SAcc& g = G[s]; const Data& D = *C.D[s];
    double logZ = g.mx + (double)std::log(g.total);
    NumericVector pip(p);
    for (int j = 0; j < p; ++j) pip[j] = (double)(g.numer[j] / g.total);
    NumericVector szm(C.K + 1);
    NumericVector szj(C.K + 1);   // joint log mass log sum_{|S|=k} exp F(S) and posterior log mass (joint - log Z)
    for (int k = 0; k <= C.K; ++k) { szj[k] = (g.sizem[k] > 0) ? g.mx + (double)std::log(g.sizem[k]) : NEG_INF; szm[k] = std::isfinite(szj[k]) ? szj[k] - logZ : NEG_INF; }
    size_t nt2 = g.top.size();
    NumericVector tF(nt2), tmask(nt2); IntegerVector tk(nt2); CharacterVector ttxt(nt2);
    for (size_t i = 0; i < nt2; ++i) {
      tF[i] = g.top[i].F; tk[i] = g.top[i].k;
      std::vector<int> v = mask_to_vec(g.top[i].m);
      double mk = 0; std::string txt;
      for (size_t q = 0; q < v.size(); ++q) { int o = D.orig[v[q]]; mk += std::ldexp(1.0, o - 1); if (q) txt += ";"; txt += std::to_string(o); }
      tmask[i] = mk; ttxt[i] = txt;
    }
    IntegerVector hv(g.hpm.k); { std::vector<int> v = mask_to_vec(g.hpm.m); for (size_t q = 0; q < v.size(); ++q) hv[q] = D.orig[v[q]]; }
    double second_F = NA_REAL;
    if (nt2 >= 2) second_F = g.top[1].F;
    double runner_up = (g.upm1 == g.hpm.m) ? g.up2 : g.up1;
    bool over_scored = (!failed.load()) && (g.hpm.F - g.hpm_eta > runner_up);
    bool certified = complete && over_scored;   // a global certificate needs every feasible model scored
    scales[s] = List::create(_["log_Z"] = logZ, _["log_m0"] = D.logm0, _["pip"] = pip, _["hpm"] = hv, _["hpm_F"] = g.hpm.F,
      _["hpm_size"] = g.hpm.k, _["hpm_eta"] = g.hpm_eta, _["second_F"] = second_F, _["margin"] = g.hpm.F - second_F,
      _["certificate_bound"] = g.hpm.F - runner_up, _["global_certified"] = certified, _["certified_over_scored_models"] = over_scored,
      _["scope"] = complete ? "full" : "restricted_to_scored_models", _["size_logmass"] = szm, _["size_logjoint"] = szj,
      _["top_F"] = tF, _["top_size"] = tk, _["top_model"] = ttxt, _["top_mask"] = tmask,
      _["numerics"] = List::create(_["n_rescale"] = (double)g.n_rescale, _["n_fallback_v3"] = (double)g.n_fb,
        _["n_fallback_slow_subtree"] = (double)g.n_slow, _["q_recomputed"] = (double)g.n_qre, _["n_fallback_nonfinite"] = (double)g.n_nonfin,
        _["recheck_count"] = (double)g.n_rechk, _["recheck_mismatch_F"] = (double)g.n_mis, _["recheck_mismatch_eta"] = (double)g.n_mis_eta,
        _["max_abs_dF_recheck"] = g.max_dF));
  }
  List out = List::create(_["scales"] = scales, _["models_scored"] = total_count, _["wall_s"] = wall, _["threads"] = nth,
    _["task_bits"] = m, _["n_tasks"] = (double)ntask, _["tasks_run"] = (double)nt, _["K"] = C.K, _["p"] = p, _["n"] = n,
    _["status"] = failed.load() ? "numerical_failure" : (complete ? "exact" : "partial"), _["complete"] = complete,
    _["models_expected"] = models_expected, _["message"] = errmsg);
  { IntegerVector tsel(nt); for (size_t i = 0; i < nt; ++i) tsel[i] = (int)tasks[i]; out["tasks"] = tsel; }
  out["task_seconds"] = NumericVector(ttime.begin(), ttime.end());
  out["task_models"] = NumericVector(tcount.begin(), tcount.end());
  if (collect_F) { List fl(C.nS); for (int s = 0; s < C.nS; ++s) fl[s] = NumericVector(store[s].begin(), store[s].end()); out["F_all"] = fl; }
  return out;
}

// Test hook: DFS-arithmetic F (row-append from the empty model, same append_row/score_current code as the enumerator)
// for requested internal bitmasks. Returns F, eta and a fallback flag per scale.
// [[Rcpp::export]]
List cpp_dfs_F(NumericMatrix X, NumericMatrix Y, IntegerVector orig, NumericVector masks, double qthr, IntegerVector fail_vars) {
  int n = X.nrow(), p = X.ncol();
  std::vector<std::unique_ptr<Data>> Ds; build_data(X, Y, orig, Ds);
  Cfg C; C.n = n; C.p = p; C.K = Ds[0]->K; C.nS = Y.ncol(); C.KS = C.K + 1; C.n1 = n + 1.0; C.G = Ds[0]->G.data(); C.qthr = qthr;
  for (auto& d : Ds) C.D.push_back(d.get());
  if (fail_vars.size()) { C.fail_var.assign(p, 0); for (int v : fail_vars) C.fail_var[v] = 1; }
  Worker W(C);
  R_xlen_t nm = masks.size();
  NumericMatrix F(nm, C.nS), E(nm, C.nS); IntegerMatrix FB(nm, C.nS);
  for (R_xlen_t i = 0; i < nm; ++i) {
    uint64_t mk = (uint64_t)masks[i];
    int k = __builtin_popcountll(mk);
    if (k > C.K) { for (int s = 0; s < C.nS; ++s) { F(i, s) = NA_REAL; E(i, s) = NA_REAL; FB(i, s) = NA_INTEGER; } continue; }
    W.reset_root(); bool slow = false; int q = 0;
    for (int j = 0; j < p; ++j) if ((mk >> j) & 1ULL) { W.S[q] = j; if (!slow) slow = !W.append_row(q, j); ++q; }
    double f[8], e[8];
    W.score_current(k, slow, f, e, false);
    for (int s = 0; s < C.nS; ++s) { F(i, s) = f[s]; E(i, s) = e[s]; FB(i, s) = (W.last_fb >> s) & 1u; }
  }
  return List::create(_["F"] = F, _["eta"] = E, _["fallback"] = FB);
}

// Test hook: v3::Scorer::score on internal bitmasks (optionally parallel, per-thread Data copies).
// [[Rcpp::export]]
List cpp_score_masks(NumericMatrix X, NumericVector y, IntegerVector orig, NumericVector masks, int threads) {
  int n = X.nrow(), p = X.ncol();
  std::vector<int> o(orig.begin(), orig.end());
  Data D0; data_init(D0, X.begin(), y.begin(), n, p, o);
  R_xlen_t nm = masks.size();
  NumericVector F(nm), LM(nm), E(nm); IntegerVector RT(nm);
  std::atomic<bool> bad(false);
#pragma omp parallel num_threads(std::max(1, threads))
  {
    Data D(D0); Scorer sc(&D);
#pragma omp for schedule(static)
    for (long i = 0; i < (long)nm; ++i) {
      uint64_t mk = (uint64_t)masks[i];
      std::vector<int> S = mask_to_vec(mk);
      if ((int)S.size() > D.K) { F[i] = NA_REAL; LM[i] = NA_REAL; E[i] = NA_REAL; RT[i] = NA_INTEGER; continue; }
      try { ScoreOut so = sc.score(S); F[i] = D.logprior[S.size()] + so.logm; LM[i] = so.logm; E[i] = sc.error_bound(so, (int)S.size()); RT[i] = so.route; }
      catch (std::exception&) { bad.store(true); }
    }
  }
  if (bad.load()) stop("numerical_failure in cpp_score_masks");
  return List::create(_["F"] = F, _["log_m"] = LM, _["eta"] = E, _["route"] = RT);
}

// Scorer::score for lists of models given as sorted-or-not original indices.
// [[Rcpp::export]]
List cpp_score_models(NumericMatrix X, NumericVector y, IntegerVector orig, List models, int threads) {
  int n = X.nrow(), p = X.ncol();
  std::vector<int> o(orig.begin(), orig.end());
  Data D0; data_init(D0, X.begin(), y.begin(), n, p, o);
  R_xlen_t nm = models.size();
  std::vector<std::vector<int>> Ms(nm);
  for (R_xlen_t i = 0; i < nm; ++i) {
    IntegerVector S = models[i];
    std::vector<int> out;
    for (int v : S) {
      auto it = std::lower_bound(D0.orig.begin(), D0.orig.end(), v);
      if (it == D0.orig.end() || *it != v) stop("index %d is not a retained original column index", v);
      out.push_back((int)(it - D0.orig.begin()));
    }
    std::sort(out.begin(), out.end());
    if (std::adjacent_find(out.begin(), out.end()) != out.end()) stop("model has duplicated indices");
    if ((int)out.size() > D0.K) stop("model %d has size %d > K = %d", (int)i + 1, (int)out.size(), D0.K);
    Ms[i] = out;
  }
  NumericVector F(nm), LM(nm), E(nm); IntegerVector SZ(nm), RT(nm); LogicalVector QR(nm);
  std::atomic<bool> bad(false);
#pragma omp parallel num_threads(std::max(1, threads))
  {
    Data D(D0); Scorer sc(&D);
#pragma omp for schedule(static)
    for (long i = 0; i < (long)nm; ++i) {
      try { ScoreOut so = sc.score(Ms[i]); int k = (int)Ms[i].size(); F[i] = D.logprior[k] + so.logm; LM[i] = so.logm; E[i] = sc.error_bound(so, k); SZ[i] = k; RT[i] = so.route; QR[i] = so.q_recomputed; }
      catch (std::exception&) { bad.store(true); }
    }
  }
  if (bad.load()) stop("numerical_failure in cpp_score_models");
  return List::create(_["size"] = SZ, _["F"] = F, _["log_m"] = LM, _["eta"] = E, _["route"] = RT, _["q_recomputed"] = QR);
}

// Consistency test of the bitmask order against v3::hpm_better.
// [[Rcpp::export]]
double cpp_order_check(int trials, int p, int seed) {
  Xoshiro256ss r; r.seed_stream((uint64_t)seed, 7);
  double bad = 0;
  for (int t = 0; t < trials; ++t) {
    uint64_t a = r.next() & ((1ULL << p) - 1), b = r.next() & ((1ULL << p) - 1);
    if (t % 3 == 0) b = a ^ (1ULL << (r.next() % p));              // nearby sets, sizes differ by one
    if (t % 3 == 1) { a &= r.next(); b = a ^ (1ULL << (r.next() % p)); }
    double Fa = (t % 2) ? 1.0 : 0.0, Fb = (t % 4 < 2) ? 1.0 : 0.0;
    std::vector<int> A = mask_to_vec(a), B = mask_to_vec(b);
    bool x = better_m(Fa, (int)A.size(), a, Fb, (int)B.size(), b);
    bool y = hpm_better(Fa, A, Fb, B);
    if (x != y) bad += 1;
  }
  return bad;
}

// ---------------------------------------------------------------------------------------------
// T37 truth-dominance audit (see lowp_td in lowp_enum.R for the definition).
// Two margin variants per centre: `literal` (T37 wording) and `toward` (moves that strictly reduce |S Delta S0|).
// Feasible moves: additions (only if |S| < K), deletions, swaps (swaps keep the size, so they are feasible at |S| = K).
// ---------------------------------------------------------------------------------------------
struct TdMove { int type = -1, a = -1, b = -1; };   // 0 add a, 1 delete a, 2 swap (a out, b in)
static std::string move_txt(const TdMove& m, const std::vector<int>& orig) {
  if (m.type < 0) return "none";
  if (m.type == 0) return "add " + std::to_string(orig[m.a]);
  if (m.type == 1) return "del " + std::to_string(orig[m.a]);
  return "swap " + std::to_string(orig[m.a]) + "->" + std::to_string(orig[m.b]);
}
// Move label by the truth status of the variables involved (tr = in S0).
static const char* move_label(const TdMove& m, const std::vector<char>& tr) {
  if (m.type < 0) return "none";
  if (m.type == 0) return tr[m.a] ? "truth_addition" : "null_addition";
  if (m.type == 1) return tr[m.a] ? "truth_deletion" : "null_deletion";
  bool out_t = tr[m.a], in_t = tr[m.b];
  if (in_t && !out_t) return "swap_null_out_truth_in";
  if (in_t && out_t) return "swap_truth_for_truth";
  if (!in_t && !out_t) return "swap_null_for_null";
  return "swap_truth_out_null_in";
}
struct TdVar { double margin = 0, gstar = 0, ostar = 0; std::string gmove, omove, olabel; };
struct TdRow { long long id; int clause; int size; std::string centre; TdVar lit, tow; };
struct TdAcc {
  long long nc[3] = {0, 0, 0};
  long long nviol[2][3] = {{0, 0, 0}, {0, 0, 0}}, nviol_s[2][3] = {{0, 0, 0}, {0, 0, 0}};
  double minm[2][3] = {{POS_INF, POS_INF, POS_INF}, {POS_INF, POS_INF, POS_INF}}; long long minid[2][3] = {{-1, -1, -1}, {-1, -1, -1}};
  std::vector<TdRow> viol[2], all;
  long long scores = 0, skipped = 0;
};

// [[Rcpp::export]]
List cpp_td(NumericMatrix X, NumericVector y, IntegerVector orig, IntegerVector S0, IntegerVector pool, int d,
            double margin, int threads, bool keep_all) {
  int n = X.nrow(), p = X.ncol();
  std::vector<int> o(orig.begin(), orig.end());
  Data D0; data_init(D0, X.begin(), y.begin(), n, p, o);
  auto to_int = [&](int v) { auto it = std::lower_bound(D0.orig.begin(), D0.orig.end(), v); if (it == D0.orig.end() || *it != v) stop("index %d is not a retained original column index", v); return (int)(it - D0.orig.begin()); };
  std::vector<int> s0; for (int v : S0) s0.push_back(to_int(v)); std::sort(s0.begin(), s0.end());
  std::vector<int> pl; for (int v : pool) pl.push_back(to_int(v)); std::sort(pl.begin(), pl.end());
  std::vector<char> tr(p, 0); for (int j : s0) tr[j] = 1;
  for (int j : pl) if (tr[j]) stop("null_pool intersects the truth");
  if (d < 0 || d > 1000) stop("d must be in 0..1000");
  if (!R_finite(margin) || margin < 0) stop("margin must be finite and >= 0");
  if (threads < 1 || threads > 1024) stop("threads must be in 1..1024");
  if (std::adjacent_find(s0.begin(), s0.end()) != s0.end()) stop("duplicate indices in truth");
  if (std::adjacent_find(pl.begin(), pl.end()) != pl.end()) stop("duplicate indices in null_pool");
  if (s0.empty()) stop("truth is empty");
  {  // guard the number of centres before any allocation: sum_{i<=d} choose(npool, i) * 2^s0 (double arithmetic, exact far beyond the cap)
    double nPd = 0, c = 1, npl = (double)pl.size();
    for (int i = 0; i <= std::min<double>(d, npl); ++i) { if (i > 0) c = c * (npl - i + 1) / i; nPd += c; }
    if (nPd > 5e7) stop("too many pool subsets (%g) for the audit", nPd);
    if (nPd * std::ldexp(1.0, (int)s0.size()) > 4e15) stop("number of centres exceeds 4e15");
  }
  int s0n = (int)s0.size();
  if (s0n > 40) stop("s0 too large");
  long long nU = 1LL << s0n;
  std::vector<std::vector<int>> Ps(1);
  { std::vector<int> cur; std::function<void(int)> rec = [&](int st) {
      if ((int)cur.size() == d) return;
      for (int i = st; i < (int)pl.size(); ++i) { cur.push_back(pl[i]); Ps.push_back(cur); rec(i + 1); cur.pop_back(); } };
    rec(0); }
  long long nP = (long long)Ps.size();
  long long ncent = nU * nP;
  int K = D0.K;
  std::vector<TdAcc> accs(std::max(1, threads));
  std::atomic<bool> bad(false);
#pragma omp parallel num_threads(std::max(1, threads))
  {
    Data D(D0); Scorer sc(&D);
    TdAcc& A = accs[omp_get_thread_num()];
    std::vector<char> inS(p, 0);
    std::vector<int> S, T;
#pragma omp for schedule(dynamic, 8)
    for (long long c = 0; c < ncent; ++c) {
      if (bad.load()) continue;
      long long um = c % nU; const std::vector<int>& P = Ps[c / nU];
      S.clear();
      for (int i = 0; i < s0n; ++i) if ((um >> i) & 1LL) S.push_back(s0[i]);
      for (int j : P) S.push_back(j);
      std::sort(S.begin(), S.end());
      int k = (int)S.size();
      if (k > K) { A.skipped++; continue; }
      try {
        for (int j : S) inS[j] = 1;
        int nmiss = 0, nextra = 0;
        for (int j : s0) if (!inS[j]) ++nmiss;
        for (int j : S) if (!tr[j]) ++nextra;
        int clause = nmiss > 0 ? 0 : (nextra > 0 ? 1 : 2);
        ScoreOut so = sc.score(S); A.scores++;
        double F0 = D.logprior[k] + so.logm;
        // literal: target moves (clause a: truth additions; clause b: null deletions); g1 best target, g2 second best target
        double g1 = NEG_INF, g2 = NEG_INF, onon = NEG_INF; TdMove m1, onm;
        // toward: best move that strictly reduces |S delta S0| (r1) and best that does not (q1)
        double r1 = NEG_INF, q1 = NEG_INF; TdMove rm, qm;
        auto consider = [&](double gain, const TdMove& mv) {
          bool target = false, reduce = false;
          if (mv.type == 0) { target = (clause == 0 && tr[mv.a]); reduce = tr[mv.a]; }
          else if (mv.type == 1) { target = (clause == 1 && !tr[mv.a]); reduce = !tr[mv.a]; }
          else { reduce = (!tr[mv.a] && tr[mv.b]); }
          if (target) { if (gain > g1) { g2 = g1; g1 = gain; m1 = mv; } else if (gain > g2) { g2 = gain; } }
          else if (gain > onon) { onon = gain; onm = mv; }
          if (reduce) { if (gain > r1) { r1 = gain; rm = mv; } }
          else if (gain > q1) { q1 = gain; qm = mv; }
        };
        auto eval = [&](const std::vector<int>& Tm) { ScoreOut s2 = sc.score(Tm); A.scores++; return D.logprior[Tm.size()] + s2.logm - F0; };
        if (k < K) {
          for (int l = 0; l < p; ++l) if (!inS[l]) {
            T = S; T.insert(std::lower_bound(T.begin(), T.end(), l), l);
            TdMove mv; mv.type = 0; mv.a = l;
            consider(eval(T), mv);
          }
        }
        for (int ii = 0; ii < k; ++ii) {
          int j = S[ii];
          T = S; T.erase(T.begin() + ii);
          TdMove mv; mv.type = 1; mv.a = j;
          consider(eval(T), mv);
        }
        for (int ii = 0; ii < k; ++ii) {          // swaps are feasible at |S| = K (size unchanged)
          int j = S[ii];
          std::vector<int> base = S; base.erase(base.begin() + ii);
          for (int l = 0; l < p; ++l) if (!inS[l]) {
            T = base; T.insert(std::lower_bound(T.begin(), T.end(), l), l);
            TdMove mv; mv.type = 2; mv.a = j; mv.b = l;
            consider(eval(T), mv);
          }
        }
        TdVar V[2];
        {   // literal
          TdVar& v = V[0];
          if (clause == 2) {
            v.gstar = NEG_INF; v.ostar = onon; v.margin = (onon == NEG_INF) ? POS_INF : -onon;
            v.gmove = "none"; v.omove = move_txt(onm, D.orig); v.olabel = move_label(onm, tr);
          } else {
            v.gstar = g1; v.ostar = std::max(onon, g2);
            v.margin = (g1 == NEG_INF) ? NEG_INF : ((v.ostar == NEG_INF) ? POS_INF : g1 - v.ostar);
            v.gmove = move_txt(m1, D.orig);
            if (g2 > onon) { v.omove = "(other target)"; v.olabel = "other_target"; }
            else { v.omove = move_txt(onm, D.orig); v.olabel = move_label(onm, tr); }
          }
        }
        {   // toward
          TdVar& v = V[1];
          if (clause == 2) { v = V[0]; }
          else {
            v.gstar = r1; v.ostar = q1;
            v.margin = (r1 == NEG_INF) ? NEG_INF : ((q1 == NEG_INF) ? POS_INF : r1 - q1);
            v.gmove = move_txt(rm, D.orig); v.omove = move_txt(qm, D.orig); v.olabel = move_label(qm, tr);
          }
        }
        A.nc[clause]++;
        std::string txt; bool txt_done = false;
        auto centre_text = [&]() { if (!txt_done) { for (size_t q = 0; q < S.size(); ++q) { if (q) txt += ";"; txt += std::to_string(D.orig[S[q]]); } txt_done = true; } return txt; };
        for (int w = 0; w < 2; ++w) {
          double mg = V[w].margin;
          if (mg < A.minm[w][clause] || (mg == A.minm[w][clause] && (A.minid[w][clause] < 0 || c < A.minid[w][clause]))) { A.minm[w][clause] = mg; A.minid[w][clause] = c; }
          if (mg < margin) A.nviol[w][clause]++;
          if (mg <= margin) { A.nviol_s[w][clause]++; A.viol[w].push_back(TdRow{c, clause, k, centre_text(), V[0], V[1]}); }
        }
        if (keep_all) A.all.push_back(TdRow{c, clause, k, centre_text(), V[0], V[1]});
        for (int j : S) inS[j] = 0;
      } catch (std::exception&) { bad.store(true); for (int j : S) inS[j] = 0; }
    }
  }
  if (bad.load()) stop("numerical_failure in cpp_td");
  TdAcc M;
  for (auto& A : accs) {
    for (int c = 0; c < 3; ++c) M.nc[c] += A.nc[c];
    for (int w = 0; w < 2; ++w) {
      for (int c = 0; c < 3; ++c) {
        M.nviol[w][c] += A.nviol[w][c]; M.nviol_s[w][c] += A.nviol_s[w][c];
        if (A.minm[w][c] < M.minm[w][c] || (A.minm[w][c] == M.minm[w][c] && A.minid[w][c] >= 0 && (M.minid[w][c] < 0 || A.minid[w][c] < M.minid[w][c]))) { M.minm[w][c] = A.minm[w][c]; M.minid[w][c] = A.minid[w][c]; }
      }
      M.viol[w].insert(M.viol[w].end(), A.viol[w].begin(), A.viol[w].end());
    }
    M.scores += A.scores; M.skipped += A.skipped;
    M.all.insert(M.all.end(), A.all.begin(), A.all.end());
  }
  auto byid = [](const TdRow& a, const TdRow& b) { return a.id < b.id; };
  for (int w = 0; w < 2; ++w) std::sort(M.viol[w].begin(), M.viol[w].end(), byid);
  std::sort(M.all.begin(), M.all.end(), byid);
  auto centre_txt = [&](long long id) {
    if (id < 0) return std::string("");
    long long um = id % nU; const std::vector<int>& P = Ps[id / nU];
    std::vector<int> S; for (int i = 0; i < s0n; ++i) if ((um >> i) & 1LL) S.push_back(s0[i]);
    for (int j : P) S.push_back(j); std::sort(S.begin(), S.end());
    std::string t; for (size_t q = 0; q < S.size(); ++q) { if (q) t += ";"; t += std::to_string(D0.orig[S[q]]); } return t; };
  const char* nm[] = {"a", "b", "c"};
  auto rows_df = [&](const std::vector<TdRow>& R, int w) {
    size_t m = R.size(); IntegerVector sz(m); NumericVector mg(m), gs(m), os(m); CharacterVector ce(m), clc(m), gm(m), om(m), ol(m);
    for (size_t i = 0; i < m; ++i) {
      const TdVar& v = (w == 0) ? R[i].lit : R[i].tow;
      sz[i] = R[i].size; mg[i] = v.margin; gs[i] = v.gstar; os[i] = v.ostar; ce[i] = R[i].centre; clc[i] = nm[R[i].clause];
      gm[i] = v.gmove; om[i] = v.omove; ol[i] = v.olabel; }
    return DataFrame::create(_["centre"] = ce, _["clause"] = clc, _["size"] = sz, _["margin"] = mg, _["g_star"] = gs, _["o_star"] = os,
                             _["g_move"] = gm, _["o_move"] = om, _["o_label"] = ol, _["stringsAsFactors"] = false); };
  auto clauses_of = [&](int w) {
    List cl(3); CharacterVector names(3);
    for (int c = 0; c < 3; ++c) {
      cl[c] = List::create(_["n_centres"] = (double)M.nc[c], _["n_violating"] = (double)M.nviol[w][c], _["n_violating_strict"] = (double)M.nviol_s[w][c],
                           _["min_margin"] = M.nc[c] ? M.minm[w][c] : NA_REAL, _["min_centre"] = centre_txt(M.minid[w][c]));
      names[c] = nm[c];
    }
    cl.attr("names") = names; return cl; };
  List toward = List::create(_["clauses"] = clauses_of(1), _["violators"] = rows_df(M.viol[1], 1));
  List out = List::create(_["clauses"] = clauses_of(0), _["violators"] = rows_df(M.viol[0], 0), _["scores_used"] = (double)M.scores,
                          _["n_centres"] = (double)(M.nc[0] + M.nc[1] + M.nc[2]), _["n_centres_skipped_over_K"] = (double)M.skipped,
                          _["toward"] = toward);
  if (keep_all) { out["centres"] = rows_df(M.all, 0); List tc = out["toward"]; tc["centres"] = rows_df(M.all, 1); out["toward"] = tc; }
  return out;
}
