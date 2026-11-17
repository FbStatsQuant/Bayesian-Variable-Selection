// score.h -- the scorer, two arithmetic forms behind one interface (INTERFACES §6).
// Scorer<Arith::Bit> is the compat scorer: the arithmetic of core/cpp/v3_score.h:76-246 (Cholesky route, refactor,
// augmented QR, non-negative Q), Gram-free (entries by the sequential sum of core/cpp/v3_score.h:45-53). It returns
// the bits of v3::Scorer for every sorted model (golden test tests/test_score.cpp). Scorer<Arith::ClassA> is WP3's.
#pragma once
#include <vector>
#include "v4/data.h"
#include "v4/status.h"

namespace v4 {

enum Route : int8_t { ROUTE_CHOL = 0, ROUTE_REFACTOR = 1, ROUTE_QR = 2 };
inline const char* route_name(int r) { return r == 0 ? "chol" : (r == 1 ? "chol_refactor" : "qr"); }

struct ScoreOut {
  double logm = 0, Q = 0;
  double logdetH = 0, logdetA = 0;
  double cond_H = 1, cond_A = 1;
  int8_t route = 0;
  bool q_recomputed = false;
};
struct RouteCounters { uint64_t routes[3] = {0, 0, 0}; uint64_t q_recomputed = 0, numerical_failures = 0; };

enum class Arith { Bit, ClassA };

template <Arith A> class Scorer;

template <> class Scorer<Arith::Bit> {
 public:
  const Data* D;
  RouteCounters cnt;   // per-scorer (per-thread) counters; summed by the owner
  explicit Scorer(const Data* d) : D(d) {}
  // log m(S) for a sorted feasible S; throws NumericalFailure after the last fallback; |S| > K -> Error(internal_error).
  ScoreOut score(ModelView S);
  // Capacity only (no value changes): the Cholesky-route buffers for supports up to kmax, so that scoring such a support
  // inside a parallel region does not allocate (WP6 K2). The QR fallback (rare) still grows its buffers on demand.
  void reserve(int kmax);
  // Entry t = score(S (+) labels[t]) (symmetric difference). Infeasible (|S u j| > K): logm NaN, route -1.
  // Reference implementation: one full score per label (bits equal by construction). WP3 adds prefix reuse.
  void flip_scores(ModelView S, const int32_t* labels, size_t nl, double* logm_out, int8_t* route_out);
  double error_bound(const ScoreOut& o, int k) const;   // core/cpp/v3_score.h:242-246
  // Test hook: one route only (0 chol, 1 refactor, 2 QR), no fallback; returns false where the route fails.
  bool score_route(ModelView S, int route, ScoreOut& o) { return route == 2 ? try_qr(S, o) : try_chol(S, route == 1, o); }
  // Test hook: the non-negative Q of core/cpp/v3_score.h:147-160 after the Cholesky route (NaN if that route fails).
  double q_nonneg_after_chol(ModelView S) { ScoreOut o; return try_chol(S, false, o) ? q_nonneg(S, LH_) : NAN; }

 private:
  std::vector<double> Gs_, bufH_, bufA_, LH_, LA_, w_, beta_, tmp_, MH_, MA_, hv_;
  Model flip_;
  void gram_sub(ModelView S, bool from_X);
  bool try_chol(ModelView S, bool from_X, ScoreOut& o);
  bool try_qr(ModelView S, ScoreOut& o);
  void finish_from_factors(ModelView S, const std::vector<double>& LH, const std::vector<double>& LA, ScoreOut& o);
  double q_nonneg(ModelView S, const std::vector<double>& LH);
};
using BitScorer = Scorer<Arith::Bit>;

// Linear-algebra helpers, core/cpp/v3_score.h:76-137, copied (row-major lower triangle).
bool chol_inplace(std::vector<double>& A, int k);
void forward_solve(const std::vector<double>& L, int k, const double* b, double* w);
void backward_solve(const std::vector<double>& L, int k, const double* w, double* x);
bool householder_lower(std::vector<double>& M, int m, int k, std::vector<double>& L, std::vector<double>& v);

}  // namespace v4
