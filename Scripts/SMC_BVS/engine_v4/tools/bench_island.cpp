// bench_island.cpp -- WP3 measurements on Owls (ENGINEERING_SPEC §0-v2.4; WP3 brief item 8). Every number it prints is
// thread-time unless labelled wall. Modes:
//   kernel <p> <threads> <nsup> <k> <div> <arith:bit|A> <tile>
//        ns per (support, label) of the engine's label-major tile kernel (products + 8-lane flip scores + odds), nsup
//        supports of size k (div = 0: the 5 truths + k-5 random members; div = 1: all random).
//   island <p> <N> <threads list> <bit|A> <lm|pm> <G> <tile> <geo:T | adaptive:Te> <L> <Hm> [n] [store_cap]
//        one island end to end on AR(0.6) data, once per thread count (same output hash required); grid geo:T = a
//        geometric T-stage grid, adaptive:Te = core's pilot rule (ESS >= 0.9 N per stage, floor 1/Te) on the island's
//        own population (a calibrated-like schedule). Prints ns per step, M, products, offers, phase times, peak RSS.
//   store <cap> <threads> <offers_per_thread>
//        cost of TopStore::offer under a realistic mix (most offers below tau, duplicates above it).
#include <omp.h>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <cmath>
#include <random>
#include "v4/island/island.h"

using namespace v4::island;
static double now() { return omp_get_wtime(); }

template <Arith A>
static void bench_kernel(int p, int T, int nsup, int k, int div, int Bk) {
  const int n = 200;
  Data D; double t0 = now(); make_ar_data(D, n, p, 0.6, 1);
  Start st; build_start(st, D, contiguous_blocks(p, 4));
  std::printf("data+tables n=%d p=%d: %.1f s wall\n", n, p, now() - t0);
  BitScorer sc(&D);
  std::mt19937_64 g(4242);
  Model truth; for (int t = 0; t < 5; ++t) truth.push_back((int)std::floor((t + 0.5) * p / 5));
  std::vector<SupportCache> sup(nsup); std::vector<int> act;
  for (int s = 0; s < nsup; ++s) {
    Model S = div ? Model() : truth;
    while ((int)S.size() < k) { int j = (int)(g() % p); if (!contains(S, j)) sorted_insert(S, j); }
    double lm = sc.score(S).logm, c = st.comp(S);
    build_support(D, st, sc, sup[s], S, zobrist(D, S), lm, D.logprior[S.size()] + c, (lm - D.logm0) - c, 1.0);
    act.insert(act.end(), S.begin(), S.end());
  }
  std::sort(act.begin(), act.end()); act.erase(std::unique(act.begin(), act.end()), act.end());
  int nA = (int)act.size();
  for (auto& s : sup) { s.arow.resize(s.k); for (int a = 0; a < s.k; ++a) s.arow[a] = (int)(std::lower_bound(act.begin(), act.end(), s.S[a]) - act.begin()); }
  avec<double> XA((size_t)nA * n); for (int a = 0; a < nA; ++a) std::memcpy(&XA[(size_t)a * n], D.col(act[a]), 8 * n);
  int ntile = (p + Bk - 1) / Bk; avec<double> Xt((size_t)ntile * Bk * n, 0.0);
  for (int ti = 0; ti < ntile; ++ti) for (int jj = 0; jj < Bk && ti * Bk + jj < p; ++jj) for (int i = 0; i < n; ++i) Xt[(size_t)ti * Bk * n + (size_t)i * Bk + jj] = D.col(ti * Bk + jj)[i];
  double tprod = 0, tflip = 0; long pairs = 0; double chk = 0;
  double w0 = now();
  #pragma omp parallel num_threads(T) reduction(+ : tprod, tflip, pairs, chk)
  {
    BitScorer scl(&D);
    avec<double> Pp((size_t)nA * Bk); std::vector<double> lb(Bk), ob(Bk);
    #pragma omp for schedule(dynamic, 4)
    for (int ti = 0; ti < ntile; ++ti) {
      int j0 = ti * Bk, nbv = std::min(Bk, p - j0); const double* Xtile = &Xt[(size_t)ti * Bk * n];
      double ta = now();
      { static const int blk = std::getenv("V4_PRODUCTS_BLOCK") ? std::atoi(std::getenv("V4_PRODUCTS_BLOCK")) : 4;
        tile_products(XA.data(), nA, n, Xtile, Bk, Pp.data(), blk); }
      double tb = now();
      for (auto& c : sup) {
        std::vector<v8d> ub(64); v8d* u = ub.data();
        for (int v = 0; v < nbv; v += 8) {
          int32_t j8[8]; unsigned valid = 0;
          for (int l = 0; l < 8; ++l) { int j = std::min(j0 + v + l, p - 1); j8[l] = j; if (v + l < nbv && !contains(c.S, j0 + v + l)) valid |= 1u << l; }
          for (int a = 0; a < c.k; ++a) u[a] = load8(&Pp[(size_t)c.arow[a] * Bk + v]);
          if constexpr (A == Arith::ClassA) eval8_add<A>(D, st, scl, c, 0, u, j8, valid, &lb[v], &ob[v]);
          else {
            unsigned rest = valid;
            while (rest) { int l0 = __builtin_ctz(rest); int q = (int)(std::lower_bound(c.S.begin(), c.S.end(), j8[l0]) - c.S.begin()); unsigned lanes = 0;
              for (int l = l0; l < 8; ++l) if (((rest >> l) & 1u) && (int)(std::lower_bound(c.S.begin(), c.S.end(), j8[l]) - c.S.begin()) == q) lanes |= 1u << l;
              eval8_add<A>(D, st, scl, c, q, u, j8, lanes, &lb[v], &ob[v]); rest &= ~lanes; }
          }
        }
        for (int jj = 0; jj < nbv; ++jj) chk += ob[jj];
        pairs += nbv;
      }
      double tc = now(); tprod += tb - ta; tflip += tc - tb;
    }
  }
  double wall = now() - w0;
  std::printf("kernel arith=%s p=%d threads=%d supports=%d k=%d div=%d tile=%d |A|=%d: products %.1f ns, flip+odds %.1f ns, "
              "total %.1f ns per (support,label) thread-time; wall %.2f s [chk %.4f]\n",
              A == Arith::Bit ? "bit" : "A", p, T, nsup, k, div, Bk, nA, 1e9 * tprod / pairs, 1e9 * tflip / pairs, 1e9 * (tprod + tflip) / pairs, wall, chk);
}

static long vm_hwm_kb() {
  FILE* f = std::fopen("/proc/self/status", "r"); if (!f) return -1;
  char line[256]; long kb = -1;
  while (std::fgets(line, sizeof line, f)) if (std::strncmp(line, "VmHWM:", 6) == 0) { kb = std::atol(line + 6); break; }
  std::fclose(f); return kb;
}
static std::vector<int> parse_list(const std::string& s) {
  std::vector<int> v; size_t i = 0;
  while (i < s.size()) { size_t j = s.find(',', i); if (j == std::string::npos) j = s.size(); v.push_back(std::atoi(s.substr(i, j - i).c_str())); i = j + 1; }
  return v;
}

// island <p> <N> <threads list, e.g. 1,24,48,96> <bit|A> <lm|pm> <G> <tile> <grid: geo:T | adaptive:Te> <L> <Hm> [n] [cap]
template <Arith A>
static void bench_island(int p, int N, const std::vector<int>& thr, KernelKind kk, int G, int Bk, const std::string& gspec, int L, int Hm, int n, uint64_t cap) {
  Data D; double t0 = now(); make_ar_data(D, n, p, 0.6, 7);
  Start st; build_start(st, D, contiguous_blocks(p, 4));
  Neighbours nb = window_neighbours(D, 14, 8);
  std::printf("# data AR(0.6) n=%d p=%d (stand-in partition: blocks of 4; window neighbours, B=14): %.1f s wall\n", n, p, now() - t0);
  IslandConfig c; c.store_dup_filter = std::getenv("V4_NO_DUP_FILTER") == nullptr; c.verbose = std::getenv("V4_VERBOSE") != nullptr;
  if (const char* e = std::getenv("V4_ISLAND_ID")) c.island = (uint32_t)std::atoi(e);
  if (const char* e = std::getenv("V4_PRODUCTS_BLOCK")) c.products_block = std::atoi(e);
  if (const char* e = std::getenv("V4_MEM_BUDGET_GB")) c.mem_budget = (uint64_t)(std::atof(e) * 1073741824.0); c.store_parallel_compact = std::getenv("V4_SERIAL_COMPACT") == nullptr; c.allow_test_kernels = true; c.seed = 2026; c.island = 1; c.N = N; c.L = L; c.Hm = Hm; c.B = 14; c.kernel = kk; c.G = G; c.tile = Bk; c.store_cap = cap;
  if (gspec.rfind("geo:", 0) == 0) {
    int Tst = std::atoi(gspec.c_str() + 4);
    c.grid.push_back(0.0); for (int t = 1; t < Tst; ++t) c.grid.push_back(std::pow(10.0, -3.0 * (1.0 - (double)t / (Tst - 1))) * ((double)t / Tst));
    c.grid.push_back(1.0);
    for (size_t i = 1; i < c.grid.size(); ++i) if (!(c.grid[i] > c.grid[i - 1])) c.grid[i] = std::nextafter(c.grid[i - 1], 2.0);
  } else if (gspec.rfind("steps:", 0) == 0) {   // explicit stages phi_1,...,phi_T (the last must be 1)
    c.grid.push_back(0.0); std::string r = gspec.substr(6); size_t i = 0;
    while (i < r.size()) { size_t j = r.find(',', i); if (j == std::string::npos) j = r.size(); c.grid.push_back(std::atof(r.substr(i, j - i).c_str())); i = j + 1; }
  } else if (gspec.rfind("adaptive:", 0) == 0) {
    c.adaptive = true; c.adaptive_H = N; c.adaptive_Te = std::atoi(gspec.c_str() + 9);
  } else { std::fprintf(stderr, "grid spec: geo:T | steps:phi1,...,1 | adaptive:Te\n"); std::exit(2); }
  uint64_t h0 = 0;
  for (int T : thr) {
    c.threads = T;
    double w0 = now();
    IslandRun r = run_island<A>(D, st, nb, c);
    double wall = now() - w0;
    const auto& k = r.ks;
    int rounds = r.T + L + Hm;
    double steps = (double)N * (p + 16) * rounds;   // elementary steps N (p + B + 2) per round
    if (!h0) h0 = r.hash();
    std::printf("island arith=%s kernel=%s p=%d n=%d N=%d threads=%d G=%d tile=%d grid=%s (T=%d) L=%d Hm=%d status=%d\n", A == Arith::Bit ? "bit" : "A",
                kk == KernelKind::LabelMajor ? "lm" : "pm", p, n, N, T, G, Bk, gspec.c_str(), r.T, L, Hm, r.status);
    std::printf("  wall %.2f s | ns per elementary step: %.1f thread-time (wall x threads / N(p+16)rounds) | %.2f wall\n", wall, 1e9 * wall * T / steps, 1e9 * wall / steps);
    std::printf("  M (sweeps per particle-round) %.3f | (support,label) pairs per particle-round / p %.3f | passes %llu | distinct supports per pass %.1f\n",
                (double)k.particle_sweeps / std::max<uint64_t>(1, k.particle_rounds), (double)k.support_label_pairs / std::max<uint64_t>(1, k.particle_rounds) / p,
                (unsigned long long)k.passes, (double)k.supports / std::max<uint64_t>(1, k.passes));
    std::printf("  products %.2f thread-s = %.1f ns per (support,label) pair = %.1f ns per step | phase A %.1f ns per pair (thread-time, incl. products)\n",
                k.t_products, 1e9 * k.t_products / std::max<uint64_t>(1, k.support_label_pairs), 1e9 * k.t_products / steps,
                1e9 * k.t_phaseA * T / std::max<uint64_t>(1, k.support_label_pairs));
    std::printf("  offers buffered %llu (%.4f per step), duplicates dropped by the snapshot filter %llu (%.4f per step), store merges %llu, store %zu entries (cap %llu)\n",
                (unsigned long long)k.store_buffered, k.store_buffered / steps, (unsigned long long)k.store_dup_dropped, k.store_dup_dropped / steps,
                (unsigned long long)k.store_merges, r.top_v.size(), (unsigned long long)(cap ? cap : 40ULL * p + 1));
    std::printf("  memory plan (admission, ESTIMATE): %s | G used %d\n", r.mem_plan.c_str(), r.G_used);
    std::printf("  store compaction: %.2f s wall in total (%llu compactions, %llu serial in-pass fallbacks; %s)\n", k.t_store_compact,
                (unsigned long long)k.store_merges, (unsigned long long)k.store_serial_merges, c.store_parallel_compact ? "parallel at pass/step boundaries" : "serial under the mutex");
    std::printf("  wall s: init %.2f orders %.2f build %.2f phaseA %.2f walk %.2f phaseB %.2f apply %.2f barrier %.2f pm %.2f\n",
                k.t_init, k.t_orders, k.t_build, k.t_phaseA, k.t_walk, k.t_phaseB, k.t_apply, k.t_barrier, k.t_pm);
    std::printf("  ns per step by phase (thread-time): orders %.1f build %.1f phaseA %.1f walk %.1f phaseB %.1f apply %.1f\n",
                1e9 * k.t_orders * T / steps, 1e9 * k.t_build * T / steps, 1e9 * k.t_phaseA * T / steps, 1e9 * k.t_walk * T / steps,
                1e9 * k.t_phaseB * T / steps, 1e9 * k.t_apply * T / steps);
    { uint64_t pool = r.top_pool.size(), ne = r.top_v.size();
      std::printf("  store: %llu entries, mean |S| %.2f, kept run %.1f MB (+ index %.1f MB); kept runs alive at most %d (process)\n", (unsigned long long)ne,
                  ne ? (double)pool / ne : 0.0, (26.0 * ne + 4.0 * pool) / 1e6, 4.0 * (double)v4::island::pow2_ceil(2 * ne + 2) / 1e6, k.kept_live_max); }
    std::printf("  logZ %.6f  HPM |S|=%zu F=%.4f  peak RSS %.2f GB  output hash %016llx (%s across thread counts)\n", r.logZ, r.hpm.S.size(), r.hpm.F,
                vm_hwm_kb() / 1048576.0, (unsigned long long)r.hash(), r.hash() == h0 ? "same" : "DIFFERENT");
    std::fflush(stdout);
  }
}

static void bench_store(uint64_t cap, int T, long per) {
  TopStore st; st.init(cap, Order::HPM);
  std::vector<StoreBuffer> bufs(T);
  // phase 1 fill: cap distinct models with F ~ N(0,1)
  double t0 = now();
  #pragma omp parallel num_threads(T)
  {
    std::mt19937_64 g(omp_get_thread_num() + 1); std::normal_distribution<double> nd;
    #pragma omp for
    for (long i = 0; i < (long)cap; ++i) { int32_t S[3] = {(int32_t)(i % 1000000), (int32_t)(1000000 + i / 1000000), 2100000}; st.offer(bufs[omp_get_thread_num()], nd(g), S, 3, splitmix64(*(uint64_t*)&i)); }
  }
  for (auto& b : bufs) st.flush(b);
  st.compact();
  double tfill = now() - t0;
  // phase 2: mix: 90% far below tau, 10% re-offers of stored models (duplicates)
  t0 = now();
  #pragma omp parallel num_threads(T)
  {
    std::mt19937_64 g(100 + omp_get_thread_num());
    #pragma omp for
    for (long i = 0; i < per * T; ++i) {
      if (g() % 10) { int32_t S[3] = {1, 2, 3}; st.offer(bufs[omp_get_thread_num()], -10.0, S, 3, 12345); }
      else { size_t e = g() % st.size(); st.offer(bufs[omp_get_thread_num()], st.value(e), st.k->pool.data() + st.k->off[e], st.k->len[e], st.k->hash[e]); }
    }
  }
  for (auto& b : bufs) st.flush(b);
  st.compact();
  double tmix = now() - t0;
  std::printf("store cap=%llu threads=%d: fill %.1f ns per offer (thread-time), mix(90%% reject, 10%% duplicate) %.1f ns per offer; merges %llu; invariant %d\n",
              (unsigned long long)cap, T, 1e9 * tfill * T / cap, 1e9 * tmix * T / (per * T), (unsigned long long)st.n_merges, (int)st.check_invariant());
}

int main(int argc, char** argv) {
  if (argc < 2) { std::fprintf(stderr, "see header\n"); return 1; }
  std::string mode = argv[1];
  if (mode == "kernel") {
    int p = atoi(argv[2]), T = atoi(argv[3]), ns = atoi(argv[4]), k = atoi(argv[5]), div = atoi(argv[6]); std::string ar = argv[7]; int Bk = atoi(argv[8]);
    if (ar == "bit") bench_kernel<Arith::Bit>(p, T, ns, k, div, Bk); else bench_kernel<Arith::ClassA>(p, T, ns, k, div, Bk);
  } else if (mode == "island") {
    if (argc < 12) { std::fprintf(stderr, "island <p> <N> <threads,list> <bit|A> <lm|pm> <G> <tile> <geo:T|steps:..|adaptive:Te> <L> <Hm> [n] [cap]\n"); return 2; }
    int p = atoi(argv[2]), N = atoi(argv[3]); std::vector<int> thr = parse_list(argv[4]); std::string ar = argv[5], kn = argv[6];
    int G = atoi(argv[7]), Bk = atoi(argv[8]); std::string gs = argv[9]; int L = atoi(argv[10]), Hm = atoi(argv[11]);
    int n = argc > 12 ? atoi(argv[12]) : 200; uint64_t cap = argc > 13 ? strtoull(argv[13], 0, 10) : 0;
    KernelKind kk = kn == "pm" ? KernelKind::ParticleMajor : KernelKind::LabelMajor;
    std::printf("# v4_bench_island flags %s, island ISA override '%s', kernel namespace %s; host threads available %d; compiler %s\n",
                V4_BIT_FLAGS_STR, V4_ISLAND_ISA_STR, kHasFMA() ? "fma" : "base", omp_get_max_threads(), __VERSION__);
    if (ar == "bit") bench_island<Arith::Bit>(p, N, thr, kk, G, Bk, gs, L, Hm, n, cap); else bench_island<Arith::ClassA>(p, N, thr, kk, G, Bk, gs, L, Hm, n, cap);
  } else if (mode == "store") {
    bench_store(strtoull(argv[2], 0, 10), atoi(argv[3]), atol(argv[4]));
  } else return 1;
  return 0;
}
