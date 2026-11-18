// g0_bench.cpp -- P1M gate G0 kernel benchmark (SMC - Engineering, 2026-11-15). Stand-alone; nothing here is engine code.
// Derived from /home/fb31/p1m_feas_bench/feas_bench.cpp (the feasibility study's benchmark; that folder is not edited).
// Lines from "#include <immintrin.h>" to draw_order() are copied verbatim from feas_bench.cpp; the drivers below are
// refactored into functions so that ONE process generates the data once and runs every mode at every thread count
// (mode `suite`), and a new mode `offer` times a bounded top-c store. Reference arithmetic for the bit checks:
// v3::Scorer::try_chol(S, from_X = true) from a COPY of the v3.1 core headers (core_copy/, = Scripts/SMC_BVS/core/cpp).
//
// modes:
//   suite  <p> <T list, e.g. 1,48,96,24> [direct_steps=200000] [frac1=0.05] [offer_cap=40000000] [bw_GB=4]
//          data once (all threads), round orders of 256 particles once; then for each T, in this order:
//          batch v2/v0 x {256 distinct supports, S0 alone}, direct, perm, bw; bit checks only at T = 1 (small samples);
//          then one pass-fraction run (untimed counts of F(S u j) - F(S) >= -Delta), then `offer` at T = 1 and the T > 1.
//   bw     <GB> <threads>                         sequential read bandwidth (sum of doubles)
//   perm   <p> <reps> [threads]                   Fisher-Yates order + inverse permutation, every thread its own
//   direct <p> <threads> <steps_per_thread> <kx> [checks]   particle-major Gram-free Gibbs step, random column order
//   batch  <p> <threads> <G> <kx> <div> <variant> <Bk> [frac] [check]
//          label-major kernel (see feas_bench.cpp): variant 0 = bit form, 1 = bit-form arithmetic + libmvec, 2 = class A.
//   offer  <cap> <threads> [p=1000000]           bounded top-c store (see the comment above struct FlatStore)
//   storetest                                    store self-test against a brute-force top-c (also run first by suite)
#include "core_copy/v3_score.h"
#include <immintrin.h>
#include <omp.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <numeric>

extern "C" __m512d _ZGVeN8v_log(__m512d);
extern "C" __m512d _ZGVeN8v_exp(__m512d);

using v3::Data; using v3::Scorer; using v3::ScoreOut;
typedef __m512d vd;
static inline vd bc(double x) { return _mm512_set1_pd(x); }
static double now() { return omp_get_wtime(); }
static const int KM = 8;   // max support size handled by the vector paths

struct Rng { v3::Xoshiro256ss g; double u() { return g.uniform(); }
  double norm() { double a = u(), b = u(); if (a < 1e-300) a = 1e-300; return std::sqrt(-2 * std::log(a)) * std::cos(2 * M_PI * b); } };

static std::vector<int> truth;
static std::vector<double> diagG;  // G_jj by the sequential sum (bits of the Gram diagonal)
static std::vector<double> logr1;   // log r of the singleton {j} (stand-in for the block-table entry)

// AR(0.6) columns (restarted every 1024 columns so that generation is parallel), standardised as M 4.4
// (mean 0, sample sd 1). y = X_S0 beta + eps, standardised.
static void make_data(Data& D, int n, int p, int threads) {
  D.n = n; D.p = p; D.K = std::min(p, n / 2); D.W = v3::nwords(p);
  D.X.resize((size_t)n * p);
  const int CH = 1024;
  #pragma omp parallel for schedule(dynamic, 4) num_threads(threads)
  for (int c0 = 0; c0 < p; c0 += CH) {
    Rng r; r.g.seed_stream(12345, (uint64_t)c0 + 1);
    std::vector<double> prev(n, 0.0);
    for (int j = c0; j < std::min(p, c0 + CH); ++j) {
      double* x = &D.X[(size_t)j * n];
      for (int i = 0; i < n; ++i) { double e = r.norm(); x[i] = (j == c0) ? e : 0.6 * prev[i] + 0.8 * e; prev[i] = x[i]; }
      double m = 0; for (int i = 0; i < n; ++i) m += x[i]; m /= n;
      double s = 0; for (int i = 0; i < n; ++i) { x[i] -= m; s += x[i] * x[i]; }
      s = std::sqrt(s / (n - 1)); for (int i = 0; i < n; ++i) x[i] /= s;
    }
  }
  truth.clear(); for (int k = 1; k <= 5; ++k) truth.push_back((int)std::floor((k - 0.5) * p / 5));
  const double beta[5] = {1.0, -0.8, 0.9, -0.7, 0.6};
  Rng r; r.g.seed_stream(777, 0);
  D.y.assign(n, 0.0);
  for (int i = 0; i < n; ++i) { double v = r.norm(); for (int k = 0; k < 5; ++k) v += beta[k] * D.col(truth[k])[i]; D.y[i] = v; }
  { double m = 0; for (double v : D.y) m += v; m /= n; double s = 0; for (double& v : D.y) { v -= m; s += v * v; }
    s = std::sqrt(s / (n - 1)); for (double& v : D.y) v /= s; }
  D.z.assign(p, 0.0); diagG.assign(p, 0.0);
  #pragma omp parallel for num_threads(threads)
  for (int a = 0; a < p; ++a) { const double* xa = D.col(a); double s = 0, g = 0; for (int i = 0; i < n; ++i) { s += xa[i] * D.y[i]; g += xa[i] * xa[i]; } D.z[a] = s; diagG[a] = g; }
  D.yty = 0; for (int i = 0; i < n; ++i) D.yty += D.y[i] * D.y[i];
  D.nu = D.a0 + n / 2.0;
  D.logCn = D.a0 * std::log(2 * D.b0) + std::lgamma(D.a0 + n / 2.0) - (n / 2.0) * std::log(M_PI) - std::lgamma(D.a0);
  D.logm0 = D.logCn - D.nu * std::log(2 * D.b0 + D.yty);
  D.logw.assign(D.K + 1, 0.0); std::vector<double> terms(D.K + 1);
  for (int k = 0; k <= D.K; ++k) { D.logw[k] = -M_LN2 - v3::lchoose_d(2.0 * p - 1.0, k); terms[k] = v3::lchoose_d((double)p, k) + D.logw[k]; }
  D.logWK = v3::log_sum_exp(terms);
  D.logprior.assign(D.K + 1, 0.0); for (int k = 0; k <= D.K; ++k) D.logprior[k] = D.logw[k] - D.logWK;
  logr1.assign(p, 0.0);
  #pragma omp parallel num_threads(threads)
  { Scorer sc(&D); std::vector<double> LH; std::vector<int> S(1);
    #pragma omp for
    for (int j = 0; j < p; ++j) { S[0] = j; ScoreOut o; sc.try_chol(S, true, o, LH); logr1[j] = o.logm - D.logm0; } }
}
static double ref_logm(Scorer& sc, const std::vector<int>& S) { ScoreOut o; std::vector<double> LH; if (!sc.try_chol(S, true, o, LH)) return NAN; return o.logm; }

// ------------------------------------------------------------------------------------------------------------
// Support cache: everything about S that the flip scores reuse.
// ------------------------------------------------------------------------------------------------------------
struct Support {
  int k = 0; int mem[KM]; int arow[KM];
  double MH[KM][KM], MA[KM][KM], LH[KM][KM], LA[KM][KM];
  double zS[KM], wH[KM];                  // forward solve L_H w = z_S
  double preH[KM + 1], preA[KM + 1], preQ[KM + 1], preC[KM + 1];  // prefix sums: log diag(L_H), log diag(L_A), w^2, comp
  double logm, lgphi, c; double ldH, ldA, quad;
  std::vector<double> XS;                  // row-major n x KM copy of the member columns (direct mode)
};
static void build_support(const Data& D, Support& s, const std::vector<int>& S, double phi) {
  int k = (int)S.size(), n = D.n; s.k = k; double n1 = n + 1.0;
  for (int a = 0; a < k; ++a) s.mem[a] = S[a];
  double Gs[KM][KM];
  for (int a = 0; a < k; ++a) for (int b = 0; b <= a; ++b) {
    const double* xa = D.col(S[a]); const double* xb = D.col(S[b]); double g = 0; for (int i = 0; i < n; ++i) g += xa[i] * xb[i];
    Gs[a][b] = g; Gs[b][a] = g; }
  for (int a = 0; a < k; ++a) for (int b = 0; b < k; ++b) { s.MH[a][b] = n1 * Gs[a][b] + (a == b ? 1.0 : 0.0); s.MA[a][b] = Gs[a][b] + (a == b ? 1.0 : 0.0); }
  auto chol = [&](double M[KM][KM], double L[KM][KM]) {
    for (int a = 0; a < k; ++a) for (int b = 0; b < k; ++b) L[a][b] = M[a][b];
    for (int j = 0; j < k; ++j) { double d = L[j][j]; for (int t = 0; t < j; ++t) d -= L[j][t] * L[j][t]; double l = std::sqrt(d); L[j][j] = l;
      for (int i = j + 1; i < k; ++i) { double x = L[i][j]; for (int t = 0; t < j; ++t) x -= L[i][t] * L[j][t]; L[i][j] = x / l; } } };
  chol(s.MH, s.LH); chol(s.MA, s.LA);
  s.preH[0] = s.preA[0] = s.preQ[0] = s.preC[0] = 0;
  for (int a = 0; a < k; ++a) {
    s.zS[a] = D.z[S[a]];
    double w = s.zS[a]; for (int t = 0; t < a; ++t) w -= s.LH[a][t] * s.wH[t]; s.wH[a] = w / s.LH[a][a];
    s.preH[a + 1] = s.preH[a] + std::log(s.LH[a][a]); s.preA[a + 1] = s.preA[a] + std::log(s.LA[a][a]);
    s.preQ[a + 1] = s.preQ[a] + s.wH[a] * s.wH[a]; s.preC[a + 1] = s.preC[a] + logr1[S[a]];
  }
  s.ldH = s.preH[k]; s.ldA = s.preA[k]; s.quad = s.preQ[k]; s.c = s.preC[k];
  double Q = D.yty - D.n * s.quad; double ldH = 2 * s.ldH, ldA = 2 * s.ldA;
  s.logm = D.logCn - 0.5 * (ldH - ldA) - D.nu * std::log(2 * D.b0 + Q);
  double lg0 = D.logprior[k] + s.c, d = (s.logm - D.logm0) - s.c; s.lgphi = lg0 + phi * d;
  s.XS.assign((size_t)n * KM, 0.0);
  for (int a = 0; a < k; ++a) { const double* xa = D.col(S[a]); for (int i = 0; i < n; ++i) s.XS[(size_t)i * KM + a] = xa[i]; }
}

static inline vd vlog_scalar(vd x) { alignas(64) double t[8]; _mm512_store_pd(t, x); for (int l = 0; l < 8; ++l) t[l] = std::log(t[l]); return _mm512_load_pd(t); }
static inline vd vexp_scalar(vd x) { alignas(64) double t[8]; _mm512_store_pd(t, x); for (int l = 0; l < 8; ++l) t[l] = std::exp(t[l]); return _mm512_load_pd(t); }

// Bit form: log m(S u {j}) for 8 labels j that share the sorted insertion position q. u[a] = G(mem[a], j), gjj, zj.
// Entries of the two Cholesky factors that do not involve the label are the cached ones of S (leading-submatrix
// property of the row/column recurrences in v3_score.h:76-90); the others follow the same operation order.
// Returns false if a pivot is not positive or Q is in the q_nonneg regime (caller falls back to the scalar reference).
template <bool FASTLOG>
static inline bool flip8_bit(const Data& D, const Support& s, int q, const vd* u, vd gjj, vd zj, vd& logm_out) {
  const int k = s.k, kk = k + 1; const double n1 = D.n + 1.0;
  auto sidx = [q](int t) { return t < q ? t : t - 1; };
  vd ld[2]; vd w[KM + 1]; vd quad;
  for (int which = 0; which < 2; ++which) {
    const double (*Ls)[KM] = which == 0 ? s.LH : s.LA; const double (*Ms)[KM] = which == 0 ? s.MH : s.MA;
    vd L[KM + 1][KM + 1];
    auto Mlab = [&](int a) { return which == 0 ? _mm512_add_pd(_mm512_mul_pd(bc(n1), u[a]), bc(0.0)) : _mm512_add_pd(u[a], bc(0.0)); };
    // row q, columns c < q
    for (int c = 0; c < q; ++c) { vd x = Mlab(c); for (int t = 0; t < c; ++t) x = _mm512_sub_pd(x, _mm512_mul_pd(L[q][t], bc(Ls[c][t]))); L[q][c] = _mm512_div_pd(x, bc(Ls[c][c])); }
    // columns c >= q
    for (int c = q; c < kk; ++c) {
      vd d = (c == q) ? (which == 0 ? _mm512_add_pd(_mm512_mul_pd(bc(n1), gjj), bc(1.0)) : _mm512_add_pd(gjj, bc(1.0))) : bc(Ms[c - 1][c - 1]);
      for (int t = 0; t < c; ++t) {
        vd lct = (t < q && c != q) ? bc(Ls[c - 1][t]) : L[c][t];
        d = _mm512_sub_pd(d, _mm512_mul_pd(lct, lct)); }
      if (_mm512_cmp_pd_mask(d, bc(0.0), _CMP_GT_OQ) != 0xFF) return false;
      vd l = _mm512_sqrt_pd(d); L[c][c] = l;
      for (int i = c + 1; i < kk; ++i) {
        vd x = (c == q) ? Mlab(i - 1) : bc(Ms[i - 1][c - 1]);
        for (int t = 0; t < c; ++t) {
          vd lit = (t < q) ? bc(Ls[i - 1][t]) : L[i][t];
          vd lct = (t < q && c != q) ? bc(Ls[c - 1][t]) : L[c][t];
          x = _mm512_sub_pd(x, _mm512_mul_pd(lit, lct)); }
        L[i][c] = _mm512_div_pd(x, l); }
    }
    vd acc = bc(which == 0 ? s.preH[q] : s.preA[q]);
    for (int a = q; a < kk; ++a) acc = _mm512_add_pd(acc, FASTLOG ? _ZGVeN8v_log(L[a][a]) : vlog_scalar(L[a][a]));
    ld[which] = acc;
    if (which == 0) {
      quad = bc(s.preQ[q]);
      for (int i = q; i < kk; ++i) {
        vd x = (i == q) ? zj : bc(s.zS[i - 1]);
        for (int t = 0; t < i; ++t) {
          vd lit = (i == q) ? L[q][t] : ((t < q) ? bc(Ls[i - 1][t]) : L[i][t]);
          vd wt = (t < q) ? bc(s.wH[t]) : w[t];
          x = _mm512_sub_pd(x, _mm512_mul_pd(lit, wt)); }
        w[i] = _mm512_div_pd(x, L[i][i]);
        quad = _mm512_add_pd(quad, _mm512_mul_pd(w[i], w[i])); }
    }
  }
  vd Q = _mm512_sub_pd(bc(D.yty), _mm512_mul_pd(bc((double)D.n), quad));
  if (_mm512_cmp_pd_mask(Q, bc(1e-8 * D.yty), _CMP_LT_OQ)) return false;
  vd ldH = _mm512_mul_pd(ld[0], bc(2.0)), ldA = _mm512_mul_pd(ld[1], bc(2.0));
  vd arg = _mm512_add_pd(bc(2 * D.b0), Q);
  vd la = FASTLOG ? _ZGVeN8v_log(arg) : vlog_scalar(arg);
  logm_out = _mm512_sub_pd(_mm512_sub_pd(bc(D.logCn), _mm512_mul_pd(bc(0.5), _mm512_sub_pd(ldH, ldA))), _mm512_mul_pd(bc(D.nu), la));
  return true;
}
// Class A: bordered update (label appended last), FMA and libmvec allowed. Same exact-arithmetic value.
static inline void flip8_A(const Data& D, const Support& s, const vd* u, vd gjj, vd zj, vd& logm_out) {
  const int k = s.k; const double n1 = D.n + 1.0;
  vd vH[KM], vA[KM]; vd dH = _mm512_fmadd_pd(bc(n1), gjj, bc(1.0)), dA = _mm512_add_pd(gjj, bc(1.0)); vd wz = zj;
  for (int c = 0; c < k; ++c) {
    vd x = _mm512_mul_pd(bc(n1), u[c]), y = u[c];
    for (int t = 0; t < c; ++t) { x = _mm512_fnmadd_pd(vH[t], bc(s.LH[c][t]), x); y = _mm512_fnmadd_pd(vA[t], bc(s.LA[c][t]), y); }
    vH[c] = _mm512_mul_pd(x, bc(1.0 / s.LH[c][c])); vA[c] = _mm512_mul_pd(y, bc(1.0 / s.LA[c][c]));
    dH = _mm512_fnmadd_pd(vH[c], vH[c], dH); dA = _mm512_fnmadd_pd(vA[c], vA[c], dA); wz = _mm512_fnmadd_pd(vH[c], bc(s.wH[c]), wz);
  }
  vd quad = _mm512_add_pd(bc(s.quad), _mm512_div_pd(_mm512_mul_pd(wz, wz), dH));
  vd Q = _mm512_fnmadd_pd(bc((double)D.n), quad, bc(D.yty));
  vd t1 = _ZGVeN8v_log(_mm512_div_pd(dH, dA)), t2 = _ZGVeN8v_log(_mm512_add_pd(bc(2 * D.b0), Q));
  logm_out = _mm512_sub_pd(bc(D.logCn - (s.ldH - s.ldA)), _mm512_fmadd_pd(bc(D.nu), t2, _mm512_mul_pd(bc(0.5), t1)));
}
// Gibbs inclusion odds o_j = plogis(lgphi(S u j) - lgphi(S)), comp summed in sorted order (singleton blocks stand-in).
template <bool FASTEXP>
static inline vd odds8(const Data& D, const Support& s, int q, vd logm, vd lr1, double phi) {
  vd c = _mm512_add_pd(bc(s.preC[q]), lr1);
  for (int a = q; a < s.k; ++a) c = _mm512_add_pd(c, bc(logr1[s.mem[a]]));
  vd lg0 = _mm512_add_pd(bc(D.logprior[s.k + 1]), c);
  vd d = _mm512_sub_pd(_mm512_sub_pd(logm, bc(D.logm0)), c);
  vd la = _mm512_sub_pd(_mm512_add_pd(lg0, _mm512_mul_pd(bc(phi), d)), bc(s.lgphi));
  __mmask8 pos = _mm512_cmp_pd_mask(la, bc(0.0), _CMP_GE_OQ);
  vd e = FASTEXP ? _ZGVeN8v_exp(_mm512_mask_sub_pd(la, pos, bc(0.0), la)) : vexp_scalar(_mm512_mask_sub_pd(la, pos, bc(0.0), la));
  vd o_neg = _mm512_div_pd(e, _mm512_add_pd(bc(1.0), e)), o_pos = _mm512_div_pd(bc(1.0), _mm512_add_pd(bc(1.0), e));
  return _mm512_mask_blend_pd(pos, o_neg, o_pos);
}
// Addressed uniform stand-in: SplitMix64 finaliser of (key, position); 53 bits. (A production build would use a
// reviewed counter-based generator; the cost is of the same order.)
static inline vd unif8(uint64_t key, __m512i pos) {
  __m512i z = _mm512_add_epi64(_mm512_set1_epi64((long long)key), _mm512_mullo_epi64(pos, _mm512_set1_epi64((long long)0x9E3779B97F4A7C15ULL)));
  z = _mm512_mullo_epi64(_mm512_xor_si512(z, _mm512_srli_epi64(z, 30)), _mm512_set1_epi64((long long)0xBF58476D1CE4E5B9ULL));
  z = _mm512_mullo_epi64(_mm512_xor_si512(z, _mm512_srli_epi64(z, 27)), _mm512_set1_epi64((long long)0x94D049BB133111EBULL));
  z = _mm512_xor_si512(z, _mm512_srli_epi64(z, 31));
  return _mm512_mul_pd(_mm512_cvtepu64_pd(_mm512_srli_epi64(z, 11)), bc(0x1.0p-53));
}

static void draw_order(Rng& r, std::vector<uint32_t>& ord, int m) {
  ord.resize(m); for (int i = 0; i < m; ++i) ord[i] = i;
  for (int i = m - 1; i >= 1; --i) { int jj = (int)std::floor(r.u() * (i + 1)); std::swap(ord[i], ord[jj]); }
}
#include <algorithm>
#include <ctime>
#include <string>

// ============================================================================================================
// G0 drivers (refactored from feas_bench.cpp main(); arithmetic unchanged)
// ============================================================================================================
static void stamp(const char* what) { time_t t = time(nullptr); char b[32]; strftime(b, sizeof b, "%H:%M:%S", localtime(&t)); printf("[%s] %s\n", b, what); fflush(stdout); }

static void run_bw(double* a, size_t len, int T, int reps) {
  double gb = len * 8.0 / 1e9, best = 1e99, sum = 0;
  for (int rep = 0; rep < reps; ++rep) { double t0 = now(); double s = 0;
    #pragma omp parallel for reduction(+:s) num_threads(T) schedule(static)
    for (size_t i = 0; i < len; ++i) s += a[i];
    best = std::min(best, now() - t0); sum += s; }
  printf("bw threads=%d GB=%.1f best_s=%.4f read_GBps=%.1f (check %.0f)\n", T, gb, best, gb / best, sum); fflush(stdout);
}

// every thread draws `reps` round orders of p + 16 labels and their inverses (the per-particle round cost under load)
static void run_perm(int p, int T, int reps) {
  double tf = 0, ti = 0; uint64_t chk = 0;
  #pragma omp parallel num_threads(T) reduction(+:tf,ti,chk)
  { Rng r; r.g.seed_stream(5, 5 + omp_get_thread_num()); std::vector<uint32_t> ord, inv(p + 16);
    double t0 = now(); for (int k = 0; k < reps; ++k) draw_order(r, ord, p + 16); double t1 = now();
    for (int k = 0; k < reps; ++k) for (int i = 0; i < p + 16; ++i) inv[ord[i]] = i; double t2 = now();
    tf += t1 - t0; ti += t2 - t1; chk += inv[7]; }
  printf("perm p=%d threads=%d reps=%d: fisher_yates %.2f ms (%.2f ns/label), inverse %.2f ms (%.2f ns/label) per thread [%llu]\n", p, T, reps,
         1e3 * tf / T / reps, 1e9 * tf / T / reps / p, 1e3 * ti / T / reps, 1e9 * ti / T / reps / p, (unsigned long long)chk); fflush(stdout);
}

static void run_direct(const Data& D, int p, int T, long steps, int kx, int nchecks) {
  const int n = D.n; const double phi = 1.0;
  double tot_s = 0; long tot_steps = 0; double chk = 0; long mism = 0, checked = 0; double t_order = 0;
  double wall0 = now();
  #pragma omp parallel num_threads(T) reduction(+:tot_s,tot_steps,chk,mism,checked,t_order)
  {
    int th = omp_get_thread_num(); Rng r; r.g.seed_stream(99, th);
    std::vector<int> S = truth; while ((int)S.size() < 5 + kx) { int j = (int)(r.u() * p); if (!std::binary_search(S.begin(), S.end(), j)) v3::sorted_insert(S, j); }
    Support s; build_support(D, s, S, phi); Scorer sc(&D);
    std::vector<uint32_t> ord; double ta = now(); draw_order(r, ord, p); t_order += now() - ta;
    const int k = s.k; double acc_chk = 0; long acc = 0;
    std::vector<int> chkj; std::vector<double> chkv;
    double tb = now();
    for (long st = 0; st < steps; ++st) {
      int j = ord[st % p];
      const double* xj = D.col(j);
      alignas(64) double u[KM] = {0, 0, 0, 0, 0, 0, 0, 0};
      const double* xs = s.XS.data();
      for (int i = 0; i < n; ++i) { double x = xj[i]; for (int a = 0; a < KM; ++a) u[a] += xs[(size_t)i * KM + a] * x; }
      int q = (int)(std::lower_bound(S.begin(), S.end(), j) - S.begin());
      if (q < k && S[q] == j) continue;
      double MH[KM + 1][KM + 1], MA[KM + 1][KM + 1]; const int kk = k + 1; const double n1 = n + 1.0;
      auto sidx = [q](int t) { return t < q ? t : t - 1; };
      double gjj = diagG[j];
      for (int a = 0; a < kk; ++a) for (int b = 0; b <= a; ++b) {
        double g; bool la = a == q, lb = b == q;
        if (la && lb) { MH[a][b] = n1 * gjj + 1.0; MA[a][b] = gjj + 1.0; continue; }
        if (la) g = u[sidx(b)]; else if (lb) g = u[sidx(a)]; else { MH[a][b] = s.MH[sidx(a)][sidx(b)]; MA[a][b] = s.MA[sidx(a)][sidx(b)]; continue; }
        MH[a][b] = n1 * g + 0.0; MA[a][b] = g + 0.0; }
      double ld2[2]; double w[KM + 1], quad = 0;
      for (int which = 0; which < 2; ++which) {
        double (*L)[KM + 1] = which == 0 ? MH : MA;
        for (int c = 0; c < kk; ++c) { double d = L[c][c]; for (int t = 0; t < c; ++t) d -= L[c][t] * L[c][t]; double l = std::sqrt(d); L[c][c] = l;
          for (int i = c + 1; i < kk; ++i) { double x = L[i][c]; for (int t = 0; t < c; ++t) x -= L[i][t] * L[c][t]; L[i][c] = x / l; } }
        double a2 = 0; for (int a = 0; a < kk; ++a) a2 += std::log(L[a][a]); ld2[which] = a2;
        if (which == 0) for (int i = 0; i < kk; ++i) { double x = (i == q) ? D.z[j] : s.zS[sidx(i)]; for (int t = 0; t < i; ++t) x -= L[i][t] * w[t]; w[i] = x / L[i][i]; quad += w[i] * w[i]; }
      }
      double Q = D.yty - n * quad; double ldH = 2 * ld2[0], ldA = 2 * ld2[1];
      double lm = D.logCn - 0.5 * (ldH - ldA) - D.nu * std::log(2 * D.b0 + Q);
      double c = s.preC[q] + logr1[j]; for (int a = q; a < k; ++a) c += logr1[S[a]];
      double lg0 = D.logprior[k + 1] + c, d = (lm - D.logm0) - c; double o = v3::plogis_log(lg0 + phi * d - s.lgphi);
      acc += (r.u() < o); acc_chk += lm;
      if (st < nchecks) { chkj.push_back(j); chkv.push_back(lm); }
    }
    tot_s += now() - tb;
    for (size_t c = 0; c < chkj.size(); ++c) { std::vector<int> Tm = S; v3::sorted_insert(Tm, chkj[c]); double ref = ref_logm(sc, Tm); ++checked; if (std::memcmp(&ref, &chkv[c], 8) != 0) ++mism; }
    tot_steps += steps; chk += acc_chk + acc;
  }
  double wall = now() - wall0;
  printf("direct p=%d threads=%d k=%d steps/thread=%ld: %.1f ns/step per thread (checks untimed); wall %.2f s; order draw %.1f ms/round; "
         "bit mismatches vs v3 scorer %ld of %ld [chk %.6f]\n", p, T, 5 + kx, steps, 1e9 * tot_s / tot_steps, wall, 1e3 * t_order / T, mism, checked, chk);
  fflush(stdout);
}

// Round orders (inverse permutations) of particle g, seeded as in feas_bench (31337, g), so that a shared precomputed set
// gives the same orders as feas_bench's per-run draw.
static void make_inv(int p, int G, int T, std::vector<std::vector<uint32_t>>& inv) {
  inv.assign(G, {});
  #pragma omp parallel for num_threads(T) schedule(dynamic, 1)
  for (int g = 0; g < G; ++g) { Rng rr; rr.g.seed_stream(31337, g); std::vector<uint32_t> ord; draw_order(rr, ord, p + 16); inv[g].resize(p + 16); for (int i = 0; i < p + 16; ++i) inv[g][ord[i]] = i; }
}

static const int NPASS = 8; static const double PASS_DELTA[NPASS] = {0, 5, 10, 12, 14, 16, 20, 30};

static void run_batch(const Data& D, int p, int T, int G, int kx, int div, int variant, int Bk, double frac, bool check,
                      const std::vector<std::vector<uint32_t>>* inv_pre, bool count_pass) {
  const int n = D.n; const double phi = 1.0;
  Rng r; r.g.seed_stream(4242, 1);
  std::vector<Support> sup(G); std::vector<std::vector<int>> Sg(G); std::vector<int> A;
  for (int g = 0; g < G; ++g) {
    std::vector<int> S = div ? std::vector<int>() : truth; int target = 5 + kx;
    while ((int)S.size() < target) { int j = (int)(r.u() * p); if (!std::binary_search(S.begin(), S.end(), j)) v3::sorted_insert(S, j); }
    Sg[g] = S; build_support(D, sup[g], S, phi); for (int j : S) A.push_back(j);
  }
  std::sort(A.begin(), A.end()); A.erase(std::unique(A.begin(), A.end()), A.end()); int nA = (int)A.size();
  for (int g = 0; g < G; ++g) for (int a = 0; a < sup[g].k; ++a) sup[g].arow[a] = (int)(std::lower_bound(A.begin(), A.end(), sup[g].mem[a]) - A.begin());
  std::vector<double> XA((size_t)nA * n); for (int a = 0; a < nA; ++a) std::memcpy(&XA[(size_t)a * n], D.col(A[a]), 8 * n);
  std::vector<std::vector<uint32_t>> inv_own; const std::vector<std::vector<uint32_t>>* inv = inv_pre;
  double tp = 0;
  if (!inv || (int)inv->size() < G) { tp = now(); make_inv(p, G, T, inv_own); tp = now() - tp; inv = &inv_own; }
  int ntile = (p + Bk - 1) / Bk; int tstep = std::max(1, (int)std::lround(1.0 / frac));
  double t_tr = 0, t_gemm = 0, t_post = 0; long nscore = 0, nacc = 0, nfallback = 0, mism = 0, checked = 0; double rbsum = 0; long labels_done = 0;
  long pass[NPASS] = {0, 0, 0, 0, 0, 0, 0, 0};
  double wall0 = now();
  #pragma omp parallel num_threads(T) reduction(+:t_tr,t_gemm,t_post,nscore,nacc,nfallback,mism,checked,rbsum,labels_done) reduction(+:pass[:NPASS])
  {
    Scorer sc(&D);
    double* Tt = (double*)aligned_alloc(64, (size_t)n * Bk * 8); double* P = (double*)aligned_alloc(64, (size_t)nA * Bk * 8);
    double* rb = (double*)aligned_alloc(64, (size_t)Bk * 8);
    #pragma omp for schedule(dynamic, 4)
    for (int ti = 0; ti < ntile; ti += tstep) {
      int j0 = ti * Bk, nb = std::min(Bk, p - j0); if (nb < Bk) continue;
      double ta = now();
      for (int jj = 0; jj < nb; ++jj) { const double* x = D.col(j0 + jj); for (int i = 0; i < n; ++i) Tt[(size_t)i * Bk + jj] = x[i]; }
      double tb = now();
      for (int a = 0; a < nA; ++a) {
        const double* xa = &XA[(size_t)a * n]; double* Pa = P + (size_t)a * Bk;
        for (int c0 = 0; c0 < nb; c0 += 64) {
          vd s0 = bc(0), s1 = bc(0), s2 = bc(0), s3 = bc(0), s4 = bc(0), s5 = bc(0), s6 = bc(0), s7 = bc(0);
          const double* tp0 = Tt + c0;
          for (int i = 0; i < n; ++i) { vd xi = bc(xa[i]); const double* row = tp0 + (size_t)i * Bk;
            s0 = _mm512_add_pd(s0, _mm512_mul_pd(xi, _mm512_load_pd(row)));      s1 = _mm512_add_pd(s1, _mm512_mul_pd(xi, _mm512_load_pd(row + 8)));
            s2 = _mm512_add_pd(s2, _mm512_mul_pd(xi, _mm512_load_pd(row + 16))); s3 = _mm512_add_pd(s3, _mm512_mul_pd(xi, _mm512_load_pd(row + 24)));
            s4 = _mm512_add_pd(s4, _mm512_mul_pd(xi, _mm512_load_pd(row + 32))); s5 = _mm512_add_pd(s5, _mm512_mul_pd(xi, _mm512_load_pd(row + 40)));
            s6 = _mm512_add_pd(s6, _mm512_mul_pd(xi, _mm512_load_pd(row + 48))); s7 = _mm512_add_pd(s7, _mm512_mul_pd(xi, _mm512_load_pd(row + 56))); }
          _mm512_store_pd(Pa + c0, s0); _mm512_store_pd(Pa + c0 + 8, s1); _mm512_store_pd(Pa + c0 + 16, s2); _mm512_store_pd(Pa + c0 + 24, s3);
          _mm512_store_pd(Pa + c0 + 32, s4); _mm512_store_pd(Pa + c0 + 40, s5); _mm512_store_pd(Pa + c0 + 48, s6); _mm512_store_pd(Pa + c0 + 56, s7);
        }
      }
      double tc = now();
      for (int jj = 0; jj < nb; ++jj) rb[jj] = 0;
      bool check_tile = check && (ti == 0 || ti == tstep * 7);
      for (int g = 0; g < G; ++g) {
        const Support& s = sup[g]; const int k = s.k; const uint32_t* ig = (*inv)[g].data() + j0;
        for (int v = 0; v < nb; v += 8) {
          int ja = j0 + v, jb = ja + 7;
          int qa = (int)(std::lower_bound(s.mem, s.mem + k, ja) - s.mem), qb = (int)(std::upper_bound(s.mem, s.mem + k, jb) - s.mem);
          vd logm; bool ok = (qa == qb);
          vd u[KM]; if (ok) { for (int a = 0; a < k; ++a) u[a] = _mm512_load_pd(P + (size_t)s.arow[a] * Bk + v);
            vd gjj = _mm512_loadu_pd(&diagG[ja]); vd zj = _mm512_loadu_pd(&D.z[ja]);
            if (variant == 0) ok = flip8_bit<false>(D, s, qa, u, gjj, zj, logm);
            else if (variant == 1) ok = flip8_bit<true>(D, s, qa, u, gjj, zj, logm);
            else flip8_A(D, s, u, gjj, zj, logm); }
          if (!ok) {
            ++nfallback; alignas(64) double lm[8];
            for (int l = 0; l < 8; ++l) { int j = ja + l; std::vector<int> Tm = Sg[g]; if (std::binary_search(Tm.begin(), Tm.end(), j)) { lm[l] = s.logm; continue; } v3::sorted_insert(Tm, j); lm[l] = ref_logm(sc, Tm); }
            logm = _mm512_load_pd(lm); qa = 0;
          }
          vd o = (variant == 0) ? odds8<false>(D, s, qa, logm, _mm512_loadu_pd(&logr1[ja]), phi) : odds8<true>(D, s, qa, logm, _mm512_loadu_pd(&logr1[ja]), phi);
          __m512i pos = _mm512_cvtepu32_epi64(_mm256_loadu_si256((const __m256i*)(ig + v)));
          vd uu = unif8(0xABCDEF12345ULL * (g + 1), pos);
          nacc += __builtin_popcount(_mm512_cmp_pd_mask(uu, o, _CMP_LT_OQ));
          _mm512_store_pd(rb + v, _mm512_add_pd(_mm512_load_pd(rb + v), o));
          if (count_pass) {   // la = F(S u j) - F(S) at phi = 1 (the comp terms cancel); untimed diagnostic run only
            vd la = _mm512_sub_pd(_mm512_add_pd(bc(D.logprior[s.k + 1]), _mm512_sub_pd(logm, bc(D.logm0))), bc(s.lgphi));
            for (int t = 0; t < NPASS; ++t) pass[t] += __builtin_popcount(_mm512_cmp_pd_mask(la, bc(-PASS_DELTA[t]), _CMP_GE_OQ));
          }
          if (check_tile && ok && g < 16) { alignas(64) double lm[8]; _mm512_store_pd(lm, logm);
            for (int l = 0; l < 8; ++l) { std::vector<int> Tm = Sg[g]; v3::sorted_insert(Tm, ja + l); double ref = ref_logm(sc, Tm); ++checked;
              if (variant == 0 ? std::memcmp(&ref, &lm[l], 8) != 0 : std::fabs(ref - lm[l]) > 1e-9 * std::fabs(ref)) ++mism; } }
        }
        nscore += nb;
      }
      for (int jj = 0; jj < nb; ++jj) rbsum += rb[jj];
      double td = now(); t_tr += tb - ta; t_gemm += tc - tb; t_post += td - tc; labels_done += nb;
    }
    free(Tt); free(P); free(rb);
  }
  double wall = now() - wall0;
  printf("batch p=%d threads=%d G=%d k=%d div=%d variant=%d Bk=%d frac=%.3f |A|=%d labels=%ld\n", p, T, G, 5 + kx, div, variant, Bk, frac, nA, labels_done);
  printf("  thread-seconds: transpose %.2f, products %.2f (%.3f ns per madd; %.1f ns per label per active column), post %.2f (%.1f ns per score)\n",
         t_tr, t_gemm, 1e9 * t_gemm / ((double)labels_done * nA * n), 1e9 * t_gemm / ((double)labels_done * nA), t_post, 1e9 * t_post / nscore);
  printf("  total %.1f ns per (support,label) thread-time; wall %.3f s; WALL-BASED %.1f ns per score x T (= wall*T/scores); round orders %s\n",
         1e9 * (t_tr + t_gemm + t_post) / nscore, wall, 1e9 * wall * T / nscore, tp > 0 ? "drawn in this run" : "precomputed (untimed)");
  printf("  accepts %ld (%.3g per score), scalar fallbacks %ld vectors of %ld, check mismatches %ld of %ld (variant 0: exact bits vs v3 scorer; 1,2: rel 1e-9) [rb %.6f]\n",
         nacc, (double)nacc / nscore, nfallback, nscore / 8, mism, checked, rbsum);
  if (count_pass) { printf("  PASS fractions (share of scores with F(S u j) - F(S) >= -Delta):");
    for (int i = 0; i < NPASS; ++i) printf(" Delta=%g: %.4g", PASS_DELTA[i], (double)pass[i] / nscore); printf("\n"); }
  fflush(stdout);
}

// ------------------------------------------------------------------------------------------------------------
// Bounded top-c store ("offer" mode). Design (documented for G0):
//  * strict total order = the HPM order of v3_ledger.h TopCmp(hpm_order = true): larger F first; exact F ties -> smaller
//    size, then lexicographic. Content = top-c of everything offered, independent of offer order (spec Store row).
//  * flat arrays per slot: F (double), 64-bit Zobrist hash, size, members (fixed 8 ints; k <= 8 in this benchmark;
//    the production store uses an integer pool, which costs about the same per entry);
//  * a binary MIN-heap of slot indices under that order (the root = the worst kept model): quick reject = one compare
//    of F with the root's F (exact ties fall through to the full compare);
//  * duplicates: open-addressing hash table (linear probing, 2^ceil(log2(1.6 c)) slots, backward-shift deletion) of
//    (hash, slot); a hit is confirmed by comparing size and members. Duplicates are looked up only after the quick reject.
//  * insert when full: erase the root's table entry, overwrite the root's slot, sift down; when not full: append, sift up.
// Offer kinds timed separately (unit costs; any mix is their weighted sum) and in two mixes:
//  REJECT (below the root), DUP-RANDOM (a random kept model again: cold hash probe + member compare), DUP-HOT (one of
//  10^4 kept models again), NEW (a new model above the root: probe miss + replace root + sift down + table insert),
//  FILL (inserts while not full, the last 2^20 of the fill).
// ------------------------------------------------------------------------------------------------------------
struct Offer { double F; uint64_t h; int32_t m[8]; uint8_t len; };
struct FlatStore {
  size_t cap = 0, size = 0; std::vector<double> F; std::vector<uint64_t> H; std::vector<uint8_t> L; std::vector<int32_t> M;
  std::vector<uint32_t> heap; std::vector<uint64_t> th; std::vector<uint32_t> ts; uint64_t tmask = 0;
  void init(size_t c) { cap = c; size = 0; F.resize(c); H.resize(c); L.resize(c); M.resize(c * 8); heap.resize(c);
    size_t t = 1; while ((double)t < 1.6 * c) t <<= 1; th.assign(t, 0); ts.assign(t, 0); tmask = t - 1; }
  // better(a, b): a precedes b in the store order
  inline bool better_off(const Offer& o, uint32_t s) const {
    if (o.F != F[s]) return o.F > F[s];
    if (o.len != L[s]) return o.len < L[s];
    const int32_t* m = &M[(size_t)s * 8]; for (int i = 0; i < o.len; ++i) if (o.m[i] != m[i]) return o.m[i] < m[i];
    return false; }
  inline bool better_ss(uint32_t a, uint32_t b) const {
    if (F[a] != F[b]) return F[a] > F[b];
    if (L[a] != L[b]) return L[a] < L[b];
    const int32_t* ma = &M[(size_t)a * 8]; const int32_t* mb = &M[(size_t)b * 8]; for (int i = 0; i < L[a]; ++i) if (ma[i] != mb[i]) return ma[i] < mb[i];
    return false; }
  inline bool same(const Offer& o, uint32_t s) const {
    if (o.len != L[s]) return false; const int32_t* m = &M[(size_t)s * 8]; for (int i = 0; i < o.len; ++i) if (o.m[i] != m[i]) return false; return true; }
  inline bool find(const Offer& o) const {
    uint64_t hk = o.h ? o.h : 1; uint64_t i = (hk * 0x9E3779B97F4A7C15ULL) >> 7 & tmask;
    while (th[i]) { if (th[i] == hk && same(o, ts[i])) return true; i = (i + 1) & tmask; } return false; }
  inline void tins(uint64_t h, uint32_t s) { uint64_t hk = h ? h : 1; uint64_t i = (hk * 0x9E3779B97F4A7C15ULL) >> 7 & tmask;
    while (th[i]) i = (i + 1) & tmask; th[i] = hk; ts[i] = s; }
  inline void terase(uint64_t h, uint32_t s) { uint64_t hk = h ? h : 1; uint64_t i = (hk * 0x9E3779B97F4A7C15ULL) >> 7 & tmask;
    while (!(th[i] == hk && ts[i] == s)) i = (i + 1) & tmask;
    uint64_t j = i;   // backward-shift deletion
    while (true) { j = (j + 1) & tmask; if (!th[j]) break; uint64_t home = (th[j] * 0x9E3779B97F4A7C15ULL) >> 7 & tmask;
      bool move = (i <= j) ? (home <= i || home > j) : (home <= i && home > j);
      if (move) { th[i] = th[j]; ts[i] = ts[j]; i = j; } }
    th[i] = 0; }
  inline void write(uint32_t s, const Offer& o) { F[s] = o.F; H[s] = o.h; L[s] = o.len; std::memcpy(&M[(size_t)s * 8], o.m, 32); }
  // min-heap under "worse first": parent is worse than (or equal to) children
  inline void sift_up(size_t i) { uint32_t x = heap[i]; while (i > 0) { size_t pa = (i - 1) >> 1; if (!better_ss(heap[pa], x)) break; heap[i] = heap[pa]; i = pa; } heap[i] = x; }
  inline void sift_down(size_t i) { uint32_t x = heap[i]; while (true) { size_t c = 2 * i + 1; if (c >= size) break;
      if (c + 1 < size && better_ss(heap[c], heap[c + 1])) ++c; if (!better_ss(x, heap[c])) break; heap[i] = heap[c]; i = c; } heap[i] = x; }
  // returns 0 reject, 1 duplicate, 2 inserted
  inline int offer(const Offer& o) {
    if (size == cap) { if (!better_off(o, heap[0])) return 0; }
    if (find(o)) return 1;
    if (size < cap) { uint32_t s = (uint32_t)size; write(s, o); heap[size] = s; ++size; sift_up(size - 1); tins(o.h, s); return 2; }
    uint32_t s = heap[0]; terase(H[s], s); write(s, o); sift_down(0); tins(o.h, s); return 2;
  }
};
static inline uint64_t zkey(int j) { uint64_t z = (uint64_t)j + 0x9E3779B97F4A7C15ULL; z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static void rand_model(Rng& r, int p, Offer& o) {
  int k = 6; o.len = (uint8_t)k; int c = 0;
  while (c < k) { int j = (int)(r.u() * p); bool dup = false; for (int i = 0; i < c; ++i) if (o.m[i] == j) dup = true; if (!dup) o.m[c++] = j; }
  std::sort(o.m, o.m + k); for (int i = k; i < 8; ++i) o.m[i] = 0; o.h = 0; for (int i = 0; i < k; ++i) o.h ^= zkey(o.m[i]); }

struct OfferTimes { double fill = 0, rej = 0, dupr = 0, duph = 0, nw = 0, mix1 = 0, mix2 = 0; long chk = 0; };
// One store of capacity c per thread: F of the initial content ~ U(0,1); NEW offers F ~ U(0.5,1.5) (stay above the root
// for the whole test: at most 2^18 inserts << c/2 entries below 0.5); REJECT offers F ~ U(-2,-1).
static void offer_one(size_t c, int p, uint64_t seed, int T, OfferTimes& out) {
  FlatStore st; st.init(c); Rng r; r.g.seed_stream(777777, seed);
  // per-thread sample sizes shrink with T (buffers stay small); NEW inserts <= c/8 keep the root below 0.5
  const size_t NF = std::min<size_t>(c / 2, (size_t)1 << 20), NR = std::max<size_t>((size_t)1 << 16, ((size_t)1 << 22) / T),
               ND = std::max<size_t>((size_t)1 << 14, ((size_t)1 << 20) / T), NN = std::min<size_t>(c / 8, ((size_t)1 << 18)), NM = NR;
  Offer o; long chk = 0;
  for (size_t i = 0; i < c - NF; ++i) { rand_model(r, p, o); o.F = r.u(); chk += st.offer(o); }   // untimed bulk of the fill
  std::vector<Offer> buf(std::max(NR, NM));
  for (size_t i = 0; i < NF; ++i) { rand_model(r, p, buf[i]); buf[i].F = r.u(); }
  double t0 = now(); for (size_t i = 0; i < NF; ++i) chk += st.offer(buf[i]); out.fill = (now() - t0) / NF;
  while (st.size < st.cap) { rand_model(r, p, o); o.F = r.u(); chk += st.offer(o); }   // (a rare duplicate in the fill)
  for (size_t i = 0; i < NR; ++i) { rand_model(r, p, buf[i]); buf[i].F = -1.0 - r.u(); }
  t0 = now(); for (size_t i = 0; i < NR; ++i) chk += st.offer(buf[i]); out.rej = (now() - t0) / NR;
  auto kept = [&](size_t s, Offer& q) { q.F = st.F[s]; q.h = st.H[s]; q.len = st.L[s]; std::memcpy(q.m, &st.M[s * 8], 32); };
  for (size_t i = 0; i < ND; ++i) kept((size_t)(r.u() * c) % c, buf[i]);
  t0 = now(); for (size_t i = 0; i < ND; ++i) chk += st.offer(buf[i]); out.dupr = (now() - t0) / ND;
  std::vector<size_t> hot(10000); for (auto& h : hot) h = (size_t)(r.u() * c) % c;
  for (size_t i = 0; i < ND; ++i) kept(hot[(size_t)(r.u() * hot.size()) % hot.size()], buf[i]);
  t0 = now(); for (size_t i = 0; i < ND; ++i) chk += st.offer(buf[i]); out.duph = (now() - t0) / ND;
  for (size_t i = 0; i < NN; ++i) { rand_model(r, p, buf[i]); buf[i].F = 0.5 + r.u(); }
  t0 = now(); for (size_t i = 0; i < NN; ++i) chk += st.offer(buf[i]); out.nw = (now() - t0) / NN;
  // mixes: pass fraction pi (rest rejected); of the passes, a share is new (1e-3 of offers at most), the rest DUP-RANDOM
  auto mix = [&](double pi, double newshare) {
    for (size_t i = 0; i < NM; ++i) { double u = r.u();
      if (u >= pi) { rand_model(r, p, buf[i]); buf[i].F = -1.0 - r.u(); }
      else if (r.u() < newshare) { rand_model(r, p, buf[i]); buf[i].F = 0.5 + r.u(); }
      else kept((size_t)(r.u() * c) % c, buf[i]); }
    double ta = now(); for (size_t i = 0; i < NM; ++i) chk += st.offer(buf[i]); return (now() - ta) / NM; };
  out.mix1 = mix(0.01, 0.01); out.mix2 = mix(0.10, 0.001);
  out.chk = chk;
}
static void run_offer(size_t cap, int T, int p) {
  size_t c = cap / T; std::vector<OfferTimes> R(T); double w0 = now();
  #pragma omp parallel num_threads(T)
  { int th = omp_get_thread_num(); offer_one(c, p, 1000 + th, T, R[th]); }
  OfferTimes a; for (auto& x : R) { a.fill += x.fill / T; a.rej += x.rej / T; a.dupr += x.dupr / T; a.duph += x.duph / T; a.nw += x.nw / T; a.mix1 += x.mix1 / T; a.mix2 += x.mix2 / T; a.chk += x.chk; }
  size_t tsz = 1; while ((double)tsz < 1.6 * c) tsz <<= 1;
  double mb = T * (c * (8 + 8 + 1 + 32 + 4) + tsz * 12.0) / 1e6;
  printf("offer cap=%zu threads=%d (one store of c=%zu per thread; %.0f MB in all) wall %.1f s; ns per offer per thread:\n", cap, T, c, mb, now() - w0);
  printf("  FILL %.1f | REJECT %.2f | DUP-RANDOM %.1f | DUP-HOT %.1f | NEW %.1f | MIX(pi=0.01,new 1%% of passes) %.2f | MIX(pi=0.10,new 0.1%%) %.2f [chk %ld]\n",
         1e9 * a.fill, 1e9 * a.rej, 1e9 * a.dupr, 1e9 * a.duph, 1e9 * a.nw, 1e9 * a.mix1, 1e9 * a.mix2, a.chk);
  fflush(stdout);
}

// store self-test: small c, offers with many duplicates and exact F ties; content must equal the brute-force top-c
static int store_test() {
  int bad = 0;
  for (int trial = 0; trial < 20; ++trial) {
    size_t c = 50 + 37 * trial; FlatStore st; st.init(c); Rng r; r.g.seed_stream(4321, trial);
    std::vector<Offer> pool(3 * c); for (auto& o : pool) { rand_model(r, 40, o); o.F = std::floor(r.u() * 8); }   // p = 40: ties in F, sizes equal
    std::vector<Offer> all;
    for (int i = 0; i < 20 * (int)c; ++i) { const Offer& o = pool[(size_t)(r.u() * pool.size()) % pool.size()]; st.offer(o); all.push_back(o); }
    auto bt = [](const Offer& a, const Offer& b) { if (a.F != b.F) return a.F > b.F; if (a.len != b.len) return a.len < b.len;
      for (int i = 0; i < a.len; ++i) if (a.m[i] != b.m[i]) return a.m[i] < b.m[i]; return false; };
    std::sort(all.begin(), all.end(), bt);
    std::vector<Offer> uniq; for (auto& o : all) if (uniq.empty() || bt(uniq.back(), o)) uniq.push_back(o);
    if (uniq.size() > c) uniq.resize(c);
    std::vector<Offer> got(st.size); for (size_t s = 0; s < st.size; ++s) { got[s].F = st.F[s]; got[s].len = st.L[s]; std::memcpy(got[s].m, &st.M[s * 8], 32); got[s].h = st.H[s]; }
    std::sort(got.begin(), got.end(), bt);
    bool ok = got.size() == uniq.size();
    for (size_t i = 0; ok && i < got.size(); ++i) if (bt(got[i], uniq[i]) || bt(uniq[i], got[i])) ok = false;
    for (size_t i = 1; ok && i < st.size; ++i) if (st.better_ss(st.heap[(i - 1) / 2], st.heap[i])) ok = false;     // heap order
    size_t occ = 0; for (auto h : st.th) occ += h != 0; if (occ != st.size) ok = false;                              // table size
    for (size_t s = 0; ok && s < st.size; ++s) { Offer q = got[0]; q.F = st.F[s]; q.h = st.H[s]; q.len = st.L[s]; std::memcpy(q.m, &st.M[s * 8], 32); if (!st.find(q)) ok = false; }
    if (!ok) ++bad;
  }
  printf("storetest: %d of 20 trials failed (content vs brute-force top-c, heap order, hash table)\n", bad);
  return bad;
}

static std::vector<int> parse_list(const char* s) { std::vector<int> v; const char* q = s; while (*q) { v.push_back(atoi(q)); while (*q && *q != ',') ++q; if (*q) ++q; } return v; }

int main(int argc, char** argv) {
  if (argc < 2) return 1;
  std::string mode = argv[1];
  const int n = 200;
  if (mode == "bw") {
    double gb = atof(argv[2]); int T = atoi(argv[3]); size_t len = (size_t)(gb * 1e9 / 8);
    std::vector<double> a(len);
    #pragma omp parallel for num_threads(T)
    for (size_t i = 0; i < len; ++i) a[i] = 1.0;
    run_bw(a.data(), len, T, 5); return 0;
  }
  if (mode == "perm") { run_perm(atoi(argv[2]), argc > 4 ? atoi(argv[4]) : 1, atoi(argv[3])); return 0; }
  if (mode == "storetest") return store_test() ? 1 : 0;
  if (mode == "offer") { run_offer((size_t)atof(argv[2]), atoi(argv[3]), argc > 4 ? atoi(argv[4]) : 1000000); return 0; }
  if (mode == "suite") {
    int p = atoi(argv[2]); std::vector<int> Ts = parse_list(argv[3]);
    long dsteps = argc > 4 ? atol(argv[4]) : 200000; double frac1 = argc > 5 ? atof(argv[5]) : 0.05;
    size_t ocap = argc > 6 ? (size_t)atof(argv[6]) : 40000000; double bwgb = argc > 7 ? atof(argv[7]) : 4.0;
    int Tmax = *std::max_element(Ts.begin(), Ts.end());
    printf("suite p=%d T={%s} direct_steps=%ld frac1=%.3f offer_cap=%zu bw_GB=%.1f omp_max_threads=%d\n", p, argv[3], dsteps, frac1, ocap, bwgb, omp_get_max_threads());
    stamp("start");
    if (store_test()) printf("STORE SELF-TEST FAILED\n");
    Data D; double t0 = now(); make_data(D, n, p, Tmax);
    printf("data n=%d p=%d gen+z+logr1 %.1f s with %d threads; logm0=%.4f\n", n, p, now() - t0, Tmax, D.logm0);
    std::vector<std::vector<uint32_t>> inv; t0 = now(); make_inv(p, 256, Tmax, inv);
    printf("round orders: 256 particles x (p+16) labels in %.2f s with %d threads (untimed setup)\n", now() - t0, Tmax);
    size_t len = (size_t)(bwgb * 1e9 / 8); std::vector<double> a(len);
    #pragma omp parallel for num_threads(Tmax)
    for (size_t i = 0; i < len; ++i) a[i] = 1.0;
    stamp("setup done");
    for (int T : Ts) {
      double frac = std::min(1.0, frac1 * T); bool chk = (T == 1);
      printf("==== T = %d (frac = %.3f; bit checks %s) ====\n", T, frac, chk ? "ON" : "off"); fflush(stdout);
      run_batch(D, p, T, 256, 0, 1, 2, 128, frac, chk, &inv, false);
      run_batch(D, p, T, 64, 0, 0, 2, 128, frac, chk, &inv, false);
      run_batch(D, p, T, 256, 0, 1, 0, 128, frac, chk, &inv, false);
      run_batch(D, p, T, 64, 0, 0, 0, 128, frac, chk, &inv, false);
      run_direct(D, p, T, chk ? dsteps / 2 : dsteps, 1, chk ? 2000 : 0);
      run_perm(p, T, 3);
      run_bw(a.data(), len, T, 3);
      stamp("T done");
    }
    std::vector<double>().swap(a);
    printf("==== pass fractions (untimed; class A; T = %d) ====\n", Tmax); fflush(stdout);
    run_batch(D, p, Tmax, 256, 0, 1, 2, 128, std::min(1.0, frac1 * Tmax), false, &inv, true);
    run_batch(D, p, Tmax, 64, 0, 0, 2, 128, std::min(1.0, frac1 * Tmax), false, &inv, true);
    run_batch(D, p, Tmax, 256, 1, 0, 2, 128, std::min(1.0, frac1 * Tmax), false, &inv, true);   // S0 + 1 null
    stamp("pass done");
    { std::vector<std::vector<uint32_t>>().swap(inv); }
    printf("==== store offers ====\n"); fflush(stdout);
    run_offer(ocap, 1, p); stamp("offer T=1 done");
    for (int T : Ts) if (T > 1) { run_offer(ocap, T, p); stamp("offer done"); }
    stamp("suite done");
    return 0;
  }
  int p = atoi(argv[2]), T = atoi(argv[3]);
  Data D; double t0 = now(); make_data(D, n, p, T);
  printf("data n=%d p=%d gen+z+logr1 %.1f s; logm0=%.4f\n", n, p, now() - t0, D.logm0);
  if (mode == "direct") { run_direct(D, p, T, atol(argv[4]), atoi(argv[5]), argc > 6 ? atoi(argv[6]) : 2000); return 0; }
  if (mode == "batch") {
    run_batch(D, p, T, atoi(argv[4]), atoi(argv[5]), atoi(argv[6]), atoi(argv[7]), atoi(argv[8]), argc > 9 ? atof(argv[9]) : 1.0,
              argc > 10 ? atoi(argv[10]) != 0 : getenv("CHECK") != nullptr, nullptr, false);
    return 0;
  }
  return 1;
}
