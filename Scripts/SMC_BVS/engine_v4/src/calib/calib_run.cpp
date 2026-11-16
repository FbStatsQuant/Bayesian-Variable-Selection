// calib_run.cpp -- `smcbvs4 calibrate` (WP4; spec §1 row 3). Reads data.bin and setup.bin, builds the calibration
// ledger (tables from setup.bin's table top stores), runs calib::calibrate_with over the island runner, writes calib.bin.
// The island runner is WP3's island with calibration roles (WP3_DESIGN §1.11; island::CalibIslandRunner); the start
// law and the neighbour lists come from setup.bin (island/setup_load.h).
#include "v4/calib_run.h"
#include <chrono>
#include "v4/island/calib_runner.h"
#include "v4/island/setup_load.h"
#include "v4/prep.h"
#include "v4/stubs.h"
#include "v4/wp4_io.h"

namespace v4::calib {

namespace {
// per-chunk evaluator for V, the local searches and the inherited export: bit scorer + comp(S) of the setup tables
// (core/cpp/v3_engine.h:84-90; the same as the merge command's)
struct CalibEval {
  const Data* D; const wp4io::SetupView* S; BitScorer sc; std::vector<std::pair<int32_t, int32_t>> scratch;
  CalibEval(const Data* d, const wp4io::SetupView* s) : D(d), S(s), sc(d) {}
  void operator()(const Model& M, double& lm, double& lg0, double& dd, double& F) {
    lm = sc.score(M).logm;
    double c = S->comp(M, scratch); size_t k = M.size();
    lg0 = D->logprior[k] + c; dd = (lm - D->logm0) - c; F = D->logprior[k] + lm;
  }
};
struct CalibFactory { const Data* D; const wp4io::SetupView* S; CalibEval make() const { return CalibEval(D, S); } };
std::string str_arg(const Json& a, const char* k, const std::string& d = "") { return a.contains(k) && a.at(k).type() == Json::STR ? a.at(k).str() : d; }
double num_arg(const Json& a, const char* k, double d) { return a.contains(k) && a.at(k).type() == Json::NUM ? a.at(k).num() : d; }
}

Json run(const Json& args) {
  const std::string dpath = str_arg(args, "data"), spath = str_arg(args, "setup"), out = str_arg(args, "out");
  if (dpath.empty() || spath.empty() || out.empty()) throw Error(Status::invalid_input, "calibrate: --data, --setup and --out are required");
  const std::string mode_s = str_arg(args, "mode", args.contains("manifest") && args.at("manifest").contains("mode") ? args.at("manifest").at("mode").str() : "");
  if (mode_s.empty()) throw Error(Status::invalid_input, "calibrate: mode not given (--mode or the manifest's mode)");
  const uint32_t mode = fmt::mode_from_name(mode_s);
  const double seed = num_arg(args, "seed", -1);
  if (!(seed >= 1) || seed != std::floor(seed) || seed > 2147483647.0) throw Error(Status::invalid_input, "calibrate: --seed must be a whole number in [1, 2^31 - 1]");
  std::string dhash;
  Data D = prep::load_data(dpath, &dhash);
  wp4io::SetupView S = wp4io::read_setup(spath, D.p, D.K, &D.zob);
  const Budgets b = budgets(D.n, D.p);
  const Rule rule = mode == fmt::M_V ? Rule::bounded : Rule::coded;   // theory mode (compat, law): coded; V: bounded (D-2, D-26)
  Settings s = settings_from(b, rule);
  if (rule == Rule::bounded) {
    s.I_max = (int)num_arg(args, "I_max", 3); s.refine_m = (int)num_arg(args, "refine_m", 1);
  }
  s.threads = (int)num_arg(args, "threads", 1);
  // the island runner: WP3's island with calibration roles (PILOT / DIAG; WP3_DESIGN §1.11). Theory modes (compat, law)
  // run the bit form particle-major (D-21; compat: 1 thread, v3 streams 0-9 owned by the runner); V runs class A
  // label-major with every thread.
  const island::Start st = island::load_start(spath, D);
  const island::Neighbours nb = island::load_neighbours(spath, D.p);
  island::CalibRunnerConfig rc; rc.seed = (uint32_t)seed; rc.B = b.B; rc.threads = s.threads;
  rc.mem_budget = (uint64_t)num_arg(args, "mem_budget", 0);
  rc.inputs_bytes = island::start_bytes(st, nb);   // the island's setup inputs (dep::Start; the flat view will shrink it)
  if (mode == fmt::M_COMPAT) { rc.compat = true; rc.kernel = island::KernelKind::ParticleMajor; rc.threads = 1; }
  else if (mode == fmt::M_LAW) rc.kernel = island::KernelKind::ParticleMajor;
  else rc.kernel = island::KernelKind::LabelMajor;
  LedgerConfig lc; lc.p = D.p; lc.islands = 4; lc.leaders = true; lc.fresh_counters = false;
  Ledger led(lc);
  wp4io::offer_tables(led, S, D.K, D.zob);   // the calibration ledger starts with the tables (core v3_core.cpp:613)
  merge::TailSettings ts; ts.threads = s.threads; ts.chunk = 64; ts.K = D.K; ts.p = D.p; ts.zob = &D.zob;
  CalibFactory fac{&D, &S};
  auto t0 = std::chrono::steady_clock::now();
  CalibOutcome oc;
  if (mode == fmt::M_V) { island::CalibIslandRunner<island::Arith::ClassA> run(D, st, nb, rc); oc = calibrate_with(run, std::move(led), fac, s, ts); }
  else { island::CalibIslandRunner<island::Arith::Bit> run(D, st, nb, rc); oc = calibrate_with(run, std::move(led), fac, s, ts); }
  const CalibOut& co = oc.co;
  Json rec = Json::object();
  rec["command"] = "calibrate"; rec["status"] = cal_status_name(co.status); rec["tier_final"] = co.tier_final;
  rec["seconds"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  if (co.status == CalStatus::ok) {
    wp4io::CalibWrite cw; cw.mode = mode; cw.co = &co; cw.led = &oc.led; cw.inherited = oc.inherited;
    cw.N = b.N[co.tier_final]; cw.L = s.tiers[co.tier_final].L; cw.Hm = s.tiers[co.tier_final].Hm; cw.stages = oc.stages;
    cw.inputs["data.bin"] = dhash; cw.inputs["setup.bin"] = S.content_hash;
    cw.extra["seed"] = seed; cw.extra["rule"] = rule == Rule::coded ? "coded" : "bounded"; cw.extra["threads"] = s.threads;
    rec["calib_bin"] = wp4io::write_calib(out, cw);
  } else rec["exit_status"] = status_name(task_status(co.status));
  return rec;
}

}  // namespace v4::calib
