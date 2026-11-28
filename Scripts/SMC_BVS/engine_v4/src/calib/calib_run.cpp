// calib_run.cpp -- `smcbvs4 calibrate` (WP4; spec §1 row 3). Reads data.bin and setup.bin, builds the calibration
// ledger (tables from setup.bin's table top stores), runs calib::calibrate_with over the island runner, writes calib.bin.
// The island runner is WP3's island with calibration roles (WP3_DESIGN §1.11; island::CalibIslandRunner); the start law
// and the neighbour lists come from setup.bin (island/setup_load.h).
//
//   smcbvs4 calibrate --data D --setup S --seed s --mode compat|law|V --out calib.bin [--threads k] [--mem-budget BYTES]
//                     [--I_max i --refine_m m (V only)]
//                     [--cost-dir DIR (D-30: one JSON-lines cost record per calibration island)] [--verbose 1]
//   smcbvs4 calibrate --plan-only 1 --mode M (--data D | --n n --p p) [--mem-budget BYTES]   settings + memory plan, no run
#include <sys/stat.h>
#include <chrono>
#include <filesystem>
#include <cmath>
#include "v4/calib_plan.h"
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
Json plan_json(const CalibMemPlan& m, uint64_t budget, double kbar, const std::string& k_src) {
  Json j = Json::object();
  auto u = [](uint64_t x) { return Json((double)x); };
  j["label"] = "ESTIMATE (calibration memory plan: 3 calibration stores + flat V / export = resident; inputs; one island ledger)";
  j["rule"] = "islands get mem_budget = the whole budget and resident_bytes = resident; an island is admitted iff "
              "resident + its plan (inputs included) <= mem_budget; refused up front iff resident >= budget or the island plan (island_plan) "
              "exceeds it; total = resident + inputs + one island ledger is the least any island needs (a lower bound)";
  j["kbar"] = kbar; j["kbar_source"] = k_src;
  j["ledger"] = u(m.ledger); j["island_ledger"] = u(m.island_ledger); j["export"] = u(m.export_);
  j["inputs"] = u(m.inputs); j["resident"] = u(m.resident); j["total"] = u(m.total); j["budget"] = u(budget);
  return j;
}
Json island_plan_json(const island::MemPlan& mp, uint64_t floor, uint64_t budget, double setup_inputs, double setup_copy, uint64_t resident_own, bool from_files) {
  Json j = Json::object();
  auto u = [](uint64_t x) { return Json((double)x); };
  j["label"] = from_files ? "ESTIMATE (calibration island plan, memory.h, real setup; = the task's predicted peak under N-1: the island's own setup inputs "
                            "(mapped sections + scratch + neighbours), WP4's live setup copy (logr + partition), the calibration's ledger + export; "
                            "the file's other pages touched by the section hash check are reclaimable page cache, not counted)"
                          : "ESTIMATE (calibration island plan from sizes: k = kbar, setup inputs and the setup copy NOT counted)";
  Json it = Json::object(); for (const auto& x : mp.items) it[x.name] = u(x.bytes);
  j["items"] = it; j["G"] = mp.G; j["k"] = mp.k; j["setup_inputs"] = setup_inputs; j["setup_copy"] = setup_copy; j["resident"] = u(resident_own);
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
  // Admission first (review PR46 MAJOR-2; INTERFACES §7 "before any allocation"): n, p, K from data.bin's meta
  // (read_data_plan) and the setup's dimensions (WP3's read_setup_dims: the section table, blk_ptr, the neighbour lengths
  // and the pi_0 size law; no table, partition array or store is read or copied). data.bin and setup.bin are loaded in
  // full only after the plan is admitted.
  const std::string dpath = cmd::input_path(args, man, "data", "data.bin", "calibrate", false),
                    spath = cmd::input_path(args, man, "setup", "setup.bin", "calibrate", false), out = str_arg(args, "out");
  wp4io::DataPlanHead dh; int64_t n = 0, p = 0; int K = 0;
  if (!dpath.empty()) { dh = wp4io::read_data_plan(dpath); n = dh.n; p = dh.p; K = dh.K; }
  else if (plan_only) { n = whole_arg(args, "n", 0, 3, (int64_t)1 << 31); p = whole_arg(args, "p", 0, 1, (int64_t)1 << 31); }
  if (n < 3 || p < 1) throw Error(Status::invalid_input, "calibrate: --data is required (or --n and --p with --plan-only)");
  const Budgets b = budgets(n, p);
  Settings s = settings_from(b, rule);
  if (rule == Rule::bounded) {
    s.I_max = (int)whole_arg(args, "I_max", 3, 0, 1000); s.refine_m = (int)whole_arg(args, "refine_m", 1, 1, 64);
  }
  s.threads = threads;
  Driver::validate(s);   // e.g. I_max > ell -> invalid_input, before anything runs (review PR37 m-4)
  // memory plan (review PR37 M-5, N-2): k = max(8, q90(pi_0 size) + 1) from setup.bin (INTERFACES §7, as WP3's plan);
  // a plan from --n / --p alone has no setup and uses the floor 8 (labelled)
  island::SetupDims sdims; double kbar = 8; std::string k_src = "floor 8 (no setup.bin)";
  if (!plan_only || (!spath.empty() && !dpath.empty())) {
    if (spath.empty()) throw Error(Status::invalid_input, "calibrate: --setup is required");
    sdims = island::read_setup_dims(spath, p, K, false);
    if (!sdims.data_hash.empty() && sdims.data_hash != dh.content_hash) throw Error(Status::invalid_input, "calibrate: setup.bin was built from another data.bin");
    wp4io::check_size_logmass(sdims.size_logmass, K, spath + ": ");
    kbar = calib_k_plan(sdims.size_logmass); k_src = "max(8, q90(pi_0 size) + 1) from setup.bin";
  }
  const CalibMemPlan plan = calib_memory_plan(p, kbar, file_bytes(dpath) + file_bytes(spath));
  Json rec = Json::object();
  rec["settings"] = settings_json(s, b, rule); rec["mem_plan"] = plan_json(plan, budget, kbar, k_src); rec["n"] = (double)n; rec["p"] = (double)p;
  rec["mode"] = mode_s;
  const uint64_t resident_own = plan.ledger + plan.export_;
  const bool files = !dpath.empty() && !spath.empty();
  // the island plan from the dimensions (nothing of the setup expanded): printed on every plan-only outcome, admitted or not
  // (review PR52 m5), and the run's up-front refusal below
  const IslandPlans ipl = calib_island_plans(s, rule, mode, b.B, b.K, n, p, budget, resident_own, files ? &sdims : nullptr, kbar);
  const bool resident_ok = !(budget && plan.resident >= budget), island_ok = !(budget && ipl.ip.total > budget);
  if (plan_only) {
    rec["island_plan"] = island_plan_json(ipl.ip, ipl.ip1.total, budget, ipl.setup_in, ipl.setup_copy, resident_own, files);
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
    rec["island_plan"] = island_plan_json(ipl.ip, ipl.ip1.total, budget, ipl.setup_in, ipl.setup_copy, resident_own, files);
    rec["status"] = "resource_limit";
    rec["reason"] = "calibration island not admitted (N-1): resident + island plan " + std::to_string(ipl.ip.total) + " B > --mem-budget";
    return rec;
  }
  if (out.empty()) throw Error(Status::invalid_input, "calibrate: --out is required");
  const int64_t seed = whole_arg(args, "seed", -1, 1, 2147483647);
  if (seed < 1) throw Error(Status::invalid_input, "calibrate: --seed is required (a whole number in [1, 2^31 - 1])");
  // admitted: the full loads (every section verified); the files must be the ones the plan read
  std::string dhash;
  const Data D = prep::load_data(dpath, &dhash);
  if (dhash != dh.content_hash) throw Error(Status::invalid_input, "calibrate: data.bin changed between the plan and the load");
  wp4io::SetupView S = wp4io::read_setup(spath, D.p, D.K, &D.zob);
  if (S.content_hash != sdims.content_hash) throw Error(Status::invalid_input, "calibrate: setup.bin changed between the plan and the load");
  // the island runner: WP3's island with calibration roles (PILOT / DIAG; WP3_DESIGN §1.11). Theory modes (compat, law)
  // run the bit form particle-major (D-21; compat: 1 thread, v3 streams 0-9 owned by the runner); V runs class A
  // label-major with every thread.
  const island::StartView st = island::load_start_view(spath, D, sdims.mappable, sdims.content_hash);   // mapped: the start law is not expanded
  const island::Neighbours nb = island::load_neighbours(spath, D.p, !sdims.mappable, sdims.content_hash);   // the mapped loader verified the sections
  island::CalibRunnerConfig rc; rc.seed = (uint32_t)seed; rc.B = b.B; rc.threads = s.threads;
  rc.cost_dir = str_arg(args, "cost_dir"); rc.verbose = whole_arg(args, "verbose", 0, 0, 1) == 1;   // execution records only (WP7 O5)
  if (!rc.cost_dir.empty()) { std::error_code ec; std::filesystem::create_directories(rc.cost_dir, ec);
    if (ec) throw Error(Status::io_error, "calibrate: cannot create --cost-dir " + rc.cost_dir + ": " + ec.message()); }
  rc.inputs_bytes = ipl.setup_in + ipl.setup_copy;   // the island's own setup inputs + WP4's live setup copy: the plan above
  if (mode == fmt::M_COMPAT) { rc.compat = true; rc.kernel = island::KernelKind::ParticleMajor; rc.threads = 1; }
  else if (mode == fmt::M_LAW) rc.kernel = island::KernelKind::ParticleMajor;
  else rc.kernel = island::KernelKind::LabelMajor;
  LedgerConfig lc; lc.p = D.p; lc.islands = 4; lc.leaders = true; lc.fresh_counters = false;
  Ledger led(lc);
  wp4io::offer_tables(led, S, D.K, D.zob);   // the calibration ledger starts with the tables (core v3_core.cpp:613)
  release_table_stores(S);                    // in the ledger now; what stays live is what the plan counts (setup_view_bytes)
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
