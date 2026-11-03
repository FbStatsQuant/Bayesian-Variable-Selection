
// =====================================================================================================================
// METH-AUDIT test-only exports. APPENDED by ma_core.R to a TESTING COPY of the production cpp/v3_core.cpp (same pattern
// as O-LS0's ls0_exports.cpp). Nothing above this block is changed. These functions reuse the production Engine,
// Ledger, ScoreCache, Holder and local search; they only change WHICH objects an island shares:
//   cpp_ma_island      one final island on stream `stream`, with its OWN Ledger and OWN ScoreCache (a worker's view);
//   cpp_ma_local       the production local search from a given centre, own Ledger, no cache, centre not emitted.
// Purpose: test that running final islands as independent workers (separate caches and ledgers, any order, any
// concurrency) gives bitwise the same island estimates as the production serial loop, and time the pieces.
// =====================================================================================================================

// [[Rcpp::export]]
List cpp_ma_island(SEXP setup, NumericVector grid, int N, int L, int Hm, int tier, double seed, double stream,
                   int island_label, double cache_capacity, bool with_tables) {
  HPtr h = get_holder(setup); const Data& D = *h->D; const Start& st = *h->st;
  if (!h->has_graph) stop("setup required");
  std::vector<double> g(grid.begin(), grid.end());
  auto t0 = Clock::now();
  Ledger led(&D, island_label);
  if (with_tables) ingest_tables(led, *h);
  ScoreCache cache; cache.init(D.W, (size_t)cache_capacity);
  Engine E(D, st, h->Nb, h->B);
  E.cache = &cache; E.led = &led; E.guard = nullptr;
  RngSource rng; rng.g.seed_stream((uint64_t)seed, (uint64_t)stream);
  E.vs = &rng;
  IslandResult res = E.run_island(island_label, N, g, L, Hm, tier, nullptr);
  double sec = secs_since(t0);
  List island = island_to_list(res, D);
  island["stream"] = List::create(_["stream"] = stream, _["position_end"] = (double)rng.g.count,
                                  _["init_draws_hash"] = hex64(res.init_hash));
  return List::create(_["island"] = island, _["ledger"] = ledger_to_list(led, D), _["seconds_total"] = sec,
                      _["cache_hits"] = (double)cache.hits, _["cache_misses"] = (double)cache.misses,
                      _["cache_clears"] = (double)cache.clears);
}

// [[Rcpp::export]]
List cpp_ma_local(SEXP setup, SEXP centre, int ell, int tier) {
  HPtr h = get_holder(setup); if (!h->has_graph) stop("setup required");
  const Data& D = *h->D; const Start& st = *h->st;
  Engine E(D, st, h->Nb, h->B);
  Ledger led(&D, 4);
  E.led = &led;
  auto t0 = Clock::now();
  LocalArchive A = E.local_search(to_internal(D, centre), ell, tier, false);
  List out = local_to_list(A, D);
  out["seconds"] = secs_since(t0);
  out["best_scored"] = led.has_hpm ? to_orig(D, led.hpmS) : IntegerVector(0);
  out["best_scored_F"] = led.has_hpm ? led.hpmF : NA_REAL;
  return out;
}
