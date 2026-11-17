// plan_tables.cpp -- v4_plan_tables: the memory plans of a V fit with REAL setup tables (gate P5; the driver re-size).
// The setup's dimensions come from a WP2 setup.bin (read_setup_dims: its mapped sections) or, before a 10^6 file exists,
// from WP2's --count-only accounting JSON (dims_from_sizes: the same formula; test start_view_mapped_wp2_setup pins it).
// Every number is the plan the code admits with (ESTIMATE, bytes):
//   final island        plan_sizes + island_memory, V (class A, label-major), N = V_N, Hm, B = budgets(n, p).B, k = max(8,
//                       q90(pi_0 size) + 1, k_store), setup inputs = mapped sections + draw scratch + neighbours (StartView)
//   calibration island  the same for the largest calibration island (pilot: leaders, round-start snapshot, N = V_H), under
//                       WP4's N-1 rule: + the calibration's resident state (ledger + export, calib_memory_plan)
//   calibrate task      = the calibration island under N-1 (it already holds X, the start law and the resident state)
//                       + WP4's SetupView copy of setup.bin (read_setup: logr, table stores, ...) until PR46's reader split
//   merge task          estimate_merge_memory (WP4): R' islands' stores streamed, N terminal supports, + data.bin + 2.5 x setup.bin
//
//   v4_plan_tables --counts AR_n200.json [--q90 5] [--setup-bin-bytes B] [--island-threads 96] [--calib-threads 96]
//                  [--merge-threads 32] [--Rp 16] [--k-store k]
//   v4_plan_tables --setup setup.bin --n n --p p [same options]
//   v4_plan_tables --setup setup.bin --data data.bin --load 1 [--island-threads T]   MEASURED: map the start law as an
//                  admitted island does (data, StartView, neighbours, draw scratch for T threads) and print /proc/self/status
//                  RSS split into anonymous (heap: what the island owns) and file-backed (mapped setup.bin / data.bin pages)
// Output: one JSON object per G (64, 256) on stdout, then a Markdown table.
#include <cstdio>
#include <cstring>
#include <string>
#include "v4/calib_run.h"
#include "v4/island/island.h"
#include "v4/island/setup_load.h"
#include "v4/json.h"
#include "v4/merge.h"
#include "v4/prep.h"
#include <fstream>

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

int main(int argc, char** argv) {
  std::string counts, setup, data; int64_t n = 0, p = 0; double q90 = -1, setup_bin = -1, k_store = 0; int load = 0;
  int ti = 96, tc = 96, tm = 32, Rp = 16;
  for (int i = 1; i + 1 < argc; i += 2) {
    const std::string k = argv[i], v = argv[i + 1];
    if (k == "--counts") counts = v; else if (k == "--setup") setup = v; else if (k == "--n") n = std::stoll(v); else if (k == "--p") p = std::stoll(v);
    else if (k == "--q90") q90 = std::stod(v); else if (k == "--setup-bin-bytes") setup_bin = std::stod(v); else if (k == "--k-store") k_store = std::stod(v);
    else if (k == "--island-threads") ti = std::stoi(v); else if (k == "--calib-threads") tc = std::stoi(v); else if (k == "--merge-threads") tm = std::stoi(v);
    else if (k == "--Rp") Rp = std::stoi(v); else if (k == "--data") data = v; else if (k == "--load") load = std::stoi(v);
    else { std::fprintf(stderr, "unknown option %s\n", k.c_str()); return 2; }
  }
  if (load) {   // MEASURED load of the start law as an admitted island holds it
    if (setup.empty() || data.empty()) { std::fprintf(stderr, "--load needs --setup and --data\n"); return 2; }
    const Json before = proc_status();
    const Data D = prep::load_data(data);
    const Json after_data = proc_status();
    const SetupDims sd = read_setup_dims(setup, D.p, D.K, false);
    const StartView v = map_start_view(setup, D, false);   // no section hash pass: measure what the island keeps, not the verification
    const Neighbours nb = load_neighbours(setup, D.p);
    v.prepare(ti);
    const Json after = proc_status();
    Json o = Json::object();
    o["label"] = "MEASURED (/proc/self/status after mapping; bytes)"; o["n"] = D.n; o["p"] = D.p; o["J"] = v.J; o["max_block"] = v.max_m;
    o["view_bytes_mapped"] = (double)v.bytes(); o["planned_setup_inputs"] = start_inputs_bytes(sd, ti); o["source"] = v.source;
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
                   " thr) | calibration island, N-1 | calibrate task | merge task (" + std::to_string(tm) + " thr) | setup inputs (mapped + scratch + nb) |\n|---|---|---|---|---|---|---|---|---|\n";
  for (int G : {1, 64, 256}) {   // G = 1: the admission floor (with a budget the island takes the largest G that fits)
    IslandConfig f; f.role = IslandRole::Final; f.N = calib::V_N; f.Hm = s.tiers[0].Hm; f.B = b.B; f.kernel = KernelKind::LabelMajor; f.threads = ti; f.G = G;
    f.inputs_bytes = start_inputs_bytes(d, ti); f.k_store = k_store;
    MemSizes zf = plan_sizes((int)n, (int)p, b.K, f); const MemPlan pf = plan_with_budget(zf, k, f);
    IslandConfig c; c.role = IslandRole::Pilot; c.island = 0; c.leaders = true; c.N = s.tiers[0].H; c.Hm = s.tiers[0].Hm; c.B = b.B;
    c.kernel = KernelKind::LabelMajor; c.threads = tc; c.G = G; c.inputs_bytes = start_inputs_bytes(d, tc) + (double)resident_own;
    MemSizes zc = plan_sizes((int)n, (int)p, b.K, c); const MemPlan pc = plan_with_budget(zc, k, c);
    IslandConfig ca = c; ca.inputs_bytes = start_inputs_bytes(d, tc);   // the same island without the calibration's resident state (the pilot alone)
    MemSizes za = plan_sizes((int)n, (int)p, b.K, ca); const MemPlan pa = plan_with_budget(za, k, ca);
    const double calib_task = (double)pc.total + setup_bin;
    merge::MergeSettings ms; ms.Rp = Rp; ms.p = (int)p; ms.N = calib::V_N; ms.K = b.K; ms.threads = tm; ms.kbar = k;
    ms.extra_bytes = (uint64_t)(data_bytes + 2.5 * setup_bin);
    const merge::MemEstimate me = merge::estimate_merge_memory(ms);
    Json o = Json::object();
    o["design"] = design; o["n"] = (double)n; o["p"] = (double)p; o["G"] = G; o["k"] = k; o["B"] = b.B; o["J"] = d.J; o["max_block"] = d.max_m;
    o["setup_view_bytes"] = (double)d.view_bytes; o["setup_inputs_island"] = f.inputs_bytes; o["setup_bin_bytes"] = setup_bin;
    o["final_island"] = (double)pf.total; o["final_island_text"] = mem_plan_text(pf);
    o["calibration_island_alone"] = (double)pa.total; o["calibration_island_n1"] = (double)pc.total; o["calibration_island_text"] = mem_plan_text(pc); o["calibration_resident"] = (double)resident_own;
    o["calibrate_task"] = calib_task; o["merge_task"] = (double)me.total;
    o["label"] = "ESTIMATE (memory plans with the real setup tables' dimensions; bytes)";
    std::printf("%s\n", o.dump().c_str());
    char row[512];
    std::snprintf(row, sizeof row, "| %s | %lld | %d | %.1f GiB | %.1f GiB | %.1f GiB | %.1f GiB | %.1f GiB | %.2f GiB |\n", design.c_str(), (long long)n, G,
                  gib((double)pf.total), gib((double)pa.total), gib((double)pc.total), gib(calib_task), gib((double)me.total), gib(f.inputs_bytes));
    md += row;
  }
  std::printf("%s", md.c_str());
  return 0;
}
