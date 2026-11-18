// smcbvs4_xeval -- EVAL-ONLY executable: V-vs-T cross predictive Hellinger of two law.bin files (xeval.h).
// A separate binary from smcbvs4 (the fit binary is untouched). Same argument style (--key value), same record/exit rules
// as smcbvs4 (writes <out> as JSON, exit 0 completed else 10 + status), same bit-libm guard.
#include <iostream>
#include <string>

#include "v4/json.h"
#include "v4/provenance.h"
#include "v4/status.h"
#include "v4/threads.h"
#include "xeval/xeval.h"

using namespace v4;

static Json number_or_string(const std::string& v) {
  char* e = nullptr; double d = std::strtod(v.c_str(), &e);
  if (e && *e == '\0' && !v.empty()) return Json(d);
  return Json(v);
}

int main(int argc, char** argv) {
  if (argc < 2 || std::string(argv[1]) != "cross") {
    std::fprintf(stderr,
      "usage: smcbvs4_xeval cross --a law_V.bin (--b law_T.bin | --b-truth 1) --truth truth.json --out cross.json\n"
      "         [--data data.bin] [--dataset ID --seed-id 1|2] [--seed s] [--threads k] [--n-x 4000] [--n-gh 64]\n"
      "         [--top-k 1000 --tail-r 1000 --tail-groups 8 --block-rows 500]\n"
      "       smcbvs4_xeval version\n");
    return argc >= 2 && std::string(argv[1]) == "version" ? 0 : exit_code(Status::invalid_input);
  }
  Json args = Json::object(), rec = Json::object();
  Status st = Status::completed;
  std::string out;
  try {
    for (int i = 2; i < argc; ++i) {
      std::string k = argv[i];
      if (k.rfind("--", 0) != 0 || i + 1 >= argc) throw Error(Status::invalid_input, "bad argument " + k);
      std::string key = k.substr(2), val = argv[++i];
      for (auto& ch : key) if (ch == '-') ch = '_';
      args[key] = number_or_string(val);
      if (key == "out") out = val;
    }
    if (args.contains("threads")) set_threads((int)args.at("threads").i64());
    require_bit_libm();   // INTERFACES §6: the same libm bits as every engine command
    rec = xeval::run(args);
  } catch (const Error& e) { st = e.st; rec = Json::object(); rec["reason"] = e.what();
  } catch (const std::bad_alloc&) { st = Status::resource_limit; rec = Json::object(); rec["reason"] = "out of memory";
  } catch (const std::exception& e) { st = Status::internal_error; rec = Json::object(); rec["reason"] = e.what(); }
  rec["status"] = status_name(st); rec["command"] = "xeval";
  try { rec["binary"] = binary_block(); } catch (...) {}
  try { if (!out.empty()) write_json_file(out, rec); } catch (...) { if (st == Status::completed) st = Status::io_error; }
  std::cout << rec.dump(2) << std::endl;
  return exit_code(st);
}
