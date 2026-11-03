
// =====================================================================================================================
// ABL-START test-only export. APPENDED by abl_core.R to a TESTING COPY of the production cpp/v3_core.cpp (pattern of
// METH-AUDIT's ma_exports.cpp). Nothing above this block is changed.
//   cpp_abl_setup(ctx, B, mode, logr_R)  -- the production cpp_setup, except for WHICH start pi_0 is built:
//     mode 0: production (blocks of size <= B, tables scored on the full y)            [arm A; must equal cpp_setup]
//     mode 1: blocks of size 1 (make_blocks(D, 1)), exact single-variable tables     [arm B; independent Bernoulli]
//     mode 2: blocks of size 1 with every log r_b set to 0 => pi_0 = capped model prior [arm C]
//     mode 3: production blocks, log r_b(U) supplied from R (logr_R, list over blocks) [arm D; e.g. backfit tables]
//   In every mode the kernel block parameter (h->B, so m = p + B + 2 labels per round) and the neighbour graph
//   N(j) = neighbour_graph(D, B) are the PRODUCTION ones; the HPM table ingestion uses logm_tab (true full-y scores
//   of the table entries of the blocks actually used). pi_0 is always built by the production build_start
//   (exact size-profile convolution, exact normaliser Zbar_0, exact sampler), so log Zhat stays unbiased.
// =====================================================================================================================
// [[Rcpp::export]]
List cpp_abl_setup(SEXP ctx, int B, int mode, SEXP logr_R) {
  HPtr h = get_holder(ctx);
  check_B(B);
  Holder* g = new Holder(); g->D = h->D; g->B = B;
  const Data& D = *g->D;
  g->st = std::make_shared<Start>(); Start& st = *g->st; st.D = &D;
  int Bst = (mode == 1 || mode == 2) ? 1 : B;
  st.B = Bst;
  auto t0 = Clock::now();
  st.blocks = make_blocks(D, Bst);
  g->block_seconds = secs_since(t0); t0 = Clock::now();
  Scorer sc(&D);
  build_tables(st, sc);   // numerical failures propagate as an R error (none expected on study designs)
  if (mode == 2) {
    for (auto& v : st.logr) for (size_t c = 0; c < v.size(); ++c) if (!std::isnan(v[c])) v[c] = 0.0;
  } else if (mode == 3) {
    List l(logr_R);
    if (l.size() != st.J) stop("logr_R must have one entry per production block (%d)", st.J);
    for (int b = 0; b < st.J; ++b) {
      NumericVector v = l[b];
      if ((size_t)v.size() != st.logr[b].size()) stop("logr_R[[%d]] has the wrong length", b + 1);
      for (size_t c = 0; c < st.logr[b].size(); ++c) {
        if (std::isnan(st.logr[b][c])) continue;
        if (!std::isfinite(v[c])) stop("logr_R[[%d]][%d] not finite", b + 1, (int)c + 1);
        st.logr[b][c] = (c == 0) ? 0.0 : v[c];
      }
    }
  }
  g->table_seconds = secs_since(t0); t0 = Clock::now();
  build_start(st);
  g->start_seconds = secs_since(t0); t0 = Clock::now();
  g->Nb = neighbour_graph(D, B);
  g->graph_seconds = secs_since(t0);
  g->has_start = true; g->has_graph = true;
  HPtr ptr(g, true);
  List tables(st.J);
  for (int b = 0; b < st.J; ++b)
    tables[b] = List::create(_["members"] = to_orig(D, st.blocks[b]), _["log_r"] = NumericVector(st.logr[b].begin(), st.logr[b].end()),
                             _["log_m"] = NumericVector(st.logm_tab[b].begin(), st.logm_tab[b].end()));
  List s = start_summary(*g);
  return List::create(_["status"] = "ok", _["ptr"] = ptr, _["B"] = B, _["B_start"] = Bst, _["mode"] = mode,
                      _["blocks"] = blocks_to_R(D, st.blocks), _["tables"] = tables,
                      _["start"] = s, _["neighbours"] = models_to_list(D, g->Nb),
                      _["seconds"] = NumericVector::create(_["blocks"] = g->block_seconds, _["tables"] = g->table_seconds,
                                                           _["start"] = g->start_seconds, _["neighbours"] = g->graph_seconds));
}

// log pi_0(S) under a setup's start (S in original indices); -Inf if infeasible.
// [[Rcpp::export]]
double cpp_abl_logpi0(SEXP setup, IntegerVector S) {
  HPtr h = get_holder(setup); const Data& D = *h->D;
  std::vector<int> s = to_internal(D, S);
  if ((int)s.size() > D.K) return R_NegInf;
  return h->st->log_pi0(s);
}
