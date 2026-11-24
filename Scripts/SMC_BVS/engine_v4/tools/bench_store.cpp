// bench_store.cpp -- Store memory / time probes (review PR11 #1, PR40 performance section). One mode per process.
//   fill  [c] [offers] [k]       Store(c, HPM), `offers` improving offers of distinct k-models (every offer enters)
//   load  [c] [k]                a valid unique sorted store of c entries loaded two ways: offer + compact (the old
//                                path) and load_unique_sorted (the bulk loader; only when built with V4_HAVE_BULK)
//   merge [c] [R] [k] [share]    R island stores of c entries each (fraction `share` of models common to all, with
//                                class-A-like values differing by 1 ulp), merged into one store with Store::merge
// Prints wall time per phase, peak RSS and an order-sensitive content hash (same bits before / after a change).
#include <sys/resource.h>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include "v4/store.h"
using namespace v4;
using Clock = std::chrono::steady_clock;
static double since(Clock::time_point t0) { return std::chrono::duration<double>(Clock::now() - t0).count(); }
static double peak_mb() { struct rusage ru; getrusage(RUSAGE_SELF, &ru); return ru.ru_maxrss / 1024.0; }
static uint64_t mix(uint64_t x) { return splitmix64(x); }
static void make_model(uint64_t id, int k, Model& S) { S.resize(k); for (int a = 0; a < k; ++a) S[a] = (int32_t)(id * (uint64_t)k + a); }

int main(int argc, char** argv) {
  std::string mode = argc > 1 ? argv[1] : "fill";
  if (mode == "fill") {
    uint64_t c = argc > 2 ? std::strtoull(argv[2], nullptr, 10) : 4000001, n = argc > 3 ? std::strtoull(argv[3], nullptr, 10) : 16000000;
    int k = argc > 4 ? std::atoi(argv[4]) : 7;
    Store s(c, Order::HPM); Model S;
    auto t0 = Clock::now();
    for (uint64_t i = 0; i < n; ++i) { make_model(i, k, S); s.offer((double)i, S, mix(i)); }
    s.compact();
    std::printf("{\"mode\":\"fill\",\"cap\":%llu,\"offers\":%llu,\"k\":%d,\"seconds\":%.2f,\"peak_rss_MB\":%.0f,\"hash\":\"%016llx\"}\n",
                (unsigned long long)c, (unsigned long long)n, k, since(t0), peak_mb(), (unsigned long long)s.content_hash());
  } else if (mode == "load") {
    uint64_t c = argc > 2 ? std::strtoull(argv[2], nullptr, 10) : 4000001; int k = argc > 3 ? std::atoi(argv[3]) : 7;
    // a valid store's sections (sorted by decreasing value, distinct models), as in an island file
    std::vector<double> v(c); std::vector<uint64_t> h(c), off(c); std::vector<uint16_t> len(c, (uint16_t)k); std::vector<int32_t> pool(c * k);
    for (uint64_t i = 0; i < c; ++i) { v[i] = -(double)i; h[i] = mix(i); off[i] = i * k; for (int a = 0; a < k; ++a) pool[i * k + a] = (int32_t)(i * k + a); }
    double t_offer, t_bulk = -1; uint64_t h1, h2 = 0;
    { Store s(c, Order::HPM); auto t0 = Clock::now();
      for (uint64_t i = 0; i < c; ++i) s.offer(v[i], ModelView(pool.data() + off[i], len[i]), h[i]);
      s.compact(); t_offer = since(t0); h1 = s.content_hash(); }
#ifdef V4_HAVE_BULK
    { Store s(c, Order::HPM); auto t0 = Clock::now();
      s.load_unique_sorted(c, v.data(), h.data(), off.data(), len.data(), pool.data(), pool.size());
      t_bulk = since(t0); h2 = s.content_hash(); }
#endif
    std::printf("{\"mode\":\"load\",\"cap\":%llu,\"k\":%d,\"offer_compact_s\":%.2f,\"bulk_s\":%.2f,\"peak_rss_MB\":%.0f,\"hash_offer\":\"%016llx\",\"hash_bulk\":\"%016llx\"}\n",
                (unsigned long long)c, k, t_offer, t_bulk, peak_mb(), (unsigned long long)h1, (unsigned long long)h2);
  } else if (mode == "merge") {
    uint64_t c = argc > 2 ? std::strtoull(argv[2], nullptr, 10) : 4000001; int R = argc > 3 ? std::atoi(argv[3]) : 3;
    int k = argc > 4 ? std::atoi(argv[4]) : 7; double share = argc > 5 ? std::atof(argv[5]) : 0.5;
    Store merged(c, Order::HPM); Model S; double t_merge = 0;
    for (int r = 0; r < R; ++r) {
      Store isl(c, Order::HPM);
      const uint64_t nshared = (uint64_t)(share * (double)c);
      for (uint64_t i = 0; i < c; ++i) {
        uint64_t id = i < nshared ? i : (uint64_t)(r + 1) * 1000000000ULL + i;   // shared ids are common to all islands
        double val = -(double)i * 1e-3;
        if (i < nshared && (r % 2 == 1)) val = std::nextafter(val, 0.0);           // class-A-like: 1 ulp apart
        make_model(id, k, S); isl.offer(val, S, mix(id));
      }
      isl.compact();
      auto t0 = Clock::now(); merged.merge(isl); t_merge += since(t0);
    }
    std::printf("{\"mode\":\"merge\",\"cap\":%llu,\"R\":%d,\"k\":%d,\"share\":%.2f,\"merge_s\":%.2f,\"peak_rss_MB\":%.0f,\"kept\":%zu,\"hash\":\"%016llx\"}\n",
                (unsigned long long)c, R, k, share, t_merge, peak_mb(), merged.size(), (unsigned long long)merged.content_hash());
  }
  return 0;
}
