// bench.cpp -- scaling micro-benchmarks for SCALING_DESIGN_v0.md (scratch; not production code).
// Includes the production headers read-only (Scripts/SMC_BVS/core/cpp) and measures:
//   gram   : data_init Gram time vs a lane-parallel, bitwise-identical Gram (checks every entry for equality)
//   score  : Scorer::score with the stored Gram vs Gram-free (from-X) columns; checks bit equality of log m
//   tables : build_tables vs a DFS bordered-Cholesky table scorer; checks bit equality of every table entry
//   setup  : complete_linkage / make_blocks / neighbour_graph timing; partial-selection neighbour graph equality
//   engine : one real Engine::run_island at small N; per-event costs; Particle-copy and eval micro-costs
// Build: g++ -std=gnu++17 -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2 -I<core/cpp> bench.cpp -o bench
typedef void* SEXP;
inline bool Rf_isNull(SEXP) { return true; }
namespace Rcpp { template <class T> struct XPtr { XPtr(SEXP) {} T* get() { return nullptr; } }; }
#include "v3_engine.h"
#include <cstdio>
#include <cstring>
#include <random>
#include <memory>

using namespace v3;
using Clk = std::chrono::steady_clock;
static double since(Clk::time_point t) { return std::chrono::duration<double>(Clk::now() - t).count(); }

// Block-correlated design: groups of 5 columns share a latent factor (rho ~ 0.6); y from 10 true columns.
static void make_data(int n, int p, uint64_t seed, std::vector<double>& X, std::vector<double>& y) {
  std::mt19937_64 g(seed); std::normal_distribution<double> N01(0, 1);
  X.assign((size_t)n * p, 0); y.assign(n, 0);
  std::vector<double> f(n);
  for (int j = 0; j < p; ++j) {
    if (j % 5 == 0) for (int i = 0; i < n; ++i) f[i] = N01(g);
    for (int i = 0; i < n; ++i) X[(size_t)j * n + i] = 0.77 * f[i] + 0.64 * N01(g);
  }
  for (int j = 0; j < p; ++j) {  // standardise (mean 0, sd 1 with n-1)
    double m = 0, s = 0; double* x = &X[(size_t)j * n];
    for (int i = 0; i < n; ++i) m += x[i]; m /= n;
    for (int i = 0; i < n; ++i) { x[i] -= m; s += x[i] * x[i]; }
    s = std::sqrt(s / (n - 1)); for (int i = 0; i < n; ++i) x[i] /= s;
  }
  for (int t = 0; t < 10; ++t) { int j = (t * 37 + 3) % p; for (int i = 0; i < n; ++i) y[i] += 0.5 * X[(size_t)j * n + i]; }
  double m = 0, s = 0; for (int i = 0; i < n; ++i) y[i] += N01(g);
  for (int i = 0; i < n; ++i) m += y[i]; m /= n; for (int i = 0; i < n; ++i) { y[i] -= m; s += y[i] * y[i]; }
  s = std::sqrt(s / (n - 1)); for (int i = 0; i < n; ++i) y[i] /= s;
}

static void init_data(Data& D, int n, int p, uint64_t seed) {
  std::vector<double> X, y; make_data(n, p, seed, X, y);
  std::vector<int> orig(p); for (int j = 0; j < p; ++j) orig[j] = j + 1;
  data_init(D, X.data(), y.data(), n, p, orig);
}

// ---- lane-parallel Gram: every entry is the same sequential sum over i = 0..n-1 (no reassociation, no FMA) ----
static void gram_lanes(const std::vector<double>& Xc, int n, int p, std::vector<double>& G) {
  std::vector<double> Xr((size_t)n * p);
  for (int j = 0; j < p; ++j) for (int i = 0; i < n; ++i) Xr[(size_t)i * p + j] = Xc[(size_t)j * n + i];
  G.assign((size_t)p * p, 0.0);
  const int RA = 8, TB = 256;
  double acc[RA][TB];
  for (int a0 = 0; a0 < p; a0 += RA) {
    int ra = std::min(RA, p - a0);
    for (int b0 = a0; b0 < p; b0 += TB) {
      int tb = std::min(TB, p - b0);
      for (int r = 0; r < ra; ++r) for (int c = 0; c < tb; ++c) acc[r][c] = 0;
      for (int i = 0; i < n; ++i) {
        const double* row = &Xr[(size_t)i * p];
        for (int r = 0; r < ra; ++r) {
          double xa = row[a0 + r]; double* ac = acc[r]; const double* xb = row + b0;
          for (int c = 0; c < tb; ++c) ac[c] += xa * xb[c];
        }
      }
      for (int r = 0; r < ra; ++r) for (int c = 0; c < tb; ++c) {
        int a = a0 + r, b = b0 + c; if (b < a) continue;
        G[(size_t)b * p + a] = acc[r][c]; G[(size_t)a * p + b] = acc[r][c];
      }
    }
  }
}

static int mode_gram(int n, int p) {
  Data D; auto t0 = Clk::now(); init_data(D, n, p, 7); double t_init = since(t0);
  std::vector<double> G2; t0 = Clk::now(); gram_lanes(D.X, n, p, G2); double t_lane = since(t0);
  size_t bad = 0; for (size_t i = 0; i < G2.size(); ++i) if (std::memcmp(&G2[i], &D.G[i], 8) != 0) ++bad;
  printf("gram n=%d p=%d data_init_s=%.3f lane_gram_s=%.3f speedup=%.1f mismatched_entries=%zu of %zu\n", n, p, t_init, t_lane,
         t_init / t_lane, bad, G2.size());
  return 0;
}

// ---- score cost: stored Gram vs Gram-free (from X); bit equality ----
static int mode_score(int n, int p) {
  Data D; init_data(D, n, p, 11);
  Scorer sc(&D); std::mt19937_64 g(5);
  int ks[] = {1, 5, 10, 20, 50, 100};
  for (int k : ks) {
    if (k > D.K) continue;
    int reps = k <= 20 ? 20000 : (k <= 50 ? 2000 : 400);
    std::vector<std::vector<int>> Ms(reps);
    for (auto& S : Ms) { std::vector<int> all; while ((int)all.size() < k) { int j = (int)(g() % p); if (std::find(all.begin(), all.end(), j) == all.end()) all.push_back(j); } std::sort(all.begin(), all.end()); S = all; }
    std::vector<double> a(reps), b(reps);
    auto t0 = Clk::now(); for (int r = 0; r < reps; ++r) a[r] = sc.score(Ms[r]).logm; double tg = since(t0) / reps;
    ScoreOut o; std::vector<double> LH;
    t0 = Clk::now(); for (int r = 0; r < reps; ++r) { sc.try_chol(Ms[r], true, o, LH); b[r] = o.logm; } double tx = since(t0) / reps;
    int bad = 0; for (int r = 0; r < reps; ++r) if (std::memcmp(&a[r], &b[r], 8) != 0) ++bad;
    printf("score n=%d p=%d k=%d gram_us=%.3f gramfree_us=%.3f mismatches=%d/%d\n", n, p, k, tg * 1e6, tx * 1e6, bad, reps);
  }
  return 0;
}

// ---- DFS bordered-Cholesky table scorer (same operation order as chol_inplace / finish_from_factors) ----
struct DFSTab {
  const Data& D; Scorer& sc; const std::vector<int>& mem; int m;
  std::vector<double>& logm; std::vector<int>& route;
  static const int MB = 16;
  double LH[MB][MB], LA[MB][MB], w[MB];
  int S[MB]; long incr = 0, fallback = 0;
  DFSTab(const Data& d, Scorer& s, const std::vector<int>& mm, std::vector<double>& lm, std::vector<int>& rt)
      : D(d), sc(s), mem(mm), m((int)mm.size()), logm(lm), route(rt) {}
  void full(uint32_t code, int k) {  // fallback: production scorer on the sorted subset
    std::vector<int> U(S, S + k); ScoreOut o = sc.score(U); logm[code] = o.logm; route[code] = o.route; ++fallback;
  }
  // state for prefix of size k: rows 0..k-1 of LH/LA, w[0..k-1], running sums
  void rec(int k, uint32_t code, int last, bool ok, double sH, double sA, double quad) {
    for (int q = last + 1; q < m; ++q) {
      int jn = mem[q]; uint32_t c2 = code | (1u << q); S[k] = jn; int kk = k + 1;
      if (kk > D.K) continue;
      bool ok2 = ok; double sH2 = sH, sA2 = sA, quad2 = quad;
      if (ok2) {
        double n1 = D.n + 1.0;
        // new row k of H = (n+1) G + I and of A = G + I, exactly as try_chol forms them
        double hr[MB], ar[MB];
        for (int t = 0; t <= k; ++t) { double gg = D.Gat(S[k], S[t]); double id = (t == k) ? 1.0 : 0.0; hr[t] = n1 * gg + id; ar[t] = gg + id; }
        for (int j = 0; j < k; ++j) {
          double s = hr[j]; for (int t = 0; t < j; ++t) s -= LH[k][t] * LH[j][t]; LH[k][j] = s / LH[j][j];
          double s2 = ar[j]; for (int t = 0; t < j; ++t) s2 -= LA[k][t] * LA[j][t]; LA[k][j] = s2 / LA[j][j];
        }
        double dH = hr[k]; for (int t = 0; t < k; ++t) dH -= LH[k][t] * LH[k][t];
        double dA = ar[k]; for (int t = 0; t < k; ++t) dA -= LA[k][t] * LA[k][t];
        if (!(dH > 0) || !std::isfinite(dH) || !(dA > 0) || !std::isfinite(dA)) ok2 = false;
        else {
          LH[k][k] = std::sqrt(dH); LA[k][k] = std::sqrt(dA);
          sH2 = sH + std::log(LH[k][k]); sA2 = sA + std::log(LA[k][k]);
          double s = D.z[jn]; for (int t = 0; t < k; ++t) s -= LH[k][t] * w[t]; w[k] = s / LH[k][k];
          quad2 = quad + w[k] * w[k];
          double Q = D.yty - D.n * quad2;
          if (Q < 1e-8 * D.yty) full(c2, kk);  // non-negative Q form needs the full model: production path
          else {
            double ldH = sH2 * 2, ldA = sA2 * 2, arg = 2 * D.b0 + Q;
            logm[c2] = (arg > 0) ? D.logCn - 0.5 * (ldH - ldA) - D.nu * std::log(arg) : NEG_INF;
            route[c2] = ROUTE_CHOL; ++incr;
          }
        }
      }
      if (!ok2) full(c2, kk);
      rec(kk, c2, q, ok2, sH2, sA2, quad2);
    }
  }
};

static int mode_tables(int n, int p, int B, int nblocks) {
  Data D; init_data(D, n, p, 13);
  Start st; st.D = &D;
  for (int b = 0; b < nblocks && (b + 1) * B <= p; ++b) { std::vector<int> c; for (int i = 0; i < B; ++i) c.push_back(b * B + i); st.blocks.push_back(c); }
  Scorer sc(&D);
  auto t0 = Clk::now(); build_tables(st, sc); double t_ref = since(t0);
  long bad = 0, tot = 0, incr = 0, fb = 0;
  t0 = Clk::now();
  std::vector<std::vector<double>> lm(st.J); std::vector<std::vector<int>> rt(st.J);
  for (int b = 0; b < st.J; ++b) {
    uint32_t nc = 1u << st.blocks[b].size();
    lm[b].assign(nc, std::numeric_limits<double>::quiet_NaN()); rt[b].assign(nc, -1);
    lm[b][0] = D.logm0; rt[b][0] = ROUTE_CHOL;
    DFSTab T(D, sc, st.blocks[b], lm[b], rt[b]);
    T.rec(0, 0, -1, true, 0.0, 0.0, 0.0);
    incr += T.incr; fb += T.fallback;
  }
  double t_dfs = since(t0);
  for (int b = 0; b < st.J; ++b) for (size_t c = 0; c < lm[b].size(); ++c) { ++tot; if (std::memcmp(&lm[b][c], &st.logm_tab[b][c], 8) != 0) ++bad; }
  printf("tables n=%d B=%d blocks=%d scores=%ld ref_s=%.3f (%.2f us/score) dfs_s=%.3f (%.2f us/score) speedup=%.1f incremental=%ld fallback=%ld mismatches=%ld\n",
         n, B, st.J, tot, t_ref, 1e6 * t_ref / tot, t_dfs, 1e6 * t_dfs / tot, t_ref / t_dfs, incr, fb, bad);
  return 0;
}

// partial-selection neighbour graph (same comparator: |r| desc, then index asc; a strict total order)
static std::vector<std::vector<int>> nb_partial(const Data& D, int B) {
  int p = D.p; std::vector<std::vector<int>> N(p); if (p == 1) return N;
  std::vector<double> s(p); for (int j = 0; j < p; ++j) s[j] = std::sqrt(D.Gat(j, j));
  double rn = std::sqrt(2.0 * std::log((double)p) / D.n);
  std::vector<std::vector<int>> chosen(p); std::vector<int> cand; std::vector<double> ra(p);
  for (int j = 0; j < p; ++j) {
    int above = 0; cand.clear();
    for (int l = 0; l < p; ++l) { if (l == j) continue; ra[l] = std::fabs(D.Gat(l, j) / (s[l] * s[j])); if (ra[l] > rn) ++above; cand.push_back(l); }
    int keep = std::min(B, std::max(1, above));
    auto cmp = [&](int a, int b) { if (ra[a] != ra[b]) return ra[a] > ra[b]; return a < b; };
    std::nth_element(cand.begin(), cand.begin() + (keep - 1), cand.end(), cmp);
    std::sort(cand.begin(), cand.begin() + keep, cmp);
    chosen[j].assign(cand.begin(), cand.begin() + keep);
  }
  for (int j = 0; j < p; ++j) for (int l : chosen[j]) { N[j].push_back(l); N[l].push_back(j); }
  for (int j = 0; j < p; ++j) { std::sort(N[j].begin(), N[j].end()); N[j].erase(std::unique(N[j].begin(), N[j].end()), N[j].end()); }
  return N;
}

static int mode_setup(int n, int p, int B) {
  Data D; auto t0 = Clk::now(); init_data(D, n, p, 17); double t_init = since(t0);
  t0 = Clk::now(); Dendrogram T = complete_linkage(D); double t_cl = since(t0);
  t0 = Clk::now(); auto blocks = make_blocks(D, B); double t_mb = since(t0);
  t0 = Clk::now(); auto N1 = neighbour_graph(D, B); double t_nb = since(t0);
  t0 = Clk::now(); auto N2 = nb_partial(D, B); double t_nb2 = since(t0);
  printf("setup n=%d p=%d B=%d data_init_s=%.3f complete_linkage_s=%.3f make_blocks_s=%.3f J=%zu neighbour_graph_s=%.3f partial_sel_s=%.3f nb_equal=%d\n",
         n, p, B, t_init, t_cl, t_mb, blocks.size(), t_nb, t_nb2, (int)(N1 == N2));
  return 0;
}

static int mode_engine(int n, int p, int B, int N, int T) {
  Data D; init_data(D, n, p, 19);
  auto h = std::make_shared<Start>(); Start& st = *h; st.D = &D; st.B = B;
  auto t0 = Clk::now(); st.blocks = make_blocks(D, B); double t_bl = since(t0);
  Scorer sc(&D); t0 = Clk::now(); build_tables(st, sc); double t_tab = since(t0);
  t0 = Clk::now(); build_start(st); double t_st = since(t0);
  t0 = Clk::now(); auto Nb = neighbour_graph(D, B); double t_nb = since(t0);
  Ledger led(&D, 4); ScoreCache cache; cache.init(D.W, 500 * (size_t)p);
  Engine E(D, st, Nb, B); E.cache = &cache; E.led = &led;
  RngSource rng; rng.g.seed_stream(12345, 10); E.vs = &rng;
  std::vector<double> grid; for (int t = 0; t <= T; ++t) grid.push_back((double)t / T);
  int L = 2, Hm = 1;
  t0 = Clk::now(); IslandResult r = E.run_island(1, N, grid, L, Hm, 0, nullptr); double t_isl = since(t0);
  double logical = 0, fresh = 0; for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) { logical += led.logical[a][b]; fresh += led.fresh[a][b]; }
  double prounds = (double)N * (T + L + Hm), steps = prounds * (p + B + 2);
  printf("engine n=%d p=%d B=%d J=%d blocks_s=%.2f tables_s=%.2f start_s=%.3f nb_s=%.2f | island N=%d T=%d L=%d Hm=%d s=%.2f us/step=%.3f ms/particle_round=%.2f logical=%.3g fresh=%.3g hit_rate=%.3f logZ=%.3f\n",
         n, p, B, st.J, t_bl, t_tab, t_st, t_nb, N, T, L, Hm, t_isl, 1e6 * t_isl / steps, 1e3 * t_isl / prounds, logical, fresh,
         (double)cache.hits / std::max<double>(1, cache.hits + cache.misses), r.logZ);
  // micro-costs at a model of size 10
  Particle P; std::vector<int> S0; for (int t = 0; t < 10; ++t) S0.push_back((t * 97 + 1) % p); std::sort(S0.begin(), S0.end());
  E.set_model(P, S0); E.led = nullptr;
  int reps = 200000; Particle Q;
  t0 = Clk::now(); for (int i = 0; i < reps; ++i) { Q = P; Q.h ^= (uint64_t)i; } double t_copy = since(t0) / reps;
  t0 = Clk::now(); double sink = 0; for (int i = 0; i < reps; ++i) sink += st.comp(P.S, E.scratch); double t_comp = since(t0) / reps;
  std::mt19937_64 g(3); int reps2 = 20000;
  E.cache = nullptr;  // misses: every flip scored
  t0 = Clk::now(); for (int i = 0; i < reps2; ++i) { Q = P; int j = (int)(g() % p); if (bit_get(Q.bits, j)) E.del_var(Q, j); else E.add_var(Q, j); E.eval(Q, ME_GIBBS_FLIP, false); sink += Q.F; } double t_miss = since(t0) / reps2;
  ScoreCache c2; c2.init(D.W, 500 * (size_t)p); E.cache = &c2; std::vector<int> js(reps2); for (auto& j : js) j = (int)(g() % 64);
  for (int i = 0; i < reps2; ++i) { Q = P; int j = js[i]; if (bit_get(Q.bits, j)) E.del_var(Q, j); else E.add_var(Q, j); E.eval(Q, ME_GIBBS_FLIP, false); }
  t0 = Clk::now(); for (int i = 0; i < reps2; ++i) { Q = P; int j = js[i]; if (bit_get(Q.bits, j)) E.del_var(Q, j); else E.add_var(Q, j); E.eval(Q, ME_GIBBS_FLIP, false); sink += Q.F; } double t_hit = since(t0) / reps2;
  printf("micro p=%d W=%d particle_copy_us=%.3f comp_us=%.3f flip_eval_miss_us=%.3f flip_eval_hit_us=%.3f (sink %.1f)\n", p, D.W, 1e6 * t_copy,
         1e6 * t_comp, 1e6 * t_miss, 1e6 * t_hit, sink * 0);
  return 0;
}

int main(int argc, char** argv) {
  if (argc < 2) { printf("usage: bench gram|score|tables|setup|engine ...\n"); return 1; }
  std::string m = argv[1];
  auto I = [&](int i, int d) { return argc > i ? atoi(argv[i]) : d; };
  if (m == "gram") return mode_gram(I(2, 200), I(3, 2000));
  if (m == "score") return mode_score(I(2, 200), I(3, 5000));
  if (m == "tables") return mode_tables(I(2, 200), I(3, 2000), I(4, 14), I(5, 20));
  if (m == "setup") return mode_setup(I(2, 200), I(3, 2000), I(4, 14));
  if (m == "engine") return mode_engine(I(2, 200), I(3, 1000), I(4, 10), I(5, 64), I(6, 8));
  return 1;
}
