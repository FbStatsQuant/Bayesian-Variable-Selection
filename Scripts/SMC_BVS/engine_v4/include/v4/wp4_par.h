// wp4_par.h -- fixed-chunk parallel loop used by WP4 (INTERFACES §7 thread rules 2-3): work is cut into chunks whose
// size does not depend on the thread count; each chunk writes only its own slot; the caller combines chunk results
// serially in chunk order. An exception thrown inside a chunk is captured and the one of the smallest chunk index is
// rethrown after the loop (so the reported failure does not depend on the schedule).
// Will be replaced by WP1's threads.h helpers when they land (same contract).
#pragma once
#include <cstddef>
#include <exception>
#include <vector>
#ifdef _OPENMP
#include <omp.h>
#endif

namespace v4 {

inline size_t n_chunks(size_t n, size_t chunk) { return chunk == 0 ? 0 : (n + chunk - 1) / chunk; }

// f(c, begin, end) for chunk c = [c*chunk, min(n, (c+1)*chunk)). threads <= 1 runs serially.
template <class F>
void for_chunks(size_t n, size_t chunk, int threads, F&& f) {
  const size_t nc = n_chunks(n, chunk);
  std::vector<std::exception_ptr> err(nc);
  if (threads <= 1 || nc <= 1) {
    for (size_t c = 0; c < nc; ++c) {
      try { f(c, c * chunk, std::min(n, (c + 1) * chunk)); } catch (...) { err[c] = std::current_exception(); break; }
    }
  } else {
#pragma omp parallel for schedule(dynamic, 1) num_threads(threads)
    for (long long c = 0; c < (long long)nc; ++c) {
      try { f((size_t)c, (size_t)c * chunk, std::min(n, ((size_t)c + 1) * chunk)); } catch (...) { err[(size_t)c] = std::current_exception(); }
    }
  }
  for (size_t c = 0; c < nc; ++c) if (err[c]) std::rethrow_exception(err[c]);
}

}  // namespace v4
