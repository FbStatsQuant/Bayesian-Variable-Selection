// bench_island.cpp -- WP3 measurements on Owls (ENGINEERING_SPEC §0-v2.4; WP3 brief item 8). Every number it prints is
// thread-time unless labelled wall. Modes:
//   kernel <p> <threads> <nsup> <k> <div> <arith:bit|A> <tile>
//        ns per (support, label) of the engine's label-major tile kernel (products + 8-lane flip scores + odds), nsup
//        supports of size k (div = 0: the 5 truths + k-5 random members; div = 1: all random).
//   island <p> <N> <threads list> <bit|A> <lm|pm> <G> <tile> <geo:T | adaptive:Te> <L> <Hm> [n] [store_cap]
//        one island end to end on AR(0.6) data, once per thread count (same output hash required); grid geo:T = a
//        geometric T-stage grid, adaptive:Te = core's pilot rule (ESS >= 0.9 N per stage, floor 1/Te) on the island's
//        own population (a calibrated-like schedule). Prints ns per step, M, products, offers, phase times, peak RSS.
//   sort <n> <threads> [k]                     the compaction sort: pairwise (PR26) vs merge-path (m3) vs __gnu_parallel
//   store <cap> <threads> <offers_per_thread>
//        cost of TopStore::offer under a realistic mix (most offers below tau, duplicates above it).
//   plan <p> <N> <threads> <G list> [n]      the admission's memory plan (no island run)
//   overheads <p> [n]                          per-call costs of the L5 levers, old vs new (1 thread)
// Environment: V4_K_STORE (calibration-measured mean stored |S| -> IslandConfig::k_store; island and plan modes; without
// it the island mode plans from pi_0 alone, which real runs refuse at p >= 1e5), V4_MEM_BUDGET_GB, V4_ISLAND_ID,
// V4_PRODUCTS_BLOCK (default: 4 with AVX-512, else 1), V4_VERBOSE, V4_NO_DUP_FILTER, V4_SERIAL_COMPACT,
// V4_NO_BOUNDED (WP6 K1: the dense label-major reference), V4_NO_CHECK_STORE (no I1 check at all, also not at checkpoints / the final write: O1),
// V4_GRAM_SLOTS (WP6 K3: Gram-row slots, -1 = auto 5G/2, 0 = off), V4_NO_ROLLING (WP6 K5: groups one after the other),
// V4_CKPT=<base> (checkpoints; resume from <base> when present) with V4_STOP_AFTER=<step> (stop after that step's checkpoint).
// Exit status: non-zero when any island run is refused or does not complete (review PR26 B1).
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
#include <parallel/algorithm>
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
  // products block read per run, as in the island path (review PR26 nit); default = the island ISA's (B2)
  IslandConfig cb; if (const char* e = std::getenv("V4_PRODUCTS_BLOCK")) cb.products_block = std::atoi(e);
  const int blk = products_block_of(cb);
  double w0 = now();
  #pragma omp parallel num_threads(T) reduction(+ : tprod, tflip, pairs, chk)
  {
    BitScorer scl(&D);
    avec<double> Pp((size_t)nA * Bk); std::vector<double> lb(Bk), ob(Bk);
    #pragma omp for schedule(dynamic, 4)
    for (int ti = 0; ti < ntile; ++ti) {
      int j0 = ti * Bk, nbv = std::min(Bk, p - j0); const double* Xtile = &Xt[(size_t)ti * Bk * n];
      double ta = now();
      tile_products(XA.data(), nA, n, Xtile, Bk, Pp.data(), blk);
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

static long vm_rss_kb() {
  FILE* f = std::fopen("/proc/self/status", "r"); if (!f) return -1;
  char line[256]; long kb = -1;
  while (std::fgets(line, sizeof line, f)) if (std::strncmp(line, "VmRSS:", 6) == 0) { kb = std::atol(line + 6); break; }
  std::fclose(f); return kb;
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
// returns 0 when every run completed; else the first failing run's code (refusals included: review PR26 B1):
// 20 + IslandRun::status (1 interrupted, 2 numerical_failure, 3 resource_limit), or exit_code(status) of a thrown error
template <Arith A>
static int bench_island(int p, int N, const std::vector<int>& thr, KernelKind kk, int G, int Bk, const std::string& gspec, int L, int Hm, int n, uint64_t cap) {
  Data D; double t0 = now(); make_ar_data(D, n, p, 0.6, 7);
  Start st; build_start(st, D, contiguous_blocks(p, 4));
  Neighbours nb = window_neighbours(D, 14, 8);
  std::printf("# data AR(0.6) n=%d p=%d (stand-in partition: blocks of 4; window neighbours, B=14): %.1f s wall\n", n, p, now() - t0);
  // setup inputs resident in this process (stand-in tables, neighbours, generator copies) beyond X, z, diag(G): the
  // CLI passes the mapped setup/calib sizes instead (inputs_bytes)
  const double inputs_extra = std::max(0.0, vm_rss_kb() * 1024.0 - ((double)n * p * 8 + 16.0 * p));
  IslandConfig c; c.store_dup_filter = std::getenv("V4_NO_DUP_FILTER") == nullptr; c.verbose = std::getenv("V4_VERBOSE") != nullptr;
  if (const char* e = std::getenv("V4_PRODUCTS_BLOCK")) c.products_block = std::atoi(e);
  c.store_parallel_compact = std::getenv("V4_SERIAL_COMPACT") == nullptr; c.allow_test_kernels = true;
  c.check_store_each_step = std::getenv("V4_CHECK_EACH_STEP") != nullptr;   // the pre-O1 behaviour (before/after comparisons)
  if (const char* e = std::getenv("V4_COST_PATH")) c.cost_path = e;   // D-30 per-step cost record (JSON lines; O2)
  c.seed = 2026; c.island = 1; c.N = N; c.L = L; c.Hm = Hm; c.B = 14; c.kernel = kk; c.G = G; c.tile = Bk; c.store_cap = cap;
  // environment overrides AFTER the defaults (the island id was reset to 1 before: manager 11-16 note 1)
  if (const char* e = std::getenv("V4_ISLAND_ID")) c.island = (uint32_t)std::atoi(e);
  if (const char* e = std::getenv("V4_MEM_BUDGET_GB")) c.mem_budget = (uint64_t)(std::atof(e) * 1073741824.0);
  if (const char* e = std::getenv("V4_K_STORE")) c.k_store = std::atof(e);   // calibration-measured mean stored |S| (B1)
  else c.k_store_optional = true;   // bench only: without V4_K_STORE the plan's k comes from pi_0 alone (r1 refuses this in real runs)
  c.inputs_bytes = inputs_extra;
  c.bounded_scoring = std::getenv("V4_NO_BOUNDED") == nullptr; c.check_store = std::getenv("V4_NO_CHECK_STORE") == nullptr;
  if (const char* e = std::getenv("V4_CKPT")) { c.ckpt_path = e; c.ckpt_every_s = 1e30; c.resume = true; }   // checkpoint only at V4_STOP_AFTER
  if (const char* e = std::getenv("V4_STOP_AFTER")) c.stop_after_step = std::atoi(e);
  if (const char* e = std::getenv("V4_GRAM_SLOTS")) c.gram_slots = std::atoi(e);   // K3: -1 auto (default), 0 off
  c.rolling_admission = std::getenv("V4_NO_ROLLING") == nullptr;   // K5: groups one after the other (the pre-K5 behaviour)
  std::printf("# bounded scoring %s, Gram-row slots %d at G %d, rolling admission %s, I1 store check %s%s\n", c.bounded_scoring ? "on" : "OFF (dense reference)",
              gram_slots_of(c, G, p), G, c.rolling_admission ? "on" : "off", !c.check_store ? "off" : c.check_store_each_step ? "after every step" : "at checkpoints and the final write (O1)",
              c.ckpt_path.empty() ? "" : (", checkpoints " + c.ckpt_path).c_str());
  std::printf("# island id %u (address key), seed %u, k_store %s, products block %d\n", c.island, c.seed,
              c.k_store > 0 ? std::to_string(c.k_store).c_str() : "absent (pi_0 plan)", products_block_of(c));
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
  uint64_t h0 = 0; int rc = 0;
  for (int T : thr) {
    c.threads = T;
    double w0 = now();
    IslandRun r;
    try { r = run_island<A>(D, st, nb, c); }
    catch (const v4::Error& e) { std::printf("island threads=%d REFUSED: %s\n", T, e.what()); std::fflush(stdout); if (!rc) rc = v4::exit_code(e.st); continue; }
    double wall = now() - w0;
    if (r.status != 0) { std::printf("island threads=%d status=%d (NOT completed): %s\n", T, r.status, r.reason.c_str()); if (!rc) rc = 20 + r.status; }
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
    std::printf("  store check (I1, parallel; O1): %llu checks, %.2f s wall (%s)\n", (unsigned long long)k.store_checks, k.t_check,
                c.check_store_each_step ? "after every step: V4_CHECK_EACH_STEP" : "before checkpoints and the final write");
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
  return rc;
}

// sort <n> <threads> [k]: the compaction's first sort (by model: hash, |S|, S, v desc) on n staged refs of mean size k,
// old (one task per pair: PR26 r2) vs new (merge-path segments: review m3) vs __gnu_parallel::sort (pre-r2); same result
template <class T, class Less>
static void psort_pairwise_old(std::vector<T>& a, std::vector<T>& tmp, Less less, int threads) {
  const size_t n = a.size(); tmp.resize(n); const int C = threads;
  std::vector<size_t> b(C + 1); for (int c = 0; c <= C; ++c) b[c] = n * (size_t)c / (size_t)C;
  #pragma omp parallel for num_threads(threads) schedule(static, 1)
  for (int c = 0; c < C; ++c) std::sort(a.begin() + b[c], a.begin() + b[c + 1], less);
  T* src = a.data(); T* dst = tmp.data();
  for (size_t width = 1; width < (size_t)C; width *= 2) {
    const int npairs = (int)((C + 2 * width - 1) / (2 * width));
    #pragma omp parallel for num_threads(threads) schedule(static, 1)
    for (int q = 0; q < npairs; ++q) {
      const size_t lo = b[std::min<size_t>(C, 2 * width * q)], mid = b[std::min<size_t>(C, 2 * width * q + width)], hi = b[std::min<size_t>(C, 2 * width * (q + 1))];
      std::merge(src + lo, src + mid, src + mid, src + hi, dst + lo, less);
    }
    std::swap(src, dst);
  }
  if (src != a.data()) std::copy(src, src + n, a.data());
}
static void bench_sort(size_t n, int T, int k) {
  std::mt19937_64 g(5); std::vector<int32_t> pool; std::vector<StoreRef> r(n);
  pool.reserve(n * (size_t)k);
  std::vector<size_t> off(n);
  for (size_t i = 0; i < n; ++i) {
    off[i] = pool.size(); int kk = 1 + (int)(g() % (2 * k)); int32_t last = -1;
    for (int a = 0; a < kk; ++a) { last += 1 + (int32_t)(g() % 1000); pool.push_back(last); }
  }
  for (size_t i = 0; i < n; ++i) {
    size_t e = i + 1 < n ? off[i + 1] : pool.size(); uint16_t kk = (uint16_t)(e - off[i]);
    uint64_t h = 1469598103934665603ull; for (size_t t = off[i]; t < e; ++t) h = (h ^ (uint64_t)pool[t]) * 1099511628211ull;
    // ~1/3 of the refs repeat an earlier model with another value (duplicates are common in staging)
    if (i > 10 && g() % 3 == 0) { size_t src = g() % i; r[i] = r[src]; r[i].v = std::normal_distribution<double>()(g); continue; }
    r[i] = StoreRef{std::normal_distribution<double>()(g), h, pool.data() + off[i], kk};
  }
  auto by_model = [](const StoreRef& a, const StoreRef& b) {
    if (a.h != b.h) return a.h < b.h;
    if (a.k != b.k) return a.k < b.k;
    int c = std::memcmp(a.S, b.S, sizeof(int32_t) * a.k);
    if (c != 0) return lex_less(a.S, a.k, b.S, b.k);
    return a.v > b.v;
  };
  auto same = [](const std::vector<StoreRef>& x, const std::vector<StoreRef>& y) {
    for (size_t i = 0; i < x.size(); ++i) if (x[i].h != y[i].h || x[i].S != y[i].S || std::memcmp(&x[i].v, &y[i].v, 8)) return false;
    return true;
  };
  std::vector<StoreRef> ref = r; std::sort(ref.begin(), ref.end(), by_model);
  double t_old = 1e30, t_new = 1e30, t_gnu = 1e30; bool ok = true;
  for (int rep = 0; rep < 3; ++rep) {
    std::vector<StoreRef> a = r, tmp; double t0 = now(); psort_pairwise_old(a, tmp, by_model, T); t_old = std::min(t_old, now() - t0); ok = ok && same(a, ref);
    a = r; tmp.clear(); t0 = now(); psort_noalloc(a, tmp, by_model, T); t_new = std::min(t_new, now() - t0); ok = ok && same(a, ref);
    a = r; t0 = now(); __gnu_parallel::sort(a.begin(), a.end(), by_model, __gnu_parallel::default_parallel_tag(T)); t_gnu = std::min(t_gnu, now() - t0); ok = ok && same(a, ref);
  }
  std::printf("sort n=%zu threads=%d (best of 3, wall): pairwise (PR26) %.3f s, merge-path (m3) %.3f s, __gnu_parallel %.3f s; identical %d\n",
              n, T, t_old, t_new, t_gnu, (int)ok);
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
    int rc = ar == "bit" ? bench_island<Arith::Bit>(p, N, thr, kk, G, Bk, gs, L, Hm, n, cap) : bench_island<Arith::ClassA>(p, N, thr, kk, G, Bk, gs, L, Hm, n, cap);
    if (rc) { std::fprintf(stderr, "v4_bench_island: a run did not complete (exit %d)\n", rc); return rc; }
  } else if (mode == "plan") {   // plan <p> <N> <threads> <G list> [n]: build data + setup, print the admission plan (no island run)
    int p = atoi(argv[2]), N = atoi(argv[3]), T = atoi(argv[4]); std::vector<int> Gs = parse_list(argv[5]); int n = argc > 6 ? atoi(argv[6]) : 200;
    Data D; make_ar_data(D, n, p, 0.6, 7); Start st; build_start(st, D, contiguous_blocks(p, 4)); Neighbours nb = window_neighbours(D, 14, 8);
    const double inputs_extra = std::max(0.0, vm_rss_kb() * 1024.0 - ((double)n * p * 8 + 16.0 * p));
    std::printf("# p=%d n=%d N=%d threads=%d: process RSS after data + setup %.2f GB (inputs beyond X/z/diagG %.2f GB)\n", p, n, N, T, vm_rss_kb() / 1048576.0, inputs_extra / 1073741824.0);
    for (int G : Gs) {
      IslandConfig c; c.N = N; c.threads = T; c.G = G; c.kernel = KernelKind::LabelMajor; c.Hm = 2; c.inputs_bytes = inputs_extra;
      if (const char* e = std::getenv("V4_K_STORE")) c.k_store = std::atof(e);
      double k = 0; MemPlan mp = plan_island(D, st, c, nullptr, &k, nullptr);
      std::printf("plan G=%d: %.2f GB  [%s]\n", G, mp.total / 1073741824.0, mem_plan_text(mp).c_str());
    }
  } else if (mode == "overheads") {   // overheads <p> [n]: per-call costs of the L5 levers, old vs new (1 thread), exactness checked
    int p = atoi(argv[2]); int n = argc > 3 ? atoi(argv[3]) : 200;
    Data D; make_ar_data(D, n, p, 0.6, 7); Start st; build_start(st, D, contiguous_blocks(p, 4));
    double Ek = 0; for (size_t k = 0; k < st.size_logmass.size(); ++k) Ek += (double)k * std::exp(st.size_logmass[k]);
    std::printf("# overheads p=%d n=%d J=%d E_pi0|S|=%.1f (1 thread)\n", p, n, st.J, Ek);
    // (1) pi_0 draw (the I step and the initial draws)
    { int nd = p >= 1000000 ? 20 : 100; double ts = 0, tf = 0; int same = 0;
      for (int i = 1; i <= nd; ++i) {
        Address a0; a0.seed = 2026; a0.island = 1; a0.xph = X_BRIDGE; a0.stage = 1; a0.particle = (uint32_t)i; a0.position = 5;
        auto nu = [&](uint32_t slot) { Address a = a0; a.slot = slot; return uniform_at(a); };
        const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
        Model S1, S2; double t0 = now(); draw_pi0(st, nu, S1); double t1 = now();
        draw_pi0_fast(st, nu, [&](const uint32_t* sl, double* out) { philox8_word(ctr.data(), kk.data(), 0, sl, out); }, S2); double t2 = now();
        ts += t1 - t0; tf += t2 - t1; same += S1 == S2; }
      std::printf("pi0 draw: original %.3f ms, vectorised %.4f ms per draw (%.0fx); %d/%d identical\n", 1e3 * ts / nd, 1e3 * tf / nd, ts / tf, same, nd); }
    // (2) round order (Fisher-Yates over m = p + 16 labels) + inverse
    { const int m = p + 16, reps = 3; std::vector<uint32_t> o1(m), o2(m), inv(m); double t_old = 0, t_new = 0, t_inv_old = 0, t_inv_new = 0; bool eq = true;
      for (int r = 0; r < reps; ++r) {
        Address a0; a0.seed = 2026; a0.island = 1; a0.xph = X_MEASURED; a0.stage = 1; a0.particle = (uint32_t)r + 1;
        double t0 = now();
        for (int t = 0; t < m; ++t) o1[t] = (uint32_t)t;
        uint32_t slot = 0;
        for (int t = m - 1; t >= 1; --t) { Address a = a0; a.slot = v4::slot_of(v4::SK_ORDER, slot++); int jj = (int)std::floor(uniform_at(a) * (t + 1)); std::swap(o1[t], o1[jj]); }
        double t1 = now();
        for (int t = 0; t < m; ++t) inv[o1[t]] = (uint32_t)t + 1;
        double t2 = now();
        for (int t = 0; t < m; ++t) o2[t] = (uint32_t)t;
        const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
        const int nd = m - 1; int jcur[8], jnext[8]; uint32_t sl[8]; double u8[8];
        auto block = [&](int d0, int* jj) {
          for (int l = 0; l < 8; ++l) sl[l] = v4::slot_of(v4::SK_ORDER, (uint32_t)std::min(d0 + l, std::max(0, nd - 1)));
          philox8_word(ctr.data(), kk.data(), 0, sl, u8);
          for (int l = 0; l < 8 && d0 + l < nd; ++l) { const int t = m - 1 - (d0 + l); jj[l] = (int)std::floor(u8[l] * (t + 1)); __builtin_prefetch(&o2[jj[l]], 1); }
        };
        if (nd > 0) block(0, jcur);
        for (int d0 = 0; d0 < nd; d0 += 8) { if (d0 + 8 < nd) block(d0 + 8, jnext);
          for (int l = 0; l < 8 && d0 + l < nd; ++l) { const int t = m - 1 - (d0 + l); std::swap(o2[t], o2[jcur[l]]); }
          std::memcpy(jcur, jnext, sizeof jcur); }
        double t3 = now();
        for (int t = 0; t < m; ++t) { if (t + 16 < m) __builtin_prefetch(&inv[o2[t + 16]], 1); inv[o2[t]] = (uint32_t)t + 1; }
        double t4 = now();
        t_old += t1 - t0; t_inv_old += t2 - t1; t_new += t3 - t2; t_inv_new += t4 - t3; eq = eq && o1 == o2;
      }
      std::printf("round order: Fisher-Yates %.1f -> %.1f ns per label; inverse %.1f -> %.1f ns per label; identical %d\n", 1e9 * t_old / reps / m,
                  1e9 * t_new / reps / m, 1e9 * t_inv_old / reps / m, 1e9 * t_inv_new / reps / m, (int)eq); }
    // (3) score rows grown from a few supports to 145 (two arrays): the zero-fill the sizing-once fix removes
    { std::vector<double> a, b; a.resize((size_t)5 * p); b.resize((size_t)5 * p);
      double t0 = now(); a.resize((size_t)145 * p); b.resize((size_t)145 * p); double t1 = now();
      std::printf("score rows: growing 5 -> 145 supports re-zero-fills %.2f GB in %.3f s (per group, before the fix)\n", 2.0 * 140 * p * 8 / 1e9, t1 - t0); }
  } else if (mode == "sort") {
    bench_sort(strtoull(argv[2], 0, 10), atoi(argv[3]), argc > 4 ? atoi(argv[4]) : 7);
  } else if (mode == "store") {
    bench_store(strtoull(argv[2], 0, 10), atoi(argv[3]), atol(argv[4]));
  } else return 1;
  return 0;
}
