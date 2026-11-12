// bitid_units.cpp -- header-level bitwise regression of v3.2-dev against v3.1 (W3-SCALE leg A).
// The SAME source is compiled twice with the production flags, once against each core's cpp/ directory:
//   g++ -std=gnu++17 -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2 -I<core>/cpp bitid_units.cpp -o units_v31
//   g++ ... -DHAVE_V31_REFS -I<core_v32dev>/cpp bitid_units.cpp -o units_v32
// Each binary writes, for a list of test cases, every byte of: the Gram, z and constants; the dendrogram and blocks;
// the neighbour graph; the block tables (log r, log m, route) and the numerical-route counters; the start (profiles,
// convolutions, normaliser, sampler tables, start mode); and one small island + local search (log Z, PIPs, HPM, stores,
// score counters, stream position). The two dump files must be byte-identical (cmp). With HAVE_V31_REFS the v3.2-dev
// binary also checks its new routines against the v3.1 reference routines kept in the headers, in the same process.
// Cases include un-standardised and tampered data that exist only to drive the scorer's fallback branches.
typedef void* SEXP;
inline bool Rf_isNull(SEXP) { return true; }
namespace Rcpp { template <class T> struct XPtr { XPtr(SEXP) {} T* get() { return nullptr; } }; }
#include "v3_engine.h"
#include <cstdio>
#include <cstring>
#include <random>

using namespace v3;
static double since(Clock::time_point t) { return std::chrono::duration<double>(Clock::now() - t).count(); }

static FILE* OUT = nullptr;
static uint64_t FNV = 1469598103934665603ULL;
static void put(const void* p, size_t nbytes) {
  if (nbytes == 0) return;
  fwrite(p, 1, nbytes, OUT);
  const unsigned char* c = (const unsigned char*)p;
  for (size_t i = 0; i < nbytes; ++i) { FNV ^= c[i]; FNV *= 1099511628211ULL; }
}
static void put_d(double x) { put(&x, sizeof x); }
static void put_i(long long x) { put(&x, sizeof x); }
static void put_vd(const std::vector<double>& v) { put_i((long long)v.size()); put(v.data(), v.size() * sizeof(double)); }
static void put_vi(const std::vector<int>& v) { put_i((long long)v.size()); put(v.data(), v.size() * sizeof(int)); }
static void put_vvi(const std::vector<std::vector<int>>& v) { put_i((long long)v.size()); for (auto& x : v) put_vi(x); }
static void put_vvd(const std::vector<std::vector<double>>& v) { put_i((long long)v.size()); for (auto& x : v) put_vd(x); }

struct Case {
  std::string name; int n = 0, p = 0;
  std::vector<double> X, y;
  int B = 0;                     // block width (0: production rule min(isqrt n, isqrt p, 16))
  double z_scale = 1.0;          // tampering of z after data_init (drives the small-Q branch); 1 = none
  bool island = false;           // also run one small island and a local search
};

static void standardise(std::vector<double>& x, int n) {
  double m = 0, s = 0;
  for (int i = 0; i < n; ++i) m += x[i];
  m /= n;
  for (int i = 0; i < n; ++i) { x[i] -= m; s += x[i] * x[i]; }
  s = std::sqrt(s / (n - 1));
  for (int i = 0; i < n; ++i) x[i] /= s;
}
// Block-correlated design: groups of 5 columns share a factor; y from 10 columns + noise; all standardised.
static Case make_generic(const std::string& name, int n, int p, uint64_t seed, double rho) {
  Case c; c.name = name; c.n = n; c.p = p;
  std::mt19937_64 g(seed); std::normal_distribution<double> N01(0, 1);
  c.X.assign((size_t)n * p, 0); c.y.assign(n, 0);
  std::vector<double> f(n), col(n);
  double a = std::sqrt(rho), b = std::sqrt(1 - rho);
  for (int j = 0; j < p; ++j) {
    if (j % 5 == 0) for (int i = 0; i < n; ++i) f[i] = N01(g);
    for (int i = 0; i < n; ++i) col[i] = a * f[i] + b * N01(g);
    standardise(col, n);
    for (int i = 0; i < n; ++i) c.X[(size_t)j * n + i] = col[i];
  }
  for (int t = 0; t < std::min(10, p); ++t) { int j = (t * 37 + 3) % p; for (int i = 0; i < n; ++i) c.y[i] += 0.5 * c.X[(size_t)j * n + i]; }
  for (int i = 0; i < n; ++i) c.y[i] += N01(g);
  standardise(c.y, n);
  return c;
}
// Copies and sign flips of columns: exact ties in correlations (|r| = 1 pairs, equal off-diagonal values), in the
// linkage distances (R13 tie rule), in the neighbour ranking (index tie-break) and in the table scores.
static void add_duplicates(Case& c, int every) {
  int n = c.n, p = c.p;
  for (int j = every; j < p; j += every) {
    int src = j - 1 - (j / every) % 3;
    double sgn = ((j / every) % 2) ? -1.0 : 1.0;
    for (int i = 0; i < n; ++i) c.X[(size_t)j * n + i] = sgn * c.X[(size_t)src * n + i];
  }
}
// Small-integer design: entries in {-1, 0, 1}, not standardised; many exactly equal Gram entries and correlations.
static Case make_integer(const std::string& name, int n, int p, uint64_t seed) {
  Case c; c.name = name; c.n = n; c.p = p;
  std::mt19937_64 g(seed);
  c.X.assign((size_t)n * p, 0); c.y.assign(n, 0);
  for (size_t i = 0; i < c.X.size(); ++i) c.X[i] = (double)((int)(g() % 3) - 1);
  for (int j = 0; j < p; ++j) c.X[(size_t)j * n + (j % n)] = 1.0;  // no all-zero column
  for (int i = 0; i < n; ++i) c.y[i] = (double)((int)(g() % 5) - 2) + c.X[i] - c.X[(size_t)(p > 1 ? 1 : 0) * n + i];
  return c;
}
static void scale_columns(Case& c, double factor, int every, int offset) {
  for (int j = offset; j < c.p; j += every) for (int i = 0; i < c.n; ++i) c.X[(size_t)j * c.n + i] *= factor;
}

static int isqrt_i(int x) { int r = (int)std::floor(std::sqrt((double)x)); while ((r + 1) * (r + 1) <= x) ++r; while (r * r > x) --r; return r; }

static long long N_REF_FAIL = 0;

static void run_case(const Case& c) {
  auto t_case = Clock::now();
  int n = c.n, p = c.p;
  put(c.name.data(), c.name.size()); put_i(n); put_i(p);
  put_vd(c.X); put_vd(c.y);
  std::vector<int> orig(p); for (int j = 0; j < p; ++j) orig[j] = j + 1;
  Data D;
  auto t0 = Clock::now();
  data_init(D, c.X.data(), c.y.data(), n, p, orig);
  double t_gram = since(t0);
#ifdef HAVE_V31_REFS
  { Data R; R.n = n; R.p = p; R.X = D.X; gram_fill_v31(R);
    if (R.G.size() != D.G.size() || std::memcmp(R.G.data(), D.G.data(), D.G.size() * sizeof(double)) != 0) { ++N_REF_FAIL; printf("  REF MISMATCH gram %s\n", c.name.c_str()); } }
#endif
  if (c.z_scale != 1.0) for (auto& v : D.z) v *= c.z_scale;
  put_vd(D.G); put_vd(D.z); put_d(D.yty); put_d(D.logCn); put_d(D.logm0); put_d(D.logWK); put_vd(D.logw); put_vd(D.logprior); put_i(D.K);
  int B = c.B > 0 ? c.B : std::min(std::min(isqrt_i(n), isqrt_i(p)), 16);
  put_i(B);
  // blocks and dendrogram
  t0 = Clock::now();
  Dendrogram T; std::vector<std::vector<int>> blocks = make_blocks(D, B, &T);
  double t_blocks = since(t0);
  put_vvi(blocks); put_vi(T.left); put_vi(T.right); put_vi(T.size); put_vi(T.minidx); put_vd(T.height); put_i(T.root);
  // neighbour graph
  t0 = Clock::now();
  std::vector<std::vector<int>> Nb = neighbour_graph(D, B);
  double t_nb = since(t0);
  put_vvi(Nb);
#ifdef HAVE_V31_REFS
  { auto R = neighbour_graph_v31(D, B); if (R != Nb) { ++N_REF_FAIL; printf("  REF MISMATCH neighbour graph %s\n", c.name.c_str()); } }
#endif
  // tables
  Start st; st.D = &D; st.B = B; st.blocks = blocks;
  Scorer sc(&D);
  std::string table_status = "ok";
  t0 = Clock::now();
  try { build_tables(st, sc); } catch (NumericalFailure& e) { table_status = e.what(); }
  double t_tab = since(t0);
  put(table_status.data(), table_status.size());
  put_vvd(st.logr); put_vvd(st.logm_tab); put_vvi(st.route_tab);
  put_i((long long)D.routes[0]); put_i((long long)D.routes[1]); put_i((long long)D.routes[2]);
  put_i((long long)D.q_recomputed_count); put_i((long long)D.numerical_failures);
  long long routes_now[5] = {(long long)D.routes[0], (long long)D.routes[1], (long long)D.routes[2], (long long)D.q_recomputed_count, (long long)D.numerical_failures};
#ifdef HAVE_V31_REFS
  { uint64_t keep[5] = {D.routes[0], D.routes[1], D.routes[2], D.q_recomputed_count, D.numerical_failures};
    D.routes[0] = D.routes[1] = D.routes[2] = 0; D.q_recomputed_count = 0; D.numerical_failures = 0;
    Start r; r.D = &D; r.B = B; r.blocks = blocks; Scorer s2(&D); std::string rs = "ok";
    try { build_tables_v31(r, s2); } catch (NumericalFailure& e) { rs = e.what(); }
    auto same_vvd = [](const std::vector<std::vector<double>>& a, const std::vector<std::vector<double>>& b) {
      if (a.size() != b.size()) return false;
      for (size_t i = 0; i < a.size(); ++i) { if (a[i].size() != b[i].size()) return false; if (!a[i].empty() && std::memcmp(a[i].data(), b[i].data(), a[i].size() * sizeof(double)) != 0) return false; }
      return true; };
    bool ok = rs == table_status && same_vvd(r.logr, st.logr) && same_vvd(r.logm_tab, st.logm_tab) && r.route_tab == st.route_tab &&
              D.routes[0] == keep[0] && D.routes[1] == keep[1] && D.routes[2] == keep[2] && D.q_recomputed_count == keep[3] && D.numerical_failures == keep[4];
    if (!ok) { ++N_REF_FAIL; printf("  REF MISMATCH tables %s (ref status %s)\n", c.name.c_str(), rs.c_str()); }
    D.routes[0] = keep[0]; D.routes[1] = keep[1]; D.routes[2] = keep[2]; D.q_recomputed_count = keep[3]; D.numerical_failures = keep[4]; }
#endif
  long long ncodes = 0, nnan = 0, nroute[3] = {0, 0, 0};
  for (auto& v : st.route_tab) for (int r : v) { ++ncodes; if (r < 0) ++nnan; else nroute[r]++; }
  double t_start = 0, t_isl = 0;
  if (table_status == "ok") {
    t0 = Clock::now();
    build_start(st);
    t_start = since(t0);
    put_vvd(st.logprof); put_vvd(st.logF); put_d(st.logZbar0); put_vd(st.size_logmass); put_vd(st.size_cum);
    for (auto& b : st.cond_cum) put_vvd(b);
    for (auto& b : st.sub_cum) put_vvd(b);
    ModeResult mr = start_mode(st, 1000000, true);
    put_vi(mr.S); put_d(mr.lg0); put_i(mr.ties); put_i(mr.truncated); put_i(mr.tie_dp_used);
    if (c.island) {
      t0 = Clock::now();
      Ledger led(&D, 1);
      ScoreCache cache; cache.init(D.W, (size_t)500 * p);
      Engine E(D, st, Nb, B); E.cache = &cache; E.led = &led;
      RngSource rng; rng.g.seed_stream(77, 10); E.vs = &rng;
      std::vector<double> grid{0.0, 0.05, 0.15, 0.3, 0.5, 0.75, 1.0};
      std::string isl_status = "ok";
      try {
        IslandResult res = E.run_island(1, 48, grid, 2, 2, 0, nullptr);
        put_d(res.logZ); put_vd(res.inc); put_vd(res.ess); put_vd(res.pip); put_vd(res.rb_acc); put_vi(res.distinct_moved); put_i((long long)res.init_hash);
        LocalArchive A = E.local_search(led.hpmS, 6, 0, false);
        put_vi(A.returned); put_d(A.returned_F); put_i(A.moves); put_i(A.n_eval); put_vvi(A.path);
      } catch (NumericalFailure& e) { isl_status = e.what(); }
      put(isl_status.data(), isl_status.size());
      put_vi(led.hpmS); put_d(led.hpmF); put_i((long long)rng.g.count);
      for (auto& e : led.top.s) { put_d(e.v); put_vi(e.S); }
      put(led.logical, sizeof led.logical); put(led.fresh, sizeof led.fresh);
      put_i((long long)cache.hits); put_i((long long)cache.misses); put_i((long long)cache.inserts);
      put_i((long long)D.routes[0]); put_i((long long)D.routes[1]); put_i((long long)D.routes[2]); put_i((long long)D.q_recomputed_count);
      t_isl = since(t0);
    }
  }
  printf("%-22s n=%4d p=%5d B=%2d J=%4d codes=%8lld unscored=%6lld routes(chol/refactor/qr)=%lld/%lld/%lld tab_counters=%lld/%lld/%lld qrec=%lld fail=%lld status=%s | s: gram %.3f blocks %.3f nb %.3f tables %.3f start %.3f island %.3f total %.2f | fnv %016llx\n",
         c.name.c_str(), n, p, B, (int)blocks.size(), ncodes, nnan, nroute[0], nroute[1], nroute[2], routes_now[0], routes_now[1], routes_now[2], routes_now[3], routes_now[4],
         table_status == "ok" ? "ok" : "numerical_failure", t_gram, t_blocks, t_nb, t_tab, t_start, t_isl, since(t_case), (unsigned long long)FNV);
  fflush(stdout);
}

int main(int argc, char** argv) {
  if (argc < 2) { fprintf(stderr, "usage: units OUT.bin [big]\n"); return 2; }
  OUT = fopen(argv[1], "wb");
  if (!OUT) { fprintf(stderr, "cannot open %s\n", argv[1]); return 2; }
  bool big = argc > 2 && std::string(argv[2]) == "big";
  std::vector<Case> cases;
  // generic designs; p not a multiple of the Gram lane width; with islands
  { Case c = make_generic("generic_p203", 200, 203, 11, 0.6); c.island = true; cases.push_back(c); }
  { Case c = make_generic("generic_p600", 200, 600, 12, 0.6); cases.push_back(c); }
  { Case c = make_generic("generic_n60_p333", 60, 333, 13, 0.3); c.island = true; cases.push_back(c); }
  { Case c = make_generic("independent_p401", 200, 401, 14, 0.0); cases.push_back(c); }
  // tiny problems: p = 1, 2, 3, 7, 8, 9; n small so that K = n/2 is small
  for (int p : {1, 2, 3, 7, 8, 9, 17}) { Case c = make_generic("tiny_p" + std::to_string(p), 12, p, 20 + p, 0.5); cases.push_back(c); }
  // block width above K: sub-models larger than K are not scored (NaN entries)
  { Case c = make_generic("B_above_K", 6, 40, 31, 0.5); c.B = 6; cases.push_back(c); }
  { Case c = make_generic("B_above_K_dup", 8, 30, 32, 0.5); add_duplicates(c, 3); c.B = 7; cases.push_back(c); }
  // exact ties: duplicated and sign-flipped columns; integer designs
  { Case c = make_generic("duplicates_p300", 200, 300, 41, 0.6); add_duplicates(c, 4); c.island = true; cases.push_back(c); }
  { Case c = make_generic("duplicates_dense", 100, 128, 42, 0.2); add_duplicates(c, 2); cases.push_back(c); }
  { Case c = make_integer("integer_n40_p120", 40, 120, 43); c.island = true; cases.push_back(c); }
  { Case c = make_integer("integer_n16_p64", 16, 64, 44); cases.push_back(c); }
  // fallback routes (un-standardised data; these cases exist only to drive the branches):
  //  huge duplicated columns: the Cholesky pivot of a duplicate is lost to rounding -> refactor -> augmented QR
  { Case c = make_generic("huge_dup_qr", 50, 90, 51, 0.5); add_duplicates(c, 3); scale_columns(c, 1e150, 1, 0); cases.push_back(c); }
  { Case c = make_generic("huge_dup_qr_mixed", 50, 99, 52, 0.5); add_duplicates(c, 2); scale_columns(c, 1e140, 3, 1); c.island = true; cases.push_back(c); }
  { Case c = make_generic("huge_dup_1e120", 30, 60, 55, 0.4); add_duplicates(c, 2); scale_columns(c, 1e120, 1, 0); cases.push_back(c); }
  //  overflowing Gram: every route fails -> NumericalFailure while scoring the tables
  { Case c = make_generic("overflow_fail", 30, 40, 53, 0.5); scale_columns(c, 1e160, 7, 3); cases.push_back(c); }
  { Case c = make_generic("overflow_fail_late", 30, 60, 54, 0.5); scale_columns(c, 1e160, 1000, 57); cases.push_back(c); }
  //  small Q: z inflated after data_init so that y'y - n z'H^{-1}z < 1e-8 y'y for good models (non-negative recomputation)
  { Case c = make_generic("smallQ_z1p002", 200, 150, 61, 0.6); c.z_scale = 1.002; cases.push_back(c); }
  { Case c = make_generic("smallQ_z1p01", 200, 150, 62, 0.6); c.z_scale = 1.01; c.island = true; cases.push_back(c); }
  { Case c = make_generic("smallQ_z1p05_dup", 120, 100, 63, 0.6); add_duplicates(c, 5); c.z_scale = 1.05; cases.push_back(c); }
  //  y exactly equal to one column (no noise) and z inflated: Q < 0 before the recomputation for every model with that column
  { Case c = make_generic("smallQ_exact_1p003", 200, 150, 64, 0.6); for (int i = 0; i < c.n; ++i) c.y[i] = c.X[(size_t)3 * c.n + i]; c.z_scale = 1.003; c.island = true; cases.push_back(c); }
  { Case c = make_generic("smallQ_exact_1p02_dup", 80, 96, 65, 0.6); add_duplicates(c, 4); for (int i = 0; i < c.n; ++i) c.y[i] = c.X[(size_t)10 * c.n + i]; c.z_scale = 1.02; cases.push_back(c); }
  if (big) {
    { Case c = make_generic("generic_p2000", 200, 2000, 71, 0.6); cases.push_back(c); }
    { Case c = make_generic("generic_p4001_dup", 200, 4001, 72, 0.6); add_duplicates(c, 50); cases.push_back(c); }
    { Case c = make_generic("generic_n400_p1500", 400, 1500, 73, 0.6); cases.push_back(c); }
  }
  for (auto& c : cases) run_case(c);
  fclose(OUT);
  printf("cases %d  dump fnv %016llx  in-process reference mismatches %lld\n", (int)cases.size(), (unsigned long long)FNV, N_REF_FAIL);
  return N_REF_FAIL == 0 ? 0 : 1;
}
