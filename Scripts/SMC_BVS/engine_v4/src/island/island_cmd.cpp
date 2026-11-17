// island_cmd.cpp -- `smcbvs4 island` (WP3; INTERFACES §1, §5.1, §5.3, §7; WP3_DESIGN §1.13): one FINAL island r of a
// fit. Reads data.bin, setup.bin and calib.bin, runs run_island with calib.bin's frozen grid, N, L, Hm and tier, and
// writes island_r.bin (island_file.h) with meta.inputs = the three content hashes (what WP4's merge checks).
//
//   Driver form:   smcbvs4 island --manifest island_r.json --out island_r.bin [--threads k] [--mem-budget BYTES]
//                  inputs by base name (data.bin, setup.bin, calib.bin) among the manifest's `inputs`; mode = the
//                  manifest's mode; r = params.id (the driver's key) or params.island (INTERFACES §5.3); seed =
//                  params.seed. The manifest is the authority: an explicit argument that disagrees is refused.
//   Explicit form: smcbvs4 island --data D --setup S --calib C --island r --seed s --mode compat|law|V --out island_r.bin
//                  [--Rp R] [--threads k] [--mem-budget BYTES | --mem-budget-gb G] [--G g] [--tile t]
//                  [--ckpt 0|1] [--ckpt-every-s s]
//   Plan only:     the same with --plan-only 1 (no --out needed): the island's admission plan (memory.h), no run.
//                  Without files: --plan-only 1 --mode M --n n --p p [--N N --threads k --G g --k k --inputs-bytes b]
//                  (ESTIMATE: k given, setup inputs given or 0).
//
// Roles: the command runs final islands only (role `final`). Pilot and diagnostic islands run inside `calibrate`, which
// owns their streams and ledgers (WP3_DESIGN §1.11).
// Kernels (D-21): compat = bit form, particle-major, 1 thread, v3 stream 9 + r; law = bit form, particle-major; V = class A,
// label-major. Memory (INTERFACES §7): --mem-budget is the whole task's memory; the island plan counts X, z, diag(G),
// the stores, ... and, as its caller-supplied term, the setup inputs (today's dep::Start + neighbour lists: start_bytes).
// k = max(8, q90(pi_0 size) + 1, calib.bin k_store). Over budget: resource_limit before the run, island_r.bin written
// with that status (no estimate section, GUARD-W), exit 11.
// Checkpoints: <out without .bin>.ckpt.{a,b} (INTERFACES §5.1), every --ckpt-every-s seconds (default 600); a restart of
// the same command resumes from the newest valid one; removed once island_r.bin is written as completed.
#include <sys/stat.h>
#include <chrono>
#include <cmath>
#include <cstdio>
#include "v4/island/island.h"
#include "v4/island/island_file.h"
#include "v4/island/setup_load.h"
#include "v4/format.h"
#include "v4/prep.h"
#include "v4/provenance.h"
#include "v4/stubs.h"
#include "v4/threads.h"

namespace v4::island {

namespace {
const char* W = "island: ";
std::string base_name(const std::string& p) { size_t k = p.find_last_of('/'); return k == std::string::npos ? p : p.substr(k + 1); }
std::string hex64(uint64_t x) { char b[19]; std::snprintf(b, sizeof b, "0x%016llx", (unsigned long long)x); return b; }
Json u64j(uint64_t x) { return Json((double)x); }   // byte counts < 2^53

// a whole number in [lo, hi] (no unchecked casts)
int64_t whole(const Json& v, const std::string& what, int64_t lo, int64_t hi) {
  if (v.type() != Json::NUM) throw Error(Status::invalid_input, W + what + " must be a number");
  const double x = v.num();
  if (!std::isfinite(x) || x != std::floor(x) || x < (double)lo || x > (double)hi)
    throw Error(Status::invalid_input, W + what + " must be a whole number in [" + std::to_string(lo) + ", " + std::to_string(hi) + "]");
  return (int64_t)x;
}
int64_t whole_arg(const Json& a, const char* k, int64_t dflt, int64_t lo, int64_t hi) {
  return a.contains(k) ? whole(a.at(k), std::string("--") + k, lo, hi) : dflt;
}
std::string str_arg(const Json& a, const char* k) {
  if (!a.contains(k)) return "";
  if (a.at(k).type() != Json::STR) throw Error(Status::invalid_input, std::string(W) + "--" + k + " must be a string");
  return a.at(k).str();
}
// --mem-budget (bytes) / --mem-budget-gb (GiB alias): a whole number of bytes in [0, 2^50], 0 = off (INTERFACES §1, §7)
uint64_t mem_budget_arg(const Json& a) {
  if (a.contains("mem_budget") && a.contains("mem_budget_gb")) throw Error(Status::invalid_input, std::string(W) + "give --mem-budget or --mem-budget-gb, not both");
  if (a.contains("mem_budget")) return (uint64_t)whole(a.at("mem_budget"), "--mem-budget", 0, (int64_t)1 << 50);
  if (a.contains("mem_budget_gb")) {
    if (a.at("mem_budget_gb").type() != Json::NUM) throw Error(Status::invalid_input, std::string(W) + "--mem-budget-gb must be a number");
    return (uint64_t)whole(Json(std::floor(a.at("mem_budget_gb").num() * 1073741824.0)), "--mem-budget-gb", 0, (int64_t)1 << 50);
  }
  return 0;
}

struct Inputs {
  Json manifest = Json::object();
  std::string data, setup, calib, out, mode;
  int64_t r = -1, seed = -1, Rp = -1;
};

// Resolves the inputs: the manifest (authority) and the explicit arguments; a disagreement is refused (as WP4's merge).
Inputs parse_inputs(const Json& args, bool plan_only) {
  Inputs in;
  if (args.contains("manifest")) {
    const Json& m = args.at("manifest");
    in.manifest = m.type() == Json::STR ? read_json_file(m.str()) : m;
    if (in.manifest.type() != Json::OBJ) throw Error(Status::invalid_input, std::string(W) + "--manifest is not a JSON object");
    if (in.manifest.contains("command") && (in.manifest.at("command").type() != Json::STR || in.manifest.at("command").str() != "island"))
      throw Error(Status::invalid_input, std::string(W) + "the manifest is not an island manifest (command)");
  }
  const bool has_man = in.manifest.size() > 0;
  const Json minp = in.manifest.contains("inputs") ? in.manifest.at("inputs") : Json::object();
  const Json mpar = in.manifest.contains("params") ? in.manifest.at("params") : Json::object();
  auto from_inputs = [&](const std::string& name) {
    std::string found;
    for (auto& [k, v] : minp.items()) if (base_name(k) == name) {
      if (!found.empty()) throw Error(Status::invalid_input, std::string(W) + "the manifest's inputs name " + name + " twice");
      found = k;
    }
    return found;
  };
  auto path_arg = [&](const char* key, const std::string& name, bool required) {
    const std::string f = from_inputs(name), a = str_arg(args, key);
    if (!a.empty() && !f.empty() && a != f) throw Error(Status::invalid_input, std::string(W) + "--" + key + " differs from the manifest's " + name);
    if (required && a.empty() && f.empty()) throw Error(Status::invalid_input, std::string(W) + "no " + name + " (give --" + key + " or a manifest input)");
    return a.empty() ? f : a;
  };
  in.data = path_arg("data", "data.bin", !plan_only);
  in.setup = path_arg("setup", "setup.bin", !plan_only);
  in.calib = path_arg("calib", "calib.bin", !plan_only);
  in.out = str_arg(args, "out");
  // mode: the manifest's, else --mode
  std::string mm;
  if (in.manifest.contains("mode")) {
    if (in.manifest.at("mode").type() != Json::STR) throw Error(Status::invalid_input, std::string(W) + "the manifest's mode must be a string");
    mm = in.manifest.at("mode").str();
  }
  const std::string ma = str_arg(args, "mode");
  if (!mm.empty() && !ma.empty() && mm != ma) throw Error(Status::invalid_input, std::string(W) + "--mode differs from the manifest's mode");
  in.mode = mm.empty() ? ma : mm;
  if (in.mode != "compat" && in.mode != "law" && in.mode != "V") throw Error(Status::invalid_input, std::string(W) + "--mode must be compat, law or V");
  // a whole-number parameter: the manifest's params (authority) or the argument; any disagreement is refused.
  // `args` holds the manifest's params too (main copies them), so an argument is compared with the manifest itself.
  auto param = [&](std::initializer_list<const char*> keys, int64_t lo, int64_t hi) -> int64_t {
    int64_t v = -1; std::string src;
    for (const char* k : keys) {
      for (int pass = 0; pass < 2; ++pass) {
        const Json& o = pass == 0 ? mpar : args;
        if (!o.contains(k)) continue;
        const std::string nm = (pass == 0 ? "manifest params." : "--") + std::string(k);
        const int64_t x = whole(o.at(k), nm, lo, hi);
        if (v >= 0 && x != v) throw Error(Status::invalid_input, W + nm + " = " + std::to_string(x) + " differs from " + src + " = " + std::to_string(v));
        if (v < 0) { v = x; src = nm; }
      }
    }
    return v;
  };
  in.r = param({"id", "island"}, 1, (1 << 20) - 1);       // INTERFACES §3: final island r = 1..R' < 2^20
  in.seed = param({"seed"}, 1, 2147483647);
  in.Rp = param({"Rp"}, 1, (1 << 20) - 1);
  if (in.Rp > 0 && in.r > in.Rp) throw Error(Status::invalid_input, std::string(W) + "island r = " + std::to_string(in.r) + " > R' = " + std::to_string(in.Rp));
  if (args.contains("role")) {   // calibration roles run inside `calibrate` (WP3_DESIGN §1.11)
    if (args.at("role").type() != Json::STR || args.at("role").str() != "final")
      throw Error(Status::invalid_input, std::string(W) + "--role must be final (pilot and diagnostic islands run inside calibrate)");
  }
  (void)has_man;
  return in;
}

// the calib.bin fields a final island needs (meta + grid; the stores are not loaded: at 10^6 they are GBs)
struct CalibHead { std::string hash, status, data_hash, setup_hash; uint32_t mode = 0; int32_t tier = 0, N = 0, L = 0, Hm = 4; double k_store = 0; int64_t seed = -1; std::vector<double> grid; };
CalibHead read_calib_head(const std::string& path) {
  fmt::Reader R(path);   // every section hash verified (INTERFACES §5.1)
  if (R.kind() != fmt::K_CALIB) throw Error(Status::invalid_input, path + ": not a calib file");
  CalibHead c; c.hash = R.content_hash(); c.mode = R.mode();
  const Json m = R.json("meta");
  c.status = m.at("status").str();
  if (c.status != "ok") throw Error(Status::invalid_input, path + ": calibration status " + c.status + " (no frozen grid)");
  c.tier = (int32_t)whole(m.at("tier"), "calib meta tier", 0, 1); c.N = (int32_t)whole(m.at("N"), "calib meta N", 1, 1 << 24);
  c.L = (int32_t)whole(m.at("L"), "calib meta L", 0, 1 << 16); c.Hm = (int32_t)whole(m.at("Hm"), "calib meta Hm", 1, 1 << 16);
  if (!m.contains("k_store") || m.at("k_store").type() != Json::NUM || !std::isfinite(m.at("k_store").num()) || !(m.at("k_store").num() > 0))
    throw Error(Status::invalid_input, path + ": k_store missing, or not finite and > 0");
  c.k_store = m.at("k_store").num();
  if (m.contains("seed")) c.seed = whole(m.at("seed"), "calib meta seed", 1, 2147483647);
  const Json& in = m.at("inputs");
  if (in.contains("data.bin")) c.data_hash = in.at("data.bin").str();
  if (in.contains("setup.bin")) c.setup_hash = in.at("setup.bin").str();
  c.grid = R.vec<double>("grid");
  if (c.grid.size() < 2 || c.grid.front() != 0.0 || c.grid.back() != 1.0) throw Error(Status::invalid_input, path + ": frozen grid does not run from 0 to 1");
  for (size_t i = 1; i < c.grid.size(); ++i) if (!(c.grid[i] > c.grid[i - 1])) throw Error(Status::invalid_input, path + ": frozen grid not strictly increasing");
  return c;
}

Json plan_json(const MemPlan& mp, uint64_t budget, double inputs_bytes, const char* label) {
  Json j = Json::object();
  j["label"] = label;
  Json items = Json::object(); for (const auto& it : mp.items) items[it.name] = u64j(it.bytes);
  j["items"] = items; j["total"] = u64j(mp.total); j["G"] = mp.G; j["k"] = mp.k; j["budget"] = u64j(budget);
  j["setup_inputs"] = inputs_bytes; j["admitted"] = budget == 0 || mp.total <= budget;
  j["text"] = mem_plan_text(mp);
  return j;
}

KernelKind kernel_of(uint32_t mode) { return mode == fmt::M_V ? KernelKind::LabelMajor : KernelKind::ParticleMajor; }
}  // namespace

Json run(const Json& args) {
  const bool plan_only = whole_arg(args, "plan_only", 0, 0, 1) == 1;
  const Inputs in = parse_inputs(args, plan_only);
  const uint32_t mode = fmt::mode_from_name(in.mode);
  const bool compat = mode == fmt::M_COMPAT;
  int threads = (int)whole_arg(args, "threads", threads_available(), 1, 4096);
  if (compat) threads = 1;   // serial v3 streams (D-21)
  const uint64_t budget = mem_budget_arg(args);
  const int G = (int)whole_arg(args, "G", 0, 0, 256), tile = (int)whole_arg(args, "tile", 128, 64, 4096);
  Json rec = Json::object();
  rec["mode"] = in.mode; rec["threads"] = threads; rec["kernel"] = kernel_of(mode) == KernelKind::LabelMajor ? "label_major" : "particle_major";

  // ---- plan without files (ESTIMATE): sizes from the arguments ----------------------------------------------------
  if (plan_only && in.data.empty()) {
    if (!in.setup.empty() || !in.calib.empty()) throw Error(Status::invalid_input, std::string(W) + "--plan-only with files needs --data, --setup and --calib");
    IslandConfig c; c.N = (int)whole_arg(args, "N", 2500, 1, 1 << 24); c.Hm = (int)whole_arg(args, "Hm", 4, 1, 1 << 16);
    c.kernel = kernel_of(mode); c.threads = threads; c.G = G; c.tile = tile; c.compat = compat; c.mem_budget = budget;
    c.inputs_bytes = (double)whole_arg(args, "inputs_bytes", 0, 0, (int64_t)1 << 50);
    const int64_t n = whole_arg(args, "n", 0, 3, (int64_t)1 << 31), p = whole_arg(args, "p", 0, 1, (int64_t)1 << 31);
    if (n < 3 || p < 1) throw Error(Status::invalid_input, std::string(W) + "--plan-only needs --data/--setup/--calib, or --n and --p");
    const double k = (double)whole_arg(args, "k", 8, 1, 1 << 16);
    const int K = (int)std::min<int64_t>(p, n / 2);   // the model cap K of data.bin (src/common/data.cpp)
    MemSizes z = plan_sizes((int)n, (int)p, K, c);
    MemPlan mp = plan_with_budget(z, k, c);
    rec["n"] = (double)n; rec["p"] = (double)p; rec["N"] = c.N;
    rec["mem_plan"] = plan_json(mp, budget, c.inputs_bytes, "ESTIMATE (final island plan from sizes: k given, setup inputs = --inputs-bytes)");
    rec["plan_only"] = true;
    rec["status"] = budget && mp.total > budget ? "resource_limit" : "completed";
    if (budget && mp.total > budget) rec["reason"] = "island not admitted: plan " + std::to_string(mp.total) + " B > --mem-budget";
    return rec;
  }

  // ---- inputs ----------------------------------------------------------------------------------------------------
  if (in.r < 1) throw Error(Status::invalid_input, std::string(W) + "the island index is required (--island r, or manifest params.id / params.island)");
  if (!plan_only && in.out.empty()) throw Error(Status::invalid_input, std::string(W) + "--out is required");
  if (!plan_only && in.seed < 1) throw Error(Status::invalid_input, std::string(W) + "--seed is required (a whole number in [1, 2^31 - 1])");
  auto t0 = std::chrono::steady_clock::now();
  const CalibHead C = read_calib_head(in.calib);
  if (C.mode != mode) throw Error(Status::invalid_input, std::string(W) + "calib.bin's mode is " + fmt::mode_name(C.mode) + ", not " + in.mode);
  if (in.seed > 0 && C.seed > 0 && C.seed != in.seed)
    throw Error(Status::invalid_input, std::string(W) + "--seed " + std::to_string(in.seed) + " differs from the calibration's seed " + std::to_string(C.seed));
  if (args.contains("N") && whole(args.at("N"), "N", 1, 1 << 24) != C.N)
    throw Error(Status::invalid_input, std::string(W) + "N differs from calib.bin's frozen N = " + std::to_string(C.N));
  std::string dhash, shash;
  Data D = prep::load_data(in.data, &dhash);
  { fmt::Reader R(in.setup);
    if (R.kind() != fmt::K_SETUP) throw Error(Status::invalid_input, in.setup + ": not a setup file");
    shash = R.content_hash();
    const Json m = R.json("meta");
    if (m.contains("inputs") && m.at("inputs").contains("data.bin") && m.at("inputs").at("data.bin").str() != dhash)
      throw Error(Status::invalid_input, std::string(W) + "setup.bin was built from another data.bin"); }
  if ((!C.data_hash.empty() && C.data_hash != dhash) || (!C.setup_hash.empty() && C.setup_hash != shash))
    throw Error(Status::invalid_input, std::string(W) + "calib.bin's meta.inputs differ from the data.bin / setup.bin in use");
  const Start st = load_start(in.setup, D);
  const Neighbours nb = load_neighbours(in.setup, D.p);
  const double t_load = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();

  IslandConfig c;
  c.seed = (uint32_t)std::max<int64_t>(1, in.seed); c.island = (uint32_t)in.r; c.role = IslandRole::Final; c.iter = 0; c.tier = (uint32_t)C.tier;
  c.N = C.N; c.grid = C.grid; c.L = C.L; c.Hm = C.Hm; c.B = (int)whole_arg(args, "B", 14, 1, 1 << 16);
  c.kernel = kernel_of(mode); c.threads = threads; c.G = G; c.tile = tile; c.compat = compat;
  c.k_store = C.k_store; c.inputs_bytes = start_bytes(st, nb);   // the setup inputs (dep::Start until StartView)
  c.mem_budget = budget; c.leaders = false; c.keep_terminal = true;
  const bool ckpt = whole_arg(args, "ckpt", 1, 0, 1) == 1;
  if (ckpt && !plan_only) {
    std::string b = in.out; if (b.size() > 4 && b.substr(b.size() - 4) == ".bin") b.resize(b.size() - 4);
    c.ckpt_path = b + ".ckpt";
    c.ckpt_every_s = (double)whole_arg(args, "ckpt_every_s", 600, 1, 1 << 30);
  }
  rec["r"] = (double)in.r; rec["N"] = C.N; rec["T"] = (double)C.grid.size() - 1; rec["L"] = C.L; rec["Hm"] = C.Hm; rec["tier"] = C.tier;
  rec["n"] = D.n; rec["p"] = D.p; rec["seed"] = (double)c.seed;
  Json inputs = Json::object(); inputs["data.bin"] = dhash; inputs["setup.bin"] = shash; inputs["calib.bin"] = C.hash;
  rec["inputs"] = inputs;
  // admission plan (the same plan_island run_island admits with)
  { MemSizes z; double k = 0; int Gp = 0;
    const MemPlan mp = plan_island(D, st, c, &z, &k, &Gp);
    rec["mem_plan"] = plan_json(mp, budget, c.inputs_bytes, "ESTIMATE (final island peak-live plan, memory.h; k = max(8, q90(pi_0) + 1, k_store))");
    if (plan_only) {
      rec["plan_only"] = true;
      rec["status"] = budget && mp.total > budget ? "resource_limit" : "completed";
      if (budget && mp.total > budget) rec["reason"] = "island not admitted: plan " + std::to_string(mp.total) + " B > --mem-budget";
      return rec;
    } }

  // ---- run ------------------------------------------------------------------------------------------------------
  const IslandRun r = mode == fmt::M_V ? run_island<Arith::ClassA>(D, st, nb, c) : run_island<Arith::Bit>(D, st, nb, c);
  if (r.status == 1) throw Error(Status::internal_error, std::string(W) + "island interrupted without a stop request");
  const std::string fhash = write_island_file(in.out, r, mode == fmt::M_V ? Arith::ClassA : Arith::Bit, inputs);
  const Status s = r.status == 0 ? Status::completed : r.status == 2 ? Status::numerical_failure : Status::resource_limit;
  if (s == Status::completed && !c.ckpt_path.empty()) { std::remove((c.ckpt_path + ".a").c_str()); std::remove((c.ckpt_path + ".b").c_str()); }
  rec["status"] = status_name(s);
  if (!r.reason.empty()) rec["reason"] = r.reason;
  rec["island_bin"] = fhash; rec["output_hash"] = hex64(r.hash()); rec["init_hash"] = hex64(r.init_hash);
  if (s == Status::completed) rec["logZ"] = r.logZ;
  rec["G_used"] = r.G_used; rec["resumed_from_step"] = r.resumed_from_step;
  Json t = Json::object(); t["load"] = t_load; t["island"] = r.ks.t_total; t["ckpt"] = r.ks.t_ckpt; t["store_check"] = r.ks.t_check;
  t["total"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  rec["seconds"] = t;
  return rec;
}

}  // namespace v4::island
