// main.cpp -- smcbvs4 <command> [--key value ...] | --manifest <json>   (INTERFACES §1, §5.3, §7)
// Every command writes <out>.json (record + status) and exits 0 (completed) or 10 + status.
#include <cstdio>
#include <iostream>
#include <string>
#include "v4/format.h"
#include "v4/gen.h"
#include "v4/json.h"
#include "v4/pmath.h"
#include "v4/prep.h"
#include "v4/provenance.h"
#include "v4/sha256.h"
#include "v4/status.h"
#include "v4/stubs.h"
#include "v4/threads.h"

using namespace v4;

static void usage() {
  std::fprintf(stderr,
    "usage: smcbvs4 <command> [--key value ...]   or   smcbvs4 <command> --manifest m.json\n"
    "commands: gen prep setup calibrate island merge eval post info version\n"
    "  gen   --design AR|IND|BLK|ADJ-OPP --n N --p P --seed S [--rho R --b B --a A --s0 K --sigma s] --out raw.bin [--truth truth.json]\n"
    "  gen-test  (same spec) --ntest M --cols 1,5,9 --out test.bin\n"
    "  prep  --in raw.bin --out data.bin    |   prep --from-r <dir> --out data.bin\n"
    "  info  --in file.bin                  (header, sections, verified hashes)\n"
    "  common: --threads k  --record out.json\n");
}

static Json number_or_string(const std::string& v) {
  char* e = nullptr; double d = std::strtod(v.c_str(), &e);
  if (e && *e == '\0' && !v.empty()) return Json(d);
  return Json(v);
}

int main(int argc, char** argv) {
  if (argc < 2) { usage(); return exit_code(Status::invalid_input); }
  std::string cmd = argv[1];
  Json args = Json::object();
  std::string record_path;
  Status st = Status::completed;
  Json rec = Json::object();
  // the record path first, so that a failure while reading the other arguments (e.g. a refused manifest) is recorded
  for (int i = 2; i + 1 < argc; ++i) if (std::string(argv[i]) == "--record") record_path = argv[i + 1];
  try {
    for (int i = 2; i < argc; ++i) {
      std::string k = argv[i];
      if (k.rfind("--", 0) != 0 || i + 1 >= argc) throw Error(Status::invalid_input, "bad argument " + k);
      std::string key = k.substr(2), val = argv[++i];
      for (auto& ch : key) if (ch == '-') ch = '_';
      if (key == "manifest") {
        Json m = read_json_file(val);
        for (auto& [kk, vv] : m.at("params").items()) args[kk] = vv;
        verify_inputs(m);   // INTERFACES §5.3: a job refuses to start on any input hash mismatch (invalid_input)
        args["manifest"] = m;
      }
      else if (key == "record") record_path = val;
      else args[key] = number_or_string(val);
    }
    if (args.contains("threads")) set_threads((int)args.at("threads").i64());
    if (cmd != "info" && cmd != "version") require_bit_libm();   // INTERFACES §6
    auto spec_from_args = [&]() {
      Json s = Json::object();
      for (const char* f : {"design", "n", "p", "seed", "rho", "b", "a", "s0", "sigma"}) if (args.contains(f)) s[f] = args.at(f);
      return s;
    };
    if (cmd == "version") {
      rec["program"] = "smcbvs4";
    } else if (cmd == "gen") {
      Json a = Json::object(); a["spec"] = spec_from_args(); a["out"] = args.at("out");
      if (args.contains("truth")) a["truth"] = args.at("truth");
      rec = gen::run(a);
    } else if (cmd == "gen-test") {
      Json a = Json::object(); a["spec"] = spec_from_args(); a["out"] = args.at("out"); a["ntest"] = args.at("ntest");
      Json cols = Json::array();
      std::string cs = args.at("cols").type() == Json::STR ? args.at("cols").str() : std::to_string(args.at("cols").i64());
      size_t pos = 0;
      while (pos < cs.size()) { size_t e = cs.find(',', pos); if (e == std::string::npos) e = cs.size(); cols.push(Json(std::stod(cs.substr(pos, e - pos)))); pos = e + 1; }
      a["cols"] = cols;
      rec = gen::run_test(a);
    } else if (cmd == "prep") {
      rec = prep::run(args);
    } else if (cmd == "info") {
      fmt::Reader rd(args.at("in").str());
      rec["kind"] = fmt::kind_name(rd.kind()); rec["mode"] = fmt::mode_name(rd.mode()); rec["content_sha256"] = rd.content_hash();
      Json secs = Json::array();
      for (auto& e : rd.sections()) {
        Json s = Json::object(); s["name"] = std::string(e.name); s["dtype"] = e.dtype; s["bytes"] = e.length;
        s["dims"] = Json::array(); s["dims"].push(e.dims[0]); if (e.ndim == 2) s["dims"].push(e.dims[1]);
        s["sha256"] = hex(e.sha256, 32); secs.push(s);
      }
      rec["sections"] = secs; rec["verified"] = true;
    } else if (cmd == "setup") rec = setup::run(args);
    else if (cmd == "calibrate") rec = calib::run(args);
    else if (cmd == "island") rec = island::run(args);
    else if (cmd == "merge") rec = merge::run(args);
    else if (cmd == "eval") rec = eval::run(args);
    else if (cmd == "post") rec = post::run(args);
    else { usage(); throw Error(Status::invalid_input, "unknown command " + cmd); }
    if (rec.contains("status") && rec.at("status").type() == Json::STR) st = status_from_name(rec.at("status").str());
  } catch (const Error& e) {
    st = e.st; rec = Json::object(); rec["reason"] = e.what();
  } catch (const std::bad_alloc&) {
    st = Status::resource_limit; rec = Json::object(); rec["reason"] = "out of memory";
  } catch (const std::exception& e) {
    st = Status::internal_error; rec = Json::object(); rec["reason"] = e.what();
  }
  rec["status"] = status_name(st); rec["command"] = cmd;
  try { rec["binary"] = binary_block(); } catch (...) {}
  // INTERFACES §7: prep data outcomes (no data.bin) exit 20 / 21, never 0
  int code = exit_code(st);
  if (st == Status::completed && rec.contains("prep_status")) {
    const std::string& ps = rec.at("prep_status").str();
    if (ps == "no_predictors") code = 20; else if (ps == "y_constant") code = 21;
  }
  if (record_path.empty() && args.contains("out") && args.at("out").type() == Json::STR) record_path = args.at("out").str() + ".json";
  try { if (!record_path.empty()) write_json_file(record_path, rec); } catch (...) { if (st == Status::completed) st = Status::io_error; }
  if (st != Status::completed) code = exit_code(st);
  std::cout << rec.dump(2) << std::endl;
  return code;
}
