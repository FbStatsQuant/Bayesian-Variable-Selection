
// APPENDED ONLY TO A TESTING COPY of v3_core.cpp. No production test switches.
// [[Rcpp::export]]
List test_rng(double seed, int stream, int n) {
  Xoshiro256ss g; g.seed_stream((uint64_t)seed, (uint64_t)stream);
  NumericVector u(n); for (int i = 0; i < n; ++i) u[i] = g.uniform();
  CharacterVector state(4); for (int i = 0; i < 4; ++i) state[i] = hex64(g.s[i]);
  double count = (double)g.count; std::string next = hex64(g.next());
  return List::create(_["uniforms"] = u, _["state"] = state, _["count"] = count, _["next"] = next);
}

// [[Rcpp::export]]
List test_pilot(NumericVector d, double phi, double H, int Te) {
  auto r = pilot_next_phi(as<std::vector<double>>(d), phi, H, Te);
  return List::create(_["phi"] = r.phi, _["forced"] = r.forced);
}

// [[Rcpp::export]]
List test_schedule(NumericVector dx, double H, int Te) {
  auto d = as<std::vector<double>>(dx); std::vector<double> grid{0}; int forced = 0;
  while (grid.back() < 1 && (int)grid.size() <= Te + 2) {
    auto r = pilot_next_phi(d, grid.back(), H, Te);
    if (!(r.phi > grid.back())) stop("non-progress in test pilot schedule");
    grid.push_back(r.phi); forced += r.forced;
  }
  return List::create(_["schedule"] = grid, _["forced_pilot_steps"] = forced);
}

// [[Rcpp::export]]
List test_grid(NumericVector lg, NumericVector d, NumericVector targets, int Te) {
  auto g = build_grid(as<std::vector<double>>(lg), as<std::vector<double>>(d), as<std::vector<double>>(targets), Te);
  return List::create(_["grid"] = g.grid, _["rho"] = g.rho, _["ok"] = g.ok, _["reason"] = g.reason,
                      _["evaluations"] = (double)g.evals);
}

struct TestUniforms : public VariateSource {
  std::vector<double> v; size_t i = 0;
  double u(const char*) override { if (i >= v.size()) throw std::runtime_error("test uniforms exhausted"); return v[i++]; }
};

// [[Rcpp::export]]
List test_resample(SEXP setup, NumericVector lw, NumericVector uniforms, double seed) {
  auto h = get_holder(setup); Engine E(*h->D, *h->st, h->Nb, h->B);
  TestUniforms prescribed; prescribed.v = as<std::vector<double>>(uniforms);
  RngSource rng; rng.g.seed_stream((uint64_t)seed, 101);
  E.vs = uniforms.size() ? (VariateSource*)&prescribed : (VariateSource*)&rng;
  auto a = E.resample(as<std::vector<double>>(lw));
  // Separate frozen reference arithmetic; exact W boundary probes are generated in R from these bits.
  std::vector<double> W(lw.size()); double mx = NEG_INF, c = 0;
  for (double x : lw) mx = std::max(mx, x);
  for (int i = 0; i < lw.size(); ++i) { c += std::exp(lw[i] - mx); W[i] = c; }
  for (double& x : W) x /= c; W.back() = 1;
  CharacterVector state(4); for (int i = 0; i < 4; ++i) state[i] = hex64(rng.g.s[i]);
  return List::create(_["ancestors"] = a, _["W_reference"] = W, _["rng_state"] = state,
                      _["draw_count"] = (double)rng.g.count, _["prescribed_count"] = (double)prescribed.i);
}

// [[Rcpp::export]]
NumericVector test_adjacent(NumericVector x, bool up) {
  NumericVector y(x.size()); for (int i = 0; i < x.size(); ++i)
    y[i] = std::nextafter(x[i], up ? POS_INF : NEG_INF);
  return y;
}

// [[Rcpp::export]]
List test_islands(SEXP setup, NumericVector grid, double seed, int N, int L, int ell, int stream0, bool adaptive, int Te) {
  auto h = get_holder(setup); const Data& D = *h->D;
  Ledger led(&D, 4);
#if TEST_PRODUCTION
  ingest_tables(led, *h);
#else
  ingest_tables(led, nullptr, *h);
#endif
  ScoreCache cache; cache.init(D.W, (size_t)std::max(500 * D.p, 32768));
  Engine E(D, *h->st, h->Nb, h->B); E.led = &led; E.cache = &cache;
  List islands, states, locals;
  std::vector<double> g(grid.begin(), grid.end());
  for (int r = 1; r <= (adaptive ? 1 : 4); ++r) {
    RngSource rng; rng.g.seed_stream((uint64_t)seed, (uint64_t)(stream0 + r - 1)); E.vs = &rng;
    Engine::Schedule sch; sch.grid = &g; sch.adaptive = adaptive; sch.H = N; sch.Te = Te;
    auto z = E.run_island_s(r, N, sch, L, 4, 0, nullptr,
#if !TEST_PRODUCTION
      false,
#endif
      adaptive ? PH_PILOT : -1, 0);
    islands.push_back(island_to_list(z, D));
    CharacterVector state(4); for (int i = 0; i < 4; ++i) state[i] = hex64(rng.g.s[i]);
    double count = (double)rng.g.count; std::string next = hex64(rng.g.next());
    states.push_back(List::create(_["state"] = state, _["count"] = count, _["next"] = next));
  }
  auto a = E.local_search(led.hpmS, ell, 0, false);
  return List::create(_["islands"] = islands, _["rng"] = states, _["local"] = local_to_list(a, D),
                      _["hpm"] = to_orig(D, led.hpmS), _["hpm_F"] = led.hpmF,
                      _["leaders0"] = store_to_list(led.lead0, D), _["leaders1"] = store_to_list(led.lead1, D),
                      _["near_store"] = store_to_list(led.top, D));
}

// [[Rcpp::export]]
List test_local(SEXP setup, IntegerVector centre, int ell) {
  auto h = get_holder(setup); const Data& D = *h->D;
  Ledger led(&D, 4); Engine E(D, *h->st, h->Nb, h->B); E.led = &led;
  auto a = E.local_search(to_internal(D, centre), ell, 0, true);
  return List::create(_["archive"] = local_to_list(a, D), _["hpm"] = to_orig(D, led.hpmS), _["F"] = led.hpmF);
}

// Actual final orchestration and all-scored ledger, small settings supplied only here.
// [[Rcpp::export]]
List test_final(SEXP setup, NumericVector grid, List ro, double seed, SEXP inherited) {
#if TEST_PRODUCTION
  return cpp_final_run(setup, grid, ro, seed, inherited, R_NilValue);
#else
  return cpp_final_run(setup, grid, ro, seed, R_NilValue, inherited, R_NilValue, R_NilValue, false);
#endif
}

// [[Rcpp::export]]
List test_cal_rng(SEXP state) {
  CPtr c(state); List out;
  for (const auto& kv : c->streams) {
    auto g = kv.second.g; CharacterVector s(4);
    for (int i = 0; i < 4; ++i) s[i] = hex64(g.s[i]);
    double count = (double)g.count; std::string next = hex64(g.next());
    out.push_back(List::create(_["stream"] = kv.first, _["state"] = s,
      _["count"] = count, _["next"] = next));
  }
  return out;
}

// PRODUCTION_ONLY_WRAPPERS
#if TEST_PRODUCTION
// Mutates ONLY a fresh testing copy of context/holder. Arbitrary Gram matrices
// permit exact floating-point threshold and disconnected/capped-graph fixtures.
// [[Rcpp::export]]
List test_cut(NumericMatrix correlation, IntegerVector orig, IntegerVector block, int n) {
  int p = correlation.ncol();
  HPtr h(new Holder(), true); h->D.reset(new Data()); h->st.reset(new Start());
  h->D->n = n; h->D->p = p; h->D->orig = as<std::vector<int>>(orig);
  h->D->G = as<std::vector<double>>(correlation); h->st->blk = as<std::vector<int>>(block);
  return cpp_cut_group(h);
}

// Test the strict > boundary without introducing a clock option into production:
// allocation is set to elapsed()+operation, with operation=2^100 so the actual
// clock increment is far below half an ULP. Nextafter probes the two neighbours.
// [[Rcpp::export]]
List test_guard_boundary() {
  RuntimeGuard g; EventCtx e; double op = std::ldexp(1.0, 100);
  g.allocation = op;
  bool equal = g.check(op, "equal", e);
  RuntimeGuard below; below.allocation = std::nextafter(op, NEG_INF);
  bool strict = below.check(op, "strict", e);
  RuntimeGuard above; above.allocation = std::nextafter(op, POS_INF);
  bool safe = above.check(op, "safe", e);
  return List::create(_["equality_stops"] = equal, _["strict_stops"] = strict, _["safe_stops"] = safe);
}

// [[Rcpp::export]]
void test_runtime_elapsed(SEXP runtime, double elapsed) {
  runtime_ptr(runtime)->elapsed_before = elapsed;
}
#endif
