// bench_store.cpp -- Store memory / time probe (review PR11 #1): Store(c, HPM), `offers` offers of k-models with
// improving values (every offer enters). Prints wall time, peak RSS and bytes per kept entry.
// Usage: v4_bench_store [c=4000001] [offers=16000000] [k=7]
#include <sys/resource.h>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include "v4/store.h"
using namespace v4;
int main(int argc, char** argv) {
  uint64_t c = argc > 1 ? std::strtoull(argv[1], nullptr, 10) : 4000001, n = argc > 2 ? std::strtoull(argv[2], nullptr, 10) : 16000000;
  int k = argc > 3 ? std::atoi(argv[3]) : 7;
  Store s(c, Order::HPM); Model S(k);
  auto t0 = std::chrono::steady_clock::now();
  for (uint64_t i = 0; i < n; ++i) {
    for (int a = 0; a < k; ++a) S[a] = (int32_t)(i * 7 + a);   // distinct sorted models
    s.offer((double)i, S, i * 0x9E3779B97F4A7C15ULL);
  }
  s.compact();
  double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  struct rusage ru; getrusage(RUSAGE_SELF, &ru);
  std::printf("{\"cap\":%llu,\"offers\":%llu,\"k\":%d,\"kept\":%zu,\"seconds\":%.2f,\"peak_rss_MB\":%.1f,\"peak_bytes_per_cap_entry\":%.1f,\"final_reserved_bytes_per_entry\":%.1f,\"invariants\":%s}\n",
              (unsigned long long)c, (unsigned long long)n, k, s.size(), secs, ru.ru_maxrss / 1024.0, ru.ru_maxrss * 1024.0 / (double)c,
              (double)s.bytes_reserved() / (double)s.size(), s.check_invariants() ? "true" : "false");
}
