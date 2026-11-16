// calib_run.cpp -- `smcbvs4 calibrate` (WP4; spec §1 row 3). Reads data.bin and setup.bin, builds the calibration
// ledger (tables from setup.bin's table top stores), runs calib::calibrate_with over the island runner, writes calib.bin.
// The island runner is WP3's island with calibration roles (WP3_DESIGN §1.11); until it is merged this command refuses
// with internal_error after validating its inputs, so the job record says exactly what is missing.
#include "v4/calib_run.h"
#include "v4/prep.h"
#include "v4/stubs.h"
#include "v4/wp4_io.h"

namespace v4::calib {

namespace {
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
  // the island runner: WP3's island with calibration roles (PILOT / DIAG; WP3_DESIGN §1.11) -- not merged yet
  throw Error(Status::internal_error, "calibrate: the island runner (WP3 calibration roles) is not available yet; inputs validated: data " +
              dhash + ", setup " + S.content_hash + ", n = " + std::to_string(D.n) + ", p = " + std::to_string(D.p) + ", rule " +
              (rule == Rule::coded ? "coded" : "bounded") + " (I_max " + std::to_string(s.I_max) + ", refine_m " + std::to_string(s.refine_m) +
              ", tier-0 H " + std::to_string(s.tiers[0].H) + ", T_e " + std::to_string(s.tiers[0].Te) + ", ell " + std::to_string(s.tiers[0].ell) + ")");
}

}  // namespace v4::calib
