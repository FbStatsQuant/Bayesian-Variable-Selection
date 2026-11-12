// engine_bench.cpp -- island benchmark and byte dump for the bit-identical engine work of leg B (B1).
// One source compiled against a core's cpp/ directory with the production flags:
//   g++ -std=gnu++17 -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2 -I<core>/cpp engine_bench.cpp -o bench
//   bench OUT.bin P N T [n]
// It builds a block-correlated design (n = 200 by default), the setup, and runs: table ingestion, inherited models,
// two islands (streams 10, 11) on a T-stage grid with L = 3 burn-in and 2 measured rounds, a local search from the
// HPM and one from the start mode -- the call sequence of cpp_final_run. It dumps every output byte (log Z, stage
// records, PIPs, RB accumulators, move statistics, stream positions, HPM with provenance, the three stores, counters,
// cache statistics, route counters) and prints microseconds per elementary step. Dumps of two cores must be equal.
typedef void* SEXP;
inline bool Rf_isNull(SEXP) { return true; }
namespace Rcpp { template <class T> struct XPtr { XPtr(SEXP) {} T* get() { return nullptr; } }; }
#include "v3_engine.h"
#include <cstdio>
#include <cstring>
#include <random>
using namespace v3;
static FILE* OUT = nullptr;
static void put(const void* p, size_t nb) { if (nb) fwrite(p, 1, nb, OUT); }
static void put_d(double x) { put(&x, sizeof x); }
static void put_i(long long x) { put(&x, sizeof x); }
static void put_vd(const std::vector<double>& v) { put_i((long long)v.size()); put(v.data(), v.size() * sizeof(double)); }
static void put_vi(const std::vector<int>& v) { put_i((long long)v.size()); put(v.data(), v.size() * sizeof(int)); }
static void put_ev(const EventCtx& e) { put_i(e.phase); put_i(e.tier); put_i(e.island); put_i(e.stage); put_i(e.round); put_i(e.particle); put_i(e.position); put_i(e.iter); put_d(e.phi); }
static void put_ms(const std::vector<MoveStats>& v) { put_i((long long)v.size()); for (auto& m : v) put(&m, sizeof m); }
static void put_store(const TopStore& s) { put_i((long long)s.s.size()); for (auto& e : s.s) { put_d(e.v); put_vi(e.S); } }
static void standardise(std::vector<double>& x, int n) {
  double m = 0, s = 0; for (int i = 0; i < n; ++i) m += x[i]; m /= n;
  for (int i = 0; i < n; ++i) { x[i] -= m; s += x[i] * x[i]; } s = std::sqrt(s / (n - 1)); for (int i = 0; i < n; ++i) x[i] /= s;
}
int main(int argc, char** argv) {
  if (argc < 5) { fprintf(stderr, "usage: bench OUT.bin P N T [n]\n"); return 2; }
  OUT = fopen(argv[1], "wb"); int p = atoi(argv[2]), N = atoi(argv[3]), T = atoi(argv[4]), n = argc > 5 ? atoi(argv[5]) : 200;
  std::mt19937_64 g(20261112); std::normal_distribution<double> N01(0, 1);
  std::vector<double> X((size_t)n * p), y(n, 0.0), f(n), col(n);
  for (int j = 0; j < p; ++j) {
    if (j % 5 == 0) for (int i = 0; i < n; ++i) f[i] = N01(g);
    for (int i = 0; i < n; ++i) col[i] = std::sqrt(0.7) * f[i] + std::sqrt(0.3) * N01(g);
    standardise(col, n); for (int i = 0; i < n; ++i) X[(size_t)j * n + i] = col[i];
  }
  const double beta[6] = {1.4, -1.0, 1.8, -1.2, 0.8, -1.6};
  for (int t = 0; t < 14; ++t) { int j = (5 * (t * (p / 5 / 14)) + (t % 5)) % p; for (int i = 0; i < n; ++i) y[i] += beta[t % 6] * X[(size_t)j * n + i]; }
  for (int i = 0; i < n; ++i) y[i] += N01(g);
  standardise(y, n);
  std::vector<int> orig(p); for (int j = 0; j < p; ++j) orig[j] = j + 1;
  Data D; data_init(D, X.data(), y.data(), n, p, orig);
  int B = std::min(std::min((int)std::floor(std::sqrt((double)n)), (int)std::floor(std::sqrt((double)p))), 16);
  Start st; st.D = &D; st.B = B; st.blocks = make_blocks(D, B);
  Scorer sc0(&D); build_tables(st, sc0); build_start(st);
  std::vector<std::vector<int>> Nb = neighbour_graph(D, B);
  Ledger led(&D, 2);
  { EventCtx ev; ev.phase = PH_TABLE; ev.island = 0; std::vector<int> U;   // table ingestion as in v3_core.cpp ingest_tables
    for (int b = 0; b < st.J; ++b) { int m = (int)st.blocks[b].size();
      for (uint32_t c = 0; c < (1u << m); ++c) { if (std::isnan(st.logm_tab[b][c])) continue; U.clear();
        for (int i = 0; i < m; ++i) if (c & (1u << i)) U.push_back(st.blocks[b][i]);
        double lm = st.logm_tab[b][c]; ev.stage = b + 1; ev.position = (int)c;
        led.event(U, D.logprior[U.size()] + lm, D.logprior[U.size()] + st.logr[b][c], lm, true, false, ev, ME_TABLE); } } }
  ScoreCache cache; cache.init(D.W, (size_t)500 * p);
  Engine E(D, st, Nb, B); E.cache = &cache; E.led = &led;
  std::vector<double> grid(T + 1); for (int t = 0; t <= T; ++t) grid[t] = std::pow((double)t / T, 2.0); grid[T] = 1.0;
  const int L = 3, Hm = 2; double steps = 0, secs = 0;
  for (int r = 1; r <= 2; ++r) {
    RngSource rng; rng.g.seed_stream(4242, (uint64_t)(9 + r)); E.vs = &rng;
    auto t0 = Clock::now();
    IslandResult res = E.run_island(r, N, grid, L, Hm, 0, nullptr);
    secs += secs_since(t0); steps += (double)N * (T + L + Hm) * (p + B + 2);
    put_d(res.logZ); put_vd(res.phi); put_vd(res.inc); put_vd(res.ess); put_vd(res.cum); put_vi(res.distinct_resampled); put_vi(res.distinct_moved);
    put_ms(res.stage_moves); put_ms(res.terminal_moves); put_vi(res.terminal_distinct); put_vd(res.pip); put_vd(res.rb_acc);
    for (auto& v : res.rb_round) put_vd(v);
    put_i((long long)res.init_hash); put_i((long long)rng.g.count);
  }
  auto t1 = Clock::now();
  LocalArchive A = E.local_search(led.hpmS, 8, 0, false);
  ModeResult mr = start_mode(st, 1000000, true);
  LocalArchive A0 = E.local_search(mr.S, 8 + (int)mr.S.size(), 0, true, -1, PH_LS0);
  double sec_ls = secs_since(t1);
  for (const LocalArchive* a : {&A, &A0}) { put_vi(a->centre); put_d(a->centre_F); put_vi(a->returned); put_d(a->returned_F); put_i(a->moves); put_i(a->n_eval);
    put_vd(a->path_F); put_vd(a->scanned_F); put_vi(a->scan_size); put_i(a->local_limit); put_i(a->local_certified); for (auto& m : a->path) put_vi(m); }
  put_vi(led.hpmS); put_d(led.hpmF); put_d(led.hpm_logm); put_ev(led.hpm_ev); put_i(led.hpm_mech);
  put_store(led.top); put_store(led.lead0); put_store(led.lead1); put_vd(led.island_best);
  put(led.logical, sizeof led.logical); put(led.fresh, sizeof led.fresh);
  put_i((long long)cache.hits); put_i((long long)cache.misses); put_i((long long)cache.inserts); put_i((long long)cache.clears); put_i((long long)cache.count);
  put_i((long long)D.routes[0]); put_i((long long)D.routes[1]); put_i((long long)D.routes[2]); put_i((long long)D.q_recomputed_count);
  fclose(OUT);
  printf("p=%d N=%d T=%d n=%d B=%d J=%d | islands %.2f s, %.3f us/step | hit rate %.3f | local searches %.2f s (%ld + %ld models) | hpm size %d F %.6f\n",
         p, N, T, n, B, st.J, secs, 1e6 * secs / steps, (double)cache.hits / (cache.hits + cache.misses), sec_ls, A.n_eval, A0.n_eval, (int)led.hpmS.size(), led.hpmF);
  return 0;
}
