
// =====================================================================================================================
// O-LS0 test-only exports. APPENDED by ls0_core.R to a TESTING COPY of the production core's cpp/v3_core.cpp
// (the pattern of the core README: "test-only exports are appended ... to testing copies"). The production sources are
// copied byte-for-byte and verified against core/source_manifest.json before this block is appended; nothing above
// this line is changed. Every function below reuses the production objects: the Holder built by cpp_setup (blocks,
// tables, pi_0, neighbour graph), the production Scorer, the production Engine::local_search, the production
// start_mode() of v3_start.h (max-plus convolution; the export was removed from production but the header kept it),
// and the production Ledger (HPM rule).
// =====================================================================================================================

// Start mode S~0 = argmax pi_0, exactly (v3_start.h start_mode; ties: smaller size, then lexicographic).
// [[Rcpp::export]]
List cpp_ls0_start_mode(SEXP setup) {
  HPtr h = get_holder(setup); if (!h->has_start) stop("setup required");
  ModeResult m = start_mode(*h->st);
  return List::create(_["model"] = to_orig(*h->D, m.S), _["log_gamma0"] = m.lg0,
                      _["log_pi0"] = m.lg0 - h->st->logZbar0, _["ties"] = (double)m.ties, _["truncated"] = m.truncated);
}

// The production local search (Engine::local_search, v3_engine.h) from a given centre, standalone: own Ledger (so the
// best model scored by this search is tracked with the production HPM rule), no cache (every evaluation is a fresh
// score; n_evaluated = logical score count), no runtime guard. emit_centre = TRUE scores the centre as an event
// (W3-VT38E caveat: LS0 must emit its centre).
// [[Rcpp::export]]
List cpp_ls0_local_search(SEXP setup, SEXP centre, int ell, bool emit_centre) {
  HPtr h = get_holder(setup); if (!h->has_graph) stop("setup required");
  const Data& D = *h->D; const Start& st = *h->st;
  Engine E(D, st, h->Nb, h->B);
  Ledger led(&D, 4);
  E.led = &led;
  auto t0 = Clock::now();
  LocalArchive A = E.local_search(to_internal(D, centre), ell, 0, emit_centre, -2);
  double sec = secs_since(t0);
  List out = local_to_list(A, D);
  out["seconds"] = sec;
  out["best_scored"] = led.has_hpm ? to_orig(D, led.hpmS) : IntegerVector(0);
  out["best_scored_F"] = led.has_hpm ? led.hpmF : NA_REAL;
  out["fresh_local"] = (double)led.fresh[PH_LOCAL][ME_LOCAL];
  return out;
}

// Exact pi_0(R_d), d = 0..d_max, R_d = {U u P : U subset S0, P subset S0^c, |P| <= d}, by a (size, #nulls) log-space
// convolution over the production blocks and tables (same objects as pi_0 itself; THEORY_MEASURES.md recipe).
// S0 = retained original indices of the truth. Returns log pi_0(R_d).
// [[Rcpp::export]]
NumericVector cpp_ls0_pi0_Rd(SEXP setup, IntegerVector S0, int d_max) {
  HPtr h = get_holder(setup); if (!h->has_start) stop("setup required");
  const Data& D = *h->D; const Start& st = *h->st;
  std::vector<int> s0 = to_internal(D, S0);
  std::vector<char> truth(D.p, 0); for (int j : s0) truth[j] = 1;
  int K = D.K, Q = d_max;
  // A[k][q]: log sum over partial models of the first b blocks with size k and q nulls (q <= Q)
  std::vector<std::vector<double>> A(K + 1, std::vector<double>(Q + 1, NEG_INF)), An;
  A[0][0] = 0.0;
  for (int b = 0; b < st.J; ++b) {
    int m = (int)st.blocks[b].size();
    uint32_t nullmask = 0; for (int i = 0; i < m; ++i) if (!truth[st.blocks[b][i]]) nullmask |= (1u << i);
    std::vector<std::vector<std::vector<double>>> terms(m + 1, std::vector<std::vector<double>>(Q + 1));
    for (uint32_t c = 0; c < (1u << m); ++c) {
      int j = __builtin_popcount(c), q = __builtin_popcount(c & nullmask);
      if (j > K || q > Q) continue;
      terms[j][q].push_back(st.logr[b][c]);
    }
    std::vector<std::vector<double>> e(m + 1, std::vector<double>(Q + 1, NEG_INF));
    for (int j = 0; j <= m; ++j) for (int q = 0; q <= Q; ++q) if (!terms[j][q].empty()) e[j][q] = log_sum_exp(terms[j][q]);
    An.assign(K + 1, std::vector<double>(Q + 1, NEG_INF));
    for (int k = 0; k <= K; ++k) for (int q = 0; q <= Q; ++q) {
      std::vector<double> v;
      for (int j = 0; j <= std::min(m, k); ++j) for (int q1 = 0; q1 <= q; ++q1) {
        double a = e[j][q1], bb = A[k - j][q - q1];
        if (a != NEG_INF && bb != NEG_INF) v.push_back(a + bb);
      }
      if (!v.empty()) An[k][q] = log_sum_exp(v);
    }
    A.swap(An);
  }
  NumericVector out(Q + 1);
  for (int d = 0; d <= Q; ++d) {
    std::vector<double> v;
    for (int k = 0; k <= K; ++k) for (int q = 0; q <= d; ++q) if (A[k][q] != NEG_INF) v.push_back(D.logprior[k] + A[k][q]);
    out[d] = log_sum_exp(v) - st.logZbar0;
  }
  return out;
}

// cpp_final_run with LS0 INTEGRATED (step 5 check). Byte-for-byte the production cpp_final_run, plus ONE block after
// the final local search: S~0 = start_mode(st); LS0 = E.local_search(S~0, ell, tier, emit_centre = true, iter = -2)
// on the SAME ledger and cache, so its scores update the reported HPM through the production HPM rule. LS0 consumes no
// random numbers. Extra outputs: hpm_before_ls0, ls0, start_mode, seconds_ls0.
// [[Rcpp::export]]
List cpp_final_run_ls0(SEXP setup, NumericVector grid, List ro, double seed, SEXP inherited, SEXP runtime) {
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
  List local, hpm_before, ls0, hpm_before_ls0, smode;
  double sec_local = 0, sec_ls0 = 0;
  std::vector<IslandResult> res;
  try {
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
      RngSource rng; rng.g.seed_stream((uint64_t)seed, (uint64_t)(9 + r));
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
    LocalArchive A = E.local_search(led.hpmS, o.ell, o.tier, false);
    sec_local = secs_since(t0);
    local = local_to_list(A, D);
    if (E.guard && E.guard->check(sec_local, "local_search", local_event(o.tier, -1))) status = "resource_limit";
    // ---------------- O-LS0 addition (the only change) ----------------
    if (status == "completed") {
      hpm_before_ls0 = List::create(_["model"] = to_orig(D, led.hpmS), _["F"] = led.hpmF,
                                    _["provenance"] = event_to_list(led.hpm_ev, led.hpm_mech));
      auto t1 = Clock::now();
      ModeResult m = start_mode(st);
      smode = List::create(_["model"] = to_orig(D, m.S), _["log_gamma0"] = m.lg0, _["ties"] = (double)m.ties, _["truncated"] = m.truncated);
      LocalArchive A0 = E.local_search(m.S, o.ell, o.tier, true, -2);
      sec_ls0 = secs_since(t1);
      ls0 = local_to_list(A0, D);
      if (E.guard && E.guard->check(sec_ls0, "ls0", local_event(o.tier, -2))) status = "resource_limit";
    }
    // -------------------------------------------------------------------
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
  out["hpm_before_ls0"] = hpm_before_ls0; out["ls0"] = ls0; out["start_mode"] = smode; out["seconds_ls0"] = sec_ls0;
  return out;
}
