// plan_tables.cpp -- v4_plan_tables: the memory plans of a V fit with REAL setup tables (gate P5; the driver re-size).
// The setup's dimensions come from a WP2 setup.bin (read_setup_dims: its mapped sections) or, before a 10^6 file exists,
// from WP2's --count-only accounting JSON (dims_from_sizes: the same formula; test start_view_mapped_wp2_setup pins it).
// Every number is the plan the code admits with (ESTIMATE, bytes):
//   final island        plan_sizes + island_memory, V (class A, label-major), N = V_N (--N), Hm, B = budgets(n, p).B, k = max(8,
//                       q90(pi_0 size) + 1, k_store), setup inputs = mapped sections + draw scratch + neighbours (StartView)
//   calibration island  the same for the largest calibration island (pilot: leaders, round-start snapshot, N = V_H), under
//                       WP4's N-1 rule: + the calibration's resident state (ledger + export, calib_memory_plan)
//   calibrate task      = the calibration island under N-1 (it already holds X, the start law and the resident state)
//                       + WP4's SetupView copy of setup.bin (read_setup: logr, table stores, ...) until PR46's reader split
//   merge task          estimate_merge_memory (WP4): R' islands' stores streamed, N terminal supports, + data.bin + 2.5 x setup.bin
//
//   v4_plan_tables --counts AR_n200.json [--q90 5] [--setup-bin-bytes B] [--island-threads 96] [--calib-threads 96]
//                  [--merge-threads 32] [--Rp 16] [--k-store k] [--N 2500]
//   v4_plan_tables --setup setup.bin --n n --p p [same options]
//   v4_plan_tables --setup setup.bin --data data.bin --load 1 [--island-threads T]   MEASURED: map the start law as an
//                  admitted island does (data, StartView, neighbours, draw scratch for T threads) and print /proc/self/status
//                  RSS split into anonymous (heap: what the island owns) and file-backed (mapped setup.bin / data.bin pages)
// Output: one JSON object per G (64, 256) on stdout, then a Markdown table.
#include <cerrno>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include "v4/calib_plan.h"
#include "v4/calib_run.h"
#include "v4/island/island.h"
#include "v4/island/setup_load.h"
#include "v4/json.h"
#include "v4/merge.h"
#include "v4/prep.h"
#include "v4/wp4_io.h"
#include <malloc.h>
#include <fstream>
#include <omp.h>

using namespace v4;
using namespace v4::island;

static double gib(double b) { return b / 1073741824.0; }

static Json proc_status() {   // VmRSS, VmHWM, RssAnon, RssFile (kB -> bytes)
  Json j = Json::object(); std::ifstream f("/proc/self/status"); std::string line;
  while (std::getline(f, line))
    for (const char* k : {"VmRSS", "VmHWM", "RssAnon", "RssFile"})
      if (line.rfind(std::string(k) + ":", 0) == 0) j[k] = 1024.0 * std::stod(line.substr(std::strlen(k) + 1));
  return j;
}

// --N: the engine's rule (calib_run.cpp whole_arg): a whole number in [V_N_MIN, V_N_MAX]; "2.5", "1e4"-style fractions, "abc", "" and a trailing junk are refused
static bool whole_n(const std::string& s, int& out) {
  if (s.empty()) return false;
  char* end = nullptr; errno = 0;
  const double x = std::strtod(s.c_str(), &end);
  if (errno || end != s.c_str() + s.size() || !std::isfinite(x) || x != std::floor(x) || x < (double)calib::V_N_MIN || x > (double)calib::V_N_MAX) return false;
  out = (int)x; return true;
}

int main(int argc, char** argv) {
  std::string counts, setup, data; int64_t n = 0, p = 0; double q90 = -1, setup_bin = -1, k_store = 0; int load = 0;
  int ti = 96, tc = 96, tm = 32, Rp = 16, vN = calib::V_N;   // vN: the V final islands' N (--N; default V_N = 2,500)
  for (int i = 1; i + 1 < argc; i += 2) {
    const std::string k = argv[i], v = argv[i + 1];
    if (k == "--counts") counts = v; else if (k == "--setup") setup = v; else if (k == "--n") n = std::stoll(v); else if (k == "--p") p = std::stoll(v);
    else if (k == "--q90") q90 = std::stod(v); else if (k == "--setup-bin-bytes") setup_bin = std::stod(v); else if (k == "--k-store") k_store = std::stod(v);
    else if (k == "--island-threads") ti = std::stoi(v); else if (k == "--calib-threads") tc = std::stoi(v); else if (k == "--merge-threads") tm = std::stoi(v);
    else if (k == "--Rp") Rp = std::stoi(v); else if (k == "--N") { if (!whole_n(v, vN)) { std::fprintf(stderr, "--N must be a whole number in [%d, %d] (as the engine's calibrate / island N)\n", calib::V_N_MIN, calib::V_N_MAX); return 2; } } else if (k == "--data") data = v; else if (k == "--load") load = std::stoi(v);
    else { std::fprintf(stderr, "unknown option %s\n", k.c_str()); return 2; }
  }
  if (load) {   // MEASURED load of the start law as an admitted island holds it
    if (setup.empty() || data.empty()) { std::fprintf(stderr, "--load needs --setup and --data\n"); return 2; }
    if (load == 3) {   // MEASURED: WP4's SetupView (read_setup) held beside the island, before and after the table stores are released
      const Data D = prep::load_data(data);
      const SetupDims sd = read_setup_dims(setup, D.p, D.K, false);
      const Json b0 = proc_status();
      wp4io::SetupView S = wp4io::read_setup(setup, D.p, D.K, &D.zob);
      const Json b1 = proc_status();
      calib::release_table_stores(S); malloc_trim(0);
      const Json b2 = proc_status();
      S = wp4io::SetupView(); malloc_trim(0);   // everything freed: what the allocator still holds is retention, not live data
      const Json b3 = proc_status();
      Json o = Json::object();
      o["label"] = "MEASURED (RssAnon, bytes): WP4's SetupView after read_setup, and after the table stores are released";
      o["p"] = D.p; o["logr_bytes"] = 8.0 * (double)sd.logr_len; o["setup_view_bytes_counted"] = setup_view_bytes(sd);
      o["anon_with_table_stores"] = b1.at("RssAnon").num() - b0.at("RssAnon").num();
      o["anon_after_release"] = b2.at("RssAnon").num() - b0.at("RssAnon").num();
      o["anon_after_free_all"] = b3.at("RssAnon").num() - b0.at("RssAnon").num();   // allocator retention after everything is freed
      std::printf("%s\n", o.dump(1).c_str());
      return 0;
    }
    const Json before = proc_status();
    const Data D = prep::load_data(data);
    const Json after_data = proc_status();
    const SetupDims sd = read_setup_dims(setup, D.p, D.K, false);
    const double tm0 = omp_get_wtime();
    const StartView v = map_start_view(setup, D, false);   // no section hash pass: measure what the island keeps, not the verification
    const double t_map = omp_get_wtime() - tm0;             // shapes + value checks (size law, cond0 rebuilt row by row)
    const Neighbours nb = load_neighbours(setup, D.p);
    v.prepare(ti);
    const Json after = proc_status();
    Json o = Json::object();
    o["label"] = "MEASURED (/proc/self/status after mapping; bytes)"; o["n"] = D.n; o["p"] = D.p; o["J"] = v.J; o["max_block"] = v.max_m;
    o["seconds_map_and_value_checks"] = t_map; o["view_bytes_mapped"] = (double)v.bytes(); o["planned_setup_inputs"] = start_inputs_bytes(sd, ti); o["source"] = v.source;
    o["before"] = before; o["after_data"] = after_data; o["after_start_view"] = after;
    o["anon_added_by_start_view"] = after.at("RssAnon").num() - after_data.at("RssAnon").num();
    if (load == 2) {   // the pre-StartView form, for comparison: the expanded dep::Start rebuilt from logr
      const dep::Start st = load_start(setup, D);
      const Json after_dep = proc_status();
      o["after_dep_start"] = after_dep; o["anon_added_by_dep_start"] = after_dep.at("RssAnon").num() - after.at("RssAnon").num();
      o["dep_start_bytes_counted"] = start_bytes(st, nb);
    }
    std::printf("%s\n", o.dump(1).c_str());
    return 0;
  }
  SetupDims d; std::string design = "setup.bin";
  if (!counts.empty()) {
    const Json J = read_json_file(counts); const Json& a = J.at("accounting");
    n = a.at("n").i64(); p = a.at("p").i64(); design = J.contains("design") ? J.at("design").str() : "?";
    std::vector<uint64_t> hist(21, 0);
    for (auto& [m, c] : a.at("block_histogram").items()) hist[(size_t)std::stoi(m)] = (uint64_t)c.num();
    uint64_t nb_bytes = 0;
    for (const auto& it : a.at("items").elems()) if (it.at("name").str().rfind("neighbours CSR", 0) == 0) nb_bytes = (uint64_t)it.at("bytes").num();
    d = dims_from_sizes(p, (int)a.at("K").i64(), hist, nb_bytes > 8 * ((uint64_t)p + 1) ? (nb_bytes - 8 * ((uint64_t)p + 1)) / 4 : 0);
    { uint64_t C = 0; for (int m = 1; m <= 20; ++m) C += hist[(size_t)m] << m;   // the table codes, re-derived from the histogram
      if (C != (uint64_t)a.at("C").num()) std::fprintf(stderr, "warning: C = %llu from the histogram, %.0f in the accounting\n", (unsigned long long)C, a.at("C").num()); }
    if (setup_bin < 0) setup_bin = a.at("setup_bin_estimate_bytes").num();
  } else if (!setup.empty()) {
    if (n < 3 || p < 1) { std::fprintf(stderr, "--setup needs --n and --p\n"); return 2; }
    d = read_setup_dims(setup, p, (int)calib::budgets(n, p).K, false);
    if (q90 < 0) q90 = pi0_size_q90(d.size_logmass);
    if (setup_bin < 0) setup_bin = (double)d.file_bytes;
  } else { std::fprintf(stderr, "give --counts or --setup\n"); return 2; }
  const calib::Budgets b = calib::budgets(n, p);
  const calib::Settings s = calib::settings_from(b, calib::Rule::bounded);
  const double k = std::max({8.0, (q90 >= 0 ? q90 : 0) + 1.0, k_store});
  // calibration resident state (WP4 N-1): ledger + export at the plan's k (calibrate: kbar = max(8, ...))
  const calib::CalibMemPlan cm = calib::calib_memory_plan(p, k, 0);
  const uint64_t resident_own = cm.ledger + cm.export_;
  const double data_bytes = (double)n * p * 8 + 64.0 * p;   // data.bin: X + the per-column arrays (mapped by merge / calibrate)
  Json all = Json::array();
  std::string md = "| design | n | G | final island (" + std::to_string(ti) + " thr) | calibration island alone (" + std::to_string(tc) +
                   " thr) | calibration island, N-1 | calibrate task (anonymous = N-1) | + reclaimable file pages | merge task (" + std::to_string(tm) +
                   " thr) | setup inputs (mapped + scratch + nb) | WP4 setup copy |\n|---|---|---|---|---|---|---|---|---|---|---|\n";
  for (int G : {1, 64, 256}) {   // G = 1: the admission floor (with a budget the island takes the largest G that fits)
    IslandConfig f; f.role = IslandRole::Final; f.N = vN; f.Hm = s.tiers[0].Hm; f.B = b.B; f.kernel = KernelKind::LabelMajor; f.threads = ti; f.G = G;
    f.inputs_bytes = start_inputs_bytes(d, ti); f.k_store = k_store;
    MemSizes zf = plan_sizes((int)n, (int)p, b.K, f); const MemPlan pf = plan_with_budget(zf, k, f);
    // the calibration island under N-1: calibrate's own plan function (calib_plan.h), so the numbers are what its admission uses
    calib::Settings sc = s; sc.threads = tc;
    const calib::IslandPlans ipl = calib::calib_island_plans(sc, calib::Rule::bounded, fmt::M_V, b.B, b.K, n, p, 0, resident_own, &d, k, G);
    const MemPlan& pc = ipl.ip;
    IslandConfig ca; ca.role = IslandRole::Pilot; ca.island = 0; ca.leaders = true; ca.N = s.tiers[0].H; ca.Hm = s.tiers[0].Hm; ca.B = b.B;
    ca.kernel = KernelKind::LabelMajor; ca.threads = tc; ca.G = G; ca.inputs_bytes = start_inputs_bytes(d, tc);   // the pilot alone: no ledger, no setup copy
    MemSizes za = plan_sizes((int)n, (int)p, b.K, ca); const MemPlan pa = plan_with_budget(za, k, ca);
    const double calib_task = (double)pc.total;                                          // anonymous memory the task must hold
    const double file_pages = std::max(0.0, setup_bin - (double)d.view_bytes);            // the rest of setup.bin, paged in once by the hash check
    merge::MergeSettings ms; ms.Rp = Rp; ms.p = (int)p; ms.N = vN; ms.K = b.K; ms.threads = tm; ms.kbar = k;
    ms.extra_bytes = (uint64_t)(data_bytes + 2.5 * setup_bin);
    const merge::MemEstimate me = merge::estimate_merge_memory(ms);
    Json o = Json::object();
    o["design"] = design; o["n"] = (double)n; o["p"] = (double)p; o["G"] = G; o["k"] = k; o["B"] = b.B; o["J"] = d.J; o["max_block"] = d.max_m;
    o["setup_view_bytes"] = (double)d.view_bytes; o["setup_inputs_island"] = f.inputs_bytes; o["setup_copy_wp4"] = ipl.setup_copy; o["setup_bin_bytes"] = setup_bin;
    o["final_island"] = (double)pf.total; o["final_island_text"] = mem_plan_text(pf);
    o["calibration_island_alone"] = (double)pa.total; o["calibration_island_n1"] = (double)pc.total; o["calibration_island_text"] = mem_plan_text(pc); o["calibration_resident"] = (double)resident_own;
    o["calibrate_task"] = calib_task; o["calibrate_file_pages"] = file_pages; o["merge_task"] = (double)me.total;
    o["label"] = "ESTIMATE (memory plans with the real setup tables' dimensions; bytes)";
    std::printf("%s\n", o.dump().c_str());
    char row[640];
    std::snprintf(row, sizeof row, "| %s | %lld | %d | %.1f GiB | %.1f GiB | %.1f GiB | %.1f GiB | %.1f GiB | %.1f GiB | %.2f GiB | %.2f GiB |\n", design.c_str(), (long long)n, G,
                  gib((double)pf.total), gib((double)pa.total), gib((double)pc.total), gib(calib_task), gib(file_pages), gib((double)me.total), gib(f.inputs_bytes), gib(ipl.setup_copy));
    md += row;
  }
  std::printf("%s", md.c_str());
  return 0;
}
