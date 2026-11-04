// n9_harness.cpp -- N9 (V5) numerical check against the PRODUCTION engine.
//
// It #includes the production headers of Scripts/SMC_BVS/core/cpp/ unchanged (v3_engine.h pulls v3_util, v3_score,
// v3_blocks, v3_start, v3_ledger, v3_calib, v3_runtime). The only shim is the three R symbols that v3_runtime.h:29-31
// refers to (SEXP, Rf_isNull, Rcpp::XPtr), which are never called here.
//
// What it does, for one design (n, p, design type, seed) and each phi in the list:
//   1. Builds Data (data_init), blocks (make_blocks), tables (build_tables), start (build_start) and the neighbour graph
//      (neighbour_graph) exactly as cpp_setup does (v3_core.cpp:269-300), with the production B = min(isqrt n, isqrt p, 16).
//   2. Enumerates the state space {S : |S| <= K} and evaluates every state with Engine::eval (production lg0, d, logm).
//   3. Extracts the EXACT transition kernel of each production step function (Engine::step_gibbs, step_uswap,
//      step_nswap, step_indep) by driving it with a scripted VariateSource:
//        - discrete uniform choices floor(u*k) are driven with u = (a+1/2)/k, a = 0..k-1 (probability 1/k each,
//          i.e. the continuous-uniform idealisation);
//        - the accept uniform's threshold is found by bisection on the 2^-53 grid of the production RNG
//          (v3_util.h:60), so the acceptance probability is the production one;
//        - the proposal is read from Engine::tmpQ after the call;
//        - the pi_0 proposal law of step_indep is extracted from draw_pi0 itself by a depth-first interval search
//          on each uniform it consumes (exact, on the 2^-53 grid).
//      The Gibbs probability o_j is read from rb_acc (v3_engine.h:128, recorded before the draw).
//   4. Checks detailed balance of each step and of the uniformly-random-order round (exact average over all orders,
//      computed by a dynamic programme over label subsets), invariance, and the asymmetry of one fixed order.
//   5. Checks the start sampler: Z̄0 from build_start vs brute force; law of draw_pi0 vs gamma_0/Z̄0; a large
//      production-RNG sample (chi-square, TV).
//   6. Monte Carlo of Engine::one_round (production RNG and Fisher-Yates order) vs the computed round kernel row.
//   7. Negative controls (mirrored, mutated steps): neighbour swap without its Hastings factor; independence step with
//      the symmetric-proposal acceptance. These must FAIL detailed balance (power of the check).
//   8. Independent long-double re-implementation of log m(S) (M §5) and of gamma_phi(S) from the spec formula.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <random>
#include <memory>
typedef void* SEXP;
inline bool Rf_isNull(SEXP x) { return x == nullptr; }
namespace Rcpp { template <class T> struct XPtr { T* p; explicit XPtr(SEXP x) : p((T*)x) {} T* get() const { return p; } }; }
#include "v3_engine.h"

using namespace v3;
typedef long double LD;
static const double TWO53 = 9007199254740992.0;  // 2^53

struct Scripted : public VariateSource {
  std::vector<double> q; size_t pos = 0; int n = 0;
  double u(const char*) override { ++n; return pos < q.size() ? q[pos++] : (pos++, 0.0); }
  void reset(const std::vector<double>& v) { q = v; pos = 0; n = 0; }
};

static int isqrt_i(int x) { int r = (int)std::floor(std::sqrt((double)x)); while ((r + 1) * (r + 1) <= x) ++r; while (r * r > x) --r; return r; }

// ------------------------------------------------------------------ design
static void make_design(int n, int p, int type, uint64_t seed, std::vector<double>& X, std::vector<double>& y) {
  std::mt19937_64 g(seed); std::normal_distribution<double> N01(0.0, 1.0);
  std::vector<double> Z((size_t)n * p);
  for (auto& v : Z) v = N01(g);
  X.assign((size_t)n * p, 0.0);
  for (int i = 0; i < n; ++i) {
    if (type == 0) {  // AR(1), rho = 0.8
      double prev = Z[i];
      X[i] = prev;
      for (int j = 1; j < p; ++j) { prev = 0.8 * prev + 0.6 * Z[(size_t)j * n + i]; X[(size_t)j * n + i] = prev; }
    } else {          // factor groups: {0,1,2} strong (r ~ 0.9), {3,4} moderate (r ~ 0.6), rest independent
      double f1 = N01(g), f2 = N01(g);
      for (int j = 0; j < p; ++j) {
        double e = Z[(size_t)j * n + i];
        double v = (j <= 2) ? 0.95 * f1 + 0.31 * e : (j <= 4 ? 0.77 * f2 + 0.64 * e : e);
        X[(size_t)j * n + i] = v;
      }
    }
  }
  std::vector<double> beta(p, 0.0);
  beta[0] = 1.0; if (p > 3) beta[3] = -0.8; if (p > 5) beta[p - 1] = 0.6;
  y.assign(n, 0.0);
  for (int i = 0; i < n; ++i) { double s = 0; for (int j = 0; j < p; ++j) s += X[(size_t)j * n + i] * beta[j]; y[i] = s + N01(g); }
  auto standardise = [&](double* v) {
    double m = 0; for (int i = 0; i < n; ++i) m += v[i]; m /= n;
    double ss = 0; for (int i = 0; i < n; ++i) { v[i] -= m; ss += v[i] * v[i]; }
    double sd = std::sqrt(ss / (n - 1)); for (int i = 0; i < n; ++i) v[i] /= sd;
  };
  for (int j = 0; j < p; ++j) standardise(&X[(size_t)j * n]);
  standardise(y.data());
}

// ------------------------------------------------------------------ independent log m (M §5) in long double
static LD logdet_solve(std::vector<LD> A, int k, std::vector<LD>* rhs) {  // returns log det (A SPD), solves A x = rhs
  LD ld = 0;
  for (int c = 0; c < k; ++c) {
    int piv = c; for (int r = c + 1; r < k; ++r) if (fabsl(A[r * k + c]) > fabsl(A[piv * k + c])) piv = r;
    if (piv != c) { for (int t = 0; t < k; ++t) std::swap(A[c * k + t], A[piv * k + t]); if (rhs) std::swap((*rhs)[c], (*rhs)[piv]); }
    LD d = A[c * k + c]; ld += logl(fabsl(d));
    for (int r = c + 1; r < k; ++r) {
      LD f = A[r * k + c] / d;
      for (int t = c; t < k; ++t) A[r * k + t] -= f * A[c * k + t];
      if (rhs) (*rhs)[r] -= f * (*rhs)[c];
    }
  }
  if (rhs) for (int c = k - 1; c >= 0; --c) { LD s = (*rhs)[c]; for (int t = c + 1; t < k; ++t) s -= A[c * k + t] * (*rhs)[t]; (*rhs)[c] = s / A[c * k + c]; }
  return ld;
}
static LD indep_logm(const Data& D, const std::vector<int>& S) {
  int k = (int)S.size(), n = D.n;
  LD a0 = 0.01L, b0 = 0.01L, nu = a0 + n / 2.0L;
  LD logCn = a0 * logl(2 * b0) + lgammal(a0 + n / 2.0L) - (n / 2.0L) * logl(acosl(-1.0L)) - lgammal(a0);
  LD yty = 0; for (int i = 0; i < n; ++i) yty += (LD)D.y[i] * D.y[i];
  if (k == 0) return logCn - nu * logl(2 * b0 + yty);
  std::vector<LD> G(k * k), H(k * k), A(k * k), z(k);
  for (int a = 0; a < k; ++a) {
    const double* xa = D.col(S[a]);
    LD s = 0; for (int i = 0; i < n; ++i) s += (LD)xa[i] * D.y[i]; z[a] = s;
    for (int b = 0; b < k; ++b) { const double* xb = D.col(S[b]); LD t = 0; for (int i = 0; i < n; ++i) t += (LD)xa[i] * xb[i]; G[a * k + b] = t; }
  }
  for (int a = 0; a < k; ++a) for (int b = 0; b < k; ++b) { H[a * k + b] = (n + 1) * G[a * k + b] + (a == b); A[a * k + b] = G[a * k + b] + (a == b); }
  std::vector<LD> w = z;
  LD ldH = logdet_solve(H, k, &w), ldA = logdet_solve(A, k, nullptr);
  LD quad = 0; for (int a = 0; a < k; ++a) quad += z[a] * w[a];
  LD Q = yty - n * quad;
  return logCn - 0.5L * (ldH - ldA) - nu * logl(2 * b0 + Q);
}

// ------------------------------------------------------------------ helpers
struct Ctx {
  Data D; Start st; std::vector<std::vector<int>> Nb; int B = 0;
  std::unique_ptr<Engine> E; Scripted src;
  std::vector<int> masks, idx;               // state list (bit masks) and inverse map
  std::vector<Particle> base;                // evaluated states
  int nS = 0;
};
static std::vector<int> mask_to_S(int m, int p) { std::vector<int> S; for (int j = 0; j < p; ++j) if (m >> j & 1) S.push_back(j); return S; }
static int S_to_mask(const std::vector<int>& S) { int m = 0; for (int j : S) m |= 1 << j; return m; }

typedef std::vector<double> Mat;  // dense nS x nS row-major, K[i*nS + j] = P(i -> j)

// smallest grid integer i in [0, 2^53] such that accepted(i * 2^-53) is false (accept set = [0, i)); returns i / 2^53
template <class F> static double accept_threshold(F accepted) {
  if (!accepted(0.0)) return 0.0;
  uint64_t lo = 0, hi = (uint64_t)1 << 53;
  while (hi - lo > 1) { uint64_t mid = lo + (hi - lo) / 2; if (accepted((double)mid / TWO53)) lo = mid; else hi = mid; }
  return (double)hi / TWO53;
}

// ---- exact law of draw_pi0 (production) by depth-first interval search over its uniforms
struct Leaf { int mask; double prob; std::vector<double> path; };
static void pi0_dfs(Ctx& c, std::vector<double> prefix, double prob, std::vector<Leaf>& out, long& runs) {
  std::vector<int> S;
  auto run = [&](const std::vector<double>& q) { c.src.reset(q); draw_pi0(c.st, c.src, S); ++runs; return S_to_mask(S); };
  int m0 = run(prefix);
  if (c.src.n <= (int)prefix.size()) { out.push_back({m0, prob, prefix}); return; }
  uint64_t lo = 0, END = (uint64_t)1 << 53;
  while (lo < END) {
    std::vector<double> q = prefix; q.push_back((double)lo / TWO53);
    int o = run(q);
    uint64_t a = lo, b = END;  // outcome(a) == o; find first x > lo with outcome != o (contiguous: cat_draw_gt is monotone)
    while (b - a > 1) { uint64_t mid = a + (b - a) / 2; q.back() = (double)mid / TWO53; if (run(q) == o) a = mid; else b = mid; }
    double w = (double)(b - lo) / TWO53;
    std::vector<double> np = prefix; np.push_back((double)lo / TWO53);
    pi0_dfs(c, np, prob * w, out, runs);
    lo = b;
  }
}

static void set_state(Ctx& c, Particle& P, int s) { P = c.base[s]; }

// ---- kernels of the four production steps
static Mat kernel_gibbs(Ctx& c, int j, double phi, double& max_thr_err) {
  int nS = c.nS; Mat K(nS * nS, 0.0); Engine& E = *c.E;
  for (int s = 0; s < nS; ++s) {
    Particle P; set_state(c, P, s);
    E.rb_on = true; E.rb_acc.assign(c.D.p, 0.0);
    c.src.reset({0.0}); E.step_gibbs(P, j, phi);
    double oj = E.rb_acc[j]; E.rb_on = false;
    int in_mask = c.masks[s] | (1 << j), out_mask = c.masks[s] & ~(1 << j);
    if (oj > 0) { if (S_to_mask(P.S) != in_mask) { fprintf(stderr, "gibbs: u=0 outcome mismatch\n"); exit(2); } }
    // accept-threshold extraction (include iff u < o_j) cross-check with the recorded o_j
    double thr = accept_threshold([&](double u) { Particle Q; set_state(c, Q, s); c.src.reset({u}); E.step_gibbs(Q, j, phi); return S_to_mask(Q.S) == in_mask; });
    max_thr_err = std::max(max_thr_err, std::fabs(thr - oj) * TWO53);  // in units of 2^-53
    if (oj > 0) K[s * nS + c.idx[in_mask]] += oj;
    if (oj < 1) K[s * nS + c.idx[out_mask]] += 1.0 - oj;
  }
  return K;
}
static Mat kernel_uswap(Ctx& c, double phi, long& nprop) {
  int nS = c.nS, p = c.D.p; Mat K(nS * nS, 0.0); Engine& E = *c.E;
  for (int s = 0; s < nS; ++s) {
    int k = __builtin_popcount(c.masks[s]);
    if (k == 0 || k == p) {
      Particle P; set_state(c, P, s); c.src.reset({}); E.step_uswap(P, phi);
      if (c.src.n != 0 || S_to_mask(P.S) != c.masks[s]) { fprintf(stderr, "uswap boundary not a pure self-loop\n"); exit(2); }
      K[s * nS + s] += 1.0; continue;
    }
    std::set<int> seen;
    double w = 1.0 / ((double)k * (p - k));
    for (int a = 0; a < k; ++a) for (int b = 0; b < p - k; ++b) {
      double ua = (a + 0.5) / k, ub = (b + 0.5) / (p - k);
      Particle P; set_state(c, P, s); c.src.reset({ua, ub, 0.0}); E.step_uswap(P, phi);
      int prop = S_to_mask(E.tmpQ.S); ++nprop;
      if (!seen.insert(prop).second) { fprintf(stderr, "uswap: proposal map not injective\n"); exit(2); }
      double alpha = accept_threshold([&](double u) { Particle Q; set_state(c, Q, s); c.src.reset({ua, ub, u}); E.step_uswap(Q, phi); return S_to_mask(Q.S) == prop; });
      K[s * nS + c.idx[prop]] += w * alpha; K[s * nS + s] += w * (1 - alpha);
    }
  }
  return K;
}
static Mat kernel_nswap(Ctx& c, double phi, long& nprop, long& nasym) {
  int nS = c.nS; Mat K(nS * nS, 0.0); Engine& E = *c.E;
  for (int s = 0; s < nS; ++s) {
    std::vector<int> S = mask_to_S(c.masks[s], c.D.p); int k = (int)S.size();
    if (k == 0) {
      Particle P; set_state(c, P, s); c.src.reset({}); E.step_nswap(P, phi, 1);
      if (c.src.n != 0 || S_to_mask(P.S) != c.masks[s]) { fprintf(stderr, "nswap at empty not a pure self-loop\n"); exit(2); }
      K[s * nS + s] += 1.0; continue;
    }
    for (int a = 0; a < k; ++a) {
      double ua = (a + 0.5) / k;
      int j = S[a];
      int cnt = 0; for (int l : c.Nb[j]) if (!(c.masks[s] >> l & 1)) ++cnt;   // mirrors v3_engine.h:169
      Particle P0; set_state(c, P0, s); c.src.reset({ua}); E.step_nswap(P0, phi, 1);
      if (cnt == 0) {
        if (c.src.n != 1 || S_to_mask(P0.S) != c.masks[s]) { fprintf(stderr, "nswap empty-candidate branch not a self-loop\n"); exit(2); }
        K[s * nS + s] += 1.0 / k; continue;
      }
      for (int b = 0; b < cnt; ++b) {
        double ub = (b + 0.5) / cnt;
        Particle P; set_state(c, P, s); c.src.reset({ua, ub, 0.0}); E.step_nswap(P, phi, 1);
        int prop = S_to_mask(E.tmpQ.S); ++nprop;
        int l = __builtin_ctz(prop & ~c.masks[s]);
        int back = 0; for (int x : c.Nb[l]) if (!(prop >> x & 1)) ++back;
        if (back != cnt) ++nasym;
        double alpha = accept_threshold([&](double u) { Particle Q; set_state(c, Q, s); c.src.reset({ua, ub, u}); E.step_nswap(Q, phi, 1); return S_to_mask(Q.S) == prop; });
        double w = 1.0 / ((double)k * cnt);
        K[s * nS + c.idx[prop]] += w * alpha; K[s * nS + s] += w * (1 - alpha);
      }
    }
  }
  return K;
}
static Mat kernel_indep(Ctx& c, double phi, const std::vector<Leaf>& leaves) {
  int nS = c.nS; Mat K(nS * nS, 0.0); Engine& E = *c.E;
  for (int s = 0; s < nS; ++s) {
    for (const Leaf& L : leaves) {
      std::vector<double> q = L.path; q.push_back(0.0);
      Particle P; set_state(c, P, s); c.src.reset(q); E.step_indep(P, phi);
      if (S_to_mask(E.tmpQ.S) != L.mask) { fprintf(stderr, "indep: proposal path mismatch\n"); exit(2); }
      if (L.mask == c.masks[s]) { K[s * nS + s] += L.prob; continue; }
      double alpha = accept_threshold([&](double u) { std::vector<double> qq = L.path; qq.push_back(u); Particle Q; set_state(c, Q, s); c.src.reset(qq); E.step_indep(Q, phi); return S_to_mask(Q.S) == L.mask; });
      K[s * nS + c.idx[L.mask]] += L.prob * alpha; K[s * nS + s] += L.prob * (1 - alpha);
    }
  }
  return K;
}
// ---- negative controls (mirrors of v3_engine.h:162-192 with one deliberate mutation each)
static Mat kernel_nswap_nohastings(Ctx& c, double phi) {
  int nS = c.nS; Mat K(nS * nS, 0.0);
  for (int s = 0; s < nS; ++s) {
    std::vector<int> S = mask_to_S(c.masks[s], c.D.p); int k = (int)S.size();
    if (k == 0) { K[s * nS + s] = 1; continue; }
    for (int j : S) {
      std::vector<int> cand; for (int l : c.Nb[j]) if (!(c.masks[s] >> l & 1)) cand.push_back(l);
      if (cand.empty()) { K[s * nS + s] += 1.0 / k; continue; }
      for (int l : cand) {
        int t = c.idx[(c.masks[s] & ~(1 << j)) | (1 << l)];
        double la = c.base[t].lgphi(phi) - c.base[s].lgphi(phi);   // MUTATION: Hastings factor |N(j)\S|/|N(l)\S'| dropped
        double al = la >= 0 ? 1 : std::exp(la), w = 1.0 / ((double)k * cand.size());
        K[s * nS + t] += w * al; K[s * nS + s] += w * (1 - al);
      }
    }
  }
  return K;
}
static Mat kernel_indep_symmetric(Ctx& c, double phi, const std::vector<Leaf>& leaves) {
  int nS = c.nS; Mat K(nS * nS, 0.0);
  for (int s = 0; s < nS; ++s) for (const Leaf& L : leaves) {
    int t = c.idx[L.mask];
    if (t == s) { K[s * nS + s] += L.prob; continue; }
    double la = c.base[t].lgphi(phi) - c.base[s].lgphi(phi);       // MUTATION: proposal ratio pi_0(S)/pi_0(S') dropped
    double al = la >= 0 ? 1 : std::exp(la);
    K[s * nS + t] += L.prob * al; K[s * nS + s] += L.prob * (1 - al);
  }
  return K;
}

// ---- diagnostics
struct DB { double rowsum_err, inv_l1, db_rel, db_abs; };
static DB check_db(const Mat& K, const std::vector<double>& pi, int nS) {
  DB r{0, 0, 0, 0};
  for (int i = 0; i < nS; ++i) { double s = 0; for (int j = 0; j < nS; ++j) s += K[i * nS + j]; r.rowsum_err = std::max(r.rowsum_err, std::fabs(s - 1)); }
  for (int j = 0; j < nS; ++j) { LD s = 0; for (int i = 0; i < nS; ++i) s += (LD)pi[i] * K[i * nS + j]; r.inv_l1 += std::fabs((double)(s - pi[j])); }
  for (int i = 0; i < nS; ++i) for (int j = i + 1; j < nS; ++j) {
    double f = pi[i] * K[i * nS + j], g = pi[j] * K[j * nS + i];
    double d = std::fabs(f - g), m = std::max(f, g);
    r.db_abs = std::max(r.db_abs, d);
    if (m > 0) r.db_rel = std::max(r.db_rel, d / m);
  }
  return r;
}
static Mat matmul(const Mat& A, const Mat& Bm, int n) {
  Mat C(n * n, 0.0);
  for (int i = 0; i < n; ++i) for (int k = 0; k < n; ++k) { double a = A[i * n + k]; if (a == 0) continue; for (int j = 0; j < n; ++j) C[i * n + j] += a * Bm[k * n + j]; }
  return C;
}
// uniformly random order of the labelled steps: average over all m! orders of K_{s1} K_{s2} ... K_{sm}
// (first step leftmost). DP: V(T) = (1/|T|) sum_{t in T} mult(t) K_t V(T \ t), on column blocks.
static Mat round_kernel(const std::vector<Mat>& KG, const Mat& KU, const Mat& KN, const Mat& KI, int p, int B, int nS) {
  // sparse forms for G, U, N
  auto sparse = [&](const Mat& M) { std::vector<std::vector<std::pair<int, double>>> R(nS); for (int i = 0; i < nS; ++i) for (int j = 0; j < nS; ++j) if (M[i * nS + j] != 0) R[i].push_back({j, M[i * nS + j]}); return R; };
  std::vector<std::vector<std::vector<std::pair<int, double>>>> sG; for (auto& M : KG) sG.push_back(sparse(M));
  auto sU = sparse(KU), sN = sparse(KN);
  int NG = 1 << p, NB = B + 1;
  auto sid = [&](int g, int nn, int u, int i) { return ((g * NB + nn) * 2 + u) * 2 + i; };
  int NSET = NG * NB * 4;
  Mat R(nS * nS, 0.0);
  const int CB = 16;
  std::vector<std::vector<double>> V(NSET);
  for (int c0 = 0; c0 < nS; c0 += CB) {
    int cb = std::min(CB, nS - c0);
    auto mulS = [&](const std::vector<std::vector<std::pair<int, double>>>& Sp, const std::vector<double>& x, std::vector<double>& y, double w) {
      for (int i = 0; i < nS; ++i) for (auto& e : Sp[i]) { const double* xr = &x[e.first * cb]; double a = w * e.second; for (int t = 0; t < cb; ++t) y[i * cb + t] += a * xr[t]; }
    };
    auto mulD = [&](const Mat& M, const std::vector<double>& x, std::vector<double>& y, double w) {
      for (int i = 0; i < nS; ++i) for (int k = 0; k < nS; ++k) { double a = M[i * nS + k]; if (a == 0) continue; a *= w; const double* xr = &x[k * cb]; for (int t = 0; t < cb; ++t) y[i * cb + t] += a * xr[t]; }
    };
    // order sets by size
    std::vector<std::vector<int>> bysize(p + B + 3);
    for (int g = 0; g < NG; ++g) for (int nn = 0; nn < NB; ++nn) for (int u = 0; u < 2; ++u) for (int i = 0; i < 2; ++i)
      bysize[__builtin_popcount(g) + nn + u + i].push_back(sid(g, nn, u, i));
    for (auto& v : V) v.clear();
    V[sid(0, 0, 0, 0)].assign(nS * cb, 0.0);
    for (int t = 0; t < cb; ++t) V[sid(0, 0, 0, 0)][(c0 + t) * cb + t] = 1.0;
    for (int sz = 1; sz <= p + B + 2; ++sz) {
      for (int id : bysize[sz]) {
        int i = id & 1, u = (id >> 1) & 1, rest = id >> 2, nn = rest % NB, g = rest / NB;
        std::vector<double> y(nS * cb, 0.0);
        double w = 1.0 / sz;
        for (int j = 0; j < p; ++j) if (g >> j & 1) mulS(sG[j], V[sid(g & ~(1 << j), nn, u, i)], y, w);
        if (nn > 0) mulS(sN, V[sid(g, nn - 1, u, i)], y, w * nn);
        if (u) mulS(sU, V[sid(g, nn, 0, i)], y, w);
        if (i) mulD(KI, V[sid(g, nn, u, 0)], y, w);
        V[id].swap(y);
      }
      // free size sz-1
      for (int id : bysize[sz - 1]) { std::vector<double>().swap(V[id]); }
    }
    const auto& F = V[sid(NG - 1, B, 1, 1)];
    for (int i = 0; i < nS; ++i) for (int t = 0; t < cb; ++t) R[i * nS + c0 + t] = F[i * cb + t];
  }
  return R;
}

static double chisq_upper_p(double x, double df) {  // Wilson-Hilferty approximation of P(chi2_df > x)
  double z = (std::cbrt(x / df) - (1 - 2 / (9 * df))) / std::sqrt(2 / (9 * df));
  return 0.5 * std::erfc(z / std::sqrt(2.0));
}

int main(int argc, char** argv) {
  if (argc < 6) { fprintf(stderr, "usage: n9_harness n p design_type seed nmc [phi ...]\n"); return 1; }
  int n = atoi(argv[1]), p = atoi(argv[2]), type = atoi(argv[3]); uint64_t seed = strtoull(argv[4], 0, 10); long nmc = atol(argv[5]);
  std::vector<double> phis; for (int a = 6; a < argc; ++a) phis.push_back(atof(argv[a]));
  if (phis.empty()) phis = {0.0, 0.5, 1.0};
  Ctx c;
  std::vector<double> X, y; make_design(n, p, type, seed, X, y);
  std::vector<int> orig(p); for (int j = 0; j < p; ++j) orig[j] = j + 1;
  data_init(c.D, X.data(), y.data(), n, p, orig);
  c.B = std::min(std::min(isqrt_i(n), isqrt_i(p)), 16);   // v3_preprocess.R:22
  c.st.D = &c.D; c.st.B = c.B;
  c.st.blocks = make_blocks(c.D, c.B);
  Scorer sc(&c.D); build_tables(c.st, sc); build_start(c.st);
  c.Nb = neighbour_graph(c.D, c.B);
  c.E.reset(new Engine(c.D, c.st, c.Nb, c.B)); c.E->vs = &c.src;
  int K = c.D.K;
  printf("# N9 harness: n=%d p=%d design=%s seed=%llu  K=%d  B=%d  m=p+B+2=%d\n", n, p, type == 0 ? "AR1(0.8)" : "factor-groups", (unsigned long long)seed, K, c.B, p + c.B + 2);
  printf("blocks:"); for (auto& b : c.st.blocks) { printf(" {"); for (size_t i = 0; i < b.size(); ++i) printf("%s%d", i ? "," : "", b[i]); printf("}"); } printf("\n");
  printf("neighbour graph N(j) (0-based) and degree:\n");
  for (int j = 0; j < p; ++j) { printf("  N(%d) = {", j); for (size_t i = 0; i < c.Nb[j].size(); ++i) printf("%s%d", i ? "," : "", c.Nb[j][i]); printf("}  deg=%zu\n", c.Nb[j].size()); }
  bool sym = true; for (int j = 0; j < p; ++j) for (int l : c.Nb[j]) { if (l == j) sym = false; if (!std::binary_search(c.Nb[l].begin(), c.Nb[l].end(), j)) sym = false; }
  printf("graph symmetric and loop-free: %s\n", sym ? "yes" : "NO");
  // states
  c.idx.assign(1 << p, -1);
  for (int m = 0; m < (1 << p); ++m) if (__builtin_popcount(m) <= K) { c.idx[m] = (int)c.masks.size(); c.masks.push_back(m); }
  c.nS = (int)c.masks.size();
  c.base.resize(c.nS);
  for (int s = 0; s < c.nS; ++s) { c.E->set_model(c.base[s], mask_to_S(c.masks[s], p)); c.E->eval(c.base[s], ME_INIT, false); }
  printf("states |S|<=K: %d\n", c.nS);

  // ---- (8) independent log m and spec gamma_phi
  {
    double dm = 0; std::vector<LD> lm(c.nS);
    for (int s = 0; s < c.nS; ++s) { lm[s] = indep_logm(c.D, mask_to_S(c.masks[s], p)); dm = std::max(dm, (double)fabsl(lm[s] - (LD)c.base[s].logm)); }
    printf("[spec] max |log m_prod - log m_indep(long double)| = %.3e\n", dm);
    // spec: log gamma_phi = log varpi(k) + phi (log m(S) - log m(0)) + (1-phi) sum_b [log m(S n C_b) - log m(0)]
    LD lm0 = lm[c.idx[0]];
    for (double phi : phis) {
      double dg = 0; LD ref = 0; bool first = true;
      for (int s = 0; s < c.nS; ++s) {
        std::vector<int> S = mask_to_S(c.masks[s], p);
        LD comp = 0;
        for (auto& b : c.st.blocks) { int mm = 0; for (int j : b) if (c.masks[s] >> j & 1) mm |= 1 << j; if (mm) comp += lm[c.idx[mm]] - lm0; }
        LD g = (LD)c.D.logprior[S.size()] + phi * (lm[s] - lm0) + (1 - phi) * comp;
        LD diff = g - (LD)c.base[s].lgphi(phi);
        if (first) { ref = diff; first = false; }
        dg = std::max(dg, (double)fabsl(diff - ref));
      }
      printf("[spec] phi=%.2f: max |log gamma_phi(code) - log gamma_phi(spec)| up to a constant = %.3e\n", phi, dg);
    }
  }

  // ---- (5) start sampler
  std::vector<Leaf> leaves; long runs = 0;
  pi0_dfs(c, {}, 1.0, leaves, runs);
  {
    LD Zbf = 0; for (int s = 0; s < c.nS; ++s) Zbf += expl((LD)c.base[s].lg0);
    printf("[start] log Zbar0 (build_start) = %.15f ; brute force log sum_S gamma0 = %.15Lf ; diff = %.3e\n", c.st.logZbar0, logl(Zbf), (double)(c.st.logZbar0 - logl(Zbf)));
    LD Zind = 0; std::vector<LD> lmi(c.nS);
    for (int s = 0; s < c.nS; ++s) lmi[s] = indep_logm(c.D, mask_to_S(c.masks[s], p));
    for (int s = 0; s < c.nS; ++s) { LD comp = 0; for (auto& b : c.st.blocks) { int mm = 0; for (int j : b) if (c.masks[s] >> j & 1) mm |= 1 << j; if (mm) comp += lmi[c.idx[mm]] - lmi[c.idx[0]]; }
      int k = __builtin_popcount(c.masks[s]); LD lw = -logl(2.0L) - (lgammal(2.0L * p) - lgammal(k + 1.0L) - lgammal(2.0L * p - k)); Zind += expl(lw + comp); }
    LD WK = 0; for (int k = 0; k <= K; ++k) WK += expl(lgammal(p + 1.0L) - lgammal(k + 1.0L) - lgammal(p - k + 1.0L) - logl(2.0L) - (lgammal(2.0L * p) - lgammal(k + 1.0L) - lgammal(2.0L * p - k)));
    printf("[start] independent (spec §5/§6.3, long double, own w(k), W_K, r_b) log Zbar0 = %.15Lf ; diff to build_start = %.3e\n", logl(Zind / WK), (double)(c.st.logZbar0 - logl(Zind / WK)));
    std::vector<double> q(c.nS, 0.0); int dup = 0;
    for (auto& L : leaves) { if (q[c.idx[L.mask]] != 0) ++dup; q[c.idx[L.mask]] += L.prob; }
    double tot = 0, maxrel = 0, tv = 0; int zero = 0;
    for (int s = 0; s < c.nS; ++s) {
      double ex = std::exp(c.st.log_pi0(mask_to_S(c.masks[s], p)));
      tot += q[s]; if (q[s] == 0) ++zero;
      maxrel = std::max(maxrel, std::fabs(q[s] - ex) / ex); tv += 0.5 * std::fabs(q[s] - ex);
    }
    printf("[start] draw_pi0 exact law (DFS over its uniforms, %zu leaves, %ld calls, %d duplicate leaves, %d states with mass 0): total=%.17g\n", leaves.size(), runs, dup, zero, tot);
    printf("[start] law(draw_pi0) vs gamma0/Zbar0: max relative error = %.3e, TV = %.3e\n", maxrel, tv);
    // large production-RNG sample
    RngSource rs; rs.g.seed_stream(seed, 77);
    std::vector<long> cnt(c.nS, 0); std::vector<int> S;
    for (long t = 0; t < nmc * 10; ++t) { draw_pi0(c.st, rs, S); cnt[c.idx[S_to_mask(S)]]++; }
    double chi = 0, tvs = 0; int df = -1; long NN = nmc * 10;
    for (int s = 0; s < c.nS; ++s) { double e = NN * q[s]; if (e > 0) { chi += (cnt[s] - e) * (cnt[s] - e) / e; ++df; } tvs += 0.5 * std::fabs(cnt[s] / (double)NN - q[s]); }
    printf("[start] production RNG sample N=%ld: chi2=%.1f df=%d p~%.3f ; TV(emp, exact)=%.4f (E[TV] scale ~ %.4f)\n", NN, chi, df, chisq_upper_p(chi, df), tvs, std::sqrt(c.nS / (2 * 3.14159 * NN)));
  }

  // ---- steps and round per phi
  for (double phi : phis) {
    std::vector<double> pi(c.nS); double mx = NEG_INF;
    for (int s = 0; s < c.nS; ++s) mx = std::max(mx, c.base[s].lgphi(phi));
    LD Zs = 0; for (int s = 0; s < c.nS; ++s) Zs += expl((LD)c.base[s].lgphi(phi) - mx);
    for (int s = 0; s < c.nS; ++s) pi[s] = (double)(expl((LD)c.base[s].lgphi(phi) - mx) / Zs);
    printf("\n== phi = %.2f ==\n", phi);
    std::vector<Mat> KG; double thr = 0;
    for (int j = 0; j < p; ++j) KG.push_back(kernel_gibbs(c, j, phi, thr));
    long npu = 0, npn = 0, nasym = 0;
    Mat KU = kernel_uswap(c, phi, npu), KN = kernel_nswap(c, phi, npn, nasym), KI = kernel_indep(c, phi, leaves);
    printf("Gibbs: o_j vs extracted accept threshold: max diff = %.1f grid units (2^-53)\n", thr);
    printf("proposals enumerated: uswap %ld, nswap %ld (of which %ld with |N(j)\\S| != |N(l)\\S'|, i.e. Hastings factor != 1)\n", npu, npn, nasym);
    auto rep = [&](const char* nm, const Mat& K) { DB d = check_db(K, pi, c.nS);
      printf("  %-28s rowsum_err=%.2e  ||piK-pi||_1=%.2e  DB max rel=%.2e  DB max abs=%.2e\n", nm, d.rowsum_err, d.inv_l1, d.db_rel, d.db_abs); return d; };
    double worst_g = 0; for (int j = 0; j < p; ++j) { char b[32]; snprintf(b, 32, "Gibbs j=%d", j); worst_g = std::max(worst_g, rep(b, KG[j]).db_rel); }
    rep("uniform swap", KU); rep("neighbour swap", KN); rep("independence (pi0)", KI);
    Mat R = round_kernel(KG, KU, KN, KI, p, c.B, c.nS);
    rep("ROUND (uniform random order)", R);
    // a fixed order: canonical list G1..Gp, U, N1..NB, I
    Mat F = KG[0]; for (int j = 1; j < p; ++j) F = matmul(F, KG[j], c.nS); F = matmul(F, KU, c.nS); for (int b = 0; b < c.B; ++b) F = matmul(F, KN, c.nS); F = matmul(F, KI, c.nS);
    rep("fixed canonical order", F);
    printf("  negative controls (must fail DB):\n");
    rep("  nswap w/o Hastings factor", kernel_nswap_nohastings(c, phi));
    rep("  indep w/ symmetric accept", kernel_indep_symmetric(c, phi, leaves));
    // ---- (6) MC of the production one_round vs row of R
    if (nmc > 0) {
      RngSource rs; rs.g.seed_stream(seed, 1000 + (uint64_t)(phi * 100));
      c.E->vs = &rs;
      int starts[3] = {0, c.idx[c.masks[c.nS - 1]], c.nS / 2};
      for (int s0 : starts) {
        std::vector<long> cnt(c.nS, 0);
        for (long t = 0; t < nmc; ++t) { Particle P = c.base[s0]; c.E->one_round(P, 0, phi); cnt[c.idx[S_to_mask(P.S)]]++; }
        double chi = 0, tv = 0; int df = -1;
        for (int s = 0; s < c.nS; ++s) { double e = nmc * R[s0 * c.nS + s]; if (e > 5) { chi += (cnt[s] - e) * (cnt[s] - e) / e; ++df; } tv += 0.5 * std::fabs(cnt[s] / (double)nmc - R[s0 * c.nS + s]); }
        printf("  MC one_round from state %d (|S|=%d), N=%ld: chi2=%.1f df=%d p~%.3f TV=%.4f\n", s0, __builtin_popcount(c.masks[s0]), nmc, chi, df, chisq_upper_p(chi, df), tv);
      }
      c.E->vs = &c.src;
    }
  }
  return 0;
}
