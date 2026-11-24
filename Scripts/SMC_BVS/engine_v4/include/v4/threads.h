// threads.h -- threading conventions (INTERFACES §7): OpenMP, fixed chunks independent of the thread count, chunk
// partials combined serially in chunk order. Helpers used by every WP.
#pragma once
#include <cstddef>
#include <cstdint>
#include <vector>
#include <omp.h>

namespace v4 {
constexpr size_t DEFAULT_CHUNK = 64;
inline int threads_available() { return omp_get_max_threads(); }
inline void set_threads(int k) { if (k > 0) omp_set_num_threads(k); }
// Deterministic sum of f(i), i in [0, n): per-chunk sequential partials (in i order), then chunk partials added in
// chunk order. The result does not depend on the thread count or schedule.
template <class F> double chunked_sum(size_t n, F f, size_t chunk = DEFAULT_CHUNK) {
  size_t nc = (n + chunk - 1) / chunk;
  std::vector<double> part(nc, 0.0);
#pragma omp parallel for schedule(dynamic, 1)
  for (long c = 0; c < (long)nc; ++c) {
    double s = 0; size_t a = (size_t)c * chunk, b = a + chunk < n ? a + chunk : n;
    for (size_t i = a; i < b; ++i) s += f(i);
    part[(size_t)c] = s;
  }
  double s = 0; for (double x : part) s += x;
  return s;
}
}  // namespace v4
