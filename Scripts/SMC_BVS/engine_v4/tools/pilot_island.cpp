// pilot_island.cpp -- CLI of include/v4/island/pilot_only.h: the calibration pilot island alone on production inputs
// (WP7 O5; the H-11 10^6 calibration pilot).
//   v4_pilot_island --data D --setup S --seed s --threads k --cost-dir DIR --out summary.json
//                   [--mem-budget BYTES] [--with-ledger 0|1] [--verbose 0|1]
// Output: DIR/cost_pilot_t0_k0_r0.jsonl (D-30 per-step record, one line per step, flushed as it runs) and summary.json
// (status, schedule, forced steps, log Z, seconds, peak RSS, settings). Exit 0 iff the island completed, else 10 + status.
#include <cstdio>
#include "v4/island/pilot_only.h"

using namespace v4;

int main(int argc, char** argv) {
  Json a = Json::object();
  for (int i = 1; i + 1 < argc; i += 2) {
    std::string k = argv[i];
    if (k.rfind("--", 0) != 0) { std::fprintf(stderr, "argument %s: expected --key value\n", argv[i]); return 2; }
    k = k.substr(2); for (auto& c : k) if (c == '-') c = '_';
    a[k] = std::string(argv[i + 1]);
  }
  const std::string out = a.contains("out") ? a.at("out").str() : "";
  if (out.empty()) { std::fprintf(stderr, "usage: v4_pilot_island --data D --setup S --seed s --threads k --cost-dir DIR --out summary.json "
                                          "[--mem-budget BYTES] [--with-ledger 0|1] [--verbose 0|1]\n"); return 2; }
  Json rec; int rc = 0;
  try { rec = island::run_pilot_only(a, rc); }
  catch (const Error& e) { rec = Json::object(); rec["status"] = status_name(e.st); rec["message"] = e.what(); rc = 10 + (int)e.st; }
  catch (const std::exception& e) { rec = Json::object(); rec["status"] = "internal_error"; rec["message"] = e.what(); rc = 15; }
  try { write_json_file(out, rec); } catch (...) { std::fprintf(stderr, "cannot write %s\n", out.c_str()); return 14; }
  std::printf("%s\n", rec.dump().c_str());
  return rc;
}
