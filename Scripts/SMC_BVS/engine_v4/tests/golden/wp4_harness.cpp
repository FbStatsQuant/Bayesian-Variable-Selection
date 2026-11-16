// wp4_harness.cpp -- TEST CODE ONLY. Appended to an unmodified COPY of core/cpp/v3_core.cpp (one translation unit,
// core headers unchanged, v3 flags from core/cpp/Makevars.v3) by tests/golden/wp4_golden.R. It drives the WP4 code
// (v4::calib::Driver, v4::merge::merge_and_tail) with the core/ engine as the island backend, so that WP4's control
// flow, grid rules, V re-scoring, ledger merge, threaded tail and assembly can be compared bit for bit with
// core/v3_calib.R::v3_calibrate and core/v3_run.R::v3_final_run (compat mode, until WP1/WP3's compat islands land).
// [[Rcpp::plugins(openmp)]]
#include <v4/calib.h>
#include <v4/merge.h>
// WP1 library sources used by the WP4 headers (compiled into this test TU; no R dependency)
#include "v4/../../src/common/status.cpp"
#include "v4/../../src/common/store.cpp"
#include "v4/../../src/common/ledger.cpp"

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
  CoreBackend(SEXP s, int th) : state(s), c(s), threads(th) {}
  v4::calib::PilotOut pilot(const v4::calib::TierSettings& ts) override {
    List r = cpp_cal_pilot(state, ts.tier, ts.H, ts.Te, ts.L, ts.Hm, ts.ell);
    v4::calib::PilotOut o; o.status = cal_status(as<std::string>(r["status"]));
    if (r.containsElementNamed("message")) o.message = as<std::string>(r["message"]);
    if (r.containsElementNamed("schedule")) { NumericVector s = r["schedule"]; o.schedule.assign(s.begin(), s.end()); }
    if (r.containsElementNamed("forced_pilot_steps")) { o.forced = as<int>(r["forced_pilot_steps"]); o.has_forced = true; }
    if (r.containsElementNamed("best_before_local")) {
      o.best_before_F = as<double>(List(r["best_before_local"])["F"]); o.best_after_F = as<double>(List(r["best_after_local"])["F"]);
      o.local_limit = as<bool>(List(r["local_search"])["local_limit"]);
    }
    return o;
  }
  v4::calib::DiagOut diag(const v4::calib::TierSettings& ts, const std::vector<double>& grid, int iter) override {
    List r = cpp_cal_diag(state, ts.tier, NumericVector(grid.begin(), grid.end()), ts.H, ts.L, ts.Hm, ts.ell, iter);
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
  List tl = settings["tiers"];
  for (int e = 0; e < 2; ++e) {
    List t = tl[e];
    s.tiers[e].tier = e; s.tiers[e].H = as<int>(t["H"]); s.tiers[e].Te = as<int>(t["T_e"]); s.tiers[e].L = as<int>(t["L"]);
    s.tiers[e].Hm = as<int>(t["Hm"]); s.tiers[e].ell = as<int>(t["ell"]);
  }
  v4::calib::Driver drv(be, s);
  auto t0 = Clock::now();
  v4::calib::CalibOut co = drv.run();
  double secs = secs_since(t0);
  List tiers(co.tiers.size());
  for (size_t i = 0; i < co.tiers.size(); ++i) {
    const auto& t = co.tiers[i];
    List grids(t.grids.size()); for (size_t g = 0; g < t.grids.size(); ++g) grids[g] = wp4h::grid_rec(t.grids[g]);
    List its(t.iterations.size());
    for (size_t k = 0; k < t.iterations.size(); ++k) {
      const auto& it = t.iterations[k];
      its[k] = List::create(_["iteration"] = it.iter, _["grid"] = it.grid, _["rho_V"] = it.rho_V, _["grid_label"] = it.grid_label,
                            _["log_Z_r"] = it.logZ_r, _["island_best"] = it.island_best, _["overall_best"] = it.overall_best,
                            _["E1"] = it.E1, _["E2"] = it.E2, _["E3"] = it.E3, _["complete"] = it.complete);
    }
    tiers[i] = List::create(_["tier"] = t.tier, _["status"] = v4::calib::cal_status_name(t.status), _["triggers"] = wp4h::trig_list(t),
                            _["schedule"] = t.pilot.schedule, _["forced_pilot_steps"] = t.pilot.forced,
                            _["grids"] = grids, _["iterations"] = its, _["converged"] = t.converged, _["rebuilds"] = t.rebuilds,
                            _["grid"] = wp4h::nullable(t.has_grid, t.grid), _["rho_V"] = wp4h::nullable(t.has_rho, t.rho_V),
                            _["grid_label"] = t.has_grid ? (SEXP)wrap(t.grid_label) : R_NilValue, _["grid_source"] = t.grid_source,
                            _["has_fallback"] = t.has_fallback);
  }
  const auto& f = co.flags;
  List flags = List::create(_["escalated"] = f.escalated,
                            _["escalation_blocked"] = f.escalation_blocked.empty() ? R_NilValue : (SEXP)wrap(f.escalation_blocked),
                            _["checks_passed_calibration"] = f.checks_passed_calibration < 0 ? LogicalVector::create(NA_LOGICAL) : LogicalVector::create(f.checks_passed_calibration == 1),
                            _["forced_pilot_steps"] = (double)f.forced_pilot_steps, _["grid_unconverged"] = f.grid_unconverged,
                            _["triggers_fired"] = f.triggers_fired,
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
  v4::LedgerConfig lcfg; lcfg.p = D.p; lcfg.islands = R; lcfg.leaders = true; lcfg.fresh_counters = false;
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
    s.isl.led = wp4h::ledger_from_v3(led, D.p, R, true, zob);
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
    fo = v4::merge::merge_and_tail(slots, pre, m.S, ff, ms);
  } else {
    fo = v4::merge::merge_and_tail(slots, pre, m.S, fac, ms);
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
