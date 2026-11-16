// CLI-level tests: exit codes, records, manifest refusal, prep data outcomes, the libm guard (INTERFACES §5.3, §6, §7).
#include <sys/wait.h>
#include <cstdlib>
#include <fstream>
#include "tk.h"
#include "tutil.h"
#include "v4/format.h"
#include "v4/json.h"
#include "v4/provenance.h"
using namespace v4;

namespace {
int run(const std::string& args, const std::string& env = "") {
  std::string cmd = env + " " + V4_SMCBVS4 + " " + args + " > /dev/null 2>&1";
  int st = std::system(cmd.c_str());
  return WIFEXITED(st) ? WEXITSTATUS(st) : -1;
}
bool exists(const std::string& f) { std::ifstream i(f); return (bool)i; }
}  // namespace

TEST(cli_pipeline_exit_codes_and_records) {
  std::string raw = tmp_path("cli_raw.bin"), data = tmp_path("cli_data.bin"), man = tmp_path("cli_man.json");
  CHECK_EQ(run("gen --design AR --n 40 --p 60 --seed 3 --out " + raw), 0);
  CHECK_EQ(run("prep --in " + raw + " --out " + data), 0);
  Json rec = read_json_file(data + ".json");
  CHECK(rec.at("status").str() == "completed" && rec.at("binary").at("libm").at("fma_variant").boolean());
  fmt::Reader rd(data);
  Json meta = rd.json("meta");
  CHECK(meta.at("mode").str() == "none" && meta.contains("binary") && meta.at("inputs").contains("raw.bin"));
  // manifest: right hash runs, wrong hash refused with invalid_input (exit 13)
  Json m = Json::object(); m["schema"] = "smcbvs4.manifest/1"; m["params"] = Json::object(); m["params"]["in"] = data;
  m["inputs"] = Json::object(); m["inputs"][data] = rd.content_hash();
  write_json_file(man, m);
  CHECK_EQ(run("info --manifest " + man + " --record " + man + ".rec"), 0);
  m["inputs"][data] = std::string(64, '0'); write_json_file(man, m);
  CHECK_EQ(run("info --manifest " + man + " --record " + man + ".rec"), 13);
  CHECK(read_json_file(man + ".rec").at("status").str() == "invalid_input");
  // stubs: internal_error (exit 15)
  CHECK_EQ(run("island --record " + man + ".rec"), 15);
  // libm guard: masked FMA -> invalid_input before any work; info / version still run
  CHECK_EQ(run("gen --design AR --n 40 --p 60 --seed 3 --out " + raw + "2", "GLIBC_TUNABLES=glibc.cpu.hwcaps=-AVX2,-FMA"), 13);
  CHECK(!exists(raw + "2"));
  CHECK_EQ(run("version --record " + man + ".rec", "GLIBC_TUNABLES=glibc.cpu.hwcaps=-AVX2,-FMA"), 0);
  for (auto f : {raw, raw + ".json", data, data + ".json", man, man + ".rec", raw + "2.json"}) std::remove(f.c_str());
}
TEST(cli_prep_data_outcomes_exit_20_21) {
  // y constant -> exit 21, no data.bin, prep_status recorded; all columns constant -> exit 20
  std::string raw = tmp_path("cli_c.bin"), data = tmp_path("cli_c_data.bin");
  for (int which : {20, 21}) {
    std::vector<double> X(30 * 4), y(30, 2.0);
    for (size_t i = 0; i < X.size(); ++i) X[i] = which == 20 ? 1.0 : (double)(i % 7);
    if (which == 20) for (int i = 0; i < 30; ++i) y[(size_t)i] = i;
    fmt::Writer w(fmt::K_RAW, fmt::M_NONE); w.add("X_cm", X, 30, 4); w.add("y", y); Json mm = Json::object(); w.add_json("meta", mm);
    w.write(raw);
    CHECK_EQ(run("prep --in " + raw + " --out " + data), which);
    CHECK(!exists(data));
    Json rec = read_json_file(data + ".json");
    CHECK(rec.at("status").str() == "completed" && rec.at("prep_status").str() == (which == 20 ? "no_predictors" : "y_constant"));
    CHECK(rec.at("hpm").size() == 0);
  }
  // non-finite input -> invalid_input (exit 13)
  std::vector<double> X(30 * 2, 1.5), y(30, 1.0); X[3] = NAN; y[1] = 2;
  fmt::Writer w(fmt::K_RAW, fmt::M_NONE); w.add("X_cm", X, 30, 2); w.add("y", y); Json mm = Json::object(); w.add_json("meta", mm);
  w.write(raw);
  CHECK_EQ(run("prep --in " + raw + " --out " + data), 13);
  for (auto f : {raw, data + ".json"}) std::remove(f.c_str());
}
TEST(json_u64_guard_and_hex64) {
  CHECK_THROWS(Json((uint64_t)1 << 60));
  CHECK(Json((uint64_t)12345).i64() == 12345);
  CHECK(hex64(0x5EEDB175C0DE2026ULL) == "0x5eedb175c0de2026");
}
