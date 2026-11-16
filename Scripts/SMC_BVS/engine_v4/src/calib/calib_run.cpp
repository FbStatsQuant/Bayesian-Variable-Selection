// calib_run.cpp -- `smcbvs4 calibrate` (WP4; spec §1 row 3). Reads data.bin and setup.bin, builds the calibration
// ledger (tables from setup.bin's table top stores), runs calib::calibrate_with over the island runner, writes calib.bin.
// The island runner is WP3's island with calibration roles (WP3_DESIGN §1.11); until it is merged this command validates
// every input and setting, plans its memory, and then refuses with internal_error naming what is missing.
//
//   smcbvs4 calibrate --data D --setup S --seed s --mode compat|law|V --out calib.bin [--threads k] [--mem-budget BYTES]
//                     [--I_max i --refine_m m (V only)]
//   smcbvs4 calibrate --plan-only 1 --mode M (--data D | --n n --p p) [--mem-budget BYTES]   settings + memory plan, no run
#include <sys/stat.h>
#include <cmath>
#include "v4/calib_run.h"
#include "v4/format.h"
#include "v4/prep.h"
#include "v4/stubs.h"
#include "v4/wp4_io.h"

namespace v4::calib {

namespace {
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
              "resident + its plan (inputs included) <= mem_budget; refused up front iff total = resident + inputs + island_ledger > budget";
  j["kbar"] = kbar; j["kbar_source"] = k_src;
  j["ledger"] = u(m.ledger); j["island_ledger"] = u(m.island_ledger); j["export"] = u(m.export_);
  j["inputs"] = u(m.inputs); j["resident"] = u(m.resident); j["total"] = u(m.total); j["budget"] = u(budget);
  return j;
}
}  // namespace

Json run(const Json& args) {
  // mode: compat | law | V only (review PR37 m-4)
  std::string mode_s = str_arg(args, "mode");
  if (mode_s.empty() && args.contains("manifest") && args.at("manifest").type() == Json::OBJ && args.at("manifest").contains("mode")) {
    const Json& mm = args.at("manifest").at("mode");
    if (mm.type() != Json::STR) throw Error(Status::invalid_input, "calibrate: the manifest's mode must be a string");
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
  const std::string dpath = str_arg(args, "data"), spath = str_arg(args, "setup"), out = str_arg(args, "out");
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
  // memory plan (review PR37 M-5, N-2): k = max(8, q90(pi_0 size) + 1) from setup.bin (INTERFACES §7, as WP3's plan);
  // a plan from --n / --p alone has no setup and uses the floor 8 (labelled)
  wp4io::SetupView S; double kbar = 8; std::string k_src = "floor 8 (no setup.bin)";
  if (!plan_only || (!spath.empty() && !dpath.empty())) {
    if (spath.empty()) throw Error(Status::invalid_input, "calibrate: --setup is required");
    S = wp4io::read_setup(spath, D.p, D.K, &D.zob);
    if (!S.data_hash.empty() && S.data_hash != dhash) throw Error(Status::invalid_input, "calibrate: setup.bin was built from another data.bin");
    if (S.size_logmass.empty()) throw Error(Status::invalid_input, "calibrate: setup.bin has no size_logmass (INTERFACES §5; the memory plan's k)");
    kbar = calib_k_plan(S.size_logmass); k_src = "max(8, q90(pi_0 size) + 1) from setup.bin";
  }
  const CalibMemPlan plan = calib_memory_plan(p, kbar, file_bytes(dpath) + file_bytes(spath));
  Json rec = Json::object();
  rec["settings"] = settings_json(s, b, rule); rec["mem_plan"] = plan_json(plan, budget, kbar, k_src); rec["n"] = (double)n; rec["p"] = (double)p;
  rec["mode"] = mode_s;
  if (budget && plan.total > budget) {   // no island can run beside the calibration state: refuse before any allocation (N-2)
    rec["status"] = "resource_limit";
    rec["reason"] = "calibrate not admitted: calibration state + inputs + one island ledger = " + std::to_string(plan.total) + " B > --mem-budget " + std::to_string(budget) + " B";
    return rec;
  }
  if (plan_only) { rec["status"] = "completed"; rec["plan_only"] = true; return rec; }
  if (out.empty()) throw Error(Status::invalid_input, "calibrate: --out is required");
  const int64_t seed = whole_arg(args, "seed", -1, 1, 2147483647);
  if (seed < 1) throw Error(Status::invalid_input, "calibrate: --seed is required (a whole number in [1, 2^31 - 1])");
  // the island runner: WP3's island with calibration roles (PILOT / DIAG; WP3_DESIGN §1.11) -- not merged yet. When it
  // is: calibrate_with(runner, ledger, fac, s, ts, plan.resident, budget) (N-1: the whole budget, resident without inputs)
  throw Error(Status::internal_error, "calibrate: the island runner (WP3 calibration roles) is not available yet; inputs and settings validated: data " +
              dhash + ", setup " + S.content_hash + ", n = " + std::to_string(n) + ", p = " + std::to_string(p) + ", " +
              settings_json(s, b, rule).dump());
}

}  // namespace v4::calib
