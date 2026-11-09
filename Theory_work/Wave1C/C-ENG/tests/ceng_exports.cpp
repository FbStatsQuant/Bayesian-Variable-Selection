
// =====================================================================================================================
// C-ENG test-only exports. APPENDED by ceng_load.R to a TESTING COPY of cpp/v3_core.cpp (core README policy:
// "Test-only exports are appended ... to testing copies"). Nothing in the production sources is changed by this file.
// =====================================================================================================================

// A start built from abstract tables (W1-N3 STATEMENT §1 instance): p, K, lambda = logprior[0..K], blocks (0-based
// internal indices, increasing within a block, any block order), logr[b] of length 2^|C_b| (entries with |U| > K are
// ignored by start_mode; pass NaN there). No data, no scorer.
struct TStart { Data D; Start st; };

// [[Rcpp::export]]
SEXP t_make_start(int p, int K, NumericVector logprior, List blocks, List logr) {
  TStart* t = new TStart();
  t->D.p = p; t->D.K = K; t->D.W = nwords(p);
  t->D.logprior.assign(logprior.begin(), logprior.end());
  if ((int)t->D.logprior.size() != K + 1) { delete t; stop("logprior must have length K + 1"); }
  t->st.D = &t->D;
  for (int b = 0; b < blocks.size(); ++b) {
    IntegerVector bl = blocks[b]; NumericVector lr = logr[b];
    t->st.blocks.push_back(std::vector<int>(bl.begin(), bl.end()));
    if (lr.size() != ((R_xlen_t)1 << bl.size())) { delete t; stop("table %d has the wrong length", b + 1); }
    t->st.logr.push_back(std::vector<double>(lr.begin(), lr.end()));
  }
  t->st.J = (int)t->st.blocks.size();
  t->st.blk.assign(p, -1); t->st.pos.assign(p, -1);
  for (int b = 0; b < t->st.J; ++b) for (size_t i = 0; i < t->st.blocks[b].size(); ++i) {
    int x = t->st.blocks[b][i];
    if (x < 0 || x >= p || t->st.blk[x] >= 0) { delete t; stop("blocks must partition 0..p-1"); }
    t->st.blk[x] = b; t->st.pos[x] = (int)i;
  }
  for (int x = 0; x < p; ++x) if (t->st.blk[x] < 0) { delete t; stop("blocks do not cover column %d", x); }
  build_start(t->st);
  return XPtr<TStart>(t, true);
}

// [[Rcpp::export]]
List t_start_mode(SEXP xp, double cap, bool tie_dp) {
  XPtr<TStart> t(xp);
  ModeResult m = start_mode(t->st, (long)cap, tie_dp);
  return List::create(_["S"] = IntegerVector(m.S.begin(), m.S.end()), _["lg0"] = m.lg0, _["ties"] = (double)m.ties,
                      _["truncated"] = m.truncated, _["tie_dp_used"] = m.tie_dp_used,
                      _["lg0_direct"] = t->st.log_gamma0(m.S));
}

// TDP-E alone (no enumeration).
// [[Rcpp::export]]
IntegerVector t_tdp(SEXP xp) {
  XPtr<TStart> t(xp);
  ModeDP dp = mode_dp(t->st);
  std::vector<int> S = mode_tie_dp(t->st, dp);
  return IntegerVector(S.begin(), S.end());
}

// Brute force over Omega_K with the code's own evaluation ghat = log_gamma0: smallest size among ghat-maximisers, then
// lex-min (lex_less). p <= 24.
// [[Rcpp::export]]
List t_brute_mode(SEXP xp) {
  XPtr<TStart> t(xp); const Start& st = t->st; int p = t->D.p, K = t->D.K;
  if (p > 24) stop("brute force needs p <= 24");
  double best = NEG_INF; std::vector<int> bestS; bool have = false; double nmax = 0;
  std::vector<int> S;
  for (uint32_t mask = 0; mask < (1u << p); ++mask) {
    if (__builtin_popcount(mask) > K) continue;
    S.clear(); for (int i = 0; i < p; ++i) if (mask & (1u << i)) S.push_back(i);
    double v = st.log_gamma0(S);
    if (!have || v > best) { best = v; bestS = S; have = true; nmax = 1; continue; }
    if (v == best) {
      if (S.size() < bestS.size()) { bestS = S; nmax = 1; }
      else if (S.size() == bestS.size()) { nmax += 1; if (lex_less(S, bestS)) bestS = S; }
    }
  }
  return List::create(_["S"] = IntegerVector(bestS.begin(), bestS.end()), _["lg0"] = best, _["N"] = nmax);
}

// Standalone production local search on a setup (own ledger, no cache), with a phase label: used to check that
// LS0 = local_search(S~0, ell, tier, emit_centre = true, -1, PH_LS0).
// [[Rcpp::export]]
List t_local_search(SEXP setup, SEXP centre, int ell, bool emit_centre, bool ls0_phase) {
  HPtr h = get_holder(setup); const Data& D = *h->D;
  Engine E(D, *h->st, h->Nb, h->B);
  Ledger led(&D, 4); E.led = &led;
  LocalArchive A = E.local_search(to_internal(D, centre), ell, 0, emit_centre, -1, ls0_phase ? PH_LS0 : PH_LOCAL);
  List out = local_to_list(A, D);
  out["ledger"] = ledger_to_list(led, D, true);
  return out;
}

// Start mode of a production setup.
// [[Rcpp::export]]
List t_setup_start_mode(SEXP setup, double cap, bool tie_dp) {
  HPtr h = get_holder(setup);
  ModeResult m = start_mode(*h->st, (long)cap, tie_dp);
  return List::create(_["model"] = to_orig(*h->D, m.S), _["lg0"] = m.lg0, _["ties"] = (double)m.ties,
                      _["truncated"] = m.truncated, _["tie_dp_used"] = m.tie_dp_used);
}
