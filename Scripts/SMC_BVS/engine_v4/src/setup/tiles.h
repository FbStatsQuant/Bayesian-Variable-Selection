// tiles.h -- streamed Gram tiles (internal to src/setup). Every entry G_jl (j < l) is the sequential sum
// s = 0; s += x_ij * x_il, i = 0..n-1, in double with no FMA: the bits of core/cpp/v3_score.h:45-53 (products commute
// exactly, and each SIMD lane carries one pair, so the vector width never changes a sum). Lanes run over pairs: the
// column tile J is copied to row-major so that the inner loop over its columns is contiguous.
// Work unit = one column tile J (copied once), against every tile I <= J. Units are handed out dynamically; the
// consumers (per-thread top-B lists, edge lists, a dense matrix) are order-free, so no result depends on the thread
// count or the schedule (INTERFACES §7 rule 1).
#pragma once
#include <emmintrin.h>
#include <omp.h>
#include <atomic>
#include <vector>
#include "v4/data.h"

namespace v4::setup::detail {

// sink(tid, j, l0, cnt, G): G[t] = G_{j, l0 + t} for t < cnt, all with l0 + t > j.
// jtiles (benchmarks only): restrict the pass to these column tiles J (each still against every I <= J).
template <class Sink>
void tile_pass(const Data& D, int tile, int threads, Sink&& sink, const std::vector<int>* jtiles = nullptr) {
  const int n = D.n, p = D.p;
  if (p < 2) return;
  const int TW = tile;
  const int nt = (p + TW - 1) / TW;
  std::atomic<int> next{0};
#pragma omp parallel num_threads(threads)
  {
    const int tid = omp_get_thread_num();
    std::vector<double> RJ((size_t)n * TW);
    std::vector<double> acc(4 * (size_t)TW);
    for (;;) {
      int u = next.fetch_add(1);
      if (u >= (jtiles ? (int)jtiles->size() : nt)) break;
      const int Jt = jtiles ? (*jtiles)[u] : nt - 1 - u;  // large tiles first (more work)
      const int l0 = Jt * TW, l1 = std::min(p, l0 + TW), w = l1 - l0;
      for (int t = 0; t < w; ++t) {
        const double* x = D.col(l0 + t);
        for (int i = 0; i < n; ++i) RJ[(size_t)i * TW + t] = x[i];
      }
      for (int It = 0; It <= Jt; ++It) {
        const int j0 = It * TW, j1 = std::min(p, j0 + TW);
        int j = j0;
        for (; j + 4 <= j1; j += 4) {
          double* a0 = acc.data(); double* a1 = a0 + TW; double* a2 = a1 + TW; double* a3 = a2 + TW;
          const double *x0 = D.col(j), *x1 = D.col(j + 1), *x2 = D.col(j + 2), *x3 = D.col(j + 3);
          int t = 0;
          // 4 x 4 register block, SSE2 (x86-64 baseline): lane (q, t) carries one pair's sum s = 0; s = s + x_iq * x_it,
          // i = 0..n-1; mul and add are separate instructions (no FMA), so each lane equals the scalar sum's bits.
          for (; t + 4 <= w; t += 4) {
            __m128d c00 = _mm_setzero_pd(), c01 = _mm_setzero_pd(), c10 = _mm_setzero_pd(), c11 = _mm_setzero_pd();
            __m128d c20 = _mm_setzero_pd(), c21 = _mm_setzero_pd(), c30 = _mm_setzero_pd(), c31 = _mm_setzero_pd();
            const double* r = &RJ[t];
            for (int i = 0; i < n; ++i, r += TW) {
              const __m128d r0 = _mm_loadu_pd(r), r1 = _mm_loadu_pd(r + 2);
              __m128d b = _mm_set1_pd(x0[i]);
              c00 = _mm_add_pd(c00, _mm_mul_pd(b, r0)); c01 = _mm_add_pd(c01, _mm_mul_pd(b, r1));
              b = _mm_set1_pd(x1[i]);
              c10 = _mm_add_pd(c10, _mm_mul_pd(b, r0)); c11 = _mm_add_pd(c11, _mm_mul_pd(b, r1));
              b = _mm_set1_pd(x2[i]);
              c20 = _mm_add_pd(c20, _mm_mul_pd(b, r0)); c21 = _mm_add_pd(c21, _mm_mul_pd(b, r1));
              b = _mm_set1_pd(x3[i]);
              c30 = _mm_add_pd(c30, _mm_mul_pd(b, r0)); c31 = _mm_add_pd(c31, _mm_mul_pd(b, r1));
            }
            _mm_storeu_pd(a0 + t, c00); _mm_storeu_pd(a0 + t + 2, c01); _mm_storeu_pd(a1 + t, c10); _mm_storeu_pd(a1 + t + 2, c11);
            _mm_storeu_pd(a2 + t, c20); _mm_storeu_pd(a2 + t + 2, c21); _mm_storeu_pd(a3 + t, c30); _mm_storeu_pd(a3 + t + 2, c31);
          }
          for (; t < w; ++t) {  // remainder columns: scalar, same operation order
            double s0 = 0, s1 = 0, s2 = 0, s3 = 0;
            for (int i = 0; i < n; ++i) { const double rt = RJ[(size_t)i * TW + t]; s0 += x0[i] * rt; s1 += x1[i] * rt; s2 += x2[i] * rt; s3 += x3[i] * rt; }
            a0[t] = s0; a1[t] = s1; a2[t] = s2; a3[t] = s3;
          }
          for (int q = 0; q < 4; ++q) {
            const int jj = j + q;
            const int start = (It == Jt) ? (jj - l0 + 1) : 0;  // only l > j
            if (start < w) sink(tid, jj, l0 + start, w - start, acc.data() + (size_t)q * TW + start);
          }
        }
        for (; j < j1; ++j) {
          double* a0 = acc.data();
          for (int t = 0; t < w; ++t) a0[t] = 0;
          const double* x0 = D.col(j);
          for (int i = 0; i < n; ++i) {
            const double* r = &RJ[(size_t)i * TW];
            const double b0 = x0[i];
            for (int t = 0; t < w; ++t) a0[t] += b0 * r[t];
          }
          const int start = (It == Jt) ? (j - l0 + 1) : 0;
          if (start < w) sink(tid, j, l0 + start, w - start, a0 + start);
        }
      }
    }
  }
}

}  // namespace v4::setup::detail
