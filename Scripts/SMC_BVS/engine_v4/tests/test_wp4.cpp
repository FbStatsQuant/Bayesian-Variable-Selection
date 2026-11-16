// test_wp4.cpp -- WP4 unit tests (no R): calibration rules and driver paths (mock backend), store/ledger order-freeness,
// threaded tail against a serial reference (thread and chunk invariance, tie rules), merge assembly, GUARD-W / T10.
// Part of v4_tests (tk harness).
#include <cstdio>
#include <limits>
#include <random>
#include "tk.h"
#include "v4/calib.h"
#include "v4/merge.h"

namespace {
bool same_bits_v(const std::vector<double>& a, const std::vector<double>& b) {
  if (a.size() != b.size()) return false;
  for (size_t i = 0; i < a.size(); ++i) if (!::same_bits(a[i], b[i])) return false;
  return true;
}

}  // namespace
using namespace v4;
namespace {
const Zobrist& zob() { static Zobrist z; static bool init = false; if (!init) { z.init(4000); init = true; } return z; }
Ledger mkled(int p, int R, bool leaders) { LedgerConfig c; c.p = p; c.islands = R; c.leaders = leaders; c.fresh_counters = false; return Ledger(c); }
}  // namespace

// ---------------------------------------------------------------------------------------------------------------------
// calibration rules
TEST(wp4_calib_rules) {
  std::mt19937_64 g(7); std::normal_distribution<double> nd;
  std::vector<double> a(200000), b(200000);
  for (size_t i = 0; i < a.size(); ++i) { a[i] = 3 * nd(g); b[i] = 20 * nd(g); }
  for (double t : {0.0, 0.013, 0.37, 1.0, 1.9}) {
    std::vector<double> x(a.size()); for (size_t i = 0; i < a.size(); ++i) x[i] = a[i] + t * b[i];
    double ref = calib::lse_cal(x);
    calib::FV s1(a, b, calib::SumMode::Serial, 1), s3(a, b, calib::SumMode::Serial, 3);
    calib::FV b1(a, b, calib::SumMode::Blocked, 1), b3(a, b, calib::SumMode::Blocked, 3);
    CHECK(same_bits(s1(t), ref));            // serial = core lse_cal bits
    CHECK(same_bits(s3(t), ref));            // threaded terms, serial sum: still class B
    double bb1 = b1(t), bb3 = b3(t);
    CHECK(same_bits(bb1, bb3));              // blocked: thread invariant
    CHECK(std::fabs(bb1 - ref) <= 1e-12 * std::max(1.0, std::fabs(ref)));   // class C: tiny summation difference
  }
  // grid construction: serial threads 1 == 3 == reference rule on the full arrays
  std::vector<double> tg{0, 0.001, 0.01, 0.05, 0.1, 0.2, 0.35, 0.5, 0.7, 0.85, 1.0};
  auto g1 = calib::build_grid(a, b, tg, 1000, calib::SumMode::Serial, 1);
  auto g3 = calib::build_grid(a, b, tg, 1000, calib::SumMode::Serial, 3);
  CHECK(g1.ok && same_bits_v(g1.grid, g3.grid) && same_bits_v(g1.rho, g3.rho) && g1.evals == g3.evals);
  auto h1 = calib::build_grid(a, b, tg, 1000, calib::SumMode::Blocked, 1);
  auto h3 = calib::build_grid(a, b, tg, 1000, calib::SumMode::Blocked, 3);
  CHECK(h1.ok && same_bits_v(h1.grid, h3.grid) && same_bits_v(h1.rho, h3.rho));
  auto tf = calib::build_grid(a, b, tg, 2, calib::SumMode::Serial, 1);
  CHECK(!tf.ok && tf.reason == "too_many_intervals");
  // refinement and grid check
  std::vector<double> gr{0, 0.25, 1};
  auto r4 = calib::refine_grid(gr, 4);
  CHECK(r4.size() == 9 && r4[1] == 0.0625 && r4[4] == 0.25 && r4.back() == 1.0 && calib::check_grid(r4));
  CHECK(calib::refine_grid(gr, 1) == gr);
  CHECK(!calib::check_grid({0, 0.5, 0.5, 1}) && !calib::check_grid({0.1, 1}) && calib::check_grid({0, 1}));
  // R's sd (values from R 4.6.0: sprintf("%.17g", sd(...)))
  CHECK(same_bits(calib::r_sd({1, 2, 4}), 1.5275252316519468));
  CHECK(same_bits(calib::r_sd({-3.5, 10.25, 7.125, 0.1}), 6.3051029267305916));
}

// ---------------------------------------------------------------------------------------------------------------------
// calibration driver with a scripted backend
struct Mock : calib::Backend {
  std::vector<double> lg0, d; double drift = 0;   // drift != 0: V changes at every call (grids never converge)
  int v_calls = 0, pilot_calls = 0, diag_calls = 0; bool v_fail = false, preflight = false;
  std::vector<double> logZ_r{-10, -10.2, -9.9, -10.1};
  calib::PilotOut pilot(const calib::TierSettings& ts) override {
    ++pilot_calls; calib::PilotOut o; o.schedule = {0, 0.02, 0.1, 0.3, 0.6, 1.0}; o.has_forced = true; o.forced = 0;
    o.best_before_F = 5; o.best_after_F = 5; (void)ts; return o;
  }
  calib::DiagOut diag(const calib::TierSettings&, const std::vector<double>&, int) override {
    ++diag_calls; calib::DiagOut o; o.logZ_r = logZ_r; o.island_best = {5, 5, 5, 5}; o.best_before_F = 5; o.best_after_F = 5; return o;
  }
  calib::VOut candidate_set() override {
    ++v_calls; calib::VOut v;
    if (v_fail) { v.status = calib::CalStatus::numerical_failure; v.message = "boom"; return v; }
    v.lg0 = lg0; v.d = d; for (auto& x : v.d) x *= (1 + drift * v_calls); return v;
  }
  bool preflight_exceeds(int) override { return preflight; }
};
static calib::Settings mk(calib::Rule r, int Te, int ell, int I_max = 3) {
  calib::Settings s; s.rule = r; s.I_max = I_max;
  for (int e = 0; e < 2; ++e) { s.tiers[e].tier = e; s.tiers[e].H = 64; s.tiers[e].Te = Te * (e + 1); s.tiers[e].L = 4; s.tiers[e].ell = ell; }
  return s;
}
TEST(wp4_calib_driver) {
  std::mt19937_64 g(3); std::normal_distribution<double> nd;
  Mock base; for (int i = 0; i < 500; ++i) { base.lg0.push_back(nd(g)); base.d.push_back(8 * nd(g)); }
  {  // coded, converging: one rebuild, no trigger, no escalation
    Mock m = base; calib::Driver drv(m, mk(calib::Rule::coded, 200, 5)); auto o = drv.run();
    CHECK(o.status == calib::CalStatus::ok && o.tiers.size() == 1 && o.tiers[0].converged && o.tiers[0].rebuilds == 1);
    CHECK(o.flags.checks_passed_calibration == 1 && o.has_frozen && o.frozen.grid == o.tiers[0].grid && o.frozen.grid_label == "rebuild_1");
  }
  {  // coded, never converging: grid_unconverged -> escalation; tier 1 also unconverged
    Mock m = base; m.drift = 0.01; calib::Driver drv(m, mk(calib::Rule::coded, 200, 2)); auto o = drv.run();
    CHECK(o.status == calib::CalStatus::ok && o.tiers.size() == 2 && o.escalated && o.tier_final == 1);
    CHECK(o.tiers[0].triggers.grid_unconverged && o.tiers[1].rebuilds == 2 && o.flags.grid_unconverged);
  }
  {  // bounded, never converging: I_max rebuilds, frozen with grid_unconverged, no escalation
    Mock m = base; m.drift = 0.01; calib::Driver drv(m, mk(calib::Rule::bounded, 200, 9, 2)); auto o = drv.run();
    CHECK(o.status == calib::CalStatus::ok && o.tiers.size() == 1 && !o.escalated && o.I_used == 2);
    CHECK(o.flags.grid_unconverged && o.has_frozen && o.frozen.grid_label == "rebuild_2" && m.diag_calls == 2);
  }
  {  // bounded, I_max = 0: pilot + preliminary grid only
    Mock m = base; calib::Driver drv(m, mk(calib::Rule::bounded, 200, 9, 0)); auto o = drv.run();
    CHECK(o.status == calib::CalStatus::ok && m.diag_calls == 0 && o.frozen.grid_label == "preliminary" && o.flags.grid_unconverged);
  }
  {  // bounded: E2 fires (island spread), no escalation; coded: same backend escalates
    Mock m = base; m.logZ_r = {-10, -14, -9, -10};
    calib::Driver drv(m, mk(calib::Rule::bounded, 200, 9)); auto o = drv.run();
    CHECK(o.tiers.size() == 1 && o.tiers[0].triggers.E2 && o.flags.checks_passed_calibration == 0);
    Mock m2 = m; calib::Driver drv2(m2, mk(calib::Rule::coded, 200, 9)); auto o2 = drv2.run();
    CHECK(o2.tiers.size() == 2 && o2.escalated);
  }
  {  // construction failure: coded escalates then takes the C-DLV fallback; bounded (D-26) never escalates and installs
     // the pilot schedule at tier 0; both flag grid_fallback and give output
    for (auto rule : {calib::Rule::coded, calib::Rule::bounded}) {
      Mock m = base; calib::Driver drv(m, mk(rule, 1, 3)); auto o = drv.run();
      CHECK(o.status == calib::CalStatus::ok && o.tiers.size() == (rule == calib::Rule::coded ? 2u : 1u) && o.flags.grid_fallback == "pilot_schedule");
      CHECK(o.frozen.grid == std::vector<double>({0, 0.02, 0.1, 0.3, 0.6, 1.0}) && !o.frozen.has_rho && o.frozen.tier == 0 + (rule == calib::Rule::coded));
    }
    {  // D-26: a rebuild fails after a successful construction -> the last good grid; grid_fallback forced on
      calib::Settings s = mk(calib::Rule::bounded, 200, 9, 3); s.test_force_build_failure = 2; s.grid_fallback = false;
      Mock m = base; m.drift = 0.01; calib::Driver drv(m, s); auto o = drv.run();
      CHECK(o.status == calib::CalStatus::ok && o.tiers.size() == 1 && o.flags.grid_fallback == "last_successful_construction");
      CHECK(o.frozen.grid == o.tiers[0].grids[0].grid && o.frozen.grid_label == "preliminary" && o.frozen.has_rho);
    }
    {  // D-26 / F7 refusals: I_max > ell, bounded tier0 = 1, coded with blocked sums or refinement
      calib::Settings s = mk(calib::Rule::bounded, 200, 2, 3); Mock m = base;
      CHECK_THROWS(calib::Driver(m, s));
      s = mk(calib::Rule::bounded, 200, 9, 3); s.tier0 = 1; CHECK_THROWS(calib::Driver(m, s));
      s = mk(calib::Rule::coded, 200, 9); s.sum_mode = calib::SumMode::Blocked; CHECK_THROWS(calib::Driver(m, s));
      s = mk(calib::Rule::coded, 200, 9); s.refine_m = 4; CHECK_THROWS(calib::Driver(m, s));
    }
    {  // F8: a non-finite log Z_r in a diagnostic island is a numerical failure (R's sd would be NA)
      Mock m = base; m.logZ_r = {-10, std::numeric_limits<double>::quiet_NaN(), -9, -10}; calib::Driver drv(m, mk(calib::Rule::coded, 200, 3)); auto o = drv.run();
      CHECK(o.status == calib::CalStatus::numerical_failure && !o.has_frozen);
    }
    calib::Settings s = mk(calib::Rule::coded, 1, 3); s.grid_fallback = false;
    Mock m = base; calib::Driver drv(m, s); auto o = drv.run();
    CHECK(o.status == calib::CalStatus::schedule_limit && !o.has_frozen && calib::task_status(o.status) == Status::resource_limit);
  }
  {  // numerical failure in V; preflight blocks the escalation
    Mock m = base; m.v_fail = true; calib::Driver drv(m, mk(calib::Rule::coded, 200, 3)); auto o = drv.run();
    CHECK(o.status == calib::CalStatus::numerical_failure && !o.has_frozen && calib::task_status(o.status) == Status::numerical_failure);
    Mock m2 = base; m2.drift = 0.01; m2.preflight = true; calib::Driver drv2(m2, mk(calib::Rule::coded, 200, 1)); auto o2 = drv2.run();
    CHECK(o2.status == calib::CalStatus::resource_limit && o2.escalation_blocked == "resource_limit" && o2.tiers.size() == 1);
  }
  {  // refinement applied to the frozen grid
    Mock m = base; calib::Settings s = mk(calib::Rule::bounded, 200, 9, 1); s.refine_m = 4; calib::Driver drv(m, s); auto o = drv.run();
    CHECK(o.frozen.grid.size() == 4 * (o.frozen.grid_unrefined.size() - 1) + 1 && calib::check_grid(o.frozen.grid));
    CHECK(o.frozen.intervals_refined == (int)o.frozen.grid.size() - 1 && o.frozen.rho_V.size() == o.frozen.grid_unrefined.size() - 1);
  }
}

// ---------------------------------------------------------------------------------------------------------------------
// toy evaluator: F(S) = sum_j w_j - 0.5 |S|^2 on a coarse grid (exact ties), lg0 = F - 0.25 |S|, logm = F + |S|
struct ToyEval {
  const std::vector<double>* w; Model bad; bool use_bad = false;
  void operator()(const Model& S, double& lm, double& lg0, double& d, double& F) {
    if (use_bad && S == bad) throw NumericalFailure("toy failure");
    double s = 0; for (int32_t j : S) s += (*w)[j];
    double k = (double)S.size();
    F = s - 0.5 * k * k; lg0 = F - 0.25 * k; lm = F + k; d = lm - lg0;
  }
};
struct ToyFactory { const std::vector<double>* w; Model bad; bool use_bad = false; ToyEval make() const { return ToyEval{w, bad, use_bad}; } };

// serial reference: core/cpp/v3_engine.h:379-419 over the toy evaluator, offering in serial order
static LocalArchive serial_local(const Model& centre, int ell, bool emit, int phase, Ledger& led, ToyFactory& fac, int p, int K, int tier) {
  LocalArchive A; ToyEval ev = fac.make();
  auto mkev = [&](uint32_t st, uint32_t rd, uint32_t pos) {
    EventCtx e; e.phase = phase; e.mech = ME_LOCAL; e.phi = 1; e.key.seg = phase == PH_LS0 ? SG_LS0 : SG_LOCAL; e.key.tier = (uint8_t)tier;
    e.key.iter = -1; e.key.unit = UNIT_LOCAL; e.key.xph = X_INIT; e.key.stage = st; e.key.round = rd; e.key.position = pos; return e;
  };
  Model C = centre; double CF, lm, lg0, d;
  ev(C, lm, lg0, d, CF); if (emit) led.event(C, zob().hash(C), CF, lg0, lm, mkev(0, 0, 0), true);
  A.centre = C; A.centre_F = CF;
  while (true) {
    uint32_t st = (uint32_t)A.scanned.size() + 1, rd = (uint32_t)A.moves; uint32_t pos = 0;
    bool have = false; Model best; double bestF = 0;
    auto consider = [&](const Model& Q) {
      double F; ev(Q, lm, lg0, d, F); ++pos; A.n_eval++;
      led.event(Q, zob().hash(Q), F, lg0, lm, mkev(st, rd, pos), true);
      if (!have || F > bestF || (F == bestF && lex_less(Q, best))) { best = Q; bestF = F; have = true; }
    };
    for (int j = 0; j < p; ++j) {
      Model Q = C; auto it = std::lower_bound(Q.begin(), Q.end(), j);
      if (it != Q.end() && *it == j) Q.erase(it); else { if ((int)C.size() >= K) continue; Q.insert(it, j); }
      consider(Q);
    }
    Model CS = C;
    for (int j : CS) for (int l = 0; l < p; ++l) {
      if (std::binary_search(C.begin(), C.end(), l)) continue;
      Model Q = C; Q.erase(std::lower_bound(Q.begin(), Q.end(), j)); Q.insert(std::lower_bound(Q.begin(), Q.end(), l), l);
      consider(Q);
    }
    A.scanned.push_back(C); A.scanned_F.push_back(CF); A.scan_complete.push_back(1); A.scan_size.push_back((int)pos);
    if (have && bestF > CF) {
      if (A.moves >= ell) { A.local_limit = true; A.termination = "move_limit"; A.returned = best; A.returned_F = bestF; break; }
      C = best; CF = bestF; A.moves++; A.path.push_back(C); A.path_F.push_back(CF);
    } else { A.termination = "no_improvement"; A.local_certified = true; A.returned = C; A.returned_F = CF; break; }
  }
  led.compact();
  return A;
}
static bool same_store(const Store& a, const Store& b) {
  if (a.size() != b.size()) return false;
  for (size_t i = 0; i < a.size(); ++i) if (!same_bits(a.v[i], b.v[i]) || !same_model(a.model(i), b.model(i))) return false;
  return true;
}
static bool same_ledger(const Ledger& a, const Ledger& b) {
  bool ok = a.has_hpm == b.has_hpm && a.hpmS == b.hpmS && same_bits(a.hpmF, b.hpmF) && a.hpm_ev.key == b.hpm_ev.key &&
            a.hpm_ev.phase == b.hpm_ev.phase && same_store(a.top, b.top) && same_store(a.lead0, b.lead0) && same_store(a.lead1, b.lead1) &&
            same_bits_v(a.island_best, b.island_best);
  for (int x = 0; x < N_PHASE; ++x) for (int y = 0; y < N_MECH; ++y) ok = ok && a.logical[x][y] == b.logical[x][y];
  return ok;
}
static bool same_archive(const LocalArchive& a, const LocalArchive& b) {
  return a.centre == b.centre && same_bits(a.centre_F, b.centre_F) && a.path == b.path && same_bits_v(a.path_F, b.path_F) &&
         a.scanned == b.scanned && same_bits_v(a.scanned_F, b.scanned_F) && a.scan_complete == b.scan_complete && a.scan_size == b.scan_size &&
         a.termination == b.termination && a.local_limit == b.local_limit && a.local_certified == b.local_certified &&
         a.returned == b.returned && same_bits(a.returned_F, b.returned_F) && a.moves == b.moves && a.n_eval == b.n_eval;
}

TEST(wp4_tail_threads_vs_serial) {
  for (int trial = 0; trial < 6; ++trial) {
    std::mt19937_64 g(100 + trial);
    int p = 150 + 37 * trial, K = trial == 3 ? 3 : 12;   // trial 3: the cap K binds (additions skipped)
    std::vector<double> w(p); for (auto& x : w) x = 0.25 * (double)((int)(g() % 41) - 20);   // coarse grid: exact ties
    ToyFactory fac{&w};
    Model c0; for (int j = 0; j < std::min(K, 3); ++j) c0.push_back((int)(g() % p)); std::sort(c0.begin(), c0.end()); c0.erase(std::unique(c0.begin(), c0.end()), c0.end());
    int ell = trial % 2 ? 2 : 50;   // odd trials: the move cap binds (local_limit)
    // small store caps make the would_enter filter matter
    auto fresh = [&]() { Ledger L = mkled(p, 4, true); L.top.init(60, Order::HPM); L.lead0.init(40, Order::LEX); L.lead1.init(40, Order::LEX); return L; };
    Ledger ref = fresh(); auto Aref = serial_local(c0, ell, trial % 3 == 0, trial % 3 == 0 ? PH_LS0 : PH_LOCAL, ref, fac, p, K, 0);
    for (int th : {1, 3}) for (size_t ch : {size_t(7), size_t(64), size_t(100000)}) {
      Ledger L = fresh(); merge::TailSettings ts; ts.threads = th; ts.chunk = ch; ts.K = K; ts.p = p; ts.zob = &zob();
      auto A = merge::local_search(c0, ell, trial % 3 == 0, trial % 3 == 0 ? PH_LS0 : PH_LOCAL, L, fac, ts);
      CHECK(same_archive(A, Aref));
      CHECK(same_ledger(L, ref));
    }
  }
  // numerical failure inside a scan: offers before the failing position applied, then NumericalFailure
  {
    int p = 80, K = 10; std::vector<double> w(p); for (int j = 0; j < p; ++j) w[j] = 0.5 * ((j * 7) % 13) - 3;
    Model c0{5, 9}; Model bad{5, 9, 40};
    ToyFactory ff{&w, bad, true};
    Ledger L = mkled(p, 4, false); merge::TailSettings ts; ts.threads = 3; ts.chunk = 8; ts.K = K; ts.p = p; ts.zob = &zob();
    bool threw = false;
    try { merge::local_search(c0, 5, false, PH_LOCAL, L, ff, ts); } catch (const NumericalFailure&) { threw = true; }
    CHECK(threw);
    CHECK(L.logical[PH_LOCAL][ME_LOCAL] == 40);   // positions 1..40 (flip j = 0..39) evaluated before the failure at j = 40
  }
}

// ---------------------------------------------------------------------------------------------------------------------
// ledger merge is order-free; merge assembly; GUARD-W (T10)
TEST(wp4_merge_guardw_t10) {
  const int p = 60, R = 4;
  std::vector<double> w(p); for (int j = 0; j < p; ++j) w[j] = 0.25 * ((j * 11) % 17) - 2;
  ToyFactory fac{&w}; ToyEval ev = fac.make();
  std::mt19937_64 g(5);
  auto island = [&](int r) {
    merge::IslandIn I; I.r = r; I.N = 100; I.Hm = 4; I.logZ = -50 + 0.1 * r; I.ess.assign(10, 80.0);
    I.pip.assign(p, 0.0); for (int j = 0; j < p; ++j) I.pip[j] = std::fmod(0.013 * (j + 1) * (r + 2), 1.0);
    I.led = mkled(p, R, false);
    for (int t = 0; t < 400; ++t) {
      Model S; int k = 1 + (int)(g() % 4); for (int a = 0; a < k; ++a) S.push_back((int)(g() % p));
      std::sort(S.begin(), S.end()); S.erase(std::unique(S.begin(), S.end()), S.end());
      double lm, lg0, d, F; ev(S, lm, lg0, d, F);
      EventCtx e; e.phase = PH_MEASURED; e.mech = ME_GIBBS_FLIP; e.key.seg = SG_FINAL; e.key.unit = (uint32_t)r; e.key.xph = X_MEASURED;
      e.key.stage = 30; e.key.round = 1 + t / 100; e.key.particle = 1 + t % 100; e.key.position = 1 + (uint32_t)(g() % 70);
      I.led.event(S, zob().hash(S), F, lg0, lm, e, true);
      if (t >= 300) I.terminal.push_back(S);   // the last measured round: N = 100 supports
    }
    I.led.compact();
    return I;
  };
  std::vector<merge::IslandSlot> slots(R);
  for (int r = 1; r <= R; ++r) { slots[r - 1].load = merge::Load::ok; slots[r - 1].isl = island(r); }
  // order-freeness of Ledger.merge
  Ledger a = mkled(p, R, false), b = mkled(p, R, false);
  for (int r : {0, 1, 2, 3}) a.merge(slots[r].isl.led);
  for (int r : {3, 1, 0, 2}) b.merge(slots[r].isl.led);
  a.compact(); b.compact();
  CHECK(same_ledger(a, b));
  merge::MergeSettings ms; ms.Rp = R; ms.N = 100; ms.p = p; ms.K = 8; ms.ell = 5; ms.threads = 3; ms.chunk = 16; ms.occ_M = {1, 10}; ms.zob = &zob();
  Ledger pre = mkled(p, R, false);
  auto fo = merge::merge_and_tail(slots, Ledger(pre), Model{1, 2}, fac, ms);
  CHECK(fo.status == Status::completed && fo.estimates_available);
  CHECK(fo.hpm == fo.local.returned || fo.hpm == fo.ls0.returned);
  double lz = calib::lse_cal(fo.logZ_r);
  CHECK(same_bits(fo.log_Z, lz - std::log(4.0)));
  double sw = 0; for (double x : fo.W_r) sw += x; CHECK(std::fabs(sw - 1) < 1e-12 && fo.R_eff >= 1 && fo.R_eff <= 4);
  double sp = 0; for (int j = 0; j < p; ++j) sp += fo.pip_T[j]; CHECK(sp > 0);
  CHECK(fo.occ_available && fo.occ.size() == 2 && fo.occ[0].M_used == 1 && fo.occ[0].occ_r.size() == 4);
  {  // per-model counts agree with the M-set occupancies
    uint64_t in10 = 0; for (size_t i = 0; i < fo.occ_top.size(); ++i) in10 += fo.occ_top[i];
    CHECK(fo.occ_top.size() == 10 && fo.occ_total == 400 && fo.occ_total_r == std::vector<uint64_t>(4, 100) && fo.occ_top_r.size() == 40);
    CHECK(same_bits((double)in10 / (double)fo.occ_total, fo.occ[1].occ));
  }
  CHECK(fo.log_Z_T >= fo.hpm_F);   // lower bound contains the HPM's mass
  // T10: GUARD-W paths -- no estimates, declared statuses
  auto run_fault = [&](int which) {
    auto s2 = slots;
    if (which == 0) s2[2].load = merge::Load::missing;
    if (which == 1) s2[2].load = merge::Load::corrupt;
    if (which == 2) s2[2].load = merge::Load::hash_mismatch;
    if (which == 3) s2[2].isl.status = Status::numerical_failure;
    if (which == 4) s2[2].isl.status = Status::resource_limit;
    if (which == 5) s2.pop_back();
    if (which == 6) s2[2].isl.r = 1;   // wrong island id
    return merge::merge_and_tail(s2, Ledger(pre), Model{1, 2}, fac, ms);
  };
  Status want[] = {Status::io_error, Status::invalid_input, Status::invalid_input, Status::numerical_failure, Status::resource_limit,
                   Status::invalid_input, Status::invalid_input};
  for (int f = 0; f < 7; ++f) {
    auto o = run_fault(f);
    CHECK(o.status == want[f] && !o.estimates_available && o.fit_state == "incomplete" && o.log_Z == 0 && o.pip_eq.empty() && o.mpm.empty());
  }
  {  // tail numerical failure
    ToyFactory ff{&w, Model{}, true};
    Ledger tmp = pre; for (auto& s : slots) tmp.merge(s.isl.led);
    Model bad = tmp.hpmS; bad.insert(std::lower_bound(bad.begin(), bad.end(), 59), 59);
    if (std::adjacent_find(bad.begin(), bad.end()) != bad.end()) bad.erase(std::find(bad.begin(), bad.end(), 59));
    ff.bad = bad;
    auto o = merge::merge_and_tail(slots, Ledger(pre), Model{1, 2}, ff, ms);
    CHECK(o.status == Status::numerical_failure && !o.estimates_available && o.hpm_incomplete && o.pip_eq.empty());
  }
  {  // runtime guard in the tail
    auto o = merge::merge_and_tail(slots, Ledger(pre), Model{1, 2}, fac, ms, [](double, const std::string& c) { return c == "ls0"; });
    CHECK(o.status == Status::resource_limit && !o.estimates_available && o.has_ls0);
  }
  {  // F8: a non-finite island log Z_r -> numerical_failure, no estimates
    auto s2 = slots; s2[1].isl.logZ = std::numeric_limits<double>::infinity();
    auto o = merge::merge_and_tail(s2, Ledger(pre), Model{1, 2}, fac, ms);
    CHECK(o.status == Status::numerical_failure && !o.estimates_available && o.pip_eq.empty());
  }
  {  // memory admission (--mem-budget): refused before any island store is loaded
    merge::MergeSettings m2 = ms; m2.mem_budget_bytes = 1000;
    auto o = merge::merge_and_tail(slots, Ledger(pre), Model{1, 2}, fac, m2);
    CHECK(o.status == Status::resource_limit && o.fit_state == "not_admitted" && !o.estimates_available && !o.has_hpm);
    m2.mem_budget_bytes = o.mem.total; auto o2 = merge::merge_and_tail(slots, Ledger(pre), Model{1, 2}, fac, m2);
    CHECK(o2.status == Status::completed);
    merge::MergeSettings big; big.p = 1000000; big.Rp = 16; big.N = 2500; big.threads = 96; big.chunk = 2048;
    merge::MemEstimate e = merge::estimate_merge_memory(big);
    CHECK(e.total < 16ull << 30);   // ESTIMATE at 10^6, V mode: ~11.7 GB <= the 16 GB target
  }
  {  // F5: zero occupancy -> NA row (no +Inf), zero islands excluded from the sd and the chi-square
    auto s2 = slots;
    for (auto& sl : s2) sl.isl.terminal.assign(100, Model{0, 1, 2, 3, 4, 5, 6, 7});   // N supports, none in any store
    s2[0].isl.terminal[0] = fo.hpm;                                                      // island 1 only: one HPM particle
    auto o = merge::merge_and_tail(s2, Ledger(pre), Model{1, 2}, fac, ms);
    CHECK(o.occ_available && o.occ[0].available && o.occ[0].n_zero_islands == 3 && std::isnan(o.occ[0].log_Z_occ_r[1]) &&
          std::isfinite(o.occ[0].log_Z_occ) && std::isnan(o.occ[0].sd_log_Z_occ_r) && o.occ[0].chi2_df == 0);
    for (auto& sl : s2) sl.isl.terminal.assign(100, Model{0, 1, 2, 3, 4, 5, 6, 7});
    auto o3 = merge::merge_and_tail(s2, Ledger(pre), Model{1, 2}, fac, ms);
    CHECK(!o3.occ[0].available && std::isnan(o3.occ[0].log_Z_occ) && o3.occ[0].n_zero_islands == 4);
  }
  {  // streaming: an island that changes between the head check and its load -> refused (no subset pooled)
    struct Flaky : merge::VectorSource { using VectorSource::VectorSource; merge::IslandIn load(int r) override { auto I = VectorSource::load(r); if (r == 3) I.r = 9; return I; } };
    Flaky src(slots);
    auto o = merge::merge_stream(src, Ledger(pre), Model{1, 2}, fac, ms);
    CHECK(o.status == Status::invalid_input && o.fit_state == "incomplete" && !o.estimates_available);
  }
  CHECK(fit_status({Status::completed, Status::io_error, Status::numerical_failure}) == Status::numerical_failure);
  CHECK(fit_status({Status::resource_limit, Status::invalid_input}) == Status::invalid_input);
}

TEST(wp4_inherited_provenance_v016) {
  // INTERFACES v0.1.6: the calibration HPM model is offered with its CALIBRATION EventCtx. Three cases (core/cpp/
  // v3_core.cpp:416-441): (i) also a table model -> table key; (ii) inherited only -> calibration key; (iii) neither ->
  // never offered. Other inherited models carry INHERITED keys with their input index.
  LedgerConfig cfg; cfg.p = 10; cfg.islands = 4; cfg.leaders = false; cfg.fresh_counters = false;
  Zobrist z; z.init(10);
  EventCtx cal; cal.phase = PH_DIAG; cal.mech = ME_USWAP; cal.key.seg = SG_CALIB; cal.key.iter = 2; cal.key.unit = 3; cal.key.stage = 4;
  Model T{2, 3}, A{1, 5};
  auto run = [&](bool table_has, const std::vector<merge::InheritedModel>& inh, const Model& chpm) {
    Ledger L(cfg);
    if (table_has) L.event(T, z.hash(T), 5.0, 1.0, 4.0, merge::table_event(1, 3), true);
    merge::offer_inherited(L, inh, true, chpm, cal, z);
    return L;
  };
  merge::InheritedModel iT{T, 5.0, 1.0, 4.0}, iA{A, 4.0, 1.0, 3.0};
  Ledger L1 = run(true, {iA, iT}, T);    // (i)
  CHECK(L1.hpmS == T && L1.hpm_ev.phase == PH_TABLE && L1.hpm_ev.key.seg == SG_TABLE && L1.hpm_ev.key.position == 3);
  Ledger L2 = run(false, {iA, iT}, T);   // (ii)
  CHECK(L2.hpmS == T && L2.hpm_ev.key == cal.key && L2.hpm_ev.phase == PH_DIAG);
  Ledger L3 = run(false, {iA}, T);       // (iii)
  CHECK(L3.hpmS == A && L3.hpm_ev.phase == PH_INHERITED && L3.hpm_ev.key.particle == 0);
  Ledger L4 = run(false, {iA, iT}, A);   // another model is the calibration HPM: T keeps its INHERITED key, index 1
  CHECK(L4.hpmS == T && L4.hpm_ev.phase == PH_INHERITED && L4.hpm_ev.key.particle == 1);
  // order-free: the island events of the same model (FINAL, later key) never take the provenance
  EventCtx fin; fin.phase = PH_MEASURED; fin.mech = ME_GIBBS_FLIP; fin.key.seg = SG_FINAL; fin.key.unit = 1;
  Ledger L5 = run(false, {iA, iT}, T); L5.event(T, z.hash(T), 5.0, 1.0, 4.0, fin, true);
  CHECK(L5.hpm_ev.key == cal.key);
}

#include "tutil.h"
#include "v4/format.h"
#include "v4/wp4_terminal.h"
TEST(wp4_terminal_supports_wp3_layout) {
  // island_r.bin terminal sections exactly as WP3 writes them (PR #21 island_file.cpp:60-64): N + 1 i64 offsets, i32 pool,
  // particle order, the last measured round only. Round trip through the WP1 container, then the merge's occupancy.
  const int N = 6, p = 20;
  std::vector<Model> sup = {{1, 4}, {}, {1, 4}, {2, 3, 19}, {1, 4}, {7}};
  std::vector<int64_t> tptr{0}; std::vector<int32_t> tS;
  for (auto& S : sup) { tS.insert(tS.end(), S.begin(), S.end()); tptr.push_back((int64_t)tS.size()); }
  std::string path = tmp_path("wp4_terminal_island.bin");
  {
    fmt::Writer w(fmt::K_ISLAND, fmt::M_LAW);
    Json m = Json::object(); m["N"] = N; m["p"] = p; w.add_json("meta", m);
    w.add_copy("terminal_S_ptr", fmt::D_I64, tptr.data(), tptr.size() * 8, tptr.size(), 0);
    w.add_copy("terminal_S", fmt::D_I32, tS.data(), tS.size() * 4, tS.size(), 0);
    w.write(path);
  }
  {
    fmt::Reader R(path);
    std::vector<Model> got = merge::read_terminal_supports(R, N, p);
    CHECK(got == sup);
    CHECK_THROWS(merge::read_terminal_supports(R, N + 1, p));   // Hm x N or any other count is refused
    CHECK_THROWS(merge::read_terminal_supports(R, N, 10));      // index out of range
  }
  std::remove(path.c_str());
  // the merge requires exactly N supports per island (or none)
  std::vector<double> w(p); for (int j = 0; j < p; ++j) w[j] = 0.25 * ((j * 7) % 11) - 1;
  ToyFactory fac{&w}; ToyEval ev = fac.make();
  const int R = 2;
  std::vector<merge::IslandSlot> slots(R);
  for (int r = 1; r <= R; ++r) {
    merge::IslandIn& I = slots[r - 1].isl; slots[r - 1].load = merge::Load::ok;
    I.r = r; I.N = N; I.logZ = -5 - r; I.ess = {5, 6}; I.pip.assign(p, 0.1 * r); I.led = mkled(p, R, false);
    for (auto& S : sup) { double lm, lg0, d, F; ev(S, lm, lg0, d, F); EventCtx e; e.phase = PH_MEASURED; e.mech = ME_GIBBS_FLIP; e.key.seg = SG_FINAL; e.key.unit = (uint32_t)r; I.led.event(S, zob().hash(S), F, lg0, lm, e, true); }
    I.led.compact(); I.terminal = sup;
  }
  merge::MergeSettings ms; ms.Rp = R; ms.N = N; ms.p = p; ms.K = 5; ms.ell = 2; ms.occ_M = {1, 10}; ms.zob = &zob();
  auto o = merge::merge_and_tail(slots, mkled(p, R, false), Model{}, fac, ms);
  CHECK(o.status == Status::completed && o.occ_total == (uint64_t)(R * N) && o.occ_total_r == std::vector<uint64_t>({N, N}));
  slots[1].isl.terminal.push_back(Model{1, 4});   // N + 1 supports (e.g. a writer that kept more than the last round)
  auto o2 = merge::merge_and_tail(slots, mkled(p, R, false), Model{}, fac, ms);
  CHECK(o2.status == Status::invalid_input && !o2.estimates_available);
}
