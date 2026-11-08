// W1-N1 numerical harness. Drives the PRODUCTION v2.2.1 headers (unmodified, include path -I CODE/cpp), except
// v3_engine.h which is taken from ./instr (production copy + 2 read-only instrumentation lines, see ../instr.diff).
//
// Modes:
//   export <design_id> <outdir>        : build design, setup (blocks, tables, start, graph) with production code,
//                                        enumerate Omega, production scores, production pilot + build_grid, and the
//                                        exact kernel matrix of each production elementary step at every phi needed.
//   mc <design_id> <outdir> <N> <reps> <grid_file> : production run_island (instrumented) on independent streams;
//                                        writes per island log Zhat and the 4N measured-endpoint states.
//
// Kernel extraction (v2, after sweep SW1): every transition probability of every elementary step is obtained by running
// the production step function on scripted uniforms (by purpose): discrete choices at interval midpoints, and every
// probability threshold (Gibbs inclusion, swap/independence acceptance) by bisection on the production step's outcome,
// down to adjacent doubles (bracket width recorded). Two quantities come from production *tables*, not from step calls:
// (i) the pi0 law of each target S' = product of the production cumulative-table interval widths along the scripted path
// (each script is validated by calling the production draw_pi0 and checking the returned model and full consumption);
// (ii) the RB recording o_j, used only as a cross-check of the bisected Gibbs threshold.
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <fstream>
#include <iostream>
#include <memory>
// ---- stubs for the only Rcpp-dependent inline function in v3_runtime.h (runtime_ptr; never called here) ----
#define _USE_MATH_DEFINES
#include <cmath>
#include <limits>
static const double NA_REAL = std::numeric_limits<double>::quiet_NaN();  // stub (Rcpp constant; registry not used)
typedef void* SEXP;
inline bool Rf_isNull(void*) { return true; }
namespace Rcpp { template <class T> struct XPtr { explicit XPtr(void*) {} T* get() { return nullptr; } }; }
#include "v3_engine.h"

using namespace v3;

struct ScriptVS : public VariateSource {
  std::map<std::string, std::deque<double>> q;
  double u(const char* p) override {
    auto it = q.find(p);
    if (it == q.end() || it->second.empty()) throw std::runtime_error(std::string("script exhausted: ") + p);
    double v = it->second.front(); it->second.pop_front(); return v;
  }
  void clear() { q.clear(); }
  void push(const char* p, double v) { q[p].push_back(v); }
  bool all_used() const { for (auto& kv : q) if (!kv.second.empty()) return false; return true; }
};

// ---------------------------------------------------------------------------------------------
// Designs (10 seeds). Raw X: Gaussian with a correlation pattern; y = X beta + noise. Standardised as M §4.4.
// ---------------------------------------------------------------------------------------------
struct Design { int id, n, p; double rho; int kind; std::vector<int> S0; std::vector<double> beta; };
static Design design_of(int id) {
  // kind: 0 iid, 1 equicorrelated rho, 2 AR(1) rho, 3 exact duplicate column (col p-1 = col 0),
  //       4 two equicorrelated blocks {0..p/2-1}, {p/2..p-1} with separate common factors, within-block correlation rho
  static const int nn[10]   = {8, 10, 12, 20, 16, 9, 14, 6, 30, 11};
  static const int pp[10]   = {8, 8, 7, 6, 8, 5, 7, 4, 8, 6};
  static const double rr[10]= {0.0, 0.6, 0.9, 0.5, 0.8, 0.0, 0.95, 0.3, 0.7, 0.0};
  static const int kk[10]   = {0, 1, 2, 4, 2, 3, 1, 1, 4, 3};
  Design d; d.id = id; d.n = nn[id]; d.p = pp[id]; d.rho = rr[id]; d.kind = kk[id];
  d.beta.assign(d.p, 0.0);
  d.beta[0] = 1.0; d.beta[1] = -0.7; if (d.p >= 6) d.beta[3] = 0.5;
  for (int j = 0; j < d.p; ++j) if (d.beta[j] != 0) d.S0.push_back(j);
  return d;
}
struct Gauss {
  Xoshiro256ss g; bool have = false; double spare = 0;
  double next() {
    if (have) { have = false; return spare; }
    double u1, u2; do { u1 = g.uniform(); } while (u1 <= 0); u2 = g.uniform();
    double r = std::sqrt(-2 * std::log(u1)); spare = r * std::sin(2 * M_PI * u2); have = true; return r * std::cos(2 * M_PI * u2);
  }
};
static void standardise(std::vector<double>& v) {
  int n = (int)v.size(); double mx = 0; for (double x : v) mx = std::max(mx, std::fabs(x));
  for (double& x : v) x /= mx;
  double m = 0; for (double x : v) m += x; m /= n;
  double s = 0; for (double& x : v) { x -= m; s += x * x; }
  double sd = std::sqrt(s / (n - 1)); for (double& x : v) x /= sd;
}
static void make_data(const Design& d, std::vector<double>& X, std::vector<double>& y) {
  Gauss G; G.g.seed_stream(1000 + d.id, 777);
  int n = d.n, p = d.p;
  X.assign((size_t)n * p, 0.0); y.assign(n, 0.0);
  for (int i = 0; i < n; ++i) {
    std::vector<double> z(p); for (int j = 0; j < p; ++j) z[j] = G.next();
    double common = G.next();
    double common2 = (d.kind == 4) ? G.next() : 0.0;  // second block's own common factor (kind 4 only)
    std::vector<double> x(p);
    for (int j = 0; j < p; ++j) {
      if (d.kind == 0 || d.kind == 3) x[j] = z[j];
      else if (d.kind == 1) x[j] = std::sqrt(d.rho) * common + std::sqrt(1 - d.rho) * z[j];
      else if (d.kind == 2) x[j] = (j == 0) ? z[0] : d.rho * x[j - 1] + std::sqrt(1 - d.rho * d.rho) * z[j];
      else { double c = (j < p / 2) ? common : common2; x[j] = std::sqrt(d.rho) * c + std::sqrt(1 - d.rho) * z[j]; }
    }
    if (d.kind == 3) x[p - 1] = x[0];
    double mu = 0; for (int j = 0; j < p; ++j) { X[(size_t)j * n + i] = x[j]; mu += d.beta[j] * x[j]; }
    y[i] = mu + 0.8 * G.next();
  }
  for (int j = 0; j < p; ++j) { std::vector<double> c(X.begin() + (size_t)j * n, X.begin() + (size_t)(j + 1) * n); standardise(c); std::copy(c.begin(), c.end(), X.begin() + (size_t)j * n); }
  standardise(y);
}
static int isqrt(int x) { int r = (int)std::floor(std::sqrt((double)x)); while ((r + 1) * (r + 1) <= x) ++r; while (r * r > x) --r; return r; }
static int ceil_log2(int x) { int c = 0; while ((1LL << c) < x) ++c; return c; }

struct World {
  Design des; Data D; Start st; std::vector<std::vector<int>> Nb; int B = 0, L = 0, ell = 0;
  std::vector<std::vector<int>> omega; std::map<std::vector<int>, int> idx;
  std::unique_ptr<Engine> E; ScoreCache cache;
};
static void build_world(World& w, int id) {
  w.des = design_of(id);
  std::vector<double> X, y; make_data(w.des, X, y);
  std::vector<int> orig(w.des.p); for (int j = 0; j < w.des.p; ++j) orig[j] = j + 1;
  data_init(w.D, X.data(), y.data(), w.des.n, w.des.p, orig);
  int n = w.des.n, p = w.des.p;
  w.B = std::min(std::min(isqrt(n), isqrt(p)), 16);
  w.L = std::max(4, ceil_log2(n + 1));
  w.ell = ceil_log2(n + p + 1);
  w.st.D = &w.D; w.st.B = w.B;
  w.st.blocks = make_blocks(w.D, w.B);
  Scorer sc(&w.D); build_tables(w.st, sc); build_start(w.st);
  w.Nb = neighbour_graph(w.D, w.B);
  for (uint32_t mask = 0; mask < (1u << p); ++mask) {
    if (__builtin_popcount(mask) > w.D.K) continue;
    std::vector<int> S; for (int j = 0; j < p; ++j) if (mask & (1u << j)) S.push_back(j);
    w.idx[S] = (int)w.omega.size(); w.omega.push_back(S);
  }
  w.E.reset(new Engine(w.D, w.st, w.Nb, w.B));
  w.cache.init(w.D.W, 1 << 16);
  w.E->cache = &w.cache; w.E->led = nullptr; w.E->guard = nullptr;
}

// ---- exact kernels of the production steps --------------------------------------------------
static Particle particle_of(World& w, const std::vector<int>& S) { Particle P; w.E->set_model(P, S); w.E->eval(P, ME_INIT, false); return P; }
// bisection for the acceptance threshold: accepted(u) is "u < alpha"; returns alpha
// accepted(u) is the production outcome for scripted u; the step's rule is "accept iff u < alpha". Returns hi, the smallest
// tested rejected double, with alpha in (lo, hi] and lo, hi adjacent doubles at exit; g_bracket records the largest
// final bracket width (hi - lo) over all calls. Endpoint cases: accepted at the largest double below 1 -> returns 1 (alpha in
// (1 - 2^-53, 1]); rejected at 0 -> returns 0 (alpha = 0).
static double g_bracket = 0.0;
template <class F> static double threshold(F accepted) {
  double hiu = std::nextafter(1.0, 0.0);
  if (accepted(hiu)) { g_bracket = std::max(g_bracket, 1.0 - hiu); return 1.0; }
  if (!accepted(0.0)) return 0.0;
  double lo = 0.0, hi = hiu;  // accepted(lo), !accepted(hi)
  for (int it = 0; it < 4000 && std::nextafter(lo, 1.0) < hi; ++it) {
    double mid = 0.5 * (lo + hi);
    if (mid <= lo || mid >= hi) mid = std::nextafter(lo, 1.0);
    if (mid >= hi) break;
    if (accepted(mid)) lo = mid; else hi = mid;
  }
  if (std::nextafter(lo, 1.0) < hi) throw std::runtime_error("threshold bisection did not reach adjacent doubles");
  g_bracket = std::max(g_bracket, hi - lo);
  return hi;
}
static double g_gibbs_rb_diff = 0.0; static long g_pi0_zero_width = 0;
static double mid_of(const std::vector<double>& cum, int k) { double a = k == 0 ? 0.0 : cum[k - 1]; return 0.5 * (a + cum[k]); }

// scripted pi0 draw producing target S'; returns production probability of that outcome (product of interval widths)
static double script_pi0(World& w, ScriptVS& vs, const std::vector<int>& T) {
  const Start& st = w.st; int J = st.J;
  int k = (int)T.size();
  std::vector<int> kb(J, 0); std::vector<uint32_t> code(J, 0);
  for (int j : T) { kb[st.blk[j]]++; code[st.blk[j]] |= (1u << st.pos[j]); }
  auto width = [](const std::vector<double>& c, int i) { return c[i] - (i == 0 ? 0.0 : c[i - 1]); };
  double prob = width(st.size_cum, k); vs.push("pi0_size", mid_of(st.size_cum, k));
  int r = k;
  for (int b = J - 1; b >= 0 && r > 0; --b) { prob *= width(st.cond_cum[b][r], kb[b]); vs.push("pi0_block_size", mid_of(st.cond_cum[b][r], kb[b])); r -= kb[b]; }
  for (int b = 0; b < J; ++b) {
    if (kb[b] == 0) continue;
    const auto& cs = st.codes_by_size[b][kb[b]];
    int i = (int)(std::find(cs.begin(), cs.end(), code[b]) - cs.begin());
    prob *= width(st.sub_cum[b][kb[b]], i); vs.push("pi0_submodel", mid_of(st.sub_cum[b][kb[b]], i));
  }
  return prob;
}

// kernel matrices: K[e] is |Omega| x |Omega| row-major; e = 0..p-1 Gibbs j, p uniform swap, p+1 neighbour swap, p+2 indep
static std::vector<std::vector<double>> kernels_at(World& w, double phi, double& max_row_err, double& pi0_mass_err) {
  int p = w.D.p, M = (int)w.omega.size();
  std::vector<std::vector<double>> K(p + 3, std::vector<double>((size_t)M * M, 0.0));
  Engine& E = *w.E; ScriptVS vs; E.vs = &vs;
  max_row_err = 0; pi0_mass_err = 0;
  auto add = [&](int e, int a, const std::vector<int>& S2, double pr) { K[e][(size_t)a * M + w.idx.at(S2)] += pr; };
  for (int a = 0; a < M; ++a) {
    const std::vector<int>& S = w.omega[a];
    Particle P0 = particle_of(w, S);
    int k = (int)S.size();
    // Gibbs j: inclusion probability by bisection on the production step outcome ("j in the new state"); the two
    // possible outcomes are S u {j} and S \ {j}. Cross-check against the production RB recording o_j.
    for (int j = 0; j < p; ++j) {
      std::vector<int> Splus = S, Sminus = S;
      if (std::find(S.begin(), S.end(), j) == S.end()) { Splus.push_back(j); std::sort(Splus.begin(), Splus.end()); }
      else Sminus.erase(std::find(Sminus.begin(), Sminus.end(), j));
      auto incl = [&](double u) { Particle P = P0; vs.clear(); vs.push("gibbs", u); E.step_gibbs(P, j, phi);
                                  if (!vs.all_used()) throw std::runtime_error("gibbs script not consumed");
                                  if (P.S != Splus && P.S != Sminus) throw std::runtime_error("gibbs outcome outside {S+, S-}");
                                  return P.S == Splus && std::find(P.S.begin(), P.S.end(), j) != P.S.end(); };
      double o = threshold(incl);
      E.rb_on = true; E.rb_acc.assign(p, 0.0);
      { Particle P = P0; vs.clear(); vs.push("gibbs", 0.5); E.step_gibbs(P, j, phi); }
      E.rb_on = false; g_gibbs_rb_diff = std::max(g_gibbs_rb_diff, std::fabs(o - E.rb_acc[j]));
      if (o > 0) add(j, a, Splus, o);
      if (o < 1) add(j, a, Sminus, 1.0 - o);
    }
    // uniform swap
    if (k == 0 || k == p) { Particle P = P0; vs.clear(); E.step_uswap(P, phi); add(p, a, P.S, 1.0); }
    else for (int ia = 0; ia < k; ++ia) for (int ib = 0; ib < p - k; ++ib) {
      double uj = (ia + 0.5) / k, ul = (ib + 0.5) / (p - k), pr = 1.0 / ((double)k * (p - k));
      std::vector<int> prop;
      auto acc = [&](double u) { Particle P = P0; vs.clear(); vs.push("uswap_j", uj); vs.push("uswap_l", ul); vs.push("uswap_accept", u);
                                 E.step_uswap(P, phi); if (!vs.all_used()) throw std::runtime_error("uswap script not consumed"); if (P.S != S) prop = P.S; return P.S != S; };
      double al = threshold(acc);
      if (prop.empty()) { Particle P = P0; vs.clear(); vs.push("uswap_j", uj); vs.push("uswap_l", ul); vs.push("uswap_accept", 0.0); E.step_uswap(P, phi); prop = P.S; }
      add(p, a, prop, pr * al); add(p, a, S, pr * (1 - al));
    }
    // neighbour swap (all B labels are the same kernel: step_nswap uses b only for its label)
    if (k == 0) { Particle P = P0; vs.clear(); E.step_nswap(P, phi, 1); add(p + 1, a, P.S, 1.0); }
    else for (int ia = 0; ia < k; ++ia) {
      int j = S[ia]; int c = 0; for (int l : w.Nb[j]) if (std::find(S.begin(), S.end(), l) == S.end()) ++c;
      double uj = (ia + 0.5) / k;
      if (c == 0) { Particle P = P0; vs.clear(); vs.push("nswap_j", uj); E.step_nswap(P, phi, 1); add(p + 1, a, P.S, 1.0 / k); continue; }
      for (int ib = 0; ib < c; ++ib) {
        double ul = (ib + 0.5) / c, pr = 1.0 / ((double)k * c);
        std::vector<int> prop;
        auto acc = [&](double u) { Particle P = P0; vs.clear(); vs.push("nswap_j", uj); vs.push("nswap_l", ul); vs.push("nswap_accept", u);
                                   E.step_nswap(P, phi, 1); if (!vs.all_used()) throw std::runtime_error("nswap script not consumed"); if (P.S != S) prop = P.S; return P.S != S; };
        double al = threshold(acc);
        if (prop.empty()) prop = S;  // alpha = 0 cannot occur (positive scores); guarded
        add(p + 1, a, prop, pr * al); add(p + 1, a, S, pr * (1 - al));
      }
    }
    // independence proposal
    double mass = 0;
    for (int b2 = 0; b2 < M; ++b2) {
      const std::vector<int>& T = w.omega[b2];
      ScriptVS probe; double pr = script_pi0(w, probe, T); mass += pr;
      if (pr == 0) { ++g_pi0_zero_width; continue; }
      if (T == S) {  // self-proposal: the state stays S whatever the acceptance; verify with the production step
        for (double u : {0.0, std::nextafter(1.0, 0.0)}) { Particle P = P0; vs.clear(); vs.q = probe.q; vs.push("indep_accept", u);
          E.step_indep(P, phi); if (P.S != S || !vs.all_used()) throw std::runtime_error("indep self-proposal mismatch"); }
        add(p + 2, a, S, pr); continue;
      }
      auto acc = [&](double u) { Particle P = P0; vs.clear(); vs.q = probe.q; vs.push("indep_accept", u); E.step_indep(P, phi);
                                 if (!vs.all_used()) throw std::runtime_error("indep script not consumed");
                                 if (P.S != S && P.S != T) throw std::runtime_error("pi0 script mismatch"); return P.S == T; };
      double al = threshold(acc);
      add(p + 2, a, T, pr * al); add(p + 2, a, S, pr * (1 - al));
    }
    pi0_mass_err = std::max(pi0_mass_err, std::fabs(mass - 1.0));
    for (int e = 0; e < p + 3; ++e) { double s = 0; for (int b2 = 0; b2 < M; ++b2) s += K[e][(size_t)a * M + b2]; max_row_err = std::max(max_row_err, std::fabs(s - 1)); }
  }
  E.vs = nullptr;
  return K;
}

static void write_bin(const std::string& f, const std::vector<double>& v) {
  FILE* fp = std::fopen(f.c_str(), "wb"); std::fwrite(v.data(), sizeof(double), v.size(), fp); std::fclose(fp);
}

static int mode_export(int id, const std::string& out) {
  World w; build_world(w, id);
  int p = w.D.p, M = (int)w.omega.size();
  // production per-model quantities
  std::ofstream om(out + "/omega.tsv");
  om.precision(17);
  om << "idx\tmask\tsize\tlg0\td\tlogm\tF\tlogpi0_prod\n";
  std::vector<double> lg0v(M), dv(M);
  long pi0_script_failures = 0, pi0_scripts_checked = 0;
  for (int a = 0; a < M; ++a) {
    Particle P = particle_of(w, w.omega[a]);
    uint32_t mask = 0; for (int j : w.omega[a]) mask |= (1u << j);
    ScriptVS probe; double pr = script_pi0(w, probe, w.omega[a]);
    if (pr > 0) {  // validate the script on the production sampler: returned model and full consumption
      ScriptVS run; run.q = probe.q; std::vector<int> got; draw_pi0(w.st, run, got);
      if (got != w.omega[a] || !run.all_used()) ++pi0_script_failures;
      ++pi0_scripts_checked;
    }
    lg0v[a] = P.lg0; dv[a] = P.d;
    om << a << "\t" << mask << "\t" << w.omega[a].size() << "\t" << P.lg0 << "\t" << P.d << "\t" << P.logm << "\t" << P.F << "\t" << std::log(pr) << "\n";
  }
  // pilot-derived grid: production adaptive pilot (stream 0) for the targets, then production build_grid on an ENUMERATED
  // V = top-20p(lg0) u top-20p(lg1) u {empty} ranked over all of Omega (production ranks calibration's scored-model leader
  // stores, v3_core.cpp:706-711, and iterates rebuilds); not the full production calibration path.
  int N0 = std::max(2500, std::max(w.des.n, p)), H0 = (512 * N0 + 2499) / 2500, T0 = std::max(1000, w.ell * w.ell);
  RngSource rng; rng.g.seed_stream(5000 + id, 0); w.E->vs = &rng;
  Engine::Schedule sch; sch.adaptive = true; sch.H = H0; sch.Te = T0;
  IslandResult pil = w.E->run_island_s(0, H0, sch, w.L, 4, 0, nullptr, PH_PILOT, 0);
  w.E->vs = nullptr;
  std::vector<double> targets{0.0}; targets.insert(targets.end(), pil.phi.begin(), pil.phi.end());
  std::vector<int> ord(M); for (int a = 0; a < M; ++a) ord[a] = a;
  std::set<int> Vs{0};
  auto topk = [&](std::function<double(int)> key) {
    std::vector<int> o = ord; std::stable_sort(o.begin(), o.end(), [&](int x, int y2) { return key(x) > key(y2); });
    for (int i = 0; i < std::min(M, 20 * p); ++i) Vs.insert(o[i]);
  };
  topk([&](int a) { return lg0v[a]; }); topk([&](int a) { return lg0v[a] + dv[a]; });
  std::vector<std::vector<int>> Vm; for (int a : Vs) Vm.push_back(w.omega[a]);
  std::sort(Vm.begin(), Vm.end());  // lexicographic, as cpp_cal_V
  std::vector<double> Vl, Vd; for (auto& S : Vm) { int a = w.idx[S]; Vl.push_back(lg0v[a]); Vd.push_back(dv[a]); }
  GridResult g = build_grid(Vl, Vd, targets, T0);
  std::ofstream meta(out + "/meta.txt"); meta.precision(17);
  meta << "id " << id << "\nn " << w.des.n << "\np " << p << "\nK " << w.D.K << "\nB " << w.B << "\nL " << w.L << "\nM " << M
       << "\nkind " << w.des.kind << "\nrho " << w.des.rho << "\nlogm0 " << w.D.logm0 << "\nlogZbar0 " << w.st.logZbar0
       << "\nJ " << w.st.J << "\nH0 " << H0 << "\nT0 " << T0 << "\nV_size " << Vm.size() << "\ngrid_ok " << g.ok << "\ngrid_reason " << g.reason
       << "\npi0_scripts_checked " << pi0_scripts_checked << "\npi0_script_failures " << pi0_script_failures << "\n";
  meta << "S0"; for (int j : w.des.S0) meta << " " << j; meta << "\n";
  meta << "pilot"; for (double t : targets) meta << " " << t; meta << "\n";
  meta << "grid"; for (double t : g.grid) meta << " " << t; meta << "\n";
  meta << "blocks"; for (auto& b : w.st.blocks) { meta << " ["; for (int j : b) meta << j << ","; meta << "]"; } meta << "\n";
  meta << "edges"; for (int j = 0; j < p; ++j) for (int l : w.Nb[j]) if (l > j) meta << " " << j << "-" << l; meta << "\n";
  // kernels at every phi needed: production grid, alternates {0,1} and {0,.5,1}, and 0.5 (negative control)
  std::set<double> phis(g.grid.begin(), g.grid.end()); phis.insert(0.0); phis.insert(0.5); phis.insert(1.0);
  std::ofstream pl(out + "/phis.txt"); pl.precision(17);
  int ip = 0;
  for (double phi : phis) {
    double rerr, merr;
    auto K = kernels_at(w, phi, rerr, merr);
    std::vector<double> flat; for (auto& k : K) flat.insert(flat.end(), k.begin(), k.end());
    write_bin(out + "/K_" + std::to_string(ip) + ".bin", flat);
    pl << ip << " " << phi << " " << rerr << " " << merr << " " << g_bracket << " " << g_gibbs_rb_diff << " " << g_pi0_zero_width << "\n";
    g_bracket = 0; g_gibbs_rb_diff = 0; g_pi0_zero_width = 0;
    std::fprintf(stderr, "design %d phi %.6g row_err %.2e pi0_mass_err %.2e\n", id, phi, rerr, merr);
    ++ip;
  }
  return 0;
}

static int mode_mc(int id, const std::string& out, int N, long reps, const std::string& gridfile, const std::string& tag) {
  World w; build_world(w, id);
  std::vector<double> grid; { std::ifstream gf(gridfile); double x; while (gf >> x) grid.push_back(x); }
  FILE* fp = std::fopen((out + "/mc_" + tag + ".bin").c_str(), "wb");
  std::vector<uint16_t> buf(4 * N);
  Engine& E = *w.E;
  E.measured_hook = [&](const std::vector<Particle>& P, int h) {
    for (int i = 0; i < N; ++i) buf[(h - 1) * N + i] = (uint16_t)w.idx.at(P[i].S);
  };
  double hook_maxdiff = 0;
  for (long r = 0; r < reps; ++r) {
    RngSource rng; rng.g.seed_stream((uint64_t)(70000 + id * 100 + N), (uint64_t)(10 + r)); E.vs = &rng;
    IslandResult res = E.run_island(1, N, grid, w.L, 4, 0, nullptr);
    double lz = res.logZ;
    // hook validation: marginal frequencies from the hook vs the production pip_plain output
    for (int j = 0; j < w.D.p; ++j) {
      double c = 0; for (int t = 0; t < 4 * N; ++t) { const auto& S = w.omega[buf[t]]; if (std::find(S.begin(), S.end(), j) != S.end()) c += 1; }
      hook_maxdiff = std::max(hook_maxdiff, std::fabs(c / (4.0 * N) - res.pip_plain[j]));
    }
    std::fwrite(&lz, sizeof(double), 1, fp); std::fwrite(buf.data(), sizeof(uint16_t), buf.size(), fp);
  }
  std::fclose(fp);
  std::printf("hook_vs_pip_plain_maxdiff %.3e%c", hook_maxdiff, 10);
  return 0;
}

int main(int argc, char** argv) {
  try {
    std::string mode = argv[1];
    if (mode == "export") return mode_export(std::atoi(argv[2]), argv[3]);
    if (mode == "mc") return mode_mc(std::atoi(argv[2]), argv[3], std::atoi(argv[4]), std::atol(argv[5]), argv[6], argv[7]);
  } catch (std::exception& e) { std::fprintf(stderr, "ERROR %s\n", e.what()); return 2; }
  return 1;
}
