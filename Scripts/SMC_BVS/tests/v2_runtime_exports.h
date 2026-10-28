// TEST TRANSLATION UNIT ONLY. Append these contents after production v3_core.cpp.
// No include, macro, hook, or exported testing interface is added to production.
// Rcpp's export parser must see these contents in the generated testing .cpp.

struct V2TestBadCrossProduct {
  Data& D;
  int column;
  double saved;
  explicit V2TestBadCrossProduct(Data& data, int j = 0) : D(data), column(j), saved(data.z.at(j)) {
    D.z[column] = std::numeric_limits<double>::quiet_NaN();
  }
  ~V2TestBadCrossProduct() { D.z[column] = saved; }
};

// Score a cross-block best through the real calibration Engine/Ledger, then
// export the ordinary inherited state with its complete first-score event.
// Singleton tables and a strong two-predictor signal make this best absent
// from the tables. Corrupt a different column, before/after the best in the
// exported lexicographic model order; ALL THREE real scorer routes then fail.
// [[Rcpp::export]]
List test_v2_final_rescore_failure(SEXP setup, List ro, double seed, bool after_hpm) {
  HPtr h = get_holder(setup);
  if (h->D->p < 4 || h->D->K < 2) stop("test requires four predictors and a feasible pair");
  const Data& D = *h->D;
  Ledger baseline(&D, as<int>(ro["islands"])); ingest_tables(baseline, *h);
  List before = ledger_to_list(baseline, D);
  RObject state(cpp_cal_new(setup, seed, ro, R_NilValue));
  CPtr c(state);
  Engine& E = *c->E;
  E.ev.phase = PH_DIAG; E.ev.tier = 1; E.ev.island = 2; E.ev.stage = 3;
  E.ev.round = 4; E.ev.particle = 5; E.ev.position = 6; E.ev.phi = 0.625; E.ev.iter = 2;
  Particle best; E.set_model(best, std::vector<int>{1, 2}); E.eval(best, ME_GIBBS_FLIP);
  if (!hpm_better(best.F, best.S, baseline.hpmF, baseline.hpmS)) stop("cross-block control must beat all table models");
  for (auto& block : h->st->blocks)
    if (std::includes(block.begin(), block.end(), best.S.begin(), best.S.end())) stop("control best belongs to a table");
  List exported = cpp_cal_export(state);
  List inherited = exported["inherited"];
  auto Ms = models_from_R(D, inherited["models"]);
  int bad = after_hpm ? 3 : 0;
  size_t fail_at = Ms.size(), best_at = Ms.size();
  for (size_t i = 0; i < Ms.size(); ++i) {
    if (Ms[i] == best.S) best_at = i;
    if (fail_at == Ms.size() && std::find(Ms[i].begin(), Ms[i].end(), bad) != Ms[i].end()) fail_at = i;
  }
  if (fail_at == Ms.size() || best_at == Ms.size() || (after_hpm ? fail_at <= best_at : fail_at >= best_at))
    stop("inherited order does not exercise requested failure position");
  Scorer sc(&D); double control = sc.score(std::vector<int>{bad}).logm;
  uint64_t routes = D.routes[ROUTE_CHOL] + D.routes[ROUTE_REFACTOR] + D.routes[ROUTE_QR];
  uint64_t failures = D.numerical_failures;
  List raw;
  {
    V2TestBadCrossProduct fault(*h->D, bad);
    raw = cpp_final_run(setup, NumericVector::create(0.0, 1.0), ro, seed, inherited, R_NilValue);
  }
  return List::create(_["raw"] = raw, _["ledger_before"] = before, _["control_log_m"] = control,
                      _["calibration_export"] = exported, _["scored_best_log_m"] = best.logm,
                      _["failure_model"] = to_orig(D, std::vector<int>{bad}), _["expected_successful_rescores"] = (double)fail_at,
                      _["successful_rescore_delta"] = (double)(D.routes[ROUTE_CHOL] + D.routes[ROUTE_REFACTOR] + D.routes[ROUTE_QR] - routes),
                      _["scorer_failure_delta"] = (double)(D.numerical_failures - failures));
}

// This is also usable as the R tier's cpp_cal_V callback: it calls the actual
// production cpp_cal_V and returns its failure result after restoring the data.
// Callers can retain the control and failure count separately as test evidence.
// [[Rcpp::export]]
List test_v2_V_rescore_failure(SEXP state) {
  CPtr c(state);
  Data& D = *c->h->D;
  if (D.p < 1 || D.K < 1) stop("test requires a feasible singleton");
  List control = cpp_cal_V(state);
  if (control.containsElementNamed("status")) stop("control V unexpectedly failed");
  uint64_t failures = D.numerical_failures;
  List result;
  {
    V2TestBadCrossProduct fault(D);
    result = cpp_cal_V(state);
  }
  return List::create(_["result"] = result, _["control"] = control,
                      _["scorer_failure_delta"] = (double)(D.numerical_failures - failures));
}
