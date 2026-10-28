// v3_core.cpp -- Rcpp entry points of the SMC-BVS v3 core layer (CORE_SPEC v2 §§1-9). Compiled by v3.R with
// Rcpp::sourceCpp; the headers in this directory hold the algorithm, this file only converts between R and C++.
#include <Rcpp.h>
#include <memory>
#include <fstream>
#include "v3_engine.h"

using namespace Rcpp;
using namespace v3;

// One holder type for contexts, starts and setups; pieces not yet built are empty.
struct Holder {
  std::shared_ptr<Data> D;
  std::shared_ptr<Start> st;
  std::vector<std::vector<int>> Nb;
  int B = 0;
  bool has_start = false, has_graph = false;
  double table_seconds = 0, block_seconds = 0, start_seconds = 0, graph_seconds = 0;
};
typedef XPtr<Holder> HPtr;

// Name of element i of a list; lists may be unnamed or partly named (CORE_SPEC §8: every observer part optional).
static std::string elem_name(List l, int i, const std::string& prefix) {
  SEXP nm = l.attr("names");
  if (!Rf_isNull(nm)) { std::string s = CHAR(STRING_ELT(nm, i)); if (!s.empty()) return s; }
  return prefix + std::to_string(i + 1);
}

static HPtr get_holder(SEXP x) {
  if (TYPEOF(x) == EXTPTRSXP) return HPtr(x);
  List l(x);
  if (l.containsElementNamed("ptr")) return HPtr((SEXP)l["ptr"]);
  stop("object has no C++ pointer (ptr)");
}

// ---------------------------------------------------------------------------------------------
// Index conversion: R level = sorted 1-based original indices (R12); C++ level = sorted 0-based internal indices.
// ---------------------------------------------------------------------------------------------
static std::vector<int> to_internal(const Data& D, SEXP Sx) {
  std::vector<int> out;
  if (Rf_isNull(Sx)) return out;
  IntegerVector S(Sx);
  for (int v : S) {
    if (v == NA_INTEGER) stop("model contains NA");
    auto it = std::lower_bound(D.orig.begin(), D.orig.end(), v);
    if (it == D.orig.end() || *it != v) stop("index %d is not a retained original column index", v);
    out.push_back((int)(it - D.orig.begin()));
  }
  std::sort(out.begin(), out.end());
  if (std::adjacent_find(out.begin(), out.end()) != out.end()) stop("model has duplicated indices");
  return out;
}
static IntegerVector to_orig(const Data& D, const std::vector<int>& S) {
  IntegerVector o(S.size());
  for (size_t i = 0; i < S.size(); ++i) o[i] = D.orig[S[i]];
  return o;
}
static List models_to_list(const Data& D, const std::vector<std::vector<int>>& Ms) {
  List L(Ms.size());
  for (size_t i = 0; i < Ms.size(); ++i) L[i] = to_orig(D, Ms[i]);
  return L;
}
static List event_to_list(const EventCtx& e, int mech) {
  return List::create(_["phase"] = phase_name(e.phase), _["mechanism"] = mech >= 0 ? mech_name(mech) : "none",
                      _["tier"] = e.tier, _["island"] = e.island, _["stage"] = e.stage, _["round"] = e.round,
                      _["particle"] = e.particle, _["position"] = e.position, _["phi"] = e.phi, _["iter"] = e.iter);
}
static std::string hex64(uint64_t x) { char b[17]; snprintf(b, sizeof b, "%016llx", (unsigned long long)x); return b; }
static int phase_index(const std::string& s) { for (int a = 0; a < N_PHASE; ++a) if (s == phase_name(a)) return a; stop("unknown phase %s", s); }
static int mech_index(const std::string& s) { for (int a = 0; a < N_MECH; ++a) if (s == mech_name(a)) return a; stop("unknown mechanism %s", s); }
static NumericMatrix counter_matrix(const uint64_t c[N_PHASE][N_MECH]) {
  NumericMatrix M(N_PHASE, N_MECH);
  CharacterVector rn(N_PHASE), cn(N_MECH);
  for (int a = 0; a < N_PHASE; ++a) { rn[a] = phase_name(a); for (int b = 0; b < N_MECH; ++b) M(a, b) = (double)c[a][b]; }
  for (int b = 0; b < N_MECH; ++b) cn[b] = mech_name(b);
  M.attr("dimnames") = List::create(rn, cn);
  return M;
}

// ---------------------------------------------------------------------------------------------
// Budgets (M §3, §6.2): exact-branch count with saturating 128-bit arithmetic.
// ---------------------------------------------------------------------------------------------
// [[Rcpp::export]]
List cpp_exact_count(double n_, double p_, double N0, double H0) {
  long long n = (long long)n_, p = (long long)p_;
  long long K = std::min(p, n / 2);
  unsigned __int128 thr = (unsigned __int128)(5 * (long long)H0 + 4 * (long long)N0) * (unsigned __int128)p;
  unsigned __int128 sum = 0, c = 1;  // C(p, 0)
  bool saturated = false;
  for (long long k = 0; k <= K; ++k) {
    if (k > 0) c = c * (unsigned __int128)(p - k + 1) / (unsigned __int128)k;  // exact: C(p,k) = C(p,k-1)(p-k+1)/k
    sum += c;
    if (sum > thr) { saturated = true; break; }  // saturate: the count only needs comparing with the threshold
  }
  double sum_d = saturated ? (double)thr + 1.0 : (double)sum;
  return List::create(_["count"] = sum_d, _["saturated"] = saturated, _["threshold"] = (double)thr, _["exact_branch"] = !saturated);
}

// ---------------------------------------------------------------------------------------------
// Context and scorer (CORE_SPEC §2)
// ---------------------------------------------------------------------------------------------
// [[Rcpp::export]]
List cpp_context(NumericMatrix X, NumericVector y, IntegerVector orig, List hooks, bool return_gram) {
  int n = X.nrow(), p = X.ncol();
  std::vector<int> o(orig.begin(), orig.end());
  Holder* h = new Holder();
  h->D = std::make_shared<Data>();
  data_init(*h->D, X.begin(), y.begin(), n, p, o);
  if (hooks.containsElementNamed("fail_min_size")) h->D->fail_min_size = as<int>(hooks["fail_min_size"]);
  if (hooks.containsElementNamed("fail_routes")) {
    CharacterVector fr = hooks["fail_routes"];
    for (auto s : fr) {
      std::string r = as<std::string>(s);
      if (r == "chol") h->D->fail_chol = true; else if (r == "chol_refactor") h->D->fail_refactor = true; else if (r == "qr") h->D->fail_qr = true;
      else stop("unknown route in hooks$fail_routes: %s", r);
    }
  }
  HPtr ptr(h, true);
  const Data& D = *h->D;
  // The p x p Gram is copied to R only on request (code review D-1: a second dense p x p matrix at large p).
  SEXP G = R_NilValue;
  if (return_gram) { NumericMatrix Gm(p, p); std::copy(D.G.begin(), D.G.end(), Gm.begin()); G = Gm; }
  return List::create(_["ptr"] = ptr, _["G"] = G, _["z"] = NumericVector(D.z.begin(), D.z.end()), _["yty"] = D.yty,
                      _["n"] = n, _["p"] = p, _["K"] = D.K, _["log_Cn"] = D.logCn, _["log_W_K"] = D.logWK,
                      _["log_w"] = NumericVector(D.logw.begin(), D.logw.end()), _["log_m0"] = D.logm0, _["nu"] = D.nu,
                      _["orig"] = orig);
}

// [[Rcpp::export]]
List cpp_score(SEXP ctx, SEXP S) {
  HPtr h = get_holder(ctx); const Data& D = *h->D;
  std::vector<int> s = to_internal(D, S);
  if ((int)s.size() > D.K) stop("v3_score: |S| = %d > K = %d (infeasible model; callers never pass these, R1)", (int)s.size(), D.K);
  Scorer sc(&D);
  ScoreOut o;
  try { o = sc.score(s); } catch (NumericalFailure& e) { return List::create(_["status"] = "numerical_failure", _["message"] = e.what()); }
  double lp = D.logprior[s.size()];
  return List::create(_["log_m"] = o.logm, _["log_prior"] = lp, _["F"] = lp + o.logm, _["log_BF"] = o.logm - D.logm0,
                      _["Q"] = o.Q, _["route"] = route_name(o.route), _["q_recomputed"] = o.q_recomputed,
                      _["error_bound"] = sc.error_bound(o, (int)s.size()),
                      _["error_bound_kind"] = "heuristic_condition_estimate");
}

// [[Rcpp::export]]
NumericVector cpp_time_scores(SEXP ctx, int k, int reps) {
  HPtr h = get_holder(ctx); const Data& D = *h->D;
  k = std::max(0, std::min(k, D.K));
  Scorer sc(&D); std::vector<int> S;
  auto t0 = Clock::now(); double sink = 0;
  for (int r = 0; r < reps; ++r) {
    S.clear(); for (int a = 0; a < k; ++a) S.push_back((r + a * 7) % D.p);
    std::sort(S.begin(), S.end()); S.erase(std::unique(S.begin(), S.end()), S.end());
    try { sink += sc.score(S).logm; } catch (NumericalFailure&) { }  // preflight timing only; failures surface in the run
  }
  double s = secs_since(t0) / std::max(1, reps);
  return NumericVector::create(_["seconds_per_score"] = s, _["sink"] = sink);
}

// ---------------------------------------------------------------------------------------------
// Blocks, tables, start, neighbour graph (CORE_SPEC §3)
// ---------------------------------------------------------------------------------------------
static List blocks_to_R(const Data& D, const std::vector<std::vector<int>>& blocks) { return models_to_list(D, blocks); }
// Block width supported by the table codes (uint32 bit codes; 2^B entries per block): 1 <= B <= 20 (code review R-6).
static const int B_MAX = 20;
static void check_B(int B) { if (B < 1 || B > B_MAX) stop("block size B = %d outside the supported range 1..%d", B, B_MAX); }
static void check_blocks(const std::vector<std::vector<int>>& bl) {
  for (auto& b : bl) if (b.empty() || (int)b.size() > B_MAX) stop("a block has %d members (supported 1..%d)", (int)b.size(), B_MAX);
}
static std::vector<std::vector<int>> blocks_from_R(const Data& D, List bl) {
  std::vector<std::vector<int>> out;
  for (int b = 0; b < bl.size(); ++b) out.push_back(to_internal(D, bl[b]));
  return out;
}

// [[Rcpp::export]]
List cpp_blocks(SEXP ctx, int B) {
  HPtr h = get_holder(ctx); const Data& D = *h->D;
  check_B(B);
  Dendrogram T;
  auto blocks = make_blocks(D, B, &T);
  int p = D.p;
  // dendrogram for inspection: merges (node ids: leaves = -orig index as in hclust, internal = merge step)
  IntegerMatrix merge(std::max(p - 1, 0), 2); NumericVector height(std::max(p - 1, 0));
  for (int s = 0; s < p - 1; ++s) {
    int nn = p + s;
    auto conv = [&](int x) { return x < p ? -D.orig[x] : (x - p + 1); };
    merge(s, 0) = conv(T.left[nn]); merge(s, 1) = conv(T.right[nn]); height[s] = T.height[nn];
  }
  std::vector<int> leaves = subtree_leaves(T, T.root, p);
  return List::create(_["blocks"] = blocks_to_R(D, blocks), _["merge"] = merge, _["height"] = height,
                      _["leaf_order"] = to_orig(D, leaves));
}

// [[Rcpp::export]]
List cpp_tables(SEXP ctx, List blocks_R) {
  HPtr h = get_holder(ctx); const Data& D = *h->D;
  Start st; st.D = &D; st.blocks = blocks_from_R(D, blocks_R);
  check_blocks(st.blocks);
  Scorer sc(&D);
  build_tables(st, sc);
  List out(st.J);
  for (int b = 0; b < st.J; ++b) {
    CharacterVector rt(st.route_tab[b].size());
    for (size_t c = 0; c < rt.size(); ++c) rt[c] = st.route_tab[b][c] < 0 ? NA_STRING : Rf_mkChar(route_name(st.route_tab[b][c]));
    out[b] = List::create(_["members"] = to_orig(D, st.blocks[b]),
                          _["log_r"] = NumericVector(st.logr[b].begin(), st.logr[b].end()),
                          _["log_m"] = NumericVector(st.logm_tab[b].begin(), st.logm_tab[b].end()), _["route"] = rt);
  }
  return out;
}

static List start_summary(const Holder& h) {
  const Start& st = *h.st;
  List prof(st.J), logF(st.J + 1);
  for (int b = 0; b < st.J; ++b) prof[b] = NumericVector(st.logprof[b].begin(), st.logprof[b].end());
  for (int b = 0; b <= st.J; ++b) logF[b] = NumericVector(st.logF[b].begin(), st.logF[b].end());
  return List::create(_["log_Zbar0"] = st.logZbar0, _["log_profiles"] = prof, _["log_F"] = logF,
                      _["size_log_mass"] = NumericVector(st.size_logmass.begin(), st.size_logmass.end()));
}

// v3_start(ctx, blocks, tables): builds pi_0 from supplied blocks and table values (no re-scoring).
// [[Rcpp::export]]
List cpp_start(SEXP ctx, List blocks_R, List tables_R) {
  HPtr h = get_holder(ctx);
  Holder* g = new Holder(); g->D = h->D;
  g->st = std::make_shared<Start>(); Start& st = *g->st; st.D = g->D.get();
  st.blocks = blocks_from_R(*g->D, blocks_R); st.J = (int)st.blocks.size();
  try { check_blocks(st.blocks); } catch (...) { delete g; throw; }
  st.blk.assign(g->D->p, -1); st.pos.assign(g->D->p, -1);
  for (int b = 0; b < st.J; ++b) for (size_t i = 0; i < st.blocks[b].size(); ++i) { st.blk[st.blocks[b][i]] = b; st.pos[st.blocks[b][i]] = (int)i; }
  for (int j = 0; j < g->D->p; ++j) if (st.blk[j] < 0) stop("blocks do not cover every column");
  if (tables_R.size() != st.J) stop("v3_start: %d tables for %d blocks", (int)tables_R.size(), st.J);
  for (int b = 0; b < st.J; ++b) {
    List tb = tables_R[b];
    NumericVector lr = tb["log_r"]; NumericVector lm = tb["log_m"];
    // the table must belong to block b (code review R-5): same members, 2^|C_b| entries
    if (to_internal(*g->D, tb["members"]) != st.blocks[b]) stop("v3_start: table %d does not belong to block %d (members differ)", b + 1, b + 1);
    if (lr.size() != ((R_xlen_t)1 << st.blocks[b].size()) || lm.size() != lr.size()) stop("v3_start: table %d has the wrong length", b + 1);
    st.logr.push_back(std::vector<double>(lr.begin(), lr.end()));
    st.logm_tab.push_back(std::vector<double>(lm.begin(), lm.end()));
    st.route_tab.push_back(std::vector<int>(lr.size(), 0));
  }
  build_start(st);
  g->has_start = true;
  HPtr ptr(g, true);
  List s = start_summary(*g); s["ptr"] = ptr;
  return s;
}

// [[Rcpp::export]]
double cpp_start_logmass(SEXP start, SEXP S) {
  HPtr h = get_holder(start); if (!h->has_start) stop("object has no start");
  std::vector<int> s = to_internal(*h->D, S);
  if ((int)s.size() > h->D->K) return R_NegInf;
  return h->st->log_pi0(s);
}
// [[Rcpp::export]]
List cpp_start_draw(SEXP start, int N, double seed, double stream, bool as_key) {
  HPtr h = get_holder(start); if (!h->has_start) stop("object has no start");
  RngSource rng; rng.g.seed_stream((uint64_t)seed, (uint64_t)stream);
  std::vector<int> S;
  if (as_key) {
    CharacterVector keys(N);
    for (int i = 0; i < N; ++i) { draw_pi0(*h->st, rng, S); keys[i] = join_idx(S, h->D->orig); }
    return List::create(_["keys"] = keys);
  }
  List out(N);
  for (int i = 0; i < N; ++i) { draw_pi0(*h->st, rng, S); out[i] = to_orig(*h->D, S); }
  return List::create(_["models"] = out);
}
// [[Rcpp::export]]
List cpp_start_mode(SEXP start) {
  HPtr h = get_holder(start); if (!h->has_start) stop("object has no start");
  ModeResult m = start_mode(*h->st);
  return List::create(_["model"] = to_orig(*h->D, m.S), _["log_gamma0"] = m.lg0, _["log_pi0"] = m.lg0 - h->st->logZbar0,
                      _["log_1m_pi0"] = log1mexp_v3(m.lg0 - h->st->logZbar0),
                      _["n_tied_sets"] = (double)m.ties, _["tie_enumeration_truncated"] = m.truncated);
}
// [[Rcpp::export]]
List cpp_discrepancy(SEXP start, SEXP S) {
  HPtr h = get_holder(start); if (!h->has_start) stop("object has no start");
  const Data& D = *h->D;
  std::vector<int> s = to_internal(D, S);
  if ((int)s.size() > D.K) stop("infeasible model");
  Scorer sc(&D); ScoreOut o = sc.score(s);
  double c = h->st->comp(s);
  return List::create(_["d"] = (o.logm - D.logm0) - c, _["log_BF"] = o.logm - D.logm0, _["log_composite"] = c,
                      _["log_gamma0"] = D.logprior[s.size()] + c, _["log_pi0"] = D.logprior[s.size()] + c - h->st->logZbar0);
}
// [[Rcpp::export]]
List cpp_neighbours(SEXP ctx, int B) {
  HPtr h = get_holder(ctx); const Data& D = *h->D;
  auto N = neighbour_graph(D, B);
  return models_to_list(D, N);
}

// v3_setup: blocks, tables (scored once, R2), start, neighbour graph in one C++ object.
// [[Rcpp::export]]
List cpp_setup(SEXP ctx, int B) {
  HPtr h = get_holder(ctx);
  check_B(B);
  Holder* g = new Holder(); g->D = h->D; g->B = B;
  const Data& D = *g->D;
  g->st = std::make_shared<Start>(); Start& st = *g->st; st.D = &D; st.B = B;
  auto t0 = Clock::now();
  st.blocks = make_blocks(D, B);
  g->block_seconds = secs_since(t0); t0 = Clock::now();
  Scorer sc(&D);
  try {
    build_tables(st, sc);
  } catch (NumericalFailure& e) {
    // M §2 numerical_failure: return the best table model scored so far (HPM order), labelled incomplete.
    std::vector<int> bestS, U; double bestF = NEG_INF; bool have = false;
    for (int b = 0; b < (int)st.logm_tab.size(); ++b)
      for (uint32_t c = 0; c < st.logm_tab[b].size(); ++c) {
        if (std::isnan(st.logm_tab[b][c])) continue;
        U.clear(); for (size_t i = 0; i < st.blocks[b].size(); ++i) if (c & (1u << i)) U.push_back(st.blocks[b][i]);
        double F = D.logprior[U.size()] + st.logm_tab[b][c];
        if (!have || hpm_better(F, U, bestF, bestS)) { bestS = U; bestF = F; have = true; }
      }
    List fail = List::create(_["status"] = "numerical_failure", _["message"] = e.what(), _["hpm"] = to_orig(D, bestS), _["hpm_F"] = bestF,
                             _["hpm_provenance"] = List::create(_["phase"] = "table", _["mechanism"] = "table"));
    delete g;
    return fail;
  }
  g->table_seconds = secs_since(t0); t0 = Clock::now();
  build_start(st);
  g->start_seconds = secs_since(t0); t0 = Clock::now();
  g->Nb = neighbour_graph(D, B);
  g->graph_seconds = secs_since(t0);
  g->has_start = true; g->has_graph = true;
  HPtr ptr(g, true);
  List tables(st.J);
  for (int b = 0; b < st.J; ++b) {
    CharacterVector rt(st.route_tab[b].size());
    for (size_t c = 0; c < rt.size(); ++c) rt[c] = st.route_tab[b][c] < 0 ? NA_STRING : Rf_mkChar(route_name(st.route_tab[b][c]));
    tables[b] = List::create(_["members"] = to_orig(D, st.blocks[b]), _["log_r"] = NumericVector(st.logr[b].begin(), st.logr[b].end()),
                             _["log_m"] = NumericVector(st.logm_tab[b].begin(), st.logm_tab[b].end()), _["route"] = rt);
  }
  List s = start_summary(*g);
  return List::create(_["status"] = "ok", _["ptr"] = ptr, _["B"] = B, _["blocks"] = blocks_to_R(D, st.blocks), _["tables"] = tables,
                      _["start"] = s, _["neighbours"] = models_to_list(D, g->Nb),
                      _["seconds"] = NumericVector::create(_["blocks"] = g->block_seconds, _["tables"] = g->table_seconds,
                                                           _["start"] = g->start_seconds, _["neighbours"] = g->graph_seconds));
}

// ---------------------------------------------------------------------------------------------
// Observer start quantities (CORE_SPEC §8.1), observer scorer only (R11).
// ---------------------------------------------------------------------------------------------
static uint32_t block_code(const Start& st, int b, const std::vector<int>& S) {
  uint32_t c = 0; for (int j : S) if (st.blk[j] == b) c |= (1u << st.pos[j]); return c;
}
// AGG (00_COMMON) q, e and T22's u_n and delta_comp for a feasible reference S0; all in log space from the tables.
static List agg_quantities(const Holder& h, const std::vector<int>& S0) {
  const Data& D = *h.D; const Start& st = *h.st;
  int p = D.p, s = (int)S0.size(), J = st.J;
  // log q
  double logq_sum = NEG_INF;
  std::vector<double> logDb(J, NEG_INF);
  for (int b = 0; b < J; ++b) {
    int m = (int)st.blocks[b].size(); uint32_t ub = block_code(st, b, S0); int nub = __builtin_popcount(ub);
    std::vector<std::vector<double>> terms(m + 1);
    for (uint32_t c = 0; c < (1u << m); ++c) {
      if ((c & ub) != ub) continue;
      int j = __builtin_popcount(c) - nub; if (j < 1) continue;
      double v = st.logr[b][c]; if (std::isnan(v)) continue;
      terms[j].push_back(v - st.logr[b][ub]);
    }
    for (int j = 1; j <= m; ++j) {
      if (terms[j].empty()) continue;
      double la = log_sum_exp(terms[j]);                                   // log a_bj
      double v = (std::lgamma(j + 1.0) + la) / j;                          // log (j! a_bj)^{1/j}
      if (v > logDb[b]) logDb[b] = v;
    }
    logq_sum = log_add(logq_sum, logDb[b]);
  }
  double q = (s == p) ? 0.0 : std::exp(logq_sum - std::log((double)(p - s)));
  // log e
  double loge = NEG_INF;
  if (s > 0) {
    for (int b = 0; b < J; ++b) {
      int m = (int)st.blocks[b].size(); uint32_t ub = block_code(st, b, S0);
      for (uint32_t c = 0; c < (1u << m); ++c) {
        int a = __builtin_popcount(ub & ~c); if (a == 0) continue;
        double v1 = st.logr[b][c], v2 = st.logr[b][c | ub]; if (std::isnan(v1) || std::isnan(v2)) continue;
        loge = std::max(loge, (v1 - v2) / a);
      }
    }
    loge += std::log(2.0 * p);
  }
  double e = (s == 0) ? 0.0 : std::exp(loge);
  // u_n
  double logu_sum = NEG_INF;
  std::vector<char> inS(p, 0); for (int j : S0) inS[j] = 1;
  for (int l = 0; l < p; ++l) {
    if (inS[l]) continue;
    int b = st.blk[l], m = (int)st.blocks[b].size(); uint32_t ub = block_code(st, b, S0), lb = 1u << st.pos[l];
    double mx = NEG_INF;
    for (uint32_t c = 0; c < (1u << m); ++c) {
      if ((c & ub) != ub || (c & lb)) continue;
      double v1 = st.logr[b][c | lb], v0 = st.logr[b][c]; if (std::isnan(v1) || std::isnan(v0)) continue;
      mx = std::max(mx, v1 - v0);
    }
    logu_sum = log_add(logu_sum, mx);
  }
  double u = (s == p) ? 0.0 : std::exp(logu_sum - std::log((double)(p - s)));
  // delta_comp (exact when <= 3 blocks meet S0): DP over (|T|, |S0 \ T|) of the meeting blocks; uncapped w(k).
  std::vector<int> meet; for (int b = 0; b < J; ++b) if (block_code(st, b, S0)) meet.push_back(b);
  double logdelta = NA_REAL; bool delta_exact = false;
  if (s == 0) { logdelta = R_NegInf; delta_exact = true; }
  else if (meet.size() <= 3) {
    std::map<std::pair<int,int>, double> acc; acc[{0, 0}] = 0.0;
    for (int b : meet) {
      int m = (int)st.blocks[b].size(); uint32_t ub = block_code(st, b, S0);
      std::map<std::pair<int,int>, double> loc;
      for (uint32_t c = 0; c < (1u << m); ++c) {
        double v1 = st.logr[b][c], v2 = st.logr[b][c | ub]; if (std::isnan(v1) || std::isnan(v2)) continue;
        std::pair<int,int> key{__builtin_popcount(c), __builtin_popcount(ub & ~c)};
        auto it = loc.find(key); double v = v1 - v2;
        if (it == loc.end() || v > it->second) loc[key] = v;
      }
      std::map<std::pair<int,int>, double> nx;
      for (auto& x : acc) for (auto& y : loc) {
        std::pair<int,int> key{x.first.first + y.first.first, x.first.second + y.first.second};
        double v = x.second + y.second; auto it = nx.find(key);
        if (it == nx.end() || v > it->second) nx[key] = v;
      }
      acc.swap(nx);
    }
    auto logw_unc = [&](int k) { return -M_LN2 - lchoose_d(2.0 * p - 1.0, k); };
    double best = NEG_INF;
    for (auto& x : acc) { int t = x.first.first, a = x.first.second; if (a < 1) continue; best = std::max(best, logw_unc(t) - logw_unc(t + a) + x.second); }
    logdelta = best; delta_exact = true;
  }
  return List::create(_["q"] = q, _["log_q"] = (s == p) ? R_NegInf : logq_sum - std::log((double)(p - s)),
                      _["e"] = e, _["log_e"] = (s == 0) ? R_NegInf : loge, _["u_n"] = u,
                      _["log_u_n"] = (s == p) ? R_NegInf : logu_sum - std::log((double)(p - s)),
                      _["delta_comp"] = delta_exact ? std::exp(logdelta) : NA_REAL, _["log_delta_comp"] = logdelta,
                      _["n_blocks_meeting"] = (int)meet.size(), _["log_D_b"] = NumericVector(logDb.begin(), logDb.end()));
}

// [[Rcpp::export]]
List cpp_observer_start(SEXP setup, List watch, SEXP truth, List chains) {
  HPtr h = get_holder(setup); const Data& D = *h->D; const Start& st = *h->st;
  Scorer osc(&D);  // the observer scorer (R11): separate instance, no cache, no ledger
  CharacterVector nm(watch.size());
  for (int i = 0; i < watch.size(); ++i) nm[i] = elem_name(watch, i, "watch");
  List per(watch.size());
  for (int i = 0; i < watch.size(); ++i) {
    std::vector<int> S = to_internal(D, watch[i]);
    if ((int)S.size() > D.K) { per[i] = List::create(_["feasible"] = false); continue; }
    ScoreOut o = osc.score(S);
    double c = st.comp(S), lg0 = D.logprior[S.size()] + c;
    IntegerVector blocks(S.size()); for (size_t a = 0; a < S.size(); ++a) blocks[a] = st.blk[S[a]] + 1;
    per[i] = List::create(_["model"] = to_orig(D, S), _["feasible"] = true, _["log_pi0"] = lg0 - st.logZbar0,
                          _["log_1m_pi0"] = log1mexp_v3(lg0 - st.logZbar0), _["log_gamma0"] = lg0,
                          _["d"] = (o.logm - D.logm0) - c, _["F"] = D.logprior[S.size()] + o.logm, _["block_of_each"] = blocks);
  }
  per.attr("names") = nm;
  List res = List::create(_["watched"] = per);
  if (!Rf_isNull(truth) && (int)to_internal(D, truth).size() > D.K) {
    res["truth_feasible"] = false;   // |S0| > K: AGG/T22 quantities and o_j(S0, 1) not defined (review R-3)
  } else if (!Rf_isNull(truth)) {
    res["truth_feasible"] = true;
    std::vector<int> S0 = to_internal(D, truth);
    IntegerVector blk(S0.size()); for (size_t a = 0; a < S0.size(); ++a) blk[a] = st.blk[S0[a]] + 1;
    res["truth_blocks"] = blk;
    res["truth_agg"] = agg_quantities(*h, S0);
    // max_j |o_j(S0, 1) - 1{j in S0}| with the observer scorer (§8.4)
    double mx = 0; std::vector<char> in(D.p, 0); for (int j : S0) in[j] = 1;
    NumericVector oj(D.p);
    for (int j = 0; j < D.p; ++j) {
      std::vector<int> W = S0, Wo = S0;
      if (in[j]) sorted_erase(Wo, j); else sorted_insert(W, j);
      double o;
      if ((int)W.size() > D.K) o = 0.0;
      else {
        double lw = D.logprior[W.size()] + osc.score(W).logm, lo = D.logprior[Wo.size()] + osc.score(Wo).logm;  // gamma_1 ratio
        o = plogis_log(lw - lo);
      }
      oj[j] = o; mx = std::max(mx, std::fabs(o - (in[j] ? 1.0 : 0.0)));
    }
    res["o_truth_phi1"] = oj; res["max_oj_dev_truth"] = mx;
  }
  List ch(chains.size());
  for (int c = 0; c < chains.size(); ++c) {
    List chain = chains[c];
    std::vector<std::vector<int>> Ms; for (int i = 0; i < chain.size(); ++i) Ms.push_back(to_internal(D, chain[i]));
    bool feas = true; for (auto& S : Ms) if ((int)S.size() > D.K) feas = false;
    if (!feas) { ch[c] = List::create(_["feasible"] = false); continue; }   // a chain model with |S| > K (review R-4)
    NumericVector tab(Ms.size() > 0 ? Ms.size() - 1 : 0), pri(Ms.size() > 0 ? Ms.size() - 1 : 0);
    for (size_t i = 0; i + 1 < Ms.size(); ++i) {
      tab[i] = st.comp(Ms[i + 1]) - st.comp(Ms[i]);
      pri[i] = D.logprior[Ms[i + 1].size()] - D.logprior[Ms[i].size()];
    }
    ch[c] = List::create(_["feasible"] = true, _["table_log_ratio"] = tab, _["prior_log_ratio"] = pri,
                         _["log_pi0_first"] = Ms.empty() ? NA_REAL : st.log_pi0(Ms[0]));
  }
  res["chains"] = ch;
  return res;
}

// ---------------------------------------------------------------------------------------------
// Observer output
// ---------------------------------------------------------------------------------------------
Rcpp::List v3::Observer::to_list() const {
  int nt = ntargets();
  CharacterVector tname(nt);
  for (int t = 0; t < nt; ++t) tname[t] = t < (int)wm.size() ? wm[t].name : ws[t - wm.size()].name;
  List models(wm.size());
  CharacterVector mn(wm.size());
  for (size_t i = 0; i < wm.size(); ++i) {
    const WModel& w = wm[i]; mn[i] = w.name;
    NumericVector cnt(w.cnt.begin(), w.cnt.end());
    cnt.attr("dim") = IntegerVector::create(R + 1, N_MECH, N_PHASE);  // [island 0..R, mech, phase]
    NumericMatrix on(N_PHASE, N_MECH), oh(N_PHASE, N_MECH);
    for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) { on(a, b) = w.opp_n[a][b]; oh(a, b) = w.opp_h[a][b]; }
    CharacterVector rn(N_PHASE), cn(N_MECH);
    for (int a = 0; a < N_PHASE; ++a) rn[a] = phase_name(a);
    for (int b = 0; b < N_MECH; ++b) cn[b] = mech_name(b);
    on.attr("dimnames") = List::create(rn, cn); oh.attr("dimnames") = List::create(rn, cn);
    models[i] = List::create(_["model"] = to_orig(*D, w.S), _["log_pi0"] = w.logpi0, _["found"] = w.found,
                             _["first_score"] = w.found ? event_to_list(w.first, w.first_mech) : List(),
                             _["counts_island_mech_phase"] = cnt, _["final_iid_hit"] = w.final_iid_hit,
                             _["final_iid_count"] = (double)w.final_iid_count,
                             _["opportunities_before_first_score"] = on, _["hazard_before_first_score"] = oh);
  }
  models.attr("names") = mn;
  CharacterVector wsn(ws.size()); for (size_t s = 0; s < ws.size(); ++s) wsn[s] = ws[s].name;
  auto tn = [&](const std::vector<int>& v) { CharacterVector o(v.size()); for (size_t i = 0; i < v.size(); ++i) o[i] = tname[v[i]]; return o; };
  auto pn = [&](const std::vector<int>& v) { CharacterVector o(v.size()); for (size_t i = 0; i < v.size(); ++i) o[i] = phase_name(v[i]); return o; };
  CharacterVector when(so_when.size()); for (size_t i = 0; i < so_when.size(); ++i) when[i] = so_when[i] == 0 ? "after_resample" : "after_move";
  DataFrame stage_occ = DataFrame::create(_["phase"] = pn(so_phase), _["tier"] = so_tier, _["iter"] = so_iter, _["island"] = so_island,
                                          _["stage"] = so_stage, _["when"] = when, _["target"] = tn(so_target),
                                          _["count"] = so_count, _["stringsAsFactors"] = false);
  DataFrame round_occ = DataFrame::create(_["tier"] = ro_tier, _["iter"] = ro_iter, _["island"] = ro_island, _["phase"] = pn(ro_phase),
                                          _["stage"] = ro_stage, _["round"] = ro_round,
                                          _["target"] = tn(ro_target), _["occ_start"] = ro_occ_start, _["occ_end"] = ro_occ_end,
                                          _["in_in"] = ro_ii, _["in_out"] = ro_io, _["out_in"] = ro_oi, _["out_out"] = ro_oo,
                                          _["stringsAsFactors"] = false);
  NumericMatrix ex(se_cnt.size(), N_MECH);
  for (size_t i = 0; i < se_cnt.size(); ++i) for (int b = 0; b < N_MECH; ++b) ex(i, b) = (double)se_cnt[i][b];
  CharacterVector cn(N_MECH); for (int b = 0; b < N_MECH; ++b) cn[b] = mech_name(b);
  ex.attr("dimnames") = List::create(R_NilValue, cn);
  CharacterVector sname(se_set.size()); for (size_t i = 0; i < se_set.size(); ++i) sname[i] = ws[se_set[i]].name;
  LogicalVector before(se_phase.size());
  for (size_t i = 0; i < se_phase.size(); ++i) before[i] = se_phase[i] == PH_FINAL_BRIDGE && se_stage[i] < T_last;
  List set_exits = List::create(_["tier"] = se_tier, _["iter"] = se_iter, _["island"] = se_island, _["phase"] = pn(se_phase),
                                _["stage"] = se_stage, _["round"] = se_round,
                                _["set"] = sname, _["before_last_weight"] = before, _["first_exits_by_mechanism"] = ex);
  List prefix;
  if (truth_idx >= 0) {
    NumericMatrix bad(R, D->p), frac(R, D->p);
    NumericVector maxfrac(R);
    for (int r = 1; r <= R; ++r) {
      double mx = 0;
      for (int j = 0; j < D->p; ++j) {
        bad(r - 1, j) = rb_bad[r][j];
        frac(r - 1, j) = rb_tot[r][j] > 0 ? rb_bad[r][j] / rb_tot[r][j] : NA_REAL;
        if (rb_tot[r][j] > 0) mx = std::max(mx, frac(r - 1, j));
      }
      maxfrac[r - 1] = mx;
    }
    // island average B-bar_r over the measured rounds
    NumericVector bbar(R, 0.0); std::vector<int> cntr(R, 0);
    for (size_t i = 0; i < pf_island.size(); ++i) { bbar[pf_island[i] - 1] += pf_Bbar[i]; cntr[pf_island[i] - 1]++; }
    for (int r = 0; r < R; ++r) bbar[r] = cntr[r] ? bbar[r] / cntr[r] : NA_REAL;
    prefix = List::create(_["per_round"] = DataFrame::create(_["island"] = pf_island, _["round"] = pf_round, _["B_bar"] = pf_Bbar),
                          _["B_bar_island"] = bbar, _["rb_offtruth_fraction"] = frac, _["rb_offtruth_max"] = maxfrac);
  }
  return List::create(_["targets"] = tname, _["models"] = models, _["sets"] = wsn,
                      _["infeasible_watched"] = CharacterVector(infeasible.begin(), infeasible.end()), _["stage_occupancy"] = stage_occ,
                      _["round_occupancy"] = round_occ, _["set_first_exits"] = set_exits, _["prefix"] = prefix);
}

// ---------------------------------------------------------------------------------------------
// Final run (CORE_SPEC §6), trace (§4), replication (§4), local search (§7)
// ---------------------------------------------------------------------------------------------
static std::vector<std::vector<int>> models_from_R(const Data& D, SEXP x) {
  std::vector<std::vector<int>> out;
  if (Rf_isNull(x)) return out;
  List l(x);
  for (int i = 0; i < l.size(); ++i) out.push_back(to_internal(D, l[i]));
  return out;
}
static List island_to_list(const IslandResult& r, const Data& D) {
  auto msdf = [](const std::vector<MoveStats>& v) {
    int n = (int)v.size();
    NumericVector g(n), gf(n), ue(n), ua(n), us(n), ne(n), na(n), nn(n), ns(n), ie(n), ia(n);
    for (int i = 0; i < n; ++i) {
      g[i] = v[i].gibbs; gf[i] = v[i].gibbs_change; ue[i] = v[i].us_exec; ua[i] = v[i].us_acc; us[i] = v[i].us_self;
      ne[i] = v[i].ns_exec; na[i] = v[i].ns_acc; nn[i] = v[i].ns_noscore; ns[i] = v[i].ns_self; ie[i] = v[i].in_exec; ia[i] = v[i].in_acc;
    }
    return DataFrame::create(_["gibbs"] = g, _["gibbs_state_changes"] = gf, _["uswap_exec"] = ue, _["uswap_acc"] = ua, _["uswap_self"] = us,
                             _["nswap_exec"] = ne, _["nswap_acc"] = na, _["nswap_reject_noscore"] = nn, _["nswap_self"] = ns,
                             _["indep_exec"] = ie, _["indep_acc"] = ia);
  };
  NumericMatrix rbr(r.rb_round.size(), D.p);
  for (size_t h = 0; h < r.rb_round.size(); ++h) for (int j = 0; j < D.p; ++j) rbr(h, j) = r.rb_round[h][j];
  IntegerMatrix off(r.offspring.size(), r.offspring.empty() ? 0 : r.offspring[0].size());
  for (size_t t = 0; t < r.offspring.size(); ++t) for (size_t i = 0; i < r.offspring[t].size(); ++i) off(t, i) = r.offspring[t][i];
  return List::create(_["log_Z"] = r.logZ, _["phi"] = r.phi, _["log_increment"] = r.inc, _["ess"] = r.ess, _["cum_log_Z"] = r.cum,
                      _["distinct_resampled"] = r.distinct_resampled, _["distinct_moved"] = r.distinct_moved,
                      _["stage_moves"] = msdf(r.stage_moves), _["terminal_moves"] = msdf(r.terminal_moves),
                      _["terminal_distinct"] = r.terminal_distinct, _["pip"] = r.pip, _["rb_acc"] = r.rb_acc, _["rb_round"] = rbr,
                      _["offspring"] = off, _["init_draws_hash"] = hex64(r.init_hash),
                      _["seconds"] = NumericVector::create(_["init"] = r.seconds_init, _["bridge"] = r.seconds_bridge,
                                                           _["burn_in"] = r.seconds_burn, _["measured"] = r.seconds_measured));
}
static List local_to_list(const LocalArchive& A, const Data& D) {
  return List::create(_["centre"] = to_orig(D, A.centre), _["centre_F"] = A.centre_F, _["path"] = models_to_list(D, A.path),
                      _["path_F"] = A.path_F, _["scanned_centres"] = models_to_list(D, A.scanned), _["scanned_F"] = A.scanned_F,
                      _["scan_complete"] = A.scan_complete, _["scan_size"] = A.scan_size, _["termination"] = A.termination,
                      _["local_limit"] = A.local_limit, _["local_certified"] = A.local_certified,
                      _["returned"] = to_orig(D, A.returned), _["returned_F"] = A.returned_F, _["moves"] = A.moves,
                      _["n_evaluated"] = (double)A.n_eval);
}
static List store_to_list(const TopStore& s, const Data& D) {
  List M(s.s.size()); NumericVector v(s.s.size()); int i = 0;
  for (auto& e : s.s) { M[i] = to_orig(D, e.S); v[i] = e.v; ++i; }
  return List::create(_["models"] = M, _["value"] = v, _["capacity"] = (double)s.cap, _["full"] = s.s.size() >= s.cap);
}
static List ledger_to_list(const Ledger& L, const Data& D) {
  List hpm = L.has_hpm ? List::create(_["model"] = to_orig(D, L.hpmS), _["F"] = L.hpmF, _["log_m"] = L.hpm_logm,
                                      _["provenance"] = event_to_list(L.hpm_ev, L.hpm_mech)) : List();
  List out = List::create(_["hpm"] = hpm, _["top"] = store_to_list(L.top, D), _["leaders_gamma0"] = store_to_list(L.lead0, D),
                          _["leaders_gamma1"] = store_to_list(L.lead1, D),
                          _["island_best"] = NumericVector(L.island_best.begin() + 1, L.island_best.end()),
                          _["logical"] = counter_matrix(L.logical), _["fresh"] = counter_matrix(L.fresh));
  if (L.dump) {
    int n = (int)L.dumpmap.size();
    List M(n); NumericVector F(n), lm(n), lg(n);
    NumericVector cnt((size_t)n * N_PHASE * N_MECH);
    CharacterVector fph(n), fme(n); IntegerVector fis(n), fst(n), fro(n), fpa(n), fpo(n), fti(n), fit(n); NumericVector fphi(n);
    int i = 0;
    for (auto& kv : L.dumpmap) {
      M[i] = to_orig(D, kv.first); F[i] = kv.second.F; lm[i] = kv.second.logm; lg[i] = kv.second.lg0;
      for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) cnt[(size_t)i + (size_t)n * (a + (size_t)N_PHASE * b)] = kv.second.cnt[a][b];
      const EventCtx& e = kv.second.first;
      fph[i] = phase_name(e.phase); fme[i] = mech_name(kv.second.first_mech); fis[i] = e.island; fst[i] = e.stage; fro[i] = e.round;
      fpa[i] = e.particle; fpo[i] = e.position; fti[i] = e.tier; fphi[i] = e.phi; fit[i] = e.iter;
      ++i;
    }
    cnt.attr("dim") = IntegerVector::create(n, N_PHASE, N_MECH);
    CharacterVector rn(N_PHASE), cn(N_MECH);
    for (int a = 0; a < N_PHASE; ++a) rn[a] = phase_name(a);
    for (int b = 0; b < N_MECH; ++b) cn[b] = mech_name(b);
    cnt.attr("dimnames") = List::create(R_NilValue, rn, cn);
    out["dump"] = List::create(_["models"] = M, _["F"] = F, _["log_m"] = lm, _["log_gamma0"] = lg, _["counts"] = cnt,
                               _["first"] = DataFrame::create(_["phase"] = fph, _["mechanism"] = fme, _["tier"] = fti, _["island"] = fis,
                                                              _["stage"] = fst, _["round"] = fro, _["particle"] = fpa,
                                                              _["position"] = fpo, _["phi"] = fphi, _["iter"] = fit,
                                                              _["stringsAsFactors"] = false));
  }
  return out;
}
static List tracer_to_list(const Tracer& t) {
  auto pn = [&](const std::vector<int>& v) { CharacterVector o(v.size()); for (size_t i = 0; i < v.size(); ++i) o[i] = phase_name(v[i]); return o; };
  DataFrame U = DataFrame::create(_["seq"] = seq_len(t.u_value.size()), _["island"] = t.u_island, _["phase"] = pn(t.u_phase),
                                  _["stage"] = t.u_stage, _["round"] = t.u_round, _["particle"] = t.u_particle, _["position"] = t.u_position,
                                  _["purpose"] = t.u_purpose, _["value"] = t.u_value, _["stringsAsFactors"] = false);
  DataFrame S = DataFrame::create(_["island"] = t.s_island, _["phase"] = pn(t.s_phase), _["stage"] = t.s_stage, _["round"] = t.s_round,
                                  _["particle"] = t.s_particle, _["position"] = t.s_position, _["label"] = t.s_label, _["phi"] = t.s_phi,
                                  _["pre"] = t.s_pre, _["proposal"] = t.s_prop, _["alpha"] = t.s_alpha, _["o_j"] = t.s_oj,
                                  _["accepted"] = t.s_accepted, _["post"] = t.s_post, _["u_first"] = t.s_u_from, _["u_count"] = t.s_u_count,
                                  _["rb_recorded"] = t.s_rb, _["stringsAsFactors"] = false);
  DataFrame O = DataFrame::create(_["island"] = t.o_island, _["phase"] = pn(t.o_phase), _["stage"] = t.o_stage, _["round"] = t.o_round,
                                  _["particle"] = t.o_particle, _["order"] = t.o_order, _["stringsAsFactors"] = false);
  DataFrame I = DataFrame::create(_["island"] = t.i_island, _["particle"] = t.i_particle, _["model"] = t.i_model,
                                  _["u_first"] = t.i_u_from, _["u_count"] = t.i_u_count, _["stringsAsFactors"] = false);
  List G(t.g_island.size());
  for (size_t i = 0; i < t.g_island.size(); ++i)
    G[i] = List::create(_["island"] = t.g_island[i], _["stage"] = t.g_stage[i], _["phi_prev"] = t.g_phi_prev[i], _["phi"] = t.g_phi[i],
                        _["incoming"] = t.g_incoming[i], _["d"] = t.g_d[i], _["log_w"] = t.g_logw[i], _["log_increment"] = t.g_inc[i],
                        _["ess"] = t.g_ess[i], _["resample_u"] = t.g_resample_u[i], _["ancestors"] = t.g_ancestors[i],
                        _["cum_log_Z"] = t.g_cumlogZ[i]);
  return List::create(_["uniforms"] = U, _["steps"] = S, _["orders"] = O, _["init"] = I, _["stages"] = G);
}

struct RunOpts {
  int N = 0, L = 0, Hm = 4, islands = 4, tier = 0, ell = 0;
  bool dump = false, resampler_trace = false;
  double cache_capacity = 0;
};

static void ingest_tables(Ledger& led, Observer* obs, const Holder& h) {
  const Data& D = *h.D; const Start& st = *h.st;
  EventCtx ev; ev.phase = PH_TABLE; ev.island = 0;
  std::vector<int> U; std::vector<uint64_t> bits(D.W);
  for (int b = 0; b < st.J; ++b) {
    int m = (int)st.blocks[b].size();
    for (uint32_t c = 0; c < (1u << m); ++c) {
      if (std::isnan(st.logm_tab[b][c])) continue;
      U.clear(); std::fill(bits.begin(), bits.end(), 0); uint64_t hh = 0;
      for (int i = 0; i < m; ++i) if (c & (1u << i)) { int j = st.blocks[b][i]; U.push_back(j); bit_set(bits, j); hh ^= D.zob.key[j]; }
      double lm = st.logm_tab[b][c], F = D.logprior[U.size()] + lm, lg0 = D.logprior[U.size()] + st.logr[b][c];
      ev.stage = b + 1; ev.position = (int)c;
      led.event(U, F, lg0, lm, true, false, ev, ME_TABLE);
      if (obs) obs->on_score(bits, hh, ev, ME_TABLE, false);
    }
  }
}

static Observer* make_observer(const Holder& h, SEXP observer, int R) {
  if (Rf_isNull(observer)) return nullptr;
  const Data& D = *h.D;
  List ob(observer);
  std::unique_ptr<Observer> o(new Observer(&D, h.st.get(), &h.Nb, R));
  if (ob.containsElementNamed("truth") && !Rf_isNull(ob["truth"])) { if (o->add_model("truth", to_internal(D, ob["truth"]))) o->truth_idx = 0; }
  ModeResult m = start_mode(*h.st);
  o->add_model("start_mode", m.S); o->mode_idx = (int)o->wm.size() - 1;
  if (ob.containsElementNamed("watch") && !Rf_isNull(ob["watch"])) {
    List w = ob["watch"];
    for (int i = 0; i < w.size(); ++i) o->add_model(elem_name(w, i, "watch"), to_internal(D, w[i]));
  }
  if (ob.containsElementNamed("watch_sets") && !Rf_isNull(ob["watch_sets"])) {
    List w = ob["watch_sets"];
    for (int i = 0; i < w.size(); ++i) o->add_set(elem_name(w, i, "set"), models_from_R(D, w[i]));
  }
  return o.release();
}

// The final run on a frozen grid. Returns raw results; R assembles the reported outputs.
// [[Rcpp::export]]
List cpp_final_run(SEXP setup, NumericVector grid, List ro, double seed, SEXP observer, SEXP inherited, SEXP init_states,
                   SEXP variates, bool trace) {
  HPtr h = get_holder(setup); const Data& D = *h->D; const Start& st = *h->st;
  if (!h->has_graph) stop("setup required");
  RunOpts o;
  o.N = as<int>(ro["N"]); o.L = as<int>(ro["L"]); o.Hm = as<int>(ro["measured_rounds"]); o.islands = as<int>(ro["islands"]);
  o.tier = as<int>(ro["tier"]); o.ell = as<int>(ro["ell"]); o.dump = as<bool>(ro["dump_scored"]);
  o.resampler_trace = as<bool>(ro["resampler_trace"]); o.cache_capacity = as<double>(ro["cache_capacity"]);
  std::vector<double> g(grid.begin(), grid.end());
  auto t_all = Clock::now();
  Ledger led(&D, o.islands); led.dump = o.dump;
  // observer: NULL, an observer list (owned here), or an external pointer shared with the calibration (v3_fit)
  std::unique_ptr<Observer> obs_owned; Observer* obsp = nullptr; bool obs_external = false;
  if (TYPEOF(observer) == EXTPTRSXP) { obsp = XPtr<Observer>(observer).get(); obs_external = true; }
  else { obs_owned.reset(make_observer(*h, observer, o.islands)); obsp = obs_owned.get(); }
  if (obsp) obsp->T_last = (int)g.size() - 1;
  if (!obs_external) ingest_tables(led, obsp, *h); else ingest_tables(led, nullptr, *h);  // shared observer saw the tables in calibration
  // inherited state (frozen calibration): offered to the stores and the HPM with provenance "inherited"
  if (!Rf_isNull(inherited)) {
    List inh(inherited);
    if (inh.containsElementNamed("models")) {
      auto Ms = models_from_R(D, inh["models"]);
      Scorer sc(&D); EventCtx ev; ev.phase = PH_INHERITED;
      for (auto& S : Ms) {
        if ((int)S.size() > D.K) stop("inherited model larger than K");
        double lm = sc.score(S).logm; double c = st.comp(S);
        led.offer_stores(S, D.logprior[S.size()] + lm, D.logprior[S.size()] + c, lm, ev, ME_INHERITED);
      }
    }
    // provenance of the inherited HPM (first score in the calibration) replaces the label "inherited"
    if (inh.containsElementNamed("hpm") && !Rf_isNull(inh["hpm"])) {
      List hp = inh["hpm"];
      if (led.hpm_ev.phase == PH_INHERITED && hp.containsElementNamed("provenance") &&
          to_internal(D, hp["model"]) == led.hpmS) {
        List pv = hp["provenance"];
        EventCtx e; e.phase = phase_index(as<std::string>(pv["phase"])); e.tier = as<int>(pv["tier"]); e.island = as<int>(pv["island"]);
        e.stage = as<int>(pv["stage"]); e.round = as<int>(pv["round"]); e.particle = as<int>(pv["particle"]);
        e.position = as<int>(pv["position"]); e.phi = as<double>(pv["phi"]); e.iter = pv.containsElementNamed("iter") ? as<int>(pv["iter"]) : -1;
        led.hpm_ev = e; led.hpm_mech = mech_index(as<std::string>(pv["mechanism"]));
      }
    }
  }
  ScoreCache cache; cache.init(D.W, (size_t)o.cache_capacity);
  Engine E(D, st, h->Nb, h->B);
  E.cache = &cache; E.led = &led; E.obs = obsp;
  std::unique_ptr<Tracer> tr;
  if (trace) { tr.reset(new Tracer()); tr->D = &D; tr->ev = &E.ev; E.tr = tr.get(); }
  // prescribed variates (trace replay)
  PrescribedSource pres; bool use_pres = false;
  std::vector<std::vector<int>> pres_orders, pres_draws;
  if (!Rf_isNull(variates)) {
    List v(variates);
    if (v.containsElementNamed("uniforms") && !Rf_isNull(v["uniforms"])) { NumericVector uu = v["uniforms"]; pres.v.assign(uu.begin(), uu.end()); use_pres = true; }
    if (v.containsElementNamed("orders") && !Rf_isNull(v["orders"])) {
      List ol = v["orders"];
      for (int i = 0; i < ol.size(); ++i) {
        // an order is a character vector of labels ("G<j>", "U", "N<b>", "I") or an integer vector of 1-based canonical positions
        std::vector<int> ord;
        if (TYPEOF(ol[i]) == STRSXP) {
          CharacterVector cv = ol[i];
          for (auto s : cv) {
            std::string x = as<std::string>(s);
            if (x == "U") ord.push_back(D.p); else if (x == "I") ord.push_back(D.p + h->B + 1);
            else if (x[0] == 'N') ord.push_back(D.p + std::stoi(x.substr(1)));
            else if (x[0] == 'G') { std::vector<int> jj = to_internal(D, IntegerVector::create(std::stoi(x.substr(1)))); ord.push_back(jj[0]); }
            else stop("bad label in prescribed order");
          }
        } else { IntegerVector iv = ol[i]; for (int x : iv) ord.push_back(x - 1); }
        pres_orders.push_back(ord);
      }
      E.pres_orders = &pres_orders;
    }
    if (v.containsElementNamed("draws") && !Rf_isNull(v["draws"])) { pres_draws = models_from_R(D, v["draws"]); E.pres_draws = &pres_draws; }
  }
  std::vector<std::vector<int>> init = models_from_R(D, init_states);
  if (!init.empty() && (int)init.size() != o.N) stop("init_states must have N models");
  for (auto& S : init) if ((int)S.size() > D.K) stop("init state larger than K");
  List islands(o.islands);
  std::string status = "completed", message;
  List local, hpm_before;
  double sec_local = 0;
  std::vector<IslandResult> res;
  try {
    for (int r = 1; r <= o.islands; ++r) {
      RngSource rng; rng.g.seed_stream((uint64_t)seed, (uint64_t)(9 + r));  // final islands: streams 10..13 (M §6.1)
      VariateSource* base = use_pres ? (VariateSource*)&pres : (VariateSource*)&rng;
      std::unique_ptr<RecordingSource> rec;
      if (tr) { rec.reset(new RecordingSource(base, tr.get())); E.vs = rec.get(); } else E.vs = base;
      res.push_back(E.run_island(r, o.N, g, o.L, o.Hm, o.tier, init.empty() ? nullptr : &init, o.resampler_trace));
      islands[r - 1] = island_to_list(res.back(), D);
    }
    hpm_before = List::create(_["model"] = to_orig(D, led.hpmS), _["F"] = led.hpmF);
    auto t0 = Clock::now();
    LocalArchive A = E.local_search(led.hpmS, o.ell, o.tier, false);  // final local search from the global best (R4)
    sec_local = secs_since(t0);
    local = local_to_list(A, D);
  } catch (NumericalFailure& e) {
    status = "numerical_failure"; message = e.what();
  }
  List out = List::create(_["status"] = status, _["message"] = message, _["islands"] = islands, _["local_search"] = local,
                          _["hpm_before_local"] = hpm_before, _["ledger"] = ledger_to_list(led, D),
                          _["cache"] = NumericVector::create(_["capacity"] = (double)cache.capacity, _["hits"] = (double)cache.hits,
                                                             _["misses"] = (double)cache.misses, _["inserts"] = (double)cache.inserts,
                                                             _["clears"] = (double)cache.clears, _["entries_at_end"] = (double)cache.count),
                          _["seconds_local"] = sec_local, _["seconds_total"] = secs_since(t_all),
                          _["log_m0"] = D.logm0, _["log_Zbar0"] = st.logZbar0);
  if (obsp && !obs_external) out["observer"] = obsp->to_list();
  if (tr) out["trace"] = tracer_to_list(*tr);
  return out;
}

// Repeated final runs on one frozen grid (A11, E4): loop in C++, no ledger/observer/local search (estimates only).
// Each replication s uses streams 10..13 of seed seeds[s], so its log Zhat_r and PIPs are bit-identical to
// those of cpp_final_run with the same seed.
// [[Rcpp::export]]
List cpp_replicate(SEXP setup, NumericVector grid, List ro, NumericVector seeds) {
  HPtr h = get_holder(setup); const Data& D = *h->D; const Start& st = *h->st;
  int N = as<int>(ro["N"]), L = as<int>(ro["L"]), Hm = as<int>(ro["measured_rounds"]), R = as<int>(ro["islands"]);
  std::vector<double> g(grid.begin(), grid.end());
  int T = (int)g.size() - 1, ns = seeds.size(), p = D.p;
  NumericMatrix logZ(ns, R);
  NumericVector pip((size_t)ns * R * p); pip.attr("dim") = IntegerVector::create(ns, R, p);
  NumericVector inc((size_t)ns * R * T); inc.attr("dim") = IntegerVector::create(ns, R, T);
  ScoreCache cache; cache.init(D.W, (size_t)as<double>(ro["cache_capacity"]));
  Engine E(D, st, h->Nb, h->B); E.cache = &cache;
  std::string status = "completed";
  try {
    for (int s = 0; s < ns; ++s) {
      for (int r = 1; r <= R; ++r) {
        RngSource rng; rng.g.seed_stream((uint64_t)seeds[s], (uint64_t)(9 + r)); E.vs = &rng;
        IslandResult res = E.run_island(r, N, g, L, Hm, 0, nullptr, false);
        logZ(s, r - 1) = res.logZ;
        for (int j = 0; j < p; ++j) pip[(size_t)s + (size_t)ns * ((r - 1) + (size_t)R * j)] = res.pip[j];
        for (int t = 0; t < T; ++t) inc[(size_t)s + (size_t)ns * ((r - 1) + (size_t)R * t)] = res.inc[t];
      }
      if ((s & 1023) == 0) Rcpp::checkUserInterrupt();
    }
  } catch (NumericalFailure& e) { status = "numerical_failure"; }
  return List::create(_["status"] = status, _["log_Z"] = logZ, _["pip"] = pip, _["log_increment"] = inc);
}

// Direct resampler interface (A17): M independent multinomial resamplings of fixed log weights, offspring counts.
// [[Rcpp::export]]
IntegerMatrix cpp_resample_sample(NumericVector logw, int M, double seed, NumericVector uniforms) {
  std::vector<double> lw(logw.begin(), logw.end());
  int N = (int)lw.size();
  Data dummy; dummy.p = 1; dummy.W = 1; dummy.K = 0; dummy.orig = {1};
  Start dst; std::vector<std::vector<int>> nb;
  Engine E(dummy, dst, nb, 0);
  RngSource rng; rng.g.seed_stream((uint64_t)seed, 101); E.vs = &rng;
  PrescribedSource pres;   // test option: prescribed uniforms (consumed N per resampling) instead of stream 101
  if (uniforms.size() > 0) { pres.v.assign(uniforms.begin(), uniforms.end()); E.vs = &pres; M = (int)(uniforms.size() / N); }
  IntegerMatrix off(M, N);
  for (int m = 0; m < M; ++m) { std::vector<int> a = E.resample(lw); for (int x : a) off(m, x)++; }
  return off;
}

// Elementary step and round samplers (CORE_SPEC §4 testing interfaces). Stream 100 of `seed` (test stream).
static int parse_label(const Holder& h, const std::string& x) {
  const Data& D = *h.D;
  if (x == "U") return D.p;
  if (x == "I") return D.p + h.B + 1;
  if (x[0] == 'N') { int b = std::stoi(x.substr(1)); if (b < 1 || b > h.B) stop("neighbour label out of range"); return D.p + b; }
  if (x[0] == 'G') { std::vector<int> jj = to_internal(D, IntegerVector::create(std::stoi(x.substr(1)))); return jj[0]; }
  stop("unknown label %s", x);
}
static List counts_to_list(const std::map<std::string, long>& cnt) {
  CharacterVector k(cnt.size()); NumericVector c(cnt.size()); int i = 0;
  for (auto& kv : cnt) { k[i] = kv.first; c[i] = (double)kv.second; ++i; }
  return List::create(_["state"] = k, _["count"] = c);
}
// [[Rcpp::export]]
List cpp_step_sample(SEXP setup, SEXP S, std::string label, double phi, double M, double seed) {
  HPtr h = get_holder(setup); const Data& D = *h->D;
  std::vector<int> s = to_internal(D, S);
  if ((int)s.size() > D.K) stop("infeasible start state");
  int lab = parse_label(*h, label);
  ScoreCache cache; cache.init(D.W, std::max<size_t>(500 * (size_t)D.p, 1 << 15));
  Engine E(D, *h->st, h->Nb, h->B); E.cache = &cache;
  E.ev.phase = PH_TEST;
  RngSource rng; rng.g.seed_stream((uint64_t)seed, 100); E.vs = &rng;
  Particle P0; E.set_model(P0, s); E.eval(P0, ME_GIBBS_FLIP, false);
  std::map<std::string, long> cnt;
  for (long m = 0; m < (long)M; ++m) {
    Particle P = P0;
    if (lab < D.p) E.step_gibbs(P, lab, phi);
    else if (lab == D.p) E.step_uswap(P, phi);
    else if (lab <= D.p + h->B) E.step_nswap(P, phi, lab - D.p);
    else E.step_indep(P, phi);
    cnt[join_idx(P.S, D.orig)]++;
  }
  return counts_to_list(cnt);
}
// [[Rcpp::export]]
List cpp_round_sample(SEXP setup, SEXP S, double phi, double M, double seed, bool trace) {
  HPtr h = get_holder(setup); const Data& D = *h->D;
  std::vector<int> s = to_internal(D, S);
  if ((int)s.size() > D.K) stop("infeasible start state");
  ScoreCache cache; cache.init(D.W, std::max<size_t>(500 * (size_t)D.p, 1 << 15));
  Engine E(D, *h->st, h->Nb, h->B); E.cache = &cache;
  E.ev.phase = PH_TEST;
  RngSource rng; rng.g.seed_stream((uint64_t)seed, 100);
  std::unique_ptr<Tracer> tr; std::unique_ptr<RecordingSource> rec;
  if (trace) { tr.reset(new Tracer()); tr->D = &D; tr->ev = &E.ev; E.tr = tr.get(); rec.reset(new RecordingSource(&rng, tr.get())); E.vs = rec.get(); }
  else E.vs = &rng;
  Particle P0; E.set_model(P0, s); E.eval(P0, ME_GIBBS_FLIP, false);
  std::map<std::string, long> cnt;
  for (long m = 0; m < (long)M; ++m) {
    Particle P = P0;
    E.ev.round = (int)m + 1; E.ev.particle = 1;
    E.one_round(P, 0, phi);
    cnt[join_idx(P.S, D.orig)]++;
  }
  List out = counts_to_list(cnt);
  if (trace) out["trace"] = tracer_to_list(*tr);
  return out;
}

// Local search testing interface (CORE_SPEC §7): fresh ledger whose best is the centre.
// [[Rcpp::export]]
List cpp_local_search(SEXP setup, SEXP centre, int ell, bool dump) {
  HPtr h = get_holder(setup); const Data& D = *h->D;
  std::vector<int> c = to_internal(D, centre);
  if ((int)c.size() > D.K) stop("infeasible centre");
  Ledger led(&D, 0); led.dump = dump;
  ScoreCache cache; cache.init(D.W, std::max<size_t>(500 * (size_t)D.p, 1 << 15));
  Engine E(D, *h->st, h->Nb, h->B); E.cache = &cache; E.led = &led;
  LocalArchive A = E.local_search(c, ell, 0, true);
  List out = local_to_list(A, D);
  out["ledger"] = ledger_to_list(led, D);
  return out;
}

// ---------------------------------------------------------------------------------------------
// Exact branch (CORE_SPEC §7 `v3_enumerate`; M §6.2; R9)
// ---------------------------------------------------------------------------------------------
// [[Rcpp::export]]
List cpp_enumerate(SEXP ctx) {
  HPtr h = get_holder(ctx); const Data& D = *h->D;
  int p = D.p, K = D.K;
  Scorer sc(&D);
  // streaming log-sum-exp with long double accumulators (rescaled when the running maximum increases)
  double mx = NEG_INF; long double total = 0; std::vector<long double> numer(p, 0.0L);
  std::vector<int> hpmS; double hpmF = NEG_INF, hpm_eta = 0; bool has = false;
  TopStore top; top.init(40 * (size_t)p + 1, true);
  // R9: two largest values of F(S) + eta(S) with their models
  double up1 = NEG_INF, up2 = NEG_INF; std::vector<int> upS1, upS2;
  double count = 0;
  std::vector<int> S;
  std::string status = "exact", message;
  std::function<void(int)> rec = [&](int start) {
    ScoreOut o = sc.score(S);
    double F = D.logprior[S.size()] + o.logm;
    double eta = sc.error_bound(o, (int)S.size());
    count += 1;
    if (F > mx) {
      long double scale = (mx == NEG_INF) ? 0.0L : std::exp((long double)(mx - F));
      total *= scale; for (auto& v : numer) v *= scale; mx = F;
    }
    long double w = std::exp((long double)(F - mx));
    total += w; for (int j : S) numer[j] += w;
    if (!has || hpm_better(F, S, hpmF, hpmS)) { has = true; hpmS = S; hpmF = F; hpm_eta = eta; }
    top.offer(F, S);
    double up = F + eta;
    if (up > up1) { up2 = up1; upS2 = upS1; up1 = up; upS1 = S; } else if (up > up2) { up2 = up; upS2 = S; }
    if (((long)count & 65535) == 0) Rcpp::checkUserInterrupt();
    if ((int)S.size() >= K) return;
    for (int j = start; j < p; ++j) { S.push_back(j); rec(j + 1); S.pop_back(); }
  };
  try { rec(0); } catch (NumericalFailure& e) { status = "numerical_failure"; message = e.what(); }
  double logZ = mx + (double)std::log(total);
  NumericVector pip(p);
  for (int j = 0; j < p; ++j) pip[j] = (double)(numer[j] / total);
  double runner_up = (upS1 == hpmS) ? up2 : up1;
  double second_F = NA_REAL;
  if (top.s.size() >= 2) second_F = std::next(top.s.begin())->v;
  bool certified = (status == "exact") && (hpmF - hpm_eta > runner_up);
  return List::create(_["status"] = status, _["message"] = message, _["log_Z"] = logZ, _["pip"] = pip,
                      _["hpm"] = to_orig(D, hpmS), _["hpm_F"] = hpmF, _["models_scored"] = count, _["top"] = store_to_list(top, D),
                      _["second_F"] = second_F, _["margin"] = hpmF - second_F, _["hpm_error_bound"] = hpm_eta, _["hpm_error_bound_kind"] = "heuristic_condition_estimate",
                      _["certificate_bound"] = hpmF - runner_up, _["global_certified"] = certified);
}

// Exact reference for analysis (CORE_SPEC §8 "Exact references", p <= 22): log gamma_0(S) and d(S) for every
// |S| <= K; models encoded as integer codes with bit (j-1) for the j-th retained column (internal order).
// [[Rcpp::export]]
List cpp_reference(SEXP setup) {
  HPtr h = get_holder(setup); const Data& D = *h->D; const Start& st = *h->st;
  int p = D.p, K = D.K;
  if (p > 22) stop("reference files are for p <= 22");
  Scorer sc(&D);
  std::vector<double> codes, lg0, dd, F;
  std::vector<int> S; uint32_t code = 0;
  std::function<void(int)> rec = [&](int start) {
    ScoreOut o = sc.score(S); double c = st.comp(S);
    codes.push_back(code); lg0.push_back(D.logprior[S.size()] + c); dd.push_back((o.logm - D.logm0) - c); F.push_back(D.logprior[S.size()] + o.logm);
    if ((int)S.size() >= K) return;
    for (int j = start; j < p; ++j) { S.push_back(j); code |= (1u << j); rec(j + 1); code &= ~(1u << j); S.pop_back(); }
  };
  rec(0);
  return List::create(_["code"] = codes, _["log_gamma0"] = lg0, _["d"] = dd, _["F"] = F, _["orig"] = IntegerVector(D.orig.begin(), D.orig.end()),
                      _["log_m0"] = D.logm0, _["log_Zbar0"] = st.logZbar0);
}

// ---------------------------------------------------------------------------------------------
// Calibration layer (CORE_SPEC v2 §10; M §§6.6-6.9). The R function v3_calibrate orchestrates; C++ keeps one
// persistent calibration state (ledger with tables and score leaders, cache, random streams 0-9) across the pilot,
// the rebuild iterations and the escalation (R3: leaders kept across tiers; R6: diagnostic streams continue).
// ---------------------------------------------------------------------------------------------
// Pure rules (testing interfaces B1, B2).
// [[Rcpp::export]]
List cpp_pilot_schedule(NumericVector d, double H, int Te) {
  std::vector<double> dv(d.begin(), d.end());
  std::vector<double> sched{0.0}; std::vector<int> forced_at; int forced = 0;
  double phi = 0.0;
  while (phi < 1.0) {
    NextPhi np = pilot_next_phi(dv, phi, H, Te);
    if (np.forced) { ++forced; forced_at.push_back((int)sched.size()); }
    phi = np.phi; sched.push_back(phi);
  }
  return List::create(_["schedule"] = sched, _["forced_pilot_steps"] = forced, _["forced_stage"] = forced_at, _["T"] = (int)sched.size() - 1);
}
// [[Rcpp::export]]
List cpp_build_grid(NumericVector lg0, NumericVector d, NumericVector targets, int Te) {
  std::vector<double> a(lg0.begin(), lg0.end()), b(d.begin(), d.end()), t(targets.begin(), targets.end());
  if (a.size() != b.size()) stop("logg0_V and d_V must have equal length");
  auto t0 = Clock::now();
  GridResult g = build_grid(a, b, t, Te);
  return List::create(_["grid"] = g.grid, _["ok"] = g.ok, _["reason"] = g.reason, _["rho_appended"] = g.rho,
                      _["intervals"] = (int)g.grid.size() - 1, _["F_V_evaluations"] = (double)g.evals, _["seconds"] = secs_since(t0));
}

struct CalState {
  RObject setup_keep, obs_keep;
  Holder* h = nullptr;
  std::unique_ptr<Ledger> led;
  ScoreCache cache;
  std::unique_ptr<Engine> E;
  Observer* obs = nullptr;
  uint64_t seed = 1;
  std::map<int, RngSource> streams;
  RngSource& stream(int k) {
    auto it = streams.find(k);
    if (it == streams.end()) { RngSource g; g.g.seed_stream(seed, (uint64_t)k); it = streams.emplace(k, g).first; }
    return it->second;
  }
};
typedef XPtr<CalState> CPtr;

// [[Rcpp::export]]
SEXP cpp_observer_new(SEXP setup, SEXP observer) {
  HPtr h = get_holder(setup);
  Observer* o = make_observer(*h, observer, 4);
  if (!o) return R_NilValue;
  XPtr<Observer> p(o, true);
  p.attr("setup") = setup;  // keep the setup alive while the observer exists
  return p;
}
// [[Rcpp::export]]
List cpp_observer_report(SEXP obs, int T_last) {
  XPtr<Observer> o(obs); o->T_last = T_last;
  return o->to_list();
}

// [[Rcpp::export]]
SEXP cpp_cal_new(SEXP setup, double seed, List ro, SEXP observer) {
  HPtr h = get_holder(setup);
  CalState* c = new CalState();
  c->setup_keep = setup; c->h = h.get(); c->seed = (uint64_t)seed;
  const Data& D = *h->D;
  c->led.reset(new Ledger(&D, 4)); c->led->dump = as<bool>(ro["dump_scored"]);
  if (TYPEOF(observer) == EXTPTRSXP) { c->obs = XPtr<Observer>(observer).get(); c->obs_keep = observer; }
  c->cache.init(D.W, (size_t)as<double>(ro["cache_capacity"]));
  c->E.reset(new Engine(D, *h->st, h->Nb, h->B));
  c->E->cache = &c->cache; c->E->led = c->led.get(); c->E->obs = c->obs;
  ingest_tables(*c->led, c->obs, *h);
  return CPtr(c, true);
}
static List hpm_now(const CalState& c) {
  const Data& D = *c.h->D;
  return List::create(_["model"] = to_orig(D, c.led->hpmS), _["F"] = c.led->hpmF, _["provenance"] = event_to_list(c.led->hpm_ev, c.led->hpm_mech));
}
// Pilot at tier e (M §6.6): stream 0 (e = 0) or 5 (e = 1); H particles; adaptive schedule; L burn-in, Hm measured
// rounds; then one local search from the global best (R4).
// [[Rcpp::export]]
List cpp_cal_pilot(SEXP state, int tier, int H, int Te, int L, int Hm, int ell) {
  CPtr c(state); const Data& D = *c->h->D;
  Engine& E = *c->E;
  int sid = tier == 0 ? 0 : 5;
  E.vs = &c->stream(sid);
  Engine::Schedule sch; sch.adaptive = true; sch.H = H; sch.Te = Te;
  try {
    auto t0 = Clock::now();
    double pos0 = (double)c->stream(sid).g.count;
    IslandResult res = E.run_island_s(0, H, sch, L, Hm, tier, nullptr, false, PH_PILOT, 0);
    List streaminfo = List::create(_["stream"] = sid, _["position_start"] = pos0, _["position_end"] = (double)c->stream(sid).g.count,
                                   _["init_draws_hash"] = hex64(res.init_hash));
    double sec_isl = secs_since(t0);
    List before = hpm_now(*c);
    t0 = Clock::now();
    LocalArchive A = E.local_search(c->led->hpmS, ell, tier, false, 0);
    double sec_ls = secs_since(t0);
    List after = hpm_now(*c);
    std::vector<double> sched{0.0}; sched.insert(sched.end(), res.phi.begin(), res.phi.end());
    return List::create(_["status"] = "ok", _["island"] = island_to_list(res, D), _["schedule"] = sched, _["forced_pilot_steps"] = res.forced,
                        _["stream"] = streaminfo,
                        _["local_search"] = local_to_list(A, D), _["best_before_local"] = before, _["best_after_local"] = after,
                        _["seconds"] = NumericVector::create(_["island"] = sec_isl, _["local"] = sec_ls));
  } catch (NumericalFailure& e) {
    return List::create(_["status"] = "numerical_failure", _["message"] = e.what());
  }
}
// One rebuild iteration's diagnostics at tier e (M §6.8): 4 diagnostic islands of H particles on `grid`, streams
// 1-4 (e = 0) or 6-9 (e = 1), continuing across iterations (R6); each with L burn-in and Hm measured rounds; island
// bests per R5; then one local search from the global best (R4).
// [[Rcpp::export]]
List cpp_cal_diag(SEXP state, int tier, NumericVector grid, int H, int L, int Hm, int ell, int iter) {
  CPtr c(state); const Data& D = *c->h->D;
  Engine& E = *c->E;
  std::vector<double> g(grid.begin(), grid.end());
  Engine::Schedule sch; sch.grid = &g;
  std::fill(c->led->island_best.begin(), c->led->island_best.end(), NEG_INF);
  try {
    List isl(4); NumericVector lz(4); auto t0 = Clock::now();
    IntegerVector sid(4); NumericVector p0(4), p1(4); CharacterVector ih(4);
    for (int r = 1; r <= 4; ++r) {
      sid[r - 1] = (tier == 0 ? 0 : 5) + r;
      E.vs = &c->stream(sid[r - 1]);
      p0[r - 1] = (double)c->stream(sid[r - 1]).g.count;   // R6: streams continue across rebuild iterations
      IslandResult res = E.run_island_s(r, H, sch, L, Hm, tier, nullptr, false, PH_DIAG, iter);
      p1[r - 1] = (double)c->stream(sid[r - 1]).g.count;
      isl[r - 1] = island_to_list(res, D); lz[r - 1] = res.logZ; ih[r - 1] = hex64(res.init_hash);
    }
    DataFrame streams = DataFrame::create(_["island"] = seq_len(4), _["stream"] = sid, _["position_start"] = p0, _["position_end"] = p1,
                                          _["init_draws_hash"] = ih, _["stringsAsFactors"] = false);
    double sec_isl = secs_since(t0);
    NumericVector ib(c->led->island_best.begin() + 1, c->led->island_best.end());
    List before = hpm_now(*c);
    t0 = Clock::now();
    LocalArchive A = E.local_search(c->led->hpmS, ell, tier, false, iter);
    double sec_ls = secs_since(t0);
    List after = hpm_now(*c);
    return List::create(_["status"] = "ok", _["islands"] = isl, _["log_Z_r"] = lz, _["streams"] = streams, _["island_best"] = ib, _["local_search"] = local_to_list(A, D),
                        _["best_before_local"] = before, _["best_after_local"] = after,
                        _["seconds"] = NumericVector::create(_["islands"] = sec_isl, _["local"] = sec_ls));
  } catch (NumericalFailure& e) {
    return List::create(_["status"] = "numerical_failure", _["message"] = e.what());
  }
}
// Candidate set V (M §6.7; R3): top 20p by log gamma_0 union top 20p by log gamma_1 union {empty}, deduplicated,
// listed in lexicographic order of the sorted index vectors (this order is also the summation order of F_V).
// log gamma_0 and d are recomputed with a separate scorer (deterministic; not score events).
// [[Rcpp::export]]
List cpp_cal_V(SEXP state) {
  CPtr c(state); const Data& D = *c->h->D; const Start& st = *c->h->st;
  std::set<std::vector<int>> V;
  V.insert(std::vector<int>());
  for (auto& e : c->led->lead0.s) V.insert(e.S);
  for (auto& e : c->led->lead1.s) V.insert(e.S);
  Scorer sc(&D);
  int n = (int)V.size();
  List M(n); NumericVector lg0(n), d(n), F(n); int i = 0;
  for (auto& S : V) {  // std::set of vectors iterates in lexicographic order
    double lm = sc.score(S).logm, cmp = st.comp(S);
    M[i] = to_orig(D, S); lg0[i] = D.logprior[S.size()] + cmp; d[i] = (lm - D.logm0) - cmp; F[i] = D.logprior[S.size()] + lm; ++i;
  }
  return List::create(_["models"] = M, _["log_gamma0"] = lg0, _["d"] = d, _["F"] = F,
                      _["n_leaders_gamma0"] = (double)c->led->lead0.s.size(), _["n_leaders_gamma1"] = (double)c->led->lead1.s.size());
}
// Inherited state for the frozen object: models of the three stores (top-(40p+1), both leader stores) and the HPM
// with provenance; calibration score counters, cache statistics and dump.
// [[Rcpp::export]]
List cpp_cal_export(SEXP state) {
  CPtr c(state); const Data& D = *c->h->D;
  std::set<std::vector<int>> U;
  for (auto& e : c->led->top.s) U.insert(e.S);
  for (auto& e : c->led->lead0.s) U.insert(e.S);
  for (auto& e : c->led->lead1.s) U.insert(e.S);
  std::vector<std::vector<int>> Ms(U.begin(), U.end());
  return List::create(_["inherited"] = List::create(_["models"] = models_to_list(D, Ms), _["hpm"] = hpm_now(*c)),
                      _["ledger"] = ledger_to_list(*c->led, D),
                      _["cache"] = NumericVector::create(_["capacity"] = (double)c->cache.capacity, _["hits"] = (double)c->cache.hits,
                                                         _["misses"] = (double)c->cache.misses, _["inserts"] = (double)c->cache.inserts,
                                                         _["clears"] = (double)c->cache.clears));
}

// Duplicate components (M §4.5) from the Gram already held by the context: pairs with |G_jl| / sqrt(G_jj G_ll) >=
// 1 - 1e-10, connected by union-find; O(p^2) time, no p x p temporaries (code review D-1). Components of size >= 2,
// as sorted original indices, ordered by their smallest member.
// [[Rcpp::export]]
List cpp_dup_components(SEXP ctx) {
  HPtr h = get_holder(ctx); const Data& D = *h->D;
  int p = D.p;
  std::vector<int> parent(p); for (int j = 0; j < p; ++j) parent[j] = j;
  std::function<int(int)> find = [&](int i) { while (parent[i] != i) { parent[i] = parent[parent[i]]; i = parent[i]; } return i; };
  std::vector<double> s(p); for (int j = 0; j < p; ++j) s[j] = std::sqrt(D.Gat(j, j));
  for (int a = 0; a < p; ++a)
    for (int b = a + 1; b < p; ++b)
      if (std::fabs(D.Gat(a, b)) / (s[a] * s[b]) >= 1 - 1e-10) { int x = find(a), y = find(b); if (x != y) parent[std::max(x, y)] = std::min(x, y); }
  std::map<int, std::vector<int>> comp;
  for (int j = 0; j < p; ++j) comp[find(j)].push_back(j);
  std::vector<std::vector<int>> out;
  for (auto& kv : comp) if (kv.second.size() >= 2) out.push_back(kv.second);
  return models_to_list(D, out);
}
