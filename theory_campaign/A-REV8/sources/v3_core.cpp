// v3_core.cpp -- Rcpp entry points of the SMC-BVS v3 core layer (CORE_SPEC v2 §§1-9). Compiled by v3.R with
// Rcpp::sourceCpp; the headers in this directory hold the algorithm, this file only converts between R and C++.
#include <Rcpp.h>
#include <memory>
#include <fstream>
#include "v3_engine.h"

using namespace Rcpp;
using namespace v3;

#include "v3_holder.h"
typedef XPtr<Holder> HPtr;

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
List cpp_context(NumericMatrix X, NumericVector y, IntegerVector orig, bool return_gram) {
  int n = X.nrow(), p = X.ncol();
  std::vector<int> o(orig.begin(), orig.end());
  Holder* h = new Holder();
  h->D = std::make_shared<Data>();
  data_init(*h->D, X.begin(), y.begin(), n, p, o);
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
                      _["error_bound_kind"] = "heuristic (not a validated interval bound)");
}

// [[Rcpp::export]]
NumericVector cpp_time_scores(SEXP ctx, int k, int reps) {
  HPtr h = get_holder(ctx); const Data& D = *h->D;
  k = std::max(0, std::min(k, D.K));
  Scorer sc(&D); std::vector<int> S;
  auto t0 = Clock::now(); double sink = 0;
  for (int r = 0; r < reps; ++r) {
    // A cyclic consecutive window has exactly k distinct columns for every p and k <= p.
    // A fixed stride followed by deduplication can silently time smaller models.
    S.clear(); for (int a = 0; a < k; ++a) S.push_back((r + a) % D.p);
    std::sort(S.begin(), S.end());
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
static const int B_MAX = 16;
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
  return List::create(_["phase"] = phase_name(r.phase), _["tier"] = r.tier, _["iter"] = r.iter, _["island"] = r.island,
                      _["log_Z"] = r.logZ, _["phi"] = r.phi, _["log_increment"] = r.inc, _["ess"] = r.ess, _["cum_log_Z"] = r.cum,
                      _["distinct_resampled"] = r.distinct_resampled, _["distinct_moved"] = r.distinct_moved,
                      _["stage_moves"] = msdf(r.stage_moves), _["terminal_moves"] = msdf(r.terminal_moves),
                      _["terminal_distinct"] = r.terminal_distinct, _["pip"] = r.pip, _["rb_acc"] = r.rb_acc, _["rb_round"] = rbr,
                      _["partial"] = r.partial, _["init_draws_hash"] = hex64(r.init_hash),
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
  return out;
}
static void ingest_tables(Ledger& led, const Holder& h) {
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
    }
  }
}

// The final run on a frozen grid. Returns raw results; R assembles the reported outputs.
// [[Rcpp::export]]
List cpp_final_run(SEXP setup, NumericVector grid, List ro, double seed, SEXP inherited, SEXP runtime) {
  HPtr h = get_holder(setup); const Data& D = *h->D; const Start& st = *h->st;
  if (!h->has_graph) stop("setup required");
  struct RunOpts { int N, L, Hm, islands, tier, ell; double cache_capacity; };
  RunOpts o;
  o.N = as<int>(ro["N"]); o.L = as<int>(ro["L"]); o.Hm = as<int>(ro["measured_rounds"]); o.islands = as<int>(ro["islands"]);
  o.tier = as<int>(ro["tier"]); o.ell = as<int>(ro["ell"]);
  o.cache_capacity = as<double>(ro["cache_capacity"]);
  std::vector<double> g(grid.begin(), grid.end());
  auto t_all = Clock::now();
  Ledger led(&D, o.islands);
  ingest_tables(led, *h);
  ScoreCache cache; cache.init(D.W, (size_t)o.cache_capacity);
  Engine E(D, st, h->Nb, h->B);
  E.cache = &cache; E.led = &led; E.guard = runtime_ptr(runtime);
  List islands(o.islands);
  std::string status = "completed", message;
  List local, hpm_before;
  double sec_local = 0;
  std::vector<IslandResult> res;
  try {
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
    for (int r = 1; r <= o.islands; ++r) {
      RngSource rng; rng.g.seed_stream((uint64_t)seed, (uint64_t)(9 + r));  // final islands: streams 10..13 (M §6.1)
      E.vs = &rng;
      res.push_back(E.run_island(r, o.N, g, o.L, o.Hm, o.tier, nullptr));
      List island = island_to_list(res.back(), D);
      island["stream"] = List::create(_["stream"] = 9 + r, _["position_start"] = 0.0,
        _["position_end"] = (double)rng.g.count, _["init_draws_hash"] = hex64(res.back().init_hash));
      islands[r - 1] = island;
      if (res.back().partial) { status = "resource_limit"; break; }
    }
    if (status == "completed") {
    hpm_before = List::create(_["model"] = to_orig(D, led.hpmS), _["F"] = led.hpmF);
    auto t0 = Clock::now();
    LocalArchive A = E.local_search(led.hpmS, o.ell, o.tier, false);  // final local search from the global best (R4)
    sec_local = secs_since(t0);
    local = local_to_list(A, D);
    if (E.guard && E.guard->check(sec_local, "local_search", local_event(o.tier, -1))) status = "resource_limit";
    }
  } catch (NumericalFailure& e) {
    status = "numerical_failure"; message = e.what();
    // Calibration already scored its saved HPM, even if inheritance stopped before
    // reaching it. Reconcile that known score without another scorer call. This is
    // failure-only so successful rescoring, stores and random draws stay unchanged.
    if (!Rf_isNull(inherited)) {
      List inh(inherited);
      if (inh.containsElementNamed("hpm") && !Rf_isNull(inh["hpm"])) {
        List hp = inh["hpm"];
        if (hp.containsElementNamed("model") && hp.containsElementNamed("F") && hp.containsElementNamed("provenance")) {
          std::vector<int> S = to_internal(D, hp["model"]);
          double F = as<double>(hp["F"]);
          bool better = !led.has_hpm || hpm_better(F, S, led.hpmF, led.hpmS);
          bool restore = led.has_hpm && led.hpm_ev.phase == PH_INHERITED && S == led.hpmS && F == led.hpmF;
          if (better || restore) {
            List pv = hp["provenance"];
            EventCtx ev; ev.phase = phase_index(as<std::string>(pv["phase"])); ev.tier = as<int>(pv["tier"]); ev.island = as<int>(pv["island"]);
            ev.stage = as<int>(pv["stage"]); ev.round = as<int>(pv["round"]); ev.particle = as<int>(pv["particle"]);
            ev.position = as<int>(pv["position"]); ev.phi = as<double>(pv["phi"]); ev.iter = pv.containsElementNamed("iter") ? as<int>(pv["iter"]) : -1;
            if (better) led.offer_hpm(S, F, F - D.logprior[S.size()], ev, mech_index(as<std::string>(pv["mechanism"])));
            else { led.hpm_ev = ev; led.hpm_mech = mech_index(as<std::string>(pv["mechanism"])); }
          }
        }
      }
    }
  }
  List out = List::create(_["status"] = status, _["message"] = message, _["islands"] = islands, _["local_search"] = local,
                          _["hpm_before_local"] = hpm_before, _["ledger"] = ledger_to_list(led, D),
                          _["cache"] = NumericVector::create(_["capacity"] = (double)cache.capacity, _["hits"] = (double)cache.hits,
                                                             _["misses"] = (double)cache.misses, _["inserts"] = (double)cache.inserts,
                                                             _["clears"] = (double)cache.clears, _["entries_at_end"] = (double)cache.count),
                          _["seconds_local"] = sec_local, _["seconds_total"] = secs_since(t_all),
                          _["log_m0"] = D.logm0, _["log_Zbar0"] = st.logZbar0);
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
                      _["second_F"] = second_F, _["margin"] = hpmF - second_F, _["hpm_error_bound"] = hpm_eta, _["hpm_error_bound_kind"] = "heuristic (not a validated interval bound)",
                      _["certificate_bound"] = hpmF - runner_up, _["global_certified"] = certified);
}

// ---------------------------------------------------------------------------------------------
// Calibration layer (CORE_SPEC v2 §10; M §§6.6-6.9). The R function v3_calibrate orchestrates; C++ keeps one
// persistent calibration state (ledger with tables and score leaders, cache, random streams 0-9) across the pilot,
// the rebuild iterations and the escalation (R3: leaders kept across tiers; R6: diagnostic streams continue).
// ---------------------------------------------------------------------------------------------
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
  RObject setup_keep, runtime_keep;
  Holder* h = nullptr;
  std::unique_ptr<Ledger> led;
  ScoreCache cache;
  std::unique_ptr<Engine> E;
  RuntimeGuard* guard = nullptr;
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
SEXP cpp_cal_new(SEXP setup, double seed, List ro, SEXP runtime) {
  HPtr h = get_holder(setup);
  CalState* c = new CalState();
  c->setup_keep = setup; c->h = h.get(); c->seed = (uint64_t)seed;
  const Data& D = *h->D;
  c->led.reset(new Ledger(&D, 4));
  c->guard = runtime_ptr(runtime); c->runtime_keep = runtime;
  c->cache.init(D.W, (size_t)as<double>(ro["cache_capacity"]));
  c->E.reset(new Engine(D, *h->st, h->Nb, h->B));
  c->E->cache = &c->cache; c->E->led = c->led.get(); c->E->guard = c->guard;
  ingest_tables(*c->led, *h);
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
    IslandResult res = E.run_island_s(0, H, sch, L, Hm, tier, nullptr, PH_PILOT, 0);
    List streaminfo = List::create(_["stream"] = sid, _["position_start"] = pos0, _["position_end"] = (double)c->stream(sid).g.count,
                                   _["init_draws_hash"] = hex64(res.init_hash));
    double sec_isl = secs_since(t0);
    std::vector<double> sched{0.0}; sched.insert(sched.end(), res.phi.begin(), res.phi.end());
    if (res.partial) return List::create(_["status"] = "resource_limit", _["island"] = island_to_list(res, D),
      _["schedule"] = sched, _["forced_pilot_steps"] = res.forced, _["stream"] = streaminfo,
      _["partial_results"] = true, _["seconds"] = NumericVector::create(_["island"] = sec_isl));
    List before = hpm_now(*c);
    t0 = Clock::now();
    LocalArchive A = E.local_search(c->led->hpmS, ell, tier, false, 0);
    double sec_ls = secs_since(t0);
    List after = hpm_now(*c);
    return List::create(_["status"] = (c->guard && c->guard->check(sec_ls, "local_search", local_event(tier, 0))) ? "resource_limit" : "ok", _["island"] = island_to_list(res, D), _["schedule"] = sched, _["forced_pilot_steps"] = res.forced,
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
      IslandResult res = E.run_island_s(r, H, sch, L, Hm, tier, nullptr, PH_DIAG, iter);
      p1[r - 1] = (double)c->stream(sid[r - 1]).g.count;
      isl[r - 1] = island_to_list(res, D); lz[r - 1] = res.logZ; ih[r - 1] = hex64(res.init_hash);
      if (res.partial) {
        Range ran(0, r - 1);
        DataFrame streams = DataFrame::create(_["island"] = seq_len(r), _["stream"] = sid[ran],
          _["position_start"] = p0[ran], _["position_end"] = p1[ran],
          _["init_draws_hash"] = ih[ran], _["stringsAsFactors"] = false);
        return List::create(_["status"] = "resource_limit", _["islands"] = isl, _["streams"] = streams,
          _["log_Z_r"] = lz[ran], _["partial_results"] = true,
          _["seconds"] = NumericVector::create(_["islands"] = secs_since(t0)));
      }
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
    return List::create(_["status"] = (c->guard && c->guard->check(sec_ls, "local_search", local_event(tier, iter))) ? "resource_limit" : "ok", _["islands"] = isl, _["log_Z_r"] = lz, _["streams"] = streams, _["island_best"] = ib, _["local_search"] = local_to_list(A, D),
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
  try {
    for (auto& S : V) {  // std::set of vectors iterates in lexicographic order
      double lm = sc.score(S).logm, cmp = st.comp(S);
      M[i] = to_orig(D, S); lg0[i] = D.logprior[S.size()] + cmp; d[i] = (lm - D.logm0) - cmp; F[i] = D.logprior[S.size()] + lm; ++i;
    }
  } catch (NumericalFailure& e) {
    // R propagates this through the calibration tier's ordinary failure handler.
    // A partially rescored V must never be supplied to grid construction.
    return List::create(_["status"] = "numerical_failure", _["message"] = e.what());
  }
  return List::create(_["models"] = M, _["log_gamma0"] = lg0, _["d"] = d, _["F"] = F,
                      _["n_leaders_gamma0"] = (double)c->led->lead0.s.size(), _["n_leaders_gamma1"] = (double)c->led->lead1.s.size());
}
// Inherited state for the frozen object: models of the three stores (top-(40p+1), both leader stores) and the HPM
// with provenance; aggregate calibration score counters and cache statistics.
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

// One shared fit clock; no statistical setting or random draw is changed.
// [[Rcpp::export]]
SEXP cpp_runtime_new(double hours, double elapsed_before) {
  XPtr<RuntimeGuard> p(new RuntimeGuard(), true);
  p->allocation = hours * 3600; p->elapsed_before = elapsed_before;
  return p;
}
// [[Rcpp::export]]
bool cpp_runtime_check(SEXP runtime, double operation_seconds, std::string checkpoint, int tier, int iter) {
  RuntimeGuard* g = runtime_ptr(runtime);
  if (!g) return false;
  EventCtx ev; ev.tier = tier; ev.iter = iter; ev.phase = PH_DIAG;
  return g->check(operation_seconds, checkpoint, ev);
}
// [[Rcpp::export]]
List cpp_runtime_report(SEXP runtime) {
  RuntimeGuard* g = runtime_ptr(runtime);
  if (!g) return List();
  List records(g->records.size());
  for (size_t i = 0; i < g->records.size(); ++i) {
    const GuardRecord& x = g->records[i];
    records[i] = List::create(_["checkpoint"] = x.checkpoint, _["phase"] = phase_name(x.event.phase),
      _["tier"] = x.event.tier, _["iter"] = x.event.iter, _["island"] = x.event.island, _["stage"] = x.event.stage,
      _["elapsed_seconds"] = x.elapsed, _["operation_seconds"] = x.operation,
      _["projected_seconds"] = x.elapsed + x.operation, _["allocation_seconds"] = x.allocation, _["exceeded"] = x.exceeded);
  }
  return List::create(_["label"] = "lead ruling 2026-10-22: operational guard, not a statistical setting",
    _["exceeded"] = g->exceeded, _["allocation_seconds"] = g->allocation, _["elapsed_seconds"] = g->elapsed(), _["checkpoints"] = records);
}

// D4 uses the uncapped >= threshold graph, independently of the strict/capped move graph.
// [[Rcpp::export]]
List cpp_cut_group(SEXP setup) {
  HPtr h = get_holder(setup); const Data& D = *h->D; const Start& st = *h->st;
  int p = D.p;
  std::vector<int> parent(p); for (int j = 0; j < p; ++j) parent[j] = j;
  std::function<int(int)> find = [&](int j) {
    while (parent[j] != j) { parent[j] = parent[parent[j]]; j = parent[j]; } return j;
  };
  std::vector<double> sd(p); for (int j = 0; j < p; ++j) sd[j] = std::sqrt(D.Gat(j, j));
  double rho = std::sqrt(2.0 * std::log((double)p) / D.n);
  for (int j = 0; j < p; ++j) for (int k = j + 1; k < p; ++k)
    if (std::fabs(D.Gat(j, k)) / (sd[j] * sd[k]) >= rho) {
      int a = find(j), b = find(k); if (a != b) parent[std::max(a, b)] = std::min(a, b);
    }
  std::map<int, std::vector<int>> comp;
  for (int j = 0; j < p; ++j) comp[find(j)].push_back(j);
  List flagged;
  for (const auto& kv : comp) {
    std::set<int> blocks; for (int j : kv.second) blocks.insert(st.blk[j] + 1);
    if (blocks.size() >= 2) flagged.push_back(List::create(_["size"] = (int)kv.second.size(),
      _["block_span"] = (int)blocks.size(), _["members"] = to_orig(D, kv.second),
      _["blocks"] = IntegerVector(blocks.begin(), blocks.end())));
  }
  return List::create(_["cut_group"] = flagged.size() > 0, _["count"] = (int)flagged.size(),
    _["components"] = flagged, _["threshold"] = rho,
    _["graph"] = "uncapped abs(sample correlation) >= threshold; no forced partner");
}

// [[Rcpp::export]]
List cpp_numerical_routes(SEXP ctx) {
  HPtr h = get_holder(ctx); const Data& D = *h->D;
  return List::create(_["chol"] = (double)D.routes[0], _["chol_refactor"] = (double)D.routes[1],
    _["qr"] = (double)D.routes[2], _["Q_recomputed"] = (double)D.q_recomputed_count,
    _["numerical_failures"] = (double)D.numerical_failures);
}
