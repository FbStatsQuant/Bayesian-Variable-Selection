// wp4_harness.cpp -- TEST CODE ONLY. Appended to an unmodified COPY of core/cpp/v3_core.cpp (one translation unit,
// core headers unchanged, v3 flags from core/cpp/Makevars.v3) by tests/golden/wp4_golden.R. It drives the WP4 code
// (v4::calib::Driver, v4::merge::merge_and_tail) with the core/ engine as the island backend, so that WP4's control
// flow, grid rules, V re-scoring, ledger merge, threaded tail and assembly can be compared bit for bit with
// core/v3_calib.R::v3_calibrate and core/v3_run.R::v3_final_run (compat mode, until WP1/WP3's compat islands land).
// [[Rcpp::plugins(openmp)]]
#include <v4/calib.h>
#include <v4/merge.h>
#include <v4/prep.h>
#include <v4/provenance.h>
#include <v4/stubs.h>
#include <v4/wp4_io.h>
// The engine library (libv4_bit.a, built with -fPIC by wp4_golden.R) is linked into this module.

namespace wp4h {

// Per-thread evaluator over core's Scorer and Start (= core/cpp/v3_engine.h:84-90 and v3_core.cpp:714-715).
struct CoreEval {
  const v3::Data* D; const v3::Start* st; v3::Scorer sc; std::vector<std::pair<int, int>> scratch;
  long fail_at = -1; long* counter = nullptr;   // fault injection (T10): throw at the fail_at-th evaluation
  CoreEval(const v3::Data* d, const v3::Start* s) : D(d), st(s), sc(d) {}
  void operator()(const v4::Model& S, double& lm, double& lg0, double& dd, double& F) {
    try { lm = sc.score(S).logm; } catch (v3::NumericalFailure& e) { throw v4::NumericalFailure(std::string(e.what()).substr(19)); }
    double c = st->comp(S, scratch);
    int k = (int)S.size();
    lg0 = D->logprior[k] + c; dd = (lm - D->logm0) - c; F = D->logprior[k] + lm;
  }
};
struct CoreFactory {
  const v3::Data* D; const v3::Start* st;
  CoreEval make() const { return CoreEval(D, st); }
};
// Fault-injecting factory: the evaluation of model `bad` throws NumericalFailure (deterministic in the model, so the
// failure does not depend on threads).
struct FaultEval : CoreEval {
  v4::Model bad;
  FaultEval(const v3::Data* d, const v3::Start* s, const v4::Model& b) : CoreEval(d, s), bad(b) {}
  void operator()(const v4::Model& S, double& lm, double& lg0, double& dd, double& F) {
    if (S == bad) throw v4::NumericalFailure("injected failure");
    CoreEval::operator()(S, lm, lg0, dd, F);
  }
};
struct FaultFactory {
  const v3::Data* D; const v3::Start* st; v4::Model bad;
  FaultEval make() const { return FaultEval(D, st, bad); }
};

inline v4::calib::CalStatus cal_status(const std::string& s) {
  if (s == "ok") return v4::calib::CalStatus::ok;
  if (s == "resource_limit") return v4::calib::CalStatus::resource_limit;
  return v4::calib::CalStatus::numerical_failure;
}

// Backend = the core calibration entry points (cpp_cal_pilot / cpp_cal_diag) on one persistent CalState, and V built
// as core/cpp/v3_core.cpp:705-708, re-scored by v4::calib::rescore_V (threaded).
struct CoreBackend : v4::calib::Backend {
  SEXP state; CPtr c; int threads;
  // fault hooks (test only), mirrored on the R side by wrappers of the same core entry points:
  bool preflight = false, force_ll_pilot = false; int fail_V_at = 0, fail_diag_at = 0, stop_grid_at = 0;
  int n_V = 0, n_diag = 0, n_grid = 0;
  CoreBackend(SEXP s, int th) : state(s), c(s), threads(th) {}
  bool preflight_exceeds(int) override { return preflight; }
  bool grid_stop(double, int, int) override { return ++n_grid == stop_grid_at; }
  v4::calib::PilotOut pilot(const v4::calib::TierSettings& ts) override {
    List r = cpp_cal_pilot(state, ts.tier, ts.H, ts.Te, ts.L, ts.Hm, ts.ell);
    v4::calib::PilotOut o; o.status = cal_status(as<std::string>(r["status"]));
    if (r.containsElementNamed("message")) o.message = as<std::string>(r["message"]);
    if (r.containsElementNamed("schedule")) { NumericVector s = r["schedule"]; o.schedule.assign(s.begin(), s.end()); }
    if (r.containsElementNamed("forced_pilot_steps")) { o.forced = as<int>(r["forced_pilot_steps"]); o.has_forced = true; }
    if (r.containsElementNamed("best_before_local")) {
      o.best_before_F = as<double>(List(r["best_before_local"])["F"]); o.best_after_F = as<double>(List(r["best_after_local"])["F"]);
      o.local_limit = as<bool>(List(r["local_search"])["local_limit"]) || force_ll_pilot;
    }
    return o;
  }
  v4::calib::DiagOut diag(const v4::calib::TierSettings& ts, const std::vector<double>& grid, int iter) override {
    List r = cpp_cal_diag(state, ts.tier, NumericVector(grid.begin(), grid.end()), ts.H, ts.L, ts.Hm, ts.ell, iter);
    if (++n_diag == fail_diag_at) { v4::calib::DiagOut f; f.status = v4::calib::CalStatus::numerical_failure; f.message = "forced"; return f; }
    v4::calib::DiagOut o; o.status = cal_status(as<std::string>(r["status"]));
    if (r.containsElementNamed("message")) o.message = as<std::string>(r["message"]);
    if (r.containsElementNamed("log_Z_r")) { NumericVector z = r["log_Z_r"]; o.logZ_r.assign(z.begin(), z.end()); }
    if (r.containsElementNamed("island_best")) { NumericVector b = r["island_best"]; o.island_best.assign(b.begin(), b.end()); }
    if (r.containsElementNamed("best_before_local")) {
      o.best_before_F = as<double>(List(r["best_before_local"])["F"]); o.best_after_F = as<double>(List(r["best_after_local"])["F"]);
      o.local_limit = as<bool>(List(r["local_search"])["local_limit"]);
    }
    return o;
  }
  v4::calib::VOut candidate_set() override {
    if (++n_V == fail_V_at) { v4::calib::VOut f; f.status = v4::calib::CalStatus::numerical_failure; f.message = "forced"; return f; }
    std::set<std::vector<int>> V;   // core/cpp/v3_core.cpp:705-708
    V.insert(std::vector<int>());
    for (auto& e : c->led->lead0.s) V.insert(e.S);
    for (auto& e : c->led->lead1.s) V.insert(e.S);
    std::vector<v4::Model> Vm(V.begin(), V.end());
    CoreFactory fac{c->h->D.get(), c->h->st.get()};
    return v4::calib::rescore_V(Vm, fac, threads);
  }
};

inline List grid_rec(const v4::calib::GridRecord& g) {
  return List::create(_["label"] = g.label, _["grid"] = g.grid, _["rho_appended"] = g.rho, _["ok"] = g.ok, _["reason"] = g.reason,
                      _["intervals"] = (int)g.grid.size() - 1, _["F_V_evaluations"] = (double)g.evals, _["V_size"] = (double)g.V_size);
}
inline SEXP trig_list(const v4::calib::TierOut& t) {
  if (!t.has_triggers) return R_NilValue;
  const auto& x = t.triggers;
  return List::create(_["E1"] = x.E1, _["E2"] = x.E2, _["E3"] = x.E3, _["forced_pilot_steps"] = x.forced_pilot_steps,
                      _["grid_failure"] = x.grid_failure, _["grid_unconverged"] = x.grid_unconverged, _["local_limit"] = x.local_limit);
}
inline SEXP nullable(bool has, const std::vector<double>& v) { return has ? (SEXP)NumericVector(v.begin(), v.end()) : R_NilValue; }

// event (v4) -> the v3 provenance list (core/cpp/v3_core.cpp:48-52)
inline List ev_list(const v4::EventCtx& e) {
  int island = e.key.unit == v4::UNIT_LOCAL ? 0 : (int)e.key.unit;
  return List::create(_["phase"] = v4::phase_name(e.phase), _["mechanism"] = v4::mech_name(e.mech), _["tier"] = (int)e.key.tier,
                      _["island"] = island, _["stage"] = (int)e.key.stage, _["round"] = (int)e.key.round,
                      _["particle"] = (int)e.key.particle, _["position"] = (int)e.key.position, _["phi"] = e.phi,
                      _["iter"] = (int)e.key.iter);
}
// v3 event -> v4 event with its serial key
inline v4::EventCtx ev_from_v3(const v3::EventCtx& e, int mech) {
  v4::EventCtx o; o.phase = e.phase; o.mech = mech; o.phi = e.phi;
  v4::EventKey& k = o.key;
  k.tier = (uint8_t)e.tier; k.iter = (int8_t)e.iter;
  switch (e.phase) {
    case PH_TABLE: k.seg = v4::SG_TABLE; break;
    case PH_INHERITED: k.seg = v4::SG_INHERITED; break;
    case PH_PILOT: case PH_DIAG: k.seg = v4::SG_CALIB; break;
    case PH_LOCAL: k.seg = (e.iter >= 0) ? v4::SG_CALIB : v4::SG_LOCAL; break;
    case PH_LS0: k.seg = v4::SG_LS0; break;
    default: k.seg = v4::SG_FINAL;
  }
  k.unit = (e.phase == PH_LOCAL || e.phase == PH_LS0) ? v4::UNIT_LOCAL : (uint32_t)e.island;
  k.xph = e.phase == PH_FINAL_BRIDGE ? v4::X_BRIDGE : e.phase == PH_BURN_IN ? v4::X_BURN : e.phase == PH_MEASURED ? v4::X_MEASURED : v4::X_INIT;
  k.stage = (uint32_t)e.stage; k.round = (uint32_t)e.round; k.particle = (uint32_t)e.particle; k.position = (uint32_t)e.position;
  return o;
}
inline void store_from_v3(v4::Store& dst, const v3::TopStore& s, const v4::Zobrist& z) {
  for (auto& e : s.s) dst.offer(e.v, e.S, z.hash(e.S));
  dst.compact();
}
inline v4::Ledger ledger_from_v3(const v3::Ledger& L, size_t p, int R, bool leaders, const v4::Zobrist& z) {
  v4::LedgerConfig cfg; cfg.p = (int32_t)p; cfg.islands = R; cfg.leaders = leaders; cfg.fresh_counters = false;
  v4::Ledger o(cfg);
  if (L.has_hpm) { o.has_hpm = true; o.hpmS = L.hpmS; o.hpmF = L.hpmF; o.hpm_logm = L.hpm_logm; o.hpm_ev = ev_from_v3(L.hpm_ev, L.hpm_mech); }
  store_from_v3(o.top, L.top, z);
  if (leaders) { store_from_v3(o.lead0, L.lead0, z); store_from_v3(o.lead1, L.lead1, z); }
  for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) o.logical[a][b] = L.logical[a][b];
  for (int r = 0; r <= R; ++r) o.island_best[r] = L.island_best[r];
  return o;
}
inline List store_list(const v4::Store& s, const v3::Data& D) {
  List M(s.size()); NumericVector v(s.size());
  for (size_t i = 0; i < s.size(); ++i) { v4::ModelView S = s.model(i); M[i] = to_orig(D, std::vector<int>(S.begin(), S.end())); v[i] = s.v[i]; }
  return List::create(_["models"] = M, _["value"] = v, _["capacity"] = (double)s.cap, _["full"] = s.size() >= s.cap);
}
inline NumericMatrix counters(const v4::Ledger& L, bool ls0) {
  int nph = ls0 ? N_PHASE : PH_LS0;
  NumericMatrix M(nph, N_MECH);
  CharacterVector rn(nph), cn(N_MECH);
  for (int a = 0; a < nph; ++a) { rn[a] = phase_name(a); for (int b = 0; b < N_MECH; ++b) M(a, b) = (double)L.logical[a][b]; }
  for (int b = 0; b < N_MECH; ++b) cn[b] = mech_name(b);
  M.attr("dimnames") = List::create(rn, cn);
  return M;
}
inline List local_list(const v4::LocalArchive& A, const v3::Data& D) {
  return List::create(_["centre"] = to_orig(D, A.centre), _["centre_F"] = A.centre_F, _["path"] = models_to_list(D, A.path),
                      _["path_F"] = A.path_F, _["scanned_centres"] = models_to_list(D, A.scanned), _["scanned_F"] = A.scanned_F,
                      _["scan_complete"] = IntegerVector(A.scan_complete.begin(), A.scan_complete.end()),
                      _["scan_size"] = IntegerVector(A.scan_size.begin(), A.scan_size.end()), _["termination"] = A.termination,
                      _["local_limit"] = A.local_limit, _["local_certified"] = A.local_certified,
                      _["returned"] = to_orig(D, A.returned), _["returned_F"] = A.returned_F, _["moves"] = A.moves,
                      _["n_evaluated"] = (double)A.n_eval);
}

}  // namespace wp4h

// [[Rcpp::export]]
List wp4_calibrate(SEXP setup, double seed, List settings) {
  HPtr h = get_holder(setup); const Data& D = *h->D;
  List ro = List::create(_["cache_capacity"] = 500.0 * D.p);
  SEXP state = cpp_cal_new(setup, seed, ro, R_NilValue);
  int threads = as<int>(settings["threads"]);
  wp4h::CoreBackend be(state, threads);
  v4::calib::Settings s;
  s.rule = as<std::string>(settings["rule"]) == "bounded" ? v4::calib::Rule::bounded : v4::calib::Rule::coded;
  s.tier0 = as<int>(settings["tier0"]); s.grid_fallback = as<bool>(settings["grid_fallback"]);
  s.I_max = as<int>(settings["I_max"]); s.refine_m = as<int>(settings["refine_m"]);
  s.sum_mode = as<std::string>(settings["sum_mode"]) == "blocked" ? v4::calib::SumMode::Blocked : v4::calib::SumMode::Serial;
  s.threads = threads;
  if (settings.containsElementNamed("force_build_failure")) s.test_force_build_failure = as<int>(settings["force_build_failure"]);
  if (settings.containsElementNamed("preflight")) be.preflight = as<bool>(settings["preflight"]);
  if (settings.containsElementNamed("force_ll_pilot")) be.force_ll_pilot = as<bool>(settings["force_ll_pilot"]);
  if (settings.containsElementNamed("fail_V_at")) be.fail_V_at = as<int>(settings["fail_V_at"]);
  if (settings.containsElementNamed("fail_diag_at")) be.fail_diag_at = as<int>(settings["fail_diag_at"]);
  if (settings.containsElementNamed("stop_grid_at")) be.stop_grid_at = as<int>(settings["stop_grid_at"]);
  List tl = settings["tiers"];
  for (int e = 0; e < 2; ++e) {
    List t = tl[e];
    s.tiers[e].tier = e; s.tiers[e].H = as<int>(t["H"]); s.tiers[e].Te = as<int>(t["T_e"]); s.tiers[e].L = as<int>(t["L"]);
    s.tiers[e].Hm = as<int>(t["Hm"]); s.tiers[e].ell = as<int>(t["ell"]);
  }
  v4::calib::CalibOut co;
  auto t0 = Clock::now();
  try { v4::calib::Driver drv(be, s); co = drv.run(); }
  catch (const v4::Error& e) { return List::create(_["status"] = "refused", _["task_status"] = v4::status_name(e.st), _["message"] = std::string(e.what())); }
  double secs = secs_since(t0);
  List tiers(co.tiers.size());
  for (size_t i = 0; i < co.tiers.size(); ++i) {
    const auto& t = co.tiers[i];
    List grids(t.grids.size()); for (size_t g = 0; g < t.grids.size(); ++g) grids[g] = wp4h::grid_rec(t.grids[g]);
    List its(t.iterations.size());
    for (size_t k = 0; k < t.iterations.size(); ++k) {
      const auto& it = t.iterations[k];
      // core/v3_calib.R:92-106: an iteration that stopped keeps only the island outputs it got (NULL if none); its
      // checks (overall_best, E1-E3) are never set
      auto nv = [](const std::vector<double>& v) { return v.empty() ? R_NilValue : (SEXP)NumericVector(v.begin(), v.end()); };
      its[k] = List::create(_["iteration"] = it.iter, _["grid"] = it.grid, _["rho_V"] = it.rho_V, _["grid_label"] = it.grid_label,
                            _["log_Z_r"] = nv(it.logZ_r), _["island_best"] = nv(it.island_best),
                            _["overall_best"] = it.complete ? wrap(it.overall_best) : R_NilValue,
                            _["E1"] = it.complete ? wrap(it.E1) : R_NilValue, _["E2"] = it.complete ? wrap(it.E2) : R_NilValue,
                            _["E3"] = it.complete ? wrap(it.E3) : R_NilValue, _["complete"] = it.complete);
    }
    tiers[i] = List::create(_["tier"] = t.tier, _["status"] = v4::calib::cal_status_name(t.status), _["triggers"] = wp4h::trig_list(t),
                            _["schedule"] = t.pilot.schedule.empty() ? R_NilValue : (SEXP)wrap(t.pilot.schedule), _["forced_pilot_steps"] = t.pilot.forced,
                            // core/v3_calib.R:33-43: a stopped tier (fail()) has no converged / rebuilds / grid_source
                            _["grids"] = grids, _["iterations"] = its,
                            _["converged"] = t.status == v4::calib::CalStatus::ok ? wrap(t.converged) : R_NilValue,
                            _["rebuilds"] = t.status == v4::calib::CalStatus::ok ? wrap(t.rebuilds) : R_NilValue,
                            _["grid"] = wp4h::nullable(t.has_grid, t.grid), _["rho_V"] = wp4h::nullable(t.has_rho, t.rho_V),
                            _["grid_label"] = t.has_grid ? (SEXP)wrap(t.grid_label) : R_NilValue,
                            _["grid_source"] = t.status == v4::calib::CalStatus::ok ? wrap(t.grid_source) : R_NilValue,
                            _["has_fallback"] = t.has_fallback);
  }
  const auto& f = co.flags;
  List flags = List::create(_["escalated"] = f.escalated,
                            _["escalation_blocked"] = f.escalation_blocked.empty() ? R_NilValue : (SEXP)wrap(f.escalation_blocked),
                            _["checks_passed_calibration"] = f.checks_passed_calibration < 0 ? LogicalVector::create(NA_LOGICAL) : LogicalVector::create(f.checks_passed_calibration == 1),
                            _["forced_pilot_steps"] = (double)f.forced_pilot_steps, _["grid_unconverged"] = f.grid_unconverged,
                            _["triggers_fired"] = co.tiers.back().has_triggers ? (SEXP)wrap(f.triggers_fired) : R_NilValue,   // core: names(NULL) after a stop before the triggers
                            _["grid_fallback"] = f.grid_fallback.empty() ? R_NilValue : (SEXP)wrap(f.grid_fallback));
  List frozen = co.has_frozen ? List::create(_["grid"] = co.frozen.grid, _["grid_unrefined"] = co.frozen.grid_unrefined,
                                             _["tier"] = co.frozen.tier, _["rho_V"] = wp4h::nullable(co.frozen.has_rho, co.frozen.rho_V),
                                             _["grid_label"] = co.frozen.grid_label, _["refine_m"] = co.frozen.refine_m)
                              : List();
  List ex = cpp_cal_export(state);
  return List::create(_["status"] = v4::calib::cal_status_name(co.status), _["tier_final"] = co.tier_final, _["escalated"] = co.escalated,
                      _["tiers"] = tiers, _["flags"] = flags, _["frozen"] = frozen, _["I_used"] = co.I_used,
                      _["hpm"] = List(ex["inherited"])["hpm"], _["inherited"] = ex["inherited"], _["ledger"] = ex["ledger"],
                      _["seconds"] = secs);
}

// The final run as R' process islands + v4 merge + v4 threaded tail (T9). Islands: core Engine, one ledger and one
// cache per island, streams 9 + r (compat). fault: "" | "island_numerical" | "tail_numerical" | "missing" | "corrupt" |
// "hash_mismatch" (T10).
// [[Rcpp::export]]
List wp4_final_merge(SEXP setup, NumericVector grid, List ro, double seed, SEXP inherited, int threads, int chunk,
                     std::string fault, int fault_island) {
  HPtr h = get_holder(setup); const Data& D = *h->D; const Start& st = *h->st;
  int N = as<int>(ro["N"]), L = as<int>(ro["L"]), Hm = as<int>(ro["measured_rounds"]), R = as<int>(ro["islands"]);
  int tier = as<int>(ro["tier"]), ell = as<int>(ro["ell"]);
  bool ls0 = ro.containsElementNamed("ls0") && as<bool>(ro["ls0"]);
  int ls0_ell = ro.containsElementNamed("ls0_ell") ? as<int>(ro["ls0_ell"]) : ell;
  bool tie_dp = !ro.containsElementNamed("ls0_tie_dp") || as<bool>(ro["ls0_tie_dp"]);
  bool plus = !ro.containsElementNamed("ls0_cap") || as<std::string>(ro["ls0_cap"]) != "ell_n";
  std::vector<double> g(grid.begin(), grid.end());
  wp4h::CoreFactory fac{&D, &st};
  v4::Zobrist zob; zob.init(D.p);
  // 1. pre-island ledger: tables (core/cpp/v3_core.cpp:372-387), inherited (419-441)
  v4::LedgerConfig lcfg; lcfg.p = D.p; lcfg.islands = R; lcfg.leaders = false; lcfg.fresh_counters = false;   // v0.1.7: no final-run leaders
  v4::Ledger pre(lcfg);
  {
    std::vector<int> U;
    for (int b = 0; b < st.J; ++b) {
      int m = (int)st.blocks[b].size();
      for (uint32_t c = 0; c < (1u << m); ++c) {
        if (std::isnan(st.logm_tab[b][c])) continue;
        U.clear();
        for (int i = 0; i < m; ++i) if (c & (1u << i)) U.push_back(st.blocks[b][i]);
        double lm = st.logm_tab[b][c], F = D.logprior[U.size()] + lm, lg0 = D.logprior[U.size()] + st.logr[b][c];
        pre.event(U, zob.hash(U), F, lg0, lm, v4::merge::table_event(b, c), true);
      }
    }
    if (!Rf_isNull(inherited)) {
      List inh(inherited);
      bool has_hpm = false; v4::Model chpm; v4::EventCtx ce;
      if (inh.containsElementNamed("hpm") && !Rf_isNull(inh["hpm"])) {
        List hp = inh["hpm"];
        if (hp.containsElementNamed("provenance") && hp.containsElementNamed("model")) {
          List pv = hp["provenance"];
          EventCtx e; e.phase = phase_index(as<std::string>(pv["phase"])); e.tier = as<int>(pv["tier"]); e.island = as<int>(pv["island"]);
          e.stage = as<int>(pv["stage"]); e.round = as<int>(pv["round"]); e.particle = as<int>(pv["particle"]);
          e.position = as<int>(pv["position"]); e.phi = as<double>(pv["phi"]); e.iter = pv.containsElementNamed("iter") ? as<int>(pv["iter"]) : -1;
          ce = wp4h::ev_from_v3(e, mech_index(as<std::string>(pv["mechanism"])));
          ce.key.seg = v4::SG_CALIB;   // a calibration event (INTERFACES v0.1.6)
          chpm = to_internal(D, hp["model"]); has_hpm = true;
        }
      }
      std::vector<v4::merge::InheritedModel> im;
      if (inh.containsElementNamed("models")) {
        auto Ms = models_from_R(D, inh["models"]);
        auto ev = fac.make();
        for (auto& S : Ms) { v4::merge::InheritedModel m; m.S = S; double dd; ev(S, m.logm, m.lg0, dd, m.F); im.push_back(m); }
      }
      v4::merge::offer_inherited(pre, im, has_hpm, chpm, ce, zob);
    }
  }
  pre.compact();
  // 2. islands as separate processes (own ledger, own cache, own stream)
  std::vector<v4::merge::IslandSlot> slots(R);
  NumericVector island_secs(R);
  for (int r = 1; r <= R; ++r) {
    auto t0 = Clock::now();
    v3::Ledger led(&D, R);
    ScoreCache cache; cache.init(D.W, (size_t)(500.0 * D.p));
    Engine E(D, st, h->Nb, h->B);
    E.cache = &cache; E.led = &led;
    RngSource rng; rng.g.seed_stream((uint64_t)seed, (uint64_t)(9 + r));
    E.vs = &rng;
    v4::merge::IslandSlot& s = slots[r - 1];
    s.load = v4::merge::Load::ok;
    try {
      IslandResult res = E.run_island(r, N, g, L, Hm, tier, nullptr);
      s.isl.status = res.partial ? v4::Status::resource_limit : v4::Status::completed;
      s.isl.logZ = res.logZ; s.isl.ess = res.ess; s.isl.rb_acc = res.rb_acc; s.isl.pip = res.pip; s.isl.rb_round = res.rb_round;
    } catch (v3::NumericalFailure& e) { s.isl.status = v4::Status::numerical_failure; s.isl.message = e.what(); s.isl.pip.assign(D.p, 0); }
    s.isl.r = r; s.isl.N = N; s.isl.L = L; s.isl.Hm = Hm;
    s.isl.led = wp4h::ledger_from_v3(led, D.p, R, false, zob);
    island_secs[r - 1] = secs_since(t0);
  }
  if (fault_island >= 1 && fault_island <= R) {
    auto& s = slots[fault_island - 1];
    if (fault == "island_numerical") s.isl.status = v4::Status::numerical_failure;
    if (fault == "missing") s.load = v4::merge::Load::missing;
    if (fault == "corrupt") s.load = v4::merge::Load::corrupt;
    if (fault == "hash_mismatch") s.load = v4::merge::Load::hash_mismatch;
  }
  ModeResult m = start_mode(st, 1000000, tie_dp);
  v4::merge::MergeSettings ms;
  ms.Rp = R; ms.N = N; ms.p = D.p; ms.K = D.K; ms.tier = tier; ms.ell = ell; ms.ls0 = ls0; ms.ls0_ell = ls0_ell;
  ms.ls0_cap_plus_mode = plus; ms.log_m0 = D.logm0; ms.threads = threads; ms.chunk = (size_t)chunk; ms.zob = &zob;
  auto t1 = Clock::now();
  v4::merge::FitOut fo;
  if (fault == "tail_numerical") {
    // fail on the first model the final local search's first scan visits after the centre (flip of column 0)
    v4::Model bad = pre.hpmS;   // placeholder; replaced below by a model of the first scan
    v4::Ledger tmp = pre; for (auto& s : slots) tmp.merge(s.isl.led);
    bad = tmp.hpmS;
    if (std::binary_search(bad.begin(), bad.end(), 0)) bad.erase(bad.begin()); else bad.insert(bad.begin(), 0);
    wp4h::FaultFactory ff{&D, &st, bad};
    fo = v4::merge::merge_and_tail(slots, std::move(pre), m.S, ff, ms);
  } else {
    fo = v4::merge::merge_and_tail(slots, std::move(pre), m.S, fac, ms);
  }
  double merge_secs = secs_since(t1);
  List out = List::create(_["status"] = v4::status_name(fo.status), _["fit_state"] = fo.fit_state, _["reason"] = fo.reason,
                          _["estimates_available"] = fo.estimates_available, _["hpm_incomplete"] = fo.hpm_incomplete,
                          _["seconds_islands"] = island_secs, _["seconds_merge_tail"] = merge_secs);
  if (fo.has_hpm) {
    out["hpm"] = to_orig(D, fo.hpm); out["hpm_F"] = fo.hpm_F; out["hpm_provenance"] = wp4h::ev_list(fo.hpm_ev);
  }
  if (!fo.estimates_available) return out;
  CharacterVector onames(D.p); for (int j = 0; j < D.p; ++j) onames[j] = std::to_string(D.orig[j]);
  NumericMatrix P(D.p, R); for (int r = 0; r < R; ++r) for (int j = 0; j < D.p; ++j) P(j, r) = fo.pip_r[r][j];
  NumericVector pe(fo.pip_eq.begin(), fo.pip_eq.end()); pe.names() = onames;
  List occ(fo.occ.size());
  out["log_Z_r"] = fo.logZ_r; out["log_Z"] = fo.log_Z; out["log_Z_lower95"] = fo.log_Z_lower95; out["log_Z_rel_m0"] = fo.log_Z_rel_m0;
  out["log_Z_r_rel_m0"] = fo.log_Z_r_rel_m0; out["pip_r"] = P; out["pip_primary"] = pe; out["mpm"] = to_orig(D, fo.mpm);
  out["pip_Z"] = fo.pip_Z; out["W_r"] = fo.W_r; out["R_eff"] = fo.R_eff; out["max_W"] = fo.max_W;
  out["log_Z_T"] = fo.log_Z_T; out["pip_T"] = fo.pip_T;
  if (fo.has_list_pip) {   // SPEC_LIST_PIP B12: the engine's list fields, compared by wp4_golden.R with core's
    NumericVector pl(fo.list_pip.pip_list.begin(), fo.list_pip.pip_list.end()); pl.names() = onames;
    out["pip_list"] = pl; out["mpm_list"] = to_orig(D, fo.list_pip.mpm_list); out["log_Z_list"] = fo.list_pip.log_Z_list;
    out["list_size"] = (double)fo.list_pip.list_size; out["list_full"] = fo.list_pip.list_full;
    out["pip_list_flag"] = fo.list_pip.flag.empty() ? R_NilValue : (SEXP)Rcpp::wrap(fo.list_pip.flag);
    {  // B10 permutation (per golden): the same store read in REVERSED entry order must give the same fields to 1e-12
      const v4::Store& T = fo.led.top; const size_t n = T.size();
      std::vector<double> v(n); std::vector<uint64_t> off(n), hs(n); std::vector<uint16_t> len(n);
      for (size_t i = 0; i < n; ++i) { const size_t k = n - 1 - i; v[i] = T.v[k]; off[i] = T.off[k]; hs[i] = T.hash[k]; len[i] = T.len[k]; }
      v4::ListPipSrc src; src.n = n; src.v = v.data(); src.off = off.data(); src.len = len.data(); src.hash = hs.data(); src.pool = T.pool.data();
      v4::ListPip lq = v4::compute_list_pip(src, D.p, T.cap);
      NumericVector pq(lq.pip_list.begin(), lq.pip_list.end()); pq.names() = onames;
      out["pip_list_permuted"] = pq; out["log_Z_list_permuted"] = lq.log_Z_list;
    }
  }
  out["near_ties"] = models_to_list(D, fo.near_ties); out["near_tie_F"] = fo.near_tie_F; out["near_tie_truncated"] = fo.near_tie_truncated;
  out["local_search"] = wp4h::local_list(fo.local, D);
  out["hpm_before_local"] = List::create(_["model"] = to_orig(D, fo.hpm_before_local), _["F"] = fo.hpm_before_local_F);
  if (ls0) {
    List l0 = wp4h::local_list(fo.ls0, D); l0["move_cap"] = fo.ls0_cap;
    out["ls0"] = l0; out["start_mode"] = to_orig(D, fo.mode_S);
    out["hpm_before_ls0"] = List::create(_["model"] = to_orig(D, fo.hpm_before_ls0), _["F"] = fo.hpm_before_ls0_F,
                                         _["provenance"] = wp4h::ev_list(fo.hpm_before_ls0_ev));
  }
  out["local_certified"] = fo.local_certified; out["local_certified_by"] = fo.local_certified_by;
  out["flags"] = List::create(_["E1"] = fo.E1, _["E2"] = fo.E2, _["E3"] = fo.E3, _["low_empirical_ESS"] = fo.low_ESS,
                              _["local_limit"] = fo.local_limit, _["near_tie_truncated"] = fo.near_tie_truncated,
                              _["checks_passed_final"] = fo.checks_passed_final, _["final_local_limit"] = fo.final_local_limit,
                              _["ls0_local_limit"] = fo.ls0_local_limit, _["ls0_improved"] = fo.ls0_improved,
                              _["ls0_hpm_changed"] = fo.ls0_hpm_changed);
  out["island_best"] = NumericVector(fo.led.island_best.begin() + 1, fo.led.island_best.end());
  out["top_store"] = wp4h::store_list(fo.led.top, D);
  out["leaders_gamma0"] = wp4h::store_list(fo.led.lead0, D); out["leaders_gamma1"] = wp4h::store_list(fo.led.lead1, D);
  out["logical"] = wp4h::counters(fo.led, ls0);
  return out;
}


// T9 THROUGH FILES: the same final run, but every input of the merge goes through the engine's files: data.bin
// (v4 Data over core's standardised X, y), setup.bin (core's blocks, tables, start mode, table top stores), calib.bin
// (frozen grid, N, L, tier, inherited models with their scores, the calibration HPM + provenance), island_r.bin x R'
// (core islands, one ledger each); then `smcbvs4 merge` (v4::merge::run, in process) and fit.bin read back.
// [[Rcpp::export]]
List wp4_files_merge(SEXP setup, NumericVector grid, List ro, double seed, SEXP inherited, std::string dir, int threads) {
  HPtr h = get_holder(setup); const Data& D3 = *h->D; const Start& st = *h->st;
  int N = as<int>(ro["N"]), L = as<int>(ro["L"]), Hm = as<int>(ro["measured_rounds"]), R = as<int>(ro["islands"]);
  int tier = as<int>(ro["tier"]), ell = as<int>(ro["ell"]);
  const int p = D3.p, n = D3.n;
  // data.bin
  auto own = std::make_shared<v4::DataOwned>();
  own->X = D3.X; own->y = D3.y; own->orig = D3.orig;
  own->col_max.assign(p, 1.0); own->col_mean.assign(p, 0.0); own->col_sd.assign(p, 1.0);
  v4::Data D = v4::make_data(own, n, p);
  v4::prep::Result pr; pr.n = n; pr.p_raw = p; pr.p = p; pr.kept = D3.orig; pr.own = own;
  std::string dpath = dir + "/data.bin", spath = dir + "/setup.bin", cpath = dir + "/calib.bin";
  std::string dh = v4::prep::write_data(dpath, D, pr, "B", v4::Json::object());
  // setup.bin (core/cpp/v3_start.h tables; table top stores over every scored code)
  v4::wp4io::SetupView S;
  S.blk = st.blk; S.pos = st.pos; S.blk_ptr.push_back(0);
  S.ttop.init(40ull * p + 1, v4::Order::HPM); S.tlead0.init(20ull * p, v4::Order::LEX); S.tlead1.init(20ull * p, v4::Order::LEX);
  for (int b = 0; b < st.J; ++b) {
    int m = (int)st.blocks[b].size();
    for (int j : st.blocks[b]) S.blk_members.push_back(j);
    S.blk_ptr.push_back((int64_t)S.blk_members.size());
    S.code_ptr.push_back((int64_t)S.logr.size());
    for (uint32_t c = 0; c < (1u << m); ++c) {
      S.logr.push_back(st.logr[b][c]);
      if (std::isnan(st.logm_tab[b][c])) continue;
      v4::Model U; for (int i = 0; i < m; ++i) if (c & (1u << i)) U.push_back(st.blocks[b][i]);
      double F = D3.logprior[U.size()] + st.logm_tab[b][c], lg0 = D3.logprior[U.size()] + st.logr[b][c];
      S.ttop.offer(F, U, D.zob.hash(U)); S.tlead0.offer(lg0, U, D.zob.hash(U)); S.tlead1.offer(F, U, D.zob.hash(U));
    }
  }
  S.code_ptr.push_back((int64_t)S.logr.size());   // J + 1 entries; code_ptr[J] = |logr| (INTERFACES v0.1.19 §2/§5)
  S.ttop.compact(); S.tlead0.compact(); S.tlead1.compact();
  bool tie_dp = !ro.containsElementNamed("ls0_tie_dp") || as<bool>(ro["ls0_tie_dp"]);
  S.mode_S = start_mode(st, 1000000, tie_dp).S;
  v4::Json sin = v4::Json::object(); sin["data.bin"] = dh;
  std::string sh = v4::wp4io::write_setup_min(spath, S, sin);
  // calib.bin
  wp4h::CoreFactory fac{&D3, &st};
  v4::LedgerConfig lc; lc.p = p; lc.islands = 4; lc.leaders = true; lc.fresh_counters = false;
  v4::Ledger cl(lc);
  std::vector<v4::merge::InheritedModel> im;
  if (!Rf_isNull(inherited)) {
    List inh(inherited);
    if (inh.containsElementNamed("models")) {
      auto Ms = models_from_R(D3, inh["models"]); auto ev = fac.make();
      for (auto& M : Ms) { v4::merge::InheritedModel x; x.S = M; double dd; ev(M, x.logm, x.lg0, dd, x.F); im.push_back(x); }
    }
    if (inh.containsElementNamed("hpm") && !Rf_isNull(inh["hpm"])) {
      List hp = inh["hpm"]; List pv = hp["provenance"];
      EventCtx e; e.phase = phase_index(as<std::string>(pv["phase"])); e.tier = as<int>(pv["tier"]); e.island = as<int>(pv["island"]);
      e.stage = as<int>(pv["stage"]); e.round = as<int>(pv["round"]); e.particle = as<int>(pv["particle"]);
      e.position = as<int>(pv["position"]); e.phi = as<double>(pv["phi"]); e.iter = pv.containsElementNamed("iter") ? as<int>(pv["iter"]) : -1;
      v4::EventCtx ce = wp4h::ev_from_v3(e, mech_index(as<std::string>(pv["mechanism"]))); ce.key.seg = v4::SG_CALIB;
      v4::Model M = to_internal(D3, hp["model"]); double lm, lg0, dd, F; auto ev = fac.make(); ev(M, lm, lg0, dd, F);
      cl.offer_hpm(M, F, lm, ce);
    }
  }
  cl.compact();
  v4::calib::CalibOut co; co.status = v4::calib::CalStatus::ok; co.tier_final = tier; co.has_frozen = true;
  co.frozen.grid.assign(grid.begin(), grid.end()); co.frozen.grid_unrefined = co.frozen.grid; co.frozen.tier = tier;
  v4::wp4io::CalibWrite cw; cw.mode = v4::fmt::M_COMPAT; cw.co = &co; cw.led = &cl; cw.inherited = im; cw.N = N; cw.L = L; cw.Hm = Hm;
  { double ks = 0; for (auto& m : im) ks += (double)m.S.size(); cw.k_store = im.empty() ? 1.0 : std::max(1.0, ks / (double)im.size()); }
  cw.inputs["data.bin"] = dh; cw.inputs["setup.bin"] = sh;
  std::string ch = v4::wp4io::write_calib(cpath, cw);
  // islands (core engine; one ledger, one cache, one stream each) -> island_r.bin
  v4::Json in = v4::Json::object(); in["data.bin"] = dh; in["setup.bin"] = sh; in["calib.bin"] = ch;
  v4::Json clean = v4::binary_block(); clean["git_commit"] = "0123456789abcdef0123456789abcdef01234567";   // test builds are dirty
  std::vector<double> g(grid.begin(), grid.end());
  v4::Json il = v4::Json::array();
  for (int r = 1; r <= R; ++r) {
    v3::Ledger led(&D3, R);
    ScoreCache cache; cache.init(D3.W, (size_t)(500.0 * p));
    Engine E(D3, st, h->Nb, h->B); E.cache = &cache; E.led = &led;
    RngSource rng; rng.g.seed_stream((uint64_t)seed, (uint64_t)(9 + r)); E.vs = &rng;
    IslandResult res = E.run_island(r, N, g, L, Hm, tier, nullptr);
    v4::merge::IslandIn I; I.status = res.partial ? v4::Status::resource_limit : v4::Status::completed;
    I.r = r; I.N = N; I.T = (int)res.phi.size(); I.L = L; I.Hm = Hm; I.logZ = res.logZ; I.ess = res.ess; I.rb_acc = res.rb_acc;
    I.pip = res.pip; I.rb_round = res.rb_round;
    I.led = wp4h::ledger_from_v3(led, p, R, false, D.zob);
    std::string ip = dir + "/island_" + std::to_string(r) + ".bin";
    v4::wp4io::write_island(ip, v4::fmt::M_COMPAT, I, in, &clean, &g);   // grid: phi of hpm_ev (v0.1.8 layout)
    il.push(ip);
  }
  // merge command
  v4::Json a = v4::Json::object();
  a["data"] = dpath; a["setup"] = spath; a["calib"] = cpath; a["out"] = dir + "/fit.bin"; a["mode"] = "compat";
  a["threads"] = threads; a["chunk"] = 256; a["ell"] = ell; a["islands"] = il; a["Rp"] = R;
  v4::Json rec = v4::merge::run(a);
  // read fit.bin back
  v4::fmt::Reader F(dir + "/fit.bin");
  v4::Json meta = F.json("meta");
  List out = List::create(_["status"] = meta.at("status").str(), _["record"] = rec.dump());
  if (!meta.at("estimates_available").boolean()) return out;
  auto models = [&](const std::string& pfx) { return models_to_list(D3, v4::wp4io::read_models(F, pfx, p, D3.K)); };
  auto vecd = [&](const std::string& nm) { std::vector<double> v = F.vec<double>(nm); return NumericVector(v.begin(), v.end()); };
  auto modl = [&](const std::string& nm) { std::vector<int32_t> v = F.vec<int32_t>(nm); return to_orig(D3, std::vector<int>(v.begin(), v.end())); };
  v4::Store top; v4::wp4io::read_store(F, meta, "top", top, p, D3.K);
  out["hpm"] = modl("hpm_S"); out["hpm_F"] = meta.at("hpm_F").num();
  out["hpm_provenance"] = wp4h::ev_list(v4::wp4io::event_from_json(meta.at("hpm_ev")));
  out["log_Z"] = meta.at("logZ").num(); out["log_Z_r"] = vecd("logZ_r");
  { NumericVector pe = vecd("pip_eq"); CharacterVector nm(p); for (int j = 0; j < p; ++j) nm[j] = std::to_string(D3.orig[j]); pe.names() = nm; out["pip_primary"] = pe; }
  { std::vector<double> pr2 = F.vec<double>("pip_r"); NumericMatrix P(p, R); for (int r = 0; r < R; ++r) for (int j = 0; j < p; ++j) P(j, r) = pr2[(size_t)r * p + j]; out["pip_r"] = P; }
  out["mpm"] = modl("mpm"); out["near_ties"] = models("near"); out["near_tie_F"] = vecd("near_F");
  if (F.has("pip_list")) {   // SPEC_LIST_PIP: the fit.bin sections and meta scalars
    NumericVector pl = vecd("pip_list"); CharacterVector nm(p); for (int j = 0; j < p; ++j) nm[j] = std::to_string(D3.orig[j]); pl.names() = nm;
    // fit.bin's mpm_list holds ORIGINAL column indices already (SPEC_LIST_PIP; the `orig` section is the kept -> original map): no to_orig here
    out["pip_list"] = pl;
    { std::vector<int32_t> mo = F.vec<int32_t>("mpm_list"); out["mpm_list"] = IntegerVector(mo.begin(), mo.end()); }
    { std::vector<int32_t> ob = F.vec<int32_t>("orig"); out["fit_orig"] = IntegerVector(ob.begin(), ob.end()); }
    out["log_Z_list"] = meta.at("log_Z_list").num();
    out["list_size"] = meta.at("list_size").num(); out["list_full"] = meta.at("list_full").boolean();
    out["pip_list_flag"] = meta.contains("pip_list_flag") ? (SEXP)Rcpp::wrap(meta.at("pip_list_flag").str()) : R_NilValue;
  }
  out["top_store"] = wp4h::store_list(top, D3); out["start_mode"] = modl("mode_S");
  out["hpm_before_local"] = List::create(_["model"] = modl("hpm_before_local_S"), _["F"] = meta.at("hpm_before_local_F").num());
  out["ls_scanned"] = models("ls_scanned"); out["ls_scanned_F"] = vecd("ls_scanned_F"); out["ls_path"] = models("ls_path");
  out["ls0_scanned"] = models("ls0_scanned"); out["ls0_scanned_F"] = vecd("ls0_scanned_F");
  out["local_certified"] = meta.at("local_certified").boolean(); out["local_certified_by"] = meta.at("local_certified_by").str();
  { std::vector<uint64_t> lg = F.vec<uint64_t>("logical"); NumericMatrix M(N_PHASE, N_MECH);
    for (int x = 0; x < N_PHASE; ++x) for (int y = 0; y < N_MECH; ++y) M(x, y) = (double)lg[(size_t)x * N_MECH + y]; out["logical"] = M; }
  const v4::Json& fl = meta.at("flags");
  out["flags"] = List::create(_["E1"] = fl.at("E1").boolean(), _["E2"] = fl.at("E2").boolean(), _["E3"] = fl.at("E3").boolean(),
                              _["low_empirical_ESS"] = fl.at("low_empirical_ESS").boolean(), _["local_limit"] = fl.at("local_limit").boolean(),
                              _["near_tie_truncated"] = fl.at("near_tie_truncated").boolean(), _["checks_passed_final"] = fl.at("checks_passed_final").boolean(),
                              _["ls0_improved"] = fl.at("ls0_improved").boolean(), _["ls0_hpm_changed"] = fl.at("ls0_hpm_changed").boolean());
  out["fit_bin"] = rec.at("fit_bin").str();
  return out;
}

// ---------------------------------------------------------------------------------------------------------------------
// The calibration over the v4 backend (calib_backend.h / calib_run.h): core's islands through an IslandRunner
// (`CoreRunner`: core Engine::run_island_s per calibration island, one fresh v3 ledger and cache per island, the v3
// streams 0-9 owned here and continued across rebuilds, core v3_core.cpp:593-596), the calibration ledger, the local
// searches, V and the inherited export in v4 code. Compared with v3_calibrate, it tests the v4 calibration ledger.
#include <v4/calib_run.h>
namespace wp4h {
v4::wp4io::SetupView setup_view_from_core(const v3::Start& st, const v3::Data& D3, const v4::Zobrist& zob) {
  const int p = D3.p;
  v4::wp4io::SetupView S;
  S.blk = st.blk; S.pos = st.pos; S.blk_ptr.push_back(0);
  S.ttop.init(40ull * p + 1, v4::Order::HPM); S.tlead0.init(20ull * p, v4::Order::LEX); S.tlead1.init(20ull * p, v4::Order::LEX);
  for (int b = 0; b < st.J; ++b) {
    int m = (int)st.blocks[b].size();
    for (int j : st.blocks[b]) S.blk_members.push_back(j);
    S.blk_ptr.push_back((int64_t)S.blk_members.size());
    S.code_ptr.push_back((int64_t)S.logr.size());
    for (uint32_t c = 0; c < (1u << m); ++c) {
      S.logr.push_back(st.logr[b][c]);
      if (std::isnan(st.logm_tab[b][c])) continue;
      v4::Model U; for (int i = 0; i < m; ++i) if (c & (1u << i)) U.push_back(st.blocks[b][i]);
      double F = D3.logprior[U.size()] + st.logm_tab[b][c], lg0 = D3.logprior[U.size()] + st.logr[b][c];
      S.ttop.offer(F, U, zob.hash(U)); S.tlead0.offer(lg0, U, zob.hash(U)); S.tlead1.offer(F, U, zob.hash(U));
    }
  }
  S.code_ptr.push_back((int64_t)S.logr.size());   // J + 1 entries; code_ptr[J] = |logr| (INTERFACES v0.1.19 §2/§5)
  S.ttop.compact(); S.tlead0.compact(); S.tlead1.compact();
  return S;
}
struct CoreRunner : v4::calib::IslandRunner {
  Holder* h; const v3::Data& D; const v3::Start& st; uint64_t seed; const v4::Zobrist& zob;
  std::map<int, RngSource> streams;
  RuntimeGuard* guard = nullptr;   // optional (golden stop path): core's runtime guard, shared by all islands as CalState's
  CoreRunner(Holder* hh, uint64_t s, const v4::Zobrist& z) : h(hh), D(*hh->D), st(*hh->st), seed(s), zob(z) {}
  RngSource& stream(int k) {
    auto it = streams.find(k);
    if (it == streams.end()) { RngSource g; g.g.seed_stream(seed, (uint64_t)k); it = streams.emplace(k, g).first; }
    return it->second;
  }
  v4::calib::IslandOut run(const v4::calib::IslandSpec& sp) override {
    const bool pilot = sp.role == v4::calib::IslandRole::Pilot;
    const int sid = (sp.tier == 0 ? 0 : 5) + (pilot ? 0 : sp.island);   // core v3_core.cpp:626, 667
    v3::Ledger led(&D, 4);
    ScoreCache cache; cache.init(D.W, (size_t)(500.0 * D.p));
    Engine E(D, st, h->Nb, h->B); E.cache = &cache; E.led = &led; E.guard = guard;
    RngSource& rs = stream(sid); E.vs = &rs;
    v4::calib::IslandOut o; o.position_start = rs.g.count;
    Engine::Schedule sch; std::vector<double> g = sp.grid;
    if (pilot) { sch.adaptive = true; sch.H = sp.H; sch.Te = sp.Te; } else sch.grid = &g;
    try {
      IslandResult res = E.run_island_s(pilot ? 0 : sp.island, sp.H, sch, sp.L, sp.Hm, sp.tier, nullptr, pilot ? PH_PILOT : PH_DIAG, sp.iter);
      o.partial = res.partial; o.status = res.partial ? v4::Status::resource_limit : v4::Status::completed;
      o.logZ = res.logZ; o.schedule = res.phi; o.forced = res.forced; o.pip = res.pip; o.init_hash = res.init_hash;
      for (size_t t = 0; t < res.phi.size(); ++t) {
        v4::StageRow row; row.phi = res.phi[t]; row.inc = res.inc[t]; row.ess = res.ess[t]; row.cum = res.cum[t];
        row.distinct_res = res.distinct_resampled[t]; row.distinct_moved = res.distinct_moved[t];
        const MoveStats& m = res.stage_moves[t];
        row.moves.gibbs = m.gibbs; row.moves.gibbs_change = m.gibbs_change; row.moves.us_exec = m.us_exec; row.moves.us_acc = m.us_acc;
        row.moves.us_self = m.us_self; row.moves.ns_exec = m.ns_exec; row.moves.ns_acc = m.ns_acc; row.moves.ns_noscore = m.ns_noscore;
        row.moves.ns_self = m.ns_self; row.moves.in_exec = m.in_exec; row.moves.in_acc = m.in_acc;
        o.stages.push_back(row);
      }
    } catch (v3::NumericalFailure& e) { o.status = v4::Status::numerical_failure; o.message = e.what(); }
    o.led = ledger_from_v3(led, D.p, 4, true, zob);   // the island's ledger (so far, on a stop)
    o.position_end = rs.g.count;
    return o;
  }
};
}  // namespace wp4h

// WP3's production island on a twin of core's data and start (WP3_DESIGN §1.11): the same standardised X and y, core's
// own block tables logr (the sampler tables rebuilt from them by the island's copy of core's arithmetic), the same
// neighbour lists and B. settings$runner == "wp3" swaps it in for CoreRunner (compat: v3 streams owned by the runner).
#include <v4/island/calib_runner.h>
namespace wp4h {
struct Wp3Twin {
  v4::Data D; v4::island::Start st; v4::island::Neighbours nb;
  Wp3Twin(const v3::Data& D3, const v3::Start& st3, const std::vector<std::vector<int>>& Nb3) {
    auto own = std::make_shared<v4::DataOwned>(); own->X = D3.X; own->y = D3.y;
    D = v4::make_data(own, D3.n, D3.p);
    st.D = &D; st.blocks = st3.blocks; st.J = (int)st3.blocks.size();
    st.blk.assign(D.p, -1); st.pos.assign(D.p, -1);
    for (int b = 0; b < st.J; ++b) for (size_t i = 0; i < st.blocks[b].size(); ++i) { st.blk[st.blocks[b][i]] = b; st.pos[st.blocks[b][i]] = (int)i; }
    st.logr = st3.logr;
    v4::island::build_sampler(st, D);
    nb.ptr.assign(1, 0); for (const auto& v : Nb3) { for (int l : v) nb.idx.push_back(l); nb.ptr.push_back((int64_t)nb.idx.size()); }
  }
};
}  // namespace wp4h

// [[Rcpp::export]]
List wp4_calibrate_ledger(SEXP setup, double seed, List settings, std::string calib_path, double guard_hours) {
  HPtr h = get_holder(setup); const Data& D = *h->D; const Start& st = *h->st;
  int threads = as<int>(settings["threads"]);
  v4::Zobrist zob; zob.init(D.p);
  v4::wp4io::SetupView S = wp4h::setup_view_from_core(st, D, zob);
  v4::LedgerConfig cfg; cfg.p = D.p; cfg.islands = 4; cfg.leaders = true; cfg.fresh_counters = false;
  v4::Ledger led(cfg);
  v4::wp4io::offer_tables(led, S, D.K, zob);   // the calibration ledger starts with the tables (core v3_core.cpp:613)
  v4::calib::Settings s;
  s.rule = as<std::string>(settings["rule"]) == "bounded" ? v4::calib::Rule::bounded : v4::calib::Rule::coded;
  s.tier0 = as<int>(settings["tier0"]); s.grid_fallback = as<bool>(settings["grid_fallback"]);
  s.I_max = as<int>(settings["I_max"]); s.refine_m = as<int>(settings["refine_m"]);
  s.sum_mode = as<std::string>(settings["sum_mode"]) == "blocked" ? v4::calib::SumMode::Blocked : v4::calib::SumMode::Serial;
  s.threads = threads;
  List tl = settings["tiers"];
  for (int e = 0; e < 2; ++e) {
    List t = tl[e];
    s.tiers[e].tier = e; s.tiers[e].H = as<int>(t["H"]); s.tiers[e].Te = as<int>(t["T_e"]); s.tiers[e].L = as<int>(t["L"]);
    s.tiers[e].Hm = as<int>(t["Hm"]); s.tiers[e].ell = as<int>(t["ell"]);
  }
  wp4h::CoreRunner core_runner(h.get(), (uint64_t)seed, zob);
  RuntimeGuard guard; if (guard_hours >= 0) { guard.allocation = guard_hours * 3600; core_runner.guard = &guard; }
  const bool force_ll = settings.containsElementNamed("force_ll_pilot") && as<bool>(settings["force_ll_pilot"]);
  // settings$runner == "wp3": WP3's production island (compat, calibration roles) in place of core's engine
  const bool wp3 = settings.containsElementNamed("runner") && as<std::string>(settings["runner"]) == "wp3";
  if (wp3 && guard_hours >= 0) Rcpp::stop("the runtime guard applies to core's runner only");
  std::unique_ptr<wp4h::Wp3Twin> tw; std::unique_ptr<v4::island::CalibIslandRunner<v4::island::Arith::Bit>> wp3_runner;
  if (wp3) {
    tw.reset(new wp4h::Wp3Twin(D, st, h->Nb));
    v4::island::CalibRunnerConfig rc; rc.seed = (uint32_t)seed; rc.compat = true; rc.kernel = v4::island::KernelKind::ParticleMajor; rc.threads = 1; rc.B = h->B;
    wp3_runner.reset(new v4::island::CalibIslandRunner<v4::island::Arith::Bit>(tw->D, tw->st, tw->nb, rc));
  }
  v4::calib::IslandRunner& runner = wp3 ? (v4::calib::IslandRunner&)*wp3_runner : (v4::calib::IslandRunner&)core_runner;
  wp4h::CoreFactory fac{&D, &st};
  v4::merge::TailSettings ts; ts.threads = threads; ts.chunk = 64; ts.K = D.K; ts.p = D.p; ts.zob = &zob;
  auto t0 = Clock::now();
  v4::calib::CalibOutcome oc;
  try { oc = v4::calib::calibrate_with(runner, std::move(led), fac, s, ts, 0, 0, force_ll); }
  catch (const v4::Error& e) { return List::create(_["status"] = "refused", _["task_status"] = v4::status_name(e.st), _["message"] = std::string(e.what())); }
  double secs = secs_since(t0);
  const v4::calib::CalibOut& co = oc.co;
  // the same export as wp4_calibrate (tiers, flags, frozen) ...
  List tiers(co.tiers.size());
  for (size_t i = 0; i < co.tiers.size(); ++i) {
    const auto& t = co.tiers[i];
    List grids(t.grids.size()); for (size_t g = 0; g < t.grids.size(); ++g) grids[g] = wp4h::grid_rec(t.grids[g]);
    List its(t.iterations.size());
    for (size_t k = 0; k < t.iterations.size(); ++k) {
      const auto& it = t.iterations[k];
      auto nv = [](const std::vector<double>& v) { return v.empty() ? R_NilValue : (SEXP)NumericVector(v.begin(), v.end()); };
      its[k] = List::create(_["iteration"] = it.iter, _["grid"] = it.grid, _["rho_V"] = it.rho_V, _["grid_label"] = it.grid_label,
                            _["log_Z_r"] = nv(it.logZ_r), _["island_best"] = nv(it.island_best),
                            _["overall_best"] = it.complete ? wrap(it.overall_best) : R_NilValue,
                            _["E1"] = it.complete ? wrap(it.E1) : R_NilValue, _["E2"] = it.complete ? wrap(it.E2) : R_NilValue,
                            _["E3"] = it.complete ? wrap(it.E3) : R_NilValue, _["complete"] = it.complete);
    }
    tiers[i] = List::create(_["tier"] = t.tier, _["status"] = v4::calib::cal_status_name(t.status), _["triggers"] = wp4h::trig_list(t),
                            _["schedule"] = t.pilot.schedule.empty() ? R_NilValue : (SEXP)wrap(t.pilot.schedule),   // core: no schedule after a pilot failure
                            _["forced_pilot_steps"] = t.pilot.forced, _["grids"] = grids, _["iterations"] = its,
                            _["converged"] = t.status == v4::calib::CalStatus::ok ? wrap(t.converged) : R_NilValue,
                            _["rebuilds"] = t.status == v4::calib::CalStatus::ok ? wrap(t.rebuilds) : R_NilValue,
                            _["grid"] = wp4h::nullable(t.has_grid, t.grid), _["rho_V"] = wp4h::nullable(t.has_rho, t.rho_V),
                            _["grid_label"] = t.has_grid ? (SEXP)wrap(t.grid_label) : R_NilValue,
                            _["grid_source"] = t.status == v4::calib::CalStatus::ok ? wrap(t.grid_source) : R_NilValue);
  }
  const auto& f = co.flags;
  List flags = List::create(_["escalated"] = f.escalated,
                            _["escalation_blocked"] = f.escalation_blocked.empty() ? R_NilValue : (SEXP)wrap(f.escalation_blocked),
                            _["checks_passed_calibration"] = f.checks_passed_calibration < 0 ? LogicalVector::create(NA_LOGICAL) : LogicalVector::create(f.checks_passed_calibration == 1),
                            _["forced_pilot_steps"] = (double)f.forced_pilot_steps, _["grid_unconverged"] = f.grid_unconverged,
                            _["triggers_fired"] = co.tiers.back().has_triggers ? (SEXP)wrap(f.triggers_fired) : R_NilValue,   // core: names(NULL) after a stop before the triggers
                            _["grid_fallback"] = f.grid_fallback.empty() ? R_NilValue : (SEXP)wrap(f.grid_fallback));
  List frozen = co.has_frozen ? List::create(_["grid"] = co.frozen.grid, _["grid_unrefined"] = co.frozen.grid_unrefined, _["tier"] = co.frozen.tier,
                                             _["rho_V"] = wp4h::nullable(co.frozen.has_rho, co.frozen.rho_V), _["grid_label"] = co.frozen.grid_label)
                              : List();
  // ... and the calibration ledger from v4 code (core's export names, v3_core.cpp:363-370, 616-618, 728-736)
  const v4::Ledger& L = oc.led;
  List hpm = L.has_hpm ? List::create(_["model"] = to_orig(D, std::vector<int>(L.hpmS.begin(), L.hpmS.end())), _["F"] = L.hpmF,
                                      _["provenance"] = wp4h::ev_list(L.hpm_ev)) : List();
  List ledger = List::create(_["top"] = wp4h::store_list(L.top, D), _["leaders_gamma0"] = wp4h::store_list(L.lead0, D),
                             _["leaders_gamma1"] = wp4h::store_list(L.lead1, D),
                             _["island_best"] = NumericVector(L.island_best.begin() + 1, L.island_best.end()),
                             _["logical"] = wp4h::counters(L, false));
  List inh(oc.inherited.size());
  for (size_t i = 0; i < oc.inherited.size(); ++i) { v4::ModelView v = oc.inherited.model(i); inh[i] = to_orig(D, std::vector<int>(v.begin(), v.end())); }
  List inh_vals = List::create(_["F"] = oc.inherited.F, _["lg0"] = oc.inherited.lg0, _["logm"] = oc.inherited.logm, _["d"] = oc.inherited.d);
  // stage records and stream positions per calibration island (review PR37 M-6)
  List stg(oc.stages.size());
  for (size_t i = 0; i < oc.stages.size(); ++i) {
    const auto& a = oc.stages[i];
    const size_t T = a.stages.size();
    NumericVector phi(T), inc(T), ess(T), cum(T), dr(T), dm(T);
    NumericMatrix mv(T, 11);
    for (size_t t = 0; t < T; ++t) {
      const auto& w = a.stages[t]; phi[t] = w.phi; inc[t] = w.inc; ess[t] = w.ess; cum[t] = w.cum; dr[t] = w.distinct_res; dm[t] = w.distinct_moved;
      const v4::MoveStats& m = w.moves; double q[11] = {(double)m.gibbs, (double)m.gibbs_change, (double)m.us_exec, (double)m.us_acc, (double)m.us_self,
        (double)m.ns_exec, (double)m.ns_acc, (double)m.ns_noscore, (double)m.ns_self, (double)m.in_exec, (double)m.in_acc};
      for (int c = 0; c < 11; ++c) mv(t, c) = q[c];
    }
    stg[i] = List::create(_["tier"] = a.tier, _["iter"] = a.iter, _["island"] = a.island, _["partial"] = a.partial, _["log_Z"] = a.logZ,
                          _["init_draws_hash"] = hex64(a.init_hash), _["position_start"] = (double)a.position_start, _["position_end"] = (double)a.position_end,
                          _["phi"] = phi, _["log_increment"] = inc, _["ess"] = ess, _["cum_log_Z"] = cum, _["distinct_resampled"] = dr,
                          _["distinct_moved"] = dm, _["moves"] = mv);
  }
  // calib.bin round trip (writer + reader)
  List cb;
  if (!calib_path.empty() && co.status == v4::calib::CalStatus::ok) {
    v4::wp4io::CalibWrite cw; cw.mode = v4::fmt::M_COMPAT; cw.co = &co; cw.led = &oc.led; cw.inherited_flat = &oc.inherited;
    cw.settings = &s; cw.k_store = oc.k_store;
    cw.N = co.tier_final == 0 ? as<int>(settings["N0"]) : as<int>(settings["N1"]); cw.L = s.tiers[co.tier_final].L; cw.Hm = 4; cw.stages = oc.stages;
    std::string hsh = v4::wp4io::write_calib(calib_path, cw);
    v4::wp4io::CalibIn ci = v4::wp4io::read_calib(calib_path, D.p, D.K);
    List inh2(ci.inherited.size());
    for (size_t i = 0; i < ci.inherited.size(); ++i) inh2[i] = to_orig(D, std::vector<int>(ci.inherited[i].S.begin(), ci.inherited[i].S.end()));
    v4::fmt::Reader R(calib_path);
    cb = List::create(_["content_hash"] = hsh, _["grid"] = ci.grid, _["tier"] = ci.tier, _["N"] = ci.N, _["inherited"] = inh2,
                      _["hpm"] = to_orig(D, std::vector<int>(ci.hpm.begin(), ci.hpm.end())), _["hpm_provenance"] = wp4h::ev_list(ci.hpm_ev),
                      _["n_stage_islands"] = (int)R.entry("stage_meta").dims[0], _["n_stage_rows"] = (double)R.entry("stage_phi").dims[0]);
  }
  return List::create(_["status"] = v4::calib::cal_status_name(co.status), _["tier_final"] = co.tier_final, _["escalated"] = co.escalated,
                      _["tiers"] = tiers, _["flags"] = flags, _["frozen"] = frozen, _["I_used"] = co.I_used, _["hpm"] = hpm, _["ledger"] = ledger,
                      _["inherited"] = List::create(_["models"] = inh, _["hpm"] = hpm), _["inherited_values"] = inh_vals, _["stages"] = stg,
                      _["k_store"] = oc.k_store, _["calib_bin"] = cb, _["seconds"] = secs);
}

// review PR37 N-3 (a): a data-level numerical failure through UNMODIFIED core (the way WP3's test_island
// numerical_failure_in_flip_deterministic forces it). A copy of the setup in which the columns `cols` (1-based original
// indices) are scaled by `scale` (X; G and z recomputed for them) and pi_0 (practically) never draws them: every table
// entry that contains one gets log r - 1000 (finite, as setup.bin requires for |U| <= K; its log m and route stay the
// table's, so both sides ingest the same table events), then core's build_start re-runs on the edited tables. Core's scorer
// throws NumericalFailure for every model containing a scaled column (Cholesky, refactor and QR all fail), so the first
// Gibbs flip onto one stops the island -- in core's calibration (cpp_cal_pilot / cpp_cal_diag catch it) and in
// CoreRunner alike. Used on both sides, so both see the same data.
// [[Rcpp::export]]
SEXP wp4_fault_setup(SEXP setup, IntegerVector cols, double scale) {
  HPtr h = get_holder(setup);
  const Data& D = *h->D;
  std::vector<int> bad;
  for (int c : cols) {
    int j = -1; for (int a = 0; a < D.p; ++a) if (D.orig[a] == c) j = a;
    if (j < 0) stop("wp4_fault_setup: column %d not kept by preprocessing", c);
    bad.push_back(j);
  }
  auto D2 = std::make_shared<Data>(D);
  const int n = D.n, p = D.p;
  for (int j : bad) for (int i = 0; i < n; ++i) D2->X[(size_t)j * n + i] *= scale;
  for (int j : bad) {
    const double* xj = D2->col(j);
    for (int a = 0; a < p; ++a) { const double* xa = D2->col(a); double s = 0; for (int i = 0; i < n; ++i) s += xa[i] * xj[i]; D2->G[(size_t)j * p + a] = s; D2->G[(size_t)a * p + j] = s; }
    double s = 0; for (int i = 0; i < n; ++i) s += xj[i] * D2->y[i]; D2->z[j] = s;
  }
  auto st2 = std::make_shared<Start>(*h->st); st2->D = D2.get();
  for (int j : bad) {
    const int b = st2->blk[j];
    for (size_t code = 0; code < st2->logr[b].size(); ++code)
      if ((code & (1u << st2->pos[j])) && !std::isnan(st2->logr[b][code])) {
        st2->logr[b][code] -= 1000.0;
      }
  }
  build_start(*st2);
  Holder* g = new Holder(*h); g->D = D2; g->st = st2;
  return HPtr(g, true);
}
