// calib_run.cpp -- `smcbvs4 calibrate` (WP4; spec §1 row 3). Reads data.bin and setup.bin, builds the calibration
// ledger (tables from setup.bin's table top stores), runs calib::calibrate_with over the island runner, writes calib.bin.
// The island runner is WP3's island with calibration roles (WP3_DESIGN §1.11; island::CalibIslandRunner); the start law
// and the neighbour lists come from setup.bin (island/setup_load.h).
//
//   smcbvs4 calibrate --data D --setup S --seed s --mode compat|law|V --out calib.bin [--threads k] [--mem-budget BYTES]
//                     [--I_max i --refine_m m (V only)]
//   smcbvs4 calibrate --plan-only 1 --mode M (--data D | --n n --p p) [--mem-budget BYTES]   settings + memory plan, no run
#include <sys/stat.h>
#include <chrono>
#include <cmath>
#include "v4/calib_run.h"
#include "v4/cmd_args.h"
#include "v4/island/calib_runner.h"
#include "v4/island/setup_load.h"
#include "v4/format.h"
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
std::string str_arg(const Json& a, const char* k, const std::string& d = "") {
  if (!a.contains(k)) return d;
  if (a.at(k).type() != Json::STR) throw Error(Status::invalid_input, std::string("calibrate: --") + k + " must be a string");
  return a.at(k).str();
}
// a whole number in [lo, hi] (review PR37 m-4: no unchecked casts)
int64_t whole_arg(const Json& a, const char* k, int64_t dflt, int64_t lo, int64_t hi) {
  if (!a.contains(k)) return dflt;
  const Json& v = a.at(k);
  if (v.type() != Json::NUM) throw Error(Status::invalid_input, std::string("calibrate: --") + k + " must be a number");
  const double x = v.num();
  if (!std::isfinite(x) || x != std::floor(x) || x < (double)lo || x > (double)hi)
    throw Error(Status::invalid_input, std::string("calibrate: --") + k + " must be a whole number in [" + std::to_string(lo) + ", " + std::to_string(hi) + "]");
  return (int64_t)x;
}
uint64_t file_bytes(const std::string& p) { struct stat st{}; return ::stat(p.c_str(), &st) == 0 ? (uint64_t)st.st_size : 0; }
Json settings_json(const Settings& s, const Budgets& b, Rule rule) {
  Json j = Json::object();
  j["rule"] = rule == Rule::coded ? "coded" : "bounded"; j["I_max"] = s.I_max; j["refine_m"] = s.refine_m;
  j["sum_mode"] = s.sum_mode == SumMode::Serial ? "serial" : "blocked";
  Json t = Json::array();
  for (int e = 0; e < (rule == Rule::coded ? 2 : 1); ++e) {
    Json x = Json::object(); x["tier"] = e; x["H"] = s.tiers[e].H; x["T_e"] = s.tiers[e].Te; x["L"] = s.tiers[e].L; x["Hm"] = s.tiers[e].Hm;
    x["ell"] = s.tiers[e].ell; x["N_final"] = frozen_N(b, rule, e); t.push(x);
  }
  j["tiers"] = t; j["K"] = b.K; j["B"] = b.B;
  return j;
}
Json plan_json(const CalibMemPlan& m, uint64_t budget, double kbar) {
  Json j = Json::object();
  auto u = [](uint64_t x) { return Json((double)x); };
  j["label"] = "ESTIMATE (calibration memory plan: 3 calibration stores, one island ledger in flight, flat V / export, inputs)";
  j["kbar"] = kbar; j["ledger"] = u(m.ledger); j["island_ledger"] = u(m.island_ledger); j["export"] = u(m.export_);
  j["inputs"] = u(m.inputs); j["resident"] = u(m.resident); j["total"] = u(m.total); j["budget"] = u(budget);
  return j;
}
// The calibration island's own plan (review PR39 MAJOR-2; WP3_DESIGN §1.11): the largest island of the calibration (the
// largest H and Hm over the tiers the rule can use), with the leader stores and the round-start snapshot, planned as
// CalibIslandRunner admits it under WP4's N-1 rule: the caller-supplied term = the setup inputs (start_bytes) + the
// calibration's resident state without the inputs (ledger + export); admitted iff that plan <= --mem-budget. With
// setup.bin it is plan_island on the real Start; without it, sizes only (k = kbar, setup inputs 0: an ESTIMATE floor).
// The calibration island's plans (largest island of the calibration: max H and Hm over the tiers the rule can use, leaders,
// round-start snapshot), planned as CalibIslandRunner admits it under the N-1 rule: the caller-supplied term = setup inputs +
// the calibration's resident state without them. `ip` at the G the budget allows, `ip1` at G = 1 (the admission floor).
// With the setup's dimensions (read_setup_dims: nothing expanded) k = q90 rule and the inputs = the Start model; without
// them, sizes only (k = kbar, setup inputs 0). The same numbers drive --plan-only and the run's up-front refusal (PR52 MAJOR-2).
struct IslandPlans { island::MemPlan ip, ip1; double setup_in = 0; };
IslandPlans calib_island_plans(const Settings& s, Rule rule, uint32_t mode, int B, int K, int64_t n, int64_t p, uint64_t budget,
                               uint64_t resident_own, const island::SetupDims* sd, double kbar) {
  island::IslandConfig ic; ic.role = island::IslandRole::Pilot; ic.island = 0; ic.leaders = true; ic.B = B; ic.G = 0; ic.mem_budget = budget;
  ic.N = 1; ic.Hm = 1;
  for (int e = 0; e < (rule == Rule::coded ? 2 : 1); ++e) { ic.N = std::max(ic.N, s.tiers[e].H); ic.Hm = std::max(ic.Hm, s.tiers[e].Hm); }
  ic.compat = mode == fmt::M_COMPAT; ic.threads = ic.compat ? 1 : s.threads;
  ic.kernel = mode == fmt::M_V ? island::KernelKind::LabelMajor : island::KernelKind::ParticleMajor;
  IslandPlans r; r.setup_in = sd ? island::start_inputs_bytes(*sd, ic.threads) : 0.0;   // mapped sections (StartView) or the rebuild model
  ic.inputs_bytes = r.setup_in + (double)resident_own;
  const double k = sd ? island::plan_k(sd->size_logmass, 0.0) : kbar;
  island::IslandConfig ic1 = ic; ic1.G = 1; ic1.mem_budget = 0;
  island::MemSizes z = island::plan_sizes((int)n, (int)p, K, ic), z1 = island::plan_sizes((int)n, (int)p, K, ic1);
  r.ip = island::plan_with_budget(z, k, ic); r.ip1 = island::plan_with_budget(z1, k, ic1);
  return r;
}

Json island_plan_json(const island::MemPlan& mp, uint64_t floor, uint64_t budget, double setup_inputs, uint64_t resident_own, bool from_files) {
  Json j = Json::object();
  auto u = [](uint64_t x) { return Json((double)x); };
  j["label"] = from_files ? "ESTIMATE (calibration island plan, memory.h, real setup; = the task's predicted peak under N-1)"
                          : "ESTIMATE (calibration island plan from sizes: k = kbar, setup inputs NOT counted)";
  Json it = Json::object(); for (const auto& x : mp.items) it[x.name] = u(x.bytes);
  j["items"] = it; j["G"] = mp.G; j["k"] = mp.k; j["setup_inputs"] = setup_inputs; j["resident"] = u(resident_own);
  // floor = the plan at G = 1: with a budget the island takes the largest G <= 256 that fits, so it is admitted iff
  // floor <= --mem-budget (the smallest budget the calibration can run with; the driver sizes from it)
  j["total"] = u(mp.total); j["floor"] = u(floor); j["budget"] = u(budget); j["admitted"] = budget == 0 || mp.total <= budget;
  j["text"] = island::mem_plan_text(mp);
  return j;
}
}  // namespace

Json run(const Json& args) {
  // mode: compat | law | V only (review PR37 m-4)
  // the driver's manifest is the authority (cmd_args.h; as merge and island): inputs by base name, its mode; a
  // disagreeing explicit argument is refused. Before, calibrate read --data / --setup only, so the driver's stage
  // (`calibrate --manifest m.json --out ...`) failed with "--data is required".
  const Json man = cmd::manifest_of(args, "calibrate");
  // the manifest freezes the scientific parameters: an explicit different seed / I_max / refine_m is refused, whichever side
  // of --manifest it is given (review PR52 MAJOR-4)
  cmd::refuse_manifest_conflicts(args, man, "calibrate", {"seed", "I_max", "refine_m"});
  std::string mode_s = str_arg(args, "mode");
  if (man.contains("mode")) {
    const Json& mm = man.at("mode");
    if (mm.type() != Json::STR) throw Error(Status::invalid_input, "calibrate: the manifest's mode must be a string");
    if (!mode_s.empty() && mode_s != mm.str()) throw Error(Status::invalid_input, "calibrate: --mode differs from the manifest's mode");
    mode_s = mm.str();
  }
  if (mode_s != "compat" && mode_s != "law" && mode_s != "V") throw Error(Status::invalid_input, "calibrate: --mode must be compat, law or V");
  const uint32_t mode = fmt::mode_from_name(mode_s);
  const Rule rule = mode == fmt::M_V ? Rule::bounded : Rule::coded;   // theory mode (compat, law): coded; V: bounded (D-2, D-26)
  if (rule == Rule::coded && (args.contains("I_max") || args.contains("refine_m")))
    throw Error(Status::invalid_input, "calibrate: --I_max / --refine_m apply to the bounded rule (mode V) only");
  const int threads = (int)whole_arg(args, "threads", 1, 1, 4096);
  const uint64_t budget = (uint64_t)whole_arg(args, "mem_budget", 0, 0, (int64_t)1 << 50);   // bytes, 0 = off (INTERFACES §7)
  const bool plan_only = whole_arg(args, "plan_only", 0, 0, 1) == 1;
  // n, p: data.bin, or --n / --p for a plan
  const std::string dpath = cmd::input_path(args, man, "data", "data.bin", "calibrate", false),
                    spath = cmd::input_path(args, man, "setup", "setup.bin", "calibrate", false), out = str_arg(args, "out");
  Data D; std::string dhash; int64_t n = 0, p = 0;
  if (!dpath.empty()) { D = prep::load_data(dpath, &dhash); n = D.n; p = D.p; }
  else if (plan_only) { n = whole_arg(args, "n", 0, 3, (int64_t)1 << 31); p = whole_arg(args, "p", 0, 1, (int64_t)1 << 31); }
  if (n < 3 || p < 1) throw Error(Status::invalid_input, "calibrate: --data is required (or --n and --p with --plan-only)");
  const Budgets b = budgets(n, p);
  Settings s = settings_from(b, rule);
  if (rule == Rule::bounded) {
    s.I_max = (int)whole_arg(args, "I_max", 3, 0, 1000); s.refine_m = (int)whole_arg(args, "refine_m", 1, 1, 64);
  }
  s.threads = threads;
  Driver::validate(s);   // e.g. I_max > ell -> invalid_input, before anything runs (review PR37 m-4)
  // memory plan (review PR37 M-5): kbar = the largest of the start mode's size + 1 and 8 (ESTIMATE until calibration measures it)
  wp4io::SetupView S; double kbar = 8;
  if (!plan_only || (!spath.empty() && !dpath.empty())) {
    if (spath.empty()) throw Error(Status::invalid_input, "calibrate: --setup is required");
    S = wp4io::read_setup(spath, D.p, D.K, &D.zob);
    if (!S.data_hash.empty() && S.data_hash != dhash) throw Error(Status::invalid_input, "calibrate: setup.bin was built from another data.bin");
    kbar = std::max(kbar, (double)S.mode_S.size() + 1);
  }
  const CalibMemPlan plan = calib_memory_plan(p, kbar, file_bytes(dpath) + file_bytes(spath));
  Json rec = Json::object();
  rec["settings"] = settings_json(s, b, rule); rec["mem_plan"] = plan_json(plan, budget, kbar); rec["n"] = (double)n; rec["p"] = (double)p;
  rec["mode"] = mode_s;
  const uint64_t resident_own = plan.ledger + plan.export_;
  const bool files = !dpath.empty() && !spath.empty();
  // the island plan from the dimensions (nothing of the setup expanded): printed on every plan-only outcome, admitted or not
  // (review PR52 m5), and the run's up-front refusal below
  island::SetupDims sdims; if (files) sdims = island::read_setup_dims(spath, p, D.K, false);
  const IslandPlans ipl = calib_island_plans(s, rule, mode, b.B, b.K, n, p, budget, resident_own, files ? &sdims : nullptr, kbar);
  const bool resident_ok = !(budget && plan.resident >= budget), island_ok = !(budget && ipl.ip.total > budget);
  if (plan_only) {
    rec["island_plan"] = island_plan_json(ipl.ip, ipl.ip1.total, budget, ipl.setup_in, resident_own, files);
    rec["plan_only"] = true;
    if (!resident_ok) { rec["status"] = "resource_limit"; rec["reason"] = "calibrate not admitted: calibration state " + std::to_string(plan.resident) + " B >= --mem-budget"; }
    else if (!island_ok) {
      rec["status"] = "resource_limit";
      rec["reason"] = "calibration island not admitted (N-1): resident + island plan " + std::to_string(ipl.ip.total) + " B > --mem-budget";
    } else rec["status"] = "completed";
    return rec;
  }
  if (!resident_ok) {   // the calibration's own state does not fit: refuse before any allocation
    rec["status"] = "resource_limit"; rec["reason"] = "calibrate not admitted: calibration state " + std::to_string(plan.resident) + " B >= --mem-budget";
    return rec;
  }
  if (!island_ok) {     // N-1: no calibration island can run beside the resident state: refuse BEFORE the Start is expanded
    rec["island_plan"] = island_plan_json(ipl.ip, ipl.ip1.total, budget, ipl.setup_in, resident_own, files);
    rec["status"] = "resource_limit";
    rec["reason"] = "calibration island not admitted (N-1): resident + island plan " + std::to_string(ipl.ip.total) + " B > --mem-budget";
    return rec;
  }
  if (out.empty()) throw Error(Status::invalid_input, "calibrate: --out is required");
  const int64_t seed = whole_arg(args, "seed", -1, 1, 2147483647);
  if (seed < 1) throw Error(Status::invalid_input, "calibrate: --seed is required (a whole number in [1, 2^31 - 1])");
  // the island runner: WP3's island with calibration roles (PILOT / DIAG; WP3_DESIGN §1.11). Theory modes (compat, law)
  // run the bit form particle-major (D-21; compat: 1 thread, v3 streams 0-9 owned by the runner); V runs class A
  // label-major with every thread.
  const island::StartView st = island::load_start_view(spath, D, sdims.mappable);   // mapped: the start law is not expanded
  const island::Neighbours nb = island::load_neighbours(spath, D.p, !sdims.mappable);   // the mapped loader verified the sections
  island::CalibRunnerConfig rc; rc.seed = (uint32_t)seed; rc.B = b.B; rc.threads = s.threads;
  rc.inputs_bytes = ipl.setup_in;   // the island's own setup inputs: the Start model of the plan above (StartView: the mapped lengths)
  if (mode == fmt::M_COMPAT) { rc.compat = true; rc.kernel = island::KernelKind::ParticleMajor; rc.threads = 1; }
  else if (mode == fmt::M_LAW) rc.kernel = island::KernelKind::ParticleMajor;
  else rc.kernel = island::KernelKind::LabelMajor;
  LedgerConfig lc; lc.p = D.p; lc.islands = 4; lc.leaders = true; lc.fresh_counters = false;
  Ledger led(lc);
  wp4io::offer_tables(led, S, D.K, D.zob);   // the calibration ledger starts with the tables (core v3_core.cpp:613)
  merge::TailSettings ts; ts.threads = s.threads; ts.chunk = 64; ts.K = D.K; ts.p = D.p; ts.zob = &D.zob;
  CalibFactory fac{&D, &S};
  // INTERFACES §7 (whole task), WP4's N-1 rule: every island gets the task budget unchanged and the calibration's own
  // state without the inputs (calibration ledger + export); the island's plan counts X, z, diag(G) and the setup inputs
  const uint64_t island_budget = budget;
  auto t0 = std::chrono::steady_clock::now();
  CalibOutcome oc;
  if (mode == fmt::M_V) { island::CalibIslandRunner<island::Arith::ClassA> run(D, st, nb, rc); oc = calibrate_with(run, std::move(led), fac, s, ts, resident_own, island_budget); }
  else { island::CalibIslandRunner<island::Arith::Bit> run(D, st, nb, rc); oc = calibrate_with(run, std::move(led), fac, s, ts, resident_own, island_budget); }
  const CalibOut& co = oc.co;
  // the record's `status` is the task status main() maps to the exit code (INTERFACES §7: "completed", 10 + status);
  // the calibration's own v3 name (ok, schedule_limit, ...) is `cal_status`. Before, `status` held "ok", which
  // status_from_name refuses: a successful `smcbvs4 calibrate` exited 13 with its record overwritten, and the driver's
  // fill refused calib.bin (its producer record was not "completed").
  rec["status"] = status_name(task_status(co.status)); rec["cal_status"] = cal_status_name(co.status); rec["tier_final"] = co.tier_final;
  rec["seconds"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  if (co.status == CalStatus::ok) {
    wp4io::CalibWrite cw; cw.mode = mode; cw.co = &co; cw.led = &oc.led; cw.inherited_flat = &oc.inherited;
    cw.settings = &s; cw.k_store = oc.k_store;
    cw.N = frozen_N(b, rule, co.tier_final); cw.L = s.tiers[co.tier_final].L; cw.Hm = s.tiers[co.tier_final].Hm; cw.stages = oc.stages;
    cw.inputs["data.bin"] = dhash; cw.inputs["setup.bin"] = S.content_hash;
    cw.extra["seed"] = (double)seed; cw.extra["threads"] = s.threads;
    rec["calib_bin"] = wp4io::write_calib(out, cw);
  }
  return rec;
}

}  // namespace v4::calib
