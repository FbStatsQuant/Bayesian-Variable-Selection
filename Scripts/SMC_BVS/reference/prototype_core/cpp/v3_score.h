// v3_score.h -- target posterior and scorer (CORE_SPEC v2 §2; M §5 and §6.13).
#pragma once
#include "v3_util.h"

namespace v3 {

// Standardised data and every constant of the target (M §5). Built once per context, read-only afterwards.
struct Data {
  int n = 0, p = 0, K = 0, W = 0;
  std::vector<double> X;     // n x p column-major, standardised (M §4.4)
  std::vector<double> y;     // standardised response
  std::vector<double> G;     // p x p Gram X^T X, column-major
  std::vector<double> z;     // X^T y
  double yty = 0, a0 = 0.01, b0 = 0.01, nu = 0, logCn = 0, logm0 = 0;
  std::vector<double> logw;      // log w(k), k = 0..K (BB(1,p): w(k) = 1/2 / C(2p-1, k))
  double logWK = 0;              // log W_K = log sum_{k<=K} C(p,k) w(k)
  std::vector<double> logprior;  // log varpi(k) = log w(k) - log W_K
  std::vector<int> orig;         // 1-based original column index of internal column j
  Zobrist zob;
  // Test hooks (A1, A3): force score routes to fail for models with |S| >= fail_min_size (never set in production).
  int fail_min_size = -1;
  bool fail_chol = false, fail_refactor = false, fail_qr = false;

  inline double Gat(int a, int b) const { return G[(size_t)b * p + a]; }
  inline const double* col(int j) const { return &X[(size_t)j * n]; }
};

enum Route { ROUTE_CHOL = 0, ROUTE_REFACTOR = 1, ROUTE_QR = 2 };
inline const char* route_name(int r) { return r == 0 ? "chol" : (r == 1 ? "chol_refactor" : "qr"); }

struct ScoreOut {
  double logm = 0, Q = 0;
  int route = 0;
  bool q_recomputed = false;  // Q replaced by the non-negative form (M §6.13)
  double logdetH = 0, logdetA = 0;
  double cond_H = 1, cond_A = 1;  // (max/min Cholesky diagonal)^2: cheap lower estimate of the condition numbers
};

// Build the Data object: G, z, constants. M §5: C_n, w(k), W_K; log w(k) via lgamma; log W_K by log-sum-exp.
inline void data_init(Data& D, const double* X, const double* y, int n, int p, const std::vector<int>& orig) {
  D.n = n; D.p = p; D.K = std::min(p, n / 2); D.W = nwords(p);
  D.X.assign(X, X + (size_t)n * p);
  D.y.assign(y, y + n);
  D.orig = orig;
  D.G.assign((size_t)p * p, 0.0);
  for (int a = 0; a < p; ++a) {
    const double* xa = D.col(a);
    for (int b = a; b < p; ++b) {
      const double* xb = D.col(b);
      double s = 0;
      for (int i = 0; i < n; ++i) s += xa[i] * xb[i];
      D.G[(size_t)b * p + a] = s; D.G[(size_t)a * p + b] = s;
    }
  }
  D.z.assign(p, 0.0);
  for (int a = 0; a < p; ++a) { const double* xa = D.col(a); double s = 0; for (int i = 0; i < n; ++i) s += xa[i] * D.y[i]; D.z[a] = s; }
  D.yty = 0; for (int i = 0; i < n; ++i) D.yty += D.y[i] * D.y[i];
  D.nu = D.a0 + n / 2.0;
  // log C_n = a0 log(2 b0) + lgamma(a0 + n/2) - (n/2) log(pi) - lgamma(a0)
  D.logCn = D.a0 * std::log(2 * D.b0) + std::lgamma(D.a0 + n / 2.0) - (n / 2.0) * std::log(M_PI) - std::lgamma(D.a0);
  D.logm0 = D.logCn - D.nu * std::log(2 * D.b0 + D.yty);
  D.logw.assign(D.K + 1, 0.0);
  std::vector<double> terms(D.K + 1);
  for (int k = 0; k <= D.K; ++k) {
    // log w(k) = log(1/2) - log C(2p-1, k)   (lgamma form; replaces the beta-function ratio)
    D.logw[k] = -M_LN2 - lchoose_d(2.0 * p - 1.0, k);
    terms[k] = lchoose_d((double)p, k) + D.logw[k];
  }
  D.logWK = log_sum_exp(terms);
  D.logprior.assign(D.K + 1, 0.0);
  for (int k = 0; k <= D.K; ++k) D.logprior[k] = D.logw[k] - D.logWK;
  D.zob.init(p);
}

// In-place Cholesky of a k x k symmetric matrix (row-major lower triangle used). Returns false on a non-positive
// or non-finite pivot. Plain textbook algorithm; deterministic operation order (bit-reproducible).
inline bool chol_inplace(std::vector<double>& A, int k) {
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
// Solve L w = b (forward) with L lower-triangular row-major.
inline void forward_solve(const std::vector<double>& L, int k, const double* b, double* w) {
  for (int i = 0; i < k; ++i) { double s = b[i]; for (int t = 0; t < i; ++t) s -= L[i * k + t] * w[t]; w[i] = s / L[i * k + i]; }
}
// Solve L^T x = w (backward).
inline void backward_solve(const std::vector<double>& L, int k, const double* w, double* x) {
  for (int i = k - 1; i >= 0; --i) { double s = w[i]; for (int t = i + 1; t < k; ++t) s -= L[t * k + i] * x[t]; x[i] = s / L[i * k + i]; }
}

// Householder QR of an m x k column-major matrix M; returns R (k x k, upper, row-major in Rout) as a lower
// triangular factor L = R^T (so that L L^T = M^T M) in the same row-major lower layout used by chol_inplace.
// Used only by the augmented-QR fallback (M §6.13): M^T M is formed implicitly, never squared.
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
      if (i == j) r = std::fabs(r);  // sign of a row of R is irrelevant for L L^T; make the diagonal positive
      L[j * k + i] = r;              // L = R^T
    }
  // fix signs of off-diagonals consistently: rows of R with negative diagonal are negated
  for (int i = 0; i < k; ++i) {
    if (M[(size_t)i * m + i] < 0) for (int j = i + 1; j < k; ++j) L[j * k + i] = -L[j * k + i];
  }
  for (int i = 0; i < k; ++i) if (!(L[i * k + i] > 0) || !std::isfinite(L[i * k + i])) return false;
  return true;
}

// The scorer: log m(S) exactly as M §5, numerics as M §6.13. Stateless apart from scratch buffers; a production
// scorer and the observer scorer are separate instances (R11).
class Scorer {
 public:
  const Data* D;
  std::vector<double> bufH, bufA, w, beta, tmp;
  explicit Scorer(const Data* d) : D(d) {}

  // Q by the non-negative form (M §6.13): Q = ||y - X_S b||^2 + (||X_S b||^2 + ||b||^2)/n, b = n H^{-1} z_S.
  // Replaces the subtraction y'y - n z'H^{-1}z when the latter falls below 1e-8 y'y (cancellation).
  double q_nonneg(const std::vector<int>& S, const std::vector<double>& LH) {
    int k = (int)S.size(), n = D->n;
    w.resize(k); beta.resize(k); tmp.resize(k);
    for (int a = 0; a < k; ++a) tmp[a] = n * D->z[S[a]];
    forward_solve(LH, k, tmp.data(), w.data());
    backward_solve(LH, k, w.data(), beta.data());
    double rss = 0, fit2 = 0, b2 = 0;
    for (int i = 0; i < n; ++i) {
      double f = 0; for (int a = 0; a < k; ++a) f += D->col(S[a])[i] * beta[a];
      double r = D->y[i] - f; rss += r * r; fit2 += f * f;
    }
    for (int a = 0; a < k; ++a) b2 += beta[a] * beta[a];
    return rss + (fit2 + b2) / n;
  }

  // Fill Gs (row-major k x k) from the stored Gram (route chol) or recomputed from X (route chol_refactor).
  void gram_sub(const std::vector<int>& S, bool from_X, std::vector<double>& Gs) {
    int k = (int)S.size(), n = D->n;
    Gs.assign((size_t)k * k, 0.0);
    for (int a = 0; a < k; ++a)
      for (int b = 0; b <= a; ++b) {
        double g;
        if (!from_X) g = D->Gat(S[a], S[b]);
        else { const double* xa = D->col(S[a]); const double* xb = D->col(S[b]); g = 0; for (int i = 0; i < n; ++i) g += xa[i] * xb[i]; }
        Gs[a * k + b] = g; Gs[b * k + a] = g;
      }
  }

  // Cholesky route: H = (n+1) G_S + I, A = G_S + I.
  bool try_chol(const std::vector<int>& S, bool from_X, ScoreOut& o, std::vector<double>& LH) {
    int k = (int)S.size(); double n1 = D->n + 1.0;
    std::vector<double> Gs; gram_sub(S, from_X, Gs);
    bufH.assign((size_t)k * k, 0.0); bufA.assign((size_t)k * k, 0.0);
    for (int a = 0; a < k; ++a) for (int b = 0; b < k; ++b) {
      bufH[a * k + b] = n1 * Gs[a * k + b] + (a == b ? 1.0 : 0.0);
      bufA[a * k + b] = Gs[a * k + b] + (a == b ? 1.0 : 0.0);
    }
    if (!chol_inplace(bufH, k) || !chol_inplace(bufA, k)) return false;
    LH = bufH;
    finish_from_factors(S, bufH, bufA, o);
    return std::isfinite(o.logm);
  }
  // Augmented QR route: H = M_H^T M_H with M_H = [sqrt(n+1) X_S; I_k], A = M_A^T M_A with M_A = [X_S; I_k].
  bool try_qr(const std::vector<int>& S, ScoreOut& o, std::vector<double>& LH) {
    int k = (int)S.size(), n = D->n, m = n + k;
    std::vector<double> MH((size_t)m * k, 0.0), MA((size_t)m * k, 0.0), LA;
    double s1 = std::sqrt(n + 1.0);
    for (int a = 0; a < k; ++a) {
      const double* xa = D->col(S[a]);
      for (int i = 0; i < n; ++i) { MH[(size_t)a * m + i] = s1 * xa[i]; MA[(size_t)a * m + i] = xa[i]; }
      MH[(size_t)a * m + n + a] = 1.0; MA[(size_t)a * m + n + a] = 1.0;
    }
    if (!householder_lower(MH, m, k, LH) || !householder_lower(MA, m, k, LA)) return false;
    finish_from_factors(S, LH, LA, o);
    return std::isfinite(o.logm);
  }
  // Common finish: log det from factor diagonals, Q by subtraction, recomputed by the non-negative form when small.
  void finish_from_factors(const std::vector<int>& S, const std::vector<double>& LH, const std::vector<double>& LA, ScoreOut& o) {
    int k = (int)S.size();
    double ldH = 0, ldA = 0, mxH = 0, mnH = POS_INF, mxA = 0, mnA = POS_INF;
    for (int a = 0; a < k; ++a) {
      double h = LH[a * k + a], g = LA[a * k + a];
      ldH += std::log(h); ldA += std::log(g);
      mxH = std::max(mxH, h); mnH = std::min(mnH, h); mxA = std::max(mxA, g); mnA = std::min(mnA, g);
    }
    ldH *= 2; ldA *= 2;  // log det = 2 sum log diag(L)
    w.resize(k); tmp.resize(k);
    for (int a = 0; a < k; ++a) tmp[a] = D->z[S[a]];
    forward_solve(LH, k, tmp.data(), w.data());
    double quad = 0; for (int a = 0; a < k; ++a) quad += w[a] * w[a];
    double Q = D->yty - D->n * quad;  // Q_S = y'y - n z' H^{-1} z
    o.q_recomputed = false;
    if (Q < 1e-8 * D->yty) { Q = q_nonneg(S, LH); o.q_recomputed = true; }
    o.Q = Q; o.logdetH = ldH; o.logdetA = ldA;
    o.cond_H = (mxH / mnH) * (mxH / mnH); o.cond_A = (mxA / mnA) * (mxA / mnA);
    double arg = 2 * D->b0 + Q;
    o.logm = (arg > 0) ? D->logCn - 0.5 * (ldH - ldA) - D->nu * std::log(arg) : NEG_INF;
  }

  // log m(S) for a sorted feasible model S (internal indices). Throws NumericalFailure after the last fallback.
  ScoreOut score(const std::vector<int>& S) {
    ScoreOut o;
    int k = (int)S.size();
    if (k > D->K) throw std::runtime_error("v3_score: |S| > K (infeasible model; callers never pass these, R1)");
    if (k == 0) { o.logm = D->logm0; o.Q = D->yty; o.route = ROUTE_CHOL; return o; }
    bool hook = (D->fail_min_size >= 0 && k >= D->fail_min_size);
    std::vector<double> LH;
    if (!(hook && D->fail_chol) && try_chol(S, false, o, LH)) { o.route = ROUTE_CHOL; return o; }
    if (!(hook && D->fail_refactor) && try_chol(S, true, o, LH)) { o.route = ROUTE_REFACTOR; return o; }
    if (!(hook && D->fail_qr) && try_qr(S, o, LH)) { o.route = ROUTE_QR; return o; }
    throw NumericalFailure("score failed after Cholesky, refactor and augmented QR for a model of size " + std::to_string(k));
  }

  // Numerical error bound of log m(S) used by R9 (documented heuristic, reported with every certificate):
  // eta(S) = 64 eps [ nu (y'y/Q)(1 + k cond_H) + k (cond_H + cond_A) + |log C_n| + nu |log(2 b0 + Q)| ].
  double error_bound(const ScoreOut& o, int k) const {
    const double eps = std::numeric_limits<double>::epsilon();
    return 64 * eps * (D->nu * (D->yty / o.Q) * (1 + k * o.cond_H) + k * (o.cond_H + o.cond_A) + std::fabs(D->logCn) +
                       D->nu * std::fabs(std::log(2 * D->b0 + o.Q)));
  }
};

// Score cache (CORE_SPEC §8.6 "Cache >= 500p entries"; M §6.3), keyed by the model's sorted member list.
// Open addressing with linear probing on the Zobrist hash; keys are stored once in a flat int pool, so an entry costs
// about 4|S| bytes plus a 29-byte slot, independent of p (a bitset key would cost p/8 bytes per entry, i.e. O(p^2)
// memory for 500p entries; code review D-1). When it holds `capacity` entries it is cleared entirely (deterministic
// "clear when full" eviction). The cache stores log m(S) only; a hit returns exactly the bits a fresh evaluation
// would return, because the scorer is a deterministic function of the sorted model.
class ScoreCache {
 public:
  size_t capacity = 0, nslots = 0, mask = 0, count = 0;
  uint64_t clears = 0, hits = 0, misses = 0, inserts = 0;
  std::vector<uint64_t> hashes, off;
  std::vector<uint32_t> len;
  std::vector<double> logm;
  std::vector<uint8_t> used;
  std::vector<int> pool;
  void init(int /*W (unused)*/, size_t cap) {
    capacity = std::max<size_t>(cap, 1);
    nslots = 16; while (nslots < 2 * capacity) nslots <<= 1;
    mask = nslots - 1;
    hashes.assign(nslots, 0); off.assign(nslots, 0); len.assign(nslots, 0); logm.assign(nslots, 0.0); used.assign(nslots, 0);
    pool.clear(); count = 0;
  }
  inline bool same(size_t s, const std::vector<int>& S) const {
    return len[s] == S.size() && std::equal(S.begin(), S.end(), pool.begin() + off[s]);
  }
  bool find(const std::vector<int>& S, uint64_t h, double& lm) {
    size_t s = h & mask;
    while (used[s]) {
      if (hashes[s] == h && same(s, S)) { lm = logm[s]; ++hits; return true; }
      s = (s + 1) & mask;
    }
    ++misses;
    return false;
  }
  void insert(const std::vector<int>& S, uint64_t h, double lm) {
    if (count >= capacity) { std::fill(used.begin(), used.end(), 0); pool.clear(); count = 0; ++clears; }
    size_t s = h & mask;
    while (used[s]) {
      if (hashes[s] == h && same(s, S)) return;
      s = (s + 1) & mask;
    }
    used[s] = 1; hashes[s] = h; logm[s] = lm; off[s] = pool.size(); len[s] = (uint32_t)S.size();
    pool.insert(pool.end(), S.begin(), S.end());
    ++count; ++inserts;
  }
};

}  // namespace v3
