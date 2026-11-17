// pilot_only.h -- the calibration pilot island alone, on a production data.bin + setup.bin (WP7 O5; WP3_ARCH_REVIEW
// §8.4, H-11 gate (2): "the 10^6 calibration pilot"). It runs exactly the first island of `smcbvs4 calibrate --mode V`:
// the same settings (calib_run.h budgets + settings_from, bounded rule, tier 0: H, Te, L, Hm), the same runner
// (island::CalibIslandRunner<ClassA>, label-major, every thread), the same IslandSpec as LedgerBackend::pilot
// (calib_backend.h: role PILOT, island 0, iteration 0, adaptive rule with floor 1/Te, resident bytes = the calibration
// ledger + export of calib_memory_plan) and the same seed. With with_ledger = 1 (default) it also builds the calibration
// ledger with the setup's table stores, as calibrate does before its pilot, so the task's memory is the real one.
// It stops after the pilot island: no local search, no diagnostic islands, no calib.bin. Test: pilot_only_equals_calibrate_pilot.
// Arguments (JSON, CLI names with '_'): data, setup, seed, threads, cost_dir, [mem_budget], [with_ledger], [verbose].
// Returns the summary record; rc = 0 iff the island completed, else 10 + status.
#pragma once
#include <sys/stat.h>
#include <chrono>
#include <cstdio>
#include <cstring>
#include <filesystem>
#include <string>
#include "v4/calib_run.h"
#include "v4/island/calib_runner.h"
#include "v4/island/setup_load.h"
#include "v4/json.h"
#include "v4/prep.h"
#include "v4/provenance.h"
#include "v4/wp4_io.h"

namespace v4::island {

namespace pilot_detail {
inline long hwm_kb() {
  FILE* f = std::fopen("/proc/self/status", "r"); if (!f) return -1;
  char ln[256]; long kb = -1;
  while (std::fgets(ln, sizeof ln, f)) if (!std::strncmp(ln, "VmHWM:", 6)) { kb = std::atol(ln + 6); break; }
  std::fclose(f); return kb;
}
inline uint64_t file_bytes(const std::string& p) { struct stat st{}; return ::stat(p.c_str(), &st) == 0 ? (uint64_t)st.st_size : 0; }

}  // namespace pilot_detail

inline Json run_pilot_only(const Json& a, int& rc_exit) {
  using namespace pilot_detail;
  auto str = [&](const char* k) { return a.contains(k) ? (a.at(k).type() == Json::STR ? a.at(k).str() : a.at(k).dump()) : std::string(); };
  auto num = [&](const char* k, long long d) { return a.contains(k) ? (a.at(k).type() == Json::STR ? std::stoll(a.at(k).str()) : (long long)a.at(k).num()) : d; };
  const std::string dpath = str("data"), spath = str("setup"), cdir = str("cost_dir");
  const long long seed = num("seed", 0), threads = num("threads", 1), budget = num("mem_budget", 0);
  const bool with_ledger = num("with_ledger", 1) == 1, verbose = num("verbose", 0) == 1;
  rc_exit = 0;
  if (dpath.empty() || spath.empty() || cdir.empty() || seed < 1 || seed > 2147483647LL || threads < 1)
    throw Error(Status::invalid_input, "pilot: --data, --setup, --seed (1..2^31-1), --threads and --cost-dir are required");
  Json rec = Json::object();
  rec["tool"] = "v4_pilot_island"; rec["binary"] = binary_block();
  try {
    auto t0 = std::chrono::steady_clock::now();
    std::string dhash;
    Data D = prep::load_data(dpath, &dhash);
    // calib_run.cpp (calibrate --mode V), verbatim in what the pilot island sees
    const calib::Budgets b = calib::budgets(D.n, D.p);
    calib::Settings s = calib::settings_from(b, calib::Rule::bounded);
    s.threads = (int)threads;
    wp4io::SetupView S = wp4io::read_setup(spath, D.p, D.K, &D.zob);
    if (!S.data_hash.empty() && S.data_hash != dhash) throw Error(Status::invalid_input, "setup.bin was built from another data.bin");
    const double kbar = std::max(8.0, (double)S.mode_S.size() + 1);
    const calib::CalibMemPlan plan = calib::calib_memory_plan(D.p, kbar, file_bytes(dpath) + file_bytes(spath));
    const island::Start st = island::load_start(spath, D);
    const island::Neighbours nb = island::load_neighbours(spath, D.p);
    std::error_code ec; std::filesystem::create_directories(cdir, ec);
    if (ec) throw Error(Status::io_error, "cannot create --cost-dir " + cdir);
    island::CalibRunnerConfig rc; rc.seed = (uint32_t)seed; rc.B = b.B; rc.threads = s.threads;
    rc.inputs_bytes = island::start_bytes(st, nb); rc.kernel = island::KernelKind::LabelMajor;
    rc.cost_dir = cdir; rc.verbose = verbose;
    LedgerConfig lc; lc.p = D.p; lc.islands = 4; lc.leaders = true; lc.fresh_counters = false;
    Ledger led(lc);
    if (with_ledger) wp4io::offer_tables(led, S, D.K, D.zob);   // calibrate's ledger before its pilot (core v3_core.cpp:613)
    const double t_setup = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    const calib::TierSettings& cs = s.tiers[0];
    calib::IslandSpec sp; sp.role = calib::IslandRole::Pilot; sp.tier = cs.tier; sp.iter = 0; sp.island = 0; sp.H = cs.H;
    sp.adaptive = true; sp.Te = cs.Te; sp.L = cs.L; sp.Hm = cs.Hm;
    sp.resident_bytes = plan.ledger + plan.export_; sp.mem_budget = (uint64_t)budget;   // as calibrate (N-1 rule)
    island::CalibIslandRunner<island::Arith::ClassA> runner(D, st, nb, rc);
    auto t1 = std::chrono::steady_clock::now();
    calib::IslandOut io = runner.run(sp);
    const double t_island = std::chrono::duration<double>(std::chrono::steady_clock::now() - t1).count();
    rec["status"] = status_name(io.status); rec["message"] = io.message; rec["partial"] = io.partial;
    rec["T"] = (int64_t)io.schedule.size(); rec["forced"] = io.forced; rec["logZ"] = io.logZ;
    rec["schedule"] = Json::array_of(io.schedule);
    rec["seconds_inputs"] = t_setup; rec["seconds_island"] = t_island; rec["peak_rss_gb"] = hwm_kb() / 1048576.0;
    Json set = Json::object(); set["n"] = D.n; set["p"] = D.p; set["H"] = cs.H; set["Te"] = cs.Te; set["L"] = cs.L; set["Hm"] = cs.Hm;
    set["B"] = b.B; set["threads"] = s.threads; set["mem_budget"] = (double)budget; set["with_ledger"] = with_ledger;
    set["plan_resident_bytes"] = (double)sp.resident_bytes; set["inputs_bytes"] = rc.inputs_bytes;
    rec["settings"] = set;
    rec["cost_record"] = island::calib_cost_path(cdir, true, cs.tier, 0, 0);
    Json in = Json::object(); in["data.bin"] = dhash; in["setup.bin"] = S.content_hash; rec["inputs"] = in;
    if (io.status != Status::completed) rc_exit = 10 + (int)io.status;
  } catch (const Error& e) {
    rec["status"] = status_name(e.st); rec["message"] = e.what(); rc_exit = 10 + (int)e.st;
  } catch (const std::exception& e) {
    rec["status"] = "internal_error"; rec["message"] = e.what(); rc_exit = 15;
  }
  return rec;
}

}  // namespace v4::island
